"""Modelo integrado de TSMC (TSM): historico FY2023-FY2025 (IFRS, 20-F), 3 escenarios de mecanismo,
DCF inverso en USD y sensibilidad geopolitica reproducible (rejilla completa).

FASE 0 (formacion). Los escenarios (tension / intermedio / eficiencia) son supuestos explicitos de mecanismo:
no son pronosticos, ni guia del emisor, ni consenso, ni recomendacion de compra o venta.
Solo biblioteca estandar de Python 3.11. Uso (desde cualquier directorio):

    python3 empresas/TSM/modelo/modelo.py

Escribe resultados.json y SHA256SUMS.txt junto a este archivo e imprime el resumen en markdown.
Sale con codigo 1 si falla algun control del motor, algun control propio de este archivo (T01 composicion,
T02 aritmetica de la transcripcion, P01 puente de margen, D01 precio congelado, G01 identidad de la rejilla)
o si la auditoria de resultados.json releido no coincide con la corrida.
"""
import copy
import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[2]))
from herramientas import modelo_integrado as mi  # noqa: E402

getcontext().prec = 40
ANIOS = ("FY2023", "FY2024", "FY2025")


def _v(bloque: dict, clave: str) -> float:
    return float(bloque[clave]["valor"])


def _reg(cid, prueba, periodo, esperado, obtenido, tol, detalle=""):
    dif = None if esperado is None or obtenido is None else obtenido - esperado
    estado = "OK" if dif is not None and abs(dif) <= tol else "FALLA"
    return {"id": cid, "prueba": prueba, "periodo": periodo, "esperado": esperado, "obtenido": obtenido,
            "diferencia": dif, "tolerancia": tol, "estado": estado, "detalle": detalle}


# ------------------------------------------------------------------ T01 / T02: transcripcion

def _tabla(base: dict) -> dict:
    t = base["transcripcion"]
    tab = {}
    for sec in ("balance", "notas", "resultados", "flujo", "capital", "ppe_nota15"):
        for k, info in t[sec].items():
            tab[k] = info["valores"]
    return tab


def controles_transcripcion(base: dict) -> list:
    """T01: cada campo del motor = suma con signo de los renglones transcritos (composicion declarada en base.json).
    T02: la aritmetica propia de los estados transcritos (subtotales, totales, caja, capital) cuadra.
    Tolerancia = 0.05 x (numero de terminos + 1): redondeo de cifras publicadas a un decimal."""
    tab = _tabla(base)
    out = []
    per = {p["periodo"]: p for p in base["historico"]}
    for e in base["composicion"]:
        sec, campo = e["campo"].split(".", 1)
        for a in e["anios"]:
            vals = [s * tab[k][a] for k, s in e["lineas"]]
            valor = per[a][sec][campo]
            tol = 0.05 * (len(vals) + 1)
            if isinstance(valor, dict):
                obtenido = sum(valor.values())
                ok_items = sorted(round(x, 1) for x in valor.values()) == sorted(round(x, 1) for x in vals)
                out.append(_reg("T01", f"{e['campo']} (detalle) = suma de renglones", a, sum(vals), obtenido, tol,
                                "renglones identicos" if ok_items else "ALERTA: el detalle no coincide renglon por renglon"))
                if not ok_items:
                    out[-1]["estado"] = "FALLA"
            else:
                out.append(_reg("T01", f"{e['campo']} = suma de renglones", a, sum(vals), valor, tol))

    def s(*claves, a):
        return sum(tab[k][a] for k in claves)

    for a in ANIOS:
        chk = [
            ("activo circulante = suma de renglones", s("a_caja", "a_fvtpl_c", "a_fvoci_c", "a_ac_c", "a_cobertura_c", "a_cxc",
                                                          "a_cxc_rel", "a_otras_cxc_rel", "a_inventarios", "a_otros_fin_c",
                                                          "a_otros_c", a=a), tab["a_total_c"][a], 11),
            ("activo no circulante = suma de renglones", s("a_fvtpl_nc", "a_fvoci_nc", "a_ac_nc", "a_asociadas", "a_ppe", "a_rou",
                                                             "a_intangibles", "a_isr_dif", "a_depositos", "a_otros_nc", a=a),
             tab["a_total_nc"][a], 10),
            ("activo total = circulante + no circulante", s("a_total_c", "a_total_nc", a=a), tab["a_total"][a], 2),
            ("pasivo circulante = suma de renglones", s("p_fvtpl_c", "p_cobertura_c", "p_proveedores", "p_proveedores_rel",
                                                          "p_sueldos", "p_bono_utilidades", "p_contratistas_equipo",
                                                          "p_dividendos_por_pagar", "p_isr_por_pagar", "p_porcion_circ_lp",
                                                          "p_acumulados_otros_c", a=a), tab["p_total_c"][a], 11),
            ("pasivo no circulante = suma de renglones", s("p_bonos", "p_prestamos_lp", "p_isr_dif", "p_arrend_nc",
                                                             "p_beneficios_def", "p_depositos_garantia", "p_otros_nc", a=a),
             tab["p_total_nc"][a], 7),
            ("pasivo total = circulante + no circulante", s("p_total_c", "p_total_nc", a=a), tab["p_total"][a], 2),
            ("utilidades retenidas = reserva legal + especial + no asignadas",
             s("k_reserva_legal", "k_reserva_especial", "k_no_asignadas", a=a), tab["k_utilidades_retenidas"][a], 3),
            ("capital de la controladora = capital social + prima + utilidades retenidas + otros",
             s("k_capital_social", "k_prima", "k_utilidades_retenidas", "k_otros", a=a), tab["k_controladora"][a], 4),
            ("capital total = controladora + no controladora", s("k_controladora", "k_no_controladora", a=a), tab["k_total"][a], 2),
            ("activo total = pasivo total + capital total", s("p_total", "k_total", a=a), tab["a_total"][a], 2),
            ("deuda de notas (bonos + prestamos) = bonos LP + prestamos LP + porcion circulante",
             s("p_bonos", "p_prestamos_lp", "p_porcion_circ_lp", a=a), s("n_bonos_total", "n_prestamos_total", a=a), 3),
            ("arrendamientos = porcion circulante + no circulante", s("n_arrend_circ", "p_arrend_nc", a=a), tab["n_arrend_total"][a], 2),
            ("utilidad bruta = ingresos - costo de ventas", tab["r_ingresos"][a] - tab["r_costo_ventas"][a], tab["r_utilidad_bruta"][a], 2),
            ("gastos de operacion = I+D + G&A + mercadotecnia", s("r_gid", "r_gya", "r_mkt", a=a), tab["r_gastos_op_total"][a], 3),
            ("utilidad de operacion = bruta - gastos + otros operativos",
             tab["r_utilidad_bruta"][a] - tab["r_gastos_op_total"][a] + tab["r_otros_ing_op"][a], tab["r_utilidad_operativa"][a], 3),
            ("no operativo = suma de renglones", s("r_asociadas", "r_ingreso_intereses", "r_otros_ingresos", "r_cambiario",
                                                   "r_costos_financieros", "r_otras_ganancias", a=a), tab["r_no_operativo_total"][a], 6),
            ("UAI = operacion + no operativo", s("r_utilidad_operativa", "r_no_operativo_total", a=a), tab["r_uai"][a], 2),
            ("utilidad neta = UAI - impuestos", tab["r_uai"][a] - tab["r_impuestos"][a], tab["r_utilidad_neta"][a], 2),
            ("utilidad neta = controladora + no controladora", s("r_un_controladora", "r_un_no_controladora", a=a),
             tab["r_utilidad_neta"][a], 2),
            ("UAI del flujo = UAI del estado de resultados", tab["r_uai"][a], tab["f_uai"][a], 1),
            ("efectivo generado por la operacion = UAI + ajustes + cambios",
             sum(tab[k][a] for k in tab if k.startswith("f_") and k not in ("f_generado_operacion", "f_impuestos_pagados", "f_cfo")),
             tab["f_generado_operacion"][a], 34),
            ("CFO = generado por la operacion + impuestos pagados", s("f_generado_operacion", "f_impuestos_pagados", a=a), tab["f_cfo"][a], 2),
            ("CFI = suma de renglones de inversion", sum(tab[k][a] for k in tab if k.startswith("i_") and k != "i_cfi"), tab["i_cfi"][a], 22),
            ("CFF = suma de renglones de financiamiento", sum(tab[k][a] for k in tab if k.startswith("x_") and k != "x_cff"), tab["x_cff"][a], 16),
            ("aumento de caja = CFO + CFI + CFF + efecto cambiario", s("f_cfo", "i_cfi", "x_cff", "z_fx", a=a), tab["z_aumento"][a], 4),
            ("caja final = inicial + aumento", s("z_caja_inicial", "z_aumento", a=a), tab["z_caja_final"][a], 2),
            ("caja final del flujo = caja del balance", tab["a_caja"][a], tab["z_caja_final"][a], 1),
            ("capital final del estado de variaciones = balance", tab["k_total"][a], tab["e_capital_final"][a], 1),
            ("utilidades retenidas finales del estado de variaciones = balance", tab["k_utilidades_retenidas"][a], tab["e_ure_final"][a], 1),
        ]
        if a != "FY2023":
            prev = ANIOS[ANIOS.index(a) - 1]
            chk += [("caja inicial = caja final del ano previo", tab["z_caja_final"][prev], tab["z_caja_inicial"][a], 1),
                    ("capital inicial del estado de variaciones = capital final previo", tab["k_total"][prev], tab["e_capital_inicial"][a], 1),
                    ("utilidades retenidas iniciales = finales previas", tab["k_utilidades_retenidas"][prev], tab["e_ure_inicial"][a], 1),
                    ("prestamos bancarios (Nota 19) = NT$ + JPY - descuento", s("n_prestamos_ntd", "n_prestamos_jpy", "n_prestamos_descuento", a=a),
                     tab["n_prestamos_total"][a], 4),
                    ("prestamos LP del balance = total Nota 19 - porcion circulante",
                     tab["n_prestamos_total"][a] - tab["n_prestamos_circ"][a], tab["p_prestamos_lp"][a], 3)]
        for prueba, esp, obt, n in chk:
            out.append(_reg("T02", prueba, a, esp, obt, 0.05 * (n + 1)))
    return out


# ------------------------------------------------------------------ P01: puente del margen bruto

def controles_puente(base: dict) -> tuple[list, dict]:
    ic = base["insumos_complementarios"]["puente_margen_bruto"]
    maximo = ic["ultramar_incremental_maximo"]
    out, tabla = [], {}
    for n, esc in base["supuestos"]["escenarios"].items():
        p = ic["escenarios"][n]
        filas = []
        for t in range(base["supuestos"]["anos"]):
            mb = (p["ancla_margen_bruto"] - p["n2_y_nodos_nuevos"][t] - p["ultramar_incremental"][t]
                  - p["tipo_de_cambio"][t] + p["utilizacion_precio_costo"][t])
            per = f"{n} ano {t + 1}"
            out.append(_reg("P01", "margen_bruto del supuesto = puente declarado", per, mb, esc["margen_bruto"][t], 1e-9))
            out.append(_reg("P01", "margen_operativo = margen_bruto - gastos operativos / ventas", per,
                            esc["margen_bruto"][t] - p["gastos_operativos_ventas"][t], esc["margen_operativo"][t], 1e-9))
            u = p["ultramar_incremental"][t]
            dentro = 0.0 <= u <= maximo + 1e-12
            out.append({"id": "P01", "prueba": "0 <= presion incremental del extranjero <= 2 pp (sin doble conteo)",
                        "periodo": per, "esperado": [0.0, maximo], "obtenido": u, "diferencia": None, "tolerancia": 0.0,
                        "estado": "OK" if dentro else "FALLA",
                        "detalle": "el ancla ya incluye 2-3 pp de dilucion temprana; solo se resta el paso a 3-4 pp"})
            filas.append({"ano": t + 1, "ancla": p["ancla_margen_bruto"], "n2_y_nodos_nuevos": p["n2_y_nodos_nuevos"][t],
                          "ultramar_incremental": u, "tipo_de_cambio": p["tipo_de_cambio"][t],
                          "utilizacion_precio_costo": p["utilizacion_precio_costo"][t], "margen_bruto": esc["margen_bruto"][t],
                          "doble_conteo_si_se_resta_dilucion_total_pp": [2.0 + 100 * u, 3.0 + 100 * u],
                          "margen_bruto_con_doble_conteo": [esc["margen_bruto"][t] - 0.02, esc["margen_bruto"][t] - 0.03]})
        tabla[n] = filas
    return out, tabla


# ------------------------------------------------------------------ 12 meses (TTM) y DCF inverso

def ttm(base: dict) -> dict:
    t = base["insumos_complementarios"]["ttm"]
    val = {k: t[k]["fy2025"] - t[k]["1s25"] + t[k]["1s26"] for k in
           ("ingresos", "utilidad_bruta", "utilidad_operativa", "cfo", "capex_ppe", "capex_intangibles", "da", "sbc")}
    val["fcf_emisor"] = val["cfo"] - val["capex_ppe"]
    val["fcf"] = val["cfo"] - val["capex_ppe"] - val["capex_intangibles"]
    val["margen_bruto"] = val["utilidad_bruta"] / val["ingresos"]
    val["margen_operativo"] = val["utilidad_operativa"] / val["ingresos"]
    val["margen_cfo"] = val["cfo"] / val["ingresos"]
    val["capex_ventas"] = (val["capex_ppe"] + val["capex_intangibles"]) / val["ingresos"]
    q = t["fcf_emisor_trimestral_miles_de_millones"]
    val["fcf_emisor_suma_trimestres"] = 1000.0 * (q["3T25"] + q["4T25"] + q["1T26"] + q["2T26"])
    val["control_fcf_emisor_vs_trimestres"] = val["fcf_emisor"] - val["fcf_emisor_suma_trimestres"]
    a = base["insumos_complementarios"]["anclas_escenarios"]["ingresos_usd_miles_de_millones"]
    val["ingresos_usd_millones"] = 1000.0 * (a["3T25"] + a["4T25"] + a["1T26"] + a["2T26"])
    val["tipo_cambio_implicito"] = val["ingresos"] / val["ingresos_usd_millones"]
    val["naturaleza"] = "calculo sobre hechos: 2025 (IFRS) - 1S25 + 1S26 (TIFRS); millones de NT$ salvo ingresos_usd_millones"
    return val


def wacc_bottom_up(d: dict, e_usd: float, deuda_usd: float, lam: float) -> dict:
    t = _v(d, "tasa_impuesto_marginal")
    bu = _v(d, "beta_desapalancada_sector")
    bl = bu * (1 + (1 - t) * deuda_usd / e_usd)
    ke = _v(d, "tasa_libre_riesgo") + bl * _v(d, "erp") + lam * _v(d, "prima_riesgo_pais_taiwan")
    kd = (_v(d, "tasa_libre_riesgo") + _v(d, "diferencial_deuda")) * (1 - t)
    w = (e_usd * ke + deuda_usd * kd) / (e_usd + deuda_usd)
    return {"capitalizacion_usd_m": e_usd, "deuda_y_arrendamientos_usd_m": deuda_usd, "d_e": deuda_usd / e_usd,
            "beta_desapalancada": bu, "beta_reapalancada": bl, "lambda": lam,
            "prima_riesgo_pais": _v(d, "prima_riesgo_pais_taiwan"), "costo_capital_acciones": ke,
            "costo_deuda_despues_impuestos": kd, "wacc": w,
            "naturaleza": "calculo con insumos citados; beta, ERP, CRP y lambda son estimaciones o supuestos, no hechos del emisor"}


def dcf_inverso_tsm(base: dict, t12: dict) -> dict:
    d = base["insumos_complementarios"]["dcf_inverso"]
    b = d["balance_30jun2026"]
    fx = _v(d, "tipo_cambio")
    ads = _v(d, "acciones_comunes") / _v(d, "acciones_por_ads")
    precio = _v(d, "precio_adr")
    precio_local_ads = _v(d, "precio_local") * _v(d, "acciones_por_ads") / fx
    deuda = b["bonos_no_circulantes"] + b["prestamos_bancarios_no_circulantes"] + b["porcion_circulante_lp"] + b["arrendamientos"]
    efectivo = b["caja"] + b["fvtpl_circulante"] + b["fvoci_circulante"] + b["costo_amortizado_circulante"]
    dn_base = deuda + b["dividendos_por_pagar"] - efectivo
    variantes_dn = {
        "base (deuda + arrendamientos + dividendos por pagar - caja - valores circulantes)": dn_base,
        "sin dividendos por pagar": dn_base - b["dividendos_por_pagar"],
        "ampliada (resta ademas activos financieros no circulantes)": dn_base - (b["fvtpl_no_circulante"] + b["fvoci_no_circulante"]
                                                                                 + b["costo_amortizado_no_circulante"]),
        "anticipos de clientes como deuda": dn_base + b["anticipos_de_clientes"],
    }
    margen_base = (t12["fcf"] - t12["sbc"]) / t12["ingresos"]
    ing_usd = t12["ingresos_usd_millones"]
    e_usd = precio * ads
    w_act = wacc_bottom_up(d, e_usd, deuda / fx, _v(d, "lambda_activos"))
    w_ing = wacc_bottom_up(d, e_usd, deuda / fx, _v(d, "lambda_ingresos"))
    w0, g0, anos, rf = w_act["wacc"], _v(d, "g_terminal"), int(_v(d, "anos")), _v(d, "tasa_libre_riesgo")

    def correr(w, g, m, dn_twd, p=precio):
        r = mi.dcf_inverso(p, ads, dn_twd / fx, w, g, m, anos, ingresos_base=ing_usd, tasa_libre_riesgo=rf)
        sol = r.get("solucion") or {}
        fl = sol.get("flujos") or [{}]
        return {"wacc": w, "g_terminal": g, "margen_fcf": m, "deuda_neta_usd_m": dn_twd / fx, "precio_usd_ads": p,
                "estado": r["estado"], "crecimiento_implicito": r["crecimiento_implicito"],
                "peso_terminal": sol.get("peso_terminal"), "multiplo_terminal_fcf": sol.get("multiplo_terminal_fcf"),
                "ingresos_ano_final_usd_m": fl[-1].get("ingresos"), "residuo": r.get("residuo"), "alertas": r["alertas"]}

    base_run = mi.dcf_inverso(precio, ads, dn_base / fx, w0, g0, margen_base, anos, ingresos_base=ing_usd,
                              tasa_libre_riesgo=rf)
    m_bajo, m_alto = d["margenes_fcf_sensibilidad"]["valor"]
    rejilla = [correr(w, g, m, dn_base) for m in (m_bajo, margen_base, m_alto)
               for w in (w0 - 0.01, w0, w0 + 0.01) for g in (g0 - 0.005, g0, g0 + 0.005)]
    variantes = {f"deuda neta: {k}": correr(w0, g0, margen_base, v_) for k, v_ in variantes_dn.items() if not k.startswith("base")}
    variantes["lambda por ingresos (sede Taiwan 1S26)"] = correr(w_ing["wacc"], g0, margen_base, dn_base)
    variantes["precio local 2330.TW convertido a ADS (sin prima del ADR)"] = correr(w0, g0, margen_base, dn_base, precio_local_ads)
    g_impl = base_run["crecimiento_implicito"]
    ingresos_4_5 = ing_usd * (1 + g_impl) ** 4.5 if g_impl is not None else None
    return {
        "naturaleza": "calculo: crecimiento de ingresos que descuenta el precio bajo supuestos explicitos; no es pronostico",
        "moneda": "USD (ingresos sustancialmente en USD, F1 p. 11); balance en NT$ convertido al tipo de cambio del dia del precio",
        "insumos": {"precio_adr": precio, "fecha_precio": "2026-09-24", "tipo_cambio": fx, "ads_equivalentes_m": ads,
                    "capitalizacion_usd_m": e_usd, "precio_local_en_usd_por_ads": precio_local_ads,
                    "prima_adr_sobre_local": precio / precio_local_ads - 1,
                    "ingresos_12m_usd_m": ing_usd, "ingresos_12m_twd_m": t12["ingresos"],
                    "fcf_12m_twd_m": t12["fcf"], "sbc_12m_twd_m": t12["sbc"], "margen_fcf_base": margen_base,
                    "definicion_margen": "(CFO - capex de PPE - intangibles - SBC) de 12 meses / ingresos de 12 meses (misma razon en NT$ y USD)",
                    "deuda_y_arrendamientos_twd_m": deuda, "efectivo_y_valores_circulantes_twd_m": efectivo,
                    "dividendos_por_pagar_twd_m": b["dividendos_por_pagar"],
                    "deuda_neta_twd_m": dn_base, "deuda_neta_usd_m": dn_base / fx,
                    "definicion_deuda_neta": list(variantes_dn)[0], "g_terminal": g0, "anos": anos, "tasa_libre_riesgo": rf},
        "wacc": w_act, "wacc_lambda_ingresos": w_ing,
        "base": {k: base_run[k] for k in ("estado", "crecimiento_implicito", "residuo", "valor_por_accion_en_solucion",
                                          "alertas", "supuestos")},
        "base_solucion": {k: base_run["solucion"][k] for k in ("valor_empresa", "vp_flujos", "valor_terminal", "vp_terminal",
                                                                "peso_terminal", "multiplo_terminal_fcf")},
        "base_flujos": base_run["solucion"]["flujos"],
        "ingresos_implicitos_a_4_5_anos_usd_m": ingresos_4_5,
        "sensibilidad": rejilla,
        "rango_sensibilidad": [min(r["crecimiento_implicito"] for r in rejilla), max(r["crecimiento_implicito"] for r in rejilla)],
        "variantes": variantes,
    }


# ------------------------------------------------------------------ sensibilidad geopolitica

def sensibilidad_geopolitica(base: dict, t12: dict) -> dict:
    """Rejilla completa e x r x c x d (81 celdas), Decimal exacto.

    L = R e (1 - r)                      ingresos perdidos (restriccion no sustituida en el periodo)
    GP' = R m - L c - R' d               c = fraccion del ingreso perdido que no se ahorra en costo
                                         d = presion INCREMENTAL de margen del extranjero (0-2 pp): el margen m
                                             consolidado ya incluye la dilucion temprana de 2-3 pp
    Gastos de operacion fijos: cambio en utilidad de operacion = -(L c + R' d).
    Doble comprobacion algebraica: COGS' = R(1 - m) - L(1 - c) + R' d  y  GP' = R' - COGS'."""
    g = base["insumos_complementarios"]["geopolitica"]
    dci = base["insumos_complementarios"]["dcf_inverso"]
    D = lambda x: Decimal(str(x))  # noqa: E731
    R, GP, OI = D(round(t12["ingresos"], 1)), D(round(t12["utilidad_bruta"], 1)), D(round(t12["utilidad_operativa"], 1))
    m = GP / R
    t = D(_v(g, "tasa_impuestos"))
    acc = D(_v(dci, "acciones_comunes"))
    fx = D(_v(dci, "tipo_cambio"))
    ads = D(_v(dci, "acciones_por_ads"))
    rj = g["rejilla"]
    filas, max_err = [], Decimal(0)
    for e in rj["fraccion_restringida"]:
        for r in rj["sustitucion"]:
            for c in rj["margen_contribucion_perdido"]:
                for dd in rj["presion_incremental_ultramar"]:
                    e_, r_, c_, d_ = D(e), D(r), D(c), D(dd)
                    L = R * e_ * (1 - r_)
                    R2 = R - L
                    GP2 = R * m - L * c_ - R2 * d_
                    COGS2 = R * (1 - m) - L * (1 - c_) + R2 * d_
                    err = abs((R2 - COGS2) - GP2)
                    max_err = max(max_err, err)
                    d_oi = -(L * c_ + R2 * d_)
                    d_un = d_oi * (1 - t)
                    filas.append({"fraccion_restringida": e, "sustitucion": r, "margen_contribucion_perdido": c,
                                  "presion_incremental_ultramar": dd, "ingresos_perdidos": float(L),
                                  "perdida_bruta_por_ventas": float(L * c_), "perdida_bruta_por_ultramar": float(R2 * d_),
                                  "margen_bruto_nuevo": float(GP2 / R2), "cambio_margen_bruto_pb": float((GP2 / R2 - m) * 10000),
                                  "cambio_utilidad_operativa": float(d_oi), "cambio_utilidad_operativa_pct": float(d_oi / OI),
                                  "cambio_upa_ntd": float(d_un / acc), "cambio_upa_usd_por_ads": float(d_un / acc * ads / fx),
                                  "doble_conteo_si_d_fuera_dilucion_total": float(R2 * D("0.02")),
                                  "control_identidad_cogs": float(err)})
    ref = g["referencias_exposicion"]
    peor = min(filas, key=lambda x: x["cambio_utilidad_operativa"])
    return {
        "naturaleza": "sensibilidad hipotetica: e, r, c y d son supuestos; no hay probabilidades ni valor esperado",
        "base": {"ingresos_12m": float(R), "utilidad_bruta_12m": float(GP), "margen_bruto_12m": float(m),
                 "utilidad_operativa_12m": float(OI), "tasa_impuestos": float(t), "acciones": float(acc),
                 "c_referencia_1_menos_costo_no_depreciacion": 1 - (t12["ingresos"] - t12["utilidad_bruta"] - t12["da"]) / t12["ingresos"]},
        "referencias": {
            "china_sede_pct_1s26": ref["china_sede_1s26"] / ref["ingresos_1s26"],
            "china_sede_pct_2t26": ref["china_sede_2t26"] / ref["ingresos_2t26"],
            "china_sede_pct_fy2025": ref["china_sede_fy2025"] / ref["ingresos_fy2025_item5"],
            "eeuu_sede_pct_1s26": ref["eeuu_sede_1s26"] / ref["ingresos_1s26"],
            "taiwan_sede_pct_1s26": ref["taiwan_sede_1s26"] / ref["ingresos_1s26"]},
        "celdas": len(filas), "control_max_error_identidad": float(max_err), "control_ok": max_err == 0,
        "peor_celda": peor,
        "doble_conteo": {"regla": ("si d se tomara como la dilucion TOTAL comunicada (2-4 pp) en lugar de la incremental (0-2 pp), "
                                   "cada celda restaria 2 pp x R' de mas"),
                         "sobreestimacion_min": min(f["doble_conteo_si_d_fuera_dilucion_total"] for f in filas),
                         "sobreestimacion_max": max(f["doble_conteo_si_d_fuera_dilucion_total"] for f in filas)},
        "filas": filas,
    }


# ------------------------------------------------------------------ mecanismo: punto de quiebre de liquidez

def punto_de_quiebre(base: dict) -> dict:
    """Recorte paralelo s (pp) a margen bruto y operativo de TODOS los anos del escenario de tension, con capex y
    dividendos sin cambio, a partir del cual el motor necesita revolvente (caja < caja_minima). Biseccion."""
    norm = mi.normalizar_base(base)
    ultimo = norm["periodos"][-1]
    sup = base["supuestos"]
    esc0 = sup["escenarios"]["tension"]

    def financiamiento(s):
        esc = copy.deepcopy(esc0)
        esc["margen_bruto"] = [x - s for x in esc0["margen_bruto"]]
        esc["margen_operativo"] = [x - s for x in esc0["margen_operativo"]]
        p = mi.proyectar_escenario(ultimo, "tension_recorte", esc, sup["anos"], sup["caja_minima"])
        return p["resumen"]["financiamiento_requerido_total"], p

    lo, hi = 0.0, 0.40
    if financiamiento(hi)[0] <= 0:
        return {"estado": "sin quiebre hasta 40 pp", "recorte_pp": None}
    if financiamiento(lo)[0] > 0:
        return {"estado": "requiere financiamiento sin recorte", "recorte_pp": 0.0}
    for _ in range(60):
        mid = (lo + hi) / 2
        if financiamiento(mid)[0] > 0:
            hi = mid
        else:
            lo = mid
    _, p = financiamiento(hi)
    return {"naturaleza": "calculo de mecanismo sobre el escenario de tension; no es pronostico",
            "recorte_paralelo_margenes": hi, "recorte_pp": 100 * hi,
            "margen_bruto_resultante": [x - hi for x in esc0["margen_bruto"]],
            "margen_operativo_resultante": [x - hi for x in esc0["margen_operativo"]],
            "primer_periodo_con_financiamiento": p["resumen"]["periodos_con_financiamiento"][:1],
            "caja_minima": sup["caja_minima"], "capex_y_dividendos": "sin cambio respecto a tension"}


# ------------------------------------------------------------------ diagnosticos de escenarios

def diagnosticos(base: dict, res: dict) -> dict:
    ic = base["insumos_complementarios"]
    fx_ref = ic["anclas_escenarios"]["guia_3T26"]["tipo_cambio"]
    u = ic["anclas_escenarios"]["ingresos_usd_miles_de_millones"]
    q24 = ic["anclas_escenarios"]["ingresos_usd_2024_trimestres"]
    usd_2025 = u["1T25"] + u["2T25"] + u["3T25"] + u["4T25"]
    usd_2024 = q24["1T24"] + q24["2T24_calculado"] + q24["3T24"] + q24["4T24"]
    amort = ic["depreciacion"]["amortizacion_ventas"]
    out = {"tipo_cambio_de_conversion": fx_ref, "ingresos_usd_2025_miles_de_millones": usd_2025,
           "ingresos_usd_2024_miles_de_millones_calculado": usd_2024, "escenarios": {}}
    for n, e in res["escenarios"].items():
        filas, cap_prev = [], res["historico"]["periodos"][-1]["balance"]["capital_contable"]
        for p in e["periodos"]:
            r, b, f, mv = p["resultados"], p["balance"], p["flujo"], p["movimientos"]["ppe"]
            usd = r["ingresos"] / fx_ref / 1000.0
            filas.append({"periodo": p["periodo"], "ingresos_usd_miles_de_millones_a_32": usd,
                          "depreciacion_sobre_ppe_inicial": (r["depreciacion_amortizacion"] - amort * r["ingresos"]) / mv["ppe_inicial"],
                          "fcf_sobre_utilidad_neta": f["fcf"] / r["utilidad_neta"],
                          "fcf_menos_dividendos": f["fcf"] - f["dividendos"],
                          "roe_sobre_capital_promedio": r["utilidad_neta"] / ((cap_prev + b["capital_contable"]) / 2),
                          "capex_usd_miles_de_millones_a_32": f["capex"] / fx_ref / 1000.0})
            cap_prev = b["capital_contable"]
        crec_2026 = filas[0]["ingresos_usd_miles_de_millones_a_32"] / usd_2025 - 1
        cagr_24_29 = (filas[3]["ingresos_usd_miles_de_millones_a_32"] / usd_2024) ** (1 / 5) - 1
        out["escenarios"][n] = {"crecimiento_usd_2026": crec_2026, "cagr_usd_2024_2029": cagr_24_29, "filas": filas,
                                "nota": "conversion a USD con el tipo de cambio de la guia del 3T26 (32): supuesto de presentacion"}
    return out


# ------------------------------------------------------------------ D01: precio contra el archivo congelado

def control_precios(base: dict) -> list:
    d = base["insumos_complementarios"]["dcf_inverso"]
    out = []
    for archivo, clave in (("yahoo_TSM_1mo.json", "precio_adr"), ("yahoo_2330.TW_1mo.json", "precio_local"),
                           ("yahoo_TWD_X_1mo.json", "tipo_cambio")):
        j = json.loads((AQUI / "datos" / archivo).read_text(encoding="utf-8"))["chart"]["result"][0]
        off = j["meta"].get("gmtoffset", 0)
        from datetime import datetime, timezone
        cierre = None
        for ts, c in zip(j["timestamp"], j["indicators"]["quote"][0]["close"]):
            if c is not None and datetime.fromtimestamp(ts + off, tz=timezone.utc).date().isoformat() == "2026-09-24":
                cierre = c
        out.append(_reg("D01", f"{clave} = cierre del 2026-09-24 en datos/{archivo}", "2026-09-24", round(cierre, 4),
                        _v(d, clave), 0.00051))
    return out


# ------------------------------------------------------------------ corrida

def main() -> int:
    base = mi.cargar_json(AQUI / "base.json")
    res = mi.construir_modelo(base)
    t12 = ttm(base)
    propios = controles_transcripcion(base)
    puente_ctrl, puente_tabla = controles_puente(base)
    propios += puente_ctrl + control_precios(base)
    propios.append(_reg("T03", "FCF del emisor de 12 meses (CFO - capex) = suma de los cuatro trimestres publicados",
                        "12m a jun-2026", t12["fcf_emisor_suma_trimestres"], t12["fcf_emisor"], 20.0,
                        "diapositivas en miles de millones con dos decimales: redondeo de hasta 4 x 5 millones"))
    geo = sensibilidad_geopolitica(base, t12)
    propios.append({"id": "G01", "prueba": "identidad COGS' en las 81 celdas de la rejilla", "periodo": "rejilla",
                    "esperado": 0.0, "obtenido": geo["control_max_error_identidad"], "diferencia": geo["control_max_error_identidad"],
                    "tolerancia": 0.0, "estado": "OK" if geo["control_ok"] else "FALLA", "detalle": "Decimal exacto"})
    res["ttm"] = t12
    res["dcf_inverso"] = dcf_inverso_tsm(base, t12)
    res["sensibilidad_geopolitica"] = geo
    res["puente_margen_bruto"] = puente_tabla
    res["punto_de_quiebre_financiamiento"] = punto_de_quiebre(base)
    res["diagnosticos_escenarios"] = diagnosticos(base, res)
    resumen_propios = {"total": len(propios), "OK": sum(c["estado"] == "OK" for c in propios),
                       "FALLA": sum(c["estado"] == "FALLA" for c in propios),
                       "por_id": {i: sum(1 for c in propios if c["id"] == i) for i in sorted({c["id"] for c in propios})},
                       "fallas": [c for c in propios if c["estado"] != "OK"]}
    res["controles_propios"] = propios
    res["resumen_controles_propios"] = resumen_propios
    mi.guardar_json(res, AQUI / "resultados.json")
    releido = mi.cargar_json(AQUI / "resultados.json")
    auditoria = mi.resumir_controles(mi.verificar(releido))
    coincide = all(auditoria[k] == res["resumen_controles"][k] for k in ("total", "OK", "FALLA", "INFO", "NO_APLICA"))
    rutas = [AQUI / "base.json", AQUI / "modelo.py", AQUI / "resultados.json"]
    if (AQUI / "datos" / "SHA256SUMS.txt").exists():
        rutas.append(AQUI / "datos" / "SHA256SUMS.txt")
    mi.escribir_sha256sums(rutas, AQUI / "SHA256SUMS.txt")
    print(mi.resumen_markdown(res))
    dcf = res["dcf_inverso"]
    print(f"DCF inverso base (USD): WACC {dcf['wacc']['wacc']:.4%}, g {dcf['insumos']['g_terminal']:.2%}, margen FCF "
          f"{dcf['insumos']['margen_fcf_base']:.4%} -> crecimiento implicito {dcf['base']['crecimiento_implicito']:.4%} "
          f"({dcf['base']['estado']}); rango de la rejilla {dcf['rango_sensibilidad'][0]:.2%} a {dcf['rango_sensibilidad'][1]:.2%}")
    print(f"Sensibilidad geopolitica: {geo['celdas']} celdas; identidad COGS max error {geo['control_max_error_identidad']}")
    pq = res["punto_de_quiebre_financiamiento"]
    print(f"Punto de quiebre de liquidez (tension): recorte paralelo de {pq.get('recorte_pp')} pp")
    print(f"Controles propios: {resumen_propios['total']} registros, FALLA {resumen_propios['FALLA']} ({resumen_propios['por_id']})")
    print(f"Auditoria de resultados.json releido: {'coincide' if coincide else 'NO COINCIDE'} "
          f"({auditoria['total']} registros, FALLA {auditoria['FALLA']})")
    ok = res["resumen_controles"]["todos_ok"] and coincide and resumen_propios["FALLA"] == 0
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
