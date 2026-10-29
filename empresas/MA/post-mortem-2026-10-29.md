# Post-mortem · MA · 3T26 (reportado el 2026-10-29)

> Rutina de cierre, 29-oct-2026. Los pronósticos del 25-sep (`pronosticos.csv`, §8 de la ficha) no se modifican. Sin posición individual; las grandes de EUA pesan en SPYM y QQQM.

## 1. Resultado real ([comunicado del 8-K](https://www.sec.gov/Archives/edgar/data/1141391/000114139126000122/ma09302026-exx991xearnings.htm), leído por WebFetch)
- Ingresos netos de US$9,807 M (+14.0% contra 8,602); UPA diluida GAAP de 5.28 y **ajustada de 5.31**; tasa ajustada de 20.1%.
- **Precio:** 610.31 → 635.70 (+4.2%) (Yahoo).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error del punto | Puntuación |
|---|---|---|---|---|---|
| Ingresos netos (US$ M) | 9,660 (9,500-9,820) | 9,638 | 9,807 | −1.5% | Dentro, a 13 M del p90 |
| UPA ajustada | 5.17 (5.03-5.31) | 5.15 | 5.31 | −2.6% | Dentro, en el p90 exacto |
| P(ingresos > 9,638) | 0.55 | — | Sí | — | Brier 0.2025 |
| P(UPA > 5.15) | 0.58 | — | Sí | — | Brier 0.1764 |

Brier promedio de los binarios: **0.1895**.

## 3. Lectura y lecciones
- Dirección correcta, pero los dos puntos quedaron en el borde alto del intervalo: **intervalos demasiado estrechos** (±1.7% en ingresos, ±2.7% en UPA) para una emisora que superó el consenso por 1.8% y 3.1%. **Lección:** con un historial de sorpresas positivas, centrar el punto arriba del consenso y ensanchar el p90.
