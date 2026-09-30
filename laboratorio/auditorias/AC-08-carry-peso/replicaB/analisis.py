"""Réplica B: carry de mercado = CETES 28d (Banxico SF43936, semanal) - T-bill 3m EUA (FRED DTB3).

Pregunta: ¿"con diferencial <=3% el peso se depreció ~14% en casi todos los casos de 20 años"?
Salida: tablas en texto. Cambios de USD/MXN en % (positivo = peso se deprecia).
Datos: CSV descargados por fetch.py / fred.py en este mismo directorio.
"""
from __future__ import annotations
import bisect, csv, os, sys, math
from datetime import date, timedelta
import numpy as np

D = os.path.dirname(os.path.abspath(__file__))
INICIO = date(2006, 1, 1)
H = {"1m": 30, "3m": 91, "6m": 182, "12m": 365}


def leer(nombre, col=1):
    out = []
    with open(f"{D}/{nombre}.csv") as f:
        r = csv.reader(f); next(r)
        for row in r:
            if len(row) <= col or row[col] in ("", "."):
                continue
            out.append((date.fromisoformat(row[0]), float(row[col])))
    return sorted(out)


cetes = leer("SF43936")
tb3 = leer("DTB3")
fix = leer("SF43718")
fx_d = [d for d, _ in fix]; fx_v = [v for _, v in fix]
tb_d = [d for d, _ in tb3]; tb_v = [v for _, v in tb3]
ULT_FIX = fx_d[-1]


def asof(ds, vs, t, maxdias=10):
    i = bisect.bisect_right(ds, t) - 1
    if i < 0 or (t - ds[i]).days > maxdias:
        return None
    return vs[i]


# ---------------- serie semanal alineada
sem = []  # (fecha, cetes, tbill, dif, fix)
for t, c in cetes:
    if t < date(2005, 1, 1):
        continue
    tb = asof(tb_d, tb_v, t, 7)
    fx = asof(fx_d, fx_v, t, 7)
    if tb is None or fx is None:
        continue
    sem.append((t, c, tb, round(c - tb, 4), fx))
fechas = [s[0] for s in sem]


def fwd(t, dias):
    """% cambio USD/MXN de t a t+dias (FIX en o antes de t+dias). None si no hay dato completo."""
    t1 = t + timedelta(days=dias)
    if t1 > ULT_FIX:
        return None
    a = asof(fx_d, fx_v, t, 7); b = asof(fx_d, fx_v, t1, 7)
    return 100 * (b / a - 1)


def maxdep(t, dias=365, parcial=False):
    t1 = t + timedelta(days=dias)
    if t1 > ULT_FIX and not parcial:
        return None
    a = asof(fx_d, fx_v, t, 7)
    i0 = bisect.bisect_right(fx_d, t); i1 = bisect.bisect_right(fx_d, t1)
    if i1 <= i0:
        return None
    m = max(fx_v[i0:i1]); j = i0 + fx_v[i0:i1].index(m)
    return 100 * (m / a - 1), fx_d[j], m


def fila_resultados(t):
    r = {k: fwd(t, v) for k, v in H.items()}
    md = maxdep(t)
    r["max12"] = md[0] if md else None
    r["max12_fecha"] = md[1] if md else None
    r["max12_nivel"] = md[2] if md else None
    if md is None:
        mp = maxdep(t, parcial=True)
        r["max_parcial"] = mp
    return r


def f(x, nd=1):
    return "  n/d" if x is None else f"{x:+.{nd}f}"


# ---------------- 1. serie y hoy
print("=" * 100)
print("1. SERIE CETES28 - DTB3 (semanal)")
s06 = [s for s in sem if s[0] >= INICIO]
print(f"obs semanales desde 2006: {len(s06)}; primera {s06[0][0]}, última {s06[-1][0]}")
hoy = sem[-1]
print(f"HOY: CETES28 {hoy[1]:.2f} ({hoy[0]}) - DTB3 {hoy[2]:.2f} (último dato FRED {tb_d[-1]}) = {hoy[3]:.2f}")
print("Últimas 12 semanas:")
for s in sem[-12:]:
    print(f"  {s[0]}  CETES {s[1]:5.2f}  TB3 {s[2]:5.2f}  dif {s[3]:5.2f}  FIX {s[4]:.4f}")
print("Promedios anuales del diferencial y % de semanas <=3:")
for y in range(2005, 2027):
    xs = [s[3] for s in sem if s[0].year == y]
    if xs:
        print(f"  {y}: media {np.mean(xs):5.2f}  min {min(xs):5.2f}  max {max(xs):5.2f}  %<=3 {100*np.mean([x<=3 for x in xs]):5.1f}  n={len(xs)}")
print("Máximo del diferencial en 2022-2026:",
      max((s[3], s[0]) for s in sem if s[0] >= date(2022, 1, 1)))
print("Máximo del diferencial en 2024-2026:",
      max((s[3], s[0]) for s in sem if s[0] >= date(2024, 1, 1)))


# ---------------- 2. episodios
def cruces(umbral, sep_dias=365, desde=INICIO):
    ev = []
    for i in range(1, len(sem)):
        t = sem[i][0]
        if t < desde:
            continue
        if sem[i][3] <= umbral and sem[i - 1][3] > umbral:
            if ev and (t - ev[-1]).days < sep_dias:
                continue
            ev.append(t)
    return ev


def estancias(umbral, tolerancia_sem=4, desde=INICIO, min_sem=1):
    """Tramos contiguos con dif<=umbral; se unen tramos separados por <=tolerancia_sem semanas arriba."""
    idx = [i for i, s in enumerate(sem) if s[0] >= desde and s[3] <= umbral]
    tramos = []
    for i in idx:
        if tramos and i - tramos[-1][1] <= tolerancia_sem + 1:
            tramos[-1][1] = i
        else:
            tramos.append([i, i])
    out = []
    for a, b in tramos:
        n = sum(1 for k in range(a, b + 1) if sem[k][3] <= umbral)
        if n >= min_sem:
            out.append((sem[a][0], sem[b][0], n, b - a + 1))
    return out


def contexto(t):
    notas = [
        (date(2006, 1, 1), date(2007, 7, 31), "Fed en 5.25% (fin del ciclo alza 2004-06); Banxico 7.0-7.25%; peso estable ~10.8-11.2"),
        (date(2007, 8, 1), date(2008, 7, 31), "inicio crisis subprime; Fed recorta rápido; carry se ensancha"),
        (date(2013, 1, 1), date(2015, 12, 31), "Banxico en mínimo 3.0% (2014-15), Fed en 0-0.25; taper tantrum, desplome petróleo 2014-15, alza Fed dic-2015"),
        (date(2016, 1, 1), date(2016, 12, 31), "Banxico sube desde 3.25%; Brexit, elección Trump (nov-2016)"),
        (date(2021, 1, 1), date(2021, 12, 31), "Banxico recorta a 4.0% (feb-2021), Fed 0-0.25"),
        (date(2025, 1, 1), date(2026, 12, 31), "ciclo de recortes Banxico hasta 6.50%; Fed 3.75-4.00%"),
    ]
    for a, b, n in notas:
        if a <= t <= b:
            return n
    return ""


print("=" * 100)
print("2-3. EPISODIOS")
for u in (2.5, 3.0, 3.5):
    print(f"\n--- Umbral {u:.1f}: cruces hacia abajo viniendo de arriba (separación >=12m), desde 2006")
    for t in cruces(u):
        s = sem[fechas.index(t)]
        r = fila_resultados(t)
        prev = sem[fechas.index(t) - 1]
        extra = ""
        if r["max12"] is None and r.get("max_parcial"):
            mp = r["max_parcial"]; extra = f" [parcial: max {mp[0]:+.1f}% al {mp[1]} ({mp[2]:.4f})]"
        print(f"  {t} dif {prev[3]:.2f}->{s[3]:.2f} FIX {s[4]:.4f} | 1m {f(r['1m'])} 3m {f(r['3m'])} 6m {f(r['6m'])} 12m {f(r['12m'])} "
              f"| max12 {f(r['max12'])} ({r['max12_fecha']}, {r['max12_nivel']}){extra} | {contexto(t)}")
    print(f"--- Umbral {u:.1f}: estancias (tramos <=umbral, se unen huecos <=4 semanas)")
    for a, b, n, largo in estancias(u):
        fa = asof(fx_d, fx_v, a, 7); fb = asof(fx_d, fx_v, b, 7)
        ra = fila_resultados(a)
        # max depreciación durante la estancia + 12m posteriores al inicio
        md_est = maxdep(a, (b - a).days + 1, parcial=True)
        print(f"  {a} -> {b}  ({n} sem <=u de {largo}) FIX {fa:.4f}->{fb:.4f} ({100*(fb/fa-1):+.1f}% en la estancia) "
              f"| desde inicio: 6m {f(ra['6m'])} 12m {f(ra['12m'])} max12 {f(ra['max12'])} | max en estancia {f(md_est[0] if md_est else None)}")

# ---------------- 4. tasa base
print("=" * 100)
print("4. TASA BASE INCONDICIONAL (todas las semanas 2006+ con ventana completa)")


def dist(sel, clave):
    xs = [fila_resultados(s[0])[clave] for s in sel]
    xs = [x for x in xs if x is not None]
    if not xs:
        return "n=0"
    xs = np.array(xs)
    return (f"n={len(xs):4d} media {xs.mean():+5.1f} mediana {np.median(xs):+5.1f} p10 {np.percentile(xs,10):+5.1f} "
            f"p90 {np.percentile(xs,90):+5.1f} %>0 {100*(xs>0).mean():4.0f} %>=10 {100*(xs>=10).mean():4.0f} %>=14 {100*(xs>=14).mean():4.0f}")


cache = {}
def fr(t):
    if t not in cache:
        cache[t] = fila_resultados(t)
    return cache[t]
fila_resultados_orig = fila_resultados
def fila_resultados(t):  # noqa: F811  (memo)
    if t not in cache:
        cache[t] = fila_resultados_orig(t)
    return cache[t]

for clave in ("1m", "3m", "6m", "12m", "max12"):
    print(f"  {clave:5s} todas      : {dist(s06, clave)}")
    for u in (2.5, 3.0, 3.5):
        print(f"  {clave:5s} dif<={u:.1f}   : {dist([s for s in s06 if s[3] <= u], clave)}")
        print(f"  {clave:5s} dif> {u:.1f}   : {dist([s for s in s06 if s[3] > u], clave)}")

# ---------------- regresión con Newey-West
print("=" * 100)
print("4b. REGRESIÓN: cambio % USD/MXN a h vs nivel del diferencial en t (semanal, 2006+), HAC Newey-West")


def ols_nw(y, x, lags):
    X = np.column_stack([np.ones_like(x), x])
    n = len(y)
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ X.T @ y
    e = y - X @ b
    u = X * e[:, None]
    S = u.T @ u
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        G = u[L:].T @ u[:-L]
        S += w * (G + G.T)
    V = XtXi @ S @ XtXi
    se = np.sqrt(np.diag(V))
    r2 = 1 - (e @ e) / ((y - y.mean()) @ (y - y.mean()))
    se_ols = np.sqrt(np.diag(XtXi) * (e @ e) / (n - 2))
    return b, se, r2, n, se_ols


for clave, lags in (("6m", 26), ("12m", 52), ("max12", 52)):
    for desde, etiqueta in ((INICIO, "2006-2026"), (date(2009, 1, 1), "2009-2026 (sin 2006-08)")):
        pares = [(s[3], fila_resultados(s[0])[clave]) for s in sem if s[0] >= desde]
        pares = [(a, b) for a, b in pares if b is not None]
        x = np.array([p[0] for p in pares]); y = np.array([p[1] for p in pares])
        for L in (lags, int(1.5 * lags)):
            b, se, r2, n, se_ols = ols_nw(y, x, L)
            print(f"  {clave:5s} {etiqueta:26s} lags={L:3d}: y = {b[0]:+.2f} {b[1]:+.2f}*dif | t_NW(b)={b[1]/se[1]:+.2f} "
                  f"(t_OLS {b[1]/se_ols[1]:+.2f}) R2={r2:.3f} n={n}")
    # también variable indicadora dif<=3
    pares = [(1.0 if s[3] <= 3 else 0.0, fila_resultados(s[0])[clave]) for s in sem if s[0] >= INICIO]
    pares = [(a, b) for a, b in pares if b is not None]
    x = np.array([p[0] for p in pares]); y = np.array([p[1] for p in pares])
    b, se, r2, n, _ = ols_nw(y, x, lags)
    print(f"  {clave:5s} dummy dif<=3 2006-2026 lags={lags}: y = {b[0]:+.2f} {b[1]:+.2f}*1[dif<=3] | t_NW={b[1]/se[1]:+.2f} R2={r2:.3f} n={n}")

# predicción puntual para el valor de hoy
print("\nPredicción del modelo lineal (2006-2026) para dif de hoy:")
for clave, lags in (("6m", 26), ("12m", 52)):
    pares = [(s[3], fila_resultados(s[0])[clave]) for s in sem if s[0] >= INICIO]
    pares = [(a, b) for a, b in pares if b is not None]
    x = np.array([p[0] for p in pares]); y = np.array([p[1] for p in pares])
    b, se, r2, n, _ = ols_nw(y, x, lags)
    print(f"  {clave}: {b[0] + b[1]*hoy[3]:+.1f}% con dif={hoy[3]:.2f}")

# ---------------- verificación: cruces sin filtro de separación
print("=" * 100)
print("Cruces a la baja de 3.0 SIN filtro de separación (para ver ruido):")
for i in range(1, len(sem)):
    if sem[i][0] >= INICIO and sem[i][3] <= 3.0 and sem[i - 1][3] > 3.0:
        print(f"  {sem[i][0]} {sem[i-1][3]:.2f}->{sem[i][3]:.2f}")
