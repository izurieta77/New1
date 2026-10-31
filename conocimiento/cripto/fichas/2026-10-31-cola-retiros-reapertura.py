"""Ficha 2026-10-31 · La cola de retiros y el precio al reabrir (Bitget 2026, Bybit 2025) y la ruta
Lightning/SPEI a Bitso para un saldo chico.

Preguntas que comprueba (solo biblioteca estándar):
  A. ¿Se abre un descuento del BTC dentro del exchange pausado frente al mercado externo?
     Bitget BTCUSDT contra Binance BTCUSDT, velas de 1 h: antes, durante la pausa y tras reabrir.
  B. ¿Dónde se ve el estrés? En el token propio: BGB/BTC (Bitget) y BNB/BTC (Binance hoy).
  C. Perfil de la cola: flujo diario (método F, DefiLlama, sin token propio) de Bitget y Bybit,
     y qué fracción de la salida de 3 días ocurre el primer día de retiros abiertos.
  D. Aritmética de la ruta para nuestros saldos: Lightning, red BTC o vender + SPEI.

Uso:
    python3 -I 2026-10-31-cola-retiros-reapertura.py               # usa la foto JSON de al lado
    python3 -I 2026-10-31-cola-retiros-reapertura.py --crudo <dir> # rehace la foto de velas desde
        <dir>/bitget-{BTCUSDT,BGBUSDT}-{a,b}.json  (api.bitget.com /api/v2/spot/market/history-candles,
        granularity=1h, endTime 6-oct-2026 y 200 h antes) y <dir>/binance-{BTCUSDT-sep26,BTCUSDT-oct26,
        BNBUSDT-oct26}.json (data-api.binance.vision /api/v3/klines interval=1h).
La parte C lee la foto DefiLlama de la ficha del 30-oct (2026-10-30-hackeos-exchanges-datos.json).
"""
import datetime as dt
import json
import os
import statistics
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTO = os.path.join(AQUI, "2026-10-31-cola-retiros-datos.json")
FOTO_30 = os.path.join(AQUI, "2026-10-30-hackeos-exchanges-datos.json")

H = 3600
# Hora de apertura (UTC) de la vela de 1 h con la mayor caída del token propio = choque público.
CHOQUE_BITGET = dt.datetime(2026, 9, 24, 20, tzinfo=dt.timezone.utc)   # BGB -5.36% en esa vela
REABRE_BITGET = dt.datetime(2026, 9, 28, 8, tzinfo=dt.timezone.utc)    # BTC reabre (B: BleepingComputer)
CHOQUE_BINANCE = dt.datetime(2026, 10, 29, 20, tzinfo=dt.timezone.utc)  # BNB -6.29% en esa vela
CORTE_BINANCE = dt.datetime(2026, 10, 31, 14, tzinfo=dt.timezone.utc)  # última vela usada (abre 14:00)

# Foto del 31-oct-2026, 14:20-14:22 UTC (fuentes A como dato; ver la ficha .md):
HOY = {
    "binance_btcusdt": 77487.18,          # data-api.binance.vision ticker/24hr
    "kraken_usdtusd": 0.99885,            # api.kraken.com Ticker USDTUSD (último)
    "deribit_indice": 77345.63,           # Deribit BTC-PERPETUAL estimated_delivery_price
    "binance_btcmxn_bid": 1456220.0,      # bookTicker BTCMXN, 6 muestras idénticas 14:20:39-14:22:23
    "binance_btcmxn_ask": 1457247.0,
    "bitso_btcmxn_bid": 1454960.0,        # api.bitso.com ticker btc_mxn 14:20:19
    "bitso_btcmxn_ask": 1454970.0,
    # getNetworkCoinAll 14:20 UTC (A): parámetros de retiro (hoy cerrados)
    "ln_fee": 0.000001, "ln_min": 0.00002, "ln_max": 0.01,
    "btc_fee": 0.00002, "btc_min": 0.0001,
    "spei_fee": 0.0,
}
SALDOS = {"real_btc": 0.001325, "real_mxn": 3001.83, "papel_btc": 0.002698}
COMISION_SPOT = 0.001   # 0.1% por lado (cripto_binance, tarifa estándar)


def _ts(t):
    return int(t.timestamp())


def foto_desde_crudo(d):
    def bitget(s):
        out = {}
        for p in "ab":
            for r in json.load(open(os.path.join(d, f"bitget-{s}-{p}.json")))["data"]:
                out[str(int(r[0]) // 1000)] = float(r[4])
        return out

    def binance(f):
        return {str(int(r[0]) // 1000): float(r[4]) for r in json.load(open(os.path.join(d, f)))}

    foto = {
        "bitget_BTCUSDT": bitget("BTCUSDT"),
        "bitget_BGBUSDT": bitget("BGBUSDT"),
        "binance_BTCUSDT": {**binance("binance-BTCUSDT-sep26.json"), **binance("binance-BTCUSDT-oct26.json")},
        "binance_BNBUSDT": binance("binance-BNBUSDT-oct26.json"),
    }
    with open(FOTO, "w") as f:
        json.dump(foto, f, separators=(",", ":"), sort_keys=True)
    return foto


def cierre(serie, t):
    """Cierre de la vela que ABRE en t (la clave es la hora de apertura)."""
    return serie[str(_ts(t))]


def pctl(x, q):
    x = sorted(x)
    i = (len(x) - 1) * q
    lo = int(i)
    return x[lo] + (x[min(lo + 1, len(x) - 1)] - x[lo]) * (i - lo)


def parte_a(f):
    print("A. Precio del BTC dentro de Bitget contra Binance (cierres de 1 h, pb = puntos base)")
    bg, bn = f["bitget_BTCUSDT"], f["binance_BTCUSDT"]
    tramos = {
        "antes (5 d previos al choque)": (CHOQUE_BITGET - dt.timedelta(days=5), CHOQUE_BITGET),
        "pausa (choque -> reapertura de BTC)": (CHOQUE_BITGET, REABRE_BITGET),
        "tras reabrir (5 d)": (REABRE_BITGET, REABRE_BITGET + dt.timedelta(days=5)),
    }
    res = {}
    for nom, (a, b) in tramos.items():
        x = [1e4 * (bg[k] / bn[k] - 1) for k in bg if k in bn and _ts(a) <= int(k) < _ts(b)]
        res[nom] = x
        print(f"  {nom:<38} n={len(x):>3}  mediana {statistics.median(x):+5.2f} pb  "
              f"p5 {pctl(x, .05):+5.2f}  p95 {pctl(x, .95):+5.2f}  máx |x| {max(abs(v) for v in x):4.1f} pb")
    p_hoy = HOY["binance_btcusdt"] * HOY["kraken_usdtusd"] / HOY["deribit_indice"] - 1
    mid_bn = (HOY["binance_btcmxn_bid"] + HOY["binance_btcmxn_ask"]) / 2
    mid_bs = (HOY["bitso_btcmxn_bid"] + HOY["bitso_btcmxn_ask"]) / 2
    print(f"  Binance hoy (pausado): BTCUSDT x USDT/USD de Kraken contra el índice de Deribit = {1e4 * p_hoy:+.1f} pb;"
          f" BTCMXN medio contra Bitso = {1e4 * (mid_bn / mid_bs - 1):+.1f} pb")
    return res, p_hoy, mid_bn / mid_bs - 1


def relativo(tok, btc, t0, t):
    return (cierre(tok, t) / cierre(btc, t)) / (cierre(tok, t0) / cierre(btc, t0)) - 1


def parte_b(f):
    print("B. Token propio contra BTC (base: cierre de la vela previa al choque)")
    g, bb = f["bitget_BGBUSDT"], f["bitget_BTCUSDT"]
    t0 = CHOQUE_BITGET - dt.timedelta(hours=1)
    marcas = [("choque +1 h", CHOQUE_BITGET), ("choque +24 h", CHOQUE_BITGET + dt.timedelta(hours=23)),
              ("reapertura de BTC", REABRE_BITGET), ("reapertura +72 h", REABRE_BITGET + dt.timedelta(hours=72)),
              ("reapertura +7 d", REABRE_BITGET + dt.timedelta(days=7))]
    out = {}
    for nom, t in marcas:
        out["BGB " + nom] = relativo(g, bb, t0, t)
        print(f"  BGB/BTC {nom:<20} {100 * out['BGB ' + nom]:+6.2f}%")
    n, nb = f["binance_BNBUSDT"], f["binance_BTCUSDT"]
    t0 = CHOQUE_BINANCE - dt.timedelta(hours=1)
    for nom, t in [("choque +1 h", CHOQUE_BINANCE), ("choque +24 h", CHOQUE_BINANCE + dt.timedelta(hours=23)),
                   ("hoy 14:00 UTC (pausa, ~42 h)", CORTE_BINANCE)]:
        out["BNB " + nom] = relativo(n, nb, t0, t)
        print(f"  BNB/BTC {nom:<28} {100 * out['BNB ' + nom]:+6.2f}%")
    return out


def flujo_dia(dias, t, t0, sin):
    """Método F: Σ (u_t − u_t0) × p_t sin token propio; % de Σ u_t0 × p_t. dias[d][tok] = [unidades, usd]."""
    fl = base = 0.0
    for k, (u, usd) in dias[t].items():
        if k in sin or not u:
            continue
        p = usd / u
        u0 = dias[t0].get(k, [0, 0])[0]
        fl += (u - u0) * p
        base += u0 * p
    return fl, 100 * fl / base


def parte_c():
    print("C. Perfil diario de la cola (DefiLlama, método F, filas de 00:00 UTC; el día d es el flujo de d-1 a d)")
    foto = json.load(open(FOTO_30))
    casos = {
        # exchange: (sin token, robo a restar el día del robo en mil M, día del robo, 1.er día con retiros abiertos)
        "bitget": ({"BGB", "BWB"}, 0.388, "2026-09-25", "2026-09-29"),
        "bybit": ({"MNT", "BIT"}, 1.46, "2025-02-22", "2025-02-22"),
    }
    out = {}
    for ex, (sin, robo, d_robo, d1) in casos.items():
        dias = foto[ex]
        fechas = sorted(dias)
        filas = []
        for a, b in zip(fechas, fechas[1:]):
            fl, pct = flujo_dia(dias, b, a, sin)
            if b == d_robo:
                fl += robo * 1e9
            filas.append((b, fl / 1e9, pct))
        i1 = [r[0] for r in filas].index(d1)
        ventana = filas[i1:i1 + 3]
        sal = [max(0.0, -r[1]) for r in ventana]
        tot = sum(sal)
        print(f"  {ex}: robo de US${robo} mil M sumado de vuelta el {d_robo}; primer día abierto {d1}")
        for b, fl, pct in filas[max(0, i1 - 4):i1 + 6]:
            marca = " <- 1.er día abierto" if b == d1 else (" <- robo" if b == d_robo else "")
            print(f"     {b}  {fl:+6.2f} mil M{marca}")
        rep = ventana and [round(s / tot, 2) if tot else None for s in sal]
        print(f"     salida de los 3 primeros días abiertos: {tot:.2f} mil M; reparto por día {rep}")
        out[ex] = {"filas": filas, "reparto": rep, "salida_3d": tot}
    return out


def parte_d():
    print("D. Ruta para nuestros saldos (parámetros de getNetworkCoinAll, 31-oct 14:20 UTC; hoy cerrados)")
    mid = (HOY["binance_btcmxn_bid"] + HOY["binance_btcmxn_ask"]) / 2
    semi = (HOY["binance_btcmxn_ask"] - HOY["binance_btcmxn_bid"]) / 2 / mid
    out = {}
    for nom, q in (("real", SALDOS["real_btc"]), ("papel", SALDOS["papel_btc"])):
        ln = HOY["ln_fee"] / q
        oc = HOY["btc_fee"] / q
        venta = COMISION_SPOT + semi + HOY["spei_fee"]
        n_fact = int(-(-q // HOY["ln_max"]))
        print(f"  {nom}: {q} BTC ≈ {q * mid:,.0f} MXN. Lightning {100 * ln:.3f}% ({n_fact} factura, máx {HOY['ln_max']} BTC)"
              f" · red BTC {100 * oc:.2f}% · vender en BTCMXN + SPEI ≈ {100 * venta:.3f}% (comisión 0.1% + medio diferencial)"
              f" y es enajenación")
        out[nom] = {"ln": ln, "onchain": oc, "venta_spei": venta, "facturas": n_fact, "mxn": q * mid}
    print(f"  MXN real {SALDOS['real_mxn']:,.2f}: SPEI a CLABE propia, comisión {HOY['spei_fee']} en el endpoint;"
          f" por debajo de 8,000 MXN (tope del SPEI en tiempo real 24/7 de 2017, B)")
    return out


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--crudo":
        foto = foto_desde_crudo(sys.argv[2])
    else:
        foto = json.load(open(FOTO))
    a, p_hoy, p_mxn = parte_a(foto)
    b = parte_b(foto)
    c = parte_c()
    d = parte_d()
    # Comprobaciones que sostienen el texto de la ficha
    pausa = a["pausa (choque -> reapertura de BTC)"]
    assert min(pausa) > -5 and max(pausa) < 10, "apareció un descuento o una prima de más de 5-10 pb"
    assert c["bitget"]["reparto"][0] > 0.5 and c["bybit"]["salida_3d"] > 4
    assert abs(p_hoy) < 0.002 and abs(p_mxn) < 0.003
    assert b["BGB choque +1 h"] < -0.03 and b["BNB choque +1 h"] < -0.03
    assert d["real"]["ln"] < 0.001 < d["real"]["onchain"]
    print("OK: todas las comprobaciones pasan")
