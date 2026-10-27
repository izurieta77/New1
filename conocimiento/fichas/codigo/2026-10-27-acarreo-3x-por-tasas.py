"""Ficha 2026-10-27: crecimiento geométrico de un 3x diario con acarreo y brecha real (R20).
G(L) ≈ L·μ − (L−1)·r − c − b(L) − L²σ²/2  (aprox. continua; μ, r, σ anuales; c comisión; b brecha real)
Comprobación 1: fórmula cerrada. Comprobación 2: Monte Carlo diario (rebalanceo diario exacto).
Uso: python3 -I este.py"""
import math, random
MU, SIG = 0.08, 0.17            # supuestos ilustrativos del S&P TR (no pronóstico)
C = 0.0091
def g_cerrada(L, r, b):
    return L * MU - (L - 1) * r - (C if L > 1 else 0) - b - L * L * SIG * SIG / 2
def g_mc(L, r, b, anos=2000, seed=7):
    random.seed(seed); dt = 1 / 252; lg = 0.0
    mu_d = MU * dt; s_d = SIG * math.sqrt(dt)
    for _ in range(int(anos * 252)):
        # log-normal del índice con media aritmética diaria mu_d; variables antitéticas (z, −z) para quitar la deriva muestral
        z = random.gauss(0, 1)
        for zz in (z, -z):
            rt = math.exp(mu_d - s_d * s_d / 2 + s_d * zz) - 1
            rl = L * rt - ((L - 1) * r + (C if L > 1 else 0) + b) * dt
            lg += math.log1p(rl)
    return lg / (2 * anos)
print("L | r | brecha b | G cerrada | G Monte Carlo")
for r in (0.001, 0.02, 0.038):
    for L, b in ((1, 0.0), (3, 0.0), (3, 0.013), (3, 0.023)):
        print(f"{L} | {r:.3f} | {b:.3f} | {g_cerrada(L, r, b)*100:6.2f}% | {g_mc(L, r, b, anos=400)*100:6.2f}%")
# L* que maximiza G sin brecha: dG/dL = μ − r − Lσ² = 0
for r in (0.001, 0.02, 0.038):
    print(f"r={r:.3f}: L* = {(MU - r)/SIG**2:.2f}; G(3)-G(1) sin brecha = {(g_cerrada(3,r,0)-g_cerrada(1,r,0))*100:.2f} pp; con brecha R20 alto (2.3) = {(g_cerrada(3,r,0.023)-g_cerrada(1,r,0))*100:.2f} pp")
# Equilibrio: μ mínimo para que el 3x empate al 1x con r=3.8% y b=2.3%
r, b = 0.038, 0.023
mu_eq = ((3 - 1) * r + C + b + (9 - 1) * SIG ** 2 / 2) / 2
print(f"μ de empate 3x = 1x con r=3.8%, b=2.3%, σ=17%: {mu_eq*100:.2f}%")
