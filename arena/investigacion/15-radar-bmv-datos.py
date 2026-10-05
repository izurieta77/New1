"""Datos de mercado del radar BMV (15-radar-bmv-2026-10-05.md). Solo biblioteca estandar.

Uso:
    python3 arena/investigacion/15-radar-bmv-datos.py --salida arena/investigacion/15-radar-bmv-2026-10-05-datos.csv
    python3 arena/investigacion/15-radar-bmv-datos.py --salida out.csv --cache-horas 0   # fuerza descarga

Fuente: Yahoo Finance chart v8 (via herramientas/datos.py, sin ajuste: cierre crudo para niveles de
alerta; los dividendos no entran en la SMA200 ni en los retornos). Universo: las emisoras .MX de
empresas/universo.csv, mas NAFTRAC y FIBRAs. Metricas por ticker:
  * precio, fecha, SMA200 (promedio de los ultimos 200 cierres), distancia a SMA200.
  * max/min de 252 sesiones (cierre), retornos 1m/3m/6m/12m por calendario.
  * vol60: desviacion estandar de 60 rendimientos log * sqrt(252).
  * liq30_mxn_mm: mediana de cierre*volumen de las ultimas 30 sesiones (millones de MXN); dias_op = sesiones con volumen > 0.
  * spread_cs_pct: estimador de Corwin-Schultz (2012) con maximos y minimos de 20 sesiones.
    ES UNA ESTIMACION, no un spread cotizado (Yahoo chart no trae bid/ask); piso en 0.
  * rho60_spy_mxn / rho60_naftrac: correlacion de 60 rendimientos diarios con SPY convertido a MXN
    (proxy de la cartera SPYM/QQQM/UPRO) y con NAFTRAC. El desfase horario del FX sesga rho hacia abajo.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import statistics
import sys
import time
import urllib.parse
from datetime import date, datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from herramientas.datos import UA_NAVEGADOR, URL_YAHOO, descargar, valor_en_o_antes  # noqa: E402

_spec = importlib.util.spec_from_file_location("pantalla", RAIZ / "arena/investigacion/pantalla.py")
pantalla = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pantalla)

EXTRA = ["NAFTRAC.MX", "FUNO11.MX", "DANHOS13.MX", "FIBRAMQ12.MX", "TERRA13.MX",
         "FIBRAPL14.MX", "FMTY14.MX", "FSHOP13.MX"]


def universo_mx() -> list[str]:
    with open(RAIZ / "empresas/universo.csv", encoding="utf-8") as f:
        return [r["ticker"] for r in csv.DictReader(f) if r["mercado"] == "MX"]


def barras(ticker: str, cache_horas):
    url = (URL_YAHOO + urllib.parse.quote(ticker, safe="") + "?"
           + urllib.parse.urlencode({"range": "2y", "interval": "1d", "events": "div"}))
    j = json.loads(descargar(url, UA_NAVEGADOR, cache_horas=cache_horas))["chart"]["result"][0]
    meta = j["meta"]
    ts = j.get("timestamp") or []
    q = j["indicators"]["quote"][0]
    off = int(meta.get("gmtoffset", 0))
    out = []
    for i, t in enumerate(ts):
        c, h, l, v = (q[k][i] if i < len(q[k]) else None for k in ("close", "high", "low", "volume"))
        if c is None or h is None or l is None:
            continue
        d = datetime.fromtimestamp(t + off, tz=timezone.utc).date()
        if out and out[-1][0] == d:
            out.pop()
        out.append((d, float(c), float(h), float(l), float(v or 0)))
    divs = []
    for _, dv in ((j.get("events") or {}).get("dividends") or {}).items():
        divs.append((datetime.fromtimestamp(dv["date"], tz=timezone.utc).date(), dv["amount"]))
    return meta, out, sorted(divs)


def corwin_schultz(b, n=20):
    s = []
    seg = b[-(n + 1):]
    k = 3 - 2 * math.sqrt(2)
    for i in range(1, len(seg)):
        h1, l1, h2, l2 = seg[i - 1][2], seg[i - 1][3], seg[i][2], seg[i][3]
        if min(h1, l1, h2, l2) <= 0:
            continue
        beta = math.log(h1 / l1) ** 2 + math.log(h2 / l2) ** 2
        gamma = math.log(max(h1, h2) / min(l1, l2)) ** 2
        alpha = (math.sqrt(2 * beta) - math.sqrt(beta)) / k - math.sqrt(gamma / k)
        s.append(2 * (math.exp(alpha) - 1) / (1 + math.exp(alpha)))
    return max(0.0, statistics.mean(s)) if s else None


def rend(serie_pc):
    return {serie_pc[i][0]: math.log(serie_pc[i][1] / serie_pc[i - 1][1]) for i in range(1, len(serie_pc))}


def corr(a: dict, b: dict, n=60):
    ks = sorted(set(a) & set(b))[-n:]
    if len(ks) < 40:
        return None
    x = [a[k] for k in ks]
    y = [b[k] for k in ks]
    mx, my = statistics.mean(x), statistics.mean(y)
    sx = math.sqrt(sum((i - mx) ** 2 for i in x))
    sy = math.sqrt(sum((i - my) ** 2 for i in y))
    return sum((i - mx) * (j - my) for i, j in zip(x, y)) / (sx * sy) if sx and sy else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True)
    ap.add_argument("--cache-horas", type=float, default=None)
    a = ap.parse_args()
    ch = a.cache_horas
    fx = pantalla.fx_cierre_eua(ch)
    spy = pantalla.a_mxn([(d, c) for d, c, *_ in barras("SPY", ch)[1]], fx)
    r_spy = rend(spy)
    _, nb, _ = barras("NAFTRAC.MX", ch)
    r_naf = rend([(d, c) for d, c, *_ in nb])
    filas = []
    for t in universo_mx() + EXTRA:
        time.sleep(0.7)
        try:
            meta, b, divs = barras(t, ch)
        except Exception as e:  # noqa: BLE001
            filas.append({"ticker": t, "estado": f"error: {e}"})
            continue
        if len(b) < 210:
            filas.append({"ticker": t, "estado": f"pocos datos ({len(b)})"})
            continue
        cierres = [x[1] for x in b]
        p = cierres[-1]
        f = b[-1][0]
        sma200 = statistics.mean(cierres[-200:])
        w = b[-252:]
        logs = [math.log(cierres[i] / cierres[i - 1]) for i in range(len(cierres) - 60, len(cierres))]
        ret = {}
        for k, n in (("1m", 1), ("3m", 3), ("6m", 6), ("12m", 12)):
            r = pantalla.retorno([(d, c) for d, c, *_ in b], f, pantalla.meses_atras(f, n))
            ret[k] = r
        v30 = [x[1] * x[4] for x in b[-30:]]
        div12 = sum(m for d, m in divs if d > pantalla.meses_atras(f, 12))
        filas.append({
            "ticker": t, "estado": "ok", "fecha": f.isoformat(), "precio": round(p, 4),
            "sma200": round(sma200, 4), "dist_sma200": round(p / sma200 - 1, 4),
            "max_252": round(max(x[1] for x in w), 4), "min_252": round(min(x[1] for x in w), 4),
            "dist_max": round(p / max(x[1] for x in w) - 1, 4),
            "ret_1m": ret["1m"], "ret_3m": ret["3m"], "ret_6m": ret["6m"], "ret_12m": ret["12m"],
            "vol60": round(statistics.stdev(logs) * math.sqrt(252), 4),
            "liq30_mxn_mm": round(statistics.median(v30) / 1e6, 2),
            "dias_op_30": sum(1 for x in b[-30:] if x[4] > 0),
            "spread_cs_pct": round(100 * (corwin_schultz(b) or 0), 3),
            "rho60_spy_mxn": None if (r := corr(rend([(d, c) for d, c, *_ in b]), r_spy)) is None else round(r, 3),
            "rho60_naftrac": None if (r := corr(rend([(d, c) for d, c, *_ in b]), r_naf)) is None else round(r, 3),
            "div12m_ps": round(div12, 4), "rend_div12m": round(div12 / p, 4) if div12 else 0.0,
            "moneda": meta.get("currency"), "nombre": meta.get("longName") or meta.get("shortName"),
        })
    campos = ["ticker", "estado", "fecha", "precio", "sma200", "dist_sma200", "max_252", "min_252",
              "dist_max", "ret_1m", "ret_3m", "ret_6m", "ret_12m", "vol60", "liq30_mxn_mm",
              "dias_op_30", "spread_cs_pct", "rho60_spy_mxn", "rho60_naftrac", "div12m_ps",
              "rend_div12m", "moneda", "nombre"]
    with open(a.salida, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        for r in filas:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
    ult = valor_en_o_antes(fx, date.today())
    print(f"{len(filas)} filas -> {a.salida}; FX ultimo cierre EUA {ult}; generado {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
