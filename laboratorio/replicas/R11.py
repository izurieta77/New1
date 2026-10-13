"""R11 (ejecución A): banda de −3% en la salida del filtro de apalancados sobre un 3x sintético del S&P 500.
Pre-registro: R11-banda-filtro-upro.md. Fuentes A: Yahoo ^GSPC, ^SP500TR, ^VIX; FRED DTB3."""
import hashlib, json, math, os, sys
from datetime import date
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "..", "..", "herramientas"))
import datos  # noqa: E402

COSTO = 0.0010
GASTO = 0.0091 / 252
CACHE = os.path.join(BASE, "R11-datos", "series.json")


def yahoo_diario(t):
    """Yahoo chart v8 con period1/period2 (con range=max Yahoo devuelve barras mensuales)."""
    import time, urllib.parse, urllib.request
    q = urllib.parse.urlencode({"period1": 599616000, "period2": int(time.time()), "interval": "1d"})
    req = urllib.request.Request(f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?{q}",
                                 headers={"User-Agent": "Mozilla/5.0"})
    r = json.load(urllib.request.urlopen(req, timeout=60))["chart"]["result"][0]
    cierre = r["indicators"]["quote"][0]["close"]
    out = []
    for ts, c in zip(r["timestamp"], cierre):
        if c is not None:
            out.append((str(date.fromtimestamp(ts)), float(c)))
    hoy = str(date.today())
    return [x for x in out if x[0] < hoy]  # solo velas cerradas


def cargar():
    if not os.path.exists(CACHE):
        s = {t: yahoo_diario(t) for t in ["^GSPC", "^SP500TR", "^VIX"]}
        s["DTB3"] = [(str(d), v) for d, v in datos.fred_serie("DTB3")]
        json.dump(s, open(CACHE, "w"))
    raw = open(CACHE, "rb").read()
    s = json.loads(raw)
    return {k: {d: v for d, v in val} for k, val in s.items()}, hashlib.sha256(raw).hexdigest()


def preparar(s):
    fechas = sorted(set(s["^GSPC"]) & set(s["^SP500TR"]) & set(s["^VIX"]))
    rf_d, ult = {}, None
    tb = sorted(s["DTB3"].items())
    j = 0
    for d in fechas:  # última tasa publicada con fecha <= d
        while j < len(tb) and tb[j][0] <= d:
            ult = tb[j][1]; j += 1
        rf_d[d] = (ult or 0.0) / 100 / 252
    return fechas, rf_d


def simular(s, fechas, rf, banda=0.03, usar_vix=True, desde=None, hasta=None):
    px = [s["^GSPC"][d] for d in fechas]
    tr = [s["^SP500TR"][d] for d in fechas]
    vix = [s["^VIX"][d] for d in fechas]
    n = 200
    acc, sma = 0.0, [None] * len(px)
    for i, p in enumerate(px):
        acc += p
        if i >= n: acc -= px[i - n]
        if i >= n - 1: sma[i] = acc / n
    senal, est = [None] * len(px), None
    for i in range(len(px)):
        if sma[i] is None: continue
        vix_mal = usar_vix and vix[i] >= 25
        entra = px[i] > sma[i] and not (usar_vix and vix[i] >= 25)
        sale = px[i] < sma[i] * (1 - banda) or vix_mal
        if est is None: est = 1 if entra else 0
        elif est == 1 and sale: est = 0
        elif est == 0 and entra: est = 1
        senal[i] = est
    i0 = next(i for i, x in enumerate(senal) if x is not None) + 2
    if desde: i0 = max(i0, next(i for i, d in enumerate(fechas) if d >= desde))
    i1 = len(px) - 1 if not hasta else max(i for i, d in enumerate(fechas) if d <= hasta)
    eq, bh, exc_r, exc_b = [1.0], [1.0], [], []
    pos_prev = senal[i0 - 2]
    salidas, dentro = 0, 0
    if pos_prev == 1: eq[0] *= 1 - COSTO
    bh[0] *= 1 - COSTO
    for i in range(i0, i1 + 1):
        d = fechas[i]
        r_sub = tr[i] / tr[i - 1] - 1
        r3 = 3 * r_sub - 2 * rf[d] - GASTO
        # la señal del cierre t se ejecuta al cierre de t+1: durante el día i se tiene lo ejecutado al cierre de i-1 (= señal de i-2)
        pos = senal[i - 2]
        r = r3 if pos == 1 else rf[d]
        e = eq[-1] * (1 + r)
        nueva = senal[i - 1]
        if nueva != pos:
            e *= 1 - COSTO
            if nueva == 0: salidas += 1
        dentro += pos == 1
        eq.append(e); bh.append(bh[-1] * (1 + r3))
        exc_r.append(r - rf[d]); exc_b.append(r3 - rf[d])
    return met(eq, exc_r, fechas[i0], fechas[i1], salidas, dentro / (i1 - i0 + 1)), met(bh, exc_b, fechas[i0], fechas[i1], 0, 1.0)


def met(eq, exc, d0, d1, salidas, inv):
    a = (date.fromisoformat(d1) - date.fromisoformat(d0)).days / 365.25
    m = sum(exc) / len(exc); sd = math.sqrt(sum((x - m) ** 2 for x in exc) / (len(exc) - 1))
    pico, mdd = eq[0], 0.0
    for v in eq: pico = max(pico, v); mdd = min(mdd, v / pico - 1)
    return dict(desde=d0, hasta=d1, cagr=eq[-1] ** (1 / a) - 1, sharpe=m / sd * math.sqrt(252), mdd=mdd, salidas=salidas, invertido=inv)


if __name__ == "__main__":
    s, sha = cargar()
    fechas, rf = preparar(s)
    print(f"{len(fechas)} días comunes {fechas[0]} a {fechas[-1]}; sha256 {sha[:16]}…")
    variantes = {"banda -3% + VIX (vigente)": dict(), "sin banda + VIX": dict(banda=0.0),
                 "banda -3% sin VIX": dict(usar_vix=False), "banda -5% + VIX": dict(banda=0.05)}
    periodos = {"completo": (None, None), "1990-2008": (None, "2008-12-31"), "2009-07-hoy": ("2009-07-01", None)}
    out = {}
    for pn, (a, b) in periodos.items():
        print(f"\n== {pn}")
        for vn, kw in variantes.items():
            r, bh = simular(s, fechas, rf, desde=a, hasta=b, **kw)
            out[f"{pn}|{vn}"] = {"regla": r, "bh": bh}
            print(f"{vn:26s} CAGR {r['cagr']:+.1%} Sharpe {r['sharpe']:.2f} MDD {r['mdd']:.1%} salidas {r['salidas']} invertido {r['invertido']:.0%} "
                  f"| 3x B&H CAGR {bh['cagr']:+.1%} Sharpe {bh['sharpe']:.2f} MDD {bh['mdd']:.1%} [{r['desde']}→{r['hasta']}]")
    json.dump({"sha256": sha, "resultados": out}, open(os.path.join(BASE, "R11-resultados.json"), "w"), indent=1)
