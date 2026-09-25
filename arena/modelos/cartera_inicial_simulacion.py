#!/usr/bin/env python3
"""Cartera inicial de la cuenta arena-claude: simulacion de candidatas a 4 meses en MXN.

Pregunta del comite (viernes 25-sep-2026, despues del cierre): que cartera inicial maximiza la
probabilidad de terminar la temporada con el mayor TWR en MXN frente a los rivales (ChatGPT y Grok),
sin romper perfiles_riesgo.arena_agresivo de config/parametros.json.
ACTUALIZACION DEL DUENO (25-sep-2026): la temporada dura 4 MESES, del 28-sep-2026 al 28-ene-2027;
perdida maxima tolerada 10,000 MXN (-50%); la cartera se ejecuta en REAL el 28-sep (titulos enteros).

Uso (desde cualquier directorio):
    python3 arena/modelos/cartera_inicial_simulacion.py                  # 20,000 trayectorias por metodo
    python3 arena/modelos/cartera_inicial_simulacion.py --caminos 4000   # corrida rapida
    python3 arena/modelos/cartera_inicial_simulacion.py --salida arena/modelos/salida_cartera_inicial.txt

DATOS (nada posterior al cierre del 25-sep-2026; corte duro CORTE):
  * Yahoo Finance chart v8, interval=1d con period1/period2, cierre ajustado (adjclose): SPY, QQQ,
    SPXL, TQQQ, SPYM, QQQM, XLB, XLE, XLF, XLI, XLK, XLP, XLU, XLV, XLY, ^VIX. MXN=X horario (vela de
    15:00-16:00 de Nueva York) solo para los dias habiles que FRED aun no publica.
  * FRED: DEXMXUS (USD/MXN, mediodia de Nueva York, H.10) y DTB3 (T-bill 3 meses).
  * CETES 28: 6.15% anual (subasta de Banxico del 22-sep-2026, via cetes.app; fuente secundaria).
  * Precios por titulo en MXN = cierre en USD del 25-sep x USD/MXN a las 16:00 NY del 25-sep.

METODOS (todos con 'rendimientos en exceso historicos + tasas de hoy'):
  M1 Bootstrap estacionario (Politis y Romano, 1994) de vectores diarios conjuntos
     (exceso SPY, exceso QQQ, excesos sectoriales, USD/MXN, VIX) de 2011-09-26 a 2026-09-25 (15 anios),
     bloque medio de 21 dias. El primer bloque sale de dias con el regimen de hoy (SPY > SMA200 y
     VIX < 20 al cierre previo). La SMA200 arranca con los 200 cierres reales al 25-sep-2026.
  M2 Igual que M1 con deriva conservadora: prima del S&P de 5%/anio sobre el T-bill (media aritmetica),
     mismo Sharpe para Nasdaq-100 y sectores (sin premio por momentum), deriva cambiaria cero.
  M3 Ventanas moviles historicas de T dias habiles, un inicio por dia, 1999-12 a 2026-03, con la
     historia real de la SMA200, del VIX y de los cierres de mes. M3c: solo inicios en el regimen de hoy.
  Rendimiento diario en USD de un 1x = rf_hoy/252 + exceso historico. Apalancado 3x sintetico =
  rf_hoy/252 + 3 x exceso historico del subyacente - arrastre/252, con el arrastre anual calibrado
  contra SPXL y TQQQ reales en 2022-2026 (incluye gasto del fondo y diferencial de los swaps). El
  decaimiento por volatilidad sale solo del compuesto diario. En MXN: (1 + r_usd)(1 + r_fx) - 1.

REGLAS SIMULADAS (perfil arena_agresivo; interpretaciones marcadas con [I]):
  * Compra inicial al cierre del dia 0 (aprox. a la apertura del 28-sep) con comision 0.29% por lado
    mas spread: 0.10% ETF 1x de indice, 0.15% sectorial, 0.20% apalancado [I, doc 02 de la arena].
  * Senales al cierre de t, ejecucion al cierre de t+1 (rezago de 1 dia). Los stops se ejecutan al
    cierre del dia en que el precio cierra en o debajo del stop [I: sin datos intradia].
  * Filtros de apalancados: 'sma' (subyacente en USD > SMA200 diaria), 'sma_vix' (ademas VIX < 25, la
    regla vigente), 'r01' (SMA de 10 meses, cierre de mes, R01), 'bh' (sin filtro). Al perder el filtro
    se vende a CETES; al recuperarlo se recompra al peso objetivo.
  * Stop 'st3': perdida al stop = 3% del capital (riesgo_por_operacion); distancia = 0.03 x V / valor de la
    linea. Tras el stop, 10 dias habiles fuera; reentrada si el filtro (o la SMA200 del subyacente en 1x)
    esta activo.
  * Cortacircuitos sobre el indice TWR (drawdown desde el maximo): -12% vende ceil(n/2) de n titulos de
    cada linea tactica; -20% vende todos los apalancados y los 1x con subyacente debajo de su SMA200 (y
    mientras dure, no se compran apalancados); -28% pausa 10 dias; -35% todo a CETES hasta el final.
    Se liberan al marcar un nuevo maximo [I: el perfil no define la liberacion].
  * Limites de perdida semanal (10%) y mensual (18%): bloquean compras tacticas 5 y 21 dias [I].
  * Maximo 8 operaciones por bloque de 21 dias habiles (las ventas que reducen riesgo siempre pasan).
  * Rivales sin cortacircuitos, comprar y mantener, con ruido idiosincratico N(0, 3 pp) en el
    rendimiento de la temporada [I].
Todo es simulacion historica: no es pronostico ni recomendacion.
"""
from __future__ import annotations

import argparse
import bisect
import io
import json
import math
import sys
import time
import urllib.parse
from contextlib import redirect_stdout
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from herramientas import metricas  # noqa: E402
from herramientas.datos import UA_NAVEGADOR, URL_YAHOO, descargar, fred_serie  # noqa: E402
from herramientas.parametros import cargar_parametros  # noqa: E402

# ------------------------------------------------------------------ supuestos con fecha y fuente
CORTE = date(2026, 9, 25)                      # ultimo cierre usable
CAPITAL = 20_000.0
CETES_28 = 0.0615                              # subasta Banxico 22-sep-2026 (cetes.app; secundaria)
COMISION = 0.0029                              # 0.25% + IVA por lado (Guia de Servicios GBM, doc 01)
SPREAD = {"SPX1": 0.0010, "NDX1": 0.0010, "SEC1": 0.0015, "SEC2": 0.0015,
          "SPX3": 0.0020, "NDX3": 0.0020}      # [I] doc 02: desviacion mediana 0.04-0.17%
SUBYACENTE = {"SPX1": "SPX", "SPX3": "SPX", "NDX1": "NDX", "NDX3": "NDX", "SEC1": "SEC1", "SEC2": "SEC2"}
APALANCADOS = {"SPX3", "NDX3"}
SECTORES = ["XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY"]
FERIADOS_NYSE = {date(2026, 11, 26), date(2026, 12, 25), date(2027, 1, 1), date(2027, 1, 18)}
INICIO_TEMPORADA, FIN_TEMPORADA = date(2026, 9, 28), date(2027, 1, 28)   # 4 meses, fin incluido
INICIO_BOOT = date(2011, 9, 26)                # 15 anios de bootstrap
BLOQUE_MEDIO = 21
RUIDO_RIVAL = 0.03
NY = ZoneInfo("America/New_York")
P2 = int(datetime(2026, 9, 26, tzinfo=timezone.utc).timestamp())   # fin exclusivo de las descargas


# ------------------------------------------------------------------ descarga
def yahoo_diario(ticker: str) -> dict[date, float]:
    url = (URL_YAHOO + urllib.parse.quote(ticker, safe="") + "?" + urllib.parse.urlencode(
        {"period1": 0, "period2": P2, "interval": "1d", "events": "div,splits"}))
    res = json.loads(descargar(url, UA_NAVEGADOR, cache_horas=12))["chart"]["result"][0]
    off = int(res["meta"].get("gmtoffset", 0))
    q = res["indicators"]["quote"][0]
    adj = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose")
    out = {}
    for i, ts in enumerate(res.get("timestamp") or []):
        f = datetime.fromtimestamp(ts + off, tz=timezone.utc).date()
        if f > CORTE:
            continue
        v = adj[i] if adj and adj[i] is not None else q["close"][i]
        if v is not None and v > 0:
            out[f] = float(v)
    return out


def yahoo_cierre_nominal(ticker: str) -> tuple[date, float]:
    """Ultimo cierre NO ajustado (precio por titulo) en o antes de CORTE."""
    url = (URL_YAHOO + urllib.parse.quote(ticker, safe="") + "?" + urllib.parse.urlencode(
        {"range": "5d", "interval": "1d"}))
    res = json.loads(descargar(url, UA_NAVEGADOR, cache_horas=12))["chart"]["result"][0]
    off = int(res["meta"].get("gmtoffset", 0))
    q = res["indicators"]["quote"][0]
    mejor = None
    for i, ts in enumerate(res.get("timestamp") or []):
        f = datetime.fromtimestamp(ts + off, tz=timezone.utc).date()
        if f <= CORTE and q["close"][i] is not None:
            mejor = (f, float(q["close"][i]))
    return mejor


def fx_16h_ny() -> dict[date, float]:
    """USD/MXN al cierre de EUA (16:00 NY): cierre de la vela horaria que empieza a las 15:00 NY."""
    url = (URL_YAHOO + urllib.parse.quote("MXN=X", safe="") + "?" + urllib.parse.urlencode(
        {"range": "1mo", "interval": "1h"}))
    res = json.loads(descargar(url, UA_NAVEGADOR, cache_horas=12))["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    out = {}
    for i, ts in enumerate(res.get("timestamp") or []):
        loc = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(NY)
        if loc.hour == 15 and loc.minute == 0 and q["close"][i] is not None and loc.date() <= CORTE:
            out[loc.date()] = float(q["close"][i])
    return out


def ffill(d: dict, fechas: list[date]) -> np.ndarray:
    ks = sorted(d)
    out, j, ult = [], 0, np.nan
    for f in fechas:
        while j < len(ks) and ks[j] <= f:
            ult = d[ks[j]]
            j += 1
        out.append(ult)
    return np.array(out, dtype=float)


def serie(d: dict, fechas: list[date]) -> np.ndarray:
    return np.array([d.get(f, np.nan) for f in fechas], dtype=float)


def cargar_datos() -> dict:
    tickers = ["SPY", "QQQ", "SPXL", "TQQQ", "SPYM", "QQQM", "^VIX"] + SECTORES
    crudo = {t: yahoo_diario(t) for t in tickers}
    fechas = sorted(f for f in crudo["SPY"] if f >= date(1993, 11, 8))
    D = {"fechas": fechas}
    for t in tickers:
        D[t] = serie(crudo[t], fechas)
    D["^VIX"] = ffill(crudo["^VIX"], fechas)
    dex = dict(fred_serie("DEXMXUS", cache_horas=12))
    ult_dex = max(dex)
    fx16 = fx_16h_ny()
    fx = ffill(dex, fechas)
    for i, f in enumerate(fechas):          # dias sin DEXMXUS publicado: vela horaria de 16:00 NY
        if f > ult_dex and f in fx16:
            fx[i] = fx16[f]
    D["FX"] = fx
    D["FX_fuente"] = f"FRED DEXMXUS hasta {ult_dex}; Yahoo MXN=X 16:00 NY despues " \
                     f"({', '.join(f'{k}:{v:.4f}' for k, v in sorted(fx16.items()) if k > ult_dex)})"
    rf = fred_serie("DTB3", cache_horas=12)
    D["RF"] = ffill(dict(rf), fechas) / 100.0
    D["RF_hoy"] = float(D["RF"][-1])
    D["RF_hoy_fecha"] = max(f for f, _ in rf if f <= CORTE)
    D["fx_hoy"] = float(fx16.get(CORTE, fx[-1]))
    D["nominal"] = {t: yahoo_cierre_nominal(t) for t in ["SPYM", "QQQM", "SPXL", "TQQQ", "VOO", "IVV",
                                                           "QQQ"] + SECTORES}
    assert fechas[-1] == CORTE, f"El ultimo dia de SPY es {fechas[-1]}, no {CORTE}"
    return D


# ------------------------------------------------------------------ utilidades de series
def excesos(nivel: np.ndarray, rf: np.ndarray) -> np.ndarray:
    """x[i] = nivel[i]/nivel[i-1] - 1 - rf[i-1]/252 (x[0] = nan)."""
    x = np.full(len(nivel), np.nan)
    x[1:] = nivel[1:] / nivel[:-1] - 1 - rf[:-1] / 252
    return x


def estado_sma(nivel: np.ndarray, n: int = 200) -> np.ndarray:
    ok = np.zeros(len(nivel), bool)
    c = np.nancumsum(np.nan_to_num(nivel))
    for i in range(n - 1, len(nivel)):
        if np.isnan(nivel[i - n + 1:i + 1]).any():
            continue
        media = (c[i] - (c[i - n] if i >= n else 0.0)) / n
        ok[i] = nivel[i] > media
    return ok


def estado_r01(nivel: np.ndarray, fechas: list[date]) -> np.ndarray:
    """SMA de 10 meses (R01): estado vigente al cierre de cada dia = decision del ultimo cierre de mes <= dia."""
    fin_mes = [i for i in range(len(fechas) - 1) if fechas[i + 1].month != fechas[i].month] + [len(fechas) - 1]
    est = np.zeros(len(fechas), bool)
    ult, prev = False, 0
    cierres = []
    for k, i in enumerate(fin_mes):
        est[prev:i] = ult
        cierres.append(nivel[i])
        if len(cierres) >= 10 and not np.isnan(cierres[-10:]).any():
            ult = bool(nivel[i] > np.mean(cierres[-10:]))
        else:
            ult = False
        est[i] = ult
        prev = i + 1
    est[prev:] = ult
    return est


def calendario_temporada() -> list[date]:
    d, out = INICIO_TEMPORADA, []
    while d <= FIN_TEMPORADA:
        if d.weekday() < 5 and d not in FERIADOS_NYSE:
            out.append(d)
        d += timedelta(days=1)
    return out


def calibrar_arrastre(x_sub: np.ndarray, nivel_real: np.ndarray, rf: np.ndarray, desde: date,
                      fechas: list[date], L: int = 3) -> tuple[float, float, float]:
    r_real = np.full(len(nivel_real), np.nan)
    r_real[1:] = nivel_real[1:] / nivel_real[:-1] - 1
    m = np.array([f >= desde for f in fechas]) & ~np.isnan(r_real) & ~np.isnan(x_sub)
    xr, rr = x_sub[m], r_real[m]
    rfd = np.roll(rf, 1)[m] / 252
    objetivo = np.log1p(rr).sum()
    lo, hi = -0.05, 0.15
    for _ in range(80):
        d = (lo + hi) / 2
        if np.log1p(rfd + L * xr - d / 252).sum() > objetivo:
            lo = d
        else:
            hi = d
    sint = rfd + L * xr - d / 252
    return d, float(np.corrcoef(sint, rr)[0, 1]), float(np.std(sint - rr) * math.sqrt(252))


# ------------------------------------------------------------------ motor de simulacion
def simular(esp: dict, D: dict) -> dict:
    """Simula una cartera sobre P trayectorias de T dias. Devuelve arreglos por trayectoria."""
    P, T = D["P"], D["T"]
    lin = esp["lineas"]
    nL = len(lin)
    cb = esp.get("cb", True)
    c_cash = D["cash_d"]
    R = np.stack([D["R"][l["activo"]] for l in lin], axis=2) if nL else np.zeros((P, T, 0))
    costo = np.array([COMISION + SPREAD[l["activo"]] for l in lin])
    w = np.array([l["w"] for l in lin])
    n_tit = np.array([l.get("titulos", 2) for l in lin])
    frac_cb1 = np.ceil(n_tit / 2) / n_tit
    mult_mitad = np.floor(n_tit / 2) / n_tit
    tact = np.array([l.get("tactica", False) for l in lin])
    lev = np.array([l["activo"] in APALANCADOS for l in lin])
    stop_on = np.array([bool(l.get("stop", False)) for l in lin])
    filt = [D["sig"][(SUBYACENTE[l["activo"]], l["filtro"])] if l.get("filtro") else None for l in lin]
    sma_u = [D["sig"][(SUBYACENTE[l["activo"]], "sma")] for l in lin]
    mes = D["mes"]

    H = np.zeros((P, nL)); cash = np.ones(P)
    held = np.zeros((P, nL), bool); px = np.ones((P, nL)); stop_px = np.zeros((P, nL))
    halved = np.zeros((P, nL), bool); cooldown = np.zeros((P, nL), int)
    pend_sell = np.zeros((P, nL)); pend_buy = np.zeros((P, nL), bool)
    ops_tot = np.zeros(P, int); ops_mes = np.zeros(P, int); ops_mes_max = np.zeros(P, int)
    rot_mes = np.zeros(P); rot_mes_max = np.zeros(P)
    peak = np.ones(P); mindd = np.zeros(P); nivel_cb = np.zeros(P, int)
    pausa = np.full(P, -1); muerto = np.zeros(P, bool); bloq_tact = np.full(P, -1)
    f_dia = np.zeros(P, bool); f_sem = np.zeros(P, bool); f_mes = np.zeros(P, bool)
    n_stops = np.zeros(P, int); n_filtro = np.zeros(P, int)
    Vh = np.zeros((P, T + 1))

    V = cash.copy()
    for j in range(nL):                                     # compra inicial (dia 0)
        ok = np.ones(P, bool) if filt[j] is None else filt[j][:, 0].copy()
        amt = w[j] * V * ok
        H[:, j] += amt * (1 - costo[j]); cash -= amt
        held[:, j] = ok
        ops_tot += ok; ops_mes += ok; rot_mes += amt
        if stop_on[j]:
            stop_px[:, j] = np.where(ok, 1 - 0.03 * V / np.maximum(H[:, j], 1e-12), 0.0)
    ops_mes_max = np.maximum(ops_mes_max, ops_mes); rot_mes_max = np.maximum(rot_mes_max, rot_mes)
    V = cash + H.sum(1); Vh[:, 0] = V
    mindd = np.minimum(mindd, V / peak - 1)

    for t in range(1, T + 1):
        r = R[:, t - 1, :]
        H *= (1 + r); px *= (1 + r); cash *= (1 + c_cash)
        if mes[t] != mes[t - 1]:
            ops_mes[:] = 0; rot_mes[:] = 0.0
        Vpre = cash + H.sum(1)
        if (pend_sell > 0).any():                            # ventas pendientes (decididas en t-1)
            s = pend_sell * H
            cash += (s * (1 - costo)).sum(1); H -= s
            nv = (pend_sell > 0).sum(1)
            ops_tot += nv; ops_mes += nv; rot_mes += s.sum(1) / Vpre
            held &= ~(pend_sell >= 0.999)
            pend_sell[:] = 0.0
        if pend_buy.any():                                   # compras pendientes
            V = cash + H.sum(1)
            for j in range(nL):
                b = pend_buy[:, j]
                if not b.any():
                    continue
                mult = np.where(halved[:, j], mult_mitad[j], 1.0)
                amt = np.where(b, np.minimum(np.clip(w[j] * mult * V - H[:, j], 0, None), cash), 0.0)
                amt = np.where(amt > 0.02 * V, amt, 0.0)
                H[:, j] += amt * (1 - costo[j]); cash -= amt
                comp = amt > 0
                held[:, j] |= comp
                if stop_on[j]:
                    nuevo = px[:, j] * (1 - 0.03 * V / np.maximum(H[:, j], 1e-12))
                    stop_px[:, j] = np.where(comp, nuevo, stop_px[:, j])
                ops_tot += comp; ops_mes += comp; rot_mes += amt / V
            pend_buy[:] = False
        if stop_on.any():                                    # stops (mismo cierre)
            hit = held & stop_on[None, :] & (px <= stop_px)
            if hit.any():
                s = np.where(hit, H, 0.0)
                cash += (s * (1 - costo)).sum(1); H -= s
                held &= ~hit
                cooldown = np.where(hit, t + 10, cooldown)
                nh = hit.sum(1)
                ops_tot += nh; ops_mes += nh; rot_mes += s.sum(1) / Vpre; n_stops += nh
        V = cash + H.sum(1)
        Vh[:, t] = V
        nuevo_max = V >= peak
        peak = np.maximum(peak, V)
        dd = V / peak - 1
        mindd = np.minimum(mindd, dd)
        # limites de perdida
        f_dia |= (V / Vh[:, t - 1] - 1) <= -0.05
        rs = V / Vh[:, max(t - 5, 0)] - 1
        rm = V / Vh[:, max(t - 21, 0)] - 1
        f_sem |= rs <= -0.10; f_mes |= rm <= -0.18
        bloq_tact = np.where(rs <= -0.10, np.maximum(bloq_tact, t + 5), bloq_tact)
        bloq_tact = np.where(rm <= -0.18, np.maximum(bloq_tact, t + 21), bloq_tact)
        if cb:
            lib = nuevo_max & (nivel_cb > 0)
            nivel_cb[lib] = 0; halved[lib] = False
            lvl = (dd <= -0.12).astype(int) + (dd <= -0.20) + (dd <= -0.28) + (dd <= -0.35)
            L1 = (lvl >= 1) & (nivel_cb < 1)
            L3 = (lvl >= 3) & (nivel_cb < 3)
            L4 = (lvl >= 4) & (nivel_cb < 4)
            nivel_cb = np.maximum(nivel_cb, lvl)
            for j in range(nL):
                if tact[j]:
                    m = L1 & held[:, j] & ~halved[:, j]
                    pend_sell[m, j] = np.maximum(pend_sell[m, j], frac_cb1[j]); halved[m, j] = True
                en2 = (nivel_cb >= 2) & held[:, j]
                m2 = en2 if lev[j] else en2 & ~sma_u[j][:, t]
                pend_sell[m2, j] = 1.0
                m4 = L4 & held[:, j]
                pend_sell[m4, j] = 1.0
            pausa[L3] = t + 10
            muerto |= L4
        for j in range(nL):                                  # filtros de tendencia
            if filt[j] is not None:
                off = held[:, j] & ~filt[j][:, t] & (pend_sell[:, j] < 1)
                n_filtro += off
                pend_sell[off, j] = 1.0
        puede = ~muerto & (t >= pausa) & (ops_mes < 8)       # reentradas
        for j in range(nL):
            eleg = puede & ~held[:, j] & (t >= cooldown[:, j]) & (pend_sell[:, j] == 0)
            cond = filt[j][:, t] if filt[j] is not None else sma_u[j][:, t]
            if lev[j] and cb:
                cond = cond & (nivel_cb < 2)
            if tact[j]:
                cond = cond & (t >= bloq_tact)
            if mult_mitad[j] == 0:
                cond = cond & ~halved[:, j]
            pend_buy[:, j] = eleg & cond
        ops_mes_max = np.maximum(ops_mes_max, ops_mes); rot_mes_max = np.maximum(rot_mes_max, rot_mes)

    return {"twr": Vh[:, -1] - 1, "mindd": mindd, "ops": ops_tot, "ops_mes_max": ops_mes_max,
            "rot_mes_max": rot_mes_max, "f_dia": f_dia, "f_sem": f_sem, "f_mes": f_mes,
            "stops": n_stops, "salidas_filtro": n_filtro, "Vh": Vh}


# ------------------------------------------------------------------ construccion de escenarios
def rend_mxn(x_usd_exceso: np.ndarray, r_fx: np.ndarray, rf_hoy: float, L: int = 1, arrastre: float = 0.0):
    return (1 + rf_hoy / 252 + L * x_usd_exceso - arrastre / 252) * (1 + r_fx) - 1


def construir_ventanas(B: dict, T: int, solo_regimen: bool = False, desde: date | None = None,
                       hasta: date | None = None) -> dict:
    """M3: ventanas historicas reales (una por dia de inicio)."""
    f = B["fechas"]
    N = len(f)
    i0 = max(B["i_min"], 252)
    inicios = np.arange(i0, N - T)
    if desde:
        inicios = inicios[np.array([f[i] >= desde for i in inicios])]
    if hasta:
        inicios = inicios[np.array([f[i] <= hasta for i in inicios])]
    if solo_regimen:
        inicios = inicios[B["regimen"][inicios]]
    P = len(inicios)
    idx = inicios[:, None] + np.arange(1, T + 1)[None, :]
    idx0 = inicios[:, None] + np.arange(0, T + 1)[None, :]
    rfh, arr = B["rf_hoy"], B["arrastre"]
    R = {"SPX1": rend_mxn(B["x"]["SPX"][idx], B["rfx"][idx], rfh),
         "NDX1": rend_mxn(B["x"]["NDX"][idx], B["rfx"][idx], rfh),
         "SPX3": rend_mxn(B["x"]["SPX"][idx], B["rfx"][idx], rfh, 3, arr["SPX"]),
         "NDX3": rend_mxn(B["x"]["NDX"][idx], B["rfx"][idx], rfh, 3, arr["NDX"])}
    # sectores: los 2 mejores por 12-1 al inicio de cada ventana (sin mirar el futuro)
    niv_sec = np.stack([B["nivel"][s] for s in SECTORES])
    mom = niv_sec[:, inicios - 21] / niv_sec[:, inicios - 252] - 1
    orden = np.argsort(-np.nan_to_num(mom, nan=-9), axis=0)
    k1, k2 = orden[0], orden[1]
    x_sec = np.stack([B["x"][s] for s in SECTORES])
    sma_sec = np.stack([B["sma"][s] for s in SECTORES])
    R["SEC1"] = rend_mxn(x_sec[k1[:, None], idx], B["rfx"][idx], rfh)
    R["SEC2"] = rend_mxn(x_sec[k2[:, None], idx], B["rfx"][idx], rfh)
    vix = B["vix"][idx0]
    sig = {}
    for u, clave in (("SPX", "SPX"), ("NDX", "NDX")):
        s = B["sma"][clave][idx0]
        sig[(u, "sma")] = s
        sig[(u, "sma_vix")] = s & (vix < 25)
        sig[(u, "r01")] = B["r01"][clave][idx0]
    sig[("SEC1", "sma")] = sma_sec[k1[:, None], idx0]
    sig[("SEC2", "sma")] = sma_sec[k2[:, None], idx0]
    return {"P": P, "T": T, "R": R, "sig": sig, "cash_d": B["cash_d"], "mes": np.arange(T + 1) // 21,
            "inicios": inicios, "sectores_elegidos": (k1, k2)}


def construir_bootstrap(B: dict, T: int, P: int, semilla: int, conservador: bool = False,
                        condicionar: bool = True, cal: list[date] | None = None) -> dict:
    """M1/M2: bootstrap estacionario de vectores diarios conjuntos de los ultimos 15 anios."""
    rng = np.random.default_rng(semilla)
    f = B["fechas"]
    N = len(f)
    i0 = next(i for i, d in enumerate(f) if d >= INICIO_BOOT)
    muestra = np.arange(i0, N)
    M = len(muestra)
    x = {k: B["x"][k].copy() for k in ["SPX", "NDX"] + SECTORES}
    rfx = B["rfx"].copy()
    if conservador:
        s_spx = np.std(x["SPX"][muestra])
        mu_spx = 0.05 / 252
        for k in x:
            xm = x[k][muestra]
            x[k] = x[k] - np.mean(xm) + mu_spx * np.std(xm) / s_spx
        rfx = rfx - np.mean(rfx[muestra])
    reg = np.where(B["regimen"][muestra])[0] if condicionar else np.arange(M)
    pos = np.empty((P, T), dtype=np.int64)
    pos[:, 0] = rng.choice(reg, size=P)
    salto = rng.random((P, T)) < 1.0 / BLOQUE_MEDIO
    nuevo = rng.integers(0, M, size=(P, T))
    for t in range(1, T):
        pos[:, t] = np.where(salto[:, t], nuevo[:, t], (pos[:, t - 1] + 1) % M)
    idx = muestra[pos]
    rfh, arr = B["rf_hoy"], B["arrastre"]
    R = {"SPX1": rend_mxn(x["SPX"][idx], rfx[idx], rfh), "NDX1": rend_mxn(x["NDX"][idx], rfx[idx], rfh),
         "SPX3": rend_mxn(x["SPX"][idx], rfx[idx], rfh, 3, arr["SPX"]),
         "NDX3": rend_mxn(x["NDX"][idx], rfx[idx], rfh, 3, arr["NDX"])}
    s1, s2 = B["top_sectores_hoy"]
    R["SEC1"] = rend_mxn(x[s1][idx], rfx[idx], rfh)
    R["SEC2"] = rend_mxn(x[s2][idx], rfx[idx], rfh)
    vix = np.concatenate([np.full((P, 1), B["vix"][-1]), B["vix"][idx]], axis=1)
    sig = {}

    def niveles(clave: str, xs: np.ndarray) -> np.ndarray:
        pref = B["nivel"][clave][N - 200:]
        cam = np.cumprod(1 + rfh / 252 + xs[idx], axis=1) * pref[-1]
        return np.concatenate([np.tile(pref, (P, 1)), cam], axis=1)   # (P, 200+T)

    def sma_de(niv: np.ndarray) -> np.ndarray:
        c = np.cumsum(niv, axis=1)
        out = np.zeros((P, T + 1), bool)
        for t in range(T + 1):
            k = 199 + t
            media = (c[:, k] - (c[:, k - 200] if k >= 200 else 0)) / 200
            out[:, t] = niv[:, k] > media
        return out

    fin_mes_temp = [t for t in range(1, T + 1) if t == T or cal[t].month != cal[t - 1].month] if cal else []
    for u, clave in (("SPX", "SPX"), ("NDX", "NDX")):
        niv = niveles(clave, x[clave])
        s = sma_de(niv)
        sig[(u, "sma")] = s
        sig[(u, "sma_vix")] = s & (vix < 25)
        # R01: 9 cierres de mes reales previos + los simulados
        fm_reales = B["fin_mes_niveles"][clave][-9:]
        est = np.zeros((P, T + 1), bool)
        est[:, 0] = B["r01"][clave][-1]
        cierres = [np.full(P, v) for v in fm_reales]
        actual = est[:, 0].copy()
        for t in range(1, T + 1):
            if t in fin_mes_temp:
                cierres.append(niv[:, 199 + t])
                ult10 = np.stack(cierres[-10:], axis=1)
                actual = niv[:, 199 + t] > ult10.mean(axis=1)
            est[:, t] = actual
        sig[(u, "r01")] = est
    for k, s in (("SEC1", s1), ("SEC2", s2)):
        sig[(k, "sma")] = sma_de(niveles(s, x[s]))
    if cal:
        mes = np.array([0] + [(d.year - cal[0].year) * 12 + d.month - cal[0].month for d in cal[:T]])
    else:
        mes = np.arange(T + 1) // 21
    return {"P": P, "T": T, "R": R, "sig": sig, "cash_d": B["cash_d"], "mes": mes}


# ------------------------------------------------------------------ carteras
def carteras(precios_mxn: dict) -> tuple[dict, dict, dict]:
    """Candidatas con titulos enteros a precios del 25-sep (MXN) y rivales."""
    def w(tk, n):
        return n * precios_mxn[tk] / CAPITAL
    c = {}
    c["C0 CETES 100%"] = {"lineas": [], "cb": True}
    A = [{"activo": "SPX1", "w": w("SPYM", 7), "titulos": 7},
         {"activo": "NDX1", "w": w("QQQM", 1), "titulos": 1}]
    c["A 7 SPYM + 1 QQQM (+CETES)"] = {"lineas": A, "cb": True}
    c["A st3 (stop 3% por linea)"] = {"lineas": [dict(l, stop=True) for l in A], "cb": True}
    B1 = lambda f, st_lev=False, st_all=False: [
        {"activo": "SPX3", "w": w("SPXL", 1), "titulos": 1, "filtro": f, "tactica": True, "stop": st_lev or st_all},
        {"activo": "SPX1", "w": w("SPYM", 5), "titulos": 5, "stop": st_all},
        {"activo": "NDX1", "w": w("QQQM", 1), "titulos": 1, "stop": st_all}]
    B2 = lambda f, st_lev=False, st_all=False: [
        {"activo": "NDX3", "w": w("TQQQ", 7), "titulos": 7, "filtro": f, "tactica": True, "stop": st_lev or st_all},
        {"activo": "SPX1", "w": w("SPYM", 6), "titulos": 6, "stop": st_all}]
    for nombre, fn in (("B1 1 SPXL + 5 SPYM + 1 QQQM", B1), ("B2 7 TQQQ + 6 SPYM", B2)):
        c[f"{nombre} | bh"] = {"lineas": fn(None), "cb": True}
        c[f"{nombre} | sma"] = {"lineas": fn("sma"), "cb": True}
        c[f"{nombre} | sma_vix"] = {"lineas": fn("sma_vix"), "cb": True}
        c[f"{nombre} | r01"] = {"lineas": fn("r01"), "cb": True}
        c[f"{nombre} | sma_vix+st3 apal."] = {"lineas": fn("sma_vix", st_lev=True), "cb": True}
        c[f"{nombre} | sma_vix+st3 todas"] = {"lineas": fn("sma_vix", st_all=True), "cb": True}
    C = [{"activo": "SPX1", "w": 0.50, "titulos": 6},
         {"activo": "SEC1", "w": 0.25, "titulos": 5, "tactica": True},
         {"activo": "SEC2", "w": 0.25, "titulos": 2, "tactica": True}]
    c["C 50% S&P + 2x25% sectores top 12-1"] = {"lineas": C, "cb": True}
    c["C st3 (stop 3% por linea)"] = {"lineas": [dict(l, stop=True) for l in C], "cb": True}
    rivales = {
        "R1 beta 1 S&P (100%)": {"lineas": [{"activo": "SPX1", "w": 1.0}], "cb": False},
        "R2 mixta 50% S&P + 50% CETES": {"lineas": [{"activo": "SPX1", "w": 0.5}], "cb": False},
        "R3 agresiva 50% TQQQ + 50% QQQ": {"lineas": [{"activo": "NDX3", "w": 0.5}, {"activo": "NDX1", "w": 0.5}],
                                            "cb": False},
    }
    campos = {"F1 {R1,R2}": ["R1 beta 1 S&P (100%)", "R2 mixta 50% S&P + 50% CETES"],
              "F2 {R2,R3}": ["R2 mixta 50% S&P + 50% CETES", "R3 agresiva 50% TQQQ + 50% QQQ"]}
    return c, rivales, campos


# ------------------------------------------------------------------ resumen
def pct(a, q):
    return float(np.percentile(a, q))


def evaluar(cands: dict, rivales: dict, campos: dict, D: dict, semilla: int) -> dict:
    rng = np.random.default_rng(semilla + 99)
    res_r = {k: simular(v, D) for k, v in rivales.items()}
    ruido = {k: rng.normal(0, RUIDO_RIVAL, D["P"]) for k in rivales}
    tw_r = {k: res_r[k]["twr"] + ruido[k] for k in rivales}
    out = {"_rivales": res_r}
    for nombre, esp in cands.items():
        r = simular(esp, D)
        fila = {"med": np.median(r["twr"]), "p10": pct(r["twr"], 10), "p90": pct(r["twr"], 90),
                "media": float(np.mean(r["twr"])),
                "p12": float(np.mean(r["mindd"] <= -0.12)), "p20": float(np.mean(r["mindd"] <= -0.20)),
                "p28": float(np.mean(r["mindd"] <= -0.28)), "p35": float(np.mean(r["mindd"] <= -0.35)),
                "p50": float(np.mean(r["twr"] <= -0.50)), "pneg": float(np.mean(r["twr"] < 0)),
                "ops": float(np.mean(r["ops"])), "ops8": float(np.mean(r["ops_mes_max"] > 8)),
                "rot15": float(np.mean(r["rot_mes_max"] > 1.5)),
                "fdia": float(np.mean(r["f_dia"])), "fsem": float(np.mean(r["f_sem"])),
                "fmes": float(np.mean(r["f_mes"])), "stops": float(np.mean(r["stops"])),
                "twr": r["twr"], "Vh": r["Vh"]}
        for cn, rv in campos.items():
            mx = np.max(np.stack([tw_r[k] for k in rv]), axis=0)
            fila[cn] = float(np.mean(r["twr"] > mx))
        for k in rivales:
            fila["vs " + k[:2]] = float(np.mean(r["twr"] > tw_r[k]))
        out[nombre] = fila
    # P(primero) de cada rival en cada campo contra la mejor alternativa de Claude no se reporta:
    # solo la de cada rival contra el otro rival y contra A (referencia)
    out["_tw_r"] = tw_r
    return out


def tabla(res: dict, campos: dict, titulo: str) -> str:
    s = io.StringIO()
    print(f"\n### {titulo}", file=s)
    enc = (f"{'candidata':44s} {'mediana':>8s} {'p10':>7s} {'p90':>7s} {'media':>7s} {'P-12%':>6s} {'P-20%':>6s}"
           f" {'P-35%':>6s} {'P<0':>5s} " + " ".join(f"{c.split()[0] + ' 1o':>7s}" for c in campos) +
           f" {'>R1':>5s} {'>R2':>5s} {'>R3':>5s} {'ops':>5s} {'stops':>5s} {'dia-5%':>6s}")
    print(enc, file=s)
    for k, f in res.items():
        if k.startswith("_"):
            continue
        print(f"{k:44s} {f['med']:+8.1%} {f['p10']:+7.1%} {f['p90']:+7.1%} {f['media']:+7.1%} {f['p12']:6.1%}"
              f" {f['p20']:6.1%} {f['p35']:6.1%} {f['pneg']:5.0%} " + " ".join(f"{f[c]:7.1%}" for c in campos) +
              f" {f['vs R1']:5.0%} {f['vs R2']:5.0%} {f['vs R3']:5.0%} {f['ops']:5.1f} {f['stops']:5.2f}"
              f" {f['fdia']:6.1%}", file=s)
    rr = res["_rivales"]
    for k, r in rr.items():
        print(f"  rival {k:36s} {np.median(r['twr']):+8.1%} {pct(r['twr'], 10):+7.1%} {pct(r['twr'], 90):+7.1%}"
              f" {np.mean(r['twr']):+7.1%} {np.mean(r['mindd'] <= -0.12):6.1%} {np.mean(r['mindd'] <= -0.20):6.1%}"
              f" (sin ruido)", file=s)
    return s.getvalue()


# ------------------------------------------------------------------ principal
def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--caminos", type=int, default=20000)
    ap.add_argument("--semilla", type=int, default=20260925)
    ap.add_argument("--salida", type=str, default=None)
    a = ap.parse_args(argv)
    buf = io.StringIO()
    t0 = time.time()
    with redirect_stdout(buf):
        correr(a.caminos, a.semilla)
        print(f"\nTiempo de corrida: {time.time() - t0:.0f} s")
    texto = buf.getvalue()
    print(texto)
    if a.salida:
        Path(a.salida).write_text(texto, encoding="utf-8")
    return 0


def correr(caminos: int, semilla: int) -> None:
    prm = cargar_parametros()["perfiles_riesgo"]["arena_agresivo"]
    print("# Simulacion de la cartera inicial arena-claude (temporada de 4 meses: 28-sep-2026 a 28-ene-2027)")
    print(f"Corrida: {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC. Corte de datos: {CORTE} (cierre). "
          f"Semilla {semilla}. Trayectorias bootstrap: {caminos}.")
    print(f"Perfil leido de config/parametros.json: cortacircuitos "
          f"{[c['nivel'] for c in prm['cortacircuitos_drawdown']]}, apalancado_max "
          f"{prm['concentracion']['etf_apalancado_max']}, indice_max {prm['concentracion']['etf_indice_max']}, "
          f"riesgo/op {prm['riesgo_por_operacion']}, kelly_max {prm['kelly_fraccion_max']}, "
          f"ops/mes {prm['operaciones_max_mes']}, orden minima {prm['orden_minima_mxn']} MXN")
    D = cargar_datos()
    f = D["fechas"]
    N = len(f)
    cal = calendario_temporada()
    T = len(cal)
    print(f"Calendario de la temporada: {T} dias habiles de NYSE, {cal[0]} a {cal[-1]} "
          f"(feriados NYSE: 26-nov, 25-dic, 1-ene, 18-ene).")
    print(f"USD/MXN: {D['FX_fuente']}. USD/MXN usado para precios por titulo: {D['fx_hoy']:.4f}.")
    print(f"T-bill 3m (FRED DTB3, {D['RF_hoy_fecha']}): {D['RF_hoy']:.2%}. CETES 28: {CETES_28:.2%}.")

    # ---------------- construccion de insumos comunes
    B = {"fechas": f, "rfx": np.full(N, np.nan), "x": {}, "nivel": {}, "sma": {}, "r01": {},
         "fin_mes_niveles": {}}
    B["rfx"][1:] = D["FX"][1:] / D["FX"][:-1] - 1
    niveles = {"SPX": D["SPY"], "NDX": D["QQQ"]}
    niveles.update({s: D[s] for s in SECTORES})
    for k, niv in niveles.items():
        B["nivel"][k] = niv
        B["x"][k] = excesos(niv, D["RF"])
        B["sma"][k] = estado_sma(niv)
    for k in ("SPX", "NDX"):
        B["r01"][k] = estado_r01(niveles[k], f)
        fm = [i for i in range(N - 1) if f[i + 1].month != f[i].month]
        B["fin_mes_niveles"][k] = niveles[k][fm]
    B["vix"] = D["^VIX"]
    B["regimen"] = np.zeros(N, bool)
    B["regimen"][1:] = B["sma"]["SPX"][:-1] & (B["vix"][:-1] < 20)   # estado al cierre previo
    B["i_min"] = next(i for i in range(N) if not np.isnan(D["QQQ"][i]) and not np.isnan(D["XLK"][i])) + 252
    B["rf_hoy"] = D["RF_hoy"]
    dias_temp = (cal[-1] - date(2026, 9, 25)).days
    B["cash_d"] = (1 + CETES_28 * dias_temp / 360) ** (1 / T) - 1
    arr = {}
    print("\n## 1. Calibracion de los apalancados sinteticos (3 x exceso diario - arrastre)")
    for u, real, x in (("SPX", "SPXL", B["x"]["SPX"]), ("NDX", "TQQQ", B["x"]["NDX"])):
        for desde in (date(2010, 3, 1), date(2022, 1, 3)):
            d, c, te = calibrar_arrastre(x, D[real], D["RF"], desde, f)
            print(f"  {real} desde {desde}: arrastre anual {d:.2%} (ademas del financiamiento a T-bill); "
                  f"corr diaria {c:.4f}; TE {te:.2%}")
        arr[u] = d                                     # se usa el de 2022-2026
    B["arrastre"] = arr
    print(f"  Usado en la simulacion: SPX3 {arr['SPX']:.2%}/anio, NDX3 {arr['NDX']:.2%}/anio (2022-2026).")

    # ---------------- precios por titulo y estado actual
    fxh = D["fx_hoy"]
    precios = {t: v[1] * fxh for t, v in D["nominal"].items()}
    print("\n## 2. Precio por titulo al cierre del 25-sep (USD x USD/MXN 16:00 NY)")
    for t in ["SPYM", "QQQM", "SPXL", "TQQQ", "VOO", "IVV", "QQQ"]:
        fch, p = D["nominal"][t]
        print(f"  {t:5s} {fch} USD {p:9.2f} -> {precios[t]:9.1f} MXN = {precios[t] / CAPITAL:6.1%} de 20,000")
    mom121 = {s: D[s][-22] / D[s][-253] - 1 for s in SECTORES}
    top = sorted(SECTORES, key=lambda s: -mom121[s])[:2]
    B["top_sectores_hoy"] = tuple(top)
    print("  Sectores por momentum 12-1 (USD): " + ", ".join(f"{s} {mom121[s]:+.1%}" for s in
                                                             sorted(SECTORES, key=lambda s: -mom121[s])))
    print(f"  C usa hoy: {top[0]} y {top[1]}.")
    metricas_actuales(D, B, precios)

    cands, rivales, campos = carteras(precios)
    print("\n## 4. Carteras (pesos por titulos enteros al 25-sep)")
    for k, e in list(cands.items()) + list(rivales.items()):
        if "|" in k and "bh" not in k:
            continue
        ls = ", ".join(f"{l['activo']} {l['w']:.1%}" + (f" ({l['titulos']} tit.)" if "titulos" in l else "")
                       for l in e["lineas"])
        print(f"  {k:44s} {ls}; CETES {1 - sum(l['w'] for l in e['lineas']):.1%}")
    print("  Equivalencias: SPX1 = SPYM (S&P 500), NDX1 = QQQM (Nasdaq-100), SPX3 = SPXL, NDX3 = TQQQ, "
          "SEC1/SEC2 = 2 sectoriales SPDR con mayor 12-1.")
    print("  Nota: B con 2 SPXL pesaria >50% (tope apalancado) y 8 SPYM >60% (tope indice): no caben hoy.")

    # ---------------- metodos
    resultados = {}
    print("\n## 5. Resultados por metodo (TWR de la temporada de 4 meses en MXN; P-12%/P-20%/P-35% = tocar ese "
          "drawdown desde el maximo; P<0 = terminar con perdida; '1o' = terminar arriba de ambos rivales del campo)")
    print("Campos: F1 = {R1 beta 1 S&P, R2 mixta 50/50} (supuesto pedido); "
          "F2 = {R2 mixta, R3 agresiva 2x Nasdaq} (sensibilidad 'Grok agresivo').")
    D1 = construir_bootstrap(B, T, caminos, semilla, conservador=False, condicionar=True, cal=cal)
    resultados["M1"] = evaluar(cands, rivales, campos, D1, semilla)
    print(tabla(resultados["M1"], campos, "M1 bootstrap 15 anios (2011-2026), inicio en regimen de hoy, deriva historica"))
    del D1
    D2 = construir_bootstrap(B, T, caminos, semilla + 1, conservador=True, condicionar=True, cal=cal)
    resultados["M2"] = evaluar(cands, rivales, campos, D2, semilla + 1)
    print(tabla(resultados["M2"], campos, "M2 bootstrap 15 anios, deriva conservadora (prima S&P 5%, "
                                          "mismo Sharpe Nasdaq/sectores, peso sin deriva)"))
    del D2
    D3 = construir_ventanas(B, T)
    print(f"\nM3: {D3['P']} ventanas, inicios {f[D3['inicios'][0]]} a {f[D3['inicios'][-1]]}")
    resultados["M3"] = evaluar(cands, rivales, campos, D3, semilla + 2)
    print(tabla(resultados["M3"], campos, "M3 ventanas moviles 1999-2026 (todas)"))
    D3c = construir_ventanas(B, T, solo_regimen=True)
    print(f"\nM3c: {D3c['P']} ventanas en el regimen de hoy (SPY>SMA200 y VIX<20 al inicio)")
    resultados["M3c"] = evaluar(cands, rivales, campos, D3c, semilla + 3)
    print(tabla(resultados["M3c"], campos, "M3c ventanas moviles en el regimen de hoy"))
    # dentro / fuera de muestra del filtro (Gayed-Bilello publicado en 2016-03)
    for et, (d0, d1) in (("antes de 2016-03 (dentro de muestra del filtro)", (None, date(2016, 3, 1))),
                         ("desde 2016-03 (fuera de muestra, post-publicacion)", (date(2016, 3, 1), None))):
        Dx = construir_ventanas(B, T, desde=d0, hasta=d1)
        sel = {k: v for k, v in cands.items() if k.startswith("B") or k.startswith("A 7")}
        rx = evaluar(sel, rivales, campos, Dx, semilla + 4)
        print(tabla(rx, campos, f"M3 {et}: {Dx['P']} ventanas"))

    # ---------------- ventaja, t y DSR
    ventaja_y_dsr(B, T, cands, rivales, D3, resultados["M3"])
    kelly(B, T, cands, caminos, semilla, cal)
    resumen_final(resultados, campos)


def metricas_actuales(D: dict, B: dict, precios: dict) -> None:
    f = D["fechas"]
    N = len(f)
    fx = D["FX"]
    print("\n## 3. Metricas actuales al 25-sep-2026 (en MXN; USD/MXN de FRED mediodia + 16:00 NY al final)")
    print(f"{'serie':10s} {'3m':>7s} {'6m':>7s} {'12-1':>7s} {'vs SMA200 USD':>13s} {'vol60 MXN':>9s} "
          f"{'DDmax 1a':>8s} {'corr60 S&P':>10s} {'corr 1a':>7s}")
    mx = {}
    for t in ["SPY", "SPYM", "QQQM", "QQQ", "SPXL", "TQQQ"] + list(B["top_sectores_hoy"]):
        mx[t] = D[t] * fx
    base = mx["SPY"]
    rb = base[1:] / base[:-1] - 1

    def i_meses(n):
        objetivo = date(f[-1].year + (f[-1].month - n - 1) // 12, (f[-1].month - n - 1) % 12 + 1, f[-1].day)
        return bisect.bisect_right(f, objetivo) - 1

    for t, s in mx.items():
        r = s[1:] / s[:-1] - 1
        i3, i6, i12, i1 = i_meses(3), i_meses(6), i_meses(12), i_meses(1)
        usd = D[t]
        sma = np.nanmean(usd[-200:])
        ult = s[-253:]
        dd = np.min(ult / np.maximum.accumulate(ult) - 1)
        v60 = np.nanstd(r[-60:]) * math.sqrt(252)
        c60 = np.corrcoef(r[-60:], rb[-60:])[0, 1]
        c1a = np.corrcoef(r[-252:], rb[-252:])[0, 1]
        print(f"{t:10s} {s[-1] / s[i3] - 1:+7.1%} {s[-1] / s[i6] - 1:+7.1%} {s[i1] / s[i12] - 1:+7.1%} "
              f"{usd[-1] / sma - 1:+13.1%} {v60:9.1%} {dd:+8.1%} {c60:10.2f} {c1a:7.2f}")
    r_fx = fx[1:] / fx[:-1] - 1
    print(f"{'USD/MXN':10s} {fx[-1] / fx[i_meses(3)] - 1:+7.1%} {fx[-1] / fx[i_meses(6)] - 1:+7.1%} "
          f"{fx[i_meses(1)] / fx[i_meses(12)] - 1:+7.1%} {fx[-1] / np.mean(fx[-200:]) - 1:+13.1%} "
          f"{np.std(r_fx[-60:]) * math.sqrt(252):9.1%} {'':>8s} {np.corrcoef(r_fx[-60:], rb[-60:])[0, 1]:10.2f} "
          f"{np.corrcoef(r_fx[-252:], rb[-252:])[0, 1]:7.2f}")
    print(f"VIX {D['^VIX'][-1]:.2f} ({f[-1]}); percentil 5 anios "
          f"{np.mean(D['^VIX'][-1260:] <= D['^VIX'][-1]):.0%}. SPY vs SMA200 (USD) "
          f"{D['SPY'][-1] / np.mean(D['SPY'][-200:]) - 1:+.1%}; QQQ {D['QQQ'][-1] / np.mean(D['QQQ'][-200:]) - 1:+.1%}.")
    print("Filtro de apalancados hoy: SPY>SMA200 " + str(bool(B["sma"]["SPX"][-1])) + ", QQQ>SMA200 " +
          str(bool(B["sma"]["NDX"][-1])) + f", VIX<25 {bool(D['^VIX'][-1] < 25)}; R01 (SMA10 al 31-ago) SPY "
          f"{bool(B['r01']['SPX'][-1])}, QQQ {bool(B['r01']['NDX'][-1])}.")
    # distancia al disparo del filtro, en sigmas de 4 meses
    for u, tk in (("SPX", "SPY"), ("NDX", "QQQ")):
        niv = D[tk]
        dist = niv[-1] / np.mean(niv[-200:]) - 1
        r = niv[1:] / niv[:-1] - 1
        v = np.std(r[-60:]) * math.sqrt(252)
        print(f"  {tk}: distancia a SMA200 {dist:+.1%} = {dist / (v * math.sqrt(1 / 3)):.2f} sigmas de 4 meses "
              f"(vol 60d USD {v:.1%}).")


def ventaja_y_dsr(B, T, cands, rivales, D3, res3) -> None:
    """Ventaja por temporada contra R1 y contra CETES; t ~ SR x sqrt(T); DSR con las variantes probadas."""
    print("\n## 6. Ventaja neta estimada y significancia (M3, 1999-2026)")
    inicios = D3["inicios"]
    P = len(inicios)
    nonov = np.arange(0, P, T)                     # temporadas sin traslape (desfase 0)
    n_ind = len(nonov)
    anios = n_ind * T / 252
    r1 = simular(rivales["R1 beta 1 S&P (100%)"], D3)["twr"]
    cet = (1 + D3["cash_d"]) ** T - 1
    print(f"Temporadas independientes (sin traslape): {n_ind} (~{anios:.1f} anios). "
          f"CETES por temporada: {cet:.2%}.")
    print(f"{'candidata':44s} {'E[R-R1]':>8s} {'IC95':>17s} {'P(R>R1)':>8s} {'SR_ann vs R1':>12s} {'t':>5s} "
          f"{'E[R-CETES]':>10s} {'SR_ann':>7s} {'t':>5s}")
    srs, series = {}, {}
    for k, fila in res3.items():
        if k.startswith("_"):
            continue
        d = fila["twr"] - r1
        m, s = float(np.mean(d[nonov])), float(np.std(d[nonov], ddof=1))
        e = fila["twr"] - cet
        me, se = float(np.mean(e[nonov])), float(np.std(e[nonov], ddof=1))
        k_ann = math.sqrt(252 / T)
        sr_d = k_ann * m / s if s > 0 else float("nan")
        sr_e = k_ann * me / se if se > 0 else float("nan")
        ic = (m - 1.96 * s / math.sqrt(n_ind), m + 1.96 * s / math.sqrt(n_ind))
        print(f"{k:44s} {m:+8.2%} [{ic[0]:+7.2%},{ic[1]:+7.2%}] {np.mean(d > 0):8.0%} {sr_d:12.2f} "
              f"{sr_d * math.sqrt(anios):5.2f} {me:+10.2%} {sr_e:7.2f} {sr_e * math.sqrt(anios):5.2f}")
        # serie diaria encadenada (temporadas sin traslape) para el DSR
        Vh = fila["Vh"][nonov]
        rd = (Vh[:, 1:] / Vh[:, :-1] - 1).ravel()
        series[k] = rd
        ex = rd - D3["cash_d"]
        srs[k] = float(np.mean(ex) / np.std(ex)) if np.std(ex) > 0 else 0.0
    vals = np.array([v for k, v in srs.items() if not k.startswith("C0")])
    V = float(np.var(vals, ddof=1))
    n_pr = len(vals)
    print(f"\nDSR (Bailey y Lopez de Prado 2014) sobre la serie diaria encadenada, N = {n_pr} variantes, "
          f"V[SR diario] = {V:.2e}:")
    for k, rd in series.items():
        if k.startswith("C0"):
            continue
        ex = rd - D3["cash_d"]
        sr = float(np.mean(ex) / np.std(ex))
        try:
            dsr = metricas.dsr_desde_estadisticos(sr, len(ex), n_pr, V, metricas.asimetria(list(ex)),
                                                  metricas.curtosis(list(ex)))
            psr = metricas.psr_desde_estadisticos(sr, len(ex), metricas.asimetria(list(ex)),
                                                  metricas.curtosis(list(ex)))
        except ValueError:
            dsr = psr = float("nan")
        print(f"  {k:44s} SR anual vs CETES {sr * math.sqrt(252):5.2f}  PSR(0) {psr:.3f}  DSR {dsr:.3f}")
    # SR del diferencial diario contra R1 (IR) para B y A
    r1v = simular(rivales["R1 beta 1 S&P (100%)"], D3)["Vh"][nonov]
    r1d = (r1v[:, 1:] / r1v[:, :-1] - 1).ravel()
    print("\nRazon de informacion diaria contra R1 (serie encadenada) y t = IR x sqrt(anios):")
    for k, rd in series.items():
        if k.startswith("C0"):
            continue
        d = rd - r1d
        ir = float(np.mean(d) / np.std(d) * math.sqrt(252)) if np.std(d) > 0 else float("nan")
        print(f"  {k:44s} IR {ir:5.2f}  t {ir * math.sqrt(anios):5.2f}")


def kelly(B, T, cands, caminos, semilla, cal) -> None:
    print("\n## 7. Kelly: fraccion de Kelly de cada cartera (sin reglas), escala k* = mu_e/sigma^2 sobre CETES")
    print("Si k* < 2 la cartera ya esta arriba de medio Kelly (kelly_fraccion_max = 0.5).")
    for nombre, cons in (("M1 deriva historica 2011-2026", False), ("M2 deriva conservadora", True)):
        Dk = construir_bootstrap(B, T, min(caminos, 8000), semilla + 7, conservador=cons, condicionar=False, cal=cal)
        linea = []
        for k in ["A 7 SPYM + 1 QQQM (+CETES)", "B1 1 SPXL + 5 SPYM + 1 QQQM | bh", "B2 7 TQQQ + 6 SPYM | bh",
                  "C 50% S&P + 2x25% sectores top 12-1"]:
            esp = {"lineas": [dict(l, filtro=None, stop=False) for l in cands[k]["lineas"]], "cb": False}
            Vh = simular(esp, Dk)["Vh"]
            rd = (Vh[:, 1:] / Vh[:, :-1] - 1).ravel() - Dk["cash_d"]
            mu, var = float(np.mean(rd)) * 252, float(np.var(rd)) * 252
            ks = mu / var if var > 0 else float("nan")
            linea.append(f"{k.split('|')[0].strip()[:26]}: mu_e {mu:+.1%} sigma {math.sqrt(var):.1%} k* {ks:.2f} "
                         f"-> fraccion de Kelly {1 / ks if ks > 0 else float('inf'):.2f}")
        print(f"  [{nombre}]")
        for x in linea:
            print("    " + x)


def resumen_final(resultados: dict, campos: dict) -> None:
    print("\n## 8. Resumen compacto (M1 | M2 | M3 | M3c): mediana, P(-12%), P(-20%), P(1o en F1), P(1o en F2)")
    claves = [k for k in resultados["M1"] if not k.startswith("_")]
    for k in claves:
        partes = []
        for m in ("M1", "M2", "M3", "M3c"):
            f = resultados[m][k]
            partes.append(f"{f['med']:+.1%} {f['p12']:.0%} {f['p20']:.0%} {f['F1 {R1,R2}']:.0%} {f['F2 {R2,R3}']:.0%}")
        print(f"{k:44s} " + " | ".join(partes))


if __name__ == "__main__":
    raise SystemExit(main())
