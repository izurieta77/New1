"""Sizing, Kelly, cortacircuitos, rachas y validacion de ordenes.

Todos los limites salen de config/parametros.json via parametros.obtener();
ninguna funcion trae limites propios. Montos en MXN salvo que se indique tipo_cambio.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from herramientas import metricas
from herramientas.parametros import cargar_parametros, niveles_cortacircuitos, obtener


# ---------------------------------------------------------------- sizing

def tamano_por_stop(capital: float, entrada: float, stop: float, riesgo_pct: float | None = None,
                    fase_prueba: bool = False, tipo_cambio: float = 1.0, lote: float = 1,
                    parametros: dict | None = None) -> dict:
    """Unidades tales que ejecutar el stop cueste <= riesgo_pct del capital.

    riesgo_pct por defecto = riesgo_por_operacion.max_riesgo_pct_capital (o _fase_prueba);
    si se pide mas que el maximo, se recorta al maximo. entrada/stop en moneda del activo;
    tipo_cambio convierte a MXN. Funciona para largos (stop < entrada) y cortos (stop > entrada).
    """
    clave = "max_riesgo_pct_capital_fase_prueba" if fase_prueba else "max_riesgo_pct_capital"
    maximo = obtener(f"riesgo_por_operacion.{clave}", parametros)
    pedido = maximo if riesgo_pct is None else riesgo_pct
    usado = min(pedido, maximo)
    riesgo_unidad = abs(entrada - stop) * tipo_cambio
    if riesgo_unidad <= 0 or capital <= 0:
        raise ValueError("Capital positivo y stop distinto de la entrada")
    unidades = math.floor(capital * usado / riesgo_unidad / lote) * lote
    valor = unidades * entrada * tipo_cambio
    return {
        "unidades": unidades,
        "lado": "largo" if stop < entrada else "corto",
        "riesgo_por_unidad_mxn": riesgo_unidad,
        "riesgo_mxn": unidades * riesgo_unidad,
        "riesgo_pct": unidades * riesgo_unidad / capital,
        "riesgo_pct_usado": usado,
        "recortado_al_maximo": pedido > maximo,
        "valor_posicion_mxn": valor,
        "peso_capital": valor / capital,
        "excede_concentracion_individual": valor / capital > obtener(
            "concentracion.accion_individual_max", parametros),
    }


def tamano_vol_objetivo(capital: float, vol_objetivo: float, vol_activo: float,
                        peso_max: float | None = None, parametros: dict | None = None) -> dict:
    """Peso = vol_objetivo / vol_activo, topado en peso_max (por defecto apalancamiento.bruto_max_fase_1)."""
    if vol_activo <= 0:
        raise ValueError("vol_activo debe ser positiva")
    tope = obtener("apalancamiento.bruto_max_fase_1", parametros) if peso_max is None else peso_max
    bruto = vol_objetivo / vol_activo
    peso = min(bruto, tope)
    return {"peso": peso, "peso_sin_tope": bruto, "monto_mxn": capital * peso,
            "limitado_por_tope": bruto > tope, "vol_esperada": peso * vol_activo}


def kelly(p: float, b: float) -> float:
    """Fraccion de Kelly f* = p - (1-p)/b (b = ganancia/perdida por unidad). Negativo = no apostar."""
    if b <= 0 or not 0 <= p <= 1:
        raise ValueError("b > 0 y p en [0,1]")
    return p - (1 - p) / b


def kelly_fraccional(p: float, b: float, fraccion: float | None = None,
                     parametros: dict | None = None) -> float:
    """max(0, f*) * fraccion, con fraccion topada en kelly.fraccion_max."""
    tope = obtener("kelly.fraccion_max", parametros)
    fraccion = tope if fraccion is None else min(fraccion, tope)
    return max(0.0, kelly(p, b)) * fraccion


# ---------------------------------------------------------------- cortacircuitos y rachas

def estado_cortacircuitos(curva_equity, parametros: dict | None = None) -> dict:
    """Drawdown actual vs maximo historico y nivel de cortacircuitos activado (el mas severo alcanzado)."""
    fechas, valores = metricas._separar(curva_equity)
    if not valores:
        raise ValueError("Curva vacia")
    i_pico = max(range(len(valores)), key=lambda i: (valores[i], -i))
    pico = valores[i_pico]
    dd = valores[-1] / pico - 1
    activado, siguiente = None, None
    for i, nivel in enumerate(niveles_cortacircuitos(parametros)):
        if dd <= nivel["nivel"] + 1e-12:
            activado = {**nivel, "indice": i}
        elif siguiente is None:
            siguiente = nivel
    return {
        "drawdown_actual": dd,
        "fecha_pico": fechas[i_pico],
        "valor_pico": pico,
        "nivel_activado": activado["nivel"] if activado else None,
        "indice_nivel": activado["indice"] if activado else None,
        "accion": activado["accion"] if activado else "Sin restriccion: operar normal",
        "siguiente_nivel": siguiente["nivel"] if siguiente else None,
        "distancia_siguiente": (dd - siguiente["nivel"]) if siguiente else None,
    }


def factor_por_rachas(resultados, parametros: dict | None = None) -> dict:
    """Factor de riesgo de una estrategia segun sus rachas (resultados en orden cronologico).

    Reglas (parametros.rachas): N perdidas seguidas -> factor_reduccion; M ganadoras
    seguidas estando reducido -> 1.0; P perdidas seguidas -> pausa (factor 0, persistente
    hasta revision: tras revisar, pasar solo resultados posteriores). Resultados = 0 se ignoran.
    """
    r = obtener("rachas", parametros)
    n_reducir, factor_red = r["perdedoras_para_reducir"], r["factor_reduccion"]
    n_restaurar, n_pausa = r["ganadoras_para_restaurar"], r["perdedoras_para_pausa"]
    factor, estado = 1.0, "normal"
    perdidas = ganadas = 0
    for x in metricas._valores(resultados):
        if x == 0:
            continue
        if x < 0:
            perdidas, ganadas = perdidas + 1, 0
        else:
            ganadas, perdidas = ganadas + 1, 0
        if estado == "pausa":
            continue
        if perdidas >= n_pausa:
            factor, estado = 0.0, "pausa"
        elif perdidas >= n_reducir:
            factor, estado = factor_red, "reducido"
        elif estado == "reducido" and ganadas >= n_restaurar:
            factor, estado = 1.0, "normal"
    acciones = {
        "normal": "Riesgo completo",
        "reducido": f"Riesgo x{factor_red} hasta {n_restaurar} ganadoras seguidas",
        "pausa": r["accion_pausa"],
    }
    return {"factor": factor, "estado": estado, "perdidas_consecutivas": perdidas,
            "ganadoras_consecutivas": ganadas, "accion": acciones[estado]}


# ---------------------------------------------------------------- validacion de ordenes

CLASES_VALIDAS = {"accion", "etf", "fondo", "cripto", "opcion", "deuda_privada",
                  "deuda_gubernamental", "fibra", "efectivo", "otro"}


def validar_orden(portafolio: dict, orden: dict, parametros: dict | None = None) -> dict:
    """Revisa una orden contra concentracion, cripto, opciones, deuda privada, satelite,
    apalancamiento, riesgo por operacion y limites de perdida diaria/semanal/mensual.

    portafolio = {
      "capital": equity total MXN,
      "posiciones": {ticker: {"valor_mxn": float con signo, "clase": str, "sector": str|None,
                              "tactica": bool, "emisor": str|None, "prima_en_riesgo_mxn": float}},
      "pnl_dia": MXN, "pnl_semana": MXN, "pnl_mes": MXN   (negativo = perdida),
      "fase": 0|1|2,
    }
    orden = {"ticker", "lado": "compra"|"venta", "cantidad", "precio", "tipo_cambio": 1.0,
             "clase", "sector", "tactica": bool, "stop": float|None, "emisor", "fase_prueba": bool}
    Ordenes que solo reducen exposicion se aprueban siempre (con advertencias).
    """
    p = parametros if parametros is not None else cargar_parametros()
    capital = float(portafolio["capital"])
    if capital <= 0:
        raise ValueError("Capital debe ser positivo")
    posiciones = {t: dict(v) for t, v in portafolio.get("posiciones", {}).items()}
    violaciones: list[str] = []
    advertencias: list[str] = []

    ticker = orden["ticker"]
    lado = orden["lado"].lower()
    if lado not in ("compra", "venta"):
        raise ValueError("lado debe ser 'compra' o 'venta'")
    fx = float(orden.get("tipo_cambio", 1.0))
    clase = orden.get("clase", "otro")
    if clase not in CLASES_VALIDAS:
        advertencias.append(f"Clase '{clase}' no reconocida; se trata como 'otro'")
    monto = float(orden["cantidad"]) * float(orden["precio"]) * fx
    signo = 1 if lado == "compra" else -1

    actual = posiciones.get(ticker, {"valor_mxn": 0.0, "clase": clase, "sector": orden.get("sector"),
                                     "tactica": orden.get("tactica", False), "emisor": orden.get("emisor"),
                                     "prima_en_riesgo_mxn": 0.0})
    valor_previo = float(actual.get("valor_mxn", 0.0))
    valor_nuevo = valor_previo + signo * monto
    reduce_exposicion = abs(valor_nuevo) < abs(valor_previo) - 1e-9 and valor_previo * valor_nuevo >= 0

    nueva = {**actual, "valor_mxn": valor_nuevo}
    for campo in ("clase", "sector", "tactica", "emisor"):
        if orden.get(campo) is not None:
            nueva[campo] = orden[campo]
    if clase == "opcion" and lado == "compra":
        nueva["prima_en_riesgo_mxn"] = float(actual.get("prima_en_riesgo_mxn", 0.0)) + monto
    posiciones[ticker] = nueva

    def peso(filtro) -> float:
        return sum(abs(float(v.get("valor_mxn", 0))) for v in posiciones.values() if filtro(v)) / capital

    conc = p["concentracion"]
    metricas_post = {
        "peso_posicion": abs(valor_nuevo) / capital,
        "bruto": peso(lambda v: True),
        "cripto": peso(lambda v: v.get("clase") == "cripto"),
        "satelite": peso(lambda v: v.get("tactica")),
        "prima_opciones": sum(float(v.get("prima_en_riesgo_mxn", 0)) for v in posiciones.values()) / capital,
    }
    if nueva.get("sector"):
        metricas_post["sector"] = peso(lambda v: v.get("sector") == nueva["sector"])
    if nueva.get("clase") == "deuda_privada" and nueva.get("emisor"):
        metricas_post["emisor"] = peso(lambda v: v.get("clase") == "deuda_privada"
                                       and v.get("emisor") == nueva["emisor"])

    if reduce_exposicion:
        advertencias.append("Orden reduce exposicion: se aprueba sin revisar limites de apertura")
        return {"aprobada": True, "violaciones": [], "advertencias": advertencias,
                "metricas_post": metricas_post}

    if nueva.get("clase") == "accion" and metricas_post["peso_posicion"] > conc["accion_individual_max"]:
        violaciones.append(f"Accion individual {metricas_post['peso_posicion']:.1%} > "
                           f"{conc['accion_individual_max']:.0%}")
    if "sector" in metricas_post and metricas_post["sector"] > conc["sector_max"]:
        violaciones.append(f"Sector {nueva['sector']} {metricas_post['sector']:.1%} > {conc['sector_max']:.0%}")
    if metricas_post["cripto"] > conc["cripto_max"]:
        violaciones.append(f"Cripto {metricas_post['cripto']:.1%} > {conc['cripto_max']:.0%}")
    if metricas_post["prima_opciones"] > conc["opciones_prima_en_riesgo_max"]:
        violaciones.append(f"Prima de opciones en riesgo {metricas_post['prima_opciones']:.1%} > "
                           f"{conc['opciones_prima_en_riesgo_max']:.0%}")
    if "emisor" in metricas_post and metricas_post["emisor"] > conc["emisor_deuda_privada_max"]:
        violaciones.append(f"Emisor {nueva['emisor']} {metricas_post['emisor']:.1%} > "
                           f"{conc['emisor_deuda_privada_max']:.0%}")
    if nueva.get("tactica") and metricas_post["satelite"] > p["estructura"]["satelite_max"]:
        violaciones.append(f"Satelite {metricas_post['satelite']:.1%} > {p['estructura']['satelite_max']:.0%}")

    fase = int(portafolio.get("fase", 1))
    tope_bruto = p["apalancamiento"]["bruto_max_fase_2" if fase >= 2 else "bruto_max_fase_1"]
    if metricas_post["bruto"] > tope_bruto + 1e-9:
        violaciones.append(f"Exposicion bruta {metricas_post['bruto']:.2f}x > {tope_bruto:.2f}x (fase {fase})")

    if orden.get("stop") is not None:
        clave = "max_riesgo_pct_capital_fase_prueba" if orden.get("fase_prueba") else "max_riesgo_pct_capital"
        riesgo = float(orden["cantidad"]) * abs(float(orden["precio"]) - float(orden["stop"])) * fx / capital
        metricas_post["riesgo_operacion"] = riesgo
        if riesgo > p["riesgo_por_operacion"][clave] + 1e-12:
            violaciones.append(f"Riesgo al stop {riesgo:.2%} > {p['riesgo_por_operacion'][clave]:.2%}")
    elif nueva.get("tactica"):
        advertencias.append("Orden tactica sin stop: no se puede verificar riesgo por operacion")

    if nueva.get("tactica"):
        for periodo in ("diaria", "semanal", "mensual"):
            campo = {"diaria": "pnl_dia", "semanal": "pnl_semana", "mensual": "pnl_mes"}[periodo]
            pnl = float(portafolio.get(campo, 0.0)) / capital
            if pnl <= -p["limites_perdida"][periodo]:
                violaciones.append(f"Limite de perdida {periodo} tocado ({pnl:.2%}): "
                                   f"{p['limites_perdida']['accion']}")

    return {"aprobada": not violaciones, "violaciones": violaciones,
            "advertencias": advertencias, "metricas_post": metricas_post}
