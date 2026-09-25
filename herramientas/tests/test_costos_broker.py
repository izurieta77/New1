"""Pruebas de herramientas/costos_broker.py.

Varias cifras esperadas vienen de documentos ya verificados:
- B2 §3 (arena/investigacion/brokers/B2-...): temporada de 6 meses, R = 6 idas y vueltas de 20,000 MXN.
- B3 §3.2: costo por lado de IBKR Tiered y Fixed por tamano de orden.
- B4 §5: entrada con Wise de 193.84 MXN por 20,000 MXN.
"""
import unittest
from dataclasses import replace

from herramientas import costos_broker as cb


def uso_b2(**kw):
    """Temporada de B2: 6 meses, R = 6 idas y vueltas del capital completo (12 operaciones de 20k)."""
    base = dict(capital_mxn=20_000, orden_promedio_mxn=20_000, operaciones_anuales=24, meses=6,
                desviacion_sic_por_lado=0.0, retiros=0, depositos=0)
    base.update(kw)
    return cb.Uso(**base)


class TestPorOperacion(unittest.TestCase):
    def setUp(self):
        self.cat = cb.catalogo()

    def test_gbm_por_lado_5000(self):
        u = cb.Uso(desviacion_sic_por_lado=0.0)
        r = cb.costo_por_lado(self.cat["gbm_sic"], u)
        self.assertAlmostEqual(r["mxn"], 14.5, places=9)  # 5,000 x 0.25% x 1.16
        self.assertAlmostEqual(r["pct_orden"], 0.0029, places=12)

    def test_gbm_desviacion_sic_se_suma(self):
        u = cb.Uso(desviacion_sic_por_lado=0.0017)
        self.assertAlmostEqual(cb.costo_por_lado(self.cat["gbm_sic"], u)["pct_orden"], 0.0046, places=12)

    def test_ibkr_tiered_manda_el_minimo(self):
        u = cb.Uso()
        self.assertAlmostEqual(cb.comision_usd_mxn(self.cat["ibkr_tiered"], u), 0.35 * u.tipo_cambio, places=9)

    def test_ibkr_tiered_y_fixed_contra_b3(self):
        ib, fx = self.cat["ibkr_tiered"], self.cat["ibkr_fixed"]
        # B3 §3.2: Tiered ~0.32% (2k), ~0.13% (5k), ~0.07% (10k); Fixed ~0.89% (2k), ~0.36% (5k)
        casos = [(ib, 2_000, 0.0032), (ib, 5_000, 0.0013), (ib, 10_000, 0.0007),
                 (fx, 2_000, 0.0089), (fx, 5_000, 0.0036)]
        for broker, orden, esperado in casos:
            with self.subTest(broker=broker.clave, orden=orden):
                r = cb.costo_por_lado(broker, cb.Uso(orden_promedio_mxn=orden))
                self.assertAlmostEqual(r["pct_orden"], esperado, delta=0.00015)

    def test_ibkr_no_lleva_desviacion_sic(self):
        ib = self.cat["ibkr_tiered"]
        a = cb.costo_por_lado(ib, cb.Uso(desviacion_sic_por_lado=0.0))["mxn"]
        b = cb.costo_por_lado(ib, cb.Uso(desviacion_sic_por_lado=0.01))["mxn"]
        self.assertAlmostEqual(a, b, places=12)

    def test_tope_maximo(self):
        b = cb.Broker(clave="x", nombre="x", ruta="extranjero", comision_min_usd=100.0, comision_max_pct=0.01)
        self.assertAlmostEqual(cb.comision_usd_mxn(b, cb.Uso()), 50.0, places=9)  # 1% de 5,000

    def test_taf_topado(self):
        b = cb.Broker(clave="x", nombre="x", ruta="extranjero", taf_usd_por_accion_venta=1.0, taf_max_usd=9.79)
        u = cb.Uso(precio_accion_usd=1.0, tipo_cambio=10.0)  # 500 acciones
        self.assertAlmostEqual(cb.regulatorias_venta_mxn(b, u), 97.9, places=9)

    def test_ruta_invalida(self):
        with self.assertRaises(ValueError):
            cb.Broker(clave="x", nombre="x", ruta="otra")


class TestContraB2(unittest.TestCase):
    """B2 §3, R = 6: GBM 696, Actinver con mes gratis 580, Kuspit con IVA 557 (672 con mantenimiento),
    Kuspit sin IVA 480, Finamex 998."""

    def setUp(self):
        self.cat = cb.catalogo()

    def test_tabla_b2(self):
        esperados = {"gbm_sic": 696.0, "actinver_trade": 580.0, "kuspit_optimista": 480.0,
                     "kuspit_prudente": 556.8 + 114.84, "finamex": 997.6}
        u = uso_b2()
        for clave, esperado in esperados.items():
            with self.subTest(clave=clave):
                r = cb.costo_total(self.cat[clave], replace(u))
                # GBM trae rendimiento de efectivo, pero fraccion_efectivo = 0
                self.assertAlmostEqual(r["torneo"], esperado, places=6)

    def test_kuspit_exento_con_rotacion_alta(self):
        k = self.cat["kuspit_prudente"]
        # 4 operaciones de 20k al mes: 40k de un lado = 2x el portafolio > 1 -> exento
        r = cb.costo_total(k, uso_b2(operaciones_anuales=48))
        self.assertEqual(r["mantenimiento"], 0.0)
        # Con rotacion de ambos lados, R = 6 (40k al mes / 20k = 2x) tambien queda exento
        r2 = cb.costo_total(replace(k, rotacion_un_lado=False), uso_b2())
        self.assertEqual(r2["mantenimiento"], 0.0)

    def test_promocion_que_cubre_todo(self):
        a = replace(self.cat["actinver_trade"], meses_sin_comision=12)
        r = cb.costo_total(a, uso_b2())
        self.assertEqual(r["comision"], 0.0)
        self.assertEqual(r["iva"], 0.0)


class TestFlujosYTotales(unittest.TestCase):
    def setUp(self):
        self.cat = cb.catalogo(recepcion_retiro_ibkr_mxn=30 * 1.16 * cb.TC_REFERENCIA)

    def test_conversion_ibkr_minimo_2_usd(self):
        r = cb.costo_total(self.cat["ibkr_tiered"], cb.Uso())
        self.assertAlmostEqual(r["conversion_entrada"], 2 * cb.TC_REFERENCIA, places=9)
        self.assertAlmostEqual(r["conversion_salida"], 2 * cb.TC_REFERENCIA, places=9)
        self.assertEqual(r["fondeo"], 0.0)  # primer deposito del mes gratis
        self.assertEqual(r["retiro"], 0.0)  # 2 retiros gratis al mes
        self.assertAlmostEqual(r["recepcion"], 615.96, places=9)

    def test_depositos_extra_se_cobran(self):
        b = replace(self.cat["ibkr_tiered"], depositos_gratis_mes=0)
        r = cb.costo_total(b, cb.Uso(depositos=3))
        self.assertAlmostEqual(r["fondeo"], 300.0, places=9)

    def test_firstrade_entrada_wise(self):
        r = cb.costo_total(self.cat["firstrade"], cb.Uso())
        self.assertAlmostEqual(r["conversion_entrada"], 193.84, places=9)
        self.assertAlmostEqual(r["retiro"], 25 * cb.TC_REFERENCIA, places=9)

    def test_sin_bmv(self):
        with self.assertRaises(ValueError):
            cb.costo_total(self.cat["firstrade"], cb.Uso(fraccion_usd=0.8))
        filas = cb.comparar(self.cat.values(), cb.Uso(fraccion_usd=0.8))
        self.assertNotIn("firstrade", [f["broker"] for f in filas])

    def test_bmv_en_ibkr_cuesta_minimo_60(self):
        u = cb.Uso(fraccion_usd=0.0, operaciones_anuales=12, retiros=0, depositos=0)
        r = cb.costo_total(self.cat["ibkr_tiered"], u)
        self.assertAlmostEqual(r["comision"], 12 * 60.0, places=9)
        self.assertEqual(r["iva"], 0.0)

    def test_componentes_suman(self):
        u = cb.Uso(operaciones_anuales=48, fraccion_efectivo=0.25, rendimiento_dividendo_anual=0.01,
                   ganancia_realizada_anual_pct=0.15)
        for b in self.cat.values():
            with self.subTest(b=b.clave):
                r = cb.costo_total(b, u)
                torneo = (r["comision"] + r["iva"] + r["terceros"] + r["regulatorias"] + r["desviacion_sic"]
                          + r["conversion_entrada"] + r["fondeo"] + r["fijos"] + r["w8ben"]
                          + r["dividendos_en_cuenta"] + r["liquidacion"] - r["efectivo"])
                self.assertAlmostEqual(r["torneo"], torneo, places=9)
                dueno = (r["torneo"] + r["salida"] + r["dividendos_fuera"] + r["fiscal_diferencial"]
                         + r["cumplimiento"])
                self.assertAlmostEqual(r["dueno"], dueno, places=9)
                self.assertAlmostEqual(r["dueno_pct"], r["dueno"] / u.capital_mxn, places=12)

    def test_efectivo_liquidacion_dividendos_fiscal(self):
        u = cb.Uso(operaciones_anuales=48, fraccion_efectivo=0.5, rendimiento_dividendo_anual=0.01,
                   ganancia_realizada_anual_pct=0.15)
        g = cb.costo_total(self.cat["gbm_sic"], u)
        self.assertAlmostEqual(g["efectivo"], 0.031 * 0.5 * 20_000, places=9)
        self.assertAlmostEqual(g["dividendos_en_cuenta"], 0.01 * 20_000 * 0.5 * 0.37, places=9)
        self.assertEqual(g["fiscal_diferencial"], 0.0)
        i = cb.costo_total(self.cat["ibkr_tiered"], u)
        self.assertAlmostEqual(i["liquidacion"], 24 * 5_000 / 252 * 0.10, places=9)
        self.assertAlmostEqual(i["dividendos_fuera"], 0.01 * 20_000 * 0.5 * 0.09, places=9)
        e = cb.costo_total(self.cat["ibkr_tiered_etf_peor_caso"], u)
        self.assertAlmostEqual(e["fiscal_diferencial"], (0.30 - 0.10) * 0.15 * 20_000, places=9)

    def test_horizonte_escala_lo_variable(self):
        g6 = cb.costo_total(self.cat["gbm_sic"], cb.Uso(operaciones_anuales=48, meses=6))
        g12 = cb.costo_total(self.cat["gbm_sic"], cb.Uso(operaciones_anuales=48, meses=12))
        self.assertAlmostEqual(2 * g6["torneo"], g12["torneo"], places=9)
        i6 = cb.costo_total(self.cat["ibkr_tiered"], cb.Uso(operaciones_anuales=48, meses=6))
        i12 = cb.costo_total(self.cat["ibkr_tiered"], cb.Uso(operaciones_anuales=48, meses=12))
        self.assertAlmostEqual(i6["conversion_entrada"], i12["conversion_entrada"], places=9)  # fijo por flujo

    def test_monotono_en_operaciones(self):
        for b in self.cat.values():
            costos = [cb.costo_total(b, cb.Uso(operaciones_anuales=o))["torneo"] for o in (0, 12, 48, 96)]
            with self.subTest(b=b.clave):
                self.assertEqual(costos, sorted(costos))

    def test_validacion_uso(self):
        with self.assertRaises(ValueError):
            cb.Uso(capital_mxn=0)
        with self.assertRaises(ValueError):
            cb.Uso(fraccion_usd=1.5)
        with self.assertRaises(ValueError):
            cb.Uso(meses=0)


class TestEquilibrios(unittest.TestCase):
    def setUp(self):
        self.cat = cb.catalogo()

    def test_equilibrio_ibkr_contra_gbm(self):
        ib, g = self.cat["ibkr_tiered"], self.cat["gbm_sic"]
        u = cb.Uso(desviacion_sic_por_lado=0.0)
        k = cb.equilibrio_operaciones(ib, g, u, total="torneo")
        self.assertIsNotNone(k)
        self.assertLessEqual(cb.costo_total(ib, replace(u, operaciones_anuales=k))["torneo"],
                             cb.costo_total(g, replace(u, operaciones_anuales=k))["torneo"])
        if k > 0:
            self.assertGreater(cb.costo_total(ib, replace(u, operaciones_anuales=k - 1))["torneo"],
                               cb.costo_total(g, replace(u, operaciones_anuales=k - 1))["torneo"])

    def test_equilibrio_inexistente(self):
        g = self.cat["gbm_sic"]
        # Con 0 operaciones ambos cuestan 0, asi que un broker solo mas caro por operacion empata en 0
        caro = replace(g, clave="caro", comision_pct=0.01)
        self.assertEqual(cb.equilibrio_operaciones(caro, g, cb.Uso()), 0)
        # Con cuota fija y comision mayor nunca alcanza a GBM
        caro_fijo = replace(caro, cuota_mensual_mxn=100.0)
        self.assertIsNone(cb.equilibrio_operaciones(caro_fijo, g, cb.Uso(), max_ops=200))

    def test_holgura_cumplimiento(self):
        u = cb.Uso(operaciones_anuales=96)
        h = cb.holgura_cumplimiento_anual(self.cat["ibkr_tiered"], self.cat["gbm_sic"], u)
        ahorro = (cb.costo_total(self.cat["gbm_sic"], u)["dueno"]
                  - cb.costo_total(self.cat["ibkr_tiered"], u)["dueno"])
        self.assertAlmostEqual(h, ahorro, places=9)
        self.assertGreater(h, 0)

    def test_tabla_markdown(self):
        t = cb.tabla_escenarios(self.cat, cb.Uso(), "torneo")
        self.assertEqual(len(t.splitlines()), 2 + len(self.cat))
        self.assertIn("n/d", cb.tabla_escenarios(self.cat, cb.Uso(fraccion_usd=0.5), "dueno"))


if __name__ == "__main__":
    unittest.main()
