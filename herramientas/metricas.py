"""Metricas de desempeno, estadistica de Sharpe, pronosticos y rachas (solo stdlib).

Convenciones:
- 'curva' / 'precios': lista de valores o de tuplas (fecha, valor).
- 'rends': rendimientos simples por periodo (0.01 = 1%).
- rf: tasa libre de riesgo ANUAL (0.07 = 7%) o lista de rf por periodo.
- Drawdowns negativos (-0.25 = -25%).
"""
from __future__ import annotations

import math
import statistics
from datetime import date
from statistics import NormalDist

N01 = NormalDist()
EULER_MASCHERONI = 0.5772156649015329
PERIODOS_POR_ANIO = 252


# ---------------------------------------------------------------- utilidades

def _separar(serie) -> tuple[list, list[float]]:
    """(fechas o indices, valores) a partir de lista de valores o de (fecha, valor)."""
    serie = list(serie)
    if serie and isinstance(serie[0], (tuple, list)):
        return [p[0] for p in serie], [float(p[1]) for p in serie]
    return list(range(len(serie))), [float(x) for x in serie]


def _valores(serie) -> list[float]:
    return _separar(serie)[1]


def _excesos(rends, rf, periodos_por_anio: int) -> list[float]:
    r = _valores(rends)
    if isinstance(rf, (list, tuple)):
        if len(rf) != len(r):
            raise ValueError("rf por periodo debe tener la misma longitud que rends")
        return [a - b for a, b in zip(r, rf)]
    rf_periodo = (1 + rf) ** (1 / periodos_por_anio) - 1
    return [x - rf_periodo for x in r]


def asimetria(x) -> float:
    """Asimetria muestral (momentos poblacionales, como en Bailey-Lopez de Prado)."""
    v = _valores(x)
    m = statistics.fmean(v)
    m2 = statistics.fmean([(a - m) ** 2 for a in v])
    m3 = statistics.fmean([(a - m) ** 3 for a in v])
    return m3 / m2 ** 1.5 if m2 > 0 else 0.0


def curtosis(x) -> float:
    """Curtosis cruda (Pearson; normal = 3, NO exceso)."""
    v = _valores(x)
    m = statistics.fmean(v)
    m2 = statistics.fmean([(a - m) ** 2 for a in v])
    m4 = statistics.fmean([(a - m) ** 4 for a in v])
    return m4 / m2 ** 2 if m2 > 0 else 3.0


# ---------------------------------------------------------------- rendimiento y riesgo

def rendimientos(precios, logaritmicos: bool = False) -> list[float]:
    """Rendimientos simples (o log) entre observaciones consecutivas."""
    v = _valores(precios)
    salida = []
    for a, b in zip(v, v[1:]):
        if a <= 0:
            raise ValueError("Precio no positivo en la serie")
        salida.append(math.log(b / a) if logaritmicos else b / a - 1)
    return salida


def rendimientos_con_fecha(serie) -> list[tuple]:
    """[(fecha_final, rendimiento)] desde [(fecha, precio)]."""
    fechas, v = _separar(serie)
    return [(fechas[i], v[i] / v[i - 1] - 1) for i in range(1, len(v))]


def cagr(curva, periodos_por_anio: int = PERIODOS_POR_ANIO, anios: float | None = None) -> float:
    """Tasa de crecimiento anual compuesta. Con fechas usa dias calendario / 365.25."""
    fechas, v = _separar(curva)
    if len(v) < 2 or v[0] <= 0:
        raise ValueError("Se requieren al menos 2 valores positivos")
    if anios is None:
        if isinstance(fechas[0], date):
            anios = (fechas[-1] - fechas[0]).days / 365.25
        else:
            anios = (len(v) - 1) / periodos_por_anio
    if anios <= 0:
        raise ValueError("Periodo de medicion nulo")
    return (v[-1] / v[0]) ** (1 / anios) - 1


def volatilidad_anualizada(rends, periodos_por_anio: int = PERIODOS_POR_ANIO) -> float:
    """Desviacion estandar muestral * sqrt(periodos por anio)."""
    return statistics.stdev(_valores(rends)) * math.sqrt(periodos_por_anio)


def sharpe(rends, rf=0.0, periodos_por_anio: int = PERIODOS_POR_ANIO) -> float:
    """Sharpe anualizado: media(exceso)/desv(exceso)*sqrt(ppa)."""
    ex = _excesos(rends, rf, periodos_por_anio)
    sd = statistics.stdev(ex)
    if sd == 0:
        return math.inf if statistics.fmean(ex) > 0 else 0.0
    return statistics.fmean(ex) / sd * math.sqrt(periodos_por_anio)


def sortino(rends, rf=0.0, periodos_por_anio: int = PERIODOS_POR_ANIO) -> float:
    """Sortino anualizado; desviacion a la baja = sqrt(media(min(0, exceso)^2)) sobre todas las obs."""
    ex = _excesos(rends, rf, periodos_por_anio)
    dd = math.sqrt(statistics.fmean([min(0.0, x) ** 2 for x in ex]))
    if dd == 0:
        return math.inf if statistics.fmean(ex) > 0 else 0.0
    return statistics.fmean(ex) / dd * math.sqrt(periodos_por_anio)


def serie_drawdown(curva) -> list[tuple]:
    """[(fecha o indice, drawdown desde el maximo previo)]."""
    fechas, v = _separar(curva)
    maximo = -math.inf
    salida = []
    for f, x in zip(fechas, v):
        maximo = max(maximo, x)
        salida.append((f, x / maximo - 1))
    return salida


def max_drawdown(curva) -> dict:
    """Maximo drawdown: valor, fecha_pico, fecha_valle, fecha_recuperacion (None si no recupera)."""
    fechas, v = _separar(curva)
    if not v:
        raise ValueError("Curva vacia")
    i_pico = 0
    peor, i_pico_mdd, i_valle = 0.0, 0, 0
    for i, x in enumerate(v):
        if x > v[i_pico]:
            i_pico = i
        dd = x / v[i_pico] - 1
        if dd < peor:
            peor, i_pico_mdd, i_valle = dd, i_pico, i
    i_rec = None
    if peor < 0:
        for j in range(i_valle + 1, len(v)):
            if v[j] >= v[i_pico_mdd]:
                i_rec = j
                break
    return {
        "valor": peor,
        "fecha_pico": fechas[i_pico_mdd] if peor < 0 else None,
        "fecha_valle": fechas[i_valle] if peor < 0 else None,
        "fecha_recuperacion": fechas[i_rec] if i_rec is not None else None,
        "periodos_pico_valle": (i_valle - i_pico_mdd) if peor < 0 else 0,
        "periodos_pico_recuperacion": (i_rec - i_pico_mdd) if i_rec is not None else None,
    }


def calmar(curva, periodos_por_anio: int = PERIODOS_POR_ANIO) -> float:
    """CAGR / |max drawdown|."""
    mdd = abs(max_drawdown(curva)["valor"])
    tasa = cagr(curva, periodos_por_anio)
    return math.inf if mdd == 0 else tasa / mdd


# ---------------------------------------------------------------- operaciones

def hit_rate(resultados) -> float:
    """Fraccion de operaciones con resultado > 0 (las de resultado 0 cuentan como no ganadoras)."""
    r = _valores(resultados)
    return sum(1 for x in r if x > 0) / len(r) if r else math.nan


def profit_factor(resultados) -> float:
    """Suma de ganancias / |suma de perdidas|; inf si no hay perdidas."""
    r = _valores(resultados)
    ganancias = sum(x for x in r if x > 0)
    perdidas = -sum(x for x in r if x < 0)
    if perdidas == 0:
        return math.inf if ganancias > 0 else math.nan
    return ganancias / perdidas


def expectancy(resultados) -> float:
    """Resultado esperado por operacion = p*ganancia_media - (1-p)*perdida_media = media."""
    r = _valores(resultados)
    return statistics.fmean(r) if r else math.nan


def racha_perdedora_observada(resultados) -> int:
    """Racha mas larga de resultados < 0 consecutivos."""
    maxima = actual = 0
    for x in _valores(resultados):
        actual = actual + 1 if x < 0 else 0
        maxima = max(maxima, actual)
    return maxima


# ---------------------------------------------------------------- Sharpe probabilistico y deflactado

def psr_desde_estadisticos(sr: float, n: int, asimetria_: float = 0.0, curtosis_: float = 3.0,
                           sr_referencia: float = 0.0) -> float:
    """PSR (Bailey y Lopez de Prado, 2012, J. of Risk 15(2)).

    PSR = Phi[(SR - SR*) sqrt(n-1) / sqrt(1 - g3*SR + (g4-1)/4*SR^2)]
    SR y SR* por periodo (NO anualizados); g4 = curtosis cruda (normal = 3).
    """
    if n < 2:
        raise ValueError("Se requieren al menos 2 observaciones")
    denominador = 1 - asimetria_ * sr + (curtosis_ - 1) / 4 * sr ** 2
    if denominador <= 0:
        raise ValueError("Denominador no positivo: momentos incompatibles con el SR")
    z = (sr - sr_referencia) * math.sqrt(n - 1) / math.sqrt(denominador)
    return N01.cdf(z)


def sharpe_probabilistico(rends, sr_referencia_anual: float = 0.0, rf=0.0,
                          periodos_por_anio: int = PERIODOS_POR_ANIO) -> float:
    """Probabilidad de que el Sharpe verdadero supere sr_referencia_anual, dados n, asimetria y curtosis."""
    ex = _excesos(rends, rf, periodos_por_anio)
    sr = statistics.fmean(ex) / statistics.stdev(ex)
    sr_ref = sr_referencia_anual / math.sqrt(periodos_por_anio)
    return psr_desde_estadisticos(sr, len(ex), asimetria(ex), curtosis(ex), sr_ref)


def sharpe_maximo_esperado(n_pruebas: int, varianza_sharpes: float) -> float:
    """SR0 = E[max SR] bajo H0 (Bailey y Lopez de Prado, 2014, JPM 40(5)).

    SR0 = sqrt(V) * ((1-g) Phi^-1(1 - 1/N) + g Phi^-1(1 - 1/(N e))), g = Euler-Mascheroni.
    V = varianza entre pruebas de los SR por periodo. Con N <= 1 no hay seleccion: SR0 = 0.
    """
    if n_pruebas <= 1:
        return 0.0
    g = EULER_MASCHERONI
    return math.sqrt(varianza_sharpes) * (
        (1 - g) * N01.inv_cdf(1 - 1 / n_pruebas) + g * N01.inv_cdf(1 - 1 / (n_pruebas * math.e)))


def dsr_desde_estadisticos(sr: float, n_obs: int, n_pruebas: int, varianza_sharpes: float,
                           asimetria_: float = 0.0, curtosis_: float = 3.0) -> float:
    """DSR = PSR evaluado en SR0 (todo por periodo, no anualizado)."""
    sr0 = sharpe_maximo_esperado(n_pruebas, varianza_sharpes)
    return psr_desde_estadisticos(sr, n_obs, asimetria_, curtosis_, sr0)


def sharpe_deflactado(rends, n_pruebas: int, varianza_sharpes: float, rf=0.0,
                      periodos_por_anio: int = PERIODOS_POR_ANIO,
                      varianza_anualizada: bool = False) -> float:
    """DSR de una estrategia elegida entre n_pruebas variantes.

    varianza_sharpes: varianza de los Sharpe de las pruebas; por periodo, o anualizada
    si varianza_anualizada=True (se divide entre periodos_por_anio).
    Criterio del sistema: DSR >= validacion_estrategias.deflated_sharpe_min_probabilidad.
    """
    ex = _excesos(rends, rf, periodos_por_anio)
    sr = statistics.fmean(ex) / statistics.stdev(ex)
    v = varianza_sharpes / periodos_por_anio if varianza_anualizada else varianza_sharpes
    return dsr_desde_estadisticos(sr, len(ex), n_pruebas, v, asimetria(ex), curtosis(ex))


# ---------------------------------------------------------------- pronosticos

def _validar_pronosticos(probabilidades, resultados) -> tuple[list[float], list[int]]:
    p = [float(x) for x in probabilidades]
    o = [int(x) for x in resultados]
    if len(p) != len(o) or not p:
        raise ValueError("Listas vacias o de distinta longitud")
    if any(not 0 <= x <= 1 for x in p) or any(x not in (0, 1) for x in o):
        raise ValueError("Probabilidades en [0,1] y resultados en {0,1}")
    return p, o


def brier(probabilidades, resultados) -> float:
    """Brier = media((p - o)^2). 0 perfecto; 0.25 = siempre 50%."""
    p, o = _validar_pronosticos(probabilidades, resultados)
    return statistics.fmean([(a - b) ** 2 for a, b in zip(p, o)])


def log_score(probabilidades, resultados, eps: float = 1e-6) -> float:
    """Media de ln(prob asignada al resultado observado). 0 perfecto; ln(0.5) = -0.693 moneda.

    Mayor es mejor. p se recorta a [eps, 1-eps] para evitar -inf. Log loss = -log_score.
    """
    p, o = _validar_pronosticos(probabilidades, resultados)
    total = 0.0
    for a, b in zip(p, o):
        a = min(max(a, eps), 1 - eps)
        total += math.log(a if b == 1 else 1 - a)
    return total / len(p)


def tabla_calibracion(probabilidades, resultados, n_cubetas: int = 10) -> list[dict]:
    """Calibracion por cubetas de igual ancho: n, prob media, frecuencia observada, diferencia."""
    p, o = _validar_pronosticos(probabilidades, resultados)
    cubetas = [[] for _ in range(n_cubetas)]
    for a, b in zip(p, o):
        i = min(int(round(a * n_cubetas, 9)), n_cubetas - 1)
        cubetas[i].append((a, b))
    tabla = []
    for i, c in enumerate(cubetas):
        fila = {"desde": i / n_cubetas, "hasta": (i + 1) / n_cubetas, "n": len(c),
                "prob_media": None, "frecuencia": None, "diferencia": None}
        if c:
            fila["prob_media"] = statistics.fmean([a for a, _ in c])
            fila["frecuencia"] = statistics.fmean([b for _, b in c])
            fila["diferencia"] = fila["frecuencia"] - fila["prob_media"]
        tabla.append(fila)
    return tabla


# ---------------------------------------------------------------- rachas

def prob_racha_perdedora(n: int, k: int, p_ganar: float) -> float:
    """P(al menos una racha de >= k perdidas seguidas en n operaciones independientes). Exacta (DP).

    Estado = longitud de la racha perdedora vigente (0..k-1); al llegar a k se absorbe.
    """
    if not 0 <= p_ganar <= 1:
        raise ValueError("p_ganar fuera de [0,1]")
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    q = 1 - p_ganar
    estado = [1.0] + [0.0] * (k - 1)
    absorbida = 0.0
    for _ in range(n):
        absorbida += q * estado[-1]
        total = sum(estado)
        estado = [p_ganar * total] + [q * x for x in estado[:-1]]
    return absorbida


def racha_esperada_max(n: int, p_ganar: float, tolerancia: float = 1e-15) -> float:
    """E[racha perdedora maxima en n operaciones] = suma_k P(racha >= k)."""
    esperado = 0.0
    for k in range(1, n + 1):
        pk = prob_racha_perdedora(n, k, p_ganar)
        esperado += pk
        if pk < tolerancia:
            break
    return esperado
