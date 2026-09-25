#!/usr/bin/env python3
"""R07 - La curva 10a-3m como predictor de recesion (Estrella y Mishkin, 1998, REStat 80(1):45-61),
la inversion de 2022-2024 y el rendimiento accionario despues de una inversion.

Reproduce desde la raiz del repo:  python3 laboratorio/replicas/R07.py
Solo biblioteca estandar. Las corridas del motor se agregan a laboratorio/replicas/R07-variantes.csv.
Salida completa en R07-salida.txt; cifras clave en R07-resultados.json.
Modo humo (sin registrar ni mostrar resultados, solo para detectar errores de programacion):
    python3 laboratorio/replicas/R07.py --humo

Pre-registro: R07-curva-invertida-y-recesion.md, secciones 1-9.
  Parte A (estadistica, NO es estrategia):
    A1 probit trimestral P(R_{q+k}) = Phi(a + b S_q), k = 1..8, 1959T1-1995T1 (H1).
    A2 fuera de muestra al estilo del articulo, objetivos 1971T1-1995T1 (H2).
    A3 probit mensual 12 meses adelante: dentro de muestra, fuera de muestra recursivo con
       cronologia final y en tiempo real (anuncios del NBER; ALFRED como verificacion) (H3).
    A4 episodio 2022-2024 (H4).  A5 rendimiento del mercado tras el inicio de cada inversion (H5).
  Parte B (operable, motor): 8 reglas de prueba + reglas sencillas + sensibilidades (H6).
"""
from __future__ import annotations

import io
import json
import math
import statistics
import sys
from datetime import date, datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from herramientas import backtest as bt  # noqa: E402
from herramientas import datos_historicos as dh  # noqa: E402
from herramientas.datos import ErrorDatos  # noqa: E402

# ================================================================ parametros pre-registrados
ID = "R07"
DIR = Path(__file__).resolve().parent
HUMO = "--humo" in sys.argv
ID_REG = None if HUMO else ID
H = 12                      # horizonte mensual (meses)
NW_MENSUAL = 11             # rezagos NW en mensual (sensibilidad: 12)
N_CONSERVADOR = 16
CORTE = date(1998, 2, 28)   # publicacion en REStat (febrero de 1998)
NORMAL = statistics.NormalDist()
SQRT2 = math.sqrt(2.0)
LOG_SQRT_2PI = 0.5 * math.log(2.0 * math.pi)
EPS = 1e-12


def mi(a: int, m: int) -> int:
    return a * 12 + m - 1


def mi_de(f: date) -> int:
    return f.year * 12 + f.month - 1


def fdm(k: int) -> date:
    return dh.fin_de_mes(k // 12, k % 12 + 1)


def et(k: int) -> str:
    return f"{k // 12:04d}-{k % 12 + 1:02d}"


def qi(a: int, t: int) -> int:
    return a * 4 + t - 1


def qi_de(f: date) -> int:
    return f.year * 4 + (f.month - 1) // 3


def etq(q: int) -> str:
    return f"{q // 4}T{q % 4 + 1}"


INICIO_EST = mi(1959, 1)            # primer origen de estimacion (como Estrella y Mishkin)
Q_INI, Q_FIN, Q_OOS_INI = qi(1959, 1), qi(1995, 1), qi(1971, 1)
M_FIN_EM = mi(1994, 3)              # ultimo origen mensual de la era del articulo (objetivo 1995-03)
OOS_ERA = (mi(1970, 1), mi(1998, 2))
OOS_POST_INI = mi(1998, 3)
OOS_POST_FIN_SENS = mi(2024, 2)
PRIMERA_DECISION = date(1971, 1, 31)

# Anuncios del NBER (Business Cycle Dating Committee Announcements, consultado 2026-09-25).
ANUNCIOS = [
    (date(1980, 6, 3), "pico", mi(1980, 1)), (date(1981, 7, 8), "valle", mi(1980, 7)),
    (date(1982, 1, 6), "pico", mi(1981, 7)), (date(1983, 7, 8), "valle", mi(1982, 11)),
    (date(1991, 4, 25), "pico", mi(1990, 7)), (date(1992, 12, 22), "valle", mi(1991, 3)),
    (date(2001, 11, 26), "pico", mi(2001, 3)), (date(2003, 7, 17), "valle", mi(2001, 11)),
    (date(2008, 12, 1), "pico", mi(2007, 12)), (date(2010, 9, 20), "valle", mi(2009, 6)),
    (date(2020, 6, 8), "pico", mi(2020, 2)), (date(2021, 7, 19), "valle", mi(2020, 4)),
]
REZAGO_PRE1979 = 12   # supuesto: giros anteriores a los anuncios formales se conocen 12 meses despues

# Cifras del articulo (RP 9609, tablas 2/A1 y 4) y de Current Issues 1996
PAPER_IN = {1: (0.071, -2.71), 2: (0.211, -4.21), 3: (0.271, -4.71), 4: (0.296, -4.57),
            5: (0.256, -3.87), 6: (0.149, -4.13), 7: (0.078, -3.02), 8: (0.031, -1.63)}
PAPER_OUT = {1: 0.072, 2: 0.236, 3: 0.328, 4: 0.295, 5: 0.155, 6: 0.141, 7: "negativo", 8: "negativo"}
CI96_SPREAD = {0.10: 0.76, 0.50: -0.82, 0.90: -2.40}


# ================================================================ salida

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


def f4(x, nd: int = 4) -> str:
    if x is None:
        return "NA"
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, float):
        if math.isnan(x):
            return "nan"
        if math.isinf(x):
            return "inf"
        return f"{x:.{nd}f}"
    return str(x)


def pct(x, nd: int = 2) -> str:
    return "NA" if x is None else f"{100 * x:.{nd}f}%"


# ================================================================ probit (stdlib)

def cdf(z: float) -> float:
    return 0.5 * math.erfc(-z / SQRT2)


def log_cdf(z: float) -> float:
    if z > -37.0:
        return math.log(0.5 * math.erfc(-z / SQRT2))
    return -0.5 * z * z - math.log(-z) - LOG_SQRT_2PI


def lam(z: float) -> float:
    """phi(z)/Phi(z), estable en la cola izquierda."""
    if z > -37.0:
        return math.exp(-0.5 * z * z - LOG_SQRT_2PI) / (0.5 * math.erfc(-z / SQRT2))
    return -z - 1.0 / z


def pseudo_r2(llu: float, llc: float, n: int) -> float:
    """Estrella (1998): 1 - (log Lu / log Lc)^(-(2/n) log Lc)."""
    return 1.0 - (llu / llc) ** (-(2.0 / n) * llc)


def ll_constante(y: list) -> float | None:
    n, n1 = len(y), sum(y)
    if n1 == 0 or n1 == n:
        return None
    p = n1 / n
    return n1 * math.log(p) + (n - n1) * math.log(1 - p)


def ll_prob(p: list, y: list) -> float:
    s = 0.0
    for pi, yi in zip(p, y):
        pi = min(max(pi, EPS), 1 - EPS)
        s += math.log(pi) if yi else math.log(1 - pi)
    return s


def probit_mv(x: list, y: list, rezagos_nw: tuple = (), max_iter: int = 100, tol: float = 1e-10) -> dict | None:
    """Probit P(y=1) = Phi(a + b x) por MV (Newton-Raphson con busqueda de paso).

    Devuelve None si y no tiene ceros y unos. rezagos_nw: rezagos de Newey-West (Bartlett) para
    errores estandar sandwich sobre los scores (0 = White); vacio = sin errores estandar.
    """
    n, n1 = len(y), sum(y)
    if n < 3 or n1 == 0 or n1 == n:
        return None
    a, b = NORMAL.inv_cdf(n1 / n), 0.0

    def loglik(a_: float, b_: float) -> float:
        s = 0.0
        for xi, yi in zip(x, y):
            z = a_ + b_ * xi
            s += log_cdf(z if yi else -z)
        return s

    L = loglik(a, b)
    conv, it = False, 0
    for it in range(1, max_iter + 1):
        g0 = g1 = h00 = h01 = h11 = 0.0
        for xi, yi in zip(x, y):
            q = 1.0 if yi else -1.0
            z = q * (a + b * xi)
            lz = lam(z)
            w = lz * (lz + z)
            g0 += lz * q
            g1 += lz * q * xi
            h00 -= w
            h01 -= w * xi
            h11 -= w * xi * xi
        det = h00 * h11 - h01 * h01
        if det == 0:
            break
        d0 = -(h11 * g0 - h01 * g1) / det
        d1 = -(-h01 * g0 + h00 * g1) / det
        paso = 1.0
        while True:
            na, nb = a + paso * d0, b + paso * d1
            nl = loglik(na, nb)
            if nl >= L - 1e-12 or paso < 1e-10:
                break
            paso *= 0.5
        a, b, L = na, nb, nl
        if max(abs(paso * d0), abs(paso * d1)) < tol:
            conv = True
            break
    llc = ll_constante(y)
    salida = {"a": a, "b": b, "ll": L, "llc": llc, "n": n, "n1": n1, "r2": pseudo_r2(L, llc, n),
              "convergio": conv, "iter": it}
    if rezagos_nw:
        sc, h00, h01, h11 = [], 0.0, 0.0, 0.0
        for xi, yi in zip(x, y):
            q = 1.0 if yi else -1.0
            z = q * (a + b * xi)
            lz = lam(z)
            w = lz * (lz + z)
            sc.append((lz * q, lz * q * xi))
            h00 += w
            h01 += w * xi
            h11 += w * xi * xi
        det = h00 * h11 - h01 * h01
        A = [[h11 / det, -h01 / det], [-h01 / det, h00 / det]]      # (-H)^{-1}
        salida["se_mv"] = (math.sqrt(A[0][0]), math.sqrt(A[1][1]))
        salida["t_mv"] = b / salida["se_mv"][1]
        for L_nw in rezagos_nw:
            S = [[sum(s[p] * s[q] for s in sc) for q in range(2)] for p in range(2)]
            for j in range(1, L_nw + 1):
                wj = 1 - j / (L_nw + 1)
                G = [[sum(sc[t][p] * sc[t - j][q] for t in range(j, n)) for q in range(2)] for p in range(2)]
                for p in range(2):
                    for q in range(2):
                        S[p][q] += wj * (G[p][q] + G[q][p])
            AS = [[sum(A[i][r] * S[r][c] for r in range(2)) for c in range(2)] for i in range(2)]
            V = [[sum(AS[i][r] * A[r][c] for r in range(2)) for c in range(2)] for i in range(2)]
            salida[f"se_nw{L_nw}"] = (math.sqrt(V[0][0]), math.sqrt(V[1][1]))
            salida[f"t_nw{L_nw}"] = b / math.sqrt(V[1][1])
    return salida


def auc(p: list, y: list) -> float | None:
    pos = [a for a, b in zip(p, y) if b]
    neg = [a for a, b in zip(p, y) if not b]
    if not pos or not neg:
        return None
    s = 0.0
    for a in pos:
        for c in neg:
            s += 1.0 if a > c else (0.5 if a == c else 0.0)
    return s / (len(pos) * len(neg))


# ================================================================ etiquetas en tiempo real

def meses_recesion(picos: list, valles: list, m_hasta: int) -> set:
    """Meses de recesion segun los giros visibles; un pico sin valle visible cuenta hasta m_hasta."""
    res = set()
    vs = sorted(valles)
    for p in sorted(picos):
        v = next((x for x in vs if x > p), None)
        fin = m_hasta if v is None else min(v, m_hasta)
        for k in range(p + 1, fin + 1):
            res.add(k)
    return res


def prob_origen(m: int, S: dict, etiqueta, inicio: int = INICIO_EST, h: int = H):
    """Probit estimado con pares (S_s, R_{s+h}), s+h <= m, y evaluado en S_m. -> (p, clima, ajuste)."""
    xs, ys = [], []
    for s in range(inicio, m - h + 1):
        xs.append(S[s])
        ys.append(etiqueta(s + h))
    clima = sum(ys) / len(ys) if ys else None
    ajuste = probit_mv(xs, ys)
    if ajuste is None:
        return clima, clima, None
    return cdf(ajuste["a"] + ajuste["b"] * S[m]), clima, ajuste


def prob_desde_historia(h) -> float:
    """Probabilidad en tiempo real con lo que ve la senal (spread y giros anunciados hasta t-1)."""
    D = h.fecha_decision
    m = mi_de(D)
    S = {mi_de(f): v for f, v in h.extras["spread"]}
    if m not in S:
        raise ValueError(f"Sin spread del mes de decision {D}")
    picos = [int(round(v)) for _, v in h.extras["pico"]]
    valles = [int(round(v)) for _, v in h.extras["valle"]]
    rec = meses_recesion(picos, valles, m)
    p, _, _ = prob_origen(m, S, lambda k: 1 if k in rec else 0)
    return p


# ================================================================ senales del motor

def _ultimos(h, n: int) -> list:
    sp = h.extras["spread"]
    if len(sp) < n:
        raise ValueError("Historia de spread insuficiente")
    ult = sp[-n:]
    if mi_de(ult[-1][0]) != mi_de(h.fecha_decision):
        raise ValueError(f"Falta el spread de {h.fecha_decision}")
    if mi_de(ult[-1][0]) - mi_de(ult[0][0]) != n - 1:
        raise ValueError("Spreads no consecutivos")
    return [v for _, v in ult]


def senal_inv1(h) -> float:
    return 0.0 if _ultimos(h, 1)[0] < 0 else 1.0


def senal_inv3(h) -> float:
    return 0.0 if all(v < 0 for v in _ultimos(h, 3)) else 1.0


def senal_inv3_medio(h) -> float:
    return 0.5 if all(v < 0 for v in _ultimos(h, 3)) else 1.0


def senal_inv_fuera12(h) -> float:
    return 0.0 if any(v < 0 for v in _ultimos(h, 12)) else 1.0


def senal_desinv12(h) -> float:
    s = _ultimos(h, 15)        # meses m-14 .. m ; j recorre m-11 .. m (indices 3..14)
    for i in range(3, 15):
        if s[i] >= 0 and s[i - 1] < 0 and s[i - 2] < 0 and s[i - 3] < 0:
            return 0.0
    return 1.0


def senal_probit50(h) -> float:
    return 0.0 if prob_desde_historia(h) > 0.5 else 1.0


def senal_probit30(h) -> float:
    return 0.0 if prob_desde_historia(h) > 0.3 else 1.0


def senal_probit_cont(h) -> float:
    return min(1.0, max(0.0, 1.0 - prob_desde_historia(h)))


VARIANTES = [  # lista cerrada del pre-registro
    ("inv1", senal_inv1, "w=0 si S_{t-1}<0"),
    ("inv3", senal_inv3, "w=0 si S<0 en t-1,t-2,t-3 (regla 6(1) cap. 04)"),
    ("inv3_medio", senal_inv3_medio, "w=0.5 si S<0 en t-1,t-2,t-3"),
    ("probit50", senal_probit50, "w=0 si P_rt>0.5 (probit 12m, etiquetas en tiempo real)"),
    ("probit30", senal_probit30, "w=0 si P_rt>0.3"),
    ("probit_cont", senal_probit_cont, "w=1-P_rt"),
    ("inv_fuera12", senal_inv_fuera12, "w=0 si algun S<0 en t-12..t-1"),
    ("desinv12", senal_desinv12, "w=0 12 meses tras des-inversion (S>=0 despues de 3 meses <0)"),
]


# ================================================================ datos

def bey(d_pct: float) -> float:
    d = d_pct / 100.0
    return 100.0 * 365.0 * d / (360.0 - 91.0 * d)


def cargar() -> dict:
    gs10 = {mi_de(f): v for f, v in dh.fred("GS10")}
    tb3 = {mi_de(f): v for f, v in dh.fred("TB3MS")}
    usrec_l = dh.fred("USREC")
    usrecq_l = dh.fred("USRECQ")
    t10y3m = dh.fred("T10Y3M")
    fx = dh.fred("DEXMXUS")
    fr = dh.french("F-F_Research_Data_Factors", "mensual")
    ini, fin = max(min(gs10), min(tb3)), min(max(gs10), max(tb3))
    for k in range(ini, fin + 1):
        if k not in gs10 or k not in tb3:
            raise SystemExit(f"Falta GS10 o TB3MS en {et(k)}: se detiene, no se imputa")
    S = {k: gs10[k] - bey(tb3[k]) for k in range(ini, fin + 1)}
    S_desc = {k: gs10[k] - tb3[k] for k in range(ini, fin + 1)}
    usrec = {mi_de(f): v for f, v in usrec_l}
    usrecq = {qi_de(f): v for f, v in usrecq_l}
    if any(v not in (0.0, 1.0) for v in usrec.values()) or any(v not in (0.0, 1.0) for v in usrecq.values()):
        raise SystemExit("USREC/USRECQ con valores distintos de 0/1")
    usrec = {k: int(v) for k, v in usrec.items()}
    usrecq = {k: int(v) for k, v in usrecq.items()}
    # trimestral: promedio de los 3 meses
    Sq, Sq_desc = {}, {}
    for q in range(qi_de(fdm(ini)) + 1, qi_de(fdm(fin)) + 1):
        meses = [q // 4 * 12 + (q % 4) * 3 + j for j in range(3)]
        if all(k in gs10 and k in tb3 for k in meses):
            g = statistics.fmean(gs10[k] for k in meses)
            Sq[q] = g - statistics.fmean(bey(tb3[k]) for k in meses)
            Sq_desc[q] = g - statistics.fmean(tb3[k] for k in meses)
    # T10Y3M promedio mensual
    por_mes: dict = {}
    for f, v in t10y3m:
        por_mes.setdefault(mi_de(f), []).append(v)
    t10_mens = {k: statistics.fmean(v) for k, v in por_mes.items()}
    mercado = dh.rendimiento_mercado_french(fr)
    rf = dh.columna(fr, "RF")
    return {"gs10": gs10, "tb3": tb3, "S": S, "S_desc": S_desc, "Sq": Sq, "Sq_desc": Sq_desc,
            "usrec": usrec, "usrecq": usrecq, "t10y3m": t10y3m, "t10_mens": t10_mens,
            "t10_dias_mes": {k: len(v) for k, v in por_mes.items()}, "fx": fx, "fr": fr,
            "mercado": mercado, "rf": rf, "s_ini": ini, "s_fin": fin}


def giros_de_usrec(usrec: dict) -> list:
    """[(tipo, mes)] de picos (mes previo al primer 1) y valles (ultimo 1) de la serie final."""
    ks = sorted(usrec)
    giros = []
    for a, b in zip(ks, ks[1:]):
        if usrec[a] == 0 and usrec[b] == 1:
            giros.append(("pico", a))
        if usrec[a] == 1 and usrec[b] == 0:
            giros.append(("valle", a))
    return giros


def giros_con_disponibilidad(usrec: dict) -> tuple[list, list]:
    """(giros [(fecha_disponible, tipo, mes)], notas). Anuncios formales desde 1980; antes, +12 meses."""
    derivados = giros_de_usrec(usrec)
    anunciados = {(t, k): f for f, t, k in ANUNCIOS}
    primero_anunciado = min(k for _, _, k in ANUNCIOS)
    salida, notas = [], []
    for t, k in derivados:
        if k >= primero_anunciado:
            if (t, k) not in anunciados:
                raise SystemExit(f"Giro {t} {et(k)} de USREC sin anuncio en la tabla del NBER")
            salida.append((anunciados[(t, k)], t, k))
        else:
            salida.append((fdm(k + REZAGO_PRE1979), t, k))
    faltan = set(anunciados) - set(derivados)
    if faltan:
        raise SystemExit(f"Anuncios del NBER sin giro en USREC: {sorted(faltan)}")
    notas.append(f"giros derivados de USREC: {len(derivados)}; con anuncio formal: {len(anunciados)}")
    return sorted(salida), notas


def etiquetas_rt_en(D: date, giros: list, m_hasta: int | None = None) -> set:
    picos = [k for f, t, k in giros if t == "pico" and f <= D]
    valles = [k for f, t, k in giros if t == "valle" and f <= D]
    return meses_recesion(picos, valles, mi_de(D) if m_hasta is None else m_hasta)


# ================================================================ evaluacion de pronosticos

def evaluar(filas: list) -> dict:
    p = [f["p"] for f in filas]
    y = [f["y"] for f in filas]
    n, n1 = len(y), sum(y)
    llu = ll_prob(p, y)
    llc = ll_constante(y)
    clim = [f["clim"] for f in filas]
    llc_rec = ll_prob(clim, y)
    out = {"n": n, "n1": n1, "ll": llu, "llc_expost": llc,
           "r2_expost": pseudo_r2(llu, llc, n) if llc is not None else None,
           "r2_recursiva": pseudo_r2(llu, llc_rec, n),
           "brier": statistics.fmean((a - b) ** 2 for a, b in zip(p, y)),
           "brier_clima_rec": statistics.fmean((a - b) ** 2 for a, b in zip(clim, y)),
           "brier_const_expost": statistics.fmean((n1 / n - b) ** 2 for b in y),
           "auc": auc(p, y), "fallos_probit": sum(1 for f in filas if f.get("fallo")),
           "no_convergio": sum(1 for f in filas if f.get("noconv"))}
    for u in (0.3, 0.5):
        tp = sum(1 for a, b in zip(p, y) if a > u and b)
        fp = sum(1 for a, b in zip(p, y) if a > u and not b)
        fn = sum(1 for a, b in zip(p, y) if a <= u and b)
        tn = sum(1 for a, b in zip(p, y) if a <= u and not b)
        out[f"u{u}"] = {"VP": tp, "FP": fp, "FN": fn, "VN": tn}
    return out


def pronosticos_mensuales(origenes, S: dict, usrec: dict, giros: list, modo: str, coef=None) -> list:
    filas = []
    for m in origenes:
        if coef is not None:
            p, clim, aj = cdf(coef["a"] + coef["b"] * S[m]), coef["clima"], True
        elif modo == "final":
            p, clim, aj = prob_origen(m, S, lambda k: usrec[k])
        elif modo == "rt":
            rec = etiquetas_rt_en(fdm(m), giros)
            p, clim, aj = prob_origen(m, S, lambda k, rec=rec: 1 if k in rec else 0)
        else:
            raise ValueError(modo)
        noconv = isinstance(aj, dict) and not aj["convergio"]
        filas.append({"origen": m, "p": p, "clim": clim, "y": usrec[m + H], "fallo": aj is None, "noconv": noconv})
    return filas


def linea_eval(nombre: str, e: dict) -> str:
    u3, u5 = e["u0.3"], e["u0.5"]
    return (f"| {nombre} | {e['n']} | {e['n1']} | {f4(e['r2_expost'])} | {f4(e['r2_recursiva'])} | "
            f"{f4(e['brier'])} | {f4(e['brier_clima_rec'])} | {f4(e['brier_const_expost'])} | {f4(e['auc'])} | "
            f"{u5['VP']}/{u5['FP']}/{u5['FN']}/{u5['VN']} | {u3['VP']}/{u3['FP']}/{u3['FN']}/{u3['VN']} | "
            f"{e['fallos_probit']} / {e['no_convergio']} |")


ENCABEZADO_EVAL = ("| Pronóstico | n | n recesión | pseudo R² (L_c ex post) | pseudo R² (L_c recursiva) | Brier | "
                   "Brier clima recursiva | Brier constante ex post | AUC | VP/FP/FN/VN (p>0.5) | "
                   "VP/FP/FN/VN (p>0.3) | fallos / no convergió |\n|---|---|---|---|---|---|---|---|---|---|---|---|")


# ================================================================ partes A

def parte_a1(d: dict, res: dict) -> None:
    print("\n## A1. Probit trimestral dentro de muestra (H1)\n")
    Sq, rq = d["Sq"], d["usrecq"]
    print("Ventana principal: origen q en [1959T1, 1995T1 - k] (spread y recesion dentro de 1959T1-1995T1). "
          "Spread = GS10 - BEY(TB3MS), promedio trimestral. t NW con k-1 rezagos (k=1: White).\n")
    print("| k | n | n recesión | a | b | pseudo R² | Artículo R² | t MV | t NW(k-1) | t NW(k) | Artículo t | "
          "R² ventana objetivo | t NW(k-1) ventana objetivo | R² spread descuento |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    tabla = {}
    for k in range(1, 9):
        qs = range(Q_INI, Q_FIN - k + 1)
        aj = probit_mv([Sq[q] for q in qs], [rq[q + k] for q in qs], rezagos_nw=(k - 1, k))
        qs2 = range(Q_INI - k, Q_FIN - k + 1)
        aj2 = probit_mv([Sq[q] for q in qs2], [rq[q + k] for q in qs2], rezagos_nw=(k - 1,))
        aj3 = probit_mv([d["Sq_desc"][q] for q in qs], [rq[q + k] for q in qs])
        tabla[k] = {"n": aj["n"], "n1": aj["n1"], "a": aj["a"], "b": aj["b"], "r2": aj["r2"], "t_mv": aj["t_mv"],
                    "t_nw_km1": aj[f"t_nw{k - 1}"], "t_nw_k": aj[f"t_nw{k}"], "r2_obj": aj2["r2"],
                    "t_nw_obj": aj2[f"t_nw{k - 1}"], "r2_desc": aj3["r2"], "convergio": aj["convergio"]}
        print(f"| {k} | {aj['n']} | {aj['n1']} | {f4(aj['a'])} | {f4(aj['b'])} | {f4(aj['r2'], 3)} | "
              f"{PAPER_IN[k][0]} | {f4(aj['t_mv'], 2)} | {f4(aj[f't_nw{k - 1}'], 2)} | {f4(aj[f't_nw{k}'], 2)} | "
              f"{PAPER_IN[k][1]} | {f4(aj2['r2'], 3)} | {f4(aj2[f't_nw{k - 1}'], 2)} | {f4(aj3['r2'], 3)} |")
    res["A1"] = tabla
    # Contraste con Current Issues 1996 (1960T1-1995T1, k=4)
    print("\nContraste con Current Issues 1996 (k = 4, datos 1960T1-1995T1):\n")
    print("| Ventana | a | b | spread con p=10% | spread con p=50% | spread con p=90% |")
    print("|---|---|---|---|---|---|")
    ci = {}
    for nombre, qs in (("origen 1960T1 a 1994T1", range(qi(1960, 1), Q_FIN - 4 + 1)),
                       ("objetivo 1960T1 a 1995T1", range(qi(1960, 1) - 4, Q_FIN - 4 + 1))):
        aj = probit_mv([Sq[q] for q in qs], [rq[q + 4] for q in qs])
        fila = {u: (NORMAL.inv_cdf(u) - aj["a"]) / aj["b"] for u in (0.10, 0.50, 0.90)}
        ci[nombre] = {"a": aj["a"], "b": aj["b"], **{str(u): v for u, v in fila.items()}}
        print(f"| {nombre} | {f4(aj['a'])} | {f4(aj['b'])} | {f4(fila[0.10], 2)} | {f4(fila[0.50], 2)} | "
              f"{f4(fila[0.90], 2)} |")
    print(f"| Current Issues 1996 (tabla) | -0.6651 (implícito) | -0.8111 (implícito) | {CI96_SPREAD[0.10]} | "
          f"{CI96_SPREAD[0.50]} | {CI96_SPREAD[0.90]} |")
    res["A1_CI96"] = ci


def parte_a2(d: dict, res: dict) -> None:
    print("\n## A2. Probit trimestral fuera de muestra al estilo del artículo (H2)\n")
    print("Objetivos tau en [1971T1, 1995T1]; origen q = tau - k; estimacion con s >= 1959T1 y s + k <= q "
          "(cronologia final). L_c ex post = constante con la frecuencia de la ventana evaluada.\n")
    Sq, rq = d["Sq"], d["usrecq"]
    print("| k | n | n recesión | pseudo R² (L_c ex post) | Artículo | pseudo R² (L_c recursiva) | Brier | "
          "Brier clima recursiva | AUC | fallos / no convergió |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    tabla = {}
    for k in range(1, 9):
        filas = []
        for tau in range(Q_OOS_INI, Q_FIN + 1):
            q = tau - k
            xs = [Sq[s] for s in range(Q_INI, q - k + 1)]
            ys = [rq[s + k] for s in range(Q_INI, q - k + 1)]
            aj = probit_mv(xs, ys)
            clim = sum(ys) / len(ys)
            p = clim if aj is None else cdf(aj["a"] + aj["b"] * Sq[q])
            filas.append({"origen": q, "p": p, "clim": clim, "y": rq[tau], "fallo": aj is None,
                          "noconv": aj is not None and not aj["convergio"]})
        e = evaluar(filas)
        tabla[k] = e
        print(f"| {k} | {e['n']} | {e['n1']} | {f4(e['r2_expost'], 3)} | {PAPER_OUT[k]} | {f4(e['r2_recursiva'], 3)} | "
              f"{f4(e['brier'])} | {f4(e['brier_clima_rec'])} | {f4(e['auc'])} | {e['fallos_probit']} / {e['no_convergio']} |")
    res["A2"] = tabla


def parte_a3(d: dict, giros: list, res: dict) -> dict:
    print("\n## A3. Probit mensual, recesión 12 meses adelante (H3)\n")
    S, usrec = d["S"], d["usrec"]
    ult_rec = max(usrec)
    ult_origen = min(ult_rec - H, d["s_fin"])
    print(f"Ultimo USREC: {et(ult_rec)}; ultimo origen evaluable: {et(ult_origen)}. Spread = GS10 - BEY(TB3MS).\n")
    # dentro de muestra
    print("### A3.1 Dentro de muestra\n")
    print("| Ventana de origen | n | n recesión | a | b | pseudo R² | t MV | t NW(11) | t NW(12) |")
    print("|---|---|---|---|---|---|---|---|---|")
    dentro = {}
    for nombre, (m0, m1) in (("1959-01 a 1994-03 (era del artículo)", (INICIO_EST, M_FIN_EM)),
                             (f"1959-01 a {et(ult_origen)} (muestra completa)", (INICIO_EST, ult_origen)),
                             (f"1998-03 a {et(ult_origen)} (solo post-publicación)", (OOS_POST_INI, ult_origen))):
        ks = range(m0, m1 + 1)
        aj = probit_mv([S[k] for k in ks], [usrec[k + H] for k in ks], rezagos_nw=(NW_MENSUAL, 12))
        dentro[nombre] = {"n": aj["n"], "n1": aj["n1"], "a": aj["a"], "b": aj["b"], "r2": aj["r2"],
                          "t_mv": aj["t_mv"], "t_nw11": aj["t_nw11"], "t_nw12": aj["t_nw12"],
                          "spread_p50": -aj["a"] / aj["b"]}
        print(f"| {nombre} | {aj['n']} | {aj['n1']} | {f4(aj['a'])} | {f4(aj['b'])} | {f4(aj['r2'], 3)} | "
              f"{f4(aj['t_mv'], 2)} | {f4(aj['t_nw11'], 2)} | {f4(aj['t_nw12'], 2)} |")
    res["A3_dentro"] = dentro
    ks = range(INICIO_EST, M_FIN_EM + 1)
    aj_em = probit_mv([S[k] for k in ks], [usrec[k + H] for k in ks])
    coef_em = {"a": aj_em["a"], "b": aj_em["b"], "clima": aj_em["n1"] / aj_em["n"]}
    # fuera de muestra
    print("\n### A3.2 Fuera de muestra (estimación recursiva; objetivo evaluado con la cronología final de hoy)\n")
    print(ENCABEZADO_EVAL)
    evals, series = {}, {}
    casos = [
        ("era 1970-01 a 1998-02, cronología final", range(OOS_ERA[0], OOS_ERA[1] + 1), "final", None),
        ("era 1970-01 a 1998-02, tiempo real", range(OOS_ERA[0], OOS_ERA[1] + 1), "rt", None),
        (f"post 1998-03 a {et(ult_origen)}, tiempo real (PRINCIPAL H3)", range(OOS_POST_INI, ult_origen + 1), "rt", None),
        (f"post 1998-03 a {et(ult_origen)}, cronología final", range(OOS_POST_INI, ult_origen + 1), "final", None),
        (f"post 1998-03 a {et(ult_origen)}, coeficientes fijos 1959-01 a 1994-03",
         range(OOS_POST_INI, ult_origen + 1), "fijo", coef_em),
        ("post 1998-03 a 2024-02, tiempo real (sensibilidad)", range(OOS_POST_INI, OOS_POST_FIN_SENS + 1), "rt", None),
        ("post 1998-03 a 2021-10, tiempo real (sin el episodio 2022-2024 como origen)",
         range(OOS_POST_INI, mi(2021, 10) + 1), "rt", None),
    ]
    for nombre, origenes, modo, coef in casos:
        filas = pronosticos_mensuales(origenes, S, usrec, giros, modo, coef)
        e = evaluar(filas)
        evals[nombre] = e
        series[nombre] = filas
        print(linea_eval(nombre, e))
    res["A3_fuera"] = evals
    res["A3_coef_em"] = coef_em
    # veredicto H3
    principal = evals[f"post 1998-03 a {et(ult_origen)}, tiempo real (PRINCIPAL H3)"]
    r2, br, brc = principal["r2_expost"], principal["brier"], principal["brier_clima_rec"]
    if r2 > 0 and br < brc:
        v = "SE SOSTIENE (pseudo R2 > 0 y Brier < clima recursiva)"
    elif r2 <= 0 and br >= brc:
        v = "REFUTADA (pseudo R2 <= 0 y Brier >= clima recursiva)"
    else:
        v = "MIXTO"
    print(f"\nVeredicto mecanico H3: {v} (pseudo R2 {f4(r2)}, Brier {f4(br)} vs clima {f4(brc)})")
    res["H3_veredicto"] = v
    # probabilidades por ano (post, tiempo real)
    filas = series[f"post 1998-03 a {et(ult_origen)}, tiempo real (PRINCIPAL H3)"]
    print("\nProbabilidad en tiempo real (origen) y recesion 12 meses despues (final), resumen por episodio:\n")
    print("| Origen | P(recesión en 12 m) | S del origen | USREC del objetivo |")
    print("|---|---|---|---|")
    for f in filas:
        if f["origen"] % 6 == 0 or f["p"] > 0.3:
            print(f"| {et(f['origen'])} | {f4(f['p'], 3)} | {f4(S[f['origen']], 2)} | {f['y']} |")
    return {"series": series, "coef_em": coef_em, "ult_origen": ult_origen}


def verificar_alfred(d: dict, giros: list, res: dict) -> None:
    print("\n## Verificación con ALFRED\n")
    print("### Revisiones de GS10 y TB3MS (vintage contra serie actual de FRED)\n")
    print("| Serie | Vintage pedido | n comunes | n distintos (>1e-9) | diferencia máxima |")
    print("|---|---|---|---|---|")
    rev = []
    hoy = date(2026, 9, 24)
    for serie, actual in (("GS10", d["gs10"]), ("TB3MS", d["tb3"])):
        for v in ("1996-12-31", "1998-02-27", "2000-01-15", "2008-12-31", "2020-06-30", hoy.isoformat()):
            try:
                vint = dh.alfred(serie, v)
            except ErrorDatos as e:
                print(f"| {serie} | {v} | sin vintage | - | {str(e)[:60]} |")
                rev.append({"serie": serie, "vintage": v, "error": str(e)[:120]})
                continue
            comunes = [(mi_de(f), x) for f, x in vint if mi_de(f) in actual]
            difs = [abs(x - actual[k]) for k, x in comunes]
            nd = sum(1 for x in difs if x > 1e-9)
            mx = max(difs) if difs else None
            print(f"| {serie} | {v} | {len(comunes)} | {nd} | {f4(mx, 4)} |")
            rev.append({"serie": serie, "vintage": v, "n": len(comunes), "n_distintos": nd, "max_dif": mx})
    res["alfred_revisiones"] = rev
    print("\n### Etiquetas de recesión en tiempo real (anuncios del NBER) contra vintages de USREC en ALFRED\n")
    print("| Fecha | último mes del vintage | meses comparados (1959-01 en adelante) | discrepancias | ejemplos |")
    print("|---|---|---|---|---|")
    fechas = [date(a, 12, 31) for a in range(2014, 2026)] + [date(2020, 6, 5), date(2020, 6, 10),
                                                            date(2021, 7, 16), date(2021, 7, 21), hoy]
    chk = []
    for D in sorted(fechas):
        try:
            vint = dh.alfred("USREC", D)
        except ErrorDatos as e:
            print(f"| {D} | sin vintage | - | - | {str(e)[:50]} |")
            continue
        vm = {mi_de(f): int(x) for f, x in vint}
        ultimo = max(vm)
        rec = etiquetas_rt_en(D, giros, m_hasta=max(ultimo, mi_de(D)))
        meses = [k for k in range(INICIO_EST, min(ultimo, mi_de(D)) + 1)]
        disc = [k for k in meses if (1 if k in rec else 0) != vm[k]]
        ej = ", ".join(f"{et(k)} (ALFRED {vm[k]})" for k in disc[:4])
        print(f"| {D} | {et(ultimo)} | {len(meses)} | {len(disc)} | {ej} |")
        chk.append({"fecha": D.isoformat(), "ultimo": et(ultimo), "n": len(meses), "discrepancias": len(disc),
                    "ejemplos": [et(k) for k in disc[:10]]})
    res["alfred_usrec"] = chk


def parte_a4(d: dict, a3: dict, giros: list, res: dict) -> None:
    print("\n## A4. El episodio 2022-2024 (H4)\n")
    S, t10, usrec = d["S"], d["t10_mens"], d["usrec"]
    inv = [k for k in range(mi(2022, 1), d["s_fin"] + 1) if S[k] < 0]
    inv_t10 = [k for k in sorted(t10) if k >= mi(2022, 1) and t10[k] < 0]
    print(f"Meses con S = GS10 - BEY(TB3MS) < 0 desde 2022-01: {len(inv)}: "
          + ", ".join(f"{et(k)} ({S[k]:+.2f})" for k in inv))
    print(f"\nMeses con promedio mensual de T10Y3M < 0 desde 2022-01: {len(inv_t10)}: "
          + ", ".join(f"{et(k)} ({t10[k]:+.2f})" for k in inv_t10))
    # rachas diarias
    serie = d["t10y3m"]
    rachas, actual = [], []
    for f, v in serie:
        if v < 0:
            actual.append((f, v))
        elif actual:
            rachas.append(actual)
            actual = []
    if actual:
        rachas.append(actual)
    rachas.sort(key=len, reverse=True)
    print("\nRachas de sesiones consecutivas con T10Y3M diario < 0 (observaciones con dato; las 5 más largas):\n")
    print("| Inicio | Fin | Sesiones | Mínimo | Fecha del mínimo |")
    print("|---|---|---|---|---|")
    top = []
    for r in rachas[:5]:
        fmin, vmin = min(r, key=lambda x: x[1])
        print(f"| {r[0][0]} | {r[-1][0]} | {len(r)} | {vmin:+.2f} | {fmin} |")
        top.append({"inicio": r[0][0].isoformat(), "fin": r[-1][0].isoformat(), "sesiones": len(r),
                    "minimo": vmin, "fecha_minimo": fmin.isoformat()})
    ult_t10 = serie[-1]
    print(f"\nÚltimo T10Y3M diario: {ult_t10[0]} = {ult_t10[1]:+.2f}")
    # resultado segun USREC
    if inv:
        v0, v1 = inv[0] + 1, min(inv[-1] + H, max(usrec))
        unos = [k for k in range(v0, v1 + 1) if usrec.get(k) == 1]
        print(f"\nVentana de verificación (USREC de FRED hoy): {et(v0)} a {et(v1)} "
              f"(la ventana completa llegaría a {et(inv[-1] + H)}); meses con USREC = 1: {len(unos)}")
        picos_post = [k for f, t, k in giros if t == "pico" and k > mi(2020, 4)]
        print(f"Picos del NBER posteriores a abr-2020 en la tabla de anuncios: {len(picos_post)}")
        fp = (len(unos) == 0 and not picos_post)
        print(f"Veredicto mecánico H4: {'FALSO POSITIVO (a la fecha)' if fp else 'NO es falso positivo'}")
        res["A4"] = {"meses_invertidos": [et(k) for k in inv], "meses_invertidos_t10": [et(k) for k in inv_t10],
                     "ventana": [et(v0), et(v1)], "usrec_unos": len(unos), "falso_positivo": fp,
                     "rachas_t10": top, "ultimo_t10": [ult_t10[0].isoformat(), ult_t10[1]]}
    # probabilidades en tiempo real
    filas = [f for f in pronosticos_mensuales(range(mi(2021, 1), d["s_fin"] + 1 - 0), S, usrec | {
        k: 0 for k in range(max(usrec) + 1, d["s_fin"] + H + 1)}, giros, "rt")]
    print("\nProbabilidad en tiempo real P(recesión en 12 m) por origen, 2021-01 en adelante "
          "(el 'y' de orígenes posteriores a " + et(a3["ult_origen"]) + " aún no se conoce):\n")
    print("| Origen | S | T10Y3M prom. mensual | P tiempo real | P coef. fijos 1959-1994 | USREC objetivo |")
    print("|---|---|---|---|---|---|")
    ce = a3["coef_em"]
    pmax = max(filas, key=lambda f: f["p"])
    for f in filas:
        k = f["origen"]
        yobj = usrec.get(k + H, "desconocido")
        print(f"| {et(k)} | {S[k]:+.2f} | {f4(t10.get(k), 2)} | {f4(f['p'], 3)} | "
              f"{f4(cdf(ce['a'] + ce['b'] * S[k]), 3)} | {yobj} |")
    n50 = sum(1 for f in filas if f["origen"] <= mi(2025, 12) and f["p"] > 0.5)
    n30 = sum(1 for f in filas if f["origen"] <= mi(2025, 12) and f["p"] > 0.3)
    print(f"\nMáximo P tiempo real: {f4(pmax['p'], 3)} en {et(pmax['origen'])}; meses con P > 0.5: {n50}; "
          f"con P > 0.3: {n30} (orígenes 2021-01 a 2025-12)")
    ult = filas[-1]
    # probabilidad actual con T10Y3M del mes en curso
    m_hoy = max(t10)
    rec = etiquetas_rt_en(date(2026, 9, 24), giros, m_hasta=d["s_fin"])
    _, _, aj = prob_origen(d["s_fin"], S, lambda k: 1 if k in rec else 0)
    p_t10 = cdf(aj["a"] + aj["b"] * t10[m_hoy])
    print(f"\nProbabilidad actual (origen {et(ult['origen'])}, S = {S[ult['origen']]:+.2f}): {f4(ult['p'], 3)} en tiempo real; "
          f"{f4(cdf(ce['a'] + ce['b'] * S[ult['origen']]), 3)} con coeficientes 1959-1994. Con el promedio de "
          f"T10Y3M de {et(m_hoy)} ({d['t10_dias_mes'][m_hoy]} sesiones, {t10[m_hoy]:+.2f}) en el mismo modelo: {f4(p_t10, 3)}")
    res["A4_prob"] = {"max": pmax["p"], "mes_max": et(pmax["origen"]), "n_mayor_05": n50, "n_mayor_03": n30,
                      "actual_origen": et(ult["origen"]), "actual_S": S[ult["origen"]], "actual_p_rt": ult["p"],
                      "actual_p_fijo": cdf(ce["a"] + ce["b"] * S[ult["origen"]]), "t10_mes": et(m_hoy),
                      "t10_valor": t10[m_hoy], "p_con_t10": p_t10,
                      "serie": [(et(f["origen"]), f["p"]) for f in filas]}


def parte_a5(d: dict, res: dict) -> None:
    print("\n## A5. Rendimiento del mercado de EUA después del inicio de una inversión (H5)\n")
    S, usrec = d["S"], d["usrec"]
    mer = {mi_de(f): r for f, r in d["mercado"]}
    rf = {mi_de(f): r for f, r in d["rf"]}
    ult = max(mer)
    k0 = d["s_ini"] + 12
    eventos = [m for m in range(k0, d["s_fin"] + 1)
               if S[m] < 0 and all(S[j] >= 0 for j in range(m - 12, m))]
    picos = [k for t, k in giros_de_usrec(usrec) if t == "pico"]

    def acum(m: int, h: int, serie: dict) -> float | None:
        if m + h > ult:
            return None
        return math.prod(1 + serie[j] for j in range(m + 1, m + h + 1)) - 1

    def mdd_y_pico(m: int, h: int = 24):
        nivel, maximo, mdd, idx_max, val_max = 1.0, 1.0, 0.0, 0, 1.0
        fin = min(m + h, ult)
        for i, j in enumerate(range(m + 1, fin + 1), start=1):
            nivel *= 1 + mer[j]
            maximo = max(maximo, nivel)
            mdd = min(mdd, nivel / maximo - 1)
            if nivel > val_max:
                val_max, idx_max = nivel, i
        return mdd, idx_max, fin - m

    print("Inicio = primer mes con S < 0 tras >= 12 meses con S >= 0. Rendimiento compuesto de French (Mkt-RF+RF) "
          "desde el mes siguiente al inicio.\n")
    print("| Inicio | S | 6 m | 12 m | 18 m | 24 m | exceso 12 m | MDD en 24 m | meses al máximo (24 m) | "
          "meses hasta el pico NBER |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    ev_out = []
    for m in eventos:
        r = {h: acum(m, h, mer) for h in (6, 12, 18, 24)}
        rf12 = acum(m, 12, rf)
        ex12 = None if r[12] is None else r[12] - rf12
        mdd, imax, meses = mdd_y_pico(m)
        pico = next((p for p in picos if p >= m), None)
        dist = None if pico is None else pico - m
        print(f"| {et(m)} | {S[m]:+.2f} | {pct(r[6])} | {pct(r[12])} | {pct(r[18])} | {pct(r[24])} | {pct(ex12)} | "
              f"{pct(mdd)} (en {meses} m) | {imax} | {'ninguno' if dist is None else dist} |")
        ev_out.append({"inicio": et(m), "S": S[m], **{f"r{h}": r[h] for h in r}, "exceso12": ex12, "mdd24": mdd,
                       "meses_al_maximo": imax, "meses_a_pico": dist})
    print("\n| Horizonte | n eventos | media eventos | mediana eventos | eventos > 0 | n ventanas incond. | "
          "media incond. | desv. est. incond. | t aprox. |")
    print("|---|---|---|---|---|---|---|---|---|")
    resumen = {}
    for h in (6, 12, 18, 24):
        ev = [x[f"r{h}"] for x in ev_out if x[f"r{h}"] is not None]
        inc = [acum(m, h, mer) for m in range(k0, ult - h + 1)]
        mi_, sd = statistics.fmean(inc), statistics.stdev(inc)
        me = statistics.fmean(ev)
        t = (me - mi_) / (sd / math.sqrt(len(ev)))
        resumen[h] = {"n": len(ev), "media": me, "mediana": statistics.median(ev), "positivos": sum(1 for x in ev if x > 0),
                      "n_inc": len(inc), "media_inc": mi_, "sd_inc": sd, "t": t}
        print(f"| {h} m | {len(ev)} | {pct(me)} | {pct(statistics.median(ev))} | {sum(1 for x in ev if x > 0)} | "
              f"{len(inc)} | {pct(mi_)} | {pct(sd)} | {f4(t, 2)} |")
    r12 = resumen[12]
    ver = "REFUTADA mi expectativa (menor, t <= -2)" if r12["t"] <= -2 else "se sostiene mi expectativa (no significativamente menor)"
    print(f"\nVeredicto mecanico H5 (12 m): {ver}")
    res["A5"] = {"eventos": ev_out, "resumen": resumen, "veredicto": ver}


# ================================================================ parte B: motor

def tabla_motor(resultados: list, segmento: str) -> None:
    print(f"\n### Segmento `{segmento}`\n")
    x0 = resultados[0].metricas[segmento]
    print(f"{x0['fecha_inicio']} a {x0['fecha_fin']}, n = {x0['n_periodos']}\n")
    print("| Variante | CAGR | Vol | Sharpe | Sortino | MDD | Calmar | Exposición media | Rotación anual | "
          "Costo anual | Cambios de señal |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in resultados:
        x = r.metricas[segmento]
        print(f"| {r.variante} | {pct(x['cagr'])} | {pct(x['vol_anual'])} | {f4(x['sharpe'])} | {f4(x['sortino'])} | "
              f"{pct(x['mdd'])} | {f4(x['calmar'])} | {f4(x['exposicion_media'], 3)} | {f4(x['rotacion_anual'], 3)} | "
              f"{pct(x['costo_anual'], 3)} | {x['n_cambios_senal']} |")


def rend_ventana(r, f0: date, f1: date) -> float | None:
    vals = [rn for f, rn in zip(r.fechas, r.r_neto) if f0 < f <= f1]
    return math.prod(1 + v for v in vals) - 1 if vals else None


def parte_b(d: dict, giros: list, res: dict) -> None:
    print("\n## B. Reglas operables en el motor (H6)\n")
    mercado, rf = d["mercado"], d["rf"]
    fechas = [f for f, _ in mercado]
    minh = fechas.index(PRIMERA_DECISION)
    ext = {"spread": [(fdm(k), v) for k, v in sorted(d["S"].items())],
           "pico": [(f, float(k)) for f, t, k in giros if t == "pico"],
           "valle": [(f, float(k)) for f, t, k in giros if t == "valle"]}
    ext_desc = dict(ext, spread=[(fdm(k), v) for k, v in sorted(d["S_desc"].items())])
    fuente = (f"French CRSP {d['fr']['version_crsp']} (Mkt-RF+RF, RF); FRED GS10, TB3MS (BEY), USREC; "
              f"anuncios NBER; descarga {datetime.now(timezone.utc).date()}")
    comunes = dict(id_replica=ID_REG, min_historia=minh, cortes=[CORTE], extras=ext, fuente_datos=fuente)
    print(f"min_historia = {minh} (primera decision {fechas[minh]}); corte {CORTE}.\n")
    base = []
    for nombre, senal, desc in VARIANTES:
        r = bt.backtest_senal(mercado, rf, senal, variante=nombre, es_prueba=True,
                              parametros={"regla": desc, "spread": "GS10-BEY(TB3MS)", "horizonte_meses": H},
                              nota="prueba pre-registrada, costos por defecto", **comunes)
        base.append(r)
    simples = [
        bt.backtest_senal(mercado, rf, bt.senal_comprar_y_mantener, variante="comprar_y_mantener", es_prueba=False,
                          nota="regla sencilla", **comunes),
        bt.backtest_senal(mercado, rf, bt.senal_efectivo, variante="efectivo", es_prueba=False,
                          nota="regla sencilla", **comunes),
        bt.backtest_senal(mercado, rf, bt.senal_media_movil(10), variante="sma10", es_prueba=False,
                          nota="regla sencilla", **comunes),
    ]
    todos = base + simples
    for seg in ("completo", "dentro_muestra", "fuera_muestra"):
        tabla_motor(todos, seg)
    # seleccion y veredictos
    elegida = max(base, key=lambda r: r.metricas["dentro_muestra"]["sharpe"])
    bh, sma = simples[0], simples[2]
    fo, fb, fs = (elegida.metricas["fuera_muestra"], bh.metricas["fuera_muestra"], sma.metricas["fuera_muestra"])
    do, db = elegida.metricas["dentro_muestra"], bh.metricas["dentro_muestra"]
    vs_bh = fo["sharpe"] > fb["sharpe"] and abs(fo["mdd"]) < abs(fb["mdd"])
    vs_sma = vs_bh and fo["sharpe"] > fs["sharpe"] and abs(fo["mdd"]) < abs(fs["mdd"])
    refuta_sharpe = fo["sharpe"] <= fb["sharpe"]
    refuta_freno = not (abs(fo["mdd"]) < abs(fb["mdd"])) and not (abs(do["mdd"]) < abs(db["mdd"]))
    print(f"\nVariante elegida dentro de muestra (mayor Sharpe neto): {elegida.variante} "
          f"(Sharpe dentro {f4(do['sharpe'])} vs comprar y mantener {f4(db['sharpe'])})")
    print(f"Fuera de muestra: Sharpe {f4(fo['sharpe'])} vs C&M {f4(fb['sharpe'])} vs SMA10 {f4(fs['sharpe'])}; "
          f"MDD {pct(fo['mdd'])} vs C&M {pct(fb['mdd'])} vs SMA10 {pct(fs['mdd'])}")
    print(f"Agrega valor frente a C&M: {vs_bh}; frente a la regla sencilla: {vs_sma}; "
          f"H6 refutada (Sharpe fuera <= C&M): {refuta_sharpe}; uso como freno refutado: {refuta_freno}")
    # DSR
    print("\n### DSR (Bailey y López de Prado) desde el registro\n")
    print("| Lectura | segmento | variante | DSR | cumple 0.95 | N | V (SR periodo) | SR anual | SR0 anual | n | "
          "PSR sin deflactar |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    dsr = {}
    if not HUMO:
        for nombre, kw in (("dentro_N_registrado", {}), ("dentro_N_conservador", {"n_pruebas": N_CONSERVADOR}),
                           ("fuera_N_registrado", {"segmento": "fuera_muestra", "variante": elegida.variante}),
                           ("fuera_N_conservador", {"segmento": "fuera_muestra", "variante": elegida.variante,
                                                    "n_pruebas": N_CONSERVADOR})):
            x = bt.sharpe_deflactado_de_registro(ID, **kw)
            dsr[nombre] = x
            print(f"| {nombre} | {x['segmento']} | {x['variante']} | {f4(x['dsr'])} | {x['cumple']} | {x['n_pruebas']} | "
                  f"{f4(x['varianza_sharpes_periodo'], 6)} | {f4(x['sr_anual'])} | {f4(x['sr0_anual'])} | {x['n_obs']} | "
                  f"{f4(x['psr_sin_deflactar'])} |")
    # ventanas descriptivas
    print("\n### Rendimiento neto en ventanas descriptivas (no pre-registradas; ver desviaciones)\n")
    ventanas = [("2000-03 a 2002-09", date(2000, 2, 29), date(2002, 9, 30)),
                ("2007-10 a 2009-02", date(2007, 9, 30), date(2009, 2, 28)),
                ("2019-06 a 2020-12", date(2019, 5, 31), date(2020, 12, 31)),
                ("2022-11 a 2024-12", date(2022, 10, 31), date(2024, 12, 31)),
                ("2025-01 a 2026-07", date(2024, 12, 31), date(2026, 7, 31))]
    print("| Variante | " + " | ".join(v[0] for v in ventanas) + " |")
    print("|---|" + "---|" * len(ventanas))
    vent = {}
    for r in todos:
        vals = [rend_ventana(r, a, b) for _, a, b in ventanas]
        vent[r.variante] = vals
        print(f"| {r.variante} | " + " | ".join(pct(v) for v in vals) + " |")
    # sensibilidades de costos
    print("\n### Sensibilidad de costos (es_prueba=False)\n")
    print("| Variante | Escenario | Sharpe dentro | Sharpe fuera | MDD fuera | CAGR fuera | Costo anual fuera |")
    print("|---|---|---|---|---|---|---|")
    sens = {}
    for escenario, com, spr in (("spread_medio", bt.COMISION_GBM_POR_LADO, bt.SPREAD_POR_LADO["medio"]),
                                ("bruto", 0.0, 0.0)):
        for (nombre, senal, desc) in VARIANTES + [("comprar_y_mantener", bt.senal_comprar_y_mantener, "C&M"),
                                                  ("sma10", bt.senal_media_movil(10), "SMA10")]:
            r = bt.backtest_senal(mercado, rf, senal, variante=nombre, es_prueba=False, comision_por_lado=com,
                                  spread_por_lado=spr, parametros={"regla": desc, "escenario": escenario},
                                  nota=f"sensibilidad de costos: {escenario}", **comunes)
            x, y = r.metricas["dentro_muestra"], r.metricas["fuera_muestra"]
            sens[f"{nombre}|{escenario}"] = {"sharpe_dentro": x["sharpe"], "sharpe_fuera": y["sharpe"],
                                             "mdd_fuera": y["mdd"], "cagr_fuera": y["cagr"]}
            print(f"| {nombre} | {escenario} | {f4(x['sharpe'])} | {f4(y['sharpe'])} | {pct(y['mdd'])} | "
                  f"{pct(y['cagr'])} | {pct(y['costo_anual'], 3)} |")
    # spread en base descuento
    print("\n### Sensibilidad: spread con T-bill en base descuento (GS10 - TB3MS)\n")
    print("| Variante | Sharpe dentro | MDD dentro | Sharpe fuera | MDD fuera | Cambios de señal |")
    print("|---|---|---|---|---|---|")
    comunes_desc = dict(comunes, extras=ext_desc)
    for nombre, senal, desc in VARIANTES[:3]:
        r = bt.backtest_senal(mercado, rf, senal, variante=nombre, es_prueba=False,
                              parametros={"regla": desc, "spread": "GS10-TB3MS (descuento)"},
                              nota="sensibilidad: spread en base descuento", **comunes_desc)
        x, y = r.metricas["dentro_muestra"], r.metricas["fuera_muestra"]
        sens[f"{nombre}|descuento"] = {"sharpe_dentro": x["sharpe"], "sharpe_fuera": y["sharpe"], "mdd_fuera": y["mdd"]}
        print(f"| {nombre} | {f4(x['sharpe'])} | {pct(x['mdd'])} | {f4(y['sharpe'])} | {pct(y['mdd'])} | "
              f"{r.metricas['completo']['n_cambios_senal']} |")
    # MXN
    print("\n### Sensibilidad en MXN (DEXMXUS; RF en USD convertida; es_prueba=False)\n")
    mx = []
    for nombre, senal in ((elegida.variante, dict((v[0], v[1]) for v in VARIANTES)[elegida.variante]),
                          ("comprar_y_mantener", bt.senal_comprar_y_mantener), ("sma10", bt.senal_media_movil(10))):
        r = bt.backtest_senal(mercado, rf, senal, variante=nombre, es_prueba=False, fx=d["fx"],
                              parametros={"moneda": "MXN"}, nota="sensibilidad MXN (DEXMXUS)", **comunes)
        mx.append(r)
    for seg in ("dentro_muestra", "fuera_muestra"):
        tabla_motor(mx, seg)
    # verificacion cruzada: probit50 del motor contra el calculo externo
    r50 = base[[v[0] for v in VARIANTES].index("probit50")]
    S = d["S"]
    discrep, n_cmp = 0, 0
    for f, w in zip(r50.fechas, r50.exposicion):
        m = mi_de(f) - 1
        if m % 24 != 0 and m < mi(2019, 1):
            continue
        rec = etiquetas_rt_en(fdm(m), giros)
        p, _, _ = prob_origen(m, S, lambda k, rec=rec: 1 if k in rec else 0)
        n_cmp += 1
        if (0.0 if p > 0.5 else 1.0) != w:
            discrep += 1
    print(f"\nVerificación cruzada probit50 (motor vs cálculo externo) en {n_cmp} decisiones "
          f"(una cada 24 meses antes de 2019 y todas desde 2019): {discrep} discrepancias")
    res["B"] = {
        "elegida": elegida.variante,
        "metricas": {r.variante: {s: {k: (v.isoformat() if isinstance(v, date) else v)
                                      for k, v in r.metricas[s].items()}
                                  for s in ("completo", "dentro_muestra", "fuera_muestra")} for r in todos},
        "veredicto": {"vs_cym": vs_bh, "vs_sma10": vs_sma, "h6_refutada_sharpe": refuta_sharpe,
                      "freno_refutado": refuta_freno},
        "dsr": dsr, "ventanas": {k: v for k, v in vent.items()}, "sensibilidades": sens,
        "mxn": {r.variante: {s: {k: (v.isoformat() if isinstance(v, date) else v) for k, v in r.metricas[s].items()}
                             for s in ("dentro_muestra", "fuera_muestra")} for r in mx},
        "verificacion_probit50": {"n": n_cmp, "discrepancias": discrep},
        "huella_datos": base[0].meta["huella_datos"], "huella_mxn": mx[0].meta["huella_datos"],
        "registro": str(base[0].ruta_registro) if base[0].ruta_registro else None,
    }


# ================================================================ principal

def main() -> None:
    res: dict = {"fecha_corrida_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    d = cargar()
    fr = d["fr"]
    print("# R07 - salida del script\n")
    print(f"Corrida: {res['fecha_corrida_utc']}")
    print(f"French F-F_Research_Data_Factors: CRSP {fr['version_crsp']}, sha256 {fr['sha256']}, "
          f"{fr['fechas'][0]} a {fr['fechas'][-1]}")
    for nota in fr.get("notas", [])[:6]:
        print(f"  nota French: {nota}")
    print(f"GS10 {et(min(d['gs10']))} a {et(max(d['gs10']))}; TB3MS {et(min(d['tb3']))} a {et(max(d['tb3']))}; "
          f"spread {et(d['s_ini'])} a {et(d['s_fin'])} ({len(d['S'])} meses)")
    print(f"USREC {et(min(d['usrec']))} a {et(max(d['usrec']))}; USRECQ {etq(min(d['usrecq']))} a {etq(max(d['usrecq']))}")
    print(f"T10Y3M diario {d['t10y3m'][0][0]} a {d['t10y3m'][-1][0]} ({len(d['t10y3m'])} obs); "
          f"DEXMXUS {d['fx'][0][0]} a {d['fx'][-1][0]}")
    res["datos"] = {"french_crsp": fr["version_crsp"], "french_sha256": fr["sha256"],
                    "spread": [et(d["s_ini"]), et(d["s_fin"])], "usrec_ultimo": et(max(d["usrec"])),
                    "usrecq_ultimo": etq(max(d["usrecq"])), "t10y3m_ultimo": d["t10y3m"][-1][0].isoformat(),
                    "dexmxus_ultimo": d["fx"][-1][0].isoformat()}
    # control del spread contra T10Y3M
    comunes = [k for k in d["t10_mens"] if k in d["S"] and k >= mi(1982, 1)]
    dif = [d["S"][k] - d["t10_mens"][k] for k in comunes]
    dif_desc = [d["S_desc"][k] - d["t10_mens"][k] for k in comunes]
    corr = statistics.correlation([d["S"][k] for k in comunes], [d["t10_mens"][k] for k in comunes])
    print(f"\nControl: S (BEY) - T10Y3M prom. mensual en {len(comunes)} meses ({et(min(comunes))} a {et(max(comunes))}): "
          f"media {statistics.fmean(dif):+.4f}, max |dif| {max(abs(x) for x in dif):.4f}, correlacion {corr:.5f}; "
          f"con base descuento: media {statistics.fmean(dif_desc):+.4f}")
    signos = sum(1 for k in comunes if (d["S"][k] < 0) != (d["t10_mens"][k] < 0))
    print(f"Meses con signo distinto entre S y T10Y3M: {signos}: "
          + ", ".join(f"{et(k)} (S {d['S'][k]:+.2f}, T10Y3M {d['t10_mens'][k]:+.2f})"
                      for k in comunes if (d["S"][k] < 0) != (d["t10_mens"][k] < 0)))
    res["control_spread"] = {"n": len(comunes), "media_dif": statistics.fmean(dif), "corr": corr,
                             "media_dif_desc": statistics.fmean(dif_desc), "meses_signo_distinto": signos}
    giros, notas = giros_con_disponibilidad(d["usrec"])
    print("\nGiros del NBER y fecha en que se consideran conocidos (1959 en adelante):")
    for f, t, k in giros:
        if k >= mi(1957, 1):
            print(f"  {t:5s} {et(k)} -> conocido {f}")
    for n_ in notas:
        print("  " + n_)
    verificar_alfred(d, giros, res)
    parte_a1(d, res)
    parte_a2(d, res)
    a3 = parte_a3(d, giros, res)
    parte_a4(d, a3, giros, res)
    parte_a5(d, res)
    parte_b(d, giros, res)
    # veredictos H1 y H2
    a1, a2 = res["A1"][4], res["A2"][4]
    if a1["b"] < 0 and abs(a1["t_nw_km1"]) >= 2 and 0.246 <= a1["r2"] <= 0.346:
        v1 = "Replicado"
    elif a1["b"] < 0 and abs(a1["t_nw_km1"]) >= 2:
        v1 = "Replicado con diferencias"
    else:
        v1 = "No replicado"
    r2o = a2["r2_expost"]
    v2 = "Replicado" if 0.245 <= r2o <= 0.345 else ("Replicado con diferencias" if r2o > 0 else "No replicado")
    print(f"\n## Veredictos mecánicos\n\nH1 (k=4, dentro): {v1} (pseudo R2 {f4(a1['r2'], 3)}, t NW {f4(a1['t_nw_km1'], 2)})")
    print(f"H2 (k=4, fuera 1971T1-1995T1): {v2} (pseudo R2 {f4(r2o, 3)})")
    print(f"H3: {res['H3_veredicto']}")
    print(f"H5: {res['A5']['veredicto']}")
    res["veredictos"] = {"H1": v1, "H2": v2, "H3": res["H3_veredicto"], "H4": res.get("A4", {}).get("falso_positivo"),
                         "H5": res["A5"]["veredicto"], "H6": res["B"]["veredicto"]}
    if not HUMO:
        with open(DIR / "R07-resultados.json", "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=1, default=str)


if __name__ == "__main__":
    if HUMO:
        sys.stdout = io.StringIO()
        try:
            main()
        finally:
            sys.stdout = sys.__stdout__
        print("humo: OK (sin registro y sin mostrar resultados)")
    else:
        with open(DIR / "R07-salida.txt", "w", encoding="utf-8") as salida:
            sys.stdout = Tee(sys.__stdout__, salida)
            try:
                main()
            finally:
                sys.stdout = sys.__stdout__
