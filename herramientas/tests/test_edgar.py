"""Pruebas de herramientas/edgar.py sin red (fixtures en tests/fixtures)."""
from __future__ import annotations

import json
import os
import tempfile
import time
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

from herramientas import edgar

FIX = Path(__file__).resolve().parent / "fixtures"


def cargar(nombre: str):
    return json.loads((FIX / nombre).read_text(encoding="utf-8"))


def fila(estados: dict, etiqueta: str) -> dict:
    return next(f for f in estados["filas"] if f["etiqueta"] == etiqueta)


class TestTransporteYCik(unittest.TestCase):
    def test_agente_usuario_por_defecto_y_variable(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("SEC_USER_AGENT", None)
            self.assertEqual(edgar.agente_usuario(), edgar.AGENTE_DEFECTO)
        with mock.patch.dict(os.environ, {"SEC_USER_AGENT": "Prueba contacto@ejemplo.com"}):
            self.assertEqual(edgar.agente_usuario(), "Prueba contacto@ejemplo.com")

    def test_limitador_respeta_intervalo(self):
        lim = edgar._Limitador(0.05)
        t0 = time.monotonic()
        for _ in range(3):
            lim.esperar()
        self.assertGreaterEqual(time.monotonic() - t0, 0.095)

    def test_intervalo_por_debajo_de_10_por_segundo(self):
        self.assertGreaterEqual(edgar.INTERVALO_MIN_S, 1 / edgar.MAX_SOLICITUDES_S)

    def test_normalizar_ticker(self):
        self.assertEqual(edgar.normalizar_ticker(" brk.b "), "BRK-B")

    def test_mapa_tickers(self):
        mapa = edgar.mapa_tickers(cargar("edgar_company_tickers_mini.json"))
        self.assertEqual(mapa["NVDA"]["cik"], 1045810)
        self.assertEqual(mapa["BRK-B"]["nombre"], "BERKSHIRE HATHAWAY INC")

    def test_busqueda_entidades_exige_ticker_exacto(self):
        datos = cargar("edgar_entidades_wmt.json")
        r = edgar.cik_desde_busqueda_entidades(datos, "wmt")
        self.assertEqual(r, {"cik": 104169, "nombre": "Walmart Inc."})
        self.assertIsNone(edgar.cik_desde_busqueda_entidades(datos, "WMTX"))

    def test_info_ticker_usa_respaldo_si_sec_rechaza_403(self):
        entidades = cargar("edgar_entidades_wmt.json")

        def falso_json(url, nombre, horas):
            if url == edgar.URL_TICKERS:
                raise edgar.ErrorSEC("403", 403)
            return entidades

        with mock.patch.object(edgar, "_json_con_cache", side_effect=falso_json):
            info = edgar.info_ticker("WMT")
        self.assertEqual(info["cik"], 104169)
        self.assertIn("403", info["fuente"])

    def test_info_ticker_mapa_y_cache_en_disco(self):
        tickers = cargar("edgar_company_tickers_mini.json")
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(edgar, "DIR_CACHE", Path(tmp)):
            with mock.patch.object(edgar, "_get", return_value=json.dumps(tickers).encode()) as get:
                self.assertEqual(edgar.cik_de_ticker("NVDA"), 1045810)
                self.assertEqual(edgar.cik_de_ticker("brk.b"), 1067983)   # segunda vez: del cache
                self.assertEqual(get.call_count, 1)
            self.assertTrue((Path(tmp) / "sec_company_tickers.json").exists())

    def test_ticker_inexistente(self):
        with mock.patch.object(edgar, "_json_con_cache",
                               side_effect=[cargar("edgar_company_tickers_mini.json"), {"hits": {"hits": []}}]):
            with self.assertRaises(edgar.ErrorSEC):
                edgar.info_ticker("NOEXISTE")


class TestSplitsYDeduplicacion(unittest.TestCase):
    def test_factor_split(self):
        self.assertEqual(edgar._factor_split(10.02), 10.0)
        self.assertAlmostEqual(edgar._factor_split(0.1001), 0.1)
        self.assertIsNone(edgar._factor_split(1.08))

    def test_eventos_split_y_ajuste(self):
        H = edgar.Hecho
        hechos = [
            H(date(2023, 1, 1), date(2023, 12, 31), 10e6, date(2024, 2, 15), "10-K", "a"),
            H(date(2023, 1, 1), date(2023, 12, 31), 100e6, date(2025, 2, 15), "10-K", "b"),
            H(date(2024, 1, 1), date(2024, 3, 31), 10e6, date(2024, 5, 10), "10-Q", "c"),
            H(date(2024, 1, 1), date(2024, 3, 31), 100e6, date(2025, 5, 10), "10-Q", "d"),
        ]
        eventos = edgar.eventos_split(hechos)
        self.assertEqual(len(eventos), 1)
        self.assertEqual(eventos[0]["factor"], 10.0)
        self.assertEqual(eventos[0]["limite_pre"], date(2024, 5, 10))
        upa = [H(date(2023, 1, 1), date(2023, 3, 31), 1.30, date(2023, 5, 10), "10-Q", "e")]
        self.assertAlmostEqual(edgar.ajustar_por_split(upa, eventos, "por_accion")[0].valor, 0.13)
        self.assertEqual(edgar.ajustar_por_split(upa, eventos, "flujo")[0].valor, 1.30)

    def test_deduplicar_conserva_la_presentacion_mas_reciente(self):
        H = edgar.Hecho
        d = edgar.deduplicar([H(None, date(2024, 12, 31), 1.0, date(2025, 2, 1), "10-K", "a"),
                              H(None, date(2024, 12, 31), 2.0, date(2026, 2, 1), "10-K", "b")])
        self.assertEqual(d[(None, date(2024, 12, 31))].valor, 2.0)

    def test_etiqueta_anio_fiscal(self):
        self.assertEqual(edgar.etiqueta_anio_fiscal(date(2026, 1, 25)), 2026)   # NVDA
        self.assertEqual(edgar.etiqueta_anio_fiscal(date(2022, 1, 1)), 2021)    # 52/53 semanas
        self.assertEqual(edgar.etiqueta_anio_fiscal(date(2026, 6, 30)), 2026)   # MSFT

    def test_calendario_ignora_ttm_de_10q(self):
        claves = {
            (date(2024, 1, 1), date(2024, 12, 31)): {"10-K"},
            (date(2024, 7, 1), date(2025, 6, 30)): {"10-Q"},   # ultimos doce meses en un 10-Q
            (date(2025, 1, 1), date(2025, 3, 31)): {"10-Q"},
        }
        cal = edgar.construir_calendario(claves)
        self.assertEqual([a["anio"] for a in cal], [2024, 2025])
        self.assertEqual(cal[1]["trimestres"], [(1, date(2025, 3, 31))])


class TestEstados(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        hechos = cargar("edgar_companyfacts_demo.json")
        cls.anual = edgar.extraer_estados(hechos, "anual")
        cls.trim = edgar.extraer_estados(hechos, "trimestral")
        cls.hechos = hechos

    def test_periodo_invalido(self):
        with self.assertRaises(ValueError):
            edgar.extraer_estados(self.hechos, "mensual")

    def test_anual_con_conceptos_alternativos(self):
        self.assertEqual([f["etiqueta"] for f in self.anual["filas"]], ["FY2023", "FY2024"])
        fy23, fy24 = fila(self.anual, "FY2023"), fila(self.anual, "FY2024")
        self.assertEqual(fy23["ingresos"], 400)                  # SalesRevenueNet
        self.assertEqual(fy24["ingresos"], 480)                  # Revenues
        self.assertAlmostEqual(fy24["crec_ingresos"], 0.20)
        self.assertEqual(fy24["utilidad_bruta"], 192)            # derivada: 480 - 288
        self.assertIn("derivado", fy24["origen"]["utilidad_bruta"])
        self.assertEqual(fy24["fcf"], 102)                       # 130 - 28 (capex con concepto nuevo)
        self.assertEqual(fy23["capex"], 20)                      # concepto viejo
        self.assertAlmostEqual(fy24["conversion_caja"], 102 / 96)
        self.assertAlmostEqual(fy24["sbc_ingresos"], 24 / 480)
        self.assertEqual(self.anual["moneda"], "USD")

    def test_split_ajusta_acciones_y_upa(self):
        self.assertEqual(len(self.anual["splits"]), 1)
        self.assertAlmostEqual(fila(self.anual, "FY2023")["upa_diluida"], 0.60)
        self.assertAlmostEqual(fila(self.trim, "FY2023 Q1")["upa_diluida"], 0.13)
        self.assertAlmostEqual(fila(self.trim, "FY2023 Q1")["acciones_diluidas"], 100e6)
        self.assertAlmostEqual(fila(self.anual, "FY2024")["dilucion_anual"], 0.0)

    def test_unidad_espuria_ignorada(self):
        self.assertAlmostEqual(fila(self.anual, "FY2024")["upa_diluida"], 0.96)

    def test_q4_derivado_y_flujo_acumulado(self):
        q4 = fila(self.trim, "FY2024 Q4")
        self.assertEqual(q4["ingresos"], 130)                    # 480 - 350
        self.assertEqual(q4["utilidad_neta"], 28)                # 96 - 68
        self.assertAlmostEqual(q4["upa_diluida"], 0.28)
        self.assertEqual(q4["flujo_operativo"], 35)              # 130 - 95
        self.assertAlmostEqual(q4["acciones_diluidas"], 100e6)   # 4 x anual - suma(Q1..Q3)
        self.assertIn("anual - 9M", q4["origen"]["ingresos"])
        q2 = fila(self.trim, "FY2025 Q2")
        self.assertEqual(q2["flujo_operativo"], 35)              # 75 - 40
        self.assertEqual(q2["capex"], 8)
        self.assertAlmostEqual(q2["crec_ingresos"], 0.25)
        self.assertAlmostEqual(q2["dilucion_anual"], 0.04)

    def test_ttm_y_columna_ttm_no_crea_anio_fiscal(self):
        self.assertNotIn("FY2026", [f["etiqueta"] for f in self.anual["filas"]])
        ttm = self.trim["ttm"]
        self.assertEqual(ttm["ingresos"], 530)
        self.assertEqual(ttm["utilidad_neta"], 112)
        self.assertEqual(ttm["fcf"], (35 + 35 + 40 + 35) - (8 + 8 + 8 + 8))
        self.assertAlmostEqual(ttm["crec_ingresos"], 530 / 440 - 1)
        self.assertIsNotNone(ttm["cambio_margen_operativo"])

    def test_balance_y_deuda_neta(self):
        q2 = fila(self.trim, "FY2025 Q2")
        self.assertEqual(q2["efectivo"], 80)
        self.assertEqual(q2["deuda"], 120)
        self.assertEqual(q2["deuda_neta"], 120 - 80 - 25)
        self.assertEqual(q2["capital_contable"], 330)

    def test_ignora_formas_no_validas(self):
        self.assertEqual(fila(self.trim, "FY2025 Q2")["ingresos"], 150)   # el 8-K con 999 no entra

    def test_acciones_en_circulacion(self):
        self.assertEqual(self.anual["acciones_en_circulacion"], {"valor": 103500000.0, "fecha": "2025-07-25"})

    def test_salto_de_acciones_sospechoso_se_descarta(self):
        fila_act = {"ingresos": 1.0, "acciones_diluidas": 60000e6, "origen": {}}
        edgar.calcular_metricas(fila_act, {"acciones_diluidas": 60e3})
        self.assertIsNone(fila_act["dilucion_anual"])
        self.assertIn("descartada", fila_act["origen"]["dilucion_anual"])

    def test_moneda_principal_prefiere_la_de_reporte(self):
        hechos = {"facts": {"ifrs-full": {"Revenue": {"units": {
            "MXN": [{"end": f"202{i}-12-31", "start": f"202{i}-01-01", "val": 1, "form": "20-F", "filed": "2025-04-01"}
                    for i in range(5)],
            "USD": [{"end": "2024-12-31", "start": "2024-01-01", "val": 1, "form": "20-F", "filed": "2025-04-01"}]}}}}}
        self.assertEqual(edgar.moneda_principal(hechos), "MXN")


class TestPresentaciones(unittest.TestCase):
    def setUp(self):
        self.sub = cargar("edgar_submissions_demo.json")

    def test_filtra_tipos_y_enmiendas(self):
        pres = edgar.parsear_presentaciones(self.sub, ("8-K", "10-Q", "10-K"), None)
        formas = [p["forma"] for p in pres]
        self.assertNotIn("4", formas)
        self.assertIn("8-K/A", formas)
        self.assertEqual(pres[0]["fecha"], "2025-08-10")
        sin_enmiendas = edgar.parsear_presentaciones(self.sub, ("8-K",), None, incluir_enmiendas=False)
        self.assertEqual({p["forma"] for p in sin_enmiendas}, {"8-K"})

    def test_items_alerta_y_urls(self):
        pres = edgar.parsear_presentaciones(self.sub, ("8-K",), None)
        reexpresion = next(p for p in pres if "4.02" in p["items"])
        self.assertTrue(reexpresion["alerta"])
        self.assertIn("reexpresion", reexpresion["items_texto"][0])
        resultados = next(p for p in pres if "2.02" in p["items"])
        self.assertFalse(resultados["alerta"])
        self.assertEqual(resultados["url"],
                         "https://www.sec.gov/Archives/edgar/data/1234567/000123456725000007/demo-20250730.htm")

    def test_limite_n(self):
        self.assertEqual(len(edgar.parsear_presentaciones(self.sub, ("8-K", "10-Q", "10-K", "4"), 3)), 3)

    def test_perfil(self):
        p = edgar.perfil_emisor(self.sub)
        self.assertEqual(p["sic"], "7372")
        self.assertEqual(p["cierre_fiscal_mmdd"], "1231")

    def test_verificar_vigencia(self):
        estados = {"periodo": "trimestral", "filas": [{"fin": date(2025, 3, 31)}]}
        aviso = edgar.verificar_vigencia(estados, self.sub)
        self.assertIn("2025-06-30", aviso)
        estados["filas"][0]["fin"] = date(2025, 6, 30)
        self.assertIsNone(edgar.verificar_vigencia(estados, self.sub))

    def test_form4(self):
        info = edgar.parsear_form4((FIX / "edgar_form4_demo.xml").read_text(encoding="utf-8"))
        self.assertEqual(info["propietario"], "Perez Ana")
        self.assertEqual(info["cargo"], "CFO")
        self.assertTrue(info["plan_10b5_1"])
        self.assertEqual([t["codigo"] for t in info["transacciones"]], ["S", "P"])
        self.assertAlmostEqual(info["transacciones"][0]["valor"], 50500.0)

    def test_transacciones_form4_se_detiene_con_403(self):
        with mock.patch.object(edgar, "presentaciones_json", return_value=self.sub), \
                mock.patch.object(edgar, "_get", side_effect=edgar.ErrorSEC("403", 403)) as get:
            r = edgar.transacciones_form4("DEMO")
        self.assertEqual(get.call_count, 1)
        self.assertEqual(r["n_revisados"], 0)
        self.assertEqual(r["n_solicitados"], 2)

    def test_tablas_markdown(self):
        anual = edgar.extraer_estados(cargar("edgar_companyfacts_demo.json"), "anual")
        tabla = edgar.tabla_resultados(anual["filas"])
        self.assertEqual(len(tabla), 2 + len(anual["filas"]))
        self.assertTrue(all(linea.count("|") == 16 for linea in tabla))


if __name__ == "__main__":
    unittest.main()
