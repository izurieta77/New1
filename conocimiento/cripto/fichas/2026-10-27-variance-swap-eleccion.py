"""Variance swap propio (fórmula del VIX/DVOL) sobre la cadena de Deribit y prima de evento de la
elección intermedia de EUA (martes 3-nov-2026).

Ficha: 2026-10-27-variance-swap-eleccion.md (misma carpeta).

Uso (rutas relativas a este archivo):
    python3 -I 2026-10-27-variance-swap-eleccion.py descargar   # baja foto nueva y la guarda en -datos.json
    python3 -I 2026-10-27-variance-swap-eleccion.py             # analiza la foto guardada

Convenciones:
- Precio de la opción en USD a plazo = mark_price (BTC) × F, con F = underlying_price del vencimiento
  (Deribit liquida opciones inversas: el pago en BTC vale el pago en USD al vencimiento).
- σ² = (2/T) Σ ΔK/K² · Q(K) − (1/T)(F/K0 − 1)², T en años de 365 días (CBOE, white paper del VIX;
  Deribit: "use the variance swap methodology").
- Varianza total w = σ² T; varianza a plazo entre vencimientos = Δw/ΔT.
- Histórico: Binance BTCUSDT 8h, ventana martes 08:00 UTC → miércoles 08:00 UTC (los resultados de la
  elección llegan entre ~00:00 y ~08:00 UTC del miércoles); Yahoo BTC-USD 1d para 2014 y 2016.
"""
import datetime as dt
import json
import math
import os
import statistics as st
import sys
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "2026-10-27-variance-swap-eleccion-datos.json")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
UTC = dt.timezone.utc

# Elecciones generales de EUA (martes después del primer lunes de noviembre, 2 U.S.C. § 7).
ELECCIONES_BINANCE = ["2018-11-06", "2020-11-03", "2022-11-08", "2024-11-05"]
ELECCIONES_YAHOO = ["2014-11-04", "2016-11-08", "2018-11-06", "2020-11-03", "2022-11-08", "2024-11-05"]


def _get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)


def descargar():
    ahora = int(dt.datetime.now(UTC).timestamp() * 1000)
    d = {
        "descargado_utc": dt.datetime.now(UTC).isoformat(timespec="seconds"),
        "cadena": _get("https://www.deribit.com/api/v2/public/get_book_summary_by_currency?currency=BTC&kind=option")["result"],
        "indice": _get("https://www.deribit.com/api/v2/public/get_index_price?index_name=btc_usd")["result"],
        "dvol": _get("https://www.deribit.com/api/v2/public/get_volatility_index_data?currency=BTC"
                     f"&start_timestamp={ahora - 3 * 3600 * 1000}&end_timestamp={ahora}&resolution=60")["result"]["data"],
        "binance_8h": {},
        "yahoo_1d": {},
    }
    for e in ELECCIONES_BINANCE:
        t0 = int((dt.datetime.fromisoformat(e).replace(tzinfo=UTC) - dt.timedelta(days=32)).timestamp() * 1000)
        d["binance_8h"][e] = _get("https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=8h"
                                  f"&startTime={t0}&limit=120")
    for e in ELECCIONES_YAHOO:
        f = dt.datetime.fromisoformat(e).replace(tzinfo=UTC)
        p1, p2 = int((f - dt.timedelta(days=45)).timestamp()), int((f + dt.timedelta(days=5)).timestamp())
        r = _get(f"https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD?interval=1d&period1={p1}&period2={p2}")
        r = r["chart"]["result"][0]
        d["yahoo_1d"][e] = list(zip(r["timestamp"], r["indicators"]["quote"][0]["close"]))
    with open(DATOS, "w") as fh:
        json.dump(d, fh)
    print("guardado", DATOS, len(d["cadena"]), "opciones")


# ---------------------------------------------------------------- variance swap por vencimiento
def _ncdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def vencimiento_ts(cod):
    return dt.datetime.strptime(cod, "%d%b%y").replace(hour=8, tzinfo=UTC)


def cadena_por_vencimiento(cadena):
    out = {}
    for o in cadena:
        _, cod, k, tipo = o["instrument_name"].split("-")
        out.setdefault(cod, []).append((float(k), tipo, o))
    return out


def var_swap(opciones, t_foto, cod, precio="mark", delta_min=0.0):
    """Devuelve dict con T, F, K0, σ_VS, σ_ATM y número de strikes usados."""
    T = (vencimiento_ts(cod) - t_foto).total_seconds() / (365 * 86400)
    F = st.median(o["underlying_price"] for _, _, o in opciones)
    strikes = sorted({k for k, _, _ in opciones})
    tabla = {(k, t): o for k, t, o in opciones}
    K0 = max([k for k in strikes if k <= F] or [strikes[0]])

    def q(k, t):
        o = tabla.get((k, t))
        if o is None:
            return None
        if precio == "mark":
            p = o["mark_price"]
        else:  # punto medio solo si hay postura de compra
            if not o.get("bid_price") or not o.get("ask_price"):
                return None
            p = (o["bid_price"] + o["ask_price"]) / 2
        if delta_min and o.get("mark_iv"):
            s = o["mark_iv"] / 100 * math.sqrt(T)
            d1 = (math.log(F / k) + s * s / 2) / s
            dl = _ncdf(d1) if t == "C" else _ncdf(d1) - 1
            if abs(dl) < delta_min:
                return None
        return p * F

    usados = []  # (K, Q)
    # puts debajo de K0, de K0 hacia abajo, cortando tras dos ceros consecutivos (regla CBOE)
    ceros = 0
    for k in sorted([k for k in strikes if k < K0], reverse=True):
        v = q(k, "P")
        if not v:
            ceros += 1
            if ceros >= 2:
                break
            continue
        ceros = 0
        usados.append((k, v))
    ceros = 0
    for k in sorted([k for k in strikes if k > K0]):
        v = q(k, "C")
        if not v:
            ceros += 1
            if ceros >= 2:
                break
            continue
        ceros = 0
        usados.append((k, v))
    vp, vc = q(K0, "P"), q(K0, "C")
    if vp and vc:
        usados.append((K0, (vp + vc) / 2))
    usados.sort()
    ks = [k for k, _ in usados]
    suma = 0.0
    for i, (k, v) in enumerate(usados):
        if len(ks) == 1:
            dk = 0
        elif i == 0:
            dk = ks[1] - ks[0]
        elif i == len(ks) - 1:
            dk = ks[-1] - ks[-2]
        else:
            dk = (ks[i + 1] - ks[i - 1]) / 2
        suma += dk / k ** 2 * v
    var = 2 / T * suma - (F / K0 - 1) ** 2 / T  # Q ya está en USD a plazo (sin factor e^{rT})
    # IV ATM interpolada en F (total de varianza lineal en ln K)
    ivs = sorted((k, o["mark_iv"]) for k, t, o in opciones if t == "C" and o.get("mark_iv"))
    atm = None
    for (k1, v1), (k2, v2) in zip(ivs, ivs[1:]):
        if k1 <= F <= k2:
            a = (math.log(F) - math.log(k1)) / (math.log(k2) - math.log(k1))
            atm = math.sqrt(((1 - a) * v1 ** 2 + a * v2 ** 2))
    return {"cod": cod, "T": T, "dias": T * 365, "F": F, "K0": K0, "n": len(usados),
            "rango": (ks[0], ks[-1]) if ks else None,
            "vs": math.sqrt(max(var, 0)) * 100, "atm": atm, "w": max(var, 0) * T,
            "w_atm": (atm / 100) ** 2 * T if atm else None}


def interp_30d(a, b):
    """Interpolación del VIX: varianza total lineal en el tiempo hasta 30 días."""
    N30 = 30 / 365
    w = a["w"] + (b["w"] - a["w"]) * (N30 - a["T"]) / (b["T"] - a["T"])
    return math.sqrt(w / N30) * 100


# ---------------------------------------------------------------- histórico de elecciones
def evento_binance(kl, fecha):
    """r = ln(open 8h miércoles 08:00 / open 8h martes 08:00); base: 20 ventanas 08→08 previas."""
    op = {dt.datetime.fromtimestamp(k[0] / 1000, UTC): float(k[1]) for k in kl}
    t0 = dt.datetime.fromisoformat(fecha).replace(hour=8, tzinfo=UTC)
    r_ev = math.log(op[t0 + dt.timedelta(days=1)] / op[t0])
    base = [math.log(op[t0 - dt.timedelta(days=i - 1)] / op[t0 - dt.timedelta(days=i)]) for i in range(1, 21)]
    return r_ev, base


def evento_yahoo(serie, fecha):
    """r = ln(cierre del miércoles / cierre del martes) (velas UTC de Yahoo); base: 20 días previos."""
    xs = [(dt.datetime.fromtimestamp(t, UTC).date(), c) for t, c in serie if c]
    dd = {d: c for d, c in xs}
    e = dt.date.fromisoformat(fecha)
    r_ev = math.log(dd[e + dt.timedelta(days=1)] / dd[e])
    base = [math.log(dd[e - dt.timedelta(days=i - 1)] / dd[e - dt.timedelta(days=i)]) for i in range(1, 21)]
    return r_ev, base


def comprobar():
    """Prueba: cadena sintética Black-76 con vol plana 40%; el VS debe dar ~40 y la ATM 40."""
    F, sig, dias = 80000.0, 0.40, 9.0
    t_foto = dt.datetime(2026, 1, 1, 8, tzinfo=UTC)
    cod = "10JAN26"
    T = dias / 365
    ops = []
    for k in range(40000, 140001, 1000):
        k = float(k)
        s = sig * math.sqrt(T)
        d1 = (math.log(F / k) + s * s / 2) / s
        d2 = d1 - s
        c = F * _ncdf(d1) - k * _ncdf(d2)
        p = c - (F - k)
        for t, v in (("C", c), ("P", p)):
            ops.append((k, t, {"mark_price": v / F, "underlying_price": F, "mark_iv": sig * 100,
                               "bid_price": v / F, "ask_price": v / F}))
    r = var_swap(ops, t_foto, cod)
    assert abs(r["vs"] - 40) < 0.3 and abs(r["atm"] - 40) < 1e-6, r
    print(f"Comprobación sintética (vol plana 40%, 9 días): VS {r['vs']:.2f}, ATM {r['atm']:.2f} → OK")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "descargar":
        descargar()
    comprobar()
    d = json.load(open(DATOS))
    t_foto = dt.datetime.fromisoformat(d["descargado_utc"])
    dvol = d["dvol"][-1]
    print(f"Foto Deribit {d['descargado_utc']}  índice {d['indice']['index_price']}  DVOL (vela 1m) {dvol[4]}")
    por = cadena_por_vencimiento(d["cadena"])
    cods = sorted(por, key=vencimiento_ts)
    res = {}
    print("\nA. Variance swap por vencimiento (mark; entre paréntesis, punto medio con postura y filtro |Δ|≥5%)")
    print(f"{'venc':>8} {'días':>6} {'F':>9} {'n':>3} {'VS':>6} {'ATM':>6} {'VS−ATM':>7} {'VS mid':>7} {'VS Δ5':>6}")
    for c in cods:
        if vencimiento_ts(c) <= t_foto:
            continue
        r = var_swap(por[c], t_foto, c)
        rm = var_swap(por[c], t_foto, c, precio="mid")
        rd = var_swap(por[c], t_foto, c, delta_min=0.05)
        res[c] = r
        r["vs_mid"], r["vs_d5"] = rm["vs"], rd["vs"]
        print(f"{c:>8} {r['dias']:6.2f} {r['F']:9.0f} {r['n']:3d} {r['vs']:6.2f} {r['atm'] or float('nan'):6.2f} "
              f"{r['vs'] - (r['atm'] or float('nan')):7.2f} {rm['vs']:7.2f} {rd['vs']:6.2f}")
    # 30 días
    orden = [res[c] for c in cods if c in res]
    a = max([x for x in orden if x["dias"] <= 30], key=lambda x: x["dias"])
    b = min([x for x in orden if x["dias"] > 30], key=lambda x: x["dias"])
    v30 = interp_30d(a, b)
    print(f"\nVS 30 días propio (interp. {a['cod']}–{b['cod']}): {v30:.2f}  contra DVOL {dvol[4]:.2f}  "
          f"(dif. {v30 - dvol[4]:+.2f} pts)")
    for clave in ("vs_mid", "vs_d5"):
        aa = dict(a, w=(a[clave] / 100) ** 2 * a["T"])
        bb = dict(b, w=(b[clave] / 100) ** 2 * b["T"])
        print(f"   variante {clave}: {interp_30d(aa, bb):.2f}")

    print("\nB. Varianza a plazo por tramo (vol anualizada; σ del tramo en %)")
    tramos = []
    prev = {"cod": "foto", "T": 0.0, "w": 0.0, "w_atm": 0.0}
    for r in orden:
        dT = r["T"] - prev["T"]
        fv = (r["w"] - prev["w"]) / dT
        fa = (r["w_atm"] - prev["w_atm"]) / dT
        tramos.append({"de": prev["cod"], "a": r["cod"], "dT": dT, "fv": fv, "fa": fa,
                       "dw": r["w"] - prev["w"], "dwa": r["w_atm"] - prev["w_atm"]})
        print(f"{prev['cod']:>8}→{r['cod']:<8} {dT * 365:6.2f} d  VS {math.sqrt(max(fv, 0)) * 100:6.2f} "
              f"(σ {math.sqrt(max(r['w'] - prev['w'], 0)) * 100:5.2f}%)   ATM {math.sqrt(max(fa, 0)) * 100:6.2f} "
              f"(σ {math.sqrt(max(r['w_atm'] - prev['w_atm'], 0)) * 100:5.2f}%)")
        prev = r
    T = {(x["de"], x["a"]): x for x in tramos}
    el = T[("31OCT26", "6NOV26")]
    base = T[("6NOV26", "13NOV26")]
    out = {}
    for nom, kw, kd in (("VS", "fv", "dw"), ("ATM", "fa", "dwa")):
        extra = el[kd] - base[kw] * el["dT"]
        out[nom] = extra
        print(f"\nElección ({nom}): tramo 31-oct→6-nov vol a plazo {math.sqrt(el[kw]) * 100:.2f} contra base 6→13-nov "
              f"{math.sqrt(base[kw]) * 100:.2f}; varianza extra {extra * 1e4:.2f} %² → salto 1σ "
              f"{math.sqrt(max(extra, 0)) * 100:.2f}%")
        dia_base = base[kw] / 365
        print(f"   razón (día de elección / día base) = {(dia_base + max(extra, 0)) / dia_base:.2f}")
    fomc = T[("28OCT26", "29OCT26")]
    for nom, kw, kd in (("VS", "fv", "dw"), ("ATM", "fa", "dwa")):
        b1 = T[("30OCT26", "31OCT26")][kw]
        print(f"FOMC ({nom}): tramo 28→29 σ {math.sqrt(fomc[kd]) * 100:.2f}%  razón vs 30→31 {fomc[kw] / b1:.2f}"
              f"  vs 6→13-nov {fomc[kw] / base[kw]:.2f}")

    print("\nC. Histórico: movimiento del día de resultados contra los 20 días previos")
    filas = []
    for e in ELECCIONES_BINANCE:
        r, b = evento_binance(d["binance_8h"][e], e)
        filas.append(("Binance 8h", e, r, b))
    for e in ELECCIONES_YAHOO:
        r, b = evento_yahoo(d["yahoo_1d"][e], e)
        filas.append(("Yahoo 1d", e, r, b))
    razones_b, razones_y = [], []
    for fu, e, r, b in filas:
        s = math.sqrt(sum(x * x for x in b) / len(b))
        rz = r * r / (s * s)
        (razones_b if fu.startswith("Bin") else razones_y).append(rz)
        print(f"{fu:>10} {e}  r {r * 100:+6.2f}%  σ previa {s * 100:5.2f}%  |r|/σ {abs(r) / s:4.2f}  r²/σ² {rz:5.2f}")
    print(f"Media r²/σ²: Binance (4) {st.mean(razones_b):.2f}; Yahoo (6) {st.mean(razones_y):.2f};"
          f" mediana Yahoo {st.median(razones_y):.2f}")

    # Probabilidad para el pronóstico: |r| del día 3→4-nov (08:00→08:00) > umbral
    print("\nD. P(|ln(open 4-nov 08:00 / open 3-nov 08:00)| > u) con σ del día de elección implícita")
    s_base_dia = math.sqrt(base["fv"] / 365)
    s_el = math.sqrt(base["fv"] / 365 + max(out["VS"], 0))
    for u in (0.02, 0.025, 0.03):
        p_imp = 2 * (1 - _ncdf(u / s_el))
        p_base = 2 * (1 - _ncdf(u / s_base_dia))
        print(f"   u {u * 100:.1f}%: normal con σ elección {s_el * 100:.2f}% → {p_imp:.2f};"
              f" con σ base {s_base_dia * 100:.2f}% → {p_base:.2f}")
    # frecuencia empírica: días 08→08 de los 20 previos de cada elección de Binance, escalados a su σ
    z = []
    for fu, e, r, b in filas:
        if fu.startswith("Bin"):
            s = math.sqrt(sum(x * x for x in b) / len(b))
            z += [abs(x) / s for x in b]
    for u in (0.02, 0.025, 0.03):
        k = u / s_base_dia
        print(f"   empírica (80 días base escalados): P(|z| > {k:.2f}) = {sum(1 for x in z if x > k) / len(z):.2f}")


if __name__ == "__main__":
    main()
