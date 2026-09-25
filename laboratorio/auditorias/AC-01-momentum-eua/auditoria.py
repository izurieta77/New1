#!/usr/bin/env python3
"""AC-01 - Auditoria ciega del factor momentum de EUA.

Reproducible sin red: lee unicamente los archivos congelados en ./datos/,
verifica sus SHA256 contra datos/SHA256SUMS.txt, calcula los estadisticos
pre-registrados (ver README.md) y escribe resultados.json.

Python 3.11, solo biblioteca estandar. Codigo escrito desde cero para esta
auditoria (no importa herramientas del repo).

Uso:  python3 auditoria.py            (escribe resultados.json e imprime tablas)
"""
import hashlib
import json
import math
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")

ARCH_MOM = "F-F_Momentum_Factor_CSV.zip"
ARCH_6P = "6_Portfolios_ME_Prior_12_2_CSV.zip"
ARCH_AQR = "Betting-Against-Beta-Equity-Factors-Monthly.xlsx"

VENTANAS = [
    ("W1", 198401, 200609),
    ("W2", 200610, 202512),
    ("W3", 200610, 201512),
    ("W4", 201601, 202512),
]
REZAGOS_NW = 6
Z95 = 1.96
FALTANTES = (-99.99, -999.0)
# Cota maxima de |B - A| atribuible solo a redondeo a 2 decimales:
# A redondeada (+-0.005) y B = 1/2(a+b) - 1/2(c+d) con 4 insumos redondeados (+-0.01)
COTA_REDONDEO = 0.015


# ---------------------------------------------------------------- integridad
def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 16), b""):
            h.update(bloque)
    return h.hexdigest()


def verificar_hashes():
    esperados = {}
    with open(os.path.join(DATOS, "SHA256SUMS.txt"), encoding="ascii") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            hx, nombre = linea.split(None, 1)
            esperados[nombre.lstrip("*")] = hx
    for nombre in (ARCH_MOM, ARCH_6P, ARCH_AQR):
        real = sha256(os.path.join(DATOS, nombre))
        if esperados.get(nombre) != real:
            sys.exit(f"ERROR: hash distinto para {nombre}: {real} vs {esperados.get(nombre)}")
    return esperados


# ---------------------------------------------------------------- lectura French
def leer_csv_de_zip(nombre_zip):
    with zipfile.ZipFile(os.path.join(DATOS, nombre_zip)) as z:
        miembros = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if len(miembros) != 1:
            sys.exit(f"ERROR: se esperaba 1 CSV en {nombre_zip}, hay {miembros}")
        texto = z.read(miembros[0]).decode("latin-1")
    return miembros[0], texto.splitlines()


def version_crsp(lineas):
    m = re.search(r"(\d{6}) CRSP", lineas[0])
    return f"CRSP {m.group(1)}" if m else lineas[0].strip()


def parsear_bloque(lineas, idx_cabecera):
    """Lee filas AAAAMM,v1,v2,... desde idx_cabecera+1 hasta la primera fila no mensual."""
    cols = [c.strip() for c in lineas[idx_cabecera].split(",")][1:]
    datos = {}
    for linea in lineas[idx_cabecera + 1:]:
        partes = [p.strip() for p in linea.split(",")]
        if not partes or not re.fullmatch(r"\d{6}", partes[0]):
            break
        vals = []
        for p in partes[1:]:
            v = float(p)
            vals.append(None if v in FALTANTES else v)
        datos[int(partes[0])] = dict(zip(cols, vals))
    return cols, datos


def leer_fuente_a():
    miembro, lineas = leer_csv_de_zip(ARCH_MOM)
    idx = next(i for i, l in enumerate(lineas) if l.strip().replace(" ", "") == ",Mom")
    cols, datos = parsear_bloque(lineas, idx)
    serie = {m: d["Mom"] for m, d in datos.items() if d["Mom"] is not None}
    return serie, {"archivo": ARCH_MOM, "miembro": miembro, "version": version_crsp(lineas),
                   "cabecera": lineas[0].strip(), "columna": "Mom", "seccion": "mensual (primer bloque)"}


def leer_fuente_b():
    miembro, lineas = leer_csv_de_zip(ARCH_6P)
    titulo = "Average Value Weighted Returns -- Monthly"
    idx_t = next(i for i, l in enumerate(lineas) if l.strip() == titulo)
    cols, datos = parsear_bloque(lineas, idx_t + 1)
    req = ["SMALL HiPRIOR", "BIG HiPRIOR", "SMALL LoPRIOR", "BIG LoPRIOR"]
    for c in req:
        if c not in cols:
            sys.exit(f"ERROR: falta columna {c} en {ARCH_6P}: {cols}")
    serie = {}
    for m, d in datos.items():
        if any(d[c] is None for c in req):
            continue
        serie[m] = 0.5 * (d["SMALL HiPRIOR"] + d["BIG HiPRIOR"]) - 0.5 * (d["SMALL LoPRIOR"] + d["BIG LoPRIOR"])
    return serie, {"archivo": ARCH_6P, "miembro": miembro, "version": version_crsp(lineas),
                   "cabecera": lineas[0].strip(), "seccion": titulo,
                   "formula": "1/2(SMALL HiPRIOR + BIG HiPRIOR) - 1/2(SMALL LoPRIOR + BIG LoPRIOR)"}


# ---------------------------------------------------------------- lectura AQR (xlsx)
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
NSR = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def _col_a_indice(letras):
    n = 0
    for ch in letras:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def leer_hoja_xlsx(ruta, nombre_hoja):
    with zipfile.ZipFile(ruta) as z:
        compartidas = []
        if "xl/sharedStrings.xml" in z.namelist():
            raiz = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in raiz.iter(NS + "si"):
                compartidas.append("".join(t.text or "" for t in si.iter(NS + "t")))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        destino = {r.attrib["Id"]: r.attrib["Target"] for r in rels}
        objetivo = None
        for hoja in wb.find(NS + "sheets"):
            if hoja.attrib["name"] == nombre_hoja:
                objetivo = destino[hoja.attrib[NSR + "id"]].lstrip("/")
                if not objetivo.startswith("xl/"):
                    objetivo = "xl/" + objetivo
        if objetivo is None:
            sys.exit(f"ERROR: no existe la hoja {nombre_hoja}")
        raiz = ET.fromstring(z.read(objetivo))
        fechas_miembros = sorted({"%04d-%02d-%02d %02d:%02d" % i.date_time[:5] for i in z.infolist()})
    filas = []
    for fila in raiz.iter(NS + "row"):
        celdas = {}
        for c in fila.findall(NS + "c"):
            col = _col_a_indice(re.match(r"[A-Z]+", c.attrib["r"]).group())
            t = c.attrib.get("t")
            v = c.find(NS + "v")
            if t == "s" and v is not None:
                val = compartidas[int(v.text)]
            elif t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter(NS + "t"))
            elif v is not None:
                val = v.text
            else:
                val = None
            celdas[col] = val
        filas.append(celdas)
    return filas, fechas_miembros


def _fecha_aqr_a_aaaamm(val):
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", val.strip())
    if m:
        return int(m.group(3)) * 100 + int(m.group(1))
    # respaldo: numero de serie de Excel (sistema 1900)
    try:
        serial = float(val)
    except ValueError:
        return None
    import datetime
    d = datetime.date(1899, 12, 30) + datetime.timedelta(days=int(serial))
    return d.year * 100 + d.month


def leer_fuente_c():
    ruta = os.path.join(DATOS, ARCH_AQR)
    filas, fechas_miembros = leer_hoja_xlsx(ruta, "UMD")
    i_cab = next(i for i, f in enumerate(filas) if f.get(0) == "DATE")
    cab = filas[i_cab]
    col_usa = next(k for k, v in cab.items() if v == "USA")
    serie = {}
    for f in filas[i_cab + 1:]:
        if not f.get(0):
            continue
        mes = _fecha_aqr_a_aaaamm(f[0])
        v = f.get(col_usa)
        if mes is None or v in (None, ""):
            continue
        serie[mes] = float(v) * 100.0  # AQR en fraccion decimal -> % mensual
    ultimo = max(serie)
    return serie, {"archivo": ARCH_AQR, "hoja": "UMD", "columna": "USA",
                   "version": f"AQR BAB Equity Factors Monthly, datos hasta {ultimo // 100}-{ultimo % 100:02d}",
                   "marcas_internas_xlsx": fechas_miembros,
                   "unidades_originales": "fraccion decimal (x100 para %)"}


# ---------------------------------------------------------------- estadistica
def media(x):
    return sum(x) / len(x)


def desv_est(x):
    m = media(x)
    return math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1))


def ee_newey_west(x, L=REZAGOS_NW):
    """Error estandar NW de la media: Bartlett w_j = 1 - j/(L+1), autocovarianzas con 1/n,
    correccion de muestra pequena n/(n-1)."""
    n = len(x)
    m = media(x)
    d = [v - m for v in x]
    s = sum(v * v for v in d) / n
    for j in range(1, L + 1):
        gamma = sum(d[t] * d[t - j] for t in range(j, n)) / n
        s += 2.0 * (1.0 - j / (L + 1.0)) * gamma
    s *= n / (n - 1.0)
    return math.sqrt(s / n)


def correlacion(x, y):
    mx, my = media(x), media(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy)


def mes_txt(m):
    return f"{m // 100}-{m % 100:02d}"


def meses_en(serie, ini, fin):
    return sorted(m for m in serie if ini <= m <= fin)


def meses_esperados(ini, fin):
    out, a, mm = [], ini // 100, ini % 100
    while a * 100 + mm <= fin:
        out.append(a * 100 + mm)
        mm += 1
        if mm == 13:
            a, mm = a + 1, 1
    return out


def estadisticos(serie, ini, fin):
    meses = meses_en(serie, ini, fin)
    esperados = meses_esperados(ini, fin)
    x = [serie[m] for m in meses]
    n = len(x)
    mu = media(x)
    sd = desv_est(x)
    t_iid = mu / (sd / math.sqrt(n))
    ee = ee_newey_west(x)
    t_nw = mu / ee
    li, ls = mu - Z95 * ee, mu + Z95 * ee
    prod = 1.0
    for v in x:
        prod *= 1.0 + v / 100.0
    comp = (prod ** (12.0 / n) - 1.0) * 100.0
    i_min = min(range(n), key=lambda i: x[i])
    i_max = max(range(n), key=lambda i: x[i])
    if li > 0:
        ver = "apoyo"
    elif ls < 0:
        ver = "contraria"
    else:
        ver = "inconcluso"
    return {
        "inicio": mes_txt(ini), "fin": mes_txt(fin),
        "n": n, "n_esperado": len(esperados),
        "cobertura_completa": meses == esperados,
        "primer_mes": mes_txt(meses[0]), "ultimo_mes": mes_txt(meses[-1]),
        "media_mensual_pct": mu,
        "desv_est_mensual_pct": sd,
        "t_iid": t_iid,
        "ee_nw_pct": ee,
        "t_nw6": t_nw,
        "ic95_nw_pct": [li, ls],
        "media_x12_pct": mu * 12.0,
        "media_x12_etiqueta": "no es CAGR",
        "compuesto_anual_pct": comp,
        "compuesto_etiqueta": "compuesto de la serie largo-corto; no es el rendimiento de una cuenta",
        "peor_mes": {"mes": mes_txt(meses[i_min]), "valor_pct": x[i_min]},
        "mejor_mes": {"mes": mes_txt(meses[i_max]), "valor_pct": x[i_max]},
        "veredicto": ver,
    }


def comparar(base, otra, ini=None, fin=None):
    """Compara otra vs base (dif = otra - base) en meses comunes."""
    comunes = sorted(set(base) & set(otra))
    if ini is not None:
        comunes = [m for m in comunes if ini <= m <= fin]
    a = [base[m] for m in comunes]
    b = [otra[m] for m in comunes]
    dif = [y - x for x, y in zip(a, b)]
    i_max = max(range(len(dif)), key=lambda i: abs(dif[i]))
    return {
        "periodo": f"{mes_txt(comunes[0])} a {mes_txt(comunes[-1])}",
        "n_comunes": len(comunes),
        "correlacion": correlacion(a, b),
        "dif_media_pct": media(dif),
        "max_dif_abs_pct": abs(dif[i_max]),
        "mes_max_dif": mes_txt(comunes[i_max]),
        "meses_dif_abs_mayor_0_015": sum(1 for d in dif if abs(d) > COTA_REDONDEO + 1e-9),
    }


# ---------------------------------------------------------------- redondeo para salida
def redondear(o, nd=6):
    if isinstance(o, float):
        return round(o, nd)
    if isinstance(o, dict):
        return {k: redondear(v, nd) for k, v in o.items()}
    if isinstance(o, list):
        return [redondear(v, nd) for v in o]
    return o


def main():
    hashes = verificar_hashes()
    a, meta_a = leer_fuente_a()
    b, meta_b = leer_fuente_b()
    c, meta_c = leer_fuente_c()
    fuentes = {
        "A_French_Mom": (a, meta_a),
        "B_French_reconstruccion_6P_VW": (b, meta_b),
        "C_AQR_UMD_USA": (c, meta_c),
    }
    res = {
        "auditoria": "AC-01-momentum-eua",
        "especificacion": {
            "ventanas": {w: [mes_txt(i), mes_txt(f)] for w, i, f in VENTANAS},
            "nw_rezagos": REZAGOS_NW, "nw_kernel": "Bartlett 1-j/(L+1)",
            "nw_correccion": "n/(n-1)", "z_ic95": Z95,
            "desv_est": "muestral, divisor n-1",
            "veredicto": "apoyo si IC95NW_inf>0; contraria si IC95NW_sup<0; inconcluso en otro caso",
            "unidades": "% mensual salvo indicacion",
        },
        "sha256": hashes,
        "fuentes": {},
        "estadisticos": {},
        "comparaciones": {},
    }
    for k, (s, meta) in fuentes.items():
        meta = dict(meta)
        meta["rango_total"] = f"{mes_txt(min(s))} a {mes_txt(max(s))}"
        meta["n_total"] = len(s)
        res["fuentes"][k] = meta
        res["estadisticos"][k] = {w: estadisticos(s, i, f) for w, i, f in VENTANAS}
    for nombre, otra in (("B_vs_A", b), ("C_vs_A", c)):
        comp = {"total_comun": comparar(a, otra)}
        for w, i, f in VENTANAS:
            comp[w] = comparar(a, otra, i, f)
        res["comparaciones"][nombre] = comp
    res["comparaciones"]["nota"] = ("dif = otra - A. 'meses_dif_abs_mayor_0_015' cuenta meses con |dif| > 0.015 pp, "
                                    "cota maxima atribuible solo a redondeo a 2 decimales (relevante para B vs A).")
    res = redondear(res)
    with open(os.path.join(AQUI, "resultados.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
        f.write("\n")
    imprimir(res)


def imprimir(res):
    print("Versiones:")
    for k, m in res["fuentes"].items():
        print(f"  {k}: {m['version']} | rango {m['rango_total']} | n={m['n_total']}")
    print()
    print("| Fuente | Ventana | n | Media %/mes | DE % | t IID | t NW(6) | IC95 NW % | Media x12 % (no es CAGR) "
          "| Compuesto anual % (serie L-C; no es cuenta) | Peor mes | Mejor mes | Veredicto |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for k, porv in res["estadisticos"].items():
        for w, e in porv.items():
            cob = "" if e["cobertura_completa"] else " (parcial)"
            print(f"| {k} | {w} {e['inicio']}..{e['fin']} | {e['n']}{cob} | {e['media_mensual_pct']:.3f} | "
                  f"{e['desv_est_mensual_pct']:.3f} | {e['t_iid']:.2f} | {e['t_nw6']:.2f} | "
                  f"[{e['ic95_nw_pct'][0]:.3f}, {e['ic95_nw_pct'][1]:.3f}] | {e['media_x12_pct']:.2f} | "
                  f"{e['compuesto_anual_pct']:.2f} | {e['peor_mes']['valor_pct']:.2f} ({e['peor_mes']['mes']}) | "
                  f"{e['mejor_mes']['valor_pct']:.2f} ({e['mejor_mes']['mes']}) | {e['veredicto']} |")
    print()
    print("| Comparacion | Tramo | Periodo | n | Correlacion | Dif media pp (otra-A) | Max |dif| pp (mes) | Meses |dif|>0.015 |")
    print("|---|---|---|---|---|---|---|---|")
    for nombre, porv in res["comparaciones"].items():
        if nombre == "nota":
            continue
        for w, cmp_ in porv.items():
            print(f"| {nombre} | {w} | {cmp_['periodo']} | {cmp_['n_comunes']} | {cmp_['correlacion']:.4f} | "
                  f"{cmp_['dif_media_pct']:.4f} | {cmp_['max_dif_abs_pct']:.4f} ({cmp_['mes_max_dif']}) | "
                  f"{cmp_['meses_dif_abs_mayor_0_015']} |")


if __name__ == "__main__":
    main()
