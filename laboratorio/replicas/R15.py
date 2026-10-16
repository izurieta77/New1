#!/usr/bin/env python3
"""R15 - USD/MXN despues de un episodio FX-1 (>= 6% sobre el minimo de 15 dias). Ejecucion A.

Reproduce desde la raiz del repo:  python3 laboratorio/replicas/R15.py
Pre-registro: laboratorio/replicas/R15-fx1-episodio-peso.md. Datos: FRED DEXMXUS (fredgraph CSV).
"""
from __future__ import annotations

import hashlib
import json
import math
import statistics
import sys
import urllib.request
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DATOS = AQUI / "R15-datos"
FIN = date(2026, 10, 15)
N_REF, UMBRAL, SEP = 15, 0.06, 20


def serie():
    DATOS.mkdir(exist_ok=True)
    ruta = DATOS / "DEXMXUS.csv"
    if not ruta.exists():
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXMXUS"
        ruta.write_bytes(urllib.request.urlopen(url, timeout=60).read())
    crudo = ruta.read_bytes()
    out, faltan = [], 0
    for linea in crudo.decode().splitlines()[1:]:
        f, v = linea.split(",")
        d = date.fromisoformat(f)
        if d > FIN:
            continue
        if v in ("", "."):
            faltan += 1
            continue
        out.append((d, float(v)))
    return out, faltan, hashlib.sha256(crudo).hexdigest()


def episodios(s, signo):
    x = [v for _, v in s]
    ev = []
    for t in range(N_REF, len(x)):
        ventana = x[t - N_REF:t]
        if signo > 0 and x[t] >= 1.06 * min(ventana) or signo < 0 and x[t] <= 0.94 * max(ventana):
            ev.append(t)
    prim = []
    for t in ev:
        if not prim or t - ultimo >= SEP:
            prim.append(t)
        ultimo = t
    return prim


def analizar(s, desde, h, signo=1):
    s = [(d, v) for d, v in s if d >= desde]
    x = [v for _, v in s]
    prim = [t for t in episodios(s, signo) if t + h < len(x)]
    cambios = [x[t + h] / x[t] - 1 for t in prim]
    incond = [x[i + h] / x[i] - 1 for i in range(len(x) - h)]
    mu = statistics.mean(incond)
    exceso = [c - mu for c in cambios]
    t_stat = statistics.mean(exceso) / (statistics.stdev(exceso) / math.sqrt(len(exceso))) if len(exceso) > 1 else float("nan")
    f3 = sum(c >= 0.03 for c in cambios) / len(cambios) if cambios else float("nan")
    f3_inc = sum(c >= 0.03 for c in incond) / len(incond)
    return {"episodios": len(prim), "fechas": [s[t][0].isoformat() for t in prim],
            "media_posterior": statistics.mean(cambios) if cambios else float("nan"),
            "media_incondicional": mu, "t_exceso": t_stat, "frec_mas3": f3, "frec_mas3_incond": f3_inc,
            "positivos": sum(c > 0 for c in cambios) / len(cambios) if cambios else float("nan")}


def main():
    s, faltan, sha = serie()
    out = [f"FRED DEXMXUS: {s[0][0]} a {s[-1][0]}, {len(s)} datos, {faltan} faltantes, sha256 {sha[:16]}…", ""]
    res = {"fuente": {"inicio": s[0][0].isoformat(), "fin": s[-1][0].isoformat(), "sha256": sha}, "variantes": {}}
    for nombre, desde in (("completa", s[0][0]), ("desde1996", date(1996, 1, 1))):
        for h in (10, 20):
            r = analizar(s, desde, h)
            res["variantes"][f"{nombre}_h{h}"] = r
            out.append(f"{nombre:10s} h={h:2d}: episodios {r['episodios']:2d} | media posterior {r['media_posterior']:+.2%} "
                       f"(incond. {r['media_incondicional']:+.2%}) | t exceso {r['t_exceso']:+.2f} | positivos {r['positivos']:.0%} | "
                       f"+3% o más {r['frec_mas3']:.0%} (incond. {r['frec_mas3_incond']:.0%})")
    out.append("")
    p = res["variantes"]["desde1996_h20"]
    out.append("Episodios (desde 1996, primer día): " + ", ".join(p["fechas"]))
    esp = analizar(s, date(1996, 1, 1), 20, signo=-1)
    res["espejo_baja_desde1996_h20"] = esp
    out.append(f"Espejo a la baja (informativo, desde 1996, h=20): episodios {esp['episodios']}, media posterior "
               f"{esp['media_posterior']:+.2%}, t {esp['t_exceso']:+.2f}")
    h1 = p["media_posterior"] < p["media_incondicional"] and p["t_exceso"] <= -1.0
    h2 = p["frec_mas3"] < 0.30
    estado = "Replicado" if h1 and h2 else ("Replicado con diferencias" if h1 or h2 else "No replicado")
    res["veredicto"] = {"H1": h1, "H2": h2, "estado_A": estado}
    out.append(f"Veredicto A (20 días, desde 1996): H1 {'sostenida' if h1 else 'refutada'}; H2 {'sostenida' if h2 else 'refutada'} -> {estado}")
    txt = "\n".join(out) + "\n"
    (AQUI / "R15-salida.txt").write_text(txt, encoding="utf-8")
    (AQUI / "R15-resultados.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    sys.stdout.write(txt)


if __name__ == "__main__":
    main()
