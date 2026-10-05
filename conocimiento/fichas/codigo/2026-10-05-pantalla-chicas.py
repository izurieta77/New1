"""Ficha 2026-10-05: pantalla de empresas chicas con utilidades, operables desde GBM (papel, fase 0).

Subcomandos (todo con datos publicos, sin credenciales):
    python3 conocimiento/fichas/codigo/2026-10-05-pantalla-chicas.py operabilidad   # lista BMV/SIC + liquidez + costo
    python3 conocimiento/fichas/codigo/2026-10-05-pantalla-chicas.py pantalla       # filtros F1-F9 + 2a fuente EDGAR + alertas 8-K
    python3 conocimiento/fichas/codigo/2026-10-05-pantalla-chicas.py backtest       # prueba pre-registrada 2015-2025
    python3 conocimiento/fichas/codigo/2026-10-05-pantalla-chicas.py todo

Fuentes: BMV (BmvJsonGeneric: series operadas del mercado local y del SIC), Yahoo chart v8 (.MX para MXN, liquidez,
spread Corwin-Schultz), Yahoo fundamentals-timeseries (fundamentales; sin credencial), SEC EDGAR (frames para el
backtest; companyfacts via herramientas/edgar.py como segunda fuente). Cache en datos/cache/chicas (ignorado por git).
Los PARAMS estan congelados segun el registro previo de la ficha (seccion 0).
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
import os
import random
import re
import statistics as st
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))
os.environ.setdefault("SEC_USER_AGENT", "SistemaInversionNew1 izurieta77@gmail.com")
from herramientas import edgar  # noqa: E402

SALIDA = RAIZ / "arena" / "investigacion"
CACHE = RAIZ / "datos" / "cache" / "chicas"
HOY = date(2026, 10, 5)

# ------------------------------------------------------------------ PARAMETROS CONGELADOS (registro previo)
PARAMS = dict(
    mcap_min_usd=300e6, mcap_max_usd=5000e6,
    ni_anios_pos=3, ni_crec_2a=1.20, udm_vs_anual=0.90,
    roic_min=0.12, nd_ebitda_max=2.0, fcf_ni_min=0.60, ev_ebit_max=15.0, dilucion_max=1.10,
    liq_mediana_mxn_min=500_000, liq_dias_min=0.90, spread_max=0.015, titulo_max_mxn=2500,
    top_n=15,
    capital_mxn=10_000, pos_max_mxn=2_500, comision_lado=0.0025 * 1.16,
    bt_liq_usd_min=1_000_000, bt_costo_rt=0.020, bt_muestra_control=150, bt_semilla=20261005,
    bt_anios=list(range(2015, 2026)),
)
ALERTAS_8K = {"1.03": "quiebra", "3.01": "aviso de deslistado", "4.01": "cambio de auditor",
              "4.02": "no confiar en estados", "2.04": "aceleracion de deuda", "2.06": "deterioro material",
              "3.02": "venta de acciones no registrada (dilucion)", "5.02": "salida de directivo"}
UA_Y = {"User-Agent": "Mozilla/5.0"}
UA_SEC = {"User-Agent": os.environ["SEC_USER_AGENT"], "Accept-Encoding": "identity"}

_lock_sec = threading.Lock()
_ultimo_sec = [0.0]


def get(url: str, headers: dict, cache_h: float | None = 20, sec: bool = False, binario=False):
    CACHE.mkdir(parents=True, exist_ok=True)
    ruta = CACHE / (hashlib.sha1(url.encode()).hexdigest() + ".gz")
    if cache_h and ruta.exists() and time.time() - ruta.stat().st_mtime < cache_h * 3600:
        return gzip.decompress(ruta.read_bytes()).decode("utf-8")
    ult = None
    for i in range(4):
        try:
            if sec:
                with _lock_sec:
                    dt = time.time() - _ultimo_sec[0]
                    if dt < 0.13:
                        time.sleep(0.13 - dt)
                    _ultimo_sec[0] = time.time()
            r = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(r, timeout=60) as resp:
                txt = resp.read().decode("utf-8")
            ruta.write_bytes(gzip.compress(txt.encode()))
            return txt
        except urllib.error.HTTPError as e:
            ult = e
            if e.code in (404, 400):
                break
            time.sleep(2 * (i + 1))
        except Exception as e:  # noqa: BLE001
            ult = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"{url}: {ult!r}")


def jget(url, headers, **kw):
    t = get(url, headers, **kw)
    i = t.find("({")
    if t.startswith("for(;;);") and i >= 0:
        return json.JSONDecoder().raw_decode(t[i + 1:])[0]
    return json.loads(t)


# ------------------------------------------------------------------ BMV
def listas_bmv() -> tuple[list[dict], list[dict]]:
    base = "https://www.bmv.com.mx/es/Grupo_BMV/BmvJsonGeneric?idSitioPagina="
    loc = jget(base + "4", UA_Y, cache_h=6)["response"]["resultado"]["A"]
    sic = jget(base + "6&mercado=CGEN_SCSOP&tipoValor=CGEN_CASEO", UA_Y, cache_h=6)["response"]["resultado"]
    sic = [x for x in sic if x.get("idTpvalor") == "1A"]
    return loc, sic


# ------------------------------------------------------------------ Yahoo
def chart(sym: str, rango="6mo", p1=None, p2=None, eventos=False):
    q = {"interval": "1d"}
    if p1:
        q.update(period1=p1, period2=p2)
    else:
        q["range"] = rango
    if eventos:
        q["events"] = "split"
    url = "https://query1.finance.yahoo.com/v8/finance/chart/" + urllib.parse.quote(sym, safe="") + "?" + urllib.parse.urlencode(q)
    try:
        d = json.loads(get(url, UA_Y, cache_h=20))["chart"]["result"][0]
    except Exception:  # noqa: BLE001
        return None
    q0 = d["indicators"]["quote"][0]
    adj = (d["indicators"].get("adjclose") or [{}])[0].get("adjclose")
    filas = []
    for i, t in enumerate(d.get("timestamp") or []):
        c = q0["close"][i] if i < len(q0["close"]) else None
        if c is None:
            continue
        filas.append(dict(f=datetime.fromtimestamp(t + int(d["meta"].get("gmtoffset", 0)), tz=timezone.utc).date(),
                          c=c, h=q0["high"][i], l=q0["low"][i], v=q0["volume"][i] or 0,
                          a=(adj[i] if adj and adj[i] is not None else c)))
    spl = [(datetime.fromtimestamp(int(k), tz=timezone.utc).date(), v["numerator"] / v["denominator"])
           for k, v in ((d.get("events") or {}).get("splits") or {}).items()]
    return dict(meta=d["meta"], filas=filas, splits=sorted(spl))


def corwin_schultz(filas: list[dict]) -> float | None:
    """Spread estimado de Corwin-Schultz (2012) con maximos y minimos diarios; mediana de pares, piso 0."""
    est = []
    for a, b in zip(filas, filas[1:]):
        if not (a["h"] and a["l"] and b["h"] and b["l"]) or a["l"] <= 0 or b["l"] <= 0:
            continue
        beta = math.log(a["h"] / a["l"]) ** 2 + math.log(b["h"] / b["l"]) ** 2
        gamma = math.log(max(a["h"], b["h"]) / min(a["l"], b["l"])) ** 2
        k = 3 - 2 * math.sqrt(2)
        alfa = (math.sqrt(2 * beta) - math.sqrt(beta)) / k - math.sqrt(gamma / k)
        est.append(max(0.0, 2 * (math.exp(alfa) - 1) / (1 + math.exp(alfa))))
    return st.median(est) if len(est) >= 20 else None


def liquidez(ch: dict | None) -> dict:
    if not ch or len(ch["filas"]) < 30:
        return dict(precio=None)
    f = [x for x in ch["filas"] if x["f"] >= HOY - timedelta(days=95)]
    ult60 = f[-60:]
    imp = [x["c"] * x["v"] for x in ult60]
    con_op = sum(1 for x in ult60 if x["v"] > 0)
    # dias habiles esperados en el rango de las ult60 filas (calendario Mon-Fri); Yahoo omite dias sin operacion
    d0, d1 = ult60[0]["f"], ult60[-1]["f"]
    esp = sum(1 for i in range((d1 - d0).days + 1) if (d0 + timedelta(days=i)).weekday() < 5) or 1
    return dict(precio=ult60[-1]["c"], fecha=str(d1), mediana_mxn=st.median(imp), dias_op=min(1.0, con_op / esp),
                spread_cs=corwin_schultz(ult60))


def ts(sym: str) -> dict:
    tipos = ("annualNetIncome,annualEBIT,annualEBITDA,annualFreeCashFlow,annualTotalDebt,annualCashAndCashEquivalents,"
             "annualStockholdersEquity,annualInvestedCapital,annualTotalRevenue,annualOrdinarySharesNumber,"
             "annualDilutedAverageShares,annualOperatingCashFlow,annualTaxRateForCalcs,trailingNetIncome,trailingEBIT,"
             "trailingEBITDA,trailingFreeCashFlow,trailingTotalRevenue,quarterlyOrdinarySharesNumber,quarterlyTotalDebt,"
             "quarterlyCashAndCashEquivalents")
    url = ("https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/"
           + urllib.parse.quote(sym, safe="") + "?type=" + tipos + "&period1=1400000000&period2=1800000000")
    try:
        d = json.loads(get(url, UA_Y, cache_h=20))["timeseries"]["result"]
    except Exception:  # noqa: BLE001
        return {}
    out = {}
    for r in d:
        for k, v in r.items():
            if k in ("meta", "timestamp"):
                continue
            out[k] = sorted((x["asOfDate"], x["reportedValue"]["raw"]) for x in v if x and x.get("reportedValue"))
    return out


def ult(serie, n=1):
    return [v for _, v in serie[-n:]] if serie else []


# ------------------------------------------------------------------ operabilidad
def simbolo_loc(x):
    s = x["cveSerie"].strip()
    return x["cveCorta"].strip().replace(" ", "") + ("" if s in ("*", "") else s.replace(" ", "")) + ".MX"


def paralelo(fn, items, n=6):
    with ThreadPoolExecutor(n) as ex:
        return list(ex.map(fn, items))


def fx_usdmxn() -> float:
    ch = chart("MXN=X", "5d")
    return ch["filas"][-1]["c"]


def operabilidad() -> list[dict]:
    loc, sic = listas_bmv()
    fx = fx_usdmxn()
    uni = [dict(origen="BMV", bmv=f"{x['cveCorta']} {x['cveSerie']}", sym=simbolo_loc(x)) for x in loc]
    uni += [dict(origen="SIC", bmv=x["cveCorta"], sym=x["cveCorta"].strip() + ".MX") for x in sic]
    # SIC: solo tickers con CIK (emisoras de EUA); el resto (ADR de otros paises, series 1/2) queda aparte
    tick = json.loads(get("https://www.sec.gov/files/company_tickers.json", UA_SEC, cache_h=72, sec=True))
    cik_de = {v["ticker"].upper().replace("-", ""): v["cik_str"] for v in tick.values()}
    for u in uni:
        base = u["sym"][:-3].upper().replace("-", "")
        u["cik"] = cik_de.get(base) if u["origen"] == "SIC" else None
    print(f"[operabilidad] BMV local {len(loc)} series | SIC acciones operadas {len(sic)} | FX {fx:.4f}", flush=True)
    chs = paralelo(lambda u: chart(u["sym"]), uni)
    for u, ch in zip(uni, chs):
        u.update(liquidez(ch))
        u["moneda"] = (ch or {}).get("meta", {}).get("currency")
    tss = paralelo(lambda u: ts(u["sym"]) if u.get("precio") else {}, uni)
    for u, t in zip(uni, tss):
        u["_ts"] = t
        acc = ult(t.get("quarterlyOrdinarySharesNumber")) or ult(t.get("annualOrdinarySharesNumber"))
        u["acciones"] = acc[0] if acc else None
        if u.get("precio") and u["acciones"]:
            u["mcap_usd"] = u["precio"] * u["acciones"] / fx
        else:
            u["mcap_usd"] = None
    return uni, fx


def costo_rt(monto, spread):
    com = 2 * monto * PARAMS["comision_lado"]
    return com + monto * (spread or 0.0), (com + monto * (spread or 0.0)) / monto


def escribe_operabilidad(uni, fx):
    P = PARAMS
    filas = []
    for u in uni:
        sp = u.get("spread_cs")
        c10 = costo_rt(P["pos_max_mxn"], sp)[1] if u.get("precio") else None
        filas.append(dict(origen=u["origen"], clave=u["bmv"], simbolo_yahoo=u["sym"], cik=u.get("cik") or "",
                          precio_mxn=round(u["precio"], 2) if u.get("precio") else "",
                          mediana_importe_mxn=round(u["mediana_mxn"]) if u.get("precio") else "",
                          dias_operados=round(u["dias_op"], 2) if u.get("precio") else "",
                          spread_cs=round(sp, 4) if sp is not None else "",
                          mcap_usd_m=round(u["mcap_usd"] / 1e6) if u.get("mcap_usd") else "",
                          costo_rt_pos2500=round(c10, 4) if c10 else ""))
    with open(SALIDA / "pantalla-chicas-2026-10-05-operabilidad.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    return filas


def en_banda(u):
    m = u.get("mcap_usd")
    return m is not None and PARAMS["mcap_min_usd"] <= m <= PARAMS["mcap_max_usd"]


def pasa_liq(u):
    P = PARAMS
    return (u.get("precio") and u["mediana_mxn"] >= P["liq_mediana_mxn_min"] and u["dias_op"] >= P["liq_dias_min"]
            and (u.get("spread_cs") is None or u["spread_cs"] <= P["spread_max"]))


def resumen_operabilidad(uni, fx) -> dict:
    P = PARAMS
    r = {}
    for org in ("BMV", "SIC"):
        g = [u for u in uni if u["origen"] == org and (org == "BMV" or u.get("cik"))]
        conp = [u for u in g if u.get("precio")]
        band = [u for u in conp if en_banda(u)]
        r[org] = dict(
            total=len([u for u in uni if u["origen"] == org]), con_cik=len(g) if org == "SIC" else None,
            con_precio=len(conp), en_banda=len(band),
            banda_liq=len([u for u in band if pasa_liq(u)]),
            banda_liq_titulo=len([u for u in band if pasa_liq(u) and u["precio"] <= P["titulo_max_mxn"]]),
            sin_dato_mcap=len([u for u in conp if u.get("mcap_usd") is None]),
            mediana_mcap_usd_m=round(st.median([u["mcap_usd"] for u in conp if u.get("mcap_usd")]) / 1e6) if any(u.get("mcap_usd") for u in conp) else None,
            menores_2b=len([u for u in conp if u.get("mcap_usd") and u["mcap_usd"] < 2e9]),
            menores_10b=len([u for u in conp if u.get("mcap_usd") and u["mcap_usd"] < 10e9]),
        )
    return r


# ------------------------------------------------------------------ pantalla
def evalua(u, fx) -> dict:
    """Aplica F2-F7 con fundamentales de Yahoo. Devuelve dict con metricas y lista de fallas."""
    P = PARAMS
    t = u["_ts"]
    fall, m = [], {}
    ni = ult(t.get("annualNetIncome"), 3)
    ebit_a = ult(t.get("annualEBIT"))
    if len(ni) < 3:
        return dict(m, fallas=["F2 sin 3 anios de NI"])
    m["ni0"], m["ni_2"] = ni[-1], ni[0]
    if not all(x > 0 for x in ni):
        fall.append("F2 NI no positiva 3 anios")
    elif ni[-1] < P["ni_crec_2a"] * ni[0]:
        fall.append("F2 NI(0) < 1.2 x NI(-2)")
    m["cagr_ni_2a"] = (ni[-1] / ni[0]) ** 0.5 - 1 if ni[0] > 0 and ni[-1] > 0 else None
    udm = ult(t.get("trailingNetIncome"))
    m["ni_udm"] = udm[0] if udm else None
    if not udm or udm[0] <= 0 or udm[0] < P["udm_vs_anual"] * ni[-1]:
        fall.append("F2 UDM")
    ebit = (ult(t.get("trailingEBIT")) or ebit_a or [None])[0]
    m["ebit"] = ebit
    tasa = (ult(t.get("annualTaxRateForCalcs")) or [0.21])[0]
    tasa = min(0.35, max(0.10, tasa))
    cap = (ult(t.get("annualInvestedCapital")) or [None])[0]
    m["roic"] = ebit * (1 - tasa) / cap if ebit and cap and cap > 0 else None
    if m["roic"] is None or m["roic"] < P["roic_min"]:
        fall.append("F3 ROIC")
    deuda = (ult(t.get("quarterlyTotalDebt")) or ult(t.get("annualTotalDebt")) or [None])[0]
    caja = (ult(t.get("quarterlyCashAndCashEquivalents")) or ult(t.get("annualCashAndCashEquivalents")) or [None])[0]
    ebitda = (ult(t.get("trailingEBITDA")) or ult(t.get("annualEBITDA")) or [None])[0]
    nd = (deuda - caja) if deuda is not None and caja is not None else None
    m["nd"], m["ebitda"] = nd, ebitda
    m["nd_ebitda"] = nd / ebitda if nd is not None and ebitda and ebitda > 0 else None
    if m["nd_ebitda"] is None or m["nd_ebitda"] > P["nd_ebitda_max"]:
        fall.append("F4 ND/EBITDA")
    fcf = (ult(t.get("annualFreeCashFlow")) or [None])[0]
    fcf_u = (ult(t.get("trailingFreeCashFlow")) or [None])[0]
    m["fcf0"], m["fcf_udm"] = fcf, fcf_u
    if fcf is None or fcf_u is None or fcf <= 0 or fcf_u <= 0 or fcf / ni[-1] < P["fcf_ni_min"]:
        fall.append("F5 FCF")
    mcap_loc = u["precio"] * u["acciones"]
    ev = mcap_loc + (nd or 0)
    m["ev_ebit"] = ev / ebit if ebit and ebit > 0 else None
    m["pu"] = mcap_loc / udm[0] if udm and udm[0] > 0 else None
    if m["ev_ebit"] is None or m["ev_ebit"] > P["ev_ebit_max"]:
        fall.append("F6 EV/EBIT")
    sh = ult(t.get("annualOrdinarySharesNumber"), 3) or ult(t.get("annualDilutedAverageShares"), 3)
    m["dilucion_2a"] = sh[-1] / sh[0] if len(sh) == 3 and sh[0] else None
    if m["dilucion_2a"] is None or m["dilucion_2a"] > P["dilucion_max"]:
        fall.append("F7 dilucion")
    m["fallas"] = fall
    return m


def verifica_edgar(sym_us: str, t: dict) -> dict:
    """2a fuente: companyfacts XBRL (herramientas/edgar.py). Compara NI, flujo operativo y utilidad operativa del ultimo FY."""
    try:
        e = edgar.estados_financieros(sym_us, "anual")
    except Exception as ex:  # noqa: BLE001
        return dict(edgar="error: " + str(ex)[:60])
    filas = e["filas"]
    if not filas:
        return dict(edgar="sin filas")
    f = filas[-1]
    ni_y = ult(t.get("annualNetIncome"))[0]
    ocf_y = ult(t.get("annualOperatingCashFlow"))
    fin_y = t["annualNetIncome"][-1][0]
    ok_fecha = abs((f["fin"] - date.fromisoformat(fin_y)).days) <= 10
    dif = lambda a, b: (abs(a - b) / abs(b)) if a is not None and b else None  # noqa: E731
    d_ni, d_ocf = dif(f["utilidad_neta"], ni_y), dif(f["flujo_operativo"], ocf_y[0] if ocf_y else None)
    ok = ok_fecha and d_ni is not None and d_ni <= 0.03 and (d_ocf is None or d_ocf <= 0.03)
    return dict(edgar="OK" if ok else "DIFIERE", edgar_fy=f["etiqueta"], edgar_ni=f["utilidad_neta"],
                edgar_ocf=f["flujo_operativo"], edgar_ingresos=f["ingresos"], edgar_op=f["utilidad_operativa"],
                dif_ni=None if d_ni is None else round(d_ni, 4), dif_ocf=None if d_ocf is None else round(d_ocf, 4),
                forma="10-K")


def alertas_8k(sym_us: str) -> str:
    try:
        pres = edgar.presentaciones_recientes(sym_us, tipos=("8-K",), n=60)
    except Exception as ex:  # noqa: BLE001
        return "error " + str(ex)[:40]
    lim = (HOY - timedelta(days=180)).isoformat()
    out = []
    for p in pres:
        if p["fecha"] < lim:
            continue
        for it in p["items"]:
            if it in ALERTAS_8K:
                out.append(f"{p['fecha']} {it} {ALERTAS_8K[it]}")
    return "; ".join(out) or "sin alertas 180d"


def tiene_10k(sym_us):
    try:
        pres = edgar.presentaciones_recientes(sym_us, tipos=("10-K", "20-F", "40-F"), n=3)
        return bool(pres) and pres[0]["forma"].startswith("10-K")
    except Exception:  # noqa: BLE001
        return False


def pantalla(uni, fx) -> tuple[list[dict], dict]:
    P = PARAMS
    emb = {"universo_total": len(uni)}
    cand = [u for u in uni if u.get("precio") and (u["origen"] == "BMV" or u.get("cik"))]
    emb["con_precio_y_cik_o_bmv"] = len(cand)
    c1 = [u for u in cand if en_banda(u)]
    emb["F1_tamano"] = len(c1)
    c2 = [u for u in c1 if pasa_liq(u)]
    emb["F8_liquidez"] = len(c2)
    c3 = [u for u in c2 if u["precio"] <= P["titulo_max_mxn"]]
    emb["F9_titulo"] = len(c3)
    # F2-F7 se evaluan sobre las que pasan F1; las que fallan F8/F9 se anotan igual para saber cuantas
    # buenas empresas se pierden por no ser operables.
    evals = []
    for u in c1:
        m = evalua(u, fx)
        liq_ok = bool(pasa_liq(u))
        tit_ok = u["precio"] <= P["titulo_max_mxn"]
        fund_ok = not m["fallas"]
        evals.append((u, m, fund_ok, liq_ok, tit_ok))
    emb["fundamentales_F2_a_F7"] = len([e for e in evals if e[2]])
    emb["fundamentales_y_liquidez"] = len([e for e in evals if e[2] and e[3]])
    emb["TODOS_los_filtros"] = len([e for e in evals if e[2] and e[3] and e[4]])
    # conteo por filtro que mas elimina
    from collections import Counter
    cnt = Counter()
    for _, m, *_r in evals:
        for f in m["fallas"]:
            cnt[f.split(" ")[0] + " " + f.split(" ")[1] if " " in f else f] += 1
    emb["fallas_por_filtro_en_banda"] = dict(cnt)
    # ranking de los que pasan fundamentales (aunque no sean operables) para mostrar el costo de la operabilidad
    def rangos(lista, clave, desc):
        orden = sorted(lista, key=lambda e: e[1][clave] if e[1][clave] is not None else -1e18, reverse=desc)
        return {id(e[0]): i + 1 for i, e in enumerate(orden)}
    buenos = [e for e in evals if e[2]]
    if buenos:
        r1, r2 = rangos(buenos, "roic", True), rangos(buenos, "cagr_ni_2a", True)
        r3 = rangos(buenos, "ev_ebit", False)
        for e in buenos:
            e[1]["score_rango"] = (r1[id(e[0])] + r2[id(e[0])] + r3[id(e[0])]) / 3
    salida = []
    for u, m, fund_ok, liq_ok, tit_ok in sorted(evals, key=lambda e: (not e[2], e[1].get("score_rango", 1e9))):
        if not fund_ok and len(salida) >= 40:
            continue
        if not fund_ok:
            continue
        sym_us = u["sym"][:-3] if u["origen"] == "SIC" else None
        fila = dict(origen=u["origen"], clave=u["bmv"], simbolo=u["sym"], operable=("SI" if liq_ok and tit_ok else "NO"),
                    motivo_no=("" if liq_ok and tit_ok else ("liquidez/spread " if not liq_ok else "") + ("titulo>2500 MXN" if not tit_ok else "")),
                    precio_mxn=round(u["precio"], 2), mcap_usd_m=round(u["mcap_usd"] / 1e6),
                    mediana_importe_mxn=round(u["mediana_mxn"]), dias_operados=round(u["dias_op"], 2),
                    spread_cs=round(u["spread_cs"], 4) if u.get("spread_cs") is not None else "",
                    costo_rt_pos2000=round(costo_rt(2000, u.get("spread_cs"))[1], 4),
                    ni0_m=round(m["ni0"] / 1e6, 1), ni_2_m=round(m["ni_2"] / 1e6, 1), cagr_ni_2a=round(m["cagr_ni_2a"], 3),
                    roic=round(m["roic"], 3), nd_ebitda=round(m["nd_ebitda"], 2), fcf0_m=round(m["fcf0"] / 1e6, 1),
                    fcf_udm_m=round(m["fcf_udm"] / 1e6, 1), ev_ebit=round(m["ev_ebit"], 1),
                    pu=round(m["pu"], 1) if m["pu"] else "", dilucion_2a=round(m["dilucion_2a"], 3),
                    score_rango=round(m["score_rango"], 1))
        if sym_us:
            if not tiene_10k(sym_us):
                fila["edgar"] = "no es 10-K (ADR/20-F): fundamentales de Yahoo pueden estar en otra moneda"
            else:
                fila.update(verifica_edgar(sym_us, u["_ts"]))
                fila["alertas_8k"] = alertas_8k(sym_us)
        else:
            fila["edgar"] = "BMV: segunda fuente no disponible gratis (XBRL BMV no automatizado); verificar a mano"
        salida.append(fila)
    return salida, emb


# ------------------------------------------------------------------ backtest
def frame(tag, unidad, per):
    url = f"https://data.sec.gov/api/xbrl/frames/us-gaap/{tag}/{unidad}/{per}.json"
    try:
        d = json.loads(get(url, UA_SEC, cache_h=24 * 30, sec=True))
    except Exception:  # noqa: BLE001
        return {}
    return {x["cik"]: (x["val"], x["accn"], x["end"]) for x in d["data"]}


def bt_fundamentales(t_anio: int) -> dict[int, dict]:
    """PIT: ejercicio t-1 (y t-2, t-3) con accesion de a lo sumo el anio t."""
    y = t_anio - 1
    ann = {}
    for tag in ("NetIncomeLoss",):
        for k in (y, y - 1, y - 2):
            ann[(tag, k)] = frame(tag, "USD", f"CY{k}")
    flu = {tag: frame(tag, "USD", f"CY{y}") for tag in (
        "OperatingIncomeLoss", "NetCashProvidedByUsedInOperatingActivities", "PaymentsToAcquirePropertyPlantAndEquipment",
        "DepreciationDepletionAndAmortization")}
    ins = {tag: frame(tag, "USD", f"CY{y}Q4I") for tag in (
        "CashAndCashEquivalentsAtCarryingValue", "StockholdersEquity", "LongTermDebt", "LongTermDebtNoncurrent",
        "LongTermDebtCurrent", "DebtCurrent")}
    shs = {k: frame("WeightedAverageNumberOfDilutedSharesOutstanding", "shares", f"CY{k}") for k in (y, y - 2)}
    out = {}
    for cik, (ni0, accn, end) in ann[("NetIncomeLoss", y)].items():
        if int(accn.split("-")[1]) > t_anio % 100 and t_anio < 2100:  # presentada despues de la formacion
            continue
        if date.fromisoformat(end) > date(t_anio, 6, 30) - timedelta(days=90):
            continue
        ni1 = ann[("NetIncomeLoss", y - 1)].get(cik)
        ni2 = ann[("NetIncomeLoss", y - 2)].get(cik)
        if not ni1 or not ni2:
            continue
        g = lambda dct, tag: (dct[tag].get(cik) or (None,))[0]  # noqa: E731
        op, ocf, capex = g(flu, "OperatingIncomeLoss"), g(flu, "NetCashProvidedByUsedInOperatingActivities"), g(flu, "PaymentsToAcquirePropertyPlantAndEquipment")
        da = g(flu, "DepreciationDepletionAndAmortization") or 0
        cash, eq = g(ins, "CashAndCashEquivalentsAtCarryingValue"), g(ins, "StockholdersEquity")
        debt = g(ins, "LongTermDebt")
        if debt is None:
            parts = [g(ins, "LongTermDebtNoncurrent"), g(ins, "LongTermDebtCurrent"), g(ins, "DebtCurrent")]
            debt = sum(p for p in parts if p) if any(parts) else 0.0  # sin deuda reportada: se asume 0 (declarado)
        sh0, sh2 = (shs[y].get(cik) or (None,))[0], (shs[y - 2].get(cik) or (None,))[0]
        out[cik] = dict(ni=[ni2[0], ni1[0], ni0], op=op, ocf=ocf, capex=capex, da=da, cash=cash, eq=eq, debt=debt, sh0=sh0, sh2=sh2)
    return out


def bt_prefiltro(f) -> bool:
    P = PARAMS
    if None in (f["op"], f["ocf"], f["cash"], f["eq"], f["sh0"], f["sh2"]) or f["op"] <= 0:
        return False
    ni = f["ni"]
    if not all(x > 0 for x in ni) or ni[2] < P["ni_crec_2a"] * ni[0]:
        return False
    cap = f["eq"] + f["debt"] - f["cash"]
    if cap <= 0 or f["op"] * 0.79 / cap < P["roic_min"]:
        return False
    ebitda = f["op"] + f["da"]
    if (f["debt"] - f["cash"]) / ebitda > P["nd_ebitda_max"]:
        return False
    fcf = f["ocf"] - abs(f["capex"] or 0)
    if fcf <= 0 or fcf / ni[2] < P["fcf_ni_min"]:
        return False
    return f["sh0"] / f["sh2"] <= P["dilucion_max"]


def hist(sym):
    ch = chart(sym, p1=int(datetime(2014, 1, 1).timestamp()), p2=int(datetime(2026, 10, 5).timestamp()), eventos=True)
    return ch


def px_en(ch, d: date):
    """(cierre sin ajustar por splits posteriores, cierre ajustado, indice) en o antes de d."""
    fs = ch["filas"]
    lo, hi = 0, len(fs) - 1
    if not fs or fs[0]["f"] > d:
        return None
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if fs[mid]["f"] <= d:
            lo = mid
        else:
            hi = mid - 1
    f = fs[lo]
    fac = 1.0
    for sd, r in ch["splits"]:
        if sd > d:
            fac *= r
    return f["c"] * fac, f["a"], lo


def backtest():
    P = PARAMS
    tick = json.loads(get("https://www.sec.gov/files/company_tickers.json", UA_SEC, cache_h=72, sec=True))
    tk = {}
    for v in tick.values():
        tk.setdefault(v["cik_str"], v["ticker"])
    res, detalle, superv = [], [], []
    for ta in P["bt_anios"]:
        print(f"[backtest] formacion 30-jun-{ta}", flush=True)
        fu = bt_fundamentales(ta)
        # supervivencia: que parte de los emisores con NI>0 en el ejercicio de formacion tiene ticker vigente
        con_ni = [c for c, f in fu.items() if f["ni"][2] > 0]
        superv.append(dict(anio=ta, emisores_NI_pos=len(con_ni), con_ticker_vigente=len([c for c in con_ni if c in tk])))
        pasan = [c for c, f in fu.items() if c in tk and bt_prefiltro(f)]
        rnd = random.Random(P["bt_semilla"] + ta)
        pos = sorted(c for c in con_ni if c in tk)
        ctrl = rnd.sample(pos, min(P["bt_muestra_control"], len(pos)))
        todos = sorted(set(pasan) | set(ctrl))
        chs = dict(zip(todos, paralelo(lambda c: hist(tk[c]), todos, n=8)))
        t0, t1 = date(ta, 6, 30), date(ta + 1, 6, 30)
        for c in todos:
            ch = chs[c]
            f = fu[c]
            fila = dict(anio=ta, cik=c, ticker=tk[c], en_pantalla=int(c in pasan), en_control=int(c in ctrl))
            if not ch or len(ch["filas"]) < 100:
                fila.update(estado="sin_precios_yahoo")
                detalle.append(fila)
                continue
            p0 = px_en(ch, t0)
            p1 = px_en(ch, t1)
            if not p0 or (ch["filas"][p0[2]]["f"] < t0 - timedelta(days=10)):
                fila.update(estado="sin_precio_en_t")
                detalle.append(fila)
                continue
            mcap = p0[0] * f["sh0"]
            ult60 = ch["filas"][max(0, p0[2] - 59):p0[2] + 1]
            adv = st.median([x["c"] * x["v"] for x in ult60]) if ult60 else 0
            ebit = f["op"]
            ev = mcap + f["debt"] - f["cash"]
            fila.update(mcap_m=round(mcap / 1e6), adv_usd=round(adv), ev_ebit=round(ev / ebit, 1) if ebit and ebit > 0 else "")
            # fin de ventana
            if not p1 or ch["filas"][p1[2]]["f"] < t1 - timedelta(days=15):
                fila.update(estado="sin_datos_al_final(deslistada?)", ret="")
            else:
                fila.update(estado="ok", ret=round(p1[1] / p0[1] - 1, 4))
            fila["banda"] = int(P["mcap_min_usd"] <= mcap <= P["mcap_max_usd"])
            fila["liq_ok"] = int(adv >= P["bt_liq_usd_min"])
            fila["valor_ok"] = int(bool(ebit and ebit > 0 and ev / ebit <= P["ev_ebit_max"]))
            detalle.append(fila)
    # agregacion
    iwm = hist("IWM")
    por_anio = []
    for ta in P["bt_anios"]:
        d = [x for x in detalle if x["anio"] == ta]
        S = [x for x in d if x["en_pantalla"] and x.get("banda") and x.get("liq_ok") and x.get("valor_ok")]
        C = [x for x in d if x["en_control"] and x.get("banda") and x.get("liq_ok")]
        Sr = [x["ret"] for x in S if x.get("estado") == "ok"]
        Cr = [x["ret"] for x in C if x.get("estado") == "ok"]
        Sm = len([x for x in S if x.get("estado") != "ok"])
        Cm = len([x for x in C if x.get("estado") != "ok"])
        i0, i1 = px_en(iwm, date(ta, 6, 30)), px_en(iwm, date(ta + 1, 6, 30))
        iw = i1[1] / i0[1] - 1 if i0 and i1 else None
        por_anio.append(dict(anio=ta, n_S=len(Sr), faltan_S=Sm, n_C=len(Cr), faltan_C=Cm,
                             ret_S=st.mean(Sr) if Sr else None, ret_S_med=st.median(Sr) if Sr else None,
                             ret_C=st.mean(Cr) if Cr else None, iwm=iw))
    return por_anio, detalle, superv


def bootstrap_ic(xs, n=20000, seed=7):
    rnd = random.Random(seed)
    ms = sorted(st.mean(rnd.choices(xs, k=len(xs))) for _ in range(n))
    return ms[int(0.10 * n)], ms[int(0.90 * n)]


def resumen_bt(por_anio, detalle):
    P = PARAMS
    v = [a for a in por_anio if a["n_S"] and a["n_C"]]
    exc_bruto = [a["ret_S"] - a["ret_C"] for a in v]
    exc_neto = [a["ret_S"] - P["bt_costo_rt"] - a["ret_C"] for a in v]  # el control tambien paga costo si se compra; se resta solo al S (conservador)
    exc_iwm = [a["ret_S"] - P["bt_costo_rt"] - a["iwm"] for a in v if a["iwm"] is not None]
    r = dict(n_anios=len(v), exceso_bruto_medio=st.mean(exc_bruto), exceso_neto_medio=st.mean(exc_neto),
             aciertos=sum(1 for e in exc_bruto if e > 0), aciertos_neto=sum(1 for e in exc_neto if e > 0),
             sd_exceso=st.stdev(exc_bruto) if len(exc_bruto) > 1 else None,
             ic80_neto=bootstrap_ic(exc_neto) if len(exc_neto) > 2 else None,
             exceso_neto_vs_iwm=st.mean(exc_iwm) if exc_iwm else None,
             ret_S_medio=st.mean([a["ret_S"] for a in v]), ret_C_medio=st.mean([a["ret_C"] for a in v]),
             iwm_medio=st.mean([a["iwm"] for a in v if a["iwm"] is not None]))
    if r["sd_exceso"]:
        se = r["sd_exceso"] / math.sqrt(len(exc_bruto))
        r["error_est"] = se
        r["efecto_min_detectable_80pot"] = 2.8 * se
    # sensibilidad a supervivencia: los que faltan al final se suponen con rendimiento X
    sens = {}
    for X in (0.0, -0.5, -1.0):
        exc = []
        for a in v:
            nS, mS = a["n_S"], a["faltan_S"]
            nC, mC = a["n_C"], a["faltan_C"]
            S = (a["ret_S"] * nS + X * mS) / (nS + mS)
            C = (a["ret_C"] * nC + X * mC) / (nC + mC)
            exc.append(S - P["bt_costo_rt"] - C)
        sens[X] = st.mean(exc)
    r["sens_faltantes"] = sens
    return r


# ------------------------------------------------------------------ main
def fmt_pct(x):
    return "n/d" if x is None else f"{x * 100:+.1f}%"


def main(arg: str):
    SALIDA.mkdir(parents=True, exist_ok=True)
    out_md = []
    uni = fx = None
    if arg in ("operabilidad", "pantalla", "todo"):
        uni, fx = operabilidad()
        filas = escribe_operabilidad(uni, fx)
        ro = resumen_operabilidad(uni, fx)
        print(json.dumps(ro, indent=1, ensure_ascii=False))
        out_md.append("## Operabilidad (BMV y SIC, datos al %s)\n\n```json\n%s\n```\n" % (HOY, json.dumps(ro, indent=1, ensure_ascii=False)))
    if arg in ("pantalla", "todo"):
        sal, emb = pantalla(uni, fx)
        print(json.dumps(emb, indent=1, ensure_ascii=False))
        if sal:
            cols = []
            for r in sal:
                for k in r:
                    if k not in cols:
                        cols.append(k)
            with open(SALIDA / "pantalla-chicas-2026-10-05.csv", "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=cols)
                w.writeheader()
                w.writerows(sal)
        else:
            (SALIDA / "pantalla-chicas-2026-10-05.csv").write_text("sin candidatos\n")
        out_md.append("## Embudo\n\n```json\n%s\n```\n" % json.dumps(emb, indent=1, ensure_ascii=False))
        out_md.append("## Candidatos (fundamentales OK; columna operable)\n\n| " + " | ".join(["origen", "simbolo", "operable", "mcap USD M", "NI0 M", "CAGR NI", "ROIC", "ND/EBITDA", "EV/EBIT", "costo RT 2k", "edgar"]) + " |\n|" + "---|" * 11 + "\n"
                      + "\n".join("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (r["origen"], r["simbolo"], r["operable"], r["mcap_usd_m"], r["ni0_m"], r["cagr_ni_2a"], r["roic"], r["nd_ebitda"], r["ev_ebit"], r["costo_rt_pos2000"], r.get("edgar", "")[:30]) for r in sal) + "\n")
    if arg in ("backtest", "todo"):
        por_anio, detalle, superv = backtest()
        cols = []
        for r in detalle:
            for k in r:
                if k not in cols:
                    cols.append(k)
        with open(SALIDA / "pantalla-chicas-2026-10-05-backtest.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(detalle)
        rb = resumen_bt(por_anio, detalle)
        print(json.dumps(rb, indent=1, default=str))
        for a in por_anio:
            print(a)
        print(superv)
        out_md.append("## Backtest\n\n```json\n%s\n```\n\n%s\n\nSupervivencia:\n%s\n" % (json.dumps(rb, indent=1, default=str), "\n".join(str(a) for a in por_anio), "\n".join(str(s) for s in superv)))
    (SALIDA / "pantalla-chicas-2026-10-05.md").write_text("# Pantalla de empresas chicas, 2026-10-05 (salida automatica del script)\n\n" + "\n".join(out_md))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "todo")
