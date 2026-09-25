import re
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from herramientas import portafolio as pf


def fx_constante(_fecha):
    return 20.0


class TestLibro(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.ops = Path(self.dir.name) / "operaciones.csv"
        self.eq = Path(self.dir.name) / "equity.csv"

    def tearDown(self):
        self.dir.cleanup()

    def registrar_basico(self):
        pf.registrar(self.ops, "2026-01-02", "", "deposito", 1_000_000)
        pf.registrar(self.ops, "2026-01-05", "NAFTRAC", "compra", 1000, 50, "MXN", comision=100, estrategia="nucleo")
        pf.registrar(self.ops, "2026-01-06", "SPY", "compra", 10, 500, "USD", comision=1, stop=450,
                     estrategia="tendencia")
        pf.registrar(self.ops, "2026-02-01", "NAFTRAC", "venta", 400, 60, "MXN", comision=40)

    def test_registro_y_posiciones(self):
        self.registrar_basico()
        ops = pf.leer_operaciones(self.ops)
        self.assertEqual(len(ops), 4)
        libro = pf.construir_libro(ops, fx_constante)
        nat = libro.posiciones["NAFTRAC"]
        self.assertAlmostEqual(nat["cantidad"], 600)
        self.assertAlmostEqual(nat["costo_mxn"], 50_100 * 0.6)
        # venta: ingreso 24,000 - 40 = 23,960; costo 40% de 50,100 = 20,040
        self.assertAlmostEqual(libro.cerradas[0]["pnl_mxn"], 3_920)
        spy = libro.posiciones["SPY"]
        self.assertAlmostEqual(spy["costo_mxn"], 5_001 * 20)
        self.assertEqual(spy["stop"], 450.0)
        efectivo = 1_000_000 - 50_100 - 5_001 * 20 + 23_960
        self.assertAlmostEqual(libro.efectivo_mxn, efectivo)
        self.assertAlmostEqual(libro.aportaciones_mxn, 1_000_000)

    def test_no_se_permiten_cortos(self):
        pf.registrar(self.ops, "2026-01-02", "", "deposito", 1000)
        with self.assertRaises(pf.ErrorPortafolio):
            pf.registrar(self.ops, "2026-01-03", "SPY", "venta", 1, 10, "USD")
        with self.assertRaises(pf.ErrorPortafolio):
            pf.registrar(self.ops, "2026-01-03", "SPY", "compra", 1, 10, "EUR")

    def test_validacion_previa_contra_parametros(self):
        pf.registrar(self.ops, "2026-01-02", "", "deposito", 100_000)
        ops = pf.leer_operaciones(self.ops)
        orden = {"fecha": date(2026, 1, 3), "ticker": "NAFTRAC", "lado": "compra", "cantidad": 3000,
                 "precio": 50, "moneda": "MXN", "stop": None, "estrategia": "nucleo"}
        r = pf.validar_contra_libro(ops, orden, None, "etf", 1)
        self.assertTrue(any("Exposicion bruta" in v for v in r["violaciones"]))  # 150,000 / 100,000
        r = pf.validar_contra_libro(ops, {**orden, "cantidad": 1000, "stop": 45, "estrategia": "tactica"}, None, "etf")
        self.assertTrue(any("Riesgo al stop" in v for v in r["violaciones"]))  # 5,000 = 5% > 1%
        r = pf.validar_contra_libro(ops, {**orden, "cantidad": 1000, "stop": 49}, None, "etf")
        self.assertTrue(r["aprobada"], r["violaciones"])
        with self.assertRaises(pf.ErrorPortafolio):
            pf.validar_contra_libro([], orden, None)

    def test_valuacion_y_snapshot(self):
        self.registrar_basico()
        libro = pf.construir_libro(pf.leer_operaciones(self.ops), fx_constante)
        precios = {"NAFTRAC": (date(2026, 2, 2), 55.0, "MXN"), "SPY": (date(2026, 2, 2), 520.0, "USD")}
        val = pf.valuar_libro(libro, precios, fx_actual=19.0)
        self.assertAlmostEqual(val["posiciones_mxn"], 600 * 55 + 10 * 520 * 19)
        self.assertAlmostEqual(val["equity_mxn"], libro.efectivo_mxn + val["posiciones_mxn"])
        self.assertAlmostEqual(sum(f["peso"] for f in val["filas"]), val["posiciones_mxn"] / val["equity_mxn"])
        filas = pf.guardar_snapshot(self.eq, date(2026, 2, 2), val)
        self.assertEqual(len(filas), 1)
        self.assertAlmostEqual(filas[0]["indice"], 100.0)
        filas = pf.guardar_snapshot(self.eq, date(2026, 2, 2), val)  # reemplaza el mismo dia
        self.assertEqual(len(filas), 1)

    def test_indice_neutral_a_flujos(self):
        filas = [
            {"fecha": date(2026, 1, 1), "efectivo_mxn": 0, "posiciones_mxn": 100, "equity_mxn": 100, "aportaciones_netas_mxn": 100},
            {"fecha": date(2026, 1, 2), "efectivo_mxn": 0, "posiciones_mxn": 110, "equity_mxn": 110, "aportaciones_netas_mxn": 100},
            {"fecha": date(2026, 1, 3), "efectivo_mxn": 0, "posiciones_mxn": 220, "equity_mxn": 220, "aportaciones_netas_mxn": 210},
        ]
        pf.recalcular_indice(filas)
        self.assertAlmostEqual(filas[1]["indice"], 110.0)
        self.assertAlmostEqual(filas[2]["indice"], 110.0)  # el deposito de 110 no es rendimiento

    def test_reconstruir_y_reporte(self):
        pf.registrar(self.ops, "2026-01-02", "", "deposito", 100_000)
        pf.registrar(self.ops, "2026-01-02", "IVV", "compra", 10, 500, "USD", estrategia="nucleo")
        ops = pf.leer_operaciones(self.ops)
        dias = [date(2026, 1, 2) + timedelta(days=i) for i in range(40)]
        serie = [(d, 500 + i) for i, d in enumerate(dias)]
        curva = pf.reconstruir_equity(ops, {"IVV": serie}, {"IVV": "USD"}, lambda d: 10.0, hasta=dias[-1])
        self.assertEqual(len(curva), 40)
        self.assertAlmostEqual(curva[0]["equity_mxn"], 100_000)
        self.assertAlmostEqual(curva[-1]["equity_mxn"], 100_000 - 50_000 + 10 * 539 * 10)
        pf.escribir_equity(self.eq, curva)
        equity = pf.leer_equity(self.eq)
        bench = pf.serie_benchmark(dias[0], dias[-1], tasa_cetes=0.07, spx_tr=[(d, 100 + i) for i, d in enumerate(dias)],
                                   fx=[(dias[0], 20.0)])
        self.assertAlmostEqual(bench[0][1], 100.0)
        esperado = 100 * (1 + 0.5 * (101 / 100 - 1) + 0.5 * 0.07 / 360)
        self.assertAlmostEqual(bench[1][1], esperado)
        libro = pf.construir_libro(ops, lambda d: 10.0)
        texto = pf.construir_reporte(ops, equity, libro, bench, 0.07, [])
        self.assertIn("Sharpe", texto)
        self.assertIn("Cortacircuitos", texto)
        self.assertIsNone(re.search(r"\bnan\b", texto.lower()))


if __name__ == "__main__":
    unittest.main()
