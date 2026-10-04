"""Ficha 2026-10-03: prima de volatilidad (VIX contra volatilidad realizada futura) y el umbral VIX 25.

1. Replica de forma independiente la tabla del cap. 05 §2.5: VIX en t contra la volatilidad realizada
   (anualizada, raiz(252) x desviacion de rendimientos log, sin restar media) de los 21 dias habiles t+1..t+21.
2. Por tramos de VIX (<15, 15-20, 20-25, 25-30, 30-40, >=40): RV futura, VIX-RV, % VIX>RV,
   rendimiento futuro del S&P a 21 dias y drag de un 3x diario implicito por la RV (9*RV^2/2, anualizado).
3. Regla del filtro: rendimiento y RV futura cuando VIX>=25 contra VIX<25.

Solo stdlib + herramientas. Uso: python3 conocimiento/fichas/codigo/2026-10-03-vrp-vix.py
"""
import math
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from herramientas import datos_historicos as dh  # noqa: E402

H = 21


def cargar():
    hv, hg = dh.yahoo_historia("^VIX"), dh.yahoo_historia("^GSPC")
    v, g = dict(zip(hv["fechas"], hv["cierres"])), dict(zip(hg["fechas"], hg["cierres"]))
    f = sorted(set(v) & set(g))
    f = [d for d in f if d.year >= 1990]
    return f, [v[d] for d in f], [g[d] for d in f]


def main():
    f, vix, px = cargar()
    r = [math.log(px[i] / px[i - 1]) for i in range(1, len(px))]  # r[i-1] es el rendimiento del dia i
    filas = []
    for i in range(1, len(f) - H):
        fut = r[i:i + H]  # dias i+1..i+H
        rv = 100 * math.sqrt(252 * sum(x * x for x in fut) / H)
        ret = px[i + H] / px[i] - 1
        filas.append((f[i], vix[i], rv, ret))
    print(f"muestra {filas[0][0]}..{filas[-1][0]} n={len(filas)} dias (horizonte {H})")

    print("\n== 1. Replica de la tabla del cap. 05 ==")
    for nombre, a, b in (("1990-2026", 1990, 2100), ("1990-1999", 1990, 1999), ("2000-2009", 2000, 2009),
                         ("2010-2019", 2010, 2019), ("2020-2026", 2020, 2100)):
        x = [t for t in filas if a <= t[0].year <= b]
        gap = [t[1] - t[2] for t in x]
        peor = min(x, key=lambda t: t[1] - t[2])
        var = st.mean(t[1] ** 2 - t[2] ** 2 for t in x) / 100
        print(f"{nombre}: n={len(x)} VIX {st.mean(t[1] for t in x):.2f} RV {st.mean(t[2] for t in x):.2f} "
              f"VIX-RV {st.mean(gap):+.2f} %VIX>RV {100*sum(g > 0 for g in gap)/len(x):.1f} "
              f"peor {peor[1]-peor[2]:+.1f} ({peor[0]}) (VIX2-RV2)/100 {var:.2f}")

    print("\n== 2. Por tramo de VIX ==")
    tramos = [(0, 15), (15, 20), (20, 25), (25, 30), (30, 40), (40, 999)]
    for a, b in tramos:
        x = [t for t in filas if a <= t[1] < b]
        rets = sorted(t[3] for t in x)
        rv = st.mean(t[2] for t in x)
        drag3 = 3 * st.mean((t[2] / 100) ** 2 for t in x)  # (L^2-L)/2*sigma^2 con L=3: costo extra contra 3x el log del indice
        print(f"VIX {a}-{b}: n={len(x)} ({100*len(x)/len(filas):.1f}%) RV fut {rv:.1f} VIX-RV {st.mean(t[1]-t[2] for t in x):+.1f} "
              f"%VIX>RV {100*sum(t[1] > t[2] for t in x)/len(x):.0f} | S&P 21d media {100*st.mean(rets):+.2f}% "
              f"p10 {100*rets[len(rets)//10]:+.1f}% %neg {100*sum(q < 0 for q in rets)/len(rets):.0f} "
              f"| drag 3x anual {100*drag3:.1f} pp")

    print("\n== 3. Umbral del filtro: VIX>=25 contra VIX<25 ==")
    for nombre, cond in (("VIX<25", lambda t: t[1] < 25), ("VIX>=25", lambda t: t[1] >= 25)):
        x = [t for t in filas if cond(t)]
        rets = [t[3] for t in x]
        # log(1+3R) ~ 3 log(1+R) - 3 R^2 por dia => en 21 dias: 3 log(1+ret) - 3 * RV^2 * H/252 (sin costos ni rf)
        r3 = [3 * math.log1p(t[3]) - 3 * (t[2] / 100) ** 2 * H / 252 for t in x]
        print(f"{nombre}: n={len(x)} RV fut {st.mean(t[2] for t in x):.1f} S&P 21d media {100*st.mean(rets):+.2f}% "
              f"sd {100*st.pstdev(rets):.1f}% | 3x log 21d media {100*st.mean(r3):+.2f}% sd {100*st.pstdev(r3):.1f}% "
              f"razon media/sd {st.mean(r3)/st.pstdev(r3):.3f}")
    print("\n== 4. Dentro del filtro de tendencia (^GSPC > SMA200 x 1.03 en t), VIX>=25 contra <25 ==")
    sma = {}
    for i in range(199, len(px)):
        sma[f[i]] = sum(px[i - 199:i + 1]) / 200
    pos = {d: i for i, d in enumerate(f)}
    for nombre, cond in (("tendencia y VIX<25", lambda t: t[1] < 25), ("tendencia y VIX>=25", lambda t: t[1] >= 25)):
        x = [t for t in filas if t[0] in sma and px[pos[t[0]]] > 1.03 * sma[t[0]] and cond(t)]
        if not x:
            continue
        r3 = [3 * math.log1p(t[3]) - 3 * (t[2] / 100) ** 2 * H / 252 for t in x]
        nosolap = x[::H]
        print(f"{nombre}: n={len(x)} (~{len(nosolap)} ventanas sin traslape) RV fut {st.mean(t[2] for t in x):.1f} "
              f"S&P 21d media {100*st.mean(t[3] for t in x):+.2f}% %neg {100*sum(t[3] < 0 for t in x)/len(x):.0f} "
              f"| 3x log 21d media {100*st.mean(r3):+.2f}% p10 {100*sorted(r3)[len(r3)//10]:+.1f}%")
    print("\n== 5. Sin traslape (una observacion cada 21 dias), VIX>=25 contra <25 ==")
    for off in (0, 7, 14):
        sub = filas[off::H]
        a = [t[3] for t in sub if t[1] < 25]
        b = [t[3] for t in sub if t[1] >= 25]
        se = math.sqrt(st.variance(a) / len(a) + st.variance(b) / len(b))
        print(f"desfase {off}: n<25={len(a)} n>=25={len(b)} media {100*st.mean(a):+.2f}% vs {100*st.mean(b):+.2f}% "
              f"dif {100*(st.mean(b)-st.mean(a)):+.2f} pp t={(st.mean(b)-st.mean(a))/se:.2f}")
    # Persistencia: correlacion VIX con RV futura
    xs, ys = [t[1] for t in filas], [t[2] for t in filas]
    print(f"\ncorrelacion VIX(t) vs RV(t+1..t+21) = {st.correlation(xs, ys):.3f}; "
          f"regresion RV = a + b VIX: b = {st.covariance(xs, ys)/st.variance(xs):.3f}, "
          f"a = {st.mean(ys)-st.covariance(xs, ys)/st.variance(xs)*st.mean(xs):.2f}")


if __name__ == "__main__":
    main()
