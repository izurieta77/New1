#!/usr/bin/env python3
"""R02 - verificacion independiente (referee, 2026-09-25). No registra nada en R02-variantes.csv.

Reproduce desde la raiz del repo:  python3 laboratorio/replicas/R02_verificacion.py
Requiere haber corrido R02.py (usa el cache de datos que deja y lee R02-variantes.csv para comparar).

Que hace, SIN herramientas/backtest.py, SIN herramientas/datos_historicos.py y SIN herramientas/estadistica.py:
  1. Lee los zips de French y los JSON de Yahoo del cache con un parser propio y los compara con
     los que usa R02.py (via datos_historicos) -> diferencia maxima.
  2. Dividendos: reconstruye el rendimiento diario de cada ETF con close + dividendo del evento
     'dividends' de Yahoo y lo compara con el de adjclose. Compara SPY (adjclose) con el mercado
     total de French 1993-2026 (diferencia de CAGR).
  3. Volatilidad EWMA propia por suma ponderada directa (ventana de 3,000 dias), no recursiva.
  4. Simula de nuevo las variantes clave con un motor propio (pesos, deriva, costos) y calcula
     Sharpe, t de Newey-West, CAGR y MDD con codigo propio; compara con la ultima corrida del CSV.
  5. Prueba de look-ahead por perturbacion: reemplaza por ruido todos los datos posteriores a una
     fecha T (mensuales y diarios) y corre las senales de R02.py con el motor de R02; los pesos
     decididos con informacion hasta T deben ser identicos.
  6. DSR recalculado con formula propia (Bailey y Lopez de Prado 2014) desde el CSV.
"""
from __future__ import annotations

import csv
import io
import json
import math
import random
import statistics
import sys
import urllib.parse
import zipfile
from bisect import bisect_right
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from statistics import NormalDist

RAIZ = Path(__file__).resolve().parents[2]
for p in (str(RAIZ), str(Path(__file__).resolve().parent)):
    if p not in sys.path:
        sys.path.insert(0, p)

CACHE = RAIZ / "datos" / "cache"
ETFS = ("SPY", "EFA", "EEM", "TLT", "IEF", "GLD", "DBC", "VNQ")
CORTE = date(2011, 12, 31)
DELTA = 60.0 / 61.0
FIN_MUESTRA = date(2026, 7, 31)
COSTO_DEFECTO = round(0.0025 * 1.16, 10) + 0.0005  # comision GBM 0.29% + spread 0.05% por lado
N01 = NormalDist()


# ================================================================ datos (parsers propios)

def fin_mes(y: int, m: int) -> date:
    return (date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1))


def french_propio(nombre: str) -> dict:
    """Primera tabla del CSV (YYYYMM o YYYYMMDD) -> {columna: [(fecha, decimal)]}."""
    with zipfile.ZipFile(CACHE / "french" / f"{nombre}_CSV.zip") as z:
        texto = z.read(z.namelist()[0]).decode("latin-1")
    columnas, datos, en_tabla = None, None, False
    for linea in texto.splitlines():
        celdas = [c.strip() for c in linea.split(",")]
        if not en_tabla:
            if len(celdas) > 2 and celdas[0] == "" and "Mkt-RF" in celdas:
                columnas = celdas[1:]
                datos = {c: [] for c in columnas}
                en_tabla = True
            continue
        if not celdas[0].isdigit():
            break
        tok = celdas[0]
        f = date(int(tok[:4]), int(tok[4:6]), int(tok[6:])) if len(tok) == 8 else fin_mes(int(tok[:4]), int(tok[4:6]))
        for c, v in zip(columnas, celdas[1:]):
            datos[c].append((f, float(v) / 100.0))
    return datos


def yahoo_crudo(ticker: str, intervalo: str) -> dict:
    from herramientas import datos as dmod  # solo para reconstruir la URL (y asi la ruta del cache)
    params = {"period1": -2208988800, "period2": 4102444800, "interval": intervalo, "events": "div,split"}
    url = dmod.URL_YAHOO + urllib.parse.quote(ticker, safe="") + "?" + urllib.parse.urlencode(params)
    return json.loads(dmod._ruta_cache(url).read_text(encoding="utf-8"))["chart"]["result"][0]


def dia_local(ts: int, desfase: int) -> date:
    x = datetime.fromtimestamp(ts + desfase, tz=timezone.utc)
    return (x + timedelta(hours=2)).date()  # barras a medianoche local +-1 h por horario de verano


def yahoo_propio(ticker: str, intervalo: str, mes_en_curso=(2026, 9)) -> dict:
    """{'precio': [(fecha, adjclose)], 'close': [...], 'div': {fecha: monto}} con fecha fin de mes
    (mensual) o dia de negociacion (diario). Se descarta el mes en curso."""
    r = yahoo_crudo(ticker, intervalo)
    desfase = int(r["meta"].get("gmtoffset", 0))
    adj = r["indicators"]["adjclose"][0]["adjclose"]
    cl = r["indicators"]["quote"][0]["close"]
    por = {}
    for ts, a, c in zip(r["timestamp"], adj, cl):
        if a is None:
            continue
        d = dia_local(ts, desfase)
        clave = fin_mes(d.year, d.month) if intervalo == "1mo" else d
        if intervalo == "1mo" and (d.year, d.month) >= mes_en_curso:
            continue
        por[clave] = (a, c)
    div = {}
    for ev in (r.get("events", {}).get("dividends") or {}).values():
        div[dia_local(int(ev["date"]), desfase)] = float(ev["amount"])
    fechas = sorted(por)
    return {"precio": [(f, por[f][0]) for f in fechas], "close": [(f, por[f][1]) for f in fechas], "div": div}


def rend(serie: list) -> list:
    return [(f1, p1 / p0 - 1) for (f0, p0), (f1, p1) in zip(serie, serie[1:])]


def fred_propio() -> list:
    from herramientas import datos as dmod
    url = dmod.URL_FRED + "?" + urllib.parse.urlencode({"id": "DEXMXUS"})
    filas = list(csv.reader(io.StringIO(dmod._ruta_cache(url).read_text(encoding="utf-8"))))[1:]
    return [(date.fromisoformat(a), float(b)) for a, b in filas if b not in ("", ".")]


# ================================================================ vol EWMA propia (suma directa)

def vol_en_fechas(diarios: list, fechas_decision: list, ventana: int = 3000, minimo: int = 120) -> dict:
    """sigma anual en cada fecha de decision con los rendimientos diarios con fecha <= esa fecha."""
    fd = [f for f, _ in diarios]
    rs = [r for _, r in diarios]
    salida, k = {}, -1
    for D in fechas_decision:
        while k + 1 < len(fd) and fd[k + 1] <= D:
            k += 1
        if k + 1 < minimo:
            continue
        j0 = max(0, k - ventana + 1)
        pesos = [DELTA ** (k - j) for j in range(j0, k + 1)]
        sw = sum(pesos)
        media = sum(w * rs[j] for w, j in zip(pesos, range(j0, k + 1))) / sw
        var = sum(w * (rs[j] - media) ** 2 for w, j in zip(pesos, range(j0, k + 1))) / sw
        salida[D] = (fd[k], math.sqrt(261 * var))
    return salida


# ================================================================ motor y metricas propios

def simular(fechas: list, activos: dict, rf: dict, pesos_por_fecha: dict, costo: float, fx: dict | None = None):
    """pesos_por_fecha[t] = {activo: w} decidido al cierre previo. Devuelve [(fecha, r_neto, r_ef)]."""
    salida, w_prev, ra_prev, rb_prev = [], None, None, None
    for t in fechas:
        w = pesos_por_fecha[t]
        f = fx[t] if fx else 1.0
        ra = {k: (1 + activos[k][t]) * f - 1 for k in w}
        re_ = (1 + rf[t]) * f - 1
        if w_prev is None:
            w_pre = {k: 0.0 for k in w}
        else:
            w_pre = {k: w_prev[k] * (1 + ra_prev[k]) / (1 + rb_prev) for k in w}
        giro = sum(abs(w[k] - w_pre[k]) for k in w)
        rb = sum(w[k] * ra[k] for k in w) + (1 - sum(w.values())) * re_
        rn = (1 - giro * costo) * (1 + rb) - 1
        salida.append((t, rn, re_))
        w_prev, ra_prev, rb_prev = w, ra, rb
    return salida


def metricas(serie: list, f0: date, f1: date) -> dict:
    tramo = [(t, rn, re_) for t, rn, re_ in serie if f0 < t <= f1]
    ex = [rn - re_ for _, rn, re_ in tramo]
    n = len(ex)
    media = sum(ex) / n
    sd = math.sqrt(sum((x - media) ** 2 for x in ex) / (n - 1))
    # Newey-West, Bartlett, 6 rezagos, error estandar sqrt(S/(n-1))
    u = [x - media for x in ex]
    S = sum(a * a for a in u) / n
    for j in range(1, 7):
        S += 2 * (1 - j / 7) * sum(u[i] * u[i - j] for i in range(j, n)) / n
    nw_t = media / math.sqrt(S / (n - 1))
    v, pico, mdd = 1.0, 1.0, 0.0
    for _, rn, _ in tramo:
        v *= 1 + rn
        pico = max(pico, v)
        mdd = min(mdd, v / pico - 1)
    dias = (tramo[-1][0] - f0).days  # f0 = cierre previo al primer mes del tramo
    return {"n": n, "sharpe": media / sd * math.sqrt(12), "nw_t": nw_t, "mdd": mdd,
            "cagr": v ** (365.25 / dias) - 1, "sr_periodo": media / sd}


def signo(hist_a: list, hist_e: list, L: int) -> float:
    return 1.0 if math.prod(1 + x for x in hist_a[-L:]) > math.prod(1 + x for x in hist_e[-L:]) else -1.0


# ================================================================ DSR propio

def dsr(sr: float, n: int, N: int, V: float, g3: float, g4: float) -> tuple:
    e = 0.5772156649015329
    sr0 = math.sqrt(V) * ((1 - e) * N01.inv_cdf(1 - 1 / N) + e * N01.inv_cdf(1 - 1 / (N * math.e)))
    z = (sr - sr0) * math.sqrt(n - 1) / math.sqrt(1 - g3 * sr + (g4 - 1) / 4 * sr * sr)
    return N01.cdf(z), sr0


# ================================================================ principal

def main() -> None:
    import R02
    from herramientas import backtest as bt
    from herramientas import datos_historicos as dh

    print("R02 - verificacion independiente (no registra)\n")
    registro = list(csv.DictReader(open(RAIZ / "laboratorio/replicas/R02-variantes.csv", encoding="utf-8")))
    ultima = {}
    for f in registro:
        ultima[(f["variante"], f["segmento"], f["moneda"], f["comision_por_lado"], f["spread_por_lado"])] = f

    # ---------------- 1. datos
    ffm = french_propio("F-F_Research_Data_Factors")
    ffd = french_propio("F-F_Research_Data_Factors_daily")
    mercado = {f: a + b for (f, a), (_, b) in zip(ffm["Mkt-RF"], ffm["RF"])}
    rf = dict(ffm["RF"])
    ref_m = dict(dh.rendimiento_mercado_french(dh.french("F-F_Research_Data_Factors", "mensual")))
    ref_d = dict(dh.columna(dh.french("F-F_Research_Data_Factors_daily", "diaria"), "Mkt-RF"))
    print("## 1. Datos con parser propio")
    print(f"- French mensual: {len(mercado)} meses; max |propio - R02| = "
          f"{max(abs(mercado[f] - ref_m[f]) for f in mercado):.2e}; fechas iguales = {set(mercado) == set(ref_m)}")
    print(f"- French diario: {len(ffd['Mkt-RF'])} dias; max |propio - R02| = "
          f"{max(abs(v - ref_d[f]) for f, v in ffd['Mkt-RF']):.2e}; fechas iguales = {set(dict(ffd['Mkt-RF'])) == set(ref_d)}")
    men, dia, crudo_d = {}, {}, {}
    for k in ETFS:
        ym = yahoo_propio(k, "1mo")
        yd = yahoo_propio(k, "1d")
        men[k] = dict(rend(ym["precio"]))
        dia[k] = rend(yd["precio"])
        crudo_d[k] = yd
        hm = dh.yahoo_historia(k, "1mo")
        r02 = dict(dh.rendimientos_de_precios(hm["fechas"], hm["precios"]))
        comunes = set(men[k]) & set(r02)
        print(f"- {k}: mensual propio {min(men[k])} a {max(men[k])} (n={len(men[k])}); fechas iguales a R02 = "
              f"{set(men[k]) == set(r02)}; max |dif| = {max(abs(men[k][f] - r02[f]) for f in comunes):.2e}")

    # ---------------- 2. dividendos
    print("\n## 2. Dividendos (rendimiento total)")
    for k in ETFS:
        yd = crudo_d[k]
        cl = yd["close"]
        adj = dict(yd["precio"])
        difs, fuera, n_div, acum_adj, acum_cl = [], [], 0, 1.0, 1.0
        for (f0, c0), (f1, c1) in zip(cl, cl[1:]):
            if c0 is None or c1 is None:
                continue
            d = yd["div"].get(f1, 0.0)
            n_div += d > 0
            r_tr = (c1 + d) / c0 - 1
            r_adj = adj[f1] / adj[f0] - 1
            (difs if f1 <= FIN_MUESTRA else fuera).append((abs(r_tr - r_adj), f1))
            acum_adj *= 1 + r_adj
            acum_cl *= c1 / c0
        anios = (cl[-1][0] - cl[0][0]).days / 365.25
        peor_f = max(fuera) if fuera else (0.0, None)
        print(f"- {k}: {n_div} dividendos en eventos; max |r(close+div) - r(adjclose)| diario hasta {FIN_MUESTRA} = "
              f"{max(difs)[0]:.2e} ({max(difs)[1]}); despues = {peor_f[0]:.2e} ({peor_f[1]}); "
              f"CAGR adjclose - CAGR close = {acum_adj ** (1 / anios) - acum_cl ** (1 / anios):.4f}")
    spy = men["SPY"]
    comunes = sorted(f for f in spy if f in mercado)
    a1 = math.prod(1 + spy[f] for f in comunes)
    a2 = math.prod(1 + mercado[f] for f in comunes)
    anios = (comunes[-1] - comunes[0]).days / 365.25 + 1 / 12
    rho = statistics.correlation([spy[f] for f in comunes], [mercado[f] for f in comunes])
    print(f"- SPY (adjclose) vs mercado French, {comunes[0]} a {comunes[-1]} (n={len(comunes)}): CAGR SPY = "
          f"{a1 ** (1 / anios) - 1:.4f}, CAGR French = {a2 ** (1 / anios) - 1:.4f}, correlacion mensual = {rho:.4f}")

    # ---------------- 3 y 4. motor propio
    print("\n## 3-4. Motor, volatilidad y metricas propios contra el CSV (ultima corrida)")
    fechas_a = sorted(f for f in mercado if f in rf)
    vol_a = vol_en_fechas(ffd["Mkt-RF"], fechas_a)
    fechas_eval_a = fechas_a[12:]

    def pesos_a(regla: str, L: int = 12) -> dict:
        salida = {}
        for i, t in enumerate(fechas_a):
            if i < 12:
                continue
            ha = [mercado[f] for f in fechas_a[:i]]
            he = [rf[f] for f in fechas_a[:i]]
            dec = fechas_a[i - 1]
            fv, sig = vol_a[dec]
            assert (dec - fv).days <= 10
            if regla == "ls_vt40":
                w = signo(ha, he, L) * min(10.0, 0.40 / sig)
            elif regla == "lo":
                w = 1.0 if signo(ha, he, L) > 0 else 0.0
            elif regla == "bh":
                w = 1.0
            elif regla == "sma10":
                idx = [math.prod(1 + x for x in ha[:j + 1]) for j in range(len(ha) - 10, len(ha))]
                w = 1.0 if idx[-1] > sum(idx) / 10 else 0.0
            elif regla == "largo_vt40":
                w = min(10.0, 0.40 / sig)
            salida[t] = {"M": w}
        return salida

    peor = 0.0

    def comparar(nombre, serie, moneda, com, spr, extra=""):
        nonlocal peor
        for seg, f0, f1 in (("completo", date(1900, 1, 1), date(2100, 1, 1)), ("dentro_muestra", date(1900, 1, 1), CORTE),
                            ("fuera_muestra", CORTE, date(2100, 1, 1))):
            fila = ultima[(nombre, seg, moneda, repr(com), repr(spr))]
            f_ini = date.fromisoformat(fila["fecha_inicio"])
            x = metricas(serie, max(f0, f_ini), f1)
            d = max(abs(x["sharpe"] - float(fila["sharpe"])), abs(x["cagr"] - float(fila["cagr"])),
                    abs(x["mdd"] - float(fila["mdd"])))
            peor = max(peor, d)
            print(f"- {nombre} {extra}[{seg}] n={x['n']} sharpe={x['sharpe']:.4f} (CSV {float(fila['sharpe']):.4f}) "
                  f"nw_t={x['nw_t']:.4f} cagr={x['cagr']:.4f} mdd={x['mdd']:.4f}; max dif = {d:.1e}")

    com_def, spr_def = round(0.0025 * 1.16, 10), 0.0005
    efectivo_a = {t: rf[t] for t in fechas_eval_a}
    for nombre, regla in (("A_ls_vt40_L12", "ls_vt40"), ("A_lo_L12", "lo"), ("A_ref_comprar_mantener", "bh"),
                          ("A_ref_sma10", "sma10"), ("A_ref_largo_vt40", "largo_vt40")):
        pw = pesos_a(regla)
        for com, spr, costo, etiqueta in ((com_def, spr_def, COSTO_DEFECTO, "defecto"), (0.0, 0.0, 0.0, "bruto")):
            serie = simular(fechas_eval_a, {"M": mercado}, efectivo_a, pw, costo)
            comparar(nombre, serie, "USD", com, spr, f"({etiqueta}) ")
            if nombre == "A_ls_vt40_L12":
                x = metricas(serie, date(1984, 12, 31), date(2009, 12, 31))
                print(f"    ventana del articulo 1985-2009 ({etiqueta}): n={x['n']} sharpe={x['sharpe']:.4f} "
                      f"nw_t={x['nw_t']:.2f} cagr={x['cagr']:.4f} mdd={x['mdd']:.4f}")

    # parte (b)
    comunes_b = sorted(set(rf).intersection(*[set(men[k]) for k in ETFS]))
    vol_b = {k: vol_en_fechas(dia[k], comunes_b) for k in ETFS}
    fechas_eval_b = comunes_b[12:]
    print(f"- Muestra comun (b) propia: {comunes_b[0]} a {comunes_b[-1]} (n={len(comunes_b)}); primer mes evaluado {fechas_eval_b[0]}")

    def pesos_b(regla: str, L: int = 12) -> dict:
        salida, n = {}, len(ETFS)
        for i, t in enumerate(comunes_b):
            if i < 12:
                continue
            dec = comunes_b[i - 1]
            he = [rf[f] for f in comunes_b[:i]]
            w = {}
            for k in ETFS:
                ha = [men[k][f] for f in comunes_b[:i]]
                fv, sig = vol_b[k][dec]
                assert (dec - fv).days <= 10
                s = signo(ha, he, L)
                if regla == "ls_vt40":
                    w[k] = s * min(10.0, 0.40 / sig) / n
                elif regla == "lo_vt10":
                    w[k] = (s > 0) * min(1.0, 0.10 / sig) / n
                elif regla == "lo":
                    w[k] = (s > 0) / n
                elif regla == "1n":
                    w[k] = 1 / n
                elif regla == "vt10":
                    w[k] = min(1.0, 0.10 / sig) / n
                elif regla == "sma10":
                    idx = [math.prod(1 + x for x in ha[:j + 1]) for j in range(len(ha) - 10, len(ha))]
                    w[k] = (idx[-1] > sum(idx) / 10) / n
            salida[t] = {k: float(v) for k, v in w.items()}
        return salida

    fx_d = fred_propio()
    fxf = [f for f, _ in fx_d]

    def fx_en(D):
        return fx_d[bisect_right(fxf, D) - 1]

    factor = {}
    for a, b in zip(comunes_b, comunes_b[1:]):
        (fa, va), (fb, vb) = fx_en(a), fx_en(b)
        assert (a - fa).days <= 10 and (b - fb).days <= 10
        factor[b] = vb / va
    efectivo_b = {t: rf[t] for t in fechas_eval_b}
    for nombre, regla in (("B_ls_vt40_L12", "ls_vt40"), ("B_lo_vt10_L12", "lo_vt10"), ("B_lo_L12", "lo"),
                          ("B_ref_1N", "1n"), ("B_ref_1N_sma10", "sma10"), ("B_ref_1N_vt10", "vt10")):
        pw = pesos_b(regla)
        for com, spr, costo, etiqueta in ((com_def, spr_def, COSTO_DEFECTO, "defecto"), (0.0, 0.0, 0.0, "bruto")):
            serie = simular(fechas_eval_b, men, efectivo_b, pw, costo)
            comparar(nombre, serie, "USD", com, spr, f"({etiqueta}) ")
        serie = simular(fechas_eval_b, men, efectivo_b, pw, COSTO_DEFECTO, fx=factor)
        comparar(nombre, serie, "MXN", com_def, spr_def, "(MXN) ")
        if nombre in ("B_lo_vt10_L12", "B_ref_1N"):
            usd = simular(fechas_eval_b, men, efectivo_b, pw, COSTO_DEFECTO)
            mxn = serie
            dif = max(abs((a[1] - a[2]) - factor[a[0]] * (b[1] - b[2])) for a, b in zip(mxn, usd))
            print(f"    {nombre}: exceso MXN = factor cambiario del mes x exceso USD (max |dif| = {dif:.1e}); "
                  f"el Sharpe en MXN contra la T-bill convertida casi no ve el tipo de cambio")
    print(f"\n=> Maxima diferencia (Sharpe, CAGR, MDD) motor propio vs CSV en todas las comparaciones: {peor:.2e}")

    # ---------------- 7. diagnostico post hoc: mezcla estatica de igual exposicion media
    print("\n## 7. Diagnostico post hoc (verificador, no registrado, no es variante): mezcla estatica con la misma"
          " exposicion media del tramo, rebalanceo mensual, costos por defecto")
    for nombre, regla, parte, seg, f0, f1 in (("A_lo_L12", "lo", "a", "dentro_muestra", date(1927, 6, 30), CORTE),
                                              ("A_lo_L12", "lo", "a", "fuera_muestra", CORTE, date(2100, 1, 1)),
                                              ("A_ref_sma10", "sma10", "a", "fuera_muestra", CORTE, date(2100, 1, 1)),
                                              ("B_lo_vt10_L12", "lo_vt10", "b", "fuera_muestra", CORTE, date(2100, 1, 1)),
                                              ("B_lo_L12", "lo", "b", "fuera_muestra", CORTE, date(2100, 1, 1)),
                                              ("B_ref_1N_sma10", "sma10", "b", "fuera_muestra", CORTE, date(2100, 1, 1))):
        if parte == "a":
            pw, fe, act, ef = pesos_a(regla), fechas_eval_a, {"M": mercado}, efectivo_a
        else:
            pw, fe, act, ef = pesos_b(regla), fechas_eval_b, men, efectivo_b
        tramo_f = [t for t in fe if f0 < t <= f1]
        e = statistics.fmean(sum(pw[t].values()) for t in tramo_f)
        claves = list(pw[fe[0]])
        estatico = {t: {k: e / len(claves) for k in claves} for t in fe}
        x_s = metricas(simular(fe, act, ef, pw, COSTO_DEFECTO), f0, f1)
        x_e = metricas(simular(fe, act, ef, estatico, COSTO_DEFECTO), f0, f1)
        print(f"- {nombre} [{seg}]: exposicion media {e:.4f}; regla: sharpe={x_s['sharpe']:.4f} cagr={x_s['cagr']:.4f} "
              f"mdd={x_s['mdd']:.4f} | mezcla estatica: sharpe={x_e['sharpe']:.4f} cagr={x_e['cagr']:.4f} mdd={x_e['mdd']:.4f}")

    # ---------------- 5. look-ahead por perturbacion
    print("\n## 5. Look-ahead: perturbacion de datos posteriores a T")
    rnd = random.Random(7)

    def perturbar(serie, T, escala):
        return [(f, v if f <= T else rnd.gauss(0, escala)) for f, v in serie]

    T = date(1990, 6, 30)
    merc_l = sorted(mercado.items())
    rf_l = sorted(rf.items())
    dia_l = ffd["Mkt-RF"]
    vol_orig = R02.vol_como_extra(dia_l, "orig")
    vol_pert = R02.vol_como_extra(perturbar(dia_l, T, 0.03), "pert")
    iguales_a = True
    for fab, lo, hi in ((lambda: R02.senal_a_ls_vt(12, 0.40, 10.0), -10.0, 10.0), (lambda: R02.senal_a_lo(12), 0.0, 1.0),
                        (lambda: R02.senal_a_ls_vt(3, 0.40, 10.0), -10.0, 10.0)):
        r1 = bt.backtest_senal(merc_l, rf_l, fab(), id_replica=None, variante="v", min_historia=12,
                               exposicion_min=lo, exposicion_max=hi, extras={"vol": vol_orig}, comision_por_lado=0.0,
                               spread_por_lado=0.0)
        r2 = bt.backtest_senal(perturbar(merc_l, T, 0.2), perturbar(rf_l, T, 0.01), fab(), id_replica=None,
                               variante="v", min_historia=12, exposicion_min=lo, exposicion_max=hi,
                               extras={"vol": vol_pert}, comision_por_lado=0.0, spread_por_lado=0.0)
        hasta = [i for i, f in enumerate(r1.fechas) if f <= fin_mes(1990, 7)]
        dif = max(abs(r1.exposicion[i] - r2.exposicion[i]) for i in hasta)
        despues = sum(1 for i in range(len(r1.fechas)) if r1.fechas[i] > fin_mes(1990, 7)
                      and r1.exposicion[i] != r2.exposicion[i])
        iguales_a &= dif == 0
        print(f"- (a) pesos hasta el mes 1990-07 (decidido con datos <= {T}): max dif = {dif:.1e} en {len(hasta)} meses; "
              f"meses posteriores que si cambian = {despues}")
    T = date(2015, 6, 30)
    act_o = {k: sorted(men[k].items()) for k in ETFS}
    act_p = {k: perturbar(act_o[k], T, 0.08) for k in ETFS}
    rf_b = [(f, v) for f, v in sorted(rf.items()) if f >= comunes_b[0]]
    ext_o = {"vol_" + k: R02.vol_como_extra(dia[k], k) for k in ETFS}
    ext_p = {"vol_" + k: R02.vol_como_extra(perturbar(dia[k], T, 0.02), k) for k in ETFS}
    for modo, L, obj, tope, lo, hi, bruto in (("ls_vt", 12, 0.40, 10.0, -1.25, 1.25, 10.0), ("lo_vt", 12, 0.10, 1.0, 0.0, 0.125, 1.0),
                                              ("ref_sma10", 12, 0.0, 1.0, 0.0, 0.125, 1.0)):
        r1 = R02.backtest_cartera(act_o, rf_b, R02.senal_cartera(modo, ETFS, L, obj, tope), id_replica=None, variante="v",
                                  min_historia=12, peso_min=lo, peso_max=hi, bruto_max=bruto, extras=ext_o)
        r2 = R02.backtest_cartera(act_p, perturbar(rf_b, T, 0.01), R02.senal_cartera(modo, ETFS, L, obj, tope),
                                  id_replica=None, variante="v", min_historia=12, peso_min=lo, peso_max=hi,
                                  bruto_max=bruto, extras=ext_p)
        hasta = [i for i, f in enumerate(r1.fechas) if f <= fin_mes(2015, 7)]
        dif = max(abs(r1.meta["pesos"][i][k] - r2.meta["pesos"][i][k]) for i in hasta for k in ETFS)
        print(f"- (b) {modo}: pesos hasta 2015-07 (decididos con datos <= {T}): max dif = {dif:.1e} en {len(hasta)} meses")

    # ---------------- 6. DSR propio
    print("\n## 6. DSR con formula propia (N = variantes distintas con es_prueba=1 en el CSV)")
    for seg in ("dentro_muestra", "fuera_muestra"):
        unicas = {}
        for f in registro:
            if f["segmento"] == seg and f["es_prueba"] == "1":
                unicas[(f["variante"], f["parametros_json"])] = f
        N = len(unicas)
        srs = [float(f["sharpe_periodo"]) for f in unicas.values()]
        V = statistics.variance(srs)
        for var in ("A_ls_vt40_L12", "A_lo_L12", "B_ls_vt40_L12", "B_lo_vt10_L12", "B_lo_vt10_L3"):
            f = [x for x in unicas.values() if x["variante"] == var][0]
            p, sr0 = dsr(float(f["sharpe_periodo"]), int(float(f["n_periodos"])), N, V, float(f["asimetria"]),
                         float(f["curtosis"]))
            print(f"- [{seg}] {var}: N={N} V={V:.6f} DSR={p:.4f} SR0_anual={sr0 * math.sqrt(12):.4f}")


if __name__ == "__main__":
    main()
