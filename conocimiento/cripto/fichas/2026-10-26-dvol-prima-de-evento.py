"""Ficha 2026-10-26 · DVOL, prima de riesgo de varianza y prima de evento (FOMC) en opciones de BTC.

Dos preguntas, con datos públicos:
  A. ¿El DVOL de Deribit (volatilidad implícita a 30 días) sobreestima la volatilidad realizada de los
     30 días siguientes? ¿Cuánto, y predice mejor que la volatilidad realizada pasada?
  B. ¿Cuánta varianza extra cotiza hoy la cadena de opciones para el día de la decisión del FOMC
     (28-oct-2026, 18:00 UTC) y cuánta varianza extra tuvo BTC, de verdad, en las 47 decisiones
     programadas de 2021-2026?

Fuentes (todas públicas, sin clave):
  - Deribit public/get_volatility_index_data (DVOL BTC, velas diarias) y
    public/get_book_summary_by_currency?currency=BTC&kind=option (cadena, mark_iv).
  - Binance data-api.binance.vision klines BTCUSDT 1d y 8h.
  - Fechas del FOMC: federalreserve.gov/monetarypolicy/fomccalendars.htm (copiadas abajo).

Uso (desde cualquier directorio; las rutas son relativas a este archivo):
  python3 -I conocimiento/cripto/fichas/2026-10-26-dvol-prima-de-evento.py descargar   # baja la foto
  python3 -I conocimiento/cripto/fichas/2026-10-26-dvol-prima-de-evento.py             # analiza la foto
La foto queda en 2026-10-26-dvol-prima-de-evento-datos.json, junto a este archivo.
"""
import datetime as dt
import json
import math
import os
import random
import statistics as st
import sys
import time
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTO = os.path.join(AQUI, "2026-10-26-dvol-prima-de-evento-datos.json")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}

# Día de la decisión (segundo día de la reunión) de las reuniones programadas, según el calendario de la Fed.
# Se excluye el "notation vote" del 22-ago-2025 (no es reunión con comunicado programado).
FOMC = """2021-01-27 2021-03-17 2021-04-28 2021-06-16 2021-07-28 2021-09-22 2021-11-03 2021-12-15
2022-01-26 2022-03-16 2022-05-04 2022-06-15 2022-07-27 2022-09-21 2022-11-02 2022-12-14
2023-02-01 2023-03-22 2023-05-03 2023-06-14 2023-07-26 2023-09-20 2023-11-01 2023-12-13
2024-01-31 2024-03-20 2024-05-01 2024-06-12 2024-07-31 2024-09-18 2024-11-07 2024-12-18
2025-01-29 2025-03-19 2025-05-07 2025-06-18 2025-07-30 2025-09-17 2025-10-29 2025-12-10
2026-01-28 2026-03-18 2026-04-29 2026-06-17 2026-07-29 2026-09-16""".split()
PROXIMO_FOMC = "2026-10-28"
VENCIMIENTOS = ["27OCT26", "28OCT26", "29OCT26", "30OCT26", "6NOV26"]


def _get(url):
    for intento in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except Exception:
            if intento == 3:
                raise
            time.sleep(2 * (intento + 1))


def descargar():
    fin = int(time.time() * 1000)
    # DVOL diario: la API devuelve hasta 1,000 velas hacia atrás y un "continuation".
    dvol, hasta = {}, fin
    while True:
        r = _get("https://www.deribit.com/api/v2/public/get_volatility_index_data?currency=BTC"
                 f"&resolution=1D&start_timestamp=1609459200000&end_timestamp={hasta}")["result"]
        for t, o, h, l, c in r["data"]:
            dvol[t] = c
        if not r["continuation"]:
            break
        hasta = r["continuation"]
    # Klines BTCUSDT (Binance) 1d y 8h desde 2021-01-01.
    def klines(intervalo):
        filas, desde = [], 1609459200000
        while True:
            k = _get("https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT"
                     f"&interval={intervalo}&startTime={desde}&limit=1000")
            filas += [[x[0], float(x[1]), float(x[4]), x[6]] for x in k]
            if len(k) < 1000:
                break
            desde = k[-1][0] + 1
        return filas
    k1d, k8h = klines("1d"), klines("8h")
    cadena = _get("https://www.deribit.com/api/v2/public/get_book_summary_by_currency?currency=BTC&kind=option")["result"]
    cadena = [{c: x[c] for c in ("instrument_name", "mark_iv", "underlying_price", "creation_timestamp",
                                 "bid_price", "ask_price", "mark_price", "open_interest")}
              for x in cadena if x["instrument_name"].split("-")[1] in VENCIMIENTOS]
    inst = _get("https://www.deribit.com/api/v2/public/get_instruments?currency=BTC&kind=option&expired=false")["result"]
    vence = {x["instrument_name"].split("-")[1]: x["expiration_timestamp"] for x in inst
             if x["instrument_name"].split("-")[1] in VENCIMIENTOS}
    foto = {"descargado_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "dvol_1d": sorted([t, c] for t, c in dvol.items()), "btc_1d": k1d, "btc_8h": k8h,
            "cadena": cadena, "vencimientos_ms": vence}
    json.dump(foto, open(FOTO, "w"), separators=(",", ":"))
    print("foto guardada:", FOTO, foto["descargado_utc"])


def fecha(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc)


def parte_a(f):
    """Prima de riesgo de volatilidad: DVOL_t contra la volatilidad realizada de t+1..t+30."""
    ahora = f["btc_1d"][-1][0]
    cierres = {fecha(t).date(): c for t, o, c, ct in f["btc_1d"] if ct < f["btc_1d"][-1][3]}  # solo velas completas
    dias = sorted(cierres)
    r = {dias[i]: math.log(cierres[dias[i]] / cierres[dias[i - 1]]) for i in range(1, len(dias))}
    # La vela diaria del DVOL que empieza el día d cierra a la misma hora que la vela diaria de BTC del día d.
    dv = {fecha(t).date(): c for t, c in f["dvol_1d"]}
    filas = []
    for d in dias:
        if d not in dv:
            continue
        i = dias.index(d)
        if i + 30 >= len(dias) or i < 30:
            continue
        fut = [r[dias[i + k]] for k in range(1, 31)]
        pas = [r[dias[i - k]] for k in range(0, 30)]
        rv_f = 100 * math.sqrt(365 / 30 * sum(x * x for x in fut))
        rv_p = 100 * math.sqrt(365 / 30 * sum(x * x for x in pas))
        filas.append((d, dv[d], rv_f, rv_p))
    n = len(filas)
    vrp = [a - b for _, a, b, _ in filas]
    vrp_var = [(a / 100) ** 2 - (b / 100) ** 2 for _, a, b, _ in filas]
    print(f"A. DVOL contra realizada a 30 días: {n} días, {filas[0][0]} a {filas[-1][0]}")
    print(f"   DVOL medio {st.mean(x[1] for x in filas):.2f}; realizada futura media {st.mean(x[2] for x in filas):.2f}")
    print(f"   VRP (puntos de vol): media {st.mean(vrp):+.2f}, mediana {st.median(vrp):+.2f}, "
          f"DVOL > realizada en {100 * sum(v > 0 for v in vrp) / n:.1f}% de los días")
    print(f"   VRP en varianza (DVOL² − RV²): media {st.mean(vrp_var):+.4f}")
    # Muestras sin traslape (cada 30 días) para un error estándar honesto.
    sub = vrp[::30]
    print(f"   Sin traslape (cada 30 d, n={len(sub)}): media {st.mean(sub):+.2f}, "
          f"e.e. {st.stdev(sub) / math.sqrt(len(sub)):.2f}, t = {st.mean(sub) / (st.stdev(sub) / math.sqrt(len(sub))):.2f}, "
          f"positivos {100 * sum(v > 0 for v in sub) / len(sub):.0f}%")
    # Mincer-Zarnowitz y error de pronóstico: DVOL contra la realizada pasada.
    def mz(xs, ys):
        mx, my = st.mean(xs), st.mean(ys)
        b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
        a = my - b * mx
        res = [y - a - b * x for x, y in zip(xs, ys)]
        r2 = 1 - sum(e * e for e in res) / sum((y - my) ** 2 for y in ys)
        return a, b, r2
    y = [x[2] for x in filas]
    for nombre, xs in (("DVOL", [x[1] for x in filas]), ("RV pasada 30d", [x[3] for x in filas])):
        a, b, r2 = mz(xs, y)
        rmse = math.sqrt(st.mean((p - q) ** 2 for p, q in zip(xs, y)))
        print(f"   {nombre:14s}: RV_fut = {a:5.2f} + {b:4.2f}·x, R² {r2:.2f}; RMSE sin ajustar {rmse:.2f} pts")
    # Por año y por tramo del DVOL.
    for an in sorted({x[0].year for x in filas}):
        g = [a - b for d, a, b, _ in filas if d.year == an]
        print(f"   {an}: n={len(g):3d} VRP media {st.mean(g):+6.2f}  positivos {100 * sum(v > 0 for v in g) / len(g):4.0f}%")
    for lo, hi in ((0, 45), (45, 60), (60, 200)):
        g = [(a, b) for d, a, b, _ in filas if lo <= a < hi]
        if g:
            print(f"   DVOL en [{lo},{hi}): n={len(g):4d} RV_fut media {st.mean(b for _, b in g):5.2f} "
                  f"(DVOL medio {st.mean(a for a, _ in g):5.2f}); RV_fut > DVOL en {100 * sum(b > a for a, b in g) / len(g):.0f}%")
    # Condicionar en el DVOL mete un sesgo mecánico (DVOL alto ⇒ VRP alto). Por eso también por la RV pasada.
    for lo, hi in ((0, 35), (35, 50), (50, 70), (70, 300)):
        g = [(a, b) for d, a, b, p in filas if lo <= p < hi]
        if g:
            print(f"   RV pasada en [{lo},{hi}): n={len(g):4d} DVOL medio {st.mean(a for a, _ in g):5.2f} "
                  f"RV_fut media {st.mean(b for _, b in g):5.2f}; VRP {st.mean(a - b for a, b in g):+5.2f}; "
                  f"razón DVOL²/RV² {st.mean(a * a for a, _ in g) / st.mean(b * b for _, b in g):.2f}")
    hoy = f["dvol_1d"][-1]
    print(f"   DVOL último (vela {fecha(hoy[0]).date()}): {hoy[1]:.2f}")
    return filas


def parte_b(f):
    """Prima de evento: varianza extra del día del FOMC, histórica (08:00→08:00 UTC) e implícita (cadena)."""
    abre8 = {fecha(t): o for t, o, c, ct in f["btc_8h"]}
    r = {}
    for t, o in abre8.items():
        if t.hour == 8:
            s = t + dt.timedelta(days=1)
            if s in abre8:
                r[t.date()] = math.log(abre8[s] / o)
    fomc = {dt.date.fromisoformat(x) for x in FOMC}
    ev = [r[d] for d in sorted(fomc) if d in r]
    resto = [v for d, v in r.items() if d not in fomc and d.weekday() < 5]  # días hábiles sin FOMC
    m_ev, m_re = st.mean(v * v for v in ev), st.mean(v * v for v in resto)
    print(f"\nB1. Histórico 08:00→08:00 UTC (Binance 8h), {len(ev)} decisiones FOMC contra {len(resto)} días hábiles sin FOMC")
    print(f"   σ diaria FOMC {100 * math.sqrt(m_ev):.2f}% contra {100 * math.sqrt(m_re):.2f}%; razón de varianzas {m_ev / m_re:.2f}")
    print(f"   |r| mediano FOMC {100 * st.median(abs(v) for v in ev):.2f}% contra {100 * st.median(abs(v) for v in resto):.2f}%")
    rnd = random.Random(20261026)
    boots = []
    for _ in range(4000):
        e = [rnd.choice(ev) for _ in ev]
        q = [rnd.choice(resto) for _ in range(len(resto))]
        boots.append(st.mean(v * v for v in e) / st.mean(v * v for v in q))
    boots.sort()
    print(f"   IC 95% bootstrap de la razón: {boots[100]:.2f}-{boots[3899]:.2f}")
    # Razón robusta: varianza del FOMC contra la de los 20 días hábiles previos a cada decisión.
    ratios = []
    for d in sorted(fomc):
        if d not in r:
            continue
        prev = [r[d - dt.timedelta(days=k)] for k in range(1, 40)
                if (d - dt.timedelta(days=k)) in r and (d - dt.timedelta(days=k)).weekday() < 5][:20]
        if len(prev) == 20:
            ratios.append(r[d] ** 2 / st.mean(v * v for v in prev))
    print(f"   Contra sus 20 días hábiles previos: media de r²/σ²_previa {st.mean(ratios):.2f}, mediana {st.median(ratios):.2f}")
    for umbral in (0.02, 0.03, 0.04):
        print(f"   P(|r| > {100 * umbral:.0f}%): FOMC {100 * sum(abs(v) > umbral for v in ev) / len(ev):.0f}% "
              f"(n={len(ev)}), resto {100 * sum(abs(v) > umbral for v in resto) / len(resto):.0f}%")
    por_an = {}
    for d in sorted(fomc):
        if d in r:
            por_an.setdefault(d.year, []).append(abs(r[d]))
    print("   |r| medio por año en FOMC: " + ", ".join(f"{a} {100 * st.mean(v):.2f}%" for a, v in por_an.items()))

    # Implícito: IV ATM por vencimiento, interpolada en el forward de cada vencimiento.
    t0 = max(x["creation_timestamp"] for x in f["cadena"])
    print(f"\nB2. Cadena Deribit (foto {fecha(t0):%Y-%m-%d %H:%M} UTC): IV ATM por vencimiento y varianza a plazo")
    atm = {}
    for v in VENCIMIENTOS:
        xs = [x for x in f["cadena"] if x["instrument_name"].split("-")[1] == v and x["mark_iv"]]
        F = st.median(x["underlying_price"] for x in xs)
        por_k = {}
        for x in xs:
            k = float(x["instrument_name"].split("-")[2])
            por_k.setdefault(k, []).append(x["mark_iv"])
        ks = sorted(por_k)
        lo = max(k for k in ks if k <= F)
        hi = min(k for k in ks if k >= F)
        ivl, ivh = st.mean(por_k[lo]), st.mean(por_k[hi])
        iv = ivl if hi == lo else ivl + (ivh - ivl) * (math.log(F / lo)) / math.log(hi / lo)
        T = (f["vencimientos_ms"][v] - t0) / 1000 / 86400 / 365
        atm[v] = (iv, T, F)
        print(f"   {v:8s} vence {fecha(f['vencimientos_ms'][v]):%a %d-%b %H:%M} UTC  F {F:9,.0f}  IV ATM {iv:5.2f}  T {T * 365:6.3f} d  w {(iv / 100) ** 2 * T:.6f}")
    ant = None
    fwd = {}
    for v in VENCIMIENTOS:
        iv, T, _ = atm[v]
        w = (iv / 100) ** 2 * T
        if ant:
            dw, dT = w - ant[1], T - ant[2]
            fwd[(ant[0], v)] = (dw, dT)
            print(f"   {ant[0]:>7s}→{v:7s}: vol a plazo {100 * math.sqrt(max(dw, 0) / dT):6.2f}% anual; "
                  f"σ del tramo {100 * math.sqrt(max(dw, 0)):.2f}% en {dT * 365:.2f} d")
        else:
            fwd[("hoy", v)] = (w, T)
        ant = (v, w, T)
    dw_ev, dT_ev = fwd[("28OCT26", "29OCT26")]
    dw_b1, dT_b1 = fwd[("27OCT26", "28OCT26")]
    dw_b2, dT_b2 = fwd[("29OCT26", "30OCT26")]
    base1 = dw_b1 / dT_b1 * dT_ev
    base2 = (dw_b1 + dw_b2) / (dT_b1 + dT_b2) * dT_ev
    print(f"   Tramo del FOMC (28→29-oct): σ implícita {100 * math.sqrt(dw_ev):.2f}%")
    for nombre, base in (("base 27→28 (limpia)", base1), ("base 27→28 y 29→30 (29→30 trae PIB y BCE)", base2)):
        extra = dw_ev - base
        print(f"   {nombre}: razón implícita {dw_ev / base:.2f}; varianza extra {extra:+.6f} "
              f"→ salto de evento 1σ {100 * math.sqrt(max(extra, 0)):.2f}%")
    # Comparación directa: σ implícita del tramo contra la σ histórica del día FOMC escalada al régimen actual.
    prev20 = [r[d] for d in sorted(r) if d.weekday() < 5][-20:]
    s_prev = math.sqrt(st.mean(v * v for v in prev20))
    print(f"   σ realizada de los últimos 20 días hábiles (08:00→08:00): {100 * s_prev:.2f}%; "
          f"× √razón histórica ({m_ev / m_re:.2f}) = {100 * s_prev * math.sqrt(m_ev / m_re):.2f}% para el día FOMC")

    # B3. Base para el pronóstico: P(|r| > σ implícita del tramo) con dos estandarizaciones históricas.
    umbral = math.sqrt(dw_ev)
    dv = {fecha(t).date(): c for t, c in f["dvol_1d"]}
    dias = sorted(r)
    z_rv, z_dv = {True: [], False: []}, {True: [], False: []}
    for d in dias:
        if d.weekday() >= 5:
            continue
        prev = [r[x] for x in dias if x < d and x.weekday() < 5][-20:]
        if len(prev) == 20:
            z_rv[d in fomc].append(abs(r[d]) / math.sqrt(st.mean(v * v for v in prev)))
        p = d - dt.timedelta(days=1)
        if p in dv:
            z_dv[d in fomc].append(abs(r[d]) / (dv[p] / 100 / math.sqrt(365)))
    k_rv = umbral / s_prev
    k_dv = umbral / (f["dvol_1d"][-1][1] / 100 / math.sqrt(365))
    print(f"\nB3. P(|r 28→29-oct| > {100 * umbral:.2f}%), umbral = σ implícita del tramo FOMC")
    for nombre, z, k in (("σ realizada 20 d", z_rv, k_rv), ("DVOL del día previo", z_dv, k_dv)):
        pf = sum(x > k for x in z[True]) / len(z[True])
        pr = sum(x > k for x in z[False]) / len(z[False])
        print(f"   escala {nombre:20s}: umbral = {k:.2f} σ; FOMC {100 * pf:.0f}% (n={len(z[True])}), "
              f"resto {100 * pr:.0f}% (n={len(z[False])}); E[z²] FOMC {st.mean(x * x for x in z[True]):.2f}, "
              f"resto {st.mean(x * x for x in z[False]):.2f}")
    print(f"   normal con σ implícita: {100 * math.erfc(1 / math.sqrt(2)):.0f}%")
    return atm, dw_ev, ev


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "descargar":
        descargar()
        sys.exit()
    foto = json.load(open(FOTO))
    print("Foto:", foto["descargado_utc"])
    parte_a(foto)
    parte_b(foto)
