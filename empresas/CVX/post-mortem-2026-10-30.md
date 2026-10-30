# Post-mortem · CVX · 3T26 (comunicado del 2026-10-30; resuelto en el cierre del 30-oct-2026)

> Los pronósticos del 25-sep (`pronosticos.csv`, §8 de la ficha) no se modifican. Sin posición individual (SPYM y QQQM las contienen, según el caso). Forma parte del rezago de 28 empresas (`herramientas/rezago_empresas.py`).

## 1. Resultado real ([comunicado del 8-K](https://www.sec.gov/Archives/edgar/data/93410/000009341026000196/a09302026ex9918-k.htm), leído por WebFetch)
- Ingresos totales y otros de US$67,798 M (contra 49,726); UPA GAAP de 5.06 y **ajustada de 5.28**; producción de 3,980 MBOED (4,086 en el 3T25).
- **Precio:** 231.46 → 235.52 (+1.8%) el 30-oct (Yahoo 1d).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error del punto | Puntuación |
|---|---|---|---|---|---|
| Ingresos totales (US$ M) | 66,800 (59,800-73,500) | 56,754 | 67,798 | −1.5% | Dentro |
| UPA ajustada | 4.20 (3.30-5.40) | 4.73 | 5.28 | −20.5% | Dentro, cerca del p90 |
| P(ingresos > 56,754) | 0.95 | — | Sí | — | Brier 0.0025 |
| P(UPA > 4.73) | 0.28 | — | Sí | — | Brier 0.5184 |

Brier promedio de los binarios: **0.2604**.

## 3. Lectura y lecciones
- **Los ingresos sí reflejaron el petróleo caro, pero la UPA no.** El punto de UPA (4.20) y el binario a 0.28 supusieron un margen que el Brent del trimestre (~100-115) superó con holgura. Es el mismo error que en XOM: modelamos el precio en ingresos y no lo trasladamos a la utilidad, que es mucho más sensible (apalancamiento operativo).
