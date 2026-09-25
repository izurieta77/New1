#!/usr/bin/env python3
"""V04. Doble ejecucion independiente (auditor-de-replicas, 2026-09-25).

Escrito SIN leer reproducir.py. Solo se leyeron la seccion PRE-REGISTRO del README
(copia literal de prerregistro.md) y los datos congelados en datos/.

Todo el calculo es propio (solo biblioteca estandar):
  - parsers de Yahoo (JSON), FRED (CSV) y Banxico (CSV latin-1),
  - alineacion por fecha (precio y tipo de cambio siempre del mismo dia),
  - conversion a MXN, indice de CETES con interes simple entre subastas,
  - simulador mensual de la SMA con costos GBM sobre |dw|,
  - metricas (CAGR, vol, Sharpe, MDD, PSR, DSR), Newey-West con dos formulas propias.
herramientas/estadistica.newey_west se usa solo como tercera comprobacion.

Salidas (sin red, deterministas):
  independiente-resultados.json   cifras propias
  independiente-comparacion.csv   una fila por cifra del README (reportado, propio, dif, tolerancia)
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import statistics
import sys
from bisect import bisect_left, bisect_right
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

AQUI = Path(__file__).resolve().parent
DATOS = AQUI / "datos"
RAIZ = AQUI.parents[2]

# ============================================================== huellas

def revisar_huellas() -> dict:
    esperadas = {}
    for linea in (AQUI / "SHA256SUMS.txt").read_text().splitlines():
        if linea.strip():
            h, ruta = linea.split(None, 1)
            esperadas[ruta.strip()] = h
    salida = {}
    for ruta, h in esperadas.items():
        real = hashlib.sha256((AQUI / ruta).read_bytes()).hexdigest()
        salida[ruta] = real == h
    malas = [r for r, ok in salida.items() if not ok]
    if malas:
        raise SystemExit(f"Huellas distintas: {malas}")
    return salida

# ============================================================== parsers propios

def leer_yahoo(nombre: str) -> dict:
    """{'close': {fecha: v}, 'adj': {fecha: v}, 'div': {fecha: monto}} en la fecha local de la bolsa."""
    d = json.loads((DATOS / nombre).read_text())
    r = d["chart"]["result"][0]
    zona = ZoneInfo(r["meta"]["exchangeTimezoneName"])
    ts = r["timestamp"]
    cierre = r["indicators"]["quote"][0]["close"]
    ajust = r["indicators"]["adjclose"][0]["adjclose"]
    close, adj = {}, {}
    for t, c, a in zip(ts, cierre, ajust):
        f = datetime.fromtimestamp(t, zona).date()
        if c is not None:
            close[f] = float(c)
        if a is not None:
            adj[f] = float(a)
    div = {}
    for _, e in (r.get("events", {}).get("dividends", {}) or {}).items():
        f = datetime.fromtimestamp(int(e["date"]), zona).date()
        div[f] = div.get(f, 0.0) + float(e["amount"])
    return {"close": close, "adj": adj, "div": div, "moneda": r["meta"].get("currency")}


def leer_fred(nombre: str) -> dict:
    out = {}
    with open(DATOS / nombre, newline="") as fh:
        lector = csv.reader(fh)
        next(lector)
        for fila in lector:
            if len(fila) < 2:
                continue
            v = fila[1].strip()
            if v in ("", "."):
                continue
            out[date.fromisoformat(fila[0].strip())] = float(v)
    return out


def leer_banxico(nombre: str) -> dict:
    """Primera columna de datos despues de la fila "Fecha"; fechas dd/mm/aaaa; omite N/E."""
    texto = (DATOS / nombre).read_bytes().decode("latin-1")
    out = {}
    en_datos = False
    for fila in csv.reader(texto.splitlines()):
        if not fila:
            continue
        if fila[0] == "Fecha":
            en_datos = True
            continue
        if not en_datos:
            continue
        m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", fila[0].strip())
        if not m:
            continue
        v = fila[1].strip()
        try:
            x = float(v)
        except ValueError:
            continue
        out[date(int(m.group(3)), int(m.group(2)), int(m.group(1)))] = x
    return out

# ============================================================== utilidades de fechas y series

def mes(f: date) -> tuple:
    return (f.year, f.month)


def mes_sig(m: tuple) -> tuple:
    return (m[0] + 1, 1) if m[1] == 12 else (m[0], m[1] + 1)


def mes_ant(m: tuple) -> tuple:
    return (m[0] - 1, 12) if m[1] == 1 else (m[0], m[1] - 1)


def rango_meses(a: tuple, b: tuple) -> list:
    out = [a]
    while out[-1] != b:
        out.append(mes_sig(out[-1]))
    return out


def fin_de_mes(fechas) -> dict:
    """{mes: ultima fecha del mes} dentro de un conjunto de fechas."""
    out = {}
    for f in sorted(fechas):
        out[mes(f)] = f
    return out


def inicio_de_mes(fechas) -> dict:
    out = {}
    for f in sorted(fechas, reverse=True):
        out[mes(f)] = f
    return out


def producto_mxn(precio: dict, fx: dict) -> dict:
    """Precio en MXN solo en fechas con precio Y tipo de cambio del mismo dia (alerta #3)."""
    return {f: precio[f] * fx[f] for f in precio if f in fx}


def anios(d0: date, d1: date) -> float:
    return (d1 - d0).days / 365.25


def cagr_valores(v0, v1, d0, d1):
    return (v1 / v0) ** (1 / anios(d0, d1)) - 1


def mdd_curva(valores: list) -> tuple:
    """(mdd, i_pico, i_valle) con el primer valor como pico posible."""
    pico_i, peor, ip, iv = 0, 0.0, 0, 0
    for i, x in enumerate(valores):
        if x > valores[pico_i]:
            pico_i = i
        dd = x / valores[pico_i] - 1
        if dd < peor:
            peor, ip, iv = dd, pico_i, i
    return peor, ip, iv


def serie_tr(close: dict, div: dict, fraccion: float) -> dict:
    """Indice de rendimiento total: I_t = I_{t-1} * (C_t + f*D_t) / C_{t-1}."""
    fechas = sorted(close)
    out = {fechas[0]: 1.0}
    for a, b in zip(fechas, fechas[1:]):
        out[b] = out[a] * (close[b] + fraccion * div.get(b, 0.0)) / close[a]
    return out

# ============================================================== CETES: indice de interes simple entre subastas

class IndiceCetes:
    def __init__(self, subastas: dict):
        self.fechas = sorted(subastas)
        self.tasas = [subastas[f] for f in self.fechas]
        self.nivel = [1.0]
        for k in range(1, len(self.fechas)):
            dias = (self.fechas[k] - self.fechas[k - 1]).days
            self.nivel.append(self.nivel[-1] * (1 + self.tasas[k - 1] / 100 * dias / 360))

    def __call__(self, d: date) -> float:
        k = bisect_right(self.fechas, d) - 1
        if k < 0:
            raise ValueError(f"CETES sin subasta antes de {d}")
        return self.nivel[k] * (1 + self.tasas[k] / 100 * (d - self.fechas[k]).days / 360)

    def tasa_vigente(self, d: date) -> float:
        k = bisect_right(self.fechas, d) - 1
        return self.tasas[k]

    def rend(self, d0: date, d1: date) -> float:
        return self(d1) / self(d0) - 1

    def rend_particion(self, d0: date, d1: date) -> float:
        """Sensibilidad: tasa de la ultima subasta <= inicio del periodo, r = y * dias / 360."""
        return self.tasa_vigente(d0) / 100 * (d1 - d0).days / 360

# ============================================================== estadistica propia

Z95 = 1.959963984540054


def nw_autocov(x: list, L: int = 6) -> float:
    """Formula 1: suma de autocovarianzas con pesos de Bartlett; se con correccion n/(n-1)."""
    n = len(x)
    m = sum(x) / n
    u = [v - m for v in x]
    omega = sum(a * a for a in u) / n
    for j in range(1, L + 1):
        omega += 2 * (1 - j / (L + 1)) * sum(u[i] * u[i - j] for i in range(j, n)) / n
    return math.sqrt(omega / n * n / (n - 1))


def nw_sumas_moviles(x: list, L: int = 6) -> float:
    """Formula 2: con residuos rellenados con ceros, sum_t S_t^2 / (L+1) = n * Omega,
    donde S_t es la suma de L+1 residuos consecutivos."""
    n = len(x)
    m = sum(x) / n
    u = [0.0] * L + [v - m for v in x] + [0.0] * L
    total = 0.0
    for t in range(len(u) - L):
        s = sum(u[t:t + L + 1])
        total += s * s
    omega = total / (L + 1) / n
    return math.sqrt(omega / n * n / (n - 1))


def prueba_nw(x: list) -> dict:
    n = len(x)
    m = sum(x) / n
    se1 = nw_autocov(x)
    se2 = nw_sumas_moviles(x)
    sd = statistics.stdev(x)
    lo, hi = m - Z95 * se1, m + Z95 * se1
    ver = "apoyo" if lo > 0 else ("contraria" if hi < 0 else "inconcluso")
    return {"n": n, "media": m, "x12": 12 * m, "se": se1, "se_formula2": se2, "t": m / se1,
            "t_iid": m / (sd / math.sqrt(n)), "ic95": [lo, hi], "veredicto": ver}


def asim_curt(x: list) -> tuple:
    m = statistics.fmean(x)
    m2 = statistics.fmean([(a - m) ** 2 for a in x])
    m3 = statistics.fmean([(a - m) ** 3 for a in x])
    m4 = statistics.fmean([(a - m) ** 4 for a in x])
    return m3 / m2 ** 1.5, m4 / m2 ** 2


def phi(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def phi_inv(p: float) -> float:
    return statistics.NormalDist().inv_cdf(p)


def psr(sr: float, n: int, g3: float, g4: float, sr_ref: float = 0.0) -> float:
    return phi((sr - sr_ref) * math.sqrt(n - 1) / math.sqrt(1 - g3 * sr + (g4 - 1) / 4 * sr * sr))


def sr_max_esperado(N: int, var: float) -> float:
    g = 0.5772156649015329
    return math.sqrt(var) * ((1 - g) * phi_inv(1 - 1 / N) + g * phi_inv(1 - 1 / (N * math.e)))

# ============================================================== carga

def cargar() -> dict:
    D = {}
    for clave, archivo in [("SPY", "yahoo_SPY_1d.json"), ("SP500TR", "yahoo_SP500TR_1d.json"),
                           ("GSPC", "yahoo_GSPC_1d.json"), ("NAFTRAC", "yahoo_NAFTRAC.MX_1d.json"),
                           ("MXX", "yahoo_MXX_1d.json"), ("MXNX", "yahoo_MXN_X_1d.json"),
                           ("EWW", "yahoo_EWW_1d.json"), ("SPYMX", "yahoo_SPY.MX_1d.json"),
                           ("IVVMX", "yahoo_IVV.MX_1d.json"), ("VOOMX", "yahoo_VOO.MX_1d.json")]:
        D[clave] = leer_yahoo(archivo)
    D["DEX"] = leer_fred("fred_DEXMXUS.csv")
    D["FMI"] = leer_fred("fred_INTGSTMXM193N.csv")
    D["FIX"] = leer_banxico("banxico_CF102_fix_SF43718.csv")
    D["CETES_SUB"] = leer_banxico("banxico_CF107_cetes28_SF43936.csv")
    D["CETES"] = IndiceCetes(D["CETES_SUB"])
    D["FX_MXNX"] = D["MXNX"]["close"]
    return D


def valor_en(serie: dict, f: date):
    if f not in serie:
        raise KeyError(f"sin dato en {f}")
    return serie[f]

# ============================================================== bloque 1: benchmarks A1-A3

W = {"W1": (date(2007, 12, 31), date(2026, 8, 31)), "W2": (date(2008, 1, 31), date(2026, 8, 31)),
     "W3": (date(2008, 1, 2), date(2026, 9, 18)), "W4": (date(2007, 12, 31), date(2025, 12, 31))}


def cagr_ventana_mensual(serie: dict, d0: date, d1: date, diaria: bool, primer_dato: bool = False):
    """CAGR entre el cierre de mes de d0 y el de d1 (o fechas exactas si diaria).
    primer_dato: si la serie empieza despues de d0, se usa su primer dato (NAFTRAC)."""
    if diaria:
        f0, f1 = d0, d1
        if primer_dato and f0 not in serie:
            f0 = min(f for f in serie if f >= d0)
    else:
        fm = fin_de_mes(serie)
        f1 = fm[mes(d1)]
        if mes(d0) in fm:
            f0 = fm[mes(d0)]
        elif primer_dato:
            f0 = min(serie)
        else:
            raise KeyError(d0)
    return cagr_valores(serie[f0], serie[f1], f0, f1), f0, f1


def benchmarks(D: dict) -> dict:
    spy, dex, fix = D["SPY"], D["DEX"], D["FIX"]
    series = {
        "spy_dex": producto_mxn(spy["adj"], dex),
        "spy_fix": producto_mxn(spy["adj"], fix),
        "spy_mxnx": producto_mxn(spy["adj"], D["FX_MXNX"]),
        "sptr_dex": producto_mxn(D["SP500TR"]["close"], dex),
        "spy_net30_dex": producto_mxn(serie_tr(spy["close"], spy["div"], 0.7), dex),
        "gspc_dex": producto_mxn(D["GSPC"]["close"], dex),
        "spy_usd": dict(spy["adj"]),
        "naftrac_adj": D["NAFTRAC"]["adj"],
        "naftrac_close": D["NAFTRAC"]["close"],
        "mxx": D["MXX"]["close"],
        "eww_adj_dex": producto_mxn(D["EWW"]["adj"], dex),
        "eww_close_dex": producto_mxn(D["EWW"]["close"], dex),
    }
    out = {"cagr": {}, "fechas": {}}
    for nombre, s in series.items():
        for w, (d0, d1) in W.items():
            c, f0, f1 = cagr_ventana_mensual(s, d0, d1, diaria=(w == "W3"),
                                             primer_dato=nombre.startswith("naftrac"))
            out["cagr"][f"{nombre}|{w}"] = c
            out["fechas"][f"{nombre}|{w}"] = [str(f0), str(f1)]
    # CETES (indice en fechas exactas de la ventana)
    I = D["CETES"]
    for w, (d0, d1) in W.items():
        out["cagr"][f"cetes|{w}"] = cagr_valores(I(d0), I(d1), d0, d1)
    # control: SPY reconstruido con cierre + dividendos brutos
    tr = producto_mxn(serie_tr(spy["close"], spy["div"], 1.0), dex)
    out["cagr"]["spy_tr_reconstruido_dex|W1"] = cagr_ventana_mensual(tr, *W["W1"], diaria=False)[0]
    # CETES: particion mensual en W1 (cierres de mes del calendario del S&P en MXN)
    fm = fin_de_mes(series["spy_dex"])
    meses = rango_meses((2008, 1), (2026, 8))
    v = 1.0
    d_ini = fm[(2007, 12)]
    for m in meses:
        v *= 1 + I.rend_particion(fm[mes_ant(m)], fm[m])
    out["cagr"]["cetes_particion|W1"] = v ** (1 / anios(d_ini, fm[(2026, 8)])) - 1
    # particion con fechas de calendario puras
    v = 1.0
    for m in meses:
        a = date(*mes_ant(m), 1)
        a = date(a.year, a.month, 1)
        d0 = (date(*m, 1) - timedelta(days=1))
        d1 = (date(*mes_sig(m), 1) - timedelta(days=1))
        v *= 1 + I.rend_particion(d0, d1)
    out["cagr"]["cetes_particion_calendario|W1"] = v ** (1 / anios(date(2007, 12, 31), date(2026, 8, 31))) - 1
    # FMI: tasa/1200 de 2008-01 a 2026-07
    fmi = D["FMI"]
    vals = [fmi[f] for f in sorted(fmi) if (2008, 1) <= mes(f) <= (2026, 7)]
    prod = math.prod(1 + x / 1200 for x in vals)
    out["cagr"]["fmi|2008-01_2026-07"] = prod ** (12 / len(vals)) - 1
    out["n_meses_fmi"] = len(vals)
    return out, series


def sensibilidades_ventana(D: dict, S: dict) -> dict:
    I = D["CETES"]
    out = {"inicio": {}, "fin": {}}
    fin = date(2026, 8, 31)
    fuentes = {"sp_mxn": S["spy_dex"], "naftrac": S["naftrac_adj"], "sp_usd": S["spy_usd"]}
    for nombre, s in fuentes.items():
        fm = fin_de_mes(s)
        f1 = fm[(2026, 8)]
        d = {}
        for m in rango_meses((2007, 1), (2009, 12)):
            if m not in fm:
                continue
            f0 = fm[m]
            d[f"{m[0]}-{m[1]:02d}"] = cagr_valores(s[f0], s[f1], f0, f1)
        out["inicio"][nombre] = d
    d = {}
    for m in rango_meses((2007, 1), (2009, 12)):
        f0 = date(*mes_sig(m), 1) - timedelta(days=1)
        d[f"{m[0]}-{m[1]:02d}"] = cagr_valores(I(f0), I(fin), f0, fin)
    out["inicio"]["cetes"] = d
    # alternativa: CETES en los cierres de mes del S&P en MXN
    fm = fin_de_mes(S["spy_dex"])
    out["inicio"]["cetes_fechas_sp"] = {f"{m[0]}-{m[1]:02d}": cagr_valores(I(fm[m]), I(fm[(2026, 8)]), fm[m], fm[(2026, 8)])
                                       for m in rango_meses((2007, 1), (2009, 12))}
    for nombre in list(out["inicio"]):
        d = out["inicio"][nombre]
        kmin = min(d, key=d.get)
        kmax = max(d, key=d.get)
        out["inicio"][nombre + "_min"] = [kmin, d[kmin]]
        out["inicio"][nombre + "_max"] = [kmax, d[kmax]]
    d0 = date(2007, 12, 31)
    for f1 in [date(2025, 12, 31), date(2026, 6, 30), date(2026, 8, 31), date(2026, 9, 18)]:
        k = str(f1)
        out["fin"][f"sp_mxn|{k}"] = cagr_valores(S["spy_dex"][d0], S["spy_dex"][f1], d0, f1)
        n0 = min(S["naftrac_adj"])
        out["fin"][f"naftrac|{k}"] = cagr_valores(S["naftrac_adj"][n0], S["naftrac_adj"][f1], n0, f1)
        out["fin"][f"cetes|{k}"] = cagr_valores(I(d0), I(f1), d0, f1)
    return out


def dividendos_implicitos(D: dict) -> dict:
    """(1 + adj) / (1 + close) - 1 por anio calendario."""
    out = {}
    for clave in ("NAFTRAC", "EWW"):
        adj, close = D[clave]["adj"], D[clave]["close"]
        comunes = sorted(set(adj) & set(close))
        fa = fin_de_mes(comunes)
        d = {}
        for anio in range(2008, 2026):
            f1 = fa[(anio, 12)]
            f0 = fa.get((anio - 1, 12)) or min(comunes)
            ra = adj[f1] / adj[f0] - 1
            rc = close[f1] / close[f0] - 1
            d[str(anio)] = (1 + ra) / (1 + rc) - 1
        out[clave] = d
        out[clave + "_eventos_por_anio"] = {str(a): sum(1 for f in D[clave]["div"] if f.year == a)
                                            for a in range(2008, 2027)}
    return out


def naftrac_imputado(D: dict, S: dict, divs: dict) -> float:
    nf = S["naftrac_adj"]
    f0, f1 = min(nf), fin_de_mes(nf)[(2026, 8)]
    factor = math.prod(1 + divs["EWW"][str(a)] for a in (2008, 2009, 2010, 2011, 2012, 2021))
    return (nf[f1] / nf[f0] * factor) ** (1 / anios(f0, f1)) - 1


def mxx_anual(D: dict) -> dict:
    s = D["MXX"]["close"]
    fa = fin_de_mes(s)
    return {str(a): s[fa[(a, 12)]] / s[fa[(a - 1, 12)]] - 1 for a in range(2022, 2026)}


def rend_mensuales(s: dict, m0: tuple, m1: tuple, fm: dict | None = None) -> tuple:
    """Rendimientos de cierre a cierre de mes para los meses m0..m1: (lista, fechas_ini, fechas_fin)."""
    fm = fm or fin_de_mes(s)
    r, a, b = [], [], []
    for m in rango_meses(m0, m1):
        f0, f1 = fm[mes_ant(m)], fm[m]
        r.append(s[f1] / s[f0] - 1)
        a.append(f0)
        b.append(f1)
    return r, a, b


def pruebas_benchmarks(D: dict, S: dict) -> dict:
    I = D["CETES"]
    sp = S["spy_dex"]
    fm = fin_de_mes(sp)
    out = {}
    for clave, (m0, m1) in {"2008-01_2026-08": ((2008, 1), (2026, 8)),
                            "1995-01_2007-12": ((1995, 1), (2007, 12))}.items():
        r, a, b = rend_mensuales(sp, m0, m1, fm)
        c = [I.rend(x, y) for x, y in zip(a, b)]
        out[f"sp_menos_cetes|{clave}"] = prueba_nw([p - q for p, q in zip(r, c)])
    nf = S["naftrac_adj"]
    fmn = fin_de_mes(nf)
    rn, an, bn = rend_mensuales(nf, (2008, 2), (2026, 8), fmn)
    rs, _, _ = rend_mensuales(sp, (2008, 2), (2026, 8), fm)
    out["sp_menos_naftrac|2008-02_2026-08"] = prueba_nw([p - q for p, q in zip(rs, rn)])
    cn = [I.rend(x, y) for x, y in zip(an, bn)]
    out["naftrac_menos_cetes|2008-02_2026-08"] = prueba_nw([p - q for p, q in zip(rn, cn)])
    # variante: CETES en las fechas del S&P
    _, a2, b2 = rend_mensuales(sp, (2008, 2), (2026, 8), fm)
    cs = [I.rend(x, y) for x, y in zip(a2, b2)]
    out["naftrac_menos_cetes_fechas_sp|2008-02_2026-08"] = prueba_nw([p - q for p, q in zip(rn, cs)])
    return out


def amortiguador(D: dict, S: dict) -> dict:
    sp_mxn, usd, dex = S["spy_dex"], D["SPY"]["adj"], D["DEX"]
    fm = fin_de_mes(sp_mxn)  # E_m: cierres con SPY y FX el mismo dia
    meses = rango_meses((2008, 1), (2026, 8))
    r_usd = [usd[fm[m]] / usd[fm[mes_ant(m)]] - 1 for m in meses]
    r_fx = [dex[fm[m]] / dex[fm[mes_ant(m)]] - 1 for m in meses]
    r_mxn = [sp_mxn[fm[m]] / sp_mxn[fm[mes_ant(m)]] - 1 for m in meses]
    # version con cierre de mes USD propio (ultimo dia de SPY)
    fu = fin_de_mes(usd)
    r_usd2 = [usd[fu[m]] / usd[fu[mes_ant(m)]] - 1 for m in meses]
    malos = [i for i, x in enumerate(r_usd) if x < -0.05]
    curva_usd = [usd[fu[(2007, 12)]]] + [usd[fu[m]] for m in meses]
    curva_mxn = [sp_mxn[fm[(2007, 12)]]] + [sp_mxn[fm[m]] for m in meses]
    nf = S["naftrac_adj"]
    fmn = fin_de_mes(nf)
    curva_nf = [nf[min(nf)]] + [nf[fmn[m]] for m in meses]
    r_nf = [curva_nf[i + 1] / curva_nf[i] - 1 for i in range(len(meses))]
    fx0, fx1 = dex[fm[(2007, 12)]], dex[fm[(2026, 8)]]
    return {
        "corr_usd_fx": statistics.correlation(r_usd, r_fx),
        "corr_usd_fx_cierre_usd": statistics.correlation(r_usd2, r_fx),
        "n_meses_usd_menor_-5": len(malos),
        "n_meses_usd_menor_-5_cierre_usd": sum(1 for x in r_usd2 if x < -0.05),
        "media_usd_en_malos": statistics.fmean([r_usd[i] for i in malos]),
        "media_fx_en_malos": statistics.fmean([r_fx[i] for i in malos]),
        "media_mxn_en_malos": statistics.fmean([r_mxn[i] for i in malos]),
        "mdd_usd_mensual": mdd_curva(curva_usd)[0],
        "mdd_mxn_mensual": mdd_curva(curva_mxn)[0],
        "vol_usd": statistics.stdev(r_usd2) * math.sqrt(12),
        "vol_usd_fechas_E": statistics.stdev(r_usd) * math.sqrt(12),
        "vol_mxn": statistics.stdev(r_mxn) * math.sqrt(12),
        "fx_inicio": fx0, "fx_fin": fx1,
        "cagr_fx": cagr_valores(fx0, fx1, fm[(2007, 12)], fm[(2026, 8)]),
        "vol_naftrac": statistics.stdev(r_nf) * math.sqrt(12),
        "mdd_naftrac_mensual": mdd_curva(curva_nf)[0],
        "enero_2008_usd": r_usd[0], "enero_2008_mxn": r_mxn[0],
    }


def meses_cierre_distinto(D: dict, S: dict) -> dict:
    fm = fin_de_mes(S["spy_dex"])
    fu = fin_de_mes(D["SPY"]["adj"])
    distintos = [f"{m[0]}-{m[1]:02d}" for m in fm if m in fu and fm[m] != fu[m]]
    en_muestra = [x for x in distintos if "1994-01" <= x <= "2026-08"]
    return {"todos": distintos, "1994-01_2026-08": en_muestra}


def a4(D: dict) -> dict:
    dex, fix = D["DEX"], D["FIX"]
    base = {"spy": D["SPY"]["adj"], "sptr": D["SP500TR"]["close"], "gspc": D["GSPC"]["close"]}
    series = {}
    for k, s in base.items():
        series[f"{k}_usd"] = s
        series[f"{k}_mxn"] = producto_mxn(s, dex)
    series["spy_mxn_fix"] = producto_mxn(base["spy"], fix)
    series["gspc_mxn_fix"] = producto_mxn(base["gspc"], fix)
    out = {}
    for k, s in series.items():
        fechas = sorted(s)
        f0, f1 = date(2007, 12, 31), date(2008, 12, 31)
        out[f"{k}|cambio_2008"] = s[f1] / s[f0] - 1
        dias = [f for f in fechas if f0 <= f <= f1]
        mdd, ip, iv = mdd_curva([s[f] for f in dias])
        out[f"{k}|mdd_diaria_2008"] = [mdd, str(dias[ip]), str(dias[iv])]
        fm = fin_de_mes(s)
        mm = rango_meses((2007, 12), (2008, 12))
        mdd, ip, iv = mdd_curva([s[fm[m]] for m in mm])
        out[f"{k}|mdd_mensual_2008"] = [mdd, str(fm[mm[ip]]), str(fm[mm[iv]])]
        dias = [f for f in fechas if date(2007, 1, 1) <= f <= date(2009, 12, 31)]
        mdd, ip, iv = mdd_curva([s[f] for f in dias])
        out[f"{k}|mdd_diaria_crisis"] = [mdd, str(dias[ip]), str(dias[iv])]
        mm = rango_meses((2007, 1), (2009, 12))
        mdd, ip, iv = mdd_curva([s[fm[m]] for m in mm])
        out[f"{k}|mdd_mensual_crisis"] = [mdd, str(fm[mm[ip]]), str(fm[mm[iv]])]
    return out


def control_sic(D: dict) -> dict:
    """SPY.MX close contra SPY close x FX del mismo dia, desde 2016."""
    spymx, spy = D["SPYMX"]["close"], D["SPY"]["close"]
    out = {}
    for nombre, fx in (("dex", D["DEX"]), ("fix", D["FIX"]), ("mxnx", D["FX_MXNX"])):
        difs = sorted(abs(spymx[f] / (spy[f] * fx[f]) - 1) for f in spymx
                      if f >= date(2016, 1, 1) and f in spy and f in fx)
        n = len(difs)
        out[nombre] = {"n": n, "mediana": statistics.median(difs),
                       "p90": statistics.quantiles(difs, n=10)[-1]}
    s = D["SPYMX"]
    for campo in ("close", "adj"):
        fechas = sorted(s[campo])
        saltos = sum(1 for a, b in zip(fechas, fechas[1:]) if abs(s[campo][b] / s[campo][a] - 1) > 0.30)
        out[f"spymx_saltos_30|{campo}"] = saltos
    out["spymx_close_2008-08-29"] = s["close"].get(date(2008, 8, 29))
    out["spymx_close_2008-09-01"] = s["close"].get(date(2008, 9, 1))
    out["spymx_adj_2008-08-29"] = s["adj"].get(date(2008, 8, 29))
    out["spymx_adj_2008-09-01"] = s["adj"].get(date(2008, 9, 1))
    return out
