#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V02. Doble ejecucion independiente (auditor de replicas, 2026-09-25).

Reimplementacion desde cero de V02 usando SOLO:
  - el pre-registro (seccion PRE-REGISTRO del README / preregistro.md), y
  - los datos congelados en datos/ (sin red).
No importa ni lee reproducir.py. resultados.json y variantes.csv (salidas del original)
solo se leen AL FINAL, en cotejo_con_original() y cotejo_variantes_csv(), despues de
calcular todo; no entran en ningun calculo.

Todo es propio: lector de CSV de French (por bloques), lector del JSON de Yahoo,
alineacion por indice de mes, fin de mes del tipo de cambio, conversion a MXN,
costos de GBM y estadistica. El error estandar Newey-West(6) se calcula con DOS
formulas propias (suma doble de Bartlett sobre pares (i, j) y autocovarianzas
ponderadas) y, solo como tercera comprobacion, con herramientas/estadistica.py.

Despues compara cada cifra que el README de V02 reporta (texto corregido el
2026-09-25; el texto anterior se conserva en afirmaciones_anteriores()) con la cifra propia
(tolerancias de la tarea: 0.01 pp en medias mensuales, 0.05 en t, 0.1 pp en
CAGR / caida maxima / medias x12; en cifras redondeadas a menos decimales se
usa media unidad del ultimo decimal publicado).

Uso: python3 laboratorio/replicas/V02-momentum-internacional/independiente.py
Salida: independiente_resultados.json (junto a este archivo) y la tabla de
comparacion en la terminal.
"""
import datetime as dt
import hashlib
import json
import math
import os
import re
import sys
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
Z95 = 1.959963984540054
L_NW = 6

# ---------------------------------------------------------------------------
# Meses como enteros: indice = anio*12 + (mes-1)
# ---------------------------------------------------------------------------

def mes_de_yyyymm(v):
    v = int(v)
    return (v // 100) * 12 + (v % 100 - 1)


def mes_de_fecha(f):
    return f.year * 12 + f.month - 1


def etiqueta(m):
    return "%04d-%02d" % (m // 12, m % 12 + 1)


# ---------------------------------------------------------------------------
# Lector propio de los CSV de French (formato por bloques con titulo y encabezado)
# ---------------------------------------------------------------------------

def leer_french(nombre):
    ruta = os.path.join(DATOS, nombre)
    with zipfile.ZipFile(ruta) as z:
        internos = [n for n in z.namelist() if n.lower().endswith(".csv")]
        assert len(internos) == 1, internos
        texto = z.read(internos[0]).decode("latin-1")
    lineas = texto.splitlines()
    preambulo = lineas[0].strip()
    bloques = []
    titulo = ""
    i = 0
    while i < len(lineas):
        s = lineas[i].strip()
        if s.startswith(","):
            cols = [c.strip() for c in s.split(",")[1:]]
            filas = {}
            j = i + 1
            while j < len(lineas):
                partes = [p.strip() for p in lineas[j].split(",")]
                if not partes[0].isdigit():
                    break
                filas[partes[0]] = [float(p) for p in partes[1:]]
                j += 1
            bloques.append({"titulo": titulo, "cols": cols, "filas": filas})
            titulo = ""
            i = j
            continue
        if s:
            titulo = s
        i += 1
    return preambulo, bloques


def serie_mensual(bloque, columna):
    """dict mes->valor (en %), excluyendo faltantes; devuelve tambien # faltantes."""
    k = bloque["cols"].index(columna)
    out, falt = {}, 0
    for clave, vals in bloque["filas"].items():
        if len(clave) != 6:
            continue
        v = vals[k]
        if v <= -99.99 + 1e-9 or v == -999:
            falt += 1
            continue
        out[mes_de_yyyymm(clave)] = v
    return out, falt


def bloque_mensual(bloques, contiene=None):
    for b in bloques:
        claves = list(b["filas"].keys())
        if not claves or len(claves[0]) != 6:
            continue
        if contiene is None or contiene.lower() in b["titulo"].lower():
            return b
    raise KeyError(contiene)


# ---------------------------------------------------------------------------
# Estadistica propia
# ---------------------------------------------------------------------------

def media(x):
    return sum(x) / len(x)


def desv(x):
    m = media(x)
    return math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1))


def se_nw_suma_doble(x, L=L_NW):
    """Var(media) = (1/n^2) * sum_i sum_j w(|i-j|) u_i u_j, w = 1-|i-j|/(L+1); x n/(n-1)."""
    n = len(x)
    m = media(x)
    u = [v - m for v in x]
    s = 0.0
    for i in range(n):
        ui = u[i]
        for j in range(max(0, i - L), min(n, i + L + 1)):
            s += (1.0 - abs(i - j) / (L + 1.0)) * ui * u[j]
    var = s / (n * n) * n / (n - 1)
    return math.sqrt(var)


def se_nw_autocov(x, L=L_NW):
    """Varianza de largo plazo = g0 + 2 sum_j (1 - j/(L+1)) g_j; Var(media) = VLP/(n-1)."""
    n = len(x)
    m = media(x)
    u = [v - m for v in x]
    def g(j):
        return sum(u[t] * u[t - j] for t in range(j, n)) / n
    vlp = g(0) + 2.0 * sum((1.0 - j / (L + 1.0)) * g(j) for j in range(1, L + 1))
    return math.sqrt(vlp / (n - 1))


def se_nw_herramienta(x, L=L_NW):
    sys.path.insert(0, os.path.join(RAIZ, "herramientas"))
    try:
        import estadistica  # noqa: E402
        return estadistica.newey_west(x, rezagos=L)["se"]
    except Exception:
        return None


def veredicto(inf, sup):
    if inf > 0:
        return "apoyo"
    if sup < 0:
        return "contraria"
    return "inconcluso"


def compuesto_anual(x_pct):
    p = 1.0
    for v in x_pct:
        p *= 1 + v / 100.0
    return (p ** (12.0 / len(x_pct)) - 1) * 100.0


def resumen(pares, con_herr=False):
    """pares = lista ordenada de (mes, valor %)."""
    x = [v for _, v in pares]
    n = len(x)
    m = media(x)
    d = desv(x)
    se1 = se_nw_suma_doble(x)
    se2 = se_nw_autocov(x)
    assert abs(se1 - se2) < 1e-10 * max(1.0, se1), (se1, se2)
    r = {
        "desde": etiqueta(pares[0][0]), "hasta": etiqueta(pares[-1][0]), "n": n,
        "media": m, "de": d, "t_iid": m / (d / math.sqrt(n)),
        "se_nw": se1, "t_nw": m / se1,
        "ic_inf": m - Z95 * se1, "ic_sup": m + Z95 * se1,
        "x12": 12 * m, "cagr": compuesto_anual(x),
    }
    r["veredicto"] = veredicto(r["ic_inf"], r["ic_sup"])
    peor = min(pares, key=lambda p: p[1])
    mejor = max(pares, key=lambda p: p[1])
    r["peor"] = (peor[1], etiqueta(peor[0]))
    r["mejor"] = (mejor[1], etiqueta(mejor[0]))
    if con_herr:
        r["se_nw_herramienta"] = se_nw_herramienta(x)
    return r


def recortar(serie, desde=None, hasta=None):
    ms = sorted(serie)
    a = ms[0] if desde is None else mes_de_yyyymm(desde)
    b = ms[-1] if hasta is None else mes_de_yyyymm(hasta)
    pares = [(m, serie[m]) for m in ms if a <= m <= b]
    # sin huecos
    for k in range(1, len(pares)):
        assert pares[k][0] == pares[k - 1][0] + 1, "hueco en la serie"
    return pares


def ols(y, x):
    my, mx = media(y), media(x)
    sxx = sum((a - mx) ** 2 for a in x)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    syy = sum((b - my) ** 2 for b in y)
    beta = sxy / sxx
    corr = sxy / math.sqrt(sxx * syy)
    return beta, corr


def asimetria(x):
    n = len(x)
    m = media(x)
    m2 = sum((v - m) ** 2 for v in x) / n
    m3 = sum((v - m) ** 3 for v in x) / n
    g1 = m3 / m2 ** 1.5
    G1 = g1 * math.sqrt(n * (n - 1)) / (n - 2)
    return g1, G1


def caida_maxima(pares_pct):
    """Indice compuesto que parte de 1.0 al cierre del mes previo al primero."""
    nivel = 1.0
    pico, f_pico = 1.0, etiqueta(pares_pct[0][0] - 1)
    peor, fp, fv = 0.0, None, None
    for m, v in pares_pct:
        nivel *= 1 + v / 100.0
        if nivel > pico:
            pico, f_pico = nivel, etiqueta(m)
        dd = nivel / pico - 1
        if dd < peor:
            peor, fp, fv = dd, f_pico, etiqueta(m)
    return peor * 100, fp, fv


def peor_12m(pares_pct):
    peor, fin = None, None
    for k in range(11, len(pares_pct)):
        p = 1.0
        for _, v in pares_pct[k - 11:k + 1]:
            p *= 1 + v / 100.0
        r = (p - 1) * 100
        if peor is None or r < peor:
            peor, fin = r, etiqueta(pares_pct[k][0])
    return peor, fin


# ---------------------------------------------------------------------------
# Datos de French por region
# ---------------------------------------------------------------------------

REGIONES = {
    "Developed": ("Developed_Mom_Factor_CSV.zip", "Developed_5_Factors_CSV.zip", "Developed_6_Portfolios_ME_Prior_12_2_CSV.zip"),
    "Developed_ex_US": ("Developed_ex_US_Mom_Factor_CSV.zip", "Developed_ex_US_5_Factors_CSV.zip", "Developed_ex_US_6_Portfolios_ME_Prior_12_2_CSV.zip"),
    "Europe": ("Europe_Mom_Factor_CSV.zip", "Europe_5_Factors_CSV.zip", "Europe_6_Portfolios_ME_Prior_12_2_CSV.zip"),
    "Japan": ("Japan_Mom_Factor_CSV.zip", "Japan_5_Factors_CSV.zip", "Japan_6_Portfolios_ME_Prior_12_2_CSV.zip"),
    "Asia_Pacific_ex_Japan": ("Asia_Pacific_ex_Japan_MOM_Factor_CSV.zip", "Asia_Pacific_ex_Japan_5_Factors_CSV.zip", "Asia_Pacific_ex_Japan_6_Portfolios_ME_Prior_12_2_CSV.zip"),
    "North_America": ("North_America_Mom_Factor_CSV.zip", "North_America_5_Factors_CSV.zip", "North_America_6_Portfolios_ME_Prior_12_2_CSV.zip"),
    "Emerging": ("Emerging_MOM_Factor_CSV.zip", "Emerging_5_Factors_CSV.zip", "Emerging_Markets_6_Portfolios_ME_Prior_12_2_CSV.zip"),
}

VENTANAS = [
    ("W0", None, None), ("W1", 200001, 202512), ("W1b", 200001, None),
    ("W2", 201001, 202512), ("W2b", 201001, None),
    ("R98-pre", None, 199802), ("R98-post", 199803, None),
    ("R99-pre", None, 199908), ("R99-post", 199909, None),
    ("FF12-in", 199011, 201103), ("FF12-out", 201104, None),
    ("AMP13-pre", None, 201306), ("AMP13-post", 201307, None),
    ("AMP09-post", 200904, None),
]


def cargar_french():
    out = {}
    for reg, (f_mom, f_5, f_6) in REGIONES.items():
        pre_m, bl_m = leer_french(f_mom)
        b = bloque_mensual(bl_m)
        assert b["cols"] == ["WML"], b["cols"]
        wml, falt_w = serie_mensual(b, "WML")
        pre_5, bl_5 = leer_french(f_5)
        b5 = bloque_mensual(bl_5)
        mkt, falt_mkt = serie_mensual(b5, "Mkt-RF")
        rf, falt_rf = serie_mensual(b5, "RF")
        falt_otras = {c: serie_mensual(b5, c)[1] for c in b5["cols"]}
        pre_6, bl_6 = leer_french(f_6)
        b6 = bloque_mensual(bl_6, "Value Weighted Returns -- Monthly")
        port = {c: serie_mensual(b6, c)[0] for c in b6["cols"]}
        falt6 = sum(serie_mensual(b6, c)[1] for c in b6["cols"])
        out[reg] = {
            "wml": wml, "mkt": mkt, "rf": rf, "port": port,
            "falt_wml": falt_w, "falt_mkt": falt_mkt, "falt_rf": falt_rf,
            "falt_5f": falt_otras, "falt_6p": falt6,
            "preambulos": [pre_m, pre_5, pre_6],
        }
    return out


# ---------------------------------------------------------------------------
# Yahoo y FRED (lectores propios)
# ---------------------------------------------------------------------------

def leer_yahoo(nombre):
    with open(os.path.join(DATOS, nombre)) as fh:
        d = json.load(fh)
    res = d.get("chart", {}).get("result")
    if not res:
        return {"existe": False, "error": d.get("chart", {}).get("error")}
    r = res[0]
    meta = r.get("meta", {})
    off = meta.get("gmtoffset", 0) or 0
    ts = r.get("timestamp") or []
    q = (r.get("indicators", {}).get("quote") or [{}])[0]
    aj = (r.get("indicators", {}).get("adjclose") or [{}])[0].get("adjclose") or []
    cierre = q.get("close") or []
    vol = q.get("volume") or []

    def fecha(t):
        return (dt.datetime(1970, 1, 1) + dt.timedelta(seconds=t + off)).date()

    dias = []
    for k, t in enumerate(ts):
        dias.append({
            "f": fecha(t),
            "c": cierre[k] if k < len(cierre) else None,
            "a": aj[k] if k < len(aj) else None,
            "v": vol[k] if k < len(vol) else None,
        })
    divs = {}
    for e in (r.get("events", {}).get("dividends") or {}).values():
        m = mes_de_fecha(fecha(e["date"]))
        divs[m] = divs.get(m, 0.0) + e["amount"]
    splits = [(fecha(e["date"]).isoformat(), e.get("numerator"), e.get("denominator"))
              for e in (r.get("events", {}).get("splits") or {}).values()]
    return {"existe": True, "meta": meta, "dias": dias, "divs": divs, "splits": splits}


def fin_de_mes_yahoo(y, campo):
    """dict mes -> (fecha, valor) con el ultimo dia del mes que tiene valor."""
    out = {}
    for d in y["dias"]:
        v = d[campo]
        if v is None:
            continue
        m = mes_de_fecha(d["f"])
        if m not in out or d["f"] >= out[m][0]:
            out[m] = (d["f"], v)
    return out


def leer_fred(nombre):
    out = []
    with open(os.path.join(DATOS, nombre)) as fh:
        enc = fh.readline()
        for linea in fh:
            partes = linea.strip().split(",")
            if len(partes) < 2:
                continue
            f, v = partes[0], partes[1].strip()
            if v in ("", "."):
                continue
            out.append((dt.date.fromisoformat(f), float(v)))
    return enc.strip(), out


# ---------------------------------------------------------------------------
# ETFs: rendimientos, MXN, costos
# ---------------------------------------------------------------------------

COMISION = 0.0025 * 1.16          # 0.29% por lado (0.25% + IVA)
SPREAD = {"EEM": 0.0005, "EFA": 0.0005, "VEA": 0.0005}
SPREAD_MOM_BASE = 0.0015
SPREAD_MOM_SENS = 0.0030
FIN_ETF = mes_de_yyyymm(202608)
MOMENTUM = ["EEMO", "PIE", "IMTM", "PIZ", "IDMO", "IMOM"]
MERCADO = ["EEM", "EFA", "VEA"]
INICIO_MOM = {"EEMO": 201604, "PIE": 200801, "IMTM": 201502, "PIZ": 200801, "IDMO": 201604, "IMOM": 201601}
PARES = [("EEMO", "EEM"), ("PIE", "EEM"), ("IMTM", "EFA"), ("IMTM", "VEA"), ("PIZ", "EFA"), ("PIZ", "VEA"),
         ("IDMO", "EFA"), ("IDMO", "VEA"), ("IMOM", "EFA"), ("IMOM", "VEA")]
REGION_ETF = {"EEMO": "Emerging", "PIE": "Emerging"}


def rend_mensuales(y, modo):
    """modo 'adj': adjclose; 'imp': (close_t + 0.7 div_mes)/close_{t-1} - 1;
    'cd': (close_t + div_mes)/close_{t-1} - 1. Devuelve dict mes -> rend (fraccion)."""
    campo = "a" if modo == "adj" else "c"
    fm = fin_de_mes_yahoo(y, campo)
    ms = sorted(fm)
    out = {}
    for k in range(1, len(ms)):
        m0, m1 = ms[k - 1], ms[k]
        if m1 != m0 + 1 or m1 > FIN_ETF:
            continue
        p0, p1 = fm[m0][1], fm[m1][1]
        if modo == "adj":
            out[m1] = p1 / p0 - 1
        else:
            fac = 0.7 if modo == "imp" else 1.0
            out[m1] = (p1 + fac * y["divs"].get(m1, 0.0)) / p0 - 1
    return out


def primer_mes_completo(y):
    """Primer mes cuyo rendimiento se puede calcular (requiere cierre del mes previo)."""
    fm = fin_de_mes_yahoo(y, "a")
    return min(fm) + 1


def metricas_mxn(r_usd, fx, meses, costo):
    """Riqueza de 20,000 MXN: compra al inicio (costo sobre el valor) y vende al final."""
    w0 = 20000.0
    w = w0 * (1 - costo)
    camino = [w0, w]
    netos = []
    for k, m in enumerate(meses):
        r_mxn = (1 + r_usd[m]) * fx[m] / fx[m - 1] - 1
        antes = w
        w = w * (1 + r_mxn)
        if k == len(meses) - 1:
            w = w * (1 - costo)
            camino.append(w)
        else:
            camino.append(w)
        netos.append(w / antes - 1 if k else (w / w0 - 1))
    n = len(meses)
    cagr = ((w / w0) ** (12.0 / n) - 1) * 100
    brutos = [(1 + r_usd[m]) * fx[m] / fx[m - 1] - 1 for m in meses]
    vol = desv([v * 100 for v in brutos]) * math.sqrt(12)
    vol_neta = desv([v * 100 for v in netos]) * math.sqrt(12)
    pico, mdd = camino[0], 0.0
    for v in camino:
        pico = max(pico, v)
        mdd = min(mdd, v / pico - 1)
    # variante sin el punto inicial de 20,000 (pico desde el valor ya comprado)
    pico2, mdd2 = camino[1], 0.0
    for v in camino[1:]:
        pico2 = max(pico2, v)
        mdd2 = min(mdd2, v / pico2 - 1)
    return {"n": n, "riqueza": w, "cagr": cagr, "vol": vol, "vol_neta": vol_neta,
            "mdd": mdd * 100, "mdd_sin_inicial": mdd2 * 100}


def cagr_usd_bruto(r_usd, meses):
    p = 1.0
    for m in meses:
        p *= 1 + r_usd[m]
    return (p ** (12.0 / len(meses)) - 1) * 100


# ---------------------------------------------------------------------------
# Corrida
# ---------------------------------------------------------------------------

def correr():
    R = {"datos": {}, "wml": {}, "crash": {}, "pierna_larga": {}, "etf": {}, "controles": {}}
    F = cargar_french()

    # --- datos efectivamente usados
    for reg, d in F.items():
        ms = sorted(d["wml"])
        R["datos"][reg] = {
            "wml_desde": etiqueta(ms[0]), "wml_hasta": etiqueta(ms[-1]), "wml_n": len(ms),
            "wml_faltantes": d["falt_wml"],
            "mkt_desde": etiqueta(min(d["mkt"])), "mkt_hasta": etiqueta(max(d["mkt"])),
            "faltantes_5f": d["falt_5f"], "faltantes_6p": d["falt_6p"],
            "port_desde": etiqueta(min(d["port"]["BIG HiPRIOR"])),
            "preambulos": d["preambulos"],
        }
    huellas = {}
    for nombre in sorted(os.listdir(DATOS)):
        with open(os.path.join(DATOS, nombre), "rb") as fh:
            huellas[nombre] = hashlib.sha256(fh.read()).hexdigest()
    R["datos"]["huellas"] = huellas
    sums = {}
    with open(os.path.join(AQUI, "SHA256SUMS.txt")) as fh:
        for linea in fh:
            partes = linea.split()
            if len(partes) == 2 and partes[1].startswith("datos/"):
                sums[partes[1][6:]] = partes[0]
    R["datos"]["huellas_coinciden_con_SHA256SUMS"] = all(huellas.get(k) == v for k, v in sums.items())
    R["datos"]["archivos_en_SHA256SUMS"] = len(sums)

    # --- WML por region y ventana
    max_dif_herr = 0.0
    for reg, d in F.items():
        R["wml"][reg] = {}
        for clave, a, b in VENTANAS:
            if clave.startswith("R99") and reg != "Emerging":
                continue
            pares = recortar(d["wml"], a, b)
            if len(pares) < 24:
                R["wml"][reg][clave] = {"n": len(pares), "nota": "menos de 24 meses"}
                continue
            r = resumen(pares, con_herr=True)
            if r.get("se_nw_herramienta") is not None:
                max_dif_herr = max(max_dif_herr, abs(r["se_nw_herramienta"] - r["se_nw"]))
            R["wml"][reg][clave] = r
    R["controles"]["max_dif_se_nw_propio_vs_herramienta"] = max_dif_herr

    # Fuente B de AC-03 (reconstruccion 2x3) y ventanas V1-V3 de AC-03, para cotejar las tablas pegadas
    R["ac03"] = {}
    for reg, d in F.items():
        p = d["port"]
        comunes = sorted(set(p["SMALL HiPRIOR"]) & set(p["BIG HiPRIOR"]) & set(p["SMALL LoPRIOR"]) & set(p["BIG LoPRIOR"]))
        wml_b = {m: 0.5 * (p["SMALL HiPRIOR"][m] + p["BIG HiPRIOR"][m]) - 0.5 * (p["SMALL LoPRIOR"][m] + p["BIG LoPRIOR"][m]) for m in comunes}
        for fuente, serie in (("A", d["wml"]), ("B", wml_b)):
            for v, a, b in (("V1", 200001, None), ("V2", 201001, None), ("V3", 201601, 202512)):
                R["ac03"]["%s:%s:%s" % (fuente, reg, v)] = resumen(recortar(serie, a, b))

    # --- crash y relacion con el mercado (W0)
    for reg, d in F.items():
        w0 = recortar(d["wml"])
        x = [v for _, v in w0]
        peores = sorted(w0, key=lambda p: p[1])[:5]
        g1, G1 = asimetria(x)
        mdd, fp, fv = caida_maxima(w0)
        p12, f12 = peor_12m(w0)
        c = {"peores5": [(etiqueta(m), v, d["mkt"].get(m)) for m, v in peores],
             "mdd": mdd, "mdd_pico": fp, "mdd_valle": fv, "peor12m": p12, "peor12m_fin": f12,
             "asimetria_g1": g1, "asimetria_G1": G1, "desv_mensual": desv(x)}
        for clave, a, b in (("W0", None, None), ("W1", 200001, 202512)):
            pares = [(m, v) for m, v in recortar(d["wml"], a, b) if m in d["mkt"]]
            beta, corr = ols([v for _, v in pares], [d["mkt"][m] for m, _ in pares])
            c["beta_" + clave], c["corr_" + clave] = beta, corr
            c["n_" + clave] = len(pares)
        # estados de Daniel y Moskowitz (Mkt-RF compuesto t-24..t-1)
        estado = {}
        for m in sorted(d["wml"]):
            prev = [m - k for k in range(1, 25)]
            if not all(p in d["mkt"] for p in prev):
                continue
            acum = 1.0
            for p_ in prev:
                acum *= 1 + d["mkt"][p_] / 100.0
            estado[m] = "bajista" if acum - 1 < 0 else "normal"
        c["meses_sin_estado"] = sum(1 for m in d["wml"] if m not in estado)
        for e in ("bajista", "normal"):
            ms = [m for m in sorted(d["wml"]) if estado.get(m) == e]
            beta, corr_e = ols([d["wml"][m] for m in ms], [d["mkt"][m] for m in ms])
            c["beta_" + e] = beta
            c["corr_" + e] = corr_e
            c["media_" + e] = media([d["wml"][m] for m in ms])
            c["n_" + e] = len(ms)
        R["crash"][reg] = c

    # --- pierna larga academica: Big High - (Mkt-RF + RF)
    for reg, d in F.items():
        bh = d["port"]["BIG HiPRIOR"]
        exc = {m: bh[m] - (d["mkt"][m] + d["rf"][m]) for m in bh if m in d["mkt"] and m in d["rf"]}
        R["pierna_larga"][reg] = {}
        for clave, a, b in (("W0", None, None), ("W1", 200001, 202512), ("W2", 201001, 202512),
                            ("AMP13-post", 201307, None), ("ETF-2016-04", 201604, None)):
            R["pierna_larga"][reg][clave] = resumen(recortar(exc, a, b))

    # WML emergente, meses de 2026 (descriptivo del README) y ventana de ETFs
    em = F["Emerging"]["wml"]
    R["wml_em_2026"] = {etiqueta(m): em[m] for m in sorted(em) if m >= mes_de_yyyymm(202601)}
    R["wml_etf_ventana"] = {reg: resumen(recortar(F[reg]["wml"], 201604, None)) for reg in ("Emerging", "Developed_ex_US")}

    # --- ETFs
    Y = {}
    for t in MOMENTUM + MERCADO:
        Y[t] = leer_yahoo("yahoo_%s_1d.json" % t)
    ydat = {}
    for t, y in Y.items():
        dias_sin = [d_["f"].isoformat() for d_ in y["dias"] if d_["a"] is None]
        ydat[t] = {"primer_dia": y["dias"][0]["f"].isoformat(), "ultimo_dia": y["dias"][-1]["f"].isoformat(),
                   "dias_sin_precio": dias_sin, "splits": y["splits"],
                   "primer_mes_completo": etiqueta(primer_mes_completo(y)),
                   "nombre": y["meta"].get("longName")}
    R["datos"]["yahoo"] = ydat

    # control: cierre + dividendos contra adjclose
    difs = []
    por_ticker = {}
    for t, y in Y.items():
        ra = rend_mensuales(y, "adj")
        rc = rend_mensuales(y, "cd")
        ds = [((rc[m] - ra[m]) * 100, m) for m in ra if m in rc]
        difs += ds
        mx = max(ds, key=lambda z: abs(z[0]))
        por_ticker[t] = {"media": media([z[0] for z in ds]), "media_abs": media([abs(z[0]) for z in ds]),
                         "max_abs": abs(mx[0]), "mes_max": etiqueta(mx[1])}
    R["controles"]["cierre_div_vs_adj"] = {
        "media_pp": media([z[0] for z in difs]), "media_abs_pp": media([abs(z[0]) for z in difs]),
        "max_abs_pp": max(abs(z[0]) for z in difs), "por_ticker": por_ticker}

    # tipo de cambio
    enc, fx_d = leer_fred("fred_DEXMXUS.csv")
    fx = {}
    for f, v in fx_d:
        m = mes_de_fecha(f)
        if m not in fx or f >= fx[m][0]:
            fx[m] = (f, v)
    fxm = {m: v for m, (f, v) in fx.items()}
    R["datos"]["dexmxus"] = {"desde": fx_d[0][0].isoformat(), "hasta": fx_d[-1][0].isoformat(),
                             "2008-01": fxm[mes_de_yyyymm(200801)], "2016-03": fxm[mes_de_yyyymm(201603)],
                             "2026-08": fxm[mes_de_yyyymm(202608)]}
    yx = leer_yahoo("yahoo_MXN_X_1d.json")
    fy = {m: v for m, (f, v) in fin_de_mes_yahoo(yx, "c").items()}
    comunes = [m for m in sorted(fxm) if m - 1 in fxm and m in fy and m - 1 in fy and m <= FIN_ETF]
    a_ = [(fxm[m] / fxm[m - 1] - 1) * 100 for m in comunes]
    b_ = [(fy[m] / fy[m - 1] - 1) * 100 for m in comunes]
    _, corr = ols(a_, b_)
    R["controles"]["fx_fred_vs_yahoo"] = {"desde": etiqueta(comunes[0]), "hasta": etiqueta(comunes[-1]), "n": len(comunes),
                                          "corr": corr, "media_abs_dif_pp": media([abs(p - q) for p, q in zip(a_, b_)])}

    rend = {t: {"adj": rend_mensuales(Y[t], "adj"), "imp": rend_mensuales(Y[t], "imp")} for t in Y}
    for mom, mer in PARES:
        region = REGION_ETF.get(mom, "Developed_ex_US")
        ini_hist = max(mes_de_yyyymm(INICIO_MOM[mom]), primer_mes_completo(Y[mom]), primer_mes_completo(Y[mer]))
        for ventana, ini in (("historia", ini_hist), ("comun", mes_de_yyyymm(201604))):
            meses = list(range(ini, FIN_ETF + 1))
            for modo in ("adj", "imp"):
                rm, rc = rend[mom][modo], rend[mer][modo]
                assert all(m in rm and m in rc and m in fxm and m - 1 in fxm for m in meses), (mom, mer, ventana)
                dif = [(m, (rm[m] - rc[m]) * 100) for m in meses]
                s = resumen(dif)
                wml = F[region]["wml"]
                beta_wml, corr_wml = ols([v for _, v in dif], [wml[m] for m, _ in dif])
                spreads = (("base", SPREAD_MOM_BASE), ("spread030", SPREAD_MOM_SENS)) if modo == "adj" else (("base", SPREAD_MOM_BASE),)
                for nombre_s, sp in spreads:
                    mm = metricas_mxn(rm, fxm, meses, COMISION + sp)
                    mc = metricas_mxn(rc, fxm, meses, COMISION + SPREAD[mer])
                    clave = "%s-%s|%s|%s|%s" % (mom, mer, ventana, "impuestos" if modo == "imp" else "sin_imp", nombre_s)
                    R["etf"][clave] = {
                        "desde": etiqueta(meses[0]), "hasta": etiqueta(meses[-1]), "n": len(meses),
                        "mom": mm, "mer": mc, "dif_cagr_mxn_neto": mm["cagr"] - mc["cagr"],
                        "dif_usd": s, "beta_dif_vs_wml": beta_wml, "corr_dif_vs_wml": corr_wml, "region_wml": region,
                        "cagr_usd_bruto_mom": cagr_usd_bruto(rm, meses), "cagr_usd_bruto_mer": cagr_usd_bruto(rc, meses),
                    }

    # SIC (JSON congelados de Yahoo .MX)
    sic = {}
    for t in MOMENTUM + MERCADO:
        y = leer_yahoo("yahoo_%s.MX_1d.json" % t)
        if not y["existe"]:
            sic[t] = {"existe": False, "error": (y["error"] or {}).get("code")}
            continue
        d26 = [d_ for d_ in y["dias"] if d_["f"].year == 2026 and d_["c"] is not None]
        sic[t] = {"existe": True, "bolsa": y["meta"].get("exchangeName"), "moneda": y["meta"].get("currency"),
                  "dias_2026_con_precio": len(d26), "dias_2026_con_volumen": sum(1 for d_ in d26 if (d_["v"] or 0) > 0)}
    R["sic"] = sic
    return R


# ---------------------------------------------------------------------------
# Comparacion con el README de V02
# ---------------------------------------------------------------------------

def tol_redondeo(txt):
    """Media unidad del ultimo decimal publicado."""
    s = txt.replace("−", "-").replace("+", "").strip()
    dec = len(s.split(".")[1]) if "." in s else 0
    return 0.5 * 10 ** (-dec)


def construir_comparacion(R):
    W = R["wml"]
    C = R["crash"]
    P = R["pierna_larga"]
    E = R["etf"]
    filas = []

    def num(seccion, desc, readme_txt, propio, tipo):
        """tipo: 'media' (0.01 pp), 't' (0.05), 'anual' (0.1 pp), 'red' (redondeo), u otro float."""
        readme = float(readme_txt.replace("−", "-").replace("+", ""))
        if tipo == "media":
            tol = max(0.01, tol_redondeo(readme_txt))
        elif tipo == "t":
            tol = max(0.05, tol_redondeo(readme_txt))
        elif tipo == "anual":
            tol = max(0.1, tol_redondeo(readme_txt))
        else:
            tol = max(1e-9, tol_redondeo(readme_txt))
        ok = abs(propio - readme) <= tol + 1e-9
        filas.append({"seccion": seccion, "cifra": desc, "readme": readme_txt, "propio": propio,
                      "dif": propio - readme, "tol": tol, "coincide": ok})

    def cat(seccion, desc, readme, propio):
        filas.append({"seccion": seccion, "cifra": desc, "readme": str(readme), "propio": str(propio),
                      "dif": None, "tol": "igual", "coincide": str(readme) == str(propio)})

    def rango(seccion, desc, lo_txt, hi_txt, valores, tipo):
        lo, hi = min(valores), max(valores)
        # el README escribe rangos "de A a B" en cualquier orden
        a = float(lo_txt.replace("−", "-").replace("+", ""))
        b = float(hi_txt.replace("−", "-").replace("+", ""))
        if a > b:
            lo_txt, hi_txt = hi_txt, lo_txt
        num(seccion, desc + " (minimo)", lo_txt, lo, tipo)
        num(seccion, desc + " (maximo)", hi_txt, hi, tipo)

    # --- Datos efectivamente usados
    s = "Datos"
    des = [r for r in REGIONES if r != "Emerging"]
    cat(s, "WML desarrollados: rango", "1990-11 a 2026-08", " / ".join(sorted({R["datos"][r]["wml_desde"] + " a " + R["datos"][r]["wml_hasta"] for r in des})))
    num(s, "WML desarrollados: meses", "430", float(max(R["datos"][r]["wml_n"] for r in des)), "red")
    cat(s, "WML desarrollados: todos con 430 meses", True, all(R["datos"][r]["wml_n"] == 430 for r in des))
    cat(s, "WML Emerging: rango", "1990-01 a 2026-08", R["datos"]["Emerging"]["wml_desde"] + " a " + R["datos"]["Emerging"]["wml_hasta"])
    num(s, "WML Emerging: meses", "440", float(R["datos"]["Emerging"]["wml_n"]), "red")
    num(s, "WML: faltantes (7 regiones)", "0", float(sum(R["datos"][r]["wml_faltantes"] for r in REGIONES)), "red")
    cat(s, "Mkt-RF 5F desarrollados: inicio", "1990-07", " / ".join(sorted({R["datos"][r]["mkt_desde"] for r in des})))
    cat(s, "Mkt-RF 5F Emerging: inicio", "1989-07", R["datos"]["Emerging"]["mkt_desde"])
    fe = R["datos"]["Emerging"]["faltantes_5f"]
    cat(s, "Emerging 5F: faltantes solo en RMW y CMA", True, fe["Mkt-RF"] == 0 and fe["RF"] == 0 and fe["SMB"] == 0 and fe["HML"] == 0 and fe["RMW"] > 0 and fe["CMA"] > 0)
    cat(s, "Preambulos: todos '202608 Bloomberg'", True, all("202608 Bloomberg" in p for r in REGIONES for p in R["datos"][r]["preambulos"]))
    cat(s, "Huella Emerging_MOM (prefijo)", "5316f98a", R["datos"]["huellas"]["Emerging_MOM_Factor_CSV.zip"][:8])
    cat(s, "Huella Developed_ex_US_Mom (prefijo)", "0b0941b3", R["datos"]["huellas"]["Developed_ex_US_Mom_Factor_CSV.zip"][:8])
    for t, f in (("EEMO", "2012-02-24"), ("PIE", "2008-01-07"), ("IMTM", "2015-01-27"), ("PIZ", "2008-01-07"),
                 ("IDMO", "2012-02-24"), ("IMOM", "2015-12-23"), ("EEM", "2003-04-14"), ("EFA", "2001-08-27"), ("VEA", "2007-07-26")):
        cat(s, "Yahoo %s: primer dia" % t, f, R["datos"]["yahoo"][t]["primer_dia"])
    cat(s, "Yahoo: un dia sin precio en cada ETF (2026-09-22)", True,
        all(R["datos"]["yahoo"][t]["dias_sin_precio"] == ["2026-09-22"] for t in MOMENTUM + MERCADO))
    fxd = R["datos"]["dexmxus"]
    cat(s, "DEXMXUS: rango", "1993-11-08 a 2026-09-18", fxd["desde"] + " a " + fxd["hasta"])
    num(s, "DEXMXUS fin de mes 2008-01", "10.8190", fxd["2008-01"], "red")
    num(s, "DEXMXUS fin de mes 2016-03", "17.2140", fxd["2016-03"], "red")
    num(s, "DEXMXUS fin de mes 2026-08", "17.0081", fxd["2026-08"], "red")
    cd = R["controles"]["cierre_div_vs_adj"]
    cat(s, "Cierre+div vs adjclose: diferencia media < 0.01 pp/mes", True, abs(cd["media_pp"]) < 0.01)
    num(s, "Cierre+div vs adjclose: diferencia maxima (pp)", "0.29", cd["max_abs_pp"], "red")
    eem_split = R["datos"]["yahoo"]["EEM"]["splits"]
    cat(s, "EEM: split 3:1 en 2008 presente y sin salto", True,
        any(sp[0].startswith("2008") and sp[1] == 3 and sp[2] == 1 for sp in eem_split) and cd["por_ticker"]["EEM"]["max_abs"] < 0.3)
    fxc = R["controles"]["fx_fred_vs_yahoo"]
    with open(os.path.join(AQUI, "preregistro.md"), "rb") as fh:
        h_pre = hashlib.sha256(fh.read()).hexdigest()
    cat(s, "Huella de preregistro.md (prefijo)", "2a9aa15f", h_pre[:8])
    with open(os.path.join(AQUI, "preregistro.md"), encoding="utf-8") as fh:
        t_pre = fh.read()
    with open(os.path.join(AQUI, "README.md"), encoding="utf-8") as fh:
        t_rd = fh.read()
    def seccion_pre(t):
        a = t.index("## PRE-REGISTRO")
        return t[a:t.index("## RESULTADOS", a)].rstrip()
    cat(s, "Seccion PRE-REGISTRO del README igual a preregistro.md", True, seccion_pre(t_pre) == seccion_pre(t_rd))
    with open(os.path.join(AQUI, "variantes.csv"), encoding="utf-8") as fh:
        n_var = sum(1 for _ in fh) - 1
    num(s, "Filas de variantes.csv", "154", float(n_var), "red")
    n_pruebas = sum(len(v) for v in W.values())
    # El pre-registro dice "unas 80 pruebas" (estimacion previa); se cuentan 7 regiones x 12 ventanas + 2 R99.
    cat(s, "Pruebas WML: 'unas 80' (estimacion del pre-registro, +-10%%; reales: %d)" % n_pruebas, True, abs(n_pruebas - 80) <= 8)
    num(s, "DEXMXUS vs MXN=X: correlacion de cambios mensuales", "0.982", fxc["corr"], "red")
    num(s, "DEXMXUS vs MXN=X: diferencia absoluta media (pp)", "0.47", fxc["media_abs_dif_pp"], "red")

    # --- Veredicto sobre la afirmacion
    s = "Veredicto"
    e = W["Emerging"]
    num(s, "A1a Emerging W1b media x12 (%)", "9.59", e["W1b"]["x12"], "anual")
    num(s, "A1a Emerging W1b CAGR (%)", "9.37", e["W1b"]["cagr"], "anual")
    num(s, "A1a Emerging W1 media x12 (%)", "8.97", e["W1"]["x12"], "anual")
    num(s, "A1a Emerging W1 CAGR (%)", "8.84", e["W1"]["cagr"], "anual")
    num(s, "A1b Emerging W1 t NW(6)", "4.10", e["W1"]["t_nw"], "t")
    num(s, "A1b Emerging W1 IC95 inferior (%/mes)", "0.39", e["W1"]["ic_inf"], "media")
    num(s, "A1b Emerging W1 IC95 superior (%/mes)", "1.10", e["W1"]["ic_sup"], "media")
    cat(s, "A1b pasa Bonferroni |t|>2.69", True, abs(e["W1"]["t_nw"]) > 2.69)
    num(s, "A1c Emerging W2b media x12 (%)", "12.30", e["W2b"]["x12"], "anual")
    num(s, "A1c Emerging W2b CAGR (%)", "12.40", e["W2b"]["cagr"], "anual")
    num(s, "A1c Emerging W2 media x12 (%)", "11.40", e["W2"]["x12"], "anual")
    num(s, "A1c Emerging W2 CAGR (%)", "11.62", e["W2"]["cagr"], "anual")
    cat(s, "A1a con anios completos (W1) fuera de +-0.5 pp de 9.6", True, all(abs(v - 9.6) > 0.5 for v in (e["W1"]["x12"], e["W1"]["cagr"])))
    cat(s, "A1c con anios completos (W2) fuera de +-0.5 pp de 12.3", True, all(abs(v - 12.3) > 0.5 for v in (e["W2"]["x12"], e["W2"]["cagr"])))
    dx = W["Developed_ex_US"]
    num(s, "A2 Developed ex US W2 t NW(6)", "4.27", dx["W2"]["t_nw"], "t")
    cat(s, "A2 Developed ex US W2 veredicto", "apoyo", dx["W2"]["veredicto"])
    num(s, "A2 Developed ex US AMP13-post t NW(6)", "3.08", dx["AMP13-post"]["t_nw"], "t")
    cat(s, "A2 Developed ex US AMP13-post veredicto", "apoyo", dx["AMP13-post"]["veredicto"])
    a1a = any(abs(v - 9.6) <= 0.5 for v in (e["W1"]["x12"], e["W1"]["cagr"], e["W1b"]["x12"], e["W1b"]["cagr"]))
    a1b = e["W1"]["t_nw"] >= 3.0
    a1c = any(abs(v - 12.3) <= 0.5 for v in (e["W2"]["x12"], e["W2"]["cagr"], e["W2b"]["x12"], e["W2b"]["cagr"]))
    a2 = dx["W2"]["veredicto"] == "apoyo" and dx["AMP13-post"]["veredicto"] == "apoyo"
    etiqueta_global = "CONFIRMADA" if (a1a and a1b and a1c and a2) else ("CONFIRMADA CON MATICES" if (a1a and a1c) else "NO CONFIRMADA")
    cat(s, "Etiqueta global segun regla pre-registrada", "CONFIRMADA", etiqueta_global)
    meses26 = R["wml_em_2026"]
    for mtxt, val in (("2026-01", "8.02"), ("2026-02", "5.53"), ("2026-03", "-5.03"), ("2026-04", "12.84"),
                      ("2026-05", "9.58"), ("2026-06", "0.36"), ("2026-07", "-16.84"), ("2026-08", "8.02")):
        num(s, "WML Emerging %s (%%)" % mtxt, val, meses26[mtxt], "red")
    num(s, "WML Emerging 2026: media de 8 meses (%/mes)", "2.81", media(list(meses26.values())), "media")
    num(s, "Japon: t NW minima en 12 ventanas", "-0.62", min(W["Japan"][k]["t_nw"] for k in W["Japan"]), "t")
    num(s, "Japon: t NW maxima en 12 ventanas", "0.68", max(W["Japan"][k]["t_nw"] for k in W["Japan"]), "t")
    cat(s, "Japon: numero de ventanas", 12, len(W["Japan"]))
    cat(s, "Developed global: inconcluso en W1", "inconcluso", W["Developed"]["W1"]["veredicto"])
    cat(s, "Developed global: inconcluso en AMP13-post", "inconcluso", W["Developed"]["AMP13-post"]["veredicto"])
    num(s, "Developed ex US W1 t NW(6)", "2.50", dx["W1"]["t_nw"], "t")
    bonf = sorted(r for r in REGIONES if abs(W[r]["W1"]["t_nw"]) > 2.69)
    cat(s, "Pasan Bonferroni en W1", "Asia_Pacific_ex_Japan, Emerging, Europe", ", ".join(bonf))

    # --- Hipotesis
    s = "Hipotesis"
    apoyo_w0 = sorted(r for r in REGIONES if W[r]["W0"]["veredicto"] == "apoyo")
    num(s, "H1: regiones con apoyo en W0", "6", float(len(apoyo_w0)), "red")
    cat(s, "H1: region inconclusa en W0", "Japan", ", ".join(sorted(set(REGIONES) - set(apoyo_w0))))
    num(s, "H2 Emerging AMP13-pre media (%/mes)", "0.79", e["AMP13-pre"]["media"], "media")
    num(s, "H2 Emerging AMP13-post media (%/mes)", "0.94", e["AMP13-post"]["media"], "media")
    num(s, "H2 Emerging FF12-in media (%/mes)", "0.76", e["FF12-in"]["media"], "media")
    num(s, "H2 Emerging FF12-out media (%/mes)", "1.02", e["FF12-out"]["media"], "media")
    num(s, "H2 Emerging R98-pre media (%/mes)", "1.11", e["R98-pre"]["media"], "media")
    num(s, "H2 Emerging R98-post media (%/mes)", "0.77", e["R98-post"]["media"], "media")
    cat(s, "H2 Emerging R98-post sigue significativo", "apoyo", e["R98-post"]["veredicto"])
    eu = W["Europe"]
    # El README no dice que corte usa para Europe y North America; las cifras (0.94 -> 0.72 y
    # 0.63 -> 0.31) solo corresponden al corte AMP13 (se revisaron R98, FF12 y AMP13).
    num(s, "H2 Europe AMP13-pre media (%/mes)", "0.94", eu["AMP13-pre"]["media"], "media")
    num(s, "H2 Europe AMP13-post media (%/mes)", "0.72", eu["AMP13-post"]["media"], "media")
    cat(s, "H2 Europe AMP13-post sigue significativo", "apoyo", eu["AMP13-post"]["veredicto"])
    na = W["North_America"]
    num(s, "H2 North America AMP13-pre media (%/mes)", "0.63", na["AMP13-pre"]["media"], "media")
    num(s, "H2 North America AMP13-post media (%/mes)", "0.31", na["AMP13-post"]["media"], "media")
    num(s, "H2 North America AMP13-post t NW(6)", "1.26", na["AMP13-post"]["t_nw"], "t")
    cat(s, "H2 North America AMP13-post deja de ser significativa", "inconcluso", na["AMP13-post"]["veredicto"])
    ap = W["Asia_Pacific_ex_Japan"]
    num(s, "H2 Asia Pacific ex Japan AMP13-pre media (%/mes)", "0.79", ap["AMP13-pre"]["media"], "media")
    num(s, "H2 Asia Pacific ex Japan AMP13-post media (%/mes)", "0.96", ap["AMP13-post"]["media"], "media")
    num(s, "H2 Asia Pacific ex Japan FF12-in media (%/mes)", "0.67", ap["FF12-in"]["media"], "media")
    num(s, "H2 Asia Pacific ex Japan FF12-out media (%/mes)", "1.09", ap["FF12-out"]["media"], "media")
    num(s, "H2 Asia Pacific ex Japan R98-pre media (%/mes)", "0.99", ap["R98-pre"]["media"], "media")
    num(s, "H2 Asia Pacific ex Japan R98-post media (%/mes)", "0.82", ap["R98-post"]["media"], "media")
    cat(s, "H2 Asia Pacific ex Japan R98 pre y post significativos", "apoyo / apoyo", ap["R98-pre"]["veredicto"] + " / " + ap["R98-post"]["veredicto"])
    num(s, "H2 Emerging R99-pre media (%/mes)", "0.89", e["R99-pre"]["media"], "media")
    num(s, "H2 Emerging R99-post media (%/mes)", "0.83", e["R99-post"]["media"], "media")
    cat(s, "H2 Emerging R99-post sigue significativo", "apoyo", e["R99-post"]["veredicto"])
    cat(s, "North America inconclusa despues de cada publicacion (R98, FF12, AMP13, AMP09 post)", True,
        all(na[k]["veredicto"] == "inconcluso" for k in ("R98-post", "FF12-out", "AMP13-post", "AMP09-post")))
    cat(s, "H3 Japon inconcluso en todas sus ventanas", True, all(W["Japan"][k]["veredicto"] == "inconcluso" for k in W["Japan"]))
    rango(s, "Crash: asimetria (g1) por region", "-0.22", "-2.67", [C[r]["asimetria_g1"] for r in REGIONES], "red")
    cat(s, "Regiones cuyo peor mes W0 es 2009-04", "Developed, Developed_ex_US, Europe, North_America",
        ", ".join(r for r in REGIONES if C[r]["peores5"][0][0] == "2009-04"))
    rango(s, "Peor mes en 2009-04 (%)", "-22.52", "-26.09",
          [C[r]["peores5"][0][1] for r in REGIONES if C[r]["peores5"][0][0] == "2009-04"], "red")
    rango(s, "Mkt-RF en ese mes (%)", "10.49", "13.67",
          [C[r]["peores5"][0][2] for r in REGIONES if C[r]["peores5"][0][0] == "2009-04"], "red")
    cat(s, "Japan: peor mes W0", "1998-01", C["Japan"]["peores5"][0][0])
    num(s, "Japan: peor mes (%)", "-19.83", C["Japan"]["peores5"][0][1], "red")
    num(s, "Japan: Mkt-RF ese mes (%)", "10.55", C["Japan"]["peores5"][0][2], "red")
    cat(s, "Asia Pacific ex Japan: peor mes W0", "1998-10", C["Asia_Pacific_ex_Japan"]["peores5"][0][0])
    num(s, "Asia Pacific ex Japan: peor mes (%)", "-36.77", C["Asia_Pacific_ex_Japan"]["peores5"][0][1], "red")
    num(s, "Asia Pacific ex Japan: Mkt-RF ese mes (%)", "18.07", C["Asia_Pacific_ex_Japan"]["peores5"][0][2], "red")
    pe = C["Emerging"]["peores5"]
    cat(s, "Emerging: peor mes", "2026-07", pe[0][0])
    num(s, "Emerging: peor mes (%)", "-16.84", pe[0][1], "red")
    num(s, "Emerging: Mkt-RF en 2026-07 (%)", "-4.2", pe[0][2], "red")
    cat(s, "Emerging: 2o y 3er peores meses", "2009-05, 2009-04", pe[1][0] + ", " + pe[2][0])
    num(s, "Emerging 2009-05 WML (%)", "-14.8", pe[1][1], "red")
    num(s, "Emerging 2009-04 WML (%)", "-14.4", pe[2][1], "red")
    num(s, "Emerging 2009-05 Mkt-RF (%)", "18", pe[1][2], "red")
    num(s, "Emerging 2009-04 Mkt-RF (%)", "17", pe[2][2], "red")
    num(s, "Caida maxima del factor: Emerging (%)", "-37", C["Emerging"]["mdd"], "red")
    num(s, "Caida maxima del factor: Asia Pacific ex Japan (%)", "-53", C["Asia_Pacific_ex_Japan"]["mdd"], "red")
    cat(s, "Caida maxima: Emerging es la menor y APxJ la mayor", True,
        min(REGIONES, key=lambda r: -C[r]["mdd"]) == "Emerging" and min(REGIONES, key=lambda r: C[r]["mdd"]) == "Asia_Pacific_ex_Japan")
    num(s, "Correlacion W0 Emerging", "-0.12", C["Emerging"]["corr_W0"], "red")
    num(s, "Correlacion W0 Europe", "-0.34", C["Europe"]["corr_W0"], "red")
    cat(s, "Correlacion W0: Emerging la menos negativa, Europe la mas", True,
        max(REGIONES, key=lambda r: C[r]["corr_W0"]) == "Emerging" and min(REGIONES, key=lambda r: C[r]["corr_W0"]) == "Europe")
    rango(s, "Beta W0", "-0.07", "-0.27", [C[r]["beta_W0"] for r in REGIONES], "red")
    num(s, "Correlacion W1 Japan", "-0.07", C["Japan"]["corr_W1"], "red")
    num(s, "Correlacion W1 Europe", "-0.45", C["Europe"]["corr_W1"], "red")
    cat(s, "Correlacion W1: Japan la menos negativa, Europe la mas", True,
        max(REGIONES, key=lambda r: C[r]["corr_W1"]) == "Japan" and min(REGIONES, key=lambda r: C[r]["corr_W1"]) == "Europe")
    cat(s, "Correlacion negativa en todas las regiones (W0)", True, all(C[r]["corr_W0"] < 0 for r in REGIONES))
    num(s, "Beta en estado bajista: Emerging", "-0.26", C["Emerging"]["beta_bajista"], "red")
    rango(s, "Beta en estado bajista: desarrollados", "-0.33", "-0.57", [C[r]["beta_bajista"] for r in REGIONES if r != "Emerging"], "red")
    num(s, "Media WML Emerging en estado bajista (%/mes)", "0.49", C["Emerging"]["media_bajista"], "media")
    num(s, "Media WML Emerging en estado normal (%/mes)", "1.11", C["Emerging"]["media_normal"], "media")
    num(s, "Emerging: meses de WML sin estado", "18", float(C["Emerging"]["meses_sin_estado"]), "red")
    pl = P["Emerging"]
    v4 = [pl[k] for k in ("W0", "W1", "W2", "AMP13-post")]
    rango(s, "Pierna larga Emerging: media en 4 ventanas (%/mes)", "0.30", "0.39", [x["media"] for x in v4], "media")
    rango(s, "Pierna larga Emerging: media x12 en 4 ventanas (%)", "3.6", "4.6", [x["x12"] for x in v4], "anual")
    cat(s, "Pierna larga Emerging: apoyo en las 4 ventanas", True, all(x["veredicto"] == "apoyo" for x in v4))
    frac = [pl[k]["media"] / W["Emerging"][k]["media"] for k in ("W0", "W1", "W2", "AMP13-post")]
    num(s, "Pierna larga Emerging / WML (fraccion, promedio 4 ventanas)", "0.40", media(frac), "anual")
    apoyos_des = sorted("%s %s" % (r, k) for r in REGIONES if r != "Emerging" for k in ("W0", "W1", "W2", "AMP13-post")
                        if P[r][k]["veredicto"] == "apoyo")
    cat(s, "Pierna larga desarrollados con apoyo", "Asia_Pacific_ex_Japan W0, Europe W2", ", ".join(apoyos_des))

    # H4 ETFs
    def g(mom, mer, ventana="historia", imp="sin_imp", sp="base"):
        return E["%s-%s|%s|%s|%s" % (mom, mer, ventana, imp, sp)]
    todas = list(E.values())
    cat(s, "H4: inconclusa en los 10 pares y todas las sensibilidades", True, all(x["dif_usd"]["veredicto"] == "inconcluso" for x in todas))
    num(s, "EEMO - EEM, CAGR MXN neto (pp/anio), 2016-04 a 2026-08", "-1.32", g("EEMO", "EEM")["dif_cagr_mxn_neto"], "anual")
    cat(s, "EEMO: ventana", "2016-04 a 2026-08", g("EEMO", "EEM")["desde"] + " a " + g("EEMO", "EEM")["hasta"])
    num(s, "PIE - EEM, CAGR MXN neto (pp/anio), desde 2008-02", "-0.79", g("PIE", "EEM")["dif_cagr_mxn_neto"], "anual")
    cat(s, "PIE: inicio", "2008-02", g("PIE", "EEM")["desde"])
    num(s, "PIE caida maxima MXN neta (%)", "-56.9", g("PIE", "EEM")["mom"]["mdd"], "anual")
    num(s, "EEM caida maxima MXN neta en ventana de PIE (%)", "-40.3", g("PIE", "EEM")["mer"]["mdd"], "anual")
    for mom, lo, hi in (("IDMO", "2.05", "2.81"), ("IMTM", "0.22", "1.04"), ("PIZ", "0.50", "1.07"), ("IMOM", "-2.20", "-3.03")):
        vals = [g(mom, mer, "historia", "sin_imp", "base")["dif_cagr_mxn_neto"] for mer in ("EFA", "VEA")]
        rango(s, "%s - EFA/VEA, dif CAGR MXN neto, historia completa, caso base (pp)" % mom, lo, hi, vals, "anual")
    num(s, "PIZ - VEA ventana comun, dif CAGR MXN neto (pp)", "-0.17", g("PIZ", "VEA", "comun")["dif_cagr_mxn_neto"], "anual")
    rango(s, "t NW(6) de la diferencia USD, todos los pares, ventanas y sensibilidades", "-0.86", "1.15",
          [x["dif_usd"]["t_nw"] for x in todas], "t")
    rango(s, "Beta de la diferencia contra WML regional (pares base, historia)", "0.28", "0.61",
          [g(mom, mer)["beta_dif_vs_wml"] for mom, mer in PARES], "red")
    num(s, "Pierna larga Emerging 2016-04 a 2026-08 (%/mes)", "0.46", pl["ETF-2016-04"]["media"], "media")
    num(s, "Pierna larga Emerging 2016-04 a 2026-08, x12 (%)", "5.5", pl["ETF-2016-04"]["x12"], "anual")
    num(s, "Pierna larga Emerging 2016-04 a 2026-08, t NW(6)", "2.33", pl["ETF-2016-04"]["t_nw"], "t")
    num(s, "WML Emerging 2016-04 a 2026-08, x12 (%)", "12.7", R["wml_etf_ventana"]["Emerging"]["x12"], "anual")
    num(s, "EEMO - EEM USD 2016-04 a 2026-08 (%/mes)", "-0.05", g("EEMO", "EEM", "comun")["dif_usd"]["media"], "media")
    num(s, "PIE - EEM USD 2016-04 a 2026-08 (%/mes)", "0.12", g("PIE", "EEM", "comun")["dif_usd"]["media"], "media")
    fxd = R["datos"]["dexmxus"]
    num(s, "Cambio USD/MXN 2016-03 a 2026-08 (%)", "-1.2", (fxd["2026-08"] / fxd["2016-03"] - 1) * 100, "red")
    num(s, "USD/MXN fin 2008-01", "10.82", fxd["2008-01"], "red")
    num(s, "USD/MXN fin 2026-08", "17.01", fxd["2026-08"], "red")
    num(s, "PIE CAGR USD bruto 2008-02 a 2026-08 (%)", "3.49", g("PIE", "EEM")["cagr_usd_bruto_mom"], "anual")
    num(s, "PIE CAGR MXN neto 2008-02 a 2026-08 (%)", "5.99", g("PIE", "EEM")["mom"]["cagr"], "anual")
    pe_ = g("PIE", "EEM")
    cat(s, "PIE - EEM: la diferencia apenas cambia de USD bruto a MXN neto (< 0.1 pp)", True,
        abs((pe_["cagr_usd_bruto_mom"] - pe_["cagr_usd_bruto_mer"]) - pe_["dif_cagr_mxn_neto"]) < 0.1)

    # --- SIC
    s = "SIC"
    S = R["sic"]
    cat(s, "Yahoo .MX 404: EEMO, IMTM, IDMO, IMOM", True, all(not S[t]["existe"] for t in ("EEMO", "IMTM", "IDMO", "IMOM")))
    cat(s, "PIE.MX y PIZ.MX: simbolo MEX sin precios", True,
        all(S[t]["existe"] and S[t]["bolsa"] == "MEX" and S[t]["dias_2026_con_precio"] == 0 for t in ("PIE", "PIZ")))
    cat(s, "EEM, EFA, VEA .MX: precios en MXN en 2026", True,
        all(S[t]["existe"] and S[t]["moneda"] == "MXN" and S[t]["dias_2026_con_precio"] > 0 for t in MERCADO))

    # --- Conclusiones permitidas
    s = "Conclusiones"
    num(s, "Emerging W0 media (%/mes)", "0.85", e["W0"]["media"], "media")
    num(s, "Emerging W0 t NW(6)", "5.08", e["W0"]["t_nw"], "t")
    num(s, "Emerging W1 media (%/mes)", "0.75", e["W1"]["media"], "media")
    num(s, "Emerging W1 t NW(6)", "4.10", e["W1"]["t_nw"], "t")
    num(s, "Emerging W2 media (%/mes)", "0.95", e["W2"]["media"], "media")
    num(s, "Emerging W2 t NW(6)", "5.74", e["W2"]["t_nw"], "t")
    num(s, "Emerging AMP13-post media (%/mes)", "0.94", e["AMP13-post"]["media"], "media")
    num(s, "Emerging AMP13-post t NW(6)", "4.28", e["AMP13-post"]["t_nw"], "t")
    num(s, "Emerging W1 x12 '~9.0%'", "9.0", e["W1"]["x12"], "anual")
    num(s, "Emerging W2 x12 '~11.4%'", "11.4", e["W2"]["x12"], "anual")
    cat(s, "Momentum fuera de EUA con apoyo tambien post-2013 (Dev ex US, Europe, APxJ AMP13-post)", True,
        all(W[r]["AMP13-post"]["veredicto"] == "apoyo" for r in ("Developed_ex_US", "Europe", "Asia_Pacific_ex_Japan")))
    cat(s, "North America inconcluso desde 2000 (W1, W1b)", True,
        W["North_America"]["W1"]["veredicto"] == "inconcluso" and W["North_America"]["W1b"]["veredicto"] == "inconcluso")
    rango(s, "Peor mes de cada region en W0 (%)", "-17", "-37", [C[r]["peores5"][0][1] for r in REGIONES], "red")
    rango(s, "Conclusiones: pierna larga Emerging '~3.6-4.6%' x12", "3.6", "4.6",
          [P["Emerging"][k]["x12"] for k in ("W0", "W1", "W2", "AMP13-post")], "anual")
    rango(s, "Caida maxima del factor por region (%)", "-37", "-53", [C[r]["mdd"] for r in REGIONES], "red")
    cat(s, "Emerging: peor mes de toda la historia = 2026-07", "2026-07", C["Emerging"]["peores5"][0][0])
    cat(s, "EEMO y PIE por debajo de EEM en historia completa (MXN neto)", True,
        g("EEMO", "EEM")["dif_cagr_mxn_neto"] < 0 and g("PIE", "EEM")["dif_cagr_mxn_neto"] < 0)
    num(s, "t maxima de IDMO/IMTM/PIZ (conclusiones NO permitidas: 't <= 1.15')", "1.15",
        max(x["dif_usd"]["t_nw"] for k, x in E.items() if k.split("-")[0] in ("IDMO", "IMTM", "PIZ")), "t")
    return filas


def afirmaciones_anteriores(R):
    """Texto del README de V02 ANTES de la correccion del 2026-09-25 (seccion 'Hipotesis del pre-registro').
    Se conserva para que la diferencia se pueda reproducir; el README corregido se coteja en construir_comparacion."""
    W, C = R["wml"], R["crash"]
    filas = []

    def fila(cifra, readme, propio, ok):
        filas.append({"seccion": "README anterior", "cifra": cifra, "readme": readme, "propio": propio, "coincide": ok})

    ap = W["Asia_Pacific_ex_Japan"]
    cortes = [(a, b, ap[a]["media"], ap[b]["media"]) for a, b in (("R98-pre", "R98-post"), ("FF12-in", "FF12-out"), ("AMP13-pre", "AMP13-post"))]
    fila("'Asia Pacific ex Japan sube' (sin decir el corte)", "sube",
         "; ".join("%s %.2f -> %.2f" % (b.split("-")[0], x, y) for a, b, x, y in cortes), all(y > x for _, _, x, y in cortes))
    em = W["Emerging"]
    fila("'Emerging solo baja con el corte de Rouwenhorst (1998)'", "solo R98 baja",
         "R98 %.2f -> %.2f; R99 %.2f -> %.2f" % (em["R98-pre"]["media"], em["R98-post"]["media"], em["R99-pre"]["media"], em["R99-post"]["media"]),
         not (em["R99-post"]["media"] < em["R99-pre"]["media"]))
    regs = [r for r in REGIONES if r != "Emerging"]
    fila("'Peor mes en los desarrollados: abril de 2009'", "2009-04 en las 6 regiones desarrolladas",
         ", ".join("%s %s" % (r, C[r]["peores5"][0][0]) for r in regs), all(C[r]["peores5"][0][0] == "2009-04" for r in regs))
    vals = [C[r]["peores5"][0][1] for r in regs if C[r]["peores5"][0][0] == "2009-04"]
    fila("'de -22% a -26%' (extremo menos negativo)", "-22", "%.2f" % max(vals), abs(max(vals) - (-22)) <= 0.5)
    return filas


def comparar_tablas_ac03(R):
    """Tablas 'Fuente A' y 'Fuente B' de AC-03 que estaban pegadas en el README de V02 (lineas 196-241)."""
    ruta = os.path.join(RAIZ, "laboratorio", "auditorias", "AC-03-momentum-internacional", "README.md")
    filas = []
    with open(ruta, encoding="utf-8") as fh:
        for linea in fh:
            m = re.match(r"\| ([AB]):(\w+) \| (V\d) \| ([\d-]+)–([\d-]+) \| (\d+) \| (.*)$", linea)
            if not m:
                continue
            fuente, reg, v = m.group(1), m.group(2), m.group(3)
            celdas = [c.strip() for c in m.group(7).split("|")]
            prop = R["ac03"]["%s:%s:%s" % (fuente, reg, v)]
            ic = re.findall(r"-?\d+\.\d+", celdas[4])
            peor = re.match(r"(-?\d+\.\d+) \((\d{4}-\d{2})\)", celdas[7])
            mejor = re.match(r"(-?\d+\.\d+) \((\d{4}-\d{2})\)", celdas[8])
            chequeos = [
                ("n", float(m.group(6)), prop["n"], 0.0),
                ("media", float(celdas[0]), prop["media"], 0.01),
                ("DE", float(celdas[1]), prop["de"], 0.005),
                ("t IID", float(celdas[2]), prop["t_iid"], 0.05),
                ("t NW", float(celdas[3]), prop["t_nw"], 0.05),
                ("IC inf", float(ic[0]), prop["ic_inf"], 0.01),
                ("IC sup", float(ic[1]), prop["ic_sup"], 0.01),
                ("x12", float(celdas[5]), prop["x12"], 0.1),
                ("compuesto", float(celdas[6]), prop["cagr"], 0.1),
                ("peor", float(peor.group(1)), prop["peor"][0], 0.005),
                ("mejor", float(mejor.group(1)), prop["mejor"][0], 0.005),
            ]
            for nombre, a, b, tol in chequeos:
                filas.append({"seccion": "Tablas AC-03 pegadas", "cifra": "%s:%s %s %s" % (fuente, reg, v, nombre),
                              "readme": a, "propio": b, "dif": b - a, "tol": tol, "coincide": abs(b - a) <= tol + 1e-9})
            for nombre, a, b in (("fecha peor", peor.group(2), prop["peor"][1]), ("fecha mejor", mejor.group(2), prop["mejor"][1]),
                                 ("veredicto", celdas[9], prop["veredicto"]),
                                 ("periodo", m.group(4) + "–" + m.group(5), prop["desde"] + "–" + prop["hasta"])):
                filas.append({"seccion": "Tablas AC-03 pegadas", "cifra": "%s:%s %s %s" % (fuente, reg, v, nombre),
                              "readme": a, "propio": b, "dif": None, "tol": "igual", "coincide": a == b})
    return filas


def cotejo_con_original(R):
    """Se ejecuta DESPUES de calcular todo lo anterior. Lee resultados.json de reproducir.py
    solo para comparar, cifra por cifra, con la corrida propia (no se usa para calcular)."""
    ruta = os.path.join(AQUI, "resultados.json")
    if not os.path.exists(ruta):
        return []
    with open(ruta, encoding="utf-8") as fh:
        O = json.load(fh)
    filas = []

    def add(bloque, clave, orig, prop, tol):
        if isinstance(orig, (str, bool, list)) or isinstance(prop, (str, bool, list)) or orig is None:
            ok, dif = orig == prop, None
        else:
            dif = prop - orig
            ok = abs(dif) <= tol + 1e-12
        filas.append({"bloque": bloque, "cifra": clave, "original": orig, "propio": prop, "dif": dif,
                      "tol": tol, "coincide": ok})

    def ym(txt):
        return int(txt.replace("-", ""))

    def res_vs(bloque, clave, o, p_, con_se=True):
        add(bloque, clave + " n", o["n"], p_["n"], 0)
        if "desde" in o:
            add(bloque, clave + " desde", o["desde"], ym(p_["desde"]), 0)
            add(bloque, clave + " hasta", o["hasta"], ym(p_["hasta"]), 0)
        add(bloque, clave + " media", o["media"], p_["media"], 0.01)
        if con_se and "se" in o:
            add(bloque, clave + " se NW", o["se"], p_["se_nw"], 0.01)
        add(bloque, clave + " t NW", o["t"], p_["t_nw"], 0.05)
        if "t_iid" in o:
            add(bloque, clave + " t IID", o["t_iid"], p_["t_iid"], 0.05)
        if "ic95" in o:
            add(bloque, clave + " IC inf", o["ic95"][0], p_["ic_inf"], 0.01)
            add(bloque, clave + " IC sup", o["ic95"][1], p_["ic_sup"], 0.01)
        add(bloque, clave + " x12", o["x12"], p_["x12"], 0.1)
        add(bloque, clave + " CAGR", o["cagr"], p_["cagr"], 0.1)
        if "veredicto" in o:
            add(bloque, clave + " veredicto", o["veredicto"], p_["veredicto"], 0)

    for reg, ventanas in O["versiones"].items():
        add("versiones", reg + " faltantes WML", ventanas["faltantes_wml"], R["datos"][reg]["wml_faltantes"], 0)
        add("versiones", reg + " rango WML", ventanas["rango_wml"],
            [ym(R["datos"][reg]["wml_desde"]), ym(R["datos"][reg]["wml_hasta"])], 0)
    for reg, ventanas in O["wml"].items():
        for w, o in ventanas.items():
            res_vs("WML", "%s %s" % (reg, w), o, R["wml"][reg][w])
    for reg, ventanas in O["pierna_larga"].items():
        for w, o in ventanas.items():
            res_vs("Pierna larga", "%s %s" % (reg, w), o, R["pierna_larga"][reg][w])
    for reg, o in O["crash"].items():
        c = R["crash"][reg]
        for k, pe in enumerate(o["peores_5"]):
            add("Crash", "%s peor #%d mes" % (reg, k + 1), pe["mes"], ym(c["peores5"][k][0]), 0)
            add("Crash", "%s peor #%d WML" % (reg, k + 1), pe["wml"], c["peores5"][k][1], 1e-9)
            add("Crash", "%s peor #%d Mkt-RF" % (reg, k + 1), pe["mkt_rf"], c["peores5"][k][2], 1e-9)
        add("Crash", reg + " caida maxima", o["caida_maxima"]["caida"], c["mdd"], 0.1)
        add("Crash", reg + " caida maxima pico", o["caida_maxima"]["pico"], ym(c["mdd_pico"]), 0)
        add("Crash", reg + " caida maxima valle", o["caida_maxima"]["valle"], ym(c["mdd_valle"]), 0)
        add("Crash", reg + " peor 12m", o["peor_12m"]["rend"], c["peor12m"], 0.1)
        add("Crash", reg + " peor 12m fin", o["peor_12m"]["termina"], ym(c["peor12m_fin"]), 0)
        add("Crash", reg + " asimetria", o["asimetria"], c["asimetria_g1"], 0.005)
        add("Crash", reg + " desv mensual", o["desv_mensual"], c["desv_mensual"], 0.01)
    for reg, o in O["mercado"].items():
        c = R["crash"][reg]
        for w in ("W0", "W1"):
            add("Mercado", "%s %s n" % (reg, w), o[w]["n"], c["n_" + w], 0)
            add("Mercado", "%s %s corr" % (reg, w), o[w]["corr"], c["corr_" + w], 0.005)
            add("Mercado", "%s %s beta" % (reg, w), o[w]["beta"], c["beta_" + w], 0.005)
        for e in ("bajista", "normal"):
            add("Mercado", "%s %s n" % (reg, e), o[e]["n"], c["n_" + e], 0)
            add("Mercado", "%s %s beta" % (reg, e), o[e]["beta"], c["beta_" + e], 0.005)
            add("Mercado", "%s %s corr" % (reg, e), o[e]["corr"], c["corr_" + e], 0.005)
            add("Mercado", "%s %s media WML" % (reg, e), o[e]["media_wml"], c["media_" + e], 0.01)
    variantes = {"base": ("historia", "sin_imp", "base"), "sens_spread_0.30": ("historia", "sin_imp", "spread030"),
                 "sens_retencion_30": ("historia", "impuestos", "base"), "comun_2016_04": ("comun", "sin_imp", "base")}
    for par, vs in O["etf"].items():
        mom, mer = par.split("_vs_")
        for v, o in vs.items():
            p_ = R["etf"]["%s-%s|%s|%s|%s" % ((mom, mer) + variantes[v])]
            clave = "%s-%s %s" % (mom, mer, v)
            add("ETF", clave + " desde", o["desde"], ym(p_["desde"]), 0)
            add("ETF", clave + " n", o["n"], p_["n"], 0)
            for lado, lp, cu in (("etf", "mom", "cagr_usd_bruto_mom"), ("comparable", "mer", "cagr_usd_bruto_mer")):
                ol, pl_ = o[lado], p_[lp]
                add("ETF", "%s %s riqueza final MXN" % (clave, lado), ol["riqueza_final_mxn"], pl_["riqueza"], 0.5)
                add("ETF", "%s %s CAGR MXN neto" % (clave, lado), ol["cagr_mxn_neto"], pl_["cagr"], 0.1)
                add("ETF", "%s %s CAGR USD bruto" % (clave, lado), ol["cagr_usd_bruto"], p_[cu], 0.1)
                add("ETF", "%s %s vol anual MXN" % (clave, lado), ol["vol_anual_mxn"], pl_["vol"], 0.1)
                add("ETF", "%s %s caida max MXN" % (clave, lado), ol["caida_max_mxn"], pl_["mdd"], 0.1)
            add("ETF", clave + " dif CAGR MXN neto", o["dif_cagr_mxn_neto_pp"], p_["dif_cagr_mxn_neto"], 0.1)
            res_vs("ETF", clave + " dif USD", o["dif_mensual_usd"], p_["dif_usd"])
            add("ETF", clave + " beta dif vs WML", o["beta_dif_sobre_wml"], p_["beta_dif_vs_wml"], 0.005)
            add("ETF", clave + " corr dif vs WML", o["corr_dif_wml"], p_["corr_dif_vs_wml"], 0.005)
    oc = O["controles"]
    pc = R["controles"]
    add("Controles", "FX n", oc["fx_dexmxus_vs_yahoo"]["n"], pc["fx_fred_vs_yahoo"]["n"], 0)
    add("Controles", "FX corr", oc["fx_dexmxus_vs_yahoo"]["corr"], pc["fx_fred_vs_yahoo"]["corr"], 0.0005)
    add("Controles", "FX dif abs media", oc["fx_dexmxus_vs_yahoo"]["dif_abs_media_pp"], pc["fx_fred_vs_yahoo"]["media_abs_dif_pp"], 0.005)
    fxd = R["datos"]["dexmxus"]
    add("Controles", "FX cambio 2016-03 a 2026-08 (%)", oc["fx_dexmxus_vs_yahoo"]["cambio_acumulado_dexmxus_2016_04_2026_08_pct"],
        (fxd["2026-08"] / fxd["2016-03"] - 1) * 100, 0.05)
    for t in MOMENTUM + MERCADO:
        o = oc["yahoo_" + t]
        y = R["datos"]["yahoo"][t]
        add("Controles", t + " primer dia", o["primer_dia"], y["primer_dia"], 0)
        add("Controles", t + " dias sin precio", o["fechas_sin_precio"], y["dias_sin_precio"], 0)
        add("Controles", t + " cierre+div vs adj max (pp)", o["control_close+div_vs_adj_max_pp"], pc["cierre_div_vs_adj"]["por_ticker"][t]["max_abs"], 0.005)
        add("Controles", t + " cierre+div vs adj media abs (pp)", o["control_close+div_vs_adj_media_pp"], pc["cierre_div_vs_adj"]["por_ticker"][t]["media_abs"], 0.005)
    od = O["descriptivo_no_preregistrado"]
    for mtxt, v in od["wml_emerging_2026"].items():
        add("Descriptivo", "WML Emerging " + mtxt, v, R["wml_em_2026"][etiqueta(mes_de_yyyymm(mtxt))], 1e-9)
    for reg, o in od["ventana_etf_2016_04_2026_08"].items():
        res_vs("Descriptivo", reg + " WML 2016-04..2026-08", o["wml"], R["wml_etf_ventana"][reg], con_se=False)
        res_vs("Descriptivo", reg + " BigHigh-Mkt 2016-04..2026-08", o["bighigh_menos_mkt"], R["pierna_larga"][reg]["ETF-2016-04"], con_se=False)
    oa = O["afirmacion"]
    add("Afirmacion", "A1b t W1", oa["A1b_t_W1"], R["wml"]["Emerging"]["W1"]["t_nw"], 0.05)
    add("Afirmacion", "A1c t W2", oa["A1c_t_W2"], R["wml"]["Emerging"]["W2"]["t_nw"], 0.05)
    add("Afirmacion", "A2 Dev ex US W2", oa["A2_devexus_W2"], R["wml"]["Developed_ex_US"]["W2"]["veredicto"], 0)
    add("Afirmacion", "A2 Dev ex US AMP13-post", oa["A2_devexus_AMP13post"], R["wml"]["Developed_ex_US"]["AMP13-post"]["veredicto"], 0)
    for reg, b in oa["bonferroni_W1"].items():
        add("Afirmacion", "Bonferroni W1 " + reg, b, abs(R["wml"][reg]["W1"]["t_nw"]) > 2.69, 0)
    return filas


def cotejo_variantes_csv(R):
    """Compara las 154 filas de variantes.csv (salida del original) con la corrida propia."""
    ruta = os.path.join(AQUI, "variantes.csv")
    filas = []
    if not os.path.exists(ruta):
        return filas
    var_etf = {"base": ("historia", "sin_imp", "base"), "sens_spread_0.30": ("historia", "sin_imp", "spread030"),
               "sens_retencion_30": ("historia", "impuestos", "base"), "comun_2016_04": ("comun", "sin_imp", "base")}
    with open(ruta, encoding="utf-8") as fh:
        enc = fh.readline().strip().split(",")
        for linea in fh:
            f = dict(zip(enc, linea.strip().split(",")))
            if f["bloque"] == "WML":
                p_ = R["wml"][f["serie"]][f["ventana"]]
                cagr = p_["cagr"]
            elif f["bloque"] == "BigHigh-Mkt":
                p_ = R["pierna_larga"][f["serie"]][f["ventana"]]
                cagr = p_["cagr"]
            else:
                mom, mer = f["serie"].split("_vs_")
                e = R["etf"]["%s-%s|%s|%s|%s" % ((mom, mer) + var_etf[f["ventana"]])]
                p_ = e["dif_usd"]
                cagr = e["dif_cagr_mxn_neto"]
            cmp_ = [("n", float(f["n"]), p_["n"], 0), ("media", float(f["media_pct_mes"]), p_["media"], 0.01),
                    ("t NW", float(f["t_nw6"]), p_["t_nw"], 0.05), ("IC inf", float(f["ic95_inf"]), p_["ic_inf"], 0.01),
                    ("IC sup", float(f["ic95_sup"]), p_["ic_sup"], 0.01), ("x12", float(f["media_x12"]), p_["x12"], 0.1),
                    ("CAGR o dif CAGR", float(f["cagr_o_difcagr"]), cagr, 0.1)]
            ok = all(abs(b - a) <= t + 1e-9 for _, a, b, t in cmp_) and f["veredicto"] == p_["veredicto"] \
                and int(f["desde"]) == int(p_["desde"].replace("-", "")) and int(f["hasta"]) == int(p_["hasta"].replace("-", ""))
            filas.append({"fila": "%s|%s|%s" % (f["bloque"], f["serie"], f["ventana"]), "coincide": ok,
                          "max_dif_media": abs(float(f["media_pct_mes"]) - p_["media"]),
                          "max_dif_t": abs(float(f["t_nw6"]) - p_["t_nw"]),
                          "max_dif_cagr": abs(float(f["cagr_o_difcagr"]) - cagr)})
    return filas


def main():
    R = correr()
    filas = construir_comparacion(R)
    filas_ac03 = comparar_tablas_ac03(R)
    filas_ant = afirmaciones_anteriores(R)
    filas_orig = cotejo_con_original(R)
    filas_var = cotejo_variantes_csv(R)
    salida = {"generado": "2026-09-25", "script": "independiente.py", "resultados": R,
              "comparacion_readme": filas, "comparacion_tablas_ac03": filas_ac03,
              "afirmaciones_anteriores_del_readme": filas_ant,
              "cotejo_resultados_json_original": filas_orig, "cotejo_variantes_csv": filas_var}
    with open(os.path.join(AQUI, "independiente_resultados.json"), "w", encoding="utf-8") as fh:
        json.dump(salida, fh, ensure_ascii=False, indent=1, default=str)

    def fmt(v):
        if isinstance(v, float):
            return "%.4f" % v
        return str(v)

    print("== Comparacion con el README de V02 (cifras propias de V02) ==")
    for f in filas:
        marca = "OK " if f["coincide"] else "DIF"
        print("%s | %-12s | %-80s | README %-28s | propio %-14s" % (marca, f["seccion"], f["cifra"][:80], f["readme"], fmt(f["propio"])))
    n_ok = sum(f["coincide"] for f in filas)
    print("Cifras propias de V02: %d comparadas, %d coinciden, %d difieren" % (len(filas), n_ok, len(filas) - n_ok))
    print("Texto del README antes de la correccion del 2026-09-25 (debe fallar; se corrigio):")
    for f in filas_ant:
        print("  %s | %s | README %s | propio %s" % ("OK " if f["coincide"] else "DIF", f["cifra"], f["readme"], f["propio"]))
    n_ok2 = sum(f["coincide"] for f in filas_ac03)
    print("Tablas AC-03 pegadas (Fuente A y B): %d comparadas, %d coinciden" % (len(filas_ac03), n_ok2))
    for f in filas_ac03:
        if not f["coincide"]:
            print("DIF | %s | README %s | propio %s" % (f["cifra"], f["readme"], fmt(f["propio"])))
    n_ok3 = sum(f["coincide"] for f in filas_orig)
    print("Cotejo con resultados.json del original: %d cifras, %d coinciden" % (len(filas_orig), n_ok3))
    for f in filas_orig:
        if not f["coincide"]:
            print("DIF | %s | %s | original %s | propio %s" % (f["bloque"], f["cifra"], f["original"], fmt(f["propio"])))
    num_orig = [f for f in filas_orig if f["dif"] is not None]
    if num_orig:
        peor = max(num_orig, key=lambda f: abs(f["dif"]))
        print("   mayor diferencia numerica: %s (%s) = %.3g" % (peor["cifra"], peor["bloque"], peor["dif"]))
    n_ok4 = sum(f["coincide"] for f in filas_var)
    print("Cotejo con variantes.csv del original: %d filas, %d coinciden; max |dif| media %.2e, t %.2e, CAGR %.2e" % (
        len(filas_var), n_ok4, max(f["max_dif_media"] for f in filas_var), max(f["max_dif_t"] for f in filas_var),
        max(f["max_dif_cagr"] for f in filas_var)))
    print("SE NW: max |propio - herramientas| = %.2e" % R["controles"]["max_dif_se_nw_propio_vs_herramienta"])
    print("Huellas de datos/ coinciden con SHA256SUMS.txt:", R["datos"]["huellas_coinciden_con_SHA256SUMS"],
          "(%d archivos)" % R["datos"]["archivos_en_SHA256SUMS"])


if __name__ == "__main__":
    main()
