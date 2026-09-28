"""AC-06: segunda ejecucion independiente de R05 (Moreira y Muir 2017; critica de Cederburg et al. 2020).

Codigo escrito desde cero (solo biblioteca estandar de Python 3.11). No importa ni copia R05.py.
De herramientas/datos.py solo se usan los parsers genericos de Yahoo y FRED.

Fuente principal B (distinta de A, que usa French/CRSP):
  * Diario: ^SP500TR de Yahoo (desde 1988-01-04) para la varianza realizada desde 1988-02;
    ^GSPC de Yahoo (precio, desde 1927-12-30) antes.
  * Mensual: ^SP500TR fin de mes desde 1988-02; antes, ^GSPC fin de mes + dividendo de Shiller
    (D anualizado / 12 sobre el precio del fin de mes previo).
  * Efectivo: rendimiento de la T-bill del mes t = tasa del mes t-1 / 1200. TB3MS (FRED) desde 1934-01;
    antes, NBER M1329AUSM193NNBR (FRED, bonos/letras del Tesoro de 3-6 meses, 1920-1934).
Control C (misma logica, datos French 202608) para separar el efecto de la ventana del de la fuente.

Uso: python3 laboratorio/auditorias/AC-06-volatilidad-gestionada/AC06.py   (sin red; lee datos/)
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import sys
import zipfile
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(RAIZ))
from herramientas.datos import parsear_fred_csv, parsear_yahoo_json  # noqa: E402

DATOS = AQUI / "datos"
COMISION, SPREAD = 0.0029, 0.0005          # GBM por lado (hecho) + spread (supuesto)
COSTO = COMISION + SPREAD
ULTIMO_MES = (2026, 8)                     # ultimo mes completo (Yahoo llega a 2026-09-28; TB3MS a 2026-08)

salida: list[str] = []


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    salida.append(s)


# ------------------------------------------------------------------ utilidades de meses

def mes(d: date) -> tuple[int, int]:
    return (d.year, d.month)


def mes_ant(m):
    return (m[0] - 1, 12) if m[1] == 1 else (m[0], m[1] - 1)


def mes_sig(m):
    return (m[0] + 1, 1) if m[1] == 12 else (m[0], m[1] + 1)


def rango(m0, m1):
    out, m = [], m0
    while m <= m1:
        out.append(m)
        m = mes_sig(m)
    return out


def txt(m):
    return f"{m[0]}-{m[1]:02d}"


# ------------------------------------------------------------------ estadistica

def media(x):
    return sum(x) / len(x)


def sd(x):
    mu = media(x)
    return math.sqrt(sum((v - mu) ** 2 for v in x) / (len(x) - 1))


def sharpe(ex):
    return media(ex) / sd(ex) * math.sqrt(12)


def ols(y, x, nw_lags=12):
    """MCO y = a + b x. Devuelve a, b, t IID, t HC0, t NW(L) de a y b, R2, sd residual."""
    n = len(y)
    mx, my = media(x), media(y)
    sxx = sum((v - mx) ** 2 for v in x)
    b = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / sxx
    a = my - b * mx
    e = [yi - a - b * xi for xi, yi in zip(x, y)]
    s2 = sum(v * v for v in e) / (n - 2)
    # (X'X)^-1
    sx, sxx0 = sum(x), sum(v * v for v in x)
    det = n * sxx0 - sx * sx
    inv = [[sxx0 / det, -sx / det], [-sx / det, n / det]]
    se_iid = [math.sqrt(s2 * inv[0][0]), math.sqrt(s2 * inv[1][1])]

    def sandwich(L):
        # S = sum_t e_t^2 z z' + sum_l w_l sum_t e_t e_{t-l} (z_t z_{t-l}' + z_{t-l} z_t')
        S = [[0.0, 0.0], [0.0, 0.0]]
        z = [(1.0, xi) for xi in x]
        for t in range(n):
            for i in range(2):
                for j in range(2):
                    S[i][j] += e[t] * e[t] * z[t][i] * z[t][j]
        for l in range(1, L + 1):
            w = 1 - l / (L + 1)
            for t in range(l, n):
                ee = e[t] * e[t - l]
                for i in range(2):
                    for j in range(2):
                        S[i][j] += w * ee * (z[t][i] * z[t - l][j] + z[t - l][i] * z[t][j])
        # V = inv S inv
        V = [[sum(inv[i][k] * S[k][m] * inv[m][j] for k in range(2) for m in range(2))
              for j in range(2)] for i in range(2)]
        return [math.sqrt(V[0][0]), math.sqrt(V[1][1])]

    se_hc0 = sandwich(0)
    se_nw = sandwich(nw_lags)
    r2 = 1 - sum(v * v for v in e) / sum((yi - my) ** 2 for yi in y)
    return {"a": a, "b": b, "t_iid": a / se_iid[0], "t_hc0": a / se_hc0[0], "t_nw": a / se_nw[0],
            "se_b_iid": se_iid[1], "r2": r2, "sd_e": math.sqrt(s2), "n": n}


def norm_cdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def jkm_p(ex1, ex2):
    """p bilateral de Jobson-Korkie con correccion de Memmel (Sharpe mensuales)."""
    n = len(ex1)
    s1, s2 = media(ex1) / sd(ex1), media(ex2) / sd(ex2)
    m1, m2 = media(ex1), media(ex2)
    cov = sum((a - m1) * (b - m2) for a, b in zip(ex1, ex2)) / (n - 1)
    rho = cov / (sd(ex1) * sd(ex2))
    v = (2 - 2 * rho + 0.5 * (s1 ** 2 + s2 ** 2 - 2 * s1 * s2 * rho ** 2)) / n
    z = (s1 - s2) / math.sqrt(v)
    return 2 * (1 - norm_cdf(abs(z)))


def percentil(x, q):
    s = sorted(x)
    k = (len(s) - 1) * q
    f = math.floor(k)
    c = min(f + 1, len(s) - 1)
    return s[f] + (s[c] - s[f]) * (k - f)


# ------------------------------------------------------------------ carga de datos

def sha(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def cargar_yahoo(nombre):
    serie = parsear_yahoo_json((DATOS / nombre).read_text(encoding="utf-8"))["serie"]
    return [(f, v) for f, v in serie]


def cargar_fred(nombre):
    return parsear_fred_csv((DATOS / nombre).read_text(encoding="utf-8"))


def cargar_shiller():
    out = {}
    with open(DATOS / "shiller_datahub.csv", encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            d = date.fromisoformat(fila["Date"])
            dv = float(fila["Dividend"])
            if dv > 0:
                out[mes(d)] = dv
    return out


def cargar_french(nombre, diario):
    z = zipfile.ZipFile(DATOS / nombre)
    texto = z.read(z.namelist()[0]).decode("latin1")
    lineas = texto.splitlines()
    version = lineas[0].strip()
    out = {}
    for ln in lineas:
        partes = [s.strip() for s in ln.split(",")]
        if len(partes) < 5 or not partes[0].isdigit():
            continue
        if diario and len(partes[0]) == 8:
            out[date(int(partes[0][:4]), int(partes[0][4:6]), int(partes[0][6:]))] = (
                float(partes[1]) / 100, float(partes[4]) / 100)
        elif not diario and len(partes[0]) == 6:
            k = (int(partes[0][:4]), int(partes[0][4:]))
            if k in out:          # la tabla anual viene despues; solo la primera (mensual)
                continue
            out[k] = (float(partes[1]) / 100, float(partes[4]) / 100)
    return version, out


def rv_mm_por_mes(diarios_por_mes):
    """RV2_MM(t) = sum (d_j - media)^2 sobre los J_t dias del mes."""
    rv2 = {}
    for m, rs in diarios_por_mes.items():
        if len(rs) < 15:
            raise SystemExit(f"Mes {txt(m)} con {len(rs)} dias (<15): alto")
        mu = media(rs)
        v = sum((r - mu) ** 2 for r in rs)
        if v <= 0:
            raise SystemExit(f"RV2 = 0 en {txt(m)}: alto")
        rv2[m] = v
    return rv2


def construir_B():
    gspc = [(f, v) for f, v in cargar_yahoo("yahoo_GSPC_1d.json") if mes(f) <= ULTIMO_MES]
    sptr = [(f, v) for f, v in cargar_yahoo("yahoo_SP500TR_1d.json") if mes(f) <= ULTIMO_MES]
    shiller = cargar_shiller()
    tb3 = {mes(f): v for f, v in cargar_fred("fred_TB3MS.csv")}
    nber = {mes(f): v for f, v in cargar_fred("fred_M1329AUSM193NNBR.csv")}

    def tasa(m):
        if m >= (1934, 1):
            return tb3[m]
        return nber[m]

    # diarios -> rendimientos por mes
    def por_mes(serie):
        d = {}
        for (f0, v0), (f1, v1) in zip(serie, serie[1:]):
            d.setdefault(mes(f1), []).append(v1 / v0 - 1)
        return d

    d_gspc = por_mes(gspc)
    d_sptr = por_mes(sptr)
    d_gspc.pop((1927, 12), None)
    diarios = {}
    for m in d_gspc:
        if m >= (1988, 2):
            diarios[m] = d_sptr[m]
        else:
            diarios[m] = d_gspc[m]
    rv2 = rv_mm_por_mes(diarios)
    rv2_gspc = rv_mm_por_mes(d_gspc)

    # fin de mes
    def fin_mes(serie):
        d = {}
        for f, v in serie:
            d[mes(f)] = v            # el ultimo del mes queda
        return d

    pf, tf = fin_mes(gspc), fin_mes(sptr)
    R, RF, fuente = {}, {}, {}
    for m in rango((1928, 1), ULTIMO_MES):
        ma = mes_ant(m)
        if m >= (1988, 2):
            R[m] = tf[m] / tf[ma] - 1
            fuente[m] = "SP500TR"
        else:
            R[m] = pf[m] / pf[ma] - 1 + shiller[m] / 12 / pf[ma]
            fuente[m] = "GSPC+Shiller"
        RF[m] = tasa(ma) / 1200
    # control: GSPC+Shiller frente a SP500TR en el traslape (1988-02 a 2023-06)
    dif = []
    for m in rango((1988, 2), (2023, 6)):
        if m in shiller:
            r_alt = pf[m] / pf[mes_ant(m)] - 1 + shiller[m] / 12 / pf[mes_ant(m)]
            dif.append(R[m] - r_alt)
    return R, RF, rv2, rv2_gspc, dif, fuente


def construir_French():
    vd, d = cargar_french("french_F-F_Research_Data_Factors_daily_CSV.zip", True)
    vm, mth = cargar_french("french_F-F_Research_Data_Factors_CSV.zip", False)
    diarios = {}
    for f, (mx, rf) in sorted(d.items()):
        diarios.setdefault(mes(f), []).append(mx)
    rv2 = rv_mm_por_mes(diarios)
    R = {m: mx + rf for m, (mx, rf) in mth.items()}
    RF = {m: rf for m, (mx, rf) in mth.items()}
    return vd, vm, R, RF, rv2


# ------------------------------------------------------------------ parte A: estadistica de MM

def estadistica_mm(R, RF, rv2, m0, m1, c_fija=None, etiqueta=""):
    meses = [m for m in rango(m0, m1) if m in R and mes_ant(m) in rv2]
    f = [R[m] - RF[m] for m in meses]
    g = [fi / rv2[mes_ant(m)] for fi, m in zip(f, meses)]
    c = c_fija if c_fija is not None else sd(f) / sd(g)
    fs = [c * v for v in g]
    reg = ols(fs, f)
    pesos = [c / rv2[mes_ant(m)] for m in meses]
    res = {
        "ventana": f"{txt(meses[0])} a {txt(meses[-1])}", "N": len(meses), "c": c,
        "alfa_anual_pct": reg["a"] * 1200, "t_iid": reg["t_iid"], "t_hc0": reg["t_hc0"],
        "t_nw12": reg["t_nw"], "beta": reg["b"], "R2": reg["r2"],
        "AR": reg["a"] / reg["sd_e"] * math.sqrt(12),
        "sharpe_mercado": sharpe(f), "sharpe_gestionada": sharpe(fs),
        "p_jkm": jkm_p(fs, f),
        "peso_P50": percentil(pesos, .5), "peso_P99": percentil(pesos, .99),
    }
    p(f"  [{etiqueta}] {res['ventana']} N={res['N']}  alfa={res['alfa_anual_pct']:.2f}%/a "
      f"t_IID={res['t_iid']:.2f} t_HC0={res['t_hc0']:.2f} t_NW12={res['t_nw12']:.2f} "
      f"beta={res['beta']:.3f} R2={res['R2']:.3f} AR={res['AR']:.3f}")
    p(f"      Sharpe mercado={res['sharpe_mercado']:.3f} gestionada={res['sharpe_gestionada']:.3f} "
      f"(dif {res['sharpe_gestionada'] - res['sharpe_mercado']:+.3f}, p JKM={res['p_jkm']:.2f})  "
      f"pesos P50={res['peso_P50']:.2f} P99={res['peso_P99']:.2f}")
    return res


# ------------------------------------------------------------------ parte C: vol_c1 operable

def backtest_vol_c1(R, RF, rv2, primer_s, min_ent=120, tope=1.0, usar_var=False):
    """w_t = min(tope, k_t / RV(t-1)) con k_t de ventana expansiva s <= t-1; costos por |w_t - w_pre_t|."""
    meses_s = [m for m in sorted(R) if m >= primer_s and mes_ant(m) in rv2]
    senal = (lambda m: rv2[m]) if usar_var else (lambda m: math.sqrt(rv2[m]))
    filas = []
    w_prev, w_pre = 0.0, 0.0          # exposicion inicial 0: se paga la entrada
    bh_prev = 0.0
    for i, m in enumerate(meses_s):
        if i < min_ent:
            continue
        ent = meses_s[:i]            # s <= t-1
        f_e = [R[s] - RF[s] for s in ent]
        g_e = [fe / senal(mes_ant(s)) for fe, s in zip(f_e, ent)]
        k = sd(f_e) / sd(g_e)
        w = min(tope, max(0.0, k / senal(mes_ant(m))))
        costo = abs(w - w_pre) * COSTO
        r_bruto = w * R[m] + (1 - w) * RF[m]
        r_neto = r_bruto - costo
        bh_costo = abs(1.0 - bh_prev) * COSTO
        bh_neto = R[m] - bh_costo
        filas.append({"mes": m, "w": w, "w_pre": w_pre, "rotacion": abs(w - w_pre), "r_neto": r_neto,
                      "r_bruto": r_bruto, "bh_neto": bh_neto, "rf": RF[m], "mkt": R[m]})
        # peso a la deriva al final del mes
        vr, vc = w * (1 + R[m]), (1 - w) * (1 + RF[m])
        w_pre = vr / (vr + vc) if vr + vc > 0 else 0.0
        bh_prev = 1.0
    return filas


def metricas(filas, m0, m1, clave):
    fs = [f for f in filas if m0 <= f["mes"] <= m1]
    r = [f[clave] for f in fs]
    ex = [f[clave] - f["rf"] for f in fs]
    v, pico, mdd = 1.0, 1.0, 0.0
    for x in r:
        v *= 1 + x
        pico = max(pico, v)
        mdd = min(mdd, v / pico - 1)
    anios = len(r) / 12
    return {"ventana": f"{txt(fs[0]['mes'])} a {txt(fs[-1]['mes'])}", "N": len(r),
            "CAGR_pct": (v ** (1 / anios) - 1) * 100, "vol_pct": sd(r) * math.sqrt(12) * 100,
            "sharpe": sharpe(ex), "MDD_pct": mdd * 100}


def alfa_estrategia(filas, m0, m1):
    fs = [f for f in filas if m0 <= f["mes"] <= m1]
    y = [f["r_neto"] - f["rf"] for f in fs]
    x = [f["mkt"] - f["rf"] for f in fs]
    reg = ols(y, x)
    return {"alfa_anual_pct": reg["a"] * 1200, "t_iid": reg["t_iid"], "t_hc0": reg["t_hc0"],
            "t_nw12": reg["t_nw"], "beta": reg["b"]}


def reporte_operable(nombre, filas, cortes):
    out = {}
    for etiqueta, (m0, m1) in cortes.items():
        a = metricas(filas, m0, m1, "r_neto")
        b = metricas(filas, m0, m1, "bh_neto")
        al = alfa_estrategia(filas, m0, m1)
        fs = [f for f in filas if m0 <= f["mes"] <= m1]
        rot = media([f["rotacion"] for f in fs])
        w_m = media([f["w"] for f in fs])
        costo_anual = rot * COSTO * 12 * 100
        n_ops = sum(1 for f in fs if f["rotacion"] > 1e-9)
        p(f"  [{nombre} | {etiqueta}] {a['ventana']} N={a['N']}")
        p(f"      vol_c1 neto : CAGR={a['CAGR_pct']:.2f}% vol={a['vol_pct']:.2f}% Sharpe={a['sharpe']:.3f} "
          f"MDD={a['MDD_pct']:.1f}%   w medio={w_m:.3f} rotacion media={rot:.4f}/mes "
          f"costo≈{costo_anual:.2f}%/a  meses con operacion={n_ops}")
        p(f"      comprar/mantener: CAGR={b['CAGR_pct']:.2f}% vol={b['vol_pct']:.2f}% Sharpe={b['sharpe']:.3f} "
          f"MDD={b['MDD_pct']:.1f}%")
        p(f"      alfa vol_c1 vs mercado: {al['alfa_anual_pct']:.2f}%/a t_IID={al['t_iid']:.2f} "
          f"t_HC0={al['t_hc0']:.2f} t_NW12={al['t_nw12']:.2f} beta={al['beta']:.3f}")
        out[etiqueta] = {"vol_c1": a, "comprar_y_mantener": b, "alfa_vs_mercado": al,
                         "w_medio": w_m, "rotacion_media_mes": rot, "costo_anual_pct": costo_anual,
                         "meses_con_operacion": n_ops}
    return out


# ------------------------------------------------------------------ principal

def main():
    resultados = {"fecha_corrida": "2026-09-28", "costos_por_lado": COSTO, "archivos": {}}
    p("AC-06: segunda ejecucion independiente de R05 (volatilidad gestionada, mercado de EUA)")
    p("=" * 100)
    for ruta in sorted(DATOS.iterdir()):
        if ruta.name == "SHA256SUMS.txt":
            continue
        h = sha(ruta)
        resultados["archivos"][ruta.name] = h
        p(f"  sha256 {ruta.name}: {h}")
    (DATOS / "SHA256SUMS.txt").write_text(
        "".join(f"{h}  {n}\n" for n, h in resultados["archivos"].items()), encoding="utf-8")

    R, RF, rv2, rv2_gspc, dif, fuente = construir_B()
    p("")
    p(f"B: meses con rendimiento {txt(min(R))} a {txt(max(R))}; RV2 {txt(min(rv2))} a {txt(max(rv2))}")
    p(f"Control de dividendos (SP500TR - [GSPC+Shiller], 1988-02 a 2023-06, N={len(dif)}): "
      f"media {media(dif) * 1200:+.3f} pp/a, sd {sd(dif) * 100:.3f} pp/mes")
    vd, vm, RFr, RFrf, rv2F = construir_French()
    p(f"French (control C): diario '{vd}' / mensual '{vm}'")
    resultados["control_dividendos"] = {"N": len(dif), "media_pp_anual": media(dif) * 1200,
                                        "sd_pp_mes": sd(dif) * 100}

    # ---------------- parte A
    p("")
    p("PARTE A: estadistica de MM (c de toda la ventana; look-ahead a proposito; no es estrategia)")
    A = {}
    A["B_articulo"] = estadistica_mm(R, RF, rv2, (1928, 2), (2015, 12), etiqueta="B ventana articulo")
    A["C_French_misma_ventana"] = estadistica_mm(RFr, RFrf, rv2F, (1928, 2), (2015, 12),
                                                 etiqueta="C French 1928-02")
    A["C_French_ventana_MM"] = estadistica_mm(RFr, RFrf, rv2F, (1926, 8), (2015, 12),
                                              etiqueta="C French 1926-08")
    A["B_solo_GSPC_RV"] = estadistica_mm(R, RF, rv2_gspc, (1928, 2), (2015, 12),
                                         etiqueta="B con RV de ^GSPC en todo el periodo")
    A["B_1988_2015"] = estadistica_mm(R, RF, rv2, (1988, 2), (2015, 12), etiqueta="B solo SP500TR 1988-02")
    A["B_1938_2015"] = estadistica_mm(R, RF, rv2, (1938, 1), (2015, 12), etiqueta="B sin 1928-1937")
    p("")
    p("H2: despues de publicarse, c fija de la ventana del articulo")
    cB = A["B_articulo"]["c"]
    cF = A["C_French_ventana_MM"]["c"]
    A["B_post"] = estadistica_mm(R, RF, rv2, (2017, 8), ULTIMO_MES, c_fija=cB, etiqueta="B post 2017-08")
    A["B_post_a_2026_07"] = estadistica_mm(R, RF, rv2, (2017, 8), (2026, 7), c_fija=cB,
                                           etiqueta="B post a 2026-07")
    A["C_French_post"] = estadistica_mm(RFr, RFrf, rv2F, (2017, 8), ULTIMO_MES, c_fija=cF,
                                        etiqueta="C French post")
    A["B_2016_ult"] = estadistica_mm(R, RF, rv2, (2016, 1), ULTIMO_MES, c_fija=cB, etiqueta="B 2016-01 a ult")
    resultados["parte_A"] = A

    # ---------------- parte C: vol_c1
    p("")
    p(f"PARTE C: vol_c1 operable, w=min(1, k_t/RV(t-1)), k_t expansivo (>=120 meses), costo {COSTO * 100:.2f}% por lado")
    filasB = backtest_vol_c1(R, RF, rv2, (1928, 2))
    filasF = backtest_vol_c1(RFr, RFrf, rv2F, (1926, 8))
    cortesB = {"dentro_muestra": (filasB[0]["mes"], (2015, 12)),
               "fuera_muestra": ((2017, 8), ULTIMO_MES),
               "fuera_muestra_a_2026_07": ((2017, 8), (2026, 7)),
               "total": (filasB[0]["mes"], ULTIMO_MES)}
    cortesF = {"dentro_muestra_1936_08": ((1936, 8), (2015, 12)),
               "dentro_muestra_1938_02": ((1938, 2), (2015, 12)),
               "fuera_muestra": ((2017, 8), ULTIMO_MES),
               "fuera_muestra_a_2026_07": ((2017, 8), (2026, 7))}
    C = {"B": reporte_operable("B", filasB, cortesB), "C_French": reporte_operable("C French", filasF, cortesF)}
    p("")
    p("Sensibilidad: var_c1 (min(1, c_t/RV2)) en B")
    filasBv = backtest_vol_c1(R, RF, rv2, (1928, 2), usar_var=True)
    C["B_var_c1"] = reporte_operable("B var_c1", filasBv, {"dentro_muestra": cortesB["dentro_muestra"],
                                                          "fuera_muestra": cortesB["fuera_muestra"]})
    resultados["parte_C"] = C

    # ---------------- veredictos mecanicos (criterios del pre-registro)
    p("")
    p("VEREDICTOS (criterios del pre-registro de R05 aplicados a B)")
    a = A["B_articulo"]
    h1 = "Replicado" if (a["t_hc0"] >= 2 and 3.30 <= a["alfa_anual_pct"] <= 6.42) else (
        "Replicado con diferencias" if a["t_hc0"] >= 2 and a["alfa_anual_pct"] > 0 else "No replicado")
    b = A["B_post"]
    h2 = "se sostiene" if (b["alfa_anual_pct"] > 0 and b["sharpe_gestionada"] > b["sharpe_mercado"]) else "refutada"
    dm, fm = C["B"]["dentro_muestra"], C["B"]["fuera_muestra"]
    h4 = ("agrega valor" if fm["vol_c1"]["sharpe"] > fm["comprar_y_mantener"]["sharpe"]
          and abs(fm["vol_c1"]["MDD_pct"]) < abs(fm["comprar_y_mantener"]["MDD_pct"]) else "refutada (Sharpe neto OOS <= B&H o MDD no menor)")
    freno = (abs(fm["vol_c1"]["MDD_pct"]) < abs(fm["comprar_y_mantener"]["MDD_pct"]) or
             abs(dm["vol_c1"]["MDD_pct"]) < abs(dm["comprar_y_mantener"]["MDD_pct"]))
    p(f"  H1 (alfa en ventana del articulo): {h1}")
    p(f"  H2 (post 2017-08): {h2}")
    p(f"  H4 (vol_c1 contra comprar y mantener, OOS): {h4}")
    p(f"  Uso como freno (MDD menor en OOS o en dentro de muestra): {'se sostiene' if freno else 'refutado'}")
    alfa3 = dm["alfa_vs_mercado"]["t_hc0"] >= 3 and fm["alfa_vs_mercado"]["t_hc0"] >= 3
    p(f"  Alfa operable con t>=3 dentro y fuera: {'si' if alfa3 else 'no'}")
    resultados["veredictos"] = {"H1": h1, "H2": h2, "H4": h4, "freno": freno, "alfa_t3": alfa3}

    (AQUI / "salida.txt").write_text("\n".join(salida) + "\n", encoding="utf-8")

    def limpiar(o):
        if isinstance(o, dict):
            return {str(k): limpiar(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [limpiar(v) for v in o]
        if isinstance(o, float):
            return round(o, 6)
        return o
    (AQUI / "resultados.json").write_text(json.dumps(limpiar(resultados), indent=1, ensure_ascii=False),
                                          encoding="utf-8")


if __name__ == "__main__":
    main()
