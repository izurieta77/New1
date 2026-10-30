# Post-mortem · INTC · 3T26 (reportado el 2026-10-29)

> Rutina de cierre, 29-oct-2026. Los pronósticos del 25-sep (`pronosticos.csv`, §8 de la ficha) no se modifican. Sin posición individual; las grandes de EUA pesan en SPYM y QQQM.

## 1. Resultado real ([comunicado del 8-K](https://www.sec.gov/Archives/edgar/data/50863/000005086326000188/q326earningsrelease.htm), leído por WebFetch)
- Ingresos netos de US$16,513 M (+21% contra 13,653); UPA GAAP de 0.60 y **non-GAAP de 0.52**; margen bruto GAAP de 43.0% (non-GAAP 44.1%). **Guía del 4T: ingresos de 15.0-16.0 mil M y UPA non-GAAP de 0.25**.
- **Precio:** cierre regular 92.07; after-hours 73.17 (**−20.5%**) [Nota 2026-10-30 01:11 UTC, revisión del 29-oct m5: precio de Yahoo 1m de las 21:38-21:39 UTC del 29-oct (consulta del cierre); las lecturas posteriores difieren] por la guía (Yahoo).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error del punto | Puntuación |
|---|---|---|---|---|---|
| Ingresos (US$ M) | 16,950 (16,200-18,300) | 16,428 | 16,513 | +2.6% | Dentro |
| UPA non-GAAP | 0.44 (0.36-0.58) | 0.391 | 0.52 | −15.4% | Dentro |
| P(ingresos > 16,428) | 0.78 | — | Sí | — | Brier 0.0484 |
| P(UPA > 0.39) | 0.74 | — | Sí | — | Brier 0.0676 |

Brier promedio de los binarios: **0.0580**.

## 3. Lectura y lecciones
- Buen resultado en los cuatro pronósticos del trimestre, pero **la guía del 4T** (UPA de 0.25 contra 0.52) llevó la acción a −20.5% en el after-hours. **Lección (la misma que CAT y GOOGL):** el precio reacciona a la guía y al capex, no al trimestre. Las fichas deben llevar un pronóstico de la guía.
