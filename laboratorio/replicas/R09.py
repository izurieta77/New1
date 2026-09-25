#!/usr/bin/env python3
"""R09 - Efecto de cambio de mes / turn of the month (Lakonishok y Smidt, 1988, RFS 1(4):403-425;
McConnell y Xu, 2008, FAJ 64(2):49-64).

Reproduce desde la raiz del repo:  python3 laboratorio/replicas/R09.py
Solo biblioteca estandar. Cada corrida de estrategia se agrega a laboratorio/replicas/R09-variantes.csv.
La salida completa se guarda tambien en R09-salida.txt y las cifras clave en R09-resultados.json.

Pre-registro: R09-efecto-cambio-de-mes.md, secciones 1-9.
  TOM = dias de negociacion -1 (ultimo del mes) y +1, +2, +3 (primeros del mes siguiente).
  Efecto: regresion diaria y_t = mu + delta*TOM_t + e_t con y_t = 100*r_t (rendimiento simple bruto);
    t MCO, HC1 y Newey-West (Bartlett, 10 rezagos). Comparacion estrecha de McConnell-Xu (TOM contra
    dias -10..-2 y +4..+10), diferencia mensual pareada (bootstrap y signo), estilo L&S (acumulado de
    4 dias contra el mes), exceso por evento, winsorizacion, sin dic-ene, sin cierres no programados,
    dia relativo y placebo.
  Datos: French F-F_Research_Data_Factors_daily (Mkt-RF + RF, CRSP, USD, con dividendos) y Yahoo
    ^GSPC 1d (indice de PRECIO, sin dividendos, sin sabados antes de 1953).
  Estrategia: mercado en la ventana [a, b] y efectivo el resto, con costos GBM. Corte 2008-02-29
    (publicacion en el FAJ de marzo/abril de 2008).
"""
from __future__ import annotations

import collections
import io
import json
import math
import random
import statistics
import sys
from datetime import date
from operator import mul
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from herramientas import backtest as bt  # noqa: E402
from herramientas import datos_historicos as dh  # noqa: E402
from herramientas import estadistica as est  # noqa: E402

# ================================================================ parametros pre-registrados
ID = "R09"
DIR = Path(__file__).resolve().parent
CORTE = date(2008, 2, 29)
INICIO_FUERA = date(2008, 3, 1)
FIN = date(2100, 1, 1)
FIN_SPX_EFECTO = date(2026, 8, 31)  # ultimo mes completo de ^GSPC
MIN_HISTORIA = 200
NW_REZAGOS = 10
BOOT_REPS = 10_000
BOOT_SEMILLA = 9
TOLERANCIA_PP = 0.03
WINSOR = (0.005, 0.995)
HUECO_DIAS = 4  # hueco de mas de 4 dias naturales = posible cierre no programado
CUENTA_MXN = 20_000
VENTANAS_TOM = {  # nombre -> (a, b): en el mercado si pos_fin >= a o pos_ini <= b (lista cerrada)
    "m1_p3": (-1, 3),
    "m2_p3": (-2, 3),
    "m3_p3": (-3, 3),
    "m1_p2": (-1, 2),
    "m1_p4": (-1, 4),
}
# McConnell y Xu, version de trabajo del 14-jul-2006, tabla 1 (CRSP VW, rendimiento diario bruto, %)
MX_T1 = {
    "A": {"desde": "1926-01", "hasta": "1986-12", "d-1": 0.17, "d+1": 0.09, "d+2": 0.18, "d+3": 0.21,
          "tom": 0.16, "t_tom": 8.50, "otros": 0.01, "t_otros": 0.98, "dif": 0.15, "t_dif": 7.07, "pos_dif": 62},
    "B": {"desde": "1987-01", "hasta": "2005-12", "d-1": 0.19, "d+1": 0.25, "d+2": 0.13, "d+3": 0.08,
          "tom": 0.15, "t_tom": 4.35, "otros": -0.00, "t_otros": -0.07, "dif": 0.15, "t_dif": 3.78, "pos_dif": 61},
    "C": {"desde": "1926-01", "hasta": "2005-12", "d-1": 0.18, "d+1": 0.12, "d+2": 0.17, "d+3": 0.18,
          "tom": 0.16, "t_tom": 9.60, "otros": 0.01, "t_otros": 0.87, "dif": 0.15, "t_dif": 8.06, "pos_dif": 62},
}
# Tabla 2, panel C (exceso sobre la T-bill de 30 dias, VW, 1926-2005)
MX_T2_C = {"tom": 0.15, "t_tom": 8.98, "otros": 0.00, "t_otros": 0.15, "dif": 0.15, "t_dif": 7.93}
# Lakonishok y Smidt (1988) citados por McConnell-Xu: DJIA (precio) 1897-1986
LS = {"tom_4d": 0.473, "mes": 0.349}
COMISION = bt.COMISION_GBM_POR_LADO
COSTO_LADO = COMISION + bt.SPREAD_POR_LADO["liquido"]
ESCENARIOS = {  # nombre -> (comision, spread, es_sensibilidad, nota)
    "defecto": (COMISION, bt.SPREAD_POR_LADO["liquido"], False, ""),
    "medio": (COMISION, bt.SPREAD_POR_LADO["medio"], True, "sensibilidad: spread medio 0.15% por lado"),
    "bruto": (0.0, 0.0, True, "sensibilidad: bruto (sin comision ni spread)"),
}
NORMAL = statistics.NormalDist()


def _ventanas(inicio: date) -> list:
    return [
        ("completo", inicio, FIN),
        ("dentro_muestra hasta 2008-02", inicio, CORTE),
        ("fuera_muestra 2008-03 al final", INICIO_FUERA, FIN),
        ("MX panel A 1926-1986", inicio, date(1986, 12, 31)),
        ("MX panel B 1987-2005", date(1987, 1, 1), date(2005, 12, 31)),
        ("MX panel C 1926-2005", inicio, date(2005, 12, 31)),
        ("hueco 2006-01 a 2008-02", date(2006, 1, 1), CORTE),
        ("fuera mitad 1 2008-03 a 2016-12", INICIO_FUERA, date(2016, 12, 31)),
        ("fuera mitad 2 2017-01 al final", date(2017, 1, 1), FIN),
    ]


# ================================================================ regresion (stdlib, por columnas)

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


def regresion(y: list, cols: list, rezagos: int = NW_REZAGOS) -> dict:
    """MCO de y sobre las columnas cols (listas de largo n) con EE MCO, HC1 y Newey-West (Bartlett).

    HC1 y NW llevan la correccion n/(n-k). Con cols = [unos] la varianza NW coincide con
    herramientas.estadistica.newey_west (se comprueba en prueba_herramientas)."""
    n, k = len(y), len(cols)
    if n <= k + 2:
        raise ValueError("muy pocas observaciones")
    XtX = [[math.fsum(map(mul, cols[i], cols[j])) for j in range(k)] for i in range(k)]
    Xty = [math.fsum(map(mul, cols[i], y)) for i in range(k)]
    inv = _inversa(XtX)
    b = [sum(inv[i][j] * Xty[j] for j in range(k)) for i in range(k)]
    ajuste = [0.0] * n
    for i in range(k):
        bi = b[i]
        ajuste = [a + bi * x for a, x in zip(ajuste, cols[i])]
    e = [a - f for a, f in zip(y, ajuste)]
    s2 = math.fsum(v * v for v in e) / (n - k)
    g = [list(map(mul, cols[i], e)) for i in range(k)]

    def gamma(j: int) -> list:
        return [[math.fsum(map(mul, g[a][j:], g[c][:n - j])) for c in range(k)] for a in range(k)]

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


def reg_dummy(y: list, dummy: list) -> dict:
    return regresion(y, [[1.0] * len(y), dummy])


def t_media(x: list) -> float:
    if len(x) < 3:
        return float("nan")
    sd = statistics.stdev(x)
    return statistics.fmean(x) / (sd / math.sqrt(len(x))) if sd > 0 else float("nan")


def t_welch(a: list, b: list) -> float:
    va, vb = statistics.variance(a), statistics.variance(b)
    return (statistics.fmean(a) - statistics.fmean(b)) / math.sqrt(va / len(a) + vb / len(b))


def bootstrap_media(vals: list) -> tuple:
    rng = random.Random(BOOT_SEMILLA)
    N = len(vals)
    medias = sorted(statistics.fmean(rng.choices(vals, k=N)) for _ in range(BOOT_REPS))
    return medias[int(0.025 * BOOT_REPS)], medias[int(0.975 * BOOT_REPS) - 1]


def p_signo(positivos: int, N: int) -> float:
    return sum(math.comb(N, i) for i in range(positivos, N + 1)) / 2 ** N


def resumen_muestra(vals: list) -> dict:
    """Media, mediana, t iid, IC95 bootstrap, positivos y p de signo de una lista de unidades."""
    N = len(vals)
    if N < 5:
        return {"n": N}
    pos = sum(1 for v in vals if v > 0)
    return {"n": N, "media": statistics.fmean(vals), "mediana": statistics.median(vals), "t_iid": t_media(vals),
            "ic95_bootstrap": bootstrap_media(vals), "positivos": pos, "pct_positivos": pos / N,
            "p_signo_una_cola": p_signo(pos, N)}


# ================================================================ calendario

def posiciones(fechas: list) -> dict:
    """fecha -> (pos_ini, pos_fin): +1.. desde el primer dia de negociacion del mes calendario y
    -1.. desde el ultimo. Se calcula sobre las fechas de la propia serie."""
    grupos: dict = {}
    for f in fechas:
        grupos.setdefault((f.year, f.month), []).append(f)
    salida = {}
    for dias in grupos.values():
        dias.sort()
        N = len(dias)
        for i, f in enumerate(dias):
            salida[f] = (i + 1, i - N)
    return salida


def en_ventana(pi: int, pf: int, a: int = -1, b: int = 3) -> bool:
    return pf >= a or pi <= b


def es_otro_mx(pi: int, pf: int) -> bool:
    return (not en_ventana(pi, pf)) and (-10 <= pf <= -2 or 4 <= pi <= 10)


def tau(pi: int, pf: int) -> int:
    """Dia relativo al cambio de mes: -1 = ultimo dia; 0, 1, 2 = +1, +2, +3; -2.. y 3.. hacia el medio."""
    return pf if -pf <= pi - 1 else pi - 1


def construir_serie(fechas: list, r: list, rf: list, pos: dict) -> dict:
    pi = [pos[f][0] for f in fechas]
    pf = [pos[f][1] for f in fechas]
    return {"fechas": fechas, "r": r, "rf": rf, "pi": pi, "pf": pf,
            "tom": [1.0 if en_ventana(a, b) else 0.0 for a, b in zip(pi, pf)]}


def unidades_mensuales(s: dict) -> list:
    """Una unidad por mes calendario m con TOM completo (dia -1 de m y +1..+3 de m+1) y resto
    (+4..-2 de m) no vacio. Se fecha con el dia -1 de m."""
    meses: dict = {}
    for i, f in enumerate(s["fechas"]):
        meses.setdefault((f.year, f.month), []).append(i)
    claves = sorted(meses)
    unidades = []
    for k, clave in enumerate(claves[:-1]):
        sig = claves[k + 1]
        y, m = clave
        if sig != ((y + 1, 1) if m == 12 else (y, m + 1)):
            raise ValueError(f"meses no consecutivos en la serie: {clave} -> {sig}")
        L, Ls = meses[clave], meses[sig]
        if s["pf"][L[-1]] != -1 or len(Ls) < 3 or [s["pi"][i] for i in Ls[:3]] != [1, 2, 3]:
            continue
        tom = [L[-1]] + Ls[:3]
        resto = [i for i in L if s["pi"][i] >= 4 and s["pf"][i] <= -2]
        if not resto:
            continue
        d2 = [i for i in L if s["pf"][i] == -2]
        f_m2 = s["fechas"][d2[0]] if d2 else None
        f_m1, f_p1 = s["fechas"][L[-1]], s["fechas"][Ls[0]]
        hueco = (f_m2 is not None and (f_m1 - f_m2).days > HUECO_DIAS) or (f_p1 - f_m1).days > HUECO_DIAS
        unidades.append({"fecha": f_m1, "tom": tom, "resto": resto, "mes": L, "hueco": hueco,
                         "dic_ene": m == 12})
    return unidades


# ================================================================ pruebas del efecto

def pruebas_efecto(s: dict, unidades: list, f0: date, f1: date, completo: bool = True) -> dict | None:
    """Todas las pruebas pre-registradas en [f0, f1] (inclusivo). Dias por su fecha; unidades
    mensuales por la fecha de su dia -1."""
    idx = [i for i, f in enumerate(s["fechas"]) if f0 <= f <= f1]
    if len(idx) < 250:
        return None
    r, rf, pi, pf = s["r"], s["rf"], s["pi"], s["pf"]
    y = [100.0 * r[i] for i in idx]
    T = [s["tom"][i] for i in idx]
    salida: dict = {"desde": s["fechas"][idx[0]], "hasta": s["fechas"][idx[-1]], "n": len(idx)}
    salida["m1"] = reg_dummy(y, T)
    y_tom = [v for v, t in zip(y, T) if t == 1.0]
    y_resto = [v for v, t in zip(y, T) if t == 0.0]
    salida["media_tom"], salida["media_resto"] = statistics.fmean(y_tom), statistics.fmean(y_resto)
    salida["n_tom"], salida["n_resto"] = len(y_tom), len(y_resto)
    if not completo:
        return salida
    # comparacion estrecha de McConnell-Xu
    sub = [i for i in idx if s["tom"][i] == 1.0 or es_otro_mx(pi[i], pf[i])]
    ys = [100.0 * r[i] for i in sub]
    Ts = [s["tom"][i] for i in sub]
    reg_mx = reg_dummy(ys, Ts)
    a_tom = [v for v, t in zip(ys, Ts) if t == 1.0]
    a_otr = [v for v, t in zip(ys, Ts) if t == 0.0]
    por_dia = {}
    for nombre, cond in (("d-1", lambda a, b: b == -1), ("d+1", lambda a, b: a == 1),
                         ("d+2", lambda a, b: a == 2), ("d+3", lambda a, b: a == 3)):
        v = [100.0 * r[i] for i in idx if cond(pi[i], pf[i])]
        por_dia[nombre] = {"media": statistics.fmean(v), "t": t_media(v), "n": len(v),
                           "pct_pos": sum(1 for x in v if x > 0) / len(v)}
    ex_tom = [100.0 * (r[i] - rf[i]) for i in sub if s["tom"][i] == 1.0]
    ex_otr = [100.0 * (r[i] - rf[i]) for i in sub if s["tom"][i] == 0.0]
    salida["mx"] = {"reg": reg_mx, "tom": statistics.fmean(a_tom), "t_tom": t_media(a_tom),
                    "otros": statistics.fmean(a_otr), "t_otros": t_media(a_otr), "n_tom": len(a_tom),
                    "n_otros": len(a_otr), "t_welch": t_welch(a_tom, a_otr),
                    "pct_pos_tom": sum(1 for v in a_tom if v > 0) / len(a_tom),
                    "pct_pos_otros": sum(1 for v in a_otr if v > 0) / len(a_otr), "por_dia": por_dia,
                    "ex_tom": statistics.fmean(ex_tom), "t_ex_tom": t_media(ex_tom),
                    "ex_otros": statistics.fmean(ex_otr), "t_ex_otros": t_media(ex_otr)}
    # winsorizacion diaria dentro de la ventana
    q = statistics.quantiles(y, n=1000, method="inclusive")
    lo, hi = q[round(WINSOR[0] * 1000) - 1], q[round(WINSOR[1] * 1000) - 1]
    salida["winsor"] = reg_dummy([min(max(v, lo), hi) for v in y], T)
    salida["winsor_limites"] = (lo, hi)
    # unidades mensuales de la ventana
    U = [u for u in unidades if f0 <= u["fecha"] <= f1]
    excl_dic = set()
    excl_hueco = set()
    for u in unidades:
        if u["dic_ene"]:
            excl_dic.update(u["tom"])
        if u["hueco"]:
            excl_hueco.update(u["tom"])
    for clave, excl in (("sin_dic_ene", excl_dic), ("sin_cierres", excl_hueco)):
        keep = [(v, t) for i, v, t in zip(idx, y, T) if i not in excl]
        salida[clave] = reg_dummy([v for v, _ in keep], [t for _, t in keep])
    salida["meses_con_hueco"] = [u["fecha"] for u in U if u["hueco"]]
    D, E, cum_tom, cum_mes, cum_resto = [], [], [], [], []
    for u in U:
        mt = statistics.fmean(100.0 * r[i] for i in u["tom"])
        mr = statistics.fmean(100.0 * r[i] for i in u["resto"])
        D.append(mt - mr)
        ct = math.prod(1 + r[i] for i in u["tom"])
        cf = math.prod(1 + rf[i] for i in u["tom"])
        E.append(100.0 * (ct - cf))
        cum_tom.append(100.0 * (ct - 1))
        cum_mes.append(100.0 * (math.prod(1 + r[i] for i in u["mes"]) - 1))
        cum_resto.append(100.0 * (math.prod(1 + r[i] for i in u["resto"]) - 1))
    salida["D"] = resumen_muestra(D)
    salida["E"] = resumen_muestra(E)
    salida["ls"] = {"n": len(U), "tom_4d": statistics.fmean(cum_tom), "mes": statistics.fmean(cum_mes),
                    "resto": statistics.fmean(cum_resto),
                    "razon_tom_mes": statistics.fmean(cum_tom) / statistics.fmean(cum_mes)
                    if statistics.fmean(cum_mes) != 0 else float("nan")}
    # dia relativo y placebo
    por_tau: dict = {}
    for i, v in zip(idx, y):
        k = tau(pi[i], pf[i])
        if -10 <= k <= 9:
            por_tau.setdefault(k, []).append(v)
    salida["tau"] = {k: (statistics.fmean(v), t_media(v), len(v)) for k, v in sorted(por_tau.items())}
    ventanas4 = []
    for s0 in range(-9, 7):
        vals = [v for k in range(s0, s0 + 4) for v in por_tau.get(k, [])]
        ventanas4.append((s0, statistics.fmean(vals)))
    orden = sorted(ventanas4, key=lambda x: -x[1])
    salida["placebo"] = ventanas4
    salida["placebo_lugar_tom"] = 1 + [k for k, _ in orden].index(-1)
    return salida


# ================================================================ senal de calendario

def senal_tom(a: int, b: int, nombre: str, invertir: bool = False):
    """Exposicion 1 si el dia a decidir cae en [a, b] (pos_fin >= a o pos_ini <= b). Lee solo las
    extras 'pos_ini_sig' y 'pos_fin_sig' publicadas al cierre de t-1 (calendario de sesiones,
    conocido de antemano; supuesto declarado en la seccion 5). No lee rendimientos."""

    def senal(h):
        f = h.fecha_decision
        if f is None:
            raise ValueError("sin fecha de decision: sube min_historia")
        vi, vf = h.extras["pos_ini_sig"], h.extras["pos_fin_sig"]
        if not len(vi) or vi[-1][0] != f or vf[-1][0] != f:
            raise ValueError(f"calendario desalineado en {f}")
        dentro = vf[-1][1] >= a or vi[-1][1] <= b
        if invertir:
            dentro = not dentro
        return 1.0 if dentro else 0.0

    senal.__qualname__ = senal.__name__ = f"cambio_de_mes_{nombre}"
    return senal


def extras_calendario(fechas: list, pos: dict) -> dict:
    """Para cada fecha d_{t-1} (fecha de disponibilidad): la posicion del dia siguiente de la serie."""
    return {"pos_ini_sig": [(fechas[i], float(pos[fechas[i + 1]][0])) for i in range(len(fechas) - 1)],
            "pos_fin_sig": [(fechas[i], float(pos[fechas[i + 1]][1])) for i in range(len(fechas) - 1)]}


# ================================================================ datos

def rf_en_fechas(fechas: list, rf_french: list, fecha_base: date) -> tuple[list, int]:
    """RF diaria de French compuesta sobre las fechas de French en (d_{t-1}, d_t]; d_0 = fecha_base
    (el precio base de la serie). Devuelve la serie y cuantas fechas no tienen ninguna fecha French."""
    fr = [f for f, _ in rf_french]
    vr = [v for _, v in rf_french]
    salida, sin_french = [], 0
    j = 0
    while j < len(fr) and fr[j] <= fecha_base:
        j += 1
    for f in fechas:
        acum, cuenta = 1.0, 0
        while j < len(fr) and fr[j] <= f:
            acum *= 1 + vr[j]
            cuenta += 1
            j += 1
        if cuenta == 0:
            sin_french += 1
        salida.append((f, acum - 1))
    return salida, sin_french


def cetes_diario(fechas: list, serie_fred: list) -> tuple[list, list]:
    """Tasa anual promedio del mes (FRED, dia 1) -> r = tasa/100 * dias naturales desde la fecha anterior/360.
    Meses sin dato dentro del rango: se arrastra la tasa previa (se reportan)."""
    tasas = {(f.year, f.month): v for f, v in serie_fred}
    primero = min(tasas)
    salida, rellenos, previa_tasa = [], set(), None
    for k, f in enumerate(fechas):
        if (f.year, f.month) < primero or k == 0:
            continue
        clave = (f.year, f.month)
        if clave in tasas:
            tasa = tasas[clave]
        elif previa_tasa is not None:
            tasa = previa_tasa
            rellenos.add(clave)
        else:
            continue
        salida.append((f, tasa / 100.0 * (f - fechas[k - 1]).days / 360.0))
        previa_tasa = tasa
    return salida, sorted(rellenos)


# ================================================================ comprobaciones sin red

def prueba_herramientas() -> float:
    rnd = random.Random(11)
    peor = 0.0
    x = [rnd.gauss(0.05, 1.0) for _ in range(600)]
    for L in (0, 5, 10):
        rg = regresion(x, [[1.0] * len(x)], L)
        nw = est.newey_west(x, L)
        peor = max(peor, abs(rg["coef"][0] - nw["media"]), abs(rg["se_nw"][0] - nw["se"]))
    d = [1.0 if i % 5 == 0 else 0.0 for i in range(600)]
    r2 = reg_dummy(x, d)
    dif = statistics.fmean(v for v, di in zip(x, d) if di) - statistics.fmean(v for v, di in zip(x, d) if not di)
    peor = max(peor, abs(r2["coef"][1] - dif))
    # calendario sintetico (dias habiles de lunes a viernes), senal sin registrar
    from datetime import timedelta
    fechas, f = [], date(2001, 1, 1)
    while len(fechas) < 700:
        if f.weekday() < 5:
            fechas.append(f)
        f += timedelta(days=1)
    pos = posiciones(fechas)
    for fe, (a, b) in pos.items():
        if a < 1 or b > -1:
            raise AssertionError("posiciones invalidas")
    activo = [(fe, rnd.gauss(0.0004, 0.01)) for fe in fechas]
    ext = extras_calendario(fechas, pos)
    for nombre, (a, b) in list(VENTANAS_TOM.items()) + [("resto", (-1, 3))]:
        sen = senal_tom(a, b, nombre, invertir=(nombre == "resto"))
        if bt.buscar_capturas(sen, len(fechas)):
            raise AssertionError("la senal de calendario captura series")
        res = bt.backtest_senal(activo, 0.0001, sen, id_replica=None, variante="prueba", min_historia=20,
                                extras=ext)
        for fe, w in zip(res.fechas, res.exposicion):
            esperado = en_ventana(pos[fe][0], pos[fe][1], a, b)
            if nombre == "resto":
                esperado = not esperado
            if w != (1.0 if esperado else 0.0):
                raise AssertionError(f"exposicion incorrecta en {fe} ({nombre})")
        for c, rot in zip(res.costo, res.rotacion):
            if abs(rot) > 1e-12 and abs(rot - 1.0) > 1e-12:
                raise AssertionError(f"rotacion inesperada {rot}")
            peor = max(peor, abs(c - rot * COSTO_LADO))
    # unidades mensuales: 4 dias de TOM
    s = construir_serie(fechas[1:], [v for _, v in activo[1:]], [0.0001] * (len(fechas) - 1), pos)
    for u in unidades_mensuales(s):
        if len(u["tom"]) != 4:
            raise AssertionError("unidad con TOM distinto de 4 dias")
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
    """Metricas del tramo (f0, f1] de una corrida ya hecha + t NW(10) del exceso neto diario
    + costo por lado de equilibrio (exceso bruto acumulado / rotacion acumulada)."""
    idx = [i for i, f in enumerate(res.fechas) if f0 < f <= f1]
    if len(idx) < 60:
        return None
    i0, i1 = idx[0], idx[-1] + 1
    fecha_ini = res.curva[i0][0]
    cambios = sum(1 for j in range(i0, i1) if res.exposicion[j] != (res.exposicion[j - 1] if j > 0 else 0.0))
    x = bt.metricas_de_periodos(res.fechas[i0:i1], fecha_ini, res.r_neto[i0:i1], res.r_efectivo[i0:i1],
                                res.exposicion[i0:i1], res.rotacion[i0:i1], res.costo[i0:i1],
                                res.r_activo[i0:i1], res.parametros["periodos_por_anio"], cambios)
    exceso = [a - b for a, b in zip(res.r_neto[i0:i1], res.r_efectivo[i0:i1])]
    exceso_bruto = [a - b for a, b in zip(res.r_bruto[i0:i1], res.r_efectivo[i0:i1])]
    anios = (res.fechas[i1 - 1] - fecha_ini).days / 365.25
    x["operaciones_por_anio"] = sum(1 for r in res.rotacion[i0:i1] if r > 1e-12) / anios if anios > 0 else None
    rot = math.fsum(res.rotacion[i0:i1])
    x["costo_equilibrio_lado"] = math.fsum(exceso_bruto) / rot if rot > 1e-12 else None
    x["exceso_bruto_anual"] = math.fsum(exceso_bruto) / anios if anios > 0 else None
    if statistics.pstdev(exceso) == 0:
        x.update({"nw_t": None})
        return x
    nw = est.newey_west(exceso, NW_REZAGOS)
    x.update({"nw_t": nw["t"]})
    return x


def limites(res, segmento: str) -> tuple:
    xx = res.metricas[segmento]
    return xx["fecha_inicio"], xx["fecha_fin"]


CLAVES_TABLA = ("cagr", "vol_anual", "sharpe", "nw_t", "sortino", "mdd", "exposicion_media",
                "operaciones_por_anio", "costo_anual", "exceso_bruto_anual", "costo_equilibrio_lado")


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
    filas = ["| variante | ventana | n | cagr | vol_anual | sharpe | nw_t | mdd | exposicion_media | costo_equilibrio_lado |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in resultados:
        for nombre, f0, f1 in ventanas:
            x = ventana(r, f0, f1)
            if x is None:
                continue
            filas.append(f"| {r.variante} | {nombre} ({x['fecha_inicio']} a {x['fecha_fin']}) | {x['n_periodos']} | "
                         f"{fmt(x['cagr'])} | {fmt(x['vol_anual'])} | {fmt(x['sharpe'])} | {fmt(x['nw_t'], 2)} | "
                         f"{fmt(x['mdd'])} | {fmt(x['exposicion_media'])} | {fmt(x['costo_equilibrio_lado'])} |")
    return "\n".join(filas)


def reportar_efecto(nombre_serie: str, res: dict) -> None:
    print(f"\n### Efecto en {nombre_serie}: regresion diaria y = mu + delta*TOM (y en % simple diario)\n")
    print("| ventana | desde | hasta | n | n TOM | mu (resto) | delta | t MCO | t HC1 | t NW10 | p NW | media TOM |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for nombre, x in res.items():
        if x is None:
            continue
        r = x["m1"]
        print(f"| {nombre} | {x['desde']} | {x['hasta']} | {x['n']} | {x['n_tom']} | {fmt(r['coef'][0])} | "
              f"{fmt(r['coef'][1])} | {fmt(r['t_ols'][1], 2)} | {fmt(r['t_hc1'][1], 2)} | {fmt(r['t_nw'][1], 2)} | "
              f"{fmt(r['p_nw'][1])} | {fmt(x['media_tom'])} |")
    print(f"\n### Efecto en {nombre_serie}: comparacion estrecha de McConnell-Xu (TOM contra -10..-2 y +4..+10)\n")
    print("| ventana | d-1 | d+1 | d+2 | d+3 | TOM (t) | otros (t) | dif | t MCO | t Welch | t NW10 | % pos TOM | % pos otros |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for nombre, x in res.items():
        if x is None or "mx" not in x:
            continue
        m = x["mx"]
        pd = m["por_dia"]
        print(f"| {nombre} | " + " | ".join(f"{fmt(pd[k]['media'])} (t {fmt(pd[k]['t'], 2)})" for k in ("d-1", "d+1", "d+2", "d+3"))
              + f" | {fmt(m['tom'])} ({fmt(m['t_tom'], 2)}) | {fmt(m['otros'])} ({fmt(m['t_otros'], 2)}) | "
              f"{fmt(m['reg']['coef'][1])} | {fmt(m['reg']['t_ols'][1], 2)} | {fmt(m['t_welch'], 2)} | "
              f"{fmt(m['reg']['t_nw'][1], 2)} | {fmt(m['pct_pos_tom'], 3)} | {fmt(m['pct_pos_otros'], 3)} |")
    print(f"\n### Efecto en {nombre_serie}: exceso sobre la RF, estrecha de McConnell-Xu (como su tabla 2)\n")
    print("| ventana | exceso TOM | t | exceso otros | t |")
    print("|---|---|---|---|---|")
    for nombre, x in res.items():
        if x is None or "mx" not in x:
            continue
        m = x["mx"]
        print(f"| {nombre} | {fmt(m['ex_tom'])} | {fmt(m['t_ex_tom'], 2)} | {fmt(m['ex_otros'])} | {fmt(m['t_ex_otros'], 2)} |")
    print(f"\n### Efecto en {nombre_serie}: pruebas robustas (delta y t NW10)\n")
    print("| ventana | delta winsor 0.5/99.5 | t NW | delta sin dic-ene | t NW | delta sin cierres | t NW | meses con hueco |")
    print("|---|---|---|---|---|---|---|---|")
    for nombre, x in res.items():
        if x is None or "winsor" not in x:
            continue
        w, dj, sc = x["winsor"], x["sin_dic_ene"], x["sin_cierres"]
        print(f"| {nombre} | {fmt(w['coef'][1])} | {fmt(w['t_nw'][1], 2)} | {fmt(dj['coef'][1])} | {fmt(dj['t_nw'][1], 2)} | "
              f"{fmt(sc['coef'][1])} | {fmt(sc['t_nw'][1], 2)} | {', '.join(str(f) for f in x['meses_con_hueco']) or '-'} |")
    print(f"\n### Efecto en {nombre_serie}: diferencia mensual pareada D_m (media diaria TOM - media diaria resto, pp)\n")
    print("| ventana | N | media D | mediana D | t iid | IC95 bootstrap | D>0 | p signo (1 cola) |")
    print("|---|---|---|---|---|---|---|---|")
    for nombre, x in res.items():
        if x is None or "D" not in x or x["D"].get("n", 0) < 5:
            continue
        p = x["D"]
        print(f"| {nombre} | {p['n']} | {fmt(p['media'])} | {fmt(p['mediana'])} | {fmt(p['t_iid'], 2)} | "
              f"[{fmt(p['ic95_bootstrap'][0])}, {fmt(p['ic95_bootstrap'][1])}] | {p['positivos']}/{p['n']} "
              f"({fmt(p['pct_positivos'], 3)}) | {fmt(p['p_signo_una_cola'])} |")
    print(f"\n### Efecto en {nombre_serie}: estilo L&S (rendimiento acumulado medio, %) y exceso por evento E\n")
    print("| ventana | meses | TOM 4 dias | mes completo | resto del mes | TOM/mes | E medio | t iid E | IC95 E | E>0 | E > 0.34 | E > 0.68 |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for nombre, x in res.items():
        if x is None or "ls" not in x or x["E"].get("n", 0) < 5:
            continue
        ls, e = x["ls"], x["E"]
        print(f"| {nombre} | {ls['n']} | {fmt(ls['tom_4d'])} | {fmt(ls['mes'])} | {fmt(ls['resto'])} | "
              f"{fmt(ls['razon_tom_mes'], 2)} | {fmt(e['media'])} | {fmt(e['t_iid'], 2)} | "
              f"[{fmt(e['ic95_bootstrap'][0])}, {fmt(e['ic95_bootstrap'][1])}] | {fmt(e['pct_positivos'], 3)} | "
              f"{fmt(x['E_sobre_1lado'], 3)} | {fmt(x['E_sobre_2lados'], 3)} |")
    print(f"\n### Efecto en {nombre_serie}: dia relativo (tau) y placebo de ventanas de 4 dias\n")
    for nombre, x in res.items():
        if x is None or "tau" not in x or not nombre.startswith(("completo", "dentro", "fuera_muestra")):
            continue
        tt = " ; ".join(f"{k:+d}: {fmt(m, 3)} (t {fmt(t, 1)})" for k, (m, t, _) in x["tau"].items())
        pl = " ; ".join(f"[{k:+d},{k + 3:+d}]: {fmt(m, 4)}" for k, m in x["placebo"])
        print(f"- {nombre}: TOM (tau -1..+2) queda en el lugar {x['placebo_lugar_tom']} de 16 ventanas.")
        print(f"  - medias por tau: {tt}")
        print(f"  - ventanas de 4 dias: {pl}")


def resumen_efecto(x: dict | None) -> dict | None:
    if x is None:
        return None
    r = x["m1"]
    salida = {"desde": x["desde"], "hasta": x["hasta"], "n": x["n"], "mu_resto": r["coef"][0], "delta": r["coef"][1],
              "t_ols": r["t_ols"][1], "t_hc1": r["t_hc1"][1], "t_nw10": r["t_nw"][1], "p_nw10": r["p_nw"][1],
              "media_tom": x["media_tom"]}
    if "mx" in x:
        m = x["mx"]
        salida.update({"mx_tom": m["tom"], "mx_otros": m["otros"], "mx_dif": m["reg"]["coef"][1],
                       "mx_t_ols": m["reg"]["t_ols"][1], "mx_t_welch": m["t_welch"], "mx_t_nw10": m["reg"]["t_nw"][1],
                       "mx_ex_tom": m["ex_tom"], "mx_ex_otros": m["ex_otros"], "mx_t_ex_otros": m["t_ex_otros"],
                       "delta_winsor": x["winsor"]["coef"][1], "t_nw_winsor": x["winsor"]["t_nw"][1],
                       "delta_sin_dic_ene": x["sin_dic_ene"]["coef"][1], "t_nw_sin_dic_ene": x["sin_dic_ene"]["t_nw"][1],
                       "delta_sin_cierres": x["sin_cierres"]["coef"][1], "t_nw_sin_cierres": x["sin_cierres"]["t_nw"][1],
                       "D": x["D"], "E": x["E"], "ls": x["ls"], "placebo_lugar_tom": x["placebo_lugar_tom"]})
    return salida


# ================================================================ principal

def main() -> dict:
    print("R09 - efecto de cambio de mes / turn of the month (Lakonishok y Smidt 1988; McConnell y Xu 2008)")
    print(f"Comprobaciones sin red (regresion vs estadistica.newey_west, posiciones, senal de calendario, costos): "
          f"diferencia maxima = {prueba_herramientas():.3e}")

    # ------------------------------------------------ datos
    ff = dh.french("F-F_Research_Data_Factors_daily", "diaria")
    mercado = dh.rendimiento_mercado_french(ff)
    rf_us = dh.columna(ff, "RF")
    fechas_us = [f for f, _ in mercado]
    if fechas_us != [f for f, _ in rf_us]:
        raise ValueError("French: fechas de Mkt y RF distintas")
    fuente_us = f"French F-F_Research_Data_Factors_daily CRSP {ff['version_crsp']} sha256 {ff['sha256'][:16]}"
    g = dh.yahoo_historia("^GSPC", "1d")
    precios = [(f, p) for f, p in zip(g["fechas"], g["precios"]) if f <= FIN_SPX_EFECTO]
    fechas_px = [f for f, _ in precios]
    spx = dh.rendimientos_de_precios(fechas_px, [p for _, p in precios])
    rf_spx, sin_french = rf_en_fechas([f for f, _ in spx], rf_us, fechas_px[0])
    fx = dh.fred("DEXMXUS")
    cetes_fred = dh.fred("INTGSTMXM193N")
    cetes_d, rellenos = cetes_diario(fechas_us, cetes_fred)
    print("\n## Datos\n")
    print(f"- French diario: {ff['fechas'][0]} a {ff['fechas'][-1]} (n={len(ff['fechas'])}), CRSP {ff['version_crsp']}, "
          f"faltantes={ff['faltantes']}, sha256={ff['sha256']}")
    print(f"- ^GSPC 1d: barras {g['fechas'][0]} a {g['fechas'][-1]} (n={len(g['fechas'])}), moneda={g['moneda']}, "
          f"adjclose={g['usa_adjclose']}, adjclose!=close={g['adjclose_difiere_de_close']}, descartes={g['descartes']}, "
          f"sin_precio={g['fechas_sin_precio']}; usadas hasta {fechas_px[-1]}; rendimientos {spx[0][0]} a {spx[-1][0]} (n={len(spx)})")
    print(f"- RF asignada a ^GSPC: {sin_french} fechas de ^GSPC sin ninguna fecha French en (d-1, d] "
          f"(RF = 0; son las posteriores al {fechas_us[-1]}, solo entran en las pruebas del efecto)")
    print(f"- FRED DEXMXUS: {fx[0][0]} a {fx[-1][0]} (n={len(fx)})")
    print(f"- FRED INTGSTMXM193N: {cetes_fred[0][0]} a {cetes_fred[-1][0]} (n={len(cetes_fred)}); CETES diario "
          f"{cetes_d[0][0]} a {cetes_d[-1][0]} (n={len(cetes_d)}); meses rellenados: {len(rellenos)} {rellenos[:10]}")

    pos_us = posiciones(fechas_us)
    pos_px = posiciones(fechas_px)
    s_us = construir_serie(fechas_us, [r for _, r in mercado], [r for _, r in rf_us], pos_us)
    s_px = construir_serie([f for f, _ in spx], [r for _, r in spx], [r for _, r in rf_spx], pos_px)
    u_us = unidades_mensuales(s_us)
    u_px = unidades_mensuales(s_px)
    # calendario: dias -1 de French contra ^GSPC en el rango comun
    fin_comun = min(fechas_us[-1], fechas_px[-1])
    m1_us = {f for f, (a, b) in pos_us.items() if b == -1 and date(1928, 1, 1) <= f <= fin_comun}
    m1_px = {f for f, (a, b) in pos_px.items() if b == -1 and date(1928, 1, 1) <= f <= fin_comun}
    dif_m1 = sorted(m1_us ^ m1_px)
    print(f"- Dias -1 (1928-01 a {fin_comun}): French {len(m1_us)}, ^GSPC {len(m1_px)}; meses con dia -1 distinto: "
          f"{len({(f.year, f.month) for f in dif_m1})} (ultimo: {dif_m1[-1] if dif_m1 else '-'})")
    print(f"- Unidades mensuales completas: French {len(u_us)} ({u_us[0]['fecha']} a {u_us[-1]['fecha']}); "
          f"^GSPC {len(u_px)} ({u_px[0]['fecha']} a {u_px[-1]['fecha']})")
    print(f"- Meses con hueco > {HUECO_DIAS} dias naturales entre el dia -2 y el +1: French "
          f"{[u['fecha'] for u in u_us if u['hueco']]}; ^GSPC {[u['fecha'] for u in u_px if u['hueco']]}")
    tom_por_mes = {}
    for f, t in zip(s_us["fechas"], s_us["tom"]):
        if t:
            tom_por_mes[(f.year, f.month)] = tom_por_mes.get((f.year, f.month), 0) + 1
    print(f"- Dias TOM por mes calendario en French (3 del inicio + 1 del fin = 4): distribucion "
          f"{sorted(collections.Counter(tom_por_mes.values()).items())}")

    # ------------------------------------------------ pruebas del efecto
    efecto = {"US": {}, "SPX": {}}
    for nombre, f0, f1 in _ventanas(date(1926, 7, 1)):
        efecto["US"][nombre] = pruebas_efecto(s_us, u_us, f0, f1)
    for nombre, f0, f1 in _ventanas(date(1928, 1, 1)):
        nombre_px = nombre.replace("1926", "1928")
        efecto["SPX"][nombre_px] = pruebas_efecto(s_px, u_px, f0, f1)
    # fraccion de eventos con E mayor al costo de 1 y 2 lados
    for serie, s, U in (("US", s_us, u_us), ("SPX", s_px, u_px)):
        ventanas = _ventanas(date(1926, 7, 1) if serie == "US" else date(1928, 1, 1))
        for (nombre, f0, f1), clave in zip(ventanas, list(efecto[serie])):
            x = efecto[serie][clave]
            if x is None:
                continue
            Es = []
            for u in U:
                if f0 <= u["fecha"] <= f1:
                    ct = math.prod(1 + s["r"][i] for i in u["tom"])
                    cf = math.prod(1 + s["rf"][i] for i in u["tom"])
                    Es.append(100.0 * (ct - cf))
            x["E_sobre_1lado"] = sum(1 for v in Es if v > 100 * COSTO_LADO) / len(Es) if Es else None
            x["E_sobre_2lados"] = sum(1 for v in Es if v > 200 * COSTO_LADO) / len(Es) if Es else None
    decadas = {}
    for dec in range(1920, 2030, 10):
        decadas[f"{dec}s"] = pruebas_efecto(s_us, u_us, date(dec, 1, 1), date(dec + 9, 12, 31), completo=False)

    print("\n## Pruebas del efecto (pre-registro, seccion 8, pruebas 1-10)")
    reportar_efecto("EUA, French Mkt (USD, con dividendos)", efecto["US"])
    reportar_efecto("^GSPC (USD, precio sin dividendos)", efecto["SPX"])
    print("\n### French por decada (diagnostico): delta y t NW10\n")
    print("| decada | desde | hasta | n | delta | t NW10 | media TOM | media resto |")
    print("|---|---|---|---|---|---|---|---|")
    for nombre, x in decadas.items():
        if x is None:
            continue
        print(f"| {nombre} | {x['desde']} | {x['hasta']} | {x['n']} | {fmt(x['m1']['coef'][1])} | "
              f"{fmt(x['m1']['t_nw'][1], 2)} | {fmt(x['media_tom'])} | {fmt(x['media_resto'])} |")

    print("\n### Comparacion con McConnell-Xu (version de 2006), tabla 1 VW bruto: French contra el articulo\n")
    print("| panel | concepto | articulo | replica French | diferencia | t articulo | t replica (MCO) |")
    print("|---|---|---|---|---|---|---|")
    mapa_panel = {"A": "MX panel A 1926-1986", "B": "MX panel B 1987-2005", "C": "MX panel C 1926-2005"}
    for p, clave in mapa_panel.items():
        m = efecto["US"][clave]["mx"]
        a = MX_T1[p]
        for concepto, rep, t_rep, art, t_art in (
                ("d-1", m["por_dia"]["d-1"]["media"], m["por_dia"]["d-1"]["t"], a["d-1"], None),
                ("d+1", m["por_dia"]["d+1"]["media"], m["por_dia"]["d+1"]["t"], a["d+1"], None),
                ("d+2", m["por_dia"]["d+2"]["media"], m["por_dia"]["d+2"]["t"], a["d+2"], None),
                ("d+3", m["por_dia"]["d+3"]["media"], m["por_dia"]["d+3"]["t"], a["d+3"], None),
                ("TOM [-1,+3]", m["tom"], m["t_tom"], a["tom"], a["t_tom"]),
                ("otros dias", m["otros"], m["t_otros"], a["otros"], a["t_otros"]),
                ("diferencia", m["reg"]["coef"][1], m["reg"]["t_ols"][1], a["dif"], a["t_dif"])):
            print(f"| {p} | {concepto} | {art} | {fmt(rep)} | {fmt(rep - art)} | {t_art if t_art is not None else 'NA'} | "
                  f"{fmt(t_rep, 2)} |")
    mc = efecto["US"]["MX panel C 1926-2005"]["mx"]
    print(f"| C (tabla 2, exceso) | TOM | {MX_T2_C['tom']} | {fmt(mc['ex_tom'])} | {fmt(mc['ex_tom'] - MX_T2_C['tom'])} | "
          f"{MX_T2_C['t_tom']} | {fmt(mc['t_ex_tom'], 2)} |")
    print(f"| C (tabla 2, exceso) | otros dias | {MX_T2_C['otros']} | {fmt(mc['ex_otros'])} | "
          f"{fmt(mc['ex_otros'] - MX_T2_C['otros'])} | {MX_T2_C['t_otros']} | {fmt(mc['t_ex_otros'], 2)} |")
    print("\n### Comparacion con L&S (DJIA precio 1897-1986: TOM 4 dias 0.473%, mes 0.349%)\n")
    for serie, clave in (("French (rendimiento total)", efecto["US"]["MX panel A 1926-1986"]),
                         ("^GSPC (precio)", efecto["SPX"]["MX panel A 1928-1986"])):
        ls = clave["ls"]
        print(f"- {serie}, {clave['desde']} a {clave['hasta']} ({ls['n']} meses): TOM 4 dias {fmt(ls['tom_4d'])}%, "
              f"mes completo {fmt(ls['mes'])}%, resto del mes {fmt(ls['resto'])}%, razon TOM/mes {fmt(ls['razon_tom_mes'], 2)}")

    # ------------------------------------------------ estrategias
    resultados: dict = {}
    fechas_spx_bt = [f for f, _ in spx if f <= fechas_us[-1]]
    spx_bt = [(f, r) for f, r in spx if f <= fechas_us[-1]]
    rf_spx_bt = [(f, r) for f, r in rf_spx if f <= fechas_us[-1]]
    ext_us = extras_calendario(fechas_us, pos_us)
    ext_px = extras_calendario(fechas_spx_bt, pos_px)
    ext_mxn = extras_calendario([f for f, _ in cetes_d], pos_us)
    fuente_px = (f"Yahoo ^GSPC 1d (precio, sin dividendos) {spx_bt[0][0]} a {spx_bt[-1][0]}; RF French diaria "
                 f"compuesta en (d-1, d]; {fuente_us}")
    fuente_mxn = f"{fuente_us}; FRED DEXMXUS; CETES FRED INTGSTMXM193N diario aproximado (tasa/360)"

    def correr(familia: str, nombre: str, senal, escenario: str, es_ref: bool, params: dict, activo, efectivo,
               fuente: str, moneda: str, extras: dict, fx_=None, efectivo_en_mxn=False, nota_extra: str = ""):
        com, spr, es_sens, nota = ESCENARIOS[escenario]
        es_prueba = (not es_ref) and (not es_sens) and familia in ("US", "SPX")
        notas = [n for n in (("referencia" if es_ref else ""), nota, nota_extra) if n]
        r = bt.backtest_senal(activo, efectivo, senal, id_replica=ID, variante=nombre, comision_por_lado=com,
                              spread_por_lado=spr, min_historia=MIN_HISTORIA, cortes=[CORTE], fx=fx_,
                              efectivo_en_mxn=efectivo_en_mxn, moneda=None if fx_ else moneda,
                              periodos_por_anio=252, extras=extras,
                              parametros={**params, "familia": familia, "escenario_costos": escenario},
                              fuente_datos=fuente, es_prueba=es_prueba, nota="; ".join(notas))
        resultados[(nombre, escenario)] = r
        return r

    def definiciones(prefijo: str) -> list:
        defs = []
        for k, (a, b) in VENTANAS_TOM.items():
            defs.append((f"{prefijo}_tom_{k}", lambda a=a, b=b, k=k: senal_tom(a, b, k), False,
                         {"tipo": "calendario", "ventana": [a, b]}))
        defs += [
            (f"{prefijo}_ref_comprar_mantener", lambda: bt.senal_comprar_y_mantener, True, {"tipo": "referencia"}),
            (f"{prefijo}_ref_efectivo", lambda: bt.senal_efectivo, True, {"tipo": "referencia"}),
            (f"{prefijo}_ref_sma200", lambda: bt.senal_media_movil(200), True, {"tipo": "referencia", "ventana": 200}),
            (f"{prefijo}_ref_resto", lambda: senal_tom(-1, 3, "resto", invertir=True), True,
             {"tipo": "referencia", "ventana": "complemento de [-1, 3]"}),
        ]
        return defs

    familias = {
        "US": (definiciones("US"), mercado, rf_us, fuente_us, "USD", ext_us),
        "SPX": (definiciones("SPX"), spx_bt, rf_spx_bt, fuente_px, "USD", ext_px),
    }
    for escenario in ("defecto", "medio", "bruto"):
        for familia, (defs, activo, efectivo, fuente, moneda, ext) in familias.items():
            for nombre, fab, es_ref, params in defs:
                correr(familia, nombre, fab(), escenario, es_ref, params, activo, efectivo, fuente, moneda, ext)
    sens = [("USMXN_tom_m1_p3", lambda: senal_tom(-1, 3, "m1_p3"), False, {"tipo": "calendario", "ventana": [-1, 3]}),
            ("USMXN_ref_comprar_mantener", lambda: bt.senal_comprar_y_mantener, True, {"tipo": "referencia"}),
            ("USMXN_ref_efectivo", lambda: bt.senal_efectivo, True, {"tipo": "referencia"}),
            ("USMXN_ref_sma200", lambda: bt.senal_media_movil(200), True, {"tipo": "referencia", "ventana": 200})]
    for nombre, fab, es_ref, params in sens:
        correr("USMXN", nombre, fab(), "defecto", es_ref, {**params, "moneda": "MXN"}, mercado, cetes_d, fuente_mxn,
               "MXN", ext_mxn, fx_=fx, efectivo_en_mxn=True,
               nota_extra="sensibilidad: MXN (activo French convertido con DEXMXUS; efectivo CETES diario)")

    # la exposicion de toda variante de calendario coincide con su definicion
    for (nombre, esc), r in resultados.items():
        pos = pos_px if nombre.startswith("SPX") else pos_us
        ventana_ab = None
        for k, ab in VENTANAS_TOM.items():
            if nombre.endswith("_tom_" + k):
                ventana_ab = ab
        invertir = nombre.endswith("_ref_resto")
        if invertir:
            ventana_ab = (-1, 3)
        if ventana_ab is None:
            continue
        for f, w in zip(r.fechas, r.exposicion):
            dentro = en_ventana(pos[f][0], pos[f][1], *ventana_ab)
            if invertir:
                dentro = not dentro
            if w != (1.0 if dentro else 0.0):
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
    nombres_mxn = [n for n, *_ in sens]
    for seg in ("completo", "dentro_muestra", "fuera_muestra"):
        f0, f1 = limites(R(nombres_mxn[0]), seg)
        print(f"\n### USMXN (sensibilidad, MXN) - costos defecto - segmento {seg} ({f0} a {f1})\n")
        print(tabla([R(n) for n in nombres_mxn], seg))

    ventanas_bt = [("MX panel A", date(1926, 6, 30), date(1986, 12, 31)),
                   ("MX panel B", date(1986, 12, 31), date(2005, 12, 31)),
                   ("hueco", date(2005, 12, 31), CORTE), ("fuera de muestra", CORTE, FIN),
                   ("fuera mitad 1", CORTE, date(2016, 12, 31)), ("fuera mitad 2", date(2016, 12, 31), FIN)]
    for familia in ("US", "SPX"):
        print(f"\n### {familia}: ventanas pre-registradas, costos por defecto\n")
        print(tabla_ventanas([R(f"{familia}_{n}") for n in ("tom_m1_p3", "ref_comprar_mantener", "ref_sma200",
                                                            "ref_resto")], ventanas_bt))

    # ------------------------------------------------ DSR
    print("\n## Sharpe deflactado (registro R09)\n")
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
                f"N={x['n_pruebas']} V_periodo={x['varianza_sharpes_periodo']:.3e} SR_anual={x['sr_anual']:.4f} "
                f"SR0_anual={x['sr0_anual']:.4f} n_obs={x['n_obs']} asim={x['asimetria']:.3f} "
                f"curt={x['curtosis']:.3f} PSR={x['psr_sin_deflactar']:.4f}")

    print(f"- Por defecto (mejor de las {n_prueba}, dentro_muestra, V de todas): {dsr('defecto')}")
    for seg in ("dentro_muestra", "fuera_muestra"):
        print(f"- Mejor de las {n_prueba} [{seg}], V de todas: {dsr(f'todas_{seg}_mejor', segmento=seg)}")
        for familia in ("US", "SPX"):
            cand = [(f["sharpe_periodo"], v) for (v, p, s), f in pruebas.items()
                    if s == seg and v.startswith(familia + "_") and f["sharpe_periodo"] is not None]
            v_fam = statistics.variance([c[0] for c in cand])
            mejor = max(cand)[1]
            print(f"- Familia {familia} [{seg}] mejor de la familia, V de la familia ({len(cand)} Sharpes), N={n_prueba}: "
                  f"{dsr(f'{familia}_{seg}_mejor_Vfam', segmento=seg, variante=mejor, varianza_sharpes=v_fam, n_pruebas=n_prueba)}")
            print(f"- Familia {familia} [{seg}] regla del articulo, V de la familia, N={n_prueba}: "
                  f"{dsr(f'{familia}_{seg}_articulo_Vfam', segmento=seg, variante=f'{familia}_tom_m1_p3', varianza_sharpes=v_fam, n_pruebas=n_prueba)}")
            print(f"- Familia {familia} [{seg}] regla del articulo, V de todas, N={n_prueba}: "
                  f"{dsr(f'{familia}_{seg}_articulo_Vtodas', segmento=seg, variante=f'{familia}_tom_m1_p3')}")

    # ------------------------------------------------ criterios pre-registrados
    print("\n## Criterios pre-registrados (seccion 2)\n")
    us_c = efecto["US"]["MX panel C 1926-2005"]
    us_in = efecto["US"]["dentro_muestra hasta 2008-02"]
    us_oos = efecto["US"]["fuera_muestra 2008-03 al final"]
    px_oos = efecto["SPX"]["fuera_muestra 2008-03 al final"]
    d_mx = us_c["mx"]["reg"]["coef"][1]
    c_i = d_mx > 0 and abs(d_mx - MX_T1["C"]["dif"]) <= TOLERANCIA_PP and us_c["mx"]["reg"]["t_ols"][1] >= 1.96
    c_ii = us_in["m1"]["coef"][1] > 0 and us_in["m1"]["t_nw"][1] >= 2
    c_iii = us_oos["m1"]["coef"][1] > 0
    c_iv = px_oos["m1"]["coef"][1] > 0
    print(f"- (i) French 1926-07..2005-12: delta_MX={d_mx:.4f} (articulo {MX_T1['C']['dif']}; |dif|="
          f"{abs(d_mx - MX_T1['C']['dif']):.4f} <= {TOLERANCIA_PP}?), t MCO={us_c['mx']['reg']['t_ols'][1]:.2f} -> {c_i}")
    print(f"- (ii) French dentro de muestra: delta={us_in['m1']['coef'][1]:.4f}, t NW10={us_in['m1']['t_nw'][1]:.2f} -> {c_ii}")
    print(f"- (iii) French fuera de muestra: delta={us_oos['m1']['coef'][1]:.4f} -> {c_iii}")
    print(f"- (iv) ^GSPC fuera de muestra: delta={px_oos['m1']['coef'][1]:.4f} -> {c_iv}")
    if d_mx <= 0 or (not c_iii and not c_iv):
        estado = "No replicado"
    elif c_i and c_ii and c_iii and c_iv:
        estado = "Replicado"
    elif d_mx > 0 and (c_iii or c_iv):
        estado = "Replicado con diferencias"
    else:
        estado = "Pendiente (caso no previsto por la regla)"
    print(f"- Estado segun la regla pre-registrada: {estado}")
    print(f"- H1b: exceso de 'otros dias' 1926-2005 = {mc['ex_otros']:.4f} (t {mc['t_ex_otros']:.2f}) -> "
          f"{'no distinto de cero' if abs(mc['t_ex_otros']) < 1.96 else 'distinto de cero'}")
    ls_px = efecto["SPX"]["MX panel A 1928-1986"]["ls"]
    print(f"- H1c (L&S con ^GSPC 1928-1986): TOM 4 dias {ls_px['tom_4d']:.4f}% contra mes {ls_px['mes']:.4f}% -> "
          f"{'TOM >= mes' if ls_px['tom_4d'] >= ls_px['mes'] else 'TOM < mes'}")

    def significativo(x: dict) -> bool:
        return x["m1"]["t_nw"][1] >= 2 and x["D"]["ic95_bootstrap"][0] > 0

    sig = {}
    for nombre_s, x in (("US", us_oos), ("SPX", px_oos)):
        sig[nombre_s] = significativo(x)
        print(f"- Significativo fuera de muestra {nombre_s} (t NW10 >= 2 y IC95 bootstrap de D excluye 0): {sig[nombre_s]} "
              f"(t NW10={x['m1']['t_nw'][1]:.2f}; IC95 D=[{x['D']['ic95_bootstrap'][0]:.4f}, {x['D']['ic95_bootstrap'][1]:.4f}])")
    s = R("US_tom_m1_p3")
    xs = ventana(s, *limites(s, "fuera_muestra"))
    crit_estr = {}
    for fam in ("US", "SPX"):
        sf = R(f"{fam}_tom_m1_p3")
        xf = ventana(sf, *limites(sf, "fuera_muestra"))
        bh = R(f"{fam}_ref_comprar_mantener").metricas["fuera_muestra"]
        sm = R(f"{fam}_ref_sma200").metricas["fuera_muestra"]
        S1 = xf["sharpe"] > 0 and (xf["nw_t"] or 0) >= 2
        S2 = xf["sharpe"] > bh["sharpe"] and xf["mdd"] > bh["mdd"]
        S3 = xf["sharpe"] > sm["sharpe"] and xf["mdd"] > sm["mdd"]
        crit_estr[fam] = {"S1": S1, "S2": S2, "S3": S3}
        print(f"- {fam}_tom_m1_p3 fuera de muestra, neto defecto: Sharpe {xf['sharpe']:.4f} (t NW10 {fmt(xf['nw_t'], 2)}), "
              f"CAGR {xf['cagr']:.4f}, MDD {xf['mdd']:.4f}; comprar y mantener: Sharpe {bh['sharpe']:.4f}, CAGR {bh['cagr']:.4f}, "
              f"MDD {bh['mdd']:.4f}; SMA200: Sharpe {sm['sharpe']:.4f}, CAGR {sm['cagr']:.4f}, MDD {sm['mdd']:.4f} -> "
              f"S1 (sobrevive a costos)={S1}; S2 (vs comprar y mantener)={S2}; S3 (vs SMA200)={S3}")
    E_us, E_px = us_oos["E"], px_oos["E"]
    E_sig = E_us["media"] > 0 and E_us["t_iid"] >= 2 and E_us["ic95_bootstrap"][0] > 0
    S1, S2 = crit_estr["US"]["S1"], crit_estr["US"]["S2"]
    if E_us["media"] <= 0 and E_px["media"] <= 0:
        decision = "descartar"
    elif S1 and S2:
        decision = "modificar (b): la estrategia sola sobrevive y supera a comprar y mantener"
    elif E_sig:
        decision = "confirmar"
    elif E_us["media"] > 0:
        decision = "modificar (a): E > 0 no significativo; timing solo como desempate sin costo; grado C"
    else:
        decision = "caso no previsto"
    print(f"- E fuera de muestra French: media {E_us['media']:.4f}% (t iid {E_us['t_iid']:.2f}; IC95 "
          f"[{E_us['ic95_bootstrap'][0]:.4f}, {E_us['ic95_bootstrap'][1]:.4f}]); ^GSPC: media {E_px['media']:.4f}% "
          f"(t iid {E_px['t_iid']:.2f}; IC95 [{E_px['ic95_bootstrap'][0]:.4f}, {E_px['ic95_bootstrap'][1]:.4f}])")
    print(f"- Regla TOM de arena/investigacion/03 (renglon TOM y [R] 5) segun el criterio pre-registrado: {decision}")

    # ------------------------------------------------ cuenta de 20,000 MXN
    print(f"\n## Traduccion a una cuenta de {CUENTA_MXN:,} MXN (diagnostico)\n")
    costo_anual_mxn = xs["costo_anual"] * CUENTA_MXN
    print(f"- Costo anual de US_tom_m1_p3 fuera de muestra con costos por defecto: {xs['costo_anual']:.4f} del capital "
          f"= {costo_anual_mxn:,.0f} MXN al anio ({xs['operaciones_por_anio']:.2f} operaciones al anio)")
    print(f"- Costo de un lado: {COSTO_LADO:.4f} x {CUENTA_MXN:,} = {COSTO_LADO * CUENTA_MXN:,.0f} MXN")
    for nombre_s, E in (("French", E_us), ("^GSPC", E_px)):
        print(f"- Prima media por evento fuera de muestra ({nombre_s}): {E['media']:.4f}% x {CUENTA_MXN:,} = "
              f"{E['media'] / 100 * CUENTA_MXN:,.0f} MXN (x12 = {12 * E['media'] / 100 * CUENTA_MXN:,.0f} MXN al anio, "
              f"antes de costos); IC95 [{E['ic95_bootstrap'][0] / 100 * CUENTA_MXN:,.0f}, "
              f"{E['ic95_bootstrap'][1] / 100 * CUENTA_MXN:,.0f}] MXN por evento")
    valores_mxn = {}
    for n in nombres_mxn:
        x = R(n).metricas["fuera_muestra"]
        valores_mxn[n] = CUENTA_MXN * (1 + x["rendimiento_total"])
        print(f"- {n}: {CUENTA_MXN:,} MXN el {x['fecha_inicio']} -> {valores_mxn[n]:,.0f} MXN el {x['fecha_fin']} "
              f"(CAGR {x['cagr']:.4f}, MDD {x['mdd']:.4f})")

    # ------------------------------------------------ salida json
    def met(nombre: str, esc: str = "defecto") -> dict:
        r = R(nombre, esc)
        salida_ = {}
        for sg in ["completo"] + r.segmentos:
            v = ventana(r, *limites(r, sg))
            salida_[sg] = {k: (v or {}).get(k) for k in ("fecha_inicio", "fecha_fin", "n_periodos", "cagr", "vol_anual",
                                                         "sharpe", "nw_t", "mdd", "exposicion_media", "costo_anual",
                                                         "operaciones_por_anio", "costo_equilibrio_lado",
                                                         "rendimiento_total")}
        return salida_

    salida = {
        "id": ID, "corte": CORTE,
        "datos": {"french_version_crsp": ff["version_crsp"], "french_sha256": ff["sha256"],
                  "french_rango": [ff["fechas"][0], ff["fechas"][-1]], "spx_rango": [spx[0][0], spx[-1][0]],
                  "spx_sin_precio": g["fechas_sin_precio"], "dexmxus_rango": [fx[0][0], fx[-1][0]],
                  "cetes_rango": [cetes_fred[0][0], cetes_fred[-1][0]], "cetes_rellenos": rellenos,
                  "meses_dia_m1_distinto": len({(f.year, f.month) for f in dif_m1}),
                  "huella_US": R("US_tom_m1_p3").meta["huella_datos"], "huella_SPX": R("SPX_tom_m1_p3").meta["huella_datos"],
                  "huella_USMXN": R("USMXN_tom_m1_p3").meta["huella_datos"]},
        "efecto": {k: {n: resumen_efecto(v) for n, v in x.items()} for k, x in efecto.items()},
        "decadas": {n: resumen_efecto(v) for n, v in decadas.items()},
        "estrategias_defecto": {n: met(n) for (n, esc) in resultados if esc == "defecto"},
        "estrategias_medio": {n: met(n, "medio") for (n, esc) in resultados if esc == "medio"},
        "estrategias_bruto": {n: met(n, "bruto") for (n, esc) in resultados if esc == "bruto"},
        "dsr": dsr_res,
        "criterios": {"i": c_i, "ii": c_ii, "iii": c_iii, "iv": c_iv, "estado": estado, "significativo_oos": sig,
                      "estrategia": crit_estr, "E_significativo_US": E_sig, "regla_TOM_03": decision},
        "cuenta_20k": {"costo_anual_mxn": costo_anual_mxn, "costo_lado_mxn": COSTO_LADO * CUENTA_MXN,
                       "E_fuera_US_mxn": E_us["media"] / 100 * CUENTA_MXN, "E_fuera_SPX_mxn": E_px["media"] / 100 * CUENTA_MXN,
                       "valores_finales_usmxn": valores_mxn},
    }
    (DIR / "R09-resultados.json").write_text(json.dumps(salida, indent=1, ensure_ascii=False, default=str),
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
        (DIR / "R09-salida.txt").write_text(buffer.getvalue(), encoding="utf-8")
