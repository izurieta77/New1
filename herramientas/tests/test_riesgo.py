import os
import tempfile
import unittest
from datetime import date

from herramientas import parametros, riesgo


class TestParametros(unittest.TestCase):
    def test_carga_desde_cualquier_cwd(self):
        previo = os.getcwd()
        try:
            with tempfile.TemporaryDirectory() as d:
                os.chdir(d)
                p = parametros.cargar_parametros(recargar=True)
                self.assertEqual(p["objetivo"]["moneda_base"], "MXN")
                self.assertEqual(parametros.obtener("kelly.fraccion_max"), 0.25)
        finally:
            os.chdir(previo)

    def test_clave_inexistente_no_se_inventa(self):
        with self.assertRaises(KeyError):
            parametros.obtener("riesgo_por_operacion.no_existe")

    def test_niveles_ordenados(self):
        niveles = [n["nivel"] for n in parametros.niveles_cortacircuitos()]
        self.assertEqual(niveles, sorted(niveles, reverse=True))


class TestSizing(unittest.TestCase):
    def test_tamano_por_stop(self):
        r = riesgo.tamano_por_stop(1_000_000, 100, 95)
        self.assertEqual(r["unidades"], 2000)
        self.assertAlmostEqual(r["riesgo_mxn"], 10_000)
        self.assertAlmostEqual(r["riesgo_pct"], 0.01)
        self.assertTrue(r["excede_concentracion_individual"])  # 20% nocional > 10%

    def test_riesgo_pedido_se_recorta_al_maximo(self):
        r = riesgo.tamano_por_stop(1_000_000, 100, 95, riesgo_pct=0.05)
        self.assertTrue(r["recortado_al_maximo"])
        self.assertAlmostEqual(r["riesgo_pct_usado"], 0.01)
        r = riesgo.tamano_por_stop(1_000_000, 100, 95, fase_prueba=True)
        self.assertEqual(r["unidades"], 1000)

    def test_corto_tipo_cambio_y_lote(self):
        r = riesgo.tamano_por_stop(1_000_000, 50, 52, tipo_cambio=17.5, lote=10)
        self.assertEqual(r["lado"], "corto")
        # 10,000 MXN / (2 USD * 17.5) = 285.7 -> 280 por lote de 10
        self.assertEqual(r["unidades"], 280)
        self.assertLessEqual(r["riesgo_mxn"], 10_000)

    def test_vol_objetivo(self):
        r = riesgo.tamano_vol_objetivo(1_000_000, 0.10, 0.20)
        self.assertAlmostEqual(r["peso"], 0.5)
        r = riesgo.tamano_vol_objetivo(1_000_000, 0.10, 0.05)
        self.assertAlmostEqual(r["peso"], 1.0)  # tope apalancamiento fase 1
        self.assertTrue(r["limitado_por_tope"])

    def test_kelly(self):
        self.assertAlmostEqual(riesgo.kelly(0.6, 1), 0.2)
        self.assertAlmostEqual(riesgo.kelly_fraccional(0.6, 1), 0.05)
        self.assertAlmostEqual(riesgo.kelly_fraccional(0.6, 1, fraccion=0.9), 0.05)  # topado a 0.25
        self.assertAlmostEqual(riesgo.kelly_fraccional(0.6, 1, fraccion=0.1), 0.02)
        self.assertEqual(riesgo.kelly_fraccional(0.4, 1), 0.0)


class TestCortacircuitos(unittest.TestCase):
    def test_niveles(self):
        self.assertIsNone(riesgo.estado_cortacircuitos([100, 105, 110])["nivel_activado"])
        e = riesgo.estado_cortacircuitos([100, 120, 115])  # -4.2%
        self.assertIsNone(e["nivel_activado"])
        self.assertAlmostEqual(riesgo.estado_cortacircuitos([100, 120, 110])["nivel_activado"], -0.08)  # -8.3%
        self.assertAlmostEqual(e["siguiente_nivel"], -0.08)
        e = riesgo.estado_cortacircuitos([100, 90])
        self.assertAlmostEqual(e["nivel_activado"], -0.08)
        self.assertIn("50%", e["accion"])
        e = riesgo.estado_cortacircuitos([(date(2026, 1, 1), 100), (date(2026, 2, 1), 84)])
        self.assertAlmostEqual(e["nivel_activado"], -0.15)
        self.assertEqual(e["fecha_pico"], date(2026, 1, 1))
        self.assertAlmostEqual(riesgo.estado_cortacircuitos([100, 80])["nivel_activado"], -0.20)
        self.assertAlmostEqual(riesgo.estado_cortacircuitos([100, 88])["nivel_activado"], -0.12)


class TestRachas(unittest.TestCase):
    def test_reduccion_restauracion_pausa(self):
        self.assertEqual(riesgo.factor_por_rachas([1, -1, -1])["factor"], 1.0)
        r = riesgo.factor_por_rachas([-1, -1, -1])
        self.assertEqual((r["factor"], r["estado"]), (0.5, "reducido"))
        self.assertEqual(riesgo.factor_por_rachas([-1, -1, -1, 1])["factor"], 0.5)
        self.assertEqual(riesgo.factor_por_rachas([-1, -1, -1, 1, 1])["factor"], 1.0)
        r = riesgo.factor_por_rachas([-1] * 5)
        self.assertEqual((r["factor"], r["estado"]), (0.0, "pausa"))
        self.assertEqual(riesgo.factor_por_rachas([-1] * 5 + [1, 1, 1])["estado"], "pausa")
        self.assertEqual(riesgo.factor_por_rachas([-1, -1, 0, -1])["estado"], "reducido")


class TestValidarOrden(unittest.TestCase):
    def portafolio(self, **extra):
        base = {"capital": 1_000_000, "fase": 1, "pnl_dia": 0, "pnl_semana": 0, "pnl_mes": 0,
                "posiciones": {"SPY": {"valor_mxn": 500_000, "clase": "etf", "tactica": False},
                               "BTC": {"valor_mxn": 40_000, "clase": "cripto", "tactica": True}}}
        base.update(extra)
        return base

    def test_orden_valida(self):
        orden = {"ticker": "AMXB", "lado": "compra", "cantidad": 1000, "precio": 15, "clase": "accion",
                 "sector": "telecom", "tactica": True, "stop": 14}
        r = riesgo.validar_orden(self.portafolio(), orden)
        self.assertTrue(r["aprobada"], r["violaciones"])

    def test_concentracion_individual(self):
        orden = {"ticker": "WALMEX", "lado": "compra", "cantidad": 2000, "precio": 60, "clase": "accion"}
        r = riesgo.validar_orden(self.portafolio(), orden)
        self.assertFalse(r["aprobada"])
        self.assertTrue(any("Accion individual" in v for v in r["violaciones"]))

    def test_cripto(self):
        orden = {"ticker": "BTC", "lado": "compra", "cantidad": 1, "precio": 20_000, "clase": "cripto", "tactica": True}
        r = riesgo.validar_orden(self.portafolio(), orden)
        self.assertTrue(any("Cripto" in v for v in r["violaciones"]))

    def test_apalancamiento(self):
        orden = {"ticker": "TLT", "lado": "compra", "cantidad": 1000, "precio": 500, "clase": "etf"}
        r = riesgo.validar_orden(self.portafolio(), orden)
        self.assertTrue(any("Exposicion bruta" in v for v in r["violaciones"]))
        r = riesgo.validar_orden(self.portafolio(fase=2), orden)  # 1.04x <= 1.3x en fase 2
        self.assertTrue(r["aprobada"], r["violaciones"])

    def test_limite_perdida_diaria_bloquea_tacticas(self):
        orden = {"ticker": "EWW", "lado": "compra", "cantidad": 100, "precio": 70, "clase": "etf", "tactica": True,
                 "stop": 65}
        r = riesgo.validar_orden(self.portafolio(pnl_dia=-25_000), orden)
        self.assertTrue(any("diaria" in v for v in r["violaciones"]))
        r = riesgo.validar_orden(self.portafolio(pnl_dia=-25_000), {**orden, "tactica": False})
        self.assertTrue(r["aprobada"], r["violaciones"])

    def test_riesgo_al_stop(self):
        orden = {"ticker": "EWW", "lado": "compra", "cantidad": 1000, "precio": 70, "clase": "etf", "stop": 50}
        r = riesgo.validar_orden(self.portafolio(), orden)
        self.assertTrue(any("Riesgo al stop" in v for v in r["violaciones"]))

    def test_reduccion_siempre_aprobada(self):
        orden = {"ticker": "BTC", "lado": "venta", "cantidad": 1, "precio": 10_000, "clase": "cripto"}
        r = riesgo.validar_orden(self.portafolio(pnl_dia=-50_000), orden)
        self.assertTrue(r["aprobada"])


if __name__ == "__main__":
    unittest.main()
