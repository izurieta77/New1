# Post-mortem · KO · 3T26 (comunicado del 2026-10-27; resuelto en el cierre del 30-oct-2026)

> Los pronósticos del 25-sep (`pronosticos.csv`, §8 de la ficha) no se modifican. Sin posición individual (SPYM y QQQM las contienen, según el caso). Forma parte del rezago de 28 empresas (`herramientas/rezago_empresas.py`).

## 1. Resultado real ([comunicado del 8-K](https://www.sec.gov/Archives/edgar/data/21344/000162828026067403/a2026q3earningsreleaseex-9.htm), leído por WebFetch)
- Ingresos operativos netos de US$13,380 M (+7%; orgánico +7%); UPA GAAP de 0.93 y **comparable de 0.91** (+11%). **Comunicado del 27-oct, resuelto 3 días tarde** (rezago).
- **Precio:** 91.73 → 92.82 → 94.08 (28 al 30-oct) (Yahoo 1d).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error del punto | Puntuación |
|---|---|---|---|---|---|
| Ingresos (US$ M) | 13,000 (12,750-13,280) | 12,890 | 13,380 | −2.8% | **Fuera (100 M sobre el p90)** |
| UPA comparable | 0.90 (0.85-0.93) | 0.88 | 0.91 | −1.1% | Dentro |
| P(ingresos > 12,890) | 0.66 | — | Sí | — | Brier 0.1156 |
| P(UPA > 0.88) | 0.62 | — | Sí | — | Brier 0.1444 |

Brier promedio de los binarios: **0.1300**.

## 3. Lectura y lecciones
- UPA bien; ingresos subestimados (+7% orgánico contra ~+4% supuesto). Resuelto tarde por el rezago de calendario.
