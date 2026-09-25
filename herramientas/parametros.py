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


def niveles_cortacircuitos(parametros: dict | None = None) -> list[dict]:
    """Niveles de drawdown ordenados del mas leve (-0.08) al mas severo (-0.20)."""
    niveles = obtener("cortacircuitos_drawdown", parametros)
    return sorted(niveles, key=lambda n: n["nivel"], reverse=True)
