"""AC-05: segunda ejecucion independiente de R08 (peso y acciones de EUA para quien mide en MXN).

Escrito desde cero a partir SOLO de las secciones 1-9 (pre-registro) de
laboratorio/replicas/R08-peso-y-acciones-para-un-mexicano.md. No importa ni copia R08.py.

Fuente principal (distinta de A):
  R  = S&P 500 Total Return, Yahoo ^SP500TR (fin de mes; no CRSP/French).
  S  = USD/MXN FIX de Banxico SF43718 (fin de mes; no FRED DEXMXUS).
  CETES = FRED INTGSTMXM193N (FMI), valor del mes t-1 / 1200 (no Banxico SF43936).
  i_US  = FRED TB3MS, valor del mes t-1 / 1200 (no French RF).
Contrastes: Yahoo MXN=X (2004-01+), FRED DEXMXUS, Banxico CETES 28 SF43936.
Solo biblioteca estandar. Uso de herramientas/: solo parsear_yahoo_json y parsear_fred_csv.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import random
import sys
from calendar import monthrange
from datetime import date, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))
from herramientas.datos import parsear_fred_csv, parsear_yahoo_json  # noqa: E402

DIR = Path(__file__).resolve().parent
DD = DIR / "datos"
SEMILLA = 20260925
COSTO_LADO = 0.0029 + 0.0005  # comision GBM + spread supuesto, por lado
INI, FIN = (1994, 1), (2026, 7)
CORTE = (2007, 5)
MAX_DIAS = 10

salida_lineas: list[str] = []


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    salida_lineas.append(s)


# ------------------------------------------------------------------ carga

def sha(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def yahoo(nombre):
    return parsear_yahoo_json((DD / nombre).read_text(encoding="utf-8"))["serie"]


def fred(nombre):
    return parsear_fred_csv((DD / nombre).read_text(encoding="utf-8"))


def banxico(nombre):
    txt = (DD / nombre).read_bytes().decode("latin-1")
    out = []
    for fila in csv.reader(io.StringIO(txt)):
        if len(fila) != 2:
            continue
        try:
            d, m, y = fila[0].split("/")
            f = date(int(y), int(m), int(d))
            v = float(fila[1])
        except ValueError:
            continue
        out.append((f, v))
    return sorted(out)


def meses(ini, fin):
    y, m = ini
    while (y, m) <= fin:
        yield (y, m)
        m += 1
        if m == 13:
            y, m = y + 1, 1


def ant(ym):
    y, m = ym
    return (y - 1, 12) if m == 1 else (y, m - 1)


def fin_mes(ym):
    return date(ym[0], ym[1], monthrange(*ym)[1])


def ultimo_leq(serie, fecha, max_dias=MAX_DIAS):
    """Ultimo (fecha, valor) con fecha <= fecha y antiguedad <= max_dias (busqueda binaria)."""
    lo, hi = 0, len(serie) - 1
    idx = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if serie[mid][0] <= fecha:
            idx = mid
            lo = mid + 1
        else:
            hi = mid - 1
    if idx < 0 or (fecha - serie[idx][0]).days > max_dias:
        return None
    return serie[idx]


def mensual_fin(serie, ini, fin):
    out = {}
    for ym in meses(ant(ini), fin):
        r = ultimo_leq(serie, fin_mes(ym))
        if r is not None:
            out[ym] = r[1]
    return out


def mensual_fred(serie):
    return {(f.year, f.month): v for f, v in serie}


# ------------------------------------------------------------------ estadistica

def media(a):
    return sum(a) / len(a)


def desv(a):
    m = media(a)
    return math.sqrt(sum((v - m) ** 2 for v in a) / (len(a) - 1))


def corr(a, b):
    ma, mb = media(a), media(b)
    sab = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    saa = sum((x - ma) ** 2 for x in a)
    sbb = sum((y - mb) ** 2 for y in b)
    return sab / math.sqrt(saa * sbb)


def vol_anual(r):
    return desv(r) * math.sqrt(12)


def cagr(r, periodos=12):
    v = 1.0
    for x in r:
        v *= 1 + x
    return v ** (periodos / len(r)) - 1


def mdd(r):
    v, pico, peor = 1.0, 1.0, 0.0
    for x in r:
        v *= 1 + x
        pico = max(pico, v)
        peor = min(peor, v / pico - 1)
    return peor


def mdd_fechas(fechas, niveles):
    pico_v, pico_f = niveles[0], fechas[0]
    peor, pf, vf = 0.0, fechas[0], fechas[0]
    for f, v in zip(fechas, niveles):
        if v > pico_v:
            pico_v, pico_f = v, f
        dd = v / pico_v - 1
        if dd < peor:
            peor, pf, vf = dd, pico_f, f
    return peor, pf, vf


def sharpe(r, rf):
    ex = [a - b for a, b in zip(r, rf)]
    return media(ex) / desv(ex) * math.sqrt(12)


def nw_t_media(a, rez=6):
    n = len(a)
    m = media(a)
    e = [v - m for v in a]
    g0 = sum(v * v for v in e) / n
    s = g0
    for L in range(1, rez + 1):
        g = sum(e[i] * e[i - L] for i in range(L, n)) / n
        s += 2 * (1 - L / (rez + 1)) * g
    return m / math.sqrt(s / n), m / (desv(a) / math.sqrt(n))


def ols_nw(y, x, rez=6):
    n = len(y)
    mx, my = media(x), media(y)
    sxx = sum((v - mx) ** 2 for v in x)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sxx
    a0 = my - b * mx
    u = [c - a0 - b * a for a, c in zip(x, y)]
    z = [(a - mx) * e for a, e in zip(x, u)]
    s = sum(v * v for v in z)
    for L in range(1, rez + 1):
        s += 2 * (1 - L / (rez + 1)) * sum(z[i] * z[i - L] for i in range(L, n))
    se = math.sqrt(s) / sxx
    return b, b / se


def indices_bloques(n, bloque, rng):
    idx = []
    while len(idx) < n:
        s = rng.randrange(0, n - bloque + 1)
        idx.extend(range(s, s + bloque))
    return idx[:n]


def ic_boot(fn, series, bloque=12, reps=5000, semilla=SEMILLA):
    """IC 95% por bootstrap de bloques moviles; las series se remuestrean pareadas."""
    rng = random.Random(semilla)
    n = len(series[0])
    vals = []
    for _ in range(reps):
        ix = indices_bloques(n, bloque, rng)
        vals.append(fn(*[[s[i] for i in ix] for s in series]))
    vals.sort()
    return vals[int(0.025 * reps)], vals[int(0.975 * reps) - 1]


# ------------------------------------------------------------------ construccion

def construir(R, S, cetes_m, rfus_m, ventana_meses):
    """Devuelve dict de listas alineadas por mes: R, x, U, f, cetes, rf."""
    d = {k: [] for k in ("ym", "R", "x", "U", "f", "cetes", "rf")}
    faltan = []
    for ym in ventana_meses:
        pm = ant(ym)
        if ym not in R or pm not in R or ym not in S or pm not in S or pm not in cetes_m or pm not in rfus_m:
            faltan.append(ym)
            continue
        r = R[ym] / R[pm] - 1
        x = S[ym] / S[pm] - 1
        c = cetes_m[pm]
        rf = rfus_m[pm]
        d["ym"].append(ym)
        d["R"].append(r)
        d["x"].append(x)
        d["U"].append((1 + r) * (1 + x) - 1)
        d["f"].append((1 + c) / (1 + rf) - 1)
        d["cetes"].append(c)
        d["rf"].append(rf)
    return d, faltan


def cubierta(d, h, c_anual=0.0):
    return [u - h * ((1 + x) - (1 + f)) - h * c_anual / 12 for u, x, f in zip(d["U"], d["x"], d["f"])]


def con_costo_entrada(r):
    r = list(r)
    r[0] = (1 + r[0]) * (1 - COSTO_LADO) - 1
    return r


def bench50(activo, cetes):
    """50% activo + 50% CETES, rebalanceo mensual con deriva; costo sobre la parte negociada."""
    out = []
    w = 0.5
    for i, (a, c) in enumerate(zip(activo, cetes)):
        giro = 0.5 if i == 0 else abs(0.5 - w)  # entrada: se compra 50%
        costo = giro * COSTO_LADO
        rp = 0.5 * a + 0.5 * c
        out.append((1 - costo) * (1 + rp) - 1)
        w = 0.5 * (1 + a) / (1 + rp)
    return out


def minvar_expansiva(d, minimo=36):
    hs, rets = [], []
    H = [x - f for x, f in zip(d["x"], d["f"])]
    for t in range(len(d["U"])):
        if t < minimo:
            h = 0.0
        else:
            U, Hh = d["U"][:t], H[:t]
            mu, mh = media(U), media(Hh)
            cov = sum((a - mu) * (b - mh) for a, b in zip(U, Hh)) / (t - 1)
            var = sum((b - mh) ** 2 for b in Hh) / (t - 1)
            h = min(1.0, max(0.0, cov / var))
        hs.append(h)
        rets.append(d["U"][t] - h * H[t])
    return hs, rets


def h_minvar(d, idx):
    U = [d["U"][i] for i in idx]
    H = [d["x"][i] - d["f"][i] for i in idx]
    mu, mh = media(U), media(H)
    return sum((a - mu) * (b - mh) for a, b in zip(U, H)) / sum((b - mh) ** 2 for b in H)


def segmentos(d):
    n = len(d["ym"])
    todos = list(range(n))
    dentro = [i for i in todos if d["ym"][i] <= CORTE]
    fuera = [i for i in todos if d["ym"][i] > CORTE]
    return {"completo": todos, "dentro": dentro, "fuera": fuera}


def sub(a, idx):
    return [a[i] for i in idx]


# ------------------------------------------------------------------ principal

def main():
    res = {"descripcion": "AC-05, segunda ejecucion independiente de R08", "fuentes_principales": {
        "R": "Yahoo ^SP500TR fin de mes", "S": "Banxico FIX SF43718 fin de mes",
        "cetes": "FRED INTGSTMXM193N mes t-1/1200", "i_us": "FRED TB3MS mes t-1/1200"}}
    huellas = {f.name: sha(f) for f in sorted(DD.iterdir()) if f.is_file() and f.name != "SHA256SUMS.txt"}
    (DD / "SHA256SUMS.txt").write_text("".join(f"{h}  {n}\n" for n, h in huellas.items()))
    res["sha256"] = huellas

    sptr_d = yahoo("yahoo_SP500TR_1d.json")
    gspc_d = yahoo("yahoo_GSPC_1d.json")
    mxnx_d = yahoo("yahoo_MXN=X_1d.json")
    fix_d = banxico("banxico_SF43718_fix.csv")
    cet28 = banxico("banxico_SF43936_cetes28.csv")
    dex_d = fred("fred_DEXMXUS.csv")
    intg = mensual_fred(fred("fred_INTGSTMXM193N.csv"))
    tb3 = mensual_fred(fred("fred_TB3MS.csv"))

    cetes_m = {k: v / 1200 for k, v in intg.items()}
    rfus_m = {k: v / 1200 for k, v in tb3.items()}
    # CETES 28 Banxico (contraste): ultima subasta <= fin de t-1, rendimiento tasa*dias/36000, indexado por t-1
    cet28_m = {}
    for ym in meses((1993, 1), FIN):
        r = ultimo_leq(cet28, fin_mes(ym), max_dias=40)
        if r:
            nxt = (ym[0] + (ym[1] == 12), 1 if ym[1] == 12 else ym[1] + 1)
            cet28_m[ym] = r[1] / 100 * monthrange(*nxt)[1] / 360

    R = mensual_fin(sptr_d, INI, FIN)
    Rp = mensual_fin(gspc_d, (1996, 1), FIN)
    S_fix = mensual_fin(fix_d, INI, FIN)
    S_mxnx = mensual_fin(mxnx_d, (2004, 1), FIN)
    S_dex = mensual_fin(dex_d, INI, FIN)

    todos_meses = list(meses(INI, FIN))
    d, faltan = construir(R, S_fix, cetes_m, rfus_m, todos_meses)
    p("=" * 78)
    p("AC-05  Segunda ejecucion independiente de R08  (B: ^SP500TR x FIX Banxico; CETES FMI; TB3MS)")
    p("=" * 78)
    p(f"Meses: {d['ym'][0]} a {d['ym'][-1]}  n={len(d['ym'])}  faltantes={faltan}")
    seg = segmentos(d)
    p(f"n completo={len(seg['completo'])} dentro={len(seg['dentro'])} fuera={len(seg['fuera'])}")

    # control de calidad FX: MXN=X y DEXMXUS contra FIX en fin de mes
    difs = [(ym, S_mxnx[ym] / S_fix[ym] - 1) for ym in S_mxnx if ym in S_fix]
    difs_dex = [(ym, S_dex[ym] / S_fix[ym] - 1) for ym in S_dex if ym in S_fix]
    p("\n[QC] Nivel fin de mes MXN=X/FIX-1: max abs = %.4f en %s ; DEXMXUS/FIX-1: max abs = %.4f en %s" % (
        max(abs(v) for _, v in difs), max(difs, key=lambda t: abs(t[1]))[0],
        max(abs(v) for _, v in difs_dex), max(difs_dex, key=lambda t: abs(t[1]))[0]))
    res["qc_fx"] = {"mxnx_vs_fix_maxabs": max(abs(v) for _, v in difs),
                    "dex_vs_fix_maxabs": max(abs(v) for _, v in difs_dex)}

    # ---------------- metricas por variante
    hs_fijas = [0.0, 0.25, 0.5, 0.75, 1.0]
    variantes = {}
    for h in hs_fijas:
        variantes[f"mxn_h{int(h*100):03d}"] = cubierta(d, h)
    hexp, rexp = minvar_expansiva(d)
    variantes["mxn_hminvar_exp36"] = rexp
    variantes["bench50_h000"] = bench50(d["U"], d["cetes"])
    variantes["bench50_h100"] = bench50(variantes["mxn_h100"], d["cetes"])
    variantes["usd_referencia"] = d["R"]
    variantes["cetes_100"] = d["cetes"]
    netas = {k: (con_costo_entrada(v) if not k.startswith("bench50") and k != "cetes_100" else v)
             for k, v in variantes.items()}

    p("\n[Metricas] neto de costo de entrada 0.34%; 50/50 con costo de rebalanceo. Sharpe vs CETES (MXN) o TB3MS (USD).")
    p(f"{'variante':22s} {'segm':9s} {'CAGR':>7s} {'vol':>6s} {'Sharpe':>7s} {'MDD':>7s}")
    res["metricas"] = {}
    for k, v in netas.items():
        res["metricas"][k] = {}
        for sn, idx in seg.items():
            r = sub(v, idx)
            if k == "usd_referencia":
                rfb = sub(d["rf"], idx)
            else:
                rfb = sub(d["cetes"], idx)
            m = {"cagr": cagr(r), "vol": vol_anual(r), "mdd": mdd(r)}
            m["sharpe"] = sharpe(r, rfb) if k != "cetes_100" else float("nan")
            res["metricas"][k][sn] = m
            p(f"{k:22s} {sn:9s} {m['cagr']*100:7.2f} {m['vol']*100:6.2f} {m['sharpe']:7.3f} {m['mdd']*100:7.2f}")
    M = res["metricas"]

    # ---------------- H1
    p("\n[H1] corr(R, x) mensual; IC95 bootstrap bloques 12, 5000 rep, semilla 20260925")
    vent = {"completo": seg["completo"], "dentro": seg["dentro"], "fuera": seg["fuera"],
            "2008-2026": [i for i, ym in enumerate(d["ym"]) if ym >= (2008, 1)],
            "2016-2026": [i for i, ym in enumerate(d["ym"]) if ym >= (2016, 1)],
            "1996-2026": [i for i, ym in enumerate(d["ym"]) if ym >= (1996, 1)],
            "2023-2026": [i for i, ym in enumerate(d["ym"]) if ym >= (2023, 1)]}
    res["H1"] = {}
    for vn, idx in vent.items():
        a, b = sub(d["R"], idx), sub(d["x"], idx)
        c = corr(a, b)
        ic = ic_boot(corr, [a, b]) if vn in ("completo", "dentro", "fuera", "2008-2026", "2016-2026") else (None, None)
        beta, tnw = ols_nw(b, a)
        neg = [i for i in range(len(a)) if a[i] < 0]
        pos = [i for i in range(len(a)) if a[i] >= 0]
        bneg, _ = ols_nw(sub(b, neg), sub(a, neg))
        bpos, _ = ols_nw(sub(b, pos), sub(a, pos))
        res["H1"][vn] = {"corr": c, "ic95": ic, "beta": beta, "t_nw": tnw, "beta_R_neg": bneg, "beta_R_pos": bpos, "n": len(a)}
        ics = f"[{ic[0]:.3f}, {ic[1]:.3f}]" if ic[0] is not None else ""
        p(f"  {vn:10s} n={len(a):3d} corr={c:6.3f} {ics:18s} beta={beta:6.3f} tNW={tnw:6.2f} beta(R<0)={bneg:6.3f} beta(R>=0)={bpos:6.3f}")
    h1c = res["H1"]["completo"]
    h1_refutada = h1c["corr"] >= 0 or (h1c["ic95"][0] <= 0 <= h1c["ic95"][1])
    h1_ok = (not h1_refutada) and all(res["H1"][k]["corr"] < 0 for k in ("dentro", "fuera", "2008-2026", "2016-2026"))
    h1_rango = -0.60 <= h1c["corr"] <= -0.35
    p(f"  H1 refutada={h1_refutada}; signo negativo en todas={h1_ok}; completo en [-0.60,-0.35]={h1_rango}")
    res["H1"]["refutada"] = h1_refutada
    res["H1"]["cumple_signos"] = h1_ok
    res["H1"]["en_rango"] = h1_rango

    # ---------------- H2
    p("\n[H2] meses extremos, completo 1994-01..2026-07")
    R1 = variantes["mxn_h100"]
    n = len(d["R"])
    orden = sorted(range(n), key=lambda i: d["R"][i])
    k10 = round(n / 10)
    grupos = {"R<-5%": [i for i in range(n) if d["R"][i] < -0.05],
              "peor_decil": orden[:k10],
              "R>+5%": [i for i in range(n) if d["R"][i] > 0.05],
              "mejor_decil": orden[-k10:]}
    res["H2"] = {}
    for g, idx in grupos.items():
        mR, mx, mU, m1 = (media(sub(s, idx)) for s in (d["R"], d["x"], d["U"], R1))
        px = sum(1 for i in idx if d["x"][i] > 0) / len(idx)
        A = 1 - mU / mR
        res["H2"][g] = {"n": len(idx), "R": mR, "x": mx, "U": mU, "R1": m1, "prop_x_pos": px, "A": A}
        p(f"  {g:12s} n={len(idx):3d} R={mR*100:6.2f} x={mx*100:6.2f} U={mU*100:6.2f} R^1={m1*100:6.2f} %x>0={px:.2f} A={A:.3f}")
    g5 = res["H2"]["R<-5%"]
    h2_ok = 0.02 <= g5["x"] <= 0.05 and 0.25 <= g5["A"] <= 0.60
    h2_signo = g5["x"] > 0 and g5["A"] > 0 and res["H2"]["peor_decil"]["x"] > 0
    p(f"  H2 en rango={h2_ok}; signo={h2_signo}")
    res["H2"]["en_rango"] = h2_ok
    res["H2"]["signo"] = h2_signo

    # ---------------- H3 (diario)
    p("\n[H3] caidas diarias por ventana (^SP500TR diario; FX = FIX mismo dia y, contraste, MXN=X)")
    res["H3"] = {}
    ventanas = {"crisis_fin": (date(2007, 7, 1), date(2009, 12, 31)),
                "anio_2008": (date(2007, 12, 31), date(2008, 12, 31)),
                "2020": (date(2020, 1, 1), date(2020, 12, 31)),
                "2022": (date(2022, 1, 1), date(2022, 12, 31))}
    episodios = {"Lehman": (date(2008, 9, 12), date(2009, 3, 9)), "COVID": (date(2020, 2, 19), date(2020, 3, 23))}

    def diario(fxserie, activo=sptr_d):
        # niveles diarios en USD, MXN sin cubrir, MXN cubierto (renovado a diario)
        fechas, usd, mxn, cub = [], [], [], []
        vc = None
        prev = None
        for f, v in activo:
            if f < date(1994, 1, 3) or f > date(2026, 7, 31):
                continue
            fx = ultimo_leq(fxserie, f)
            if fx is None:
                continue
            ym = (f.year, f.month)
            if prev is None:
                vc = v * fx[1]
            else:
                pf, pv, pfx = prev
                r = v / pv - 1
                x = fx[1] / pfx - 1
                dias = (f - pf).days
                c = cetes_m.get(ant(ym), 0) * 12 / 360 * dias
                rf = rfus_m.get(ant(ym), 0) * 12 / 360 * dias
                fd = (1 + c) / (1 + rf) - 1
                u = (1 + r) * (1 + x) - 1
                vc = vc * (1 + u - (x - fd))
            fechas.append(f)
            usd.append(v)
            mxn.append(v * fx[1])
            cub.append(vc)
            prev = (f, v, fx[1])
        return fechas, usd, mxn, cub

    for fxn, fxs in (("FIX", fix_d), ("MXN=X", mxnx_d), ("DEXMXUS", dex_d)):
        fe, us, mx, cu = diario(fxs)
        res["H3"][fxn] = {}
        for vn, (a, b) in ventanas.items():
            ix = [i for i, f in enumerate(fe) if a <= f <= b]
            if not ix:
                continue
            ff = sub(fe, ix)
            out = {}
            for sn, niv in (("USD", sub(us, ix)), ("MXN", sub(mx, ix)), ("MXN_cub", sub(cu, ix))):
                dd, pf, vf = mdd_fechas(ff, niv)
                out[sn] = {"mdd": dd, "pico": str(pf), "valle": vf.isoformat()}
            res["H3"][fxn][vn] = out
            p(f"  {fxn:7s} {vn:10s} USD {out['USD']['mdd']*100:6.1f} ({out['USD']['pico']}->{out['USD']['valle']})"
              f"  MXN {out['MXN']['mdd']*100:6.1f} ({out['MXN']['pico']}->{out['MXN']['valle']})"
              f"  MXNcub {out['MXN_cub']['mdd']*100:6.1f}")
        for en, (a, b) in episodios.items():
            ia = max(i for i, f in enumerate(fe) if f <= a)
            ib = max(i for i, f in enumerate(fe) if f <= b)
            ch = {s: niv[ib] / niv[ia] - 1 for s, niv in (("USD", us), ("MXN", mx), ("MXN_cub", cu))}
            res["H3"][fxn]["ep_" + en] = ch
            p(f"  {fxn:7s} episodio {en:6s} {fe[ia]}->{fe[ib]}: USD {ch['USD']*100:6.1f}  MXN {ch['MXN']*100:6.1f}  MXNcub {ch['MXN_cub']*100:6.1f}")
    h3 = res["H3"]["FIX"]
    gap = {v: (h3[v]["MXN"]["mdd"] - h3[v]["USD"]["mdd"]) * 100 for v in ventanas}
    h3_refutada = gap["crisis_fin"] < 5 or gap["2020"] < 5
    h3_ok = gap["crisis_fin"] >= 10 and gap["2020"] >= 10 and gap["2022"] <= 5
    p(f"  Ventaja MXN sobre USD (pp, FIX): {', '.join(f'{k}={v:.1f}' for k, v in gap.items())}")
    p(f"  H3 refutada={h3_refutada}; cumple completa={h3_ok}")
    res["H3"]["ventaja_pp_FIX"] = gap
    res["H3"]["refutada"] = h3_refutada
    res["H3"]["cumple"] = h3_ok

    # ---------------- H4
    p("\n[H4] volatilidad y caida por razon de cobertura (neto)")
    res["H4"] = {}
    for sn in seg:
        vols = [M[f"mxn_h{int(h*100):03d}"][sn]["vol"] for h in hs_fijas]
        mdds = [M[f"mxn_h{int(h*100):03d}"][sn]["mdd"] for h in hs_fijas]
        res["H4"][sn] = {"vols": vols, "mdds": mdds}
        p(f"  {sn:9s} vol h=0..1: {' '.join(f'{v*100:6.2f}' for v in vols)} | MDD: {' '.join(f'{v*100:6.1f}' for v in mdds)}")
    def dvol(a, b):
        return vol_anual(a) - vol_anual(b)
    for sn in ("completo", "fuera", "dentro"):
        a = sub(netas["mxn_h100"], seg[sn])
        b = sub(netas["mxn_h000"], seg[sn])
        ic = ic_boot(dvol, [a, b])
        res["H4"][sn]["dvol"] = dvol(a, b)
        res["H4"][sn]["dvol_ic95"] = ic
        p(f"  {sn:9s} vol(h=1)-vol(h=0) = {dvol(a,b)*100:5.2f} pp  IC95 [{ic[0]*100:.2f}, {ic[1]*100:.2f}]")
    hm = {sn: h_minvar(d, idx) for sn, idx in seg.items()}
    res["H4"]["h_minvar"] = hm
    p(f"  h minima varianza (sin recortar): " + ", ".join(f"{k}={v:.3f}" for k, v in hm.items()))
    h4_refutada = res["H4"]["completo"]["dvol"] <= 0 or res["H4"]["fuera"]["dvol"] <= 0
    vc = res["H4"]["completo"]["vols"]
    h4_partes = {
        "dvol>=1pp_completo": res["H4"]["completo"]["dvol"] >= 0.01,
        "dvol>=1pp_dentro": res["H4"]["dentro"]["dvol"] >= 0.01,
        "dvol>=1pp_fuera": res["H4"]["fuera"]["dvol"] >= 0.01,
        "mdd_h1_peor_5pp_completo": (res["H4"]["completo"]["mdds"][0] - res["H4"]["completo"]["mdds"][4]) >= 0.05,
        "mdd_h1_peor_5pp_fuera": (res["H4"]["fuera"]["mdds"][0] - res["H4"]["fuera"]["mdds"][4]) >= 0.05,
        "vol_monotona_completo": all(vc[i] < vc[i + 1] for i in range(4)),
        "hminvar_completo<=0.25": hm["completo"] <= 0.25,
    }
    res["H4"]["refutada"] = h4_refutada
    res["H4"]["partes"] = h4_partes
    p(f"  H4 refutada (nucleo)={h4_refutada}; partes: {h4_partes}")

    # ---------------- H5
    p("\n[H5] costo de no cubrir")
    fx_ = [a - b for a, b in zip(R1, d["U"])]
    res["H5"] = {}
    for sn, idx in seg.items():
        tnw, tiid = nw_t_media(sub(fx_, idx))
        dc = M["mxn_h100"][sn]["cagr"] - M["mxn_h000"][sn]["cagr"]
        res["H5"][sn] = {"dCAGR": dc, "media_f_menos_x_mensual": media(sub(fx_, idx)), "t_nw": tnw, "t_iid": tiid}
        p(f"  {sn:9s} CAGR(h1)-CAGR(h0)={dc*100:6.2f} pp; media(f-x)={media(sub(fx_, idx))*100:6.3f}%/mes (x12={media(sub(fx_, idx))*1200:5.2f}) tNW={tnw:5.2f} tIID={tiid:5.2f}")
    h5_ok = 0.005 <= res["H5"]["completo"]["dCAGR"] <= 0.04
    res["H5"]["cumple"] = h5_ok
    p(f"  H5 cumple={h5_ok}")

    # ---------------- H6
    p("\n[H6] benchmark 50/50 (acciones EUA + CETES)")
    res["H6"] = {}
    for sn in seg:
        a, b = M["bench50_h000"][sn], M["bench50_h100"][sn]
        res["H6"][sn] = {"vol_h0": a["vol"], "vol_h1": b["vol"], "mdd_h0": a["mdd"], "mdd_h1": b["mdd"],
                         "cagr_h0": a["cagr"], "cagr_h1": b["cagr"]}
        p(f"  {sn:9s} vol h0={a['vol']*100:5.2f} h1={b['vol']*100:5.2f} | MDD h0={a['mdd']*100:6.1f} h1={b['mdd']*100:6.1f} | CAGR h0={a['cagr']*100:5.2f} h1={b['cagr']*100:5.2f}")
    h6_ok = all(res["H6"][s]["vol_h0"] < res["H6"][s]["vol_h1"] and res["H6"][s]["mdd_h0"] > res["H6"][s]["mdd_h1"]
                for s in ("completo", "fuera"))
    h6_fuera = res["H6"]["fuera"]["vol_h0"] < res["H6"]["fuera"]["vol_h1"] and res["H6"]["fuera"]["mdd_h0"] > res["H6"]["fuera"]["mdd_h1"]
    res["H6"]["cumple"] = h6_ok
    res["H6"]["cumple_fuera"] = h6_fuera
    p(f"  H6 cumple (completo y fuera)={h6_ok}; fuera={h6_fuera}")

    # ---------------- H7
    p("\n[H7] minima varianza expansiva (min 36 meses, recorte [0,1])")
    hv = sorted(hexp[36:])
    red = M["mxn_h000"]["fuera"]["vol"] - M["mxn_hminvar_exp36"]["fuera"]["vol"]
    dmdd = M["mxn_h000"]["fuera"]["mdd"] - M["mxn_hminvar_exp36"]["fuera"]["mdd"]
    hfuera = [hexp[i] for i in seg["fuera"]]
    res["H7"] = {"h_min": hv[0], "h_mediana": hv[len(hv) // 2], "h_max": hv[-1],
                 "h_media_fuera": media(hfuera), "reduccion_vol_fuera": red, "empeora_mdd_fuera": dmdd,
                 "cumple": red < 0.005}
    p(f"  h: min={hv[0]:.3f} mediana={hv[len(hv)//2]:.3f} max={hv[-1]:.3f}; media fuera={media(hfuera):.3f}")
    p(f"  reduccion vol fuera vs h0 = {red*100:.2f} pp; MDD(h0)-MDD(P6) fuera = {dmdd*100:.2f} pp")
    p(f"  H7 cumple (no reduce >=0.5 pp)={red < 0.005}; P6 adoptable={red >= 0.005 and dmdd <= 0.02}")

    # ---------------- contrastes de fuente
    p("\n[Contrastes de fuente] corr(R,x), vol h0/h1, dvol, dCAGR")
    res["contrastes"] = {}
    alt = {
        "B_principal(SP500TR,FIX,INTG,TB3MS)": (R, S_fix, cetes_m, rfus_m, todos_meses),
        "FX=DEXMXUS": (R, S_dex, cetes_m, rfus_m, todos_meses),
        "CETES=Banxico28": (R, S_fix, cet28_m, rfus_m, todos_meses),
        "FIX_2004-01+": (R, S_fix, cetes_m, rfus_m, list(meses((2004, 1), FIN))),
        "FX=MXN=X_2004-01+": (R, S_mxnx, cetes_m, rfus_m, list(meses((2004, 1), FIN))),
    }
    for an, args in alt.items():
        dd_, falt = construir(*args)
        sg = segmentos(dd_)
        fila = {}
        for sn, idx in sg.items():
            if not idx:
                continue
            u = con_costo_entrada(sub(dd_["U"], idx))
            h1 = con_costo_entrada(sub(cubierta(dd_, 1.0), idx))
            fila[sn] = {"corr": corr(sub(dd_["R"], idx), sub(dd_["x"], idx)), "vol_h0": vol_anual(u), "vol_h1": vol_anual(h1),
                        "cagr_h0": cagr(u), "cagr_h1": cagr(h1), "mdd_h0": mdd(u), "mdd_h1": mdd(h1), "n": len(idx)}
            p(f"  {an:36s} {sn:9s} n={len(idx):3d} corr={fila[sn]['corr']:6.3f} vol0={fila[sn]['vol_h0']*100:5.2f} vol1={fila[sn]['vol_h1']*100:5.2f} "
              f"dvol={(fila[sn]['vol_h1']-fila[sn]['vol_h0'])*100:5.2f} dCAGR={(fila[sn]['cagr_h1']-fila[sn]['cagr_h0'])*100:5.2f}")
        fila["faltantes"] = [list(f) for f in falt]
        res["contrastes"][an] = fila

    # ---------------- S3b cifras del capitulo (^GSPC precio x DEXMXUS), descriptivo
    p("\n[S3b] capitulo 16: ^GSPC precio x DEXMXUS; corr con dln(USD/MXN); vol; CAGR")
    res["S3b"] = {}
    for vn, ini in (("1996-2026", (1996, 1)), ("2008-2026", (2008, 1)), ("2016-2026", (2016, 1)), ("2023-2026", (2023, 1))):
        ms = [ym for ym in meses(ini, FIN) if ym in Rp and ant(ym) in Rp and ym in S_dex and ant(ym) in S_dex]
        rp = [Rp[ym] / Rp[ant(ym)] - 1 for ym in ms]
        lx = [math.log(S_dex[ym] / S_dex[ant(ym)]) for ym in ms]
        um = [(1 + a) * math.exp(b) - 1 for a, b in zip(rp, lx)]
        fila = {"corr": corr(rp, lx), "vol_usd": vol_anual(rp), "vol_mxn": vol_anual(um), "cagr_usd": cagr(rp), "cagr_mxn": cagr(um)}
        res["S3b"][vn] = fila
        p(f"  {vn}: corr={fila['corr']:.3f} vol USD={fila['vol_usd']*100:.1f} MXN={fila['vol_mxn']*100:.1f} CAGR USD={fila['cagr_usd']*100:.2f} MXN={fila['cagr_mxn']*100:.2f}")
    ms = [ym for ym in meses((1996, 1), FIN) if ym in Rp and ant(ym) in Rp and ym in S_dex and ant(ym) in S_dex]
    rp = [Rp[ym] / Rp[ant(ym)] - 1 for ym in ms]
    xx = [S_dex[ym] / S_dex[ant(ym)] - 1 for ym in ms]
    ix = [i for i in range(len(rp)) if rp[i] < -0.05]
    a3 = {"n": len(ix), "R": media(sub(rp, ix)), "x": media(sub(xx, ix)),
          "U": media([(1 + rp[i]) * (1 + xx[i]) - 1 for i in ix])}
    res["S3b"]["A3"] = a3
    p(f"  A3 (1996-2026, ^GSPC<-5%): n={a3['n']} R={a3['R']*100:.1f} x={a3['x']*100:.1f} U={a3['U']*100:.1f}")
    fe, us, mx, _ = diario(dex_d, gspc_d)
    for vn, (a, b) in (("2007-2009", (date(2007, 1, 1), date(2009, 12, 31))), ("2020", ventanas["2020"]), ("2022", ventanas["2022"])):
        ixx = [i for i, f in enumerate(fe) if a <= f <= b]
        du = mdd_fechas(sub(fe, ixx), sub(us, ixx))[0]
        dm = mdd_fechas(sub(fe, ixx), sub(mx, ixx))[0]
        res["S3b"]["A4_" + vn] = {"usd": du, "mxn": dm}
        p(f"  A4 {vn}: MDD USD={du*100:.1f} MXN={dm*100:.1f}")

    # ---------------- estado y conclusion operable (reglas pre-registradas)
    p("\n[Veredicto con criterios pre-registrados]")
    if h1_refutada or h4_refutada:
        estado = "No replicado"
    else:
        estado = "Replicado con diferencias (como maximo; 'Replicado' exige ademas tolerancias S3b)"
    fuera_ok = {
        "H1_fuera": res["H1"]["fuera"]["corr"] < 0 and res["H1"]["fuera"]["ic95"][1] < 0,
        "H3_crisis_y_2020": not h3_refutada,
        "H4_fuera": res["H4"]["fuera"]["dvol"] > 0,
        "H6_fuera": h6_fuera,
    }
    parc = {}
    for h in (0.25, 0.5):
        k = f"mxn_h{int(h*100):03d}"
        parc[k] = M[k]["fuera"]["vol"] < M["mxn_h000"]["fuera"]["vol"] and M[k]["fuera"]["mdd"] > M["mxn_h000"]["fuera"]["mdd"]
    h5c = res["H5"]["completo"]
    modif_h5 = h5c["dCAGR"] > 0.03 and h5c["t_nw"] >= 2
    confirma = all(fuera_ok.values())
    if h4_refutada and confirma:
        concl = ("CONFLICTO de reglas del pre-registro: las cuatro condiciones de 'se confirma' se cumplen fuera de muestra "
                 "(no cubrir), pero 'se descarta si se refuta H4' se activa porque vol(h=1) <= vol(h=0) en la muestra completa. "
                 "Lectura fuera de muestra: no cubrir; lectura literal de refutacion: se descarta")
    elif h4_refutada:
        concl = "Se descarta (H4 refutada)"
    elif confirma and not any(parc.values()) and not modif_h5:
        concl = "Se confirma: no cubrir acciones de EUA"
    elif any(parc.values()) or modif_h5:
        concl = "Se modifica"
    else:
        concl = "No se confirma (alguna condicion fuera de muestra falla)"
    res["veredicto"] = {"estado": estado, "condiciones_fuera": fuera_ok, "parcial_domina_h0_fuera": parc,
                        "modifica_por_H5": modif_h5, "conclusion_operable": concl}
    p(f"  Estado: {estado}")
    p(f"  Condiciones fuera de muestra: {fuera_ok}")
    p(f"  Cobertura parcial domina a h0 fuera: {parc}; modifica por H5: {modif_h5}")
    p(f"  Conclusion operable: {concl}")

    (DIR / "salida.txt").write_text("\n".join(salida_lineas) + "\n", encoding="utf-8")
    (DIR / "resultados.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str), encoding="utf-8")


if __name__ == "__main__":
    main()
