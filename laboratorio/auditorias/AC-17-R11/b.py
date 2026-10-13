#!/usr/bin/env python3
"""AC-17-R11, ejecucion B (independiente). Biblioteca estandar solamente.

Banda de -3% en la salida del filtro SMA200 + VIX sobre un 3x diario sintetico del S&P 500.

Fuentes B (distintas a las de A, que usa Yahoo ^GSPC / ^SP500TR / ^VIX):
  - S&P 500 precio (senal y rendimiento de precio): CBOE SPX_History.csv (cdn-api.cboe.com)
    verificado contra FRED SP500 en el tramo comun (2016-10 a hoy).
  - Dividendos: rendimiento por dividendo mensual del S&P 500 de multpl.com (tabla por mes);
    total return aproximado = r_precio + yield_mes/252.
  - VIX: CBOE VIX_History.csv (historia oficial).
  - rf: FRED DTB3 (mismo que A; no hay alternativa diaria razonable).
  - Sensibilidad 2009-07+: Yahoo UPRO adjclose (chart v8).

Uso: python3 -I b.py [ruta_datos]
"""
import csv
import datetime as dt
import hashlib
import json
import math
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "datos")
COSTO = 0.0010          # por lado
GASTO_UPRO = 0.0091     # anual
DPA = 252               # dias por anio para rf, gasto y dividendo diario


def sha(fn):
    return hashlib.sha256(open(fn, "rb").read()).hexdigest()


def p(nombre):
    return os.path.join(DATOS, nombre)


# ---------------------------------------------------------------- carga
def leer_cboe(fn, col):
    out = {}
    with open(fn, newline="") as f:
        for r in csv.DictReader(f):
            try:
                d = dt.datetime.strptime(r["DATE"], "%m/%d/%Y").date()
                v = float(r[col])
            except (ValueError, KeyError):
                continue
            if v > 0:
                out[d] = v
    return out


def leer_fred(fn, col):
    out = {}
    with open(fn, newline="") as f:
        for r in csv.DictReader(f):
            v = r[col].strip()
            if v in ("", "."):
                continue
            out[dt.date.fromisoformat(r["observation_date"])] = float(v)
    return out


def leer_multpl(fn):
    h = open(fn, encoding="utf-8").read()
    filas = re.findall(r"<tr[^>]*>\s*<td>([^<]*)</td>\s*<td>(.*?)</td>", h, re.S)
    out = {}
    for fecha, val in filas:
        val = re.sub(r"<[^>]+>|&#x2002;|&#x2009;|\s|†|%", "", val)
        try:
            d = dt.datetime.strptime(fecha.strip(), "%b %d, %Y").date()
            out[(d.year, d.month)] = float(val) / 100.0
        except ValueError:
            continue
    return out


def leer_yahoo_adj(fn):
    j = json.load(open(fn))["chart"]["result"][0]
    off = j["meta"].get("gmtoffset", 0)
    ac = j["indicators"]["adjclose"][0]["adjclose"]
    out = {}
    for t, v in zip(j["timestamp"], ac):
        if v is not None:
            out[dt.datetime.utcfromtimestamp(t + off).date()] = v
    return out


spx = leer_cboe(p("SPX_History_cboe.csv"), "SPX")
vix = leer_cboe(p("VIX_History.csv"), "CLOSE")
fred_spx = leer_fred(p("SP500_fred.csv"), "SP500")
dtb3 = leer_fred(p("DTB3.csv"), "DTB3")
dy = leer_multpl(p("multpl_sp500_dividend_yield_by_month.html"))
upro = leer_yahoo_adj(p("UPRO_yahoo_chart.json"))

# Contraste CBOE vs FRED en el tramo comun; se corrige con FRED cualquier diferencia > 0.1 %.
correcciones = []
for d, v in fred_spx.items():
    if d in spx and abs(spx[d] / v - 1) > 0.001:
        correcciones.append((d.isoformat(), spx[d], v))
        spx[d] = v

# SMA200 sobre todos los cierres del SPX (CBOE desde 1975)
fechas_spx = sorted(spx)
sma = {}
ventana = []
suma = 0.0
for d in fechas_spx:
    ventana.append(spx[d]); suma += spx[d]
    if len(ventana) > 200:
        suma -= ventana.pop(0)
    if len(ventana) == 200:
        sma[d] = suma / 200.0

# Panel: dias con SPX, SMA200 y VIX desde 1990-01-02
INICIO = dt.date(1990, 1, 2)
panel = [d for d in fechas_spx if d >= INICIO and d in sma and d in vix]
desc_sin_vix = [d.isoformat() for d in fechas_spx if d >= INICIO and d not in vix]
desc_vix_sin_spx = sorted(d.isoformat() for d in vix if d >= INICIO and d not in spx)

# rf: DTB3 del ultimo dia habil disponible ANTES de t (forward-fill)
fechas_rf = sorted(dtb3)


def rf_previa(d, _cache={"i": 0}):
    i = _cache["i"]
    while i + 1 < len(fechas_rf) and fechas_rf[i + 1] < d:
        i += 1
    _cache["i"] = i
    return dtb3[fechas_rf[i]] / 100.0


falta_dy = set()


def yield_mes(d):
    k = (d.year, d.month)
    if k in dy:
        return dy[k]
    falta_dy.add(k)
    # mes anterior disponible
    y, m = k
    for _ in range(24):
        m -= 1
        if m == 0:
            y, m = y - 1, 12
        if (y, m) in dy:
            return dy[(y, m)]
    raise KeyError(k)


# Rendimientos diarios (cierre panel[i-1] -> panel[i])
r_tr, r_px, rf_d, r3x = [None], [None], [None], [None]
for i in range(1, len(panel)):
    d0, d1 = panel[i - 1], panel[i]
    rp = spx[d1] / spx[d0] - 1.0
    rt = rp + yield_mes(d1) / DPA
    rf = rf_previa(d1) / DPA
    r_px.append(rp); r_tr.append(rt); rf_d.append(rf)
    r3x.append(3 * rt - 2 * rf - GASTO_UPRO / DPA)


# ---------------------------------------------------------------- reglas
def senales(banda, usar_vix):
    """Estado deseado al cierre t (1 = dentro). Histeresis: salida y entrada distintas."""
    est = []
    s = 0
    for d in panel:
        c, m, v = spx[d], sma[d], vix[d]
        vix_mal = usar_vix and v >= 25
        if s == 1:
            if c < m * (1 - banda) or vix_mal:
                s = 0
        else:
            if c > m and not vix_mal:
                s = 1
        est.append(s)
    return est


def simular(est, r_activo):
    """Senal al cierre t, ejecucion al cierre t+1 -> el rendimiento del dia t+2 usa est[t].
    Costo COSTO al cierre del dia en que se ejecuta el cambio. Fuera: rf.
    Devuelve listas por dia i>=2: rendimiento neto, posicion, salida_ejecutada."""
    rets, pos, salidas = [], [], []
    for i in range(2, len(panel)):
        x = est[i - 2]
        r = r_activo[i] if x == 1 else rf_d[i]
        # cambio ejecutado al cierre del dia i (senal del cierre i-1)
        nuevo = est[i - 1]
        sal = 0
        if nuevo != x:
            r = (1 + r) * (1 - COSTO) - 1
            sal = 1 if (x == 1 and nuevo == 0) else 0
        rets.append(r); pos.append(x); salidas.append(sal)
    return rets, pos, salidas


def comprar_mantener(r_activo):
    rets = []
    for i in range(2, len(panel)):
        r = r_activo[i]
        if i == 2:  # compra al cierre del dia 1 (mismo arranque que las reglas)
            r = (1 + r) * (1 - COSTO) - 1
        rets.append(r)
    return rets, [1] * len(rets), [0] * len(rets)


FECHAS_R = panel[2:]
RF_R = rf_d[2:]


def metricas(rets, pos, sal, desde, hasta):
    idx = [k for k, d in enumerate(FECHAS_R) if desde <= d <= hasta]
    if not idx:
        return None
    a, b = idx[0], idx[-1]
    rr = rets[a:b + 1]
    ex = [r - f for r, f in zip(rr, RF_R[a:b + 1])]
    eq, pico, mdd = 1.0, 1.0, 0.0
    f_pico = f_valle = f_pico_mdd = FECHAS_R[a]
    for k, r in enumerate(rr):
        eq *= 1 + r
        if eq > pico:
            pico, f_pico = eq, FECHAS_R[a + k]
        if eq / pico - 1 < mdd:
            mdd, f_valle, f_pico_mdd = eq / pico - 1, FECHAS_R[a + k], f_pico
    d_ini = panel[panel.index(FECHAS_R[a]) - 1]
    anios = (FECHAS_R[b] - d_ini).days / 365.25
    n = len(rr)
    mu = sum(ex) / n
    sd = math.sqrt(sum((x - mu) ** 2 for x in ex) / (n - 1))
    m_r = sum(rr) / n
    sd_r = math.sqrt(sum((x - m_r) ** 2 for x in rr) / (n - 1))
    return {
        "desde": FECHAS_R[a].isoformat(), "hasta": FECHAS_R[b].isoformat(), "dias": n,
        "CAGR": eq ** (1 / anios) - 1,
        "vol": sd_r * math.sqrt(DPA),
        "sharpe": mu / sd * math.sqrt(DPA),
        "MDD": mdd, "MDD_pico": f_pico_mdd.isoformat(), "MDD_valle": f_valle.isoformat(),
        "salidas": sum(sal[a:b + 1]),
        "invertido": sum(pos[a:b + 1]) / n,
    }


CONFIGS = [
    ("banda3_vix (principal)", 0.03, True),
    ("sinbanda_vix (comparacion)", 0.00, True),
    ("banda3_sinvix (variante)", 0.03, False),
    ("banda5_vix (variante)", 0.05, True),
]
FIN = panel[-1]
PERIODOS = [
    ("completo", dt.date(1990, 1, 1), FIN),
    ("1990-2008", dt.date(1990, 1, 1), dt.date(2008, 12, 31)),
    ("2009-07-hoy", dt.date(2009, 7, 1), FIN),
]

res = {}
series = {}
for nombre, banda, uv in CONFIGS:
    est = senales(banda, uv)
    series[nombre] = (est, simular(est, r3x))
series["comprar_mantener_3x"] = (None, comprar_mantener(r3x))
series["comprar_mantener_1x_TR (referencia)"] = (None, comprar_mantener(r_tr))

for nombre, (_, (rets, pos, sal)) in series.items():
    res[nombre] = {per: metricas(rets, pos, sal, a, b) for per, a, b in PERIODOS}

# Sensibilidad: UPRO real en 2009-07-hoy (adjclose Yahoo), mismas senales
r_upro = [None]
faltan_upro = 0
for i in range(1, len(panel)):
    d0, d1 = panel[i - 1], panel[i]
    if d0 in upro and d1 in upro:
        r_upro.append(upro[d1] / upro[d0] - 1)
    else:
        r_upro.append(r3x[i])  # antes de UPRO: sintetico (no se reporta)
        if d1 >= dt.date(2009, 7, 1):
            faltan_upro += 1
sens = {}
for nombre, banda, uv in CONFIGS:
    est = series[nombre][0]
    rets, pos, sal = simular(est, r_upro)
    sens[nombre] = metricas(rets, pos, sal, dt.date(2009, 7, 1), FIN)
rets, pos, sal = comprar_mantener(r_upro)
# comprar y mantener UPRO desde 2009-07 (el costo de entrada se cobra en 1990 en la serie; se ignora aqui)
sens["comprar_mantener_UPRO"] = metricas(rets, pos, sal, dt.date(2009, 7, 1), FIN)

# Seguimiento sintetico vs UPRO
pares = [(r3x[i], r_upro[i]) for i in range(1, len(panel))
         if panel[i] >= dt.date(2009, 7, 1) and panel[i - 1] in upro and panel[i] in upro]
e_s = math.prod(1 + a for a, _ in pares); e_u = math.prod(1 + b for _, b in pares)
anios_u = len(pares) / DPA
seguimiento = {"dias": len(pares), "CAGR_sintetico": e_s ** (1 / anios_u) - 1,
               "CAGR_UPRO": e_u ** (1 / anios_u) - 1}


# ---------------------------------------------------------------- salida
def fmt(m):
    return (f"{m['CAGR']*100:7.2f}% {m['vol']*100:6.1f}% {m['sharpe']:6.2f} "
            f"{m['MDD']*100:7.1f}% {m['salidas']:5d} {m['invertido']*100:6.1f}%")


print("Huellas sha256:")
for fn in sorted(os.listdir(DATOS)):
    print(f"  {sha(p(fn))}  {fn}")
print(f"\nPanel: {panel[0]} a {panel[-1]}, {len(panel)} dias; rendimientos desde {FECHAS_R[0]} ({len(FECHAS_R)} dias)")
print(f"Dias SPX sin VIX descartados: {desc_sin_vix}")
print(f"Dias VIX sin SPX (feriados) ignorados: {len(desc_vix_sin_spx)}")
print(f"Correcciones SPX CBOE con FRED: {correcciones}")
print(f"Meses sin yield multpl (se usa el previo): {sorted(falta_dy)}")
print(f"Dias 2009-07+ sin UPRO: {faltan_upro}")
for per, _, _ in PERIODOS:
    print(f"\n== {per} ==")
    print(f"{'config':38s} {'CAGR':>8s} {'vol':>7s} {'Sharpe':>6s} {'MDD':>8s} {'sal':>5s} {'inv':>7s}")
    for nombre in res:
        print(f"{nombre:38s} {fmt(res[nombre][per])}")
print("\n== Sensibilidad UPRO real 2009-07-hoy ==")
for nombre, m in sens.items():
    print(f"{nombre:38s} {fmt(m)}")
print(f"\nSeguimiento 2009-07+: {seguimiento}")

# Criterio de refutacion (seccion 2)
P, S = "banda3_vix (principal)", "sinbanda_vix (comparacion)"
c = res[P]["completo"]; s = res[S]["completo"]
reduce = c["salidas"] < s["salidas"]
mdd_ok = (s["MDD"] - c["MDD"]) <= 0.05
sh_ok = (c["sharpe"] - s["sharpe"]) >= -0.05
signo = math.copysign(1, c["sharpe"] - s["sharpe"])
inversiones = []
for per in ("1990-2008", "2009-07-hoy"):
    dif = res[P][per]["sharpe"] - res[S][per]["sharpe"]
    if math.copysign(1, dif) != signo:
        inversiones.append((per, round(dif, 3)))
dif_upro = sens[P]["sharpe"] - sens[S]["sharpe"]
if not (reduce and mdd_ok and sh_ok):
    estado = "No replicado"
elif inversiones:
    estado = "Replicado con diferencias"
else:
    estado = "Replicado"
print("\nCriterio §2 (periodo completo, banda3_vix vs sinbanda_vix):")
print(f"  salidas {c['salidas']} vs {s['salidas']} -> reduce: {reduce}")
print(f"  MDD {c['MDD']*100:.1f}% vs {s['MDD']*100:.1f}% -> empeora <=5pp: {mdd_ok}")
print(f"  Sharpe {c['sharpe']:.3f} vs {s['sharpe']:.3f} (dif {c['sharpe']-s['sharpe']:+.3f}) -> baja <=0.05: {sh_ok}")
print(f"  Subperiodos con signo invertido en Sharpe: {inversiones}")
for per in ("1990-2008", "2009-07-hoy"):
    print(f"  {per}: dif Sharpe {res[P][per]['sharpe']-res[S][per]['sharpe']:+.4f}, "
          f"salidas {res[P][per]['salidas']} vs {res[S][per]['salidas']}, "
          f"MDD {res[P][per]['MDD']*100:.1f}% vs {res[S][per]['MDD']*100:.1f}%")
print(f"  Sensibilidad UPRO 2009-07+: dif Sharpe {dif_upro:+.4f}")
print("\nMDD (pico -> valle), periodo completo:")
for nombre in res:
    m = res[nombre]["completo"]
    print(f"  {nombre:38s} {m['MDD']*100:6.1f}%  {m['MDD_pico']} -> {m['MDD_valle']}")
print(f"  ESTADO B: {estado}")

json.dump({"resultados": res, "sensibilidad_upro": sens, "seguimiento": seguimiento,
           "estado": estado, "inversiones": inversiones, "correcciones": correcciones,
           "descartados_sin_vix": desc_sin_vix,
           "huellas": {fn: sha(p(fn)) for fn in sorted(os.listdir(DATOS))}},
          open(os.path.join(AQUI, "b-resultados.json"), "w"), indent=1, default=str)
