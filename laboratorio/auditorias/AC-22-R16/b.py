"""AC-22-R16, ejecución B independiente (desde cero, solo biblioteca estándar).

Pre-registro: laboratorio/replicas/R16-stop-fijo-upro.md (commit c067ef6).
Datos B: CBOE SPX (señal y precio), multpl (yield mensual de dividendos -> TR aproximado),
CBOE VIX (con contraste FRED VIXCLS si existe), FRED DTB3 (rf).
Uso: python3 -I b.py  (lee ./datos relativo a este archivo)
"""
import csv, json, math, os, re, sys, datetime as dt

AQUI = os.path.dirname(os.path.abspath(__file__))
DAT = os.path.join(AQUI, "datos")
FIN = dt.date(2026, 10, 16)
COSTO = 0.001
GASTO = 0.0091
STOPS = [("S8", 0.08), ("S10.92", 0.1092), ("S15", 0.15), ("S20", 0.20)]
OUT = []


def p(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s)


# ---------- carga ----------
def leer_cboe(nombre, col):
    d = {}
    with open(os.path.join(DAT, nombre)) as f:
        for r in csv.DictReader(f):
            m, dd, y = r["DATE"].split("/")
            v = r[col].strip()
            if v:
                d[dt.date(int(y), int(m), int(dd))] = float(v)
    return d


def leer_fred(nombre):
    d = {}
    ruta = os.path.join(DAT, nombre)
    if not os.path.exists(ruta):
        return None
    with open(ruta) as f:
        rd = csv.reader(f)
        next(rd)
        for r in rd:
            if len(r) < 2 or r[1] in ("", "."):
                continue
            d[dt.date.fromisoformat(r[0])] = float(r[1])
    return d


def leer_multpl():
    html = open(os.path.join(DAT, "multpl_sp500_dividend_yield_by_month.html"), encoding="utf-8").read()
    filas = re.findall(r"<td>\s*([A-Z][a-z]{2} \d{1,2}, \d{4})\s*</td>\s*<td>(.*?)</td>", html, re.S)
    y = {}
    for fecha, val in filas:
        f = dt.datetime.strptime(fecha, "%b %d, %Y").date()
        num = re.search(r"([\d.]+)%", val)
        if num and (f.year, f.month) not in y:
            y[(f.year, f.month)] = float(num.group(1)) / 100
    return y


spx = leer_cboe("SPX_History_cboe.csv", "SPX")
vix = leer_cboe("VIX_History.csv", "CLOSE")
# FRED no respondió el 2026-10-19: DTB3 es copia de la descarga de AC-17 (hasta 2026-10-08)
# y se completa con la tasa de descuento a 13 semanas del Tesoro (la misma que publica DTB3).
dtb3 = leer_fred("DTB3_fred_copia_AC17.csv")
_n_tes = 0
with open(os.path.join(DAT, "treasury_bill_rates_2026.csv")) as f:
    for r in csv.DictReader(f):
        m_, d_, y_ = r["Date"].split("/")
        fe = dt.date(int(y_), int(m_), int(d_))
        if fe in dtb3 and abs(dtb3[fe] - float(r["13 WEEKS BANK DISCOUNT"])) > 0.005:
            print("  aviso DTB3 != Tesoro", fe, dtb3[fe], r["13 WEEKS BANK DISCOUNT"])
        if fe not in dtb3:
            dtb3[fe] = float(r["13 WEEKS BANK DISCOUNT"]); _n_tes += 1
vixcls = leer_fred("VIXCLS.csv")
sp500f = leer_fred("SP500_fred_copia_AC17.csv")
dy = leer_multpl()

# ---------- panel (§7) ----------
dias_spx = sorted(d for d in spx if dt.date(1990, 1, 2) <= d <= FIN)
dias_vix = sorted(d for d in vix if dt.date(1990, 1, 2) <= d <= FIN)
sin_vix = [d for d in dias_spx if d not in vix]
sin_spx = [d for d in dias_vix if d not in spx]
dias = [d for d in dias_spx if d in vix]
p("AC-22-R16 ejecución B  |  panel común SPX(CBOE) y VIX(CBOE):", dias[0], "a", dias[-1], "n =", len(dias))
p("  días con SPX sin VIX descartados:", len(sin_vix), [str(x) for x in sin_vix])
p("  días con VIX sin SPX ignorados:", len(sin_spx))

# contrastes de fuente
if vixcls:
    com = [d for d in dias if d in vixcls]
    dif = [d for d in com if abs(vixcls[d] - vix[d]) > 0.015]
    p("  contraste VIX CBOE vs FRED VIXCLS: días comunes", len(com), "| difieren >0.015:", len(dif), [str(x) for x in dif[:8]])
if sp500f:
    com = [d for d in dias if d in sp500f]
    dif = [d for d in com if abs(sp500f[d] / spx[d] - 1) > 1e-4]
    p("  contraste SPX CBOE vs FRED SP500: días comunes", len(com), "| difieren >0.01%:", len(dif), [(str(x), spx[x], sp500f[x]) for x in dif[:5]])

px = [spx[d] for d in dias]
vx = [vix[d] for d in dias]
n = len(dias)

# rf diaria: último DTB3 publicado ANTES de t (rezago de 1 día), simple /252
rf_fechas = sorted(dtb3)
rf = [0.0] * n
j = 0
ult = None
for i, d in enumerate(dias):
    while j < len(rf_fechas) and rf_fechas[j] < d:
        ult = dtb3[rf_fechas[j]]
        j += 1
    rf[i] = (ult if ult is not None else 0.0) / 100 / 252
p("  rf: DTB3 (FRED, copia AC-17) + Tesoro 13 sem. para", _n_tes, "días posteriores")
p("  último DTB3 disponible:", rf_fechas[-1], "=", dtb3[rf_fechas[-1]])

# TR aproximado y 3x sintético (rendimiento del día i: cierre i-1 -> cierre i)
faltan_dy = set()
rtr = [0.0] * n
r3 = [0.0] * n
for i in range(1, n):
    k = (dias[i].year, dias[i].month)
    yv = dy.get(k)
    if yv is None:
        faltan_dy.add(k)
        yv = dy[max(x for x in dy if x <= k)]
    rtr[i] = px[i] / px[i - 1] - 1 + yv / 252
    r3[i] = 3 * rtr[i] - 2 * rf[i] - GASTO / 252
if faltan_dy:
    p("  meses sin yield de multpl (se usa el previo):", sorted(faltan_dy))

# SMA200 sobre cierres comunes; inicio = día con 200 cierres comunes (§6)
sma = [None] * n
s = 0.0
for i in range(n):
    s += px[i]
    if i >= 200:
        s -= px[i - 200]
    if i >= 199:
        sma[i] = s / 200
I0 = 199
p("  inicio de evaluación (200 cierres comunes):", dias[I0], "| primer rendimiento:", dias[I0 + 1])

# ---------- estado del filtro V0 (decidido al cierre de t) ----------
filtro = [False] * n  # estado deseado por el filtro al cierre de t
st = False
for i in range(I0, n):
    if st:
        if px[i] < sma[i] * 0.97 or vx[i] >= 25:
            st = False
    else:
        if px[i] > sma[i] and vx[i] < 25:
            st = True
    filtro[i] = st


# ---------- simulador ----------
def simular(stop=None, reentrada21=False):
    """Devuelve (rend diarios netos, en_mercado por día, salidas [(i, tipo)], entradas).
    Filtro: decidido al cierre t, ejecutado al cierre t+1.
    Stop: valor del 3x al cierre t <= nivel -> salida al cierre t.
    Tras stop: bloqueo hasta que el filtro esté apagado y vuelva a dar entrada
    (o, con reentrada21, a los 21 días hábiles si el filtro sigue encendido)."""
    pos = False
    bloqueado = False
    apagado_desde_stop = False
    dia_stop = None
    nivel = None
    v3 = 1.0  # índice del 3x
    rend = [0.0] * n
    dentro = [False] * n
    salidas = []
    entradas = 0
    for i in range(I0 + 1, n):
        # rendimiento del día i con la posición vigente desde el cierre i-1
        r = r3[i] if pos else rf[i]
        v3 *= 1 + r3[i]
        dentro[i] = pos
        eq = 1 + r
        # decisiones ejecutadas al cierre de i
        desea = filtro[i - 1]  # señal del cierre i-1 se ejecuta al cierre i
        if bloqueado:
            if not filtro[i - 1]:
                apagado_desde_stop = True
            if apagado_desde_stop and desea:
                bloqueado = False
            elif reentrada21 and desea and i - dia_stop >= 21:
                bloqueado = False
        if pos:
            if not desea:
                pos = False
                salidas.append((i, "filtro"))
                eq *= 1 - COSTO
            elif stop is not None and v3 <= nivel:
                pos = False
                salidas.append((i, "stop"))
                eq *= 1 - COSTO
                bloqueado = True
                apagado_desde_stop = False
                dia_stop = i
        else:
            if desea and not bloqueado and not (salidas and salidas[-1][0] == i):
                pos = True
                entradas += 1
                eq *= 1 - COSTO
                nivel = v3 * (1 - stop) if stop is not None else None
        rend[i] = eq - 1
    return rend, dentro, salidas, entradas


def bh():
    rend = [0.0] * n
    for i in range(I0 + 1, n):
        rend[i] = r3[i]
    rend[I0 + 1] = (1 + r3[I0 + 1]) * 1.0 - 1  # compra al cierre I0
    # costo de compra al cierre I0 se carga en el primer día
    rend[I0 + 1] = (1 - COSTO) * (1 + r3[I0 + 1]) - 1
    return rend


def metricas(rend, a, b, salidas=None, dentro=None):
    rs = rend[a:b + 1]
    ex = [rend[i] - rf[i] for i in range(a, b + 1)]
    eq = 1.0
    pico = 1.0
    mdd = 0.0
    for x in rs:
        eq *= 1 + x
        pico = max(pico, eq)
        mdd = min(mdd, eq / pico - 1)
    anios = (dias[b] - dias[a - 1]).days / 365.25
    cagr = eq ** (1 / anios) - 1
    m = sum(rs) / len(rs)
    vol = math.sqrt(sum((x - m) ** 2 for x in rs) / (len(rs) - 1)) * math.sqrt(252)
    me = sum(ex) / len(ex)
    se = math.sqrt(sum((x - me) ** 2 for x in ex) / (len(ex) - 1))
    sh = me / se * math.sqrt(252)
    out = {"cagr": cagr, "vol": vol, "sharpe": sh, "mdd": mdd}
    if salidas is not None:
        sal = [s for s in salidas if a <= s[0] <= b]
        out["salidas"] = len(sal)
        out["salidas_stop"] = sum(1 for s in sal if s[1] == "stop")
        out["invertido"] = sum(1 for i in range(a, b + 1) if dentro[i]) / (b - a + 1)
    else:
        out["salidas"] = 0
        out["salidas_stop"] = 0
        out["invertido"] = 1.0
    return out


def idx(fecha, desde=True):
    if desde:
        return next(i for i in range(I0 + 1, n) if dias[i] >= fecha)
    return max(i for i in range(I0 + 1, n) if dias[i] <= fecha)


PER = {
    "completo": (I0 + 1, n - 1),
    "1990-2008": (I0 + 1, idx(dt.date(2008, 12, 31), False)),
    "2009-hoy": (idx(dt.date(2009, 1, 1)), n - 1),
}

res = {}
corr = {}
corr["V0"] = simular(None)
for nom, s_ in STOPS:
    corr[nom] = simular(s_)
corr["S10.92-reent21"] = simular(0.1092, reentrada21=True)
rb = bh()
orden = ["V0", "S8", "S10.92", "S15", "S20", "S10.92-reent21", "BH3x"]
for per, (a, b) in PER.items():
    res[per] = {}
    for k in orden:
        if k == "BH3x":
            res[per][k] = metricas(rb, a, b)
        else:
            rr, de, sa, _ = corr[k]
            res[per][k] = metricas(rr, a, b, sa, de)

for per, (a, b) in PER.items():
    p("")
    p(f"=== {per}: {dias[a]} a {dias[b]} ({b - a + 1} rendimientos) ===")
    p(f"{'regla':<16}{'CAGR':>8}{'Vol':>8}{'Sharpe':>8}{'MDD':>9}{'sal':>5}{'stop':>5}{'inv':>7}")
    for k in orden:
        m = res[per][k]
        p(f"{k:<16}{m['cagr']*100:7.2f}%{m['vol']*100:7.1f}%{m['sharpe']:8.3f}{m['mdd']*100:8.1f}%{m['salidas']:5d}{m['salidas_stop']:5d}{m['invertido']*100:6.1f}%")

# ---------- H1 ----------
p("")
H1 = {}
for per in PER:
    v0 = res[per]["V0"]
    s = res[per]["S10.92"]
    dmdd = (s["mdd"] - v0["mdd"]) * 100  # positivo = mejora
    dsh = s["sharpe"] - v0["sharpe"]
    H1[per] = {"mejora_mdd_pp": dmdd, "delta_sharpe": dsh, "sostenida": dmdd >= 3 and dsh >= -0.03}
    p(f"H1 [{per}] S10.92 vs V0: mejora MDD = {dmdd:+.2f} pp (umbral +3), ΔSharpe = {dsh:+.3f} (umbral -0.03) -> {'SOSTENIDA' if H1[per]['sostenida'] else 'REFUTADA'}")

# ---------- H2 ----------
sal_v0 = [i for i, t in corr["V0"][2]]
stops = [i for i, t in corr["S10.92"][2] if t == "stop"]
red = 0
detalle = []
for i in stops:
    sig = [k for k in sal_v0 if i <= k <= i + 21]
    ok = bool(sig)
    red += ok
    sigv0 = next((k for k in sal_v0 if k >= i), None)
    detalle.append({"fecha_stop": str(dias[i]), "v0_sale": str(dias[sigv0]) if sigv0 else None,
                    "dias_habiles": (sigv0 - i) if sigv0 else None, "dentro_21": ok})
prop = red / len(stops) if stops else float("nan")
p(f"H2: salidas por stop de S10.92 = {len(stops)}; V0 sale en [0,21] días hábiles en {red} -> {prop*100:.1f}% (umbral 50%) -> {'SOSTENIDA' if prop >= 0.5 else 'REFUTADA'}")
for d_ in detalle:
    p(f"   stop {d_['fecha_stop']}  V0 sale {d_['v0_sale']}  (+{d_['dias_habiles']} dh)  {'<=21' if d_['dentro_21'] else '>21'}")

estado = "Replicado" if H1["completo"]["sostenida"] else "No replicado"
p("")
p(f"VEREDICTO (§2, periodo completo): H1 {'sostenida' if H1['completo']['sostenida'] else 'refutada'} -> estado '{estado}'. H2 informativa: {prop*100:.1f}%.")

json.dump({
    "ejecucion": "B", "auditoria": "AC-22-R16", "panel": [str(dias[I0 + 1]), str(dias[-1])],
    "fuentes": {"senal": "CBOE SPX", "tr": "CBOE SPX + multpl yield mensual/252", "vix": "CBOE VIX_History",
                "rf": "FRED DTB3"},
    "periodos": {k: [str(dias[a]), str(dias[b])] for k, (a, b) in PER.items()},
    "resultados": res, "H1": H1,
    "H2": {"n_stops": len(stops), "redundantes_21": red, "proporcion": prop, "detalle": detalle},
    "estado": estado,
}, open(os.path.join(AQUI, "b-resultados.json"), "w"), indent=1, ensure_ascii=False)
open(os.path.join(AQUI, "salida.txt"), "w").write("\n".join(OUT) + "\n")
