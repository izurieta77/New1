#!/usr/bin/env python3
"""R09 - comprobacion independiente (no registra corridas en el CSV de variantes).

python3 laboratorio/replicas/R09_verificacion.py

Recalcula SIN el motor ni las funciones de R09.py (mismos datos French, codigo propio):
1. Calendario: TOM con itertools.groupby y dia -1 por "la fecha siguiente cae en otro mes".
   Comprueba que todo mes calendario interior tiene 4 dias TOM y que coincide con R09.
2. delta (TOM - resto), delta_MX (TOM - otros -10..-2, +4..+10) y E medio (exceso de 4 dias por
   evento) en las ventanas clave, como diferencias de medias directas.
3. Curvas netas de US_tom_m1_p3 y comprar y mantener con el modelo de costos del motor
   (|w - w_pre| x (0.29% + 0.05%), deriva de pesos), CAGR, Sharpe y MDD por segmento, contra la
   ultima corrida registrada en R09-variantes.csv.
"""
from __future__ import annotations

import csv
import itertools
import math
import statistics
import sys
from datetime import date
from pathlib import Path

DIR = Path(__file__).resolve().parent
RAIZ = DIR.parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
from herramientas import datos_historicos as dh  # noqa: E402

CORTE = date(2008, 2, 29)
COSTO = 0.0025 * 1.16 + 0.0005
MIN_HISTORIA = 200


def main() -> None:
    ff = dh.french("F-F_Research_Data_Factors_daily", "diaria")
    fechas = ff["fechas"]
    mkt = [a + b for a, b in zip(ff["columnas"]["Mkt-RF"], ff["columnas"]["RF"])]
    rf = list(ff["columnas"]["RF"])
    n = len(fechas)

    # 1. calendario con groupby
    tom = [False] * n
    m1 = [False] * n
    otros = [False] * n
    for _, grupo in itertools.groupby(range(n), key=lambda i: (fechas[i].year, fechas[i].month)):
        g = list(grupo)
        for k, i in enumerate(g):
            desde_inicio, desde_fin = k + 1, len(g) - k
            tom[i] = desde_inicio <= 3 or desde_fin == 1
            m1[i] = desde_fin == 1
            otros[i] = (not tom[i]) and (2 <= desde_fin <= 10 or 4 <= desde_inicio <= 10)
    # dia -1 por la fecha siguiente (independiente de la cuenta por grupo)
    for i in range(n - 1):
        if m1[i] != (fechas[i + 1].month != fechas[i].month):
            raise AssertionError(f"dia -1 inconsistente en {fechas[i]}")
    conteo = {}
    for i in range(n):
        if tom[i]:
            conteo[(fechas[i].year, fechas[i].month)] = conteo.get((fechas[i].year, fechas[i].month), 0) + 1
    print(f"1. Meses con 4 dias TOM: {sum(1 for v in conteo.values() if v == 4)} de {len(conteo)}; "
          f"dias TOM totales {sum(tom)}")

    # 2. medias directas
    def delta(f0: date, f1: date, sub_otros: bool = False) -> tuple:
        a = [100 * mkt[i] for i in range(n) if f0 <= fechas[i] <= f1 and tom[i]]
        b = [100 * mkt[i] for i in range(n) if f0 <= fechas[i] <= f1 and not tom[i] and (otros[i] or not sub_otros)]
        return statistics.fmean(a) - statistics.fmean(b), len(a), len(b)

    for nombre, f0, f1, sub in (("delta dentro 1926-07..2008-02", date(1926, 7, 1), CORTE, False),
                                ("delta fuera 2008-03..2026-07", date(2008, 3, 1), date(2100, 1, 1), False),
                                ("delta_MX panel C 1926..2005", date(1926, 1, 1), date(2005, 12, 31), True),
                                ("delta_MX fuera", date(2008, 3, 1), date(2100, 1, 1), True)):
        d, na, nb = delta(f0, f1, sub)
        print(f"2. {nombre}: {d:.4f} pp (TOM n={na}, comparacion n={nb})")
    # E por evento: dia -1 del mes m y +1..+3 del mes m+1, fechado con el dia -1
    E = []
    for i in range(n - 3):
        if m1[i] and all(fechas[j].month != fechas[i].month for j in range(i + 1, i + 4)) \
                and all(tom[j] for j in range(i + 1, i + 4)):
            ct = math.prod(1 + mkt[j] for j in range(i, i + 4))
            cf = math.prod(1 + rf[j] for j in range(i, i + 4))
            E.append((fechas[i], 100 * (ct - cf)))
    for nombre, f0, f1 in (("dentro", date(1926, 7, 1), CORTE), ("fuera", date(2008, 3, 1), date(2100, 1, 1))):
        v = [e for f, e in E if f0 <= f <= f1]
        print(f"2. E medio {nombre}: {statistics.fmean(v):.4f}% (N={len(v)})")

    # 3. curvas netas
    def curva(regla) -> list:
        w_prev, ra_prev, rb_prev = 0.0, None, None
        salida = []
        for t in range(MIN_HISTORIA, n):
            w = 1.0 if regla(t) else 0.0
            w_pre = w_prev if rb_prev is None else w_prev * (1 + ra_prev) / (1 + rb_prev)
            c = abs(w - w_pre) * COSTO
            rb = w * mkt[t] + (1 - w) * rf[t]
            salida.append((fechas[t], (1 - c) * (1 + rb) - 1, rf[t]))
            w_prev, ra_prev, rb_prev = w, mkt[t], rb
        return salida

    def metricas(tramo: list, fecha_ini: date) -> dict:
        nivel, maximo, mdd = 1.0, 1.0, 0.0
        for _, r, _ in tramo:
            nivel *= 1 + r
            maximo = max(maximo, nivel)
            mdd = min(mdd, nivel / maximo - 1)
        anios = (tramo[-1][0] - fecha_ini).days / 365.25
        ex = [r - x for _, r, x in tramo]
        return {"cagr": nivel ** (1 / anios) - 1, "sharpe": statistics.fmean(ex) / statistics.stdev(ex) * math.sqrt(252),
                "mdd": mdd}

    filas = list(csv.DictReader(open(DIR / "R09-variantes.csv", encoding="utf-8")))
    peor = 0.0
    for variante, regla in (("US_tom_m1_p3", lambda t: tom[t]), ("US_ref_comprar_mantener", lambda t: True)):
        c = curva(regla)
        for seg in ("dentro_muestra", "fuera_muestra"):
            if seg == "dentro_muestra":
                tramo = [x for x in c if x[0] <= CORTE]
                f_ini = fechas[MIN_HISTORIA - 1]
            else:
                tramo = [x for x in c if x[0] > CORTE]
                f_ini = max(x[0] for x in c if x[0] <= CORTE)
            mine = metricas(tramo, f_ini)
            reg = [f for f in filas if f["variante"] == variante and f["segmento"] == seg
                   and float(f["spread_por_lado"]) == 0.0005][-1]
            difs = {k: abs(mine[k] - float(reg[k])) for k in ("cagr", "sharpe", "mdd")}
            peor = max(peor, *difs.values())
            print(f"3. {variante} [{seg}] directo: CAGR {mine['cagr']:.6f}, Sharpe {mine['sharpe']:.6f}, MDD {mine['mdd']:.6f}; "
                  f"CSV: {float(reg['cagr']):.6f}, {float(reg['sharpe']):.6f}, {float(reg['mdd']):.6f}; "
                  f"dif max {max(difs.values()):.2e}")
    print(f"Diferencia maxima contra el CSV: {peor:.2e}")


if __name__ == "__main__":
    main()
