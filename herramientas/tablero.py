"""Tablero markdown de mercado y regimen (FRED + Yahoo).

Uso:
    python3 herramientas/tablero.py [--salida ruta.md] [--cache-horas H] [--hilos N]

Por serie: ultimo valor y fecha, cambio 1s/1m/3m (7/30/91 dias calendario; en pb para
tasas, en puntos para VIX, en % para precios), distancia a la SMA de 200 observaciones
(solo precios) y percentil del ultimo valor en la ventana de 5 anios (o la disponible).
Si una fuente falla se reporta y el tablero continua.
"""
from __future__ import annotations

import argparse
import statistics
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from herramientas import datos

# ---------------------------------------------------------------- universo
# (id, nombre, tipo, usa_sma). tipo: 'precio' (% cambio), 'tasa' (pb), 'puntos'
SERIES_FRED = [
    ("SP500", "S&P 500", "precio", True),
    ("NASDAQCOM", "Nasdaq Composite", "precio", True),
    ("DGS10", "Treasury 10a (%)", "tasa", False),
    ("DGS2", "Treasury 2a (%)", "tasa", False),
    ("T10Y2Y", "Curva 10a-2a (pp)", "tasa", False),
    ("T10Y3M", "Curva 10a-3m (pp)", "tasa", False),
    ("DFF", "Fed funds efectiva (%)", "tasa", False),
    ("DFII10", "Tasa real 10a TIPS (%)", "tasa", False),
    ("T5YIE", "Inflacion implicita 5a (%)", "tasa", False),
    ("VIXCLS", "VIX", "puntos", False),
    ("BAMLH0A0HYM2", "Spread HY EUA OAS (%)", "tasa", False),
    ("DEXMXUS", "USD/MXN (FRED H.10)", "precio", True),
    ("DCOILWTICO", "Petroleo WTI (USD)", "precio", True),
]
SERIES_YAHOO = [
    ("^GSPC", "S&P 500", "precio", True),
    ("^MXX", "S&P/BMV IPC", "precio", True),
    ("MXN=X", "USD/MXN", "precio", True),
    ("^VIX", "VIX (CBOE, Yahoo)", "puntos", False),
    ("GC=F", "Oro futuro (USD)", "precio", True),
    ("BTC-USD", "Bitcoin (USD)", "precio", True),
    ("SPY", "SPY", "precio", True),
    ("EWW", "EWW Mexico (USD)", "precio", True),
    ("TLT", "TLT Treasuries 20a+", "precio", True),
]

# ---------------------------------------------------------------- umbrales de regimen
VENTANA_SMA = 200                  # observaciones
UMBRAL_VIX_CALMA = 15.0            # VIX < 15 calma
UMBRAL_VIX_ESTRES = 25.0           # VIX > 25 estres; entre ambos normal
UMBRAL_HY_VIGILANCIA = 1.10        # spread / mediana 1a > 1.10 vigilancia
UMBRAL_HY_ESTRES = 1.25            # spread / mediana 1a > 1.25 estres
UMBRAL_CURVA_PLANA = 0.50          # pp: 0 a 0.50 plana, > 0.50 positiva, < 0 invertida
UMBRAL_MXN_DEPRECIACION_1M = 0.05  # USD/MXN +5% en 30 dias = depreciacion rapida
UMBRAL_REZAGO_DIAS = 3             # dato mas viejo que esto (dias calendario) se marca como rezagado
SUMA_RISK_ON = 2                   # suma de senales >= 2 risk-on; <= -2 risk-off
DIAS_CAMBIO = {"1s": 7, "1m": 30, "3m": 91}


# ---------------------------------------------------------------- calculos por serie

def percentil(valores: list[float], x: float) -> float:
    """Percentil (0-100) de x dentro de valores: % de observaciones <= x."""
    return 100.0 * sum(1 for v in valores if v <= x) / len(valores)


def resumen_serie(serie: list[tuple], tipo: str, usa_sma: bool, hoy: date | None = None) -> dict:
    """Metricas de tablero para una serie [(fecha, valor)] ordenada."""
    hoy = hoy or date.today()
    fecha, ultimo = serie[-1]
    r = {"ultimo": ultimo, "fecha": fecha, "rezago_dias": (hoy - fecha).days, "cambios": {}}
    for etiqueta, dias in DIAS_CAMBIO.items():
        previo = datos.valor_en_o_antes(serie, fecha - timedelta(days=dias))
        if previo is None:
            r["cambios"][etiqueta] = None
        elif tipo == "precio":
            r["cambios"][etiqueta] = ultimo / previo[1] - 1 if previo[1] else None
        else:
            r["cambios"][etiqueta] = ultimo - previo[1]
    r["sma200"] = None
    r["dist_sma200"] = None
    if usa_sma and len(serie) >= VENTANA_SMA:
        sma = statistics.fmean(v for _, v in serie[-VENTANA_SMA:])
        r["sma200"] = sma
        r["dist_sma200"] = ultimo / sma - 1
    inicio = datos.hace_anios(fecha, 5)
    ventana = [v for f, v in serie if f >= inicio]
    r["percentil_5a"] = percentil(ventana, ultimo)
    r["anios_ventana"] = (fecha - max(serie[0][0], inicio)).days / 365.25
    return r


def mediana_ultimo_anio(serie: list[tuple]) -> float:
    fin = serie[-1][0]
    return statistics.median(v for f, v in serie if f > fin - timedelta(days=365))


def minimo_ultimo_anio(serie: list[tuple]) -> float:
    fin = serie[-1][0]
    return min(v for f, v in serie if f > fin - timedelta(days=365))


# ---------------------------------------------------------------- regimen

def diagnostico_regimen(series: dict, resumenes: dict) -> dict:
    """Reglas explicitas -> dimensiones con (estado, senal +1/0/-1, evidencia) y diagnostico global.

    series/resumenes indexados por clave 'FRED:ID' o 'YAHOO:TICKER'.
    """
    dims = []

    def primero(*claves):
        for c in claves:
            if c in resumenes:
                return c
        return None

    # 1. Tendencia: S&P 500 vs SMA200
    c = primero("FRED:SP500", "YAHOO:^GSPC")
    if c and resumenes[c]["dist_sma200"] is not None:
        d = resumenes[c]["dist_sma200"]
        dims.append(("Tendencia (S&P 500 vs SMA200)", "alcista" if d > 0 else "bajista", 1 if d > 0 else -1,
                     f"{resumenes[c]['ultimo']:,.2f} vs SMA200 {resumenes[c]['sma200']:,.2f} ({d:+.1%}) [{c}]"))
    else:
        dims.append(("Tendencia (S&P 500 vs SMA200)", "sin dato", 0, "S&P 500 no disponible"))

    # 2. Volatilidad: VIX
    # Se usa la fuente mas reciente entre Yahoo ^VIX y FRED VIXCLS (FRED publica con rezago).
    cands = [k for k in ("YAHOO:^VIX", "FRED:VIXCLS") if k in resumenes]
    kv = max(cands, key=lambda k: resumenes[k]["fecha"]) if cands else None
    if kv:
        vix = resumenes[kv]["ultimo"]
        if vix < UMBRAL_VIX_CALMA:
            estado, senal = "calma", 1
        elif vix <= UMBRAL_VIX_ESTRES:
            estado, senal = "normal", 0
        else:
            estado, senal = "estres", -1
        dims.append(("Volatilidad (VIX)", estado, senal,
                     f"VIX {vix:.2f} ({resumenes[kv]['fecha']}, {kv}); calma <{UMBRAL_VIX_CALMA:g}, "
                     f"estres >{UMBRAL_VIX_ESTRES:g}; pctl 5a {resumenes[kv]['percentil_5a']:.0f}"))
    else:
        dims.append(("Volatilidad (VIX)", "sin dato", 0, "VIX no disponible (Yahoo ^VIX ni FRED VIXCLS)"))

    # 3. Credito: spread HY vs mediana de 1 anio
    if "FRED:BAMLH0A0HYM2" in series:
        s = series["FRED:BAMLH0A0HYM2"]
        ultimo, med = s[-1][1], mediana_ultimo_anio(s)
        razon = ultimo / med
        if razon > UMBRAL_HY_ESTRES:
            estado, senal = "estres", -1
        elif razon > UMBRAL_HY_VIGILANCIA:
            estado, senal = "vigilancia", 0
        else:
            estado, senal = "benigno", 1
        cambio = resumenes["FRED:BAMLH0A0HYM2"]["cambios"]["1m"]
        dims.append(("Credito (spread HY)", estado, senal,
                     f"OAS {ultimo:.2f}% vs mediana 1a {med:.2f}% (x{razon:.2f}); 1m {_pb(cambio)}; "
                     f"vigilancia >x{UMBRAL_HY_VIGILANCIA:g}, estres >x{UMBRAL_HY_ESTRES:g}"))
    else:
        dims.append(("Credito (spread HY)", "sin dato", 0, "BAMLH0A0HYM2 no disponible"))

    # 4. Curva: 10a-2a y 10a-3m
    if "FRED:T10Y2Y" in series and "FRED:T10Y3M" in series:
        a, b = series["FRED:T10Y2Y"], series["FRED:T10Y3M"]
        v2, v3 = a[-1][1], b[-1][1]
        if v2 < 0 and v3 < 0:
            estado, senal = "invertida (ambas)", -1
        elif v2 < 0 or v3 < 0:
            estado, senal = "parcialmente invertida", -1
        elif min(minimo_ultimo_anio(a), minimo_ultimo_anio(b)) < 0:
            estado, senal = "des-invertida en los ultimos 12m", 0
        elif v2 > UMBRAL_CURVA_PLANA and v3 > UMBRAL_CURVA_PLANA:
            estado, senal = "positiva", 1
        else:
            estado, senal = "plana", 0
        dims.append(("Curva EUA (10a-2a, 10a-3m)", estado, senal,
                     f"10a-2a {v2:+.2f} pp, 10a-3m {v3:+.2f} pp; min 12m {minimo_ultimo_anio(a):+.2f} / "
                     f"{minimo_ultimo_anio(b):+.2f}; plana si 0-{UMBRAL_CURVA_PLANA:g} pp"))
    else:
        dims.append(("Curva EUA (10a-2a, 10a-3m)", "sin dato", 0, "T10Y2Y/T10Y3M no disponibles"))

    # 5. Dolar-peso: USD/MXN vs SMA200 y cambio 1m
    c = primero("YAHOO:MXN=X", "FRED:DEXMXUS")
    if c and resumenes[c]["dist_sma200"] is not None:
        r = resumenes[c]
        cambio_1m = r["cambios"]["1m"]
        if cambio_1m is not None and cambio_1m > UMBRAL_MXN_DEPRECIACION_1M:
            estado, senal = "depreciacion rapida del peso", -1
        elif r["dist_sma200"] < 0:
            estado, senal = "peso fuerte (USD/MXN < SMA200)", 1
        else:
            estado, senal = "peso debil (USD/MXN > SMA200)", -1
        dims.append(("Dolar-peso (USD/MXN)", estado, senal,
                     f"{r['ultimo']:.4f} vs SMA200 {r['sma200']:.4f} ({r['dist_sma200']:+.1%}); "
                     f"1m {_pct(cambio_1m)}; pctl 5a {r['percentil_5a']:.0f} [{c}]"))
    else:
        dims.append(("Dolar-peso (USD/MXN)", "sin dato", 0, "USD/MXN no disponible"))

    suma = sum(d[2] for d in dims)
    con_dato = sum(1 for d in dims if d[1] != "sin dato")
    if suma >= SUMA_RISK_ON:
        global_ = "RISK-ON"
    elif suma <= -SUMA_RISK_ON:
        global_ = "RISK-OFF"
    else:
        global_ = "MIXTO / TRANSICION"
    return {"dimensiones": dims, "suma": suma, "con_dato": con_dato, "diagnostico": global_}


# ---------------------------------------------------------------- formato

def _pct(x) -> str:
    return "n/d" if x is None else f"{x:+.1%}"


def _pb(x) -> str:
    return "n/d" if x is None else f"{x * 100:+.0f} pb"


def _cambio(x, tipo: str) -> str:
    if x is None:
        return "n/d"
    if tipo == "precio":
        return _pct(x)
    if tipo == "tasa":
        return _pb(x)
    return f"{x:+.2f}"


def _num(x: float, tipo: str) -> str:
    if tipo != "precio" or abs(x) >= 50:
        return f"{x:,.2f}"
    return f"{x:.4f}"


def fila_markdown(nombre: str, fuente: str, r: dict, tipo: str) -> str:
    fecha = r["fecha"].isoformat()
    if r["rezago_dias"] > UMBRAL_REZAGO_DIAS:
        fecha += f" (rezago {r['rezago_dias']} d)"
    pctl = f"{r['percentil_5a']:.0f}"
    if r["anios_ventana"] < 4.9:
        pctl += f" ({r['anios_ventana']:.1f}a)"
    sma = _pct(r["dist_sma200"]) if r["dist_sma200"] is not None else "-"
    return (f"| {nombre} | {fuente} | {_num(r['ultimo'], tipo)} | {fecha} | {_cambio(r['cambios']['1s'], tipo)} | "
            f"{_cambio(r['cambios']['1m'], tipo)} | {_cambio(r['cambios']['3m'], tipo)} | {sma} | {pctl} |")


def construir_markdown(series: dict, resumenes: dict, errores: list[str], regimen: dict,
                       generado: datetime) -> str:
    lineas = [
        f"# Tablero de mercado y regimen - {generado.date().isoformat()}",
        "",
        f"Generado {generado.strftime('%Y-%m-%d %H:%M')} UTC. Fuentes: FRED (CSV publico) y Yahoo Finance "
        "(chart v8, cierre ajustado). Reglas y umbrales en herramientas/tablero.py.",
        "",
        "## Regimen",
        "",
        "| Dimension | Estado | Senal | Evidencia |",
        "|---|---|---|---|",
    ]
    for nombre, estado, senal, evidencia in regimen["dimensiones"]:
        lineas.append(f"| {nombre} | {estado} | {senal:+d} | {evidencia} |")
    lineas += [
        "",
        f"**Diagnostico: {regimen['diagnostico']}** (suma de senales {regimen['suma']:+d} sobre "
        f"{regimen['con_dato']} dimensiones con dato; risk-on si >= +{SUMA_RISK_ON}, risk-off si <= -{SUMA_RISK_ON}).",
        "",
        "Lectura: son reglas descriptivas del estado actual, no pronosticos. Senal +1 = favorable a activos de "
        "riesgo, -1 = desfavorable. Para un inversionista en MXN, peso debil eleva el valor en MXN de activos en USD.",
        "",
        "## Mercados",
        "",
        "| Serie | Fuente | Ultimo | Fecha | 1s | 1m | 3m | vs SMA200 | Pctl 5a |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for fuente, universo in (("FRED", SERIES_FRED), ("YAHOO", SERIES_YAHOO)):
        for ident, nombre, tipo, _ in universo:
            clave = f"{fuente}:{ident}"
            if clave in resumenes:
                lineas.append(fila_markdown(nombre, f"{fuente} {ident}", resumenes[clave], tipo))
    lineas += [
        "",
        "Notas: cambios 1s/1m/3m = 7/30/91 dias calendario; tasas y spreads en puntos base (pb), VIX en puntos, "
        f"precios en %. SMA200 = media de las ultimas {VENTANA_SMA} observaciones. Pctl 5a = % de observaciones "
        "de los ultimos 5 anios <= ultimo valor; entre parentesis la ventana real si es menor "
        "(FRED publica solo ~3 anios del spread HY de ICE). Yahoo puede mostrar el precio intradia del dia en curso.",
    ]
    if errores:
        lineas += ["", "## Fuentes con error", ""] + [f"- {e}" for e in errores]
    return "\n".join(lineas) + "\n"


# ---------------------------------------------------------------- orquestacion

def _descargar_una(fuente: str, ident: str, cache_horas: float | None):
    if fuente == "FRED":
        desde = datos.hace_anios(date.today(), 5) - timedelta(days=10)
        return datos.fred_serie(ident, desde=desde, cache_horas=cache_horas)
    return datos.yahoo_serie(ident, rango="5y", intervalo="1d", cache_horas=cache_horas)


def generar(cache_horas: float | None = None, hilos: int = 6) -> tuple[str, dict]:
    """Descarga todo, calcula y devuelve (markdown, regimen)."""
    tareas = [("FRED", s) for s in SERIES_FRED] + [("YAHOO", s) for s in SERIES_YAHOO]
    series, resumenes, errores = {}, {}, []
    with ThreadPoolExecutor(max_workers=hilos) as ejecutor:
        futuros = {(f, s[0]): ejecutor.submit(_descargar_una, f, s[0], cache_horas) for f, s in tareas}
    for fuente, (ident, nombre, tipo, usa_sma) in tareas:
        clave = f"{fuente}:{ident}"
        try:
            serie = futuros[(fuente, ident)].result()
            series[clave] = serie
            resumenes[clave] = resumen_serie(serie, tipo, usa_sma)
        except Exception as e:  # la fuente falla: se reporta y se sigue
            errores.append(f"{clave} ({nombre}): {e}")
    regimen = diagnostico_regimen(series, resumenes)
    generado = datetime.now(timezone.utc).replace(tzinfo=None)
    return construir_markdown(series, resumenes, errores, regimen, generado), regimen


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Tablero markdown de mercado y regimen")
    ap.add_argument("--salida", help="ruta del archivo markdown (si se omite, imprime en pantalla)")
    ap.add_argument("--cache-horas", type=float, default=0,
                    help="reutiliza descargas de datos/cache con esta antiguedad maxima (0 = sin cache)")
    ap.add_argument("--hilos", type=int, default=6, help="descargas en paralelo")
    args = ap.parse_args(argv)
    markdown, regimen = generar(cache_horas=args.cache_horas or None, hilos=args.hilos)
    if args.salida:
        ruta = Path(args.salida)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(markdown, encoding="utf-8")
        print(f"Tablero escrito en {ruta}")
        print(f"Diagnostico: {regimen['diagnostico']} (suma {regimen['suma']:+d})")
        for nombre, estado, senal, _ in regimen["dimensiones"]:
            print(f"  {nombre}: {estado} ({senal:+d})")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
