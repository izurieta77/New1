"""Cliente SEC EDGAR (solo biblioteca estandar): CIK, hechos XBRL, estados financieros y presentaciones.

Uso:
    python3 herramientas/edgar.py NVDA --periodo trimestral [--n 8] [--json] [--presentaciones 12]
    python3 herramientas/edgar.py WMT --periodo anual --n 5

User-Agent: la SEC exige identificarse. Se lee de la variable de entorno SEC_USER_AGENT
(default "SistemaInversionNew1/1.0 investigacion"). Comprobado el 2026-09-25:
  - data.sec.gov (companyfacts, submissions) ACEPTA el default sin correo.
  - www.sec.gov (company_tickers.json, Archives/ con los XML de Form 4) lo RECHAZA con 403;
    exige un correo en el User-Agent, p. ej.
        export SEC_USER_AGENT="SistemaInversionNew1 tu_correo@dominio.com"
    Sin correo, cik_de_ticker usa la busqueda de entidades de EDGAR (efts.sec.gov), que si
    acepta el default, y transacciones_form4 se omite con aviso.
Ritmo: <= 10 solicitudes/s (politica de acceso justo de la SEC); aqui se deja en ~9/s.

Metodo de estados financieros (companyfacts XBRL, solo hechos no dimensionales):
  1. Por concepto: se filtran formas 10-K/10-Q/20-F/40-F (y enmiendas); con varias versiones
     del mismo periodo se usa la presentada MAS RECIENTE (incluye reexpresiones).
  2. Splits: se detectan comparando el mismo periodo de acciones promedio en dos presentaciones
     (razon ~2, 3, 4, 10, 1/10...). Acciones y UPA presentadas antes del split se ajustan.
  3. Calendario fiscal: se arma con los periodos anuales y acumulados (YTD) de la empresa.
     Trimestre k = hecho directo de 3 meses, o acumulado(k) - acumulado(k-1); el Q4 sale de
     anual - 9M. El flujo de efectivo en 10-Q solo viene acumulado: por eso se deriva.
     UPA derivada es aproximada (el promedio de acciones cambia) y acciones Q4 = 4*anual - suma(Q1..Q3).
  4. Cada campo prueba conceptos alternativos por periodo en orden de prioridad.
"""
from __future__ import annotations

import argparse
import gzip
import json
import math
import os
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Callable, NamedTuple

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from herramientas.parametros import DIR_CACHE

AGENTE_DEFECTO = "SistemaInversionNew1/1.0 investigacion"
URL_TICKERS = "https://www.sec.gov/files/company_tickers.json"
URL_ENTIDADES = "https://efts.sec.gov/LATEST/search-index?keysTyped={q}"
URL_HECHOS = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
URL_PRESENTACIONES = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
URL_ARCHIVO = "https://www.sec.gov/Archives/edgar/data/{cik}/{accn}/{doc}"
URL_INDICE = "https://www.sec.gov/Archives/edgar/data/{cik}/{accn}/{accn_guiones}-index.htm"

MAX_SOLICITUDES_S = 10
INTERVALO_MIN_S = 0.11          # ~9 solicitudes/s: margen bajo el limite de 10/s
TIMEOUT_S = 30
REINTENTOS = 3
CODIGOS_REINTENTABLES = {429, 500, 502, 503, 504}
CACHE_TICKERS_H = 24 * 7
CACHE_HECHOS_H = 12
CACHE_PRESENTACIONES_H = 6

FORMAS_VALIDAS = {"10-K", "10-K/A", "10-Q", "10-Q/A", "10-KT", "10-KT/A",
                  "20-F", "20-F/A", "40-F", "40-F/A"}
FORMAS_ANUALES = {"10-K", "10-K/A", "10-KT", "10-KT/A", "20-F", "20-F/A", "40-F", "40-F/A"}
RANGO_TRIMESTRE = (80, 100)     # dias entre inicio y fin (13-14 semanas)
RANGO_ACUMULADO = (170, 285)    # 6M y 9M
RANGO_ANUAL = (350, 380)        # 52/53 semanas o anio calendario
FACTORES_SPLIT = (1.5, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30, 40, 50, 100)
TOLERANCIA_SPLIT = 0.015

# Campos: clase y conceptos alternativos (taxonomia, concepto) en orden de prioridad.
# clase: flujo (sumable), por_accion (UPA, aprox. sumable), promedio (acciones promedio), saldo (balance).
CAMPOS: dict[str, dict] = {
    "ingresos": {"clase": "flujo", "conceptos": [
        ("us-gaap", "Revenues"),
        ("us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax"),
        ("us-gaap", "RevenuesNetOfInterestExpense"),
        ("us-gaap", "RevenueFromContractWithCustomerIncludingAssessedTax"),
        ("us-gaap", "SalesRevenueNet"),
        ("us-gaap", "SalesRevenueGoodsNet"),
        ("ifrs-full", "Revenue"),
        ("ifrs-full", "RevenueFromContractsWithCustomers")]},
    "costo_ventas": {"clase": "flujo", "conceptos": [
        ("us-gaap", "CostOfRevenue"),
        ("us-gaap", "CostOfGoodsAndServicesSold"),
        ("us-gaap", "CostOfGoodsSold"),
        ("ifrs-full", "CostOfSales")]},
    "utilidad_bruta": {"clase": "flujo", "conceptos": [
        ("us-gaap", "GrossProfit"),
        ("ifrs-full", "GrossProfit")]},
    "utilidad_operativa": {"clase": "flujo", "conceptos": [
        ("us-gaap", "OperatingIncomeLoss"),
        ("ifrs-full", "ProfitLossFromOperatingActivities")]},
    "utilidad_neta": {"clase": "flujo", "conceptos": [
        ("us-gaap", "NetIncomeLoss"),
        ("us-gaap", "NetIncomeLossAvailableToCommonStockholdersBasic"),
        ("us-gaap", "ProfitLoss"),
        ("ifrs-full", "ProfitLossAttributableToOwnersOfParent"),
        ("ifrs-full", "ProfitLoss")]},
    "upa_diluida": {"clase": "por_accion", "conceptos": [
        ("us-gaap", "EarningsPerShareDiluted"),
        ("us-gaap", "EarningsPerShareBasicAndDiluted"),
        ("us-gaap", "IncomeLossFromContinuingOperationsPerDilutedShare"),
        ("ifrs-full", "DilutedEarningsLossPerShare")]},
    "flujo_operativo": {"clase": "flujo", "conceptos": [
        ("us-gaap", "NetCashProvidedByUsedInOperatingActivities"),
        ("us-gaap", "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"),
        ("ifrs-full", "CashFlowsFromUsedInOperatingActivities")]},
    "capex": {"clase": "flujo", "conceptos": [
        ("us-gaap", "PaymentsToAcquirePropertyPlantAndEquipment"),
        ("us-gaap", "PaymentsToAcquireProductiveAssets"),
        ("us-gaap", "PaymentsForCapitalImprovements"),
        ("ifrs-full", "PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities")]},
    "sbc": {"clase": "flujo", "conceptos": [
        ("us-gaap", "ShareBasedCompensation"),
        ("us-gaap", "AllocatedShareBasedCompensationExpense"),
        ("ifrs-full", "AdjustmentsForSharebasedPayments")]},
    "efectivo": {"clase": "saldo", "conceptos": [
        ("us-gaap", "CashAndCashEquivalentsAtCarryingValue"),
        ("us-gaap", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"),
        ("us-gaap", "Cash"),
        ("ifrs-full", "CashAndCashEquivalents")]},
    "inversiones_cp": {"clase": "saldo", "conceptos": [
        ("us-gaap", "ShortTermInvestments"),
        ("us-gaap", "MarketableSecuritiesCurrent"),
        ("us-gaap", "AvailableForSaleSecuritiesDebtSecuritiesCurrent"),
        ("us-gaap", "DebtSecuritiesCurrent"),
        ("us-gaap", "AvailableForSaleSecuritiesCurrent"),
        ("ifrs-full", "CurrentInvestments")]},
    "deuda_lp_total": {"clase": "saldo", "conceptos": [
        ("us-gaap", "LongTermDebt"),
        ("us-gaap", "LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities")]},
    "deuda_lp_no_circulante": {"clase": "saldo", "conceptos": [
        ("us-gaap", "LongTermDebtNoncurrent"),
        ("us-gaap", "LongTermDebtAndCapitalLeaseObligations"),
        ("ifrs-full", "NoncurrentPortionOfNoncurrentBorrowings"),
        ("ifrs-full", "LongtermBorrowings")]},
    "deuda_lp_circulante": {"clase": "saldo", "conceptos": [
        ("us-gaap", "LongTermDebtCurrent"),
        ("us-gaap", "LongTermDebtAndCapitalLeaseObligationsCurrent"),
        ("ifrs-full", "CurrentPortionOfNoncurrentBorrowings")]},
    "deuda_cp": {"clase": "saldo", "conceptos": [
        ("us-gaap", "ShortTermBorrowings"),
        ("us-gaap", "CommercialPaper"),
        ("ifrs-full", "ShorttermBorrowings")]},
    "capital_contable": {"clase": "saldo", "conceptos": [
        ("us-gaap", "StockholdersEquity"),
        ("us-gaap", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"),
        ("ifrs-full", "EquityAttributableToOwnersOfParent"),
        ("ifrs-full", "Equity")]},
    "acciones_diluidas": {"clase": "promedio", "conceptos": [
        ("us-gaap", "WeightedAverageNumberOfDilutedSharesOutstanding"),
        ("us-gaap", "WeightedAverageNumberOfShareOutstandingBasicAndDiluted"),
        ("ifrs-full", "AdjustedWeightedAverageShares"),
        ("ifrs-full", "WeightedAverageShares")]},
}
CONCEPTOS_ACCIONES_SPLIT = [
    ("us-gaap", "WeightedAverageNumberOfDilutedSharesOutstanding"),
    ("us-gaap", "WeightedAverageNumberOfSharesOutstandingBasic"),
    ("ifrs-full", "AdjustedWeightedAverageShares"),
    ("ifrs-full", "WeightedAverageShares"),
]
CAMPOS_FLUJO_TTM = ["ingresos", "costo_ventas", "utilidad_bruta", "utilidad_operativa", "utilidad_neta",
                    "upa_diluida", "flujo_operativo", "capex", "fcf", "sbc"]
CAMPOS_SALDO = ["efectivo", "inversiones_cp", "deuda", "deuda_neta", "capital_contable"]

ITEMS_8K = {
    "1.01": "Acuerdo material", "1.02": "Terminacion de acuerdo material", "1.03": "Quiebra o concurso",
    "1.04": "Seguridad minera", "1.05": "Incidente de ciberseguridad material",
    "2.01": "Adquisicion o venta de activos", "2.02": "Resultados de operacion",
    "2.03": "Nueva obligacion financiera", "2.04": "Detonante de aceleracion de deuda",
    "2.05": "Costos de salida o reestructura", "2.06": "Deterioro material",
    "3.01": "Aviso de deslistado o incumplimiento de listado", "3.02": "Venta no registrada de acciones",
    "3.03": "Modificacion de derechos de tenedores", "4.01": "Cambio de auditor",
    "4.02": "Estados financieros previos ya no confiables (reexpresion)", "5.01": "Cambio de control",
    "5.02": "Salida o nombramiento de directivos/consejeros; compensacion",
    "5.03": "Cambio de estatutos o de anio fiscal", "5.05": "Cambio al codigo de etica",
    "5.07": "Votacion de accionistas", "7.01": "Regulation FD", "8.01": "Otros eventos",
    "9.01": "Estados financieros y anexos",
}
ITEMS_8K_ALERTA = {"1.03", "1.05", "2.04", "2.05", "2.06", "3.01", "4.01", "4.02", "5.01"}
CODIGOS_FORM4 = {"P": "compra en mercado", "S": "venta en mercado", "A": "otorgamiento",
                 "M": "ejercicio de derivado", "F": "retencion fiscal", "G": "donacion",
                 "C": "conversion", "D": "disposicion al emisor", "X": "ejercicio de opcion"}


class ErrorSEC(Exception):
    """Fallo al consultar o interpretar datos de EDGAR. 'codigo' = HTTP status si aplica."""

    def __init__(self, mensaje: str, codigo: int | None = None):
        super().__init__(mensaje)
        self.codigo = codigo


# ---------------------------------------------------------------- transporte

def agente_usuario() -> str:
    return os.environ.get("SEC_USER_AGENT", "").strip() or AGENTE_DEFECTO


class _Limitador:
    """Garantiza un intervalo minimo entre solicitudes (seguro entre hilos)."""

    def __init__(self, intervalo_s: float):
        self.intervalo_s = intervalo_s
        self._candado = threading.Lock()
        self._ultimo = 0.0

    def esperar(self) -> None:
        with self._candado:
            ahora = time.monotonic()
            espera = self._ultimo + self.intervalo_s - ahora
            if espera > 0:
                time.sleep(espera)
            self._ultimo = time.monotonic()


LIMITADOR = _Limitador(INTERVALO_MIN_S)


def _get(url: str, timeout: float = TIMEOUT_S, reintentos: int = REINTENTOS) -> bytes:
    """GET a la SEC con User-Agent, gzip, ritmo <= 10/s y reintentos para 429/5xx."""
    encabezados = {"User-Agent": agente_usuario(), "Accept-Encoding": "gzip, deflate"}
    ultimo: Exception | None = None
    for intento in range(reintentos):
        LIMITADOR.esperar()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=encabezados),
                                        timeout=timeout) as resp:
                cuerpo = resp.read()
                if resp.headers.get("Content-Encoding", "").lower() == "gzip":
                    cuerpo = gzip.decompress(cuerpo)
                return cuerpo
        except urllib.error.HTTPError as e:
            ultimo = e
            if e.code == 403:
                raise ErrorSEC(
                    f"SEC rechazo la solicitud (403) a {url}. www.sec.gov exige un correo en el "
                    "User-Agent: export SEC_USER_AGENT=\"SistemaInversionNew1 tu_correo@dominio.com\"",
                    403) from e
            if e.code == 404:
                raise ErrorSEC(f"No existe en EDGAR (404): {url}", 404) from e
            if e.code not in CODIGOS_REINTENTABLES:
                raise ErrorSEC(f"HTTP {e.code} en {url}", e.code) from e
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            ultimo = e
        if intento < reintentos - 1:
            time.sleep(1.0 * (2 ** intento))
    raise ErrorSEC(f"No se pudo descargar {url}: {ultimo!r}",
                   getattr(ultimo, "code", None))


def _ruta_cache(nombre: str) -> Path:
    return DIR_CACHE / nombre


def _json_con_cache(url: str, nombre_cache: str | None, cache_horas: float | None) -> dict | list:
    if nombre_cache and cache_horas:
        ruta = _ruta_cache(nombre_cache)
        if ruta.exists() and (time.time() - ruta.stat().st_mtime) < cache_horas * 3600:
            try:
                return json.loads(ruta.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
    cuerpo = _get(url)
    try:
        datos = json.loads(cuerpo.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ErrorSEC(f"JSON invalido de {url}: {e!r}") from e
    if nombre_cache and cache_horas:
        try:
            DIR_CACHE.mkdir(parents=True, exist_ok=True)
            _ruta_cache(nombre_cache).write_text(json.dumps(datos), encoding="utf-8")
        except OSError:
            pass
    return datos


# ---------------------------------------------------------------- CIK

def normalizar_ticker(ticker: str) -> str:
    """'brk.b' -> 'BRK-B' (convencion de la SEC)."""
    return ticker.strip().upper().replace(".", "-").replace("/", "-")


def mapa_tickers(datos_tickers: dict) -> dict[str, dict]:
    """company_tickers.json -> {TICKER: {'cik': int, 'nombre': str}}."""
    mapa = {}
    for fila in datos_tickers.values():
        try:
            mapa[normalizar_ticker(str(fila["ticker"]))] = {"cik": int(fila["cik_str"]),
                                                            "nombre": str(fila["title"])}
        except (KeyError, TypeError, ValueError):
            continue
    return mapa


def cik_desde_busqueda_entidades(datos: dict, ticker: str) -> dict | None:
    """Respuesta de efts.sec.gov/LATEST/search-index -> {'cik', 'nombre'} si un ticker coincide exacto."""
    objetivo = normalizar_ticker(ticker)
    for hit in (datos.get("hits") or {}).get("hits") or []:
        fuente = hit.get("_source") or {}
        tickers = [normalizar_ticker(t) for t in str(fuente.get("tickers") or "").split(",") if t.strip()]
        if objetivo in tickers:
            nombre = str(fuente.get("entity") or "")
            if " (" in nombre:
                nombre = nombre.rsplit(" (", 1)[0]
            try:
                return {"cik": int(hit["_id"]), "nombre": nombre}
            except (KeyError, ValueError):
                continue
    return None


def info_ticker(ticker: str, cache_horas: float | None = CACHE_TICKERS_H) -> dict:
    """{'ticker', 'cik', 'nombre', 'fuente'}; usa company_tickers.json (cache) o la busqueda de entidades."""
    objetivo = normalizar_ticker(ticker)
    if objetivo.isdigit():
        return {"ticker": objetivo, "cik": int(objetivo), "nombre": "", "fuente": "cik directo"}
    error_mapa: ErrorSEC | None = None
    try:
        mapa = mapa_tickers(_json_con_cache(URL_TICKERS, "sec_company_tickers.json", cache_horas))
        if objetivo in mapa:
            return {"ticker": objetivo, **mapa[objetivo], "fuente": "company_tickers.json"}
    except ErrorSEC as e:
        error_mapa = e
    datos = _json_con_cache(URL_ENTIDADES.format(q=urllib.parse.quote(objetivo)),
                            f"sec_entidad_{objetivo}.json", cache_horas)
    hallado = cik_desde_busqueda_entidades(datos, objetivo)
    if hallado:
        fuente = "busqueda de entidades EDGAR" + (" (company_tickers.json rechazado: 403)"
                                                  if error_mapa and error_mapa.codigo == 403 else "")
        return {"ticker": objetivo, **hallado, "fuente": fuente}
    raise ErrorSEC(f"Ticker {objetivo} no encontrado en EDGAR (emisora no registrada en la SEC o ticker distinto)")


def cik_de_ticker(ticker: str, cache_horas: float | None = CACHE_TICKERS_H) -> int:
    """CIK entero de un ticker (cache en datos/cache)."""
    return int(info_ticker(ticker, cache_horas)["cik"])


def _resolver_cik(cik_o_ticker) -> int:
    if isinstance(cik_o_ticker, int):
        return cik_o_ticker
    texto = str(cik_o_ticker).strip()
    return int(texto) if texto.isdigit() else cik_de_ticker(texto)


def hechos_compania(cik_o_ticker, cache_horas: float | None = CACHE_HECHOS_H) -> dict:
    """JSON companyfacts completo (todos los conceptos XBRL no dimensionales)."""
    cik = _resolver_cik(cik_o_ticker)
    return _json_con_cache(URL_HECHOS.format(cik=cik), f"sec_companyfacts_{cik:010d}.json", cache_horas)


def presentaciones_json(cik_o_ticker, cache_horas: float | None = CACHE_PRESENTACIONES_H) -> dict:
    cik = _resolver_cik(cik_o_ticker)
    return _json_con_cache(URL_PRESENTACIONES.format(cik=cik), f"sec_submissions_{cik:010d}.json",
                           cache_horas)


# ---------------------------------------------------------------- hechos XBRL -> series

class Hecho(NamedTuple):
    inicio: date | None
    fin: date
    valor: float
    presentado: date
    forma: str
    accn: str


def _fecha(texto: str | None) -> date | None:
    if not texto:
        return None
    try:
        return date.fromisoformat(texto[:10])
    except ValueError:
        return None


def _unidad(unidades: dict, clase: str, moneda: str | None = None) -> str | None:
    """Unidad a usar: 'shares' para acciones; '<moneda>/shares' para UPA; la moneda de reporte para montos.

    Con 'moneda' definida solo se acepta esa moneda (evita mezclar la moneda de reporte con traducciones
    de conveniencia a USD que publican algunas emisoras 20-F).
    """
    claves = list(unidades)
    if clase == "promedio":
        return "shares" if "shares" in unidades else None
    if clase == "por_accion":
        if moneda:
            return f"{moneda}/shares" if f"{moneda}/shares" in unidades else None
        if "USD/shares" in unidades:
            return "USD/shares"
        return next((k for k in claves if k.endswith("/shares")), None)
    if moneda:
        return moneda if moneda in unidades else None
    if "USD" in unidades:
        return "USD"
    return next((k for k in claves if k not in ("shares", "pure") and "/" not in k), None)


def moneda_principal(hechos_json: dict) -> str | None:
    """Moneda con mas hechos entre los conceptos monetarios de CAMPOS (moneda de reporte)."""
    conteo: dict = defaultdict(int)
    for spec in CAMPOS.values():
        if spec["clase"] not in ("flujo", "saldo"):
            continue
        for tax, concepto in spec["conceptos"]:
            nodo = ((hechos_json.get("facts") or {}).get(tax) or {}).get(concepto) or {}
            for unidad, hechos in (nodo.get("units") or {}).items():
                if unidad not in ("shares", "pure") and "/" not in unidad:
                    conteo[unidad] += sum(1 for f in hechos if f.get("form") in FORMAS_VALIDAS)
    if not conteo:
        return None
    return max(sorted(conteo), key=lambda u: conteo[u])


def hechos_concepto(hechos_json: dict, taxonomia: str, concepto: str, clase: str,
                    moneda: str | None = None) -> tuple[list[Hecho], str | None]:
    """Hechos de un concepto en formas validas y su unidad."""
    nodo = ((hechos_json.get("facts") or {}).get(taxonomia) or {}).get(concepto)
    if not nodo:
        return [], None
    unidad = _unidad(nodo.get("units") or {}, clase, moneda)
    if not unidad:
        return [], None
    salida = []
    for f in nodo["units"][unidad]:
        if f.get("form") not in FORMAS_VALIDAS:
            continue
        fin, presentado = _fecha(f.get("end")), _fecha(f.get("filed"))
        valor = f.get("val")
        if fin is None or presentado is None or not isinstance(valor, (int, float)):
            continue
        salida.append(Hecho(_fecha(f.get("start")), fin, float(valor), presentado,
                            str(f.get("form")), str(f.get("accn", ""))))
    return salida, unidad


def _factor_split(razon: float) -> float | None:
    """Razon nueva/vieja cercana a un split tipico (o su inverso) -> factor; si no, None."""
    if razon <= 0:
        return None
    for k in FACTORES_SPLIT:
        for c in (float(k), 1.0 / k):
            if abs(razon / c - 1) <= TOLERANCIA_SPLIT:
                return c
    return None


def eventos_split(hechos_acciones: list[Hecho]) -> list[dict]:
    """Splits detectados por reexpresion del mismo periodo entre presentaciones.

    Devuelve [{'factor': k, 'limite_pre': fecha, 'limite_post': fecha}]: todo valor presentado en o
    antes de limite_pre esta en base pre-split y se multiplica por k (acciones) o divide (UPA).
    """
    por_periodo: dict = defaultdict(list)
    for h in hechos_acciones:
        por_periodo[(h.inicio, h.fin)].append(h)
    pares = []
    for lista in por_periodo.values():
        lista.sort(key=lambda h: h.presentado)
        for a, b in zip(lista, lista[1:]):
            if a.valor > 0 and b.valor > 0 and b.presentado > a.presentado:
                k = _factor_split(b.valor / a.valor)
                if k and k != 1.0:
                    pares.append((a.presentado, b.presentado, k))
    pares.sort()
    grupos: list[dict] = []
    for pre, post, k in pares:
        for g in grupos:
            if g["factor"] == k and pre < g["limite_post"] and post > g["limite_pre"]:
                g["limite_pre"] = max(g["limite_pre"], pre)
                g["limite_post"] = min(g["limite_post"], post)
                g["pares"] += 1
                break
        else:
            grupos.append({"factor": k, "limite_pre": pre, "limite_post": post, "pares": 1})
    return sorted(grupos, key=lambda g: g["limite_pre"])


def ajustar_por_split(hechos: list[Hecho], eventos: list[dict], clase: str) -> list[Hecho]:
    """Lleva acciones (x k) y UPA (/ k) presentadas antes de cada split a la base actual."""
    if not eventos or clase not in ("promedio", "por_accion"):
        return hechos
    salida = []
    for h in hechos:
        factor = 1.0
        for ev in eventos:
            if h.presentado <= ev["limite_pre"]:
                factor *= ev["factor"]
        if factor != 1.0:
            valor = h.valor * factor if clase == "promedio" else h.valor / factor
            h = h._replace(valor=valor)
        salida.append(h)
    return salida


def deduplicar(hechos: list[Hecho]) -> dict:
    """{(inicio, fin): Hecho} conservando la presentacion mas reciente (reexpresiones incluidas)."""
    elegido: dict = {}
    for h in hechos:
        clave = (h.inicio, h.fin)
        actual = elegido.get(clave)
        if actual is None or (h.presentado, h.forma.startswith("10-K")) > (actual.presentado,
                                                                           actual.forma.startswith("10-K")):
            elegido[clave] = h
    return elegido


def _dias(inicio: date, fin: date) -> int:
    return (fin - inicio).days


def etiqueta_anio_fiscal(fin_anual: date) -> int:
    """Anio fiscal = anio en que termina (si termina del 1 al 7 de enero, cuenta como el anio previo)."""
    return fin_anual.year - 1 if (fin_anual.month == 1 and fin_anual.day <= 7) else fin_anual.year


def construir_calendario(claves) -> list[dict]:
    """Anios fiscales [{'inicio','fin' (o None si en curso),'anio','trimestres': [(k, fin_k)]}].

    claves: {(inicio, fin): {formas}} o iterable de (inicio, fin). Un periodo de ~12 meses solo define
    anio fiscal si aparece en una forma anual (10-K/20-F/40-F): asi se ignoran las columnas de
    "ultimos doce meses" que algunas emisoras (p. ej. AMZN) incluyen en sus 10-Q.
    """
    formas_por_clave = claves if isinstance(claves, dict) else {c: None for c in claves}
    durs = [(i, f) for (i, f) in formas_por_clave if i is not None and f is not None and f > i]
    anuales: dict = {}
    for i, f in durs:
        formas = formas_por_clave[(i, f)]
        if RANGO_ANUAL[0] <= _dias(i, f) <= RANGO_ANUAL[1] and (formas is None or formas & FORMAS_ANUALES):
            anuales[i] = max(f, anuales.get(i, f))
    inicios = set(anuales)
    for i, f in durs:
        if RANGO_ACUMULADO[0] <= _dias(i, f) <= RANGO_ACUMULADO[1]:
            inicios.add(i)
    # Anio en curso con solo Q1 reportado: trimestre que arranca justo despues de un cierre anual.
    siguientes = {f + timedelta(days=1) for f in anuales.values()}
    for i, f in durs:
        if RANGO_TRIMESTRE[0] <= _dias(i, f) <= RANGO_TRIMESTRE[1]:
            if any(abs((i - s).days) <= 3 for s in siguientes) and i not in inicios:
                if not any(abs((i - s).days) <= 3 for s in inicios):
                    inicios.add(i)
    calendario = []
    for s in sorted(inicios):
        fin_anual = anuales.get(s)
        limite = fin_anual or s + timedelta(days=RANGO_ANUAL[1])
        fines = set()
        for i, f in durs:
            if f > limite:
                continue
            d = _dias(i, f)
            if i == s and RANGO_TRIMESTRE[0] <= d <= RANGO_ANUAL[1]:
                fines.add(f)
            elif s <= i and RANGO_TRIMESTRE[0] <= d <= RANGO_TRIMESTRE[1]:
                fines.add(f)
        if fin_anual:
            fines.add(fin_anual)
        trimestres, previo, k = [], s - timedelta(days=1), 0
        for f in sorted(fines):
            n = round((f - previo).days / 91.3)
            if n < 1:
                continue
            k += n
            if k > 4:
                break
            trimestres.append((k, f))
            previo = f
        fin_estimado = fin_anual or s + timedelta(days=364)
        calendario.append({"inicio": s, "fin": fin_anual, "anio": etiqueta_anio_fiscal(fin_estimado),
                           "trimestres": trimestres})
    # Si dos inicios producen el mismo anio fiscal (transiciones raras), se queda el que tenga cierre anual.
    por_anio: dict = {}
    for a in calendario:
        previo = por_anio.get(a["anio"])
        if previo is None or (a["fin"] is not None and previo["fin"] is None) or (
                (a["fin"] is None) == (previo["fin"] is None) and len(a["trimestres"]) > len(previo["trimestres"])):
            por_anio[a["anio"]] = a
    return [por_anio[k] for k in sorted(por_anio)]


def _valores_trimestrales(dedup: dict, calendario: list[dict], clase: str) -> dict:
    """{(anio, k): (valor, origen)} para un concepto."""
    salida = {}
    if clase == "saldo":
        por_fin = {f: h for (i, f), h in dedup.items() if i is None}
        for a in calendario:
            for k, f in a["trimestres"]:
                h = por_fin.get(f) or next((por_fin[f + timedelta(days=d)] for d in (-1, 1, -2, 2, -3, 3)
                                            if f + timedelta(days=d) in por_fin), None)
                if h is not None:
                    salida[(a["anio"], k)] = (h.valor, "reportado")
        return salida
    trimestrales = defaultdict(list)
    for (i, f), h in dedup.items():
        if i is not None and RANGO_TRIMESTRE[0] <= _dias(i, f) <= RANGO_TRIMESTRE[1]:
            trimestrales[f].append(h)
    for a in calendario:
        s = a["inicio"]
        acumulado = {0: 0.0}
        directos: dict = {}
        fin_previo, k_previo = s - timedelta(days=1), 0
        for k, f in a["trimestres"]:
            inicio_esperado = fin_previo + timedelta(days=1) if k == k_previo + 1 else f - timedelta(days=90)
            q, origen = None, None
            candidatos = [h for h in trimestrales.get(f, []) if abs((h.inicio - inicio_esperado).days) <= 10]
            if candidatos:
                q, origen = candidatos[0].valor, "reportado"
            ytd = dedup.get((s, f))
            if q is None and ytd is not None and k == 1:
                q, origen = ytd.valor, "reportado"
            elif q is None and ytd is not None:
                es_q4 = a["fin"] is not None and f == a["fin"]
                if clase in ("flujo", "por_accion") and acumulado.get(k - 1) is not None:
                    q = ytd.valor - acumulado[k - 1]
                    origen = "derivado anual - 9M" if es_q4 else "derivado acumulado - previo"
                    if clase == "por_accion":
                        origen += " (aprox.)"
                elif clase == "promedio" and all(directos.get(j) is not None for j in range(1, k)):
                    q = k * ytd.valor - sum(directos[j] for j in range(1, k))
                    origen = "derivado promedio (aprox.)"
            if clase in ("flujo", "por_accion"):
                if ytd is not None:
                    acumulado[k] = ytd.valor
                elif q is not None and acumulado.get(k - 1) is not None:
                    acumulado[k] = acumulado[k - 1] + q
                else:
                    acumulado[k] = None
            directos[k] = q
            if q is not None:
                salida[(a["anio"], k)] = (q, origen)
            fin_previo, k_previo = f, k
    return salida


def _valores_anuales(dedup: dict, calendario: list[dict], clase: str) -> dict:
    """{anio: (valor, origen)} para un concepto."""
    salida = {}
    for a in calendario:
        if a["fin"] is None:
            continue
        if clase == "saldo":
            h = dedup.get((None, a["fin"]))
        else:
            h = dedup.get((a["inicio"], a["fin"]))
        if h is not None:
            salida[a["anio"]] = (h.valor, "reportado")
    return salida


def _dividir(a, b):
    if a is None or b is None or b == 0:
        return None
    return a / b


def _crecimiento(actual, previo):
    if actual is None or previo is None or previo <= 0:
        return None
    return actual / previo - 1


def _completar_derivados(fila: dict) -> None:
    """Utilidad bruta derivada, FCF, deuda total y neta."""
    origen = fila["origen"]
    if fila.get("utilidad_bruta") is None and fila.get("ingresos") is not None and fila.get("costo_ventas") is not None:
        fila["utilidad_bruta"] = fila["ingresos"] - fila["costo_ventas"]
        origen["utilidad_bruta"] = "derivado ingresos - costo de ventas"
    if fila.get("flujo_operativo") is not None and fila.get("capex") is not None:
        fila["fcf"] = fila["flujo_operativo"] - fila["capex"]
        origen["fcf"] = "flujo operativo - capex"
    else:
        fila["fcf"] = None
    partes_lp = None
    if fila.get("deuda_lp_total") is not None:
        partes_lp = fila["deuda_lp_total"]
    elif fila.get("deuda_lp_no_circulante") is not None or fila.get("deuda_lp_circulante") is not None:
        partes_lp = (fila.get("deuda_lp_no_circulante") or 0.0) + (fila.get("deuda_lp_circulante") or 0.0)
    if partes_lp is None and fila.get("deuda_cp") is None:
        fila["deuda"] = None
    else:
        fila["deuda"] = (partes_lp or 0.0) + (fila.get("deuda_cp") or 0.0)
        origen["deuda"] = "deuda de largo plazo (incl. circulante) + deuda de corto plazo; sin arrendamientos"
    if fila.get("deuda") is not None and fila.get("efectivo") is not None:
        fila["deuda_neta"] = fila["deuda"] - fila["efectivo"] - (fila.get("inversiones_cp") or 0.0)
        origen["deuda_neta"] = "deuda - efectivo - inversiones CP" + (
            "" if fila.get("inversiones_cp") is not None else " (sin inversiones CP reportadas: se toman como 0)")
    else:
        fila["deuda_neta"] = None


def calcular_metricas(fila: dict, previa: dict | None) -> None:
    """Margenes, SBC/ingresos, conversion de caja y variaciones contra el mismo periodo del anio previo."""
    ing = fila.get("ingresos")
    fila["margen_bruto"] = _dividir(fila.get("utilidad_bruta"), ing)
    fila["margen_operativo"] = _dividir(fila.get("utilidad_operativa"), ing)
    fila["margen_neto"] = _dividir(fila.get("utilidad_neta"), ing)
    fila["margen_fcf"] = _dividir(fila.get("fcf"), ing)
    fila["sbc_ingresos"] = _dividir(fila.get("sbc"), ing)
    un = fila.get("utilidad_neta")
    fila["conversion_caja"] = _dividir(fila.get("fcf"), un) if un is not None and un > 0 else None
    p = previa or {}
    fila["crec_ingresos"] = _crecimiento(ing, p.get("ingresos"))
    fila["crec_utilidad_operativa"] = _crecimiento(fila.get("utilidad_operativa"), p.get("utilidad_operativa"))
    fila["crec_upa"] = _crecimiento(fila.get("upa_diluida"), p.get("upa_diluida"))
    fila["crec_fcf"] = _crecimiento(fila.get("fcf"), p.get("fcf"))
    fila["dilucion_anual"] = _crecimiento(fila.get("acciones_diluidas"), p.get("acciones_diluidas"))
    fila["cambio_margen_operativo"] = (fila["margen_operativo"] - p["margen_operativo"]
                                       if fila["margen_operativo"] is not None and p.get("margen_operativo") is not None
                                       else None)
    fila["cambio_margen_bruto"] = (fila["margen_bruto"] - p["margen_bruto"]
                                   if fila["margen_bruto"] is not None and p.get("margen_bruto") is not None
                                   else None)


def _ttm(filas_trim: list[dict]) -> dict | None:
    """Suma de los ultimos 4 trimestres consecutivos (flujos) y ultimo saldo."""
    if len(filas_trim) < 4:
        return None
    ultimas = filas_trim[-4:]
    for a, b in zip(ultimas, ultimas[1:]):
        consecutivo = (b["anio_fiscal"] == a["anio_fiscal"] and b["trimestre"] == a["trimestre"] + 1) or (
            b["anio_fiscal"] == a["anio_fiscal"] + 1 and a["trimestre"] == 4 and b["trimestre"] == 1)
        if not consecutivo:
            return None
    ttm = {"etiqueta": f"TTM a {ultimas[-1]['etiqueta']}", "fin": ultimas[-1]["fin"],
           "inicio": ultimas[0]["inicio"], "origen": {}}
    for campo in CAMPOS_FLUJO_TTM:
        valores = [f.get(campo) for f in ultimas]
        ttm[campo] = sum(valores) if all(v is not None for v in valores) else None
    for campo in CAMPOS_SALDO + ["acciones_diluidas"]:
        ttm[campo] = ultimas[-1].get(campo)
    return ttm


def extraer_estados(hechos_json: dict, periodo: str = "anual") -> dict:
    """Estados financieros normalizados desde un JSON companyfacts (sin red).

    periodo: 'anual' o 'trimestral'. Devuelve dict con 'filas' (antigua -> reciente),
    'ttm' (solo trimestral), 'splits', 'conceptos' usados, 'moneda' y 'notas'.
    """
    if periodo not in ("anual", "trimestral"):
        raise ValueError("periodo debe ser 'anual' o 'trimestral'")
    splits_hechos: list[Hecho] = []
    for tax, concepto in CONCEPTOS_ACCIONES_SPLIT:
        hs, _ = hechos_concepto(hechos_json, tax, concepto, "promedio")
        splits_hechos += hs
    eventos = eventos_split(splits_hechos)

    por_concepto: dict = {}
    monedas = set()
    claves_calendario = set()
    for campo, spec in CAMPOS.items():
        for tax, concepto in spec["conceptos"]:
            hs, unidad = hechos_concepto(hechos_json, tax, concepto, spec["clase"])
            if not hs:
                continue
            hs = ajustar_por_split(hs, eventos, spec["clase"])
            dedup = deduplicar(hs)
            por_concepto[(campo, tax, concepto)] = dedup
            if spec["clase"] == "flujo" and unidad:
                monedas.add(unidad)
            if spec["clase"] in ("flujo", "por_accion"):
                claves_calendario.update(k for k in dedup if k[0] is not None)
    calendario = construir_calendario(claves_calendario)

    datos: dict = defaultdict(dict)        # clave_periodo -> campo -> valor
    origenes: dict = defaultdict(dict)
    conceptos_usados: dict = defaultdict(set)
    for campo, spec in CAMPOS.items():
        for tax, concepto in spec["conceptos"]:
            dedup = por_concepto.get((campo, tax, concepto))
            if dedup is None:
                continue
            if periodo == "anual":
                valores = _valores_anuales(dedup, calendario, spec["clase"])
            else:
                valores = _valores_trimestrales(dedup, calendario, spec["clase"])
            for clave, (valor, origen) in valores.items():
                if campo not in datos[clave]:
                    datos[clave][campo] = valor
                    origenes[clave][campo] = f"{concepto}: {origen}"
                    conceptos_usados[campo].add(concepto)

    filas = []
    for a in calendario:
        if periodo == "anual":
            if a["fin"] is None or a["anio"] not in datos:
                continue
            fila = {"etiqueta": f"FY{a['anio']}", "anio_fiscal": a["anio"], "trimestre": None,
                    "inicio": a["inicio"], "fin": a["fin"]}
            fila.update({c: datos[a["anio"]].get(c) for c in CAMPOS})
            fila["origen"] = dict(origenes[a["anio"]])
            filas.append(fila)
        else:
            previo_fin = a["inicio"] - timedelta(days=1)
            for k, f in a["trimestres"]:
                clave = (a["anio"], k)
                inicio = previo_fin + timedelta(days=1)
                previo_fin = f
                if clave not in datos:
                    continue
                fila = {"etiqueta": f"FY{a['anio']} Q{k}", "anio_fiscal": a["anio"], "trimestre": k,
                        "inicio": inicio, "fin": f}
                fila.update({c: datos[clave].get(c) for c in CAMPOS})
                fila["origen"] = dict(origenes[clave])
                filas.append(fila)
    for fila in filas:
        _completar_derivados(fila)
    indice = {(f["anio_fiscal"], f["trimestre"]): f for f in filas}
    for fila in filas:
        previa = indice.get((fila["anio_fiscal"] - 1, fila["trimestre"]))
        calcular_metricas(fila, previa)

    ttm = None
    if periodo == "trimestral":
        ttm = _ttm(filas)
        if ttm:
            ttm_previo = _ttm(filas[:-4]) if len(filas) >= 8 else None
            calcular_metricas(ttm, ttm_previo)
    notas = []
    if len(monedas) > 1:
        notas.append(f"Varias unidades monetarias en conceptos de flujo: {sorted(monedas)}")
    for ev in eventos:
        notas.append(f"Split detectado: factor {ev['factor']:g} entre {ev['limite_pre']} y {ev['limite_post']} "
                     f"({ev['pares']} periodos reexpresados); acciones y UPA previas ajustadas")
    if not filas:
        notas.append("Sin datos financieros utilizables en companyfacts (sin us-gaap/ifrs-full o sin formas 10-K/10-Q/20-F)")
    return {
        "cik": hechos_json.get("cik"),
        "nombre": hechos_json.get("entityName", ""),
        "periodo": periodo,
        "moneda": sorted(monedas)[0] if monedas else None,
        "filas": filas,
        "ttm": ttm,
        "splits": eventos,
        "conceptos": {c: sorted(v) for c, v in conceptos_usados.items()},
        "notas": notas,
        "acciones_en_circulacion": acciones_en_circulacion(hechos_json),
    }


def acciones_en_circulacion(hechos_json: dict) -> dict | None:
    """Ultimo dei:EntityCommonStockSharesOutstanding (portada del ultimo 10-K/10-Q): {'valor', 'fecha'}.

    Con varias clases (p. ej. GOOGL/GOOG) suma las clases reportadas en la misma fecha.
    """
    nodo = ((hechos_json.get("facts") or {}).get("dei") or {}).get("EntityCommonStockSharesOutstanding")
    if not nodo or "shares" not in nodo.get("units", {}):
        return None
    hechos = [f for f in nodo["units"]["shares"] if f.get("form") in FORMAS_VALIDAS and f.get("end")]
    if not hechos:
        return None
    ultimo_accn = max(hechos, key=lambda f: (f.get("filed", ""), f["end"]))["accn"]
    mismos = [f for f in hechos if f["accn"] == ultimo_accn]
    fecha = max(f["end"] for f in mismos)
    total = sum(float(f["val"]) for f in mismos if f["end"] == fecha)
    return {"valor": total, "fecha": fecha}


def estados_financieros(ticker: str, periodo: str = "anual", cache_horas: float | None = CACHE_HECHOS_H) -> dict:
    """Descarga companyfacts y devuelve estados normalizados (ver extraer_estados)."""
    info = info_ticker(ticker)
    resultado = extraer_estados(hechos_compania(info["cik"], cache_horas), periodo)
    resultado["ticker"] = info["ticker"]
    resultado["cik"] = info["cik"]
    resultado["nombre"] = resultado["nombre"] or info["nombre"]
    resultado["fuente_cik"] = info["fuente"]
    return resultado


# ---------------------------------------------------------------- presentaciones

def parsear_presentaciones(sub_json: dict, tipos=("8-K", "10-Q", "10-K", "4"), n: int | None = 20,
                           incluir_enmiendas: bool = True) -> list[dict]:
    """Lista de presentaciones recientes desde submissions JSON (mas reciente primero)."""
    recientes = ((sub_json.get("filings") or {}).get("recent")) or {}
    formas = recientes.get("form") or []
    cik = int(sub_json.get("cik") or 0)
    tipos_set = set(tipos)
    salida = []
    for i, forma in enumerate(formas):
        base = forma[:-2] if forma.endswith("/A") else forma
        if forma not in tipos_set and not (incluir_enmiendas and base in tipos_set):
            continue
        def campo(nombre, defecto=""):
            lista = recientes.get(nombre) or []
            return lista[i] if i < len(lista) else defecto
        accn = campo("accessionNumber")
        doc = campo("primaryDocument")
        accn_sin = accn.replace("-", "")
        items_txt = campo("items") or ""
        items = [x.strip() for x in items_txt.split(",") if x.strip()]
        salida.append({
            "fecha": campo("filingDate"),
            "fecha_reporte": campo("reportDate"),
            "forma": forma,
            "descripcion": campo("primaryDocDescription"),
            "items": items,
            "items_texto": [f"{it} {ITEMS_8K.get(it, '')}".strip() for it in items],
            "alerta": any(it in ITEMS_8K_ALERTA for it in items) or forma.endswith("/A"),
            "accn": accn,
            "documento": doc,
            "url": URL_ARCHIVO.format(cik=cik, accn=accn_sin, doc=doc) if doc else "",
            "url_indice": URL_INDICE.format(cik=cik, accn=accn_sin, accn_guiones=accn),
        })
    salida.sort(key=lambda p: (p["fecha"], p["accn"]), reverse=True)
    return salida[:n] if n else salida


def presentaciones_recientes(ticker: str, tipos=("8-K", "10-Q", "10-K", "4"), n: int | None = 20,
                             cache_horas: float | None = CACHE_PRESENTACIONES_H) -> list[dict]:
    """Presentaciones recientes del emisor (submissions de data.sec.gov)."""
    return parsear_presentaciones(presentaciones_json(ticker, cache_horas), tipos, n)


def perfil_emisor(sub_json: dict) -> dict:
    """Datos de portada: nombre, SIC, cierre fiscal, bolsas, estado de incorporacion, sitio."""
    return {
        "nombre": sub_json.get("name", ""),
        "tickers": sub_json.get("tickers") or [],
        "bolsas": sub_json.get("exchanges") or [],
        "sic": sub_json.get("sic", ""),
        "sic_descripcion": sub_json.get("sicDescription", ""),
        "cierre_fiscal_mmdd": sub_json.get("fiscalYearEnd", ""),
        "incorporacion": sub_json.get("stateOfIncorporationDescription") or sub_json.get("stateOfIncorporation", ""),
        "categoria": sub_json.get("category", ""),
        "sitio_inversionistas": sub_json.get("investorWebsite") or sub_json.get("website") or "",
    }


def _texto(nodo, ruta: str) -> str:
    x = nodo.find(ruta) if nodo is not None else None
    return (x.text or "").strip() if x is not None and x.text else ""


def parsear_form4(xml_texto: str) -> dict:
    """XML de Form 4 -> {'propietario','cargo','plan_10b5_1','transacciones': [...]}."""
    raiz = ET.fromstring(xml_texto)
    dueno = raiz.find("reportingOwner")
    relacion = dueno.find("reportingOwnerRelationship") if dueno is not None else None
    cargo = _texto(relacion, "officerTitle")
    if not cargo and relacion is not None:
        if _texto(relacion, "isDirector") in ("1", "true"):
            cargo = "Consejero"
        elif _texto(relacion, "isTenPercentOwner") in ("1", "true"):
            cargo = "Tenedor >10%"
    transacciones = []
    for t in raiz.findall("nonDerivativeTable/nonDerivativeTransaction"):
        try:
            acciones = float(_texto(t, "transactionAmounts/transactionShares/value") or 0)
        except ValueError:
            acciones = 0.0
        try:
            precio = float(_texto(t, "transactionAmounts/transactionPricePerShare/value") or 0)
        except ValueError:
            precio = 0.0
        codigo = _texto(t, "transactionCoding/transactionCode")
        transacciones.append({
            "fecha": _texto(t, "transactionDate/value"),
            "codigo": codigo,
            "tipo": CODIGOS_FORM4.get(codigo, codigo),
            "acciones": acciones,
            "precio": precio,
            "adquirida_dispuesta": _texto(t, "transactionAmounts/transactionAcquiredDisposedCode/value"),
            "valor": acciones * precio,
        })
    return {
        "propietario": _texto(dueno, "reportingOwnerId/rptOwnerName"),
        "cargo": cargo,
        "plan_10b5_1": _texto(raiz, "aff10b5One") in ("1", "true"),
        "transacciones": transacciones,
    }


def transacciones_form4(ticker: str, n: int = 20, cache_horas: float | None = CACHE_PRESENTACIONES_H) -> dict:
    """Resumen de los ultimos n Form 4 (requiere SEC_USER_AGENT con correo: www.sec.gov/Archives)."""
    sub = presentaciones_json(ticker, cache_horas)
    formas4 = parsear_presentaciones(sub, ("4",), n, incluir_enmiendas=False)
    detalle, errores = [], []
    for p in formas4:
        doc = p["documento"].split("/", 1)[1] if "/" in p["documento"] else p["documento"]
        url = URL_ARCHIVO.format(cik=int(sub.get("cik") or 0), accn=p["accn"].replace("-", ""), doc=doc)
        try:
            info = parsear_form4(_get(url).decode("utf-8", "replace"))
        except ErrorSEC as e:
            errores.append(str(e))
            if e.codigo == 403:
                break
            continue
        except ET.ParseError as e:
            errores.append(f"XML invalido {url}: {e}")
            continue
        info["fecha_presentacion"] = p["fecha"]
        info["url"] = url
        detalle.append(info)
    compras = sum(t["valor"] for d in detalle for t in d["transacciones"] if t["codigo"] == "P")
    ventas = sum(t["valor"] for d in detalle for t in d["transacciones"] if t["codigo"] == "S")
    ventas_plan = sum(t["valor"] for d in detalle if d["plan_10b5_1"]
                      for t in d["transacciones"] if t["codigo"] == "S")
    return {"detalle": detalle, "errores": errores, "compras_mercado": compras,
            "ventas_mercado": ventas, "ventas_bajo_plan_10b5_1": ventas_plan,
            "n_revisados": len(detalle), "n_solicitados": len(formas4)}


# ---------------------------------------------------------------- formato

def fmt_monto(x: float | None, escala: float = 1e6) -> str:
    if x is None:
        return "n.d."
    return f"{x / escala:,.1f}"


def fmt_pct(x: float | None, decimales: int = 1) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n.d."
    return f"{x * 100:.{decimales}f}%"


def fmt_num(x: float | None, decimales: int = 2) -> str:
    if x is None:
        return "n.d."
    return f"{x:,.{decimales}f}"


def fmt_pp(x: float | None) -> str:
    if x is None:
        return "n.d."
    return f"{x * 100:+.1f} pp"


def tabla_resultados(filas: list[dict]) -> list[str]:
    """Tabla markdown de resultados, caja y dilucion (montos en millones)."""
    enc = ("| Periodo | Fin | Ingresos | Crec a/a | Mg bruto | Mg oper | Utilidad neta | UPA dil | "
           "Flujo oper | Capex | FCF | FCF/UN | SBC/Ing | Acciones dil (M) | Dilucion a/a |")
    lineas = [enc, "|" + "---|" * 15]
    for f in filas:
        lineas.append(
            f"| {f['etiqueta']} | {f['fin']} | {fmt_monto(f.get('ingresos'))} | {fmt_pct(f.get('crec_ingresos'))} | "
            f"{fmt_pct(f.get('margen_bruto'))} | {fmt_pct(f.get('margen_operativo'))} | "
            f"{fmt_monto(f.get('utilidad_neta'))} | {fmt_num(f.get('upa_diluida'))} | "
            f"{fmt_monto(f.get('flujo_operativo'))} | {fmt_monto(f.get('capex'))} | {fmt_monto(f.get('fcf'))} | "
            f"{fmt_num(f.get('conversion_caja'))} | {fmt_pct(f.get('sbc_ingresos'))} | "
            f"{fmt_monto(f.get('acciones_diluidas'))} | {fmt_pct(f.get('dilucion_anual'))} |")
    return lineas


def tabla_balance(filas: list[dict]) -> list[str]:
    lineas = ["| Periodo | Efectivo | Inversiones CP | Deuda | Deuda neta | Capital contable |",
              "|---|---|---|---|---|---|"]
    for f in filas:
        lineas.append(f"| {f['etiqueta']} | {fmt_monto(f.get('efectivo'))} | {fmt_monto(f.get('inversiones_cp'))} | "
                      f"{fmt_monto(f.get('deuda'))} | {fmt_monto(f.get('deuda_neta'))} | "
                      f"{fmt_monto(f.get('capital_contable'))} |")
    return lineas


def tabla_presentaciones(presentaciones: list[dict]) -> list[str]:
    lineas = ["| Fecha | Forma | Periodo | Items / descripcion | Documento |", "|---|---|---|---|---|"]
    for p in presentaciones:
        detalle = "; ".join(p["items_texto"]) if p["items_texto"] else p["descripcion"]
        marca = "**ALERTA** " if p["alerta"] else ""
        lineas.append(f"| {p['fecha']} | {p['forma']} | {p['fecha_reporte'] or ''} | {marca}{detalle} | "
                      f"[doc]({p['url']}) |")
    return lineas


def _json_por_defecto(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()
    if isinstance(o, set):
        return sorted(o)
    raise TypeError(str(type(o)))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Estados financieros y presentaciones desde SEC EDGAR")
    ap.add_argument("ticker")
    ap.add_argument("--periodo", choices=["anual", "trimestral"], default="anual")
    ap.add_argument("--n", type=int, default=None, help="periodos a mostrar (default 5 anual, 8 trimestral)")
    ap.add_argument("--presentaciones", type=int, default=10, help="presentaciones recientes a listar (0 = ninguna)")
    ap.add_argument("--form4", action="store_true", help="resume los ultimos 20 Form 4 (requiere SEC_USER_AGENT con correo)")
    ap.add_argument("--json", action="store_true", help="imprime el resultado completo en JSON")
    ap.add_argument("--cache-horas", type=float, default=CACHE_HECHOS_H, help="vigencia del cache (0 = sin cache)")
    args = ap.parse_args(argv)
    cache = args.cache_horas or None
    try:
        estados = estados_financieros(args.ticker, args.periodo, cache)
    except ErrorSEC as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    n = args.n or (5 if args.periodo == "anual" else 8)
    filas = estados["filas"][-n:]
    if args.json:
        salida = dict(estados)
        salida["filas"] = filas
        print(json.dumps(salida, default=_json_por_defecto, ensure_ascii=False, indent=1))
        return 0
    print(f"# {estados['nombre']} ({estados['ticker']}) - CIK {estados['cik']} - {args.periodo}")
    print(f"Moneda: {estados['moneda']} (montos en millones; UPA en unidades). CIK via: {estados['fuente_cik']}. "
          f"User-Agent: {agente_usuario()}")
    for nota in estados["notas"]:
        print(f"- {nota}")
    print()
    print("\n".join(tabla_resultados(filas)))
    if estados["ttm"]:
        print()
        print("\n".join(tabla_resultados([estados["ttm"]])))
    print()
    print("\n".join(tabla_balance(filas)))
    derivados = sorted({f"{f['etiqueta']}:{c}" for f in filas for c, o in f["origen"].items() if "derivado" in o})
    if derivados:
        print(f"\nValores derivados (no reportados como trimestre aislado): {', '.join(derivados[:40])}"
              + (" ..." if len(derivados) > 40 else ""))
    print("\nConceptos XBRL usados: " + "; ".join(f"{c}={'/'.join(v)}" for c, v in sorted(estados["conceptos"].items())))
    if args.presentaciones:
        try:
            sub = presentaciones_json(estados["ticker"], cache)
            corporativas = parsear_presentaciones(sub, ("8-K", "10-Q", "10-K", "20-F", "6-K", "DEF 14A"),
                                                  args.presentaciones)
            formas4 = parsear_presentaciones(sub, ("4",), None, incluir_enmiendas=False)
            print()
            print("\n".join(tabla_presentaciones(corporativas)))
            recientes4 = [p for p in formas4 if p["fecha"] >= (date.today() - timedelta(days=90)).isoformat()]
            print(f"\nForm 4 (insiders) en los ultimos 90 dias: {len(recientes4)}"
                  + (f"; el mas reciente {formas4[0]['fecha']}" if formas4 else "")
                  + ". Detalle de compras/ventas: --form4 (requiere SEC_USER_AGENT con correo).")
        except ErrorSEC as e:
            print(f"\nPresentaciones no disponibles: {e}")
    if args.form4:
        try:
            r = transacciones_form4(estados["ticker"])
            print(f"\nForm 4 (ultimos {r['n_revisados']}/{r['n_solicitados']}): compras en mercado "
                  f"{r['compras_mercado']:,.0f} USD; ventas en mercado {r['ventas_mercado']:,.0f} USD "
                  f"(bajo plan 10b5-1: {r['ventas_bajo_plan_10b5_1']:,.0f})")
            for err in r["errores"][:3]:
                print(f"- {err}")
        except ErrorSEC as e:
            print(f"\nForm 4 no disponible: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
