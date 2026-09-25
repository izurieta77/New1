"""R06 - Replica de Gayed y Bilello (2016), "Leverage for the Long Run": ETFs apalancados 2x y 3x
con re-apalancamiento diario y filtro de tendencia de 200 dias sobre el mercado de EUA.

Reproduce (desde la raiz del repo):   python3 laboratorio/replicas/R06.py
Prueba del codigo con datos sinteticos (sin red, registro en un directorio temporal):
                                      python3 laboratorio/replicas/R06.py --prueba-sintetica

Articulo: Gayed, M. A. y C. Bilello (2016), Charles H. Dow Award 2016, SSRN 2741701.
PDF consultado: https://docs.cmtassociation.org/dow-award/2016-gayed-bilello.pdf (sha256 c181b05d...).

Datos (ficha R06-apalancados-y-filtro-de-tendencia.md, seccion 3):
  - French F-F_Research_Data_Factors_daily, CRSP 202607, congelado en R06-datos/ (SHA256SUMS.txt).
  - Yahoo (adjclose): SPY, QQQ, SSO, UPRO, QLD, TQQQ; ^GSPC y ^NDX de precio.
  - FRED: VIXCLS, DEXMXUS, INTGSTMXM193N. Yahoo y FRED no se congelan (se imprime su huella).
Motor: herramientas/backtest.py. Cada corrida se agrega a R06-variantes.csv (nunca se borra).
Salidas: R06-variantes.csv, R06-resultados.json y R06-salida.txt (copia de lo impreso).
Solo biblioteca estandar.
"""
from __future__ import annotations

import argparse
import array
import calendar
import hashlib
import io
import json
import math
import random
import statistics
import sys
import tempfile
import zipfile
from bisect import bisect_left, bisect_right
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(RAIZ))

from herramientas import backtest as bt  # noqa: E402
from herramientas import datos_historicos as dh  # noqa: E402
from herramientas import metricas as mt  # noqa: E402
from herramientas.estadistica import newey_west  # noqa: E402
from herramientas.huellas import verificar  # noqa: E402

ID = "R06"
FICHA = AQUI / "R06-apalancados-y-filtro-de-tendencia.md"
# sha256 de las secciones 1-9 (de "## PRE-REGISTRO" a "## RESULTADOS"), calculado el 2026-09-25 06:13 UTC
SHA_PRE_REGISTRO = "b12cbc772436d4c0f6b02f4f1284c636e663041d0c92080b69d8b6e2e4797699"
DIR_DATOS = AQUI / "R06-datos"
ZIP_FRENCH = DIR_DATOS / "202607" / "F-F_Research_Data_Factors_daily_CSV.zip"

CORTE = date(2015, 10, 31)            # fin de la muestra del articulo (octubre de 2015)
PUBLICACION = date(2016, 3, 3)        # SSRN
INICIO_ART = date(1928, 10, 1)
FIN_ART = date(2015, 10, 30)
FIN_DATOS = date(2026, 7, 31)         # ultimo dia con RF diario de French
INICIO_VIX = date(1990, 1, 3)
INICIO_NDX = date(1986, 8, 1)
INICIO_MXN = date(1993, 11, 10)
INICIO_SPY_QQQ = date(2006, 6, 22)    # ventana comun con SSO y QLD

GA = 0.009                            # gasto anual del ETF apalancado (supuesto de la tarea)
COMISION_ART = 0.01                   # comision de apalancamiento del articulo (p. 15)
FIN_EXTRA = 0.005                     # sensibilidad: financiamiento a RF + 0.50%
C_GBM = bt.COMISION_GBM_POR_LADO      # 0.0029 (hecho, Guia GBM V1025)
S_LIQ = bt.SPREAD_POR_LADO["liquido"]  # 0.0005 (supuesto [I])
COSTOS = {
    "defecto": (C_GBM, S_LIQ),
    "sin_costos_tx": (0.0, 0.0),
    "spread_medio": (C_GBM, bt.SPREAD_POR_LADO["medio"]),
    "doble_pierna": (2 * C_GBM, 2 * S_LIQ),
}
PPA = 252
NW_REZAGOS = 10

# Cifras del articulo (verificadas en el PDF el 2026-09-25; ficha, seccion 1)
ART = {
    "bh_L1": {"cagr": 0.091, "vol": 0.189, "sharpe": 0.30, "mdd": -0.862},
    "bh_L2": {"cagr": 0.137, "vol": 0.378, "sharpe": 0.27, "mdd": -0.988},
    "bh_L3": {"cagr": 0.153, "vol": 0.567, "sharpe": 0.21, "mdd": -0.999},
    "sma200_L1": {"cagr": 0.109, "vol": 0.124, "sharpe": 0.60, "mdd": -0.495, "oper": 5},
    "sma200_L2": {"cagr": 0.191, "vol": 0.249, "sharpe": 0.51, "mdd": -0.787, "oper": 5},
    "sma200_L3": {"cagr": 0.268, "vol": 0.373, "sharpe": 0.47, "mdd": -0.922, "oper": 5},
    "sma10_L1": {"cagr": 0.117, "vol": 0.121, "sharpe": 0.69, "mdd": -0.495, "oper": 38},
    "sma20_L1": {"cagr": 0.104, "vol": 0.117, "sharpe": 0.60, "mdd": -0.466, "oper": 26},
    "sma50_L1": {"cagr": 0.103, "vol": 0.117, "sharpe": 0.59, "mdd": -0.466, "oper": 15},
    "sma100_L1": {"cagr": 0.108, "vol": 0.122, "sharpe": 0.60, "mdd": -0.465, "oper": 10},
}
ART_TABLA1 = {1: 1969.0, 2: 169000.0, 3: 570965.0}  # crecimiento de 1 dolar, sin costo
ART_TABLA9 = [  # (pico, valle, S&P, 2x LRS, 3x LRS)
    (date(1929, 9, 16), date(1932, 6, 1), -0.862, -0.353, -0.498),
    (date(1973, 1, 11), date(1974, 10, 3), -0.448, -0.251, -0.367),
    (date(2000, 3, 24), date(2002, 10, 9), -0.474, -0.310, -0.458),
    (date(2007, 10, 9), date(2009, 3, 9), -0.552, -0.213, -0.311),
]
VENTANAS_DENTRO = [(date(1928, 10, 1), date(1929, 12, 31))] + \
    [(date(a, 1, 1), date(a + 9, 12, 31)) for a in range(1930, 2000, 10)] + \
    [(date(2000, 1, 1), date(2015, 10, 31))]
VENTANAS_FUERA = [(date(2015, 11, 1), date(2019, 12, 31)), (date(2020, 1, 1), date(2026, 7, 31))]
ETFS = {  # ticker -> (L, subyacente)
    "SSO": (2, "SPY"), "UPRO": (3, "SPY"), "QLD": (2, "QQQ"), "TQQQ": (3, "QQQ"),
}


# ============================================================== salida (pantalla + archivo)

class Salida:
    def __init__(self):
        self.lineas: list[str] = []

    def __call__(self, *partes):
        texto = " ".join(str(p) for p in partes)
        print(texto, flush=True)
        self.lineas.append(texto)


P = Salida()


def pct(x, d=2):
    return "NA" if x is None else f"{100 * x:.{d}f}%"


def num(x, d=3):
    if x is None:
        return "NA"
    if isinstance(x, float) and math.isinf(x):
        return "inf"
    return f"{x:.{d}f}"


# ============================================================== pre-registro y datos

def verificar_pre_registro() -> str:
    t = FICHA.read_text(encoding="utf-8")
    i, j = t.index("## PRE-REGISTRO"), t.index("## RESULTADOS")
    h = hashlib.sha256(t[i:j].encode("utf-8")).hexdigest()
    if h != SHA_PRE_REGISTRO:
        raise SystemExit(f"El pre-registro (secciones 1-9) cambio: sha256 {h} != {SHA_PRE_REGISTRO}. "
                         "Los cambios van en 'Desviaciones del pre-registro', no en las secciones 1-9.")
    return h


def huella_serie(serie) -> str:
    return hashlib.sha256(repr(list(serie)).encode()).hexdigest()[:16]


class Fuentes:
    """Datos reales: French congelado, Yahoo y FRED por herramientas/datos_historicos.py."""
    sintetico = False

    def french(self) -> dict:
        fallas = verificar(str(DIR_DATOS / "SHA256SUMS.txt"))
        if fallas:
            raise SystemExit(f"Huella de R06-datos no coincide: {fallas}")
        contenido = ZIP_FRENCH.read_bytes()
        with zipfile.ZipFile(io.BytesIO(contenido)) as z:
            nombres = [n for n in z.namelist() if n.lower().endswith(".csv")]
            texto = z.read(nombres[0]).decode("utf-8", errors="replace")
        t = dh.tabla_french(texto, "diaria")
        t["sha256"] = hashlib.sha256(contenido).hexdigest()
        t["archivo"] = str(ZIP_FRENCH.relative_to(RAIZ))
        return t

    def yahoo(self, ticker: str) -> dict:
        return dh.yahoo_historia(ticker, "1d")

    def fred(self, serie: str) -> list:
        return dh.fred(serie)


class FuentesSinteticas(Fuentes):
    """Datos aleatorios con la misma estructura (solo para probar el codigo)."""
    sintetico = True

    def __init__(self):
        self.rng = random.Random(20260925)
        self._dias = [d for d in (date(1926, 7, 1) + timedelta(k) for k in range((date(2026, 9, 24) - date(1926, 7, 1)).days + 1))
                      if d.weekday() < 5]
        self._cache: dict = {}

    def french(self) -> dict:
        fechas = [d for d in self._dias if d <= FIN_DATOS]
        mkt = [self.rng.gauss(0.0003, 0.011) for _ in fechas]
        rf = [0.0001 for _ in fechas]
        return {"fechas": fechas, "columnas": {"Mkt-RF": mkt, "SMB": mkt, "HML": mkt, "RF": rf},
                "version_crsp": "SINTETICO", "notas": ["sintetico"], "faltantes": 0,
                "sha256": "sintetico", "archivo": "sintetico", "tablas_en_archivo": []}

    def _precios(self, inicio: date, mu: float, sd: float, base=None):
        fechas = [d for d in self._dias if d >= inicio]
        p, precios = 100.0, []
        for k, _ in enumerate(fechas):
            r = base[k] if base is not None else self.rng.gauss(mu, sd)
            p *= 1 + r
            precios.append(p)
        return fechas, precios

    def yahoo(self, ticker: str) -> dict:
        if ticker in self._cache:
            return self._cache[ticker]
        inicios = {"SPY": date(1993, 1, 29), "QQQ": date(1999, 3, 10), "SSO": date(2006, 6, 21),
                   "UPRO": date(2009, 6, 25), "QLD": date(2006, 6, 21), "TQQQ": date(2010, 2, 11),
                   "^GSPC": date(1927, 12, 30), "^NDX": date(1985, 10, 1)}
        if ticker in ETFS:
            L, sub = ETFS[ticker]
            fs, ps = self.yahoo(sub)["fechas"], self.yahoo(sub)["precios"]
            k0 = bisect_left(fs, inicios[ticker])
            rs = [ps[k] / ps[k - 1] - 1 for k in range(k0, len(ps))]
            fechas, precios = self._precios(inicios[ticker], 0, 0,
                                            base=[L * r + self.rng.gauss(0, 0.0003) for r in rs])
        else:
            fechas, precios = self._precios(inicios[ticker], 0.0003, 0.012)
        h = {"fechas": fechas, "precios": precios, "cierres": precios, "usa_adjclose": True,
             "adjclose_difiere_de_close": False, "moneda": "USD", "descartes": [],
             "fechas_sin_precio": [], "url": "sintetico"}
        self._cache[ticker] = h
        return h

    def fred(self, serie: str) -> list:
        if serie == "VIXCLS":
            return [(d, max(9.0, 18 + 6 * math.sin(k / 300) + self.rng.gauss(0, 3)))
                    for k, d in enumerate(d for d in self._dias if d >= date(1990, 1, 2))]
        if serie == "DEXMXUS":
            v, salida = 3.15, []
            for d in (d for d in self._dias if d >= date(1993, 11, 8)):
                v *= 1 + self.rng.gauss(0.0001, 0.006)
                salida.append((d, v))
            return salida
        if serie == "INTGSTMXM193N":
            return [(date(a, m, 1), 10.0) for a in range(1986, 2027) for m in range(1, 13)
                    if date(1986, 10, 1) <= date(a, m, 1) <= date(2026, 7, 1)]
        raise KeyError(serie)


# ============================================================== series

def rendimientos_yahoo(h: dict, ticker: str, hasta: date = FIN_DATOS) -> list[tuple]:
    fechas, precios = h["fechas"], h["precios"]
    k = bisect_right(fechas, hasta)
    sin_precio = [f for f in h.get("fechas_sin_precio", []) if f <= hasta]
    if sin_precio:
        raise SystemExit(f"{ticker}: fechas sin precio dentro de la ventana {sin_precio[:5]}")
    return dh.rendimientos_de_precios(fechas[:k], precios[:k])


def niveles(fechas, precios, hasta: date = FIN_DATOS) -> list[tuple]:
    k = bisect_right(fechas, hasta)
    return list(zip(fechas[:k], precios[:k]))


def niveles_de_rendimientos(rends: list[tuple]) -> list[tuple]:
    nivel, salida = 1.0, []
    for f, r in rends:
        nivel *= 1 + r
        salida.append((f, nivel))
    return salida


def simular_letf(sub: list[tuple], rf: dict, L: int, *, gasto: float, financiar: bool,
                 fin_extra: float = 0.0) -> list[tuple]:
    """r_L = L*r_sub - (L-1)*(RF + fin_extra*dd/365.25) [si financiar] - gasto*dd/365.25.

    dd = dias naturales desde la fecha anterior del subyacente (1 en la primera). Solo fechas con RF.
    """
    salida, previa = [], None
    for f, r in sub:
        dd = (f - previa).days if previa is not None else 1
        previa = f
        if f not in rf:
            continue
        x = L * r - gasto * dd / 365.25
        if financiar and L != 1:
            x -= (L - 1) * (rf[f] + fin_extra * dd / 365.25)
        if x <= -1:
            raise SystemExit(f"ETF simulado {L}x liquidado el {f} (r = {x})")
        salida.append((f, x))
    return salida


def cetes_diario(tasas_mensuales: list[tuple], fechas: list[date]) -> list[tuple]:
    """r_d = tasa_mes/100 * dd/360 con la tasa del mismo mes (aproximacion declarada, ficha 5)."""
    mapa = {(f.year, f.month): v for f, v in tasas_mensuales}
    salida, previa = [], None
    for f in fechas:
        dd = (f - previa).days if previa is not None else 1
        previa = f
        if (f.year, f.month) not in mapa:
            continue
        salida.append((f, mapa[(f.year, f.month)] / 100 * dd / 360))
    return salida


# ============================================================== senal (funcion pura de Historia)

def senal_filtro(ventana: int = 200, rezago: int = 0, umbral_vix: float | None = None,
                 peso: float = 1.0, banda: float | None = None):
    """Exposicion 'peso' al ETF si el subyacente (extras['sub']) cierra arriba de su media de
    'ventana' dias (0 = sin media) y, si umbral_vix, el VIX (extras['vix']) esta debajo del umbral.
    rezago=1: usa el cierre de t-2 (ejecucion al cierre siguiente a la senal).
    banda: con el filtro activo, no rebalancea si el peso a la deriva esta en peso +- banda.
    """
    def senal(h):
        sub = h.extras["sub"]
        n = len(sub)
        fin = n - rezago
        if fin < max(ventana, 1):
            raise ValueError(f"historia del subyacente insuficiente ({n}) para ventana {ventana}")
        if (h.fecha_decision - sub[n - 1][0]).days > 7:
            raise ValueError(f"subyacente rezagado: {sub[n - 1][0]} vs {h.fecha_decision}")
        fecha_ref, nivel = sub[fin - 1]
        activo_ok = True
        if ventana:
            ult = sub[fin - ventana:fin]
            activo_ok = nivel > math.fsum(v for _, v in ult) / ventana
        if activo_ok and umbral_vix is not None:
            vix = h.extras["vix"]
            k = len(vix) - 1
            while k >= 0 and vix[k][0] > fecha_ref:
                k -= 1
            if k < 0 or (fecha_ref - vix[k][0]).days > 7:
                raise ValueError(f"VIX no disponible cerca de {fecha_ref}")
            activo_ok = vix[k][1] < umbral_vix
        if not activo_ok:
            return 0.0
        if banda is None:
            return peso
        w = h.exposicion_actual
        if w <= 0 or len(h.activo) == 0:
            return peso
        ra, re_ = h.activo[-1], h.efectivo[-1]
        rb = w * ra + (1 - w) * re_
        w_pre = w * (1 + ra) / (1 + rb) if 1 + rb != 0 else w
        if abs(w_pre - peso) <= banda:
            return min(max(w_pre, 0.0), 1.0)
        return peso

    senal.__qualname__ = senal.__name__ = (
        f"filtro_sma{ventana}_rez{rezago}_vix{umbral_vix}_peso{peso}_banda{banda}")
    return senal


# ============================================================== corridas

class Corrida:
    """Lo necesario de un ResultadoBacktest (arrays compactos para no agotar memoria)."""

    def __init__(self, r: bt.ResultadoBacktest):
        self.variante = r.variante
        self.metricas = r.metricas
        self.fechas = r.fechas
        self.r_neto = array.array("d", r.r_neto)
        self.r_efectivo = array.array("d", r.r_efectivo)
        self.r_activo = array.array("d", r.r_activo)
        self.exposicion = array.array("d", r.exposicion)
        self.rotacion = array.array("d", r.rotacion)
        self.costo = array.array("d", r.costo)
        self.fecha_inicial = r.curva[0][0]
        self.huella = r.meta["huella_datos"]
        self.descartes = (r.meta["descartadas_activo"], r.meta["descartadas_efectivo"])


class Laboratorio:
    def __init__(self, dir_replicas: Path):
        self.dir = dir_replicas
        self.res: dict[str, Corrida] = {}
        self.n_corridas = 0

    def correr(self, variante: str, activo, efectivo, senal, *, es_prueba: bool, min_historia: int,
               extras: dict, parametros: dict, fuente: str, nota: str, costos: str = "defecto",
               fx=None, efectivo_en_mxn: bool = False) -> Corrida:
        if variante in self.res:
            raise SystemExit(f"Variante repetida en el plan: {variante}")
        c, s = COSTOS[costos]
        r = bt.backtest_senal(activo, efectivo, senal, id_replica=ID, variante=variante,
                              comision_por_lado=c, spread_por_lado=s, min_historia=min_historia,
                              cortes=[CORTE], extras=extras, fx=fx, efectivo_en_mxn=efectivo_en_mxn,
                              periodos_por_anio=PPA, parametros=dict(parametros, costos=costos),
                              fuente_datos=fuente, es_prueba=es_prueba, nota=nota, dir_replicas=self.dir)
        self.n_corridas += 1
        k = Corrida(r)
        self.res[variante] = k
        return k


def ventana_metricas(k: Corrida, d0: date, d1: date) -> dict:
    """Metricas del motor sobre el tramo [d0, d1] de una corrida (sin registrar)."""
    i0 = bisect_left(k.fechas, d0)
    i1 = bisect_right(k.fechas, d1)
    if i1 - i0 < 3:
        return {}
    f0 = k.fechas[i0 - 1] if i0 > 0 else k.fecha_inicial
    exp = list(k.exposicion[i0:i1])
    previo = k.exposicion[i0 - 1] if i0 > 0 else 0.0
    cambios = sum(1 for j, w in enumerate(exp) if w != (exp[j - 1] if j > 0 else previo))
    x = bt.metricas_de_periodos(k.fechas[i0:i1], f0, list(k.r_neto[i0:i1]), list(k.r_efectivo[i0:i1]),
                                exp, list(k.rotacion[i0:i1]), list(k.costo[i0:i1]),
                                list(k.r_activo[i0:i1]), PPA, cambios)
    return x


def sharpe_art(x: dict):
    """Sharpe al estilo del articulo: (CAGR - CAGR del efectivo) / vol anual."""
    if not x or x.get("cagr") is None or not x.get("vol_anual"):
        return None
    return (x["cagr"] - x["cagr_efectivo"]) / x["vol_anual"]


def cambios_por_anio(x: dict):
    if not x or x.get("n_cambios_senal") is None:
        return None
    anios = (x["fecha_fin"] - x["fecha_inicio"]).days / 365.25
    return x["n_cambios_senal"] / anios if anios > 0 else None


def mdd_con_fechas(k: Corrida, d0: date, d1: date) -> dict:
    i0 = bisect_left(k.fechas, d0)
    i1 = bisect_right(k.fechas, d1)
    f0 = k.fechas[i0 - 1] if i0 > 0 else k.fecha_inicial
    v, curva = 1.0, [(f0, 1.0)]
    for j in range(i0, i1):
        v *= 1 + k.r_neto[j]
        curva.append((k.fechas[j], v))
    return mt.max_drawdown(curva)


ENCABEZADO = (f"{'variante':<40}{'inicio':>11}{'fin':>11}{'n':>7}{'CAGR':>9}{'vol':>8}{'Sharpe':>8}"
              f"{'Sh_art':>8}{'MDD':>9}{'invert':>8}{'camb/a':>8}{'costo/a':>9}")


def fila(nombre: str, x: dict) -> str:
    if not x:
        return f"{nombre[:40]:<40} (sin datos)"
    return (f"{nombre[:40]:<40}{str(x['fecha_inicio']):>11}{str(x['fecha_fin']):>11}{x['n_periodos']:>7}"
            f"{pct(x['cagr']):>9}{pct(x['vol_anual']):>8}{num(x['sharpe']):>8}{num(sharpe_art(x)):>8}"
            f"{pct(x['mdd']):>9}{pct(x['tiempo_invertido'], 1):>8}{num(cambios_por_anio(x), 2):>8}"
            f"{pct(x['costo_anual'], 3):>9}")


def tabla(lab: Laboratorio, titulo: str, variantes: list[str], segmentos=("completo", "dentro_muestra", "fuera_muestra")):
    for s in segmentos:
        P(f"\n--- {titulo} [{s}] ---")
        P(ENCABEZADO)
        for v in variantes:
            if v in lab.res:
                P(fila(v, lab.res[v].metricas.get(s, {})))


# ============================================================== analisis sin registro

def ols(x: list[float], y: list[float]) -> dict:
    mx, my = statistics.fmean(x), statistics.fmean(y)
    sxx = sum((a - mx) ** 2 for a in x)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    b = sxy / sxx
    a = my - b * mx
    ss_tot = sum((v - my) ** 2 for v in y)
    ss_res = sum((v - a - b * u) ** 2 for u, v in zip(x, y))
    return {"a": a, "b": b, "r2": 1 - ss_res / ss_tot if ss_tot > 0 else None, "n": len(x)}


def estados_sma(niv: list[tuple], ventana: int = 200) -> dict:
    """Estado de la senal para el dia t (decidido al cierre de t-1): 1 si S_{t-1} > SMA_{t-1}."""
    estado, suma = {}, 0.0
    vals = [v for _, v in niv]
    for t in range(1, len(niv)):
        j = t - 1
        if j + 1 >= ventana:
            media = math.fsum(vals[j + 1 - ventana:j + 1]) / ventana
            estado[niv[t][0]] = 1 if vals[j] > media else 0
    return estado


def analisis_decaimiento(mercado: list[tuple], rf: dict, estado: dict) -> dict:
    """H1 y H2: brecha en logaritmos de L x (financiado a RF, sin gasto) contra L veces el indice."""
    salida = {}
    por_anio: dict = {}
    for f, m_ in mercado:
        r_f = rf[f]
        x = m_ - r_f
        a = por_anio.setdefault(f.year, {"rv": 0.0, "g2": 0.0, "g3": 0.0, "n": 0})
        a["rv"] += x * x
        for L in (2, 3):
            a[f"g{L}"] += math.log(1 + L * m_ - (L - 1) * r_f) - L * math.log(1 + m_) + (L - 1) * math.log(1 + r_f)
        a["n"] += 1
    anios = [y for y in sorted(por_anio) if 1927 <= y <= 2025]
    rv = [por_anio[y]["rv"] for y in anios]
    for L in (2, 3):
        g = [por_anio[y][f"g{L}"] for y in anios]
        reg = ols(rv, g)
        reg["pendiente_teorica"] = -L * (L - 1) / 2
        reg["pendiente_relativa"] = reg["b"] / reg["pendiente_teorica"]
        salida[f"regresion_L{L}"] = reg
    # decaimiento anualizado por tramo y por regimen (3x y 2x)
    tramos = {"dentro_muestra": (INICIO_ART, FIN_ART), "fuera_muestra": (date(2015, 11, 1), FIN_DATOS),
              "completo": (INICIO_ART, FIN_DATOS)}
    for nombre, (d0, d1) in tramos.items():
        filas = [(f, m_, rf[f]) for f, m_ in mercado if d0 <= f <= d1]
        anios_t = (filas[-1][0] - filas[0][0]).days / 365.25
        res = {"anios": anios_t}
        for L in (2, 3):
            brecha = math.fsum(math.log(1 + L * m_ - (L - 1) * r) - L * math.log(1 + m_) + (L - 1) * math.log(1 + r)
                               for _, m_, r in filas)
            rv_t = math.fsum((m_ - r) ** 2 for _, m_, r in filas)
            res[f"L{L}_brecha_log_anual"] = brecha / anios_t
            res[f"L{L}_teorica_anual"] = -L * (L - 1) / 2 * rv_t / anios_t
        # regimen
        for s in (1, 0):
            sel = [(m_, r) for f, m_, r in filas if estado.get(f) == s]
            if len(sel) < 30:
                continue
            ex = [m_ - r for m_, r in sel]
            res[f"reg{s}_dias"] = len(sel)
            res[f"reg{s}_frac"] = len(sel) / len(filas)
            res[f"reg{s}_vol_anual"] = statistics.stdev([m_ for m_, _ in sel]) * math.sqrt(PPA)
            res[f"reg{s}_exceso_medio_anual"] = statistics.fmean(ex) * PPA
            for L in (2, 3):
                b = math.fsum(math.log(1 + L * m_ - (L - 1) * r) - L * math.log(1 + m_) + (L - 1) * math.log(1 + r)
                              for m_, r in sel)
                res[f"reg{s}_L{L}_brecha_log_por_anio_en_regimen"] = b / (len(sel) / PPA)
        if res.get("reg1_vol_anual"):
            res["cociente_vol_abajo_arriba"] = res.get("reg0_vol_anual", float("nan")) / res["reg1_vol_anual"]
        salida[nombre] = res
    # por decada
    dec = {}
    for y in anios:
        d = f"{(y // 10) * 10}s"
        e = dec.setdefault(d, {"anios": 0, "rv": 0.0, "g2": 0.0, "g3": 0.0})
        e["anios"] += 1
        e["rv"] += por_anio[y]["rv"]
        e["g2"] += por_anio[y]["g2"]
        e["g3"] += por_anio[y]["g3"]
    salida["por_decada"] = {d: {"vol_anual": math.sqrt(e["rv"] / e["anios"]), "L2_brecha_anual": e["g2"] / e["anios"],
                                "L3_brecha_anual": e["g3"] / e["anios"], "anios": e["anios"]}
                            for d, e in dec.items()}
    salida["anios_regresion"] = (anios[0], anios[-1], len(anios))
    return salida


def validar_simulador(real: list[tuple], sim: list[tuple]) -> dict:
    mr, ms = dict(real), dict(sim)
    fechas = sorted(set(mr) & set(ms))
    a = [mr[f] for f in fechas]
    b = [ms[f] for f in fechas]
    d = [y - x for x, y in zip(a, b)]
    anios = (fechas[-1] - fechas[0]).days / 365.25

    def cagr(xs):
        return math.exp(math.fsum(math.log(1 + x) for x in xs) / anios) - 1

    def mdd(xs):
        v, pico, peor = 1.0, 1.0, 0.0
        for x in xs:
            v *= 1 + x
            pico = max(pico, v)
            peor = min(peor, v / pico - 1)
        return peor

    return {"inicio": fechas[0], "fin": fechas[-1], "n": len(fechas),
            "correlacion": statistics.correlation(a, b),
            "error_seguimiento_anual": statistics.stdev(d) * math.sqrt(PPA),
            "dif_media_anual_sim_menos_real": statistics.fmean(d) * PPA,
            "cagr_real": cagr(a), "cagr_sim": cagr(b), "dif_cagr_sim_menos_real": cagr(b) - cagr(a),
            "mdd_real": mdd(a), "mdd_sim": mdd(b)}


def brecha_realizada(etf: list[tuple], sub: list[tuple], rf: dict, L: int) -> dict:
    """Brecha anual en logaritmos del ETF real contra L*subyacente - (L-1)*RF, y la teorica."""
    me, ms = dict(etf), dict(sub)
    fechas = sorted(set(me) & set(ms) & set(rf))
    anios = (fechas[-1] - fechas[0]).days / 365.25
    g = math.fsum(math.log(1 + me[f]) - L * math.log(1 + ms[f]) + (L - 1) * math.log(1 + rf[f]) for f in fechas)
    rv = math.fsum((ms[f] - rf[f]) ** 2 for f in fechas)
    return {"brecha_log_anual": g / anios, "teorica_sin_gasto": -L * (L - 1) / 2 * rv / anios,
            "vol_sub_anual": math.sqrt(rv / anios), "inicio": fechas[0], "fin": fechas[-1]}


def sumar_meses(f: date, meses: int) -> date:
    m = f.month - 1 + meses
    a, m = f.year + m // 12, m % 12 + 1
    return date(a, m, min(f.day, calendar.monthrange(a, m)[1]))


def percentil(xs: list[float], q: float) -> float:
    s = sorted(xs)
    if not s:
        return float("nan")
    i = min(len(s) - 1, max(0, int(round(q * (len(s) - 1)))))
    return s[i]


def temporadas(k: Corrida, d0: date | None = None, d1: date | None = None, meses: int = 6) -> dict:
    """Temporadas de 'meses' meses que empiezan el primer dia habil de cada mes dentro de [d0, d1]."""
    fechas, r = k.fechas, k.r_neto
    d0 = d0 or fechas[0]
    d1 = d1 or fechas[-1]
    inicios, visto = [], set()
    for i, f in enumerate(fechas):
        if f < d0 or f > d1:
            continue
        if (f.year, f.month) not in visto:
            visto.add((f.year, f.month))
            if i > 0 and fechas[i - 1].month == f.month:
                continue  # el mes empezo antes de d0: no es un inicio completo
            inicios.append(i)
    rets, mdds = [], []
    for i in inicios:
        fin = sumar_meses(fechas[i].replace(day=1), meses)
        if fin > d1 + timedelta(days=1) or fin > fechas[-1] + timedelta(days=1):
            break
        j = bisect_left(fechas, fin)
        v, pico, peor = 1.0, 1.0, 0.0
        for t in range(i, j):
            v *= 1 + r[t]
            pico = max(pico, v)
            peor = min(peor, v / pico - 1)
        rets.append(v - 1)
        mdds.append(peor)
    i0, i1 = bisect_left(fechas, d0), bisect_right(fechas, d1)
    dias = list(r[i0:i1])
    n = len(mdds)
    return {"n_temporadas": n, "mediana": percentil(rets, 0.5), "p5": percentil(rets, 0.05),
            "p95": percentil(rets, 0.95), "media": statistics.fmean(rets) if rets else None,
            "frac_ret_neg": sum(1 for x in rets if x < 0) / n if n else None,
            **{f"frac_dd_{abs(int(u * 100))}": (sum(1 for x in mdds if x <= u) / n if n else None)
               for u in (-0.12, -0.20, -0.28, -0.35)},
            "peor_dd": min(mdds) if mdds else None, "peor_ret": min(rets) if rets else None,
            "frac_dias_perdida_5": sum(1 for x in dias if x <= -0.05) / len(dias) if dias else None,
            "peor_dia": min(dias) if dias else None,
            "desde": fechas[i0] if dias else None, "hasta": fechas[i1 - 1] if dias else None}


def dif_newey_west(a: Corrida, b: Corrida, segmento: str) -> dict:
    ma, mb = dict(zip(a.fechas, a.r_neto)), dict(zip(b.fechas, b.r_neto))
    fechas = sorted(set(ma) & set(mb))
    if segmento == "dentro_muestra":
        fechas = [f for f in fechas if f <= CORTE]
    elif segmento == "fuera_muestra":
        fechas = [f for f in fechas if f > CORTE]
    x = [ma[f] - mb[f] for f in fechas]
    return newey_west(x, NW_REZAGOS)


# ============================================================== principal

def principal(sintetico: bool) -> None:
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sha_pre = verificar_pre_registro()
    fuentes = FuentesSinteticas() if sintetico else Fuentes()
    dir_reg = Path(tempfile.mkdtemp(prefix="R06_sintetico_")) if sintetico else AQUI
    lab = Laboratorio(dir_reg)
    P(f"R06 - corrida {ahora} - {'SINTETICA (no es resultado)' if sintetico else 'datos reales'}")
    P(f"Pre-registro verificado: sha256 {sha_pre}")
    P(f"Registro de variantes: {dir_reg / (ID + '-variantes.csv')}")

    # ---------------------------------------------------------------- datos
    fr = fuentes.french()
    if fr["faltantes"]:
        raise SystemExit(f"French con {fr['faltantes']} faltantes")
    mercado_todo = dh.rendimiento_mercado_french(fr) if not sintetico else \
        [(f, a + b) for f, a, b in zip(fr["fechas"], fr["columnas"]["Mkt-RF"], fr["columnas"]["RF"])]
    rf_serie = list(zip(fr["fechas"], fr["columnas"]["RF"]))
    rf = dict(rf_serie)
    huecos = [(a, b) for (a, _), (b, _) in zip(mercado_todo, mercado_todo[1:]) if (b - a).days > 4]
    P(f"\nFrench diario: CRSP {fr['version_crsp']}, sha256 {fr['sha256']}, {mercado_todo[0][0]} a "
      f"{mercado_todo[-1][0]}, n={len(mercado_todo)}, faltantes={fr['faltantes']}")
    P(f"  notas: {' | '.join(fr['notas'][:3])}")
    P(f"  huecos de mas de 4 dias naturales: {len(huecos)}; {[(str(a), str(b)) for a, b in huecos[:12]]}")
    mercado = [(f, r) for f, r in mercado_todo if f <= FIN_DATOS]
    niv_mercado = niveles_de_rendimientos(mercado)
    fechas_fr = [f for f, _ in mercado]
    fuente_fr = f"French daily CRSP {fr['version_crsp']} sha256 {fr['sha256'][:12]}"

    yh = {}
    for tk in ["SPY", "QQQ", "SSO", "UPRO", "QLD", "TQQQ", "^GSPC", "^NDX"]:
        h = fuentes.yahoo(tk)
        yh[tk] = h
        rs = rendimientos_yahoo(h, tk)
        L = ETFS.get(tk, (1, None))[0]
        umbral = 0.60 if L == 3 else (0.40 if L == 2 else 0.25)
        extremos = [(str(f), round(r, 4)) for f, r in rs if abs(r) > umbral]
        P(f"Yahoo {tk}: {h['fechas'][0]} a {h['fechas'][-1]} (usado hasta {rs[-1][0]}), n={len(rs)}, "
          f"adjclose={h['usa_adjclose']}, adj!=close={h['adjclose_difiere_de_close']}, "
          f"sin_precio(total)={len(h['fechas_sin_precio'])}, huella={huella_serie(rs)}, "
          f"|r|>{umbral:.0%}: {extremos[:5]}")
    vix = [(f, v) for f, v in fuentes.fred("VIXCLS") if f <= FIN_DATOS]
    fx = fuentes.fred("DEXMXUS")
    cetes_m = fuentes.fred("INTGSTMXM193N")
    P(f"FRED VIXCLS: {vix[0][0]} a {vix[-1][0]}, n={len(vix)}, huella={huella_serie(vix)}")
    P(f"FRED DEXMXUS: {fx[0][0]} a {fx[-1][0]}, n={len(fx)}, huella={huella_serie(fx)}")
    P(f"FRED INTGSTMXM193N: {cetes_m[0][0]} a {cetes_m[-1][0]}, n={len(cetes_m)}, huella={huella_serie(cetes_m)}")
    rf_art = [rf[f] for f in fechas_fr if INICIO_ART <= f <= FIN_ART]
    anios_art = (FIN_ART - date(1928, 9, 30)).days / 365.25
    cagr_rf_art = math.exp(math.fsum(math.log(1 + x) for x in rf_art) / anios_art) - 1
    P(f"CAGR de RF (T-bill de French) en 1928-10-01 a 2015-10-30: {pct(cagr_rf_art)} (el articulo no la cobra "
      f"sobre la parte apalancada; ficha 1)")

    def idx_desde(fechas: list[date], d: date) -> int:
        return bisect_left(fechas, d)

    # ---------------------------------------------------------------- series simuladas (French)
    sim = {}
    for L in (1, 2, 3):
        sim[("real", L)] = simular_letf(mercado, rf, L, gasto=GA if L > 1 else 0.0, financiar=True)
        sim[("art", L)] = simular_letf(mercado, rf, L, gasto=COMISION_ART if L > 1 else 0.0, financiar=False)
        sim[("art0", L)] = simular_letf(mercado, rf, L, gasto=0.0, financiar=False)
        sim[("fin50", L)] = simular_letf(mercado, rf, L, gasto=GA if L > 1 else 0.0, financiar=True,
                                         fin_extra=FIN_EXTRA)
    mh_art = idx_desde(fechas_fr, INICIO_ART)
    mh_vix = idx_desde(fechas_fr, INICIO_VIX)
    ex_fr = {"sub": niv_mercado}
    ex_fr_vix = {"sub": niv_mercado, "vix": vix}
    base_par = {"subyacente": "French Mkt-RF+RF", "gasto_anual": GA, "financiamiento": "(L-1)*RF"}
    art_par = {"subyacente": "French Mkt-RF+RF", "comision_articulo": COMISION_ART, "financiamiento": "ninguno"}

    # ---------------------------------------------------------------- bloque A (es_prueba=1)
    P("\n=== Corridas ===")
    for n_ in (50, 100, 150, 200, 250):
        for L in (1, 2, 3):
            lab.correr(f"sma{n_}_L{L}", sim[("real", L)], rf_serie, senal_filtro(n_), es_prueba=True,
                       min_historia=mh_art, extras=ex_fr, parametros=dict(base_par, L=L, ventana=n_, rezago=0),
                       fuente=fuente_fr, nota="A principal")
    P(f"bloque A listo ({lab.n_corridas} corridas)")
    # ---------------------------------------------------------------- bloque B
    for L in (1, 2, 3):
        lab.correr(f"bh_L{L}", sim[("real", L)], rf_serie, bt.senal_comprar_y_mantener, es_prueba=False,
                   min_historia=mh_art, extras=ex_fr, parametros=dict(base_par, L=L, regla="comprar_y_mantener"),
                   fuente=fuente_fr, nota="B referencia")
    lab.correr("efectivo", sim[("real", 1)], rf_serie, bt.senal_efectivo, es_prueba=False, min_historia=mh_art,
               extras=ex_fr, parametros=dict(base_par, L=1, regla="efectivo"), fuente=fuente_fr, nota="B referencia")
    # ---------------------------------------------------------------- bloque C (convencion del articulo)
    for L in (1, 2, 3):
        lab.correr(f"art_bh_L{L}", sim[("art", L)], rf_serie, bt.senal_comprar_y_mantener, es_prueba=False,
                   costos="sin_costos_tx", min_historia=mh_art, extras=ex_fr,
                   parametros=dict(art_par, L=L, regla="comprar_y_mantener"), fuente=fuente_fr,
                   nota="C convencion del articulo")
        lab.correr(f"art_sma200_L{L}", sim[("art", L)], rf_serie, senal_filtro(200), es_prueba=False,
                   costos="sin_costos_tx", min_historia=mh_art, extras=ex_fr,
                   parametros=dict(art_par, L=L, ventana=200, rezago=0), fuente=fuente_fr,
                   nota="C convencion del articulo")
    for L in (2, 3):
        lab.correr(f"art_bh_L{L}_sin_comision", sim[("art0", L)], rf_serie, bt.senal_comprar_y_mantener,
                   es_prueba=False, costos="sin_costos_tx", min_historia=mh_art, extras=ex_fr,
                   parametros=dict(art_par, L=L, comision_articulo=0.0, regla="comprar_y_mantener"),
                   fuente=fuente_fr, nota="C Tabla 1 (sin costo de apalancamiento)")
    for n_ in (10, 20, 50, 100):
        lab.correr(f"art_sma{n_}_L1", sim[("art", 1)], rf_serie, senal_filtro(n_), es_prueba=False,
                   costos="sin_costos_tx", min_historia=mh_art, extras=ex_fr,
                   parametros=dict(art_par, L=1, ventana=n_, rezago=0), fuente=fuente_fr, nota="C Tabla 6")
    P(f"bloques B y C listos ({lab.n_corridas} corridas)")
    # ---------------------------------------------------------------- bloque D (costos)
    for esc in ("sin_costos_tx", "spread_medio"):
        for L in (1, 2, 3):
            lab.correr(f"sma200_L{L}|{esc}", sim[("real", L)], rf_serie, senal_filtro(200), es_prueba=False,
                       costos=esc, min_historia=mh_art, extras=ex_fr,
                       parametros=dict(base_par, L=L, ventana=200, rezago=0), fuente=fuente_fr, nota=f"D {esc}")
    for L in (2, 3):
        par = dict(base_par, L=L, financiamiento="(L-1)*(RF+0.5%)")
        lab.correr(f"sma200_L{L}|fin_rf_mas_50pb", sim[("fin50", L)], rf_serie, senal_filtro(200), es_prueba=False,
                   min_historia=mh_art, extras=ex_fr, parametros=dict(par, ventana=200, rezago=0),
                   fuente=fuente_fr, nota="D financiamiento RF+0.50%")
        lab.correr(f"bh_L{L}|fin_rf_mas_50pb", sim[("fin50", L)], rf_serie, bt.senal_comprar_y_mantener,
                   es_prueba=False, min_historia=mh_art, extras=ex_fr,
                   parametros=dict(par, regla="comprar_y_mantener"), fuente=fuente_fr, nota="D financiamiento RF+0.50%")
    for L in (2, 3):
        lab.correr(f"sma200_L{L}|doble_pierna", sim[("real", L)], rf_serie, senal_filtro(200), es_prueba=False,
                   costos="doble_pierna", min_historia=mh_art, extras=ex_fr,
                   parametros=dict(base_par, L=L, ventana=200, rezago=0), fuente=fuente_fr, nota="D doble pierna")
    # ---------------------------------------------------------------- bloque E (rezago)
    for L in (1, 2, 3):
        lab.correr(f"sma200_L{L}|rezago1", sim[("real", L)], rf_serie, senal_filtro(200, rezago=1),
                   es_prueba=False, min_historia=mh_art, extras=ex_fr,
                   parametros=dict(base_par, L=L, ventana=200, rezago=1), fuente=fuente_fr, nota="E rezago 1 dia")
    P(f"bloques D y E listos ({lab.n_corridas} corridas)")
    # ---------------------------------------------------------------- bloque F (VIX, 1990-2026)
    for u in (20, 25, 30):
        for L in (2, 3):
            lab.correr(f"1990_sma200_vix{u}_L{L}", sim[("real", L)], rf_serie, senal_filtro(200, umbral_vix=u),
                       es_prueba=True, min_historia=mh_vix, extras=ex_fr_vix,
                       parametros=dict(base_par, L=L, ventana=200, rezago=0, umbral_vix=u), fuente=fuente_fr + "; FRED VIXCLS",
                       nota="F VIX")
    lab.correr("1990_vix25_solo_L3", sim[("real", 3)], rf_serie, senal_filtro(0, umbral_vix=25), es_prueba=True,
               min_historia=mh_vix, extras=ex_fr_vix, parametros=dict(base_par, L=3, ventana=0, umbral_vix=25),
               fuente=fuente_fr + "; FRED VIXCLS", nota="F VIX solo")
    for L in (1, 2, 3):
        lab.correr(f"1990_bh_L{L}", sim[("real", L)], rf_serie, bt.senal_comprar_y_mantener, es_prueba=False,
                   min_historia=mh_vix, extras=ex_fr, parametros=dict(base_par, L=L, regla="comprar_y_mantener", ventana_inicio="1990"),
                   fuente=fuente_fr, nota="F referencia misma ventana")
        lab.correr(f"1990_sma200_L{L}", sim[("real", L)], rf_serie, senal_filtro(200), es_prueba=False,
                   min_historia=mh_vix, extras=ex_fr, parametros=dict(base_par, L=L, ventana=200, rezago=0, ventana_inicio="1990"),
                   fuente=fuente_fr, nota="F referencia misma ventana")
    P(f"bloque F listo ({lab.n_corridas} corridas)")

    # ---------------------------------------------------------------- bloque G (ETFs reales)
    rets = {tk: rendimientos_yahoo(yh[tk], tk) for tk in yh}
    niv_y = {tk: niveles(yh[tk]["fechas"], yh[tk]["precios"]) for tk in yh}
    validacion = {}
    for tk, (L, sub_tk) in ETFS.items():
        real = rets[tk]
        f_real = {f for f, _ in real}
        sub_r = [(f, r) for f, r in rets[sub_tk] if f in f_real]
        sim_sub = simular_letf(sub_r, rf, L, gasto=GA, financiar=True)
        fuente_y = f"Yahoo {tk} adjclose huella {huella_serie(real)}; senal {sub_tk} adjclose; RF {fuente_fr}"
        ex_y = {"sub": niv_y[sub_tk]}
        par_y = {"etf": tk, "L": L, "subyacente_senal": sub_tk}
        lab.correr(f"real_{tk}_bh", real, rf_serie, bt.senal_comprar_y_mantener, es_prueba=False, min_historia=1,
                   extras=ex_y, parametros=dict(par_y, regla="comprar_y_mantener"), fuente=fuente_y, nota="G real")
        lab.correr(f"real_{tk}_sma200", real, rf_serie, senal_filtro(200), es_prueba=False, min_historia=1,
                   extras=ex_y, parametros=dict(par_y, ventana=200, rezago=0), fuente=fuente_y, nota="G real")
        lab.correr(f"real_{tk}_sma200|rezago1", real, rf_serie, senal_filtro(200, rezago=1), es_prueba=False,
                   min_historia=1, extras=ex_y, parametros=dict(par_y, ventana=200, rezago=1), fuente=fuente_y,
                   nota="G real rezago 1 dia")
        fuente_s = f"simulado {L}x de {sub_tk} adjclose - (L-1)RF - {GA:.2%}; RF {fuente_fr}"
        lab.correr(f"sim_{tk}_bh", sim_sub, rf_serie, bt.senal_comprar_y_mantener, es_prueba=False, min_historia=1,
                   extras=ex_y, parametros=dict(par_y, simulado=True, gasto_anual=GA, regla="comprar_y_mantener"),
                   fuente=fuente_s, nota="G simulado misma ventana")
        lab.correr(f"sim_{tk}_sma200", sim_sub, rf_serie, senal_filtro(200), es_prueba=False, min_historia=1,
                   extras=ex_y, parametros=dict(par_y, simulado=True, gasto_anual=GA, ventana=200, rezago=0),
                   fuente=fuente_s, nota="G simulado misma ventana")
        v = {"con_subyacente_real": validar_simulador(real, sim_sub)}
        if sub_tk == "SPY":
            v["con_mercado_french"] = validar_simulador(real, sim[("real", L)])
        else:
            ndx_r = [(f, r) for f, r in rets["^NDX"] if f in f_real]
            v["con_ndx_precio"] = validar_simulador(real, simular_letf(ndx_r, rf, L, gasto=GA, financiar=True))
        v["brecha_realizada"] = brecha_realizada(real, rets[sub_tk], rf, L)
        validacion[tk] = v
    for tk in ("SPY", "QQQ"):
        serie = [(f, r) for f, r in rets[tk] if f >= INICIO_SPY_QQQ]
        ex_y = {"sub": niv_y[tk]}
        fuente_y = f"Yahoo {tk} adjclose huella {huella_serie(serie)}; RF {fuente_fr}"
        lab.correr(f"real_{tk}_bh", serie, rf_serie, bt.senal_comprar_y_mantener, es_prueba=False, min_historia=1,
                   extras=ex_y, parametros={"etf": tk, "L": 1, "regla": "comprar_y_mantener"}, fuente=fuente_y,
                   nota="G subyacente")
        lab.correr(f"real_{tk}_sma200", serie, rf_serie, senal_filtro(200), es_prueba=False, min_historia=1,
                   extras=ex_y, parametros={"etf": tk, "L": 1, "ventana": 200, "rezago": 0}, fuente=fuente_y,
                   nota="G subyacente")
    for tk, idx in (("UPRO", "^GSPC"), ("TQQQ", "^NDX")):
        lab.correr(f"real_{tk}_sma200|senal_{idx.strip('^')}_precio", rets[tk], rf_serie, senal_filtro(200),
                   es_prueba=False, min_historia=1, extras={"sub": niv_y[idx]},
                   parametros={"etf": tk, "L": ETFS[tk][0], "subyacente_senal": idx, "ventana": 200, "rezago": 0},
                   fuente=f"Yahoo {tk} adjclose; senal {idx} precio; RF {fuente_fr}", nota="G senal sobre indice de precio")
    P(f"bloque G listo ({lab.n_corridas} corridas)")
    # ---------------------------------------------------------------- bloque H (Nasdaq-100 largo)
    ndx = rets["^NDX"]
    f_ndx = [f for f, _ in ndx if f in rf]
    mh_ndx = idx_desde(f_ndx, INICIO_NDX)
    for L in (1, 2, 3):
        s_ndx = simular_letf(ndx, rf, L, gasto=GA if L > 1 else 0.0, financiar=True)
        par = {"subyacente": "^NDX precio (sin dividendos)", "L": L, "gasto_anual": GA if L > 1 else 0.0,
               "financiamiento": "(L-1)*RF"}
        fuente_n = f"Yahoo ^NDX precio huella {huella_serie(ndx)}; RF {fuente_fr}"
        lab.correr(f"ndx_bh_L{L}", s_ndx, rf_serie, bt.senal_comprar_y_mantener, es_prueba=False, min_historia=mh_ndx,
                   extras={"sub": niv_y["^NDX"]}, parametros=dict(par, regla="comprar_y_mantener"), fuente=fuente_n,
                   nota="H Nasdaq-100 largo")
        lab.correr(f"ndx_sma200_L{L}", s_ndx, rf_serie, senal_filtro(200), es_prueba=False, min_historia=mh_ndx,
                   extras={"sub": niv_y["^NDX"]}, parametros=dict(par, ventana=200, rezago=0), fuente=fuente_n,
                   nota="H Nasdaq-100 largo")
    # ---------------------------------------------------------------- bloque I (MXN)
    cetes = cetes_diario(cetes_m, fechas_fr)
    f_cetes = {f for f, _ in cetes}
    mh_mxn = idx_desde([f for f in fechas_fr if f in f_cetes], INICIO_MXN)
    fuente_mx = f"{fuente_fr}; FRED DEXMXUS; FRED INTGSTMXM193N (Cetes, r=tasa*dd/360)"
    for v_, L, s_ in (("bh_L1", 1, bt.senal_comprar_y_mantener), ("bh_L3", 3, bt.senal_comprar_y_mantener),
                      ("sma200_L2", 2, senal_filtro(200)), ("sma200_L3", 3, senal_filtro(200))):
        lab.correr(f"mxn_cetes_{v_}", sim[("real", L)], cetes, s_, es_prueba=False, min_historia=mh_mxn,
                   extras=ex_fr, fx=fx, efectivo_en_mxn=True,
                   parametros=dict(base_par, L=L, moneda="MXN", efectivo="Cetes"), fuente=fuente_mx, nota="I MXN")
    mh_mxn_usd = idx_desde(fechas_fr, INICIO_MXN)
    lab.correr("mxn_rfusd_sma200_L3", sim[("real", 3)], rf_serie, senal_filtro(200), es_prueba=False,
               min_historia=mh_mxn_usd, extras=ex_fr, fx=fx, efectivo_en_mxn=False,
               parametros=dict(base_par, L=3, moneda="MXN", efectivo="RF USD convertido"), fuente=fuente_mx,
               nota="I MXN")
    P(f"bloques H e I listos ({lab.n_corridas} corridas)")
    # ---------------------------------------------------------------- bloque J (arena)
    for k_, nombre in ((0.25, "025"), (0.5, "050"), (1.0, "100")):
        lab.correr(f"arena_k{nombre}_sma200_vix25_L3", sim[("real", 3)], rf_serie,
                   senal_filtro(200, umbral_vix=25, peso=k_, banda=0.05), es_prueba=False, min_historia=mh_vix,
                   extras=ex_fr_vix, parametros=dict(base_par, L=3, ventana=200, umbral_vix=25, peso=k_, banda=0.05),
                   fuente=fuente_fr + "; FRED VIXCLS", nota="J arena")
    lab.correr("arena_k050_sma200_vix25_L3|rezago1", sim[("real", 3)], rf_serie,
               senal_filtro(200, rezago=1, umbral_vix=25, peso=0.5, banda=0.05), es_prueba=False,
               min_historia=mh_vix + 1,  # con rezago, la primera decision necesita el VIX del 1990-01-02
               extras=ex_fr_vix, parametros=dict(base_par, L=3, ventana=200, rezago=1, umbral_vix=25, peso=0.5, banda=0.05),
               fuente=fuente_fr + "; FRED VIXCLS", nota="J arena rezago 1 dia")
    lab.correr("arena_k050_sma200_L3", sim[("real", 3)], rf_serie, senal_filtro(200, peso=0.5, banda=0.05),
               es_prueba=False, min_historia=mh_art, extras=ex_fr,
               parametros=dict(base_par, L=3, ventana=200, peso=0.5, banda=0.05), fuente=fuente_fr, nota="J arena 1928-2026")
    lab.correr("arena_k050_bh_L3", sim[("real", 3)], rf_serie, senal_filtro(0, peso=0.5, banda=0.05),
               es_prueba=False, min_historia=mh_art, extras=ex_fr,
               parametros=dict(base_par, L=3, ventana=0, peso=0.5, banda=0.05), fuente=fuente_fr, nota="J arena sin filtro")
    for tk in ("UPRO", "TQQQ"):
        sub_tk = ETFS[tk][1]
        lab.correr(f"arena_k050_real_{tk}_sma200_vix25", rets[tk], rf_serie,
                   senal_filtro(200, umbral_vix=25, peso=0.5, banda=0.05), es_prueba=False, min_historia=1,
                   extras={"sub": niv_y[sub_tk], "vix": vix},
                   parametros={"etf": tk, "L": 3, "subyacente_senal": sub_tk, "ventana": 200, "umbral_vix": 25,
                               "peso": 0.5, "banda": 0.05},
                   fuente=f"Yahoo {tk} adjclose; senal {sub_tk}; FRED VIXCLS; RF {fuente_fr}", nota="J arena ETF real")
    P(f"bloque J listo: {lab.n_corridas} corridas registradas en total")

    # ================================================================ RESULTADOS
    R = lab.res
    salida_json: dict = {"corrida_utc": ahora, "sintetico": sintetico, "sha_pre_registro": sha_pre,
                         "french": {"version_crsp": fr["version_crsp"], "sha256": fr["sha256"]},
                         "n_corridas": lab.n_corridas, "cagr_rf_articulo": cagr_rf_art}

    tabla(lab, "Bloques A y B: implementacion realista (financiamiento (L-1)*RF + 0.9%/anio, costos GBM)",
          ["bh_L1", "bh_L2", "bh_L3", "efectivo"] + [f"sma{n_}_L{L}" for L in (1, 2, 3) for n_ in (50, 100, 150, 200, 250)])
    tabla(lab, "Bloque C: convencion del articulo (sin financiamiento, comision 1%, sin costos de transaccion)",
          ["art_bh_L1", "art_bh_L2", "art_bh_L3", "art_bh_L2_sin_comision", "art_bh_L3_sin_comision",
           "art_sma10_L1", "art_sma20_L1", "art_sma50_L1", "art_sma100_L1",
           "art_sma200_L1", "art_sma200_L2", "art_sma200_L3"], segmentos=("dentro_muestra",))
    P("\nCifras del articulo (oct-1928 a oct-2015): " + "; ".join(
        f"{k}: CAGR {pct(v['cagr'], 1)} vol {pct(v['vol'], 1)} Sh {v['sharpe']} MDD {pct(v['mdd'], 1)}"
        + (f" oper/a {v['oper']}" if 'oper' in v else "") for k, v in ART.items()))
    # Tabla 1
    P("\n--- Tabla 1 del articulo: crecimiento de 1 dolar, 1928-10-01 a 2015-10-30, sin costo de apalancamiento ---")
    t1 = {}
    for L, v_ in ((1, "art_bh_L1"), (2, "art_bh_L2_sin_comision"), (3, "art_bh_L3_sin_comision")):
        x = R[v_].metricas["dentro_muestra"]
        t1[L] = 1 + x["rendimiento_total"]
        P(f"  {L}x: replica ${t1[L]:,.0f} (multiplo contra 1x: {t1[L] / t1[1] if L > 1 else 1:,.1f}) | "
          f"articulo ${ART_TABLA1[L]:,.0f} (multiplo {ART_TABLA1[L] / ART_TABLA1[1]:,.1f})")
    salida_json["tabla1"] = t1

    tabla(lab, "Bloque D: costos", [f"sma200_L{L}|{e}" for e in ("sin_costos_tx", "spread_medio") for L in (1, 2, 3)]
          + ["sma200_L2|fin_rf_mas_50pb", "sma200_L3|fin_rf_mas_50pb", "bh_L2|fin_rf_mas_50pb",
             "bh_L3|fin_rf_mas_50pb", "sma200_L2|doble_pierna", "sma200_L3|doble_pierna"])
    tabla(lab, "Bloque E: ejecucion con rezago de 1 dia", [f"sma200_L{L}{s}" for L in (1, 2, 3) for s in ("", "|rezago1")])
    tabla(lab, "Bloque F: VIX (1990-01-03 a 2026-07-31)",
          ["1990_bh_L1", "1990_bh_L2", "1990_bh_L3", "1990_sma200_L1", "1990_sma200_L2", "1990_sma200_L3"]
          + [f"1990_sma200_vix{u}_L{L}" for L in (2, 3) for u in (20, 25, 30)] + ["1990_vix25_solo_L3"])
    tabla(lab, "Bloque G: ETFs reales, sus subyacentes y el simulador en la misma ventana",
          ["real_SPY_bh", "real_SPY_sma200", "real_QQQ_bh", "real_QQQ_sma200"]
          + [f"{p}_{tk}_{r}" for tk in ETFS for p, r in (("real", "bh"), ("sim", "bh"), ("real", "sma200"),
                                                          ("sim", "sma200"), ("real", "sma200|rezago1"))]
          + ["real_UPRO_sma200|senal_GSPC_precio", "real_TQQQ_sma200|senal_NDX_precio"])
    tabla(lab, "Bloque H: Nasdaq-100 largo (^NDX de precio, sin dividendos)",
          [f"ndx_{r}_L{L}" for L in (1, 2, 3) for r in ("bh", "sma200")])
    tabla(lab, "Bloque I: en MXN (DEXMXUS)", ["mxn_cetes_bh_L1", "mxn_cetes_bh_L3", "mxn_cetes_sma200_L2",
                                              "mxn_cetes_sma200_L3", "mxn_rfusd_sma200_L3"])
    tabla(lab, "Bloque J: cartera de la arena (peso k en 3x, bandas de 5 pp)",
          ["arena_k025_sma200_vix25_L3", "arena_k050_sma200_vix25_L3", "arena_k100_sma200_vix25_L3",
           "arena_k050_sma200_vix25_L3|rezago1", "arena_k050_sma200_L3", "arena_k050_bh_L3",
           "arena_k050_real_UPRO_sma200_vix25", "arena_k050_real_TQQQ_sma200_vix25"])

    # ---------------------------------------------------------------- tramo posterior a la publicacion
    P(f"\n--- Tramo posterior a la publicacion ({PUBLICACION + timedelta(days=1)} a {FIN_DATOS}), sin registro ---")
    P(ENCABEZADO)
    post = {}
    for v_ in ["bh_L1", "bh_L2", "bh_L3", "sma200_L1", "sma200_L2", "sma200_L3", "sma200_L2|rezago1",
               "sma200_L3|rezago1", "real_SPY_bh", "real_QQQ_bh", "real_SSO_bh", "real_SSO_sma200", "real_UPRO_bh",
               "real_UPRO_sma200", "real_UPRO_sma200|rezago1", "real_QLD_bh", "real_QLD_sma200", "real_TQQQ_bh",
               "real_TQQQ_sma200", "real_TQQQ_sma200|rezago1"]:
        x = ventana_metricas(R[v_], PUBLICACION + timedelta(days=1), FIN_DATOS)
        post[v_] = x
        P(fila(v_, x))

    # ---------------------------------------------------------------- mecanismo (H1, H2)
    estado = estados_sma(niv_mercado, 200)
    dec = analisis_decaimiento([(f, r) for f, r in mercado if f >= date(1927, 1, 1)], rf, estado)
    salida_json["decaimiento"] = dec
    P("\n--- H1: decaimiento por volatilidad (L x financiado a RF, sin gasto, contra L veces el indice) ---")
    P(f"años calendario usados: {dec['anios_regresion']}")
    for L in (2, 3):
        g = dec[f"regresion_L{L}"]
        P(f"  L={L}: brecha_log_anual = {g['a']:+.5f} + ({g['b']:.4f}) x varianza_realizada_anual; R2={g['r2']:.4f}; "
          f"pendiente teorica {g['pendiente_teorica']:.1f}; pendiente/teorica = {g['pendiente_relativa']:.4f}")
    for tramo in ("dentro_muestra", "fuera_muestra", "completo"):
        d = dec[tramo]
        P(f"  {tramo} ({d['anios']:.2f} años): brecha anual 2x {pct(d['L2_brecha_log_anual'])} (teorica "
          f"{pct(d['L2_teorica_anual'])}); 3x {pct(d['L3_brecha_log_anual'])} (teorica {pct(d['L3_teorica_anual'])})")
    P("  por decada (vol anual del mercado, brecha anual 2x y 3x en logaritmos):")
    for d_, e in dec["por_decada"].items():
        P(f"    {d_}: vol {pct(e['vol_anual'], 1)}  2x {pct(e['L2_brecha_anual'])}  3x {pct(e['L3_brecha_anual'])}  ({e['anios']} años)")
    P("\n--- H2: regimen segun la senal de 200 dias al cierre de t-1 (1 = arriba, 0 = abajo) ---")
    for tramo in ("dentro_muestra", "fuera_muestra", "completo"):
        d = dec[tramo]
        P(f"  {tramo}: arriba {pct(d.get('reg1_frac'), 1)} de los dias, vol {pct(d.get('reg1_vol_anual'))}, "
          f"exceso medio {pct(d.get('reg1_exceso_medio_anual'))}/año, brecha 3x {pct(d.get('reg1_L3_brecha_log_por_anio_en_regimen'))}/año | "
          f"abajo vol {pct(d.get('reg0_vol_anual'))}, exceso {pct(d.get('reg0_exceso_medio_anual'))}/año, "
          f"brecha 3x {pct(d.get('reg0_L3_brecha_log_por_anio_en_regimen'))}/año | cociente vol abajo/arriba "
          f"{num(d.get('cociente_vol_abajo_arriba'))}")

    # ---------------------------------------------------------------- simulador contra ETFs reales (H6)
    P("\n--- H6: validacion del simulador (sim = L x subyacente - (L-1) RF - 0.9%/año) contra el ETF real ---")
    for tk, v in validacion.items():
        for clave in ("con_subyacente_real", "con_mercado_french", "con_ndx_precio"):
            if clave not in v:
                continue
            x = v[clave]
            P(f"  {tk} {clave:<20} {x['inicio']} a {x['fin']} n={x['n']}: corr={x['correlacion']:.5f} "
              f"TE={pct(x['error_seguimiento_anual'])} dif media sim-real={pct(x['dif_media_anual_sim_menos_real'])}/año "
              f"CAGR real {pct(x['cagr_real'])} sim {pct(x['cagr_sim'])} (dif {x['dif_cagr_sim_menos_real'] * 100:+.2f} pp) "
              f"MDD real {pct(x['mdd_real'])} sim {pct(x['mdd_sim'])}")
        b = v["brecha_realizada"]
        P(f"  {tk} brecha realizada contra {ETFS[tk][0]} x subyacente - ({ETFS[tk][0]}-1) RF: "
          f"{pct(b['brecha_log_anual'])}/año; teorica por varianza (sin gasto) {pct(b['teorica_sin_gasto'])}/año; "
          f"vol del subyacente {pct(b['vol_sub_anual'])}")
    salida_json["validacion_simulador"] = validacion

    # ---------------------------------------------------------------- tablas 9 del articulo
    P("\n--- Tabla 9 del articulo: MDD dentro de cada mercado bajista (fechas del articulo) ---")
    t9 = []
    for pico, valle, a_sp, a2, a3 in ART_TABLA9:
        filas9 = {v_: mdd_con_fechas(R[v_], pico + timedelta(days=1), valle)["valor"]
                  for v_ in ("art_bh_L1", "art_sma200_L2", "art_sma200_L3", "sma200_L2", "sma200_L3",
                             "sma200_L2|rezago1", "sma200_L3|rezago1", "bh_L3")}
        t9.append({"pico": pico, "valle": valle, **filas9})
        P(f"  {pico} a {valle}: articulo S&P {pct(a_sp, 1)} 2x {pct(a2, 1)} 3x {pct(a3, 1)} | replica (conv. art.) "
          f"1x {pct(filas9['art_bh_L1'], 1)} 2x {pct(filas9['art_sma200_L2'], 1)} 3x {pct(filas9['art_sma200_L3'], 1)} | "
          f"realista 2x {pct(filas9['sma200_L2'], 1)} 3x {pct(filas9['sma200_L3'], 1)} | con rezago 2x "
          f"{pct(filas9['sma200_L2|rezago1'], 1)} 3x {pct(filas9['sma200_L3|rezago1'], 1)} | 3x sin filtro {pct(filas9['bh_L3'], 1)}")
    salida_json["tabla9"] = t9
    P("\n--- Fechas de los drawdowns maximos (dentro y fuera de muestra) ---")
    for v_ in ("bh_L1", "bh_L2", "bh_L3", "sma200_L1", "sma200_L2", "sma200_L3", "art_sma200_L2", "art_sma200_L3",
               "real_UPRO_bh", "real_UPRO_sma200", "real_TQQQ_bh", "real_TQQQ_sma200", "ndx_bh_L3", "ndx_sma200_L3"):
        k = R[v_]
        for s, (d0, d1) in (("dentro", (date(1900, 1, 1), CORTE)), ("fuera", (CORTE + timedelta(days=1), FIN_DATOS))):
            if bisect_right(k.fechas, d1) - bisect_left(k.fechas, d0) < 3:
                continue
            x = mdd_con_fechas(k, d0, d1)
            P(f"  {v_:<22} {s:<6} MDD {pct(x['valor'])} pico {x['fecha_pico']} valle {x['fecha_valle']} "
              f"recuperacion {x['fecha_recuperacion']}")

    # ---------------------------------------------------------------- subperiodos
    P("\n--- Subperiodos: realista, neto (CAGR y MDD) ---")
    P(f"{'ventana':<25}{'bh_L1':>9}{'sma200_L1':>11}{'bh_L2':>9}{'sma200_L2':>11}{'bh_L3':>9}{'sma200_L3':>11}"
      f"{'MDD bh_L1':>11}{'MDD s200L2':>12}{'MDD s200L3':>12}{'MDD bh_L3':>11}")
    sub_res, gana = [], 0
    for d0, d1 in VENTANAS_DENTRO + VENTANAS_FUERA:
        xs = {v_: ventana_metricas(R[v_], d0, d1) for v_ in ("bh_L1", "sma200_L1", "bh_L2", "sma200_L2", "bh_L3", "sma200_L3")}
        dentro = d1 <= CORTE
        if dentro and xs["sma200_L2"]["cagr"] > xs["bh_L1"]["cagr"]:
            gana += 1
        sub_res.append({"ventana": (d0, d1), **{v_: {"cagr": x["cagr"], "mdd": x["mdd"], "sharpe": x["sharpe"]} for v_, x in xs.items()}})
        P(f"{str(d0) + ' a ' + str(d1):<25}" + "".join(f"{pct(xs[v_]['cagr']):>{w}}" for v_, w in
                                                       (("bh_L1", 9), ("sma200_L1", 11), ("bh_L2", 9), ("sma200_L2", 11), ("bh_L3", 9), ("sma200_L3", 11)))
          + f"{pct(xs['bh_L1']['mdd']):>11}{pct(xs['sma200_L2']['mdd']):>12}{pct(xs['sma200_L3']['mdd']):>12}{pct(xs['bh_L3']['mdd']):>11}")
    P(f"Ventanas dentro de muestra con CAGR sma200_L2 > bh_L1: {gana} de {len(VENTANAS_DENTRO)}")
    salida_json["subperiodos"] = sub_res

    # ---------------------------------------------------------------- Newey-West
    P(f"\n--- Diferencia diaria de rendimientos netos, media y error estandar Newey-West ({NW_REZAGOS} rezagos) ---")
    nw = {}
    for a_, b_ in (("sma200_L2", "bh_L2"), ("sma200_L3", "bh_L3"), ("sma200_L2", "bh_L1"), ("sma200_L3", "bh_L1"),
                   ("sma200_L1", "bh_L1"), ("sma200_L3|rezago1", "bh_L3"), ("real_UPRO_sma200", "real_UPRO_bh"),
                   ("real_TQQQ_sma200", "real_TQQQ_bh")):
        for s in ("dentro_muestra", "fuera_muestra", "completo"):
            try:
                x = dif_newey_west(R[a_], R[b_], s)
            except ValueError:
                continue
            nw[f"{a_} - {b_} | {s}"] = x
            P(f"  {a_ + ' - ' + b_:<36} {s:<15} n={x['n']:<6} media={x['media'] * 100:+.4f}%/dia "
              f"(x252 {x['media'] * 25200:+.2f}%) t_NW={x['t']:+.2f} IC95=[{x['ic95'][0] * 100:+.4f}, {x['ic95'][1] * 100:+.4f}]%/dia")
    salida_json["newey_west"] = nw

    # ---------------------------------------------------------------- DSR
    P("\n--- Sharpe deflactado (Bailey y Lopez de Prado) ---")
    dsr = {}
    for etiqueta, kw in (("sma200_L2 dentro N=registradas", dict(segmento="dentro_muestra", variante="sma200_L2")),
                         ("sma200_L3 dentro N=registradas", dict(segmento="dentro_muestra", variante="sma200_L3")),
                         ("mejor dentro N=registradas", dict(segmento="dentro_muestra")),
                         ("sma200_L3 dentro N=50", dict(segmento="dentro_muestra", variante="sma200_L3", n_pruebas=50)),
                         ("sma200_L2 dentro N=50", dict(segmento="dentro_muestra", variante="sma200_L2", n_pruebas=50)),
                         ("sma200_L3 fuera N=registradas", dict(segmento="fuera_muestra", variante="sma200_L3")),
                         ("sma200_L2 fuera N=registradas", dict(segmento="fuera_muestra", variante="sma200_L2")),
                         ("mejor fuera N=registradas", dict(segmento="fuera_muestra"))):
        d = bt.sharpe_deflactado_de_registro(ID, dir_replicas=dir_reg, **kw)
        dsr[etiqueta] = d
        P(f"  {etiqueta:<32} variante={d['variante']:<24} DSR={d['dsr']:.4f} cumple(>={d['umbral']})={d['cumple']} "
          f"N={d['n_pruebas']} (registradas {d['n_registradas']}) V={d['varianza_sharpes_periodo']:.3e} "
          f"SR={d['sr_periodo']:.4f}/dia ({d['sr_anual']:.3f} anual) SR0={d['sr0_periodo']:.4f}/dia ({d['sr0_anual']:.3f} anual) "
          f"T={d['n_obs']} asim={d['asimetria']:.3f} curt={d['curtosis']:.2f} PSR={d['psr_sin_deflactar']:.4f}")
    salida_json["dsr"] = dsr

    # ---------------------------------------------------------------- temporadas (arena)
    P("\n--- Temporadas de 6 meses (inicio cada mes; ventanas traslapadas) ---")
    P(f"{'variante':<40}{'desde':>11}{'hasta':>11}{'n':>5}{'mediana':>9}{'p5':>9}{'p95':>9}{'%neg':>7}"
      f"{'DD<=12':>8}{'DD<=20':>8}{'DD<=28':>8}{'DD<=35':>8}{'peorDD':>9}{'dias<=-5%':>10}{'peor dia':>10}")
    temp = {}
    for v_, d0 in (("1990_bh_L1", None), ("1990_sma200_L3", None), ("1990_bh_L3", None),
                   ("arena_k025_sma200_vix25_L3", None), ("arena_k050_sma200_vix25_L3", None),
                   ("arena_k100_sma200_vix25_L3", None), ("arena_k050_sma200_vix25_L3|rezago1", None),
                   ("bh_L1", None), ("arena_k050_sma200_L3", None), ("arena_k050_bh_L3", None),
                   ("arena_k050_real_UPRO_sma200_vix25", None), ("arena_k050_real_TQQQ_sma200_vix25", None),
                   ("real_UPRO_bh", None), ("real_TQQQ_bh", None)):
        x = temporadas(R[v_], d0)
        temp[v_] = x
        P(f"{v_[:40]:<40}{str(x['desde']):>11}{str(x['hasta']):>11}{x['n_temporadas']:>5}{pct(x['mediana'], 1):>9}"
          f"{pct(x['p5'], 1):>9}{pct(x['p95'], 1):>9}{pct(x['frac_ret_neg'], 0):>7}{pct(x['frac_dd_12'], 1):>8}"
          f"{pct(x['frac_dd_20'], 1):>8}{pct(x['frac_dd_28'], 1):>8}{pct(x['frac_dd_35'], 1):>8}{pct(x['peor_dd'], 1):>9}"
          f"{pct(x['frac_dias_perdida_5'], 2):>10}{pct(x['peor_dia'], 1):>10}")
    salida_json["temporadas"] = temp

    # ================================================================ criterios pre-registrados
    P("\n================ CRITERIOS PRE-REGISTRADOS ================")
    dm = {v_: R[v_].metricas["dentro_muestra"] for v_ in R}
    fm = {v_: R[v_].metricas.get("fuera_muestra", {}) for v_ in R}
    c1 = abs(dm["art_bh_L1"]["cagr"] - 0.091) <= 0.010 and abs(dm["art_bh_L1"]["vol_anual"] - 0.189) <= 0.015
    c2 = (abs(dm["art_sma200_L2"]["cagr"] - 0.191) <= 0.03 and dm["art_sma200_L2"]["cagr"] > dm["art_bh_L1"]["cagr"]
          and dm["art_sma200_L2"]["cagr"] > dm["art_bh_L2"]["cagr"])
    c3 = abs(dm["art_sma200_L3"]["cagr"] - 0.268) <= 0.04 and dm["art_sma200_L3"]["cagr"] > dm["art_sma200_L2"]["cagr"]
    c4 = abs(dm["art_sma200_L2"]["mdd"] - (-0.787)) <= 0.10 and dm["art_sma200_L2"]["mdd"] > dm["art_bh_L2"]["mdd"]
    c5 = sharpe_art(dm["art_sma200_L2"]) > sharpe_art(dm["art_bh_L1"])
    pend_ok = all(abs(dec[f"regresion_L{L}"]["pendiente_relativa"] - 1) <= 0.20 and dec[f"regresion_L{L}"]["r2"] >= 0.80
                  for L in (2, 3))
    cociente = dec["dentro_muestra"].get("cociente_vol_abajo_arriba") or 0
    c6 = pend_ok and cociente >= 1.3
    P(f"C1 datos: CAGR 1x {pct(dm['art_bh_L1']['cagr'])} (9.1% +- 1 pp) y vol {pct(dm['art_bh_L1']['vol_anual'])} (18.9% +- 1.5 pp)? {c1}")
    P(f"C2 LRS 2x CAGR {pct(dm['art_sma200_L2']['cagr'])} en 19.1% +- 3 pp y > 1x ({pct(dm['art_bh_L1']['cagr'])}) y > 2x B&H "
      f"({pct(dm['art_bh_L2']['cagr'])})? {c2}")
    P(f"C3 LRS 3x CAGR {pct(dm['art_sma200_L3']['cagr'])} en 26.8% +- 4 pp y > LRS 2x? {c3}")
    P(f"C4 LRS 2x MDD {pct(dm['art_sma200_L2']['mdd'])} en -78.7% +- 10 pp y menos profundo que 2x B&H ({pct(dm['art_bh_L2']['mdd'])})? {c4}")
    P(f"C5 Sharpe (articulo) LRS 2x {num(sharpe_art(dm['art_sma200_L2']))} > 1x {num(sharpe_art(dm['art_bh_L1']))}? {c5}")
    P(f"C6 mecanismo: pendientes/teorica {num(dec['regresion_L2']['pendiente_relativa'])} y "
      f"{num(dec['regresion_L3']['pendiente_relativa'])} (+-20%), R2 {num(dec['regresion_L2']['r2'])} y "
      f"{num(dec['regresion_L3']['r2'])} (>= 0.80), cociente vol abajo/arriba {num(cociente)} (>= 1.3)? {c6}")
    ref_a = dm["sma200_L2"]["cagr"] <= dm["bh_L1"]["cagr"]
    ref_b = dm["sma200_L2"]["sharpe"] <= dm["bh_L1"]["sharpe"]
    P(f"Refutacion a) dentro_muestra realista neto: CAGR sma200_L2 {pct(dm['sma200_L2']['cagr'])} <= bh_L1 {pct(dm['bh_L1']['cagr'])}? {ref_a}")
    P(f"Refutacion b) dentro_muestra realista neto: Sharpe sma200_L2 {num(dm['sma200_L2']['sharpe'])} <= bh_L1 {num(dm['bh_L1']['sharpe'])}? {ref_b}")
    solo_algunos = gana < 5
    P(f"Subperiodos: CAGR sma200_L2 > bh_L1 en {gana} de 9 ventanas; 'solo en algunos subperiodos' (< 5)? {solo_algunos}")
    if ref_a or ref_b:
        estado_final = "No replicado"
    elif all((c1, c2, c3, c4, c5, c6)) and not solo_algunos:
        estado_final = "Replicado"
    else:
        estado_final = "Replicado con diferencias"
    P(f"ESTADO segun reglas pre-registradas: {estado_final}")

    def veredicto(m1, m2, m3, b1, b2, b3) -> str:
        se_sostiene = all(m["sharpe"] >= b1["sharpe"] and m["cagr"] > b1["cagr"] for m in (m2, m3))
        if se_sostiene:
            return "Se sostiene"
        if m2["mdd"] > b2["mdd"] and m3["mdd"] > b3["mdd"]:
            return "Solo proteccion"
        return "No se sostiene"

    ver_oos = veredicto(None, fm["sma200_L2"], fm["sma200_L3"], fm["bh_L1"], fm["bh_L2"], fm["bh_L3"])
    P(f"Fuera de muestra (2015-11 a 2026-07, realista, neto): sma200_L2 CAGR {pct(fm['sma200_L2']['cagr'])} Sh "
      f"{num(fm['sma200_L2']['sharpe'])} MDD {pct(fm['sma200_L2']['mdd'])}; sma200_L3 CAGR {pct(fm['sma200_L3']['cagr'])} "
      f"Sh {num(fm['sma200_L3']['sharpe'])} MDD {pct(fm['sma200_L3']['mdd'])}; bh_L1 CAGR {pct(fm['bh_L1']['cagr'])} Sh "
      f"{num(fm['bh_L1']['sharpe'])}; bh_L2 MDD {pct(fm['bh_L2']['mdd'])}; bh_L3 MDD {pct(fm['bh_L3']['mdd'])} -> {ver_oos}")
    ver_spy = veredicto(None, fm["real_SSO_sma200"], fm["real_UPRO_sma200"], fm["real_SPY_bh"], fm["real_SSO_bh"], fm["real_UPRO_bh"])
    ver_qqq = veredicto(None, fm["real_QLD_sma200"], fm["real_TQQQ_sma200"], fm["real_QQQ_bh"], fm["real_QLD_bh"], fm["real_TQQQ_bh"])
    P(f"Corroboracion con ETFs reales fuera de muestra: SSO/UPRO contra SPY -> {ver_spy}; QLD/TQQQ contra QQQ -> {ver_qqq}")

    # ---------------------------------------------------------------- conclusion operable (reglas pre-registradas)
    def reduce_mdd(v_filtro, v_bh):
        return fm[v_filtro]["mdd"] > fm[v_bh]["mdd"]

    red = {tk: {"cierre": reduce_mdd(f"real_{tk}_sma200", f"real_{tk}_bh"),
                "rezago1": reduce_mdd(f"real_{tk}_sma200|rezago1", f"real_{tk}_bh")} for tk in ("UPRO", "TQQQ")}
    P(f"Reduccion del MDD fuera de muestra en ETFs reales: {red}")
    if estado_final != "No replicado" and ver_oos in ("Se sostiene", "Solo proteccion") and \
            all(red[tk]["cierre"] and red[tk]["rezago1"] for tk in red):
        op_filtro = "Se confirma"
    elif ver_oos == "No se sostiene" or all(not red[tk]["cierre"] and not red[tk]["rezago1"] for tk in red):
        op_filtro = "Se descarta"
    else:
        op_filtro = "Se modifica"
    P(f"Regla 1 (filtro de 200 dias para apalancados): {op_filtro}")
    vix_ok = True
    for s in ("dentro_muestra", "fuera_muestra"):
        base = R["1990_sma200_L3"].metricas[s]
        v25 = R["1990_sma200_vix25_L3"].metricas[s]
        d_mdd = v25["mdd"] - base["mdd"]
        d_sh = v25["sharpe"] - base["sharpe"]
        signos = {u: R[f"1990_sma200_vix{u}_L3"].metricas[s]["mdd"] - base["mdd"] for u in (20, 30)}
        ok = d_mdd >= 0.05 and d_sh >= -0.05 and all(x > 0 for x in signos.values())
        vix_ok = vix_ok and ok
        P(f"  VIX {s}: MDD vix25 - MDD sma200 = {d_mdd * 100:+.2f} pp (>= +5), Sharpe {d_sh:+.3f} (>= -0.05), "
          f"dif MDD con umbral 20 {signos[20] * 100:+.2f} pp y 30 {signos[30] * 100:+.2f} pp (> 0) -> {ok}")
    op_vix = "Se mantiene" if vix_ok else "Se propone quitarlo o dejarlo opcional"
    P(f"Regla 2 (VIX < 25): {op_vix}")
    t50 = temp["arena_k050_sma200_vix25_L3"]
    t50r = temp["arena_k050_sma200_vix25_L3|rezago1"]
    t50l = temp["arena_k050_sma200_L3"]
    sensato = (all(t["frac_dd_20"] <= 0.10 and t["frac_dd_35"] <= 0.01 for t in (t50, t50r)) and t50l["frac_dd_35"] <= 0.02)
    alto = any(t["frac_dd_35"] > 0.02 or t["frac_dd_20"] > 0.20 for t in (t50, t50r, t50l))
    op_max = "Sensato" if sensato else ("Demasiado alto" if alto else "Aceptable con reservas")
    P(f"  k=0.5 SMA200+VIX25 1990-2026: DD<=-20% {pct(t50['frac_dd_20'], 1)}, DD<=-35% {pct(t50['frac_dd_35'], 1)}; "
      f"con rezago: {pct(t50r['frac_dd_20'], 1)}, {pct(t50r['frac_dd_35'], 1)}; SMA200 sola 1928-2026: DD<=-20% "
      f"{pct(t50l['frac_dd_20'], 1)}, DD<=-35% {pct(t50l['frac_dd_35'], 1)}")
    P(f"Regla 3 (etf_apalancado_max = 0.5): {op_max}")
    salida_json["criterios"] = {"C1": c1, "C2": c2, "C3": c3, "C4": c4, "C5": c5, "C6": c6, "refutacion_a": ref_a,
                                "refutacion_b": ref_b, "ventanas_gana": gana, "estado": estado_final,
                                "veredicto_fuera": ver_oos, "veredicto_spy": ver_spy, "veredicto_qqq": ver_qqq,
                                "reduccion_mdd_reales": red, "op_filtro": op_filtro, "op_vix": op_vix, "op_max": op_max}
    salida_json["metricas"] = {v_: R[v_].metricas for v_ in R}
    salida_json["tramo_post_publicacion"] = post

    sufijo = "-sintetico" if sintetico else ""
    destino_txt = (dir_reg if sintetico else AQUI) / f"{ID}-salida{sufijo}.txt"
    destino_json = (dir_reg if sintetico else AQUI) / f"{ID}-resultados{sufijo}.json"
    destino_json.write_text(json.dumps(salida_json, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    P(f"\nSalidas: {destino_json}")
    P(f"         {destino_txt}")
    destino_txt.write_text("\n".join(P.lineas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--prueba-sintetica", action="store_true",
                    help="corre todo con datos aleatorios y registro en un directorio temporal")
    args = ap.parse_args()
    principal(args.prueba_sintetica)
