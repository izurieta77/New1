# Post-mortem · AMZN · 3T26 (reportado el 2026-10-29)

> Rutina de cierre, 29-oct-2026. Los pronósticos del 25-sep (`pronosticos.csv`, §8 de la ficha) no se modifican. Sin posición individual; las grandes de EUA pesan en SPYM y QQQM.

## 1. Resultado real ([comunicado del 8-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000038/amzn-20260930xex991.htm), leído por WebFetch)
- Ventas netas de US$201,944 M (+12.1% contra 180,169); AWS 45,984 (+39%) con utilidad operativa de 17,773; utilidad de operación de 28,076; UPA diluida GAAP de 1.89 (1.95 en el 3T25, que llevaba 9.5 mil M de ganancias de Anthropic); otros ingresos de −703 M. Guía del 4T: ventas de 240-247 mil M y utilidad de operación de 28.5-33.5 mil M.
- **Precio:** cierre regular 243.79; after-hours 231.12 (−5.2%) (Yahoo).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error del punto | Puntuación |
|---|---|---|---|---|---|
| Ventas netas (US$ M) | 204,000 (200,500-207,500) | 202,130 | 201,944 | +1.0% | Dentro |
| UPA GAAP | 2.20 (1.80-4.00) | 1.946 | 1.89 | +16.4% | Dentro, cerca del p10 |
| P(ventas > 202,130) | 0.72 | — | No (por 186 M) | — | Brier 0.5184 |
| P(UPA > 1.946) | 0.75 | — | No | — | Brier 0.5625 |

Brier promedio de los binarios: **0.5404**.

## 3. Lectura y lecciones
- **Mal resultado en los binarios** (0.72 y 0.75, los dos NO; Brier promedio de 0.54). El punto de UPA suponía ganancias en la inversión en Anthropic (el intervalo llegaba a 4.00), y en este trimestre no las hubo (otros ingresos de −703 M). Las ventas fallaron por 186 M contra el consenso. **Lección:** cuando la UPA GAAP depende de revaluaciones de inversiones, el binario contra el consenso debe ir cerca de 0.5, no a 0.75.
