"""Ficha 2026-10-02: ¿un pico de riesgo geopolítico (GPR de Caldara-Iacoviello) predice el
rendimiento o la volatilidad siguientes del mercado de EUA?

Datos: GPR mensual (.dta oficial, matteoiacoviello.com) y French F-F_Research_Data_Factors
(mensual y diario) para el exceso de mercado. 1985-01 en adelante (inicio del GPR "reciente").
1. Regresión del exceso del mes siguiente sobre el choque de GPR (log GPR - media log de 12 meses previos),
   con error estándar Newey-West (3 rezagos).
2. Estudio de eventos: meses de choque (top 5% del choque); exceso a 1, 3 y 12 meses y
   volatilidad realizada del mes siguiente contra el resto, con p de permutación (5,000).
Solo stdlib + herramientas. Semilla 20261002.
"""
import math
import random
import statistics as st
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from herramientas import datos_historicos as dh, geopolitica as gp  # noqa: E402

random.seed(20261002)


def ols_nw(y, x, lags=3):
    n = len(y)
    mx, my = st.mean(x), st.mean(y)
    sxx = sum((a - mx) ** 2 for a in x)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sxx
    a0 = my - b * mx
    u = [c - a0 - b * a for a, c in zip(x, y)]
    z = [(a - mx) * e for a, e in zip(x, u)]
    s = sum(v * v for v in z)
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        s += 2 * w * sum(z[t] * z[t - L] for t in range(L, n))
    se = math.sqrt(s) / sxx
    return b, b / se


def main():
    registro = []
    g = gp.descargar_gpr(cache_horas=24, registro=registro)
    filas = gp.serie_mensual_gpr(g["mensual"])
    gpr = {(f["fecha"].year, f["fecha"].month): f["GPR"] for f in filas if f.get("GPR")}
    tm = dh.french("F-F_Research_Data_Factors", "mensual")
    exc = {(f.year, f.month): e for f, e in zip(tm["fechas"], tm["columnas"]["Mkt-RF"]) if e is not None}
    td = dh.french("F-F_Research_Data_Factors_daily", "diaria")
    vol = {}
    for f, e in zip(td["fechas"], td["columnas"]["Mkt-RF"]):
        if e is not None:
            vol.setdefault((f.year, f.month), []).append(e)
    vol = {k: st.pstdev(v) * math.sqrt(252) for k, v in vol.items() if len(v) > 10}

    meses = sorted(k for k in gpr if k >= (1985, 1))
    def sig(k, h=1):
        y, m = k
        m += h
        y += (m - 1) // 12
        m = (m - 1) % 12 + 1
        return (y, m)

    obs = []
    for i, k in enumerate(meses):
        if i < 12:
            continue
        base = st.mean(math.log(gpr[j]) for j in meses[i - 12:i])
        choque = math.log(gpr[k]) - base
        r1 = exc.get(sig(k, 1))
        if r1 is None:
            continue
        r3 = [exc.get(sig(k, h)) for h in (1, 2, 3)]
        r12 = [exc.get(sig(k, h)) for h in range(1, 13)]
        obs.append({"k": k, "choque": choque, "r0": exc.get(k), "r1": r1,
                    "r3": math.prod(1 + x for x in r3) - 1 if None not in r3 else None,
                    "r12": math.prod(1 + x for x in r12) - 1 if None not in r12 else None,
                    "v1": vol.get(sig(k, 1)), "v0": vol.get(k)})
    print(f"Muestra: {obs[0]['k']}..{obs[-1]['k']} n={len(obs)} meses; último GPR {meses[-1]}={gpr[meses[-1]]:.1f}")

    b, t = ols_nw([o["r1"] for o in obs], [o["choque"] for o in obs])
    print(f"\n1. Exceso del mes siguiente sobre choque GPR: beta {100*b:.3f} pp por 1.0 de log-choque, t(NW3) {t:.2f}")
    vv = [o for o in obs if o["v1"] and o["v0"]]
    b2, t2 = ols_nw([o["v1"] for o in vv], [o["choque"] for o in vv])
    print(f"   Volatilidad realizada del mes siguiente sobre choque: beta {100*b2:.2f} pp, t(NW3) {t2:.2f}")

    umbral = sorted(o["choque"] for o in obs)[int(0.95 * len(obs))]
    ev = [o for o in obs if o["choque"] >= umbral]
    print(f"\n2. Meses de choque (top 5%, log-choque >= {umbral:.2f}): n={len(ev)}")
    print("   " + ", ".join(f"{y}-{m:02d}" for (y, m) in [o['k'] for o in ev]))
    for campo, nombre in (("r0", "mismo mes"), ("r1", "+1 mes"), ("r3", "+3 meses"), ("r12", "+12 meses"), ("v1", "vol +1 mes")):
        e = [o[campo] for o in ev if o[campo] is not None]
        todo = [o[campo] for o in obs if o[campo] is not None]
        dif = st.mean(e) - st.mean(todo)
        cnt = 0
        for _ in range(5000):
            muestra = random.sample(todo, len(e))
            if abs(st.mean(muestra) - st.mean(todo)) >= abs(dif):
                cnt += 1
        print(f"   {nombre:10s}: eventos {100*st.mean(e):6.2f}% vs todos {100*st.mean(todo):6.2f}% "
              f"(dif {100*dif:+.2f} pp, p perm {cnt/5000:.3f}, n={len(e)})")


if __name__ == "__main__":
    main()
