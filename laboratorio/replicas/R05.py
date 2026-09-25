#!/usr/bin/env python3
"""R05 - Portafolios con volatilidad gestionada (Moreira y Muir, 2017, JF 72(4):1611-1644)
contra la critica de Cederburg, O'Doherty, Wang y Yan (2020, JFE 138(1):95-117).

Reproduce desde la raiz del repo:  python3 laboratorio/replicas/R05.py
Solo biblioteca estandar. Las corridas del motor se agregan a laboratorio/replicas/R05-variantes.csv.
Salida completa en R05-salida.txt; cifras clave en R05-resultados.json.

Pre-registro: R05-portafolio-volatilidad-gestionada.md, secciones 1-9.
  Parte A (estadistica, NO es estrategia): f^s_t = c/RV2_{t-1} * f_t con c de la ventana completa
     (look-ahead a proposito: es la estadistica del articulo). Regresion de expansion
     f^s = a + b f + e con errores HC0, HC1 y NW(12). Variantes A1-A4 (tabla 5 de MM).
  Parte B (Cederburg et al.): combinacion media-varianza en tiempo real (K=120, gamma=5,
     |y|<=5) como senal del motor; se verifica contra un calculo directo independiente.
  Parte C (operable): exposicion min(tope, c_t/RV2_{t-1}) o min(tope, k_t/RV_{t-1}), con c_t en
     tiempo real (ventana expansiva). 7 variantes de prueba + reglas sencillas + sensibilidades.
"""
from __future__ import annotations

import io
import json
import math
import statistics
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from herramientas import backtest as bt  # noqa: E402
from herramientas import datos_historicos as dh  # noqa: E402

# ================================================================ parametros pre-registrados
ID = "R05"
DIR = Path(__file__).resolve().parent
CORTES = [date(2015, 12, 31), date(2017, 7, 31)]
NOMBRES = ["dentro_muestra", "hueco_2016_2017", "fuera_muestra"]
K = 120                     # meses de entrenamiento inicial (Cederburg et al.)
MIN_HISTORIA = K + 1        # 1926-07..1936-07 visibles -> primera decision 1936-08
GAMMA = 5.0
TOPE_COMB = 5.0
NW_REZAGOS = 12
J_MIN = 15
SPREAD_MARGEN_ANUAL = 0.03  # supuesto (sensibilidad fuera del motor)
N_CONSERVADOR = 13
COMISION = bt.COMISION_GBM_POR_LADO
ESCENARIOS = {
    "defecto": (COMISION, bt.SPREAD_POR_LADO["liquido"]),
    "spread_medio": (COMISION, bt.SPREAD_POR_LADO["medio"]),
    "bruto": (0.0, 0.0),
}
VARIANTES = [  # (nombre, forma, tope, clave_rv) - lista cerrada del pre-registro
    ("var_c1", "var", 1.0, "rv2_mm"),
    ("var_c1.5", "var", 1.5, "rv2_mm"),
    ("var_c2", "var", 2.0, "rv2_mm"),
    ("vol_c1", "vol", 1.0, "rv2_mm"),
    ("vol_c1.5", "vol", 1.5, "rv2_mm"),
    ("vol_c2", "vol", 2.0, "rv2_mm"),
    ("var_c1_rvCOWY", "var", 1.0, "rv2_cowy"),
]
NORMAL = statistics.NormalDist()

# Cifras de los articulos (seccion 1 del pre-registro)
MM = {
    "A1_var": {"alfa": 4.86, "se": 1.56, "beta": 0.61, "n": 1065, "r2": 0.37, "rmse": 51.39, "sharpe": 0.52,
               "ar": 0.34, "p50": 0.93, "p75": 1.59, "p90": 2.64, "p99": 6.39},
    "A2_vol": {"alfa": 3.30, "se": 1.02, "sharpe": 0.53, "ar": 0.33, "p50": 1.23, "p75": 1.61, "p90": 2.08,
               "p99": 3.36},
    "A3_var_tope1": {"alfa": 2.12, "se": 0.71, "sharpe": 0.52, "ar": 0.30},
    "A4_var_tope1.5": {"alfa": 3.10, "se": 0.98, "sharpe": 0.53, "ar": 0.33},
    "sharpe_mercado": 0.42,
}
COWY = {"t1": {"sr_f": 0.42, "sr_fs": 0.51, "dif": 0.09, "p": 0.30, "p01": 0.04, "p50": 0.96, "p99": 6.47},
        "t3": {"alfa": 4.63, "t_white": 3.08, "beta": 0.63, "r2": 0.40, "ar": 0.32, "c": 10.33, "sr_comb": 0.53},
        "t5": {"S1": 0.42, "S2": 0.46, "dif": -0.04, "p": 0.64, "cer_S1": 1.56, "cer_S2": 1.75, "S3": 0.53}}


def fm(a: int, m: int) -> date:
    return dh.fin_de_mes(a, m)


FIN = date(2100, 1, 1)
VENTANA_MM = (fm(1926, 8), fm(2015, 12))
VENTANA_COWY = (fm(1926, 8), fm(2016, 12))
VENTANA_COWY_OOS = (fm(1936, 8), fm(2016, 12))
POST_JF = (fm(2017, 8), FIN)
POST_NBER = (fm(2016, 1), FIN)
SUBPERIODOS = [("1926-08 a 1955-12", fm(1926, 8), fm(1955, 12)), ("1956-01 a 1985-12", fm(1956, 1), fm(1985, 12)),
               ("1986-01 a 2015-12", fm(1986, 1), fm(2015, 12)), ("2016-01 al final", fm(2016, 1), FIN),
               ("1926-08 al final", fm(1926, 8), FIN)]
SEG_FECHAS = {"completo": (date(1900, 1, 1), FIN), "dentro_muestra": (date(1900, 1, 1), CORTES[0]),
              "hueco_2016_2017": (fm(2016, 1), CORTES[1]), "fuera_muestra": (fm(2017, 8), FIN)}


# ================================================================ salida (pantalla + archivo)

class Tee(io.TextIOBase):
    def __init__(self, *destinos):
        self.destinos = destinos

    def write(self, s):
        for d in self.destinos:
            d.write(s)
        return len(s)

    def flush(self):
        for d in self.destinos:
            d.flush()


def f4(x, nd=4) -> str:
    if x is None:
        return "NA"
    if isinstance(x, float):
        if math.isnan(x):
            return "nan"
        if math.isinf(x):
            return "inf"
        return f"{x:.{nd}f}"
    return str(x)


# ================================================================ datos

def cargar() -> dict:
    fd = dh.french("F-F_Research_Data_Factors_daily", "diaria")
    fmn = dh.french("F-F_Research_Data_Factors", "mensual")
    if fd["version_crsp"] != fmn["version_crsp"]:
        raise SystemExit(f"Version CRSP distinta: diario {fd['version_crsp']} vs mensual {fmn['version_crsp']}")
    por_mes: dict[date, list[float]] = {}
    for f, v in dh.columna(fd, "Mkt-RF"):
        por_mes.setdefault(fm(f.year, f.month), []).append(v)
    rv2_mm, rv2_cowy, dias = {}, {}, {}
    for mes in sorted(por_mes):
        d = por_mes[mes]
        J = len(d)
        if J < J_MIN:
            raise SystemExit(f"Mes {mes} con {J} dias (< {J_MIN}): se detiene, no se imputa")
        media = sum(d) / J
        a = sum((x - media) ** 2 for x in d)
        b = 22.0 / J * sum(x * x for x in d)
        if a <= 0 or b <= 0:
            raise SystemExit(f"RV2 no positiva en {mes}")
        rv2_mm[mes], rv2_cowy[mes], dias[mes] = a, b, J
    f = dict(dh.columna(fmn, "Mkt-RF"))
    rf = dh.columna(fmn, "RF")
    mercado = dh.rendimiento_mercado_french(fmn)
    fechas = sorted(f)
    if fechas != sorted(rv2_mm):
        faltan = sorted(set(fechas) ^ set(rv2_mm))
        raise SystemExit(f"Meses de rendimientos y de RV no coinciden: {faltan[:6]}")
    for a, b in zip(fechas, fechas[1:]):
        if (b.year * 12 + b.month) - (a.year * 12 + a.month) != 1:
            raise SystemExit(f"Meses no consecutivos: {a} -> {b}")
    previo = {b: a for a, b in zip(fechas, fechas[1:])}
    return {"fd": fd, "fm": fmn, "f": f, "rf": rf, "mercado": mercado, "fechas": fechas, "previo": previo,
            "rv2_mm": rv2_mm, "rv2_cowy": rv2_cowy, "dias": dias,
            "extras": {"rv2_mm": sorted(rv2_mm.items()), "rv2_cowy": sorted(rv2_cowy.items())}}


# ================================================================ estadistica (stdlib)

def ols2(y: list, x: list, rezagos: int = NW_REZAGOS) -> dict:
    """MCO y = a + b x + e con e.e. MCO, HC0 (White), HC1 y Newey-West (Bartlett, n/(n-k))."""
    n, k = len(y), 2
    sx, sxx = sum(x), sum(v * v for v in x)
    det = n * sxx - sx * sx
    inv = [[sxx / det, -sx / det], [-sx / det, n / det]]
    sy, sxy = sum(y), sum(a * b for a, b in zip(x, y))
    a_ = inv[0][0] * sy + inv[0][1] * sxy
    b_ = inv[1][0] * sy + inv[1][1] * sxy
    e = [yi - a_ - b_ * xi for xi, yi in zip(x, y)]
    s2 = sum(v * v for v in e) / (n - k)
    g = [(ei, ei * xi) for ei, xi in zip(e, x)]

    def gamma(j: int) -> list:
        return [[sum(g[t][p] * g[t - j][q] for t in range(j, n)) for q in range(2)] for p in range(2)]

    S0 = gamma(0)
    S = [fila[:] for fila in S0]
    for j in range(1, rezagos + 1):
        w = 1 - j / (rezagos + 1)
        G = gamma(j)
        for p in range(2):
            for q in range(2):
                S[p][q] += w * (G[p][q] + G[q][p])

    def sandwich(M: list) -> list:
        A = [[sum(inv[i][r] * M[r][c] for r in range(2)) for c in range(2)] for i in range(2)]
        return [[sum(A[i][r] * inv[r][c] for r in range(2)) for c in range(2)] for i in range(2)]

    v_hc0 = sandwich(S0)
    v_nw = sandwich(S)
    corr = n / (n - k)
    my = sy / n
    sst = sum((v - my) ** 2 for v in y)

    def se(v: float) -> float:
        return math.sqrt(v) if v > 0 else float("nan")

    salida = {"n": n, "a": a_, "b": b_, "s2": s2,
              "r2": 1 - sum(v * v for v in e) / sst if sst > 0 else float("nan"),
              "se_a_ols": se(s2 * inv[0][0]), "se_b_ols": se(s2 * inv[1][1]),
              "se_a_hc0": se(v_hc0[0][0]), "se_b_hc0": se(v_hc0[1][1]),
              "se_a_hc1": se(corr * v_hc0[0][0]), "se_a_nw": se(corr * v_nw[0][0]),
              "se_b_nw": se(corr * v_nw[1][1])}
    for clave in ("ols", "hc0", "hc1", "nw"):
        s = salida[f"se_a_{clave}"]
        salida[f"t_a_{clave}"] = a_ / s if s and s > 0 else float("nan")
    return salida


def sharpe_anual(x: list) -> float:
    return statistics.fmean(x) / statistics.stdev(x) * math.sqrt(12)


def cer_anual_pct(x: list, gamma: float = GAMMA) -> float:
    return (statistics.fmean(x) - gamma / 2 * statistics.variance(x)) * 12 * 100


def jobson_korkie(a: list, b: list) -> dict:
    """Prueba de igualdad de Sharpe (Jobson-Korkie 1981 con correccion de Memmel 2003), como en
    Cederburg et al. (2020), nota 8. z > 0 si SR(a) > SR(b). p a dos colas."""
    T = len(a)
    if T != len(b) or T < 3:
        raise ValueError("series de distinto largo o muy cortas")
    mi, mj = statistics.fmean(a), statistics.fmean(b)
    si, sj = statistics.stdev(a), statistics.stdev(b)
    sij = statistics.covariance(a, b)
    theta = (2 * si ** 2 * sj ** 2 - 2 * si * sj * sij + 0.5 * mi ** 2 * sj ** 2 + 0.5 * mj ** 2 * si ** 2
             - mi * mj / (si * sj) * sij ** 2) / T
    z = (sj * mi - si * mj) / math.sqrt(theta)
    return {"sr_a": mi / si * math.sqrt(12), "sr_b": mj / sj * math.sqrt(12),
            "dif": (mi / si - mj / sj) * math.sqrt(12), "z": z, "p": 2 * (1 - NORMAL.cdf(abs(z))), "n": T}


def percentiles(x: list) -> dict:
    q = statistics.quantiles(x, n=100, method="inclusive")
    return {"p01": q[0], "p50": q[49], "p75": q[74], "p90": q[89], "p99": q[98]}


# ================================================================ Parte A: estadistica del articulo

def parte_a(D: dict, f0: date, f1: date, forma: str = "var", tope: float | None = None,
            clave: str = "rv2_mm", c_fija: float | None = None, c_ventana: tuple | None = None) -> dict:
    """Regresion de expansion en [f0, f1]. c se elige para igualar sd(f^s) y sd(f) en la ventana
    (o en c_ventana, o se fija con c_fija). Con tope, c es la del caso sin tope (como MM)."""
    def base(g0, g1):
        fechas = [t for t in D["fechas"] if t in D["previo"] and g0 <= t <= g1]
        f = [D["f"][t] for t in fechas]
        rv = [D[clave][D["previo"][t]] for t in fechas]
        s = [1 / r if forma == "var" else 1 / math.sqrt(r) for r in rv]
        return fechas, f, s

    fechas, f, s = base(f0, f1)
    if c_fija is not None:
        c = c_fija
    else:
        _, fc, sc = base(*(c_ventana or (f0, f1)))
        c = statistics.stdev(fc) / statistics.stdev([a * b for a, b in zip(sc, fc)])
    w_sin_tope = [c * v for v in s]
    w = [min(tope, v) for v in w_sin_tope] if tope is not None else w_sin_tope
    fs = [a * b for a, b in zip(w, f)]
    r = ols2(fs, f)
    jk = jobson_korkie(fs, f)
    salida = {"desde": fechas[0], "hasta": fechas[-1], "n": len(f), "forma": forma, "tope": tope, "clave": clave,
              "c": c, "c_pct2": c * 1e4 if forma == "var" else c * 1e2,
              "alfa": r["a"] * 1200, "se_hc0": r["se_a_hc0"] * 1200, "t_hc0": r["t_a_hc0"],
              "t_hc1": r["t_a_hc1"], "t_nw": r["t_a_nw"], "t_ols": r["t_a_ols"],
              "beta": r["b"], "se_beta_hc0": r["se_b_hc0"], "r2": r["r2"],
              "rmse": math.sqrt(r["s2"]) * 1200, "ar": r["a"] / math.sqrt(r["s2"]) * math.sqrt(12),
              "sr_f": sharpe_anual(f), "sr_fs": sharpe_anual(fs), "jk_dif": jk["dif"], "jk_p": jk["p"],
              "media_f": statistics.fmean(f) * 1200, "media_fs": statistics.fmean(fs) * 1200,
              "sd_f": statistics.stdev(f) * math.sqrt(12) * 100, "sd_fs": statistics.stdev(fs) * math.sqrt(12) * 100,
              "corr": statistics.correlation(fs, f), "frac_tope": (sum(1 for v in w_sin_tope if tope is not None
                                                                     and v >= tope) / len(w)),
              "pesos": percentiles(w)}
    return salida


def linea_a(nombre: str, x: dict) -> str:
    p = x["pesos"]
    return (f"| {nombre} | {x['desde']:%Y-%m} a {x['hasta']:%Y-%m} | {x['n']} | {f4(x['alfa'], 2)} "
            f"({f4(x['se_hc0'], 2)}) | {f4(x['t_hc0'], 2)} / {f4(x['t_nw'], 2)} | {f4(x['beta'], 3)} | "
            f"{f4(x['r2'], 3)} | {f4(x['rmse'], 2)} | {f4(x['ar'], 3)} | {f4(x['sr_f'], 3)} | {f4(x['sr_fs'], 3)} | "
            f"{f4(x['jk_dif'], 3)} [{f4(x['jk_p'], 2)}] | {f4(p['p50'], 2)}/{f4(p['p75'], 2)}/{f4(p['p90'], 2)}/"
            f"{f4(p['p99'], 2)} | {f4(x['frac_tope'], 3)} |")


ENCABEZADO_A = ("| Caso | Ventana | N | α %/año (e.e. HC0) | t HC0 / t NW12 | β | R² | rmse | AR | SR mercado | "
                "SR gestionada | ΔSR [p JK] | P50/P75/P90/P99 de w | frac. en tope |\n"
                "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")


# ================================================================ senales (funciones puras de h)

def hacer_senal_gestionada(forma: str, tope: float, clave: str):
    """w_t = min(tope, c_t / RV2_{t-1}) (var) o min(tope, k_t / RV_{t-1}) (vol).
    c_t = sd(f_s) / sd(f_s / x_{s-1}) con todos los s <= t-1 disponibles (ventana expansiva)."""
    def senal(h: bt.Historia) -> float:
        n = len(h)
        F, A, E = h.fechas[0:n], h.activo[0:n], h.efectivo[0:n]
        ex = h.extras[clave]
        rv = dict(ex[0:len(ex)])
        f, g = [], []
        for s in range(1, n):
            r = rv.get(F[s - 1])
            if r is None:
                continue
            x = r if forma == "var" else math.sqrt(r)
            fs = A[s] - E[s]
            f.append(fs)
            g.append(fs / x)
        if len(f) < K:
            raise ValueError(f"entrenamiento de {len(f)} meses (< {K})")
        c = statistics.stdev(f) / statistics.stdev(g)
        r_ult = rv[F[-1]]
        x_ult = r_ult if forma == "var" else math.sqrt(r_ult)
        return min(tope, c / x_ult)

    senal.__qualname__ = senal.__name__ = f"gestionada_{forma}_tope{tope}_{clave}"
    return senal


def hacer_senal_s1(clave: str):
    """Cederburg et al. (2020), ecs. 15-16: y_t = clip(x_s/RV2_{t-1} + x, -5, 5),
    [x_s, x]' = (1/gamma) Sigma^-1 mu de (f_s/RV2_{s-1}, f_s) en s <= t-1 (invariante a c_t)."""
    def senal(h: bt.Historia) -> float:
        n = len(h)
        F, A, E = h.fechas[0:n], h.activo[0:n], h.efectivo[0:n]
        ex = h.extras[clave]
        rv = dict(ex[0:len(ex)])
        f, g = [], []
        for s in range(1, n):
            r = rv.get(F[s - 1])
            if r is None:
                continue
            fs = A[s] - E[s]
            f.append(fs)
            g.append(fs / r)
        if len(f) < K:
            raise ValueError(f"entrenamiento de {len(f)} meses (< {K})")
        mg, mf = statistics.fmean(g), statistics.fmean(f)
        vg, vf, cgf = statistics.variance(g), statistics.variance(f), statistics.covariance(g, f)
        det = vg * vf - cgf * cgf
        x_s = (vf * mg - cgf * mf) / det / GAMMA
        x_o = (vg * mf - cgf * mg) / det / GAMMA
        y = x_s / rv[F[-1]] + x_o
        return max(-TOPE_COMB, min(TOPE_COMB, y))

    senal.__qualname__ = senal.__name__ = f"cederburg_S1_{clave}"
    return senal


def senal_s2(h: bt.Historia) -> float:
    """Original en tiempo real: z_t = clip((1/gamma) mu_f / var_f, -5, 5) con s = 1..t-1."""
    n = len(h)
    A, E = h.activo[0:n], h.efectivo[0:n]
    f = [A[s] - E[s] for s in range(1, n)]
    if len(f) < K:
        raise ValueError("entrenamiento corto")
    z = statistics.fmean(f) / statistics.variance(f) / GAMMA
    return max(-TOPE_COMB, min(TOPE_COMB, z))


# ================================================================ verificacion independiente

def pesos_directos(D: dict, fechas_eval: list, tipo: str, clave: str, forma: str = "var",
                   tope: float | None = None) -> list:
    """Segunda implementacion (sin el motor) de los pesos: indices explicitos de entrenamiento."""
    todas = D["fechas"]
    pos = {t: i for i, t in enumerate(todas)}
    salida = []
    for t in fechas_eval:
        i = pos[t]
        entren = todas[1:i]  # s = 1926-08 .. t-1
        f = [D["f"][s] for s in entren]
        rv_prev = [D[clave][D["previo"][s]] for s in entren]
        r_ult = D[clave][D["previo"][t]]
        if tipo == "gestionada":
            x = [r if forma == "var" else math.sqrt(r) for r in rv_prev]
            c = statistics.stdev(f) / statistics.stdev([a / b for a, b in zip(f, x)])
            x_ult = r_ult if forma == "var" else math.sqrt(r_ult)
            salida.append(min(tope, c / x_ult))
        elif tipo == "S1":
            g = [a / b for a, b in zip(f, rv_prev)]
            mu = [statistics.fmean(g), statistics.fmean(f)]
            vg, vf, c_ = statistics.variance(g), statistics.variance(f), statistics.covariance(g, f)
            det = vg * vf - c_ * c_
            x_s = (vf * mu[0] - c_ * mu[1]) / det / GAMMA
            x_o = (vg * mu[1] - c_ * mu[0]) / det / GAMMA
            salida.append(max(-TOPE_COMB, min(TOPE_COMB, x_s / r_ult + x_o)))
        else:
            salida.append(max(-TOPE_COMB, min(TOPE_COMB, statistics.fmean(f) / statistics.variance(f) / GAMMA)))
    return salida


# ================================================================ utilidades sobre resultados del motor

def indices_ventana(res: bt.ResultadoBacktest, f0: date, f1: date) -> tuple[int, int]:
    idx = [i for i, f in enumerate(res.fechas) if f0 <= f <= f1]
    if not idx:
        raise ValueError(f"ventana vacia {f0}..{f1}")
    return idx[0], idx[-1] + 1


def exceso(res: bt.ResultadoBacktest, f0: date, f1: date, r: list | None = None) -> list:
    i0, i1 = indices_ventana(res, f0, f1)
    rr = r if r is not None else res.r_neto
    return [rr[i] - res.r_efectivo[i] for i in range(i0, i1)]


def exceso_mercado(res: bt.ResultadoBacktest, f0: date, f1: date) -> list:
    i0, i1 = indices_ventana(res, f0, f1)
    return [res.r_activo[i] - res.r_efectivo[i] for i in range(i0, i1)]


def alfa_contra_mercado(res: bt.ResultadoBacktest, f0: date, f1: date) -> dict:
    y, x = exceso(res, f0, f1), exceso_mercado(res, f0, f1)
    if max(y) - min(y) == 0:  # regla de 100% efectivo: exceso identicamente 0
        return {"alfa": float("nan"), "t_hc0": float("nan"), "t_nw": float("nan"), "beta": float("nan"),
                "n": len(y), "ar": float("nan")}
    r = ols2(y, x)
    return {"alfa": r["a"] * 1200, "t_hc0": r["t_a_hc0"], "t_nw": r["t_a_nw"], "beta": r["b"], "n": r["n"],
            "ar": r["a"] / math.sqrt(r["s2"]) * math.sqrt(12) if r["s2"] > 0 else float("nan")}


def metricas_ventana(res: bt.ResultadoBacktest, r: list, f0: date, f1: date) -> dict:
    i0, i1 = indices_ventana(res, f0, f1)
    fi = res.curva[0][0] if i0 == 0 else res.fechas[i0 - 1]
    return bt.metricas_de_periodos(res.fechas[i0:i1], fi, r[i0:i1], res.r_efectivo[i0:i1], res.exposicion[i0:i1],
                                   res.rotacion[i0:i1], res.costo[i0:i1], res.r_activo[i0:i1], 12, 0)


def tabla_motor(resultados: list, segmento: str, bh: bt.ResultadoBacktest) -> str:
    f0, f1 = SEG_FECHAS[segmento]
    lineas = ["| variante | CAGR | vol | Sharpe | Sortino | MDD | Calmar | expos. media | rotación/año | "
              "costo/año | α vs mercado %/año (t HC0; t NW12) | β | ΔSR vs CyM [p JK] |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in resultados:
        x = r.metricas[segmento]
        a = alfa_contra_mercado(r, f0, f1)
        if r is bh or max(r.exposicion) == min(r.exposicion) == 0:
            jk_txt = "—"
        else:
            jk = jobson_korkie(exceso(r, f0, f1), exceso(bh, f0, f1))
            jk_txt = f"{f4(jk['dif'], 3)} [{f4(jk['p'], 2)}]"
        lineas.append(f"| {r.variante} | {f4(x['cagr'])} | {f4(x['vol_anual'])} | {f4(x['sharpe'])} | "
                      f"{f4(x['sortino'])} | {f4(x['mdd'])} | {f4(x['calmar'])} | {f4(x['exposicion_media'])} | "
                      f"{f4(x['rotacion_anual'])} | {f4(x['costo_anual'])} | {f4(a['alfa'], 2)} ({f4(a['t_hc0'], 2)}; "
                      f"{f4(a['t_nw'], 2)}) | {f4(a['beta'], 3)} | {jk_txt} |")
    x = resultados[0].metricas[segmento]
    return f"Segmento {segmento}: {x['fecha_inicio']} (cierre base) a {x['fecha_fin']}, n={x['n_periodos']}\n" \
        + "\n".join(lineas)


# ================================================================ principal

def main() -> dict:
    buf = io.StringIO()
    salida_original = sys.stdout
    sys.stdout = Tee(salida_original, buf)
    res_json: dict = {"id": ID}
    try:
        res_json = correr_todo()
    finally:
        sys.stdout = salida_original
        (DIR / "R05-salida.txt").write_text(buf.getvalue(), encoding="utf-8")
    (DIR / "R05-resultados.json").write_text(json.dumps(res_json, indent=1, ensure_ascii=False, default=str),
                                              encoding="utf-8")
    return res_json


def correr_todo() -> dict:
    R: dict = {"id": ID}
    D = cargar()
    fd, fmn = D["fd"], D["fm"]
    fuente = (f"French F-F_Research_Data_Factors (+_daily) CRSP {fmn['version_crsp']} sha256 "
              f"{fmn['sha256'][:12]}/{fd['sha256'][:12]}")
    print(f"# R05 - salida de laboratorio/replicas/R05.py\n")
    print("## Datos")
    for t in (fd, fmn):
        print(f"- {t['archivo']}: {t['fechas'][0]} a {t['fechas'][-1]} ({len(t['fechas'])} obs), CRSP "
              f"{t['version_crsp']}, sha256 {t['sha256']}, faltantes {t['faltantes']}")
        for nota in t["notas"]:
            print(f"    nota: {nota}")
    dias = list(D["dias"].values())
    print(f"- Meses con RV: {len(D['rv2_mm'])} ({min(D['rv2_mm'])} a {max(D['rv2_mm'])}); dias por mes: "
          f"min {min(dias)}, mediana {statistics.median(dias)}, max {max(dias)}")
    R["datos"] = {"crsp": fmn["version_crsp"], "sha256_mensual": fmn["sha256"], "sha256_diario": fd["sha256"],
                  "mensual": [fmn["fechas"][0], fmn["fechas"][-1], len(fmn["fechas"])],
                  "diario": [fd["fechas"][0], fd["fechas"][-1], len(fd["fechas"])],
                  "dias_min": min(dias), "dias_max": max(dias)}

    # ------------------------------------------------------------ Parte A
    print("\n## Parte A. Réplica estadística de MM (c con la ventana completa; no es estrategia)\n")
    A = {}
    A["A1_var"] = parte_a(D, *VENTANA_MM, "var")
    A["A2_vol"] = parte_a(D, *VENTANA_MM, "vol")
    A["A3_var_tope1"] = parte_a(D, *VENTANA_MM, "var", tope=1.0)
    A["A4_var_tope1.5"] = parte_a(D, *VENTANA_MM, "var", tope=1.5)
    A["A1_var_rvCOWY_MMventana"] = parte_a(D, *VENTANA_MM, "var", clave="rv2_cowy")
    A["A1_var_rvCOWY_1926_2016"] = parte_a(D, *VENTANA_COWY, "var", clave="rv2_cowy")
    A["A1_var_rvMM_1926_2016"] = parte_a(D, *VENTANA_COWY, "var")
    print(ENCABEZADO_A)
    for k, v in A.items():
        print(linea_a(k, v))
    print("\nCifras de MM (tabla 1 y 5, NBER WP 22208) para comparar:")
    for k in ("A1_var", "A2_vol", "A3_var_tope1", "A4_var_tope1.5"):
        m, x = MM[k], A[k]
        dentro = abs(x["alfa"] - m["alfa"]) <= m["se"]
        print(f"- {k}: α artículo {m['alfa']} ({m['se']}) vs réplica {f4(x['alfa'], 2)} ({f4(x['se_hc0'], 2)}); "
              f"diferencia {f4(x['alfa'] - m['alfa'], 2)} pp; dentro de ±1 e.e.: {dentro}; t HC0 {f4(x['t_hc0'], 2)}; "
              f"Sharpe gestionada artículo {m['sharpe']} vs {f4(x['sr_fs'], 3)}; AR {m['ar']} vs {f4(x['ar'], 3)}")
    m, x = MM["A1_var"], A["A1_var"]
    print(f"- A1: β {m['beta']} vs {f4(x['beta'], 3)}; N {m['n']} vs {x['n']}; R² {m['r2']} vs {f4(x['r2'], 3)}; "
          f"rmse {m['rmse']} vs {f4(x['rmse'], 2)}; SR mercado {MM['sharpe_mercado']} vs {f4(x['sr_f'], 3)}")
    c3 = COWY["t3"]
    x = A["A1_var_rvCOWY_1926_2016"]
    print(f"- Cederburg tabla 3 (RV COWY, 1926-08 a 2016-12): α {c3['alfa']} (t {c3['t_white']}) vs {f4(x['alfa'], 2)} "
          f"(t HC0 {f4(x['t_hc0'], 2)}); β {c3['beta']} vs {f4(x['beta'], 3)}; R² {c3['r2']} vs {f4(x['r2'], 3)}; "
          f"AR {c3['ar']} vs {f4(x['ar'], 3)}; c* {c3['c']} vs c×10⁴ {f4(x['c_pct2'], 2)}")
    c1 = COWY["t1"]
    print(f"- Cederburg tabla 1 (comparación directa): SR {c1['sr_f']} vs {f4(x['sr_f'], 3)}; SR gestionada "
          f"{c1['sr_fs']} vs {f4(x['sr_fs'], 3)}; ΔSR {c1['dif']} [p {c1['p']}] vs {f4(x['jk_dif'], 3)} "
          f"[p {f4(x['jk_p'], 2)}]; pesos P01/P50/P99 {c1['p01']}/{c1['p50']}/{c1['p99']} vs "
          f"{f4(x['pesos']['p01'], 2)}/{f4(x['pesos']['p50'], 2)}/{f4(x['pesos']['p99'], 2)}; "
          f"media gestionada {f4(x['media_fs'], 2)} vs 9.55; media mercado {f4(x['media_f'], 2)} vs 7.80; "
          f"sd {f4(x['sd_f'], 2)} vs 18.61; corr {f4(x['corr'], 3)} vs 0.63")

    print("\n### H2. MM después de publicarse (c fija de 1926-08 a 2015-12)\n")
    c_mm = A["A1_var"]["c"]
    H2 = {"A1_post_JF_2017-08": parte_a(D, *POST_JF, "var", c_fija=c_mm),
          "A1_post_NBER_2016-01": parte_a(D, *POST_NBER, "var", c_fija=c_mm),
          "A2_vol_post_JF_2017-08": parte_a(D, *POST_JF, "vol", c_fija=A["A2_vol"]["c"]),
          "A3_tope1_post_JF_2017-08": parte_a(D, *POST_JF, "var", tope=1.0, c_fija=c_mm),
          "A4_tope1.5_post_JF_2017-08": parte_a(D, *POST_JF, "var", tope=1.5, c_fija=c_mm)}
    print(ENCABEZADO_A)
    for k, v in H2.items():
        print(linea_a(k, v))

    print("\n### Subperiodos (A1, c de cada ventana)\n")
    SUB = {nombre: parte_a(D, f0, f1, "var") for nombre, f0, f1 in SUBPERIODOS}
    print(ENCABEZADO_A)
    for k, v in SUB.items():
        print(linea_a(k, v))
    R["parte_a"] = A
    R["h2"] = H2
    R["subperiodos"] = SUB

    # ------------------------------------------------------------ Parte C (registrada)
    print("\n## Parte C. Versión operable en el motor (registrada en R05-variantes.csv)\n")
    base = dict(id_replica=ID, min_historia=MIN_HISTORIA, cortes=CORTES, nombres_segmentos=NOMBRES,
                extras=D["extras"], fuente_datos=fuente)

    def correr(senal, variante, *, es_prueba, escenario="defecto", nota="", emin=0.0, emax=1.0, fx=None,
               parametros=None):
        com, spr = ESCENARIOS[escenario]
        return bt.backtest_senal(D["mercado"], D["rf"], senal, variante=variante, comision_por_lado=com,
                                 spread_por_lado=spr, exposicion_min=emin, exposicion_max=emax, fx=fx,
                                 parametros=parametros or {}, es_prueba=es_prueba, nota=nota, **base)

    pruebas = []
    for nombre, forma, tope, clave in VARIANTES:
        pruebas.append(correr(hacer_senal_gestionada(forma, tope, clave), nombre, es_prueba=True, emax=tope,
                              parametros={"forma": forma, "tope": tope, "rv": clave, "K": K,
                                          "c": "expansiva, sd(f)/sd(f/x) sin tope"}))
    bh = correr(bt.senal_comprar_y_mantener, "comprar_y_mantener", es_prueba=False, nota="regla sencilla")
    ef = correr(bt.senal_efectivo, "efectivo", es_prueba=False, nota="regla sencilla")
    sma = correr(bt.senal_media_movil(10), "sma10", es_prueba=False, nota="regla sencilla del mismo tipo (riesgo)")
    principales = pruebas + [bh, sma, ef]

    # verificacion independiente de pesos
    difs = {}
    for r, (nombre, forma, tope, clave) in zip(pruebas, VARIANTES):
        directos = pesos_directos(D, r.fechas, "gestionada", clave, forma, tope)
        difs[nombre] = max(abs(a - b) for a, b in zip(directos, r.exposicion))
    print("Verificación: máx |w_motor − w_directo| por variante: "
          + ", ".join(f"{k} {v:.2e}" for k, v in difs.items()))
    R["verificacion_pesos_C"] = difs

    for seg in ["completo"] + NOMBRES:
        print()
        print(tabla_motor(principales, seg, bh))

    print("\nDistribución de exposiciones (fracción de meses en el tope; P50) por segmento:")
    expos = {}
    for r, (nombre, forma, tope, clave) in zip(pruebas, VARIANTES):
        fila = {}
        for seg in ["completo", "dentro_muestra", "fuera_muestra"]:
            i0, i1 = indices_ventana(r, *SEG_FECHAS[seg])
            w = r.exposicion[i0:i1]
            fila[seg] = {"frac_tope": sum(1 for v in w if v >= tope - 1e-12) / len(w),
                         "p50": statistics.median(w), "min": min(w)}
        expos[nombre] = fila
        print(f"- {nombre}: " + "; ".join(f"{s} tope {f4(v['frac_tope'], 3)}, P50 {f4(v['p50'], 3)}, min "
                                           f"{f4(v['min'], 3)}" for s, v in fila.items()))
    R["exposiciones"] = expos

    # tabla compacta para JSON
    def resumen(r):
        out = {}
        for seg in ["completo"] + NOMBRES:
            x = r.metricas[seg]
            a = alfa_contra_mercado(r, *SEG_FECHAS[seg])
            out[seg] = {k: x[k] for k in ("fecha_inicio", "fecha_fin", "n_periodos", "cagr", "vol_anual", "sharpe",
                                          "mdd", "exposicion_media", "rotacion_anual", "costo_anual", "psr")}
            out[seg].update({"alfa": a["alfa"], "t_hc0": a["t_hc0"], "t_nw": a["t_nw"], "beta": a["beta"]})
            if r is not bh and not max(r.exposicion) == min(r.exposicion) == 0:
                jk = jobson_korkie(exceso(r, *SEG_FECHAS[seg]), exceso(bh, *SEG_FECHAS[seg]))
                out[seg].update({"dsr_vs_cym": jk["dif"], "p_jk": jk["p"]})
        return out

    R["parte_c"] = {r.variante: resumen(r) for r in principales}

    # ------------------------------------------------------------ sensibilidad de costos
    print("\n### Sensibilidad de costos (es_prueba=False)\n")
    sens = {}
    for escenario in ("spread_medio", "bruto"):
        filas = []
        for nombre, forma, tope, clave in VARIANTES:
            filas.append(correr(hacer_senal_gestionada(forma, tope, clave), f"{nombre}|{escenario}",
                                es_prueba=False, escenario=escenario, emax=tope, nota=f"sensibilidad: {escenario}",
                                parametros={"forma": forma, "tope": tope, "rv": clave, "K": K}))
        bh_e = correr(bt.senal_comprar_y_mantener, f"comprar_y_mantener|{escenario}", es_prueba=False,
                      escenario=escenario, nota=f"sensibilidad: {escenario}")
        sma_e = correr(bt.senal_media_movil(10), f"sma10|{escenario}", es_prueba=False, escenario=escenario,
                       nota=f"sensibilidad: {escenario}")
        filas += [bh_e, sma_e]
        for seg in ("dentro_muestra", "fuera_muestra"):
            print(tabla_motor(filas, seg, bh_e))
            print()
        sens[escenario] = {r.variante: resumen_simple(r) for r in filas}
    R["sensibilidad_costos"] = sens

    # ------------------------------------------------------------ costo de apalancamiento (fuera del motor)
    print("### Sensibilidad: costo del apalancamiento de 3%/año sobre RF (post-proceso, no registrado)\n")
    print("| variante | segmento | Sharpe motor | Sharpe ajustado | CAGR motor | CAGR ajustado | MDD ajustado |")
    print("|---|---|---|---|---|---|---|")
    apal = {}
    for r, (nombre, forma, tope, clave) in zip(pruebas, VARIANTES):
        if tope <= 1.0:
            continue
        r_adj = [rn - max(w - 1.0, 0.0) * SPREAD_MARGEN_ANUAL / 12 for rn, w in zip(r.r_neto, r.exposicion)]
        apal[nombre] = {}
        for seg in ("completo", "dentro_muestra", "fuera_muestra"):
            x = metricas_ventana(r, r_adj, *SEG_FECHAS[seg])
            y = r.metricas[seg]
            apal[nombre][seg] = {"sharpe": x["sharpe"], "cagr": x["cagr"], "mdd": x["mdd"]}
            print(f"| {nombre} | {seg} | {f4(y['sharpe'])} | {f4(x['sharpe'])} | {f4(y['cagr'])} | {f4(x['cagr'])} | "
                  f"{f4(x['mdd'])} |")
    R["sensibilidad_apalancamiento"] = apal

    # ------------------------------------------------------------ MXN
    print("\n### Sensibilidad en MXN (DEXMXUS; efectivo RF en USD convertido; es_prueba=False)\n")
    fx = dh.fred("DEXMXUS")
    print(f"DEXMXUS: {fx[0][0]} a {fx[-1][0]} ({len(fx)} obs)")
    mx = []
    for nombre, forma, tope, clave in [VARIANTES[0], VARIANTES[3]]:
        mx.append(correr(hacer_senal_gestionada(forma, tope, clave), f"{nombre}|mxn|rf_usd", es_prueba=False,
                         emax=tope, fx=fx, nota="sensibilidad: MXN con DEXMXUS",
                         parametros={"forma": forma, "tope": tope, "rv": clave, "K": K}))
    bh_mx = correr(bt.senal_comprar_y_mantener, "comprar_y_mantener|mxn|rf_usd", es_prueba=False, fx=fx,
                   nota="sensibilidad: MXN con DEXMXUS")
    sma_mx = correr(bt.senal_media_movil(10), "sma10|mxn|rf_usd", es_prueba=False, fx=fx,
                    nota="sensibilidad: MXN con DEXMXUS")
    mx += [bh_mx, sma_mx]
    for seg in ("completo", "dentro_muestra", "fuera_muestra"):
        print(bt.comparar(mx, seg, claves=("cagr", "vol_anual", "sharpe", "mdd", "exposicion_media",
                                           "costo_anual")).replace("\n", "\n") + f"\n  ({seg}: "
              f"{mx[0].metricas[seg]['fecha_inicio']} a {mx[0].metricas[seg]['fecha_fin']})\n")
    R["mxn"] = {r.variante: resumen_simple(r) for r in mx}

    # ------------------------------------------------------------ Parte B: Cederburg en el motor
    print("\n## Parte B. Combinación en tiempo real de Cederburg et al. (motor; es_prueba=False)\n")
    s1 = correr(hacer_senal_s1("rv2_cowy"), "cederburg_S1_tiempo_real|bruto", es_prueba=False, escenario="bruto",
                emin=-TOPE_COMB, emax=TOPE_COMB, nota="contraste Cederburg: S1 bruto",
                parametros={"K": K, "gamma": GAMMA, "tope": TOPE_COMB, "rv": "rv2_cowy"})
    s2 = correr(senal_s2, "cederburg_S2_original_tiempo_real|bruto", es_prueba=False, escenario="bruto",
                emin=-TOPE_COMB, emax=TOPE_COMB, nota="contraste Cederburg: S2 bruto",
                parametros={"K": K, "gamma": GAMMA, "tope": TOPE_COMB})
    s1_mm = correr(hacer_senal_s1("rv2_mm"), "cederburg_S1_rvMM|bruto", es_prueba=False, escenario="bruto",
                   emin=-TOPE_COMB, emax=TOPE_COMB, nota="contraste Cederburg: S1 con RV de MM, bruto",
                   parametros={"K": K, "gamma": GAMMA, "tope": TOPE_COMB, "rv": "rv2_mm"})
    s1_d = correr(hacer_senal_s1("rv2_cowy"), "cederburg_S1_tiempo_real|defecto", es_prueba=False,
                  emin=-TOPE_COMB, emax=TOPE_COMB, nota="contraste Cederburg: S1 con costos GBM",
                  parametros={"K": K, "gamma": GAMMA, "tope": TOPE_COMB, "rv": "rv2_cowy"})
    s2_d = correr(senal_s2, "cederburg_S2_original_tiempo_real|defecto", es_prueba=False,
                  emin=-TOPE_COMB, emax=TOPE_COMB, nota="contraste Cederburg: S2 con costos GBM",
                  parametros={"K": K, "gamma": GAMMA, "tope": TOPE_COMB})
    ver_b = {"S1": max(abs(a - b) for a, b in zip(pesos_directos(D, s1.fechas, "S1", "rv2_cowy"), s1.exposicion)),
             "S1_rvMM": max(abs(a - b) for a, b in zip(pesos_directos(D, s1_mm.fechas, "S1", "rv2_mm"),
                                                         s1_mm.exposicion)),
             "S2": max(abs(a - b) for a, b in zip(pesos_directos(D, s2.fechas, "S2", "rv2_cowy"), s2.exposicion))}
    print("Verificación: máx |y_motor − y_directo|: " + ", ".join(f"{k} {v:.2e}" for k, v in ver_b.items()))
    R["verificacion_pesos_B"] = ver_b

    def s3_ex_post(f0, f1, clave):
        fechas = [t for t in D["fechas"] if t in D["previo"] and f0 <= t <= f1]
        f = [D["f"][t] for t in fechas]
        g = [D["f"][t] / D[clave][D["previo"][t]] for t in fechas]
        mg, mf = statistics.fmean(g), statistics.fmean(f)
        vg, vf, c_ = statistics.variance(g), statistics.variance(f), statistics.covariance(g, f)
        det = vg * vf - c_ * c_
        q = (vf * mg * mg - 2 * c_ * mg * mf + vg * mf * mf) / det
        return math.sqrt(q) * math.sqrt(12)

    ventanas_b = [("Cederburg OOS 1936-08 a 2016-12", *VENTANA_COWY_OOS),
                  ("dentro_muestra 1936-08 a 2015-12", fm(1936, 8), CORTES[0]),
                  ("fuera_muestra 2017-08 al final", *SEG_FECHAS["fuera_muestra"]),
                  ("completo 1936-08 al final", fm(1936, 8), FIN),
                  ("2017-01 al final (post-Cederburg)", fm(2017, 1), FIN)]
    print("\n| Ventana | n | S1 comb. tiempo real | S2 original tiempo real | S1−S2 [p JK] | CER S1 | CER S2 | "
          "S3 ex post | S1 RV MM | S1 neto GBM | S2 neto GBM | S1−S2 neto [p JK] | y medio S1 | "
          "frac. |y|=5 |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    B = {}
    for nombre, f0, f1 in ventanas_b:
        e1, e2 = exceso(s1, f0, f1), exceso(s2, f0, f1)
        jk = jobson_korkie(e1, e2)
        jk_n = jobson_korkie(exceso(s1_d, f0, f1), exceso(s2_d, f0, f1))
        i0, i1 = indices_ventana(s1, f0, f1)
        ys = s1.exposicion[i0:i1]
        B[nombre] = {"n": len(e1), "S1": jk["sr_a"], "S2": jk["sr_b"], "dif": jk["dif"], "p": jk["p"],
                     "cer_S1": cer_anual_pct(e1), "cer_S2": cer_anual_pct(e2), "S3": s3_ex_post(f0, f1, "rv2_cowy"),
                     "S1_rvMM": sharpe_anual(exceso(s1_mm, f0, f1)), "S1_neto": jk_n["sr_a"], "S2_neto": jk_n["sr_b"],
                     "dif_neto": jk_n["dif"], "p_neto": jk_n["p"], "y_medio": statistics.fmean(ys),
                     "frac_tope": sum(1 for v in ys if abs(v) >= TOPE_COMB - 1e-12) / len(ys)}
        b = B[nombre]
        print(f"| {nombre} | {b['n']} | {f4(b['S1'], 3)} | {f4(b['S2'], 3)} | {f4(b['dif'], 3)} [{f4(b['p'], 2)}] | "
              f"{f4(b['cer_S1'], 2)} | {f4(b['cer_S2'], 2)} | {f4(b['S3'], 3)} | {f4(b['S1_rvMM'], 3)} | "
              f"{f4(b['S1_neto'], 3)} | {f4(b['S2_neto'], 3)} | {f4(b['dif_neto'], 3)} [{f4(b['p_neto'], 2)}] | "
              f"{f4(b['y_medio'], 3)} | {f4(b['frac_tope'], 3)} |")
    t5 = COWY["t5"]
    print(f"\nCederburg tabla 5 (MKT): S1 {t5['S1']}, S2 {t5['S2']}, dif {t5['dif']} [p {t5['p']}], CER S1 "
          f"{t5['cer_S1']}, CER S2 {t5['cer_S2']}, S3 {t5['S3']}")
    R["parte_b"] = B

    # ------------------------------------------------------------ DSR
    print("\n## Sharpe deflactado (registro R05)\n")
    dsr = {}
    d0 = bt.sharpe_deflactado_de_registro(ID)
    sel = d0["variante"]
    dsr["dentro_N_registrado"] = d0
    dsr["dentro_N_conservador"] = bt.sharpe_deflactado_de_registro(ID, n_pruebas=max(N_CONSERVADOR, d0["n_registradas"]))
    dsr["fuera_N_registrado"] = bt.sharpe_deflactado_de_registro(ID, segmento="fuera_muestra", variante=sel)
    dsr["fuera_N_conservador"] = bt.sharpe_deflactado_de_registro(
        ID, n_pruebas=max(N_CONSERVADOR, d0["n_registradas"]), segmento="fuera_muestra", variante=sel)
    print("| Lectura | segmento | variante | DSR | cumple 0.95 | N | V (SR periodo) | SR anual | SR0 anual | n | "
          "PSR sin deflactar |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for k, v in dsr.items():
        print(f"| {k} | {v['segmento']} | {v['variante']} | {f4(v['dsr'])} | {v['cumple']} | {v['n_pruebas']} | "
              f"{f4(v['varianza_sharpes_periodo'], 6)} | {f4(v['sr_anual'])} | {f4(v['sr0_anual'])} | {v['n_obs']} | "
              f"{f4(v['psr_sin_deflactar'])} |")
    R["dsr"] = dsr
    R["seleccionada"] = sel

    # ------------------------------------------------------------ veredictos pre-registrados (mecanicos)
    print("\n## Veredictos mecánicos según el pre-registro\n")
    a1 = A["A1_var"]
    h1_tol = abs(a1["alfa"] - MM["A1_var"]["alfa"]) <= MM["A1_var"]["se"]
    h1 = ("No replicado" if a1["alfa"] <= 0 or a1["t_hc0"] < 2 else
          "Replicado" if h1_tol else "Replicado con diferencias")
    h2x = H2["A1_post_JF_2017-08"]
    h2 = ("se sostiene" if h2x["alfa"] > 0 and h2x["sr_fs"] > h2x["sr_f"] else "refutada") + \
         (" (significativo)" if h2x["t_hc0"] >= 2 else " (no significativo)")
    bc = B["Cederburg OOS 1936-08 a 2016-12"]
    tol3 = abs(bc["S1"] - t5["S1"]) <= 0.05 and abs(bc["S2"] - t5["S2"]) <= 0.05
    if bc["dif"] > 0 and bc["p"] < 0.10:
        h3 = "crítica refutada para el mercado"
    elif bc["dif"] < 0:
        h3 = "Replicado" if tol3 else "Replicado con diferencias"
    else:
        h3 = "No replicado (S1−S2 ≥ 0, no significativo)"
    rsel = next(r for r in pruebas if r.variante == sel)
    fo, dn = rsel.metricas["fuera_muestra"], rsel.metricas["dentro_muestra"]
    bfo, bdn = bh.metricas["fuera_muestra"], bh.metricas["dentro_muestra"]
    sfo = sma.metricas["fuera_muestra"]
    vs_bh = fo["sharpe"] > bfo["sharpe"] and abs(fo["mdd"]) < abs(bfo["mdd"])
    vs_sma = vs_bh and fo["sharpe"] > sfo["sharpe"] and abs(fo["mdd"]) < abs(sfo["mdd"])
    a_fo = alfa_contra_mercado(rsel, *SEG_FECHAS["fuera_muestra"])
    a_dn = alfa_contra_mercado(rsel, *SEG_FECHAS["dentro_muestra"])
    freno = abs(fo["mdd"]) < abs(bfo["mdd"]) or abs(dn["mdd"]) < abs(bdn["mdd"])
    h4 = {"seleccionada": sel, "agrega_valor_vs_cym": vs_bh, "agrega_valor_vs_sma10": vs_sma,
          "h4_refutada_sharpe": fo["sharpe"] <= bfo["sharpe"],
          "freno_refutado": not freno,
          "mdd_fuera_menor": abs(fo["mdd"]) < abs(bfo["mdd"]), "mdd_dentro_menor": abs(dn["mdd"]) < abs(bdn["mdd"]),
          "alfa_fuera": a_fo, "alfa_dentro": a_dn,
          "alfa_t3": a_fo["t_hc0"] >= 3 and a_dn["t_hc0"] >= 3, "dsr_dentro": d0["dsr"],
          "dsr_cumple": d0["cumple"]}
    print(f"- H1 (MM 1926-2015): {h1}. α {f4(a1['alfa'], 2)} (t HC0 {f4(a1['t_hc0'], 2)}) vs 4.86 ± 1.56")
    print(f"- H2 (post JF 2017-08 a {h2x['hasta']}): {h2}. α {f4(h2x['alfa'], 2)} (t HC0 {f4(h2x['t_hc0'], 2)}); "
          f"SR gestionada {f4(h2x['sr_fs'], 3)} vs mercado {f4(h2x['sr_f'], 3)} [p JK {f4(h2x['jk_p'], 2)}]")
    print(f"- H3 (Cederburg): {h3}. S1 {f4(bc['S1'], 3)} vs S2 {f4(bc['S2'], 3)} (artículo 0.42 vs 0.46); "
          f"dif {f4(bc['dif'], 3)} [p {f4(bc['p'], 2)}]")
    print(f"- H4 (operable): seleccionada {sel}. Fuera: Sharpe {f4(fo['sharpe'])} vs CyM {f4(bfo['sharpe'])} vs SMA10 "
          f"{f4(sfo['sharpe'])}; MDD {f4(fo['mdd'])} vs {f4(bfo['mdd'])} vs {f4(sfo['mdd'])}. Agrega valor vs CyM: "
          f"{vs_bh}; vs SMA10: {vs_sma}; H4 refutada por Sharpe: {h4['h4_refutada_sharpe']}; freno refutado: "
          f"{h4['freno_refutado']}; α fuera {f4(a_fo['alfa'], 2)} (t {f4(a_fo['t_hc0'], 2)}), α dentro "
          f"{f4(a_dn['alfa'], 2)} (t {f4(a_dn['t_hc0'], 2)}); DSR dentro {f4(d0['dsr'])}")
    R["veredictos"] = {"H1": h1, "H2": h2, "H3": h3, "H4": h4}
    print(f"\nRegistro: {bt.ruta_registro(ID)}")
    return R


def resumen_simple(r: bt.ResultadoBacktest) -> dict:
    return {seg: {k: r.metricas[seg][k] for k in ("fecha_inicio", "fecha_fin", "cagr", "vol_anual", "sharpe", "mdd",
                                                   "exposicion_media", "costo_anual")}
            for seg in ["completo"] + r.segmentos}


if __name__ == "__main__":
    main()
