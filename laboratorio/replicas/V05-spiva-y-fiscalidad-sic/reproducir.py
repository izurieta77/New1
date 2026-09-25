"""V05 - SPIVA (EUA y Mexico) y fiscalidad del SIC: verificacion con documentos oficiales congelados.

Reproduce, desde la raiz del repo:
  python3 laboratorio/replicas/V05-spiva-y-fiscalidad-sic/reproducir.py
Sin red. Solo biblioteca estandar (mas herramientas/ del repo). Lee datos/ (huellas en SHA256SUMS.txt)
y escribe resultados.json. El pre-registro es prerregistro.md (huella tomada antes de descargar nada)."""
import csv
import datetime
import json
import math
import os
import re
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, RAIZ)
from herramientas.estadistica import newey_west, veredicto  # noqa: E402
from herramientas.huellas import verificar  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "datos")
NUM = r"((?:[ \t]+-?\d{1,3}\.\d{2})+)"
TOL = 0.05  # pp, tolerancia de redondeo pre-registrada

fallas = verificar(os.path.join(AQUI, "SHA256SUMS.txt"))
assert not fallas, f"datos congelados alterados: {fallas}"


def leer(rel):
    with open(os.path.join(D, rel), encoding="utf-8") as f:
        return f.read()


def control_extraccion():
    """Si pypdf esta instalado, re-extrae cada PDF de SPIVA y compara con el .txt congelado."""
    try:
        sys.path.insert(0, D)
        from extraer_texto import extraer
    except Exception:
        return "pypdf no disponible: se confia en las huellas de los .txt"
    try:
        import glob
        malos = [p for p in sorted(glob.glob(os.path.join(D, "spiva", "*.pdf")))
                 if extraer(p) != open(p[:-4] + ".txt", encoding="utf-8").read()]
    except ImportError:
        return "pypdf no disponible: se confia en las huellas de los .txt"
    return "re-extraccion identica en los 9 PDF" if not malos else f"DIFERENCIAS: {malos}"


def fila(texto, ancla, etiqueta, fin_encabezado):
    """Primera fila `etiqueta` + numeros despues de `ancla`; devuelve (valores, encabezado)."""
    i = texto.find(ancla)
    if i < 0:
        return None, None
    seg = texto[i:]
    m = re.search(etiqueta + NUM, seg)
    if not m:
        return None, None
    enc = seg[:seg.find(fin_encabezado)] if fin_encabezado in seg[:m.start()] else seg[:m.start()]
    return [float(x) for x in m.group(1).split()], enc


# ---------------------------------------------------------------- 1. SPIVA EUA (A1)
EUA = [  # archivo, edicion, corte, publicacion (fuente de la fecha)
    ("spiva-us-year-end-2023.txt", "SPIVA U.S. Year-End 2023", "2023-12-31", "marzo 2024 (citado asi en SPIVA U.S. Focus Mid-Year 2024, nota 1)"),
    ("spiva-us-mid-year-2024.txt", "SPIVA U.S. Focus Mid-Year 2024", "2024-06-30", "~oct-nov 2024 (PDF creado 2024-10-29)"),
    ("spiva-us-year-end-2024.txt", "SPIVA U.S. Year-End 2024", "2024-12-31", "~marzo 2025 (primera captura Wayback 2025-03-24)"),
    ("spiva-us-mid-year-2025.txt", "SPIVA U.S. Mid-Year 2025", "2025-06-30", "~sep 2025 (primera captura Wayback 2025-09-05)"),
    ("spiva-us-year-end-2025.txt", "SPIVA U.S. Year-End 2025", "2025-12-31", "marzo 2026 (resumen de buscador; no hay fecha impresa en el PDF)"),
    ("spiva-us-mid-year-2026.txt", "SPIVA U.S. Mid-Year 2026", "2026-06-30", "~16-17 sep 2026 (PDF creado 2026-09-16; captura Wayback 2026-09-17)"),
]
res = {"control_extraccion_pdf": control_extraccion(), "A1_eua": [], "A2_mexico": [], "contexto_mxn": []}
for arch, ed, corte, pub in EUA:
    t = leer("spiva/" + arch)
    vals, enc = fila(t, "Report 1a", r"All Large-Cap Funds S&P 500", "All Domestic Funds")
    reg = {"edicion": ed, "archivo": arch, "corte": corte, "publicacion": pub, "diez_anios": None}
    if vals:
        cols = (["YTD"] if "YTD" in enc else []) + ["1", "3", "5", "10", "15", "20"]
        assert len(cols) == len(vals), (ed, vals)
        reg.update({"columnas": cols, "valores": vals, "diez_anios": vals[cols.index("10")]})
    else:
        reg["nota"] = "formato 'Focus' sin Report 1a: la cifra a 10 anios solo aparece en una grafica"
    res["A1_eua"].append(reg)

# ---------------------------------------------------------------- 2. SPIVA America Latina (A2)
LATAM = [
    ("spiva-latin-america-scorecard-year-end-2023.txt", "SPIVA Latin America Year-End 2023", "2023-12-31", "abril 2024 (PDF creado 2024-04-26)", "en"),
    ("spiva-latin-america-year-end-2024.txt", "SPIVA Latin America Year-End 2024", "2024-12-31", "abril 2025 (PDF creado 2025-04-08)", "en"),
    ("spiva-latin-america-mid-year-2025-es.txt", "Scorecard SPIVA para America Latina: Primer semestre de 2025", "2025-06-30", "octubre 2025 (PDF creado 2025-10-20)", "es"),
]
for arch, ed, corte, pub, idioma in LATAM:
    t = leer("spiva/" + arch)
    if idioma == "en":
        vals, enc = fila(t, "Report 1a", r"Mexico Equity Funds S&P/BMV IRT", "Brazil Equity Funds")
        i2 = t.find("10-Year", t.find("Report 2: Survivorship"))
        sup = re.search(r"Mexico Equity Funds (\d+) (\d{1,3}\.\d{2})", t[i2:])
        usa, _ = fila(t, "Report 1a", r"U\.S\. Equity \(MXN\) Funds S&P 500 \(MXN\)", "Brazil")
        glo, _ = fila(t, "Report 1a", r"Global Equity \(MXN\) Funds S&P World Index \(MXN\)", "Brazil")
    else:
        vals, enc = fila(t, "Tabla 1a", r"Renta variable de México S&P/BMV IRT", "Renta variable de Brasil")
        i2 = t.find("10 años", t.find("Tabla 2: supervivencia de los fondos (continuación)", t.find("Tabla 2: supervivencia de los fondos (continuación)") + 10))
        sup = re.search(r"Renta variable de México (\d+) (\d{1,3}\.\d{2})", t[i2:])
        usa, _ = fila(t, "Tabla 1a", r"Renta variable de EE\. UU\.\s*\n\(MXN\) S&P 500 \(MXN\)", "Renta")
        glo, _ = fila(t, "Tabla 1a", r"Renta variable global \(MXN\) S&P World \(MXN\)", "Renta")
    cols = (["YTD"] if "YTD" in enc else []) + ["1", "3", "5", "10"]
    assert len(cols) == len(vals), (ed, vals)
    reg = {"edicion": ed, "archivo": arch, "corte": corte, "publicacion": pub, "indice": "S&P/BMV IRT (IPC con dividendos)",
           "columnas": cols, "valores": vals, "diez_anios": vals[cols.index("10")],
           "supervivencia_10_anios": {"fondos_iniciales": int(sup.group(1)), "pct": float(sup.group(2))} if sup else None}
    res["A2_mexico"].append(reg)
    res["contexto_mxn"].append({"edicion": ed,
                                "fondos_eua_en_mxn_vs_sp500_mxn_10a": usa[cols.index("10")] if usa and len(usa) == len(cols) else None,
                                "fondos_globales_mxn_vs_sp_world_mxn_10a": glo[cols.index("10")] if glo and len(glo) == len(cols) else None})
res["A2_mexico_no_obtenidas"] = [{
    "edicion": "SPIVA Latin America Year-End 2025", "corte": "2025-12-31",
    "motivo": "spglobal.com devuelve 403; sin captura en Wayback",
    "cifra_segun_resumen_de_buscador_no_verificada": {"1": 75.6, "3": 69.8, "5": 77.3, "10": 75.6}}]


def veredicto_cifra(afirmada, eds, matices_etiqueta):
    con = [e for e in eds if e["diez_anios"] is not None]
    coinc = [e["edicion"] for e in con if abs(e["diez_anios"] - afirmada) <= TOL]
    ultima = max(con, key=lambda e: e["corte"])
    if not coinc:
        v = "no confirmada"
    elif ultima["edicion"] in coinc and not matices_etiqueta:
        v = "confirmada"
    else:
        v = "confirmada con matices"
    return {"afirmada": afirmada, "ediciones_que_coinciden": coinc, "edicion_mas_reciente_obtenida": ultima["edicion"],
            "cifra_mas_reciente_obtenida": ultima["diez_anios"], "matices_de_etiqueta": matices_etiqueta, "veredicto": v}


res["veredicto_A1"] = veredicto_cifra(85.6, res["A1_eua"], [
    "'fondos grandes' en el reporte es 'All Large-Cap Funds' (fondos que invierten en empresas grandes, no fondos de mucho patrimonio)"])
res["veredicto_A2"] = veredicto_cifra(82.9, res["A2_mexico"], [
    "el indice de SPIVA es el S&P/BMV IRT (IPC con dividendos reinvertidos), no el IPC de precio",
    "existe una edicion posterior no obtenida (Year-End 2025) y en Mid-Year 2025 el 82.93% es la tasa de SUPERVIVENCIA a 10 anios, no la de bajo desempenio"])

# ---------------------------------------------------------------- 3. A3: caracteristicas de los ganadores
t = leer("spiva/spiva-latin-america-year-end-2024.txt")
tp = re.sub(r"\s+", " ", t)
a3 = {
    "fuente": "SPIVA Latin America Year-End 2024, paginas 7-8 y Exhibit 8 (datos al 31-dic-2024)",
    "periodo_de_los_ganadores": re.search(r"where only (\d+\.\d)% of funds underperformed in 2024", tp).group(0),
    "no_benchmark_promedio_cuartil_superior_pct": float(re.search(r"outside of the S&P/BMV IRT benchmark was (\d+\.\d)%", tp).group(1)),
    "fondos_indexados_y_etfs_extranjeros_texto_pct": float(re.search(r"average of (\d+\.\d)% weight in foreign index funds and ETFs", tp).group(1)),
}
ex8 = re.search(r"Exhibit 8: Non-Benchmark Holdings in Top-Quartile Mexico Equity Funds.*?(\d+\.\d)% (\d+\.\d)% (\d+\.\d)%", tp)
a3["exhibit8_grafica_pct"] = {"no_benchmark": float(ex8.group(1)), "valores_offshore": float(ex8.group(2)), "fondos_indexados_y_etfs": float(ex8.group(3))}
a3["discrepancia_texto_vs_grafica_pp"] = round(a3["fondos_indexados_y_etfs_extranjeros_texto_pct"] - a3["exhibit8_grafica_pct"]["fondos_indexados_y_etfs"], 2)
a3["veredicto"] = "confirmada con matices"
a3["matices"] = ["se refiere al cuartil superior de 2024 (horizonte de 1 anio), no a los fondos que ganaron a 10 anios",
                 "S&P mide peso fuera del indice (cota inferior del active share), no el active share",
                 "el texto dice 16.4% y la grafica 16.2% en fondos indexados y ETFs extranjeros"]
res["A3_ganadores_mexico"] = a3

# ---------------------------------------------------------------- 4. Analisis B (mecanico, datos propios)


def mensual_yahoo(rel):
    d = json.loads(leer(rel))["chart"]["result"][0]
    out = {}
    for ts, ac in zip(d["timestamp"], d["indicators"]["adjclose"][0]["adjclose"]):
        f = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)
        if f.day == 1 and ac is not None:  # barras mensuales; descarta la barra viva del dia
            out[(f.year, f.month)] = ac
    return out


def fx_fin_de_mes(rel):
    out = {}
    with open(os.path.join(D, rel)) as f:
        for r in csv.DictReader(f):
            v = r["DEXMXUS"].strip()
            if v in ("", "."):
                continue
            y, m, _ = map(int, r["observation_date"].split("-"))
            out[(y, m)] = float(v)  # el CSV esta ordenado: queda el ultimo dato habil del mes
    return out


def meses(a, b):
    (y, m), out = a, []
    while (y, m) <= b:
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def previo(ym):
    y, m = ym
    return (y - 1, 12) if m == 1 else (y, m - 1)


ipc = mensual_yahoo("mercado/yahoo_NAFTRAC.MX_1mo_max.json")
spy = mensual_yahoo("mercado/yahoo_SPY_1mo_max.json")
fx = fx_fin_de_mes("mercado/fred_DEXMXUS.csv")
spx_mxn = {k: spy[k] * fx[k] for k in spy if k in fx}


def rend(serie, ventana):
    return [serie[k] / serie[previo(k)] - 1 for k in ventana]


def cagr(r):
    return math.prod(1 + x for x in r) ** (12 / len(r)) - 1


PESOS = [0.0, 0.1, 0.2, 0.3, 0.5]


def analisis(a, b, pesos_extra=()):
    v = meses(a, b)
    ri, rs = rend(ipc, v), rend(spx_mxn, v)
    tabla = []
    for w in sorted(set(PESOS) | set(pesos_extra)):
        rm = [(1 - w) * x + w * y for x, y in zip(ri, rs)]
        tabla.append({"peso_sp500": w, "cagr_pct": 100 * cagr(rm)})
    base = tabla[0]["cagr_pct"]
    for f in tabla:
        f["ventaja_vs_ipc_pp"] = f["cagr_pct"] - base
    reg = [f for f in tabla if f["peso_sp500"] in PESOS]
    equilibrio = {}
    for g in (1, 2, 3):
        w = None
        for f0, f1 in zip(reg, reg[1:]):
            if f0["ventaja_vs_ipc_pp"] < g <= f1["ventaja_vs_ipc_pp"]:
                w = f0["peso_sp500"] + (g - f0["ventaja_vs_ipc_pp"]) * (f1["peso_sp500"] - f0["peso_sp500"]) / (f1["ventaja_vs_ipc_pp"] - f0["ventaja_vs_ipc_pp"])
                break
        equilibrio[f"{g}pp"] = w
    dif = [100 * (y - x) for x, y in zip(ri, rs)]
    nw = newey_west(dif, 6)
    nw["veredicto"] = veredicto(nw["ic95"])
    return {"ventana": f"{a[0]}-{a[1]:02d} a {b[0]}-{b[1]:02d}", "n_meses": len(v),
            "cagr_ipc_naftrac_pct": 100 * cagr(ri), "cagr_sp500_mxn_pct": 100 * cagr(rs),
            "carteras": tabla, "peso_sp500_para_compensar_gastos": equilibrio,
            "diferencia_mensual_sp500mxn_menos_ipc": {k: nw[k] for k in ("n", "media", "se", "t", "ic95", "veredicto")}}


res["B_preregistrado"] = analisis((2015, 1), (2024, 12))
res["B_preregistrado"]["control_contra_spiva"] = {
    "spiva_ye2024_irt_10a_anualizado_pct": 4.14, "spiva_ye2024_sp500_mxn_10a_anualizado_pct": 17.08,
    "fuente": "SPIVA Latin America Year-End 2024, Report 3 (fila de indices)"}
res["B_exploratorio"] = {
    "anio_2024 (no pre-registrado; se agrego tras leer A3)": analisis((2024, 1), (2024, 12), pesos_extra=(0.164,)),
    "2016-2025 (no pre-registrado; ventana de la edicion Year-End 2025)": analisis((2016, 1), (2025, 12)),
}

# ---------------------------------------------------------------- 5. SIC: ETFs UCITS irlandeses y equivalentes de EUA


def liquidez(ticker):
    d = json.loads(leer(f"mercado/yahoo_{ticker}_1d_1y.json"))["chart"]["result"][0]
    q = d["indicators"]["quote"][0]
    val = sorted((v or 0) * (c or 0) for v, c in zip(q["volume"], q["close"]))
    n = len(val)
    med = (val[n // 2] + val[(n - 1) // 2]) / 2
    ult = datetime.datetime.fromtimestamp(d["timestamp"][-1], datetime.timezone.utc).date().isoformat()
    return {"ticker": ticker, "nombre": d["meta"].get("longName"), "bolsa": d["meta"].get("exchangeName"),
            "moneda": d["meta"].get("currency"), "precio_mxn": d["meta"].get("regularMarketPrice"),
            "sesiones": n, "sesiones_con_volumen": sum(1 for v in q["volume"] if v),
            "mediana_valor_diario_mxn": round(med), "ultima_sesion": ult}


UCITS = ["CSPXN.MX", "VUAAN.MX", "IUSAN.MX", "IWDAN.MX", "VWRAN.MX", "ISACN.MX", "EIMIN.MX", "CNDXN.MX"]
EUA_SIC = ["IVV.MX", "VOO.MX", "SPY.MX"]
res["sic_ucits"] = [liquidez(x) for x in UCITS]
res["sic_eua"] = [liquidez(x) for x in EUA_SIC]

# rendimiento por dividendo de SPY a 12 meses (proxy del S&P 500) para la fuga por retenciones
d = json.loads(leer("mercado/yahoo_SPY_1d_2y_div.json"))["chart"]["result"][0]
ult_ts = d["timestamp"][-1]
precio = d["meta"]["regularMarketPrice"]
divs = [v["amount"] for v in d["events"]["dividends"].values() if ult_ts - v["date"] <= 365 * 86400]
y = sum(divs) / precio
res["fuga_por_dividendos"] = {
    "spy_dividendos_12m_usd": sum(divs), "n_pagos": len(divs), "precio_usd": precio, "rendimiento_div_pct": 100 * y,
    "fuga_anual_pp": {"ETF_EUA_en_SIC_sin_W8BEN_30pct": 100 * y * 0.30, "ETF_EUA_con_W8BEN_10pct": 100 * y * 0.10,
                      "UCITS_irlandes_15pct_dentro_del_fondo": 100 * y * 0.15},
    "nota": "Solo la retencion de EUA. No incluye el 10% adicional de Mexico ni la acumulacion anual de dividendos (art. 140/142 LISR), que solo aplican a dividendos distribuidos: un UCITS de acumulacion no distribuye."}

# ---------------------------------------------------------------- 6. Citas legales (verificacion textual mecanica)


def contiene(rel, frase):
    return re.sub(r"\s+", " ", frase) in re.sub(r"\s+", " ", leer(rel))


CITAS = [
    ("legal/LISR.txt", "aplicando la tasa del 10% a las ganancias obtenidas en el ejercicio", "Art. 129 LISR: 10% definitivo"),
    ("legal/LISR.txt", "acciones emitidas por sociedades extranjeras cotizadas en dichas bolsas de valores", "Art. 129 fr. I incluye acciones extranjeras cotizadas (SIC)"),
    ("legal/LISR.txt", "títulos que representen índices accionarios enajenados en las bolsas de", "Art. 129 fr. II: ETFs de indices accionarios"),
    ("legal/LISR.txt", "en el ejercicio o en los diez siguientes", "Art. 129: perdidas contra ganancias del mismo tipo, 10 anios"),
    ("legal/LISR.txt", "perderá el derech o a hacerlo en los ejercicios posteriores", "Art. 129: si no se aplica la perdida pudiendo, se pierde"),
    ("legal/LISR.txt", "deberán hacer el cálculo de la ganancia o pérdida del ejercicio", "Art. 129: el intermediario calcula y entrega constancia"),
    ("legal/LISR.txt", "tasa adicional del 10% sobre los dividendos o utilidades distribuidos por las p ersonas morales residentes en", "Art. 140: 10% adicional dividendos mexicanos"),
    ("legal/LISR.txt", "la tasa del 10%, al monto al cual tengan derecho", "Art. 142 fr. V: 10% adicional dividendos extranjeros"),
    ("legal/LISR.txt", "XXII. Los que se reciban por herencia o legado.", "Art. 93 fr. XXII: herencias exentas de ISR en Mexico"),
    ("legal/LISR.txt", "sólo será aplicable cuando el contribuyente ejerza el control efectivo", "Art. 176: REFIPRE solo con control efectivo"),
    ("legal/LIF_2026.txt", "la tasa de retención anual a que se refieren los artículos 54 y 135", "Art. 24 LIF 2026"),
    ("legal/LIF_2026.txt", "de la Ley del Impuesto sobre la Renta será del 0.90 por ciento.", "Art. 24 LIF 2026: 0.90%"),
    ("legal/irs-instrucciones-706NA.txt", "exceeds the filing threshold of $60,000", "706-NA: umbral de 60,000 USD"),
    ("legal/irs-instrucciones-706NA.txt", "In general, the maximum unified credit is $13,000.", "706-NA: credito unificado 13,000 USD"),
    ("legal/irs-instrucciones-706NA.txt", "Generally, no matter where stock certificates are physically located, stock of corporations organized in or under U.S. law is property located in the United States, and all other corporate stock is property located outside the United States.", "706-NA: situs de acciones"),
    ("legal/irs-instrucciones-706NA.txt", "For an NRNC decedent who died after 2004 and before 2012, a portion of stock in a RIC", "706-NA: excepcion RIC solo 2005-2011"),
    ("legal/irs-instrucciones-706NA.txt", "Australia Ireland Austria Italy Canada* Japan Denmark Netherlands Finland South Africa France Switzerland Germany United Kingdom Greece", "706-NA: lista de tratados sucesorios (Mexico no aparece)"),
    ("legal/ecfr-26CFR20.2104-1.txt", "Shares of stock issued by a domestic corporation, irrespective of the location of the certificates", "26 CFR 20.2104-1(a)(5)"),
    ("legal/irs-tratado-eua-mexico.txt", "b) 10 percent of the gross amount of the dividends in other cases.", "Tratado EUA-Mexico art. 10: 10%"),
    ("legal/irs-tratado-eua-irlanda.txt", "b) 15 percent of the gross amount of the dividends in all other cases.", "Tratado EUA-Irlanda art. 10: 15%"),
    ("legal/gbm_como-funcionan-los-impuestos-por-las-acciones-de-empresas-extranjeras-en-el-sic.txt", "No tiene ninguna retención. Pago del ISR anual del 10% sobre las ganancias.", "GBM: SIC sin retencion, 10% anual"),
    ("legal/gbm_como-funcionan-los-impuestos-sobre-los-dividendos-en-trading-mx.txt", "La segunda retención es en México del 10%, sobre monto neto, después del impuesto retenido en el extranjero.", "GBM: 10% sobre neto en dividendos SIC"),
    ("legal/gbm_como-y-donde-recibo-los-comprobantes-fiscales-o-cfdi-por-mis-ganancias.txt", "Tus Constancias Fiscales (o CFDI) por las ganancias del 2025 ya están disponibles en tu app GBM.", "GBM: constancias 2025 en la app"),
]
res["citas_legales"] = [{"archivo": a, "tema": tema, "frase": fr, "encontrada": contiene(a, fr)} for a, fr, tema in CITAS]
assert all(c["encontrada"] for c in res["citas_legales"]), [c for c in res["citas_legales"] if not c["encontrada"]]
assert "Mexico" not in re.search(r"Australia Ireland.*?Greece", leer("legal/irs-instrucciones-706NA.txt")).group(0)

with open(os.path.join(AQUI, "resultados.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1, ensure_ascii=False)

# ---------------------------------------------------------------- salida
print("Control de extraccion:", res["control_extraccion_pdf"])
print("\nA1  % de fondos All Large-Cap por debajo del S&P 500 a 10 anios")
for e in res["A1_eua"]:
    print(f"  {e['edicion']:<34} corte {e['corte']}  10a: {e['diez_anios']}")
print("  ->", res["veredicto_A1"]["veredicto"], "| coincide en:", res["veredicto_A1"]["ediciones_que_coinciden"])
print("\nA2  % de fondos Mexico Equity por debajo del S&P/BMV IRT a 10 anios")
for e in res["A2_mexico"]:
    print(f"  {e['edicion'][:34]:<34} corte {e['corte']}  10a: {e['diez_anios']}  supervivencia 10a: {e['supervivencia_10_anios']}")
print("  ->", res["veredicto_A2"]["veredicto"], "| coincide en:", res["veredicto_A2"]["ediciones_que_coinciden"])
print("\nA3 ", {k: v for k, v in a3.items() if k not in ("matices",)})
for nombre, b in [("B pre-registrado", res["B_preregistrado"])] + list(res["B_exploratorio"].items()):
    print(f"\n{nombre}: {b['ventana']} (n={b['n_meses']})  IPC {b['cagr_ipc_naftrac_pct']:.2f}%  S&P500 MXN {b['cagr_sp500_mxn_pct']:.2f}%")
    for c in b["carteras"]:
        print(f"   w={c['peso_sp500']:.3f}  CAGR {c['cagr_pct']:6.2f}%  ventaja {c['ventaja_vs_ipc_pp']:+.2f} pp")
    nw = b["diferencia_mensual_sp500mxn_menos_ipc"]
    print(f"   equilibrio gastos: {b['peso_sp500_para_compensar_gastos']}  | dif mensual media {nw['media']:.3f}%  t {nw['t']:.2f}  IC95 [{nw['ic95'][0]:.3f}, {nw['ic95'][1]:.3f}]  {nw['veredicto']}")
print("\nSIC  UCITS irlandeses / EUA (precio MXN, sesiones con volumen, mediana valor diario MXN)")
for r in res["sic_ucits"] + res["sic_eua"]:
    print(f"  {r['ticker']:<9} {r['precio_mxn']:>10}  {r['sesiones_con_volumen']:>3}/{r['sesiones']}  {r['mediana_valor_diario_mxn']:>12,}  {r['nombre']}")
print("\nFuga por dividendos:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in res["fuga_por_dividendos"]["fuga_anual_pp"].items()},
      f"(rend. div SPY 12m {res['fuga_por_dividendos']['rendimiento_div_pct']:.2f}%)")
print("Citas legales encontradas:", sum(c["encontrada"] for c in res["citas_legales"]), "de", len(res["citas_legales"]))
