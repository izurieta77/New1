"""Pruebas de herramientas/geopolitica.py sin red (fixtures y .dta sintetico)."""
from __future__ import annotations

import json
import struct
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from unittest import mock

from herramientas import geopolitica as geo

FIX = Path(__file__).resolve().parent / "fixtures"


def cargar(nombre: str):
    return json.loads((FIX / nombre).read_text(encoding="utf-8"))


def construir_dta(variables: list[tuple], filas: list[tuple], version: int = 118) -> bytes:
    """.dta minimo (Stata 118 LSF). variables: [(nombre, tipo, formato, etiqueta)], tipo 'f', 'h', 'd' o ('s', n)."""
    k, n = len(variables), len(filas)
    codigos, empaques = [], []
    for _, tipo, _, _ in variables:
        if isinstance(tipo, tuple):
            codigos.append(tipo[1])
            empaques.append(("s", tipo[1]))
        else:
            codigos.append({"f": 65527, "h": 65529, "d": 65526}[tipo])
            empaques.append((tipo, None))
    datos = b""
    for fila in filas:
        for (cod, largo), valor in zip(empaques, fila):
            datos += valor.encode().ljust(largo, b"\0") if cod == "s" else struct.pack("<" + cod, valor)
    return (b"<stata_dta><header><release>" + str(version).encode() + b"</release><byteorder>LSF</byteorder>"
            + b"<K>" + struct.pack("<H", k) + b"</K><N>" + struct.pack("<Q", n) + b"</N>"
            + b"<label>" + struct.pack("<H", 0) + b"</label><timestamp>\x00</timestamp></header>"
            + b"<map>" + b"\0" * 112 + b"</map>"
            + b"<variable_types>" + struct.pack(f"<{k}H", *codigos) + b"</variable_types>"
            + b"<varnames>" + b"".join(v[0].encode().ljust(129, b"\0") for v in variables) + b"</varnames>"
            + b"<sortlist>" + b"\0" * (2 * (k + 1)) + b"</sortlist>"
            + b"<formats>" + b"".join(v[2].encode().ljust(57, b"\0") for v in variables) + b"</formats>"
            + b"<value_label_names>" + b"\0" * (129 * k) + b"</value_label_names>"
            + b"<variable_labels>" + b"".join(v[3].encode().ljust(321, b"\0") for v in variables) + b"</variable_labels>"
            + b"<characteristics></characteristics><data>" + datos + b"</data>"
            + b"<strls></strls><value_labels></value_labels></stata_dta>")


FALTANTE_FLOAT = struct.unpack("<f", b"\x00\x00\x00\x7f")[0]   # valor faltante "." de Stata en float


class TestDta(unittest.TestCase):
    def test_leer_dta_mensual(self):
        variables = [("month", "f", "%tm", "Date (year/month)"), ("GPR", "f", "%5.2fc", "Recent GPR"),
                     ("GPRC_MEX", "f", "%5.2fc", "Country GPR (Mexico)"), ("N10", "h", "%9.0g", "Articulos"),
                     ("event", ("s", 12), "%12s", "evento")]
        filas = [(798.0, 150.5, 0.2, 1200, ""), (799.0, 117.875, FALTANTE_FLOAT, 1100, "Hormuz")]
        dta = geo.leer_dta(construir_dta(variables, filas))
        self.assertEqual(dta["version"], 118)
        self.assertEqual(dta["variables"], ["month", "GPR", "GPRC_MEX", "N10", "event"])
        self.assertEqual(dta["etiquetas"]["GPRC_MEX"], "Country GPR (Mexico)")
        self.assertAlmostEqual(dta["filas"][1]["GPR"], 117.875)
        self.assertIsNone(dta["filas"][1]["GPRC_MEX"])
        self.assertEqual(dta["filas"][0]["N10"], 1200)
        self.assertEqual(dta["filas"][1]["event"], "Hormuz")
        serie = geo.serie_mensual_gpr(dta)
        self.assertEqual(serie[-1]["fecha"], date(2026, 8, 1))

    def test_fechas_stata(self):
        self.assertEqual(geo.fecha_stata(799, "%tm"), date(2026, 8, 1))
        self.assertEqual(geo.fecha_stata(0, "%td"), date(1960, 1, 1))
        self.assertEqual(geo.fecha_stata(24000, "%tdNN/DD/CCYY"), date(2025, 9, 16))
        self.assertIsNone(geo.fecha_stata(None, "%td"))
        self.assertIsNone(geo.fecha_stata(5, "%9.0g"))

    def test_rechaza_formatos_no_soportados(self):
        with self.assertRaises(geo.ErrorFuente):
            geo.leer_dta(b"\xd0\xcf\x11\xe0 esto es un xls")
        with self.assertRaises(geo.ErrorFuente):
            geo.leer_dta(construir_dta([("x", "f", "%9.0g", "")], [(1.0,)], version=115))
        completo = construir_dta([("x", "d", "%9.0g", "")], [(1.0,), (2.0,)])
        truncado = completo[:completo.index(b"<data>") + 6 + 4]     # 4 de los 16 bytes de datos
        with self.assertRaises(geo.ErrorFuente):
            geo.leer_dta(truncado)


class TestResumenGpr(unittest.TestCase):
    def test_mensual(self):
        filas = [{"fecha": date(1985 + i // 12, i % 12 + 1, 1), "GPR": 100.0 + i % 50, "GPRT": 90.0, "GPRA": 80.0,
                  "GPRC_MEX": 0.1 + (i % 10) / 100} for i in range(120)]
        filas.append({"fecha": date(1995, 1, 1), "GPR": 300.0, "GPRT": 310.0, "GPRA": 200.0, "GPRC_MEX": 0.5})
        res = geo.resumen_gpr_mensual(filas, ["MEX", "XXX"], {"GPRC_MEX": "Mexico"})
        self.assertEqual(res["fecha"], date(1995, 1, 1))
        self.assertEqual(res["series"]["GPR"]["ultimo"], 300.0)
        self.assertEqual(res["series"]["GPR"]["percentil"], 100.0)
        self.assertEqual([p["pais"] for p in res["paises"]], ["MEX"])
        with self.assertRaises(geo.ErrorFuente):
            geo.resumen_gpr_mensual([{"fecha": date(2020, 1, 1), "GPR": None}], ["MEX"])

    def test_diario(self):
        filas = [{"fecha": date(2026, 6, 1) + (date(2026, 6, 2) - date(2026, 6, 1)) * i, "GPRD": 100.0 + i,
                  "GPRD_MA7": 100.0, "GPRD_MA30": 90.0 + i / 10, "event": "Ataque" if i == 80 else ""}
                 for i in range(100)]
        res = geo.resumen_gpr_diario(filas)
        self.assertEqual(res["gprd"], 199.0)
        self.assertEqual(res["picos"][0]["gprd"], 199.0)
        self.assertEqual(res["eventos_anotados"][0]["evento"], "Ataque")
        self.assertEqual(res["percentil_ma30_5a"], 100.0)

    def test_csv_si_se_publicara(self):
        filas = geo.parsear_gpr_csv("month,GPR\n2026-08,117.9\n")
        self.assertEqual(filas[0]["GPR"], 117.9)


class TestPalabrasYProbabilidades(unittest.TestCase):
    def test_coincidencias(self):
        self.assertTrue(geo.coincide("Bank of Mexico rate decision", "Mexico"))
        self.assertFalse(geo.coincide("Kamala New Mexico", "Mexico"))
        self.assertTrue(geo.coincide("New Mexico and Mexico tariffs", "Mexico"))
        self.assertFalse(geo.coincide("Final: Federation Cup", "Fed"))
        self.assertTrue(geo.coincide("Fed's October decision", "Fed"))
        self.assertTrue(geo.coincide("Tariffs on Canada", "tariff"))
        self.assertFalse(geo.coincide("Edmonton Oilers win", "oil"))
        self.assertFalse(geo.coincide("", "oil"))

    def test_probabilidad_implicita(self):
        self.assertAlmostEqual(geo.probabilidad_implicita(0.64, 0.66, 0.60), 0.65)
        self.assertEqual(geo.probabilidad_implicita(0.10, 0.45, 0.30), 0.30)    # diferencial > 10 pp
        self.assertEqual(geo.probabilidad_implicita(None, 0.5, 0.42), 0.42)
        self.assertIsNone(geo.probabilidad_implicita(None, None, None))


class TestPolymarket(unittest.TestCase):
    def setUp(self):
        self.datos = cargar("polymarket_busqueda_mexico.json")

    def test_busqueda_filtra_ruido_cerrados_y_exclusiones(self):
        mercados = geo.polymarket_desde_busqueda(self.datos, "Mexico")
        self.assertEqual(sorted(m["id"] for m in mercados), ["1", "2", "3"])   # sin clima, cerrado ni New Mexico
        m1 = next(m for m in mercados if m["id"] == "1")
        self.assertEqual(m1["probabilidad"], 0.67)
        self.assertEqual(m1["resultado"], "Yes")
        self.assertEqual(m1["url"], "https://polymarket.com/event/bank-of-mexico-decision-in-november")
        self.assertEqual(m1["cierre"], "2026-11-05")

    def test_filtrar_mercados(self):
        mercados = geo.polymarket_desde_busqueda(self.datos, "Mexico")
        filtrados = geo.filtrar_mercados(mercados, 10000, 6)
        self.assertEqual([m["id"] for m in filtrados], ["1", "2"])            # la cola de 0.4% se descarta
        self.assertEqual(len(geo.filtrar_mercados(mercados, 10000, 6, max_por_evento=1)), 1)
        bajos = geo.filtrar_mercados(mercados, 1e9, 6)
        self.assertTrue(all(m["volumen_bajo"] for m in bajos))
        self.assertFalse(any("volumen_bajo" in m for m in mercados))           # no muta la entrada

    def test_mercado_sin_precio(self):
        self.assertIsNone(geo.mercado_polymarket({"outcomes": "[]", "outcomePrices": "[]"}))


class TestKalshi(unittest.TestCase):
    def test_series_relevantes(self):
        series = cargar("kalshi_series_mini.json")["series"]
        rel = geo.series_relevantes(series, "Mexico", 5)
        self.assertEqual([s["ticker"] for s in rel], ["KXCBDECISIONMEXICO", "KXTARIFFSMEX"])

    def test_eventos(self):
        mercados = geo.kalshi_desde_eventos(cargar("kalshi_eventos_banxico.json"))
        self.assertEqual(mercados[0]["evento"], "Bank of Mexico rate decision in November")   # cierra antes
        por_id = {m["id"]: m for m in mercados}
        self.assertAlmostEqual(por_id["KXCBDECISIONMEXICO-26NOV05-H0"]["probabilidad"], 0.645)
        self.assertAlmostEqual(por_id["KXCBDECISIONMEXICO-26NOV05-C25"]["probabilidad"], 0.30)
        self.assertNotIn("KXCBDECISIONMEXICO-26NOV05-X", por_id)                               # no activo
        self.assertEqual(por_id["KXCBDECISIONMEXICO-26NOV05-H0"]["cierre"], "2026-11-05")

    def test_centavos_api_anterior(self):
        m = geo.mercado_kalshi({"status": "active", "yes_bid": 40, "yes_ask": 44, "last_price": 41,
                                "volume": 100, "ticker": "T"}, {"title": "Evento"})
        self.assertAlmostEqual(m["probabilidad"], 0.42)

    def test_busqueda_v1(self):
        mercados = geo.kalshi_desde_busqueda_v1(cargar("kalshi_busqueda_v1_fed.json"), "Fed",
                                                datetime(2026, 9, 25, tzinfo=timezone.utc))
        self.assertEqual([m["id"] for m in mercados], ["KXFEDDECISION-26OCT-H25"])
        self.assertAlmostEqual(mercados[0]["probabilidad"], 0.675)


class TestGenerar(unittest.TestCase):
    def _router(self, url, **kw):
        if "public-search" in url:
            return cargar("polymarket_busqueda_mexico.json")
        if "/series?" in url:
            return cargar("kalshi_series_mini.json")
        if "/events?" in url:
            return cargar("kalshi_eventos_banxico.json")
        if "v1/search" in url:
            return {"current_page": []}
        raise geo.ErrorFuente(f"URL inesperada {url}")

    def test_generar_completo_sin_red(self):
        dta = geo.leer_dta(construir_dta(
            [("month", "f", "%tm", "Date"), ("GPR", "f", "%5.2fc", "GPR"), ("GPRT", "f", "%5.2fc", "T"),
             ("GPRA", "f", "%5.2fc", "A"), ("GPRC_MEX", "f", "%5.2fc", "Mexico")],
            [(float(m), 100.0 + m % 7, 100.0, 100.0, 0.2) for m in range(300, 800)]))
        with mock.patch.object(geo, "descargar_gpr", return_value={"mensual": {"formato": "dta", **dta}}), \
                mock.patch.object(geo, "_get_json", side_effect=self._router), \
                mock.patch.object(geo.time, "sleep"):
            md, datos = geo.generar(["Mexico"], ["MEX"], volumen_min=1000, cache_horas=None, fecha=date(2026, 9, 25))
        self.assertIn("# Monitor geopolitico 2026-09-25", md)
        self.assertIn("| MEX |", md)
        self.assertIn("No change in Bank of Mexico", md)
        self.assertIn("Bank of Mexico rate decision in November - Maintain current rate", md)
        self.assertIn("## 5. Fuentes primarias para revisar", md)
        self.assertEqual(datos["gpr"]["mensual"]["fecha"], date(2026, 8, 1))

    def test_fuentes_caidas_no_rompen(self):
        with mock.patch.object(geo, "_get", side_effect=geo.ErrorFuente("sin red")), \
                mock.patch.object(geo.time, "sleep"):
            md, datos = geo.generar(["Fed"], ["MEX"], cache_horas=None, fecha=date(2026, 9, 25))
        self.assertIn("GPR no disponible", md)
        self.assertIn("## 6. Estado de las fuentes", md)
        self.assertTrue(any("sin red" in r for r in datos["registro"]))
        self.assertTrue(any("Kalshi" in r for r in datos["registro"]))


if __name__ == "__main__":
    unittest.main()
