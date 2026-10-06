"""Puertas P1-P6, puntaje 0-100 (cap. 26 §6.2) y nivel (adenda del dueño) del radar EUA 2026-10-05.

Uso (despues de radar_eua.py):
    python3 arena/investigacion/radar_eua_puntaje.py \
        --metricas arena/investigacion/radar-eua-2026-10-05-metricas.csv \
        --salida arena/investigacion/radar-eua-2026-10-05.csv [--tablas ruta.md]

Reglas (todas deterministas; lo no verificable toma el valor mas bajo de la escala):
  * Plantilla de referencia del puntaje = ORO (+25% en 7 meses, stop -12.5%, 2:1): es la unica cuyo objetivo
    puede apoyarse en datos (crecimiento del consenso con multiplo constante). Diamante y Platino se reportan
    como tasa base, pero ninguna tesis con datos llega a +40% en 3m ni a +50% en 5m.
  * Edge = EV bruto HONESTO de la plantilla (la menor de la tasa base propia y la de su grupo) MENOS el EV de la
    misma plantilla en SPYM (alfa sobre el indice, no beta). P4 exige edge >= 2x costo ida y vuelta.
  * Objetivo sustentado: g = P/U1 / P/U2 - 1 (consenso de las fichas al 24-sep); objetivo 7m = (1+g)^(7/12) - 1
    con multiplo constante. Sin par de consenso verificado => no sustentado => asimetria = 0.
  * P1 solo se da con contraparte nombrada Y evidencia fechada de su restriccion (revisiones al alza). El
    momentum/tendencia sin restriccion especifica es "el mercado" (cap. 26 §6.4) => P1 falla.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

CARTERA_PAPEL = 20486.35
CAP = {  # tope por titulo en MXN, cuenta REAL de 10,000 (parametros.json arena_agresivo)
    "apalancado": 0.50 * 10000, "indice": 0.60 * 10000, "sector": 0.25 * 10000, "accion": 0.30 * 10000,
}
APALANCADOS = {"UPRO", "SPXL", "TQQQ", "TECL", "SOXL"}
INDICES = {"SPYM", "QQQM"}
SECTOR_ETF = {"XLK", "XLE", "XLV", "XLU", "XLP", "XLF", "XLI", "SMH", "SOXX", "GDX", "COPX"}
AI_NARR = {"NVDA", "AVGO", "MSFT", "META", "GOOGL", "AMZN", "TSM", "ASML", "SMH", "SOXX", "XLK", "TQQQ", "ANET",
           "PLTR", "ORCL", "AAPL", "AMD", "MU", "LRCX", "AMAT", "INTC", "SNDK", "TECL", "SOXL", "DELL", "CRWD", "PANW"}

# (fecha reporte, estado, P/U1 24-sep, P/U2 24-sep) de las fichas; None = sin dato verificado
FICHA = {
    "NVDA": ("2026-11-17", "confirmada (llamada 26-ago)", 24.1, 14.3),
    "AMD": ("2026-11-03", "estimada", 40.4, None),
    "MU": ("~2026-12-17", "estimada (no verificada)", 6.8, None),
    "AVGO": ("2026-12-09", "estimada", 18.1, None),
    "LRCX": ("2026-10-21", "Yahoo confirmada; no en IR", 32.3, 26.2),
    "AMAT": ("2026-11-12", "Yahoo no estimada", 25.7, None),
    "PLTR": ("2026-11-02", "estimada", 119.5, 82.8),
    "MSFT": ("2026-10-28", "estimada", 25.2, 21.0),
    "META": ("2026-10-28", "estimada", 24.9, 22.9),
    "GOOGL": ("2026-10-28", "estimada", 22.9, None),
    "AMZN": ("2026-10-29", "estimada", 23.8, None),
    "ORCL": ("2026-12-10", "estimada", 17.1, 12.7),
    "NFLX": ("2026-10-20", "confirmada por la emisora", 20.0, 18.8),
    "AAPL": ("2026-10-29", "no verificada en IR", 38.1, 35.1),
    "ANET": ("2026-11-03", "estimada", 50.0, 39.7),
    "INTC": ("2026-10-22", "estimada", 83.8, 61.8),
    "SNDK": ("2026-11-05", "estimada", 8.2, 6.7),
    "CRWD": ("2026-12-01", "Yahoo no estimada", 206.7, 161.7),
    "PANW": ("2026-11-18", "estimada", 93.1, None),
    "CSCO": ("2026-11-12", "Yahoo confirmada", 20.8, 19.0),
    "TXN": ("2026-10-27", "no confirmada", 31.8, 26.8),
    "TSLA": ("2026-10-21", "estimada", 213.0, 172.0),
    "DELL": ("2026-11-24", "estimada", 20.7, None),
    "XOM": ("2026-10-30", "estimada", None, None),
    "CVX": ("2026-10-30", "estimada", None, None),
    "JPM": ("2026-10-13", "confirmada por la emisora", None, None),
    "GS": ("2026-10-13", "no verificada", None, None),
    "MS": ("2026-10-14", "confirmada", None, None),
    "BAC": ("2026-10-14", "Yahoo no estimada", None, None),
    "WFC": ("2026-10-13", "confirmada", None, None),
    "JNJ": ("2026-10-13", "confirmada por la emisora", None, None),
    "UNH": ("2026-10-13", "Zacks/MarketBeat", None, None),
    "PG": ("2026-10-22", "confirmada por la emisora", None, None),
    "KO": ("2026-10-20", "Yahoo", None, None),
    "PM": ("2026-10-21", "Yahoo confirmada", None, None),
    "GE": ("2026-10-20", "confirmada por la emisora", None, None),
    "GEV": ("2026-10-28", "confirmada por la emisora", None, None),
    "CAT": ("2026-10-29", "estimada", None, None),
    "RTX": ("2026-10-20", "estimada", None, None),
    "LLY": ("2026-10-29", "estimada", None, None),
    "ABBV": ("2026-10-29", "Yahoo no estimada", None, None),
    "MRK": ("2026-10-29", "Yahoo no estimada", None, None),
    "TMO": ("2026-10-22", "estimada", None, None),
    "V": ("2026-10-27", "estimada", None, None),
    "MA": ("2026-10-29", "estimada", None, None),
    "BRK-B": ("2026-11-07", "estimada", None, None),
    "WMT": ("2026-11-19", "Yahoo no estimada", None, None),
    "COST": ("2026-12-10", "estimada (no verificada)", None, None),
    "HD": ("2026-11-17", "Yahoo no estimada", None, None),
    "SPCX": ("2026-11-03", "estimada", None, None),
}
# Geopolitica/regulatorio (cap. 23-24, juicio): 10 bajo, 5 medio, 0 alto
GEO = {"NVDA": 5, "AMD": 5, "MU": 5, "AVGO": 5, "INTC": 5, "SNDK": 5, "LRCX": 0, "AMAT": 0, "TSM": 0, "ASML": 0,
       "MSFT": 5, "META": 5, "GOOGL": 5, "AMZN": 5, "ORCL": 5, "NFLX": 10, "AAPL": 5, "PLTR": 5, "ANET": 5,
       "CRWD": 5, "PANW": 5, "DELL": 5, "UBER": 5, "XOM": 5, "CVX": 5, "XLE": 5, "SPYM": 5, "QQQM": 5, "UPRO": 5,
       "SPXL": 5, "TQQQ": 5, "TECL": 5, "SOXL": 0, "SMH": 5, "SOXX": 5, "XLK": 5, "GLD": 5, "IAU": 5, "GDX": 5,
       "COPX": 5}
# P1: (cumple, contraparte y condicion) solo con evidencia fechada de la restriccion
P1 = {
    "NVDA": (True, "Analistas anclados a la guia: supero la guia de ingresos 3 de 3 (+4.6 a +5.7%) y el consenso de UPA 4 de 4 (ficha 25-sep); deja de operar cuando el consenso ya incorpora la sorpresa"),
    "MU": (True, "Analistas anclados: guia 1T FY27 de 61.5 mil M contra consenso de 57.4 (+7%) (post-mortem 30-sep); deja de operar cuando el consenso se reajusta; el precio no se movio (1,065.11 -> 1,063.96)"),
    "AMAT": (True, "Revision al alza ya visible en el consenso FY27 de UPA (ficha 25-sep); contraparte = analistas que revisan tarde; deja de operar al agotarse las revisiones"),
}
P1_FALLA_DEFECTO = "Sin restriccion especifica: momentum/tendencia es 'el mercado' (cap. 26 §6.4)"

DESC = {
    "NVDA": "P/U FY28 de 14.3x contra mediana historica de 51x GAAP: descuenta que FY28 (+~70%) es el pico; DCF inverso exige FCF +14.9%/ano 10 anos (r 9%)",
    "MU": "~7x la UPA FY27 de consenso: descuenta que FY27 es el pico del ciclo de memoria",
    "AMD": "P/U 2027 de 40x: ejecucion casi perfecta de Helios; FCF +29-35%/ano por 10 anos",
    "AVGO": "P/U FY27 de 18.1x; DCF inverso: FCF +14.9-19.6%/ano; IA FY27 de 100-115 mil M en el escenario base",
    "LRCX": "P/U FY27 de 32.3x contra 23.7x de mediana a 5 anos; FCF +23-28%/ano por 10 anos",
    "AMAT": "P/U FY27 de 25.7x tras comprimirse de ~41x; descuenta digestion del WFE en 2027",
    "PLTR": "P/Ventas de 80x contra 26x de mediana; P/U 2027 de 83x: crecimiento sostenido por encima de +60%",
    "MSFT": "P/U FY27 de 25.2x; FCF +18-21%/ano por 10 anos; capex y OpenAI",
    "META": "P/U 2027 de 22.9x contra 23.8x de mediana GAAP: valuacion en su rango; capex 2027 > 200 mil M es el debate",
    "GOOGL": "P/U 2027 de 22.9x; TTM de 17.2x (32.7x sin ganancias de capital); Cloud +50-65% en la base",
    "AMZN": "VE/UO de 30.1x (31x en 2025); AWS +30-35% en la base",
    "ORCL": "P/U FY27/FY28 de 17.1x/12.7x con FCF negativo hasta FY28: descuenta riesgo de financiamiento",
    "NFLX": "P/U 2026e de 20.0x contra 40.5x de mediana a 5 anos: descuenta menor tiempo en pantalla",
    "AAPL": "P/U de 38x contra promedio de 30x; FCF +12.6-15%/ano contra +8.5% historico",
    "ANET": "P/U 2026e de 50x y 2027e de 39.7x, arriba del maximo de 5 anos",
    "INTC": "P/U 2027 de 62x; DCF inverso +38-44%/ano: descuenta que la fundicion 14A funcione",
    "SNDK": "P/U FY27 de 8.2x: descuenta que el precio de NAND toca techo",
    "TSM": "P/U 33x TTM / 21x adelantado (NVDA ficha [13]); fundamentales propios no verificados",
    "ASML": "P/U adelantado ~33x (pares en fichas AMAT/LRCX); fundamentales propios no verificados",
    "UBER": "Sin ficha: fundamentales no verificados",
}
REF_ETF = {
    "SPYM": "Cierre del S&P 500 bajo su SMA200 (7,442.59 hoy) o VIX >= 25",
    "QQQM": "Cierre de Nasdaq-100 bajo su SMA200 o VIX >= 25",
    "UPRO": "Filtro del comite: ^GSPC < SMA200 x 0.97 (7,009) o VIX >= 25, o stop de 134-136 USD",
    "SPXL": "Igual que UPRO; 1 titulo (5,326 MXN) rebasa 50% de la cuenta real",
    "TQQQ": "Nasdaq-100 < SMA200 x 0.97 o VIX >= 25; decision del comite: nunca TQQQ",
    "TECL": "XLK < SMA200 x 0.97 o VIX >= 25",
    "SOXL": "SOXX < SMA200 x 0.97 o VIX >= 25; cola historica de -90%",
    "SMH": "Cierre bajo SMA200; el desarme de crowding de jul-2026 se repite",
    "XLK": "Cierre bajo SMA200",
    "GLD": "Tasa real de 10a > 3% y sin cierre sobre SMA200",
    "GDX": "Oro cierra bajo su minimo reciente",
    "XLE": "Cese al fuego EUA-Iran y petroleo a la baja",
}
REF = {
    "NVDA": "Guia del 4T (17-nov) bajo el consenso, DSO > 70 dias, margen bruto < 71% o evento de credito de OpenAI",
    "MU": "Precios contrato 4T26 (TrendForce, oct) planos o a la baja; margen bruto < 86% en el 1T FY27",
    "AMD": "Retraso de Helios/HBM4 o UPA 2027 < US$11",
    "AVGO": "IA FY27 < US$90 mil M o margen operativo non-GAAP < 62%",
    "LRCX": "WFE 2027 plano o nuevas restricciones a China tras el 10-ene-2027; UPA FY27 < US$8.5",
    "AMAT": "Ingresos FY27 < US$40 mil M o no renovacion de la suspension a China; UPA FY27 < US$15",
    "PLTR": "Ingresos 2027 < US$11 mil M (< +35%) o friccion presupuestal tras las intermedias",
    "MSFT": "Capex/arrendamientos sin retorno o financiamiento de OpenAI en duda",
    "META": "Guia de capex 2027 > US$200 mil M con FCF negativo o anuncios < +15%",
    "GOOGL": "Cloud < +45% o perdida de consultas de Search; margen operativo < 31%",
    "AMZN": "AWS < +25% o UO 2027 < US$115 mil M",
    "ORCL": "Mas retrasos de energia/financiamiento o recorte de calificacion; UPA FY28 < US$9",
    "NFLX": "Ingresos 2027 < +9% o UPA 2027 < US$3.5",
    "AAPL": "Guia del 1T FY27 por debajo, aranceles 232/301 o memoria que comprime margen",
    "ANET": "Ingresos 2027 < US$15 mil M o margen bruto < 60%",
    "INTC": "FCF mas negativo o sin cliente externo para 14A",
    "SNDK": "Precios NAND tocan techo en 4T26-1T27; UPA FY27 < US$170",
    "TSM": "Controles a China o evento en Taiwan (tipo E, cap. 23)",
    "ASML": "Controles de exportacion a China",
    "UBER": "n/d",
}
# Catalizadores de indices/ETF (fechas del cap. 26 §6.6 y fichas): sin fecha especifica del activo
CAT_INDICE = "27-28-oct FOMC; 3-nov intermedias; 10-ene-2027 vence la tregua EUA-China"


def f(x, d=None):
    try:
        return float(x)
    except (TypeError, ValueError):
        return d


def edge_de(m, nombre, fuente="hon"):
    """(alfa sobre SPYM, multiplo del costo) de una plantilla; fuente: hon (la menor de propia/grupo) o own."""
    costo = f(m["costo_rt"])
    if fuente == "hon":
        ev_net = f(m.get(f"{nombre}_hon_ev_neto"))
        ev = None if ev_net is None else ev_net + costo
    else:
        ev = f(m.get(f"{nombre}_own_ev_bruto"))
    ref = f(m.get(f"{nombre}_ref_spym_ev_bruto"))
    if ev is None or ref is None:
        return None, None
    return ev - ref, (ev - ref) / costo


def escala_edge(mult):
    return 0 if mult is None or mult < 2 else (10 if mult < 3 else (18 if mult < 5 else 25))


def puntaje(m, t):
    """Devuelve dict con componentes."""
    costo = f(m["costo_rt"])
    edge, mult = edge_de(m, "Oro")
    edge_o, mult_o = edge_de(m, "Oro", "own")
    c_edge = escala_edge(mult)
    c_evid = 5  # C para todos: laboratorio 0 ventajas demostradas de 26 pruebas
    rep = FICHA.get(t)
    if t in APALANCADOS | INDICES | SECTOR_ETF or rep is None:
        c_cat = 2 if (t in APALANCADOS | INDICES | SECTOR_ETF) else 0
    else:
        c_cat = 10 if rep[1].startswith("confirmada") and not rep[1].startswith("confirmada (no") else 6
        if rep[0].startswith("~") or "no verificada" in rep[1]:
            c_cat = 6
    # objetivo sustentado
    g = None
    obj7 = None
    if rep and rep[2] and rep[3]:
        g = rep[2] / rep[3] - 1
        obj7 = (1 + g) ** (7 / 12) - 1
    sustentado = obj7 is not None and obj7 >= 0.20
    c_asim = 10 if sustentado else 0
    # liquidez: 3 si EUA > 500 MM USD/dia y .MX con >= 20 de 22 sesiones; 0 si falta; 5 nunca (spread no verificado)
    sesmx = f(m.get("sesiones_MX_22"))
    usdv = f(m.get("usd_vol_medio_63d_mm"), 0)
    c_liq = 3 if (sesmx is not None and sesmx >= 20 and usdv > 500) else 0
    c_cost = 5 if costo <= 0.007 else (3 if costo <= 0.012 else 0)
    corr = f(m.get("corr60_mxn_cartera"))
    c_corr = 0 if corr is None else (10 if corr < 0.3 else (6 if corr < 0.6 else (2 if corr < 0.8 else 0)))
    c_geo = GEO.get(t, 0)
    c_adv = 0
    # crowding
    r6, vol = f(m["ret_6m"], 0), f(m["vol_60d"], 0)
    if t in APALANCADOS:
        r6, vol = r6 / 3, vol / 3
    if r6 >= 1.0:
        c_crowd = -10
    elif r6 >= 0.5 or vol >= 0.6:
        c_crowd = -8
    elif r6 >= 0.3 and t in AI_NARR:
        c_crowd = -5
    elif r6 >= 0.3:
        c_crowd = -3
    elif t in AI_NARR:
        c_crowd = -3
    else:
        c_crowd = 0
    if t in APALANCADOS:
        c_crowd = max(-10, c_crowd - 2)
    total = c_edge + c_evid + c_cat + c_asim + c_liq + c_cost + c_corr + c_geo + c_adv + c_crowd
    sens = total - c_edge + escala_edge(mult_o)
    extra = {}
    for n in ('Diamante', 'Platino'):
        e, mu = edge_de(m, n)
        extra[f'edge_mult_{n}'] = mu
    return dict(**extra, total_si_tasa_propia=sens, edge_mult_propia_oro=mult_o, edge_alfa_oro=edge, edge_mult=mult, c_edge=c_edge, c_evid=c_evid, c_cat=c_cat, c_asim=c_asim,
                c_liq=c_liq, c_cost=c_cost, c_corr=c_corr, c_geo=c_geo, c_adv=c_adv, c_crowd=c_crowd,
                total=total, g_consenso=g, obj_7m_consenso=obj7, objetivo_sustentado=sustentado)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metricas", required=True)
    ap.add_argument("--salida", required=True)
    ap.add_argument("--tablas")
    a = ap.parse_args()
    filas = list(csv.DictReader(open(a.metricas, encoding="utf-8")))
    out = []
    for m in filas:
        t = m["ticker"]
        pt = puntaje(m, t)
        mxn = f(m["precio_mxn_titulo"])
        if t in APALANCADOS:
            cap = CAP["apalancado"]
        elif t in INDICES:
            cap = CAP["indice"]
        elif t in SECTOR_ETF:
            cap = CAP["sector"]
        else:
            cap = CAP["accion"]
        cabe_real = mxn <= cap
        cabe_papel = mxn <= cap * CARTERA_PAPEL / 10000
        sesmx = f(m.get("sesiones_MX_22"))
        sic = "no verificado (sin .MX en Yahoo)" if sesmx is None else (
            f"proxy Yahoo .MX {int(sesmx)}/22 sesiones; BMV no verificada" + ("; liquidez baja" if sesmx < 15 else ""))
        p1ok, p1txt = P1.get(t, (False, P1_FALLA_DEFECTO))
        p2 = True
        p3_real = cabe_real and sesmx is not None and sesmx >= 10
        p3_papel = cabe_papel and sesmx is not None and sesmx >= 10
        p4 = pt["edge_mult"] is not None and pt["edge_mult"] >= 2
        p5 = t in REF or t in REF_ETF  # stop, plazo y hecho que refuta escritos solo para los presentados
        p6 = True
        sust = pt["objetivo_sustentado"]
        gates_real = [p1ok, p2, p3_real, p4, p5, p6]
        gates_papel = [p1ok, p2, p3_papel, p4, p5, p6]
        pot = "Oro" if sust else "sin objetivo sustentado"
        sc = pt["total"]
        if all(gates_real) and sust and sc >= 55:
            nivel = "Oro"
        elif all(gates_papel) and sust and sc >= 55:
            nivel = "Oro (solo papel)"
        else:
            nivel = "Sin nivel"
        fallan = [n for n, ok in zip(["P1", "P2", "P3", "P4", "P5", "P6"], gates_real) if not ok]
        if not sust:
            fallan.append("objetivo")
        row = dict(ticker=t, tipo=m["tipo"], precio_usd=m["precio_usd"], precio_mxn_titulo=m["precio_mxn_titulo"],
                   cabe_real=cabe_real, cabe_papel=cabe_papel, sic=sic, P1=p1ok, P2=p2, P3_real=p3_real,
                   P3_papel=p3_papel, P4=p4, P5=p5, P6=p6, nivel=nivel, nivel_potencial=pot, puertas_falladas=" ".join(fallan))
        row.update({k: (round(v, 4) if isinstance(v, float) else v) for k, v in pt.items()})
        for k in ("ret_1m", "ret_3m", "ret_6m", "ret_12m", "vol_60d", "dist_sma200", "dist_max_52s", "sma50", "sma200",
                  "max_52s", "corr60_mxn_cartera", "costo_rt", "usd_vol_medio_63d_mm"):
            row[k] = m.get(k)
        for n in ("Diamante", "Platino", "Oro"):
            for k in (f"{n}_own_p_obj", f"{n}_grp_p_obj", f"{n}_hon_p_obj", f"{n}_hon_fuente", f"{n}_hon_ev_neto",
                      f"{n}_fin_own_p", f"{n}_fin_grp_p", f"{n}_own_p_stop", f"{n}_grp_p_stop", f"{n}_ref_spym_ev_bruto",
                      f"{n}_filtro_p_obj", f"{n}_filtro_p_stop", f"{n}_filtro_ev_bruto", f"{n}_own_n", f"{n}_grp_n"):
                row[k] = m.get(k)
        rep = FICHA.get(t)
        row["fecha_reporte"] = rep[0] if rep else ""
        row["estado_fecha"] = rep[1] if rep else ""
        row["contraparte_P1"] = p1txt
        row["que_descuenta"] = DESC.get(t, "")
        row["hecho_que_refuta"] = REF.get(t, REF_ETF.get(t, ""))
        out.append(row)
    out.sort(key=lambda r: (r["nivel"] == "Sin nivel", -r["total"]))
    campos = []
    for r in out:
        for k in r:
            if k not in campos:
                campos.append(k)
    with open(a.salida, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(out)
    print(f"CSV: {a.salida} ({len(out)} filas)")
    niveles = {}
    for r in out:
        niveles[r["nivel"]] = niveles.get(r["nivel"], 0) + 1
    print("Niveles:", niveles)
    for r in out[:40]:
        print(r["ticker"], r["total"], r["nivel"], r["puertas_falladas"], "edge x", r["edge_mult"], "obj7", r["obj_7m_consenso"])


if __name__ == "__main__":
    main()
