"""Radar EUA 2026-10-05: metricas verificables + tasas base de las plantillas de nivel (solo biblioteca estandar).

Uso:
    python3 arena/investigacion/radar_eua.py --salida arena/investigacion/radar-eua-2026-10-05-metricas.csv [--corte 2026-10-05]

Que calcula (todo con Yahoo chart v8 via herramientas/datos.py; nada posterior al corte):
  * precio, retornos 1/3/6m, vol 60d, distancia a SMA200, drawdown 1a, distancia al maximo 52s;
  * liquidez: volumen en dolares medio de 63 sesiones; sesiones con volumen en 22 de <TICKER>.MX (proxy SIC);
  * precio del titulo en MXN (precio * USDMXN al cierre de EUA) y cabida en el tope por posicion;
  * correlacion a 60 dias en MXN con la cartera actual (SPYM 40.2 / QQQM 27.4 / UPRO 26.8 %);
  * TASA BASE de las tres plantillas del dueño (adenda del 13-radar): ventanas moviles diarias de 10 anios
    (o lo que haya) del propio candidato y de su GRUPO (todas las series del grupo juntas). Cada ventana se
    resuelve como la regla real: sale en el primer cierre >= +objetivo, o <= -stop, o al plazo.
        Diamante: +40% en 63 sesiones (3m), stop -20%   (2:1)
        Platino : +50% en 105 sesiones (5m), stop -25%  (2:1)
        Oro     : +25% en 147 sesiones (7m), stop -12.5% (2:1)
    Para apalancados se agrega la variante con filtro (subyacente > SMA200 x 1.03 y VIX < 25 al entrar; sale
    si el subyacente cierra < SMA200 x 0.97 o VIX >= 25).
Sesgos conocidos: las series son de los emisores que HOY existen y son grandes (sesgo de supervivencia, sube
las tasas base); los retornos son en USD (sin FX); las ventanas se traslapan (n efectivo ~ n/plazo).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
for p in (RAIZ, Path(__file__).resolve().parent):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from herramientas.datos import UA_NAVEGADOR, URL_YAHOO, ErrorDatos, descargar, valor_en_o_antes  # noqa: E402
import pantalla  # noqa: E402

COMISION_RT = 0.0058      # 0.25% + IVA por lado (REGLAS-MOTOR §4)
FX_RT = 0.0030            # SUPUESTO: costo cambiario implicito del SIC ida y vuelta (no publicado, no verificado)
SPREAD_LIQ = 0.0010       # supuesto 01-gbm: 0.10% liquidos / 0.30% medio / 0.60% bajo
SPREAD_MED = 0.0030
CAP_ACCION_REAL = 0.30 * 10000.0     # accion_individual_max arena 0.30 x 10,000 MXN (cuenta real)
CAP_ACCION_PAPEL = 0.30 * 20486.35   # cuenta de papel (equity 2026-10-05)
CAP_APALANCADO_REAL = 0.50 * 10000.0
PLANTILLAS = {
    "Diamante": dict(T=0.40, S=0.20, H=63),
    "Platino": dict(T=0.50, S=0.25, H=105),
    "Oro": dict(T=0.25, S=0.125, H=147),
}
CARTERA = {"SPYM": 0.402, "QQQM": 0.274, "UPRO": 0.268}
SUBY = {"UPRO": "^GSPC", "SPXL": "^GSPC", "TQQQ": "^NDX", "TECL": "XLK", "SOXL": "SOXX"}

GRUPOS = {
    "semis": ["NVDA", "AMD", "MU", "AVGO", "INTC", "LRCX", "AMAT", "TXN", "SNDK", "TSM", "ASML", "SMH", "SOXX"],
    "software_ciber": ["MSFT", "ORCL", "PLTR", "PANW", "CRWD"],
    "hardware_redes": ["AAPL", "CSCO", "DELL", "ANET"],
    "internet_megacap": ["GOOGL", "META", "AMZN", "NFLX", "TSLA", "UBER"],
    "financieras": ["JPM", "BAC", "MS", "GS", "WFC", "V", "MA", "BRK-B", "XLF"],
    "salud": ["LLY", "JNJ", "ABBV", "MRK", "UNH", "TMO", "XLV"],
    "energia": ["XOM", "CVX", "XLE"],
    "industrial_defensa": ["CAT", "GE", "GEV", "RTX", "SPCX", "XLI"],
    "consumo": ["WMT", "COST", "KO", "PG", "PM", "HD", "XLP"],
    "indices": ["SPYM", "QQQM", "SPY", "QQQ"],
    "apalancado_sp500": ["UPRO", "SPXL"],
    "apalancado_nasdaq_tec": ["TQQQ", "TECL"],
    "apalancado_semis": ["SOXL"],
    "oro": ["GLD", "IAU"],
    "mineras": ["GDX", "COPX"],
    "bonos": ["TLT", "IEF", "HYG"],
    "utilities": ["XLU"],
    "tecnologia_etf": ["XLK"],
}
UNIVERSO_US = ["WMT", "COST", "KO", "PG", "PM", "AMZN", "TSLA", "HD", "XOM", "CVX", "SPCX", "CAT", "GE", "GEV", "RTX",
               "LLY", "JNJ", "ABBV", "MRK", "UNH", "TMO", "GOOGL", "META", "NFLX", "BRK-B", "JPM", "V", "MA", "BAC",
               "MS", "GS", "WFC", "NVDA", "AAPL", "MSFT", "AVGO", "MU", "AMD", "INTC", "PLTR", "ORCL", "CSCO", "LRCX",
               "AMAT", "DELL", "PANW", "CRWD", "ANET", "SNDK", "TXN"]
FUERA = ["TSM", "ASML", "UBER"]
ETFS = ["SPYM", "QQQM", "SPXL", "UPRO", "TQQQ", "TECL", "SOXL", "GLD", "IAU", "GDX", "COPX", "XLE", "XLK", "XLV",
        "XLU", "XLP", "XLF", "XLI", "SMH", "SOXX", "TLT", "IEF", "HYG"]
ALIAS_MX = {"BRK-B": "BRKB"}  # clave en el SIC
AUX = ["^GSPC", "^NDX", "^VIX", "SPY", "QQQ"]


def grafica(t: str, rango: str, cache: float):
    url = URL_YAHOO + __import__("urllib.parse").parse.quote(t, safe="") + "?range=" + rango + "&interval=1d"
    for k in range(4):
        try:
            r = json.loads(descargar(url, UA_NAVEGADOR, cache_horas=cache))["chart"]["result"][0]
            break
        except ErrorDatos as e:
            if "429" in str(e) and k < 3:
                time.sleep(15 * (k + 1))
                continue
            raise
    off = int(r["meta"].get("gmtoffset", 0))
    q = r["indicators"]["quote"][0]
    adj = (r["indicators"].get("adjclose") or [{}])[0].get("adjclose")
    filas = {}
    ts_list = r.get("timestamp") or []
    rmp, rmt = r["meta"].get("regularMarketPrice"), r["meta"].get("regularMarketTime")
    for i, ts in enumerate(ts_list):
        # Yahoo a veces deja la ultima vela en null justo despues del cierre: se usa regularMarketPrice del mismo dia
        if i == len(ts_list) - 1 and q["close"][i] is None and rmp and rmt and \
                datetime.fromtimestamp(rmt + off, tz=timezone.utc).date() == datetime.fromtimestamp(ts + off, tz=timezone.utc).date():
            q["close"][i] = rmp
            if adj and i < len(adj):
                adj[i] = rmp
        c = (adj[i] if adj and i < len(adj) and adj[i] is not None else
             (q["close"][i] if i < len(q["close"]) else None))
        if c is None:
            continue
        d = datetime.fromtimestamp(ts + off, tz=timezone.utc).date()
        v = q["volume"][i] if i < len(q.get("volume", [])) and q["volume"][i] is not None else 0
        raw = q["close"][i] if q["close"][i] is not None else c
        filas[d] = (float(c), float(raw), float(v))
    time.sleep(0.4)
    return sorted(filas.items()), r["meta"]


def ventanas(cierres: list[float], T: float, S: float, H: int, mask=None):
    """Resuelve cada ventana: devuelve lista de (resultado, retorno). resultado: 'obj','stop','plazo'."""
    out = []
    n = len(cierres)
    for i in range(0, n - H):
        if mask is not None and not mask[i]:
            continue
        p0 = cierres[i]
        res = None
        for j in range(i + 1, i + H + 1):
            r = cierres[j] / p0 - 1
            if r >= T:
                res = ("obj", T)
                break
            if r <= -S:
                res = ("stop", min(r, -S) if r < -S else -S)
                break
        if res is None:
            res = ("plazo", cierres[i + H] / p0 - 1)
        out.append(res)
    return out


def frac_final(cierres, T, H):
    """Fraccion de ventanas moviles (todas las fechas de inicio) cuyo retorno al plazo H es >= T."""
    n = len(cierres) - H
    if n <= 0:
        return 0, None
    k = sum(1 for i in range(n) if cierres[i + H] / cierres[i] - 1 >= T)
    return n, k / n


def resumen(v):
    if not v:
        return None
    n = len(v)
    ph = sum(1 for a, _ in v if a == "obj") / n
    ps = sum(1 for a, _ in v if a == "stop") / n
    ev = sum(r for _, r in v) / n
    return dict(n=n, p_obj=ph, p_stop=ps, ev=ev)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True)
    ap.add_argument("--corte", default=None)
    ap.add_argument("--cache-horas", type=float, default=6.0)
    a = ap.parse_args(argv)
    corte = date.fromisoformat(a.corte) if a.corte else date.today()
    cache = a.cache_horas
    todos = list(dict.fromkeys(UNIVERSO_US + FUERA + ETFS + AUX))
    datos = {}
    for k, t in enumerate(todos):
        try:
            datos[t], _ = grafica(t, "10y", cache)
            datos[t] = [(d, x) for d, x in datos[t] if d <= corte]
            print(f"[{k+1}/{len(todos)}] {t}: {len(datos[t])} sesiones", file=sys.stderr)
        except ErrorDatos as e:
            print(f"[{k+1}/{len(todos)}] {t}: ERROR {e}", file=sys.stderr)
    # SIC proxy
    sic = {}
    for t in UNIVERSO_US + FUERA + ETFS:
        try:
            s, _ = grafica(ALIAS_MX.get(t, t) + ".MX", "3mo", cache)
            s = [(d, x) for d, x in s if d <= corte][-22:]
            sic[t] = (sum(1 for _, x in s if x[2] > 0), s[-1][1][1] if s else None, s[-1][0] if s else None)
        except ErrorDatos:
            sic[t] = (None, None, None)
    fx = pantalla.fx_cierre_eua(cache)
    fx = [(d, x) for d, x in fx if d <= corte]
    usdmxn = fx[-1][1]

    def retorno_diario_mxn(t, n=61):
        s = [(d, x[0]) for d, x in datos[t]]
        mx = pantalla.a_mxn(s, fx)
        return {mx[i][0]: mx[i][1] / mx[i - 1][1] - 1 for i in range(1, len(mx))}

    rc = {t: retorno_diario_mxn(t) for t in CARTERA}
    fechas_c = sorted(set.intersection(*[set(r) for r in rc.values()]))[-60:]
    cart = [sum(CARTERA[t] * rc[t][d] for t in CARTERA) / sum(CARTERA.values()) for d in fechas_c]

    def corr(x, y):
        mx, my = statistics.mean(x), statistics.mean(y)
        sx = math.sqrt(sum((i - mx) ** 2 for i in x))
        sy = math.sqrt(sum((i - my) ** 2 for i in y))
        return sum((i - mx) * (j - my) for i, j in zip(x, y)) / (sx * sy) if sx and sy else float("nan")

    # cierres y ventanas por serie
    cier = {t: [x[0] for _, x in datos[t]] for t in datos}
    vol_sesiones = {}
    plant_res = {}
    for nombre, pl in PLANTILLAS.items():
        for t in todos:
            if t in cier and not t.startswith("^"):
                plant_res[(t, nombre)] = ventanas(cier[t], pl["T"], pl["S"], pl["H"])
    grupo_de = {}
    for g, ms in GRUPOS.items():
        for m in ms:
            grupo_de.setdefault(m, []).append(g)

    ref = {nombre: resumen(plant_res[("SPYM", nombre)])["ev"] for nombre in PLANTILLAS}
    FINAL = {"Diamante": (0.40, 63), "Platino": (0.50, 105), "Oro": (0.20, 147)}
    filas = []
    for t in UNIVERSO_US + FUERA + ETFS:
        if t not in datos:
            continue
        s = datos[t]
        if len(s) < 253:
            print(f"{t}: solo {len(s)} sesiones; fila con datos parciales", file=sys.stderr)
        px = [x[0] for _, x in s]
        raw = [x[1] for _, x in s]
        vol = [x[2] for _, x in s]
        f = {"ticker": t, "tipo": "accion_universo" if t in UNIVERSO_US else ("accion_fuera" if t in FUERA else "etf"),
             "fecha": s[-1][0].isoformat(), "precio_usd": round(raw[-1], 2)}
        if f["fecha"] != corte.isoformat():
            f["nota_fecha"] = "ultimo dato " + f["fecha"]
        d24 = dict(s).get(date(2026, 9, 24))
        f["precio_24sep"] = round(d24[1], 2) if d24 else None   # cierre de referencia de los P/U de las fichas
        f["precio_mxn_titulo"] = round(raw[-1] * usdmxn, 0)
        f["cabe_real"] = f["precio_mxn_titulo"] <= (CAP_APALANCADO_REAL if t in SUBY else CAP_ACCION_REAL)
        f["cabe_papel"] = f["precio_mxn_titulo"] <= (0.5 * 20486.35 if t in SUBY else CAP_ACCION_PAPEL)

        def ret(meses_dias):
            return px[-1] / px[-1 - meses_dias] - 1 if len(px) > meses_dias else None
        f["ret_1m"], f["ret_3m"], f["ret_6m"] = ret(21), ret(63), ret(126)
        f["ret_12m"] = ret(252)
        lg = [math.log(px[i] / px[i - 1]) for i in range(len(px) - 60, len(px))]
        f["vol_60d"] = statistics.stdev(lg) * math.sqrt(252)
        sma = statistics.mean(px[-200:])
        f["dist_sma200"] = px[-1] / sma - 1 if len(px) >= 200 else None
        f["dist_max_52s"] = px[-1] / max(px[-252:]) - 1
        pico, dd = px[-min(252, len(px))], 0
        for x in px[-252:]:
            pico = max(pico, x)
            dd = min(dd, x / pico - 1)
        f["dd_max_1a"] = dd
        f["usd_vol_medio_63d_mm"] = statistics.mean(r * v for r, v in zip(raw[-63:], vol[-63:])) / 1e6
        f["sesiones_MX_22"], f["precio_MX_ultimo"], f["fecha_MX"] = sic[t]
        # correlacion 60d MXN
        try:
            rt = retorno_diario_mxn(t)
            xs = [rt[d] for d in fechas_c if d in rt]
            if len(xs) == len(fechas_c):
                f["corr60_mxn_cartera"] = corr(xs, cart)
        except Exception:
            pass
        # costos
        spread = SPREAD_LIQ if f["usd_vol_medio_63d_mm"] > 500 else SPREAD_MED
        f["costo_rt"] = COMISION_RT + spread + FX_RT
        # base rates
        gr = [g for g in grupo_de.get(t, [])]
        for nombre in PLANTILLAS:
            propio = resumen(plant_res.get((t, nombre), []))
            gv = []
            for g in gr:
                for m in GRUPOS[g]:
                    gv += plant_res.get((m, nombre), [])
            grp = resumen(gv)
            for pref, r in (("own", propio), ("grp", grp)):
                if r:
                    f[f"{nombre}_{pref}_n"] = r["n"]
                    f[f"{nombre}_{pref}_p_obj"] = round(r["p_obj"], 4)
                    f[f"{nombre}_{pref}_p_stop"] = round(r["p_stop"], 4)
                    f[f"{nombre}_{pref}_ev_bruto"] = round(r["ev"], 4)
            if propio and grp:
                h = propio if propio["p_obj"] <= grp["p_obj"] else grp   # honesta = la menor
                f[f"{nombre}_hon_fuente"] = "propia" if h is propio else "grupo"
                f[f"{nombre}_hon_p_obj"] = round(h["p_obj"], 4)
                f[f"{nombre}_hon_ev_neto"] = round(h["ev"] - f["costo_rt"], 4)
                f[f"{nombre}_hon_ev_mult"] = round(h["ev"] / f["costo_rt"], 2)
        for nombre, (Tf, Hf) in FINAL.items():
            n1, p1 = frac_final(px, Tf, Hf)
            f[f"{nombre}_fin_own_p"] = round(p1, 4) if p1 is not None else None
            acum_n = acum_k = 0
            for g in gr:
                for m in GRUPOS[g]:
                    if m in cier:
                        nn, pp = frac_final(cier[m], Tf, Hf)
                        if pp is not None:
                            acum_n += nn
                            acum_k += pp * nn
            f[f"{nombre}_fin_grp_p"] = round(acum_k / acum_n, 4) if acum_n else None
            f[f"{nombre}_ref_spym_ev_bruto"] = round(ref[nombre], 4)
        f["sma50"] = round(statistics.mean(raw[-50:]), 2) if len(raw) >= 50 else None
        f["sma200"] = round(statistics.mean(raw[-200:]), 2) if len(raw) >= 200 else None
        f["max_52s"] = round(max(raw[-252:]), 2)
        # apalancados con filtro
        if t in SUBY and SUBY[t] in cier and "^VIX" in cier:
            u = dict(datos[SUBY[t]])
            vx = dict(datos["^VIX"])
            fechas = [d for d, _ in s]
            ub = [u.get(d, (None,))[0] for d in fechas]
            vv = [vx.get(d, (None,))[0] for d in fechas]
            maskA = []
            for i in range(len(fechas)):
                if i < 200 or ub[i] is None or vv[i] is None:
                    maskA.append(False)
                    continue
                w = [x for x in ub[i - 199:i + 1] if x is not None]
                if len(w) < 190:
                    maskA.append(False)
                    continue
                m = statistics.mean(w)
                maskA.append(ub[i] > m * 1.03 and vv[i] < 25)
            for nombre, pl in PLANTILLAS.items():
                v = ventanas(px, pl["T"], pl["S"], pl["H"], mask=maskA)
                r = resumen(v)
                if r:
                    f[f"{nombre}_filtro_n"] = r["n"]
                    f[f"{nombre}_filtro_p_obj"] = round(r["p_obj"], 4)
                    f[f"{nombre}_filtro_p_stop"] = round(r["p_stop"], 4)
                    f[f"{nombre}_filtro_ev_bruto"] = round(r["ev"], 4)
            f["filtro_hoy"] = bool(maskA[-1])
            f["suby"] = SUBY[t]
            # costo por volatilidad: 12m real vs 3x del subyacente y formula teorica
            L = 2.0 if False else 3.0
            ub12 = ub[-1] / ub[-253] - 1 if ub[-253] else None
            f["suby_ret_12m"] = ub12
            sg = statistics.stdev([math.log(ub[i] / ub[i - 1]) for i in range(len(ub) - 60, len(ub)) if ub[i] and ub[i - 1]]) * math.sqrt(252)
            f["suby_vol_60d"] = sg
            f["drag_teorico_anual"] = (L * L - L) / 2 * sg ** 2
        filas.append(f)

    campos = []
    for f in filas:
        for k in f:
            if k not in campos:
                campos.append(k)
    with open(a.salida, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        for f in filas:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in f.items()})
    print(f"CSV: {a.salida} ({len(filas)} filas; corte {corte}; USDMXN {usdmxn:.4f}; corr sobre {len(fechas_c)} dias)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
