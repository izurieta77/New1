"""Calculos ilustrativos del modulo 20 (metodos cuantitativos). NO es una replica ni una regla.

Datos: French (F-F_Research_Data_Factors diario y mensual), Yahoo (^GSPC, ^MXX, MXN=X).
Solo biblioteca estandar. Uso: python3 laboratorio/ilustraciones/M20_hechos_estilizados.py
Salida: estadisticos que cita conocimiento/20-metodos-cuantitativos-y-econometria.md.
"""
import math
import random
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from herramientas import datos_historicos as dh  # noqa: E402
from herramientas.estadistica import newey_west  # noqa: E402

N01 = st.NormalDist()


def momentos(x):
    n = len(x); m = sum(x) / n
    s2 = sum((v - m) ** 2 for v in x) / n
    s = math.sqrt(s2)
    g3 = sum((v - m) ** 3 for v in x) / n / s ** 3
    g4 = sum((v - m) ** 4 for v in x) / n / s ** 4
    return m, s, g3, g4


def colas(x, nombre):
    m, s, g3, g4 = momentos(x)
    n = len(x)
    print(f"\n== Colas: {nombre} (n={n})  media={m:.5f} sd={s:.5f} asim={g3:.2f} curtosis={g4:.1f}")
    for k in (3, 4, 5, 7, 10):
        obs = sum(abs(v - m) > k * s for v in x)
        esp = n * 2 * (1 - N01.cdf(k))
        print(f"  |z|>{k}: observados={obs}  esperados normal={esp:.4f}  razon={obs / esp if esp else float('inf'):.0f}")
    peor = min(x); print(f"  peor dia={peor:.4f}  z={(peor - m) / s:.1f}  P_normal~{N01.cdf((peor - m) / s):.1e}")
    # Hill sobre perdidas (cola izquierda)
    perd = sorted((-v for v in x if v < 0), reverse=True)
    for frac in (0.005, 0.01, 0.025):
        k = int(frac * n)
        xk = perd[k]
        h = sum(math.log(perd[i] / xk) for i in range(k)) / k
        print(f"  Hill cola izquierda k={k} ({frac:.1%} de n): alfa={1 / h:.2f}")


def garch11(r, iters=4000, semilla=1):
    """GARCH(1,1) gaussiano por maxima verosimilitud (busqueda aleatoria local, stdlib)."""
    m = sum(r) / len(r); e = [v - m for v in r]; var0 = sum(v * v for v in e) / len(e)

    def nll(w, a, b):
        if w <= 0 or a < 0 or b < 0 or a + b >= 0.9999:
            return float("inf")
        h = var0; ll = 0.0
        for v in e:
            ll += math.log(h) + v * v / h
            h = w + a * v * v + b * h
        return 0.5 * ll
    rng = random.Random(semilla)
    best = (var0 * 0.02, 0.08, 0.9); fb = nll(*best); paso = [var0 * 0.01, 0.02, 0.02]
    for i in range(iters):
        cand = tuple(max(1e-12, best[j] + rng.gauss(0, paso[j])) for j in range(3))
        fc = nll(*cand)
        if fc < fb:
            best, fb = cand, fc
        if i % 500 == 499:
            paso = [p * 0.6 for p in paso]
    w, a, b = best
    return w, a, b, fb


def ols(y, X):
    """OLS con stdlib: resuelve (X'X) b = X'y por eliminacion gaussiana."""
    k = len(X[0])
    A = [[sum(X[t][i] * X[t][j] for t in range(len(y))) for j in range(k)] for i in range(k)]
    c = [sum(X[t][i] * y[t] for t in range(len(y))) for i in range(k)]
    for i in range(k):
        p = max(range(i, k), key=lambda r: abs(A[r][i]))
        A[i], A[p] = A[p], A[i]; c[i], c[p] = c[p], c[i]
        for r in range(i + 1, k):
            f = A[r][i] / A[i][i]
            for j in range(i, k):
                A[r][j] -= f * A[i][j]
            c[r] -= f * c[i]
    b = [0.0] * k
    for i in reversed(range(k)):
        b[i] = (c[i] - sum(A[i][j] * b[j] for j in range(i + 1, k))) / A[i][i]
    return b


def har_vs_rezago(r, inicio_oos=0.5, h=22):
    """Pronostico de la varianza realizada de los proximos h dias (suma de r^2).
    Modelos: (a) HAR con componentes 1, 5 y 22 dias (estimado con ventana expansiva, re-estimado cada 250 dias),
    (b) ingenuo: varianza de los ultimos 22 dias. Perdida QLIKE y MSE en log; Diebold-Mariano con NW."""
    r2 = [v * v for v in r]
    n = len(r2)
    def med(t, k):
        return sum(r2[t - k + 1:t + 1]) / k
    filas = []
    for t in range(22, n - h):
        y = sum(r2[t + 1:t + 1 + h]) / h
        filas.append((t, y, med(t, 1), med(t, 5), med(t, 22)))
    t0 = int(len(filas) * inicio_oos)
    perd_har, perd_ing = [], []
    b = None
    for i in range(t0, len(filas)):
        if b is None or (i - t0) % 250 == 0:
            ent = filas[:i - h]  # solo informacion conocida: el objetivo termina antes de t
            b = ols([f[1] for f in ent], [[1.0, f[2], f[3], f[4]] for f in ent])
        _, y, d, w, mth = filas[i]
        f_har = max(1e-10, b[0] + b[1] * d + b[2] * w + b[3] * mth)
        f_ing = max(1e-10, mth)
        q = lambda f: y / f - math.log(y / f) - 1 if y > 0 else 0.0
        perd_har.append(q(f_har)); perd_ing.append(q(f_ing))
    dif = [a - c for a, c in zip(perd_ing, perd_har)]
    nw = newey_west(dif, rezagos=h)
    return b, st.fmean(perd_har), st.fmean(perd_ing), nw


def main():
    diaria = dh.french("F-F_Research_Data_Factors_daily", "diaria")
    mkt_d = [a + b for a, b in zip(diaria["columnas"]["Mkt-RF"], diaria["columnas"]["RF"]) if a is not None]
    print("French diario:", diaria["fechas"][0], "->", diaria["fechas"][-1], "version", diaria.get("version_crsp"))
    colas([math.log1p(v) for v in mkt_d], "Mercado EUA diario (French, log)")

    mensual = dh.french("F-F_Research_Data_Factors", "mensual")
    ex = [v for v in mensual["columnas"]["Mkt-RF"] if v is not None]
    print("\nFrench mensual:", mensual["fechas"][0], "->", mensual["fechas"][-1])
    m, s, g3, g4 = momentos(ex)
    T = len(ex) / 12
    sr = m / s * math.sqrt(12)
    print(f"  Exceso mensual: media={m:.5f} ({m*12:.3%}/a) sd={s:.4f} ({s*math.sqrt(12):.2%}/a) SR anual={sr:.3f} anos={T:.1f}")
    print(f"  EE media anual = sd_anual/sqrt(T) = {s*math.sqrt(12)/math.sqrt(T):.3%}; t=SR*sqrt(T)={sr*math.sqrt(T):.2f}")
    nw = newey_west(ex, 6); print(f"  t iid={nw['t_iid']:.2f} t NW(6)={nw['t']:.2f}")
    for a0, a1 in ((1926, 1955), (1956, 1985), (1986, 2015), (1996, 2025)):
        sub = [v for f, v in zip(mensual["fechas"], mensual["columnas"]["Mkt-RF"]) if v is not None and a0 <= f.year <= a1]
        mm, ss, _, _ = momentos(sub)
        print(f"  {a0}-{a1}: prima anual={mm*12:.2%}  EE={ss*math.sqrt(12)/math.sqrt(len(sub)/12):.2%}  SR={mm/ss*math.sqrt(12):.2f}")
    # Monte Carlo: 200 estrategias sin ventaja, 10 anos mensuales, vol 15%
    rng = random.Random(20260925)
    maxs = []
    for _ in range(2000):
        best = -9
        for _ in range(200):
            x = [rng.gauss(0, 0.15 / math.sqrt(12)) for _ in range(120)]
            best = max(best, st.fmean(x) / st.stdev(x) * math.sqrt(12))
        maxs.append(best)
    maxs.sort()
    print(f"\nMonte Carlo: max SR anual de 200 estrategias nulas, 10 anos: mediana={maxs[1000]:.2f} p5={maxs[100]:.2f} p95={maxs[1900]:.2f}")

    gspc = dh.yahoo_historia("^GSPC")
    p = gspc["precios"]; f = gspc["fechas"]
    r = [math.log(p[i] / p[i - 1]) for i in range(1, len(p))]
    print("\n^GSPC:", f[0], "->", f[-1])
    r_desde2000 = [v for d, v in zip(f[1:], r) if d.year >= 2000]
    w, a, b, _ = garch11(r_desde2000)
    print(f"  GARCH(1,1) 2000-2026: omega={w:.2e} alpha={a:.3f} beta={b:.3f} persistencia={a+b:.4f} vida media={math.log(0.5)/math.log(a+b):.0f} dias vol LP anual={math.sqrt(w/(1-a-b)*252):.1%}")
    bh, qh, qi, nwq = har_vs_rezago(r_desde2000)
    print(f"  HAR coef (c, d, s, m)={[round(x, 6) if i == 0 else round(x, 3) for i, x in enumerate(bh)]}")
    print(f"  QLIKE media OOS: HAR={qh:.4f} ingenuo22d={qi:.4f}; DM (ingenuo-HAR) media={nwq['media']:.4f} t_NW={nwq['t']:.2f}")

    for tic in ("^MXX", "MXN=X"):
        try:
            h = dh.yahoo_historia(tic)
            pp = h["precios"]; ff = h["fechas"]
            rr = [math.log(pp[i] / pp[i - 1]) for i in range(1, len(pp)) if pp[i] > 0 and pp[i - 1] > 0]
            print(f"\n{tic}: {ff[0]} -> {ff[-1]}")
            colas(rr, tic + " diario (log)")
        except Exception as e:  # noqa: BLE001
            print(tic, "error", e)


if __name__ == "__main__":
    main()
