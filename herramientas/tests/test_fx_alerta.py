"""Pruebas de la regla FX-1 (herramientas/fx_alerta.py), sin red."""
import json
import math
import os
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from herramientas import banxico, datos
from herramientas import fx_alerta as fx
from herramientas import portafolio as pf
from herramientas import supervision as sv
from herramientas.parametros import parametros_efectivos

AYER = date(2026, 9, 29)       # martes
HOY = date(2026, 9, 30)        # miercoles
RUIDO = [0.004, -0.004] * 10   # sd ~0.41%: los umbrales quedan en sus pisos (1%, 3%, 4.5%)


def habiles_hasta(fin: date, n: int) -> list[date]:
    fechas, d = [], fin
    while len(fechas) < n:
        if d.weekday() < 5:
            fechas.append(d)
        d -= timedelta(days=1)
    return fechas[::-1]


def serie(rend: list[float], v0: float = 17.0, fin: date = AYER) -> list[tuple[date, float]]:
    """Referencia diaria que termina en 'fin' a partir de rendimientos logaritmicos."""
    vals = [v0]
    for r in rend:
        vals.append(vals[-1] * math.exp(r))
    return list(zip(habiles_hasta(fin, len(vals)), vals))


def datos_fx(ref, spot, fuente_ref="FIX Banxico SF43718"):
    return {"spot": spot, "hora": datetime(2026, 9, 30, 15, 0, tzinfo=timezone.utc),
            "fuente_spot": "spot Yahoo MXN=X 1m", "referencia": ref, "fuente_ref": fuente_ref, "notas": []}


class TestNiveles(unittest.TestCase):
    def test_ok_con_linea_informativa(self):
        ref = serie(RUIDO + [0.001] * 5)
        ev = fx.evaluar(ref, ref[-1][1] * 1.002, HOY)
        self.assertEqual(ev["candidatos"], [])
        self.assertLess(ev["umbral"]["alerta_d10"], 0.0451)  # piso de 4.5%
        (nivel, texto), = fx.lineas(ev, fx.decidir(ev, {}), datos_fx(ref, ev["spot"]), {"papel": 10_000.0})
        self.assertEqual(nivel, fx.OK)
        for pieza in ("FX-1 OK", "Δ1 +0.20%", "Δ10", "σd", "referencia FIX Banxico", "15:00 UTC", "papel ±100 MXN"):
            self.assertIn(pieza, texto)

    def test_aviso_por_d1(self):
        ref = serie(RUIDO + [0.0] * 5)
        ev = fx.evaluar(ref, ref[-1][1] * 1.012, HOY)
        c = fx.decidir(ev, {})["disparo"]
        self.assertEqual((c["nivel"], c["direccion"], c["motivo"]), (fx.AVISO, "sube", "Δ1"))
        self.assertAlmostEqual(ev["d1"], 0.012, places=6)
        self.assertLess(abs(ev["d10"]), 0.03)

    def test_aviso_por_d10(self):
        ref = serie(RUIDO + [0.0032] * 10)
        ev = fx.evaluar(ref, ref[-1][1] * 1.003, HOY)
        c = fx.decidir(ev, {})["disparo"]
        self.assertEqual((c["nivel"], c["direccion"], c["motivo"]), (fx.AVISO, "sube", "Δ10"))
        self.assertTrue(0.03 <= ev["d10"] < 0.045)
        self.assertLess(ev["d1"], 0.01)

    def test_alerta_por_d10(self):
        ref = serie(RUIDO + [0.0045] * 10)
        ev = fx.evaluar(ref, ref[-1][1] * 1.004, HOY)
        c = fx.decidir(ev, {})["disparo"]
        self.assertEqual((c["nivel"], c["direccion"], c["motivo"]), (fx.ALERTA, "sube", "Δ10"))
        self.assertGreaterEqual(ev["d10"], 0.045)
        self.assertLess(ev["ep_sube"], 0.06)

    def test_alerta_por_episodio_peso_fuerte(self):
        # Maximo hace 15 dias habiles; cae 2.6% antes de la ventana de D10 y 3.8% dentro: D10 no llega a
        # 4.5%, pero el episodio (hoy / maximo de las 15 referencias anteriores) pasa de -6%.
        ref = serie(RUIDO + [-0.0065] * 4 + [-0.0035] * 10)
        ev = fx.evaluar(ref, ref[-1][1] * 0.997, HOY)
        self.assertTrue(-0.045 < ev["d10"] <= -0.03)
        self.assertLessEqual(ev["ep_baja"], -0.06)
        c = fx.decidir(ev, {})["disparo"]
        self.assertEqual((c["nivel"], c["direccion"], c["motivo"], c["dias"]), (fx.ALERTA, "baja", "episodio", 15))
        (nivel, texto), = fx.lineas(ev, fx.decidir(ev, {}), datos_fx(ref, ev["spot"]), {"real-binance": 2_000.0})
        self.assertEqual(nivel, fx.ALERTA)
        self.assertIn("el dólar bajó 6.", texto)
        # Sin lotes no se inventa el efecto: solo la exposicion de hoy.
        self.assertIn("en 15 días; hoy tienes unos 2,000 MXN en dólares: cada 1% del dólar les mueve unos 20 MXN;",
                      texto)
        self.assertNotIn("a tu dinero le", texto)
        # Con lotes (BTC comprado antes del maximo de la ventana), el efecto es el del movimiento completo.
        base = c["base"]
        self.assertEqual(base, ev["max15"])
        lotes = {"real-binance": [{"ticker": "BTC-USD", "fecha": date(2026, 9, 1), "cantidad": 0.02,
                                   "precio": 100_000.0 / ev["spot"], "fx_compra": None}]}
        (_, texto), = fx.lineas(ev, fx.decidir(ev, {}), datos_fx(ref, ev["spot"]), {"real-binance": 2_000.0}, lotes)
        esperado = 0.02 * (100_000.0 / ev["spot"]) * (ev["spot"] - base[1])
        self.assertIn(f"a tu dinero le resta unos {abs(esperado):,.0f} MXN; hoy tienes", texto)

    def test_episodio_usa_la_referencia_de_hoy_si_existe(self):
        ref = serie(RUIDO + [0.0] * 5)
        con_hoy = ref + [(HOY, ref[-1][1] * 1.07)]
        ev = fx.evaluar(con_hoy, ref[-1][1] * 1.001, HOY)  # el spot ya regreso; el FIX de hoy no
        self.assertGreater(ev["ep_sube"], 0.06)
        self.assertEqual(ev["candidatos"][0]["motivo"], "episodio")

    def test_umbral_con_volatilidad_alta(self):
        ref = serie([0.012, -0.012] * 10 + [0.0])  # sd ~1.2%: 2 sd = 2.4% > piso de 1%
        ev = fx.evaluar(ref, ref[-1][1] * 1.015, HOY)
        self.assertAlmostEqual(ev["umbral"]["aviso_d1"], 2 * ev["sigma"])
        self.assertEqual(ev["candidatos"], [])

    def test_referencia_insuficiente(self):
        with self.assertRaises(fx.ErrorFX):
            fx.evaluar(serie([0.001] * 10), 17.0, HOY)


class TestSupresion(unittest.TestCase):
    def setUp(self):
        self.ref = serie(RUIDO + [0.0045] * 10)
        self.spot = self.ref[-1][1] * 1.004

    def test_no_se_repite_y_redispara_al_ampliarse_1_sigma(self):
        ev = fx.evaluar(self.ref, self.spot, HOY)
        d0 = fx.decidir(ev, {})
        self.assertEqual(d0["disparo"]["nivel"], fx.ALERTA)
        estado = d0["estado"]
        self.assertIn("ALERTA:sube", estado["registros"])
        # Dos dias habiles despues, el dolar sube menos de sd raiz(10): no se repite (ni como AVISO).
        s10 = ev["sigma10"]
        ev2 = fx.evaluar(self.ref, self.spot * math.exp(0.8 * s10), date(2026, 10, 2))
        d2 = fx.decidir(ev2, estado)
        self.assertIsNone(d2["disparo"])
        self.assertEqual([(c["nivel"], c["direccion"]) for c, _ in d2["suprimidos"]],
                         [(fx.ALERTA, "sube"), (fx.AVISO, "sube")])
        (nivel, texto), = fx.lineas(ev2, d2, datos_fx(self.ref, ev2["spot"]), {})
        self.assertEqual(nivel, fx.OK)
        self.assertIn("suprimida: ya se avisó con la ALERTA del 30-sep; no se repite hasta el 14-oct", texto)
        # Si se amplia 1 sd raiz(10) mas desde el nivel avisado, vuelve a disparar.
        ev3 = fx.evaluar(self.ref, self.spot * math.exp(1.1 * s10), date(2026, 10, 2))
        d3 = fx.decidir(ev3, estado)
        self.assertEqual(d3["disparo"]["nivel"], fx.ALERTA)
        self.assertEqual(d3["estado"]["registros"]["ALERTA:sube"]["fecha"], "2026-10-02")

    def test_vence_a_los_10_dias_habiles_y_no_cruza_direcciones(self):
        estado = fx.decidir(fx.evaluar(self.ref, self.spot, HOY), {})["estado"]
        self.assertIsNone(fx.decidir(fx.evaluar(self.ref, self.spot, date(2026, 10, 13)), estado)["disparo"])
        self.assertIsNotNone(fx.decidir(fx.evaluar(self.ref, self.spot, date(2026, 10, 14)), estado)["disparo"])
        # Una ALERTA de subida no calla un movimiento a la baja.
        baja = serie(RUIDO + [0.0] * 5)
        ev = fx.evaluar(baja, baja[-1][1] * 0.985, date(2026, 10, 1))
        self.assertEqual(fx.decidir(ev, estado)["disparo"]["direccion"], "baja")

    def test_un_aviso_vigente_no_calla_una_alerta(self):
        estado = {"registros": {"AVISO:sube": {"fecha": "2026-09-29", "nivel": fx.AVISO, "direccion": "sube",
                                               "usdmxn": self.spot, "sigma10": 0.01, "motivo": "Δ1"}}}
        d = fx.decidir(fx.evaluar(self.ref, self.spot, HOY), estado)
        self.assertEqual(d["disparo"]["nivel"], fx.ALERTA)

    def test_estado_en_archivo(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "supervision" / "estado-fx.json"
            primera = fx.revisar(datos_fx(self.ref, self.spot), {}, HOY, ruta)
            self.assertEqual(primera[0][0], fx.ALERTA)
            self.assertEqual(json.loads(ruta.read_text(encoding="utf-8"))["registros"]["ALERTA:sube"]["fecha"],
                             "2026-09-30")
            segunda = fx.revisar(datos_fx(self.ref, self.spot * 1.001), {}, HOY, ruta)
            self.assertEqual(segunda[0][0], fx.OK)
            # Solo lectura (registrar=False) no escribe.
            ruta.unlink()
            fx.revisar(datos_fx(self.ref, self.spot), {}, HOY, ruta, registrar=False)
            self.assertFalse(ruta.exists())


class TestFuentes(unittest.TestCase):
    AHORA = datetime(2026, 9, 30, 15, 0, tzinfo=timezone.utc)

    def fuentes(self, **cambios):
        ref = serie(RUIDO + [0.0] * 5)
        base = {"spot_yahoo": lambda: {"precio": 17.2, "hora": self.AHORA, "cierre_previo": 17.1, "gmtoffset": 3600},
                "diario_yahoo": lambda: {"cierres": [(d + timedelta(days=1), v) for d, v in ref if d < AYER],
                                         "aperturas": {}, "gmtoffset": 3600},
                "fix": lambda *_a: ref,
                "spot_binance": lambda: 17.25,
                "diario_binance": lambda _h: ref}
        base.update(cambios)
        return base

    @staticmethod
    def falla(*_a):
        raise datos.ErrorDatos("sin red")

    def test_con_token_usa_fix(self):
        d = fx.obtener(self.AHORA, self.fuentes())
        self.assertEqual(d["fuente_ref"], "FIX Banxico SF43718")
        self.assertEqual((d["spot"], d["fuente_spot"]), (17.2, "spot Yahoo MXN=X 1m"))

    def test_respaldo_sin_token_usa_cierres_de_yahoo(self):
        with mock.patch.dict(os.environ, {"BANXICO_TOKEN": ""}):
            d = fx.obtener(self.AHORA, self.fuentes(fix=banxico.rango))  # lanza SinToken antes de la red
        self.assertIn("cierres diarios Yahoo MXN=X", d["fuente_ref"])
        self.assertIn("sin BANXICO_TOKEN", d["notas"][0])
        # El cierre anterior segun Yahoo (previousClose) es la referencia del dia habil anterior.
        self.assertEqual(d["referencia"][-1], (AYER, 17.1))
        self.assertEqual(fx.evaluar(d["referencia"], d["spot"], HOY)["ref1"], (AYER, 17.1))

    def test_si_yahoo_falla_usa_binance_con_nota_de_base(self):
        d = fx.obtener(self.AHORA, self.fuentes(fix=lambda *_a: (_ for _ in ()).throw(banxico.SinToken("x")),
                                                spot_yahoo=self.falla, diario_yahoo=self.falla))
        self.assertEqual((d["spot"], d["fuente_spot"]), (17.25, "spot Binance USDT/MXN"))
        self.assertIn("Binance USDT/MXN", d["fuente_ref"])
        self.assertIn(fx.NOTA_BINANCE, d["notas"])
        self.assertEqual(sum(n == fx.NOTA_BINANCE for n in d["notas"]), 1)

    def test_sin_ninguna_fuente(self):
        with self.assertRaises(fx.ErrorFX):
            fx.obtener(self.AHORA, self.fuentes(spot_yahoo=self.falla, spot_binance=self.falla))

    def test_reetiqueta_cierres_de_yahoo(self):
        # Barras de Londres: lunes 28 (cotizacion del domingo en la noche = cierre del viernes 25),
        # martes 29 (= cierre del lunes 28) y la barra en curso del miercoles 30 (precio en vivo).
        barras = [(date(2026, 9, 28), 17.74), (date(2026, 9, 29), 17.97), (HOY, 18.02)]
        self.assertEqual(fx.referencia_yahoo(barras, HOY, 18.029),
                         [(date(2026, 9, 25), 17.74), (date(2026, 9, 28), 17.97), (AYER, 18.029)])
        self.assertEqual(fx.referencia_yahoo(barras, HOY, None)[-1], (date(2026, 9, 28), 17.97))

    def test_spot_yahoo_1m(self):
        texto = json.dumps({"chart": {"result": [{"meta": {"previousClose": 18.0292, "gmtoffset": 3600},
                                                  "timestamp": [1790780000, 1790780060, 1790780120],
                                                  "indicators": {"quote": [{"close": [18.01, 18.02, None]}]}}]}})
        s = fx.parsear_spot_yahoo(texto)
        self.assertEqual((s["precio"], s["cierre_previo"]), (18.02, 18.0292))
        self.assertEqual(s["hora"], datetime.fromtimestamp(1790780060, tz=timezone.utc))

    def test_binance_solo_cierres_de_dias_habiles_completos(self):
        def vela(d, o, h, l, c):
            ms = int(datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp() * 1000)
            return [ms, str(o), str(h), str(l), str(c), "1", ms + 86_399_999]
        velas = [vela(date(2026, 9, 25), 17.69, 17.8, 17.6, 17.70), vela(date(2026, 9, 26), 17.7, 17.75, 17.69, 17.748),
                 vela(date(2026, 9, 29), 17.98, 18.13, 17.87, 18.047), vela(HOY, 18.047, 18.11, 17.94, 18.0)]
        self.assertEqual(fx.parsear_klines_binance(json.dumps(velas), HOY),
                         [(date(2026, 9, 25), 17.70), (AYER, 18.047)])


class TestEfectoPorCuenta(unittest.TestCase):
    def test_descomposicion_precio_y_cambio(self):
        pos = [{"cantidad": 7, "p0": 90.0, "p1": 91.0, "moneda": "USD"},
               {"cantidad": 10, "p0": 50.0, "p1": 49.0, "moneda": "MXN"}]
        e = fx.descomponer(pos, 18.0, 18.2)
        self.assertAlmostEqual(e["precio"], 7 * 1.0 * 18.0 - 10.0)
        self.assertAlmostEqual(e["cambio"], 7 * 91.0 * 0.2)
        self.assertAlmostEqual(e["total"], (7 * 91 * 18.2 + 490) - (7 * 90 * 18.0 + 500))

    def test_efecto_del_movimiento_y_frase(self):
        self.assertAlmostEqual(fx.efecto_movimiento(10_510.0, 0.051), 510.0)
        c = {"nivel": fx.ALERTA, "direccion": "sube", "motivo": "Δ10", "cambio": 0.051, "umbral": 0.045, "dias": 10,
             "base": (date(2026, 9, 16), 17.19)}
        expos = {"papel": 99_999.0, "real": 8_000.0, "real-binance": 2_510.0}
        # Todo lo real se tuvo toda la ventana: el efecto real es el del movimiento completo.
        frase = fx.frase_dueno(c, expos, HOY, 510.0)
        self.assertEqual(frase, "el dólar subió 5.1% en 10 días; a tu dinero le suma unos 510 MXN; hoy tienes unos "
                                "10,510 MXN en dólares: cada 1% del dólar les mueve unos 105 MXN; no hay que hacer "
                                "nada hoy, lo revisa el comité del viernes 2-oct")
        # Comprado con el dolar ya arriba: el efecto real es chico y la frase dice por que.
        frase = fx.frase_dueno(c, expos, HOY, 3.2)
        self.assertIn("a tu dinero le suma unos 3 MXN, porque casi todo lo que tienes en dólares lo compraste con "
                      "el dólar ya arriba; hoy tienes unos 10,510 MXN", frase)
        self.assertIn("a tu dinero casi no le cambió (menos de 1 MXN)", fx.frase_dueno(c, expos, HOY, -0.3))
        self.assertIn("a tu dinero le resta 1 MXN,", fx.frase_dueno(c, expos, HOY, -1.2))
        # Sin lotes: solo la exposicion, nunca parte en USD de hoy x movimiento de toda la ventana.
        self.assertNotIn("a tu dinero le", fx.frase_dueno(c, expos, HOY))
        self.assertIn("comité de hoy, viernes 2-oct", fx.frase_dueno(c, {"real": 1_000.0}, date(2026, 10, 2)))
        self.assertIn("no tiene parte en dólares", fx.frase_dueno(c, {"real": 0.0}, HOY))
        self.assertIn("no pude calcular", fx.frase_dueno(c, {"papel": 1_000.0, "real": None}, HOY))

    def test_efecto_cambiario_por_lote(self):
        ref = [(date(2026, 9, 16), 17.20), (date(2026, 9, 22), 17.60), (date(2026, 9, 28), 17.90),
               (date(2026, 9, 29), 18.07)]
        base, spot = (date(2026, 9, 16), 17.20), 18.10
        lote = {"ticker": "X", "cantidad": 2.0, "precio": 100.0, "fx_compra": None}
        # Ya estaba al inicio de la ventana: desde la base.
        self.assertAlmostEqual(fx.efecto_cambiario([{**lote, "fecha": date(2026, 9, 1)}], ref, base, spot, HOY),
                               200 * (18.10 - 17.20))
        # Comprado dentro de la ventana: desde la referencia de su fecha, o desde su tipo_cambio.
        self.assertAlmostEqual(fx.efecto_cambiario([{**lote, "fecha": date(2026, 9, 29)}], ref, base, spot, HOY),
                               200 * (18.10 - 18.07))
        self.assertAlmostEqual(fx.efecto_cambiario([{**lote, "fecha": date(2026, 9, 29), "fx_compra": 18.05}],
                                                   ref, base, spot, HOY), 200 * (18.10 - 18.05))
        # Comprado en fin de semana: la referencia anterior mas cercana.
        self.assertAlmostEqual(fx.efecto_cambiario([{**lote, "fecha": date(2026, 9, 27)}], ref, base, spot, HOY),
                               200 * (18.10 - 17.60))
        # Comprado hoy sin referencia de hoy: efecto cero.
        self.assertAlmostEqual(fx.efecto_cambiario([{**lote, "fecha": HOY}], ref, base, spot, HOY), 0.0)

    def test_lotes_usd_peps(self):
        ops = [{"fecha": date(2026, 9, 1), "ticker": "SPYM", "lado": "compra", "cantidad": 5, "moneda": "USD",
                "tipo_cambio": 17.2},
               {"fecha": date(2026, 9, 20), "ticker": "SPYM", "lado": "compra", "cantidad": 3, "moneda": "USD",
                "tipo_cambio": None},
               {"fecha": date(2026, 9, 25), "ticker": "SPYM", "lado": "venta", "cantidad": 6, "moneda": "USD",
                "tipo_cambio": 17.8},
               {"fecha": date(2026, 9, 29), "ticker": "BTC-USD", "lado": "compra", "cantidad": 0.001,
                "moneda": "MXN", "tipo_cambio": None},
               {"fecha": date(2026, 9, 29), "ticker": "AMXB.MX", "lado": "compra", "cantidad": 10, "moneda": "MXN",
                "tipo_cambio": None},
               {"fecha": date(2026, 9, 29), "ticker": "QQQM", "lado": "compra", "cantidad": 1, "moneda": "USD",
                "tipo_cambio": 18.0}]
        filas = [{"ticker": "SPYM", "moneda": "USD", "precio": 90.0},
                 {"ticker": "BTC-USD", "moneda": "USD", "precio": 110_000.0},
                 {"ticker": "AMXB.MX", "moneda": "MXN", "precio": 20.0},
                 {"ticker": "QQQM", "moneda": "USD", "precio": None}]  # sin precio: no entra
        lotes = fx.lotes_usd(ops, filas)
        self.assertEqual([(x["ticker"], x["fecha"], x["cantidad"], x["fx_compra"]) for x in lotes],
                         [("BTC-USD", date(2026, 9, 29), 0.001, None), ("SPYM", date(2026, 9, 20), 2, None)])

    def test_supervision_calcula_la_parte_usd_de_cada_libro(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = Path(tmp)
            ops = b / "operaciones.csv"
            pf.registrar(ops, "2026-09-28", "", "deposito", 20_000)
            pf.registrar(ops, "2026-09-28", "SPYM", "compra", 7, 80.0, "USD", comision=0, tipo_cambio=18.0)
            (b / "real-binance").mkdir()
            rb = b / "real-binance" / "operaciones.csv"
            pf.registrar(rb, "2026-09-29", "", "deposito", 5_000)
            pf.registrar(rb, "2026-09-29", "BTC-USD", "compra", 0.001, 1_500_000.0, "MXN")
            precios = lambda _t: ({"SPYM": (AYER, 90.0, "USD"), "BTC-USD": (AYER, 100_000.0, "USD")}, [])  # noqa: E731
            ref = serie(RUIDO + [0.0045] * 10)
            salida = sv.supervisar(datetime(2026, 9, 30, 15, 0, tzinfo=timezone.utc),
                                   parametros_efectivos("arena_agresivo"), precios, None, None, 18.0,
                                   lambda _d: (lambda _f: 18.0), b, parametros_efectivos("cripto_binance"),
                                   datos_fx=lambda: datos_fx(ref, ref[-1][1] * 1.004))
            fx1 = [x for x in salida if x[1].startswith("FX-1")]
            self.assertEqual(len(fx1), 1)
            nivel, texto = fx1[0]
            self.assertEqual(nivel, sv.ALERTA)
            # papel: 7 x 90 x 18 = 11,340 MXN en USD -> 113 por 1%; real-binance: 0.001 x 100,000 x 18 = 1,800 -> 18.
            self.assertIn("papel ±113 MXN; real sin libro valuado; papel-binance sin libro valuado; "
                          "real-binance ±18 MXN; total ±131 MXN", texto)
            # El BTC real se compro el 29-sep (dentro de la ventana de D10): el efecto real es el del
            # USD/MXN de su fecha al spot (0.4%), no el de toda la ventana (4.5% x 1,800 = 78 MXN).
            spot = ref[-1][1] * 1.004
            efecto = 0.001 * 100_000.0 * (spot - ref[-1][1])
            self.assertIn(f"a tu dinero le suma unos {efecto:,.0f} MXN, porque casi todo lo que tienes en dólares "
                          f"lo compraste con el dólar ya arriba; hoy tienes unos 1,800 MXN en dólares", texto)
            self.assertNotIn("unos 78 MXN", texto)
            self.assertTrue((b / "supervision" / "estado-fx.json").exists())
            # Sin datos de tipo de cambio: AVISO, no se cae la supervision.
            corto = lambda: datos_fx(serie([0.001] * 5), 17.0)  # noqa: E731
            salida = sv.supervisar(datetime(2026, 9, 30, 15, 0, tzinfo=timezone.utc),
                                   parametros_efectivos("arena_agresivo"), None, None, None, None, None, b,
                                   datos_fx=corto)
            self.assertIn(sv.AVISO, [n for n, t in salida if t.startswith("FX-1 sin datos")])


class TestRevision(unittest.TestCase):
    """Correcciones de la revision de FX-1 (30-sep-2026)."""

    AHORA = datetime(2026, 9, 30, 15, 0, tzinfo=timezone.utc)

    @staticmethod
    def falla(*_a):
        raise datos.ErrorDatos("sin red")

    def test_sin_spot_de_yahoo_ni_token_el_cierre_de_ayer_sale_de_la_apertura_en_curso(self):
        ref = serie(RUIDO + [0.0] * 5)
        diario = {"cierres": [(d + timedelta(days=1), v) for d, v in ref if d < AYER] + [(HOY, 17.3)],
                  "aperturas": {HOY: 17.15}, "gmtoffset": 3600}
        base = {"spot_yahoo": self.falla, "spot_binance": lambda: 17.25, "diario_yahoo": lambda: diario,
                "fix": lambda *_a: (_ for _ in ()).throw(banxico.SinToken("x")), "diario_binance": self.falla}
        d = fx.obtener(self.AHORA, base)
        self.assertEqual(d["referencia"][-1], (AYER, 17.15))  # no el precio en vivo de la barra en curso
        self.assertEqual(fx.evaluar(d["referencia"], d["spot"], HOY)["ref1"][0], AYER)
        self.assertFalse(any("referencia más reciente" in n for n in d["notas"]))
        # Si tampoco hay apertura, D1 mediria 2 dias: se dice en una nota.
        d = fx.obtener(self.AHORA, {**base, "diario_yahoo": lambda: {**diario, "aperturas": {}}})
        self.assertEqual(d["referencia"][-1][0], date(2026, 9, 28))
        self.assertTrue(any("del 28-sep, no del 29-sep: Δ1 mide 2 días hábiles" in n for n in d["notas"]))

    def test_parsea_diario_de_yahoo_con_barra_en_curso(self):
        # Forma real (30-sep): la barra del dia en curso trae cierre nulo y un punto extra con el precio en vivo.
        ts = [int(datetime(2026, 9, 27, 23, tzinfo=timezone.utc).timestamp()),
              int(datetime(2026, 9, 28, 23, tzinfo=timezone.utc).timestamp()),
              int(datetime(2026, 9, 29, 23, tzinfo=timezone.utc).timestamp()),
              int(datetime(2026, 9, 30, 16, 2, tzinfo=timezone.utc).timestamp())]
        texto = json.dumps({"chart": {"result": [{"meta": {"gmtoffset": 3600}, "timestamp": ts, "indicators": {
            "quote": [{"open": [17.7445, 17.9732, 18.0292, 18.0292], "close": [17.7487, 17.9720, None, 18.0741],
                       "high": [99.0, 99.0, 99.0, 99.0], "low": [1.0, 1.0, 1.0, 1.0]}]}}]}})
        d = fx.parsear_diario_yahoo(texto)
        self.assertEqual(d["cierres"], [(date(2026, 9, 28), 17.7487), (AYER, 17.9720), (HOY, 18.0741)])
        self.assertEqual(d["aperturas"][HOY], 18.0292)
        self.assertEqual(fx.referencia_yahoo(d["cierres"], HOY, None, d["aperturas"][HOY]),
                         [(date(2026, 9, 25), 17.7487), (date(2026, 9, 28), 17.9720), (AYER, 18.0292)])

    def test_la_fecha_es_la_de_la_ciudad_de_mexico(self):
        jueves_noche = datetime(2026, 10, 2, 1, 27, tzinfo=timezone.utc)  # 19:27 CDMX del jueves 1-oct
        self.assertEqual(fx.fecha_local(jueves_noche), date(2026, 10, 1))
        jueves = date(2026, 10, 1)
        ref = serie(RUIDO + [0.0045] * 10, fin=date(2026, 9, 30)) + [(jueves, 18.3)]  # FIX del jueves ya publicado
        d = fx.obtener(jueves_noche, {"spot_yahoo": lambda: {"precio": 18.31, "hora": jueves_noche,
                                                             "cierre_previo": 18.3, "gmtoffset": 3600},
                                      "fix": lambda *_a: ref})
        self.assertEqual(d["notas"], [])
        ev = fx.evaluar(d["referencia"], d["spot"], fx.fecha_local(jueves_noche))
        self.assertEqual((ev["ref1"][0], ev["ref_hoy"]), (date(2026, 9, 30), 18.3))
        c = fx.decidir(ev, {})["disparo"]
        self.assertEqual(c["nivel"], fx.ALERTA)
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "estado-fx.json"
            (nivel, texto), = fx.revisar(d, {"real": 1_000.0}, fx.fecha_local(jueves_noche), ruta)
            self.assertIn("lo revisa el comité del viernes 2-oct", texto)
            self.assertNotIn("comité de hoy", texto)
            self.assertEqual(json.loads(ruta.read_text(encoding="utf-8"))["registros"]["ALERTA:sube"]["fecha"],
                             "2026-10-01")

    def _main(self, argv, por_cuenta=None, lineas=None):
        ref = serie(RUIDO + [0.0045] * 10)
        d = datos_fx(ref, ref[-1][1] * 1.004)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ruta = Path(tmp.name) / "supervision" / "estado-fx.json"
        salida = []
        parches = [mock.patch.object(fx, "obtener", lambda _a: dict(d)),
                   mock.patch.object(fx, "RUTA_ESTADO", ruta),
                   mock.patch.object(fx, "fecha_local", lambda _a: HOY),
                   mock.patch("builtins.print", lambda *a, **_k: salida.append(" ".join(map(str, a))))]
        if por_cuenta is not None:
            parches.append(mock.patch.object(fx, "por_cuenta", por_cuenta))
        if lineas is not None:
            parches.append(mock.patch.object(fx, "lineas", lineas))
        for pa in parches:
            pa.start()
            self.addCleanup(pa.stop)
        return fx.main(argv), salida, ruta

    def test_registrar_guarda_al_final_y_por_cuenta_no_tumba_la_salida(self):
        def revienta(*_a, **_k):
            raise datos.ErrorDatos("Yahoo caido")
        nivel, salida, ruta = self._main(["--registrar"], por_cuenta=revienta)
        self.assertEqual(nivel, fx.ALERTA)
        self.assertTrue(salida[0].startswith("ALERTA · FX-1 ALERTA"))
        self.assertIn("sin libros valuados (ErrorDatos: Yahoo caido)", salida[0])
        self.assertIn("registrada en bitacora/supervision/estado-fx.json", salida[-1])
        self.assertTrue(ruta.exists())

    def test_si_la_salida_falla_la_alerta_no_queda_suprimida(self):
        def rompe(*_a, **_k):
            raise RuntimeError("x")
        with self.assertRaises(RuntimeError):
            self._main(["--registrar"], por_cuenta=lambda *_a: fx.cuentas_vacias(), lineas=rompe)
        ruta = fx.RUTA_ESTADO
        self.assertFalse(ruta.exists())
        with tempfile.TemporaryDirectory() as tmp:
            r = Path(tmp) / "estado-fx.json"
            ref = serie(RUIDO + [0.0045] * 10)
            with mock.patch.object(fx, "lineas", rompe), self.assertRaises(RuntimeError):
                fx.revisar(datos_fx(ref, ref[-1][1] * 1.004), {}, HOY, r)
            self.assertFalse(r.exists())

    def test_si_no_se_puede_guardar_el_estado_la_alerta_sale_igual(self):
        ref = serie(RUIDO + [0.0045] * 10)

        def disco_lleno(*_a):
            raise OSError("No space left on device")
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(fx, "guardar_estado", disco_lleno):
            salida = fx.revisar(datos_fx(ref, ref[-1][1] * 1.004), {}, HOY, Path(tmp) / "estado-fx.json")
        self.assertEqual([n for n, _ in salida], [fx.ALERTA, fx.AVISO])
        self.assertIn("no se pudo guardar estado-fx.json", salida[1][1])

    def test_estado_mal_formado_no_tumba_la_supervision(self):
        ref = serie(RUIDO + [0.0045] * 10)
        casos = ['[]', '{"registros": []}',
                 '{"registros": {"ALERTA:sube": {"fecha": "28/09/2026", "nivel": 2, "direccion": "sube", '
                 '"usdmxn": 17.8}}}',
                 '{"registros": {"ALERTA:sube": {"fecha": "2026-09-28", "nivel": 2}}}']
        for contenido in casos:
            with self.subTest(contenido=contenido), tempfile.TemporaryDirectory() as tmp:
                b = Path(tmp)
                (b / "supervision").mkdir()
                (b / "supervision" / "estado-fx.json").write_text(contenido, encoding="utf-8")
                (b / "estado-rutinas.md").write_text("2026-09-30 14:00 UTC · x · OK\n", encoding="utf-8")
                salida = sv.supervisar(self.AHORA, parametros_efectivos("arena_agresivo"), None, None, None, None,
                                       None, b, datos_fx=lambda: datos_fx(ref, ref[-1][1] * 1.004))
                fx1 = [t for _, t in salida if t.startswith("FX-1")]
                self.assertEqual(len(fx1), 1)
                self.assertTrue(fx1[0].startswith("FX-1 ALERTA"))
                self.assertRegex(fx1[0], "estado-fx.json( con forma inválida|: registro)")
                self.assertIn("latido", " ".join(t for _, t in salida))  # el resto de la supervision sigue
        # Un registro valido convive con uno invalido: el valido sigue suprimiendo.
        estado, notas = fx.validar_estado({"registros": {
            "ALERTA:sube": {"fecha": "2026-09-30", "nivel": 2, "direccion": "sube", "usdmxn": "17.9"},
            "AVISO:baja": {"fecha": "2026-09-30", "nivel": 1, "direccion": "lateral", "usdmxn": 17.9}}})
        self.assertEqual(list(estado["registros"]), ["ALERTA:sube"])
        self.assertEqual(estado["registros"]["ALERTA:sube"]["usdmxn"], 17.9)
        self.assertIn("AVISO:baja", notas[0])

    def test_cualquier_error_de_fx1_es_aviso(self):
        def rompe():
            raise KeyError("referencia")
        salida = sv.revisar_fx(rompe, {}, self.AHORA, Path(tempfile.gettempdir()))
        self.assertEqual(salida[0][0], sv.AVISO)
        self.assertTrue(salida[0][1].startswith("FX-1 error (KeyError"))

    def test_sin_red_tambien_hay_linea_fx1(self):
        with tempfile.TemporaryDirectory() as tmp:
            salida = sv.supervisar(self.AHORA, parametros_efectivos("arena_agresivo"), None, None, None, None,
                                   None, Path(tmp))
        self.assertIn((sv.OK, "FX-1 no evaluada (--sin-red: no se consultó el tipo de cambio); "
                              "corre python3 herramientas/fx_alerta.py"), salida)

    def test_brief_misma_ventana_y_tickers_omitidos(self):
        class Libro:
            posiciones = {"SPYM": {"cantidad": 7, "moneda": "USD"}, "XYZ": {"cantidad": 1, "moneda": "USD"}}

        def grafica(t, *_a):
            if t == "XYZ":
                raise datos.ErrorDatos("404")
            return {"meta": {"currency": "USD"}, "serie": [(date(2026, 9, 28), 90.0), (AYER, 91.0)]}
        pos, omitidos = fx._posiciones_con_cierres(Libro(), grafica)
        self.assertEqual(omitidos, ["XYZ"])
        self.assertEqual((pos[0]["f0"], pos[0]["p0"], pos[0]["p1"]), (date(2026, 9, 28), 90.0, 91.0))
        # fx0 = USD/MXN de la fecha del cierre previo: precio y cambio cubren la misma ventana.
        pos[0]["fx0"] = 17.90
        e = fx.descomponer(pos, 18.05, 18.10)
        self.assertAlmostEqual(e["precio"], 7 * 1.0 * 17.90)
        self.assertAlmostEqual(e["cambio"], 7 * 91.0 * (18.10 - 17.90))
        self.assertAlmostEqual(e["total"], 7 * 91 * 18.10 - 7 * 90 * 17.90)
        ref = serie(RUIDO + [0.0] * 5)
        d = datos_fx(ref, 17.2)
        ev = fx.evaluar(ref, 17.2, HOY)
        cuentas = {"expos": {"papel": 7 * 91 * 18.1, "real": None}, "efectos": {"papel": e, "real": None},
                   "lotes": {}, "previos": {"papel": (date(2026, 9, 28), date(2026, 9, 28)), "real": None},
                   "notas": ["papel: sin cierres de Yahoo para XYZ; no entran en el efecto de precio ni en la parte "
                             "en USD (subestimadas)"]}
        linea = fx.linea_brief(d, ev, fx.decidir(ev, {}), cuentas)
        self.assertIn("papel (desde el cierre del 28-sep): precio +125 MXN, cambio +127 MXN; real: sin libro", linea)
        self.assertIn("al USD/MXN de la fecha de ese cierre", linea)
        self.assertIn("sin cierres de Yahoo para XYZ", linea)


if __name__ == "__main__":
    unittest.main()
