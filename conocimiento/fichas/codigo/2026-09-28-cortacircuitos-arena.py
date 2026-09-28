"""Ficha 2026-09-28: probabilidad de tocar los cortacircuitos de la arena en una temporada de 4 meses.
Datos: Yahoo ^SP500TR (diario, rango 30y; range=max degrada a barras trimestrales) x FRED DEXMXUS (MXN por USD). Solo stdlib + herramientas.datos.
1) Fórmula cerrada (browniano con deriva, horizonte finito) para P(drawdown desde el inicio <= -a).
2) Histórico: temporadas móviles de 85 días hábiles, 1996-2026, en MXN y en USD; DD desde el inicio y desde el pico.
3) Comprobación de E[MDD] ~ 1.25 sigma sqrt(T) sin deriva (cap. 07 §2.7).
"""
import math, random, sys, bisect
sys.path.insert(0, '.')
from herramientas import datos

N = 85                       # días hábiles 28-sep-2026 a 28-ene-2027 (aprox.)
NIV = [0.12, 0.20, 0.28, 0.35, 0.50]
Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))

sp = datos.yahoo_serie('^SP500TR', rango='30y', intervalo='1d')
fx = datos.fred_serie('DEXMXUS', desde='1993-11-01')
fxd = [d for d, _ in fx]; fxv = [v for _, v in fx]
def fx_en(d):
    i = bisect.bisect_right(fxd, d) - 1
    return fxv[i] if i >= 0 else None
serie = [(d, v, fx_en(d)) for d, v in sp if d >= fxd[0]]
serie = [(d, v, f) for d, v, f in serie if f]
print(f"Datos: {serie[0][0]} a {serie[-1][0]}, n={len(serie)}")

def rend(moneda):
    return [ (v*(f if moneda=='MXN' else 1)) for _, v, f in serie]

def estadisticas(niveles):
    lr = [math.log(niveles[i]/niveles[i-1]) for i in range(1, len(niveles))]
    m = sum(lr)/len(lr); s = math.sqrt(sum((x-m)**2 for x in lr)/(len(lr)-1))
    return m, s

for moneda in ('MXN', 'USD'):
    x = rend(moneda)
    mu, sg = estadisticas(x)
    print(f"\n== {moneda}: mu diaria {mu:.5f} ({mu*252:.2%}/a), sigma diaria {sg:.4f} ({sg*math.sqrt(252):.2%}/a)")
    # 1) cerrada: P(min log W_t <= ln(1-a)) en T=N con deriva mu
    T = N
    print("  Fórmula cerrada (DD desde el inicio):", end=' ')
    for a in NIV:
        b = -math.log(1-a)
        p = Phi((-b - mu*T)/(sg*math.sqrt(T))) + math.exp(-2*mu*b/sg**2)*Phi((-b + mu*T)/(sg*math.sqrt(T)))
        print(f"-{a:.0%}: {p:.3f}", end='  ')
    print()
    # 2) histórico, ventanas que empiezan cada 5 días
    cuenta_ini = {a: 0 for a in NIV}; cuenta_pico = {a: 0 for a in NIV}; n = 0; mdds = []
    for i in range(0, len(x) - N, 5):
        w = x[i:i+N+1]; base = w[0]; pico = base; mdd = 0; mini = 1
        for v in w:
            pico = max(pico, v); mdd = max(mdd, 1 - v/pico); mini = min(mini, v/base)
        n += 1; mdds.append(mdd)
        for a in NIV:
            cuenta_ini[a] += (1 - mini) >= a
            cuenta_pico[a] += mdd >= a
    print(f"  Histórico ({n} temporadas):")
    print("   DD desde el inicio: " + "  ".join(f"-{a:.0%}: {cuenta_ini[a]/n:.3f}" for a in NIV))
    print("   DD desde el pico:   " + "  ".join(f"-{a:.0%}: {cuenta_pico[a]/n:.3f}" for a in NIV))
    mdds.sort()
    print(f"   MDD de temporada: mediana {mdds[len(mdds)//2]:.1%}, p90 {mdds[int(.9*len(mdds))]:.1%}, peor {mdds[-1]:.1%}")

# 3) E[MDD] sin deriva
random.seed(20260928)
sig = 0.01; M = 1000; R = 2000; acc = 0
for _ in range(R):
    lw = 0; pk = 0; md = 0
    for _ in range(M):
        lw += sig * random.gauss(0, 1); pk = max(pk, lw); md = max(md, pk - lw)
    acc += md
print(f"\nE[MDD] log sin deriva / (sigma sqrt T): {acc/R/(sig*math.sqrt(M)):.3f} (teórico sqrt(pi/2)={math.sqrt(math.pi/2):.3f})")
