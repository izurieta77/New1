# Post-mortem · GEV · 3T26 (comunicado del 2026-10-28; resuelto en el cierre del 30-oct-2026)

> Los pronósticos del 25-sep (`pronosticos.csv`, §8 de la ficha) no se modifican. Sin posición individual (SPYM y QQQM las contienen, según el caso). Forma parte del rezago de 28 empresas (`herramientas/rezago_empresas.py`).

## 1. Resultado real ([comunicado del 8-K](https://www.sec.gov/Archives/edgar/data/1996810/000199681026000162/gevpressrelease3q26.htm), leído por WebFetch)
- Ingresos de US$12,642 M (+27%); **UPA diluida GAAP de 4.81** (1.64 en el 3T25); EBITDA ajustado de 1,943 (15.4%); pedidos de 29.3 mil M (+96% orgánico); cartera de 197 mil M. Comunicado del 28-oct, resuelto 2 días tarde.
- **Precio:** 878.03 → 887.85 → 857.87 (28 al 30-oct) (Yahoo 1d).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error del punto | Puntuación |
|---|---|---|---|---|---|
| Ingresos (US$ M) | 12,000 (11,500-12,550) | 12,013 | 12,642 | −5.1% | **Fuera** |
| UPA GAAP | 3.90 (3.00-4.80) | 4.17 | 4.81 | −18.9% | **Fuera por 0.01** |
| P(ingresos > 12,013) | 0.48 | — | Sí | — | Brier 0.2704 |
| P(UPA > 4.17) | 0.38 | — | Sí | — | Brier 0.3844 |

Brier promedio de los binarios: **0.3274**.

## 3. Lectura y lecciones
- **Mal resultado:** los dos puntos fuera y los dos binarios del lado equivocado (Brier promedio de 0.33). El auge de pedidos de energía para centros de datos (+96%) se subestimó. **Lección:** en emisoras con pedidos que se duplican, el punto debe seguir a la cartera y a los pedidos, no al consenso.
