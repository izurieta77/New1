#!/usr/bin/env python3
"""R02 - Momentum de series de tiempo (Moskowitz, Ooi y Pedersen, 2012, JFE 104(2):228-250).

Reproduce desde la raiz del repo:  python3 laboratorio/replicas/R02.py
Solo biblioteca estandar. Cada corrida se agrega a laboratorio/replicas/R02-variantes.csv.

Partes (ver el pre-registro en R02-momentum-series-de-tiempo.md, secciones 1-9):
  (a) Mercado total de EUA (French, Mkt-RF + RF) desde 1926, volatilidad ex ante con
      Mkt-RF diario (EWMA, centro de masa de 60 dias, x261), variantes L = 3/6/12.
  (b) 8 ETFs (SPY, EFA, EEM, TLT, IEF, GLD, DBC, VNQ) desde que existen todos, con
      volatilidad objetivo por activo. Motor de cartera propio (backtest_cartera) que
      replica el modelo de tiempo y costos de herramientas/backtest.py; antes de usarlo
      se comprueba contra backtest_senal con datos sinteticos.
Corte unico 2011-12-31 (el articulo estuvo en linea desde el 11-dic-2011):
dentro_muestra <= 2011-12, fuera_muestra = 2012-01 en adelante.
"""
from __future__ import annotations

import math
import random
import statistics
import sys
import types
from bisect import bisect_right
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Callable, Mapping

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from herramientas import backtest as bt  # noqa: E402
from herramientas import datos_historicos as dh  # noqa: E402
from herramientas import estadistica as est  # noqa: E402

# ================================================================ parametros pre-registrados
ID = "R02"
CORTE = date(2011, 12, 31)
LOOKBACKS = (3, 6, 12)
SIGMA_ARTICULO = 0.40      # volatilidad ex ante por posicion (MOP ec. 5)
SIGMA_OPERABLE = 0.10      # volatilidad objetivo por activo en la version solo-largos
TOPE_APALANCAMIENTO = 10.0  # |0.40/sigma| <= 10
DELTA = 60.0 / 61.0        # centro de masa delta/(1-delta) = 60 dias
ANUALIZA = 261             # MOP ec. 1
MIN_DIAS_VOL = 120
MAX_DIAS_VOL_VIEJA = 10    # la ultima vol visible no puede tener mas de 10 dias
MIN_HISTORIA = 12
ETFS = ("SPY", "EFA", "EEM", "TLT", "IEF", "GLD", "DBC", "VNQ")
COMISION = bt.COMISION_GBM_POR_LADO
ESCENARIOS = {  # nombre -> (comision, spread, es_sensibilidad, nota)
    "defecto": (COMISION, bt.SPREAD_POR_LADO["liquido"], False, ""),
    "medio": (COMISION, bt.SPREAD_POR_LADO["medio"], True, "sensibilidad: spread medio 0.15% por lado"),
    "bruto": (0.0, 0.0, True, "sensibilidad: bruto (sin comision ni spread)"),
}


# ================================================================ volatilidad ex ante (EWMA)

def construir_vol_ewma(rend_diarios: list) -> list:
    """[(fecha, r)] diarios -> [(fecha, sigma anual | None)]. Varianza ponderada normalizada:
    E_w[r^2] - E_w[r]^2 con pesos (1-d) d^i divididos entre 1 - d^n; sigma = sqrt(261 var).
    Causal por construccion (el valor en d usa rendimientos <= d); se audita con
    bt.auditar_constructor antes de usarla."""
    s0 = s1 = s2 = 0.0
    salida = []
    for k, (f, r) in enumerate(rend_diarios, start=1):
        s0 = DELTA * s0 + (1 - DELTA)
        s1 = DELTA * s1 + (1 - DELTA) * r
        s2 = DELTA * s2 + (1 - DELTA) * r * r
        if k < MIN_DIAS_VOL:
            salida.append((f, None))
            continue
        media = s1 / s0
        var = max(s2 / s0 - media * media, 0.0)
        salida.append((f, math.sqrt(ANUALIZA * var)))
    return salida


def vol_como_extra(rend_diarios: list, nombre: str) -> list:
    auditoria = bt.auditar_constructor(construir_vol_ewma, rend_diarios, n_cortes=12, semilla=2)
    if not auditoria["causal"]:
        raise bt.ErrorLookAhead(f"vol {nombre}: {auditoria['primer_fallo']}")
    return [(f, v) for f, v in construir_vol_ewma(rend_diarios) if v is not None and v > 0]


# ================================================================ piezas de las senales (puras)

def _signo_exceso(activo, efectivo, L: int) -> float:
    """+1 si el rendimiento acumulado de L periodos supera al del efectivo, si no -1."""
    if len(activo) < L:
        raise ValueError(f"momentum {L}: historia de {len(activo)}")
    acum_a = math.prod(1 + r for r in activo[-L:])
    acum_e = math.prod(1 + r for r in efectivo[-L:])
    return 1.0 if acum_a > acum_e else -1.0


def _ultima_vol(serie, fecha_decision) -> float:
    if not len(serie):
        raise ValueError("sin volatilidad visible")
    f, v = serie[-1]
    if (fecha_decision - f).days > MAX_DIAS_VOL_VIEJA:
        raise ValueError(f"volatilidad vieja: {f} para decidir en {fecha_decision}")
    return v


# ---- parte (a): senales de un activo (reciben bt.Historia)

def senal_a_ls_vt(L: int, objetivo: float, tope: float):
    def senal(h):
        s = _signo_exceso(h.activo, h.efectivo, L)
        w = s * objetivo / _ultima_vol(h.extras["vol"], h.fecha_decision)
        return max(-tope, min(tope, w))
    senal.__qualname__ = senal.__name__ = f"a_ls_vt{int(objetivo * 100)}_L{L}"
    return senal


def senal_a_lo(L: int):
    def senal(h):
        return 1.0 if _signo_exceso(h.activo, h.efectivo, L) > 0 else 0.0
    senal.__qualname__ = senal.__name__ = f"a_lo_L{L}"
    return senal


def senal_a_largo_vt(objetivo: float, tope: float):
    def senal(h):
        return min(tope, objetivo / _ultima_vol(h.extras["vol"], h.fecha_decision))
    senal.__qualname__ = senal.__name__ = f"a_largo_vt{int(objetivo * 100)}"
    return senal


# ---- parte (b): senales de cartera (reciben HistoriaCartera y devuelven {ticker: peso})

def senal_cartera(modo: str, tickers: tuple, L: int = 12, objetivo: float = 0.0, tope: float = 1.0):
    """modos: ls_vt, lo_vt, lo, ref_1n, ref_1n_sin_rebalanceo, ref_sma10, ref_vt, ref_largo_vt."""
    n = len(tickers)

    def senal(h):
        pesos = {}
        if modo == "ref_1n_sin_rebalanceo":
            previos = h.pesos_actuales
            if sum(abs(w) for w in previos.values()) == 0:
                return {k: 1.0 / n for k in tickers}
            rb = sum(previos[k] * h.activos[k][-1] for k in tickers) \
                + (1 - sum(previos.values())) * h.efectivo[-1]
            return {k: previos[k] * (1 + h.activos[k][-1]) / (1 + rb) for k in tickers}
        for k in tickers:
            if modo == "ref_1n":
                pesos[k] = 1.0 / n
            elif modo == "ref_sma10":
                ult = h.indices[k][-10:]
                if len(ult) < 10:
                    raise ValueError("sma10: historia corta")
                pesos[k] = (1.0 / n) if ult[-1] > statistics.fmean(ult) else 0.0
            else:
                sigma = _ultima_vol(h.extras["vol_" + k], h.fecha_decision)
                if modo == "ref_vt":
                    pesos[k] = min(1.0, objetivo / sigma) / n
                elif modo == "ref_largo_vt":
                    pesos[k] = min(tope, objetivo / sigma) / n
                else:
                    s = _signo_exceso(h.activos[k], h.efectivo, L)
                    if modo == "ls_vt":
                        pesos[k] = s * min(tope, objetivo / sigma) / n
                    elif modo == "lo_vt":
                        pesos[k] = (1.0 if s > 0 else 0.0) * min(1.0, objetivo / sigma) / n
                    elif modo == "lo":
                        pesos[k] = (1.0 if s > 0 else 0.0) / n
                    else:
                        raise ValueError(f"modo desconocido {modo}")
        return pesos
    senal.__qualname__ = senal.__name__ = f"cartera_{modo}_L{L}_obj{objetivo}_tope{tope}"
    return senal


# ================================================================ motor de cartera

@dataclass(frozen=True, slots=True)
class HistoriaCartera:
    """Lo que ve la senal de cartera al decidir t: todo termina en t-1 (vistas de solo lectura)."""
    fechas: bt.Vista
    activos: Mapping
    indices: Mapping
    efectivo: bt.Vista
    extras: Mapping
    pesos_actuales: Mapping

    def __len__(self) -> int:
        return len(self.fechas)

    @property
    def fecha_decision(self):
        return self.fechas[-1] if len(self.fechas) else None


def backtest_cartera(activos: dict, efectivo, senal: Callable, *, id_replica: str | None, variante: str,
                     comision_por_lado: float = COMISION, spread_por_lado: float = bt.SPREAD_POR_LADO_DEFECTO,
                     min_historia: int = 1, peso_min: float = 0.0, peso_max: float = 1.0,
                     bruto_max: float = 1.0, cortes=(), fx=None, efectivo_en_mxn: bool = False,
                     max_dias_fx: int = 10, extras: dict | None = None, parametros: dict | None = None,
                     fuente_datos: str = "", es_prueba: bool = True, nota: str = "") -> bt.ResultadoBacktest:
    """Version multiactivo de bt.backtest_senal con el MISMO modelo de tiempo y costos:
    w_pre_i = w_{t-1,i}(1+ra_{t-1,i})/(1+rb_{t-1}); costo = sum_i |w_i - w_pre_i| (com + spread);
    rb = sum_i w_i ra_i + (1 - sum_i w_i) re; r_neto = rb - costo (1 + rb).
    'exposicion' = suma neta de pesos; meta['pesos'] guarda los pesos por activo."""
    if not variante or min_historia < 1:
        raise ValueError("variante obligatoria y min_historia >= 1")
    tickers = tuple(activos)
    series = {k: bt._validar_serie(v, f"activo {k}") for k, v in activos.items()}
    if isinstance(efectivo, (int, float)):
        base = series[tickers[0]]
        serie_ef = [(f, float(efectivo)) for f, _ in base]
    else:
        serie_ef = bt._validar_serie(efectivo, "efectivo")
    mapas = {k: dict(v) for k, v in series.items()}
    mapa_ef = dict(serie_ef)
    comunes = set(mapa_ef)
    for mp in mapas.values():
        comunes &= set(mp)
    fechas = sorted(comunes)
    n = len(fechas)
    if n < min_historia + 3:
        raise ValueError(f"Muy pocos periodos alineados ({n})")
    ra_orig = {k: [mapas[k][f] for f in fechas] for k in tickers}
    re_orig = [mapa_ef[f] for f in fechas]
    ppa = bt.inferir_periodos_por_anio(fechas)

    factor_fx = [None] * n
    serie_fx = None
    if fx is not None:
        serie_fx = bt._validar_serie(fx, "fx")
        fx_f = [f for f, _ in serie_fx]
        fx_v = [v for _, v in serie_fx]
        previo = bt._valor_en_o_antes(fx_f, fx_v, fechas[0])
        for t in range(1, n):
            actual = bt._valor_en_o_antes(fx_f, fx_v, fechas[t])
            if previo is not None and actual is not None \
                    and (fechas[t] - actual[0]).days <= max_dias_fx \
                    and (fechas[t - 1] - previo[0]).days <= max_dias_fx:
                factor_fx[t] = actual[1] / previo[1]
            previo = actual
        disponibles = [t for t in range(n) if factor_fx[t] is not None]
        if not disponibles:
            raise ValueError("fx no cubre ningun periodo")
        huecos = [fechas[t] for t in range(max(disponibles[0], min_historia), n) if factor_fx[t] is None]
        if huecos:
            raise ValueError(f"fx con huecos en {huecos[:5]}")
        inicio = max(min_historia, disponibles[0])
        moneda = "MXN"
    else:
        inicio = min_historia
        moneda = "USD"

    def convertir(r: float, t: int, es_efectivo: bool) -> float:
        if factor_fx[t] is None or (es_efectivo and efectivo_en_mxn):
            return r
        return (1 + r) * factor_fx[t] - 1

    extras = dict(extras or {})
    if serie_fx is not None:
        extras["fx"] = serie_fx
    extras_val = {k: bt._validar_serie(v, f"extras[{k}]") for k, v in extras.items()}

    capturas = bt.buscar_capturas(senal, n)
    if capturas:
        raise bt.ErrorLookAhead("La senal de cartera captura series completas: " + "; ".join(capturas[:5]))

    vis_fechas, vis_ef = [], []
    vis_act = {k: [] for k in tickers}
    vis_idx = {k: [] for k in tickers}
    vis_extras = {k: [] for k in extras_val}
    punteros = {k: 0 for k in extras_val}

    pesos_hist, exposicion, bruta, rotacion, costo, ordenes = [], [], [], [], [], []
    r_a, r_e, r_b, r_n, fechas_eval = [], [], [], [], []
    w_prev = {k: 0.0 for k in tickers}
    ra_prev = None
    rb_prev = None
    for t in range(n):
        if t >= inicio:
            h = HistoriaCartera(
                fechas=bt.Vista(vis_fechas, t),
                activos=types.MappingProxyType({k: bt.Vista(vis_act[k], t) for k in tickers}),
                indices=types.MappingProxyType({k: bt.Vista(vis_idx[k], t) for k in tickers}),
                efectivo=bt.Vista(vis_ef, t),
                extras=types.MappingProxyType({k: bt.Vista(v, len(v)) for k, v in vis_extras.items()}),
                pesos_actuales=types.MappingProxyType(dict(w_prev)))
            propuestos = senal(h)
            if set(propuestos) - set(tickers):
                raise ValueError(f"pesos para activos desconocidos: {set(propuestos) - set(tickers)}")
            w = {k: float(propuestos.get(k, 0.0)) for k in tickers}
            for k, v in w.items():
                if not math.isfinite(v) or not peso_min - 1e-12 <= v <= peso_max + 1e-12:
                    raise ValueError(f"peso {k}={v} fuera de [{peso_min}, {peso_max}] en {fechas[t]}")
            if sum(abs(v) for v in w.values()) > bruto_max + 1e-9:
                raise ValueError(f"exposicion bruta {sum(abs(v) for v in w.values())} > {bruto_max} en {fechas[t]}")
            ra = {k: convertir(ra_orig[k][t], t, False) for k in tickers}
            re_ = convertir(re_orig[t], t, True)
            if t == inicio or rb_prev is None or 1 + rb_prev == 0:
                w_pre = dict(w_prev)
            else:
                w_pre = {k: w_prev[k] * (1 + ra_prev[k]) / (1 + rb_prev) for k in tickers}
            giro = sum(abs(w[k] - w_pre[k]) for k in tickers)
            c = giro * (comision_por_lado + spread_por_lado)
            suma_w = sum(w.values())
            rb = sum(w[k] * ra[k] for k in tickers) + (1 - suma_w) * re_
            rn = rb - c * (1 + rb)
            pesos_hist.append(w)
            exposicion.append(suma_w)
            bruta.append(sum(abs(v) for v in w.values()))
            rotacion.append(giro)
            costo.append(c)
            ordenes.append(sum(1 for k in tickers if abs(w[k] - w_pre[k]) > 1e-12))
            r_a.append(statistics.fmean(ra.values()))  # proxy: 1/N bruto del mes
            r_e.append(re_)
            r_b.append(rb)
            r_n.append(rn)
            fechas_eval.append(fechas[t])
            w_prev, ra_prev, rb_prev = w, ra, rb
        vis_fechas.append(fechas[t])
        vis_ef.append(re_orig[t])
        for k in tickers:
            vis_act[k].append(ra_orig[k][t])
            vis_idx[k].append((vis_idx[k][-1] if vis_idx[k] else 1.0) * (1 + ra_orig[k][t]))
        for k, serie in extras_val.items():
            p = punteros[k]
            while p < len(serie) and serie[p][0] <= fechas[t]:
                vis_extras[k].append(serie[p])
                p += 1
            punteros[k] = p

    fecha_inicial = fechas[inicio - 1]
    curva = [(fecha_inicial, 1.0)]
    for f, r in zip(fechas_eval, r_n):
        curva.append((f, curva[-1][1] * (1 + r)))
    cortes_f = sorted(bt._como_fecha(c) for c in cortes)
    nombres = bt.SEGMENTOS_POR_CORTES.get(len(cortes_f)) or []

    def tramo(i0: int, i1: int) -> dict:
        f0 = fecha_inicial if i0 == 0 else fechas_eval[i0 - 1]
        cambios = sum(1 for j in range(i0, i1)
                      if pesos_hist[j] != (pesos_hist[j - 1] if j > 0 else {k: 0.0 for k in tickers}))
        return bt.metricas_de_periodos(fechas_eval[i0:i1], f0, r_n[i0:i1], r_e[i0:i1], exposicion[i0:i1],
                                       rotacion[i0:i1], costo[i0:i1], r_a[i0:i1], ppa, cambios)

    metricas = {"completo": tramo(0, len(r_n))}
    limites = [0] + [bisect_right(fechas_eval, c) for c in cortes_f] + [len(r_n)]
    for k, nombre in enumerate(nombres if cortes_f else []):
        metricas[nombre] = tramo(limites[k], limites[k + 1])
    config = {
        "variante": variante, "senal": getattr(senal, "__qualname__", repr(senal)),
        "motor": "R02.backtest_cartera", "activos": list(tickers),
        "comision_por_lado": comision_por_lado, "spread_por_lado": spread_por_lado,
        "min_historia": min_historia, "peso_min": peso_min, "peso_max": peso_max, "bruto_max": bruto_max,
        "cortes": [c.isoformat() for c in cortes_f], "segmentos": list(nombres) if cortes_f else [],
        "fx": fx is not None, "efectivo_en_mxn": efectivo_en_mxn, "max_dias_fx": max_dias_fx,
        "periodos_por_anio": ppa, "rebalanceo_con_deriva": True, "extras": sorted(extras_val),
        "usuario": parametros or {},
    }
    huella = bt._huella(fechas, [ra_orig[k] for k in tickers], re_orig, factor_fx)
    res = bt.ResultadoBacktest(
        variante=variante, fechas=fechas_eval, exposicion=exposicion, rotacion=rotacion, costo=costo,
        r_activo=r_a, r_efectivo=r_e, r_bruto=r_b, r_neto=r_n, curva=curva, metricas=metricas,
        segmentos=list(nombres) if cortes_f else [], parametros=config,
        meta={"indice_inicio": inicio, "huella_datos": huella, "moneda": moneda, "fuente_datos": fuente_datos,
              "fuente_costos": bt.FUENTE_COSTOS, "n_alineados": n, "pesos": pesos_hist,
              "exposicion_bruta": bruta, "ordenes": ordenes,
              "r_activos": {k: [convertir(ra_orig[k][t], t, False) for t in range(inicio, n)] for k in tickers}})
    if id_replica is not None:
        res.ruta_registro = bt.registrar_variante(res, id_replica, es_prueba=es_prueba, nota=nota)
    return res


# ================================================================ prueba del motor de cartera

def prueba_consistencia() -> float:
    """backtest_cartera con 1 activo == bt.backtest_senal (datos SINTETICOS, sin registrar)."""
    rnd = random.Random(20260925)
    fechas = [dh.fin_de_mes(2000 + (k // 12), k % 12 + 1) for k in range(240)]
    activo = [(f, rnd.gauss(0.007, 0.05)) for f in fechas]
    ef = [(f, 0.002 + rnd.random() * 0.001) for f in fechas]
    vol = [(f, 0.08 + abs(rnd.gauss(0.12, 0.05))) for f in fechas]
    fx = []
    nivel = 10.0
    for f in fechas:
        nivel *= 1 + rnd.gauss(0.002, 0.03)
        fx.append((f, nivel))
    peor = 0.0
    casos = [("ls", senal_a_ls_vt(12, 0.40, 10.0), -10.0, 10.0),
             ("lo", senal_a_lo(6), 0.0, 1.0),
             ("sma", bt.senal_media_movil(10), 0.0, 1.0)]
    for nombre, s1, lo, hi in casos:
        def envolver(s):
            def senal(h):
                hh = bt.Historia(fechas=h.fechas, activo=h.activos["X"], efectivo=h.efectivo,
                                 indice=h.indices["X"], extras=h.extras,
                                 exposicion_actual=h.pesos_actuales["X"])
                return {"X": s(hh)}
            return senal
        for con_fx in (False, True):
            kw = {"fx": fx} if con_fx else {}
            r1 = bt.backtest_senal(activo, ef, s1, id_replica=None, variante="prueba", min_historia=12,
                                   exposicion_min=lo, exposicion_max=hi, extras={"vol": vol}, cortes=[CORTE],
                                   **kw)
            r2 = backtest_cartera({"X": activo}, ef, envolver(s1), id_replica=None, variante="prueba",
                                  min_historia=12, peso_min=lo, peso_max=hi, bruto_max=max(abs(lo), hi),
                                  extras={"vol": vol}, cortes=[CORTE], **kw)
            if r1.fechas != r2.fechas:
                raise AssertionError(f"fechas distintas en {nombre}")
            for a, b in ((r1.r_neto, r2.r_neto), (r1.costo, r2.costo), (r1.exposicion, r2.exposicion)):
                peor = max(peor, max(abs(x - y) for x, y in zip(a, b)))
            for seg in r1.metricas:
                for clave in ("cagr", "sharpe", "mdd", "rotacion_anual", "costo_anual"):
                    peor = max(peor, abs(r1.metricas[seg][clave] - r2.metricas[seg][clave]))
    if peor > 1e-12:
        raise AssertionError(f"backtest_cartera difiere de backtest_senal: {peor}")
    return peor


# ================================================================ reporte

def fmt(x, d=4) -> str:
    if x is None:
        return "NA"
    if isinstance(x, float):
        return "inf" if math.isinf(x) else f"{x:.{d}f}"
    return str(x)


def ventana(res, f0: date, f1: date) -> dict | None:
    """Metricas del tramo (f0, f1] de una corrida ya hecha + t de Newey-West del exceso."""
    idx = [i for i, f in enumerate(res.fechas) if f0 < f <= f1]
    if len(idx) < 12:
        return None
    i0, i1 = idx[0], idx[-1] + 1
    fecha_ini = res.curva[i0][0]  # curva[i] es el cierre previo al periodo i
    cambios = sum(1 for j in range(i0, i1) if res.exposicion[j] != (res.exposicion[j - 1] if j > 0 else 0.0))
    x = bt.metricas_de_periodos(res.fechas[i0:i1], fecha_ini, res.r_neto[i0:i1], res.r_efectivo[i0:i1],
                                res.exposicion[i0:i1], res.rotacion[i0:i1], res.costo[i0:i1],
                                res.r_activo[i0:i1], res.parametros["periodos_por_anio"], cambios)
    exceso = [a - b for a, b in zip(res.r_neto[i0:i1], res.r_efectivo[i0:i1])]
    if statistics.pstdev(exceso) == 0:  # p. ej. 100% efectivo: exceso identico a 0, t indefinido
        x.update({"nw_t": None, "exceso_medio_anual": statistics.fmean(exceso) * 12})
        return x
    nw = est.newey_west(exceso, 6)
    x.update({"nw_t": nw["t"], "exceso_medio_anual": nw["media"] * 12})
    return x


def limites_segmento(res, segmento: str) -> tuple:
    x = res.metricas[segmento]
    return x["fecha_inicio"], x["fecha_fin"]


def tabla(resultados: list, segmento: str) -> str:
    claves = ("cagr", "vol_anual", "sharpe", "nw_t", "sortino", "mdd", "exposicion_media",
              "rotacion_anual", "costo_anual")
    enc = f"| variante | {' | '.join(claves)} |\n|---|" + "---|" * len(claves)
    filas = [enc]
    for r in resultados:
        f0, f1 = limites_segmento(r, segmento)
        x = dict(r.metricas[segmento])
        v = ventana(r, f0, f1)
        x["nw_t"] = v["nw_t"] if v else None
        filas.append(f"| {r.variante} | " + " | ".join(fmt(x[k]) for k in claves) + " |")
    return "\n".join(filas)


def tabla_ventanas(resultados: list, ventanas: list) -> str:
    enc = "| variante | ventana | n | cagr | vol_anual | sharpe | nw_t | mdd | exposicion_media |\n|---|---|---|---|---|---|---|---|---|"
    filas = [enc]
    for r in resultados:
        for nombre, f0, f1 in ventanas:
            x = ventana(r, f0, f1)
            if x is None:
                continue
            filas.append(f"| {r.variante} | {nombre} ({x['fecha_inicio']} a {x['fecha_fin']}) | {x['n_periodos']} | "
                         f"{fmt(x['cagr'])} | {fmt(x['vol_anual'])} | {fmt(x['sharpe'])} | {fmt(x['nw_t'], 2)} | "
                         f"{fmt(x['mdd'])} | {fmt(x['exposicion_media'])} |")
    return "\n".join(filas)


def descomposicion_timing(res, i0: int, i1: int) -> dict:
    """Solo-largos: media(sum_i W_i ex_i) = sum_i [media(W_i) media(ex_i) + cov(W_i, ex_i)], bruto."""
    pesos = res.meta.get("pesos")
    if pesos is None:  # un activo
        w = res.exposicion[i0:i1]
        ex = [a - b for a, b in zip(res.r_activo[i0:i1], res.r_efectivo[i0:i1])]
        mw, me = statistics.fmean(w), statistics.fmean(ex)
        cov = statistics.fmean([(a - mw) * (b - me) for a, b in zip(w, ex)])
        return {"exposicion_x_prima_anual": mw * me * 12, "timing_anual": cov * 12}
    total_ep = total_cov = 0.0
    for k, serie in res.meta["r_activos"].items():
        w = [p[k] for p in pesos[i0:i1]]
        ex = [a - b for a, b in zip(serie[i0:i1], res.r_efectivo[i0:i1])]
        mw, me = statistics.fmean(w), statistics.fmean(ex)
        total_ep += mw * me
        total_cov += statistics.fmean([(a - mw) * (b - me) for a, b in zip(w, ex)])
    return {"exposicion_x_prima_anual": total_ep * 12, "timing_anual": total_cov * 12}


def indices_segmento(res, f0: date, f1: date) -> tuple:
    idx = [i for i, f in enumerate(res.fechas) if f0 < f <= f1]
    return idx[0], idx[-1] + 1


# ================================================================ principal

def main() -> None:
    print("R02 - momentum de series de tiempo (MOP 2012)")
    difer = prueba_consistencia()
    print(f"Prueba de consistencia backtest_cartera vs backtest_senal (sintetico, con y sin fx): "
          f"diferencia maxima = {difer:.3e}")

    # ------------------------------------------------ datos parte (a)
    ff = dh.french("F-F_Research_Data_Factors", "mensual")
    ffd = dh.french("F-F_Research_Data_Factors_daily", "diaria")
    mercado = dh.rendimiento_mercado_french(ff)
    rf = dh.columna(ff, "RF")
    exceso_diario = dh.columna(ffd, "Mkt-RF")
    vol_mkt = vol_como_extra(exceso_diario, "Mkt-RF diario")
    fuente_a = (f"French F-F_Research_Data_Factors CRSP {ff['version_crsp']} sha256 {ff['sha256'][:16]}; "
                f"daily CRSP {ffd['version_crsp']} sha256 {ffd['sha256'][:16]}")
    print("\n## Datos (a)")
    print(f"- French mensual: {ff['fechas'][0]} a {ff['fechas'][-1]} (n={len(ff['fechas'])}), CRSP {ff['version_crsp']}, "
          f"faltantes={ff['faltantes']}, sha256={ff['sha256']}")
    print(f"- French diario: {ffd['fechas'][0]} a {ffd['fechas'][-1]} (n={len(ffd['fechas'])}), CRSP {ffd['version_crsp']}, "
          f"faltantes={ffd['faltantes']}, sha256={ffd['sha256']}")
    print(f"- Volatilidad EWMA Mkt-RF: auditoria causal OK; {len(vol_mkt)} valores desde {vol_mkt[0][0]}; "
          f"min={min(v for _, v in vol_mkt):.4f}, max={max(v for _, v in vol_mkt):.4f}")

    # ------------------------------------------------ datos parte (b)
    print("\n## Datos (b)")
    mensual, diario, vols = {}, {}, {}
    for k in ETFS:
        hm = dh.yahoo_historia(k, "1mo")
        hd = dh.yahoo_historia(k, "1d")
        mensual[k] = dh.rendimientos_de_precios(hm["fechas"], hm["precios"])
        diario[k] = dh.rendimientos_de_precios(hd["fechas"], hd["precios"])
        vols[k] = vol_como_extra(diario[k], k)
        # chequeo cruzado: rendimiento mensual 1mo contra el de precios diarios a fin de mes
        ultimo = {}
        for f, p in zip(hd["fechas"], hd["precios"]):
            ultimo[(f.year, f.month)] = p
        claves = sorted(ultimo)
        rd = {dh.fin_de_mes(*b): ultimo[b] / ultimo[a] - 1 for a, b in zip(claves, claves[1:])}
        difs = [abs(r - rd[f]) for f, r in mensual[k] if f in rd]
        print(f"- {k}: mensual {hm['fechas'][0]} a {hm['fechas'][-1]} (n={len(hm['fechas'])}), adjclose={hm['usa_adjclose']}, "
              f"moneda={hm['moneda']}, descartes={hm['descartes']}, sin_precio_mensual={len(hm['fechas_sin_precio'])}; "
              f"diario {hd['fechas'][0]} a {hd['fechas'][-1]} (n={len(hd['fechas'])}), sin_precio_diario={hd['fechas_sin_precio'][:5]}"
              f"{'...' if len(hd['fechas_sin_precio']) > 5 else ''} ({len(hd['fechas_sin_precio'])}); "
              f"max |r_1mo - r_diario_fin_de_mes| = {max(difs):.2e} en {len(difs)} meses; vol EWMA auditada")
    comunes = set(dict(rf))
    for k in ETFS:
        comunes &= set(f for f, _ in mensual[k])
    comunes = sorted(comunes)
    print(f"- Muestra comun (b): {comunes[0]} a {comunes[-1]}, n={len(comunes)} meses")
    fuente_b = (f"Yahoo chart v8 adjclose 1mo/1d {','.join(ETFS)} (descarga 2026-09-25); RF French CRSP "
                f"{ff['version_crsp']} sha256 {ff['sha256'][:16]}")
    extras_b = {"vol_" + k: vols[k] for k in ETFS}

    # ------------------------------------------------ corridas
    resultados: dict = {}

    def correr_a(nombre, senal, lo, hi, escenario, es_ref, params, fx=None, nota_extra=""):
        com, spr, es_sens, nota = ESCENARIOS[escenario]
        es_prueba = not es_ref and not es_sens and fx is None
        notas = [n for n in (("referencia" if es_ref else ""), nota, nota_extra) if n]
        r = bt.backtest_senal(mercado, rf, senal, id_replica=ID, variante=nombre, comision_por_lado=com,
                              spread_por_lado=spr, min_historia=MIN_HISTORIA, exposicion_min=lo,
                              exposicion_max=hi, cortes=[CORTE], extras={"vol": vol_mkt}, fx=fx,
                              parametros={**params, "parte": "a", "escenario_costos": escenario},
                              fuente_datos=fuente_a, es_prueba=es_prueba, nota="; ".join(notas))
        resultados[(nombre, escenario, "MXN" if fx else "USD")] = r
        return r

    def correr_b(nombre, senal, lo, hi, bruto, escenario, es_ref, params, fx=None, nota_extra=""):
        com, spr, es_sens, nota = ESCENARIOS[escenario]
        es_prueba = not es_ref and not es_sens and fx is None
        notas = [n for n in (("referencia" if es_ref else ""), nota, nota_extra) if n]
        r = backtest_cartera({k: mensual[k] for k in ETFS}, rf, senal, id_replica=ID, variante=nombre,
                             comision_por_lado=com, spread_por_lado=spr, min_historia=MIN_HISTORIA,
                             peso_min=lo, peso_max=hi, bruto_max=bruto, cortes=[CORTE], extras=extras_b, fx=fx,
                             parametros={**params, "parte": "b", "escenario_costos": escenario},
                             fuente_datos=fuente_b, es_prueba=es_prueba, nota="; ".join(notas))
        resultados[(nombre, escenario, "MXN" if fx else "USD")] = r
        return r

    n8 = len(ETFS)
    tope_b = TOPE_APALANCAMIENTO / n8
    definiciones_a = []  # (nombre, fabrica, lo, hi, es_ref, params)
    for L in LOOKBACKS:
        definiciones_a.append((f"A_ls_vt40_L{L}", lambda L=L: senal_a_ls_vt(L, SIGMA_ARTICULO, TOPE_APALANCAMIENTO),
                               -TOPE_APALANCAMIENTO, TOPE_APALANCAMIENTO, False,
                               {"L": L, "tipo": "largo/corto", "sigma_obj": SIGMA_ARTICULO, "tope": TOPE_APALANCAMIENTO}))
    for L in LOOKBACKS:
        definiciones_a.append((f"A_lo_L{L}", lambda L=L: senal_a_lo(L), 0.0, 1.0, False,
                               {"L": L, "tipo": "solo largos"}))
    definiciones_a += [
        ("A_ref_comprar_mantener", lambda: bt.senal_comprar_y_mantener, 0.0, 1.0, True, {"tipo": "referencia"}),
        ("A_ref_efectivo", lambda: bt.senal_efectivo, 0.0, 1.0, True, {"tipo": "referencia"}),
        ("A_ref_sma10", lambda: bt.senal_media_movil(10), 0.0, 1.0, True, {"tipo": "referencia", "ventana": 10}),
        ("A_ref_largo_vt40", lambda: senal_a_largo_vt(SIGMA_ARTICULO, TOPE_APALANCAMIENTO), 0.0,
         TOPE_APALANCAMIENTO, True, {"tipo": "referencia", "sigma_obj": SIGMA_ARTICULO, "tope": TOPE_APALANCAMIENTO}),
    ]
    definiciones_b = []  # (nombre, fabrica, lo, hi, bruto, es_ref, params)
    for L in LOOKBACKS:
        definiciones_b.append((f"B_ls_vt40_L{L}", lambda L=L: senal_cartera("ls_vt", ETFS, L, SIGMA_ARTICULO, TOPE_APALANCAMIENTO),
                               -tope_b, tope_b, TOPE_APALANCAMIENTO, False,
                               {"L": L, "tipo": "largo/corto", "sigma_obj": SIGMA_ARTICULO, "tope_por_activo": TOPE_APALANCAMIENTO}))
    for L in LOOKBACKS:
        definiciones_b.append((f"B_lo_vt10_L{L}", lambda L=L: senal_cartera("lo_vt", ETFS, L, SIGMA_OPERABLE, 1.0),
                               0.0, 1.0 / n8, 1.0, False, {"L": L, "tipo": "solo largos", "sigma_obj": SIGMA_OPERABLE, "tope_por_activo": 1.0}))
    for L in LOOKBACKS:
        definiciones_b.append((f"B_lo_L{L}", lambda L=L: senal_cartera("lo", ETFS, L), 0.0, 1.0 / n8, 1.0, False,
                               {"L": L, "tipo": "solo largos binaria"}))
    definiciones_b += [
        ("B_ref_1N", lambda: senal_cartera("ref_1n", ETFS), 0.0, 1.0 / n8, 1.0, True, {"tipo": "referencia"}),
        ("B_ref_1N_sin_rebalanceo", lambda: senal_cartera("ref_1n_sin_rebalanceo", ETFS), 0.0, 1.0, 1.0, True,
         {"tipo": "referencia"}),
        ("B_ref_efectivo", lambda: senal_cartera("ref_1n", ()), 0.0, 1.0, 1.0, True, {"tipo": "referencia"}),
        ("B_ref_1N_sma10", lambda: senal_cartera("ref_sma10", ETFS), 0.0, 1.0 / n8, 1.0, True,
         {"tipo": "referencia", "ventana": 10}),
        ("B_ref_1N_vt10", lambda: senal_cartera("ref_vt", ETFS, objetivo=SIGMA_OPERABLE), 0.0, 1.0 / n8, 1.0, True,
         {"tipo": "referencia", "sigma_obj": SIGMA_OPERABLE, "tope_por_activo": 1.0}),
        ("B_ref_largo_vt40", lambda: senal_cartera("ref_largo_vt", ETFS, objetivo=SIGMA_ARTICULO, tope=TOPE_APALANCAMIENTO),
         0.0, tope_b, TOPE_APALANCAMIENTO, True,
         {"tipo": "referencia", "sigma_obj": SIGMA_ARTICULO, "tope_por_activo": TOPE_APALANCAMIENTO}),
    ]

    for escenario in ("defecto", "medio", "bruto"):
        for nombre, fab, lo, hi, es_ref, params in definiciones_a:
            correr_a(nombre, fab(), lo, hi, escenario, es_ref, params)
        for nombre, fab, lo, hi, bruto, es_ref, params in definiciones_b:
            correr_b(nombre, fab(), lo, hi, bruto, escenario, es_ref, params)

    fx = dh.fred("DEXMXUS")
    print(f"\n- FRED DEXMXUS: {fx[0][0]} a {fx[-1][0]} (n={len(fx)})")
    para_mxn = {"B_ls_vt40_L12", "B_lo_vt10_L12", "B_lo_L12", "B_ref_1N", "B_ref_1N_sma10", "B_ref_1N_vt10"}
    for nombre, fab, lo, hi, bruto, es_ref, params in definiciones_b:
        if nombre in para_mxn:
            correr_b(nombre, fab(), lo, hi, bruto, "defecto", es_ref, {**params, "moneda": "MXN"}, fx=fx,
                     nota_extra="sensibilidad: MXN con DEXMXUS (efectivo T-bill USD convertido)")

    # ------------------------------------------------ reporte
    def R(nombre, esc="defecto", mon="USD"):
        return resultados[(nombre, esc, mon)]

    nombres_a = [d[0] for d in definiciones_a]
    nombres_b = [d[0] for d in definiciones_b]
    for parte, nombres in (("a", nombres_a), ("b", nombres_b)):
        for esc in ("defecto", "medio", "bruto"):
            for seg in ("completo", "dentro_muestra", "fuera_muestra"):
                ejemplo = R(nombres[0], esc)
                f0, f1 = limites_segmento(ejemplo, seg)
                print(f"\n### Parte ({parte}) - costos {esc} - segmento {seg} ({f0} a {f1})\n")
                print(tabla([R(n, esc) for n in nombres], seg))

    print("\n### Parte (b) en MXN (DEXMXUS), costos por defecto\n")
    for seg in ("completo", "dentro_muestra", "fuera_muestra"):
        ejemplo = R("B_ref_1N", "defecto", "MXN")
        f0, f1 = limites_segmento(ejemplo, seg)
        print(f"\nSegmento {seg} ({f0} a {f1})\n")
        print(tabla([R(n, "defecto", "MXN") for n in nombres_b if n in para_mxn], seg))

    # ventanas pre-registradas
    ventanas_a = [("pre-articulo", date(1927, 6, 30), date(1984, 12, 31)),
                  ("articulo 1985-2009", date(1984, 12, 31), date(2009, 12, 31)),
                  ("post-publicacion", CORTE, date(2100, 1, 1))]
    decadas = [(f"{d}s", date(d - 1, 12, 31), date(d + 9, 12, 31)) for d in range(1920, 2030, 10)]
    clave_a = ["A_ls_vt40_L3", "A_ls_vt40_L6", "A_ls_vt40_L12", "A_lo_L3", "A_lo_L6", "A_lo_L12",
               "A_ref_comprar_mantener", "A_ref_sma10", "A_ref_largo_vt40"]
    print("\n### Parte (a): ventanas pre-registradas, costos por defecto\n")
    print(tabla_ventanas([R(n) for n in clave_a], ventanas_a))
    print("\n### Parte (a): ventana del articulo 1985-2009, BRUTO (H1b)\n")
    print(tabla_ventanas([R(n, "bruto") for n in clave_a], ventanas_a[1:2]))
    print("\n### Parte (a): por decadas, costos por defecto\n")
    print(tabla_ventanas([R(n) for n in ("A_ls_vt40_L12", "A_lo_L12", "A_ref_comprar_mantener")], decadas))
    ventanas_b = [("OOS 2012-2019", CORTE, date(2019, 12, 31)), ("OOS 2020-2026", date(2019, 12, 31), date(2100, 1, 1))]
    print("\n### Parte (b): mitades del tramo fuera de muestra, costos por defecto\n")
    print(tabla_ventanas([R(n) for n in nombres_b if n != "B_ref_efectivo"], ventanas_b))

    # diagnosticos
    print("\n### Diagnosticos\n")
    for n in ("A_ls_vt40_L3", "A_ls_vt40_L6", "A_ls_vt40_L12", "A_ref_largo_vt40"):
        r = R(n)
        en_tope = sum(1 for w in r.exposicion if abs(w) >= TOPE_APALANCAMIENTO - 1e-12)
        print(f"- {n}: meses en el tope |w|=10: {en_tope} de {len(r.exposicion)}; |w| medio="
              f"{statistics.fmean(abs(w) for w in r.exposicion):.3f}, max |w|={max(abs(w) for w in r.exposicion):.3f}; "
              f"peor mes neto={min(r.r_neto):.4f} ({r.fechas[r.r_neto.index(min(r.r_neto))]})")
    for n in nombres_b:
        r = R(n)
        if "vt40" in n:
            en_tope = sum(1 for p in r.meta["pesos"] for w in p.values() if abs(w) >= tope_b - 1e-12)
            print(f"- {n}: activo-meses en el tope 10/N: {en_tope}; exposicion bruta media="
                  f"{statistics.fmean(r.meta['exposicion_bruta']):.3f}, max={max(r.meta['exposicion_bruta']):.3f}")
        for seg in ("dentro_muestra", "fuera_muestra"):
            f0, f1 = limites_segmento(r, seg)
            i0, i1 = indices_segmento(r, f0, f1)
            print(f"- {n} [{seg}]: ordenes medias por mes={statistics.fmean(r.meta['ordenes'][i0:i1]):.2f}, "
                  f"meses con > 8 ordenes={sum(1 for o in r.meta['ordenes'][i0:i1] if o > 8)}")
    print("\nDescomposicion (bruta, anualizada x12): exposicion media x prima + covarianza de timing\n")
    for n in ("A_lo_L3", "A_lo_L6", "A_lo_L12", "A_ref_sma10", "B_lo_L3", "B_lo_L6", "B_lo_L12",
              "B_lo_vt10_L3", "B_lo_vt10_L6", "B_lo_vt10_L12", "B_ref_1N_sma10", "B_ref_1N_vt10", "B_ref_1N"):
        r = R(n)
        for seg in ("dentro_muestra", "fuera_muestra"):
            f0, f1 = limites_segmento(r, seg)
            i0, i1 = indices_segmento(r, f0, f1)
            d = descomposicion_timing(r, i0, i1)
            print(f"- {n} [{seg}]: exposicion x prima = {d['exposicion_x_prima_anual']:.4f}; "
                  f"timing = {d['timing_anual']:.4f}")

    # ------------------------------------------------ DSR
    print("\n### Sharpe deflactado (registro R02)\n")
    filas = bt.leer_registro(ID)
    pruebas = {}
    for f in filas:
        if f["es_prueba"] == 1:
            pruebas[(f["variante"], f["parametros_json"], f["segmento"])] = f
    n_prueba = len({(v, p) for v, p, _ in pruebas})
    print(f"- Variantes distintas con es_prueba=1: {n_prueba}; filas totales en el CSV: {len(filas)}")

    def dsr(**kw):
        try:
            d = bt.sharpe_deflactado_de_registro(ID, **kw)
        except ValueError as e:
            return f"error: {e}"
        return (f"variante={d['variante']} seg={d['segmento']} DSR={d['dsr']:.4f} cumple={d['cumple']} "
                f"N={d['n_pruebas']} V_periodo={d['varianza_sharpes_periodo']:.6f} SR_anual={d['sr_anual']:.4f} "
                f"SR0_anual={d['sr0_anual']:.4f} n_obs={d['n_obs']} asim={d['asimetria']:.3f} "
                f"curt={d['curtosis']:.3f} PSR={d['psr_sin_deflactar']:.4f}")

    print(f"- Por defecto (mejor de las {n_prueba}, dentro_muestra, V de todas): {dsr()}")
    for seg in ("dentro_muestra", "fuera_muestra"):
        for familia, prefijo in (("A", "A_"), ("B", "B_")):
            srs = [f["sharpe_periodo"] for (v, p, s), f in pruebas.items()
                   if s == seg and v.startswith(prefijo) and f["sharpe_periodo"] is not None]
            v_fam = statistics.variance(srs)
            mejor = max(((f["sharpe_periodo"], v) for (v, p, s), f in pruebas.items()
                         if s == seg and v.startswith(prefijo) and f["sharpe_periodo"] is not None),
                        default=(None, None))[1]
            print(f"- Familia {familia} [{seg}] mejor de la familia, V de la familia ({len(srs)} Sharpes), "
                  f"N={n_prueba}: {dsr(segmento=seg, variante=mejor, varianza_sharpes=v_fam, n_pruebas=n_prueba)}")
        for v in ("A_ls_vt40_L12", "A_lo_L12", "B_ls_vt40_L12", "B_lo_vt10_L12", "B_lo_L12"):
            print(f"- Pre-especificada {v} [{seg}], V de todas, N={n_prueba}: {dsr(segmento=seg, variante=v)}")


if __name__ == "__main__":
    main()
