"""AC-24-R18 · Ejecución B independiente de R18 (escrita desde cero, solo biblioteca estándar).

Pregunta: probabilidad de que la mezcla SPYM/QQQM/UPRO-sintético(V0)/efectivo, rebalanceada
mensualmente, caiga >= 8% (y >= 12%) bajo su máximo desde t dentro de t+1..t+63.

Fuente B (distinta de A, que usa Yahoo):
  - S&P 500: CBOE SPX (precio) + rendimiento por dividendo mensual de multpl (TR aproximado).
  - VIX: CBOE VIX_History. Tasa: FRED DTB3 (copia AC-21) y, al final, el 13 semanas del Tesoro.
  - Nasdaq-100: FRED NASDAQ100 (precio, copia AC-21; FRED estaba en mantenimiento el 21-oct).
  - MXN (sensibilidad): FRED DEXMXUS (copia R15-datos).
Uso: python3 -I b.py <carpeta_datos> <salida_json>
"""
import csv, json, math, re, sys, datetime as dt

DATOS = sys.argv[1] if len(sys.argv) > 1 else "datos"
SALIDA = sys.argv[2] if len(sys.argv) > 2 else "b-resultados.json"
FIN = dt.date(2026, 10, 16)
H = 63
UMBRALES = (0.08, 0.12)
QQQM, CASH = 0.268, 0.053
VARIANTES = {"0%": 0.0, "13.5%": 0.135, "26.9% (vigente)": 0.269, "40%": 0.40}
GASTO_SPYM, GASTO_QQQM, GASTO_UPRO = 0.0002, 0.0015, 0.0091


def fecha_mdy(s):
    m, d, y = s.split("/")
    return dt.date(int(y), int(m), int(d))


def leer_cboe(nombre, col):
    out = {}
    with open(f"{DATOS}/{nombre}") as f:
        for r in csv.DictReader(f):
            try:
                v = float(r[col])
            except (ValueError, KeyError):
                continue
            if v > 0:
                out[fecha_mdy(r["DATE"])] = v
    return out


def leer_fred(nombre):
    out = {}
    with open(f"{DATOS}/{nombre}") as f:
        rd = csv.reader(f)
        next(rd)
        for d, v in rd:
            try:
                out[dt.date.fromisoformat(d)] = float(v)
            except ValueError:
                pass  # "." = sin dato
    return out


def leer_multpl():
    t = open(f"{DATOS}/multpl_sp500_dividend_yield_by_month.html", encoding="utf-8").read()
    filas = re.findall(r"<td>([A-Z][a-z]{2} \d{1,2}, \d{4})</td>\s*<td>(.*?)</td>", t, re.S)
    out = {}
    for d, v in filas:
        f = dt.datetime.strptime(d, "%b %d, %Y").date()
        y = float(re.search(r"([\d.]+)%", v).group(1)) / 100
        # Una entrada por mes; si hay dos (estimación a media fecha), se queda la de fin de mes.
        k = (f.year, f.month)
        if k not in out or f.day > out[k][0]:
            out[k] = (f.day, y)
    return {k: v[1] for k, v in out.items()}


def leer_tesoro_2026():
    out = {}
    with open(f"{DATOS}/treasury_bill_rates_2026.csv") as f:
        for r in csv.DictReader(f):
            out[fecha_mdy(r["Date"])] = float(r["13 WEEKS BANK DISCOUNT"])
    return out


spx = leer_cboe("SPX_History_cboe.csv", "SPX")
vix = leer_cboe("VIX_History.csv", "CLOSE")
ndx = leer_fred("NASDAQ100.csv")
tb = leer_fred("DTB3.csv")
for d, v in leer_tesoro_2026().items():
    tb.setdefault(d, v)  # solo rellena días que DTB3 no tiene (16-oct-2026)
dy = leer_multpl()
fx = leer_fred("DEXMXUS.csv")

# §7: se omiten los días sin dato en alguna serie.
dias = sorted(d for d in spx if d in vix and d in ndx and d in tb and d <= FIN)
n = len(dias)
S = [spx[d] for d in dias]
V = [vix[d] for d in dias]
N = [ndx[d] for d in dias]
# Días hábiles (lun-vie) en (d_{i-1}, d_i]: devengo de dividendo y de tasa si se omitió algún día.
DH = [1] + [sum(1 for k in range(1, (dias[i] - dias[i - 1]).days + 1)
                if (dias[i - 1] + dt.timedelta(k)).weekday() < 5) for i in range(1, n)]
RF = [tb[d] / 100 / 252 * DH[i] for i, d in enumerate(dias)]

# Rendimientos diarios (del cierre del día común previo al cierre de d).
r_tr = [None] * n
r_ndx = [None] * n
for i in range(1, n):
    y = dy[(dias[i].year, dias[i].month)]
    r_tr[i] = S[i] / S[i - 1] - 1 + y / 252 * DH[i]
    r_ndx[i] = N[i] / N[i - 1] - 1

# Filtro V0 con histéresis, sobre los días comunes; SMA200 desde 200 cierres comunes.
estado = [None] * n
on = None
suma = 0.0
for i in range(n):
    suma += S[i]
    if i >= 200:
        suma -= S[i - 200]
    if i < 199:
        continue
    sma = suma / 200
    if on is None:
        on = S[i] > sma and V[i] < 25
    elif on and (S[i] < sma * 0.97 or V[i] >= 25):
        on = False
    elif (not on) and S[i] > sma and V[i] < 25:
        on = True
    estado[i] = on

# §5: señal del cierre de t-2 aplicada al rendimiento del día t.
i0 = 199 + 2  # primer día con rendimiento y señal disponible
r_upro = [None] * n
for i in range(i0, n):
    if estado[i - 2]:
        r_upro[i] = 3 * r_tr[i] - 2 * RF[i] - GASTO_UPRO / 252 * DH[i]
    else:
        r_upro[i] = RF[i]
r_spym = [None if r is None else r_tr[i] - GASTO_SPYM / 252 * DH[i] for i, r in enumerate(r_tr)]
r_qqqm = [None if r is None else r_ndx[i] - GASTO_QQQM / 252 * DH[i] for i, r in enumerate(r_ndx)]


def curva(w_upro):
    w = {"spym": 1 - QQQM - CASH - w_upro, "qqqm": QQQM, "upro": w_upro, "cash": CASH}
    ret = {"spym": r_spym, "qqqm": r_qqqm, "upro": r_upro, "cash": RF}
    base = i0 - 1
    val = [1.0]
    hold = dict(w)
    for i in range(i0, n):
        if dias[i].month != dias[i - 1].month:  # rebalanceo al inicio de cada mes
            tot = sum(hold.values())
            hold = {k: tot * w[k] for k in w}
        for k in hold:
            hold[k] *= 1 + ret[k][i]
        val.append(sum(hold.values()))
    return dias[base:], val


def toques(fechas, val, desde=None, hasta=None, paso=1):
    """Fracción de días de inicio t (con ventana completa t+1..t+63) que tocan cada umbral."""
    res = {u: 0 for u in UMBRALES}
    m = len(val)
    cuenta = 0
    for t in range(0, m - H, paso):
        if desde and fechas[t] < desde:
            continue
        if hasta and fechas[t] > hasta:
            continue
        cuenta += 1
        pico = val[t]
        peor = 0.0
        for s in range(t + 1, t + H + 1):
            if val[s] > pico:
                pico = val[s]
            dd = val[s] / pico - 1
            if dd < peor:
                peor = dd
        for u in UMBRALES:
            if peor <= -u:
                res[u] += 1
    return {f"{int(u*100)}%": (res[u] / cuenta if cuenta else None) for u in UMBRALES}, cuenta


def stats(fechas, val):
    años = (fechas[-1] - fechas[0]).days / 365.25
    cagr = val[-1] ** (1 / años) - 1
    rs = [val[i] / val[i - 1] - 1 for i in range(1, len(val))]
    mu = sum(rs) / len(rs)
    vol = math.sqrt(sum((x - mu) ** 2 for x in rs) / (len(rs) - 1)) * math.sqrt(252)
    pico, mdd = val[0], 0.0
    for v in val:
        pico = max(pico, v)
        mdd = min(mdd, v / pico - 1)
    return {"cagr": cagr, "vol": vol, "mdd": mdd}


PER = {
    "completo": (None, None),
    "1990-2008": (None, dt.date(2008, 12, 31)),
    "2009-hoy": (dt.date(2009, 1, 1), None),
}
out = {"fuente": "B: CBOE SPX + multpl div, CBOE VIX, FRED DTB3 (+Tesoro 13s), FRED NASDAQ100, FRED DEXMXUS",
       "dias_comunes": n, "inicio_curva": str(dias[i0 - 1]), "fin": str(dias[-1]),
       "pct_dias_v0_encendido": sum(1 for i in range(i0, n) if estado[i - 2]) / (n - i0),
       "variantes": {}}
lineas = [f"Días comunes: {n} ({dias[0]} a {dias[-1]}); curva desde {dias[i0-1]}",
          f"V0 encendido: {out['pct_dias_v0_encendido']:.1%} de los días"]
for nombre, wu in VARIANTES.items():
    f, v = curva(wu)
    d = {"pesos": {"SPYM": round(1 - QQQM - CASH - wu, 4), "QQQM": QQQM, "UPRO": wu, "cash": CASH},
         "stats": stats(f, v), "prob": {}, "n_inicios": {}}
    for p, (a, b) in PER.items():
        d["prob"][p], d["n_inicios"][p] = toques(f, v, a, b)
    # Sensibilidad: ventanas sin traslape (cada 63 días) y en MXN desde 1994.
    d["prob"]["completo_sin_traslape"], d["n_inicios"]["completo_sin_traslape"] = toques(f, v, paso=H)
    fxv, ult = [], None
    fm, vm = [], []
    for x, y in zip(f, v):
        if x in fx:
            ult = fx[x]
        if ult is not None and x >= dt.date(1994, 1, 3):
            fm.append(x)
            vm.append(y * ult)
    d["prob"]["MXN_1994-hoy"], d["n_inicios"]["MXN_1994-hoy"] = toques(fm, vm)
    d["prob"]["USD_1994-hoy"], d["n_inicios"]["USD_1994-hoy"] = toques(f, v, dt.date(1994, 1, 3))
    out["variantes"][nombre] = d
    s = d["stats"]
    lineas.append(f"\nUPRO {nombre}: SPYM {d['pesos']['SPYM']:.3f} | CAGR {s['cagr']:.2%} vol {s['vol']:.2%} MDD {s['mdd']:.1%}")
    for p, pr in d["prob"].items():
        lineas.append(f"  {p:24s} P(>=8%) {pr['8%']:.1%}  P(>=12%) {pr['12%']:.1%}  (inicios {d['n_inicios'][p]})")

pv = out["variantes"]["26.9% (vigente)"]["prob"]["completo"]["8%"]
p135 = out["variantes"]["13.5%"]["prob"]["completo"]["8%"]
out["H1_prob_vigente_8"] = pv
out["H1_sostenida"] = pv <= 0.15
out["H2_reduccion_pp"] = (pv - p135) * 100
out["H2_sostenida"] = (pv - p135) >= 0.05
lineas.append(f"\nH1: P vigente = {pv:.1%} -> {'sostenida' if pv <= 0.15 else 'REFUTADA'} (umbral 15%)")
lineas.append(f"H2: reducción al bajar a 13.5% = {(pv-p135)*100:.1f} pp -> {'sostenida' if out['H2_sostenida'] else 'no sostenida'} (umbral 5 pp)")
print("\n".join(lineas))
json.dump(out, open(SALIDA, "w"), indent=2, ensure_ascii=False, default=str)
