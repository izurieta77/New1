"""Réplica fuera de muestra del momentum de serie de tiempo semanal de BTC
(Liu y Tsyvinski, RFS 2021, NBER w24877, tabla 14 panel B y tabla 17).

Datos: klines semanales BTCUSDT de data-api.binance.vision (semana lunes 00:00 a
domingo 23:59:59 UTC; el paper usa domingo 23:59:59 UTC de CoinDesk).
Muestra fuera del paper: semanas cuyo cierre es posterior al 31-may-2018.
Solo biblioteca estándar. Uso: python3 -I este_archivo.py
"""
import json, math, urllib.request, datetime as dt, statistics as st

URL = "https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1w&limit=1000"
k = json.load(urllib.request.urlopen(URL, timeout=30))
ahora = dt.datetime.now(dt.timezone.utc).timestamp() * 1000
k = [r for r in k if r[6] < ahora]                         # solo semanas cerradas
fechas = [dt.datetime.fromtimestamp(r[6] / 1000, dt.timezone.utc).date() for r in k]
cierres = [float(r[4]) for r in k]
R = [cierres[i] / cierres[i - 1] - 1 for i in range(1, len(cierres))]   # rendimiento simple semanal
F = fechas[1:]

def ols(x, y, lags):
    n = len(x); mx, my = st.fmean(x), st.fmean(y)
    sxx = sum((a - mx) ** 2 for a in x)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sxx
    a0 = my - b * mx
    e = [c - a0 - b * a for a, c in zip(x, y)]
    s2 = sum(v * v for v in e) / (n - 2)
    t_ols = b / math.sqrt(s2 / sxx)
    # Newey-West para la pendiente
    u = [(a - mx) * v for a, v in zip(x, e)]
    S = sum(v * v for v in u)
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        S += 2 * w * sum(u[i] * u[i - L] for i in range(L, n))
    t_nw = b / (math.sqrt(S) / sxx)
    r2 = 1 - sum(v * v for v in e) / sum((c - my) ** 2 for c in y)
    return b, t_ols, t_nw, r2, n

corte = dt.date(2018, 5, 31)
i0 = next(i for i, f in enumerate(F) if f > corte)
print(f"Semanas cerradas: {len(R)} ({F[0]} a {F[-1]}); fuera de muestra desde {F[i0]}: {len(R) - i0}")
print(f"sigma semanal fuera de muestra: {st.pstdev(R[i0:]) * 100:.2f}% (paper 2011-2018: 16.64%)")
paper = {1: 0.19, 2: 0.22, 3: 0.21, 4: 0.09}
for h in (1, 2, 3, 4):
    x = R[i0:len(R) - h]; y = R[i0 + h:]
    b, t, tnw, r2, n = ols(x, y, lags=h + 3)
    print(f"h={h}: beta {b:+.3f} (paper {paper[h]:+.2f}) t_OLS {t:+.2f} t_NW {tnw:+.2f} R2 {r2:.3f} n={n} "
          f"efecto 1 sigma {b * st.pstdev(x) * 100:+.2f} pp")

# Quintiles sin mirar adelante (análogo de la tabla 17): cortes con los primeros 2 años fuera de muestra
ent = R[i0:i0 + 104]
q = [sorted(ent)[int(len(ent) * p)] for p in (0.2, 0.4, 0.6, 0.8)]
grupos = {g: [] for g in range(1, 6)}
for i in range(i0 + 104, len(R) - 1):
    g = 1 + sum(R[i] > c for c in q)
    grupos[g].append(R[i + 1])
print("Cortes de quintil (%):", [round(c * 100, 2) for c in q])
for g, v in grupos.items():
    m = st.fmean(v); s = st.pstdev(v)
    print(f"Q{g}: n={len(v)} R_t+1 media {m * 100:+.2f}%  t {m / (s / math.sqrt(len(v))):+.2f}  Sharpe sem {m / s:+.2f}")
dif = st.fmean(grupos[5]) - st.fmean(grupos[1])
print(f"Q5-Q1: {dif * 100:+.2f} pp por semana (paper tabla 17: +4.53)")

# Signo simple: largo la semana siguiente solo si R_t > 0, contra comprar y mantener
largo = [R[i + 1] if R[i] > 0 else 0.0 for i in range(i0, len(R) - 1)]
bh = R[i0 + 1:]
def anual(v):
    g = 1.0
    for r in v: g *= 1 + r
    return g ** (52 / len(v)) - 1, st.fmean(v) / st.pstdev(v) * math.sqrt(52)
for nom, v in (("signo 1 semana", largo), ("comprar y mantener", bh)):
    cagr, sh = anual(v); print(f"{nom}: CAGR {cagr * 100:+.1f}% Sharpe anual {sh:.2f} (sin costos)")
print(f"Semanas largo: {sum(1 for i in range(i0, len(R) - 1) if R[i] > 0)} de {len(R) - 1 - i0}; "
      f"cambios de posición: {sum(1 for i in range(i0 + 1, len(R) - 1) if (R[i] > 0) != (R[i - 1] > 0))}")

# Estabilidad: beta h=1 por mitades y Q5 sin las 5 mejores semanas siguientes
mitad = i0 + (len(R) - i0) // 2
for nom, a, z in (("1.a mitad", i0, mitad), ("2.a mitad", mitad, len(R))):
    b, t, tnw, r2, n = ols(R[a:z - 1], R[a + 1:z], lags=4)
    print(f"{nom} ({F[a]} a {F[z - 1]}): beta h=1 {b:+.3f} t_NW {tnw:+.2f} n={n}")
q5 = sorted(grupos[5])
print(f"Q5 sin sus 5 mejores semanas: media {st.fmean(q5[:-5]) * 100:+.2f}% (n={len(q5) - 5})")
