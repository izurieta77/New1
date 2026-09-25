import itertools
import math
import random
import statistics
import unittest
from datetime import date

from herramientas import metricas as m


def racha_max(secuencia) -> int:
    maxima = actual = 0
    for gano in secuencia:
        actual = 0 if gano else actual + 1
        maxima = max(maxima, actual)
    return maxima


def enumerar(n, p_ganar):
    """Distribucion exacta de la racha perdedora maxima por enumeracion de 2^n secuencias."""
    dist = {}
    for s in itertools.product((True, False), repeat=n):
        g = sum(s)
        prob = p_ganar ** g * (1 - p_ganar) ** (n - g)
        k = racha_max(s)
        dist[k] = dist.get(k, 0.0) + prob
    return dist


class TestRendimiento(unittest.TestCase):
    def test_rendimientos_y_cagr(self):
        self.assertEqual([round(x, 12) for x in m.rendimientos([100, 110, 99])], [0.1, -0.1])
        self.assertAlmostEqual(m.cagr([100, 110, 121], periodos_por_anio=1), 0.10, places=12)
        curva = [(date(2020, 1, 1), 100.0), (date(2022, 1, 1), 121.0)]
        self.assertAlmostEqual(m.cagr(curva), 1.21 ** (365.25 / 731) - 1, places=12)

    def test_sharpe_valor_conocido(self):
        r = [0.02, 0.0, 0.02, 0.0]  # media 0.01, desv muestral sqrt(4e-4/3)
        esperado = 0.01 / math.sqrt(4e-4 / 3) * math.sqrt(252)
        self.assertAlmostEqual(m.sharpe(r), esperado, places=10)
        self.assertAlmostEqual(m.sharpe(r, periodos_por_anio=1), 0.8660254037844386, places=12)
        rf = 0.05
        rf_p = 1.05 ** (1 / 252) - 1
        self.assertAlmostEqual(m.sharpe(r, rf), (0.01 - rf_p) / math.sqrt(4e-4 / 3) * math.sqrt(252), places=10)

    def test_volatilidad_y_sortino(self):
        r = [0.01, -0.02, 0.03, -0.01]
        self.assertAlmostEqual(m.volatilidad_anualizada(r, 12), statistics.stdev(r) * math.sqrt(12), places=12)
        dd = math.sqrt((0.02 ** 2 + 0.01 ** 2) / 4)
        self.assertAlmostEqual(m.sortino(r, periodos_por_anio=12), statistics.fmean(r) / dd * math.sqrt(12), places=12)

    def test_max_drawdown_serie_sintetica(self):
        curva = [100, 120, 90, 110, 130, 65, 70, 140]
        res = m.max_drawdown(curva)
        self.assertAlmostEqual(res["valor"], -0.5)
        self.assertEqual((res["fecha_pico"], res["fecha_valle"], res["fecha_recuperacion"]), (4, 5, 7))
        self.assertEqual(res["periodos_pico_recuperacion"], 3)
        con_fechas = [(date(2024, 1, i + 1), v) for i, v in enumerate([100, 80, 90])]
        res = m.max_drawdown(con_fechas)
        self.assertAlmostEqual(res["valor"], -0.2)
        self.assertEqual(res["fecha_pico"], date(2024, 1, 1))
        self.assertIsNone(res["fecha_recuperacion"])
        self.assertEqual(m.max_drawdown([1, 2, 3])["valor"], 0.0)

    def test_calmar(self):
        curva = [100, 50, 121]
        self.assertAlmostEqual(m.calmar(curva, periodos_por_anio=1), (1.21 ** 0.5 - 1) / 0.5, places=12)


class TestOperaciones(unittest.TestCase):
    def test_hit_pf_expectancy(self):
        r = [100, -50, 200, -50, 0]
        self.assertAlmostEqual(m.hit_rate(r), 0.4)
        self.assertAlmostEqual(m.profit_factor(r), 3.0)
        self.assertAlmostEqual(m.expectancy(r), 40.0)
        self.assertEqual(m.profit_factor([1, 2]), math.inf)
        self.assertEqual(m.racha_perdedora_observada([1, -1, -1, 0, -1, -1, -1, 2]), 3)


class TestSharpeEstadistico(unittest.TestCase):
    def test_psr_normal(self):
        sr, n = 0.1, 253
        esperado = statistics.NormalDist().cdf(sr * math.sqrt(n - 1) / math.sqrt(1 + sr ** 2 / 2))
        self.assertAlmostEqual(m.psr_desde_estadisticos(sr, n, 0.0, 3.0), esperado, places=12)
        self.assertAlmostEqual(m.psr_desde_estadisticos(0.1, 100, -1, 6, 0.1), 0.5, places=12)

    def test_psr_penaliza_asimetria_negativa(self):
        normal = m.psr_desde_estadisticos(0.1, 250, 0.0, 3.0)
        colas = m.psr_desde_estadisticos(0.1, 250, -2.0, 10.0)
        self.assertLess(colas, normal)

    def test_dsr_ejemplo_publicado(self):
        # Ejemplo del paper (SR anual 2.5, V anual 0.5, N=100, T=1250, asim -3, curt 10);
        # replica publicada en marti.ai (2018): DSR ~ 0.8997.
        dsr = m.dsr_desde_estadisticos(2.5 / math.sqrt(252), 1250, 100, 0.5 / 252, -3, 10)
        self.assertAlmostEqual(dsr, 0.8997, delta=0.001)

    def test_sr0_y_un_solo_ensayo(self):
        self.assertEqual(m.sharpe_maximo_esperado(1, 0.1), 0.0)
        g = m.EULER_MASCHERONI
        nd = statistics.NormalDist()
        esperado = math.sqrt(0.04) * ((1 - g) * nd.inv_cdf(1 - 1 / 10) + g * nd.inv_cdf(1 - 1 / (10 * math.e)))
        self.assertAlmostEqual(m.sharpe_maximo_esperado(10, 0.04), esperado, places=12)
        self.assertGreater(m.sharpe_maximo_esperado(1000, 0.04), m.sharpe_maximo_esperado(10, 0.04))

    def test_dsr_desde_rendimientos(self):
        rnd = random.Random(7)
        r = [rnd.gauss(0.0008, 0.01) for _ in range(1000)]
        psr = m.sharpe_probabilistico(r)
        self.assertAlmostEqual(m.sharpe_deflactado(r, 1, 0.0), psr, places=12)
        self.assertLess(m.sharpe_deflactado(r, 50, 0.5, varianza_anualizada=True), psr)

    def test_curtosis_cruda(self):
        rnd = random.Random(1)
        x = [rnd.gauss(0, 1) for _ in range(20000)]
        self.assertAlmostEqual(m.curtosis(x), 3.0, delta=0.15)
        self.assertAlmostEqual(m.asimetria(x), 0.0, delta=0.05)


class TestPronosticos(unittest.TestCase):
    def test_brier_log(self):
        self.assertAlmostEqual(m.brier([1, 0, 0.5], [1, 0, 1]), 0.25 / 3)
        self.assertAlmostEqual(m.log_score([0.8, 0.3], [1, 0]), (math.log(0.8) + math.log(0.7)) / 2)
        self.assertAlmostEqual(m.log_score([0.5], [1]), math.log(0.5))
        self.assertTrue(math.isfinite(m.log_score([0.0], [1])))
        with self.assertRaises(ValueError):
            m.brier([1.2], [1])

    def test_tabla_calibracion(self):
        t = m.tabla_calibracion([0.05, 0.15, 0.12, 0.95, 1.0], [0, 1, 0, 1, 1])
        self.assertEqual(len(t), 10)
        self.assertEqual(t[1]["n"], 2)
        self.assertAlmostEqual(t[1]["frecuencia"], 0.5)
        self.assertAlmostEqual(t[1]["prob_media"], 0.135)
        self.assertEqual(t[9]["n"], 2)
        self.assertEqual(t[5]["n"], 0)


class TestRachas(unittest.TestCase):
    def test_casos_cerrados(self):
        self.assertAlmostEqual(m.prob_racha_perdedora(10, 1, 0.6), 1 - 0.6 ** 10, places=14)
        self.assertAlmostEqual(m.prob_racha_perdedora(5, 5, 0.6), 0.4 ** 5, places=14)
        self.assertEqual(m.prob_racha_perdedora(3, 4, 0.5), 0.0)
        self.assertEqual(m.prob_racha_perdedora(3, 0, 0.5), 1.0)

    def test_contra_enumeracion_exhaustiva(self):
        for n in (1, 4, 7, 10):
            for p in (0.3, 0.5, 0.62):
                dist = enumerar(n, p)
                for k in range(1, n + 1):
                    exacta = sum(v for kk, v in dist.items() if kk >= k)
                    self.assertAlmostEqual(m.prob_racha_perdedora(n, k, p), exacta, places=12)
                esperada = sum(k * v for k, v in dist.items())
                self.assertAlmostEqual(m.racha_esperada_max(n, p), esperada, places=10)

    def test_contra_monte_carlo(self):
        rnd = random.Random(20260925)
        n, k, p, sims = 50, 4, 0.55, 40000
        exitos = sum(1 for _ in range(sims) if racha_max([rnd.random() < p for _ in range(n)]) >= k)
        estimada = exitos / sims
        exacta = m.prob_racha_perdedora(n, k, p)
        error_std = math.sqrt(exacta * (1 - exacta) / sims)
        self.assertLess(abs(estimada - exacta), 4 * error_std)


if __name__ == "__main__":
    unittest.main()
