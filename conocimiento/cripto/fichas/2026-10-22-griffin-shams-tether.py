"""Griffin y Shams (JF 2020, "Is Bitcoin Really Untethered?"): prueba fuera de muestra,
con datos diarios públicos de jun-2020 a oct-2026, de las dos huellas del "lado de la oferta":
  (H1) la emisión neta de USDT llega DESPUÉS de caídas de BTC (coeficientes negativos de
       la emisión sobre los rendimientos rezagados);
  (H2) la emisión neta PREDICE alzas de BTC al día siguiente (coeficiente positivo).
La hipótesis de demanda predice lo contrario en H1 (la emisión sigue a alzas/demanda) y
cero en H2 una vez que se controla por el rendimiento propio.

Datos (públicos, sin clave):
  - USDT circulante diario de DefiLlama: https://stablecoins.llama.fi/stablecoin/1
    (campo tokens[].circulating.peggedUSD, foto a las 00:00 UTC de cada fecha);
  - velas diarias BTCUSDT de data-api.binance.vision (cierran 00:00 UTC).
Alineación conservadora: emision[d] = ln(circ[d+1]/circ[d]) es lo que cambió durante el
día UTC d (foto de las 00:00 del d+1 menos la del d) y se compara con la vela del día d.
H2 usa la vela d+1 y, para cubrir un posible desfase de la foto, también la d+2.
Límite: el paper usa flujos HORARIOS de Bitfinex a exchanges, no la oferta total diaria;
esto es una prueba gruesa, no una réplica. Uso: python3 -I este_archivo.py
"""
import json, math, urllib.request, datetime as dt
import numpy as np

UA = {"User-Agent": "Mozilla/5.0"}
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))

# Inicio jun-2020: antes, la serie de DefiLlama no cubre todas las cadenas (marca 0.03 mm USD
# el 1-ene-2019 y 3.2 mm el 1-ene-2020, cuando el USDT en circulación era de ~2 y ~4 mm).
INI = dt.datetime(2020, 6, 1, tzinfo=dt.timezone.utc)
ahora_ms = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)

# --- BTC diario (solo velas cerradas) ---
k, t = [], int(INI.timestamp() * 1000)
while True:
    lote = get(f"https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d&startTime={t}&limit=1000")
    if not lote:
        break
    k += lote
    t = lote[-1][0] + 86400 * 1000
    if len(lote) < 1000:
        break
cierre = {r[0] // 1000: float(r[4]) for r in k if r[6] < ahora_ms}
apert = {r[0] // 1000: float(r[1]) for r in k if r[6] < ahora_ms}

# --- USDT circulante ---
u = get("https://stablecoins.llama.fi/stablecoin/1")["tokens"]
circ = {r["date"]: r["circulating"]["peggedUSD"] for r in u if r["date"] >= INI.timestamp()}

dias = sorted(d for d in cierre if d in circ and d + 86400 in circ)
r = np.array([math.log(cierre[d] / apert[d]) for d in dias])          # vela del día d
e = np.array([math.log(circ[d + 86400] / circ[d]) for d in dias])    # emisión durante d
dmon = np.array([circ[d + 86400] - circ[d] for d in dias])           # en USD
fechas = [dt.datetime.fromtimestamp(d, dt.timezone.utc).date() for d in dias]
# huecos: ¿días consecutivos?
consec = all(dias[i + 1] - dias[i] == 86400 for i in range(len(dias) - 1))

def ols_nw(y, X, L=5):
    X = np.column_stack([np.ones(len(y)), X])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    u_ = y - X @ b
    XtXi = np.linalg.inv(X.T @ X)
    S = (X * u_[:, None]).T @ (X * u_[:, None])
    for l in range(1, L + 1):
        w = 1 - l / (L + 1)
        G = (X[l:] * u_[l:, None]).T @ (X[:-l] * u_[:-l, None])
        S += w * (G + G.T)
    V = XtXi @ S @ XtXi
    return b, b / np.sqrt(np.diag(V))

def tramo(mask, nombre):
    rr, ee = r[mask], e[mask]
    n = len(rr)
    print(f"\n== {nombre}: {n} días ==")
    # H1: e_d sobre r_{d-1..d-3} y r_d (contemporáneo)
    y = ee[3:]
    X = np.column_stack([rr[3:], rr[2:-1], rr[1:-2], rr[:-3]])
    b, tt = ols_nw(y * 1e4, X)  # emisión en pb
    print("H1 emisión(pb) ~ r_d, r_d-1, r_d-2, r_d-3: b =", np.round(b[1:], 2), " t NW =", np.round(tt[1:], 2))
    # H2: r_{d+1} sobre e_d controlando r_d
    for h in (1, 2):
        y = rr[h:]
        X = np.column_stack([ee[:-h] * 1e4, rr[:-h]])
        b, tt = ols_nw(y * 100, X)  # rendimiento en %
        print(f"H2 r_d+{h}(%) ~ emisión_d(pb), r_d: b_emis = {b[1]:.4f} (t {tt[1]:.2f}); b_r = {b[2]:.3f} (t {tt[2]:.2f})")
    # Evento: días con emisión en el decil superior
    q = np.quantile(ee, 0.9)
    idx = [i for i in range(3, n - 2) if ee[i] >= q]
    pre = np.mean([rr[i - 3:i].sum() for i in idx]) * 100
    post = np.mean([rr[i + 1] for i in idx]) * 100
    base_pre = np.mean([rr[i - 3:i].sum() for i in range(3, n - 2)]) * 100
    base_post = np.mean(rr[4:n - 1]) * 100
    print(f"Decil superior de emisión (>= {q*1e4:.1f} pb/día, {len(idx)} días): r 3 días antes {pre:+.2f}% "
          f"(incondicional {base_pre:+.2f}%); r día siguiente {post:+.3f}% (incond. {base_post:+.3f}%)")
    return idx

print(f"Muestra {fechas[0]} a {fechas[-1]}, {len(dias)} días; consecutivos: {consec}")
print(f"USDT circulante: {circ[dias[0]]/1e9:.2f} mm -> {circ[dias[-1]+86400]/1e9:.2f} mm USD")
print(f"Emisión neta diaria: media {dmon.mean()/1e6:.1f} M, p95 {np.quantile(dmon,0.95)/1e6:.0f} M, "
      f"días con quema neta {np.mean(dmon<0)*100:.1f}%")
F = np.array([f.year for f in fechas])
tramo(np.ones(len(r), bool), "Todo jun-2020 a oct-2026")
tramo(F <= 2021, "jun-2020 a 2021")
tramo(F >= 2022, "2022-2026 (después de la orden de la CFTC, oct-2021)")
# Últimos 30 días, descriptivo
print("\nÚltimos 10 días (fecha, emisión M USD, r BTC %):")
for i in range(len(dias) - 10, len(dias)):
    print(f"  {fechas[i]}  {dmon[i]/1e6:+9.1f}  {r[i]*100:+6.2f}")
s30 = dmon[-30:].sum() / 1e9
print(f"Emisión neta 30 días: {s30:+.2f} mm USD; BTC 30 días {(r[-30:].sum())*100:+.2f}% (log)")
