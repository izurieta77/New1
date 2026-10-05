"""Ficha 2026-10-05: tasa base de las ganancias que definen Diamante, Platino y Oro.

Diamante: > +40% en 2-3 meses | Platino: > +50% en 3-5 meses | Oro: +20% a +30% en 5-7 meses.
Para cada ticker del universo (empresas/universo.csv) mas BTC-USD y ETH-USD: con ventanas diarias que
empiezan en cada dia, mide la fraccion que (a) termina arriba del umbral al plazo (rendimiento al
cierre del plazo) y (b) toca el umbral en cualquier dia dentro del plazo (maximo intradiario del
cierre). Ventanas: 63 dias habiles (3 meses; 2 meses = 42), 105 (5 meses), 147 (7 meses); cripto en dias
calendario equivalentes. Cierre ajustado de Yahoo; sin costos ni impuestos. Sesgo de supervivencia:
el universo es la lista actual de empresas grandes (declarado).
Uso: python3 conocimiento/fichas/codigo/2026-10-05-tasa-base-ganancias.py
"""
import csv
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from herramientas import datos_historicos as dh  # noqa: E402

RAIZ = Path(__file__).resolve().parents[3]
VENT = {"2m": 42, "3m": 63, "5m": 105, "7m": 147}


def tickers():
    with open(RAIZ / "empresas/universo.csv", encoding="utf-8", newline="") as f:
        return [r["ticker"] for r in csv.DictReader(f)]


def ventanas(px, n, umbral_bajo, umbral_alto=None):
    fin, toca, banda, tot = 0, 0, 0, 0
    for i in range(0, len(px) - n):
        base = px[i]
        w = px[i + 1:i + n + 1]
        r_fin = w[-1] / base - 1
        r_max = max(w) / base - 1
        tot += 1
        fin += r_fin >= umbral_bajo
        toca += r_max >= umbral_bajo
        if umbral_alto is not None:
            banda += umbral_bajo <= r_fin <= umbral_alto
    return fin, toca, banda, tot


def main():
    res = {}
    for t in tickers() + ["BTC-USD", "ETH-USD"]:
        try:
            h = dh.yahoo_historia(t)
        except Exception as e:  # sin dato
            print("sin dato", t, e)
            continue
        px = [p for p in h["precios"] if p]
        fechas = h["fechas"]
        corte = [p for p, f in zip(h["precios"], fechas) if f.year >= 2016 and p]
        esc = 1.0 if t.endswith("USD") and t[:3] in ("BTC", "ETH") else 1.0
        factor = 365 / 252 if t in ("BTC-USD", "ETH-USD") else 1.0
        res[t] = (corte, factor)
    print(f"{len(res)} series (2016-2026)\n")
    reglas = [("Diamante >+40% en 2m", 0.40, "2m"), ("Diamante >+40% en 3m", 0.40, "3m"),
              ("Platino >+50% en 3m", 0.50, "3m"), ("Platino >+50% en 5m", 0.50, "5m"),
              ("Oro +20% a +30% en 5m", 0.20, "5m"), ("Oro +20% a +30% en 7m", 0.20, "7m")]
    grupos = {"Universo (EUA y MX)": [t for t in res if t not in ("BTC-USD", "ETH-USD")],
              "BTC y ETH": ["BTC-USD", "ETH-USD"]}
    for gnom, lista in grupos.items():
        print(f"== {gnom} ({len(lista)} series) ==")
        print("regla | termina arriba del umbral | toca el umbral en la ventana | termina en la banda (Oro) | ventanas")
        for nom, um, v in reglas:
            fin = toca = banda = tot = 0
            for t in lista:
                px, fac = res[t]
                n = int(round(VENT[v] * fac))
                a, b, c, d = ventanas(px, n, um, 0.30 if nom.startswith("Oro") else None)
                fin += a; toca += b; banda += c; tot += d
            extra = f"{100*banda/tot:.1f}%" if nom.startswith("Oro") else "-"
            print(f"{nom} | {100*fin/tot:.1f}% | {100*toca/tot:.1f}% | {extra} | {tot:,}")
        print()
    # por ticker: cuantos tickers del universo tuvieron al menos una ventana de Diamante (3m, >40%) y cuantas veces
    lista = grupos["Universo (EUA y MX)"]
    fr = []
    for t in lista:
        px, fac = res[t]
        a, b, c, d = ventanas(px, 63, 0.40)
        fr.append((b / d, t))
    fr.sort(reverse=True)
    print("Tickers con mas frecuencia de tocar +40% en 3 meses:", ", ".join(f"{t} {100*x:.0f}%" for x, t in fr[:8]))
    print("Mediana del universo:", f"{100*st.median(x for x, _ in fr):.1f}%", "| sin una sola ventana:", sum(1 for x, _ in fr if x == 0))


if __name__ == "__main__":
    main()
