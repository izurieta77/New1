#!/usr/bin/env python3
"""AC-16-R10, ejecucion B (independiente, segunda fuente).

Filtro de tendencia SMA con banda sobre BTC-USD (Yahoo Finance chart v8, diario UTC).
Escrito desde cero, solo biblioteca estandar. No usa codigo de la ejecucion A.

Uso:  python3 -I b.py [ruta_json_yahoo]
Salida: tablas en stdout y resultados_b.json junto a este archivo.

Convenciones (declaradas en README.md):
- Cierre del dia t = campo close de la barra Yahoo con fecha t (dia UTC; cierra 23:59:59 UTC,
  equivalente a la vela Binance con fecha de apertura t que cierra 00:00 UTC de t+1).
- Se descarta la barra del dia de descarga (2026-10-12) porque esta incompleta.
- SMA_N(t) = media simple de los N cierres disponibles que terminan en t (incluye t).
- Primera senal valida: primer dia con N cierres. Antes de ese dia y en ese dia la cartera esta en efectivo.
- Estado inicial: en efectivo; se entra solo con senal de entrada (cierre > SMA*(1+b)).
  Despues: si invertido y cierre < SMA*(1-b) -> salir; si fuera y cierre > SMA*(1+b) -> entrar.
  Desigualdades estrictas; la banda no se redondea.
- Ejecucion t+1: la orden decidida con el cierre de t se ejecuta al cierre de t+1; el rendimiento del
  dia t+1 (cierre t -> cierre t+1) lo recibe la posicion anterior. Ejecucion t: se ejecuta al cierre de t.
- Costo 0.15% por lado: la equidad se multiplica por (1-0.0015) en cada compra o venta.
  Efectivo rinde 0. No se liquida la posicion al final (valuacion a mercado).
- Comprar y mantener: compra al cierre del dia de inicio (paga 0.15% una vez), sin venta final.
- Metricas: CAGR con dias calendario/365; vol = desv. est. muestral de rend. diarios * sqrt(365);
  Sharpe = media diaria*365 / vol (rf=0); MDD sobre la equidad diaria incluyendo el valor inicial.
- Operaciones = viajes redondos = numero de salidas (ventas) ejecutadas en la ventana; tambien se
  reportan lados (compras + ventas).
- Salida en falso: venta ejecutada a precio P_v en fecha d_v, seguida de una compra ejecutada en
  fecha d_c con d_c - d_v <= 30 dias calendario y precio P_c > P_v. Fraccion = falsas / ventas.
"""
import datetime as dt
import hashlib
import json
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RUTA_DEF = os.path.join(AQUI, "datos", "yahoo_BTC-USD_1d.json")
FECHA_DESCARGA = dt.date(2026, 10, 12)
COSTO = 0.0015
# Primer dia con 200 cierres de BTCUSDT en Binance (velas desde 2017-08-17, sin huecos):
# 2017-08-17 + 199 dias = 2018-03-04 (solo se usaron las fechas de Binance, no sus precios).
INICIO_COMUN = dt.date(2018, 3, 4)

CONFIGS = [
    ("principal_sma200_b3_t+1", 200, 0.03, 1),
    ("sin_banda_sma200_t+1", 200, 0.0, 1),
    ("banda5_sma200_t+1", 200, 0.05, 1),
    ("sma100_b3_t+1", 100, 0.03, 1),
    ("mismo_dia_sma200_b3_t", 200, 0.03, 0),
]


def cargar(ruta):
    with open(ruta, "rb") as f:
        crudo = f.read()
    sha = hashlib.sha256(crudo).hexdigest()
    j = json.loads(crudo)
    r = j["chart"]["result"][0]
    ts = r["timestamp"]
    cl = r["indicators"]["quote"][0]["close"]
    fechas, cierres, nulos = [], [], 0
    for t, c in zip(ts, cl):
        f = dt.datetime.fromtimestamp(t, dt.timezone.utc).date()
        if f >= FECHA_DESCARGA:
            continue
        if c is None or not (c > 0):
            nulos += 1
            continue
        fechas.append(f)
        cierres.append(float(c))
    # Dias faltantes (huecos en el calendario)
    faltan = 0
    for a, b in zip(fechas, fechas[1:]):
        faltan += (b - a).days - 1
    return fechas, cierres, sha, nulos, faltan, r["meta"].get("dataGranularity")


def sma(cierres, n):
    out = [None] * len(cierres)
    s = 0.0
    for i, c in enumerate(cierres):
        s += c
        if i >= n:
            s -= cierres[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


def simular(fechas, cierres, n, banda, rezago, i0):
    """Corre la regla empezando (en efectivo) en el indice i0 (dia de la primera senal valida
    de la ventana). Devuelve equidad diaria desde i0, operaciones y posiciones."""
    m = sma(cierres, n)
    assert m[i0] is not None, "i0 sin SMA valida"
    # estado deseado al cierre de cada dia (decidido con el cierre de ese dia)
    estado = {}
    s = 0
    for i in range(i0, len(cierres)):
        c, mm = cierres[i], m[i]
        if s == 0 and c > mm * (1 + banda):
            s = 1
        elif s == 1 and c < mm * (1 - banda):
            s = 0
        estado[i] = s
    # posicion efectiva tras el cierre del dia i (ya ejecutadas las ordenes de ese cierre)
    pos = {}
    for i in range(i0, len(cierres)):
        if rezago == 0:
            pos[i] = estado[i]
        else:
            pos[i] = estado[i - 1] if i - 1 >= i0 else 0
    eq = [1.0]
    ops = []  # (fecha, 'C'/'V', precio)
    previo = 0
    # dia i0: posible ejecucion al cierre de i0 (solo con rezago 0)
    if pos[i0] != previo:
        eq[0] *= (1 - COSTO)
        ops.append((fechas[i0], "C" if pos[i0] else "V", cierres[i0]))
    previo = pos[i0]
    for i in range(i0 + 1, len(cierres)):
        v = eq[-1]
        if previo == 1:
            v *= cierres[i] / cierres[i - 1]
        if pos[i] != previo:
            v *= (1 - COSTO)
            ops.append((fechas[i], "C" if pos[i] else "V", cierres[i]))
        previo = pos[i]
        eq.append(v)
    return eq, ops


def comprar_mantener(cierres, i0):
    eq = [1.0 - COSTO]
    for i in range(i0 + 1, len(cierres)):
        eq.append(eq[-1] * cierres[i] / cierres[i - 1])
    return eq


def metricas(fechas_v, eq_v, ops, ini, fin):
    """fechas_v/eq_v: equidad diaria de la corrida. Se evalua la ventana [ini, fin] tomando como
    valor inicial la equidad al cierre del ultimo dia anterior a ini (o el primero si no hay)."""
    idx = [k for k, f in enumerate(fechas_v) if ini <= f <= fin]
    k0 = idx[0] - 1 if idx[0] > 0 else idx[0]
    k1 = idx[-1]
    serie = eq_v[k0:k1 + 1]
    rend = [serie[j] / serie[j - 1] - 1 for j in range(1, len(serie))]
    dias = (fechas_v[k1] - fechas_v[k0]).days
    cagr = (serie[-1] / serie[0]) ** (365.0 / dias) - 1
    mu = sum(rend) / len(rend)
    var = sum((x - mu) ** 2 for x in rend) / (len(rend) - 1)
    vol = math.sqrt(var) * math.sqrt(365)
    sharpe = mu * 365 / vol if vol > 0 else float("nan")
    pico, mdd = serie[0], 0.0
    for v in serie:
        pico = max(pico, v)
        mdd = min(mdd, v / pico - 1)
    ventas = [o for o in ops if o[1] == "V" and fechas_v[k0] < o[0] <= fechas_v[k1]]
    lados = [o for o in ops if fechas_v[k0] < o[0] <= fechas_v[k1]]
    falsas = 0
    for (fv, _, pv) in ventas:
        comp = [o for o in ops if o[1] == "C" and o[0] > fv]
        if comp:
            fc, _, pc = comp[0]
            if (fc - fv).days <= 30 and pc > pv:
                falsas += 1
    dias_inv = None
    return {
        "desde": fechas_v[k0].isoformat(), "hasta": fechas_v[k1].isoformat(),
        "cagr": cagr, "vol": vol, "sharpe": sharpe, "mdd": mdd,
        "viajes": len(ventas), "lados": len(lados), "falsas": falsas,
        "pct_falsas": (falsas / len(ventas)) if ventas else None,
        "multiplo": serie[-1] / serie[0],
    }


def correr(fechas, cierres, i0, ventanas):
    fv = fechas[i0:]
    res = {}
    bh = comprar_mantener(cierres, i0)
    res["comprar_y_mantener"] = {w: metricas(fv, bh, [], a, b) for w, (a, b) in ventanas.items()}
    detalle = {}
    for nombre, n, banda, rez in CONFIGS:
        eq, ops = simular(fechas, cierres, n, banda, rez, i0)
        res[nombre] = {w: metricas(fv, eq, ops, a, b) for w, (a, b) in ventanas.items()}
        detalle[nombre] = [(o[0].isoformat(), o[1], round(o[2], 2)) for o in ops]
    return res, detalle


def fmt(res, ventana):
    lin = ["| Configuracion | Desde | Hasta | CAGR | Vol | Sharpe | MDD | Viajes | Salidas en falso |",
           "|---|---|---|---:|---:|---:|---:|---:|---:|"]
    for nombre, d in res.items():
        m = d[ventana]
        pf = "-" if m["pct_falsas"] is None else f"{m['falsas']}/{m['viajes']} ({m['pct_falsas']*100:.0f}%)"
        if nombre == "comprar_y_mantener":
            pf, via = "-", "-"
        else:
            via = str(m["viajes"])
        lin.append(f"| {nombre} | {m['desde']} | {m['hasta']} | {m['cagr']*100:.1f}% | {m['vol']*100:.1f}% | "
                   f"{m['sharpe']:.2f} | {m['mdd']*100:.1f}% | {via} | {pf} |")
    return "\n".join(lin)


def veredicto(res, ventana):
    bh = res["comprar_y_mantener"][ventana]
    p = res["principal_sma200_b3_t+1"][ventana]
    mejora_mdd = (p["mdd"] - bh["mdd"]) * 100  # pp, positivo = mejor
    return {
        "mejora_mdd_pp": mejora_mdd,
        "dif_cagr_pp": (p["cagr"] - bh["cagr"]) * 100,
        "dif_sharpe": p["sharpe"] - bh["sharpe"],
        "refuta": (mejora_mdd < 25) or (p["sharpe"] < bh["sharpe"]),
        "cagr_dentro_15pp": (bh["cagr"] - p["cagr"]) * 100 <= 15,
    }


def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else RUTA_DEF
    fechas, cierres, sha, nulos, faltan, gran = cargar(ruta)
    assert gran == "1d", gran
    print(f"Fuente: {ruta}\nsha256: {sha}\nGranularidad: {gran}  Observaciones: {len(cierres)}  "
          f"{fechas[0]} a {fechas[-1]}  Nulos descartados: {nulos}  Dias faltantes: {faltan}")
    fin = fechas[-1]
    salida = {"sha256": sha, "n_obs": len(cierres), "primera_fecha": fechas[0].isoformat(),
              "ultima_fecha": fin.isoformat(), "nulos": nulos, "dias_faltantes": faltan}

    # (a) Periodo completo: cada configuracion empieza en su propia primera senal valida
    #     (SMA200 -> indice 199; SMA100 -> 99). Para comparar en igualdad, todas las configuraciones
    #     y comprar y mantener se evaluan desde la primera senal valida de SMA200; la SMA100 tambien
    #     arranca ahi (en efectivo) para no darle un periodo distinto.
    i0 = 199
    ventanas_a = {
        "completo": (fechas[i0], fin),
        "2015-2016": (dt.date(2015, 1, 1), dt.date(2016, 12, 31)),
        "2017-2020": (dt.date(2017, 1, 1), dt.date(2020, 12, 31)),
        "2021-hoy": (dt.date(2021, 1, 1), fin),
    }
    res_a, det_a = correr(fechas, cierres, i0, ventanas_a)

    # (b) Periodo comun con Binance: arranque en efectivo el 2018-03-04 (SMA con historia Yahoo)
    j0 = fechas.index(INICIO_COMUN)
    ventanas_b = {
        "comun": (INICIO_COMUN, fin),
        "2018-2020": (INICIO_COMUN, dt.date(2020, 12, 31)),
        "2021-hoy": (dt.date(2021, 1, 1), fin),
    }
    res_b, det_b = correr(fechas, cierres, j0, ventanas_b)

    for titulo, res, vs in (("(a) PERIODO COMPLETO YAHOO", res_a, ventanas_a),
                            ("(b) PERIODO COMUN CON BINANCE", res_b, ventanas_b)):
        for w in vs:
            print(f"\n### {titulo} - {w}\n")
            print(fmt(res, w))
    vered = {
        "completo": veredicto(res_a, "completo"),
        "comun": veredicto(res_b, "comun"),
        "a_2017-2020": veredicto(res_a, "2017-2020"),
        "a_2021-hoy": veredicto(res_a, "2021-hoy"),
        "b_2018-2020": veredicto(res_b, "2018-2020"),
        "b_2021-hoy": veredicto(res_b, "2021-hoy"),
    }
    print("\n### Criterio de refutacion (regla principal vs comprar y mantener)\n")
    for k, v in vered.items():
        print(f"{k}: mejora MDD {v['mejora_mdd_pp']:.1f} pp; dif CAGR {v['dif_cagr_pp']:.1f} pp; "
              f"dif Sharpe {v['dif_sharpe']:+.2f}; refuta={v['refuta']}; CAGR dentro de 15 pp={v['cagr_dentro_15pp']}")
    print("\n### Operaciones regla principal (periodo comun)")
    for o in det_b["principal_sma200_b3_t+1"]:
        print(o)
    salida.update({"periodo_completo": res_a, "periodo_comun": res_b, "veredicto": vered,
                   "operaciones_completo": det_a, "operaciones_comun": det_b})
    with open(os.path.join(AQUI, "resultados_b.json"), "w") as f:
        json.dump(salida, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
