#!/usr/bin/env python3
"""AC-27-R20: ejecución B independiente de la réplica R20.

Brecha diaria entre UPRO real (con distribuciones) y un 3x sintético:
    sint_t = 3*r_idx_t - 2*tasa_t - 0.0091/252
Periodo de rendimientos: 2009-06-26 -> 2026-10-23 (inclusive).

Escrito desde cero (solo biblioteca estándar), sin leer R20.py.
Fuentes:
  - Yahoo chart v8: UPRO, ^SP500TR, SPY (events=div|split) -> datos/yahoo_*.json
  - FRED fredgraph.csv: DTB3, DFF -> datos/fred_*.csv
Uso:
  python3 ac27_r20.py            # usa la caché de datos/ si existe; si no, descarga
  python3 ac27_r20.py --descargar
"""
import csv
import datetime as dt
import hashlib
import json
import math
import os
import sys
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
INICIO = dt.date(2009, 6, 26)   # primer rendimiento
FIN = dt.date(2026, 10, 23)     # último rendimiento
GASTO = 0.0091
ER_SPY = 0.000945               # gasto de SPY, se suma de vuelta en la variante SPY
P1, P2 = 1243296000, 1793404800  # 2009-05-26 .. 2026-10-31


# ------------------------------------------------------------------ descarga
def _get(url, ua):
    hdr = {"User-Agent": "Mozilla/5.0"} if ua else {}
    req = urllib.request.Request(url, headers=hdr)
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def descargar():
    os.makedirs(DATOS, exist_ok=True)
    for s, nombre in [("UPRO", "UPRO"), ("%5ESP500TR", "SP500TR"), ("SPY", "SPY"), ("%5EGSPC", "GSPC")]:
        url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{s}?period1={P1}&period2={P2}"
               "&interval=1d&events=div%7Csplit&includeAdjustedClose=true")
        open(os.path.join(DATOS, f"yahoo_{nombre}.json"), "wb").write(_get(url, True))
    for f in ("DTB3", "DFF"):
        # FRED corta la conexión con UA de navegador; se usa el UA por defecto de urllib.
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={f}"
        open(os.path.join(DATOS, f"fred_{f}.csv"), "wb").write(_get(url, False))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ------------------------------------------------------------------ lectura
def leer_yahoo(nombre):
    d = json.load(open(os.path.join(DATOS, f"yahoo_{nombre}.json")))["chart"]["result"][0]
    off = d["meta"].get("gmtoffset", -14400)
    q = d["indicators"]["quote"][0]["close"]
    adj = d["indicators"].get("adjclose", [{}])[0].get("adjclose")
    cierre, ajust, divs = {}, {}, {}
    for i, t in enumerate(d["timestamp"]):
        f = (dt.datetime.utcfromtimestamp(t + off)).date()
        if q[i] is None:
            continue
        cierre[f] = q[i]
        if adj and adj[i] is not None:
            ajust[f] = adj[i]
    for k, v in d.get("events", {}).get("dividends", {}).items():
        f = (dt.datetime.utcfromtimestamp(int(v["date"]) + off)).date()
        divs[f] = divs.get(f, 0.0) + v["amount"]
    return cierre, ajust, divs


def leer_fred(sid):
    out = {}
    with open(os.path.join(DATOS, f"fred_{sid}.csv")) as fh:
        for row in csv.DictReader(fh):
            v = row[sid].strip()
            if v in ("", "."):
                continue
            out[dt.date.fromisoformat(row["observation_date"])] = float(v) / 100.0
    return out


def asof(serie):
    """Devuelve función fecha -> último valor disponible en o antes de la fecha."""
    fechas = sorted(serie)
    import bisect

    def f(d):
        i = bisect.bisect_right(fechas, d) - 1
        if i < 0:
            raise ValueError(d)
        return serie[fechas[i]]
    return f


def rend_tr(fechas, cierre, divs):
    """Rendimiento total reconstruido: (P_t + D_t)/P_{t-1} - 1, D sumando dividendos con ex-date
    en (t-1, t]."""
    out = {}
    dfechas = sorted(divs)
    for a, b in zip(fechas[:-1], fechas[1:]):
        D = sum(divs[x] for x in dfechas if a < x <= b)
        out[b] = (cierre[b] + D) / cierre[a] - 1.0
    return out


def rend_px(fechas, px):
    return {b: px[b] / px[a] - 1.0 for a, b in zip(fechas[:-1], fechas[1:])}


# ------------------------------------------------------------------ estadística
def ols_nw(y, x, lags=6):
    """OLS y = a + b x con errores Newey-West (Bartlett). Devuelve a, b, se_a, se_b, t_a, t_b."""
    n = len(y)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((xi - mx) ** 2 for xi in x)
    b = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / sxx
    a = my - b * mx
    e = [yi - a - b * xi for xi, yi in zip(x, y)]
    # X'X
    s0, s1, s2 = n, sum(x), sum(xi * xi for xi in x)
    det = s0 * s2 - s1 * s1
    inv = [[s2 / det, -s1 / det], [-s1 / det, s0 / det]]
    # S = sum_l w_l sum_t (u_t u_{t-l}' + u_{t-l} u_t'), u_t = x_t e_t
    u = [(e[i], x[i] * e[i]) for i in range(n)]
    S = [[0.0, 0.0], [0.0, 0.0]]
    for l in range(0, lags + 1):
        w = 1.0 if l == 0 else 1.0 - l / (lags + 1.0)
        G = [[0.0, 0.0], [0.0, 0.0]]
        for t in range(l, n):
            ut, us = u[t], u[t - l]
            for i in range(2):
                for j in range(2):
                    G[i][j] += ut[i] * us[j]
        for i in range(2):
            for j in range(2):
                S[i][j] += w * (G[i][j] if l == 0 else G[i][j] + G[j][i])

    def mm(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    V = mm(mm(inv, S), inv)
    se_a, se_b = math.sqrt(V[0][0]), math.sqrt(V[1][1])
    return {"a": a, "b": b, "se_a": se_a, "se_b": se_b, "t_a": a / se_a, "t_b": b / se_b, "n": n}


def cagr(rs, d0, d1):
    v = 1.0
    for r in rs:
        v *= 1 + r
    años = ((d1 - d0).days + 1) / 365.25
    return v ** (1 / años) - 1, v


# ------------------------------------------------------------------ cálculo
def calcular(r_upro, r_idx, fechas, tasa_f, tramo_f, devengo, previa, inicio=INICIO):
    """fechas: lista de fechas de rendimiento (con su fecha anterior en fechas_prev)."""
    filas = []
    for a, b in zip(fechas[:-1], fechas[1:]):
        if b < inicio or b > FIN:
            continue
        ref = a if previa else b
        y = tasa_f(ref)
        if devengo == "252":
            fin_d = y / 252.0
        else:  # días naturales / 360
            fin_d = y * (b - a).days / 360.0
        sint = 3 * r_idx[b] - 2 * fin_d - GASTO / 252.0
        filas.append({"f": b, "g": r_upro[b] - sint, "real": r_upro[b], "sint": sint,
                      "ridx": r_idx[b], "fin_d": fin_d, "tramo_y": tramo_f(ref), "dias": (b - a).days})
    return filas


def resumir(filas, detalle=True):
    n = len(filas)
    g = [x["g"] for x in filas]
    m1 = 252 * sum(g) / n
    d0, d1 = filas[0]["f"], filas[-1]["f"]
    c_real, v_real = cagr([x["real"] for x in filas], d0, d1)
    c_sint, v_sint = cagr([x["sint"] for x in filas], d0, d1)
    out = {"n": n, "desde": str(d0), "hasta": str(d1),
           "M1_brecha_arit_pp": 100 * m1,
           "M1b_cagr_real_pct": 100 * c_real, "M1b_cagr_sint_pct": 100 * c_sint,
           "M1b_dif_pp": 100 * (c_real - c_sint),
           "multiplo_real": v_real, "multiplo_sint": v_sint}
    if not detalle:
        return out
    tramos = {"<0.5%": [], "0.5-3%": [], ">=3%": []}
    for x in filas:
        y = x["tramo_y"]
        k = "<0.5%" if y < 0.005 else ("0.5-3%" if y < 0.03 else ">=3%")
        tramos[k].append(x["g"])
    out["M2_tramos"] = {k: {"n": len(v), "brecha_pp": 100 * 252 * sum(v) / len(v) if v else None}
                        for k, v in tramos.items()}
    t = out["M2_tramos"]
    out["H2_dif_alto_menos_bajo_pp"] = t[">=3%"]["brecha_pp"] - t["<0.5%"]["brecha_pp"]
    años = {}
    for x in filas:
        años.setdefault(x["f"].year, []).append(x)
    out["M2_anual"] = {}
    for a, v in sorted(años.items()):
        gg = [x["g"] for x in v]
        out["M2_anual"][str(a)] = {"n": len(v), "brecha_pp": 100 * 252 * sum(gg) / len(gg),
                                   "tasa_media_pct": 100 * sum(x["tramo_y"] for x in v) / len(v)}
    r3 = ols_nw(g, [x["fin_d"] for x in filas], 6)
    out["M3"] = {"const_anual_pp": 100 * 252 * r3["a"], "t_const": r3["t_a"],
                 "pendiente": r3["b"], "t_pendiente": r3["t_b"],
                 "nota": "brecha_t = a + b*financiamiento_diario_t; b=0 => financiamiento escala exactamente 2x; b<0 => extra"}
    r4 = ols_nw(g, [x["ridx"] for x in filas], 6)
    out["M4"] = {"const_anual_pp": 100 * 252 * r4["a"], "pendiente": r4["b"], "t_pendiente_NW6": r4["t_b"]}
    return out


def main():
    if "--descargar" in sys.argv or not os.path.exists(os.path.join(DATOS, "fred_DFF.csv")):
        descargar()
    archivos = sorted(os.listdir(DATOS))
    hashes = {f: sha(os.path.join(DATOS, f)) for f in archivos}

    up_c, up_a, up_d = leer_yahoo("UPRO")
    tr_c, _, _ = leer_yahoo("SP500TR")
    spy_c, _, spy_d = leer_yahoo("SPY")
    dtb3, dff = leer_fred("DTB3"), leer_fred("DFF")
    f_dtb3, f_dff = asof(dtb3), asof(dff)

    # Intersección de fechas UPRO ∩ índice (incluye la fecha previa a INICIO)
    fechas = sorted(d for d in set(up_c) & set(tr_c) & set(spy_c) if d <= FIN)
    fechas = [d for d in fechas if d >= dt.date(2009, 6, 25)]
    assert fechas[0] == dt.date(2009, 6, 25), fechas[0]

    r_up_rec = rend_tr(fechas, up_c, up_d)          # UPRO reconstruido cierre + dividendos
    r_up_adj = rend_px(fechas, up_a)                # UPRO adjclose de Yahoo
    r_tr = rend_px(fechas, tr_c)                    # ^SP500TR
    r_spy = {k: v + ER_SPY / 252 for k, v in rend_tr(fechas, spy_c, spy_d).items()}  # SPY TR + gasto

    res = {"fuentes_sha256": hashes, "parametros": {"inicio": str(INICIO), "fin": str(FIN), "gasto": GASTO}}
    # Principal B: UPRO reconstruido, ^SP500TR, DFF, /252, tasa del día previo
    var = {
        "B_principal_DFF_252_rec_SP500TR": (r_up_rec, r_tr, f_dff, f_dff, "252", True),
        "DTB3_252_rec_SP500TR": (r_up_rec, r_tr, f_dtb3, f_dtb3, "252", True),
        "DTB3_252_rec_SP500TR_tasa_mismo_dia": (r_up_rec, r_tr, f_dtb3, f_dtb3, "252", False),
        "DTB3_252_adj_SP500TR_tasa_mismo_dia(=receta pre-registro)": (r_up_adj, r_tr, f_dtb3, f_dtb3, "252", False),
        "DFF_252_rec_SP500TR_tramosDTB3": (r_up_rec, r_tr, f_dff, f_dtb3, "252", True),
        "DFF_act360_rec_SP500TR": (r_up_rec, r_tr, f_dff, f_dff, "act360", True),
        "DTB3_act360_rec_SP500TR": (r_up_rec, r_tr, f_dtb3, f_dtb3, "act360", True),
        "DFF_252_rec_SPYTR": (r_up_rec, r_spy, f_dff, f_dff, "252", True),
        "DTB3_252_rec_SPYTR": (r_up_rec, r_spy, f_dtb3, f_dtb3, "252", True),
        "DFF_act360_rec_SPYTR": (r_up_rec, r_spy, f_dff, f_dff, "act360", True),
        "DTB3_252_adj_SP500TR_mismo_dia_desde_0629(=ventana efectiva de A)": (r_up_adj, r_tr, f_dtb3, f_dtb3, "252", False, dt.date(2009, 6, 29)),
    }
    res["variantes"] = {}
    for k, args in var.items():
        filas = calcular(*args[:2], fechas, *args[2:])
        res["variantes"][k] = resumir(filas)
        if k.startswith("B_principal"):
            # Diagnóstico de devengo: brecha media según días naturales del intervalo (base /252)
            dg = {}
            for x in filas:
                kk = "1 dia" if x["dias"] == 1 else (">=3 dias" if x["dias"] >= 3 else "2 dias")
                alto = "tasa>=3%" if x["tramo_y"] >= 0.03 else "tasa<3%"
                dg.setdefault(alto + " | " + kk, []).append(x["g"])
            res["diagnostico_devengo_brecha_diaria_pb"] = {kk: {"n": len(v), "media_pb_dia": 1e4 * sum(v) / len(v)}
                                                          for kk, v in sorted(dg.items())}

    # Control de construcción
    comunes = [d for d in fechas[1:] if INICIO <= d <= FIN]
    dif = [r_up_rec[d] - r_up_adj[d] for d in comunes]
    res["control_UPRO_rec_vs_adj"] = {"media_diaria_anual_pp": 100 * 252 * sum(dif) / len(dif),
                                      "max_abs": max(abs(x) for x in dif)}
    dif2 = [r_spy[d] - r_tr[d] for d in comunes]
    res["control_SPYTR_vs_SP500TR"] = {"media_diaria_anual_pp": 100 * 252 * sum(dif2) / len(dif2)}

    # Diagnóstico 1: brecha media por día de la semana (DFF, /252), por índice y régimen de tasa
    res["diagnostico_dia_semana_pb"] = {}
    for nidx, ri in (("SP500TR", r_tr), ("SPYTR", r_spy)):
        for x in calcular(r_up_rec, ri, fechas, f_dff, f_dff, "252", True):
            k = f"{nidx} | {'tasa>=3%' if x['tramo_y'] >= 0.03 else 'tasa<3%'}"
            res["diagnostico_dia_semana_pb"].setdefault(k, {}).setdefault(
                ["lun", "mar", "mie", "jue", "vie"][x["f"].weekday()], []).append(x["g"])
    for k, v in res["diagnostico_dia_semana_pb"].items():
        res["diagnostico_dia_semana_pb"][k] = {d: round(1e4 * sum(g) / len(g), 2) for d, g in v.items()}
    # Diagnóstico 2: ¿H3 es un efecto del índice? UPRO - 3*SPYTR sobre r(^SP500TR); SPYTR - SP500TR sobre r(^SP500TR)
    r_a = ols_nw([r_up_rec[d] - 3 * r_spy[d] for d in comunes], [r_tr[d] for d in comunes], 6)
    r_b = ols_nw([r_spy[d] - r_tr[d] for d in comunes], [r_tr[d] for d in comunes], 6)
    sd = math.sqrt(sum((x - sum(dif2) / len(dif2)) ** 2 for x in dif2) / len(dif2))
    res["diagnostico_H3"] = {"UPRO_menos_3SPYTR_sobre_rSP500TR": {"b": r_a["b"], "t_NW6": r_a["t_b"]},
                             "SPYTR_menos_SP500TR_sobre_rSP500TR": {"b": r_b["b"], "t_NW6": r_b["t_b"]},
                             "sd_diaria_SPYTR_menos_SP500TR_pb": 1e4 * sd}

    p = res["variantes"]["B_principal_DFF_252_rec_SP500TR"]
    q = res["variantes"]["DTB3_252_rec_SP500TR"]
    res["veredicto"] = {}
    for nombre, v in (("DFF", p), ("DTB3", q)):
        res["veredicto"][nombre] = {
            "H1 (M1 <= -0.5 pp)": v["M1_brecha_arit_pp"] <= -0.5,
            "H2 (alto - bajo <= -0.5 pp)": v["H2_dif_alto_menos_bajo_pp"] <= -0.5,
            "H3 (pendiente<0 y t_NW6 <= -2)": v["M4"]["pendiente"] < 0 and v["M4"]["t_pendiente_NW6"] <= -2,
        }
    json.dump(res, open(os.path.join(AQUI, "resultados.json"), "w"), indent=1, ensure_ascii=False, default=str)

    # Impresión resumida
    for k, v in res["variantes"].items():
        t = v["M2_tramos"]
        print(f"{k:58s} n={v['n']} M1={v['M1_brecha_arit_pp']:+.3f} M1b={v['M1b_dif_pp']:+.3f} "
              f"tramos={[None if t[x]['brecha_pp'] is None else round(t[x]['brecha_pp'], 2) for x in t]} "
              f"(n={[t[x]['n'] for x in t]}) H2dif={v['H2_dif_alto_menos_bajo_pp']:+.2f} "
              f"M3 c={v['M3']['const_anual_pp']:+.2f} b={v['M3']['pendiente']:+.3f} t={v['M3']['t_pendiente']:+.2f} "
              f"M4 b={v['M4']['pendiente']:+.5f} t={v['M4']['t_pendiente_NW6']:+.2f}")
    print("control UPRO rec-adj", res["control_UPRO_rec_vs_adj"])
    print("control SPYTR-SP500TR", res["control_SPYTR_vs_SP500TR"])
    print("diagnostico devengo", json.dumps(res["diagnostico_devengo_brecha_diaria_pb"], ensure_ascii=False))
    print("dia semana", json.dumps(res["diagnostico_dia_semana_pb"], ensure_ascii=False))
    print("diagnostico H3", json.dumps(res["diagnostico_H3"], ensure_ascii=False))
    print("veredicto", json.dumps(res["veredicto"], ensure_ascii=False))
    print("anual (principal DFF):")
    for a, v in p["M2_anual"].items():
        print(f"  {a} n={v['n']} brecha={v['brecha_pp']:+.2f} DFF={v['tasa_media_pct']:.2f}  | DTB3 brecha={q['M2_anual'][a]['brecha_pp']:+.2f}")


if __name__ == "__main__":
    main()
