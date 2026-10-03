"""Ficha 2026-10-02 (trabajo continuo): ¿cuánto crecimiento esperado gana o pierde la cartera W40
(modo C moderado: 40% SPY, 27% QQQ, 27% UPRO, 6% efectivo) frente a la cartera A (56% SPY, 27% QQQ,
17% efectivo), según la prima de riesgo que se suponga? En MXN sobre 20,000 (papel) y 10,000 (real),
para una temporada de 4 meses (85 días hábiles).

Modelo: g = r_f + w'μ_exc − ½ w'Σw − costos; UPRO = 3x S&P diario con financiamiento 2×r_f y gasto 0.91%.
Parámetros: σ S&P 16%, σ Nasdaq-100 21%, correlación 0.90, r_f 5.0% (T-bill), r MXN de efectivo 7% (CETES)
para la parte en efectivo. Primas del S&P en exceso: 0, 2, 4, 6 y 8%; Nasdaq = S&P + 1 pp.
Monte Carlo lognormal (20,000 caminos) para P(pérdida) y P(−12%) en la temporada, sin FX ni stop.
Solo stdlib. Semilla 20261002.
"""
import math
import random
import statistics as st

random.seed(20261002)
SIG = {"spx": 0.16, "ndx": 0.21}
RHO = 0.90
RF = 0.050
CETES = 0.07
DIAS = 85
GASTO_UPRO = 0.0091


def momentos(w_spx, w_ndx, w_upro, w_cash, mu_spx):
    mu_ndx = mu_spx + 0.01
    # exposición efectiva al S&P (UPRO = 3x) y al Nasdaq
    e_spx = w_spx + 3 * w_upro
    e_ndx = w_ndx
    var = (e_spx * SIG["spx"]) ** 2 + (e_ndx * SIG["ndx"]) ** 2 + 2 * e_spx * e_ndx * RHO * SIG["spx"] * SIG["ndx"]
    costo = w_upro * (GASTO_UPRO + 0 * RF)  # el financiamiento ya está en el exceso: UPRO paga 2×r_f
    arit = (w_spx + w_ndx + w_upro) * RF + e_spx * mu_spx + e_ndx * mu_ndx - w_upro * 2 * RF + w_cash * CETES - costo
    # nota: w_upro*(3*r_spx - 2*rf) = w_upro*rf + 3*w_upro*mu_spx ; ya contado arriba
    g = arit - var / 2
    return arit, math.sqrt(var), g


def simula(arit, sig, n=20000):
    t = DIAS / 252
    mu_log = (arit - sig ** 2 / 2) * t
    s = sig * math.sqrt(t)
    perdida = menos12 = 0
    finales = []
    for _ in range(n):
        # camino con 17 pasos semanales para el mínimo
        x, minimo = 0.0, 0.0
        for _ in range(17):
            x += random.gauss(mu_log / 17, s / math.sqrt(17))
            minimo = min(minimo, x)
        finales.append(math.exp(x) - 1)
        perdida += x < 0
        menos12 += math.exp(minimo) - 1 <= -0.12
    finales.sort()
    return perdida / n, menos12 / n, finales[n // 10], finales[n // 2], finales[9 * n // 10]


def main():
    carteras = {"A (56/27/0/17)": (0.56, 0.27, 0.0, 0.17), "W40 (40/27/27/6)": (0.40, 0.27, 0.27, 0.06),
                "Solo S&P 1x (100%)": (1.0, 0.0, 0.0, 0.0), "Kelly-medio aprox.": None}
    print("prima S&P | cartera | arit | σ | g (log anual) | g 4 meses | +MXN/20k | P(pérdida) | P(−12%) | p10/p50/p90 temporada")
    for mu in (0.0, 0.02, 0.04, 0.06, 0.08):
        for nombre, w in carteras.items():
            if w is None:
                # medio Kelly sobre el S&P: L = 0.5 * mu/σ², resto en CETES
                L = max(0.0, 0.5 * mu / SIG["spx"] ** 2)
                w = (min(L, 1.0), 0.0, max(0.0, (L - 1) / 3), max(0.0, 1 - min(L, 1.0) - max(0.0, (L - 1) / 3)))
                nombre = f"Kelly-medio (L={L:.2f})"
            arit, sig, g = momentos(*w, mu)
            g4 = math.exp(g * DIAS / 252) - 1
            pp, p12, p10, p50, p90 = simula(arit, sig)
            print(f"{100*mu:4.0f}% | {nombre:22s} | {100*arit:5.2f}% | {100*sig:5.1f}% | {100*g:5.2f}% | {100*g4:5.2f}% | "
                  f"{20000*g4:7.0f} | {pp:.2f} | {p12:.2f} | {100*p10:+.1f}/{100*p50:+.1f}/{100*p90:+.1f}%")
        print()


if __name__ == "__main__":
    main()
