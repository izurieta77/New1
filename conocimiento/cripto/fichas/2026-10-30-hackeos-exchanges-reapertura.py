"""Ficha 2026-10-30 · Hackeos de exchanges: tiempo hasta reabrir retiros, fuga de clientes y recuperación.

Tres partes (solo biblioteca estándar):
  A. Tasas base de días hasta la primera reapertura de retiros y de recuperación del cliente,
     con la tabla de casos de abajo (fechas y grado de fuente en la ficha .md).
  B. Flujo neto por día y a 7 días (método F de lista-senales-de-alerta.md: unidades × precio del día,
     sin token propio, solo filas de 00:00 UTC) alrededor de los hackeos de Bybit (feb-2025),
     Bitget (sep-2026) y Binance (oct-2026), con datos de DefiLlama.
  C. Pérdida contra reservas rastreadas y lectura para O0007 y para el pronóstico del día.

Uso:
    python3 -I 2026-10-30-hackeos-exchanges-reapertura.py               # usa la foto JSON de al lado
    python3 -I 2026-10-30-hackeos-exchanges-reapertura.py --crudo <dir> # rehace la foto desde
        <dir>/bybit.json, <dir>/bitget.json y <dir>/binance-cex.json, bajados aparte con
        curl -sS -o <dir>/<x>.json https://api.llama.fi/protocol/<x>   (x = bybit, bitget, binance-cex)
"""
import datetime as dt
import json
import os
import statistics
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTO = os.path.join(AQUI, "2026-10-30-hackeos-exchanges-datos.json")

# ---------------------------------------------------------------- A. casos
# dias = días naturales del hackeo (o de la pausa) a la PRIMERA reapertura de retiros de cripto o fiat.
# None = nunca reabrió como empresa en marcha. pausa=False: nunca suspendió retiros.
# recup = fracción nominal que recuperó el cliente (en la unidad del pasivo); meses = hasta cobrar.
CASOS = [
    # nombre,           fecha,        perdida_musd, pausa, dias, solvente, recup, meses_cobro, grado
    ("Mt.Gox",          "2014-02-07", 470,  True,  None, False, 0.20, 125, "B fechas; C recup"),
    ("Bitfinex",        "2016-08-02", 72,   True,  8,    True,  1.00, 8,   "B"),
    ("Coincheck",       "2018-01-26", 530,  True,  18,   True,  1.00, 1.5, "B (yen 13-feb; BTC 12-mar)"),
    ("Binance 2019",    "2019-05-07", 40,   True,  8,    True,  1.00, 0,   "B"),
    ("KuCoin",          "2020-09-26", 281,  True,  7,    True,  1.00, 0,   "C (rango 4-11 d)"),
    ("CoinEx",          "2023-09-12", 70,   True,  9,    True,  1.00, 0,   "B"),
    ("Poloniex",        "2023-11-10", 120,  True,  20,   True,  1.00, 0,   "C (gradual 29/30-nov)"),
    ("DMM Bitcoin",     "2024-05-31", 305,  True,  281,  False, 1.00, 9,   "B (traspaso a SBI 8-mar-2025)"),
    ("WazirX",          "2024-07-18", 235,  True,  463,  False, 0.85, 15,  "C (recup. disputada 55-85%)"),
    ("Bybit",           "2025-02-21", 1460, False, 0,    True,  1.00, 0,   "B"),
    ("Bitget",          "2026-09-24", 388,  True,  4,    True,  1.00, 0,   "B (BTC 28-sep 08:00; fiat 2-oct)"),
]
CONTROL_FRAUDE = ("FTX", "2022-11-08", True, None, 1.19, 30, "B (119% en USD a precio de la petición)")


def parte_a():
    print("A. Tasas base de reapertura y recuperación")
    pausados_solv = [c for c in CASOS if c[3] and c[5]]
    d_solv = sorted(c[4] for c in pausados_solv)
    print(f"  Pausaron y eran solventes (n={len(d_solv)}): días {d_solv}; mediana {statistics.median(d_solv)}")
    for h in (1, 2, 4, 7.5, 8, 14, 21):
        k = sum(1 for d in d_solv if d <= h)
        print(f"    reabrió en <= {h:>4} d: {k}/{len(d_solv)} = {k / len(d_solv):.2f}")
    todos = [c[4] if c[4] is not None else float("inf") for c in CASOS if c[3]]
    todos.sort()
    print(f"  Todos los que pausaron (n={len(todos)}), incl. insolventes: mediana "
          f"{statistics.median(todos)} d; nunca reabrieron {sum(1 for x in todos if x == float('inf'))}")
    solv = [c for c in CASOS if c[5]]
    ins = [c for c in CASOS if not c[5]]
    print(f"  Recuperación nominal: solventes {sum(c[6] for c in solv) / len(solv):.2f} (n={len(solv)}); "
          f"insolventes/liquidados {statistics.mean(c[6] for c in ins):.2f} (n={len(ins)}), "
          f"meses hasta cobrar {[c[7] for c in ins]}")
    return d_solv


# ---------------------------------------------------------------- B. flujos DefiLlama
VENTANAS = {
    "bybit": ("2025-02-14", "2025-03-05"),
    "bitget": ("2026-09-16", "2026-10-09"),
    "binance-cex": ("2026-10-16", "2026-10-30"),
}
SIN_TOKEN = {"binance-cex": {"BNB"}, "bybit": {"MNT", "BIT"}, "bitget": {"BGB", "BWB"}}


def foto_desde_crudo(dirc):
    foto = {}
    for ex, (a, b) in VENTANAS.items():
        d = json.load(open(os.path.join(dirc, ex + ".json")))
        a, b = dt.date.fromisoformat(a), dt.date.fromisoformat(b)
        U, V = {}, {}
        for k, o in d["chainTvls"].items():
            if "OwnTokens" in k or k in ("staking", "pool2", "borrowed"):
                continue
            for clave, D in (("tokens", U), ("tokensInUsd", V)):
                for f in o.get(clave) or []:
                    t = dt.datetime.fromtimestamp(f["date"], dt.timezone.utc)
                    if t.hour or t.minute or not (a <= t.date() <= b):
                        continue
                    dia = D.setdefault(t.date().isoformat(), {})
                    for kk, v in f["tokens"].items():
                        if kk in SIN_TOKEN[ex]:
                            continue
                        dia[kk] = dia.get(kk, 0) + v
        foto[ex] = {dia: {k: [round(U[dia][k], 6), round(V[dia].get(k, 0), 2)]
                          for k in U[dia] if U[dia][k] and V[dia].get(k, 0) >= 1e5}
                    for dia in sorted(U) if dia in V}
    json.dump(foto, open(FOTO, "w"), separators=(",", ":"))
    return foto


def flujo(F, t, t0):
    fl = base = 0.0
    for k, (u, usd) in F[t].items():
        p = usd / u
        u0 = F[t0].get(k, [0, 0])[0]
        fl += (u - u0) * p
        base += u0 * p
    return fl, 100 * fl / base


def parte_b(foto):
    print("\nB. Flujo neto (método F, sin token propio; millones de USD)")
    res = {}
    for ex, F in foto.items():
        dias = sorted(F)
        print(f"  {ex}")
        res[ex] = {}
        for i, t in enumerate(dias):
            if i == 0:
                continue
            f1, p1 = flujo(F, t, dias[i - 1])
            t7 = (dt.date.fromisoformat(t) - dt.timedelta(days=7)).isoformat()
            s7 = f"{flujo(F, t, t7)[1]:+6.2f}%" if t7 in F else "   n/d"
            tot = sum(v[1] for v in F[t].values())
            res[ex][t] = (f1, p1, tot)
            print(f"    {t}  total {tot / 1e9:7.2f} mil M  1d {f1 / 1e6:+8.0f} ({p1:+6.2f}%)  7d {s7}")
    return res


def parte_c(foto, res, d_solv):
    print("\nC. Pérdida contra reservas y lectura")
    pre = {"bybit": ("2025-02-21", 1460), "bitget": ("2026-09-24", 388), "binance-cex": ("2026-10-29", 6300)}
    for ex, (dia, perd) in pre.items():
        tot = sum(v[1] for v in foto[ex][dia].values())
        print(f"  {ex}: pérdida {perd} M / reservas sin token propio del {dia} {tot / 1e9:.2f} mil M = {100 * perd * 1e6 / tot:.1f}%")
    # fuga de clientes tras reabrir (o sin pausa), sin el robo
    by = res["bybit"]
    fuga_by = by["2025-02-22"][0] + by["2025-02-23"][0] + 1460e6
    base_by = by["2025-02-21"][2]
    print(f"  Bybit (sin pausa): salida neta 22+23-feb sin el robo {fuga_by / 1e6:+.0f} M = {100 * fuga_by / base_by:+.1f}% de las reservas del 21-feb")
    bg = res["bitget"]
    fuga_bg = sum(bg[d][0] for d in ("2026-09-29", "2026-09-30", "2026-10-01"))
    base_bg = bg["2026-09-28"][2]
    print(f"  Bitget (reabre BTC 28-sep 08:00): salida 29-sep a 1-oct {fuga_bg / 1e6:+.0f} M = {100 * fuga_bg / base_bg:+.1f}%; "
          f"reposición 2-oct {bg['2026-10-02'][0] / 1e6:+.0f} M")
    bg_pausa = sum(bg[d][0] for d in ("2026-09-26", "2026-09-27", "2026-09-28"))
    print(f"  Bitget durante la pausa (26-28-sep): {bg_pausa / 1e6:+.0f} M (con retiros cerrados no hay corrida que medir)")
    bn = res["binance-cex"]
    print(f"  Binance 30-oct (fila 00:00 UTC, hackeo 20:20 UTC del 29): 1d {bn['2026-10-30'][0] / 1e9:+.2f} mil M; "
          f"sin el robo estimado (6.3 mil M, C): {(bn['2026-10-30'][0] + 6.3e9) / 1e9:+.2f} mil M")
    F = foto["binance-cex"]
    t, t0 = "2026-10-30", "2026-10-29"
    contrib = []
    for k, (u, usd) in F[t].items():
        u0 = F[t0].get(k, [0, 0])[0]
        contrib.append(((u - u0) * usd / u, k, u - u0))
    contrib.sort()
    print("  Binance, mayores salidas por token 29→30-oct:",
          "; ".join(f"{k} {f / 1e9:+.2f} mil M ({du:+,.0f} u)" for f, k, du in contrib[:5]))
    # Lectura para el disparador de 24 h y para P0204
    n = len(d_solv)
    pausados = [d for d in d_solv if d > 0]
    print(f"  De {len(pausados)} solventes que sí pausaron, {sum(1 for d in pausados if d > 1)} tardaron más de 1 día "
          f"y {sum(1 for d in pausados if d <= 2)} reabrieron en <= 2 días (la guía de 48 h de Yi He no tiene precedente).")
    return n


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--crudo":
        foto = foto_desde_crudo(sys.argv[2])
    else:
        foto = json.load(open(FOTO))
    d_solv = parte_a()
    res = parte_b(foto)
    parte_c(foto, res, d_solv)
