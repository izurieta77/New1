#!/usr/bin/env python3
"""R04 - Efecto Halloween / "Sell in May and go away" (Bouman y Jacobsen, 2002, AER 92(5):1618-1635).

Reproduce desde la raiz del repo:  python3 laboratorio/replicas/R04.py
Solo biblioteca estandar. Cada corrida de estrategia se agrega a laboratorio/replicas/R04-variantes.csv.
La salida completa se guarda tambien en R04-salida.txt y las cifras clave en R04-resultados.json.

Pre-registro: R04-efecto-halloween.md, secciones 1-9.
  Efecto: regresion mensual y_t = mu + a1*S_t + e_t con y_t = 100*ln(1+R_t) y S_t = 1 de noviembre
    a abril; t MCO, HC1 y Newey-West (Bartlett, 12 rezagos). Pruebas robustas: dummy de enero,
    dummies de Maberly-Pierce (oct-1987, ago-1998), winsorizacion 1/99, diferencia anual pareada
    (bootstrap y prueba de signo), exceso sobre el efectivo por mitad del anio y placebo de calendario.
  Mercados: EUA = French Mkt-RF + RF (CRSP, USD, con dividendos); Mexico = ^MXX (Yahoo, MXN,
    indice de PRECIO, sin dividendos); efectivo MX = CETES (FRED INTGSTMXM193N).
  Estrategia: mercado en los meses de la ventana y efectivo el resto, con costos GBM.
  Corte unico 2002-12-31 (publicacion en el AER de diciembre de 2002).
"""
from __future__ import annotations

import io
import json
import math
import random
import statistics
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from herramientas import backtest as bt  # noqa: E402
from herramientas import datos_historicos as dh  # noqa: E402
from herramientas import estadistica as est  # noqa: E402

# ================================================================ parametros pre-registrados
ID = "R04"
DIR = Path(__file__).resolve().parent
CORTE = date(2002, 12, 31)
FIN = date(2100, 1, 1)
MIN_HISTORIA = 10
NW_REZAGOS = 12
BOOT_REPS = 10_000
BOOT_SEMILLA = 4
INVIERNO = frozenset({11, 12, 1, 2, 3, 4})
VERANO = frozenset(range(5, 11))
VENTANAS_CAL = {  # nombre -> meses en el mercado (lista cerrada del pre-registro)
    "nov_abr": INVIERNO,
    "oct_abr": frozenset({10, 11, 12, 1, 2, 3, 4}),
    "nov_may": frozenset({11, 12, 1, 2, 3, 4, 5}),
    "dic_abr": frozenset({12, 1, 2, 3, 4}),
    "nov_mar": frozenset({11, 12, 1, 2, 3}),
}
# Maberly y Pierce (2004), Econ Journal Watch 1(1), tabla 1: CRSP VW con dividendos, log, 1970-01 a 1998-08
MP = {"A": {"mu": 0.4235, "t_mu": 1.21, "a1": 1.0349, "t_a1": 2.10},
      "B": {"mu": 0.6800, "a1": 0.7784, "t_a1": 1.69, "a2": -22.0560},
      "C": {"a1": 0.6205, "t_a1": 1.28, "a3": 0.9363}}
TOLERANCIA_PP = 0.20
MESES_MP = {(1987, 10), (1998, 8)}
COMISION = bt.COMISION_GBM_POR_LADO
ESCENARIOS = {  # nombre -> (comision, spread, es_sensibilidad, nota)
    "defecto": (COMISION, bt.SPREAD_POR_LADO["liquido"], False, ""),
    "medio": (COMISION, bt.SPREAD_POR_LADO["medio"], True, "sensibilidad: spread medio 0.15% por lado"),
    "bruto": (0.0, 0.0, True, "sensibilidad: bruto (sin comision ni spread)"),
}
NORMAL = statistics.NormalDist()


def d(a: int, m: int) -> date:
    return dh.fin_de_mes(a, m)


VENTANAS_EFECTO = {
    "US": [("completo", d(1926, 7), d(2100, 12)),
           ("dentro_muestra 1926-07 a 2002-12", d(1926, 7), CORTE),
           ("fuera_muestra 2003-01 al final", d(2003, 1), d(2100, 12)),
           ("pre-articulo 1926-07 a 1969-12", d(1926, 7), d(1969, 12)),
           ("ARTICULO 1970-01 a 1998-08", d(1970, 1), d(1998, 8)),
           ("hueco 1998-09 a 2002-12", d(1998, 9), CORTE),
           ("contraste WP1997 1973-01 a 1996-12", d(1973, 1), d(1996, 12)),
           ("contraste JZ-OOS 1998-09 a 2011-07", d(1998, 9), d(2011, 7))],
    "MX": [("completo", d(1991, 12), d(2100, 12)),
           ("dentro_muestra 1991-12 a 2002-12", d(1991, 12), CORTE),
           ("fuera_muestra 2003-01 al final", d(2003, 1), d(2100, 12)),
           ("traslape articulo 1991-12 a 1998-08", d(1991, 12), d(1998, 8)),
           ("hueco 1998-09 a 2002-12", d(1998, 9), CORTE),
           ("contraste JZ-OOS 1998-09 a 2011-07", d(1998, 9), d(2011, 7))],
}


# ================================================================ algebra y regresion (stdlib)

def _inversa(A: list) -> list:
    n = len(A)
    M = [[float(v) for v in fila] + [1.0 if i == j else 0.0 for j in range(n)] for i, fila in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[p][c]) < 1e-14:
            raise ValueError("matriz singular")
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [v / piv for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0.0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [fila[n:] for fila in M]


def _mm(A: list, B: list) -> list:
    return [[sum(a * b for a, b in zip(fila, col)) for col in zip(*B)] for fila in A]


def regresion(y: list, X: list, rezagos: int = NW_REZAGOS) -> dict:
    """MCO de y sobre X (lista de filas) con errores estandar MCO, HC1 y Newey-West (Bartlett).

    HC1 y NW llevan la correccion n/(n-k). Con X = [[1]] la varianza NW coincide con
    herramientas.estadistica.newey_west (se comprueba en prueba_herramientas)."""
    n, k = len(y), len(X[0])
    if n <= k + 2:
        raise ValueError("muy pocas observaciones")
    XtX = [[sum(X[t][i] * X[t][j] for t in range(n)) for j in range(k)] for i in range(k)]
    Xty = [sum(X[t][i] * y[t] for t in range(n)) for i in range(k)]
    inv = _inversa(XtX)
    b = [sum(inv[i][j] * Xty[j] for j in range(k)) for i in range(k)]
    e = [y[t] - sum(b[i] * X[t][i] for i in range(k)) for t in range(n)]
    s2 = sum(v * v for v in e) / (n - k)
    g = [[X[t][i] * e[t] for i in range(k)] for t in range(n)]

    def gamma(j: int) -> list:
        return [[sum(g[t][a] * g[t - j][c] for t in range(j, n)) for c in range(k)] for a in range(k)]

    S0 = gamma(0)
    S = [fila[:] for fila in S0]
    for j in range(1, rezagos + 1):
        w = 1 - j / (rezagos + 1)
        G = gamma(j)
        for a in range(k):
            for c in range(k):
                S[a][c] += w * (G[a][c] + G[c][a])
    corr = n / (n - k)
    v_hc = _mm(_mm(inv, S0), inv)
    v_nw = _mm(_mm(inv, S), inv)

    def raiz(v: float) -> float:
        return math.sqrt(v) if v > 0 else float("nan")

    se_ols = [raiz(s2 * inv[i][i]) for i in range(k)]
    se_hc = [raiz(corr * v_hc[i][i]) for i in range(k)]
    se_nw = [raiz(corr * v_nw[i][i]) for i in range(k)]

    def t(se: list) -> list:
        return [b[i] / se[i] if se[i] and se[i] > 0 else float("nan") for i in range(k)]

    t_nw = t(se_nw)
    return {"n": n, "coef": b, "se_ols": se_ols, "se_hc1": se_hc, "se_nw": se_nw,
            "t_ols": t(se_ols), "t_hc1": t(se_hc), "t_nw": t_nw,
            "p_nw": [2 * (1 - NORMAL.cdf(abs(x))) if math.isfinite(x) else float("nan") for x in t_nw],
            "rezagos": rezagos}


def a_log_pct(serie: list) -> list:
    """[(fecha, R simple)] -> [(fecha, 100*ln(1+R))]."""
    return [(f, 100.0 * math.log1p(r)) for f, r in serie]


# ================================================================ pruebas del efecto

def pareado_anual(pts: list) -> dict:
    """D_Y = suma y(nov_{Y-1}..abr_Y) - suma y(may_Y..oct_Y) para anios Halloween completos."""
    m = {(f.year, f.month): v for f, v in pts}
    if not m:
        return {"n": 0}
    anios = sorted({a for a, _ in m})
    D = []
    for Y in range(anios[0], anios[-1] + 1):
        inv = [(Y - 1, 11), (Y - 1, 12)] + [(Y, k) for k in range(1, 5)]
        ver = [(Y, k) for k in range(5, 11)]
        if all(k in m for k in inv + ver):
            D.append((Y, sum(m[k] for k in inv) - sum(m[k] for k in ver)))
    vals = [v for _, v in D]
    N = len(vals)
    if N < 3:
        return {"n": N}
    media, sd = statistics.fmean(vals), statistics.stdev(vals)
    rng = random.Random(BOOT_SEMILLA)
    medias = sorted(statistics.fmean(rng.choices(vals, k=N)) for _ in range(BOOT_REPS))
    ic = (medias[int(0.025 * BOOT_REPS)], medias[int(0.975 * BOOT_REPS) - 1])
    positivos = sum(1 for v in vals if v > 0)
    p_signo = sum(math.comb(N, i) for i in range(positivos, N + 1)) / 2 ** N
    return {"n": N, "anio_ini": D[0][0], "anio_fin": D[-1][0], "media": media, "mediana": statistics.median(vals),
            "sd": sd, "t_iid": media / (sd / math.sqrt(N)), "ic95_bootstrap": ic, "positivos": positivos,
            "p_signo_una_cola": p_signo, "peor": min(D, key=lambda x: x[1]), "mejor": max(D, key=lambda x: x[1])}


def semestres_invierno(pts_exceso: list) -> dict:
    """Exceso (log %) acumulado de cada semestre nov_{Y-1}..abr_Y completo en la ventana."""
    m = {(f.year, f.month): v for f, v in pts_exceso}
    if not m:
        return {"n": 0}
    anios = sorted({a for a, _ in m})
    W = []
    for Y in range(anios[0], anios[-1] + 1):
        inv = [(Y - 1, 11), (Y - 1, 12)] + [(Y, k) for k in range(1, 5)]
        if all(k in m for k in inv):
            W.append((Y, sum(m[k] for k in inv)))
    vals = [v for _, v in W]
    if len(vals) < 3:
        return {"n": len(vals)}
    return {"n": len(vals), "media": statistics.fmean(vals), "mediana": statistics.median(vals),
            "pct_positivos": sum(1 for v in vals if v > 0) / len(vals), "peor": min(W, key=lambda x: x[1]),
            "mejor": max(W, key=lambda x: x[1])}


def pruebas_efecto(serie_log: list, rf: dict | None, f0: date, f1: date, placebo: bool = True) -> dict | None:
    """Todas las pruebas pre-registradas en la ventana [f0, f1] (fechas fin de mes, inclusivas)."""
    pts = [(f, v) for f, v in serie_log if f0 <= f <= f1]
    if len(pts) < 24:
        return None
    y = [v for _, v in pts]
    S = [1.0 if f.month in INVIERNO else 0.0 for f, _ in pts]
    J = [1.0 if f.month == 1 else 0.0 for f, _ in pts]
    salida: dict = {"desde": pts[0][0], "hasta": pts[-1][0], "n": len(pts)}
    salida["m1"] = regresion(y, [[1.0, s] for s in S])
    salida["m2_enero"] = regresion(y, [[1.0, s, j] for s, j in zip(S, J)])
    q = statistics.quantiles(y, n=100, method="inclusive")
    lo, hi = q[0], q[98]
    yw = [min(max(v, lo), hi) for v in y]
    salida["winsor"] = regresion(yw, [[1.0, s] for s in S])
    salida["winsor_limites"] = (lo, hi)
    D = [1.0 if (f.year, f.month) in MESES_MP else 0.0 for f, _ in pts]
    if sum(D) == len(MESES_MP):
        salida["mp_B"] = regresion(y, [[1.0, s, dd] for s, dd in zip(S, D)])
        salida["mp_C"] = regresion(y, [[1.0, s, dd, j] for s, dd, j in zip(S, D, J)])
    salida["pareado"] = pareado_anual(pts)
    salida["media_invierno"] = statistics.fmean(v for v, s in zip(y, S) if s == 1.0)
    salida["media_verano"] = statistics.fmean(v for v, s in zip(y, S) if s == 0.0)
    if rf is not None:
        ex = [(f, v - 100.0 * math.log1p(rf[f])) for f, v in pts if f in rf]
        if len(ex) != len(pts):
            raise ValueError("faltan tasas de efectivo en la ventana")
        e = [v for _, v in ex]
        salida["exceso"] = regresion(e, [[s, 1.0 - s] for s in S])  # coef[0] invierno, coef[1] verano
        salida["semestres_invierno"] = semestres_invierno(ex)
    if placebo:
        rot = []
        for k in range(1, 13):
            meses = {(k - 1 + i) % 12 + 1 for i in range(6)}
            r = regresion(y, [[1.0, 1.0 if f.month in meses else 0.0] for f, _ in pts])
            rot.append((k, r["coef"][1], r["t_nw"][1]))
        orden = sorted(rot, key=lambda x: -x[1])
        salida["placebo"] = rot
        salida["placebo_lugar_nov"] = 1 + [k for k, _, _ in orden].index(11)
    return salida


# ================================================================ senal de calendario

def senal_calendario(meses: frozenset, nombre: str):
    """Exposicion 1 si el mes del periodo a decidir esta en 'meses'. Solo usa la fecha de decision
    (fin de t-1): el calendario se conoce de antemano. Exige datos mensuales consecutivos."""
    meses = frozenset(meses)

    def senal(h):
        f = h.fecha_decision
        if f is None:
            raise ValueError("sin fecha de decision: sube min_historia")
        return 1.0 if f.month % 12 + 1 in meses else 0.0

    senal.__qualname__ = senal.__name__ = f"calendario_{nombre}"
    return senal


# ================================================================ datos

def exigir_meses_consecutivos(serie: list, nombre: str) -> None:
    for (a, _), (b, _) in zip(serie, serie[1:]):
        if (b.year * 12 + b.month) - (a.year * 12 + a.month) != 1 or b != dh.a_fin_de_mes(b):
            raise ValueError(f"{nombre}: meses no consecutivos o fecha no fin de mes entre {a} y {b}")


def cetes_mensual(serie_fred: list) -> tuple[list, list]:
    """Tasa anual promedio del mes (FRED, dia 1) -> rendimiento simple del mes = tasa/100 * dias/360.
    Meses faltantes: se arrastra la tasa previa (se reportan)."""
    tasas = {(f.year, f.month): v for f, v in serie_fred}
    y, m = min(tasas)
    fin = max(tasas)
    salida, rellenos, previa = [], [], None
    while (y, m) <= fin:
        if (y, m) in tasas:
            tasa = tasas[(y, m)]
        else:
            tasa = previa
            rellenos.append(d(y, m))
        f = d(y, m)
        f_prev = d(y - 1, 12) if m == 1 else d(y, m - 1)
        salida.append((f, tasa / 100.0 * (f - f_prev).days / 360.0))
        previa = tasa
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return salida, rellenos


# ================================================================ comprobaciones sin red

def prueba_herramientas() -> float:
    rnd = random.Random(11)
    peor = 0.0
    x = [rnd.gauss(0.5, 2.0) for _ in range(300)]
    for L in (0, 6, 12):
        r = regresion(x, [[1.0] for _ in x], L)
        nw = est.newey_west(x, L)
        peor = max(peor, abs(r["coef"][0] - nw["media"]), abs(r["se_nw"][0] - nw["se"]))
    s = [1.0 if i % 12 < 6 else 0.0 for i in range(300)]
    r2 = regresion(x, [[1.0, si] for si in s])
    dif = statistics.fmean(v for v, si in zip(x, s) if si) - statistics.fmean(v for v, si in zip(x, s) if not si)
    peor = max(peor, abs(r2["coef"][1] - dif))
    # senal de calendario con datos sinteticos, sin registrar
    fechas = [d(2000 + k // 12, k % 12 + 1) for k in range(120)]
    activo = [(f, rnd.gauss(0.01, 0.04)) for f in fechas]
    for nombre, meses in VENTANAS_CAL.items():
        sen = senal_calendario(meses, nombre)
        if bt.buscar_capturas(sen, len(fechas)):
            raise AssertionError("la senal de calendario captura series")
        res = bt.backtest_senal(activo, 0.002, sen, id_replica=None, variante="prueba", min_historia=MIN_HISTORIA)
        for f, w in zip(res.fechas, res.exposicion):
            if w != (1.0 if f.month in meses else 0.0):
                raise AssertionError(f"exposicion incorrecta en {f} ({nombre})")
        costo_esperado = COMISION + bt.SPREAD_POR_LADO["liquido"]
        for c, rot in zip(res.costo, res.rotacion):
            if rot not in (0.0, 1.0) and abs(rot) > 1e-12:
                raise AssertionError(f"rotacion inesperada {rot}")
            peor = max(peor, abs(c - rot * costo_esperado))
    if peor > 1e-9:
        raise AssertionError(f"prueba de herramientas fallo: {peor}")
    return peor


# ================================================================ reporte

class _Tee:
    def __init__(self, *salidas):
        self.salidas = salidas

    def write(self, x):
        for s in self.salidas:
            s.write(x)

    def flush(self):
        for s in self.salidas:
            s.flush()


def fmt(x, dec: int = 4) -> str:
    if x is None:
        return "NA"
    if isinstance(x, float):
        if math.isnan(x):
            return "NA"
        return "inf" if math.isinf(x) else f"{x:.{dec}f}"
    return str(x)


def ventana(res, f0: date, f1: date) -> dict | None:
    """Metricas del tramo (f0, f1] de una corrida ya hecha + t NW(12) del exceso neto."""
    idx = [i for i, f in enumerate(res.fechas) if f0 < f <= f1]
    if len(idx) < 12:
        return None
    i0, i1 = idx[0], idx[-1] + 1
    fecha_ini = res.curva[i0][0]
    cambios = sum(1 for j in range(i0, i1) if res.exposicion[j] != (res.exposicion[j - 1] if j > 0 else 0.0))
    x = bt.metricas_de_periodos(res.fechas[i0:i1], fecha_ini, res.r_neto[i0:i1], res.r_efectivo[i0:i1],
                                res.exposicion[i0:i1], res.rotacion[i0:i1], res.costo[i0:i1],
                                res.r_activo[i0:i1], res.parametros["periodos_por_anio"], cambios)
    exceso = [a - b for a, b in zip(res.r_neto[i0:i1], res.r_efectivo[i0:i1])]
    anios = (res.fechas[i1 - 1] - fecha_ini).days / 365.25
    x["operaciones_por_anio"] = sum(1 for r in res.rotacion[i0:i1] if r > 1e-12) / anios if anios > 0 else None
    if statistics.pstdev(exceso) == 0:
        x.update({"nw_t": None, "exceso_medio_anual": statistics.fmean(exceso) * 12})
        return x
    nw = est.newey_west(exceso, NW_REZAGOS)
    x.update({"nw_t": nw["t"], "exceso_medio_anual": nw["media"] * 12})
    return x


def limites(res, segmento: str) -> tuple:
    x = res.metricas[segmento]
    return x["fecha_inicio"], x["fecha_fin"]


CLAVES_TABLA = ("cagr", "vol_anual", "sharpe", "nw_t", "sortino", "mdd", "exposicion_media",
                "operaciones_por_anio", "costo_anual")


def tabla(resultados: list, segmento: str) -> str:
    filas = [f"| variante | {' | '.join(CLAVES_TABLA)} |", "|---|" + "---|" * len(CLAVES_TABLA)]
    for r in resultados:
        f0, f1 = limites(r, segmento)
        v = ventana(r, f0, f1)
        if v is None:
            continue
        filas.append(f"| {r.variante} | " + " | ".join(fmt(v[k]) for k in CLAVES_TABLA) + " |")
    return "\n".join(filas)


def tabla_ventanas(resultados: list, ventanas: list) -> str:
    filas = ["| variante | ventana | n | cagr | vol_anual | sharpe | nw_t | mdd | exposicion_media |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in resultados:
        for nombre, f0, f1 in ventanas:
            x = ventana(r, f0, f1)
            if x is None:
                continue
            filas.append(f"| {r.variante} | {nombre} ({x['fecha_inicio']} a {x['fecha_fin']}) | {x['n_periodos']} | "
                         f"{fmt(x['cagr'])} | {fmt(x['vol_anual'])} | {fmt(x['sharpe'])} | {fmt(x['nw_t'], 2)} | "
                         f"{fmt(x['mdd'])} | {fmt(x['exposicion_media'])} |")
    return "\n".join(filas)


def linea_reg(nombre: str, r: dict, i: int = 1) -> str:
    return (f"| {nombre} | {r['n']} | {fmt(r['coef'][i])} | {fmt(r['t_ols'][i], 2)} | {fmt(r['t_hc1'][i], 2)} | "
            f"{fmt(r['t_nw'][i], 2)} | {fmt(r['p_nw'][i])} |")


def reportar_efecto(mercado: str, resultados: dict) -> None:
    print(f"\n### Efecto en {mercado}: regresion y_t = mu + a1*S_t (y en % log mensual)\n")
    print("| ventana | desde | hasta | n | mu (verano) | a1 | t MCO | t HC1 | t NW12 | p NW | media inv. | media ver. |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for nombre, x in resultados.items():
        if x is None:
            continue
        r = x["m1"]
        print(f"| {nombre} | {x['desde']} | {x['hasta']} | {x['n']} | {fmt(r['coef'][0])} | {fmt(r['coef'][1])} | "
              f"{fmt(r['t_ols'][1], 2)} | {fmt(r['t_hc1'][1], 2)} | {fmt(r['t_nw'][1], 2)} | {fmt(r['p_nw'][1])} | "
              f"{fmt(x['media_invierno'])} | {fmt(x['media_verano'])} |")
    print(f"\n### Efecto en {mercado}: pruebas robustas (a1 y t NW12)\n")
    print("| ventana | a1 con enero | t NW | a1 enero (coef) | t NW enero | a1 winsor 1/99 | t NW winsor | "
          "a1 MP-B | t MCO MP-B | a1 MP-C | t MCO MP-C |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for nombre, x in resultados.items():
        if x is None:
            continue
        m2, w = x["m2_enero"], x["winsor"]
        b = x.get("mp_B")
        c = x.get("mp_C")
        print(f"| {nombre} | {fmt(m2['coef'][1])} | {fmt(m2['t_nw'][1], 2)} | {fmt(m2['coef'][2])} | "
              f"{fmt(m2['t_nw'][2], 2)} | {fmt(w['coef'][1])} | {fmt(w['t_nw'][1], 2)} | "
              f"{fmt(b['coef'][1]) if b else 'NA'} | {fmt(b['t_ols'][1], 2) if b else 'NA'} | "
              f"{fmt(c['coef'][1]) if c else 'NA'} | {fmt(c['t_ols'][1], 2) if c else 'NA'} |")
    print(f"\n### Efecto en {mercado}: diferencia anual pareada D_Y (invierno - verano, % log de 6 meses)\n")
    print("| ventana | anios | media D | mediana D | t iid | IC95 bootstrap | D>0 | p signo (1 cola) | 6*a1 | peor anio | mejor anio |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for nombre, x in resultados.items():
        if x is None or x["pareado"].get("n", 0) < 3:
            continue
        p = x["pareado"]
        print(f"| {nombre} | {p['anio_ini']}-{p['anio_fin']} (N={p['n']}) | {fmt(p['media'], 3)} | "
              f"{fmt(p['mediana'], 3)} | {fmt(p['t_iid'], 2)} | [{fmt(p['ic95_bootstrap'][0], 3)}, "
              f"{fmt(p['ic95_bootstrap'][1], 3)}] | {p['positivos']}/{p['n']} | {fmt(p['p_signo_una_cola'])} | "
              f"{fmt(6 * x['m1']['coef'][1], 3)} | {p['peor'][0]}: {fmt(p['peor'][1], 2)} | "
              f"{p['mejor'][0]}: {fmt(p['mejor'][1], 2)} |")
    if any(x is not None and "exceso" in x for x in resultados.values()):
        print(f"\n### Efecto en {mercado}: exceso sobre el efectivo por mitad del anio (% log mensual, t NW12)\n")
        print("| ventana | exceso nov-abr | t NW | exceso may-oct | t NW | semestres inv. (N) | media semestre | "
              "mediana | % semestres > 0 | peor semestre |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        for nombre, x in resultados.items():
            if x is None or "exceso" not in x:
                continue
            e, s = x["exceso"], x["semestres_invierno"]
            if s.get("n", 0) < 3:
                continue
            print(f"| {nombre} | {fmt(e['coef'][0])} | {fmt(e['t_nw'][0], 2)} | {fmt(e['coef'][1])} | "
                  f"{fmt(e['t_nw'][1], 2)} | {s['n']} | {fmt(s['media'], 3)} | {fmt(s['mediana'], 3)} | "
                  f"{fmt(s['pct_positivos'], 3)} | {s['peor'][0]}: {fmt(s['peor'][1], 2)} |")
    print(f"\n### Efecto en {mercado}: placebo de calendario (a1 de las 12 ventanas de 6 meses; lugar de nov-abr)\n")
    for nombre, x in resultados.items():
        if x is None or "placebo" not in x:
            continue
        rot = " ; ".join(f"inicio {k}: {fmt(a, 3)} (t {fmt(t, 2)})" for k, a, t in x["placebo"])
        print(f"- {nombre}: lugar de nov-abr = {x['placebo_lugar_nov']} de 12. {rot}")


def resumen_reg(x: dict | None) -> dict | None:
    if x is None:
        return None
    r = x["m1"]
    salida = {"desde": x["desde"], "hasta": x["hasta"], "n": x["n"], "mu": r["coef"][0], "a1": r["coef"][1],
              "t_ols": r["t_ols"][1], "t_hc1": r["t_hc1"][1], "t_nw12": r["t_nw"][1], "p_nw12": r["p_nw"][1],
              "a1_enero": x["m2_enero"]["coef"][1], "t_nw12_enero": x["m2_enero"]["t_nw"][1],
              "a1_winsor": x["winsor"]["coef"][1], "t_nw12_winsor": x["winsor"]["t_nw"][1],
              "pareado": {k: v for k, v in x["pareado"].items()},
              "placebo_lugar_nov": x.get("placebo_lugar_nov")}
    if "exceso" in x:
        salida.update({"exceso_invierno": x["exceso"]["coef"][0], "t_nw12_exceso_invierno": x["exceso"]["t_nw"][0],
                       "exceso_verano": x["exceso"]["coef"][1], "t_nw12_exceso_verano": x["exceso"]["t_nw"][1],
                       "semestres_invierno": x["semestres_invierno"]})
    if "mp_B" in x:
        salida.update({"mp_B_a1": x["mp_B"]["coef"][1], "mp_B_t_ols": x["mp_B"]["t_ols"][1],
                       "mp_C_a1": x["mp_C"]["coef"][1], "mp_C_t_ols": x["mp_C"]["t_ols"][1]})
    return salida


# ================================================================ principal

def main() -> dict:
    print("R04 - efecto Halloween / Sell in May (Bouman y Jacobsen, 2002)")
    print(f"Comprobaciones sin red (regresion vs estadistica.newey_west, senal de calendario, costos): "
          f"diferencia maxima = {prueba_herramientas():.3e}")

    # ------------------------------------------------ datos
    ff = dh.french("F-F_Research_Data_Factors", "mensual")
    mercado = dh.rendimiento_mercado_french(ff)
    rf_us = dh.columna(ff, "RF")
    exigir_meses_consecutivos(mercado, "French Mkt")
    fuente_us = f"French F-F_Research_Data_Factors CRSP {ff['version_crsp']} sha256 {ff['sha256'][:16]}"
    hm = dh.yahoo_historia("^MXX", "1mo")
    mxx = dh.rendimientos_de_precios(hm["fechas"], hm["precios"])
    exigir_meses_consecutivos(mxx, "^MXX")
    hn = dh.yahoo_historia("NAFTRAC.MX", "1mo")
    naf = dh.rendimientos_de_precios(hn["fechas"], hn["precios"])
    exigir_meses_consecutivos(naf, "NAFTRAC.MX")
    cetes_fred = dh.fred("INTGSTMXM193N")
    cetes, rellenos = cetes_mensual(cetes_fred)
    fx = dh.fred("DEXMXUS")
    fuente_mx = (f"Yahoo ^MXX 1mo (precio, sin dividendos) {hm['fechas'][0]} a {hm['fechas'][-1]}; "
                 f"CETES FRED INTGSTMXM193N {cetes_fred[0][0]} a {cetes_fred[-1][0]} (descarga 2026-09-25)")
    fuente_naf = (f"Yahoo NAFTRAC.MX 1mo adjclose {hn['fechas'][0]} a {hn['fechas'][-1]}; CETES FRED INTGSTMXM193N")
    fuente_usmxn = f"{fuente_us}; FRED DEXMXUS; CETES FRED INTGSTMXM193N"
    print("\n## Datos\n")
    print(f"- French mensual: {ff['fechas'][0]} a {ff['fechas'][-1]} (n={len(ff['fechas'])}), CRSP {ff['version_crsp']}, "
          f"faltantes={ff['faltantes']}, sha256={ff['sha256']}")
    print(f"- ^MXX 1mo: barras {hm['fechas'][0]} a {hm['fechas'][-1]} (n={len(hm['fechas'])}), moneda={hm['moneda']}, "
          f"adjclose={hm['usa_adjclose']}, adjclose!=close={hm['adjclose_difiere_de_close']}, descartes={hm['descartes']}, "
          f"sin_precio={hm['fechas_sin_precio']}; rendimientos {mxx[0][0]} a {mxx[-1][0]} (n={len(mxx)})")
    print(f"- NAFTRAC.MX 1mo: barras {hn['fechas'][0]} a {hn['fechas'][-1]} (n={len(hn['fechas'])}), moneda={hn['moneda']}, "
          f"adjclose={hn['usa_adjclose']}, adjclose!=close={hn['adjclose_difiere_de_close']}, descartes={hn['descartes']}, "
          f"sin_precio={hn['fechas_sin_precio']}; rendimientos {naf[0][0]} a {naf[-1][0]} (n={len(naf)})")
    rell_rango = [f for f in rellenos if mxx[0][0] <= f <= mxx[-1][0]]
    print(f"- CETES (INTGSTMXM193N): {cetes_fred[0][0]} a {cetes_fred[-1][0]} (n={len(cetes_fred)}); meses rellenados "
          f"(arrastre) en todo el rango: {len(rellenos)} {rellenos[:10]}; dentro del rango de ^MXX: {len(rell_rango)}; "
          f"tasa anual min={min(v for _, v in cetes_fred):.2f}%, max={max(v for _, v in cetes_fred):.2f}%")
    print(f"- FRED DEXMXUS: {fx[0][0]} a {fx[-1][0]} (n={len(fx)})")

    # ------------------------------------------------ pruebas del efecto
    rf_us_d = dict(rf_us)
    cetes_d = dict(cetes)
    log_us, log_mx, log_naf = a_log_pct(mercado), a_log_pct(mxx), a_log_pct(naf)
    efecto = {"US": {}, "MX": {}}
    for nombre, f0, f1 in VENTANAS_EFECTO["US"]:
        efecto["US"][nombre] = pruebas_efecto(log_us, rf_us_d, f0, f1)
    for nombre, f0, f1 in VENTANAS_EFECTO["MX"]:
        efecto["MX"][nombre] = pruebas_efecto(log_mx, cetes_d, f0, f1)
    efecto_naf = {"NAFTRAC completo": pruebas_efecto(log_naf, cetes_d, naf[0][0], d(2100, 12))}
    decadas = {}
    for dec in range(1920, 2030, 10):
        decadas[f"{dec}s"] = pruebas_efecto(log_us, None, d(dec, 1), d(dec + 9, 12), placebo=False)

    print("\n## Pruebas del efecto (pre-registro, seccion 8, pruebas 1-9)")
    reportar_efecto("EUA (French Mkt, USD, con dividendos)", efecto["US"])
    reportar_efecto("Mexico (^MXX, MXN, precio sin dividendos; efectivo CETES)", efecto["MX"])
    reportar_efecto("NAFTRAC.MX (rendimiento total, MXN; efectivo CETES)", efecto_naf)
    print("\n### EUA por decada (diagnostico): a1 y t NW12\n")
    print("| decada | desde | hasta | n | a1 | t NW12 | media inv. | media ver. |")
    print("|---|---|---|---|---|---|---|---|")
    for nombre, x in decadas.items():
        if x is None:
            continue
        print(f"| {nombre} | {x['desde']} | {x['hasta']} | {x['n']} | {fmt(x['m1']['coef'][1])} | "
              f"{fmt(x['m1']['t_nw'][1], 2)} | {fmt(x['media_invierno'])} | {fmt(x['media_verano'])} |")

    art = efecto["US"]["ARTICULO 1970-01 a 1998-08"]
    print("\n### Comparacion con Maberly-Pierce (2004), tabla 1 (1970-01 a 1998-08, CRSP VW log)\n")
    print("| modelo | coef | articulo/MP | replica | diferencia | t MP | t MCO replica | t NW12 replica |")
    print("|---|---|---|---|---|---|---|---|")
    print(f"| A | mu | {MP['A']['mu']} | {fmt(art['m1']['coef'][0])} | {fmt(art['m1']['coef'][0] - MP['A']['mu'])} | "
          f"{MP['A']['t_mu']} | {fmt(art['m1']['t_ols'][0], 2)} | {fmt(art['m1']['t_nw'][0], 2)} |")
    print(f"| A | a1 | {MP['A']['a1']} | {fmt(art['m1']['coef'][1])} | {fmt(art['m1']['coef'][1] - MP['A']['a1'])} | "
          f"{MP['A']['t_a1']} | {fmt(art['m1']['t_ols'][1], 2)} | {fmt(art['m1']['t_nw'][1], 2)} |")
    print(f"| B (dummy oct-87 y ago-98) | mu | {MP['B']['mu']} | {fmt(art['mp_B']['coef'][0])} | "
          f"{fmt(art['mp_B']['coef'][0] - MP['B']['mu'])} | 2.08 | {fmt(art['mp_B']['t_ols'][0], 2)} | {fmt(art['mp_B']['t_nw'][0], 2)} |")
    print(f"| B | a1 | {MP['B']['a1']} | {fmt(art['mp_B']['coef'][1])} | {fmt(art['mp_B']['coef'][1] - MP['B']['a1'])} | "
          f"{MP['B']['t_a1']} | {fmt(art['mp_B']['t_ols'][1], 2)} | {fmt(art['mp_B']['t_nw'][1], 2)} |")
    print(f"| B | a2 (dummy) | {MP['B']['a2']} | {fmt(art['mp_B']['coef'][2])} | "
          f"{fmt(art['mp_B']['coef'][2] - MP['B']['a2'])} | -7.27 | {fmt(art['mp_B']['t_ols'][2], 2)} | {fmt(art['mp_B']['t_nw'][2], 2)} |")
    print(f"| C (+ enero) | a1 | {MP['C']['a1']} | {fmt(art['mp_C']['coef'][1])} | {fmt(art['mp_C']['coef'][1] - MP['C']['a1'])} | "
          f"{MP['C']['t_a1']} | {fmt(art['mp_C']['t_ols'][1], 2)} | {fmt(art['mp_C']['t_nw'][1], 2)} |")
    print(f"| C | a3 (enero) | {MP['C']['a3']} | {fmt(art['mp_C']['coef'][3])} | {fmt(art['mp_C']['coef'][3] - MP['C']['a3'])} | "
          f"1.08 | {fmt(art['mp_C']['t_ols'][3], 2)} | {fmt(art['mp_C']['t_nw'][3], 2)} |")

    # ------------------------------------------------ estrategias
    resultados: dict = {}

    def correr(familia: str, nombre: str, senal, escenario: str, es_ref: bool, params: dict,
               activo, efectivo, fuente: str, moneda: str, cortes=(CORTE,), fx_=None, efectivo_en_mxn=False,
               nota_extra: str = ""):
        com, spr, es_sens, nota = ESCENARIOS[escenario]
        es_prueba = (not es_ref) and (not es_sens) and familia in ("US", "MX")
        notas = [n for n in (("referencia" if es_ref else ""), nota, nota_extra) if n]
        r = bt.backtest_senal(activo, efectivo, senal, id_replica=ID, variante=nombre, comision_por_lado=com,
                              spread_por_lado=spr, min_historia=MIN_HISTORIA, cortes=list(cortes), fx=fx_,
                              efectivo_en_mxn=efectivo_en_mxn, moneda=None if fx_ else moneda,
                              parametros={**params, "familia": familia, "escenario_costos": escenario},
                              fuente_datos=fuente, es_prueba=es_prueba, nota="; ".join(notas))
        resultados[(nombre, escenario)] = r
        return r

    def definiciones(prefijo: str) -> list:
        defs = []
        for nombre, meses in VENTANAS_CAL.items():
            defs.append((f"{prefijo}_{nombre}", lambda meses=meses, nombre=nombre: senal_calendario(meses, nombre),
                         False, {"meses": sorted(meses), "tipo": "calendario"}))
        defs += [
            (f"{prefijo}_ref_comprar_mantener", lambda: bt.senal_comprar_y_mantener, True, {"tipo": "referencia"}),
            (f"{prefijo}_ref_efectivo", lambda: bt.senal_efectivo, True, {"tipo": "referencia"}),
            (f"{prefijo}_ref_sma10", lambda: bt.senal_media_movil(10), True, {"tipo": "referencia", "ventana": 10}),
            (f"{prefijo}_ref_verano", lambda: senal_calendario(VERANO, "may_oct"), True,
             {"tipo": "referencia", "meses": sorted(VERANO)}),
        ]
        return defs

    familias = {
        "US": (definiciones("US"), mercado, rf_us, fuente_us, "USD"),
        "MX": (definiciones("MX"), mxx, cetes, fuente_mx, "MXN"),
    }
    for escenario in ("defecto", "medio", "bruto"):
        for familia, (defs, activo, efectivo, fuente, moneda) in familias.items():
            for nombre, fab, es_ref, params in defs:
                correr(familia, nombre, fab(), escenario, es_ref, params, activo, efectivo, fuente, moneda)
    sens = [("USMXN_nov_abr", lambda: senal_calendario(INVIERNO, "nov_abr"), False, {"meses": sorted(INVIERNO)}),
            ("USMXN_ref_comprar_mantener", lambda: bt.senal_comprar_y_mantener, True, {"tipo": "referencia"}),
            ("USMXN_ref_efectivo", lambda: bt.senal_efectivo, True, {"tipo": "referencia"}),
            ("USMXN_ref_sma10", lambda: bt.senal_media_movil(10), True, {"tipo": "referencia", "ventana": 10})]
    for nombre, fab, es_ref, params in sens:
        correr("USMXN", nombre, fab(), "defecto", es_ref, {**params, "moneda": "MXN"}, mercado, cetes, fuente_usmxn,
               "MXN", fx_=fx, efectivo_en_mxn=True,
               nota_extra="sensibilidad: MXN (activo EUA convertido con DEXMXUS; efectivo CETES)")
    for nombre, fab, es_ref, params in sens:
        nombre_n = nombre.replace("USMXN", "NAFTRAC")
        correr("NAFTRAC", nombre_n, fab(), "defecto", es_ref, params, naf, cetes, fuente_naf, "MXN", cortes=(),
               nota_extra="sensibilidad: NAFTRAC rendimiento total (todo posterior a 2002, sin corte)")

    # la exposicion de toda variante de calendario coincide con su definicion
    for (nombre, esc), r in resultados.items():
        meses = None
        for k, m in VENTANAS_CAL.items():
            if nombre.endswith("_" + k):
                meses = m
        if nombre.endswith("_ref_verano"):
            meses = VERANO
        if meses is not None:
            for f, w in zip(r.fechas, r.exposicion):
                if w != (1.0 if f.month in meses else 0.0):
                    raise AssertionError(f"{nombre} {esc}: exposicion incorrecta en {f}")
    print(f"\nCorridas de estrategia registradas en esta ejecucion: {len(resultados)} (exposiciones de calendario verificadas)")

    def R(nombre: str, esc: str = "defecto"):
        return resultados[(nombre, esc)]

    print("\n## Estrategias")
    for familia, (defs, *_resto) in familias.items():
        nombres = [n for n, *_ in defs]
        for esc in ("defecto", "medio", "bruto"):
            for seg in ("completo", "dentro_muestra", "fuera_muestra"):
                f0, f1 = limites(R(nombres[0], esc), seg)
                print(f"\n### {familia} - costos {esc} - segmento {seg} ({f0} a {f1})\n")
                print(tabla([R(n, esc) for n in nombres], seg))
    for prefijo in ("USMXN", "NAFTRAC"):
        nombres = [n.replace("USMXN", prefijo) for n, *_ in sens]
        segs = ("completo", "dentro_muestra", "fuera_muestra") if prefijo == "USMXN" else ("completo",)
        for seg in segs:
            f0, f1 = limites(R(nombres[0]), seg)
            print(f"\n### {prefijo} (sensibilidad, MXN) - costos defecto - segmento {seg} ({f0} a {f1})\n")
            print(tabla([R(n) for n in nombres], seg))

    ventanas_us = [("pre-articulo", d(1927, 4), d(1969, 12)), ("articulo", d(1969, 12), d(1998, 8)),
                   ("hueco", d(1998, 8), CORTE), ("fuera de muestra", CORTE, FIN)]
    ventanas_mx = [("traslape articulo", d(1992, 9), d(1998, 8)), ("hueco", d(1998, 8), CORTE),
                   ("fuera de muestra", CORTE, FIN)]
    print("\n### EUA: ventanas pre-registradas, costos por defecto\n")
    print(tabla_ventanas([R(n) for n in ("US_nov_abr", "US_ref_comprar_mantener", "US_ref_sma10", "US_ref_verano")],
                         ventanas_us))
    print("\n### Mexico: ventanas pre-registradas, costos por defecto\n")
    print(tabla_ventanas([R(n) for n in ("MX_nov_abr", "MX_ref_comprar_mantener", "MX_ref_sma10", "MX_ref_verano")],
                         ventanas_mx))

    # ------------------------------------------------ DSR
    print("\n## Sharpe deflactado (registro R04)\n")
    filas = bt.leer_registro(ID)
    pruebas = {}
    for f in filas:
        if f["es_prueba"] == 1:
            pruebas[(f["variante"], f["parametros_json"], f["segmento"])] = f
    n_prueba = len({(v, p) for v, p, _ in pruebas})
    print(f"- Variantes distintas con es_prueba=1: {n_prueba}; filas totales en el CSV: {len(filas)}")
    dsr_res: dict = {}

    def dsr(clave: str, **kw) -> str:
        try:
            x = bt.sharpe_deflactado_de_registro(ID, **kw)
        except ValueError as e:
            dsr_res[clave] = {"error": str(e)}
            return f"error: {e}"
        dsr_res[clave] = x
        return (f"variante={x['variante']} seg={x['segmento']} DSR={x['dsr']:.4f} cumple={x['cumple']} "
                f"N={x['n_pruebas']} V_periodo={x['varianza_sharpes_periodo']:.6f} SR_anual={x['sr_anual']:.4f} "
                f"SR0_anual={x['sr0_anual']:.4f} n_obs={x['n_obs']} asim={x['asimetria']:.3f} "
                f"curt={x['curtosis']:.3f} PSR={x['psr_sin_deflactar']:.4f}")

    print(f"- Por defecto (mejor de las {n_prueba}, dentro_muestra, V de todas): {dsr('defecto')}")
    for seg in ("dentro_muestra", "fuera_muestra"):
        for familia in ("US", "MX"):
            cand = [(f["sharpe_periodo"], v) for (v, p, s), f in pruebas.items()
                    if s == seg and v.startswith(familia + "_") and f["sharpe_periodo"] is not None]
            v_fam = statistics.variance([c[0] for c in cand])
            mejor = max(cand)[1]
            print(f"- Familia {familia} [{seg}] mejor de la familia, V de la familia ({len(cand)} Sharpes), N={n_prueba}: "
                  f"{dsr(f'{familia}_{seg}_mejor_Vfam', segmento=seg, variante=mejor, varianza_sharpes=v_fam, n_pruebas=n_prueba)}")
            print(f"- Familia {familia} [{seg}] regla del articulo, V de la familia, N={n_prueba}: "
                  f"{dsr(f'{familia}_{seg}_articulo_Vfam', segmento=seg, variante=f'{familia}_nov_abr', varianza_sharpes=v_fam, n_pruebas=n_prueba)}")
            print(f"- Familia {familia} [{seg}] regla del articulo, V de todas, N={n_prueba}: "
                  f"{dsr(f'{familia}_{seg}_articulo_Vtodas', segmento=seg, variante=f'{familia}_nov_abr')}")

    # ------------------------------------------------ criterios pre-registrados
    print("\n## Criterios pre-registrados (seccion 2)\n")

    def reg(mercado_: str, nombre: str) -> dict:
        return efecto[mercado_][nombre]

    us_art = reg("US", "ARTICULO 1970-01 a 1998-08")
    us_in = reg("US", "dentro_muestra 1926-07 a 2002-12")
    us_oos = reg("US", "fuera_muestra 2003-01 al final")
    mx_oos = reg("MX", "fuera_muestra 2003-01 al final")
    a_art = us_art["m1"]["coef"][1]
    c_i = a_art > 0 and abs(a_art - MP["A"]["a1"]) <= TOLERANCIA_PP and us_art["m1"]["t_ols"][1] >= 1.96
    c_ii = us_in["m1"]["coef"][1] > 0 and us_in["m1"]["t_nw"][1] >= 2
    c_iii = us_oos["m1"]["coef"][1] > 0
    c_iv = mx_oos["m1"]["coef"][1] > 0
    print(f"- (i) EUA 1970-01..1998-08: a1={a_art:.4f} (MP {MP['A']['a1']}; |dif|={abs(a_art - MP['A']['a1']):.4f} "
          f"<= {TOLERANCIA_PP}?), t MCO={us_art['m1']['t_ols'][1]:.2f} -> {c_i}")
    print(f"- (ii) EUA 1926-07..2002-12: a1={us_in['m1']['coef'][1]:.4f}, t NW12={us_in['m1']['t_nw'][1]:.2f} -> {c_ii}")
    print(f"- (iii) EUA 2003-01..final: a1={us_oos['m1']['coef'][1]:.4f} -> {c_iii}")
    print(f"- (iv) Mexico 2003-01..final: a1={mx_oos['m1']['coef'][1]:.4f} -> {c_iv}")
    if a_art <= 0 or (not c_iii and not c_iv):
        estado = "No replicado"
    elif c_i and c_ii and c_iii and c_iv:
        estado = "Replicado"
    elif a_art > 0 and (c_iii or c_iv):
        estado = "Replicado con diferencias"
    else:
        estado = "Pendiente (caso no previsto por la regla)"
    print(f"- Estado segun la regla pre-registrada: {estado}")

    def significativo(x: dict) -> bool:
        p = x["pareado"]
        return x["m1"]["t_nw"][1] >= 2 and p["ic95_bootstrap"][0] > 0

    sig = {}
    for mercado_, x in (("US", us_oos), ("MX", mx_oos)):
        sig[mercado_] = significativo(x)
        print(f"- Significativo fuera de muestra {mercado_} (t NW12 >= 2 y IC95 bootstrap de D excluye 0): {sig[mercado_]} "
              f"(t NW12={x['m1']['t_nw'][1]:.2f}; IC95 D=[{x['pareado']['ic95_bootstrap'][0]:.3f}, "
              f"{x['pareado']['ic95_bootstrap'][1]:.3f}]); exceso nov-abr={x['exceso']['coef'][0]:.4f} "
              f"(t NW12={x['exceso']['t_nw'][0]:.2f})")
    confirmar = any(sig[m_] and x["exceso"]["coef"][0] > 0 and x["exceso"]["t_nw"][0] >= 2
                    for m_, x in (("US", us_oos), ("MX", mx_oos)))
    descartar = us_oos["m1"]["coef"][1] <= 0 and mx_oos["m1"]["coef"][1] <= 0
    modificar = (not confirmar) and (not descartar) and any(
        x["exceso"]["coef"][0] > 0 for x in (us_oos, mx_oos))
    decision = "confirmar" if confirmar else "descartar" if descartar else "modificar" if modificar else "caso no previsto"
    print(f"- Regla [R] 6 de arena/investigacion/03 segun el criterio pre-registrado: {decision}")
    h5 = {}
    for familia in ("US", "MX"):
        s = R(f"{familia}_nov_abr")
        for ref in ("ref_comprar_mantener", "ref_sma10"):
            b = R(f"{familia}_{ref}")
            xs, xb = s.metricas["fuera_muestra"], b.metricas["fuera_muestra"]
            gana = xs["sharpe"] > xb["sharpe"] and xs["mdd"] > xb["mdd"]
            h5[f"{familia}_vs_{ref}"] = gana
            print(f"- H5 {familia}_nov_abr vs {familia}_{ref} fuera de muestra: Sharpe {xs['sharpe']:.4f} vs {xb['sharpe']:.4f}; "
                  f"MDD {xs['mdd']:.4f} vs {xb['mdd']:.4f}; CAGR {xs['cagr']:.4f} vs {xb['cagr']:.4f} -> "
                  f"{'supera en Sharpe y MDD' if gana else 'NO supera en ambos'}")

    # ------------------------------------------------ salida json
    def met(nombre: str, esc: str = "defecto") -> dict:
        r = R(nombre, esc)
        return {s: {k: r.metricas[s][k] for k in ("fecha_inicio", "fecha_fin", "n_periodos", "cagr", "vol_anual",
                                                   "sharpe", "mdd", "exposicion_media", "costo_anual")}
                for s in ["completo"] + r.segmentos}

    salida = {
        "id": ID, "corte": CORTE,
        "datos": {"french_version_crsp": ff["version_crsp"], "french_sha256": ff["sha256"],
                  "french_rango": [ff["fechas"][0], ff["fechas"][-1]], "mxx_rango": [mxx[0][0], mxx[-1][0]],
                  "naftrac_rango": [naf[0][0], naf[-1][0]], "cetes_rango": [cetes_fred[0][0], cetes_fred[-1][0]],
                  "cetes_rellenos_rango_mxx": len(rell_rango), "dexmxus_rango": [fx[0][0], fx[-1][0]],
                  "huella_US": R("US_nov_abr").meta["huella_datos"], "huella_MX": R("MX_nov_abr").meta["huella_datos"]},
        "efecto": {m_: {k: resumen_reg(v) for k, v in x.items()} for m_, x in efecto.items()},
        "efecto_naftrac": resumen_reg(efecto_naf["NAFTRAC completo"]),
        "estrategias_defecto": {n: met(n) for (n, esc) in resultados if esc == "defecto"},
        "dsr": dsr_res,
        "criterios": {"i": c_i, "ii": c_ii, "iii": c_iii, "iv": c_iv, "estado": estado,
                      "significativo_oos": sig, "regla_R6": decision, "h5": h5},
    }
    (DIR / "R04-resultados.json").write_text(json.dumps(salida, indent=1, ensure_ascii=False, default=str),
                                             encoding="utf-8")
    return salida


if __name__ == "__main__":
    buffer = io.StringIO()
    original = sys.stdout
    sys.stdout = _Tee(original, buffer)
    try:
        main()
    finally:
        sys.stdout = original
        (DIR / "R04-salida.txt").write_text(buffer.getvalue(), encoding="utf-8")
