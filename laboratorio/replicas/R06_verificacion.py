"""R06 - verificacion independiente del motor (no es una variante nueva; no registra nada).

Recalcula sin herramientas/backtest.py cuatro corridas de R06 (bh_L1, bh_L3, sma200_L2 y
sma200_L3|rezago1, implementacion realista con costos GBM por defecto) sobre el mismo zip
congelado de French, y compara CAGR y MDD de dentro_muestra y fuera_muestra con R06-resultados.json.
Uso (desde la raiz del repo): python3 laboratorio/replicas/R06_verificacion.py
"""
import io
import json
import math
import sys
import zipfile
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent.parent))
from herramientas import datos_historicos as dh  # noqa: E402

GA, COSTO = 0.009, 0.0029 + 0.0005
INICIO, CORTE, FIN = date(1928, 10, 1), date(2015, 10, 31), date(2026, 7, 31)

with zipfile.ZipFile(io.BytesIO((AQUI / "R06-datos/202607/F-F_Research_Data_Factors_daily_CSV.zip").read_bytes())) as z:
    t = dh.tabla_french(z.read(z.namelist()[0]).decode("utf-8"), "diaria")
filas = [(f, a + b, b) for f, a, b in zip(t["fechas"], t["columnas"]["Mkt-RF"], t["columnas"]["RF"]) if f <= FIN]

nivel, niveles, previa, letf = 1.0, [], None, {1: [], 2: [], 3: []}
for f, m, rf in filas:
    dd = (f - previa).days if previa else 1
    previa = f
    nivel *= 1 + m
    niveles.append(nivel)
    for L in (1, 2, 3):
        letf[L].append(L * m - (L - 1) * rf - (GA if L > 1 else 0.0) * dd / 365.25)


def senal(t_, rezago):
    """Exposicion para el dia t_: nivel de t_-1-rezago contra su media de 200 dias."""
    j = t_ - 1 - rezago
    return 1.0 if niveles[j] > sum(niveles[j - 199:j + 1]) / 200 else 0.0


def correr(L, regla, rezago=0):
    i0 = next(i for i, x in enumerate(filas) if x[0] >= INICIO)
    w_prev, salida = 0.0, []
    for i in range(i0, len(filas)):
        w = 1.0 if regla == "bh" else senal(i, rezago)
        c = abs(w - w_prev) * COSTO  # con w en {0, 1} la deriva no cambia el peso
        rb = w * letf[L][i] + (1 - w) * filas[i][2]
        salida.append((filas[i][0], rb - c * (1 + rb)))
        w_prev = w
    return filas[i0 - 1][0], salida


def metricas(f0, serie, d0, d1):
    tramo = [(f, r) for f, r in serie if d0 < f <= d1]
    base = f0 if d0 < serie[0][0] else max(f for f, _ in serie if f <= d0)
    v, pico, mdd = 1.0, 1.0, 0.0
    for _, r in tramo:
        v *= 1 + r
        pico = max(pico, v)
        mdd = min(mdd, v / pico - 1)
    anios = (tramo[-1][0] - base).days / 365.25
    return v ** (1 / anios) - 1, mdd


res = json.loads((AQUI / "R06-resultados.json").read_text(encoding="utf-8"))["metricas"]
peor = 0.0
for nombre, L, regla, rez in (("bh_L1", 1, "bh", 0), ("bh_L3", 3, "bh", 0), ("sma200_L2", 2, "sma", 0),
                              ("sma200_L3|rezago1", 3, "sma", 1)):
    f0, serie = correr(L, regla, rez)
    for seg, (d0, d1) in (("dentro_muestra", (date(1900, 1, 1), CORTE)), ("fuera_muestra", (CORTE, FIN))):
        cagr, mdd = metricas(f0, serie, d0, d1)
        m = res[nombre][seg]
        dif = max(abs(cagr - m["cagr"]), abs(mdd - m["mdd"]))
        peor = max(peor, dif)
        print(f"{nombre:<20} {seg:<15} CAGR {cagr:.6%} (motor {m['cagr']:.6%})  MDD {mdd:.6%} (motor {m['mdd']:.6%})  dif max {dif:.2e}")
print(f"Diferencia maxima contra el motor: {peor:.2e}")
