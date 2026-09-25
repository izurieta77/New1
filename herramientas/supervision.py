"""Supervision barata y determinista de la cuenta arena (papel y real) para corridas frecuentes.

Uso:
    python3 herramientas/supervision.py            # con precios de Yahoo
    python3 herramientas/supervision.py --sin-red  # solo archivos (latidos, pendientes, bloqueos)

Revisa, con el perfil arena_agresivo:
- cada libro (GBM papel: bitacora/operaciones.csv; GBM real: bitacora/real/; Binance papel y real:
  bitacora/papel-binance/ y bitacora/real-binance/, con el perfil cripto_binance): cortacircuitos
  sobre el indice time-weighted (con un punto intradia), tope absoluto de perdida y stops por posicion;
- filtro de apalancados: subyacente sobre su SMA200 y VIX < 25;
- ordenes pendientes vencidas, latido mas reciente, bloqueos y dudas abiertas.
Codigo de salida: 0 = OK, 1 = AVISO, 2 = ALERTA.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Callable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from herramientas import datos, portafolio, riesgo
from herramientas.parametros import DIR_BITACORA, parametros_efectivos

OK, AVISO, ALERTA = 0, 1, 2
NOMBRE = {OK: "OK", AVISO: "AVISO", ALERTA: "ALERTA"}
# ETF apalancado -> indice subyacente para el filtro SMA200.
APALANCADOS = {"SPXL": "^GSPC", "UPRO": "^GSPC", "SSO": "^GSPC", "TQQQ": "^NDX", "QLD": "^NDX",
               "SOXL": "^SOX", "TNA": "^RUT", "UDOW": "^DJI", "TECL": "^NDX"}
VIX_MAX = 25.0
SMA_DIAS = 200
LATIDO_MAX_HORAS = {True: 26.0, False: 74.0}  # dia habil / fin de semana
RE_LATIDO = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC · ([^·]+?) ·")

Precios = Callable[[list[str]], tuple[dict, list[str]]]
Serie = Callable[[str], list[tuple[date, float]]]
FabricaFX = Callable[[date], Callable[[date], float]]  # desde -> fx historico USD/MXN


def _base_ticker(t: str) -> str:
    return t.upper().split(".")[0]


def sma(valores: list[float], n: int = SMA_DIAS) -> float | None:
    return sum(valores[-n:]) / n if len(valores) >= n else None


def revisar_libro(nombre: str, ruta_ops: Path, ruta_equity: Path, params: dict, precios: Precios,
                  fx_actual: float | None, fabrica_fx: FabricaFX | None) -> tuple[list[tuple[int, str]], list[str]]:
    """Cortacircuitos, tope absoluto y stops de un libro. Devuelve ([(nivel, texto)], tickers)."""
    if not ruta_ops.exists():
        return [(OK, f"{nombre}: sin libro ({ruta_ops.name} no existe)")], []
    ops = portafolio.leer_operaciones(ruta_ops)
    if not ops:
        return [(OK, f"{nombre}: libro vacío")], []
    fx_hist = None
    if any(o["moneda"] == "USD" for o in ops):
        if fabrica_fx is None:
            return [(AVISO, f"{nombre}: hay operaciones en USD y no hay tipo de cambio histórico")], []
        fx_hist = fabrica_fx(min(o["fecha"] for o in ops))
    libro = portafolio.construir_libro(ops, fx_hist)
    if not libro.posiciones:
        return [(OK, f"{nombre}: sin posiciones; efectivo {libro.efectivo_mxn:,.0f} MXN")], []
    px, errores = precios(sorted(libro.posiciones))
    val = portafolio.valuar_libro(libro, px, fx_actual or 1.0)
    salida: list[tuple[int, str]] = [(AVISO, f"{nombre}: sin precio de {e}") for e in errores]
    # Stops por posicion (precio en la moneda del instrumento).
    for f in val["filas"]:
        if f["stop"] is None or f["precio"] is None:
            continue
        dist = f["precio"] / f["stop"] - 1
        if f["precio"] <= f["stop"]:
            salida.append((ALERTA, f"{nombre}: {f['ticker']} en {f['precio']:.2f} tocó su stop {f['stop']:.2f}"))
        elif dist < 0.02:
            salida.append((AVISO, f"{nombre}: {f['ticker']} a {dist:.1%} de su stop {f['stop']:.2f}"))
    # Tope absoluto del dueno.
    tope = riesgo.estado_tope_perdida(val["equity_mxn"], val["aportaciones_netas_mxn"], params)
    if tope.get("aplica"):
        nivel = ALERTA if tope["activado"] else (AVISO if tope["margen_mxn"] < 0.2 * tope["tope_mxn"] else OK)
        salida.append((nivel, f"{nombre}: P&L {tope['pnl_mxn']:,.0f} MXN; tope -{tope['tope_mxn']:,.0f} "
                              f"(margen {tope['margen_mxn']:,.0f})"))
    # Cortacircuitos sobre el indice TWR con un punto intradia (solo si no hubo flujos desde el ultimo snapshot).
    equity = portafolio.leer_equity(ruta_equity) if ruta_equity.exists() else []
    curva = [(r["fecha"], r["indice"]) for r in equity]
    if equity and abs(equity[-1]["aportaciones_netas_mxn"] - val["aportaciones_netas_mxn"]) < 0.01 \
            and equity[-1]["equity_mxn"] > 0:
        curva.append((date.today(), equity[-1]["indice"] * val["equity_mxn"] / equity[-1]["equity_mxn"]))
    if len(curva) >= 1:
        cc = riesgo.estado_cortacircuitos(curva, params)
        nivel = ALERTA if cc["nivel_activado"] is not None else OK
        salida.append((nivel, f"{nombre}: drawdown {cc['drawdown_actual']:.1%}; "
                              f"{'ACTIVADO ' + format(cc['nivel_activado'], '.0%') + ' -> ' + cc['accion'] if nivel else 'sin cortacircuitos'}"))
    salida.append((OK, f"{nombre}: equity {val['equity_mxn']:,.0f} MXN ({len(libro.posiciones)} posiciones)"))
    return salida, list(libro.posiciones)


def revisar_filtro_apalancados(tickers: list[str], serie: Serie, vix: float | None) -> list[tuple[int, str]]:
    salida = []
    for t in sorted({_base_ticker(t) for t in tickers if _base_ticker(t) in APALANCADOS}):
        sub = APALANCADOS[t]
        valores = [v for _, v in serie(sub)]
        m = sma(valores)
        if m is None or vix is None:
            salida.append((AVISO, f"filtro {t}: sin datos suficientes de {sub} o VIX"))
            continue
        ok = valores[-1] > m and vix < VIX_MAX
        salida.append((OK if ok else ALERTA, f"filtro {t}: {sub} {valores[-1]:,.0f} vs SMA200 {m:,.0f}; "
                                             f"VIX {vix:.1f} -> {'se cumple' if ok else 'ROTO: vender según perfil'}"))
    return salida


def revisar_pendientes(ruta: Path, hoy: date) -> list[tuple[int, str]]:
    if not ruta.exists():
        return []
    with open(ruta, encoding="utf-8") as f:
        filas = [r for r in csv.DictReader(f) if r.get("estado", "").strip() == "pendiente"]
    vencidas = [r for r in filas if r.get("fecha_ejecucion") and date.fromisoformat(r["fecha_ejecucion"]) < hoy]
    salida = [(AVISO, f"orden pendiente vencida: {r.get('id')} {r.get('lado')} {r.get('ticker')} "
                      f"(debió ejecutarse el {r['fecha_ejecucion']})") for r in vencidas]
    if filas and not vencidas:
        salida.append((OK, f"{len(filas)} órdenes pendientes en fecha"))
    return salida


def revisar_latidos(ruta: Path, ahora: datetime) -> list[tuple[int, str]]:
    if not ruta.exists():
        return [(AVISO, "sin bitacora/estado-rutinas.md")]
    fechas = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        m = RE_LATIDO.match(linea.strip())
        if m:
            fechas.append((datetime.strptime(m.group(1), "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc),
                           m.group(2).strip()))
    if not fechas:
        return [(AVISO, "sin latidos legibles en estado-rutinas.md")]
    ultima, rutina = max(fechas)
    horas = (ahora - ultima).total_seconds() / 3600
    limite = LATIDO_MAX_HORAS[ahora.weekday() < 5]
    return [(AVISO if horas > limite else OK, f"último latido hace {horas:.1f} h ({rutina})")]


def contar_abiertos(ruta: Path) -> int:
    """Filas de tabla markdown cuyo Estado no dice cerrado/cerrada (encabezado y separador excluidos)."""
    if not ruta.exists():
        return 0
    filas = [l for l in ruta.read_text(encoding="utf-8").splitlines() if l.startswith("|")]
    if len(filas) < 3:
        return 0
    return sum(1 for l in filas[2:] if "cerrad" not in l.split("|")[-2].lower())


def libros(bitacora: Path, params: dict, params_cripto: dict | None) -> list[tuple[str, Path, Path, dict]]:
    """(nombre, operaciones, equity, parametros) de cada libro supervisado."""
    salida = [("papel", bitacora / "operaciones.csv", bitacora / "equity.csv", params),
              ("real", bitacora / "real" / "operaciones.csv", bitacora / "real" / "equity.csv", params)]
    if params_cripto is not None:
        for nombre, carpeta in (("papel-binance", "papel-binance"), ("real-binance", "real-binance")):
            salida.append((nombre, bitacora / carpeta / "operaciones.csv", bitacora / carpeta / "equity.csv",
                           params_cripto))
    return salida


def supervisar(ahora: datetime, params: dict, precios: Precios | None, serie: Serie | None,
               vix: float | None, fx_actual: float | None, fabrica_fx: FabricaFX | None = None,
               bitacora: Path = DIR_BITACORA, params_cripto: dict | None = None) -> list[tuple[int, str]]:
    salida: list[tuple[int, str]] = []
    tickers: list[str] = []
    if precios is not None:
        for nombre, ops, eq, prm in libros(bitacora, params, params_cripto):
            lineas, tks = revisar_libro(nombre, ops, eq, prm, precios, fx_actual, fabrica_fx)
            salida += lineas
            tickers += tks
        if serie is not None:
            salida += revisar_filtro_apalancados(tickers, serie, vix)
    salida += revisar_pendientes(bitacora / "ordenes-pendientes.csv", ahora.date())
    salida += revisar_latidos(bitacora / "estado-rutinas.md", ahora)
    for archivo, etiqueta in (("bloqueos.md", "bloqueos abiertos"), ("decisiones-pendientes.md", "dudas abiertas")):
        n = contar_abiertos(bitacora / archivo)
        if n:
            salida.append((AVISO, f"{n} {etiqueta} en bitacora/{archivo}"))
    return salida


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Supervision de la cuenta arena")
    ap.add_argument("--sin-red", action="store_true", help="no consulta precios (solo archivos)")
    args = ap.parse_args(argv)
    params = parametros_efectivos("arena_agresivo")
    ahora = datetime.now(timezone.utc)
    precios = serie = None
    vix = fx = None
    if not args.sin_red:
        precios = portafolio.precios_mercado
        serie = lambda t: datos.yahoo_serie(t, "2y", "1d")  # noqa: E731
        try:
            vix = datos.yahoo_ultimo("^VIX")[1]
            fx = datos.yahoo_ultimo(portafolio.TICKER_FX)[1]
        except datos.ErrorDatos as e:
            print(f"AVISO · datos de mercado no disponibles: {e}")
    salida = supervisar(ahora, params, precios, serie, vix, fx,
                        None if args.sin_red else portafolio.proveedor_fx_yahoo,
                        params_cripto=parametros_efectivos("cripto_binance"))
    peor = max([n for n, _ in salida], default=OK)
    print(f"{ahora:%Y-%m-%d %H:%M} UTC · supervisión · {NOMBRE[peor]}")
    for nivel, texto in sorted(salida, key=lambda x: -x[0]):
        print(f"{NOMBRE[nivel]} · {texto}")
    return peor


if __name__ == "__main__":
    sys.exit(main())
