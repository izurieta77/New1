"""Modelo integrado de Wal-Mart de Mexico y Centroamerica (WALMEX.MX): historico FY2024-FY2025 y 1S2026
(NIIF, MXN), 3 escenarios de mecanismo, DCF inverso.

FASE 0 (formacion). Los escenarios son supuestos explicitos de mecanismo (tension / intermedio /
eficiencia): no son pronosticos, ni guia del emisor, ni consenso, ni recomendacion de compra o venta.
Solo biblioteca estandar (mas openpyxl/xlrd, ya instalados, solo para leer los .xlsx/.xls de datos/).

    python3 empresas/WALMEX.MX/modelo/modelo.py

Capas (cero invencion):
  datos/Walmex_Financial_Statements_4Q25.xlsx   estados financieros 2025/2024 tal como los publico WALMEX
                                                 (mismas cifras que WALMEX_4T25_BMV / Earnings Release 4Q25).
  datos/Walmex_Financial_Statements_2Q26.xlsx   estados financieros del periodo de 6 meses a jun-2026
                                                 (mismas cifras que WALMEX_2T26_BMV).
  datos/Walmex_Reporte_Anual_BMV_2025.txt       Informe Anual 2025 (texto extraido del PDF BMV/Emisnet):
                                                 notas 8 (inmuebles y equipo), 9 (arrendamientos), 12
                                                 (partes relacionadas), 14/23 (COFECE), 18 (capital), 22 (segmentos).
  datos/WALMEX_2T26_BMV.txt                     Reporte trimestral 2T26 BMV (notas condensadas: COFECE,
                                                 arrendamientos, segmentos, capital social).
  datos/Walmex_IA25_Resumen_Financiero.txt       Tabla resumen 2015-2025 del Informe Anual 2025 (paginas 61-62):
                                                 usada como segunda lectura independiente de los totales anuales.
  datos/Walmex_Programa_de_Inversion_2026.txt    Comunicado del 25-mar-2026 (capex y dividendos 2026 guiados).
  datos/yahoo_WALMEX.MX_1mo_2026-09-25.json      Precio de cierre (Yahoo Finance).
  datos/damodaran_betaemerg.xls, damodaran_betaGlobal.xls, damodaran_ctrypremJuly26.xlsx
                                                 Insumos de costo de capital (Damodaran, enero/julio 2026).

Cada linea de base.json cita el documento y la pagina/nota exacta en "fuentes_campos". La descomposicion de
"Leases and other long-term liabilities" en arrendamientos_financieros + otros_pasivos_lp, y de "otros
pasivos circulantes", se verifica por CUADRE EXACTO contra el total de pasivos publicado (ver _check_balance):
esto es la doble comprobacion de esas partidas (no son un residuo sin verificar).

Sale con codigo 1 si: falla una huella de datos/, algun control del motor FALLA, o la auditoria de
resultados.json releido no coincide con lo guardado.
"""
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DATOS = AQUI / "datos"
sys.path.insert(0, str(AQUI.parents[2]))
from herramientas import modelo_integrado as mi  # noqa: E402
from herramientas import huellas  # noqa: E402

M = lambda miles: round(miles / 1000.0, 6)  # miles de MXN -> millones de MXN  # noqa: E731

FUENTES = {
    "F1": {"documento": "WALMEX Reporte Anual 2025 (Informe Anual integrado, presentado en BMV/Emisnet; "
                          "incluye los estados financieros consolidados auditados NIIF al 31-dic-2025 y 2024)",
           "url": "https://www.walmex.mx (seccion Relacion con Inversionistas / Informe Anual 2025); "
                  "copia congelada en datos/Walmex_Reporte_Anual_BMV_2025.pdf",
           "fecha": "2026 (ejercicio 2025)", "descargado": "2026-09-25"},
    "F2": {"documento": "WALMEX Estados Financieros 4T25 estructurados (hoja de calculo publicada junto con el "
                          "reporte trimestral 4T25 en BMV; mismas cifras que el Reporte Anual 2025, Nota de "
                          "Estados Financieros)",
           "url": "BMV/Emisnet, WALMEX 4T25; copia en datos/Walmex_Financial_Statements_4Q25.xlsx",
           "fecha": "2026-02-18", "descargado": "2026-09-25"},
    "F3": {"documento": "WALMEX Reporte trimestral 2T26 (BMV, formato con notas NIIF condensadas)",
           "url": "BMV/Emisnet, WALMEX 2T26; copia en datos/WALMEX_2T26_BMV.pdf y .txt",
           "fecha": "2026-07 (periodo a 30-jun-2026)", "descargado": "2026-09-25"},
    "F4": {"documento": "WALMEX Estados Financieros 2T26 estructurados (hoja de calculo con balance a jun-2026 "
                          "y flujo de 6 meses a jun-2026 y jun-2025)",
           "url": "BMV/Emisnet, WALMEX 2T26; copia en datos/Walmex_Financial_Statements_2Q26.xlsx",
           "fecha": "2026-07", "descargado": "2026-09-25"},
    "F5": {"documento": "WALMEX Reports Fourth Quarter and Full Year 2025 Results (earnings release en ingles)",
           "url": "walmex.mx / BMV; copia en datos/Walmex_Earnings_Release_4Q25.pdf",
           "fecha": "2026-02-18", "descargado": "2026-09-25"},
    "F6": {"documento": "WALMEX Informe Anual 2025 - Resumen Financiero 2015-2025 (paginas 61-62 del Informe "
                          "Anual; extracto en texto)",
           "url": "walmex.mx; copia en datos/Walmex_IA25_Resumen_Financiero.pdf",
           "fecha": "2026", "descargado": "2026-09-25"},
    "F7": {"documento": "Walmart de Mexico y Centroamerica Anuncia su Programa de Inversion 2026 y su "
                          "Propuesta de Pago de Dividendos y Recompra de Acciones (comunicado Walmex Day 2026)",
           "url": "walmex.mx; copia en datos/Walmex_Programa_de_Inversion_2026.pdf",
           "fecha": "2026-03-25", "descargado": "2026-09-25"},
    "F8": {"documento": "Yahoo Finance, WALMEX.MX, precios diarios 1 mes", "url": "https://query1.finance.yahoo.com",
           "fecha": "2026-09-25", "descargado": "2026-09-25"},
    "F9": {"documento": "A. Damodaran, Betas by industry (Emerging Markets), enero 2026",
           "url": "https://pages.stern.nyu.edu/~adamodar/", "fecha": "2026-01-07", "descargado": "2026-09-25"},
    "F10": {"documento": "A. Damodaran, Betas by industry (Global), enero 2026",
            "url": "https://pages.stern.nyu.edu/~adamodar/", "fecha": "2026-01-07", "descargado": "2026-09-25"},
    "F11": {"documento": "A. Damodaran, Country default spreads and risk premiums, julio 2026",
            "url": "https://pages.stern.nyu.edu/~adamodar/", "fecha": "2026-07-01", "descargado": "2026-09-25"},
}


# ------------------------------------------------------------------ periodo FY2024 y FY2025 (fuente F1/F2)
# Cifras en MILES de MXN, transcritas de datos/Walmex_Financial_Statements_4Q25.xlsx hoja "Balance sheet" y
# "Cash flow" (=BMV WALMEX_4T25; ver tambien Reporte Anual 2025 notas citadas). Los totales de resultados
# (P&L anual) se toman de la hoja "P&L by quarter" del mismo archivo, SUMANDO los 4 trimestres de cada anio
# (control: la suma exacta de trimestres debe reproducir los totales anuales publicados en el Earnings
# Release 4T25 (F5, pagina 2) y en el Informe Anual 2025 resumen (F6, pagina 61); ver _check_pl_anual).

PL_TRIMESTRES = {
    # miles de MXN; fuente F2 hoja "P&L by quarter"
    "2024": {
        "Q1": {"ventas": 224588763, "otros_ing": 1604855, "costo_ventas": -172025182, "gastos_generales": -35466191,
               "otros_ing_op": 607548, "otros_gto_op": -140039, "ing_fin": 752699, "gto_fin": -2776597,
               "utilidad_neta": 13183311},
        "Q2": {"ventas": 225746164, "otros_ing": 1668953, "costo_ventas": -172500625, "gastos_generales": -37827399,
               "otros_ing_op": 1095582, "otros_gto_op": -198573, "ing_fin": 1054371, "gto_fin": -2731765,
               "utilidad_neta": 12510125},
        "Q3": {"ventas": 228426505, "otros_ing": 1767448, "costo_ventas": -172785911, "gastos_generales": -39169345,
               "otros_ing_op": 633981, "otros_gto_op": -150011, "ing_fin": 1187087, "gto_fin": -2811980,
               "utilidad_neta": 12934381},
        "Q4": {"ventas": 272881165, "otros_ing": 1823638, "costo_ventas": -209722555, "gastos_generales": -43622311,
               "otros_ing_op": 447016, "otros_gto_op": -324488, "ing_fin": 678674, "gto_fin": -3779990,
               "utilidad_neta": 15199567},
    },
    "2025": {
        "Q1": {"ventas": 239160734, "otros_ing": 1813879, "costo_ventas": -182900156, "gastos_generales": -39723431,
               "otros_ing_op": 715719, "otros_gto_op": -177836, "ing_fin": 329700, "gto_fin": -2800026,
               "utilidad_neta": 12316745},
        "Q2": {"ventas": 244556170, "otros_ing": 1697627, "costo_ventas": -186848081, "gastos_generales": -42423807,
               "otros_ing_op": 566207, "otros_gto_op": -281017, "ing_fin": 455964, "gto_fin": -2646253,
               "utilidad_neta": 11226894},
        "Q3": {"ventas": 239794954, "otros_ing": 1725219, "costo_ventas": -181746347, "gastos_generales": -40946589,
               "otros_ing_op": 426638, "otros_gto_op": -233118, "ing_fin": 530506, "gto_fin": -3223295,
               "utilidad_neta": 11747296},
        "Q4": {"ventas": 280982376, "otros_ing": 1866925, "costo_ventas": -214905405, "gastos_generales": -44950665,
               "otros_ing_op": 685238, "otros_gto_op": -361484, "ing_fin": 531425, "gto_fin": -2795123,
               "utilidad_neta": 14599806},
    },
    # fuente F4 hoja "P&L by quarter" (2Q26 workbook trae Q1/Q2 2026 directos, sin necesidad de sumar)
    "2026H1": {
        "Q1": {"ventas": 243262759, "otros_ing": 1755727, "costo_ventas": -185425324, "gastos_generales": -41487070,
               "otros_ing_op": 648208, "otros_gto_op": -282726, "ing_fin": 600453, "gto_fin": -2895590,
               "utilidad_neta": 12499551},
        "Q2": {"ventas": 249215193, "otros_ing": 1732651, "costo_ventas": -190822849, "gastos_generales": -43679658,
               "otros_ing_op": 808393, "otros_gto_op": -234044, "ing_fin": 534533, "gto_fin": -2799623,
               "utilidad_neta": 11152382},
    },
}


def _suma_pl(trimestres: dict) -> dict:
    claves = next(iter(trimestres.values())).keys()
    return {k: sum(q[k] for q in trimestres.values()) for k in claves}


def construir_resultados(pl: dict) -> dict:
    """Mapea el P&L (miles) al esquema del motor (millones). gastos_operativos se define NETO de otros
    ingresos/gastos operativos (para que utilidad_bruta - gastos_operativos = utilidad_operativa, control
    C15), documentado en fuentes_campos."""
    ingresos = pl["ventas"] + pl["otros_ing"]
    costo_ventas = -pl["costo_ventas"]
    utilidad_bruta = ingresos - costo_ventas
    gastos_operativos = -pl["gastos_generales"] - pl["otros_ing_op"] - pl["otros_gto_op"]
    utilidad_operativa = utilidad_bruta - gastos_operativos
    gasto_intereses = -pl["gto_fin"]
    ingreso_intereses = pl["ing_fin"]
    uai = utilidad_operativa - gasto_intereses + ingreso_intereses
    utilidad_neta = pl["utilidad_neta"]
    impuestos = uai - utilidad_neta
    return {
        "ingresos": M(ingresos), "costo_ventas": M(costo_ventas), "utilidad_bruta": M(utilidad_bruta),
        "gastos_operativos": M(gastos_operativos), "utilidad_operativa": M(utilidad_operativa),
        "gasto_intereses": M(gasto_intereses), "ingreso_intereses": M(ingreso_intereses),
        "utilidad_antes_impuestos": M(uai), "impuestos": M(impuestos), "utilidad_neta": M(utilidad_neta),
        "utilidad_neta_controladora": M(utilidad_neta),
    }


FC_RESULTADOS = {
    "resultados.ingresos": "F2/F1 P&L: Net Sales + Other revenues = Total revenues (asi calcula WALMEX su margen "
        "bruto; Earnings Release 4T25 F5 p.2 y Reporte Anual F1 Estados de Resultados)",
    "resultados.costo_ventas": "F2/F5 P&L: Cost of sales",
    "resultados.utilidad_bruta": "F2/F5 P&L: Gross profit (= Total revenues - Cost of sales)",
    "resultados.gastos_operativos": "F2 P&L: General expenses - Other income + Other expenses (neto; asi "
        "Gross profit - gastos_operativos = Operating income, F5 p.2)",
    "resultados.utilidad_operativa": "F2/F5 P&L: Operating income",
    "resultados.gasto_intereses": "F2 P&L: Financial expenses (suma de los 4 trimestres; incluye interes de "
        "arrendamientos IFRS16, Nota 9/21 del Reporte Anual F1)",
    "resultados.ingreso_intereses": "F2 P&L: Financial income (suma de los 4 trimestres)",
    "resultados.utilidad_antes_impuestos": "F2/F5 P&L: Income before income taxes",
    "resultados.impuestos": "F2/F5 P&L: implicito = UAI - utilidad neta (Taxes, F5 p.2)",
    "resultados.utilidad_neta": "F2/F5 P&L: Consolidated net income (=utilidad neta controladora; WALMEX no "
        "tiene participacion no controladora, F1 Nota sobre participacion no controladora / IA25 tabla F6 p.61)",
}


def construir_balance_2025_2024() -> tuple:
    """Balance a dic-2025 y dic-2024, miles de MXN, fuente F2 hoja 'Balance sheet' (= F1 Estado de Situacion
    Financiera Consolidado). La descomposicion de 'Leases and other long-term liabilities' usa Nota 15 (F1
    p.196-197): LT lease liability (Nota 9) + ISR LP + ingreso diferido por rentas + partes relacionadas LP
    (Nota 12) + otros."""
    BS = {
        "2025": {"caja": 28591153, "cxc": 26634850, "inventarios": 107450921, "prepagados": 1432523,
                 "ppe": 195080344, "rou": 63545003, "prop_inv": 4133976, "intangibles": 42646550,
                 "isr_diferido_activo": 23189157, "otros_activos_lp": 2568786,
                 "proveedores": 123903939, "arr_cp": 5186942, "otras_cxp": 38820282, "isr_por_pagar": 1805549,
                 "leases_y_otros_lp": 83988302, "isr_lp": 2364599, "beneficios_empleados": 3623589,
                 "capital_social": 45027866, "utilidades_retenidas": 180017034, "ori": 14702423,
                 "prima_venta_acciones": 6230963, "fondo_plan_acciones": -10398225,
                 "arr_lp_nota9": 75661205},   # Nota 9 (F1 p.192): pasivo por arrendamiento LP
        "2024": {"caja": 36513582, "cxc": 24862289, "inventarios": 110694942, "prepagados": 1326455,
                 "ppe": 180715011, "rou": 63958072, "prop_inv": 4351732, "intangibles": 47393126,
                 "isr_diferido_activo": 21678914, "otros_activos_lp": 2398942,
                 "proveedores": 121971233, "arr_cp": 4735116, "otras_cxp": 39899960, "isr_por_pagar": 4187435,
                 "leases_y_otros_lp": 84844691, "isr_lp": 2381292, "beneficios_empleados": 2997869,
                 "capital_social": 45429160, "utilidades_retenidas": 167447963, "ori": 25260173,
                 "prima_venta_acciones": 5906487, "fondo_plan_acciones": -11168314,
                 "arr_lp_nota9": 74994788},
    }
    return BS["2025"], BS["2024"]


def construir_balance_jun2026_2025() -> tuple:
    """Balance a jun-2026 y jun-2025, miles de MXN, fuente F4 hoja 'Balance sheet'. El pasivo por
    arrendamiento total a jun-2026 se toma de la nota de arrendamientos (F3, 'Pasivo por arrendamiento -
    neto $83,098,100'); el LP se obtiene restando el corto plazo del balance (residuo verificado: ver
    _check_balance, que cuadra el pasivo total exacto)."""
    BS = {
        "2026H1": {"caja": 30118253, "cxc": 29276926, "inventarios": 107528941, "prepagados": 1729352,
                   "ppe": 197792350, "rou": 65093662, "prop_inv": 4060187, "intangibles": 43798208,
                   "isr_diferido_activo": 24410677, "otros_activos_lp": 2138034,
                   "proveedores": 114233228, "arr_cp": 5495153, "otras_cxp": 54741776, "isr_por_pagar": 451241,
                   "leases_y_otros_lp": 85994789, "isr_lp": 2636446, "beneficios_empleados": 3780163,
                   "capital_social": 44840434, "utilidades_retenidas": 180098013, "ori": 17354616,
                   "prima_venta_acciones": 6488469, "fondo_plan_acciones": -10167738,
                   "arr_total_nota": 83098100},   # F3: 'Pasivo por arrendamiento - neto'
    }
    return BS["2026H1"]


def mapear_balance(bs: dict, con_arr_lp_nota=True) -> tuple:
    """Devuelve (balance_motor_en_millones, memo_millones). arrendamientos_financieros = CP + LP del pasivo
    por arrendamiento (Nota 9/15 o nota de arrendamientos del trimestre). otros_pasivos_lp = resto de
    'leases and other long-term liabilities' + ISR LP (linea separada del balance) + beneficios a empleados."""
    if con_arr_lp_nota:
        arr_lp = bs["arr_lp_nota9"]
    else:
        arr_lp = bs["leases_y_otros_lp"] - (bs["arr_total_lp_residuo"])
    arr_total = bs["arr_cp"] + arr_lp
    otros_lp_del_bloque = bs["leases_y_otros_lp"] - arr_lp
    otros_pasivos_lp = otros_lp_del_bloque + bs["isr_lp"] + bs["beneficios_empleados"]
    otros_pasivos_circulantes = bs["otras_cxp"] + bs["isr_por_pagar"]
    otros_activos_lp = bs["prop_inv"] + bs["intangibles"] + bs["isr_diferido_activo"] + bs["otros_activos_lp"]
    ppe_neto = bs["ppe"] + bs["rou"]
    activo_total = bs["caja"] + bs["cxc"] + bs["inventarios"] + bs["prepagados"] + ppe_neto + otros_activos_lp
    pasivo_total = bs["proveedores"] + otros_pasivos_circulantes + arr_total + otros_pasivos_lp
    capital_contable = (bs["capital_social"] + bs["utilidades_retenidas"] + bs["ori"] + bs["prima_venta_acciones"]
                        + bs["fondo_plan_acciones"])
    balance = {
        "caja": M(bs["caja"]), "cuentas_por_cobrar": M(bs["cxc"]), "inventarios": M(bs["inventarios"]),
        "otros_activos_circulantes": M(bs["prepagados"]), "ppe_neto": M(ppe_neto),
        "otros_activos_lp": M(otros_activos_lp), "activo_total": M(activo_total),
        "proveedores": M(bs["proveedores"]), "otros_pasivos_circulantes": M(otros_pasivos_circulantes),
        "deuda": 0.0, "arrendamientos_financieros": M(arr_total), "revolvente": 0.0,
        "otros_pasivos_lp": M(otros_pasivos_lp), "pasivo_total": M(pasivo_total),
        "capital_contable": M(capital_contable), "utilidades_retenidas": M(bs["utilidades_retenidas"]),
    }
    memo = {"ppe_sin_derecho_uso": M(bs["ppe"]), "activos_derecho_uso": M(bs["rou"]),
            "arrendamiento_corto_plazo": M(bs["arr_cp"]), "arrendamiento_largo_plazo": M(arr_lp),
            "leases_y_otros_pasivos_lp_total_bs": M(bs["leases_y_otros_lp"]),
            "otros_dentro_de_leases_y_otros_lp": M(otros_lp_del_bloque),
            "isr_diferido_activo": M(bs["isr_diferido_activo"]), "isr_pasivo_lp": M(bs["isr_lp"]),
            "beneficios_empleados_pasivo": M(bs["beneficios_empleados"]), "unidades": "millones de MXN"}
    return balance, memo


def _check_balance(nombre: str, balance: dict, esperado_activo: float, esperado_pasivo: float) -> None:
    da = abs(balance["activo_total"] - M(esperado_activo))
    dp = abs(balance["pasivo_total"] - M(esperado_pasivo))
    if da > 0.6 or dp > 0.6:
        raise AssertionError(f"{nombre}: activo_total dif={da}, pasivo_total dif={dp} (tolerancia redondeo 0.6 MDP)")


# ------------------------------------------------------------------ flujo de efectivo (fuente F2/F4 hoja "Cash flow")

def construir_flujo(cf: dict, utilidad_neta_millones: float) -> dict:
    """cf trae las lineas EXACTAS del estado de flujos (miles de MXN) tal como las publica WALMEX. Se separa
    cambio_capital_trabajo (variaciones de capital de trabajo) y otros_operativos (resto de la conciliacion
    utilidad->CFO: partidas no monetarias + ISR pagado en efectivo vs devengado + beneficios pagados), de
    modo que utilidad_neta + D&A + SBC + cambio_capital_trabajo + otros_operativos = CFO EXACTO (control C07)."""
    isr_devengado = cf["ibt"] - cf["utilidad_neta"]     # miles; utilidad neta consolidada = flujo (sin NCI)
    ct = {
        "cuentas_por_cobrar": cf["d_cxc"], "inventarios": cf["d_inv"], "pagos_anticipados_y_otros": cf["d_prepag"],
        "proveedores": cf["d_prov"], "otras_cuentas_por_pagar": cf["d_otras_cxp"],
    }
    oo = {
        "perdida_(utilidad)_baja_de_activos": cf["perdida_baja"], "interes_ganado_(reverso_no_monetario)": cf["int_ganado"],
        "interes_por_pasivos_de_arrendamiento_(nota_9)": cf["int_arrendamiento"],
        "efecto_cambiario_no_realizado": cf["fx_no_realizado"], "provision_obligaciones_laborales": cf["prov_laboral"],
        "interes_a_cargo_(reverso_no_monetario)": cf["int_a_cargo"],
        "diferencia_isr_devengado_vs_isr_pagado_en_efectivo": cf["isr_pagado"] + isr_devengado,
        "beneficios_a_empleados_pagados": cf["beneficios_pagados"],
    }
    capex = -cf["capex"]
    cfi_otros = cf["int_cobrado"] + cf["venta_ppe"] + cf["fondo_plan_acciones_inv"]
    dividendos = -(cf.get("dividendos") or 0)
    recompras = -cf["recompras"]
    principal_arr = -cf["pago_arrendamiento"]
    flujo = {
        "depreciacion_amortizacion": M(cf["da"]), "sbc": M(cf["sbc"]), "cfo": M(cf["cfo_neto"]),
        "capex": M(capex), "cfi": M(cf["cfi_neto"]), "cff": M(cf["cff_neto"]),
        "dividendos": M(dividendos), "recompras": M(recompras), "emision_deuda": 0.0, "amortizacion_deuda": 0.0,
        "principal_arrendamientos_financieros": M(principal_arr), "emision_acciones": 0.0,
        "efecto_cambiario": M(cf["fx_caja"]),
        "cambio_capital_trabajo": {k: M(v) for k, v in ct.items()},
        "otros_operativos": {k: M(v) for k, v in oo.items()},
        "otros_inversion": {k: M(v) for k, v in {"interes_cobrado": cf["int_cobrado"], "venta_ppe": cf["venta_ppe"],
                                                  "fondo_plan_acciones": cf["fondo_plan_acciones_inv"]}.items()},
        "otros_financiamiento": {k: M(v) for k, v in {"interes_pagado": cf["interes_pagado"]}.items()},
        "caja_inicial": M(cf["caja_ini"]), "caja_final": M(cf["caja_fin"]), "utilidad_neta": utilidad_neta_millones,
    }
    return flujo


FC_FLUJO = {
    "flujo.cfo": "F2/F4 Cash flow: 'Net cash flow operating activities'",
    "flujo.capex": "F2/F4 Cash flow: 'Long-lived assets' (Investing activities); = 'ADQUISICIONES DE INMUEBLES Y "
        "EQUIPO' del resumen F6 p.61",
    "flujo.cfi": "F2/F4 Cash flow: 'Net cash flow used in from investing activities'",
    "flujo.cff": "F2/F4 Cash flow: 'Net cash flow used in investing activities' (asi rotulada por WALMEX; es la "
        "de financiamiento)",
    "flujo.dividendos": "F2/F4 Cash flow: 'Dividend payment' (= 'Dividendo pagado' F6 p.61)",
    "flujo.recompras": "F2/F4 Cash flow: 'Repurchase of shares' (= 'Inversion en recompra de acciones' F6 p.61)",
    "flujo.principal_arrendamientos_financieros": "F2/F4 Cash flow: 'Payment of leases liability' (incluye "
        "principal + interes pagados en efectivo del pasivo por arrendamiento, Nota 9 F1 p.192: "
        "$4,170,343 + $9,115,155 = $13,285,498 en 2025)",
    "flujo.depreciacion_amortizacion": "F2/F4 Cash flow: 'Depreciation and amortization' (=EBITDA - utilidad "
        "operativa, control interno)",
    "flujo.sbc": "F2/F4 Cash flow: 'Stock option compensation expenses'",
    "flujo.efecto_cambiario": "F2/F4 Cash flow: 'Effect of changes in the value of cash'",
    "flujo.otros_operativos": "F2/F4 Cash flow, seccion 'Operating activities': partidas no monetarias "
        "(perdida en baja de activos, interes ganado y a cargo -reversos-, interes por pasivos de arrendamiento "
        "Nota 9, efecto cambiario no realizado, provision de obligaciones laborales) mas la diferencia entre "
        "ISR pagado en efectivo ('Income tax paid') y el ISR devengado implicito (Income before income taxes - "
        "Consolidated net income del mismo estado), mas beneficios a empleados pagados; ver modelo.py "
        "construir_flujo() para el detalle exacto de cada componente.",
}


# ------------------------------------------------------------------ movimientos de PPE y arrendamientos (Nota 8/9)

def movimientos_ppe_2024_2025() -> tuple:
    """Nota 8 (Inmuebles y equipo, F1 p.199-200) y Nota 9 (Arrendamiento / derecho de uso, F1 p.191-192).
    ppe_neto del motor = PPE + derecho de uso; 'adiciones' = altas de costo (PPE costo + obras en proceso +
    derecho de uso costo); 'depreciacion' = cargo del ejercicio (PPE + derecho de uso, magnitud positiva);
    'otros' = bajas/traspasos/efecto de conversion de ambos rubros (costo y depreciacion acumulada), y de
    obras en proceso. ppe_inicial a dic-2023 = PPE (156,127,476) + derecho de uso (61,483,671) segun las
    mismas notas (columna 'DICIEMBRE 31, 2023')."""
    ppe_inicial_2023 = 156127476 + 61483671
    datos = {
        "2024": {
            "ppe_costo_adiciones": 10177200, "ppe_costo_bajas": -7585402, "ppe_costo_traspasos": 20984612,
            "ppe_costo_efecto": 12824936,
            "ppe_depre_cargo": -15849666, "ppe_depre_bajas": 6980674, "ppe_depre_traspasos": -161028,
            "ppe_depre_efecto": -5402495,
            "obras_adiciones": 23185101, "obras_bajas": 17956, "obras_traspasos": -20654858, "obras_efecto": 70505,
            "rou_costo_adiciones": 1821479, "rou_costo_bajasmodact": 4145807, "rou_costo_traspasos": -367253,
            "rou_costo_efecto": 2697522,
            "rou_depre_cargo": -5532684, "rou_depre_bajasmodact": 509128, "rou_depre_traspasos": 158663,
            "rou_depre_efecto": -958261,
        },
        "2025": {
            "ppe_costo_adiciones": 10534771, "ppe_costo_bajas": -5397474, "ppe_costo_traspasos": 22050881,
            "ppe_costo_efecto": -8832961,
            "ppe_depre_cargo": -17574664, "ppe_depre_bajas": 4732867, "ppe_depre_traspasos": -108658,
            "ppe_depre_efecto": 3876809,
            "obras_adiciones": 27312581, "obras_bajas": -87161, "obras_traspasos": -22245174, "obras_efecto": 103516,
            "rou_costo_adiciones": 2771976, "rou_costo_bajasmodact": 3961671, "rou_costo_traspasos": -291169,
            "rou_costo_efecto": -1911073,
            "rou_depre_cargo": -5857857, "rou_depre_bajasmodact": 45326, "rou_depre_traspasos": 121815,
            "rou_depre_efecto": 746242,
        },
    }
    out = {}
    for anio, d in datos.items():
        adiciones = d["ppe_costo_adiciones"] + d["obras_adiciones"] + d["rou_costo_adiciones"]
        depreciacion = -(d["ppe_depre_cargo"] + d["rou_depre_cargo"])
        otros = (d["ppe_costo_bajas"] + d["ppe_costo_traspasos"] + d["ppe_costo_efecto"]
                 + d["ppe_depre_bajas"] + d["ppe_depre_traspasos"] + d["ppe_depre_efecto"]
                 + d["obras_bajas"] + d["obras_traspasos"] + d["obras_efecto"]
                 + d["rou_costo_bajasmodact"] + d["rou_costo_traspasos"] + d["rou_costo_efecto"]
                 + d["rou_depre_bajasmodact"] + d["rou_depre_traspasos"] + d["rou_depre_efecto"])
        out[anio] = {"adiciones": M(adiciones), "depreciacion": M(depreciacion), "otros": M(otros)}
    return out["2024"], out["2025"], M(ppe_inicial_2023)


def movimientos_arrendamientos_2024_2025() -> tuple:
    """Nota 9 (F1 p.192): 'conciliacion entre los saldos ... del pasivo por arrendamiento'. 'nuevos' agrega
    nuevos contratos + modificaciones/ajustes; 'principal' = pago de principal SEGUN ESTA NOTA (difiere en
    ~0.03% de 'Pagos de renta - principal' del cash flow por conversion de Centroamerica; ver notas-y-modelo.md);
    'otros' = intereses devengados netos de pagos + efecto de conversion."""
    datos = {
        "2024": {"inicial": 75253796, "nuevos_contratos": 1815029, "modif_ajustes": 5255291,
                 "pagos_principal": -4198979, "intereses_dev_neto_pagos": -711483, "efecto_conversion": 2316249,
                 "final": 79729903},
        "2025": {"inicial": 79729903, "nuevos_contratos": 2779031, "modif_ajustes": 4720641,
                 "pagos_principal": -4123847, "intereses_dev_neto_pagos": -747242, "efecto_conversion": -1510339,
                 "final": 80848147},
    }
    out = {}
    for anio, d in datos.items():
        nuevos = d["nuevos_contratos"] + d["modif_ajustes"]
        principal = -d["pagos_principal"]
        otros = d["intereses_dev_neto_pagos"] + d["efecto_conversion"]
        calc_final = d["inicial"] + nuevos - principal + otros
        assert abs(calc_final - d["final"]) <= 1, f"{anio}: roll-forward arrendamientos no cuadra: {calc_final} vs {d['final']}"
        out[anio] = {"inicial": M(d["inicial"]), "nuevos": M(nuevos), "principal": M(principal), "otros": M(otros),
                     "fuente": "Nota 9, F1 p.192 (conciliacion de saldos del pasivo por arrendamiento)"}
    return out["2024"], out["2025"]


# ------------------------------------------------------------------ construccion de base.json

def construir_historico() -> list:
    pl24 = _suma_pl(PL_TRIMESTRES["2024"])
    pl25 = _suma_pl(PL_TRIMESTRES["2025"])
    pl26h1 = _suma_pl(PL_TRIMESTRES["2026H1"])
    r24, r25, r26h1 = construir_resultados(pl24), construir_resultados(pl25), construir_resultados(pl26h1)

    bs25, bs24 = construir_balance_2025_2024()
    bal25, memo25 = mapear_balance(bs25)
    bal24, memo24 = mapear_balance(bs24)
    bs26h1 = construir_balance_jun2026_2025()
    bs26h1["arr_lp_nota9"] = bs26h1["arr_total_nota"] - bs26h1["arr_cp"]
    bal26h1, memo26h1 = mapear_balance(bs26h1)

    # controles de cuadre exacto contra los totales de balance PUBLICADOS por WALMEX (F2/F4)
    _check_balance("FY2024", bal24, 493893065, 261017596)
    _check_balance("FY2025", bal25, 495273263, 259693202)
    _check_balance("1S2026", bal26h1, 505946590, 267332796)

    cf25 = {"ibt": 68876648, "utilidad_neta": 49890741, "da": 24953131, "perdida_baja": 223564, "sbc": 304661,
            "int_ganado": -1327640, "int_arrendamiento": 9115155, "fx_no_realizado": 857863, "prov_laboral": 1031707,
            "int_a_cargo": 263182, "cfo_neto": 82437748, "d_cxc": -1642439, "d_inv": 1249411, "d_prepag": -406351,
            "d_prov": 4755799, "d_otras_cxp": -1571215, "isr_pagado": -23574671, "beneficios_pagados": -671057,
            "capex": -38981955, "int_cobrado": 1327640, "venta_ppe": 544462, "fondo_plan_acciones_inv": 789904,
            "cfi_neto": -36319949, "dividendos": -28922976, "recompras": -8799988, "interes_pagado": -263182,
            "pago_arrendamiento": -13285498, "cff_neto": -51271644, "fx_caja": -2768584, "caja_ini": 36513582,
            "caja_fin": 28591153}
    cf24 = {"ibt": 68931487, "utilidad_neta": 53827384, "da": 22639474, "perdida_baja": -402757, "sbc": 493766,
            "int_ganado": -2657187, "int_arrendamiento": 8593484, "fx_no_realizado": -62852, "prov_laboral": 574290,
            "int_a_cargo": 42902, "cfo_neto": 72635535, "d_cxc": -173566, "d_inv": -12543798, "d_prepag": -826096,
            "d_prov": 3057479, "d_otras_cxp": 2121813, "isr_pagado": -16397777, "beneficios_pagados": -755127,
            "capex": -34763789, "int_cobrado": 2657187, "venta_ppe": 872570, "fondo_plan_acciones_inv": 699272,
            "cfi_neto": -30534760, "dividendos": -37399452, "recompras": 0, "interes_pagado": -42902,
            "pago_arrendamiento": -12355100, "cff_neto": -49797454, "fx_caja": 3541276, "caja_ini": 40668985,
            "caja_fin": 36513582}
    cf26h1 = {"ibt": 30931033, "utilidad_neta": 23651933, "da": 13127660, "perdida_baja": 229113, "sbc": -23393,
              "int_ganado": -511904, "int_arrendamiento": 4668054, "fx_no_realizado": 236870, "prov_laboral": 364838,
              "int_a_cargo": 23518, "cfo_neto": 23281751, "d_cxc": -3152488, "d_inv": 172045, "d_prepag": 148733,
              "d_prov": -10012535, "d_otras_cxp": -4160702, "isr_pagado": -8578681, "beneficios_pagados": -180410,
              "capex": -11701395, "int_cobrado": 511904, "venta_ppe": 183055, "fondo_plan_acciones_inv": 511386,
              "cfi_neto": -10495050, "dividendos": 0, "recompras": -3998809, "interes_pagado": -23518,
              "pago_arrendamiento": -6940560, "cff_neto": -10962887, "fx_caja": -296714, "caja_ini": 28591153,
              "caja_fin": 30118253}

    f24 = construir_flujo(cf24, r24["utilidad_neta"])
    f25 = construir_flujo(cf25, r25["utilidad_neta"])
    f26h1 = construir_flujo(cf26h1, r26h1["utilidad_neta"])

    for nombre, r, f in (("FY2024", r24, f24), ("FY2025", r25, f25), ("1S2026", r26h1, f26h1)):
        un = f["utilidad_neta"] + f["depreciacion_amortizacion"] + f["sbc"]
        ct_tot = sum(f["cambio_capital_trabajo"].values())
        oo_tot = sum(f["otros_operativos"].values())
        cfo_calc = un + ct_tot + oo_tot
        if abs(cfo_calc - f["cfo"]) > 0.05:
            raise AssertionError(f"{nombre}: puente utilidad->CFO no cuadra: {cfo_calc} vs {f['cfo']} (dif "
                                 f"{cfo_calc - f['cfo']})")

    mp24, mp25, ppe_ini_2023 = movimientos_ppe_2024_2025()
    ma24, ma25 = movimientos_arrendamientos_2024_2025()
    mp24["ppe_inicial"] = ppe_ini_2023
    mp24["fuente"] = "Nota 8 + Nota 9, F1 p.199-200 y p.191-192 (roll-forward de costo y depreciacion acumulada)"
    mp25["fuente"] = mp24["fuente"]

    ebitda_25 = 103447  # F5 p.2 / F6 p.61: 'FLUJO OPERATIVO (EBITDA)' 2025
    ebitda_24 = 99998    # idem 2024
    ajustado25 = [{"nombre": "ebitda_emisor", "base": "utilidad_operativa",
                   "ajustes": {"depreciacion_y_amortizacion (F2/F5)": f25["depreciacion_amortizacion"]},
                   "valor_ajustado": float(ebitda_25),
                   "fuente": "F5 p.2 / F6 p.61: EBITDA = utilidad de operacion + D&A (definicion del glosario "
                             "del emisor, 'Flujo Operativo')"}]
    ajustado24 = [{"nombre": "ebitda_emisor", "base": "utilidad_operativa",
                   "ajustes": {"depreciacion_y_amortizacion (F2/F5)": f24["depreciacion_amortizacion"]},
                   "valor_ajustado": float(ebitda_24),
                   "fuente": ajustado25[0]["fuente"]}]

    memo25.update({"capex_mexico_2025": M(33291269), "capex_centroamerica_2025": M(5690686),
                   "ebitda_reportado": ebitda_25, "activos_mexico": M(381747650),
                   "activos_centroamerica": M(75624168), "credito_mercantil": M(37901445),
                   "dividendo_por_accion_ordinario_2025_pesos": 1.30, "dividendo_por_accion_extra_2025_pesos": 0.39,
                   "acciones_recompradas_2025_millones": 154.0, "cofece_multa_pesos_millones": 93.4})
    memo24.update({"capex_mexico_2024": M(29219848), "capex_centroamerica_2024": M(5543941),
                   "ebitda_reportado": ebitda_24, "activos_mexico": M(363070453),
                   "activos_centroamerica": M(88125708), "credito_mercantil": M(42696904),
                   "dividendo_por_accion_ordinario_2024_pesos": 1.18, "dividendo_por_accion_extra_2024_pesos": 0.99,
                   "acciones_recompradas_2024_millones": 0.0})
    memo26h1.update({"utilidad_operativa_mexico_1s2026": M(30571773), "utilidad_operativa_ca_1s2026": M(4919487),
                     "utilidad_operativa_mexico_1s2025": M(30292604), "utilidad_operativa_ca_1s2025": M(5863404),
                     "acciones_en_circulacion_millones": 17220.231803, "acciones_recompradas_acum_2026": 71.98})

    p24 = {"periodo": "FY2024", "anio": 2024, "fin": "2024-12-31",
           "fuente": "F1 (Informe Anual 2025, comparativo 2024) / F2 (Estados Financieros 4T25 estructurados) / "
                     "F5 (Earnings Release 4T25 p.2) / F6 (Resumen 2015-2025 p.61)",
           "fuentes_campos": FC_RESULTADOS | FC_FLUJO,
           "resultados": r24, "balance": bal24, "flujo": f24,
           "movimientos_ppe": mp24, "movimientos_arrendamientos": ma24,
           "ajustado": ajustado24, "memo": memo24,
           "notas": "Primer ejercicio de la base (no hay periodo previo en base.json para C13); movimientos_ppe "
                    "y movimientos_arrendamientos SI traen saldo inicial (dic-2023, Nota 8/9), asi que C05/C06 "
                    "corren igual para FY2024."}
    p25 = {"periodo": "FY2025", "anio": 2025, "fin": "2025-12-31",
           "fuente": p24["fuente"], "fuentes_campos": FC_RESULTADOS | FC_FLUJO,
           "resultados": r25, "balance": bal25, "flujo": f25,
           "movimientos_ppe": mp25, "movimientos_arrendamientos": ma25,
           "ajustado": ajustado25, "memo": memo25, "notas": "Cierre del ejercicio anual mas reciente disponible."}
    p26h1 = {"periodo": "1S2026", "anio": 2026, "fin": "2026-06-30",
             "fuente": "F3 (Reporte trimestral 2T26 BMV) / F4 (Estados Financieros 2T26 estructurados)",
             "fuentes_campos": FC_RESULTADOS | FC_FLUJO,
             "resultados": r26h1, "balance": bal26h1, "flujo": f26h1, "memo": memo26h1,
             "notas": ("Periodo de 6 meses (no anual): resultados y flujo son del semestre, no anualizados. "
                       "El reporte trimestral condensado NO trae roll-forward de PPE/derecho de uso ni del "
                       "pasivo por arrendamiento con el detalle de la Nota 8/9 anual, asi que movimientos_ppe y "
                       "movimientos_arrendamientos se omiten aqui (C05/C06 quedan en INFO para este periodo, no "
                       "FALLA). El desglose de 'Leases and other long-term liabilities' en arrendamientos_lp + "
                       "otros_pasivos_lp se obtuvo por diferencia contra el pasivo total por arrendamiento de la "
                       "nota de arrendamientos del trimestre ($83,098,100) y se verifico por cuadre EXACTO del "
                       "pasivo total del balance (ver _check_balance en modelo.py).")}
    return [p24, p25, p26h1]


# ------------------------------------------------------------------ doble comprobacion (segunda lectura independiente)
# Cifras anuales tal como aparecen en DOS documentos distintos de los usados para construir el historico:
# el Earnings Release 4T25 en ingles (F5, pagina 2, tabla 'Results 2025 / 2024') y la tabla resumen 2015-2025
# del Informe Anual (F6, paginas 61-62). Ambos son independientes del archivo estructurado F2 usado arriba
# (formatos y layout distintos; mismo emisor). Si difieren de lo calculado aqui en mas que redondeo, es FALLA.

SEGUNDA_LECTURA_F5_F6 = {
    "FY2025": {"ventas_netas": 1004494, "otros_ingresos": 7104, "ingresos_totales": 1011598, "costo_ventas": 766400,
               "utilidad_bruta": 245198, "utilidad_operativa": 78494, "ebitda": 103447, "utilidad_antes_impuestos": 68877,
               "impuestos": 18986, "utilidad_neta": 49891, "activo_total": 495273,
               "capital_contable": 235580, "capex": 38982, "dividendo_pagado": 28923, "recompra_pesos": 8800,
               "acciones_recompradas_millones": 154, "caja": 28591, "inventarios": 107451, "proveedores": 123904},
    "FY2024": {"ventas_netas": 951642, "otros_ingresos": 6865, "ingresos_totales": 958507, "costo_ventas": 727034,
               "utilidad_bruta": 231473, "utilidad_operativa": 77359, "ebitda": 99998, "utilidad_antes_impuestos": 68931,
               "impuestos": 15104, "utilidad_neta": 53827, "activo_total": 493893,
               "capital_contable": 232875, "capex": 34764, "dividendo_pagado": 37399, "recompra_pesos": 0,
               "acciones_recompradas_millones": 0, "caja": 36514, "inventarios": 110695, "proveedores": 121971},
}


def doble_comprobacion(hist: list) -> dict:
    """Compara, para cada cifra anual clave, el valor construido en base.json (redondeado a millones enteros)
    contra la segunda lectura independiente (F5 p.2 + F6 p.61-62). Tolerancia = 1 (redondeo de millones)."""
    por_periodo = {p["periodo"]: p for p in hist}
    filas = []

    def chk(periodo, campo, calculado, segunda_lectura):
        if segunda_lectura is None:
            return
        dif = round(calculado) - segunda_lectura
        filas.append({"periodo": periodo, "campo": campo, "calculado_base_json": round(calculado, 3),
                      "segunda_lectura_F5_F6": segunda_lectura, "diferencia_redondeo": dif,
                      "ok": abs(dif) <= 1})

    for per in ("FY2024", "FY2025"):
        p = por_periodo[per]
        sl = SEGUNDA_LECTURA_F5_F6[per]
        r, b, f = p["resultados"], p["balance"], p["flujo"]
        chk(per, "ingresos_totales", r["ingresos"], sl["ingresos_totales"])
        chk(per, "costo_ventas", r["costo_ventas"], sl["costo_ventas"])
        chk(per, "utilidad_bruta", r["utilidad_bruta"], sl["utilidad_bruta"])
        chk(per, "utilidad_operativa", r["utilidad_operativa"], sl["utilidad_operativa"])
        chk(per, "utilidad_antes_impuestos", r["utilidad_antes_impuestos"], sl["utilidad_antes_impuestos"])
        chk(per, "impuestos", r["impuestos"], sl["impuestos"])
        chk(per, "utilidad_neta", r["utilidad_neta"], sl["utilidad_neta"])
        ebitda_calc = r["utilidad_operativa"] + f["depreciacion_amortizacion"]
        chk(per, "ebitda", ebitda_calc, sl["ebitda"])
        chk(per, "activo_total", b["activo_total"], sl["activo_total"])
        chk(per, "capital_contable", b["capital_contable"], sl["capital_contable"])
        chk(per, "caja", b["caja"], sl["caja"])
        chk(per, "inventarios", b["inventarios"], sl["inventarios"])
        chk(per, "proveedores", b["proveedores"], sl["proveedores"])
        chk(per, "capex", f["capex"], sl["capex"])
        chk(per, "dividendos_pagados", f["dividendos"], sl["dividendo_pagado"])
        chk(per, "recompras", f["recompras"], sl["recompra_pesos"])
    ok = sum(1 for x in filas if x["ok"])
    return {"naturaleza": "doble comprobacion: mismas cifras leidas de DOS documentos independientes del emisor "
                          "(Earnings Release 4T25 en ingles, F5 p.2; y tabla resumen 2015-2025 del Informe Anual, "
                          "F6 p.61-62) contra lo transcrito a base.json desde el archivo de estados financieros "
                          "estructurado (F2). Tolerancia = 1 (redondeo a millones enteros).",
            "total": len(filas), "ok": ok, "fallas": [x for x in filas if not x["ok"]], "detalle": filas}


# ------------------------------------------------------------------ costo de capital (WACC) y DCF inverso

def leer_damodaran():
    import xlrd
    import openpyxl
    import warnings
    warnings.filterwarnings("ignore")

    def beta_retail(archivo):
        wb = xlrd.open_workbook(str(DATOS / archivo))
        ws = wb.sheet_by_name("Industry Averages")
        for r in range(10, ws.nrows):
            if ws.cell_value(r, 0) == "Retail (Grocery and Food)":
                return {"beta_bruta": ws.cell_value(r, 2), "de_ratio": ws.cell_value(r, 3),
                        "beta_desapalancada": ws.cell_value(r, 5),
                        "beta_desapalancada_corregida_caja": ws.cell_value(r, 7)}
        raise KeyError("Retail (Grocery and Food) no encontrado")

    beta_emerg = beta_retail("damodaran_betaemerg.xls")
    beta_global = beta_retail("damodaran_betaGlobal.xls")
    wb = openpyxl.load_workbook(DATOS / "damodaran_ctrypremJuly26.xlsx", data_only=True)
    ws = wb["ERPs by country"]
    erp_madura = None
    for row in ws.iter_rows(values_only=True):
        if row and row[0] == "Enter the current risk premium for the US =":
            erp_madura = row[4]
            break
    crp_mexico = None
    for row in ws.iter_rows(values_only=True):
        if row and row[0] == "Mexico":
            crp_mexico = {"default_spread": row[3], "erp_total": row[4], "crp_ajustada_volatilidad": row[5],
                          "crp_cds": row[7] if len(row) > 7 else None}
            break
    return {"beta_emergentes_retail": beta_emerg, "beta_global_retail": beta_global,
            "erp_madura_eua": erp_madura, "crp_mexico": crp_mexico,
            "fuente": "F9/F10/F11: Damodaran, industria 'Retail (Grocery and Food)', beta desapalancada "
                      "corregida por caja; CRP Mexico ajustada por volatilidad relativa de mercado (metodo "
                      "estandar Damodaran, hoja 'ERPs by country')"}


def tasa_libre_riesgo():
    """FRED DGS10 (10-year Treasury, fecha reciente) y T5YIE (breakeven 5 anios) via herramientas.datos."""
    from herramientas import datos
    dgs10 = datos.fred_serie("DGS10", desde="2026-09-01")
    t5yie = datos.fred_serie("T5YIE", desde="2026-09-01")
    return {"rf_usd_10y": dgs10[-1][1] / 100, "fecha_rf_usd": str(dgs10[-1][0]),
            "inflacion_esperada_eua_5y": t5yie[-1][1] / 100, "fecha_inflacion_eua": str(t5yie[-1][0]),
            "fuente": "FRED DGS10 y T5YIE (ver herramientas/README.md 'Fuentes de datos')"}


def costo_capital(dam: dict, rf: dict, inflacion_mx: float, beta_u: float, deuda_en_estructura: float,
                  capitalizacion: float, tasa_marginal: float, kd_pretax: float) -> dict:
    """WACC en MXN. beta relevered con Hamada (deuda = arrendamientos, unica 'deuda' de WALMEX);
    r_f MXN = r_f USD ajustada por diferencial de inflacion esperada (Mexico vs EUA, metodo IFE aproximado);
    Ke = r_f + beta_L x ERP madura + CRP Mexico (Damodaran, ajustada por volatilidad)."""
    t = tasa_marginal
    crp = dam["crp_mexico"]["crp_ajustada_volatilidad"]
    erp = dam["erp_madura_eua"]
    beta_l = beta_u * (1 + (1 - t) * deuda_en_estructura / capitalizacion) if capitalizacion else beta_u
    rf_usd = rf["rf_usd_10y"]
    ke_usd = rf_usd + beta_l * erp + crp
    pi_mx, pi_us = inflacion_mx, rf["inflacion_esperada_eua_5y"]
    rf_mxn = (1 + rf_usd) * (1 + pi_mx) / (1 + pi_us) - 1
    ke_mxn = (1 + ke_usd) * (1 + pi_mx) / (1 + pi_us) - 1
    e, d = capitalizacion, deuda_en_estructura
    w = (e * ke_mxn + d * kd_pretax * (1 - t)) / (e + d) if (e + d) else ke_mxn
    return {"beta_desapalancada": beta_u, "beta_relevered": beta_l, "deuda_en_estructura": d, "capitalizacion": e,
            "rf_usd": rf_usd, "rf_mxn_estimada": rf_mxn, "erp_madura_eua": erp, "crp_mexico": crp,
            "ke_usd": ke_usd, "ke_mxn": ke_mxn, "kd_antes_impuestos": kd_pretax,
            "kd_despues_impuestos": kd_pretax * (1 - t), "tasa_marginal": t,
            "inflacion_esperada_mx": pi_mx, "inflacion_esperada_eua": pi_us,
            "peso_capital": e / (e + d) if (e + d) else 1.0, "wacc": w,
            "naturaleza": "calculo con insumos citados (Damodaran, FRED); beta, ERP, CRP e inflacion esperada de "
                          "Mexico son estimaciones de mercado, no hechos del emisor"}


def construir_dcf_inverso(hist: list) -> dict:
    p25, p26h1 = hist[1], hist[2]
    ing_1s25 = 487228.410  # F4: Q1+Q2 2025 Total revenues (miles/1000), ver notas-y-modelo.md
    ing_ttm = p25["resultados"]["ingresos"] - ing_1s25 + p26h1["resultados"]["ingresos"]

    precio = 45.81      # Yahoo WALMEX.MX, cierre 2026-09-23 (ultimo cierre disponible al 2026-09-25; F8)
    fecha_precio = "2026-09-23"
    acciones = 17220.231803    # F3 p.34: 'Numero de acciones en circulacion' a 30-jun-2026 (no hay dilucion, F3 p.81)
    caja_jun26 = p26h1["balance"]["caja"]
    arr_jun26 = p26h1["balance"]["arrendamientos_financieros"]
    deuda_neta_sin_arr = -caja_jun26
    deuda_neta_con_arr = arr_jun26 - caja_jun26

    dam = leer_damodaran()
    rf = tasa_libre_riesgo()
    inflacion_mx = 0.037   # F6 p.61: inflacion Mexico 2025 (hecho realizado, usado como proxy de esperada; supuesto)
    tasa_marginal = 0.30   # F1 Nota 16: tasa ISR Mexico
    capitalizacion = precio * acciones
    int_arr_25 = 9115.155
    arr_prom_25 = (79729.903 + 80848.147) / 2
    kd_arrendamientos = int_arr_25 / arr_prom_25

    w_arr = costo_capital(dam, rf, inflacion_mx, dam["beta_emergentes_retail"]["beta_desapalancada_corregida_caja"],
                          arr_jun26, capitalizacion, tasa_marginal, kd_arrendamientos)
    w_sin_arr = costo_capital(dam, rf, inflacion_mx, dam["beta_emergentes_retail"]["beta_desapalancada_corregida_caja"],
                              0.0, capitalizacion, tasa_marginal, 0.0)
    w_global = costo_capital(dam, rf, inflacion_mx, dam["beta_global_retail"]["beta_desapalancada_corregida_caja"],
                             arr_jun26, capitalizacion, tasa_marginal, kd_arrendamientos)

    def margen_fcf_despues_arr(p):
        f = p["flujo"]
        fcf = f["cfo"] - f["capex"] - f["principal_arrendamientos_financieros"]
        return fcf / p["resultados"]["ingresos"]

    m24, m25 = margen_fcf_despues_arr(hist[0]), margen_fcf_despues_arr(hist[1])
    m_prom = (m24 + m25) / 2
    anos, g0 = 10, 0.045
    w0 = w_arr["wacc"]

    def correr(w, g, m, dn, p=precio):
        r = mi.dcf_inverso(p, acciones, dn, w, g, m, anos, ingresos_base=ing_ttm,
                           tasa_libre_riesgo=w_arr["rf_mxn_estimada"])
        sol = r.get("solucion") or {}
        return {"wacc": w, "g_terminal": g, "margen_fcf": m, "deuda_neta": dn, "precio": p, "estado": r["estado"],
                "crecimiento_implicito": r["crecimiento_implicito"], "peso_terminal": sol.get("peso_terminal"),
                "residuo": r.get("residuo"), "alertas": r["alertas"],
                "valor_por_accion_en_solucion": r.get("valor_por_accion_en_solucion")}

    base_run = mi.dcf_inverso(precio, acciones, deuda_neta_con_arr, w0, g0, m25, anos, ingresos_base=ing_ttm,
                              tasa_libre_riesgo=w_arr["rf_mxn_estimada"])
    rejilla = []
    for etq, m in (("FY2024", m24), ("FY2025", m25), ("promedio 2024-2025", m_prom)):
        for w in (w0 - 0.01, w0, w0 + 0.01):
            for g in (g0 - 0.01, g0, g0 + 0.01):
                x = correr(w, g, m, deuda_neta_con_arr)
                x["margen_etiqueta"] = etq
                rejilla.append(x)
    variantes = {
        "sin_arrendamientos_como_deuda": correr(w_sin_arr["wacc"], g0, m25, deuda_neta_sin_arr),
        "beta_global_en_vez_de_emergentes": correr(w_global["wacc"], g0, m25, deuda_neta_con_arr),
        "margen_FCF_promedio_2024_2025": correr(w0, g0, m_prom, deuda_neta_con_arr),
        "g_terminal_3.0pct": correr(w0, 0.03, m25, deuda_neta_con_arr),
        "g_terminal_5.5pct": correr(w0, 0.055, m25, deuda_neta_con_arr),
        "wacc_menos_100pb": correr(w0 - 0.01, g0, m25, deuda_neta_con_arr),
        "wacc_mas_100pb": correr(w0 + 0.01, g0, m25, deuda_neta_con_arr),
    }
    return {
        "naturaleza": "calculo: crecimiento anual constante de ingresos (10 anos) que descuenta el precio de "
                      "cierre bajo supuestos EXPLICITOS de WACC, g terminal y margen FCF; NO es pronostico ni "
                      "recomendacion de compra o venta (FASE 0).",
        "insumos": {"precio": precio, "fecha_precio": fecha_precio, "acciones_millones": acciones,
                    "capitalizacion": capitalizacion, "ingresos_base_ttm_jun26": ing_ttm,
                    "ingresos_1s2025_para_ttm": ing_1s25, "caja_jun26": caja_jun26,
                    "arrendamientos_jun26": arr_jun26, "deuda_neta_sin_arrendamientos": deuda_neta_sin_arr,
                    "deuda_neta_con_arrendamientos": deuda_neta_con_arr, "g_terminal": g0, "anos": anos,
                    "definicion_deuda_neta": "deuda financiera (=0, WALMEX no tiene deuda financiera) + "
                                             "arrendamientos IFRS16 (si se cuentan como deuda) - caja, a jun-2026",
                    "definicion_margen": "FCF despues de arrendamientos / ingresos totales = (CFO - capex - "
                                         "principal de arrendamientos) / ingresos (mismo calculo que el control "
                                         "C12 del motor sobre el historico reportado)"},
        "damodaran": dam, "tasa_libre_riesgo": rf,
        "wacc_con_arrendamientos_como_deuda": w_arr, "wacc_sin_arrendamientos": w_sin_arr,
        "wacc_beta_global": w_global, "kd_arrendamientos_implicita": kd_arrendamientos,
        "margen_fcf_fy2024": m24, "margen_fcf_fy2025": m25, "margen_fcf_promedio": m_prom,
        "base": {k: base_run[k] for k in ("estado", "crecimiento_implicito", "residuo", "alertas")},
        "base_valor_por_accion_en_solucion": base_run.get("valor_por_accion_en_solucion"),
        "base_solucion": (base_run.get("solucion") or {}),
        "sensibilidad": rejilla, "variantes": variantes,
    }


# ------------------------------------------------------------------ escenarios de mecanismo (supuestos explicitos)

def construir_supuestos() -> dict:
    """Tres escenarios de MECANISMO (no pronosticos): 'tension' (consumo debil sostenido + presion de costos +
    disciplina de capital defensiva), 'intermedio' (continuidad de las tendencias 2024-2025), 'eficiencia'
    (aceleracion de e-commerce/automatizacion de cadena de suministro segun el Programa de Inversion 2026, F7,
    con apalancamiento operativo y mejor capital de trabajo). Los niveles de partida son los drivers implicitos
    FY2025 (ver notas-y-modelo.md s3); las desviaciones y su razon se documentan ahi mismo."""
    return {
        "anos": 5, "caja_minima": 20000.0,
        "nota": "Supuestos de escenario (mecanismo); no son pronosticos, guia del emisor ni consenso.",
        "fuente_supuestos": "notas-y-modelo.md s4; niveles de partida = drivers implicitos FY2025 (base.json)",
        "escenarios": {
            "tension": {
                "descripcion": "Consumo debil sostenido (entorno descrito por el propio emisor en 2T26, F3), "
                    "compresion de margen por mayor promocionalidad, costo de fondeo de arrendamientos al alza, "
                    "y respuesta defensiva: recorte de capex y pausa de recompras.",
                "fuente_supuestos": "notas-y-modelo.md s4.1",
                "crecimiento_ingresos": 0.020, "margen_bruto": 0.237, "margen_operativo": 0.070,
                "tasa_impuestos": 0.30, "da_ventas": 0.026, "capex_ventas": 0.035, "sbc_ventas": 0.0003,
                "dias_cxc": 10.0, "dias_inventario": 55.0, "dias_proveedores": 55.0,
                "tasa_interes": 0.11, "tasa_arrendamientos_financieros": 0.115, "tasa_revolvente": 0.13,
                "nuevos_arrendamientos_financieros": 6000.0, "dividendos_payout": 0.45, "recompras": 0.0,
            },
            "intermedio": {
                "descripcion": "Continuidad de las tendencias 2024-2025 (crecimiento ~4-5%, margenes estables, "
                    "capital de trabajo similar al historico reciente).",
                "fuente_supuestos": "notas-y-modelo.md s4.2",
                "crecimiento_ingresos": 0.045, "margen_bruto": 0.242, "margen_operativo": 0.078,
                "tasa_impuestos": 0.27, "da_ventas": 0.025, "capex_ventas": 0.040, "sbc_ventas": 0.0003,
                "dias_cxc": 9.5, "dias_inventario": 52.0, "dias_proveedores": 59.0,
                "tasa_interes": 0.10, "tasa_arrendamientos_financieros": 0.11, "tasa_revolvente": 0.12,
                "nuevos_arrendamientos_financieros": 8000.0, "dividendos_payout": 0.58, "recompras": 8000.0,
            },
            "eficiencia": {
                "descripcion": "Aceleracion de e-commerce/On-Demand y automatizacion de cadena de suministro "
                    "(Centros de Distribucion de Guanajuato y Tlaxcala anunciados para 2027, F7), apalancamiento "
                    "operativo y mejor negociacion con proveedores (mas dias de cuentas por pagar).",
                "fuente_supuestos": "notas-y-modelo.md s4.3",
                "crecimiento_ingresos": 0.070, "margen_bruto": 0.246, "margen_operativo": 0.085,
                "tasa_impuestos": 0.27, "da_ventas": 0.024, "capex_ventas": 0.043, "sbc_ventas": 0.0003,
                "dias_cxc": 9.0, "dias_inventario": 48.0, "dias_proveedores": 63.0,
                "tasa_interes": 0.10, "tasa_arrendamientos_financieros": 0.105, "tasa_revolvente": 0.115,
                "nuevos_arrendamientos_financieros": 10000.0, "dividendos_payout": 0.60, "recompras": 10000.0,
            },
        },
    }


# ------------------------------------------------------------------ ensamblado de base.json y corrida

def construir_base() -> dict:
    hist = construir_historico()
    return {
        "empresa": "Wal-Mart de Mexico, S.A.B. de C.V. (Walmart de Mexico y Centroamerica)", "ticker": "WALMEX.MX",
        "moneda": "MXN", "unidades": "millones", "fecha_corte": "2026-09-25",
        "aviso": "FASE 0 (formacion): no es recomendacion de compra o venta. Escenarios = supuestos de "
                 "mecanismo, no pronosticos. WALMEX no reporta ante la SEC; fuente = BMV/Emisnet y "
                 "walmex.mx (Relacion con Inversionistas).",
        "fuentes": FUENTES,
        "historico": hist,
        "supuestos": construir_supuestos(),
    }


def main(argv) -> int:
    fallas_huellas = huellas.verificar(str(DATOS / "SHA256SUMS.txt"))
    base = construir_base()
    mi.guardar_json(base, AQUI / "base.json")
    res = mi.construir_modelo(base)
    dc = doble_comprobacion(base["historico"])
    dcf = construir_dcf_inverso(base["historico"])
    res["doble_comprobacion"] = dc
    res["dcf_inverso"] = dcf
    mi.guardar_json(res, AQUI / "resultados.json")
    releido = mi.cargar_json(AQUI / "resultados.json")
    auditoria = mi.resumir_controles(mi.verificar(releido))
    coincide = all(auditoria[k] == res["resumen_controles"][k] for k in ("total", "OK", "FALLA", "INFO", "NO_APLICA"))
    mi.escribir_sha256sums([AQUI / "base.json", AQUI / "modelo.py", AQUI / "resultados.json"], AQUI / "SHA256SUMS.txt")
    print(mi.resumen_markdown(res))
    print(f"\nDoble comprobacion (segunda lectura F5/F6): {dc['ok']}/{dc['total']} cifras OK")
    if dc["fallas"]:
        for x in dc["fallas"]:
            print("  FALLA:", x)
    print(f"DCF inverso: WACC (arrendamientos como deuda) {dcf['wacc_con_arrendamientos_como_deuda']['wacc']:.4%}, "
          f"g terminal {dcf['insumos']['g_terminal']:.2%}, margen FCF FY2025 {dcf['margen_fcf_fy2025']:.4%} -> "
          f"crecimiento implicito {dcf['base']['crecimiento_implicito']:.4%} ({dcf['base']['estado']})")
    print(f"Huellas de datos/: {'OK' if not fallas_huellas else fallas_huellas}")
    print(f"Auditoria de resultados.json releido: {'coincide' if coincide else 'NO COINCIDE'} "
          f"({auditoria['total']} registros, FALLA {auditoria['FALLA']})")
    ok = res["resumen_controles"]["todos_ok"] and coincide and not fallas_huellas and not dc["fallas"]
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
