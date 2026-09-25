"""Modelo integrado de NVIDIA (NVDA): historico FY2024-FY2026, 3 escenarios de mecanismo, DCF inverso y
sensibilidad geopolitica reproducible.

FASE 0 (formacion). Los escenarios son supuestos explicitos de mecanismo (tension / intermedio / eficiencia):
no son pronosticos, ni guia del emisor, ni consenso, ni recomendacion de compra o venta.
Solo biblioteca estandar de Python 3.11. Uso (desde cualquier directorio):

    python3 empresas/NVDA/modelo/modelo.py

Escribe resultados.json y SHA256SUMS.txt junto a este archivo e imprime el resumen en markdown.
Sale con codigo 1 si algun control del motor FALLA o si la auditoria de resultados.json releido no
coincide con la corrida.
"""
import sys
from decimal import Decimal, getcontext
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[2]))
from herramientas import modelo_integrado as mi  # noqa: E402

getcontext().prec = 40


def _v(bloque: dict, clave: str) -> float:
    return float(bloque[clave]["valor"])


# ------------------------------------------------------------------ DCF inverso

def wacc_bottom_up(d: dict, beta_u: float) -> dict:
    """WACC con beta del sector reapalancada (conocimiento/03 s2.3). Pesos a valor de mercado."""
    e = _v(d, "precio") * _v(d, "acciones_diluidas")
    deuda = _v(d, "deuda_financiera") + _v(d, "arrendamientos_operativos")
    t = _v(d, "tasa_impuesto_marginal")
    beta_l = beta_u * (1 + (1 - t) * deuda / e)
    ke = _v(d, "tasa_libre_riesgo") + beta_l * _v(d, "erp")
    kd_dt = _v(d, "costo_deuda_antes_impuestos") * (1 - t)
    w = (e * ke + deuda * kd_dt) / (e + deuda)
    return {"capitalizacion": e, "deuda_y_arrendamientos": deuda, "d_e": deuda / e, "beta_desapalancada": beta_u,
            "beta_reapalancada": beta_l, "costo_capital_acciones": ke, "costo_deuda_despues_impuestos": kd_dt,
            "wacc": w, "naturaleza": "calculo con insumos citados; beta y ERP son estimaciones, no hechos del emisor"}


def dcf_inverso_nvda(base: dict) -> dict:
    d = base["insumos_complementarios"]["dcf_inverso"]
    ingresos_12m = _v(d, "ingresos_fy2026") - _v(d, "ingresos_1s_fy2026") + _v(d, "ingresos_1s_fy2027")
    fcf_12m = _v(d, "fcf_emisor_fy2026") - _v(d, "fcf_emisor_1s_fy2026") + _v(d, "fcf_emisor_1s_fy2027")
    sbc_12m = _v(d, "sbc_fy2026") - _v(d, "sbc_1s_fy2026") + _v(d, "sbc_1s_fy2027")
    margen_base = (fcf_12m - sbc_12m) / ingresos_12m
    deuda_neta = (_v(d, "deuda_financiera") + _v(d, "arrendamientos_operativos") - _v(d, "caja")
                  - _v(d, "valores_de_deuda_negociables"))
    inversiones_capital = (_v(d, "valores_de_capital_negociables") + _v(d, "valores_de_capital_publicos_lp")
                           + _v(d, "valores_no_negociables"))
    deuda_neta_ampliada = deuda_neta - inversiones_capital
    w_sector = wacc_bottom_up(d, _v(d, "beta_desapalancada_sector"))
    w_regr = wacc_bottom_up(d, _v(d, "beta_regresion_1a"))
    w0 = w_sector["wacc"]
    g0 = _v(d, "g_terminal")
    anos = int(_v(d, "anos"))
    rf = _v(d, "tasa_libre_riesgo")
    precio, acciones = _v(d, "precio"), _v(d, "acciones_diluidas")

    def correr(w, g, m, dn):
        r = mi.dcf_inverso(precio, acciones, dn, w, g, m, anos, ingresos_base=ingresos_12m, tasa_libre_riesgo=rf)
        sol = r.get("solucion") or {}
        return {"wacc": w, "g_terminal": g, "margen_fcf": m, "deuda_neta": dn, "estado": r["estado"],
                "crecimiento_implicito": r["crecimiento_implicito"], "peso_terminal": sol.get("peso_terminal"),
                "multiplo_terminal_fcf": sol.get("multiplo_terminal_fcf"),
                "ingresos_ano_final": (sol.get("flujos") or [{}])[-1].get("ingresos"),
                "residuo": r.get("residuo"), "alertas": r["alertas"]}

    base_run = mi.dcf_inverso(precio, acciones, deuda_neta, w0, g0, margen_base, anos, ingresos_base=ingresos_12m,
                              tasa_libre_riesgo=rf)
    m_bajo, m_alto = d["margenes_fcf_sensibilidad"]["valor"]
    rejilla = []
    for m in (m_bajo, margen_base, m_alto):
        for w in (w0 - 0.01, w0, w0 + 0.01):
            for g in (g0 - 0.005, g0, g0 + 0.005):
                rejilla.append(correr(w, g, m, deuda_neta))
    variantes = {
        "deuda_neta_ampliada_resta_inversiones_de_capital": correr(w0, g0, margen_base, deuda_neta_ampliada),
        "beta_regresion_1a": correr(w_regr["wacc"], g0, margen_base, deuda_neta),
    }
    return {
        "naturaleza": "calculo: crecimiento que descuenta el precio bajo supuestos explicitos; no es pronostico",
        "insumos": {"precio": precio, "fecha_precio": "2026-09-24", "acciones_diluidas": acciones,
                    "ingresos_12m": ingresos_12m, "fcf_emisor_12m": fcf_12m, "sbc_12m": sbc_12m,
                    "margen_fcf_base": margen_base,
                    "definicion_margen": "(FCF del emisor de 12 meses - SBC de 12 meses) / ingresos de 12 meses",
                    "deuda_neta": deuda_neta,
                    "definicion_deuda_neta": "deuda financiera + arrendamientos operativos - caja - valores de deuda negociables",
                    "inversiones_de_capital": inversiones_capital, "deuda_neta_ampliada": deuda_neta_ampliada,
                    "g_terminal": g0, "anos": anos, "tasa_libre_riesgo": rf},
        "wacc": w_sector, "wacc_beta_regresion": w_regr,
        "base": {k: base_run[k] for k in ("estado", "crecimiento_implicito", "residuo", "valor_por_accion_en_solucion",
                                          "alertas", "supuestos")},
        "base_solucion": {k: base_run["solucion"][k] for k in ("valor_empresa", "vp_flujos", "valor_terminal",
                                                                "vp_terminal", "peso_terminal", "multiplo_terminal_fcf")},
        "base_flujos": base_run["solucion"]["flujos"],
        "sensibilidad": rejilla,
        "variantes": variantes,
    }


# ------------------------------------------------------------------ sensibilidad geopolitica

def sensibilidad_geopolitica(base: dict) -> dict:
    """Rejilla completa fraccion restringida x sustitucion x margen de contribucion perdido (27 celdas).

    L = R x e x (1 - r) ingresos perdidos; perdida bruta = L x c (c = fraccion del ingreso perdido que no se
    ahorra en costo); GP' = GP - L x c; R' = R - L. Gastos de operacion fijos: la perdida operativa = L x c.
    Doble comprobacion algebraica: COGS' = (R - GP) - L x (1 - c) y GP' = R' - COGS'. Decimal exacto."""
    g = base["insumos_complementarios"]["geopolitica"]
    D = lambda x: Decimal(str(x))  # noqa: E731
    R = D(_v(g, "ingresos_12m"))
    GP = D(_v(g, "utilidad_bruta_fy2026")) - D(_v(g, "utilidad_bruta_1s_fy2026")) + D(_v(g, "utilidad_bruta_1s_fy2027"))
    OI = (D(_v(g, "utilidad_operativa_fy2026")) - D(_v(g, "utilidad_operativa_1s_fy2026"))
          + D(_v(g, "utilidad_operativa_1s_fy2027")))
    t = D(_v(g, "tasa_impuestos"))
    acc = D(_v(g, "acciones_diluidas"))
    rj = g["rejilla"]
    filas, max_err = [], Decimal(0)
    for e in rj["fraccion_restringida"]:
        for r in rj["sustitucion"]:
            for c in rj["margen_contribucion_perdido"]:
                e_, r_, c_ = D(e), D(r), D(c)
                L = R * e_ * (1 - r_)
                R2 = R - L
                GP2 = GP - L * c_
                COGS2 = (R - GP) - L * (1 - c_)
                err = abs((R2 - COGS2) - GP2)
                max_err = max(max_err, err)
                d_oi = -L * c_
                d_un = d_oi * (1 - t)
                filas.append({"fraccion_restringida": e, "sustitucion": r, "margen_contribucion_perdido": c,
                              "ingresos_perdidos": float(L), "ingresos_nuevos": float(R2),
                              "utilidad_bruta_nueva": float(GP2), "margen_bruto_base": float(GP / R),
                              "margen_bruto_nuevo": float(GP2 / R2),
                              "cambio_margen_bruto_pb": float((GP2 / R2 - GP / R) * 10000),
                              "cambio_utilidad_operativa": float(d_oi),
                              "cambio_utilidad_operativa_pct": float(d_oi / OI),
                              "cambio_utilidad_neta": float(d_un),
                              "cambio_upa_usd": float(d_un / acc),
                              "control_identidad_cogs": float(err)})
    ref = g["referencias_exposicion"]
    ing_fy26 = _v(base["insumos_complementarios"]["dcf_inverso"], "ingresos_fy2026")
    return {
        "naturaleza": "sensibilidad hipotetica: e, r y c son supuestos; no hay probabilidades ni valor esperado",
        "base": {"ingresos_12m": float(R), "utilidad_bruta_12m": float(GP), "margen_bruto_12m": float(GP / R),
                 "utilidad_operativa_12m": float(OI), "tasa_impuestos": float(t), "acciones_diluidas": float(acc)},
        "referencias": {
            "china_hk_sede_pct_fy2026": _v(ref, "china_hk_sede_fy2026") / ing_fy26,
            "china_hk_sede_pct_2t_fy2027": _v(ref, "china_hk_sede_2t_fy2027") / _v(ref, "ingresos_2t_fy2027"),
            "otros_paises_sede_pct_fy2026": _v(ref, "otros_paises_sede_fy2026") / ing_fy26,
            "taiwan_sede_pct_fy2026": _v(ref, "taiwan_sede_fy2026") / ing_fy26,
            "cargo_H20_pct_ingresos_fy2026": _v(ref, "cargo_H20") / ing_fy26,
            "cargo_H20_mas_H200": _v(ref, "cargo_H20") + _v(ref, "cargo_H200"),
        },
        "celdas": len(filas),
        "control_max_error_identidad": float(max_err),
        "control_ok": max_err == 0,
        "filas": filas,
    }


# ------------------------------------------------------------------ corrida

def main() -> int:
    base = mi.cargar_json(AQUI / "base.json")
    res = mi.construir_modelo(base)
    res["dcf_inverso"] = dcf_inverso_nvda(base)
    res["sensibilidad_geopolitica"] = sensibilidad_geopolitica(base)
    mi.guardar_json(res, AQUI / "resultados.json")
    # Auditoria: releer resultados.json y recalcular TODOS los controles desde los estados guardados.
    releido = mi.cargar_json(AQUI / "resultados.json")
    auditoria = mi.resumir_controles(mi.verificar(releido))
    coincide = all(auditoria[k] == res["resumen_controles"][k] for k in ("total", "OK", "FALLA", "INFO", "NO_APLICA"))
    mi.escribir_sha256sums([AQUI / "base.json", AQUI / "modelo.py", AQUI / "resultados.json"], AQUI / "SHA256SUMS.txt")
    print(mi.resumen_markdown(res))
    dcf = res["dcf_inverso"]
    print(f"DCF inverso base: WACC {dcf['wacc']['wacc']:.4%}, g {dcf['insumos']['g_terminal']:.2%}, "
          f"margen FCF {dcf['insumos']['margen_fcf_base']:.4%} -> crecimiento implicito "
          f"{dcf['base']['crecimiento_implicito']:.4%} ({dcf['base']['estado']})")
    geo = res["sensibilidad_geopolitica"]
    print(f"Sensibilidad geopolitica: {geo['celdas']} celdas, identidad COGS max error {geo['control_max_error_identidad']}")
    print(f"Auditoria de resultados.json releido: {'coincide' if coincide else 'NO COINCIDE'} "
          f"({auditoria['total']} registros, FALLA {auditoria['FALLA']})")
    ok = res["resumen_controles"]["todos_ok"] and coincide and geo["control_ok"]
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
