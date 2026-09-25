"""V02 - Momentum internacional: factor WML de French por region y ETFs de momentum en MXN.

Reproduce (desde la raiz del repo, sin red):
    python3 laboratorio/replicas/V02-momentum-internacional/reproducir.py
Datos congelados en ./datos (ver SHA256SUMS.txt). Pre-registro: preregistro.md.
Escribe resultados.json y variantes.csv (una fila por prueba) e imprime las tablas del README.
"""
import csv
import json
import math
import os
import statistics
import sys
from datetime import date, datetime, timezone

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, RAIZ)
from herramientas.estadistica import newey_west, veredicto  # noqa: E402
from herramientas.huellas import verificar  # noqa: E402
from herramientas.datos_historicos import (_texto_de_zip, tabla_french,  # noqa: E402
                                           parsear_yahoo_historia, fin_de_mes)

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
REZAGOS = 6
MIN_MESES = 24

# ---------------------------------------------------------------- parametros pre-registrados
REGIONES = {  # clave: (archivo WML, archivo 5 factores, archivo 6 carteras)
    "Developed": ("Developed_Mom_Factor_CSV.zip", "Developed_5_Factors_CSV.zip",
                  "Developed_6_Portfolios_ME_Prior_12_2_CSV.zip"),
    "Developed_ex_US": ("Developed_ex_US_Mom_Factor_CSV.zip", "Developed_ex_US_5_Factors_CSV.zip",
                        "Developed_ex_US_6_Portfolios_ME_Prior_12_2_CSV.zip"),
    "Europe": ("Europe_Mom_Factor_CSV.zip", "Europe_5_Factors_CSV.zip",
               "Europe_6_Portfolios_ME_Prior_12_2_CSV.zip"),
    "Japan": ("Japan_Mom_Factor_CSV.zip", "Japan_5_Factors_CSV.zip",
              "Japan_6_Portfolios_ME_Prior_12_2_CSV.zip"),
    "Asia_Pacific_ex_Japan": ("Asia_Pacific_ex_Japan_MOM_Factor_CSV.zip",
                              "Asia_Pacific_ex_Japan_5_Factors_CSV.zip",
                              "Asia_Pacific_ex_Japan_6_Portfolios_ME_Prior_12_2_CSV.zip"),
    "North_America": ("North_America_Mom_Factor_CSV.zip", "North_America_5_Factors_CSV.zip",
                      "North_America_6_Portfolios_ME_Prior_12_2_CSV.zip"),
    "Emerging": ("Emerging_MOM_Factor_CSV.zip", "Emerging_5_Factors_CSV.zip",
                 "Emerging_Markets_6_Portfolios_ME_Prior_12_2_CSV.zip"),
}
INI, FIN = "INI", "FIN"
VENTANAS = [  # (clave, desde YYYYMM | INI, hasta YYYYMM | FIN, solo_region)
    ("W0", INI, FIN, None),
    ("W1", 200001, 202512, None),
    ("W1b", 200001, FIN, None),
    ("W2", 201001, 202512, None),
    ("W2b", 201001, FIN, None),
    ("R98-pre", INI, 199802, None),
    ("R98-post", 199803, FIN, None),
    ("R99-pre", INI, 199908, "Emerging"),
    ("R99-post", 199909, FIN, "Emerging"),
    ("FF12-in", 199011, 201103, None),
    ("FF12-out", 201104, FIN, None),
    ("AMP13-pre", INI, 201306, None),
    ("AMP13-post", 201307, FIN, None),
    ("AMP09-post", 200904, FIN, None),
]
VENTANAS_PIERNA_LARGA = ["W0", "W1", "W2", "AMP13-post"]
BONFERRONI_T = 2.69  # 5% bilateral / 7 regiones en W1

# ETFs (pares pre-registrados). Primer mes de rendimiento: ver desviaciones en README.
PARES = [  # (etf, comparable, region WML para la beta, primer mes de rendimiento)
    ("EEMO", "EEM", "Emerging", 201604),
    ("PIE", "EEM", "Emerging", 200802),  # desviacion: Yahoo inicia 2008-01-07; 2008-01 no es mes completo
    ("IMTM", "EFA", "Developed_ex_US", 201502),
    ("IMTM", "VEA", "Developed_ex_US", 201502),
    ("PIZ", "EFA", "Developed_ex_US", 200802),
    ("PIZ", "VEA", "Developed_ex_US", 200802),
    ("IDMO", "EFA", "Developed_ex_US", 201604),
    ("IDMO", "VEA", "Developed_ex_US", 201604),
    ("IMOM", "EFA", "Developed_ex_US", 201601),
    ("IMOM", "VEA", "Developed_ex_US", 201601),
]
VENTANA_COMUN = 201604
FIN_ETF = 202608
MOMENTUM_ETF = {"EEMO", "PIE", "IMTM", "PIZ", "IDMO", "IMOM"}
COMISION = 0.0025 * 1.16          # 0.29% por lado (GBM, hecho)
SPREAD_MERCADO = 0.0005           # EEM/EFA/VEA, supuesto
SPREAD_MOM_BASE = 0.0015          # ETFs de momentum, caso base (supuesto)
SPREAD_MOM_SENS = 0.0030          # sensibilidad (supuesto)
RETENCION_DIV = 0.30              # sensibilidad: retencion EUA sin W-8BEN
CAPITAL = 20000.0


# ---------------------------------------------------------------- utilidades
def ym(d):
    return d.year * 100 + d.month


def leer_french(nombre, seccion=None):
    texto, _ = _texto_de_zip(open(os.path.join(DATOS, nombre), "rb").read())
    t = tabla_french(texto, "mensual", seccion)
    version = next((ln.strip() for ln in t["notas"] if "created using" in ln), None)
    return t, version


def serie(t, col):
    """{YYYYMM: valor en %} omitiendo faltantes."""
    return {ym(f): v * 100 for f, v in zip(t["fechas"], t["columnas"][col]) if v is not None}


def consecutivos(claves):
    idx = [k // 100 * 12 + k % 100 for k in claves]
    return all(b - a == 1 for a, b in zip(idx, idx[1:]))


def recortar(d, a, b):
    ks = sorted(d)
    a = ks[0] if a == INI else a
    b = ks[-1] if b == FIN else b
    return [(k, d[k]) for k in ks if a <= k <= b]


def cagr(xs_pct):
    w = 1.0
    for x in xs_pct:
        w *= 1 + x / 100
    return (w ** (12 / len(xs_pct)) - 1) * 100


def estad(pares_km):
    xs = [v for _, v in pares_km]
    r = newey_west(xs, REZAGOS)
    r["ic95"] = list(r["ic95"])
    r.update({"desde": pares_km[0][0], "hasta": pares_km[-1][0], "x12": 12 * r["media"],
              "cagr": cagr(xs), "veredicto": veredicto(r["ic95"])})
    return r


def corr_beta(x, y):
    mx, my = statistics.fmean(x), statistics.fmean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy), sxy / sxx  # corr, beta de y sobre x


def asimetria(xs):
    m, s, n = statistics.fmean(xs), statistics.pstdev(xs), len(xs)
    return sum((x - m) ** 3 for x in xs) / n / s ** 3


def caida_maxima(fechas, rend_pct):
    w, pico, fpico, peor = 1.0, 1.0, None, (0.0, None, None)
    for f, x in zip(fechas, rend_pct):
        w *= 1 + x / 100
        if w > pico:
            pico, fpico = w, f
        dd = w / pico - 1
        if dd < peor[0]:
            peor = (dd, fpico, f)
    return {"caida": peor[0] * 100, "pico": peor[1], "valle": peor[2]}


def peor_12m(fechas, rend_pct):
    peor = (float("inf"), None)
    for i in range(11, len(rend_pct)):
        w = 1.0
        for x in rend_pct[i - 11:i + 1]:
            w *= 1 + x / 100
        if w - 1 < peor[0]:
            peor = (w - 1, fechas[i])
    return {"rend": peor[0] * 100, "termina": peor[1]}


# ---------------------------------------------------------------- 0. integridad
fallas = verificar(os.path.join(AQUI, "SHA256SUMS.txt"))
assert fallas == [], f"los datos congelados cambiaron: {fallas}"

res = {"id": "V02-momentum-internacional", "unidades": "rendimientos mensuales en %; USD salvo que diga MXN",
       "versiones": {}, "wml": {}, "afirmacion": {}, "crash": {}, "mercado": {},
       "pierna_larga": {}, "etf": {}, "controles": {}}
filas_var = []

# ---------------------------------------------------------------- 1. WML por region
WML, MKT, RF, BIGHI = {}, {}, {}, {}
for reg, (f_wml, f_5f, f_6p) in REGIONES.items():
    t, v1 = leer_french(f_wml)
    t5, v2 = leer_french(f_5f)
    t6, v3 = leer_french(f_6p, "Average Value Weighted Returns -- Monthly")
    WML[reg] = serie(t, "WML")
    MKT[reg] = serie(t5, "Mkt-RF")
    RF[reg] = serie(t5, "RF")
    BIGHI[reg] = serie(t6, "BIG HiPRIOR")
    for d in (WML[reg], MKT[reg], RF[reg], BIGHI[reg]):
        assert consecutivos(sorted(d)), f"{reg}: meses no consecutivos"
    res["versiones"][reg] = {"wml": v1, "5f": v2, "6p": v3, "faltantes_wml": t["faltantes"],
                             "rango_wml": [min(WML[reg]), max(WML[reg])]}
    res["wml"][reg] = {}
    for clave, a, b, solo in VENTANAS:
        if solo and solo != reg:
            continue
        datos_v = recortar(WML[reg], a, b)
        if len(datos_v) < MIN_MESES:
            res["wml"][reg][clave] = {"n": len(datos_v), "nota": "menos de 24 meses: no se calcula"}
            continue
        r = estad(datos_v)
        res["wml"][reg][clave] = r
        filas_var.append(["WML", reg, clave, r["desde"], r["hasta"], r["n"], r["media"], r["t"],
                          r["ic95"][0], r["ic95"][1], r["veredicto"], r["x12"], r["cagr"]])

# ---------------------------------------------------------------- 2. afirmacion recibida
E = res["wml"]["Emerging"]
def dentro(valor, meta):
    return abs(valor - meta) <= 0.5
a1a = [(v, m, round(E[v][m], 2)) for v in ("W1", "W1b") for m in ("x12", "cagr") if dentro(E[v][m], 9.6)]
a1c = [(v, m, round(E[v][m], 2)) for v in ("W2", "W2b") for m in ("x12", "cagr") if dentro(E[v][m], 12.3)]
t_w1 = E["W1"]["t"]
a1b = "muy alta (>=3)" if t_w1 >= 3 else ("significativa, no muy alta" if t_w1 >= 1.96 else "no significativa")
dx = res["wml"]["Developed_ex_US"]
apoyos_a2 = [dx["W2"]["veredicto"] == "apoyo", dx["AMP13-post"]["veredicto"] == "apoyo"]
a2 = "confirmada" if all(apoyos_a2) else ("con matices" if any(apoyos_a2) else "no confirmada")
if not a1a or not a1c:
    glob = "no confirmada"
elif a1b.startswith("muy alta") and a2 == "confirmada":
    glob = "confirmada"
else:
    glob = "confirmada con matices"
res["afirmacion"] = {"A1a_coincidencias": a1a, "A1b_t_W1": t_w1, "A1b": a1b, "A1c_coincidencias": a1c,
                     "A1c_t_W2": E["W2"]["t"], "A2_devexus_W2": dx["W2"]["veredicto"],
                     "A2_devexus_AMP13post": dx["AMP13-post"]["veredicto"], "A2": a2, "global": glob,
                     "bonferroni_W1": {r: abs(res["wml"][r]["W1"]["t"]) > BONFERRONI_T for r in REGIONES}}

# ---------------------------------------------------------------- 3. crash y mercado
for reg in REGIONES:
    ks = sorted(WML[reg])
    x = [WML[reg][k] for k in ks]
    peores = sorted(ks, key=lambda k: WML[reg][k])[:5]
    res["crash"][reg] = {
        "peores_5": [{"mes": k, "wml": WML[reg][k], "mkt_rf": MKT[reg].get(k)} for k in peores],
        "caida_maxima": caida_maxima(ks, x), "peor_12m": peor_12m(ks, x),
        "asimetria": asimetria(x), "desv_mensual": statistics.stdev(x)}
    res["mercado"][reg] = {}
    for clave in ("W0", "W1"):
        a, b = (INI, FIN) if clave == "W0" else (200001, 202512)
        comunes = [k for k, _ in recortar(WML[reg], a, b) if k in MKT[reg]]
        c, beta = corr_beta([MKT[reg][k] for k in comunes], [WML[reg][k] for k in comunes])
        res["mercado"][reg][clave] = {"n": len(comunes), "corr": c, "beta": beta}
    # estado bajista: acumulado de Mkt-RF en t-24..t-1 < 0 (Daniel y Moskowitz 2016)
    mk = sorted(MKT[reg])
    estado = {}
    for i in range(24, len(mk)):
        w = 1.0
        for k in mk[i - 24:i]:
            w *= 1 + MKT[reg][k] / 100
        estado[mk[i]] = "bajista" if w - 1 < 0 else "normal"
    for st in ("bajista", "normal"):
        ks_st = [k for k in ks if estado.get(k) == st]
        c, beta = corr_beta([MKT[reg][k] for k in ks_st], [WML[reg][k] for k in ks_st])
        res["mercado"][reg][st] = {"n": len(ks_st), "beta": beta, "corr": c,
                                   "media_wml": statistics.fmean(WML[reg][k] for k in ks_st)}

# ---------------------------------------------------------------- 4. pierna larga academica
for reg in REGIONES:
    exceso = {k: BIGHI[reg][k] - (MKT[reg][k] + RF[reg][k]) for k in BIGHI[reg] if k in MKT[reg]}
    assert consecutivos(sorted(exceso))
    res["pierna_larga"][reg] = {}
    for clave, a, b, solo in VENTANAS:
        if clave not in VENTANAS_PIERNA_LARGA:
            continue
        r = estad(recortar(exceso, a, b))
        res["pierna_larga"][reg][clave] = r
        filas_var.append(["BigHigh-Mkt", reg, clave, r["desde"], r["hasta"], r["n"], r["media"], r["t"],
                          r["ic95"][0], r["ic95"][1], r["veredicto"], r["x12"], r["cagr"]])


# ---------------------------------------------------------------- 5. ETFs en MXN
def leer_yahoo(tk):
    txt = open(os.path.join(DATOS, f"yahoo_{tk}_1d.json")).read()
    h = parsear_yahoo_historia(txt, "1d", True)
    crudo = json.loads(txt)["chart"]["result"][0]
    desfase = int(crudo["meta"].get("gmtoffset", 0))
    divs = {}
    for ts, ev in (crudo.get("events", {}).get("dividends") or {}).items():
        dia = datetime.fromtimestamp(int(ts) + desfase, tz=timezone.utc).date()
        divs[ym(dia)] = divs.get(ym(dia), 0.0) + float(ev["amount"])
    adj, cie = {}, {}
    for f, p, c in zip(h["fechas"], h["precios"], h["cierres"]):
        adj[ym(f)] = p          # ultimo dia con precio del mes (fechas crecientes)
        if c is not None:
            cie[ym(f)] = c
    return {"adj": adj, "close": cie, "divs": divs, "sin_precio": [str(x) for x in h["fechas_sin_precio"]],
            "primer_dia": str(h["fechas"][0]), "nombre": crudo["meta"].get("longName")}


def rend_mensual(px, ks):
    return {k: (px[k] / px[p] - 1) * 100 for p, k in zip(ks, ks[1:])}


def meses(a, b):
    out, k = [], a
    while k <= b:
        out.append(k)
        k = k + 1 if k % 100 < 12 else (k // 100 + 1) * 100 + 1
    return out


def anterior(k):
    return k - 1 if k % 100 > 1 else (k // 100 - 1) * 100 + 12


# Tipo de cambio: ultima observacion valida de cada mes (DEXMXUS)
fx = {}
with open(os.path.join(DATOS, "fred_DEXMXUS.csv")) as f:
    for fila in csv.DictReader(f):
        v = fila["DEXMXUS"].strip()
        if v in ("", "."):
            continue
        fx[ym(date.fromisoformat(fila["observation_date"]))] = float(v)  # sobrescribe: queda la ultima
# Control: Yahoo MXN=X
y_fx = leer_yahoo("MXN_X")["adj"]
comunes_fx = [k for k in meses(200401, 202608) if k in fx and anterior(k) in fx and k in y_fx and anterior(k) in y_fx]
dfx = [(fx[k] / fx[anterior(k)] - 1) * 100 for k in comunes_fx]
dyf = [(y_fx[k] / y_fx[anterior(k)] - 1) * 100 for k in comunes_fx]
res["controles"]["fx_dexmxus_vs_yahoo"] = {"n": len(comunes_fx), "corr": corr_beta(dfx, dyf)[0],
                                           "dif_abs_media_pp": statistics.fmean(abs(a - b) for a, b in zip(dfx, dyf)),
                                           "cambio_acumulado_dexmxus_2016_04_2026_08_pct": (fx[202608] / fx[201603] - 1) * 100}

Y = {tk: leer_yahoo(tk) for tk in ("EEMO", "PIE", "IMTM", "PIZ", "IDMO", "IMOM", "EEM", "EFA", "VEA")}
R_ADJ, R_RET = {}, {}
for tk, y in Y.items():
    ks = sorted(y["adj"])
    R_ADJ[tk] = rend_mensual(y["adj"], ks)
    # sensibilidad: dividendos con retencion; control con retencion 0 contra adjclose
    kc = sorted(y["close"])
    R_RET[tk], dif0 = {}, []
    for p, k in zip(kc, kc[1:]):
        dv = y["divs"].get(k, 0.0)
        R_RET[tk][k] = ((y["close"][k] + (1 - RETENCION_DIV) * dv) / y["close"][p] - 1) * 100
        if k in R_ADJ[tk] and k >= 200802:
            dif0.append(abs(((y["close"][k] + dv) / y["close"][p] - 1) * 100 - R_ADJ[tk][k]))
    res["controles"][f"yahoo_{tk}"] = {"nombre": y["nombre"], "primer_dia": y["primer_dia"],
                                       "fechas_sin_precio": y["sin_precio"],
                                       "control_close+div_vs_adj_max_pp": max(dif0) if dif0 else None,
                                       "control_close+div_vs_adj_media_pp": statistics.fmean(dif0) if dif0 else None}


def evaluar(etf, bench, desde, hasta, spread_mom, rend):
    ks = meses(desde, hasta)
    faltan = [k for k in ks if k not in rend[etf] or k not in rend[bench] or k not in fx or anterior(k) not in fx]
    assert not faltan, f"{etf}/{bench}: faltan meses {faltan[:5]}"
    out = {}
    for tk, spread in ((etf, spread_mom), (bench, SPREAD_MERCADO)):
        mxn = [((1 + rend[tk][k] / 100) * fx[k] / fx[anterior(k)] - 1) * 100 for k in ks]
        costo = COMISION + spread
        w = CAPITAL * (1 - costo)
        for x in mxn:
            w *= 1 + x / 100
        w *= (1 - costo)
        n = len(ks)
        usd_bruto = 1.0
        for k in ks:
            usd_bruto *= 1 + rend[tk][k] / 100
        out[tk] = {"riqueza_final_mxn": w, "cagr_mxn_neto": ((w / CAPITAL) ** (12 / n) - 1) * 100,
                   "cagr_usd_bruto": (usd_bruto ** (12 / n) - 1) * 100,
                   "vol_anual_mxn": statistics.stdev(mxn) * math.sqrt(12),
                   "caida_max_mxn": caida_maxima(ks, mxn)["caida"]}
    dif = [(k, rend[etf][k] - rend[bench][k]) for k in ks]
    r = estad(dif)
    reg = next(p[2] for p in PARES if p[0] == etf)
    comunes = [k for k in ks if k in WML[reg]]
    c, beta = corr_beta([WML[reg][k] for k in comunes], [rend[etf][k] - rend[bench][k] for k in comunes])
    return {"desde": desde, "hasta": hasta, "n": len(ks), "etf": out[etf], "comparable": out[bench],
            "dif_cagr_mxn_neto_pp": out[etf]["cagr_mxn_neto"] - out[bench]["cagr_mxn_neto"],
            "dif_mensual_usd": r, "beta_dif_sobre_wml": beta, "corr_dif_wml": c, "n_beta": len(comunes)}


for etf, bench, reg, desde in PARES:
    clave = f"{etf}_vs_{bench}"
    res["etf"][clave] = {
        "base": evaluar(etf, bench, desde, FIN_ETF, SPREAD_MOM_BASE, R_ADJ),
        "sens_spread_0.30": evaluar(etf, bench, desde, FIN_ETF, SPREAD_MOM_SENS, R_ADJ),
        "sens_retencion_30": evaluar(etf, bench, desde, FIN_ETF, SPREAD_MOM_BASE, R_RET),
        "comun_2016_04": evaluar(etf, bench, VENTANA_COMUN, FIN_ETF, SPREAD_MOM_BASE, R_ADJ),
    }
    for var, r in res["etf"][clave].items():
        d = r["dif_mensual_usd"]
        filas_var.append(["ETF-dif", clave, var, d["desde"], d["hasta"], d["n"], d["media"], d["t"],
                          d["ic95"][0], d["ic95"][1], d["veredicto"], d["x12"], r["dif_cagr_mxn_neto_pp"]])

# ---------------------------------------------------------------- 6. DESCRIPTIVO, NO PRE-REGISTRADO
# (a) meses de 2026 de WML emergente: explican la diferencia entre W1/W2 y W1b/W2b.
# (b) misma ventana que los ETFs (2016-04 a 2026-08): WML y pierna larga academica, para separar
#     "periodo" de "implementacion". No lleva veredicto y no cambia ningun resultado pre-registrado.
res["descriptivo_no_preregistrado"] = {
    "wml_emerging_2026": {k: WML["Emerging"][k] for k in sorted(WML["Emerging"]) if k >= 202601},
    "ventana_etf_2016_04_2026_08": {}}
for reg in ("Emerging", "Developed_ex_US"):
    exceso = {k: BIGHI[reg][k] - (MKT[reg][k] + RF[reg][k]) for k in BIGHI[reg] if k in MKT[reg]}
    w_ = estad(recortar(WML[reg], VENTANA_COMUN, FIN_ETF))
    l_ = estad(recortar(exceso, VENTANA_COMUN, FIN_ETF))
    res["descriptivo_no_preregistrado"]["ventana_etf_2016_04_2026_08"][reg] = {
        "wml": {k: w_[k] for k in ("n", "media", "t", "x12", "cagr")},
        "bighigh_menos_mkt": {k: l_[k] for k in ("n", "media", "t", "x12", "cagr")}}

# ---------------------------------------------------------------- salida
with open(os.path.join(AQUI, "resultados.json"), "w") as f:
    json.dump(res, f, indent=1, default=str)
with open(os.path.join(AQUI, "variantes.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["bloque", "serie", "ventana", "desde", "hasta", "n", "media_pct_mes", "t_nw6",
                "ic95_inf", "ic95_sup", "veredicto", "media_x12", "cagr_o_difcagr"])
    for fila in filas_var:
        w.writerow([f"{v:.6f}" if isinstance(v, float) else v for v in fila])


def fmt_ic(ic):
    return f"[{ic[0]:.3f}, {ic[1]:.3f}]"


print("## Versiones:", {r: v["wml"] for r, v in res["versiones"].items()})
print("\n## WML por region y ventana (USD, largo-corto, sin costos)")
print("| Region | Ventana | Meses | n | Media %/mes | x12 | CAGR factor | t NW(6) | IC95 | Veredicto |")
print("|---|---|---|---|---|---|---|---|---|---|")
for reg in REGIONES:
    for clave, *_ in VENTANAS:
        r = res["wml"][reg].get(clave)
        if not r or "media" not in r:
            continue
        print(f"| {reg} | {clave} | {r['desde']}-{r['hasta']} | {r['n']} | {r['media']:.3f} | {r['x12']:.2f}% | "
              f"{r['cagr']:.2f}% | {r['t']:.2f} | {fmt_ic(r['ic95'])} | {r['veredicto']} |")
print("\n## Afirmacion:", json.dumps(res["afirmacion"], default=str))
print("\n## Crash y mercado")
print("| Region | Peor mes (WML, Mkt-RF) | 2o | 3o | Caida max (pico-valle) | Peor 12m | Asim. | Corr W0 | Beta W0 | Corr W1 | Beta bajista (n) | Beta normal (n) | Media WML bajista | Media WML normal |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for reg in REGIONES:
    c, m = res["crash"][reg], res["mercado"][reg]
    p = [f"{x['mes']} ({x['wml']:.1f}, {x['mkt_rf']:.1f})" for x in c["peores_5"]]
    cm = c["caida_maxima"]
    print(f"| {reg} | {p[0]} | {p[1]} | {p[2]} | {cm['caida']:.1f}% ({cm['pico']}-{cm['valle']}) | "
          f"{c['peor_12m']['rend']:.1f}% (a {c['peor_12m']['termina']}) | {c['asimetria']:.2f} | {m['W0']['corr']:.2f} | "
          f"{m['W0']['beta']:.2f} | {m['W1']['corr']:.2f} | {m['bajista']['beta']:.2f} ({m['bajista']['n']}) | "
          f"{m['normal']['beta']:.2f} ({m['normal']['n']}) | {m['bajista']['media_wml']:.2f} | {m['normal']['media_wml']:.2f} |")
print("\n## Peores 5 meses completos")
for reg in REGIONES:
    print(reg, [(x["mes"], round(x["wml"], 2), round(x["mkt_rf"], 2)) for x in res["crash"][reg]["peores_5"]])
print("\n## Pierna larga: Big High - mercado regional (USD, sin costos)")
print("| Region | Ventana | Meses | n | Media %/mes | x12 | t NW(6) | IC95 | Veredicto |")
print("|---|---|---|---|---|---|---|---|---|")
for reg in REGIONES:
    for clave in VENTANAS_PIERNA_LARGA:
        r = res["pierna_larga"][reg][clave]
        print(f"| {reg} | {clave} | {r['desde']}-{r['hasta']} | {r['n']} | {r['media']:.3f} | {r['x12']:.2f}% | "
              f"{r['t']:.2f} | {fmt_ic(r['ic95'])} | {r['veredicto']} |")
print("\n## ETFs (MXN, netos de comision GBM y spread; gasto del ETF ya en el precio)")
print("| Par | Variante | Meses | n | CAGR MXN ETF | CAGR MXN comp. | Dif pp | 20k MXN -> ETF | -> comp. | Vol ETF | Vol comp. | Caida ETF | Caida comp. | Dif media %/mes USD | t NW(6) | IC95 | Veredicto | Beta dif/WML |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for clave, vs in res["etf"].items():
    etf, bench = clave.split("_vs_")
    for var, r in vs.items():
        d = r["dif_mensual_usd"]
        print(f"| {clave} | {var} | {r['desde']}-{r['hasta']} | {r['n']} | {r['etf']['cagr_mxn_neto']:.2f}% | "
              f"{r['comparable']['cagr_mxn_neto']:.2f}% | {r['dif_cagr_mxn_neto_pp']:+.2f} | {r['etf']['riqueza_final_mxn']:,.0f} | "
              f"{r['comparable']['riqueza_final_mxn']:,.0f} | {r['etf']['vol_anual_mxn']:.1f}% | {r['comparable']['vol_anual_mxn']:.1f}% | "
              f"{r['etf']['caida_max_mxn']:.1f}% | {r['comparable']['caida_max_mxn']:.1f}% | {d['media']:+.3f} | {d['t']:.2f} | "
              f"{fmt_ic(d['ic95'])} | {d['veredicto']} | {r['beta_dif_sobre_wml']:.2f} |")
print("\n## Descriptivo NO pre-registrado:", json.dumps(res["descriptivo_no_preregistrado"], default=str))
print("\n## Controles:", json.dumps(res["controles"], default=str, indent=0))
print(f"\nFilas en variantes.csv: {len(filas_var)}")
