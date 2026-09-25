"""C06: calculos exploratorios del capitulo 06 (asset pricing empirico y anomalias).

NO es una replica pre-registrada: son calculos descriptivos, sin optimizacion de parametros,
escritos el 2026-09-25 para dar cifras propias al capitulo. Estado: exploratorio.

Datos congelados en datos/ (sin red):
- Kenneth French Data Library, version CRSP 202607: F-F_Research_Data_Factors, F-F_Momentum_Factor,
  F-F_Research_Data_5_Factors_2x3 (sha256 en el capitulo).
- Shiller, ie_data.xls (guardado 2024-09-04; datos 1871-01 a 2024-09).

Bloques:
 C1  Momentum (UMD) en estado "bear": rendimiento acumulado del mercado t-24..t-1 < 0
     (indicador de Daniel-Moskowitz 2016). Media, t Newey-West(6), 20 peores meses.
 C2  Factor momentum (Ehsani-Linnainmaa 2022) con SMB, HML, RMW, CMA, UMD: rendimiento del mes
     siguiente segun el signo de los 12 meses previos; portafolio TS de factor momentum.
 P1  CAPE -> rendimiento real anualizado a 10 anios (dentro y fuera de muestra, ventana expansiva
     que solo usa pares cuyo rendimiento ya se realizo).
 P2  Log D/P -> rendimiento real total del mes siguiente; R2 fuera de muestra (Goyal-Welch) y con
     restricciones de Campbell-Thompson (pendiente > 0 y pronostico >= 0).

Uso (desde la raiz del repo): python3 laboratorio/replicas/C06-predictibilidad-y-momentum/reproducir.py
"""
import math
import statistics
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))
from herramientas.datos_historicos import french, columna  # noqa: E402
from herramientas.estadistica import newey_west  # noqa: E402

DATOS = Path(__file__).resolve().parent / "datos"


def ols(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    a = my - b * mx
    res = [c - (a + b * u) for u, c in zip(x, y)]
    r2 = 1 - sum(e * e for e in res) / sum((c - my) ** 2 for c in y)
    return a, b, r2


def bloque_momentum():
    ff3 = french("F-F_Research_Data_Factors", dir_cache=DATOS)
    ff5 = french("F-F_Research_Data_5_Factors_2x3", dir_cache=DATOS)
    mom = french("F-F_Momentum_Factor", dir_cache=DATOS)
    print("French CRSP:", ff3.get("version_crsp"), ff5.get("version_crsp"), mom.get("version_crsp"))
    mk = dict(columna(ff3, "Mkt-RF"))
    rf = dict(columna(ff3, "RF"))
    um = dict(columna(mom, list(mom["columnas"])[0]))
    fe = sorted(mk)
    idx = {f: i for i, f in enumerate(fe)}
    crono = []
    for f in sorted(set(mk) & set(um)):
        i = idx[f]
        if i < 24:
            continue
        cum = 1.0
        for j in range(i - 24, i):
            cum *= 1 + mk[fe[j]] + rf[fe[j]]
        crono.append((f, um[f], cum < 1, mk[f]))
    for etiqueta, cond in (("bear", True), ("no bear", False)):
        v = [u for _, u, b, _ in crono if b == cond]
        nw = newey_west(v, 6)
        print(f"C1 UMD {etiqueta}: n={nw['n']} media={nw['media']*100:.3f}%/mes t_NW={nw['t']:.2f}")
    for lo, hi in ((1927, 1999), (2000, 2026)):
        for cond in (True, False):
            v = [u for f, u, b, _ in crono if b == cond and lo <= f.year <= hi]
            nw = newey_west(v, 6)
            print(f"C1 {lo}-{hi} bear={cond}: n={nw['n']} media={nw['media']*100:.3f}% t_NW={nw['t']:.2f}")
    reb = [u for _, u, b, m in crono if b and m > 0]
    nw = newey_west(reb, 6)
    print(f"C1 bear y mercado sube en el mes (contemporaneo): n={nw['n']} media={nw['media']*100:.2f}% t={nw['t']:.2f}")
    peores = sorted(crono, key=lambda z: z[1])[:20]
    print("C1 20 peores meses de UMD:", sum(p[2] for p in peores), "en estado bear; fraccion de meses bear:",
          round(sum(1 for c in crono if c[2]) / len(crono), 3))
    for f, u, b, m in peores:
        print(f"   {f} UMD={u*100:.1f}% bear={int(b)} mercado={m*100:.1f}%")

    facs = {n: dict(columna(ff5, n)) for n in ("SMB", "HML", "RMW", "CMA")}
    facs["UMD"] = um
    fe5 = sorted(set.intersection(*[set(d) for d in facs.values()]))
    regs, port = [], []
    for i in range(12, len(fe5)):
        f = fe5[i]
        pr = []
        for n, d in facs.items():
            pasado = sum(d[fe5[j]] for j in range(i - 12, i))
            regs.append((f, pasado > 0, d[f]))
            pr.append(d[f] if pasado > 0 else -d[f])
        port.append((f, sum(pr) / len(pr)))
    for lo, hi in ((1964, 2026), (1964, 1999), (2000, 2026), (2016, 2026)):
        p = [r for f, s, r in regs if s and lo <= f.year <= hi]
        q = [r for f, s, r in regs if not s and lo <= f.year <= hi]
        nw = newey_west([x for f, x in port if lo <= f.year <= hi], 6)
        print(f"C2 {lo}-{hi}: tras anio + {statistics.mean(p)*1e4:.1f} pb (n={len(p)}) | tras anio - "
              f"{statistics.mean(q)*1e4:.1f} pb (n={len(q)}) | TSFM {nw['media']*1e4:.1f} pb/mes t={nw['t']:.2f}")


def bloque_predictibilidad():
    import xlrd
    s = xlrd.open_workbook(str(DATOS / "ie_data.xls")).sheet_by_name("Data")
    filas = [[s.cell_value(r, c) for c in range(22)] for r in range(8, s.nrows)]
    filas = [v for v in filas if isinstance(v[0], float)]
    num = lambda x: x if isinstance(x, float) else None  # noqa: E731
    fechas = [v[0] for v in filas]
    P, D, cape = [num(v[1]) for v in filas], [num(v[2]) for v in filas], [num(v[12]) for v in filas]
    rtr, r10 = [num(v[9]) for v in filas], [num(v[19]) for v in filas]
    print("Shiller:", fechas[0], "a", fechas[-1], "CAPE ultimo", round(cape[-1], 2))
    idx = [i for i in range(len(filas)) if cape[i] and r10[i] is not None]
    a, b, r2 = ols([math.log(cape[i]) for i in idx], [r10[i] for i in idx])
    print(f"P1 dentro de muestra {fechas[idx[0]]}-{fechas[idx[-1]]}: r10 = {a:.4f} {b:+.4f} ln(CAPE), R2={r2:.3f}")
    for c in (15, 20, 25, 30, 35, 40):
        print(f"   CAPE {c}: {100*(a+b*math.log(c)):.2f}% real anual")
    for lo, hi in ((1950, 2014.99), (1950, 1969.99), (1970, 1989.99), (1990, 2014.99)):
        sm = sh = 0.0
        fs, ys = [], []
        for t in idx:
            if not lo <= fechas[t] <= hi:
                continue
            tr = [i for i in idx if i <= t - 120]
            a2, b2, _ = ols([math.log(cape[i]) for i in tr], [r10[i] for i in tr])
            f = a2 + b2 * math.log(cape[t])
            h = sum(r10[i] for i in tr) / len(tr)
            sm += (r10[t] - f) ** 2
            sh += (r10[t] - h) ** 2
            fs.append(f)
            ys.append(r10[t])
        print(f"P1 fuera de muestra {lo}-{int(hi)}: n={len(fs)} R2_OOS={1-sm/sh:.3f} "
              f"pronostico medio {100*statistics.mean(fs):.2f}% realizado {100*statistics.mean(ys):.2f}%")
    ret = [None] + [rtr[i] / rtr[i - 1] - 1 if rtr[i] and rtr[i - 1] else None for i in range(1, len(rtr))]
    dp = [math.log(d / p) if d and p else None for d, p in zip(D, P)]
    datos = [(dp[i], ret[i + 1], fechas[i]) for i in range(len(filas) - 1)
             if dp[i] is not None and ret[i + 1] is not None]
    a, b, r2 = ols([d[0] for d in datos], [d[1] for d in datos])
    print(f"P2 dentro de muestra mensual: b={b:.4f} R2={r2:.4f} n={len(datos)}")
    for inicio in (1927, 1950, 1990):
        sm = sh = sc = 0.0
        k = 0
        for j in range(len(datos)):
            if datos[j][2] < inicio:
                continue
            tr = datos[:j]
            a2, b2, _ = ols([t[0] for t in tr], [t[1] for t in tr])
            f = a2 + b2 * datos[j][0]
            h = sum(t[1] for t in tr) / len(tr)
            fc = max(f, 0.0) if b2 > 0 else h
            y = datos[j][1]
            sm += (y - f) ** 2
            sh += (y - h) ** 2
            sc += (y - fc) ** 2
            k += 1
        print(f"P2 fuera de muestra desde {inicio}: n={k} R2_OOS={1-sm/sh:.4f} CT={1-sc/sh:.4f}")


if __name__ == "__main__":
    bloque_momentum()
    bloque_predictibilidad()
