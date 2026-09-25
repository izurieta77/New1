"""Pruebas de herramientas/backtest.py: anti look-ahead, costos, metricas, segmentos, MXN y registro."""
import csv
import functools
import math
import random
import statistics
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from herramientas import backtest as bt
from herramientas import metricas as m


def fechas_mensuales(n: int, inicio=date(2000, 1, 31)) -> list[date]:
    salida, y, mo = [], inicio.year, inicio.month
    for _ in range(n):
        dia = [31, 29 if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mo - 1]
        salida.append(date(y, mo, dia))
        mo += 1
        if mo == 13:
            y, mo = y + 1, 1
    return salida


def serie_aleatoria(n: int, semilla: int = 1, media: float = 0.008, sd: float = 0.045) -> list[tuple]:
    rnd = random.Random(semilla)
    return list(zip(fechas_mensuales(n), [rnd.gauss(media, sd) for _ in range(n)]))


def efectivo_constante(serie, r=0.002):
    return [(f, r) for f, _ in serie]


SIN_COSTOS = {"comision_por_lado": 0.0, "spread_por_lado": 0.0}

# serie global para probar que una senal que la lee como global es detectada
_SERIE_GLOBAL: list = []
activo = []  # nombre que coincide con el atributo h.activo: no debe dar falso positivo


def _senal_que_lee_global(h):
    return 1.0 if _SERIE_GLOBAL[len(h)][1] > 0 else 0.0


def _senal_que_usa_atributo_activo(h):
    return 1.0 if h.activo[-1] > 0 else 0.0


class TestAntiLookAhead(unittest.TestCase):
    def setUp(self):
        self.datos = serie_aleatoria(120, semilla=3)
        self.ef = efectivo_constante(self.datos)

    def test_la_senal_solo_ve_hasta_t_menos_1(self):
        registro = []  # la senal no captura self (self guarda la serie completa y seria detectada)

        def espia(h):
            t = len(h)
            bloqueos = []
            for intento in (lambda: h.activo[t], lambda: h.fechas[t], lambda: h.efectivo[t], lambda: h.indice[t]):
                try:
                    intento()
                    bloqueos.append(False)
                except IndexError:
                    bloqueos.append(True)
            # en memoria alcanzable solo hay t observaciones: el dato t aun no existe
            registro.append((t, h.fecha_decision, len(h.activo._datos), len(h.indice._datos),
                             all(bloqueos), len(h.activo[t - 5:t + 50])))
            return 1.0

        r = bt.backtest_senal(self.datos, self.ef, espia, id_replica=None, variante="espia", min_historia=12)
        self.assertEqual(len(registro), 120 - 12)
        fechas = [f for f, _ in self.datos]
        for t, fecha_decision, en_memoria, en_memoria_indice, bloqueado, largo_corte in registro:
            self.assertEqual(fecha_decision, fechas[t - 1])
            self.assertEqual(en_memoria, t)
            self.assertEqual(en_memoria_indice, t)
            self.assertTrue(bloqueado)  # pedir el periodo que se decide lanza IndexError
            self.assertEqual(largo_corte, 5)  # los cortes se recortan a t
        self.assertEqual(r.fechas[0], fechas[12])

    def test_capturar_self_con_la_serie_es_detectado(self):
        def usa_self(h):
            return 1.0 if self.datos[len(h)][1] > 0 else 0.0

        with self.assertRaises(bt.ErrorLookAhead):
            bt.backtest_senal(self.datos, self.ef, usa_self, id_replica=None, variante="self")

    def test_closure_que_mira_el_futuro_es_detectada(self):
        datos = self.datos

        def oraculo(h):
            return 1.0 if datos[len(h)][1] > 0 else 0.0  # lee el rendimiento del periodo que decide

        with self.assertRaises(bt.ErrorLookAhead):
            bt.backtest_senal(datos, self.ef, oraculo, id_replica=None, variante="oraculo", **SIN_COSTOS)
        # con la revision desactivada corre, y muestra por que hay que bloquearla
        trampa = bt.backtest_senal(datos, self.ef, oraculo, id_replica=None, variante="oraculo",
                                   permitir_capturas=True, **SIN_COSTOS)
        honesta = bt.backtest_senal(datos, self.ef, bt.senal_comprar_y_mantener, id_replica=None,
                                    variante="bh", **SIN_COSTOS)
        self.assertGreater(trampa.metricas["completo"]["sharpe"], 3 * honesta.metricas["completo"]["sharpe"])
        self.assertTrue(all(r >= min(0.0, e) - 1e-15 for r, e in zip(trampa.r_neto, trampa.r_efectivo)))

    def test_global_default_objeto_y_partial_detectados(self):
        global _SERIE_GLOBAL
        _SERIE_GLOBAL = list(self.datos)
        try:
            with self.assertRaises(bt.ErrorLookAhead):
                bt.backtest_senal(self.datos, self.ef, _senal_que_lee_global, id_replica=None, variante="g")
        finally:
            _SERIE_GLOBAL = []

        def por_defecto(h, futuro=list(self.datos)):
            return 1.0 if futuro[len(h)][1] > 0 else 0.0

        class Oraculo:
            def __init__(self, datos):
                self.tabla = {"serie": list(datos)}  # anidado un nivel

            def __call__(self, h):
                return 1.0 if self.tabla["serie"][len(h)][1] > 0 else 0.0

        def con_datos(serie, h):
            return 1.0 if serie[len(h)][1] > 0 else 0.0

        for senal in (por_defecto, Oraculo(self.datos), functools.partial(con_datos, list(self.datos))):
            with self.assertRaises(bt.ErrorLookAhead, msg=repr(senal)):
                bt.backtest_senal(self.datos, self.ef, senal, id_replica=None, variante="x")

    def test_nombre_de_atributo_no_es_falso_positivo(self):
        global activo
        activo = list(self.datos)  # global con el mismo nombre que h.activo
        try:
            r = bt.backtest_senal(self.datos, self.ef, _senal_que_usa_atributo_activo, id_replica=None, variante="a")
            self.assertEqual(len(r.r_neto), 119)
        finally:
            activo = []

    def test_resultado_invariante_a_alterar_el_futuro(self):
        senal = bt.senal_media_movil(10)
        base = bt.backtest_senal(self.datos, self.ef, senal, id_replica=None, variante="sma", min_historia=10)
        rnd = random.Random(99)
        for k in (30, 60, 100):
            alterados = self.datos[:k] + [(f, rnd.gauss(0, 0.2)) for f, _ in self.datos[k:]]
            otro = bt.backtest_senal(alterados, self.ef, senal, id_replica=None, variante="sma", min_historia=10)
            # la exposicion del periodo k depende de datos hasta k-1: identica hasta k inclusive
            i = otro.fechas.index(self.datos[k][0])
            self.assertEqual(base.exposicion[:i + 1], otro.exposicion[:i + 1])

    def test_senal_usa_el_rendimiento_previo_no_el_actual(self):
        fechas = fechas_mensuales(40)
        alterna = [(f, 0.10 if i % 2 == 0 else -0.10) for i, f in enumerate(fechas)]

        def sigue_ultimo(h):
            return 1.0 if h.activo[-1] > 0 else 0.0

        r = bt.backtest_senal(alterna, 0.0, sigue_ultimo, id_replica=None, variante="ultimo", **SIN_COSTOS)
        # siempre entra despues de +10% y le toca -10%: no puede "atinar" al periodo actual
        for w, ra in zip(r.exposicion, r.r_activo):
            self.assertEqual(w == 1.0, ra < 0)
        self.assertLess(r.metricas["completo"]["rendimiento_total"], 0)

    def test_constructor_centrado_detectado_y_causal_aceptado(self):
        def media_centrada(datos):
            v = [x for _, x in datos]
            return [statistics.fmean(v[max(0, i - 3):i + 4]) for i in range(len(v))]

        def media_causal(datos):
            v = [x for _, x in datos]
            return [statistics.fmean(v[max(0, i - 6):i + 1]) for i in range(len(v))]

        def zscore_muestra_completa(datos):
            v = [x for _, x in datos]
            mu, sd = statistics.fmean(v), statistics.pstdev(v)
            return [(x - mu) / sd for x in v]

        self.assertFalse(bt.auditar_constructor(media_centrada, self.datos)["causal"])
        self.assertFalse(bt.auditar_constructor(zscore_muestra_completa, self.datos)["causal"])
        auditoria = bt.auditar_constructor(media_causal, self.datos)
        self.assertTrue(auditoria["causal"])
        with self.assertRaises(bt.ErrorLookAhead):
            bt.senal_precalculada([(f, 1.0) for f, _ in self.datos], bt.auditar_constructor(media_centrada, self.datos))

        valores = media_causal(self.datos)
        pesos = [(f, 1.0 if v > 0 else 0.0) for (f, _), v in zip(self.datos, valores)]
        senal = bt.senal_precalculada(pesos, auditoria)
        r = bt.backtest_senal(self.datos, self.ef, senal, id_replica=None, variante="pre", min_historia=7)
        # la exposicion del periodo t es la senal calculada al cierre de t-1
        for k, f in enumerate(r.fechas):
            t = [x for x, _ in self.datos].index(f)
            self.assertEqual(r.exposicion[k], pesos[t - 1][1])

    def test_extras_solo_con_fecha_de_disponibilidad_pasada(self):
        vistos = []
        macro = [(f + timedelta(days=15), float(i)) for i, (f, _) in enumerate(self.datos)]  # publicado 15 dias despues

        def mira_macro(h):
            ext = h.extras["macro"]
            vistos.append((len(ext), ext[-1][0] if len(ext) else None, h.fecha_decision))
            return 0.5

        bt.backtest_senal(self.datos, self.ef, mira_macro, id_replica=None, variante="m", extras={"macro": macro})
        # en t=1 solo se conoce hasta fecha_0: el dato de fecha_0 se publica 15 dias despues -> 0 visibles
        self.assertEqual(vistos[0][0], 0)
        self.assertEqual(vistos[1][0], 1)
        for largo, ultima_disponible, fecha_decision in vistos:
            if largo:
                self.assertLessEqual(ultima_disponible, fecha_decision)

    def test_exposicion_invalida(self):
        with self.assertRaises(ValueError):
            bt.backtest_senal(self.datos, self.ef, lambda h: 1.5, id_replica=None, variante="x")
        with self.assertRaises(ValueError):
            bt.backtest_senal(self.datos, self.ef, lambda h: float("nan"), id_replica=None, variante="x")
        r = bt.backtest_senal(self.datos, self.ef, lambda h: 1.5, id_replica=None, variante="x", exposicion_max=2.0)
        self.assertEqual(r.exposicion[0], 1.5)

    def test_id_replica_es_obligatorio(self):
        with self.assertRaises(TypeError):
            bt.backtest_senal(self.datos, self.ef, bt.senal_comprar_y_mantener, variante="x")  # sin id_replica


class TestCostosYRendimientos(unittest.TestCase):
    def setUp(self):
        self.datos = serie_aleatoria(60, semilla=5)
        self.ef = efectivo_constante(self.datos, 0.003)

    def test_costos_por_defecto_gbm(self):
        self.assertAlmostEqual(bt.COMISION_GBM_POR_LADO, 0.0029, places=12)
        self.assertAlmostEqual(bt.SPREAD_POR_LADO_DEFECTO, 0.0005, places=12)
        r = bt.backtest_senal(self.datos, self.ef, bt.senal_comprar_y_mantener, id_replica=None, variante="bh")
        self.assertAlmostEqual(r.costo[0], 0.0034, places=12)

    def test_comprar_y_mantener_paga_una_entrada(self):
        c, s = 0.003, 0.001
        r = bt.backtest_senal(self.datos, self.ef, bt.senal_comprar_y_mantener, id_replica=None, variante="bh",
                              comision_por_lado=c, spread_por_lado=s)
        self.assertAlmostEqual(r.rotacion[0], 1.0, places=12)
        self.assertAlmostEqual(r.r_neto[0], (1 - (c + s)) * (1 + self.datos[1][1]) - 1, places=12)
        self.assertTrue(all(abs(x) < 1e-12 for x in r.costo[1:]))  # w=1 no deriva
        self.assertAlmostEqual(r.curva[-1][1], (1 - c - s) * math.prod(1 + x for _, x in self.datos[1:]), places=10)
        self.assertEqual(r.metricas["completo"]["n_cambios_senal"], 1)

    def test_alternar_paga_cada_cambio(self):
        c = 0.005

        def alterna(h):
            return float(len(h) % 2)

        r = bt.backtest_senal(self.datos, self.ef, alterna, id_replica=None, variante="alt",
                              comision_por_lado=c, spread_por_lado=0.0)
        for k, (w, costo) in enumerate(zip(r.exposicion, r.costo)):
            previo = r.exposicion[k - 1] if k else 0.0
            self.assertAlmostEqual(costo, abs(w - previo) * c, places=12)
            ra, re_ = r.r_activo[k], r.r_efectivo[k]
            self.assertAlmostEqual(r.r_neto[k], (1 - costo) * (1 + w * ra + (1 - w) * re_) - 1, places=12)

    def test_deriva_de_pesos_constantes(self):
        r = bt.backtest_senal(self.datos, self.ef, lambda h: 0.5, id_replica=None, variante="mitad",
                              comision_por_lado=0.01, spread_por_lado=0.0)
        for k in range(1, len(r.exposicion)):
            w_pre = 0.5 * (1 + r.r_activo[k - 1]) / (1 + r.r_bruto[k - 1])
            self.assertAlmostEqual(r.rotacion[k], abs(0.5 - w_pre), places=12)
        sin_deriva = bt.backtest_senal(self.datos, self.ef, lambda h: 0.5, id_replica=None, variante="mitad",
                                       comision_por_lado=0.01, spread_por_lado=0.0, rebalanceo_con_deriva=False)
        self.assertTrue(all(x == 0 for x in sin_deriva.rotacion[1:]))

    def test_sin_costos_neto_igual_a_bruto(self):
        r = bt.backtest_senal(self.datos, self.ef, bt.senal_media_movil(6), id_replica=None, variante="sma",
                              min_historia=6, **SIN_COSTOS)
        self.assertEqual(r.r_neto, r.r_bruto)

    def test_efectivo_constante_numerico(self):
        r = bt.backtest_senal(self.datos, 0.001, bt.senal_efectivo, id_replica=None, variante="cash", **SIN_COSTOS)
        self.assertTrue(all(abs(x - 0.001) < 1e-15 for x in r.r_neto))

    def test_alineacion_reporta_descartes(self):
        ef = efectivo_constante(self.datos)[:-5]
        r = bt.backtest_senal(self.datos, ef, bt.senal_comprar_y_mantener, id_replica=None, variante="bh")
        self.assertEqual(r.meta["descartadas_activo"], 5)
        self.assertEqual(r.fechas[-1], self.datos[-6][0])


class TestMetricas(unittest.TestCase):
    def test_coinciden_con_metricas_py(self):
        datos = serie_aleatoria(150, semilla=11)
        ef = efectivo_constante(datos, 0.0025)
        r = bt.backtest_senal(datos, ef, bt.senal_media_movil(10), id_replica=None, variante="sma", min_historia=10)
        x = r.metricas["completo"]
        self.assertEqual(x["periodos_por_anio"], 12)
        self.assertAlmostEqual(x["cagr"], m.cagr(r.curva), places=12)
        self.assertAlmostEqual(x["vol_anual"], m.volatilidad_anualizada(r.r_neto, 12), places=12)
        self.assertAlmostEqual(x["sharpe"], m.sharpe(r.r_neto, rf=r.r_efectivo, periodos_por_anio=12), places=12)
        self.assertAlmostEqual(x["sortino"], m.sortino(r.r_neto, rf=r.r_efectivo, periodos_por_anio=12), places=12)
        self.assertAlmostEqual(x["mdd"], m.max_drawdown(r.curva)["valor"], places=12)
        self.assertAlmostEqual(x["calmar"], x["cagr"] / abs(x["mdd"]), places=12)
        exceso = [a - b for a, b in zip(r.r_neto, r.r_efectivo)]
        self.assertAlmostEqual(x["sharpe_periodo"] * math.sqrt(12), x["sharpe"], places=12)
        self.assertAlmostEqual(x["asimetria"], m.asimetria(exceso), places=12)
        self.assertAlmostEqual(x["exposicion_media"], statistics.fmean(r.exposicion), places=12)
        self.assertEqual(x["fecha_inicio"], datos[9][0])

    def test_inferir_frecuencia(self):
        self.assertEqual(bt.inferir_periodos_por_anio(fechas_mensuales(30)), 12)
        diarias = [date(2026, 1, 5) + timedelta(days=i) for i in range(30) if (date(2026, 1, 5) + timedelta(days=i)).weekday() < 5]
        self.assertEqual(bt.inferir_periodos_por_anio(diarias), 252)
        self.assertEqual(bt.inferir_periodos_por_anio([date(2000 + i, 12, 31) for i in range(10)]), 1)


class TestSegmentos(unittest.TestCase):
    def test_dentro_y_fuera_de_muestra(self):
        datos = serie_aleatoria(100, semilla=2)
        corte = datos[59][0]
        r = bt.backtest_senal(datos, efectivo_constante(datos), bt.senal_comprar_y_mantener, id_replica=None,
                              variante="bh", cortes=[corte.isoformat()])
        dentro, fuera = r.metricas["dentro_muestra"], r.metricas["fuera_muestra"]
        self.assertEqual(r.segmentos, ["dentro_muestra", "fuera_muestra"])
        self.assertEqual(dentro["fecha_fin"], corte)
        self.assertEqual(fuera["fecha_inicio"], corte)  # la curva fuera de muestra arranca en el corte
        self.assertEqual(dentro["n_periodos"] + fuera["n_periodos"], r.metricas["completo"]["n_periodos"])
        total = (1 + dentro["rendimiento_total"]) * (1 + fuera["rendimiento_total"]) - 1
        self.assertAlmostEqual(total, r.metricas["completo"]["rendimiento_total"], places=10)
        self.assertEqual(fuera["n_cambios_senal"], 0)

    def test_tres_segmentos(self):
        datos = serie_aleatoria(90, semilla=4)
        r = bt.backtest_senal(datos, 0.0, bt.senal_comprar_y_mantener, id_replica=None, variante="bh",
                              cortes=[datos[30][0], datos[60][0]])
        self.assertEqual(r.segmentos, ["desarrollo", "validacion", "prueba"])
        self.assertEqual(sum(r.metricas[s]["n_periodos"] for s in r.segmentos), 89)


class TestMonedaMXN(unittest.TestCase):
    def test_conversion_y_efectivo_local(self):
        datos = serie_aleatoria(30, semilla=8)
        fx = [(f, 17.0 * (1.01 ** i)) for i, (f, _) in enumerate(datos)]
        cetes = efectivo_constante(datos, 0.005)
        vistos = []

        def mira_fx(h):
            vistos.append(h.extras["fx"][-1][0] if len(h.extras["fx"]) else None)
            return 1.0

        r = bt.backtest_senal(datos, cetes, mira_fx, id_replica=None, variante="bh_mxn", fx=fx,
                              efectivo_en_mxn=True, **SIN_COSTOS)
        self.assertEqual(r.meta["moneda"], "MXN")
        for k, f in enumerate(r.fechas):
            t = [x for x, _ in datos].index(f)
            self.assertAlmostEqual(r.r_activo[k], (1 + datos[t][1]) * 1.01 - 1, places=12)
            self.assertAlmostEqual(r.r_efectivo[k], 0.005, places=15)  # CETES ya en MXN
            self.assertEqual(vistos[k], datos[t - 1][0])  # el fx visible es el de t-1
        usd = bt.backtest_senal(datos, cetes, bt.senal_efectivo, id_replica=None, variante="cash", fx=fx, **SIN_COSTOS)
        self.assertAlmostEqual(usd.r_efectivo[0], 1.005 * 1.01 - 1, places=12)  # efectivo en USD convertido

    def test_fx_con_huecos_es_error(self):
        datos = serie_aleatoria(30, semilla=8)
        fx = [(f, 17.0) for i, (f, _) in enumerate(datos) if not 10 <= i <= 12]
        with self.assertRaises(ValueError):
            bt.backtest_senal(datos, 0.0, bt.senal_comprar_y_mantener, id_replica=None, variante="x", fx=fx)


class TestRegistroVariantes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.datos = serie_aleatoria(180, semilla=21)
        self.ef = efectivo_constante(self.datos, 0.002)
        self.corte = self.datos[119][0]

    def tearDown(self):
        self.tmp.cleanup()

    def correr(self, ventana, **k):
        return bt.backtest_senal(self.datos, self.ef, bt.senal_media_movil(ventana), id_replica="T01",
                                 variante=f"sma{ventana}", min_historia=12, cortes=[self.corte],
                                 parametros={"ventana": ventana}, dir_replicas=self.dir, **k)

    def test_cada_corrida_se_registra_y_dsr(self):
        a, b, c = self.correr(3), self.correr(6), self.correr(10)
        ruta = self.dir / "T01-variantes.csv"
        self.assertEqual(a.ruta_registro, ruta)
        with open(ruta, newline="", encoding="utf-8") as f:
            filas = list(csv.reader(f))
        self.assertEqual(filas[0], bt.COLUMNAS_REGISTRO)
        self.assertEqual(len(filas) - 1, 3 * 3)  # 3 corridas x (completo + 2 segmentos)

        res = bt.sharpe_deflactado_de_registro("T01", dir_replicas=self.dir)
        self.assertEqual(res["segmento"], "dentro_muestra")
        self.assertEqual(res["n_pruebas"], 3)
        srs = [x.metricas["dentro_muestra"]["sharpe_periodo"] for x in (a, b, c)]
        self.assertAlmostEqual(res["varianza_sharpes_periodo"], statistics.variance(srs), places=12)
        mejor = max((a, b, c), key=lambda x: x.metricas["dentro_muestra"]["sharpe_periodo"])
        self.assertEqual(res["variante"], mejor.variante)
        x = mejor.metricas["dentro_muestra"]
        esperado = m.dsr_desde_estadisticos(x["sharpe_periodo"], x["n_periodos"], 3, statistics.variance(srs),
                                            x["asimetria"], x["curtosis"])
        self.assertAlmostEqual(res["dsr"], esperado, places=12)
        self.assertLessEqual(res["dsr"], res["psr_sin_deflactar"])
        self.assertEqual(res["umbral"], 0.95)

        # N y V explicitos (variantes probadas fuera del registro)
        explicito = bt.sharpe_deflactado_de_registro("T01", 50, 0.01, dir_replicas=self.dir)
        self.assertLess(explicito["dsr"], res["dsr"])
        with self.assertRaises(ValueError):
            bt.sharpe_deflactado_de_registro("T01", 2, dir_replicas=self.dir)  # no se permite subcontar

    def test_repetir_variante_no_infla_n_y_sensibilidad_no_cuenta(self):
        self.correr(3)
        self.correr(3)
        self.correr(6, es_prueba=False, nota="sensibilidad de costos")
        res = bt.sharpe_deflactado_de_registro(self.dir / "T01-variantes.csv")
        self.assertEqual(res["n_pruebas"], 1)
        self.assertEqual(res["sr0_periodo"], 0.0)
        self.assertAlmostEqual(res["dsr"], res["psr_sin_deflactar"], places=12)
        filas = bt.leer_registro("T01", dir_replicas=self.dir)
        self.assertEqual(len(filas), 9)
        self.assertEqual(filas[-1]["nota"], "sensibilidad de costos")

    def test_esquema_distinto_no_se_mezcla_e_id_seguro(self):
        (self.dir / "T02-variantes.csv").write_text("a,b\n1,2\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            bt.backtest_senal(self.datos, self.ef, bt.senal_comprar_y_mantener, id_replica="T02",
                              variante="bh", dir_replicas=self.dir)
        with self.assertRaises(ValueError):
            bt.backtest_senal(self.datos, self.ef, bt.senal_comprar_y_mantener, id_replica="../fuera",
                              variante="bh", dir_replicas=self.dir)


if __name__ == "__main__":
    unittest.main()
