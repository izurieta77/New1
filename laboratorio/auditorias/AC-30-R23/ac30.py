#!/usr/bin/env python3
"""AC-30 · Ejecución B independiente de R23 (U0 contra U13.5).

Código escrito desde cero por el auditor-de-replicas. No importa ni lee
R16.py, R18.py, R21.py ni R23.py. Solo biblioteca estándar.

Reglas tomadas de los pre-registros (.md) de R16/R18/R20/R21/R23:
- Filtro V0: señal sobre ^GSPC (cierre) y ^VIX: entra si GSPC > SMA200 y VIX < 25;
  sale si GSPC < SMA200*0.97 o VIX >= 25; si no, mantiene. Señal del cierre t-2
  aplicada al rendimiento del día t (cierre t, ejecución al cierre t+1).
- UPRO sintético (filtro encendido): 3*r_TR - 2*rf - 0.91%/252 - brecha(DTB3)/252,
  brecha por tramos de R20-A: DTB3 < 0.5%: 1.31; 0.5-3%: 1.54; >= 3%: 2.30 pp/año.
  Apagado: rf. UPRO real (fuera de muestra): adjclose de R20-datos cuando está
  encendido; rf si no.
- SPYM = r_TR - 0.02%/252; QQQM = r_NDX - 0.15%/252; efectivo = rf = DTB3/100/252.
- Mezclas (QQQM 26.8% y efectivo 5.3% fijos):
  U13.5: SPYM 54.4 / QQQM 26.8 / UPRO 13.5 / efectivo 5.3
  U0-efectivo: SPYM 54.4 / QQQM 26.8 / efectivo 18.8
  U0-SPYM: SPYM 67.9 / QQQM 26.8 / efectivo 5.3
- Rebalanceo a pesos objetivo al cierre del último día hábil de cada mes
  (el primer rendimiento de cada mes se gana a pesos objetivo). Sin costos de
  operación ni impuestos.
- Métrica de toque: fracción de ventanas de 126 puntos consecutivos de la curva
  en que la curva cae >= 12% (o 20%) bajo el máximo alcanzado dentro de la ventana.
- Contrafactual: delta diaria constante sumada a r_TR y r_NDX tal que el CAGR del
  S&P TR en 1990-2026 sea mu; rf y la señal no cambian.
"""
import json, math, sys, hashlib, os
from datetime import date

BASE = "/home/user/New1/laboratorio/replicas"
F16 = os.path.join(BASE, "R16-datos", "series.json")
F12 = os.path.join(BASE, "R12-datos", "series.json")
F20 = os.path.join(BASE, "R20-datos", "series.json")

GASTO_UPRO, GASTO_SPYM, GASTO_QQQM = 0.0091, 0.0002, 0.0015
VIX_UMBRAL, SMA_N, SALIDA = 25.0, 200, 0.97
VENT, UMBRALES = 126, (0.12, 0.20)
W_QQQM, W_CASH = 0.268, 0.053
MEZCLAS = {
    # (spym, qqqm, upro, cash)
    "U0-efectivo": (0.544, 0.268, 0.000, 0.188),
    "U0-SPYM":     (0.679, 0.268, 0.000, 0.053),
    "U13.5":       (0.544, 0.268, 0.135, 0.053),
}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def d(s):
    y, m, dd = s.split("-")
    return date(int(y), int(m), int(dd))


def brecha_tramo(dtb3_pct):
    if dtb3_pct < 0.5:
        return 0.0131
    if dtb3_pct < 3.0:
        return 0.0154
    return 0.0230


def cargar():
    s16 = json.load(open(F16))
    s12 = json.load(open(F12))
    s20 = json.load(open(F20))
    gspc = {r[0]: r[1] for r in s16["^GSPC"]}
    tr = {r[0]: r[1] for r in s16["^SP500TR"]}
    vix = {r[0]: r[1] for r in s16["^VIX"]}
    ndx = {r[0]: r[1] for r in s12["^NDX"]}
    upro = {r[0]: r[1] for r in s20["UPRO"]}
    # DTB3 con el último dato hacia adelante (ffill) sobre las fechas de mercado
    dtb3_raw = sorted((r[0], r[1]) for r in s16["DTB3"] if r[1] is not None)
    fechas = sorted(set(gspc) & set(tr) & set(vix) & set(ndx))
    dtb3 = {}
    j, ult = 0, None
    for f in fechas:
        while j < len(dtb3_raw) and dtb3_raw[j][0] <= f:
            ult = dtb3_raw[j][1]
            j += 1
        dtb3[f] = ult
    fechas = [f for f in fechas if dtb3[f] is not None
              and None not in (gspc[f], tr[f], vix[f], ndx[f])]
    return fechas, gspc, tr, vix, ndx, dtb3, upro


def filtro_v0(fechas, gspc, vix):
    """Estado del filtro al cierre de cada fecha (None antes de tener SMA200)."""
    px = [gspc[f] for f in fechas]
    estado = [None] * len(fechas)
    acum = 0.0
    on = None
    for i, p in enumerate(px):
        acum += p
        if i >= SMA_N:
            acum -= px[i - SMA_N]
        if i < SMA_N - 1:
            continue
        sma = acum / SMA_N
        v = vix[fechas[i]]
        entra = p > sma and v < VIX_UMBRAL
        sale = p < sma * SALIDA or v >= VIX_UMBRAL
        if on is None:
            on = bool(entra)
        elif on and sale:
            on = False
        elif (not on) and entra:
            on = True
        estado[i] = on
    return estado


def construir_base(fechas, gspc, tr, vix, ndx, dtb3, upro):
    """Serie de días de rendimiento: cada fila t usa la señal de t-2."""
    estado = filtro_v0(fechas, gspc, vix)
    filas = []
    for t in range(2, len(fechas)):
        if estado[t - 2] is None:
            continue
        f, f0 = fechas[t], fechas[t - 1]
        filas.append({
            "fecha": f,
            "f_prev": f0,
            "on": estado[t - 2],
            "r_tr": tr[f] / tr[f0] - 1.0,
            "r_ndx": ndx[f] / ndx[f0] - 1.0,
            "rf": dtb3[f] / 100.0 / 252.0,
            "brecha": brecha_tramo(dtb3[f]) / 252.0,
            "r_upro_real": (upro[f] / upro[f0] - 1.0) if (f in upro and f0 in upro) else None,
        })
    return filas


def curva(filas, pesos, delta=0.0, upro_real=False):
    w_spym, w_qqqm, w_upro, w_cash = pesos
    V = [1.0]
    pos = [w_spym, w_qqqm, w_upro, w_cash]
    fechas = [filas[0]["f_prev"]]
    n = len(filas)
    for i, x in enumerate(filas):
        r_spym = x["r_tr"] + delta - GASTO_SPYM / 252.0
        r_qqqm = x["r_ndx"] + delta - GASTO_QQQM / 252.0
        rf = x["rf"]
        if x["on"]:
            if upro_real:
                r_upro = x["r_upro_real"]
            else:
                r_upro = 3.0 * (x["r_tr"] + delta) - 2.0 * rf - GASTO_UPRO / 252.0 - x["brecha"]
        else:
            r_upro = rf
        pos[0] *= 1.0 + r_spym
        pos[1] *= 1.0 + r_qqqm
        pos[2] *= 1.0 + r_upro
        pos[3] *= 1.0 + rf
        v = sum(pos)
        V.append(v)
        fechas.append(x["fecha"])
        # rebalanceo al cierre del último día hábil del mes
        if i + 1 < n and filas[i + 1]["fecha"][:7] != x["fecha"][:7]:
            pos = [v * w_spym, v * w_qqqm, v * w_upro, v * w_cash]
    return fechas, V


def cagr(fechas, V):
    anios = (d(fechas[-1]) - d(fechas[0])).days / 365.25
    return (V[-1] / V[0]) ** (1.0 / anios) - 1.0


def mdd(V):
    m, peor = V[0], 0.0
    for v in V:
        if v > m:
            m = v
        dd = v / m - 1.0
        if dd < peor:
            peor = dd
    return peor


def prob_toque(V, vent=VENT, umbrales=UMBRALES):
    """Fracción de ventanas de `vent` puntos consecutivos cuyo drawdown interno
    (contra el máximo dentro de la ventana) alcanza cada umbral."""
    n = len(V)
    nv = n - vent + 1
    cuenta = [0] * len(umbrales)
    for t in range(nv):
        m = V[t]
        peor = 0.0
        for s in range(t + 1, t + vent):
            v = V[s]
            if v > m:
                m = v
            else:
                dd = v / m - 1.0
                if dd < peor:
                    peor = dd
        for k, u in enumerate(umbrales):
            if peor <= -u:
                cuenta[k] += 1
    return [c / nv for c in cuenta], nv


def vol_anual(V):
    r = [V[i] / V[i - 1] - 1 for i in range(1, len(V))]
    mu = sum(r) / len(r)
    return math.sqrt(sum((x - mu) ** 2 for x in r) / (len(r) - 1) * 252)


def metricas(fechas, V):
    p, nv = prob_toque(V)
    return {"CAGR": cagr(fechas, V), "MDD": mdd(V), "P12": p[0], "P20": p[1],
            "vol": vol_anual(V), "ventanas": nv, "dias": len(V) - 1}


def cagr_tr(filas, delta):
    V = 1.0
    for x in filas:
        V *= 1.0 + x["r_tr"] + delta
    anios = (d(filas[-1]["fecha"]) - d(filas[0]["f_prev"])).days / 365.25
    return V ** (1.0 / anios) - 1.0


def delta_para_mu(filas, mu):
    lo, hi = -0.002, 0.002
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if cagr_tr(filas, mid) < mu:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def dcagr_mu(filas, mu):
    delta = delta_para_mu(filas, mu)
    c13 = cagr(*curva(filas, MEZCLAS["U13.5"], delta))
    c0 = cagr(*curva(filas, MEZCLAS["U0-efectivo"], delta))
    return c13 - c0, delta


def main():
    out = {}
    print("AC-30 · R23 ejecución B independiente")
    for p in (F16, F12, F20):
        print(f"  sha256 {os.path.relpath(p, BASE)}: {sha(p)}")
    fechas, gspc, tr, vix, ndx, dtb3, upro = cargar()
    filas = construir_base(fechas, gspc, tr, vix, ndx, dtb3, upro)
    print(f"Fechas comunes (GSPC, TR, VIX, NDX, DTB3): {len(fechas)} de {fechas[0]} a {fechas[-1]}")
    print(f"Días de rendimiento con señal: {len(filas)} de {filas[0]['fecha']} a {filas[-1]['fecha']}"
          f" (curva arranca en {filas[0]['f_prev']})")
    n_on = sum(1 for x in filas if x["on"])
    print(f"Filtro V0 encendido: {n_on} días ({100*n_on/len(filas):.1f}%)")
    rf_med = sum(x["rf"] for x in filas) / len(filas) * 252
    print(f"rf medio muestral (DTB3): {100*rf_med:.3f}%  CAGR S&P TR muestral: {100*cagr_tr(filas, 0.0):.3f}%")
    out["muestra"] = {"dias": len(filas), "inicio": filas[0]["f_prev"], "fin": filas[-1]["fecha"],
                      "rf_medio": rf_med, "cagr_sp_tr": cagr_tr(filas, 0.0), "dias_on": n_on}

    # (1) 1990-2026 sintético con brecha
    print("\n(1) 1990-2026, 3x sintético con brecha por tramos de R20-A")
    print(f"{'mezcla':12s} {'CAGR':>8s} {'MDD':>8s} {'P(-12%)':>8s} {'P(-20%)':>8s} {'vol':>7s} {'vent':>6s}")
    out["hist"] = {}
    for nom, w in MEZCLAS.items():
        m = metricas(*curva(filas, w))
        out["hist"][nom] = m
        print(f"{nom:12s} {100*m['CAGR']:8.3f} {100*m['MDD']:8.2f} {100*m['P12']:8.2f} {100*m['P20']:8.2f} {100*m['vol']:7.2f} {m['ventanas']:6d}")
    h = out["hist"]
    print(f"Δ(U13.5 − U0-efectivo): CAGR {100*(h['U13.5']['CAGR']-h['U0-efectivo']['CAGR']):+.3f} pp; "
          f"P(−12%) {100*(h['U13.5']['P12']-h['U0-efectivo']['P12']):+.2f} pp; "
          f"P(−20%) {100*(h['U13.5']['P20']-h['U0-efectivo']['P20']):+.2f} pp")
    print(f"Δ(U13.5 − U0-SPYM):     CAGR {100*(h['U13.5']['CAGR']-h['U0-SPYM']['CAGR']):+.3f} pp; "
          f"P(−12%) {100*(h['U13.5']['P12']-h['U0-SPYM']['P12']):+.2f} pp")

    # (2) contrafactual de deriva
    print("\n(2) Contrafactual de deriva (δ diaria constante en r_TR y r_NDX; rf fijo; señal fija)")
    print(f"{'μ':>5s} {'δ×252':>7s} {'mezcla':12s} {'CAGR':>8s} {'MDD':>8s} {'P(-12%)':>8s} {'P(-20%)':>8s}  ΔCAGR / ΔP12 / ΔP20 vs U0-efectivo")
    out["mu"] = {}
    for mu in (0.05, 0.07, 0.09, 0.11, 0.13):
        delta = delta_para_mu(filas, mu)
        res = {}
        for nom, w in MEZCLAS.items():
            res[nom] = metricas(*curva(filas, w, delta))
        res["delta"] = delta
        res["cagr_tr_check"] = cagr_tr(filas, delta)
        out["mu"][f"{int(round(mu*100))}"] = res
        for nom in MEZCLAS:
            m = res[nom]
            extra = ""
            if nom == "U13.5":
                b = res["U0-efectivo"]
                extra = (f"  {100*(m['CAGR']-b['CAGR']):+.3f} / {100*(m['P12']-b['P12']):+.2f} / {100*(m['P20']-b['P20']):+.2f}")
            print(f"{100*mu:5.0f} {100*delta*252:7.2f} {nom:12s} {100*m['CAGR']:8.3f} {100*m['MDD']:8.2f} {100*m['P12']:8.2f} {100*m['P20']:8.2f}{extra}")
    # μ* de empate por bisección en [3%, 15%]
    lo, hi = 0.03, 0.15
    dlo, _ = dcagr_mu(filas, lo)
    dhi, _ = dcagr_mu(filas, hi)
    print(f"ΔCAGR en μ=3%: {100*dlo:+.3f} pp; en μ=15%: {100*dhi:+.3f} pp")
    mu_star = None
    if dlo * dhi < 0:
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            dm, _ = dcagr_mu(filas, mid)
            if (dm < 0) == (dlo < 0):
                lo, dlo = mid, dm
            else:
                hi, dhi = mid, dm
            if hi - lo < 1e-5:
                break
        mu_star = 0.5 * (lo + hi)
        print(f"μ* de empate (ΔCAGR = 0): {100*mu_star:.3f}%")
    else:
        print("Sin cambio de signo en [3%, 15%]: μ* fuera del rango")
    out["mu_star"] = mu_star

    # (3) fuera de muestra con UPRO real
    print("\n(3) Fuera de muestra 2009-06-29 → fin de la caché, UPRO real (adjclose) contra sintético+brecha")
    oos = [x for x in filas if x["fecha"] >= "2009-06-29" and x["r_upro_real"] is not None]
    # Comprobación de continuidad: todas las fechas desde 2009-06-29 deben tener UPRO
    faltan = [x["fecha"] for x in filas if x["fecha"] >= "2009-06-29" and x["r_upro_real"] is None]
    print(f"Días OOS: {len(oos)} de {oos[0]['fecha']} a {oos[-1]['fecha']} (curva arranca {oos[0]['f_prev']}); sin UPRO: {len(faltan)}")
    n_on = sum(1 for x in oos if x["on"])
    print(f"Filtro encendido en OOS: {n_on} días ({100*n_on/len(oos):.1f}%); CAGR S&P TR OOS: {100*cagr_tr(oos, 0.0):.3f}%")
    out["oos"] = {"dias": len(oos), "inicio": oos[0]["f_prev"], "fin": oos[-1]["fecha"], "real": {}, "sint": {}}
    print(f"{'modo':10s} {'mezcla':12s} {'CAGR':>8s} {'MDD':>8s} {'P(-12%)':>8s} {'P(-20%)':>8s} {'vol':>7s}")
    for modo, real in (("real", True), ("sintético", False)):
        for nom, w in MEZCLAS.items():
            m = metricas(*curva(oos, w, 0.0, upro_real=real))
            out["oos"]["real" if real else "sint"][nom] = m
            print(f"{modo:10s} {nom:12s} {100*m['CAGR']:8.3f} {100*m['MDD']:8.2f} {100*m['P12']:8.2f} {100*m['P20']:8.2f} {100*m['vol']:7.2f}")
    R, S = out["oos"]["real"], out["oos"]["sint"]
    d_cagr_oos = R["U13.5"]["CAGR"] - R["U0-efectivo"]["CAGR"]
    d_p12_oos = R["U13.5"]["P12"] - R["U0-efectivo"]["P12"]
    d_h4 = R["U13.5"]["CAGR"] - S["U13.5"]["CAGR"]
    print(f"UPRO real: Δ(U13.5 − U0-efectivo) CAGR {100*d_cagr_oos:+.3f} pp; P(−12%) {100*d_p12_oos:+.2f} pp; "
          f"P(−20%) {100*(R['U13.5']['P20']-R['U0-efectivo']['P20']):+.2f} pp")
    print(f"H4: CAGR U13.5 real − sintético+brecha = {100*d_h4:+.3f} pp")
    # UPRO solo, informativo: brecha real-sintético en la ventana OOS
    V_r = [1.0]; V_s = [1.0]; sum_gap = 0.0
    for x in oos:
        rs = 3.0 * x["r_tr"] - 2.0 * x["rf"] - GASTO_UPRO / 252.0
        V_r.append(V_r[-1] * (1 + x["r_upro_real"])); V_s.append(V_s[-1] * (1 + rs))
        sum_gap += x["r_upro_real"] - rs
    print(f"Control UPRO real vs sintético sin brecha (sin filtro), OOS: brecha aritmética {100*sum_gap/len(oos)*252:+.3f} pp/año")

    # Veredictos
    m7 = out["mu"]["7"]
    d7 = m7["U13.5"]["CAGR"] - m7["U0-efectivo"]["CAGR"]
    p7 = m7["U13.5"]["P12"] - m7["U0-efectivo"]["P12"]
    H1 = (d7 < 0.0030) or (p7 > 0.030)
    H2 = mu_star is not None and 0.06 <= mu_star <= 0.12
    H3 = (d_cagr_oos > 0.010) and (d_p12_oos >= 0.030)
    H4 = abs(d_h4) <= 0.0050
    print("\nVEREDICTOS")
    print(f"H1 (μ=7%: ΔCAGR {100*d7:+.3f} pp < 0.30 o ΔP(−12%) {100*p7:+.2f} pp > 3.0): {'SOSTENIDA' if H1 else 'REFUTADA'}")
    print(f"H2 (μ* = {('%.2f%%' % (100*mu_star)) if mu_star is not None else 'n/d'} en [6%, 12%]): {'SOSTENIDA' if H2 else 'REFUTADA'}")
    print(f"H3 (OOS real: ΔCAGR {100*d_cagr_oos:+.3f} > 1.0 y ΔP(−12%) {100*d_p12_oos:+.2f} ≥ 3.0): {'SOSTENIDA' if H3 else 'REFUTADA'}")
    print(f"H4 (|real − sintético| = {100*abs(d_h4):.3f} pp ≤ 0.50): {'SOSTENIDA' if H4 else 'REFUTADA'}")
    out["veredictos"] = {"H1": H1, "H2": H2, "H3": H3, "H4": H4,
                         "dcagr_mu7": d7, "dp12_mu7": p7, "dcagr_oos": d_cagr_oos, "dp12_oos": d_p12_oos, "h4_diff": d_h4}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
