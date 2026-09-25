"""V04 - Benchmarks en pesos (S&P 500, IPC via NAFTRAC, CETES 28) y SMA de 10 meses con senal en USD o MXN.

Reproduce (desde la raiz del repo, SIN red):
    python3 laboratorio/replicas/V04-benchmarks-en-pesos-y-sma10-senal-mxn/reproducir.py
Datos congelados en ./datos (huellas en SHA256SUMS.txt, junto con la del pre-registro).
Pre-registro: prerregistro.md (escrito 2026-09-25 05:40 UTC, antes de calcular).
Salidas: resultados.json (determinista) y V04-variantes.csv (registro del motor, solo se agrega).

Doble implementacion interna (si difieren mas de 1e-10, el script se detiene):
  - Parser propio de Yahoo/FRED contra herramientas.datos_historicos / herramientas.datos.
  - Simulador propio de la regla (senal, deriva, costos, metricas) contra herramientas/backtest.py.
  - Newey-West de la herramienta contra una forma cuadratica con la matriz de Bartlett completa.
Solo biblioteca estandar.
"""
from __future__ import annotations

import bisect
import csv
import io
import json
import math
import os
import statistics
import sys
from datetime import date, datetime, timedelta, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
from herramientas import backtest as bt  # noqa: E402
from herramientas import metricas as mt  # noqa: E402
from herramientas.datos import parsear_fred_csv  # noqa: E402
from herramientas.datos_historicos import parsear_yahoo_historia  # noqa: E402
from herramientas.estadistica import Z95, newey_west, veredicto  # noqa: E402
from herramientas.huellas import verificar  # noqa: E402

DATOS = os.path.join(AQUI, "datos")
ID = "V04"
REZAGOS = 6
TOL_CAGR = 0.0030   # +-0.30 pp (pre-registro, seccion 8)
TOL_PCT = 0.010     # +-1.0 pp en caidas y cambios porcentuales
EPS = 1e-10
C_GBM = bt.COMISION_GBM_POR_LADO             # 0.0029 (hecho)
S_LIQ = bt.SPREAD_POR_LADO["liquido"]         # 0.0005 (supuesto)
COSTOS = {
    "defecto": (C_GBM, S_LIQ),
    "sin_costos": (0.0, 0.0),
    "spread_medio": (C_GBM, bt.SPREAD_POR_LADO["medio"]),
    "doble_pierna": (2 * C_GBM, 2 * S_LIQ),
}
AFIRMACIONES = {"A1_sp_mxn_cagr": 0.145, "A2_naftrac_cagr": 0.063, "A3_cetes_cagr": 0.061,
                "A4_2008_usd": -0.47, "A4_2008_mxn": -0.216,
                "A5_sma_mxn_cagr": 0.146, "A5_bh_cagr": 0.135, "A5_sma_mxn_mdd": -0.12, "A5_bh_mdd": -0.31}
R = {"id": ID, "prerregistro": "prerregistro.md (2026-09-25 05:40 UTC)", "controles": {}}


def detener(msg):
    print("ALTO:", msg)
    sys.exit(1)


# =============================================================== 0. huellas
fallas = verificar(os.path.join(AQUI, "SHA256SUMS.txt"))
if fallas:
    detener("huellas que no coinciden: " + ", ".join(fallas))
R["controles"]["huellas"] = "OK (datos, descargar_datos.py y prerregistro.md)"


# =============================================================== 1. parsers (propios + herramienta)
def leer(nombre, modo="r", codificacion="utf-8"):
    with open(os.path.join(DATOS, nombre), modo, encoding=None if "b" in modo else codificacion) as f:
        return f.read()


def _dia_local(ts, desfase):
    m = datetime.fromtimestamp(int(ts) + desfase, tz=timezone.utc)
    d = m.date()
    return d + timedelta(days=1) if m.hour >= 22 else d


def yahoo_propio(nombre):
    """-> (adj {fecha: adjclose}, close {fecha: close}, dividendos {fecha: monto}, meta)."""
    res = json.loads(leer(nombre))["chart"]["result"][0]
    meta = res["meta"]
    off = int(meta.get("gmtoffset", 0))
    ts = res.get("timestamp") or []
    q = res["indicators"]["quote"][0]
    cl = q.get("close") or []
    adj_l = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose") or []
    adj, close = {}, {}
    for i, t in enumerate(ts):
        d = _dia_local(t, off)
        if i < len(cl) and cl[i] is not None:
            close[d] = float(cl[i])
        if i < len(adj_l) and adj_l[i] is not None:
            adj[d] = float(adj_l[i])
    divs = {}
    for k, v in ((res.get("events") or {}).get("dividends") or {}).items():
        divs[_dia_local(int(v.get("date", k)), off)] = float(v["amount"])
    return adj, close, divs, meta


def yahoo_herramienta(nombre):
    h = parsear_yahoo_historia(leer(nombre), "1d", solo_periodos_completos=False)
    return dict(zip(h["fechas"], h["precios"])), dict(zip(h["fechas"], h["cierres"]))


def fred_propio(nombre):
    out = {}
    for fila in list(csv.reader(io.StringIO(leer(nombre))))[1:]:
        if len(fila) >= 2 and fila[1].strip() not in ("", "."):
            out[date.fromisoformat(fila[0].strip())] = float(fila[1])
    return out


def banxico(nombre, columna=1):
    """CSV de exportacion del SIE de Banxico (latin-1). Filas de datos: dd/mm/aaaa,valor[,valor]."""
    out = {}
    for linea in leer(nombre, codificacion="latin-1").splitlines():
        partes = linea.strip().split(",")
        if len(partes) <= columna or len(partes[0]) != 10 or partes[0][2] != "/":
            continue
        try:
            d = date(int(partes[0][6:10]), int(partes[0][3:5]), int(partes[0][0:2]))
        except ValueError:
            continue
        v = partes[columna].strip().strip('"')
        if v in ("", "N/E", "N/D"):
            continue
        out[d] = float(v)
    return out


def banxico_csv_modulo(nombre, columna=1):
    """Segunda ruta de lectura (modulo csv) para contrastar el parser de Banxico."""
    out = {}
    for fila in csv.reader(io.StringIO(leer(nombre, codificacion="latin-1"))):
        if len(fila) > columna and len(fila[0]) == 10 and fila[0].count("/") == 2:
            try:
                d = datetime.strptime(fila[0], "%d/%m/%Y").date()
                out[d] = float(fila[columna])
            except ValueError:
                continue
    return out


YAHOO = {}
dif_parser = 0.0
for tk, arch in [("SPY", "yahoo_SPY_1d.json"), ("SP500TR", "yahoo_SP500TR_1d.json"),
                 ("GSPC", "yahoo_GSPC_1d.json"), ("NAFTRAC", "yahoo_NAFTRAC.MX_1d.json"),
                 ("MXX", "yahoo_MXX_1d.json"), ("MXNX", "yahoo_MXN_X_1d.json"),
                 ("SPY.MX", "yahoo_SPY.MX_1d.json"), ("IVV.MX", "yahoo_IVV.MX_1d.json"),
                 ("VOO.MX", "yahoo_VOO.MX_1d.json")]:
    adj, close, divs, meta = yahoo_propio(arch)
    h_adj, h_cl = yahoo_herramienta(arch)
    comunes = set(adj) & set(h_adj)
    # la herramienta usa close cuando adjclose es nulo: esas fechas extra deben tener close y no adj
    faltan = set(adj) - set(h_adj)
    extra = {d for d in set(h_adj) - set(adj) if not (d in close and h_adj[d] == close[d])}
    if faltan or extra:
        detener(f"{tk}: fechas distintas entre parser propio y herramienta: {sorted(faltan | extra)[:5]}")
    for d in comunes:
        dif_parser = max(dif_parser, abs(adj[d] - h_adj[d]) / adj[d])
    YAHOO[tk] = {"adj": adj, "close": close, "divs": divs, "moneda": meta.get("currency"),
                 "zona": meta.get("exchangeTimezoneName")}
if dif_parser > EPS:
    detener(f"parser Yahoo difiere {dif_parser}")
DEX = fred_propio("fred_DEXMXUS.csv")
dex_h = dict(parsear_fred_csv(leer("fred_DEXMXUS.csv")))
if dex_h != DEX:
    detener("parser FRED propio distinto de herramientas.datos.parsear_fred_csv")
IMF = fred_propio("fred_INTGSTMXM193N.csv")
FIX = banxico("banxico_CF102_fix_SF43718.csv")
CET = banxico("banxico_CF107_cetes28_SF43936.csv")
if FIX != banxico_csv_modulo("banxico_CF102_fix_SF43718.csv") or \
        CET != banxico_csv_modulo("banxico_CF107_cetes28_SF43936.csv"):
    detener("los dos parsers de Banxico difieren")
MXNX = YAHOO["MXNX"]["close"]
R["controles"]["parsers"] = {"yahoo_dif_rel_max": dif_parser, "fred_identico": True, "banxico_identico": True}
R["datos"] = {k: {"desde": min(v["adj"]).isoformat(), "hasta": max(v["adj"]).isoformat(), "n": len(v["adj"]),
                  "dividendos": len(v["divs"]), "moneda": v["moneda"]} for k, v in YAHOO.items()}
for k, v in [("DEXMXUS", DEX), ("FIX_SF43718", FIX), ("CETES28_SF43936", CET), ("IMF_INTGSTMXM193N", IMF)]:
    R["datos"][k] = {"desde": min(v).isoformat(), "hasta": max(v).isoformat(), "n": len(v)}


# =============================================================== 2. series derivadas
class Serie:
    """Serie diaria {fecha: valor} con busqueda 'ultimo dato <= fecha'."""

    def __init__(self, nombre, valores: dict):
        self.nombre = nombre
        self.v = dict(valores)
        self.f = sorted(self.v)

    def en_o_antes(self, d, max_dias=7, primero_si_no_hay=False):
        k = bisect.bisect_right(self.f, d) - 1
        if k < 0:
            if primero_si_no_hay:
                return self.f[0], self.v[self.f[0]], "primer_dato"
            return None
        if (d - self.f[k]).days > max_dias:
            return None
        return self.f[k], self.v[self.f[k]], ""

    def ventana(self, d0, d1):
        i0 = bisect.bisect_left(self.f, d0)
        i1 = bisect.bisect_right(self.f, d1)
        return [(f, self.v[f]) for f in self.f[i0:i1]]

    def cierres_mes(self):
        e = {}
        for f in self.f:
            e[(f.year, f.month)] = f
        return e

    def primeros_mes(self):
        p = {}
        for f in reversed(self.f):
            p[(f.year, f.month)] = f
        return p


class IndiceCetes:
    """I(d) con interes simple entre colocaciones: I(d) = I(a_k)(1 + y_k/100 (d - a_k)/360)."""

    def __init__(self, subastas: dict, nombre="CETES28"):
        self.nombre = nombre
        self.a = sorted(subastas)
        self.y = [subastas[x] for x in self.a]
        self.i = [1.0]
        for k in range(1, len(self.a)):
            self.i.append(self.i[-1] * (1 + self.y[k - 1] / 100 * (self.a[k] - self.a[k - 1]).days / 360))

    def valor(self, d):
        k = bisect.bisect_right(self.a, d) - 1
        if k < 0 or (d - self.a[k]).days > 14:
            raise ValueError(f"CETES sin subasta util para {d}")
        return self.i[k] * (1 + self.y[k] / 100 * (d - self.a[k]).days / 360)

    def tasa_en(self, d):
        k = bisect.bisect_right(self.a, d) - 1
        return self.y[k]

    def r(self, d0, d1):
        return self.valor(d1) / self.valor(d0) - 1

    def en_o_antes(self, d, max_dias=7, primero_si_no_hay=False):
        return d, self.valor(d), ""


CETES = IndiceCetes(CET)


def cetes_r_por_periodo(d0, d1):
    """Sensibilidad: tasa de la ultima subasta <= d0, interes simple por todo el periodo."""
    return CETES.tasa_en(d0) / 100 * (d1 - d0).days / 360


def en_mxn(precios: dict, fx: dict):
    return {d: p * fx[d] for d, p in precios.items() if d in fx}


def tr_desde_cierre(close: dict, divs: dict, fraccion=1.0):
    """Indice de rendimiento total desde cierres + dividendos (reinvertidos al cierre del ex-date)."""
    fechas = sorted(close)
    faltan = [d for d in divs if d not in close and fechas[0] <= d <= fechas[-1]]
    if faltan:
        detener(f"dividendos en fechas sin cierre: {faltan[:3]}")
    out = {fechas[0]: close[fechas[0]]}
    for a, b in zip(fechas, fechas[1:]):
        out[b] = out[a] * (close[b] + fraccion * divs.get(b, 0.0)) / close[a]
    return out


SPY = YAHOO["SPY"]
SPY_NET30 = tr_desde_cierre(SPY["close"], SPY["divs"], 0.70)
SPY_TR_REC = tr_desde_cierre(SPY["close"], SPY["divs"], 1.0)
S = {
    "SP_USD_SPY": Serie("SPY adjclose (USD)", SPY["adj"]),
    "SP_USD_SP500TR": Serie("^SP500TR (USD)", YAHOO["SP500TR"]["adj"]),
    "SP_USD_GSPC": Serie("^GSPC precio (USD)", YAHOO["GSPC"]["adj"]),
    "SP_MXN_SPY_DEX": Serie("SPY adjclose x DEXMXUS", en_mxn(SPY["adj"], DEX)),
    "SP_MXN_SPY_FIX": Serie("SPY adjclose x FIX", en_mxn(SPY["adj"], FIX)),
    "SP_MXN_SPY_MXNX": Serie("SPY adjclose x MXN=X", en_mxn(SPY["adj"], MXNX)),
    "SP_MXN_SP500TR_DEX": Serie("^SP500TR x DEXMXUS", en_mxn(YAHOO["SP500TR"]["adj"], DEX)),
    "SP_MXN_GSPC_DEX": Serie("^GSPC precio x DEXMXUS", en_mxn(YAHOO["GSPC"]["adj"], DEX)),
    "SP_MXN_SPY_NET30_DEX": Serie("SPY dividendos netos de 30% x DEXMXUS", en_mxn(SPY_NET30, DEX)),
    "SP_MXN_SPY_TRREC_DEX": Serie("SPY cierre + dividendos brutos (reconstruido) x DEXMXUS", en_mxn(SPY_TR_REC, DEX)),
    "SP_MXN_GSPC_FIX": Serie("^GSPC precio x FIX", en_mxn(YAHOO["GSPC"]["adj"], FIX)),
    "SP_MXN_SP500TR_FIX": Serie("^SP500TR x FIX", en_mxn(YAHOO["SP500TR"]["adj"], FIX)),
    "NAFTRAC_ADJ": Serie("NAFTRAC adjclose", YAHOO["NAFTRAC"]["adj"]),
    "NAFTRAC_CLOSE": Serie("NAFTRAC close (sin ajuste)", YAHOO["NAFTRAC"]["close"]),
    "MXX_PRECIO": Serie("^MXX (IPC precio)", YAHOO["MXX"]["adj"]),
    "SPY.MX_ADJ": Serie("SPY.MX adjclose (SIC, MXN)", YAHOO["SPY.MX"]["adj"]),
    "IVV.MX_ADJ": Serie("IVV.MX adjclose (SIC, MXN)", YAHOO["IVV.MX"]["adj"]),
    "CETES28": CETES,
}


def cagr(v0, v1, d0, d1):
    return (v1 / v0) ** (365.25 / (d1 - d0).days) - 1


def caida_maxima(puntos):
    """puntos: [(fecha, valor)] -> (mdd, fecha_pico, fecha_valle)."""
    pico_v, pico_f = -math.inf, None
    peor = (0.0, None, None)
    for f, v in puntos:
        if v > pico_v:
            pico_v, pico_f = v, f
        dd = v / pico_v - 1
        if dd < peor[0]:
            peor = (dd, pico_f, f)
    return peor


def rendimiento_ventana(serie, d0, d1, primero_si_no_hay=False):
    a = serie.en_o_antes(d0, primero_si_no_hay=primero_si_no_hay)
    b = serie.en_o_antes(d1)
    if a is None or b is None:
        return None
    return {"desde": a[0].isoformat(), "hasta": b[0].isoformat(), "cagr": cagr(a[1], b[1], a[0], b[0]),
            "total": b[1] / a[1] - 1, "nota": a[2]}


# =============================================================== 3. A1-A3: benchmarks
VENTANAS = {
    "W1": (date(2007, 12, 31), date(2026, 8, 31)),
    "W2": (date(2008, 1, 31), date(2026, 8, 31)),
    "W3": (date(2008, 1, 2), date(2026, 9, 18)),
    "W4": (date(2007, 12, 31), date(2025, 12, 31)),
}
SERIES_A = ["SP_MXN_SPY_DEX", "SP_MXN_SPY_FIX", "SP_MXN_SPY_MXNX", "SP_MXN_SP500TR_DEX", "SP_MXN_GSPC_DEX",
            "SP_MXN_SPY_NET30_DEX", "SP_MXN_SPY_TRREC_DEX", "SP_USD_SPY", "SP_USD_SP500TR", "SP_USD_GSPC",
            "NAFTRAC_ADJ", "NAFTRAC_CLOSE", "MXX_PRECIO", "SPY.MX_ADJ", "IVV.MX_ADJ", "CETES28"]
tabla_a = {}
for s in SERIES_A:
    tabla_a[s] = {}
    for w, (d0, d1) in VENTANAS.items():
        tabla_a[s][w] = rendimiento_ventana(S[s], d0, d1, primero_si_no_hay=True)


def fin_de_mes(a, m):
    return (date(a + m // 12, m % 12 + 1, 1) - timedelta(days=1))


def rango_meses(a0, m0, a1, m1):
    out = []
    a, m = a0, m0
    while (a, m) <= (a1, m1):
        out.append((a, m))
        a, m = (a + 1, 1) if m == 12 else (a, m + 1)
    return out


sens_inicio = {}
for s in ["SP_MXN_SPY_DEX", "NAFTRAC_ADJ", "CETES28", "SP_USD_SPY"]:
    filas = []
    for a, m in rango_meses(2007, 1, 2009, 12):
        r = rendimiento_ventana(S[s], fin_de_mes(a, m), date(2026, 8, 31))
        if r is not None:
            filas.append({"inicio": f"{a}-{m:02d}", **r})
    cs = [x["cagr"] for x in filas]
    sens_inicio[s] = {"filas": filas, "min": min(cs), "max": max(cs),
                      "inicio_min": filas[cs.index(min(cs))]["inicio"], "inicio_max": filas[cs.index(max(cs))]["inicio"]}
sens_fin = {}
for s in ["SP_MXN_SPY_DEX", "NAFTRAC_ADJ", "CETES28"]:
    sens_fin[s] = {d.isoformat(): rendimiento_ventana(S[s], date(2007, 12, 31), d, primero_si_no_hay=True)
                   for d in [date(2025, 12, 31), date(2026, 6, 30), date(2026, 8, 31), date(2026, 9, 18)]}

# CETES: particion mensual e IMF (contraste)
v = 1.0
for a, m in rango_meses(2008, 1, 2026, 8):
    d0, d1 = fin_de_mes(a, m - 1) if m > 1 else date(a - 1, 12, 31), fin_de_mes(a, m)
    v *= 1 + cetes_r_por_periodo(d0, d1)
cetes_mensual_w1 = cagr(1.0, v, date(2007, 12, 31), date(2026, 8, 31))
v = 1.0
imf_meses = 0
for a, m in rango_meses(2008, 1, 2026, 8):
    tasa = IMF.get(date(a, m, 1))
    if tasa is not None:
        v *= 1 + tasa / 1200
        imf_meses += 1
cetes_imf = {"cagr_hasta_ultimo_dato": None, "meses": imf_meses}
if imf_meses:
    ult = max(d for d in IMF if d <= date(2026, 8, 1))
    cetes_imf["cagr_hasta_ultimo_dato"] = cagr(1.0, v, date(2007, 12, 31), fin_de_mes(ult.year, ult.month))
    cetes_imf["ultimo_mes"] = ult.isoformat()[:7]

# Dividendos de NAFTRAC por anio (contribucion adj - close) y comparacion con el IPC de precio
naftrac_anual = []
for anio in range(2008, 2026):
    d0 = date(anio - 1, 12, 31)
    d1 = date(anio, 12, 31)
    ra = rendimiento_ventana(S["NAFTRAC_ADJ"], d0, d1, primero_si_no_hay=True)
    rc = rendimiento_ventana(S["NAFTRAC_CLOSE"], d0, d1, primero_si_no_hay=True)
    rm = rendimiento_ventana(S["MXX_PRECIO"], d0, d1)
    ndiv = sum(1 for f in YAHOO["NAFTRAC"]["divs"] if f.year == anio)
    naftrac_anual.append({"anio": anio, "adj": ra["total"], "close": rc["total"],
                          "div_implicito": (1 + ra["total"]) / (1 + rc["total"]) - 1,
                          "mxx_precio": rm["total"] if rm else None, "eventos_div_yahoo": ndiv})

R["A1_A3"] = {"ventanas": {k: [a.isoformat(), b.isoformat()] for k, (a, b) in VENTANAS.items()},
              "tabla": tabla_a, "sens_inicio": sens_inicio, "sens_fin": sens_fin,
              "cetes_particion_mensual_W1": cetes_mensual_w1, "cetes_imf": cetes_imf,
              "naftrac_por_anio": naftrac_anual}


# ---- pruebas NW de A (diferencias mensuales)
def nw_matriz(x, L=REZAGOS):
    """Segunda implementacion: forma cuadratica con la matriz de Bartlett completa."""
    n = len(x)
    mu = sum(x) / n
    u = [a - mu for a in x]
    tot = 0.0
    for i in range(n):
        for j in range(max(0, i - L), min(n, i + L + 1)):
            tot += (1 - abs(i - j) / (L + 1)) * u[i] * u[j]
    return math.sqrt(tot / n / n * n / (n - 1))


DIF_NW = [0.0]


def prueba(x, etiqueta):
    r = newey_west(x, REZAGOS)
    se2 = nw_matriz(x)
    DIF_NW[0] = max(DIF_NW[0], abs(se2 - r["se"]))
    if abs(se2 - r["se"]) > 1e-12:
        detener(f"NW difiere en {etiqueta}")
    return {"prueba": etiqueta, "n": r["n"], "media_pct_mes": 100 * r["media"], "x12_pct": 1200 * r["media"],
            "t_nw6": r["t"], "t_iid": r["t_iid"], "ic95_pct_mes": [100 * r["ic95"][0], 100 * r["ic95"][1]],
            "veredicto": veredicto(r["ic95"])}


def mensuales(serie: Serie):
    e = serie.cierres_mes()
    claves = sorted(e)
    return {k: serie.v[e[k]] / serie.v[e[p]] - 1 for p, k in zip(claves, claves[1:])}, e


sp_m, sp_e = mensuales(S["SP_MXN_SPY_DEX"])
usd_m, _ = mensuales(Serie("usd_en_fechas_mxn", {d: SPY["adj"][d] for d in S["SP_MXN_SPY_DEX"].f}))
naf_m, _ = mensuales(S["NAFTRAC_ADJ"])
cet_m = {}
claves_sp = sorted(sp_e)
for p, k in zip(claves_sp, claves_sp[1:]):
    cet_m[k] = CETES.r(sp_e[p], sp_e[k])
pruebas_a = []
W1M = rango_meses(2008, 1, 2026, 8)
W1M_NAF = rango_meses(2008, 2, 2026, 8)
P95 = rango_meses(1995, 1, 2007, 12)
pruebas_a.append(prueba([sp_m[k] - cet_m[k] for k in W1M], "S&P MXN - CETES, 2008-01 a 2026-08"))
pruebas_a.append(prueba([sp_m[k] - cet_m[k] for k in P95], "S&P MXN - CETES, 1995-01 a 2007-12"))
pruebas_a.append(prueba([sp_m[k] - naf_m[k] for k in W1M_NAF], "S&P MXN - NAFTRAC, 2008-02 a 2026-08"))
pruebas_a.append(prueba([naf_m[k] - cet_m[k] for k in W1M_NAF], "NAFTRAC - CETES, 2008-02 a 2026-08"))
fx_m = {k: (1 + sp_m[k]) / (1 + usd_m[k]) - 1 for k in sp_m}
xs = [usd_m[k] for k in W1M]
fs = [fx_m[k] for k in W1M]
malos = [k for k in W1M if usd_m[k] < -0.05]
curva_usd_m = [(sp_e[k], SPY["adj"][sp_e[k]]) for k in [(2007, 12)] + W1M]
curva_mxn_m = [(sp_e[k], S["SP_MXN_SPY_DEX"].v[sp_e[k]]) for k in [(2007, 12)] + W1M]
amortiguador = {
    "corr_mensual_sp_usd_vs_fx": statistics.correlation(xs, fs),
    "meses_sp_usd_menor_a_-5pct": len(malos),
    "fx_media_en_esos_meses": statistics.fmean(fx_m[k] for k in malos),
    "sp_usd_media_en_esos_meses": statistics.fmean(usd_m[k] for k in malos),
    "sp_mxn_media_en_esos_meses": statistics.fmean(sp_m[k] for k in malos),
    "mdd_mensual_usd_W1": caida_maxima(curva_usd_m)[0],
    "mdd_mensual_mxn_W1": caida_maxima(curva_mxn_m)[0],
    "vol_anual_usd_W1": statistics.stdev(xs) * math.sqrt(12),
    "vol_anual_mxn_W1": statistics.stdev([sp_m[k] for k in W1M]) * math.sqrt(12),
    "vol_anual_naftrac_W1": statistics.stdev([naf_m[k] for k in W1M_NAF]) * math.sqrt(12),
    "mdd_mensual_naftrac_W1": caida_maxima([(date(2008, 1, 2), YAHOO["NAFTRAC"]["adj"][date(2008, 1, 2)])] +
                                           [(S["NAFTRAC_ADJ"].cierres_mes()[k], S["NAFTRAC_ADJ"].v[S["NAFTRAC_ADJ"].cierres_mes()[k]]) for k in W1M])[0],
}
R["A1_A3"]["pruebas_nw"] = pruebas_a
R["A1_A3"]["amortiguador"] = amortiguador

# ---- control de conversion: SIC (SPY.MX close) contra SPY close x FX en la misma fecha
conv = {}
for nom, fx in [("DEXMXUS", DEX), ("FIX", FIX), ("MXN=X", MXNX)]:
    difs = []
    for d, c in YAHOO["SPY.MX"]["close"].items():
        if d in SPY["close"] and d in fx and d >= date(2016, 1, 1):
            difs.append(c / (SPY["close"][d] * fx[d]) - 1)
    difs.sort()
    ab = sorted(abs(x) for x in difs)
    conv[nom] = {"n": len(difs), "mediana": difs[len(difs) // 2], "mediana_abs": ab[len(ab) // 2],
                 "p90_abs": ab[int(0.9 * len(ab))]}
R["control_conversion_sic_2016_en_adelante"] = conv


# =============================================================== 4. A4: 2008
def medidas_2008(serie: Serie):
    out = {}
    r = rendimiento_ventana(serie, date(2007, 12, 31), date(2008, 12, 31))
    out["cambio_2007-12-31_a_2008-12-31"] = r["total"] if r else None
    for nombre, (d0, d1) in {"dentro_2008": (date(2007, 12, 31), date(2008, 12, 31)),
                             "crisis_2007_2009": (date(2007, 1, 1), date(2009, 12, 31))}.items():
        diarios = serie.ventana(d0, d1)
        e = {}
        for f, x in diarios:
            e[(f.year, f.month)] = (f, x)
        mens = [e[k] for k in sorted(e)]
        dd_d = caida_maxima(diarios)
        dd_m = caida_maxima(mens)
        out[f"mdd_diaria_{nombre}"] = {"valor": dd_d[0], "pico": dd_d[1].isoformat(), "valle": dd_d[2].isoformat()}
        out[f"mdd_mensual_{nombre}"] = {"valor": dd_m[0], "pico": dd_m[1].isoformat(), "valle": dd_m[2].isoformat()}
    return out


a4 = {s: medidas_2008(S[s]) for s in ["SP_USD_SPY", "SP_USD_SP500TR", "SP_USD_GSPC", "SP_MXN_SPY_DEX",
                                      "SP_MXN_SP500TR_DEX", "SP_MXN_GSPC_DEX", "SP_MXN_SPY_FIX",
                                      "SP_MXN_SP500TR_FIX", "SP_MXN_GSPC_FIX"]}


def coincidencias(objetivo, prefijo):
    out = []
    for s, med in a4.items():
        if not s.startswith(prefijo):
            continue
        for k, x in med.items():
            val = x if isinstance(x, float) else (x or {}).get("valor")
            if val is not None and abs(val - objetivo) <= TOL_PCT:
                out.append({"serie": s, "medida": k, "valor": val})
    return out


R["A4"] = {"medidas": a4, "coincide_47_usd": coincidencias(-0.47, "SP_USD"),
           "coincide_21.6_mxn": coincidencias(-0.216, "SP_MXN")}


# =============================================================== 5. A5: SMA
def siguiente(ym):
    a, m = ym
    return (a + 1, 1) if m == 12 else (a, m + 1)


def anterior(ym):
    a, m = ym
    return (a - 1, 12) if m == 1 else (a, m - 1)


class Universo:
    """Fechas base (activo y FX en la misma fecha), valores del activo y de las senales."""

    def __init__(self, nombre, valores_activo: dict, senales: dict):
        self.nombre = nombre
        self.base = Serie(nombre, valores_activo)
        self.E = self.base.cierres_mes()
        self.F = self.base.primeros_mes()
        self.senales = {k: {d: s[d] for d in self.base.f} for k, s in senales.items()}

    def etiquetas(self, modo, ym_ini, ym_fin):
        if modo == "T0":
            meses = rango_meses(*anterior(anterior(ym_ini)), *ym_fin)
            return [self.E[k] for k in meses]
        meses = rango_meses(*anterior(ym_ini), *siguiente(ym_fin))
        return [self.F[k] for k in meses]

    def puntos_senal(self, clave, hist_desde=None):
        return [(self.E[k], self.senales[clave][self.E[k]]) for k in sorted(self.E)
                if hist_desde is None or k >= hist_desde]


def senal_sma(n: int, clave: str):
    def senal(h):
        serie = h.extras[clave]
        if len(serie) < n:
            return 0.0
        ultimos = [x for _, x in serie[len(serie) - n:]]
        return 1.0 if ultimos[-1] > sum(ultimos) / n else 0.0
    senal.__qualname__ = senal.__name__ = f"sma{n}_{clave}"
    return senal


def simulador_propio(etq, v_act, cetes_r, puntos, n, costo, siempre=None, w0=0.0):
    """Implementacion independiente del motor (misma especificacion, otro codigo)."""
    fe = [f for f, _ in puntos]
    pv = [x for _, x in puntos]
    w_prev, ra_prev, rb_prev = w0, None, None
    rn, rex, ws = [], [], []
    for k in range(2, len(etq)):
        dec = etq[k - 1]
        if siempre is not None:
            w = siempre
        else:
            j = bisect.bisect_right(fe, dec)
            ult = pv[max(0, j - n):j]
            w = 1.0 if (j >= n and ult[-1] > sum(ult) / n) else 0.0
        ra = v_act[etq[k]] / v_act[etq[k - 1]] - 1
        re_ = cetes_r(etq[k - 1], etq[k])
        w_pre = w_prev if k == 2 else w_prev * (1 + ra_prev) / (1 + rb_prev)
        c = abs(w - w_pre) * costo
        rb = w * ra + (1 - w) * re_
        rn.append((1 - c) * (1 + rb) - 1)
        rex.append(re_)
        ws.append(w)
        w_prev, ra_prev, rb_prev = w, ra, rb
    return rn, rex, ws


def metricas_propias(fechas, f0, rn, rex):
    curva = [(f0, 1.0)]
    for f, r in zip(fechas, rn):
        curva.append((f, curva[-1][1] * (1 + r)))
    anios = (fechas[-1] - f0).days / 365.25
    ex = [a - b for a, b in zip(rn, rex)]
    sd = statistics.stdev(ex)
    sh = statistics.fmean(ex) / sd * math.sqrt(12) if sd > 0 else (math.inf if statistics.fmean(ex) > 0 else 0.0)
    return {"cagr": curva[-1][1] ** (1 / anios) - 1, "mdd": caida_maxima(curva)[0],
            "vol_anual": statistics.stdev(rn) * math.sqrt(12), "sharpe": sh}


CORRIDAS = {}
DIF_MOTOR = [0.0]
NOMBRES_SEG = ["1995-2007", "2008-2026"]


def correr(variante, uni: Universo, modo, clave_senal, n, *, costos="defecto", es_prueba=True,
           ym_ini=(1995, 1), ym_fin=(2026, 8), hist_desde=None, cetes_r=None, nota="", parametros=None,
           cortar=True):
    cetes_r = cetes_r or CETES.r
    etq = uni.etiquetas(modo, ym_ini, ym_fin)
    v = uni.base.v
    activo = [(etq[k], v[etq[k]] / v[etq[k - 1]] - 1) for k in range(1, len(etq))]
    efectivo = [(etq[k], cetes_r(etq[k - 1], etq[k])) for k in range(1, len(etq))]
    c, s = COSTOS[costos]
    extras, senal = {}, None
    if clave_senal == "bh":
        senal = bt.senal_comprar_y_mantener
    elif clave_senal == "efectivo":
        senal = bt.senal_efectivo
    else:
        extras = {clave_senal: uni.puntos_senal(clave_senal, hist_desde)}
        senal = senal_sma(n, clave_senal)
    corte = uni.E.get((2007, 12)) if modo == "T0" else uni.F.get((2008, 1))
    usar_corte = cortar and corte is not None and etq[1] < corte < etq[-1]
    res = bt.backtest_senal(activo, efectivo, senal, id_replica=ID, variante=variante,
                            comision_por_lado=c, spread_por_lado=s, min_historia=1,
                            cortes=[corte] if usar_corte else [],
                            nombres_segmentos=NOMBRES_SEG if usar_corte else None,
                            moneda="MXN", periodos_por_anio=12, extras=extras,
                            parametros=parametros or {}, es_prueba=es_prueba, nota=nota,
                            fuente_datos=f"V04 congelado: {uni.nombre}; efectivo CETES28 Banxico SF43936",
                            dir_replicas=AQUI)
    # ---- doble implementacion
    siempre = 1.0 if clave_senal == "bh" else (0.0 if clave_senal == "efectivo" else None)
    puntos = extras.get(clave_senal, [])
    rn, rex, ws = simulador_propio(etq, v, cetes_r, puntos, n, c + s, siempre)
    if len(rn) != len(res.r_neto) or any(abs(a - b) > EPS for a, b in zip(rn, res.r_neto)) or ws != res.exposicion:
        detener(f"motor y simulador propio difieren en {variante}")
    segs = {"completo": (0, len(rn))}
    if usar_corte:
        i = bisect.bisect_right(res.fechas, corte)
        segs.update({NOMBRES_SEG[0]: (0, i), NOMBRES_SEG[1]: (i, len(rn))})
    salida = {"variante": variante, "modo": modo, "senal": clave_senal, "n": n, "costos": costos,
              "es_prueba": es_prueba, "universo": uni.nombre, "nota": nota, "segmentos": {}}
    for sg, (i0, i1) in segs.items():
        f0 = res.curva[0][0] if i0 == 0 else res.fechas[i0 - 1]
        mp = metricas_propias(res.fechas[i0:i1], f0, rn[i0:i1], rex[i0:i1])
        me = res.metricas[sg]
        for k in ("cagr", "mdd", "vol_anual", "sharpe"):
            DIF_MOTOR[0] = max(DIF_MOTOR[0], abs(mp[k] - me[k]))
            if abs(mp[k] - me[k]) > EPS:
                detener(f"metrica {k} difiere en {variante}/{sg}: {mp[k]} vs {me[k]}")
        salida["segmentos"][sg] = {
            "desde": f0.isoformat(), "hasta": res.fechas[i1 - 1].isoformat(), "n_meses": i1 - i0,
            "cagr": me["cagr"], "vol_anual": me["vol_anual"], "sharpe": me["sharpe"], "mdd": me["mdd"],
            "tiempo_invertido": me["tiempo_invertido"], "n_cambios_senal": me["n_cambios_senal"],
            "costo_anual": me["costo_anual"], "cagr_efectivo": me["cagr_efectivo"],
            "sharpe_periodo": me["sharpe_periodo"]}
    CORRIDAS[variante] = {"res": res, "resumen": salida, "corte": corte if usar_corte else None}
    return salida


# ---- universos
def universo_usd_mxn(nombre, precios_tr_usd, fx, precios_senal_usd=None):
    p_sig = precios_senal_usd or precios_tr_usd
    comunes = {d for d in precios_tr_usd if d in fx and d in p_sig}
    act = {d: precios_tr_usd[d] * fx[d] for d in comunes}
    return Universo(nombre, act, {"usd": {d: p_sig[d] for d in comunes},
                                  "mxn": {d: p_sig[d] * fx[d] for d in comunes}})


U = {
    "base": universo_usd_mxn("SPY adjclose x DEXMXUS", SPY["adj"], DEX),
    "sp500tr": universo_usd_mxn("^SP500TR x DEXMXUS", YAHOO["SP500TR"]["adj"], DEX),
    "fix": universo_usd_mxn("SPY adjclose x FIX Banxico", SPY["adj"], FIX),
    "mxnx": universo_usd_mxn("SPY adjclose x MXN=X", SPY["adj"], MXNX),
    "senal_precio": universo_usd_mxn("SPY adjclose x DEXMXUS; senal sobre SPY close (sin dividendos)",
                                     SPY["adj"], DEX, SPY["close"]),
    "div_neto30": universo_usd_mxn("SPY dividendos netos de 30% x DEXMXUS", SPY_NET30, DEX),
    "spymx": Universo("SPY.MX adjclose (SIC, MXN, Yahoo)", YAHOO["SPY.MX"]["adj"],
                      {"mxn": YAHOO["SPY.MX"]["adj"]}),
}
ub = U["base"]
_e_spy = Serie("x", SPY["adj"]).cierres_mes()
R["A5_meses_E_distinto_ultimo_dia_spy"] = sum(1 for k, d in ub.E.items() if d != _e_spy[k])

# ---- bloque de prueba: N = 16
for modo in ("T0", "T1"):
    for sig in ("usd", "mxn"):
        for n in (6, 8, 10, 12):
            correr(f"sma{n}_{sig}_{modo}", ub, modo, sig, n, es_prueba=True,
                   parametros={"n": n, "senal": sig, "ejecucion": modo})
# ---- referencias
for modo in ("T0", "T1"):
    correr(f"bh_{modo}", ub, modo, "bh", 0, es_prueba=False, parametros={"ejecucion": modo}, nota="referencia")
    correr(f"cetes_{modo}", ub, modo, "efectivo", 0, es_prueba=False, parametros={"ejecucion": modo},
           nota="referencia")
# ---- sensibilidad de costos
for costos in ("sin_costos", "spread_medio", "doble_pierna"):
    for modo in ("T0", "T1"):
        for sig in ("usd", "mxn"):
            correr(f"sma10_{sig}_{modo}|{costos}", ub, modo, sig, 10, costos=costos, es_prueba=False,
                   parametros={"n": 10, "senal": sig, "ejecucion": modo, "costos": costos}, nota="sens. costos")
        correr(f"bh_{modo}|{costos}", ub, modo, "bh", 0, costos=costos, es_prueba=False,
               parametros={"ejecucion": modo, "costos": costos}, nota="sens. costos")
# ---- sensibilidad de datos
for clave_u, ym_ini in [("sp500tr", (1995, 1)), ("fix", (1995, 1)), ("mxnx", (2005, 1)),
                        ("senal_precio", (1995, 1)), ("div_neto30", (1995, 1))]:
    for modo in ("T0", "T1"):
        for sig in ("usd", "mxn"):
            correr(f"sma10_{sig}_{modo}|{clave_u}", U[clave_u], modo, sig, 10, es_prueba=False, ym_ini=ym_ini,
                   parametros={"n": 10, "senal": sig, "ejecucion": modo, "datos": clave_u}, nota="sens. datos")
        if clave_u != "senal_precio":
            correr(f"bh_{modo}|{clave_u}", U[clave_u], modo, "bh", 0, es_prueba=False, ym_ini=ym_ini,
                   parametros={"ejecucion": modo, "datos": clave_u}, nota="sens. datos")
for modo in ("T0", "T1"):
    for sig in ("usd", "mxn"):
        correr(f"sma10_{sig}_{modo}|cetes_por_periodo", ub, modo, sig, 10, es_prueba=False,
               cetes_r=cetes_r_por_periodo,
               parametros={"n": 10, "senal": sig, "ejecucion": modo, "efectivo": "cetes_por_periodo"},
               nota="sens. datos")
    correr(f"bh_{modo}|cetes_por_periodo", ub, modo, "bh", 0, es_prueba=False, cetes_r=cetes_r_por_periodo,
           parametros={"ejecucion": modo, "efectivo": "cetes_por_periodo"}, nota="sens. datos")
# ---- corrida aislada 2008-01 a 2026-08 (entra desde cero)
for modo in ("T0", "T1"):
    for sig in ("usd", "mxn"):
        correr(f"sma10_{sig}_{modo}|aislada2008", ub, modo, sig, 10, es_prueba=False, ym_ini=(2008, 1),
               cortar=False, parametros={"n": 10, "senal": sig, "ejecucion": modo, "aislada": "2008-01"},
               nota="corrida aislada")
    correr(f"bh_{modo}|aislada2008", ub, modo, "bh", 0, es_prueba=False, ym_ini=(2008, 1), cortar=False,
           parametros={"ejecucion": modo, "aislada": "2008-01"}, nota="corrida aislada")
# ---- busqueda de origen (no es evidencia)
for modo in ("T0", "T1"):
    for sig in ("usd", "mxn"):
        correr(f"sma10_{sig}_{modo}|hist2008", ub, modo, sig, 10, es_prueba=False, ym_ini=(2008, 11),
               hist_desde=(2008, 1), cortar=False,
               parametros={"n": 10, "senal": sig, "ejecucion": modo, "historia_desde": "2008-01"},
               nota="busqueda de origen")
    correr(f"bh_{modo}|hist2008", ub, modo, "bh", 0, es_prueba=False, ym_ini=(2008, 11), cortar=False,
           parametros={"ejecucion": modo, "ventana": "2008-11"}, nota="busqueda de origen")
    correr(f"sma10_mxn_{modo}|spymx_hist2008", U["spymx"], modo, "mxn", 10, es_prueba=False,
           ym_ini=(2008, 11), cortar=False,
           parametros={"n": 10, "senal": "mxn", "ejecucion": modo, "activo": "SPY.MX adjclose"},
           nota="busqueda de origen")
    correr(f"bh_{modo}|spymx_hist2008", U["spymx"], modo, "bh", 0, es_prueba=False, ym_ini=(2008, 11),
           cortar=False, parametros={"ejecucion": modo, "activo": "SPY.MX adjclose"}, nota="busqueda de origen")

R["controles"]["motor_vs_simulador_propio_dif_max"] = DIF_MOTOR[0]
R["controles"]["nw_vs_matriz_bartlett_dif_max"] = DIF_NW[0]


# ---- pruebas NW: SMA - comprar y mantener (mismos periodos)
def dif_sma_bh(v_sma, v_bh):
    a, b = CORRIDAS[v_sma], CORRIDAS[v_bh]
    if a["res"].fechas != b["res"].fechas:
        detener("fechas distintas en la diferencia")
    x = [p - q for p, q in zip(a["res"].r_neto, b["res"].r_neto)]
    corte = a["corte"]
    i = bisect.bisect_right(a["res"].fechas, corte)
    return {"1995-2026": prueba(x, f"{v_sma} - {v_bh}, completo"),
            "1995-2007": prueba(x[:i], f"{v_sma} - {v_bh}, 1995-2007"),
            "2008-2026": prueba(x[i:], f"{v_sma} - {v_bh}, 2008-2026")}


pruebas_b = {}
for modo in ("T1", "T0"):
    for sig in ("mxn", "usd"):
        pruebas_b[f"sma10_{sig}_{modo}"] = dif_sma_bh(f"sma10_{sig}_{modo}", f"bh_{modo}")
# ---- Sharpe deflactado (N = 16 registradas)
dsr = {}
for seg in NOMBRES_SEG:
    dsr[seg] = {}
    for var in ("sma10_mxn_T1", "sma10_mxn_T0", "sma10_usd_T1", None):
        d = bt.sharpe_deflactado_de_registro(ID, segmento=seg, variante=var, dir_replicas=AQUI)
        dsr[seg][var or "mejor"] = d
    dsr[seg]["N100_sma10_mxn_T1"] = bt.sharpe_deflactado_de_registro(ID, n_pruebas=100, segmento=seg,
                                                                      variante="sma10_mxn_T1", dir_replicas=AQUI)

# ---- A5: comparacion con las cifras recibidas
comp_a5 = []
for v_sma, v_bh in [("sma10_mxn_T0", "bh_T0"), ("sma10_mxn_T1", "bh_T1"),
                    ("sma10_mxn_T0|aislada2008", "bh_T0|aislada2008"),
                    ("sma10_mxn_T1|aislada2008", "bh_T1|aislada2008"),
                    ("sma10_mxn_T0|hist2008", "bh_T0|hist2008"), ("sma10_mxn_T1|hist2008", "bh_T1|hist2008"),
                    ("sma10_mxn_T0|spymx_hist2008", "bh_T0|spymx_hist2008"),
                    ("sma10_mxn_T1|spymx_hist2008", "bh_T1|spymx_hist2008")]:
    sg = "2008-2026" if "2008-2026" in CORRIDAS[v_sma]["resumen"]["segmentos"] else "completo"
    a = CORRIDAS[v_sma]["resumen"]["segmentos"][sg]
    b = CORRIDAS[v_bh]["resumen"]["segmentos"][sg]
    comp_a5.append({
        "sma": v_sma, "bh": v_bh, "segmento": sg, "desde": a["desde"], "hasta": a["hasta"],
        "cagr_sma": a["cagr"], "cagr_bh": b["cagr"], "mdd_sma": a["mdd"], "mdd_bh": b["mdd"],
        "ok_cagr_sma": abs(a["cagr"] - AFIRMACIONES["A5_sma_mxn_cagr"]) <= TOL_CAGR,
        "ok_cagr_bh": abs(b["cagr"] - AFIRMACIONES["A5_bh_cagr"]) <= TOL_CAGR,
        "ok_mdd_sma": abs(a["mdd"] - AFIRMACIONES["A5_sma_mxn_mdd"]) <= TOL_PCT,
        "ok_mdd_bh": abs(b["mdd"] - AFIRMACIONES["A5_bh_mdd"]) <= TOL_PCT})

R["A5"] = {"corridas": {k: v["resumen"] for k, v in CORRIDAS.items()},
           "pruebas_nw_sma_menos_bh": pruebas_b, "dsr": dsr, "comparacion_con_afirmacion": comp_a5,
           "n_variantes_prueba": sum(1 for v in CORRIDAS.values() if v["resumen"]["es_prueba"]),
           "n_corridas_totales": len(CORRIDAS)}

# =============================================================== 6. dictamen de A1-A4
w1 = tabla_a


def ok(x, obj, tol):
    return x is not None and abs(x - obj) <= tol


dictamen = {
    "A1": {"W1": w1["SP_MXN_SPY_DEX"]["W1"]["cagr"],
           "reproduce_W1": ok(w1["SP_MXN_SPY_DEX"]["W1"]["cagr"], 0.145, TOL_CAGR),
           "ventanas_que_reproducen": [w for w in VENTANAS if ok(w1["SP_MXN_SPY_DEX"][w]["cagr"], 0.145, TOL_CAGR)],
           "inicios_que_reproducen": [x["inicio"] for x in sens_inicio["SP_MXN_SPY_DEX"]["filas"]
                                      if ok(x["cagr"], 0.145, TOL_CAGR)]},
    "A2": {"W1": w1["NAFTRAC_ADJ"]["W1"]["cagr"],
           "reproduce_W1": ok(w1["NAFTRAC_ADJ"]["W1"]["cagr"], 0.063, TOL_CAGR),
           "ventanas_que_reproducen": [w for w in VENTANAS if ok(w1["NAFTRAC_ADJ"][w]["cagr"], 0.063, TOL_CAGR)]},
    "A3": {"W1": w1["CETES28"]["W1"]["cagr"],
           "reproduce_W1": ok(w1["CETES28"]["W1"]["cagr"], 0.061, TOL_CAGR),
           "ventanas_que_reproducen": [w for w in VENTANAS if ok(w1["CETES28"][w]["cagr"], 0.061, TOL_CAGR)]},
    "A4": {"47_usd": R["A4"]["coincide_47_usd"], "21.6_mxn": R["A4"]["coincide_21.6_mxn"]},
    "A5": [x for x in comp_a5 if x["ok_cagr_sma"] and x["ok_cagr_bh"] and x["ok_mdd_sma"] and x["ok_mdd_bh"]],
}
R["dictamen"] = dictamen


# =============================================================== 7. salida
def limpiar(o):
    if isinstance(o, dict):
        return {str(k): limpiar(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [limpiar(v) for v in o]
    if isinstance(o, float):
        return None if not math.isfinite(o) else round(o, 12)
    if isinstance(o, date):
        return o.isoformat()
    return o


with open(os.path.join(AQUI, "resultados.json"), "w", encoding="utf-8") as f:
    json.dump(limpiar(R), f, indent=1, ensure_ascii=False, sort_keys=True)


def pct(x, d=2):
    return "n/d" if x is None else f"{100 * x:.{d}f}%"


print("== Controles ==")
print(json.dumps(limpiar(R["controles"]), indent=1))
print("\n== A1-A3: CAGR por ventana (sin costos ni impuestos) ==")
print("| Serie | " + " | ".join(VENTANAS) + " |")
for s in SERIES_A:
    celdas = []
    for w in VENTANAS:
        x = tabla_a[s][w]
        celdas.append("n/d" if x is None else f"{pct(x['cagr'])} ({x['desde']}→{x['hasta']}{', ' + x['nota'] if x['nota'] else ''})")
    print(f"| {S[s].nombre} | " + " | ".join(celdas) + " |")
print("\nSensibilidad de inicio (fin 2026-08-31):")
for s, x in sens_inicio.items():
    print(f"  {s}: min {pct(x['min'])} ({x['inicio_min']}), max {pct(x['max'])} ({x['inicio_max']})")
    print("   ", "; ".join(f"{f['inicio']}: {pct(f['cagr'])}" for f in x["filas"] if f["inicio"].endswith(("-06", "-12", "-09", "-03"))))
print("Sensibilidad de fin (inicio 2007-12-31):")
for s, x in sens_fin.items():
    print(f"  {s}: " + "; ".join(f"{k}: {pct(v['cagr'])}" for k, v in x.items() if v))
print(f"CETES particion mensual W1: {pct(cetes_mensual_w1)}; IMF {cetes_imf}")
print("\nNAFTRAC por anio (adj, close, dividendo implicito, ^MXX, eventos Yahoo):")
for x in naftrac_anual:
    print(f"  {x['anio']}: adj {pct(x['adj'])} close {pct(x['close'])} div {pct(x['div_implicito'])} "
          f"MXX {pct(x['mxx_precio'])} eventos {x['eventos_div_yahoo']}")
print("\nPruebas NW (A):")
for p in pruebas_a:
    print(f"  {p['prueba']}: n={p['n']} media {p['media_pct_mes']:.3f}%/mes x12 {p['x12_pct']:.2f}% "
          f"t={p['t_nw6']:.2f} IC [{p['ic95_pct_mes'][0]:.3f}, {p['ic95_pct_mes'][1]:.3f}] {p['veredicto']}")
print("Amortiguador:", json.dumps(limpiar(amortiguador), indent=1))
print("Conversion SIC:", json.dumps(limpiar(conv), indent=1))
print("\n== A4: 2008 ==")
for s, med in a4.items():
    print(f"  {S[s].nombre}:")
    for k, x in med.items():
        if isinstance(x, dict):
            print(f"     {k}: {pct(x['valor'])} ({x['pico']} → {x['valle']})")
        else:
            print(f"     {k}: {pct(x)}")
print("  coincide 47% USD:", R["A4"]["coincide_47_usd"])
print("  coincide 21.6% MXN:", R["A4"]["coincide_21.6_mxn"])
print("\n== A5: corridas (segmento 2008-2026 si existe; si no, completo) ==")
print("| Variante | prueba | desde | hasta | CAGR | Vol | Sharpe | MDD | invertido | cambios | costo/año |")
for k, v in CORRIDAS.items():
    segs = v["resumen"]["segmentos"]
    for sg in (["1995-2007", "2008-2026", "completo"] if "2008-2026" in segs else ["completo"]):
        x = segs[sg]
        print(f"| {k} [{sg}] | {int(v['resumen']['es_prueba'])} | {x['desde']} | {x['hasta']} | {pct(x['cagr'])} | "
              f"{pct(x['vol_anual'])} | {x['sharpe']:.3f} | {pct(x['mdd'])} | {pct(x['tiempo_invertido'], 1)} | "
              f"{x['n_cambios_senal']} | {pct(x['costo_anual'], 3)} |")
print("\nPruebas NW SMA10 - comprar y mantener:")
for k, v in pruebas_b.items():
    for sg, p in v.items():
        print(f"  {k} {sg}: n={p['n']} media {p['media_pct_mes']:.3f}%/mes x12 {p['x12_pct']:.2f}% t={p['t_nw6']:.2f} "
              f"IC [{p['ic95_pct_mes'][0]:.3f}, {p['ic95_pct_mes'][1]:.3f}] {p['veredicto']}")
print("\nDSR:")
for seg, x in dsr.items():
    for var, d in x.items():
        print(f"  {seg} {var}: variante={d['variante']} DSR={d['dsr']:.4f} N={d['n_pruebas']} "
              f"SR_anual={d['sr_anual']:.3f} SR0_anual={d['sr0_anual']:.3f} PSR={d['psr_sin_deflactar']:.4f}")
print("\nA5 contra la afirmacion:")
for x in comp_a5:
    print(f"  {x['sma']} vs {x['bh']} [{x['segmento']} {x['desde']}→{x['hasta']}]: SMA {pct(x['cagr_sma'])} / "
          f"{pct(x['mdd_sma'])}; B&H {pct(x['cagr_bh'])} / {pct(x['mdd_bh'])}; "
          f"ok={x['ok_cagr_sma']},{x['ok_cagr_bh']},{x['ok_mdd_sma']},{x['ok_mdd_bh']}")
print("\nDictamen:", json.dumps(limpiar({k: v for k, v in dictamen.items() if k != "A5"}), indent=1))
print("A5 reproducen:", [x["sma"] for x in dictamen["A5"]])
print(f"\nVariantes de prueba registradas: {R['A5']['n_variantes_prueba']}; corridas totales: {R['A5']['n_corridas_totales']}")
