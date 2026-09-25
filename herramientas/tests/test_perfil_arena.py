import unittest
from datetime import date, timedelta

from herramientas import portafolio as pf
from herramientas import riesgo
from herramientas.parametros import cargar_parametros, niveles_cortacircuitos, parametros_efectivos


class TestPerfilArena(unittest.TestCase):
    """El libro de la cuenta arena debe usar los limites del perfil arena_agresivo."""

    def setUp(self):
        self.base = cargar_parametros()
        self.arena = parametros_efectivos("arena_agresivo")

    def test_estandar_es_el_nivel_superior(self):
        est = parametros_efectivos("estandar")
        self.assertEqual(est["cortacircuitos_drawdown"], self.base["cortacircuitos_drawdown"])
        self.assertEqual(est["perfil_activo"], "estandar")

    def test_sustituciones_del_perfil(self):
        prof = self.base["perfiles_riesgo"]["arena_agresivo"]
        niveles = [n["nivel"] for n in niveles_cortacircuitos(self.arena)]
        self.assertEqual(niveles, sorted([n["nivel"] for n in prof["cortacircuitos_drawdown"]], reverse=True))
        self.assertAlmostEqual(self.arena["riesgo_por_operacion"]["max_riesgo_pct_capital"],
                               prof["riesgo_por_operacion"])
        self.assertAlmostEqual(self.arena["concentracion"]["accion_individual_max"],
                               prof["concentracion"]["accion_individual_max"])
        # Lo que el perfil no trae se hereda del nivel superior.
        self.assertEqual(self.arena["concentracion"]["sector_max"], self.base["concentracion"]["sector_max"])
        self.assertIn("accion_pausa", self.arena["rachas"])
        self.assertIn("accion", self.arena["limites_perdida"])
        self.assertEqual(self.arena["kelly"]["fraccion_max"], prof["kelly_fraccion_max"])
        self.assertEqual(self.arena["perdida_maxima_tolerable_mxn"]["valor"], 10000)
        with self.assertRaises(KeyError):
            parametros_efectivos("no_existe")

    def test_cortacircuitos_arena_no_dispara_con_menos_de_12(self):
        curva = [(date(2026, 9, 28), 100.0), (date(2026, 10, 5), 91.5)]  # -8.5%
        est = riesgo.estado_cortacircuitos(curva, parametros_efectivos("estandar"))
        arena = riesgo.estado_cortacircuitos(curva, self.arena)
        self.assertIsNotNone(est["nivel_activado"])   # el estandar reduce en -8%
        self.assertIsNone(arena["nivel_activado"])    # la arena no hasta -12%
        self.assertAlmostEqual(arena["siguiente_nivel"], -0.12)
        curva.append((date(2026, 10, 6), 79.0))       # -21%
        self.assertAlmostEqual(riesgo.estado_cortacircuitos(curva, self.arena)["nivel_activado"], -0.20)

    def test_tope_absoluto_de_perdida(self):
        self.assertFalse(riesgo.estado_tope_perdida(19_000, 20_000, self.arena)["activado"])
        t = riesgo.estado_tope_perdida(9_990, 20_000, self.arena)
        self.assertTrue(t["activado"])
        self.assertAlmostEqual(t["margen_mxn"], -10)
        self.assertFalse(riesgo.estado_tope_perdida(9_990, 20_000, parametros_efectivos("estandar"))["aplica"])

    def test_riesgo_por_operacion_arena(self):
        # 20,000 MXN; compra de 5,000 MXN con stop a -11.6% = 580 MXN = 2.9% < 3% (arena) pero > 1% (estandar).
        ops = [{"fecha": date(2026, 9, 28), "ticker": "EFECTIVO", "lado": "deposito", "cantidad": 20_000.0,
                "precio": 1.0, "moneda": "MXN", "comision": 0.0, "stop": None, "tesis_id": "", "estrategia": "",
                "notas": ""}]
        orden = {"fecha": date(2026, 9, 28), "ticker": "SPXL", "lado": "compra", "cantidad": 1,
                 "precio": 5_000.0, "moneda": "MXN", "stop": 4_420.0, "estrategia": "tendencia"}
        arena = pf.validar_contra_libro(ops, orden, None, "etf", 1, self.arena)
        est = pf.validar_contra_libro(ops, orden, None, "etf", 1, parametros_efectivos("estandar"))
        self.assertFalse(any("Riesgo al stop" in v for v in arena["violaciones"]))
        self.assertTrue(any("Riesgo al stop" in v for v in est["violaciones"]))

    def test_reporte_muestra_perfil_y_tope(self):
        ops = [{"fecha": date(2026, 9, 28), "ticker": "EFECTIVO", "lado": "deposito", "cantidad": 20_000.0,
                "precio": 1.0, "moneda": "MXN", "comision": 0.0, "stop": None, "tesis_id": "", "estrategia": "",
                "notas": ""}]
        libro = pf.construir_libro(ops, None)
        equity = [{"fecha": date(2026, 9, 28) + timedelta(days=i), "efectivo_mxn": 20_000.0 - 100 * i,
                   "posiciones_mxn": 0.0, "equity_mxn": 20_000.0 - 100 * i, "aportaciones_netas_mxn": 20_000.0,
                   "indice": 1.0 - 0.005 * i} for i in range(3)]
        texto = pf.construir_reporte(ops, equity, libro, None, None, [], self.arena)
        self.assertIn("perfil arena_agresivo", texto)
        self.assertIn("Tope absoluto de perdida", texto)
        self.assertIn("-12%", texto)


if __name__ == "__main__":
    unittest.main()
