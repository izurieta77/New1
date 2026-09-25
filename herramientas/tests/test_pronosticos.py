import contextlib
import csv
import io
import tempfile
import unittest
from pathlib import Path

from herramientas import pronosticos as pr


class TestBitacoraPronosticos(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.ruta = Path(self.dir.name) / "sub" / "pronosticos.csv"

    def tearDown(self):
        self.dir.cleanup()

    def test_crea_con_encabezado(self):
        pr.asegurar_archivo(self.ruta)
        with open(self.ruta, newline="", encoding="utf-8") as f:
            self.assertEqual(next(csv.reader(f)), pr.COLUMNAS)
        self.assertEqual(pr.leer(self.ruta), [])

    def test_ciclo_completo(self):
        a = pr.agregar(self.ruta, "S&P 500 > 8000 al cierre de 2026?", "0.30", "2026-12-31",
                       "Cierre FRED SP500 del 2026-12-31 > 8000", autor="claude", fecha_creacion="2026-09-25")
        b = pr.agregar(self.ruta, "USD/MXN < 18 el 2026-10-31?", "70%", "2026-10-31", "FIX Banxico < 18",
                       autor="gpt", fecha_creacion="2026-09-25")
        c = pr.agregar(self.ruta, "Banxico recorta en octubre?", 0.8, "2026-09-30", "Comunicado Banxico",
                       fecha_creacion="2026-09-25")
        self.assertEqual([a["id"], b["id"], c["id"]], ["P0001", "P0002", "P0003"])
        self.assertEqual(b["probabilidad"], "0.7000")
        self.assertEqual(len(pr.pendientes(self.ruta)), 3)
        self.assertEqual([f["id"] for f in pr.vencidos(self.ruta, hoy="2026-10-01")], ["P0003"])

        pr.resolver(self.ruta, "P0003", "si", fecha_resuelto="2026-10-01", notas="recorte 25 pb")
        pr.resolver(self.ruta, "P0002", "no", fecha_resuelto="2026-10-31")
        pr.resolver(self.ruta, "P0001", "anulada", fecha_resuelto="2027-01-02")
        with self.assertRaises(pr.ErrorBitacora):
            pr.resolver(self.ruta, "P0002", "si")
        with self.assertRaises(pr.ErrorBitacora):
            pr.resolver(self.ruta, "P9999", "si")
        self.assertEqual(pr.pendientes(self.ruta), [])

        res = pr.puntuar(self.ruta)
        g = res["global"]
        self.assertEqual(g["n"], 2)  # la anulada no cuenta
        self.assertAlmostEqual(g["brier"], ((0.8 - 1) ** 2 + (0.7 - 0) ** 2) / 2)
        self.assertEqual(set(res["por_autor"]), {"claude", "gpt"})
        self.assertAlmostEqual(res["por_autor"]["gpt"]["brier"], 0.49)
        self.assertEqual(pr.puntuar(self.ruta, autor="claude")["global"]["n"], 1)
        texto = pr.formatear_puntuacion(res)
        self.assertIn("muestra insuficiente", texto)

    def test_validaciones(self):
        with self.assertRaises(pr.ErrorBitacora):
            pr.agregar(self.ruta, "x", 1.5, "2026-12-31", "c")
        with self.assertRaises(pr.ErrorBitacora):
            pr.agregar(self.ruta, "x", 0.5, "2026-01-01", "c", fecha_creacion="2026-09-25")
        with self.assertRaises(ValueError):
            pr.agregar(self.ruta, "x", 0.5, "31/12/2026", "c")
        with self.assertRaises(pr.ErrorBitacora):
            pr.parsear_resultado("quiza")

    def test_cli(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self._cli()

    def _cli(self):
        codigo = pr.main(["--archivo", str(self.ruta), "agregar", "--pregunta", "q", "--probabilidad", "0.4",
                          "--fecha-resolucion", "2099-01-01", "--criterio", "c"])
        self.assertEqual(codigo, 0)
        self.assertEqual(pr.main(["--archivo", str(self.ruta), "resolver", "P0001", "--resultado", "0"]), 0)
        self.assertEqual(pr.main(["--archivo", str(self.ruta), "puntuar"]), 0)


if __name__ == "__main__":
    unittest.main()
