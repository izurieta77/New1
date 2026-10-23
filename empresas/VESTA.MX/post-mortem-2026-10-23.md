# Post-mortem · Corporación Inmobiliaria Vesta (VESTA.MX) · 3T26 (reportado el 22-oct-2026)

> Rutina de cierre, 23-oct-2026 (~21:45 UTC). Los pronósticos se registraron el 25-sep en `empresas/VESTA.MX/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado, y no se modifican. Las resoluciones están en `empresas/VESTA.MX/resoluciones.csv`. Sin posición: no hay decisión de cartera ni votos del comité que evaluar, solo pronósticos. No se ejecutó `herramientas/pronosticos.py resolver` ni se tocaron `bitacora/pronosticos.csv` ni `competencia/calibracion-agentes.csv`. Todas las cifras están en **USD** (moneda de reporte de Vesta).

## 1. Resultado real (fuente primaria)
**Fuente:** comunicado "Q3 2026 Earnings Results" (Ciudad de México, 22-oct-2026; llamada el 23-oct) en el sitio de RI de Vesta: [Quarterly Report 3Q 2026 VF.pdf](https://d1io3yog0oux5.cloudfront.net/_a97d61def23f5b56c47196ea9549d7c3/vesta/db/2288/21966/quarterly_reports/Quarterly+Report+3Q+2026+VF.pdf) (25 pp., sha256 `ed3a320c…`), enlazado desde [ir.vesta.com.mx](https://ir.vesta.com.mx/). La versión en español es el [Reporte Trimestral 3T 2026](https://d1io3yog0oux5.cloudfront.net/_a97d61def23f5b56c47196ea9549d7c3/vesta/db/2288/21966/spanish_quarterly_results/Reporte+Trimestral+3T+2026+VF.pdf). Cotejado con:
- el XBRL IFRS entregado a la BMV el 22-oct a las 14:00: [ifrsxbrl_1597180_2026-03_1.zip](https://www.bmv.com.mx/docs-pub/ifrsxbrl/ifrsxbrl_1597180_2026-03_1.zip) (sha256 `31ca424f…`; `Revenue` jul-sep 2026 = 79,563 miles; `DilutedEarningsLossPerShare` = 0.12, redondeado a dos decimales);
- y el 6-K ante la SEC ([ex-99.1](https://www.sec.gov/Archives/edgar/data/1969373/000196937326000018/quarterlyreport3q2026ex-991.htm)).

No hubo evento relevante de resultados en la BMV: la lista de [VESTA-7793](https://www.bmv.com.mx/es/emisoras/eventosrelevantes/VESTA-7793-CGEN_CAPIT) solo trae "Movimientos inusitados" del 21-oct.

Trimestre jul-sep 2026 (no el acumulado de 9 meses):
- **Ingresos totales: 79.6** (+9.9% a/a contra 72.4).
  - Rentas: 74.0. Servicios reembolsables: 3.5. Energía: 2.1. Sin energía: 77.5 (+10.8%).
- NOI ajustado: 72.9 (margen de 94.1%). EBITDA ajustado: 65.2 (margen de 84.1%). Vesta FFO: 47.1 (−0.7%); por acción, 0.0501 (−9.2%, por la dilución).
- Ganancia por revaluación de propiedades: **+60.2** (+4.8 un año antes). Costos financieros: 18.1; intereses ganados: 2.8.
- Utilidad antes de impuestos: 104.0. Impuestos: **beneficio de 6.7** (corriente −13.4 y diferido +20.1). **Tasa efectiva: −6.4%** (beneficio; 52.4% de gasto en el 3T25; cálculo propio con el XBRL: −6.661 / 103.978).
- Utilidad del periodo: 110.6. **UPA diluida (cuadro Financial Indicators): US$0.1199** (0.0322 en el 3T25). Acciones promedio: 939.0 M.
- **Nota:** 110.6 / 939.0 da 0.1178 (cálculo propio), por debajo de la diluida reportada. La diferencia no se explica en el comunicado (no verificado; quizá otro denominador). El criterio manda la cifra del cuadro: **0.1199**. Con 0.1178, la resolución no cambia: queda dentro del intervalo y arriba de 0.04.
- Operación: ocupación total de **93.9%** (+220 pb t/t); 1.6 M pies² de contratos nuevos (récord) y 2.3 M en total. Guía de 2026 elevada: ingresos de +11.5-12.5% (antes +10-11%).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos totales 3T26 (USD M, con energía) | 80.4 (78.0-83.0) | 81.3 | 79.6 | +1.01% | +2.14% | Dentro del 80% |
| UPA diluida 3T26 (USD) | 0.060 (0.005-0.120) | 0.04 | 0.1199 | −49.96% | −66.64% | Dentro del 80%, en el borde (p90 = 0.120) |
| P(ingresos > 81.3) | 0.30 | — | No | — | — | Brier 0.0900 |
| P(UPA > 0.04) | 0.62 | — | Sí | — | — | Brier 0.1444 |

Brier promedio de los binarios: **0.1172**. Los dos puntos fueron mejores que el consenso.

## 3. Matriz y lectura
- **Ingresos: buen proceso, buen resultado.** El punto (80.4) y el sesgo contra el consenso (p = 0.30 de superarlo) fueron correctos. El pequeño error viene de la energía (2.1 contra 2.5 supuesta) y de los reembolsos. La ocupación subió más de lo supuesto (93.9% al cierre contra ~92% promedio), pero los contratos nuevos aportan poco en el mismo trimestre en que se firman.
- **UPA: resultado dentro del intervalo por amplitud, no por precisión.**
  - El punto se equivocó a la mitad (−50%). Las dos partidas que se señalaron como volátiles se fueron en contra: revaluación de +60.2 contra +20 supuesta, e impuestos con beneficio de +6.7 contra un gasto de −10. Juntas suman ~+57 M antes de dilución, ≈ +0.06 por acción (cálculo propio), que es justo el error.
  - Lo operativo se acertó: EBITDA ajustado de 65.2 contra ~65, y costo financiero neto de ~−15.3 contra −14 − 2.5 de *make-whole* (el monto del *make-whole* no se revela por separado).
  - Matriz: **buena decisión (intervalo amplio a propósito, documentado) y buen resultado, con suerte en el borde**. El real (0.1199) queda a 0.0001 del p90. La ficha anticipaba un sesgo a la baja por la depreciación del peso; el diferido salió a favor (+20.1).
- **Binarios.** Ingresos > 81.3 con p = 0.30: buena decisión y buen resultado. UPA > 0.04 con p = 0.62: buena decisión y buen resultado. Con una revaluación positiva probable por la ocupación al alza, pudo ser ~0.70.
- **Qué se sabía el 25-sep:** el prepago de US$105 M (9-sep), las mejoras de calificación (S&P y Fitch) y el arrendamiento fuerte que la empresa ya mencionaba. El rebote de ocupación anticipaba revaluación positiva.
- **Qué no se podía saber:** el monto de la revaluación (avalúos trimestrales) ni la estimación anual de la tasa efectiva que la empresa aplica cada trimestre ("estimated its 2026 effective tax rate"). La tasa es negativa en 9M26 (beneficio de 12.8 sobre 300.7).
- **Escenario (§7):** ocupación total de 93.9% (≥ 92.5% apunta al alcista) y contratos nuevos de 1.6 M pies² (≥ 1 M). Las dos señales de la §7 apuntan al **alcista**, y la guía de ingresos sube. Falta el T-MEC. Se anota en la adenda sin cambiar las probabilidades.

## 4. Lecciones (cada una cambia algo concreto)
1. **En FIBRAs y desarrolladores IFRS de valor razonable, el punto de UPA debe salir de la revaluación esperada, no de un supuesto fijo.** Checklist de la §8: modelar la revaluación con el cambio de ocupación y de *cap rate* del trimestre. En el 3T26, una ocupación +220 pb t/t y la mejora de calificación apuntaban a revaluación alta. Registrar también un pronóstico de FFO por acción, que es la variable estable (aquí, 0.0501).
2. **Tasa efectiva:** −6.4% (beneficio) contra un gasto de ~10% supuesto. Vesta estima una tasa anual y la reparte; leer la tasa acumulada del año (9M26: beneficio) antes de suponer gasto. Es el cuarto caso de tasa mal supuesta en la semana (AMX, BOLSA, ASUR y Vesta). Regla: anotar la tasa de los últimos 4 trimestres y la del acumulado del año junto al supuesto.
3. **Ingresos con energía:** la energía (~2-2.5 M) es volátil y está pegada a su costo. El criterio con energía funcionó; mantenerlo, pero registrar también el de sin energía (77.5), que es la base de la guía.

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`: las cifras del 3T25 de la ficha (ingresos de 72.4, UPA de 0.0322 y FFO de 47.4) coinciden con la columna comparativa del comunicado.
