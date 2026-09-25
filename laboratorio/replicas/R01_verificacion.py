"""R01 - Comprobacion independiente (doble implementacion) de sma10 y comprar y mantener, SIN el motor.

Reproduce: python3 laboratorio/replicas/R01_verificacion.py  (despues de R01.py)
Lee el zip congelado de French (CRSP 202607), reimplementa la regla y el modelo de costos con
aritmetica propia y compara contra R01-resultados.json. No es una variante nueva: es la misma
regla calculada por otro camino; no se registra en R01-variantes.csv. Da ademas las fechas de
pico y valle de los drawdowns maximos. Solo biblioteca estandar.
"""
import csv
import io
import json
import math
import zipfile
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ZIP = AQUI / "R01-datos" / "202607" / "F-F_Research_Data_Factors_CSV.zip"
CORTE = date(2006, 12, 31)
COSTO_LADO = 0.0029 + 0.0005


def leer_french():
    with zipfile.ZipFile(ZIP) as z:
        texto = z.read(z.namelist()[0]).decode("latin-1")
    filas = []
    for fila in csv.reader(io.StringIO(texto)):
        if fila and fila[0].strip().isdigit() and len(fila[0].strip()) == 6:
            ym = int(fila[0])
            a, m = divmod(ym, 100)
            fin = date(a + (m == 12), m % 12 + 1, 1)
            fin = date.fromordinal(fin.toordinal() - 1)
            filas.append((fin, float(fila[1]) / 100 + float(fila[4]) / 100, float(fila[4]) / 100))
        elif filas and fila and "Annual" in fila[0]:
            break
    return filas


def simular(filas, ventana, costo_lado, siempre=False):
    """Decide w_t al cierre de t-1 con el indice TR hasta t-1; costo sobre |w_t - w_pre_t|."""
    indice, nivel = [], 1.0
    for _, mkt, _ in filas:
        nivel *= 1 + mkt
        indice.append(nivel)
    salida, w_prev, ra_prev, rb_prev = [], 0.0, None, None
    for t in range(12, len(filas)):
        if siempre:
            w = 1.0
        else:
            ult = indice[t - ventana:t]
            w = 1.0 if ult[-1] > sum(ult) / ventana else 0.0
        f, mkt, rf = filas[t]
        w_pre = w_prev if ra_prev is None else w_prev * (1 + ra_prev) / (1 + rb_prev)
        c = abs(w - w_pre) * costo_lado
        rb = w * mkt + (1 - w) * rf
        rn = (1 - c) * (1 + rb) - 1
        salida.append((f, rn, rf, w))
        w_prev, ra_prev, rb_prev = w, mkt, rb
    return salida


def resumen(serie, f0, desde, hasta):
    tramo = [x for x in serie if desde <= x[0] <= hasta]
    inicio = f0 if tramo[0] is serie[0] else serie[serie.index(tramo[0]) - 1][0]
    nivel, maximo, pico, peor, fp, fv = 1.0, 1.0, inicio, 0.0, None, None
    for f, rn, _, _ in tramo:
        nivel *= 1 + rn
        if nivel > maximo:
            maximo, pico = nivel, f
        dd = nivel / maximo - 1
        if dd < peor:
            peor, fp, fv = dd, pico, f
    anios = (tramo[-1][0] - inicio).days / 365.25
    ex = [rn - rf for _, rn, rf, _ in tramo]
    media = sum(ex) / len(ex)
    sd = math.sqrt(sum((x - media) ** 2 for x in ex) / (len(ex) - 1))
    return {"cagr": nivel ** (1 / anios) - 1, "mdd": peor, "pico": fp, "valle": fv,
            "sharpe": media / sd * math.sqrt(12), "invertido": sum(w for *_, w in tramo) / len(tramo),
            "n": len(tramo)}


def main():
    filas = leer_french()
    f0 = filas[11][0]
    res = json.loads((AQUI / "R01-resultados.json").read_text(encoding="utf-8"))
    motor = {r["variante"] + "|" + r["segmento"]: r for k in ("principal_dentro_muestra", "principal_fuera_muestra",
                                                              "principal_completo")
             for r in res["tablas"][k]}
    motor.update({r["variante"] + "|" + r["segmento"]: r for k in ("costos_dentro_muestra", "costos_fuera_muestra")
                  for r in res["tablas"][k]})
    segmentos = {"completo": (date(1900, 1, 1), date(2100, 1, 1)), "dentro_muestra": (date(1900, 1, 1), CORTE),
                 "fuera_muestra": (date(2007, 1, 1), date(2100, 1, 1))}
    max_dif = 0.0
    for nombre, clave, costo, siempre in (("sma10", "sma10", COSTO_LADO, False),
                                          ("comprar_y_mantener", "comprar_y_mantener", COSTO_LADO, True),
                                          ("sma10 sin costos", "sma10|sin_costos", 0.0, False),
                                          ("B&H sin costos", "comprar_y_mantener|sin_costos", 0.0, True)):
        serie = simular(filas, 10, costo, siempre)
        for seg, (a, b) in segmentos.items():
            r = resumen(serie, f0, a, b)
            m = motor.get(f"{clave}|{seg}")
            difs = ""
            if m:
                d = [abs(r["cagr"] - m["cagr"]), abs(r["mdd"] - m["mdd"]), abs(r["sharpe"] - m["sharpe"])]
                max_dif = max(max_dif, *d)
                difs = f" | motor: CAGR {100 * m['cagr']:.4f}% MDD {100 * m['mdd']:.4f}% Sharpe {m['sharpe']:.4f}"
            print(f"{nombre:<20} {seg:<15} n={r['n']:<5} CAGR {100 * r['cagr']:.4f}% MDD {100 * r['mdd']:.4f}% "
                  f"(pico {r['pico']}, valle {r['valle']}) Sharpe {r['sharpe']:.4f} invertido {100 * r['invertido']:.2f}%{difs}")
    print(f"Maxima diferencia absoluta contra el motor (CAGR, MDD, Sharpe): {max_dif:.2e}")
    assert max_dif < 1e-9, "la doble implementacion no coincide con el motor"


if __name__ == "__main__":
    main()
