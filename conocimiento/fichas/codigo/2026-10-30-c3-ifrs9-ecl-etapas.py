"""Ficha 2026-10-30 · C3 · IFRS 9 / AASB 9 §5.5: pérdida esperada de 12 meses (etapa 1) contra la de toda la vida (etapa 2),
ponderada por escenarios (5.5.17 a), con valor del dinero en el tiempo (5.5.17 b) y horizonte contractual (5.5.19).
ECL = Σ_t PD_marginal(t) · LGD · EAD(t) · DF(t). Comprobación 2: Monte Carlo de incumplimientos.
Uso: python3 -I este.py"""
import math, random

def ecl(pd_anual, lgd, ead0, años, tasa, amort=True, horizonte=None):
    h = años if horizonte is None else min(horizonte, años)
    sup, tot = 1.0, 0.0
    for t in range(1, h + 1):
        pd_m = sup * pd_anual                      # PD marginal del año t (riesgo constante)
        ead = ead0 * (1 - (t - 1) / años) if amort else ead0
        tot += pd_m * lgd * ead / (1 + tasa) ** t
        sup *= 1 - pd_anual
    return tot

# Préstamo de 1,000 a 5 años, amortización lineal, tasa efectiva de 12%, LGD de 45%
EAD, AÑOS, TASA, LGD = 1000.0, 5, 0.12, 0.45
esc = [("base", 0.60, 0.02), ("adverso", 0.30, 0.05), ("severo", 0.10, 0.12)]   # (nombre, peso, PD anual)
def ponderada(h):
    return sum(w * ecl(pd, LGD, EAD, AÑOS, TASA, horizonte=h) for _, w, pd in esc)
e12, evida = ponderada(1), ponderada(None)
print(f"ECL 12 meses (etapa 1) ponderada = {e12:.2f}  ({e12/EAD:.2%} de la EAD)")
print(f"ECL vida (etapa 2) ponderada     = {evida:.2f}  ({evida/EAD:.2%}); razón vida/12m = {evida/e12:.2f}x")
# no linealidad: ECL con la PD promedio ponderada ≠ ECL ponderada (5.5.17 a exige ponderar resultados)
pd_prom = sum(w * pd for _, w, pd in esc)
print(f"ECL vida con PD promedio ({pd_prom:.3f}) = {ecl(pd_prom, LGD, EAD, AÑOS, TASA):.2f} contra ponderada {evida:.2f}")

# Efecto escalón en una cartera: 10,000 préstamos; qué pasa con la reserva si 10% pasa a etapa 2
for frac in (0.0, 0.05, 0.10, 0.20):
    res = (1 - frac) * e12 + frac * evida
    print(f"  {frac:.0%} en etapa 2 → reserva {res:.2f} por préstamo ({res/e12 - 1:+.0%} contra todo en etapa 1)")

# Segunda comprobación: Monte Carlo del escenario adverso, vida completa, con descuento
random.seed(9); N = 200000; pd = 0.05; tot = 0.0
for _ in range(N):
    for t in range(1, AÑOS + 1):
        if random.random() < pd:
            tot += LGD * EAD * (1 - (t - 1) / AÑOS) / (1 + TASA) ** t; break
print(f"Monte Carlo adverso (vida): {tot/N:.2f} contra cerrada {ecl(0.05, LGD, EAD, AÑOS, TASA):.2f}")
