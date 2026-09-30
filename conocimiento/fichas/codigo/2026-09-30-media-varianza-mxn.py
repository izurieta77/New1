"""Ficha 2026-09-30: media-varianza en MXN con ETFs del SIC (SPY, QQQ, GLD) y CETES.

1. Estima mu y Sigma mensuales en MXN (2005-01 a 2026-09) y calcula: minima varianza (GMV),
   tangente sin cortos (malla de 1%), 1/N y la cartera (a) del 30-sep (32% S&P, 55% Nasdaq, 13% CETES).
2. Inestabilidad: pesos tangentes por mitades y por bootstrap (1,000 remuestreos).
3. Fuera de muestra: tangente con ventana movil de 60 meses contra 1/N y contra 60/40 S&P/Nasdaq fijo.

Solo stdlib + herramientas del repo. Uso: python3 conocimiento/fichas/codigo/2026-09-30-media-varianza-mxn.py
"""
import math
import random
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from herramientas import datos  # noqa: E402

ACTIVOS = ["SPY", "QQQ", "GLD"]


def mensual(ticker):
    s = datos.yahoo_serie(ticker, rango="30y", intervalo="1mo")
    return {(d.year, d.month): v for d, v in s if d.day == 1}


def cargar():
    fx = mensual("MXN=X")
    px = {t: mensual(t) for t in ACTIVOS}
    cetes = {(d.year, d.month): v for d, v in datos.fred_serie("INTGSTMXM193N")}
    meses = sorted(set(fx).intersection(*[set(p) for p in px.values()]))
    meses = [m for m in meses if m >= (2004, 12)]
    ultimo_cetes = None
    filas = []
    for a, b in zip(meses, meses[1:]):
        rs = [px[t][b] * fx[b] / (px[t][a] * fx[a]) - 1 for t in ACTIVOS]
        ultimo_cetes = cetes.get(a, ultimo_cetes)
        filas.append((b, rs, ultimo_cetes / 1200))
    return filas


def mu_cov(rs):
    n = len(rs[0])
    mu = [st.mean(r[i] for r in rs) for i in range(n)]
    cov = [[st.covariance([r[i] for r in rs], [r[j] for r in rs]) for j in range(n)] for i in range(n)]
    return mu, cov


def stats(w, mu, cov, rf):
    m = sum(wi * mi for wi, mi in zip(w, mu)) + (1 - sum(w)) * rf
    v = sum(w[i] * w[j] * cov[i][j] for i in range(len(w)) for j in range(len(w)))
    return m, math.sqrt(v)


def malla(paso=0.01):
    k = round(1 / paso)
    for i in range(k + 1):
        for j in range(k + 1 - i):
            yield [i * paso, j * paso, (k - i - j) * paso]


def tangente(mu, cov, rf, paso=0.01):
    mejor = None
    for w in malla(paso):
        m, s = stats(w, mu, cov, rf)
        sh = (m - rf) / s
        if mejor is None or sh > mejor[0]:
            mejor = (sh, w)
    return mejor


def gmv(mu, cov, rf):
    return min(((stats(w, mu, cov, rf)[1], w) for w in malla()), key=lambda x: x[0])


def anual(m, s):
    return 12 * m, math.sqrt(12) * s


def main():
    filas = cargar()
    rs = [r for _, r, _ in filas]
    rf = st.mean(c for _, _, c in filas)
    print(f"Muestra {filas[0][0]}..{filas[-1][0]} n={len(filas)} meses; CETES medio {1200*rf:.2f}%/año (FRED INTGSTMXM193N, x12)")
    mu, cov = mu_cov(rs)
    print("\n== 1. Momentos en MXN (anualizados, media x12) ==")
    for t, m, i in zip(ACTIVOS, mu, range(3)):
        print(f"{t}: media {1200*m:.2f}% sigma {100*math.sqrt(12*cov[i][i]):.2f}% Sharpe {(m-rf)/math.sqrt(cov[i][i])*math.sqrt(12):.2f}")
    cor = lambda i, j: cov[i][j] / math.sqrt(cov[i][i] * cov[j][j])
    print(f"correlaciones: SPY-QQQ {cor(0,1):.2f} SPY-GLD {cor(0,2):.2f} QQQ-GLD {cor(1,2):.2f}")

    carteras = {
        "Tangente (sin cortos)": tangente(mu, cov, rf)[1],
        "GMV riesgosa": gmv(mu, cov, rf)[1],
        "1/N (SPY,QQQ,GLD)": [1 / 3] * 3,
        "Cartera (a) 32/55/0 + 13% CETES": [0.32, 0.55, 0.0],
        "60/40 S&P/Nasdaq": [0.6, 0.4, 0.0],
    }
    print("\n== 2. Carteras en muestra ==")
    for nombre, w in carteras.items():
        m, s = stats(w, mu, cov, rf)
        ma, sa = anual(m, s)
        print(f"{nombre}: pesos {[round(x,2) for x in w]} | media {100*ma:.2f}% sigma {100*sa:.2f}% Sharpe {(ma-12*rf)/sa:.2f}")

    print("\n== 3. Inestabilidad de la tangente ==")
    mitad = len(rs) // 2
    for etiqueta, sub, c in (("1a mitad", rs[:mitad], [x for _, _, x in filas[:mitad]]),
                              ("2a mitad", rs[mitad:], [x for _, _, x in filas[mitad:]])):
        m2, c2 = mu_cov(sub)
        print(f"{etiqueta} ({filas[0 if etiqueta=='1a mitad' else mitad][0]}..): tangente {tangente(m2, c2, st.mean(c), 0.05)[1]}")
    random.seed(20260930)
    pesos = []
    for _ in range(1000):
        muestra = [rs[random.randrange(len(rs))] for _ in rs]
        m2, c2 = mu_cov(muestra)
        pesos.append(tangente(m2, c2, rf, 0.05)[1])
    for i, t in enumerate(ACTIVOS):
        xs = sorted(p[i] for p in pesos)
        print(f"bootstrap {t}: p10 {xs[100]:.2f} mediana {xs[500]:.2f} p90 {xs[900]:.2f}; P(peso=0) {sum(x==0 for x in xs)/1000:.2f}")

    print("\n== 4. Fuera de muestra: ventana movil de 60 meses, rebalanceo mensual, sin costos ==")
    res = {"Tangente 60m": [], "1/N": [], "60/40 S&P/Nasdaq": [], "S&P solo": []}
    for k in range(60, len(filas)):
        ventana = rs[k - 60:k]
        m2, c2 = mu_cov(ventana)
        rfk = filas[k][2]
        w_t = tangente(m2, c2, st.mean(x for _, _, x in filas[k - 60:k]), 0.05)[1]
        r = rs[k]
        for nombre, w in (("Tangente 60m", w_t), ("1/N", [1 / 3] * 3), ("60/40 S&P/Nasdaq", [0.6, 0.4, 0]),
                          ("S&P solo", [1, 0, 0])):
            res[nombre].append((sum(a * b for a, b in zip(w, r)), rfk))
    print(f"periodo {filas[60][0]}..{filas[-1][0]} ({len(filas)-60} meses)")
    for nombre, xs in res.items():
        r = [a for a, _ in xs]
        ex = [a - b for a, b in xs]
        g = math.exp(sum(math.log1p(a) for a in r) / len(r) * 12) - 1
        v, pico, mdd = 1.0, 1.0, 0.0
        for a in r:
            v *= 1 + a
            pico = max(pico, v)
            mdd = max(mdd, 1 - v / pico)
        print(f"{nombre}: CAGR {100*g:.2f}% sigma {100*st.pstdev(r)*math.sqrt(12):.2f}% "
              f"Sharpe {st.mean(ex)/st.pstdev(ex)*math.sqrt(12):.2f} MDD {100*mdd:.1f}%")


if __name__ == "__main__":
    main()
