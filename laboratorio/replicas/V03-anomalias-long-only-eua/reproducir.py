"""V03 - Anomalias de EUA (rentabilidad, recompras, baja volatilidad, baja inversion):
quintil 'bueno' menos mercado (LONG-ONLY, lo operable en GBM) y largo-corto academico.

Reproduce (desde la raiz del repo):
    python3 laboratorio/replicas/V03-anomalias-long-only-eua/reproducir.py
Sin red: datos congelados en ./datos (ver SHA256SUMS.txt). Pre-registro en prerregistro.md.
Salidas: resultados.json, variantes.csv y tablas en la salida estandar.
"""
import csv
import io
import json
import math
import os
import re
import statistics
import sys
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
from herramientas.estadistica import newey_west, veredicto, ic_bootstrap_bloques  # noqa: E402
from herramientas.huellas import verificar  # noqa: E402
from herramientas.datos_historicos import tabla_french  # noqa: E402  (solo para la doble verificacion)

REZAGOS = 6
FIN = 202607                 # ultimo mes de la version CRSP 202607
COSTO_LADO = 0.29 + 0.05     # % por lado: comision GBM 0.25%+IVA (hecho) + spread 0.05% (supuesto)
TOL_AFIRMACION = 0.30        # pp, criterio pre-registrado

# ----------------------------------------------------------------- integridad de datos
fallas = verificar(os.path.join(AQUI, "SHA256SUMS.txt"))
assert fallas == [], f"los datos congelados o el pre-registro cambiaron: {fallas}"


# ----------------------------------------------------------------- parser propio (implementacion A)
def texto_zip(nombre):
    with zipfile.ZipFile(os.path.join(AQUI, "datos", nombre)) as z:
        csvs = [n for n in z.namelist() if n.lower().endswith(".csv")]
        assert len(csvs) == 1, z.namelist()
        return z.read(csvs[0]).decode("latin-1")


def tablas_mensuales(texto):
    """Lista de (titulo, columnas, {yyyymm: [valores en % o None]}) de las tablas YYYYMM."""
    lineas = texto.replace("\r", "").split("\n")
    salida, ultimo_texto, i = [], "", 0
    while i < len(lineas):
        c = [x.strip() for x in lineas[i].split(",")]
        sig = [x.strip() for x in lineas[i + 1].split(",")] if i + 1 < len(lineas) else [""]
        if len(c) > 1 and c[0] == "" and re.fullmatch(r"\d{6}", sig[0]) and len(sig) == len(c):
            cols, filas, j = c[1:], {}, i + 1
            while j < len(lineas):
                s = [x.strip() for x in lineas[j].split(",")]
                if not re.fullmatch(r"\d{6}", s[0]) or len(s) != len(c):
                    break
                vals = []
                for v in s[1:]:
                    x = float(v)
                    vals.append(None if x in (-99.99, -999.0) else x)
                filas[int(s[0])] = vals
                j += 1
            salida.append((ultimo_texto, cols, filas))
            i = j
            continue
        if lineas[i].strip() and not re.fullmatch(r"\d{4,8}", c[0]):
            ultimo_texto = lineas[i].strip().strip(",").strip()
        i += 1
    return salida


def serie(tabla, col):
    titulo, cols, filas = tabla
    k = cols.index(col)
    return {m: v[k] for m, v in filas.items()}


def consecutivos(meses):
    idx = [m // 100 * 12 + m % 100 for m in meses]
    return all(b - a == 1 for a, b in zip(idx, idx[1:]))


# ----------------------------------------------------------------- carga
TX = {n: texto_zip(n) for n in [
    "F-F_Research_Data_Factors_CSV.zip", "F-F_Research_Data_5_Factors_2x3_CSV.zip",
    "Portfolios_Formed_on_OP_CSV.zip", "Portfolios_Formed_on_NI_CSV.zip",
    "Portfolios_Formed_on_VAR_CSV.zip", "Portfolios_Formed_on_RESVAR_CSV.zip",
    "Portfolios_Formed_on_INV_CSV.zip"]}
VERSION = {n: re.search(r"(\d{6}) CRSP", t).group(1) for n, t in TX.items()}
assert set(VERSION.values()) == {"202607"}, VERSION


def tabla_por_titulo(nombre, clave):
    ts = [t for t in tablas_mensuales(TX[nombre]) if clave.lower() in t[0].lower()]
    assert ts, (nombre, clave)
    return ts[0]


ff3 = tablas_mensuales(TX["F-F_Research_Data_Factors_CSV.zip"])[0]
ff5 = tablas_mensuales(TX["F-F_Research_Data_5_Factors_2x3_CSV.zip"])[0]
MKT = {m: a + b for (m, a), b in zip(serie(ff3, "Mkt-RF").items(), serie(ff3, "RF").values())}
RMW, CMA = serie(ff5, "RMW"), serie(ff5, "CMA")

VW, EW = {}, {}
for cod, arch in [("OP", "Portfolios_Formed_on_OP_CSV.zip"), ("NI", "Portfolios_Formed_on_NI_CSV.zip"),
                  ("VAR", "Portfolios_Formed_on_VAR_CSV.zip"), ("RESVAR", "Portfolios_Formed_on_RESVAR_CSV.zip"),
                  ("INV", "Portfolios_Formed_on_INV_CSV.zip")]:
    VW[cod] = tabla_por_titulo(arch, "Value Weight")
    EW[cod] = tabla_por_titulo(arch, "Equal Weight")
    assert "monthly" in VW[cod][0].lower() and "monthly" in EW[cod][0].lower(), (cod, VW[cod][0], EW[cod][0])

# ----------------------------------------------------------------- doble verificacion del parser
def comparar_con_herramientas(nombre, tabla_propia, seccion):
    t = tabla_french(TX[nombre], "mensual", seccion)
    _, cols, filas = tabla_propia
    assert [int(p) for p in t["periodos"]] == sorted(filas), nombre
    maxdif = 0.0
    for c in cols:
        for p, v in zip(t["periodos"], t["columnas"][c]):
            a = filas[int(p)][cols.index(c)]
            if a is None or v is None:
                assert a is None and v is None, (nombre, c, p)
                continue
            maxdif = max(maxdif, abs(a / 100 - v))
    assert maxdif < 1e-12, (nombre, maxdif)
    return maxdif


CHEQUEO_PARSER = {
    "FF3": comparar_con_herramientas("F-F_Research_Data_Factors_CSV.zip", ff3, 0),
    "FF5": comparar_con_herramientas("F-F_Research_Data_5_Factors_2x3_CSV.zip", ff5, 0),
}
for cod, arch in [("OP", "Portfolios_Formed_on_OP_CSV.zip"), ("NI", "Portfolios_Formed_on_NI_CSV.zip"),
                  ("VAR", "Portfolios_Formed_on_VAR_CSV.zip"), ("RESVAR", "Portfolios_Formed_on_RESVAR_CSV.zip"),
                  ("INV", "Portfolios_Formed_on_INV_CSV.zip")]:
    CHEQUEO_PARSER[cod + "-VW"] = comparar_con_herramientas(arch, VW[cod], 0)
    CHEQUEO_PARSER[cod + "-EW"] = comparar_con_herramientas(arch, EW[cod], 1)

# ----------------------------------------------------------------- tipo de cambio (MXN por USD)
fx_fin_mes = {}
with open(os.path.join(AQUI, "datos", "DEXMXUS.csv")) as f:
    lector = csv.reader(f)
    next(lector)
    for fecha, valor in lector:
        valor = valor.strip()
        if valor in ("", "."):
            continue
        m = int(fecha[:4]) * 100 + int(fecha[5:7])
        fx_fin_mes[m] = float(valor)  # el archivo viene ordenado: queda la ultima obs. del mes
mfx = sorted(fx_fin_mes)
assert consecutivos(mfx)
FX = {b: fx_fin_mes[b] / fx_fin_mes[a] - 1 for a, b in zip(mfx, mfx[1:])}  # decimal


# ----------------------------------------------------------------- definicion de series
def dif(a, b):
    return {m: (a[m] - b[m]) if a.get(m) is not None and b.get(m) is not None else None
            for m in sorted(set(a) & set(b))}


def col(tabla, c):
    return serie(tabla, c)


BUENO = {"OP": "Hi 20", "NI": "< 0", "VAR": "Lo 20", "RESVAR": "Lo 20", "INV": "Lo 20"}
MALO = {"OP": "Lo 20", "NI": "Hi 20", "VAR": "Hi 20", "RESVAR": "Hi 20", "INV": "Hi 20"}

SERIES = {}   # nombre -> dict(serie, pierna_larga, pierna_corta, tipo, primaria)
for cod in ["OP", "NI", "VAR", "INV", "RESVAR"]:
    larga = col(VW[cod], BUENO[cod])
    SERIES[f"{cod}-LO-VW"] = {"x": dif(larga, MKT), "larga": larga, "corta": MKT, "tipo": "LO",
                              "primaria": cod != "RESVAR", "def": f"{cod} {BUENO[cod]} VW - Mkt"}
    SERIES[f"{cod}-LS-VW"] = {"x": dif(larga, col(VW[cod], MALO[cod])), "larga": larga,
                              "corta": col(VW[cod], MALO[cod]), "tipo": "LS", "primaria": cod != "RESVAR",
                              "def": f"{cod} {BUENO[cod]} VW - {MALO[cod]} VW"}
for cod in ["OP", "NI", "VAR", "INV"]:
    larga, corta = col(EW[cod], BUENO[cod]), col(EW[cod], MALO[cod])
    SERIES[f"{cod}-LS-EW"] = {"x": dif(larga, corta), "larga": larga, "corta": corta, "tipo": "LS",
                              "primaria": False, "def": f"{cod} {BUENO[cod]} EW - {MALO[cod]} EW"}
SERIES["RMW"] = {"x": RMW, "larga": None, "corta": None, "tipo": "factor", "primaria": False,
                 "def": "Factor RMW 2x3 (robusta - debil)"}
SERIES["CMA"] = {"x": CMA, "larga": None, "corta": None, "tipo": "factor", "primaria": False,
                 "def": "Factor CMA 2x3 (conservadora - agresiva)"}

# Fecha de publicacion (ultimo mes 'pre'); verificada con Crossref (ver prerregistro.md)
PUB = {"OP": (201504, "Fama-French 2015, JFE 116(1), abr-2015"),
       "NI": (200804, "Pontiff-Woodgate 2008, JF 63(2), abr-2008"),
       "VAR": (200602, "Ang-Hodrick-Xing-Zhang 2006, JF 61(1), feb-2006"),
       "RESVAR": (200602, "Ang-Hodrick-Xing-Zhang 2006, JF 61(1), feb-2006"),
       "INV": (200808, "Cooper-Gulen-Schill 2008, JF 63(4), ago-2008"),
       "RMW": (201504, "Fama-French 2015"), "CMA": (201504, "Fama-French 2015")}
PUB_VARIANTE = {"OP": (201304, "Novy-Marx 2013, JFE 108(1), abr-2013 (rentabilidad bruta)"),
                "INV": (201504, "Fama-French 2015, JFE 116(1), abr-2015")}


def siguiente(m):
    return m + 1 if m % 100 < 12 else (m // 100 + 1) * 100 + 1


def ventanas_de(nombre):
    cod = nombre.split("-")[0]
    x = SERIES[nombre]["x"]
    inicio = min(m for m, v in x.items() if v is not None)
    p, _ = PUB[cod]
    w = {"completo": (inicio, FIN), "pre": (inicio, p), "2000-2025": (200001, 202512),
         "2000-ult": (200001, FIN), "post": (siguiente(p), FIN)}
    return w


# ----------------------------------------------------------------- estadistica
def nw_matriz(x, L):
    """Implementacion B de Newey-West: forma cuadratica con la matriz de Bartlett completa."""
    n = len(x)
    m = sum(x) / n
    u = [v - m for v in x]
    omega = 0.0
    for i in range(n):
        for j in range(max(0, i - L), min(n, i + L + 1)):
            omega += (1 - abs(i - j) / (L + 1)) * u[i] * u[j]
    omega /= n
    return math.sqrt(omega / (n - 1))


def tramo(d, a, b):
    ms = [m for m in sorted(d) if a <= m <= b]
    assert ms and consecutivos(ms), (a, b)
    faltan = [m for m in ms if d[m] is None]
    return ms, [d[m] for m in ms if d[m] is not None], faltan


def cagr(rend_pct):
    riqueza = 1.0
    for r in rend_pct:
        riqueza *= 1 + r / 100
    return (riqueza ** (12 / len(rend_pct)) - 1) * 100


def caida_maxima(rend_pct):
    riqueza, pico, peor = 1.0, 1.0, 0.0
    for r in rend_pct:
        riqueza *= 1 + r / 100
        pico = max(pico, riqueza)
        peor = min(peor, riqueza / pico - 1)
    return peor * 100


CHEQUEO_NW = {"max_dif_se": 0.0}


def estadistica(x, bootstrap=False):
    r = newey_west(x, REZAGOS)
    se_b = nw_matriz(x, REZAGOS)
    CHEQUEO_NW["max_dif_se"] = max(CHEQUEO_NW["max_dif_se"], abs(se_b - r["se"]))
    assert abs(se_b - r["se"]) < 1e-10, (se_b, r["se"])
    out = {"n": r["n"], "media_pct_mes": r["media"], "x12_pct": 12 * r["media"], "se": r["se"],
           "t_nw6": r["t"], "t_iid": r["t_iid"], "ic95": list(r["ic95"]), "veredicto": veredicto(r["ic95"]),
           "tau_equilibrio_pct": 12 * r["media"] / (2 * COSTO_LADO) * 100,
           "x12_neto_tau100_pct": 12 * r["media"] - 2 * COSTO_LADO}
    if bootstrap:
        out["ic95_bootstrap_bloques12"] = list(ic_bootstrap_bloques(x, 12, 5000, 7))
    return out


def descriptivo(larga, corta, a, b, fx=False):
    """CAGR, volatilidad y caida maxima de las dos piernas (en USD, o en MXN si fx)."""
    ms = [m for m in sorted(larga) if a <= m <= b]
    def conv(d):
        if not fx:
            return [d[m] for m in ms]
        return [((1 + d[m] / 100) * (1 + FX[m]) - 1) * 100 for m in ms]
    L_, C_ = conv(larga), conv(corta)
    return {"cagr_larga": cagr(L_), "cagr_corta": cagr(C_), "dif_cagr": cagr(L_) - cagr(C_),
            "vol_larga": statistics.stdev(L_) * math.sqrt(12), "vol_corta": statistics.stdev(C_) * math.sqrt(12),
            "dd_larga": caida_maxima(L_), "dd_corta": caida_maxima(C_)}


# ----------------------------------------------------------------- corridas registradas
RES = {"version_datos": VERSION, "costo_por_lado_pct": COSTO_LADO, "celdas": [], "mxn": [], "afirmaciones": {}}
VARIANTES = []


def registrar(serie_n, ventana, a, b, moneda="USD", pub_ref=None, primaria=False):
    s = SERIES[serie_n]
    if moneda == "USD":
        ms, x, faltan = tramo(s["x"], a, b)
    else:
        ms = [m for m in sorted(s["x"]) if a <= m <= b]
        assert consecutivos(ms) and all(m in FX for m in ms)
        faltan = [m for m in ms if s["x"][m] is None]
        x = [s["x"][m] * (1 + FX[m]) for m in ms if s["x"][m] is not None]  # (Rp - Rm)(1 + f)
    assert not faltan, (serie_n, ventana, faltan)
    boot = primaria and ventana in ("2000-2025", "post") and moneda == "USD"
    e = estadistica(x, bootstrap=boot)
    e.update({"serie": serie_n, "definicion": s["def"], "tipo": s["tipo"], "ventana": ventana,
              "desde": a, "hasta": b, "moneda": moneda, "primaria": primaria, "publicacion": pub_ref})
    if s["larga"] is not None:
        e["descriptivo"] = descriptivo(s["larga"], s["corta"], a, b, fx=(moneda == "MXN"))
    (RES["mxn"] if moneda == "MXN" else RES["celdas"]).append(e)
    VARIANTES.append({"serie": serie_n, "ventana": ventana, "desde": a, "hasta": b, "moneda": moneda,
                      "primaria": int(primaria), "es_prueba": 1, "n": e["n"],
                      "media_pct_mes": round(e["media_pct_mes"], 6), "t_nw6": round(e["t_nw6"], 4),
                      "veredicto": e["veredicto"], "nota": pub_ref or ""})
    return e


for nombre in SERIES:
    cod = nombre.split("-")[0]
    for v, (a, b) in ventanas_de(nombre).items():
        prim = SERIES[nombre]["primaria"] and v in ("2000-2025", "post")
        registrar(nombre, v, a, b, pub_ref=PUB[cod][1] if v in ("pre", "post") else None, primaria=prim)
# variantes de fecha de publicacion
for cod in ("OP", "INV"):
    p, ref = PUB_VARIANTE[cod]
    for tipo in ("LO", "LS"):
        nombre = f"{cod}-{tipo}-VW"
        inicio = ventanas_de(nombre)["completo"][0]
        registrar(nombre, "pre-variante", inicio, p, pub_ref=ref)
        registrar(nombre, "post-variante", siguiente(p), FIN, pub_ref=ref)
# MXN: solo long-only
for cod in ("OP", "NI", "VAR", "INV", "RESVAR"):
    nombre = f"{cod}-LO-VW"
    p, ref = PUB[cod]
    registrar(nombre, "mxn-completo", 199401, FIN, "MXN")
    registrar(nombre, "2000-2025", 200001, 202512, "MXN")
    registrar(nombre, "post", siguiente(p), FIN, "MXN", pub_ref=ref)


# ----------------------------------------------------------------- EXPLORATORIO (post-hoc)
# Desviacion declarada en README: ninguna definicion registrada reproduce "baja volatilidad 3.6%".
# Solo para buscar el origen de la cifra: deciles extremos VW de VAR y RESVAR. es_prueba=0; no entra
# a ningun veredicto ni cuenta como evidencia.
RES["exploratorio"] = []
for cod in ("VAR", "RESVAR"):
    lo10, hi10 = col(VW[cod], "Lo 10"), col(VW[cod], "Hi 10")
    for nombre, x in ((f"{cod}-LO10-VW", dif(lo10, MKT)), (f"{cod}-LS10-VW", dif(lo10, hi10))):
        for v, (a, b) in (("2000-2025", (200001, 202512)), ("2000-ult", (200001, FIN))):
            ms, xs, faltan = tramo(x, a, b)
            assert not faltan
            e = estadistica(xs)
            d = descriptivo(lo10, MKT if "LO10" in nombre else hi10, a, b)
            e.update({"serie": nombre, "ventana": v, "desde": a, "hasta": b, "dif_cagr": d["dif_cagr"],
                      "nota": "exploratorio post-hoc; no es prueba"})
            RES["exploratorio"].append(e)
            VARIANTES.append({"serie": nombre, "ventana": v, "desde": a, "hasta": b, "moneda": "USD",
                              "primaria": 0, "es_prueba": 0, "n": e["n"],
                              "media_pct_mes": round(e["media_pct_mes"], 6), "t_nw6": round(e["t_nw6"], 4),
                              "veredicto": e["veredicto"], "nota": "exploratorio post-hoc (origen de la cifra 3.6%)"})


# ----------------------------------------------------------------- afirmaciones recibidas
def celda(serie_n, ventana, moneda="USD"):
    lst = RES["mxn"] if moneda == "MXN" else RES["celdas"]
    return next(c for c in lst if c["serie"] == serie_n and c["ventana"] == ventana)


AFIRMACIONES = {"rentables 4.5%": (4.5, ["RMW", "OP-LS-VW", "OP-LO-VW", "OP-LS-EW"], "OP"),
                "recompras 5.3%": (5.3, ["NI-LS-VW", "NI-LO-VW", "NI-LS-EW"], "NI"),
                "baja volatilidad 3.6% extra": (3.6, ["VAR-LO-VW", "VAR-LS-VW", "VAR-LS-EW",
                                                      "RESVAR-LO-VW", "RESVAR-LS-VW"], "VAR")}
for texto, (cifra, candidatas, cod) in AFIRMACIONES.items():
    filas, coinciden = [], []
    for s_n in candidatas:
        for v in ("2000-2025", "2000-ult"):
            c = celda(s_n, v)
            metr = {"x12": c["x12_pct"]}
            if "descriptivo" in c:
                metr["dif_cagr"] = c["descriptivo"]["dif_cagr"]
            for k, val in metr.items():
                ok = abs(val - cifra) <= TOL_AFIRMACION
                filas.append({"serie": s_n, "ventana": v, "metrica": k, "valor": val, "coincide": ok,
                              "t_nw6": c["t_nw6"], "veredicto": c["veredicto"]})
                if ok:
                    coinciden.append(f"{s_n} {v} {k}={val:.2f}")
    lo = f"{cod}-LO-VW"
    RES["afirmaciones"][texto] = {
        "cifra": cifra, "candidatas": filas, "coinciden": coinciden,
        "LO_VW_2000_2025": celda(lo, "2000-2025")["veredicto"], "LO_VW_post": celda(lo, "post")["veredicto"],
        "LO_VW_MXN_post": celda(lo, "post", "MXN")["veredicto"]}
RES["chequeos"] = {"parser_max_dif_vs_herramientas": CHEQUEO_PARSER, "nw_max_dif_se": CHEQUEO_NW["max_dif_se"],
                   "n_pruebas": sum(v["es_prueba"] for v in VARIANTES),
                   "n_exploratorias": sum(1 - v["es_prueba"] for v in VARIANTES)}

with open(os.path.join(AQUI, "resultados.json"), "w") as f:
    json.dump(RES, f, indent=1, ensure_ascii=False)
with open(os.path.join(AQUI, "variantes.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(VARIANTES[0]))
    w.writeheader()
    w.writerows(VARIANTES)

# ----------------------------------------------------------------- tablas
def fila(c):
    ic = c["ic95"]
    return (f"| {c['serie']} | {c['ventana']} | {c['desde']}-{c['hasta']} | {c['n']} | {c['media_pct_mes']:.3f} | "
            f"{c['x12_pct']:.2f} | {c['t_nw6']:.2f} | [{ic[0]:.3f}, {ic[1]:.3f}] | {c['veredicto']} |")


print(f"Version datos: {VERSION}")
print(f"Chequeos: parser max dif = {max(CHEQUEO_PARSER.values()):.1e}; NW max dif se = {CHEQUEO_NW['max_dif_se']:.1e}; "
      f"pruebas registradas = {RES['chequeos']['n_pruebas']}; exploratorias = {RES['chequeos']['n_exploratorias']}")
print("\n| Serie | Ventana | Meses | n | Media %/mes | x12 % | t NW(6) | IC95 %/mes | Veredicto |")
print("|---|---|---|---|---|---|---|---|---|")
for c in RES["celdas"]:
    print(fila(c))
print("\nMXN (exceso long-only sobre el mercado, ambos convertidos con DEXMXUS)")
print("| Serie | Ventana | Meses | n | Media %/mes | x12 % | t NW(6) | IC95 %/mes | Veredicto |")
print("|---|---|---|---|---|---|---|---|---|")
for c in RES["mxn"]:
    print(fila(c))
print("\nDescriptivo long-only (CAGR %, vol %, caida max %): cartera vs mercado")
print("| Serie | Ventana | Moneda | CAGR cartera | CAGR mercado | Dif CAGR | Vol cartera | Vol mercado | DD cartera | DD mercado |")
print("|---|---|---|---|---|---|---|---|---|---|")
for c in RES["celdas"] + RES["mxn"]:
    if c["tipo"] == "LO" and c["ventana"] in ("completo", "2000-2025", "post", "mxn-completo"):
        d = c["descriptivo"]
        print(f"| {c['serie']} | {c['ventana']} | {c['moneda']} | {d['cagr_larga']:.2f} | {d['cagr_corta']:.2f} | "
              f"{d['dif_cagr']:+.2f} | {d['vol_larga']:.1f} | {d['vol_corta']:.1f} | {d['dd_larga']:.1f} | {d['dd_corta']:.1f} |")
print("\nBootstrap de bloques (12 meses, 5000, semilla 7), primarias")
for c in RES["celdas"]:
    if "ic95_bootstrap_bloques12" in c:
        b = c["ic95_bootstrap_bloques12"]
        print(f"| {c['serie']} | {c['ventana']} | [{c['ic95'][0]:.3f}, {c['ic95'][1]:.3f}] | [{b[0]:.3f}, {b[1]:.3f}] |")
print("\nCostos: rotacion de equilibrio tau* (% anual una via) y x12 neto con tau=100%, primarias LO")
for c in RES["celdas"]:
    if c["tipo"] == "LO" and c["ventana"] in ("2000-2025", "post") and c["primaria"]:
        print(f"| {c['serie']} | {c['ventana']} | x12={c['x12_pct']:.2f} | tau*={c['tau_equilibrio_pct']:.0f}% | "
              f"neto(tau=100%)={c['x12_neto_tau100_pct']:.2f} |")
print("\nEXPLORATORIO post-hoc (no es prueba): deciles extremos VW de volatilidad")
for c in RES["exploratorio"]:
    print(f"| {c['serie']} | {c['ventana']} | {c['n']} | x12={c['x12_pct']:.2f} | dif_cagr={c['dif_cagr']:.2f} | "
          f"t={c['t_nw6']:.2f} | [{c['ic95'][0]:.3f}, {c['ic95'][1]:.3f}] | {c['veredicto']} |")
print("\nAfirmaciones")
for k, v in RES["afirmaciones"].items():
    print(f"* {k}: coinciden -> {v['coinciden'] or 'ninguna'}; LO-VW 2000-2025={v['LO_VW_2000_2025']}, "
          f"post={v['LO_VW_post']}, MXN post={v['LO_VW_MXN_post']}")
    for r in v["candidatas"]:
        print(f"    {r['serie']:14s} {r['ventana']:9s} {r['metrica']:8s} {r['valor']:6.2f} t={r['t_nw6']:5.2f} "
              f"{r['veredicto']:10s} {'<- coincide' if r['coincide'] else ''}")
