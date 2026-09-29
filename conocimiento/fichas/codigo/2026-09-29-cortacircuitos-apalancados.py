"""Ficha 2026-09-29 (continuación de 2026-09-28): cortacircuitos de la arena con apalancamiento (modo C).
Temporadas de 85 días hábiles, 1996-2026, medidas en MXN. Simulador de R06: r_L = L*r - (L-1)*rf - 0.9%/252.
Filtro: ^GSPC (precio) < SMA200 al cierre de t -> el sleeve apalancado está en efectivo (rf) el día t+1.
Variante con VIX: además exige ^VIX < 25 al cierre de t. Sin acciones de los cortacircuitos (peor caso).
"""
import math, sys, bisect
sys.path.insert(0, '.')
from herramientas import datos

N = 85; NIV = [0.12, 0.20, 0.28, 0.35, 0.50]
tr = dict(datos.yahoo_serie('^SP500TR', rango='30y'))
px = dict(datos.yahoo_serie('^GSPC', rango='30y'))
vx = dict(datos.yahoo_serie('^VIX', rango='30y'))
def asof(serie):
    ks = [k for k, _ in serie]; vs = [v for _, v in serie]
    return lambda d: vs[bisect.bisect_right(ks, d) - 1] if bisect.bisect_right(ks, d) else None
fx = asof(datos.fred_serie('DEXMXUS', desde='1995-01-01'))
rf = asof(datos.fred_serie('DTB3', desde='1995-01-01'))
fechas = sorted(d for d in tr if d in px)
cerr = [px[d] for d in fechas]
sma = [None]*len(fechas)
acc = 0
for i, c in enumerate(cerr):
    acc += c
    if i >= 200: acc -= cerr[i-200]
    if i >= 199: sma[i] = acc/200
filas = []  # (fecha, r_usd, rf_d, fx_ratio, filtro_sma(t-1), filtro_vix(t-1))
for i in range(200, len(fechas)):
    d0, d1 = fechas[i-1], fechas[i]
    f0, f1 = fx(d0), fx(d1); r0 = rf(d1)
    if not (f0 and f1 and r0 is not None): continue
    on_sma = cerr[i-1] > sma[i-1]
    v = vx.get(d0)
    on_vix = on_sma and (v is not None and v < 25)
    filas.append((d1, tr[d1]/tr[d0]-1, r0/100/252, f1/f0, on_sma, on_vix))
print(f"Datos: {filas[0][0]} a {filas[-1][0]}, n={len(filas)}")

def r_lev(L, r, rfd):
    return L*r - (L-1)*rfd - (0.009/252 if L > 1 else 0)
def diario(cartera, f):
    _, r, rfd, fxr, on_s, on_v = f
    total = 0
    for peso, L, filtro in cartera:
        activo = {'nada': True, 'sma': on_s, 'vix': on_v}[filtro]
        rl = r_lev(L, r, rfd) if activo else rfd
        total += peso * ((1 + rl) * fxr - 1)
    return total
CARTERAS = {
    'A actual: 100% 1x': [(1.0, 1, 'nada')],
    'C1: 50% 3x sin filtro + 50% 1x': [(0.5, 3, 'nada'), (0.5, 1, 'nada')],
    'C2: 50% 3x filtro SMA200 + 50% 1x': [(0.5, 3, 'sma'), (0.5, 1, 'nada')],
    'C3: 50% 3x filtro SMA200+VIX + 50% 1x': [(0.5, 3, 'vix'), (0.5, 1, 'nada')],
    'C4: 100% 3x filtro SMA200': [(1.0, 3, 'sma')],
}
for nombre, cart in CARTERAS.items():
    diarios = [diario(cart, f) for f in filas]
    cnt = {a: 0 for a in NIV}; rets = []; n = 0
    for i in range(0, len(diarios) - N, 5):
        w = 1; pico = 1; mdd = 0
        for r in diarios[i:i+N]:
            w *= 1 + r; pico = max(pico, w); mdd = max(mdd, 1 - w/pico)
        n += 1; rets.append(w - 1)
        for a in NIV: cnt[a] += mdd >= a
    rets.sort()
    q = lambda p: rets[int(p*(len(rets)-1))]
    print(f"\n{nombre} ({n} temporadas)")
    print("  P(DD desde el pico): " + "  ".join(f"-{a:.0%}: {cnt[a]/n:.3f}" for a in NIV))
    print(f"  Rend. de temporada MXN: p10 {q(.1):+.1%}  mediana {q(.5):+.1%}  p90 {q(.9):+.1%}  P(>+40%) {sum(r>0.40 for r in rets)/n:.3f}")
