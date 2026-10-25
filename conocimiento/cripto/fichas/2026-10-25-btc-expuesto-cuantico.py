"""Ficha 2026-10-25 · Conteo propio del BTC expuesto a la exposición larga cuántica (P2PK de coinbase).

Muestra estratificada de las transacciones coinbase de los bloques 0-419,999 (6 estratos, 60
bloques por estrato, semilla 20261025), leída de las API públicas de Esplora
(blockstream.info/api y mempool.space/api): tipo de cada salida y si ya se gastó (/outspends).

Uso:  python3 -I 2026-10-25-btc-expuesto-cuantico.py 2026-10-25-btc-expuesto-cuantico-muestra.jsonl
"""
import json, random, statistics, sys, math

ruta = sys.argv[1] if len(sys.argv) > 1 else "2026-10-25-btc-expuesto-cuantico-muestra.jsonl"
filas = [json.loads(l) for l in open(ruta)]
SAT = 1e8

estratos = {}
for f in filas:
    estratos.setdefault(tuple(f["estrato"]), []).append(f)


def por_bloque(f):
    """BTC de la coinbase: total, en P2PK sin gastar, en P2PK gastado, en otros tipos sin gastar."""
    tot = sum(v["sat"] for v in f["vout"]) / SAT
    p2pk_viva = sum(v["sat"] for v in f["vout"] if v["tipo"] == "p2pk" and not v["gastada"]) / SAT
    p2pk_gast = sum(v["sat"] for v in f["vout"] if v["tipo"] == "p2pk" and v["gastada"]) / SAT
    otra_viva = sum(v["sat"] for v in f["vout"] if v["tipo"] != "p2pk" and not v["gastada"]) / SAT
    llaves = sum(1 for v in f["vout"] if v["tipo"] == "p2pk" and not v["gastada"] and v["sat"] > 0)
    return tot, p2pk_viva, p2pk_gast, otra_viva, llaves


def estimar(estr):
    total = 0.0
    llaves = 0.0
    filas_out = []
    for (lo, hi), fs in sorted(estr.items()):
        N = hi - lo
        xs = [por_bloque(f) for f in fs]
        m_viva = statistics.mean(x[1] for x in xs)
        m_tot = statistics.mean(x[0] for x in xs)
        frac_p2pk = statistics.mean(1.0 if (x[1] + x[2]) > 0 else 0.0 for x in xs)
        m_llaves = statistics.mean(x[4] for x in xs)
        total += N * m_viva
        llaves += N * m_llaves
        filas_out.append((lo, hi, len(fs), frac_p2pk, m_viva / m_tot if m_tot else 0, N * m_viva))
    return total, llaves, filas_out


total, llaves, tabla = estimar(estratos)
print("Estrato (alturas)       n   %coinb. P2PK  %BTC sigue en P2PK  BTC estimado")
for lo, hi, n, fp, fv, b in tabla:
    print(f"{lo:>7,}-{hi-1:>7,}  {n:>4}   {fp*100:6.1f}%        {fv*100:6.1f}%        {b:>12,.0f}")
print(f"Estimación puntual de BTC en P2PK de coinbase sin gastar: {total:,.0f} BTC; llaves expuestas ≈ {llaves:,.0f}")

# Bootstrap estratificado (re-muestreo dentro de cada estrato)
random.seed(1)
bs = []
for _ in range(4000):
    e2 = {k: [random.choice(v) for _ in v] for k, v in estratos.items()}
    bs.append(estimar(e2)[0])
bs.sort()
lo95, hi95 = bs[int(0.025 * len(bs))], bs[int(0.975 * len(bs))]
print(f"IC 95% bootstrap: {lo95:,.0f} - {hi95:,.0f} BTC")

# Comparación con Babbush et al. (arXiv 2603.28846 v2): >1.7 M BTC en P2PK (todas las P2PK, no solo coinbase),
# ~6.9 M BTC vulnerables en total (fig. 5) y ~2.3 M vulnerables y dormidos 5 años (fig. 13).
ALTURA = 973080  # punta de la cadena, blockstream.info/api/blocks/tip/height, 25-oct-2026 14:3x UTC
OFERTA = 210000 * (50 + 25 + 12.5 + 6.25) + (ALTURA + 1 - 840000) * 3.125  # emisión teórica por calendario
print(f"Oferta emitida por calendario a la altura {ALTURA:,}: {OFERTA:,.0f} BTC")
for nombre, b in [("P2PK coinbase (propio)", total), ("P2PK total (paper)", 1.7e6),
                  ("vulnerables y dormidos (paper)", 2.3e6), ("vulnerables total (paper)", 6.9e6)]:
    print(f"{nombre:34s} {b/1e6:5.2f} M BTC = {b/OFERTA*100:5.1f}% de la oferta")

# Tiempo de barrido secuencial de las llaves P2PK de coinbase con una sola máquina
for etiqueta, minutos in [("reloj rápido, 10 min/llave", 10), ("reloj rápido, 1 h/llave", 60),
                          ("reloj lento, 26 días/llave", 26 * 24 * 60)]:
    dias = llaves * minutos / 60 / 24
    print(f"Barrer {llaves:,.0f} llaves a {etiqueta}: {dias:,.0f} días ({dias/365:,.1f} años)")

# Escala de mercado: oferta vendible contra la peor salida diaria reciente de los ETF spot (22-oct-2026, −635.5 M USD)
PRECIO = 80304.31   # BTCUSDT Binance 25-oct-2026 14:19 UTC
SALIDA = 635.5e6 / PRECIO
print(f"Salida ETF del 22-oct ≈ {SALIDA:,.0f} BTC; P2PK coinbase = {total/SALIDA:,.0f} días de esa salida")
