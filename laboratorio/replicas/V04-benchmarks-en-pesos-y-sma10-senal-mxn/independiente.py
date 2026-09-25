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


def _se_herramienta(x: list):
    """Tercera comprobacion (no se usa para ningun resultado): herramientas/estadistica.newey_west."""
    try:
        sys.path.insert(0, str(RAIZ))
        from herramientas.estadistica import newey_west
        return newey_west(x, 6)["se"]
    except Exception:
        return None


def prueba_nw(x: list) -> dict:
    n = len(x)
    m = sum(x) / n
    se1 = nw_autocov(x)
    se2 = nw_sumas_moviles(x)
    se3 = _se_herramienta(x)
    sd = statistics.stdev(x)
    lo, hi = m - Z95 * se1, m + Z95 * se1
    ver = "apoyo" if lo > 0 else ("contraria" if hi < 0 else "inconcluso")
    return {"n": n, "media": m, "x12": 12 * m, "se": se1, "se_formula2": se2, "se_herramienta": se3, "t": m / se1,
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

def estructura(D: dict) -> dict:
    """Hechos de estructura que el pre-registro cita (rangos de fechas, dividendos)."""
    out = {
        "DEXMXUS": [str(min(D["DEX"])), str(max(D["DEX"]))],
        "FIX": [str(min(D["FIX"])), str(max(D["FIX"]))],
        "MXN=X inicio": str(min(D["FX_MXNX"])),
        "CETES": [str(min(D["CETES_SUB"])), str(max(D["CETES_SUB"]))],
        "SPY": [str(min(D["SPY"]["adj"])), str(max(D["SPY"]["adj"]))],
        "NAFTRAC inicio": str(min(D["NAFTRAC"]["adj"])),
        "SPY.MX inicio": str(min(D["SPYMX"]["close"])),
        "IVV.MX inicio": str(min(D["IVVMX"]["close"])),
        "SPY barras sin precio": 0,
    }
    for k in ("SPYMX", "IVVMX"):
        dv = D[k]["div"]
        out[f"{k} dividendo maximo antes de 2016"] = max(v for f, v in dv.items() if f.year < 2016)
        out[f"{k} dividendo minimo desde 2016"] = min(v for f, v in dv.items() if f.year >= 2016)
    return out


# ============================================================== bloque 3: SMA mensual (A5), simulador propio

COMISION = 0.0025 * 1.16   # 0.29% por lado (Guia GBM V1025)
SPREAD = 0.0005            # 0.05% por lado (supuesto del pre-registro)


def preparar(activo_usd: dict, fx: dict, senal_usd: dict | None = None) -> dict:
    """Fechas con precio y FX el mismo dia; E = ultimo dia del mes, G = primer dia del mes."""
    senal_usd = senal_usd or activo_usd
    fechas = sorted(f for f in activo_usd if f in fx and f in senal_usd)
    return {"fechas": fechas, "E": fin_de_mes(fechas), "G": inicio_de_mes(fechas),
            "pm": {f: activo_usd[f] * fx[f] for f in fechas},
            "s_usd": {f: senal_usd[f] for f in fechas},
            "s_mxn": {f: senal_usd[f] * fx[f] for f in fechas}}


def simular(P: dict, I: IndiceCetes, regla, ejecucion: str, m0: tuple, m1: tuple,
            costo_lado: float = COMISION + SPREAD, w_inicial: float = 0.0, efectivo: str = "indice") -> dict:
    """regla: ('bh',) | ('cetes',) | ('sma', n, 'usd'|'mxn').
    Mes m: decision con el cierre E_{m-1}; T0 opera en E_{m-1} (periodo E_{m-1}..E_m);
    T1 opera en G_m, primer dia del mes m (periodo G_m..G_{m+1})."""
    E, G, pm = P["E"], P["G"], P["pm"]
    filas = []
    w_prev = w_inicial
    for m in rango_meses(m0, m1):
        if regla[0] == "bh":
            w = 1.0
        elif regla[0] == "cetes":
            w = 0.0
        else:
            n, moneda = regla[1], regla[2]
            s = P["s_usd"] if moneda == "usd" else P["s_mxn"]
            cierres = []
            k = mes_ant(m)
            for _ in range(n):
                cierres.append(s[E[k]])
                k = mes_ant(k)
            cierres.reverse()
            w = 1.0 if cierres[-1] > statistics.fmean(cierres) else 0.0
        if ejecucion == "T0":
            d0, d1 = E[mes_ant(m)], E[m]
        else:
            d0, d1 = G[m], G[mes_sig(m)]
        ra = pm[d1] / pm[d0] - 1
        re_ = I.rend(d0, d1) if efectivo == "indice" else I.rend_particion(d0, d1)
        c = abs(w - w_prev) * costo_lado
        rb = w * ra + (1 - w) * re_
        rn = (1 - c) * (1 + rb) - 1
        filas.append({"mes": m, "d0": d0, "d1": d1, "w": w, "w_prev": w_prev, "c": c,
                      "ra": ra, "re": re_, "rn": rn})
        w_prev = w
    return {"filas": filas}


def metricas(filas: list) -> dict:
    rn = [f["rn"] for f in filas]
    ex = [f["rn"] - f["re"] for f in filas]
    d0, d1 = filas[0]["d0"], filas[-1]["d1"]
    curva = [1.0]
    for r in rn:
        curva.append(curva[-1] * (1 + r))
    a = anios(d0, d1)
    fechas_curva = [d0] + [f["d1"] for f in filas]
    mdd, ip, iv = mdd_curva(curva)
    sd_ex = statistics.stdev(ex)
    sr_p = statistics.fmean(ex) / sd_ex if sd_ex > 0 else None
    g3, g4 = asim_curt(ex) if sd_ex > 0 else (None, None)
    return {
        "n": len(rn), "d0": str(d0), "d1": str(d1),
        "cagr": curva[-1] ** (1 / a) - 1,
        "vol": statistics.stdev(rn) * math.sqrt(12),
        "sharpe": sr_p * math.sqrt(12) if sr_p is not None else None,
        "sr_periodo": sr_p, "asimetria": g3, "curtosis": g4,
        "psr": psr(sr_p, len(ex), g3, g4) if sr_p is not None else None,
        "mdd": mdd, "mdd_pico": str(fechas_curva[ip]), "mdd_valle": str(fechas_curva[iv]),
        "tiempo": sum(1 for f in filas if f["w"] != 0) / len(filas),
        "cambios": sum(1 for f in filas if f["w"] != f["w_prev"]),
        "costo_anual": sum(f["c"] for f in filas) / a,
    }


SEG = {"1995-2007": ((1995, 1), (2007, 12)), "2008-2026": ((2008, 1), (2026, 8)),
       "1995-2026": ((1995, 1), (2026, 8))}


def tramo(sim: dict, m0: tuple, m1: tuple) -> list:
    return [f for f in sim["filas"] if m0 <= f["mes"] <= m1]


def reglas_prueba():
    for n in (6, 8, 10, 12):
        for moneda in ("usd", "mxn"):
            for ej in ("T0", "T1"):
                yield f"sma{n}_{moneda}_{ej}", ("sma", n, moneda), ej


def bloque_sma(D: dict) -> dict:
    I = D["CETES"]
    spy = D["SPY"]
    base = preparar(spy["adj"], D["DEX"])
    out = {"variantes": {}, "referencias": {}, "nw": {}, "dsr": {}, "sens": {}, "posthoc": {}}
    sims = {}
    # ---- 16 variantes de prueba y referencias, corrida 1995-01 a 2026-08
    for nombre, regla, ej in reglas_prueba():
        sims[nombre] = simular(base, I, regla, ej, (1995, 1), (2026, 8))
    for ej in ("T0", "T1"):
        sims[f"bh_{ej}"] = simular(base, I, ("bh",), ej, (1995, 1), (2026, 8))
    sims["cetes_T0"] = simular(base, I, ("cetes",), "T0", (1995, 1), (2026, 8))
    for nombre, sim in sims.items():
        out["variantes"][nombre] = {s: metricas(tramo(sim, *r)) for s, r in SEG.items()}
    # ---- prueba principal: SMA10 - comprar y mantener
    for moneda in ("mxn", "usd"):
        for ej in ("T1", "T0"):
            a, b = sims[f"sma10_{moneda}_{ej}"], sims[f"bh_{ej}"]
            for s, r in SEG.items():
                x = [p["rn"] - q["rn"] for p, q in zip(tramo(a, *r), tramo(b, *r))]
                out["nw"][f"sma10_{moneda}_{ej}|{s}"] = prueba_nw(x)
    # ---- DSR con N = 16 (varianza muestral de los SR por periodo de las 16 pruebas)
    for s in ("2008-2026", "1995-2007"):
        pruebas = {k: out["variantes"][k][s] for k, _, _ in reglas_prueba()}
        srs = [v["sr_periodo"] for v in pruebas.values()]
        var = statistics.variance(srs)
        mejor = max(pruebas, key=lambda k: pruebas[k]["sr_periodo"])
        for nombre, N in [("sma10_mxn_T1", 16), ("sma10_mxn_T0", 16), ("sma10_usd_T1", 16),
                          (mejor, 16), ("sma10_mxn_T1", 100)]:
            v = pruebas[nombre]
            sr0 = sr_max_esperado(N, var)
            out["dsr"][f"{s}|{nombre}|N{N}"] = {
                "sharpe_anual": v["sr_periodo"] * math.sqrt(12), "sr0_anual": sr0 * math.sqrt(12),
                "psr": v["psr"], "dsr": psr(v["sr_periodo"], v["n"], v["asimetria"], v["curtosis"], sr0),
                "mejor": nombre == mejor}
        out["dsr"][f"{s}|mejor"] = mejor
        for ej in ("T0", "T1"):
            out["dsr"][f"{s}|psr_bh_{ej}"] = out["variantes"][f"bh_{ej}"][s]["psr"]
    # ---- sensibilidades (2008-2026)
    def corrida(P, regla, ej, costo=COMISION + SPREAD, m0=(1995, 1), efectivo="indice", w0=0.0):
        sim = simular(P, I, regla, ej, m0, (2026, 8), costo_lado=costo, w_inicial=w0, efectivo=efectivo)
        return metricas(tramo(sim, (2008, 1), (2026, 8)) if m0 < (2008, 1) else sim["filas"])

    casos = {
        "base": (base, {}), "sin_costos": (base, {"costo": 0.0}),
        "spread_medio": (base, {"costo": 0.0029 + 0.0015}),
        "doble_pierna": (base, {"costo": 0.0058 + 0.0010}),
        "sp500tr": (preparar(D["SP500TR"]["close"], D["DEX"]), {}),
        "fix": (preparar(spy["adj"], D["FIX"]), {}),
        "mxnx": (preparar(spy["adj"], D["FX_MXNX"]), {"m0": (2005, 1)}),
        "senal_close": (preparar(spy["adj"], D["DEX"], spy["close"]), {}),
        "div_net30": (preparar(serie_tr(spy["close"], spy["div"], 0.7), D["DEX"]), {}),
        "div_net30_senal_adj": (preparar(serie_tr(spy["close"], spy["div"], 0.7), D["DEX"],
                                         {f: spy["adj"][f] for f in spy["adj"]}), {}),
        "cetes_particion": (base, {"efectivo": "particion"}),
        "aislada_2008": (base, {"m0": (2008, 1)}),
        "origen_2008_11": (base, {"m0": (2008, 11)}),
    }
    for caso, (P, kw) in casos.items():
        d = {}
        for etiqueta, regla, ej in [("mxn_T1", ("sma", 10, "mxn"), "T1"), ("usd_T1", ("sma", 10, "usd"), "T1"),
                                    ("bh_T1", ("bh",), "T1"), ("mxn_T0", ("sma", 10, "mxn"), "T0"),
                                    ("bh_T0", ("bh",), "T0")]:
            d[etiqueta] = corrida(P, regla, ej, **kw)
        out["sens"][caso] = d
    # ---- POST-HOC: ventanas que empiezan en 2007 (T0, corrida aislada que entra desde cero)
    for mi in range(1, 13):
        for mf in ((2026, 6), (2026, 8)):
            k = f"2007-{mi:02d}_{mf[0]}-{mf[1]:02d}"
            s = simular(base, I, ("sma", 10, "mxn"), "T0", (2007, mi), mf)
            b = simular(base, I, ("bh",), "T0", (2007, mi), mf)
            out["posthoc"][k] = {"sma": metricas(s["filas"]), "bh": metricas(b["filas"])}
    return out

# ============================================================== comparacion automatica con el README

TOL = {  # tolerancias (unidades del README)
    "media": 0.01,   # %/mes (medias y limites de IC)
    "x12": 0.12,     # pp/anio (media x 12; equivale a 0.01 pp/mes)
    "t": 0.05,
    "pct": 0.1,      # pp: CAGR, caida maxima, cambio %, volatilidad, tiempo invertido, dividendos, FX
    "sharpe": 0.01,  # Sharpe anual y SR0 anual
    "prob": 0.005,   # PSR, DSR
    "corr": 0.01,
    "costo": 0.01,   # pp/anio
    "nivel": 0.01,   # niveles (tipo de cambio, precios)
    "sic": 0.01,     # pp (diferencia de conversion)
    "entero": 0,
}


def _limpiar(s: str) -> str:
    return s.replace("−", "-").replace("**", "").replace("*", "").replace(",", "")


def num_txt(s: str) -> tuple:
    """(valor, decimales) del primer numero de s."""
    m = re.search(r"[-+]?\d+(?:\.\d+)?", _limpiar(s))
    if not m:
        raise ValueError(f"sin numero en {s!r}")
    t = m.group(0)
    return float(t), (len(t.split(".")[1]) if "." in t else 0)


def clave_var(s: str) -> str:
    """'SMA10-MXN-T1' -> 'sma10_mxn_T1'."""
    a, b, c = s.replace("*", "").strip().split("-")
    return f"{a.lower()}_{b.lower()}_{c}"


def nums_txt(s: str) -> list:
    return [(float(t), len(t.split(".")[1]) if "." in t else 0)
            for t in re.findall(r"[-+]?\d+(?:\.\d+)?", _limpiar(s))]


class Comparador:
    def __init__(self, texto: str):
        self.texto = texto
        self.lineas = texto.splitlines()
        self.filas = []

    # ---- registro
    def num(self, bloque, fila, campo, tipo, reportado, propio, dec=None):
        if isinstance(reportado, str):
            rep, d = num_txt(reportado)
        else:
            rep, d = reportado
        dec = d if dec is None else dec
        dif = propio - rep
        # una cifra impresa con menos decimales (p. ej. "-28%") no puede ser mas precisa que su redondeo
        tol = max(TOL[tipo], 0.5 * 10 ** (-dec)) if tipo != "entero" else 0
        ok = abs(dif) <= tol + 1e-9
        fmt = lambda x: f"{x + 0.0:.{dec}f}".replace("-0." + "0" * dec, "0." + "0" * dec) if dec else str(round(x))
        exacto = fmt(propio) == fmt(rep)
        self.filas.append({"bloque": bloque, "fila": fila, "campo": campo, "tipo": tipo,
                           "reportado": rep, "propio": propio, "dif": dif, "tolerancia": tol,
                           "ok": ok, "exacto_al_redondeo": exacto})

    def cat(self, bloque, fila, campo, reportado, propio):
        ok = reportado == propio
        self.filas.append({"bloque": bloque, "fila": fila, "campo": campo, "tipo": "categoria",
                           "reportado": reportado, "propio": propio, "dif": "", "tolerancia": "igual",
                           "ok": ok, "exacto_al_redondeo": ok})

    # ---- lectura
    def tabla(self, marcador: str) -> list:
        i = next(k for k, l in enumerate(self.lineas) if marcador in l)
        j = next(k for k in range(i + 1, len(self.lineas)) if self.lineas[k].startswith("|"))
        filas = []
        while j < len(self.lineas) and self.lineas[j].startswith("|"):
            filas.append([c.strip() for c in self.lineas[j].strip().strip("|").split("|")])
            j += 1
        return filas[2:]

    def buscar(self, patron: str) -> tuple:
        m = re.search(patron, self.texto)
        if not m:
            raise ValueError(f"No se encontro en el README: {patron!r}")
        return m.groups()


def comparar(texto: str, R: dict) -> list:
    C = Comparador(texto)
    B, SV, DV, AM, A4, SMA = R["benchmarks"], R["sens_ventana"], R["dividendos"], R["amortiguador"], R["a4"], R["sma"]
    V, NW, DSR, SE, PH = SMA["variantes"], SMA["nw"], SMA["dsr"], SMA["sens"], SMA["posthoc"]
    P = lambda x: 100 * x

    # ---------- 0. estructura de los datos citada en el pre-registro
    b = "0. Estructura de datos (pre-registro)"
    E_ = R["estructura"]
    g = C.buscar(r"`DEXMXUS` \(FRED\) va de (\d{4}-\d{2}-\d{2}) a (\d{4}-\d{2}-\d{2}). FIX de Banxico \(SF43718\) va de (\d{4}-\d{2}-\d{2}) a (\d{4}-\d{2}-\d{2}). `MXN=X` \(Yahoo\) empieza en (\d{4}-\d{2}-\d{2})")
    C.cat(b, "DEXMXUS", "rango", f"{g[0]} a {g[1]}", " a ".join(E_["DEXMXUS"]))
    C.cat(b, "FIX", "rango", f"{g[2]} a {g[3]}", " a ".join(E_["FIX"]))
    C.cat(b, "MXN=X", "inicio", g[4], E_["MXN=X inicio"])
    g = C.buscar(r"va de 1982 a la subasta del (\d{4}-\d{2}-\d{2}). SPY en Yahoo va de (\d{4}-\d{2}-\d{2}) a (\d{4}-\d{2}-\d{2}), sin barras vacías")
    C.cat(b, "CETES", "ultima subasta", g[0], E_["CETES"][1])
    C.cat(b, "SPY", "rango", f"{g[1]} a {g[2]}", " a ".join(E_["SPY"]))
    # la seccion PRE-REGISTRO del README es copia literal de prerregistro.md (encabezados un nivel abajo)
    ini = C.texto.index("## PRE-REGISTRO")
    fin = C.texto.index("## RESULTADOS (después de correr)")
    copia = C.texto[ini:fin].split("\n")
    k0 = next(i for i, l in enumerate(copia) if l.startswith("> Escrito el 2026-09-25"))
    copia = "\n".join(copia[k0:]).strip().rstrip("-").strip()
    original = (AQUI / "prerregistro.md").read_text().split("\n")
    original = "\n".join(original[2:]).strip()
    original = re.sub(r"(?m)^## ", "### ", original)
    C.cat(b, "PRE-REGISTRO del README", "identico a prerregistro.md (huella 84aabaa6...)", True, copia == original)
    C.buscar(r"el CSV de CETES se exportó desde 1990")
    C.cat(b, "CETES", "primer dato del CSV (nota menor del README)", "1990", E_["CETES"][0][:4])
    g = C.buscar(r"`NAFTRAC.MX` en Yahoo \*\*empieza el (\d{4}-\d{2}-\d{2})\*\*")
    C.cat(b, "NAFTRAC", "inicio", g[0], E_["NAFTRAC inicio"])
    g = C.buscar(r"`SPY.MX` e `IVV.MX` \(cotización del SIC en MXN\) empiezan en (\d{4}-\d{2}-\d{2})")
    C.cat(b, "SPY.MX", "inicio", g[0], E_["SPY.MX inicio"])
    C.cat(b, "IVV.MX", "inicio", g[0], E_["IVV.MX inicio"])
    C.buscar(r"sus dividendos en Yahoo están en \*\*USD hasta 2015 y en MXN desde 2016\*\*")
    for k in ("SPYMX", "IVVMX"):
        C.cat(b, k, "dividendos: todos < 5 antes de 2016 y > 5 desde 2016 (USD luego MXN)", True,
              E_[f"{k} dividendo maximo antes de 2016"] < 5 < E_[f"{k} dividendo minimo desde 2016"])

    # ---------- 1. tabla A1-A3
    claves = ["spy_dex", "spy_fix", "spy_mxnx", "sptr_dex", "spy_net30_dex", "gspc_dex", "spy_usd",
              "naftrac_adj", "naftrac_close", "mxx", "cetes", "eww_adj_dex", "eww_close_dex"]
    filas = C.tabla("### 1. A1-A3")
    assert len(filas) == len(claves), len(filas)
    for fila, k in zip(filas, claves):
        for w, celda in zip(("W1", "W2", "W3", "W4"), fila[1:]):
            C.num("1. CAGR A1-A3", fila[0][:40], w, "pct", celda, P(B["cagr"][f"{k}|{w}"]))
    g = C.buscar(r"Con partición mensual \(tasa de la última subasta ≤ inicio de mes\): ([\d.]+)%")
    C.num("1. CAGR A1-A3", "CETES particion mensual", "W1", "pct", g[0], P(B["cagr"]["cetes_particion|W1"]))
    g = C.buscar(r"INTGSTMXM193N`, tasa/1200, de 2008-01 a 2026-07\): ([\d.]+)%")
    C.num("1. CAGR A1-A3", "FMI tasa/1200", "2008-01 a 2026-07", "pct", g[0], P(B["cagr"]["fmi|2008-01_2026-07"]))

    # ---------- 1b. sensibilidad de inicio
    mapa = {"S&P TR en MXN": "sp_mxn", "NAFTRAC": "naftrac", "CETES 28": "cetes", "S&P TR en USD": "sp_usd"}
    for fila in C.tabla("**Sensibilidad a la fecha de inicio"):
        k = next(v for n, v in mapa.items() if fila[0].startswith(n))
        for col, extremo in ((1, "min"), (2, "max")):
            (val, dec), = nums_txt(fila[col].split("(")[0])
            mes_rep = re.search(r"inicio (\d{4}-\d{2})", fila[col]).group(1)
            mes_p, v_p = SV["inicio"][f"{k}_{extremo}"]
            C.num("1b. Sensibilidad de inicio", fila[0], extremo, "pct", (val, dec), P(v_p))
            C.cat("1b. Sensibilidad de inicio", fila[0], f"mes del {extremo}", mes_rep, mes_p)
        for mes_rep, val in re.findall(r"(\d{4}-\d{2}): \**([\d.]+)%", fila[3]):
            C.num("1b. Sensibilidad de inicio", fila[0], mes_rep, "pct", val, P(SV["inicio"][k][mes_rep]))

    # ---------- 1c. sensibilidad de fin
    mapa = {"S&P TR en MXN": "sp_mxn", "NAFTRAC": "naftrac", "CETES": "cetes"}
    for fila in C.tabla("**Sensibilidad a la fecha de fin**"):
        k = mapa[fila[0]]
        for f, celda in zip(("2025-12-31", "2026-06-30", "2026-08-31", "2026-09-18"), fila[1:]):
            C.num("1c. Sensibilidad de fin", fila[0], f, "pct", celda, P(SV["fin"][f"{k}|{f}"]))

    # ---------- 1d. dividendos de NAFTRAC, EWW y ^MXX
    nd = DV["NAFTRAC"]
    g = C.buscar(r"Vale \*\*(0\.00)% en 2008, 2009, 2010, 2011, 2012 y 2021\*\*")
    for a in ("2008", "2009", "2010", "2011", "2012", "2021"):
        C.num("1d. Dividendos", "NAFTRAC implicito", a, "pct", g[0], P(nd[a]))
        C.cat("1d. Dividendos", "NAFTRAC eventos en Yahoo", a, 0, DV["NAFTRAC_eventos_por_anio"][a])
    otros = {a: v for a, v in nd.items() if a not in ("2008", "2009", "2010", "2011", "2012", "2021")}
    g = C.buscar(r"En los otros años va de ([\d.]+)% a ([\d.]+)%, por ejemplo 2019 = ([\d.]+)%, 2023 = ([\d.]+)% y 2025 = ([\d.]+)%")
    C.num("1d. Dividendos", "NAFTRAC otros anios", "minimo", "pct", g[0], P(min(otros.values())))
    C.num("1d. Dividendos", "NAFTRAC otros anios", "maximo", "pct", g[1], P(max(otros.values())))
    for a, val in zip(("2019", "2023", "2025"), g[2:]):
        C.num("1d. Dividendos", "NAFTRAC implicito", a, "pct", val, P(nd[a]))
    g = C.buscar(r"que en USD fue de ([\d.]+)%, ([\d.]+)%, ([\d.]+)%, ([\d.]+)%, ([\d.]+)% y ([\d.]+)%")
    for a, val in zip(("2008", "2009", "2010", "2011", "2012", "2021"), g):
        C.num("1d. Dividendos", "EWW implicito (USD)", a, "pct", val, P(DV["EWW"][a]))
    g = C.buscar(r"NAFTRAC en W1 pasaría de ([\d.]+)% a \*\*([\d.]+)%\*\*")
    C.num("1d. Dividendos", "NAFTRAC W1", "sin imputar", "pct", g[0], P(B["cagr"]["naftrac_adj|W1"]))
    C.num("1d. Dividendos", "NAFTRAC W1", "con dividendos de EWW imputados", "pct", g[1], P(R["naftrac_imputado"]))
    g = C.buscar(r"Su \"benchmark\" da (−?[\d.]+)%, (−?[\d.]+)%, (−?[\d.]+)% y (−?[\d.]+)%")
    for a, val in zip(("2022", "2023", "2024", "2025"), g):
        C.num("1d. Dividendos", "^MXX precio, anio calendario", a, "pct", val, P(R["mxx_anual"][a]))

    # ---------- 1e. pruebas NW de benchmarks
    mapa = {"S&P MXN − CETES, 2008-01 a 2026-08": "sp_menos_cetes|2008-01_2026-08",
            "S&P MXN − CETES, 1995-01 a 2007-12": "sp_menos_cetes|1995-01_2007-12",
            "S&P MXN − NAFTRAC, 2008-02 a 2026-08": "sp_menos_naftrac|2008-02_2026-08",
            "NAFTRAC − CETES, 2008-02 a 2026-08": "naftrac_menos_cetes|2008-02_2026-08"}
    for fila in C.tabla("**Pruebas Newey-West (6 rezagos) sobre diferencias mensuales en MXN:**"):
        x = R["pruebas_benchmarks"][mapa[fila[0]]]
        b = "1e. NW benchmarks"
        C.num(b, fila[0], "n", "entero", fila[1], x["n"])
        C.num(b, fila[0], "media %/mes", "media", fila[2], P(x["media"]))
        C.num(b, fila[0], "x12", "x12", fila[3], P(x["x12"]))
        C.num(b, fila[0], "t NW(6)", "t", fila[4], x["t"])
        C.num(b, fila[0], "t IID", "t", fila[5], x["t_iid"])
        (lo, dlo), (hi, dhi) = nums_txt(fila[6])
        C.num(b, fila[0], "IC95 inferior", "media", (lo, dlo), P(x["ic95"][0]))
        C.num(b, fila[0], "IC95 superior", "media", (hi, dhi), P(x["ic95"][1]))
        C.cat(b, fila[0], "veredicto", fila[7].replace("*", ""), x["veredicto"])

    # ---------- 1f. amortiguador
    b = "1f. Amortiguador"
    g = C.buscar(r"variación de MXN/USD es \*\*(−[\d.]+)\*\*")
    C.num(b, "W1", "correlacion S&P USD vs MXN/USD", "corr", g[0], AM["corr_usd_fx"])
    g = C.buscar(r"En los (\d+) meses con el S&P en USD por debajo de −5% \(media (−[\d.]+)%\), el peso se depreció en promedio \*\*\+([\d.]+)%\*\*, y el S&P en MXN cayó en promedio (−[\d.]+)%")
    C.num(b, "W1", "meses con S&P USD < -5%", "entero", g[0], AM["n_meses_usd_menor_-5"])
    C.num(b, "W1", "media S&P USD en esos meses", "pct", g[1], P(AM["media_usd_en_malos"]))
    C.num(b, "W1", "media MXN/USD en esos meses", "pct", g[2], P(AM["media_fx_en_malos"]))
    C.num(b, "W1", "media S&P MXN en esos meses", "pct", g[3], P(AM["media_mxn_en_malos"]))
    g = C.buscar(r"La caída máxima mensual en W1 fue (−[\d.]+)% en USD y \*\*(−[\d.]+)% en MXN\*\*. La volatilidad anual fue ([\d.]+)% en USD y ([\d.]+)% en MXN")
    C.num(b, "W1", "MDD mensual USD", "pct", g[0], P(AM["mdd_usd_mensual"]))
    C.num(b, "W1", "MDD mensual MXN", "pct", g[1], P(AM["mdd_mxn_mensual"]))
    C.num(b, "W1", "vol anual USD", "pct", g[2], P(AM["vol_usd"]))
    C.num(b, "W1", "vol anual MXN", "pct", g[3], P(AM["vol_mxn"]))
    g = C.buscar(r"MXN/USD pasó de ([\d.]+) a ([\d.]+), un CAGR de \*\*\+([\d.]+)%\*\*")
    C.num(b, "W1", "MXN/USD inicial", "nivel", g[0], AM["fx_inicio"])
    C.num(b, "W1", "MXN/USD final", "nivel", g[1], AM["fx_fin"])
    C.num(b, "W1", "CAGR MXN/USD", "pct", g[2], P(AM["cagr_fx"]))
    g = C.buscar(r"entre el S&P en MXN \(([\d.]+)%\) y en USD \(([\d.]+)%\), porque ([\d.]+) × ([\d.]+) − 1 = ([\d.]+)%")
    C.num(b, "W1", "S&P MXN", "pct", g[0], P(B["cagr"]["spy_dex|W1"]))
    C.num(b, "W1", "S&P USD", "pct", g[1], P(B["cagr"]["spy_usd|W1"]))
    C.num(b, "W1", "factor 1 + CAGR USD", "nivel", g[2], 1 + B["cagr"]["spy_usd|W1"], dec=4)
    C.num(b, "W1", "factor 1 + CAGR MXN/USD", "nivel", g[3], 1 + AM["cagr_fx"], dec=4)
    C.num(b, "W1", "aritmetica del README con sus factores impresos", "pct", g[4],
          P(float(g[2]) * float(g[3]) - 1))
    g = C.buscar(r"NAFTRAC en W1 tuvo volatilidad de ([\d.]+)% y caída máxima mensual de (−[\d.]+)%")
    C.num(b, "W1", "vol NAFTRAC", "pct", g[0], P(AM["vol_naftrac"]))
    C.num(b, "W1", "MDD mensual NAFTRAC", "pct", g[1], P(AM["mdd_naftrac_mensual"]))

    # ---------- 1g. controles de datos citados en el texto
    b = "1g. Controles de datos"
    g = C.buscar(r"Reconstruir SPY con cierre \+ dividendos brutos da ([\d.]+)% en W1")
    C.num(b, "SPY TR reconstruido x DEXMXUS", "W1", "pct", g[0], P(B["cagr"]["spy_tr_reconstruido_dex|W1"]))
    g = C.buscar(r"En (\d+) meses el cierre de mes usado no fue el último día de SPY")
    C.num(b, "cierres E_m distintos del ultimo dia de SPY", "numero", "entero", g[0], len(R["cierres_distintos"]["todos"]))
    g = C.buscar(r"La mediana de la diferencia absoluta es ([\d.]+)% con DEXMXUS y ([\d.]+)% con FIX, y el percentil 90 es ([\d.]+)%. Con MXN=X la mediana es ([\d.]+)%")
    S = R["sic"]
    C.num(b, "SPY.MX vs SPY x FX (2016-)", "mediana DEXMXUS", "sic", g[0], P(S["dex"]["mediana"]))
    C.num(b, "SPY.MX vs SPY x FX (2016-)", "mediana FIX", "sic", g[1], P(S["fix"]["mediana"]))
    C.num(b, "SPY.MX vs SPY x FX (2016-)", "p90 DEXMXUS", "sic", g[2], P(S["dex"]["p90"]))
    C.num(b, "SPY.MX vs SPY x FX (2016-)", "mediana MXN=X", "sic", g[3], P(S["mxnx"]["mediana"]))
    g = C.buscar(r"por ejemplo, ([\d.]+) el 2008-08-29 y ([\d,.]+) el 2008-09-01, con (\d+) saltos mayores a 30%")
    C.num(b, "SPY.MX adjclose", "2008-08-29", "nivel", g[0], S["spymx_adj_2008-08-29"])
    C.num(b, "SPY.MX adjclose", "2008-09-01", "nivel", g[1], S["spymx_adj_2008-09-01"])
    C.num(b, "SPY.MX adjclose", "saltos > 30%", "entero", g[2], S["spymx_saltos_30|adj"])

    # ---------- 2. A4
    b = "2. A4 (2008)"
    cols = ["spy_usd", "sptr_usd", "gspc_usd", "spy_mxn", "sptr_mxn", "gspc_mxn", "spy_mxn_fix"]
    medidas = ["cambio_2008", "mdd_diaria_2008", "mdd_mensual_2008", "mdd_diaria_crisis", "mdd_mensual_crisis"]
    filas = C.tabla("### 2. A4: 2008, medida por medida")
    assert len(filas) == 5
    for fila, med in zip(filas, medidas):
        for col, celda in zip(cols, fila[1:]):
            x = A4[f"{col}|{med}"]
            C.num(b, med, col, "pct", celda.split("(")[0], P(x[0] if isinstance(x, list) else x))
    for col in cols:
        x = A4[f"{col}|mdd_diaria_2008"]
        C.cat(b, "mdd_diaria_2008 (pico, valle)", col, "2007-12-31 a 2008-11-20", f"{x[1]} a {x[2]}")
        C.cat(b, "mdd_mensual_2008 (mes del valle)", col, "2008-11", A4[f"{col}|mdd_mensual_2008"][2][:7])
    mes_txt = {"ene": "01", "feb": "02", "mar": "03", "abr": "04", "may": "05", "jun": "06", "jul": "07",
               "ago": "08", "sep": "09", "oct": "10", "nov": "11", "dic": "12"}
    for fila, med in ((filas[3], "mdd_diaria_crisis"), (filas[4], "mdd_mensual_crisis")):
        for col, celda in zip(cols, fila[1:]):
            m = re.search(r"\((.+) a (.+)\)", celda)
            if not m:
                continue
            x = A4[f"{col}|{med}"]
            if med == "mdd_diaria_crisis":
                C.cat(b, f"{med} (pico, valle)", col, f"{m.group(1)} a {m.group(2)}", f"{x[1]} a {x[2]}")
            else:
                conv = lambda s: f"{s.split('-')[1]}-{mes_txt[s.split('-')[0]]}"
                C.cat(b, f"{med} (mes pico, mes valle)", col, f"{conv(m.group(1))} a {conv(m.group(2))}",
                      f"{x[1][:7]} a {x[2][:7]}")
    g = C.buscar(r"\^GSPC × FIX (−[\d.]+)%\)")
    C.num(b, "cambio_2008", "gspc_mxn_fix", "pct", g[0], P(A4["gspc_mxn_fix|cambio_2008"]))
    # coincidencias dentro de +-1.0 pp
    usd = [k for k in A4 if "_usd|" in k and abs(abs(P(A4[k][0] if isinstance(A4[k], list) else A4[k])) - 47) <= 1.0]
    mxn = [k for k in A4 if "_mxn" in k and abs(abs(P(A4[k][0] if isinstance(A4[k], list) else A4[k])) - 21.6) <= 1.0]
    C.buscar(r"\*\*47% en USD:\*\* solo la caída diaria dentro de 2008 \(SPY (−[\d.]+)% y \^SP500TR (−[\d.]+)%\)")
    C.cat(b, "coincidencias con 47% (USD), README: 'solo la caida diaria dentro de 2008 (SPY y ^SP500TR)'", "lista",
          sorted(["spy_usd|mdd_diaria_2008", "sptr_usd|mdd_diaria_2008"]), sorted(usd))
    C.buscar(r"\*\*21.6% en MXN:\*\* solo el cambio entre fechas fijas del año calendario \*\*sin dividendos\*\* \(\^GSPC × DEXMXUS (−[\d.]+)%; \^GSPC × FIX (−[\d.]+)%\)")
    C.cat(b, "coincidencias con 21.6% (MXN), README: 'solo el cambio de fechas fijas sin dividendos (^GSPC x DEXMXUS y x FIX)'", "lista",
          sorted(["gspc_mxn|cambio_2008", "gspc_mxn_fix|cambio_2008"]), sorted(mxn))
    g = C.buscar(r"Con dividendos da (−[\d.]+)%\.")
    C.num(b, "cambio_2008 con dividendos (SPY TR MXN)", "texto", "pct", g[0], P(A4["spy_mxn|cambio_2008"]))

    # ---------- 3a. tabla principal 2008-2026 y 3b. 1995-2007
    def clave_regla(fila):
        r, ej = fila[0].replace("*", ""), fila[1].replace("*", "")
        if r.startswith("Comprar"):
            return f"bh_{ej}"
        if r.startswith("100% CETES"):
            return "cetes_T0"
        return f"sma10_{'usd' if 'USD' in r else 'mxn'}_{ej}"

    for marcador, seg, campos in (("**Tabla principal. 2008-2026**", "2008-2026",
                                   ["cagr", "vol", "sharpe", "mdd", "tiempo", "cambios", "costo_anual"]),
                                  ("**1995-2007** (fuera de la ventana", "1995-2007",
                                   ["cagr", "vol", "sharpe", "mdd", "cambios"])):
        b = f"3. SMA tabla {seg}"
        for fila in C.tabla(marcador):
            k = clave_regla(fila)
            x = V[k][seg]
            for campo, celda in zip(campos, fila[2:]):
                if celda.strip("* ") == "—":
                    continue
                if campo == "cambios":
                    C.num(b, k, campo, "entero", celda, x[campo])
                elif campo == "sharpe":
                    C.num(b, k, campo, "sharpe", celda, x[campo])
                elif campo == "costo_anual":
                    C.num(b, k, campo, "costo", celda, P(x[campo]))
                else:
                    C.num(b, k, campo, "pct", celda, P(x[campo]))

    # ---------- 3c. 16 variantes
    b = "3c. 16 variantes"
    for fila in C.tabla("**Las 16 variantes de prueba**"):
        nombre = fila[0].strip("*").strip()
        k = {"comprar y mantener T0": "bh_T0", "comprar y mantener T1": "bh_T1"}.get(nombre, nombre)
        for seg, celda in zip(("1995-2007", "2008-2026", "1995-2026"), fila[1:]):
            partes = [p.strip() for p in celda.split("/")]
            x = V[k][seg]
            C.num(b, k, f"{seg} CAGR", "pct", partes[0], P(x["cagr"]))
            C.num(b, k, f"{seg} MDD", "pct", partes[1], P(x["mdd"]))
            if len(partes) > 2:
                C.num(b, k, f"{seg} Sharpe", "sharpe", partes[2], x["sharpe"])
    # afirmaciones sobre las parejas USD/MXN
    parejas = [(n, ej) for n in (6, 8, 10, 12) for ej in ("T0", "T1")]
    mxn_gana_08 = sum(1 for n, ej in parejas if V[f"sma{n}_mxn_{ej}"]["2008-2026"]["cagr"] > V[f"sma{n}_usd_{ej}"]["2008-2026"]["cagr"])
    usd_gana_95 = [f"sma{n}_{ej}" for n, ej in parejas if V[f"sma{n}_usd_{ej}"]["1995-2007"]["cagr"] > V[f"sma{n}_mxn_{ej}"]["1995-2007"]["cagr"]]
    g = C.buscar(r"En 2008-2026, las (\d) parejas USD/MXN favorecen a la señal en MXN")
    C.num(b, "parejas 2008-2026 que favorecen MXN", "numero", "entero", g[0], mxn_gana_08)
    g = C.buscar(r"En 1995-2007 la señal en USD tuvo más CAGR en (\d) de las 8 parejas")
    C.num(b, "parejas 1995-2007 con mas CAGR en USD", "numero", "entero", g[0], len(usd_gana_95))
    C.cat(b, "parejas 1995-2007 con mas CAGR en USD", "lista",
          "sma10_T0, sma10_T1, sma12_T0, sma12_T1, sma6_T1, sma8_T1", ", ".join(sorted(usd_gana_95)))
    # rangos de caida maxima (Resumen 8)
    for seg, patron in (("2008-2026", r"En 2008-2026 va de (−[\d.]+)% a (−[\d.]+)%, contra (−[\d.]+)% y (−[\d.]+)%"),
                        ("1995-2007", r"En 1995-2007 va de (−[\d.]+)% a (−[\d.]+)%, contra (−[\d.]+)% y (−[\d.]+)%")):
        g = C.buscar(patron)
        mdds = [V[k][seg]["mdd"] for k, _, _ in reglas_prueba()]
        bh = sorted([V["bh_T0"][seg]["mdd"], V["bh_T1"][seg]["mdd"]], reverse=True)
        C.num(b, f"rango MDD 16 variantes {seg}", "menos profunda", "pct", g[0], P(max(mdds)))
        C.num(b, f"rango MDD 16 variantes {seg}", "mas profunda", "pct", g[1], P(min(mdds)))
        C.num(b, f"MDD comprar y mantener {seg}", "menos profunda", "pct", g[2], P(bh[0]))
        C.num(b, f"MDD comprar y mantener {seg}", "mas profunda", "pct", g[3], P(bh[1]))
        C.cat(b, f"las 16 con MDD menor que comprar y mantener ({seg})", "todas", True,
              all(m > max(V["bh_T0"][seg]["mdd"], V["bh_T1"][seg]["mdd"]) for m in mdds))

    # ---------- 3d. prueba principal NW
    b = "3d. NW SMA10 - comprar y mantener"
    for fila in C.tabla("**Prueba principal pre-registrada"):
        k = clave_var(fila[0]) + "|" + fila[1].replace("*", "")
        x = NW[k]
        C.num(b, k, "n", "entero", fila[2], x["n"])
        C.num(b, k, "media %/mes", "media", fila[3], P(x["media"]))
        C.num(b, k, "x12", "x12", fila[4], P(x["x12"]))
        C.num(b, k, "t NW(6)", "t", fila[5], x["t"])
        (lo, dlo), (hi, dhi) = nums_txt(fila[6])
        C.num(b, k, "IC95 inferior", "media", (lo, dlo), P(x["ic95"][0]))
        C.num(b, k, "IC95 superior", "media", (hi, dhi), P(x["ic95"][1]))
        C.cat(b, k, "veredicto", fila[7].replace("*", ""), x["veredicto"])

    # ---------- 3e. DSR
    b = "3e. Sharpe deflactado"
    for fila in C.tabla("**Sharpe deflactado** (`sharpe_deflactado_de_registro`"):
        seg, var = fila[0], fila[1].replace("*", "")
        if var.startswith("Mejor variante"):
            nombre = re.search(r"\((\w+)\)", var).group(1)
            C.cat(b, seg, "mejor variante", nombre, DSR[f"{seg}|mejor"])
            k = f"{seg}|{DSR[f'{seg}|mejor']}|N16"
        else:
            base_ = clave_var(var.split(" ")[0])
            k = f"{seg}|{base_}|N{100 if 'N = 100' in var else 16}"
            if "además es la mejor" in var:
                C.cat(b, seg, "mejor variante", base_, DSR[f"{seg}|mejor"])
        x = DSR[k]
        C.num(b, k, "Sharpe anual", "sharpe", fila[2], x["sharpe_anual"])
        C.num(b, k, "SR0 anual", "sharpe", fila[3], x["sr0_anual"])
        C.num(b, k, "PSR", "prob", fila[4], x["psr"])
        C.num(b, k, "DSR", "prob", fila[5], x["dsr"])
        C.cat(b, k, ">= 0.95", fila[6].replace("*", "") == "sí", x["dsr"] >= 0.95)
    g = C.buscar(r"comprar y mantener tiene PSR de \*\*([\d.]+) \(T0\) y ([\d.]+) \(T1\) en 2008-2026\*\*, y de ([\d.]+) y ([\d.]+) en 1995-2007")
    for val, seg, ej in zip(g, ("2008-2026", "2008-2026", "1995-2007", "1995-2007"), ("T0", "T1", "T0", "T1")):
        C.num(b, f"PSR comprar y mantener {ej}", seg, "prob", val, DSR[f"{seg}|psr_bh_{ej}"])

    # ---------- 3f. sensibilidades
    b = "3f. Sensibilidades SMA10 2008-2026"
    mapa = [("Base", "base"), ("Sin costos", "sin_costos"), ("Spread medio", "spread_medio"),
            ("Doble pierna", "doble_pierna"), ("^SP500TR", "sp500tr"), ("FIX en vez", "fix"),
            ("MXN=X", "mxnx"), ("Señal sobre precio", "senal_close"), ("Dividendos netos", "div_net30"),
            ("CETES con partición", "cetes_particion"), ("Corrida aislada", "aislada_2008"),
            ("Búsqueda de origen", "origen_2008_11")]
    cols = ["mxn_T1", "usd_T1", "bh_T1", "mxn_T0", "bh_T0"]
    for fila in C.tabla("**Sensibilidades de SMA10, 2008-2026**"):
        caso = next(v for n, v in mapa if fila[0].startswith(n))
        for col, celda in zip(cols, fila[1:]):
            if celda.strip() == "—":
                continue
            partes = [p.strip() for p in celda.split("/")]
            x = SE[caso][col]
            C.num(b, caso, f"{col} CAGR", "pct", partes[0], P(x["cagr"]))
            C.num(b, caso, f"{col} MDD", "pct", partes[1], P(x["mdd"]))
    g = C.buscar(r"comprar y mantener \*\*le gana\*\* a la SMA10-MXN: ([\d.]+)% contra ([\d.]+)% en T1")
    C.num(b, "origen_2008_11", "bh_T1 CAGR (texto)", "pct", g[0], P(SE["origen_2008_11"]["bh_T1"]["cagr"]))
    C.num(b, "origen_2008_11", "mxn_T1 CAGR (texto)", "pct", g[1], P(SE["origen_2008_11"]["mxn_T1"]["cagr"]))

    # ---------- 3g. comparacion con las cifras recibidas
    b = "3g. Cifras recibidas de A5"
    fuentes = [lambda: (V["sma10_mxn_T0"]["2008-2026"], V["bh_T0"]["2008-2026"]),
               lambda: (V["sma10_mxn_T1"]["2008-2026"], V["bh_T1"]["2008-2026"]),
               lambda: (SE["aislada_2008"]["mxn_T0"], SE["aislada_2008"]["bh_T0"]),
               lambda: (SE["origen_2008_11"]["mxn_T0"], SE["origen_2008_11"]["bh_T0"]),
               lambda: (PH["2007-01_2026-08"]["sma"], PH["2007-01_2026-08"]["bh"]),
               lambda: (PH["2007-07_2026-08"]["sma"], PH["2007-07_2026-08"]["bh"]),
               lambda: (PH["2007-10_2026-08"]["sma"], PH["2007-10_2026-08"]["bh"]),
               lambda: (PH["2007-01_2026-06"]["sma"], PH["2007-01_2026-06"]["bh"])]
    filas = C.tabla("**Comparación con las cifras recibidas.**")
    assert len(filas) == len(fuentes)
    for fila, fuente in zip(filas, fuentes):
        s, h = fuente()
        etiqueta = fila[0].replace("*", "")
        (sc, dsc), (sm, dsm) = nums_txt(fila[1])
        (hc, dhc), (hm, dhm) = nums_txt(fila[2])
        C.num(b, etiqueta, "SMA10-MXN CAGR", "pct", (sc, dsc), P(s["cagr"]))
        C.num(b, etiqueta, "SMA10-MXN MDD", "pct", (sm, dsm), P(s["mdd"]))
        C.num(b, etiqueta, "B&H CAGR", "pct", (hc, dhc), P(h["cagr"]))
        C.num(b, etiqueta, "B&H MDD", "pct", (hm, dhm), P(h["mdd"]))
        banderas_rep = [x.strip().replace("*", "") == "sí" for x in fila[3].split(",")]
        propias = [abs(P(s["cagr"]) - 14.6) <= 0.30 + 1e-9, abs(P(h["cagr"]) - 13.5) <= 0.30 + 1e-9,
                   abs(P(s["mdd"]) + 12) <= 1.0 + 1e-9, abs(P(h["mdd"]) + 31) <= 1.0 + 1e-9]
        C.cat(b, etiqueta, "dentro de tolerancia (4 banderas)", banderas_rep, propias)
    trimestrales = [f"2007-{m:02d}_{f}" for m in (1, 4, 7, 10) for f in ("2026-06", "2026-08")]
    reproducen = sum(1 for k in trimestrales if abs(P(PH[k]["sma"]["cagr"]) - 14.6) <= 0.30
                     and abs(P(PH[k]["bh"]["cagr"]) - 13.5) <= 0.30 and abs(P(PH[k]["sma"]["mdd"]) + 12) <= 1.0
                     and abs(P(PH[k]["bh"]["mdd"]) + 31) <= 1.0)
    C.buscar(r"El −31% de comprar y mantener es la caída del pico de septiembre de 2007 al valle de febrero de 2009")
    for k in ("2007-01_2026-08", "2007-07_2026-08", "2007-01_2026-06"):
        h = PH[k]["bh"]
        C.cat(b, f"post-hoc {k}: pico y valle del -31% de comprar y mantener", "meses", "2007-09 a 2009-02",
              f"{h['mdd_pico'][:7]} a {h['mdd_valle'][:7]}")
    g = C.buscar(r"En la búsqueda post-hoc, (\d) de las (\d) ventanas que empiezan en 2007 reproducen las cuatro cifras")
    C.num(b, "post-hoc: ventanas que reproducen (inicios ene/abr/jul/oct x fin jun/ago, inferido)", "numero",
          "entero", g[0], reproducen)

    # ---------- 4. cifras citadas en Resumen, calificacion y conclusiones
    b = "4. Texto (Resumen y conclusiones)"
    T = [
        (r"S&P cayó (\d+\.\d)% en dólares y (\d+\.\d)% en pesos", [("enero 2008 USD", "pct", -P(AM["enero_2008_usd"])),
                                                                     ("enero 2008 MXN", "pct", -P(AM["enero_2008_mxn"]))]),
        (r"entre ene-2007 y dic-2009 el CAGR va de \*\*([\d.]+)% a ([\d.]+)%\*\*", [("inicio min", "pct", P(SV["inicio"]["sp_mxn_min"][1])),
                                                                                  ("inicio max", "pct", P(SV["inicio"]["sp_mxn_max"][1]))]),
        (r"el resultado cambia ([\d.]+) pp o menos", [("max |dif| SP500TR/FIX/MXN=X vs SPY x DEX, W1-W4", "pct", R["max_dif_fuentes"])]),
        (r"se reproduce \(([\d.]+)% en W1; ([\d.]+)% si se corta en jun-2026\)", [("NAFTRAC W1", "pct", P(B["cagr"]["naftrac_adj|W1"])),
                                                                                   ("NAFTRAC fin jun-2026", "pct", P(SV["fin"]["naftrac|2026-06-30"]))]),
        (r"rindió probablemente \*\*~([\d.]+)-([\d.]+)%\*\*", [("IPC con dividendos, extremo bajo (EWW x DEX)", "pct", P(B["cagr"]["eww_adj_dex|W1"])),
                                                            ("IPC con dividendos, extremo alto (imputado)", "pct", P(R["naftrac_imputado"]))]),
        (r"da \*\*([\d.]+)%\*\* en W1. Cualquier fecha de inicio entre 2007 y 2009 da entre ([\d.]+)% y ([\d.]+)%",
         [("CETES W1", "pct", P(B["cagr"]["cetes|W1"])), ("CETES inicio min", "pct", P(SV["inicio"]["cetes_min"][1])),
          ("CETES inicio max", "pct", P(SV["inicio"]["cetes_max"][1]))]),
        (r"en USD \(−([\d.]+)%, del 31-dic-2007 al 20-nov-2008\)", [("A4 caida diaria 2008 USD", "pct", -P(A4["spy_usd|mdd_diaria_2008"][0]))]),
        (r"en MXN \*\*sin dividendos\*\* \(−([\d.]+)%\)", [("A4 cambio 2008 ^GSPC MXN", "pct", -P(A4["gspc_mxn|cambio_2008"]))]),
        (r"Año calendario: \*\*−([\d.]+)% en USD contra −([\d.]+)% en MXN\*\*", [("A4 cambio 2008 USD", "pct", -P(A4["spy_usd|cambio_2008"])),
                                                                                 ("A4 cambio 2008 MXN", "pct", -P(A4["spy_mxn|cambio_2008"]))]),
        (r"Caída diaria dentro de 2008: \*\*−([\d.]+)% contra −([\d.]+)%\*\*", [("A4 diaria 2008 USD", "pct", -P(A4["spy_usd|mdd_diaria_2008"][0])),
                                                                                ("A4 diaria 2008 MXN", "pct", -P(A4["spy_mxn|mdd_diaria_2008"][0]))]),
        (r"Caída mensual de la crisis: \*\*−([\d.]+)% contra −([\d.]+)%\*\*", [("A4 mensual crisis USD", "pct", -P(A4["spy_usd|mdd_mensual_crisis"][0])),
                                                                               ("A4 mensual crisis MXN", "pct", -P(A4["spy_mxn|mdd_mensual_crisis"][0]))]),
        (r"da \*\*([\d.]+)% contra ([\d.]+)%\*\* de comprar y mantener, con caída máxima de \*\*−([\d.]+)% contra −([\d.]+)%\*\*",
         [("SMA10-MXN-T0 CAGR", "pct", P(V["sma10_mxn_T0"]["2008-2026"]["cagr"])), ("B&H T0 CAGR", "pct", P(V["bh_T0"]["2008-2026"]["cagr"])),
          ("SMA10-MXN-T0 MDD", "pct", -P(V["sma10_mxn_T0"]["2008-2026"]["mdd"])), ("B&H T0 MDD", "pct", -P(V["bh_T0"]["2008-2026"]["mdd"]))]),
        (r"la principal\) da \*\*([\d.]+)% contra ([\d.]+)%\*\*, con caída de \*\*−([\d.]+)% contra −([\d.]+)%\*\*",
         [("SMA10-MXN-T1 CAGR", "pct", P(V["sma10_mxn_T1"]["2008-2026"]["cagr"])), ("B&H T1 CAGR", "pct", P(V["bh_T1"]["2008-2026"]["cagr"])),
          ("SMA10-MXN-T1 MDD", "pct", -P(V["sma10_mxn_T1"]["2008-2026"]["mdd"])), ("B&H T1 MDD", "pct", -P(V["bh_T1"]["2008-2026"]["mdd"]))]),
        (r"de jul-2007 a ago-2026 da ([\d.]+)% contra ([\d.]+)% y −([\d.]+)% contra −([\d.]+)%",
         [("post-hoc jul-2007 SMA CAGR", "pct", P(PH["2007-07_2026-08"]["sma"]["cagr"])), ("post-hoc jul-2007 B&H CAGR", "pct", P(PH["2007-07_2026-08"]["bh"]["cagr"])),
          ("post-hoc jul-2007 SMA MDD", "pct", -P(PH["2007-07_2026-08"]["sma"]["mdd"])), ("post-hoc jul-2007 B&H MDD", "pct", -P(PH["2007-07_2026-08"]["bh"]["mdd"]))]),
        (r"da \*\*\+([\d.]+) pp al año, con t NW\(6\) = ([\d.]+)\*\*", [("NW SMA10-MXN-T1 2008-2026 x12", "x12", P(NW["sma10_mxn_T1|2008-2026"]["x12"])),
                                                                       ("NW SMA10-MXN-T1 2008-2026 t", "t", NW["sma10_mxn_T1|2008-2026"]["t"])]),
        (r"También es inconcluso en 1995-2007 \(t = ([\d.]+)\) y en 1995-2026 \(t = ([\d.]+)\)",
         [("NW SMA10-MXN-T1 1995-2007 t", "t", NW["sma10_mxn_T1|1995-2007"]["t"]), ("NW SMA10-MXN-T1 1995-2026 t", "t", NW["sma10_mxn_T1|1995-2026"]["t"])]),
        (r"En 1995-2007 la SMA10 con señal en USD rindió ([\d.]+)% y la de MXN ([\d.]+)%, con caídas de −([\d.]+)% y −([\d.]+)% \(T1\)",
         [("SMA10-USD-T1 1995-2007 CAGR", "pct", P(V["sma10_usd_T1"]["1995-2007"]["cagr"])), ("SMA10-MXN-T1 1995-2007 CAGR", "pct", P(V["sma10_mxn_T1"]["1995-2007"]["cagr"])),
          ("SMA10-USD-T1 1995-2007 MDD", "pct", -P(V["sma10_usd_T1"]["1995-2007"]["mdd"])), ("SMA10-MXN-T1 1995-2007 MDD", "pct", -P(V["sma10_mxn_T1"]["1995-2007"]["mdd"]))]),
        (r"\(([\d.]+)% contra ([\d.]+)%\)\.\n8\.", [("SMA10-USD-T1 2008-2026 CAGR", "pct", P(V["sma10_usd_T1"]["2008-2026"]["cagr"])),
                                                     ("B&H T1 2008-2026 CAGR", "pct", P(V["bh_T1"]["2008-2026"]["cagr"]))]),
        (r"SMA10-MXN-T1 da DSR = \*\*([\d.]+)\*\* en 2008-2026 y \*\*([\d.]+)\*\* en 1995-2007", [("DSR 2008-2026", "prob", DSR["2008-2026|sma10_mxn_T1|N16"]["dsr"]),
                                                                                                 ("DSR 1995-2007", "prob", DSR["1995-2007|sma10_mxn_T1|N16"]["dsr"])]),
        (r"Comprar y mantener tiene PSR de ([\d.]+) en el mismo tramo", [("PSR B&H T1 2008-2026", "prob", DSR["2008-2026|psr_bh_T1"])]),
        (r"el diferencial fue de \+([\d.]+) pp al año como media × 12, con t = ([\d.]+)", [("S&P MXN - CETES x12", "x12", P(R["pruebas_benchmarks"]["sp_menos_cetes|2008-01_2026-08"]["x12"])),
                                                                                         ("S&P MXN - CETES t", "t", R["pruebas_benchmarks"]["sp_menos_cetes|2008-01_2026-08"]["t"])]),
        (r"De 1995 a 2007, CETES rindió ([\d.]+)% anual y el S&P en MXN ([\d.]+)%, con t = ([\d.]+)",
         [("CETES 1995-2007", "pct", P(V["cetes_T0"]["1995-2007"]["cagr"])), ("S&P MXN 1995-2007 (B&H T0)", "pct", P(V["bh_T0"]["1995-2007"]["cagr"])),
          ("S&P MXN - CETES 1995-2007 t", "t", R["pruebas_benchmarks"]["sp_menos_cetes|1995-01_2007-12"]["t"])]),
        (r"en el límite de la tolerancia \(\+([\d.]+) pp\)", [("CETES W1 - 6.1", "pct", P(B["cagr"]["cetes|W1"]) - 6.1)]),
        (r"Ninguna definición nuestra baja de ([\d.]+)%", [("CETES minimo (inicio 2007-2009)", "pct", P(SV["inicio"]["cetes_min"][1]))]),
        (r"inconclusa en todos los tramos \(t de ([\d.]+) a ([\d.]+)\)", [("t minima SMA10-MXN", "t", R["t_rango_sma10_mxn"][0]),
                                                                          ("t maxima SMA10-MXN", "t", R["t_rango_sma10_mxn"][1])]),
        (r"correlación de (−[\d.]+) y caída máxima mensual de (−\d+)% en MXN contra (−\d+)% en USD en W1",
         [("correlacion", "corr", AM["corr_usd_fx"]), ("MDD MXN W1", "pct", P(AM["mdd_mxn_mensual"])), ("MDD USD W1", "pct", P(AM["mdd_usd_mensual"]))]),
        (r"Con dividendos netos de 30% de retención baja a \*\*([\d.]+)%\*\*", [("S&P net30 W1", "pct", P(B["cagr"]["spy_net30_dex|W1"]))]),
        (r"con una depreciación del peso de ([\d.]+)% anual", [("CAGR MXN/USD W1", "pct", P(AM["cagr_fx"]))]),
        # seccion 4 (calificacion)
        (r"\| ([\d.]+)% \(W1\); ([\d.]+)% \(W2\) \|", [("sec.4 A1 W1", "pct", P(B["cagr"]["spy_dex|W1"])),
                                                        ("sec.4 A1 W2", "pct", P(B["cagr"]["spy_dex|W2"]))]),
        (r"Rango según el inicio: ([\d.]+)-([\d.]+)%", [("sec.4 A1 inicio min", "pct", P(SV["inicio"]["sp_mxn_min"][1])),
                                                       ("sec.4 A1 inicio max", "pct", P(SV["inicio"]["sp_mxn_max"][1]))]),
        (r"\| ([\d.]+)% \(W1\); ([\d.]+)% con fin en jun-2026 \|", [("sec.4 A2 W1", "pct", P(B["cagr"]["naftrac_adj|W1"])),
                                                                     ("sec.4 A2 fin jun-2026", "pct", P(SV["fin"]["naftrac|2026-06-30"]))]),
        (r"La estimación post-hoc con dividendos es ~([\d.]+)-([\d.]+)%", [("sec.4 A2 extremo bajo", "pct", P(B["cagr"]["eww_adj_dex|W1"])),
                                                                          ("sec.4 A2 extremo alto", "pct", P(R["naftrac_imputado"]))]),
        (r"\| A3: CETES \| [\d.]+% \| ([\d.]+)% \|", [("sec.4 A3 CETES W1", "pct", P(B["cagr"]["cetes|W1"]))]),
        (r"\| (−[\d.]+)% \(caída diaria dentro de 2008, USD\); (−[\d.]+)% \(cambio del año calendario, MXN, precio\)",
         [("sec.4 A4 USD", "pct", P(A4["spy_usd|mdd_diaria_2008"][0])), ("sec.4 A4 MXN precio", "pct", P(A4["gspc_mxn|cambio_2008"]))]),
        (r"Con la misma medida: (−[\d.]+)% contra (−[\d.]+)%, o (−[\d.]+)% contra (−[\d.]+)%",
         [("sec.4 A4 cambio USD", "pct", P(A4["spy_usd|cambio_2008"])), ("sec.4 A4 cambio MXN", "pct", P(A4["spy_mxn|cambio_2008"])),
          ("sec.4 A4 diaria USD", "pct", P(A4["spy_usd|mdd_diaria_2008"][0])), ("sec.4 A4 diaria MXN", "pct", P(A4["spy_mxn|mdd_diaria_2008"][0]))]),
        (r"\| ([\d.]+)-([\d.]+)% / (−[\d.]+) a (−[\d.]+)% contra ([\d.]+)% / (−[\d.]+) a (−[\d.]+)% \|",
         [("sec.4 A5 SMA T0 CAGR", "pct", P(V["sma10_mxn_T0"]["2008-2026"]["cagr"])), ("sec.4 A5 SMA T1 CAGR", "pct", P(V["sma10_mxn_T1"]["2008-2026"]["cagr"])),
          ("sec.4 A5 SMA T0 MDD", "pct", P(V["sma10_mxn_T0"]["2008-2026"]["mdd"])), ("sec.4 A5 SMA T1 MDD", "pct", P(V["sma10_mxn_T1"]["2008-2026"]["mdd"])),
          ("sec.4 A5 B&H CAGR", "pct", P(V["bh_T0"]["2008-2026"]["cagr"])), ("sec.4 A5 B&H T0 MDD", "pct", P(V["bh_T0"]["2008-2026"]["mdd"])),
          ("sec.4 A5 B&H T1 MDD", "pct", P(V["bh_T1"]["2008-2026"]["mdd"]))]),
        (r"La ventaja de rendimiento no es significativa \(t = ([\d.]+)\) y el DSR en 1995-2007 es ([\d.]+)\.",
         [("sec.4 A5 t", "t", NW["sma10_mxn_T1|2008-2026"]["t"]), ("sec.4 A5 DSR 1995-2007", "prob", DSR["1995-2007|sma10_mxn_T1|N16"]["dsr"])]),
        # conclusiones permitidas y seccion 5
        (r"con rendimiento total en MXN rindió \*\*([\d.]+)%\*\* anual antes de impuestos. Si se empieza un mes después, \*\*([\d.]+)%\*\*. El resultado depende mucho de la fecha de inicio: ([\d.]+)-([\d.]+)%",
         [("concl. S&P W1", "pct", P(B["cagr"]["spy_dex|W1"])), ("concl. S&P W2", "pct", P(B["cagr"]["spy_dex|W2"])),
          ("concl. inicio min", "pct", P(SV["inicio"]["sp_mxn_min"][1])), ("concl. inicio max", "pct", P(SV["inicio"]["sp_mxn_max"][1]))]),
        (r"le ganó a CETES con significancia \(t NW = ([\d.]+)\). En 1995-2007 no: CETES rindió ([\d.]+)% y el S&P en MXN ([\d.]+)%",
         [("concl. t S&P-CETES", "t", R["pruebas_benchmarks"]["sp_menos_cetes|2008-01_2026-08"]["t"]),
          ("concl. CETES 1995-2007", "pct", P(V["cetes_T0"]["1995-2007"]["cagr"])), ("concl. S&P MXN 1995-2007", "pct", P(V["bh_T0"]["1995-2007"]["cagr"]))]),
        (r"el contraste correcto para 2008 es \*\*−([\d.]+)% contra −([\d.]+)%\*\* \(año calendario\) o \*\*−([\d.]+)% contra −([\d.]+)%\*\*",
         [("concl. cambio USD", "pct", -P(A4["spy_usd|cambio_2008"])), ("concl. cambio MXN", "pct", -P(A4["spy_mxn|cambio_2008"])),
          ("concl. diaria USD", "pct", -P(A4["spy_usd|mdd_diaria_2008"][0])), ("concl. diaria MXN", "pct", -P(A4["spy_mxn|mdd_diaria_2008"][0]))]),
        (r"NAFTRAC rindió ≥ ([\d.]+)% anual", [("concl. NAFTRAC piso", "pct", P(B["cagr"]["naftrac_adj|W1"]))]),
        (r"Los CETES 28 de Banxico rindieron ([\d.]+)% anual en W1", [("concl. CETES W1", "pct", P(B["cagr"]["cetes|W1"]))]),
        (r"Es ([\d.]+)% desde el cierre de 2007, y ([\d.]+)% solo empezando a fin de enero de 2008",
         [("concl. NO: S&P W1", "pct", P(B["cagr"]["spy_dex|W1"])), ("concl. NO: S&P W2", "pct", P(B["cagr"]["spy_dex|W2"]))]),
        (r"Que un DSR de ([\d.]+) en 2008-2026 valide la regla. Mide el Sharpe contra cero en un tramo en el que comprar y mantener también pasa \(PSR de ([\d.]+)\). En 1995-2007 el DSR es ([\d.]+)\.",
         [("concl. NO: DSR 2008-2026", "prob", DSR["2008-2026|sma10_mxn_T1|N16"]["dsr"]), ("concl. NO: PSR B&H", "prob", DSR["2008-2026|psr_bh_T1"]),
          ("concl. NO: DSR 1995-2007", "prob", DSR["1995-2007|sma10_mxn_T1|N16"]["dsr"])]),
        (r"S&P 500 con rendimiento total vía SPY: \*\*([\d.]+)%\*\* anual", [("sec.5 meta S&P", "pct", P(B["cagr"]["spy_dex|W1"]))]),
        (r"CETES 28: \*\*([\d.]+)%\*\*", [("sec.5 meta CETES", "pct", P(B["cagr"]["cetes|W1"]))]),
        (r"IPC: \*\*al menos ([\d.]+)%\*\*, probablemente ([\d.]+)-([\d.]+)% con dividendos",
         [("sec.5 meta IPC piso", "pct", P(B["cagr"]["naftrac_adj|W1"])), ("sec.5 IPC extremo bajo", "pct", P(B["cagr"]["eww_adj_dex|W1"])),
          ("sec.5 IPC extremo alto", "pct", P(R["naftrac_imputado"]))]),
    ]
    for patron, specs in T:
        g = C.buscar(patron)
        for val, (desc, tipo, propio) in zip(g, specs):
            C.num(b, desc, "texto", tipo, val, propio)
    return C.filas


# ============================================================== main

def a_json(x):
    if isinstance(x, dict):
        return {str(k): a_json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [a_json(v) for v in x]
    if isinstance(x, date):
        return str(x)
    if isinstance(x, float):
        return round(x, 12)
    return x


def main() -> int:
    huellas = revisar_huellas()
    D = cargar()
    R = {"huellas_ok": huellas}
    R["benchmarks"], S = benchmarks(D)
    R["sens_ventana"] = sensibilidades_ventana(D, S)
    R["dividendos"] = dividendos_implicitos(D)
    R["naftrac_imputado"] = naftrac_imputado(D, S, R["dividendos"])
    R["mxx_anual"] = mxx_anual(D)
    R["pruebas_benchmarks"] = pruebas_benchmarks(D, S)
    R["amortiguador"] = amortiguador(D, S)
    R["cierres_distintos"] = meses_cierre_distinto(D, S)["todos"] and meses_cierre_distinto(D, S)
    R["a4"] = a4(D)
    R["sic"] = control_sic(D)
    R["sma"] = bloque_sma(D)
    c = R["benchmarks"]["cagr"]
    R["max_dif_fuentes"] = max(abs(100 * (c[f"{k}|{w}"] - c[f"spy_dex|{w}"]))
                               for k in ("sptr_dex", "spy_fix", "spy_mxnx") for w in W)
    ts = [R["sma"]["nw"][f"sma10_mxn_{ej}|{s}"]["t"] for ej in ("T0", "T1")
          for s in ("2008-2026", "1995-2007", "1995-2026") if not (ej == "T0" and s == "1995-2026")]
    R["t_rango_sma10_mxn"] = [min(ts), max(ts)]
    # tercera comprobacion del error estandar NW con la herramienta del repo
    sys.path.insert(0, str(RAIZ))
    try:
        from herramientas.estadistica import newey_west
    except Exception:  # pragma: no cover
        newey_west = None
    difs = []
    todas = list(R["pruebas_benchmarks"].values()) + list(R["sma"]["nw"].values())
    R["nw_max_dif_formula1_vs_2"] = max(abs(x["se"] - x["se_formula2"]) for x in todas)
    R["nw_n_pruebas"] = len(todas)
    R["nw_max_dif_formula1_vs_herramienta"] = max(abs(x["se"] - x["se_herramienta"]) for x in todas
                                                  if x["se_herramienta"] is not None)
    # robustez: el tramo 2008-2026 de la sensibilidad MXN=X no depende del mes de arranque
    Pm = preparar(D["SPY"]["adj"], D["FX_MXNX"])
    difs = []
    for m0 in ((2004, 12), (2005, 1), (2006, 1)):
        for regla, ej in ((("sma", 10, "mxn"), "T1"), (("sma", 10, "mxn"), "T0"), (("bh",), "T1")):
            sim = simular(Pm, D["CETES"], regla, ej, m0, (2026, 8))
            difs.append(metricas(tramo(sim, (2008, 1), (2026, 8)))["cagr"])
    R["mxnx_arranque_max_dif_cagr_2008_2026"] = max(abs(difs[i] - difs[i % 3]) for i in range(len(difs)))
    R["estructura"] = estructura(D)

    texto = (AQUI / "README.md").read_text()
    corte = texto.find("## Doble ejecución independiente")
    texto_rep = texto if corte < 0 else texto[:corte]
    filas = comparar(texto_rep, R)
    with open(AQUI / "independiente-comparacion.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["bloque", "fila", "campo", "tipo", "reportado", "propio", "dif",
                                           "tolerancia", "ok", "exacto_al_redondeo"])
        w.writeheader()
        for f in filas:
            g = dict(f)
            if isinstance(g["propio"], float):
                g["propio"] = f"{g['propio']:.6f}"
            if isinstance(g["dif"], float):
                g["dif"] = f"{g['dif']:.6f}"
            w.writerow(g)
    resumen = {}
    for f in filas:
        r = resumen.setdefault(f["bloque"], {"cifras": 0, "ok": 0, "exactas": 0, "max_dif": {}})
        r["cifras"] += 1
        r["ok"] += f["ok"]
        r["exactas"] += f["exacto_al_redondeo"]
        if isinstance(f["dif"], float):
            r["max_dif"][f["tipo"]] = max(r["max_dif"].get(f["tipo"], 0.0), abs(f["dif"]))
    R["comparacion"] = {"total": len(filas), "ok": sum(f["ok"] for f in filas),
                        "exactas": sum(f["exacto_al_redondeo"] for f in filas),
                        "numericas": sum(1 for f in filas if f["tipo"] != "categoria"),
                        "categoricas": sum(1 for f in filas if f["tipo"] == "categoria"),
                        "por_bloque": resumen,
                        "fuera_de_tolerancia": [f for f in filas if not f["ok"]],
                        "no_exactas": [f for f in filas if f["ok"] and not f["exacto_al_redondeo"]]}
    (AQUI / "independiente-resultados.json").write_text(json.dumps(a_json(R), ensure_ascii=False, indent=1) + "\n")
    print(f"Cifras comparadas: {len(filas)} | dentro de tolerancia: {R['comparacion']['ok']} | "
          f"identicas al redondeo: {R['comparacion']['exactas']}")
    for bloque, r in resumen.items():
        print(f"  {bloque:40s} {r['cifras']:4d} {r['ok']:4d} {r['exactas']:4d} "
              + ", ".join(f"{k}: {v:.4f}" for k, v in r["max_dif"].items()))
    for f in R["comparacion"]["fuera_de_tolerancia"]:
        print("FUERA:", f)
    for f in R["comparacion"]["no_exactas"]:
        print("NO EXACTA:", f["bloque"], f["fila"], f["campo"], f["reportado"], round(f["propio"], 5))
    print(f"NW: max |se formula 1 - se formula 2| = {R['nw_max_dif_formula1_vs_2']:.1e}; "
          f"formula 1 - herramienta = {R['nw_max_dif_formula1_vs_herramienta']:.1e} ({R['nw_n_pruebas']} pruebas)")
    print(f"MXN=X: max dif de CAGR 2008-2026 al mover el arranque (2004-12, 2005-01, 2006-01) = "
          f"{R['mxnx_arranque_max_dif_cagr_2008_2026']:.1e}")
    print("Estructura:", R["estructura"])
    return 0 if R["comparacion"]["ok"] == len(filas) else 1


if __name__ == "__main__":
    sys.exit(main())
