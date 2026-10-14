"""AC-18-R13, ejecucion B independiente: anomalia de devengos (Sloan 1996).

Codigo escrito desde cero por el auditor (no se leyo R13.py ni R13-salida.txt).
Solo biblioteca estandar. Correr con:  python3 -I b.py [directorio_datos]

Fuente principal B: Open Source Asset Pricing (Chen y Zimmermann), release
2025-10 (v2.0.0), senal "Accruals" (definicion de Sloan: devengos de balance /
activos totales promedio, filtro |precio| > 5). Archivos PredictorAltPorts_*.
Cotejo secundario: French Portfolios_Formed_on_AC (misma fuente que A, parser propio).
Factores: French F-F_Research_Data_5_Factors_2x3.
"""
import csv
import hashlib
import io
import math
import os
import sys
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "datos")

PRE = (196307, 199606)
COSTO_MENSUAL = 1.0 / 12.0  # 1% anual en puntos porcentuales por mes
NW_LAGS = 6

FALTANTES = []


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def es_faltante(x):
    return x is None or abs(x - (-99.99)) < 1e-9 or abs(x - (-999.0)) < 1e-9


# ---------------------------------------------------------------- lectores
def leer_osap(zip_nombre, senal="Accruals"):
    """Devuelve {port: {yyyymm: ret%}} para la senal pedida."""
    ruta = os.path.join(DATOS, zip_nombre)
    z = zipfile.ZipFile(ruta)
    nombre = z.namelist()[0]
    out = {}
    with z.open(nombre) as h:
        lector = csv.reader(io.TextIOWrapper(h, encoding="utf-8"))
        cab = next(lector)
        i_s, i_p, i_d, i_r = (cab.index(c) for c in ("signalname", "port", "date", "ret"))
        for fila in lector:
            if fila[i_s] != senal:
                continue
            d = fila[i_d]
            ym = int(d[0:4]) * 100 + int(d[5:7])
            txt = fila[i_r].strip()
            r = None if txt in ("", "NA", "NaN") else float(txt)
            if r is None or es_faltante(r):
                FALTANTES.append((zip_nombre, fila[i_p], ym))
                continue
            out.setdefault(fila[i_p], {})[ym] = r
    return out


def leer_osap_csv(nombre, senal="Accruals"):
    ruta = os.path.join(DATOS, nombre)
    out = {}
    with open(ruta, encoding="utf-8") as h:
        lector = csv.reader(h)
        cab = next(lector)
        i_s, i_p, i_d, i_r = (cab.index(c) for c in ("signalname", "port", "date", "ret"))
        for fila in lector:
            if fila[i_s] != senal:
                continue
            d = fila[i_d]
            ym = int(d[0:4]) * 100 + int(d[5:7])
            txt = fila[i_r].strip()
            if txt in ("", "NA", "NaN"):
                continue
            out.setdefault(fila[i_p], {})[ym] = float(txt)
    return out


def signallag_medio(nombre, senal="Accruals"):
    sumas = {}
    with open(os.path.join(DATOS, nombre), encoding="utf-8") as h:
        for fila in csv.DictReader(h):
            if fila["signalname"] != senal or fila["signallag"] in ("", "NA"):
                continue
            a = sumas.setdefault(fila["port"], [0.0, 0])
            a[0] += float(fila["signallag"])
            a[1] += 1
    return {k: v[0] / v[1] for k, v in sumas.items()}


def secciones_french(zip_nombre):
    """Parte un CSV de French en secciones {titulo: (columnas, {yyyymm: [valores]})}.
    Solo filas con fecha de 6 digitos (mensuales)."""
    z = zipfile.ZipFile(os.path.join(DATOS, zip_nombre))
    texto = z.read(z.namelist()[0]).decode("latin-1").splitlines()
    secciones = {}
    titulo = "PRINCIPAL"
    cols = None
    for linea in texto:
        s = linea.strip()
        if not s:
            continue
        partes = [p.strip() for p in s.split(",")]
        if partes[0] == "" and len(partes) > 1:  # cabecera de columnas
            cols = partes[1:]
            secciones.setdefault(titulo, (cols, {}))
            continue
        if partes[0].isdigit():
            if len(partes[0]) == 6 and cols is not None:
                vals = []
                for p in partes[1:]:
                    v = float(p)
                    if es_faltante(v):
                        FALTANTES.append((zip_nombre + ":" + titulo, partes[0]))
                        v = None
                    vals.append(v)
                secciones[titulo][1][int(partes[0])] = vals
            continue
        # linea de texto: posible titulo de seccion
        if "--" in s or "Returns" in s or "Number" in s or "Average" in s or "Sum" in s:
            titulo = s
            cols = None
    return secciones


def columna(sec, nombre):
    cols, filas = sec
    j = cols.index(nombre)
    return {ym: v[j] for ym, v in filas.items() if v[j] is not None}


# ---------------------------------------------------------------- algebra
def invertir(A):
    n = len(A)
    M = [list(map(float, A[i])) + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        p = M[c][c]
        if abs(p) < 1e-14:
            raise ValueError("matriz singular")
        M[c] = [x / p for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0.0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [fila[n:] for fila in M]


def ols_nw(y, X, lags=NW_LAGS):
    """OLS con errores estandar convencionales y Newey-West (Bartlett, sin ajuste g.l. en NW)."""
    T, k = len(y), len(X[0])
    XtX = [[sum(X[t][i] * X[t][j] for t in range(T)) for j in range(k)] for i in range(k)]
    Xty = [sum(X[t][i] * y[t] for t in range(T)) for i in range(k)]
    iX = invertir(XtX)
    b = [sum(iX[i][j] * Xty[j] for j in range(k)) for i in range(k)]
    e = [y[t] - sum(X[t][i] * b[i] for i in range(k)) for t in range(T)]
    s2 = sum(v * v for v in e) / (T - k)
    se_c = [math.sqrt(s2 * iX[i][i]) for i in range(k)]
    # Omega = G0 + sum_l w_l (G_l + G_l'), pesos de Bartlett
    S2 = [[0.0] * k for _ in range(k)]
    G0 = [[sum(X[t][i] * X[t][j] * e[t] * e[t] for t in range(T)) for j in range(k)] for i in range(k)]
    for i in range(k):
        for j in range(k):
            S2[i][j] = G0[i][j]
    for l in range(1, lags + 1):
        w = 1.0 - l / (lags + 1.0)
        G = [[sum(X[t][i] * e[t] * X[t - l][j] * e[t - l] for t in range(l, T)) for j in range(k)] for i in range(k)]
        for i in range(k):
            for j in range(k):
                S2[i][j] += w * (G[i][j] + G[j][i])
    V = [[sum(iX[i][a] * S2[a][c] * iX[c][j] for a in range(k) for c in range(k)) for j in range(k)] for i in range(k)]
    se_nw = [math.sqrt(V[i][i]) for i in range(k)]
    return b, se_c, se_nw


def stats_media(serie):
    """media, desv. est., t convencional, t NW(6) de una serie mensual en %."""
    y = list(serie)
    T = len(y)
    m = sum(y) / T
    sd = math.sqrt(sum((v - m) ** 2 for v in y) / (T - 1))
    t_c = m / (sd / math.sqrt(T))
    e = [v - m for v in y]
    om = sum(v * v for v in e)
    for l in range(1, NW_LAGS + 1):
        w = 1.0 - l / (NW_LAGS + 1.0)
        om += 2.0 * w * sum(e[t] * e[t - l] for t in range(l, T))
    se_nw = math.sqrt(om) / T
    return {"n": T, "media": m, "sd": sd, "t": t_c, "t_nw": m / se_nw}


# ---------------------------------------------------------------- utilidades
def recorte(d, ini, fin):
    return [(ym, d[ym]) for ym in sorted(d) if ini <= ym <= fin]


def largo_corto(ports, lo, hi):
    comunes = sorted(set(ports[lo]) & set(ports[hi]))
    return {ym: ports[lo][ym] - ports[hi][ym] for ym in comunes}


def fmt_ym(ym):
    return "%d-%02d" % (ym // 100, ym % 100)


def linea_stats(etq, s):
    return "%-38s n=%3d  media=%7.3f%%  sd=%6.3f  t=%6.2f  tNW6=%6.2f" % (
        etq, s["n"], s["media"], s["sd"], s["t"], s["t_nw"])


def bloque(nombre, ls, ultimo, mkt, ff5, salida, con_alfa=False):
    tramos = [("pre  " + fmt_ym(PRE[0]) + ".." + fmt_ym(PRE[1]), PRE[0], PRE[1]),
              ("post " + fmt_ym(199607) + ".." + fmt_ym(ultimo), 199607, ultimo),
              ("2001+ " + fmt_ym(200101) + ".." + fmt_ym(ultimo), 200101, ultimo)]
    res = {}
    salida.append("")
    salida.append("== " + nombre)
    for etq, a, b in tramos:
        serie = [v for _, v in recorte(ls, a, b)]
        s = stats_media(serie)
        sc = stats_media([v - COSTO_MENSUAL for v in serie])
        res[etq.split()[0]] = (s, sc)
        salida.append(linea_stats("  bruto  " + etq, s))
        salida.append(linea_stats("  1%/ano " + etq, sc))
        salida.append("  %-38s media anual simple=%6.2f%%  (neta=%6.2f%%)" % ("", 12 * s["media"], 12 * sc["media"]))
        mk = stats_media([v for _, v in recorte(mkt, a, b)])
        salida.append(linea_stats("  Mkt-RF " + etq, mk))
        if con_alfa:
            meses = [ym for ym, _ in recorte(ls, a, b) if ym in ff5]
            y = [ls[ym] for ym in meses]
            Xc = [[1.0, ff5[ym][0]] for ym in meses]
            bc, sec, senw = ols_nw(y, Xc)
            salida.append("  alfa CAPM %-27s a=%7.3f%%/mes t=%6.2f tNW6=%6.2f beta=%6.3f (n=%d)" % (
                etq, bc[0], bc[0] / sec[0], bc[0] / senw[0], bc[1], len(y)))
            X5 = [[1.0] + list(ff5[ym][0:5]) for ym in meses]
            b5, se5, se5nw = ols_nw(y, X5)
            salida.append("  alfa FF5  %-27s a=%7.3f%%/mes t=%6.2f tNW6=%6.2f  b(Mkt,SMB,HML,RMW,CMA)=%s" % (
                etq, b5[0], b5[0] / se5[0], b5[0] / se5nw[0], ",".join("%.2f" % v for v in b5[1:])))
            res["alfa_" + etq.split()[0]] = (bc[0], bc[0] / senw[0], b5[0], b5[0] / se5nw[0])
    pre, post = res["pre"][0], res["post"][0]
    caida = 1.0 - post["media"] / pre["media"]
    salida.append("  caida de la media post vs pre: %.1f%%" % (100 * caida))
    res["caida"] = caida
    return res


def veredicto(res):
    pre, post = res["pre"][0], res["post"][0]
    h1 = pre["media"] > 0 and pre["t_nw"] >= 2.0
    h2 = (post["media"] <= 0.5 * pre["media"]) and post["t_nw"] < 2.0
    if not h1:
        est = "No replicado"
    elif not h2:
        est = "Replicado con diferencias"
    else:
        est = "Replicado"
    return h1, h2, est


def main():
    salida = []
    salida.append("AC-18-R13 ejecucion B (codigo independiente)")
    salida.append("Directorio de datos: " + DATOS)
    archivos = ["PredictorAltPorts_DecilesVW.zip", "PredictorAltPorts_DecilesEW.zip",
                "PredictorAltPorts_QuintilesVW.zip", "PredictorAltPorts_QuintilesEW.zip",
                "PredictorPortsFull.csv",
                "F-F_Research_Data_5_Factors_2x3_CSV.zip", "Portfolios_Formed_on_AC_CSV.zip"]
    for a in archivos:
        salida.append("  sha256 %s  %s" % (sha256(os.path.join(DATOS, a)), a))

    # factores French
    ff = secciones_french("F-F_Research_Data_5_Factors_2x3_CSV.zip")
    cols, filas = ff["PRINCIPAL"]
    assert cols[:6] == ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "RF"], cols
    ff5 = {ym: v for ym, v in filas.items() if all(x is not None for x in v)}
    mkt = {ym: v[0] for ym, v in ff5.items()}
    salida.append("Factores FF5: %s..%s" % (fmt_ym(min(ff5)), fmt_ym(max(ff5))))

    # OSAP
    dvw = leer_osap("PredictorAltPorts_DecilesVW.zip")
    dew = leer_osap("PredictorAltPorts_DecilesEW.zip")
    qvw = leer_osap("PredictorAltPorts_QuintilesVW.zip")
    qew = leer_osap("PredictorAltPorts_QuintilesEW.zip")
    op = leer_osap_csv("PredictorPortsFull.csv")
    salida.append("OSAP Accruals deciles VW: puertos %s, %s..%s" % (
        sorted(dvw), fmt_ym(min(dvw["01"])), fmt_ym(max(dvw["01"]))))
    salida.append("OSAP quintiles VW: puertos %s" % sorted(qvw))

    # Orientacion: OSAP guarda la senal FIRMADA (signallag = Sign * Accruals, Sign = -1),
    # de modo que el puerto mas alto es el de devengos MAS BAJOS y LS = p_alto - p01.
    # Se verifica con los datos en vez de suponerlo.
    for etq, ports, alto in (("OP deciles EW", op, "10"), ("Alt deciles VW", dvw, "10"),
                             ("Alt deciles EW", dew, "10"), ("Alt quintiles VW", qvw, "05"),
                             ("Alt quintiles EW", qew, "05")):
        ls_chk = largo_corto(ports, alto, "01")
        if "LS" in ports:
            dif = [abs(ls_chk[ym] - ports["LS"][ym]) for ym in ls_chk if ym in ports["LS"]]
            salida.append("Chequeo %-17s max|(p%s-p01) - LS_OSAP| = %.1e (n=%d)" % (etq, alto, max(dif), len(dif)))
    sl = signallag_medio("PredictorPortsFull.csv")
    salida.append("signallag medio por puerto (OP): " + ", ".join("%s:%.3f" % (k, v) for k, v in sorted(sl.items())))
    salida.append("=> la senal esta firmada (-devengos): Lo devengos = p10 (p05 en quintiles), Hi = p01")
    dif2 = [abs(dew["01"][ym] - op["01"][ym]) for ym in dew["01"] if ym in op["01"]]
    salida.append("Chequeo DecilesEW (alt) vs OP (EW deciles): max|dif p01| = %.2e" % max(dif2))

    ult_osap = max(dvw["01"])
    variantes = [
        ("OSAP PRINCIPAL VW deciles Lo10-Hi10", largo_corto(dvw, "10", "01"), True),
        ("OSAP V1 EW deciles Lo10-Hi10", largo_corto(dew, "10", "01"), False),
        ("OSAP V2 VW quintiles Lo20-Hi20", largo_corto(qvw, "05", "01"), False),
        ("OSAP V3 EW quintiles Lo20-Hi20", largo_corto(qew, "05", "01"), False),
    ]
    resultados = {}
    for nombre, ls, alfa in variantes:
        resultados[nombre] = bloque(nombre, ls, ult_osap, mkt, ff5, salida, con_alfa=alfa)

    # cotejo French AC (misma fuente que A, parser propio)
    fr = secciones_french("Portfolios_Formed_on_AC_CSV.zip")
    vw_key = [k for k in fr if k.startswith("Value Weighted Returns -- Monthly")][0]
    ew_key = [k for k in fr if k.startswith("Equal Weighted Returns -- Monthly")][0]
    fvw, few = fr[vw_key], fr[ew_key]
    ult_fr = max(fvw[1])
    salida.append("")
    salida.append("French AC: %s..%s (secciones: %s | %s)" % (fmt_ym(min(fvw[1])), fmt_ym(ult_fr), vw_key, ew_key))
    fr_var = [
        ("FRENCH VW deciles Lo10-Hi10", columna(fvw, "Lo 10"), columna(fvw, "Hi 10"), True),
        ("FRENCH EW deciles Lo10-Hi10", columna(few, "Lo 10"), columna(few, "Hi 10"), False),
        ("FRENCH VW quintiles Lo20-Hi20", columna(fvw, "Lo 20"), columna(fvw, "Hi 20"), False),
        ("FRENCH EW quintiles Lo20-Hi20", columna(few, "Lo 20"), columna(few, "Hi 20"), False),
    ]
    for nombre, lo, hi, alfa in fr_var:
        ls = {ym: lo[ym] - hi[ym] for ym in sorted(set(lo) & set(hi))}
        resultados[nombre] = bloque(nombre, ls, ult_fr, mkt, ff5, salida, con_alfa=alfa)
        resultados[nombre + " [comun ..2024-12]"] = bloque(
            nombre + " [periodo comun con OSAP, post hasta " + fmt_ym(ult_osap) + "]",
            ls, ult_osap, mkt, ff5, salida, con_alfa=False)

    # correlacion OSAP VW vs French VW (deciles)
    a = largo_corto(dvw, "10", "01")
    b_ = {ym: v for ym, v in ((ym, columna(fvw, "Lo 10")[ym] - columna(fvw, "Hi 10")[ym]) for ym in fvw[1])}
    com = [ym for ym in sorted(set(a) & set(b_)) if ym >= 196307]
    xa, xb = [a[m] for m in com], [b_[m] for m in com]
    ma, mb = sum(xa) / len(xa), sum(xb) / len(xb)
    cor = sum((p - ma) * (q - mb) for p, q in zip(xa, xb)) / math.sqrt(
        sum((p - ma) ** 2 for p in xa) * sum((q - mb) ** 2 for q in xb))
    salida.append("")
    salida.append("Correlacion mensual LS VW deciles OSAP vs French (%s..%s): %.3f" % (
        fmt_ym(com[0]), fmt_ym(com[-1]), cor))

    salida.append("")
    salida.append("== Faltantes (-99.99/-999/NA) encontrados: %d" % len(FALTANTES))
    for f in FALTANTES[:20]:
        salida.append("   " + str(f))

    salida.append("")
    salida.append("== VEREDICTO segun criterio del par. 2 del pre-registro")
    for nombre in resultados:
        if "[comun" in nombre:
            continue
        h1, h2, est = veredicto(resultados[nombre])
        r = resultados[nombre]
        salida.append("  %-38s H1=%s H2=%s caida=%5.1f%% -> %s" % (
            nombre, "sostenida" if h1 else "refutada", "sostenida" if h2 else "refutada",
            100 * r["caida"], est))
    for nombre in resultados:
        if "[comun" in nombre:
            h1, h2, est = veredicto(resultados[nombre])
            salida.append("  %-50s H1=%s H2=%s caida=%5.1f%% -> %s" % (
                nombre, "sostenida" if h1 else "refutada", "sostenida" if h2 else "refutada",
                100 * resultados[nombre]["caida"], est))

    print("\n".join(salida))


if __name__ == "__main__":
    main()
