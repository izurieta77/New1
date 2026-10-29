# Post-mortem · CAT · 3T26 (reportado el 2026-10-29)

> Rutina de cierre, 29-oct-2026. Los pronósticos del 25-sep (`pronosticos.csv`, §8 de la ficha) no se modifican. Sin posición individual; las grandes de EUA pesan en SPYM y QQQM.

## 1. Resultado real ([comunicado del 8-K](https://www.sec.gov/Archives/edgar/data/18230/000001823026000052/ex991toformcat3q2026earnin.htm), leído por WebFetch)
- Ventas e ingresos de US$20,682 M (+17% contra 17,638); utilidad por acción GAAP de 7.13 y **ajustada de 7.20**; margen operativo de 20.4% (ajustado 20.6%); tasa de 22.9% (26.7% en el 3T25).
- **Precio:** 713.38 → 647.39 (−9.3%) con resultados arriba del consenso (Yahoo).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error del punto | Puntuación |
|---|---|---|---|---|---|
| Ventas e ingresos (US$ M) | 20,800 (19,800-22,200) | 20,399 | 20,682 | +0.57% | Dentro |
| UPA ajustada | 7.05 (6.35-8.30) | 6.92 | 7.20 | −2.1% | Dentro |
| P(ventas > 20,399) | 0.68 | — | Sí | — | Brier 0.1024 |
| P(UPA > 6.92) | 0.58 | — | Sí | — | Brier 0.1764 |

Brier promedio de los binarios: **0.1394**.

## 3. Lectura y lecciones
- Buen proceso y buen resultado en los cuatro pronósticos. El precio cayó −9.3% con un reporte arriba del consenso. [Inferencia] Pesó lo que el comunicado dice de pedidos o de la guía, que no se leyó. **Lección:** la reacción del precio no se pronosticó; para emisoras con valuación alta, el riesgo está en la guía y no en el trimestre.
