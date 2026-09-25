"""R08 - El peso y las acciones de EUA para un inversionista que mide en pesos (cobertura natural).

Reproduce (desde la raiz del repo):   python3 laboratorio/replicas/R08.py
Prueba del codigo con datos sinteticos (sin red, sin tocar el registro real):
                                      python3 laboratorio/replicas/R08.py --prueba-sintetica

Hallazgo: conocimiento/16-macro-global-divisas-y-el-peso.md §5.4, §6.2 regla 4 y §6.4.
Referencia (mecanismo): Campbell, Serfaty-de Medeiros y Viceira (2010), "Global Currency Hedging",
Journal of Finance 65(1): 87-121 (NBER WP 13088, mayo de 2007).
Ficha y pre-registro: R08-peso-y-acciones-para-un-mexicano.md (secciones 1-9, huella verificada abajo).

Datos: French F-F_Research_Data_Factors (mensual y diario), FRED DEXMXUS / INTGSTMXM193N /
IR3TIB01MXM156N / IR3TIB01USM156N, Banxico SIE (FIX SF43718, CETES 28 SF43936), Yahoo ^SP500TR,
^GSPC e IVVPESO.MX. En la primera corrida se descargan y se congelan en R08-datos/ con
SHA256SUMS.txt; despues se leen de ahi y se verifican las huellas.
Motor: herramientas/backtest.py (id_replica="R08"). Cada corrida se agrega a R08-variantes.csv.
Salidas: R08-variantes.csv, R08-resultados.json y R08-salida.txt (copia de lo impreso).
Solo biblioteca estandar.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from bisect import bisect_right
from calendar import monthrange
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(RAIZ))

from herramientas import backtest as bt  # noqa: E402
from herramientas import datos as dt  # noqa: E402
from herramientas import datos_historicos as dh  # noqa: E402
from herramientas import huellas  # noqa: E402
from herramientas import metricas as mt  # noqa: E402
from herramientas.estadistica import newey_west  # noqa: E402

ID = "R08"
FICHA = AQUI / "R08-peso-y-acciones-para-un-mexicano.md"
# sha256 de las secciones 1-9 (de "## PRE-REGISTRO" a "## RESULTADOS"), calculado el 2026-09-25 06:42 UTC
SHA_PRE_REGISTRO = "b3364065cc61a703daface2964d14bd49769f437a06ab0b549844975faca47e5"
DIR_DATOS = AQUI / "R08-datos"

CORTE = date(2007, 5, 31)            # NBER WP 13088, mayo de 2007
BASE = date(1993, 12, 31)            # rendimientos desde 1994-01
BASE_FIX = date(1991, 11, 30)        # extension con FIX (S2)
BASE_IB = date(1997, 1, 31)          # tasas interbancarias (S4)
BASE_IVV = date(2014, 11, 30)        # IVVPESO (S9)
FIN = date(2026, 7, 31)              # ultimo mes de French CRSP 202607
SEMILLA = 20260925
BLOQUE = 12
REPS = 5000
MIN_MESES_MINVAR = 36
MAX_DIAS = 10

C_GBM = bt.COMISION_GBM_POR_LADO                 # 0.0029 (hecho)
S_LIQ = bt.SPREAD_POR_LADO["liquido"]             # 0.0005 (supuesto)
S_MED = bt.SPREAD_POR_LADO["medio"]               # 0.0015 (supuesto)
H_FIJAS = {"mxn_h000": 0.0, "mxn_h025": 0.25, "mxn_h050": 0.5, "mxn_h075": 0.75, "mxn_h100": 1.0}

VENTANAS_CAL = {  # descriptivas (fin de mes de la primera y ultima observacion)
    "1996-2026": (date(1996, 1, 31), FIN),
    "2008-2026": (date(2008, 1, 31), FIN),
    "2016-2026": (date(2016, 1, 31), FIN),
    "2023-2026": (date(2023, 1, 31), FIN),
}
VENTANAS_CRISIS = {
    "crisis_financiera": (date(2007, 7, 1), date(2009, 12, 31)),
    "anio_2008": (date(2007, 12, 31), date(2008, 12, 31)),
    "2020": (date(2020, 1, 1), date(2020, 12, 31)),
    "2022": (date(2022, 1, 1), date(2022, 12, 31)),
}
EPISODIOS = {"Lehman": (date(2008, 9, 12), date(2009, 3, 9)), "COVID": (date(2020, 2, 19), date(2020, 3, 23))}

# Cifras del capitulo 16 §5.4 (indice de precio ^GSPC x DEXMXUS). Tolerancias pre-registradas.
CAPITULO = {
    "A1_corr": {"1996-2026": -0.50, "2008-2026": -0.56, "2016-2026": -0.42, "2023-2026": -0.44},
    "A2_vol": {"1996-2026": (0.153, 0.136), "2008-2026": (0.156, 0.134), "2016-2026": (0.150, 0.149),
               "2023-2026": (0.123, 0.116)},
    "A3": {"n": 40, "r_usd": -0.078, "x": 0.037, "r_mxn": -0.045},
    "A4": {"crisis_financiera": (-0.568, -0.398), "2020": (-0.339, -0.150), "2022": (-0.254, -0.274)},
    "A5": {"Lehman": (-0.466, -0.182), "COVID": (-0.339, -0.107)},
    "A6": {"1996-2026": (0.0817, 0.1106, 0.0267), "2016-2026": (0.1348, 0.1141, -0.0182)},
}
TOL = {"A1": 0.05, "A2": 0.005, "A3": 0.01, "A4": 0.01, "A6": 0.003}

URL_FRED = dt.URL_FRED + "?id="
BANXICO = "https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarSeries"
SERIES_BANXICO = {"banxico_SF43718_fix.csv": ("CF102", "6", "SF43718"),
                  "banxico_SF43936_cetes28.csv": ("CF107", "22", "SF43936")}
SERIES_FRED = ["DEXMXUS", "INTGSTMXM193N", "IR3TIB01MXM156N", "IR3TIB01USM156N"]
TICKERS = {"sp500tr": "^SP500TR", "gspc": "^GSPC", "ivvpeso": "IVVPESO.MX"}

# Destino del registro (se cambia a un directorio temporal en --prueba-sintetica)
DIR_REG: Path | None = None
SALIDA: list[str] = []


def P(*args) -> None:
    texto = " ".join(str(a) for a in args)
    print(texto)
    SALIDA.append(texto)


# ============================================================== utilidades

def verificar_pre_registro() -> str:
    t = FICHA.read_text(encoding="utf-8")
    i, j = t.index("## PRE-REGISTRO"), t.index("## RESULTADOS")
    h = hashlib.sha256(t[i:j].encode("utf-8")).hexdigest()
    if h != SHA_PRE_REGISTRO:
        raise SystemExit(f"El pre-registro (secciones 1-9) cambio: sha256 {h} != {SHA_PRE_REGISTRO}. "
                         "Los cambios van en 'Desviaciones del pre-registro', no en las secciones 1-9.")
    return h


def fin_de_mes(f: date) -> date:
    return date(f.year, f.month, monthrange(f.year, f.month)[1])


def mes_anterior(f: date) -> date:
    return fin_de_mes(date(f.year, f.month, 1) - timedelta(days=1))


def valor_en_o_antes(serie: list[tuple], f: date, max_dias: int | None = MAX_DIAS):
    """Ultimo (fecha, valor) con fecha <= f y antiguedad <= max_dias; None si no hay."""
    fechas = [a for a, _ in serie] if not hasattr(serie, "_fechas") else serie._fechas
    k = bisect_right(fechas, f) - 1
    if k < 0:
        return None
    if max_dias is not None and (f - serie[k][0]).days > max_dias:
        return None
    return serie[k]


class Serie(list):
    """Lista de (fecha, valor) ordenada con indice de fechas precalculado."""

    def __init__(self, datos):
        super().__init__(sorted(datos))
        self._fechas = [a for a, _ in self]


def huella_serie(serie) -> str:
    return hashlib.sha256(repr(list(serie)).encode()).hexdigest()[:16]


def corr(a: list[float], b: list[float]) -> float:
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    sab = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    saa = sum((x - ma) ** 2 for x in a)
    sbb = sum((y - mb) ** 2 for y in b)
    return sab / math.sqrt(saa * sbb)


def _indices_bloques(n: int, bloque: int, rng: random.Random) -> list[int]:
    idx: list[int] = []
    bloque = min(bloque, n)
    while len(idx) < n:
        i = rng.randrange(0, n - bloque + 1)
        idx.extend(range(i, i + bloque))
    return idx[:n]


def _cuantiles(vals: list[float]) -> tuple[float, float]:
    vals = sorted(vals)
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]


def ic_boot_corr(a, b) -> tuple[float, float]:
    rng = random.Random(SEMILLA)
    vals = []
    for _ in range(REPS):
        idx = _indices_bloques(len(a), BLOQUE, rng)
        vals.append(corr([a[i] for i in idx], [b[i] for i in idx]))
    return _cuantiles(vals)


def vol_anual(x: list[float], ppa: int = 12) -> float:
    return statistics.stdev(x) * math.sqrt(ppa)


def ic_boot_dif_vol(a, b) -> tuple[float, float]:
    """IC 95% de vol(a) - vol(b), anualizada, con bloques pareados (mismos indices)."""
    rng = random.Random(SEMILLA)
    vals = []
    for _ in range(REPS):
        idx = _indices_bloques(len(a), BLOQUE, rng)
        vals.append(vol_anual([a[i] for i in idx]) - vol_anual([b[i] for i in idx]))
    return _cuantiles(vals)


def beta_nw(y: list[float], x: list[float], rezagos: int = 6) -> dict:
    """MCO y = a + b x con error estandar Newey-West(rezagos) de b."""
    n = len(x)
    mx, my = statistics.fmean(x), statistics.fmean(y)
    z = [v - mx for v in x]
    sxx = sum(v * v for v in z)
    b = sum(zi * (yi - my) for zi, yi in zip(z, y)) / sxx
    a = my - b * mx
    e = [yi - a - b * xi for xi, yi in zip(x, y)]
    g = [zi * ei for zi, ei in zip(z, e)]
    s = sum(v * v for v in g)
    for j in range(1, rezagos + 1):
        s += 2 * (1 - j / (rezagos + 1)) * sum(g[t] * g[t - j] for t in range(j, n))
    se = math.sqrt(s) / sxx
    se_iid = math.sqrt(sum(v * v for v in e) / (n - 2) / sxx)
    return {"n": n, "a": a, "b": b, "se_nw": se, "t_nw": b / se, "t_iid": b / se_iid}


def curva_de(fechas: list[date], rends: list[float], f0: date) -> list[tuple]:
    c = [(f0, 1.0)]
    for f, r in zip(fechas, rends):
        c.append((f, c[-1][1] * (1 + r)))
    return c


def cagr_de(rends: list[float], f0: date, f1: date) -> float:
    anios = (f1 - f0).days / 365.25
    return math.prod(1 + r for r in rends) ** (1 / anios) - 1


def mdd_de(curva: list[tuple]) -> dict:
    x = mt.max_drawdown(curva)
    return {"mdd": x["valor"], "pico": x["fecha_pico"], "valle": x["fecha_valle"],
            "recuperacion": x.get("fecha_recuperacion")}


def fmt(x, d: int = 4) -> str:
    if x is None:
        return "NA"
    if isinstance(x, bool):
        return "sí" if x else "no"
    if isinstance(x, float):
        if math.isnan(x):
            return "nan"
        return f"{x:.{d}f}"
    return str(x)


def pct(x, d: int = 2) -> str:
    return "NA" if x is None else f"{100 * x:.{d}f}%"


def tabla(encabezados: list[str], filas: list[list]) -> str:
    lineas = ["| " + " | ".join(encabezados) + " |", "|" + "---|" * len(encabezados)]
    for f in filas:
        lineas.append("| " + " | ".join(str(c) for c in f) + " |")
    return "\n".join(lineas)


# ============================================================== descarga y congelado

def _post_banxico(cuadro: str, sector: str, serie: str) -> bytes:
    campos = [("idCuadro", cuadro), ("sector", sector), ("version", "3"), ("locale", "es"),
              ("series", serie), ("anoInicial", "1990"), ("anoFinal", "2026"),
              ("tipoInformacion", "4,1"), ("metadatosWeb", "true"), ("formatoHorizontal", "false"),
              ("formatoCSV.x", "10"), ("formatoCSV.y", "10")]
    ultimo = None
    for intento in range(4):
        try:
            req = urllib.request.Request(BANXICO, data=urllib.parse.urlencode(campos).encode())
            with urllib.request.urlopen(req, timeout=120) as r:
                contenido = r.read()
            if b"Fecha" not in contenido:
                raise dh.ErrorDatos(f"Banxico {serie}: respuesta sin tabla ({contenido[:120]!r})")
            return contenido
        except Exception as e:  # noqa: BLE001 - se reintenta y al final se reporta
            ultimo = e
            time.sleep(2 * (intento + 1))
    raise dh.ErrorDatos(f"Banxico {serie}: {ultimo!r}")


def parsear_banxico(texto: str) -> list[tuple[date, float]]:
    filas, en_datos = [], False
    for linea in texto.splitlines():
        s = linea.strip()
        if not en_datos:
            en_datos = s.startswith('"Fecha"')
            continue
        partes = [p.strip().strip('"') for p in s.split(",")]
        if len(partes) < 2:
            continue
        try:
            f = datetime.strptime(partes[0], "%d/%m/%Y").date()
            filas.append((f, float(partes[1])))
        except ValueError:
            continue  # N/E u otras marcas
    return sorted(filas)


def cargar_datos() -> dict:
    DIR_DATOS.mkdir(parents=True, exist_ok=True)
    manifiesto = DIR_DATOS / "SHA256SUMS.txt"
    bitacora_ruta = DIR_DATOS / "bitacora_descarga.json"
    bitacora = json.loads(bitacora_ruta.read_text()) if bitacora_ruta.exists() else {}
    ahora = datetime.now(timezone.utc).isoformat(timespec="seconds")

    def congelar(nombre: str, obtener, url: str) -> bytes:
        ruta = DIR_DATOS / nombre
        if ruta.exists():
            return ruta.read_bytes()
        if manifiesto.exists():
            raise SystemExit(f"Falta {ruta} y ya existe {manifiesto}: los datos congelados estan incompletos")
        contenido = obtener()
        ruta.write_bytes(contenido)
        bitacora[nombre] = {"url": url, "descargado_utc": ahora}
        return contenido

    salida: dict = {}
    # French (dh.french congela el zip en R08-datos/french; cache_horas=None no caduca)
    for clave, archivo, frec in (("fr_m", "F-F_Research_Data_Factors", "mensual"),
                                 ("fr_d", "F-F_Research_Data_Factors_daily", "diaria")):
        ya = (DIR_DATOS / "french" / dh.nombre_zip_french(archivo)).exists()
        if not ya and manifiesto.exists():
            raise SystemExit(f"Falta el zip de French {archivo} en R08-datos/french")
        t = dh.french(archivo, frec, dir_cache=DIR_DATOS / "french")
        if not ya:
            bitacora[f"french/{dh.nombre_zip_french(archivo)}"] = {"url": t["url"], "descargado_utc": ahora}
        mercado = dict(dh.rendimiento_mercado_french(t))
        rf = dict(dh.columna(t, "RF"))
        salida[clave] = {"fechas": sorted(mercado), "R": mercado, "RF": rf, "version_crsp": t["version_crsp"],
                         "sha256": t["sha256"], "rango": (t["fechas"][0], t["fechas"][-1])}
    # FRED
    for s in SERIES_FRED:
        url = URL_FRED + s
        texto = congelar(f"fred_{s}.csv", lambda url=url: dt.descargar(url).encode("utf-8"), url).decode("utf-8")
        salida[s] = Serie(dt.parsear_fred_csv(texto))
    # Banxico
    for nombre, (cuadro, sector, serie) in SERIES_BANXICO.items():
        crudo = congelar(nombre, lambda c=cuadro, se=sector, s=serie: _post_banxico(c, se, s),
                         f"{BANXICO} (POST idCuadro={cuadro}, series={serie})")
        salida[serie] = Serie(parsear_banxico(crudo.decode("latin-1")))
    # Yahoo
    for clave, ticker in TICKERS.items():
        params = {"period1": dh.YAHOO_PERIODO_1, "period2": dh.YAHOO_PERIODO_2, "interval": "1d",
                  "events": "div,split"}
        url = dt.URL_YAHOO + urllib.parse.quote(ticker, safe="") + "?" + urllib.parse.urlencode(params)
        nombre = "yahoo_" + ticker.replace("^", "").replace("=", "_") + "_1d.json"
        texto = congelar(nombre, lambda url=url: dt.descargar(url, dt.UA_NAVEGADOR).encode("utf-8"), url)
        h = dh.parsear_yahoo_historia(texto.decode("utf-8"), "1d", solo_periodos_completos=True)
        salida[clave] = Serie(zip(h["fechas"], h["precios"]))
        salida[clave + "_meta"] = {"ticker": ticker, "moneda": h["moneda"], "usa_adjclose": h["usa_adjclose"],
                                   "adjclose_difiere_de_close": h["adjclose_difiere_de_close"],
                                   "fechas_sin_precio": [str(f) for f in h["fechas_sin_precio"]],
                                   "rango": (h["fechas"][0], h["fechas"][-1]), "n": len(h["fechas"])}
    bitacora_ruta.write_text(json.dumps(bitacora, indent=1, ensure_ascii=False, default=str))
    archivos = sorted(str(p) for p in DIR_DATOS.rglob("*")
                      if p.is_file() and p.name not in ("SHA256SUMS.txt", "bitacora_descarga.json"))
    if not manifiesto.exists():
        huellas.crear(str(DIR_DATOS), archivos)
        salida["huellas_estado"] = "creadas en esta corrida"
    else:
        fallas = huellas.verificar(str(manifiesto))
        if fallas:
            raise SystemExit(f"Huellas que no coinciden en R08-datos: {fallas}")
        salida["huellas_estado"] = "verificadas contra SHA256SUMS.txt"
    salida["manifiesto"] = manifiesto.read_text()
    return salida


def datos_sinteticos() -> dict:
    """Mismas estructuras que cargar_datos, con numeros aleatorios (solo para probar el codigo)."""
    rng = random.Random(1)
    meses = []
    f = date(1985, 1, 31)
    while f <= FIN:
        meses.append(f)
        f = fin_de_mes(f + timedelta(days=1))
    dias = []
    d = date(1985, 1, 2)
    while d <= date(2026, 9, 24):
        if d.weekday() < 5:
            dias.append(d)
        d += timedelta(days=1)
    choque_m = {m: rng.gauss(0, 1) for m in meses}
    R_m = {m: 0.008 + 0.04 * choque_m[m] for m in meses}
    fr_m = {"fechas": meses, "R": R_m, "RF": {m: 0.003 for m in meses}, "version_crsp": "sintetico",
            "sha256": "sintetico", "rango": (meses[0], meses[-1])}
    choque_d = {x: rng.gauss(0, 1) for x in dias}
    dias_fr = [x for x in dias if x <= FIN]
    fr_d = {"fechas": dias_fr, "R": {x: 0.0004 + 0.01 * choque_d[x] for x in dias_fr},
            "RF": {x: 0.0001 for x in dias_fr}, "version_crsp": "sintetico", "sha256": "sintetico",
            "rango": (dias_fr[0], dias_fr[-1])}
    fx, v = [], 3.1
    for x in dias:
        v *= math.exp(0.0001 - 0.004 * choque_d[x] + 0.004 * rng.gauss(0, 1))
        fx.append((x, v))
    salida = {"fr_m": fr_m, "fr_d": fr_d,
              "DEXMXUS": Serie((a, b) for a, b in fx if a >= date(1993, 11, 8) and a <= date(2026, 9, 18)),
              "SF43718": Serie((a, b) for a, b in fx if a >= date(1991, 11, 12)),
              "SF43936": Serie((x, 7.0 + math.sin(i / 50)) for i, x in enumerate(dias) if x.weekday() == 3),
              "INTGSTMXM193N": Serie((date(m.year, m.month, 1), 7.0) for m in meses),
              "IR3TIB01MXM156N": Serie((date(m.year, m.month, 1), 7.5) for m in meses if m.year >= 1997),
              "IR3TIB01USM156N": Serie((date(m.year, m.month, 1), 3.0) for m in meses)}
    for clave, inicio, deriva in (("sp500tr", date(1988, 1, 4), 0.0004), ("gspc", date(1985, 1, 2), 0.0003),
                                  ("ivvpeso", date(2014, 11, 5), 0.0005)):
        p, serie = 100.0, []
        for x in dias:
            if x >= inicio:
                p *= 1 + deriva + 0.01 * choque_d[x]
                serie.append((x, p))
        salida[clave] = Serie(serie)
        salida[clave + "_meta"] = {"ticker": clave, "moneda": "sintetico", "usa_adjclose": True,
                                   "adjclose_difiere_de_close": False, "fechas_sin_precio": [],
                                   "rango": (serie[0][0], serie[-1][0]), "n": len(serie)}
    salida["huellas_estado"] = "sintetico"
    salida["manifiesto"] = "sintetico"
    return salida


# ============================================================== construccion de series

def meses_entre(fr_m: dict, base: date, fin: date) -> list[date]:
    return [m for m in fr_m["fechas"] if base <= m <= fin]


def tasa_cetes_mensual(cetes: Serie, mes: date) -> float:
    """CETES 28 del mes: ultima subasta <= fin del mes anterior; tasa/100 x dias del mes / 360."""
    previo = mes_anterior(mes)
    v = valor_en_o_antes(cetes, previo, max_dias=31)
    if v is None:
        raise dh.ErrorDatos(f"Sin subasta de CETES en los 31 dias previos a {previo}")
    return v[1] / 100 * mes.day / 360


def tasa_fred_mes_anterior(serie: Serie, mes: date, max_dias: int = 0) -> float:
    """Valor FRED (fecha = dia 1) del mes t-1, /1200. max_dias > 0 permite usar el ultimo valor
    conocido si el del mes t-1 falta (desviacion del 2026-09-25: IR3TIB01USM156N no tiene 2020-04)."""
    previo = mes_anterior(mes)
    v = valor_en_o_antes(serie, date(previo.year, previo.month, 1), max_dias=max_dias)
    if v is None:
        raise dh.ErrorDatos(f"Sin dato FRED para {previo:%Y-%m}")
    return v[1] / 1200


def panel_mensual(meses: list[date], R: dict, RF: dict, fx: Serie, i_mx, i_us=None, nombre_fx="") -> dict:
    """Series alineadas a 'meses' (indice 0 = base, no se evalua; su valor queda en 0.0).

    i_mx(mes) -> rendimiento mensual en MXN del efectivo (y de la pata MXN de la cobertura).
    i_us(mes) -> tasa USD de la cobertura; None = RF de French.
    """
    S = []
    for m in meses:
        v = valor_en_o_antes(fx, m)
        if v is None:
            raise dh.ErrorDatos(f"{nombre_fx}: sin tipo de cambio en los {MAX_DIAS} dias previos a {m}")
        S.append(v[1])
    p = {"meses": meses, "S": S, "R": [0.0], "RF": [0.0], "x": [0.0], "cet": [0.0], "ius": [0.0], "f": [0.0],
         "U": [0.0], "H": [0.0]}
    for k in range(1, len(meses)):
        m = meses[k]
        r, rf = R[m], RF[m]
        x = S[k] / S[k - 1] - 1
        cet = i_mx(m)
        ius = rf if i_us is None else i_us(m)
        f = (1 + cet) / (1 + ius) - 1
        for clave, val in (("R", r), ("RF", rf), ("x", x), ("cet", cet), ("ius", ius), ("f", f),
                           ("U", (1 + r) * (1 + x) - 1), ("H", x - f)):
            p[clave].append(val)
    return p


def rend_cubierto(p: dict, h, c: float = 0.0) -> list[float]:
    """R^h = U - h H - h c/12. h puede ser un numero o una lista por periodo (indice 0 = base)."""
    salida = [0.0]
    for k in range(1, len(p["meses"])):
        hk = h[k] if isinstance(h, list) else h
        salida.append(p["U"][k] - hk * p["H"][k] - hk * c / 12)
    return salida


def constructor_minvar(datos: list[tuple], recortar: bool = True) -> list[float]:
    """datos = [(U_k, H_k)] desde el primer mes evaluado. Salida k = h para el mes k+1, estimada con
    datos[0..k] (ventana expansiva). Menos de MIN_MESES_MINVAR observaciones -> 0.0."""
    salida = []
    su = sh = suh = shh = 0.0
    n = 0
    for u, hh in datos:
        n += 1
        su += u
        sh += hh
        suh += u * hh
        shh += hh * hh
        if n < MIN_MESES_MINVAR:
            salida.append(0.0)
            continue
        cov = (suh - su * sh / n) / (n - 1)
        var = (shh - sh * sh / n) / (n - 1)
        h = cov / var if var > 0 else 0.0
        salida.append(min(1.0, max(0.0, h)) if recortar else h)
    return salida


def h_minvar(U: list[float], H: list[float]) -> float:
    mu, mh = statistics.fmean(U), statistics.fmean(H)
    cov = sum((a - mu) * (b - mh) for a, b in zip(U, H)) / (len(U) - 1)
    return cov / statistics.variance(H)


def serie(meses: list[date], valores: list[float]) -> list[tuple]:
    return list(zip(meses, valores))


def precio_fin_de_mes(precios: Serie, meses: list[date]) -> tuple[list[float], list[int]]:
    salida, edades = [], []
    for m in meses:
        v = valor_en_o_antes(precios, m)
        if v is None:
            raise dh.ErrorDatos(f"Sin precio en los {MAX_DIAS} dias previos a {m}")
        salida.append(v[1])
        edades.append((m - v[0]).days)
    return salida, edades


def rends_de_precios(precios: list[float]) -> list[float]:
    return [0.0] + [precios[k] / precios[k - 1] - 1 for k in range(1, len(precios))]


# ============================================================== motor

def senal_mitad(h) -> float:
    return 0.5


def correr(variante: str, activo, efectivo, senal, *, es_prueba: bool, nota: str = "", fx=None,
           moneda: str = "MXN", spread: float = S_LIQ, cortes=(CORTE,), parametros: dict | None = None,
           fuente: str = "") -> bt.ResultadoBacktest:
    return bt.backtest_senal(
        activo, efectivo, senal, id_replica=ID, variante=variante, comision_por_lado=C_GBM,
        spread_por_lado=spread, min_historia=1, exposicion_inicial=0.0, cortes=cortes, fx=fx,
        efectivo_en_mxn=fx is not None, moneda=None if fx is not None else moneda,
        parametros=parametros or {}, fuente_datos=fuente, es_prueba=es_prueba, nota=nota,
        dir_replicas=DIR_REG)


def metr(r: bt.ResultadoBacktest, seg: str = "completo") -> dict:
    return r.metricas[seg]


# ============================================================== analisis

def principal(d: dict, res: dict) -> dict:
    fr_m = d["fr_m"]
    cetes = d["SF43936"]
    meses = meses_entre(fr_m, BASE, FIN)
    p = panel_mensual(meses, fr_m["R"], fr_m["RF"], d["DEXMXUS"], lambda m: tasa_cetes_mensual(cetes, m),
                      nombre_fx="DEXMXUS")
    fuente = (f"French F-F_Research_Data_Factors CRSP {fr_m['version_crsp']} sha256 {fr_m['sha256'][:16]}; "
              f"FRED DEXMXUS huella {huella_serie(d['DEXMXUS'])}; Banxico SF43936 huella {huella_serie(cetes)}")
    P(f"\n== Especificacion principal: {meses[1]} a {meses[-1]} ({len(meses) - 1} meses), corte {CORTE} ==")
    P(f"Fuente: {fuente}")
    activo_usd = serie(meses, [fr_m["R"][m] for m in meses])
    efectivo_mxn = serie(meses, p["cet"])
    efectivo_mxn[0] = (meses[0], 0.0)
    resultados = {}

    # --- P1: sin cubrir, con el fx del motor
    r1 = correr("mxn_h000", activo_usd, efectivo_mxn, bt.senal_comprar_y_mantener, es_prueba=True,
                fx=d["DEXMXUS"], parametros={"h": 0.0, "fx": "DEXMXUS", "efectivo": "CETES28 SF43936"},
                fuente=fuente, nota="P1 sin cubrir (conversion del motor)")
    resultados["mxn_h000"] = r1
    dif = max(abs(a - b) for a, b in zip(r1.r_activo, p["U"][1:]))
    difc = max(abs(a - b) for a, b in zip(r1.r_efectivo, p["cet"][1:]))
    P(f"Control: |U propio - r_activo del motor| max = {dif:.3e}; |CETES propio - r_efectivo| max = {difc:.3e}")
    if dif > 1e-12 or difc > 1e-12:
        raise SystemExit("La construccion propia de U no coincide con la del motor")
    res["control_motor_U"] = dif
    # --- P2-P5
    for nombre, h in H_FIJAS.items():
        if h == 0.0:
            continue
        rh = rend_cubierto(p, h)
        resultados[nombre] = correr(nombre, serie(meses, rh), efectivo_mxn, bt.senal_comprar_y_mantener,
                                    es_prueba=True, parametros={"h": h, "c": 0.0, "fx": "DEXMXUS",
                                                                "cobertura": "CETES28 vs RF French"},
                                    fuente=fuente, nota=f"cobertura fija h={h}")
    # --- P6: minima varianza expansiva (auditada)
    datos_mv = list(zip(p["U"][1:], p["H"][1:]))
    auditoria = bt.auditar_constructor(constructor_minvar, datos_mv, n_cortes=24, semilla=SEMILLA)
    P(f"Auditoria de prefijo del constructor de minima varianza: causal={auditoria['causal']} "
      f"cortes={len(auditoria['cortes'])} primer_fallo={auditoria['primer_fallo']}")
    if not auditoria["causal"]:
        raise SystemExit("El constructor de minima varianza no es causal")
    dec = constructor_minvar(datos_mv)            # dec[k] = h para el mes evaluado k+1
    h_din = [0.0, 0.0] + dec[:-1]                 # indice del panel: 0 = base, 1 = primer mes (h = 0)
    resultados["mxn_hminvar_exp36"] = correr(
        "mxn_hminvar_exp36", serie(meses, rend_cubierto(p, h_din)), efectivo_mxn, bt.senal_comprar_y_mantener,
        es_prueba=True, parametros={"h": "minvar_expansiva", "min_meses": MIN_MESES_MINVAR, "recorte": [0, 1],
                                    "c": 0.0, "auditoria_causal": auditoria["causal"]},
        fuente=fuente, nota="P6 minima varianza expansiva; h_t con meses <= t-1")
    # --- P7, P8: benchmark 50/50
    resultados["bench50_h000"] = correr("bench50_h000", activo_usd, efectivo_mxn, senal_mitad, es_prueba=True,
                                        fx=d["DEXMXUS"], parametros={"peso_acciones": 0.5, "h": 0.0},
                                        fuente=fuente, nota="P7 50% sin cubrir + 50% CETES, rebalanceo mensual")
    resultados["bench50_h100"] = correr("bench50_h100", serie(meses, rend_cubierto(p, 1.0)), efectivo_mxn,
                                        senal_mitad, es_prueba=True, parametros={"peso_acciones": 0.5, "h": 1.0},
                                        fuente=fuente, nota="P8 50% cubierto + 50% CETES, rebalanceo mensual")
    # --- referencias S0
    ref_usd = correr("usd_referencia", activo_usd, serie(meses, [0.0] + p["RF"][1:]), bt.senal_comprar_y_mantener,
                     es_prueba=False, moneda="USD", parametros={"moneda": "USD"}, fuente=fuente,
                     nota="S0 referencia en USD contra RF")
    cetes100 = correr("cetes_100", activo_usd, efectivo_mxn, bt.senal_efectivo, es_prueba=False, fx=d["DEXMXUS"],
                      parametros={"exposicion": 0.0}, fuente=fuente, nota="S0 100% CETES")
    res["h_dinamica"] = {"meses": [str(m) for m in meses[1:]], "h": h_din[1:],
                         "crudo": [0.0] + constructor_minvar(datos_mv, recortar=False)[:-1]}
    return {"panel": p, "meses": meses, "resultados": resultados, "ref_usd": ref_usd, "cetes100": cetes100,
            "fuente": fuente, "efectivo": efectivo_mxn, "activo_usd": activo_usd}


def tabla_variantes(resultados: list[bt.ResultadoBacktest], seg: str) -> str:
    filas = []
    for r in resultados:
        x = r.metricas[seg]
        filas.append([r.variante, x["fecha_inicio"], x["fecha_fin"], x["n_periodos"], pct(x["cagr"]),
                      pct(x["vol_anual"]), fmt(x["sharpe"], 3), pct(x["mdd"]), fmt(x["calmar"], 3),
                      pct(x["cagr_efectivo"]), pct(x["costo_anual"], 3)])
    return tabla(["variante", "inicio (base)", "fin", "n", "CAGR", "vol", "Sharpe vs efectivo", "MDD", "Calmar",
                  "CAGR efectivo", "costo anual"], filas)


def descriptivos(pr: dict, res: dict) -> None:
    p, meses = pr["panel"], pr["meses"]
    n = len(meses)
    idx_seg = {
        "completo": (1, n),
        "dentro_muestra": (1, bisect_right(meses, CORTE)),
        "fuera_muestra": (bisect_right(meses, CORTE), n),
    }
    for nombre, (a, b) in VENTANAS_CAL.items():
        idx_seg[nombre] = (meses.index(a), meses.index(b) + 1)
    R1 = rend_cubierto(p, 1.0)
    salida = {}
    P("\n== H1: correlacion mensual de R (EUA, USD) con x (variacion de USD/MXN) ==")
    filas = []
    for seg, (a, b) in idx_seg.items():
        R, x, U, r1 = p["R"][a:b], p["x"][a:b], p["U"][a:b], R1[a:b]
        c = corr(R, x)
        ic = ic_boot_corr(R, x)
        lnx = [math.log(1 + v) for v in x]
        bet = beta_nw(x, R)
        neg = [k for k in range(len(R)) if R[k] < 0]
        pos = [k for k in range(len(R)) if R[k] >= 0]
        b_neg = beta_nw([x[k] for k in neg], [R[k] for k in neg])
        b_pos = beta_nw([x[k] for k in pos], [R[k] for k in pos])
        s = {"inicio": meses[a], "fin": meses[b - 1], "n": b - a, "corr": c, "ic95": ic, "corr_ln": corr(R, lnx),
             "beta": bet, "beta_R_neg": b_neg, "beta_R_pos": b_pos,
             "vol_usd": vol_anual(R), "vol_mxn": vol_anual(U), "vol_h100": vol_anual(r1), "vol_x": vol_anual(x)}
        salida[seg] = s
        filas.append([seg, f"{meses[a]:%Y-%m} a {meses[b - 1]:%Y-%m}", b - a, fmt(c, 3),
                      f"[{fmt(ic[0], 3)}, {fmt(ic[1], 3)}]", fmt(s["corr_ln"], 3),
                      f"{fmt(bet['b'], 3)} (t NW {fmt(bet['t_nw'], 2)})",
                      f"{fmt(b_neg['b'], 3)} / {fmt(b_pos['b'], 3)}",
                      pct(s["vol_usd"], 1), pct(s["vol_mxn"], 1), pct(s["vol_h100"], 1), pct(s["vol_x"], 1)])
    P(tabla(["segmento", "meses", "n", "corr(R,x)", "IC95 bootstrap", "corr(R,Δln S)",
             "beta de x sobre R", "beta R<0 / R≥0", "vol USD", "vol MXN sin cubrir", "vol MXN cubierto", "vol x"],
            filas))
    res["correlaciones"] = salida

    P("\n== H2: meses de caida y de alza grandes (muestra completa 1994-01 a 2026-07) ==")
    a, b = idx_seg["completo"]
    R, x, U, r1 = p["R"][a:b], p["x"][a:b], p["U"][a:b], R1[a:b]
    k10 = int(round(0.10 * len(R)))
    orden = sorted(range(len(R)), key=lambda k: R[k])
    grupos = {"R < -5%": [k for k in range(len(R)) if R[k] < -0.05],
              "peor decil de R": orden[:k10],
              "R > +5%": [k for k in range(len(R)) if R[k] > 0.05],
              "mejor decil de R": orden[-k10:],
              "todos": list(range(len(R)))}
    cond, filas = {}, []
    for g, ks in grupos.items():
        mR = statistics.fmean(R[k] for k in ks)
        mx = statistics.fmean(x[k] for k in ks)
        mU = statistics.fmean(U[k] for k in ks)
        m1 = statistics.fmean(r1[k] for k in ks)
        frac = sum(1 for k in ks if x[k] > 0) / len(ks)
        A = 1 - mU / mR if mR != 0 else None
        cond[g] = {"n": len(ks), "media_R": mR, "media_x": mx, "media_U": mU, "media_R1": m1,
                   "frac_x_pos": frac, "amortiguacion": A}
        filas.append([g, len(ks), pct(mR), pct(mx), pct(mU), pct(m1), pct(frac, 1), fmt(A, 3)])
    P(tabla(["grupo", "n", "media R (USD)", "media x (USD/MXN)", "media MXN sin cubrir", "media MXN cubierto",
             "% meses con x > 0", "amortiguación A"], filas))
    res["condicionales"] = cond
    # subsegmentos para R < -5%
    filas = []
    for seg in ("dentro_muestra", "fuera_muestra"):
        a2, b2 = idx_seg[seg]
        ks = [k for k in range(a2, b2) if p["R"][k] < -0.05]
        if ks:
            mR = statistics.fmean(p["R"][k] for k in ks)
            mU = statistics.fmean(p["U"][k] for k in ks)
            filas.append([seg, len(ks), pct(mR), pct(statistics.fmean(p["x"][k] for k in ks)), pct(mU),
                          fmt(1 - mU / mR, 3)])
            res["condicionales"][f"R < -5% {seg}"] = {"n": len(ks), "media_R": mR, "media_U": mU,
                                                       "media_x": statistics.fmean(p["x"][k] for k in ks),
                                                       "amortiguacion": 1 - mU / mR}
    P("Meses con R < -5% por segmento:")
    P(tabla(["segmento", "n", "media R", "media x", "media MXN sin cubrir", "A"], filas))
    P("Los 10 peores meses de R:")
    filas = []
    for k in orden[:10]:
        filas.append([f"{meses[a + k]:%Y-%m}", pct(R[k]), pct(x[k]), pct(U[k]), pct(r1[k])])
    P(tabla(["mes", "R (USD)", "x (USD/MXN)", "MXN sin cubrir", "MXN cubierto"], filas))

    P("\n== H4 y H5: cobertura ==")
    info = {}
    for seg in ("completo", "dentro_muestra", "fuera_muestra"):
        a2, b2 = idx_seg[seg]
        U2, R12, H2 = p["U"][a2:b2], R1[a2:b2], p["H"][a2:b2]
        ic = ic_boot_dif_vol(R12, U2)
        carry = [r - u for r, u in zip(R12, U2)]    # = f - x
        nw = newey_west(carry, 6)
        info[seg] = {"dif_vol_h1_h0": vol_anual(R12) - vol_anual(U2), "ic95_dif_vol": ic,
                     "h_minvar": h_minvar(U2, H2), "media_f_menos_x_anual": nw["media"] * 12,
                     "t_nw": nw["t"], "t_iid": nw["t_iid"], "n": b2 - a2,
                     "media_f_anual": statistics.fmean(p["f"][a2:b2]) * 12,
                     "media_x_anual": statistics.fmean(p["x"][a2:b2]) * 12}
    filas = [[seg, v["n"], pct(v["dif_vol_h1_h0"]), f"[{pct(v['ic95_dif_vol'][0])}, {pct(v['ic95_dif_vol'][1])}]",
              fmt(v["h_minvar"], 3), pct(v["media_f_anual"]), pct(v["media_x_anual"]), pct(v["media_f_menos_x_anual"]),
              f"{fmt(v['t_nw'], 2)} / {fmt(v['t_iid'], 2)}"] for seg, v in info.items()]
    P(tabla(["segmento", "n", "vol(h=1) − vol(h=0)", "IC95 bootstrap pareado", "h mín. varianza (sin recortar)",
             "media f ×12", "media x ×12", "media (f − x) ×12", "t NW(6) / t IID"], filas))
    res["cobertura"] = info
    hd = [v for v in res["h_dinamica"]["h"][MIN_MESES_MINVAR:]]
    hc = [v for v in res["h_dinamica"]["crudo"][MIN_MESES_MINVAR:]]
    res["h_dinamica_resumen"] = {"desde": res["h_dinamica"]["meses"][MIN_MESES_MINVAR], "n": len(hd),
                                 "min": min(hd), "mediana": statistics.median(hd), "max": max(hd),
                                 "crudo_min": min(hc), "crudo_mediana": statistics.median(hc), "crudo_max": max(hc),
                                 "frac_en_cero": sum(1 for v in hd if v == 0.0) / len(hd),
                                 "ultimo": hd[-1], "ultimo_crudo": hc[-1]}
    P("h dinamica (P6, recortada [0,1]) desde " + str(res["h_dinamica_resumen"]["desde"]) + ": " +
      json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in res["h_dinamica_resumen"].items()}))

    P("\n== Rendimiento por ventana (series brutas, sin costos) ==")
    filas, rend = [], {}
    for seg, (a2, b2) in idx_seg.items():
        f0, f1 = meses[a2 - 1], meses[b2 - 1]
        z = {"usd": cagr_de(p["R"][a2:b2], f0, f1), "mxn_h0": cagr_de(p["U"][a2:b2], f0, f1),
             "mxn_h1": cagr_de(R1[a2:b2], f0, f1), "fx": (p["S"][b2 - 1] / p["S"][a2 - 1]) ** (365.25 / (f1 - f0).days) - 1,
             "cetes": cagr_de(p["cet"][a2:b2], f0, f1), "rf": cagr_de(p["RF"][a2:b2], f0, f1),
             "mdd_usd": mdd_de(curva_de(meses[a2:b2], p["R"][a2:b2], f0))["mdd"],
             "mdd_mxn_h0": mdd_de(curva_de(meses[a2:b2], p["U"][a2:b2], f0))["mdd"],
             "mdd_mxn_h1": mdd_de(curva_de(meses[a2:b2], R1[a2:b2], f0))["mdd"]}
        rend[seg] = z
        filas.append([seg, f"{f0:%Y-%m} a {f1:%Y-%m}", pct(z["usd"]), pct(z["mxn_h0"]), pct(z["mxn_h1"]),
                      pct(z["fx"]), pct(z["cetes"]), pct(z["rf"]), pct(z["mdd_usd"], 1), pct(z["mdd_mxn_h0"], 1),
                      pct(z["mdd_mxn_h1"], 1)])
    P(tabla(["ventana", "base a fin", "CAGR USD", "CAGR MXN sin cubrir", "CAGR MXN cubierto", "USD/MXN anual",
             "CETES", "T-bill", "MDD USD (mensual)", "MDD MXN sin cubrir", "MDD MXN cubierto"], filas))
    res["rendimiento_ventanas"] = rend


def panel_diario(d: dict) -> dict:
    fr_d, cetes, fx = d["fr_d"], d["SF43936"], d["DEXMXUS"]
    dias = [x for x in fr_d["fechas"] if BASE <= x <= FIN]
    S = []
    for x in dias:
        v = valor_en_o_antes(fx, x)
        if v is None:
            raise dh.ErrorDatos(f"DEXMXUS sin dato en los {MAX_DIAS} dias previos a {x}")
        S.append(v[1])
    p = {"dias": dias, "S": S, "R": [0.0], "RF": [0.0], "U": [0.0], "H": [0.0], "cet": [0.0]}
    for k in range(1, len(dias)):
        x0, x1 = dias[k - 1], dias[k]
        tasa = valor_en_o_antes(cetes, x0, max_dias=31)
        cet = tasa[1] / 100 * (x1 - x0).days / 360
        r, rf = fr_d["R"][x1], fr_d["RF"][x1]
        xx = S[k] / S[k - 1] - 1
        f = (1 + cet) / (1 + rf) - 1
        p["R"].append(r)
        p["RF"].append(rf)
        p["cet"].append(cet)
        p["U"].append((1 + r) * (1 + xx) - 1)
        p["H"].append(xx - f)
    p["R1"] = [u - h for u, h in zip(p["U"], p["H"])]
    return p


def niveles(fechas: list[date], rends: list[float]) -> dict:
    """Nivel acumulado por fecha (indice 0 = base con nivel 1)."""
    nivel, v = {}, 1.0
    for k, (f, r) in enumerate(zip(fechas, rends)):
        if k > 0:
            v *= 1 + r
        nivel[f] = v
    return nivel


def puntos_ventana(fechas: list[date], a: date, b: date) -> list[date]:
    """Fechas de la ventana: el ultimo dato <= a (nivel al inicio de la ventana) y los de (a, b]."""
    previos = [f for f in fechas if f <= a]
    return ([previos[-1]] if previos else []) + [f for f in fechas if a < f <= b]


def caidas_ventanas(fechas: list[date], series_niveles: dict, etiqueta: str) -> dict:
    salida = {}
    for w, (a, b) in VENTANAS_CRISIS.items():
        fs = puntos_ventana(fechas, a, b)
        if len(fs) < 2:
            continue
        fila = {}
        ref = mdd_de([(f, series_niveles["usd"][f]) for f in fs])
        for nombre, niv in series_niveles.items():
            curva = [(f, niv[f]) for f in fs]
            z = mdd_de(curva)
            z["entre_pico_y_valle_usd"] = (niv[ref["valle"]] / niv[ref["pico"]] - 1) if ref["pico"] else 0.0
            z["punta_a_punta"] = niv[fs[-1]] / niv[fs[0]] - 1
            fila[nombre] = z
        salida[w] = fila
    filas = []
    for w, fila in salida.items():
        for nombre, z in fila.items():
            filas.append([w, nombre, pct(z["mdd"], 1), z["pico"], z["valle"], pct(z["entre_pico_y_valle_usd"], 1),
                          pct(z["punta_a_punta"], 1)])
    P(f"\n== Caidas por ventana ({etiqueta}) ==")
    P(tabla(["ventana", "serie", "MDD en la ventana", "pico", "valle", "cambio entre pico y valle de USD",
             "cambio punta a punta"], filas))
    return salida


def episodios(fechas: list[date], series_niveles: dict, etiqueta: str) -> dict:
    salida, filas = {}, []
    for e, (a, b) in EPISODIOS.items():
        fa = max(f for f in fechas if f <= a)
        fb = max(f for f in fechas if f <= b)
        salida[e] = {"desde": fa, "hasta": fb}
        for nombre, niv in series_niveles.items():
            salida[e][nombre] = niv[fb] / niv[fa] - 1
        filas.append([e, fa, fb] + [pct(salida[e][nombre], 1) for nombre in series_niveles])
    P(f"Episodios ({etiqueta}):")
    P(tabla(["episodio", "desde", "hasta"] + list(series_niveles), filas))
    return salida


def diario(d: dict, pr: dict, res: dict) -> None:
    p = panel_diario(d)
    dias = p["dias"]
    niv = {"usd": niveles(dias, p["R"]), "mxn_sin_cubrir": niveles(dias, p["U"]), "mxn_cubierto": niveles(dias, p["R1"])}
    res["caidas_diarias_french"] = caidas_ventanas(dias, niv, "diario, French rendimiento total; DEXMXUS; CETES")
    res["episodios_french"] = episodios(dias, niv, "diario, French rendimiento total")
    # mensual (mismas ventanas)
    pm, meses = pr["panel"], pr["meses"]
    R1 = rend_cubierto(pm, 1.0)
    nivm = {"usd": niveles(meses, pm["R"]), "mxn_sin_cubrir": niveles(meses, pm["U"]), "mxn_cubierto": niveles(meses, R1)}
    res["caidas_mensuales_french"] = caidas_ventanas(meses, nivm, "mensual, French rendimiento total")
    # S8: corridas diarias registradas
    fuente = (f"French diario CRSP {d['fr_d']['version_crsp']} sha256 {d['fr_d']['sha256'][:16]}; DEXMXUS; "
              f"CETES28 devengado por dia natural")
    efe = serie(dias, [0.0] + p["cet"][1:])
    act = serie(dias, [d["fr_d"]["R"][x] for x in dias])
    rd = {
        "usd_referencia_diaria": correr("usd_referencia_diaria", act, serie(dias, [0.0] + p["RF"][1:]),
                                        bt.senal_comprar_y_mantener, es_prueba=False, moneda="USD",
                                        parametros={"frecuencia": "diaria"}, fuente=fuente, nota="S8"),
        "mxn_h000_diaria": correr("mxn_h000_diaria", act, efe, bt.senal_comprar_y_mantener, es_prueba=False,
                                  fx=d["DEXMXUS"], parametros={"frecuencia": "diaria", "h": 0.0}, fuente=fuente,
                                  nota="S8"),
        "mxn_h100_diaria": correr("mxn_h100_diaria", serie(dias, p["R1"]), efe, bt.senal_comprar_y_mantener,
                                  es_prueba=False, parametros={"frecuencia": "diaria", "h": 1.0}, fuente=fuente,
                                  nota="S8 cobertura renovada a diario"),
    }
    dif = max(abs(a - b) for a, b in zip(rd["mxn_h000_diaria"].r_activo, p["U"][1:]))
    P(f"Control diario: |U propio - r_activo del motor| max = {dif:.3e}")
    res["control_motor_U_diario"] = dif
    for seg in ("completo", "dentro_muestra", "fuera_muestra"):
        P(f"S8 diario, segmento {seg}:")
        P(tabla_variantes(list(rd.values()), seg))
    res["S8"] = {k: v.metricas for k, v in rd.items()}
    # correlacion diaria (asincronica: mediodia NY contra cierre) solo como referencia
    # x = (1 + U)/(1 + R) - 1 (corregido el 2026-09-25: las corridas 1 y 2 usaban U/(1 + R) - 1)
    x_d = [(1 + p["U"][k]) / (1 + p["R"][k]) - 1 if k > 0 else 0.0 for k in range(len(dias))]
    res["corr_diaria_asincronica"] = corr(p["R"][1:], x_d[1:])
    P(f"Correlacion diaria R vs x (asincronica: DEXMXUS al mediodia vs cierre): {res['corr_diaria_asincronica']:.3f}")


def capitulo(d: dict, res: dict) -> None:
    """S3b: cifras del capitulo con ^GSPC precio x DEXMXUS."""
    P("\n== S3b: cifras del capitulo 16 con ^GSPC (precio) x DEXMXUS ==")
    g, fx = d["gspc"], d["DEXMXUS"]
    meses = [m for m in meses_entre(d["fr_m"], BASE, FIN)]
    precios, edades = precio_fin_de_mes(g, meses)
    S = [valor_en_o_antes(fx, m)[1] for m in meses]
    r = rends_de_precios(precios)
    x = [0.0] + [S[k] / S[k - 1] - 1 for k in range(1, len(S))]
    lnx = [0.0] + [math.log(S[k] / S[k - 1]) for k in range(1, len(S))]
    u = [(1 + a) * (1 + b) - 1 for a, b in zip(r, x)]
    out = {"A1": {}, "A2": {}, "A6": {}}
    filas = []
    for w, (a, b) in VENTANAS_CAL.items():
        ia, ib = meses.index(a), meses.index(b) + 1
        c = corr(r[ia:ib], lnx[ia:ib])
        vu, vm = vol_anual(r[ia:ib]), vol_anual(u[ia:ib])
        out["A1"][w] = {"propio": c, "capitulo": CAPITULO["A1_corr"][w],
                        "dentro_tolerancia": abs(c - CAPITULO["A1_corr"][w]) <= TOL["A1"]}
        cu, cm = CAPITULO["A2_vol"][w]
        out["A2"][w] = {"propio": (vu, vm), "capitulo": (cu, cm),
                        "dentro_tolerancia": abs(vu - cu) <= TOL["A2"] and abs(vm - cm) <= TOL["A2"]}
        filas.append([w, fmt(c, 3), fmt(CAPITULO["A1_corr"][w], 2), fmt(out["A1"][w]["dentro_tolerancia"]),
                      f"{pct(vu, 1)} / {pct(vm, 1)}", f"{pct(cu, 1)} / {pct(cm, 1)}",
                      fmt(out["A2"][w]["dentro_tolerancia"])])
    P(tabla(["ventana", "corr(r, Δln S) propia", "capítulo", "±0.05", "vol USD / MXN propia", "capítulo", "±0.5 pp"],
            filas))
    # A3
    ia, ib = meses.index(VENTANAS_CAL["1996-2026"][0]), len(meses)
    ks = [k for k in range(ia, ib) if r[k] < -0.05]
    a3 = {"n": len(ks), "r_usd": statistics.fmean(r[k] for k in ks), "x": statistics.fmean(x[k] for k in ks),
          "r_mxn": statistics.fmean(u[k] for k in ks)}
    a3["dentro_tolerancia"] = all(abs(a3[k] - CAPITULO["A3"][k]) <= TOL["A3"] for k in ("r_usd", "x", "r_mxn"))
    out["A3"] = a3
    P(f"A3 (meses con ^GSPC < -5%, 1996-01 a 2026-07): n={a3['n']} (capítulo 40); R USD {pct(a3['r_usd'])} "
      f"(−7.8%); x {pct(a3['x'])} (+3.7%); MXN {pct(a3['r_mxn'])} (−4.5%); dentro de ±1 pp: "
      f"{fmt(a3['dentro_tolerancia'])}")
    # A6
    filas = []
    for w, (f0, f1) in {"1996-2026": (date(1995, 12, 31), FIN), "2016-2026": (date(2015, 12, 31), FIN)}.items():
        i0, i1 = meses.index(f0), meses.index(f1)
        anios = (f1 - f0).days / 365.25
        cu = (precios[i1] / precios[i0]) ** (1 / anios) - 1
        cm = (precios[i1] * S[i1] / (precios[i0] * S[i0])) ** (1 / anios) - 1
        cfx = (S[i1] / S[i0]) ** (1 / anios) - 1
        k = CAPITULO["A6"][w]
        ok = abs(cu - k[0]) <= TOL["A6"] and abs(cm - k[1]) <= TOL["A6"] and abs(cfx - k[2]) <= TOL["A6"]
        out["A6"][w] = {"propio": (cu, cm, cfx), "capitulo": k, "dentro_tolerancia": ok}
        filas.append([w, f"{f0} a {f1}", f"{pct(cu)} / {pct(cm)} / {pct(cfx)}",
                      f"{pct(k[0])} / {pct(k[1])} / {pct(k[2])}", fmt(ok)])
    P(tabla(["ventana", "base a fin", "CAGR USD / MXN / USD-MXN propio", "capítulo", "±0.30 pp"], filas))
    # A4 y A5 (diario)
    dias = [f for f in g._fechas if BASE <= f <= FIN]
    niv_u, niv_m = {}, {}
    for f in dias:
        v = valor_en_o_antes(g, f)[1]
        s = valor_en_o_antes(fx, f)
        if s is None:
            raise dh.ErrorDatos(f"DEXMXUS sin dato cerca de {f}")
        niv_u[f] = v
        niv_m[f] = v * s[1]
    cd = caidas_ventanas(dias, {"usd": niv_u, "mxn_sin_cubrir": niv_m}, "diario, ^GSPC precio x DEXMXUS")
    out["A4"] = {}
    for w, (cu, cm) in CAPITULO["A4"].items():
        pu, pm_ = cd[w]["usd"]["mdd"], cd[w]["mxn_sin_cubrir"]["mdd"]
        out["A4"][w] = {"propio": (pu, pm_), "capitulo": (cu, cm),
                        "dentro_tolerancia": abs(pu - cu) <= TOL["A4"] and abs(pm_ - cm) <= TOL["A4"]}
        P(f"A4 {w}: propio {pct(pu, 1)} / {pct(pm_, 1)}; capítulo {pct(cu, 1)} / {pct(cm, 1)}; ±1 pp: "
          f"{fmt(out['A4'][w]['dentro_tolerancia'])}")
    out["A5"] = episodios(dias, {"usd": niv_u, "mxn_sin_cubrir": niv_m}, "diario, ^GSPC precio")
    out["caidas"] = cd
    out["edad_max_precio_mensual_dias"] = max(edades)
    res["capitulo"] = out
    # motor (S3b)
    efe = serie(meses, [0.0] + [tasa_cetes_mensual(d["SF43936"], m) for m in meses[1:]])
    rf = serie(meses, [0.0] + [d["fr_m"]["RF"][m] for m in meses[1:]])
    fuente = f"Yahoo ^GSPC (precio) huella {huella_serie(g)}; DEXMXUS"
    r_u = correr("gspc_precio_usd", serie(meses, r), rf, bt.senal_comprar_y_mantener, es_prueba=False,
                 moneda="USD", parametros={"indice": "^GSPC precio"}, fuente=fuente, nota="S3b capitulo")
    r_m = correr("gspc_precio_mxn_h000", serie(meses, r), efe, bt.senal_comprar_y_mantener, es_prueba=False,
                 fx=d["DEXMXUS"], parametros={"indice": "^GSPC precio", "h": 0.0}, fuente=fuente, nota="S3b capitulo")
    res["S3b_motor"] = {"gspc_precio_usd": r_u.metricas, "gspc_precio_mxn_h000": r_m.metricas}


def sensibilidades(d: dict, pr: dict, res: dict) -> None:
    fr_m, cetes = d["fr_m"], d["SF43936"]
    sens = {}
    P("\n== Sensibilidades (es_prueba=0) ==")

    def bloque(etiqueta, rs, segs=("completo", "dentro_muestra", "fuera_muestra")):
        for seg in segs:
            if all(seg in r.metricas for r in rs):
                P(f"{etiqueta}, segmento {seg}:")
                P(tabla_variantes(rs, seg))
        sens[etiqueta] = {r.variante: r.metricas for r in rs}

    # S1: FIX
    meses = pr["meses"]
    pf = panel_mensual(meses, fr_m["R"], fr_m["RF"], d["SF43718"], lambda m: tasa_cetes_mensual(cetes, m), nombre_fx="FIX")
    fu = f"French CRSP {fr_m['version_crsp']}; Banxico FIX SF43718 huella {huella_serie(d['SF43718'])}; CETES SF43936"
    rs = [correr("mxn_h000_fix", pr["activo_usd"], pr["efectivo"], bt.senal_comprar_y_mantener, es_prueba=False,
                 fx=d["SF43718"], parametros={"h": 0.0, "fx": "FIX"}, fuente=fu, nota="S1"),
          correr("mxn_h100_fix", serie(meses, rend_cubierto(pf, 1.0)), pr["efectivo"], bt.senal_comprar_y_mantener,
                 es_prueba=False, parametros={"h": 1.0, "fx": "FIX"}, fuente=fu, nota="S1")]
    bloque("S1 FIX", rs)
    sens["S1_corr_completo"] = corr(pf["R"][1:], pf["x"][1:])
    P(f"S1 corr(R, x) con FIX 1994-01 a 2026-07: {sens['S1_corr_completo']:.3f}")

    # S2: extension con FIX desde 1991-12
    m2 = meses_entre(fr_m, BASE_FIX, FIN)
    p2 = panel_mensual(m2, fr_m["R"], fr_m["RF"], d["SF43718"], lambda m: tasa_cetes_mensual(cetes, m), nombre_fx="FIX")
    efe2 = serie(m2, p2["cet"])
    act2 = serie(m2, [fr_m["R"][m] for m in m2])
    rs = [correr("mxn_h000_fix_desde1991", act2, efe2, bt.senal_comprar_y_mantener, es_prueba=False, fx=d["SF43718"],
                 parametros={"h": 0.0, "fx": "FIX", "base": str(BASE_FIX)}, fuente=fu, nota="S2"),
          correr("mxn_h100_fix_desde1991", serie(m2, rend_cubierto(p2, 1.0)), efe2, bt.senal_comprar_y_mantener,
                 es_prueba=False, parametros={"h": 1.0, "fx": "FIX", "base": str(BASE_FIX)}, fuente=fu, nota="S2"),
          correr("usd_referencia_desde1991", act2, serie(m2, [0.0] + p2["RF"][1:]), bt.senal_comprar_y_mantener,
                 es_prueba=False, moneda="USD", parametros={"base": str(BASE_FIX)}, fuente=fu, nota="S2")]
    bloque("S2 FIX desde 1991-12", rs)
    ib = m2.index(date(1994, 11, 30)) + 1
    sens["S2_corr"] = {"1991-12 a 2026-07": corr(p2["R"][1:], p2["x"][1:]),
                       "bandas 1991-12 a 1994-11": corr(p2["R"][1:ib], p2["x"][1:ib]),
                       "ic95_completo": ic_boot_corr(p2["R"][1:], p2["x"][1:]),
                       "n_bandas": ib - 1}
    P("S2 correlaciones: " + json.dumps({k: (round(v, 4) if isinstance(v, float) else v)
                                          for k, v in sens["S2_corr"].items()}, default=str))

    # S3a: ^SP500TR
    ps, _ = precio_fin_de_mes(d["sp500tr"], meses)
    rsp = rends_de_precios(ps)
    Rsp = {m: v for m, v in zip(meses, rsp)}
    p3 = panel_mensual(meses, Rsp, fr_m["RF"], d["DEXMXUS"], lambda m: tasa_cetes_mensual(cetes, m), nombre_fx="DEXMXUS")
    fu3 = f"Yahoo ^SP500TR huella {huella_serie(d['sp500tr'])}; DEXMXUS; CETES SF43936; RF French"
    rs = [correr("mxn_h000_sp500tr", serie(meses, rsp), pr["efectivo"], bt.senal_comprar_y_mantener, es_prueba=False,
                 fx=d["DEXMXUS"], parametros={"h": 0.0, "activo": "^SP500TR"}, fuente=fu3, nota="S3a"),
          correr("mxn_h100_sp500tr", serie(meses, rend_cubierto(p3, 1.0)), pr["efectivo"], bt.senal_comprar_y_mantener,
                 es_prueba=False, parametros={"h": 1.0, "activo": "^SP500TR"}, fuente=fu3, nota="S3a"),
          correr("usd_referencia_sp500tr", serie(meses, rsp), serie(meses, [0.0] + p3["RF"][1:]),
                 bt.senal_comprar_y_mantener, es_prueba=False, moneda="USD", parametros={"activo": "^SP500TR"},
                 fuente=fu3, nota="S3a")]
    bloque("S3a ^SP500TR", rs)
    sens["S3a_corr_completo"] = corr(p3["R"][1:], p3["x"][1:])
    sens["S3a_corr_con_french"] = corr(p3["R"][1:], pr["panel"]["R"][1:])
    P(f"S3a corr(R_sp500tr, x) = {sens['S3a_corr_completo']:.3f}; corr(R_sp500tr, R_french) = "
      f"{sens['S3a_corr_con_french']:.4f}")

    # S4: tasas interbancarias para la cobertura (1997-02 a 2026-07)
    m4 = meses_entre(fr_m, BASE_IB, FIN)
    p4 = panel_mensual(m4, fr_m["R"], fr_m["RF"], d["DEXMXUS"],
                       lambda m: tasa_fred_mes_anterior(d["IR3TIB01MXM156N"], m),
                       i_us=lambda m: tasa_fred_mes_anterior(d["IR3TIB01USM156N"], m, max_dias=62),
                       nombre_fx="DEXMXUS")
    efe4 = serie(m4, [0.0] + [tasa_cetes_mensual(cetes, m) for m in m4[1:]])
    fu4 = "French; DEXMXUS; cobertura con OCDE IR3TIB01MXM156N vs IR3TIB01USM156N (mes t-1 /1200); efectivo CETES"
    rs = [correr("mxn_h000_desde1997", serie(m4, [fr_m["R"][m] for m in m4]), efe4, bt.senal_comprar_y_mantener,
                 es_prueba=False, fx=d["DEXMXUS"], parametros={"h": 0.0, "base": str(BASE_IB)}, fuente=fu4, nota="S4"),
          correr("mxn_h050_interbancaria", serie(m4, rend_cubierto(p4, 0.5)), efe4, bt.senal_comprar_y_mantener,
                 es_prueba=False, parametros={"h": 0.5, "tasas": "interbancarias"}, fuente=fu4, nota="S4"),
          correr("mxn_h100_interbancaria", serie(m4, rend_cubierto(p4, 1.0)), efe4, bt.senal_comprar_y_mantener,
                 es_prueba=False, parametros={"h": 1.0, "tasas": "interbancarias"}, fuente=fu4, nota="S4")]
    bloque("S4 cobertura con tasas interbancarias", rs)
    carry4 = [a - b for a, b in zip(rend_cubierto(p4, 1.0)[1:], p4["U"][1:])]
    nw4 = newey_west(carry4, 6)
    sens["S4_carry"] = {"media_anual": nw4["media"] * 12, "t_nw": nw4["t"], "t_iid": nw4["t_iid"],
                        "media_f_anual": statistics.fmean(p4["f"][1:]) * 12}
    P(f"S4 media (f - x) x12 = {pct(nw4['media'] * 12)} (t NW {nw4['t']:.2f}); media f x12 = "
      f"{pct(sens['S4_carry']['media_f_anual'])}")

    # S5: CETES aproximado del FMI
    p5 = panel_mensual(meses, fr_m["R"], fr_m["RF"], d["DEXMXUS"],
                       lambda m: tasa_fred_mes_anterior(d["INTGSTMXM193N"], m), nombre_fx="DEXMXUS")
    efe5 = serie(meses, p5["cet"])
    fu5 = "French; DEXMXUS; CETES = FRED INTGSTMXM193N (mes t-1 /1200)"
    rs = [correr("mxn_h000_cetes_fmi", pr["activo_usd"], efe5, bt.senal_comprar_y_mantener, es_prueba=False,
                 fx=d["DEXMXUS"], parametros={"h": 0.0, "efectivo": "INTGSTMXM193N"}, fuente=fu5, nota="S5"),
          correr("mxn_h100_cetes_fmi", serie(meses, rend_cubierto(p5, 1.0)), efe5, bt.senal_comprar_y_mantener,
                 es_prueba=False, parametros={"h": 1.0, "efectivo": "INTGSTMXM193N"}, fuente=fu5, nota="S5")]
    bloque("S5 CETES del FMI", rs)

    # S6: costo de la cobertura
    p = pr["panel"]
    fu6 = pr["fuente"]
    rs = []
    h_din = [0.0] + res["h_dinamica"]["h"]
    for c in (0.005, 0.01):
        etiqueta = f"costo{int(round(c * 1e4)):03d}"
        for nombre, h in H_FIJAS.items():
            if h == 0.0:
                continue
            rs.append(correr(f"{nombre}_{etiqueta}", serie(meses, rend_cubierto(p, h, c)), pr["efectivo"],
                             bt.senal_comprar_y_mantener, es_prueba=False, parametros={"h": h, "c": c},
                             fuente=fu6, nota="S6"))
        rs.append(correr(f"mxn_hminvar_exp36_{etiqueta}", serie(meses, rend_cubierto(p, h_din, c)), pr["efectivo"],
                         bt.senal_comprar_y_mantener, es_prueba=False, parametros={"h": "minvar_expansiva", "c": c},
                         fuente=fu6, nota="S6"))
        rs.append(correr(f"bench50_h100_{etiqueta}", serie(meses, rend_cubierto(p, 1.0, c)), pr["efectivo"],
                         senal_mitad, es_prueba=False, parametros={"peso_acciones": 0.5, "h": 1.0, "c": c},
                         fuente=fu6, nota="S6"))
    bloque("S6 costo de la cobertura", rs, segs=("completo", "fuera_muestra"))

    # S7: spread medio
    rs = []
    for nombre, r0 in pr["resultados"].items():
        if nombre in ("mxn_h000", "bench50_h000"):
            act, fx = pr["activo_usd"], d["DEXMXUS"]
        else:
            act, fx = serie(meses, [0.0] + list(r0.r_activo)), None
        sen = senal_mitad if nombre.startswith("bench50") else bt.senal_comprar_y_mantener
        rs.append(correr(f"{nombre}_spread_medio", act, pr["efectivo"], sen, es_prueba=False, fx=fx, spread=S_MED,
                         parametros={"base": nombre, "spread": S_MED}, fuente=pr["fuente"], nota="S7"))
    bloque("S7 spread medio", rs, segs=("completo", "fuera_muestra"))
    res["sensibilidades"] = sens


def ivvpeso(d: dict, res: dict) -> None:
    """S9: IVVPESO.MX contra el S&P 500 TR cubierto sintetico y sin cubrir, 2014-12 a 2026-07."""
    P("\n== S9: IVVPESO.MX (cubierto real) ==")
    fr_m, cetes = d["fr_m"], d["SF43936"]
    meses = meses_entre(fr_m, BASE_IVV, FIN)
    pi, edades = precio_fin_de_mes(d["ivvpeso"], meses)
    ri = rends_de_precios(pi)
    ps, _ = precio_fin_de_mes(d["sp500tr"], meses)
    rsp = rends_de_precios(ps)
    Rsp = {m: v for m, v in zip(meses, rsp)}
    p = panel_mensual(meses, Rsp, fr_m["RF"], d["DEXMXUS"], lambda m: tasa_cetes_mensual(cetes, m), nombre_fx="DEXMXUS")
    r1 = rend_cubierto(p, 1.0)
    efe = serie(meses, p["cet"])
    fu = (f"Yahoo IVVPESO.MX huella {huella_serie(d['ivvpeso'])}; ^SP500TR huella {huella_serie(d['sp500tr'])}; "
          f"DEXMXUS; CETES SF43936; RF French")
    rs = [correr("ivvpeso_real", serie(meses, ri), efe, bt.senal_comprar_y_mantener, es_prueba=False, cortes=(),
                 parametros={"instrumento": "IVVPESO.MX"}, fuente=fu, nota="S9"),
          correr("sp500tr_mxn_h100_sintetico", serie(meses, r1), efe, bt.senal_comprar_y_mantener, es_prueba=False,
                 cortes=(), parametros={"h": 1.0, "activo": "^SP500TR"}, fuente=fu, nota="S9"),
          correr("sp500tr_mxn_h000", serie(meses, rsp), efe, bt.senal_comprar_y_mantener, es_prueba=False, cortes=(),
                 fx=d["DEXMXUS"], parametros={"h": 0.0, "activo": "^SP500TR"}, fuente=fu, nota="S9")]
    P(tabla_variantes(rs, "completo"))
    difs = [a - b for a, b in zip(ri[1:], r1[1:])]
    out = {"n": len(meses) - 1, "corr_ivvpeso_sintetico": corr(ri[1:], r1[1:]),
           "corr_ivvpeso_sin_cubrir": corr(ri[1:], rs[2].r_activo),
           "error_seguimiento_anual": vol_anual(difs), "media_dif_anual": statistics.fmean(difs) * 12,
           "meses_precio_viejo_mas_de_3_dias": sum(1 for e in edades if e > 3), "edad_max_dias": max(edades),
           "metricas": {r.variante: r.metricas["completo"] for r in rs},
           "vol_ivvpeso": vol_anual(ri[1:]), "vol_sin_cubrir": vol_anual(rs[2].r_activo),
           "meta": d["ivvpeso_meta"]}
    P(f"corr(IVVPESO, cubierto sintetico) = {out['corr_ivvpeso_sintetico']:.3f}; corr(IVVPESO, sin cubrir) = "
      f"{out['corr_ivvpeso_sin_cubrir']:.3f}; error de seguimiento anual = {pct(out['error_seguimiento_anual'])}; "
      f"media de la diferencia x12 = {pct(out['media_dif_anual'])}; meses con precio de mas de 3 dias = "
      f"{out['meses_precio_viejo_mas_de_3_dias']} (max {out['edad_max_dias']} dias)")
    niv = {"ivvpeso": niveles(meses, ri), "sintetico_h1": niveles(meses, r1), "sin_cubrir": niveles(meses, [0.0] + list(rs[2].r_activo))}
    filas = []
    for w in ("2020", "2022"):
        a, b = VENTANAS_CRISIS[w]
        fs = puntos_ventana(meses, a, b)
        fila = [w]
        for nombre in niv:
            fila.append(pct(mdd_de([(f, niv[nombre][f]) for f in fs])["mdd"], 1))
        filas.append(fila)
        out[f"mdd_mensual_{w}"] = dict(zip(niv, [mdd_de([(f, niv[n][f]) for f in fs])["mdd"] for n in niv]))
    P("MDD mensual (nivel inicial = ultimo cierre de mes <= inicio de la ventana):")
    P(tabla(["ventana", "IVVPESO", "S&P TR cubierto sintético", "S&P TR sin cubrir"], filas))
    res["S9"] = out


def veredictos(pr: dict, res: dict) -> dict:
    R = pr["resultados"]
    m = {k: v.metricas for k, v in R.items()}
    co, cd = res["correlaciones"], res["caidas_diarias_french"]
    cond, cob = res["condicionales"], res["cobertura"]
    v: dict = {}
    # H1
    v["H1_refutada"] = not (co["completo"]["corr"] < 0 and co["completo"]["ic95"][1] < 0)
    v["H1_en_rango"] = -0.60 <= co["completo"]["corr"] <= -0.35
    v["H1_negativa_en"] = {s: co[s]["corr"] < 0 for s in ("dentro_muestra", "fuera_muestra", "2008-2026", "2016-2026")}
    # H2
    g = cond["R < -5%"]
    v["H2"] = {"media_x_positiva": g["media_x"] > 0, "media_x_en_rango": 0.02 <= g["media_x"] <= 0.05,
               "A_en_rango": 0.25 <= g["amortiguacion"] <= 0.60,
               "peor_decil_signo": cond["peor decil de R"]["media_x"] > 0 and cond["peor decil de R"]["amortiguacion"] > 0}
    # H3
    dif = {w: cd[w]["mxn_sin_cubrir"]["mdd"] - cd[w]["usd"]["mdd"] for w in cd}
    v["H3_diferencias_pp"] = dif
    v["H3"] = {"crisis_financiera_>=10pp": dif["crisis_financiera"] >= 0.10, "2020_>=10pp": dif["2020"] >= 0.10,
               "2022_no_mejor_>5pp": dif["2022"] <= 0.05}
    v["H3_refutada"] = dif["crisis_financiera"] < 0.05 or dif["2020"] < 0.05
    # H4
    vd = {s: m["mxn_h100"][s]["vol_anual"] - m["mxn_h000"][s]["vol_anual"] for s in ("completo", "dentro_muestra", "fuera_muestra")}
    md = {s: m["mxn_h100"][s]["mdd"] - m["mxn_h000"][s]["mdd"] for s in ("completo", "fuera_muestra")}
    vols = [m[n]["completo"]["vol_anual"] for n in H_FIJAS]
    v["H4"] = {"dif_vol": vd, "dif_mdd": md,
               "vol_>=1pp_en_todos": all(x >= 0.01 for x in vd.values()),
               "mdd_h1_mas_profunda_>=5pp": all(x <= -0.05 for x in md.values()),
               "vol_monotona_en_h": all(a < b for a, b in zip(vols, vols[1:])),
               "h_minvar_completo_<=0.25": cob["completo"]["h_minvar"] <= 0.25}
    v["H4_refutada"] = vd["completo"] <= 0 or vd["fuera_muestra"] <= 0
    # H5
    dc = m["mxn_h100"]["completo"]["cagr"] - m["mxn_h000"]["completo"]["cagr"]
    v["H5"] = {"dif_cagr_h1_h0": dc, "positiva": dc > 0, "en_rango": 0.005 <= dc <= 0.04,
               "media_f_menos_x_anual": cob["completo"]["media_f_menos_x_anual"], "t_nw": cob["completo"]["t_nw"]}
    # H6
    v["H6"] = {s: {"vol_menor": m["bench50_h000"][s]["vol_anual"] < m["bench50_h100"][s]["vol_anual"],
                   "mdd_menor": m["bench50_h000"][s]["mdd"] > m["bench50_h100"][s]["mdd"]}
               for s in ("completo", "fuera_muestra")}
    # H7
    dv7 = m["mxn_hminvar_exp36"]["fuera_muestra"]["vol_anual"] - m["mxn_h000"]["fuera_muestra"]["vol_anual"]
    dm7 = m["mxn_hminvar_exp36"]["fuera_muestra"]["mdd"] - m["mxn_h000"]["fuera_muestra"]["mdd"]
    v["H7"] = {"dif_vol_fuera": dv7, "dif_mdd_fuera": dm7, "no_reduce_0.5pp": dv7 > -0.005}
    v["P6_se_adopta"] = dv7 <= -0.005 and dm7 >= -0.02
    # estado
    h1_ok = not v["H1_refutada"]
    h4_ok = not v["H4_refutada"]
    if not (h1_ok and h4_ok):
        estado = "No replicado"
    else:
        magnitudes = (v["H1_en_rango"] and all(v["H1_negativa_en"].values()) and all(v["H2"].values())
                      and all(v["H3"].values()) and all(v["H4"][k] for k in ("vol_>=1pp_en_todos",
                                                                             "mdd_h1_mas_profunda_>=5pp",
                                                                             "vol_monotona_en_h",
                                                                             "h_minvar_completo_<=0.25")))
        cap = res["capitulo"]
        tolerancias = (all(x["dentro_tolerancia"] for x in cap["A1"].values())
                       and all(x["dentro_tolerancia"] for x in cap["A2"].values())
                       and cap["A3"]["dentro_tolerancia"]
                       and all(x["dentro_tolerancia"] for x in cap["A4"].values())
                       and all(x["dentro_tolerancia"] for x in cap["A6"].values()))
        v["magnitudes_en_rango"] = magnitudes
        v["capitulo_en_tolerancia"] = tolerancias
        estado = "Replicado" if (magnitudes and tolerancias and not v["H3_refutada"]) else "Replicado con diferencias"
    v["estado_automatico"] = estado
    # regla operable
    fuera_h1 = co["fuera_muestra"]["corr"] < 0 and co["fuera_muestra"]["ic95"][1] < 0
    fuera_h4 = vd["fuera_muestra"] >= 0.01 and md["fuera_muestra"] <= -0.05
    fuera_h6 = v["H6"]["fuera_muestra"]["vol_menor"] and v["H6"]["fuera_muestra"]["mdd_menor"]
    h3_ok = v["H3"]["crisis_financiera_>=10pp"] and v["H3"]["2020_>=10pp"]
    parcial = [n for n in ("mxn_h025", "mxn_h050")
               if m[n]["fuera_muestra"]["vol_anual"] < m["mxn_h000"]["fuera_muestra"]["vol_anual"]
               and m[n]["fuera_muestra"]["mdd"] > m["mxn_h000"]["fuera_muestra"]["mdd"]]
    costo_grande = cob["completo"]["media_f_menos_x_anual"] > 0.03 and cob["completo"]["t_nw"] >= 2
    if v["H4_refutada"]:
        regla = "descarta"
    elif parcial or costo_grande:
        regla = "modifica"
    elif fuera_h1 and h3_ok and fuera_h4 and fuera_h6:
        regla = "confirma"
    else:
        regla = "sin decision (condiciones de confirmacion incompletas)"
    v["regla_operable"] = {"decision": regla, "H1_fuera": fuera_h1, "H3_2008_2020": h3_ok, "H4_fuera": fuera_h4,
                           "H6_fuera": fuera_h6, "coberturas_parciales_mejores_fuera": parcial,
                           "costo_no_cubrir_>3pp_signif": costo_grande}
    return v


# ============================================================== main

def main() -> None:
    global DIR_REG
    ap = argparse.ArgumentParser()
    ap.add_argument("--prueba-sintetica", action="store_true")
    args = ap.parse_args()
    inicio = datetime.now(timezone.utc)
    if args.prueba_sintetica:
        tmp = Path(tempfile.mkdtemp(prefix="R08-prueba-"))
        DIR_REG = tmp
        d = datos_sinteticos()
        destino = tmp
        P(f"MODO PRUEBA SINTETICA: registro en {tmp} (el real no se toca)")
    else:
        DIR_REG = None
        h = verificar_pre_registro()
        P(f"R08 - corrida {inicio:%Y-%m-%d %H:%M:%S} UTC. Pre-registro verificado (sha256 {h[:16]}...)")
        d = cargar_datos()
        destino = AQUI
    P(f"Datos: {d['huellas_estado']}")
    fr_m, fr_d = d["fr_m"], d["fr_d"]
    P(f"French mensual CRSP {fr_m['version_crsp']} sha256 {fr_m['sha256']} rango {fr_m['rango']}")
    P(f"French diario CRSP {fr_d['version_crsp']} sha256 {fr_d['sha256']} rango {fr_d['rango']}")
    for s in ("DEXMXUS", "SF43718", "SF43936", "INTGSTMXM193N", "IR3TIB01MXM156N", "IR3TIB01USM156N"):
        P(f"{s}: {d[s][0][0]} a {d[s][-1][0]} n={len(d[s])} huella {huella_serie(d[s])}")
    for k in TICKERS:
        mm = d[k + "_meta"]
        P(f"{mm['ticker']}: {mm['rango'][0]} a {mm['rango'][1]} n={mm['n']} moneda {mm['moneda']} "
          f"adjclose={mm['usa_adjclose']} difiere_de_close={mm['adjclose_difiere_de_close']} "
          f"sin_precio={len(mm['fechas_sin_precio'])}")
    res: dict = {"corrida_utc": inicio.isoformat(timespec="seconds"), "modo": "sintetico" if args.prueba_sintetica else "real",
                 "sha_pre_registro": SHA_PRE_REGISTRO, "manifiesto": d["manifiesto"],
                 "french": {"mensual": {k: fr_m[k] for k in ("version_crsp", "sha256", "rango")},
                            "diario": {k: fr_d[k] for k in ("version_crsp", "sha256", "rango")}}}

    pr = principal(d, res)
    todos = list(pr["resultados"].values()) + [pr["ref_usd"], pr["cetes100"]]
    for seg in ("completo", "dentro_muestra", "fuera_muestra"):
        P(f"\n== Variantes P1-P8 y referencias, segmento {seg} (motor, neto de costos) ==")
        P(tabla_variantes(todos, seg))
    P("\nTabla de comparar() del motor (completo):")
    P(bt.comparar(todos, "completo"))
    res["variantes"] = {r.variante: r.metricas for r in todos}
    descriptivos(pr, res)
    diario(d, pr, res)
    capitulo(d, res)
    sensibilidades(d, pr, res)
    ivvpeso(d, res)

    P("\n== Sharpe deflactado (registro R08, es_prueba=1) ==")
    dsr = {}
    for etiqueta, var in (("elegida", None), ("mxn_h000", "mxn_h000"), ("mxn_h100", "mxn_h100")):
        x = bt.sharpe_deflactado_de_registro(ID, variante=var, dir_replicas=DIR_REG)
        dsr[etiqueta] = x
        P(f"{etiqueta}: " + json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in x.items()}))
    res["dsr"] = dsr

    v = veredictos(pr, res)
    res["veredictos"] = v
    P("\n== Veredictos automaticos (reglas pre-registradas) ==")
    P(json.dumps(v, indent=1, ensure_ascii=False, default=str))

    (destino / "R08-resultados.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    (destino / "R08-salida.txt").write_text("\n".join(SALIDA) + "\n", encoding="utf-8")
    P(f"\nSalidas: {destino / 'R08-resultados.json'}, {destino / 'R08-salida.txt'}, registro "
      f"{bt.ruta_registro(ID, DIR_REG)}")


if __name__ == "__main__":
    main()
