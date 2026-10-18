"""R12 (ejecución A): condición VIX >= 25 en el filtro de un 3x sintético del Nasdaq-100 (fuera de muestra de R11).
Pre-registro: R12-condicion-vix-filtro.md. Fuentes A: Yahoo ^NDX, ^VIX; FRED DTB3.
Reproduce: python3 laboratorio/replicas/R12.py"""
import hashlib, json, math, os, sys, time, urllib.parse, urllib.request
from datetime import date
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "..", "..", "herramientas"))
import datos  # noqa: E402

COSTO = 0.0010
GASTO = 0.0095 / 252
FIN = "2026-10-16"
CACHE = os.path.join(BASE, "R12-datos", "series.json")


def yahoo_diario(t, p1=599616000):
    q = urllib.parse.urlencode({"period1": p1, "period2": int(time.time()), "interval": "1d"})
    req = urllib.request.Request(f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?{q}",
                                 headers={"User-Agent": "Mozilla/5.0"})
    r = json.load(urllib.request.urlopen(req, timeout=60))["chart"]["result"][0]
    out = [(str(date.fromtimestamp(ts)), float(c)) for ts, c in zip(r["timestamp"], r["indicators"]["quote"][0]["close"]) if c is not None]
    return [x for x in out if x[0] <= FIN]


def cargar():
    if not os.path.exists(CACHE):
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        s = {t: yahoo_diario(t) for t in ["^NDX", "^VIX"]}
        s["DTB3"] = [(str(d), v) for d, v in datos.fred_serie("DTB3")]
        json.dump(s, open(CACHE, "w"))
    raw = open(CACHE, "rb").read()
    s = json.loads(raw)
    return {k: {d: v for d, v in val} for k, val in s.items()}, hashlib.sha256(raw).hexdigest()


def preparar(s):
    fechas = sorted(set(s["^NDX"]) & set(s["^VIX"]))
    rf, ult, j = {}, None, 0
    tb = sorted(s["DTB3"].items())
    for d in fechas:
        while j < len(tb) and tb[j][0] <= d:
            ult = tb[j][1]; j += 1
        rf[d] = (ult or 0.0) / 100 / 252
    return fechas, rf


def senales(px, vix, usar_vix=True, umbral=25.0, confirmar=1):
    n, acc, sma = 200, 0.0, [None] * len(px)
    for i, p in enumerate(px):
        acc += p
        if i >= n: acc -= px[i - n]
        if i >= n - 1: sma[i] = acc / n
    out, est = [None] * len(px), None
    for i in range(len(px)):
        if sma[i] is None: continue
        vix_alto = usar_vix and all(vix[k] >= umbral for k in range(max(0, i - confirmar + 1), i + 1))
        vix_bajo = (not usar_vix) or vix[i] < umbral
        entra = px[i] > sma[i] * 1.03 and vix_bajo
        sale = px[i] < sma[i] * 0.97 or vix_alto
        if est is None: est = 1 if px[i] > sma[i] and vix_bajo else 0
        elif est == 1 and sale: est = 0
        elif est == 0 and entra: est = 1
        out[i] = est
    return out


def simular(s, fechas, rf, desde=None, hasta=None, **kw):
    px = [s["^NDX"][d] for d in fechas]
    vix = [s["^VIX"][d] for d in fechas]
    sen = senales(px, vix, **kw)
    i0 = next(i for i, x in enumerate(sen) if x is not None) + 2
    if desde: i0 = max(i0, next(i for i, d in enumerate(fechas) if d >= desde))
    i1 = len(px) - 1 if not hasta else max(i for i, d in enumerate(fechas) if d <= hasta)
    eq, bh, er, eb = [1.0], [1.0], [], []
    if sen[i0 - 2] == 1: eq[0] *= 1 - COSTO
    bh[0] *= 1 - COSTO
    salidas = dentro = 0
    for i in range(i0, i1 + 1):
        d = fechas[i]
        r3 = 3 * (px[i] / px[i - 1] - 1) - 2 * rf[d] - GASTO
        pos = sen[i - 2]          # señal de t ejecutada al cierre de t+1
        r = r3 if pos == 1 else rf[d]
        e = eq[-1] * (1 + r)
        if sen[i - 1] != pos:
            e *= 1 - COSTO
            salidas += sen[i - 1] == 0
        dentro += pos == 1
        eq.append(e); bh.append(bh[-1] * (1 + r3)); er.append(r - rf[d]); eb.append(r3 - rf[d])
    return met(eq, er, fechas[i0], fechas[i1], salidas, dentro / (i1 - i0 + 1)), met(bh, eb, fechas[i0], fechas[i1], 0, 1.0)


def met(eq, exc, d0, d1, salidas, inv):
    a = (date.fromisoformat(d1) - date.fromisoformat(d0)).days / 365.25
    m = sum(exc) / len(exc); sd = math.sqrt(sum((x - m) ** 2 for x in exc) / (len(exc) - 1))
    pico, mdd = eq[0], 0.0
    for v in eq: pico = max(pico, v); mdd = min(mdd, v / pico - 1)
    return dict(desde=d0, hasta=d1, cagr=eq[-1] ** (1 / a) - 1, sharpe=m / sd * math.sqrt(252), mdd=mdd, salidas=salidas, invertido=inv)


if __name__ == "__main__":
    s, sha = cargar()
    fechas, rf = preparar(s)
    lineas = [f"Yahoo ^NDX y ^VIX, FRED DTB3: {len(fechas)} días comunes {fechas[0]} a {fechas[-1]}; sha256 {sha[:16]}…"]
    variantes = {"V0 vigente (VIX>=25)": {}, "V1 sin VIX": dict(usar_vix=False),
                 "V2 VIX>=25 dos cierres": dict(confirmar=2), "V3 VIX>=30": dict(umbral=30.0)}
    periodos = {"completo": (None, None), "1990-2008": (None, "2008-12-31"), "2009-hoy": ("2009-01-01", None)}
    out = {}
    for pn, (a, b) in periodos.items():
        lineas.append(f"\n== {pn}")
        for vn, kw in variantes.items():
            r, bh = simular(s, fechas, rf, desde=a, hasta=b, **kw)
            out[f"{pn}|{vn}"] = {"regla": r, "bh": bh}
            lineas.append(f"{vn:24s} CAGR {r['cagr']:+.1%} Sharpe {r['sharpe']:.2f} MDD {r['mdd']:.1%} salidas {r['salidas']:3d} "
                          f"invertido {r['invertido']:.0%} | 3x B&H CAGR {bh['cagr']:+.1%} Sharpe {bh['sharpe']:.2f} MDD {bh['mdd']:.1%} [{r['desde']}→{r['hasta']}]")
    v0, v1 = out["completo|V0 vigente (VIX>=25)"]["regla"], out["completo|V1 sin VIX"]["regla"]
    h1 = v1["sharpe"] > v0["sharpe"] and v1["mdd"] >= v0["mdd"] - 0.03
    h2 = v1["salidas"] <= 0.6 * v0["salidas"]
    estado = "Replicado" if h1 and h2 else ("Replicado con diferencias" if h2 else "No replicado")
    lineas.append(f"\nVeredicto A: H1 {'sostenida' if h1 else 'refutada'}; H2 {'sostenida' if h2 else 'refutada'} -> {estado}")
    txt = "\n".join(lineas) + "\n"
    open(os.path.join(BASE, "R12-salida.txt"), "w").write(txt)
    json.dump({"sha256": sha, "veredicto": {"H1": h1, "H2": h2, "estado_A": estado}, "resultados": out},
              open(os.path.join(BASE, "R12-resultados.json"), "w"), indent=1)
    sys.stdout.write(txt)
