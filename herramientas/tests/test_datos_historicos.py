"""Pruebas sin red de herramientas/datos_historicos.py (fixtures sinteticas en tests/fixtures/)."""
import io
import json
import tempfile
import unittest
import zipfile
from datetime import date
from pathlib import Path
from unittest import mock

from herramientas import datos, datos_historicos as dh
from herramientas.datos import ErrorDatos

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def leer(nombre: str) -> str:
    return (FIXTURES / nombre).read_bytes().decode("utf-8")


def zip_de(nombre_csv: str, texto: str) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr(nombre_csv, texto.encode("utf-8"))
    return buf.getvalue()


def sin_red(*_a, **_k):
    raise AssertionError("La prueba intento usar la red")


class TestParserFrench(unittest.TestCase):
    def test_mensual_decimales_fin_de_mes_y_notas(self):
        texto = leer("french_factores_mini.csv")
        self.assertIn("\r\n", texto)  # los archivos reales usan CRLF
        t = dh.tabla_french(texto, "mensual")
        self.assertEqual(list(t["columnas"]), ["Mkt-RF", "SMB", "HML", "RF"])
        self.assertEqual(t["fechas"][0], date(2024, 10, 31))
        self.assertEqual(t["fechas"][-1], date(2025, 2, 28))
        self.assertEqual(len(t["fechas"]), 5)  # la seccion anual NO se mezcla
        self.assertAlmostEqual(t["columnas"]["Mkt-RF"][1], 0.0651, places=12)
        self.assertAlmostEqual(t["columnas"]["RF"][0], 0.0039, places=12)
        self.assertEqual(t["version_crsp"], "202607")
        self.assertTrue(any("ICE BofA" in n for n in t["notas"]))
        self.assertEqual(t["titulo"], "")
        self.assertEqual(t["unidad"], "decimal (porcentaje/100)")

    def test_seccion_anual(self):
        t = dh.tabla_french(leer("french_factores_mini.csv"), "anual")
        self.assertEqual(t["titulo"], "Annual Factors: January-December")
        self.assertEqual(t["fechas"], [date(2023, 12, 31), date(2024, 12, 31)])
        self.assertAlmostEqual(t["columnas"]["HML"][0], -0.1398, places=12)

    def test_diario(self):
        t = dh.tabla_french(leer("french_diario_mini.csv"), "diaria")
        self.assertEqual(t["fechas"][0], date(2026, 7, 27))
        self.assertEqual(t["fechas"][-1], date(2026, 7, 31))
        self.assertAlmostEqual(t["columnas"]["Mkt-RF"][2], -0.0152, places=12)
        with self.assertRaises(ErrorDatos):
            dh.tabla_french(leer("french_diario_mini.csv"), "mensual")

    def test_momentum_faltantes_y_titulo_en_dos_lineas(self):
        texto = leer("french_momentum_mini.csv")
        t = dh.tabla_french(texto, "mensual")
        self.assertEqual(t["columnas"]["Mom"], [0.0057, None, -0.0152, None])
        self.assertEqual(t["faltantes"], 2)
        self.assertEqual(dh.columna(t, "Mom"), [(date(1927, 1, 31), 0.0057), (date(1927, 3, 31), -0.0152)])
        a = dh.tabla_french(texto, "anual")
        self.assertEqual(a["titulo"], "Annual Factors: January-December")
        self.assertAlmostEqual(a["columnas"]["Mom"][1], 0.2643, places=12)

    def test_carteras_secciones_y_unidades(self):
        texto = leer("french_carteras_mini.csv")
        vw = dh.tabla_french(texto, "mensual")
        self.assertIn("Value Weighted", vw["titulo"])
        self.assertAlmostEqual(vw["columnas"]["BIG HiBM"][0], 0.04, places=12)
        ew = dh.tabla_french(texto, "mensual", seccion="equal weighted")
        self.assertAlmostEqual(ew["columnas"]["SMALL LoBM"][1], -0.05, places=12)
        self.assertEqual(dh.tabla_french(texto, "mensual", seccion=1)["titulo"], ew["titulo"])
        firmas = dh.tabla_french(texto, "mensual", seccion="Number of Firms")
        self.assertEqual(firmas["columnas"]["SMALL LoBM"], [1200.0, 1210.0])  # no se divide entre 100
        self.assertEqual(firmas["unidad"], "original (sin escalar)")
        with self.assertRaises(ErrorDatos):
            dh.tabla_french(texto, "mensual", seccion="no existe")

    def test_rendimiento_mercado(self):
        t = dh.tabla_french(leer("french_factores_mini.csv"), "mensual")
        mkt = dh.rendimiento_mercado_french(t)
        self.assertAlmostEqual(mkt[0][1], -0.0097 + 0.0039, places=12)

    def test_texto_sin_tablas(self):
        with self.assertRaises(ErrorDatos):
            dh.parsear_french_csv("<html>Not Found</html>")

    def test_nombre_zip(self):
        for entrada in ("F-F_Momentum_Factor", "F-F_Momentum_Factor_CSV", "F-F_Momentum_Factor_CSV.zip"):
            self.assertEqual(dh.nombre_zip_french(entrada), "F-F_Momentum_Factor_CSV.zip")


class TestFrenchCache(unittest.TestCase):
    def test_lee_del_cache_sin_red(self):
        with tempfile.TemporaryDirectory() as tmp:
            contenido = zip_de("F-F_Research_Data_Factors.csv", leer("french_factores_mini.csv"))
            (Path(tmp) / "F-F_Research_Data_Factors_CSV.zip").write_bytes(contenido)
            with mock.patch.object(dh, "_descargar_binario", sin_red):
                t = dh.french("F-F_Research_Data_Factors", "mensual", dir_cache=tmp)
            self.assertEqual(len(t["fechas"]), 5)
            self.assertEqual(t["csv"], "F-F_Research_Data_Factors.csv")
            self.assertEqual(len(t["sha256"]), 64)
            self.assertTrue(t["url"].endswith("/ftp/F-F_Research_Data_Factors_CSV.zip"))

    def test_descarga_guarda_y_valida_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            contenido = zip_de("F-F_Research_Data_Factors_daily.csv", leer("french_diario_mini.csv"))
            with mock.patch.object(dh, "_descargar_binario", return_value=contenido) as desc:
                t = dh.french("F-F_Research_Data_Factors_daily", "diaria", dir_cache=tmp)
                self.assertEqual(desc.call_count, 1)
                self.assertIn("F-F_Research_Data_Factors_daily_CSV.zip", desc.call_args[0][0])
            self.assertTrue((Path(tmp) / "F-F_Research_Data_Factors_daily_CSV.zip").exists())
            self.assertEqual(t["fechas"][-1], date(2026, 7, 31))
            with mock.patch.object(dh, "_descargar_binario", return_value=b"<html>error</html>"):
                with self.assertRaises(ErrorDatos):
                    dh.french("F-F_Momentum_Factor", "mensual", dir_cache=tmp)
            self.assertFalse((Path(tmp) / "F-F_Momentum_Factor_CSV.zip").exists())

    def test_refrescar_ignora_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            viejo = zip_de("F-F_Research_Data_Factors.csv", leer("french_factores_mini.csv"))
            (Path(tmp) / "F-F_Research_Data_Factors_CSV.zip").write_bytes(viejo)
            nuevo = zip_de("F-F_Research_Data_Factors.csv", leer("french_factores_mini.csv").replace("202607", "202608"))
            with mock.patch.object(dh, "_descargar_binario", return_value=nuevo):
                t = dh.french("F-F_Research_Data_Factors", "mensual", refrescar=True, dir_cache=tmp)
            self.assertEqual(t["version_crsp"], "202608")


class TestYahoo(unittest.TestCase):
    def test_mensual_fin_de_mes_y_mes_incompleto(self):
        h = dh.parsear_yahoo_historia(leer("yahoo_mensual_mini.json"), "1mo")
        # marzo tiene cierre nulo; septiembre-2026 esta en curso -> se descarta
        self.assertEqual(h["fechas"], [date(2026, 1, 31), date(2026, 2, 28), date(2026, 4, 30), date(2026, 5, 31),
                                       date(2026, 6, 30), date(2026, 7, 31), date(2026, 8, 31)])
        self.assertEqual(h["precios"][-1], 110.0)
        self.assertTrue(h["descartes"])
        self.assertTrue(h["usa_adjclose"])
        self.assertFalse(h["adjclose_difiere_de_close"])  # indice de precio: sin dividendos

    def test_mensual_incompleto_conservado_si_se_pide(self):
        h = dh.parsear_yahoo_historia(leer("yahoo_mensual_mini.json"), "1mo", solo_periodos_completos=False)
        self.assertEqual(h["fechas"][-1], date(2026, 9, 30))
        self.assertEqual(h["precios"][-1], 110.5)  # el ultimo punto del mes (en vivo)

    def test_mensual_robusto_a_cambio_de_horario(self):
        crudo = json.loads(leer("yahoo_mensual_mini.json"))
        crudo["chart"]["result"][0]["meta"]["gmtoffset"] = -18000  # consulta hecha en invierno
        h = dh.parsear_yahoo_historia(json.dumps(crudo), "1mo")
        self.assertEqual(h["fechas"][3], date(2026, 5, 31))  # la barra de mayo no cae en abril
        self.assertEqual(len(h["fechas"]), 7)

    def test_diario_sesion_abierta_y_adjclose(self):
        h = dh.parsear_yahoo_historia(leer("yahoo_diario_mini.json"), "1d")
        self.assertEqual(h["fechas"], [date(2026, 9, 22), date(2026, 9, 23), date(2026, 9, 24)])
        self.assertEqual(h["precios"][:2], [758.0, 763.0])
        self.assertTrue(h["adjclose_difiere_de_close"])
        completo = dh.parsear_yahoo_historia(leer("yahoo_diario_mini.json"), "1d", solo_periodos_completos=False)
        self.assertEqual(completo["fechas"][-1], date(2026, 9, 25))

    def test_granularidad_degradada_es_error(self):
        with self.assertRaises(ErrorDatos):
            dh.parsear_yahoo_historia(leer("yahoo_rango_max_3mo.json"), "1mo")

    def test_url_usa_period1_period2_y_no_range_max(self):
        capturas = []

        def falso_descargar(url, encabezados=None, **k):
            capturas.append((url, encabezados))
            return leer("yahoo_mensual_mini.json")

        with mock.patch.object(datos, "descargar", falso_descargar):
            h = dh.yahoo_historia("^GSPC", "1mo")
        url, encabezados = capturas[0]
        self.assertIn("%5EGSPC", url)
        self.assertIn("period1=-2208988800", url)
        self.assertIn("interval=1mo", url)
        self.assertNotIn("range=", url)
        self.assertEqual(encabezados, datos.UA_NAVEGADOR)
        self.assertEqual(len(h["fechas"]), 7)

    def test_rendimientos_de_precios(self):
        r = dh.rendimientos_de_precios([date(2026, 1, 31), date(2026, 2, 28), date(2026, 3, 31)], [100.0, 110.0, 99.0])
        self.assertEqual(r[0][0], date(2026, 2, 28))
        self.assertAlmostEqual(r[0][1], 0.10, places=12)
        self.assertAlmostEqual(r[1][1], -0.10, places=12)


class TestFredAlfred(unittest.TestCase):
    def test_alfred_vintage(self):
        capturas = []

        def falso_descargar(url, encabezados=None, **k):
            capturas.append(url)
            return leer("alfred_gdpc1_20081031_mini.csv")

        with mock.patch.object(datos, "descargar", falso_descargar):
            v = dh.alfred("GDPC1", "2008-10-31")
            ultimo = dh.alfred_ultimo_conocido("GDPC1", date(2008, 10, 31))
        self.assertIn("alfred.stlouisfed.org", capturas[0])
        self.assertIn("vintage_date=2008-10-31", capturas[0])
        self.assertEqual(v[-1], (date(2008, 7, 1), 11720.0))
        self.assertEqual(ultimo, (date(2008, 7, 1), 11720.0))

    def test_alfred_no_acepta_observaciones_posteriores(self):
        with mock.patch.object(datos, "descargar", return_value=leer("alfred_gdpc1_20081031_mini.csv")):
            with self.assertRaises(ErrorDatos):
                dh.alfred("GDPC1", "2008-05-01")

    def test_alfred_404_explicado(self):
        def falla(*a, **k):
            raise ErrorDatos("No se pudo descargar x: <HTTPError 404: 'Not Found'>")

        with mock.patch.object(datos, "descargar", falla):
            with self.assertRaisesRegex(ErrorDatos, "no existe vintage"):
                dh.alfred("UNRATE", "1950-01-01")

    def test_fred_delega(self):
        with mock.patch.object(datos, "descargar", return_value="observation_date,DEXMXUS\n2026-09-17,17.1829\n2026-09-18,.\n"):
            self.assertEqual(dh.fred("DEXMXUS"), [(date(2026, 9, 17), 17.1829)])


if __name__ == "__main__":
    unittest.main()
