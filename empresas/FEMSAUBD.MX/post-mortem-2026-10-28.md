# Post-mortem · FEMSA (FEMSAUBD.MX) · 3T26 (6-K del 28-oct-2026)

> Rutina de cierre, 28-oct-2026. Los pronósticos del 25-sep (`pronosticos.csv`, §8 de la ficha) no se modifican. Sin posición.

## 1. Resultado real ([EX-99.1](https://www.sec.gov/Archives/edgar/data/1061736/000110465926119381/tm2628435d1_ex99-1.htm), leído por WebFetch)
- **Ingresos totales: Ps 235,609 M (+9.8%; +9.4% comparable).** Por unidad: OXXO México +10.3% (tiendas iguales +9.2%: ticket +5.5%, tráfico +3.5%); Americas & Mobility +18.1% (+10.9% comparable); Europa −5.2% (+4.0% comparable); Salud +7.0%; Coca-Cola FEMSA +10.9%.
- **Utilidad de operación:** 19,918 (+9.9%; margen de 8.5%). EBITDA ajustado de 34,833 (+12.9%; 14.8%).
- **UN mayoritaria: Ps 6,810 M** (2,415 en el 3T25, que llevaba una pérdida de 3,146 por operaciones discontinuadas de Solistica). Ganancia cambiaria de 1,121 contra una pérdida de 1,261. Tasa de 32.5%.
- **UPA as reported: Ps 2.00 por unidad BD** (3,412.7 M unidades, con tesorería). La proforma sin tesorería es de 2.01. El criterio pide la as reported.
- **Precio:** 230.56 (−0.75%).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Puntuación |
|---|---|---|---|---|---|
| Ingresos (Ps M) | 230,000 (225,000-235,500) | 228,760 | 235,609 | −2.38% | **Fuera por 109 M** |
| UPA por unidad (as reported) | 1.80 (1.15-2.30) | 2.03 | 2.00 | −10.0% | Dentro |
| P(ingresos > 228,760) | 0.60 | — | Sí | — | Brier 0.16 |
| P(UPA > 2.03) | 0.30 | — | No (2.00) | — | Brier 0.09 |

## 3. Lectura y lecciones
- **Ingresos:** las tiendas iguales de OXXO (+9.2%) superaron lo que el intervalo admitía. El p90 se quedó 109 M corto: un fallo marginal, pero un fallo.
- **UPA:** el binario a 0.30 acertó la dirección (NO) por 0.03. El punto (1.80) fue conservador: la ganancia cambiaria y la ausencia de discontinuadas lo superaron.
- **Lección:** en conglomerados con partidas no operativas grandes (cambiaria, discontinuadas), el intervalo de la UPA debe abrirse por esas partidas, no por el crecimiento operativo. No hay errores de hecho que registrar.
