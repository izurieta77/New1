"""Ficha 2-nov-2026 · Reapertura de Binance, día dos: E1 oficial, perfil de la cola y cierres
intermitentes por "replenishes the hot wallet".

Preguntas:
  A. E1 oficial (método F, fila 2-nov 00:00 contra 26-oct 00:00) y proyección de la fila del 3-nov.
  B. Perfil de la cola: flujo por tramo (día uno completo, día dos hasta la fila intradía) y ritmo
     por hora, contra Bitget (sep-2026) y Bybit (feb-2025) a la misma escala de días.
  C. Por token: qué sale el día dos (¿sigue siendo stablecoin?) y el BTC en carteras (E2).
  D. Cierres de retiro por motivo (getNetworkCoinAll): cuántos pares dicen "replenishes the hot
     wallet" y qué implica para las reservas en caliente.
  E. BNB/BTC contra el umbral de P0217.

Uso:
  python3 -I 2026-11-02-reapertura-binance-dia-dos.py              # lee la foto .json
  python3 -I 2026-11-02-reapertura-binance-dia-dos.py --crudo <dir> # rehace la foto desde las APIs
    <dir>/llama/binance-cex.json   (api.llama.fi/protocol/binance-cex)
    <dir>/net/net.json             (binance.com/bapi/capital/v1/public/capital/getNetworkCoinAll)
    <dir>/bn/t24.json              (data-api.binance.vision ticker/24hr)
Solo biblioteca estándar.
"""
import datetime as dt
import json
import os
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTO = os.path.join(AQUI, "2026-11-02-reapertura-binance-datos.json")
FOTO_30 = os.path.join(AQUI, "2026-10-30-hackeos-exchanges-datos.json")
UTC = dt.timezone.utc

FILAS = ["2026-10-25T00:00", "2026-10-26T00:00", "2026-10-27T00:00", "2026-11-01T00:00",
         "2026-11-02T00:00", "2026-11-02T14:08"]
REABRE = dt.datetime(2026, 11, 1, 6, tzinfo=UTC)          # inicio de la fase uno (Update #4)
FIN_D1 = dt.datetime(2026, 11, 2, 0, tzinfo=UTC)
INTRA = dt.datetime(2026, 11, 2, 14, 8, 59, tzinfo=UTC)    # fila intradía de DefiLlama
P0217_BASE = 0.0092134                                     # BNB/BTC, vela 19:00 UTC del 29-oct
# Observaciones de getNetworkCoinAll (A) en las bitácoras del 1 y 2-nov y esta corrida.
PARES = [("2026-11-01T14:20", 15, None), ("2026-11-02T03:02", 15, 31), ("2026-11-02T06:24", 14, 30),
         ("2026-11-02T10:20", 14, 30), ("2026-11-02T11:43", 14, 30), ("2026-11-02T13:16", 14, 29),
         ("2026-11-02T15:23", 14, 30)]


def construir(crudo):
    d = json.load(open(os.path.join(crudo, "llama", "binance-cex.json")))
    filas = {f: {} for f in FILAS}
    for cadena, o in d["chainTvls"].items():
        if cadena == "OwnTokens":   # agregado que repite el BNB de Binance-OwnTokens y Op_Bnb-OwnTokens
            continue
        U = {f["date"]: f["tokens"] for f in o.get("tokens") or []}
        V = {f["date"]: f["tokens"] for f in o.get("tokensInUsd") or []}
        for t in U:
            k = dt.datetime.fromtimestamp(t, UTC).strftime("%Y-%m-%dT%H:%M")
            if k not in filas:
                continue
            for tok, u in U[t].items():
                a = filas[k].setdefault(tok, [0.0, 0.0])
                a[0] += u
                a[1] += (V.get(t) or {}).get(tok, 0.0)
    for k in filas:
        filas[k] = {t: [round(u, 5), round(v, 2)] for t, (u, v) in filas[k].items() if u or v}
    # Ranking histórico de E1 (todas las filas de 00:00 desde el 1-nov-2022, ventanas de 7 días solapadas)
    Ud, Vd = {}, {}
    for o in d["chainTvls"].values():
        for clave, DD in (("tokens", Ud), ("tokensInUsd", Vd)):
            for fila in o.get(clave) or []:
                t = dt.datetime.fromtimestamp(fila["date"], UTC)
                if t.hour or t.minute:
                    continue
                dia = DD.setdefault(t.date(), {})
                for k, v in fila["tokens"].items():
                    dia[k] = dia.get(k, 0) + v
    rk = []
    for t in sorted(Ud):
        t0 = t - dt.timedelta(days=7)
        if t < dt.date(2022, 11, 1) or t0 not in Ud or t not in Vd:
            continue
        fl = base = 0.0
        for k, u in Ud[t].items():
            if k == "BNB" or not u:
                continue
            pr = Vd[t].get(k, 0) / u
            fl += (u - Ud[t0].get(k, 0)) * pr
            base += Ud[t0].get(k, 0) * pr
        if base:
            rk.append((round(100 * fl / base, 3), t.isoformat()))
    rk.sort()
    net = json.load(open(os.path.join(crudo, "net", "net.json")))["data"]
    motivos, abiertos, pares = Counter(), set(), []
    for c in net:
        for n in c["networkList"]:
            if n.get("withdrawEnable"):
                abiertos.add(c["coin"])
                pares.append(c["coin"] + "/" + n["network"])
            else:
                motivos[(n.get("withdrawDesc") or "(sin texto)")[:80]] += 1
    hot = sorted(c["coin"] + "/" + n["network"] for c in net for n in c["networkList"]
                 if not n.get("withdrawEnable") and c["coin"] in abiertos
                 and "replenishes the hot wallet" in (n.get("withdrawDesc") or ""))
    t24 = {x["symbol"]: float(x["lastPrice"]) for x in json.load(open(os.path.join(crudo, "bn", "t24.json")))}
    foto = {"llama": filas, "ranking_e1": {"n": len(rk), "peores": rk[:10]}, "red": {"activos": len(net), "con_retiro": sorted(abiertos), "pares": sorted(pares),
                                     "motivos_cierre": dict(motivos.most_common()),
                                     "hot_en_activos_abiertos": hot, "consulta": "2026-11-02T15:23:53Z"},
            "precios": {"BNBBTC": t24["BNBBTC"], "BTCUSDT": t24["BTCUSDT"], "consulta": "2026-11-02T15:23:54Z"},
            "fuentes": {"llama": "api.llama.fi/protocol/binance-cex 15:23 UTC (C)",
                        "red": "getNetworkCoinAll 15:23 UTC (A)", "precios": "data-api.binance.vision (A)"}}
    json.dump(foto, open(FOTO, "w"), ensure_ascii=False, indent=0, sort_keys=True)
    print("foto escrita:", FOTO)


def flujo(L, t, t0, sin=("BNB",)):
    """Método F: Σ (u_t − u_t0) × p_t, sin el token propio; % de Σ u_t0 × p_t."""
    fl = base = 0.0
    por = {}
    for k, (u, v) in L[t].items():
        if k in sin or not u:
            continue
        p = v / u
        u0 = L[t0].get(k, [0, 0])[0]
        fl += (u - u0) * p
        base += u0 * p
        por[k] = (u - u0) * p
    return fl, 100 * fl / base, por


def parte_a(L):
    print("A. E1 oficial (método F)")
    fe, pe, _ = flujo(L, "2026-11-02T00:00", "2026-10-26T00:00")
    print(f"  Fila 2-nov 00:00 contra 26-oct 00:00: {pe:+.2f}% ({fe / 1e9:+.2f} mil M)  → "
          f"{'ROJA' if pe < -5.3 else 'ÁMBAR' if pe < -2.1 else 'VERDE'}")
    fp, pp, _ = flujo(L, "2026-11-02T14:08", "2026-10-27T00:00")
    print(f"  Proyección fila 3-nov si no saliera nada más (14:08 contra 27-oct 00:00): {pp:+.2f}% "
          f"({fp / 1e9:+.2f} mil M)")
    return {"e1": pe, "e1_usd": fe, "e1_proy": pp}


def parte_a2(rk):
    pos = [i for i, (_, t) in enumerate(rk["peores"]) if t == "2026-11-02"][0] + 1
    print(f"  Ranking: fila 2-nov = n.º {pos} de {rk['n']} ventanas desde nov-2022; peores: "
          + ", ".join(f"{t} {x:+.2f}%" for x, t in rk["peores"][:8]))
    return pos


def parte_b(L, ex):
    print("B. Perfil de la cola, sin token propio")
    h1 = (FIN_D1 - REABRE).total_seconds() / 3600
    h2 = (INTRA - FIN_D1).total_seconds() / 3600
    f1, p1, por1 = flujo(L, "2026-11-02T00:00", "2026-11-01T00:00")
    f2, p2, por2 = flujo(L, "2026-11-02T14:08", "2026-11-02T00:00")
    print(f"  Binance día uno (06:00→24:00, {h1:.0f} h): {f1 / 1e9:+.2f} mil M ({p1:+.2f}%), {p1 / h1:+.3f}%/h")
    print(f"  Binance día dos (00:00→14:09, {h2:.2f} h): {f2 / 1e9:+.2f} mil M ({p2:+.2f}%), {p2 / h2:+.3f}%/h")
    print(f"  Razón de ritmos día dos / día uno: {(p2 / h2) / (p1 / h1):.2f}")
    out = {"d1": (f1, p1, p1 / h1), "d2": (f2, p2, p2 / h2), "por1": por1, "por2": por2, "h": (h1, h2)}
    # Bitget: BTC abrió el 28-sep 08:00; fila 29-sep = día uno (16 h); 30-sep y 1-oct = días dos y tres.
    bg = ex["bitget"]
    dias = ["2026-09-28", "2026-09-29", "2026-09-30", "2026-10-01", "2026-10-02", "2026-10-05"]
    serie = [flujo(bg, dias[i + 1], dias[i], sin=("BGB", "BWB"))[1] for i in range(4)]
    tot = sum(serie[:3])
    print("  Bitget por día (%): " + ", ".join(f"{x:+.2f}" for x in serie)
          + f"; día uno = {100 * serie[0] / tot:.0f}% del neto de 3 días")
    f3, p3, _ = flujo(bg, "2026-10-01", "2026-09-28", sin=("BGB", "BWB"))
    print(f"  Bitget 3 días (28-sep → 1-oct): {p3:+.2f}%")
    out["bitget3"] = p3
    out["bitget"] = serie
    # Bybit: hackeo 21-feb-2025 ≈14:00 UTC, retiros nunca se pausaron. Fila 22-feb = ≈10 h; 23 y 24.
    by = ex["bybit"]
    d = ["2025-02-21", "2025-02-22", "2025-02-23", "2025-02-24", "2025-02-25"]
    sb = [flujo(by, d[i + 1], d[i], sin=("MNT", "BIT"))[1] for i in range(4)]
    print("  Bybit por día (%): " + ", ".join(f"{x:+.2f}" for x in sb))
    _, p2b, _ = flujo(by, "2025-02-23", "2025-02-21", sin=("MNT", "BIT"))
    print(f"  Bybit 2 días (21-feb → 23-feb): {p2b:+.2f}%")
    out["bybit2"] = p2b
    print(f"  Bybit sin el robo (1.46 mil M en la fila del 22-feb): día uno ≈ {sb[0] + 100 * 1.46 / 16.20:+.2f}%")
    out["bybit"] = sb
    return out


def parte_c(L, b):
    print("C. Por token (mil M USD) y BTC en carteras")
    for nom, por in (("día uno", b["por1"]), ("día dos", b["por2"])):
        top = sorted(por.items(), key=lambda x: x[1])[:5]
        st = sum(v for k, v in por.items() if k.startswith("USD") or k in ("FDUSD", "DAI", "TUSD"))
        tot = sum(por.values())
        print(f"  {nom}: " + ", ".join(f"{k} {v / 1e9:+.2f}" for k, v in top)
              + f"; stablecoins {100 * st / tot:.0f}% del neto")
        b["stable_" + nom] = st / tot
    btc = {k: L[k]["BTC"][0] for k in FILAS}
    for k in FILAS:
        print(f"  BTC {k}: {btc[k]:,.0f}")
    d26 = 100 * (btc["2026-11-02T14:08"] / btc["2026-10-26T00:00"] - 1)
    d27 = 100 * (btc["2026-11-02T00:00"] / btc["2026-10-26T00:00"] - 1)
    print(f"  E2 BTC 7 días: fila 2-nov {d27:+.2f}%; 14:08 contra 26-oct {d26:+.2f}% (ÁMBAR < −5%)")
    tot = sum(v for _, v in L["2026-11-02T14:08"].values())
    bnb = L["2026-11-02T14:08"]["BNB"][1]
    print(f"  E2 BNB sobre lo rastreado (14:08, sin duplicar OwnTokens): {100 * bnb / tot:.1f}%")
    return {"btc": btc, "e2_btc": d27, "e2_btc_intra": d26, "bnb_pct": 100 * bnb / tot}


def parte_d(red):
    print("D. Cierres por motivo (getNetworkCoinAll, 15:23 UTC)")
    m = red["motivos_cierre"]
    for k, v in sorted(m.items(), key=lambda x: -x[1])[:6]:
        print(f"  {v:4d}  {k}")
    hot = red["hot_en_activos_abiertos"]
    print(f"  Activos con retiro {len(red['con_retiro'])}/{red['activos']}, pares {len(red['pares'])}; "
          f"en esos activos, {len(hot)} redes cerradas por 'hot wallet': {', '.join(hot)}")
    print("  Pares abiertos en el tiempo: " + "; ".join(f"{t[11:]} {a}/{p}" for t, a, p in PARES))
    return {"hot": hot, "n_hot": sum(v for k, v in m.items() if "replenishes the hot" in k)}


def parte_e(pr):
    r = pr["BNBBTC"]
    print(f"E. BNB/BTC {r:.6f}: {100 * (r / P0217_BASE - 1):+.2f}% contra la base de P0217 "
          f"(umbral −3% = {P0217_BASE * 0.97:.7f})")
    return 100 * (r / P0217_BASE - 1)


if __name__ == "__main__":
    if "--crudo" in sys.argv:
        construir(sys.argv[sys.argv.index("--crudo") + 1])
    f = json.load(open(FOTO))
    L = f["llama"]
    a = parte_a(L)
    pos = parte_a2(f["ranking_e1"])
    b = parte_b(L, json.load(open(FOTO_30)))
    c = parte_c(L, b)
    d = parte_d(f["red"])
    e = parte_e(f["precios"])
    # Comprobaciones que sostienen el texto de la ficha
    assert abs(a["e1"] - (-8.78)) < 0.01                 # E1 oficial coincide con la réplica de arbitraje
    assert a["e1"] < -5.3                                 # ROJA
    assert all(t.startswith("2022-12") for _, t in f["ranking_e1"]["peores"][:pos - 1])  # solo dic-2022 es peor
    assert a["e1_proy"] < a["e1"]                         # la fila del 3-nov sale más honda si no entra nada
    assert b["d1"][1] < b["d2"][1] < 0                    # sigue saliendo el día dos, pero menos
    assert b["d2"][2] > b["d1"][2]                        # y más lento por hora (menos negativo)
    assert b["bitget"][0] < b["bitget"][1]                # Bitget: el día uno fue el peor
    assert b["bybit"][1] < b["bybit"][0]                  # Bybit (sin pausa): el día dos fue peor que el uno
    assert c["btc"]["2026-11-02T14:08"] < c["btc"]["2026-11-02T00:00"] < c["btc"]["2026-11-01T00:00"]
    assert d["n_hot"] > 300 and "BTC/BTC" in f["red"]["pares"] and "USDT/TRX" in f["red"]["pares"]
    assert -3 < e < 0                                     # P0217 no se cumple todavía
    print("OK: todas las comprobaciones pasan")
