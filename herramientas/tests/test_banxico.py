import os, unittest
from datetime import date
from unittest import mock

from herramientas import banxico as bx

PAYLOAD = {"bmx": {"series": [
    {"idSerie": "SF43936", "titulo": "CETES 28", "datos": [
        {"fecha": "17/09/2026", "dato": "6.20"}, {"fecha": "24/09/2026", "dato": "6.15"}, {"fecha": "01/10/2026", "dato": "N/E"}]},
    {"idSerie": "SF43718", "titulo": "FIX", "datos": [{"fecha": "25/09/2026", "dato": "17.7100"}]},
]}}


class TestBanxico(unittest.TestCase):
    def test_sin_token_lanza(self):
        with mock.patch.dict(os.environ, {"BANXICO_TOKEN": ""}):
            with self.assertRaises(bx.SinToken):
                bx.token()

    def test_parsea_y_omite_ne(self):
        datos = bx._parsear(PAYLOAD)
        self.assertEqual(datos["SF43936"], [(date(2026, 9, 17), 6.20), (date(2026, 9, 24), 6.15)])
        self.assertEqual(datos["SF43718"], [(date(2026, 9, 25), 17.71)])

    def test_oportuno_y_cetes(self):
        with mock.patch.dict(os.environ, {"BANXICO_TOKEN": "x"}), mock.patch.object(bx, "_fetch", return_value=PAYLOAD):
            self.assertEqual(bx.cetes28_anual(), (date(2026, 9, 24), 6.15))
            self.assertEqual(bx.oportuno()["SF43718"], (date(2026, 9, 25), 17.71))


if __name__ == "__main__":
    unittest.main()
