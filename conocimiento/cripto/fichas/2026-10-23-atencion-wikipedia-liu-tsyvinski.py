#!/usr/bin/env python3
"""Atención como predictor del rendimiento de BTC (Liu-Tsyvinski, RFS 2021, sección 4.2 del WP NBER 24877).

Réplica fuera de muestra con un proxy público de atención: visitas diarias al artículo "Bitcoin"
de la Wikipedia en inglés (Wikimedia REST API, agente "user", todas las plataformas), 2015-07-01 en adelante.
Google Trends respondió 429 (sin API pública estable), así que no se usa.

Medida de atención (como LT): la semana t contra el promedio de las 4 semanas previas.
  - principal: a_t = ln(V_t) - ln(media(V_{t-1..t-4}))  (robusta a la caída de nivel de Wikipedia)
  - robustez: d_t = V_t - media(V_{t-1..t-4}) (el diseño literal de LT, en niveles)
  Ambas se estandarizan (z) con la desviación estándar del tramo analizado.
Rendimiento semanal: cierres diarios Yahoo BTC-USD (vela UTC), domingo contra domingo, en %.
Regresiones: R_{t+h} = a + b*z_t (+ c*R_t), h = 1..4, t MCO y t Newey-West (rezagos h+3).
Quintiles sin mirar adelante: cortes con la ventana expansiva previa (mínimo 104 semanas).

Uso: python3 -I 2026-10-23-atencion-wikipedia-liu-tsyvinski.py [--cache DIR]
Solo biblioteca estándar. Corrido el 23-oct-2026 ~14:3x UTC.
"""
import json, math, sys, os, time, urllib.request, urllib.error, datetime as dt, statistics as st

UA = "research-script/1.0 (estudio academico; sin contacto)"
WIKI = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/"
        "all-access/user/Bitcoin/daily/20150701/20261022")
YAHOO = ("https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD?interval=1d"
         "&period1=1420070400&period2=1792800000")
LT_END = dt.date(2018, 5, 31)   # fin de la muestra de LT
LAST_WEEK_END = dt.date(2026, 10, 18)  # último domingo completo al correr


def get(url, cache, name):
    if cache and os.path.exists(os.path.join(cache, name)):
        return json.load(open(os.path.join(cache, name)))
    req = urllib.request.Request(url, headers={"User-Agent": UA if "wikimedia" in url else "Mozilla/5.0"})
    for intento in range(5):  # Wikimedia responde 429 de forma intermitente
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code != 429 or intento == 4:
                raise
            time.sleep(5 * (intento + 1))


def ols(y, X):
    """MCO con constante ya incluida en X; devuelve b, t MCO, t NW(L), R2."""
    n, k = len(y), len(X[0])
    XtX = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(k)] for a in range(k)]
    inv = invert(XtX)
    Xty = [sum(X[i][a] * y[i] for i in range(n)) for a in range(k)]
    b = [sum(inv[a][c] * Xty[c] for c in range(k)) for a in range(k)]
    e = [y[i] - sum(b[a] * X[i][a] for a in range(k)) for i in range(n)]
    s2 = sum(x * x for x in e) / (n - k)
    t_ols = [b[a] / math.sqrt(s2 * inv[a][a]) for a in range(k)]
    ym = sum(y) / n
    r2 = 1 - sum(x * x for x in e) / sum((v - ym) ** 2 for v in y)
    return b, t_ols, inv, e, r2


def nw_t(X, e, inv, b, L):
    n, k = len(e), len(b)
    S = [[0.0] * k for _ in range(k)]
    for lag in range(L + 1):
        w = 1.0 if lag == 0 else 1 - lag / (L + 1)
        for i in range(lag, n):
            for a in range(k):
                for c in range(k):
                    v = X[i][a] * e[i] * X[i - lag][c] * e[i - lag]
                    S[a][c] += w * v if lag == 0 else w * (v + X[i - lag][a] * e[i - lag] * X[i][c] * e[i])
    V = [[sum(inv[a][p] * S[p][q] * inv[q][c] for p in range(k) for q in range(k)) for c in range(k)] for a in range(k)]
    return [b[a] / math.sqrt(V[a][a]) for a in range(k)]


def invert(M):
    n = len(M)
    A = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]


def main():
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    wiki = get(WIKI, cache, "wiki_user.json")["items"]
    views = {dt.datetime.strptime(x["timestamp"][:8], "%Y%m%d").date(): x["views"] for x in wiki}
    yd = get(YAHOO, cache, "btc_yahoo.json")["chart"]["result"][0]
    closes = {}
    for ts, c in zip(yd["timestamp"], yd["indicators"]["quote"][0]["close"]):
        if c is not None:
            closes[dt.datetime.utcfromtimestamp(ts).date()] = c

    # semanas lunes-domingo; se identifican por su domingo
    first_sun = dt.date(2015, 7, 5)
    weeks = []
    d = first_sun + dt.timedelta(days=7)
    while d <= LAST_WEEK_END:
        days = [d - dt.timedelta(days=i) for i in range(7)]
        if all(x in views for x in days) and d in closes and (d - dt.timedelta(days=7)) in closes:
            V = sum(views[x] for x in days)
            R = (closes[d] / closes[d - dt.timedelta(days=7)] - 1) * 100
            weeks.append((d, V, R))
        d += dt.timedelta(days=7)
    print(f"Semanas completas: {len(weeks)} ({weeks[0][0]} a {weeks[-1][0]})")

    # atención: semana t contra las 4 previas
    rows = []
    for i in range(4, len(weeks)):
        d, V, R = weeks[i]
        prev = [weeks[j][1] for j in range(i - 4, i)]
        a_log = math.log(V) - math.log(sum(prev) / 4)
        a_lvl = V - sum(prev) / 4
        rows.append({"d": d, "V": V, "R": R, "a_log": a_log, "a_lvl": a_lvl})
    for i, r in enumerate(rows):
        for h in range(1, 5):
            r[f"R{h}"] = rows[i + h]["R"] if i + h < len(rows) else None

    def tramo(nombre, sel, var):
        sub = [r for r in rows if sel(r["d"])]
        sd = st.pstdev([r[var] for r in sub])
        print(f"\n== {nombre} · medida {var} · n={len(sub)} semanas ({sub[0]['d']} a {sub[-1]['d']}) · sd={sd:.4f}")
        for h in range(1, 5):
            s = [r for r in sub if r[f"R{h}"] is not None]
            y = [r[f"R{h}"] for r in s]
            X = [[1.0, r[var] / sd] for r in s]
            b, t, inv, e, r2 = ols(y, X)
            tn = nw_t(X, e, inv, b, h + 3)
            X2 = [[1.0, r[var] / sd, r["R"]] for r in s]
            b2, t2, inv2, e2, r22 = ols(y, X2)
            tn2 = nw_t(X2, e2, inv2, b2, h + 3)
            print(f"  h={h}: b={b[1]:+.2f} pp por 1 sd (t MCO {t[1]:+.2f}, t NW {tn[1]:+.2f}, R2 {r2:.3f})"
                  f" | con R_t: b={b2[1]:+.2f} (t NW {tn2[1]:+.2f}); c(R_t)={b2[2]:+.3f} (t NW {tn2[2]:+.2f})")
        return sub

    in_lt = lambda d: d <= LT_END
    oos = lambda d: d > LT_END
    post22 = lambda d: d >= dt.date(2022, 1, 1)
    for var in ("a_log", "a_lvl"):
        tramo("Traslape con LT (jul-2015 a may-2018)", in_lt, var)
        tramo("Fuera de muestra (jun-2018 a oct-2026)", oos, var)
        tramo("Era ETF/2022+ (ene-2022 a oct-2026)", post22, var)

    # atención sigue al rendimiento (tabla 25 de LT)
    print("\n== ¿La atención sigue al precio? a_log_t ~ R_t + R_{t-1} (z) ==")
    for nombre, sel in (("traslape LT", in_lt), ("fuera de muestra", oos)):
        idx = [i for i, r in enumerate(rows) if sel(r["d"]) and i >= 1]
        sd = st.pstdev([rows[i]["a_log"] for i in idx])
        y = [rows[i]["a_log"] / sd for i in idx]
        X = [[1.0, rows[i]["R"], rows[i - 1]["R"]] for i in idx]
        b, t, inv, e, r2 = ols(y, X)
        tn = nw_t(X, e, inv, b, 4)
        print(f"  {nombre}: R_t {b[1]:+.4f} sd por pp (t NW {tn[1]:+.2f}); R_t-1 {b[2]:+.4f} (t NW {tn[2]:+.2f}); R2 {r2:.3f}")

    # quintiles sin mirar adelante (ventana expansiva, >=104 semanas), fuera de muestra
    print("\n== Quintiles sin mirar adelante, fuera de muestra (R_{t+1} medio, % semanal) ==")
    buckets = {q: [] for q in range(1, 6)}
    for i, r in enumerate(rows):
        if not oos(r["d"]) or r["R1"] is None or i < 104:
            continue
        hist = sorted(x["a_log"] for x in rows[:i])
        cuts = [hist[int(len(hist) * p)] for p in (0.2, 0.4, 0.6, 0.8)]
        q = 1 + sum(r["a_log"] > c for c in cuts)
        buckets[q].append(r["R1"])
    allr = [x for q in buckets for x in buckets[q]]
    print(f"  incondicional: {st.mean(allr):+.2f}% (n={len(allr)})")
    for q in range(1, 6):
        v = buckets[q]
        m, s = st.mean(v), st.stdev(v)
        print(f"  Q{q}: {m:+.2f}% (t {m / (s / math.sqrt(len(v))):+.2f}, Sharpe sem {m / s:+.2f}, n={len(v)})")
    d15 = st.mean(buckets[5]) - st.mean(buckets[1])
    se = math.sqrt(st.variance(buckets[5]) / len(buckets[5]) + st.variance(buckets[1]) / len(buckets[1]))
    print(f"  Q5-Q1: {d15:+.2f} pp (t Welch {d15 / se:+.2f}); LT tabla 22 (sin mirar adelante): +7.39 pp")

    # lectura actual
    print("\n== Últimas semanas ==")
    sd_oos = st.pstdev([r["a_log"] for r in rows if oos(r["d"])])
    hist = sorted(x["a_log"] for x in rows[:-1])
    for r in rows[-4:]:
        pct = sum(x <= r["a_log"] for x in hist) / len(hist) * 100
        print(f"  semana al {r['d']}: visitas {r['V']:,} · a_log {r['a_log']:+.3f} (z {r['a_log'] / sd_oos:+.2f}, percentil {pct:.0f}) · R {r['R']:+.2f}%")
    # semana en curso (lun 19 a jue 22-oct, 4 días) contra la media diaria de las 4 semanas previas
    cur = [dt.date(2026, 10, 19) + dt.timedelta(days=i) for i in range(4)]
    if all(x in views for x in cur):
        md = sum(views[x] for x in cur) / 4
        prevd = sum(w[1] for w in weeks[-4:]) / 28
        print(f"  semana en curso (19-22 oct, parcial): media diaria {md:,.0f} vs {prevd:,.0f} -> a_log parcial {math.log(md / prevd):+.3f}")


if __name__ == "__main__":
    main()
