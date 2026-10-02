"""Ficha 2026-10-01 (trabajo continuo): ¿qué serie debe dar la señal del filtro de 200 días?

Compara, para un 3x diario sintético filtrado (S&P y Nasdaq-100), la señal calculada sobre:
  (a) el índice de precio (^GSPC / ^NDX), (b) el ETF con dividendos (SPY / QQQ, cierre ajustado),
  (c) el precio del ETF sin ajustar (SPY / QQQ, cierre),
sin banda y con banda ±3% (salida < SMA*0.97, entrada > SMA*1.03). Rezago de 1 día (señal al
cierre t, posición en t+1). Fuera del 3x: T-bill (FRED DTB3). Costo: gasto 0.91%/año, financiamiento
2×rf, y 0.29% por cambio de posición (GBM).
Solo stdlib + herramientas. Uso: python3 conocimiento/fichas/codigo/2026-10-01-serie-senal-filtro.py
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from herramientas import datos, datos_historicos as dh  # noqa: E402


def historia(ticker):
    h = dh.yahoo_historia(ticker)
    return dict(zip(h["fechas"], h["precios"])), dict(zip(h["fechas"], h["cierres"]))


def senal(serie, fechas, banda):
    out, dentro, ventana = {}, False, []
    for f in fechas:
        p = serie[f]
        ventana.append(p)
        if len(ventana) > 200:
            ventana.pop(0)
        if len(ventana) < 200:
            out[f] = None
            continue
        sma = sum(ventana) / 200
        if banda == 0:
            dentro = p > sma
        else:
            if dentro and p < sma * (1 - banda):
                dentro = False
            elif not dentro and p > sma * (1 + banda):
                dentro = True
        out[f] = dentro
    return out


def simula(fechas, r_etf, s, rf):
    v, pico, mdd, cambios, prev = 1.0, 1.0, 0.0, 0, None
    for i in range(1, len(fechas)):
        f0, f1 = fechas[i - 1], fechas[i]
        estado = s[f0]
        if estado is None:
            continue
        rfd = rf.get(f1, 0.0)
        if prev is not None and estado != prev:
            v *= 1 - 0.0029
            cambios += 1
        prev = estado
        r = 3 * r_etf[f1] - 2 * rfd - 0.0091 / 252 if estado else rfd
        v *= 1 + r
        pico = max(pico, v)
        mdd = max(mdd, 1 - v / pico)
    return v, mdd, cambios


def main():
    rf_serie = datos.fred_serie("DTB3")
    rf = {}
    ult = 0.0
    for f, x in rf_serie:
        ult = x / 100 / 252
        rf[f] = ult
    for nombre, indice, etf in (("S&P 500", "^GSPC", "SPY"), ("Nasdaq-100", "^NDX", "QQQ")):
        idx, _ = historia(indice)
        adj, crudo = historia(etf)
        fechas = sorted(set(idx) & set(adj) & set(crudo))
        rf_f, ultimo = {}, 0.0
        for f in fechas:
            ultimo = rf.get(f, ultimo)
            rf_f[f] = ultimo
        r_etf = {fechas[i]: adj[fechas[i]] / adj[fechas[i - 1]] - 1 for i in range(1, len(fechas))}
        anios = (fechas[-1] - fechas[0]).days / 365.25
        print(f"\n== {nombre}: {fechas[0]}..{fechas[-1]} ({anios:.1f} años) ==")
        series = {"índice de precio": idx, "ETF ajustado (TR)": adj, "ETF sin ajustar": crudo}
        for banda in (0.0, 0.03):
            sen = {k: senal(v, fechas, banda) for k, v in series.items()}
            base = sen["índice de precio"]
            for k, s in sen.items():
                v, mdd, cambios = simula(fechas, r_etf, s, rf_f)
                cagr = v ** (1 / anios) - 1
                difer = sum(1 for f in fechas if s[f] is not None and base[f] is not None and s[f] != base[f])
                print(f"banda {banda:.0%} | {k:18s} | CAGR {100*cagr:6.2f}% | MDD {100*mdd:5.1f}% | cambios {cambios:4d} "
                      f"({cambios/anios:4.1f}/año) | días distintos vs índice {difer}")
        bh = math.prod(1 + r_etf[f] for f in fechas[1:]) ** (1 / anios) - 1
        print(f"referencia: {etf} comprar y mantener 1x CAGR {100*bh:.2f}%")


if __name__ == "__main__":
    main()
