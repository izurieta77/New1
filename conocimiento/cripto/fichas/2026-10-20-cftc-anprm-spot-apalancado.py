"""Ficha 2026-10-20 · CFTC ANPRM "Regulation CTX / Regulation CAM" (91 FR 64811, RIN 3038-AF80).

Comprueba tres cosas:
1. Calendario: 13-oct-2026 + 60 días cae en sábado, y por eso el cierre de comentarios es el lunes
   14-dic-2026; a partir de ahí, la fecha más temprana plausible de vigencia (ANPRM -> NPRM -> regla final).
2. Por qué el apalancamiento minorista preocupa al regulador: la probabilidad de liquidación de un largo
   apalancado en BTC dentro de la ventana de "actual delivery" (28 días), por dos métodos:
   A) fórmula cerrada de cruce de barrera para un movimiento browniano geométrico (vol30 actual y vol estresada);
   B) ventanas históricas de 28 días con los MÍNIMOS diarios de BTCUSDT en Binance (ago-2017 a 19-oct-2026).
3. Contraste: un spot pagado al 100% (lo que hace la cuenta) no tiene liquidación; su peor caída en 28 días
   se reporta para escala.

Uso: python3 -I 2026-10-20-cftc-anprm-spot-apalancado.py   (descarga velas públicas de data-api.binance.vision)
"""
import datetime as dt
import json
import math
import urllib.request
from statistics import NormalDist

N = NormalDist()

# ---------- 1. Calendario ----------
pub = dt.date(2026, 10, 13)
d60 = pub + dt.timedelta(days=60)
cierre = d60
while cierre.weekday() >= 5:  # sábado/domingo -> siguiente día hábil
    cierre += dt.timedelta(days=1)
print(f"Publicación FR {pub}; +60 días = {d60} ({d60.strftime('%A')}); cierre efectivo {cierre}")
assert cierre == dt.date(2026, 12, 14), "no cuadra con DATES del FR"
# Supuestos de ruta mínima (no son plazos legales, salvo el de la CRA): análisis de comentarios 60 d,
# NPRM con 60 d de comentarios, regla final 60 d después, vigencia >= 60 d (regla mayor, 5 U.S.C. 801(a)(3)).
f = cierre
for nombre, dias in [("NPRM publicado", 60), ("cierre de comentarios del NPRM", 60),
                     ("regla final publicada", 60), ("vigencia (regla mayor, CRA)", 60)]:
    f += dt.timedelta(days=dias)
    print(f"  {nombre:<32} ~{f}")
vigencia_min = f

# ---------- 2A. Fórmula cerrada ----------
def p_cruce(b, sigma, T):
    """P(min_{t<=T} S_t/S_0 <= b), GBM sin drift en precio (drift log = -sigma^2/2)."""
    mu = -0.5 * sigma ** 2
    lb = math.log(b)
    s = sigma * math.sqrt(T)
    return N.cdf((lb - mu * T) / s) + math.exp(2 * mu * lb / sigma ** 2) * N.cdf((lb + mu * T) / s)

def barrera(L, mm=0.005):
    """Precio de liquidación relativo de un largo aislado con apalancamiento L y margen de mantenimiento mm."""
    return (1 - 1 / L) / (1 - mm)

T = 28 / 365
VOL30 = 0.3209  # vol30 de la bitácora del 20-oct (cascada 18:42 del 19-oct, recalculada hoy)
levs = [2, 3, 5, 10, 20]

# ---------- 2B. Ventanas históricas ----------
def klines(start_ms, end_ms):
    out = []
    while start_ms < end_ms:
        url = ("https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d"
               f"&startTime={start_ms}&endTime={end_ms}&limit=1000")
        with urllib.request.urlopen(url, timeout=60) as r:
            k = json.load(r)
        if not k:
            break
        out += k
        start_ms = k[-1][0] + 86_400_000
    return out

ini = int(dt.datetime(2017, 8, 17, tzinfo=dt.timezone.utc).timestamp() * 1000)
fin = int(dt.datetime(2026, 10, 19, 23, 59, 59, tzinfo=dt.timezone.utc).timestamp() * 1000)
K = klines(ini, fin)
cl = [float(x[4]) for x in K]
lo = [float(x[3]) for x in K]
n = len(K)
print(f"\nVelas diarias: {n} ({dt.datetime.utcfromtimestamp(K[0][0]/1000).date()} a "
      f"{dt.datetime.utcfromtimestamp(K[-1][0]/1000).date()})")
assert dt.datetime.utcfromtimestamp(K[-1][0] / 1000).date() == dt.date(2026, 10, 19)

# Entrada al cierre del día i; ventana = mínimos de los días i+1..i+28.
peor = []
for i in range(n - 28):
    peor.append(min(lo[i + 1:i + 29]) / cl[i])
desde22 = [j for j in range(n - 28) if K[j][0] >= int(dt.datetime(2022, 8, 1, tzinfo=dt.timezone.utc).timestamp() * 1000)]

print(f"\n{'L':>3} {'barrera':>8} {'A vol30':>8} {'A vol60':>8} {'B 2017-26':>10} {'B ago22-26':>11}")
res = {}
for L in levs:
    b = barrera(L)
    a1 = p_cruce(b, VOL30, T)
    a2 = p_cruce(b, 0.60, T)
    b_all = sum(p <= b for p in peor) / len(peor)
    b_22 = sum(peor[j] <= b for j in desde22) / len(desde22)
    res[L] = (b, a1, a2, b_all, b_22)
    print(f"{L:>3} {b:>8.4f} {a1:>8.2%} {a2:>8.2%} {b_all:>10.2%} {b_22:>11.2%}")

# ---------- 3. Spot pagado ----------
pe = sorted(peor)
print(f"\nSpot pagado (sin liquidación): peor caída intraventana 28d, mediana {1-pe[len(pe)//2]:.1%}, "
      f"p95 {1-pe[int(0.05*len(pe))]:.1%}, máximo {1-pe[0]:.1%}")

# Aserciones de coherencia
assert all(res[a][3] <= res[b][3] for a, b in zip(levs, levs[1:])), "B debe crecer con L"
assert all(res[a][1] <= res[b][1] for a, b in zip(levs, levs[1:])), "A debe crecer con L"
# 2x en 28 días requiere una caída de ~50%: poco frecuente pero no imposible (2018, mar-2020, 2022).
assert res[2][3] < 0.05
print("\nOK: aserciones superadas")
