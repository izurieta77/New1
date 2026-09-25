#!/usr/bin/env python3
"""R03 - Primas de factores de EUA antes y despues de su publicacion (McLean y Pontiff, 2016, JF 71(1):5-32).

Reproduce desde la raiz del repo:  python3 laboratorio/replicas/R03.py
Solo biblioteca estandar. Cada corrida del motor se agrega a laboratorio/replicas/R03-variantes.csv.
La salida completa queda tambien en laboratorio/replicas/R03-salida.txt y las cifras clave en
laboratorio/replicas/R03-resultados.json.

Bloques (ver el pre-registro en R03-primas-de-factores-pre-post-publicacion.md, secciones 1-9):
  A. Primas por tramo (pre-muestra / muestra original / fuera de muestra antes de publicar /
     post-publicacion) y por decada de SMB, HML, Mom, RMW y CMA; decaimiento agrupado estilo
     McLean-Pontiff (regresion con errores agrupados por mes + bootstrap de bloques de 12 meses).
  B. Crashes de momentum (peores meses, estado "oso" de Daniel-Moskowitz), drawdowns y
     "muerte del value" 2007-2020 y lo posterior; ventanas de 6 meses.
  C. Verificacion de cifras que el sistema ya publico en conocimiento/02 y conocimiento/03.
  D. Corridas del motor (herramientas/backtest.py): tenencia de cada factor (RF + F contra RF),
     combinacion 1/5 y control de crash de momentum (regla 7 del capitulo 02), con referencias,
     sensibilidades de costos y DSR.
"""
from __future__ import annotations

import io
import json
import math
import random
import statistics
import sys
from bisect import bisect_left, bisect_right
from datetime import date, datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from herramientas import backtest as bt  # noqa: E402
from herramientas import datos_historicos as dh  # noqa: E402
from herramientas import estadistica as est  # noqa: E402

# ================================================================ parametros pre-registrados
ID = "R03"
SEMILLA = 20260925
N_BOOT = 5000
BLOQUE = 12
REZAGOS_NW = 6
FIN_DATOS = date(2026, 7, 31)
MIN_DIAS_VOL = 15          # dias habiles minimos para la volatilidad de un mes
MIN_MESES_VOL = 60         # historia minima de volatilidades para el percentil 80
PERCENTIL_VOL = 0.80
MESES_OSO = 24             # estado "oso": mercado acumulado de 24 meses < 0 (Daniel-Moskowitz)
MIN_HISTORIA_MOM = 10      # familia MOM: primer mes evaluado 1927-11 (SMA10 necesita 10 meses)
CORTES_MOM = (date(2013, 3, 31), date(2016, 11, 30))  # fin de muestra DM; numero de la JFE
COSTO_DEFECTO = (bt.COMISION_GBM_POR_LADO, bt.SPREAD_POR_LADO["liquido"])
COSTO_MEDIO = (bt.COMISION_GBM_POR_LADO, bt.SPREAD_POR_LADO["medio"])

# Tramos de McLean-Pontiff (seccion 6 del pre-registro). "pub" es el corte: mes de publicacion
# incluido en el tramo anterior. "alt" es la fecha alternativa verificada (sensibilidad).
TRAMOS = {
    "SMB": {"is_ini": date(1936, 1, 31), "is_fin": date(1975, 12, 31), "pub": date(1981, 3, 31),
            "alt": date(1979, 6, 30), "articulo": "Banz (1981), JFE 9(1), mar-1981",
            "n": (480, 63, 544)},
    "HML": {"is_ini": date(1963, 7, 31), "is_fin": date(1990, 12, 31), "pub": date(1992, 6, 30),
            "alt": None, "articulo": "Fama-French (1992), JF 47(2), jun-1992", "n": (330, 18, 409)},
    "MOM": {"is_ini": date(1965, 1, 31), "is_fin": date(1989, 12, 31), "pub": date(1993, 3, 31),
            "alt": None, "articulo": "Jegadeesh-Titman (1993), JF 48(1), mar-1993", "n": (300, 39, 400)},
    "RMW": {"is_ini": date(1963, 7, 31), "is_fin": date(2013, 12, 31), "pub": date(2015, 4, 30),
            "alt": date(2014, 10, 31), "articulo": "Fama-French (2015), JFE 116(1), abr-2015",
            "n": (606, 16, 135)},
    "CMA": {"is_ini": date(1963, 7, 31), "is_fin": date(2013, 12, 31), "pub": date(2015, 4, 30),
            "alt": date(2014, 10, 31), "articulo": "Fama-French (2015), JFE 116(1), abr-2015",
            "n": (606, 16, 135)},
}
FACTORES = ("SMB", "HML", "MOM", "RMW", "CMA")
MP_POST, MP_OOS = 0.58, 0.26            # McLean-Pontiff (2016), resumen publicado
FF2015_T4 = {"SMB": (0.29, 2.31), "HML": (0.37, 3.20), "RMW": (0.25, 2.92), "CMA": (0.33, 4.07)}
DM_PEORES = ["1932-08", "1932-07", "2001-01", "2009-04", "1939-09", "1933-04", "2009-03", "2002-11",
             "1938-06", "2009-08", "1931-06", "1933-05", "2001-11", "2001-10", "1974-01"]
DM_PEORES_VAL = [-74.36, -60.98, -49.19, -45.52, -43.83, -43.14, -42.28, -37.04, -33.36, -30.54,
                 -29.72, -28.90, -25.31, -24.98, -24.04]

SALIDA = io.StringIO()
RESULTADOS: dict = {}


def p(*args) -> None:
    texto = " ".join(str(a) for a in args)
    print(texto)
    SALIDA.write(texto + "\n")


def ym(d: date) -> str:
    return f"{d.year:04d}-{d.month:02d}"


def fin_mes_previo(d: date) -> date:
    return dh.fin_de_mes(d.year - 1, 12) if d.month == 1 else dh.fin_de_mes(d.year, d.month - 1)


def fmt(x, dec=4) -> str:
    if x is None:
        return "NA"
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return "NA"
    return f"{x:.{dec}f}"


def pct(x, dec=2) -> str:
    return "NA" if x is None else f"{100 * x:.{dec}f}"


# ================================================================ datos

class Serie:
    """Serie mensual {fecha fin de mes: valor decimal} con fechas ordenadas."""

    def __init__(self, pares):
        pares = sorted(pares)
        self.fechas = [f for f, _ in pares]
        self.valores = [v for _, v in pares]
        self.mapa = dict(pares)

    def tramo(self, ini: date, fin: date) -> list[float]:
        i0 = bisect_left(self.fechas, ini)
        i1 = bisect_right(self.fechas, fin)
        return self.valores[i0:i1]

    def pares(self, ini: date | None = None, fin: date | None = None) -> list[tuple]:
        i0 = 0 if ini is None else bisect_left(self.fechas, ini)
        i1 = len(self.fechas) if fin is None else bisect_right(self.fechas, fin)
        return list(zip(self.fechas[i0:i1], self.valores[i0:i1]))


def verificar_tabla(t: dict, nombre: str, n_esperado: int, mensual: bool = True) -> None:
    fechas = t["fechas"]
    if n_esperado is not None and len(fechas) != n_esperado:
        raise SystemExit(f"{nombre}: {len(fechas)} filas, se esperaban {n_esperado}")
    if any(b <= a for a, b in zip(fechas, fechas[1:])):
        raise SystemExit(f"{nombre}: fechas no estrictamente crecientes")
    if mensual and any(f != dh.a_fin_de_mes(f) for f in fechas):
        raise SystemExit(f"{nombre}: hay fechas que no son fin de mes")
    if t["faltantes"]:
        raise SystemExit(f"{nombre}: {t['faltantes']} faltantes (-99.99/-999); el pre-registro espera 0")


def cargar() -> dict:
    f3 = dh.french("F-F_Research_Data_Factors", "mensual")
    fm = dh.french("F-F_Momentum_Factor", "mensual")
    f5 = dh.french("F-F_Research_Data_5_Factors_2x3", "mensual")
    fd = dh.french("F-F_Research_Data_Factors_daily", "diaria")
    verificar_tabla(f3, "F-F_Research_Data_Factors", 1201)
    verificar_tabla(fm, "F-F_Momentum_Factor", 1195)
    verificar_tabla(f5, "F-F_Research_Data_5_Factors_2x3", 757)
    verificar_tabla(fd, "F-F_Research_Data_Factors_daily", None, mensual=False)
    for t, nombre in ((f3, "3F"), (fm, "Mom"), (f5, "5F")):
        tablas = t.get("tablas_en_archivo", [])
        if not any(fr == "anual" for _, fr, _ in tablas) or t["fechas"][-1] != FIN_DATOS:
            raise SystemExit(f"{nombre}: formato inesperado (tablas {tablas}, ultima fecha {t['fechas'][-1]})")
    p("## Datos (French, cache local en datos/cache/french/)\n")
    p("| Archivo | Rango | Filas | Columnas | Version CRSP | sha256 | Tablas en el archivo |")
    p("|---|---|---|---|---|---|---|")
    for nombre, t in (("F-F_Research_Data_Factors", f3), ("F-F_Momentum_Factor", fm),
                      ("F-F_Research_Data_5_Factors_2x3", f5), ("F-F_Research_Data_Factors_daily", fd)):
        p(f"| {nombre} | {t['fechas'][0]} a {t['fechas'][-1]} | {len(t['fechas'])} | "
          f"{', '.join(t['columnas'])} | {t['version_crsp']} | `{t['sha256']}` | "
          f"{'; '.join(f'{a} ({b}, {c})' for a, b, c in t.get('tablas_en_archivo', []))} |")
    p("")
    RESULTADOS["datos"] = {n: {"version_crsp": t["version_crsp"], "sha256": t["sha256"],
                               "inicio": str(t["fechas"][0]), "fin": str(t["fechas"][-1]), "filas": len(t["fechas"])}
                           for n, t in (("3F", f3), ("Mom", fm), ("5F", f5), ("diario", fd))}
    s = {
        "MKT": Serie(dh.columna(f3, "Mkt-RF")), "RF": Serie(dh.columna(f3, "RF")),
        "SMB": Serie(dh.columna(f3, "SMB")), "HML": Serie(dh.columna(f3, "HML")),
        "MOM": Serie(dh.columna(fm, "Mom")),
        "RMW": Serie(dh.columna(f5, "RMW")), "CMA": Serie(dh.columna(f5, "CMA")),
        "SMB5": Serie(dh.columna(f5, "SMB")), "HML5": Serie(dh.columna(f5, "HML")),
        "MKT5": Serie(dh.columna(f5, "Mkt-RF")), "RF5": Serie(dh.columna(f5, "RF")),
    }
    s["MKT_TOTAL"] = Serie([(f, s["MKT"].mapa[f] + s["RF"].mapa[f]) for f in s["MKT"].fechas])
    # diagnostico de consistencia entre archivos (no cambia datos)
    comunes = [f for f in s["RF5"].fechas if f in s["RF"].mapa]
    dif_rf = max(abs(s["RF5"].mapa[f] - s["RF"].mapa[f]) for f in comunes)
    dif_mkt = max(abs(s["MKT5"].mapa[f] - s["MKT"].mapa[f]) for f in comunes)
    p(f"Consistencia 3F vs 5F en {len(comunes)} meses comunes: max |RF5-RF3| = {dif_rf:.6f}; "
      f"max |MktRF5-MktRF3| = {dif_mkt:.6f} (decimales).")
    # volatilidad mensual de Mkt-RF diario (se usa como extra en la familia MOM)
    por_mes: dict = {}
    for f, v in dh.columna(fd, "Mkt-RF"):
        por_mes.setdefault((f.year, f.month), []).append(v)
    vol = [(dh.fin_de_mes(a, m), statistics.stdev(x)) for (a, m), x in sorted(por_mes.items())
           if len(x) >= MIN_DIAS_VOL]
    s["VOL"] = Serie(vol)
    p(f"Volatilidad mensual (desv. de Mkt-RF diario, >= {MIN_DIAS_VOL} dias): {len(vol)} meses, "
      f"{vol[0][0]} a {vol[-1][0]}; meses descartados por pocos dias: {len(por_mes) - len(vol)}.\n")
    s["_meta"] = {"f3": f3, "fm": fm, "f5": f5, "fd": fd}
    return s


# ================================================================ estadistica

def estad(x: list[float]) -> dict:
    n = len(x)
    m = statistics.fmean(x)
    sd = statistics.stdev(x)
    nw = est.newey_west(x, REZAGOS_NW)
    return {"n": n, "media": m, "sd": sd, "t_iid": m / (sd / math.sqrt(n)), "t_nw": nw["t"],
            "ee_nw": nw["se"], "sharpe": m / sd * math.sqrt(12), "arit": 12 * m,
            "geo": math.prod(1 + r for r in x) ** (12 / n) - 1, "ic95": nw["ic95"],
            "veredicto": est.veredicto(nw["ic95"])}


def invertir(a: list[list[float]]) -> list[list[float]]:
    n = len(a)
    m = [fila[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, fila in enumerate(a)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[piv][c]) < 1e-15:
            raise ValueError("matriz singular")
        m[c], m[piv] = m[piv], m[c]
        d = m[c][c]
        m[c] = [v / d for v in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                k = m[r][c]
                m[r] = [vr - k * vc for vr, vc in zip(m[r], m[c])]
    return [fila[n:] for fila in m]


def _xtx(X):
    k = len(X[0])
    return [[sum(x[a] * x[b] for x in X) for b in range(k)] for a in range(k)]


def _sandwich(inv, meat, c):
    k = len(inv)
    tmp = [[sum(inv[a][i] * meat[i][b] for i in range(k)) for b in range(k)] for a in range(k)]
    return [[c * sum(tmp[a][i] * inv[i][b] for i in range(k)) for b in range(k)] for a in range(k)]


def ols_cluster(y, X, grupos):
    """OLS con errores agrupados (correccion G/(G-1)*(N-1)/(N-K))."""
    n, k = len(y), len(X[0])
    inv = invertir(_xtx(X))
    xty = [sum(x[a] * v for x, v in zip(X, y)) for a in range(k)]
    beta = [sum(inv[a][b] * xty[b] for b in range(k)) for a in range(k)]
    e = [v - sum(x[a] * beta[a] for a in range(k)) for x, v in zip(X, y)]
    sumas: dict = {}
    for x, u, g in zip(X, e, grupos):
        s = sumas.setdefault(g, [0.0] * k)
        for a in range(k):
            s[a] += x[a] * u
    meat = [[sum(s[a] * s[b] for s in sumas.values()) for b in range(k)] for a in range(k)]
    G = len(sumas)
    V = _sandwich(inv, meat, G / (G - 1) * (n - 1) / (n - k))
    return beta, [math.sqrt(V[a][a]) for a in range(k)], G


def ols_nw(y, X, rezagos=REZAGOS_NW):
    """OLS con errores Newey-West (Bartlett) sobre una serie de tiempo contigua; correccion n/(n-k)."""
    n, k = len(y), len(X[0])
    inv = invertir(_xtx(X))
    xty = [sum(x[a] * v for x, v in zip(X, y)) for a in range(k)]
    beta = [sum(inv[a][b] * xty[b] for b in range(k)) for a in range(k)]
    u = [[x[a] * (v - sum(x[b] * beta[b] for b in range(k))) for a in range(k)] for x, v in zip(X, y)]
    S = [[sum(ut[a] * ut[b] for ut in u) for b in range(k)] for a in range(k)]
    for j in range(1, rezagos + 1):
        w = 1 - j / (rezagos + 1)
        for a in range(k):
            for b in range(k):
                g = sum(u[t][a] * u[t - j][b] for t in range(j, n))
                gt = sum(u[t - j][a] * u[t][b] for t in range(j, n))
                S[a][b] += w * (g + gt)
    V = _sandwich(inv, S, n / (n - k))
    return beta, [math.sqrt(V[a][a]) for a in range(k)]


# ================================================================ bloque A

def etiqueta(d: date, cfg: dict, pub: date | None = None) -> str:
    pub = pub or cfg["pub"]
    if d < cfg["is_ini"]:
        return "PRE"
    if d <= cfg["is_fin"]:
        return "IS"
    if d <= pub:
        return "OOS"
    return "POST"


def construir_panel(s: dict, nombres: dict, pubs: dict | None = None) -> dict:
    """{factor: [(fecha, r, etiqueta)]}. nombres: factor -> clave de la serie (SMB o SMB5...)."""
    pubs = pubs or {}
    return {f: [(d, r, etiqueta(d, TRAMOS[f], pubs.get(f))) for d, r in s[clave].pares()]
            for f, clave in nombres.items()}


def mp_puntual(panel: dict) -> dict:
    m_is = {f: statistics.fmean(r for _, r, l in filas if l == "IS") for f, filas in panel.items()}
    y, X, g = [], [], []
    for f, filas in panel.items():
        for d, r, l in filas:
            if l in ("IS", "OOS", "POST"):
                y.append(r / m_is[f])
                X.append([1.0, 1.0 if l == "OOS" else 0.0, 1.0 if l == "POST" else 0.0])
                g.append(d)
    beta, ee, G = ols_cluster(y, X, g)
    por_factor = {}
    for f, filas in panel.items():
        grupos = {l: [r for _, r, ll in filas if ll == l] for l in ("PRE", "IS", "OOS", "POST")}
        e_is, e_post = estad(grupos["IS"]), estad(grupos["POST"])
        e_oos = estad(grupos["OOS"]) if len(grupos["OOS"]) >= 3 else None
        delta = e_post["media"] - e_is["media"]
        por_factor[f] = {
            "IS": e_is, "OOS": e_oos, "POST": e_post,
            "PRE": estad(grupos["PRE"]) if len(grupos["PRE"]) >= 3 else None,
            "decaimiento_post": 1 - e_post["media"] / e_is["media"],
            "decaimiento_oos": (1 - e_oos["media"] / e_is["media"]) if e_oos else None,
            "delta_post_menos_is": delta,
            "t_delta": delta / math.sqrt(e_post["ee_nw"] ** 2 + e_is["ee_nw"] ** 2),
        }
    return {"a": beta[0], "b1": beta[1], "b2": beta[2], "ee_a": ee[0], "ee_b1": ee[1], "ee_b2": ee[2],
            "t_b1": beta[1] / ee[1], "t_b2": beta[2] / ee[2], "n_obs": len(y), "n_meses": G,
            "D": -beta[2], "D_oos": -beta[1], "promedio_decaimientos": statistics.fmean(
                v["decaimiento_post"] for v in por_factor.values()), "por_factor": por_factor}


def mp_bootstrap(panel: dict, reps: int = N_BOOT, semilla: int = SEMILLA) -> dict:
    """Bootstrap de bloques moviles de BLOQUE meses calendario sobre todo el panel (conjunto)."""
    factores = list(panel)
    etiquetas = ("IS", "OOS", "POST")
    calendario = sorted({d for filas in panel.values() for d, _, _ in filas})
    idx = {d: i for i, d in enumerate(calendario)}
    T, F = len(calendario), len(factores)
    K = F * 3
    mes_s = [[0.0] * K for _ in range(T)]
    mes_c = [[0] * K for _ in range(T)]
    for fi, f in enumerate(factores):
        for d, r, l in panel[f]:
            if l in etiquetas:
                k = fi * 3 + etiquetas.index(l)
                mes_s[idx[d]][k] += r
                mes_c[idx[d]][k] += 1
    n_ini = T - BLOQUE + 1
    blk_s, blk_c = [], []
    for s0 in range(n_ini):
        bs, bc = [0.0] * K, [0] * K
        for j in range(s0, s0 + BLOQUE):
            for k in range(K):
                bs[k] += mes_s[j][k]
                bc[k] += mes_c[j][k]
        blk_s.append(bs)
        blk_c.append(bc)
    nbl, resto = divmod(T, BLOQUE)
    rng = random.Random(semilla)
    D, D_oos, prom = [], [], []
    dec = {f: [] for f in factores}
    dec_oos = {f: [] for f in factores}
    m_is_neg = {f: 0 for f in factores}
    sin_oos_algun_factor = 0
    for _ in range(reps):
        S, C = [0.0] * K, [0] * K
        for _b in range(nbl):
            s0 = rng.randrange(n_ini)
            bs, bc = blk_s[s0], blk_c[s0]
            for k in range(K):
                S[k] += bs[k]
                C[k] += bc[k]
        if resto:
            s0 = rng.randrange(n_ini)
            for j in range(s0, s0 + resto):
                for k in range(K):
                    S[k] += mes_s[j][k]
                    C[k] += mes_c[j][k]
        m_is = {}
        valido = True
        for fi, f in enumerate(factores):
            ci = C[fi * 3]
            if ci == 0:
                valido = False
                break
            m_is[f] = S[fi * 3] / ci
            if m_is[f] <= 0:
                m_is_neg[f] += 1
        if not valido:
            continue
        num_post = sum(S[fi * 3 + 2] / m_is[f] for fi, f in enumerate(factores))
        n_post = sum(C[fi * 3 + 2] for fi in range(F))
        if n_post:
            D.append(1 - num_post / n_post)
        n_oos = sum(C[fi * 3 + 1] for fi in range(F))
        if any(C[fi * 3 + 1] == 0 for fi in range(F)):
            sin_oos_algun_factor += 1
        if n_oos:
            D_oos.append(1 - sum(S[fi * 3 + 1] / m_is[f] for fi, f in enumerate(factores)) / n_oos)
        ds = []
        for fi, f in enumerate(factores):
            if C[fi * 3 + 2]:
                v = 1 - (S[fi * 3 + 2] / C[fi * 3 + 2]) / m_is[f]
                dec[f].append(v)
                ds.append(v)
            if C[fi * 3 + 1]:
                dec_oos[f].append(1 - (S[fi * 3 + 1] / C[fi * 3 + 1]) / m_is[f])
        if len(ds) == F:
            prom.append(statistics.fmean(ds))

    def ic(v):
        if len(v) < 40:
            return (None, None)
        v = sorted(v)
        return v[int(0.025 * len(v))], v[int(0.975 * len(v)) - 1]

    return {"reps": reps, "semilla": semilla, "bloque": BLOQUE, "meses_calendario": T,
            "ic_D": ic(D), "n_D": len(D), "ic_D_oos": ic(D_oos), "n_D_oos": len(D_oos),
            "reps_sin_oos_en_algun_factor": sin_oos_algun_factor,
            "ic_promedio": ic(prom), "n_promedio": len(prom),
            "ic_factor": {f: ic(dec[f]) for f in factores},
            "ic_factor_oos": {f: ic(dec_oos[f]) for f in factores},
            "n_factor_oos": {f: len(dec_oos[f]) for f in factores},
            "frac_m_is_no_positiva": {f: m_is_neg[f] / reps for f in factores}}


def imprimir_mp(titulo: str, mp: dict, bs: dict) -> None:
    p(f"#### {titulo}\n")
    p("| Factor | n IS / OOS / POST | media IS %/mes (t iid; t NW) | media OOS %/mes | media POST %/mes (t NW) | "
      "Decaimiento OOS | Decaimiento POST [IC95 bootstrap] | Frac. rep. con media IS <= 0 | "
      "Δ POST−IS pp/mes (t NW) |")
    p("|---|---|---|---|---|---|---|---|---|")
    for f, v in mp["por_factor"].items():
        ic = bs["ic_factor"][f]
        p(f"| {f} | {v['IS']['n']} / {v['OOS']['n'] if v['OOS'] else 0} / {v['POST']['n']} | "
          f"{pct(v['IS']['media'], 3)} ({fmt(v['IS']['t_iid'], 2)}; {fmt(v['IS']['t_nw'], 2)}) | "
          f"{pct(v['OOS']['media'], 3) if v['OOS'] else 'NA'} | "
          f"{pct(v['POST']['media'], 3)} ({fmt(v['POST']['t_nw'], 2)}) | "
          f"{pct(v['decaimiento_oos'], 1) if v['decaimiento_oos'] is not None else 'NA'}% | "
          f"{pct(v['decaimiento_post'], 1)}% [{pct(ic[0], 1)}%, {pct(ic[1], 1)}%] | "
          f"{fmt(bs['frac_m_is_no_positiva'][f], 4)} | "
          f"{pct(v['delta_post_menos_is'], 3)} ({fmt(v['t_delta'], 2)}) |")
    p("")
    p(f"- Regresion agrupada (y = r/media_IS; errores agrupados por mes; {mp['n_obs']} obs., "
      f"{mp['n_meses']} meses): a = {fmt(mp['a'], 6)}; b1 (post-muestra) = {fmt(mp['b1'], 4)} "
      f"(ee {fmt(mp['ee_b1'], 4)}, t {fmt(mp['t_b1'], 2)}); b2 (post-publicacion) = {fmt(mp['b2'], 4)} "
      f"(ee {fmt(mp['ee_b2'], 4)}, t {fmt(mp['t_b2'], 2)}).")
    p(f"- **D = −b2 = {pct(mp['D'], 1)}%**, IC95 bootstrap [{pct(bs['ic_D'][0], 1)}%, {pct(bs['ic_D'][1], 1)}%] "
      f"({bs['n_D']} repeticiones validas). McLean-Pontiff: 58%.")
    p(f"- Decaimiento fuera de muestra antes de publicar: D_oos = −b1 = {pct(mp['D_oos'], 1)}%, IC95 "
      f"[{pct(bs['ic_D_oos'][0], 1)}%, {pct(bs['ic_D_oos'][1], 1)}%] ({bs['n_D_oos']} rep.; en "
      f"{bs['reps_sin_oos_en_algun_factor']} rep. algun factor quedo sin meses OOS). McLean-Pontiff: 26%.")
    p(f"- Promedio simple de los decaimientos POST por factor: {pct(mp['promedio_decaimientos'], 1)}%, "
      f"IC95 [{pct(bs['ic_promedio'][0], 1)}%, {pct(bs['ic_promedio'][1], 1)}%].")
    p(f"- Bootstrap: {bs['reps']} repeticiones, bloques de {bs['bloque']} meses calendario sobre "
      f"{bs['meses_calendario']} meses, semilla {bs['semilla']}.\n")


def bloque_a(s: dict) -> dict:
    p("# Bloque A. Primas por tramo, por decada y decaimiento post-publicacion\n")
    principales = {"SMB": "SMB", "HML": "HML", "MOM": "MOM", "RMW": "RMW", "CMA": "CMA"}
    panel = construir_panel(s, principales)
    # conteos pre-registrados
    for f, filas in panel.items():
        n = tuple(sum(1 for _, _, l in filas if l == e) for e in ("IS", "OOS", "POST"))
        if n != TRAMOS[f]["n"]:
            raise SystemExit(f"{f}: conteo de meses IS/OOS/POST {n} != pre-registrado {TRAMOS[f]['n']}")
    p("Conteos de meses IS / OOS / POST verificados contra el pre-registro.\n")

    # --- tabla por tramo (incluye pre-muestra y el mercado en las mismas ventanas)
    p("### A.1 Estadisticos por tramo de McLean-Pontiff (brutos, largo-corto, USD)\n")
    p("Media y desv. en % mensual; Sharpe = media/desv·√12; geo = rendimiento geometrico anual de Π(1+F); "
      "t NW con 6 rezagos. Mkt-RF en la misma ventana como referencia.\n")
    p("| Factor | Tramo | Ventana | n | Media %/mes | Desv. %/mes | t iid | t NW | IC95 NW (%/mes) | Sharpe | "
      "×12 % | Geo % | Veredicto | Mkt-RF: media %/mes (Sharpe) |")
    p("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    tabla_tramos = {}
    for f in FACTORES:
        cfg = TRAMOS[f]
        serie = s[f]
        ventanas = []
        if serie.fechas[0] < cfg["is_ini"]:
            ventanas.append(("PRE", serie.fechas[0], fin_mes_previo(cfg["is_ini"])))
        ventanas += [("IS", cfg["is_ini"], cfg["is_fin"]),
                     ("OOS", dh.a_fin_de_mes(date(cfg["is_fin"].year + (cfg["is_fin"].month == 12),
                                                   cfg["is_fin"].month % 12 + 1, 1)), cfg["pub"]),
                     ("POST", dh.a_fin_de_mes(date(cfg["pub"].year + (cfg["pub"].month == 12),
                                                    cfg["pub"].month % 12 + 1, 1)), FIN_DATOS),
                     ("COMPLETO", serie.fechas[0], FIN_DATOS)]
        tabla_tramos[f] = {}
        for nombre, a, b in ventanas:
            x = serie.tramo(a, b)
            e = estad(x)
            mk = estad(s["MKT"].tramo(a, b))
            tabla_tramos[f][nombre] = {**e, "ventana": f"{ym(a)} a {ym(b)}"}
            p(f"| {f} | {nombre} | {ym(a)} a {ym(b)} | {e['n']} | {pct(e['media'], 3)} | {pct(e['sd'], 3)} | "
              f"{fmt(e['t_iid'], 2)} | {fmt(e['t_nw'], 2)} | [{pct(e['ic95'][0], 3)}, {pct(e['ic95'][1], 3)}] | "
              f"{fmt(e['sharpe'], 3)} | {pct(e['arit'])} | {pct(e['geo'])} | {e['veredicto']} | "
              f"{pct(mk['media'], 3)} ({fmt(mk['sharpe'], 3)}) |")
    p("")

    # --- H1: datos de hoy contra los articulos
    p("### A.2 H1: la muestra original con los datos de hoy\n")
    p("| Factor | Muestra del articulo | Media hoy %/mes | t iid hoy | t NW hoy | Cifra del articulo (otra construccion salvo FF2015) | ¿Media > 0 y t iid >= 2? |")
    p("|---|---|---|---|---|---|---|")
    cifras = {"SMB": "Banz: γ1 = −0.00052 (t −2.92); muy pequeñas − muy grandes 1.52%/mes",
              "HML": "FF92: decil alto − bajo de BE/ME 1.53%/mes; pendiente ln(BE/ME) 0.50 (t 5.71)",
              "MOM": "JT93: 6/6 comprar−vender 0.95%/mes (t 3.07)",
              "RMW": "FF2015 tabla 4 (2×3): 0.25 (t 2.92)", "CMA": "FF2015 tabla 4 (2×3): 0.33 (t 4.07)"}
    h1 = {}
    for f in FACTORES:
        e = tabla_tramos[f]["IS"]
        ok = e["media"] > 0 and e["t_iid"] >= 2
        h1[f] = ok
        p(f"| {f} | {e['ventana']} | {pct(e['media'], 3)} | {fmt(e['t_iid'], 2)} | {fmt(e['t_nw'], 2)} | "
          f"{cifras[f]} | {'si' if ok else 'NO'} |")
    p("")
    p("H1-magnitud contra FF2015 tabla 4 (2×3, 1963-07 a 2013-12, 606 meses; tolerancia ±0.05 pp/mes). "
      "Se usa el archivo de 5 factores (misma construccion que el articulo); el de 3 factores se reporta como referencia.\n")
    p("| Factor | FF2015 media (t) | Hoy, archivo 5F: media (t iid) | Δ pp/mes | ¿Dentro de ±0.05? | Hoy, archivo 3F: media (t iid) |")
    p("|---|---|---|---|---|---|")
    h1_mag = {}
    for f, (m_art, t_art) in FF2015_T4.items():
        clave5 = {"SMB": "SMB5", "HML": "HML5"}.get(f, f)
        e5 = estad(s[clave5].tramo(date(1963, 7, 31), date(2013, 12, 31)))
        d = 100 * e5["media"] - m_art
        h1_mag[f] = abs(d) <= 0.05 + 1e-12
        tres = ""
        if f in ("SMB", "HML"):
            e3 = estad(s[f].tramo(date(1963, 7, 31), date(2013, 12, 31)))
            tres = f"{pct(e3['media'], 3)} ({fmt(e3['t_iid'], 2)})"
        p(f"| {f} | {m_art:.2f} ({t_art:.2f}) | {pct(e5['media'], 3)} ({fmt(e5['t_iid'], 2)}) [n={e5['n']}] | "
          f"{d:+.3f} | {'si' if h1_mag[f] else 'NO'} | {tres or 'igual (solo 5F)'} |")
    e_mk = estad(s["MKT5"].tramo(date(1963, 7, 31), date(2013, 12, 31)))
    p(f"| Mkt-RF (ref.) | 0.50 (2.74) | {pct(e_mk['media'], 3)} ({fmt(e_mk['t_iid'], 2)}) | "
      f"{100 * e_mk['media'] - 0.50:+.3f} | {'si' if abs(100 * e_mk['media'] - 0.50) <= 0.05 else 'NO'} | |")
    p("")
    condicion_a = sum(1 for f in ("HML", "MOM", "RMW", "CMA") if not h1[f]) == 0 and sum(h1_mag.values()) >= 3
    # factores distintos que fallan alguna parte de A (t >= 2 o magnitud contra FF2015)
    fallas_factores = sorted({f for f in ("HML", "MOM", "RMW", "CMA") if not h1[f]} |
                             {f for f, ok in h1_mag.items() if not ok})
    fallas_a = len(fallas_factores)
    p(f"Factores que fallan alguna parte de la condicion A: {', '.join(fallas_factores) or 'ninguno'}.")
    p(f"Condicion A: {'SE CUMPLE' if condicion_a else 'NO se cumple'} (fallas t>=2 en HML/MOM/RMW/CMA: "
      f"{sum(1 for f in ('HML', 'MOM', 'RMW', 'CMA') if not h1[f])}; factores dentro de ±0.05 de FF2015: "
      f"{sum(h1_mag.values())} de 4).\n")

    # --- decaimiento
    p("### A.3 Decaimiento post-publicacion (diseno McLean-Pontiff)\n")
    mp = mp_puntual(panel)
    bs = mp_bootstrap(panel)
    imprimir_mp("Principal: SMB y HML de 3 factores, Mom, RMW y CMA de 5 factores; fechas de la revista", mp, bs)

    sens = {}
    p("### A.4 Sensibilidades del decaimiento (lista cerrada del pre-registro)\n")
    pubs_alt = {"SMB": TRAMOS["SMB"]["alt"], "RMW": TRAMOS["RMW"]["alt"], "CMA": TRAMOS["CMA"]["alt"]}
    panel_alt = construir_panel(s, principales, pubs_alt)
    sens["fechas_alternativas"] = (mp_puntual(panel_alt), mp_bootstrap(panel_alt))
    imprimir_mp("S1. Fechas alternativas: Banz 1979-06 (recepcion), FF2015 2014-10 (en linea)", *sens["fechas_alternativas"])
    panel5 = construir_panel(s, {"SMB": "SMB5", "HML": "HML5", "MOM": "MOM", "RMW": "RMW", "CMA": "CMA"})
    # con el archivo de 5F, la muestra de SMB empieza en 1963-07 (no hay 1936-1963): se reporta tal cual
    sens["archivo_5F"] = (mp_puntual(panel5), mp_bootstrap(panel5))
    imprimir_mp("S2. SMB y HML del archivo de 5 factores (SMB: muestra original recortada a 1963-07 a 1975-12)",
                *sens["archivo_5F"])
    debiles = [f for f in FACTORES if mp["por_factor"][f]["IS"]["t_iid"] < 2]
    if debiles:
        panel_sin = {f: v for f, v in panel.items() if f not in debiles}
        sens["sin_debiles"] = (mp_puntual(panel_sin), mp_bootstrap(panel_sin))
        imprimir_mp(f"S3. Sin los factores con t iid < 2 dentro de muestra ({', '.join(debiles)})", *sens["sin_debiles"])
    else:
        p("S3. Ningun factor tiene t iid < 2 dentro de muestra: la sensibilidad no aplica.\n")
    p("S4. Pre-muestra: ver las filas PRE de la tabla A.1 (SMB 1926-07 a 1935-12, HML 1926-07 a 1963-06, "
      "Mom 1927-01 a 1964-12).\n")

    # --- decadas
    p("### A.5 Primas por decada (media %/mes, t NW, Sharpe anual, geometrico anual %)\n")
    decadas = [(date(1926, 7, 31), date(1929, 12, 31), "1926-07 a 1929")] + \
              [(date(a, 1, 31), date(a + 9, 12, 31), f"{a}s") for a in range(1930, 2020, 10)] + \
              [(date(2020, 1, 31), FIN_DATOS, "2020-01 a 2026-07")]
    p("| Decada | " + " | ".join(f"{f}: media (t NW) / Sharpe / geo" for f in ("MKT",) + FACTORES) + " |")
    p("|---|" + "---|" * (len(FACTORES) + 1))
    tabla_dec = {}
    for a, b, et in decadas:
        celdas = []
        for f in ("MKT",) + FACTORES:
            x = s[f].tramo(a, b)
            if len(x) < 12:
                celdas.append("—")
                continue
            e = estad(x)
            tabla_dec.setdefault(f, {})[et] = e
            celdas.append(f"{pct(e['media'], 2)} ({fmt(e['t_nw'], 2)}) / {fmt(e['sharpe'], 2)} / {pct(e['geo'], 1)}")
        p(f"| {et} | " + " | ".join(celdas) + " |")
    p("")
    RESULTADOS["bloque_a"] = {
        "tramos": {f: {k: {kk: vv for kk, vv in v.items() if kk != "ic95"} for k, v in d.items()}
                   for f, d in tabla_tramos.items()},
        "h1": h1, "h1_magnitud": h1_mag, "condicion_a": condicion_a, "fallas_condicion_a": fallas_a,
        "mp": {k: v for k, v in mp.items() if k != "por_factor"},
        "mp_por_factor": {f: {"decaimiento_post": v["decaimiento_post"], "decaimiento_oos": v["decaimiento_oos"],
                              "delta": v["delta_post_menos_is"], "t_delta": v["t_delta"],
                              "media_is": v["IS"]["media"], "media_post": v["POST"]["media"]}
                          for f, v in mp["por_factor"].items()},
        "bootstrap": bs,
        "sensibilidades": {k: {"D": v[0]["D"], "ic_D": v[1]["ic_D"], "D_oos": v[0]["D_oos"],
                               "ic_D_oos": v[1]["ic_D_oos"], "t_b2": v[0]["t_b2"],
                               "por_factor": {f: vv["decaimiento_post"] for f, vv in v[0]["por_factor"].items()}}
                           for k, v in sens.items()},
        "decadas": {f: {k: {"media": v["media"], "t_nw": v["t_nw"], "sharpe": v["sharpe"], "geo": v["geo"], "n": v["n"]}
                        for k, v in d.items()} for f, d in tabla_dec.items()},
    }
    return {"mp": mp, "bs": bs, "condicion_a": condicion_a, "fallas_a": fallas_a, "h1": h1, "h1_mag": h1_mag,
            "tramos": tabla_tramos}


# ================================================================ bloque B

def curva_indice(serie: Serie, ini: date | None = None) -> list[tuple]:
    pares = serie.pares(ini)
    curva = [(fin_mes_previo(pares[0][0]), 1.0)]
    for f, r in pares:
        curva.append((f, curva[-1][1] * (1 + r)))
    return curva


def episodios_dd(curva: list[tuple], top: int = 3) -> list[dict]:
    eps = []
    i_pico, en_dd, i_valle = 0, False, None
    for i in range(1, len(curva)):
        if curva[i][1] >= curva[i_pico][1]:
            if en_dd:
                eps.append((i_pico, i_valle, i))
                en_dd = False
            i_pico = i
        else:
            if not en_dd:
                en_dd, i_valle = True, i
            elif curva[i][1] < curva[i_valle][1]:
                i_valle = i
    if en_dd:
        eps.append((i_pico, i_valle, None))
    salida = [{"pico": curva[a][0], "valle": curva[b][0], "recuperacion": curva[c][0] if c else None,
               "profundidad": curva[b][1] / curva[a][1] - 1, "meses_pico_valle": b - a} for a, b, c in eps]
    return sorted(salida, key=lambda e: e["profundidad"])[:top]


def mercado_24m(s: dict, d: date):
    fechas = s["MKT_TOTAL"].fechas
    i = bisect_left(fechas, d)
    if i < MESES_OSO or i >= len(fechas) or fechas[i] != d:
        return None
    return math.prod(1 + v for v in s["MKT_TOTAL"].valores[i - MESES_OSO:i]) - 1


def bloque_b(s: dict) -> dict:
    p("# Bloque B. Crashes de momentum, drawdowns y \"muerte del value\"\n")
    res = {}
    mom = s["MOM"]
    # --- peores meses
    def tabla_peores(pares, titulo, k=15):
        p(f"#### {titulo}\n")
        p("| Rango | Mes | Mom % | Mercado acumulado 24m previos % | Mercado del mes % | ¿Oso? | ¿Mercado del mes > 0? | ¿En la tabla 2 de DM? |")
        p("|---|---|---|---|---|---|---|---|")
        filas = sorted(pares, key=lambda x: x[1])[:k]
        n_oso = n_sube = n_dm = 0
        salida = []
        for rango, (d, r) in enumerate(filas, 1):
            m24 = mercado_24m(s, d)
            mt = s["MKT_TOTAL"].mapa[d]
            oso = m24 is not None and m24 < 0
            n_oso += oso
            n_sube += mt > 0
            en_dm = ym(d) in DM_PEORES
            n_dm += en_dm
            salida.append({"mes": ym(d), "mom": r, "mkt_24m": m24, "mkt_mes": mt, "oso": oso})
            p(f"| {rango} | {ym(d)} | {pct(r)} | {pct(m24) if m24 is not None else 'NA (<24 meses)'} | {pct(mt)} | "
              f"{'si' if oso else 'no'} | {'si' if mt > 0 else 'no'} | {'si' if en_dm else 'no'} |")
        p(f"\nOso en {n_oso} de {len(filas)}; mercado del mes > 0 en {n_sube} de {len(filas)}; "
          f"coinciden con la tabla 2 de DM: {n_dm} de {len(filas)}.\n")
        return {"filas": salida, "n_oso": n_oso, "n_sube": n_sube, "n_dm": n_dm}

    res["peores_completo"] = tabla_peores(mom.pares(), "B.1 Los 15 peores meses de Mom, 1927-01 a 2026-07")
    res["peores_dm"] = tabla_peores(mom.pares(None, date(2013, 3, 31)),
                                    "B.2 Los 15 peores meses de Mom en la ventana de DM, 1927-01 a 2013-03")
    res["peores_post_dm"] = tabla_peores(mom.pares(date(2013, 4, 30)),
                                         "B.3 Los 5 peores meses de Mom despues de DM, 2013-04 a 2026-07", k=5)
    p("Tabla 2 de DM (WML de deciles), para comparar magnitudes: " +
      "; ".join(f"{m} {v:.2f}%" for m, v in zip(DM_PEORES, DM_PEORES_VAL)) + ".\n")
    h4a = res["peores_completo"]["n_oso"] >= 10
    h4b = res["peores_completo"]["n_sube"] >= 12
    h4c = res["peores_dm"]["n_dm"] >= 8

    # --- oso vs normal
    p("#### B.4 Media de Mom en meses \"oso\" (mercado de 24 meses previos < 0) contra los demas\n")
    p("Regresion Mom_t = a + b·Oso_t con errores Newey-West (6 rezagos) sobre la serie contigua; "
      "b es la diferencia de medias oso − normal.\n")
    p("| Ventana | n oso | n normal | Media normal %/mes | Media oso %/mes | Diferencia b pp/mes | t NW de b |")
    p("|---|---|---|---|---|---|---|")
    res["oso_vs_normal"] = {}
    for a, b, et in ((date(1928, 7, 31), FIN_DATOS, "1928-07 a 2026-07 (completo con 24m)"),
                     (date(1928, 7, 31), date(2013, 3, 31), "1928-07 a 2013-03 (DM)"),
                     (date(2013, 4, 30), FIN_DATOS, "2013-04 a 2026-07 (post DM)")):
        pares = mom.pares(a, b)
        osos = [1.0 if (mercado_24m(s, d) or 0) < 0 else 0.0 for d, _ in pares]
        y = [r for _, r in pares]
        n_oso = int(sum(osos))
        m_n = statistics.fmean([r for r, o in zip(y, osos) if o == 0])
        if n_oso >= 2:
            beta, ee = ols_nw(y, [[1.0, o] for o in osos])
            m_o = statistics.fmean([r for r, o in zip(y, osos) if o == 1])
            tb = beta[1] / ee[1]
        else:
            beta, m_o, tb = [m_n, None], (statistics.fmean([r for r, o in zip(y, osos) if o == 1]) if n_oso else None), None
        res["oso_vs_normal"][et] = {"n_oso": n_oso, "n_normal": len(y) - n_oso, "media_normal": m_n,
                                    "media_oso": m_o, "b": beta[1], "t_b": tb}
        p(f"| {et} | {n_oso} | {len(y) - n_oso} | {pct(m_n, 3)} | {pct(m_o, 3) if m_o is not None else 'NA'} | "
          f"{pct(beta[1], 3) if beta[1] is not None else 'NA'} | {fmt(tb, 2)} |")
    p("")
    h4d = res["oso_vs_normal"]["1928-07 a 2013-03 (DM)"]["media_oso"] < \
        res["oso_vs_normal"]["1928-07 a 2013-03 (DM)"]["media_normal"]
    comp = res["oso_vs_normal"]["1928-07 a 2026-07 (completo con 24m)"]
    h4d_completo = comp["media_oso"] < comp["media_normal"]
    res["H4"] = {"a_oso>=10de15": h4a, "b_mercado_sube>=12de15": h4b, "c_coincide_dm>=8": h4c,
                 "d_media_oso<normal_DM": h4d, "d_media_oso<normal_completo": h4d_completo,
                 "confirmada": h4a and h4b and h4c and h4d_completo}
    p(f"H4: (a) oso >= 10 de 15: {'si' if h4a else 'NO'}; (b) mercado del mes > 0 en >= 12 de 15: "
      f"{'si' if h4b else 'NO'}; (c) >= 8 de los 15 de DM entre los 15 peores de Mom en 1927-01 a 2013-03: "
      f"{'si' if h4c else 'NO'}; (d) media oso < media normal (completo): {'si' if h4d_completo else 'NO'} "
      f"(ventana DM: {'si' if h4d else 'NO'}). **H4 {'confirmada' if res['H4']['confirmada'] else 'no confirmada'}.**\n")

    # --- drawdowns
    p("#### B.5 Los 3 peores drawdowns de Π(1+F) por factor (desde el primer dato)\n")
    p("| Factor | # | Pico | Valle | Profundidad % | Meses pico-valle | Recuperacion |")
    p("|---|---|---|---|---|---|---|")
    res["drawdowns"] = {}
    for f in ("MKT",) + FACTORES:
        eps = episodios_dd(curva_indice(s[f]))
        res["drawdowns"][f] = [{k: (ym(v) if isinstance(v, date) else v) for k, v in e.items()} for e in eps]
        for k, e in enumerate(eps, 1):
            p(f"| {f} | {k} | {ym(e['pico'])} | {ym(e['valle'])} | {pct(e['profundidad'], 1)} | "
              f"{e['meses_pico_valle']} | {ym(e['recuperacion']) if e['recuperacion'] else 'no recupera a 2026-07'} |")
    p("Nota: MKT es Mkt-RF (exceso), no el mercado total.\n")

    # --- muerte del value
    p("#### B.6 \"Muerte del value\": HML 2007-2020 y lo posterior\n")
    res["value"] = {}
    for clave, et in (("HML", "HML archivo 3F"), ("HML5", "HML archivo 5F")):
        curva = curva_indice(s[clave])
        fechas = [c[0] for c in curva]
        vals = [c[1] for c in curva]
        runmax, i_run = [], []
        mx, imx = -1.0, 0
        for i, v in enumerate(vals):
            if v > mx:
                mx, imx = v, i
            runmax.append(mx)
            i_run.append(imx)
        rango = [i for i, d in enumerate(fechas) if date(2007, 1, 1) <= d <= date(2020, 12, 31)]
        i_valle = min(rango, key=lambda i: vals[i] / runmax[i])
        i_pico = i_run[i_valle]
        prof = vals[i_valle] / vals[i_pico] - 1
        rec = vals[-1] / vals[i_valle] - 1
        dist = vals[-1] / vals[i_pico] - 1
        res["value"][clave] = {"pico": ym(fechas[i_pico]), "valle": ym(fechas[i_valle]), "profundidad": prof,
                               "meses": i_valle - i_pico, "desde_valle_a_2026_07": rec, "distancia_pico_2026_07": dist,
                               "supera_pico_despues": any(v >= vals[i_pico] for v in vals[i_valle:])}
        p(f"- {et}: pico {ym(fechas[i_pico])}, valle {ym(fechas[i_valle])}, profundidad **{pct(prof, 1)}%** en "
          f"{i_valle - i_pico} meses; del valle a 2026-07: **{pct(rec, 1)}%**; distancia al pico en 2026-07: "
          f"**{pct(dist, 1)}%**; ¿recupero el pico despues del valle?: "
          f"{'si' if res['value'][clave]['supera_pico_despues'] else 'no'}.")
    v3 = res["value"]["HML"]
    p("")
    p("| Ventana | n | HML media %/mes (t NW) | Sharpe | Geo anual % | Mkt-RF media %/mes |")
    p("|---|---|---|---|---|---|")
    valle_d = date(int(v3["valle"][:4]), int(v3["valle"][5:]), 1)
    desde_valle = dh.a_fin_de_mes(date(valle_d.year + (valle_d.month == 12), valle_d.month % 12 + 1, 1))
    res["value"]["ventanas"] = {}
    for a, b, et in ((date(1992, 1, 31), date(2006, 12, 31), "1992-01 a 2006-12"),
                     (date(2007, 1, 31), date(2020, 12, 31), "2007-01 a 2020-12"),
                     (date(2021, 1, 31), FIN_DATOS, "2021-01 a 2026-07"),
                     (desde_valle, FIN_DATOS, f"{ym(desde_valle)} a 2026-07 (desde el valle)")):
        e = estad(s["HML"].tramo(a, b))
        mk = statistics.fmean(s["MKT"].tramo(a, b))
        res["value"]["ventanas"][et] = {"n": e["n"], "media": e["media"], "t_nw": e["t_nw"], "sharpe": e["sharpe"], "geo": e["geo"]}
        p(f"| {et} | {e['n']} | {pct(e['media'], 3)} ({fmt(e['t_nw'], 2)}) | {fmt(e['sharpe'], 3)} | {pct(e['geo'])} | {pct(mk, 3)} |")
    p("")
    p("HML (archivo 3F) por año calendario, Π(1+HML) − 1 en %: " + "; ".join(
        f"{a}{' (ene-jul)' if a == 2026 else ''}: {pct(math.prod(1 + r for r in s['HML'].tramo(date(a, 1, 31), date(a, 12, 31))) - 1, 1)}"
        for a in range(2007, 2027)) + ".\n")
    h5a = v3["profundidad"] <= -0.50
    h5b = res["value"]["ventanas"]["2007-01 a 2020-12"]["media"] < 0
    h5c = v3["desde_valle_a_2026_07"] > 0 and not v3["supera_pico_despues"]
    res["H5"] = {"a_caida<=-50%": h5a, "b_media_2007_2020<0": h5b, "c_recupera_pero_bajo_pico": h5c,
                 "confirmada": h5a and h5b and h5c}
    p(f"H5: (a) caida <= −50%: {'si' if h5a else 'NO'}; (b) media 2007-2020 < 0: {'si' if h5b else 'NO'}; "
      f"(c) acumulado positivo desde el valle pero bajo el pico previo: {'si' if h5c else 'NO'}. "
      f"**H5 {'confirmada' if res['H5']['confirmada'] else 'no confirmada'}.**\n")

    # --- ventanas de 6 meses
    p("#### B.7 Ventanas de 6 meses traslapadas con acumulado > 0 (antes = termina <= publicacion; "
      "despues = empieza despues de la publicacion; las que cruzan la fecha se excluyen)\n")
    p("| Factor | Publicacion | n antes | % > 0 antes | n despues | % > 0 despues |")
    p("|---|---|---|---|---|---|")
    res["ventanas6"] = {}
    for f in FACTORES:
        pub = TRAMOS[f]["pub"]
        pares = s[f].pares()
        antes, despues = [], []
        for i in range(len(pares) - 5):
            acum = math.prod(1 + r for _, r in pares[i:i + 6]) - 1
            if pares[i + 5][0] <= pub:
                antes.append(acum > 0)
            elif pares[i][0] > pub:
                despues.append(acum > 0)
        res["ventanas6"][f] = {"n_antes": len(antes), "frac_antes": sum(antes) / len(antes),
                               "n_despues": len(despues), "frac_despues": sum(despues) / len(despues)}
        p(f"| {f} | {ym(pub)} | {len(antes)} | {pct(sum(antes) / len(antes), 1)} | {len(despues)} | "
          f"{pct(sum(despues) / len(despues), 1)} |")
    p("")
    RESULTADOS["bloque_b"] = res
    return res


# ================================================================ bloque C

def _dec(txt: str) -> int:
    return len(txt.split(".")[1]) if "." in txt else 0


def comparar_cifra(cid, desc, publicado: str, candidatos: dict) -> dict:
    """candidatos: {definicion: valor calculado}. Tolerancia = 1 unidad del ultimo digito publicado."""
    pub = float(publicado.replace("−", "-").replace("+", ""))
    unidad = 10 ** (-_dec(publicado))
    mejor = min(candidatos.items(), key=lambda kv: abs(kv[1] - pub) if kv[1] is not None else math.inf)
    dif = mejor[1] - pub if mejor[1] is not None else None
    if dif is None:
        estado = "no calculable"
    elif abs(dif) <= unidad + 1e-9:
        estado = "reproducida"
    elif abs(dif) <= 5 * unidad + 1e-9:
        estado = "diferencia menor"
    else:
        estado = "DISCREPANCIA"
    p(f"| {cid} | {desc} | {publicado} | {mejor[1]:.{max(2, _dec(publicado))}f} | {mejor[0]} | "
      f"{dif:+.{max(2, _dec(publicado))}f} | {estado} |")
    return {"id": cid, "desc": desc, "publicado": publicado, "calculado": mejor[1], "definicion": mejor[0],
            "diferencia": dif, "estado": estado}


def bloque_c(s: dict) -> list:
    p("# Bloque C. Cifras que el sistema ya publico (conocimiento/02 y /03)\n")
    p("Tolerancia: 1 unidad del ultimo digito publicado = \"reproducida\"; hasta 5 unidades = \"diferencia menor\"; "
      "mas = \"DISCREPANCIA\". Se prueban las definiciones declaradas y se reporta la mas cercana.\n")
    p("| # | Afirmacion | Publicado | Calculado | Definicion que mas se acerca | Diferencia | Estado |")
    p("|---|---|---|---|---|---|---|")
    out = []
    D = lambda a, m: dh.fin_de_mes(a, m)  # noqa: E731

    def anual(claves, a, b):
        c = {}
        for k in claves:
            e = estad(s[k].tramo(a, b))
            c[f"{k} media×12"] = 100 * e["arit"]
            c[f"{k} geometrica"] = 100 * e["geo"]
        return c

    def tstat(claves, a, b):
        c = {}
        for k in claves:
            e = estad(s[k].tramo(a, b))
            c[f"{k} t iid"] = e["t_iid"]
            c[f"{k} t NW6"] = e["t_nw"]
        return c

    def sharpe(claves, a, b):
        return {f"{k} Sharpe": estad(s[k].tramo(a, b))["sharpe"] for k in claves}

    opciones = {"MKT": ("MKT5", "MKT"), "SMB": ("SMB5", "SMB"), "HML": ("HML5", "HML"), "RMW": ("RMW",),
                "CMA": ("CMA",), "MOM": ("MOM",)}
    tabla02 = {
        "C1": ((D(1963, 7), D(2026, 7)), {"MKT": ("7.19", "3.70"), "SMB": ("2.25", "1.71"), "HML": ("3.59", "2.77"),
                                          "RMW": ("3.08", "3.10"), "CMA": ("2.96", "3.27"), "MOM": ("7.25", "3.96")}),
        "C2": ((D(1963, 7), D(1991, 6)), {"MKT": ("4.55", "1.52"), "SMB": ("3.68", "1.89"), "HML": ("4.96", "2.98"),
                                          "RMW": ("2.39", "2.34"), "CMA": ("3.76", "2.97"), "MOM": ("9.55", "4.20")}),
        "C3": ((D(1992, 1), D(2026, 7)), {"MKT": ("9.06", "3.54"), "SMB": ("1.14", "0.63"), "HML": ("2.81", "1.45"),
                                          "RMW": ("3.58", "2.22"), "CMA": ("2.51", "1.95"), "MOM": ("4.92", "1.77")}),
        "C4": ((D(2016, 1), D(2025, 12)), {"MKT": ("12.96", "2.60"), "SMB": ("-2.21", "-0.68"), "HML": ("-0.49", "-0.12"),
                                           "RMW": ("3.55", "1.48"), "CMA": ("-0.65", "-0.24"), "MOM": ("0.34", "0.08")}),
    }
    for cid, ((a, b), cifras) in tabla02.items():
        for f, (v, t) in cifras.items():
            out.append(comparar_cifra(cid, f"{f} {ym(a)} a {ym(b)}, anual %", v, anual(opciones[f], a, b)))
            out.append(comparar_cifra(cid, f"{f} {ym(a)} a {ym(b)}, t", t, tstat(opciones[f], a, b)))
    c5 = {"MKT": ("10.42", "+7.4"), "SMB": ("-4.66", "+6.6"), "HML": ("8.07", "+12.3"), "RMW": ("5.85", "-5.8"),
          "CMA": ("1.30", "+7.2"), "MOM": ("2.31", "+10.2")}
    for f, (v, acum) in c5.items():
        out.append(comparar_cifra("C5", f"{f} 2021-2025, anual %", v, anual(opciones[f], D(2021, 1), D(2025, 12))))
        cands = {}
        for k in opciones[f]:
            x = s[k].tramo(D(2026, 1), D(2026, 7))
            cands[f"{k} compuesto"] = 100 * (math.prod(1 + r for r in x) - 1)
            cands[f"{k} suma"] = 100 * sum(x)
        out.append(comparar_cifra("C5", f"{f} ene-jul 2026 acumulado %", acum, cands))
    # C6-C9 series largas
    largas = [("C6", "HML", ("HML",), D(1926, 7), D(2026, 7), "4.26", "3.46"),
              ("C6", "HML", ("HML",), D(1926, 7), D(1991, 12), "5.02", "3.18"),
              ("C6", "HML", ("HML",), D(1992, 1), D(2026, 7), "2.81", "1.45"),
              ("C7", "MOM", ("MOM",), D(1927, 1), D(2026, 7), "7.41", "4.55"),
              ("C7", "MOM", ("MOM",), D(1927, 1), D(1989, 12), "8.53", "4.15"),
              ("C7", "MOM", ("MOM",), D(1994, 1), D(2026, 7), "4.49", "1.54"),
              ("C7", "MOM", ("MOM",), D(2000, 1), D(2026, 7), "2.47", "0.72"),
              ("C9", "SMB", ("SMB",), D(1926, 7), D(2026, 7), "1.99", "1.82"),
              ("C9", "SMB", ("SMB",), D(1992, 1), D(2026, 7), "0.66", "0.36")]
    for cid, f, claves, a, b, v, t in largas:
        out.append(comparar_cifra(cid, f"{f} {ym(a)} a {ym(b)}, anual %", v, anual(claves, a, b)))
        out.append(comparar_cifra(cid, f"{f} {ym(a)} a {ym(b)}, t", t, tstat(claves, a, b)))
    # drawdowns y crash (C6, C8, C13)
    for clave in ("HML",):
        eps = episodios_dd(curva_indice(s[clave]), top=1)
        e = eps[0]
        out.append(comparar_cifra("C6", f"HML 3F peor DD (calc.: {ym(e['pico'])} a {ym(e['valle'])}; publ.: 2006-12 a 2020-09) %",
                                  "-57.8", {"HML 3F": 100 * e["profundidad"]}))
    eps_mom = episodios_dd(curva_indice(s["MOM"]), top=10)
    for pico_pub, valle_pub, prof in (("1932-06", "1939-09", "-78.4"), ("2008-11", "2009-09", "-57.8")):
        cand = [e for e in eps_mom if ym(e["valle"])[:4] == valle_pub[:4]]
        e = cand[0] if cand else None
        if e:
            out.append(comparar_cifra("C8", f"Mom DD (calc.: pico {ym(e['pico'])}, valle {ym(e['valle'])}; publ.: {pico_pub} a {valle_pub}) %",
                                      prof, {"Mom episodio de DD": 100 * e["profundidad"]}))
    x = s["MOM"].mapa[D(2009, 4)]
    out.append(comparar_cifra("C8", "Mom abril 2009 %", "-34.4", {"Mom": 100 * x}))
    x = s["MOM"].tramo(D(2009, 3), D(2009, 9))
    out.append(comparar_cifra("C8", "Mom mar-sep 2009 acumulado %", "-56.4",
                              {"compuesto": 100 * (math.prod(1 + r for r in x) - 1), "suma": 100 * sum(x)}))
    # C10 combinaciones
    fechas63 = [f for f in s["RMW"].fechas]
    for hk in ("HML5", "HML"):
        s[f"HMLMOM_{hk}"] = Serie([(f, 0.5 * s[hk].mapa[f] + 0.5 * s["MOM"].mapa[f]) for f in fechas63])
    for sk, hk in (("SMB5", "HML5"), ("SMB", "HML")):
        s[f"EW5_{hk}"] = Serie([(f, (s[sk].mapa[f] + s[hk].mapa[f] + s["MOM"].mapa[f] + s["RMW"].mapa[f] +
                                     s["CMA"].mapa[f]) / 5) for f in fechas63])
    a, b = D(1963, 7), D(2026, 7)
    out.append(comparar_cifra("C10", "HML+Mom 50/50 1963-07 a 2026-07, anual %", "5.42", anual(("HMLMOM_HML5", "HMLMOM_HML"), a, b)))
    out.append(comparar_cifra("C10", "HML+Mom 50/50 1963-07 a 2026-07, t", "5.34", tstat(("HMLMOM_HML5", "HMLMOM_HML"), a, b)))
    out.append(comparar_cifra("C10", "HML+Mom 50/50 1963-07 a 2026-07, Sharpe", "0.67", sharpe(("HMLMOM_HML5", "HMLMOM_HML"), a, b)))
    out.append(comparar_cifra("C10", "corr(HML, Mom) 1963-07 a 2026-07", "-0.19",
                              {f"{hk}": statistics.correlation(s[hk].tramo(a, b), s["MOM"].tramo(a, b)) for hk in ("HML5", "HML")}))
    out.append(comparar_cifra("C10", "corr(HML, Mom) 2016-2025", "-0.30",
                              {f"{hk}": statistics.correlation(s[hk].tramo(D(2016, 1), D(2025, 12)), s["MOM"].tramo(D(2016, 1), D(2025, 12)))
                               for hk in ("HML5", "HML")}))
    out.append(comparar_cifra("C10", "HML+Mom 50/50 2016-2025, anual %", "-0.07", anual(("HMLMOM_HML5", "HMLMOM_HML"), D(2016, 1), D(2025, 12))))
    out.append(comparar_cifra("C10", "HML+Mom 50/50 2016-2025, Sharpe", "-0.01", sharpe(("HMLMOM_HML5", "HMLMOM_HML"), D(2016, 1), D(2025, 12))))
    out.append(comparar_cifra("C10", "EW5 1963-07 a 2026-07, Sharpe", "0.84", sharpe(("EW5_HML5", "EW5_HML"), a, b)))
    out.append(comparar_cifra("C10", "EW5 1963-07 a 2026-07, t", "6.65", tstat(("EW5_HML5", "EW5_HML"), a, b)))
    out.append(comparar_cifra("C10", "EW5 2016-2025, anual %", "0.11", anual(("EW5_HML5", "EW5_HML"), D(2016, 1), D(2025, 12))))
    out.append(comparar_cifra("C10", "EW5 2016-2025, t", "0.07", tstat(("EW5_HML5", "EW5_HML"), D(2016, 1), D(2025, 12))))
    # C11-C12 capitulo 03
    cap03 = [("C11", ("HML", "HML5"), D(1963, 7), D(1991, 12), "4.23", "0.52", "2.75"),
             ("C11", ("HML", "HML5"), D(1992, 1), D(2026, 7), "2.19", "0.25", "1.45"),
             ("C11", ("HML", "HML5"), D(1992, 1), D(2006, 12), "7.61", "0.72", None),
             ("C11", ("HML", "HML5"), D(2007, 1), D(2020, 12), "-5.67", None, None),
             ("C12", ("RMW",), D(1963, 7), D(2013, 12), "2.95", "0.41", "2.94"),
             ("C12", ("RMW",), D(2014, 1), D(2026, 7), "2.23", "0.30", "1.08"),
             ("C12", ("CMA",), D(1963, 7), D(2013, 12), "3.72", "0.56", None),
             ("C12", ("CMA",), D(2014, 1), D(2026, 7), "-1.10", "-0.10", None)]
    for cid, claves, a, b, g, sh, t in cap03:
        nombre = claves[0]
        out.append(comparar_cifra(cid, f"{nombre} {ym(a)} a {ym(b)}, anual %", g, anual(claves, a, b)))
        if sh:
            out.append(comparar_cifra(cid, f"{nombre} {ym(a)} a {ym(b)}, Sharpe", sh, sharpe(claves, a, b)))
        if t:
            out.append(comparar_cifra(cid, f"{nombre} {ym(a)} a {ym(b)}, t", t, tstat(claves, a, b)))
    # C13 muerte del value (usa el calculo del bloque B)
    vb = RESULTADOS["bloque_b"]["value"]
    out.append(comparar_cifra("C13", f"HML caida pico-valle (calc. 3F: {vb['HML']['pico']} a {vb['HML']['valle']}; "
                                     f"5F: {vb['HML5']['pico']} a {vb['HML5']['valle']}) %", "-57.8",
                              {"HML 3F": 100 * vb["HML"]["profundidad"], "HML 5F": 100 * vb["HML5"]["profundidad"]}))
    out.append(comparar_cifra("C13", "HML del valle a 2026-07 %", "+66.8",
                              {"HML 3F": 100 * vb["HML"]["desde_valle_a_2026_07"], "HML 5F": 100 * vb["HML5"]["desde_valle_a_2026_07"]}))
    out.append(comparar_cifra("C13", "HML distancia al pico en 2026-07 %", "-29.6",
                              {"HML 3F": 100 * vb["HML"]["distancia_pico_2026_07"], "HML 5F": 100 * vb["HML5"]["distancia_pico_2026_07"]}))
    p("")
    conteo = {}
    for o in out:
        conteo[o["estado"]] = conteo.get(o["estado"], 0) + 1
    p("Resumen del bloque C: " + "; ".join(f"{k}: {v}" for k, v in sorted(conteo.items())) + f" (de {len(out)} cifras).\n")
    RESULTADOS["bloque_c"] = {"cifras": out, "conteo": conteo}
    return out


# ================================================================ bloque D (motor)

def _oso(h) -> bool:
    mk = h.extras["mkt"]
    if len(mk) < MESES_OSO:
        return False
    acum = 1.0
    for _, r in mk[-MESES_OSO:]:
        acum *= 1 + r
    return acum - 1 < 0


def _vol_alta(h) -> bool:
    v = h.extras["vol"]
    n = len(v)
    if n < MIN_MESES_VOL:
        return False
    ordenados = sorted(x for _, x in v)
    umbral = ordenados[math.ceil(PERCENTIL_VOL * n) - 1]
    return v[-1][1] > umbral


def senal_osovol_50(h) -> float:
    return 0.5 if (_oso(h) and _vol_alta(h)) else 1.0


def senal_oso_50(h) -> float:
    return 0.5 if _oso(h) else 1.0


def senal_osovol_0(h) -> float:
    return 0.0 if (_oso(h) and _vol_alta(h)) else 1.0


def senal_oso_0(h) -> float:
    return 0.0 if _oso(h) else 1.0


def activo_factor(s: dict, factor_pares: list, ancla: bool = True):
    fechas = [f for f, _ in factor_pares]
    activo = [(f, s["RF"].mapa[f] + r) for f, r in factor_pares]
    efectivo = [(f, s["RF"].mapa[f]) for f in fechas]
    if ancla:
        a = fin_mes_previo(fechas[0])
        activo = [(a, 0.0)] + activo
        efectivo = [(a, 0.0)] + efectivo
    return activo, efectivo


def correr(s, variante, activo, efectivo, senal, cortes, *, es_prueba, nota, costo=(0.0, 0.0),
           min_historia=1, extras=None, parametros=None):
    fuente = (f"French CRSP {RESULTADOS['datos']['3F']['version_crsp']} (3F sha {RESULTADOS['datos']['3F']['sha256'][:12]}, "
              f"Mom sha {RESULTADOS['datos']['Mom']['sha256'][:12]}, 5F sha {RESULTADOS['datos']['5F']['sha256'][:12]})")
    return bt.backtest_senal(activo, efectivo, senal, id_replica=ID, variante=variante,
                             comision_por_lado=costo[0], spread_por_lado=costo[1], min_historia=min_historia,
                             exposicion_min=0.0, exposicion_max=1.0, cortes=list(cortes), extras=extras,
                             parametros=parametros or {}, fuente_datos=fuente, es_prueba=es_prueba, nota=nota)


def nw_exceso(r, i0, i1):
    ex = [a - b for a, b in zip(r.r_neto[i0:i1], r.r_efectivo[i0:i1])]
    if len(ex) < 3 or statistics.pstdev(ex) == 0:
        return None
    return est.newey_west(ex, REZAGOS_NW)["t"]


def indices_segmentos(r) -> dict:
    lims = [0] + [bisect_right(r.fechas, date.fromisoformat(c)) for c in r.parametros["cortes"]] + [len(r.fechas)]
    nombres = ["completo"] + list(r.segmentos)
    out = {"completo": (0, len(r.fechas))}
    for k, nombre in enumerate(r.segmentos):
        out[nombre] = (lims[k], lims[k + 1])
    return {n: out[n] for n in nombres}


def tabla_motor(resultados: list, segmento: str) -> None:
    claves = ("n_periodos", "cagr", "vol_anual", "sharpe", "sortino", "mdd", "exposicion_media", "rotacion_anual", "costo_anual")
    p(f"| variante ({segmento}) | costo/lado | inicio | fin | " + " | ".join(claves) + " | t NW exceso |")
    p("|---|---|---|---|" + "---|" * (len(claves) + 1))
    for r in resultados:
        x = r.metricas[segmento]
        i0, i1 = indices_segmentos(r)[segmento]
        c = r.parametros["comision_por_lado"] + r.parametros["spread_por_lado"]
        p(f"| {r.variante} | {100 * c:.2f}% | {x['fecha_inicio']} | {x['fecha_fin']} | " +
          " | ".join(str(x[k]) if k == "n_periodos" else fmt(x[k]) for k in claves) + f" | {fmt(nw_exceso(r, i0, i1), 2)} |")
    p("")


def bloque_d(s: dict, a_res: dict) -> dict:
    p("# Bloque D. Corridas del motor (herramientas/backtest.py), registradas en R03-variantes.csv\n")
    res = {}
    # ---------- familia F
    especificacion = {}
    for f in FACTORES:
        cfg = TRAMOS[f]
        especificacion[f"F_{f}"] = (s[f].pares(cfg["is_ini"]), (cfg["is_fin"], cfg["pub"]), f)
    ew_fechas = s["RMW"].fechas
    ew = [(d, (s["SMB"].mapa[d] + s["HML"].mapa[d] + s["MOM"].mapa[d] + s["RMW"].mapa[d] + s["CMA"].mapa[d]) / 5)
          for d in ew_fechas]
    especificacion["F_EW5"] = (ew, (date(2013, 12, 31), date(2015, 4, 30)), "EW5")
    principales, referencias = [], []
    for var, (pares, cortes, f) in especificacion.items():
        act, efe = activo_factor(s, pares)
        r = correr(s, var, act, efe, bt.senal_comprar_y_mantener, cortes, es_prueba=True,
                   nota="principal bruta (como el articulo)",
                   parametros={"factor": f, "inicio": str(pares[0][0]), "cortes": [str(c) for c in cortes],
                               "ancla": "periodo 0.0 en el fin del mes previo"})
        principales.append(r)
        # verificacion motor vs calculo directo (seccion 7 del pre-registro)
        if f in TRAMOS:
            directo = a_res["tramos"][f]
            for seg, clave in (("desarrollo", "IS"), ("validacion", "OOS"), ("prueba", "POST")):
                m = r.metricas[seg]
                if m["n_periodos"] != directo[clave]["n"] or abs(m["sharpe"] - directo[clave]["sharpe"]) > 1e-9:
                    raise SystemExit(f"{var} {seg}: motor n={m['n_periodos']} sharpe={m['sharpe']} vs directo "
                                     f"n={directo[clave]['n']} sharpe={directo[clave]['sharpe']}")
        mk_pares = s["MKT"].pares(pares[0][0])
        act_m, efe_m = activo_factor(s, mk_pares)
        referencias.append(correr(s, f"REF_MKT_{f}", act_m, efe_m, bt.senal_comprar_y_mantener, cortes,
                                  es_prueba=False, nota="referencia: mercado comprar y mantener, mismo periodo y cortes",
                                  parametros={"serie": "Mkt-RF+RF", "inicio": str(pares[0][0])}))
    p("Verificacion: en SMB, HML, MOM, RMW y CMA el motor reproduce n y Sharpe del calculo directo en "
      "desarrollo = IS, validacion = OOS y prueba = POST (diferencia < 1e-9).\n")
    for seg in ("desarrollo", "validacion", "prueba", "completo"):
        p(f"### D.1 Familia F, segmento {seg} (brutas)\n")
        tabla_motor(principales + referencias, seg)
    # ---------- familia MOM (control de crash)
    mom_pares = s["MOM"].pares()
    act, efe = activo_factor(s, mom_pares, ancla=False)
    extras = {"mkt": s["MKT_TOTAL"].pares(), "vol": s["VOL"].pares()}
    senales = {"MOM_ctrl_osovol_50": senal_osovol_50, "MOM_ctrl_oso_50": senal_oso_50,
               "MOM_ctrl_osovol_0": senal_osovol_0, "MOM_ctrl_oso_0": senal_oso_0}
    mom_res = []
    for var, sen in senales.items():
        mom_res.append(correr(s, var, act, efe, sen, CORTES_MOM, es_prueba=True, nota="principal bruta",
                              min_historia=MIN_HISTORIA_MOM, extras=extras,
                              parametros={"meses_oso": MESES_OSO, "percentil_vol": PERCENTIL_VOL,
                                          "min_meses_vol": MIN_MESES_VOL, "min_dias_vol": MIN_DIAS_VOL}))
    refs_mom = [
        correr(s, "MOM_ref_siempre", act, efe, bt.senal_comprar_y_mantener, CORTES_MOM, es_prueba=False,
               nota="referencia", min_historia=MIN_HISTORIA_MOM, extras=extras),
        correr(s, "MOM_ref_efectivo", act, efe, bt.senal_efectivo, CORTES_MOM, es_prueba=False,
               nota="referencia", min_historia=MIN_HISTORIA_MOM, extras=extras),
        correr(s, "MOM_ref_sma10", act, efe, bt.senal_media_movil(10), CORTES_MOM, es_prueba=False,
               nota="referencia: regla sencilla del mismo tipo", min_historia=MIN_HISTORIA_MOM, extras=extras),
    ]
    act_mk, efe_mk = activo_factor(s, s["MKT"].pares(date(1927, 1, 31)), ancla=False)
    refs_mom.append(correr(s, "MKT_ref_mom", act_mk, efe_mk, bt.senal_comprar_y_mantener, CORTES_MOM, es_prueba=False,
                           nota="referencia: mercado", min_historia=MIN_HISTORIA_MOM, extras=extras))
    for seg in ("desarrollo", "validacion", "prueba", "completo"):
        p(f"### D.2 Familia MOM (control de crash), segmento {seg} (brutas)\n")
        tabla_motor(mom_res + refs_mom, seg)
    p("Meses con exposicion < 1 (regla activa) por segmento:\n")
    p("| variante | " + " | ".join(("desarrollo", "validacion", "prueba", "completo")) + " | ultimo mes activo |")
    p("|---|---|---|---|---|---|")
    activos = {}
    for r in mom_res:
        seg_idx = indices_segmentos(r)
        cuenta = {k: sum(1 for w in r.exposicion[a:b] if w < 1) for k, (a, b) in seg_idx.items()}
        ult = max((f for f, w in zip(r.fechas, r.exposicion) if w < 1), default=None)
        activos[r.variante] = {**cuenta, "ultimo": str(ult)}
        p(f"| {r.variante} | {cuenta['desarrollo']} | {cuenta['validacion']} | {cuenta['prueba']} | {cuenta['completo']} | {ult} |")
    p("")
    # Mom en los 15 peores meses bajo cada control
    peores = sorted(s["MOM"].pares(date(1927, 11, 30)), key=lambda x: x[1])[:15]
    p("Rendimiento neto del mes (%) en los 15 peores meses de Mom (desde 1927-11), por variante:\n")
    p("| Mes | Mom | " + " | ".join(r.variante for r in mom_res) + " |")
    p("|---|---|" + "---|" * len(mom_res))
    for d, v in peores:
        celdas = []
        for r in mom_res:
            i = r.fechas.index(d)
            celdas.append(f"{pct(r.r_neto[i] - r.r_efectivo[i])} (w={r.exposicion[i]:.1f})")
        p(f"| {ym(d)} | {pct(v)} | " + " | ".join(celdas) + " |")
    p("(Columnas de variantes: exceso sobre RF del mes y exposicion w.)\n")
    # H6
    ref = refs_mom[0]
    regla = mom_res[0]
    h6 = {}
    for seg in ("desarrollo", "validacion", "prueba", "completo"):
        a, b = regla.metricas[seg], ref.metricas[seg]
        h6[seg] = {"sharpe_regla": a["sharpe"], "sharpe_ref": b["sharpe"], "mdd_regla": a["mdd"], "mdd_ref": b["mdd"],
                   "mejor_sharpe": a["sharpe"] > b["sharpe"], "mejor_mdd": a["mdd"] > b["mdd"],
                   "meses_activa": activos[regla.variante][seg]}
    dentro = h6["desarrollo"]["mejor_sharpe"] and h6["desarrollo"]["mejor_mdd"]
    if h6["prueba"]["meses_activa"] == 0:
        fuera = "no informativa (la regla no se activa en prueba)"
    elif h6["prueba"]["mejor_sharpe"] and h6["prueba"]["mejor_mdd"]:
        fuera = "confirmada fuera de muestra"
    else:
        fuera = "no confirmada fuera de muestra"
    h6["veredicto_dentro"] = "confirmada dentro de muestra" if dentro else "no confirmada dentro de muestra"
    h6["veredicto_fuera"] = fuera
    p(f"H6 ({regla.variante} contra {ref.variante}): desarrollo Sharpe {fmt(h6['desarrollo']['sharpe_regla'])} vs "
      f"{fmt(h6['desarrollo']['sharpe_ref'])}, MDD {fmt(h6['desarrollo']['mdd_regla'])} vs {fmt(h6['desarrollo']['mdd_ref'])} "
      f"-> **{h6['veredicto_dentro']}**; prueba Sharpe {fmt(h6['prueba']['sharpe_regla'])} vs "
      f"{fmt(h6['prueba']['sharpe_ref'])}, MDD {fmt(h6['prueba']['mdd_regla'])} vs {fmt(h6['prueba']['mdd_ref'])}, "
      f"meses activa en prueba {h6['prueba']['meses_activa']} -> **{fuera}**.\n")

    # ---------- sensibilidades del motor (lista cerrada)
    p("### D.3 Sensibilidades del motor\n")
    sens = []
    for costo, nombre in ((COSTO_DEFECTO, "defecto"), (COSTO_MEDIO, "medio")):
        nota = f"sensibilidad: costos {nombre} (solo overlay; no incluye la rotacion interna del factor)"
        for var, (pares, cortes, f) in especificacion.items():
            act_f, efe_f = activo_factor(s, pares)
            sens.append(correr(s, var, act_f, efe_f, bt.senal_comprar_y_mantener, cortes, es_prueba=False, nota=nota,
                               costo=costo, parametros={"factor": f, "inicio": str(pares[0][0]), "cortes": [str(c) for c in cortes],
                                                        "ancla": "periodo 0.0 en el fin del mes previo"}))
            act_m, efe_m = activo_factor(s, s["MKT"].pares(pares[0][0]))
            sens.append(correr(s, f"REF_MKT_{f}", act_m, efe_m, bt.senal_comprar_y_mantener, cortes, es_prueba=False,
                               nota=nota, costo=costo, parametros={"serie": "Mkt-RF+RF", "inicio": str(pares[0][0])}))
        for var, sen in senales.items():
            sens.append(correr(s, var, act, efe, sen, CORTES_MOM, es_prueba=False, nota=nota, costo=costo,
                               min_historia=MIN_HISTORIA_MOM, extras=extras,
                               parametros={"meses_oso": MESES_OSO, "percentil_vol": PERCENTIL_VOL,
                                           "min_meses_vol": MIN_MESES_VOL, "min_dias_vol": MIN_DIAS_VOL}))
        for var, sen in (("MOM_ref_siempre", bt.senal_comprar_y_mantener), ("MOM_ref_efectivo", bt.senal_efectivo),
                         ("MOM_ref_sma10", bt.senal_media_movil(10))):
            sens.append(correr(s, var, act, efe, sen, CORTES_MOM, es_prueba=False, nota=nota, costo=costo,
                               min_historia=MIN_HISTORIA_MOM, extras=extras))
        sens.append(correr(s, "MKT_ref_mom", act_mk, efe_mk, bt.senal_comprar_y_mantener, CORTES_MOM, es_prueba=False,
                           nota=nota, costo=costo, min_historia=MIN_HISTORIA_MOM, extras=extras))
    p("Costos (solo overlay), segmento prueba — familia MOM:\n")
    tabla_motor([r for r in sens if r.variante.startswith(("MOM_", "MKT_ref"))], "prueba")
    p("Costos (solo overlay), segmento prueba — familia F:\n")
    tabla_motor([r for r in sens if r.variante.startswith(("F_", "REF_MKT"))], "prueba")
    otros = []
    for f in ("SMB", "RMW", "CMA"):
        cfg = TRAMOS[f]
        pares = s[f].pares(cfg["is_ini"])
        act_f, efe_f = activo_factor(s, pares)
        otros.append(correr(s, f"F_{f}_altfecha", act_f, efe_f, bt.senal_comprar_y_mantener, (cfg["is_fin"], cfg["alt"]),
                            es_prueba=False, nota="sensibilidad: fecha de publicacion alternativa",
                            parametros={"factor": f, "corte_pub": str(cfg["alt"])}))
    for f, clave in (("SMB", "SMB5"), ("HML", "HML5")):
        cfg = TRAMOS[f]
        pares = s[clave].pares()
        act_f, efe_f = activo_factor(s, pares)
        otros.append(correr(s, f"F_{f}_ff5", act_f, efe_f, bt.senal_comprar_y_mantener, (cfg["is_fin"], cfg["pub"]),
                            es_prueba=False, nota="sensibilidad: archivo de 5 factores", parametros={"factor": clave}))
    for f in ("SMB", "HML", "MOM"):
        cfg = TRAMOS[f]
        pares = s[f].pares()
        act_f, efe_f = activo_factor(s, pares)
        otros.append(correr(s, f"F_{f}_hist", act_f, efe_f, bt.senal_comprar_y_mantener, (cfg["is_fin"], cfg["pub"]),
                            es_prueba=False, nota="sensibilidad: historia completa (desarrollo incluye pre-muestra)",
                            parametros={"factor": f, "inicio": str(pares[0][0])}))
    for seg in ("desarrollo", "validacion", "prueba"):
        p(f"Fechas alternativas, archivo 5F e historia completa — segmento {seg}:\n")
        tabla_motor(otros, seg)

    # ---------- DSR
    p("### D.4 Sharpe deflactado (DSR) con el registro R03-variantes.csv\n")
    filas = bt.leer_registro(ID)
    familias = {"F": [f"F_{f}" for f in FACTORES] + ["F_EW5"], "MOM": list(senales)}

    def var_familia(seg, nombres):
        unicas = {}
        for fila in filas:
            if fila["segmento"] == seg and fila["es_prueba"] == 1 and fila["variante"] in nombres:
                unicas[(fila["variante"], fila["parametros_json"])] = fila
        srs = [f["sharpe_periodo"] for f in unicas.values() if f["sharpe_periodo"] is not None]
        return statistics.variance(srs), max(unicas.values(), key=lambda f: f["sharpe_periodo"])["variante"]

    dsr = []
    for seg in ("desarrollo", "prueba"):
        d0 = bt.sharpe_deflactado_de_registro(ID, segmento=seg)
        dsr.append(("Por defecto: mejor de las 10, V de todas", d0))
        for fam, nombres in familias.items():
            v, mejor = var_familia(seg, nombres)
            dsr.append((f"Mejor de la familia {fam}, V de {fam}",
                        bt.sharpe_deflactado_de_registro(ID, n_pruebas=d0["n_registradas"], varianza_sharpes=v,
                                                         segmento=seg, variante=mejor)))
        for nombre in familias["F"] + familias["MOM"]:
            dsr.append(("Pre-especificada, V de todas", bt.sharpe_deflactado_de_registro(ID, segmento=seg, variante=nombre)))
    p("| Lectura | Segmento | Variante | DSR | ¿Cumple 0.95? | N | V por periodo | SR anual | SR0 anual | n_obs | PSR sin deflactar |")
    p("|---|---|---|---|---|---|---|---|---|---|---|")
    for lectura, d in dsr:
        p(f"| {lectura} | {d['segmento']} | {d['variante']} | {fmt(d['dsr'])} | {'si' if d['cumple'] else 'no'} | "
          f"{d['n_pruebas']} | {fmt(d['varianza_sharpes_periodo'], 6)} | {fmt(d['sr_anual'])} | {fmt(d['sr0_anual'])} | "
          f"{d['n_obs']} | {fmt(d['psr_sin_deflactar'])} |")
    p("")
    res["dsr"] = [{"lectura": l, **{k: v for k, v in d.items()}} for l, d in dsr]
    res["H6"] = h6
    res["activos"] = activos
    res["n_corridas"] = len(principales) + len(referencias) + len(mom_res) + len(refs_mom) + len(sens) + len(otros)
    res["metricas_principales"] = {r.variante: {seg: {k: r.metricas[seg][k] for k in ("n_periodos", "cagr", "sharpe", "mdd", "vol_anual")}
                                                for seg in ["completo"] + r.segmentos} for r in principales + mom_res + refs_mom + referencias}
    res["curva_hml_hist"] = next(r for r in otros if r.variante == "F_HML_hist")
    p(f"Corridas del motor en esta ejecucion: {res['n_corridas']} (cada una agrega 4 filas al CSV: completo + 3 segmentos).\n")
    return res


# ================================================================ principal

def main() -> None:
    inicio = datetime.now(timezone.utc)
    p(f"# R03 — salida de `python3 laboratorio/replicas/R03.py` ({inicio.strftime('%Y-%m-%dT%H:%M:%SZ')})\n")
    s = cargar()
    a_res = bloque_a(s)
    b_res = bloque_b(s)
    bloque_c(s)
    d_res = bloque_d(s, a_res)
    # "muerte del value" con la curva RF+HML del motor (sensibilidad del bloque B)
    r = d_res.pop("curva_hml_hist")
    curva = r.curva
    fechas = [c[0] for c in curva]
    vals = [c[1] for c in curva]
    mx, imx, peor, ip, iv = -1, 0, 0.0, 0, 0
    for i, v in enumerate(vals):
        if v > mx:
            mx, imx = v, i
        if date(2007, 1, 1) <= fechas[i] <= date(2020, 12, 31) and v / mx - 1 < peor:
            peor, ip, iv = v / mx - 1, imx, i
    p(f"Sensibilidad B.6 con la curva RF+HML del motor (F_HML_hist, bruta): pico {ym(fechas[ip])}, valle {ym(fechas[iv])}, "
      f"profundidad {pct(peor, 1)}%; del valle a 2026-07 {pct(vals[-1] / vals[iv] - 1, 1)}%; distancia al pico "
      f"{pct(vals[-1] / vals[ip] - 1, 1)}%.\n")
    RESULTADOS["bloque_b"]["value"]["RF+HML_motor"] = {"pico": ym(fechas[ip]), "valle": ym(fechas[iv]), "profundidad": peor,
                                                       "desde_valle": vals[-1] / vals[iv] - 1, "distancia": vals[-1] / vals[ip] - 1}
    # ---------- estado pre-registrado
    mp, bs = a_res["mp"], a_res["bs"]
    D, (lo, hi) = mp["D"], bs["ic_D"]
    todos_bajan = all(v["POST"]["media"] < v["IS"]["media"] for v in mp["por_factor"].values())
    lista_dec = ", ".join(f + ": " + pct(v["decaimiento_post"], 1) + "%" for f, v in mp["por_factor"].items())
    if D <= 0 or a_res["fallas_a"] >= 2:
        estado = "No replicado"
    elif a_res["condicion_a"] and lo > 0 and lo <= MP_POST <= hi and todos_bajan:
        estado = "Replicado"
    else:
        estado = "Replicado con diferencias"
    p("# Estado pre-registrado\n")
    p(f"- Condicion A: {'se cumple' if a_res['condicion_a'] else 'no se cumple'} (fallas: {a_res['fallas_a']}).")
    p(f"- D = {pct(D, 1)}%, IC95 [{pct(lo, 1)}%, {pct(hi, 1)}%]; ¿limite inferior > 0?: {'si' if lo > 0 else 'no'}; "
      f"¿contiene 58%?: {'si' if lo <= MP_POST <= hi else 'no'}.")
    p(f"- ¿Los cinco factores tienen media POST < media IS?: {'si' if todos_bajan else 'no'} "
      f"({lista_dec}).")
    p(f"- **Estado: {estado}.** H4: {'confirmada' if b_res['H4']['confirmada'] else 'no confirmada'}; "
      f"H5: {'confirmada' if b_res['H5']['confirmada'] else 'no confirmada'}; "
      f"H6: {d_res['H6']['veredicto_dentro']} / {d_res['H6']['veredicto_fuera']}.\n")
    RESULTADOS["estado"] = estado
    RESULTADOS["bloque_d"] = {k: v for k, v in d_res.items()}
    fin = datetime.now(timezone.utc)
    RESULTADOS["corrida"] = {"inicio_utc": inicio.isoformat(), "fin_utc": fin.isoformat()}
    p(f"Fin: {fin.strftime('%Y-%m-%dT%H:%M:%SZ')}.")
    carpeta = Path(__file__).resolve().parent
    (carpeta / "R03-salida.txt").write_text(SALIDA.getvalue(), encoding="utf-8")
    (carpeta / "R03-resultados.json").write_text(json.dumps(RESULTADOS, indent=1, ensure_ascii=False, default=str),
                                                 encoding="utf-8")


if __name__ == "__main__":
    main()
