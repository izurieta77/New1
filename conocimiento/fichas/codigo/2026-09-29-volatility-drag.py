"""Ficha 2026-09-29: volatility drag con datos de French y ETFs reales.

Comprueba:
1. G ~ A - sigma^2/2 con el mercado de EUA (French, Mkt-RF + RF), mensual y anual.
2. El drag observado por decada contra sigma^2/2.
3. Apalancamiento diario sintetico L en {1, 1.5, 2, 3, 4} (French diario):
   g(L) observado contra rf + L*mu - L^2*sigma^2/2, y L* = mu/sigma^2.
4. ETF reales: UPRO (3x S&P) contra SPY, crecimiento observado contra la formula.

Solo stdlib + herramientas del repo. Uso: python3 conocimiento/fichas/codigo/2026-09-29-volatility-drag.py
"""
import math
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from herramientas import datos, datos_historicos as dh  # noqa: E402


def geo(rs):
    """Media geometrica por periodo."""
    return math.exp(sum(math.log1p(r) for r in rs) / len(rs)) - 1


def resumen_mensual(rs, etiqueta):
    a, s, g = st.mean(rs), st.pstdev(rs), geo(rs)
    a_an, var_an = 12 * a, 12 * s * s
    g_an = (1 + g) ** 12 - 1
    # Comparacion en tasas continuas (log): ln(1+G) ~ A - s^2/2 exacto a 2o orden por periodo
    g_log = 12 * math.log1p(g)
    aprox_log = 12 * (a - s * s / 2)
    print(f"{etiqueta}: n={len(rs)} meses | A={a_an:.4f}/año (x12) sigma={math.sqrt(var_an):.4f} "
          f"| G compuesto={g_an:.4f} | 12*ln(1+G)={g_log:.4f} vs 12*(A-s²/2)={aprox_log:.4f} "
          f"(error {100*(g_log-aprox_log):+.2f} pp) | drag x12 obs={100*(a_an-g_log):.2f} pp vs s²/2={100*var_an/2:.2f} pp")
    return a_an, math.sqrt(var_an), g_an


def main():
    print("== 1. Mercado EUA (French F-F_Research_Data_Factors) ==")
    tm = dh.french("F-F_Research_Data_Factors", "mensual")
    serie_m = dh.rendimiento_mercado_french(tm)
    print(f"archivo {tm['archivo']} sha256 {tm['sha256'][:12]} {serie_m[0][0]}..{serie_m[-1][0]}")
    rs = [r for _, r in serie_m]
    resumen_mensual(rs, "Mensual completo")

    ta = dh.french("F-F_Research_Data_Factors", "anual")
    ra = dh.rendimiento_mercado_french(ta)
    # El anual de French se compone de meses; aqui se usa tal cual
    anual = [r for _, r in ra]
    a, s, g = st.mean(anual), st.pstdev(anual), geo(anual)
    print(f"Anual calendario: n={len(anual)} ({ra[0][0].year}-{ra[-1][0].year}) | A={a:.4f} s={s:.4f} G={g:.4f} "
          f"| drag obs A-G={100*(a-g):.2f} pp vs s²/2={100*s*s/2:.2f} pp | A-s²/2={a-s*s/2:.4f}")
    print("  (dos sesgos: la aprox. es de 2o orden y la asimetria negativa/curtosis agrega drag)")

    print("\n== 2. Por decada (mensual, anualizado) ==")
    print("decada | sigma | drag obs (A x12 - 12 ln(1+G)) | s²/2 | diferencia")
    por_dec = {}
    for f, r in serie_m:
        por_dec.setdefault(f.year // 10 * 10, []).append(r)
    for dec in sorted(por_dec):
        x = por_dec[dec]
        if len(x) < 60:
            continue
        a_m, s_m = st.mean(x), st.pstdev(x)
        drag_obs = 12 * a_m - 12 * math.log1p(geo(x))
        teo = 12 * s_m * s_m / 2
        print(f"{dec}s | {math.sqrt(12)*s_m:.3f} | {100*drag_obs:.2f} | {100*teo:.2f} | {100*(drag_obs-teo):+.2f} pp")

    print("\n== 3. Apalancamiento diario sintetico (French diario, sin costos) ==")
    td = dh.french("F-F_Research_Data_Factors_daily", "diaria")
    exc = [(f, e, rf) for f, e, rf in zip(td["fechas"], td["columnas"]["Mkt-RF"], td["columnas"]["RF"])
           if e is not None and rf is not None]
    print(f"archivo {td['archivo']} sha256 {td['sha256'][:12]} {exc[0][0]}..{exc[-1][0]} n={len(exc)}")
    dias = len(exc) / ((exc[-1][0] - exc[0][0]).days / 365.25)
    mu_d = st.mean(e for _, e, _ in exc)
    var_d = st.pvariance([e for _, e, _ in exc])
    rf_d = st.mean(r for _, _, r in exc)
    mu, var, rf = mu_d * dias, var_d * dias, rf_d * dias
    lstar = mu / var
    print(f"dias/año={dias:.1f} | mu exceso aritm={mu:.4f} sigma={math.sqrt(var):.4f} rf={rf:.4f} | L*=mu/s²={lstar:.2f}")
    print("L | g obs (log, /año) | formula rf+L mu-L² s²/2 | CAGR obs | MDD")
    for L in (1, 1.5, 2, 3, 4):
        logs, v, pico, mdd = 0.0, 1.0, 1.0, 0.0
        for _, e, r in exc:
            x = r + L * e
            if x <= -1:
                logs = -math.inf
                mdd = 1.0
                break
            logs += math.log1p(x)
            v *= 1 + x
            pico = max(pico, v)
            mdd = max(mdd, 1 - v / pico)
        g_obs = logs / (len(exc) / dias)
        teo = rf + L * mu - L * L * var / 2
        print(f"{L} | {g_obs:.4f} | {teo:.4f} | {math.exp(g_obs)-1:.4f} | {mdd:.3f}")

    print("\n== 4. ETF reales: UPRO contra SPY (Yahoo, cierre ajustado) ==")
    spy = dict(datos.yahoo_serie("SPY", rango="30y"))
    upro = dict(datos.yahoo_serie("UPRO", rango="30y"))
    fechas = sorted(set(spy) & set(upro))
    rs_spy = [spy[b] / spy[a] - 1 for a, b in zip(fechas, fechas[1:])]
    rs_up = [upro[b] / upro[a] - 1 for a, b in zip(fechas, fechas[1:])]
    anios = (fechas[-1] - fechas[0]).days / 365.25
    n_an = len(rs_spy) / anios
    g_spy = sum(math.log1p(r) for r in rs_spy) / anios
    g_up = sum(math.log1p(r) for r in rs_up) / anios
    m_spy, v_spy = st.mean(rs_spy) * n_an, st.pvariance(rs_spy) * n_an
    # Prediccion ingenua (sin costos): 3x la media aritmetica, 9x la varianza; rf aprox. de French en el periodo
    rf_per = [r for f, _, r in exc if fechas[0] <= f <= fechas[-1]]
    rf_p = st.mean(rf_per) * dias if rf_per else 0.0
    pred = -2 * rf_p + 3 * m_spy - 9 * v_spy / 2
    print(f"{fechas[0]}..{fechas[-1]} ({anios:.1f} años, n={len(rs_spy)})")
    print(f"SPY: g log={g_spy:.4f} (CAGR {math.exp(g_spy)-1:.4f}) sigma={math.sqrt(v_spy):.4f}")
    print(f"UPRO: g log={g_up:.4f} (CAGR {math.exp(g_up)-1:.4f}) sigma={math.sqrt(st.pvariance(rs_up)*n_an):.4f}")
    print(f"Formula -2rf+3A-9s²/2 = {pred:.4f} | brecha obs-formula = {100*(g_up-pred):+.2f} pp/año "
          f"(gasto 0.91%, financiamiento sobre rf, swaps) | 3x g SPY = {3*g_spy:.4f}")
    print(f"beta diaria UPRO/SPY = {st.covariance(rs_up, rs_spy)/st.variance(rs_spy):.3f}")


if __name__ == "__main__":
    main()
