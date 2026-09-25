"""Pruebas de herramientas/modelo_integrado.py (sin red).

Caso sintetico hecho a mano (cuadra al centavo; aritmetica en los comentarios) y casos alterados que
DEBEN fallar controles especificos. Correr desde la raiz: python3 -m unittest herramientas.tests.test_modelo_integrado
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from herramientas import modelo_integrado as mi


def base_sintetica() -> dict:
    """Dos ejercicios que cuadran.

    FY2024: UB 400 = 1000 - 600; UO 200 = 400 - 200; UAI 195 = 200 - 10 + 5; UN 156 = 195 - 39.
      Activo 1000 = 100+50+120+80+20+500+130; pasivo 450 = 90+60+200+30+70; capital 550.
      CFO 200 = 156+50+10-20+4; CFI -70 = -60-10; CFF -110 = -20-5-40-45; caja 80+200-70-110 = 100.
      Capital 550 = 469+156+10-40-45; URE 400 = 329+156-40-45.
    FY2025: UB 451; UO 231 = 451 - 220; intereses 10.5 = 5% x (200+220)/2; UAI 225 = 231-10.5+4.5; UN 180.
      Activo 1123 = 168+50+130+85+22+523+145; pasivo 485 = 100+63+220+32+70; capital 638.
      CFO 245 = 180+55+12-5+3; CFI -85; CFF -93 = 50-30-6-50-60+5-2; caja 100+245-85-93+1 = 168.
      Capital 638 = 550+180+12-50-60+5+1 (ORI); URE 470 = 400+180-50-60.
      PPE 523 = 500+78-55 (adiciones = capex 70 + arrendamientos nuevos 8); deuda 220 = 200+50-30;
      arrendamientos 32 = 30+8-6.
    """
    return {
        "empresa": "Sintetica SA", "ticker": "SINT", "moneda": "USD", "unidades": "millones",
        "fecha_corte": "2026-09-25",
        "fuentes": {"S1": {"documento": "caso sintetico de prueba", "fecha": "2026-09-25"}},
        "historico": [
            {"periodo": "FY2024", "anio": 2024, "fin": "2024-12-31", "fuente": "S1 tabla 1",
             "resultados": {"ingresos": 1000, "costo_ventas": 600, "utilidad_bruta": 400, "gastos_operativos": 200,
                            "utilidad_operativa": 200, "gasto_intereses": 10, "otros_ingresos": 5,
                            "utilidad_antes_impuestos": 195, "impuestos": 39, "utilidad_neta": 156},
             "balance": {"caja": 100, "inversiones_cp": 50, "cuentas_por_cobrar": 120, "inventarios": 80,
                         "otros_activos_circulantes": 20, "ppe_neto": 500, "otros_activos_lp": 130,
                         "activo_total": 1000, "proveedores": 90, "otros_pasivos_circulantes": 60, "deuda": 200,
                         "arrendamientos_financieros": 30, "otros_pasivos_lp": 70, "pasivo_total": 450,
                         "capital_contable": 550, "utilidades_retenidas": 400},
             "flujo": {"caja_inicial": 80, "utilidad_neta": 156, "depreciacion_amortizacion": 50, "sbc": 10,
                       "cambio_capital_trabajo": -20, "otros_operativos": {"impuestos_diferidos": 3, "otros": 1},
                       "cfo": 200, "capex": 60, "otros_inversion": -10, "cfi": -70, "emision_deuda": 0,
                       "amortizacion_deuda": 20, "principal_arrendamientos_financieros": 5, "dividendos": 40,
                       "recompras": 45, "emision_acciones": 0, "otros_financiamiento": 0, "cff": -110,
                       "efecto_cambiario": 0, "caja_final": 100},
             "movimientos_capital": {"capital_inicial": 469, "utilidades_retenidas_iniciales": 329,
                                     "dividendos_declarados": 40, "recompras": 45,
                                     "recompras_contra_utilidades_retenidas": 45}},
            {"periodo": "FY2025", "anio": 2025, "fin": "2025-12-31", "fuente": "S1 tabla 2",
             "fuentes_campos": {"flujo.capex": "S1 tabla 2, renglon 7"},
             "resultados": {"ingresos": 1100, "costo_ventas": 649, "utilidad_bruta": 451, "gastos_operativos": 220,
                            "utilidad_operativa": 231, "gasto_intereses": 10.5, "otros_ingresos": 4.5,
                            "utilidad_antes_impuestos": 225, "impuestos": 45, "utilidad_neta": 180},
             "balance": {"caja": 168, "inversiones_cp": 50, "cuentas_por_cobrar": 130, "inventarios": 85,
                         "otros_activos_circulantes": 22, "ppe_neto": 523, "otros_activos_lp": 145,
                         "activo_total": 1123, "proveedores": 100, "otros_pasivos_circulantes": 63, "deuda": 220,
                         "arrendamientos_financieros": 32, "otros_pasivos_lp": 70, "pasivo_total": 485,
                         "capital_contable": 638, "utilidades_retenidas": 470},
             "flujo": {"utilidad_neta": 180, "depreciacion_amortizacion": 55, "sbc": 12,
                       "cambio_capital_trabajo": -5, "otros_operativos": 3, "cfo": 245, "capex": 70,
                       "otros_inversion": -15, "cfi": -85, "emision_deuda": 50, "amortizacion_deuda": 30,
                       "principal_arrendamientos_financieros": 6, "dividendos": 50, "recompras": 60,
                       "emision_acciones": 5, "otros_financiamiento": -2, "cff": -93, "efecto_cambiario": 1,
                       "fcf_reportado": 175},
             "movimientos_capital": {"dividendos_declarados": 50, "recompras": 60, "ori": 1,
                                     "recompras_contra_utilidades_retenidas": 60},
             "movimientos_ppe": {"adiciones": 78, "depreciacion": 55, "otros": 0},
             "movimientos_deuda": {"emisiones": 50, "amortizaciones": 30, "otros": 0},
             "movimientos_arrendamientos": {"nuevos": 8},
             "ajustado": {"base": "utilidad_neta", "ajustes": {"ganancia_no_recurrente": -10},
                          "valor_ajustado": 170, "fuente": "S1 tabla 3"}},
        ],
    }


def supuestos_sinteticos() -> dict:
    return {
        "anos": 5, "caja_minima": 60,
        "nota": "Supuestos de escenario para pruebas; no son pronosticos",
        "escenarios": {
            "continuidad": {
                "descripcion": "drivers cercanos a FY2025", "crecimiento_ingresos": 0.08, "margen_bruto": 0.41,
                "margen_operativo": 0.21, "tasa_impuestos": 0.2, "da_ventas": 0.05, "capex_ventas": 0.065,
                "sbc_ventas": 0.011, "dias_cxc": 43, "dias_inventario": 48, "dias_proveedores": 56,
                "tasa_interes": 0.05, "dividendos_payout": 0.3, "recompras": 40, "amortizacion_deuda": 20,
                "principal_arrendamientos_financieros": 6, "nuevos_arrendamientos_financieros": 8,
                "tasa_arrendamientos_financieros": 0.04, "tasa_rendimiento_caja": 0.03,
                "ajuste_utilidad_neta": -5},
            "tension": {
                "descripcion": "margen cae y capex alto con recompras: fuerza revolvente",
                "crecimiento_ingresos": [-0.05, 0.0, 0.02, 0.03, 0.03], "margen_bruto": 0.38,
                "margen_operativo": 0.08, "tasa_impuestos": 0.2, "da_ventas": 0.05,
                "capex_ventas": [0.12, 0.12, 0.04, 0.04, 0.04], "sbc_ventas": 0.011, "dias_cxc": 50,
                "dias_inventario": 55, "dias_proveedores": 50, "tasa_interes": 0.06, "tasa_revolvente": 0.09,
                "dividendos": 20, "recompras": [100, 100, 0, 0, 0], "amortizacion_deuda": 20,
                "principal_arrendamientos_financieros": 6, "amortizacion_intangibles": 3},
        },
    }


def modelo(base=None, sup=None):
    return mi.construir_modelo(base if base is not None else base_sintetica(),
                               sup if sup is not None else supuestos_sinteticos())


def estados(controles, cid, ambito=None, periodo=None):
    return [c["estado"] for c in controles if c["id"] == cid
            and (ambito is None or c["ambito"] == ambito) and (periodo is None or c["periodo"] == periodo)]


def fallan(controles) -> set:
    return {c["id"] for c in controles if c["estado"] == "FALLA"}


class TestCasoQueCuadra(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.res = modelo()

    def test_todos_los_controles_ok(self):
        rc = self.res["resumen_controles"]
        self.assertTrue(rc["todos_ok"], rc["fallas"])
        self.assertEqual(rc["FALLA"], 0)

    def test_al_menos_13_tipos_de_control_evaluados(self):
        ids = self.res["resumen_controles"]["ids_evaluados"]
        self.assertGreaterEqual(len(ids), 13)
        self.assertEqual(ids, [f"C{i:02d}" for i in range(1, 17)])
        self.assertEqual(len(mi.CONTROLES), 16)

    def test_cada_registro_declara_tolerancia_y_estado(self):
        for c in self.res["controles"]:
            self.assertIn(c["estado"], ("OK", "FALLA", "INFO", "NO_APLICA"))
            self.assertIsInstance(c["tolerancia"], float)
            self.assertGreater(c["tolerancia"], 0)
            for k in ("id", "control", "prueba", "ambito", "periodo", "esperado", "obtenido", "diferencia", "detalle"):
                self.assertIn(k, c)

    def test_controles_reales_en_historico(self):
        ctl = self.res["controles"]
        for cid in ("C01", "C02", "C03", "C04", "C07", "C12", "C14", "C15"):
            self.assertIn("OK", estados(ctl, cid, "historico", "FY2025"), cid)
        for cid in ("C05", "C06", "C13"):
            self.assertEqual(set(estados(ctl, cid, "historico", "FY2025")), {"OK"}, cid)
        # primer ejercicio: con saldos iniciales explicitos C03/C04 se prueban; C13 no aplica
        self.assertEqual(estados(ctl, "C03", "historico", "FY2024"), ["OK"])
        self.assertEqual(estados(ctl, "C04", "historico", "FY2024"), ["OK"])
        self.assertEqual(estados(ctl, "C13", "historico", "FY2024"), ["NO_APLICA"])
        # C08-C11 en el historico son implicitos: se informan, no se "aprueban"
        self.assertEqual(set(estados(ctl, "C08", "historico")), {"INFO"})

    def test_reconciliacion_reproduce_el_historico(self):
        rec = self.res["historico"]["reconciliacion"]["FY2025"]
        self.assertLessEqual(rec["max_diferencia"], 1e-9)
        self.assertEqual(rec["lineas_fuera_de_tolerancia"], [])
        lineas = {c["linea"]: c for c in rec["comparacion"]}
        self.assertAlmostEqual(lineas["balance.caja"]["modelo"], 168.0, places=9)
        self.assertAlmostEqual(lineas["resultados.utilidad_neta"]["modelo"], 180.0, places=9)
        self.assertAlmostEqual(lineas["resultados.gasto_intereses"]["modelo"], 10.5, places=9)

    def test_partidas_conciliatorias_explicitas(self):
        partidas = {p["partida"].split(" (")[0]: p for p in
                    self.res["historico"]["reconciliacion"]["FY2025"]["partidas_conciliatorias"]}
        self.assertAlmostEqual(partidas["otros_operativos del CFO"]["monto"], 3.0, places=9)
        self.assertAlmostEqual(partidas["otros_financiamiento"]["monto"], -2.0, places=9)
        self.assertAlmostEqual(partidas["otros_inversion"]["monto"], -15.0, places=9)
        self.assertAlmostEqual(partidas["nuevos arrendamientos financieros"]["monto"], 8.0, places=9)
        self.assertAlmostEqual(partidas["movimiento no monetario / no explicado en otros_pasivos_circulantes"]["monto"],
                               3.0, places=9)
        self.assertFalse(any(p["material"] for p in partidas.values()))

    def test_drivers_implicitos(self):
        d = self.res["historico"]["drivers_implicitos"]["FY2025"]
        self.assertAlmostEqual(d["crecimiento_ingresos"], 0.10)
        self.assertAlmostEqual(d["tasa_interes_sobre_deuda"], 0.05)
        self.assertAlmostEqual(d["tasa_impuestos"], 0.20)
        self.assertAlmostEqual(d["dias_cxc"], 130 * 365 / 1100)
        self.assertAlmostEqual(d["fcf"], 175.0)
        self.assertAlmostEqual(d["fcf_despues_arrendamientos"], 169.0)
        self.assertEqual(self.res["historico"]["drivers_implicitos"]["FY2024"]["crecimiento_ingresos"], None)

    def test_gaap_vs_ajustado(self):
        filas = self.res["historico"]["ajustado"]
        self.assertEqual(len(filas), 1)
        self.assertEqual(filas[0]["ajustado"], 170.0)
        self.assertEqual(estados(self.res["controles"], "C14", "historico"), ["OK"])

    def test_balance_cuadra_y_caja_es_cierre_en_proyeccion(self):
        for esc in self.res["escenarios"].values():
            prev_caja = self.res["historico"]["periodos"][-1]["balance"]["caja"]
            for p in esc["periodos"]:
                b, f = p["balance"], p["flujo"]
                self.assertAlmostEqual(b["activo_total"], b["pasivo_total"] + b["capital_contable"], places=7)
                self.assertAlmostEqual(prev_caja + f["cfo"] + f["cfi"] + f["cff"], b["caja"], places=7)
                self.assertGreaterEqual(b["caja"], p["supuestos"]["caja_minima"] - 1e-7)
                prev_caja = b["caja"]

    def test_financiamiento_requerido_explicito_y_barrido(self):
        esc = self.res["escenarios"]["tension"]
        per = esc["periodos"]
        self.assertGreater(per[0]["flujo"]["disposicion_revolvente"], 0)
        self.assertAlmostEqual(per[0]["balance"]["caja"], 60.0, places=7)
        self.assertEqual(esc["resumen"]["periodos_con_financiamiento"], ["2026E", "2027E"])
        self.assertAlmostEqual(esc["resumen"]["financiamiento_requerido_total"],
                               sum(p["flujo"]["disposicion_revolvente"] for p in per))
        self.assertTrue(any("FINANCIAMIENTO REQUERIDO" in a for a in esc["alertas"]))
        # anos 3-5: capex bajo y sin recompras -> el excedente paga revolvente
        self.assertGreater(per[2]["flujo"]["pago_revolvente"], 0)
        self.assertLess(per[-1]["balance"]["revolvente"], esc["resumen"]["revolvente_maximo"])
        self.assertEqual(self.res["escenarios"]["continuidad"]["resumen"]["financiamiento_requerido_total"], 0.0)

    def test_intereses_circulares_sobre_revolvente(self):
        p = self.res["escenarios"]["tension"]["periodos"][1]
        pv = self.res["escenarios"]["tension"]["periodos"][0]["balance"]
        s, b = p["supuestos"], p["balance"]
        esperado = (s["tasa_interes"] * (pv["deuda"] + b["deuda"]) / 2
                    + s["tasa_revolvente"] * (pv["revolvente"] + b["revolvente"]) / 2)
        self.assertAlmostEqual(p["resultados"]["gasto_intereses"], esperado, places=9)
        self.assertEqual(set(estados(self.res["controles"], "C10", "escenario:tension")), {"OK"})

    def test_dividendos_por_payout_y_amortizacion_de_intangibles(self):
        p = self.res["escenarios"]["continuidad"]["periodos"][0]
        self.assertAlmostEqual(p["flujo"]["dividendos"], 0.3 * p["resultados"]["utilidad_neta"])
        t = self.res["escenarios"]["tension"]["periodos"][0]
        self.assertAlmostEqual(t["balance"]["otros_activos_lp"], 145 - 3)
        self.assertAlmostEqual(t["movimientos"]["ppe"]["depreciacion_ppe"], t["resultados"]["depreciacion_amortizacion"] - 3)

    def test_etiquetas_y_naturaleza(self):
        self.assertEqual([p["periodo"] for p in self.res["escenarios"]["continuidad"]["periodos"]],
                         ["2026E", "2027E", "2028E", "2029E", "2030E"])
        self.assertIn("no es pronostico", self.res["escenarios"]["tension"]["naturaleza"])
        self.assertEqual(self.res["historico"]["periodos"][0]["naturaleza"], "hecho (filing)")
        self.assertIn("FASE 0", self.res["meta"]["aviso"])

    def test_determinista_y_serializable(self):
        a = json.dumps(modelo(), sort_keys=True, allow_nan=False)
        b = json.dumps(modelo(), sort_keys=True, allow_nan=False)
        self.assertEqual(a, b)

    def test_verificar_sobre_json_releido(self):
        releido = json.loads(json.dumps(self.res))
        self.assertEqual(fallan(mi.verificar(releido)), set())

    def test_resumen_markdown(self):
        md = mi.resumen_markdown(self.res)
        self.assertIn("| C13 |", md)
        self.assertIn("Financiamiento requerido", md)
        self.assertIn("no es pronostico", md)


class TestProyeccionAlteradaDebeFallar(unittest.TestCase):
    """Se altera el resultado ya construido y se re-verifica: los controles deben detectarlo."""

    @classmethod
    def setUpClass(cls):
        cls.res = modelo()

    def alterar(self, escenario, i, seccion, campo, delta):
        r = copy.deepcopy(self.res)
        r["escenarios"][escenario]["periodos"][i][seccion][campo] += delta
        return mi.verificar(r)

    def test_cxc_alterada(self):
        f = fallan(self.alterar("continuidad", 1, "balance", "cuentas_por_cobrar", 10))
        self.assertTrue({"C01", "C07", "C08"} <= f, f)

    def test_inventario_alterado(self):
        self.assertIn("C09", fallan(self.alterar("continuidad", 0, "balance", "inventarios", 1)))

    def test_proveedores_alterados(self):
        self.assertIn("C09", fallan(self.alterar("continuidad", 0, "balance", "proveedores", -1)))

    def test_impuestos_alterados(self):
        f = fallan(self.alterar("continuidad", 2, "resultados", "impuestos", 0.5))
        self.assertTrue({"C11", "C15"} <= f, f)

    def test_intereses_alterados(self):
        self.assertIn("C10", fallan(self.alterar("tension", 1, "resultados", "gasto_intereses", 0.01)))

    def test_fcf_alterado(self):
        self.assertIn("C12", fallan(self.alterar("continuidad", 0, "flujo", "fcf", 1)))
        self.assertIn("C12", fallan(self.alterar("continuidad", 0, "flujo", "fcf_despues_arrendamientos", 1)))

    def test_deuda_alterada(self):
        f = fallan(self.alterar("continuidad", 3, "balance", "deuda", 5))
        self.assertTrue({"C01", "C06"} <= f, f)

    def test_ppe_alterado(self):
        f = fallan(self.alterar("continuidad", 0, "balance", "ppe_neto", 5))
        self.assertTrue({"C01", "C05"} <= f, f)

    def test_utilidades_retenidas_alteradas(self):
        self.assertIn("C04", fallan(self.alterar("continuidad", 0, "balance", "utilidades_retenidas", 5)))

    def test_capital_alterado(self):
        f = fallan(self.alterar("continuidad", 0, "balance", "capital_contable", 5))
        self.assertTrue({"C01", "C03"} <= f, f)

    def test_cfo_alterado(self):
        f = fallan(self.alterar("continuidad", 0, "flujo", "cfo", 5))
        self.assertTrue({"C02", "C07", "C12"} <= f, f)

    def test_plug_oculto_detectado(self):
        """Un plug que mantiene activo = pasivo + capital (caja, activo y capital +50) lo atrapan C02 y C03."""
        r = copy.deepcopy(self.res)
        b = r["escenarios"]["continuidad"]["periodos"][2]["balance"]
        for k in ("caja", "activo_total", "capital_contable"):
            b[k] += 50
        ctl = mi.verificar(r)
        f = fallan(ctl)
        self.assertNotIn("C01", {c["id"] for c in ctl if c["estado"] == "FALLA" and "pasivo_total +" in c["prueba"]})
        self.assertTrue({"C02", "C03"} <= f, f)

    def test_revolvente_escondido(self):
        """Borrar la disposicion del flujo sin tocar saldos: C16 y la suma del CFF fallan."""
        r = copy.deepcopy(self.res)
        r["escenarios"]["tension"]["periodos"][0]["flujo"]["disposicion_revolvente"] = 0.0
        f = fallan(mi.verificar(r))
        self.assertTrue({"C02", "C06", "C16"} <= f, f)

    def test_caja_bajo_minimo(self):
        r = copy.deepcopy(self.res)
        p = r["escenarios"]["tension"]["periodos"][0]
        p["supuestos"]["caja_minima"] = 1000.0
        self.assertIn("C16", fallan(mi.verificar(r)))

    def test_ingresos_no_siguen_crecimiento(self):
        self.assertIn("C15", fallan(self.alterar("continuidad", 0, "resultados", "ingresos", 3)))

    def test_ajuste_gaap_proyeccion_alterado(self):
        r = copy.deepcopy(self.res)
        r["escenarios"]["continuidad"]["periodos"][0]["metricas"]["utilidad_neta_ajustada"] += 1
        self.assertIn("C14", fallan(mi.verificar(r)))


class TestHistoricoInconsistenteDebeFallar(unittest.TestCase):
    """Errores de transcripcion en la base: el modelo se construye pero los controles fallan."""

    def correr(self, mutar) -> set:
        b = base_sintetica()
        mutar(b)
        res = mi.construir_modelo(b, supuestos_sinteticos())
        self.assertFalse(res["resumen_controles"]["todos_ok"])
        return {c["id"] for c in res["controles"] if c["estado"] == "FALLA" and c["ambito"] == "historico"}

    def test_caja_mal_transcrita(self):
        f = self.correr(lambda b: b["historico"][1]["balance"].__setitem__("caja", 175))
        self.assertTrue({"C01", "C02", "C13"} <= f, f)

    def test_activo_total_no_cuadra(self):
        f = self.correr(lambda b: b["historico"][1]["balance"].__setitem__("activo_total", 1130))
        self.assertTrue({"C01", "C13"} <= f, f)

    def test_utilidad_neta_inconsistente(self):
        f = self.correr(lambda b: b["historico"][1]["resultados"].__setitem__("utilidad_neta", 185))
        self.assertTrue({"C07", "C13", "C15"} <= f, f)

    def test_capital_no_cuadra_con_variaciones(self):
        f = self.correr(lambda b: b["historico"][1]["movimientos_capital"].__setitem__("ori", 4))
        self.assertTrue({"C03", "C13"} <= f, f)

    def test_utilidades_retenidas_no_cuadran(self):
        f = self.correr(lambda b: b["historico"][1]["balance"].__setitem__("utilidades_retenidas", 480))
        self.assertIn("C04", f)

    def test_ppe_no_cuadra_con_nota(self):
        f = self.correr(lambda b: b["historico"][1]["movimientos_ppe"].__setitem__("adiciones", 90))
        self.assertIn("C05", f)

    def test_deuda_no_cuadra_con_nota(self):
        f = self.correr(lambda b: b["historico"][1]["movimientos_deuda"].__setitem__("emisiones", 60))
        self.assertIn("C06", f)

    def test_puente_cfo_no_cuadra(self):
        f = self.correr(lambda b: b["historico"][1]["flujo"].__setitem__("otros_operativos", 9))
        self.assertIn("C07", f)

    def test_fcf_reportado_distinto(self):
        f = self.correr(lambda b: b["historico"][1]["flujo"].__setitem__("fcf_reportado", 180))
        self.assertIn("C12", f)

    def test_ajuste_no_gaap_no_cuadra(self):
        f = self.correr(lambda b: b["historico"][1]["ajustado"].__setitem__("valor_ajustado", 175))
        self.assertIn("C14", f)

    def test_utilidad_bruta_no_cuadra(self):
        f = self.correr(lambda b: b["historico"][0]["resultados"].__setitem__("utilidad_bruta", 410))
        self.assertIn("C15", f)

    def test_cff_componentes_no_cuadran(self):
        f = self.correr(lambda b: b["historico"][1]["flujo"].__setitem__("dividendos", 55))
        self.assertIn("C02", f)

    def test_tolerancia_declarada_y_configurable(self):
        """Una diferencia de 1 unidad cabe en la tolerancia historica por defecto (2 unidades, redondeo de
        cifras publicadas) pero falla si la base declara una tolerancia mas estricta."""
        b = base_sintetica()
        b["historico"][1]["ajustado"]["valor_ajustado"] = 171
        self.assertTrue(mi.construir_modelo(b)["resumen_controles"]["todos_ok"])
        b["tolerancias"] = {"historico_abs": 0.5, "historico_rel": 0.0}
        res = mi.construir_modelo(b)
        c14 = [c for c in res["controles"] if c["id"] == "C14"][0]
        self.assertEqual((c14["estado"], c14["tolerancia"]), ("FALLA", 0.5))

    def test_partida_conciliatoria_material_se_alerta(self):
        b = base_sintetica()
        # Omitir dividendos y recompras (error tipico): el motor reproduce, pero la partida sale material.
        for k in ("dividendos", "recompras", "otros_financiamiento"):
            b["historico"][1]["flujo"].pop(k)
        b["historico"][1]["movimientos_capital"] = None
        res = mi.construir_modelo(b)
        rec = res["historico"]["reconciliacion"]["FY2025"]
        self.assertTrue(rec["alertas_materialidad"])
        c13 = [c for c in res["controles"] if c["id"] == "C13" and c["periodo"] == "FY2025"][0]
        self.assertIn("ALERTA", c13["detalle"])
        self.assertIn("flujo.dividendos", res["historico"]["periodos"][1]["ceros_por_omision"])


class TestBaseDerivadaYValidacion(unittest.TestCase):
    def test_otros_derivados_como_residuo(self):
        b = base_sintetica()
        for per in b["historico"]:
            for k in ("otros_activos_circulantes", "otros_activos_lp", "otros_pasivos_lp"):
                per["balance"].pop(k)
        res = mi.construir_modelo(b, supuestos_sinteticos())
        p = res["historico"]["periodos"][1]
        self.assertEqual(p["balance"]["otros_activos_lp"], 1123 - (168 + 50 + 130 + 85 + 523))
        self.assertEqual(p["balance"]["otros_activos_circulantes"], 0.0)
        self.assertEqual(p["balance"]["otros_pasivos_lp"], 70.0)
        self.assertTrue(p["derivados"])
        self.assertTrue(res["resumen_controles"]["todos_ok"], res["resumen_controles"]["fallas"])
        self.assertIn("INFO", estados(res["controles"], "C01", "historico", "FY2025"))

    def test_sin_movimientos_opcionales_sigue_cuadrando(self):
        b = base_sintetica()
        for per in b["historico"]:
            for k in ("movimientos_capital", "movimientos_ppe", "movimientos_deuda", "movimientos_arrendamientos",
                      "ajustado"):
                per.pop(k, None)
            per["flujo"].pop("caja_inicial", None)
        res = mi.construir_modelo(b, supuestos_sinteticos())
        self.assertTrue(res["resumen_controles"]["todos_ok"], res["resumen_controles"]["fallas"])
        self.assertEqual(estados(res["controles"], "C03", "historico", "FY2025"), ["INFO"])
        c02 = [c for c in res["controles"] if c["id"] == "C02" and c["periodo"] == "FY2024"
               and c["prueba"].startswith("caja inicial + CFO")]
        self.assertEqual(c02[0]["estado"], "NO_APLICA")
        self.assertEqual(estados(res["controles"], "C13", "historico", "FY2025"), ["OK"])

    def test_solo_historico_sin_supuestos(self):
        res = mi.construir_modelo(base_sintetica())
        self.assertEqual(res["escenarios"], {})
        self.assertTrue(res["resumen_controles"]["todos_ok"])

    def test_errores_de_base(self):
        casos = [
            (lambda b: b["historico"].pop(), "al menos 2"),
            (lambda b: b["historico"][0].pop("fuente"), "fuente"),
            (lambda b: b["historico"][1]["flujo"].__setitem__("capex", -70), "capex: debe ser >= 0"),
            (lambda b: b["historico"][1]["balance"].__setitem__("cuentas_x_cobrar", 1), "claves no reconocidas"),
            (lambda b: b["historico"][1]["resultados"].pop("impuestos"), "impuestos: falta"),
            (lambda b: b["historico"][1]["resultados"].__setitem__("ingresos", "1100"), "numero finito"),
            (lambda b: b["historico"].reverse(), "orden cronologico"),
            (lambda b: b["historico"][1]["ajustado"].pop("fuente"), "ajustado[0].fuente"),
            (lambda b: b["historico"][1]["fuentes_campos"].__setitem__("flujo.capx", "x"), "campos inexistentes"),
            (lambda b: b.__setitem__("tolerancias", {"historico_absoluta": 1}), "tolerancias.historico_absoluta"),
        ]
        for mutar, texto in casos:
            b = base_sintetica()
            mutar(b)
            with self.assertRaises(ValueError) as cm:
                mi.construir_modelo(b)
            self.assertIn(texto, str(cm.exception))

    def test_errores_de_supuestos(self):
        def con(cambio):
            s = supuestos_sinteticos()
            cambio(s)
            return s
        casos = [
            (lambda s: s["escenarios"]["continuidad"].__setitem__("margen_operatvo", 0.2), "claves no reconocidas"),
            (lambda s: s["escenarios"]["continuidad"].pop("dias_cxc"), "dias_cxc: falta"),
            (lambda s: s["escenarios"]["continuidad"].__setitem__("crecimiento_ingresos", [0.1, 0.1]), "la lista tiene 2"),
            (lambda s: s["escenarios"]["continuidad"].__setitem__("dividendos", 10), "no ambos"),
            (lambda s: s.pop("caja_minima"), "caja_minima"),
            (lambda s: s["escenarios"]["continuidad"].__setitem__("capex_ventas", -0.1), "capex_ventas debe ser >= 0"),
            (lambda s: s["escenarios"]["continuidad"].__setitem__("tasa_impuestos", 1.2), "tasa_impuestos"),
            (lambda s: s["escenarios"]["continuidad"].pop("descripcion"), "descripcion"),
            (lambda s: s.__setitem__("anos", 0), "anos"),
            (lambda s: s["escenarios"]["tension"].__setitem__("amortizacion_deuda", 500), "excede la deuda"),
        ]
        for cambio, texto in casos:
            with self.assertRaises(ValueError, msg=texto) as cm:
                mi.construir_modelo(base_sintetica(), con(cambio))
            self.assertIn(texto, str(cm.exception))


class TestDcfInverso(unittest.TestCase):
    def test_ida_y_vuelta(self):
        for g in (-0.1, 0.0, 0.07, 0.25):
            v = mi.valor_empresa_dcf(1000, g, 0.2, 0.09, 0.03, 10)["valor_empresa"]
            deuda_neta = 250.0
            precio = (v - deuda_neta) / 50
            r = mi.dcf_inverso(precio, 50, deuda_neta, 0.09, 0.03, 0.2, 10, ingresos_base=1000)
            self.assertEqual(r["estado"], "OK")
            self.assertAlmostEqual(r["crecimiento_implicito"], g, places=8)
            self.assertAlmostEqual(r["valor_por_accion_en_solucion"], precio, places=4)
            self.assertLess(abs(r["residuo"]), 1e-4)

    def test_valor_terminal_a_mano(self):
        # 1 ano, g = 0: FCF1 = 100; VT = 100 x 1.02 / 0.08 = 1275; VE = (100 + 1275) / 1.10 = 1250
        v = mi.valor_empresa_dcf(1000, 0.0, 0.1, 0.10, 0.02, 1)
        self.assertAlmostEqual(v["valor_terminal"], 1275.0)
        self.assertAlmostEqual(v["valor_empresa"], 1250.0)
        self.assertAlmostEqual(v["peso_terminal"], 1275 / 1375)

    def test_supuestos_explicitos_y_alertas(self):
        r = mi.dcf_inverso(100, 10, 0, 0.09, 0.05, 0.15, 5, ingresos_base=500, tasa_libre_riesgo=0.04)
        for k in ("wacc", "g_terminal", "margen_fcf", "anos", "ingresos_base", "deuda_neta", "definicion_fcf",
                  "valor_terminal", "descuento", "valor_empresa_objetivo"):
            self.assertIn(k, r["supuestos"])
        self.assertTrue(any("tasa libre de riesgo" in a for a in r["alertas"]))
        self.assertIn("no es pronostico", r["aviso"])

    def test_mayor_wacc_exige_mas_crecimiento(self):
        filas = mi.dcf_inverso_sensibilidad(100, 10, 0, [0.08, 0.10, 0.12], [0.2], 0.03, 10, ingresos_base=400)
        gs = [f["crecimiento_implicito"] for f in filas]
        self.assertTrue(all(f["estado"] == "OK" for f in filas))
        self.assertTrue(gs[0] < gs[1] < gs[2])

    def test_sin_solucion_en_rango(self):
        alto = mi.dcf_inverso(1e9, 1, 0, 0.09, 0.03, 0.2, 10, ingresos_base=100)
        self.assertEqual(alto["estado"], "PRECIO_SOBRE_EL_RANGO")
        self.assertIsNone(alto["crecimiento_implicito"])
        bajo = mi.dcf_inverso(0.001, 1, 0, 0.09, 0.03, 0.2, 10, ingresos_base=1e6)
        self.assertEqual(bajo["estado"], "PRECIO_BAJO_EL_RANGO")
        caja_neta = mi.dcf_inverso(1, 10, -50, 0.09, 0.03, 0.2, 10, ingresos_base=100)
        self.assertEqual(caja_neta["estado"], "SIN_SOLUCION")

    def test_entradas_invalidas(self):
        with self.assertRaises(ValueError):
            mi.dcf_inverso(100, 10, 0, 0.03, 0.03, 0.2, 10, ingresos_base=100)
        with self.assertRaises(ValueError):
            mi.dcf_inverso(100, 10, 0, 0.09, 0.03, -0.1, 10, ingresos_base=100)
        with self.assertRaises(ValueError):
            mi.dcf_inverso(100, 0, 0, 0.09, 0.03, 0.2, 10, ingresos_base=100)
        with self.assertRaises(ValueError):
            mi.dcf_inverso(100, 10, 0, 0.09, 0.03, 0.2, 0, ingresos_base=100)


class TestCliYHuellas(unittest.TestCase):
    def test_correr_escribe_resultados_y_sha256(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "base.json").write_text(json.dumps(base_sintetica()), encoding="utf-8")
            (d / "supuestos.json").write_text(json.dumps(supuestos_sinteticos()), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                codigo = mi.main(["correr", "--base", str(d / "base.json"), "--supuestos", str(d / "supuestos.json"),
                                  "--salida", str(d / "resultados.json"), "--sha256", str(d / "SHA256SUMS.txt"),
                                  "--markdown", str(d / "resumen.md")])
            self.assertEqual(codigo, 0)
            res = json.loads((d / "resultados.json").read_text(encoding="utf-8"))
            self.assertTrue(res["resumen_controles"]["todos_ok"])
            lineas = (d / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lineas), 3)
            for ln in lineas:
                h, nombre = ln.split("  ")
                self.assertEqual(h, hashlib.sha256((d / nombre).read_bytes()).hexdigest())
            self.assertTrue((d / "resumen.md").read_text(encoding="utf-8").startswith("Motor"))

    def test_correr_devuelve_1_si_falla_un_control(self):
        b = base_sintetica()
        b["historico"][1]["balance"]["caja"] = 175
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "base.json").write_text(json.dumps(b), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                codigo = mi.main(["correr", "--base", str(d / "base.json"), "--salida", str(d / "r.json")])
            self.assertEqual(codigo, 1)

    def test_cli_dcf_inverso(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            codigo = mi.main(["dcf-inverso", "--precio", "100", "--acciones", "10", "--deuda-neta", "0", "--wacc",
                              "0.09", "--g-terminal", "0.03", "--margen-fcf", "0.2", "--anos", "10",
                              "--ingresos-base", "400"])
        self.assertEqual(codigo, 0)
        self.assertEqual(json.loads(buf.getvalue())["estado"], "OK")


if __name__ == "__main__":
    unittest.main()
