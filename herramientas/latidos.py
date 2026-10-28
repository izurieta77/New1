"""Comprobación mecánica de las horas de los latidos (`bitacora/estado-rutinas.md`).

Problema que resuelve: siete reincidencias de "horas posteriores al commit" (revisiones del
11 al 27-oct-2026). Una hora escrita a mano ("~13:35", "13:1x") o calculada a ojo queda
después del commit que la registra. Aquí la regla deja de depender de la memoria:

  python3 herramientas/latidos.py ahora
      Imprime la hora que va en el latido: AAAA-MM-DD HH:MM UTC (de la máquina, no a mano).

  python3 herramientas/latidos.py antes-de-commit
      Revisa las líneas AGREGADAS en el staging (`git add` ya hecho) de estado-rutinas.md:
      formato exacto (sin "x", "~" ni rangos) y hora <= ahora (+1 min de tolerancia).
      Con --bitacora revisa además las horas "HH:Mx" o "~HH:MM" en lo agregado bajo bitacora/
      (solo avisa). Sale con código 1 si un latido no pasa.

  python3 herramientas/latidos.py auditar --desde AAAA-MM-DD
      Para cada commit desde esa fecha que tocó estado-rutinas.md, compara la hora de cada
      latido que agregó contra la hora del commit (UTC). Lista los que quedaron después.

Solo lee git; no escribe nada.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

ARCHIVO = "bitacora/estado-rutinas.md"
RE_LATIDO = re.compile(r"^(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}) UTC · ")
RE_INICIO_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2} ")
# horas aproximadas que no deben escribirse: "13:1x", "~13:35", "13:3x-13:4x"
RE_HORA_VAGA = re.compile(r"(~\s?\d{1,2}:\d{2}|\b\d{1,2}:\d[xX]\b)")
TOLERANCIA = timedelta(minutes=1)


def ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


def formato_latido(t: datetime) -> str:
    return t.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def hora_de_latido(linea: str) -> datetime | None:
    """Hora (UTC) de una línea de latido bien formada; None si no lo es."""
    m = RE_LATIDO.match(linea)
    if not m:
        return None
    f, h, mi = m.groups()
    return datetime.strptime(f"{f} {h}:{mi}", "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)


def revisar_linea(linea: str, referencia: datetime) -> str | None:
    """Devuelve el problema de un latido agregado, o None si pasa.

    referencia = ahora (antes del commit) o la hora del commit (auditoría).
    """
    if not RE_INICIO_FECHA.match(linea):
        return None  # no es un latido (encabezado u otra cosa)
    t = hora_de_latido(linea)
    if t is None:
        return "formato: se espera 'AAAA-MM-DD HH:MM UTC · ' (sin x, ~ ni rangos)"
    if t > referencia + TOLERANCIA:
        return f"hora {t:%H:%M} posterior a {referencia:%Y-%m-%d %H:%M:%S} UTC"
    return None


def lineas_agregadas(diff: str) -> list[tuple[str, str]]:
    """(archivo, línea) de cada línea agregada en un diff unificado."""
    out, actual = [], None
    for l in diff.splitlines():
        if l.startswith("+++ "):
            actual = l[6:] if l.startswith("+++ b/") else None
        elif l.startswith("+") and not l.startswith("+++") and actual:
            out.append((actual, l[1:].rstrip("\r")))
    return out


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def cmd_antes_de_commit(bitacora: bool) -> int:
    ref = ahora_utc()
    rutas = ["bitacora/"] if bitacora else [ARCHIVO]
    nuevas = lineas_agregadas(_git("diff", "--cached", "-U0", "--", *rutas))
    malos = 0
    for archivo, linea in nuevas:
        if archivo == ARCHIVO:
            p = revisar_linea(linea, ref)
            if p:
                malos += 1
                print(f"LATIDO MAL · {p}\n  {linea[:160]}")
        elif bitacora:
            for m in RE_HORA_VAGA.finditer(linea):
                print(f"aviso · hora vaga '{m.group(0)}' en {archivo}: {linea[:120]}")
    if malos:
        print(f"Corrige con la hora de la máquina: {formato_latido(ref)}")
        return 1
    print(f"OK · {sum(1 for a, _ in nuevas if a == ARCHIVO)} latido(s) revisado(s); ahora {formato_latido(ref)}")
    return 0


def cmd_auditar(desde: str) -> int:
    log = _git("log", f"--since={desde}T00:00:00Z", "--format=%H %cI", "--", ARCHIVO)
    total = malos = 0
    for fila in log.splitlines():
        sha, fecha = fila.split(" ", 1)
        t_commit = datetime.fromisoformat(fecha).astimezone(timezone.utc)
        diff = _git("show", "-U0", "--format=", sha, "--", ARCHIVO)
        for _, linea in lineas_agregadas(diff):
            if not RE_INICIO_FECHA.match(linea):
                continue
            total += 1
            p = revisar_linea(linea, t_commit)
            if p:
                malos += 1
                print(f"{sha[:7]} · {p} · {linea[:110]}")
    print(f"Latidos revisados: {total}; con problema: {malos}")
    return 1 if malos else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ahora")
    a = sub.add_parser("antes-de-commit")
    a.add_argument("--bitacora", action="store_true", help="avisar también horas vagas en bitacora/")
    b = sub.add_parser("auditar")
    b.add_argument("--desde", required=True)
    ns = ap.parse_args(argv)
    if ns.cmd == "ahora":
        print(formato_latido(ahora_utc()))
        return 0
    if ns.cmd == "antes-de-commit":
        return cmd_antes_de_commit(ns.bitacora)
    return cmd_auditar(ns.desde)


if __name__ == "__main__":
    sys.exit(main())
