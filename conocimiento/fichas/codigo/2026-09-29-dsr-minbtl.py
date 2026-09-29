"""Ficha 2026-09-29: PSR, DSR y MinBTL. Comprobación de las fórmulas de metricas.py por simulación (stdlib).
1) E[max SR] de N estrategias sin habilidad: fórmula (Bailey-LdP) vs Monte Carlo.
2) MinBTL: años mínimos para que E[max SR] (anual) de N pruebas sin habilidad no llegue a 1.
3) PSR: tasa de falsos positivos con SR verdadero 0 y datos normales vs colas gruesas.
4) Ejemplo del paper del DSR (SR 2.5, T 1250, N 100, V 0.5, asim -3, curt 10) con metricas.
5) Aplicación: temporada de la arena (85 días) — ¿cuánto Sharpe se puede distinguir de 0?
"""
import math, random, sys, statistics as st
sys.path.insert(0, '.')
from herramientas import metricas as m
random.seed(20260929)
Nd = st.NormalDist()
g = 0.5772156649

def emax(N, V=1.0):
    return math.sqrt(V) * ((1-g)*Nd.inv_cdf(1-1/N) + g*Nd.inv_cdf(1-1/(N*math.e)))

print("1) E[max] de N normales estándar: fórmula vs Monte Carlo (20,000 réplicas)")
for N in (10, 45, 100, 1000):
    mc = sum(max(random.gauss(0,1) for _ in range(N)) for _ in range(20000 if N<1000 else 3000)) / (20000 if N<1000 else 3000)
    print(f"   N={N:5d}  fórmula {emax(N):.3f}  MC {mc:.3f}  metricas.sharpe_maximo_esperado {m.sharpe_maximo_esperado(N,1.0):.3f}")

print("\n2) MinBTL (años) = (E[max] con V=1 / SR anual objetivo)^2, SR objetivo 1")
for N in (2, 7, 10, 45, 100, 1000):
    print(f"   N={N:5d}: {emax(N)**2:.2f} años")

print("\n3) PSR(0) >= 0.95 con SR verdadero = 0 (tasa de falsos positivos), T=252 días, 4,000 réplicas")
for nombre, gen in [("normal", lambda: random.gauss(0, 0.01)),
                    ("t de Student 3 gl", lambda: 0.01*random.gauss(0,1)/math.sqrt(sum(random.gauss(0,1)**2 for _ in range(3))/3))]:
    fp = 0; R = 4000
    for _ in range(R):
        x = [gen() for _ in range(252)]
        mu = sum(x)/252; sd = math.sqrt(sum((v-mu)**2 for v in x)/251)
        sr = mu/sd
        a = m.asimetria(x); k = m.curtosis(x)
        p = m.psr_desde_estadisticos(sr, 252, a, k, 0.0)
        fp += p >= 0.95
    print(f"   {nombre}: {fp/R:.3f} (nominal 0.05)")

print("\n4) Ejemplo del paper DSR con metricas.dsr_desde_estadisticos")
sr_d = 2.5/math.sqrt(252)
print("   DSR =", round(m.dsr_desde_estadisticos(sr_d, 1250, 100, 0.5/252, -3, 10), 4))

print("\n5) Temporada de 85 días: SR anual mínimo para PSR(0) >= 0.95 (normal)")
T = 85
sr_d_min = Nd.inv_cdf(0.95) / math.sqrt(T - 1)
print(f"   SR diario {sr_d_min:.4f} -> anual {sr_d_min*math.sqrt(252):.2f}")
