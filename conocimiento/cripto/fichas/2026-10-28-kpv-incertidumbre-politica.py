"""Ficha 2026-10-28 · Kelly-Pástor-Veronesi (JF 2016): el precio de la incertidumbre política en opciones.

Réplica propia, con datos públicos, de la medida IVD de KPV (ec. 1-2 del NBER WP 19812, rev. jul-2015):
    IVD_tau = IV_b − ½ (IV_a + IV_c)
  donde IV_b promedia la volatilidad implícita de opciones cuya vida abarca el evento tau, e IV_a e IV_c
  la de opciones con el MISMO plazo cuya vida no lo abarca (antes y después). KPV usan opciones ATM de
  OptionMetrics con vencimiento mensual; aquí, sin OptionMetrics, se usa un índice de plazo constante:
    - S&P 500: VIX (CBOE, 30 días naturales ≈ 21 hábiles), Yahoo ^VIX, 1990-2026.
      Tratamiento: hábiles [tau−20, tau−1] (toda ventana de 30 días que empieza ahí abarca tau).
      Control a: hábiles [tau−41, tau−22] (la ventana termina antes de tau). Control c: [tau+1, tau+20].
    - BTC: DVOL (Deribit, 30 días naturales), 2021-2026, en días naturales:
      tratamiento [tau−20, tau−1], a [tau−51, tau−32], c [tau+1, tau+20].
  Igual que KPV, IV_x = raíz del promedio de varianzas (VIX²).

Eventos: elección federal de EUA, "the Tuesday next after the 1st Monday in November" de cada año par
(2 U.S.C. § 7). Muestra de KPV para EUA: hasta 2012. Fuera de muestra: 2014-2024.
Placebos: (i) el mismo martes de noviembre en años impares (controla estacionalidad de octubre-noviembre);
(ii) todos los días hábiles a más de 45 hábiles de una elección (distribución nula, como la tabla 8 de KPV).

Además: (iii) la parte ya observable de 2026 (tratamiento parcial contra a); (iv) comprobación de la
conversión de KPV (1.43/27.8 = 5.1% de prima en un put ATM a plazo, elasticidad precio-vol ≈ 1);
(v) pendiente put de la cadena de BTC por vencimiento (SlopeD de KPV, ec. 6, en corte transversal).

Uso (rutas relativas a este archivo):
  python3 -I conocimiento/cripto/fichas/2026-10-28-kpv-incertidumbre-politica.py descargar
  python3 -I conocimiento/cripto/fichas/2026-10-28-kpv-incertidumbre-politica.py
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
FOTO = os.path.join(AQUI, "2026-10-28-kpv-incertidumbre-politica-datos.json")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
VENC = ["30OCT26", "31OCT26", "6NOV26", "13NOV26", "27NOV26", "25DEC26"]


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
    fin = int(time.time())
    v = _get("https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX"
             f"?period1=631152000&period2={fin}&interval=1d")["chart"]["result"][0]
    vix = [[dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat(), c]
           for t, c in zip(v["timestamp"], v["indicators"]["quote"][0]["close"]) if c]
    dvol, hasta = {}, fin * 1000
    while True:
        r = _get("https://www.deribit.com/api/v2/public/get_volatility_index_data?currency=BTC"
                 f"&resolution=1D&start_timestamp=1609459200000&end_timestamp={hasta}")["result"]
        for t, o, h, l, c in r["data"]:
            dvol[dt.datetime.fromtimestamp(t / 1000, dt.timezone.utc).date().isoformat()] = c
        if not r["continuation"]:
            break
        hasta = r["continuation"]
    cad = _get("https://www.deribit.com/api/v2/public/get_book_summary_by_currency?currency=BTC&kind=option")["result"]
    cad = [{c: x[c] for c in ("instrument_name", "mark_iv", "underlying_price", "open_interest", "creation_timestamp")}
           for x in cad if x["instrument_name"].split("-")[1] in VENC]
    inst = _get("https://www.deribit.com/api/v2/public/get_instruments?currency=BTC&kind=option&expired=false")["result"]
    vence = {x["instrument_name"].split("-")[1]: x["expiration_timestamp"] for x in inst
             if x["instrument_name"].split("-")[1] in VENC}
    foto = {"descargado_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "vix_1d": vix, "dvol_1d": sorted(dvol.items()), "cadena": cad, "vencimientos_ms": vence}
    json.dump(foto, open(FOTO, "w"), separators=(",", ":"))
    print("foto guardada:", FOTO, foto["descargado_utc"], len(vix), "VIX,", len(dvol), "DVOL,", len(cad), "opciones")


def eleccion(anio):
    """Martes siguiente al primer lunes de noviembre (2 U.S.C. § 7)."""
    d = dt.date(anio, 11, 1)
    while d.weekday() != 0:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(days=1)


def rms(xs):
    return math.sqrt(sum(x * x for x in xs) / len(xs))


def ivd_habiles(fechas, val, i):
    """IVD de KPV con índice de plazo constante en días hábiles; i = índice del primer día >= tau."""
    if i - 41 < 0 or i + 20 >= len(fechas):
        return None
    b = rms(val[i - 20:i])
    a = rms(val[i - 41:i - 21])
    c = rms(val[i + 1:i + 21])
    return b - (a + c) / 2, b, a, c


def ivd_naturales(serie, tau):
    def ventana(d0, d1):
        xs = [serie.get(tau + dt.timedelta(days=k)) for k in range(d0, d1 + 1)]
        xs = [x for x in xs if x is not None]
        return rms(xs) if len(xs) >= 15 else None
    b, a, c = ventana(-20, -1), ventana(-51, -32), ventana(1, 20)
    if None in (b, a, c):
        return None
    return b - (a + c) / 2, b, a, c


def indice(fechas, d):
    for i, f in enumerate(fechas):
        if f >= d:
            return i
    return None


def resumen(xs):
    m = st.mean(xs)
    se = st.stdev(xs) / math.sqrt(len(xs)) if len(xs) > 1 else float("nan")
    return m, m / se if se else float("nan"), st.median(xs)


def p_placebo(nulos, n, obs, rng, reps=20000):
    """P(media de n pseudo-eventos >= media observada), remuestreo sin reemplazo (tabla 8 de KPV)."""
    k = sum(1 for _ in range(reps) if st.mean(rng.sample(nulos, n)) >= obs)
    return k / reps


def bs_put_fwd(F, K, s, T):
    d1 = (math.log(F / K) + 0.5 * s * s * T) / (s * math.sqrt(T))
    d2 = d1 - s * math.sqrt(T)
    N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return K * N(-d2) - F * N(-d1)


def delta_put(F, K, s, T):
    d1 = (math.log(F / K) + 0.5 * s * s * T) / (s * math.sqrt(T))
    return 0.5 * (1 + math.erf(d1 / math.sqrt(2))) - 1


def analizar(f):
    rng = random.Random(20261028)
    fechas = [dt.date.fromisoformat(d) for d, _ in f["vix_1d"]]
    vix = [c for _, c in f["vix_1d"]]
    print(f"Foto {f['descargado_utc']} · VIX {fechas[0]}..{fechas[-1]} ({len(vix)} días) · "
          f"DVOL {f['dvol_1d'][0][0]}..{f['dvol_1d'][-1][0]}")

    # ---- (iv) Conversión de KPV --------------------------------------------------------------------
    F, T = 100.0, 1 / 12
    p0, p1 = bs_put_fwd(F, F, 0.278, T), bs_put_fwd(F, F, 0.278 * 1.001, T)
    elast = ((p1 - p0) / p0) / 0.001
    print("\n(iv) Conversión de KPV: 1.43/27.8 = %.2f%%; elasticidad precio-vol del put ATM a plazo "
          "(σ=27.8%%, 1 mes) = %.4f; put con σ 29.23 cuesta %+.2f%% más que con 27.8"
          % (100 * 1.43 / 27.8, elast, 100 * (bs_put_fwd(F, F, 0.2923, T) / p0 - 1)))

    # ---- (i) Elecciones de EUA con el VIX ---------------------------------------------------------
    print("\n(i) IVD con el VIX (puntos de vol anual), elecciones federales de EUA")
    print(" año   tipo          tau         IV_b   IV_a   IV_c    IVD   IVD/ctrl")
    filas = {}
    for anio in range(1990, 2025, 2):
        tau = eleccion(anio)
        i = indice(fechas, tau)
        r = ivd_habiles(fechas, vix, i)
        if r is None:
            continue
        d, b, a, c = r
        tipo = "presidencial" if anio % 4 == 0 else "intermedia"
        filas[anio] = (d, b, a, c, tipo)
        print(f" {anio}  {tipo:12s}  {tau}  {b:5.2f}  {a:5.2f}  {c:5.2f}  {d:+5.2f}  {100 * d / ((a + c) / 2):+6.1f}%")
    dentro = [filas[y][0] for y in filas if y <= 2012]
    fuera = [filas[y][0] for y in filas if y >= 2014]
    todas = [filas[y][0] for y in filas]
    rel = lambda ys: st.mean(100 * filas[y][0] / ((filas[y][2] + filas[y][3]) / 2) for y in ys)
    # Nula: todos los días a más de 45 hábiles de cualquier elección.
    elec_i = [indice(fechas, eleccion(y)) for y in range(1990, 2027, 2)]
    nulos = []
    for i in range(41, len(fechas) - 21):
        if all(e is None or abs(i - e) > 45 for e in elec_i):
            r = ivd_habiles(fechas, vix, i)
            if r:
                nulos.append(r[0])
    print(f" Nula (días a > 45 hábiles de una elección): n={len(nulos)}, media {st.mean(nulos):+.3f}, "
          f"mediana {st.median(nulos):+.3f}, desv. {st.stdev(nulos):.2f}")
    for nombre, xs, ys in (("1990-2012 (muestra de KPV)", dentro, [y for y in filas if y <= 2012]),
                           ("2014-2024 (fuera de muestra)", fuera, [y for y in filas if y >= 2014]),
                           ("1990-2024", todas, list(filas))):
        m, t, med = resumen(xs)
        p = p_placebo(nulos, len(xs), m, rng)
        pos = sum(1 for x in xs if x > 0)
        print(f" {nombre:28s} n={len(xs):2d}  media {m:+.2f} (t {t:+.2f})  mediana {med:+.2f}  "
              f"positivos {pos}/{len(xs)}  relativa {rel(ys):+.1f}%  p_placebo {p:.3f}")
    # Robustez: dejar uno fuera, y de dónde sale la prima (antes contra después).
    for nombre, ys in (("1990-2012", [y for y in filas if y <= 2012]), ("2014-2024", [y for y in filas if y >= 2014])):
        loo = [st.mean(filas[z][0] for z in ys if z != y) for y in ys]
        ba = st.mean(filas[y][1] - filas[y][2] for y in ys)
        bc = st.mean(filas[y][1] - filas[y][3] for y in ys)
        print(f"   {nombre}: media dejando uno fuera, mín {min(loo):+.2f} / máx {max(loo):+.2f}; "
              f"b − a {ba:+.2f}, b − c {bc:+.2f}")
    for tipo in ("intermedia", "presidencial"):
        xs = [filas[y][0] for y in filas if filas[y][4] == tipo]
        m, t, med = resumen(xs)
        print(f"   {tipo:12s} n={len(xs):2d}  media {m:+.2f} (t {t:+.2f})  mediana {med:+.2f}  "
              f"p_placebo {p_placebo(nulos, len(xs), m, rng):.3f}")

    # ---- (ii) Placebo de calendario: mismo martes en años impares ---------------------------------
    imp = []
    for anio in range(1991, 2026, 2):
        r = ivd_habiles(fechas, vix, indice(fechas, eleccion(anio)))
        if r:
            imp.append(r[0])
    m, t, med = resumen(imp)
    print(f"\n(ii) Placebo de calendario (mismo martes, años impares 1991-2025): n={len(imp)}, media {m:+.2f} "
          f"(t {t:+.2f}), mediana {med:+.2f}, positivos {sum(1 for x in imp if x > 0)}/{len(imp)}")
    dif = st.mean(todas) - st.mean(imp)
    se = math.sqrt(st.variance(todas) / len(todas) + st.variance(imp) / len(imp))
    print(f"     Pares menos impares: {dif:+.2f} pts (t de Welch {dif / se:+.2f})")

    # ---- (iii) 2026: lo que ya se observa ----------------------------------------------------------
    tau = eleccion(2026)
    i = indice(fechas, tau)
    if i is None:  # tau aún no llega: índice virtual = último día + hábiles que faltan
        faltan = 0
        d = fechas[-1] + dt.timedelta(days=1)
        while d < tau:
            if d.weekday() < 5:
                faltan += 1
            d += dt.timedelta(days=1)
        i = len(fechas) + faltan
    obs = vix[i - 20:]  # tratamiento observado hasta hoy
    k = len(obs)
    a26 = rms(vix[i - 41:i - 21])
    print(f"\n(iii) 2026 (tau {tau}): {k} de 20 días del tratamiento observados (último {fechas[-1]}); "
          f"IV_b parcial {rms(obs):.2f}, IV_a {a26:.2f}, b_parcial − a {rms(obs) - a26:+.2f}")
    comp = []
    for y in filas:
        j = indice(fechas, eleccion(y))
        comp.append(rms(vix[j - 20:j - 20 + k]) - rms(vix[j - 41:j - 21]))
    m, t, med = resumen(comp)
    pct = sum(1 for x in comp if x <= rms(obs) - a26) / len(comp)
    print(f"     Histórico, mismo tramo parcial (b_parcial − a), 1990-2024: media {m:+.2f}, mediana {med:+.2f}; "
          f"2026 queda en el percentil {100 * pct:.0f}")

    # ---- BTC con DVOL ------------------------------------------------------------------------------
    dv = {dt.date.fromisoformat(d): c for d, c in f["dvol_1d"]}
    print("\n(i-b) IVD con el DVOL de BTC (días naturales)")
    for anio in (2022, 2024):
        r = ivd_naturales(dv, eleccion(anio))
        if r:
            d, b, a, c = r
            print(f" {anio}: IV_b {b:.2f}  IV_a {a:.2f}  IV_c {c:.2f}  IVD {d:+.2f} ({100 * d / ((a + c) / 2):+.1f}%)"
                  + ("  [contaminado: quiebra de FTX 8-11-nov-2022]" if anio == 2022 else ""))
    nul_b = []
    t0 = min(dv) + dt.timedelta(days=52)
    d = t0
    while d <= max(dv) - dt.timedelta(days=21):
        if all(abs((d - eleccion(y)).days) > 60 for y in (2022, 2024, 2026)):
            r = ivd_naturales(dv, d)
            if r:
                nul_b.append(r[0])
        d += dt.timedelta(days=1)
    print(f" Nula DVOL (días a > 60 de una elección): n={len(nul_b)}, media {st.mean(nul_b):+.2f}, "
          f"desv. {st.stdev(nul_b):.2f}; percentil del IVD 2024: "
          f"{100 * sum(1 for x in nul_b if x <= ivd_naturales(dv, eleccion(2024))[0]) / len(nul_b):.0f}")
    hoy = max(dv)
    obs_b = [dv[tau + dt.timedelta(days=k)] for k in range(-20, 0) if tau + dt.timedelta(days=k) in dv]
    a_b = rms([dv[tau + dt.timedelta(days=k)] for k in range(-51, -31) if tau + dt.timedelta(days=k) in dv])
    print(f" 2026: {len(obs_b)} de 20 días observados (último {hoy}); IV_b parcial {rms(obs_b):.2f}, IV_a {a_b:.2f}, "
          f"b_parcial − a {rms(obs_b) - a_b:+.2f}")

    # ---- (v) Pendiente put por vencimiento (SlopeD transversal) ------------------------------------
    print("\n(v) Pendiente de KPV en la cadena de BTC: regresión de IV (decimal) sobre Δ de puts con "
          "−0.5 < Δ < −0.1 y OI > 0")
    t_foto = max(x["creation_timestamp"] for x in f["cadena"])
    print("  venc.     días  n   pendiente  IV(Δ−0.10)−IV(Δ−0.50) pts   IV ATM(0.4<|Δ|<0.5)")
    for v in VENC:
        filas_v = []
        for x in f["cadena"]:
            p = x["instrument_name"].split("-")
            if p[1] != v or p[3] != "P" or not x["mark_iv"] or x["open_interest"] <= 0:
                continue
            T = (f["vencimientos_ms"][v] - t_foto) / 1000 / 86400 / 365
            s = x["mark_iv"] / 100
            dlt = delta_put(x["underlying_price"], float(p[2]), s, T)
            filas_v.append((dlt, s))
        atm = [s for d_, s in filas_v if -0.5 < d_ < -0.4]
        otm = [(d_, s) for d_, s in filas_v if -0.5 < d_ < -0.1]
        if len(otm) < 3:
            continue
        mx, my = st.mean(d_ for d_, _ in otm), st.mean(s for _, s in otm)
        b = sum((d_ - mx) * (s - my) for d_, s in otm) / sum((d_ - mx) ** 2 for d_, _ in otm)
        dias = T * 365
        print(f"  {v:8s} {dias:5.2f} {len(otm):2d}   {b:+.4f}    {100 * b * 0.4:+6.2f}"
              f"                     {100 * math.sqrt(st.mean(s * s for s in atm)) if atm else float('nan'):6.2f}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "descargar":
        descargar()
    analizar(json.load(open(FOTO)))
