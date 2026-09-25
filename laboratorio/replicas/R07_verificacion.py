#!/usr/bin/env python3
"""R07 - verificacion independiente (no registra corridas en el CSV de variantes).

python3 laboratorio/replicas/R07_verificacion.py

1. Recalcula SIN el motor la curva neta de comprar y mantener, inv3 e inv_fuera12 (mismo modelo de
   costos: |w - w_pre| x (0.29% + 0.05%), deriva de pesos) y compara Sharpe, MDD y CAGR con el CSV.
2. Descriptivo post hoc (no pre-registrado): meses con S < 0 antes de 1966 y, para cada pico del NBER
   desde 1960, el minimo de S y la maxima probabilidad en tiempo real en los 24 meses previos al pico.
"""
from __future__ import annotations

import importlib.util
import math
import statistics
import sys
from datetime import date
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.argv = [sys.argv[0]]
spec = importlib.util.spec_from_file_location("r07", DIR / "R07.py")
r07 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r07)
from herramientas import backtest as bt  # noqa: E402

COSTO = bt.COMISION_GBM_POR_LADO + bt.SPREAD_POR_LADO["liquido"]


def curva_directa(regla, d, m0: int, m1: int):
    """Decisiones mensuales de m0 a m1 (indices de mes). regla(m_origen) -> w."""
    mer = {r07.mi_de(f): r for f, r in d["mercado"]}
    rf = {r07.mi_de(f): r for f, r in d["rf"]}
    w_prev, ra_prev, rb_prev = 0.0, None, None
    netos, exc = [], []
    for t in range(m0, m1 + 1):
        w = regla(t - 1)
        w_pre = w_prev if rb_prev is None else w_prev * (1 + ra_prev) / (1 + rb_prev)
        c = abs(w - w_pre) * COSTO
        rb = w * mer[t] + (1 - w) * rf[t]
        rn = (1 - c) * (1 + rb) - 1
        netos.append(rn)
        exc.append(rn - rf[t])
        w_prev, ra_prev, rb_prev = w, mer[t], rb
    return netos, exc


def metricas(netos, exc, meses_previos_para_curva: int = 0):
    nivel, maximo, mdd = 1.0, 1.0, 0.0
    for r in netos:
        nivel *= 1 + r
        maximo = max(maximo, nivel)
        mdd = min(mdd, nivel / maximo - 1)
    sharpe = statistics.fmean(exc) / statistics.stdev(exc) * math.sqrt(12)
    return sharpe, mdd


def main() -> None:
    d = r07.cargar()
    S = d["S"]
    filas = bt.leer_registro("R07", dir_replicas=DIR)
    print("## 1. Recalculo sin el motor (costos por defecto)\n")
    print("| Regla | Segmento | Sharpe directo | Sharpe CSV | MDD directo | MDD CSV |")
    print("|---|---|---|---|---|---|")
    reglas = {
        "comprar_y_mantener": lambda m: 1.0,
        "inv3": lambda m: 0.0 if all(S[m - j] < 0 for j in range(3)) else 1.0,
        "inv_fuera12": lambda m: 0.0 if any(S[m - j] < 0 for j in range(12)) else 1.0,
    }
    m_ini, m_corte, m_fin = r07.mi(1971, 1), r07.mi(1998, 2), r07.mi(2026, 7)
    for nombre, regla in reglas.items():
        netos, exc = curva_directa(regla, d, m_ini, m_fin)
        n_d = m_corte - m_ini + 1
        for seg, (a, b) in (("dentro_muestra", (0, n_d)), ("fuera_muestra", (n_d, len(netos)))):
            sh, mdd = metricas(netos[a:b], exc[a:b])
            csv = [f for f in filas if f["variante"] == nombre and f["segmento"] == seg
                   and f["comision_por_lado"] == bt.COMISION_GBM_POR_LADO
                   and f["spread_por_lado"] == bt.SPREAD_POR_LADO["liquido"] and "descuento" not in f["nota"]
                   and "MXN" not in f["nota"]]
            c = csv[-1]
            print(f"| {nombre} | {seg} | {sh:.4f} | {c['sharpe']:.4f} | {100 * mdd:.2f}% | {100 * c['mdd']:.2f}% |")
    print("\n## 2. Descriptivo post hoc (no pre-registrado)\n")
    neg_pre66 = [k for k in sorted(S) if k < r07.mi(1966, 1) and S[k] < 0]
    print(f"Meses con S < 0 de {r07.et(min(S))} a 1965-12: {len(neg_pre66)} "
          + ", ".join(f"{r07.et(k)} ({S[k]:+.2f})" for k in neg_pre66))
    giros, _ = r07.giros_con_disponibilidad(d["usrec"])
    picos = [k for f, t, k in giros if t == "pico" and k >= r07.mi(1957, 1)]
    print("\n| Pico NBER | mínimo de S en los 24 meses previos (mes) | meses con S < 0 en esos 24 | "
          "máx. P tiempo real en los 24 meses previos (mes) |")
    print("|---|---|---|---|")
    for p in picos:
        ventana = range(p - 24, p + 1)
        kmin = min(ventana, key=lambda k: S[k])
        nneg = sum(1 for k in ventana if S[k] < 0)
        if p - 24 >= r07.mi(1970, 1):
            ps = []
            for m in ventana:
                rec = r07.etiquetas_rt_en(r07.fdm(m), giros)
                pr, _, _ = r07.prob_origen(m, S, lambda k, rec=rec: 1 if k in rec else 0)
                ps.append((pr, m))
            pm, mm = max(ps)
            txt = f"{pm:.3f} ({r07.et(mm)})"
        else:
            txt = "no calculado (orígenes anteriores a 1970-01)"
        print(f"| {r07.et(p)} | {S[kmin]:+.2f} ({r07.et(kmin)}) | {nneg} | {txt} |")


if __name__ == "__main__":
    main()
