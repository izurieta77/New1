import json
import re
import unittest
from datetime import date, timedelta

from herramientas import datos, tablero


class TestParsers(unittest.TestCase):
    def test_fred_ignora_faltantes(self):
        texto = "observation_date,DGS10\n2026-09-04,4.80\n2026-09-07,\n2026-09-08,.\n2026-09-09,4.83\n"
        self.assertEqual(datos.parsear_fred_csv(texto), [(date(2026, 9, 4), 4.80), (date(2026, 9, 9), 4.83)])
        with self.assertRaises(datos.ErrorDatos):
            datos.parsear_fred_csv("<html>error</html>")

    def test_yahoo_prefiere_ajustado_y_hora_local(self):
        base = 1790256600  # 2026-09-24 14:30 UTC
        crudo = {"chart": {"error": None, "result": [{
            "meta": {"currency": "USD", "gmtoffset": -14400},
            "timestamp": [base - 86400, base, base + 3600],
            "indicators": {"quote": [{"close": [10.0, 11.0, None]}],
                           "adjclose": [{"adjclose": [9.5, None, 12.0]}]}}]}}
        r = datos.parsear_yahoo_json(json.dumps(crudo))
        self.assertEqual(r["meta"]["currency"], "USD")
        # dia 1 ajustado 9.5; dia 2: ajustado nulo -> cierre 11, luego punto del mismo dia 12 (se queda el ultimo)
        self.assertEqual(r["serie"], [(date(2026, 9, 23), 9.5), (date(2026, 9, 24), 12.0)])

    def test_yahoo_error(self):
        with self.assertRaises(datos.ErrorDatos):
            datos.parsear_yahoo_json(json.dumps({"chart": {"error": {"code": "Not Found"}, "result": None}}))

    def test_valor_en_o_antes(self):
        s = [(date(2026, 1, d), float(d)) for d in (2, 5, 9)]
        self.assertEqual(datos.valor_en_o_antes(s, date(2026, 1, 6)), (date(2026, 1, 5), 5.0))
        self.assertIsNone(datos.valor_en_o_antes(s, date(2026, 1, 1)))
        self.assertEqual(datos.hace_anios(date(2024, 2, 29), 1), date(2023, 2, 28))


def serie_lineal(dias, inicio, paso, fin=date(2026, 9, 24)):
    return [(fin - timedelta(days=dias - 1 - i), inicio + paso * i) for i in range(dias)]


class TestTablero(unittest.TestCase):
    def test_resumen_precio(self):
        s = serie_lineal(400, 100.0, 1.0)
        r = tablero.resumen_serie(s, "precio", True, hoy=date(2026, 9, 25))
        self.assertEqual(r["ultimo"], 499.0)
        self.assertAlmostEqual(r["cambios"]["1s"], 499 / 492 - 1)
        self.assertAlmostEqual(r["sma200"], sum(v for _, v in s[-200:]) / 200)
        self.assertEqual(r["percentil_5a"], 100.0)
        self.assertEqual(r["rezago_dias"], 1)

    def test_resumen_tasa_en_puntos(self):
        s = serie_lineal(100, 4.0, 0.01)
        r = tablero.resumen_serie(s, "tasa", False)
        self.assertAlmostEqual(r["cambios"]["1m"], 0.30)
        self.assertIsNone(r["sma200"])

    def test_regimen(self):
        series = {
            "FRED:SP500": serie_lineal(300, 100.0, 1.0),
            "FRED:VIXCLS": serie_lineal(300, 30.0, -0.06),       # termina en 12.06 -> calma
            "FRED:BAMLH0A0HYM2": serie_lineal(400, 3.0, 0.0),    # igual a la mediana -> benigno
            "FRED:T10Y2Y": serie_lineal(400, -0.5, 0.004),       # cruza cero en los ultimos 12m
            "FRED:T10Y3M": serie_lineal(400, 1.0, 0.0),
            "YAHOO:MXN=X": serie_lineal(300, 20.0, -0.01),       # peso fuerte
        }
        tipos = {"FRED:SP500": ("precio", True), "FRED:VIXCLS": ("puntos", False),
                 "FRED:BAMLH0A0HYM2": ("tasa", False), "FRED:T10Y2Y": ("tasa", False),
                 "FRED:T10Y3M": ("tasa", False), "YAHOO:MXN=X": ("precio", True)}
        res = {k: tablero.resumen_serie(v, *tipos[k]) for k, v in series.items()}
        reg = tablero.diagnostico_regimen(series, res)
        estados = {d[0]: (d[1], d[2]) for d in reg["dimensiones"]}
        self.assertEqual(estados["Tendencia (S&P 500 vs SMA200)"], ("alcista", 1))
        self.assertEqual(estados["Volatilidad (VIX)"], ("calma", 1))
        self.assertEqual(estados["Credito (spread HY)"], ("benigno", 1))
        self.assertEqual(estados["Curva EUA (10a-2a, 10a-3m)"][1], 0)
        self.assertEqual(estados["Dolar-peso (USD/MXN)"][1], 1)
        self.assertEqual(reg["diagnostico"], "RISK-ON")
        md = tablero.construir_markdown(series, res, ["X: fallo"], reg, tablero.datetime(2026, 9, 25))
        self.assertIn("## Fuentes con error", md)
        self.assertIsNone(re.search(r"\bnan\b", md.lower()))

    def test_regimen_sin_datos(self):
        reg = tablero.diagnostico_regimen({}, {})
        self.assertEqual(reg["con_dato"], 0)
        self.assertEqual(reg["diagnostico"], "MIXTO / TRANSICION")


if __name__ == "__main__":
    unittest.main()
