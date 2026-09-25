#!/usr/bin/env python3
"""AC-03 momentum internacional -- auditoria ciega.

Reproducible sin red: lee solo archivos congelados en datos/ (verifica SHA256SUMS.txt).
Python 3.11, solo biblioteca estandar. Escribe resultados.json e imprime tablas.

Especificacion: ver README.md seccion 2 (pre-registrada) y adenda 1.
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
SALIDA = os.path.join(AQUI, "resultados.json")

LAGS_NW = 6
Z95 = 1.96

REGIONES_A = ["Emerging", "Developed_ex_US", "Europe", "Asia_Pacific_ex_Japan", "Japan", "North_America"]
# archivo de portafolios 2x3 por region (French usa "Emerging_Markets" en este archivo)
ARCHIVO_B = {
    "Emerging": "Emerging_Markets_6_Portfolios_ME_Prior_12_2_CSV.zip",
    "Developed_ex_US": "Developed_ex_US_6_Portfolios_ME_Prior_12_2_CSV.zip",
    "Europe": "Europe_6_Portfolios_ME_Prior_12_2_CSV.zip",
    "Asia_Pacific_ex_Japan": "Asia_Pacific_ex_Japan_6_Portfolios_ME_Prior_12_2_CSV.zip",
    "Japan": "Japan_6_Portfolios_ME_Prior_12_2_CSV.zip",
    "North_America": "North_America_6_Portfolios_ME_Prior_12_2_CSV.zip",
}
ARCHIVO_C = "AQR_Betting-Against-Beta-Equity-Factors-Monthly.xlsx"

VENTANAS = [
    ("V1", "2000-01 a ultimo mes", 200001, None),
    ("V2", "2010-01 a ultimo mes", 201001, None),
    ("V3", "2016-01 a 2025-12", 201601, 202512),
]

# pares comparables (A/B region French, columna AQR, nota)
PARES_C = [
    ("Europe", "Europe", "misma region nominal; AQR = promedio ponderado de factores por pais"),
    ("Japan", "JPN", "mismo pais"),
    ("North_America", "North America", "misma region nominal; AQR = USA+CAN ponderado"),
    ("Developed_ex_US", "Global Ex USA", "aproximado; universos de paises distintos"),
    ("Asia_Pacific_ex_Japan", "Pacific", "NO equivalente: AQR Pacific incluye Japon"),
]

AFIRMACION_EMERGENTES = {"V1": 9.6, "V2": 12.3}
TOL_PP = 0.15


# ----------------------------------------------------------------------------- utilidades
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def verificar_sumas():
    res = []
    with open(os.path.join(DATOS, "SHA256SUMS.txt"), encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            esperado, nombre = linea.split(None, 1)
            nombre = nombre.lstrip("*")
            real = sha256(os.path.join(DATOS, nombre))
            res.append({"archivo": nombre, "sha256": real, "ok": real == esperado})
    malos = [r["archivo"] for r in res if not r["ok"]]
    if malos:
        sys.exit("ERROR: SHA256 no coincide para: %s" % malos)
    return res


def ym_txt(ym):
    return "%04d-%02d" % (ym // 100, ym % 100)


# ----------------------------------------------------------------------------- lectores French
def leer_csv_zip(nombre):
    z = zipfile.ZipFile(os.path.join(DATOS, nombre))
    interno = z.namelist()[0]
    texto = z.read(interno).decode("latin-1")
    return interno, texto.splitlines()


def bloque_mensual(lineas, titulo=None):
    """Devuelve (cabecera, {yyyymm: [valores]}) del primer bloque mensual
    (o del bloque cuyo titulo contiene `titulo`)."""
    i = 0
    if titulo is not None:
        while i < len(lineas) and titulo not in lineas[i]:
            i += 1
        if i == len(lineas):
            raise ValueError("no se encontro bloque %r" % titulo)
        i += 1
    # buscar cabecera (linea que empieza con coma)
    while i < len(lineas) and not lineas[i].startswith(","):
        i += 1
    cab = [c.strip() for c in lineas[i].split(",")[1:]]
    i += 1
    datos = {}
    while i < len(lineas):
        partes = [p.strip() for p in lineas[i].split(",")]
        if not partes[0].isdigit() or len(partes[0]) != 6:
            break
        vals = []
        for p in partes[1:]:
            v = float(p)
            vals.append(None if abs(v - (-99.99)) < 1e-9 or abs(v - (-999)) < 1e-9 else v)
        datos[int(partes[0])] = vals
        i += 1
    return cab, datos


def serie_A(region):
    nombre = "%s_MOM_Factor_CSV.zip" % region
    interno, lineas = leer_csv_zip(nombre)
    cab, datos = bloque_mensual(lineas)
    j = cab.index("WML")
    serie = {ym: v[j] for ym, v in datos.items()}
    return nombre, lineas[0].strip(), serie


def serie_B(region):
    nombre = ARCHIVO_B[region]
    interno, lineas = leer_csv_zip(nombre)
    cab, datos = bloque_mensual(lineas, "Average Value Weighted Returns -- Monthly")
    idx = {c: k for k, c in enumerate(cab)}
    sl, sh = idx["SMALL LoPRIOR"], idx["SMALL HiPRIOR"]
    bl, bh = idx["BIG LoPRIOR"], idx["BIG HiPRIOR"]
    serie = {}
    for ym, v in datos.items():
        if None in (v[sl], v[sh], v[bl], v[bh]):
            serie[ym] = None
        else:
            serie[ym] = 0.5 * (v[sh] + v[bh]) - 0.5 * (v[sl] + v[bl])
    return nombre, lineas[0].strip(), serie


# ----------------------------------------------------------------------------- lector xlsx (AQR)
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def _col(ref):
    letras = re.match(r"[A-Z]+", ref).group()
    n = 0
    for ch in letras:
        n = n * 26 + ord(ch) - 64
    return n - 1


def leer_hoja_xlsx(nombre, hoja):
    z = zipfile.ZipFile(os.path.join(DATOS, nombre))
    compartidas = []
    if "xl/sharedStrings.xml" in z.namelist():
        raiz = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in raiz.findall("m:si", NS):
            compartidas.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    mapa = {r.get("Id"): r.get("Target") for r in rels}
    destino = None
    for s in wb.find("m:sheets", NS):
        if s.get("name") == hoja:
            destino = mapa[s.get("{%s}id" % NS["r"])]
    if destino is None:
        raise ValueError("hoja %r no existe" % hoja)
    destino = destino[1:] if destino.startswith("/") else "xl/" + destino
    raiz = ET.fromstring(z.read(destino))
    filas = []
    for fila in raiz.iter("{%s}row" % NS["m"]):
        d = {}
        for c in fila.findall("m:c", NS):
            t = c.get("t")
            v = c.find("m:v", NS)
            if t == "s" and v is not None:
                val = compartidas[int(v.text)]
            elif t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
            elif v is not None:
                val = v.text
            else:
                val = None
            d[_col(c.get("r"))] = val
        filas.append(d)
    return filas


def series_C():
    filas = leer_hoja_xlsx(ARCHIVO_C, "UMD")
    cab = None
    series = {}
    for d in filas:
        if cab is None:
            if d.get(0) == "DATE":
                cab = {k: v for k, v in d.items() if k > 0 and v}
                for nom in cab.values():
                    series[nom] = {}
            continue
        f = d.get(0)
        if not f or not re.match(r"\d{2}/\d{2}/\d{4}$", str(f)):
            continue
        mes, _dia, anio = str(f).split("/")
        ym = int(anio) * 100 + int(mes)
        for k, nom in cab.items():
            v = d.get(k)
            if v not in (None, ""):
                series[nom][ym] = float(v) * 100.0  # decimal -> %
    # texto de cabecera (primeras lineas descriptivas)
    desc = [str(d.get(0)) for d in filas[:8] if d.get(0)]
    return ARCHIVO_C, desc, series


# ----------------------------------------------------------------------------- estadistica propia
def media(x):
    return sum(x) / len(x)


def desv_est(x):
    m = media(x)
    return math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1))


def ee_newey_west(x, lags=LAGS_NW):
    """Error estandar NW de la media: Bartlett, correccion n/(n-1)."""
    n = len(x)
    m = media(x)
    e = [v - m for v in x]
    s = sum(v * v for v in e) / n
    for j in range(1, lags + 1):
        g = sum(e[t] * e[t - j] for t in range(j, n)) / n
        s += 2.0 * (1.0 - j / (lags + 1.0)) * g
    s *= n / (n - 1.0)
    return math.sqrt(s / n)


def veredicto(lo, hi):
    if lo > 0:
        return "apoyo"
    if hi < 0:
        return "contraria"
    return "inconcluso"


def estadisticos(serie, inicio, fin):
    meses = sorted(ym for ym in serie if ym >= inicio and (fin is None or ym <= fin))
    validos = [(ym, serie[ym]) for ym in meses if serie[ym] is not None]
    faltantes = len(meses) - len(validos)
    if len(validos) < 24:
        return {"n": len(validos), "nota": "muestra insuficiente (<24)"}
    x = [v for _, v in validos]
    n = len(x)
    m = media(x)
    sd = desv_est(x)
    ee_iid = sd / math.sqrt(n)
    ee_nw = ee_newey_west(x)
    lo, hi = m - Z95 * ee_nw, m + Z95 * ee_nw
    prod = 1.0
    for v in x:
        prod *= 1.0 + v / 100.0
    comp = (prod ** (12.0 / n) - 1.0) * 100.0 if prod > 0 else None
    peor = min(validos, key=lambda p: p[1])
    mejor = max(validos, key=lambda p: p[1])
    return {
        "desde": ym_txt(validos[0][0]),
        "hasta": ym_txt(validos[-1][0]),
        "n": n,
        "meses_faltantes": faltantes,
        "media_mensual_pct": m,
        "desv_est_pct": sd,
        "t_iid": m / ee_iid,
        "ee_nw_pct": ee_nw,
        "t_nw": m / ee_nw,
        "ic95_nw_pct": [lo, hi],
        "media_x12_pct_no_es_CAGR": 12.0 * m,
        "compuesto_anual_pct_serie_largo_corto_no_es_rendimiento_de_cuenta": comp,
        "peor_mes": {"fecha": ym_txt(peor[0]), "pct": peor[1]},
        "mejor_mes": {"fecha": ym_txt(mejor[0]), "pct": mejor[1]},
        "veredicto": veredicto(lo, hi),
    }


def concordancia(s1, s2):
    comunes = sorted(ym for ym in s1 if ym in s2 and s1[ym] is not None and s2[ym] is not None)
    if len(comunes) < 24:
        return {"n_comun": len(comunes)}
    a = [s1[ym] for ym in comunes]
    b = [s2[ym] for ym in comunes]
    ma, mb = media(a), media(b)
    cov = sum((p - ma) * (q - mb) for p, q in zip(a, b))
    va = sum((p - ma) ** 2 for p in a)
    vb = sum((q - mb) ** 2 for q in b)
    dif = [p - q for p, q in zip(a, b)]
    return {
        "desde": ym_txt(comunes[0]),
        "hasta": ym_txt(comunes[-1]),
        "n_comun": len(comunes),
        "correlacion": cov / math.sqrt(va * vb),
        "media_x12_1_pct": 12 * ma,
        "media_x12_2_pct": 12 * mb,
        "media_dif_mensual_pct": media(dif),
        "max_abs_dif_pct": max(abs(d) for d in dif),
    }


def recortar(serie, inicio, fin=None):
    return {ym: v for ym, v in serie.items() if ym >= inicio and (fin is None or ym <= fin)}


def redondear(obj, nd=6):
    if isinstance(obj, float):
        return round(obj, nd)
    if isinstance(obj, dict):
        return {k: redondear(v, nd) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redondear(v, nd) for v in obj]
    return obj


# ----------------------------------------------------------------------------- principal
def main():
    sumas = verificar_sumas()
    archivos = {s["archivo"]: {"sha256": s["sha256"]} for s in sumas}

    series = {}  # clave -> dict
    for reg in REGIONES_A:
        nom, cab, s = serie_A(reg)
        archivos[nom]["version_cabecera"] = cab
        series["A|" + reg] = {"fuente": "A French MOM/WML", "archivo": nom, "columna": "WML", "serie": s}
        nom, cab, s = serie_B(reg)
        archivos[nom]["version_cabecera"] = cab
        series["B|" + reg] = {"fuente": "B reconstruccion French 2x3 VW",
                              "archivo": nom,
                              "columna": "0.5*(SMALL HiPRIOR+BIG HiPRIOR)-0.5*(SMALL LoPRIOR+BIG LoPRIOR)",
                              "serie": s}
    nom, desc, sc = series_C()
    archivos[nom]["version_cabecera"] = " / ".join(desc)
    for col, s in sc.items():
        series["C|" + col] = {"fuente": "C AQR UMD", "archivo": nom, "columna": col, "serie": s}

    resultados = {}
    for clave, info in series.items():
        s = info["serie"]
        meses_validos = sorted(ym for ym, v in s.items() if v is not None)
        ult = meses_validos[-1]
        vent = {}
        for vid, etiqueta, ini, fin in VENTANAS:
            r = estadisticos(s, ini, fin)
            r["etiqueta"] = etiqueta
            vent[vid] = r
        resultados[clave] = {
            "fuente": info["fuente"], "archivo": info["archivo"], "columna": info["columna"],
            "primer_mes": ym_txt(meses_validos[0]), "ultimo_mes": ym_txt(ult),
            "ventanas": vent,
        }

    # --- diagnostico A vs B (misma base French)
    diag_ab = {}
    for reg in REGIONES_A:
        diag_ab[reg] = {vid: concordancia(recortar(series["A|" + reg]["serie"], ini, fin),
                                          recortar(series["B|" + reg]["serie"], ini, fin))
                        for vid, _, ini, fin in VENTANAS}
        diag_ab[reg]["historia_completa"] = concordancia(series["A|" + reg]["serie"], series["B|" + reg]["serie"])

    # --- diagnostico A/B vs C en meses comunes
    diag_c = {}
    for reg, col, nota in PARES_C:
        d = {"nota": nota}
        for vid, _, ini, fin in VENTANAS:
            d[vid] = {
                "A_vs_C": concordancia(recortar(series["A|" + reg]["serie"], ini, fin),
                                       recortar(series["C|" + col]["serie"], ini, fin)),
                "B_vs_C": concordancia(recortar(series["B|" + reg]["serie"], ini, fin),
                                       recortar(series["C|" + col]["serie"], ini, fin)),
            }
        diag_c["%s~%s" % (reg, col)] = d

    # --- sensibilidad del fin de ventana (Emerging, A y B)
    sens = {}
    for fuente in ("A", "B"):
        s = series[fuente + "|Emerging"]["serie"]
        for ini in (200001, 201001):
            for fin in (202512, 202607, 202608):
                r = estadisticos(s, ini, fin)
                sens["%s|%s..%s" % (fuente, ym_txt(ini), ym_txt(fin))] = {
                    "n": r["n"],
                    "media_x12_pct": r["media_x12_pct_no_es_CAGR"],
                    "compuesto_pct": r["compuesto_anual_pct_serie_largo_corto_no_es_rendimiento_de_cuenta"],
                    "t_nw": r["t_nw"], "veredicto": r["veredicto"],
                }

    # --- evaluacion de afirmaciones
    af = {"emergentes": {}, "japon_norteamerica": {}}
    for fuente in ("A", "B"):
        for vid, objetivo in AFIRMACION_EMERGENTES.items():
            r = resultados[fuente + "|Emerging"]["ventanas"][vid]
            mx = r["media_x12_pct_no_es_CAGR"]
            cp = r["compuesto_anual_pct_serie_largo_corto_no_es_rendimiento_de_cuenta"]
            af["emergentes"]["%s|%s" % (fuente, vid)] = {
                "afirmado_pct": objetivo,
                "media_x12_pct": mx,
                "compuesto_pct": cp,
                "coincide_media_x12": abs(mx - objetivo) <= TOL_PP,
                "coincide_compuesto": cp is not None and abs(cp - objetivo) <= TOL_PP,
                "veredicto_nw": r["veredicto"],
                "t_nw": r["t_nw"],
            }
    af["emergentes"]["C"] = "AQR BAB/UMD no publica serie de emergentes: la fuente C no puede evaluar esta afirmacion."
    casos = {
        "Japon": [("A", "A|Japan"), ("B", "B|Japan"), ("C", "C|JPN")],
        "Norteamerica": [("A", "A|North_America"), ("B", "B|North_America"), ("C", "C|North America"),
                         ("C-complemento USA", "C|USA"), ("C-complemento CAN", "C|CAN")],
    }
    for region, lista in casos.items():
        for etiqueta, clave in lista:
            v = {vid: resultados[clave]["ventanas"][vid]["veredicto"] for vid, _, _, _ in VENTANAS}
            af["japon_norteamerica"]["%s|%s" % (region, etiqueta)] = {
                "serie": clave,
                "veredictos": v,
                "t_nw": {vid: resultados[clave]["ventanas"][vid]["t_nw"] for vid, _, _, _ in VENTANAS},
                "inconcluso_en_V1_y_V2": v["V1"] == "inconcluso" and v["V2"] == "inconcluso",
            }

    salida = {
        "id": "AC-03-momentum-internacional",
        "especificacion": {
            "unidades": "% mensual, USD",
            "nw": "Bartlett, %d rezagos, correccion n/(n-1)" % LAGS_NW,
            "ic": "media +/- 1.96*EE_NW",
            "veredicto": "apoyo si IC95 NW inferior > 0; contraria si superior < 0; si no inconcluso",
            "ventanas": {vid: [etq, ini, fin] for vid, etq, ini, fin in VENTANAS},
            "media_x12": "aritmetica x12; NO es CAGR",
            "compuesto": "(prod(1+r))^(12/n)-1; compuesto de la serie largo-corto; NO es el rendimiento de una cuenta",
            "tolerancia_afirmacion_pp": TOL_PP,
        },
        "archivos": archivos,
        "series": {k: v for k, v in resultados.items()},
        "diagnostico_A_vs_B": diag_ab,
        "diagnostico_vs_C": diag_c,
        "sensibilidad_emergentes_fin_de_ventana": sens,
        "afirmaciones": af,
    }
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(redondear(salida), f, ensure_ascii=False, indent=1)

    # ---------------------------------------------------------- impresion
    print("Archivos verificados (SHA256 OK):", len(sumas))
    for nom, a in sorted(archivos.items()):
        print("  %-58s %s" % (nom, a.get("version_cabecera", "")[:70]))
    print()
    hdr = "%-26s %-3s %-17s %4s %7s %6s %6s %6s %17s %7s %7s %16s %16s %s"
    print(hdr % ("serie", "V", "periodo", "n", "med%m", "sd", "tIID", "tNW", "IC95NW", "x12%", "comp%",
                 "peor", "mejor", "veredicto"))
    for clave in sorted(resultados, key=lambda k: (k.split("|")[0], k)):
        r = resultados[clave]
        for vid, _, _, _ in VENTANAS:
            w = r["ventanas"][vid]
            if "media_mensual_pct" not in w:
                print("%-26s %-3s n=%d %s" % (clave, vid, w["n"], w.get("nota", "")))
                continue
            comp = w["compuesto_anual_pct_serie_largo_corto_no_es_rendimiento_de_cuenta"]
            print("%-26s %-3s %-17s %4d %7.3f %6.2f %6.2f %6.2f [%6.3f,%6.3f] %7.2f %7s %16s %16s %s" % (
                clave, vid, w["desde"] + ".." + w["hasta"], w["n"], w["media_mensual_pct"], w["desv_est_pct"],
                w["t_iid"], w["t_nw"], w["ic95_nw_pct"][0], w["ic95_nw_pct"][1],
                w["media_x12_pct_no_es_CAGR"], "%.2f" % comp if comp is not None else "n/d",
                "%.2f(%s)" % (w["peor_mes"]["pct"], w["peor_mes"]["fecha"]),
                "%.2f(%s)" % (w["mejor_mes"]["pct"], w["mejor_mes"]["fecha"]), w["veredicto"]))
    print()
    print("Diagnostico A vs B (historia completa):")
    for reg in REGIONES_A:
        d = diag_ab[reg]["historia_completa"]
        print("  %-22s n=%d corr=%.5f media_dif=%.4f max|dif|=%.3f x12 A=%.3f B=%.3f" % (
            reg, d["n_comun"], d["correlacion"], d["media_dif_mensual_pct"], d["max_abs_dif_pct"],
            d["media_x12_1_pct"], d["media_x12_2_pct"]))
    print()
    print("Diagnostico A/B vs C (meses comunes):")
    for par, d in diag_c.items():
        for vid, _, _, _ in VENTANAS:
            for k in ("A_vs_C", "B_vs_C"):
                c = d[vid][k]
                if "correlacion" not in c:
                    continue
                print("  %-36s %s %s %s..%s n=%d corr=%.3f x12(French)=%.2f x12(AQR)=%.2f media_dif=%.3f max|dif|=%.2f" % (
                    par, vid, k, c["desde"], c["hasta"], c["n_comun"], c["correlacion"],
                    c["media_x12_1_pct"], c["media_x12_2_pct"], c["media_dif_mensual_pct"], c["max_abs_dif_pct"]))
    print()
    print("Sensibilidad emergentes (fin de ventana):")
    for k, v in sens.items():
        print("  %-24s n=%d x12=%.2f comp=%.2f tNW=%.2f %s" % (k, v["n"], v["media_x12_pct"], v["compuesto_pct"],
                                                             v["t_nw"], v["veredicto"]))
    print()
    print("Afirmaciones:")
    for k, v in af["emergentes"].items():
        print("  Emergentes", k, v if isinstance(v, str) else redondear(v, 3))
    for k, v in af["japon_norteamerica"].items():
        print("  ", k, redondear(v, 3))


if __name__ == "__main__":
    main()
