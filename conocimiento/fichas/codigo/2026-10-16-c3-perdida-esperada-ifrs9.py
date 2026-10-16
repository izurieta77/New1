#!/usr/bin/env python3
"""Ficha 16-oct-2026 (Doctorado contabilidad C3): pérdida crediticia esperada (IFRS 9) y el "efecto escalón".

ECL = sum_t PD_marginal(t) x LGD x EAD(t) x DF(t). Etapa 1: solo el primer año (12 meses).
Etapa 2: toda la vida. Etapa 3: toda la vida, con PD = 1, y los intereses se reconocen sobre el neto.
Supuestos ilustrativos (no de ningún banco): préstamo amortizable a 5 años, PD anual 1% (etapa 1)
que sube a 4% si el riesgo aumenta de forma significativa, LGD 45%, tasa efectiva 8%.
Corre con python3 -I; las aserciones son la comprobación.
"""

def saldos(principal=1000.0, anios=5):
    return [principal * (anios - t) / anios for t in range(anios)]  # EAD al inicio de cada año

def ecl(pd_anual, lgd=0.45, tasa=0.08, anios_horizonte=5):
    sob, total = 1.0, 0.0
    for t, ead in enumerate(saldos()[:anios_horizonte]):
        pd_marg = sob * pd_anual
        total += pd_marg * lgd * ead / (1 + tasa) ** (t + 1)
        sob *= 1 - pd_anual
    return total

e1 = ecl(0.01, anios_horizonte=1)        # etapa 1: 12 meses
e2_misma_pd = ecl(0.01)                  # vida total, sin deterioro (solo para aislar el horizonte)
e2 = ecl(0.04)                           # etapa 2: vida total con PD mayor
print(f"Etapa 1 (12 meses, PD 1%): {e1:.2f}; vida total con PD 1%: {e2_misma_pd:.2f}; etapa 2 (PD 4%): {e2:.2f}")
assert abs(e1 - 0.01 * 0.45 * 1000 / 1.08) < 1e-9          # 4.1667
assert e2 > 6 * e1                                            # el escalón: de 4.17 a 43.18 por 1,000 (x10.4)

# Cartera de 100,000: si 10% migra de etapa 1 a 2, ¿cuánto sube la provisión?
cartera, mig = 100_000.0, 0.10
prov_antes = cartera / 1000 * e1
prov_despues = cartera * (1 - mig) / 1000 * e1 + cartera * mig / 1000 * e2
print(f"Provisión: {prov_antes:,.0f} -> {prov_despues:,.0f} (x{prov_despues/prov_antes:.2f}) con 10% en etapa 2")
assert prov_despues / prov_antes > 1.5

# Etapa 3: intereses sobre el neto (costo amortizado) en vez del bruto
bruto, prov3, tasa = 1000.0, 450.0, 0.08
int_bruto, int_neto = bruto * tasa, (bruto - prov3) * tasa
print(f"Intereses etapa 3: {int_neto:.0f} sobre el neto contra {int_bruto:.0f} sobre el bruto")
assert int_neto == 44.0 and int_bruto == 80.0
print("Comprobaciones OK")
