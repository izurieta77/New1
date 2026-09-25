import csv
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from herramientas import portafolio as pf
from herramientas import supervision as sv
from herramientas.parametros import parametros_efectivos


def fx(_desde):
    return lambda _f: 18.0


class TestSupervision(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.b = Path(self.tmp.name)
        (self.b / "real").mkdir()
        self.params = parametros_efectivos("arena_agresivo")
        self.ahora = datetime(2026, 9, 29, 16, 0, tzinfo=timezone.utc)  # martes

    def tearDown(self):
        self.tmp.cleanup()

    def libro_papel(self, stop=70.0):
        ops = self.b / "operaciones.csv"
        pf.registrar(ops, "2026-09-28", "", "deposito", 20_000)
        pf.registrar(ops, "2026-09-28", "SPYM", "compra", 7, 80.0, "USD", comision=29, stop=stop)
        pf.registrar(ops, "2026-09-28", "SPXL", "compra", 1, 290.0, "USD", comision=15)

    def precios(self, spym, spxl):
        return lambda _t: ({"SPYM": (date(2026, 9, 29), spym, "USD"), "SPXL": (date(2026, 9, 29), spxl, "USD")}, [])

    def test_sin_libros_solo_archivos(self):
        salida = sv.supervisar(self.ahora, self.params, None, None, None, None, None, self.b)
        self.assertTrue(any("sin bitacora/estado-rutinas.md" in t for _, t in salida))

    def test_stop_tocado_es_alerta(self):
        self.libro_papel(stop=78.0)
        salida = sv.supervisar(self.ahora, self.params, self.precios(77.0, 290.0), None, None, 18.0, fx, self.b)
        self.assertIn((sv.ALERTA, "papel: SPYM en 77.00 tocó su stop 78.00"), salida)

    def test_tope_absoluto_y_cortacircuitos(self):
        self.libro_papel()
        # Posiciones de ~10,080 + 5,220 MXN; con precios a la mitad se pierden ~7,650 MXN (margen < 20% del tope).
        salida = sv.supervisar(self.ahora, self.params, self.precios(40.0, 145.0), None, None, 18.0, fx, self.b)
        tope = [x for x in salida if "tope -10,000" in x[1]][0]
        pnl = float(tope[1].split("P&L ")[1].split(" MXN")[0].replace(",", ""))
        margen = float(tope[1].split("margen ")[1].rstrip(")").replace(",", ""))
        self.assertLess(pnl, -7000)
        self.assertAlmostEqual(margen, pnl + 10_000, delta=1)
        self.assertEqual(tope[0], sv.AVISO if margen < 2_000 else sv.OK)
        # Curva de equity: 20,000 el 28-sep; hoy ~12,350 -> -38%: cortacircuitos activado.
        pf.escribir_equity(self.b / "equity.csv", [{"fecha": date(2026, 9, 28), "efectivo_mxn": 4_700.0,
                                                  "posiciones_mxn": 15_300.0, "equity_mxn": 20_000.0,
                                                  "aportaciones_netas_mxn": 20_000.0, "indice": 1.0}])
        salida = sv.supervisar(self.ahora, self.params, self.precios(40.0, 145.0), None, None, 18.0, fx, self.b)
        cc = [x for x in salida if "drawdown" in x[1]][0]
        self.assertEqual(cc[0], sv.ALERTA)
        self.assertIn("ACTIVADO -35%", cc[1])

    def test_libro_binance_con_su_tope(self):
        (self.b / "real-binance").mkdir()
        ops = self.b / "real-binance" / "operaciones.csv"
        pf.registrar(ops, "2026-09-28", "", "deposito", 10_000)
        pf.registrar(ops, "2026-09-28", "BTC-USD", "compra", 0.08, 100_000.0, "USD", comision=0)  # FX 1: 8,000 MXN
        precios = lambda _t: ({"BTC-USD": (date(2026, 9, 29), 60_000.0, "USD")}, [])  # noqa: E731
        cripto = parametros_efectivos("cripto_binance")
        salida = sv.supervisar(self.ahora, self.params, precios, None, None, 1.0, lambda _d: (lambda _f: 1.0),
                               self.b, params_cripto=cripto)
        tope = [x for x in salida if x[1].startswith("real-binance: P&L")][0]
        self.assertIn("tope -5,000", tope[1])
        # 0.08 x 60,000 = 4,800 + 2,000 de efectivo = 6,800: P&L -3,200, margen 1,800 > 20% del tope (1,000).
        self.assertEqual(tope[0], sv.OK)

    def test_filtro_apalancados(self):
        serie_ok = lambda _t: [(date(2026, 1, 1) + timedelta(days=i), 100.0 + i) for i in range(250)]  # noqa: E731
        serie_mal = lambda _t: [(date(2026, 1, 1) + timedelta(days=i), 400.0 - i) for i in range(250)]  # noqa: E731
        self.assertEqual(sv.revisar_filtro_apalancados(["SPXL", "SPYM"], serie_ok, 15.0)[0][0], sv.OK)
        self.assertEqual(sv.revisar_filtro_apalancados(["SPXL"], serie_ok, 26.0)[0][0], sv.ALERTA)
        self.assertEqual(sv.revisar_filtro_apalancados(["SPXL.MX"], serie_mal, 15.0)[0][0], sv.ALERTA)
        self.assertEqual(sv.revisar_filtro_apalancados(["SPYM"], serie_ok, 15.0), [])

    def test_pendientes_latidos_y_abiertos(self):
        with open(self.b / "ordenes-pendientes.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "ticker", "lado", "fecha_ejecucion", "estado"])
            w.writerow(["O1", "SPYM", "compra", "2026-09-28", "pendiente"])
            w.writerow(["O2", "SPXL", "compra", "2026-09-30", "pendiente"])
            w.writerow(["O3", "QQQM", "compra", "2026-09-28", "ejecutada"])
        pend = sv.revisar_pendientes(self.b / "ordenes-pendientes.csv", self.ahora.date())
        self.assertEqual([n for n, _ in pend], [sv.AVISO])
        with open(self.b / "ordenes-pendientes.csv", "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["O4", "SPYM", "compra", "2026-09-28", "en_espera"])
        pend = sv.revisar_pendientes(self.b / "ordenes-pendientes.csv", self.ahora.date())
        self.assertEqual([n for n, _ in pend], [sv.AVISO, sv.AVISO])
        self.assertIn("orden en espera: O4", pend[1][1])
        (self.b / "estado-rutinas.md").write_text("# Estado\n\n2026-09-27 12:55 UTC · pre-apertura · OK · abc · x\n",
                                                   encoding="utf-8")
        self.assertEqual(sv.revisar_latidos(self.b / "estado-rutinas.md", self.ahora)[0][0], sv.AVISO)  # 51 h
        (self.b / "bloqueos.md").write_text("| a | Estado |\n|---|---|\n| x | abierto |\n| y | cerrado |\n",
                                            encoding="utf-8")
        self.assertEqual(sv.contar_abiertos(self.b / "bloqueos.md"), 1)


if __name__ == "__main__":
    unittest.main()
