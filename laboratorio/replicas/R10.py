"""R10 (ejecución A): filtro SMA200 con banda sobre BTC/USDT de Binance. Pre-registro: R10-filtro-sma200-btc.md."""
import hashlib, json, math, os, sys, time, urllib.request
from datetime import datetime, timezone, timedelta

BASE = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(BASE, "R10-datos", "BTCUSDT-1d.json")
COSTO = 0.0015


def descargar():
    filas, inicio = [], 1502928000000  # 2017-08-17
    while True:
        url = ("https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d"
               f"&startTime={inicio}&limit=1000")
        with urllib.request.urlopen(url, timeout=60) as r:
            lote = json.load(r)
        if not lote:
            break
        filas += lote
        inicio = lote[-1][0] + 86_400_000
        if len(lote) < 1000:
            break
        time.sleep(0.3)
    hoy = int(datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)
    filas = [f for f in filas if f[6] < hoy]  # solo velas cerradas
    with open(DATOS, "w") as f:
        json.dump(filas, f)


def cargar():
    if not os.path.exists(DATOS):
        descargar()
    filas = json.load(open(DATOS))
    sha = hashlib.sha256(open(DATOS, "rb").read()).hexdigest()
    serie = [(datetime.fromtimestamp(f[0] / 1000, timezone.utc).date(), float(f[4])) for f in filas]
    return serie, sha


def simular(serie, n=200, banda=0.03, rezago=1, desde=None, hasta=None):
    fechas = [d for d, _ in serie]
    precios = [p for _, p in serie]
    sma = [None] * len(precios)
    acum = 0.0
    for i, p in enumerate(precios):
        acum += p
        if i >= n:
            acum -= precios[i - n]
        if i >= n - 1:
            sma[i] = acum / n
    # señal: 1 invertido, 0 fuera; arranca en el primer día con SMA según el lado de la media
    senal = [None] * len(precios)
    estado = None
    for i in range(len(precios)):
        if sma[i] is None:
            continue
        if estado is None:
            estado = 1 if precios[i] > sma[i] else 0
        elif estado == 1 and precios[i] < sma[i] * (1 - banda):
            estado = 0
        elif estado == 0 and precios[i] > sma[i] * (1 + banda):
            estado = 1
        senal[i] = estado
    primero = next(i for i, s in enumerate(senal) if s is not None) + rezago
    # posición en el día i (rendimiento de i-1 a i) = señal de i-1-rezago+... : posición vigente al cierre de i-1
    pos = [None] * len(precios)
    for i in range(primero, len(precios)):
        pos[i] = senal[i - rezago]
    i0 = primero
    if desde:
        i0 = max(i0, next(i for i, d in enumerate(fechas) if d >= desde))
    i1 = len(precios) - 1 if not hasta else max(i for i, d in enumerate(fechas) if d <= hasta)
    eq, bh = [1.0], [1.0]
    trades, salidas = 0, []
    prev = pos[i0]
    eq[0] *= (1 - COSTO) if prev == 1 else 1
    bh[0] *= (1 - COSTO)
    for i in range(i0 + 1, i1 + 1):
        r = precios[i] / precios[i - 1] - 1
        e = eq[-1] * (1 + r) if pos[i - 1] == 1 else eq[-1]
        if pos[i] != pos[i - 1]:
            e *= (1 - COSTO)
            if pos[i] == 0:
                salidas.append(i)
            else:
                trades += 1
        eq.append(e)
        bh.append(bh[-1] * (1 + r))
    # salidas en falso: reentrada a un precio mayor que el de salida dentro de 30 días
    falsas = 0
    for s in salidas:
        for j in range(s + 1, min(s + 31, i1 + 1)):
            if pos[j] == 1:
                if precios[j] > precios[s]:
                    falsas += 1
                break
    return metricas(eq, fechas[i0], fechas[i1]), metricas(bh, fechas[i0], fechas[i1]), len(salidas), falsas


def metricas(eq, d0, d1):
    anios = (d1 - d0).days / 365.0
    cagr = eq[-1] ** (1 / anios) - 1
    rs = [eq[i] / eq[i - 1] - 1 for i in range(1, len(eq))]
    m = sum(rs) / len(rs)
    sd = math.sqrt(sum((x - m) ** 2 for x in rs) / (len(rs) - 1))
    pico, mdd = eq[0], 0.0
    for v in eq:
        pico = max(pico, v)
        mdd = min(mdd, v / pico - 1)
    return {"desde": str(d0), "hasta": str(d1), "cagr": cagr, "vol": sd * math.sqrt(365),
            "sharpe": (m / sd) * math.sqrt(365) if sd else float("nan"), "mdd": mdd, "multiplo": eq[-1]}


if __name__ == "__main__":
    serie, sha = cargar()
    print(f"BTCUSDT 1d: {len(serie)} cierres, {serie[0][0]} a {serie[-1][0]}, sha256 {sha[:16]}…")
    huecos = sum(1 for a, b in zip(serie, serie[1:]) if (b[0] - a[0]).days != 1)
    print("huecos de fecha:", huecos)
    from datetime import date
    variantes = {"principal SMA200 ±3% t+1": dict(), "sin banda": dict(banda=0.0),
                 "banda ±5%": dict(banda=0.05), "SMA100 ±3%": dict(n=100), "mismo día t": dict(rezago=0)}
    periodos = {"completo": (None, None), "2018-2020": (None, date(2020, 12, 31)), "2021-hoy": (date(2021, 1, 1), None)}
    out = {}
    for pn, (a, b) in periodos.items():
        print(f"\n== {pn}")
        for vn, kw in variantes.items():
            r, bh, ns, nf = simular(serie, desde=a, hasta=b, **kw)
            out[f"{pn}|{vn}"] = {"regla": r, "bh": bh, "salidas": ns, "falsas": nf}
            print(f"{vn:28s} CAGR {r['cagr']:+.1%} vol {r['vol']:.1%} Sharpe {r['sharpe']:.2f} MDD {r['mdd']:.1%} "
                  f"salidas {ns} falsas {nf} ({(nf/ns if ns else 0):.0%}) | B&H CAGR {bh['cagr']:+.1%} Sharpe {bh['sharpe']:.2f} "
                  f"MDD {bh['mdd']:.1%} [{r['desde']}→{r['hasta']}]")
    json.dump({"sha256": sha, "resultados": out}, open(os.path.join(BASE, "R10-resultados.json"), "w"), indent=1, default=str)
