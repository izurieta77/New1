#!/usr/bin/env python3
"""AC-10: segunda ejecucion independiente (ciega) de R02, momentum de series de tiempo
(TSMOM-12, Moskowitz-Ooi-Pedersen 2012).

Escrito desde el pre-registro de R02 (secciones 1 a 9), sin leer R02.py, R02_verificacion.py,
R02-variantes.csv ni los resultados de la ficha. Biblioteca estandar de Python 3.11.
De herramientas/ solo usa parsear_yahoo_json y parsear_fred_csv (lectores genericos) y, del
codigo de AC-09, el lector OLE2/BIFF8 del xls de Shiller (generico). La senal, la volatilidad
EWMA, la alineacion de fechas, el motor de cartera, los costos y las metricas estan aqui.

Fuentes (distintas de A, que usa French/CRSP mensual y diario y Yahoo adjclose 1mo):
  (a) Mercado de EUA = S&P 500 de rendimiento total:
      - Yahoo ^GSPC diario (period1/period2 explicitos) desde 1927-12-30: precio y volatilidad.
      - Shiller ie_data.xls: dividendo D (anual) -> D/12 por mes, hasta 1996-10.
      - Yahoo ^SP500TR diario, range=30y, desde 1996-11.
      - Rf: FRED TB3MS/1200 desde 1934-01; FRED M1329AUSM193NNBR/1200 antes (NBER).
  (b) 8 ETFs: Yahoo diario range=30y con events=div,split. Rendimiento total construido aqui
      con el cierre (ajustado solo por splits) mas el dividendo en la fecha ex:
      (C_d + Div_d)/C_{d-1} - 1. No se usa adjclose (salvo en un chequeo cruzado impreso).
      Rf: TB3MS/1200.
  MXN: FRED DEXMXUS (ultimo dato <= fin de mes).

Uso: python3 laboratorio/auditorias/AC-10-tsmom/AC10.py   (sin red; lee datos/)
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import statistics
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))
from herramientas.datos import parsear_fred_csv, parsear_yahoo_json  # noqa: E402

AQUI = Path(__file__).resolve().parent
DATOS = AQUI / "datos"
SALIDA: list[str] = []
RES: dict = {}

COMISION = 0.0029
SPREAD_DEF, SPREAD_MEDIO = 0.0005, 0.0015
COSTO_DEF = COMISION + SPREAD_DEF        # 0.34% por lado
COSTO_MEDIO = COMISION + SPREAD_MEDIO    # 0.44% por lado
FIN_PRE = (2026, 7)                      # fin pre-registrado
FIN_EXT = (2026, 8)                      # ultimo mes con TB3MS
DELTA = 60 / 61
MIN_DIAS = 120
TOPE = 10.0
ETFS = ["SPY", "EFA", "EEM", "TLT", "IEF", "GLD", "DBC", "VNQ"]


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    SALIDA.append(s)


# ------------------------------------------------------------ meses
def sig(m):
    return (m[0] + (m[1] == 12), m[1] % 12 + 1)


def ant(m):
    return (m[0] - (m[1] == 1), (m[1] - 2) % 12 + 1)


def rango(a, b):
    out, m = [], a
    while m <= b:
        out.append(m)
        m = sig(m)
    return out


def ftxt(m):
    return f"{m[0]}-{m[1]:02d}"


def retro(m, k):
    for _ in range(k):
        m = ant(m)
    return m


# ------------------------------------------------------------ carga
def cargar_shiller_D():
    spec = importlib.util.spec_from_file_location(
        "ac09", RAIZ / "laboratorio/auditorias/AC-09-sma10-faber/AC09.py")
    ac09 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ac09)
    celdas = ac09.biff_hoja(ac09.ole_flujo((DATOS / "shiller_ie_data.xls").read_bytes(), "Workbook"), "Data")
    D = {}
    for (r, c), v in celdas.items():
        if c != 0 or not (1870 < v < 2100):
            continue
        y = int(v)
        mo = int(round((v - y) * 100))
        if 1 <= mo <= 12 and (r, 2) in celdas and celdas[(r, 2)] > 0:
            D[(y, mo)] = celdas[(r, 2)]
    return D


def yahoo_cierres(nombre):
    """[(fecha, cierre)] diario de un indice (adjclose = close)."""
    return parsear_yahoo_json((DATOS / nombre).read_text())["serie"]


def yahoo_tr_etf(nombre):
    """Indice de rendimiento total diario propio: cierre + dividendo ex. Devuelve
    ([(fecha, indice)], [(fecha, adjclose)], n_dividendos)."""
    j = json.loads((DATOS / nombre).read_text())["chart"]["result"][0]
    off = int(j["meta"].get("gmtoffset", 0))
    tz = timezone(timedelta(seconds=off))
    q = j["indicators"]["quote"][0]["close"]
    adj = j["indicators"]["adjclose"][0]["adjclose"]
    dias = {}
    for i, ts in enumerate(j["timestamp"]):
        if q[i] is None:
            continue
        d = datetime.fromtimestamp(ts, tz).date()
        dias[d] = (q[i], adj[i])
    divs = {}
    for k, v in (j.get("events", {}).get("dividends", {}) or {}).items():
        d = datetime.fromtimestamp(int(k), tz).date()
        divs[d] = divs.get(d, 0.0) + v["amount"]
    fechas = sorted(dias)
    hoy = max(fechas)
    fechas = [d for d in fechas if d < hoy]          # la ultima barra es intradia
    idx, ser, sadj = 1.0, [], []
    for i, d in enumerate(fechas):
        if i > 0:
            c0 = dias[fechas[i - 1]][0]
            idx *= (dias[d][0] + divs.get(d, 0.0)) / c0
        ser.append((d, idx))
        sadj.append((d, dias[d][1]))
    huerfanos = [d for d in divs if d not in dias]
    return ser, sadj, len(divs), huerfanos


def fin_de_mes(serie):
    out = {}
    for d, v in serie:
        out[(d.year, d.month)] = (d, v)
    return out


def rend_mensual(serie, hasta):
    fm = fin_de_mes(serie)
    ms = sorted(fm)
    return {m: fm[m][1] / fm[ant(m)][1] - 1 for m in ms[1:] if ant(m) in fm and m <= hasta}


def fred(nombre):
    return parsear_fred_csv((DATOS / nombre).read_text())


# ------------------------------------------------------------ volatilidad EWMA
def ewma_vol(serie):
    """serie [(fecha, nivel)] diaria -> {fecha: sigma anual} con >= MIN_DIAS rendimientos.
    sigma^2 = 261 * (E[r^2] - E[r]^2), E[.] media exponencial normalizada por 1 - delta^n."""
    m1 = m2 = 0.0
    n = 0
    out = {}
    for i in range(1, len(serie)):
        r = serie[i][1] / serie[i - 1][1] - 1
        m1 = DELTA * m1 + (1 - DELTA) * r
        m2 = DELTA * m2 + (1 - DELTA) * r * r
        n += 1
        if n >= MIN_DIAS:
            w = 1 - DELTA ** n
            var = m2 / w - (m1 / w) ** 2
            out[serie[i][0]] = math.sqrt(max(var, 0.0) * 261)
    return out


def sigma_fin_mes(vol: dict):
    """{mes: sigma del ultimo dia habil <= fin de ese mes}."""
    out = {}
    for d in sorted(vol):
        out[(d.year, d.month)] = vol[d]
    return out


# ------------------------------------------------------------ senales
def senal_ts(r: dict, rf: dict, m, L):
    """+1 si prod(1+r) > prod(1+rf) en los L meses previos a m (t-L..t-1); si no, -1."""
    a = b = 1.0
    for k in range(1, L + 1):
        mm = retro(m, k)
        a *= 1 + r[mm]
        b *= 1 + rf[mm]
    return 1 if a > b else -1


def senal_sma10(r: dict, m):
    """1 si el indice TR en t-1 > media de t-10..t-1 (indice reconstruido localmente)."""
    lv, v = [1.0], 1.0
    for k in range(10, 0, -1):            # niveles t-10..t-1 relativos a t-11
        v *= 1 + r[retro(m, k)]
        lv.append(v)
    niveles = lv[1:]
    return 1 if niveles[-1] > statistics.fmean(niveles) else 0


# ------------------------------------------------------------ motor de cartera
def cartera(R: dict, rf: dict, W: dict, meses, costo, mantener=False):
    """R {activo: {mes: r}}, W {mes: {activo: peso}}. Pesos con deriva entre meses;
    costo = sum|W - W_pre| * costo; r_neto = r_b - costo*(1 + r_b). Inicio en efectivo.
    mantener=True: solo el primer mes usa W; despues se deja la deriva (sin rebalanceo)."""
    pre = {}
    out, ordenes, giro = {}, [], {}
    for i, m in enumerate(meses):
        w = dict(pre) if (mantener and i > 0) else W[m]
        activos = set(w) | set(pre)
        dif = {a: w.get(a, 0.0) - pre.get(a, 0.0) for a in activos}
        t = sum(abs(x) for x in dif.values())
        ordenes.append(sum(1 for x in dif.values() if abs(x) > 1e-9))
        rb = sum(w[a] * R[a][m] for a in w) + (1 - sum(w.values())) * rf[m]
        out[m] = rb - costo * t * (1 + rb)
        giro[m] = t
        pre = {a: w[a] * (1 + R[a][m]) / (1 + rb) for a in w}
    return out, ordenes, giro


# ------------------------------------------------------------ metricas
def metricas(serie: dict, rf: dict, a, b):
    ms = [m for m in rango(a, b) if m in serie]
    x = [serie[m] for m in ms]
    ex = [serie[m] - rf[m] for m in ms]
    n = len(x)
    v, pico, mdd = 1.0, 1.0, 0.0
    for q in x:
        v *= 1 + q
        pico = max(pico, v)
        mdd = min(mdd, v / pico - 1)
    sde = statistics.stdev(ex)
    dd = math.sqrt(sum(min(e, 0.0) ** 2 for e in ex) / n)
    mu, se, t = nw_t(ex)
    return {"desde": ftxt(ms[0]), "hasta": ftxt(ms[-1]), "n": n,
            "cagr": v ** (12 / n) - 1, "vol": statistics.stdev(x) * math.sqrt(12),
            "sharpe": statistics.fmean(ex) / sde * math.sqrt(12) if sde > 0 else 0.0,
            "sortino": statistics.fmean(ex) * 12 / (dd * math.sqrt(12)) if dd > 0 else 0.0,
            "mdd": mdd, "t_nw6": t, "exceso_mensual": mu}


def nw_t(x, L=6):
    n = len(x)
    mu = statistics.fmean(x)
    e = [q - mu for q in x]
    s = sum(q * q for q in e) / n
    for l in range(1, L + 1):
        g = sum(e[i] * e[i - l] for i in range(l, n)) / n
        s += 2 * (1 - l / (L + 1)) * g
    se = math.sqrt(s / n)
    return mu, se, (mu / se if se > 0 else 0.0)


def fmt(d):
    return (f"CAGR {d['cagr']*100:6.2f}% | vol {d['vol']*100:6.2f}% | Sharpe {d['sharpe']:6.3f} | "
            f"t NW6 {d['t_nw6']:5.2f} | Sortino {d['sortino']:6.3f} | MDD {d['mdd']*100:7.2f}% | "
            f"n {d['n']} ({d['desde']} a {d['hasta']})")


def ncdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def nppf(q):
    lo, hi = -12.0, 12.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if ncdf(mid) < q else (lo, mid)
    return (lo + hi) / 2


def dsr(ex, sr_ensayos, N):
    T = len(ex)
    mu, sd = statistics.fmean(ex), statistics.pstdev(ex)
    sr = mu / sd
    sk = sum(((q - mu) / sd) ** 3 for q in ex) / T
    ku = sum(((q - mu) / sd) ** 4 for q in ex) / T
    V = statistics.variance(sr_ensayos)
    g = 0.5772156649
    sr0 = math.sqrt(V) * ((1 - g) * nppf(1 - 1 / N) + g * nppf(1 - 1 / (N * math.e)))
    den = math.sqrt(max(1 - sk * sr + (ku - 1) / 4 * sr * sr, 1e-12))
    return {"sr_mensual": sr, "sr0": sr0, "N": N, "dsr": ncdf((sr - sr0) * math.sqrt(T - 1) / den)}


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ------------------------------------------------------------ principal
def main():
    sums = []
    for f in sorted(DATOS.iterdir()):
        if f.name in ("SHA256SUMS.txt",):
            continue
        sums.append(f"{sha(f)}  {f.name}")
    (DATOS / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n")
    p("AC-10, ejecucion B de R02 (TSMOM). Huellas de datos:")
    for s in sums:
        p("  " + s)
    RES["sha256"] = {s.split("  ")[1]: s.split("  ")[0] for s in sums}

    # ---------------- rf
    rf = {}
    for d, v in fred("fred_M1329AUSM193NNBR.csv"):
        if d < date(1934, 1, 1):
            rf[(d.year, d.month)] = v / 1200
    for d, v in fred("fred_TB3MS.csv"):
        rf[(d.year, d.month)] = v / 1200

    # ---------------- (a) S&P 500 TR
    gspc = yahoo_cierres("yahoo_GSPC_1d.json")
    gspc = [x for x in gspc if x[0] < date(2026, 10, 1)]
    sptr = yahoo_cierres("yahoo_SP500TR_1d_30y.json")
    sptr = [x for x in sptr if x[0] < date(2026, 10, 1)]
    D = cargar_shiller_D()
    fm_g = fin_de_mes(gspc)
    r_px = rend_mensual(gspc, FIN_EXT)
    r_tr = rend_mensual(sptr, FIN_EXT)
    corte_tr = min(r_tr)                                     # primer mes completo ^SP500TR
    rA = {}
    for m in sorted(r_px):
        if m >= corte_tr:
            rA[m] = r_tr[m]
        else:
            rA[m] = r_px[m] + (D[m] / 12) / fm_g[ant(m)][1]
    p(f"\n(a) r_mercado: ^GSPC + D/12 de Shiller de {ftxt(min(rA))} a {ftxt(ant(corte_tr))}; "
      f"^SP500TR (range=30y) de {ftxt(corte_tr)} a {ftxt(max(rA))}")
    tras = [m for m in r_tr if m <= (2026, 6)]
    cg = math.prod(1 + r_px[m] + (D[m] / 12) / fm_g[ant(m)][1] for m in tras) ** (12 / len(tras)) - 1
    ct = math.prod(1 + r_tr[m] for m in tras) ** (12 / len(tras)) - 1
    p(f"    traslape {ftxt(tras[0])} a {ftxt(tras[-1])}: ^GSPC+Shiller D {cg*100:.2f}%/a contra ^SP500TR {ct*100:.2f}%/a")
    sigA = sigma_fin_mes(ewma_vol(gspc))                   # volatilidad de precio ^GSPC

    def pesos_A(nombre, m):
        sg = sigA[ant(m)]
        if nombre.startswith("A_ls_vt40_L"):
            L = int(nombre.split("L")[-1])
            return senal_ts(rA, rf, m, L) * min(0.40 / sg, TOPE)
        if nombre.startswith("A_lo_L"):
            L = int(nombre.split("L")[-1])
            return 1.0 if senal_ts(rA, rf, m, L) == 1 else 0.0
        if nombre == "A_ref_comprar_mantener":
            return 1.0
        if nombre == "A_ref_efectivo":
            return 0.0
        if nombre == "A_ref_sma10":
            return float(senal_sma10(rA, m))
        if nombre == "A_ref_largo_vt40":
            return min(0.40 / sg, TOPE)
        raise KeyError(nombre)

    m0 = min(rA)
    for _ in range(12):
        m0 = sig(m0)
    ini_A = m0                                             # primer mes con 12 meses previos
    mesesA = rango(ini_A, FIN_EXT)
    nombresA = ["A_ls_vt40_L3", "A_ls_vt40_L6", "A_ls_vt40_L12", "A_lo_L3", "A_lo_L6", "A_lo_L12",
                "A_ref_comprar_mantener", "A_ref_efectivo", "A_ref_sma10", "A_ref_largo_vt40"]
    RA = {"mkt": rA}
    corridasA, pesosA = {}, {}
    for c_nom, c in (("def", COSTO_DEF), ("medio", COSTO_MEDIO), ("bruto", 0.0)):
        for nm in nombresA:
            W = {m: {"mkt": pesos_A(nm, m)} for m in mesesA}
            pesosA[nm] = {m: W[m]["mkt"] for m in mesesA}
            corridasA[(nm, c_nom)] = cartera(RA, rf, W, mesesA, c)
    tope_meses = sum(1 for m in mesesA if 0.40 / sigA[ant(m)] >= TOPE)
    p(f"    primer mes evaluado (a): {ftxt(ini_A)} (A: 1927-07); meses con tope |w|=10: {tope_meses}")
    p(f"    peso medio |w| A_ls_vt40_L12: {statistics.fmean(abs(pesosA['A_ls_vt40_L12'][m]) for m in mesesA):.3f}; "
      f"max {max(abs(pesosA['A_ls_vt40_L12'][m]) for m in mesesA):.2f}")

    segA = {"total": (ini_A, FIN_PRE), "dentro": (ini_A, (2011, 12)), "pre1985": (ini_A, (1984, 12)),
            "articulo": ((1985, 1), (2009, 12)), "fuera": ((2012, 1), FIN_PRE), "fuera_ext": ((2012, 1), FIN_EXT)}
    RES["a"] = {}
    for c_nom in ("def", "bruto", "medio"):
        p(f"\n=== (a) S&P 500 TR, costos {c_nom} ===")
        for sn, (a, b) in segA.items():
            p(f"-- {sn} {ftxt(a)} a {ftxt(b)}")
            for nm in nombresA:
                if nm == "A_ref_efectivo" and sn != "total":
                    continue
                d = metricas(corridasA[(nm, c_nom)][0], rf, a, b)
                RES["a"].setdefault(c_nom, {}).setdefault(sn, {})[nm] = d
                p(f"   {nm:24s} {fmt(d)}")
    # decadas, regla del articulo y solo-largos L12, costos por defecto
    p("\n-- (a) por decadas, costos por defecto (Sharpe ls_vt40_L12 / lo_L12 / comprar y mantener)")
    for dec in range(1920, 2030, 10):
        a, b = max((dec, 1), ini_A), min((dec + 9, 12), FIN_PRE)
        if a > b:
            continue
        fila = [metricas(corridasA[(nm, "def")][0], rf, a, b)["sharpe"]
                for nm in ("A_ls_vt40_L12", "A_lo_L12", "A_ref_comprar_mantener")]
        RES["a"].setdefault("decadas", {})[f"{dec}s"] = fila
        p(f"   {dec}s {ftxt(a)}-{ftxt(b)}: {fila[0]:6.3f} / {fila[1]:6.3f} / {fila[2]:6.3f}")
    # descomposicion de timing (solo largos)
    p("\n-- (a) descomposicion solo-largos (exceso mensual, sin costos): E[w]*E[x] + cov(w,x)")
    for nm in ("A_lo_L3", "A_lo_L6", "A_lo_L12", "A_ref_sma10"):
        for sn in ("dentro", "fuera"):
            a, b = segA[sn]
            ms = rango(a, b)
            w = [pesosA[nm][m] for m in ms]
            x = [rA[m] - rf[m] for m in ms]
            ew, exx = statistics.fmean(w), statistics.fmean(x)
            cov = statistics.fmean([(wi - ew) * (xi - exx) for wi, xi in zip(w, x)])
            p(f"   {nm:12s} {sn:6s}: E[w] {ew:.3f} x E[x] {exx*100:.3f}% = {ew*exx*100:.3f}% ; cov {cov*100:+.3f}%/mes")

    # ---------------- (b) ETFs
    p("\n=== (b) 8 ETFs, rendimiento total propio (cierre + dividendo ex) ===")
    RB, sigB, chequeo = {}, {}, {}
    for t in ETFS:
        ser, sadj, nd, huer = yahoo_tr_etf(f"yahoo_{t}_1d_30y_div.json")
        RB[t] = rend_mensual(ser, FIN_EXT)
        sigB[t] = sigma_fin_mes(ewma_vol(ser))
        radj = rend_mensual(sadj, FIN_EXT)
        com = [m for m in RB[t] if m in radj]
        dmax = max(abs(RB[t][m] - radj[m]) for m in com)
        tr_p = math.prod(1 + RB[t][m] for m in com) ** (12 / len(com)) - 1
        tr_a = math.prod(1 + radj[m] for m in com) ** (12 / len(com)) - 1
        chequeo[t] = {"desde": ftxt(min(RB[t])), "dividendos": nd, "div_sin_barra": len(huer),
                      "dif_max_mensual_vs_adjclose": dmax, "cagr_propio": tr_p, "cagr_adjclose": tr_a}
        p(f"   {t}: desde {ftxt(min(RB[t]))}, {nd} dividendos ({len(huer)} sin barra), "
          f"dif. max mensual contra adjclose {dmax*100:.3f} pp; CAGR propio {tr_p*100:.2f}% vs adjclose {tr_a*100:.2f}%")
    RES["b_chequeo_adjclose"] = chequeo
    ini_com = max(min(RB[t]) for t in ETFS)
    m0 = ini_com
    for _ in range(12):
        m0 = sig(m0)
    ini_B = m0
    mesesB = rango(ini_B, FIN_EXT)
    p(f"   muestra comun desde {ftxt(ini_com)}; primer mes evaluado {ftxt(ini_B)}")
    N = len(ETFS)
    falta_sig = [(t, ftxt(m)) for t in ETFS for m in mesesB if ant(m) not in sigB[t]]
    p(f"   meses sin sigma (>=120 dias): {falta_sig}")

    def pesos_B(nombre, m):
        w = {}
        for t in ETFS:
            sg = sigB[t][ant(m)]
            if nombre.startswith("B_ls_vt40_L"):
                s = senal_ts(RB[t], rf, m, int(nombre.split("L")[-1]))
                w[t] = s * min(0.40 / sg, TOPE) / N
            elif nombre.startswith("B_lo_vt10_L"):
                s = senal_ts(RB[t], rf, m, int(nombre.split("L")[-1]))
                w[t] = (1.0 if s == 1 else 0.0) * min(1.0, 0.10 / sg) / N
            elif nombre.startswith("B_lo_L"):
                s = senal_ts(RB[t], rf, m, int(nombre.split("L")[-1]))
                w[t] = (1.0 if s == 1 else 0.0) / N
            elif nombre in ("B_ref_1N", "B_ref_1N_sin_rebalanceo"):
                w[t] = 1 / N
            elif nombre == "B_ref_efectivo":
                w[t] = 0.0
            elif nombre == "B_ref_1N_sma10":
                w[t] = senal_sma10(RB[t], m) / N
            elif nombre == "B_ref_1N_vt10":
                w[t] = min(1.0, 0.10 / sg) / N
            elif nombre == "B_ref_largo_vt40":
                w[t] = min(0.40 / sg, TOPE) / N
            else:
                raise KeyError(nombre)
        return w

    nombresB = ["B_ls_vt40_L3", "B_ls_vt40_L6", "B_ls_vt40_L12", "B_lo_vt10_L3", "B_lo_vt10_L6",
                "B_lo_vt10_L12", "B_lo_L3", "B_lo_L6", "B_lo_L12", "B_ref_1N", "B_ref_1N_sin_rebalanceo",
                "B_ref_efectivo", "B_ref_1N_sma10", "B_ref_1N_vt10", "B_ref_largo_vt40"]
    corridasB, pesosB = {}, {}
    for c_nom, c in (("def", COSTO_DEF), ("medio", COSTO_MEDIO), ("bruto", 0.0)):
        for nm in nombresB:
            W = {m: pesos_B(nm, m) for m in mesesB}
            pesosB[nm] = W
            corridasB[(nm, c_nom)] = cartera(RB, rf, W, mesesB, c, mantener=(nm == "B_ref_1N_sin_rebalanceo"))
    segB = {"total": (ini_B, FIN_PRE), "dentro": (ini_B, (2011, 12)), "fuera": ((2012, 1), FIN_PRE),
            "fuera_1": ((2012, 1), (2019, 12)), "fuera_2": ((2020, 1), FIN_PRE), "fuera_ext": ((2012, 1), FIN_EXT)}
    RES["b"] = {}
    for c_nom in ("def", "bruto", "medio"):
        p(f"\n=== (b) 8 ETFs, costos {c_nom} ===")
        for sn, (a, b) in segB.items():
            p(f"-- {sn} {ftxt(a)} a {ftxt(b)}")
            for nm in nombresB:
                if nm == "B_ref_efectivo" and sn != "total":
                    continue
                d = metricas(corridasB[(nm, c_nom)][0], rf, a, b)
                RES["b"].setdefault(c_nom, {}).setdefault(sn, {})[nm] = d
                p(f"   {nm:24s} {fmt(d)}")
    p("\n-- (b) ordenes por mes (activos con |dW|>0) y apalancamiento bruto medio, fuera de muestra, costos def")
    fu = rango(*segB["fuera"])
    for nm in nombresB:
        _, ords, giro = corridasB[(nm, "def")]
        o = statistics.fmean(ords[mesesB.index(m)] for m in fu)
        g = statistics.fmean(giro[m] for m in fu) * 12
        br = statistics.fmean(sum(abs(x) for x in pesosB[nm][m].values()) for m in fu)
        p(f"   {nm:24s} ordenes/mes {o:4.2f} | giro anual {g:5.2f} | |W| bruto medio {br:5.2f}")

    # ---------------- H4: diferencias contra 1/N y 1/N-SMA10 (t NW6)
    p("\n-- H4, fuera de muestra 2012-01 a 2026-07, costos por defecto: diferencia mensual (t NW6)")
    a, b = segB["fuera"]
    ms = rango(a, b)
    RES["h4"] = {}
    for nm in ("B_lo_vt10_L12", "B_lo_L12", "B_lo_vt10_L3", "B_lo_vt10_L6"):
        for ref in ("B_ref_1N", "B_ref_1N_sma10", "B_ref_1N_vt10"):
            x = [corridasB[(nm, "def")][0][m] - corridasB[(ref, "def")][0][m] for m in ms]
            mu, se, t = nw_t(x)
            RES["h4"][f"{nm}-{ref}"] = {"dif_mensual": mu, "t_nw6": t}
            p(f"   {nm} - {ref}: {mu*100:+.3f}%/mes, t {t:+.2f}")

    # ---------------- DSR, fuera de muestra, N = 15 (los 15 es_prueba)
    p("\n-- DSR fuera de muestra (2012-01 a 2026-07, costos def), V[SR] de los 15 ensayos, N = 15")
    pruebas = nombresA[:6] + nombresB[:9]
    srs = []
    for nm in pruebas:
        ser = corridasA[(nm, "def")][0] if nm.startswith("A_") else corridasB[(nm, "def")][0]
        ex = [ser[m] - rf[m] for m in ms]
        srs.append(statistics.fmean(ex) / statistics.pstdev(ex))
    RES["dsr"] = {}
    for nm in ("A_ls_vt40_L12", "B_ls_vt40_L12", "B_lo_vt10_L12"):
        ser = corridasA[(nm, "def")][0] if nm.startswith("A_") else corridasB[(nm, "def")][0]
        ex = [ser[m] - rf[m] for m in ms]
        d = dsr(ex, srs, 15)
        RES["dsr"][nm] = d
        p(f"   {nm}: SR mensual {d['sr_mensual']:.4f}, SR0 {d['sr0']:.4f}, DSR {d['dsr']:.3f}")
    # DSR dentro de muestra (a), V de los 6 ensayos de (a)
    a2, b2 = segA["dentro"]
    ms2 = rango(a2, b2)
    srs2 = []
    for nm in nombresA[:6]:
        ex = [corridasA[(nm, "def")][0][m] - rf[m] for m in ms2]
        srs2.append(statistics.fmean(ex) / statistics.pstdev(ex))
    ex = [corridasA[("A_ls_vt40_L12", "def")][0][m] - rf[m] for m in ms2]
    d = dsr(ex, srs2, 15)
    RES["dsr"]["A_ls_vt40_L12_dentro"] = d
    p(f"   A_ls_vt40_L12 dentro (V de 6 ensayos de (a), N = 15): DSR {d['dsr']:.3f}")

    # ---------------- MXN
    p("\n-- MXN (DEXMXUS ultimo dato <= fin de mes), fuera de muestra 2012-01 a 2026-07, costos def")
    fx = {}
    for d0, v in fred("fred_DEXMXUS.csv"):
        fx[(d0.year, d0.month)] = v
    RES["mxn"] = {}
    for nm in ("B_ls_vt40_L12", "B_lo_vt10_L12", "B_lo_L12", "B_ref_1N", "B_ref_1N_sma10", "B_ref_1N_vt10"):
        ser = corridasB[(nm, "def")][0]
        sm = {m: (1 + ser[m]) * fx[m] / fx[ant(m)] - 1 for m in ms}
        rfm = {m: (1 + rf[m]) * fx[m] / fx[ant(m)] - 1 for m in ms}
        d = metricas(sm, rfm, a, b)
        RES["mxn"][nm] = d
        p(f"   {nm:24s} CAGR {d['cagr']*100:6.2f}% | vol {d['vol']*100:5.2f}% | MDD {d['mdd']*100:7.2f}%")

    # ---------------- criterios pre-registrados
    p("\n=== Criterios de la seccion 2 (B) ===")
    h1b = RES["a"]["bruto"]["articulo"]["A_ls_vt40_L12"]
    h1 = RES["a"]["def"]["dentro"]["A_ls_vt40_L12"]
    h2 = RES["a"]["def"]["fuera"]["A_ls_vt40_L12"]
    h3 = RES["b"]["def"]["fuera"]["B_ls_vt40_L12"]
    i_ok = h1b["sharpe"] > 0
    ii_ok = h1["sharpe"] > 0 and h1["t_nw6"] >= 2
    iii_ok = h3["sharpe"] > 0 and h3["t_nw6"] >= 2
    if i_ok and ii_ok and iii_ok:
        estado = "Replicado"
    elif not i_ok or (h1["sharpe"] <= 0 and h3["sharpe"] <= 0):
        estado = "No replicado"
    else:
        estado = "Replicado con diferencias"
    p(f"   (i)  H1b bruto 1985-2009: Sharpe {h1b['sharpe']:.3f} -> {'cumple' if i_ok else 'falla'}")
    p(f"   (ii) H1 neto {h1['desde']} a 2011-12: Sharpe {h1['sharpe']:.3f}, t {h1['t_nw6']:.2f} -> {'cumple' if ii_ok else 'no cumple'}")
    p(f"   H2 neto 2012-01 a 2026-07: Sharpe {h2['sharpe']:.3f}, t {h2['t_nw6']:.2f}")
    p(f"   (iii) H3 neto 2012-01 a 2026-07: Sharpe {h3['sharpe']:.3f}, t {h3['t_nw6']:.2f} -> {'cumple' if iii_ok else 'no cumple'}")
    p(f"   Estado B: {estado}")
    lo = RES["b"]["def"]["fuera"]["B_lo_vt10_L12"]
    n1 = RES["b"]["def"]["fuera"]["B_ref_1N"]
    ns = RES["b"]["def"]["fuera"]["B_ref_1N_sma10"]
    vt = RES["b"]["def"]["fuera"]["B_ref_1N_vt10"]
    vs1 = lo["sharpe"] > n1["sharpe"] and lo["mdd"] > n1["mdd"]
    vss = lo["sharpe"] > ns["sharpe"] and lo["mdd"] > ns["mdd"]
    p(f"   H4 B_lo_vt10_L12: Sharpe {lo['sharpe']:.3f} MDD {lo['mdd']*100:.2f}% | 1/N {n1['sharpe']:.3f} {n1['mdd']*100:.2f}% "
      f"| 1/N-SMA10 {ns['sharpe']:.3f} {ns['mdd']*100:.2f}% | 1/N-vt10 {vt['sharpe']:.3f} {vt['mdd']*100:.2f}%")
    p(f"   H4 contra 1/N: {'supera' if vs1 else 'no agrega valor frente a 1/N'}; "
      f"contra 1/N-SMA10: {'supera' if vss else 'no agrega valor frente a la regla sencilla'}")
    RES["criterios"] = {"i": i_ok, "ii": ii_ok, "iii": iii_ok, "estado": estado,
                        "h4_vs_1N": vs1, "h4_vs_1N_sma10": vss}

    conciliacion(rA, rf, sigA, ini_A, RB, sigB, mesesB, nombresB)

    (AQUI / "salida.txt").write_text("\n".join(SALIDA) + "\n")
    (AQUI / "resultados.json").write_text(json.dumps(RES, indent=1, ensure_ascii=False, default=str))


# ------------------------------------------------------------ conciliacion (escrita DESPUES de leer A)
def french_zip(nombre, diario):
    import zipfile
    z = zipfile.ZipFile(DATOS / nombre)
    txt = z.read(z.namelist()[0]).decode("latin-1").splitlines()
    mkt, rfx = {}, {}
    for ln in txt:
        c = [x.strip() for x in ln.split(",")]
        if len(c) < 5 or not c[0].isdigit() or len(c[0]) != (8 if diario else 6):
            continue
        k = date(int(c[0][:4]), int(c[0][4:6]), int(c[0][6:8])) if diario else (int(c[0][:4]), int(c[0][4:6]))
        mkt[k], rfx[k] = float(c[1]) / 100, float(c[4]) / 100
    return mkt, rfx


def pesos_a(nombre, m, r_sig, rf_sig, sg_m):
    sg = sg_m[ant(m)]
    if nombre.startswith("A_ls_vt40_L"):
        return senal_ts(r_sig, rf_sig, m, int(nombre.split("L")[-1])) * min(0.40 / sg, TOPE)
    if nombre.startswith("A_lo_L"):
        return 1.0 if senal_ts(r_sig, rf_sig, m, int(nombre.split("L")[-1])) == 1 else 0.0
    if nombre == "A_ref_comprar_mantener":
        return 1.0
    if nombre == "A_ref_sma10":
        return float(senal_sma10(r_sig, m))
    if nombre == "A_ref_largo_vt40":
        return min(0.40 / sg, TOPE)
    raise KeyError(nombre)


def correr_a(nombre, r_ret, rf_ret, r_sig, rf_sig, sg_m, ini, fin, costo):
    meses = rango(ini, fin)
    W = {m: {"mkt": pesos_a(nombre, m, r_sig, rf_sig, sg_m)} for m in meses}
    return cartera({"mkt": r_ret}, rf_ret, W, meses, costo)[0], W


def conciliacion(rA, rf, sigA, ini_A, RB, sigB, mesesB, nombresB):
    p("\n=== CONCILIACION (agregada despues de leer los resultados de A; no cambia nada de arriba) ===")
    mk, rff = french_zip("french_F-F_Research_Data_Factors_CSV_202607.zip", False)
    mkd, _ = french_zip("french_F-F_Research_Data_Factors_daily_CSV_202607.zip", True)
    rF = {m: mk[m] + rff[m] for m in mk}
    niv, v = [], 1.0
    for d in sorted(mkd):
        v *= 1 + mkd[d]
        niv.append((d, v))
    sigF = sigma_fin_mes(ewma_vol(niv))
    iniF = (1927, 7)
    C = {}
    lista = ["A_ls_vt40_L3", "A_ls_vt40_L6", "A_ls_vt40_L12", "A_lo_L3", "A_lo_L6", "A_lo_L12",
             "A_ref_comprar_mantener", "A_ref_sma10", "A_ref_largo_vt40"]
    segs = {"dentro": (iniF, (2011, 12)), "dentro_1929": ((1929, 1), (2011, 12)), "pre1985": (iniF, (1984, 12)),
            "articulo": ((1985, 1), (2009, 12)), "fuera": ((2012, 1), FIN_PRE)}
    p("-- Control C: codigo de B sobre French CRSP 202607 de A (mensual Mkt-RF+RF, RF, sigma de Mkt-RF diario), desde 1927-07")
    for c_nom, c in (("def", COSTO_DEF), ("bruto", 0.0)):
        for nm in lista:
            ser, _ = correr_a(nm, rF, rff, rF, rff, sigF, iniF, FIN_PRE, c)
            for sn, (a, b) in segs.items():
                d = metricas(ser, rff, a, b)
                C.setdefault(c_nom, {}).setdefault(sn, {})[nm] = d
        for sn in segs:
            p(f"   [{c_nom}] {sn}")
            for nm in lista:
                p(f"      {nm:24s} {fmt(C[c_nom][sn][nm])}")
    RES["control_C"] = C

    # Descomposicion fuente: senal / sigma / rf / rendimientos, A_ls_vt40_L12 y A_lo_L12
    p("\n-- Descomposicion: cada fila cambia un insumo de B (S&P TR, TB3MS, sigma ^GSPC) por el de A (French)")
    combos = {
        "B puro (S&P, TB3MS, sigma S&P)": (rA, rf, rA, rf, sigA),
        "B con rf French (efectivo y senal)": (rA, rff, rA, rff, sigA),
        "B con sigma French": (rA, rf, rA, rf, sigF),
        "B con senal French (r y rf French en la senal)": (rA, rf, rF, rff, sigA),
        "rendimientos S&P, senal+sigma+rf French": (rA, rff, rF, rff, sigF),
        "rendimientos French, senal+sigma+rf S&P/TB3MS": (rF, rf, rA, rf, sigA),
        "A puro (French)": (rF, rff, rF, rff, sigF),
    }
    D = {}
    for nm in ("A_ls_vt40_L12", "A_lo_L12"):
        for etiqueta, (rr, rfr, rs, rfs, sg) in combos.items():
            for c_nom, c in (("def", COSTO_DEF), ("bruto", 0.0)):
                ser, _ = correr_a(nm, rr, rfr, rs, rfs, sg, (1929, 1), FIN_PRE, c)
                for sn, (a, b) in (("dentro_1929", ((1929, 1), (2011, 12))), ("articulo", ((1985, 1), (2009, 12))),
                                   ("fuera", ((2012, 1), FIN_PRE))):
                    D.setdefault(nm, {}).setdefault(etiqueta, {}).setdefault(c_nom, {})[sn] = metricas(ser, rfr, a, b)
            x = D[nm][etiqueta]
            p(f"   {nm} | {etiqueta:48s} | dentro29 neto {x['def']['dentro_1929']['sharpe']:.3f} (t {x['def']['dentro_1929']['t_nw6']:.2f})"
              f" | articulo bruto {x['bruto']['articulo']['sharpe']:.3f} | fuera neto {x['def']['fuera']['sharpe']:.3f} (t {x['def']['fuera']['t_nw6']:.2f})")
    RES["descomposicion_a"] = D

    # meses con signo L12 distinto
    p("\n-- Meses con signo TSMOM-12 distinto (S&P/TB3MS contra French), por segmento")
    for sn, (a, b) in (("1929-1984", ((1929, 1), (1984, 12))), ("1985-2009", ((1985, 1), (2009, 12))),
                       ("2010-2011", ((2010, 1), (2011, 12))), ("2012-2026-07", ((2012, 1), FIN_PRE))):
        ms = rango(a, b)
        dif = [m for m in ms if senal_ts(rA, rf, m, 12) != senal_ts(rF, rff, m, 12)]
        p(f"   {sn}: {len(dif)} de {len(ms)}: {', '.join(ftxt(m) for m in dif[:30])}{' ...' if len(dif) > 30 else ''}")
    # contribucion de los meses con signo distinto, A_ls_vt40_L12 bruto, ventana del articulo
    serB, WB = correr_a("A_ls_vt40_L12", rA, rf, rA, rf, sigA, (1929, 1), FIN_PRE, 0.0)
    serF, WF = correr_a("A_ls_vt40_L12", rF, rff, rF, rff, sigF, (1929, 1), FIN_PRE, 0.0)
    p("   Ventana del articulo, A_ls_vt40_L12 bruto, meses con signo distinto: w_B, w_A, exceso S&P, exceso French")
    for m in rango((1985, 1), FIN_PRE):
        if (WB[m]["mkt"] > 0) != (WF[m]["mkt"] > 0):
            p(f"      {ftxt(m)}: w_B {WB[m]['mkt']:+.2f}, w_A {WF[m]['mkt']:+.2f}, x_S&P {(rA[m]-rf[m])*100:+.2f}%, "
              f"x_French {(rF[m]-rff[m])*100:+.2f}% -> exceso de la regla B {(serB[m]-rf[m])*100:+.1f}% contra A {(serF[m]-rff[m])*100:+.1f}%")
    # cociente de sigmas
    for sn, (a, b) in (("1929-1984", ((1929, 1), (1984, 12))), ("1985-2009", ((1985, 1), (2009, 12))),
                       ("2012-2026-07", ((2012, 1), FIN_PRE))):
        ms = rango(a, b)
        q = statistics.fmean(sigA[ant(m)] / sigF[ant(m)] for m in ms)
        p(f"   sigma ^GSPC / sigma French Mkt-RF, media {sn}: {q:.3f}")
    # rendimiento pre-1929 de A (ventana)
    ser, _ = correr_a("A_ls_vt40_L12", rF, rff, rF, rff, sigF, iniF, FIN_PRE, COSTO_DEF)
    pre = metricas(ser, rff, iniF, (1928, 12))
    p(f"   A_ls_vt40_L12 French 1927-07 a 1928-12 (fuera de la ventana de B): {fmt(pre)}")

    # (b) con RF French
    p("\n-- (b) con RF de French en lugar de TB3MS (efectivo, senal y exceso), costos def, fuera 2012-01 a 2026-07")
    RES["b_rf_french"] = {}
    for nm in ("B_ls_vt40_L12", "B_lo_vt10_L12", "B_lo_L12", "B_ref_1N", "B_ref_1N_sma10", "B_ref_1N_vt10"):
        W = {}
        mesesC = [m for m in mesesB if m <= FIN_PRE]
        for m in mesesC:
            w = {}
            for t in ETFS:
                sg = sigB[t][ant(m)]
                if nm == "B_ls_vt40_L12":
                    w[t] = senal_ts(RB[t], rff, m, 12) * min(0.40 / sg, TOPE) / 8
                elif nm == "B_lo_vt10_L12":
                    w[t] = (senal_ts(RB[t], rff, m, 12) == 1) * min(1.0, 0.10 / sg) / 8
                elif nm == "B_lo_L12":
                    w[t] = (senal_ts(RB[t], rff, m, 12) == 1) / 8
                elif nm == "B_ref_1N":
                    w[t] = 1 / 8
                elif nm == "B_ref_1N_sma10":
                    w[t] = senal_sma10(RB[t], m) / 8
                else:
                    w[t] = min(1.0, 0.10 / sg) / 8
            W[m] = w
        ser = cartera(RB, rff, W, mesesC, COSTO_DEF)[0]
        d = metricas(ser, rff, (2012, 1), FIN_PRE)
        dd = metricas(ser, rff, (2007, 3), (2011, 12))
        RES["b_rf_french"][nm] = {"fuera": d, "dentro": dd}
        p(f"   {nm:16s} fuera {fmt(d)}")
        p(f"   {'':16s} dentro {fmt(dd)}")


if __name__ == "__main__":
    main()
