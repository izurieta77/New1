#!/usr/bin/env python3
"""V03 - Doble ejecucion independiente (auditor-de-replicas), 2026-09-25.

Reimplementacion desde cero de V03, escrita SIN leer `reproducir.py`.
Entradas: solo el pre-registro (seccion PRE-REGISTRO del README, copia literal de
`prerregistro.md`) y los datos congelados en `datos/` (verificados por SHA-256).

Todo es propio: lectura de los zip de French, lectura de DEXMXUS, alineacion de
fechas, construccion de diferenciales, conversion a MXN, error estandar
Newey-West (dos formulas propias distintas), IC95, veredicto, bootstrap de
bloques moviles, CAGR, volatilidad y caida maxima. `herramientas.estadistica`
se usa solo como TERCERA comprobacion del error estandar, nunca para las cifras.

Despues compara cada cifra de las tablas de RESULTADOS del README (y las cifras
citadas en el texto) contra las propias, con las tolerancias del encargo:
0.01 pp en medias mensuales (y limites de IC, que estan en %/mes), 0.05 en t,
0.1 pp en CAGR / caida maxima / volatilidad / diferencia de CAGR. Para media x12
la tolerancia equivalente es 0.12 pp (0.01 x 12). Ademas marca si la cifra propia,
redondeada a los decimales impresos, coincide exactamente con la impresa.

Salidas (sin red):
  - independiente-resultados.json   cifras propias
  - independiente-comparacion.csv   una fila por cifra comparada
  - resumen en pantalla (y tabla markdown para el README)

Uso, desde la raiz del repo:
    python3 laboratorio/replicas/V03-anomalias-long-only-eua/independiente.py
"""
import csv
import hashlib
import io
import json
import math
import os
import random
import re
import sys
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(BASE, "datos")
RAIZ = os.path.abspath(os.path.join(BASE, "..", "..", ".."))

Z = 1.959963984540054  # cuantil 97.5% de la normal
REZAGOS = 6
FIN = "202607"
COSTO_LADO = 0.25 * 1.16 + 0.05  # % por lado: comision GBM con IVA + spread supuesto


# ---------------------------------------------------------------------------
# 0. Huellas (implementacion propia con hashlib)
# ---------------------------------------------------------------------------
def verificar_huellas():
    ruta = os.path.join(BASE, "SHA256SUMS.txt")
    malos = []
    total = 0
    with open(ruta, encoding="utf-8") as fh:
        for linea in fh:
            linea = linea.strip()
            if not linea:
                continue
            esperado, nombre = linea.split(None, 1)
            h = hashlib.sha256()
            with open(os.path.join(BASE, nombre.strip()), "rb") as fb:
                for bloque in iter(lambda: fb.read(1 << 16), b""):
                    h.update(bloque)
            total += 1
            if h.hexdigest() != esperado:
                malos.append(nombre)
    if malos:
        sys.exit("HUELLA DISTINTA: " + ", ".join(malos))
    return total


# ---------------------------------------------------------------------------
# 1. Lectura propia de los CSV de Kenneth French y de FRED
# ---------------------------------------------------------------------------
def leer_french(nombre_zip):
    """Devuelve lista de secciones: {'titulo', 'columnas', 'filas': {clave: [float|None]}}.

    Una seccion empieza con una linea que inicia con ',' (encabezados); su titulo es
    la ultima linea de texto no vacia anterior. Termina en la primera linea vacia.
    -99.99 y -999 se guardan como None (faltante).
    """
    with zipfile.ZipFile(os.path.join(DATOS, nombre_zip)) as z:
        miembros = z.namelist()
        assert len(miembros) == 1, miembros
        texto = z.read(miembros[0]).decode("latin-1")
    secciones = []
    ultimo_texto = ""
    actual = None
    for cruda in texto.splitlines():
        linea = cruda.strip()
        if not linea:
            actual = None
            continue
        if linea.startswith(","):
            actual = {
                "titulo": ultimo_texto,
                "columnas": [c.strip() for c in linea.split(",")[1:]],
                "filas": {},
                "faltantes": 0,
            }
            secciones.append(actual)
            continue
        campos = [c.strip() for c in linea.split(",")]
        if actual is not None and campos[0].isdigit():
            valores = []
            for c in campos[1:]:
                v = float(c)
                if v in (-99.99, -999.0):
                    valores.append(None)
                    actual["faltantes"] += 1
                else:
                    valores.append(v)
            assert len(valores) == len(actual["columnas"]), (nombre_zip, campos[0])
            assert campos[0] not in actual["filas"], ("fecha repetida", campos[0])
            actual["filas"][campos[0]] = valores
        else:
            ultimo_texto = linea
            actual = None
    return secciones


def seccion_mensual(secciones, contiene=None):
    """Elige la unica seccion con fechas AAAAMM (y, si se pide, cuyo titulo contenga el texto)."""
    candidatas = []
    for s in secciones:
        claves = list(s["filas"])
        if not claves or not all(len(k) == 6 for k in claves):
            continue
        if contiene is not None and contiene.lower() not in s["titulo"].lower():
            continue
        candidatas.append(s)
    assert len(candidatas) == 1, [c["titulo"] for c in candidatas]
    return candidatas[0]


def columna(seccion, nombre):
    i = seccion["columnas"].index(nombre)
    return {k: v[i] for k, v in seccion["filas"].items()}


def leer_dexmxus():
    """Ultima observacion no vacia de cada mes calendario -> {AAAAMM: nivel}."""
    fin_de_mes = {}
    fechas = []
    with open(os.path.join(DATOS, "DEXMXUS.csv"), encoding="utf-8") as fh:
        lector = csv.reader(fh)
        encabezado = next(lector)
        assert encabezado == ["observation_date", "DEXMXUS"], encabezado
        vacias = 0
        for fila in lector:
            fecha, valor = fila[0], fila[1].strip()
            fechas.append(fecha)
            if valor in ("", "."):
                vacias += 1
                continue
            clave = fecha[0:4] + fecha[5:7]
            fin_de_mes[clave] = float(valor)  # el archivo va en orden: gana la ultima
    assert fechas == sorted(fechas)
    return fin_de_mes, fechas[0], fechas[-1], vacias


# ---------------------------------------------------------------------------
# 2. Fechas
# ---------------------------------------------------------------------------
def a_indice(aaaamm):
    return int(aaaamm[:4]) * 12 + int(aaaamm[4:]) - 1


def a_clave(indice):
    return "%04d%02d" % (indice // 12, indice % 12 + 1)


def meses(ini, fin):
    return [a_clave(i) for i in range(a_indice(ini), a_indice(fin) + 1)]


def siguiente(aaaamm):
    return a_clave(a_indice(aaaamm) + 1)


# ---------------------------------------------------------------------------
# 3. Estadistica propia
# ---------------------------------------------------------------------------
def nw_autocovarianzas(x, L=REZAGOS):
    """Formula 1: suma de autocovarianzas con pesos de Bartlett."""
    n = len(x)
    m = math.fsum(x) / n
    u = [v - m for v in x]
    s = math.fsum(a * a for a in u)
    for j in range(1, L + 1):
        w = (L + 1 - j) / (L + 1)
        s += 2.0 * w * math.fsum(u[t] * u[t - j] for t in range(j, n))
    omega = s / n
    return m, math.sqrt(omega / (n - 1))  # omega/n * n/(n-1)


def nw_sumas_moviles(x, L=REZAGOS):
    """Formula 2 (distinta): identidad de Bartlett con sumas moviles de L+1 residuos.

    Con u rellenado con ceros fuera de 0..n-1 y S_t = sum_{k=t-L..t} u_k,
    sum_t S_t^2 / (L+1) = sum_{a,b} u_a u_b (1 - |a-b|/(L+1))_+ = n * omega.
    """
    n = len(x)
    m = math.fsum(x) / n
    u = [v - m for v in x]
    total = 0.0
    acum = 0.0
    for t in range(n + L):
        if t < n:
            acum += u[t]
        if t - L - 1 >= 0:
            acum -= u[t - L - 1]
        total += acum * acum
    omega = total / (n * (L + 1))
    return m, math.sqrt(omega / (n - 1))


def veredicto(lo, hi):
    if lo > 0:
        return "apoyo"
    if hi < 0:
        return "contraria"
    return "inconcluso"


def bootstrap_bloques(x, largo=12, reps=5000, semilla=7):
    """Bootstrap de bloques moviles propio. Cuantiles por rango mas cercano."""
    n = len(x)
    rng = random.Random(semilla)
    n_bloques = -(-n // largo)
    medias = []
    for _ in range(reps):
        muestra = []
        for _b in range(n_bloques):
            i = rng.randrange(n - largo + 1)
            muestra.extend(x[i:i + largo])
        medias.append(math.fsum(muestra[:n]) / n)
    medias.sort()
    k_lo = math.ceil(0.025 * reps) - 1
    k_hi = math.ceil(0.975 * reps) - 1
    return medias[k_lo], medias[k_hi]


def cagr(r_dec):
    log_total = math.fsum(math.log1p(v) for v in r_dec)
    return math.exp(log_total * 12.0 / len(r_dec)) - 1.0


def vol_anual(r_dec):
    n = len(r_dec)
    m = math.fsum(r_dec) / n
    return math.sqrt(math.fsum((v - m) ** 2 for v in r_dec) / (n - 1)) * math.sqrt(12.0)


def caida_maxima(r_dec):
    riqueza = 1.0
    pico = 1.0  # se cuenta el capital inicial como pico
    peor = 0.0
    for v in r_dec:
        riqueza *= 1.0 + v
        pico = max(pico, riqueza)
        peor = min(peor, riqueza / pico - 1.0)
    return peor


# ---------------------------------------------------------------------------
# 4. Datos y series (lista cerrada del pre-registro, seccion 3)
# ---------------------------------------------------------------------------
def cargar():
    ff3 = seccion_mensual(leer_french("F-F_Research_Data_Factors_CSV.zip"))
    ff5 = seccion_mensual(leer_french("F-F_Research_Data_5_Factors_2x3_CSV.zip"))
    mkt_rf = columna(ff3, "Mkt-RF")
    rf = columna(ff3, "RF")
    mkt = {k: mkt_rf[k] + rf[k] for k in mkt_rf}
    info = {
        "ff3_rango": (min(ff3["filas"]), max(ff3["filas"])),
        "ff5_rango": (min(ff5["filas"]), max(ff5["filas"])),
        "faltantes": {"ff3": ff3["faltantes"], "ff5": ff5["faltantes"]},
    }
    carteras = {}
    for cod in ("OP", "NI", "VAR", "RESVAR", "INV"):
        secs = leer_french("Portfolios_Formed_on_%s_CSV.zip" % cod)
        vw = seccion_mensual(secs, "Value Weight")
        ew = seccion_mensual(secs, "Equal Weight")
        carteras[cod] = {"VW": vw, "EW": ew}
        info["%s_titulos" % cod] = (vw["titulo"], ew["titulo"])
        info["%s_rango" % cod] = (min(vw["filas"]), max(vw["filas"]))
        info["faltantes"][cod] = vw["faltantes"] + ew["faltantes"]
    return mkt, ff5, carteras, info


ANOM = {
    #  codigo: (pierna buena, pierna mala, ultimo mes pre-publicacion)
    "OP": ("Hi 20", "Lo 20", "201504"),
    "NI": ("< 0", "Hi 20", "200804"),
    "VAR": ("Lo 20", "Hi 20", "200602"),
    "INV": ("Lo 20", "Hi 20", "200808"),
    "RESVAR": ("Lo 20", "Hi 20", "200602"),
}
VARIANTES = {
    # (serie base, etiqueta, ultimo mes pre)
    "NM13": ("OP", "Novy-Marx 2013", "201304"),
    "FF15": ("INV", "Fama-French 2015", "201504"),
}


def construir_series(mkt, ff5, carteras):
    """Devuelve dict nombre -> {'larga': {mes: %}, 'corta': {mes: %}, 'ultimo_pre', 'tipo'}."""
    S = {}
    for cod, (buena, mala, pre) in ANOM.items():
        vw = carteras[cod]["VW"]
        ew = carteras[cod]["EW"]
        S["%s-LO-VW" % cod] = {"larga": columna(vw, buena), "corta": mkt, "ultimo_pre": pre, "tipo": "LO"}
        S["%s-LS-VW" % cod] = {"larga": columna(vw, buena), "corta": columna(vw, mala), "ultimo_pre": pre, "tipo": "LS"}
        if cod != "RESVAR":
            S["%s-LS-EW" % cod] = {"larga": columna(ew, buena), "corta": columna(ew, mala), "ultimo_pre": pre, "tipo": "LS"}
    for f in ("RMW", "CMA"):
        cero = {k: 0.0 for k in ff5["filas"]}
        S[f] = {"larga": columna(ff5, f), "corta": cero, "ultimo_pre": "201504", "tipo": "F"}
    # exploratorias post-hoc (deciles)
    for cod in ("VAR", "RESVAR"):
        vw = carteras[cod]["VW"]
        S["%s Lo 10 - Mkt" % cod] = {"larga": columna(vw, "Lo 10"), "corta": mkt, "ultimo_pre": ANOM[cod][2], "tipo": "LO"}
        S["%s Lo 10 - Hi 10" % cod] = {"larga": columna(vw, "Lo 10"), "corta": columna(vw, "Hi 10"), "ultimo_pre": ANOM[cod][2], "tipo": "LS"}
    return S


def inicio_de(serie):
    return max(min(serie["larga"]), min(serie["corta"]))


def ventanas_usd(serie):
    ini = inicio_de(serie)
    pre = serie["ultimo_pre"]
    return {
        "completo": (ini, FIN),
        "pre": (ini, pre),
        "2000-2025": ("200001", "202512"),
        "2000-ult": ("200001", FIN),
        "post": (siguiente(pre), FIN),
    }


def extraer(serie, ini, fin, fx=None):
    """Diferencial mes a mes en %, y las dos piernas en decimal (USD o MXN)."""
    ms = meses(ini, fin)
    d, a, b = [], [], []
    for m in ms:
        la, co = serie["larga"].get(m), serie["corta"].get(m)
        if la is None or co is None:
            raise ValueError("faltante en %s" % m)
        if fx is None:
            d.append(la - co)
            a.append(la / 100.0)
            b.append(co / 100.0)
        else:
            f = fx[m]
            d.append((la - co) * (1.0 + f))
            a.append((1.0 + la / 100.0) * (1.0 + f) - 1.0)
            b.append((1.0 + co / 100.0) * (1.0 + f) - 1.0)
    return ms, d, a, b


def prueba(ms, d, con_bootstrap=False):
    m1, se1 = nw_autocovarianzas(d)
    m2, se2 = nw_sumas_moviles(d)
    assert abs(m1 - m2) < 1e-13 and abs(se1 - se2) < 1e-12, (se1, se2)
    lo, hi = m1 - Z * se1, m1 + Z * se1
    r = {
        "ini": ms[0], "fin": ms[-1], "n": len(d),
        "media": m1, "x12": 12 * m1, "se": se1, "se_formula2": se2,
        "t": m1 / se1, "lo": lo, "hi": hi, "veredicto": veredicto(lo, hi),
    }
    if con_bootstrap:
        r["b_lo"], r["b_hi"] = bootstrap_bloques(d)
    return r


def descriptivo(a, b):
    ca, cb = cagr(a), cagr(b)
    return {
        "cagr_p": 100 * ca, "cagr_m": 100 * cb, "dif": 100 * (ca - cb),
        "vol_p": 100 * vol_anual(a), "vol_m": 100 * vol_anual(b),
        "mdd_p": 100 * caida_maxima(a), "mdd_m": 100 * caida_maxima(b),
    }


def calcular():
    mkt, ff5, carteras, info = cargar()
    S = construir_series(mkt, ff5, carteras)
    niveles, fx_ini, fx_fin, fx_vacias = leer_dexmxus()
    info["fx"] = {"primera": fx_ini, "ultima": fx_fin, "vacias": fx_vacias}
    fx = {}
    for m in meses("199401", FIN):
        previo = a_clave(a_indice(m) - 1)
        fx[m] = niveles[m] / niveles[previo] - 1.0

    R, D, pruebas = {}, {}, []
    primarias = [f"{a}-{t}-VW" for a in ("OP", "NI", "VAR", "INV") for t in ("LO", "LS")]
    for nombre, serie in S.items():
        if " Lo 10" in nombre:
            continue
        for v, (ini, fin) in ventanas_usd(serie).items():
            ms, d, a, b = extraer(serie, ini, fin)
            boot = nombre in primarias and v in ("2000-2025", "post")
            R[(nombre, v)] = prueba(ms, d, boot)
            pruebas.append((nombre, v, "USD"))
            if serie["tipo"] != "F":
                D[(nombre, v, "USD")] = descriptivo(a, b)
    # variantes de fecha de publicacion
    for etiqueta, (base, texto, pre) in VARIANTES.items():
        for tipo in ("LO", "LS"):
            nombre = f"{base}-{tipo}-VW"
            serie = S[nombre]
            for v, (ini, fin) in (("pre", (inicio_de(serie), pre)), ("post", (siguiente(pre), FIN))):
                ms, d, a, b = extraer(serie, ini, fin)
                R[(nombre, f"{etiqueta}-{v}")] = prueba(ms, d)
                pruebas.append((nombre, f"{etiqueta}-{v}", "USD"))
    # MXN: solo LO
    for cod in ("OP", "NI", "VAR", "INV", "RESVAR"):
        nombre = f"{cod}-LO-VW"
        serie = S[nombre]
        vent = {"mxn-completo": ("199401", FIN), "2000-2025": ("200001", "202512"),
                "post": ventanas_usd(serie)["post"]}
        for v, (ini, fin) in vent.items():
            ms, d, a, b = extraer(serie, ini, fin, fx)
            R[(nombre + "-MXN", v)] = prueba(ms, d)
            pruebas.append((nombre + "-MXN", v, "MXN"))
            D[(nombre, v, "MXN")] = descriptivo(a, b)
    # exploratorias post-hoc (no son prueba)
    for nombre in ("VAR Lo 10 - Mkt", "VAR Lo 10 - Hi 10", "RESVAR Lo 10 - Mkt", "RESVAR Lo 10 - Hi 10"):
        for v, (ini, fin) in (("2000-2025", ("200001", "202512")), ("2000-ult", ("200001", FIN))):
            ms, d, a, b = extraer(S[nombre], ini, fin)
            R[(nombre, v)] = prueba(ms, d)
            D[(nombre, v, "USD")] = descriptivo(a, b)
    # tercera comprobacion del error estandar con la herramienta del repo
    sys.path.insert(0, RAIZ)
    try:
        from herramientas.estadistica import newey_west as nw_repo
        max_dif = 0.0
        for (nombre, v), r in R.items():
            serie = S[nombre.replace("-MXN", "")]
            if nombre.endswith("-MXN"):
                _, d, _, _ = extraer(serie, r["ini"], r["fin"], fx)
            else:
                _, d, _, _ = extraer(serie, r["ini"], r["fin"])
            max_dif = max(max_dif, abs(nw_repo(d, REZAGOS)["se"] - r["se"]))
        info["max_dif_se_vs_herramienta"] = max_dif
    except ImportError:
        info["max_dif_se_vs_herramienta"] = None
    info["max_dif_se_formulas_propias"] = max(abs(r["se"] - r["se_formula2"]) for r in R.values())
    info["inicio_series"] = sorted({inicio_de(s) for s in S.values()})
    return S, R, D, pruebas, info


# ---------------------------------------------------------------------------
# 5. Lectura de las cifras reportadas en el README
# ---------------------------------------------------------------------------
def norm(s):
    return s.replace("−", "-").replace("**", "").replace("%", "").replace("+", "").strip()


def num(s):
    return float(norm(s))


def decimales(s):
    s = norm(s)
    return len(s.split(".")[1]) if "." in s else 0


RE_PAR = re.compile(r"(-?\d+(?:\.\d+)?)\s*\((-?\d+(?:\.\d+)?)\)")
RE_IC = re.compile(r"\[(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\]")


def tablas_readme():
    with open(os.path.join(BASE, "README.md"), encoding="utf-8") as fh:
        texto = fh.read()
    ini = texto.index("## RESULTADOS")
    fin = texto.index("## Conclusiones permitidas")
    cuerpo = texto[ini:fin]
    bloques = {}
    actual = None
    for linea in cuerpo.splitlines():
        if linea.startswith("### "):
            actual = linea[4:].strip()
            bloques[actual] = []
            continue
        s = linea.strip()
        if actual and s.startswith("|"):
            celdas = [c.strip() for c in s.strip("|").split("|")]
            bloques[actual].append(celdas)
    # quitar encabezado + separador de cada tabla
    limpias = {}
    for k, filas in bloques.items():
        out = []
        for i, f in enumerate(filas):
            if set("".join(f)) <= set("-: "):
                continue
            if i + 1 < len(filas) and set("".join(filas[i + 1])) <= set("-: "):
                continue
            out.append(f)
        limpias[k] = out
    return texto, limpias


# ---------------------------------------------------------------------------
# 6. Comparacion
# ---------------------------------------------------------------------------
TOL = {"media": 0.01, "ic": 0.01, "x12": 0.12, "t": 0.05, "cagr": 0.1, "dif": 0.1,
       "vol": 0.1, "mdd": 0.1, "n": 0, "tau": 1.0, "neto": 0.12}


class Comparador:
    def __init__(self):
        self.filas = []

    def num(self, tabla, fila, campo, tipo, texto_rep, propio):
        rep = num(texto_rep)
        dif = propio - rep
        tol = TOL[tipo]
        ok = abs(dif) <= tol + 1e-9
        k = decimales(texto_rep)
        exacto = abs(round(propio + 0.0, k) - rep) < 10 ** (-k) / 2 + 1e-9 if tipo != "n" else propio == rep
        self.filas.append({"tabla": tabla, "fila": fila, "campo": campo, "tipo": tipo,
                           "reportado": texto_rep, "propio": propio, "dif": dif,
                           "tolerancia": tol, "ok": ok, "exacto_al_redondeo": exacto})

    def cat(self, tabla, fila, campo, rep, propio):
        ok = rep == propio
        self.filas.append({"tabla": tabla, "fila": fila, "campo": campo, "tipo": "categoria",
                           "reportado": rep, "propio": propio, "dif": "",
                           "tolerancia": "igual", "ok": ok, "exacto_al_redondeo": ok})


VENTANAS_TABLA = ["completo", "pre", "2000-2025", "2000-ult", "post"]
ALIAS = {"RMW": "RMW", "CMA": "CMA"}


def comparar(R, D, pruebas, info):
    texto, T = tablas_readme()
    C = Comparador()
    claves = list(T)

    def bloque(prefijo):
        (k,) = [k for k in claves if k.startswith(prefijo)]
        return k, T[k]

    # Tablas 1-3: media x12 (t) por ventana, negrita = apoyo
    for pref in ("1.", "2.", "3."):
        k, filas = bloque(pref)
        for f in filas:
            nombre = f[0]
            pre = f[2].replace("-", "")
            ini_post = R[(nombre, "post")]["ini"]
            C.cat(k, nombre, "ultimo mes pre", pre, a_clave(a_indice(ini_post) - 1))
            for v, celda in zip(VENTANAS_TABLA, f[3:8]):
                x12, t = RE_PAR.search(norm(celda.replace("**", ""))).groups()
                r = R[(nombre, v)]
                C.num(k, nombre, v + " x12", "x12", x12, r["x12"])
                C.num(k, nombre, v + " t", "t", t, r["t"])
                C.cat(k, nombre, v + " apoyo(negrita)", "**" in celda, r["veredicto"] == "apoyo")
    # Tabla 4: detalle de primarias
    k, filas = bloque("4.")
    for f in filas:
        nombre, v = f[0], f[1]
        r = R[(nombre, v)]
        a, b = f[2].split("–")
        C.cat(k, f"{nombre} {v}", "meses", f"{a}-{b}", f"{r['ini']}-{r['fin']}")
        C.num(k, f"{nombre} {v}", "n", "n", f[3], r["n"])
        C.num(k, f"{nombre} {v}", "media", "media", f[4], r["media"])
        C.num(k, f"{nombre} {v}", "x12", "x12", f[5], r["x12"])
        C.num(k, f"{nombre} {v}", "t", "t", f[6], r["t"])
        lo, hi = RE_IC.search(norm(f[7])).groups()
        C.num(k, f"{nombre} {v}", "IC NW lo", "ic", lo, r["lo"])
        C.num(k, f"{nombre} {v}", "IC NW hi", "ic", hi, r["hi"])
        lo, hi = RE_IC.search(norm(f[8])).groups()
        C.num(k, f"{nombre} {v}", "IC boot lo", "ic", lo, r["b_lo"])
        C.num(k, f"{nombre} {v}", "IC boot hi", "ic", hi, r["b_hi"])
        C.cat(k, f"{nombre} {v}", "veredicto", f[9], r["veredicto"])
    # Tabla 5: variantes de publicacion
    k, filas = bloque("5.")
    for f in filas:
        nombre = f[0]
        etiqueta = "NM13" if f[1].startswith("Novy") else "FF15"
        r = R[(nombre, f"{etiqueta}-{f[2]}")]
        fila = f"{nombre} {etiqueta} {f[2]}"
        a, b = f[3].split("–")
        C.cat(k, fila, "meses", f"{a}-{b}", f"{r['ini']}-{r['fin']}")
        C.num(k, fila, "x12", "x12", f[4], r["x12"])
        C.num(k, fila, "t", "t", f[5], r["t"])
        lo, hi = RE_IC.search(norm(f[6])).groups()
        C.num(k, fila, "IC NW lo", "ic", lo, r["lo"])
        C.num(k, fila, "IC NW hi", "ic", hi, r["hi"])
        C.cat(k, fila, "veredicto", f[7], r["veredicto"])
    # Tabla 6: MXN
    k, filas = bloque("6.")
    for f in filas:
        nombre, v = f[0], f[1]
        r = R[(nombre + "-MXN", v)]
        fila = f"{nombre} MXN {v}"
        a, b = f[2].split("–")
        C.cat(k, fila, "meses", f"{a}-{b}", f"{r['ini']}-{r['fin']}")
        C.num(k, fila, "n", "n", f[3], r["n"])
        C.num(k, fila, "media", "media", f[4], r["media"])
        C.num(k, fila, "x12", "x12", f[5], r["x12"])
        C.num(k, fila, "t", "t", f[6], r["t"])
        lo, hi = RE_IC.search(norm(f[7])).groups()
        C.num(k, fila, "IC NW lo", "ic", lo, r["lo"])
        C.num(k, fila, "IC NW hi", "ic", hi, r["hi"])
        C.cat(k, fila, "veredicto", f[8], r["veredicto"])
    # Tabla 7: descriptivo
    k, filas = bloque("7.")
    campos7 = [("CAGR cartera", "cagr_p", "cagr"), ("CAGR mercado", "cagr_m", "cagr"),
               ("Dif. CAGR", "dif", "dif"), ("Vol. cartera", "vol_p", "vol"),
               ("Vol. mercado", "vol_m", "vol"), ("Caida max. cartera", "mdd_p", "mdd"),
               ("Caida max. mercado", "mdd_m", "mdd")]
    for f in filas:
        nombre, v, mon = f[0], f[1], f[2]
        d = D[(nombre, v, mon)]
        for (etq, clave, tipo), celda in zip(campos7, f[3:10]):
            C.num(k, f"{nombre} {v} {mon}", etq, tipo, celda, d[clave])
    # Tabla 8: costos
    k, filas = bloque("8.")
    for f in filas:
        nombre = f[0].replace(", MXN", "")
        clave = (nombre + "-MXN", f[1]) if ", MXN" in f[0] else (nombre, f[1])
        r = R[clave]
        fila = f"{f[0]} {f[1]}"
        C.num(k, fila, "x12 bruto", "x12", f[2], r["x12"])
        C.num(k, fila, "tau*", "tau", f[3], 100 * r["x12"] / (2 * COSTO_LADO))
        C.num(k, fila, "neto tau=100%", "neto", f[4], r["x12"] - 2 * COSTO_LADO)
    # Seccion 9: exploratorio post-hoc
    k, filas = bloque("9.")
    for f in filas:
        nombre = norm(f[0]).replace(" - ", " - ")
        nombre = f[0].replace("−", "-")
        r = R[(nombre, f[1])]
        d = D[(nombre, f[1], "USD")]
        fila = f"{nombre} {f[1]}"
        C.num(k, fila, "n", "n", f[2], r["n"])
        C.num(k, fila, "x12", "x12", f[3], r["x12"])
        C.num(k, fila, "Dif. CAGR", "dif", f[4], d["dif"])
        C.num(k, fila, "t", "t", f[5], r["t"])
        lo, hi = RE_IC.search(norm(f[6])).groups()
        C.num(k, fila, "IC NW lo", "ic", lo, r["lo"])
        C.num(k, fila, "IC NW hi", "ic", hi, r["hi"])

    # ----- Cifras citadas en el texto (Resumen, Controles, seccion 9, 10, conclusiones)
    X = "texto"
    lo_2000 = [R[(f"{a}-LO-VW", "2000-2025")] for a in ("OP", "NI", "VAR", "INV")]
    lo_post = [R[(f"{a}-LO-VW", "post")] for a in ("OP", "NI", "VAR", "INV")]
    C.num(X, "Resumen 2", "LO 2000-2025 x12 minimo", "x12", "0.8", min(r["x12"] for r in lo_2000))
    C.num(X, "Resumen 2", "LO 2000-2025 x12 maximo", "x12", "2.1", max(r["x12"] for r in lo_2000))
    C.num(X, "Resumen 2", "LO post x12 minimo", "x12", "0.15", min(r["x12"] for r in lo_post))
    C.num(X, "Resumen 2", "LO post x12 maximo", "x12", "0.72", max(r["x12"] for r in lo_post))
    C.num(X, "Conclusion 3", "LO 2000-2025 t minima", "t", "0.52", min(r["t"] for r in lo_2000))
    C.num(X, "Conclusion 3", "LO 2000-2025 t maxima", "t", "1.42", max(r["t"] for r in lo_2000))
    C.num(X, "Resumen 3 / Controles", "RMW 2000-ult x12", "x12", "4.48", R[("RMW", "2000-ult")]["x12"])
    C.num(X, "Resumen 3 / Controles", "RMW 2000-ult t", "t", "2.28", R[("RMW", "2000-ult")]["t"])
    C.num(X, "Controles", "RMW 2000-2025 x12", "x12", "4.76", R[("RMW", "2000-2025")]["x12"])
    C.num(X, "Controles", "RMW 2000-2025 t", "t", "2.43", R[("RMW", "2000-2025")]["t"])
    C.num(X, "Seccion 9 (Recompras)", "NI-LS-VW 2000-ult IC lo", "ic", "0.010", R[("NI-LS-VW", "2000-ult")]["lo"])
    C.num(X, "Seccion 9 (Recompras)", "NI-LS-VW 2000-ult IC hi", "ic", "0.872", R[("NI-LS-VW", "2000-ult")]["hi"])
    C.num(X, "Resumen 5 / Seccion 9", "VAR-LO-VW 2000-2025 Dif. CAGR", "dif", "1.49", D[("VAR-LO-VW", "2000-2025", "USD")]["dif"])
    C.num(X, "Resumen 6 / Conclusion 8", "NI-LS-EW post x12", "x12", "10.70", R[("NI-LS-EW", "post")]["x12"])
    C.num(X, "Resumen 6 / Conclusion 8", "NI-LS-EW post t", "t", "2.63", R[("NI-LS-EW", "post")]["t"])
    C.num(X, "Resumen 7 / Conclusion 7", "VAR-LO 2000-2025 USD vol cartera", "vol", "11.9", D[("VAR-LO-VW", "2000-2025", "USD")]["vol_p"])
    C.num(X, "Resumen 7 / Conclusion 7", "VAR-LO 2000-2025 USD vol mercado", "vol", "15.7", D[("VAR-LO-VW", "2000-2025", "USD")]["vol_m"])
    C.num(X, "Resumen 7 / Conclusion 7", "VAR-LO 2000-2025 USD MDD cartera", "mdd", "-36.5", D[("VAR-LO-VW", "2000-2025", "USD")]["mdd_p"])
    C.num(X, "Resumen 7 / Conclusion 7", "VAR-LO 2000-2025 USD MDD mercado", "mdd", "-50.3", D[("VAR-LO-VW", "2000-2025", "USD")]["mdd_m"])
    C.num(X, "Resumen 7 / Conclusion 7", "VAR-LO 2000-2025 MXN MDD cartera", "mdd", "-17.0", D[("VAR-LO-VW", "2000-2025", "MXN")]["mdd_p"])
    C.num(X, "Resumen 7 / Conclusion 7", "VAR-LO 2000-2025 MXN MDD mercado", "mdd", "-39.9", D[("VAR-LO-VW", "2000-2025", "MXN")]["mdd_m"])

    # Recuento (seccion 10 y Resumen 1)
    apoyos = [p for p in pruebas if R[(p[0], p[1])]["veredicto"] == "apoyo"]
    contrarias = [p for p in pruebas if R[(p[0], p[1])]["veredicto"] == "contraria"]
    prim = [(f"{a}-{t}-VW", v) for a in ("OP", "NI", "VAR", "INV") for t in ("LO", "LS") for v in ("2000-2025", "post")]
    mxn = [p for p in pruebas if p[2] == "MXN"]
    post_apoyo = sorted({p[0] for p in apoyos if p[1].endswith("post")})
    C.num(X, "Seccion 10", "pruebas registradas", "n", "103", len(pruebas))
    C.num(X, "Seccion 10", "pruebas con apoyo", "n", "25", len(apoyos))
    C.num(X, "Seccion 10 / Resumen 1", "primarias con apoyo (de 16)", "n", "0",
          sum(R[p]["veredicto"] == "apoyo" for p in prim))
    C.num(X, "Seccion 10 / Resumen 1", "MXN con apoyo (de 15)", "n", "0",
          sum(R[(p[0], p[1])]["veredicto"] == "apoyo" for p in mxn))
    C.cat(X, "Seccion 10", "unica serie con apoyo en post", "NI-LS-EW", ",".join(post_apoyo))
    C.num(X, "Tabla 1 (nota)", "pruebas contrarias", "n", "0", len(contrarias))
    C.num(X, "Controles", "faltantes -99.99/-999 en series usadas", "n", "0",
          sum(v for k, v in info["faltantes"].items() if k in ("ff3", "ff5", "OP", "NI", "VAR", "RESVAR", "INV")))
    C.cat(X, "Tabla 1 (nota)", "inicio de todas las series", "196307", ",".join(info["inicio_series"]))
    C.cat(X, "Datos", "rango Mkt (FF3)", "192607-202607", "-".join(info["ff3_rango"]))
    C.cat(X, "Datos", "rango DEXMXUS", "1993-11-08..2026-09-18", f"{info['fx']['primera']}..{info['fx']['ultima']}")

    # Criterio de afirmaciones (seccion 7 del pre-registro): +-0.30 pp en x12 o Dif. CAGR
    candidatos = {
        "Rentables 4.5%": (4.5, ["RMW", "OP-LS-VW", "OP-LO-VW", "OP-LS-EW"]),
        "Recompras 5.3%": (5.3, ["NI-LS-VW", "NI-LO-VW", "NI-LS-EW"]),
        "Baja volatilidad 3.6%": (3.6, ["VAR-LO-VW", "VAR-LS-VW", "VAR-LS-EW", "RESVAR-LO-VW", "RESVAR-LS-VW"]),
    }
    coincidencias = {}
    for afirm, (cifra, defs) in candidatos.items():
        hits = []
        for nombre in defs:
            for v in ("2000-2025", "2000-ult"):
                x12 = R[(nombre, v)]["x12"]
                if abs(x12 - cifra) <= 0.30:
                    hits.append(f"{nombre} {v} x12={x12:.2f}")
                if (nombre, v, "USD") in D:
                    dc = D[(nombre, v, "USD")]["dif"]
                    if abs(dc - cifra) <= 0.30:
                        hits.append(f"{nombre} {v} difCAGR={dc:.2f}")
        coincidencias[afirm] = hits
    rep = {
        "Rentables 4.5%": "RMW 2000-2025 x12; RMW 2000-ult x12; OP-LS-VW 2000-ult x12",
        "Recompras 5.3%": "NI-LS-VW 2000-ult x12",
        "Baja volatilidad 3.6%": "ninguna",
    }
    for afirm, hits in coincidencias.items():
        propio = "; ".join(h.split("=")[0].replace(" difCAGR", " difCAGR").replace(" x12", " x12") for h in hits) or "ninguna"
        C.cat(X, "Seccion 9 (criterio)", f"coincidencias '{afirm}'", rep[afirm], propio)
    return C, coincidencias


# ---------------------------------------------------------------------------
# 7. Salidas
# ---------------------------------------------------------------------------
def main():
    n_huellas = verificar_huellas()
    S, R, D, pruebas, info = calcular()
    C, coincidencias = comparar(R, D, pruebas, info)

    salida_json = {
        "fecha": "2026-09-25",
        "autor": "auditor-de-replicas (independiente.py, escrito sin leer reproducir.py)",
        "huellas_verificadas": n_huellas,
        "info": {k: v for k, v in info.items()},
        "pruebas": [{"serie": s, "ventana": v, "moneda": m, **{kk: vv for kk, vv in R[(s, v)].items()}}
                    for s, v, m in pruebas],
        "exploratorias": [{"serie": s, "ventana": v, **R[(s, v)]} for (s, v) in R if " Lo 10" in s],
        "descriptivo": [{"serie": s, "ventana": v, "moneda": m, **d} for (s, v, m), d in D.items()],
        "coincidencias_afirmaciones": coincidencias,
    }
    with open(os.path.join(BASE, "independiente-resultados.json"), "w", encoding="utf-8") as fh:
        json.dump(salida_json, fh, ensure_ascii=False, indent=1, default=str)
    with open(os.path.join(BASE, "independiente-comparacion.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(C.filas[0]))
        w.writeheader()
        for f in C.filas:
            g = dict(f)
            if isinstance(g["propio"], float):
                g["propio"] = "%.6f" % g["propio"]
                g["dif"] = "%.6f" % g["dif"]
            w.writerow(g)

    print(f"Huellas verificadas: {n_huellas} archivos")
    print(f"Pruebas registradas: {len(pruebas)}")
    print(f"Max |se formula1 - se formula2| = {info['max_dif_se_formulas_propias']:.2e}")
    print(f"Max |se propio - herramientas.estadistica| = {info['max_dif_se_vs_herramienta']}")
    print(f"Titulos de seccion usados: " + "; ".join(f"{k}: {info[k][0]} / {info[k][1]}" for k in info if k.endswith("_titulos")))
    print()
    # resumen por tabla
    por_tabla = {}
    for f in C.filas:
        t = por_tabla.setdefault(f["tabla"], {"n": 0, "ok": 0, "exacto": 0, "max": {}})
        t["n"] += 1
        t["ok"] += f["ok"]
        t["exacto"] += f["exacto_al_redondeo"]
        if f["tipo"] != "categoria":
            t["max"][f["tipo"]] = max(t["max"].get(f["tipo"], 0.0), abs(f["dif"]))
    print("| Bloque del README | Cifras comparadas | Dentro de tolerancia | Iguales al redondeo impreso | Mayor diferencia absoluta por tipo |")
    print("|---|---|---|---|---|")
    tot = [0, 0, 0]
    for k, t in por_tabla.items():
        mx = ", ".join(f"{tp} {v:.4f}" for tp, v in t["max"].items())
        print(f"| {k} | {t['n']} | {t['ok']} | {t['exacto']} | {mx} |")
        tot[0] += t["n"]; tot[1] += t["ok"]; tot[2] += t["exacto"]
    print(f"| **Total** | **{tot[0]}** | **{tot[1]}** | **{tot[2]}** | |")
    print()
    fuera = [f for f in C.filas if not f["ok"]]
    redondeo = [f for f in C.filas if f["ok"] and not f["exacto_al_redondeo"]]
    print(f"FUERA DE TOLERANCIA: {len(fuera)}")
    for f in fuera:
        print("  ", f["tabla"], "|", f["fila"], "|", f["campo"], "| rep", f["reportado"], "| propio",
              f["propio"] if not isinstance(f["propio"], float) else round(f["propio"], 4), "| dif",
              f["dif"] if f["dif"] == "" else round(f["dif"], 4))
    print(f"Dentro de tolerancia pero distinta al redondeo impreso: {len(redondeo)}")
    for f in redondeo:
        print("  ", f["tabla"], "|", f["fila"], "|", f["campo"], "| rep", f["reportado"], "| propio",
              f["propio"] if not isinstance(f["propio"], float) else round(f["propio"], 5), "| dif",
              f["dif"] if f["dif"] == "" else round(f["dif"], 5))
    print()
    print("Coincidencias con las afirmaciones (+-0.30 pp):")
    for k, v in coincidencias.items():
        print("  ", k, "->", v or "ninguna")
    return 0 if not fuera else 1


if __name__ == "__main__":
    sys.exit(main())
