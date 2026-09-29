"""AC-07: segunda ejecucion independiente de R06 (Gayed y Bilello 2016).

ETF apalancados 2x/3x con filtro de media movil simple de 200 dias.
Fuente B (distinta de A, que usa French/CRSP):
  1) Simulacion 2x/3x sobre ^SP500TR (Yahoo) desde 1988, rf = FRED DTB3.
  2) ETFs reales SSO, UPRO, QLD, TQQQ (Yahoo adjclose) con filtro SMA200 sobre ^GSPC o ^NDX.
  3) Extra (comite 2-oct): temporadas de 85 dias habiles en MXN para 50% 3x filtrado + 50% 1x.

Solo biblioteca estandar; de herramientas/datos.py se usan solo los parsers genericos.
Sin red: lee datos/ (descargados el 2026-09-29 ~17:49 UTC). Escribe salida.txt,
resultados.json y datos/SHA256SUMS.txt.

Ejecutar: python3 laboratorio/auditorias/AC-07-apalancados-filtro/AC07.py
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(RAIZ))
from herramientas.datos import parsear_fred_csv, parsear_yahoo_json  # noqa: E402

DATOS = AQUI / "datos"
COSTO = 0.0029 + 0.0005        # comision GBM + spread, por lado, sobre |cambio de peso|
GASTO = 0.009                  # gasto anual del ETF simulado (L >= 2)
N_SMA = 200
CORTE_FIN_IS = date(2015, 10, 31)
FIN = date(2026, 8, 31)        # ultimo mes completo
FIN_A = date(2026, 7, 31)      # fin de A (French 202607), solo como control
PUBLICACION = date(2016, 3, 3)

LINEAS: list[str] = []


def p(*a):
    s = " ".join(str(x) for x in a)
    LINEAS.append(s)
    print(s)


# ------------------------------------------------------------------ datos

def yahoo(nombre: str) -> dict[date, float]:
    texto = (DATOS / f"yahoo_{nombre}_1d.json").read_text(encoding="utf-8")
    serie = parsear_yahoo_json(texto)["serie"]
    return {f: v for f, v in serie if f <= date(2026, 9, 28)}  # el 29-sep es intradia


def fred(nombre: str) -> list[tuple[date, float]]:
    return parsear_fred_csv((DATOS / f"fred_{nombre}.csv").read_text(encoding="utf-8"))


def ultimo_hasta(serie: list[tuple[date, float]]):
    """Devuelve f(d) = ultimo valor con fecha <= d (serie ordenada)."""
    fechas = [f for f, _ in serie]
    vals = [v for _, v in serie]
    import bisect

    def f(d: date, max_dias: int = 10):
        i = bisect.bisect_right(fechas, d) - 1
        if i < 0 or (d - fechas[i]).days > max_dias:
            raise ValueError(f"sin dato vigente para {d}")
        return vals[i]
    return f


# ------------------------------------------------------------------ piezas

def rendimientos(niveles: dict[date, float]) -> tuple[list[date], dict[date, float]]:
    fechas = sorted(niveles)
    r = {}
    for a, b in zip(fechas, fechas[1:]):
        r[b] = niveles[b] / niveles[a] - 1.0
    return fechas, r


def estado_filtro(niveles: dict[date, float], n: int = N_SMA) -> dict[date, bool]:
    """on[d] = nivel(d) > media simple de los n cierres que terminan en d (empate -> fuera)."""
    fechas = sorted(niveles)
    on = {}
    suma = 0.0
    for i, d in enumerate(fechas):
        suma += niveles[d]
        if i >= n:
            suma -= niveles[fechas[i - n]]
        if i >= n - 1:
            on[d] = niveles[d] > suma / n
    return on


_CAL: dict[int, tuple[list[date], dict[date, int]]] = {}


def senal_previa(senal: dict[date, bool], d: date, rezago: int) -> bool:
    """Estado del filtro al cierre del dia habil (del calendario del subyacente) que esta
    1 + rezago sesiones antes de d. d debe ser dia habil del subyacente."""
    clave = id(senal)
    if clave not in _CAL:
        cal = sorted(senal)
        _CAL[clave] = (cal, {f: i for i, f in enumerate(cal)})
    cal, pos = _CAL[clave]
    if d not in pos:
        raise ValueError(f"{d} no es dia del subyacente")
    j = pos[d] - 1 - rezago
    if j < 0:
        raise ValueError(f"senal no disponible para {d}")
    return cal[j] in senal and senal[cal[j]]


def correr(fechas: list[date], r_act: dict[date, float], rf: dict[date, float],
           senal: dict[date, bool] | None, rezago: int, inicio: date, fin: date,
           costo: float = COSTO):
    """Corrida continua. fechas = calendario completo del activo (incluye historia previa).

    Dia t (indice i): peso w_t = senal en fechas[i-1-rezago] (None = siempre 1).
    V_t = V_{t-1} * (1 - |w_t - w_{t-1}| * costo) * (1 + w_t r_t + (1 - w_t) rf_t).
    Exposicion inicial 0: la primera compra paga costo.
    Devuelve lista de (fecha, r_neto, rf, w).
    """
    out = []
    w_prev = 0.0
    for i, d in enumerate(fechas):
        if d < inicio or d > fin or i == 0:
            continue
        if senal is None:
            w = 1.0
        else:
            w = 1.0 if senal_previa(senal, d, rezago) else 0.0
        c = abs(w - w_prev) * costo
        r = (1 - c) * (1 + w * r_act[d] + (1 - w) * rf[d]) - 1
        out.append((d, r, rf[d], w))
        w_prev = w
    return out


def metricas(serie, desde: date, hasta: date, fecha_base: date | None = None) -> dict:
    s = [x for x in serie if desde <= x[0] <= hasta]
    if len(s) < 20:
        return {}
    v, pico, mdd = 1.0, 1.0, 0.0
    for _, r, _, _ in s:
        v *= 1 + r
        pico = max(pico, v)
        mdd = min(mdd, v / pico - 1)
    base = fecha_base or s[0][0]
    anios = (s[-1][0] - base).days / 365.25
    rs = [x[1] for x in s]
    ex = [x[1] - x[2] for x in s]
    n = len(rs)
    m = sum(rs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in rs) / (n - 1))
    me = sum(ex) / n
    sde = math.sqrt(sum((x - me) ** 2 for x in ex) / (n - 1))
    cambios = sum(1 for a, b in zip(s, s[1:]) if a[3] != b[3])
    return {
        "desde": str(s[0][0]), "hasta": str(s[-1][0]), "dias": n,
        "cagr": v ** (1 / anios) - 1, "vol": sd * math.sqrt(252),
        "sharpe": me / sde * math.sqrt(252) if sde > 1e-9 else 0.0, "mdd": mdd,
        "cambios": cambios, "cambios_anio": cambios / anios,
        "invertido": sum(x[3] for x in s) / n,
    }


def fecha_anterior(fechas: list[date], d: date) -> date:
    prev = [f for f in fechas if f < d]
    return prev[-1]


def fmt(m: dict) -> str:
    if not m:
        return "(sin datos)"
    return (f"CAGR {m['cagr']*100:6.2f}%  vol {m['vol']*100:5.1f}%  Sharpe {m['sharpe']:5.2f}  "
            f"MDD {m['mdd']*100:6.1f}%  camb/año {m['cambios_anio']:4.1f}  inv {m['invertido']*100:4.0f}%")


# ------------------------------------------------------------------ principal

def main():
    # huellas
    sums = []
    for f in sorted(DATOS.iterdir()):
        if f.name == "SHA256SUMS.txt":
            continue
        sums.append(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}")
    (DATOS / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")

    p("AC-07  segunda ejecucion independiente de R06 (fuente B: Yahoo + FRED DTB3)")
    p(f"Costo por cambio {COSTO*100:.2f}% por lado; gasto simulado {GASTO*100:.1f}%/año; SMA {N_SMA}")
    p("")

    niv = {n: yahoo(n) for n in "SP500TR GSPC NDX SPY QQQ SSO UPRO QLD TQQQ".split()}
    dtb3 = ultimo_hasta(fred("DTB3"))
    fx = ultimo_hasta(fred("DEXMXUS"))

    def rf_para(fechas):
        """rf_t = DTB3 vigente al cierre de t-1 (tasa de descuento, base 360) * dias naturales/360."""
        out = {}
        for a, b in zip(fechas, fechas[1:]):
            out[b] = dtb3(a) / 100 * (b - a).days / 360
        return out

    # control de datos: huecos y saltos
    for n, d in niv.items():
        f = sorted(d)
        huecos = [(str(a), (b - a).days) for a, b in zip(f, f[1:]) if (b - a).days > 5]
        _, r = rendimientos(d)
        lim = 0.60 if n in ("UPRO", "TQQQ") else 0.40 if n in ("SSO", "QLD") else 0.25
        saltos = [(str(k), round(v, 3)) for k, v in r.items() if abs(v) > lim]
        p(f"datos {n:8s} {f[0]} a {f[-1]}  {len(f)} dias  huecos>5d: {len(huecos)} {huecos[:3]}  |r|>{lim}: {saltos}")
    p("")

    res: dict = {"parametros": {"costo_lado": COSTO, "gasto": GASTO, "sma": N_SMA,
                                "fin": str(FIN), "corte": str(CORTE_FIN_IS)}}

    # ======================= 1) simulacion sobre ^SP500TR =========================
    p("=" * 100)
    p("1) SIMULADO desde ^SP500TR: r_L = L*r - (L-1)*rf - 0.9%*dd/365.25; efectivo = DTB3")
    p("=" * 100)
    fechas_tr, r_tr = rendimientos(niv["SP500TR"])
    rf_tr = rf_para(fechas_tr)
    sim = {}
    for L in (1, 2, 3):
        g = GASTO if L >= 2 else 0.0
        sim[L] = {d: L * r_tr[d] - (L - 1) * rf_tr[d] - g * (d - a).days / 365.25
                  for a, d in zip(fechas_tr, fechas_tr[1:])}
    on_tr = estado_filtro(niv["SP500TR"])
    on_gspc = estado_filtro(niv["GSPC"])
    comunes = [d for d in on_tr if d in on_gspc]
    acuerdo = sum(1 for d in comunes if on_tr[d] == on_gspc[d]) / len(comunes)
    p(f"Senal SMA200 ^SP500TR vs ^GSPC: mismo estado en {acuerdo*100:.1f}% de {len(comunes)} dias")
    inicio_sim = date(1988, 11, 1)  # primer dia con SMA200 de ^SP500TR disponible con rezago
    segmentos = {
        "dentro_1988_2015": (inicio_sim, date(2015, 10, 30)),
        "dentro_1990_2015_(ventana_bloque_F_de_A)": (date(1990, 1, 2), date(2015, 10, 30)),
        "sub_2000_01_a_2015_10": (date(2000, 1, 3), date(2015, 10, 30)),
        "sub_2015_11_a_2019_12": (date(2015, 11, 2), date(2019, 12, 31)),
        "sub_2020_01_a_2026_07": (date(2020, 1, 2), FIN_A),
        "fuera_2015_11_a_2026_08": (date(2015, 11, 2), FIN),
        "fuera_hasta_2026_07_(ventana_A)": (date(2015, 11, 2), FIN_A),
        "post_publicacion_2016_03_04": (date(2016, 3, 4), FIN),
        "toda_1988_2026_08": (inicio_sim, FIN),
    }
    corr_sim = {}
    for L in (1, 2, 3):
        corr_sim[f"bh_L{L}"] = correr(fechas_tr, sim[L], rf_tr, None, 0, inicio_sim, FIN)
        corr_sim[f"sma200_L{L}"] = correr(fechas_tr, sim[L], rf_tr, on_tr, 0, inicio_sim, FIN)
        corr_sim[f"sma200_L{L}_rezago"] = correr(fechas_tr, sim[L], rf_tr, on_tr, 1, inicio_sim, FIN)
        corr_sim[f"sma200gspc_L{L}"] = correr(fechas_tr, sim[L], rf_tr, on_gspc, 0, inicio_sim, FIN)
    corr_sim["efectivo"] = correr(fechas_tr, sim[1], rf_tr, {d: False for d in on_tr}, 0, inicio_sim, FIN)
    corr_sim["sma200_L2_sin_costo"] = correr(fechas_tr, sim[2], rf_tr, on_tr, 0, inicio_sim, FIN, 0.0)
    corr_sim["sma200_L3_sin_costo"] = correr(fechas_tr, sim[3], rf_tr, on_tr, 0, inicio_sim, FIN, 0.0)
    res["simulado"] = {}
    for seg, (a, b) in segmentos.items():
        p(f"\n-- {seg}  ({a} a {b})")
        base = fecha_anterior(fechas_tr, a)
        res["simulado"][seg] = {}
        for k, s in corr_sim.items():
            m = metricas(s, a, b, base)
            res["simulado"][seg][k] = m
            p(f"  {k:24s} {fmt(m)}")

    def veredicto(tab, bh1="bh_L1", pref="sma200_L", bhp="bh_L"):
        sost = all(tab[f"{pref}{L}"]["sharpe"] >= tab[bh1]["sharpe"] and
                   tab[f"{pref}{L}"]["cagr"] > tab[bh1]["cagr"] for L in (2, 3))
        prot = all(tab[f"{pref}{L}"]["mdd"] > tab[f"{bhp}{L}"]["mdd"] for L in (2, 3))
        return "Se sostiene" if sost else "Solo protección" if prot else "No se sostiene"

    v_oos = veredicto(res["simulado"]["fuera_2015_11_a_2026_08"])
    v_oos_a = veredicto(res["simulado"]["fuera_hasta_2026_07_(ventana_A)"])
    t = res["simulado"]["fuera_2015_11_a_2026_08"]
    sost_r = all(t[f"sma200_L{L}_rezago"]["sharpe"] >= t["bh_L1"]["sharpe"] and
                 t[f"sma200_L{L}_rezago"]["cagr"] > t["bh_L1"]["cagr"] for L in (2, 3))
    prot_r = all(t[f"sma200_L{L}_rezago"]["mdd"] > t[f"bh_L{L}"]["mdd"] for L in (2, 3))
    v_oos_rez = "Se sostiene" if sost_r else "Solo protección" if prot_r else "No se sostiene"
    ti = res["simulado"]["dentro_1988_2015"]
    refuta = (ti["sma200_L2"]["cagr"] <= ti["bh_L1"]["cagr"] or
              ti["sma200_L2"]["sharpe"] <= ti["bh_L1"]["sharpe"])
    p("")
    p(f"VEREDICTO fuera de muestra (simulado, al cierre, 2015-11 a 2026-08): {v_oos}")
    p(f"  mismo, ventana de A (hasta 2026-07): {v_oos_a};  con rezago de 1 dia: {v_oos_rez}")
    p(f"Refutacion dentro de muestra 1988-2015 (LRS2x <= 1x en CAGR o Sharpe): {'SI' if refuta else 'NO'}")
    res["veredictos"] = {"fuera_sim_cierre": v_oos, "fuera_sim_ventanaA": v_oos_a,
                         "fuera_sim_rezago": v_oos_rez, "refuta_dentro_1988_2015": refuta}

    # ======================= 2) ETFs reales ======================================
    p("")
    p("=" * 100)
    p("2) ETFs REALES (Yahoo adjclose), filtro SMA200 sobre ^GSPC (SSO, UPRO) o ^NDX (QLD, TQQQ)")
    p("   efectivo = DTB3; costo 0.34% por cambio; 'cierre' = senal t-1; 'rezago' = senal t-2")
    p("=" * 100)
    on_ndx = estado_filtro(niv["NDX"])
    on_1x = {"SPY": estado_filtro(niv["SPY"]), "QQQ": estado_filtro(niv["QQQ"])}
    etfs = {"SSO": ("SPY", on_gspc, 2), "UPRO": ("SPY", on_gspc, 3),
            "QLD": ("QQQ", on_ndx, 2), "TQQQ": ("QQQ", on_ndx, 3)}
    res["reales"] = {}
    series_reales = {}
    for etf, (base1x, on, L) in etfs.items():
        f_e, r_e = rendimientos(niv[etf])
        rf_e = rf_para(f_e)
        f_b, r_b = rendimientos(niv[base1x])
        rf_b = rf_para(f_b)
        ini = f_e[1]
        # simulador sobre el 1x real en la misma ventana (validacion H6)
        fb_set = set(f_b)
        comunes = [d for d in f_e if d in fb_set]
        assert len(comunes) == len(f_e), f"{etf}: fechas sin {base1x}"
        sim_e = {d: L * r_b[d] - (L - 1) * rf_b[d] - GASTO * (d - a).days / 365.25
                 for a, d in zip(f_e, f_e[1:])}
        corr = {
            f"{etf}_bh": correr(f_e, r_e, rf_e, None, 0, ini, FIN),
            f"{etf}_sma200": correr(f_e, r_e, rf_e, on, 0, ini, FIN),
            f"{etf}_sma200_rezago": correr(f_e, r_e, rf_e, on, 1, ini, FIN),
            f"{etf}_sma200_senal{base1x}": correr(f_e, r_e, rf_e, on_1x[base1x], 0, ini, FIN),
            f"{etf}_sma200_senal{base1x}_rezago": correr(f_e, r_e, rf_e, on_1x[base1x], 1, ini, FIN),
            f"{base1x}_bh": correr(f_b, r_b, rf_b, None, 0, ini, FIN),
            f"{base1x}_sma200": correr(f_b, r_b, rf_b, on, 0, ini, FIN),
            f"sim{L}x_{base1x}_bh": correr(f_e, sim_e, rf_e, None, 0, ini, FIN),
            f"sim{L}x_{base1x}_sma200": correr(f_e, sim_e, rf_e, on, 0, ini, FIN),
        }
        series_reales[etf] = corr
        res["reales"][etf] = {}
        for seg, (a, b) in {"toda": (ini, FIN), "fuera_2015_11_a_2026_08": (date(2015, 11, 2), FIN),
                            "fuera_hasta_2026_07": (date(2015, 11, 2), FIN_A)}.items():
            p(f"\n-- {etf} ({L}x, 1x = {base1x})  {seg}")
            baseF = fecha_anterior(f_e, a)
            res["reales"][etf][seg] = {}
            for k, s in corr.items():
                m = metricas(s, a, b, baseF)
                res["reales"][etf][seg][k] = m
                p(f"  {k:24s} {fmt(m)}")
        # correlacion diaria sim vs real
        xs = [sim_e[d] for d in f_e[1:] if d <= FIN]
        ys = [r_e[d] for d in f_e[1:] if d <= FIN]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        rho = cov / math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
        tt = res["reales"][etf]["toda"]
        dif = tt[f"sim{L}x_{base1x}_bh"]["cagr"] - tt[f"{etf}_bh"]["cagr"]
        res["reales"][etf]["validacion"] = {"rho": rho, "cagr_sim_menos_real": dif}
        p(f"  validacion simulador: rho diaria {rho:.4f}; CAGR sim - real {dif*100:+.2f} pp/año")

    p("")
    p("Veredicto con ETFs reales, fuera de muestra (2x y 3x del mismo indice contra su 1x):")
    res["veredictos"]["reales"] = {}
    for idx, (e2, e3, b1) in {"S&P": ("SSO", "UPRO", "SPY"), "NDX": ("QLD", "TQQQ", "QQQ")}.items():
        for modo in ("sma200", "sma200_rezago"):
            tab = {}
            for L, e in ((2, e2), (3, e3)):
                t = res["reales"][e]["fuera_2015_11_a_2026_08"]
                tab[f"s{L}"] = t[f"{e}_{modo}"]
                tab[f"b{L}"] = t[f"{e}_bh"]
                tab["b1"] = t[f"{b1}_bh"]
            v = veredicto(tab, bh1="b1", pref="s", bhp="b")
            res["veredictos"]["reales"][f"{idx}_{modo}"] = v
            p(f"  {idx:4s} {modo:14s}: {v}")

    # ======================= 3) temporadas en MXN ================================
    p("")
    p("=" * 100)
    p("3) TEMPORADAS en MXN: 85 dias habiles, inicio cada 5 dias; carteras con ETFs reales")
    p("   50% 3x filtrado (fuera -> T-bill USD) + 50% 1x; bandas de rebalanceo 50% +- 5 pp;")
    p("   costo 0.34% sobre cada pierna de ETF operada; MXN = USD * DEXMXUS (ultimo <= fecha)")
    p("=" * 100)

    def cartera(lev: str, base1x: str, on, k: float, rezago: int, filtrar: bool = True,
                desde: date = date(1900, 1, 1)):
        f_l, r_l = rendimientos(niv[lev])
        f_b, r_b = rendimientos(niv[base1x])
        fb = set(f_b)
        f = [d for d in f_l if d in fb and desde <= d <= FIN]
        rf = rf_para(f)
        a_val, b_val = 0.0, 1.0  # manga apalancada (ETF o efectivo) y manga 1x
        # inicio: todo en efectivo, se compra al primer dia (paga costo)
        a_val, b_val, en_etf = k, 0.0, False
        cash_b = 1 - k  # efectivo de la manga 1x antes de comprar
        curva = []
        for i, d in enumerate(f):
            if i == 0:
                continue
            quiere = True
            if filtrar:
                quiere = senal_previa(on, d, rezago)
            V = a_val + b_val + cash_b
            costo = 0.0
            if cash_b > 0:  # compra inicial de la manga 1x
                costo += cash_b * COSTO
                b_val, cash_b = cash_b, 0.0
            if quiere != en_etf:
                costo += a_val * COSTO
                en_etf = quiere
            wa = a_val / V
            if abs(wa - k) > 0.05:
                delta = abs(k * V - a_val)
                costo += delta * COSTO  # pierna 1x
                if en_etf:
                    costo += delta * COSTO  # pierna apalancada
                a_val, b_val = k * V, (1 - k) * V
            # costo se descuenta proporcionalmente
            fac = 1 - costo / V
            a_val *= fac
            b_val *= fac
            a_val *= 1 + (r_l[d] if en_etf else rf[d])
            b_val *= 1 + r_b[d]
            curva.append((d, a_val + b_val))
        return curva

    def temporadas(curva, mxn=True, largo=85, paso=5):
        vals = [(d, v * (fx(d) if mxn else 1.0)) for d, v in curva]
        dds, rets = [], []
        for s in range(0, len(vals) - largo, paso):
            v0 = vals[s][1]
            pico, dd = v0, 0.0
            for _, v in vals[s + 1: s + largo + 1]:
                pico = max(pico, v)
                dd = min(dd, v / pico - 1)
            dds.append(dd)
            rets.append(vals[s + largo][1] / v0 - 1)
        return dds, rets

    def pct(x, q):
        x = sorted(x)
        h = (len(x) - 1) * q
        lo = math.floor(h)
        return x[lo] + (h - lo) * (x[min(lo + 1, len(x) - 1)] - x[lo])

    res["temporadas"] = {}
    carteras = {
        "50UPROfilt+50SPY_rezago": ("UPRO", "SPY", on_gspc, 0.5, 1, True, date(2009, 6, 25)),
        "50UPROfilt+50SPY_cierre": ("UPRO", "SPY", on_gspc, 0.5, 0, True, date(2009, 6, 25)),
        "50UPRObh+50SPY": ("UPRO", "SPY", on_gspc, 0.5, 0, False, date(2009, 6, 25)),
        "100SPY": ("SPY", "SPY", on_gspc, 0.0, 0, False, date(2009, 6, 25)),
        "50TQQQfilt+50QQQ_rezago": ("TQQQ", "QQQ", on_ndx, 0.5, 1, True, date(2010, 2, 11)),
        "50TQQQfilt+50QQQ_cierre": ("TQQQ", "QQQ", on_ndx, 0.5, 0, True, date(2010, 2, 11)),
        "50TQQQbh+50QQQ": ("TQQQ", "QQQ", on_ndx, 0.5, 0, False, date(2010, 2, 11)),
        "100QQQ": ("QQQ", "QQQ", on_ndx, 0.0, 0, False, date(2010, 2, 11)),
    }
    p(f"\n{'cartera':26s} {'desde':10s} {'n':>4s}  P(DD>=12%) P(>=20%) P(>=28%) P(>=35%)   p10    mediana   p90   | peor DD")
    for nom, args in carteras.items():
        cur = cartera(*args)
        for mon in ("MXN", "USD"):
            dds, rets = temporadas(cur, mxn=(mon == "MXN"))
            fr = {u: sum(1 for x in dds if x <= -u / 100) / len(dds) for u in (12, 20, 28, 35)}
            r = {"desde": str(cur[0][0]), "hasta": str(cur[-1][0]), "n": len(dds),
                 "p_dd": fr, "p10": pct(rets, 0.10), "mediana": pct(rets, 0.5),
                 "p90": pct(rets, 0.90), "peor_dd": min(dds)}
            res["temporadas"][f"{nom}_{mon}"] = r
            if mon == "MXN" or nom.startswith("50") and nom.endswith("rezago"):
                p(f"{nom+' '+mon:26s} {r['desde']} {r['n']:4d}    {fr[12]*100:5.1f}%   {fr[20]*100:5.1f}%  "
                  f"{fr[28]*100:5.1f}%  {fr[35]*100:5.1f}%  {r['p10']*100:6.1f}% {r['mediana']*100:6.1f}% "
                  f"{r['p90']*100:6.1f}% | {r['peor_dd']*100:6.1f}%")
    p("Nota: temporadas traslapadas (17 por ventana); no son independientes.")

    (AQUI / "salida.txt").write_text("\n".join(LINEAS) + "\n", encoding="utf-8")
    (AQUI / "resultados.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str),
                                          encoding="utf-8")


if __name__ == "__main__":
    main()
