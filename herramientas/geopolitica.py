"""Monitor geopolitico en markdown: indice GPR de Caldara-Iacoviello, mercados de prediccion
(Polymarket y Kalshi) filtrados por palabras clave, y fuentes primarias para revisar.

Uso:
    python3 herramientas/geopolitica.py [--palabras "Fed,recession,tariff,Taiwan"] [--salida ruta.md]
        [--max-por-palabra 6] [--volumen-min 10000] [--paises MEX,USA,CHN] [--cache-horas 6]
        [--sin-gpr] [--sin-polymarket] [--sin-kalshi] [--json]

Si una fuente falla, lo anota en "Estado de las fuentes" y sigue.

GPR (https://www.matteoiacoviello.com/gpr.htm): verificado el 2026-09-25, el sitio NO publica CSV
(data_gpr_export.csv responde 404); publica .xls (BIFF8/OLE2, no legible con la biblioteca estandar)
y .dta de Stata (formato abierto, documentado). Se intenta CSV primero por si aparece; luego se lee el
.dta con un lector propio (versiones 117-119). El .xls se omite con aviso.

Polymarket: gamma-api /public-search (busqueda por texto, eventos activos); respaldo /markets ordenado
por volumen con filtro local. Kalshi: API oficial trade-api v2 (/series por categoria con volumen ->
/events?series_ticker=...&status=open&with_nested_markets=true); respaldo: /v1/search/series (endpoint
que usa la web de Kalshi, no documentado). Precio de un contrato binario ~ probabilidad implicita.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import statistics
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from herramientas.parametros import DIR_CACHE

AGENTE = "Mozilla/5.0"
TIMEOUT_S = 30
REINTENTOS = 3
PAUSA_S = 0.25

URL_GPR_PAGINA = "https://www.matteoiacoviello.com/gpr.htm"
URL_GPR_BASE = "https://www.matteoiacoviello.com/gpr_files/"
ARCHIVOS_GPR = {"mensual": "data_gpr_export", "diario": "data_gpr_daily_recent"}

URL_POLY = "https://gamma-api.polymarket.com"
URL_POLY_EVENTO = "https://polymarket.com/event/{slug}"
URLS_KALSHI = ["https://api.elections.kalshi.com/trade-api/v2", "https://external-api.kalshi.com/trade-api/v2"]
URL_KALSHI_BUSQUEDA = "https://api.elections.kalshi.com/v1/search/series"

PALABRAS_DEFECTO = ["Fed", "recession", "tariff", "Taiwan", "China", "Iran", "Russia", "Ukraine",
                    "Mexico", "oil", "election"]
EXCLUSIONES = {"mexico": ["new mexico"], "oil": ["oilers"], "china": ["china open"]}
ETIQUETAS_RUIDO_POLY = {"weather", "sports", "parlays", "daily temperature", "esports", "games", "soccer",
                        "basketball", "football", "tennis", "mentions", "nba", "nfl", "mlb", "nhl"}
CATEGORIAS_KALSHI = ["Economics", "Politics", "World", "Financials", "Commodities", "Elections"]
PAISES_DEFECTO = ["MEX", "USA", "CHN", "TWN", "RUS", "UKR", "ISR", "SAU", "KOR", "JPN", "DEU", "IND", "VEN", "TUR"]

FUENTES_PRIMARIAS = [
    ("Mexico", "Banxico: anuncios de politica monetaria y calendario", "https://www.banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/anuncios-politica-monetaria-t.html"),
    ("Mexico", "Diario Oficial de la Federacion (decretos, aranceles, regulacion)", "https://www.dof.gob.mx/"),
    ("Mexico", "SHCP (finanzas publicas, deuda, Paquete Economico)", "https://www.gob.mx/shcp"),
    ("Mexico", "Secretaria de Economia (comercio, T-MEC, aranceles)", "https://www.gob.mx/se"),
    ("Mexico", "INEGI (inflacion, PIB, empleo)", "https://www.inegi.org.mx/"),
    ("EUA", "Federal Reserve: comunicados FOMC y calendario", "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"),
    ("EUA", "Casa Blanca: acciones presidenciales (ordenes ejecutivas, proclamaciones arancelarias)", "https://www.whitehouse.gov/presidential-actions/"),
    ("EUA", "Federal Register (aranceles, controles, sanciones publicadas)", "https://www.federalregister.gov/"),
    ("EUA", "USTR (Seccion 301, T-MEC, negociaciones)", "https://ustr.gov/about-us/policy-offices/press-office/press-releases"),
    ("EUA", "Commerce BIS (controles de exportacion, Entity List)", "https://www.bis.gov/news-updates"),
    ("EUA", "Tesoro OFAC (sanciones: acciones recientes)", "https://ofac.treasury.gov/recent-actions"),
    ("EUA", "EIA (inventarios y precios de petroleo)", "https://www.eia.gov/petroleum/supply/weekly/"),
    ("China", "MOFCOM (comercio, controles de exportacion de China)", "https://english.mofcom.gov.cn/"),
    ("China/Taiwan", "Ministerio de Defensa de Taiwan (actividad militar del EPL)", "https://www.mnd.gov.tw/"),
    ("Europa", "Comision Europea: comercio y sanciones", "https://policy.trade.ec.europa.eu/news_en"),
    ("Energia", "OPEP: comunicados de reuniones", "https://www.opec.org/opec_web/en/press_room/28.htm"),
    ("Conflictos", "ISW (Rusia-Ucrania, Medio Oriente)", "https://understandingwar.org/"),
    ("Conflictos", "IAEA (programa nuclear de Iran)", "https://www.iaea.org/newscenter/pressreleases"),
    ("Conflictos", "ACLED (eventos de conflicto con datos)", "https://acleddata.com/"),
    ("Global", "FMI (WEO, consultas por pais)", "https://www.imf.org/en/News"),
]


class ErrorFuente(Exception):
    """Fallo de una fuente externa."""


# ---------------------------------------------------------------- transporte

def _get(url: str, aceptar: str = "application/json", cache_nombre: str | None = None,
         cache_horas: float | None = None, reintentos: int = REINTENTOS) -> bytes:
    """GET con User-Agent de navegador, reintentos (429/5xx) y cache opcional en datos/cache."""
    if cache_nombre and cache_horas:
        ruta = DIR_CACHE / cache_nombre
        if ruta.exists() and (time.time() - ruta.stat().st_mtime) < cache_horas * 3600:
            return ruta.read_bytes()
    ultimo: Exception | None = None
    for intento in range(reintentos):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": AGENTE, "Accept": aceptar})
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
                cuerpo = resp.read()
            if cache_nombre and cache_horas:
                try:
                    DIR_CACHE.mkdir(parents=True, exist_ok=True)
                    (DIR_CACHE / cache_nombre).write_bytes(cuerpo)
                except OSError:
                    pass
            return cuerpo
        except urllib.error.HTTPError as e:
            ultimo = e
            if e.code not in (429, 500, 502, 503, 504):
                raise ErrorFuente(f"HTTP {e.code} en {url}") from e
            espera = float(e.headers.get("Retry-After") or 0) if e.headers else 0
            time.sleep(max(espera, 1.5 * (intento + 1)))
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            ultimo = e
            time.sleep(1.0 * (intento + 1))
    raise ErrorFuente(f"No se pudo descargar {url}: {ultimo!r}")


def _get_json(url: str, **kw):
    try:
        return json.loads(_get(url, **kw).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ErrorFuente(f"JSON invalido de {url}: {e!r}") from e


# ---------------------------------------------------------------- lector Stata .dta (117-119)

_FALTANTE = {"b": 100, "h": 32740, "l": 2147483620, "f": 1.7014117331926443e38, "d": 8.98846567431158e307}


def leer_dta(contenido: bytes) -> dict:
    """Lee un .dta de Stata 13+ (release 117, 118 o 119).

    Devuelve {'version', 'variables': [nombres], 'etiquetas': {var: etiqueta}, 'formatos': {var: fmt},
    'filas': [dict]}. Valores faltantes de Stata -> None; strL -> None (no se leen).
    """
    if not contenido.startswith(b"<stata_dta><header><release>"):
        raise ErrorFuente("No es un .dta de Stata 13+ (se esperaba <stata_dta>)")
    version = int(contenido[28:31])
    if version not in (117, 118, 119):
        raise ErrorFuente(f"Version de .dta no soportada: {version}")

    def seccion(etiqueta: bytes) -> int:
        i = contenido.find(b"<" + etiqueta + b">")
        if i < 0:
            raise ErrorFuente(f"Seccion {etiqueta!r} ausente en .dta")
        return i + len(etiqueta) + 2

    i = seccion(b"byteorder")
    orden = "<" if contenido[i:i + 3] == b"LSF" else ">"
    i = seccion(b"K")
    k = struct.unpack(orden + ("I" if version == 119 else "H"), contenido[i:i + (4 if version == 119 else 2)])[0]
    i = seccion(b"N")
    n = struct.unpack(orden + ("I" if version == 117 else "Q"), contenido[i:i + (4 if version == 117 else 8)])[0]
    i = seccion(b"variable_types")
    tipos = struct.unpack(orden + f"{k}H", contenido[i:i + 2 * k])
    largo_nombre = 33 if version == 117 else 129
    largo_formato = 49 if version == 117 else 57
    largo_etiqueta = 81 if version == 117 else 321

    def cadenas(etiqueta: bytes, largo: int) -> list[str]:
        j = seccion(etiqueta)
        return [contenido[j + t * largo:j + (t + 1) * largo].split(b"\0")[0].decode("utf-8", "replace")
                for t in range(k)]

    nombres = cadenas(b"varnames", largo_nombre)
    formatos = cadenas(b"formats", largo_formato)
    etiquetas = cadenas(b"variable_labels", largo_etiqueta)
    especificacion = []
    for t in tipos:
        if 1 <= t <= 2045:
            especificacion.append(("s", t))
        elif t == 32768:
            especificacion.append(("L", 8))
        elif t == 65526:
            especificacion.append(("d", 8))
        elif t == 65527:
            especificacion.append(("f", 4))
        elif t == 65528:
            especificacion.append(("l", 4))
        elif t == 65529:
            especificacion.append(("h", 2))
        elif t == 65530:
            especificacion.append(("b", 1))
        else:
            raise ErrorFuente(f"Tipo de variable .dta desconocido: {t}")
    ancho = sum(a for _, a in especificacion)
    i = seccion(b"data")
    if i + ancho * n > len(contenido):
        raise ErrorFuente("Archivo .dta truncado")
    filas = []
    for r in range(n):
        base = i + r * ancho
        fila, pos = {}, base
        for nombre, (cod, largo) in zip(nombres, especificacion):
            crudo = contenido[pos:pos + largo]
            pos += largo
            if cod == "s":
                fila[nombre] = crudo.split(b"\0")[0].decode("utf-8", "replace").strip()
            elif cod == "L":
                fila[nombre] = None
            else:
                valor = struct.unpack(orden + cod, crudo)[0]
                fila[nombre] = None if valor > _FALTANTE[cod] else valor
        filas.append(fila)
    return {"version": version, "variables": nombres, "etiquetas": dict(zip(nombres, etiquetas)),
            "formatos": dict(zip(nombres, formatos)), "filas": filas}


def fecha_stata(valor, formato: str) -> date | None:
    """Convierte fechas de Stata: %td (dias desde 1960-01-01) y %tm (meses desde 1960m1)."""
    if valor is None:
        return None
    base = date(1960, 1, 1)
    f = formato.lower()
    if f.startswith("%td") or f.startswith("%d"):
        return base + timedelta(days=int(valor))
    if f.startswith("%tm"):
        m = int(valor)
        return date(1960 + m // 12, m % 12 + 1, 1)
    return None


# ---------------------------------------------------------------- GPR

def _percentil(valores: list[float], x: float) -> float:
    return 100.0 * sum(1 for v in valores if v <= x) / len(valores) if valores else float("nan")


def parsear_gpr_csv(texto: str) -> list[dict]:
    """CSV de GPR (si algun dia se publica) -> filas dict con numeros convertidos."""
    filas = []
    for fila in csv.DictReader(io.StringIO(texto)):
        limpia = {}
        for k, v in fila.items():
            try:
                limpia[k] = float(v) if v not in ("", None) else None
            except ValueError:
                limpia[k] = v
        filas.append(limpia)
    return filas


def serie_mensual_gpr(dta: dict) -> list[dict]:
    """Filas mensuales con 'fecha' (date) y las columnas numericas."""
    fmt = dta["formatos"].get("month", "%tm")
    salida = []
    for f in dta["filas"]:
        fecha = fecha_stata(f.get("month"), fmt)
        if fecha:
            salida.append({**f, "fecha": fecha})
    return sorted(salida, key=lambda f: f["fecha"])


def serie_diaria_gpr(dta: dict) -> list[dict]:
    fmt = dta["formatos"].get("date", "%td")
    salida = []
    for f in dta["filas"]:
        fecha = fecha_stata(f.get("date"), fmt)
        if fecha is None and f.get("DAY"):
            try:
                fecha = datetime.strptime(str(f["DAY"]), "%Y%m%d").date()
            except ValueError:
                fecha = None
        if fecha:
            salida.append({**f, "fecha": fecha})
    return sorted(salida, key=lambda f: f["fecha"])


def resumen_gpr_mensual(filas: list[dict], paises: list[str], etiquetas: dict | None = None) -> dict:
    """Ultimo mes con GPR, promedios, percentil historico y paises."""
    validas = [f for f in filas if f.get("GPR") is not None]
    if not validas:
        raise ErrorFuente("GPR mensual sin datos")
    ultimo = validas[-1]
    historia = [f["GPR"] for f in validas if f["fecha"].year >= 1985]
    res = {"fecha": ultimo["fecha"], "series": {}, "paises": []}
    for clave in ("GPR", "GPRT", "GPRA"):
        valores = [f.get(clave) for f in validas if f.get(clave) is not None and f["fecha"].year >= 1985]
        if not valores:
            continue
        actual = ultimo.get(clave)
        res["series"][clave] = {
            "ultimo": actual,
            "prom_3m": statistics.fmean(valores[-3:]),
            "prom_12m": statistics.fmean(valores[-12:]),
            "percentil": _percentil(valores, actual) if actual is not None else None,
            "hace_12m": valores[-13] if len(valores) >= 13 else None,
        }
    for pais in paises:
        col = f"GPRC_{pais}"
        valores = [(f["fecha"], f.get(col)) for f in validas if f.get(col) is not None and f["fecha"].year >= 1985]
        if not valores:
            continue
        actual = valores[-1][1]
        historia_pais = [v for _, v in valores]
        res["paises"].append({
            "pais": pais,
            "nombre": (etiquetas or {}).get(col, col),
            "fecha": valores[-1][0],
            "ultimo": actual,
            "prom_12m": statistics.fmean(historia_pais[-12:]),
            "percentil": _percentil(historia_pais, actual),
        })
    res["percentil_nota"] = f"percentil respecto a {len(historia)} meses desde 1985"
    return res


def resumen_gpr_diario(filas: list[dict], ventana_eventos: int = 90) -> dict:
    validas = [f for f in filas if f.get("GPRD") is not None]
    if not validas:
        raise ErrorFuente("GPR diario sin datos")
    ultimo = validas[-1]
    cinco = [f for f in validas if f["fecha"] >= ultimo["fecha"] - timedelta(days=5 * 365)]
    ma30 = [f.get("GPRD_MA30") for f in cinco if f.get("GPRD_MA30") is not None]
    corte = ultimo["fecha"] - timedelta(days=ventana_eventos)
    recientes = [f for f in validas if f["fecha"] >= corte]
    picos = sorted(recientes, key=lambda f: -f["GPRD"])[:5]
    return {
        "fecha": ultimo["fecha"],
        "gprd": ultimo["GPRD"],
        "ma7": ultimo.get("GPRD_MA7"),
        "ma30": ultimo.get("GPRD_MA30"),
        "percentil_ma30_5a": _percentil(ma30, ultimo["GPRD_MA30"]) if ma30 and ultimo.get("GPRD_MA30") else None,
        "picos": [{"fecha": f["fecha"], "gprd": f["GPRD"], "evento": f.get("event") or ""} for f in picos],
        "eventos_anotados": [{"fecha": f["fecha"], "gprd": f["GPRD"], "evento": f["event"]}
                             for f in recientes if f.get("event")][-8:],
    }


def descargar_gpr(cache_horas: float | None, registro: list[str]) -> dict:
    """Intenta CSV, luego .dta. Devuelve {'mensual': dta|filas, 'diario': ...}; anota cada intento."""
    salida = {}
    for clave, base in ARCHIVOS_GPR.items():
        try:
            texto = _get(URL_GPR_BASE + base + ".csv", aceptar="text/csv", reintentos=1).decode("utf-8", "replace")
            if texto.lstrip().startswith("<"):
                raise ErrorFuente("respuesta HTML")
            salida[clave] = {"formato": "csv", "filas": parsear_gpr_csv(texto)}
            registro.append(f"GPR {clave}: CSV encontrado ({base}.csv)")
            continue
        except ErrorFuente as e:
            registro.append(f"GPR {clave}: sin CSV ({base}.csv: {e}); .xls omitido (BIFF8 no legible con stdlib); se usa .dta")
        try:
            contenido = _get(URL_GPR_BASE + base + ".dta", aceptar="application/octet-stream",
                             cache_nombre=f"gpr_{base}.dta", cache_horas=cache_horas)
            salida[clave] = {"formato": "dta", **leer_dta(contenido)}
        except ErrorFuente as e:
            registro.append(f"GPR {clave}: fallo .dta: {e}")
    return salida


# ---------------------------------------------------------------- palabras clave

def patron_palabra(palabra: str) -> re.Pattern:
    """Coincidencia de palabra completa, sin distinguir mayusculas; admite plural y posesivo."""
    return re.compile(r"(?<![A-Za-z])" + re.escape(palabra) + r"(?:s|es|'s)?(?![A-Za-z])", re.IGNORECASE)


def coincide(texto: str, palabra: str) -> bool:
    if not texto:
        return False
    limpio = texto
    for excl in EXCLUSIONES.get(palabra.lower(), []):
        limpio = re.sub(re.escape(excl), " ", limpio, flags=re.IGNORECASE)
    return bool(patron_palabra(palabra).search(limpio))


def _float(x) -> float | None:
    try:
        return float(x) if x not in (None, "") else None
    except (TypeError, ValueError):
        return None


def probabilidad_implicita(compra: float | None, venta: float | None, ultimo: float | None,
                           diferencial_max: float = 0.10) -> float | None:
    """Punto medio si el diferencial es razonable; si no, ultimo precio negociado."""
    if compra is not None and venta is not None and venta > 0 and 0 <= venta - compra <= diferencial_max:
        return (compra + venta) / 2
    return ultimo


# ---------------------------------------------------------------- Polymarket

def _lista_json(x) -> list:
    if isinstance(x, list):
        return x
    try:
        valor = json.loads(x or "[]")
        return valor if isinstance(valor, list) else []
    except (TypeError, json.JSONDecodeError):
        return []


def mercado_polymarket(m: dict, evento: dict | None = None) -> dict | None:
    """Normaliza un mercado de gamma-api; None si esta cerrado o sin precio."""
    if m.get("closed") or m.get("archived") or m.get("active") is False:
        return None
    resultados = _lista_json(m.get("outcomes"))
    precios = [_float(p) for p in _lista_json(m.get("outcomePrices"))]
    if not precios or precios[0] is None:
        return None
    etiqueta = resultados[0] if resultados else "Si"
    prob = precios[0]
    compra, venta = _float(m.get("bestBid")), _float(m.get("bestAsk"))
    evento = evento or ((m.get("events") or [None])[0]) or {}
    pregunta = m.get("question") or evento.get("title") or ""
    return {
        "fuente": "Polymarket",
        "id": str(m.get("id") or m.get("conditionId") or pregunta),
        "evento": evento.get("title") or pregunta,
        "pregunta": pregunta,
        "resultado": etiqueta,
        "probabilidad": prob,
        "compra": compra,
        "venta": venta,
        "ultimo": _float(m.get("lastTradePrice")),
        "cambio_1s": _float(m.get("oneWeekPriceChange")),
        "volumen": _float(m.get("volumeNum")) or _float(m.get("volume")) or 0.0,
        "volumen_24h": _float(m.get("volume24hr")),
        "cierre": (m.get("endDate") or evento.get("endDate") or "")[:10],
        "url": URL_POLY_EVENTO.format(slug=evento.get("slug") or m.get("slug") or ""),
        "etiquetas": [str(t.get("label", "")).lower() for t in (evento.get("tags") or []) if isinstance(t, dict)],
    }


def polymarket_desde_busqueda(datos: dict, palabra: str) -> list[dict]:
    """Respuesta de /public-search -> mercados abiertos relevantes para la palabra."""
    salida = []
    for evento in datos.get("events") or []:
        etiquetas = {str(t.get("label", "")).lower() for t in (evento.get("tags") or []) if isinstance(t, dict)}
        if etiquetas & ETIQUETAS_RUIDO_POLY or evento.get("closed"):
            continue
        for m in evento.get("markets") or []:
            norm = mercado_polymarket(m, evento)
            if norm and (coincide(norm["evento"], palabra) or coincide(norm["pregunta"], palabra)):
                salida.append(norm)
    return salida


def polymarket(palabras: list[str], max_por_palabra: int, volumen_min: float, cache_horas: float | None,
               registro: list[str]) -> dict[str, list[dict]]:
    resultados: dict[str, list[dict]] = {}
    respaldo: list[dict] | None = None
    for palabra in palabras:
        url = URL_POLY + "/public-search?" + urllib.parse.urlencode(
            {"q": palabra, "events_status": "active", "limit_per_type": 25, "keep_closed_markets": 0})
        try:
            datos = _get_json(url, cache_nombre=f"poly_busqueda_{palabra.lower()}.json", cache_horas=cache_horas)
            mercados = polymarket_desde_busqueda(datos, palabra)
        except ErrorFuente as e:
            registro.append(f"Polymarket busqueda '{palabra}': {e}; se usa /markets por volumen")
            if respaldo is None:
                try:
                    lista = _get_json(URL_POLY + "/markets?" + urllib.parse.urlencode(
                        {"active": "true", "closed": "false", "order": "volumeNum", "ascending": "false",
                         "limit": 500}), cache_nombre="poly_markets_volumen.json", cache_horas=cache_horas)
                    respaldo = [x for x in (mercado_polymarket(m) for m in lista) if x]
                except ErrorFuente as e2:
                    registro.append(f"Polymarket /markets: {e2}")
                    respaldo = []
            mercados = [m for m in respaldo if coincide(m["pregunta"], palabra) or coincide(m["evento"], palabra)]
        vistos, unicos = set(), []
        for m in sorted(mercados, key=lambda x: -(x["volumen"] or 0)):
            if m["id"] in vistos or (m["volumen"] or 0) < volumen_min:
                continue
            vistos.add(m["id"])
            unicos.append(m)
        resultados[palabra] = unicos[:max_por_palabra]
        time.sleep(PAUSA_S)
    return resultados


# ---------------------------------------------------------------- Kalshi

def mercado_kalshi(m: dict, evento: dict) -> dict | None:
    """Normaliza un mercado de trade-api v2; None si no esta activo."""
    if m.get("status") not in ("active", "open", None):
        return None
    compra, venta = _float(m.get("yes_bid_dollars")), _float(m.get("yes_ask_dollars"))
    ultimo = _float(m.get("last_price_dollars"))
    if compra is None and venta is None and ultimo is None:      # campos en centavos (API anterior)
        centavos = [_float(m.get(c)) for c in ("yes_bid", "yes_ask", "last_price")]
        compra, venta, ultimo = (None if c is None else c / 100 for c in centavos)
    prob = probabilidad_implicita(compra, venta, ultimo)
    if prob is None:
        return None
    subtitulo = m.get("yes_sub_title") or m.get("subtitle") or ""
    return {
        "fuente": "Kalshi",
        "id": m.get("ticker", ""),
        "evento": evento.get("title", ""),
        "pregunta": f"{evento.get('title', '')} - {subtitulo}".strip(" -"),
        "resultado": subtitulo or "Si",
        "probabilidad": prob,
        "compra": compra,
        "venta": venta,
        "ultimo": ultimo,
        "cambio_1s": None,
        "volumen": _float(m.get("volume_fp")) or _float(m.get("volume")) or 0.0,
        "volumen_24h": _float(m.get("volume_24h_fp")) or _float(m.get("volume_24h")),
        "interes_abierto": _float(m.get("open_interest_fp")) or _float(m.get("open_interest")),
        "cierre": (m.get("close_time") or "")[:10],
        "url": f"serie {evento.get('series_ticker', '')} / mercado {m.get('ticker', '')}",
    }


def series_relevantes(series: list[dict], palabra: str, maximo: int) -> list[dict]:
    """Series cuyo titulo o etiquetas coinciden, sin duplicados, ordenadas por volumen historico."""
    vistas, salida = set(), []
    for s in series:
        textos = [s.get("title", "")] + list(s.get("tags") or [])
        if s.get("ticker") in vistas or not any(coincide(t, palabra) for t in textos):
            continue
        vistas.add(s.get("ticker"))
        salida.append(s)
    salida.sort(key=lambda s: -(_float(s.get("volume_fp")) or _float(s.get("volume")) or 0))
    return salida[:maximo]


def kalshi_desde_eventos(datos: dict, max_eventos: int = 3, max_mercados: int = 6) -> list[dict]:
    """Respuesta de /events con mercados anidados -> mercados normalizados (eventos que cierran antes primero)."""
    eventos = datos.get("events") or []
    salida = []
    def cierre_evento(e):
        cierres = [m.get("close_time") or "9999" for m in e.get("markets") or []]
        return min(cierres) if cierres else "9999"
    for evento in sorted(eventos, key=cierre_evento)[:max_eventos]:
        mercados = [x for x in (mercado_kalshi(m, evento) for m in evento.get("markets") or []) if x]
        mercados.sort(key=lambda x: -(x["volumen"] or 0))
        salida += mercados[:max_mercados]
    return salida


def kalshi_desde_busqueda_v1(datos: dict, palabra: str, ahora: datetime) -> list[dict]:
    """Respuesta de /v1/search/series (no documentado) -> mercados abiertos."""
    salida = []
    for s in datos.get("current_page") or []:
        titulo = s.get("event_title") or s.get("series_title") or ""
        if str(s.get("category", "")).lower() in ("sports", "entertainment"):
            continue
        if not (coincide(titulo, palabra) or coincide(s.get("series_title", ""), palabra)):
            continue
        for m in s.get("markets") or []:
            cierre = m.get("close_ts") or ""
            if m.get("result") or not cierre or cierre[:19] < ahora.strftime("%Y-%m-%dT%H:%M:%S"):
                continue
            compra, venta = _float(m.get("yes_bid_dollars")), _float(m.get("yes_ask_dollars"))
            ultimo = _float(m.get("last_price_dollars"))
            prob = probabilidad_implicita(compra, venta, ultimo)
            if prob is None:
                continue
            salida.append({
                "fuente": "Kalshi", "id": m.get("ticker", ""), "evento": titulo,
                "pregunta": f"{titulo} - {m.get('yes_subtitle', '')}".strip(" -"),
                "resultado": m.get("yes_subtitle") or "Si", "probabilidad": prob, "compra": compra,
                "venta": venta, "ultimo": ultimo, "cambio_1s": None, "volumen": _float(m.get("volume")) or 0.0,
                "volumen_24h": None, "interes_abierto": None, "cierre": cierre[:10],
                "url": f"serie {s.get('series_ticker', '')} / mercado {m.get('ticker', '')}",
            })
    return salida


def kalshi(palabras: list[str], max_por_palabra: int, volumen_min: float, cache_horas: float | None,
           registro: list[str], series_por_palabra: int = 4) -> dict[str, list[dict]]:
    series, base_ok = [], None
    for base in URLS_KALSHI:
        series = []
        try:
            for cat in CATEGORIAS_KALSHI:
                datos = _get_json(f"{base}/series?" + urllib.parse.urlencode({"category": cat, "include_volume": "true"}),
                                  cache_nombre=f"kalshi_series_{cat.lower()}.json", cache_horas=cache_horas)
                series += datos.get("series") or []
                time.sleep(PAUSA_S)
            base_ok = base
            break
        except ErrorFuente as e:
            registro.append(f"Kalshi {base}/series: {e}")
    resultados: dict[str, list[dict]] = {}
    ahora = datetime.now(timezone.utc)
    for palabra in palabras:
        mercados: list[dict] = []
        if base_ok:
            for s in series_relevantes(series, palabra, series_por_palabra):
                try:
                    datos = _get_json(f"{base_ok}/events?" + urllib.parse.urlencode(
                        {"series_ticker": s["ticker"], "status": "open", "with_nested_markets": "true", "limit": 25}),
                        cache_nombre=f"kalshi_eventos_{s['ticker']}.json", cache_horas=cache_horas)
                    for m in kalshi_desde_eventos(datos):
                        m["serie"] = s.get("title", "")
                        mercados.append(m)
                except ErrorFuente as e:
                    registro.append(f"Kalshi eventos {s.get('ticker')}: {e}")
                time.sleep(PAUSA_S)
        if not mercados:
            try:
                datos = _get_json(URL_KALSHI_BUSQUEDA + "?" + urllib.parse.urlencode(
                    {"query": palabra, "order_by": "querymatch", "page_size": 10}),
                    cache_nombre=f"kalshi_busqueda_{palabra.lower()}.json", cache_horas=cache_horas)
                mercados = kalshi_desde_busqueda_v1(datos, palabra, ahora)
                if mercados:
                    registro.append(f"Kalshi '{palabra}': sin series oficiales abiertas; se uso /v1/search (no documentado)")
                time.sleep(PAUSA_S)
            except ErrorFuente as e:
                registro.append(f"Kalshi busqueda v1 '{palabra}': {e}")
        vistos, unicos = set(), []
        for m in sorted(mercados, key=lambda x: -(x["volumen"] or 0)):
            if m["id"] in vistos or (m["volumen"] or 0) < volumen_min:
                continue
            vistos.add(m["id"])
            unicos.append(m)
        resultados[palabra] = unicos[:max_por_palabra]
    return resultados


# ---------------------------------------------------------------- markdown

def _pct(x) -> str:
    return "n.d." if x is None else f"{x * 100:.1f}%"


def _n(x, d=1) -> str:
    return "n.d." if x is None else f"{x:,.{d}f}"


def _vol(x) -> str:
    if x is None:
        return "n.d."
    if x >= 1e6:
        return f"{x / 1e6:,.1f} M"
    if x >= 1e3:
        return f"{x / 1e3:,.0f} mil"
    return f"{x:,.0f}"


def tabla_mercados(mercados: list[dict], con_url: bool = True) -> list[str]:
    lineas = ["| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |",
              "|---|---|---|---|---|---|---|"]
    for m in mercados:
        pregunta = m["pregunta"].replace("|", "/")[:110]
        cv = f"{_n(m.get('compra'), 2)}/{_n(m.get('venta'), 2)}"
        enlace = f"[ver]({m['url']})" if con_url and m["url"].startswith("http") else m["url"]
        lineas.append(f"| {pregunta} | {str(m['resultado'])[:40]} | {_pct(m['probabilidad'])} | {cv} | "
                      f"{_vol(m.get('volumen'))} | {m.get('cierre') or 'n.d.'} | {enlace} |")
    return lineas


def construir_markdown(fecha: date, gpr: dict | None, poly: dict | None, kal: dict | None,
                       registro: list[str], palabras: list[str]) -> str:
    l = [f"# Monitor geopolitico {fecha.isoformat()}", "",
         "> Generado por herramientas/geopolitica.py. Hechos con fecha y fuente; la lectura es del analista. "
         "Un precio de mercado de prediccion es una probabilidad implicita neutral al riesgo, no una verdad: "
         "revisar liquidez, diferencial compra/venta y criterio de resolucion antes de usarlo.", "",
         f"Palabras clave: {', '.join(palabras)}", ""]
    l += ["## 1. Indice de riesgo geopolitico (Caldara e Iacoviello)", "",
          f"Fuente: {URL_GPR_PAGINA} (conteo de articulos de prensa sobre tensiones, amenazas y actos "
          "geopoliticos; base 1985-2019 = 100). Mensual y diario.", ""]
    if gpr and gpr.get("mensual"):
        m = gpr["mensual"]
        l += [f"Ultimo mes: {m['fecha'].strftime('%Y-%m')} ({m['percentil_nota']}).", "",
              "| Serie | Ultimo | Prom. 3m | Prom. 12m | Hace 12m | Percentil historico |", "|---|---|---|---|---|---|"]
        nombres = {"GPR": "GPR total", "GPRT": "Amenazas (GPRT)", "GPRA": "Actos (GPRA)"}
        for clave, s in m["series"].items():
            l.append(f"| {nombres.get(clave, clave)} | {_n(s['ultimo'])} | {_n(s['prom_3m'])} | {_n(s['prom_12m'])} | "
                     f"{_n(s['hace_12m'])} | {_n(s['percentil'], 0)} |")
        if m["paises"]:
            l += ["", "Por pais (porcentaje de articulos que mencionan riesgo geopolitico y al pais; percentil "
                  "contra su propia historia desde 1985):", "",
                  "| Pais | Mes | Ultimo | Prom. 12m | Percentil |", "|---|---|---|---|---|"]
            for p in sorted(m["paises"], key=lambda x: -x["percentil"]):
                l.append(f"| {p['pais']} | {p['fecha'].strftime('%Y-%m')} | {_n(p['ultimo'], 2)} | {_n(p['prom_12m'], 2)} | "
                         f"{_n(p['percentil'], 0)} |")
        l.append("")
    if gpr and gpr.get("diario"):
        d = gpr["diario"]
        l += [f"Diario al {d['fecha']}: GPRD {_n(d['gprd'])}, media 7 dias {_n(d['ma7'])}, media 30 dias {_n(d['ma30'])} "
              f"(percentil 5 anios de la media 30d: {_n(d['percentil_ma30_5a'], 0)}).", "",
              "Picos de los ultimos 90 dias:", "", "| Fecha | GPRD | Evento anotado por los autores |", "|---|---|---|"]
        for p in d["picos"]:
            l.append(f"| {p['fecha']} | {_n(p['gprd'])} | {p['evento'] or ''} |")
        if d["eventos_anotados"]:
            l += ["", "Eventos anotados recientes: " + "; ".join(f"{e['fecha']} {e['evento']}" for e in d["eventos_anotados"])]
        l.append("")
    if not gpr or (not gpr.get("mensual") and not gpr.get("diario")):
        l += ["GPR no disponible en esta corrida (ver estado de las fuentes).", ""]
    l += ["Lectura: GPR alto predice menor inversion y empleo y mayor riesgo a la baja en acciones (Caldara e "
          "Iacoviello, AER 2022); el componente de amenazas suele anticipar al de actos. Usarlo como variable de "
          "regimen, no como senal de compra/venta aislada.", ""]
    for titulo, datos in (("## 2. Polymarket", poly), ("## 3. Kalshi (API oficial v2)", kal)):
        l += [titulo, ""]
        if datos is None:
            l += ["Omitido en esta corrida.", ""]
            continue
        for palabra in palabras:
            mercados = datos.get(palabra) or []
            l += [f"### {palabra}", ""]
            l += (tabla_mercados(mercados) if mercados else ["Sin mercados abiertos que cumplan filtros."]) + [""]
    l += ["## 4. Como leer estos precios", "",
          "- Precio de 0.30 en un contrato Si/No = el mercado asigna ~30% (menos comisiones y prima de riesgo). "
          "Los extremos (<5% y >95%) suelen estar sesgados (favorito-longshot).",
          "- Diferencial compra/venta amplio o volumen bajo = probabilidad poco informativa.",
          "- Leer el criterio de resolucion exacto (fecha, fuente, definicion) antes de compararlo con un pronostico propio.",
          "- Diferencias grandes entre Polymarket y Kalshi para el mismo evento suelen deberse a criterios distintos, "
          "no a arbitraje gratuito.",
          "- Registrar en bitacora/pronosticos.csv la probabilidad propia y la del mercado para medir si se agrega valor.", ""]
    l += ["## 5. Fuentes primarias para revisar", "", "| Region | Fuente | URL |", "|---|---|---|"]
    for region, fuente, url in FUENTES_PRIMARIAS:
        l.append(f"| {region} | {fuente} | {url} |")
    l += ["", "## 6. Estado de las fuentes", ""]
    l += [f"- {r}" for r in registro] if registro else ["- Todas las fuentes respondieron."]
    l.append("")
    return "\n".join(l)


def generar(palabras: list[str] | None = None, paises: list[str] | None = None, max_por_palabra: int = 6,
            volumen_min: float = 10000.0, cache_horas: float | None = 6, con_gpr: bool = True,
            con_poly: bool = True, con_kalshi: bool = True, fecha: date | None = None) -> tuple[str, dict]:
    palabras = palabras or PALABRAS_DEFECTO
    paises = paises or PAISES_DEFECTO
    fecha = fecha or date.today()
    registro: list[str] = []
    gpr = None
    if con_gpr:
        gpr = {}
        crudo = descargar_gpr(cache_horas, registro)
        try:
            if "mensual" in crudo:
                fuente = crudo["mensual"]
                if fuente["formato"] == "dta":
                    gpr["mensual"] = resumen_gpr_mensual(serie_mensual_gpr(fuente), paises, fuente.get("etiquetas"))
                else:
                    filas = [{**f, "fecha": datetime.strptime(str(f.get("month"))[:7], "%Y-%m").date()}
                             for f in fuente["filas"] if f.get("month")]
                    gpr["mensual"] = resumen_gpr_mensual(filas, paises)
        except (ErrorFuente, ValueError, KeyError, TypeError) as e:
            registro.append(f"GPR mensual: no se pudo resumir: {e!r}")
        try:
            if "diario" in crudo and crudo["diario"]["formato"] == "dta":
                gpr["diario"] = resumen_gpr_diario(serie_diaria_gpr(crudo["diario"]))
        except (ErrorFuente, ValueError, KeyError, TypeError) as e:
            registro.append(f"GPR diario: no se pudo resumir: {e!r}")
    poly = kal = None
    if con_poly:
        try:
            poly = polymarket(palabras, max_por_palabra, volumen_min, cache_horas, registro)
        except Exception as e:  # la fuente falla: se reporta y se sigue
            registro.append(f"Polymarket: {e!r}")
            poly = {}
    if con_kalshi:
        try:
            kal = kalshi(palabras, max_por_palabra, volumen_min, cache_horas, registro)
        except Exception as e:
            registro.append(f"Kalshi: {e!r}")
            kal = {}
    markdown = construir_markdown(fecha, gpr, poly, kal, registro, palabras)
    return markdown, {"gpr": gpr, "polymarket": poly, "kalshi": kal, "registro": registro}


def _json_por_defecto(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()
    raise TypeError(str(type(o)))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Monitor geopolitico: GPR + mercados de prediccion + fuentes")
    ap.add_argument("--palabras", default=",".join(PALABRAS_DEFECTO), help="palabras clave separadas por coma")
    ap.add_argument("--paises", default=",".join(PAISES_DEFECTO), help="codigos ISO3 para GPR por pais")
    ap.add_argument("--max-por-palabra", type=int, default=6)
    ap.add_argument("--volumen-min", type=float, default=10000.0, help="volumen minimo (USD o contratos)")
    ap.add_argument("--cache-horas", type=float, default=6.0, help="0 = sin cache")
    ap.add_argument("--sin-gpr", action="store_true")
    ap.add_argument("--sin-polymarket", action="store_true")
    ap.add_argument("--sin-kalshi", action="store_true")
    ap.add_argument("--salida", default=None, help="ruta del markdown (si se omite, imprime)")
    ap.add_argument("--json", action="store_true", help="imprime los datos en JSON en vez de markdown")
    args = ap.parse_args(argv)
    palabras = [p.strip() for p in args.palabras.split(",") if p.strip()]
    paises = [p.strip().upper() for p in args.paises.split(",") if p.strip()]
    markdown, datos = generar(palabras, paises, args.max_por_palabra, args.volumen_min, args.cache_horas or None,
                              not args.sin_gpr, not args.sin_polymarket, not args.sin_kalshi)
    if args.json:
        print(json.dumps(datos, default=_json_por_defecto, ensure_ascii=False, indent=1))
        return 0
    if args.salida:
        ruta = Path(args.salida)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(markdown, encoding="utf-8")
        print(f"Monitor escrito en {ruta}")
        for r in datos["registro"]:
            print(f"  {r}")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
