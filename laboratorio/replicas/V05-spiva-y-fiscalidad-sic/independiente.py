#!/usr/bin/env python3
"""V05 - Doble ejecucion independiente (auditor-de-replicas), 2026-09-25.

Escrito SIN leer `reproducir.py` ni `resultados.json`. Entradas: el pre-registro
(`prerregistro.md`, copia literal en el README) y los datos congelados en `datos/`,
cuyas huellas se revisan primero con hashlib.

V05 es sobre todo documental. Por eso cada cifra de SPIVA se lee de nuevo de los
PDF por DOS rutas propias que no comparten codigo:
  (a) texto por filas: el .txt congelado (extraccion pypdf) leido con expresiones
      regulares propias por encabezado de tabla y etiqueta de fila;
  (b) coordenadas: pdfminer.six sobre el PDF (otro extractor), reconstruyendo cada
      fila de la tabla por la posicion vertical de los numeros. Si pdfminer no esta
      instalado, la ruta (b) se omite y se avisa.
Las dos rutas deben coincidir; si no, el script falla.

Lo computacional (analisis B, liquidez, dividendos, impuesto sucesorio) se
re-implementa desde cero: lectura del JSON de Yahoo y del CSV de FRED, alineacion
por mes, conversion a MXN, CAGR, mezclas con rebalanceo mensual, interpolacion y
Newey-West(6) con dos formulas propias (suma de autocovarianzas con pesos de
Bartlett e identidad de sumas moviles). `herramientas.estadistica.newey_west` solo
se usa como tercera comprobacion del error estandar.

Las reglas fiscales se verifican buscando la frase literal en el texto primario
congelado (ley, DOF, IRS, tratados, Revenue, GBM), comparando sin espacios para
tolerar las palabras partidas por la extraccion de texto.

Al final compara cada cifra del README con la propia. Tolerancias: 0.01 pp en
medias mensuales e IC (%/mes); 0.05 en t; 0.1 pp en CAGR, ventaja de CAGR, pesos
de compensacion y brechas; 0.005 pp (igualdad al redondeo) en cifras leidas de
SPIVA y en tasas legales; igualdad exacta en conteos, montos del impuesto,
veredictos y estados documentales.

Salidas (sin red): independiente-resultados.json e independiente-comparacion.csv.
Uso, desde la raiz del repo:
    python3 laboratorio/replicas/V05-spiva-y-fiscalidad-sic/independiente.py
"""
import csv
import datetime as dt
import hashlib
import html
import json
import math
import os
import re
import statistics
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(BASE, "datos")
EXTRA = os.path.join(BASE, "independiente-datos")
RAIZ = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
Z = 1.959963984540054
REZ = 6
NUM = r"-?\d+\.\d{2}"


def leer(ruta):
    with open(ruta, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def plano(t):
    return re.sub(r"\s+", " ", t)


def compacto(t):
    return re.sub(r"\s+", "", t).lower()


def sin_html(t):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    return plano(html.unescape(re.sub(r"<[^>]+>", " ", t)))


# ---------------------------------------------------------------------------
# 0. Huellas
# ---------------------------------------------------------------------------
def huellas():
    listados, malos = set(), []
    with open(os.path.join(BASE, "SHA256SUMS.txt"), encoding="utf-8") as fh:
        for linea in fh:
            if not linea.strip():
                continue
            h, ruta = linea.split(None, 1)
            ruta = ruta.strip()
            listados.add(ruta)
            p = os.path.join(BASE, ruta)
            if not os.path.exists(p):
                malos.append(("falta", ruta))
                continue
            with open(p, "rb") as f:
                if hashlib.sha256(f.read()).hexdigest() != h:
                    malos.append(("difiere", ruta))
    no_listados = []
    for r, _, fs in os.walk(DATOS):
        for f in fs:
            rel = os.path.relpath(os.path.join(r, f), BASE)
            if rel not in listados:
                no_listados.append(rel)
    return {"listados": len(listados), "malos": malos, "no_listados": sorted(no_listados)}


# ---------------------------------------------------------------------------
# 1. SPIVA, ruta (a): texto por filas (.txt congelado, extraccion pypdf)
# ---------------------------------------------------------------------------
def txt_spiva(nombre):
    return leer(os.path.join(DATOS, "spiva", nombre + ".txt"))


def pagina_de(texto, pos):
    marcas = [(m.start(), int(m.group(1))) for m in re.finditer(r"===== PAGINA (\d+) =====", texto)]
    pag = None
    for p, n in marcas:
        if p <= pos:
            pag = n
    return pag


def fila_texto(nombre, encabezado, etiqueta, ncols, ventana=4000):
    """Primera fila `etiqueta` despues de un `encabezado` que tenga ncols numeros."""
    crudo = txt_spiva(nombre)
    for m in re.finditer(re.escape(encabezado), crudo):
        tramo = plano(crudo[m.start(): m.start() + ventana])
        j = tramo.find(etiqueta)
        if j < 0:
            continue
        nums = re.findall(r"(?<![\d.])" + NUM + r"(?![\d])", tramo[j + len(etiqueta): j + len(etiqueta) + 400])
        if len(nums) >= ncols:
            return [float(x) for x in nums[:ncols]], pagina_de(crudo, m.start())
    raise SystemExit(f"[ruta a] no encontre '{etiqueta}' tras '{encabezado}' en {nombre}")


def supervivencia_texto(nombre, encabezado, sub10, etiqueta):
    crudo = txt_spiva(nombre)
    i = crudo.find(encabezado)
    if i < 0:
        raise SystemExit(f"[ruta a] sin encabezado de supervivencia en {nombre}")
    tramo = plano(crudo[i: i + 20000])
    k = tramo.find(sub10)
    m = re.search(re.escape(etiqueta) + r" (\d+) (\d+\.\d{2})", tramo[k:])
    return int(m.group(1)), float(m.group(2)), pagina_de(crudo, i)


# ---------------------------------------------------------------------------
# 1. SPIVA, ruta (b): coordenadas con pdfminer sobre el PDF
# ---------------------------------------------------------------------------
try:
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LAParams, LTChar, LTTextLineHorizontal
    HAY_PDFMINER = True
except Exception:  # pragma: no cover
    HAY_PDFMINER = False

_CACHE_PAG = {}


def trozos_pagina(nombre, pagina):
    """Trozos de texto (x0, y0, x1, y1, texto) de una pagina; se parten en huecos > 2.5 pt."""
    clave = (nombre, pagina)
    if clave in _CACHE_PAG:
        return _CACHE_PAG[clave]
    ruta = os.path.join(DATOS, "spiva", nombre + ".pdf")
    lap = LAParams(char_margin=1.0, word_margin=0.1, line_margin=0.3)
    out = []

    def cerrar(tr):
        if tr:
            txt = "".join(c.get_text() for c in tr).strip()
            if txt:
                out.append((tr[0].x0, min(c.y0 for c in tr), tr[-1].x1, max(c.y1 for c in tr), txt))

    def recorrer(o):
        if isinstance(o, LTTextLineHorizontal):
            tr = []
            for c in o:
                if not isinstance(c, LTChar):
                    continue
                if tr and c.x0 - tr[-1].x1 > 2.5:
                    cerrar(tr)
                    tr = []
                tr.append(c)
            cerrar(tr)
            return
        if hasattr(o, "__iter__"):
            for h in o:
                recorrer(h)

    for pg in extract_pages(ruta, page_numbers=[pagina - 1], laparams=lap):
        recorrer(pg)
    _CACHE_PAG[clave] = out
    return out


def fila_coord(nombre, pagina, etiqueta, ncols, debajo_de=None, exige=None, solo_decimales=True):
    tr = trozos_pagina(nombre, pagina)
    if exige and not any(exige in t[4] for t in tr):
        raise SystemExit(f"[ruta b] la pagina {pagina} de {nombre} no contiene '{exige}'")
    cands = [t for t in tr if t[4].startswith(etiqueta)]
    if debajo_de:
        ref = [t for t in tr if t[4].startswith(debajo_de)]
        ytop = max(r[1] for r in ref)
        cands = [c for c in cands if c[1] < ytop]
    cands.sort(key=lambda t: -t[1])
    if not cands:
        raise SystemExit(f"[ruta b] sin etiqueta '{etiqueta}' en {nombre} p.{pagina}")
    lab = cands[0]
    esnum = re.compile(r"-?\d+(?:\.\d+)?")
    # filas candidatas: la de la etiqueta y, si no alcanza, las siguientes hacia abajo (etiquetas en 2 lineas)
    ys = sorted({round((t[1] + t[3]) / 2, 1) for t in tr if esnum.fullmatch(t[4]) and t[0] > lab[0]
                 and (lab[1] - 16) <= (t[1] + t[3]) / 2 <= lab[3] + 1}, reverse=True)
    for y in ys:
        nums = sorted([t for t in tr if esnum.fullmatch(t[4]) and abs((t[1] + t[3]) / 2 - y) <= 3 and t[0] > lab[0]],
                      key=lambda t: t[0])
        dec = [t for t in nums if "." in t[4]] if solo_decimales else nums
        if len(dec) >= ncols:
            return [float(t[4]) for t in (nums if len(nums) == ncols else dec)][:ncols], [float(t[4]) for t in nums]
    raise SystemExit(f"[ruta b] fila '{etiqueta}' incompleta en {nombre} p.{pagina}")


def metadatos_pdf(nombre):
    if not HAY_PDFMINER:
        return None
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfparser import PDFParser
    with open(os.path.join(DATOS, "spiva", nombre + ".pdf"), "rb") as fh:
        doc = PDFDocument(PDFParser(fh))
        info = doc.info[0] if doc.info else {}
        v = info.get("CreationDate")
        if hasattr(v, "resolve"):
            v = v.resolve()
        if isinstance(v, bytes):
            v = v.decode("latin-1")
        return v[2:10] if v else None


def corte(nombre):
    t = plano(txt_spiva(nombre))
    en = re.findall(r"Data as of ([A-Z][a-z]+)\.? (\d+), (\d{4})", t)
    es = re.findall(r"Datos al (\d+) de (\w+) de (\d{4})", t)
    meses = {"Dec": 12, "June": 6, "Sept": 9, "diciembre": 12, "junio": 6}
    fechas = [(int(a), meses[m], int(d)) for m, d, a in en if m in meses] + [(int(a), meses[m], int(d)) for d, m, a in es if m in meses]
    # la fecha de corte es la mas frecuente
    return max(set(fechas), key=fechas.count)


US = [
    # (edicion, archivo, encabezado, etiqueta, columnas)
    ("Year-End 2023", "spiva-us-year-end-2023", "Report 1a: Percentage of U.S. Equity Funds Underperforming", "All Large-Cap Funds", ["1a", "3a", "5a", "10a", "15a", "20a"]),
    ("Focus Mid-Year 2024", "spiva-us-mid-year-2024", "Report 3: Fund Underperformance Rates", "All Large-Cap", ["ytd", "1a", "3a", "5a", "10a", "15a", "20a"]),
    ("Year-End 2024", "spiva-us-year-end-2024", "Report 1a: Percentage of U.S. Equity Funds Underperforming", "All Large-Cap Funds", ["1a", "3a", "5a", "10a", "15a", "20a"]),
    ("Mid-Year 2025", "spiva-us-mid-year-2025", "Report 1a: Percentage of U.S. Equity Funds Underperforming", "All Large-Cap Funds", ["ytd", "1a", "3a", "5a", "10a", "15a", "20a"]),
    ("Year-End 2025", "spiva-us-year-end-2025", "Report 1a: Percentage of U.S. Equity Funds Underperforming", "All Large-Cap Funds", ["1a", "3a", "5a", "10a", "15a", "20a"]),
    ("Mid-Year 2026", "spiva-us-mid-year-2026", "Report 1a: Percentage of U.S. Equity Funds Underperforming", "All Large-Cap Funds", ["ytd", "1a", "3a", "5a", "10a", "15a", "20a"]),
]
LA = {
    "Year-End 2023": ("spiva-latin-america-scorecard-year-end-2023", "Report 1a: Percentage of Funds Underperforming", ["1a", "3a", "5a", "10a"],
                      {"mx": "Mexico Equity Funds"}, ("Report 2: Survivorship", "10-Year", "Mexico Equity Funds")),
    "Year-End 2024": ("spiva-latin-america-year-end-2024", "Report 1a: Percentage of Funds Underperforming", ["1a", "3a", "5a", "10a"],
                      {"mx": "Mexico Equity Funds", "eua_mxn": "U.S. Equity (MXN) Funds", "global_mxn": "Global Equity (MXN) Funds"},
                      ("Report 2: Survivorship", "10-Year", "Mexico Equity Funds")),
    "Primer semestre 2025": ("spiva-latin-america-mid-year-2025-es", "Tabla 1a: porcentaje de fondos superados", ["ytd", "1a", "3a", "5a", "10a"],
                             {"mx": "Renta variable de México", "eua_mxn": "Renta variable de EE. UU. (MXN)", "global_mxn": "Renta variable global (MXN)"},
                             ("Tabla 2: supervivencia", "10 años", "Renta variable de México")),
}
# etiquetas para la ruta (b) cuando la etiqueta de categoria ocupa dos lineas: se ancla en el indice
ANCLA_B = {"Renta variable de EE. UU. (MXN)": "S&P 500 (MXN)"}


def spiva():
    res = {"eua": {}, "latam": {}, "rutas": {}, "discrepancias_rutas": []}
    for ed, arch, enc, etq, cols in US:
        va, pag = fila_texto(arch, enc, etq, len(cols))
        fila = dict(zip(cols, va))
        fila.update({"pagina": pag, "corte": "%04d-%02d-%02d" % corte(arch), "creacion_pdf": metadatos_pdf(arch),
                     "tabla": enc.split(":")[0]})
        if HAY_PDFMINER:
            vb, _ = fila_coord(arch, pag, etq, len(cols), exige=enc.split(":")[0])
            if vb != va:
                res["discrepancias_rutas"].append((ed, etq, va, vb))
        res["eua"][ed] = fila
    for ed, (arch, enc, cols, etiquetas, sup) in LA.items():
        d = {"corte": "%04d-%02d-%02d" % corte(arch), "creacion_pdf": metadatos_pdf(arch)}
        for clave, etq in etiquetas.items():
            va, pag = fila_texto(arch, enc, etq, len(cols))
            if HAY_PDFMINER:
                eb = ANCLA_B.get(etq, etq)
                vb, _ = fila_coord(arch, pag, eb, len(cols), exige=enc.split(":")[0][:8])
                if vb != va:
                    res["discrepancias_rutas"].append((ed, etq, va, vb))
            d[clave] = dict(zip(cols, va))
            d[clave]["pagina"] = pag
        n0, s10, pag = supervivencia_texto(arch, *sup)
        if HAY_PDFMINER:
            # la tabla de supervivencia puede seguir en la pagina siguiente: se busca el bloque "10" en ambas
            ok = False
            for p in (pag, pag + 1, pag + 2):
                tr = trozos_pagina(arch, p)
                if any(t[4].startswith(sup[1]) for t in tr) and any(t[4].startswith(sup[2]) for t in tr):
                    try:
                        _, todos = fila_coord(arch, p, sup[2], 2, debajo_de=sup[1], solo_decimales=False)
                    except SystemExit:
                        continue
                    ok = todos[:2] == [float(n0), s10]
                    if ok:
                        break
            if not ok:
                res["discrepancias_rutas"].append((ed, "supervivencia 10", [n0, s10], None))
        d["superv10"] = {"fondos_iniciales": n0, "pct": s10, "sobrevivientes": round(n0 * s10 / 100)}
        res["latam"][ed] = d

    # Reports 3 y 4 (rendimientos anualizados), Year-End 2024
    arch = "spiva-latin-america-year-end-2024"
    r34 = {}
    for rep, enc in (("ew", "Report 3: Average Fund Performance (Equal-Weighted)"), ("aw", "Report 4: Average Fund Performance (Asset-Weighted)")):
        for etq in ("S&P/BMV IRT", "Mexico Equity Funds", "S&P 500 (MXN)", "U.S. Equity (MXN) Funds", "S&P World Index (MXN)", "Global Equity (MXN) Funds"):
            va, pag = fila_texto(arch, enc, etq, 4)
            if HAY_PDFMINER:
                vb, _ = fila_coord(arch, pag, etq, 4, exige=enc.split(":")[0])
                if vb != va:
                    res["discrepancias_rutas"].append(("R3/4 " + rep, etq, va, vb))
            r34.setdefault(etq, {})[rep] = dict(zip(["1a", "3a", "5a", "10a"], va))
    res["latam"]["Year-End 2024"]["reports_3_4"] = r34

    # A3: texto y Exhibit 8
    t = plano(txt_spiva(arch))
    a3 = {
        "texto_fuera_indice": float(re.search(r"outside of the S&P/BMV IRT benchmark was (\d+\.\d)%", t).group(1)),
        "texto_etfs_extranjeros": float(re.search(r"held an average of (\d+\.\d)% weight in foreign index funds and ETFs", t).group(1)),
        "texto_bajo_1a": float(re.search(r"where only (\d+\.\d)% of funds underperformed in 2024", t).group(1)),
    }
    m = re.search(r"Exhibit 8: Non-Benchmark Holdings.*?(\d+\.\d)% (\d+\.\d)% (\d+\.\d)% .*?Non-Benchmark Securities Offshore Securities Index Funds and ETFs", t)
    a3["grafica_texto_orden"] = [float(m.group(i)) for i in (1, 2, 3)]
    if HAY_PDFMINER:
        crudo = txt_spiva(arch)
        pag = pagina_de(crudo, crudo.find("Exhibit 8: Non-Benchmark Holdings"))
        tr = trozos_pagina(arch, pag)
        barras = [t_ for t_ in tr if re.fullmatch(r"\d+\.\d%", t_[4])]
        graf = {}
        for lab in ("Non-Benchmark Securities", "Offshore Securities", "Index Funds and ETFs"):
            L_ = [t_ for t_ in tr if t_[4].startswith(lab)][0]
            xc = (L_[0] + L_[2]) / 2
            b = min(barras, key=lambda t_: abs((t_[0] + t_[2]) / 2 - xc))
            graf[lab] = float(b[4][:-1])
        a3["grafica_coordenadas"] = graf
        a3["paginas"] = [pagina_de(crudo, crudo.find("outside of the S&P/BMV IRT")), pag]
        if [graf["Non-Benchmark Securities"], graf["Offshore Securities"], graf["Index Funds and ETFs"]] != a3["grafica_texto_orden"]:
            res["discrepancias_rutas"].append(("Exhibit 8", "barras", a3["grafica_texto_orden"], graf))
    res["a3"] = a3
    res["rutas"] = {"a_texto_pypdf": True, "b_coordenadas_pdfminer": HAY_PDFMINER}
    return res


# ---------------------------------------------------------------------------
# 2. Analisis B
# ---------------------------------------------------------------------------
def yahoo(nombre):
    with open(os.path.join(DATOS, "mercado", nombre), encoding="utf-8") as fh:
        return json.load(fh)["chart"]["result"][0]


def mensual_adj(nombre):
    r = yahoo(nombre)
    out = {}
    for t, a in zip(r["timestamp"], r["indicators"]["adjclose"][0]["adjclose"]):
        d = dt.datetime.fromtimestamp(t, dt.timezone.utc)
        k = (d.year, d.month)
        if k not in out and a is not None:  # la barra de inicio de mes; se ignora la cotizacion parcial repetida
            out[k] = a
    return out


def fx_fin_de_mes():
    out = {}
    with open(os.path.join(DATOS, "mercado", "fred_DEXMXUS.csv"), encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            v = fila["DEXMXUS"].strip()
            if v in ("", "."):
                continue
            f = dt.date.fromisoformat(fila["observation_date"])
            k = (f.year, f.month)
            if k not in out or f > out[k][0]:
                out[k] = (f, float(v))
    return out


def meses(a, b):
    y, m = a
    out = []
    while (y, m) <= b:
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def previo(k):
    return (k[0] - 1, 12) if k[1] == 1 else (k[0], k[1] - 1)


def cagr(r):
    g = 1.0
    for x in r:
        g *= 1 + x
    return g ** (12 / len(r)) - 1


def nw_autocov(x, L=REZ, corr=True):
    n = len(x)
    mu = sum(x) / n
    e = [v - mu for v in x]
    om = sum(v * v for v in e) / n
    for j in range(1, L + 1):
        om += 2 * (1 - j / (L + 1)) * sum(e[t] * e[t - j] for t in range(j, n)) / n
    return mu, math.sqrt(om / n * (n / (n - 1) if corr else 1.0))


def nw_sumas_moviles(x, L=REZ, corr=True):
    """Identidad: con L ceros a cada lado, sum_s (suma de L+1 residuos consecutivos)^2 / (L+1) = n * Omega."""
    n = len(x)
    mu = sum(x) / n
    e = [0.0] * L + [v - mu for v in x] + [0.0] * L
    tot = 0.0
    for s in range(0, n + L):
        S = sum(e[s: s + L + 1])
        tot += S * S
    om = tot / (L + 1) / n
    return mu, math.sqrt(om / n * (n / (n - 1) if corr else 1.0))


def veredicto(lo, hi):
    return "apoyo" if lo > 0 else ("contraria" if hi < 0 else "inconcluso")


def interp_peso(grid, obj):
    for (w0, a0), (w1, a1) in zip(grid, grid[1:]):
        if a0 <= obj <= a1:
            return w0 + (w1 - w0) * (obj - a0) / (a1 - a0)
    return None


def peso_exacto(ri, rs, obj):
    base = cagr(ri)
    lo, hi = 0.0, 1.0
    for _ in range(80):
        w = (lo + hi) / 2
        if cagr([(1 - w) * a + w * b for a, b in zip(ri, rs)]) - base < obj:
            lo = w
        else:
            hi = w
    return (lo + hi) / 2


def analisis_b():
    naf = mensual_adj("yahoo_NAFTRAC.MX_1mo_max.json")
    spy = mensual_adj("yahoo_SPY_1mo_max.json")
    fx = fx_fin_de_mes()
    try:
        sys.path.insert(0, RAIZ)
        from herramientas import estadistica as est  # tercera comprobacion
    except Exception:
        est = None
    ventanas = {"prereg_2015_2024": ((2015, 1), (2024, 12)), "expl_2024": ((2024, 1), (2024, 12)), "expl_2016_2025": ((2016, 1), (2025, 12))}
    pesos = [0.0, 0.10, 0.164, 0.20, 0.30, 0.50, 1.0]
    grid_w = [0.0, 0.10, 0.20, 0.30, 0.50, 1.0]  # rejilla pre-registrada
    out = {}
    for nom, (a, b) in ventanas.items():
        ks = meses(a, b)
        ri = [naf[k] / naf[previo(k)] - 1 for k in ks]
        rs = [spy[k] * fx[k][1] / (spy[previo(k)] * fx[previo(k)][1]) - 1 for k in ks]
        base = cagr(ri)
        mezclas = {}
        for w in pesos:
            c = cagr([(1 - w) * x + w * y for x, y in zip(ri, rs)])
            mezclas["%g" % (100 * w)] = {"cagr_pct": 100 * c, "ventaja_pp": 100 * (c - base)}
        grid = [(100 * w, mezclas["%g" % (100 * w)]["ventaja_pp"]) for w in grid_w]
        d = [y - x for x, y in zip(ri, rs)]
        mu, se1 = nw_autocov(d)
        _, se2 = nw_sumas_moviles(d)
        _, se_sin = nw_autocov(d, corr=False)
        se3 = est.newey_west(d, REZ)["se"] if est else None
        lo, hi = mu - Z * se1, mu + Z * se1
        out[nom] = {
            "n": len(ks), "desde": "%d-%02d" % ks[0], "hasta": "%d-%02d" % ks[-1],
            "fx_primero": fx[previo(ks[0])][0].isoformat(), "fx_ultimo": fx[ks[-1]][0].isoformat(),
            "ipc_cagr_pct": 100 * base, "sp_mxn_cagr_pct": 100 * cagr(rs), "mezclas": mezclas,
            "peso_compensa_pct": {str(g): interp_peso(grid, g) for g in (1, 2, 3)},
            "peso_compensa_exacto_pct": {str(g): 100 * peso_exacto(ri, rs, g / 100) for g in (1, 2, 3)},
            "dif_media_pct_mes": 100 * mu, "se_nw_pct": 100 * se1, "t_nw": mu / se1,
            "t_nw_sin_correccion": mu / se_sin, "t_iid": mu / (statistics.stdev(d) / math.sqrt(len(d))),
            "ic95_pct": [100 * lo, 100 * hi], "veredicto": veredicto(lo, hi),
            "se_formula2_menos_formula1": se2 - se1, "se_herramientas_menos_formula1": (se3 - se1) if se3 is not None else None,
        }
    # sesgo de NAFTRAC y SPY contra los indices de SPIVA (Report 3, 10 anos a 2024)
    return out, naf, spy, fx


# ---------------------------------------------------------------------------
# 3. Descriptivos: liquidez SIC, dividendo de SPY, impuesto sucesorio
# ---------------------------------------------------------------------------
TICKERS = ["CSPXN.MX", "VUAAN.MX", "IUSAN.MX", "IWDAN.MX", "VWRAN.MX", "ISACN.MX", "EIMIN.MX", "CNDXN.MX", "IVV.MX", "VOO.MX", "SPY.MX"]


def liquidez():
    out = {}
    for tk in TICKERS:
        r = yahoo(f"yahoo_{tk}_1d_1y.json")
        q = r["indicators"]["quote"][0]
        valores = [(c or 0.0) * (v or 0) for c, v in zip(q["close"], q["volume"])]
        cierres = [(t, c) for t, c in zip(r["timestamp"], q["close"]) if c is not None]
        out[tk] = {
            "precio_meta": r["meta"].get("regularMarketPrice"), "ultimo_cierre": cierres[-1][1],
            "fecha_ultima": dt.datetime.fromtimestamp(r["timestamp"][-1], dt.timezone.utc).date().isoformat(),
            "sesiones": len(r["timestamp"]), "con_volumen": sum(1 for v in q["volume"] if v and v > 0),
            "mediana_valor_mxn": statistics.median(valores), "moneda": r["meta"].get("currency"),
            "bolsa": r["meta"].get("exchangeName"), "nombre": r["meta"].get("longName"),
        }
    return out


def dividendo_spy():
    r = yahoo("yahoo_SPY_1d_2y_div.json")
    divs = sorted((int(k), v["amount"]) for k, v in r["events"]["dividends"].items())
    t_fin = r["timestamp"][-1]
    cierre = r["indicators"]["quote"][0]["close"][-1]
    ttm = [(t, a) for t, a in divs if t > t_fin - 365 * 86400]
    y = sum(a for _, a in ttm) / cierre
    return {"n_dividendos_12m": len(ttm), "suma_12m_usd": sum(a for _, a in ttm), "cierre": cierre,
            "fecha": dt.datetime.fromtimestamp(t_fin, dt.timezone.utc).date().isoformat(),
            "rend_div_pct": 100 * y, "fuga_pp": {"10": 100 * y * 0.10, "15": 100 * y * 0.15, "30": 100 * y * 0.30}}


def tarifa_2001c():
    t = plano(leer(os.path.join(DATOS, "legal", "usc-26-2001.txt")))
    tramos = []
    m = re.search(r"Not over \$10,000 (\d+) percent of such amount", t)
    tramos.append((0.0, 0.0, int(m.group(1)) / 100))
    for m in re.finditer(r"Over \$([\d,]+) but not over \$([\d,]+) \$([\d,]+),? plus (\d+) percent of the excess of such amount over \$([\d,]+)", t):
        lo, _, base, tasa, sobre = m.groups()
        assert lo == sobre
        tramos.append((float(lo.replace(",", "")), float(base.replace(",", "")), int(tasa) / 100))
    m = re.search(r"Over \$1,000,000 \$([\d,]+), plus (\d+) percent of the excess of such amount over \$1,000,000", t)
    tramos.append((1_000_000.0, float(m.group(1).replace(",", "")), int(m.group(2)) / 100))
    tramos.sort()
    # continuidad de la tarifa (control interno): base_k+1 = base_k + tasa_k * ancho_k
    for (l0, b0, r0), (l1, b1, _) in zip(tramos, tramos[1:]):
        assert abs(b0 + r0 * (l1 - l0) - b1) < 0.5, (l0, l1)
    t2 = plano(leer(os.path.join(DATOS, "legal", "usc-26-2102.txt")))
    credito = float(re.search(r"A credit of \$([\d,]+) shall be allowed against the tax imposed by section 2101", t2).group(1).replace(",", ""))
    return tramos, credito


def impuesto_sucesorio(fx):
    tramos, credito = tarifa_2001c()

    def tentativo(x):
        lo, base, tasa = [tr for tr in tramos if tr[0] <= x][-1]
        return base + tasa * (x - lo)
    f_tc, tc = max(fx.values())
    filas = {}
    for usd in (20000 / tc, 60000, 100000, 250000, 500000, 1000000):
        imp = max(0.0, tentativo(usd) - credito)
        filas["%.0f" % usd] = {"usd": usd, "mxn": usd * tc, "impuesto_usd": imp, "tasa_efectiva_pct": 100 * imp / usd}
    return {"tc": tc, "fecha_tc": f_tc.isoformat(), "credito": credito, "tarifa_min_pct": 100 * tramos[0][2],
            "tarifa_max_pct": 100 * tramos[-1][2], "n_tramos": len(tramos), "filas": filas}


# ---------------------------------------------------------------------------
# 4. Citas legales: frase literal en la fuente primaria congelada
# ---------------------------------------------------------------------------
def fuente(nombre):
    if nombre.startswith("extra:"):
        return leer(os.path.join(EXTRA, nombre[6:]))
    t = leer(os.path.join(DATOS, "legal", nombre))
    return sin_html(t) if nombre.endswith(".html") else t


CITAS = [
    ("L01", "ISR 10% definitivo sobre ganancias en bolsa", ["LISR.txt"], ["cuyo pago se considerará como definitivo, aplicando la tasa del 10% a las ganancias obtenidas en el ejercicio"]),
    ("L02", "Art. 129 fr. I incluye acciones extranjeras cotizadas en bolsa", ["LISR.txt"], ["o de acciones emitidas por sociedades extranjeras cotizadas en dichas bolsas de valores o mercados de derivados"]),
    ("L03", "Art. 129 fr. II incluye títulos que representen índices accionarios", ["LISR.txt"], ["La enajenación de títulos que representen índices accionarios enajenados en las bolsas de valores o mercados de derivados"]),
    ("L04", "Pérdidas solo contra ganancias del mismo tipo, en el ejercicio o en los 10 siguientes", ["LISR.txt"], ["podrán disminuir dicha pérdida únicamente contra el monto de la ganancia que en su caso obtenga el mismo contribuyente en el ejercicio o en los diez siguientes"]),
    ("L05", "Pérdidas actualizadas por inflación", ["LISR.txt"], ["las pérdidas se actualizarán por el periodo comprendido desde el mes en que ocurrieron"]),
    ("L06", "Si pudiendo no se disminuye la pérdida, se pierde", ["LISR.txt"], ["pudiendo haberlo hecho conforme a este artículo, perderá el derecho a hacerlo en los ejercicios posteriores y hasta por la cantidad en la que pudo haberlo efectuado"]),
    ("L07", "Declaración junto con la anual del art. 150", ["LISR.txt"], ["deberá entregarse de manera conjunta a la declaración anual a que se refiere el artículo 150"]),
    ("L08", "El intermediario expide las constancias", ["LISR.txt"], ["los intermediarios del mercado de valores deberán expedir las constancias correspondientes"]),
    ("L09", "GBM: sin retención en la venta y 10% anual", ["gbm_como-funcionan-los-impuestos-por-las-acciones-de-empresas-extranjeras-en-el-sic.txt"], ["No tiene ninguna retención. Pago del ISR anual del 10% sobre las ganancias"]),
    ("L10", "GBM: constancias 2025 en la app; sin CFDI para Trading USA", ["gbm_como-y-donde-recibo-los-comprobantes-fiscales-o-cfdi-por-mis-ganancias.txt", "gbm_como-funcionan-los-impuestos-por-las-acciones-de-empresas-extranjeras-en-el-sic.txt"],
     ["Tus Constancias Fiscales (o CFDI) por las ganancias del 2025 ya están disponibles en tu app GBM", "GBM sí emite CFDI para Trading MX y SIC, pero no para Trading USA"]),
    ("L11", "LIF 2026 art. 24: retención anual 0.90% (arts. 54 y 135 LISR)", ["LIF_2026.txt"], ["Durante el ejercicio fiscal de 2026 la tasa de retención anual a que se refieren los artículos 54 y 135 de la Ley del Impuesto sobre la Renta será del 0.90 por ciento"]),
    ("L12", "LIF 2026 publicada en el DOF el 7-nov-2025, vigente desde 01-01-2026", ["LIF_2026.txt"], ["Nueva Ley publicada en el Diario Oficial de la Federación el 7 de noviembre de 2025", "TEXTO VIGENTE a partir del 01-01-2026"]),
    ("L13", "Retención sobre el capital, como pago provisional (arts. 54 y 135)", ["LISR.txt"], ["sobre el monto del capital que dé lugar al pago de los intereses, como pago provisional"]),
    ("L14", "Dividendos mexicanos: acumulación, acreditamiento del ISR corporativo y 10% adicional retenido definitivo", ["LISR.txt"],
     ["Las personas físicas deberán acumular a sus demás ingresos, los percibidos por dividendos o utilidades", "tasa adicional del 10% sobre los dividendos o utilidades distribuidos por las personas morales residentes en México", "El pago realizado conforme a este párrafo será definitivo"]),
    ("L15", "Dividendos extranjeros: acumulación más 10% adicional definitivo (art. 142 fr. V)", ["LISR.txt"],
     ["V. Los dividendos o utilidades distribuidos por sociedades residentes en el extranjero", "además de acumularlos para efectos de determinar el pago del impuesto sobre la renta", "deberán enterar de forma adicional, el impuesto sobre la renta que se cause por multiplicar la tasa del 10%", "El pago de este impuesto tendrá el carácter de definitivo"]),
    ("L16", "Base del 10% adicional: sin incluir el impuesto retenido (neto)", ["LISR.txt"], ["al monto al cual tengan derecho del dividendo o utilidad efectivamente distribuido por el residente en el extranjero, sin incluir el monto del impuesto retenido que en su caso se hubiere efectuado"]),
    ("L17", "Acreditamiento del impuesto pagado en el extranjero (art. 5)", ["LISR.txt"], ["podrán acreditar, contra el impuesto que conforme a esta Ley les corresponda pagar, el impuesto sobre la renta que hayan pagado en el extranjero"]),
    ("L18", "GBM: EUA retiene 30% o 10% con W-8BEN; México 10% sobre neto", ["gbm_como-funcionan-los-impuestos-sobre-los-dividendos-en-trading-mx.txt"],
     ["Si es de Estados Unidos, es del 30%, que baja al 10% si tienes tu W-8BEN vigente", "La segunda retención es en México del 10%, sobre monto neto, después del impuesto retenido en el extranjero"]),
    ("L19", "Tratado México-EUA art. 10: 10% en dividendos de cartera", ["irs-tratado-eua-mexico.txt"], ["b) 10 percent of the gross amount of the dividends in other cases"]),
    ("L20", "LISR: última reforma DOF 01-04-2024 (texto de la Cámara)", ["LISR.txt", "extra:diputados-lisr-ref.txt"],
     ["Última reforma publicada DOF 01-04-2024", "Última reforma publicada en el Diario Oficial de la Federación el 1 de abril de 2024"]),
    ("L21", "706-NA: umbral de declaración de 60,000 USD (instrucciones 09/2025)", ["irs-instrucciones-706NA.txt", "irs-instrucciones-706NA.html"], ["exceeds the filing threshold of $60,000", "Revised: 09/2025"]),
    ("L22", "Crédito unificado de 13,000 USD (706-NA y 26 USC 2102(b)(1))", ["irs-instrucciones-706NA.txt", "usc-26-2102.txt"], ["In general, the maximum unified credit is $13,000", "A credit of $13,000 shall be allowed against the tax imposed by section 2101"]),
    ("L23", "Tarifa 26 USC 2001(c): de 18% a 40%", ["usc-26-2001.txt"], ["Not over $10,000 18 percent of such amount", "Over $1,000,000 $345,800, plus 40 percent of the excess of such amount over $1,000,000"]),
    ("L24", "Tratados sucesorios: 15 países, sin México", ["irs-instrucciones-706NA.txt", "irs-instrucciones-706NA.html"],
     ["Death tax treaties are in effect with the following countries. Australia Ireland Austria Italy Canada* Japan Denmark Netherlands Finland South Africa France Switzerland Germany United Kingdom Greece"]),
    ("L25", "Situs: acciones de sociedad de EUA sin importar dónde estén los certificados", ["ecfr-26CFR20.2104-1.txt", "ecfr-26CFR20.2104-1.html"], ["Shares of stock issued by a domestic corporation, irrespective of the location of the certificates"]),
    ("L26", "Excepción RIC terminó para fallecimientos después del 31-dic-2011", ["usc-26-2105.txt"], ["This subsection shall not apply to estates of decedents dying after December 31, 2011"]),
    ("L27", "Tratado EUA-Irlanda art. 10: 15% en dividendos de cartera", ["irs-tratado-eua-irlanda.txt"], ["b) 15 percent of the gross amount of the dividends in all other cases"]),
    ("L28", "CAT irlandés s.75: exención si causante y heredero no tienen domicilio ni residencia habitual en Irlanda", ["revenue-ie-cat-notas-guia-part09.txt"],
     ["the disponer is neither domiciled nor ordinarily resident in the State at the date of the disposition", "the beneficiary is neither domiciled nor ordinarily resident in the State at the time the gift or inheritance is taken"]),
    ("L29", "REFIPRE (art. 176) solo con control efectivo", ["LISR.txt"], ["Lo dispuesto en este Capítulo sólo será aplicable cuando el contribuyente ejerza el control efectivo sobre la entidad extranjera"]),
    ("L30", "GBM: W-8BEN reduce la retención de 30% a 10%", ["gbm_que-es-y-como-funciona-el-w-8ben-para-trading-mx-y-sic.txt"], ["se reduce la retención en el extranjero sobre tus ganancias del 30% al 10%"]),
    ("L31", "iShares: CSPX e IUSA domiciliados en Irlanda, TER 0.07% (página del emisor, consulta en vivo 2026-09-25)", ["extra:ishares-CSPX-253743.txt", "extra:ishares-IUSA-251900.txt"],
     ["Domicile Ireland", "ISIN IE00B5BMR087", "Total Expense Ratio 0.07%", "Use of Income Accumulating", "ISIN IE0031442068", "Use of Income Distributing"]),
]


def citas():
    textos = {}
    out = []
    for cid, desc, fuentes, frases in CITAS:
        comp = {}
        for f in fuentes:
            if f not in textos:
                textos[f] = compacto(fuente(f))
            comp[f] = textos[f]
        faltan = [fr for fr in frases if not any(compacto(fr) in c for c in comp.values())]
        out.append({"id": cid, "regla": desc, "fuentes": fuentes, "frases": len(frases), "faltan": faltan, "ok": not faltan})
    # Mexico no aparece en la lista de tratados sucesorios
    t = plano(fuente("irs-instrucciones-706NA.txt"))
    i = t.find("Death tax treaties are in effect with the following countries.")
    lista = t[i: t.find("*Article XXIX B", i)]
    paises = ["Australia", "Ireland", "Austria", "Italy", "Canada", "Japan", "Denmark", "Netherlands", "Finland", "South Africa", "France", "Switzerland", "Germany", "United Kingdom", "Greece"]
    out.append({"id": "L24b", "regla": "Lista de tratados: 15 países y México ausente", "fuentes": ["irs-instrucciones-706NA.txt"],
                "frases": 1, "faltan": [] if (all(p in lista for p in paises) and "Mexico" not in lista) else ["lista"],
                "ok": all(p in lista for p in paises) and "Mexico" not in lista, "n_paises": len(paises)})
    return out


# ---------------------------------------------------------------------------
# 5. Comparacion con el README
# ---------------------------------------------------------------------------
README = leer(os.path.join(BASE, "README.md"))
COMP = []


def seccion(inicio, fin_prefijo="### "):
    i = README.find(inicio)
    if i < 0:
        raise SystemExit(f"README sin seccion '{inicio}'")
    j = README.find("\n" + fin_prefijo, i + len(inicio))
    k = README.find("\n## ", i + len(inicio))
    cands = [x for x in (j, k) if x > 0]
    return README[i: min(cands) if cands else len(README)]


def celdas(sec, prefijo):
    for linea in sec.splitlines():
        if linea.startswith(prefijo):
            return [c.strip() for c in linea.strip().strip("|").split("|")]
    raise SystemExit(f"README: fila '{prefijo}' no encontrada")


def nums_str(celda):
    c = celda.replace("−", "-").replace("**", "").replace(",", "")
    return re.findall(r"[-+]?\d+(?:\.\d+)?", c)


def comparar(bloque, concepto, readme, propio, tol=0, nota=""):
    fila = {"bloque": bloque, "concepto": concepto, "readme": readme, "propio": propio, "tolerancia": tol, "nota": nota}
    if isinstance(propio, str):
        fila.update(tipo="categorica", diferencia="", dentro=(readme == propio), identica=(readme == propio))
    elif readme is None or readme == "":
        fila.update(tipo="numerica", diferencia="", dentro=False, identica=False, readme="(sin cifra)")
    else:
        r = float(str(readme).replace("+", ""))
        dec = len(str(readme).split(".")[1]) if "." in str(readme) else 0
        dif = propio - r
        fila.update(tipo="numerica", diferencia=dif, dentro=abs(dif) <= tol + 1e-9,
                    identica=("%.*f" % (dec, propio + (1e-9 if propio >= 0 else -1e-9)) == "%.*f" % (dec, r)))
    COMP.append(fila)


MESES_ES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
H_GLOBAL = {}
REEXTRACCION = {}


def comparar_publicacion(bloque, ed, celda, creacion):
    """Fecha de publicacion del README contra la fecha de creacion del PDF (metadatos).
    Igual mes -> 'verificada'. README anterior a los metadatos -> 'no contradicha' (PDF regenerado;
    la fuente de la fecha del README no esta congelada). README posterior -> 'contradicha'."""
    m = re.search(r"(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)\w*[- ]+(?:\w+[- ]+)?(\d{4})", celda)
    if not m or not creacion:
        comparar(bloque, f"{ed}: publicación", celda, "(sin fecha comparable)")
        return
    rd = (int(m.group(2)), MESES_ES[m.group(1)])
    md = (int(creacion[:4]), int(creacion[4:6]))
    estado = "verificada" if rd == md else ("no contradicha" if rd < md else "contradicha")
    fila = {"bloque": bloque, "concepto": f"{ed}: publicación ({celda}) vs creación del PDF {creacion[:4]}-{creacion[4:6]}-{creacion[6:8]}",
            "readme": celda, "propio": estado, "tolerancia": "", "tipo": "categorica", "diferencia": "",
            "dentro": estado != "contradicha", "identica": estado == "verificada",
            "nota": "" if estado == "verificada" else "metadatos regenerados por S&P; la fecha del README viene de una fuente no congelada"}
    COMP.append(fila)


def reextraccion_pypdf():
    """Re-extrae con pypdf (si esta instalado) en el formato documentado en datos/extraer_texto.py."""
    try:
        import pypdf
    except Exception:
        return {"hecha": False}
    pares = [(os.path.join("spiva", f[:-4] + ".pdf"), os.path.join("spiva", f)) for f in sorted(os.listdir(os.path.join(DATOS, "spiva"))) if f.endswith(".txt")]
    pares += [("legal/LIF_2026.pdf", "legal/LIF_2026.txt"), ("legal/LISR-texto-vigente-ult-ref-DOF-2024-04-01.pdf", "legal/LISR.txt"),
              ("legal/irs-tratado-eua-mexico.pdf", "legal/irs-tratado-eua-mexico.txt"), ("legal/irs-tratado-eua-irlanda.pdf", "legal/irs-tratado-eua-irlanda.txt")]
    iguales = {}
    for pdf, txt in pares:
        r = pypdf.PdfReader(os.path.join(DATOS, pdf))
        texto = "".join("\n===== PAGINA %d =====\n" % i + (p.extract_text() or "") for i, p in enumerate(r.pages, 1))
        iguales[pdf] = texto == leer(os.path.join(DATOS, txt))
    return {"hecha": True, "version_pypdf": pypdf.__version__, "iguales": iguales,
            "spiva_identicos": sum(v for k, v in iguales.items() if k.startswith("spiva")),
            "legales_identicos": sum(v for k, v in iguales.items() if k.startswith("legal"))}


def comparar_texto(bloque, concepto, patron, propios, tol, sec=None):
    t = sec if sec is not None else README
    m = re.search(patron, t)
    if not m:
        COMP.append({"bloque": bloque, "concepto": concepto, "readme": "(texto no encontrado)", "propio": str(propios),
                     "tolerancia": tol, "tipo": "texto", "diferencia": "", "dentro": False, "identica": False, "nota": patron})
        return
    for g, p in zip(m.groups(), propios):
        comparar(bloque, concepto, g.replace("−", "-").replace(",", ""), p, tol)


def comparar_readme(S, B, liq, div, suc, cit):
    eua, la = S["eua"], S["latam"]
    # --- Tabla 1 (A1)
    sec = seccion("### 1. A1")
    filas = {"Year-End 2023": "| Year-End 2023 |", "Focus Mid-Year 2024": "| Focus Mid-Year 2024 |", "Year-End 2024": "| Year-End 2024 |",
             "Mid-Year 2025": "| Mid-Year 2025 |", "Year-End 2025": "| **Year-End 2025** |", "Mid-Year 2026": "| **Mid-Year 2026 (la más reciente)** |"}
    meses_es = {12: "dic", 6: "jun"}
    for ed, pref in filas.items():
        c = celdas(sec, pref)
        y, m, d = map(int, eua[ed]["corte"].split("-"))
        comparar("1. A1 (Report 1a)", f"{ed}: corte", c[1], f"{d:02d}-{meses_es[m]}-{y}")
        for idx, col in zip(range(3, 10), ["ytd", "1a", "3a", "5a", "10a", "15a", "20a"]):
            if col not in eua[ed]:
                continue
            n = nums_str(c[idx]) if idx < len(c) else []
            comparar("1. A1 (Report 1a)", f"{ed}: {col}", n[0] if n else None, eua[ed][col], 0.005)
    for ed, pref in filas.items():
        comparar_publicacion("1. A1 (publicación)", ed, celdas(sec, pref)[2], eua[ed]["creacion_pdf"])
    rango10 = [eua[e]["10a"] for e in eua]
    rango1520 = [eua[e][k] for e in eua for k in ("15a", "20a")]
    comparar_texto("1. A1 (veredicto)", "rango 10 años (%)", r"\*\*de (\d+)% a (\d+)%\*\* de los fondos \*large-cap\* quedaron debajo del S&P 500 a 10 años", [min(rango10), max(rango10)], 0.5, sec)
    comparar_texto("1. A1 (veredicto)", "rango 15 y 20 años (%)", r"\*\*de (\d+)% a (\d+)%\*\* a 15 y 20 años", [min(rango1520), max(rango1520)], 0.5, sec)
    # --- Tabla 2 (A2)
    sec = seccion("### 2. A2")
    for ed, pref, cols in (("Year-End 2023", "| Year-End 2023 |", ["1a", "3a", "5a", "10a"]), ("Year-End 2024", "| **Year-End 2024** |", ["1a", "3a", "5a", "10a"]),
                           ("Primer semestre 2025", "| Primer semestre 2025 (español) |", ["ytd", "1a", "3a", "5a", "10a"])):
        c = celdas(sec, pref)
        y, m, d = map(int, la[ed]["corte"].split("-"))
        comparar("2. A2 (Tabla 1a)", f"{ed}: corte", c[1], f"{d:02d}-{meses_es[m]}-{y}")
        comparar_publicacion("2. A2 (publicación)", ed, c[2], la[ed]["creacion_pdf"])
        for idx, col in zip(range(3, 8), ["ytd", "1a", "3a", "5a", "10a"]):
            if col not in cols:
                continue
            comparar("2. A2 (Tabla 1a)", f"{ed}: {col}", nums_str(c[idx])[0], la[ed]["mx"][col], 0.005)
        sv = nums_str(c[8])
        comparar("2. A2 (supervivencia)", f"{ed}: supervivencia 10 años %", sv[0], la[ed]["superv10"]["pct"], 0.005)
        comparar("2. A2 (supervivencia)", f"{ed}: fondos iniciales", sv[1], float(la[ed]["superv10"]["fondos_iniciales"]), 0)
    comparar_texto("2. A2 (contexto)", "EUA (MXN) 10 años, YE2024 y mitad 2025", r"S&P 500 \(MXN\): \*\*(\d+\.\d+)%\*\* en cierre de 2024 y en mitad de 2025", [la["Year-End 2024"]["eua_mxn"]["10a"]], 0.005, sec)
    comparar("2. A2 (contexto)", "EUA (MXN) 10 años mitad 2025 = YE2024", "86.67", la["Primer semestre 2025"]["eua_mxn"]["10a"], 0.005)
    comparar_texto("2. A2 (contexto)", "Global (MXN) 10 años, ambas", r"S&P World \(MXN\): \*\*(\d+)%\*\* en ambas", [la["Year-End 2024"]["global_mxn"]["10a"]], 0.005, sec)
    comparar("2. A2 (contexto)", "Global (MXN) 10 años mitad 2025", "100", la["Primer semestre 2025"]["global_mxn"]["10a"], 0.005)
    r34 = la["Year-End 2024"]["reports_3_4"]
    for pref, etq in (("| S&P/BMV IRT |", "S&P/BMV IRT"), ("| Fondos Mexico Equity (equiponderado / por activos) |", "Mexico Equity Funds"),
                      ("| S&P 500 (MXN) |", "S&P 500 (MXN)"), ("| Fondos U.S. Equity (MXN) |", "U.S. Equity (MXN) Funds"),
                      ("| S&P World (MXN) |", "S&P World Index (MXN)"), ("| Fondos Global Equity (MXN) |", "Global Equity (MXN) Funds")):
        c = celdas(sec, pref)
        for idx, col in zip(range(1, 5), ["1a", "3a", "5a", "10a"]):
            n = nums_str(c[idx])
            comparar("2. Reports 3 y 4", f"{etq}: {col} EW", n[0], r34[etq]["ew"][col], 0.005)
            if etq.startswith("Fondos") or "Funds" in etq:
                comparar("2. Reports 3 y 4", f"{etq}: {col} AW", n[1], r34[etq]["aw"][col], 0.005)
            else:
                comparar("2. Reports 3 y 4", f"{etq}: {col} AW = EW (índice)", n[0], r34[etq]["aw"][col], 0.005)
    # --- A3
    sec = seccion("### 3. A3")
    a3 = S["a3"]
    g = a3.get("grafica_coordenadas") or dict(zip(["Non-Benchmark Securities", "Offshore Securities", "Index Funds and ETFs"], a3["grafica_texto_orden"]))
    c = celdas(sec, "| Valores fuera del S&P/BMV IRT |")
    comparar("3. A3", "fuera del índice: texto", nums_str(c[1])[0], a3["texto_fuera_indice"], 0.005)
    comparar("3. A3", "fuera del índice: gráfica", nums_str(c[2])[0], g["Non-Benchmark Securities"], 0.005)
    c = celdas(sec, "| Valores *offshore*")
    comparar("3. A3", "offshore: gráfica", nums_str(c[2])[0], g["Offshore Securities"], 0.005)
    c = celdas(sec, "| Fondos indexados y ETFs extranjeros |")
    comparar("3. A3", "ETFs extranjeros: texto", nums_str(c[1])[0], a3["texto_etfs_extranjeros"], 0.005)
    comparar("3. A3", "ETFs extranjeros: gráfica", nums_str(c[2])[0], g["Index Funds and ETFs"], 0.005)
    comparar_texto("3. A3", "texto vs gráfica (pp)", r"texto y gráfica no coinciden por (\d+\.\d+) pp", [a3["texto_etfs_extranjeros"] - g["Index Funds and ETFs"]], 0.005, sec)
    if "paginas" in a3:
        comparar_texto("3. A3", "páginas del texto y del Exhibit 8", r"páginas (\d+) y (\d+) y Exhibit 8", [float(p) for p in a3["paginas"]], 0, sec)
    # --- Analisis B
    sec = seccion("### 4. Análisis B")
    P = B["prereg_2015_2024"]
    for pref, w in (("| 0% (IPC", "0"), ("| 10% |", "10"), ("| 20% |", "20"), ("| 30% |", "30"), ("| 50% |", "50"), ("| 100% (S&P", "100")):
        c = celdas(sec, pref)
        comparar("4. B pre-registrado", f"CAGR {w}% S&P", nums_str(c[1])[0], P["mezclas"][w]["cagr_pct"], 0.1)
        if w != "0":
            comparar("4. B pre-registrado", f"ventaja {w}% S&P (pp)", nums_str(c[2])[0], P["mezclas"][w]["ventaja_pp"], 0.1)
    comparar_texto("4. B pre-registrado", "peso para 1/2/3 pp", r"\*\*(\d+\.\d)%\*\* para 1 pp, \*\*(\d+\.\d)%\*\* para 2 pp y \*\*(\d+\.\d)%\*\* para 3 pp",
                   [P["peso_compensa_pct"]["1"], P["peso_compensa_pct"]["2"], P["peso_compensa_pct"]["3"]], 0.1, sec)
    comparar_texto("4. B prueba", "media dif. %/mes", r"media de \*\*(\d+\.\d+)% al mes\*\*", [P["dif_media_pct_mes"]], 0.01, sec)
    comparar_texto("4. B prueba", "t NW(6)", r"t Newey-West\(6\) = \*\*(\d+\.\d+)\*\*", [P["t_nw"]], 0.05, sec)
    comparar_texto("4. B prueba", "IC95 (%/mes)", r"IC 95% = \*\*\[(-?\d+\.\d+), (-?\d+\.\d+)\]\*\*", P["ic95_pct"], 0.01, sec)
    comparar_texto("4. B prueba", "veredicto", r"lo que da \*\*(\w+)\*\*", [P["veredicto"]], 0, sec)
    for pref, clave in (("| 2024 (12 meses) |", "expl_2024"), ("| 2016-2025 (120 meses) |", "expl_2016_2025")):
        E = B[clave]
        c = celdas(sec, pref)
        comparar("4. B exploratorio", f"{clave}: IPC CAGR", nums_str(c[1])[0], E["ipc_cagr_pct"], 0.1)
        comparar("4. B exploratorio", f"{clave}: S&P MXN CAGR", nums_str(c[2])[0], E["sp_mxn_cagr_pct"], 0.1)
        v = nums_str(c[3])
        ws = ["10", "16.4", "20"] if len(v) == 3 else ["10", "20"]
        for s, w in zip(v, ws):
            comparar("4. B exploratorio", f"{clave}: ventaja {w}%", s, E["mezclas"][w]["ventaja_pp"], 0.1)
        comparar("4. B exploratorio", f"{clave}: peso para 2 pp", nums_str(c[4])[0], E["peso_compensa_pct"]["2"], 0.1)
        comparar("4. B exploratorio", f"{clave}: t NW(6)", nums_str(c[5])[0], E["t_nw"], 0.05)
        comparar("4. B exploratorio", f"{clave}: veredicto", c[6].replace("*", "").split(" ")[0], E["veredicto"])
    comparar_texto("4. B lectura", "ventaja fondo promedio 2024 EW/AW (pp)", r"\+(\d+\.\d) pp equiponderado y \+(\d+\.\d) pp ponderado por activos",
                   [r34["Mexico Equity Funds"]["ew"]["1a"] - r34["S&P/BMV IRT"]["ew"]["1a"], r34["Mexico Equity Funds"]["aw"]["1a"] - r34["S&P/BMV IRT"]["aw"]["1a"]], 0.1, sec)
    comparar_texto("4. B lectura", "t 2016-2025", r"queda inconclusa \(t = (\d+\.\d+)\)", [B["expl_2016_2025"]["t_nw"]], 0.05, sec)
    if "una séptima parte de su cartera" in sec:
        comparar("4. B lectura", "'una séptima parte' (100/7 %) vs peso para 2 pp", "%.2f" % (100 / 7), P["peso_compensa_pct"]["2"], 0.5)
    # --- Controles de calidad
    sec = seccion("### Controles de calidad")
    comparar_texto("Controles", "archivos con huella (sin el pre-registro)", r"OK \((\d+) archivos más el pre-registro\)", [float(H_GLOBAL["listados"] - 1)], 0, sec)
    if REEXTRACCION.get("hecha"):
        comparar("Controles", "re-extracción pypdf de los 9 PDF de SPIVA idéntica al .txt", "idénticos", "idénticos" if REEXTRACCION["spiva_identicos"] == 9 else "difieren")
    comparar_texto("Controles", "CAGR IPC/S&P 2015-2024 y 80/20", r"reproduce los CAGR: (\d+\.\d+)% y (\d+\.\d+)% en 2015-2024 \(80/20 → (\d+\.\d+)%\); (−?\d+\.\d+)% y (\d+\.\d+)% en 2024; (\d+\.\d+)% y (\d+\.\d+)% en 2016-2025",
                   [P["ipc_cagr_pct"], P["sp_mxn_cagr_pct"], P["mezclas"]["20"]["cagr_pct"], B["expl_2024"]["ipc_cagr_pct"], B["expl_2024"]["sp_mxn_cagr_pct"],
                    B["expl_2016_2025"]["ipc_cagr_pct"], B["expl_2016_2025"]["sp_mxn_cagr_pct"]], 0.1, sec)
    irt10 = r34["S&P/BMV IRT"]["ew"]["10a"]
    sp10 = r34["S&P 500 (MXN)"]["ew"]["10a"]
    comparar_texto("Controles", "NAFTRAC vs IRT de SPIVA", r"NAFTRAC da (\d+\.\d+)% contra (\d+\.\d+)% del S&P/BMV IRT según SPIVA\. La \*\*brecha de (−?\d+\.\d+) pp",
                   [P["ipc_cagr_pct"], irt10, P["ipc_cagr_pct"] - irt10], 0.1, sec)
    comparar_texto("Controles", "SPY×DEXMXUS vs S&P 500 (MXN) de SPIVA", r"SPY × DEXMXUS da (\d+\.\d+)% contra (\d+\.\d+)% del S&P 500 \(MXN\) de SPIVA \((−?\d+\.\d+) pp",
                   [P["sp_mxn_cagr_pct"], sp10, P["sp_mxn_cagr_pct"] - sp10], 0.1, sec)
    sb = B["sesgo_mezclas"]
    comparar_texto("Controles", "sobrestimación de la ventaja (pp), 20% a 50%", r"sobrestimada en unos (\d+\.\d+)-(\d+\.\d+) pp", [sb["20"], sb["50"]], 0.1, sec)
    # --- Liquidez
    sec = seccion("### 6. SIC: liquidez")
    for tk in TICKERS:
        c = celdas(sec, f"| {tk} |")
        L_ = liq[tk]
        comparar("6. Liquidez SIC", f"{tk}: precio", nums_str(c[3])[0], L_["precio_meta"], 0.005)
        s = nums_str(c[4])
        comparar("6. Liquidez SIC", f"{tk}: sesiones con volumen", s[0], float(L_["con_volumen"]), 0)
        comparar("6. Liquidez SIC", f"{tk}: sesiones", s[1], float(L_["sesiones"]), 0)
        comparar("6. Liquidez SIC", f"{tk}: mediana valor diario MXN", nums_str(c[5])[0], L_["mediana_valor_mxn"], 0.5)
    comparar_texto("6. Liquidez SIC", "CSPX y VUAA como % de 20,000 MXN", r"\*\*un título de CSPX equivale a ~(\d+)% de una cuenta de 20,000 MXN\*\*, y uno de VUAA a ~(\d+)%",
                   [100 * liq["CSPXN.MX"]["precio_meta"] / 20000, 100 * liq["VUAAN.MX"]["precio_meta"] / 20000], 0.5, sec)
    # --- Impuesto sucesorio
    sec = seccion("### 7. Impuesto sucesorio")
    comparar_texto("7. Estate tax", "tipo de cambio", r"TC (\d+\.\d+) MXN/USD del 18-sep-2026", [suc["tc"]], 0.00005, sec)
    comparar("7. Estate tax", "fecha del TC", "2026-09-18", suc["fecha_tc"])
    for pref, clave in (("| 1,160 USD", "%.0f" % (20000 / suc["tc"])), ("| 60,000 USD |", "60000"), ("| 100,000 USD |", "100000"),
                        ("| 250,000 USD |", "250000"), ("| 500,000 USD |", "500000"), ("| 1,000,000 USD |", "1000000")):
        c = celdas(sec, pref)
        f_ = suc["filas"][clave]
        comparar("7. Estate tax", f"{clave} USD: USD", nums_str(c[0])[0], f_["usd"], 0.5)
        comparar("7. Estate tax", f"{clave} USD: MXN", nums_str(c[1])[0], f_["mxn"], 0.5)
        comparar("7. Estate tax", f"{clave} USD: impuesto", nums_str(c[2])[0], f_["impuesto_usd"], 0)
        comparar("7. Estate tax", f"{clave} USD: tasa efectiva", nums_str(c[3])[0], f_["tasa_efectiva_pct"], 0.05)
    # --- Fiscalidad (tabla 5): estado documental
    sec = seccion("### 5. Fiscalidad")
    ok = {x["id"]: x["ok"] for x in cit}
    mapa = [
        ("| ISR sobre la ganancia en BMV y SIC", ["L01", "L02", "L03", "L07"], "**Verificado**"),
        ("| Pérdidas |", ["L04", "L05", "L06"], "**Verificado**"),
        ("| Constancia |", ["L08", "L10"], "**Verificado**"),
        ("| Retención de ISR sobre intereses en 2026 |", ["L11", "L12", "L13"], "**Verificado**"),
        ("| Dividendos de emisoras mexicanas |", ["L14"], "**Verificado**"),
        ("| Dividendos extranjeros (SIC) |", ["L15", "L17", "L18", "L19"], "**Verificado**"),
        ("| Reformas 2026 |", ["L20"], "**Verificado**"),
        ("| *Estate tax* EUA: umbral y crédito |", ["L21", "L22", "L23"], "**Verificado**"),
        ("| Tratado sucesorio México-EUA |", ["L24", "L24b"], "**Verificado**"),
        ("| *Situs* de acciones y ETFs de EUA vía SIC/Indeval |", ["L25", "L26"], "Regla **verificada**"),
        ("| Dividendos dentro del UCITS irlandés |", ["L27", "L19"], "Tasas **verificadas**"),
        ("| Impuesto sucesorio irlandés (CAT) sobre UCITS |", ["L28"], "**Verificado**"),
        ("| ISR mexicano sobre ganancias en UCITS del SIC |", ["L02", "L03", "L29"], "**Inferencia**"),
    ]
    for pref, ids, estado in mapa:
        c = celdas(sec, pref)
        propio = estado if all(ok[i] for i in ids) else "NO VERIFICADO: " + ",".join(i for i in ids if not ok[i])
        comparar("5. Fiscalidad", pref.strip("| ").strip() + " (" + ",".join(ids) + ")", estado if c[2].startswith(estado) else c[2][:40], propio)
    c = celdas(sec, "| Dividendos extranjeros (SIC) |")
    base_readme = "ambigua" if "ambigua" in c[2] else ("neta" if "neto" in c[2] or "neta" in c[2] else "(no dice)")
    comparar("5. Fiscalidad", "Base del 10% adicional de dividendos extranjeros (L16)", base_readme, "neta" if ok["L16"] else "no verificada",
             nota="art. 142 fr. V: 'sin incluir el monto del impuesto retenido que en su caso se hubiere efectuado'")
    c = celdas(sec, "| UCITS irlandeses en el SIC |")
    ucits = [tk for tk in TICKERS if "UCITS" in (liq[tk]["nombre"] or "") and liq[tk]["moneda"] == "MXN" and liq[tk]["bolsa"] == "MEX"]
    comparar("5. Fiscalidad", "UCITS que cotizan en MXN en MEX (Yahoo)", "8", float(len(ucits)), 0)
    # --- Resumen y conclusiones (texto)
    sec = seccion("## Resumen", "## ")
    comparar_texto("Resumen", "85.59 / 83.33", r"La cifra exacta es \*\*(\d+\.\d+)%\*\*.*?da \*\*(\d+\.\d+)%\*\*", [eua["Year-End 2025"]["10a"], eua["Mid-Year 2026"]["10a"]], 0.005, sec)
    comparar_texto("Resumen", "82.93 / 73.17 / supervivencia 82.93 (34 de 41)", r"La cifra es \*\*(\d+\.\d+)%\*\*.*?da \*\*(\d+\.\d+)%\*\*.*?\*\*(\d+\.\d+)% es la tasa de supervivencia\*\* a 10 años \((\d+) de (\d+) fondos\)",
                   [la["Year-End 2024"]["mx"]["10a"], la["Primer semestre 2025"]["mx"]["10a"], la["Primer semestre 2025"]["superv10"]["pct"],
                    float(la["Primer semestre 2025"]["superv10"]["sobrevivientes"]), float(la["Primer semestre 2025"]["superv10"]["fondos_iniciales"])], 0.005, sec)
    comparar_texto("Resumen", "74.3 / 16.4 / 16.2", r"\*\*(\d+\.\d)%\*\* en valores fuera del S&P/BMV IRT y \*\*(\d+\.\d)%\*\* en fondos indexados.*?la gráfica dice (\d+\.\d)%",
                   [a3["texto_fuera_indice"], a3["texto_etfs_extranjeros"], g["Index Funds and ETFs"]], 0.005, sec)
    comparar_texto("Resumen", "IPC 3.53 / S&P 16.98 / 10% → 1.45 / 13.8 / +8.7", r"rindió \*\*(\d+\.\d+)%\*\* anual y el S&P 500 en pesos \*\*(\d+\.\d+)%\*\*.*?por \*\*(\d+\.\d+) pp\*\*.*?bastaba con \*\*(\d+\.\d)%\*\*.*?daba \*\*\+(\d+\.\d) pp\*\*",
                   [P["ipc_cagr_pct"], P["sp_mxn_cagr_pct"], P["mezclas"]["10"]["ventaja_pp"], P["peso_compensa_pct"]["2"], B["expl_2024"]["mezclas"]["16.4"]["ventaja_pp"]], 0.1, sec)
    comparar_texto("Resumen", "86.67 / 100 / 12.65 vs 17.08 / 7.09 vs 14.33", r"\*\*(\d+\.\d+)%\*\* de los fondos mexicanos de acciones de EUA.*?\*\*(\d+)%\*\* de los fondos globales.*?rindieron \*\*(\d+\.\d+)%\*\* contra \*\*(\d+\.\d+)%\*\*.*?globales \*\*(\d+\.\d+)%\*\* contra \*\*(\d+\.\d+)%\*\*",
                   [la["Year-End 2024"]["eua_mxn"]["10a"], la["Year-End 2024"]["global_mxn"]["10a"], r34["U.S. Equity (MXN) Funds"]["ew"]["10a"], sp10,
                    r34["Global Equity (MXN) Funds"]["ew"]["10a"], r34["S&P World Index (MXN)"]["ew"]["10a"]], 0.005, sec)
    comparar_texto("Resumen", "retención intereses 2026", r"La retención sobre intereses en 2026 es \*\*(\d+\.\d+)%\*\*", [0.90 if ok["L11"] else float("nan")], 0.0, sec)
    comparar_texto("Resumen", "umbral / crédito / tasa máx.", r"arriba de \*\*(\d+,\d+) USD\*\* de umbral \(crédito de \*\*(\d+,\d+) USD\*\*\), con tasa marginal de hasta \*\*(\d+)%\*\*",
                   [60000.0 if ok["L21"] else float("nan"), suc["credito"], suc["tarifa_max_pct"]], 0, sec)
    comparar_texto("Resumen", "lista de tratados", r"lista de (\d+) países", [15.0 if ok["L24b"] else float("nan")], 0, sec)
    comparar_texto("Resumen", "CSPX sesiones y mediana (millones)", r"se negocia en (\d+) de (\d+) sesiones, con mediana de \*\*(\d+) millones de MXN\*\*",
                   [float(liq["CSPXN.MX"]["con_volumen"]), float(liq["CSPXN.MX"]["sesiones"]), liq["CSPXN.MX"]["mediana_valor_mxn"] / 1e6], 0.5, sec)
    comparar_texto("Resumen", "VUAA sesiones, mediana, precios", r"se negocia en (\d+) de (\d+) sesiones, con mediana de \*\*(\d+\.\d) millones de MXN\*\* y precio de ~(\d,\d+) MXN, contra ~(\d+,\d+) MXN de CSPX",
                   [float(liq["VUAAN.MX"]["con_volumen"]), float(liq["VUAAN.MX"]["sesiones"]), liq["VUAAN.MX"]["mediana_valor_mxn"] / 1e6, liq["VUAAN.MX"]["precio_meta"], liq["CSPXN.MX"]["precio_meta"]], 50, sec)
    comparar_texto("Resumen", "IUSA sesiones", r"casi no se negocia \((\d+) de (\d+) sesiones\)", [float(liq["IUSAN.MX"]["con_volumen"]), float(liq["IUSAN.MX"]["sesiones"])], 0, sec)
    comparar_texto("Resumen", "rendimiento por dividendo S&P", r"rendimiento por dividendo del S&P de \*\*(\d+\.\d+)%\*\*", [div["rend_div_pct"]], 0.005, sec)
    comparar_texto("Resumen", "fuga 15/10/30", r"esa fuga es de \*\*(\d+\.\d+) pp\*\* al año, contra (\d+\.\d+) pp y (\d+\.\d+) pp", [div["fuga_pp"]["15"], div["fuga_pp"]["10"], div["fuga_pp"]["30"]], 0.005, sec)
    sec = seccion("## Conclusiones permitidas", "## ")
    rango_mx = [la[e]["mx"]["10a"] for e in la]
    comparar_texto("Conclusiones", "rango EUA 10 años", r"\*\*de (\d+)% a (\d+)%\*\* de los fondos \*large-cap\*", [min(rango10), max(rango10)], 0.5, sec)
    comparar_texto("Conclusiones", "rango México 10 años", r"\*\*de (\d+)% a (\d+)%\*\* de los fondos activos quedaron debajo del S&P/BMV IRT", [min(rango_mx), max(rango_mx)], 0.5, sec)
    comparar_texto("Conclusiones", "fondos que invierten afuera: % y pp", r"en \*\*(\d+)% a (\d+)%\*\* de los casos a 10 años, y en promedio por \*\*(\d+\.\d) a (\d+\.\d) pp al año\*\*",
                   [la["Year-End 2024"]["eua_mxn"]["10a"], la["Year-End 2024"]["global_mxn"]["10a"], sp10 - r34["U.S. Equity (MXN) Funds"]["ew"]["10a"],
                    r34["S&P World Index (MXN)"]["ew"]["10a"] - r34["Global Equity (MXN) Funds"]["ew"]["10a"]], 0.5, sec)
    comparar_texto("Conclusiones", "umbral en MXN y tasas efectivas", r"más de ~(\d+\.\d+) millones de MXN.*?\((\d+\.\d)% efectivo con 100,000 USD y (\d+)% con 1 MUSD\)",
                   [suc["filas"]["60000"]["mxn"] / 1e6, suc["filas"]["100000"]["tasa_efectiva_pct"], suc["filas"]["1000000"]["tasa_efectiva_pct"]], 0.5, sec)
    sec = seccion("## Conclusiones que NO se sostienen", "## ")
    comparar_texto("Conclusiones NO", "t 2015-2024", r"es marginal \(t = (\d+\.\d+)\)", [P["t_nw"]], 0.05, sec)


# ---------------------------------------------------------------------------
def main():
    H = huellas()
    H_GLOBAL.update(H)
    print(f"Huellas: {H['listados']} listadas, {len(H['malos'])} con problema, no listadas en datos/: {H['no_listados']}")
    if H["malos"]:
        raise SystemExit(f"Huellas con problema: {H['malos']}")
    REEXTRACCION.update(reextraccion_pypdf())
    if REEXTRACCION["hecha"]:
        print(f"Re-extraccion pypdf {REEXTRACCION['version_pypdf']}: SPIVA {REEXTRACCION['spiva_identicos']}/9 y legales {REEXTRACCION['legales_identicos']}/4 identicos al .txt congelado")
    if not HAY_PDFMINER:
        print("AVISO: pdfminer no esta instalado; se omite la ruta (b) de coordenadas.")
    S = spiva()
    if S["discrepancias_rutas"]:
        raise SystemExit(f"Las rutas (a) y (b) no coinciden: {S['discrepancias_rutas']}")
    print("SPIVA: rutas (a) texto y (b) coordenadas coinciden en todas las filas." if HAY_PDFMINER else "SPIVA: solo ruta (a).")
    B, naf, spy, fx = analisis_b()
    # sesgo de las mezclas por la brecha de NAFTRAC (IRT de SPIVA) y de SPY: ajuste aditivo mensual hasta igualar el CAGR de SPIVA
    r34 = S["latam"]["Year-End 2024"]["reports_3_4"]
    ks = meses((2015, 1), (2024, 12))
    ri = [naf[k] / naf[previo(k)] - 1 for k in ks]
    rs = [spy[k] * fx[k][1] / (spy[previo(k)] * fx[previo(k)][1]) - 1 for k in ks]

    def ajusta(r, obj):
        lo, hi = -0.01, 0.01
        for _ in range(100):
            c = (lo + hi) / 2
            lo, hi = (c, hi) if cagr([x + c for x in r]) < obj else (lo, c)
        return [x + (lo + hi) / 2 for x in r]
    ri2 = ajusta(ri, r34["S&P/BMV IRT"]["ew"]["10a"] / 100)
    rs2 = ajusta(rs, r34["S&P 500 (MXN)"]["ew"]["10a"] / 100)
    sesgo = {}
    for w in (0.10, 0.20, 0.30, 0.50):
        v1 = cagr([(1 - w) * a + w * b for a, b in zip(ri, rs)]) - cagr(ri)
        v2 = cagr([(1 - w) * a + w * b for a, b in zip(ri2, rs2)]) - cagr(ri2)
        v3 = cagr([(1 - w) * a + w * b for a, b in zip(ri2, rs)]) - cagr(ri2)
        sesgo["%g" % (100 * w)] = 100 * (v1 - v3)
        sesgo["%g_ambos" % (100 * w)] = 100 * (v1 - v2)
    B["sesgo_mezclas"] = sesgo
    liq = liquidez()
    div = dividendo_spy()
    suc = impuesto_sucesorio(fx)
    cit = citas()
    faltan = [c for c in cit if not c["ok"]]
    print(f"Citas legales: {len(cit)} reglas, {len(cit) - len(faltan)} encontradas literalmente; faltan: {[(c['id'], c['faltan']) for c in faltan]}")
    comparar_readme(S, B, liq, div, suc, cit)
    n = len(COMP)
    dentro = sum(1 for c in COMP if c["dentro"])
    ident = sum(1 for c in COMP if c["identica"])
    print(f"Comparacion con el README: {n} cifras, {dentro} dentro de tolerancia, {ident} identicas al redondeo impreso.")
    for c in COMP:
        if not c["dentro"]:
            print("  FUERA:", c["bloque"], "|", c["concepto"], "| README:", c["readme"], "| propio:", c["propio"], "|", c.get("nota", ""))
    with open(os.path.join(BASE, "independiente-comparacion.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["bloque", "concepto", "readme", "propio", "diferencia", "tolerancia", "tipo", "dentro", "identica", "nota"])
        w.writeheader()
        for c in COMP:
            w.writerow({k: c.get(k, "") for k in w.fieldnames})
    extra_h = {f: hashlib.sha256(open(os.path.join(EXTRA, f), "rb").read()).hexdigest() for f in sorted(os.listdir(EXTRA))}
    res = {"fecha": "2026-09-25", "autor": "auditor-de-replicas (doble ejecucion independiente)", "huellas": H, "reextraccion_pypdf": REEXTRACCION,
           "huellas_independiente_datos": extra_h, "spiva": S, "analisis_b": B, "liquidez": liq, "dividendo_spy": div,
           "impuesto_sucesorio": suc, "citas_legales": cit,
           "comparacion": {"cifras": n, "dentro": dentro, "identicas": ident, "fuera": [c for c in COMP if not c["dentro"]]}}
    with open(os.path.join(BASE, "independiente-resultados.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1, default=str)
    # resumen por bloque (markdown)
    bloques = {}
    for c in COMP:
        b = bloques.setdefault(c["bloque"], [0, 0, 0])
        b[0] += 1
        b[1] += c["dentro"]
        b[2] += c["identica"]
    print("\n| Bloque | Cifras | Dentro de tolerancia | Idénticas al redondeo |\n|---|---|---|---|")
    for k, (a, b_, c_) in bloques.items():
        print(f"| {k} | {a} | {b_} | {c_} |")
    print(f"| **Total** | **{n}** | **{dentro}** | **{ident}** |")
    P = B["prereg_2015_2024"]
    print(f"\nB 2015-2024: media {P['dif_media_pct_mes']:.4f} %/mes, t NW {P['t_nw']:.4f} (sin n/(n-1): {P['t_nw_sin_correccion']:.4f}; IID {P['t_iid']:.4f}), "
          f"IC [{P['ic95_pct'][0]:.4f}, {P['ic95_pct'][1]:.4f}], {P['veredicto']}; EE formula2-formula1 {P['se_formula2_menos_formula1']:.2e}, "
          f"herramientas-formula1 {P['se_herramientas_menos_formula1']}")
    return 0 if dentro == n and not faltan else 1


if __name__ == "__main__":
    sys.exit(main())
