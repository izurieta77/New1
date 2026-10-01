"""Ficha 2026-10-01: Brier, su descomposición y el poder estadístico del criterio de salida.

1. Descomposición de Murphy (1973): BS = REL - RES + UNC, comprobada como identidad exacta
   con pronósticos en valores discretos.
2. Brier esperado de un pronosticador PERFECTAMENTE calibrado = E[p(1-p)]: depende de la
   nitidez (qué tan lejos de 0.5 están los pronósticos), no solo de la habilidad.
   Se calcula con la mezcla real de probabilidades de bitacora/pronosticos.csv.
3. Distribución del Brier con n = 50 y P(Brier <= 0.20) para varios pronosticadores.
4. n necesario para distinguir 0.20 de 0.25 con 80% de poder.

Solo stdlib. Semilla 20261001. Uso: python3 conocimiento/fichas/codigo/2026-10-01-brier-poder.py
"""
import csv
import math
import random
import statistics as st
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
random.seed(20261001)


def brier(ps, os_):
    return sum((p - o) ** 2 for p, o in zip(ps, os_)) / len(ps)


def murphy(ps, os_):
    n = len(ps)
    obar = sum(os_) / n
    grupos = {}
    for p, o in zip(ps, os_):
        grupos.setdefault(p, []).append(o)
    rel = sum(len(g) * (p - sum(g) / len(g)) ** 2 for p, g in grupos.items()) / n
    res = sum(len(g) * (sum(g) / len(g) - obar) ** 2 for g in grupos.values()) / n
    unc = obar * (1 - obar)
    return rel, res, unc


def main():
    print("== 1. Identidad de Murphy con pronósticos discretos ==")
    niveles = [0.1, 0.3, 0.5, 0.7, 0.9]
    ps = [random.choice(niveles) for _ in range(2000)]
    os_ = [1 if random.random() < min(1, max(0, p + 0.05)) else 0 for p in ps]  # sesgo de +5 pp
    rel, res, unc = murphy(ps, os_)
    print(f"BS={brier(ps, os_):.6f}  REL-RES+UNC={rel - res + unc:.6f}  (REL {rel:.4f}, RES {res:.4f}, UNC {unc:.4f})")

    print("\n== 2. Brier esperado si el pronosticador está perfectamente calibrado: E[p(1-p)] ==")
    filas = list(csv.DictReader(open(RAIZ / "bitacora/pronosticos.csv", newline="", encoding="utf-8")))
    probs = [float(r["probabilidad"]) for r in filas]
    e = st.mean(p * (1 - p) for p in probs)
    print(f"Bitácora: n={len(probs)} pronósticos; media |p-0.5| = {st.mean(abs(p-0.5) for p in probs):.3f}; "
          f"E[p(1-p)] = {e:.4f}  <- Brier esperado AUN con calibración perfecta")
    for p in (0.5, 0.6, 0.7, 0.75, 0.8, 0.9):
        print(f"  todos los pronósticos en {p:.2f}/{1-p:.2f}: Brier esperado {p*(1-p):.4f}")

    print("\n== 3. Distribución del Brier con n = 50 (20,000 simulaciones) ==")
    def simula(probs_reales, sesgo=0.0, n=50, reps=20000):
        res = []
        for _ in range(reps):
            muestra = [random.choice(probs_reales) for _ in range(n)]
            b = 0.0
            for q in muestra:  # q = probabilidad verdadera; pronóstico = q + sesgo (sobreconfianza si se aleja de 0.5)
                f = min(0.99, max(0.01, q + sesgo * (1 if q > 0.5 else -1)))
                o = 1 if random.random() < q else 0
                b += (f - o) ** 2
            res.append(b / n)
        res.sort()
        return st.mean(res), res[len(res) // 20], res[-len(res) // 20], sum(x <= 0.20 for x in res) / len(res)
    casos = {
        "Calibrado, mezcla actual de la bitácora": (probs, 0.0),
        "Calibrado, nitidez media (p en 0.25/0.75)": ([0.25, 0.75], 0.0),
        "Calibrado, nítido (p en 0.15/0.85)": ([0.15, 0.85], 0.0),
        "Sobreconfiado +10 pp sobre la mezcla actual": (probs, 0.10),
    }
    for nombre, (pr, s) in casos.items():
        m, p5, p95, ok = simula(pr, s)
        print(f"{nombre}: media {m:.4f}, IC90% [{p5:.4f}, {p95:.4f}], P(Brier<=0.20) = {ok:.2f}")

    print("\n== 4. n para distinguir 0.20 de 0.25 (una cola, 5%, poder 80%) ==")
    # Varianza por pronóstico de (f-o)^2 con f calibrado: var = E[(f-o)^4] - E[(f-o)^2]^2
    for nombre, pr in (("mezcla actual", probs), ("p en 0.25/0.75", [0.25, 0.75])):
        m2 = st.mean(q * (1 - q) ** 2 + (1 - q) * q ** 2 for q in pr)
        m4 = st.mean(q * (1 - q) ** 4 + (1 - q) * q ** 4 for q in pr)
        var_item = m4 - m2 ** 2
        n = ((1.645 + 0.842) * math.sqrt(var_item) / 0.05) ** 2
        print(f"{nombre}: sd por pronóstico {math.sqrt(var_item):.3f}; SE con n=50 {math.sqrt(var_item/50):.4f}; n necesario ~{n:.0f}")


if __name__ == "__main__":
    main()
