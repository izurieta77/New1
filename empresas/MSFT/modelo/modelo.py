"""MSFT: modelo integrado de 3 estados (FY2024-FY2026 historico; FY2027E-FY2031E escenarios de mecanismo).

FASE 0 (formacion). Los escenarios son supuestos de MECANISMO, no pronosticos, guia ni consenso; nada aqui es
recomendacion de compra o venta. Solo biblioteca estandar (Python 3.11).

Que hace, en orden:
  0. Verifica las huellas SHA-256 de los insumos congelados (datos/SHA256SUMS.txt, herramientas/huellas.py).
  1. construir_modelo(base.json): reconcilia el historico (C13) y proyecta tension / intermedio / eficiencia.
  2. Doble comprobacion de la transcripcion: cada cifra de base.json tecleada desde los visores R de la SEC
     (primera lectura) se compara con los hechos XBRL de companyfacts (segunda lectura, automatica).
  3. Indicadores de las notas (FCF antes y despues de principal de arrendamientos, SBC, recompras, OpenAI, ...).
  4. DCF inverso (precio Yahoo 2026-09-24) con WACC y g terminal explicitos y mallas de sensibilidad.
  5. Sensibilidad geopolitica de mecanismo (choque de suministro sobre el escenario intermedio).
Salida: resultados.json y SHA256SUMS.txt. Codigo de salida 1 si falla cualquier control o comprobacion.

Uso (desde la raiz del repo o desde cualquier lugar):  python3 empresas/MSFT/modelo/modelo.py
"""
import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[2]))
from herramientas import huellas  # noqa: E402
from herramientas import modelo_integrado as mi  # noqa: E402

DATOS = AQUI / "datos"
TOL_TRANSCRIPCION = 0.5  # millones: las cifras publicadas son enteras; cualquier diferencia >= 1 se reporta

PERIODOS = {"FY2024": ("2023-07-01", "2024-06-30", "2023-06-30"),
            "FY2025": ("2024-07-01", "2025-06-30", "2024-06-30"),
            "FY2026": ("2025-07-01", "2026-06-30", "2025-06-30")}

# campo de base.json -> [(concepto XBRL, signo)]; 'D' = duracion del ejercicio, 'I' = saldo al cierre,
# 'I0' = saldo al cierre del ejercicio previo.
MAPA = {
    ("resultados", "ingresos"): ("D", [("RevenueFromContractWithCustomerExcludingAssessedTax", 1)]),
    ("resultados", "costo_ventas"): ("D", [("CostOfGoodsAndServicesSold", 1)]),
    ("resultados", "utilidad_bruta"): ("D", [("GrossProfit", 1)]),
    ("resultados", "gastos_operativos"): ("D", [("OperatingExpenses", 1)]),
    ("resultados", "utilidad_operativa"): ("D", [("OperatingIncomeLoss", 1)]),
    ("resultados", "gasto_intereses"): ("D", [("InterestExpenseNonoperating", 1)]),
    ("resultados", "ingreso_intereses"): ("D", [("InvestmentIncomeNet", 1)]),
    ("resultados", "otros_ingresos"): ("D", [("GainLossOnInvestments", 1), ("GainLossOnDerivativeInstrumentsNetPretax", 1),
                                             ("ForeignCurrencyTransactionGainLossBeforeTax", 1),
                                             ("OtherNonoperatingIncomeExpense", 1)]),
    ("resultados", "utilidad_antes_impuestos"): ("D", [(
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", 1)]),
    ("resultados", "impuestos"): ("D", [("IncomeTaxExpenseBenefit", 1)]),
    ("resultados", "utilidad_neta"): ("D", [("NetIncomeLoss", 1)]),
    ("balance", "caja"): ("I", [("CashAndCashEquivalentsAtCarryingValue", 1)]),
    ("balance", "inversiones_cp"): ("I", [("ShortTermInvestments", 1)]),
    ("balance", "cuentas_por_cobrar"): ("I", [("AccountsReceivableNetCurrent", 1)]),
    ("balance", "inventarios"): ("I", [("InventoryNet", 1)]),
    ("balance", "otros_activos_circulantes"): ("I", [("OtherAssetsCurrent", 1)]),
    ("balance", "ppe_neto"): ("I", [("PropertyPlantAndEquipmentNet", 1)]),
    ("balance", "otros_activos_lp"): ("I", [("OperatingLeaseRightOfUseAsset", 1), ("LongTermInvestments", 1), ("Goodwill", 1),
                                            ("FiniteLivedIntangibleAssetsNet", 1), ("OtherAssetsNoncurrent", 1)]),
    ("balance", "activo_total"): ("I", [("Assets", 1)]),
    ("balance", "proveedores"): ("I", [("AccountsPayableCurrent", 1)]),
    ("balance", "deuda"): ("I", [("LongTermDebtCurrent", 1), ("LongTermDebtNoncurrent", 1), ("CommercialPaper?", 1)]),
    ("balance", "arrendamientos_financieros"): ("I", [("FinanceLeaseLiability", 1)]),
    ("balance", "pasivo_total"): ("I", [("Liabilities", 1)]),
    ("balance", "capital_contable"): ("I", [("StockholdersEquity", 1)]),
    ("balance", "utilidades_retenidas"): ("I", [("RetainedEarningsAccumulatedDeficit", 1)]),
    ("flujo", "sbc"): ("D", [("ShareBasedCompensation", 1)]),
    ("flujo", "cfo"): ("D", [("NetCashProvidedByUsedInOperatingActivities", 1)]),
    ("flujo", "capex"): ("D", [("PaymentsToAcquirePropertyPlantAndEquipment", 1)]),
    ("flujo", "cfi"): ("D", [("NetCashProvidedByUsedInInvestingActivities", 1)]),
    ("flujo", "cff"): ("D", [("NetCashProvidedByUsedInFinancingActivities", 1)]),
    ("flujo", "dividendos"): ("D", [("PaymentsOfDividendsCommonStock", 1)]),
    ("flujo", "recompras"): ("D", [("PaymentsForRepurchaseOfCommonStock", 1)]),
    ("flujo", "emision_acciones"): ("D", [("ProceedsFromIssuanceOfCommonStock", 1)]),
    ("flujo", "principal_arrendamientos_financieros"): ("D", [("FinanceLeasePrincipalPayments", 1)]),
    ("flujo", "efecto_cambiario"): ("D", [(
        "EffectOfExchangeRateOnCashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsIncludingDisposalGroupAndDiscontinuedOperations", 1)]),
    ("flujo", "caja_final"): ("I", [("CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", 1)]),
    ("flujo", "caja_inicial"): ("I0", [("CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", 1)]),
    ("flujo", "utilidad_neta"): ("D", [("NetIncomeLoss", 1)]),
    ("flujo", "cambio_capital_trabajo"): ("D", [
        ("IncreaseDecreaseInAccountsReceivable", -1), ("IncreaseDecreaseInInventories", -1),
        ("IncreaseDecreaseInOtherCurrentAssets", -1), ("IncreaseDecreaseInOtherNoncurrentAssets", -1),
        ("IncreaseDecreaseInAccountsPayable", 1), ("IncreaseDecreaseInContractWithCustomerLiability", 1),
        ("IncreaseDecreaseInAccruedIncomeTaxesPayable", 1), ("IncreaseDecreaseInOtherCurrentLiabilities", 1),
        ("IncreaseDecreaseInOtherNoncurrentLiabilities", 1)]),
    ("movimientos_capital", "capital_inicial"): ("I0", [("StockholdersEquity", 1)]),
    ("movimientos_capital", "utilidades_retenidas_iniciales"): ("I0", [("RetainedEarningsAccumulatedDeficit", 1)]),
    ("movimientos_capital", "sbc"): ("D", [("ShareBasedCompensation", 1)]),
    ("movimientos_capital", "ori"): ("D", [("OtherComprehensiveIncomeLossNetOfTaxPortionAttributableToParent", 1)]),
    ("movimientos_capital", "dividendos_declarados"): ("D", [("DividendsCommonStockCash", 1)]),
}
# componentes de detalle {campo: {concepto del filing: [(concepto XBRL, signo)]}}
MAPA_DETALLE = {
    "otros_operativos": {"Deferred income taxes": [("DeferredIncomeTaxesAndTaxCredits", 1)]},
    "otros_inversion": {"Purchases of investments": [("PaymentsToAcquireInvestments", -1)],
                        "Maturities of investments": [("ProceedsFromMaturitiesPrepaymentsAndCallsOfAvailableForSaleSecurities", 1)],
                        "Other, net": [("PaymentsForProceedsFromOtherInvestingActivities", -1)]},
    "otros_financiamiento": {"Other, net (reportado)": [("ProceedsFromPaymentsForOtherFinancingActivities", 1)]},
}
# diferencias conocidas y explicadas (no son error de transcripcion)
EXPLICADAS = {
    ("FY2025", "movimientos_capital.dividendos_declarados"):
        "estado de variaciones (R7) 24,677 vs suma de la Nota 15 (hecho XBRL) 24,676: redondeo del emisor",
    ("FY2026", "movimientos_capital.dividendos_declarados"):
        "estado de variaciones (R7) 27,034 vs suma de la Nota 15 (hecho XBRL) 27,035: redondeo del emisor",
}


def _indice_xbrl():
    ext = mi.cargar_json(DATOS / "xbrl_companyfacts_msft_extracto.json")
    idx = {}
    for h in ext["hechos"]:
        if h["unidad"] not in ("USD", "shares"):
            continue
        clave = (h["concepto"], h["inicio"], h["fin"])
        # varias presentaciones: se prefiere la mas reciente (el extracto ya trae una sola por saldo historico)
        if clave not in idx or h["presentado"] > idx[clave]["presentado"]:
            idx[clave] = h
    return ext, idx


def _valor_xbrl(idx, tipo, conceptos, per):
    ini, fin, fin_prev = PERIODOS[per]
    total, usados, faltan = 0.0, [], []
    for concepto, signo in conceptos:
        opcional = concepto.endswith("?")
        c = concepto.rstrip("?")
        clave = (c, ini, fin) if tipo == "D" else (c, None, fin if tipo == "I" else fin_prev)
        h = idx.get(clave)
        if h is None:
            if not opcional:
                faltan.append(c)
            continue
        total += signo * h["valor"] / 1e6
        usados.append(f"{'-' if signo < 0 else ''}{c} [{h['accn']}]")
    return (None if faltan else total), usados, faltan


def doble_comprobacion(base: dict) -> dict:
    """Primera lectura (base.json, tecleada desde los visores R) contra segunda lectura (XBRL companyfacts)."""
    ext, idx = _indice_xbrl()
    filas = []
    for p in base["historico"]:
        per = p["periodo"]
        for (sec, campo), (tipo, conceptos) in MAPA.items():
            bloque = p.get(sec) or {}
            if campo not in bloque:
                continue
            v = bloque[campo]
            v = sum(v.values()) if isinstance(v, dict) else v
            x, usados, faltan = _valor_xbrl(idx, tipo, conceptos, per)
            etiqueta = f"{sec}.{campo}"
            if x is None:
                estado, dif = "SIN_XBRL", None
            else:
                dif = v - x
                if abs(dif) <= TOL_TRANSCRIPCION:
                    estado = "OK"
                elif (per, etiqueta) in EXPLICADAS:
                    estado = "DIFERENCIA_EXPLICADA"
                else:
                    estado = "FALLA"
            filas.append({"periodo": per, "campo": etiqueta, "base": v, "xbrl": x, "diferencia": dif, "estado": estado,
                          "conceptos": usados, "faltan": faltan, "explicacion": EXPLICADAS.get((per, etiqueta))})
        # detalle del flujo
        for campo, comps in MAPA_DETALLE.items():
            det = (p.get("flujo") or {}).get(campo)
            if not isinstance(det, dict):
                continue
            for concepto_filing, conceptos in comps.items():
                if concepto_filing not in det:
                    continue
                x, usados, faltan = _valor_xbrl(idx, "D", conceptos, per)
                v = det[concepto_filing]
                estado = "SIN_XBRL" if x is None else ("OK" if abs(v - x) <= TOL_TRANSCRIPCION else "FALLA")
                filas.append({"periodo": per, "campo": f"flujo.{campo}[{concepto_filing}]", "base": v, "xbrl": x,
                              "diferencia": None if x is None else v - x, "estado": estado, "conceptos": usados,
                              "faltan": faltan, "explicacion": None})
        # suma de otros pasivos contra el total XBRL (el reparto circulante/LP depende del arrendamiento financiero,
        # que en XBRL no dimensional solo viene como total)
        b = p["balance"]
        x, usados, faltan = _valor_xbrl(idx, "I", [("Liabilities", 1), ("AccountsPayableCurrent", -1),
                                                   ("LongTermDebtCurrent", -1), ("LongTermDebtNoncurrent", -1),
                                                   ("CommercialPaper?", -1), ("FinanceLeaseLiability", -1)], per)
        v = b["otros_pasivos_circulantes"] + b["otros_pasivos_lp"]
        filas.append({"periodo": per, "campo": "balance.otros_pasivos_circulantes + otros_pasivos_lp", "base": v,
                      "xbrl": x, "diferencia": None if x is None else v - x,
                      "estado": "SIN_XBRL" if x is None else ("OK" if abs(v - x) <= TOL_TRANSCRIPCION else "FALLA"),
                      "conceptos": usados, "faltan": faltan, "explicacion": None})
    # memo FY2026 (notas) con contraparte XBRL no dimensional
    memo = base["historico"][-1]["memo"]
    memo_chk = [
        ("memo.arrendamientos.operativo_total", memo["arrendamientos"]["operativo_total"], [("OperatingLeaseLiability", 1)], "I"),
        ("memo.arrendamientos.operativo_lp", memo["arrendamientos"]["operativo_lp"], [("OperatingLeaseLiabilityNoncurrent", 1)], "I"),
        ("memo.arrendamientos.derecho_de_uso_operativo", memo["arrendamientos"]["derecho_de_uso_operativo"],
         [("OperatingLeaseRightOfUseAsset", 1)], "I"),
        ("memo.arrendamientos.pagos_no_descontados_financieros.total",
         memo["arrendamientos"]["pagos_no_descontados_financieros"]["total"], [("FinanceLeaseLiabilityPaymentsDue", 1)], "I"),
        ("memo.arrendamientos.pagos_no_descontados_operativos.total",
         memo["arrendamientos"]["pagos_no_descontados_operativos"]["total"], [("LesseeOperatingLeaseLiabilityPaymentsDue", 1)], "I"),
        ("memo.arrendamientos.derecho_de_uso_obtenido.financiero", memo["arrendamientos"]["derecho_de_uso_obtenido"]["financiero"],
         [("RightOfUseAssetObtainedInExchangeForFinanceLeaseLiability", 1)], "D"),
        ("memo.arrendamientos.costo.interes_financiero", memo["arrendamientos"]["costo"]["interes_financiero"],
         [("FinanceLeaseInterestExpense", 1)], "D"),
        ("memo.ppe.depreciacion", memo["ppe"]["depreciacion"], [("Depreciation", 1)], "D"),
        ("memo.inversiones_metodo_de_participacion", memo["inversiones_metodo_de_participacion"]["monto"],
         [("EquityMethodInvestments", 1)], "I"),
        ("memo.inversiones_restringidas.total", memo["inversiones_restringidas_por_contrato_con_proveedor"]["total"],
         [("RestrictedInvestments", 1)], "I"),
        ("memo.obligaciones_de_desempeno_pendientes", memo["obligaciones_de_desempeno_pendientes"]["monto"],
         [("RevenueRemainingPerformanceObligation", 1)], "I"),
        ("memo.impuestos.impuestos_pagados", memo["impuestos"]["impuestos_pagados"], [("IncomeTaxesPaidNet", 1)], "D"),
        ("memo.deuda.valor_nominal", memo["deuda"]["valor_nominal"], [("DebtInstrumentCarryingAmount", 1)], "I"),
        ("memo.deuda.valor_razonable", memo["deuda"]["valor_razonable"], [("LongTermDebtFairValue", 1)], "I"),
        ("memo.deuda.intereses_pagados", memo["deuda"]["intereses_pagados"], [("InterestPaid", 1)], "D"),
        ("memo.recompras.retenciones_fiscales_excluidas", memo["recompras"]["retenciones_fiscales_excluidas"],
         [("PaymentsRelatedToTaxWithholdingForShareBasedCompensation", 1)], "D"),
        ("memo.dividendos_declarados_nota15.monto", memo["dividendos_declarados_nota15"]["monto"],
         [("DividendsCommonStockCash", 1)], "D"),
        ("memo.acciones.promedio_diluidas_FY2026", memo["acciones"]["promedio_diluidas_FY2026"],
         [("WeightedAverageNumberOfDilutedSharesOutstanding", 1)], "D"),
        ("memo.acciones.incrementales_por_sbc", memo["acciones"]["incrementales_por_sbc"],
         [("IncrementalCommonSharesAttributableToShareBasedPaymentArrangements", 1)], "D"),
        ("memo.sbc.beneficio_fiscal", memo["sbc"]["beneficio_fiscal"],
         [("EmployeeServiceShareBasedCompensationTaxBenefitFromCompensationExpense", 1)], "D"),
    ]
    for etq, v, conceptos, tipo in memo_chk:
        x, usados, faltan = _valor_xbrl(idx, tipo, conceptos, "FY2026")
        filas.append({"periodo": "FY2026", "campo": etq, "base": v, "xbrl": x, "diferencia": None if x is None else v - x,
                      "estado": "SIN_XBRL" if x is None else ("OK" if abs(v - x) <= TOL_TRANSCRIPCION else "FALLA"),
                      "conceptos": usados, "faltan": faltan, "explicacion": None})
    cuenta = {e: sum(1 for f in filas if f["estado"] == e) for e in ("OK", "DIFERENCIA_EXPLICADA", "FALLA", "SIN_XBRL")}
    return {"naturaleza": "control de transcripcion: primera lectura = visores R de la SEC tecleados en base.json; "
                          "segunda lectura = hechos XBRL no dimensionales de companyfacts (misma presentacion)",
            "extracto": {"archivo": "datos/xbrl_companyfacts_msft_extracto.json",
                         "sha256_companyfacts_completo": ext["sha256_archivo_completo"]},
            "tolerancia_millones": TOL_TRANSCRIPCION, **cuenta, "todos_ok": cuenta["FALLA"] == 0,
            "sin_contraparte_xbrl_no_dimensional": "D&A ('Depreciation, amortization, and other'), ganancias en inversiones "
                "del flujo, adquisiciones y ventas de inversiones, deuda de 90 dias o menos, reparto circulante/LP del "
                "arrendamiento financiero y columnas del estado de variaciones son conceptos propios del emisor o "
                "dimensionales: se prueban por identidad aritmetica (C01-C04, C07, C15) y quedan con estado SIN_XBRL o "
                "fuera de esta tabla",
            "filas": filas}


def indicadores_notas(base: dict, res: dict) -> dict:
    """Calculo sobre hechos del filing (no supuestos)."""
    h = {p["periodo"]: p for p in base["historico"]}
    out = {"naturaleza": "calculo sobre hechos (F1/F2/F3)", "fcf": {}}
    for per, p in h.items():
        r, f = p["resultados"], p["flujo"]
        fcf = f["cfo"] - f["capex"]
        fcf2 = fcf - f["principal_arrendamientos_financieros"]
        out["fcf"][per] = {
            "cfo": f["cfo"], "capex_efectivo": f["capex"], "fcf_cfo_menos_capex": fcf,
            "principal_arrendamientos_financieros": f["principal_arrendamientos_financieros"],
            "fcf_despues_de_principal": fcf2, "fcf_menos_sbc": fcf - f["sbc"],
            "fcf_despues_de_principal_menos_sbc": fcf2 - f["sbc"],
            "margen_fcf": fcf / r["ingresos"], "margen_fcf_despues_de_principal": fcf2 / r["ingresos"],
            "margen_fcf_menos_sbc": (fcf - f["sbc"]) / r["ingresos"],
            "conversion_fcf_sobre_utilidad_neta": fcf / r["utilidad_neta"],
            "capex_sobre_ingresos": f["capex"] / r["ingresos"],
            "da_sobre_ingresos": f["depreciacion_amortizacion"] / r["ingresos"],
            "capex_sobre_da": f["capex"] / f["depreciacion_amortizacion"],
        }
    m26, m25, m24 = h["FY2026"]["memo"], h["FY2025"]["memo"], h["FY2024"]["memo"]
    inv26 = (h["FY2026"]["flujo"]["capex"] + (m26["ppe"]["compras_en_cuentas_por_pagar"] - m25["ppe_compras_en_cuentas_por_pagar"]["monto"])
             + m26["arrendamientos"]["derecho_de_uso_obtenido"]["financiero"])
    inv25 = (h["FY2025"]["flujo"]["capex"] + (m25["ppe_compras_en_cuentas_por_pagar"]["monto"] - m24["ppe_compras_en_cuentas_por_pagar"]["monto"])
             + m25["arrendamientos"]["derecho_de_uso_obtenido_financiero"])
    out["inversion_en_activos_devengada_aprox"] = {
        "definicion": "capex en efectivo + aumento de compras de PPE por pagar + derecho de uso obtenido por arrendamiento "
                      "financiero (Inferencia: aproxima la inversion devengada; no incluye arrendamientos operativos)",
        "FY2025": inv25, "FY2026": inv26,
        "FY2026_sobre_ingresos": inv26 / h["FY2026"]["resultados"]["ingresos"]}
    r26, r25 = h["FY2026"]["resultados"], h["FY2025"]["resultados"]
    aj = res["historico"]["ajustado"]
    out["gaap_vs_ajustado"] = {"filas": aj,
                               "crecimiento_utilidad_neta_gaap": r26["utilidad_neta"] / r25["utilidad_neta"] - 1,
                               "crecimiento_utilidad_neta_sin_openai": aj[-1]["crecimiento_ajustado"]}
    oa = m26["openai"]
    out["openai"] = {"ingresos_sobre_ingresos_totales": oa["ingresos_por_acuerdos_comerciales"] / r26["ingresos"],
                     "cxc_sobre_cxc_totales": oa["cuentas_por_cobrar"] / h["FY2026"]["balance"]["cuentas_por_cobrar"],
                     "resultado_antes_impuestos_sobre_uai": oa["resultado_antes_impuestos_en_otros_ingresos"] / r26["utilidad_antes_impuestos"],
                     "compromiso_pendiente_de_fondeo": oa["compromiso_de_fondeo_total"] - oa["fondeado"]}
    sb, rc = m26["sbc"], m26["recompras"]
    acc = rc["acciones_en_circulacion_millones"]
    out["sbc_y_recompras"] = {
        "sbc_sobre_ingresos": sb["gasto"] / r26["ingresos"],
        "costo_no_reconocido_en_anos_de_gasto_actual": sb["costo_no_reconocido"] / sb["gasto"],
        "recompras_flujo": rc["flujo_de_efectivo"], "recompras_programa": rc["programa_monto"],
        "retenciones_fiscales": rc["retenciones_fiscales_excluidas"],
        "programa_mas_retenciones_menos_flujo": rc["programa_monto"] + rc["retenciones_fiscales_excluidas"] - rc["flujo_de_efectivo"],
        "precio_promedio_programa_usd": rc["programa_monto"] / rc["programa_acciones_millones"],
        "cambio_neto_acciones_millones": acc["final"] - acc["inicial"],
        "cambio_neto_acciones_pct": acc["final"] / acc["inicial"] - 1,
        "recompras_flujo_menos_emision_acciones": rc["flujo_de_efectivo"] - h["FY2026"]["flujo"]["emision_acciones"],
    }
    ar = m26["arrendamientos"]
    out["arrendamientos"] = {
        "pasivo_reconocido_total": h["FY2026"]["balance"]["arrendamientos_financieros"] + ar["operativo_total"],
        "pagos_no_descontados_reconocidos": ar["pagos_no_descontados_financieros"]["total"] + ar["pagos_no_descontados_operativos"]["total"],
        "valor_presente_sobre_no_descontado_financieros": h["FY2026"]["balance"]["arrendamientos_financieros"]
        / ar["pagos_no_descontados_financieros"]["total"],
        "no_iniciados": ar["no_iniciados"]["monto"],
        "no_iniciados_sobre_pasivo_reconocido": ar["no_iniciados"]["monto"]
        / (h["FY2026"]["balance"]["arrendamientos_financieros"] + ar["operativo_total"]),
        "crecimiento_pasivo_financiero": h["FY2026"]["balance"]["arrendamientos_financieros"]
        / h["FY2025"]["balance"]["arrendamientos_financieros"] - 1,
    }
    b26 = h["FY2026"]["balance"]
    out["posicion_financiera_FY2026"] = {
        "deuda": b26["deuda"], "arrendamientos_financieros": b26["arrendamientos_financieros"],
        "caja_mas_inversiones_cp": b26["caja"] + b26["inversiones_cp"],
        "inversiones_cp_restringidas": m26["inversiones_restringidas_por_contrato_con_proveedor"]["en_inversiones_cp"],
        "deuda_neta_sin_arrendamientos": b26["deuda"] - b26["caja"] - b26["inversiones_cp"],
        "deuda_neta_con_arrendamientos_financieros_y_sin_restringidas":
            b26["deuda"] + b26["arrendamientos_financieros"] - b26["caja"]
            - (b26["inversiones_cp"] - m26["inversiones_restringidas_por_contrato_con_proveedor"]["en_inversiones_cp"]),
    }
    cfo_det = h["FY2026"]["flujo"]["otros_operativos"]
    out["calidad_cfo_FY2026"] = {
        "impuestos_diferidos_sumados_al_cfo": cfo_det["Deferred income taxes"],
        "ganancias_no_monetarias_restadas": cfo_det["Net recognized losses (gains) on investments and derivatives"],
        "cfo_sin_impuestos_diferidos": h["FY2026"]["flujo"]["cfo"] - cfo_det["Deferred income taxes"],
        "impuestos_diferidos_FY2025": h["FY2025"]["flujo"]["otros_operativos"]["Deferred income taxes"],
    }
    return out


def dcf_inverso(base: dict, ind: dict) -> dict:
    mk = base["mercado_y_dcf"]
    v = {k: (x["valor"] if isinstance(x, dict) and "valor" in x else x) for k, x in mk.items()}
    precio = v["precio"]
    acciones = v["acciones_basicas_portada"] + v["acciones_incrementales_sbc"]
    acciones_completa = v["acciones_basicas_portada"] + v["rsu_no_vestidas"]
    inv_cp_libres = v["inversiones_cp"] - v["inversiones_cp_restringidas"]
    deuda_neta = v["deuda"] + v["arrendamientos_financieros"] - v["caja"] - inv_cp_libres
    deuda_neta_con_inv_lp = deuda_neta - (v["inversiones_lp"] - v["inversiones_lp_restringidas"])
    # costo de capital (conocimiento/03 s2.3 y s6.1 regla 3)
    rf = v["tasa_bono_10a"] - v["diferencial_default_eua"]
    cap = precio * v["acciones_basicas_portada"]
    d_mkt = v["deuda"] + v["arrendamientos_financieros"]
    de = d_mkt / cap
    t = v["tasa_marginal_impuestos"]
    beta_l = v["beta_desapalancada"] * (1 + (1 - t) * de)
    ke = rf + beta_l * v["erp"]
    kd = v["tasa_bono_10a"] + v["diferencial_deuda"]
    wacc_calc = (cap * ke + d_mkt * kd * (1 - t)) / (cap + d_mkt)
    wacc = round(wacc_calc, 3)
    g = v["g_terminal"]
    dw, dg = v["sensibilidad_wacc_pp"], v["sensibilidad_g_pp"]
    anos = v["anos_explicitos"]
    ing = v["ingresos_base"]
    fcf = ind["fcf"]
    margen_base = fcf["FY2026"]["margen_fcf"]
    margenes = {"FY2026 CFO - capex - SBC": fcf["FY2026"]["margen_fcf_menos_sbc"],
                "FY2026 CFO - capex (base)": margen_base,
                "FY2025 CFO - capex": fcf["FY2025"]["margen_fcf"],
                "FY2024 CFO - capex": fcf["FY2024"]["margen_fcf"]}
    base_res = mi.dcf_inverso(precio, acciones, deuda_neta, wacc, g, margen_base, anos, ingresos_base=ing,
                              tasa_libre_riesgo=rf)
    sol = base_res.pop("solucion")
    base_res["solucion_resumen"] = {k: sol[k] for k in ("valor_empresa", "vp_flujos", "vp_terminal", "peso_terminal",
                                                        "multiplo_terminal_fcf")}
    base_res["solucion_resumen"]["ingresos_ano_10"] = sol["flujos"][-1]["ingresos"]
    base_res["solucion_resumen"]["fcf_ano_10"] = sol["flujos"][-1]["fcf"]
    waccs = [round(wacc - dw, 3), wacc, round(wacc + dw, 3)]
    gs = [round(g - dg, 4), g, round(g + dg, 4)]
    malla_wg = []
    for w in waccs:
        for gg in gs:
            r = mi.dcf_inverso(precio, acciones, deuda_neta, w, gg, margen_base, anos, ingresos_base=ing, tasa_libre_riesgo=rf)
            malla_wg.append({"wacc": w, "g_terminal": gg, "crecimiento_implicito": r["crecimiento_implicito"],
                             "estado": r["estado"], "peso_terminal": r.get("solucion", {}).get("peso_terminal"),
                             "alertas": r["alertas"]})
    malla_wm = []
    for w in waccs:
        for nombre, m in margenes.items():
            r = mi.dcf_inverso(precio, acciones, deuda_neta, w, g, m, anos, ingresos_base=ing)
            malla_wm.append({"wacc": w, "margen": nombre, "margen_fcf": m, "crecimiento_implicito": r["crecimiento_implicito"],
                             "estado": r["estado"]})
    variantes = {}
    for nombre, (acc_v, dn_v) in {"dilucion completa (78 M RSU no vestidas)": (acciones_completa, deuda_neta),
                                  "restando inversiones LP no restringidas a valor en libros": (acciones, deuda_neta_con_inv_lp)}.items():
        r = mi.dcf_inverso(precio, acc_v, dn_v, wacc, g, margen_base, anos, ingresos_base=ing, tasa_libre_riesgo=rf)
        variantes[nombre] = {"acciones": acc_v, "deuda_neta": dn_v, "crecimiento_implicito": r["crecimiento_implicito"],
                             "estado": r["estado"]}
    return {
        "naturaleza": "DCF inverso: crecimiento que descuenta el precio bajo supuestos explicitos; no es pronostico ni recomendacion",
        "insumos": {"precio": precio, "fecha_precio": mk["precio"]["fecha"], "acciones_diluidas_millones": acciones,
                    "definicion_acciones": "portada 23-jul-2026 + acciones incrementales por SBC (metodo de tesoreria, Nota 2)",
                    "deuda_neta": deuda_neta,
                    "definicion_deuda_neta": "deuda 40,294 + arrendamientos financieros 66,594 - caja 20,935 - inversiones CP "
                                             "no restringidas (55,908 - 3,800); arrendamientos operativos fuera porque su costo ya "
                                             "esta en el CFO",
                    "ingresos_base": ing, "margen_fcf_base": margen_base,
                    "definicion_fcf": "FCFF = CFO - capex (FY2026: 66,987 / 331,839); el interes de arrendamientos financieros "
                                      "ya esta dentro del CFO (sesgo menor, conservador)",
                    "anos_explicitos": anos},
        "costo_de_capital": {"r_f_ajustada": rf, "erp": v["erp"], "beta_desapalancada": v["beta_desapalancada"],
                             "d_sobre_e_mercado": de, "beta_reapalancada": beta_l, "k_e": ke, "k_d_antes_impuestos": kd,
                             "tasa_marginal": t, "wacc_calculado": wacc_calc, "wacc_usado": wacc, "g_terminal": g,
                             "nota": "beta de regresion 1 ano = 0.98 (dossier-2026-09-25); con ella k_e ~9.1% y WACC ~9.0%, "
                                     "cerca del caso WACC - 1 pp"},
        "base": base_res,
        "malla_wacc_x_g": malla_wg,
        "malla_wacc_x_margen": malla_wm,
        "variantes": variantes,
    }


def sensibilidad_geopolitica(base: dict, res: dict) -> dict:
    """Mecanismo: choque de suministro (Taiwan / controles de exportacion de chips / energia) aplicado 2 anos al
    escenario intermedio. Magnitudes = supuesto de escenario, sin probabilidad asignada."""
    sup = copy.deepcopy(base["supuestos"])
    esc = copy.deepcopy(sup["escenarios"]["intermedio"])
    choque = {"crecimiento_ingresos": [-0.04, -0.04, 0, 0, 0], "capex_ventas": [0.04, 0.04, 0, 0, 0],
              "margen_bruto": [-0.01, -0.01, 0, 0, 0], "margen_operativo": [-0.01, -0.01, 0, 0, 0]}
    for k, deltas in choque.items():
        serie = esc[k] if isinstance(esc[k], list) else [esc[k]] * sup["anos"]
        esc[k] = [round(a + d, 6) for a, d in zip(serie, deltas)]
    esc["descripcion"] = ("Intermedio con choque de suministro de 2 anos (FY2027E-FY2028E): -4 pp de crecimiento por "
                          "capacidad retrasada, +4 pp de capex/ventas por componentes mas caros, -1 pp de margen bruto y operativo")
    sup_v = {"anos": sup["anos"], "caja_minima": sup["caja_minima"], "nota": sup["nota"],
             "escenarios": {"intermedio_choque_suministro": esc}}
    rv = mi.construir_modelo(base, sup_v)
    e0 = res["escenarios"]["intermedio"]["resumen"]
    e1 = rv["escenarios"]["intermedio_choque_suministro"]["resumen"]
    delta = {k: e1[k] - e0[k] for k in ("utilidad_neta_acumulada", "fcf_acumulado", "fcf_despues_arrendamientos_acumulado",
                                         "financiamiento_requerido_total", "caja_final", "deuda_neta_final", "ingresos_final")}
    return {"naturaleza": "supuesto de escenario (mecanismo); no es pronostico ni probabilidad",
            "cadena_causal": "acontecimiento (bloqueo o restriccion de suministro de chips/energia) -> exposicion (capex de "
                             "centros de datos con GPU y componentes de Asia) -> efecto (capacidad retrasada, componentes mas "
                             "caros) -> lineas (crecimiento de ingresos, capex/ventas, margenes) -> FCF y deuda neta -> valuacion",
            "choque_aplicado": choque, "resumen_intermedio": e0, "resumen_con_choque": e1, "delta": delta,
            "periodos_con_choque": [{"periodo": p["periodo"], "ingresos": p["resultados"]["ingresos"],
                                     "fcf": p["flujo"]["fcf"], "financiamiento_requerido": p["flujo"]["disposicion_revolvente"]}
                                    for p in rv["escenarios"]["intermedio_choque_suministro"]["periodos"]],
            "controles": {k: rv["resumen_controles"][k] for k in ("total", "OK", "FALLA", "INFO", "NO_APLICA", "todos_ok")}}


def main() -> int:
    fallas_huellas = huellas.verificar(str(DATOS / "SHA256SUMS.txt"))
    if fallas_huellas:
        print("FALLAN las huellas de los insumos congelados:", fallas_huellas)
        return 1
    base = mi.cargar_json(AQUI / "base.json")
    res = mi.construir_modelo(base)
    res["doble_comprobacion_xbrl"] = doble_comprobacion(base)
    res["indicadores_notas"] = indicadores_notas(base, res)
    res["dcf_inverso"] = dcf_inverso(base, res["indicadores_notas"])
    res["sensibilidad_geopolitica"] = sensibilidad_geopolitica(base, res)
    res["huellas_insumos"] = {"manifiesto": "datos/SHA256SUMS.txt", "verificado": True}
    mi.guardar_json(res, AQUI / "resultados.json")
    mi.escribir_sha256sums([AQUI / "base.json", AQUI / "modelo.py", AQUI / "resultados.json", DATOS / "SHA256SUMS.txt"],
                           AQUI / "SHA256SUMS.txt")
    print(mi.resumen_markdown(res))
    dc = res["doble_comprobacion_xbrl"]
    print(f"Doble comprobacion XBRL: OK {dc['OK']}, explicadas {dc['DIFERENCIA_EXPLICADA']}, FALLA {dc['FALLA']}, "
          f"sin XBRL {dc['SIN_XBRL']}")
    for f in dc["filas"]:
        if f["estado"] in ("FALLA", "DIFERENCIA_EXPLICADA"):
            print("  ", f["estado"], f["periodo"], f["campo"], f["base"], f["xbrl"], f["explicacion"] or "")
    d = res["dcf_inverso"]
    print(f"DCF inverso: WACC {d['costo_de_capital']['wacc_usado']:.3f}, g {d['costo_de_capital']['g_terminal']}, "
          f"margen {d['insumos']['margen_fcf_base']:.4f} -> crecimiento implicito "
          f"{d['base']['crecimiento_implicito']:.4f} ({d['base']['estado']}); alertas: {d['base']['alertas']}")
    sg = res["sensibilidad_geopolitica"]
    print("Sensibilidad geopolitica (delta vs intermedio):", {k: round(x, 1) for k, x in sg["delta"].items()},
          "controles OK:", sg["controles"]["todos_ok"])
    ok = res["resumen_controles"]["todos_ok"] and dc["todos_ok"] and sg["controles"]["todos_ok"]
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
