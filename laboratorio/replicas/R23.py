"""R23 (ejecución A): ¿aporta el último UPRO (13.5%) frente a no tenerlo (U0), con el UPRO realista y con la deriva
del S&P como variable? Pre-registro: R23-u0-contra-u13-upro-real.md (mismo commit, antes de correr).
Datos: los de R18/R21 (cachés de R16 y R12, 1990-2026) y el UPRO real de R20 (R20-datos/series.json, 2009-2026).
Reproduce: python3 laboratorio/replicas/R23.py"""
import hashlib, json, math, os, sys
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import R16, R18  # noqa: E402

PESO_U13 = 0.135
WQ = 0.268                       # QQQM fijo, como en R18
WC_R18 = 0.053                   # efectivo de R18
TRAMOS_A = [(-1, 0.5, 1.31), (0.5, 3.0, 1.54), (3.0, 99, 2.30)]   # brecha R20-A por tramo de DTB3, pp/año
MUS = [0.05, 0.07, 0.09, 0.11, 0.13]   # CAGR nominal objetivo del S&P TR en el contrafactual de deriva
NIVELES, H = (0.12, 0.20), 126
INI_REAL = "2009-06-29"          # primer cierre completo del UPRO en R20


def brecha_diaria(rf_dia):
    tasa = rf_dia * 252 * 100
    return next(b for lo, hi, b in TRAMOS_A if lo <= tasa < hi) / 100 / 252


def base(D, ndx):
    """Filas (fecha, r_spx_bruto, r_ndx_bruto, rf, señal) alineadas como en R21."""
    fechas, px, op, lo, tr, vix, rf = D
    sen = R16.filtro(px, vix)
    out = []
    for i in range(2, len(fechas)):
        d, d0 = fechas[i], fechas[i - 1]
        if d not in ndx or d0 not in ndx or sen[i - 2] is None:
            continue
        out.append((d, tr[i] / tr[i - 1] - 1, ndx[d] / ndx[d0] - 1, rf[i], sen[i - 2]))
    return out


def desplazamiento(filas, mu):
    """δ diario tal que el CAGR del S&P TR desplazado en la muestra sea mu (bisección)."""
    n = len(filas)
    def cagr_con(delta):
        acc = 0.0
        for _, r1, *_ in filas:
            acc += math.log(1 + r1 + delta)
        return math.exp(acc * 252 / n) - 1
    a, b = -0.002, 0.002
    for _ in range(60):
        m = (a + b) / 2
        if cagr_con(m) < mu: a = m
        else: b = m
    return (a + b) / 2


def rendimientos(filas, delta=0.0, upro_real=None):
    """(fecha, r_spym, r_qqqm, r_upro, rf). UPRO = sintético con brecha por tramos, o el real si se pasa la serie."""
    out = []
    for d, r1, rq, rf, s in filas:
        r1d, rqd = r1 + delta, rq + delta
        if upro_real is not None:
            if d not in upro_real: continue
            ru = upro_real[d]
        else:
            ru = 3 * r1d - 2 * rf - R18.GASTO_UPRO - brecha_diaria(rf)
        out.append((d, r1d - R18.GASTO_SPYM, rqd - R18.GASTO_QQQM, ru if s == 1 else rf, rf))
    return out


def curva(R, ws, wq, wu, wc):
    eq, v, mes = [1.0], [ws, wq, wu, wc], None
    for d, rs, rq, ru, rf in R:
        if d[:7] != mes:
            tot = sum(v); v = [tot * ws, tot * wq, tot * wu, tot * wc]; mes = d[:7]
        v = [v[0] * (1 + rs), v[1] * (1 + rq), v[2] * (1 + ru), v[3] * (1 + rf)]
        eq.append(sum(v))
    return eq


def prob(eq, nivel, H):
    n = toques = 0
    for t in range(0, len(eq) - H):
        pico = eq[t]
        for k in range(t + 1, t + H + 1):
            pico = max(pico, eq[k])
            if eq[k] / pico - 1 <= -nivel:
                toques += 1; break
        n += 1
    return toques / n


def mdd(eq):
    pico, peor = eq[0], 0.0
    for x in eq:
        pico = max(pico, x); peor = min(peor, x / pico - 1)
    return peor


def metricas(R):
    """Tres carteras: U0-efectivo (comité W44: el 13.5% va a efectivo), U0-SPYM (convención R18) y U13.5."""
    n = len(R); out = {}
    carteras = {"U0-efectivo": (1 - WQ - WC_R18 - PESO_U13, WQ, 0.0, WC_R18 + PESO_U13),
                "U0-SPYM": (1 - WQ - WC_R18, WQ, 0.0, WC_R18),
                "U13.5": (1 - WQ - WC_R18 - PESO_U13, WQ, PESO_U13, WC_R18)}
    for nom, w in carteras.items():
        eq = curva(R, *w)
        fila = {"CAGR_pct": round(((eq[-1] / eq[0]) ** (252 / n) - 1) * 100, 3), "MDD_pct": round(mdd(eq) * 100, 2)}
        for nv in NIVELES:
            fila[f"P{int(nv*100)}_{H}d"] = round(prob(eq, nv, H) * 100, 2)
        out[nom] = fila
    out["dCAGR_U13_menos_U0efectivo_pp"] = round(out["U13.5"]["CAGR_pct"] - out["U0-efectivo"]["CAGR_pct"], 3)
    out["dP12_U13_menos_U0efectivo_pp"] = round(out["U13.5"][f"P12_{H}d"] - out["U0-efectivo"][f"P12_{H}d"], 2)
    out["n_dias"] = n; out["periodo"] = [R[0][0], R[-1][0]]
    return out


def cargar_upro_real():
    raw = open(os.path.join(BASE, "R20-datos", "series.json"), "rb").read()
    s = json.loads(raw)["UPRO"]
    px = {d: v for d, v in s}
    fechas = sorted(px)
    r = {fechas[i]: px[fechas[i]] / px[fechas[i - 1]] - 1 for i in range(1, len(fechas)) if fechas[i] >= INI_REAL}
    return r, hashlib.sha256(raw).hexdigest()


if __name__ == "__main__":
    D, ndx, sha16 = R18.cargar()
    filas = base(D, ndx)
    upro, sha20 = cargar_upro_real()
    res = {"sha256_r16": sha16, "sha256_r20_datos": sha20}
    # 1) histórico 1990-2026, sintético con brecha, sin desplazar
    res["historico_sintetico_brecha"] = metricas(rendimientos(filas))
    spx_cagr = math.exp(sum(math.log(1 + r1) for _, r1, *_ in filas) * 252 / len(filas)) - 1
    rf_media = sum(f[3] for f in filas) / len(filas) * 252
    res["spx_tr_cagr_muestra_pct"] = round(spx_cagr * 100, 3); res["rf_media_pct"] = round(rf_media * 100, 3)
    # 2) contrafactual de deriva: δ tal que el CAGR del S&P TR = μ
    res["contrafactual_deriva"] = {}
    for mu in MUS:
        delta = desplazamiento(filas, mu)
        m = metricas(rendimientos(filas, delta))
        m["delta_diario"] = delta
        res["contrafactual_deriva"][f"mu_{int(mu*100)}"] = m
    # μ* de empate (ΔCAGR = 0) por bisección entre 3% y 15%
    def dcagr(mu):
        return metricas(rendimientos(filas, desplazamiento(filas, mu)))["dCAGR_U13_menos_U0efectivo_pp"]
    a, b = 0.03, 0.15
    for _ in range(25):
        m = (a + b) / 2
        if dcagr(m) < 0: a = m
        else: b = m
    res["mu_empate_pct"] = round((a + b) / 2 * 100, 2)
    # 3) fuera de muestra 2009-2026 con el UPRO real, y el sintético con brecha en la misma ventana
    filas_09 = [f for f in filas if f[0] >= INI_REAL]
    res["fuera_de_muestra_upro_real"] = metricas(rendimientos(filas_09, upro_real=upro))
    R_sint = rendimientos(filas_09)
    fechas_real = set(r[0] for r in rendimientos(filas_09, upro_real=upro))
    res["fuera_de_muestra_sintetico_brecha"] = metricas([r for r in R_sint if r[0] in fechas_real])
    # hipótesis
    h7 = res["contrafactual_deriva"]["mu_7"]
    res["H1_mu7_dCAGR_pp"] = h7["dCAGR_U13_menos_U0efectivo_pp"]; res["H1_mu7_dP12_pp"] = h7["dP12_U13_menos_U0efectivo_pp"]
    res["H1_objecion_se_sostiene"] = (h7["dCAGR_U13_menos_U0efectivo_pp"] < 0.30) or (h7["dP12_U13_menos_U0efectivo_pp"] > 3.0)
    res["H2_sostenida"] = 6.0 <= res["mu_empate_pct"] <= 12.0
    fr = res["fuera_de_muestra_upro_real"]; fs = res["fuera_de_muestra_sintetico_brecha"]
    res["H3_dCAGR_real_pp"] = fr["dCAGR_U13_menos_U0efectivo_pp"]; res["H3_dP12_real_pp"] = fr["dP12_U13_menos_U0efectivo_pp"]
    res["H3_sostenida"] = fr["dCAGR_U13_menos_U0efectivo_pp"] > 1.0 and fr["dP12_U13_menos_U0efectivo_pp"] >= 3.0
    res["H4_real_vs_sintetico_dCAGR_pp"] = round(fr["U13.5"]["CAGR_pct"] - fs["U13.5"]["CAGR_pct"], 3)
    res["H4_sostenida"] = abs(res["H4_real_vs_sintetico_dCAGR_pp"]) <= 0.50
    print(json.dumps(res, indent=1, ensure_ascii=False))
    json.dump(res, open(os.path.join(BASE, "R23-resultados.json"), "w"), indent=1, ensure_ascii=False)
