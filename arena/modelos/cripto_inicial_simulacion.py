#!/usr/bin/env python3
"""Cartera cripto inicial de la cuenta arena-claude-binance: K1-K4 a 4 meses, en MXN.

Pregunta del comite cripto (viernes 25-sep-2026, ~21:00 UTC): que cartera inicial de la cuenta Binance
(10,000 MXN, solo spot, universo BTC y ETH, ejecucion manual del dueno) maximiza la probabilidad de que la
cuenta COMBINADA (20,000 GBM + 10,000 Binance) termine primero frente a ChatGPT y Grok, sin que el tope de
perdida de 5,000 MXN (perfiles_riesgo.cripto_binance de config/parametros.json) sea probable.
Temporada: 28-sep-2026 a 28-ene-2027 = 122 dias corridos (cripto opera 24/7).

Uso (desde cualquier directorio):
    python3 arena/modelos/cripto_inicial_simulacion.py                   # 20,000 trayectorias por metodo
    python3 arena/modelos/cripto_inicial_simulacion.py --caminos 4000    # corrida rapida
    python3 arena/modelos/cripto_inicial_simulacion.py --salida arena/modelos/salida_cripto_inicial.txt

CANDIDATAS (del comite; interpretaciones propias marcadas [I]):
  K1 100% BTC, comprar y mantener.
  K2 BTC/ETH 70/30, comprar y mantener, sin rebalanceo [I].
  K3 Filtro SMA200: 100% BTC si el cierre diario de BTC-USD (00:00 UTC) > promedio de sus ultimos 200 cierres
     diarios (200 dias corridos); si no, USDT [I: activo BTC, senal en USD]. Senal al cierre de t, ejecucion al
     cierre de t+1 [I: rezago de 1 dia por ejecucion manual]. Comision 0.1% por cambio.
  K4 55% BTC + 20% ETH + 25% USDT, con dos ordenes limite de compra de BTC por 12.5% del capital inicial cada
     una, a -15% y -25% del precio de entrada de BTC [I: se llenan si el minimo diario toca el limite, al precio
     limite o al cierre previo si ya estaba abajo].
  K0 100% USDT: solo referencia, no es candidata.

DATOS (corte duro CORTE = 24-sep-2026: la vela diaria del 25-sep de BTC/ETH seguia abierta al correr):
  * Yahoo Finance chart v8, interval=1d, period1=0: BTC-USD (desde 2014-09-17), ETH-USD (desde 2017-11-09),
    USDT-USD (control de paridad), MXN=X, SPY y QQQ (cierre ajustado). FRED DTB3 (T-bill 3m) y DEXMXUS (solo
    para verificar la alineacion del tipo de cambio).
  * ALINEACION DEL TIPO DE CAMBIO (verificado en esta corrida contra FRED DEXMXUS): la vela diaria de MXN=X con
    fecha de Londres L es, desde el 2-abr-2018, una foto a ~23:00 UTC del dia L-1 (open ~ close); antes era
    una vela completa que cerraba al final del dia L. Se define FX_fin(D) = USD/MXN al final del dia UTC D:
    vela L=D antes del cambio y vela L=D+1 despues. Asi empata con el cierre de BTC (00:00 UTC de D+1, 1 h
    despues) y con el de SPY (16:00 NY, ~3 h antes). Sabado y domingo sin vela: se arrastra el ultimo valor.
  * Tasas de hoy: T-bill DTB3 (ultimo dato de FRED) y CETES 28 = 6.15% (subasta Banxico 22-sep-2026, via
    cetes.app, fuente secundaria; mismo supuesto que arena/modelos/cartera_inicial_simulacion.py).

METODOS (rendimientos diarios conjuntos BTC, ETH, minimos intradia, USD/MXN, SPY y QQQ; calendario corrido):
  M1  Ventanas moviles reales de 122 dias, un inicio por dia, 2017-11-09 a 2026-05-25. M1c: solo inicios con
      BTC > SMA200 (regimen de hoy). Tramos: antes de 2021 (dentro de muestra de Detzel et al. 2021) y desde 2021.
  M2  Bootstrap estacionario (Politis y Romano 1994), bloque medio de 30 dias, de 2017-11-10 a 2026-09-24,
      deriva historica (in-sample). El primer bloque sale de dias con BTC > SMA200. La SMA arranca con los
      200 cierres reales al 24-sep-2026 y la entrada es al ultimo cierre real.
  M2r Igual que M2 con muestra 2022-01-01 a 2026-09-24 (regimen reciente, menor volatilidad).
  M3  Igual que M2 con deriva conservadora: BTC y ETH con el mismo Sharpe que el S&P (prima del S&P de 5%/anio
      sobre el T-bill, media aritmetica), deriva cambiaria cero. Recorte de ~60% frente a la deriva historica.
  M4  Igual que M3 pero prima cripto CERO (rendimiento aritmetico de BTC y ETH = T-bill). Cota pesimista.
  Rendimiento diario en USD de la pierna S&P = rf_hoy/365 + beta x (exceso historico diario sobre DTB3).
  En MXN: (1 + r_usd)(1 + r_fx) - 1. El USDT vale 1 USD (sin rendimiento: el perfil prohibe Earn y prestamos).

REGLAS SIMULADAS (perfil cripto_binance vigente, corregido el 25-sep-2026 en el commit c31a2c9; [I] = interpretacion):
  * Costos: MXN->USDT 0.2% [I: 0.1% de comision + 0.1% de desviacion frente al USD/MXN de Yahoo]; cada
    compra o venta spot 0.1% (dato del comite); cripto -> MXN 0.3%. Valuacion final a mercado (no se liquida).
  * Cortacircuitos sobre el valor en MXN al cierre diario, drawdown desde el maximo (el maximo arranca en 10,000):
    -20% -> exposicion BTC+ETH <= 50% del valor (vende a MXN); -30% -> <= 25%; -40% -> pausa 7 dias sin compras
    y <= 25%; -50% o valor <= 5,000 MXN (tope del dueno) -> todo a MXN y la cuenta queda parada el resto de la
    temporada. El tope de exposicion se libera al marcar un nuevo maximo [I: el perfil no define la liberacion;
    mismo criterio que cartera_inicial_simulacion.py]; al liberarse, K1/K2/K4 recompran con el MXN de los cortes.
    Las compras (reentrada de K3, ordenes de K4) nunca rebasan el tope vigente.
  * P(tocar x) se mide con cierres diarios; se reporta tambien la version con minimos intradia.
  * Cuenta combinada propia = pierna GBM + pierna Binance (K0-K4). Pierna GBM: (a) la cartera A que sello el comite
    de GBM (commit c24bb1b: 7 SPYM + 1 QQQM = 56.3% S&P + 27.1% Nasdaq-100 + 16.6% liquidez en MXN a tasa CETES
    [I]), y (b) las betas 1.30 y 1.45 al S&P que pidio el orquestador (costo 0.42%, arrastre del 3x de
    2.14%/anio sobre la fraccion apalancada). Sin cortacircuitos de GBM [I].
  * Rivales (no se conocen sus carteras) [I]: pierna GBM R1 beta 1 S&P, R2 50% S&P + 50% CETES o R3 50% TQQQ
    + 50% QQQ; pierna cripto C1 100% BTC, C2 60/40 BTC/ETH, C3 50% BTC + 50% USDT o C4 100% ETH. Comprar y
    mantener, sin cortacircuitos, con ruido idiosincratico N(0, 3 pp) en GBM y N(0, 5 pp) en cripto.
    Campos: F1 {R1+C2, R2+C3} (base), F2 {R1+C1, R3+C4} (agresivo), F3 {R1+C2, R1+C2} (clones),
    F4 {R2+C3, R2+C3} (conservadores). '1o' = combinada propia arriba de los dos rivales.
Todo es simulacion historica: no es pronostico ni recomendacion.
"""
from __future__ import annotations

import argparse
import io
import json
import math
import sys
import time
import urllib.parse
from contextlib import redirect_stdout
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from arena.investigacion.pantalla import meses_atras  # noqa: E402
from herramientas import estadistica, metricas  # noqa: E402
from herramientas.datos import UA_NAVEGADOR, URL_YAHOO, descargar, fred_serie  # noqa: E402
from herramientas.parametros import cargar_parametros  # noqa: E402

# ------------------------------------------------------------------ supuestos con fecha y fuente
CORTE = date(2026, 9, 24)                       # ultimo dia UTC completo de BTC/ETH
P2 = int(datetime(2026, 9, 26, tzinfo=timezone.utc).timestamp())
INICIO_TEMPORADA, FIN_TEMPORADA = date(2026, 9, 28), date(2027, 1, 28)
H = (FIN_TEMPORADA - INICIO_TEMPORADA).days     # 122 dias corridos
INICIO_MUESTRA = date(2017, 11, 10)             # primer rendimiento diario de ETH-USD
INICIO_RECIENTE = date(2022, 1, 1)
CORTE_PUBLICACION = date(2021, 1, 1)            # Detzel et al. (2021), Financial Management 50(1)
CAMBIO_FX = date(2018, 4, 2)                    # primera vela de MXN=X tipo "foto a las 23:00 UTC de L-1"
CAPITAL, CAPITAL_GBM = 10_000.0, 20_000.0
COMISION = 0.001                                # Binance spot, 0.1% por lado (dato del comite)
CONVERSION = 0.002                              # [I] MXN -> USDT
COSTO_GBM, COSTO_GBM_1X, COSTO_GBM_R3 = 0.0042, 0.0039, 0.0044   # 0.29% + spread (doc 02 de la arena)
CETES_28 = 0.0615
ARRASTRE_SPX3, ARRASTRE_NDX3 = 0.0214, 0.0277   # calibrados en cartera_inicial_simulacion.py (2022-2026)
RUIDO_GBM, RUIDO_CRIPTO = 0.03, 0.05            # [I] ruido idiosincratico de los rivales
BLOQUE = 30
SEMILLA = 20260925
BETAS = (1.30, 1.45)
PRIMA_SPX_M3 = 0.05
PESOS_A = (0.563, 0.271, 0.166)                 # cartera A de GBM: SPYM, QQQM, liquidez (salida_cartera_inicial.txt)
PIERNAS_PROPIAS = (("A", "A sellada (b~0.9)"), ("B1.30", "beta 1.30"), ("B1.45", "beta 1.45"))


# ------------------------------------------------------------------ descarga
def yahoo_json(ticker: str) -> dict:
    url = (URL_YAHOO + urllib.parse.quote(ticker, safe="") + "?" + urllib.parse.urlencode(
        {"period1": 0, "period2": P2, "interval": "1d", "events": "div,splits"}))
    return json.loads(descargar(url, UA_NAVEGADOR, cache_horas=12))["chart"]["result"][0]


def serie_cripto(ticker: str) -> tuple[dict, dict]:
    """{dia UTC: (cierre, minimo)} hasta CORTE, y la metadata (precio vivo)."""
    res = yahoo_json(ticker)
    q = res["indicators"]["quote"][0]
    out = {}
    for i, ts in enumerate(res.get("timestamp") or []):
        d = datetime.fromtimestamp(ts, tz=timezone.utc).date()
        c, lo = q["close"][i], q["low"][i]
        if d <= CORTE and c and c > 0:
            out[d] = (float(c), float(min(lo, c)) if lo and lo > 0 else float(c))
    return out, res["meta"]


def serie_eua(ticker: str) -> tuple[dict, dict]:
    """{dia de Nueva York: cierre ajustado} hasta CORTE."""
    res = yahoo_json(ticker)
    off = int(res["meta"].get("gmtoffset", 0))
    adj = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose")
    q = res["indicators"]["quote"][0]
    out = {}
    for i, ts in enumerate(res.get("timestamp") or []):
        d = datetime.fromtimestamp(ts + off, tz=timezone.utc).date()
        v = adj[i] if adj and adj[i] is not None else q["close"][i]
        if d <= CORTE and v and v > 0:
            out[d] = float(v)
    return out, res["meta"]


def serie_fx() -> tuple[dict, dict]:
    """{dia UTC D: USD/MXN al final de D} con la convencion de velas explicada en el docstring."""
    res = yahoo_json("MXN=X")
    q = res["indicators"]["quote"][0]["close"]
    out = {}
    for ts, c in zip(res.get("timestamp") or [], q):
        if c is None:
            continue
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        if (dt.hour, dt.minute) == (23, 0):
            L = (dt + timedelta(hours=1)).date()
        elif (dt.hour, dt.minute) == (0, 0):
            L = dt.date()
        else:
            continue                              # vela viva del dia
        D = L if L < CAMBIO_FX else L - timedelta(days=1)
        if D <= CORTE:
            out[D] = float(c)
    return out, res["meta"]


def ffill(d: dict, fechas: list[date]) -> np.ndarray:
    ks = sorted(d)
    out, j, ult = [], 0, np.nan
    for f in fechas:
        while j < len(ks) and ks[j] <= f:
            ult = d[ks[j]]
            j += 1
        out.append(ult)
    return np.array(out, dtype=float)


def cargar_datos() -> dict:
    btc, meta_b = serie_cripto("BTC-USD")
    eth, meta_e = serie_cripto("ETH-USD")
    usdt, _ = serie_cripto("USDT-USD")
    fx, meta_fx = serie_fx()
    spy, meta_spy = serie_eua("SPY")
    qqq, _ = serie_eua("QQQ")
    dtb3 = dict(fred_serie("DTB3", "2014-01-01", cache_horas=12))
    dex = dict(fred_serie("DEXMXUS", "2014-01-01", cache_horas=12))
    p0 = min(btc)
    fechas = [p0 + timedelta(days=k) for k in range((CORTE - p0).days + 1)]
    faltan_btc = sum(1 for f in fechas if f not in btc)
    faltan_eth = sum(1 for f in fechas if f >= min(eth) and f not in eth)
    D = {"fechas": fechas, "faltan_btc": faltan_btc, "faltan_eth": faltan_eth}
    D["btc"] = ffill({k: v[0] for k, v in btc.items()}, fechas)
    D["btc_lo"] = np.array([btc[f][1] if f in btc else np.nan for f in fechas])
    D["eth"] = ffill({k: v[0] for k, v in eth.items()}, fechas)
    D["eth"][np.array([f < min(eth) for f in fechas])] = np.nan
    D["eth_lo"] = np.array([eth[f][1] if f in eth else np.nan for f in fechas])
    D["fx"] = ffill(fx, fechas)
    D["spy"] = ffill(spy, fechas)
    D["qqq"] = ffill(qqq, fechas)
    D["nyse"] = np.array([f in spy for f in fechas])
    D["rf"] = ffill(dtb3, fechas) / 100.0
    D["rf_hoy"] = float(D["rf"][-1])
    D["rf_hoy_fecha"] = max(f for f in dtb3 if f <= CORTE)
    D["usdt"] = {k: v[0] for k, v in usdt.items()}
    D["dex"] = dex
    D["fx_dict"] = fx
    D["vivo"] = {"BTC": (meta_b.get("regularMarketPrice"), meta_b.get("regularMarketTime")),
                 "ETH": (meta_e.get("regularMarketPrice"), meta_e.get("regularMarketTime")),
                 "FX": (meta_fx.get("regularMarketPrice"), meta_fx.get("regularMarketTime")),
                 "SPY": (meta_spy.get("regularMarketPrice"), meta_spy.get("regularMarketTime"))}
    assert fechas[-1] == CORTE and not np.isnan(D["fx"][-1]) and not np.isnan(D["spy"][-1])
    # rendimientos diarios (indice t = rendimiento de t-1 a t)
    n = len(fechas)
    for k in ("btc", "eth", "fx", "spy", "qqq"):
        r = np.full(n, np.nan)
        r[1:] = D[k][1:] / D[k][:-1] - 1
        D["r_" + k] = r
    for k in ("btc", "eth"):
        lo = np.full(n, np.nan)
        lo[1:] = D[k + "_lo"][1:] / D[k][:-1]
        D["lo_" + k] = np.minimum(lo, 1 + D["r_" + k])
    rf_d = np.full(n, np.nan)
    rf_d[1:] = D["rf"][:-1] / 365.0
    D["e_spy"] = D["r_spy"] - rf_d
    D["e_qqq"] = D["r_qqq"] - rf_d
    for k in ("btc", "eth"):
        for m in (50, 100, 150, 200):
            D[f"sig_{k}_{m}"] = senal_sma(D[k], m)
    D["i0"] = fechas.index(INICIO_MUESTRA)
    return D


# ------------------------------------------------------------------ utilidades
def media_movil(x: np.ndarray, n: int) -> np.ndarray:
    out = np.full(len(x), np.nan)
    ok = ~np.isnan(x)
    c = np.cumsum(np.where(ok, x, 0.0))
    cnt = np.cumsum(ok)
    for i in range(n - 1, len(x)):
        a = c[i] - (c[i - n] if i >= n else 0.0)
        k = cnt[i] - (cnt[i - n] if i >= n else 0)
        if k == n:
            out[i] = a / n
    return out


def senal_sma(x: np.ndarray, n: int) -> np.ndarray:
    m = media_movil(x, n)
    return np.where(np.isnan(m), False, x > m)


def pct(x, q):
    return float(np.percentile(x, q))


def fmt(x, d=1, signo=True):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "   n/d"
    return f"{x * 100:+.{d}f}%" if signo else f"{x * 100:.{d}f}%"


def corr(a, b):
    m = ~(np.isnan(a) | np.isnan(b))
    return float(np.corrcoef(a[m], b[m])[0, 1]) if m.sum() > 5 else float("nan")


# ------------------------------------------------------------------ trayectorias
CAMPOS_R = ("rb", "lb", "re", "le", "rx", "es", "eq")


def pool_arrays(D: dict, desde: int) -> dict:
    s = slice(desde, len(D["fechas"]))
    return {"rb": D["r_btc"][s], "lb": D["lo_btc"][s], "re": D["r_eth"][s], "le": D["lo_eth"][s],
            "rx": D["r_fx"][s], "es": D["e_spy"][s], "eq": D["e_qqq"][s]}


def ajustar_deriva(pool: dict, D: dict, modo: str) -> tuple[dict, dict]:
    """M3 / M4: cambia la media aritmetica de cada serie, preserva la forma (minimos relativos al cierre)."""
    p = {k: v.copy() for k, v in pool.items()}
    info = {}
    nyse_sd = np.nanstd(D["r_spy"][D["i0"]:][D["nyse"][D["i0"]:]]) * math.sqrt(252)
    sr_spx = PRIMA_SPX_M3 / nyse_sd
    rf_hoy = D["rf_hoy"]
    for k_r, k_l in (("rb", "lb"), ("re", "le")):
        r = p[k_r]
        sd = np.std(r) * math.sqrt(365)
        mu_obj = rf_hoy + (sr_spx * sd if modo == "M3" else 0.0)   # aritmetico anual en USD
        # r_hist incluye la rf historica; la nueva media diaria total = mu_obj/365
        nuevo = r - r.mean() + mu_obj / 365
        p[k_l] = p[k_l] * (1 + nuevo) / (1 + r)
        p[k_r] = nuevo
        info[k_r] = (r.mean() * 365, mu_obj, sd)
    p["rx"] = p["rx"] - p["rx"].mean()
    p["es"] = p["es"] - p["es"].mean() + PRIMA_SPX_M3 / 365
    sd_q = np.nanstd(D["r_qqq"][D["i0"]:][D["nyse"][D["i0"]:]]) * math.sqrt(252)
    p["eq"] = p["eq"] - p["eq"].mean() + sr_spx * sd_q / 365
    info["sr_spx"] = sr_spx
    return p, info


def indices_bootstrap(n_caminos: int, n_obs: int, rng: np.random.Generator,
                      primeros: np.ndarray | None = None) -> np.ndarray:
    idx = np.empty((n_caminos, H), dtype=np.int64)
    idx[:, 0] = rng.choice(primeros, n_caminos) if primeros is not None else rng.integers(0, n_obs, n_caminos)
    salto = rng.random((n_caminos, H)) < 1.0 / BLOQUE
    nuevos = rng.integers(0, n_obs, (n_caminos, H))
    for t in range(1, H):
        idx[:, t] = np.where(salto[:, t], nuevos[:, t], (idx[:, t - 1] + 1) % n_obs)
    return idx


def senal_simulada(hist: np.ndarray, r: np.ndarray, n: int) -> np.ndarray:
    """Senal precio > SMA(n) en t = 0..H, con los n cierres reales previos + la trayectoria simulada."""
    P_ = r.shape[0]
    base = hist[-n:] / hist[-1]                                  # precios relativos a la entrada
    sim = np.cumprod(1 + r, axis=1)
    full = np.concatenate([np.broadcast_to(base, (P_, n)), sim], axis=1)
    cs = np.concatenate([np.zeros((P_, 1)), np.cumsum(full, axis=1)], axis=1)
    t = np.arange(H + 1)
    sma = (cs[:, n + t] - cs[:, t]) / n
    precio = full[:, n - 1 + t]
    return precio > sma


def caminos_bootstrap(D: dict, pool: dict, n_caminos: int, rng: np.random.Generator,
                      regimen_inicial: bool = True, desde: int | None = None) -> dict:
    n_obs = len(pool["rb"])
    primeros = None
    if regimen_inicial:
        sig = D["sig_btc_200"][desde:][:n_obs]
        primeros = np.flatnonzero(sig)
    idx = indices_bootstrap(n_caminos, n_obs, rng, primeros)
    C = {k: pool[k][idx] for k in CAMPOS_R}
    for k, serie in (("b", "btc"), ("e", "eth")):
        r = C["r" + k]
        for m in (50, 200):
            C[f"sig_{k}_{m}"] = senal_simulada(D[serie], r, m)
    C["P"] = n_caminos
    return C


def caminos_ventanas(D: dict, solo_regimen: bool = False, hasta: date | None = None,
                     desde_f: date | None = None) -> dict:
    fechas = D["fechas"]
    i_ini = fechas.index(INICIO_MUESTRA) - 1                     # entrada al cierre del 2017-11-09
    starts = np.arange(i_ini, len(fechas) - H)
    if solo_regimen:
        starts = starts[D["sig_btc_200"][starts]]
    if hasta is not None:
        starts = starts[np.array([fechas[s] < hasta for s in starts])]
    if desde_f is not None:
        starts = starts[np.array([fechas[s] >= desde_f for s in starts])]
    off = starts[:, None] + 1 + np.arange(H)[None, :]
    C = {"rb": D["r_btc"][off], "lb": D["lo_btc"][off], "re": D["r_eth"][off], "le": D["lo_eth"][off],
         "rx": D["r_fx"][off], "es": D["e_spy"][off], "eq": D["e_qqq"][off]}
    offs = starts[:, None] + np.arange(H + 1)[None, :]
    for k, serie in (("b", "btc"), ("e", "eth")):
        for m in (50, 200):
            C[f"sig_{k}_{m}"] = D[f"sig_{serie}_{m}"][offs]
    C["P"] = len(starts)
    C["starts"] = starts
    return C


# ------------------------------------------------------------------ motor de la cuenta Binance
CANDIDATAS = {
    "K0": {"nombre": "K0 100% USDT (referencia)", "lineas": [], "reserva": 1.0},
    "K1": {"nombre": "K1 100% BTC", "lineas": [{"a": "b", "w": 1.0}]},
    "K2": {"nombre": "K2 BTC/ETH 70/30", "lineas": [{"a": "b", "w": 0.7}, {"a": "e", "w": 0.3}]},
    "K3": {"nombre": "K3 BTC con filtro SMA200 (rezago 1d)",
           "lineas": [{"a": "b", "w": 1.0, "filtro": "sig_b_200"}], "rezago": 1},
    "K4": {"nombre": "K4 55/20/25 + compra de caidas", "lineas": [{"a": "b", "w": 0.55}, {"a": "e", "w": 0.20}],
           "reserva": 0.25, "dips": [(0.85, 0.125), (0.75, 0.125)]},
}
VARIANTES = {
    "K3a": {"nombre": "K3a SMA200 sin rezago (ideal)", "lineas": [{"a": "b", "w": 1.0, "filtro": "sig_b_200"}],
            "rezago": 0},
    "K3b": {"nombre": "K3b 70/30 con SMA200 por activo", "lineas": [
        {"a": "b", "w": 0.7, "filtro": "sig_b_200"}, {"a": "e", "w": 0.3, "filtro": "sig_e_200"}], "rezago": 1},
    "K3c": {"nombre": "K3c BTC con SMA50 (regla R7 cap.14)", "lineas": [{"a": "b", "w": 1.0, "filtro": "sig_b_50"}],
            "rezago": 1},
    "K4s": {"nombre": "K4s 55/20/25 sin compra de caidas", "lineas": [{"a": "b", "w": 0.55}, {"a": "e", "w": 0.20}],
            "reserva": 0.25},
}


def simular_cuenta(esp: dict, C: dict) -> dict:
    """Cuenta Binance con las reglas del perfil cripto_binance. Unidades: q, u y reserva en MXN al tipo de cambio
    y precios de entrada (valor_t = q * precio_rel_t * fx_rel_t); mxn en pesos."""
    P = C["P"]
    lin = esp["lineas"]
    nL = len(lin)
    rez = esp.get("rezago", 1)
    w = np.array([l["w"] for l in lin]) if nL else np.zeros(0)
    filtrada = np.array([bool(l.get("filtro")) for l in lin]) if nL else np.zeros(0, bool)
    cap0 = CAPITAL * (1 - CONVERSION)
    q = np.zeros((P, nL))
    u = np.zeros((P, nL))
    reserva = np.full(P, cap0 * esp.get("reserva", 0.0))
    mxn = np.zeros(P)
    ops = np.ones(P, dtype=np.int64)                             # MXN -> USDT
    ops_mes = np.zeros((P, 6), dtype=np.int64)
    for j, l in enumerate(lin):
        on = C[l["filtro"]][:, 0] if l.get("filtro") else np.ones(P, bool)
        q[:, j] = np.where(on, cap0 * w[j] * (1 - COMISION), 0.0)
        u[:, j] = np.where(on, 0.0, cap0 * w[j])
        ops += on
    ops_mes[:, 0] = ops
    px = {"b": np.ones(P), "e": np.ones(P)}
    fx = np.ones(P)
    dips = esp.get("dips", [])
    lleno = np.zeros((P, len(dips)), bool)
    j_btc = next((j for j, l in enumerate(lin) if l["a"] == "b"), None)
    parado = np.zeros(P, bool)
    pausa_hasta = np.zeros(P, dtype=np.int64)
    tope = np.ones(P)                                            # exposicion maxima vigente (fraccion del valor)
    pico = np.full(P, CAPITAL)
    dd = np.zeros(P)
    maxdd = np.zeros(P)
    maxdd_lo = np.zeros(P)
    vmin = np.full(P, CAPITAL)
    n_pausas = np.zeros(P, dtype=np.int64)
    n_cortes = np.zeros(P, dtype=np.int64)
    n_liberaciones = np.zeros(P, dtype=np.int64)
    expo_fin = np.zeros(P)
    mes_de = [min((INICIO_TEMPORADA + timedelta(days=t)).month % 12, 5) for t in range(H + 1)]

    def matriz(dic):
        return np.stack([dic[l["a"]] for l in lin], 1) if nL else np.zeros((P, 0))

    for t in range(1, H + 1):
        k = t - 1
        prev_b = px["b"].copy()
        lo = {"b": px["b"] * C["lb"][:, k], "e": px["e"] * C["le"][:, k]}
        px["b"] = px["b"] * (1 + C["rb"][:, k])
        px["e"] = px["e"] * (1 + C["re"][:, k])
        fx = fx * (1 + C["rx"][:, k])
        activo = ~parado & (t >= pausa_hasta)
        for d_i, (nivel, frac) in enumerate(dips):              # ordenes limite de K4 (intradia)
            f = ~lleno[:, d_i] & activo & (lo["b"] <= nivel)
            if f.any():
                precio = np.minimum(nivel, prev_b)
                pxs_f = matriz(px)
                pxs_f[:, j_btc] = precio
                X_f = (q * pxs_f).sum(1) * fx
                V_f = X_f + (u.sum(1) + reserva) * fx + mxn
                hueco = np.maximum(tope * V_f - X_f, 0.0) / fx
                monto = np.minimum(np.minimum(cap0 * frac, reserva), hueco) * f
                q[:, j_btc] += monto * (1 - COMISION) / precio
                reserva -= monto
                lleno[:, d_i] |= f
                hubo = monto > 0
                ops += hubo
                ops_mes[:, mes_de[t]] += hubo
        pxs = matriz(px)
        X = (q * pxs).sum(1) * fx
        V = X + (u.sum(1) + reserva) * fx + mxn
        V_lo = (q * matriz(lo)).sum(1) * fx + (u.sum(1) + reserva) * fx + mxn
        maxdd_lo = np.minimum(maxdd_lo, V_lo / pico - 1)
        dd_prev = dd
        pico = np.maximum(pico, V)
        dd = V / pico - 1
        maxdd = np.minimum(maxdd, dd)
        vmin = np.minimum(vmin, V)
        # --- cortacircuitos
        stop = ((dd <= -0.50) | (V <= CAPITAL - 5000)) & ~parado
        if stop.any():
            mxn = mxn + stop * (X * (1 - COMISION - CONVERSION) + (u.sum(1) + reserva) * fx * (1 - CONVERSION))
            q[stop] = 0.0
            u[stop] = 0.0
            reserva = np.where(stop, 0.0, reserva)
            parado |= stop
            ops += stop
            tope = np.where(stop, 0.0, tope)
        cruza40 = (dd <= -0.40) & (dd_prev > -0.40) & ~parado
        pausa_hasta = np.where(cruza40, t + 7, pausa_hasta)
        n_pausas += cruza40
        nivel_tope = np.where(dd <= -0.30, 0.25, np.where(dd <= -0.20, 0.50, 1.0))
        nuevo_tope = np.minimum(tope, nivel_tope)
        corte = (nuevo_tope < tope) & ~parado                   # la venta es una accion al cruzar el nivel,
        n_cortes += corte                                        # no un rebalanceo diario [I]
        tope = np.where(parado, 0.0, nuevo_tope)
        X = (q * pxs).sum(1) * fx
        V = X + (u.sum(1) + reserva) * fx + mxn
        exceso = np.maximum(X - tope * V, 0.0) * corte
        if (exceso > 0).any():
            frac_v = np.where(X > 0, exceso / np.maximum(X, 1e-12), 0.0)
            mxn = mxn + exceso * (1 - COMISION - CONVERSION)
            q = q * (1 - frac_v[:, None])
            ops += exceso > 0
            ops_mes[:, mes_de[t]] += exceso > 0
        libera = (dd >= 0) & (tope < 1) & ~parado
        if libera.any():
            tope = np.where(libera, 1.0, tope)
            n_liberaciones += libera
            if nL and not filtrada.any():                        # comprar y mantener: recompra con el MXN de los cortes
                recompra = libera & (mxn > 0)
                wn = w / w.sum()
                for j in range(nL):
                    q[:, j] += np.where(recompra, mxn * wn[j] * (1 - COMISION - CONVERSION) / (pxs[:, j] * fx), 0.0)
                mxn = np.where(recompra, 0.0, mxn)
                ops += recompra
                ops_mes[:, mes_de[t]] += recompra
        # --- senales de tendencia (K3) al cierre de t
        if t < H:
            for j, l in enumerate(lin):
                if not l.get("filtro"):
                    continue
                obj = C[l["filtro"]][:, max(t - rez, 0)]
                p_j = px[l["a"]]
                vender = ~obj & (q[:, j] > 0) & ~parado
                u[:, j] = np.where(vender, u[:, j] + q[:, j] * p_j * (1 - COMISION), u[:, j])
                q[:, j] = np.where(vender, 0.0, q[:, j])
                X = (q * matriz(px)).sum(1) * fx
                V = X + (u.sum(1) + reserva) * fx + mxn
                hueco = np.maximum(tope * V - X, 0.0)
                comprar = obj & (q[:, j] == 0) & ((u[:, j] > 0) | (mxn > 0)) & ~parado & (t >= pausa_hasta) & (hueco > 0)
                de_u = np.minimum(u[:, j] * fx, hueco) * comprar
                de_m = np.minimum(mxn, hueco - de_u) * comprar
                q[:, j] += (de_u * (1 - COMISION) + de_m * (1 - COMISION - CONVERSION)) / (p_j * fx)
                u[:, j] -= de_u / fx
                mxn = mxn - de_m
                ops += vender | comprar
                ops_mes[:, mes_de[t]] += vender | comprar
    pxs = matriz(px)
    X = (q * pxs).sum(1) * fx
    V = X + (u.sum(1) + reserva) * fx + mxn
    expo_fin = X / V
    return {"R": V / CAPITAL - 1, "maxdd": maxdd, "maxdd_lo": maxdd_lo, "vmin": vmin, "parado": parado,
            "ops": ops, "ops_mes_max": ops_mes.max(1), "pausas": n_pausas, "cortes": n_cortes,
            "liberaciones": n_liberaciones, "expo_fin": expo_fin, "V": V}


# ------------------------------------------------------------------ piernas GBM y rivales (comprar y mantener)
def crecimientos(C: dict, rf_hoy: float) -> dict:
    g = {}
    g["fx"] = np.prod(1 + C["rx"], axis=1)
    g["btc"] = np.prod(1 + C["rb"], axis=1)
    g["eth"] = np.prod(1 + C["re"], axis=1)
    for b in (1.0,) + BETAS:
        arr = (b - 1) / 2 * ARRASTRE_SPX3
        g[f"spx{b:.2f}"] = np.prod(1 + rf_hoy / 365 + b * C["es"] - arr / 365, axis=1)
    g["qqq1"] = np.prod(1 + rf_hoy / 365 + C["eq"], axis=1)
    g["qqq3"] = np.prod(1 + rf_hoy / 365 + 3 * C["eq"] - ARRASTRE_NDX3 / 365, axis=1)
    g["cetes"] = (1 + CETES_28 / 360) ** H
    return g


def pierna_gbm(arq: str, g: dict) -> np.ndarray:
    """Rendimiento de la temporada en MXN de una pierna GBM de 20,000."""
    if arq == "R1":
        return (1 - COSTO_GBM_1X) * g["spx1.00"] * g["fx"] - 1
    if arq == "R2":
        return 0.5 * (1 - COSTO_GBM_1X) * g["spx1.00"] * g["fx"] + 0.5 * g["cetes"] - 1
    if arq == "R3":
        return (1 - COSTO_GBM_R3) * 0.5 * (g["qqq3"] + g["qqq1"]) * g["fx"] - 1
    if arq == "A":
        ws, wq, wc = PESOS_A
        return (1 - COSTO_GBM_1X) * (ws * g["spx1.00"] + wq * g["qqq1"]) * g["fx"] + wc * g["cetes"] - 1
    b = float(arq[1:])
    return (1 - COSTO_GBM) * g[f"spx{b:.2f}"] * g["fx"] - 1


def pierna_cripto(arq: str, g: dict) -> np.ndarray:
    c = (1 - CONVERSION)
    k = 1 - COMISION
    if arq == "C1":
        return c * k * g["btc"] * g["fx"] - 1
    if arq == "C2":
        return c * (0.6 * k * g["btc"] + 0.4 * k * g["eth"]) * g["fx"] - 1
    if arq == "C3":
        return c * (0.5 * k * g["btc"] + 0.5) * g["fx"] - 1
    if arq == "C4":
        return c * k * g["eth"] * g["fx"] - 1
    raise ValueError(arq)


CAMPOS = {"F1": [("R1", "C2"), ("R2", "C3")], "F2": [("R1", "C1"), ("R3", "C4")],
          "F3": [("R1", "C2"), ("R1", "C2")], "F4": [("R2", "C3"), ("R2", "C3")]}
DESC_GBM = {"R1": "beta 1 S&P", "R2": "50% S&P + 50% CETES", "R3": "50% TQQQ + 50% QQQ"}
DESC_CR = {"C1": "100% BTC", "C2": "60/40 BTC/ETH", "C3": "50% BTC + 50% USDT", "C4": "100% ETH"}


def rivales(g: dict, rng: np.random.Generator, P: int) -> dict:
    out = {}
    for campo, lista in CAMPOS.items():
        rs = []
        for a_gbm, a_cr in lista:
            rg = pierna_gbm(a_gbm, g) + rng.normal(0, RUIDO_GBM, P)
            rc = pierna_cripto(a_cr, g) + rng.normal(0, RUIDO_CRIPTO, P)
            rs.append((CAPITAL_GBM * rg + CAPITAL * rc) / (CAPITAL_GBM + CAPITAL))
        out[campo] = np.stack(rs, 1)
    return out


# ------------------------------------------------------------------ reporte por metodo
ENCAB = ("candidata                                   mediana     p10     p90   media   P<0  P-20%  P-30%  P-40% "
         "P-50%/tope  P(V<=5k)  DDmed  DDp90  P-20%id  ops  opsmes>8  expo.fin  libera")


def fila_dist(nombre: str, s: dict) -> str:
    R, dd = s["R"], s["maxdd"]
    return (f"{nombre:42s} {fmt(np.median(R)):>8s} {fmt(pct(R, 10)):>7s} {fmt(pct(R, 90)):>7s} "
            f"{fmt(R.mean()):>7s} {np.mean(R < 0):5.0%} {np.mean(dd <= -0.20):6.1%} {np.mean(dd <= -0.30):6.1%} "
            f"{np.mean(dd <= -0.40):6.1%} {np.mean(s['parado']):10.1%} {np.mean(s['vmin'] <= CAPITAL - 5000):9.1%} "
            f"{fmt(np.median(dd)):>6s} {fmt(pct(dd, 10)):>6s} {np.mean(s['maxdd_lo'] <= -0.20):8.1%} "
            f"{np.mean(s['ops']):4.1f} {np.mean(s['ops_mes_max'] > 8):8.1%} {np.median(s['expo_fin']):8.0%} "
            f"{np.mean(s['liberaciones'] > 0):7.1%}")


def evaluar_metodo(etiqueta: str, C: dict, D: dict, rng: np.random.Generator, resumen: dict,
                   variantes: bool = True) -> dict:
    P = C["P"]
    print(f"\n### {etiqueta}  (trayectorias: {P})")
    print(ENCAB)
    res = {}
    for k, esp in list(CANDIDATAS.items()) + (list(VARIANTES.items()) if variantes else []):
        s = simular_cuenta(esp, C)
        res[k] = s
        print(fila_dist(esp["nombre"], s))
    g = crecimientos(C, D["rf_hoy"])
    print("  referencias comprar y mantener (sin cortacircuitos): "
          + "; ".join(f"{DESC_CR[a]} med {fmt(np.median(pierna_cripto(a, g)))}" for a in ("C1", "C2", "C3", "C4")))
    print("  piernas GBM: " + "; ".join(f"{n} med {fmt(np.median(pierna_gbm(a, g)))} p10 {fmt(pct(pierna_gbm(a, g), 10))}"
                                        for n, a in (("R1 beta1", "R1"), ("R2 50/50", "R2"), ("R3 2x NDX", "R3"),
                                                     ("propia A", "A"), ("propia b1.30", "B1.30"),
                                                     ("propia b1.45", "B1.45"))))
    riv = rivales(g, rng, P)
    print(f"  Cuenta combinada (20k GBM + 10k Binance). P(1o) = arriba de los dos rivales; ult = abajo de ambos.")
    print("  candidata                                  GBM                comb.med  comb.p10  P(comb<0)    F1 1o   F2 1o"
          "   F3 1o   F4 1o  prom 1o   F1 ult   F2 ult")
    tabla = {}
    for clave_g, desc_g in PIERNAS_PROPIAS:
        rg = pierna_gbm(clave_g, g)
        for k, esp in CANDIDATAS.items():
            comb = (CAPITAL_GBM * rg + CAPITAL * res[k]["R"]) / (CAPITAL_GBM + CAPITAL)
            p1 = {c: float(np.mean(comb > riv[c].max(1))) for c in CAMPOS}
            pu = {c: float(np.mean(comb < riv[c].min(1))) for c in CAMPOS}
            prom = float(np.mean(list(p1.values())))
            tabla[(k, clave_g)] = {"p1": p1, "prom": prom, "pu": pu, "med": float(np.median(comb)),
                                   "p10": pct(comb, 10)}
            print(f"  {esp['nombre']:42s} {desc_g:17s} {fmt(np.median(comb)):>8s}  {fmt(pct(comb, 10)):>8s}   "
                  f"{np.mean(comb < 0):6.1%}  " + "  ".join(f"{p1[c]:6.1%}" for c in CAMPOS)
                  + f"  {prom:6.1%}  {pu['F1']:6.1%}  {pu['F2']:6.1%}")
    resumen[etiqueta] = {"res": res, "tabla": tabla}
    return res


# ------------------------------------------------------------------ secciones
def seccion_datos(D: dict) -> None:
    f = D["fechas"]
    print("## 0. Datos y verificaciones")
    print(f"  BTC-USD {f[0]} a {CORTE} ({len(f)} dias, faltantes {D['faltan_btc']}); ETH-USD desde "
          f"{f[int(np.flatnonzero(~np.isnan(D['eth']))[0])]} (faltantes {D['faltan_eth']}).")
    # verificacion del tipo de cambio contra DEXMXUS: rendimientos mensuales (fin de mes)
    fx, dex = D["fx_dict"], D["dex"]
    meses = sorted({(d.year, d.month) for d in dex if d >= date(2017, 11, 1)})
    def fin_mes(dic, y, m):
        ks = [d for d in dic if d.year == y and d.month == m]
        return dic[max(ks)] if ks else np.nan
    a = np.array([fin_mes(fx, y, m) for y, m in meses])
    b = np.array([fin_mes(dex, y, m) for y, m in meses])
    ra, rb = a[1:] / a[:-1] - 1, b[1:] / b[:-1] - 1
    print(f"  USD/MXN Yahoo (convencion corregida) vs FRED DEXMXUS, rendimientos mensuales 2017-11 a 2026-09: "
          f"corr {corr(ra, rb):.3f}; diferencia media absoluta {np.nanmean(np.abs(ra - rb)) * 100:.2f} pp.")
    ult = max(fx)
    print(f"  USD/MXN al final del {ult} (foto 23:00 UTC): {fx[ult]:.4f}. Vivo: {D['vivo']['FX'][0]} "
          f"({datetime.fromtimestamp(D['vivo']['FX'][1], tz=timezone.utc):%Y-%m-%d %H:%M} UTC).")
    u = D["usdt"]
    us = np.array([u[k] for k in sorted(u) if k >= date(2017, 11, 9)])
    print(f"  USDT-USD (Yahoo, cierres diarios desde 2017-11-09): min {us.min():.4f}, max {us.max():.4f}, "
          f"dias con |desvio| > 1%: {int(np.sum(np.abs(us - 1) > 0.01))} de {len(us)}.")
    print(f"  T-bill DTB3 {D['rf_hoy_fecha']}: {D['rf_hoy']:.2%}. CETES 28: {CETES_28:.2%} (supuesto, fuente secundaria).")
    vb, tb = D["vivo"]["BTC"]
    ve, te = D["vivo"]["ETH"]
    print(f"  Precio vivo al correr: BTC {vb:,.0f} USD, ETH {ve:,.2f} USD "
          f"({datetime.fromtimestamp(tb, tz=timezone.utc):%Y-%m-%d %H:%M} UTC); cierre {CORTE}: "
          f"BTC {D['btc'][-1]:,.0f}, ETH {D['eth'][-1]:,.2f}.")


def metricas_actuales(D: dict) -> None:
    print("\n## 1. Metricas actuales (cierre del 24-sep-2026 UTC; cripto anualiza con raiz(365), SPY con raiz(252))")
    f = D["fechas"]
    corte = f[-1]
    nyse = D["nyse"]
    fx = D["fx"]
    idx_n = np.flatnonzero(nyse)
    def rend_nyse(nivel):
        v = nivel[idx_n]
        return v[1:] / v[:-1] - 1
    spy_mxn = rend_nyse(D["spy"] * fx)
    series = {
        "BTC USD": (D["btc"], 365), "BTC MXN": (D["btc"] * fx, 365),
        "ETH USD": (D["eth"], 365), "ETH MXN": (D["eth"] * fx, 365),
        "SPY MXN": (D["spy"] * fx, 252), "USD/MXN": (fx, 252),
    }
    print("serie        precio      3m      6m    12-1   vsSMA200  vsSMA50  vol60d  DD vs max  DDmax 1a  "
          "corr60 S&P  corr1a S&P  corr1a sem")
    fechas_idx = {d: i for i, d in enumerate(f)}
    def valor(nivel, d):
        return nivel[fechas_idx[d]]
    for nom, (niv, ppa) in series.items():
        if ppa == 252:
            obs = niv[idx_n]
        else:
            obs = niv[~np.isnan(niv)]
        p = obs[-1]
        r3 = p / valor(niv, meses_atras(corte, 3)) - 1
        r6 = p / valor(niv, meses_atras(corte, 6)) - 1
        r12_1 = valor(niv, meses_atras(corte, 1)) / valor(niv, meses_atras(corte, 12)) - 1
        s200 = p / np.mean(obs[-200:]) - 1
        s50 = p / np.mean(obs[-50:]) - 1
        lg = np.diff(np.log(obs[-61:]))
        vol = np.std(lg, ddof=1) * math.sqrt(ppa)
        maxhist = np.nanmax(obs)
        anio = niv[np.array([d > meses_atras(corte, 12) for d in f])]
        anio = anio[~np.isnan(anio)]
        pk, ddm = anio[0], 0.0
        for x in anio:
            pk = max(pk, x)
            ddm = min(ddm, x / pk - 1)
        r_n = rend_nyse(niv)
        c60 = corr(r_n[-60:], spy_mxn[-60:])
        c1a = corr(r_n[-252:], spy_mxn[-252:])
        # semanal (viernes NY): ultimo dia NYSE de cada semana
        sem = [i for i in range(len(idx_n) - 1) if f[idx_n[i + 1]].isocalendar()[1] != f[idx_n[i]].isocalendar()[1]]
        sem = np.array(sem[-53:])
        ws = niv[idx_n][sem]
        wsp = (D["spy"] * fx)[idx_n][sem]
        c1w = corr(ws[1:] / ws[:-1] - 1, wsp[1:] / wsp[:-1] - 1)
        print(f"{nom:9s} {p:11,.2f} {fmt(r3):>7s} {fmt(r6):>7s} {fmt(r12_1):>7s} {fmt(s200):>9s} {fmt(s50):>8s} "
              f"{fmt(vol, 1, False):>7s} {fmt(p / maxhist - 1):>9s} {fmt(ddm):>9s} {c60:10.2f} {c1a:11.2f} {c1w:10.2f}")
    rb = rend_nyse(D["btc"] * fx)
    re_ = rend_nyse(D["eth"] * fx)
    rs_u, rq_u = rend_nyse(D["spy"]), rend_nyse(D["qqq"])
    desde = np.array([f[i] >= INICIO_MUESTRA for i in idx_n[1:]])
    b_q = np.cov(rq_u[desde], rs_u[desde])[0, 1] / np.var(rs_u[desde], ddof=1)
    b_a = PESOS_A[0] + PESOS_A[1] * b_q
    print(f"  Beta de QQQ contra SPY (USD, dias NYSE, 2017-11 a 2026-09): {b_q:.2f} -> beta de la cartera A de GBM "
          f"(56.3% SPYM + 27.1% QQQM + 16.6% liquidez) = {b_a:.2f}. Las betas 1.30-1.45 que pidio el orquestador NO son la "
          f"cartera sellada (commit c24bb1b); se simulan las tres.")
    print(f"  corr BTC-ETH (MXN, dias NYSE, 1 anio): {corr(rb[-252:], re_[-252:]):.2f}. Cartera GBM propuesta (beta 1.3-1.45"
          f" al S&P) = beta x S&P: su correlacion con BTC es la de la columna 'corr S&P'.")
    i = len(f) - 1
    for k, n in (("btc", 200), ("btc", 50), ("eth", 200)):
        m = media_movil(D[k], n)[i]
        print(f"  {k.upper()} SMA{n} (USD, {n} cierres diarios): {m:,.2f}; precio/SMA - 1 = {fmt(D[k][i] / m - 1)}; "
              f"senal {'ENCENDIDA' if D[k][i] > m else 'APAGADA'}.")
    sig = D["sig_btc_200"]
    cambios = np.flatnonzero(sig[1:] != sig[:-1]) + 1
    ult = cambios[-1]
    print(f"  Ultimo cruce de BTC sobre su SMA200: {f[ult]} (senal {'encendida' if sig[ult] else 'apagada'} desde entonces). "
          f"Cruces desde 2017-11-09: {int(np.sum(cambios >= D['i0']))} "
          f"({np.sum(cambios >= D['i0']) / ((len(f) - D['i0']) / 365.25):.1f} por anio).")
    ath = int(np.nanargmax(D["btc"]))
    lo1 = int(np.nanargmin(np.where(np.array([d > meses_atras(corte, 12) for d in f]), D["btc"], np.inf)))
    print(f"  BTC: maximo historico {D['btc'][ath]:,.0f} ({f[ath]}); minimo de 12 meses {D['btc'][lo1]:,.0f} ({f[lo1]}); "
          f"desde el minimo {fmt(D['btc'][-1] / D['btc'][lo1] - 1)}.")


def seccion_correlacion(D: dict) -> None:
    print("\n## 3. Correlacion BTC vs S&P 500 (SPY TR) en ventanas de 4 meses (122 dias corridos), 2017-11 a 2026-09")
    f = D["fechas"]
    idx_n = np.flatnonzero(D["nyse"])
    fx = D["fx"]
    def niv_n(x):
        return x[idx_n]
    rb_m = niv_n(D["btc"] * fx)
    rs_m = niv_n(D["spy"] * fx)
    rb_u, rs_u = niv_n(D["btc"]), niv_n(D["spy"])
    re_m = niv_n(D["eth"] * fx)
    r = {k: v[1:] / v[:-1] - 1 for k, v in (("bm", rb_m), ("sm", rs_m), ("bu", rb_u), ("su", rs_u), ("em", re_m))}
    fe = [f[i] for i in idx_n[1:]]
    ini = next(i for i, d in enumerate(fe) if d >= INICIO_MUESTRA)
    cs_m, cs_u, ce_m, anios = [], [], [], []
    for j in range(ini, len(fe)):
        d_fin = fe[j]
        d_ini = d_fin - timedelta(days=H)
        a = next(k for k in range(j, -1, -1) if fe[k] <= d_ini) + 1 if fe[0] <= d_ini else 0
        if fe[a] < INICIO_MUESTRA:
            continue
        cs_m.append(corr(r["bm"][a:j + 1], r["sm"][a:j + 1]))
        cs_u.append(corr(r["bu"][a:j + 1], r["su"][a:j + 1]))
        ce_m.append(corr(r["em"][a:j + 1], r["sm"][a:j + 1]))
        anios.append(d_fin.year)
    cs_m, cs_u, ce_m, anios = map(np.array, (cs_m, cs_u, ce_m, anios))
    print(f"  Correlacion de rendimientos diarios (dias NYSE) dentro de cada ventana movil ({len(cs_m)} ventanas):")
    for nom, x in (("BTC vs S&P, en MXN", cs_m), ("BTC vs S&P, en USD", cs_u), ("ETH vs S&P, en MXN", ce_m)):
        print(f"    {nom:20s} mediana {np.median(x):+.2f}  p10 {pct(x, 10):+.2f}  p90 {pct(x, 90):+.2f}  "
              f"P(>0.3) {np.mean(x > 0.3):4.0%}  P(>0.5) {np.mean(x > 0.5):4.0%}  ultima ventana {x[-1]:+.2f}")
    print("    Mediana por anio (ventanas que terminan en ese anio), MXN / USD: " + "; ".join(
        f"{y}: {np.median(cs_m[anios == y]):+.2f}/{np.median(cs_u[anios == y]):+.2f}" for y in sorted(set(anios))))
    # correlacion de los rendimientos de temporada (no traslapados)
    i0 = D["i0"] - 1
    starts = np.arange(i0, len(f) - H, H)
    Rb = D["btc"][starts + H] * fx[starts + H] / (D["btc"][starts] * fx[starts]) - 1
    Rs = D["spy"][starts + H] * fx[starts + H] / (D["spy"][starts] * fx[starts]) - 1
    Rbu = D["btc"][starts + H] / D["btc"][starts] - 1
    Rsu = D["spy"][starts + H] / D["spy"][starts] - 1
    print(f"  Rendimientos de 4 meses NO traslapados ({len(starts)} temporadas desde 2017-11-09): corr MXN "
          f"{corr(Rb, Rs):+.2f}, USD {corr(Rbu, Rsu):+.2f}. Con n = {len(starts)} el IC95 de una correlacion de ~0.3 "
          f"va de {math.tanh(math.atanh(0.3) - 1.96 / math.sqrt(len(starts) - 3)):+.2f} a "
          f"{math.tanh(math.atanh(0.3) + 1.96 / math.sqrt(len(starts) - 3)):+.2f}.")
    # estres: dias de S&P en MXN en el peor 5%
    m = np.array([d >= INICIO_MUESTRA for d in fe])
    sm, bm = r["sm"][m], r["bm"][m]
    u5 = np.percentile(sm, 5)
    mal = sm <= u5
    print(f"  Dias con S&P en MXN en su peor 5% (<= {u5:+.2%}, n = {mal.sum()}): BTC en MXN promedio {bm[mal].mean():+.2%}, "
          f"cae en {np.mean(bm[mal] < 0):.0%} de esos dias; en el resto de los dias promedio {bm[~mal].mean():+.2%}.")
    # diversificacion de la cuenta combinada con ventanas moviles reales
    C = caminos_ventanas(D)
    g = crecimientos(C, D["rf_hoy"])
    rc = pierna_cripto("C1", g)
    for clave_g, desc_g in PIERNAS_PROPIAS:
        rg = pierna_gbm(clave_g, g)
        comb = (CAPITAL_GBM * rg + CAPITAL * rc) / (CAPITAL_GBM + CAPITAL)
        sg, sc, sp = np.std(rg), np.std(rc), np.std(comb)
        w1, w2 = 2 / 3, 1 / 3
        rho = corr(rg, rc)
        cov = np.cov(rg, rc)[0, 1]
        cuota = (w2 ** 2 * sc ** 2 + w1 * w2 * cov) / sp ** 2
        print(f"  Combinada con K1 (sin cortacircuitos) y GBM {desc_g} (ventanas moviles, {C['P']}): sd 4m GBM {sg:.1%}, cripto {sc:.1%}, "
              f"combinada {sp:.1%}; corr de temporada {rho:+.2f}; sd si corr = 1: {w1 * sg + w2 * sc:.1%}; "
              f"si corr = 0: {math.sqrt((w1 * sg) ** 2 + (w2 * sc) ** 2):.1%}; la cripto aporta {cuota:.0%} de la varianza "
              f"con {w2:.0%} del capital.")


def seccion_significancia(D: dict) -> None:
    print("\n## 6. Ventaja neta y significancia (backtest continuo diario en MXN, 2017-11-10 a 2026-09-24)")
    f = D["fechas"]
    i0 = D["i0"]
    rb = D["r_btc"][i0:]
    re_ = D["r_eth"][i0:]
    rx = D["r_fx"][i0:]
    fe = f[i0:]
    anios = len(rb) / 365.25
    rbm = (1 + rb) * (1 + rx) - 1
    rem = (1 + re_) * (1 + rx) - 1

    def filtrado(sig_full, rezago, r_act):
        sig = sig_full[i0 - 2:len(f)]                            # sig[k] = senal al cierre de fe[k-2]
        pos = sig[2 - rezago - 1: len(sig) - rezago - 1] if rezago else sig[1:-1]
        pos = pos[:len(r_act)].astype(float)
        cambio = np.abs(np.diff(np.concatenate([[pos[0]], pos])))
        return pos * r_act + (1 - pos) * rx - COMISION * cambio, pos
    out = {}
    out["K1 BTC comprar y mantener"] = rbm
    out["K2 70/30 (rebalanceo diario, aprox.)"] = 0.7 * rbm + 0.3 * rem
    for m in (200, 150, 100, 50):
        out[f"BTC SMA{m} rezago 1d" + (" = K3" if m == 200 else "")], _ = filtrado(D[f"sig_btc_{m}"], 1, rbm)
    out["BTC SMA200 sin rezago = K3a"], pos200 = filtrado(D["sig_btc_200"], 0, rbm)
    k3b_b, _ = filtrado(D["sig_btc_200"], 1, rbm)
    k3b_e, _ = filtrado(D["sig_eth_200"], 1, rem)
    out["K3b 70/30 SMA200 por activo"] = 0.7 * k3b_b + 0.3 * k3b_e
    print(f"  {anios:.1f} anios. SR = media/sd x raiz(365), contra 0 en MXN (sin restar CETES). t ~ SR x raiz(anios).")
    print("  estrategia                                 CAGR     vol     SR     t   MDD     %invertido  cambios/anio")
    srs = {}
    for k, r in out.items():
        curva = np.cumprod(1 + r)
        cagr = curva[-1] ** (1 / anios) - 1
        sd = np.std(r, ddof=1) * math.sqrt(365)
        sr = np.mean(r) / np.std(r, ddof=1) * math.sqrt(365)
        srs[k] = sr
        mdd = metricas.max_drawdown(list(curva))["valor"]
        print(f"  {k:40s} {cagr:+7.1%} {sd:6.1%} {sr:6.2f} {sr * math.sqrt(anios):5.2f} {mdd:+6.1%}")
    print(f"  K3 invertido {pos200.mean():.0%} del tiempo.")
    # prima de BTC en USD sobre T-bill
    rf_d = D["rf"][i0 - 1:-1] / 365
    ex = rb - rf_d
    sr_ex = ex.mean() / ex.std(ddof=1) * math.sqrt(365)
    nw = estadistica.newey_west(list(ex), rezagos=10)
    print(f"  Prima de BTC en USD sobre T-bill: media x365 {ex.mean() * 365:+.1%}, SR {sr_ex:.2f}, t IID "
          f"{nw['t_iid']:.2f} / t NW(10) {nw['t']:.2f}; IC95 anual [{nw['ic95'][0] * 365:+.0%}, {nw['ic95'][1] * 365:+.0%}].")
    for a, b, nom in ((date(2017, 11, 10), CORTE_PUBLICACION, "2017-11 a 2020-12"), (CORTE_PUBLICACION, CORTE, "2021-01 a 2026-09"),
                      (INICIO_RECIENTE, CORTE, "2022-01 a 2026-09")):
        m = np.array([a <= d < b or (d == CORTE and b == CORTE) for d in fe])
        e = ex[m]
        print(f"    {nom}: media x365 {e.mean() * 365:+.1%}, SR {e.mean() / e.std(ddof=1) * math.sqrt(365):.2f}, "
              f"t {e.mean() / e.std(ddof=1) * math.sqrt(len(e)):.2f}")
    # K3 - K1
    dif = out["BTC SMA200 rezago 1d = K3"] - rbm
    nw = estadistica.newey_west(list(dif), rezagos=10)
    ic = estadistica.ic_bootstrap_bloques(list(dif), bloque=BLOQUE, repeticiones=2000, semilla=7)
    ir = dif.mean() / dif.std(ddof=1) * math.sqrt(365)
    print(f"  K3 - K1 diario: media x365 {dif.mean() * 365:+.1%}, IR {ir:.2f}, t IID {nw['t_iid']:.2f} / t NW(10) {nw['t']:.2f}, "
          f"IC95 NW anual [{nw['ic95'][0] * 365:+.0%}, {nw['ic95'][1] * 365:+.0%}], IC95 bootstrap de bloques (30d) anual "
          f"[{ic[0] * 365:+.0%}, {ic[1] * 365:+.0%}] -> {estadistica.veredicto(ic)}.")
    for a, b, nom in ((date(2017, 11, 10), CORTE_PUBLICACION, "antes de 2021 (in-sample de Detzel et al.)"),
                      (CORTE_PUBLICACION, date(2026, 9, 25), "desde 2021 (post-publicacion)")):
        m = np.array([a <= d < b for d in fe])
        e = dif[m]
        k1 = rbm[m]
        k3 = out["BTC SMA200 rezago 1d = K3"][m]
        print(f"    {nom}: K3-K1 media x365 {e.mean() * 365:+.1%}, IR {e.mean() / e.std(ddof=1) * math.sqrt(365):.2f}, "
              f"t {e.mean() / e.std(ddof=1) * math.sqrt(len(e)):.2f}; SR K1 {k1.mean() / k1.std() * math.sqrt(365):.2f} "
              f"vs K3 {k3.mean() / k3.std() * math.sqrt(365):.2f}")
    # DSR
    vals = np.array(list(srs.values()))
    v_ann = float(np.var(vals, ddof=1))
    for n_p in (4, len(srs)):
        dsr = metricas.sharpe_deflactado(list(out["BTC SMA200 rezago 1d = K3"]), n_pruebas=n_p, varianza_sharpes=v_ann,
                                         periodos_por_anio=365, varianza_anualizada=True)
        psr = metricas.sharpe_probabilistico(list(out["BTC SMA200 rezago 1d = K3"]), 0.0, periodos_por_anio=365)
        print(f"  DSR de K3 (SR contra 0) con N = {n_p} variantes y V[SR anual] = {v_ann:.3f}: {dsr:.3f} (PSR(0) {psr:.3f}); "
              f"umbral del sistema 0.95.")
    irs = []
    for k, r in out.items():
        if k.startswith("K1") or k.startswith("K2"):
            continue
        d_ = r - rbm
        irs.append(d_.mean() / d_.std(ddof=1) * math.sqrt(365))
    v_ir = float(np.var(irs, ddof=1))
    dsr_ir = metricas.sharpe_deflactado(list(dif), n_pruebas=len(irs), varianza_sharpes=v_ir, periodos_por_anio=365,
                                        varianza_anualizada=True)
    print(f"  DSR de la DIFERENCIA K3 - K1 (IR) con N = {len(irs)} variantes de filtro, V[IR] = {v_ir:.3f}: {dsr_ir:.3f}.")
    # temporadas no traslapadas: K3 - K1 y K4 - K4s
    C = caminos_ventanas(D)
    st = C["starts"]
    sel = np.flatnonzero((st - st[0]) % H == 0)
    Cn = {k: (v[sel] if isinstance(v, np.ndarray) and v.ndim >= 1 and len(v) == C["P"] else v) for k, v in C.items()}
    Cn["P"] = len(sel)
    s = {k: simular_cuenta(e, Cn) for k, e in (("K1", CANDIDATAS["K1"]), ("K3", CANDIDATAS["K3"]),
                                                ("K4", CANDIDATAS["K4"]), ("K4s", VARIANTES["K4s"]),
                                                ("K2", CANDIDATAS["K2"]))}
    for a, b, nom in (("K3", "K1", "filtro SMA200 (K3 - K1)"), ("K4", "K4s", "compra de caidas (K4 - K4s)"),
                      ("K4", "K2", "K4 - K2")):
        d_ = s[a]["R"] - s[b]["R"]
        se = d_.std(ddof=1) / math.sqrt(len(d_))
        print(f"  Temporadas de 122 dias no traslapadas (n = {len(d_)}), {nom}: media {d_.mean():+.2%}, mediana "
              f"{np.median(d_):+.2%}, EE {se:.2%}, t {d_.mean() / se:.2f}, IC95 [{d_.mean() - 1.96 * se:+.1%}, "
              f"{d_.mean() + 1.96 * se:+.1%}], gana en {np.mean(d_ > 0):.0%}.")
    k1 = s["K1"]["R"]
    se = k1.std(ddof=1) / math.sqrt(len(k1))
    print(f"  K1 por temporada (n = {len(k1)}): media {k1.mean():+.1%}, mediana {np.median(k1):+.1%}, sd {k1.std(ddof=1):.1%}, "
          f"IC95 de la media [{k1.mean() - 1.96 * se:+.1%}, {k1.mean() + 1.96 * se:+.1%}].")


def resumen_final(res_all: dict) -> None:
    print("\n## 7. Resumen compacto por metodo: mediana | P(-20%) | P(-30%) | P(tope) | DD mediano | P(1o) promedio F1-F4 "
          "con GBM A / b1.30 / b1.45 | P(1o) en F1 con A / b1.30 / b1.45")
    for et, v in res_all.items():
        print(f"  [{et}]")
        for k, esp in CANDIDATAS.items():
            s = v["res"][k]
            t = v["tabla"]
            print(f"    {esp['nombre']:42s} {fmt(np.median(s['R'])):>7s} | {np.mean(s['maxdd'] <= -0.2):5.1%} | "
                  f"{np.mean(s['maxdd'] <= -0.3):5.1%} | {np.mean(s['parado']):4.1%} | {fmt(np.median(s['maxdd'])):>6s} | "
                  + " / ".join(f"{t[(k, g)]['prom']:5.1%}" for g, _ in PIERNAS_PROPIAS) + " | "
                  + " / ".join(f"{t[(k, g)]['p1']['F1']:5.1%}" for g, _ in PIERNAS_PROPIAS))


# ------------------------------------------------------------------ principal
def correr(n_caminos: int) -> None:
    t0 = time.time()
    par = cargar_parametros()
    perfil = par["perfiles_riesgo"]["cripto_binance"]
    niveles = [c["nivel"] for c in perfil["cortacircuitos_drawdown"]]
    tope = perfil["perdida_maxima_tolerable_mxn"]["valor"]
    acciones = [c["accion"] for c in perfil["cortacircuitos_drawdown"]]
    assert tope == 5000 and niveles == [-0.2, -0.3, -0.4, -0.5], "el perfil cambio: revisar las reglas simuladas"
    assert "50%" in acciones[0] and "25%" in acciones[1] and "25%" in acciones[2], "cambiaron los topes de exposicion"
    D = cargar_datos()
    print(f"# Simulacion de la cartera cripto inicial arena-claude-binance (temporada 28-sep-2026 a 28-ene-2027, "
          f"{H} dias corridos)")
    print(f"Corrida: {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC. Corte: {CORTE} (cierre UTC). Semilla {SEMILLA}. "
          f"Trayectorias bootstrap: {n_caminos}. Bloque medio {BLOQUE} dias.")
    print(f"Perfil cripto_binance leido de config/parametros.json: tope {tope:,} MXN, cortacircuitos {niveles}, "
          f"ops/mes {perfil['operaciones_max_mes']}.")
    for c in perfil["cortacircuitos_drawdown"]:
        print(f"  {c['nivel']:+.0%}: {c['accion']}")
    seccion_datos(D)
    metricas_actuales(D)
    rng = np.random.default_rng(SEMILLA)
    resumen = {}
    print("\n## 2. Distribucion del rendimiento de la cuenta Binance a 4 meses (TWR en MXN, neto de costos) y torneo")
    print("  Columnas: P-x% = tocar un drawdown de x% desde el maximo (cierres diarios); P-50%/tope = cortacircuitos "
          "final (-50% o valor <= 5,000 MXN) -> todo a MXN; P(V<=5k) = valor minimo <= 5,000 MXN; DDmed/DDp90 = caida "
          "maxima mediana y del peor 10%; P-20%id = con minimos intradia; ops = operaciones (incluye MXN->USDT); "
          "opsmes>8 = P(algun mes con mas de 8 operaciones); expo.fin = exposicion BTC+ETH mediana al final; libera = "
          "P(el tope de exposicion se libera por nuevo maximo).")
    C = caminos_ventanas(D)
    evaluar_metodo(f"M1 ventanas moviles 2017-11 a 2026-05 (todas)", C, D, rng, resumen)
    C = caminos_ventanas(D, solo_regimen=True)
    evaluar_metodo("M1c ventanas moviles con BTC > SMA200 al inicio (regimen de hoy)", C, D, rng, resumen)
    C = caminos_ventanas(D, hasta=CORTE_PUBLICACION)
    evaluar_metodo("M1 antes de 2021 (in-sample de Detzel et al. 2021)", C, D, rng, resumen, variantes=True)
    C = caminos_ventanas(D, desde_f=CORTE_PUBLICACION)
    evaluar_metodo("M1 desde 2021 (post-publicacion)", C, D, rng, resumen, variantes=True)
    pool = pool_arrays(D, D["i0"])
    C = caminos_bootstrap(D, pool, n_caminos, rng, True, D["i0"])
    evaluar_metodo("M2 bootstrap 2017-11 a 2026-09, deriva historica", C, D, rng, resumen)
    i_rec = D["fechas"].index(INICIO_RECIENTE)
    pool_r = pool_arrays(D, i_rec)
    C = caminos_bootstrap(D, pool_r, n_caminos, rng, True, i_rec)
    evaluar_metodo("M2r bootstrap 2022-01 a 2026-09, deriva historica", C, D, rng, resumen)
    p3, info3 = ajustar_deriva(pool, D, "M3")
    print(f"\n  Deriva M3: SR de referencia del S&P {info3['sr_spx']:.2f}; BTC media aritmetica anual historica "
          f"{info3['rb'][0]:+.0%} -> {info3['rb'][1]:+.0%} (vol {info3['rb'][2]:.0%}); ETH {info3['re'][0]:+.0%} -> "
          f"{info3['re'][1]:+.0%} (vol {info3['re'][2]:.0%}).")
    C = caminos_bootstrap(D, p3, n_caminos, rng, True, D["i0"])
    evaluar_metodo("M3 bootstrap, deriva conservadora (Sharpe cripto = Sharpe S&P)", C, D, rng, resumen)
    p4, _ = ajustar_deriva(pool, D, "M4")
    C = caminos_bootstrap(D, p4, n_caminos, rng, True, D["i0"])
    evaluar_metodo("M4 bootstrap, prima cripto cero (cota pesimista)", C, D, rng, resumen, variantes=False)
    seccion_correlacion(D)
    seccion_significancia(D)
    resumen_final(resumen)
    print(f"\nTiempo de corrida: {time.time() - t0:.0f} s")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--caminos", type=int, default=20000)
    ap.add_argument("--salida", type=str, default=None)
    a = ap.parse_args(argv)
    if a.salida:
        buf = io.StringIO()
        with redirect_stdout(buf):
            correr(a.caminos)
        texto = buf.getvalue()
        ruta = Path(a.salida)
        if not ruta.is_absolute():
            ruta = RAIZ / ruta
        ruta.write_text(texto, encoding="utf-8")
        print(texto)
    else:
        correr(a.caminos)
    return 0


if __name__ == "__main__":
    sys.exit(main())
