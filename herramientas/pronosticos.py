"""Bitacora de pronosticos probabilisticos y su puntuacion (Brier, log score, calibracion).

Uso:
    python3 herramientas/pronosticos.py agregar --pregunta "..." --probabilidad 0.65 \\
        --fecha-resolucion 2026-12-31 --criterio "..." [--autor claude] [--notas "..."]
    python3 herramientas/pronosticos.py resolver P0001 --resultado si|no|anulada [--fecha AAAA-MM-DD]
    python3 herramientas/pronosticos.py pendientes
    python3 herramientas/pronosticos.py vencidos [--hoy AAAA-MM-DD]
    python3 herramientas/pronosticos.py puntuar [--autor claude]
Opcion global: --archivo RUTA (por defecto bitacora/pronosticos.csv).
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import tempfile
from datetime import date
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from herramientas import metricas
from herramientas.parametros import DIR_BITACORA, obtener

COLUMNAS = ["id", "fecha_creacion", "autor", "pregunta", "probabilidad", "fecha_resolucion",
            "criterio_resolucion", "resultado", "fecha_resuelto", "notas"]
RUTA_DEFECTO = DIR_BITACORA / "pronosticos.csv"
VERDADERO = {"1", "si", "sí", "s", "true", "verdadero", "yes", "y"}
FALSO = {"0", "no", "n", "false", "falso"}
ANULADA = {"anulada", "anulado", "nula", "void", "na"}


class ErrorBitacora(Exception):
    """Operacion invalida sobre la bitacora."""


# ---------------------------------------------------------------- archivo

def asegurar_archivo(ruta: str | Path = RUTA_DEFECTO) -> Path:
    """Crea el CSV con encabezado si no existe."""
    ruta = Path(ruta)
    if not ruta.exists():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(COLUMNAS)
    return ruta


def leer(ruta: str | Path = RUTA_DEFECTO) -> list[dict]:
    ruta = asegurar_archivo(ruta)
    with open(ruta, newline="", encoding="utf-8") as f:
        return [dict(fila) for fila in csv.DictReader(f)]


def escribir(ruta: str | Path, filas: list[dict]) -> None:
    """Escritura atomica (archivo temporal + reemplazo)."""
    ruta = Path(ruta)
    fd, tmp = tempfile.mkstemp(dir=ruta.parent, suffix=".tmp")
    with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS)
        w.writeheader()
        for fila in filas:
            w.writerow({c: fila.get(c, "") for c in COLUMNAS})
    os.replace(tmp, ruta)


# ---------------------------------------------------------------- validacion

def parsear_probabilidad(texto) -> float:
    """Acepta 0.65 o '65%'. Debe quedar en [0, 1]."""
    t = str(texto).strip()
    p = float(t[:-1]) / 100 if t.endswith("%") else float(t)
    if not 0 <= p <= 1:
        raise ErrorBitacora(f"Probabilidad fuera de [0,1]: {texto} (use 0.65 o 65%)")
    return p


def parsear_resultado(texto) -> str:
    t = str(texto).strip().lower()
    if t in VERDADERO:
        return "1"
    if t in FALSO:
        return "0"
    if t in ANULADA:
        return "anulada"
    raise ErrorBitacora(f"Resultado invalido: {texto} (si/no/1/0/anulada)")


def _fecha(texto) -> str:
    return date.fromisoformat(str(texto)).isoformat()


# ---------------------------------------------------------------- operaciones

def siguiente_id(filas: list[dict]) -> str:
    numeros = [int(f["id"][1:]) for f in filas if f.get("id", "").startswith("P") and f["id"][1:].isdigit()]
    return f"P{(max(numeros) + 1) if numeros else 1:04d}"


def agregar(ruta: str | Path, pregunta: str, probabilidad, fecha_resolucion, criterio: str,
            autor: str = "claude", notas: str = "", fecha_creacion=None) -> dict:
    """Agrega un pronostico abierto y devuelve la fila."""
    if not pregunta.strip() or not criterio.strip():
        raise ErrorBitacora("Pregunta y criterio de resolucion son obligatorios")
    filas = leer(ruta)
    fila = {
        "id": siguiente_id(filas),
        "fecha_creacion": _fecha(fecha_creacion or date.today()),
        "autor": autor.strip(),
        "pregunta": pregunta.strip(),
        "probabilidad": f"{parsear_probabilidad(probabilidad):.4f}",
        "fecha_resolucion": _fecha(fecha_resolucion),
        "criterio_resolucion": criterio.strip(),
        "resultado": "", "fecha_resuelto": "", "notas": notas.strip(),
    }
    if fila["fecha_resolucion"] < fila["fecha_creacion"]:
        raise ErrorBitacora("La fecha de resolucion es anterior a la de creacion")
    filas.append(fila)
    escribir(ruta, filas)
    return fila


def resolver(ruta: str | Path, id_: str, resultado, fecha_resuelto=None, notas: str | None = None) -> dict:
    """Marca un pronostico como 1, 0 o anulada."""
    filas = leer(ruta)
    for fila in filas:
        if fila["id"] == id_:
            if fila["resultado"]:
                raise ErrorBitacora(f"{id_} ya estaba resuelto ({fila['resultado']})")
            fila["resultado"] = parsear_resultado(resultado)
            fila["fecha_resuelto"] = _fecha(fecha_resuelto or date.today())
            if notas:
                fila["notas"] = f"{fila['notas']} | {notas}".strip(" |")
            escribir(ruta, filas)
            return fila
    raise ErrorBitacora(f"No existe el pronostico {id_}")


def pendientes(ruta: str | Path = RUTA_DEFECTO) -> list[dict]:
    """Pronosticos sin resolver, por fecha de resolucion."""
    return sorted((f for f in leer(ruta) if not f["resultado"]), key=lambda f: f["fecha_resolucion"])


def vencidos(ruta: str | Path = RUTA_DEFECTO, hoy=None) -> list[dict]:
    """Pendientes con fecha_resolucion <= hoy (ya deben resolverse)."""
    limite = _fecha(hoy or date.today())
    return [f for f in pendientes(ruta) if f["fecha_resolucion"] <= limite]


def _puntuar_grupo(filas: list[dict]) -> dict:
    p = [float(f["probabilidad"]) for f in filas]
    o = [int(f["resultado"]) for f in filas]
    n = len(p)
    if n == 0:
        return {"n": 0}
    tasa_base = sum(o) / n
    b = metricas.brier(p, o)
    b_clima = tasa_base * (1 - tasa_base)
    return {
        "n": n,
        "brier": b,
        "brier_skill_vs_50": 1 - b / 0.25,
        "brier_climatologia": b_clima,
        "brier_skill_vs_climatologia": (1 - b / b_clima) if b_clima > 0 else None,
        "log_score": metricas.log_score(p, o),
        "tasa_base": tasa_base,
        "prob_media": sum(p) / n,
        "calibracion": metricas.tabla_calibracion(p, o, 10),
    }


def puntuar(ruta: str | Path = RUTA_DEFECTO, autor: str | None = None) -> dict:
    """Puntuacion global y por autor de pronosticos resueltos (anulados excluidos)."""
    resueltos = [f for f in leer(ruta) if f["resultado"] in ("0", "1")]
    if autor:
        resueltos = [f for f in resueltos if f["autor"] == autor]
    autores = sorted({f["autor"] for f in resueltos})
    return {
        "global": _puntuar_grupo(resueltos),
        "por_autor": {a: _puntuar_grupo([f for f in resueltos if f["autor"] == a]) for a in autores},
        "brier_objetivo": obtener("pronosticos.brier_objetivo"),
        "min_para_evaluar": obtener("pronosticos.min_pronosticos_para_evaluar"),
    }


# ---------------------------------------------------------------- presentacion

def _tabla(filas: list[dict], columnas: list[str]) -> str:
    if not filas:
        return "(sin registros)"
    salida = ["| " + " | ".join(columnas) + " |", "|" + "---|" * len(columnas)]
    for f in filas:
        salida.append("| " + " | ".join(str(f.get(c, "")).replace("|", "/") for c in columnas) + " |")
    return "\n".join(salida)


def formatear_puntuacion(res: dict) -> str:
    lineas = [f"Objetivo Brier <= {res['brier_objetivo']}; minimo {res['min_para_evaluar']} pronosticos para evaluar.", ""]
    grupos = [("GLOBAL", res["global"])] + list(res["por_autor"].items())
    lineas += ["| Grupo | n | Brier | Skill vs 50% | Skill vs tasa base | Log score | Tasa base | Veredicto |",
               "|---|---|---|---|---|---|---|---|"]
    for nombre, g in grupos:
        if not g.get("n"):
            lineas.append(f"| {nombre} | 0 | - | - | - | - | - | sin resueltos |")
            continue
        if g["n"] < res["min_para_evaluar"]:
            veredicto = "muestra insuficiente"
        else:
            veredicto = "cumple" if g["brier"] <= res["brier_objetivo"] else "NO cumple"
        bss = g["brier_skill_vs_climatologia"]
        lineas.append(f"| {nombre} | {g['n']} | {g['brier']:.4f} | {g['brier_skill_vs_50']:+.3f} | "
                      f"{'n/d' if bss is None else f'{bss:+.3f}'} | {g['log_score']:.4f} | "
                      f"{g['tasa_base']:.2f} | {veredicto} |")
    g = res["global"]
    if g.get("n"):
        lineas += ["", "Calibracion global (cubetas de 10 pp):", "",
                   "| Cubeta | n | Prob media | Frecuencia | Diferencia |", "|---|---|---|---|---|"]
        for c in g["calibracion"]:
            if c["n"]:
                lineas.append(f"| {c['desde']:.1f}-{c['hasta']:.1f} | {c['n']} | {c['prob_media']:.3f} | "
                              f"{c['frecuencia']:.3f} | {c['diferencia']:+.3f} |")
    return "\n".join(lineas)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Bitacora de pronosticos")
    ap.add_argument("--archivo", default=str(RUTA_DEFECTO), help="ruta del CSV de pronosticos")
    sub = ap.add_subparsers(dest="comando", required=True)
    a = sub.add_parser("agregar", help="registrar un pronostico")
    a.add_argument("--pregunta", required=True)
    a.add_argument("--probabilidad", required=True, help="0.65 o 65%%")
    a.add_argument("--fecha-resolucion", required=True)
    a.add_argument("--criterio", required=True, help="criterio verificable de resolucion")
    a.add_argument("--autor", default="claude")
    a.add_argument("--notas", default="")
    a.add_argument("--fecha-creacion", default=None)
    r = sub.add_parser("resolver", help="resolver un pronostico")
    r.add_argument("id")
    r.add_argument("--resultado", required=True, help="si/no/1/0/anulada")
    r.add_argument("--fecha", default=None)
    r.add_argument("--notas", default=None)
    sub.add_parser("pendientes", help="listar pronosticos abiertos")
    v = sub.add_parser("vencidos", help="abiertos con fecha de resolucion <= hoy")
    v.add_argument("--hoy", default=None)
    s = sub.add_parser("puntuar", help="Brier, log score y calibracion")
    s.add_argument("--autor", default=None)
    args = ap.parse_args(argv)

    cols = ["id", "autor", "probabilidad", "fecha_resolucion", "pregunta", "criterio_resolucion"]
    try:
        if args.comando == "agregar":
            f = agregar(args.archivo, args.pregunta, args.probabilidad, args.fecha_resolucion,
                        args.criterio, args.autor, args.notas, args.fecha_creacion)
            print(f"Agregado {f['id']}: p={f['probabilidad']} resuelve {f['fecha_resolucion']}")
        elif args.comando == "resolver":
            f = resolver(args.archivo, args.id, args.resultado, args.fecha, args.notas)
            print(f"Resuelto {f['id']}: resultado={f['resultado']} ({f['fecha_resuelto']})")
        elif args.comando == "pendientes":
            print(_tabla(pendientes(args.archivo), cols))
        elif args.comando == "vencidos":
            print(_tabla(vencidos(args.archivo, args.hoy), cols))
        elif args.comando == "puntuar":
            print(formatear_puntuacion(puntuar(args.archivo, args.autor)))
    except (ErrorBitacora, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
