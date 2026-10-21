"""Makarov y Schoar (JFE 2020, "Trading and arbitrage in cryptocurrency markets"),
aplicado al par BTCMXN de Binance: prima contra el precio implícito BTCUSDT x USD/MXN,
su persistencia (vida media), su "beta de presión compradora" (tabla 5 del paper) y
cuánto del diferencial se explica por el rezago del libro en pesos cuando se mueve el
USD/MXN o el BTC (hipótesis de E9).

Datos (públicos, sin clave):
  - velas 1h BTCMXN y BTCUSDT de data-api.binance.vision (campo 8 = número de operaciones);
  - USD/MXN 1h de Yahoo chart v8 (MXN=X; sin fines de semana);
  - foto del libro de Binance BTCMXN y de Bitso btc_mxn (plan B) al correr.
Prima_t = ln(BTCMXN_cierre / (BTCUSDT_cierre * USDMXN_cierre)), solo horas con >= 1
operación en BTCMXN y con barra de USD/MXN. No corrige USDT/USD (~0.9988 en Kraken,
sesgo de ~+0.1 pp en la prima contra el dólar). Uso: python3 -I este_archivo.py
"""
import json, math, urllib.request, datetime as dt, statistics as st
import numpy as np

UA = {"User-Agent": "Mozilla/5.0"}
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))

B = "https://data-api.binance.vision/api/v3/"
DIAS = 90
ahora_ms = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)
ini_ms = ahora_ms - DIAS * 86400 * 1000

def klines(sym):
    out, t = [], ini_ms
    while True:
        k = get(f"{B}klines?symbol={sym}&interval=1h&startTime={t}&limit=1000")
        if not k:
            break
        out += k
        t = k[-1][0] + 3600 * 1000
        if len(k) < 1000:
            break
    return {r[0]: r for r in out if r[6] < ahora_ms}      # solo velas cerradas

mxn, usdt = klines("BTCMXN"), klines("BTCUSDT")
y = get("https://query1.finance.yahoo.com/v8/finance/chart/MXN=X?interval=1h&range=90d")["chart"]["result"][0]
fx = {}
for ts, c in zip(y["timestamp"], y["indicators"]["quote"][0]["close"]):
    if c is not None and ts % 3600 == 0:
        fx[ts * 1000] = c

horas = sorted(h for h in mxn if h in usdt and h in fx)
con_op = [h for h in horas if int(mxn[h][8]) > 0]
P = {h: math.log(float(mxn[h][4]) / (float(usdt[h][4]) * fx[h])) for h in con_op}
p = np.array([P[h] for h in con_op]) * 100                     # en %
f0 = dt.datetime.fromtimestamp(con_op[0] / 1000, dt.timezone.utc)
f1 = dt.datetime.fromtimestamp(con_op[-1] / 1000, dt.timezone.utc)
vol_dia = sum(float(mxn[h][5]) for h in mxn) / DIAS
print(f"Muestra: {f0:%Y-%m-%d %H}h a {f1:%Y-%m-%d %H}h UTC; horas con FX: {len(horas)}; con >=1 operación BTCMXN: {len(con_op)} ({len(con_op)/len(horas):.0%})")
print(f"Volumen medio BTCMXN: {vol_dia:.3f} BTC/día")
print(f"Prima (%): media {p.mean():+.3f}, mediana {np.median(p):+.3f}, p5 {np.percentile(p,5):+.3f}, p95 {np.percentile(p,95):+.3f}, de {p.std(ddof=1):.3f}")
print(f"Prima |p| > 0.5%: {np.mean(abs(p)>0.5):.1%}; > 1%: {np.mean(abs(p)>1):.1%}; p > 0: {np.mean(p>0):.1%}")
# segundo método: media de las primas simples (no log)
p_simple = np.array([float(mxn[h][4]) / (float(usdt[h][4]) * fx[h]) - 1 for h in con_op]) * 100
print(f"Comprobación (prima simple): media {p_simple.mean():+.3f}, mediana {np.median(p_simple):+.3f}")

# Persistencia: AR(1) en pares de horas consecutivas, ambas con operación
pares = [(P[h] * 100, P[h + 3600000] * 100) for h in con_op if (h + 3600000) in P]
x0 = np.array([a for a, _ in pares]); x1 = np.array([b for _, b in pares])
X = np.column_stack([np.ones_like(x0), x0]); rho = np.linalg.lstsq(X, x1, rcond=None)[0][1]
vida = math.log(0.5) / math.log(rho) if 0 < rho < 1 else float("nan")
print(f"AR(1) horario (n={len(pares)}): rho = {rho:.3f}; vida media = {vida:.1f} h")

# Rezago del libro en pesos: cambio de prima contra cambio del USD/MXN y del BTCUSDT
# en horas consecutivas con operación. Si el libro MXN no se mueve, beta_fx ~ -1, beta_btc ~ -1.
d = [(P[h + 3600000] * 100 - P[h] * 100,
      math.log(fx[h + 3600000] / fx[h]) * 100,
      math.log(float(usdt[h + 3600000][4]) / float(usdt[h][4])) * 100) for h in con_op if (h + 3600000) in P]
D = np.array(d)
Xr = np.column_stack([np.ones(len(D)), D[:, 1], D[:, 2]])
b, res, *_ = np.linalg.lstsq(Xr, D[:, 0], rcond=None)
e = D[:, 0] - Xr @ b
cov = np.linalg.inv(Xr.T @ Xr) * (e @ e) / (len(D) - 3)
t = b / np.sqrt(np.diag(cov))
r2 = 1 - (e @ e) / ((D[:, 0] - D[:, 0].mean()) @ (D[:, 0] - D[:, 0].mean()))
print(f"dPrima = a + b_fx dFX + b_btc dBTC (n={len(D)}): b_fx {b[1]:+.2f} (t {t[1]:.1f}), b_btc {b[2]:+.2f} (t {t[2]:.1f}), R2 {r2:.2f}")

# "Beta de presión compradora" estilo tabla 5 (prima diaria media contra rendimiento de 7 días de BTCUSDT;
# el paper usa la desviación del log precio de EUA contra su tendencia Hodrick-Prescott semanal)
dia = {}
for h in con_op:
    dia.setdefault(h // 86400000, []).append(P[h] * 100)
dk = get(f"{B}klines?symbol=BTCUSDT&interval=1d&limit={DIAS + 10}")
cd = {r[0] // 86400000: float(r[4]) for r in dk if r[6] < ahora_ms}
xs, ys = [], []
for dd, v in sorted(dia.items()):
    if dd - 1 in cd and dd - 8 in cd:
        xs.append(math.log(cd[dd - 1] / cd[dd - 8]) * 100); ys.append(st.fmean(v))
xs, ys = np.array(xs), np.array(ys)
bb = np.polyfit(xs, ys, 1)
print(f"Beta de presión (n={len(xs)} días): pendiente {bb[0]:+.4f} pp de prima por pp de rendimiento a 7 días; corr {np.corrcoef(xs, ys)[0,1]:+.2f}")
print("Paper, tabla 5 (ene-2017 a abr-2018, Bitso): prima MXN 0.027, beta 0.078; KRW 0.066 y 0.22")

# Foto del libro: Binance BTCMXN contra Bitso btc_mxn, ambos contra el implícito
px = float(get(B + "ticker/price?symbol=BTCUSDT")["price"])
fxv = get("https://query1.finance.yahoo.com/v8/finance/chart/MXN=X?interval=1m&range=1d")["chart"]["result"][0]["meta"]["regularMarketPrice"]
imp = px * fxv
bn = get(B + "depth?symbol=BTCMXN&limit=100")
bs = get("https://api.bitso.com/v3/order_book/?book=btc_mxn&aggregate=true")["payload"]
def foto(nombre, bid, ask, bids):
    prof = sum(pp * q for pp, q in bids if pp >= imp * 0.995)
    print(f"{nombre}: compra {bid:,.0f} ({(bid/imp-1)*100:+.2f}% del implícito), venta {ask:,.0f} ({(ask/imp-1)*100:+.2f}%), "
          f"diferencial {(ask-bid)/((ask+bid)/2)*100:.3f}%, compra a -0.5% del implícito {prof:,.0f} MXN")
print(f"Implícito: {px:,.2f} x {fxv:.4f} = {imp:,.0f} MXN")
foto("Binance BTCMXN", float(bn["bids"][0][0]), float(bn["asks"][0][0]), [(float(a), float(c)) for a, c in bn["bids"]])
foto("Bitso btc_mxn ", float(bs["bids"][0]["price"]), float(bs["asks"][0]["price"]), [(float(r["price"]), float(r["amount"])) for r in bs["bids"]])

# Costo de salida de la cuenta (0.001325 BTC) en Binance BTCMXN: venta a mercado contra el implícito
q, cobro = 0.001325, 0.0
for pp, qq in [(float(a), float(c)) for a, c in bn["bids"]]:
    t_ = min(q, qq); cobro += t_ * pp; q -= t_
    if q <= 1e-12:
        break
print(f"Venta a mercado de 0.001325 BTC: {cobro:,.0f} MXN contra {0.001325*imp:,.0f} implícito ({(cobro/(0.001325*imp)-1)*100:+.2f}%; + comisión 0.1%)")
