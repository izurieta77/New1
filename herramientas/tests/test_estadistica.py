import math
import os
import tempfile
import unittest

from herramientas import estadistica, huellas


class TestNeweyWest(unittest.TestCase):
    def test_rezago_cero_igual_a_iid(self):
        x = [0.5, -1.2, 2.0, 0.3, -0.7, 1.1, 0.9, -0.4, 0.2, 1.5]
        r = estadistica.newey_west(x, rezagos=0)
        self.assertAlmostEqual(r["t"], r["t_iid"], places=10)

    def test_implementacion_matricial(self):
        # Segunda implementacion: kernel de Bartlett completo (sin sumar por rezagos).
        x = [math.sin(i / 3.0) + 0.1 * (i % 5) for i in range(60)]
        L = 6
        r = estadistica.newey_west(x, rezagos=L)
        n = len(x)
        m = sum(x) / n
        u = [v - m for v in x]
        s = sum(u[i] * u[j] * max(0.0, 1 - abs(i - j) / (L + 1)) for i in range(n) for j in range(n))
        se2 = math.sqrt(s / n ** 2 * n / (n - 1))
        self.assertAlmostEqual(r["se"], se2, places=12)

    def test_veredicto(self):
        self.assertEqual(estadistica.veredicto((0.1, 0.5)), "apoyo")
        self.assertEqual(estadistica.veredicto((-0.5, -0.1)), "contraria")
        self.assertEqual(estadistica.veredicto((-0.1, 0.5)), "inconcluso")

    def test_bootstrap_contiene_media(self):
        x = [0.01 * ((i * 7) % 11 - 5) for i in range(120)]
        lo, hi = estadistica.ic_bootstrap_bloques(x, bloque=6, repeticiones=500)
        m = sum(x) / len(x)
        self.assertLessEqual(lo, m)
        self.assertGreaterEqual(hi, m)


class TestHuellas(unittest.TestCase):
    def test_crear_y_verificar(self):
        with tempfile.TemporaryDirectory() as d:
            a = os.path.join(d, "datos.csv")
            with open(a, "w") as f:
                f.write("x\n1\n")
            man = huellas.crear(d, [a])
            self.assertEqual(huellas.verificar(man), [])
            with open(a, "a") as f:
                f.write("2\n")
            self.assertEqual(huellas.verificar(man), ["datos.csv"])


if __name__ == "__main__":
    unittest.main()
