"""Carga de config/parametros.json, fuente unica de verdad de los limites de riesgo.

Ningun modulo del kit define limites propios: todos los leen de aqui. Si una clave
no existe se lanza KeyError; nunca se inventa un valor por defecto.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

RAIZ_REPO = Path(__file__).resolve().parent.parent
RUTA_PARAMETROS = RAIZ_REPO / "config" / "parametros.json"
DIR_BITACORA = RAIZ_REPO / "bitacora"
DIR_CACHE = RAIZ_REPO / "datos" / "cache"


@lru_cache(maxsize=8)
def _leer(ruta: str) -> dict:
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def cargar_parametros(ruta: str | Path | None = None, recargar: bool = False) -> dict:
    """Devuelve el diccionario de parametros (copia profunda, segura de mutar)."""
    ruta = str(Path(ruta) if ruta else RUTA_PARAMETROS)
    if recargar:
        _leer.cache_clear()
    return json.loads(json.dumps(_leer(ruta)))


def obtener(clave: str, parametros: dict | None = None) -> Any:
    """Lee una clave con notacion punteada, p. ej. 'kelly.fraccion_max'.

    Lanza KeyError si no existe: los limites no se inventan.
    """
    nodo: Any = parametros if parametros is not None else cargar_parametros()
    recorrido = []
    for parte in clave.split("."):
        recorrido.append(parte)
        if not isinstance(nodo, dict) or parte not in nodo:
            raise KeyError(f"Parametro inexistente en parametros.json: {'.'.join(recorrido)}")
        nodo = nodo[parte]
    return nodo


PERFIL_ESTANDAR = "estandar"


def parametros_efectivos(perfil: str | None = None, parametros: dict | None = None) -> dict:
    """Parametros de nivel superior con las sustituciones del perfil indicado.

    El perfil 'estandar' (o None) es el nivel superior tal cual. Otro perfil, p. ej.
    'arena_agresivo', sustituye cortacircuitos y combina rachas, limites de perdida,
    concentracion y estructura; su riesgo por operacion (escalar) y su Kelly se traducen
    al formato del nivel superior. Las claves que el perfil no trae se heredan.
    """
    base = json.loads(json.dumps(parametros if parametros is not None else cargar_parametros()))
    if perfil in (None, "", PERFIL_ESTANDAR):
        base["perfil_activo"] = PERFIL_ESTANDAR
        return base
    prof = obtener(f"perfiles_riesgo.{perfil}", base)
    if not isinstance(prof, dict):
        raise KeyError(f"Perfil de riesgo sin definicion: {perfil}")
    if "cortacircuitos_drawdown" in prof:
        base["cortacircuitos_drawdown"] = prof["cortacircuitos_drawdown"]
    for clave in ("rachas", "limites_perdida", "concentracion", "estructura"):
        if isinstance(prof.get(clave), dict):
            base[clave] = {**base.get(clave, {}), **prof[clave]}
    rpo = prof.get("riesgo_por_operacion")
    if isinstance(rpo, (int, float)):
        base["riesgo_por_operacion"] = {**base["riesgo_por_operacion"], "max_riesgo_pct_capital": float(rpo),
                                        "max_riesgo_pct_capital_fase_prueba": float(rpo)}
    elif isinstance(rpo, dict):
        base["riesgo_por_operacion"] = {**base["riesgo_por_operacion"], **rpo}
    if "kelly_fraccion_max" in prof:
        base["kelly"] = {**base.get("kelly", {}), "fraccion_max": prof["kelly_fraccion_max"]}
    if "perdida_maxima_tolerable_mxn" in prof:
        base["perdida_maxima_tolerable_mxn"] = prof["perdida_maxima_tolerable_mxn"]
    base["perfil_activo"] = perfil
    return base


def niveles_cortacircuitos(parametros: dict | None = None) -> list[dict]:
    """Niveles de drawdown del perfil recibido, del mas leve al mas severo."""
    niveles = obtener("cortacircuitos_drawdown", parametros)
    return sorted(niveles, key=lambda n: n["nivel"], reverse=True)
