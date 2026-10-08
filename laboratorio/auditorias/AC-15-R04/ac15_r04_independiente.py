#!/usr/bin/env python3
"""AC-15 / R04: re-implementacion independiente del efecto Halloween.

Escrita desde cero a partir de la especificacion de pre-registro de R04
(secciones 1 a 9 de laboratorio/replicas/R04-efecto-halloween.md).

Fuente de EUA (TERCERA fuente, distinta de French CRSP y de Yahoo ^GSPC):
  Shiller, ie_data.xls (S&P Composite mensual, precio P y dividendo 12m D),
  convertida a CSV por convertir_shiller_xls.py.
Efectivo (solo estrategias): FRED TB3MS (T-bill 3 meses, % anual, mensual).
Verificacion de alineacion (no es la serie probada): French F-F factores
  mensuales (Mkt-RF + RF), solo para comparar correlaciones por rezago.

Solo biblioteca estandar. Las regresiones, Newey-West, bootstrap y la
logica de la senal y los costos estan escritos aqui; no se importa nada
de herramientas/ ni del codigo original de R04.

Uso:
    python3 ac15_r04_independiente.py > salida.txt
"""
import csv
import hashlib
import json
import math
import os
import random
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "datos_crudos")

MES_EN_MERCADO = {11, 12, 1, 2, 3, 4}          # Halloween: noviembre a abril
COSTO_LADO = 0.0029 + 0.0005                   # comision GBM + spread por defecto
LAGS_NW = 12
INICIO_EFECTIVO = (1934, 1)                    # primer mes de TB3MS
RESULTADOS = {}


# --------------------------------------------------------------------------
# Utilidades de calendario
# --------------------------------------------------------------------------
def mi(y, m):
    """Indice entero de mes: y*12 + (m-1)."""
    return y * 12 + (m - 1)


def ym(idx):
    y, r = divmod(idx, 12)
    return y, r + 1


def fmt(idx):
    y, m = ym(idx)
    return f"{y}-{m:02d}"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 16), b""):
            h.update(bloque)
    return h.hexdigest()


# --------------------------------------------------------------------------
# Carga de datos
# --------------------------------------------------------------------------
def cargar_shiller():
    """Devuelve dict idx -> (P, D) con P y D como float o None."""
    datos = {}
    with open(os.path.join(RAW, "shiller_mensual.csv"), newline="") as f:
        for fila in csv.DictReader(f):
            idx = mi(int(fila["anio"]), int(fila["mes"]))
            P = float(fila["P"]) if fila["P"] else None
            D = float(fila["D"]) if fila["D"] else None
            datos[idx] = (P, D)
    return datos


def retornos_shiller(datos):
    """Rendimientos mensuales del mes t con precio de cierre de t y t-1.

    TR_t = (P_t + D_t/12) / P_{t-1} - 1   (D es el dividendo de 12 meses)
    PR_t = P_t / P_{t-1} - 1              (solo precio, sensibilidad)
    Se requiere P_{t-1}, P_t (y D_t para TR); si falta, el mes no entra.
    """
    tr, pr = {}, {}
    for idx in sorted(datos):
        if idx - 1 not in datos:
            continue
        P1, _ = datos[idx - 1]
        P0, D0 = datos[idx]
        if P1 is None or P0 is None:
            continue
        pr[idx] = P0 / P1 - 1.0
        if D0 is not None:
            tr[idx] = (P0 + D0 / 12.0) / P1 - 1.0
    return tr, pr


def cargar_french():
    """Mkt-RF y RF mensuales (%) de French; solo para verificacion de alineacion."""
    ruta = os.path.join(RAW, "french_factors_csv.zip")
    z = zipfile.ZipFile(ruta)
    texto = z.read(z.namelist()[0]).decode("latin-1").splitlines()
    out = {}
    for linea in texto:
        partes = [p.strip() for p in linea.split(",")]
        if len(partes) >= 5 and len(partes[0]) == 6 and partes[0].isdigit():
            y, m = int(partes[0][:4]), int(partes[0][4:])
            mkt, rf = float(partes[1]), float(partes[4])
            if mkt <= -99:
                continue
            out[mi(y, m)] = (mkt, rf)
        elif out and len(partes[0]) == 4:
            # la seccion anual empieza despues de la mensual; se detiene aqui
            break
    return out


def cargar_tbill():
    """Tasa anual (%) del T-bill a 3 meses; devuelve idx -> rf mensual simple."""
    out = {}
    with open(os.path.join(RAW, "fred_TB3MS.csv"), newline="") as f:
        for fila in csv.DictReader(f):
            if fila["TB3MS"] in ("", "."):
                continue
            y, m = int(fila["observation_date"][:4]), int(fila["observation_date"][5:7])
            out[mi(y, m)] = float(fila["TB3MS"]) / 100.0 / 12.0
    return out


# --------------------------------------------------------------------------
# Algebra lineal minima (Gauss-Jordan) y MCO con errores estandar
# --------------------------------------------------------------------------
def inversa(A):
    n = len(A)
    M = [list(map(float, A[i])) + [1.0 if i == j else 0.0 for j in range(n)]
         for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[piv][c]) < 1e-14:
            raise ValueError("matriz singular")
        M[c], M[piv] = M[piv], M[c]
        p = M[c][c]
        M[c] = [v / p for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0.0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [row[n:] for row in M]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def transpuesta(A):
    return [list(col) for col in zip(*A)]


def mco(y, X, lags=LAGS_NW):
    """MCO con errores estandar: clasico, HC1 y Newey-West (Bartlett, lags).

    La correccion n/(n-k) se aplica a HC1 y NW, como pre-registro.
    """
    n, k = len(y), len(X[0])
    Xt = transpuesta(X)
    XtX = matmul(Xt, X)
    XtX_inv = inversa(XtX)
    Xty = [[sum(Xt[i][t] * y[t] for t in range(n))] for i in range(k)]
    b = [v[0] for v in matmul(XtX_inv, Xty)]
    e = [y[t] - sum(X[t][j] * b[j] for j in range(k)) for t in range(n)]

    s2 = sum(v * v for v in e) / (n - k)
    V_cl = [[s2 * XtX_inv[i][j] for j in range(k)] for i in range(k)]

    # meat de White: sum e_t^2 x_t x_t'
    S0 = [[0.0] * k for _ in range(k)]
    for t in range(n):
        for i in range(k):
            for j in range(k):
                S0[i][j] += e[t] * e[t] * X[t][i] * X[t][j]
    corr = n / (n - k)
    V_hc = matmul(matmul(XtX_inv, S0), XtX_inv)
    V_hc = [[corr * v for v in row] for row in V_hc]

    # Newey-West: S = S0 + sum_l w_l sum_t e_t e_{t-l} (x_t x_{t-l}' + x_{t-l} x_t')
    S = [row[:] for row in S0]
    for l in range(1, lags + 1):
        w = 1.0 - l / (lags + 1.0)
        for t in range(l, n):
            c = w * e[t] * e[t - l]
            for i in range(k):
                for j in range(k):
                    S[i][j] += c * (X[t][i] * X[t - l][j] + X[t - l][i] * X[t][j])
    V_nw = matmul(matmul(XtX_inv, S), XtX_inv)
    V_nw = [[corr * v for v in row] for row in V_nw]

    def t_de(V):
        return [b[i] / math.sqrt(V[i][i]) if V[i][i] > 0 else float("nan")
                for i in range(k)]

    return {
        "n": n, "k": k, "beta": b,
        "t_mco": t_de(V_cl), "t_hc1": t_de(V_hc), "t_nw": t_de(V_nw),
        "p_nw": [math.erfc(abs(t) / math.sqrt(2)) for t in t_de(V_nw)],
    }


def p_binomial_una_cola(k, n):
    """P(X >= k) con X ~ Binomial(n, 1/2)."""
    return sum(math.comb(n, j) for j in range(k, n + 1)) / (2 ** n)


# --------------------------------------------------------------------------
# Ventanas y regresiones del efecto
# --------------------------------------------------------------------------
def serie_ventana(rend, desde, hasta):
    """Lista (idx, y) de meses contiguos con rendimiento en [desde, hasta]."""
    a, b = mi(*desde), mi(*hasta)
    out = []
    for idx in range(a, b + 1):
        if idx not in rend:
            raise ValueError(f"falta rendimiento en {fmt(idx)} dentro de la ventana")
        out.append((idx, 100.0 * math.log(1.0 + rend[idx])))
    return out


def regresion_efecto(serie, modelo="A"):
    """y_t = mu + a1*S_t (+ a2*D_t) (+ a3*Enero_t). S=1 en noviembre-abril."""
    y = [v for _, v in serie]
    X = []
    for idx, _ in serie:
        _, m = ym(idx)
        S = 1.0 if m in MES_EN_MERCADO else 0.0
        fila = [1.0, S]
        if modelo == "B":
            fila += [1.0 if ym(idx) == (1987, 10) else 0.0,
                     1.0 if ym(idx) == (1998, 8) else 0.0]
        elif modelo == "C":
            fila += [1.0 if m == 1 else 0.0]
        X.append(fila)
    r = mco(y, X)
    r["media_invierno"] = None
    inv = [v for (idx, v), fila in zip(serie, X) if fila[1] == 1.0]
    ver = [v for (idx, v), fila in zip(serie, X) if fila[1] == 0.0]
    r["media_invierno"] = sum(inv) / len(inv) if inv else float("nan")
    r["media_verano"] = sum(ver) / len(ver) if ver else float("nan")
    return r


def diferencias_anuales(serie):
    """D_Y = sum(nov Y-1 .. abr Y) - sum(may Y .. oct Y), solo anios completos."""
    val = {idx: v for idx, v in serie}
    inicio, fin = serie[0][0], serie[-1][0]
    filas = []
    for anio in range(ym(inicio)[0] + 1, ym(fin)[0] + 1):
        ini_h = mi(anio - 1, 11)
        fin_h = mi(anio, 10)
        if ini_h < inicio or fin_h > fin:
            continue
        inv = sum(val[mi(anio - 1, 11) + k] for k in range(6))   # nov..abr
        ver = sum(val[mi(anio, 5) + k] for k in range(6))        # may..oct
        filas.append((anio, inv - ver))
    return filas


def resumen_diferencias(filas):
    if not filas:
        return None
    dif = [d for _, d in filas]
    N = len(dif)
    media = sum(dif) / N
    sd = math.sqrt(sum((d - media) ** 2 for d in dif) / (N - 1)) if N > 1 else float("nan")
    t_iid = media / (sd / math.sqrt(N)) if sd > 0 else float("nan")
    rng = random.Random(4)                        # semilla del pre-registro
    boot = []
    for _ in range(10000):
        muestra = [dif[rng.randrange(N)] for _ in range(N)]
        boot.append(sum(muestra) / N)
    boot.sort()
    lo, hi = boot[int(0.025 * 10000)], boot[int(0.975 * 10000) - 1]
    pos = sum(1 for d in dif if d > 0)
    return {
        "N": N, "media": media, "t_iid": t_iid,
        "ic95": [lo, hi], "positivos": pos,
        "p_signo": p_binomial_una_cola(pos, N),
        "peor": min(filas, key=lambda x: x[1]), "mejor": max(filas, key=lambda x: x[1]),
    }


def exceso_por_mitad(rend, rf, desde, hasta):
    """Media mensual de y - 100*ln(1+rf) en invierno y verano, con t NW(12)."""
    a, b = mi(*desde), mi(*hasta)
    filas, X = [], []
    for idx in range(a, b + 1):
        _, m = ym(idx)
        ex = 100.0 * math.log(1.0 + rend[idx]) - 100.0 * math.log(1.0 + rf[idx])
        inv = 1.0 if m in MES_EN_MERCADO else 0.0
        filas.append(ex)
        X.append([inv, 1.0 - inv])                   # sin constante: dos medias
    r = mco(filas, X)
    return {"inv": r["beta"][0], "t_inv": r["t_nw"][0],
            "ver": r["beta"][1], "t_ver": r["t_nw"][1]}


# --------------------------------------------------------------------------
# Estrategias
# --------------------------------------------------------------------------
def senal_halloween(idx):
    return 1.0 if ym(idx)[1] in MES_EN_MERCADO else 0.0


def senal_sma10(indice_tr, idx):
    """1 si el nivel de t-1 supera la media de los 10 meses hasta t-1 (inclusive)."""
    if idx - 10 not in indice_tr:
        return None
    previos = [indice_tr[idx - 1 - k] for k in range(10)]
    return 1.0 if indice_tr[idx - 1] > sum(previos) / 10.0 else 0.0


def backtest(rend, rf, desde, hasta, senal, costo_lado=COSTO_LADO):
    """Exposicion w_t al mercado en el mes t; resto en efectivo.

    r_neto_t = w_t*R_t + (1-w_t)*rf_t - costo*|w_t - w_{t-1}|.
    Sin costo inicial en el primer mes de la ventana (w_{t-1} = w_t).
    """
    a, b = mi(*desde), mi(*hasta)
    rs, ex, w_prev, ops, expos = [], [], None, 0, []
    for idx in range(a, b + 1):
        w = senal(idx)
        if w is None:
            raise ValueError(f"senal no disponible en {fmt(idx)}")
        w_prev_eff = w if w_prev is None else w_prev
        c = costo_lado * abs(w - w_prev_eff)
        if w_prev is not None and w != w_prev:
            ops += 1
        r = w * rend[idx] + (1.0 - w) * rf[idx] - c
        rs.append(r)
        ex.append(r - rf[idx])
        expos.append(w)
        w_prev = w
    n = len(rs)
    anios = n / 12.0
    wealth, pico, mdd = 1.0, 1.0, 0.0
    for r in rs:
        wealth *= (1.0 + r)
        pico = max(pico, wealth)
        mdd = min(mdd, wealth / pico - 1.0)
    cagr = wealth ** (1.0 / anios) - 1.0
    media_ex = sum(ex) / n
    sd_ex = math.sqrt(sum((v - media_ex) ** 2 for v in ex) / (n - 1))
    sd_r = math.sqrt(sum((v - sum(rs) / n) ** 2 for v in rs) / (n - 1))
    return {
        "n_meses": n, "cagr": cagr,
        "vol": sd_r * math.sqrt(12),
        "sharpe": (media_ex / sd_ex) * math.sqrt(12) if sd_ex > 0 else float("nan"),
        "mdd": mdd, "ops_por_anio": ops / anios,
        "exposicion": sum(expos) / n,
        "costo_anual": sum(abs(expos[i] - (expos[i - 1] if i > 0 else expos[i]))
                           for i in range(n)) * costo_lado / anios,
    }


# --------------------------------------------------------------------------
# Programa principal
# --------------------------------------------------------------------------
VENTANAS = [
    ("completo 1926-07 a 2023-06", (1926, 7), (2023, 6)),
    ("dentro_muestra 1926-07 a 2002-12", (1926, 7), (2002, 12)),
    ("fuera_muestra 2003-01 a 2023-06", (2003, 1), (2023, 6)),
    ("pre-articulo 1926-07 a 1969-12", (1926, 7), (1969, 12)),
    ("ARTICULO 1970-01 a 1998-08", (1970, 1), (1998, 8)),
    ("hueco 1998-09 a 2002-12", (1998, 9), (2002, 12)),
    ("contraste WP1997 1973-01 a 1996-12", (1973, 1), (1996, 12)),
    ("contraste JZ-OOS 1998-09 a 2011-07", (1998, 9), (2011, 7)),
    ("extra Shiller 1872-01 a 1925-12", (1872, 1), (1925, 12)),
]


def linea_efecto(nombre, r):
    return (f"{nombre:<36} n={r['n']:>4}  a1={r['beta'][1]:>8.4f}  "
            f"t_MCO={r['t_mco'][1]:>6.2f}  t_HC1={r['t_hc1'][1]:>6.2f}  "
            f"t_NW={r['t_nw'][1]:>6.2f}  mu={r['beta'][0]:>8.4f}")


def main():
    datos = cargar_shiller()
    tr, pr = retornos_shiller(datos)
    french = cargar_french()
    rf_tb = cargar_tbill()

    ultimo_tr = max(tr)
    print("=== AC-15 / R04: replica independiente (fuente de EUA: Shiller) ===")
    print(f"Shiller: primer mes con TR {fmt(min(tr))}, ultimo {fmt(ultimo_tr)} "
          f"(D disponible hasta 2023-06; el archivo termina en 2023-09 sin D)")
    print(f"French F-F factores: {fmt(min(french))} a {fmt(max(french))}; "
          f"sha256 {sha256(os.path.join(RAW, 'french_factors_csv.zip'))[:16]}...")
    print(f"TB3MS: {fmt(min(rf_tb))} a {fmt(max(rf_tb))}; "
          f"sha256 {sha256(os.path.join(RAW, 'fred_TB3MS.csv'))[:16]}...")
    print(f"Shiller sha256 {sha256(os.path.join(RAW, 'shiller_mensual.csv'))[:16]}... "
          f"(xls: {sha256(os.path.join(RAW, 'shiller_ie_data.xls'))[:16]}...)")
    print("Costo por defecto por lado: 0.34% (0.29% GBM + 0.05% spread)")
    print()

    # ---- 1. Alineacion: Shiller TR y PR contra French Mkt total, por rezago
    print("--- 1. Verificacion de alineacion (Shiller contra French Mkt-RF+RF, 1926-07 a 2023-06) ---")
    comunes = [i for i in sorted(tr) if i in french and mi(1926, 7) <= i <= mi(2023, 6)]
    fr_tot = {i: (french[i][0] + french[i][1]) / 100.0 for i in french}

    def corr(xs, ys):
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
        sxx = sum((a - mx) ** 2 for a in xs)
        syy = sum((b - my) ** 2 for b in ys)
        return sxy / math.sqrt(sxx * syy)

    alin = {}
    for rezago in (-1, 0, 1):
        pares = [(tr[i + rezago], fr_tot[i]) for i in comunes
                 if (i + rezago) in tr and i in fr_tot]
        xs = [a for a, _ in pares]
        ys = [b for _, b in pares]
        c = corr(xs, ys)
        alin[rezago] = c
        print(f"  rezago {rezago:+d}: corr(TR_Shiller[t+{rezago}], French_t) = {c:.4f} "
              f"(n={len(pares)})")
    print(f"  media mensual TR Shiller {sum(tr[i] for i in comunes)/len(comunes)*100:.4f}% "
          f"vs French {sum(fr_tot[i] for i in comunes)/len(comunes)*100:.4f}%")
    print("  Lectura: con cierre de fin de mes, corr en rezago 0 debe ser ~0.95 o mas.")
    print("  Un promedio mensual de precios produce corr 0 y +1 cercanas a sqrt(0.5)=0.707 y corr -1 cercana a 0.")
    print(f"  Control de fecha: French Mkt-RF 1987-10 = {french[mi(1987,10)][0]:.2f}%, "
          f"1987-11 = {french[mi(1987,11)][0]:.2f}% (crac de octubre de 1987)")
    print()
    RESULTADOS["alineacion_corr"] = alin

    # ---- 1b. Prueba de contaminacion: French mezclado como si fuera promedio mensual
    print("--- 1b. Diagnostico: efecto con French mezclado de forma analoga al promedio de Shiller ---")
    print("  Serie mezclada: log(1+R_b,t) = 0.5*log(1+R_t) + 0.5*log(1+R_{t-1}) (solo diagnostico)")
    mezclado = {}
    for idx in sorted(fr_tot):
        if idx - 1 in fr_tot:
            lt = math.log(1.0 + fr_tot[idx])
            lt1 = math.log(1.0 + fr_tot[idx - 1])
            mezclado[idx] = math.exp(0.5 * lt + 0.5 * lt1) - 1.0
    for nombre, d, h in VENTANAS[1:2] + VENTANAS[4:5] + VENTANAS[2:3]:
        s_fr = serie_ventana(fr_tot, d, h)
        s_mz = serie_ventana(mezclado, max(d, (1926, 8)), h)   # mezclado empieza en 1926-08
        s_sh = serie_ventana(tr, d, h)
        rf_ = regresion_efecto(s_fr, "A")
        rm_ = regresion_efecto(s_mz, "A")
        rs_ = regresion_efecto(s_sh, "A")
        print(f"  {nombre:<36} French a1={rf_['beta'][1]:.3f} (t_NW {rf_['t_nw'][1]:.2f})  |  "
              f"French mezclado a1={rm_['beta'][1]:.3f} (t_NW {rm_['t_nw'][1]:.2f})  |  "
              f"Shiller a1={rs_['beta'][1]:.3f} (t_NW {rs_['t_nw'][1]:.2f})")
    RESULTADOS["mezclado"] = {}
    for nombre, d, h in VENTANAS[:5]:
        rm_ = regresion_efecto(serie_ventana(mezclado, max(d, (1926, 8)), h), "A")
        RESULTADOS["mezclado"][nombre] = {"a1": rm_["beta"][1], "t_nw": rm_["t_nw"][1]}
    print()

    # ---- 2. Regresiones del efecto, EUA, TR (principal) y PR (sensibilidad)
    print("--- 2. Efecto Halloween, EUA Shiller TR (modelo A: y=100ln(1+R), S=1 nov-abr) ---")
    res_tr = {}
    for nombre, d, h in VENTANAS:
        s = serie_ventana(tr, d, h)
        r = regresion_efecto(s, "A")
        res_tr[nombre] = r
        print(linea_efecto(nombre, r))
    RESULTADOS["efecto_TR"] = {k: {"a1": v["beta"][1], "mu": v["beta"][0],
                                   "t_mco": v["t_mco"][1], "t_hc1": v["t_hc1"][1],
                                   "t_nw": v["t_nw"][1], "n": v["n"],
                                   "media_inv": v["media_invierno"],
                                   "media_ver": v["media_verano"]}
                               for k, v in res_tr.items()}
    print()

    print("--- 2b. Sensibilidad: solo precio (PR, sin dividendos) ---")
    for nombre, d, h in VENTANAS[:5]:
        s = serie_ventana(pr, d, h)
        r = regresion_efecto(s, "A")
        print(linea_efecto(nombre, r))
    print()

    print("--- 2c. Sensibilidad de alineacion: S desplazado un mes (error de fecha hipotetico) ---")
    for nombre, d, h in VENTANAS[4:5]:
        a, b = mi(*d), mi(*h)
        for desfase in (-1, +1):
            y, X = [], []
            for idx in range(a, b + 1):
                _, m = ym(idx + desfase)
                S = 1.0 if m in MES_EN_MERCADO else 0.0
                y.append(100.0 * math.log(1.0 + tr[idx]))
                X.append([1.0, S])
            r = mco(y, X)
            print(f"  {nombre} con S desplazado {desfase:+d}: a1={r['beta'][1]:.4f} "
                  f"t_NW={r['t_nw'][1]:.2f}")
    print()

    print("--- 2d. Modelos B (dummies oct-1987, ago-1998) y C (+enero), TR ---")
    s = serie_ventana(tr, (1970, 1), (1998, 8))
    rb = regresion_efecto(s, "B")
    rc = regresion_efecto(s, "C")
    print(f"  B: a1={rb['beta'][1]:.4f} t_MCO={rb['t_mco'][1]:.2f} t_NW={rb['t_nw'][1]:.2f} "
          f"a2(dummy)={rb['beta'][2]:.3f}")
    print(f"  C: a1={rc['beta'][1]:.4f} t_MCO={rc['t_mco'][1]:.2f} t_NW={rc['t_nw'][1]:.2f} "
          f"a3(enero)={rc['beta'][2]:.4f}")
    RESULTADOS["articulo_B"] = {"a1": rb["beta"][1], "t_nw": rb["t_nw"][1]}
    RESULTADOS["articulo_C"] = {"a1": rc["beta"][1], "t_nw": rc["t_nw"][1]}
    print()

    print("--- 3. Diferencia anual pareada D_Y (invierno menos verano), TR ---")
    for nombre, d, h in VENTANAS[:5]:
        filas = diferencias_anuales(serie_ventana(tr, d, h))
        rs = resumen_diferencias(filas)
        if rs is None:
            continue
        print(f"  {nombre:<36} N={rs['N']:>3}  mediaD={rs['media']:>8.3f}  t_iid={rs['t_iid']:>5.2f}  "
              f"IC95=[{rs['ic95'][0]:.3f}, {rs['ic95'][1]:.3f}]  D>0={rs['positivos']}/{rs['N']}  "
              f"p_signo={rs['p_signo']:.4f}")
    print()

    print("--- 4. Exceso sobre efectivo (TB3MS desde 1934-01) por mitad del ano, TR ---")
    print("  Nota: TB3MS empieza en 1934-01; las pruebas con efectivo se recortan a ese mes.")
    for nombre, d, h in VENTANAS[:5]:
        d2 = max(d, INICIO_EFECTIVO)
        e = exceso_por_mitad(tr, rf_tb, d2, h)
        print(f"  {nombre:<36} nov-abr={e['inv']:>7.4f} (t_NW {e['t_inv']:>5.2f})  "
              f"may-oct={e['ver']:>7.4f} (t_NW {e['t_ver']:>5.2f})")
    print()

    print("--- 5. Ventanas moviles: cuando cambia la conclusion (TR) ---")
    print("  5a. Ventana creciente desde 1926-07, fin en diciembre de cada anio")
    cambios = []
    for fin in range(1950, 2024):
        hasta = (fin, 12) if fin < 2023 else (2023, 6)
        r = regresion_efecto(serie_ventana(tr, (1926, 7), hasta), "A")
        cambios.append((fin, r["beta"][1], r["t_nw"][1]))
    for fin, a1, t in cambios:
        if fin % 5 == 0 or fin == 2023:
            print(f"    fin {fin}: a1={a1:.4f}  t_NW={t:.2f}")
    RESULTADOS["expansiva_tnw"] = {str(f): t for f, _, t in cambios}
    print("  5b. Ventanas de 20 anios que empiezan en enero de cada anio")
    roll20 = []
    for ini in range(1926, 2004):
        hasta = (ini + 19, 12)
        if mi(*hasta) > mi(2023, 6):
            break
        r = regresion_efecto(serie_ventana(tr, (ini, 1), hasta), "A")
        roll20.append((ini, r["beta"][1], r["t_nw"][1]))
    for ini, a1, t in roll20:
        if ini % 5 == 1:
            print(f"    {ini}-{ini+19}: a1={a1:.4f}  t_NW={t:.2f}")
    neg = [ini for ini, a1, t in roll20 if t < 2.0]
    print(f"    ventanas de 20 anios con t_NW < 2: {len(neg)} de {len(roll20)}; "
          f"inicios: {neg[:12]}{'...' if len(neg) > 12 else ''}")
    RESULTADOS["roll20"] = [{"inicio": i, "a1": a, "t_nw": t} for i, a, t in roll20]
    print()

    print("  5c. Decadas (diagnostico)")
    decadas = [((1926, 7), (1929, 12))] + [((y, 1), (y + 9, 12)) for y in range(1930, 2020, 10)] \
        + [((2020, 1), (2023, 6))]
    for d, h in decadas:
        r = regresion_efecto(serie_ventana(tr, d, h), "A")
        print(f"    {fmt(mi(*d))} a {fmt(mi(*h))}: a1={r['beta'][1]:.4f}  t_NW={r['t_nw'][1]:.2f}  n={r['n']}")
    print()

    # ---- 6. Criterios pre-registrados (EUA), con esta fuente
    print("--- 6. Criterios pre-registrados (EUA) con la fuente Shiller TR ---")
    art = res_tr["ARTICULO 1970-01 a 1998-08"]
    dentro = res_tr["dentro_muestra 1926-07 a 2002-12"]
    fuera = res_tr["fuera_muestra 2003-01 a 2023-06"]
    c_i = (art["beta"][1] > 0) and (abs(art["beta"][1] - 1.0349) <= 0.20) and (art["t_mco"][1] >= 1.96)
    c_ii = (dentro["beta"][1] > 0) and (dentro["t_nw"][1] >= 2.0)
    c_iii = fuera["beta"][1] > 0
    print(f"  (i)   1970-01 a 1998-08: a1={art['beta'][1]:.4f} (|a1-1.0349|={abs(art['beta'][1]-1.0349):.4f}), "
          f"t_MCO={art['t_mco'][1]:.2f} -> {'CUMPLE' if c_i else 'NO CUMPLE'}")
    print(f"  (ii)  1926-07 a 2002-12: a1={dentro['beta'][1]:.4f}, t_NW={dentro['t_nw'][1]:.2f} "
          f"-> {'CUMPLE' if c_ii else 'NO CUMPLE'}")
    print(f"  (iii) 2003-01 a 2023-06: a1={fuera['beta'][1]:.4f}, t_NW={fuera['t_nw'][1]:.2f} "
          f"-> a1 > 0: {'CUMPLE' if c_iii else 'NO CUMPLE'}")
    print("  (iv)  Mexico: no se re-ejecuta con esta fuente (ver README).")
    RESULTADOS["criterios"] = {"i": c_i, "ii": c_ii, "iii": c_iii}
    print()

    # ---- 7. Estrategias, costos por defecto, fuera de muestra y dentro
    print("--- 7. Estrategias EUA Shiller (costos por defecto, cash = TB3MS) ---")
    senales = {
        "Halloween nov-abr": lambda idx: senal_halloween(idx),
        "Comprar y mantener": lambda idx: 1.0,
        "Efectivo": lambda idx: 0.0,
        "Verano may-oct": lambda idx: 1.0 - senal_halloween(idx),
        "SMA10 (nivel TR)": lambda idx: senal_sma10(indice, idx),
    }
    indice = {}
    nivel = 1.0
    for idx in sorted(tr):
        nivel *= (1.0 + tr[idx])
        indice[idx] = nivel
    # SMA10 necesita 10 meses de historia previos; el indice cubre desde el primer TR
    for nombre_ventana, d, h in [("dentro 1934-01 a 2002-12", INICIO_EFECTIVO, (2002, 12)),
                                 ("fuera 2003-01 a 2023-06", (2003, 1), (2023, 6))]:
        print(f"  {nombre_ventana}")
        for nombre, sen in senales.items():
            if nombre.startswith("SMA10"):
                def sen_ok(idx, _s=sen):
                    v = _s(idx)
                    return 0.0 if v is None else v
                senal_use = sen_ok
            else:
                senal_use = sen
            b = backtest(tr, rf_tb, d, h, senal_use)
            print(f"    {nombre:<20} CAGR={b['cagr']*100:>6.2f}%  vol={b['vol']*100:>6.2f}%  "
                  f"Sharpe={b['sharpe']:>6.3f}  MDD={b['mdd']*100:>7.2f}%  "
                  f"ops/anio={b['ops_por_anio']:>5.2f}  costo/anio={b['costo_anual']*100:>5.2f}%")
            RESULTADOS.setdefault("estrategias", {}).setdefault(nombre_ventana, {})[nombre] = b
        print()

    # Bruto (sin costo) para Halloween, referencia
    for nombre_ventana, d, h in [("fuera 2003-01 a 2023-06", (2003, 1), (2023, 6))]:
        b = backtest(tr, rf_tb, d, h, senal_halloween, costo_lado=0.0)
        print(f"  Halloween bruto ({nombre_ventana}): CAGR={b['cagr']*100:.2f}% Sharpe={b['sharpe']:.3f} "
              f"MDD={b['mdd']*100:.2f}%")

    # ---- 8. Control de codigo: misma logica con French (fuente original), fechas del original
    print("--- 8. Control de codigo: misma logica sobre French (fuente del original) ---")
    rf_fr = {idx: v[1] / 100.0 for idx, v in french.items()}
    print("  Referencia: cifras publicadas en R04-efecto-halloween.md (seccion 11), no del .py")
    referencia = {
        "dentro": {"alfa1_modelo_A_1926_2002": 0.6819, "t_nw_1926_2002": 2.07,
                   "US_nov_abr_cagr": 0.0821, "US_nov_abr_vol": 0.1253, "US_nov_abr_sharpe": 0.3962,
                   "US_nov_abr_mdd": -0.5760, "US_nov_abr_ops": 1.9955,
                   "BH_cagr": 0.0980, "BH_vol": 0.1936, "BH_sharpe": 0.3874, "BH_mdd": -0.8365},
        "fuera": {"US_nov_abr_cagr": 0.0687, "US_nov_abr_vol": 0.1079, "US_nov_abr_sharpe": 0.5161,
                  "US_nov_abr_mdd": -0.3032, "US_nov_abr_ops": 1.9931,
                  "alfa1_modelo_A_2003_2026": 0.2886, "t_nw_2003_2026": 0.70},
    }
    fr_ex = french  # alias legible
    rf_fr_full = rf_fr
    tot_fr = {i: (v[0] + v[1]) / 100.0 for i, v in french.items()}
    a_dentro = regresion_efecto(serie_ventana(tot_fr, (1926, 7), (2002, 12)), "A")
    a_fuera = regresion_efecto(serie_ventana(tot_fr, (2003, 1), (2026, 7)), "A")
    print(f"  French a1 1926-07..2002-12 = {a_dentro['beta'][1]:.4f} (orig. 0.6819), "
          f"t_NW={a_dentro['t_nw'][1]:.2f} (orig. 2.07)")
    print(f"  French a1 2003-01..2026-07 = {a_fuera['beta'][1]:.4f} (orig. 0.2886), "
          f"t_NW={a_fuera['t_nw'][1]:.2f} (orig. 0.70)")
    RESULTADOS["control_french"] = {"a1_dentro": a_dentro["beta"][1], "t_nw_dentro": a_dentro["t_nw"][1],
                                    "a1_fuera": a_fuera["beta"][1], "t_nw_fuera": a_fuera["t_nw"][1]}
    for etiqueta, d, h, ref in [("dentro 1927-05 a 2002-12", (1927, 5), (2002, 12), referencia["dentro"]),
                                ("fuera 2003-01 a 2026-07", (2003, 1), (2026, 7), referencia["fuera"])]:
        b = backtest(tot_fr, rf_fr, d, h, senal_halloween)
        bh = backtest(tot_fr, rf_fr, d, h, lambda idx: 1.0)
        print(f"  {etiqueta}: US_nov_abr CAGR={b['cagr']:.4f} (orig. {ref['US_nov_abr_cagr']:.4f}) "
              f"vol={b['vol']:.4f} (orig. {ref['US_nov_abr_vol']:.4f}) "
              f"Sharpe={b['sharpe']:.4f} (orig. {ref['US_nov_abr_sharpe']:.4f}) "
              f"MDD={b['mdd']:.4f} (orig. {ref['US_nov_abr_mdd']:.4f}) "
              f"ops={b['ops_por_anio']:.4f} (orig. {ref['US_nov_abr_ops']:.4f})")
        if "BH_cagr" in ref:
            print(f"  {etiqueta}: comprar y mantener CAGR={bh['cagr']:.4f} (orig. {ref['BH_cagr']:.4f}) "
                  f"vol={bh['vol']:.4f} (orig. {ref['BH_vol']:.4f}) Sharpe={bh['sharpe']:.4f} "
                  f"(orig. {ref['BH_sharpe']:.4f}) MDD={bh['mdd']:.4f} (orig. {ref['BH_mdd']:.4f})")
        RESULTADOS.setdefault("control_french_estrategia", {})[etiqueta] = {"halloween": b, "bh": bh}
    print()

    with open(os.path.join(BASE, "resultados_independiente.json"), "w") as f:
        json.dump(RESULTADOS, f, indent=2, default=lambda o: None)


if __name__ == "__main__":
    main()
