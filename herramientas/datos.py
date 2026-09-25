"""Descarga de datos de mercado: FRED (CSV sin llave), Yahoo (chart JSON) y CoinGecko.

Todas las funciones devuelven listas ordenadas por fecha de tuplas (fecha, valor)
con fecha tipo datetime.date (datetime.datetime para intervalos intradia).
Errores de red o de formato se reportan como ErrorDatos tras reintentar.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
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
TIMEOUT_S = 20
REINTENTOS = 3
ESPERA_BASE_S = 1.5
CODIGOS_REINTENTABLES = {408, 425, 429, 500, 502, 503, 504}

URL_FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv"
URL_YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/"
URL_COINGECKO = "https://api.coingecko.com/api/v3/simple/price"


class ErrorDatos(Exception):
    """Fallo al obtener o interpretar datos de una fuente."""


# ---------------------------------------------------------------- transporte

def _ruta_cache(url: str) -> Path:
    return DIR_CACHE / (hashlib.sha1(url.encode()).hexdigest() + ".txt")


def descargar(url: str, encabezados: dict | None = None, timeout: float = TIMEOUT_S,
              reintentos: int = REINTENTOS, cache_horas: float | None = None) -> str:
    """GET con reintentos exponenciales; cache opcional en datos/cache con vigencia en horas."""
    if cache_horas:
        ruta = _ruta_cache(url)
        if ruta.exists() and (time.time() - ruta.stat().st_mtime) < cache_horas * 3600:
            return ruta.read_text(encoding="utf-8")
    encabezados = {"User-Agent": AGENTE, **(encabezados or {})}
    ultimo_error: Exception | None = None
    for intento in range(reintentos):
        try:
            solicitud = urllib.request.Request(url, headers=encabezados)
            with urllib.request.urlopen(solicitud, timeout=timeout) as resp:
                texto = resp.read().decode("utf-8")
            if cache_horas:
                DIR_CACHE.mkdir(parents=True, exist_ok=True)
                _ruta_cache(url).write_text(texto, encoding="utf-8")
            return texto
        except urllib.error.HTTPError as e:
            ultimo_error = e
            if e.code not in CODIGOS_REINTENTABLES:
                break
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            ultimo_error = e
        if intento < reintentos - 1:
            time.sleep(ESPERA_BASE_S * (2 ** intento))
    raise ErrorDatos(f"No se pudo descargar {url}: {ultimo_error!r}")


# ---------------------------------------------------------------- FRED

def parsear_fred_csv(texto: str) -> list[tuple[date, float]]:
    """Convierte el CSV de FRED en [(fecha, valor)], ignorando '.' y celdas vacias."""
    lector = csv.reader(io.StringIO(texto))
    encabezado = next(lector, None)
    if not encabezado or encabezado[0].strip().lower() not in ("observation_date", "date"):
        raise ErrorDatos(f"Respuesta de FRED sin formato CSV esperado: {texto[:120]!r}")
    serie = []
    for fila in lector:
        if len(fila) < 2:
            continue
        valor = fila[1].strip()
        if valor in ("", "."):
            continue
        try:
            serie.append((date.fromisoformat(fila[0].strip()), float(valor)))
        except ValueError:
            continue
    return serie


def fred_serie(id_serie: str, desde: date | str | None = None,
               cache_horas: float | None = None) -> list[tuple[date, float]]:
    """Serie de FRED por id (p. ej. 'DGS10'); 'desde' filtra la fecha inicial."""
    params = {"id": id_serie}
    if desde:
        params["cosd"] = str(desde)
    url = URL_FRED + "?" + urllib.parse.urlencode(params)
    serie = parsear_fred_csv(descargar(url, cache_horas=cache_horas))
    if desde:
        d0 = date.fromisoformat(str(desde))
        serie = [(f, v) for f, v in serie if f >= d0]
    if not serie:
        raise ErrorDatos(f"FRED {id_serie}: serie vacia")
    return serie


# ---------------------------------------------------------------- Yahoo

def parsear_yahoo_json(texto: str, intervalo: str = "1d") -> dict:
    """Interpreta el JSON de chart v8 -> {'meta': dict, 'serie': [(fecha, precio)]}.

    Usa cierre ajustado si existe y no es nulo; si no, el cierre. Fechas en hora
    local de la bolsa (gmtoffset). Si hay dos puntos el mismo dia, conserva el ultimo.
    """
    try:
        datos = json.loads(texto)
        grafica = datos["chart"]
        if grafica.get("error"):
            raise ErrorDatos(f"Yahoo error: {grafica['error']}")
        resultado = grafica["result"][0]
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as e:
        raise ErrorDatos(f"JSON de Yahoo inesperado: {e!r}") from e
    meta = resultado.get("meta", {})
    tiempos = resultado.get("timestamp") or []
    indicadores = resultado.get("indicators", {})
    cierres = (indicadores.get("quote") or [{}])[0].get("close") or []
    ajustados = None
    if indicadores.get("adjclose"):
        ajustados = indicadores["adjclose"][0].get("adjclose")
    desfase = int(meta.get("gmtoffset", 0))
    intradia = intervalo.endswith("m") or intervalo.endswith("h")
    por_fecha: dict = {}
    for i, ts in enumerate(tiempos):
        valor = None
        if ajustados and i < len(ajustados) and ajustados[i] is not None:
            valor = ajustados[i]
        elif i < len(cierres) and cierres[i] is not None:
            valor = cierres[i]
        if valor is None:
            continue
        momento = datetime.fromtimestamp(ts + desfase, tz=timezone.utc).replace(tzinfo=None)
        clave = momento if intradia else momento.date()
        por_fecha[clave] = float(valor)
    return {"meta": meta, "serie": sorted(por_fecha.items())}


def yahoo_grafica(ticker: str, rango: str = "2y", intervalo: str = "1d",
                  cache_horas: float | None = None) -> dict:
    """Serie y metadatos (moneda, bolsa) de Yahoo para un ticker."""
    url = (URL_YAHOO + urllib.parse.quote(ticker, safe="") + "?"
           + urllib.parse.urlencode({"range": rango, "interval": intervalo}))
    resultado = parsear_yahoo_json(descargar(url, cache_horas=cache_horas), intervalo)
    if not resultado["serie"]:
        raise ErrorDatos(f"Yahoo {ticker}: serie vacia")
    return resultado


def yahoo_serie(ticker: str, rango: str = "2y", intervalo: str = "1d",
                cache_horas: float | None = None) -> list[tuple[date, float]]:
    """[(fecha, cierre ajustado o cierre)] de Yahoo."""
    return yahoo_grafica(ticker, rango, intervalo, cache_horas)["serie"]


def yahoo_ultimo(ticker: str, cache_horas: float | None = None) -> tuple[date, float, str]:
    """(fecha, ultimo precio, moneda) de Yahoo."""
    g = yahoo_grafica(ticker, "5d", "1d", cache_horas)
    fecha, precio = g["serie"][-1]
    return fecha, precio, str(g["meta"].get("currency", "")).upper()


# ---------------------------------------------------------------- CoinGecko

def coingecko_precio(ids: str | list[str], vs: str | list[str] = "usd",
                     cache_horas: float | None = None) -> dict:
    """Precio spot {id: {moneda: precio}}; ids como 'bitcoin' o ['bitcoin','ethereum']."""
    ids_txt = ids if isinstance(ids, str) else ",".join(ids)
    vs_txt = vs if isinstance(vs, str) else ",".join(vs)
    url = URL_COINGECKO + "?" + urllib.parse.urlencode({"ids": ids_txt, "vs_currencies": vs_txt})
    try:
        datos = json.loads(descargar(url, cache_horas=cache_horas))
    except json.JSONDecodeError as e:
        raise ErrorDatos(f"CoinGecko devolvio JSON invalido: {e!r}") from e
    if not isinstance(datos, dict) or not datos:
        raise ErrorDatos(f"CoinGecko sin datos para {ids_txt}")
    return datos


# ---------------------------------------------------------------- utilidades de series

def valor_en_o_antes(serie: list[tuple], fecha) -> tuple | None:
    """Ultima observacion con fecha <= fecha (busqueda binaria)."""
    izq, der = 0, len(serie) - 1
    encontrado = None
    while izq <= der:
        medio = (izq + der) // 2
        if serie[medio][0] <= fecha:
            encontrado = serie[medio]
            izq = medio + 1
        else:
            der = medio - 1
    return encontrado


def recortar(serie: list[tuple], desde) -> list[tuple]:
    """Observaciones con fecha >= desde."""
    return [p for p in serie if p[0] >= desde]


def hace_anios(fecha: date, anios: int) -> date:
    """Misma fecha 'anios' atras (29-feb -> 28-feb)."""
    try:
        return fecha.replace(year=fecha.year - anios)
    except ValueError:
        return fecha.replace(year=fecha.year - anios, day=28)


def hoy_menos(dias: int) -> date:
    return date.today() - timedelta(days=dias)
