"""Motor generico de backtest de senales con registro obligatorio de variantes (solo stdlib).

Modelo de tiempo. El periodo t es el intervalo (fecha_{t-1}, fecha_t]:
  1. Al cierre de t-1 la senal decide la exposicion w_t. Solo ve datos hasta t-1.
  2. Se rebalancea desde la exposicion que dejo la deriva, w_pre_t = w_{t-1}(1+ra_{t-1})/(1+rb_{t-1}),
     hasta w_t. Se paga costo_t = |w_t - w_pre_t| * (comision_por_lado + spread_por_lado).
  3. Durante t: r_bruto_t = w_t * r_activo_t + (1 - w_t) * r_efectivo_t.
     V_t = V_{t-1} * (1 - costo_t) * (1 + r_bruto_t), de modo que r_neto_t = V_t / V_{t-1} - 1.
  Con w > 1 la parte apalancada se financia a la tasa de efectivo. Con w < 0 (corto) se cobra
  efectivo sobre todo el valor. No se cobra margen, prestamo de titulos ni liquidacion final.
  Son supuestos declarados: si una replica los necesita, se agregan en ella.

Garantia anti look-ahead:
  a) Estructural. La senal recibe un objeto Historia con vistas de solo lectura sobre listas
     que el motor va llenando. Cuando se decide w_t, esas listas contienen exactamente t
     observaciones (0..t-1): el dato t se agrega DESPUES de la decision. Pedir h.activo[t]
     lanza IndexError. Las series externas (extras, fx) se entregan con fecha <= fecha_{t-1}.
  b) Capturas. Si la senal captura, por closure, argumentos por defecto, atributos o globales,
     un contenedor con >= n elementos (una serie completa), se lanza ErrorLookAhead. Esta
     revision es heuristica: la garantia fuerte es (a). Las senales deben ser funciones puras
     de su argumento.
  c) Senales precalculadas sobre toda la muestra. Se aceptan solo con auditar_constructor,
     que comprueba invariancia de prefijo: constructor(datos[:T]) == constructor(datos)[:T].
     Una media movil centrada o un z-score con la media de toda la muestra fallan la prueba.

Registro de variantes: si id_replica no es None, cada corrida agrega una fila por segmento
a laboratorio/replicas/<id_replica>-variantes.csv. id_replica es obligatorio. Para correr sin
registrar hay que pasar id_replica=None de forma explicita. sharpe_deflactado_de_registro
calcula el DSR de Bailey y Lopez de Prado (2014) con N y V tomados del registro.

Costos por defecto (declarados, ver arena/investigacion/01-gbm-operativa-y-costos.md):
  comision_por_lado = 0.25% + IVA 16% = 0.29%. Es un hecho de la Guia de Servicios GBM V1025,
    §2.1 y §3 del documento, escalon hasta 1 MDP, Trading MX/SIC.
  spread_por_lado = 0.05%. Es la mitad de la estimacion [I] de 0.10% de ida y vuelta para ETFs
    liquidos (§3). NO esta verificado. Los escenarios 'medio' (0.15%) e 'iliquido' (0.30%)
    estan en SPREAD_POR_LADO.
"""
from __future__ import annotations

import array
import collections
import csv
import dis
import functools
import hashlib
import json
import math
import numbers
import random
import re
import statistics
import sys
import types
from bisect import bisect_right
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from herramientas import metricas as m
from herramientas.parametros import RAIZ_REPO, obtener

IVA = 0.16
COMISION_GBM_POR_LADO = round(0.0025 * (1 + IVA), 10)  # 0.0029
SPREAD_POR_LADO = {"liquido": 0.0005, "medio": 0.0015, "iliquido": 0.0030}  # [I] no verificado
SPREAD_POR_LADO_DEFECTO = SPREAD_POR_LADO["liquido"]
FUENTE_COSTOS = ("arena/investigacion/01-gbm-operativa-y-costos.md §2.1 y §3: comision 0.25%+IVA "
                 "(hecho, Guia GBM V1025); spread = mitad de la estimacion de ida y vuelta [I]")
DIR_REPLICAS = RAIZ_REPO / "laboratorio" / "replicas"
SEGMENTOS_POR_CORTES = {0: [], 1: ["dentro_muestra", "fuera_muestra"],
                        2: ["desarrollo", "validacion", "prueba"]}
SEGMENTOS_SELECCION = ("dentro_muestra", "desarrollo", "completo")
_ID_VALIDO = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")


class ErrorLookAhead(Exception):
    """La senal puede ver (o vio) datos posteriores al momento de la decision."""


# ================================================================ vista de solo lectura

class Vista(Sequence):
    """Vista de solo lectura de los primeros n elementos de una lista. Los indices >= n no existen."""

    __slots__ = ("_datos", "_n")

    def __init__(self, datos: list, n: int):
        self._datos = datos
        self._n = n

    def __len__(self) -> int:
        return self._n

    def __getitem__(self, i):
        if isinstance(i, slice):
            inicio, fin, paso = i.indices(self._n)
            return tuple(self._datos[inicio:fin:paso])
        if i < 0:
            i += self._n
        if not 0 <= i < self._n:
            raise IndexError(f"indice fuera de la historia visible (n={self._n}): look-ahead bloqueado")
        return self._datos[i]

    def __repr__(self) -> str:
        return f"Vista(n={self._n})"


@dataclass(frozen=True, slots=True)
class Historia:
    """Lo que ve la senal al decidir el periodo t. Todo termina en t-1.

    fechas, activo (rendimientos en su moneda), efectivo, indice (nivel acumulado del activo,
    1.0 * prod(1 + r)) -> Vistas de longitud t. extras -> {nombre: Vista de (fecha, valor)} con
    fecha de disponibilidad <= fechas[-1]. exposicion_actual = w_{t-1} (o la inicial).
    """
    fechas: Vista
    activo: Vista
    efectivo: Vista
    indice: Vista
    extras: Mapping
    exposicion_actual: float

    def __len__(self) -> int:
        return len(self.fechas)

    @property
    def fecha_decision(self):
        """Fecha del ultimo dato visible (cierre de t-1), o None si no hay historia."""
        return self.fechas[-1] if len(self.fechas) else None


# ================================================================ senales de referencia

def senal_comprar_y_mantener(h: Historia) -> float:
    return 1.0


def senal_efectivo(h: Historia) -> float:
    return 0.0


def senal_media_movil(ventana: int) -> Callable[[Historia], float]:
    """1 si el indice del activo cierra arriba de su media simple de 'ventana' periodos, si no 0.

    Requiere min_historia >= ventana. Ejemplo: regla de 10 meses de Faber (2007) con ventana=10.
    """
    if ventana < 1:
        raise ValueError("ventana >= 1")

    def senal(h: Historia) -> float:
        if len(h.indice) < ventana:
            raise ValueError(f"media movil {ventana}: historia de {len(h.indice)} (sube min_historia)")
        ultimos = h.indice[-ventana:]
        return 1.0 if ultimos[-1] > statistics.fmean(ultimos) else 0.0

    senal.__qualname__ = senal.__name__ = f"media_movil_{ventana}"
    return senal


def senal_momentum_absoluto(ventana: int) -> Callable[[Historia], float]:
    """1 si el rendimiento acumulado de 'ventana' periodos supera al del efectivo, si no 0."""
    if ventana < 1:
        raise ValueError("ventana >= 1")

    def senal(h: Historia) -> float:
        if len(h.activo) < ventana:
            raise ValueError(f"momentum {ventana}: historia de {len(h.activo)} (sube min_historia)")
        acum_a = math.prod(1 + r for r in h.activo[-ventana:])
        acum_e = math.prod(1 + r for r in h.efectivo[-ventana:])
        return 1.0 if acum_a > acum_e else 0.0

    senal.__qualname__ = senal.__name__ = f"momentum_absoluto_{ventana}"
    return senal


def con_rezago(serie: list[tuple], dias: int) -> list[tuple]:
    """Mueve fechas de observacion a fechas de disponibilidad (+dias) para usarlas como extras."""
    return [(f + timedelta(days=dias), v) for f, v in serie]


# ================================================================ auditorias anti look-ahead

_TIPOS_IGNORADOS = (str, bytes, bytearray, range, Vista, types.ModuleType, type,
                    types.FunctionType, types.BuiltinFunctionType, types.MethodType)
_CONTENEDORES = (list, tuple, dict, set, frozenset, collections.deque, array.array, Mapping)


def _revisar_objeto(obj, n: int, ruta: str, hallazgos: list, profundidad: int, vistos: set) -> None:
    if id(obj) in vistos or profundidad > 2 or obj is None or isinstance(obj, (numbers.Number, bool)):
        return
    vistos.add(id(obj))
    if isinstance(obj, _TIPOS_IGNORADOS):
        return
    if isinstance(obj, _CONTENEDORES) or (isinstance(obj, Sequence) and hasattr(obj, "__len__")):
        try:
            largo = len(obj)
        except TypeError:
            return
        if largo >= n:
            hallazgos.append(f"{ruta}: contenedor {type(obj).__name__} de {largo} elementos (>= {n} periodos)")
            return
        if largo <= 1000:
            elementos = obj.values() if isinstance(obj, Mapping) else obj
            for k, e in enumerate(elementos):
                _revisar_objeto(e, n, f"{ruta}[{k}]", hallazgos, profundidad + 1, vistos)
        return
    atributos = getattr(obj, "__dict__", None)
    if isinstance(atributos, dict):
        for nombre, valor in atributos.items():
            _revisar_objeto(valor, n, f"{ruta}.{nombre}", hallazgos, profundidad + 1, vistos)


def _globales_de_codigo(codigo: types.CodeType) -> set[str]:
    """Nombres leidos como globales (LOAD_GLOBAL/LOAD_NAME), incluidos lambdas y comprensiones
    internas. No incluye nombres de atributos (h.activo no cuenta como global 'activo')."""
    nombres = {i.argval for i in dis.get_instructions(codigo)
               if i.opname in ("LOAD_GLOBAL", "LOAD_NAME") and isinstance(i.argval, str)}
    for c in codigo.co_consts:
        if isinstance(c, types.CodeType):
            nombres |= _globales_de_codigo(c)
    return nombres


def buscar_capturas(senal: Callable, n: int) -> list[str]:
    """Contenedores con >= n elementos alcanzables desde la senal fuera de su argumento."""
    hallazgos: list[str] = []
    vistos: set = set()
    pendientes = [(senal, "senal")]
    revisadas: set = set()
    while pendientes:
        f, ruta = pendientes.pop()
        if id(f) in revisadas:
            continue
        revisadas.add(id(f))
        if isinstance(f, functools.partial):
            for k, a in enumerate(f.args):
                _revisar_objeto(a, n, f"{ruta}.args[{k}]", hallazgos, 0, vistos)
            for k, a in (f.keywords or {}).items():
                _revisar_objeto(a, n, f"{ruta}.keywords[{k}]", hallazgos, 0, vistos)
            pendientes.append((f.func, f"{ruta}.func"))
            continue
        if isinstance(f, types.MethodType):
            _revisar_objeto(f.__self__, n, f"{ruta}.__self__", hallazgos, 0, vistos)
            pendientes.append((f.__func__, f"{ruta}.__func__"))
            continue
        if isinstance(f, types.FunctionType):
            for celda, nombre in zip(f.__closure__ or (), f.__code__.co_freevars):
                try:
                    contenido = celda.cell_contents
                except ValueError:
                    continue
                if isinstance(contenido, types.FunctionType):
                    pendientes.append((contenido, f"{ruta}<closure {nombre}>"))
                else:
                    _revisar_objeto(contenido, n, f"{ruta}<closure {nombre}>", hallazgos, 0, vistos)
            for k, d in enumerate(f.__defaults__ or ()):
                _revisar_objeto(d, n, f"{ruta}<default {k}>", hallazgos, 0, vistos)
            for k, d in (f.__kwdefaults__ or {}).items():
                _revisar_objeto(d, n, f"{ruta}<kwdefault {k}>", hallazgos, 0, vistos)
            for nombre in sorted(_globales_de_codigo(f.__code__)):
                if nombre in f.__globals__:
                    g = f.__globals__[nombre]
                    if isinstance(g, types.FunctionType) and g.__module__ == f.__module__:
                        pendientes.append((g, f"{ruta}<global {nombre}>"))
                    else:
                        _revisar_objeto(g, n, f"{ruta}<global {nombre}>", hallazgos, 0, vistos)
            continue
        if callable(f) and not isinstance(f, _TIPOS_IGNORADOS):
            _revisar_objeto(f, n, f"{ruta}<objeto>", hallazgos, 0, vistos)
            llamada = getattr(type(f), "__call__", None)
            if isinstance(llamada, types.FunctionType):
                pendientes.append((llamada, f"{ruta}.__call__"))
    return hallazgos


def auditar_constructor(constructor: Callable[[list], list], datos: list, n_cortes: int = 12,
                        semilla: int = 0, tolerancia: float = 1e-12) -> dict:
    """Prueba de invariancia de prefijo para senales calculadas sobre toda la muestra.

    constructor(datos) -> lista de igual longitud; el elemento k es la decision tomada con
    la informacion disponible al cierre de k. Es causal si, para cada corte T,
    constructor(datos[:T]) == constructor(datos)[:T]. Devuelve {'causal', 'cortes', 'primer_fallo'}.
    """
    n = len(datos)
    if n < 4:
        raise ValueError("Se requieren al menos 4 observaciones para auditar")
    completo = list(constructor(list(datos)))
    if len(completo) != n:
        raise ValueError(f"El constructor devolvio {len(completo)} valores para {n} datos")
    rnd = random.Random(semilla)
    cortes = sorted({2, n // 2, n - 1} | {rnd.randint(2, n - 1) for _ in range(max(0, n_cortes - 3))})

    def iguales(a, b) -> bool:
        if a is None or b is None:
            return a is b
        if isinstance(a, numbers.Real) and isinstance(b, numbers.Real):
            if math.isnan(a) or math.isnan(b):
                return math.isnan(a) and math.isnan(b)
            return abs(a - b) <= tolerancia * max(1.0, abs(a), abs(b))
        return a == b

    for T in cortes:
        parcial = list(constructor(list(datos[:T])))
        if len(parcial) != T:
            return {"causal": False, "cortes": cortes,
                    "primer_fallo": {"corte": T, "motivo": f"longitud {len(parcial)} != {T}"}}
        for k in range(T):
            if not iguales(parcial[k], completo[k]):
                return {"causal": False, "cortes": cortes,
                        "primer_fallo": {"corte": T, "indice": k, "con_toda_la_muestra": completo[k],
                                         "solo_con_datos_hasta_el_corte": parcial[k]}}
    return {"causal": True, "cortes": cortes, "primer_fallo": None}


def senal_precalculada(valores: list[tuple], auditoria: dict) -> Callable[[Historia], float]:
    """Senal desde una serie [(fecha, w)] ya calculada. En t usa el valor de fecha_{t-1}.

    Exige una auditoria causal de auditar_constructor. Si no la hay, lanza ErrorLookAhead.
    """
    if not auditoria or auditoria.get("causal") is not True:
        raise ErrorLookAhead(f"Senal precalculada sin auditoria causal: {auditoria and auditoria.get('primer_fallo')}")
    fechas = [f for f, _ in valores]
    pesos = [w for _, w in valores]
    if any(b <= a for a, b in zip(fechas, fechas[1:])):
        raise ValueError("Fechas de la senal precalculada no crecientes")

    def senal(h: Historia) -> float:
        if h.fecha_decision is None:
            raise ValueError("Sin historia: sube min_historia")
        k = bisect_right(fechas, h.fecha_decision) - 1
        if k < 0:
            raise ValueError(f"Sin valor de senal en o antes de {h.fecha_decision}")
        return pesos[k]

    senal._auditada = True  # type: ignore[attr-defined]
    return senal


# ================================================================ alineacion y utilidades

def _como_fecha(x) -> date:
    if isinstance(x, datetime):
        return x.date()
    if isinstance(x, date):
        return x
    return date.fromisoformat(str(x))


def _validar_serie(serie, nombre: str) -> list[tuple[date, float]]:
    salida = [(_como_fecha(f), float(v)) for f, v in serie]
    if any(b[0] <= a[0] for a, b in zip(salida, salida[1:])):
        raise ValueError(f"{nombre}: fechas no estrictamente crecientes")
    if any(not math.isfinite(v) for _, v in salida):
        raise ValueError(f"{nombre}: valores no finitos")
    return salida


def inferir_periodos_por_anio(fechas: list[date]) -> int:
    """252 (diaria), 52, 12, 4 o 1 segun la mediana de dias entre observaciones."""
    brechas = sorted((b - a).days for a, b in zip(fechas, fechas[1:]))
    if not brechas:
        raise ValueError("No se puede inferir la frecuencia con menos de 2 fechas")
    mediana = brechas[len(brechas) // 2]
    for minimo, maximo, ppa in ((1, 4, 252), (5, 9, 52), (26, 33, 12), (85, 95, 4), (360, 370, 1)):
        if minimo <= mediana <= maximo:
            return ppa
    raise ValueError(f"Frecuencia no reconocida (mediana {mediana} dias): pasa periodos_por_anio")


def _valor_en_o_antes(fechas: list[date], valores: list[float], fecha: date):
    k = bisect_right(fechas, fecha) - 1
    return (fechas[k], valores[k]) if k >= 0 else None


def _huella(*partes) -> str:
    h = hashlib.sha1()
    for parte in partes:
        h.update(repr(parte).encode())
    return h.hexdigest()[:16]


# ================================================================ metricas

def metricas_de_periodos(fechas: list[date], fecha_inicial: date, r_neto: list[float],
                         r_efectivo: list[float], exposicion: list[float], rotacion: list[float],
                         costo: list[float], r_activo: list[float], periodos_por_anio: int,
                         n_cambios: int) -> dict:
    """Metricas de un tramo. Usa herramientas/metricas.py y agrega las que faltan.

    sharpe/sortino: sobre el exceso contra el efectivo del mismo periodo. sharpe_periodo,
    asimetria y curtosis (cruda) del exceso: insumos del PSR/DSR. calmar = cagr / |mdd|.
    """
    n = len(r_neto)
    salida: dict[str, Any] = {"n_periodos": n, "fecha_inicio": fecha_inicial,
                              "fecha_fin": fechas[-1] if fechas else None,
                              "periodos_por_anio": periodos_por_anio}
    claves = ("rendimiento_total", "cagr", "vol_anual", "sharpe", "sortino", "mdd", "calmar",
              "sharpe_periodo", "asimetria", "curtosis", "psr", "exposicion_media", "tiempo_invertido",
              "rotacion_anual", "costo_anual", "n_cambios_senal", "cagr_activo_sin_costos", "cagr_efectivo")
    salida.update({k: None for k in claves})
    if n < 3:
        return salida
    curva = [(fecha_inicial, 1.0)]
    for f, r in zip(fechas, r_neto):
        curva.append((f, curva[-1][1] * (1 + r)))
    anios = (fechas[-1] - fecha_inicial).days / 365.25
    exceso = [a - b for a, b in zip(r_neto, r_efectivo)]
    sd = statistics.stdev(exceso)
    sr_p = statistics.fmean(exceso) / sd if sd > 0 else None
    asim, curt = m.asimetria(exceso), m.curtosis(exceso)
    psr = None
    if sr_p is not None:
        try:
            psr = m.psr_desde_estadisticos(sr_p, n, asim, curt)
        except ValueError:
            psr = None
    mdd = m.max_drawdown(curva)["valor"]
    cagr = m.cagr(curva)
    salida.update({
        "rendimiento_total": curva[-1][1] - 1,
        "cagr": cagr,
        "vol_anual": m.volatilidad_anualizada(r_neto, periodos_por_anio),
        "sharpe": m.sharpe(r_neto, rf=list(r_efectivo), periodos_por_anio=periodos_por_anio),
        "sortino": m.sortino(r_neto, rf=list(r_efectivo), periodos_por_anio=periodos_por_anio),
        "mdd": mdd,
        "calmar": (math.inf if cagr > 0 else 0.0) if mdd == 0 else cagr / abs(mdd),
        "sharpe_periodo": sr_p,
        "asimetria": asim,
        "curtosis": curt,
        "psr": psr,
        "exposicion_media": statistics.fmean(exposicion),
        "tiempo_invertido": sum(1 for w in exposicion if w != 0) / n,
        "rotacion_anual": sum(rotacion) / anios if anios > 0 else None,
        "costo_anual": sum(costo) / anios if anios > 0 else None,
        "n_cambios_senal": n_cambios,
        "cagr_activo_sin_costos": (math.prod(1 + r for r in r_activo)) ** (1 / anios) - 1 if anios > 0 else None,
        "cagr_efectivo": (math.prod(1 + r for r in r_efectivo)) ** (1 / anios) - 1 if anios > 0 else None,
    })
    return salida


# ================================================================ resultado

@dataclass
class ResultadoBacktest:
    variante: str
    fechas: list
    exposicion: list
    rotacion: list
    costo: list
    r_activo: list
    r_efectivo: list
    r_bruto: list
    r_neto: list
    curva: list
    metricas: dict
    segmentos: list
    parametros: dict
    meta: dict = field(default_factory=dict)
    ruta_registro: Path | None = None

    def resumen(self, segmentos: list[str] | None = None) -> str:
        """Tabla de texto con las metricas principales por segmento."""
        filas = []
        for s in segmentos or (["completo"] + self.segmentos):
            x = self.metricas[s]
            filas.append(f"{s:<15} {str(x['fecha_inicio']):>10} a {str(x['fecha_fin']):>10} n={x['n_periodos']:<6} "
                         + " ".join(f"{k}={_fmt(x[k])}" for k in ("cagr", "vol_anual", "sharpe", "sortino",
                                                                   "mdd", "calmar", "exposicion_media",
                                                                   "rotacion_anual", "costo_anual")))
        return f"[{self.variante}]\n" + "\n".join(filas)


def _fmt(x) -> str:
    if x is None:
        return "NA"
    if isinstance(x, float):
        return "inf" if math.isinf(x) else f"{x:.4f}"
    return str(x)


# ================================================================ motor

def backtest_senal(activo, efectivo, senal: Callable[[Historia], float], *,
                   id_replica: str | None, variante: str,
                   comision_por_lado: float = COMISION_GBM_POR_LADO,
                   spread_por_lado: float = SPREAD_POR_LADO_DEFECTO,
                   min_historia: int = 1,
                   exposicion_min: float = 0.0, exposicion_max: float = 1.0,
                   exposicion_inicial: float = 0.0,
                   cortes=(), nombres_segmentos: list[str] | None = None,
                   fx=None, efectivo_en_mxn: bool = False, max_dias_fx: int = 10,
                   moneda: str | None = None,
                   periodos_por_anio: int | None = None,
                   extras: dict | None = None,
                   rebalanceo_con_deriva: bool = True,
                   permitir_capturas: bool = False,
                   parametros: dict | None = None,
                   fuente_datos: str = "",
                   es_prueba: bool = True, nota: str = "",
                   dir_replicas: Path | str | None = None) -> ResultadoBacktest:
    """Corre una senal sobre un activo contra efectivo y registra la variante.

    activo: [(fecha, rendimiento del periodo que termina en fecha)] en moneda del activo.
    efectivo: igual, o un numero (rendimiento constante por periodo, p. ej. 0.0).
        Se usa la interseccion de fechas; las descartadas se reportan en meta.
    senal(h: Historia) -> exposicion en [exposicion_min, exposicion_max].
    min_historia: periodos visibles antes de la primera decision (>= 1). El periodo
        min_historia-1 da la fecha inicial de la curva.
    cortes: fechas de separacion. 1 corte -> dentro_muestra / fuera_muestra (p. ej. la
        fecha de publicacion del articulo). 2 cortes -> desarrollo / validacion / prueba.
        Un periodo con fecha <= corte queda en el segmento anterior al corte.
    fx: [(fecha, MXN por USD)]. Convierte el activo (y el efectivo si no efectivo_en_mxn):
        1 + r_MXN = (1 + r_USD) * FX_t / FX_{t-1}, con el ultimo FX <= cada fecha y a lo mas
        max_dias_fx dias de antiguedad. La senal ve rendimientos en moneda original y extras['fx'].
    extras: {nombre: [(fecha_de_disponibilidad, valor)]}. La senal ve las entradas con
        fecha <= fecha_{t-1}. Para datos macro usa fechas de publicacion (ALFRED o con_rezago).
    id_replica: obligatorio. None = no registrar (solo pruebas); si no, se agrega a
        laboratorio/replicas/<id>-variantes.csv.
    """
    if id_replica is not None and not _ID_VALIDO.match(id_replica):
        raise ValueError(f"id_replica invalido: {id_replica!r}")
    if not variante:
        raise ValueError("variante es obligatoria (nombre de la regla y sus parametros)")
    if min_historia < 1:
        raise ValueError("min_historia >= 1: el primer periodo solo fija la fecha inicial de la curva")
    if comision_por_lado < 0 or spread_por_lado < 0:
        raise ValueError("Costos negativos")
    if not exposicion_min <= exposicion_inicial <= exposicion_max:
        raise ValueError("exposicion_inicial fuera de [exposicion_min, exposicion_max]")

    serie_activo = _validar_serie(activo, "activo")
    if isinstance(efectivo, numbers.Real):
        serie_efectivo = [(f, float(efectivo)) for f, _ in serie_activo]
    else:
        serie_efectivo = _validar_serie(efectivo, "efectivo")
    mapa_ef = dict(serie_efectivo)
    fechas = [f for f, _ in serie_activo if f in mapa_ef]
    descartadas_activo = len(serie_activo) - len(fechas)
    descartadas_efectivo = len(serie_efectivo) - len(fechas)
    mapa_ac = dict(serie_activo)
    ra_orig = [mapa_ac[f] for f in fechas]
    re_orig = [mapa_ef[f] for f in fechas]
    n = len(fechas)
    if n < min_historia + 3:
        raise ValueError(f"Muy pocos periodos alineados ({n}) para min_historia={min_historia}")
    ppa = periodos_por_anio or inferir_periodos_por_anio(fechas)

    # ---- conversion de moneda
    factor_fx: list[float | None] = [None] * n
    serie_fx = None
    if fx is not None:
        serie_fx = _validar_serie(fx, "fx")
        fx_f = [f for f, _ in serie_fx]
        fx_v = [v for _, v in serie_fx]
        if any(v <= 0 for v in fx_v):
            raise ValueError("fx con valores no positivos")
        previo = _valor_en_o_antes(fx_f, fx_v, fechas[0])
        for t in range(1, n):
            actual = _valor_en_o_antes(fx_f, fx_v, fechas[t])
            if previo is not None and actual is not None \
                    and (fechas[t] - actual[0]).days <= max_dias_fx \
                    and (fechas[t - 1] - previo[0]).days <= max_dias_fx:
                factor_fx[t] = actual[1] / previo[1]
            previo = actual
        disponibles = [t for t in range(n) if factor_fx[t] is not None]
        if not disponibles:
            raise ValueError("fx no cubre ningun periodo del activo")
        primero_fx = disponibles[0]
        huecos = [fechas[t] for t in range(max(primero_fx, min_historia), n) if factor_fx[t] is None]
        if huecos:
            raise ValueError(f"fx con huecos > {max_dias_fx} dias en {huecos[:5]}")
        inicio = max(min_historia, primero_fx)
        moneda_final = "MXN"
    else:
        inicio = min_historia
        moneda_final = moneda or "USD"
    if inicio >= n - 2:
        raise ValueError("No quedan periodos para evaluar")

    def convertir(r: float, t: int, es_efectivo: bool) -> float:
        if factor_fx[t] is None or (es_efectivo and efectivo_en_mxn):
            return r
        return (1 + r) * factor_fx[t] - 1

    # ---- extras (incluye fx si existe)
    extras = dict(extras or {})
    if serie_fx is not None:
        if "fx" in extras:
            raise ValueError("'fx' es un nombre reservado en extras")
        extras["fx"] = serie_fx
    extras_val = {k: _validar_serie(v, f"extras[{k}]") for k, v in extras.items()}

    # ---- revision de capturas
    if not permitir_capturas and not getattr(senal, "_auditada", False):
        capturas = buscar_capturas(senal, n)
        if capturas:
            raise ErrorLookAhead("La senal captura series completas fuera de su argumento (posible "
                                 "look-ahead). Pasalas como extras (se entregan truncadas por fecha) o "
                                 "usa senal_precalculada + auditar_constructor. Hallazgos: "
                                 + "; ".join(capturas[:5]))

    # ---- listas visibles (se llenan despues de cada decision)
    vis_fechas: list = []
    vis_activo: list = []
    vis_efectivo: list = []
    vis_indice: list = []
    vis_extras: dict[str, list] = {k: [] for k in extras_val}
    punteros = {k: 0 for k in extras_val}

    exposicion, rotacion, costo, r_a, r_e, r_b, r_n, fechas_eval = [], [], [], [], [], [], [], []
    w_prev = exposicion_inicial
    ra_prev = rb_prev = None
    for t in range(n):
        if t >= inicio:
            h = Historia(
                fechas=Vista(vis_fechas, t), activo=Vista(vis_activo, t),
                efectivo=Vista(vis_efectivo, t), indice=Vista(vis_indice, t),
                extras=types.MappingProxyType({k: Vista(v, len(v)) for k, v in vis_extras.items()}),
                exposicion_actual=w_prev)
            w = senal(h)
            if isinstance(w, bool):
                w = float(w)
            if not isinstance(w, numbers.Real) or not math.isfinite(w):
                raise ValueError(f"La senal devolvio {w!r} en {fechas[t]}")
            w = float(w)
            if not exposicion_min - 1e-12 <= w <= exposicion_max + 1e-12:
                raise ValueError(f"Exposicion {w} fuera de [{exposicion_min}, {exposicion_max}] en {fechas[t]}")
            ra = convertir(ra_orig[t], t, False)
            re_ = convertir(re_orig[t], t, True)
            if t == inicio or not rebalanceo_con_deriva or rb_prev is None or 1 + rb_prev == 0:
                w_pre = w_prev
            else:
                w_pre = w_prev * (1 + ra_prev) / (1 + rb_prev)
            giro = abs(w - w_pre)
            c = giro * (comision_por_lado + spread_por_lado)
            rb = w * ra + (1 - w) * re_
            rn = rb - c * (1 + rb)  # = (1 - c)(1 + rb) - 1, exacto cuando c = 0
            exposicion.append(w)
            rotacion.append(giro)
            costo.append(c)
            r_a.append(ra)
            r_e.append(re_)
            r_b.append(rb)
            r_n.append(rn)
            fechas_eval.append(fechas[t])
            w_prev, ra_prev, rb_prev = w, ra, rb
        # el dato t se vuelve visible SOLO despues de decidir w_t
        vis_fechas.append(fechas[t])
        vis_activo.append(ra_orig[t])
        vis_efectivo.append(re_orig[t])
        vis_indice.append((vis_indice[-1] if vis_indice else 1.0) * (1 + ra_orig[t]))
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

    # ---- segmentos
    cortes_f = sorted(_como_fecha(c) for c in cortes)
    nombres = nombres_segmentos or SEGMENTOS_POR_CORTES.get(len(cortes_f)) \
        or [f"segmento_{k + 1}" for k in range(len(cortes_f) + 1)]
    if cortes_f and len(nombres) != len(cortes_f) + 1:
        raise ValueError("nombres_segmentos debe tener len(cortes) + 1 nombres")
    if "completo" in nombres:
        raise ValueError("'completo' es un segmento reservado")

    def tramo(i0: int, i1: int) -> dict:
        f0 = fecha_inicial if i0 == 0 else fechas_eval[i0 - 1]
        exp = exposicion[i0:i1]
        cambios = sum(1 for k in range(i0, i1)
                      if exposicion[k] != (exposicion[k - 1] if k > 0 else exposicion_inicial))
        return metricas_de_periodos(fechas_eval[i0:i1], f0, r_n[i0:i1], r_e[i0:i1], exp,
                                    rotacion[i0:i1], costo[i0:i1], r_a[i0:i1], ppa, cambios)

    metricas_seg = {"completo": tramo(0, len(r_n))}
    limites = [0]
    for c in cortes_f:
        limites.append(bisect_right(fechas_eval, c))
    limites.append(len(r_n))
    for k, nombre in enumerate(nombres if cortes_f else []):
        metricas_seg[nombre] = tramo(limites[k], limites[k + 1])
    segmentos = list(nombres) if cortes_f else []

    config = {
        "variante": variante,
        "senal": getattr(senal, "__qualname__", repr(senal)),
        "comision_por_lado": comision_por_lado, "spread_por_lado": spread_por_lado,
        "min_historia": min_historia, "exposicion_min": exposicion_min,
        "exposicion_max": exposicion_max, "exposicion_inicial": exposicion_inicial,
        "cortes": [c.isoformat() for c in cortes_f], "segmentos": segmentos,
        "fx": fx is not None, "efectivo_en_mxn": efectivo_en_mxn, "max_dias_fx": max_dias_fx,
        "periodos_por_anio": ppa, "rebalanceo_con_deriva": rebalanceo_con_deriva,
        "permitir_capturas": permitir_capturas, "extras": sorted(extras_val),
        "usuario": parametros or {},
    }
    huella = _huella(fechas, ra_orig, re_orig, factor_fx)
    resultado = ResultadoBacktest(
        variante=variante, fechas=fechas_eval, exposicion=exposicion, rotacion=rotacion, costo=costo,
        r_activo=r_a, r_efectivo=r_e, r_bruto=r_b, r_neto=r_n, curva=curva, metricas=metricas_seg,
        segmentos=segmentos, parametros=config,
        meta={"descartadas_activo": descartadas_activo, "descartadas_efectivo": descartadas_efectivo,
              "indice_inicio": inicio, "huella_datos": huella, "moneda": moneda_final,
              "fuente_datos": fuente_datos, "fuente_costos": FUENTE_COSTOS,
              "n_alineados": n})
    if id_replica is not None:
        resultado.ruta_registro = registrar_variante(resultado, id_replica, es_prueba=es_prueba,
                                                     nota=nota, dir_replicas=dir_replicas)
    return resultado


# ================================================================ registro de variantes

COLUMNAS_REGISTRO = [
    "fecha_registro_utc", "id_replica", "corrida", "variante", "es_prueba", "segmento",
    "fecha_inicio", "fecha_fin", "n_periodos", "periodos_por_anio", "moneda",
    "rendimiento_total", "cagr", "vol_anual", "sharpe", "sortino", "mdd", "calmar",
    "sharpe_periodo", "asimetria", "curtosis", "psr",
    "exposicion_media", "tiempo_invertido", "rotacion_anual", "costo_anual", "n_cambios_senal",
    "cagr_activo_sin_costos", "cagr_efectivo",
    "comision_por_lado", "spread_por_lado", "cortes", "huella_datos", "fuente_datos",
    "parametros_json", "nota",
]
_NUMERICAS = {"n_periodos", "periodos_por_anio", "rendimiento_total", "cagr", "vol_anual", "sharpe",
              "sortino", "mdd", "calmar", "sharpe_periodo", "asimetria", "curtosis", "psr",
              "exposicion_media", "tiempo_invertido", "rotacion_anual", "costo_anual",
              "n_cambios_senal", "cagr_activo_sin_costos", "cagr_efectivo", "comision_por_lado",
              "spread_por_lado", "es_prueba"}


def ruta_registro(id_replica: str, dir_replicas: Path | str | None = None) -> Path:
    if not _ID_VALIDO.match(id_replica):
        raise ValueError(f"id_replica invalido: {id_replica!r}")
    return Path(dir_replicas or DIR_REPLICAS) / f"{id_replica}-variantes.csv"


def _celda(x) -> str:
    if x is None:
        return ""
    if isinstance(x, float):
        return repr(x)
    if isinstance(x, date):
        return x.isoformat()
    return str(x)


def registrar_variante(resultado: ResultadoBacktest, id_replica: str, es_prueba: bool = True,
                       nota: str = "", dir_replicas: Path | str | None = None) -> Path:
    """Agrega una fila por segmento (completo + cortes) al CSV de la replica."""
    ruta = ruta_registro(id_replica, dir_replicas)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    existe = ruta.exists() and ruta.stat().st_size > 0
    if existe:
        with open(ruta, newline="", encoding="utf-8") as f:
            encabezado = next(csv.reader(f), [])
        if encabezado != COLUMNAS_REGISTRO:
            raise ValueError(f"{ruta} tiene otro esquema de columnas; no se mezcla (migra o usa otro id)")
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    parametros_json = json.dumps(resultado.parametros, sort_keys=True, ensure_ascii=False, default=str)
    corrida = hashlib.sha1((ahora + parametros_json + resultado.meta["huella_datos"]).encode()).hexdigest()[:10]
    filas = []
    for segmento in ["completo"] + resultado.segmentos:
        x = resultado.metricas[segmento]
        fila = {
            "fecha_registro_utc": ahora, "id_replica": id_replica, "corrida": corrida,
            "variante": resultado.variante, "es_prueba": 1 if es_prueba else 0, "segmento": segmento,
            "moneda": resultado.meta["moneda"],
            "comision_por_lado": resultado.parametros["comision_por_lado"],
            "spread_por_lado": resultado.parametros["spread_por_lado"],
            "cortes": "|".join(resultado.parametros["cortes"]),
            "huella_datos": resultado.meta["huella_datos"],
            "fuente_datos": resultado.meta["fuente_datos"],
            "parametros_json": parametros_json, "nota": nota,
        }
        for k in COLUMNAS_REGISTRO:
            if k in x and k not in fila:
                fila[k] = x[k]
        filas.append([_celda(fila.get(k)) for k in COLUMNAS_REGISTRO])
    with open(ruta, "a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        if not existe:
            escritor.writerow(COLUMNAS_REGISTRO)
        escritor.writerows(filas)
    return ruta


def leer_registro(registro: str | Path, dir_replicas: Path | str | None = None) -> list[dict]:
    """Filas del registro (id de replica o ruta al CSV) con columnas numericas como float/None."""
    ruta = Path(registro) if str(registro).endswith(".csv") else ruta_registro(str(registro), dir_replicas)
    with open(ruta, newline="", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    for fila in filas:
        for k in _NUMERICAS:
            v = fila.get(k, "")
            fila[k] = float(v) if v not in ("", None) else None
    return filas


def sharpe_deflactado_de_registro(registro: str | Path, n_pruebas: int | None = None,
                                  varianza_sharpes: float | None = None, *,
                                  segmento: str | None = None, variante: str | None = None,
                                  varianza_anualizada: bool = False,
                                  dir_replicas: Path | str | None = None) -> dict:
    """DSR (Bailey y Lopez de Prado, 2014) de la variante elegida entre las registradas.

    n_pruebas: numero de variantes probadas. None = variantes distintas (variante +
        parametros) con es_prueba=1 en el segmento. Si se da un N menor que las registradas,
        se lanza ValueError: no se permite subcontar.
    varianza_sharpes: varianza entre variantes de su Sharpe POR PERIODO (o anualizado si
        varianza_anualizada=True). None = varianza muestral de los registrados (0 si hay 1).
    segmento: donde se hizo la seleccion. None = el primero que exista de
        dentro_muestra, desarrollo, completo.
    variante: la evaluada. None = la de mayor Sharpe en el segmento, que es la seleccionada.
    """
    filas = leer_registro(registro, dir_replicas)
    if segmento is None:
        presentes = {f["segmento"] for f in filas}
        segmento = next((s for s in SEGMENTOS_SELECCION if s in presentes), None)
        if segmento is None:
            raise ValueError("El registro no tiene segmentos de seleccion")
    candidatas = [f for f in filas if f["segmento"] == segmento and f["es_prueba"] == 1]
    unicas: dict = {}
    for f in candidatas:
        unicas[(f["variante"], f["parametros_json"])] = f  # la ultima corrida de cada variante
    pruebas = list(unicas.values())
    validas = [f for f in pruebas if f["sharpe_periodo"] is not None]
    if not validas:
        raise ValueError(f"Sin variantes con Sharpe calculable en el segmento {segmento!r}")
    if variante is None:
        elegida = max(validas, key=lambda f: f["sharpe_periodo"])
    else:
        coincidencias = [f for f in validas if f["variante"] == variante]
        if not coincidencias:
            raise ValueError(f"Variante {variante!r} no esta en el registro (segmento {segmento})")
        elegida = coincidencias[-1]
    ppa = int(elegida["periodos_por_anio"])
    n_registradas = len(pruebas)
    if n_pruebas is None:
        n_pruebas = n_registradas
    elif n_pruebas < n_registradas:
        raise ValueError(f"n_pruebas={n_pruebas} es menor que las {n_registradas} variantes registradas")
    if varianza_sharpes is None:
        srs = [f["sharpe_periodo"] for f in validas]
        v = statistics.variance(srs) if len(srs) >= 2 else 0.0
    else:
        v = varianza_sharpes / ppa if varianza_anualizada else varianza_sharpes
    sr = elegida["sharpe_periodo"]
    n_obs = int(elegida["n_periodos"])
    dsr = m.dsr_desde_estadisticos(sr, n_obs, n_pruebas, v, elegida["asimetria"], elegida["curtosis"])
    sr0 = m.sharpe_maximo_esperado(n_pruebas, v)
    umbral = obtener("validacion_estrategias.deflated_sharpe_min_probabilidad")
    return {
        "variante": elegida["variante"], "segmento": segmento, "dsr": dsr, "umbral": umbral,
        "cumple": dsr >= umbral, "n_pruebas": n_pruebas, "n_registradas": n_registradas,
        "varianza_sharpes_periodo": v, "sr_periodo": sr, "sr_anual": sr * math.sqrt(ppa),
        "sr0_periodo": sr0, "sr0_anual": sr0 * math.sqrt(ppa), "n_obs": n_obs,
        "asimetria": elegida["asimetria"], "curtosis": elegida["curtosis"],
        "psr_sin_deflactar": m.psr_desde_estadisticos(sr, n_obs, elegida["asimetria"], elegida["curtosis"]),
    }


# ================================================================ comparacion

def comparar(resultados: list[ResultadoBacktest], segmento: str = "completo",
             claves=("cagr", "vol_anual", "sharpe", "sortino", "mdd", "calmar", "exposicion_media",
                     "rotacion_anual", "costo_anual")) -> str:
    """Tabla de texto para comparar variantes (incluida la regla sencilla) en un segmento."""
    anchos = [max(len(k) + 2, 10) for k in claves]
    lineas = [f"{'variante':<28}" + "".join(f"{k:>{a}}" for k, a in zip(claves, anchos))]
    for r in resultados:
        x = r.metricas[segmento]
        lineas.append(f"{r.variante[:28]:<28}" + "".join(f"{_fmt(x[k]):>{a}}" for k, a in zip(claves, anchos)))
    return "\n".join(lineas)
