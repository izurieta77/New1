"""Modelo integrado de America Movil (AMXB.MX; ADS AMX): historico FY2023-FY2025 (IFRS, MXN), 3 escenarios de
mecanismo, DCF inverso con sensibilidad y sensibilidad geopolitica/regulatoria reproducible.

FASE 0 (formacion). Los escenarios son supuestos explicitos de mecanismo (tension / intermedio / eficiencia): no son
pronosticos, ni guia del emisor, ni consenso, ni recomendacion de compra o venta. Solo biblioteca estandar.

    python3 empresas/AMXB.MX/modelo/modelo.py            # corre todo, escribe resultados.json y SHA256SUMS.txt
    python3 empresas/AMXB.MX/modelo/modelo.py --base     # regenera los periodos de base.json desde la transcripcion

Capas (cero invencion):
  datos/transcripcion_filing_miles.json   hecho (filing): renglones del 20-F en miles de MXN, con pagina.
  base.json                               mapeo de esos renglones a los campos del motor (millones) + supuestos.
  datos/*extraccion*, datos/xbrl_*        segunda lectura (visor XBRL de la SEC y companyfacts) para la doble comprobacion.
Sale con codigo 1 si: falla una huella de datos/, el mapeo de base.json no reproduce la transcripcion, la doble
comprobacion encuentra una diferencia no explicada, algun control del motor FALLA, o la auditoria de resultados.json
releido no coincide.
"""
import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DATOS = AQUI / "datos"
sys.path.insert(0, str(AQUI.parents[2]))
from herramientas import modelo_integrado as mi  # noqa: E402
from herramientas import huellas  # noqa: E402

getcontext().prec = 40
PERIODOS = ("FY2023", "FY2024", "FY2025")
FIN = {"FY2023": "2023-12-31", "FY2024": "2024-12-31", "FY2025": "2025-12-31"}


def M(x) -> float:
    """miles de MXN -> millones de MXN (exacto a 3 decimales)."""
    return float(Decimal(int(x)) / Decimal(1000))


def S(xs) -> float:
    return float(sum(Decimal(int(x)) for x in xs) / Decimal(1000))


# ------------------------------------------------------------------ mapeo transcripcion -> campos del motor

def mapear_periodo(nombre: str, P: dict) -> dict:
    """Convierte los renglones del filing (miles) en un periodo de base.json (millones).

    Decisiones de mapeo (declaradas en notas-y-modelo.md s3):
      - ppe_neto = PPE neto + activos por derecho de uso (IFRS 16); arrendamientos_financieros = pasivo por derecho de uso.
      - capex = compra de PPE + adquisicion de intangibles (misma cifra que el 'capex' del emisor).
      - CFO del motor = CFO IFRS - intereses pagados (financiamiento) - intereses de arrendamientos (Nota 15); el
        principal de arrendamientos = pagos del pasivo por derecho de uso - intereses devengados de ese pasivo.
        Asi el CFO incluye todo el costo financiero, como en la proyeccion del motor.
      - otros_* activos y pasivos: suma de renglones reportados (no se derivan como residuo).
    """
    r = P["resultados"]["lineas"]
    b = P["balance"]["lineas"]
    f = P["flujo"]["lineas"]
    c = P["capital"]["lineas"]
    pp = P["ppe"]["lineas"]
    u = P["derecho_uso"]["lineas"]
    d = P["deuda"]["lineas"]
    fr, fb, ff, fc = (P[k]["fuente"] for k in ("resultados", "balance", "flujo", "capital"))
    fppe, fu, fd = P["ppe"]["fuente"], P["derecho_uso"]["fuente"], P["deuda"]["fuente"]

    resultados = {
        "ingresos": M(r["ingresos_operativos"]),
        "costo_ventas": M(r["costo_ventas_equipos_y_servicios"]),
        "gastos_operativos": S([r["gastos_comerciales_admin_generales"], r["otros_gastos"], r["depreciacion_y_amortizacion"]]),
        "utilidad_operativa": M(r["utilidad_operativa"]),
        "gasto_intereses": M(-r["gasto_por_intereses"]),
        "ingreso_intereses": M(r["ingreso_por_intereses"]),
        "otros_ingresos": S([r["resultado_cambiario_neto"], r["valuacion_derivados_costo_laboral_otros"],
                             r["participacion_en_asociadas"]]),
        "utilidad_antes_impuestos": M(r["utilidad_antes_impuestos"]),
        "impuestos": M(r["impuesto_a_la_utilidad"]),
        "utilidad_neta": M(r["utilidad_neta"]),
        "utilidad_neta_controladora": M(r["utilidad_neta_controladora"]),
    }
    balance = {
        "caja": M(b["efectivo_y_equivalentes"]),
        "inversiones_cp": M(b["inversiones_capital_vr_ori_y_otras_cp"]),
        "cuentas_por_cobrar": M(b["cxc_suscriptores_distribuidores_impuestos_contrato_otros"]),
        "inventarios": M(b["inventarios"]),
        "otros_activos_circulantes": S([b["cxc_partes_relacionadas"], b["derivados_activo"], b["otros_activos_circulantes"]]),
        "ppe_neto": S([b["ppe_neto"], b["activos_derecho_uso"]]),
        "otros_activos_lp": S([b[k] for k in ("intangibles", "credito_mercantil", "inversiones_en_asociadas",
                                              "impuestos_diferidos_activo", "cxc_largo_plazo", "otros_activos_lp",
                                              "instrumentos_deuda_vr_ori")]),
        "activo_total": M(b["activo_total"]),
        "proveedores": M(b["proveedores_y_cuentas_por_pagar"]),
        "otros_pasivos_circulantes": S([b[k] for k in ("pasivos_acumulados", "impuesto_utilidad_por_pagar",
                                                       "otros_impuestos_por_pagar", "derivados_pasivo",
                                                       "partes_relacionadas_pasivo", "ingresos_diferidos_cp")]),
        "deuda": S([b["deuda_cp"], b["deuda_lp"]]),
        "arrendamientos_financieros": S([b["arrendamientos_cp"], b["arrendamientos_lp"]]),
        "otros_pasivos_lp": S([b[k] for k in ("impuestos_diferidos_pasivo", "cuentas_por_pagar_lp", "ingresos_diferidos_lp",
                                              "obligaciones_retiro_activos", "beneficios_a_empleados")]),
        "pasivo_total": M(b["pasivo_total"]),
        "capital_contable": M(b["capital_contable_total"]),
        "utilidades_retenidas": M(b["utilidades_retenidas_total"]),
    }
    int_arr = u["pasivo_intereses"]
    int_pag = -f["intereses_pagados"]
    pagos_arr = -f["pago_pasivo_derecho_uso"]
    ct = {"suscriptores_distribuidores_impuestos_contrato": f["ct_suscriptores_distribuidores_impuestos_contrato"],
          "pagos_anticipados": f["ct_pagos_anticipados"], "partes_relacionadas": f["ct_partes_relacionadas"],
          "inventarios": f["ct_inventarios"], "otros_activos": f["ct_otros_activos"],
          "proveedores_y_pasivos_acumulados": f["ct_proveedores_y_pasivos_acumulados"],
          "ingresos_diferidos": f["ct_ingresos_diferidos"]}
    oo = {"impuesto_a_la_utilidad_devengado (el CFO IFRS parte de la UAI)": r["impuesto_a_la_utilidad"],
          "participacion_en_asociadas": f["participacion_en_asociadas"], "resultado_venta_ppe": f["resultado_venta_ppe"],
          "costo_neto_obligaciones_laborales": f["costo_neto_obligaciones_laborales"], "cambiario_neto": f["cambiario_neto"],
          "ingreso_por_intereses": f["ingreso_por_intereses"], "gasto_por_intereses": f["gasto_por_intereses"],
          "ptu": f["ptu"], "valuacion_derivados_intereses_capitalizados_otros": f["valuacion_derivados_intereses_capitalizados_otros"],
          "ganancia_posicion_monetaria (Argentina, IAS 29)": f["ganancia_posicion_monetaria"],
          "deterioro_documentos_negocio_conjunto": f["deterioro_documentos_negocio_conjunto"],
          "deterioro_inversion_negocio_conjunto": f["deterioro_inversion_negocio_conjunto"],
          "beneficios_empleados_pagados": f["beneficios_empleados_pagados"], "ptu_pagada": f["ptu_pagada"],
          "intereses_cobrados": f["intereses_cobrados"], "impuestos_pagados": f["impuestos_pagados"],
          "RECLASIFICACION intereses pagados (desde financiamiento)": -int_pag,
          "RECLASIFICACION intereses de arrendamientos (Nota 15; desde financiamiento)": -int_arr}
    oi = {k: f[k] for k in ("dividendos_cobrados", "venta_ppe", "adquisicion_negocios", "earn_out_combinacion",
                            "instrumentos_financieros_neto", "inversiones_en_asociadas", "adquisicion_inversiones",
                            "venta_inversiones", "documentos_negocio_conjunto")}
    of = {"adquisicion_no_controladora": f["adquisicion_no_controladora"],
          "pago_contraprestacion_diferida": f["pago_contraprestacion_diferida"]}
    flujo = {
        "depreciacion_amortizacion": S([f["depreciacion_ppe_y_derecho_uso"], f["amortizacion_intangibles_y_otros"]]),
        "sbc": 0.0,
        "cfo": S([f["flujo_operacion"], -int_pag, -int_arr]),
        "capex": S([-f["compra_ppe"], -f["adquisicion_intangibles"]]),
        "cfi": M(f["flujo_inversion"]),
        "cff": S([f["flujo_financiamiento"], int_pag, int_arr]),
        "dividendos": M(-f["dividendos_pagados"]),
        "recompras": M(-f["recompra_acciones"]),
        "emision_deuda": M(f["prestamos_obtenidos"]),
        "amortizacion_deuda": M(-f["pago_prestamos"]),
        "principal_arrendamientos_financieros": S([pagos_arr, -int_arr]),
        "emision_acciones": 0.0,
        "efecto_cambiario": M(f["efecto_cambiario_efectivo"]),
        "cambio_capital_trabajo": {k: M(v) for k, v in ct.items()},
        "otros_operativos": {k: M(v) for k, v in oo.items()},
        "otros_inversion": {k: M(v) for k, v in oi.items()},
        "otros_financiamiento": {k: M(v) for k, v in of.items()},
        "caja_inicial": M(f["efectivo_inicial"]),
        "caja_final": M(f["efectivo_final"]),
        "utilidad_neta": M(r["utilidad_neta"]),
    }
    div_decl = -(c["dividendos_decretados_controladora"] + c["dividendos_decretados_no_controladora"])
    rec_total = -(c["recompra_capital_social"] + c["recompra_utilidades_retenidas"])
    otros_cap = (c["otras_adquisiciones_no_controladora_ure"] + c["otras_adquisiciones_no_controladora_nci"]
                 + c.get("perdida_transaccion_bajo_control_comun_ure", 0))
    otros_ure = {"utilidad_no_controladora (no llega a utilidades retenidas)": -r["utilidad_neta_no_controladora"],
                 "dividendos_no_controladora (no salen de utilidades retenidas)": -c["dividendos_decretados_no_controladora"],
                 "traspaso_superavit_revaluacion": c["traspaso_superavit_revaluacion_a_ure"],
                 "reciclaje_superavit_torres_peru_rd": c["reciclaje_superavit_torres_peru_rd"],
                 "adquisiciones_no_controladora_y_control_comun": c["otras_adquisiciones_no_controladora_ure"]
                 + c.get("perdida_transaccion_bajo_control_comun_ure", 0)}
    movimientos_capital = {
        "fuente": f"{fc}; utilidades retenidas = columna + reserva legal (F-5)",
        "capital_inicial": M(c["capital_total_inicial"]),
        "utilidades_retenidas_iniciales": S([c["ure_inicial_columna"], c["reserva_legal"]]),
        "dividendos_declarados": M(div_decl),
        "recompras": M(rec_total),
        "ori": M(r["ori_total"]),
        "otros": M(otros_cap),
        "recompras_contra_utilidades_retenidas": M(-c["recompra_utilidades_retenidas"]),
        "otros_utilidades_retenidas": {k: M(v) for k, v in otros_ure.items() if v},
    }
    adic = {"ppe_adiciones": pp["adiciones"], "derecho_uso_altas_y_bajas": u["activo_altas_y_bajas"],
            "derecho_uso_modificaciones": u["activo_modificaciones"]}
    otros_ppe = {f"ppe_{k}": v for k, v in pp.items() if k not in ("inicial", "adiciones", "depreciacion", "final")}
    otros_ppe.update({f"derecho_uso_{k[7:]}": v for k, v in u.items()
                      if k.startswith("activo_") and k not in ("activo_inicial", "activo_altas_y_bajas",
                                                               "activo_modificaciones", "activo_depreciacion", "activo_final")})
    movimientos_ppe = {
        "fuente": f"{fppe} + {fu}: rubro PPE + derecho de uso",
        "ppe_inicial": S([pp["inicial"], u["activo_inicial"]]),
        "adiciones": {k: M(v) for k, v in adic.items()},
        "depreciacion": S([-pp["depreciacion"], -u["activo_depreciacion"]]),
        "otros": {k: M(v) for k, v in otros_ppe.items() if v},
    }
    movimientos_deuda = {"fuente": f"{fd}; emisiones y amortizaciones de {ff}",
                         "deuda_inicial": M(d["inicial"]), "emisiones": M(f["prestamos_obtenidos"]),
                         "amortizaciones": M(-f["pago_prestamos"]), "otros": M(d["cambiario_y_otros"])}
    nuevos = {k: u[k] for k in ("pasivo_altas_y_bajas", "pasivo_combinacion", "pasivo_modificaciones") if k in u}
    movimientos_arrendamientos = {"fuente": f"{fu}; principal = pagos - intereses devengados del pasivo",
                                  "inicial": M(u["pasivo_inicial"]), "nuevos": {k: M(v) for k, v in nuevos.items()},
                                  "principal": S([pagos_arr, -int_arr]), "otros": M(u["pasivo_conversion"])}
    ebitda_emisor = P["emisor"]["lineas_millones"]["ebitda"]
    ajustado = [{"nombre": "ebitda_emisor", "base": "utilidad_operativa",
                 "ajustes": {"depreciacion_y_amortizacion (F-6)": M(r["depreciacion_y_amortizacion"])},
                 "valor_ajustado": float(ebitda_emisor),
                 "fuente": f"{P['emisor']['fuente']}; EBITDA = utilidad de operacion + D&A (definicion del glosario del emisor)"}]
    fc_campos = {
        "resultados.ingresos": f"{fr}: ingresos operativos", "resultados.costo_ventas": f"{fr}: costo de ventas de equipos y servicios (sin D&A)",
        "resultados.gastos_operativos": f"{fr}: gastos comerciales, de administracion y generales + otros gastos + D&A",
        "resultados.utilidad_operativa": f"{fr}", "resultados.gasto_intereses": f"{fr}: gasto por intereses (incluye intereses de arrendamientos, ver Nota 15)",
        "resultados.ingreso_intereses": f"{fr}", "resultados.otros_ingresos": f"{fr}: cambiario neto + valuacion de derivados, costo laboral y otros + asociadas",
        "resultados.utilidad_antes_impuestos": f"{fr}", "resultados.impuestos": f"{fr}", "resultados.utilidad_neta": f"{fr}: utilidad neta consolidada",
        "resultados.utilidad_neta_controladora": f"{fr}",
        "balance.caja": f"{fb}: efectivo y equivalentes", "balance.inversiones_cp": f"{fb}: inversiones de capital a VR con cambios en ORI y otras de corto plazo (Verizon, BT)",
        "balance.cuentas_por_cobrar": f"{fb}: suscriptores, distribuidores, impuestos por recuperar, activos de contrato y otros",
        "balance.inventarios": f"{fb}", "balance.otros_activos_circulantes": f"{fb}: partes relacionadas + derivados + otros activos circulantes",
        "balance.ppe_neto": f"{fb}: PPE neto + activos por derecho de uso", "balance.otros_activos_lp": f"{fb}: intangibles + credito mercantil + asociadas + ISR diferido + cxc LP + otros + instrumentos de deuda",
        "balance.activo_total": f"{fb}", "balance.proveedores": f"{fb}: cuentas por pagar circulantes (Nota 16a: proveedores, acreedores diversos, intereses y dividendos por pagar)",
        "balance.otros_pasivos_circulantes": f"{fb}: pasivos acumulados + ISR + otros impuestos + derivados + partes relacionadas + ingresos diferidos",
        "balance.deuda": f"{fb}: deuda de corto plazo y porcion circulante + deuda de largo plazo",
        "balance.arrendamientos_financieros": f"{fb}: pasivo por derecho de uso de corto y largo plazo",
        "balance.otros_pasivos_lp": f"{fb}: ISR diferido + cuentas por pagar LP + ingresos diferidos LP + retiro de activos + beneficios a empleados",
        "balance.pasivo_total": f"{fb}", "balance.capital_contable": f"{fb}: capital contable total (incluye no controladora)",
        "balance.utilidades_retenidas": f"{fb}: utilidades retenidas totales",
        "flujo.cfo": f"{ff}: flujo de operacion IFRS - intereses pagados - intereses de arrendamientos ({fu}); reclasificacion declarada",
        "flujo.capex": f"{ff}: compra de PPE + adquisicion de intangibles", "flujo.cfi": f"{ff}",
        "flujo.cff": f"{ff}: flujo de financiamiento IFRS + intereses pagados + intereses de arrendamientos (reclasificados a CFO)",
        "flujo.dividendos": f"{ff}: dividendos pagados", "flujo.recompras": f"{ff}: recompra de acciones",
        "flujo.emision_deuda": f"{ff}: prestamos obtenidos", "flujo.amortizacion_deuda": f"{ff}: pago de prestamos",
        "flujo.principal_arrendamientos_financieros": f"{ff} pago del pasivo por derecho de uso - intereses del pasivo ({fu})",
        "flujo.efecto_cambiario": f"{ff}", "flujo.depreciacion_amortizacion": f"{ff}: depreciacion de PPE y derecho de uso + amortizacion de intangibles",
        "flujo.sbc": "F1: no se identificaron planes de pagos basados en acciones (busqueda 'share-based' en el 20-F); 0",
    }
    memo = {
        "cfo_ifrs_reportado": M(f["flujo_operacion"]), "cff_ifrs_reportado": M(f["flujo_financiamiento"]),
        "intereses_pagados_deuda": M(int_pag), "intereses_arrendamientos_nota15": M(int_arr),
        "pagos_totales_arrendamientos": M(pagos_arr), "compra_ppe": M(-f["compra_ppe"]),
        "adquisicion_intangibles": M(-f["adquisicion_intangibles"]), "ebitda_emisor": float(ebitda_emisor),
        "ppe_sin_derecho_uso": M(b["ppe_neto"]), "activos_derecho_uso": M(b["activos_derecho_uso"]),
        "beneficios_a_empleados_pasivo": M(b["beneficios_a_empleados"]),
        "participacion_no_controladora": M(b["participacion_no_controladora"]),
        "unidades": "millones de MXN",
    }
    return {
        "periodo": nombre, "anio": int(nombre[2:]), "fin": FIN[nombre],
        "fuente": (f"{fr}; {fb}; {ff}; {fc}; {fppe}; {fu}; {fd}. Transcripcion en miles en "
                   f"datos/transcripcion_filing_miles.json; aqui en millones."),
        "fuentes_campos": fc_campos,
        "resultados": resultados, "balance": balance, "flujo": flujo,
        "movimientos_capital": movimientos_capital, "movimientos_ppe": movimientos_ppe,
        "movimientos_deuda": movimientos_deuda, "movimientos_arrendamientos": movimientos_arrendamientos,
        "ajustado": ajustado, "memo": memo,
        "notas": ("Mapeo declarado: PPE incluye derecho de uso; arrendamientos IFRS 16 como 'arrendamientos_financieros'; "
                  "intereses pagados y de arrendamientos reclasificados de financiamiento a operacion; capex incluye intangibles."),
    }


# ------------------------------------------------------------------ doble comprobacion de la transcripcion

PAGINAS = {  # (documento, paginas PDF) por bloque y periodo; ver datos/extractos_texto_paginas.json
    "FY2023": {"resultados": ("F1", [100]), "balance": ("F2", [100]), "flujo": ("F1", [102]), "capital": ("F1", [101]),
               "ppe": ("F1", [135]), "derecho_uso": ("F1", [156]), "deuda": ("F2", [178]), "emisor": ("F5", [8])},
    "FY2024": {"resultados": ("F1", [100]), "balance": ("F1", [99]), "flujo": ("F1", [102]), "capital": ("F1", [101]),
               "ppe": ("F1", [136]), "derecho_uso": ("F1", [156]), "deuda": ("F1", [169]), "emisor": ("F4", [8])},
    "FY2025": {"resultados": ("F1", [100]), "balance": ("F1", [99]), "flujo": ("F1", [102]), "capital": ("F1", [101]),
               "ppe": ("F1", [137]), "derecho_uso": ("F1", [156]), "deuda": ("F1", [169]), "emisor": ("F4", [8])},
}

R_BAL = {"efectivo_y_equivalentes": "Cash and cash equivalents",
         "inversiones_capital_vr_ori_y_otras_cp": "Equity investments at fair value through OCI and other short-term investments",
         "cxc_suscriptores_distribuidores_impuestos_contrato_otros": "Subscribers, distributors, recoverable taxes, contract assets and other, net",
         "cxc_partes_relacionadas": "Related parties (asset)", "derivados_activo": "Derivative financial instruments (asset)",
         "inventarios": "Inventories, net", "otros_activos_circulantes": "Other current assets, net",
         "total_activo_circulante": "Total current assets", "ppe_neto": "Property, plant and equipment, net",
         "intangibles": "Intangibles, net", "credito_mercantil": "Goodwill", "inversiones_en_asociadas": "Investments in associated companies",
         "impuestos_diferidos_activo": "Deferred income taxes (asset)",
         "cxc_largo_plazo": "Accounts receivable, subscribers, distributors and contract assets, net (non-current)",
         "otros_activos_lp": "Other assets, net", "instrumentos_deuda_vr_ori": "Debt instruments at fair value through OCI",
         "activos_derecho_uso": "Right-of-use assets, net", "activo_total": "Total assets",
         "deuda_cp": "Short-term debt and current portion of long-term debt",
         "arrendamientos_cp": "Short-term liability related to right-of-use of assets", "proveedores_y_cuentas_por_pagar": "Accounts payable (current)",
         "pasivos_acumulados": "Accrued liabilities", "impuesto_utilidad_por_pagar": "Income tax", "otros_impuestos_por_pagar": "Other taxes payable",
         "derivados_pasivo": "Derivative financial instruments (liability)", "partes_relacionadas_pasivo": "Related parties (liability)",
         "ingresos_diferidos_cp": "Deferred revenues (current)", "total_pasivo_circulante": "Total current liabilities",
         "deuda_lp": "Long-term debt", "arrendamientos_lp": "Long-term liability related to right-of-use of assets",
         "impuestos_diferidos_pasivo": "Deferred income taxes (liability)", "cuentas_por_pagar_lp": "Accounts payable (non-current)",
         "ingresos_diferidos_lp": "Deferred revenues (non-current)", "obligaciones_retiro_activos": "Asset retirement obligations",
         "beneficios_a_empleados": "Employee benefits", "total_pasivo_no_circulante": "Total non-current liabilities",
         "pasivo_total": "Total liabilities", "capital_social": "Capital stock", "utilidades_retenidas_anos_anteriores": "Retained earnings prior years",
         "utilidad_del_ano": "Profit for the year", "utilidades_retenidas_total": "Total retained earnings",
         "ori_acumulado": "Other comprehensive loss items", "capital_controladora": "Equity attributable to equity holders of the parent",
         "participacion_no_controladora": "Non-controlling interests", "capital_contable_total": "Total equity"}
R_RES = {"ingresos_servicios": "Service revenues", "venta_equipos": "Sales of equipment", "ingresos_operativos": "Operating revenues",
         "costo_ventas_equipos_y_servicios": "Cost of sales of equipment and services",
         "gastos_comerciales_admin_generales": "Commercial, administrative and general expenses", "otros_gastos": "Other expenses",
         "depreciacion_y_amortizacion": "Depreciation and amortization", "costos_y_gastos_operativos": "Operating costs and expenses",
         "utilidad_operativa": "Operating income", "ingreso_por_intereses": "Interest income", "gasto_por_intereses": "Interest expense",
         "resultado_cambiario_neto": "Foreign currency exchange gain (loss), net",
         "valuacion_derivados_costo_laboral_otros": "Valuation of derivatives, interest cost from labor obligations and other financial items, net",
         "participacion_en_asociadas": "Equity interest in net result of associated companies",
         "utilidad_antes_impuestos": "Profit before income tax", "impuesto_a_la_utilidad": "Income tax", "utilidad_neta": "Net profit for the year",
         "utilidad_neta_controladora": "Equity holders of the parent", "utilidad_neta_no_controladora": "Non-controlling interests",
         "ori_total": "Total other comprehensive (loss) income items, net of deferred taxes"}
R_FLU = {"utilidad_antes_impuestos": "Profit before income tax",
         "depreciacion_ppe_y_derecho_uso": "Depreciation property, plant and equipment and right-of-use assets",
         "amortizacion_intangibles_y_otros": "Amortization of intangible and other assets",
         "participacion_en_asociadas": "Equity interest in net result of associated companies",
         "resultado_venta_ppe": "(Gain) loss on sale of property, plant and equipment",
         "costo_neto_obligaciones_laborales": "Net period cost of labor obligations", "cambiario_neto": "Foreign currency exchange (income) loss, net",
         "ingreso_por_intereses": "Interest income", "gasto_por_intereses": "Interest expense", "ptu": "Employee profit sharing",
         "valuacion_derivados_intereses_capitalizados_otros": "Valuation of derivative financial instruments, capitalized interest expense and other, net",
         "ganancia_posicion_monetaria": "Gain on net monetary positions",
         "deterioro_documentos_negocio_conjunto": "Impairment to notes receivable from joint venture",
         "deterioro_inversion_negocio_conjunto": "Impairment of investment in joint venture",
         "ct_suscriptores_distribuidores_impuestos_contrato": "Subscribers, distributors, recoverable taxes, contract assets and other",
         "ct_pagos_anticipados": "Prepaid expenses", "ct_partes_relacionadas": "Related parties", "ct_inventarios": "Inventories",
         "ct_otros_activos": "Other assets", "ct_proveedores_y_pasivos_acumulados": "Accounts payable and accrued liabilities",
         "ct_ingresos_diferidos": "Deferred revenues", "beneficios_empleados_pagados": "Employee benefits paid",
         "ptu_pagada": "Employee profit sharing paid", "intereses_cobrados": "Interest received", "impuestos_pagados": "Income taxes paid",
         "flujo_operacion": "Net cash flows provided by operating activities", "compra_ppe": "Purchase of property, plant and equipment",
         "adquisicion_intangibles": "Acquisition of intangibles", "dividendos_cobrados": "Dividends received",
         "venta_ppe": "Proceeds from sale of property, plant and equipment", "adquisicion_negocios": "Acquisition of business, net of cash acquired",
         "earn_out_combinacion": "Contractual earn-out from business combination", "instrumentos_financieros_neto": "Financial instruments, net",
         "inversiones_en_asociadas": "Investments in associated companies", "adquisicion_inversiones": "Acquisition of investments",
         "venta_inversiones": "Sale of investments", "documentos_negocio_conjunto": "Acquisition of notes from joint venture",
         "flujo_inversion": "Net cash flows used in investing activities", "prestamos_obtenidos": "Loans obtained",
         "pago_prestamos": "Repayment of loans", "pago_pasivo_derecho_uso": "Payment of liability related to right-of-use of assets",
         "intereses_pagados": "Interest paid", "recompra_acciones": "Repurchase of shares", "dividendos_pagados": "Dividends paid",
         "adquisicion_no_controladora": "Acquisition of non-controlling interests",
         "pago_contraprestacion_diferida": "Payment of deferred consideration of equity interest",
         "flujo_financiamiento": "Net cash flows used in financing activities",
         "cambio_neto_efectivo": "Net (decrease) increase in cash and cash equivalents",
         "efecto_cambiario_efectivo": "Adjustment to cash flows due to exchange rate fluctuations, net",
         "efectivo_inicial": "Cash and cash equivalents at beginning of the year", "efectivo_final": "Cash and cash equivalents at end of the year"}


def _identidades(T: dict) -> list:
    """(A) Identidades aritmeticas de los propios estados transcritos (totales, cruces entre estados y continuidad)."""
    out = []

    def chk(nombre, a, b):
        out.append({"prueba": nombre, "esperado": a, "obtenido": b, "ok": a == b})
    ps = T["periodos"]
    for per, P in ps.items():
        r, b, f, c = (P[k]["lineas"] for k in ("resultados", "balance", "flujo", "capital"))
        p, u, d = P["ppe"]["lineas"], P["derecho_uso"]["lineas"], P["deuda"]["lineas"]
        chk(f"{per} ingresos = servicios + equipos", r["ingresos_servicios"] + r["venta_equipos"], r["ingresos_operativos"])
        chk(f"{per} costos y gastos = suma", r["costo_ventas_equipos_y_servicios"] + r["gastos_comerciales_admin_generales"]
            + r["otros_gastos"] + r["depreciacion_y_amortizacion"], r["costos_y_gastos_operativos"])
        chk(f"{per} UO = ingresos - costos", r["ingresos_operativos"] - r["costos_y_gastos_operativos"], r["utilidad_operativa"])
        chk(f"{per} UAI = UO + financieros + asociadas", r["utilidad_operativa"] + r["ingreso_por_intereses"] + r["gasto_por_intereses"]
            + r["resultado_cambiario_neto"] + r["valuacion_derivados_costo_laboral_otros"] + r["participacion_en_asociadas"],
            r["utilidad_antes_impuestos"])
        chk(f"{per} UN = UAI - ISR", r["utilidad_antes_impuestos"] - r["impuesto_a_la_utilidad"], r["utilidad_neta"])
        chk(f"{per} UN = controladora + no controladora", r["utilidad_neta_controladora"] + r["utilidad_neta_no_controladora"], r["utilidad_neta"])
        ac = ("efectivo_y_equivalentes", "inversiones_capital_vr_ori_y_otras_cp", "cxc_suscriptores_distribuidores_impuestos_contrato_otros",
              "cxc_partes_relacionadas", "derivados_activo", "inventarios", "otros_activos_circulantes")
        anc = ("ppe_neto", "intangibles", "credito_mercantil", "inversiones_en_asociadas", "impuestos_diferidos_activo",
               "cxc_largo_plazo", "otros_activos_lp", "instrumentos_deuda_vr_ori", "activos_derecho_uso")
        pc = ("deuda_cp", "arrendamientos_cp", "proveedores_y_cuentas_por_pagar", "pasivos_acumulados", "impuesto_utilidad_por_pagar",
              "otros_impuestos_por_pagar", "derivados_pasivo", "partes_relacionadas_pasivo", "ingresos_diferidos_cp")
        pnc = ("deuda_lp", "arrendamientos_lp", "impuestos_diferidos_pasivo", "cuentas_por_pagar_lp", "ingresos_diferidos_lp",
               "obligaciones_retiro_activos", "beneficios_a_empleados")
        chk(f"{per} activo circulante = suma", sum(b[k] for k in ac), b["total_activo_circulante"])
        chk(f"{per} activo total = circulante + no circulante", b["total_activo_circulante"] + sum(b[k] for k in anc), b["activo_total"])
        chk(f"{per} pasivo circulante = suma", sum(b[k] for k in pc), b["total_pasivo_circulante"])
        chk(f"{per} pasivo no circulante = suma", sum(b[k] for k in pnc), b["total_pasivo_no_circulante"])
        chk(f"{per} pasivo total", b["total_pasivo_circulante"] + b["total_pasivo_no_circulante"], b["pasivo_total"])
        chk(f"{per} utilidades retenidas = anteriores + del ano", b["utilidades_retenidas_anos_anteriores"] + b["utilidad_del_ano"],
            b["utilidades_retenidas_total"])
        chk(f"{per} capital controladora", b["capital_social"] + b["utilidades_retenidas_total"] + b["ori_acumulado"], b["capital_controladora"])
        chk(f"{per} capital total", b["capital_controladora"] + b["participacion_no_controladora"], b["capital_contable_total"])
        chk(f"{per} activo = pasivo + capital", b["pasivo_total"] + b["capital_contable_total"], b["activo_total"])
        chk(f"{per} utilidad del ano (balance) = controladora (resultados)", b["utilidad_del_ano"], r["utilidad_neta_controladora"])
        op = [k for k in R_FLU if R_FLU[k] and k not in ("flujo_operacion",) and list(R_FLU).index(k) < list(R_FLU).index("flujo_operacion")]
        chk(f"{per} CFO = suma de renglones", sum(f[k] for k in op), f["flujo_operacion"])
        iv = ("compra_ppe", "adquisicion_intangibles", "dividendos_cobrados", "venta_ppe", "adquisicion_negocios", "earn_out_combinacion",
              "instrumentos_financieros_neto", "inversiones_en_asociadas", "adquisicion_inversiones", "venta_inversiones",
              "documentos_negocio_conjunto")
        chk(f"{per} CFI = suma", sum(f[k] for k in iv), f["flujo_inversion"])
        fi = ("prestamos_obtenidos", "pago_prestamos", "pago_pasivo_derecho_uso", "intereses_pagados", "recompra_acciones",
              "dividendos_pagados", "adquisicion_no_controladora", "pago_contraprestacion_diferida")
        chk(f"{per} CFF = suma", sum(f[k] for k in fi), f["flujo_financiamiento"])
        chk(f"{per} cambio neto de efectivo", f["flujo_operacion"] + f["flujo_inversion"] + f["flujo_financiamiento"], f["cambio_neto_efectivo"])
        chk(f"{per} efectivo final", f["efectivo_inicial"] + f["cambio_neto_efectivo"] + f["efecto_cambiario_efectivo"], f["efectivo_final"])
        chk(f"{per} efectivo del flujo = balance", f["efectivo_final"], b["efectivo_y_equivalentes"])
        chk(f"{per} UAI flujo = resultados", f["utilidad_antes_impuestos"], r["utilidad_antes_impuestos"])
        chk(f"{per} D&A flujo = resultados", f["depreciacion_ppe_y_derecho_uso"] + f["amortizacion_intangibles_y_otros"], r["depreciacion_y_amortizacion"])
        chk(f"{per} gasto por intereses flujo = resultados", f["gasto_por_intereses"], -r["gasto_por_intereses"])
        otros_cap = (c["otras_adquisiciones_no_controladora_ure"] + c["otras_adquisiciones_no_controladora_nci"]
                     + c.get("perdida_transaccion_bajo_control_comun_ure", 0))
        chk(f"{per} variaciones del capital (ORI total de F-6)", c["capital_total_inicial"] + c["utilidad_neta_total"] + r["ori_total"]
            + c["dividendos_decretados_controladora"] + c["dividendos_decretados_no_controladora"] + c["recompra_capital_social"]
            + c["recompra_utilidades_retenidas"] + otros_cap, c["capital_total_final"])
        chk(f"{per} capital final (variaciones) = balance", c["capital_total_final"], b["capital_contable_total"])
        chk(f"{per} columna de utilidades retenidas", c["ure_inicial_columna"] + r["utilidad_neta_controladora"]
            + c["dividendos_decretados_controladora"] + c["recompra_utilidades_retenidas"] + c["traspaso_superavit_revaluacion_a_ure"]
            + c["reciclaje_superavit_torres_peru_rd"] + c["otras_adquisiciones_no_controladora_ure"]
            + c.get("perdida_transaccion_bajo_control_comun_ure", 0), c["ure_final_columna"])
        chk(f"{per} columna + reserva legal = utilidades retenidas del balance", c["ure_final_columna"] + c["reserva_legal"],
            b["utilidades_retenidas_total"])
        chk(f"{per} utilidad neta (variaciones) = resultados", c["utilidad_neta_total"], r["utilidad_neta"])
        chk(f"{per} PPE roll-forward (Nota 10)", sum(v for k, v in p.items() if k != "final"), p["final"])
        chk(f"{per} PPE Nota 10 = balance", p["final"], b["ppe_neto"])
        chk(f"{per} derecho de uso roll-forward (Nota 15)",
            sum(v for k, v in u.items() if k.startswith("activo_") and k != "activo_final"), u["activo_final"])
        chk(f"{per} derecho de uso = balance", u["activo_final"], b["activos_derecho_uso"])
        chk(f"{per} pasivo por arrendamiento roll-forward (Nota 15)",
            sum(v for k, v in u.items() if k.startswith("pasivo_") and k != "pasivo_final"), u["pasivo_final"])
        chk(f"{per} pasivo por arrendamiento = balance", u["pasivo_final"], b["arrendamientos_cp"] + b["arrendamientos_lp"])
        chk(f"{per} depreciacion Nota 10 + Nota 15 = flujo", -(p["depreciacion"] + u["activo_depreciacion"]), f["depreciacion_ppe_y_derecho_uso"])
        chk(f"{per} pagos de arrendamiento Nota 15 = flujo", u["pasivo_pagos"], f["pago_pasivo_derecho_uso"])
        chk(f"{per} deuda roll-forward (Nota 19)", d["inicial"] + d["flujo_de_efectivo"] + d["cambiario_y_otros"], d["final"])
        chk(f"{per} deuda Nota 19 = balance", d["final"], b["deuda_cp"] + b["deuda_lp"])
        chk(f"{per} flujo de deuda Nota 19 = prestamos - pagos", d["flujo_de_efectivo"], f["prestamos_obtenidos"] + f["pago_prestamos"])
        chk(f"{per} EBITDA emisor (millones, redondeo) ~ UO + D&A",
            round((r["utilidad_operativa"] + r["depreciacion_y_amortizacion"]) / 1000), P["emisor"]["lineas_millones"]["ebitda"])
    pers = list(ps)
    for a, bb in zip(pers, pers[1:]):
        A, B = ps[a], ps[bb]
        chk(f"{bb} efectivo inicial = balance {a}", B["flujo"]["lineas"]["efectivo_inicial"], A["balance"]["lineas"]["efectivo_y_equivalentes"])
        chk(f"{bb} capital inicial = balance {a}", B["capital"]["lineas"]["capital_total_inicial"], A["balance"]["lineas"]["capital_contable_total"])
        chk(f"{bb} utilidades retenidas iniciales = balance {a}",
            B["capital"]["lineas"]["ure_inicial_columna"] + B["capital"]["lineas"]["reserva_legal"], A["balance"]["lineas"]["utilidades_retenidas_total"])
        chk(f"{bb} PPE inicial = final {a}", B["ppe"]["lineas"]["inicial"], A["ppe"]["lineas"]["final"])
        chk(f"{bb} derecho de uso inicial = final {a}", B["derecho_uso"]["lineas"]["activo_inicial"], A["derecho_uso"]["lineas"]["activo_final"])
        chk(f"{bb} arrendamiento inicial = final {a}", B["derecho_uso"]["lineas"]["pasivo_inicial"], A["derecho_uso"]["lineas"]["pasivo_final"])
        chk(f"{bb} deuda inicial = final {a}", B["deuda"]["lineas"]["inicial"], A["deuda"]["lineas"]["final"])
    return out


def _valores(T: dict):
    """Itera (periodo, bloque, clave, valor) de la transcripcion, sin ceros."""
    for per, P in T["periodos"].items():
        for bloque in PAGINAS[per]:
            lineas = P[bloque].get("lineas") or P[bloque].get("lineas_millones")
            for k, v in lineas.items():
                if v:
                    yield per, bloque, k, v


def _texto_paginas(extractos: dict, doc: str, pags: list) -> tuple:
    texto = " ".join(extractos["documentos"][doc]["paginas"][str(p)] for p in pags)
    return texto, texto.replace(" ", "")


def _indice_xbrl(X: dict) -> dict:
    idx = {}
    for h in X["hechos"]:
        idx.setdefault((h["fin"], h["inicio"]), set()).add(abs(int(h["valor_mxn"])))
    return idx


def _en_xbrl(idx: dict, per: str, v) -> bool | None:
    if per not in ("FY2023", "FY2024"):
        return None                                   # companyfacts aun no trae el 20-F 2025
    anio = int(per[2:])
    cand = (idx.get((f"{anio}-12-31", None), set()) | idx.get((f"{anio}-12-31", f"{anio}-01-01"), set())
            | idx.get((f"{anio - 1}-12-31", None), set()))
    return abs(int(v)) * 1000 in cand


def _en_visor(R: dict, per: str, bloque: str, k: str, v):
    """None si el renglon no esta en el visor leido; True/False si coincide."""
    anio = per[2:]
    tabla = {"balance": ("R2_situacion_financiera", R_BAL), "resultados": ("R3_resultados", R_RES),
             "flujo": ("R5_flujos", R_FLU)}.get(bloque)
    if tabla:
        nombre, mapa = tabla
        if k in mapa and anio in R[nombre] and mapa[k] in R[nombre][anio]:
            return int(R[nombre][anio][mapa[k]]) == int(v)
        return None
    if bloque == "capital":
        cap = R["R4_capital_saldos_finales"]
        eq = {"capital_total_final": (anio, "Total equity"), "ure_final_columna": (anio, "Retained earnings (column)"),
              "capital_total_inicial": (str(int(anio) - 1), "Total equity"),
              "ure_inicial_columna": (str(int(anio) - 1), "Retained earnings (column)"), "reserva_legal": (anio, "Legal reserve")}
        if k in eq and eq[k][0] in cap:
            return int(cap[eq[k][0]][eq[k][1]]) == int(v)
    return None


def doble_comprobacion(T: dict) -> dict:
    """(A) identidades; (B) cada cifra aparece en el texto de su pagina; (C) SEC companyfacts (XBRL, 2023-2024);
    (D) visor XBRL de la SEC del 20-F 2025 (R2/R3/R4/R5). Se reporta la cobertura independiente (C o D) por cifra."""
    extractos = mi.cargar_json(DATOS / "extractos_texto_paginas.json")
    R = mi.cargar_json(DATOS / "segunda_extraccion_sec_visor_R.json")
    idx = _indice_xbrl(mi.cargar_json(DATOS / "xbrl_companyfacts_amx_20F2024_extracto.json"))
    ident = _identidades(T)
    filas = []
    for per, bloque, k, v in _valores(T):
        doc, pags = PAGINAS[per][bloque]
        texto, texto2 = _texto_paginas(extractos, doc, pags)
        s = f"{abs(int(v)):,}"
        b_ok = s in texto or s in texto2
        filas.append({"cifra": f"{per}.{bloque}.{k}", "valor": v, "pagina": f"{doc} p. PDF {pags}", "B_texto": b_ok,
                      "C_xbrl": _en_xbrl(idx, per, v), "D_visor": _en_visor(R, per, bloque, k, v)})
    n = len(filas)
    independientes = [f for f in filas if f["C_xbrl"] or f["D_visor"]]
    return {
        "naturaleza": "control de transcripcion (mismo autor; doble lectura, no auditoria independiente)",
        "A_identidades": {"total": len(ident), "ok": sum(1 for x in ident if x["ok"]), "fallas": [x for x in ident if not x["ok"]]},
        "B_texto_pagina": {"total": n, "ok": sum(1 for f in filas if f["B_texto"]),
                           "no_encontradas": [f["cifra"] for f in filas if not f["B_texto"]]},
        "C_xbrl_companyfacts": {"aplicables": sum(1 for f in filas if f["C_xbrl"] is not None),
                                "ok": sum(1 for f in filas if f["C_xbrl"]),
                                "nota": "companyfacts solo trae hechos ifrs-full no dimensionales: las columnas del estado de "
                                        "variaciones, las etiquetas propias del emisor y varios renglones de notas no aparecen"},
        "D_visor_R": {"comparadas": sum(1 for f in filas if f["D_visor"] is not None),
                      "ok": sum(1 for f in filas if f["D_visor"]),
                      "diferencias": [f["cifra"] for f in filas if f["D_visor"] is False]},
        "cobertura_independiente": {"cifras": n, "con_C_o_D": len(independientes),
                                    "solo_pdf_e_identidades": [f["cifra"] for f in filas if not (f["C_xbrl"] or f["D_visor"])]},
        "detalle": filas,
    }


# ------------------------------------------------------------------ DCF inverso

def _v(d: dict, k: str) -> float:
    return float(d[k]["valor"])


def costo_capital(d: dict, beta_u: float, crp: float, con_arrendamientos: bool, rf_local: bool = False) -> dict:
    """WACC en MXN (conocimiento/03 s2.3): k_e = r_f + beta_L x ERP madura + CRP ponderada; conversion a MXN por diferencial de
    inflacion (o, si rf_local, r_f MXN = M-bono 10a - diferencial de default de Mexico). Pesos a valor de mercado."""
    t = _v(d, "tasa_marginal")
    e = _v(d, "precio") * _v(d, "acciones")
    deuda_fin = _v(d, "deuda_financiera_jun26")
    arr = _v(d, "arrendamientos_jun26")
    beta_l = beta_u * (1 + (1 - t) * (deuda_fin + arr) / e)      # Damodaran desapalanca con deuda + arrendamientos
    rf_usd = _v(d, "tbond_10a") - _v(d, "diferencial_default_eua")
    ke_usd = rf_usd + beta_l * _v(d, "erp_madura") + crp
    pi_mx, pi_us = _v(d, "inflacion_mx"), _v(d, "inflacion_eua")
    if rf_local:
        rf_mxn = _v(d, "mbono_10a") - _v(d, "diferencial_default_mx")
        ke = rf_mxn + beta_l * _v(d, "erp_madura") + crp
    else:
        rf_mxn = (1 + rf_usd) * (1 + pi_mx) / (1 + pi_us) - 1
        ke = (1 + ke_usd) * (1 + pi_mx) / (1 + pi_us) - 1
    kd_fin = _v(d, "kd_mxn")
    if con_arrendamientos:
        deuda = deuda_fin + arr
        kd = (deuda_fin * kd_fin + arr * _v(d, "tasa_arrendamientos")) / deuda
    else:
        deuda, kd = deuda_fin, kd_fin
    w = (e * ke + deuda * kd * (1 - t)) / (e + deuda)
    return {"capitalizacion": e, "deuda_en_pesos_de_pesos": deuda, "beta_desapalancada": beta_u, "beta_reapalancada": beta_l,
            "rf_usd_ajustada": rf_usd, "rf_mxn": rf_mxn, "crp_ponderada": crp, "ke_usd": ke_usd, "ke_mxn": ke,
            "kd_antes_impuestos": kd, "kd_despues_impuestos": kd * (1 - t), "peso_capital": e / (e + deuda), "wacc": w,
            "metodo_rf": "M-bono 10a - diferencial de default de Mexico" if rf_local else "USD + diferencial de inflacion",
            "arrendamientos_como_deuda": con_arrendamientos,
            "naturaleza": "calculo con insumos citados; beta, ERP, CRP e inflacion esperada de Mexico son estimaciones, no hechos del emisor"}


def crp_ponderada(d: dict, dam: dict) -> dict:
    """CRP ponderada por ingresos externos por segmento 2025 (F1 Nota 23). Segmentos multi-pais: promedio simple de sus
    paises (el filing no da ingresos por pais dentro del segmento); Europa = Austria (supuesto; ver notas s6)."""
    paises = dam["archivos"]["ctrypremJuly26.xlsx"]["paises"]
    seg = d["ingresos_externos_segmento_2025_miles"]["valor"]
    mapa = d["paises_por_segmento"]["valor"]
    filas, tot, pond = [], 0, 0.0
    for s, ing in seg.items():
        cs = [paises[p]["crp_rating"] for p in mapa[s]]
        crp = sum(cs) / len(cs)
        filas.append({"segmento": s, "ingresos_externos_miles": ing, "paises": mapa[s], "crp_promedio": crp})
        tot += ing
        pond += ing * crp
    for fl in filas:
        fl["peso"] = fl["ingresos_externos_miles"] / tot
    return {"crp_ponderada": pond / tot, "filas": filas, "ingresos_totales_miles": tot}


def margenes_fcff(d: dict) -> dict:
    """FCFF sin apalancamiento (cálculo sobre hechos). Opcion B (base): arrendamientos como costo operativo -> se restan
    todos los pagos de arrendamiento y la deuda neta excluye arrendamientos. Opcion A: arrendamientos como deuda."""
    t = _v(d, "tasa_marginal")
    out = {}
    for anio in ("2023", "2024", "2025"):
        h = d["historico_fcff"]["valor"][anio]
        escudo_deuda = t * (h["gasto_intereses"] - h["intereses_arrendamientos"])
        fcff_b = h["cfo_ifrs"] - h["intereses_cobrados"] - h["pagos_arrendamientos"] - h["capex"] - escudo_deuda
        fcff_a = h["cfo_ifrs"] - h["intereses_cobrados"] - h["capex"] - t * h["gasto_intereses"]
        out[anio] = {"ingresos": h["ingresos"], "fcff_b": fcff_b, "margen_b": fcff_b / h["ingresos"],
                     "fcff_a": fcff_a, "margen_a": fcff_a / h["ingresos"], "escudo_fiscal_deuda": escudo_deuda}
    tt = d["ttm_jun26"]["valor"]
    h25 = d["historico_fcff"]["valor"]["2025"]
    ing_ttm = h25["ingresos"] - tt["ingresos_6m25"] + tt["ingresos_6m26"]
    cfo_ttm = h25["cfo_ifrs"] - tt["cfo_6m25"] + tt["cfo_6m26"]
    arr_ttm = h25["pagos_arrendamientos"] - tt["arrendamientos_6m25"] + tt["arrendamientos_6m26"]
    capex_ttm = h25["capex"] - tt["capex_6m25"] + tt["capex_6m26"]
    fcff_ttm = cfo_ttm - h25["intereses_cobrados"] - arr_ttm - capex_ttm - out["2025"]["escudo_fiscal_deuda"]
    out["ttm_jun26"] = {"ingresos": ing_ttm, "cfo_ifrs": cfo_ttm, "pagos_arrendamientos": arr_ttm, "capex": capex_ttm,
                        "fcff_b": fcff_ttm, "margen_b": fcff_ttm / ing_ttm,
                        "nota": "intereses cobrados y escudo fiscal de 12 meses no publicados: se usan los de 2025 (aproximacion)"}
    out["promedio_2023_2025_margen_b"] = sum(out[a]["margen_b"] for a in ("2023", "2024", "2025")) / 3
    return out


def dcf_inverso_amx(base: dict) -> dict:
    d = base["insumos_complementarios"]["dcf_inverso"]
    dam = mi.cargar_json(DATOS / "damodaran_extracto.json")
    crp = crp_ponderada(d, dam)
    beta_em = dam["archivos"]["betaemerg.xls"]["filas"]["Telecom. Services"]["beta_desapalancada_corregida_caja"]
    beta_gl = dam["archivos"]["betaGlobal.xls"]["filas"]["Telecom. Services"]["beta_desapalancada_corregida_caja"]
    w_base = costo_capital(d, beta_em, crp["crp_ponderada"], con_arrendamientos=False)
    w_arr = costo_capital(d, beta_em, crp["crp_ponderada"], con_arrendamientos=True)
    w_local = costo_capital(d, beta_em, crp["crp_ponderada"], con_arrendamientos=False, rf_local=True)
    w_global = costo_capital(d, beta_gl, crp["crp_ponderada"], con_arrendamientos=False)
    mg = margenes_fcff(d)
    ing = mg["ttm_jun26"]["ingresos"]
    precio, acciones = _v(d, "precio"), _v(d, "acciones")
    deuda_neta_fin = _v(d, "deuda_financiera_jun26") - _v(d, "caja_valores_jun26")
    nci = _v(d, "no_controladora_dic25")
    dn_base = deuda_neta_fin + nci
    arr = _v(d, "arrendamientos_jun26")
    pens = _v(d, "beneficios_empleados_netos_dic25")
    g0, anos = _v(d, "g_terminal"), int(_v(d, "anos"))
    w0 = w_base["wacc"]
    m_base = mg["2025"]["margen_b"]
    rf_mxn = w_base["rf_mxn"]

    def correr(w, g, m, dn, p=precio, ingresos=ing):
        r = mi.dcf_inverso(p, acciones, dn, w, g, m, anos, ingresos_base=ingresos, tasa_libre_riesgo=rf_mxn)
        sol = r.get("solucion") or {}
        return {"wacc": w, "g_terminal": g, "margen_fcf": m, "deuda_neta": dn, "precio": p, "estado": r["estado"],
                "crecimiento_implicito": r["crecimiento_implicito"], "peso_terminal": sol.get("peso_terminal"),
                "multiplo_terminal_fcf": sol.get("multiplo_terminal_fcf"),
                "ingresos_ano_final": (sol.get("flujos") or [{}])[-1].get("ingresos"),
                "residuo": r.get("residuo"), "alertas": r["alertas"]}

    base_run = mi.dcf_inverso(precio, acciones, dn_base, w0, g0, m_base, anos, ingresos_base=ing, tasa_libre_riesgo=rf_mxn)
    margenes = {"bajo (promedio 2023-2025)": mg["promedio_2023_2025_margen_b"], "base (2025)": m_base,
                "alto (12 meses a jun-26)": mg["ttm_jun26"]["margen_b"]}
    rejilla = []
    for etq, m in margenes.items():
        for w in (w0 - 0.01, w0, w0 + 0.01):
            for g in (g0 - 0.005, g0, g0 + 0.005):
                x = correr(w, g, m, dn_base)
                x["margen_etiqueta"] = etq
                rejilla.append(x)
    fcff_pens = mg["2025"]["fcff_b"] - _v(d, "beneficios_empleados_pagados_2025")
    variantes = {
        "precio_cierre_23sep_19.34": correr(w0, g0, m_base, dn_base, p=_v(d, "precio_alterno")),
        "sin_no_controladora_en_deuda_neta": correr(w0, g0, m_base, deuda_neta_fin),
        "arrendamientos_como_deuda (FCFF antes de arrendamientos, WACC con arrendamientos)":
            correr(w_arr["wacc"], g0, mg["2025"]["margen_a"], dn_base + arr),
        "pensiones_como_deuda (suma pagos de beneficios 2025 al FCFF y el pasivo neto a la deuda neta)":
            correr(w0, g0, fcff_pens / mg["2025"]["ingresos"], dn_base + pens),
        "rf_local_mbono (WACC con r_f MXN del M-bono)": correr(w_local["wacc"], g0, m_base, dn_base),
        "beta_global_telecom": correr(w_global["wacc"], g0, m_base, dn_base),
    }
    return {
        "naturaleza": "calculo: crecimiento anual de ingresos (10 anos) que descuenta el precio bajo supuestos explicitos; no es pronostico",
        "insumos": {"precio": precio, "fecha_precio": d["precio"]["fecha"], "acciones_millones": acciones,
                    "capitalizacion": precio * acciones, "ingresos_base_ttm_jun26": ing,
                    "deuda_financiera_jun26": _v(d, "deuda_financiera_jun26"), "caja_valores_jun26": _v(d, "caja_valores_jun26"),
                    "deuda_neta_financiera": deuda_neta_fin, "no_controladora_dic25": nci, "deuda_neta_base": dn_base,
                    "definicion_deuda_neta": "deuda financiera - efectivo y valores (jun-26, F3 p. 32) + participacion no controladora a valor en libros (dic-25)",
                    "margen_fcf_base": m_base,
                    "definicion_margen": "FCFF 2025 = CFO IFRS - intereses cobrados - pagos de arrendamiento - capex - 30% x (gasto por intereses - intereses de arrendamientos), / ingresos 2025",
                    "g_terminal": g0, "anos": anos, "rf_mxn_implicita": rf_mxn,
                    "valor_empresa_objetivo": precio * acciones + dn_base},
        "crp": crp, "wacc": w_base, "wacc_arrendamientos_como_deuda": w_arr, "wacc_rf_local": w_local, "wacc_beta_global": w_global,
        "margenes_fcff": mg,
        "base": {k: base_run[k] for k in ("estado", "crecimiento_implicito", "residuo", "valor_por_accion_en_solucion", "alertas", "supuestos")},
        "base_solucion": {k: base_run["solucion"][k] for k in ("valor_empresa", "vp_flujos", "valor_terminal", "vp_terminal",
                                                                "peso_terminal", "multiplo_terminal_fcf")},
        "base_flujos": base_run["solucion"]["flujos"],
        "sensibilidad": rejilla,
        "variantes": variantes,
    }


# ------------------------------------------------------------------ sensibilidad geopolitica / regulatoria

def sensibilidad_geopolitica(base: dict) -> dict:
    """Dos mecanismos con insumos citados y parametros hipoteticos (sin probabilidades):
    (1) Registro obligatorio de lineas moviles en Mexico (politica publica): lineas de prepago suspendidas todo un ano.
        L = prepago x s x ARPU x k x 12; perdida de EBITDA = L x c; utilidad = perdida x (1 - t).
    (2) Choque cambiario sobre deuda en USD (macro-geopolitica): perdida cambiaria = deuda USD x TC x choque x (1 - h).
    Doble comprobacion algebraica en Decimal: identidades de cada celda."""
    g = base["insumos_complementarios"]["geopolitica"]
    D = lambda x: Decimal(str(x))  # noqa: E731
    prep = D(_v(g, "prepago_mexico_miles"))
    arpu = D(_v(g, "arpu_mexico_mxn_mes"))
    serv_movil_anual = D(_v(g, "servicio_movil_mexico_2t26")) * 4
    ebitda_ttm = D(_v(g, "ebitda_2025")) - D(_v(g, "ebitda_6m25")) + D(_v(g, "ebitda_6m26"))
    un_ttm = D(_v(g, "utilidad_controladora_2025")) - D(_v(g, "utilidad_controladora_6m25")) + D(_v(g, "utilidad_controladora_6m26"))
    acc = D(_v(g, "acciones_millones"))
    t = D(_v(g, "tasa_marginal"))
    rj = g["rejilla_lineas"]["valor"]
    filas1, max_err = [], Decimal(0)
    for s in rj["s_fraccion_prepago_suspendida"]:
        for k in rj["k_arpu_relativo_suspendidas"]:
            for c in rj["c_margen_de_contribucion"]:
                s_, k_, c_ = D(s), D(k), D(c)
                lineas = prep * s_                                   # miles de lineas
                L = lineas * arpu * k_ * 12 / 1000                   # millones de MXN al ano
                de = -L * c_
                dun = de * (1 - t)
                err = abs((L - L * c_) - L * (1 - c_))
                max_err = max(max_err, err)
                filas1.append({"s": s, "k": k, "c": c, "lineas_suspendidas_miles": float(lineas),
                               "ingresos_perdidos_anuales": float(L), "pct_servicio_movil_mexico": float(L / serv_movil_anual),
                               "cambio_ebitda": float(de), "pct_ebitda_12m": float(de / ebitda_ttm),
                               "cambio_utilidad_neta": float(dun), "pct_utilidad_12m": float(dun / un_ttm),
                               "cambio_upa_mxn": float(dun / acc)})
    usd = D(_v(g, "deuda_usd_jun26_musd"))
    tc = D(_v(g, "usdmxn_jun26"))
    cob = D(_v(g, "coberturas_usd_mxn_dic25_musd"))
    h_obs = cob / usd
    rj2 = g["rejilla_cambiaria"]["valor"]
    filas2 = []
    for choque in rj2["choque_depreciacion_mxn"]:
        for h in (Decimal(0), h_obs):
            ch = D(choque)
            bruto = usd * tc * ch
            perdida = bruto * (1 - h)
            dun = -perdida * (1 - t)
            err = abs((bruto - perdida) - bruto * h)
            max_err = max(max_err, err)
            filas2.append({"choque": choque, "cobertura": float(h), "aumento_deuda_bruta_mxn": float(bruto),
                           "perdida_cambiaria_antes_impuestos": float(perdida), "cambio_utilidad_neta": float(dun),
                           "pct_utilidad_12m": float(dun / un_ttm), "cambio_upa_mxn": float(dun / acc)})
    obs = g["elasticidad_observada"]["valor"]
    elast = [{"anio": a, "resultado_cambiario": x["resultado_cambiario"], "cambio_usdmxn": x["cambio_usdmxn"],
              "millones_por_1pct": x["resultado_cambiario"] / (100 * x["cambio_usdmxn"])} for a, x in obs.items()]
    return {
        "naturaleza": "sensibilidad hipotetica: s, k, c, choque y cobertura son parametros; no hay probabilidades ni valor esperado",
        "base": {"ebitda_12m_jun26": float(ebitda_ttm), "utilidad_controladora_12m_jun26": float(un_ttm),
                 "servicio_movil_mexico_anualizado_2t26": float(serv_movil_anual), "prepago_mexico_miles": float(prep),
                 "arpu_mexico": float(arpu), "deuda_usd_musd": float(usd), "usdmxn": float(tc),
                 "coberturas_usd_mxn_musd": float(cob), "cobertura_observada": float(h_obs), "tasa_marginal": float(t)},
        "registro_lineas": filas1,
        "choque_cambiario": filas2,
        "elasticidad_cambiaria_observada": elast,
        "celdas": len(filas1) + len(filas2),
        "control_max_error_identidad": float(max_err),
        "control_ok": max_err == 0,
    }


# ------------------------------------------------------------------ calculos citados en las notas

def calculos_notas(base: dict, T: dict) -> dict:
    """Cifras 'calculo propio' de notas-y-modelo.md, reproducibles desde base.json y la transcripcion."""
    q = base["insumos_complementarios"]["notas"]
    p25 = T["periodos"]["FY2025"]
    u = p25["derecho_uso"]["lineas"]
    b = p25["balance"]["lineas"]
    rp = q["arrendamientos_partes_relacionadas"]["valor"]
    deuda_moneda = q["deuda_por_moneda_dic25_miles"]["valor"]
    tot_deuda = sum(deuda_moneda.values())
    venc = q["vencimientos_deuda_lp_dic25_miles"]["valor"]
    out = {
        "arrendamientos_pasivo_partes_relacionadas_pct": rp["pasivo_2025"] / u["pasivo_final"],
        "arrendamientos_activo_partes_relacionadas_pct": rp["activo_2025"] / u["activo_final"],
        "costo_arrendamientos_partes_relacionadas_pct_ingresos": rp["costo_total_2025"] / p25["resultados"]["lineas"]["ingresos_operativos"],
        "interes_implicito_arrendamientos_2025": u["pasivo_intereses"] / ((u["pasivo_inicial"] + u["pasivo_final"]) / 2),
        "deuda_por_moneda_pct": {k: v / tot_deuda for k, v in deuda_moneda.items()},
        "deuda_total_nota14": tot_deuda,
        "deuda_no_mxn_pct": 1 - deuda_moneda["MXN"] / tot_deuda,
        "vencimientos_lp_pct": {k: v / sum(venc.values()) for k, v in venc.items()},
        "deuda_cp_pct_total": b["deuda_cp"] / (b["deuda_cp"] + b["deuda_lp"]),
        "gasto_intereses_sin_arrendamientos_2025": -p25["resultados"]["lineas"]["gasto_por_intereses"] - u["pasivo_intereses"],
        "tasa_implicita_deuda_2025": (-p25["resultados"]["lineas"]["gasto_por_intereses"] - u["pasivo_intereses"])
        / ((T["periodos"]["FY2024"]["deuda"]["lineas"]["final"] + p25["deuda"]["lineas"]["final"]) / 2),
        "pension_mexico_neta_dic25_miles": q["pension_mexico_dic25_miles"]["valor"]["neto"],
        "pension_mexico_cobertura_activos": -q["pension_mexico_dic25_miles"]["valor"]["activos"] / q["pension_mexico_dic25_miles"]["valor"]["dbo"],
        "brasil_contingencias_fiscales_provision_pct": q["brasil_contingencias_miles"]["valor"]["provision"] / q["brasil_contingencias_miles"]["valor"]["total"],
        "reexpresion_isr_2024_millones": q["reexpresion_2024"]["valor"]["isr_20f"] - q["reexpresion_2024"]["valor"]["isr_4t24"],
        "reexpresion_un_2024_millones": q["reexpresion_2024"]["valor"]["un_20f"] - q["reexpresion_2024"]["valor"]["un_4t24"],
    }
    fcf = q["fcf_emisor_2025"]["valor"]
    h = base["historico"][-1]
    fcf_desp_arr = h["flujo"]["cfo"] - h["flujo"]["capex"] - h["flujo"]["principal_arrendamientos_financieros"]
    out["fcf_emisor_2025_reconciliacion"] = {
        "fcf_despues_arrendamientos_motor": fcf_desp_arr, "mas_beneficios_empleados_emisor": fcf["beneficios_empleados"],
        "mas_inversion_y_otros_emisor": fcf["inversion_y_otros"],
        "fcf_reconstruido": fcf_desp_arr + fcf["beneficios_empleados"] + fcf["inversion_y_otros"], "fcf_emisor": fcf["fcf"],
        "diferencia": fcf_desp_arr + fcf["beneficios_empleados"] + fcf["inversion_y_otros"] - fcf["fcf"]}
    return out


# ------------------------------------------------------------------ corrida

def periodos_desde_transcripcion() -> list:
    T = mi.cargar_json(DATOS / "transcripcion_filing_miles.json")
    return [mapear_periodo(p, T["periodos"][p]) for p in PERIODOS]


def main(argv) -> int:
    if "--base" in argv:
        ruta = AQUI / "base.json"
        base = mi.cargar_json(ruta)
        base["historico"] = periodos_desde_transcripcion()
        mi.guardar_json(base, ruta)
        print(f"base.json: {len(base['historico'])} periodos regenerados desde la transcripcion")
        return 0
    fallas_huellas = huellas.verificar(str(DATOS / "SHA256SUMS.txt"))
    base = mi.cargar_json(AQUI / "base.json")
    T = mi.cargar_json(DATOS / "transcripcion_filing_miles.json")
    mapeo_ok = json.dumps(base["historico"], sort_keys=True) == json.dumps(periodos_desde_transcripcion(), sort_keys=True)
    dc = doble_comprobacion(T)
    res = mi.construir_modelo(base)
    res["dcf_inverso"] = dcf_inverso_amx(base)
    res["sensibilidad_geopolitica"] = sensibilidad_geopolitica(base)
    res["doble_comprobacion"] = dc
    res["calculos_notas"] = calculos_notas(base, T)
    res["control_mapeo_base"] = {"ok": mapeo_ok, "detalle": "base.json.historico == mapear_periodo(transcripcion)"}
    res["huellas_datos"] = {"ok": not fallas_huellas, "fallas": fallas_huellas}
    mi.guardar_json(res, AQUI / "resultados.json")
    releido = mi.cargar_json(AQUI / "resultados.json")
    auditoria = mi.resumir_controles(mi.verificar(releido))
    coincide = all(auditoria[k] == res["resumen_controles"][k] for k in ("total", "OK", "FALLA", "INFO", "NO_APLICA"))
    mi.escribir_sha256sums([AQUI / "base.json", AQUI / "modelo.py", AQUI / "resultados.json"], AQUI / "SHA256SUMS.txt")
    print(mi.resumen_markdown(res))
    dcf = res["dcf_inverso"]
    print(f"DCF inverso base: WACC {dcf['wacc']['wacc']:.4%}, g {dcf['insumos']['g_terminal']:.2%}, margen FCFF "
          f"{dcf['insumos']['margen_fcf_base']:.4%} -> crecimiento implicito {dcf['base']['crecimiento_implicito']:.4%} "
          f"({dcf['base']['estado']})")
    geo = res["sensibilidad_geopolitica"]
    print(f"Sensibilidad geopolitica: {geo['celdas']} celdas, identidad max error {geo['control_max_error_identidad']}")
    dok = (not dc["A_identidades"]["fallas"] and not dc["B_texto_pagina"]["no_encontradas"]
           and not dc["D_visor_R"]["diferencias"])
    ci = dc["cobertura_independiente"]
    print(f"Doble comprobacion: A {dc['A_identidades']['ok']}/{dc['A_identidades']['total']}, "
          f"B {dc['B_texto_pagina']['ok']}/{dc['B_texto_pagina']['total']}, "
          f"C {dc['C_xbrl_companyfacts']['ok']}/{dc['C_xbrl_companyfacts']['aplicables']}, "
          f"D {dc['D_visor_R']['ok']}/{dc['D_visor_R']['comparadas']}; cifras con fuente independiente (C o D) "
          f"{ci['con_C_o_D']}/{ci['cifras']}")
    print(f"Mapeo base.json = transcripcion: {mapeo_ok}; huellas de datos/: {'OK' if not fallas_huellas else fallas_huellas}")
    print(f"Auditoria de resultados.json releido: {'coincide' if coincide else 'NO COINCIDE'} "
          f"({auditoria['total']} registros, FALLA {auditoria['FALLA']})")
    ok = res["resumen_controles"]["todos_ok"] and coincide and geo["control_ok"] and mapeo_ok and not fallas_huellas and dok
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
