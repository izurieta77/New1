"""Pruebas de herramientas/dossier.py sin red (fuentes simuladas con mock)."""
from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest import mock

from herramientas import dossier, edgar

FIX = Path(__file__).resolve().parent / "fixtures"


def serie_sintetica(n: int = 300, inicio: float = 100.0, paso: float = 0.001, fin: date = date(2026, 9, 24)):
    """Serie diaria (solo dias habiles) con crecimiento geometrico constante."""
    fechas, f = [], fin
    while len(fechas) < n:
        if f.weekday() < 5:
            fechas.append(f)
        f -= timedelta(days=1)
    fechas.reverse()
    return [(d, inicio * (1 + paso) ** i) for i, d in enumerate(fechas)]


class TestPreciosYValuacion(unittest.TestCase):
    def test_resumen_precios(self):
        serie = serie_sintetica(300, 100.0, 0.001)
        r = dossier.resumen_precios(serie, serie)
        self.assertAlmostEqual(r["rend_12m"], 1.001 ** 252 - 1, places=9)
        self.assertAlmostEqual(r["momentum_12_1"], 1.001 ** 231 - 1, places=9)
        self.assertGreater(r["dist_sma200"], 0)
        self.assertEqual(r["max_drawdown_1a"], 0.0)
        self.assertAlmostEqual(r["beta_1a"], 1.0, places=6)
        self.assertEqual(r["dist_max_52s"], 0.0)

    def test_resumen_precios_vacio(self):
        self.assertEqual(dossier.resumen_precios([]), {})

    def test_reverse_dcf_recupera_crecimiento(self):
        valor = dossier.valor_presente_fcf(100.0, 0.12, 0.09, 0.03)
        g = dossier.crecimiento_implicito(valor, 100.0, 0.09, 0.03)
        self.assertAlmostEqual(g, 0.12, places=6)

    def test_reverse_dcf_casos_no_calculables(self):
        self.assertIsNone(dossier.crecimiento_implicito(1000.0, -5.0, 0.09))
        self.assertIsNone(dossier.crecimiento_implicito(1000.0, 10.0, 0.02, 0.03))
        with self.assertRaises(ValueError):
            dossier.valor_presente_fcf(1.0, 0.1, 0.03, 0.03)

    def test_valuacion_y_monedas_distintas(self):
        estados = edgar.extraer_estados(json.loads((FIX / "edgar_companyfacts_demo.json").read_text()), "trimestral")
        val = dossier.valuacion(10.0, "USD", estados, None)
        self.assertAlmostEqual(val["capitalizacion"], 10.0 * 103.5e6)
        self.assertAlmostEqual(val["ev"], 10.0 * 103.5e6 + 120 - 80 - 25)
        self.assertAlmostEqual(val["pu"], 10.0 * 103.5e6 / 112)
        self.assertNotIn("aviso", dossier.valuacion(10.0, "USD", estados, None, date(2025, 9, 1)))
        self.assertIn("aviso", dossier.valuacion(10.0, "USD", estados, None, date(2026, 9, 25)))
        otra = dossier.valuacion(10.0, "MXN", estados, None)
        self.assertIsNone(otra.get("capitalizacion"))
        self.assertIn("distinta", otra["nota"])


class TestAlertasYPronosticos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        hechos = json.loads((FIX / "edgar_companyfacts_demo.json").read_text())
        cls.anual = edgar.extraer_estados(hechos, "anual")
        cls.trim = edgar.extraer_estados(hechos, "trimestral")

    def test_alertas(self):
        alertas = {a["alerta"]: a for a in dossier.alertas_financieras(self.anual, self.trim)}
        self.assertEqual(alertas["Dilucion > 3%/anio"]["estado"], "ACTIVA")        # 104/100 - 1 = 4%
        self.assertEqual(alertas["SBC > 10% de ingresos"]["estado"], "ok")
        self.assertEqual(alertas["Conversion de caja TTM < 0.7"]["estado"], "ok")
        self.assertEqual(alertas["Utilidad neta TTM negativa"]["estado"], "ok")
        self.assertEqual(alertas["Dilucion promedio 3 anios > 3%/anio"]["estado"], "n.d.")

    def test_alerta_conversion_y_margen(self):
        anual = {"filas": [{"etiqueta": "FY1", "conversion_caja": 0.5, "dilucion_anual": 0.0, "sbc_ingresos": 0.12}]}
        trim = {"filas": [{"etiqueta": "FY1 Q4", "cambio_margen_bruto": -0.03, "cambio_margen_operativo": -0.01}],
                "ttm": {"conversion_caja": 0.6, "cambio_margen_operativo": -0.025, "utilidad_neta": -1.0}}
        alertas = {a["alerta"]: a["estado"] for a in dossier.alertas_financieras(anual, trim)}
        self.assertEqual(alertas["Conversion de caja TTM < 0.7"], "ACTIVA")
        self.assertEqual(alertas["Conversion de caja ultimo anio < 0.7"], "ACTIVA")
        self.assertEqual(alertas["SBC > 10% de ingresos"], "ACTIVA")
        self.assertEqual(alertas["Caida de margen operativo TTM > 2 pp a/a"], "ACTIVA")
        self.assertEqual(alertas["Caida de margen bruto ultimo trimestre > 2 pp a/a"], "ACTIVA")
        self.assertEqual(alertas["Caida de margen operativo ultimo trimestre > 2 pp a/a"], "ok")
        self.assertEqual(alertas["Utilidad neta TTM negativa"], "ACTIVA")

    def test_ancla_pronostico(self):
        anc = dossier.ancla_pronostico(self.trim["filas"], "ingresos", minimo_errores=2)
        self.assertEqual(anc["trimestre"], "FY2025 Q3")
        # mismo trimestre del anio previo (120) x crecimiento a/a del ultimo (150/120)
        self.assertAlmostEqual(anc["punto"], 120 * 150 / 120)
        self.assertLessEqual(anc["p10"], anc["punto"] * 1.5)
        self.assertIsNone(dossier.ancla_pronostico([], "ingresos"))

    def test_clave_previa(self):
        self.assertEqual(dossier._clave_previa(2025, 1, 1), (2024, 4))
        self.assertEqual(dossier._clave_previa(2025, 2, 5), (2024, 1))
        self.assertEqual(dossier._clave_previa(2024, 4, -1), (2025, 1))

    def test_fecha_limite_bmv(self):
        cierre, limite = dossier.fecha_limite_bmv(date(2026, 7, 20))
        self.assertEqual(cierre, date(2026, 6, 30))            # limite del 2T26 aun no vence
        self.assertEqual(limite, date(2026, 7, 28))            # 20 dias habiles despues del 30-jun
        cierre, limite = dossier.fecha_limite_bmv(date(2026, 9, 25))
        self.assertEqual((cierre, limite), (date(2026, 9, 30), date(2026, 10, 28)))
        cierre, limite = dossier.fecha_limite_bmv(date(2027, 1, 5))
        self.assertEqual(cierre, date(2026, 12, 31))
        self.assertEqual(limite, dossier._sumar_dias_habiles(date(2026, 12, 31), 40))

    def test_proximo_reporte(self):
        pres = [{"forma": "8-K", "items": ["2.02", "9.01"], "fecha": "2026-07-29"},
                {"forma": "8-K", "items": ["8.01"], "fecha": "2026-09-02"}]
        fecha, base = dossier._proximo_reporte(pres)
        self.assertEqual(fecha, "2026-10-28")
        self.assertIn("no confirmado", base)


class TestGenerar(unittest.TestCase):
    def setUp(self):
        self.hechos = json.loads((FIX / "edgar_companyfacts_demo.json").read_text())
        self.sub = json.loads((FIX / "edgar_submissions_demo.json").read_text())
        self.serie = serie_sintetica(400, 10.0, 0.0005)

    def _parches(self):
        return [
            mock.patch.object(dossier, "descargar_precios",
                              side_effect=lambda t, *a, **k: (self.serie, {"currency": "USD", "longName": "Demo Corp"})),
            mock.patch.object(edgar, "info_ticker",
                              return_value={"ticker": "DEMO", "cik": 1234567, "nombre": "DEMO CORP", "fuente": "prueba"}),
            mock.patch.object(edgar, "hechos_compania", return_value=self.hechos),
            mock.patch.object(edgar, "presentaciones_json", return_value=self.sub),
        ]

    def test_dossier_eua_completo(self):
        parches = self._parches()
        for p in parches:
            p.start()
        try:
            md, res = dossier.generar("DEMO", date(2026, 9, 25))
        finally:
            for p in parches:
                p.stop()
        for seccion in ("## 0. Resumen automatico", "## 1. Precio y momentum", "### 3.1 Ultimos 8 trimestres",
                        "### 3.2 Ultimos 5 anios fiscales", "## 4. Valuacion de mercado y reverse DCF",
                        "## 5. Alertas automaticas", "## 6. Presentaciones recientes", "## 7. Negocio y moat",
                        "## 9. Exposicion geopolitica", "## 11. Escenarios", "## 12. Pronostico del proximo reporte",
                        "## 13. Riesgos y criterio para matar la tesis", "## 14. Tamano de posicion"):
            self.assertIn(seccion, md)
        self.assertIn("Dilucion > 3%/anio", res["alertas_activas"])
        self.assertIn("4.02", md)                                    # 8-K de reexpresion como alerta
        self.assertIn("pronosticos.py agregar", md)
        self.assertEqual(res["errores"], [])

    def test_dossier_mexicano_sin_edgar(self):
        with mock.patch.object(dossier, "descargar_precios",
                               side_effect=lambda t, *a, **k: (self.serie, {"currency": "MXN",
                                                                             "longName": "Wal-Mart de Mexico"})), \
                mock.patch.object(edgar, "estados_financieros", side_effect=AssertionError("no debe llamar EDGAR")):
            md, res = dossier.generar("WALMEX.MX", date(2026, 9, 25))
        self.assertTrue(res["es_mx"])
        self.assertIn("Emisnet", md)
        self.assertIn("bmv.com.mx", md)
        self.assertIn("walmex.mx", md)
        self.assertIn("## 5. Alertas (aplicar a mano", md)
        self.assertIn("Circular Unica de Emisoras", md)
        self.assertIn("MXN", md)

    def test_fuente_caida_no_rompe(self):
        with mock.patch.object(dossier, "descargar_precios", side_effect=RuntimeError("sin red")), \
                mock.patch.object(edgar, "info_ticker", side_effect=edgar.ErrorSEC("sin red")), \
                mock.patch.object(edgar, "presentaciones_json", side_effect=edgar.ErrorSEC("sin red")):
            md, res = dossier.generar("DEMO", date(2026, 9, 25))
        self.assertIn("## Errores de fuentes", md)
        self.assertGreaterEqual(len(res["errores"]), 2)

    def test_main_escribe_archivo(self):
        parches = self._parches()
        for p in parches:
            p.start()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                with contextlib.redirect_stdout(io.StringIO()) as salida:
                    codigo = dossier.main(["DEMO", "--fecha", "2026-09-25", "--salida-dir", tmp])
                self.assertIn("Dossier escrito en", salida.getvalue())
                ruta = Path(tmp) / "DEMO" / "dossier-2026-09-25.md"
                self.assertEqual(codigo, 0)
                self.assertTrue(ruta.exists())
        finally:
            for p in parches:
                p.stop()


if __name__ == "__main__":
    unittest.main()
