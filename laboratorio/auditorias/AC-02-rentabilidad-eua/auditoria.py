#!/usr/bin/env python3
"""AC-02 — Auditoría ciega del factor de rentabilidad (RMW) de EUA.

Reproducible sin red: lee solo archivos congelados en ./datos/, verifica SHA256,
calcula estadísticos por ventana y fuente, y escribe ./resultados.json.

Python 3.11, solo biblioteca estándar. Newey-West (Bartlett, L=6, corrección n/(n-1))
y t convencional IID implementados aquí desde cero.

Fuentes:
  A  = French, F-F_Research_Data_5_Factors_2x3, columna RMW (% mensual)
  B  = French, 6_Portfolios_ME_OP_2x3 (value-weighted),
       RMW_B = 1/2 (Small HiOP + Big HiOP) - 1/2 (Small LoOP + Big LoOP)
  C1 = Hou-Xue-Zhang q5, R_ROE (% mensual)
  C2 = AQR Quality Minus Junk, columna USA (decimal -> % mensual)
"""
import hashlib
import json
import math
import os
import re
import zipfile
import xml.etree.ElementTree as ET

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
SALIDA = os.path.join(AQUI, "resultados.json")

VENTANAS = [
    ("W1", 196307, 199912),
    ("W2", 200001, 202512),
    ("W3", 201501, 202512),
    ("W4", 201601, 202512),
]
L_NW = 6
Z95 = 1.96

ARCH_FF5 = "F-F_Research_Data_5_Factors_2x3_CSV.zip"
ARCH_6P = "6_Portfolios_ME_OP_2x3_CSV.zip"
ARCH_Q5 = "q5_factors_monthly_2025.csv"
ARCH_QMJ = "Quality-Minus-Junk-Factors-Monthly.xlsx"


# ---------------------------------------------------------------- integridad
def verificar_sha256():
    esperado = {}
    with open(os.path.join(DATOS, "SHA256SUMS.txt"), encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            h, nombre = linea.split(None, 1)
            esperado[nombre.lstrip("*")] = h
    res = {}
    for nombre, h in esperado.items():
        with open(os.path.join(DATOS, nombre), "rb") as f:
            real = hashlib.sha256(f.read()).hexdigest()
        if real != h:
            raise SystemExit(f"SHA256 no coincide para {nombre}: {real} != {h}")
        res[nombre] = h
    return res


# ---------------------------------------------------------------- lectores
def _leer_zip_texto(nombre_zip):
    z = zipfile.ZipFile(os.path.join(DATOS, nombre_zip))
    miembros = z.namelist()
    assert len(miembros) == 1, miembros
    info = z.getinfo(miembros[0])
    return z.read(miembros[0]).decode("latin-1"), miembros[0], info.date_time


def _seccion_mensual(lineas, idx_cabecera):
    """Lee filas YYYYMM,... a partir de la línea de cabecera hasta la primera línea vacía."""
    cab = [c.strip() for c in lineas[idx_cabecera].split(",")]
    filas = {}
    for linea in lineas[idx_cabecera + 1:]:
        s = linea.strip()
        if not s:
            break
        partes = [p.strip() for p in s.split(",")]
        if not re.fullmatch(r"\d{6}", partes[0]):
            break
        filas[int(partes[0])] = [float(x) for x in partes[1:]]
    return cab, filas


def leer_ff5():
    texto, miembro, fecha_zip = _leer_zip_texto(ARCH_FF5)
    lineas = texto.splitlines()
    version = lineas[0].strip()
    idx = next(i for i, l in enumerate(lineas) if l.strip().startswith(",Mkt-RF"))
    cab, filas = _seccion_mensual(lineas, idx)
    j = cab.index("RMW") - 1
    serie = {ym: v[j] for ym, v in filas.items()}
    meta = {"archivo": ARCH_FF5, "miembro": miembro, "fecha_interna_zip": list(fecha_zip),
            "cabecera": version, "columna": "RMW", "unidades": "% mensual",
            "primer_mes": min(serie), "ultimo_mes": max(serie)}
    return serie, meta


def leer_6p_me_op():
    texto, miembro, fecha_zip = _leer_zip_texto(ARCH_6P)
    lineas = texto.splitlines()
    version = lineas[0].strip()
    idx_titulo = next(i for i, l in enumerate(lineas)
                      if "Average Value Weighted Returns -- Monthly" in l)
    idx = idx_titulo + 1
    cab, filas = _seccion_mensual(lineas, idx)
    cols = cab[1:]
    iSL, iSH = cols.index("SMALL LoOP"), cols.index("SMALL HiOP")
    iBL, iBH = cols.index("BIG LoOP"), cols.index("BIG HiOP")
    serie = {}
    faltantes = 0
    for ym, v in filas.items():
        vals = [v[iSL], v[iSH], v[iBL], v[iBH]]
        if any(x <= -99.99 for x in vals):
            faltantes += 1
            continue
        serie[ym] = 0.5 * (v[iSH] + v[iBH]) - 0.5 * (v[iSL] + v[iBL])
    meta = {"archivo": ARCH_6P, "miembro": miembro, "fecha_interna_zip": list(fecha_zip),
            "cabecera": version, "seccion": "Average Value Weighted Returns -- Monthly",
            "columnas_usadas": ["SMALL HiOP", "BIG HiOP", "SMALL LoOP", "BIG LoOP"],
            "formula": "0.5*(SMALL HiOP + BIG HiOP) - 0.5*(SMALL LoOP + BIG LoOP)",
            "meses_con_faltantes_excluidos": faltantes, "unidades": "% mensual",
            "primer_mes": min(serie), "ultimo_mes": max(serie)}
    return serie, meta


def leer_q5():
    with open(os.path.join(DATOS, ARCH_Q5), encoding="utf-8") as f:
        lineas = [l.strip() for l in f if l.strip()]
    cab = lineas[0].split(",")
    iy, im, ir = cab.index("year"), cab.index("month"), cab.index("R_ROE")
    serie = {}
    for l in lineas[1:]:
        p = l.split(",")
        serie[int(p[iy]) * 100 + int(p[im])] = float(p[ir])
    meta = {"archivo": ARCH_Q5, "cabecera": lineas[0], "columna": "R_ROE",
            "unidades": "% mensual",
            "version": "global-q.org, 'Latest Release, 7/30/2026' (pagina guardada en datos/globalq_factors_page.html); archivo muestra 1967-2025",
            "primer_mes": min(serie), "ultimo_mes": max(serie)}
    return serie, meta


_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_NSR = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def _col_a_indice(letras):
    n = 0
    for ch in letras:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def leer_xlsx_hoja(ruta, nombre_hoja):
    """Lector mínimo xlsx: sharedStrings + XML de la hoja. Devuelve lista de dict{col: texto}."""
    z = zipfile.ZipFile(ruta)
    compartidas = []
    if "xl/sharedStrings.xml" in z.namelist():
        raiz = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in raiz.findall(_NS + "si"):
            compartidas.append("".join(t.text or "" for t in si.iter(_NS + "t")))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    mapa = {r.get("Id"): r.get("Target") for r in rels}
    destino = None
    for s in wb.find(_NS + "sheets"):
        if s.get("name") == nombre_hoja:
            t = mapa[s.get(_NSR)].lstrip("/")
            destino = t if t.startswith("xl/") else "xl/" + t
    if destino is None:
        raise SystemExit(f"Hoja {nombre_hoja!r} no encontrada en {ruta}")
    raiz = ET.fromstring(z.read(destino))
    filas = []
    for fila in raiz.iter(_NS + "row"):
        d = {}
        for c in fila.findall(_NS + "c"):
            col = _col_a_indice(re.match(r"[A-Z]+", c.get("r")).group())
            tipo = c.get("t")
            v = c.find(_NS + "v")
            if tipo == "s" and v is not None:
                d[col] = compartidas[int(v.text)]
            elif tipo == "inlineStr":
                d[col] = "".join(x.text or "" for x in c.iter(_NS + "t"))
            elif v is not None:
                d[col] = v.text
        filas.append(d)
    return filas


def leer_qmj():
    ruta = os.path.join(DATOS, ARCH_QMJ)
    filas = leer_xlsx_hoja(ruta, "QMJ Factors")
    titulo = filas[0].get(0, "")
    idx_cab = next(i for i, f in enumerate(filas) if f.get(0) == "DATE")
    cab = filas[idx_cab]
    col_usa = next(k for k, v in cab.items() if v == "USA")
    serie = {}
    for f in filas[idx_cab + 1:]:
        d = f.get(0)
        if not d or not re.fullmatch(r"\d{2}/\d{2}/\d{4}", d):
            continue
        v = f.get(col_usa)
        if v is None or v == "":
            continue
        mm, _, yyyy = d.split("/")
        serie[int(yyyy) * 100 + int(mm)] = float(v) * 100.0
    meta = {"archivo": ARCH_QMJ, "hoja": "QMJ Factors", "titulo": titulo, "columna": "USA",
            "unidades": "decimal en archivo; convertido a % mensual (x100)",
            "version": "sin sello de version en el archivo; AQR reconstruye el historico en cada actualizacion; version identificada por SHA256 y ultimo mes",
            "primer_mes": min(serie), "ultimo_mes": max(serie)}
    return serie, meta


# ---------------------------------------------------------------- estadística
def media(x):
    return sum(x) / len(x)


def desv_est(x):
    m = media(x)
    return math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1))


def ee_newey_west(x, L=L_NW):
    """EE de la media, Newey-West con kernel de Bartlett y corrección n/(n-1)."""
    n = len(x)
    m = media(x)
    e = [v - m for v in x]
    s = sum(v * v for v in e) / n
    for j in range(1, L + 1):
        gj = sum(e[t] * e[t - j] for t in range(j, n)) / n
        s += 2.0 * (1.0 - j / (L + 1.0)) * gj
    s *= n / (n - 1.0)
    return math.sqrt(s / n)


def veredicto(lo, hi):
    if lo > 0:
        return "apoyo"
    if hi < 0:
        return "contraria"
    return "inconcluso"


def ym_txt(ym):
    return f"{ym // 100:04d}-{ym % 100:02d}"


def estadisticos(serie, ini, fin):
    meses = sorted(ym for ym in serie if ini <= ym <= fin)
    if len(meses) < 3:
        return None
    x = [serie[ym] for ym in meses]
    n = len(x)
    m = media(x)
    sd = desv_est(x)
    t_iid = m / (sd / math.sqrt(n))
    ee = ee_newey_west(x)
    t_nw = m / ee
    lo, hi = m - Z95 * ee, m + Z95 * ee
    prod = 1.0
    for v in x:
        prod *= 1.0 + v / 100.0
    comp = (prod ** (12.0 / n) - 1.0) * 100.0
    i_min = min(range(n), key=lambda i: x[i])
    i_max = max(range(n), key=lambda i: x[i])
    # meses faltantes dentro del rango efectivo
    esperado = 0
    y, mo = meses[0] // 100, meses[0] % 100
    while y * 100 + mo <= meses[-1]:
        esperado += 1
        mo += 1
        if mo == 13:
            y, mo = y + 1, 1
    return {
        "ventana_pedida": f"{ym_txt(ini)} a {ym_txt(fin)}",
        "ventana_efectiva": f"{ym_txt(meses[0])} a {ym_txt(meses[-1])}",
        "n": n,
        "huecos_en_ventana_efectiva": esperado - n,
        "media_mensual_pct": m,
        "desv_est_mensual_pct": sd,
        "t_iid": t_iid,
        "ee_nw_mensual_pct": ee,
        "t_nw6": t_nw,
        "ic95_nw_mensual_pct": [lo, hi],
        "ic95_nw_x12_pct": [lo * 12, hi * 12],
        "media_x12_pct": m * 12,
        "media_x12_etiqueta": "media aritmetica x12; no es CAGR",
        "compuesto_anual_pct": comp,
        "compuesto_etiqueta": "compuesto de la serie largo-corto; no es el rendimiento de una cuenta",
        "peor_mes": {"mes": ym_txt(meses[i_min]), "pct": x[i_min]},
        "mejor_mes": {"mes": ym_txt(meses[i_max]), "pct": x[i_max]},
        "veredicto": veredicto(lo, hi),
    }


def correlacion(a, b):
    ma, mb = media(a), media(b)
    sab = sum((u - ma) * (v - mb) for u, v in zip(a, b))
    saa = sum((u - ma) ** 2 for u in a)
    sbb = sum((v - mb) ** 2 for v in b)
    return sab / math.sqrt(saa * sbb)


def comparar_mes_a_mes(sa, sb, ini, fin):
    meses = sorted(ym for ym in sa if ym in sb and ini <= ym <= fin)
    a = [sa[m] for m in meses]
    b = [sb[m] for m in meses]
    d = [v - u for u, v in zip(a, b)]  # B - A
    i_max = max(range(len(d)), key=lambda i: abs(d[i]))
    return {
        "ventana_efectiva": f"{ym_txt(meses[0])} a {ym_txt(meses[-1])}",
        "n_comun": len(meses),
        "correlacion": correlacion(a, b),
        "dif_media_B_menos_A_pct_mensual": media(d),
        "dif_media_B_menos_A_x12_pct": media(d) * 12,
        "desv_est_dif_pct": desv_est(d),
        "max_abs_dif_pct": abs(d[i_max]),
        "mes_max_abs_dif": ym_txt(meses[i_max]),
        "meses_abs_dif_mayor_0p01": sum(1 for v in d if abs(v) > 0.01),
        "meses_abs_dif_mayor_0p5": sum(1 for v in d if abs(v) > 0.5),
        "t_nw6_de_la_diferencia": media(d) / ee_newey_west(d),
    }


def correlaciones(series, ini, fin):
    nombres = list(series)
    out = {}
    for i in range(len(nombres)):
        for j in range(i + 1, len(nombres)):
            a, b = nombres[i], nombres[j]
            meses = sorted(ym for ym in series[a] if ym in series[b] and ini <= ym <= fin)
            if len(meses) < 3:
                continue
            out[f"{a}~{b}"] = {
                "n_comun": len(meses),
                "desde": ym_txt(meses[0]), "hasta": ym_txt(meses[-1]),
                "r": correlacion([series[a][m] for m in meses], [series[b][m] for m in meses]),
            }
    return out


# ---------------------------------------------------------------- criterio sección 6
RANGO_NIVEL = (4.0, 5.3)  # "~4.5-4.8%" interpretado como [4.5-0.5, 4.8+0.5], fijado antes de calcular


def evaluar_afirmacion(est, exigir_nivel):
    w2, w3, w4 = est.get("W2"), est.get("W3"), est.get("W4")
    patron = (w2 is not None and w2["veredicto"] == "apoyo"
              and w3 is not None and w3["veredicto"] == "inconcluso"
              and w4 is not None and w4["veredicto"] == "inconcluso")
    res = {
        "W2_apoyo": w2 is not None and w2["veredicto"] == "apoyo",
        "W3_inconcluso": w3 is not None and w3["veredicto"] == "inconcluso",
        "W4_inconcluso": w4 is not None and w4["veredicto"] == "inconcluso",
        "patron_significancia_se_sostiene": patron,
    }
    if w2 is not None:
        n12 = RANGO_NIVEL[0] <= w2["media_x12_pct"] <= RANGO_NIVEL[1]
        nc = RANGO_NIVEL[0] <= w2["compuesto_anual_pct"] <= RANGO_NIVEL[1]
        res["W2_media_x12_en_rango_4.0_5.3"] = n12
        res["W2_compuesto_en_rango_4.0_5.3"] = nc
        if exigir_nivel:
            res["se_sostiene_con_media_x12"] = patron and n12
            res["se_sostiene_con_compuesto"] = patron and nc
        else:
            res["nota"] = "constructo distinto de RMW: nivel reportado pero no exigido (seccion 6)"
            res["se_sostiene_con_media_x12"] = patron
            res["se_sostiene_con_compuesto"] = patron
    return res


# ---------------------------------------------------------------- principal
def main():
    sha = verificar_sha256()
    A, metaA = leer_ff5()
    B, metaB = leer_6p_me_op()
    C1, metaC1 = leer_q5()
    C2, metaC2 = leer_qmj()
    fuentes = {
        "A_FF5_RMW": (A, metaA, True),
        "B_reconstruccion_6P_ME_OP": (B, metaB, True),
        "C1_HXZ_R_ROE": (C1, metaC1, False),
        "C2_AQR_QMJ_USA": (C2, metaC2, False),
    }
    resultados = {
        "id": "AC-02-rentabilidad-eua",
        "especificacion": {
            "ventanas": {w: [ym_txt(i), ym_txt(f)] for w, i, f in VENTANAS},
            "newey_west": {"rezagos": L_NW, "kernel": "Bartlett w_j=1-j/(L+1)",
                           "correccion": "n/(n-1)", "z": Z95},
            "veredicto": "apoyo si IC95 NW inferior > 0; contraria si superior < 0; inconcluso en otro caso",
            "compuesto": "(prod(1+r_t/100))^(12/n)-1",
            "rango_nivel_afirmacion_pct": list(RANGO_NIVEL),
        },
        "sha256": sha,
        "fuentes": {},
        "estadisticos": {},
        "comparacion_A_vs_B": {},
        "correlaciones": {},
        "evaluacion_afirmacion": {},
    }
    for nombre, (serie, meta, exigir) in fuentes.items():
        meta = dict(meta)
        meta["primer_mes"] = ym_txt(meta["primer_mes"])
        meta["ultimo_mes"] = ym_txt(meta["ultimo_mes"])
        resultados["fuentes"][nombre] = meta
        est = {}
        for w, i, f in VENTANAS:
            est[w] = estadisticos(serie, i, f)
        resultados["estadisticos"][nombre] = est
        resultados["evaluacion_afirmacion"][nombre] = evaluar_afirmacion(est, exigir)
    series = {k: v[0] for k, v in fuentes.items()}
    for w, i, f in VENTANAS:
        resultados["comparacion_A_vs_B"][w] = comparar_mes_a_mes(A, B, i, f)
        resultados["correlaciones"][w] = correlaciones(series, i, f)
    resultados["comparacion_A_vs_B"]["muestra_comun_completa"] = comparar_mes_a_mes(
        A, B, 0, 999999)
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    imprimir(resultados)


def imprimir(r):
    print("SHA256 verificado para", len(r["sha256"]), "archivos")
    for nombre, meta in r["fuentes"].items():
        print(f"{nombre}: {meta['primer_mes']}..{meta['ultimo_mes']}  |  "
              f"{meta.get('cabecera', '')[:70]}")
    print()
    enc = (f"{'fuente':28s} {'ven':3s} {'efectiva':19s} {'n':>4s} {'media%':>7s} {'sd%':>6s} "
           f"{'tIID':>6s} {'tNW6':>6s} {'IC95NW(mes)':>17s} {'x12%':>6s} {'comp%':>6s} "
           f"{'peor':>15s} {'mejor':>15s} veredicto")
    print(enc)
    for nombre, est in r["estadisticos"].items():
        for w, e in est.items():
            if e is None:
                print(f"{nombre:28s} {w:3s} sin datos")
                continue
            print(f"{nombre:28s} {w:3s} {e['ventana_efectiva']:19s} {e['n']:4d} "
                  f"{e['media_mensual_pct']:7.3f} {e['desv_est_mensual_pct']:6.3f} "
                  f"{e['t_iid']:6.2f} {e['t_nw6']:6.2f} "
                  f"[{e['ic95_nw_mensual_pct'][0]:6.3f},{e['ic95_nw_mensual_pct'][1]:6.3f}] "
                  f"{e['media_x12_pct']:6.2f} {e['compuesto_anual_pct']:6.2f} "
                  f"{e['peor_mes']['pct']:7.2f}@{e['peor_mes']['mes']} "
                  f"{e['mejor_mes']['pct']:6.2f}@{e['mejor_mes']['mes']} {e['veredicto']}")
    print("\nComparacion mes a mes A (oficial) vs B (reconstruccion):")
    for w, c in r["comparacion_A_vs_B"].items():
        print(f"  {w}: n={c['n_comun']} r={c['correlacion']:.5f} difmedia(B-A)={c['dif_media_B_menos_A_pct_mensual']:.4f}%/mes "
              f"(x12 {c['dif_media_B_menos_A_x12_pct']:.3f}) sd_dif={c['desv_est_dif_pct']:.4f} "
              f"max|dif|={c['max_abs_dif_pct']:.4f}@{c['mes_max_abs_dif']} "
              f">0.01:{c['meses_abs_dif_mayor_0p01']} >0.5:{c['meses_abs_dif_mayor_0p5']} "
              f"tNW(dif)={c['t_nw6_de_la_diferencia']:.2f}")
    print("\nCorrelaciones:")
    for w, cs in r["correlaciones"].items():
        for par, c in cs.items():
            print(f"  {w} {par:45s} n={c['n_comun']:4d} {c['desde']}..{c['hasta']} r={c['r']:.3f}")
    print("\nEvaluacion de la afirmacion:")
    for nombre, ev in r["evaluacion_afirmacion"].items():
        print(f"  {nombre}: {ev}")


if __name__ == "__main__":
    main()
