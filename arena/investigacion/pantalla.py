"""Pantalla cuantitativa de momentum en MXN para la cuenta arena (solo biblioteca estandar).

Uso:
    python3 arena/investigacion/pantalla.py --salida arena/investigacion/pantalla-AAAA-MM-DD.csv
    python3 arena/investigacion/pantalla.py --salida out.csv --markdown   # tablas en stdout
    python3 arena/investigacion/pantalla.py --salida out.csv --corte 2026-09-24 --cache-horas 0

Fuente: Yahoo Finance chart v8 (cierre ajustado por splits y dividendos cuando existe),
via herramientas/datos.py. Tipo de cambio: MXN=X (MXN por USD), mismo endpoint.

Metodo (todo sobre la serie en MXN):
  * Serie USD -> MXN: precio_usd(d) * USDMXN(ultimo dato <= d). Series .MX ya estan en MXN.
  * Corte: ultimo dia comun de la sesion de EUA (o --corte). Nada posterior al corte se usa.
  * Retornos por calendario: 1m, 3m, 6m = P(t)/P(t-n meses) - 1; 12-1 = P(t-1m)/P(t-12m) - 1.
  * Vol 60d = desviacion estandar de 60 rendimientos log diarios * sqrt(252).
  * dist_sma200 = P / promedio de los ultimos 200 cierres - 1 (en MXN y en moneda local).
  * dd_max_1a = drawdown maximo dentro de los ultimos 12 meses (pico a valle).
  * dist_max_52s = P / maximo de 12 meses - 1.
  * ratio_6m_vol = ret_6m / vol_60d.
  * Momentum compuesto = promedio de los rangos (1 = mejor) de ret_3m, ret_6m y ret_12_1
    sobre todo el universo con datos completos. Filtro de tendencia: P > SMA200 (MXN).
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
import time
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from herramientas.datos import ErrorDatos, valor_en_o_antes, yahoo_grafica  # noqa: E402

# ------------------------------------------------------------------ universo
# (ticker, categoria, etiqueta). Las etiquetas de acciones son propias, no GICS.
UNIVERSO: list[tuple[str, str, str]] = [
    ("SPY", "indice_eua", "S&P 500"), ("VOO", "indice_eua", "S&P 500"),
    ("QQQ", "indice_eua", "Nasdaq-100"), ("IWM", "indice_eua", "Russell 2000"),
    ("DIA", "indice_eua", "Dow Jones"),
    ("SMH", "sector_eua", "Semiconductores"), ("SOXX", "sector_eua", "Semiconductores"),
    ("XLK", "sector_eua", "Tecnologia"), ("IGV", "sector_eua", "Software"),
    ("XLF", "sector_eua", "Financiero"), ("XLE", "sector_eua", "Energia"),
    ("XLI", "sector_eua", "Industrial"), ("XLV", "sector_eua", "Salud"),
    ("XLU", "sector_eua", "Servicios publicos"), ("XLP", "sector_eua", "Consumo basico"),
    ("XLY", "sector_eua", "Consumo discrecional"), ("XLC", "sector_eua", "Comunicaciones"),
    ("ARKK", "tematico", "Innovacion (ARK)"),
    ("KWEB", "internacional", "Internet China"), ("FXI", "internacional", "China large cap"),
    ("EEM", "internacional", "Emergentes"), ("EWZ", "internacional", "Brasil"),
    ("EWW", "internacional", "Mexico"), ("EWJ", "internacional", "Japon"),
    ("INDA", "internacional", "India"),
    ("GLD", "materias_primas", "Oro"), ("IAU", "materias_primas", "Oro"),
    ("SLV", "materias_primas", "Plata"), ("GDX", "materias_primas", "Mineras de oro"),
    ("COPX", "materias_primas", "Mineras de cobre"), ("URA", "materias_primas", "Uranio"),
    ("TLT", "bonos", "Tesoro EUA 20+"), ("IEF", "bonos", "Tesoro EUA 7-10"),
    ("HYG", "bonos", "High yield EUA"),
    ("IBIT", "cripto", "Bitcoin spot"),
    ("TQQQ", "apalancado", "3x Nasdaq-100"), ("QLD", "apalancado", "2x Nasdaq-100"),
    ("SOXL", "apalancado", "3x Semiconductores"), ("SPXL", "apalancado", "3x S&P 500"),
    ("UPRO", "apalancado", "3x S&P 500"), ("SSO", "apalancado", "2x S&P 500"),
    ("TECL", "apalancado", "3x Tecnologia"),
    ("NVDA", "accion_eua", "Semis"), ("MSFT", "accion_eua", "Software"),
    ("AAPL", "accion_eua", "Hardware"), ("AMZN", "accion_eua", "Comercio/nube"),
    ("META", "accion_eua", "Internet"), ("GOOGL", "accion_eua", "Internet"),
    ("AVGO", "accion_eua", "Semis"), ("TSLA", "accion_eua", "Autos/IA"),
    ("AMD", "accion_eua", "Semis"), ("PLTR", "accion_eua", "Software"),
    ("NFLX", "accion_eua", "Medios"), ("LLY", "accion_eua", "Farma"),
    ("COST", "accion_eua", "Consumo basico"), ("JPM", "accion_eua", "Banca"),
    ("ORCL", "accion_eua", "Software/nube"), ("MU", "accion_eua", "Semis (memoria)"),
    ("TSM", "accion_eua", "Semis (ADR)"), ("ASML", "accion_eua", "Equipo semis (ADR)"),
    ("UBER", "accion_eua", "Plataformas"),
    ("NAFTRAC.MX", "bmv", "IPC (ETF)"), ("WALMEX.MX", "bmv", "Comercio"),
    ("GMEXICOB.MX", "bmv", "Mineria/cobre"), ("AMXB.MX", "bmv", "Telecom"),
    ("GFNORTEO.MX", "bmv", "Banca"), ("CEMEXCPO.MX", "bmv", "Cemento"),
    ("FEMSAUBD.MX", "bmv", "Consumo"),
]

# Subyacente de cada apalancado, para el filtro de parametros.json (subyacente > SMA200).
SUBYACENTE = {"TQQQ": "QQQ", "QLD": "QQQ", "SOXL": "SOXX", "SPXL": "SPY",
              "UPRO": "SPY", "SSO": "SPY", "TECL": "XLK"}

TICKER_FX = "MXN=X"
PAUSA_S = 1.0
REINTENTOS_429 = 3
ESPERA_429_S = 15.0
DIAS_ANIO = 252
MIN_OBS = 260  # ~12 meses + holgura para 12-1 y SMA200


# ------------------------------------------------------------------ descarga

def descargar_serie(ticker: str, cache_horas: float | None) -> dict:
    """yahoo_grafica con reintento adicional en 429 (datos.py ya reintenta 3 veces)."""
    for intento in range(REINTENTOS_429 + 1):
        try:
            return yahoo_grafica(ticker, "2y", "1d", cache_horas=cache_horas)
        except ErrorDatos as e:
            if "429" in str(e) and intento < REINTENTOS_429:
                time.sleep(ESPERA_429_S * (intento + 1))
                continue
            raise
    raise ErrorDatos(f"{ticker}: agotados reintentos")


# ------------------------------------------------------------------ utilidades

def meses_atras(f: date, n: int) -> date:
    """Misma fecha n meses antes (ajusta al ultimo dia valido del mes)."""
    m = f.month - n
    a = f.year + (m - 1) // 12
    m = (m - 1) % 12 + 1
    for d in (f.day, 30, 29, 28):
        try:
            return date(a, m, min(f.day, d))
        except ValueError:
            continue
    return date(a, m, 28)


def a_mxn(serie: list[tuple[date, float]], fx: list[tuple[date, float]]) -> list[tuple[date, float]]:
    salida = []
    for f, p in serie:
        t = valor_en_o_antes(fx, f)
        if t is not None:
            salida.append((f, p * t[1]))
    return salida


def retorno(serie, f_fin: date, f_ini: date) -> float | None:
    a = valor_en_o_antes(serie, f_ini)
    b = valor_en_o_antes(serie, f_fin)
    if not a or not b or a[1] <= 0 or a[0] < serie[0][0]:
        return None
    return b[1] / a[1] - 1


def metricas(serie: list[tuple[date, float]], corte: date) -> dict:
    """Metricas sobre una serie ya recortada al corte (en la moneda que se pase)."""
    precios = [p for _, p in serie]
    p = precios[-1]
    m1, m3, m6, m12 = (meses_atras(corte, k) for k in (1, 3, 6, 12))
    if serie[0][0] > m12:
        return {"completo": False}
    logs = [math.log(precios[i] / precios[i - 1]) for i in range(1, len(precios))]
    vol60 = statistics.stdev(logs[-60:]) * math.sqrt(DIAS_ANIO)
    sma200 = statistics.fmean(precios[-200:])
    anio = [q for f, q in serie if f > m12]
    pico, dd = anio[0], 0.0
    for q in anio:
        pico = max(pico, q)
        dd = min(dd, q / pico - 1)
    r6 = retorno(serie, corte, m6)
    return {
        "completo": True,
        "precio": p,
        "ret_1m": retorno(serie, corte, m1),
        "ret_3m": retorno(serie, corte, m3),
        "ret_6m": r6,
        "ret_12_1": retorno(serie, m1, m12),
        "ret_12m": retorno(serie, corte, m12),
        "vol_60d": vol60,
        "dist_sma200": p / sma200 - 1,
        "dd_max_1a": dd,
        "dist_max_52s": p / max(anio) - 1,
        "ratio_6m_vol": (r6 / vol60) if (r6 is not None and vol60 > 0) else None,
        "max_salto_diario": max(abs(x) for x in logs[-DIAS_ANIO:]),
    }


def rangos(valores: dict[str, float]) -> dict[str, float]:
    """Rango 1 = mayor valor; empates reciben el rango promedio."""
    orden = sorted(valores.items(), key=lambda kv: kv[1], reverse=True)
    res, i = {}, 0
    while i < len(orden):
        j = i
        while j + 1 < len(orden) and orden[j + 1][1] == orden[i][1]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            res[orden[k][0]] = r
        i = j + 1
    return res


# ------------------------------------------------------------------ pantalla

def correr(corte_arg: date | None, cache_horas: float | None, verbose: bool = True) -> tuple[list[dict], dict]:
    crudos, errores = {}, {}
    todos = [TICKER_FX] + [t for t, _, _ in UNIVERSO]
    for i, t in enumerate(todos):
        try:
            crudos[t] = descargar_serie(t, cache_horas)
            if verbose:
                print(f"[{i + 1}/{len(todos)}] {t}: {len(crudos[t]['serie'])} obs", file=sys.stderr)
        except ErrorDatos as e:
            errores[t] = str(e)
            print(f"[{i + 1}/{len(todos)}] {t}: ERROR {e}", file=sys.stderr)
        time.sleep(PAUSA_S)
    if TICKER_FX not in crudos:
        raise SystemExit("Sin tipo de cambio MXN=X: no se puede convertir a MXN")
    fx = crudos[TICKER_FX]["serie"]

    # Corte: ultimo dia de sesion comun de EUA (SPY) salvo que se indique.
    if corte_arg:
        corte = corte_arg
    else:
        ref = crudos.get("SPY") or next(v for k, v in crudos.items() if k != TICKER_FX)
        corte = ref["serie"][-1][0]
    fx = [x for x in fx if x[0] <= corte]

    filas = []
    for t, cat, etiqueta in UNIVERSO:
        if t not in crudos:
            filas.append({"ticker": t, "categoria": cat, "etiqueta": etiqueta,
                          "estado": "sin_datos", "nota": errores.get(t, "")})
            continue
        meta = crudos[t]["meta"]
        moneda = str(meta.get("currency", "")).upper()
        local = [x for x in crudos[t]["serie"] if x[0] <= corte]
        serie_mxn = local if moneda == "MXN" else a_mxn(local, fx)
        fila = {"ticker": t, "categoria": cat, "etiqueta": etiqueta, "moneda": moneda,
                "bolsa": meta.get("exchangeName", ""), "obs": len(local),
                "fecha_ultimo": local[-1][0].isoformat() if local else ""}
        if len(serie_mxn) < MIN_OBS:
            fila.update(estado="historia_insuficiente", nota=f"{len(serie_mxn)} obs")
            filas.append(fila)
            continue
        m = metricas(serie_mxn, corte)
        if not m["completo"]:
            fila.update(estado="historia_insuficiente", nota="serie inicia despues de t-12m")
            filas.append(fila)
            continue
        ml = metricas(local, corte)
        fila.update({k: v for k, v in m.items() if k != "completo"})
        fila["precio_local"] = local[-1][1]
        fila["ret_6m_local"] = ml.get("ret_6m")
        fila["ret_3m_local"] = ml.get("ret_3m")
        fila["dist_sma200_local"] = ml.get("dist_sma200")
        fila["sobre_sma200"] = m["dist_sma200"] > 0
        notas = []
        if local[-1][0] < corte:
            notas.append(f"ultimo dato {local[-1][0].isoformat()} < corte")
        if m["max_salto_diario"] > math.log(1.4):
            notas.append("salto diario >40%: revisar ajuste")
        fila["nota"] = "; ".join(notas)
        fila["estado"] = "ok"
        filas.append(fila)

    # Subyacentes de apalancados (filtro en moneda local, como en parametros.json)
    por_t = {f["ticker"]: f for f in filas}
    for t, sub in SUBYACENTE.items():
        if t in por_t and sub in por_t and por_t[sub].get("estado") == "ok":
            por_t[t]["subyacente"] = sub
            por_t[t]["subyacente_sobre_sma200_local"] = por_t[sub]["dist_sma200_local"] > 0

    # Rangos y momentum compuesto
    ok = [f for f in filas if f.get("estado") == "ok"
          and None not in (f["ret_3m"], f["ret_6m"], f["ret_12_1"])]
    r3 = rangos({f["ticker"]: f["ret_3m"] for f in ok})
    r6 = rangos({f["ticker"]: f["ret_6m"] for f in ok})
    r12 = rangos({f["ticker"]: f["ret_12_1"] for f in ok})
    for f in ok:
        t = f["ticker"]
        f["rango_3m"], f["rango_6m"], f["rango_12_1"] = r3[t], r6[t], r12[t]
        f["momentum_compuesto"] = (r3[t] + r6[t] + r12[t]) / 3
    ok.sort(key=lambda f: (f["momentum_compuesto"], -f["ret_6m"]))
    for i, f in enumerate(ok, 1):
        f["rango_general"] = i
    pos = 0
    for f in ok:
        if f["sobre_sma200"]:
            pos += 1
            f["rango_filtrado"] = pos
    resto = [f for f in filas if f not in ok]
    ordenadas = ok + resto

    fx_fin = valor_en_o_antes(fx, corte)
    contexto = {
        "corte": corte,
        "fx_corte": fx_fin,
        "fx_ret_1m": retorno(fx, corte, meses_atras(corte, 1)),
        "fx_ret_3m": retorno(fx, corte, meses_atras(corte, 3)),
        "fx_ret_6m": retorno(fx, corte, meses_atras(corte, 6)),
        "fx_ret_12m": retorno(fx, corte, meses_atras(corte, 12)),
        "errores": errores,
        "n_universo": len(UNIVERSO),
        "n_ok": len(ok),
        "n_sobre_sma200": pos,
    }
    return ordenadas, contexto


COLUMNAS = ["rango_general", "rango_filtrado", "ticker", "categoria", "etiqueta", "moneda", "bolsa",
            "fecha_ultimo", "obs", "precio_local", "precio", "ret_1m", "ret_3m", "ret_6m", "ret_12_1",
            "ret_12m", "vol_60d", "dist_sma200", "sobre_sma200", "dd_max_1a", "dist_max_52s",
            "ratio_6m_vol", "rango_3m", "rango_6m", "rango_12_1", "momentum_compuesto",
            "ret_3m_local", "ret_6m_local", "dist_sma200_local", "subyacente",
            "subyacente_sobre_sma200_local", "max_salto_diario", "estado", "nota"]


def guardar_csv(filas: list[dict], ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNAS, extrasaction="ignore")
        w.writeheader()
        for f in filas:
            fila = {}
            for k in COLUMNAS:
                v = f.get(k, "")
                if isinstance(v, float):
                    v = round(v, 6)
                fila[k] = v
            w.writerow(fila)


# ------------------------------------------------------------------ markdown

def _p(x, dec=1) -> str:
    return "n/d" if x is None or x == "" else f"{x * 100:+.{dec}f}%"


def _n(x, dec=2) -> str:
    return "n/d" if x is None or x == "" else f"{x:.{dec}f}"


def tabla(filas: list[dict], rango_col: str) -> str:
    enc = ("| # | Ticker | Tipo | 1m | 3m | 6m | 12-1 | Vol 60d | vs SMA200 | DD max 1a | vs max 52s "
           "| 6m/vol | Score |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    lineas = [enc]
    for f in filas:
        lineas.append(
            f"| {f.get(rango_col, '')} | {f['ticker']} | {f['etiqueta']} | {_p(f['ret_1m'])} | {_p(f['ret_3m'])} "
            f"| {_p(f['ret_6m'])} | {_p(f['ret_12_1'])} | {_p(f['vol_60d'], 0)} | {_p(f['dist_sma200'])} "
            f"| {_p(f['dd_max_1a'])} | {_p(f['dist_max_52s'])} | {_n(f['ratio_6m_vol'])} "
            f"| {_n(f['momentum_compuesto'], 1)} |")
    return "\n".join(lineas)


def resumen_categorias(filas: list[dict]) -> str:
    ok = [f for f in filas if f.get("estado") == "ok"]
    cats: dict[str, list[dict]] = {}
    for f in ok:
        cats.setdefault(f["categoria"], []).append(f)
    enc = ("| Categoria | N | Mediana 3m | Mediana 6m | Mediana 12-1 | Mediana vol 60d | % sobre SMA200 "
           "| Mediana score |\n|---|---|---|---|---|---|---|---|")
    lineas = [enc]
    orden = sorted(cats.items(), key=lambda kv: statistics.median(f["momentum_compuesto"] for f in kv[1]))
    for c, fs in orden:
        med = lambda k: statistics.median(f[k] for f in fs)  # noqa: E731
        sobre = sum(1 for f in fs if f["sobre_sma200"]) / len(fs)
        lineas.append(f"| {c} | {len(fs)} | {_p(med('ret_3m'))} | {_p(med('ret_6m'))} | {_p(med('ret_12_1'))} "
                      f"| {_p(med('vol_60d'), 0)} | {sobre * 100:.0f}% | {med('momentum_compuesto'):.1f} |")
    return "\n".join(lineas)


def markdown(filas: list[dict], ctx: dict) -> str:
    ok = [f for f in filas if f.get("estado") == "ok"]
    filtrados = [f for f in ok if f.get("rango_filtrado")]
    partes = [
        f"Corte: {ctx['corte']} | USDMXN al corte: {ctx['fx_corte'][1]:.4f} ({ctx['fx_corte'][0]})",
        f"USDMXN 1m {_p(ctx['fx_ret_1m'])} | 3m {_p(ctx['fx_ret_3m'])} | 6m {_p(ctx['fx_ret_6m'])} "
        f"| 12m {_p(ctx['fx_ret_12m'])}",
        f"Universo {ctx['n_universo']} | con datos completos {ctx['n_ok']} | sobre SMA200 (MXN) {ctx['n_sobre_sma200']}",
        f"Errores: {ctx['errores'] or 'ninguno'}",
        "", "## Top 20 (filtrado por tendencia)", tabla(filtrados[:20], "rango_filtrado"),
        "", "## Bottom 10 (universo completo)", tabla(ok[-10:], "rango_general"),
        "", "## Categorias", resumen_categorias(filas),
    ]
    otros = [f for f in filas if f.get("estado") != "ok"]
    if otros:
        partes += ["", "## Sin metricas", *[f"- {f['ticker']}: {f.get('estado')} {f.get('nota', '')}" for f in otros]]
    notas = [f for f in ok if f.get("nota")]
    if notas:
        partes += ["", "## Notas de calidad", *[f"- {f['ticker']}: {f['nota']}" for f in notas]]
    return "\n".join(partes)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida", required=True, help="ruta del CSV de resultados")
    ap.add_argument("--corte", help="fecha de corte AAAA-MM-DD (por omision: ultima sesion de SPY)")
    ap.add_argument("--cache-horas", type=float, default=6.0, help="vigencia de cache en horas (0 = sin cache)")
    ap.add_argument("--markdown", action="store_true", help="imprime tablas markdown en stdout")
    a = ap.parse_args(argv)
    corte = date.fromisoformat(a.corte) if a.corte else None
    filas, ctx = correr(corte, a.cache_horas or None)
    guardar_csv(filas, Path(a.salida))
    print(f"CSV: {a.salida} ({len(filas)} filas; corte {ctx['corte']})", file=sys.stderr)
    if a.markdown:
        print(markdown(filas, ctx))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
