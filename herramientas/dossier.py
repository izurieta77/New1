"""Dossier de empresa en markdown: precio y momentum, estados financieros (EDGAR), alertas,
presentaciones recientes, valuacion inversa y secciones que completa el analista.

Uso:
    python3 herramientas/dossier.py MSFT
    python3 herramientas/dossier.py WALMEX.MX
    python3 herramientas/dossier.py AMXB.MX --edgar-ticker AMX      (emisora mexicana con 20-F en la SEC)
Opciones: --fecha AAAA-MM-DD, --salida-dir DIR (default empresas/), --cache-horas H,
          --tasas 0.08,0.09,0.10,0.11 (reverse DCF), --crecimiento-terminal 0.03, --form4, --stdout

Escribe empresas/<TICKER>/dossier-<fecha>.md. Si una fuente falla, lo anota y sigue.
Emisoras .MX sin EDGAR: plantilla con precio, momentum y fuentes (BMV Emisnet, BIVA, reportes trimestrales).
Umbrales de alerta (heuristicas de calidad, no limites de riesgo): dilucion > 3%/anio, conversion de caja
FCF/utilidad neta < 0.7, SBC > 10% de ingresos, caida de margen operativo o bruto > 2 pp a/a.
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from herramientas import edgar
from herramientas.parametros import RAIZ_REPO, obtener

try:  # descarga de precios del kit; si no existe se usa la implementacion local
    from herramientas import datos as _datos
except Exception:  # pragma: no cover - solo si datos.py no existe o falla al importar
    _datos = None

DIR_EMPRESAS = RAIZ_REPO / "empresas"
DIR_CONOCIMIENTO = RAIZ_REPO / "conocimiento"

UMBRAL_DILUCION = 0.03
UMBRAL_CONVERSION = 0.70
UMBRAL_SBC = 0.10
UMBRAL_CAIDA_MARGEN = 0.02
TASAS_DCF = (0.08, 0.09, 0.10, 0.11)
CRECIMIENTO_TERMINAL = 0.03
ANIOS_DCF = 10
DIAS_HABILES = {"1m": 21, "3m": 63, "6m": 126, "12m": 252}

# Emisoras de la BMV que presentan 20-F en la SEC (verificado en EDGAR y Yahoo el 2026-09-25).
# La SEC recibe solo el anual en XBRL; las cifras vienen en la moneda de reporte del emisor.
MX_A_EDGAR = {
    "AMXB.MX": "AMX", "FEMSAUBD.MX": "FMX", "CEMEXCPO.MX": "CX", "KOFUBL.MX": "KOF",
    "ASURB.MX": "ASR", "OMAB.MX": "OMAB", "GAPB.MX": "PAC", "VISTAA.MX": "VIST",
    "SIMECB.MX": "SIM", "TLEVISACPO.MX": "TV",
}
# Sitios de relacion con inversionistas verificados (ampliar al verificar cada emisora).
SITIOS_IR_MX = {
    "WALMEX.MX": "https://www.walmex.mx/informacion-financiera/trimestral.html",
}
CAPITULOS = [
    ("04", "renta fija y macro"), ("11", "Mexico"), ("13", "estado del mercado"),
    ("15", "eventos corporativos"), ("16", "macro, FX y peso"), ("17", "crisis"),
    ("22", "fuentes de datos con IA"), ("23", "geopolitica y riesgo politico"),
]


# ---------------------------------------------------------------- precios

def _yahoo_propio(ticker: str, rango: str = "5y") -> tuple[list, dict]:
    """Descarga directa del chart v8 de Yahoo (solo si datos.py no esta disponible)."""
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/" + urllib.parse.quote(ticker, safe="")
           + "?" + urllib.parse.urlencode({"range": rango, "interval": "1d"}))
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                                timeout=20) as resp:
        crudo = json.loads(resp.read().decode("utf-8"))
    res = crudo["chart"]["result"][0]
    meta = res.get("meta", {})
    tiempos = res.get("timestamp") or []
    ind = res.get("indicators", {})
    cierres = (ind.get("quote") or [{}])[0].get("close") or []
    ajust = (ind.get("adjclose") or [{}])[0].get("adjclose") if ind.get("adjclose") else None
    desfase = int(meta.get("gmtoffset", 0))
    por_fecha = {}
    for i, ts in enumerate(tiempos):
        v = ajust[i] if ajust and i < len(ajust) and ajust[i] is not None else (
            cierres[i] if i < len(cierres) else None)
        if v is not None:
            por_fecha[datetime.fromtimestamp(ts + desfase, tz=timezone.utc).date()] = float(v)
    return sorted(por_fecha.items()), meta


def descargar_precios(ticker: str, rango: str = "5y", cache_horas: float | None = None) -> tuple[list, dict]:
    """([(fecha, precio ajustado)], meta). Usa datos.yahoo_grafica / yahoo_serie si existen."""
    if _datos is not None and hasattr(_datos, "yahoo_grafica"):
        g = _datos.yahoo_grafica(ticker, rango, "1d", cache_horas)
        return g["serie"], g.get("meta", {})
    if _datos is not None and hasattr(_datos, "yahoo_serie"):
        return _datos.yahoo_serie(ticker, rango, "1d", cache_horas), {}
    return _yahoo_propio(ticker, rango)


def _rend(valores: list[float], atras: int, hasta: int = 0) -> float | None:
    """Rendimiento entre valores[-1-atras] y valores[-1-hasta]."""
    if len(valores) <= atras:
        return None
    base = valores[-1 - atras]
    fin = valores[-1 - hasta]
    return fin / base - 1 if base > 0 else None


def resumen_precios(serie: list[tuple], serie_ref: list[tuple] | None = None) -> dict:
    """Momentum, medias moviles, volatilidad, drawdown y beta (ventanas en dias habiles)."""
    if not serie:
        return {}
    fechas = [f for f, _ in serie]
    v = [p for _, p in serie]
    r = {"fecha": fechas[-1], "ultimo": v[-1], "n": len(v)}
    for etiqueta, dias in DIAS_HABILES.items():
        r[f"rend_{etiqueta}"] = _rend(v, dias)
    r["momentum_12_1"] = _rend(v, 252, 21)
    for n in (50, 200):
        r[f"sma{n}"] = statistics.fmean(v[-n:]) if len(v) >= n else None
        r[f"dist_sma{n}"] = v[-1] / r[f"sma{n}"] - 1 if r[f"sma{n}"] else None
    ventana = v[-252:]
    r["max_52s"], r["min_52s"] = max(ventana), min(ventana)
    r["dist_max_52s"] = v[-1] / r["max_52s"] - 1
    rends = [b / a - 1 for a, b in zip(ventana, ventana[1:]) if a > 0]
    r["vol_anual_1a"] = statistics.stdev(rends) * math.sqrt(252) if len(rends) > 20 else None
    pico, mdd = ventana[0], 0.0
    for x in ventana:
        pico = max(pico, x)
        mdd = min(mdd, x / pico - 1)
    r["max_drawdown_1a"] = mdd
    r["beta_1a"] = None
    if serie_ref:
        ref = dict(serie_ref)
        propio = dict(serie)
        comunes = [f for f in fechas[-253:] if f in ref]
        pares = []
        for a, b in zip(comunes, comunes[1:]):
            pa, pb = propio[a], propio[b]
            ra, rb = ref[a], ref[b]
            if pa > 0 and ra > 0:
                pares.append((pb / pa - 1, rb / ra - 1))
        if len(pares) > 60:
            xs = [y for _, y in pares]
            ys = [x for x, _ in pares]
            mx, my = statistics.fmean(xs), statistics.fmean(ys)
            var = sum((x - mx) ** 2 for x in xs)
            if var > 0:
                r["beta_1a"] = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / var
    return r


# ---------------------------------------------------------------- valuacion

def valor_presente_fcf(fcf0: float, g: float, r: float, g_terminal: float, anios: int = ANIOS_DCF) -> float:
    """VP de FCF que crece a g por 'anios' y luego a g_terminal a perpetuidad (descuento r)."""
    if r <= g_terminal:
        raise ValueError("La tasa de descuento debe exceder el crecimiento terminal")
    vp, flujo = 0.0, fcf0
    for t in range(1, anios + 1):
        flujo *= 1 + g
        vp += flujo / (1 + r) ** t
    terminal = flujo * (1 + g_terminal) / (r - g_terminal)
    return vp + terminal / (1 + r) ** anios


def crecimiento_implicito(valor_mercado: float, fcf0: float, r: float, g_terminal: float = CRECIMIENTO_TERMINAL,
                          anios: int = ANIOS_DCF) -> float | None:
    """Reverse DCF: crecimiento anual de FCF por 'anios' que justifica el valor de mercado (biseccion)."""
    if valor_mercado is None or fcf0 is None or fcf0 <= 0 or valor_mercado <= 0 or r <= g_terminal:
        return None
    bajo, alto = -0.5, 1.5
    if valor_presente_fcf(fcf0, alto, r, g_terminal, anios) < valor_mercado:
        return None
    if valor_presente_fcf(fcf0, bajo, r, g_terminal, anios) > valor_mercado:
        return bajo
    for _ in range(200):
        medio = (bajo + alto) / 2
        if valor_presente_fcf(fcf0, medio, r, g_terminal, anios) > valor_mercado:
            alto = medio
        else:
            bajo = medio
    return (bajo + alto) / 2


def valuacion(precio: float | None, moneda_precio: str | None, estados_t: dict | None, estados_a: dict | None) -> dict:
    """Capitalizacion, EV y multiplos TTM; vacio si no hay acciones o si las monedas no coinciden."""
    res: dict = {"nota": None}
    if precio is None or not estados_t:
        res["nota"] = "Sin precio o sin estados trimestrales: no se calcula valuacion"
        return res
    moneda = estados_t.get("moneda")
    if moneda_precio and moneda and moneda_precio.upper() != moneda.upper():
        res["nota"] = (f"Moneda del precio ({moneda_precio}) distinta a la de los estados ({moneda}): "
                       "no se calculan multiplos (posible ADR con razon distinta o reporte en otra moneda)")
        return res
    acciones = (estados_t.get("acciones_en_circulacion") or {}).get("valor")
    base = estados_t.get("ttm")
    if base is None and estados_a and estados_a.get("filas"):
        base = estados_a["filas"][-1]
        res["base"] = f"ultimo anual {base['etiqueta']}"
    else:
        res["base"] = base["etiqueta"] if base else None
    if not acciones or base is None:
        res["nota"] = "Sin acciones en circulacion (dei) o sin base TTM/anual"
        return res
    cap = precio * acciones
    res["acciones"] = acciones
    res["fecha_acciones"] = (estados_t.get("acciones_en_circulacion") or {}).get("fecha")
    res["capitalizacion"] = cap
    deuda, efectivo, inv = base.get("deuda"), base.get("efectivo"), base.get("inversiones_cp")
    res["ev"] = cap + (deuda or 0.0) - (efectivo or 0.0) - (inv or 0.0)
    un, fcf, sbc = base.get("utilidad_neta"), base.get("fcf"), base.get("sbc")
    ing, ebit = base.get("ingresos"), base.get("utilidad_operativa")
    res["pu"] = cap / un if un and un > 0 else None
    res["p_fcf"] = cap / fcf if fcf and fcf > 0 else None
    res["fcf_yield"] = fcf / cap if fcf is not None else None
    res["fcf_menos_sbc_yield"] = (fcf - sbc) / cap if fcf is not None and sbc is not None else None
    res["ev_ingresos"] = res["ev"] / ing if ing else None
    res["ev_ebit"] = res["ev"] / ebit if ebit and ebit > 0 else None
    res["fcf"] = fcf
    res["fcf_menos_sbc"] = fcf - sbc if fcf is not None and sbc is not None else None
    return res


# ---------------------------------------------------------------- alertas

def alertas_financieras(anual: dict | None, trimestral: dict | None) -> list[dict]:
    """Alertas automaticas: [{'alerta','valor','umbral','estado','detalle'}]. estado: ACTIVA / ok / n.d."""
    salida = []
    ttm = (trimestral or {}).get("ttm") or {}
    filas_a = (anual or {}).get("filas") or []
    ult_a = filas_a[-1] if filas_a else {}
    filas_t = (trimestral or {}).get("filas") or []
    ult_t = filas_t[-1] if filas_t else {}

    def agregar(nombre, valor, umbral_txt, activa, detalle, fmt=edgar.fmt_pct):
        estado = "n.d." if valor is None else ("ACTIVA" if activa else "ok")
        salida.append({"alerta": nombre, "valor": fmt(valor) if valor is not None else "n.d.",
                       "umbral": umbral_txt, "estado": estado, "detalle": detalle})

    dil = ttm.get("dilucion_anual") if ttm.get("dilucion_anual") is not None else ult_a.get("dilucion_anual")
    base_dil = "TTM (acciones diluidas del ultimo trimestre vs mismo trimestre del anio previo)" \
        if ttm.get("dilucion_anual") is not None else f"anual {ult_a.get('etiqueta', '')}"
    agregar("Dilucion > 3%/anio", dil, "> 3.0%", dil is not None and dil > UMBRAL_DILUCION, base_dil)
    dil_3a = None
    if len(filas_a) >= 4 and filas_a[-1].get("acciones_diluidas") and filas_a[-4].get("acciones_diluidas"):
        dil_3a = (filas_a[-1]["acciones_diluidas"] / filas_a[-4]["acciones_diluidas"]) ** (1 / 3) - 1
    agregar("Dilucion promedio 3 anios > 3%/anio", dil_3a, "> 3.0%", dil_3a is not None and dil_3a > UMBRAL_DILUCION,
            "CAGR de acciones diluidas en 3 anios fiscales")
    conv = ttm.get("conversion_caja")
    agregar("Conversion de caja TTM < 0.7", conv, "< 0.70", conv is not None and conv < UMBRAL_CONVERSION,
            "FCF / utilidad neta, TTM", fmt=edgar.fmt_num)
    conv_a = ult_a.get("conversion_caja")
    agregar("Conversion de caja ultimo anio < 0.7", conv_a, "< 0.70",
            conv_a is not None and conv_a < UMBRAL_CONVERSION, f"FCF / utilidad neta {ult_a.get('etiqueta', '')}",
            fmt=edgar.fmt_num)
    sbc = ttm.get("sbc_ingresos") if ttm.get("sbc_ingresos") is not None else ult_a.get("sbc_ingresos")
    agregar("SBC > 10% de ingresos", sbc, "> 10.0%", sbc is not None and sbc > UMBRAL_SBC,
            "TTM" if ttm.get("sbc_ingresos") is not None else f"anual {ult_a.get('etiqueta', '')}")
    cm = ttm.get("cambio_margen_operativo")
    agregar("Caida de margen operativo TTM > 2 pp a/a", cm, "< -2.0 pp",
            cm is not None and cm < -UMBRAL_CAIDA_MARGEN, "margen operativo TTM vs TTM de hace un anio",
            fmt=edgar.fmt_pp)
    cmb = ult_t.get("cambio_margen_bruto")
    agregar("Caida de margen bruto ultimo trimestre > 2 pp a/a", cmb, "< -2.0 pp",
            cmb is not None and cmb < -UMBRAL_CAIDA_MARGEN,
            f"{ult_t.get('etiqueta', '')} vs mismo trimestre del anio previo", fmt=edgar.fmt_pp)
    cmo = ult_t.get("cambio_margen_operativo")
    agregar("Caida de margen operativo ultimo trimestre > 2 pp a/a", cmo, "< -2.0 pp",
            cmo is not None and cmo < -UMBRAL_CAIDA_MARGEN,
            f"{ult_t.get('etiqueta', '')} vs mismo trimestre del anio previo", fmt=edgar.fmt_pp)
    un = ttm.get("utilidad_neta") if ttm else ult_a.get("utilidad_neta")
    agregar("Utilidad neta TTM negativa", un, "< 0", un is not None and un < 0, "perdida contable",
            fmt=edgar.fmt_monto)
    return salida


# ---------------------------------------------------------------- utilidades de texto

def _pct(x) -> str:
    return edgar.fmt_pct(x)


def _num(x, d=2) -> str:
    return edgar.fmt_num(x, d)


def _grande(x, moneda: str | None = "") -> str:
    if x is None:
        return "n.d."
    for escala, sufijo in ((1e12, "billones"), (1e9, "miles de millones"), (1e6, "millones")):
        if abs(x) >= escala:
            return f"{x / escala:,.2f} {sufijo} {moneda or ''}".strip()
    return f"{x:,.0f} {moneda or ''}".strip()


def enlaces_conocimiento(desde: Path) -> list[str]:
    """Enlaces relativos a los capitulos existentes de conocimiento/ (o su numero si aun no existen)."""
    lineas = []
    for num, tema in CAPITULOS:
        archivos = sorted(DIR_CONOCIMIENTO.glob(f"{num}-*.md")) if DIR_CONOCIMIENTO.exists() else []
        if archivos:
            rel = Path("../..") / "conocimiento" / archivos[0].name
            lineas.append(f"[{num} {tema}]({rel.as_posix()})")
        else:
            lineas.append(f"cap. {num} {tema} (pendiente)")
    return lineas


def _proximo_reporte(presentaciones: list[dict]) -> tuple[str | None, str]:
    """Fecha estimada del proximo reporte: ultimo 8-K con item 2.02 + 91 dias (estimacion, no confirmada)."""
    resultados = [p for p in presentaciones if p["forma"].startswith("8-K") and "2.02" in p["items"]]
    if not resultados:
        return None, "sin 8-K 2.02 reciente en submissions"
    ultimo = max(resultados, key=lambda p: p["fecha"])
    fecha = date.fromisoformat(ultimo["fecha"]) + timedelta(days=91)
    return fecha.isoformat(), f"ultimo 8-K de resultados {ultimo['fecha']} + 91 dias (no confirmado)"


# ---------------------------------------------------------------- secciones

def seccion_precio(ticker: str, resumen: dict, meta: dict, referencia: str) -> list[str]:
    if not resumen:
        return ["## 1. Precio y momentum", "", "Precio no disponible (fuente con error; ver seccion de errores).", ""]
    moneda = str(meta.get("currency", "") or "").upper()
    tendencia = "sobre" if (resumen.get("dist_sma200") or 0) > 0 else "bajo"
    return [
        "## 1. Precio y momentum",
        "",
        f"Fuente: Yahoo Finance chart v8 (cierre ajustado por dividendos y splits), bolsa {meta.get('fullExchangeName') or meta.get('exchangeName') or 'n.d.'}. "
        f"Beta contra {referencia}.",
        "",
        "| Metrica | Valor |",
        "|---|---|",
        f"| Ultimo cierre ({resumen['fecha']}) | {_num(resumen['ultimo'])} {moneda} |",
        f"| Rendimiento 1m / 3m / 6m / 12m | {_pct(resumen.get('rend_1m'))} / {_pct(resumen.get('rend_3m'))} / "
        f"{_pct(resumen.get('rend_6m'))} / {_pct(resumen.get('rend_12m'))} |",
        f"| Momentum 12-1 (excluye ultimo mes) | {_pct(resumen.get('momentum_12_1'))} |",
        f"| Distancia a SMA50 / SMA200 | {_pct(resumen.get('dist_sma50'))} / {_pct(resumen.get('dist_sma200'))} "
        f"({tendencia} la media de 200 dias) |",
        f"| Maximo / minimo 52 semanas | {_num(resumen.get('max_52s'))} / {_num(resumen.get('min_52s'))} "
        f"(distancia al maximo {_pct(resumen.get('dist_max_52s'))}) |",
        f"| Volatilidad anualizada 1a | {_pct(resumen.get('vol_anual_1a'))} |",
        f"| Maximo drawdown 1a | {_pct(resumen.get('max_drawdown_1a'))} |",
        f"| Beta 1a (diaria) | {_num(resumen.get('beta_1a'))} |",
        "",
    ]


def seccion_estados(anual: dict | None, trimestral: dict | None) -> list[str]:
    lineas = ["## 3. Estados financieros (SEC EDGAR, XBRL)", ""]
    if not anual and not trimestral:
        return lineas + ["Sin datos de EDGAR.", ""]
    base = trimestral or anual
    moneda = base.get("moneda") or "n.d."
    lineas += [f"Montos en millones de {moneda}; UPA en {moneda} por accion. Fuente: companyfacts de la SEC "
               f"(CIK {base.get('cik')}). Valores de Q4 y de flujo trimestral se derivan de acumulados "
               "(anual - 9M); ver notas.", ""]
    notas = []
    for e in (anual, trimestral):
        for n in (e or {}).get("notas", []):
            if n not in notas:
                notas.append(n)
    if notas:
        lineas += [f"- {n}" for n in notas] + [""]
    if trimestral and trimestral.get("filas"):
        filas = trimestral["filas"][-8:]
        lineas += ["### 3.1 Ultimos 8 trimestres", ""] + edgar.tabla_resultados(filas)
        if trimestral.get("ttm"):
            lineas += edgar.tabla_resultados([trimestral["ttm"]])[2:]
        lineas += ["", "Balance al cierre de cada trimestre:", ""] + edgar.tabla_balance(filas) + [""]
        derivados = sorted({f"{f['etiqueta']}:{c}" for f in filas for c, o in f["origen"].items() if "derivado" in o})
        if derivados:
            lineas += [f"Derivados (no reportados aislados): {', '.join(derivados[:30])}"
                       + (" ..." if len(derivados) > 30 else ""), ""]
        descartes = [f"{f['etiqueta']}: {o}" for f in filas for c, o in f["origen"].items() if o.startswith("descartada")]
        lineas += [f"- {d}" for d in descartes] + ([""] if descartes else [])
    if anual and anual.get("filas"):
        filas = anual["filas"][-5:]
        lineas += ["### 3.2 Ultimos 5 anios fiscales", ""] + edgar.tabla_resultados(filas)
        lineas += ["", "Balance al cierre fiscal:", ""] + edgar.tabla_balance(filas) + [""]
        descartes = [f"{f['etiqueta']}: {o}" for f in filas for c, o in f["origen"].items() if o.startswith("descartada")]
        lineas += [f"- {d}" for d in descartes] + ([""] if descartes else [])
    conceptos = (trimestral or anual).get("conceptos") or {}
    if conceptos:
        lineas += ["Conceptos XBRL usados: " + "; ".join(f"{c}={'/'.join(v)}" for c, v in sorted(conceptos.items())), ""]
    return lineas


def seccion_valuacion(val: dict, moneda: str | None, tasas, g_terminal: float) -> list[str]:
    lineas = ["## 4. Valuacion de mercado y reverse DCF", ""]
    if val.get("nota") and not val.get("capitalizacion"):
        return lineas + [val["nota"], ""]
    lineas += [
        f"Base: {val.get('base')}. Acciones en circulacion (portada del ultimo reporte, fecha {val.get('fecha_acciones')}): "
        f"{val['acciones'] / 1e6:,.1f} millones. Con varias series se suman; si hay ADR o series con distinto "
        "derecho economico, verificar.",
        "",
        "| Metrica | Valor |",
        "|---|---|",
        f"| Capitalizacion | {_grande(val.get('capitalizacion'), moneda)} |",
        f"| Valor empresa (cap + deuda - efectivo - inversiones CP; sin arrendamientos) | {_grande(val.get('ev'), moneda)} |",
        f"| P/U (cap / utilidad neta) | {_num(val.get('pu'), 1)} |",
        f"| P/FCF | {_num(val.get('p_fcf'), 1)} |",
        f"| FCF yield / (FCF - SBC) yield | {_pct(val.get('fcf_yield'))} / {_pct(val.get('fcf_menos_sbc_yield'))} |",
        f"| EV/Ingresos | {_num(val.get('ev_ingresos'), 1)} |",
        f"| EV/EBIT | {_num(val.get('ev_ebit'), 1)} |",
        "",
        f"Reverse DCF (valor de capital = VP del FCF a {ANIOS_DCF} anios + perpetuidad a {g_terminal:.1%}): "
        "crecimiento anual del FCF que el precio actual ya descuenta.",
        "",
        "| Tasa de descuento | g implicito con FCF | g implicito con FCF - SBC |",
        "|---|---|---|",
    ]
    for r in tasas:
        g1 = crecimiento_implicito(val.get("capitalizacion"), val.get("fcf"), r, g_terminal)
        g2 = crecimiento_implicito(val.get("capitalizacion"), val.get("fcf_menos_sbc"), r, g_terminal)
        lineas.append(f"| {r:.0%} | {_pct(g1)} | {_pct(g2)} |")
    lineas += [
        "",
        "Lectura: si el g implicito supera lo que el negocio puede sostener 10 anios (compararlo con el "
        "crecimiento historico de 5 anios de la seccion 3.2 y con el crecimiento del mercado total), el precio "
        "exige perfeccion. n.d. = FCF negativo o g fuera de rango (-50% a 150%). FCF TTM de un anio con capex "
        "atipico distorsiona: normalizar si aplica.",
        "",
    ]
    return lineas


def seccion_alertas(alertas: list[dict], presentaciones: list[dict]) -> list[str]:
    lineas = ["## 5. Alertas automaticas", "", "| Alerta | Valor | Umbral | Estado | Base |", "|---|---|---|---|---|"]
    for a in alertas:
        estado = f"**{a['estado']}**" if a["estado"] == "ACTIVA" else a["estado"]
        lineas.append(f"| {a['alerta']} | {a['valor']} | {a['umbral']} | {estado} | {a['detalle']} |")
    corte = (date.today() - timedelta(days=365)).isoformat()
    graves = [p for p in presentaciones if p["alerta"] and p["fecha"] >= corte]
    lineas.append(f"| 8-K con items de alerta o enmiendas (12 meses) | {len(graves)} | > 0 | "
                  f"{'**ACTIVA**' if graves else 'ok'} | items 1.03, 1.05, 2.04-2.06, 3.01, 4.01, 4.02, 5.01 o /A |")
    lineas.append("")
    for p in graves[:8]:
        lineas.append(f"- {p['fecha']} {p['forma']}: {'; '.join(p['items_texto']) or p['descripcion']} ([doc]({p['url']}))")
    if graves:
        lineas.append("")
    return lineas


def seccion_presentaciones(presentaciones: list[dict], formas4: list[dict], resumen4: dict | None,
                           error4: str | None) -> list[str]:
    lineas = ["## 6. Presentaciones recientes (EDGAR)", ""]
    if not presentaciones:
        return lineas + ["Sin presentaciones disponibles.", ""]
    lineas += edgar.tabla_presentaciones(presentaciones[:15]) + [""]
    corte = (date.today() - timedelta(days=90)).isoformat()
    n90 = sum(1 for p in formas4 if p["fecha"] >= corte)
    lineas.append(f"Form 4 (insiders) en 90 dias: {n90}" + (f"; ultimo {formas4[0]['fecha']}" if formas4 else "") + ".")
    if resumen4:
        lineas.append(f"Ultimos {resumen4['n_revisados']} Form 4: compras en mercado (codigo P) "
                      f"{resumen4['compras_mercado']:,.0f} USD; ventas en mercado (S) {resumen4['ventas_mercado']:,.0f} USD, "
                      f"de ellas bajo plan 10b5-1 {resumen4['ventas_bajo_plan_10b5_1']:,.0f} USD. Las compras "
                      "discrecionales de directivos pesan mas que las ventas programadas (ver cap. 15).")
    elif error4:
        lineas.append(f"Detalle de Form 4 no disponible: {error4}")
    else:
        lineas.append("Detalle de compras/ventas: correr con --form4 y SEC_USER_AGENT con correo "
                      "(www.sec.gov/Archives rechaza el User-Agent sin correo).")
    lineas.append("")
    return lineas


def _clave_previa(anio: int, k: int, n: int) -> tuple[int, int]:
    """Trimestre fiscal n posiciones antes de (anio, k)."""
    indice = anio * 4 + (k - 1) - n
    return indice // 4, indice % 4 + 1


def ancla_pronostico(filas_t: list[dict], campo: str = "ingresos", minimo_errores: int = 6) -> dict | None:
    """Ancla ingenua del proximo trimestre y su intervalo empirico de 80%.

    Modelo: X(t) = X(t-4) x (1 + crecimiento a/a de t-1). El intervalo aplica los percentiles 10 y 90 de los
    errores relativos que ese mismo modelo tuvo en los trimestres historicos disponibles (hasta 12).
    Solo para series positivas. No es un pronostico: es la base contra la cual se ajusta por guia y consenso.
    """
    datos = {(f["anio_fiscal"], f["trimestre"]): f.get(campo) for f in filas_t if f.get(campo) is not None}
    if not datos:
        return None

    def ingenuo(anio, k):
        a4, a1, a5 = (datos.get(_clave_previa(anio, k, n)) for n in (4, 1, 5))
        if None in (a4, a1, a5) or min(a4, a1, a5) <= 0:
            return None
        return a4 * (a1 / a5)

    errores = []
    for (anio, k), real in sorted(datos.items())[-12:]:
        pron = ingenuo(anio, k)
        if pron and real > 0:
            errores.append(real / pron - 1)
    ultimo = max(datos)
    siguiente = _clave_previa(ultimo[0], ultimo[1], -1)
    punto = ingenuo(*siguiente)
    if punto is None:
        return None
    res = {"trimestre": f"FY{siguiente[0]} Q{siguiente[1]}", "punto": punto, "n_errores": len(errores),
           "p10": None, "p90": None}
    if len(errores) >= minimo_errores:
        cortes = statistics.quantiles(errores, n=10, method="inclusive")
        res["p10"], res["p90"] = punto * (1 + cortes[0]), punto * (1 + cortes[-1])
    return res


def _sumar_dias_habiles(inicio: date, dias: int) -> date:
    """Suma dias habiles (lunes a viernes; no descuenta feriados oficiales)."""
    fecha, sumados = inicio, 0
    while sumados < dias:
        fecha += timedelta(days=1)
        if fecha.weekday() < 5:
            sumados += 1
    return fecha


def fecha_limite_bmv(hoy: date) -> tuple[date, date]:
    """(cierre de trimestre, fecha limite) del proximo reporte trimestral BMV segun la Circular Unica de
    Emisoras: 20 dias habiles tras Q1-Q3 y 40 tras Q4 (sin feriados; la emisora suele reportar antes)."""
    cierres = []
    for anio in (hoy.year - 1, hoy.year, hoy.year + 1):
        for mes, dia in ((3, 31), (6, 30), (9, 30), (12, 31)):
            cierres.append(date(anio, mes, dia))
    for cierre in cierres:
        limite = _sumar_dias_habiles(cierre, 40 if cierre.month == 12 else 20)
        if limite >= hoy:
            return cierre, limite
    raise ValueError("sin cierre trimestral")  # pragma: no cover


def secciones_analista(ticker: str, nombre: str, trimestral: dict | None, anual: dict | None,
                       presentaciones: list[dict], precio: float | None, moneda: str | None, es_mx: bool,
                       hoy: date | None = None) -> list[str]:
    """Secciones que completa el analista, con datos precargados cuando existen."""
    hoy = hoy or date.today()
    ttm = (trimestral or {}).get("ttm") or {}
    filas_a = (anual or {}).get("filas") or []
    filas_t = (trimestral or {}).get("filas") or []
    crec_5a = None
    if len(filas_a) >= 6 and filas_a[-1].get("ingresos") and filas_a[-6].get("ingresos") and filas_a[-6]["ingresos"] > 0:
        crec_5a = (filas_a[-1]["ingresos"] / filas_a[-6]["ingresos"]) ** (1 / 5) - 1
    recompra = None
    if len(filas_a) >= 2 and filas_a[-1].get("acciones_diluidas") and filas_a[-2].get("acciones_diluidas"):
        recompra = filas_a[-1]["acciones_diluidas"] / filas_a[-2]["acciones_diluidas"] - 1
    capex_int = _pct((ttm.get("capex") / ttm["ingresos"]) if ttm.get("capex") and ttm.get("ingresos") else None)
    if es_mx:
        cierre, limite = fecha_limite_bmv(hoy)
        proximo = limite.isoformat()
        base_proximo = (f"trimestre al {cierre}; limite de la Circular Unica de Emisoras (20/40 dias habiles, "
                        "sin feriados); la emisora suele reportar antes")
        fuente_reporte, doc_anual, doc_proxy, doc_directivos = (
            "BMV eventos relevantes", "informe anual BMV", "convocatoria y actas de asamblea",
            "eventos relevantes de cambios en consejo o direccion")
    else:
        proximo, base_proximo = _proximo_reporte(presentaciones) if presentaciones else (None, "sin datos EDGAR")
        fuente_reporte, doc_anual, doc_proxy, doc_directivos = (
            "EDGAR 8-K 2.02", "10-K", "proxy DEF 14A", "8-K item 5.02")
    anc_ing = ancla_pronostico(filas_t, "ingresos")
    anc_upa = ancla_pronostico(filas_t, "upa_diluida")
    etiqueta_sig = (anc_ing or anc_upa or {}).get("trimestre") or "proximo trimestre"
    limite_pos_std = obtener("concentracion.accion_individual_max")
    limite_pos_arena = obtener("perfiles_riesgo.arena_agresivo.concentracion.accion_individual_max")
    riesgo_std = obtener("riesgo_por_operacion.max_riesgo_pct_capital")
    riesgo_arena = obtener("perfiles_riesgo.arena_agresivo.riesgo_por_operacion")
    brier = obtener("pronosticos.brier_objetivo")

    def fila_ancla(nombre_campo, anc, escala_monto):
        if not anc:
            return f"| {nombre_campo} | n.d. | n.d. | | |"
        fmt = (lambda x: edgar.fmt_monto(x)) if escala_monto else (lambda x: _num(x))
        intervalo = (f"{fmt(anc['p10'])} a {fmt(anc['p90'])} (n={anc['n_errores']})"
                     if anc.get("p10") is not None else f"n.d. (n={anc['n_errores']} errores)")
        return f"| {nombre_campo} | {fmt(anc['punto'])} | {intervalo} | | |"

    criterio = (f"reporte trimestral BMV de {ticker}; ingresos totales reportados" if es_mx
                else f"8-K item 2.02 de {ticker}; ingresos totales reportados")
    lineas = []
    if es_mx:
        lineas += ["> Emisora de la BMV: completar las tablas con el reporte trimestral (BMV/BIVA) antes de las "
                   "secciones siguientes.", ""]
    lineas += [
        "## 7. Negocio y moat (analista)",
        "",
        f"- Que vende, a quien, y quien decide la compra. Segmentos y su peso en ingresos ({doc_anual}, nota de segmentos).",
        "- Fuente de ventaja: costos de cambio / efecto red / escala / activos intangibles / eficiencia. Evidencia medible "
        "(retencion, precios, margen bruto vs competidores), no adjetivos.",
        f"- Crecimiento de ingresos 5 anios (CAGR): {_pct(crec_5a)}. Margen operativo TTM: {_pct(ttm.get('margen_operativo'))}. "
        f"Margen bruto TTM: {_pct(ttm.get('margen_bruto'))}.",
        "- Que tendria que pasar para que el moat se erosione y como se veria primero en los numeros.",
        "",
        "## 8. Gerencia y asignacion de capital (analista)",
        "",
        f"- Cambio en acciones diluidas ultimo anio: {_pct(recompra)} (negativo = recompra neta). SBC/ingresos TTM: "
        f"{_pct(ttm.get('sbc_ingresos'))}. Capex/ingresos TTM: {capex_int}.",
        "- Historial: dijeron vs hicieron (guias previas vs resultados), adquisiciones y su retorno, politica de dividendos.",
        f"- Incentivos ({doc_proxy}): metricas de bono, tenencia de directivos, dilucion por planes.",
        f"- Compras/ventas de insiders y cambios de directivos ({doc_directivos}).",
        "",
        "## 9. Exposicion geopolitica y regulatoria (analista)",
        "",
        f"Ingresos por region ({doc_anual}: ingresos por area geografica o nota de segmentos; companyfacts de la SEC "
        "no trae datos dimensionales):",
        "",
        "| Region | % ingresos ultimo anio | Tendencia | Riesgo especifico (aranceles, controles de exportacion, sanciones, FX) |",
        "|---|---|---|---|",
        "| Estados Unidos | | | |",
        "| Mexico / LatAm | | | |",
        "| China + Hong Kong | | | |",
        "| Taiwan / cadena de suministro | | | |",
        "| Europa | | | |",
        "| Resto | | | |",
        "",
        "Cadena causal por riesgo relevante (acontecimiento -> exposicion -> efecto economico -> estado financiero -> "
        "valuacion -> precio):",
        "",
        "| Acontecimiento | Exposicion | Efecto economico | Linea del estado financiero | Efecto en valuacion | Probabilidad (fuente) |",
        "|---|---|---|---|---|---|",
        "| | | | | | |",
        "",
        "- Regulacion: antimonopolio, privacidad, subsidios/CHIPS, T-MEC (revision 2026), licencias de exportacion.",
        "- Probabilidades de mercados de prediccion: correr `python3 herramientas/geopolitica.py` y copiar aqui las "
        "que muevan la tesis.",
        "",
        "## 10. Catalizadores con fecha (analista)",
        "",
        "| Fecha | Evento | Impacto esperado | Fuente |",
        "|---|---|---|---|",
        f"| {proximo or 'n.d.'} | Reporte {etiqueta_sig} ({base_proximo}) | | {fuente_reporte} |",
        "| | Junta anual / cambio de guia / dia del inversionista | | |",
        "| | Decision regulatoria o arancelaria | | |",
        "",
        "## 11. Escenarios bear / base / bull (analista)",
        "",
        f"Precio actual: {_num(precio)} {moneda or ''}. Probabilidades suman 1. Valor esperado = suma(p_i x precio_i).",
        "",
        "| Escenario | Probabilidad | Supuestos clave (crecimiento, margen, multiplo) | Precio a 12 meses | Rendimiento |",
        "|---|---|---|---|---|",
        "| Bear | | | | |",
        "| Base | | | | |",
        "| Bull | | | | |",
        "| **Valor esperado** | 1.00 | | = suma(p x precio) | = VE / precio - 1 |",
        "",
        "Regla: sin asimetria (VE claramente > precio y bear acotado) no hay posicion. Contrastar con el reverse DCF.",
        "",
        "## 12. Pronostico del proximo reporte (registrar antes del reporte)",
        "",
        f"Ancla estadistica ingenua para {etiqueta_sig}: mismo trimestre del anio previo x (1 + crecimiento a/a del "
        "ultimo trimestre). Intervalo 80% = percentiles 10-90 de los errores historicos de ese mismo modelo. "
        "No es el pronostico: ajustar por guia de la empresa, consenso y lo que diga la seccion 9.",
        "",
        "| Variable | Ancla ingenua | Intervalo 80% empirico del ancla | Punto propio | Intervalo 80% propio |",
        "|---|---|---|---|---|",
        fila_ancla("Ingresos (millones)", anc_ing, True),
        fila_ancla("UPA diluida", anc_upa, False),
        "",
        f"Registrar (probabilidad propia; objetivo Brier <= {brier}); repetir con `python3 herramientas/pronosticos.py "
        f"--archivo empresas/{ticker}/pronosticos.csv agregar ...` para el ledger de la empresa:",
        "",
        "```",
        "python3 herramientas/pronosticos.py agregar --autor claude \\",
        f"  --pregunta \"{ticker}: ingresos {etiqueta_sig} > [umbral = guia o consenso]?\" \\",
        "  --probabilidad 0.__ --fecha-resolucion " + (proximo or "AAAA-MM-DD") + " \\",
        f"  --criterio \"{criterio}\"",
        "```",
        "",
        "## 13. Riesgos y criterio para matar la tesis (analista)",
        "",
        "| Riesgo | Senal temprana medible | Umbral que mata la tesis |",
        "|---|---|---|",
        "| Desaceleracion | crecimiento a/a de ingresos 2 trimestres seguidos | < __% |",
        "| Margen | margen operativo TTM | cae > __ pp |",
        "| Dilucion / SBC | alertas de la seccion 5 | se activan 2 trimestres |",
        "| Geopolitico / regulatorio | evento de la seccion 9 | ocurre |",
        "| Precio | cierre bajo SMA200 con tesis rota | venta sin discusion |",
        "",
        "## 14. Tamano de posicion (config/parametros.json)",
        "",
        f"- Limite por accion individual: {limite_pos_std:.0%} del capital (perfil estandar); {limite_pos_arena:.0%} "
        "(cuenta arena, perfil provisional).",
        f"- Riesgo maximo por operacion (perdida al stop): {riesgo_std:.1%} estandar; {riesgo_arena:.1%} arena.",
        "- Acciones = capital x riesgo_pct / (entrada - stop); valor de la posicion = acciones x entrada, acotado "
        "por el limite de concentracion (herramientas/riesgo.py tamano_por_stop). Fase 0: solo portafolio de papel.",
        "",
    ]
    return lineas


def secciones_mexico_sin_edgar() -> list[str]:
    """Secciones 5 y 6 para emisoras BMV sin EDGAR: reglas de alerta a aplicar a mano y eventos relevantes."""
    return [
        "## 5. Alertas (aplicar a mano con la tabla trimestral)",
        "",
        f"- Dilucion > {UMBRAL_DILUCION:.0%}/anio (acciones en circulacion a/a).",
        f"- Conversion de caja FCF/utilidad neta < {UMBRAL_CONVERSION}.",
        f"- Pagos basados en acciones > {UMBRAL_SBC:.0%} de ingresos (raro en emisoras mexicanas; revisar notas).",
        f"- Caida de margen operativo o bruto > {UMBRAL_CAIDA_MARGEN * 100:.0f} pp a/a.",
        "- Evento relevante de cambio de auditor, reexpresion, incumplimiento de covenants o suspension de cotizacion.",
        "",
        "## 6. Eventos relevantes y reportes (BMV)",
        "",
        "- Eventos relevantes, reportes trimestrales e informe anual: BMV Emisnet (seccion 3) y BIVA.",
        "- Plazos (Circular Unica de Emisoras, CNBV): reporte de Q1-Q3 dentro de 20 dias habiles tras el cierre; "
        "Q4 dentro de 40 dias habiles; informe anual y estados auditados en fechas posteriores.",
        "- Derechos corporativos (dividendos, recompras, splits): avisos de derechos en BMV.",
        "",
    ]


def seccion_mexico(ticker: str, meta: dict, estados_mx: dict | None, ticker_edgar: str | None) -> list[str]:
    emisora = ticker.upper().replace(".MX", "")
    lineas = [
        "## 3. Estados financieros (emisora de la BMV)",
        "",
        f"{meta.get('longName') or emisora} no presenta 10-K/10-Q ante la SEC"
        + (f"; su ADR {ticker_edgar} presenta 20-F (solo anual en XBRL)." if ticker_edgar else
           ": no hay datos en EDGAR. Cifras a capturar del reporte trimestral."),
        "",
        "Fuentes primarias:",
        "",
        "- BMV, informacion de emisoras (Emisnet: reportes trimestrales, eventos relevantes, informe anual): "
        "https://www.bmv.com.mx/es/emisoras/informacion-de-emisoras",
        "- BMV, informacion financiera en formato XBRL por emisora y trimestre: "
        "https://www.bmv.com.mx/es/emisoras/archivos-estadar-xbrl",
        "- BIVA, emisoras inscritas: https://www.biva.mx/empresas/emisoras_inscritas",
        "- CNBV (supervision, sanciones): https://www.gob.mx/cnbv",
    ]
    if ticker.upper() in SITIOS_IR_MX:
        lineas.append(f"- Relacion con inversionistas de la emisora: {SITIOS_IR_MX[ticker.upper()]}")
    lineas += [
        "",
        "Plantilla trimestral (millones de MXN; capturar del reporte trimestral BMV):",
        "",
        "| Trimestre | Ingresos | Crec a/a | Utilidad bruta | EBITDA | Utilidad operativa | Utilidad neta | UPA | "
        "Flujo operativo | Capex | FCF | Deuda neta | Acciones (M) |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    lineas += ["| | | | | | | | | | | | | |"] * 8
    lineas.append("")
    if estados_mx and estados_mx.get("filas"):
        filas = estados_mx["filas"][-5:]
        lineas += [f"### 3.1 Anual desde el 20-F de {ticker_edgar} (SEC XBRL; moneda {estados_mx.get('moneda')})", ""]
        lineas += [f"- {n}" for n in estados_mx.get("notas", [])] + [""]
        lineas += edgar.tabla_resultados(filas) + [""] + edgar.tabla_balance(filas) + [""]
    return lineas


# ---------------------------------------------------------------- orquestacion

def generar(ticker: str, fecha: date | None = None, cache_horas: float | None = edgar.CACHE_HECHOS_H,
            edgar_ticker: str | None = None, tasas=TASAS_DCF, g_terminal: float = CRECIMIENTO_TERMINAL,
            con_form4: bool = False) -> tuple[str, dict]:
    """Construye el markdown del dossier. Devuelve (markdown, resumen)."""
    fecha = fecha or date.today()
    ticker = ticker.strip().upper()
    es_mx = ticker.endswith(".MX")
    errores: list[str] = []
    resumen: dict = {"ticker": ticker, "es_mx": es_mx}

    serie, meta = [], {}
    try:
        serie, meta = descargar_precios(ticker, "5y", cache_horas)
    except Exception as e:
        errores.append(f"Precio {ticker} (Yahoo): {e}")
    referencia = "^MXX (S&P/BMV IPC)" if es_mx else "^GSPC (S&P 500)"
    serie_ref = []
    try:
        serie_ref, _ = descargar_precios("^MXX" if es_mx else "^GSPC", "5y", cache_horas)
    except Exception as e:
        errores.append(f"Referencia de beta: {e}")
    precio_res = resumen_precios(serie, serie_ref) if serie else {}
    precio = precio_res.get("ultimo")
    moneda_precio = str(meta.get("currency") or "").upper() or None
    resumen["precio"] = precio

    ticker_sec = edgar_ticker or (MX_A_EDGAR.get(ticker) if es_mx else ticker)
    anual = trimestral = None
    presentaciones: list[dict] = []
    formas4: list[dict] = []
    perfil: dict = {}
    resumen4, error4 = None, None
    if ticker_sec:
        try:
            anual = edgar.estados_financieros(ticker_sec, "anual", cache_horas)
            if not es_mx:
                trimestral = edgar.estados_financieros(ticker_sec, "trimestral", cache_horas)
        except edgar.ErrorSEC as e:
            errores.append(f"EDGAR estados {ticker_sec}: {e}")
        try:
            sub = edgar.presentaciones_json(ticker_sec, cache_horas)
            perfil = edgar.perfil_emisor(sub)
            presentaciones = edgar.parsear_presentaciones(
                sub, ("8-K", "10-Q", "10-K", "20-F", "6-K", "DEF 14A", "40-F"), 40)
            formas4 = edgar.parsear_presentaciones(sub, ("4",), None, incluir_enmiendas=False)
            for est in (anual, trimestral):
                if est:
                    aviso = edgar.verificar_vigencia(est, sub)
                    if aviso and aviso not in est["notas"]:
                        est["notas"].append(aviso)
        except edgar.ErrorSEC as e:
            errores.append(f"EDGAR presentaciones {ticker_sec}: {e}")
        if con_form4 and not es_mx:
            try:
                resumen4 = edgar.transacciones_form4(ticker_sec, 20, cache_horas)
                if resumen4["errores"] and not resumen4["detalle"]:
                    error4, resumen4 = resumen4["errores"][0], None
            except edgar.ErrorSEC as e:
                error4 = str(e)

    nombre = (anual or {}).get("nombre") or perfil.get("nombre") or meta.get("longName") or ticker
    if es_mx:
        nombre = meta.get("longName") or nombre
    val = valuacion(precio, moneda_precio, trimestral, anual) if not es_mx else (
        valuacion(precio, moneda_precio, anual, anual) if anual else {"nota": "Sin EDGAR: valuacion a capturar"})
    alertas = alertas_financieras(anual, trimestral) if (anual or trimestral) else []
    activas = [a["alerta"] for a in alertas if a["estado"] == "ACTIVA"]
    resumen.update({"nombre": nombre, "alertas_activas": activas,
                    "ingresos_ttm": ((trimestral or {}).get("ttm") or {}).get("ingresos"),
                    "capitalizacion": val.get("capitalizacion")})

    ruta_rel = Path("empresas") / ticker
    lineas = [
        f"# Dossier {nombre} ({ticker})",
        "",
        f"> Generado {fecha.isoformat()} por herramientas/dossier.py. Estado: BORRADOR - las secciones marcadas "
        "(analista) se completan a mano con fuentes primarias. Datos: Yahoo Finance (precio), SEC EDGAR "
        "companyfacts/submissions (estados y presentaciones). Hechos con fecha y fuente; inferencias marcadas.",
        "",
        "Capitulos relacionados: " + " · ".join(enlaces_conocimiento(ruta_rel)),
        "",
        "## 0. Resumen automatico",
        "",
        f"- Precio: {_num(precio)} {moneda_precio or ''} al {precio_res.get('fecha', 'n.d.')}; 12m {_pct(precio_res.get('rend_12m'))}; "
        f"{'sobre' if (precio_res.get('dist_sma200') or 0) > 0 else 'bajo'} SMA200 ({_pct(precio_res.get('dist_sma200'))}).",
    ]
    ttm = (trimestral or {}).get("ttm") or {}
    if ttm:
        lineas.append(f"- TTM: ingresos {edgar.fmt_monto(ttm.get('ingresos'))} M (a/a {_pct(ttm.get('crec_ingresos'))}), "
                      f"margen operativo {_pct(ttm.get('margen_operativo'))}, FCF {edgar.fmt_monto(ttm.get('fcf'))} M, "
                      f"conversion {_num(ttm.get('conversion_caja'))}, dilucion {_pct(ttm.get('dilucion_anual'))}.")
    if val.get("capitalizacion"):
        lineas.append(f"- Capitalizacion {_grande(val['capitalizacion'], moneda_precio)}; P/U {_num(val.get('pu'), 1)}; "
                      f"P/FCF {_num(val.get('p_fcf'), 1)}; FCF yield {_pct(val.get('fcf_yield'))}.")
    lineas.append(f"- Alertas activas: {', '.join(activas) if activas else 'ninguna'}" if alertas else
                  "- Alertas: sin datos financieros automaticos (capturar del reporte).")
    if perfil:
        lineas.append(f"- Emisor: {perfil.get('nombre')} · SIC {perfil.get('sic')} {perfil.get('sic_descripcion')} · "
                      f"cierre fiscal {perfil.get('cierre_fiscal_mmdd')} · {perfil.get('incorporacion')} · "
                      f"bolsas {', '.join(perfil.get('bolsas') or [])} · IR: {perfil.get('sitio_inversionistas') or 'n.d.'}")
    lineas.append("")
    lineas += seccion_precio(ticker, precio_res, meta, referencia)
    lineas += ["## 2. Contexto", "",
               "Inferencia (llenar): regimen de mercado actual (bitacora/briefs, tablero.py) y como afecta a la tesis.", ""]
    if es_mx:
        lineas += seccion_mexico(ticker, meta, anual, ticker_sec)
        if anual:
            lineas += seccion_valuacion(val, (anual or {}).get("moneda"), tasas, g_terminal)
            lineas += seccion_alertas(alertas, presentaciones)
            lineas += seccion_presentaciones(presentaciones, formas4, None, None)
        else:
            lineas += ["## 4. Valuacion", "", "Capitalizacion = precio x acciones en circulacion (reporte BMV). "
                       "Reverse DCF: `from herramientas.dossier import crecimiento_implicito` con capitalizacion y FCF "
                       "capturados (misma moneda).", ""]
            lineas += secciones_mexico_sin_edgar()
    else:
        lineas += seccion_estados(anual, trimestral)
        lineas += seccion_valuacion(val, (trimestral or anual or {}).get("moneda"), tasas, g_terminal)
        lineas += seccion_alertas(alertas, presentaciones)
        lineas += seccion_presentaciones(presentaciones, formas4, resumen4, error4)
    lineas += secciones_analista(ticker, nombre, trimestral, anual, presentaciones, precio, moneda_precio, es_mx, fecha)
    lineas += ["## 15. Fuentes", ""]
    lineas.append(f"- Yahoo Finance chart: https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(ticker)}?range=5y&interval=1d")
    if anual or trimestral:
        cik = (anual or trimestral)["cik"]
        lineas.append(f"- SEC companyfacts: https://data.sec.gov/api/xbrl/companyfacts/CIK{int(cik):010d}.json")
        lineas.append(f"- SEC submissions: https://data.sec.gov/submissions/CIK{int(cik):010d}.json")
        lineas.append(f"- EDGAR (listado de presentaciones): https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={int(cik)}")
    if errores:
        lineas += ["", "## Errores de fuentes", ""] + [f"- {e}" for e in errores]
    lineas.append("")
    resumen["errores"] = errores
    return "\n".join(lineas), resumen


def ruta_dossier(ticker: str, fecha: date, salida_dir: Path | None = None) -> Path:
    return (salida_dir or DIR_EMPRESAS) / ticker.strip().upper() / f"dossier-{fecha.isoformat()}.md"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Genera el dossier markdown de una empresa")
    ap.add_argument("ticker", help="ticker de Yahoo (MSFT, WALMEX.MX, ...)")
    ap.add_argument("--fecha", default=None, help="fecha del dossier AAAA-MM-DD (default hoy)")
    ap.add_argument("--salida-dir", default=None, help="directorio base (default empresas/)")
    ap.add_argument("--edgar-ticker", default=None, help="ticker en la SEC si difiere (p. ej. AMX para AMXB.MX)")
    ap.add_argument("--cache-horas", type=float, default=edgar.CACHE_HECHOS_H, help="vigencia del cache (0 = sin cache)")
    ap.add_argument("--tasas", default=",".join(str(t) for t in TASAS_DCF), help="tasas de descuento del reverse DCF")
    ap.add_argument("--crecimiento-terminal", type=float, default=CRECIMIENTO_TERMINAL)
    ap.add_argument("--form4", action="store_true", help="resume los ultimos 20 Form 4 (requiere SEC_USER_AGENT con correo)")
    ap.add_argument("--stdout", action="store_true", help="imprime en pantalla en vez de escribir el archivo")
    args = ap.parse_args(argv)
    fecha = date.fromisoformat(args.fecha) if args.fecha else date.today()
    tasas = tuple(float(x) for x in args.tasas.split(",") if x.strip())
    markdown, resumen = generar(args.ticker, fecha, args.cache_horas or None, args.edgar_ticker, tasas,
                                args.crecimiento_terminal, args.form4)
    if args.stdout:
        print(markdown)
        return 0
    ruta = ruta_dossier(args.ticker, fecha, Path(args.salida_dir) if args.salida_dir else None)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(markdown, encoding="utf-8")
    print(f"Dossier escrito en {ruta}")
    print(f"Alertas activas: {', '.join(resumen['alertas_activas']) or 'ninguna'}")
    for e in resumen["errores"]:
        print(f"Aviso de fuente: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
