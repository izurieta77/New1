"""Ficha 2026-11-01 · Reapertura de Binance, día uno: velocidad de salida, BNB/BTC y precio interno.

Sigue los pasos (a) y (b) de la ficha 2026-10-31-cola-retiros-reapertura.md con los datos del día de la
reapertura por fases (Recovery Update #4, fase uno entre 06:00 y 09:00 UTC del 1-nov-2026).

  A. Calendario de la reapertura: activos con retiro abierto en getNetworkCoinAll (990 activos) y horas de
     pausa hasta el primer BTC, contra Bitget (sep-2026).
  B. Velocidad de salida (método F, DefiLlama, sin BNB): la fila intradía de las 13:29 UTC del 1-nov contra
     la de 00:00 UTC (≈7.5 h de reapertura), contra el primer día de Bitget. E1 formal (00:00 contra 00:00
     de t−7) y lo que marcaría la fila del 2-nov si no hubiera más flujo. E2 (BNB sobre lo rastreado).
  C. BNB/BTC por hora desde el choque, contra el umbral de P0217 (0.97 × razón previa).
  D. Precio interno: Binance BTCUSDT × USDT/USD de Kraken contra Coinbase BTC-USD (cierres de 1 h), antes,
     durante la pausa y tras reabrir.

Uso:
    python3 -I 2026-11-01-reapertura-binance-dia-uno.py              # lee la foto *-datos.json
    python3 -I 2026-11-01-reapertura-binance-dia-uno.py --crudo DIR  # rehace la foto desde los JSON crudos
Crudos en DIR: llama.json (api.llama.fi/protocol/binance-cex), btc1h.json y bnb1h.json (data-api.binance.vision
klines 1h), cb1h.json (api.exchange.coinbase.com candles 3600), krk1h.json (api.kraken.com OHLC USDTUSD 60).
Solo biblioteca estándar.
"""
import datetime as dt
import json
import os
import statistics as st
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTO = os.path.join(AQUI, "2026-11-01-reapertura-binance-datos.json")
FOTO_30 = os.path.join(AQUI, "2026-10-30-hackeos-exchanges-datos.json")
UTC = dt.timezone.utc

FILAS_LLAMA = ["2026-10-25T00:00", "2026-10-26T00:00", "2026-10-29T00:00", "2026-10-30T00:00",
               "2026-10-31T00:00", "2026-11-01T00:00", "2026-11-01T13:29"]
PREVIA = dt.datetime(2026, 10, 29, 19, tzinfo=UTC)    # última vela de 1 h antes del choque (P0217)
CHOQUE = dt.datetime(2026, 10, 29, 20, tzinfo=UTC)    # vela con la mayor caída de BNB (inferido, ficha 31-oct)
REABRE = dt.datetime(2026, 11, 1, 6, tzinfo=UTC)      # inicio de la ventana de la fase uno (Update #4)
CORTE = dt.datetime(2026, 11, 1, 14, tzinfo=UTC)      # primera vela no completa a la hora de la consulta
DESDE = dt.datetime(2026, 10, 27, tzinfo=UTC)

# Observaciones de getNetworkCoinAll (A): bitácoras de cripto del 31-oct y 1-nov, y esta corrida.
REAPERTURA = [("2026-10-31T14:20", 0), ("2026-11-01T02:59", 0), ("2026-11-01T06:18", 1),
              ("2026-11-01T10:19", 7), ("2026-11-01T11:42", 13), ("2026-11-01T13:08", 15),
              ("2026-11-01T14:20", 15)]
# Bitget (B, BleepingComputer y crypto.news, ficha del 30-oct): choque ≈24-sep 20:00 UTC; BTC el 28-sep 08:00.
BITGET_CHOQUE = dt.datetime(2026, 9, 24, 20, tzinfo=UTC)
BITGET_BTC = dt.datetime(2026, 9, 28, 8, tzinfo=UTC)
BINANCE_CHOQUE_ALERTA = dt.datetime(2026, 10, 29, 21, 50, tzinfo=UTC)  # alerta del 30-oct, "≈21:50 UTC"
BINANCE_BTC_VISTO = dt.datetime(2026, 11, 1, 6, 18, tzinfo=UTC)        # primera consulta con BTC abierto


def ts(t):
    return int(t.timestamp())


def construir(crudo):
    d = json.load(open(os.path.join(crudo, "llama.json")))
    filas = {f: {} for f in FILAS_LLAMA}
    for cadena, o in d["chainTvls"].items():
        if cadena == "OwnTokens":   # agregado que repite el BNB de Binance-OwnTokens y Op_Bnb-OwnTokens
            continue
        for clave, i in (("tokens", 0), ("tokensInUsd", 1)):
            for fila in o.get(clave) or []:
                k = dt.datetime.fromtimestamp(fila["date"], UTC).strftime("%Y-%m-%dT%H:%M")
                if k not in filas:
                    continue
                for tok, v in fila["tokens"].items():
                    par = filas[k].setdefault(tok, [0.0, 0.0])
                    par[i] += v
    for k in filas:
        filas[k] = {t: [round(u, 6), round(v, 2)] for t, (u, v) in filas[k].items() if u}

    def kl(nombre):
        return {str(x[0] // 1000): float(x[4]) for x in json.load(open(os.path.join(crudo, nombre)))
                if ts(DESDE) <= x[0] // 1000 < ts(CORTE)}
    cb = {str(x[0]): x[4] for x in json.load(open(os.path.join(crudo, "cb1h.json")))
          if ts(DESDE) <= x[0] < ts(CORTE)}
    kr = {str(x[0]): float(x[4]) for x in json.load(open(os.path.join(crudo, "krk1h.json")))["result"]["USDTZUSD"]
          if ts(DESDE) <= x[0] < ts(CORTE)}
    foto = {"llama": filas, "binance_BTCUSDT": kl("btc1h.json"), "binance_BNBUSDT": kl("bnb1h.json"),
            "coinbase_BTCUSD": cb, "kraken_USDTUSD": kr,
            "nota": "Cierres de velas de 1 h (clave = apertura en segundos UTC), 27-oct 00:00 a 1-nov 13:00 UTC. "
                    "DefiLlama: suma de todas las cadenas salvo el agregado OwnTokens; [unidades, USD]."}
    json.dump(foto, open(FOTO, "w"), separators=(",", ":"))
    print("foto escrita:", FOTO)


def flujo(filas, t, t0, sin=("BNB",)):
    """Método F: Σ (u_t − u_t0) × p_t sin token propio; % de Σ u_t0 × p_t. filas[d][tok] = [unidades, usd]."""
    fl = base = 0.0
    por = {}
    for k, (u, usd) in filas[t].items():
        if k in sin or not u:
            continue
        p = usd / u
        u0 = filas[t0].get(k, [0, 0])[0]
        fl += (u - u0) * p
        base += u0 * p
        por[k] = (u - u0) * p
    return fl, 100 * fl / base, por


def parte_a():
    print("A. Calendario de la reapertura (getNetworkCoinAll, 990 activos)")
    for h, n in REAPERTURA:
        print(f"  {h} UTC  retiros abiertos: {n:>2}/990")
    hb = (BITGET_BTC - BITGET_CHOQUE).total_seconds() / 3600
    hn = (BINANCE_BTC_VISTO - BINANCE_CHOQUE_ALERTA).total_seconds() / 3600
    print(f"  Pausa hasta el primer BTC: Bitget {hb:.0f} h; Binance {hn:.1f} h (cota superior: primera consulta)")
    return {"horas_bitget": hb, "horas_binance": hn}


def parte_b(f):
    print("B. Velocidad de salida (DefiLlama, método F, sin BNB)")
    L = f["llama"]
    out = {}
    fl, pct, por = flujo(L, "2026-11-01T13:29", "2026-11-01T00:00")
    out["intradia"] = (fl, pct)
    horas = (dt.datetime(2026, 11, 1, 13, 29, tzinfo=UTC) - REABRE).total_seconds() / 3600
    print(f"  1-nov 00:00 → 13:29 UTC (≈{horas:.1f} h desde las 06:00): {fl / 1e9:+.2f} mil M USD ({pct:+.2f}%)")
    peores = sorted(por.items(), key=lambda x: x[1])[:5]
    print("   por token (mil M):", ", ".join(f"{k} {v / 1e9:+.2f}" for k, v in peores))
    print(f"   parte de stablecoins (USDT+USDC+USD1+FDUSD): "
          f"{100 * sum(por.get(k, 0) for k in ('USDT', 'USDC', 'USD1', 'FDUSD')) / fl:.0f}%")
    b0, b1 = L["2026-11-01T00:00"]["BTC"][0], L["2026-11-01T13:29"]["BTC"][0]
    print(f"   BTC en carteras: {b0:,.0f} → {b1:,.0f} ({b1 - b0:+,.0f} BTC, {100 * (b1 / b0 - 1):+.2f}%)")
    out["btc"] = (b0, b1)
    fl0, pct0, _ = flujo(L, "2026-11-01T00:00", "2026-10-31T00:00")
    print(f"  Último día de pausa (31-oct → 1-nov 00:00): {fl0 / 1e9:+.3f} mil M ({pct0:+.3f}%)")
    out["pausa"] = pct0
    fe, pe, _ = flujo(L, "2026-11-01T00:00", "2026-10-25T00:00")
    print(f"  E1 formal (1-nov 00:00 contra 25-oct 00:00): {pe:+.2f}% ({fe / 1e9:+.2f} mil M)")
    out["e1_formal"] = pe
    fp, pp, _ = flujo(L, "2026-11-01T13:29", "2026-10-26T00:00")
    print(f"  E1 de mañana si no saliera nada más (13:29 contra 26-oct 00:00): {pp:+.2f}% "
          f"(ÁMBAR < −2.1%, ROJA < −5.3%)")
    out["e1_proyectado"] = pp
    # E2: BNB sobre lo rastreado (BNB ya contado una sola vez: se quitó el agregado OwnTokens)
    for k in ("2026-11-01T00:00", "2026-11-01T13:29"):
        tot = sum(v for _, v in L[k].values())
        bnb = L[k].get("BNB", [0, 0])[1]
        print(f"  E2 {k}: rastreado US${tot / 1e9:.1f} mil M; sin BNB US${(tot - bnb) / 1e9:.1f}; BNB {100 * bnb / tot:.1f}%")
        out["e2_" + k] = 100 * bnb / tot
    # Bitget: primer día con BTC abierto (fila 29-sep = 28-sep 00:00 → 29-sep 00:00; abrió a las 08:00, 16 h)
    bg = json.load(open(FOTO_30))["bitget"]
    flb, pb, _ = flujo(bg, "2026-09-29", "2026-09-28", sin=("BGB", "BWB"))
    print(f"  Bitget, primer día (16 h de reapertura): {flb / 1e9:+.2f} mil M ({pb:+.2f}%)")
    out["bitget_dia1"] = pb
    print(f"  Ritmo por hora de reapertura: Binance {pct / horas:+.3f}%/h; Bitget {pb / 16:+.3f}%/h "
          f"(×{(pct / horas) / (pb / 16):.1f})")
    out["ritmo"] = (pct / horas, pb / 16)
    return out


def parte_c(f):
    print("C. BNB/BTC por hora (base: cierre de la vela de las 19:00 UTC del 29-oct)")
    n, b = f["binance_BNBUSDT"], f["binance_BTCUSDT"]
    r0 = n[str(ts(PREVIA))] / b[str(ts(PREVIA))]
    out = {"r0": r0}
    for nom, t in [("choque +1 h", CHOQUE), ("pausa, 31-oct 00:00", dt.datetime(2026, 10, 31, tzinfo=UTC)),
                   ("vela de las 05:00 (antes de abrir)", dt.datetime(2026, 11, 1, 5, tzinfo=UTC)),
                   ("vela de las 06:00 (abre)", REABRE), ("vela de las 13:00 (última completa)", CORTE - dt.timedelta(hours=1))]:
        r = n[str(ts(t))] / b[str(ts(t))]
        out[nom] = 100 * (r / r0 - 1)
        print(f"  {nom:<36} {r:.7f}  {out[nom]:+6.2f}%")
    minimo = min((n[k] / b[k], k) for k in n if int(k) >= ts(REABRE))
    out["min_tras_abrir"] = 100 * (minimo[0] / r0 - 1)
    print(f"  Mínimo tras abrir: {out['min_tras_abrir']:+.2f}% "
          f"({dt.datetime.fromtimestamp(int(minimo[1]), UTC):%d-%b %H:%M}); umbral P0217 {0.97 * r0:.7f} (−3%)")
    return out


def parte_d(f):
    print("D. Binance BTCUSDT × USDT/USD (Kraken) contra Coinbase BTC-USD, cierres de 1 h, en pb")
    b, cb, kr = f["binance_BTCUSDT"], f["coinbase_BTCUSD"], f["kraken_USDTUSD"]
    def tramo(a, z):
        v = [1e4 * (b[k] * kr[k] / cb[k] - 1) for k in b if ts(a) <= int(k) < ts(z) and k in cb and k in kr]
        return len(v), st.median(v), min(v), max(v)
    out = {}
    for nom, a, z in [("antes del choque (27-oct 00:00 → 29-oct 20:00)", DESDE, CHOQUE),
                      ("pausa (29-oct 20:00 → 1-nov 06:00)", CHOQUE, REABRE),
                      ("reabierto (1-nov 06:00 → 13:00)", REABRE, CORTE)]:
        out[nom] = tramo(a, z)
        n_, med, lo, hi = out[nom]
        print(f"  {nom:<48} n={n_:>2}  mediana {med:+5.1f}  mín {lo:+5.1f}  máx {hi:+5.1f}")
    return out


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--crudo":
        construir(sys.argv[2])
    f = json.load(open(FOTO))
    a = parte_a()
    bb = parte_b(f)
    c = parte_c(f)
    d = parte_d(f)
    # Comprobaciones que sostienen el texto de la ficha
    assert a["horas_binance"] < a["horas_bitget"]                       # Binance reabrió BTC antes que Bitget
    assert abs(bb["pausa"]) < 0.01                                      # sin flujo durante la pausa
    assert bb["intradia"][1] < -2.5                                     # salida de ≈−2.8% en ≈7.5 h
    assert bb["btc"][1] - bb["btc"][0] < -10000                         # más de 10 mil BTC salieron
    assert -5.3 < bb["e1_formal"] < -2.1                                # E1 formal: ÁMBAR
    assert bb["e1_proyectado"] < -5.3                                   # la fila del 2-nov ya marcaría ROJA
    assert bb["ritmo"][1] < bb["ritmo"][0] < 0                          # Binance sale, pero más lento por hora que Bitget (en %)
    assert 15 < bb["e2_2026-11-01T13:29"] < 20                          # E2: BNB < 20%, VERDE
    assert c["vela de las 13:00 (última completa)"] > c["vela de las 06:00 (abre)"]   # BNB/BTC repunta al abrir
    assert c["min_tras_abrir"] > -3                                     # lejos del umbral de P0217
    assert d["pausa (29-oct 20:00 → 1-nov 06:00)"][1] > d["antes del choque (27-oct 00:00 → 29-oct 20:00)"][1]
    assert d["reabierto (1-nov 06:00 → 13:00)"][1] < d["pausa (29-oct 20:00 → 1-nov 06:00)"][1]
    print("OK: todas las comprobaciones pasan")
