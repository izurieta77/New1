"""Pruebas del conciliador de ventas de combustible (datos/asunto-fiscal-sgm/conciliacion_ventas_cfdi.py)."""
import importlib.util
import os
import tempfile
import unittest

RUTA = os.path.join(os.path.dirname(__file__), "..", "..", "datos", "asunto-fiscal-sgm", "conciliacion_ventas_cfdi.py")
spec = importlib.util.spec_from_file_location("conciliacion_ventas_cfdi", RUTA)
cv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cv)

TPL = ('<?xml version="1.0" encoding="UTF-8"?>'
       '<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/{v}" '
       'xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital" Version="{ver}" Fecha="{f}T10:00:00" '
       'TipoDeComprobante="{t}" FormaPago="{fp}" MetodoPago="PUE">'
       '<cfdi:Receptor Rfc="{r}"/><cfdi:Conceptos><cfdi:Concepto ClaveProdServ="{c}" Cantidad="{q}"/>'
       '</cfdi:Conceptos><cfdi:Complemento><tfd:TimbreFiscalDigital UUID="{u}"/></cfdi:Complemento>'
       '</cfdi:Comprobante>')


def xml(d, nombre, u, f="2026-01-05", t="I", fp="04", r="XAXX010101000", c="15101505", q=1000, v="4"):
    ver = "4.0" if v == "4" else "3.3"
    with open(os.path.join(d, nombre), "w", encoding="utf-8") as h:
        h.write(TPL.format(v=v, ver=ver, f=f, t=t, fp=fp, r=r, c=c, q=q, u=u))


class TestConciliacion(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = os.path.join(self.tmp.name, "xml")
        os.makedirs(self.d)
        self.vol = os.path.join(self.tmp.name, "vol.csv")

    def tearDown(self):
        self.tmp.cleanup()

    def entregas(self, filas):
        with open(self.vol, "w", encoding="utf-8") as h:
            h.write("mes,producto,litros_entregados\n")
            for m, p, l in filas:
                h.write(f"{m},{p},{l}\n")

    def fila(self, filas, mes, prod):
        return next(f for f in filas if f[0] == mes and f[1] == prod)

    def test_cfdi_33_se_cuenta(self):
        xml(self.d, "a.xml", "U1", q=5000, v="3")
        self.entregas([("2026-01", "diesel", 5000)])
        filas, _, _, errores, _ = cv.conciliar(self.d, self.vol)
        f = self.fila(filas, "2026-01", "diesel")
        self.assertEqual(f[2], 5000)
        self.assertEqual(f[8], "OK")
        self.assertEqual(errores, [])

    def test_xml_no_cfdi_es_error_visible(self):
        with open(os.path.join(self.d, "x.xml"), "w") as h:
            h.write('<?xml version="1.0"?><otro xmlns="urn:x"/>')
        self.entregas([])
        _, _, _, errores, _ = cv.conciliar(self.d, self.vol)
        self.assertEqual(len(errores), 1)

    def test_cancelado_por_metadata_se_excluye(self):
        xml(self.d, "a.xml", "U1", q=1000)
        xml(self.d, "b.xml", "U2", q=500)
        meta = os.path.join(self.tmp.name, "m.txt")
        with open(meta, "w") as h:
            h.write("Uuid~RfcEmisor~Estatus\nU2~X~0\n")
        self.entregas([("2026-01", "diesel", 1000)])
        filas, *_ = cv.conciliar(self.d, self.vol, meta)
        self.assertEqual(self.fila(filas, "2026-01", "diesel")[2], 1000)

    def test_egresos_no_restan_por_omision(self):
        xml(self.d, "a.xml", "U1", q=1000)
        xml(self.d, "e.xml", "U2", t="E", q=100)
        self.entregas([("2026-01", "diesel", 1000)])
        filas, *_ = cv.conciliar(self.d, self.vol)
        f = self.fila(filas, "2026-01", "diesel")
        self.assertEqual((f[2], f[5], f[8]), (1000, 100, "OK"))
        filas, *_ = cv.conciliar(self.d, self.vol, restar_egresos=True)
        self.assertEqual(self.fila(filas, "2026-01", "diesel")[2], 900)

    def test_uuid_repetido(self):
        xml(self.d, "a.xml", "U1")
        xml(self.d, "a2.xml", "U1")
        self.entregas([("2026-01", "diesel", 1000)])
        filas, _, repetidos, _, _ = cv.conciliar(self.d, self.vol)
        self.assertEqual(repetidos, ["U1"])
        self.assertEqual(self.fila(filas, "2026-01", "diesel")[2], 1000)

    def test_entregas_en_cero_con_litros_facturados(self):
        xml(self.d, "a.xml", "U1", q=800)
        self.entregas([("2026-01", "diesel", 0)])
        filas, *_ = cv.conciliar(self.d, self.vol)
        self.assertIn("FACTURADO > ENTREGADO", self.fila(filas, "2026-01", "diesel")[8])

    def test_bandas_05_y_15(self):
        self.assertEqual(cv.clasificar(990, 1000)[1], "ENTREGADO > FACTURADO > 0.5% (55 VII f)")
        self.assertEqual(cv.clasificar(980, 1000)[1], "ENTREGADO > FACTURADO > 1.5% (55 VII y 111 Bis b)")
        self.assertEqual(cv.clasificar(996, 1000)[1], "OK")
        self.assertEqual(cv.clasificar(1006, 1000)[1], "FACTURADO > ENTREGADO")

    def test_global_con_clave_generica_se_reporta_aparte(self):
        xml(self.d, "g.xml", "U1", c="01010101", q=1)
        self.entregas([("2026-01", "diesel", 1000)])
        filas, _, _, _, sin_clave = cv.conciliar(self.d, self.vol)
        self.assertEqual(sin_clave, {"2026-01": 1})

    def test_nominativo_en_efectivo(self):
        xml(self.d, "a.xml", "U1", r="ABC010101AAA", fp="01")
        self.entregas([("2026-01", "diesel", 1000)])
        _, efectivo, _, _, _ = cv.conciliar(self.d, self.vol)
        self.assertEqual([d["uuid"] for d in efectivo], ["U1"])

    def test_reporte_se_genera(self):
        xml(self.d, "a.xml", "U1")
        self.entregas([("2026-01", "diesel", 1000)])
        texto = cv.reporte(*cv.conciliar(self.d, self.vol))
        self.assertIn("| 2026-01 | diesel |", texto)


if __name__ == "__main__":
    unittest.main()
