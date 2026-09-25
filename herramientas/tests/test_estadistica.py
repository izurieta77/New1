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


class TestPesosYContribuciones(unittest.TestCase):
    """Errores de razonamiento del examen S6 (2026-09-25): peso de gamma_6, kernel y benchmark fijo."""

    def test_pesos_bartlett(self):
        w = estadistica.pesos_bartlett(6)
        self.assertEqual(len(w), 7)
        self.assertAlmostEqual(w[0], 1.0)
        self.assertAlmostEqual(w[1], 6 / 7)
        self.assertAlmostEqual(w[6], 1 / 7)  # 1 - 6/7: el rezago 6 pesa 1/7, no 1
        for L in range(0, 25):
            self.assertAlmostEqual(sum(estadistica.pesos_bartlett(L)[1:]), L / 2)
        self.assertEqual(estadistica.pesos_bartlett(0), [1.0])
        with self.assertRaises(ValueError):
            estadistica.pesos_bartlett(-1)

    def test_contribuciones_coinciden_con_newey_west(self):
        x = [math.sin(i / 3.0) + 0.1 * (i % 5) - 0.02 * i for i in range(80)]
        for L in (0, 1, 6, 12):
            r = estadistica.newey_west(x, rezagos=L)
            d = estadistica.contribuciones_nw(x, rezagos=L)
            self.assertAlmostEqual(sum(d["contribuciones"]), d["S"], places=12)
            self.assertAlmostEqual(d["se"], r["se"], places=12)
            self.assertAlmostEqual(d["t"], r["t"], places=10)
            if L:
                g = d["gammas"]
                self.assertAlmostEqual(d["contribuciones"][L], 2 * g[L] / (L + 1), places=14)

    def test_bartlett_semidefinido_uniforme_no(self):
        # NW (1986/1987), Teorema 1: S_Bartlett = e'Pe/(L+1) >= 0, con P Toeplitz de gammas.
        x = [((i * 37) % 17 - 8) / 5.0 + (-1) ** i * 0.7 for i in range(50)]
        for L in (1, 3, 6, 20, 49):
            d = estadistica.contribuciones_nw(x, rezagos=L)
            g = d["gammas"]
            ePe = sum(g[abs(i - j)] for i in range(L + 1) for j in range(L + 1))
            self.assertAlmostEqual(d["S"], ePe / (L + 1), places=10)
            self.assertGreaterEqual(d["S"], -1e-12)
        # Serie alternante: gamma_1 muy negativo. Uniforme con L=1 da S < 0; Bartlett no.
        alt = [(-1) ** i for i in range(10)]
        self.assertLess(estadistica.contribuciones_nw(alt, 1, kernel="uniforme")["S"], 0)
        self.assertGreaterEqual(estadistica.contribuciones_nw(alt, 1)["S"], 0)
        # Con datos centrados, gamma_0 + 2*suma de todas las gammas = (suma u)^2/n = 0.
        u = estadistica.contribuciones_nw(x, len(x) - 1, kernel="uniforme")
        self.assertAlmostEqual(u["S"], 0.0, places=10)
        with self.assertRaises(ValueError):
            estadistica.contribuciones_nw(x, 2, kernel="parzen")

    def test_se_diferencia_y_benchmark_fijo(self):
        a, b = 0.043, 0.040
        self.assertAlmostEqual(estadistica.se_diferencia(a, b, 0.0), math.hypot(a, b))
        self.assertGreater(estadistica.se_diferencia(a, b, 0.0), a)  # b independiente: fijo subestima
        umbral = b / (2 * a)
        self.assertAlmostEqual(estadistica.se_diferencia(a, b, umbral), a, places=12)
        self.assertLess(estadistica.se_diferencia(a, b, 0.75), a)  # corr alta: fijo sobrestima
        self.assertAlmostEqual(estadistica.se_diferencia(a, a, 1.0), 0.0)
        with self.assertRaises(ValueError):
            estadistica.se_diferencia(a, b, 1.5)


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
