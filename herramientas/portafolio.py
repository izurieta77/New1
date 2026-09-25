"""Libro de operaciones en papel, valuacion a mercado, curva de equity y reporte vs benchmark.

Uso:
    python3 herramientas/portafolio.py registrar --lado deposito --cantidad 1000000 --fecha 2026-09-25
    python3 herramientas/portafolio.py registrar --fecha 2026-09-25 --ticker SPY --lado compra \\
        --cantidad 10 --precio 767.18 --moneda USD [--comision 1] [--stop 700] [--tesis-id T001] \\
        [--estrategia nucleo] [--notas "..."]
    (compras/ventas se validan antes contra parametros.json; --clase, --fase, --forzar)
    python3 herramientas/portafolio.py posiciones
    python3 herramientas/portafolio.py valuar [--reconstruir] [--sin-guardar]
    python3 herramientas/portafolio.py reporte [--tasa-cetes 0.07] [--salida ruta.md]
Opciones globales: --operaciones RUTA, --equity RUTA, --perfil {arena_agresivo,cripto_binance,estandar}.
El libro por defecto es la cuenta arena-claude, asi que el perfil por defecto es arena_agresivo.

Convenciones: moneda base MXN. Efectivo unico en MXN; operaciones en USD se convierten con
USD/MXN (Yahoo MXN=X) del cierre en o antes de la fecha de la operacion. Costo promedio
ponderado (comisiones incluidas). No se permiten ventas en corto (venta > posicion).
El rendimiento se mide con indice time-weighted (neutral a depositos y retiros).
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path
from typing import Callable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from herramientas import datos, metricas, riesgo
from herramientas.parametros import DIR_BITACORA, obtener, parametros_efectivos

COLUMNAS_OPS = ["fecha", "ticker", "lado", "cantidad", "precio", "moneda", "comision", "stop",
                "tesis_id", "estrategia", "notas"]
COLUMNAS_EQUITY = ["fecha", "efectivo_mxn", "posiciones_mxn", "equity_mxn", "aportaciones_netas_mxn", "indice"]
RUTA_OPS = DIR_BITACORA / "operaciones.csv"
RUTA_EQUITY = DIR_BITACORA / "equity.csv"
LADOS = ("compra", "venta", "deposito", "retiro")
MONEDAS = ("MXN", "USD")
TICKER_EFECTIVO = "EFECTIVO"
TICKER_FX = "MXN=X"                 # USD/MXN en Yahoo
TICKER_SPX_TR = "^SP500TR"          # S&P 500 Total Return (USD) en Yahoo
SERIE_CETES_PROXY = "INTGSTMXM193N"  # FRED/FMI: T-bills Mexico, % anual, mensual (proxy de CETES 28d)
MIN_OBS_METRICAS = 20
EPS = 1e-9

FuncionFX = Callable[[date], float]


class ErrorPortafolio(Exception):
    """Operacion invalida sobre el libro."""


# ---------------------------------------------------------------- archivos

def asegurar_archivo(ruta: str | Path, columnas: list[str]) -> Path:
    ruta = Path(ruta)
    if not ruta.exists():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(columnas)
    return ruta


def _escribir_csv(ruta: str | Path, columnas: list[str], filas: list[dict]) -> None:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=ruta.parent, suffix=".tmp")
    with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columnas)
        w.writeheader()
        for fila in filas:
            w.writerow({c: fila.get(c, "") for c in columnas})
    os.replace(tmp, ruta)


def _flotante(x, defecto=None):
    return defecto if x in (None, "") else float(x)


def leer_operaciones(ruta: str | Path = RUTA_OPS) -> list[dict]:
    """Operaciones tipadas y ordenadas por fecha (orden de registro dentro del mismo dia)."""
    ruta = asegurar_archivo(ruta, COLUMNAS_OPS)
    with open(ruta, newline="", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    ops = []
    for i, f in enumerate(filas):
        ops.append({**f, "fecha": date.fromisoformat(f["fecha"]), "cantidad": float(f["cantidad"]),
                    "precio": float(f["precio"]), "comision": _flotante(f["comision"], 0.0),
                    "stop": _flotante(f["stop"]), "lado": f["lado"].lower(), "moneda": f["moneda"].upper(),
                    "_orden": i})
    return sorted(ops, key=lambda o: (o["fecha"], o["_orden"]))


def leer_equity(ruta: str | Path = RUTA_EQUITY) -> list[dict]:
    ruta = asegurar_archivo(ruta, COLUMNAS_EQUITY)
    with open(ruta, newline="", encoding="utf-8") as f:
        return [{"fecha": date.fromisoformat(r["fecha"]),
                 **{c: float(r[c]) for c in COLUMNAS_EQUITY[1:] if r.get(c) not in (None, "")}}
                for r in csv.DictReader(f)]


def escribir_equity(ruta: str | Path, filas: list[dict]) -> None:
    filas = recalcular_indice(sorted(filas, key=lambda r: r["fecha"]))
    salida = [{"fecha": r["fecha"].isoformat(), **{c: f"{r[c]:.2f}" for c in COLUMNAS_EQUITY[1:5]},
               "indice": f"{r['indice']:.6f}"} for r in filas]
    _escribir_csv(ruta, COLUMNAS_EQUITY, salida)


def recalcular_indice(filas: list[dict]) -> list[dict]:
    """Indice time-weighted base 100: I_t = I_{t-1} * (E_t - flujo_t) / E_{t-1}."""
    indice = 100.0
    for i, r in enumerate(filas):
        if i > 0 and filas[i - 1]["equity_mxn"] > EPS:
            flujo = r["aportaciones_netas_mxn"] - filas[i - 1]["aportaciones_netas_mxn"]
            indice *= (r["equity_mxn"] - flujo) / filas[i - 1]["equity_mxn"]
        r["indice"] = indice
    return filas


# ---------------------------------------------------------------- tipo de cambio

def proveedor_fx_yahoo(desde: date | None = None) -> FuncionFX:
    """Funcion fecha -> USD/MXN (cierre en o antes de la fecha), cargada una sola vez."""
    cache: dict = {}

    def fx(fecha: date) -> float:
        if "serie" not in cache:
            cache["serie"] = datos.yahoo_serie(TICKER_FX, rango=_rango_para(desde or fecha - timedelta(days=30)))
        punto = datos.valor_en_o_antes(cache["serie"], fecha) or cache["serie"][0]
        return punto[1]
    return fx


def _rango_para(desde: date) -> str:
    """Rango de Yahoo minimo que cubre desde 'desde' hasta hoy."""
    dias = (date.today() - desde).days + 10
    for rango, limite in (("1mo", 28), ("3mo", 88), ("6mo", 180), ("1y", 362), ("2y", 728),
                          ("5y", 1822), ("10y", 3650)):
        if dias <= limite:
            return rango
    return "max"


# ---------------------------------------------------------------- libro

class Libro:
    """Estado del portafolio al aplicar operaciones en orden cronologico (montos en MXN)."""

    def __init__(self):
        self.efectivo_mxn = 0.0
        self.aportaciones_mxn = 0.0
        self.posiciones: dict[str, dict] = {}
        self.cerradas: list[dict] = []
        self.realizado_mxn: dict[str, float] = {}

    def aplicar(self, op: dict, fx: float = 1.0) -> None:
        """Aplica una operacion; fx = MXN por unidad de la moneda de la operacion."""
        lado, q, precio, com = op["lado"], op["cantidad"], op["precio"], op.get("comision", 0.0) or 0.0
        bruto = q * precio
        if lado == "deposito":
            self.efectivo_mxn += bruto * fx
            self.aportaciones_mxn += bruto * fx
        elif lado == "retiro":
            self.efectivo_mxn -= bruto * fx
            self.aportaciones_mxn -= bruto * fx
        elif lado == "compra":
            p = self.posiciones.setdefault(op["ticker"], {
                "ticker": op["ticker"], "cantidad": 0.0, "costo_mxn": 0.0, "costo_moneda": 0.0,
                "moneda": op["moneda"], "estrategia": "", "tesis_id": "", "stop": None})
            p["cantidad"] += q
            p["costo_mxn"] += (bruto + com) * fx
            p["costo_moneda"] += bruto + com
            for campo in ("estrategia", "tesis_id", "stop"):
                if op.get(campo) not in (None, ""):
                    p[campo] = op[campo]
            self.efectivo_mxn -= (bruto + com) * fx
        elif lado == "venta":
            p = self.posiciones.get(op["ticker"])
            if p is None or q > p["cantidad"] + EPS:
                tenencia = 0 if p is None else p["cantidad"]
                raise ErrorPortafolio(f"Venta de {q} {op['ticker']} excede la posicion ({tenencia}); "
                                      "no se admiten cortos")
            fraccion = q / p["cantidad"]
            costo = p["costo_mxn"] * fraccion
            ingreso = (bruto - com) * fx
            pnl = ingreso - costo
            self.efectivo_mxn += ingreso
            self.cerradas.append({"fecha": op["fecha"], "ticker": op["ticker"], "cantidad": q, "pnl_mxn": pnl,
                                  "rendimiento": pnl / costo if costo else 0.0,
                                  "estrategia": p["estrategia"] or op.get("estrategia", ""),
                                  "tesis_id": p["tesis_id"] or op.get("tesis_id", "")})
            self.realizado_mxn[op["ticker"]] = self.realizado_mxn.get(op["ticker"], 0.0) + pnl
            p["cantidad"] -= q
            p["costo_mxn"] -= costo
            p["costo_moneda"] -= p["costo_moneda"] * fraccion
            if p["cantidad"] <= EPS:
                del self.posiciones[op["ticker"]]
        else:
            raise ErrorPortafolio(f"Lado invalido: {lado}")


def _fx_de(op: dict, fx_hist: FuncionFX | None) -> float:
    if op["moneda"] == "MXN":
        return 1.0
    if fx_hist is None:
        raise ErrorPortafolio("Se requiere tipo de cambio historico para operaciones en USD")
    return fx_hist(op["fecha"])


def construir_libro(operaciones: list[dict], fx_hist: FuncionFX | None = None,
                    hasta: date | None = None) -> Libro:
    """Libro con todas las operaciones con fecha <= hasta."""
    libro = Libro()
    for op in operaciones:
        if hasta is not None and op["fecha"] > hasta:
            break
        libro.aplicar(op, _fx_de(op, fx_hist))
    return libro


def _requiere_fx(operaciones: list[dict]) -> bool:
    return any(op["moneda"] != "MXN" for op in operaciones)


def registrar(ruta: str | Path, fecha, ticker: str, lado: str, cantidad: float, precio: float = 1.0,
              moneda: str = "MXN", comision: float = 0.0, stop: float | None = None, tesis_id: str = "",
              estrategia: str = "", notas: str = "") -> dict:
    """Valida y agrega una operacion al libro (depositos/retiros usan ticker EFECTIVO y precio 1)."""
    lado, moneda = lado.lower(), moneda.upper()
    if lado not in LADOS:
        raise ErrorPortafolio(f"lado debe ser uno de {LADOS}")
    if moneda not in MONEDAS:
        raise ErrorPortafolio(f"moneda debe ser una de {MONEDAS}")
    if lado in ("deposito", "retiro"):
        ticker, precio = TICKER_EFECTIVO, 1.0
    if not ticker:
        raise ErrorPortafolio("ticker obligatorio")
    if cantidad <= 0 or precio <= 0 or comision < 0:
        raise ErrorPortafolio("cantidad y precio positivos; comision >= 0")
    fecha = date.fromisoformat(str(fecha))
    fila = {"fecha": fecha.isoformat(), "ticker": ticker.upper() if lado in ("deposito", "retiro") else ticker,
            "lado": lado, "cantidad": repr(float(cantidad)), "precio": repr(float(precio)), "moneda": moneda,
            "comision": repr(float(comision)), "stop": "" if stop is None else repr(float(stop)),
            "tesis_id": tesis_id, "estrategia": estrategia, "notas": notas}
    ops = leer_operaciones(ruta)
    if lado == "venta":
        tenencia = sum(o["cantidad"] * (1 if o["lado"] == "compra" else -1) for o in ops
                       if o["ticker"] == ticker and o["lado"] in ("compra", "venta") and o["fecha"] <= fecha)
        if cantidad > tenencia + EPS:
            raise ErrorPortafolio(f"Venta de {cantidad} {ticker} excede la posicion ({tenencia}); no se admiten cortos")
    asegurar_archivo(ruta, COLUMNAS_OPS)
    with open(ruta, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=COLUMNAS_OPS).writerow(fila)
    return fila


def validar_contra_libro(operaciones: list[dict], orden: dict, fx_hist: FuncionFX | None,
                         clase: str = "otro", fase: int = 1, parametros: dict | None = None) -> dict:
    """Valida una compra/venta con riesgo.validar_orden usando el libro valuado A COSTO.

    Tactica = estrategia distinta de '' y 'nucleo'. Sin precios de mercado ni P&L del
    periodo: revisa apalancamiento bruto, satelite, riesgo al stop y limites por clase.
    """
    libro = construir_libro(operaciones, fx_hist)
    capital = libro.efectivo_mxn + sum(p["costo_mxn"] for p in libro.posiciones.values())
    if capital <= 0:
        raise ErrorPortafolio("Capital nulo o negativo: registre primero un deposito")
    posiciones = {t: {"valor_mxn": p["costo_mxn"], "clase": "otro",
                      "tactica": p["estrategia"] not in ("", "nucleo")} for t, p in libro.posiciones.items()}
    fx = 1.0 if orden["moneda"] == "MXN" else fx_hist(orden["fecha"])
    return riesgo.validar_orden(
        {"capital": capital, "fase": fase, "posiciones": posiciones},
        {"ticker": orden["ticker"], "lado": orden["lado"], "cantidad": orden["cantidad"], "precio": orden["precio"],
         "tipo_cambio": fx, "clase": clase, "tactica": orden.get("estrategia", "") not in ("", "nucleo"),
         "stop": orden.get("stop")}, parametros)


# ---------------------------------------------------------------- valuacion

def precios_mercado(tickers: list[str]) -> tuple[dict, list[str]]:
    """{ticker: (fecha, precio, moneda, tipo_instrumento)} desde Yahoo, y lista de errores."""
    precios, errores = {}, []
    for t in tickers:
        try:
            g = datos.yahoo_grafica(t, "5d", "1d")
            fecha, precio = g["serie"][-1]
            precios[t] = (fecha, precio, str(g["meta"].get("currency", "")).upper(),
                          str(g["meta"].get("instrumentType", "")).upper())
        except datos.ErrorDatos as e:
            errores.append(f"{t}: {e}")
    return precios, errores


def valuar_libro(libro: Libro, precios: dict, fx_actual: float) -> dict:
    """Valuacion a mercado en MXN. precios: {ticker: (fecha, precio, moneda[, tipo])}."""
    filas, faltantes = [], []
    total = 0.0
    for t, p in sorted(libro.posiciones.items()):
        if t not in precios:
            faltantes.append(t)
            valor = p["costo_mxn"]  # sin precio: se valua a costo y se reporta
            precio, moneda, fecha = None, p["moneda"], None
        else:
            fecha, precio, moneda = precios[t][0], precios[t][1], (precios[t][2] or p["moneda"])
            valor = p["cantidad"] * precio * (fx_actual if moneda == "USD" else 1.0)
        total += valor
        filas.append({"ticker": t, "cantidad": p["cantidad"], "moneda": moneda, "precio": precio,
                      "fecha_precio": fecha, "costo_promedio": p["costo_moneda"] / p["cantidad"],
                      "costo_mxn": p["costo_mxn"], "valor_mxn": valor, "pnl_no_realizado_mxn": valor - p["costo_mxn"],
                      "estrategia": p["estrategia"], "stop": p["stop"],
                      "tipo": precios[t][3] if t in precios and len(precios[t]) > 3 else ""})
    equity = libro.efectivo_mxn + total
    for f in filas:
        f["peso"] = f["valor_mxn"] / equity if equity > EPS else 0.0
    return {"filas": filas, "efectivo_mxn": libro.efectivo_mxn, "posiciones_mxn": total, "equity_mxn": equity,
            "aportaciones_netas_mxn": libro.aportaciones_mxn, "faltantes": faltantes,
            "pnl_realizado_mxn": sum(libro.realizado_mxn.values())}


def guardar_snapshot(ruta: str | Path, fecha: date, valuacion: dict) -> list[dict]:
    """Inserta o reemplaza la fila de 'fecha' en equity.csv y recalcula el indice."""
    filas = [r for r in leer_equity(ruta) if r["fecha"] != fecha]
    filas.append({"fecha": fecha, "efectivo_mxn": valuacion["efectivo_mxn"],
                  "posiciones_mxn": valuacion["posiciones_mxn"], "equity_mxn": valuacion["equity_mxn"],
                  "aportaciones_netas_mxn": valuacion["aportaciones_netas_mxn"]})
    escribir_equity(ruta, filas)
    return leer_equity(ruta)


def reconstruir_equity(operaciones: list[dict], series: dict, monedas: dict, fx_hist: FuncionFX,
                       hasta: date | None = None) -> list[dict]:
    """Curva diaria desde la primera operacion con cierres historicos.

    series: {ticker: [(fecha, cierre)]}; monedas: {ticker: 'USD'|'MXN'}.
    """
    if not operaciones:
        return []
    hasta = hasta or date.today()
    inicio = operaciones[0]["fecha"]
    fechas = {op["fecha"] for op in operaciones}
    for s in series.values():
        fechas.update(f for f, _ in s if inicio <= f <= hasta)
    libro, i, filas = Libro(), 0, []
    for d in sorted(f for f in fechas if f <= hasta):
        while i < len(operaciones) and operaciones[i]["fecha"] <= d:
            libro.aplicar(operaciones[i], _fx_de(operaciones[i], fx_hist))
            i += 1
        valor = 0.0
        for t, p in libro.posiciones.items():
            punto = datos.valor_en_o_antes(series.get(t, []), d)
            if punto is None:
                valor += p["costo_mxn"]
            else:
                valor += p["cantidad"] * punto[1] * (fx_hist(d) if monedas.get(t, p["moneda"]) == "USD" else 1.0)
        filas.append({"fecha": d, "efectivo_mxn": libro.efectivo_mxn, "posiciones_mxn": valor,
                      "equity_mxn": libro.efectivo_mxn + valor, "aportaciones_netas_mxn": libro.aportaciones_mxn})
    return recalcular_indice(filas)


# ---------------------------------------------------------------- benchmark

def tasa_cetes_proxy(desde: date) -> list[tuple[date, float]]:
    """Serie mensual FRED INTGSTMXM193N (% anual) como proxy de CETES 28 dias."""
    return datos.fred_serie(SERIE_CETES_PROXY, desde=desde - timedelta(days=120))


def serie_benchmark(desde: date, hasta: date | None = None, tasa_cetes: float | None = None,
                    spx_tr: list | None = None, fx: list | None = None,
                    cetes: list | None = None) -> list[tuple[date, float]]:
    """Indice base 100 del benchmark principal: 50% S&P 500 TR en MXN + 50% CETES, rebalanceo diario.

    CETES devenga tasa*dias/360 (convencion de mercado de dinero MX). tasa_cetes (anual,
    0.07 = 7%) fija una tasa constante; si no, se usa el proxy mensual de FRED.
    """
    hasta = hasta or date.today()
    rango = _rango_para(desde - timedelta(days=10))
    spx_tr = spx_tr if spx_tr is not None else datos.yahoo_serie(TICKER_SPX_TR, rango=rango)
    fx = fx if fx is not None else datos.yahoo_serie(TICKER_FX, rango=rango)
    if tasa_cetes is None and cetes is None:
        cetes = tasa_cetes_proxy(desde)

    def tasa(d: date) -> float:
        if tasa_cetes is not None:
            return tasa_cetes
        punto = datos.valor_en_o_antes(cetes, d) or cetes[0]
        return punto[1] / 100

    indice, previo, salida = 100.0, None, []
    for d, v in spx_tr:
        if d > hasta:
            break
        punto_fx = datos.valor_en_o_antes(fx, d)
        if punto_fx is None:
            continue
        valor_mxn = v * punto_fx[1]
        if d < desde:
            previo = (d, valor_mxn)
            continue
        if previo is not None:
            r_eq = valor_mxn / previo[1] - 1
            r_cetes = tasa(previo[0]) * (d - previo[0]).days / 360
            indice *= 1 + 0.5 * r_eq + 0.5 * r_cetes
        salida.append((d, indice))
        previo = (d, valor_mxn)
    return salida


# ---------------------------------------------------------------- reporte

def _periodos_por_anio(fechas: list[date]) -> float:
    anios = (fechas[-1] - fechas[0]).days / 365.25
    return (len(fechas) - 1) / anios if anios > 0 else 252.0


def metricas_curva(curva: list[tuple[date, float]], rf: float = 0.0) -> dict:
    """Metricas de una curva (fecha, valor); CAGR solo con >= 1 anio; ratios con >= 20 rendimientos."""
    fechas = [f for f, _ in curva]
    rends = metricas.rendimientos(curva)
    dias = (fechas[-1] - fechas[0]).days
    ppa = _periodos_por_anio(fechas)
    r = {"inicio": fechas[0], "fin": fechas[-1], "dias": dias, "n_rend": len(rends),
         "rendimiento_total": curva[-1][1] / curva[0][1] - 1,
         "cagr": metricas.cagr(curva) if dias >= 365 else None,
         "max_drawdown": metricas.max_drawdown(curva)["valor"], "ppa": ppa,
         "volatilidad": None, "sharpe": None, "sortino": None, "calmar": None}
    if len(rends) >= MIN_OBS_METRICAS:
        r["volatilidad"] = metricas.volatilidad_anualizada(rends, round(ppa))
        r["sharpe"] = metricas.sharpe(rends, rf, round(ppa))
        r["sortino"] = metricas.sortino(rends, rf, round(ppa))
    if r["cagr"] is not None and r["max_drawdown"] < 0:
        r["calmar"] = r["cagr"] / abs(r["max_drawdown"])
    return r


def _fmt(x, formato="{:+.2%}") -> str:
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "n/d"
    return formato.format(x)


def construir_reporte(operaciones: list[dict], equity: list[dict], libro: Libro,
                      benchmark: list[tuple[date, float]] | None, rf: float | None,
                      notas_datos: list[str], parametros: dict | None = None) -> str:
    """Reporte markdown: resumen, metricas vs benchmark, cortacircuitos, operaciones y rachas."""
    lineas = [f"# Reporte de portafolio en papel - {date.today().isoformat()}", ""]
    if not equity:
        lineas.append("Sin curva de equity: ejecute `portafolio.py valuar` (o `valuar --reconstruir`).")
        return "\n".join(lineas) + "\n"
    ultimo = equity[-1]
    lineas += [
        f"- Equity: {ultimo['equity_mxn']:,.2f} MXN (efectivo {ultimo['efectivo_mxn']:,.2f}; "
        f"posiciones {ultimo['posiciones_mxn']:,.2f}) al {ultimo['fecha']}",
        f"- Aportaciones netas: {ultimo['aportaciones_netas_mxn']:,.2f} MXN; P&L total "
        f"{ultimo['equity_mxn'] - ultimo['aportaciones_netas_mxn']:,.2f} MXN",
        f"- P&L realizado acumulado: {sum(libro.realizado_mxn.values()):,.2f} MXN",
        f"- Benchmark principal (parametros): {obtener('objetivo.benchmark_principal')}",
        f"- Tasa libre de riesgo usada en Sharpe/Sortino: {_fmt(rf, '{:.2%}')} anual",
        "",
    ]
    curva = [(r["fecha"], r["indice"]) for r in equity]
    if len(curva) < 2:
        lineas.append("Un solo punto en la curva de equity: metricas no disponibles todavia.")
    else:
        mp = metricas_curva(curva, rf or 0.0)
        mb = None
        if benchmark:
            alineada = []
            for f, _ in curva:
                punto = datos.valor_en_o_antes(benchmark, f)
                if punto is not None:
                    alineada.append((f, punto[1]))
            if len(alineada) == len(curva):
                mb = metricas_curva(alineada, rf or 0.0)
                rp = metricas.rendimientos(curva)
                rb = metricas.rendimientos(alineada)
                activos = [a - b for a, b in zip(rp, rb)]
                if len(activos) >= MIN_OBS_METRICAS:
                    te = metricas.volatilidad_anualizada(activos, round(mp["ppa"]))
                    mb["tracking_error"] = te
                    mb["ir"] = (sum(activos) / len(activos) * mp["ppa"]) / te if te > 0 else None
        lineas += [f"## Metricas ({mp['inicio']} a {mp['fin']}, {mp['dias']} dias, {mp['n_rend']} rendimientos)", "",
                   "| Metrica | Portafolio | Benchmark | Diferencia |", "|---|---|---|---|"]
        for clave, nombre, formato in (("rendimiento_total", "Rendimiento del periodo", "{:+.2%}"),
                                       ("cagr", "CAGR (solo >= 1 anio)", "{:+.2%}"),
                                       ("volatilidad", "Volatilidad anual", "{:.2%}"),
                                       ("sharpe", "Sharpe", "{:.2f}"), ("sortino", "Sortino", "{:.2f}"),
                                       ("max_drawdown", "Max drawdown", "{:.2%}"), ("calmar", "Calmar", "{:.2f}")):
            a = mp.get(clave)
            b = mb.get(clave) if mb else None
            dif = (a - b) if (a is not None and b is not None) else None
            lineas.append(f"| {nombre} | {_fmt(a, formato)} | {_fmt(b, formato)} | {_fmt(dif, formato)} |")
        if mb and "tracking_error" in mb:
            lineas.append(f"| Tracking error / IR | {_fmt(mb['tracking_error'], '{:.2%}')} | "
                          f"IR {_fmt(mb['ir'], '{:.2f}')} | |")
        if mp["n_rend"] < MIN_OBS_METRICAS:
            lineas.append(f"\nMenos de {MIN_OBS_METRICAS} rendimientos: volatilidad y ratios no se calculan.")
        if not mb:
            lineas.append("\nBenchmark no disponible para todas las fechas de la curva.")
        cc = riesgo.estado_cortacircuitos(curva, parametros)
        perfil = (parametros or {}).get("perfil_activo", "estandar")
        lineas += ["", f"## Cortacircuitos (perfil {perfil}, sobre indice time-weighted)", "",
                   f"- Drawdown actual: {cc['drawdown_actual']:.2%} desde el pico del {cc['fecha_pico']}",
                   f"- Nivel activado: {_fmt(cc['nivel_activado'], '{:.0%}')} -> {cc['accion']}",
                   f"- Siguiente nivel: {_fmt(cc['siguiente_nivel'], '{:.0%}')} "
                   f"(margen {_fmt(cc['distancia_siguiente'], '{:.2%}')})"]
    tope = riesgo.estado_tope_perdida(ultimo["equity_mxn"], ultimo["aportaciones_netas_mxn"], parametros)
    if tope.get("aplica"):
        lineas += ["", "## Tope absoluto de perdida del dueno", "",
                   f"- P&L vs aportaciones: {tope['pnl_mxn']:,.2f} MXN; tope -{tope['tope_mxn']:,.0f} MXN; "
                   f"margen {tope['margen_mxn']:,.2f} MXN",
                   f"- Estado: {'ACTIVADO -> ' + tope['accion'] if tope['activado'] else 'no activado'}"]
    cerradas = libro.cerradas
    lineas += ["", "## Operaciones cerradas", ""]
    if not cerradas:
        lineas.append("Sin operaciones cerradas.")
    else:
        pnl = [c["pnl_mxn"] for c in cerradas]
        lineas += [f"- n = {len(pnl)}; hit rate {metricas.hit_rate(pnl):.1%}; profit factor "
                   f"{_fmt(metricas.profit_factor(pnl), '{:.2f}')}; expectancy {metricas.expectancy(pnl):,.2f} MXN",
                   f"- Racha perdedora maxima observada: {metricas.racha_perdedora_observada(pnl)}", "",
                   "| Estrategia | n | Hit rate | Expectancy MXN | Estado rachas | Factor |", "|---|---|---|---|---|---|"]
        for est in sorted({c["estrategia"] or "(sin estrategia)" for c in cerradas}):
            sub = [c["pnl_mxn"] for c in cerradas if (c["estrategia"] or "(sin estrategia)") == est]
            fr = riesgo.factor_por_rachas(sub, parametros)
            lineas.append(f"| {est} | {len(sub)} | {metricas.hit_rate(sub):.1%} | {metricas.expectancy(sub):,.2f} | "
                          f"{fr['estado']} | {fr['factor']:.2f} |")
    vp = obtener("validacion_estrategias")
    meses = (equity[-1]["fecha"] - equity[0]["fecha"]).days / 30.44
    lineas += ["", "## Requisitos de paper trading (parametros.validacion_estrategias)", "",
               f"- Meses de track record: {meses:.1f} / {vp['paper_trading_min_meses']}",
               f"- Operaciones cerradas: {len(cerradas)} / {vp['paper_trading_min_operaciones']}"]
    if notas_datos:
        lineas += ["", "## Notas de datos", ""] + [f"- {n}" for n in notas_datos]
    return "\n".join(lineas) + "\n"


# ---------------------------------------------------------------- CLI

def _tabla_posiciones(filas: list[dict], con_mercado: bool) -> str:
    if not filas:
        return "(sin posiciones abiertas)"
    if con_mercado:
        cab = "| Ticker | Cantidad | Moneda | Costo prom | Precio | Fecha precio | Valor MXN | Peso | P&L no realizado MXN |"
        salida = [cab, "|---|---|---|---|---|---|---|---|---|"]
        for f in filas:
            salida.append(f"| {f['ticker']} | {f['cantidad']:g} | {f['moneda']} | {f['costo_promedio']:,.4f} | "
                          f"{_fmt(f['precio'], '{:,.4f}')} | {f['fecha_precio'] or 'n/d'} | {f['valor_mxn']:,.2f} | "
                          f"{f['peso']:.1%} | {f['pnl_no_realizado_mxn']:,.2f} |")
    else:
        salida = ["| Ticker | Cantidad | Moneda | Costo prom | Costo MXN | Estrategia | Stop |", "|---|---|---|---|---|---|---|"]
        for f in filas:
            salida.append(f"| {f['ticker']} | {f['cantidad']:g} | {f['moneda']} | {f['costo_moneda'] / f['cantidad']:,.4f} | "
                          f"{f['costo_mxn']:,.2f} | {f['estrategia']} | {_fmt(f['stop'], '{:,.4f}')} |")
    return "\n".join(salida)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Portafolio en papel")
    ap.add_argument("--operaciones", default=str(RUTA_OPS))
    ap.add_argument("--equity", default=str(RUTA_EQUITY))
    ap.add_argument("--perfil", default="arena_agresivo", choices=("arena_agresivo", "cripto_binance", "estandar"),
                    help="perfil de riesgo de la cuenta del libro (por defecto la arena de GBM)")
    sub = ap.add_subparsers(dest="comando", required=True)
    r = sub.add_parser("registrar", help="agregar operacion al libro")
    r.add_argument("--fecha", default=date.today().isoformat())
    r.add_argument("--ticker", default=TICKER_EFECTIVO)
    r.add_argument("--lado", required=True, choices=LADOS)
    r.add_argument("--cantidad", type=float, required=True, help="unidades; en deposito/retiro, monto")
    r.add_argument("--precio", type=float, default=1.0)
    r.add_argument("--moneda", default="MXN", choices=MONEDAS)
    r.add_argument("--comision", type=float, default=0.0)
    r.add_argument("--stop", type=float, default=None)
    r.add_argument("--tesis-id", default="")
    r.add_argument("--estrategia", default="")
    r.add_argument("--notas", default="")
    r.add_argument("--clase", default="otro", choices=sorted(riesgo.CLASES_VALIDAS),
                   help="clase del activo para limites de concentracion")
    r.add_argument("--fase", type=int, default=1, help="fase del sistema para el tope de apalancamiento")
    r.add_argument("--forzar", action="store_true",
                   help="registra aunque viole limites (queda marcado en notas)")
    sub.add_parser("posiciones", help="posiciones a costo")
    v = sub.add_parser("valuar", help="valuacion a mercado y snapshot en equity.csv")
    v.add_argument("--reconstruir", action="store_true", help="reconstruye equity.csv diario desde la 1a operacion")
    v.add_argument("--sin-guardar", action="store_true")
    v.add_argument("--fecha", default=None, help="fecha del snapshot (por defecto hoy)")
    p = sub.add_parser("reporte", help="metricas vs benchmark, cortacircuitos y rachas")
    p.add_argument("--tasa-cetes", type=float, default=None, help="tasa anual constante (0.07); si no, proxy FRED")
    p.add_argument("--salida", default=None)
    args = ap.parse_args(argv)
    params = parametros_efectivos(args.perfil)

    try:
        if args.comando == "registrar":
            notas = args.notas
            if args.lado in ("compra", "venta"):
                previas = leer_operaciones(args.operaciones)
                orden = {"fecha": date.fromisoformat(args.fecha), "ticker": args.ticker, "lado": args.lado,
                         "cantidad": args.cantidad, "precio": args.precio, "moneda": args.moneda,
                         "stop": args.stop, "estrategia": args.estrategia}
                usa_usd = args.moneda != "MXN" or _requiere_fx(previas)
                inicio = min([o["fecha"] for o in previas] + [orden["fecha"]])
                val = validar_contra_libro(previas, orden, proveedor_fx_yahoo(inicio) if usa_usd else None,
                                           args.clase, args.fase, params)
                for a in val["advertencias"]:
                    print(f"Advertencia: {a}")
                if val["violaciones"]:
                    for v in val["violaciones"]:
                        print(f"VIOLACION: {v}", file=sys.stderr)
                    if not args.forzar:
                        print("Operacion NO registrada (use --forzar para registrarla marcada).", file=sys.stderr)
                        return 2
                    notas = (notas + " | FORZADA: " + "; ".join(val["violaciones"])).strip(" |")
            fila = registrar(args.operaciones, args.fecha, args.ticker, args.lado, args.cantidad, args.precio,
                             args.moneda, args.comision, args.stop, args.tesis_id, args.estrategia, notas)
            print(f"Registrado: {fila['fecha']} {fila['lado']} {fila['cantidad']} {fila['ticker']} @ "
                  f"{fila['precio']} {fila['moneda']}")
            return 0
        ops = leer_operaciones(args.operaciones)
        fx_hist = proveedor_fx_yahoo(ops[0]["fecha"]) if ops and _requiere_fx(ops) else None
        libro = construir_libro(ops, fx_hist)
        if args.comando == "posiciones":
            print(_tabla_posiciones(list(libro.posiciones.values()), False))
            print(f"\nEfectivo: {libro.efectivo_mxn:,.2f} MXN | Aportaciones netas: {libro.aportaciones_mxn:,.2f} MXN"
                  f" | P&L realizado: {sum(libro.realizado_mxn.values()):,.2f} MXN")
        elif args.comando == "valuar":
            tickers = sorted(libro.posiciones)
            precios, errores = precios_mercado(tickers)
            necesita_fx = any(p[2] == "USD" for p in precios.values()) or _requiere_fx(ops)
            fx_actual = datos.yahoo_ultimo(TICKER_FX)[1] if necesita_fx else 1.0
            val = valuar_libro(libro, precios, fx_actual)
            print(_tabla_posiciones(val["filas"], True))
            print(f"\nUSD/MXN {fx_actual:.4f} | Efectivo {val['efectivo_mxn']:,.2f} | Posiciones "
                  f"{val['posiciones_mxn']:,.2f} | Equity {val['equity_mxn']:,.2f} MXN")
            for e in errores:
                print(f"Error de precio (valuado a costo): {e}")
            if args.reconstruir and ops:
                rango = _rango_para(ops[0]["fecha"])
                series, monedas = {}, {}
                for t in {o["ticker"] for o in ops if o["lado"] in ("compra", "venta")}:
                    g = datos.yahoo_grafica(t, rango, "1d")
                    series[t], monedas[t] = g["serie"], str(g["meta"].get("currency", "")).upper()
                fx_fn = fx_hist or proveedor_fx_yahoo(ops[0]["fecha"])
                filas = reconstruir_equity(ops, series, monedas, fx_fn)
                if not args.sin_guardar:
                    escribir_equity(args.equity, filas)
                    print(f"equity.csv reconstruido: {len(filas)} filas")
            elif not args.sin_guardar:
                fecha = date.fromisoformat(args.fecha) if args.fecha else date.today()
                guardar_snapshot(args.equity, fecha, val)
                print(f"Snapshot {fecha} guardado en {args.equity}")
        elif args.comando == "reporte":
            equity = leer_equity(args.equity)
            notas, bench, rf = [], None, args.tasa_cetes
            if equity:
                try:
                    cetes = None if args.tasa_cetes is not None else tasa_cetes_proxy(equity[0]["fecha"])
                    bench = serie_benchmark(equity[0]["fecha"], tasa_cetes=args.tasa_cetes, cetes=cetes)
                    if rf is None and cetes:
                        rf = cetes[-1][1] / 100
                        notas.append(f"rf y CETES = proxy FRED {SERIE_CETES_PROXY} (T-bills Mexico, FMI, mensual); "
                                     f"ultimo dato {cetes[-1][0]} = {cetes[-1][1]:.2f}%")
                    notas.append("S&P 500 TR = Yahoo ^SP500TR convertido con MXN=X; rebalanceo diario 50/50")
                except datos.ErrorDatos as e:
                    notas.append(f"Benchmark no disponible: {e}")
            texto = construir_reporte(ops, equity, libro, bench, rf, notas, params)
            if args.salida:
                Path(args.salida).parent.mkdir(parents=True, exist_ok=True)
                Path(args.salida).write_text(texto, encoding="utf-8")
                print(f"Reporte escrito en {args.salida}")
            else:
                print(texto)
    except (ErrorPortafolio, datos.ErrorDatos, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
