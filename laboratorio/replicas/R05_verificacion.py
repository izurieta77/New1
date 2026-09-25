#!/usr/bin/env python3
"""R05 - verificacion independiente del motor (no registra nada).

Reproduce desde la raiz del repo:  python3 laboratorio/replicas/R05_verificacion.py
Requiere haber corrido R05.py (lee R05-variantes.csv para comparar).

Recalcula SIN herramientas/backtest.py los rendimientos netos de las 7 variantes de prueba, de
comprar y mantener y de la SMA10, con costos por defecto:
  - pesos: R05.pesos_directos (indices explicitos de entrenamiento) o la regla SMA10 escrita aqui;
  - costo_t = |w_t - w_pre_t| * (comision + spread), w_pre_t = w_{t-1}(1+ra_{t-1})/(1+rb_{t-1}),
    w_pre del primer periodo = 0 (entrada pagada);
  - r_neto = rb - costo * (1 + rb), rb = w ra + (1 - w) rf.
Compara Sharpe, CAGR y MDD por segmento con la ultima corrida registrada de cada variante.
Ademas reporta las fechas de pico y valle de la caida maxima (dato que el CSV no guarda).
"""
from __future__ import annotations

import math
import statistics
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
for p in (str(RAIZ), str(Path(__file__).resolve().parent)):
    if p not in sys.path:
        sys.path.insert(0, p)

import R05  # noqa: E402
from herramientas import backtest as bt  # noqa: E402
from herramientas import metricas as m  # noqa: E402

COSTO = bt.COMISION_GBM_POR_LADO + bt.SPREAD_POR_LADO["liquido"]


def simular(D: dict, fechas_eval: list, pesos: list) -> list:
    ra = {t: r for t, r in D["mercado"]}
    rf = {t: r for t, r in D["rf"]}
    salida, w_prev, ra_prev, rb_prev = [], 0.0, None, None
    for k, (t, w) in enumerate(zip(fechas_eval, pesos)):
        w_pre = w_prev if k == 0 else w_prev * (1 + ra_prev) / (1 + rb_prev)
        c = abs(w - w_pre) * COSTO
        rb = w * ra[t] + (1 - w) * rf[t]
        salida.append((t, rb - c * (1 + rb), rf[t]))
        w_prev, ra_prev, rb_prev = w, ra[t], rb
    return salida


def pesos_sma10(D: dict, fechas_eval: list) -> list:
    todas = D["fechas"]
    ra = {t: r for t, r in D["mercado"]}
    nivel, niveles = 1.0, {}
    for t in todas:
        nivel *= 1 + ra[t]
        niveles[t] = nivel
    pos = {t: i for i, t in enumerate(todas)}
    out = []
    for t in fechas_eval:
        ult = [niveles[todas[j]] for j in range(pos[t] - 10, pos[t])]
        out.append(1.0 if ult[-1] > statistics.fmean(ult) else 0.0)
    return out


def metricas(serie: list, f0: date, f1: date, base: date) -> dict:
    tramo = [x for x in serie if f0 <= x[0] <= f1]
    idx = serie.index(tramo[0])
    inicio = base if idx == 0 else serie[idx - 1][0]
    curva = [(inicio, 1.0)]
    for t, rn, _ in tramo:
        curva.append((t, curva[-1][1] * (1 + rn)))
    mdd = m.max_drawdown(curva)
    return {"sharpe": m.sharpe([rn for _, rn, _ in tramo], rf=[r for _, _, r in tramo], periodos_por_anio=12),
            "cagr": m.cagr(curva), "mdd": mdd["valor"], "pico": mdd["fecha_pico"], "valle": mdd["fecha_valle"],
            "recuperacion": mdd["fecha_recuperacion"]}


def main() -> None:
    D = R05.cargar()
    registro = bt.leer_registro(R05.ID)
    ultimas: dict = {}
    for fila in registro:
        ultimas[(fila["variante"], fila["segmento"])] = fila  # la ultima corrida de cada variante
    fechas_eval = [t for t in D["fechas"] if t >= R05.fm(1936, 8)]
    base = R05.fm(1936, 7)
    casos = [(n, R05.pesos_directos(D, fechas_eval, "gestionada", c, f, tp)) for n, f, tp, c in R05.VARIANTES]
    casos += [("comprar_y_mantener", [1.0] * len(fechas_eval)), ("sma10", pesos_sma10(D, fechas_eval))]
    print("| variante | segmento | Sharpe indep. | dif. vs CSV | CAGR indep. | dif. vs CSV | MDD indep. | dif. vs CSV |"
          " pico | valle | recuperación |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    peor = 0.0
    for nombre, pesos in casos:
        serie = simular(D, fechas_eval, pesos)
        for seg in ("completo", "dentro_muestra", "fuera_muestra"):
            x = metricas(serie, *R05.SEG_FECHAS[seg], base)
            fila = ultimas[(nombre, seg)]
            difs = [x["sharpe"] - fila["sharpe"], x["cagr"] - fila["cagr"], x["mdd"] - fila["mdd"]]
            peor = max(peor, max(abs(v) for v in difs))
            print(f"| {nombre} | {seg} | {x['sharpe']:.4f} | {difs[0]:.1e} | {x['cagr']:.4f} | {difs[1]:.1e} | "
                  f"{x['mdd']:.4f} | {difs[2]:.1e} | {x['pico']} | {x['valle']} | {x['recuperacion']} |")
    print(f"\nDiferencia máxima absoluta contra el registro: {peor:.2e}")


if __name__ == "__main__":
    main()
