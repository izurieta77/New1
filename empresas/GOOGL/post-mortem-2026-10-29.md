# Post-mortem · GOOGL · 3T26 (reportado el 2026-10-28)

> Rutina de cierre, 29-oct-2026. Los pronósticos del 25-sep (`pronosticos.csv`, §8 de la ficha) no se modifican. Sin posición individual; las grandes de EUA pesan en SPYM y QQQM.

## 1. Resultado real ([comunicado del 8-K](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000080/googexhibit991q32026.htm), leído por WebFetch)
- Ingresos de US$127,577 M (+24.7% contra 102,346); UPA diluida GAAP de 2.12, con una pérdida en valores de capital de 8.7 mil M (−0.55 por acción; UPA sin ese efecto ≈ 2.67); Google Cloud de 30,709 M (+103%); utilidad de operación de 40,576 M (32%); compras de PP&E de 51,355 M; tasa ≈ 18.2% (cálculo propio).
- **Precio:** 324.89 → 283.82 el 29-oct (−12.6%); after-hours 281.38 (Yahoo).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error del punto | Puntuación |
|---|---|---|---|---|---|
| Ingresos (US$ M) | 127,800 (125,000-130,800) | 127,298 | 127,577 | +0.17% | Dentro |
| UPA diluida GAAP | 2.20 (1.45-3.60) | 3.019 | 2.12 | +3.8% | Dentro |
| P(ingresos > 127,298) | 0.58 | — | Sí | — | Brier 0.1764 |
| P(UPA sin valores de capital > 3.019) | 0.40 | — | No (≈2.67) | — | Brier 0.16 |

Brier promedio de los binarios: **0.1682**.

## 3. Lectura y lecciones
- Buen proceso en ingresos y UPA: el intervalo amplio de la UPA (por la volatilidad de los valores de capital) se justificó con una pérdida de 8.7 mil M. El precio cayó −12.6% con ingresos en línea: el mercado castigó el capex (51.4 mil M, más del doble del 3T25) y el flujo libre, que no se pronosticaron. **Lección:** en emisoras con capex explosivo, agregar un pronóstico de capex o flujo libre, porque es la variable que hoy mueve el precio. **Resuelto un día tarde:** reportó el 28-oct; ver el registro de errores.
