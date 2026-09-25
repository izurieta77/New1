"""Comprobación numérica de la ficha 2026-09-25-kelly-fraccional (solo stdlib).
1) Fórmula cerrada: fracción del crecimiento 2c-c^2 y P(tocar x) = x^(2/c-1) (r=0).
2) Monte Carlo mensual con horizonte finito (30 años) y deriva lognormal.
3) Caso binario p=0.55, b=1 (crecimiento exacto por esperanza).
4) Error de estimación: ventaja real = mitad de la estimada.
5) Contraejemplo: salto de -30% en un mes con apalancamiento Kelly completo.
"""
import math, random
random.seed(20260925)
MU_EX, SIG = 0.05, 0.16          # prima 5%, vol 16% (supuestos del cap. 07)
FSTAR = MU_EX / SIG**2           # 1.953
SR = MU_EX / SIG
print(f"f* continuo = {FSTAR:.3f}; SR = {SR:.4f}; g*(exceso) = SR^2/2 = {SR**2/2:.4%}")

def g(c, r=0.0):
    return r + SR**2 * (c - c*c/2)
print("\n1) Fórmula cerrada (r=0, horizonte infinito)")
for c in (1.0, 0.5, 0.25, 2.0):
    fr = (2*c - c*c)
    ps = [x**(2/c - 1) if c < 2 else float('nan') for x in (0.8, 0.65, 0.5)]
    print(f"  c={c:4.2f} crec={fr:6.1%} vol_rel={c:.2f} P(-20/-35/-50%)=" + "/".join(f"{p:.3f}" for p in ps))

print("\n2) Monte Carlo mensual, 30 años, 6000 trayectorias, r=0 (exceso)")
def mc(c, anios=30, n=20000, r=0.0, mu_real=MU_EX):
    w = c * FSTAR
    dt = 1/12
    m = (r + w*mu_real - 0.5*(w*SIG)**2) * dt
    s = w * SIG * math.sqrt(dt)
    toques = {0.8: 0, 0.65: 0, 0.5: 0}; logs = []
    for _ in range(n):
        lw, mn = 0.0, 0.0
        for _ in range(anios*12):
            lw += m + s*random.gauss(0, 1)
            if lw < mn: mn = lw
        for x in toques:
            if mn <= math.log(x): toques[x] += 1
        logs.append(lw)
    return {x: v/n for x, v in toques.items()}, sum(logs)/n/anios
for c in (1.0, 0.5, 0.25):
    t, gm = mc(c, n=6000)
    print(f"  c={c:4.2f} g_emp={gm:.4%} (teo {g(c):.4%}) P(-20/-35/-50%)={t[0.8]:.3f}/{t[0.65]:.3f}/{t[0.5]:.3f}")

print("\n3) Binario p=0.55, b=1: crecimiento esperado por apuesta")
p, b = 0.55, 1.0
fb = p - (1-p)/b
gb = lambda f: p*math.log(1+b*f) + (1-p)*math.log(1-f)
for c in (1.0, 0.5, 0.25, 2.0):
    print(f"  c={c:4.2f} f={c*fb:.3f} g/g*={gb(c*fb)/gb(fb):7.1%}")

print("\n4) Error de estimación: crees c=0.5, la prima real es la mitad (2.5%)")
c_efectiva = 0.5 * FSTAR / ((MU_EX/2)/SIG**2)
print(f"  c efectiva = {c_efectiva:.2f}; P(-35%) teórica pasa de {0.65**3:.3f} a {0.65**(2/c_efectiva-1):.3f}")
c_tope = 0.25 * FSTAR / ((MU_EX/2)/SIG**2)
print(f"  con tope 0.25: c efectiva = {c_tope:.2f}; P(-35%) = {0.65**(2/c_tope-1):.3f}")

print("\n5) Contraejemplo: salto de -30% en un mes (no lognormal)")
for c in (1.0, 0.5, 0.25):
    w = c*FSTAR
    print(f"  c={c:4.2f} peso={w:.2f}x -> riqueza tras el salto = {max(0,1 - 0.30*w):.3f}")

print("\n6) Con r=4% (nominal, sin restar cetes): exponente 2g/(c SR)^2")
for c in (1.0, 0.5, 0.25):
    e = 2*g(c, 0.04)/(c*SR)**2
    print(f"  c={c:4.2f} P(-35%) = {0.65**e:.4f} (vs r=0: {0.65**(2/c-1):.4f})")
