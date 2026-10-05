"""Ficha 2026-10-05: duracion y convexidad, de la formula al ETF real (TLT).

1. Bono con cupon (tipo Mbono, cupon semestral): precio, duracion de Macaulay y modificada, convexidad
   analitica, verificadas con diferencias finitas (segunda comprobacion).
2. TLT (Yahoo, cierre ajustado, incluye cupones) contra FRED DGS20: regresion diaria
   r_TLT - y/252 = a + b1*dy + b2*dy^2 -> duracion empirica (-b1) y convexidad empirica (2*b2).
   Por subperiodos y en dias de movimientos grandes (|dy| >= 15 pb).
3. Prediccion de choques: -D*dy + C/2*dy^2 contra el rendimiento real de TLT en los 10 peores/mejores dias.
Solo stdlib + herramientas. Uso: python3 conocimiento/fichas/codigo/2026-10-05-duracion-convexidad.py
"""
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from herramientas import datos, datos_historicos as dh  # noqa: E402


def precio(y, cupon, anios, f=2, nominal=100.0):
    n = int(round(anios * f))
    c = nominal * cupon / f
    return sum(c / (1 + y / f) ** k for k in range(1, n + 1)) + nominal / (1 + y / f) ** n


def analitico(y, cupon, anios, f=2, nominal=100.0):
    n = int(round(anios * f))
    c = nominal * cupon / f
    p = precio(y, cupon, anios, f, nominal)
    flujos = [(k / f, c + (nominal if k == n else 0)) for k in range(1, n + 1)]
    mac = sum(t * cf / (1 + y / f) ** (t * f) for t, cf in flujos) / p
    mod = mac / (1 + y / f)
    conv = sum(cf * t * (t + 1 / f) / (1 + y / f) ** (t * f + 2) for t, cf in flujos) / p
    return p, mac, mod, conv


def ols(X, y):
    k = len(X[0])
    xtx = [[sum(r[i] * r[j] for r in X) for j in range(k)] for i in range(k)]
    xty = [sum(r[i] * v for r, v in zip(X, y)) for i in range(k)]
    # Gauss-Jordan
    m = [row[:] + [b] for row, b in zip(xtx, xty)]
    for i in range(k):
        piv = m[i][i]
        m[i] = [v / piv for v in m[i]]
        for j in range(k):
            if j != i:
                fct = m[j][i]
                m[j] = [a - fct * b for a, b in zip(m[j], m[i])]
    beta = [m[i][k] for i in range(k)]
    res = [v - sum(b * x for b, x in zip(beta, r)) for r, v in zip(X, y)]
    r2 = 1 - st.pvariance(res) / st.pvariance(y)
    return beta, r2


def main():
    print("== 1. Bono a 10 años, cupon 8%, rendimiento 9% (tipo Mbono) ==")
    y, c, T = 0.09, 0.08, 10
    p, mac, mod, conv = analitico(y, c, T)
    h = 1e-4
    pu, pd = precio(y + h, c, T), precio(y - h, c, T)
    mod_fd = (pd - pu) / (2 * h * p)
    conv_fd = (pu + pd - 2 * p) / (h * h * p)
    print(f"precio {p:.4f} | Macaulay {mac:.4f} | modificada {mod:.4f} (dif. finitas {mod_fd:.4f}) | "
          f"convexidad {conv:.2f} (dif. finitas {conv_fd:.2f})")
    for dy in (0.01, 0.02, -0.02):
        real = precio(y + dy, c, T) / p - 1
        aprox1 = -mod * dy
        aprox2 = aprox1 + conv / 2 * dy * dy
        print(f"dy {dy*1e4:+.0f} pb: real {100*real:+.3f}% | solo duracion {100*aprox1:+.3f}% | + convexidad {100*aprox2:+.3f}%")

    print("\n== 2. TLT contra FRED DGS20 (diario) ==")
    t = dh.yahoo_historia("TLT")
    tlt = dict(zip(t["fechas"], t["precios"]))
    g = {d: v for d, v in datos.fred_serie("DGS20")}
    fechas = sorted(set(tlt) & set(g))
    filas = []
    for a, b in zip(fechas, fechas[1:]):
        if (b - a).days > 5:
            continue
        r = tlt[b] / tlt[a] - 1
        dy = (g[b] - g[a]) / 100
        filas.append((b, r - g[a] / 100 / 252, dy))
    print(f"{filas[0][0]}..{filas[-1][0]} n={len(filas)} dias")
    for nombre, a, b_ in (("completo", 2002, 2100), ("2002-2011", 2002, 2011), ("2012-2019", 2012, 2019),
                          ("2020-2026", 2020, 2100)):
        x = [f for f in filas if a <= f[0].year <= b_]
        beta, r2 = ols([[1, f[2], f[2] ** 2] for f in x], [f[1] for f in x])
        print(f"{nombre}: n={len(x)} duracion empirica {-beta[1]:.2f} | convexidad empirica {2*beta[2]:.0f} | R2 {r2:.3f}")
    grandes = [f for f in filas if abs(f[2]) >= 0.0015]
    beta, r2 = ols([[1, f[2], f[2] ** 2] for f in grandes], [f[1] for f in grandes])
    print(f"dias |dy|>=15 pb: n={len(grandes)} duracion {-beta[1]:.2f} convexidad {2*beta[2]:.0f} R2 {r2:.3f}")

    print("\n== 3. Choques extremos (2020-2026): prediccion con D y C del periodo ==")
    x = [f for f in filas if f[0].year >= 2020]
    beta, _ = ols([[1, f[2], f[2] ** 2] for f in x], [f[1] for f in x])
    D, C = -beta[1], 2 * beta[2]
    ext = sorted(x, key=lambda f: f[2])[:5] + sorted(x, key=lambda f: f[2])[-5:]
    errs = []
    for f in ext:
        pred = -D * f[2] + C / 2 * f[2] ** 2
        errs.append(abs(f[1] - pred))
        print(f"{f[0]} dy {f[2]*1e4:+.0f} pb: TLT {100*f[1]:+.2f}% pred {100*pred:+.2f}%")
    print(f"error absoluto medio en extremos: {100*st.mean(errs):.2f} pp")


if __name__ == "__main__":
    main()
