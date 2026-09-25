"""R01 - Replica de Faber (2007): timing con media movil de 10 meses sobre el mercado de EUA.

Reproduce (desde la raiz del repo):   python3 laboratorio/replicas/R01.py
Prueba del codigo con datos sinteticos (sin red, sin tocar el registro real):
                                      python3 laboratorio/replicas/R01.py --prueba-sintetica

Articulo: Faber, M. T. (2007), "A Quantitative Approach to Tactical Asset Allocation",
Journal of Wealth Management 9(4): 69-79 (SSRN 962461; working paper 2006, actualizacion 2013).

Datos (ver ficha R01-timing-sma10-faber.md, seccion 3):
  - French F-F_Research_Data_Factors mensual, CRSP 202607 (principal) y vintages CRSP 202407 (FIZ)
    y 200607. Congelados en R01-datos/ y verificados contra R01-datos/SHA256SUMS.txt.
  - Yahoo ^GSPC diario (senal sobre indice de precio), FRED DEXMXUS e INTGSTMXM193N (moneda):
    se descargan con herramientas/datos_historicos.py (no se congelan; condiciones de uso pendientes).
Motor: herramientas/backtest.py. Cada corrida se agrega a R01-variantes.csv (nunca se borra).
Salidas: R01-variantes.csv, R01-resultados.json y R01-salida.txt (copia de lo impreso).
Analisis post-hoc (no pre-registrado, agregado tras la corrida 1): bootstrap_pareado. Se marca asi en la salida.
Solo biblioteca estandar.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import random
import re
import statistics
import sys
import tempfile
import zipfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(RAIZ))

from herramientas import backtest as bt  # noqa: E402
from herramientas import datos_historicos as dh  # noqa: E402
from herramientas.estadistica import newey_west  # noqa: E402
from herramientas.huellas import sha256 as sha256_archivo  # noqa: E402
from herramientas.huellas import verificar  # noqa: E402

ID = "R01"
CORTE = date(2006, 12, 31)
MIN_HISTORIA = 12
FICHA = AQUI / "R01-timing-sma10-faber.md"
# sha256 de las secciones 1-9 (de "## PRE-REGISTRO" a "## RESULTADOS"), calculado el 2026-09-25 05:22 UTC
SHA_PRE_REGISTRO = "679f434ac371d0a88cfc1d84933ea40b5ae8c84268a9aca27ee4b30bd0e2e936"
DIR_DATOS = AQUI / "R01-datos"
URL_ARCHIVO = ("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/"
               "Historical_Archives/")
VINTAGES = {  # version_crsp -> (ruta relativa en R01-datos, url de descarga si falta)
    "202607": ("202607/F-F_Research_Data_Factors_CSV.zip", None),
    "202407": ("202407/F-F_Research_Data_Factors_CSV.zip",
               URL_ARCHIVO + "08%202024%20Update/ftp/F-F_Research_Data_Factors_CSV.zip"),
    "200607": ("200607/F-F_Research_Data_Factors_TXT.zip",
               URL_ARCHIVO + "08%202006%20Update/ftp/F-F_Research_Data_Factors_TXT.zip"),
}
C_GBM = bt.COMISION_GBM_POR_LADO           # 0.0029 (hecho, Guia GBM V1025)
S_LIQ = bt.SPREAD_POR_LADO["liquido"]       # 0.0005 (supuesto [I])
COSTOS = {
    "defecto": (C_GBM, S_LIQ),
    "sin_costos": (0.0, 0.0),
    "spread_medio": (C_GBM, bt.SPREAD_POR_LADO["medio"]),
    "spread_iliquido": (C_GBM, bt.SPREAD_POR_LADO["iliquido"]),
    "doble_pierna": (2 * C_GBM, 2 * S_LIQ),
}
VENTANAS = (6, 8, 10, 12)
# Tramos del articulo (se calculan sobre las series de las corridas; no se registran aparte)
TRAMO_2006 = (date(1927, 7, 31), date(2005, 12, 31))   # vs Tabla 2 del working paper 2006 (1900-2005)
TRAMO_2013 = (date(1927, 7, 31), date(2012, 12, 31))   # vs actualizacion 2013 (1901-2012)
# Ventanas de la adenda del 2026-09-25 (operacionalizacion de "solo en algunos subperiodos")
VENTANAS_DECADA_DENTRO = [(date(1927, 7, 31), date(1929, 12, 31))] + \
    [(date(a, 1, 31), date(a + 9, 12, 31)) for a in range(1930, 2000, 10)] + \
    [(date(2000, 1, 31), date(2006, 12, 31))]
VENTANAS_DECADA_FUERA = [(date(2007, 1, 31), date(2009, 12, 31)), (date(2010, 1, 31), date(2019, 12, 31)),
                         (date(2020, 1, 31), date(2026, 7, 31))]
# Cifras del articulo (verificadas en los PDF el 2026-09-25; ver ficha, seccion 1)
FABER_2006 = {"cagr_bh": 0.0975, "cagr_t": 0.1066, "sd_bh": 0.1991, "sd_t": 0.1538, "sharpe_bh": 0.29,
              "sharpe_t": 0.43, "mdd_bh": -0.8366, "mdd_t_tabla": -0.4998, "mdd_t_texto": -0.4224,
              "mar_bh": 0.14, "mar_t": 0.23, "ulcer_bh": 0.2033, "ulcer_t": 0.1170, "invertido_t": 0.6977,
              "rt_anio": 0.67, "pct_oper_pos": 0.63, "mejor_bh": 0.5288, "mejor_t": 0.5240,
              "peor_bh": -0.4386, "peor_t": -0.2669, "media_arit_bh": 0.1166, "media_arit_t": 0.1172,
              "pct_anios_debajo": 0.40}
FABER_2013 = {"cagr_bh": 0.0932, "cagr_t": 0.1018, "mdd_bh": -0.8366, "mdd_t": -0.4224,
              "media_arit_bh": 0.1126, "media_arit_t": 0.1122, "invertido_t": 0.70, "pct_anios_debajo": 0.50}


# ============================================================== salida (pantalla + archivo)

class Salida:
    def __init__(self):
        self.lineas: list[str] = []

    def __call__(self, *partes):
        texto = " ".join(str(p) for p in partes)
        print(texto)
        self.lineas.append(texto)


P = Salida()


# ============================================================== utilidades

def verificar_pre_registro() -> str:
    t = FICHA.read_text(encoding="utf-8")
    i, j = t.index("## PRE-REGISTRO"), t.index("## RESULTADOS")
    h = hashlib.sha256(t[i:j].encode("utf-8")).hexdigest()
    if h != SHA_PRE_REGISTRO:
        raise SystemExit(f"El pre-registro (secciones 1-9) cambio: sha256 {h} != {SHA_PRE_REGISTRO}. "
                         "Los cambios van en 'Desviaciones del pre-registro', no en las secciones 1-9.")
    return h


def meses_consecutivos(serie, nombre: str) -> None:
    idx = [f.year * 12 + f.month for f, _ in serie]
    huecos = [(serie[k][0], serie[k + 1][0]) for k in range(len(idx) - 1) if idx[k + 1] - idx[k] != 1]
    if huecos:
        raise SystemExit(f"{nombre}: meses no consecutivos {huecos[:5]}")


def texto_de_zip(contenido: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(contenido)) as z:
        nombres = [n for n in z.namelist() if not n.endswith("/")]
        if len(nombres) != 1:
            raise SystemExit(f"Se esperaba un archivo en el zip; hay {nombres}")
        crudo = z.read(nombres[0])
    try:
        return crudo.decode("utf-8")
    except UnicodeDecodeError:
        return crudo.decode("latin-1")


def txt_french_a_csv(texto: str) -> str:
    """Formato TXT antiguo de French (columnas separadas por espacios) -> CSV del formato actual."""
    salida = []
    for linea in texto.splitlines():
        s = linea.strip()
        partes = s.split()
        if partes and "Mkt-RF" in partes and not s[0].isdigit():
            salida.append("," + ",".join(partes))
        elif re.match(r"^\d{4,8}\s", s):
            salida.append(",".join(partes))
        else:
            salida.append(linea)
    return "\n".join(salida)


def huella_serie(serie) -> str:
    return hashlib.sha256(repr([(f.isoformat(), round(v, 12)) for f, v in serie]).encode()).hexdigest()[:16]


def pct(x, d=2) -> str:
    return "NA" if x is None else f"{100 * x:.{d}f}%"


def num(x, d=3) -> str:
    return "NA" if x is None else ("inf" if isinstance(x, float) and math.isinf(x) else f"{x:.{d}f}")


# ============================================================== datos reales

def asegurar_datos_congelados() -> None:
    for vintage, (rel, url) in VINTAGES.items():
        ruta = DIR_DATOS / rel
        if ruta.exists():
            continue
        ruta.parent.mkdir(parents=True, exist_ok=True)
        if url is None:  # principal: se descarga la version vigente (probablemente otra -> falla la huella)
            dh.french("F-F_Research_Data_Factors", "mensual", dir_cache=ruta.parent)
        else:
            ruta.write_bytes(dh._descargar_binario(url))
    fallas = verificar(str(DIR_DATOS / "SHA256SUMS.txt"))
    if fallas:
        raise SystemExit(f"Datos congelados distintos a los del pre-registro: {fallas}. French publica versiones "
                         "nuevas cada mes; esta replica exige los bytes exactos de R01-datos/SHA256SUMS.txt.")


def cargar_french(vintage: str) -> dict:
    rel, _ = VINTAGES[vintage]
    ruta = DIR_DATOS / rel
    texto = texto_de_zip(ruta.read_bytes())
    if rel.endswith("_TXT.zip"):
        texto = txt_french_a_csv(texto)
    tabla = dh.tabla_french(texto, "mensual")
    if tabla["version_crsp"] != vintage:
        raise SystemExit(f"Vintage esperado {vintage}, archivo dice {tabla['version_crsp']}")
    if tabla["faltantes"]:
        raise SystemExit(f"French {vintage}: {tabla['faltantes']} faltantes (no se imputan)")
    mercado = dh.rendimiento_mercado_french(tabla)
    rf = dh.columna(tabla, "RF")
    if len(mercado) != len(tabla["fechas"]) or len(rf) != len(tabla["fechas"]):
        raise SystemExit(f"French {vintage}: filas descartadas por faltantes")
    meses_consecutivos(mercado, f"French {vintage}")
    return {"vintage": vintage, "mercado": mercado, "rf": rf, "sha256": sha256_archivo(str(ruta)),
            "ruta": str(ruta.relative_to(RAIZ)), "notas": tabla["notas"],
            "rango": (tabla["fechas"][0], tabla["fechas"][-1]), "n": len(tabla["fechas"])}


def gspc_fin_de_mes() -> dict:
    h = dh.yahoo_historia("^GSPC", "1d")
    ultimo: dict = {}
    for f, p in zip(h["fechas"], h["precios"]):
        if p is not None and p > 0:
            ultimo[(f.year, f.month)] = (f, p)
    meses = sorted(ultimo)[:-1]  # el ultimo mes con datos se considera incompleto y se descarta
    serie = [(dh.a_fin_de_mes(ultimo[k][0]), ultimo[k][1]) for k in meses]
    meses_consecutivos(serie, "^GSPC fin de mes")
    return {"serie": serie, "rango_diario": (h["fechas"][0], h["fechas"][-1]), "n_diario": len(h["fechas"]),
            "fechas_sin_precio": [str(x) for x in h.get("fechas_sin_precio", [])],
            "usa_adjclose": h.get("usa_adjclose"), "adjclose_difiere_de_close": h.get("adjclose_difiere_de_close"),
            "huella": huella_serie(serie), "url": h.get("url")}


def cargar_mxn() -> dict:
    fx = dh.fred("DEXMXUS")
    cetes_tasa = dh.fred("INTGSTMXM193N")
    cetes = [(dh.a_fin_de_mes(f), v / 1200.0) for f, v in cetes_tasa]
    meses_consecutivos(cetes, "INTGSTMXM193N")
    return {"fx": fx, "cetes": cetes, "fx_rango": (fx[0][0], fx[-1][0]), "fx_n": len(fx),
            "cetes_rango": (cetes[0][0], cetes[-1][0]), "cetes_n": len(cetes),
            "fx_huella": huella_serie(fx), "cetes_huella": huella_serie(cetes)}


def datos_reales() -> dict:
    asegurar_datos_congelados()
    d = {"french": {v: cargar_french(v) for v in VINTAGES}}
    d["gspc"] = gspc_fin_de_mes()
    d["mxn"] = cargar_mxn()
    return d


# ============================================================== datos sinteticos (solo prueba del codigo)

def datos_sinteticos() -> dict:
    rnd = random.Random(12345)

    def meses(a0, m0, a1, m1):
        salida, a, m = [], a0, m0
        while (a, m) <= (a1, m1):
            salida.append(dh.fin_de_mes(a, m))
            m += 1
            if m == 13:
                a, m = a + 1, 1
        return salida

    def french_falso(vintage, a1, m1):
        fechas = meses(1926, 7, a1, m1)
        mercado = [(f, rnd.gauss(0.008, 0.05)) for f in fechas]
        rf = [(f, 0.003) for f in fechas]
        return {"vintage": vintage, "mercado": mercado, "rf": rf, "sha256": "sintetico", "ruta": "sintetico",
                "notas": [], "rango": (fechas[0], fechas[-1]), "n": len(fechas)}

    french = {"202607": french_falso("202607", 2026, 7), "202407": french_falso("202407", 2024, 7),
              "200607": french_falso("200607", 2006, 7)}
    nivel, gspc = 100.0, []
    for f in meses(1927, 12, 2026, 8):
        nivel *= 1 + rnd.gauss(0.005, 0.05)
        gspc.append((f, nivel))
    fx, dia, v = [], date(1993, 11, 8), 3.1
    while dia <= date(2026, 9, 18):
        if dia.weekday() < 5:
            v *= 1 + rnd.gauss(0.0001, 0.006)
            fx.append((dia, v))
        dia += timedelta(days=1)
    cetes = [(f, 0.005) for f in meses(1986, 10, 2026, 7)]
    return {"french": french,
            "gspc": {"serie": gspc, "rango_diario": None, "n_diario": 0, "fechas_sin_precio": [],
                     "usa_adjclose": None, "adjclose_difiere_de_close": None, "huella": "sintetico", "url": None},
            "mxn": {"fx": fx, "cetes": cetes, "fx_rango": (fx[0][0], fx[-1][0]), "fx_n": len(fx),
                    "cetes_rango": (cetes[0][0], cetes[-1][0]), "cetes_n": len(cetes),
                    "fx_huella": "sintetico", "cetes_huella": "sintetico"}}


# ============================================================== senales propias (funciones puras de h)

def senal_sma_con_rezago(ventana: int, rezago: int):
    """Como senal_media_movil(ventana), pero decide t con datos hasta t-1-rezago."""
    def senal(h):
        if len(h.indice) < ventana + rezago:
            raise ValueError("historia insuficiente para la SMA con rezago")
        serie = h.indice[len(h.indice) - ventana - rezago:len(h.indice) - rezago]
        return 1.0 if serie[-1] > statistics.fmean(serie) else 0.0
    senal.__qualname__ = senal.__name__ = f"media_movil_{ventana}_rezago_{rezago}"
    return senal


def senal_sma_sobre_extra(nombre: str, ventana: int):
    """SMA sobre una serie externa de niveles (p. ej. ^GSPC de precio) visible hasta t-1."""
    def senal(h):
        serie = h.extras[nombre]
        if len(serie) < ventana:
            raise ValueError(f"{nombre}: historia insuficiente")
        ultimos = serie[-ventana:]
        if ultimos[-1][0] != h.fecha_decision:
            raise ValueError(f"{nombre}: ultimo dato {ultimos[-1][0]} != fecha de decision {h.fecha_decision}")
        valores = [v for _, v in ultimos]
        return 1.0 if valores[-1] > statistics.fmean(valores) else 0.0
    senal.__qualname__ = senal.__name__ = f"media_movil_{ventana}_sobre_{nombre}"
    return senal


# ============================================================== corridas

class Corredor:
    def __init__(self, registrar: bool, dir_replicas=None):
        self.registrar = registrar
        self.dir_replicas = dir_replicas
        self.res: dict[str, bt.ResultadoBacktest] = {}
        self.bloque: dict[str, str] = {}

    def __call__(self, clave, activo, efectivo, senal, *, bloque, costo="defecto", es_prueba=False,
                 nota="", parametros=None, **kw):
        if clave in self.res:
            raise ValueError(f"variante repetida: {clave}")
        com, spr = COSTOS[costo]
        kw.setdefault("cortes", [CORTE])
        kw.setdefault("min_historia", MIN_HISTORIA)
        par = {"bloque": bloque, "escenario_costos": costo}
        par.update(parametros or {})
        r = bt.backtest_senal(activo, efectivo, senal, id_replica=ID if self.registrar else None,
                              variante=clave, comision_por_lado=com, spread_por_lado=spr,
                              parametros=par, es_prueba=es_prueba, nota=nota,
                              dir_replicas=self.dir_replicas, **kw)
        self.res[clave] = r
        self.bloque[clave] = bloque
        return r


def correr_todo(d: dict, corr: Corredor) -> None:
    f = d["french"]["202607"]
    mkt, rf = f["mercado"], f["rf"]
    fuente = f"French F-F_Research_Data_Factors CRSP {f['vintage']} sha256 {f['sha256'][:12]}"
    reglas = {f"sma{n}": (bt.senal_media_movil(n), {"ventana": n, "senal_sobre": "indice TR (Mkt-RF+RF)"})
              for n in VENTANAS}
    reglas["mom12"] = (bt.senal_momentum_absoluto(12), {"ventana": 12, "regla": "momentum absoluto vs RF"})
    # A. Principal (es_prueba=1)
    for nombre, (senal, par) in reglas.items():
        corr(nombre, mkt, rf, senal, bloque="A", es_prueba=True, parametros=par, fuente_datos=fuente,
             nota="principal; costos GBM por defecto")
    # B. Referencias
    corr("comprar_y_mantener", mkt, rf, bt.senal_comprar_y_mantener, bloque="B", fuente_datos=fuente,
         nota="referencia")
    corr("efectivo", mkt, rf, bt.senal_efectivo, bloque="B", fuente_datos=fuente, nota="referencia")
    # C. Costos
    for costo in ("sin_costos", "spread_medio", "spread_iliquido", "doble_pierna"):
        for nombre, (senal, par) in list(reglas.items()) + [("comprar_y_mantener",
                                                             (bt.senal_comprar_y_mantener, {}))]:
            corr(f"{nombre}|{costo}", mkt, rf, senal, bloque="C", costo=costo, parametros=par,
                 fuente_datos=fuente, nota=f"sensibilidad de costos: {costo}")
    # D. Ejecucion: rezago de 1 mes
    corr("sma10|rezago1m", mkt, rf, senal_sma_con_rezago(10, 1), bloque="D",
         parametros={"ventana": 10, "rezago_meses": 1}, fuente_datos=fuente,
         nota="sensibilidad de ejecucion: decide t con datos hasta t-2")
    # E. Vintages de French
    for vintage in ("202407", "200607"):
        fv = d["french"][vintage]
        fuente_v = f"French F-F_Research_Data_Factors CRSP {vintage} sha256 {fv['sha256'][:12]}"
        for costo in ("defecto", "sin_costos"):
            corr(f"sma10|vintage{vintage}|{costo}", fv["mercado"], fv["rf"], bt.senal_media_movil(10),
                 bloque="E", costo=costo, parametros={"ventana": 10, "vintage": vintage},
                 fuente_datos=fuente_v, nota=f"sensibilidad de datos: vintage {vintage}, {costo}")
            corr(f"comprar_y_mantener|vintage{vintage}|{costo}", fv["mercado"], fv["rf"],
                 bt.senal_comprar_y_mantener, bloque="E", costo=costo, parametros={"vintage": vintage},
                 fuente_datos=fuente_v, nota=f"sensibilidad de datos: vintage {vintage}, {costo}")
    # F. Senal sobre indice de precio (^GSPC) en muestra comun desde 1928-01
    inicio_f = date(1928, 1, 31)
    mkt_f = [x for x in mkt if x[0] >= inicio_f]
    rf_f = [x for x in rf if x[0] >= inicio_f]
    gspc = d["gspc"]["serie"]
    fuente_f = fuente + f"; Yahoo ^GSPC diario->fin de mes huella {d['gspc']['huella']}"
    corr("sma10|muestra1928", mkt_f, rf_f, bt.senal_media_movil(10), bloque="F",
         parametros={"ventana": 10, "senal_sobre": "indice TR"}, fuente_datos=fuente_f,
         nota="sensibilidad de senal: TR en muestra comun desde 1928-01")
    corr("sma10_precio_gspc|muestra1928", mkt_f, rf_f, senal_sma_sobre_extra("gspc", 10), bloque="F",
         extras={"gspc": gspc}, parametros={"ventana": 10, "senal_sobre": "^GSPC precio"},
         fuente_datos=fuente_f, nota="sensibilidad de senal: ^GSPC precio sin dividendos")
    corr("comprar_y_mantener|muestra1928", mkt_f, rf_f, bt.senal_comprar_y_mantener, bloque="F",
         fuente_datos=fuente_f, nota="referencia de la muestra comun desde 1928-01")
    # G. Moneda MXN (senal en USD)
    fx, cetes = d["mxn"]["fx"], d["mxn"]["cetes"]
    for nombre_ef, efectivo, en_mxn in (("rf_usd", rf, False), ("cetes", cetes, True)):
        fuente_g = fuente + f"; FRED DEXMXUS huella {d['mxn']['fx_huella']}" + \
            (f"; FRED INTGSTMXM193N/1200 huella {d['mxn']['cetes_huella']}" if en_mxn else "")
        for nombre, senal in (("sma10", bt.senal_media_movil(10)), ("comprar_y_mantener", bt.senal_comprar_y_mantener),
                              ("efectivo", bt.senal_efectivo)):
            corr(f"{nombre}|mxn|{nombre_ef}", mkt, efectivo, senal, bloque="G", fx=fx, efectivo_en_mxn=en_mxn,
                 parametros={"moneda": "MXN", "efectivo": nombre_ef}, fuente_datos=fuente_g,
                 nota=f"sensibilidad de moneda: MXN, efectivo {nombre_ef}")


# ============================================================== analisis

def indices_tramo(r: bt.ResultadoBacktest, desde: date, hasta: date) -> tuple[int, int]:
    idx = [i for i, f in enumerate(r.fechas) if desde <= f <= hasta]
    if not idx:
        raise ValueError(f"sin periodos entre {desde} y {hasta}")
    return idx[0], idx[-1] + 1


def metricas_tramo(r: bt.ResultadoBacktest, desde: date, hasta: date) -> dict:
    i0, i1 = indices_tramo(r, desde, hasta)
    f0 = r.curva[i0][0]
    exp0 = r.parametros["exposicion_inicial"]
    cambios = sum(1 for k in range(i0, i1) if r.exposicion[k] != (r.exposicion[k - 1] if k > 0 else exp0))
    return bt.metricas_de_periodos(r.fechas[i0:i1], f0, r.r_neto[i0:i1], r.r_efectivo[i0:i1],
                                   r.exposicion[i0:i1], r.rotacion[i0:i1], r.costo[i0:i1],
                                   r.r_activo[i0:i1], r.parametros["periodos_por_anio"], cambios)


def estilo_faber(r: bt.ResultadoBacktest, desde: date, hasta: date) -> dict:
    """Estadisticas comparables con la Tabla 2 del working paper 2006."""
    i0, i1 = indices_tramo(r, desde, hasta)
    fechas, rn, exp, ra = r.fechas[i0:i1], r.r_neto[i0:i1], r.exposicion[i0:i1], r.r_activo[i0:i1]
    por_anio: dict[int, list] = {}
    for f, x in zip(fechas, rn):
        por_anio.setdefault(f.year, []).append(x)
    anios = sorted(a for a, xs in por_anio.items() if len(xs) == 12)
    anuales = {a: math.prod(1 + x for x in por_anio[a]) - 1 for a in anios}
    vals = list(anuales.values())
    nivel, maximo, dds = 1.0, 1.0, []
    for x in rn:
        nivel *= 1 + x
        maximo = max(maximo, nivel)
        dds.append(nivel / maximo - 1)
    ulcer = math.sqrt(statistics.fmean(d * d for d in dds))
    # operaciones: tramos consecutivos con exposicion 1; rendimiento del activo mientras se sostiene
    operaciones, actual = [], None
    for w, x in zip(exp, ra):
        if w == 1.0:
            actual = (actual if actual is not None else 1.0) * (1 + x)
        elif actual is not None:
            operaciones.append(actual - 1)
            actual = None
    if actual is not None:
        operaciones.append(actual - 1)
    salidas = sum(1 for k in range(1, len(exp)) if exp[k - 1] == 1.0 and exp[k] == 0.0)
    anios_tramo = (fechas[-1] - r.curva[i0][0]).days / 365.25
    m = metricas_tramo(r, desde, hasta)
    media = statistics.fmean(vals)
    sd = statistics.stdev(vals)
    return {"anios_completos": (anios[0], anios[-1], len(anios)), "anuales": anuales,
            "cagr": m["cagr"], "media_aritmetica_anual": media, "sd_anual_calendario": sd,
            "vol_mensual_anualizada": m["vol_anual"], "sharpe_faber_rf4": (media - 0.04) / sd,
            "sharpe_motor": m["sharpe"], "mdd": m["mdd"], "mar": m["cagr"] / abs(m["mdd"]) if m["mdd"] else None,
            "ulcer": ulcer, "invertido": m["tiempo_invertido"], "salidas_por_anio": salidas / anios_tramo,
            "rotacion_anual": m["rotacion_anual"], "n_operaciones": len(operaciones),
            "pct_operaciones_positivas": (sum(1 for o in operaciones if o > 0) / len(operaciones)) if operaciones else None,
            "mejor_anio": max(vals), "peor_anio": min(vals), "metricas": m}


def pct_anios_debajo(t: dict, b: dict) -> float:
    comunes = sorted(set(t["anuales"]) & set(b["anuales"]))
    return sum(1 for a in comunes if t["anuales"][a] < b["anuales"][a]) / len(comunes)


def reduccion_mdd(mt: dict, mb: dict) -> float | None:
    if mt["mdd"] is None or mb["mdd"] in (None, 0):
        return None
    return 1 - mt["mdd"] / mb["mdd"]


def tabla_metricas(res: dict, claves: list[str], segmento: str, titulo: str) -> list[dict]:
    P(f"\n--- {titulo} [{segmento}] ---")
    P(f"{'variante':<34}{'inicio':>11}{'fin':>11}{'n':>5}{'CAGR':>8}{'vol':>8}{'Sharpe':>8}{'Sortino':>8}"
      f"{'MDD':>9}{'Calmar':>8}{'invert':>8}{'rot/a':>7}{'costo/a':>9}{'camb':>6}{'PSR':>7}")
    filas = []
    for c in claves:
        x = res[c].metricas.get(segmento)
        if x is None or x["n_periodos"] < 3:
            P(f"{c:<34} (sin datos en el segmento)")
            continue
        P(f"{c[:34]:<34}{str(x['fecha_inicio']):>11}{str(x['fecha_fin']):>11}{x['n_periodos']:>5}"
          f"{pct(x['cagr']):>8}{pct(x['vol_anual']):>8}{num(x['sharpe']):>8}{num(x['sortino']):>8}"
          f"{pct(x['mdd']):>9}{num(x['calmar']):>8}{pct(x['tiempo_invertido'], 1):>8}"
          f"{num(x['rotacion_anual'], 2):>7}{pct(x['costo_anual'], 3):>9}{x['n_cambios_senal']:>6}"
          f"{num(x['psr'], 3):>7}")
        filas.append({"variante": c, "segmento": segmento, **{k: x[k] for k in (
            "fecha_inicio", "fecha_fin", "n_periodos", "cagr", "vol_anual", "sharpe", "sortino", "mdd", "calmar",
            "tiempo_invertido", "rotacion_anual", "costo_anual", "n_cambios_senal", "psr", "sharpe_periodo",
            "asimetria", "curtosis", "cagr_activo_sin_costos", "cagr_efectivo")}})
    return filas


def prueba_diferencia(ra: bt.ResultadoBacktest, rb: bt.ResultadoBacktest, desde: date, hasta: date) -> dict:
    ia0, ia1 = indices_tramo(ra, desde, hasta)
    ib0, ib1 = indices_tramo(rb, desde, hasta)
    if ra.fechas[ia0:ia1] != rb.fechas[ib0:ib1]:
        raise ValueError("fechas distintas en la prueba de diferencia")
    dif = [a - b for a, b in zip(ra.r_neto[ia0:ia1], rb.r_neto[ib0:ib1])]
    nw = newey_west(dif, 6)
    return {"n": nw["n"], "media_mensual": nw["media"], "se": nw["se"], "t_nw6": nw["t"],
            "ic95": nw["ic95"], "media_x12": 12 * nw["media"]}


def _sr_anual(x: list[float]) -> float:
    sd = statistics.stdev(x)
    return statistics.fmean(x) / sd * math.sqrt(12) if sd > 0 else 0.0


def _mdd(rends: list[float]) -> float:
    nivel, maximo, peor = 1.0, 1.0, 0.0
    for x in rends:
        nivel *= 1 + x
        maximo = max(maximo, nivel)
        peor = min(peor, nivel / maximo - 1)
    return peor


def bootstrap_pareado(ra: bt.ResultadoBacktest, rb: bt.ResultadoBacktest, desde: date, hasta: date,
                      bloque: int = 12, repeticiones: int = 2000, semilla: int = 20260925) -> dict:
    """ANALISIS POST-HOC (no pre-registrado): bootstrap de bloques moviles pareado (mismos bloques para
    ambas series) de los rendimientos netos mensuales. Da la distribucion de la diferencia de Sharpe
    anualizado (exceso sobre el efectivo) y de la reduccion relativa del MDD. No re-simula la senal:
    remuestrea los rendimientos realizados."""
    ia0, ia1 = indices_tramo(ra, desde, hasta)
    ib0, ib1 = indices_tramo(rb, desde, hasta)
    if ra.fechas[ia0:ia1] != rb.fechas[ib0:ib1]:
        raise ValueError("fechas distintas en el bootstrap")
    na, nb = ra.r_neto[ia0:ia1], rb.r_neto[ib0:ib1]
    ea = [x - e for x, e in zip(na, ra.r_efectivo[ia0:ia1])]
    eb = [x - e for x, e in zip(nb, rb.r_efectivo[ib0:ib1])]
    n = len(na)
    rng = random.Random(semilla)
    difs, reds = [], []
    for _ in range(repeticiones):
        sa, sb, xa, xb = [], [], [], []
        while len(sa) < n:
            i = rng.randrange(0, n - bloque + 1)
            sa.extend(ea[i:i + bloque])
            sb.extend(eb[i:i + bloque])
            xa.extend(na[i:i + bloque])
            xb.extend(nb[i:i + bloque])
        difs.append(_sr_anual(sa[:n]) - _sr_anual(sb[:n]))
        mb = _mdd(xb[:n])
        reds.append(1 - _mdd(xa[:n]) / mb if mb < 0 else float("nan"))
    difs.sort()
    reds = sorted(r for r in reds if not math.isnan(r))
    q = lambda v, p: v[min(len(v) - 1, max(0, int(p * len(v))))]  # noqa: E731
    return {"n": n, "bloque": bloque, "repeticiones": repeticiones, "semilla": semilla,
            "dif_sharpe_obs": _sr_anual(ea) - _sr_anual(eb), "dif_sharpe_ic95": (q(difs, 0.025), q(difs, 0.975)),
            "frac_dif_sharpe_le_0": sum(1 for x in difs if x <= 0) / len(difs),
            "red_mdd_obs": 1 - _mdd(na) / _mdd(nb), "red_mdd_ic95": (q(reds, 0.025), q(reds, 0.975)),
            "frac_red_mdd_lt_020": sum(1 for x in reds if x < 0.20) / len(reds)}


def analizar(d: dict, corr: Corredor, dir_replicas=None, con_dsr=True) -> dict:
    res = corr.res
    out: dict = {"tablas": {}, "tramos_articulo": {}, "criterios": {}, "sensibilidad": {}, "dsr": {}}
    principales = [f"sma{n}" for n in VENTANAS] + ["mom12", "comprar_y_mantener", "efectivo"]
    P("\n================ RESULTADOS PRINCIPALES (neto de costos GBM por defecto: 0.29% + 0.05% por lado) ================")
    for seg in ("completo", "dentro_muestra", "fuera_muestra"):
        out["tablas"][f"principal_{seg}"] = tabla_metricas(res, principales, seg, "Bloques A y B")
    P("\n--- comparar() del motor [fuera_muestra] ---")
    P(bt.comparar([res[c] for c in principales], "fuera_muestra"))

    # ---------------- tramo del articulo, sin costos
    P("\n================ TRAMO DEL ARTICULO (sin costos, como Faber) ================")
    for nombre_tramo, (desde, hasta) in (("1927-07_a_2005-12", TRAMO_2006), ("1927-07_a_2012-12", TRAMO_2013)):
        P(f"\n--- {nombre_tramo} ---")
        P(f"{'variante':<28}{'CAGR':>8}{'media a.':>9}{'sd anual':>9}{'vol mens':>9}{'Sh rf4%':>8}{'Sharpe':>8}"
          f"{'MDD':>9}{'MAR':>7}{'Ulcer':>8}{'invert':>8}{'sal/a':>7}{'%op+':>7}{'mejor':>8}{'peor':>9}")
        est = {}
        for c in [f"sma{n}|sin_costos" for n in VENTANAS] + ["mom12|sin_costos", "comprar_y_mantener|sin_costos"]:
            e = estilo_faber(res[c], desde, hasta)
            est[c] = e
            P(f"{c[:28]:<28}{pct(e['cagr']):>8}{pct(e['media_aritmetica_anual']):>9}{pct(e['sd_anual_calendario']):>9}"
              f"{pct(e['vol_mensual_anualizada']):>9}{num(e['sharpe_faber_rf4'], 2):>8}{num(e['sharpe_motor'], 3):>8}"
              f"{pct(e['mdd']):>9}{num(e['mar'], 2):>7}{pct(e['ulcer']):>8}{pct(e['invertido'], 1):>8}"
              f"{num(e['salidas_por_anio'], 2):>7}{pct(e['pct_operaciones_positivas'], 0):>7}"
              f"{pct(e['mejor_anio']):>8}{pct(e['peor_anio']):>9}")
        bh = est["comprar_y_mantener|sin_costos"]
        P(f"anios calendario completos: {bh['anios_completos']}")
        for c in [f"sma{n}|sin_costos" for n in VENTANAS] + ["mom12|sin_costos"]:
            e = est[c]
            P(f"{c:<22} reduccion MDD={num(reduccion_mdd(e, bh), 4)}  dif CAGR={100 * (e['cagr'] - bh['cagr']):+.3f} pp  "
              f"dif media arit={100 * (e['media_aritmetica_anual'] - bh['media_aritmetica_anual']):+.3f} pp  "
              f"% anios debajo de B&H={pct(pct_anios_debajo(e, bh), 1)}  operaciones={e['n_operaciones']}")
        out["tramos_articulo"][nombre_tramo] = {c: {k: v for k, v in e.items() if k not in ("anuales", "metricas")}
                                                | {"reduccion_mdd": reduccion_mdd(e, bh) if c != "comprar_y_mantener|sin_costos" else None,
                                                   "dif_cagr": e["cagr"] - bh["cagr"],
                                                   "pct_anios_debajo": pct_anios_debajo(e, bh)}
                                                for c, e in est.items()}
    P("\nCifras del articulo, 2006 (Tabla 2, 1900-2005): CAGR 9.75% vs 10.66%; sd 19.91% vs 15.38%; Sharpe 0.29 vs 0.43; "
      "MDD 83.66% vs 49.98% (texto: 42.24%); MAR 0.14 vs 0.23; Ulcer 20.33% vs 11.70%; invertido 69.77%; "
      "0.67 RT/anio; 63% op+; mejor 52.88% vs 52.40%; peor -43.86% vs -26.69%; media arit. 11.66% vs 11.72%; ~40% anios debajo")
    P("Cifras del articulo, 2013 (1901-2012): CAGR 9.32% vs 10.18%; media arit. 11.26% vs 11.22%; MDD 83.66% vs 42.24%; "
      "~70% invertido; <1 RT/anio; ~50% anios debajo")

    # ---------------- criterios pre-registrados
    P("\n================ CRITERIOS PRE-REGISTRADOS ================")
    t06 = out["tramos_articulo"]["1927-07_a_2005-12"]
    e_t, e_b = t06["sma10|sin_costos"], t06["comprar_y_mantener|sin_costos"]
    c1v, c2v, c3v, c4v = e_t["reduccion_mdd"], e_t["dif_cagr"], e_t["invertido"], e_t["salidas_por_anio"]
    c1 = 0.30 <= c1v <= 0.60
    c2 = 0.0 < c2v <= 0.0191
    c3 = 0.60 <= c3v <= 0.80
    c4 = 0.40 <= c4v <= 1.00
    din_t, din_b = res["sma10"].metricas["dentro_muestra"], res["comprar_y_mantener"].metricas["dentro_muestra"]
    red_din = reduccion_mdd(din_t, din_b)
    refuta_a = red_din < 0.20
    refuta_b = din_t["sharpe"] <= din_b["sharpe"]
    # adenda 2026-09-25: subperiodos
    decadas = []
    for desde, hasta in VENTANAS_DECADA_DENTRO + VENTANAS_DECADA_FUERA:
        mt, mb = metricas_tramo(res["sma10"], desde, hasta), metricas_tramo(res["comprar_y_mantener"], desde, hasta)
        decadas.append({"desde": desde, "hasta": hasta, "cagr_sma10": mt["cagr"], "cagr_bh": mb["cagr"],
                        "sharpe_sma10": mt["sharpe"], "sharpe_bh": mb["sharpe"], "mdd_sma10": mt["mdd"],
                        "mdd_bh": mb["mdd"], "reduccion_mdd": reduccion_mdd(mt, mb),
                        "invertido": mt["tiempo_invertido"], "dentro": hasta <= CORTE})
    n_dec_ok = sum(1 for x in decadas if x["dentro"] and x["reduccion_mdd"] is not None and x["reduccion_mdd"] > 0)
    n_dec = sum(1 for x in decadas if x["dentro"])
    solo_algunos = n_dec_ok < 5
    if refuta_a or refuta_b:
        estado = "No replicado"
    elif c1 and c2 and c3 and c4 and not solo_algunos:
        estado = "Replicado"
    else:
        estado = "Replicado con diferencias"
    fue_t, fue_b = res["sma10"].metricas["fuera_muestra"], res["comprar_y_mantener"].metricas["fuera_muestra"]
    red_fue = reduccion_mdd(fue_t, fue_b)
    if red_fue >= 0.20 and fue_t["sharpe"] >= fue_b["sharpe"]:
        veredicto_fuera = "Se sostiene"
    elif red_fue >= 0.20:
        veredicto_fuera = "Solo proteccion"
    else:
        veredicto_fuera = "No se sostiene"
    P(f"C1 reduccion relativa del MDD (1927-07..2005-12, sin costos) = {c1v:.4f} en [0.30, 0.60]? {c1}")
    P(f"C2 dif CAGR sma10 - B&H = {100 * c2v:+.3f} pp en (0, +1.91 pp]? {c2}")
    P(f"C3 tiempo invertido = {c3v:.4f} en [0.60, 0.80]? {c3}")
    P(f"C4 salidas por anio = {c4v:.4f} en [0.40, 1.00]? {c4}")
    P(f"Refutacion a) dentro_muestra neto: reduccion MDD = {red_din:.4f} < 0.20? {refuta_a}")
    P(f"Refutacion b) dentro_muestra neto: Sharpe sma10 {din_t['sharpe']:.4f} <= Sharpe B&H {din_b['sharpe']:.4f}? {refuta_b}")
    P(f"Subperiodos (adenda): reduccion MDD > 0 en {n_dec_ok} de {n_dec} ventanas dentro de muestra; "
      f"'solo en algunos subperiodos' (< 5)? {solo_algunos}")
    P(f"ESTADO segun reglas pre-registradas: {estado}")
    P(f"Fuera de muestra (2007-01..2026-07, neto): reduccion MDD = {red_fue:.4f}; Sharpe sma10 {fue_t['sharpe']:.4f} "
      f"vs B&H {fue_b['sharpe']:.4f} -> veredicto: {veredicto_fuera}")
    out["criterios"] = {"C1": [c1v, c1], "C2": [c2v, c2], "C3": [c3v, c3], "C4": [c4v, c4],
                        "refuta_a": [red_din, refuta_a], "refuta_b": [din_t["sharpe"], din_b["sharpe"], refuta_b],
                        "subperiodos_ok": [n_dec_ok, n_dec, solo_algunos], "estado": estado,
                        "fuera": {"reduccion_mdd": red_fue, "sharpe_sma10": fue_t["sharpe"],
                                  "sharpe_bh": fue_b["sharpe"], "veredicto": veredicto_fuera}}
    P("\n--- Subperiodos: sma10 vs comprar y mantener (neto, costos por defecto) ---")
    P(f"{'ventana':<25}{'CAGR sma10':>11}{'CAGR B&H':>10}{'Sh sma10':>9}{'Sh B&H':>8}{'MDD sma10':>10}{'MDD B&H':>9}"
      f"{'red MDD':>9}{'invert':>8}")
    for x in decadas:
        P(f"{str(x['desde'])[:7] + ' a ' + str(x['hasta'])[:7]:<25}{pct(x['cagr_sma10']):>11}{pct(x['cagr_bh']):>10}"
          f"{num(x['sharpe_sma10'], 2):>9}{num(x['sharpe_bh'], 2):>8}{pct(x['mdd_sma10']):>10}{pct(x['mdd_bh']):>9}"
          f"{num(x['reduccion_mdd'], 3):>9}{pct(x['invertido'], 0):>8}")
    out["subperiodos"] = decadas

    # ---------------- pruebas de diferencia (Newey-West 6)
    P("\n--- Diferencia mensual de rendimientos netos, media y error estandar Newey-West (6 rezagos) ---")
    out["diferencias"] = {}
    segs = {"dentro_muestra": (date(1927, 7, 31), CORTE), "fuera_muestra": (date(2007, 1, 31), date(2026, 7, 31)),
            "completo": (date(1927, 7, 31), date(2026, 7, 31))}
    for a, b in (("sma10", "comprar_y_mantener"), ("mom12", "comprar_y_mantener"), ("sma10", "mom12"),
                 ("sma10|sin_costos", "comprar_y_mantener|sin_costos")):
        for seg, (desde, hasta) in segs.items():
            pd = prueba_diferencia(res[a], res[b], desde, hasta)
            out["diferencias"][f"{a} - {b} [{seg}]"] = pd
            P(f"{a + ' - ' + b:<50} {seg:<15} n={pd['n']:<5} media={100 * pd['media_mensual']:+.4f}%/mes "
              f"(x12 {100 * pd['media_x12']:+.2f}%) t_NW6={pd['t_nw6']:+.2f} "
              f"IC95=[{100 * pd['ic95'][0]:+.4f}, {100 * pd['ic95'][1]:+.4f}]%/mes")

    # ---------------- analisis post-hoc (agregado despues de la corrida 1; ver Desviaciones en la ficha)
    P("\n--- POST-HOC (no pre-registrado): bootstrap pareado de bloques de 12 meses, 2000 repeticiones ---")
    out["post_hoc_bootstrap"] = {}
    for a, b in (("sma10", "comprar_y_mantener"), ("sma10", "mom12")):
        for seg in ("dentro_muestra", "fuera_muestra"):
            bs = bootstrap_pareado(res[a], res[b], *segs[seg])
            out["post_hoc_bootstrap"][f"{a} vs {b} [{seg}]"] = bs
            P(f"{a + ' vs ' + b:<30} {seg:<15} dif Sharpe obs={bs['dif_sharpe_obs']:+.3f} "
              f"IC95=[{bs['dif_sharpe_ic95'][0]:+.3f}, {bs['dif_sharpe_ic95'][1]:+.3f}] frac<=0={bs['frac_dif_sharpe_le_0']:.3f} | "
              f"red MDD obs={bs['red_mdd_obs']:+.3f} IC95=[{bs['red_mdd_ic95'][0]:+.3f}, {bs['red_mdd_ic95'][1]:+.3f}] "
              f"frac<0.20={bs['frac_red_mdd_lt_020']:.3f}")

    # ---------------- sensibilidad
    P("\n================ SENSIBILIDAD ================")
    costos_claves = []
    for nombre in [f"sma{n}" for n in VENTANAS] + ["mom12", "comprar_y_mantener"]:
        costos_claves.append(nombre)
        costos_claves += [f"{nombre}|{c}" for c in ("sin_costos", "spread_medio", "spread_iliquido", "doble_pierna")]
    for seg in ("dentro_muestra", "fuera_muestra"):
        out["tablas"][f"costos_{seg}"] = tabla_metricas(res, costos_claves, seg, "Bloque C (costos)")
    for seg in ("dentro_muestra", "fuera_muestra"):
        out["tablas"][f"rezago_{seg}"] = tabla_metricas(res, ["sma10", "sma10|rezago1m", "comprar_y_mantener"], seg,
                                                        "Bloque D (rezago de ejecucion)")
    claves_e = [c for c in res if corr.bloque[c] == "E"]
    for seg in ("completo", "dentro_muestra", "fuera_muestra"):
        out["tablas"][f"vintages_{seg}"] = tabla_metricas(res, claves_e, seg, "Bloque E (vintages de French)")
    P("\nVintages en el tramo del articulo 1927-07..2005-12 (sin costos):")
    out["sensibilidad"]["vintages_tramo2006"] = {}
    for v in ("202607", "202407", "200607"):
        ct = "sma10|sin_costos" if v == "202607" else f"sma10|vintage{v}|sin_costos"
        cb = "comprar_y_mantener|sin_costos" if v == "202607" else f"comprar_y_mantener|vintage{v}|sin_costos"
        et, eb = estilo_faber(res[ct], *TRAMO_2006), estilo_faber(res[cb], *TRAMO_2006)
        fila = {"cagr_t": et["cagr"], "cagr_bh": eb["cagr"], "mdd_t": et["mdd"], "mdd_bh": eb["mdd"],
                "reduccion_mdd": reduccion_mdd(et, eb), "dif_cagr": et["cagr"] - eb["cagr"],
                "invertido": et["invertido"], "salidas_por_anio": et["salidas_por_anio"],
                "sharpe_t": et["sharpe_motor"], "sharpe_bh": eb["sharpe_motor"]}
        out["sensibilidad"]["vintages_tramo2006"][v] = fila
        P(f"  CRSP {v}: CAGR {pct(fila['cagr_t'])} vs {pct(fila['cagr_bh'])} (dif {100 * fila['dif_cagr']:+.3f} pp); "
          f"MDD {pct(fila['mdd_t'])} vs {pct(fila['mdd_bh'])} (reduccion {fila['reduccion_mdd']:.4f}); "
          f"invertido {pct(fila['invertido'], 1)}; salidas/anio {fila['salidas_por_anio']:.3f}; "
          f"Sharpe {fila['sharpe_t']:.3f} vs {fila['sharpe_bh']:.3f}")
    # coincidencia de senales entre vintages (meses comunes)
    s26 = dict(zip(res["sma10|sin_costos"].fechas, res["sma10|sin_costos"].exposicion))
    for v in ("202407", "200607"):
        sv = dict(zip(res[f"sma10|vintage{v}|sin_costos"].fechas, res[f"sma10|vintage{v}|sin_costos"].exposicion))
        comunes = sorted(set(s26) & set(sv))
        distintos = [f for f in comunes if s26[f] != sv[f]]
        out["sensibilidad"][f"senales_distintas_202607_vs_{v}"] = {"meses_comunes": len(comunes),
                                                                   "meses_distintos": len(distintos),
                                                                   "fechas": [str(f) for f in distintos]}
        P(f"  Senal sma10 CRSP 202607 vs {v}: {len(distintos)} de {len(comunes)} meses con exposicion distinta: "
          f"{[str(f) for f in distintos[:12]]}{' ...' if len(distintos) > 12 else ''}")
    claves_f = ["sma10|muestra1928", "sma10_precio_gspc|muestra1928", "comprar_y_mantener|muestra1928"]
    for seg in ("completo", "dentro_muestra", "fuera_muestra"):
        out["tablas"][f"senal_precio_{seg}"] = tabla_metricas(res, claves_f, seg, "Bloque F (senal sobre ^GSPC precio)")
    a, b = res["sma10|muestra1928"], res["sma10_precio_gspc|muestra1928"]
    dif_f = sum(1 for x, y in zip(a.exposicion, b.exposicion) if x != y)
    out["sensibilidad"]["senal_precio_meses_distintos"] = [dif_f, len(a.exposicion)]
    P(f"  Meses con exposicion distinta (TR vs precio): {dif_f} de {len(a.exposicion)}")
    claves_g = [c for c in res if corr.bloque[c] == "G"]
    for seg in ("completo", "dentro_muestra", "fuera_muestra"):
        out["tablas"][f"mxn_{seg}"] = tabla_metricas(res, claves_g, seg, "Bloque G (MXN)")
    # misma ventana en USD para comparar con MXN
    g0 = res["sma10|mxn|rf_usd"].fechas[0]
    P(f"\n  Mismo periodo que MXN en USD ({g0} a {res['sma10'].fechas[-1]}), neto:")
    usd_mismo = {}
    for c in ("sma10", "comprar_y_mantener"):
        m = metricas_tramo(res[c], g0, date(2026, 7, 31))
        usd_mismo[c] = {k: m[k] for k in ("cagr", "vol_anual", "sharpe", "mdd", "tiempo_invertido")}
        P(f"  {c:<20} CAGR {pct(m['cagr'])} vol {pct(m['vol_anual'])} Sharpe {num(m['sharpe'])} MDD {pct(m['mdd'])}")
    out["sensibilidad"]["usd_mismo_periodo_mxn"] = usd_mismo

    # ---------------- DSR
    if con_dsr:
        P("\n================ SHARPE DEFLACTADO ================")
        for etiqueta, kw in (("sma10 dentro_muestra N=registradas", {"segmento": "dentro_muestra", "variante": "sma10"}),
                             ("mejor variante dentro_muestra N=registradas", {"segmento": "dentro_muestra"}),
                             ("sma10 dentro_muestra N=20", {"segmento": "dentro_muestra", "variante": "sma10", "n_pruebas": 20}),
                             ("sma10 fuera_muestra N=registradas", {"segmento": "fuera_muestra", "variante": "sma10"}),
                             ("sma10 completo N=registradas", {"segmento": "completo", "variante": "sma10"})):
            x = bt.sharpe_deflactado_de_registro(ID, dir_replicas=dir_replicas, **kw)
            out["dsr"][etiqueta] = x
            P(f"{etiqueta:<46} variante={x['variante']:<6} DSR={x['dsr']:.4f} cumple(>= {x['umbral']})={x['cumple']} "
              f"N={x['n_pruebas']} (registradas {x['n_registradas']}) V={x['varianza_sharpes_periodo']:.3e} "
              f"SR={x['sr_periodo']:.4f}/mes ({x['sr_anual']:.3f} anual) SR0={x['sr0_periodo']:.4f}/mes "
              f"({x['sr0_anual']:.3f} anual) T={x['n_obs']} asim={x['asimetria']:.3f} curt={x['curtosis']:.3f} "
              f"PSR={x['psr_sin_deflactar']:.4f}")
    return out


# ============================================================== principal

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prueba-sintetica", action="store_true",
                    help="datos sinteticos, registro en un directorio temporal (prueba del codigo)")
    args = ap.parse_args()
    inicio = datetime.now(timezone.utc)
    sha_pre = verificar_pre_registro()
    if args.prueba_sintetica:
        dir_tmp = tempfile.mkdtemp(prefix="R01-prueba-")
        d = datos_sinteticos()
        corr = Corredor(registrar=True, dir_replicas=dir_tmp)
        P(f"PRUEBA SINTETICA: registro en {dir_tmp} (no es un resultado)")
    else:
        d = datos_reales()
        corr = Corredor(registrar=True)
    P(f"R01 - Faber (2007) SMA de 10 meses. Corrida {inicio.strftime('%Y-%m-%dT%H:%M:%SZ')}. "
      f"Pre-registro sha256 {sha_pre[:16]} verificado.")
    for v, f in d["french"].items():
        P(f"French CRSP {v}: {f['rango'][0]} a {f['rango'][1]} ({f['n']} meses), sha256 {f['sha256']}, {f['ruta']}")
    g = d["gspc"]
    P(f"Yahoo ^GSPC diario: {g['rango_diario']} n={g['n_diario']}; fin de mes {g['serie'][0][0]} a {g['serie'][-1][0]} "
      f"({len(g['serie'])} meses); usa_adjclose={g['usa_adjclose']} adjclose!=close={g['adjclose_difiere_de_close']}; "
      f"sin precio={g['fechas_sin_precio']}; huella {g['huella']}")
    x = d["mxn"]
    P(f"FRED DEXMXUS {x['fx_rango']} n={x['fx_n']} huella {x['fx_huella']}; INTGSTMXM193N (fin de mes, /1200) "
      f"{x['cetes_rango']} n={x['cetes_n']} huella {x['cetes_huella']}")
    correr_todo(d, corr)
    P(f"\nCorridas registradas en esta ejecucion: {len(corr.res)} "
      f"(es_prueba=1: {sum(1 for c in corr.res if corr.bloque[c] == 'A')})")
    huellas = sorted({(corr.bloque[c], r.meta['huella_datos']) for c, r in corr.res.items()})
    P(f"huella_datos por bloque: {huellas}")
    out = analizar(d, corr, dir_replicas=corr.dir_replicas)
    out["meta"] = {"corrida_utc": inicio.strftime("%Y-%m-%dT%H:%M:%SZ"), "sha_pre_registro": sha_pre,
                   "sintetica": args.prueba_sintetica, "n_corridas": len(corr.res),
                   "huellas_datos": {c: r.meta["huella_datos"] for c, r in corr.res.items()},
                   "french": {v: {k: f[k] for k in ("sha256", "ruta", "rango", "n")} for v, f in d["french"].items()},
                   "gspc": {k: g[k] for k in ("rango_diario", "n_diario", "fechas_sin_precio", "huella", "url")},
                   "mxn": {k: x[k] for k in ("fx_rango", "fx_n", "cetes_rango", "cetes_n", "fx_huella", "cetes_huella")},
                   "costos": COSTOS, "registro": str(bt.ruta_registro(ID, corr.dir_replicas))}
    destino = (Path(corr.dir_replicas) if args.prueba_sintetica else AQUI)
    (destino / "R01-resultados.json").write_text(json.dumps(out, indent=1, default=str, ensure_ascii=False),
                                                 encoding="utf-8")
    (destino / "R01-salida.txt").write_text("\n".join(P.lineas) + "\n", encoding="utf-8")
    print(f"\nEscrito: {destino / 'R01-resultados.json'} y {destino / 'R01-salida.txt'}")


if __name__ == "__main__":
    main()
