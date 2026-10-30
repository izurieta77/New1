"""Lista de empresas con pronósticos de resultados por resolver (para el cierre y la conciliación).

Problema que resuelve (28/29-oct-2026): los cierres armaban su lista con el calendario del brief y se les
pasaron KOF, Walmex y Alphabet, más un rezago de 25 empresas. Aquí la lista sale de los datos:
toda `empresas/<T>/pronosticos.csv` con fecha_resolucion <= hoy + N días y sin `resoluciones.csv`
que cubra esos ids.

  python3 herramientas/rezago_empresas.py [--hoy AAAA-MM-DD] [--dias 3] [--md]

Solo lee archivos del repo.
"""
from __future__ import annotations
import argparse, csv, datetime as dt, os, sys

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def pendientes(hoy: dt.date, dias: int, raiz: str = RAIZ):
    out = []
    base = os.path.join(raiz, "empresas")
    for t in sorted(os.listdir(base)):
        p = os.path.join(base, t, "pronosticos.csv")
        if not os.path.isfile(p):
            continue
        resueltos = set()
        r = os.path.join(base, t, "resoluciones.csv")
        if os.path.isfile(r):
            resueltos = {row["id"] for row in csv.DictReader(open(r, encoding="utf-8"))}
        filas = [row for row in csv.DictReader(open(p, encoding="utf-8"))
                 if row.get("fecha_resolucion") and row["id"] not in resueltos]
        lim = hoy + dt.timedelta(days=dias)
        filas = [f for f in filas if dt.date.fromisoformat(f["fecha_resolucion"][:10]) <= lim]
        if filas:
            fmin = min(f["fecha_resolucion"][:10] for f in filas)
            out.append({"ticker": t, "fecha_min": fmin, "n": len(filas),
                        "vencido": dt.date.fromisoformat(fmin) <= hoy,
                        "ids": [f["id"] for f in filas]})
    return sorted(out, key=lambda z: (z["fecha_min"], z["ticker"]))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Empresas con pronósticos por resolver")
    ap.add_argument("--hoy", default=dt.date.today().isoformat())
    ap.add_argument("--dias", type=int, default=3)
    ap.add_argument("--md", action="store_true", help="salida como tabla Markdown")
    ns = ap.parse_args(argv)
    hoy = dt.date.fromisoformat(ns.hoy)
    p = pendientes(hoy, ns.dias)
    if ns.md:
        print("| Empresa | Fecha más temprana | Pronósticos sin resolver | Estado |\n|---|---|---|---|")
        for x in p:
            print(f"| {x['ticker']} | {x['fecha_min']} | {x['n']} | {'**VENCIDO**' if x['vencido'] else 'por vencer'} |")
    else:
        for x in p:
            print(f"{x['ticker']:14s} {x['fecha_min']} n={x['n']} {'VENCIDO' if x['vencido'] else 'por vencer'}")
    print(f"Total: {len(p)} empresas ({sum(1 for x in p if x['vencido'])} vencidas) con hoy={hoy} y ventana de {ns.dias} días")
    return 0


if __name__ == "__main__":
    sys.exit(main())
