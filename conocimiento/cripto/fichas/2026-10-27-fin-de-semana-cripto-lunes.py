"""Comprobación rápida de Ebadollahyvahed y Umeorah (arXiv:2610.35702): la varianza de fin de semana de BTC
(Garman-Klass, sáb+dom) contra la varianza Garman-Klass del lunes del ^GSPC, antes y después del 11-ene-2024.
Sin controles HAR (solo correlación de logs y regresión con el log-varianza del viernes como control).
Uso: python3 -I este.py   (descarga Yahoo chart v8)"""
import json, math, urllib.request, urllib.parse, datetime as dt, statistics as st
def y(t):
    q = urllib.parse.urlencode({"period1": 1509494400, "period2": 1782000000, "interval": "1d"})
    r = json.load(urllib.request.urlopen(urllib.request.Request(
        f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?{q}", headers={"User-Agent": "Mozilla/5.0"}), timeout=60))["chart"]["result"][0]
    o = r["indicators"]["quote"][0]; out = {}
    for i, ts in enumerate(r["timestamp"]):
        if None in (o["open"][i], o["high"][i], o["low"][i], o["close"][i]): continue
        out[dt.datetime.utcfromtimestamp(ts).date()] = (o["open"][i], o["high"][i], o["low"][i], o["close"][i])
    return out
def gk(b):
    o, h, l, c = b
    return 0.5 * math.log(h / l) ** 2 - (2 * math.log(2) - 1) * math.log(c / o) ** 2
btc, spx = y("BTC-USD"), y("^GSPC")
filas = []
for d in sorted(spx):
    if d.weekday() != 0: continue
    sa, do, vi = d - dt.timedelta(2), d - dt.timedelta(1), d - dt.timedelta(3)
    if sa in btc and do in btc and vi in spx:
        w = math.log(gk(btc[sa]) + gk(btc[do]) + 1e-10)
        filas.append((d, w, math.log(gk(spx[d]) + 1e-10), math.log(gk(spx[vi]) + 1e-10)))
def ols2(y_, x1, x2):
    # y = a + b1 x1 + b2 x2 ; devuelve b1 y su t (errores clásicos)
    n = len(y_); m = lambda v: sum(v) / n
    X = [(1, a, b) for a, b in zip(x1, x2)]
    import itertools
    XtX = [[sum(r[i] * r[j] for r in X) for j in range(3)] for i in range(3)]
    Xty = [sum(r[i] * v for r, v in zip(X, y_)) for i in range(3)]
    # inversa 3x3
    a = XtX; det = (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1]) - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0]) + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
    inv = [[(a[(j+1)%3][(i+1)%3]*a[(j+2)%3][(i+2)%3]-a[(j+1)%3][(i+2)%3]*a[(j+2)%3][(i+1)%3])/det for j in range(3)] for i in range(3)]
    b = [sum(inv[i][k] * Xty[k] for k in range(3)) for i in range(3)]
    e = [v - (b[0] + b[1] * p + b[2] * q) for v, p, q in zip(y_, x1, x2)]
    s2 = sum(z * z for z in e) / (n - 3)
    return b[1], b[1] / math.sqrt(s2 * inv[1][1])
corte = dt.date(2024, 1, 11)
for nom, sub in (("2017-11 a 2024-01", [f for f in filas if f[0] < corte]), ("2024-01 en adelante", [f for f in filas if f[0] >= corte])):
    W = [f[1] for f in sub]; M = [f[2] for f in sub]; V = [f[3] for f in sub]
    b, t = ols2(M, W, V)
    print(f"{nom}: lunes n={len(sub)} | corr(W, lunes)={st.correlation(W, M):.3f} | gamma={b:.3f} (t={t:.2f}) con control del viernes | "
          f"+1σ de W -> varianza del lunes x{math.exp(b*st.pstdev(W)):.2f}")
