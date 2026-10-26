"""E1 (método F, conocimiento/cripto/lista-senales-de-alerta.md §F), réplica literal de la conciliación.

Fallo bitacora/arbitraje/2026-10-25.md §4 (2.3). No es la herramienta oficial: llevar E1 a herramientas/
con una prueba sigue en manos del trabajo continuo.

Flujo neto de t-7 a t = Σ_token (unidades_t − unidades_{t−7}) × precio_t, con precio_t = USD_t / unidades_t,
sin BNB, solo filas de 00:00 UTC (la API agrega una fila intradía que duplica el total), todas las cadenas
de `chainTvls`. Se reporta como % de Σ unidades_{t−7} × precio_t.

Uso (el JSON es dato descargado: guárdalo en un directorio propio y corre con -I):
    curl -sS -o <dir>/binance-cex.json https://api.llama.fi/protocol/binance-cex
    python3 -I 2026-10-25-e1-metodo-f.py <dir>/binance-cex.json 2026-10-24 2026-10-25
"""
import datetime as dt
import json
import sys


def series(d):
    U, V = {}, {}
    for o in d["chainTvls"].values():
        for clave, D in (("tokens", U), ("tokensInUsd", V)):
            for fila in o.get(clave) or []:
                t = dt.datetime.fromtimestamp(fila["date"], dt.timezone.utc)
                if t.hour or t.minute:
                    continue
                dia = D.setdefault(t.date(), {})
                for k, v in fila["tokens"].items():
                    dia[k] = dia.get(k, 0) + v
    return U, V


def e1(U, V, t, t0):
    flujo = base = 0.0
    for k, u in U[t].items():
        if k == "BNB" or not u:
            continue
        p = V[t].get(k, 0) / u
        u0 = U[t0].get(k, 0)
        flujo += (u - u0) * p
        base += u0 * p
    return flujo, 100 * flujo / base


if __name__ == "__main__":
    U, V = series(json.load(open(sys.argv[1])))
    for f in sys.argv[2:]:
        t = dt.date.fromisoformat(f)
        fl, pct = e1(U, V, t, t - dt.timedelta(days=7))
        print(f"E1 {t} contra {t - dt.timedelta(days=7)}: {pct:+.2f}% ({fl / 1e9:+.2f} mil millones USD)")
