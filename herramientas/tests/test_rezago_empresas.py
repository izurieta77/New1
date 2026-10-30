"""Pruebas de herramientas/rezago_empresas.py con un árbol temporal."""
import csv, datetime as dt, os, tempfile, unittest
from herramientas import rezago_empresas as rz

CAMPOS = ["id", "fecha_resolucion"]


def escribir(p, filas, campos):
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, campos); w.writeheader(); w.writerows(filas)


class TestRezago(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(); os.makedirs(os.path.join(self.d, "empresas", "AAA"))
        os.makedirs(os.path.join(self.d, "empresas", "BBB")); os.makedirs(os.path.join(self.d, "empresas", "CCC"))
        escribir(os.path.join(self.d, "empresas", "AAA", "pronosticos.csv"), [{"id": "A1", "fecha_resolucion": "2026-10-28"}], CAMPOS)
        escribir(os.path.join(self.d, "empresas", "BBB", "pronosticos.csv"), [{"id": "B1", "fecha_resolucion": "2026-10-28"}], CAMPOS)
        escribir(os.path.join(self.d, "empresas", "BBB", "resoluciones.csv"), [{"id": "B1"}], ["id"])
        escribir(os.path.join(self.d, "empresas", "CCC", "pronosticos.csv"), [{"id": "C1", "fecha_resolucion": "2026-11-20"}], CAMPOS)

    def test_vencido_y_resuelto(self):
        p = rz.pendientes(dt.date(2026, 10, 29), 3, self.d)
        self.assertEqual([x["ticker"] for x in p], ["AAA"])
        self.assertTrue(p[0]["vencido"])

    def test_ventana(self):
        p = rz.pendientes(dt.date(2026, 11, 18), 3, self.d)
        self.assertEqual([x["ticker"] for x in p], ["AAA", "CCC"])
        self.assertFalse(p[1]["vencido"])


if __name__ == "__main__":
    unittest.main()
