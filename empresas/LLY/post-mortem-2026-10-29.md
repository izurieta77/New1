# Post-mortem · LLY · 3T26 (reportado el 2026-10-29)

> Rutina de cierre, 29-oct-2026. Los pronósticos del 25-sep (`pronosticos.csv`, §8 de la ficha) no se modifican. Sin posición individual; las grandes de EUA pesan en SPYM y QQQM.

## 1. Resultado real ([comunicado del 8-K](https://www.sec.gov/Archives/edgar/data/59478/000005947826000104/q326lillysalesandearningsp.htm), leído por WebFetch)
- Ingresos de US$24,397 M (+39% contra 17,601); Mounjaro 10,723 (+65%) y Zepbound 5,352 (+49%); UPA reportada de 7.22 y **non-GAAP de 7.48**, con un IPR&D adquirido de 4,181 M (4.57 por acción) incluido; tasa non-GAAP de 24.0%.
- **Precio:** 1,288.30 → 1,373.70 (+6.6%) (Yahoo).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error del punto | Puntuación |
|---|---|---|---|---|---|
| Ingresos (US$ M) | 23,200 (22,000-24,500) | 22,329 | 24,397 | −4.9% | Dentro, cerca del p90 |
| UPA non-GAAP (con IPR&D) | 7.90 (5.30-11.00) | 9.93 | 7.48 | +5.6% | Dentro |
| P(ingresos > 22,329) | 0.75 | — | Sí | — | Brier 0.0625 |
| P(UPA > 9.93) | 0.28 | — | No | — | Brier 0.0784 |

Brier promedio de los binarios: **0.0704**.

## 3. Lectura y lecciones
- Buen proceso: el binario de UPA a 0.28 anticipó que el IPR&D adquirido (4.57 por acción) hundiría la UPA contra el consenso. Los ingresos se subestimaron (−4.9%): la demanda de incretinas creció más de lo supuesto. **Lección:** en franquicias con crecimiento > 40%, el punto debe extrapolar la aceleración reciente, no una desaceleración.
