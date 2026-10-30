# Post-mortem · MRK · 3T26 (comunicado del 2026-10-29; resuelto en el cierre del 30-oct-2026)

> Los pronósticos del 25-sep (`pronosticos.csv`, §8 de la ficha) no se modifican. Sin posición individual (SPYM y QQQM las contienen, según el caso). Forma parte del rezago de 28 empresas (`herramientas/rezago_empresas.py`).

## 1. Resultado real ([comunicado del 8-K](https://www.sec.gov/Archives/edgar/data/310158/000110465926119825/tm2628203d1_ex99-1.htm), leído por WebFetch)
- Ventas mundiales de US$18,085 M (+5%; +4% sin tipo de cambio); UPA GAAP de 2.04 y **non-GAAP de 2.49**; Keytruda más Keytruda Qlex 8,601 (+6%); guía 2026 de ventas de 66.8-67.3 mil M y de UPA non-GAAP de 2.77-2.82 (con cargos únicos de 6.05 por acción).
- **Precio:** 140.93 → 146.33 (+3.8%) el 29-oct (Yahoo 1d).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error del punto | Puntuación |
|---|---|---|---|---|---|
| Ventas (US$ M) | 17,550 (17,000-18,050) | 17,340 | 18,085 | −3.0% | **Fuera (35 M sobre el p90)** |
| UPA non-GAAP | 2.30 (1.95-2.50) | 2.206 | 2.49 | −7.6% | Dentro, cerca del p90 |
| P(ventas > 17,340) | 0.66 | — | Sí | — | Brier 0.1156 |
| P(UPA > 2.206) | 0.65 | — | Sí | — | Brier 0.1225 |

Brier promedio de los binarios: **0.1190**.

## 3. Lectura y lecciones
- Dirección correcta en los binarios; los dos puntos quedaron cortos y las ventas salieron del intervalo por 35 M. **Lección:** en farmacéuticas con un producto dominante (Keytruda), el intervalo de ventas de ±3% es estrecho.
