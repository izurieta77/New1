# Post-mortem · Bolsa Mexicana de Valores (BOLSAA.MX) · 3T26 (reportado el 20-oct-2026)

> Rutina de cierre, 22-oct-2026 (~21:45 UTC). Los pronósticos se registraron el 25-sep en `empresas/BOLSAA.MX/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado, y no se modifican. Las resoluciones están en `empresas/BOLSAA.MX/resoluciones.csv`. Sin posición: no hay decisión de cartera ni votos del comité que evaluar, solo pronósticos. No se ejecutó `herramientas/pronosticos.py resolver` ni se tocaron `bitacora/pronosticos.csv` ni `competencia/calibracion-agentes.csv`.

## 1. Resultado real (fuente primaria)
**Fuente:** Grupo BMV, comunicado "Resultados del 3er trimestre de 2026" (Ciudad de México, 20-oct-2026; llamada el 21-oct), en su sitio de relación con inversionistas: [GBMV-doc-BMV_3T26_esp.pdf](https://www.bmv.com.mx/docs-pub/reporteTrimestral/GBMV-doc-BMV_3T26_esp.pdf) (28 pp., sha256 `362aa834…`), enlazado desde [reportes financieros](https://www.bmv.com.mx/es/relacion-con-inversionistas/reportes-financieros). Cotejado con el reporte trimestral XBRL entregado a la BMV: [ifrsxbrl_1596526_2026-03_1.zip](https://www.bmv.com.mx/docs-pub/ifrsxbrl/ifrsxbrl_1596526_2026-03_1.zip) (sha256 `c801b8c4…`; `Revenue` 3T26 = 1,160,972 miles). No hubo evento relevante de resultados en Emisnet (la lista de eventos de BOLSA-7029 termina el 21-jul-2026).

Estado de resultados 3T26 (Ps miles en el comunicado; aquí en Ps M):
- **Ingresos: 1,161** (1,160.972; +5.4% a/a contra 1,101.5; −3.1% t/t contra 1,198 del 2T26, cálculo propio).
  - Derivados +19.2% (MexDer +21.9%, Asigna +16.4%); OTC (SIF ICAP) +11.2%; Indeval +4.8%; capitales −0.9%; servicios de información +1.1%.
- Gastos: 606 (+11.5%; personal +14.2%, depreciación +24.8%). Utilidad de operación: 555 (margen 47.8%). EBITDA: 635 (margen 54.7%).
- RIF: 55 (ganancia cambiaria de 5). Tasa de impuestos: **29.3%** (31.1% un año antes). Minoritario: −39.5.
- **Utilidad neta: 396.9 M** (+1.0%). **Miles de acciones: 551,591. Utilidad por acción: 0.72** (0.70 en 3T25).
- VOPD de capitales: **Ps 17,116 M** (+1% a/a; 2T26: 21,486).
- **Nota de definición:** el XBRL reporta `BasicEarningsLossPerShare` = 0.80, que coincide con la utilidad consolidada (436.5 M, incluye minoritario) / 551.6 M acciones (cálculo propio). El criterio del pronóstico manda la "Utilidad por Acción del estado de resultados trimestral del comunicado": **0.72**, que también es UN controladora / acciones (396.9 / 551.6 = 0.720).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos 3T26 | 1,180 (1,125-1,240) | 1,200 | 1,161 | +1.64% | +3.36% | Dentro del 80% |
| UPA 3T26 | 0.71 (0.65-0.78) | 0.74 | 0.72 | −1.39% | +2.78% | Dentro del 80% |
| P(ingresos > 1,200) | 0.35 | — | No | — | — | Brier 0.1225 |
| P(UPA > 0.74) | 0.30 | — | No | — | — | Brier 0.0900 |

Brier promedio de los binarios: **0.1063**. Los dos puntos fueron mejores que el consenso.

## 3. Matriz y lectura
- **Ingresos: buen proceso, buen resultado (con un supuesto equivocado).** El supuesto "el 3T queda al nivel del 2T" se rompió: el VOPD de capitales cayó de 21.5 mil M a 17.1 mil M y los ingresos bajaron 3.1% t/t. El punto (+7% a/a) quedó arriba del real (+5.4%), pero dentro del intervalo, y el sesgo contra el consenso (abajo de 1,200) fue correcto. Derivados y OTC compensaron capitales.
- **UPA: buen resultado, con compensación de errores.** Gastos (606 contra ~605), minoritario (−39.5 contra −40) y acciones (551.6 contra 551) se acertaron. El menor ingreso (−19 M contra el punto) se compensó con una tasa de 29.3% contra 31.5% supuesta y un RIF de 55 contra 50. Sin la tasa más baja, la UPA habría salido en ~0.70 (inferencia aproximada).
- **Binarios (0.35 y 0.30): buenas decisiones, buen resultado.** Se apostó contra el consenso con un argumento (volumen sin impulso adicional, gasto creciendo +12-13%) que se cumplió.
- **Qué se sabía el 25-sep:** el VOPD de julio-agosto (estadísticas mensuales, no consultadas en la ficha), la inflación de gastos y el peso fuerte.
- **Qué no se podía saber:** la tasa efectiva del trimestre.
- **Escenario (§7):** el VOPD (17.1 mil M) queda **debajo** del umbral del bajista (~18 mil M); el gasto (606) queda debajo del umbral de 620 M; los ingresos de 9M26 (3,570 M, +7.0%) siguen en ruta a la parte baja del rango base (4,750-4,830). **Lectura (inferencia):** señal mixta; el volumen de capitales apunta al bajista, pero derivados y OTC sostienen el ingreso. Se anota en la adenda sin cambiar las probabilidades.

## 4. Lecciones (cada una cambia algo concreto)
1. **Revisar el VOPD mensual publicado antes de fijar el punto.** Las estadísticas de julio y agosto ya existían al 25-sep. Checklist de la §8 para emisoras de volumen (BOLSA, casas de bolsa): anotar el VOPD de los meses ya transcurridos del trimestre.
2. **Definición de UPA explícita en el criterio.** Aquí el criterio decía "del comunicado" y eso evitó la ambigüedad con el 0.80 del XBRL (que usa utilidad consolidada). Regla: en emisoras con minoritario relevante, el criterio debe nombrar el numerador (UN controladora) y la fuente.
3. **Tasa efectiva:** anotar la tasa de los últimos 4 trimestres junto al supuesto (misma lección que AMX del 21-oct; segundo caso en dos días).

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`: las cifras del 2T26 de la ficha no se contradicen con este comunicado (que no repite la columna del 2T26; solo se usó el 1,198 de la ficha para el t/t).
