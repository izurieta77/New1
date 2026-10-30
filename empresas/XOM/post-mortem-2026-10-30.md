# Post-mortem · XOM · 3T26 (comunicado del 2026-10-30; resuelto en el cierre del 30-oct-2026)

> Los pronósticos del 25-sep (`pronosticos.csv`, §8 de la ficha) no se modifican. Sin posición individual (SPYM y QQQM las contienen, según el caso). Forma parte del rezago de 28 empresas (`herramientas/rezago_empresas.py`).

## 1. Resultado real ([comunicado del 8-K](https://www.sec.gov/Archives/edgar/data/2115436/000211543626000018/livef8k3q26992.htm), leído por WebFetch)
- Ingresos totales y otros de US$113,164 M (contra 85,294); UPA GAAP de 3.72 y **ajustada (sin partidas identificadas ni efectos de tiempo) de 4.23**. Primer reporte trimestral de la nueva tenedora (CIK 2115436); el comunicado es el EX-99.1 y el estado de resultados, el EX-99.2.
- **Precio:** 183.29 → 187.25 (+2.2%) el 30-oct (Yahoo 1d).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error del punto | Puntuación |
|---|---|---|---|---|---|
| Ingresos totales (US$ M) | 113,000 (101,000-123,000) | 99,167 | 113,164 | −0.1% | Dentro |
| UPA ajustada | 3.55 (3.00-4.10) | 3.62 | 4.23 | −16.1% | **Fuera** |
| P(ingresos > 99,167) | 0.88 | — | Sí | — | Brier 0.0144 |
| P(UPA > 3.62) | 0.43 | — | Sí | — | Brier 0.3249 |

Brier promedio de los binarios: **0.1697**.

## 3. Lectura y lecciones
- **Igual que CVX:** ingresos exactos (−0.1%) y UPA muy por debajo. El petróleo caro entró en los ingresos del modelo y no en el margen. **Lección para las petroleras:** pronosticar la UPA con la sensibilidad publicada de utilidad por dólar del Brent (las dos la publican), no con un margen fijo.
