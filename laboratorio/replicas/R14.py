#!/usr/bin/env python3
"""R14 - Rebote de indices tras un desplome de un dia. Ejecucion A.

Reproduce desde la raiz del repo:  python3 laboratorio/replicas/R14.py
Pre-registro: laboratorio/replicas/R14-rebote-tras-desplome.md (secciones 1-9).
Datos: Yahoo chart v8 diario (period1/period2) de ^GSPC, ^IXIC, ^N225 y ^KS11, hasta el 14-oct-2026.
Guarda los datos descargados en R14-datos/ (con sha256) y escribe R14-salida.txt y R14-resultados.json.
"""
from __future__ import annotations

import hashlib
import json
import math
import statistics
import sys
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DATOS = AQUI / "R14-datos"
INDICES = ["^GSPC", "^IXIC", "^N225", "^KS11"]
FIN = date(2026, 10, 14)
UMBRALES = [-0.05, -0.07]
HORIZONTES = [11, 22]
SEP_EPISODIO = 11
P2 = int(datetime(2026, 10, 15, tzinfo=timezone.utc).timestamp())


def descargar(sim):
    DATOS.mkdir(exist_ok=True)
    ruta = DATOS / (sim.replace("^", "") + ".json")
    if not ruta.exists():
        url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.request.quote(sim)}"
               f"?period1=0&period2={P2}&interval=1d")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        ruta.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    crudo = ruta.read_bytes()
    r = json.loads(crudo)["chart"]["result"][0]
    serie, descartes = [], 0
    for t, c in zip(r["timestamp"], r["indicators"]["quote"][0]["close"]):
        d = datetime.fromtimestamp(t, tz=timezone.utc).date()
        if c is None or d > FIN:
            descartes += c is None
            continue
        if serie and (d <= serie[-1][0] or c == serie[-1][1]):
            descartes += 1
            continue
        serie.append((d, c))
    return serie, descartes, hashlib.sha256(crudo).hexdigest()


def eventos(serie, umbral, h):
    precios = [c for _, c in serie]
    out = []
    for i in range(1, len(precios) - h):
        r = precios[i] / precios[i - 1] - 1
        if r <= umbral:
            out.append({"i": i, "fecha": serie[i][0].isoformat(), "caida": r,
                        "adelante": precios[i + h] / precios[i] - 1})
    return out


def incondicional(serie, h):
    p = [c for _, c in serie]
    x = [p[i + h] / p[i] - 1 for i in range(len(p) - h)]
    return statistics.mean(x), sum(v > 0 for v in x) / len(x)


def episodios(ev):
    grupos = []
    for e in ev:
        if grupos and e["i"] - grupos[-1][-1]["i"] < SEP_EPISODIO:
            grupos[-1].append(e)
        else:
            grupos.append([e])
    return grupos


def t_stat(x):
    if len(x) < 2:
        return float("nan")
    return statistics.mean(x) / (statistics.stdev(x) / math.sqrt(len(x)))


def main():
    out, res = [], {"indices": {}, "variantes": {}}
    p = out.append
    series = {}
    for s in INDICES:
        serie, desc, sha = descargar(s)
        series[s] = serie
        res["indices"][s] = {"inicio": serie[0][0].isoformat(), "fin": serie[-1][0].isoformat(),
                             "n": len(serie), "descartes": desc, "sha256": sha}
        p(f"{s}: {serie[0][0]} a {serie[-1][0]}, {len(serie)} cierres, {desc} descartados, sha256 {sha[:16]}…")
    p("")
    for u in UMBRALES:
        for h in HORIZONTES:
            clave = f"u{int(u*100)}_h{h}"
            todos, ep_exceso, ep_pos, prim_exceso, prim_pos = [], [], [], [], []
            p(f"== Umbral {u:.0%}, horizonte {h} días ==")
            for s in INDICES:
                ev = eventos(series[s], u, h)
                mu, f0 = incondicional(series[s], h)
                gs = episodios(ev)
                for e in ev:
                    e["exceso"] = e["adelante"] - mu
                todos += ev
                for g in gs:
                    ep_exceso.append(statistics.mean(e["exceso"] for e in g))
                    ep_pos.append(statistics.mean(e["adelante"] > 0 for e in g))
                    prim_exceso.append(g[0]["exceso"])
                    prim_pos.append(g[0]["adelante"] > 0)
                fr = sum(e["adelante"] > 0 for e in ev) / len(ev) if ev else float("nan")
                ex = statistics.mean(e["exceso"] for e in ev) if ev else float("nan")
                p(f"  {s:6s} eventos {len(ev):3d} episodios {len(gs):3d} | positivos {fr:.1%} (incond. {f0:.1%})"
                  f" | exceso medio {ex:+.2%} (media incond. {mu:+.2%})")
            n = len(todos)
            freq = sum(e["adelante"] > 0 for e in todos) / n
            ex_ev = statistics.mean(e["exceso"] for e in todos)
            r = {"eventos": n, "episodios": len(ep_exceso), "frecuencia_positivos": freq,
                 "exceso_medio_eventos": ex_ev, "exceso_medio_episodios": statistics.mean(ep_exceso),
                 "t_episodios": t_stat(ep_exceso), "primeros_frecuencia": sum(prim_pos) / len(prim_pos),
                 "primeros_exceso": statistics.mean(prim_exceso), "primeros_t": t_stat(prim_exceso)}
            res["variantes"][clave] = r
            p(f"  AGRUPADO: {n} eventos, {r['episodios']} episodios | positivos {freq:.1%} | exceso medio "
              f"{ex_ev:+.2%} (por episodio {r['exceso_medio_episodios']:+.2%}, t {r['t_episodios']:+.2f})")
            p(f"  Solo primer desplome: positivos {r['primeros_frecuencia']:.1%}, exceso {r['primeros_exceso']:+.2%},"
              f" t {r['primeros_t']:+.2f}")
            p("")
    v = res["variantes"]["u-5_h11"]
    h1 = v["frecuencia_positivos"] > 0.55
    h2 = v["exceso_medio_episodios"] > 0 and v["t_episodios"] >= 1.0
    estado = "Replicado" if h1 and h2 else ("Replicado con diferencias" if h1 or h2 else "No replicado")
    res["veredicto"] = {"H1": h1, "H2": h2, "estado_A": estado}
    p(f"Veredicto A (principal -5%, 11 días): H1 {'sostenida' if h1 else 'refutada'}; "
      f"H2 {'sostenida' if h2 else 'refutada'} -> {estado}")
    txt = "\n".join(out) + "\n"
    (AQUI / "R14-salida.txt").write_text(txt, encoding="utf-8")
    (AQUI / "R14-resultados.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    sys.stdout.write(txt)


if __name__ == "__main__":
    main()
