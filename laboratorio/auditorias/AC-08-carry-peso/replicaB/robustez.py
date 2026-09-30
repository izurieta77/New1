"""Robustez de la Réplica B: convención de tasa, plazo del T-bill, <= vs <, persistencia, n independientes."""
from __future__ import annotations
import bisect, csv, os
from datetime import date, timedelta
import numpy as np

D = os.path.dirname(os.path.abspath(__file__))
INICIO = date(2006, 1, 1)


def leer(n):
    out = []
    with open(f"{D}/{n}.csv") as f:
        r = csv.reader(f); next(r)
        for row in r:
            if len(row) > 1 and row[1] not in ("", "."):
                out.append((date.fromisoformat(row[0]), float(row[1])))
    return sorted(out)


cetes, tb3, tb4, fix = leer("SF43936"), leer("DTB3"), leer("DTB4WK"), leer("SF43718")
fx_d = [d for d, _ in fix]; fx_v = [v for _, v in fix]; ULT = fx_d[-1]


def asof(serie, t, maxd=7):
    ds = [d for d, _ in serie] if not isinstance(serie, tuple) else serie[0]
    i = bisect.bisect_right(ds, t) - 1
    if i < 0 or (t - ds[i]).days > maxd:
        return None
    return serie[i][1]


tb3_d = [d for d, _ in tb3]; tb4_d = [d for d, _ in tb4]


def av(ds, s, t, maxd=7):
    i = bisect.bisect_right(ds, t) - 1
    if i < 0 or (t - ds[i]).days > maxd:
        return None
    return s[i][1]


def fxat(t):
    i = bisect.bisect_right(fx_d, t) - 1
    return fx_v[i]


def mmy(d, dias):  # descuento -> rendimiento money-market act/360 (convención CETES)
    d = d / 100
    return 100 * 360 * d / (360 - dias * d)


def serie(variante):
    out = []
    for t, c in cetes:
        if variante == "DTB3":
            x = av(tb3_d, tb3, t)
        elif variante == "DTB3_mmy":
            x = av(tb3_d, tb3, t); x = None if x is None else mmy(x, 91)
        elif variante == "DTB4WK_mmy":
            x = av(tb4_d, tb4, t); x = None if x is None else mmy(x, 28)
        if x is None:
            continue
        out.append((t, c - x))
    return out


def fwd(t, dias):
    t1 = t + timedelta(days=dias)
    if t1 > ULT:
        return None
    return 100 * (fxat(t1) / fxat(t) - 1)


def maxdep(t, dias=365):
    t1 = t + timedelta(days=dias)
    i0 = bisect.bisect_right(fx_d, t); i1 = bisect.bisect_right(fx_d, t1)
    m = max(fx_v[i0:i1])
    return 100 * (m / fxat(t) - 1), t1 <= ULT


def cruces(s, u, estricto=False, persist=1, sep=365):
    ev = []
    below = (lambda x: x < u) if estricto else (lambda x: x <= u)
    for i in range(1, len(s)):
        t = s[i][0]
        if t < INICIO:
            continue
        if below(s[i][1]) and not below(s[i - 1][1]):
            if persist > 1 and not all(below(s[j][1]) for j in range(i, min(i + persist, len(s)))):
                continue
            if ev and (t - ev[-1]).days < sep:
                continue
            ev.append(t)
    return ev


for var in ("DTB3", "DTB3_mmy", "DTB4WK_mmy"):
    s = serie(var)
    print(f"\n=== {var}: hoy {s[-1][0]} dif = {s[-1][1]:.2f}")
    for u in (2.5, 3.0, 3.5):
        for estricto in (False, True):
            for persist in (1, 4):
                ev = cruces(s, u, estricto, persist)
                txt = []
                for t in ev:
                    r12 = fwd(t, 365); m, completo = maxdep(t)
                    txt.append(f"{t}[12m {'n/d' if r12 is None else f'{r12:+.1f}'} max {m:+.1f}{'' if completo else '*'}]")
                print(f"  u={u} {'<' if estricto else '<='} persist={persist}: " + "  ".join(txt))
    # semanas <=3 y su max12, por régimen
    for u in (3.0,):
        sel = [(t, x) for t, x in s if t >= INICIO and x <= u and t + timedelta(days=365) <= ULT]
        por = {}
        for t, x in sel:
            k = "2006-07" if t.year <= 2008 else ("2013-16" if t.year <= 2017 else "otro")
            por.setdefault(k, []).append((fwd(t, 365), maxdep(t)[0]))
        for k, v in por.items():
            a = np.array(v)
            print(f"  semanas<=3 régimen {k}: n={len(v)} mediana 12m {np.median(a[:,0]):+.1f} rango [{a[:,0].min():+.1f},{a[:,0].max():+.1f}] "
                  f"mediana max12 {np.median(a[:,1]):+.1f} rango [{a[:,1].min():+.1f},{a[:,1].max():+.1f}] %max12>=14 {100*(a[:,1]>=14).mean():.0f}")

# tasa base: probabilidad de max12 >= 14% y 12m >= 14% en todas las semanas con ventana completa
s = serie("DTB3")
sel = [t for t, x in s if t >= INICIO and t + timedelta(days=365) <= ULT]
m12 = np.array([maxdep(t)[0] for t in sel]); c12 = np.array([fwd(t, 365) for t in sel])
print(f"\nBase 2006-2025 (n={len(sel)} semanas): P(max12>=14)={100*(m12>=14).mean():.0f}%  P(12m>=14)={100*(c12>=14).mean():.0f}%  "
      f"mediana max12 {np.median(m12):+.1f}  mediana 12m {np.median(c12):+.1f}")
# base por bloques anuales no traslapados (primer jueves de cada año)
anual = []
for y in range(2006, 2026):
    ts = [t for t in sel if t.year == y]
    if ts:
        anual.append((ts[0], fwd(ts[0], 365), maxdep(ts[0])[0]))
a = np.array([[x[1], x[2]] for x in anual])
print(f"Base anual no traslapada (n={len(anual)}): mediana 12m {np.median(a[:,0]):+.1f}, mediana max12 {np.median(a[:,1]):+.1f}, "
      f"#12m>=14: {(a[:,0]>=14).sum()}, #max12>=14: {(a[:,1]>=14).sum()}")
for t, c, m in anual:
    print(f"   {t} 12m {c:+6.1f} max12 {m:+6.1f}")

# comprobaciones puntuales
print("\nChequeos FIX:")
for t in [date(2006, 2, 23), date(2007, 2, 23), date(2014, 6, 12), date(2015, 6, 12), date(2015, 10, 8), date(2016, 10, 7),
          date(2026, 4, 9), date(2026, 9, 29)]:
    i = bisect.bisect_right(fx_d, t) - 1
    print(f"  {t}: FIX {fx_v[i]} (obs {fx_d[i]})")
w = [(d, v) for d, v in fix if d >= date(2026, 6, 1)]
mn = min(w, key=lambda x: x[1]); print(f"  mínimo FIX desde 1-jun-2026: {mn}; a 18.071: {100*(18.071/mn[1]-1):+.2f}%; a 17.8413 (28-sep): {100*(17.8413/mn[1]-1):+.2f}%")
