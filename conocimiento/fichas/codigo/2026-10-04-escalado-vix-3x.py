"""Ficha 2026-10-04: sleeve 3x diario con banda SMA200 +-3%, con o sin interruptor VIX<25,
contra escalado continuo por VIX (w = min(1, (K/VIX)^2)).

Datos: French diario (Mkt-RF + RF, con dividendos) para el rendimiento y el financiamiento;
Yahoo ^GSPC (cierre) para la SMA200 y ^VIX para la senal. Senal al cierre de t, aplicada en t+1.
3x sintetico: r3 = 3*(Mkt-RF) + RF - gasto (0.91%/año) - diferencial de swap (0.50%/año sobre 2x prestado).
Fuera del 3x el sleeve gana RF. Costo de cambio de exposicion: 0.10% por unidad de peso movida.
Sin stop por precio (limite declarado). Uso: python3 conocimiento/fichas/codigo/2026-10-04-escalado-vix-3x.py
"""
import math
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from herramientas import datos_historicos as dh  # noqa: E402

GASTO, SWAP, COSTO = 0.0091, 0.0050, 0.0010


def cargar():
    fr = dh.french("F-F_Research_Data_Factors_daily", "diaria")
    ff = {f: (e, r) for f, e, r in zip(fr["fechas"], fr["columnas"]["Mkt-RF"], fr["columnas"]["RF"])
          if e is not None and r is not None}
    hv, hg = dh.yahoo_historia("^VIX"), dh.yahoo_historia("^GSPC")
    vix = dict(zip(hv["fechas"], hv["cierres"]))
    gs = dict(zip(hg["fechas"], hg["cierres"]))
    todas = sorted(set(gs) & set(vix))
    # SMA200 de ^GSPC sobre sus propios dias
    gf = sorted(gs)
    sma = {}
    for i in range(199, len(gf)):
        sma[gf[i]] = sum(gs[d] for d in gf[i - 199:i + 1]) / 200
    dias = [d for d in todas if d in ff and d in sma and d.year >= 1990]
    return dias, ff, vix, gs, sma, fr["sha256"][:12]


def simular(dias, ff, vix, gs, sma, regla):
    v, pico, mdd, w, invert, giros = 1.0, 1.0, 0.0, 0.0, 0.0, 0.0
    tendencia = False
    logs = []
    for i in range(1, len(dias)):
        d0, d1 = dias[i - 1], dias[i]
        # senal con datos de d0
        x = gs[d0] / sma[d0]
        if not tendencia and x > 1.03:
            tendencia = True
        elif tendencia and x < 0.97:
            tendencia = False
        nuevo = regla(tendencia, vix[d0])
        giros += abs(nuevo - w)
        costo = COSTO * abs(nuevo - w)
        w = nuevo
        e, rf = ff[d1]
        r3 = 3 * e + rf - (GASTO + 2 * SWAP) / 252
        r = w * r3 + (1 - w) * rf - costo
        v *= 1 + r
        logs.append(math.log1p(r))
        pico = max(pico, v)
        mdd = max(mdd, 1 - v / pico)
        invert += w
    anios = len(logs) / 252
    g = math.exp(sum(logs) / anios) - 1
    sd = st.pstdev(logs) * math.sqrt(252)
    return g, sd, mdd, invert / len(logs), giros / anios


REGLAS = {
    "3x siempre": lambda t, vx: 1.0,
    "banda SMA200 sola": lambda t, vx: 1.0 if t else 0.0,
    "banda + VIX<25 (vigente)": lambda t, vx: 1.0 if t and vx < 25 else 0.0,
    "banda + escala K=18": lambda t, vx: min(1.0, (18 / vx) ** 2) if t else 0.0,
    "banda + escala K=22": lambda t, vx: min(1.0, (22 / vx) ** 2) if t else 0.0,
    "escala K=18 sin banda": lambda t, vx: min(1.0, (18 / vx) ** 2),
}


def main():
    dias, ff, vix, gs, sma, sha = cargar()
    print(f"French diario sha {sha}; muestra {dias[0]}..{dias[-1]} ({len(dias)} dias)")
    for etiqueta, a, b in (("1990-2026", 1990, 2100), ("1990-2007", 1990, 2007), ("2008-2026", 2008, 2100)):
        sub = [d for d in dias if a <= d.year <= b]
        print(f"\n== {etiqueta} ({sub[0]}..{sub[-1]}) ==")
        print("regla | CAGR | sigma | MDD | exposicion media | giro/año")
        for nombre, regla in REGLAS.items():
            g, sd, mdd, inv, gir = simular(sub, ff, vix, gs, sma, regla)
            print(f"{nombre} | {100*g:.2f}% | {100*sd:.1f}% | {100*mdd:.1f}% | {inv:.2f} | {gir:.1f}")
    # 1x de referencia
    sub = dias
    v, logs = 1.0, []
    for d in sub[1:]:
        e, rf = ff[d]
        logs.append(math.log1p(e + rf))
    print(f"\nreferencia 1x mercado 1990-2026: CAGR {100*(math.exp(sum(logs)/(len(logs)/252))-1):.2f}%")


if __name__ == "__main__":
    main()
