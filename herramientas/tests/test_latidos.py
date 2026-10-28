"""Pruebas de herramientas/latidos.py (funciones puras; no tocan git)."""
import unittest
from datetime import datetime, timezone

from herramientas import latidos as lt

T = datetime(2026, 10, 27, 21, 42, 54, tzinfo=timezone.utc)  # hora del commit fb1e654


class TestLatidos(unittest.TestCase):
    def test_hora_bien_formada(self):
        self.assertEqual(lt.hora_de_latido("2026-10-27 21:42 UTC · cierre · OK"), T.replace(second=0))

    def test_hora_vaga_es_formato_malo(self):
        for l in ("2026-10-27 13:3x UTC · inteligencia · OK", "2026-10-27 ~13:35 UTC · x", "2026-10-27 13:16-13:3x UTC · x"):
            self.assertIn("formato", lt.revisar_linea(l, T))

    def test_posterior_al_commit(self):
        # caso real de la revisión del 27-oct: latido "21:45" con commit 21:42:54
        self.assertIn("posterior", lt.revisar_linea("2026-10-27 21:45 UTC · cierre · OK", T))

    def test_tolerancia_de_un_minuto(self):
        self.assertIsNone(lt.revisar_linea("2026-10-27 21:43 UTC · cierre · OK", T))
        self.assertIsNone(lt.revisar_linea("2026-10-27 21:42 UTC · cierre · OK", T))

    def test_lineas_que_no_son_latido(self):
        self.assertIsNone(lt.revisar_linea("# Estado de las rutinas", T))
        self.assertIsNone(lt.revisar_linea("", T))

    def test_lineas_agregadas(self):
        diff = ("diff --git a/bitacora/estado-rutinas.md b/bitacora/estado-rutinas.md\n"
                "--- a/bitacora/estado-rutinas.md\n+++ b/bitacora/estado-rutinas.md\n"
                "@@ -1,0 +2 @@\n+2026-10-27 21:42 UTC · cierre · OK\r\n-viejo\n")
        self.assertEqual(lt.lineas_agregadas(diff), [("bitacora/estado-rutinas.md", "2026-10-27 21:42 UTC · cierre · OK")])

    def test_hora_vaga_regex(self):
        self.assertTrue(lt.RE_HORA_VAGA.search("corrida 17:1x UTC"))
        self.assertTrue(lt.RE_HORA_VAGA.search("a las ~21:5x"))
        self.assertFalse(lt.RE_HORA_VAGA.search("a las 21:50 UTC"))


if __name__ == "__main__":
    unittest.main()
