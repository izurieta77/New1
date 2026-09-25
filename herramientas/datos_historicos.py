"""Series historicas largas para las replicas del laboratorio (solo biblioteca estandar).

Fuentes:
- Kenneth French Data Library: zip con CSV; se cachea en datos/cache/french/.
- Yahoo Finance chart v8: historia completa de precios (adjclose si existe).
- FRED: ultima version de una serie.
- ALFRED: la serie tal como se conocia en una fecha (vintage), sin look-ahead.

Hallazgos verificados en vivo el 2026-09-25 (se documentan porque cambian resultados):
1. French: los CSV traen notas al inicio, una tabla principal (YYYYMM o YYYYMMDD), una
   seccion "Annual Factors" (YYYY) y una linea de copyright; fin de linea CRLF. Desde 2025
   el preambulo declara la version CRSP ("created using the 202607 CRSP database") y el
   cambio de fuente de la T-bill en 202406 (Ibbotson -> ICE BofA). El archivo de momentum
   trae 10 lineas de notas antes del encabezado y marca faltantes con -99.99 o -999.
   El parser no depende de numeros de linea: detecta encabezado + filas numericas.
2. Yahoo: con range=max la API degrada la granularidad en silencio (pide 1mo o 1d y
   devuelve dataGranularity=3mo, 169 puntos desde 1984). Por eso yahoo_historia pide
   period1=1900-01-01 / period2=2100-01-01, que devuelve la granularidad pedida
   (^GSPC: 1d desde 1927-12-30; 1mo desde 1985-01). Si la granularidad devuelta no es
   la pedida se lanza ErrorDatos.
3. Yahoo mensual: cada barra tiene fecha del dia 1 del mes pero su cierre es el del
   ULTIMO dia de negociacion del mes; se re-etiqueta a fin de mes calendario para alinear
   con French. Yahoo agrega el mes en curso y un punto "en vivo" (regularMarketTime):
   por defecto se descartan los periodos incompletos.
4. ^GSPC es indice de precio: adjclose == close (sin dividendos). Para rendimiento total
   usa ^SP500TR (Yahoo) o Mkt-RF + RF de French.
5. ALFRED responde 404 si la fecha de vintage es anterior a la primera publicacion.

Convenciones: fechas datetime.date; rendimientos y factores French en decimales (1% = 0.01).
"""
from __future__ import annotations

import calendar
import csv
import hashlib
import io
import json
import os
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from herramientas import datos
from herramientas.datos import ErrorDatos
from herramientas.parametros import DIR_CACHE

URL_FRENCH = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
URL_ALFRED = "https://alfred.stlouisfed.org/graph/alfredgraph.csv"
DIR_CACHE_FRENCH = DIR_CACHE / "french"
FALTANTES_FRENCH = (-99.99, -999.0)
TIMEOUT_ZIP_S = 60

# period1 / period2 fijos: URL estable (cacheable) y granularidad completa (ver hallazgo 2).
YAHOO_PERIODO_1 = -2208988800  # 1900-01-01 UTC
YAHOO_PERIODO_2 = 4102444800   # 2100-01-01 UTC
INTERVALOS_YAHOO = {"1d", "1wk", "1mo"}

DIGITOS_POR_FRECUENCIA = {"diaria": 8, "semanal": 8, "mensual": 6, "anual": 4}
FRECUENCIA_POR_DIGITOS = {8: "diaria", 6: "mensual", 4: "anual"}
# Secciones de archivos de carteras que NO estan en porcentaje (no se dividen entre 100).
TITULOS_NO_PORCENTAJE = ("number of firms", "average firm size", "average market cap",
                         "sum of be", "be/me", "be / me", "value weight average of")


# ================================================================ utilidades de fecha

def fin_de_mes(anio: int, mes: int) -> date:
    return date(anio, mes, calendar.monthrange(anio, mes)[1])


def a_fin_de_mes(fecha: date) -> date:
    return fin_de_mes(fecha.year, fecha.month)


def _fecha_french(token: str) -> date:
    """YYYYMMDD -> ese dia; YYYYMM -> fin de mes; YYYY -> 31-dic."""
    if len(token) == 8:
        return date(int(token[:4]), int(token[4:6]), int(token[6:]))
    if len(token) == 6:
        return fin_de_mes(int(token[:4]), int(token[4:]))
    if len(token) == 4:
        return date(int(token), 12, 31)
    raise ErrorDatos(f"Fecha French no reconocida: {token!r}")


# ================================================================ Kenneth French

def nombre_zip_french(nombre_archivo: str) -> str:
    """'F-F_Research_Data_Factors' | '..._CSV' | '..._CSV.zip' -> '..._CSV.zip'."""
    nombre = nombre_archivo.strip().split("/")[-1]
    if nombre.lower().endswith(".zip"):
        return nombre
    if nombre.endswith("_CSV"):
        return nombre + ".zip"
    return nombre + "_CSV.zip"


def _es_fila_datos(celdas: list[str]) -> bool:
    return bool(celdas) and celdas[0].strip().isdigit() and len(celdas[0].strip()) in FRECUENCIA_POR_DIGITOS


def _es_porcentaje(titulo: str) -> bool:
    t = titulo.lower()
    return not any(clave in t for clave in TITULOS_NO_PORCENTAJE)


def parsear_french_csv(texto: str) -> dict:
    """Divide un CSV de French en notas y tablas.

    Devuelve {'notas': [lineas antes de la primera tabla], 'tablas': [tabla, ...]} donde
    tabla = {'titulo', 'columnas', 'frecuencia', 'digitos', 'periodos': [token],
             'filas': [[valor crudo | None]], 'linea': n, 'porcentaje': bool}.
    Una tabla empieza en una linea con comas cuya primera celda no es fecha y a la que
    sigue una fila de datos con el mismo numero de celdas; termina en la primera linea que
    no es fila de datos. El titulo es el bloque de texto pegado al encabezado (desde la
    ultima linea en blanco), p. ej. 'Annual Factors: January-December'; '' si no hay.
    Valores -99.99 / -999 -> None.
    """
    lineas = texto.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    celdas_por_linea = [next(csv.reader([l])) if l.strip() else [] for l in lineas]
    notas: list[str] = []
    tablas: list[dict] = []
    bloque: list[str] = []  # lineas de texto desde la ultima linea en blanco
    i = 0
    while i < len(lineas):
        celdas = celdas_por_linea[i]
        siguiente = celdas_por_linea[i + 1] if i + 1 < len(lineas) else []
        es_encabezado = (len(celdas) >= 2 and not _es_fila_datos(celdas)
                         and _es_fila_datos(siguiente) and len(siguiente) == len(celdas))
        if not es_encabezado:
            if lineas[i].strip():
                if not tablas:
                    notas.append(lineas[i].strip())
                bloque.append(lineas[i].strip().strip(",").strip())
            else:
                bloque = []
            i += 1
            continue
        columnas = [c.strip() for c in celdas[1:]]
        titulo = " ".join(t for t in bloque if t)
        periodos, filas = [], []
        digitos = len(siguiente[0].strip())
        j = i + 1
        while j < len(lineas) and _es_fila_datos(celdas_por_linea[j]) \
                and len(celdas_por_linea[j]) == len(celdas):
            fila_celdas = celdas_por_linea[j]
            token = fila_celdas[0].strip()
            if len(token) != digitos:
                raise ErrorDatos(f"Linea {j + 1}: fecha {token!r} con longitud distinta dentro de la tabla")
            valores = []
            for c in fila_celdas[1:]:
                c = c.strip()
                if c == "":
                    valores.append(None)
                    continue
                try:
                    v = float(c)
                except ValueError as e:
                    raise ErrorDatos(f"Linea {j + 1}: valor no numerico {c!r}") from e
                valores.append(None if any(abs(v - f) < 1e-9 for f in FALTANTES_FRENCH) else v)
            periodos.append(token)
            filas.append(valores)
            j += 1
        tablas.append({"titulo": titulo, "columnas": columnas, "digitos": digitos,
                       "frecuencia": FRECUENCIA_POR_DIGITOS[digitos], "periodos": periodos,
                       "filas": filas, "linea": i + 1, "porcentaje": _es_porcentaje(titulo)})
        bloque = []
        i = j
    if not tablas:
        raise ErrorDatos("El CSV de French no contiene ninguna tabla reconocible")
    return {"notas": notas, "tablas": tablas}


def _version_crsp(notas: list[str]) -> str | None:
    for linea in notas:
        palabras = linea.replace(".", " ").split()
        for k, p in enumerate(palabras):
            if p.upper() == "CRSP" and k > 0 and palabras[k - 1].isdigit():
                return palabras[k - 1]
    return None


def _descargar_binario(url: str, timeout: float = TIMEOUT_ZIP_S,
                       reintentos: int = datos.REINTENTOS) -> bytes:
    ultimo: Exception | None = None
    for intento in range(reintentos):
        try:
            with urllib.request.urlopen(urllib.request.Request(url), timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            ultimo = e
            if e.code not in datos.CODIGOS_REINTENTABLES:
                break
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            ultimo = e
        if intento < reintentos - 1:
            time.sleep(datos.ESPERA_BASE_S * (2 ** intento))
    raise ErrorDatos(f"No se pudo descargar {url}: {ultimo!r}")


def _escritura_atomica(ruta: Path, contenido: bytes) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=ruta.parent, prefix=".tmp-")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(contenido)
        os.replace(tmp, ruta)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def french_zip(nombre_archivo: str, refrescar: bool = False, cache_horas: float | None = None,
               dir_cache: Path | str | None = None) -> tuple[bytes, Path]:
    """Bytes del zip (cache en datos/cache/french). cache_horas=None: el cache no caduca."""
    nombre = nombre_zip_french(nombre_archivo)
    ruta = Path(dir_cache) if dir_cache else DIR_CACHE_FRENCH
    ruta = ruta / nombre
    vigente = ruta.exists() and (cache_horas is None
                                 or (time.time() - ruta.stat().st_mtime) < cache_horas * 3600)
    if vigente and not refrescar:
        return ruta.read_bytes(), ruta
    contenido = _descargar_binario(URL_FRENCH + nombre)
    if not zipfile.is_zipfile(io.BytesIO(contenido)):
        raise ErrorDatos(f"French {nombre}: la respuesta no es un zip ({contenido[:60]!r})")
    _escritura_atomica(ruta, contenido)
    return contenido, ruta


def _texto_de_zip(contenido: bytes) -> tuple[str, str]:
    with zipfile.ZipFile(io.BytesIO(contenido)) as z:
        nombres = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if len(nombres) != 1:
            raise ErrorDatos(f"Se esperaba un CSV en el zip; hay {z.namelist()}")
        crudo = z.read(nombres[0])
    try:
        return crudo.decode("utf-8"), nombres[0]
    except UnicodeDecodeError:
        return crudo.decode("latin-1"), nombres[0]


def _elegir_tabla(tablas: list[dict], frecuencia: str, seccion: int | str | None) -> dict:
    if frecuencia not in DIGITOS_POR_FRECUENCIA:
        raise ValueError(f"frecuencia debe ser una de {sorted(DIGITOS_POR_FRECUENCIA)}")
    candidatas = [t for t in tablas if t["digitos"] == DIGITOS_POR_FRECUENCIA[frecuencia]]
    if isinstance(seccion, str):
        candidatas = [t for t in candidatas if seccion.lower() in t["titulo"].lower()]
    elif isinstance(seccion, int):
        candidatas = candidatas[seccion:seccion + 1]
    if not candidatas:
        disponibles = [(t["titulo"] or "(sin titulo)", t["frecuencia"]) for t in tablas]
        raise ErrorDatos(f"No hay tabla {frecuencia} (seccion={seccion!r}); disponibles: {disponibles}")
    return candidatas[0]


def tabla_french(texto: str, frecuencia: str = "mensual", seccion: int | str | None = None) -> dict:
    """Tabla elegida de un CSV ya descomprimido -> {'fechas', 'columnas', ...} (ver french)."""
    doc = parsear_french_csv(texto)
    t = _elegir_tabla(doc["tablas"], frecuencia, seccion)
    escala = 100.0 if t["porcentaje"] else 1.0
    columnas = {c: [] for c in t["columnas"]}
    for fila in t["filas"]:
        for c, v in zip(t["columnas"], fila):
            columnas[c].append(None if v is None else v / escala)
    fechas = [_fecha_french(p) for p in t["periodos"]]
    if any(b <= a for a, b in zip(fechas, fechas[1:])):
        raise ErrorDatos("Fechas French no estrictamente crecientes")
    return {
        "frecuencia": frecuencia,
        "titulo": t["titulo"],
        "fechas": fechas,
        "periodos": list(t["periodos"]),
        "columnas": columnas,
        "unidad": "decimal (porcentaje/100)" if t["porcentaje"] else "original (sin escalar)",
        "faltantes": sum(v is None for vs in columnas.values() for v in vs),
        "notas": doc["notas"],
        "version_crsp": _version_crsp(doc["notas"]),
        "tablas_en_archivo": [(x["titulo"] or "(principal)", x["frecuencia"], len(x["periodos"]))
                              for x in doc["tablas"]],
    }


def french(nombre_archivo: str, frecuencia: str = "mensual", seccion: int | str | None = None,
           refrescar: bool = False, cache_horas: float | None = None,
           dir_cache: Path | str | None = None) -> dict:
    """Descarga (o lee del cache) un archivo de la French Data Library y devuelve una tabla.

    nombre_archivo: p. ej. 'F-F_Research_Data_Factors', 'F-F_Research_Data_Factors_daily',
        'F-F_Momentum_Factor', 'F-F_Research_Data_5_Factors_2x3' (con o sin '_CSV.zip').
    frecuencia: 'mensual' (YYYYMM, fecha = fin de mes), 'diaria'/'semanal' (YYYYMMDD) o
        'anual' (YYYY, fecha = 31-dic). La tabla anual es la seccion 'Annual Factors'.
    seccion: None = primera tabla de esa frecuencia; int = indice entre esas tablas;
        str = subcadena del titulo (archivos de carteras con varias secciones).

    Devuelve dict con 'fechas' [date], 'columnas' {nombre: [decimal | None]}, 'titulo',
    'version_crsp', 'notas' (preambulo), 'sha256' y 'ruta_cache' del zip, 'url'.
    """
    contenido, ruta = french_zip(nombre_archivo, refrescar, cache_horas, dir_cache)
    texto, nombre_csv = _texto_de_zip(contenido)
    tabla = tabla_french(texto, frecuencia, seccion)
    tabla.update({
        "archivo": nombre_zip_french(nombre_archivo),
        "csv": nombre_csv,
        "url": URL_FRENCH + nombre_zip_french(nombre_archivo),
        "ruta_cache": str(ruta),
        "sha256": hashlib.sha256(contenido).hexdigest(),
        "fecha_cache_utc": datetime.fromtimestamp(ruta.stat().st_mtime, tz=timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%SZ"),
    })
    return tabla


def columna(tabla: dict, nombre: str, omitir_faltantes: bool = True) -> list[tuple[date, float]]:
    """[(fecha, valor)] de una columna de una tabla French."""
    if nombre not in tabla["columnas"]:
        raise KeyError(f"Columna {nombre!r} no existe; hay {list(tabla['columnas'])}")
    return [(f, v) for f, v in zip(tabla["fechas"], tabla["columnas"][nombre])
            if not (omitir_faltantes and v is None)]


def rendimiento_mercado_french(tabla: dict) -> list[tuple[date, float]]:
    """Rendimiento total del mercado = Mkt-RF + RF (aditivo, como lo construye French)."""
    mkt, rf = tabla["columnas"]["Mkt-RF"], tabla["columnas"]["RF"]
    return [(f, a + b) for f, a, b in zip(tabla["fechas"], mkt, rf) if a is not None and b is not None]


# ================================================================ Yahoo

def _fecha_local(ts: int, desfase: int) -> tuple[date, datetime]:
    """Fecha local de la bolsa. Barras a medianoche local (+-2 h por horario de verano) se
    redondean al dia mas cercano para que un cambio de desfase no las mueva de mes."""
    momento = datetime.fromtimestamp(ts + desfase, tz=timezone.utc).replace(tzinfo=None)
    dia = momento.date()
    if momento.hour >= 22:
        dia += timedelta(days=1)
    return dia, momento


def parsear_yahoo_historia(texto: str, intervalo: str = "1d",
                           solo_periodos_completos: bool = True) -> dict:
    """JSON de chart v8 -> historia con fechas, precios (adjclose si existe) y cierres.

    Mensual: fecha re-etiquetada a fin de mes calendario (la barra del dia 1 trae el cierre
    del ultimo dia de negociacion del mes). Varios puntos del mismo periodo (barra + punto
    en vivo): se conserva el ultimo. Periodo incompleto (mes/semana en curso, o sesion
    abierta en diario): se descarta si solo_periodos_completos, y se reporta en 'descartes'.
    """
    if intervalo not in INTERVALOS_YAHOO:
        raise ValueError(f"intervalo debe ser uno de {sorted(INTERVALOS_YAHOO)}")
    try:
        grafica = json.loads(texto)["chart"]
        if grafica.get("error"):
            raise ErrorDatos(f"Yahoo error: {grafica['error']}")
        res = grafica["result"][0]
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as e:
        raise ErrorDatos(f"JSON de Yahoo inesperado: {e!r}") from e
    meta = res.get("meta", {})
    granularidad = meta.get("dataGranularity")
    if granularidad and granularidad != intervalo:
        raise ErrorDatos(f"Yahoo devolvio granularidad {granularidad!r} en vez de {intervalo!r} "
                         "(con range=max la API degrada la granularidad; usar period1/period2)")
    tiempos = res.get("timestamp") or []
    ind = res.get("indicators", {})
    cierres = (ind.get("quote") or [{}])[0].get("close") or []
    ajustados = (ind.get("adjclose") or [{}])[0].get("adjclose") if ind.get("adjclose") else None
    desfase = int(meta.get("gmtoffset", 0))
    ref_ts = meta.get("regularMarketTime")
    ref_fecha = _fecha_local(int(ref_ts), desfase)[0] if ref_ts else date.today()

    por_periodo: dict = {}
    for i, ts in enumerate(tiempos):
        cierre = cierres[i] if i < len(cierres) else None
        ajustado = ajustados[i] if ajustados and i < len(ajustados) else None
        precio = ajustado if ajustado is not None else cierre
        if precio is None:
            continue
        dia, _ = _fecha_local(ts, desfase)
        if intervalo == "1mo":
            clave = (dia.year, dia.month)
        elif intervalo == "1wk":
            clave = dia - timedelta(days=dia.weekday())  # lunes de esa semana
        else:
            clave = dia
        por_periodo[clave] = (dia, float(precio), None if cierre is None else float(cierre),
                              ajustado is not None)

    descartes = []
    claves = sorted(por_periodo)
    if claves and solo_periodos_completos:
        ultima = claves[-1]
        incompleto = False
        if intervalo == "1mo":
            incompleto = (ref_fecha.year, ref_fecha.month) <= ultima
        elif intervalo == "1wk":
            incompleto = ref_fecha < ultima + timedelta(days=7)
        else:
            regular = (meta.get("currentTradingPeriod") or {}).get("regular") or {}
            if ref_ts and regular.get("start") and regular.get("end"):
                abierta = int(regular["start"]) <= int(ref_ts) < int(regular["end"])
                incompleto = abierta and ultima == _fecha_local(int(regular["start"]), desfase)[0]
        if incompleto:
            descartes.append(f"periodo incompleto {ultima} (referencia {ref_fecha})")
            claves = claves[:-1]

    fechas, precios, cierres_out = [], [], []
    usa_ajustado = False
    for clave in claves:
        dia, precio, cierre, es_aj = por_periodo[clave]
        if intervalo == "1mo":
            fechas.append(fin_de_mes(*clave))
        elif intervalo == "1wk":
            fechas.append(clave)
        else:
            fechas.append(dia)
        precios.append(precio)
        cierres_out.append(cierre)
        usa_ajustado = usa_ajustado or es_aj
    difiere = any(c is not None and abs(p - c) > 1e-9 * max(1.0, abs(c))
                  for p, c in zip(precios, cierres_out))
    return {
        "ticker": meta.get("symbol"),
        "intervalo": intervalo,
        "fechas": fechas,
        "precios": precios,
        "cierres": cierres_out,
        "usa_adjclose": usa_ajustado,
        "adjclose_difiere_de_close": difiere,
        "moneda": str(meta.get("currency", "")).upper(),
        "zona_horaria": meta.get("exchangeTimezoneName"),
        "etiqueta_fecha": {"1mo": "fin de mes calendario", "1wk": "lunes de la semana",
                           "1d": "dia de negociacion"}[intervalo],
        "fecha_referencia": ref_fecha,
        "descartes": descartes,
    }


def yahoo_historia(ticker: str, intervalo: str = "1d", solo_periodos_completos: bool = True,
                   cache_horas: float | None = 12) -> dict:
    """Historia completa de Yahoo (period1=1900, period2=2100; ver hallazgo 2 del modulo).

    Devuelve dict con 'fechas', 'precios' (adjclose si existe, si no close), 'cierres',
    'moneda', 'usa_adjclose', 'adjclose_difiere_de_close' (False en indices como ^GSPC:
    NO incluyen dividendos), 'descartes' y 'url'.
    """
    params = {"period1": YAHOO_PERIODO_1, "period2": YAHOO_PERIODO_2, "interval": intervalo,
              "events": "div,split"}
    url = datos.URL_YAHOO + urllib.parse.quote(ticker, safe="") + "?" + urllib.parse.urlencode(params)
    historia = parsear_yahoo_historia(datos.descargar(url, datos.UA_NAVEGADOR, cache_horas=cache_horas),
                                      intervalo, solo_periodos_completos)
    if not historia["fechas"]:
        raise ErrorDatos(f"Yahoo {ticker}: serie vacia")
    historia["url"] = url
    return historia


def rendimientos_de_precios(fechas: list, precios: list[float]) -> list[tuple]:
    """[(fecha_t, P_t / P_{t-1} - 1)] para t >= 1."""
    if len(fechas) != len(precios):
        raise ValueError("fechas y precios de distinta longitud")
    salida = []
    for i in range(1, len(precios)):
        if precios[i - 1] <= 0:
            raise ValueError(f"Precio no positivo en {fechas[i - 1]}")
        salida.append((fechas[i], precios[i] / precios[i - 1] - 1))
    return salida


# ================================================================ FRED / ALFRED

def fred(serie: str, desde: date | str | None = None,
         cache_horas: float | None = 12) -> list[tuple[date, float]]:
    """Ultima version de una serie de FRED: [(fecha_observacion, valor)].

    OJO: es la serie revisada de hoy. Para decisiones historicas de series revisables
    (PIB, empleo, inflacion) usa alfred(serie, fecha) y fechas de disponibilidad.
    """
    return datos.fred_serie(serie, desde=desde, cache_horas=cache_horas)


def alfred(serie: str, fecha_vintage: date | str,
           cache_horas: float | None = 24 * 365 * 100) -> list[tuple[date, float]]:
    """Serie tal como se conocia al cierre de fecha_vintage (vintage de ALFRED).

    Solo contiene observaciones publicadas hasta esa fecha: no hay look-ahead de revisiones
    ni de datos posteriores. Un vintage no cambia, por eso el cache por defecto no caduca.
    La fecha de cada tupla es la de OBSERVACION (p. ej. 2008-07-01 = 3T-2008), no la de
    publicacion: para una senal usa la fecha de vintage como fecha de disponibilidad.
    """
    fv = date.fromisoformat(str(fecha_vintage))
    url = URL_ALFRED + "?" + urllib.parse.urlencode({"id": serie, "vintage_date": fv.isoformat()})
    try:
        texto = datos.descargar(url, cache_horas=cache_horas)
    except ErrorDatos as e:
        if "404" in str(e):
            raise ErrorDatos(f"ALFRED {serie}: no existe vintage al {fv} (probablemente anterior a "
                             f"la primera publicacion en ALFRED)") from e
        raise
    valores = datos.parsear_fred_csv(texto)
    posteriores = [f for f, _ in valores if f > fv]
    if posteriores:
        raise ErrorDatos(f"ALFRED {serie}@{fv}: observaciones posteriores al vintage {posteriores[:3]}")
    if not valores:
        raise ErrorDatos(f"ALFRED {serie}@{fv}: serie vacia")
    return valores


def alfred_ultimo_conocido(serie: str, fecha: date | str) -> tuple[date, float]:
    """(fecha_observacion, valor) del dato mas reciente que se conocia en 'fecha'."""
    return alfred(serie, fecha)[-1]


# ================================================================ prueba en vivo

def _prueba_en_vivo() -> None:
    """python3 -m herramientas.datos_historicos: descarga y reporta rangos de fechas."""
    for nombre, frec in [("F-F_Research_Data_Factors", "mensual"),
                         ("F-F_Research_Data_Factors", "anual"),
                         ("F-F_Research_Data_Factors_daily", "diaria"),
                         ("F-F_Momentum_Factor", "mensual"),
                         ("F-F_Research_Data_5_Factors_2x3", "mensual")]:
        t = french(nombre, frec)
        print(f"French {nombre} [{frec}] CRSP {t['version_crsp']}: {t['fechas'][0]} a {t['fechas'][-1]}, "
              f"n={len(t['fechas'])}, columnas={list(t['columnas'])}, faltantes={t['faltantes']}, "
              f"sha256={t['sha256'][:12]}")
    for intervalo in ("1mo", "1d"):
        h = yahoo_historia("^GSPC", intervalo)
        print(f"Yahoo ^GSPC [{intervalo}]: {h['fechas'][0]} a {h['fechas'][-1]}, n={len(h['fechas'])}, "
              f"adjclose={h['usa_adjclose']}, adjclose!=close={h['adjclose_difiere_de_close']}, "
              f"descartes={h['descartes']}")
    fx = fred("DEXMXUS")
    print(f"FRED DEXMXUS: {fx[0][0]} a {fx[-1][0]}, n={len(fx)}")
    v = alfred("GDPC1", "2008-10-31")
    print(f"ALFRED GDPC1@2008-10-31: ultima observacion {v[-1][0]} = {v[-1][1]}")


if __name__ == "__main__":
    _prueba_en_vivo()
