# Post-mortem · ABBV · 3T26 (comunicado del 2026-10-30; resuelto en el cierre del 30-oct-2026)

> Los pronósticos del 25-sep (`pronosticos.csv`, §8 de la ficha) no se modifican. Sin posición individual (SPYM y QQQM las contienen, según el caso). Forma parte del rezago de 28 empresas (`herramientas/rezago_empresas.py`).

## 1. Resultado real ([comunicado del 8-K](https://www.sec.gov/Archives/edgar/data/1551152/000155115226000033/abbv-20260930xexhibit991.htm), leído por WebFetch)
- Ingresos netos de US$17,404 M (+10.3%); UPA GAAP de 2.37 y **ajustada de 3.82**, con −0.11 de IPR&D y milestones; Skyrizi 5,776 y Rinvoq 2,706; guía 2026 de UPA ajustada subida a 13.95-13.99.
- **Precio:** 290.79 → 294.89 (+1.4%) el 30-oct (Yahoo 1d).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error del punto | Puntuación |
|---|---|---|---|---|---|
| Ingresos (US$ M) | 17,450 (17,150-17,750) | 17,314 | 17,404 | +0.3% | Dentro |
| UPA ajustada | 3.55 (2.75-3.88) | 3.844 | 3.82 | −7.1% | Dentro |
| P(ingresos > 17,314) | 0.70 | — | Sí | — | Brier 0.09 |
| P(UPA > 3.844) | 0.15 | — | No (3.82) | — | Brier 0.0225 |

Brier promedio de los binarios: **0.0562**.

## 3. Lectura y lecciones
- Buen proceso: el binario de UPA a 0.15 anticipó que el IPR&D adquirido restaría contra el consenso; fue −0.11 y la UPA quedó 0.02 abajo. El punto de UPA (3.55) supuso más IPR&D del que hubo.
