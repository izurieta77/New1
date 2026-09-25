"""AC-04: segunda ejecucion independiente del efecto Halloween (R04).

Escrito desde cero; no importa ni copia laboratorio/replicas/R04.py.
Solo biblioteca estandar de Python 3.11. De herramientas/datos.py solo se usan
`descargar`, `parsear_yahoo_json` y `parsear_fred_csv` (transporte y parseo).

Fuentes:
  - Shiller ie_data.xls (Yale): S&P Composite, precio promedio mensual + dividendo/12.
  - Yahoo ^SP500TR, ^MXX, EWW (diarios -> ultimo cierre del mes).
  - FRED TB3MS, INTGSTMXM193N.

Uso: python3 laboratorio/auditorias/AC-04-halloween/AC04.py [--sin-red]
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import struct
import sys
import urllib.parse
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))
from herramientas.datos import descargar, parsear_fred_csv, parsear_yahoo_json  # noqa: E402

AQUI = Path(__file__).resolve().parent
DIR_DATOS = AQUI / "datos"
SIN_RED = "--sin-red" in sys.argv

URL_SHILLER = "http://www.econ.yale.edu/~shiller/data/ie_data.xls"
URL_YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/"
URL_FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="

COSTO_LADO = 0.0029 + 0.0005
FIN = (2026, 7)
SALIDA: list[str] = []


def p(*a):
    linea = " ".join(str(x) for x in a)
    print(linea)
    SALIDA.append(linea)


# ------------------------------------------------------------------ descarga con copia local

def obtener_bytes(url: str, nombre: str) -> bytes:
    ruta = DIR_DATOS / nombre
    if SIN_RED and ruta.exists():
        return ruta.read_bytes()
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        datos = r.read()
    DIR_DATOS.mkdir(parents=True, exist_ok=True)
    ruta.write_bytes(datos)
    return datos


def obtener_texto(url: str, nombre: str, ua_navegador: bool) -> str:
    ruta = DIR_DATOS / nombre
    if SIN_RED and ruta.exists():
        return ruta.read_text(encoding="utf-8")
    texto = descargar(url, {"User-Agent": "Mozilla/5.0"} if ua_navegador else None)
    DIR_DATOS.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")
    return texto


def huella(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


# ------------------------------------------------------------------ lector OLE2 + BIFF8 minimo

def ole2_flujo(datos: bytes, nombre_flujo: str) -> bytes:
    if datos[:8] != bytes.fromhex("D0CF11E0A1B11AE1"):
        raise ValueError("no es un archivo OLE2")
    tam_sector = 1 << struct.unpack_from("<H", datos, 0x1E)[0]
    tam_mini = 1 << struct.unpack_from("<H", datos, 0x20)[0]
    n_fat = struct.unpack_from("<I", datos, 0x2C)[0]
    dir_ini = struct.unpack_from("<I", datos, 0x30)[0]
    corte_mini = struct.unpack_from("<I", datos, 0x38)[0]
    minifat_ini = struct.unpack_from("<I", datos, 0x3C)[0]
    difat_ini = struct.unpack_from("<I", datos, 0x44)[0]
    n_difat = struct.unpack_from("<I", datos, 0x48)[0]

    def sector(i):
        o = 512 + i * tam_sector
        return datos[o:o + tam_sector]

    difat = list(struct.unpack_from("<109I", datos, 0x4C))
    s = difat_ini
    for _ in range(n_difat):
        bloque = sector(s)
        vals = struct.unpack("<%dI" % (tam_sector // 4), bloque)
        difat.extend(vals[:-1])
        s = vals[-1]
    difat = [x for x in difat if x < 0xFFFFFFFA][:n_fat]
    fat: list[int] = []
    for s in difat:
        fat.extend(struct.unpack("<%dI" % (tam_sector // 4), sector(s)))

    def cadena(ini):
        out, s, vistos = [], ini, 0
        while s < 0xFFFFFFFA:
            out.append(s)
            s = fat[s]
            vistos += 1
            if vistos > len(fat):
                raise ValueError("cadena FAT ciclica")
        return out

    directorio = b"".join(sector(s) for s in cadena(dir_ini))
    entradas = []
    for k in range(len(directorio) // 128):
        e = directorio[k * 128:(k + 1) * 128]
        ln = struct.unpack_from("<H", e, 0x40)[0]
        nombre = e[:max(ln - 2, 0)].decode("utf-16-le", "replace")
        tipo = e[0x42]
        ini = struct.unpack_from("<I", e, 0x74)[0]
        tam = struct.unpack_from("<I", e, 0x78)[0]
        entradas.append((nombre, tipo, ini, tam))
    raiz = entradas[0]
    for nombre, tipo, ini, tam in entradas:
        if nombre == nombre_flujo:
            if tam >= corte_mini:
                return b"".join(sector(s) for s in cadena(ini))[:tam]
            mini_flujo = b"".join(sector(s) for s in cadena(raiz[2]))
            minifat = []
            for s in cadena(minifat_ini):
                minifat.extend(struct.unpack("<%dI" % (tam_sector // 4), sector(s)))
            out, s = [], ini
            while s < 0xFFFFFFFA:
                out.append(mini_flujo[s * tam_mini:(s + 1) * tam_mini])
                s = minifat[s]
            return b"".join(out)[:tam]
    raise ValueError(f"flujo {nombre_flujo} no encontrado")


def rk_a_float(rk: int) -> float:
    if rk & 2:
        v = float(struct.unpack("<i", struct.pack("<I", rk & 0xFFFFFFFC))[0] >> 2)
    else:
        v = struct.unpack("<d", struct.pack("<Q", (rk & 0xFFFFFFFC) << 32))[0]
    return v / 100 if rk & 1 else v


def biff_hojas(libro: bytes) -> dict[str, int]:
    """nombre de hoja -> offset del BOF en el flujo Workbook."""
    hojas, o = {}, 0
    while o + 4 <= len(libro):
        tipo, ln = struct.unpack_from("<HH", libro, o)
        cuerpo = libro[o + 4:o + 4 + ln]
        if tipo == 0x0085:
            pos = struct.unpack_from("<I", cuerpo, 0)[0]
            n = cuerpo[6]
            flags = cuerpo[7]
            if flags & 1:
                nombre = cuerpo[8:8 + 2 * n].decode("utf-16-le")
            else:
                nombre = cuerpo[8:8 + n].decode("latin-1")
            hojas[nombre] = pos
        if tipo == 0x000A and hojas:  # EOF del globals
            break
        o += 4 + ln
    return hojas


def biff_numeros(libro: bytes, pos: int) -> dict[tuple[int, int], float]:
    """Celdas numericas (NUMBER, RK, MULRK, FORMULA numerica) de una hoja."""
    celdas, o = {}, pos
    while o + 4 <= len(libro):
        tipo, ln = struct.unpack_from("<HH", libro, o)
        c = libro[o + 4:o + 4 + ln]
        if tipo == 0x0203:
            r, col = struct.unpack_from("<HH", c, 0)
            celdas[(r, col)] = struct.unpack_from("<d", c, 6)[0]
        elif tipo == 0x027E:
            r, col = struct.unpack_from("<HH", c, 0)
            celdas[(r, col)] = rk_a_float(struct.unpack_from("<I", c, 6)[0])
        elif tipo == 0x00BD:
            r, c0 = struct.unpack_from("<HH", c, 0)
            n = (ln - 6) // 6
            for k in range(n):
                celdas[(r, c0 + k)] = rk_a_float(struct.unpack_from("<I", c, 4 + 6 * k + 2)[0])
        elif tipo == 0x0006:
            r, col = struct.unpack_from("<HH", c, 0)
            res = c[6:14]
            if res[6:8] != b"\xff\xff":
                celdas[(r, col)] = struct.unpack("<d", res)[0]
        elif tipo == 0x000A:
            break
        o += 4 + ln
    return celdas


def shiller_mensual():
    datos = obtener_bytes(URL_SHILLER, "ie_data.xls")
    libro = ole2_flujo(datos, "Workbook")
    hojas = biff_hojas(libro)
    celdas = biff_numeros(libro, hojas["Data"])
    filas = sorted({r for r, _ in celdas})
    serie = {}
    for r in filas:
        f = celdas.get((r, 0))
        if f is None or not (1800 < f < 2100):
            continue
        anio = int(f)
        mes = int(round((f - anio) * 100))
        if not 1 <= mes <= 12:
            continue
        precio, div = celdas.get((r, 1)), celdas.get((r, 2))
        serie[(anio, mes)] = (precio, div)
    return serie, huella(datos), sorted(hojas)


# ------------------------------------------------------------------ Yahoo / FRED

def yahoo_fin_de_mes(ticker: str):
    url = URL_YAHOO + urllib.parse.quote(ticker, safe="") + "?" + urllib.parse.urlencode(
        {"period1": -1400000000, "period2": 1790000000, "interval": "1d"})
    nombre = "yahoo_" + ticker.replace("^", "") + "_1d.json"
    texto = obtener_texto(url, nombre, True)
    g = parsear_yahoo_json(texto, "1d")
    ult = {}
    for f, v in g["serie"]:
        ult[(f.year, f.month)] = (f, v)  # la serie viene ordenada: queda el ultimo dia
    hoy = date.today()
    ult.pop((hoy.year, hoy.month), None)  # mes en curso
    return {k: v[1] for k, v in ult.items()}, g["serie"][0][0], g["serie"][-1][0], huella(texto.encode())


def fred_mensual(idf: str):
    texto = obtener_texto(URL_FRED + idf, "fred_" + idf + ".csv", False)
    return {(f.year, f.month): v for f, v in parsear_fred_csv(texto)}, huella(texto.encode())


URL_FRENCH = ("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
              "F-F_Research_Data_Factors_CSV.zip")


def french_mercado():
    """Mkt-RF + RF mensual de French (diagnostico: misma fuente que A)."""
    import io
    import zipfile
    datos = obtener_bytes(URL_FRENCH, "F-F_Research_Data_Factors_CSV.zip")
    with zipfile.ZipFile(io.BytesIO(datos)) as z:
        texto = z.read(z.namelist()[0]).decode("latin-1")
    out = {}
    for linea in texto.splitlines():
        partes = [x.strip() for x in linea.split(",")]
        if len(partes) >= 5 and len(partes[0]) == 6 and partes[0].isdigit():
            m = (int(partes[0][:4]), int(partes[0][4:]))
            out[m] = (float(partes[1]) + float(partes[4])) / 100
        elif out and partes[0] == "":
            continue
        elif out and not partes[0].isdigit():
            break  # termina el bloque mensual (sigue el anual)
    return out, huella(datos)


# ------------------------------------------------------------------ utilidades de meses

def sig(m):
    return (m[0] + (m[1] == 12), m[1] % 12 + 1)


def ant(m):
    return (m[0] - (m[1] == 1), 12 if m[1] == 1 else m[1] - 1)


def rango(a, b):
    out, m = [], a
    while m <= b:
        out.append(m)
        m = sig(m)
    return out


def rend_de_niveles(niveles: dict):
    """R_t = N_t/N_{t-1} - 1 solo si ambos meses existen."""
    return {m: niveles[m] / niveles[ant(m)] - 1 for m in niveles if ant(m) in niveles}


def invierno(m):
    return m[1] in (11, 12, 1, 2, 3, 4)


def ftxt(m):
    return f"{m[0]}-{m[1]:02d}"


# ------------------------------------------------------------------ estadistica

def regresion_halloween(rend: dict, a, b):
    meses = [m for m in rango(a, b) if m in rend]
    faltan = len(rango(a, b)) - len(meses)
    y = [100 * math.log(1 + rend[m]) for m in meses]
    s = [1.0 if invierno(m) else 0.0 for m in meses]
    n = len(y)
    y1 = [v for v, d in zip(y, s) if d]
    y0 = [v for v, d in zip(y, s) if not d]
    mu = sum(y0) / len(y0)
    alfa = sum(y1) / len(y1) - mu
    resid = [v - mu - alfa * d for v, d in zip(y, s)]
    k = 2
    sigma2 = sum(e * e for e in resid) / (n - k)
    sbar = sum(s) / n
    sxx = sum((d - sbar) ** 2 for d in s)
    se_mco = math.sqrt(sigma2 / sxx)
    # Newey-West: (X'X)^-1 S (X'X)^-1 con X = [1, s]
    xtx = [[n, sum(s)], [sum(s), sum(d * d for d in s)]]
    det = xtx[0][0] * xtx[1][1] - xtx[0][1] * xtx[1][0]
    inv = [[xtx[1][1] / det, -xtx[0][1] / det], [-xtx[1][0] / det, xtx[0][0] / det]]
    g = [(e, e * d) for e, d in zip(resid, s)]
    L = 12
    S = [[0.0, 0.0], [0.0, 0.0]]
    for j in range(L + 1):
        w = 1.0 if j == 0 else 1 - j / (L + 1)
        G = [[0.0, 0.0], [0.0, 0.0]]
        for t in range(j, n):
            for i1 in range(2):
                for i2 in range(2):
                    G[i1][i2] += g[t][i1] * g[t - j][i2]
        for i1 in range(2):
            for i2 in range(2):
                S[i1][i2] += w * (G[i1][i2] + (G[i2][i1] if j > 0 else 0.0))
    V = [[sum(inv[a1][c] * S[c][d] * inv[d][b1] for c in range(2) for d in range(2))
          for b1 in range(2)] for a1 in range(2)]
    se_nw = math.sqrt(V[1][1] * n / (n - k))
    return {"ini": ftxt(meses[0]), "fin": ftxt(meses[-1]), "n": n, "faltan": faltan,
            "mu": mu, "alfa": alfa, "t_mco": alfa / se_mco, "t_nw": alfa / se_nw}


def diferencia_anual(rend: dict, a, b, semilla=4, reps=10000):
    ds = []
    for anio in range(a[0], b[0] + 1):
        inv_m = [(anio - 1, 11), (anio - 1, 12)] + [(anio, k) for k in range(1, 5)]
        ver_m = [(anio, k) for k in range(5, 11)]
        todos = inv_m + ver_m
        if any(m < a or m > b or m not in rend for m in todos):
            continue
        ds.append(sum(100 * math.log(1 + rend[m]) for m in inv_m)
                  - sum(100 * math.log(1 + rend[m]) for m in ver_m))
    n = len(ds)
    media = sum(ds) / n
    sd = math.sqrt(sum((d - media) ** 2 for d in ds) / (n - 1))
    rng = random.Random(semilla)
    medias = sorted(sum(rng.choice(ds) for _ in range(n)) / n for _ in range(reps))
    return {"n_anios": n, "media": media, "t": media / (sd / math.sqrt(n)),
            "ic95": (medias[int(0.025 * reps)], medias[int(0.975 * reps) - 1]),
            "positivos": sum(d > 0 for d in ds)}


# ------------------------------------------------------------------ estrategia

def estrategia(rend: dict, rf: dict, a, b, regla):
    meses = rango(a, b)
    faltan = [m for m in meses if m not in rend or m not in rf]
    if faltan:
        raise ValueError(f"faltan meses: {faltan[:5]}")
    w_prev, riqueza, pico, mdd = 0.0, 1.0, 1.0, 0.0
    netos, exc, ops = [], [], 0
    for m in meses:
        w = regla(m)
        costo = COSTO_LADO * abs(w - w_prev)
        if w != w_prev:
            ops += 1
        r = w * rend[m] + (1 - w) * rf[m] - costo
        netos.append(r)
        exc.append(r - rf[m])
        riqueza *= 1 + r
        pico = max(pico, riqueza)
        mdd = min(mdd, riqueza / pico - 1)
        w_prev = w
    n = len(netos)
    cagr = riqueza ** (12 / n) - 1
    mr = sum(netos) / n
    vol = math.sqrt(sum((x - mr) ** 2 for x in netos) / (n - 1)) * math.sqrt(12)
    me = sum(exc) / n
    sde = math.sqrt(sum((x - me) ** 2 for x in exc) / (n - 1))
    sharpe = me / sde * math.sqrt(12) if sde > 0 else float("nan")
    return {"n": n, "cagr": cagr, "vol": vol, "sharpe": sharpe, "mdd": mdd, "ops": ops}


# ------------------------------------------------------------------ principal

def imprimir_reg(etiqueta, r):
    p(f"  {etiqueta:<34} {r['ini']}..{r['fin']} n={r['n']:>4} (faltan {r['faltan']})  "
      f"mu={r['mu']:+.4f}  alfa1={r['alfa']:+.4f}  t_MCO={r['t_mco']:+.2f}  t_NW12={r['t_nw']:+.2f}")


def imprimir_dy(etiqueta, d):
    p(f"  {etiqueta:<34} D_y: anios={d['n_anios']} media={d['media']:+.2f} t={d['t']:+.2f} "
      f"IC95=[{d['ic95'][0]:+.2f}, {d['ic95'][1]:+.2f}] positivos={d['positivos']}/{d['n_anios']}")


def imprimir_est(etiqueta, e):
    p(f"  {etiqueta:<34} n={e['n']} CAGR={100*e['cagr']:6.2f}%  vol={100*e['vol']:5.2f}%  "
      f"Sharpe={e['sharpe']:+.3f}  MDD={100*e['mdd']:7.2f}%  operaciones={e['ops']}")


def main():
    p("AC-04 efecto Halloween: ejecucion B independiente. Consulta:", date.today().isoformat())
    res = {}

    # ---- datos
    sh, h_sh, hojas = shiller_mensual()
    sh_ok = {m: v for m, v in sh.items() if v[0] and v[1]}
    ult_div = max(sh_ok)
    p(f"Shiller ie_data.xls sha256[:16]={h_sh} hojas={hojas} meses={len(sh)} "
      f"primero={ftxt(min(sh))} ultimo_con_P={ftxt(max(m for m, v in sh.items() if v[0]))} "
      f"ultimo_con_D={ftxt(ult_div)}")
    r_sh = {}
    for m, (pr, dv) in sh_ok.items():
        a = ant(m)
        if a in sh_ok:
            r_sh[m] = (pr + dv / 12) / sh_ok[a][0] - 1
    r_sh_precio = {m: sh_ok[m][0] / sh_ok[ant(m)][0] - 1 for m in sh_ok if ant(m) in sh_ok}

    series = {}
    for t in ["^SP500TR", "^GSPC", "^MXX", "EWW"]:
        niv, f0, f1, h = yahoo_fin_de_mes(t)
        series[t] = rend_de_niveles(niv)
        p(f"Yahoo {t}: diario {f0}..{f1} sha256[:16]={h} meses_con_nivel={len(niv)} "
          f"primer_rend={ftxt(min(series[t]))} ultimo_rend={ftxt(max(series[t]))}")
    niv_gspc, _, _, _ = yahoo_fin_de_mes("^GSPC")
    r_hib = {}
    for m, pf in niv_gspc.items():
        a = ant(m)
        if a in niv_gspc and m in sh_ok:
            r_hib[m] = (pf + sh_ok[m][1] / 12) / niv_gspc[a] - 1
    r_fr, h_fr = french_mercado()
    p(f"Hibrido ^GSPC fin de mes + D Shiller/12: {ftxt(min(r_hib))}..{ftxt(max(r_hib))}; "
      f"French Mkt-RF+RF {ftxt(min(r_fr))}..{ftxt(max(r_fr))} sha256[:16]={h_fr}")
    tb, h_tb = fred_mensual("TB3MS")
    ce, h_ce = fred_mensual("INTGSTMXM193N")
    p(f"FRED TB3MS {ftxt(min(tb))}..{ftxt(max(tb))} sha256[:16]={h_tb}; "
      f"INTGSTMXM193N {ftxt(min(ce))}..{ftxt(max(ce))} sha256[:16]={h_ce}")
    rf_us = {m: v / 1200 for m, v in tb.items()}
    rf_mx = {m: v / 1200 for m, v in ce.items()}

    # ---- regresiones
    p("\n1. Regresion y_t = mu + alfa1*S_t (y = 100 ln(1+R), % mensual)")
    p(" EUA")
    casos = [
        ("US_Shiller_1970-01_1998-08", r_sh, (1970, 1), (1998, 8)),
        ("US_Shiller_1926-07_2002-12", r_sh, (1926, 7), (2002, 12)),
        ("US_Shiller_1926-07_1969-12", r_sh, (1926, 7), (1969, 12)),
        ("US_Shiller_1973-01_1996-12", r_sh, (1973, 1), (1996, 12)),
        ("US_Shiller_2003-01_finD", r_sh, (2003, 1), ult_div),
        ("US_ShillerPrecio_1970-01_1998-08", r_sh_precio, (1970, 1), (1998, 8)),
        ("DIAG_Hibrido_1970-01_1998-08", r_hib, (1970, 1), (1998, 8)),
        ("DIAG_Hibrido_1928-01_2002-12", r_hib, (1928, 1), (2002, 12)),
        ("DIAG_French_1970-01_1998-08", r_fr, (1970, 1), (1998, 8)),
        ("DIAG_French_1926-07_2002-12", r_fr, (1926, 7), (2002, 12)),
        ("DIAG_French_2003-01_2026-07", r_fr, (2003, 1), FIN),
        ("US_SP500TR_1988-02_1998-08", series["^SP500TR"], (1988, 2), (1998, 8)),
        ("US_SP500TR_1988-02_2002-12", series["^SP500TR"], (1988, 2), (2002, 12)),
        ("US_SP500TR_2003-01_2026-07", series["^SP500TR"], (2003, 1), FIN),
        ("US_GSPCprecio_2003-01_2026-07", series["^GSPC"], (2003, 1), FIN),
    ]
    casos_mx = [
        ("MX_MXX_1991-12_2002-12", series["^MXX"], (1991, 12), (2002, 12)),
        ("MX_MXX_1991-12_1998-08", series["^MXX"], (1991, 12), (1998, 8)),
        ("MX_MXX_2003-01_2026-07", series["^MXX"], (2003, 1), FIN),
        ("MX_EWW_1996-05_2002-12", series["EWW"], (1996, 5), (2002, 12)),
        ("MX_EWW_2003-01_2026-07", series["EWW"], (2003, 1), FIN),
    ]
    for grupo, lista in ((" EUA", casos), (" Mexico", casos_mx)):
        if grupo == " Mexico":
            p(" Mexico")
        for et, rr, a, b in lista:
            r = regresion_halloween(rr, a, b)
            imprimir_reg(et, r)
            res[et] = r
    p("\n  Diferencia anual pareada D_y (invierno - verano, suma de 6 meses, %)")
    sel = [c for c in casos if c[0] in ("US_Shiller_1970-01_1998-08", "US_Shiller_1926-07_2002-12",
                                        "DIAG_Hibrido_1970-01_1998-08", "DIAG_French_2003-01_2026-07",
                                        "US_SP500TR_2003-01_2026-07")]
    for et, rr, a, b in sel + [casos_mx[0], casos_mx[2], casos_mx[4]]:
        d = diferencia_anual(rr, a, b)
        imprimir_dy(et, d)
        res[et]["Dy"] = d

    # ---- estrategia
    p("\n2. Estrategia 2003-01..2026-07, costo 0.34% por lado, compra inicial cargada")
    nov_abr = lambda m: 1.0 if invierno(m) else 0.0  # noqa: E731
    siempre = lambda m: 1.0  # noqa: E731
    nunca = lambda m: 0.0  # noqa: E731
    for et, rr, rf in [("US ^SP500TR / TB3MS (USD)", series["^SP500TR"], rf_us),
                       ("DIAG US French Mkt / TB3MS (USD)", r_fr, rf_us),
                       ("MX ^MXX / CETES (MXN)", series["^MXX"], rf_mx),
                       ("MX EWW / TB3MS (USD)", series["EWW"], rf_us)]:
        p(" " + et)
        for nombre, regla in [("nov_abr", nov_abr), ("comprar_mantener", siempre), ("efectivo", nunca)]:
            e = estrategia(rr, rf, (2003, 1), FIN, regla)
            imprimir_est(nombre, e)
            res[f"EST {et} {nombre}"] = e

    # ---- criterios
    p("\n3. Criterios pre-registrados de R04 aplicados a B")
    a1 = res["US_Shiller_1970-01_1998-08"]
    a2 = res["US_Shiller_1926-07_2002-12"]
    a3 = res["US_SP500TR_2003-01_2026-07"]
    a4 = res["MX_MXX_2003-01_2026-07"]
    c1 = a1["alfa"] > 0 and abs(a1["alfa"] - 1.0349) <= 0.20 and a1["t_mco"] >= 1.96
    c2 = a2["alfa"] > 0 and a2["t_nw"] >= 2
    c3 = a3["alfa"] > 0
    c4 = a4["alfa"] > 0
    p(f"  (i)   EUA 1970-01..1998-08 alfa={a1['alfa']:+.4f} (|dif vs 1.0349|={abs(a1['alfa']-1.0349):.4f}) "
      f"t_MCO={a1['t_mco']:+.2f} -> {'CUMPLE' if c1 else 'NO CUMPLE'}")
    p(f"  (ii)  EUA 1926-07..2002-12 alfa={a2['alfa']:+.4f} t_NW={a2['t_nw']:+.2f} -> {'CUMPLE' if c2 else 'NO CUMPLE'}")
    p(f"  (iii) EUA 2003-01..2026-07 alfa={a3['alfa']:+.4f} -> {'CUMPLE' if c3 else 'NO CUMPLE'}")
    p(f"  (iv)  MX  2003-01..2026-07 alfa={a4['alfa']:+.4f} -> {'CUMPLE' if c4 else 'NO CUMPLE'}")
    if c1 and c2 and c3 and c4:
        estado = "Replicado"
    elif a1["alfa"] <= 0 or (not c3 and not c4):
        estado = "No replicado"
    elif a1["alfa"] > 0 and (c3 or c4):
        estado = "Replicado con diferencias"
    else:
        estado = "No replicado"
    for et in ["US_SP500TR_2003-01_2026-07", "MX_MXX_2003-01_2026-07", "MX_EWW_2003-01_2026-07"]:
        r = res[et]
        sigf = r["t_nw"] >= 2 and r["Dy"]["ic95"][0] > 0
        p(f"  Fuera de muestra {et}: {'significativo' if sigf else 'mismo signo, no significativo' if r['alfa'] > 0 else 'signo contrario'}")
    p(f"  ESTADO B: {estado}")
    res["estado"] = estado

    (AQUI / "salida.txt").write_text("\n".join(SALIDA) + "\n", encoding="utf-8")
    (AQUI / "resultados.json").write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")


if __name__ == "__main__":
    main()
