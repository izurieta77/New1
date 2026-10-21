# Post-mortem · Tesla (TSLA) · 3T26 (reportado el 21-oct-2026, después del cierre)

> Rutina de cierre, 21-oct-2026 (~21:40 UTC). Los pronósticos se registraron el 25-sep en `empresas/TSLA/pronosticos.csv`, antes del resultado. Las resoluciones están en `empresas/TSLA/resoluciones.csv`. La fecha estimada en la ficha (~21-oct) fue correcta. Fase 0.

## 1. Resultado real (fuente primaria)
8-K del 21-oct-2026 (ítems 2.02 y 9.01), Q3 2026 Update, Ex. 99.1 ([SEC](https://www.sec.gov/Archives/edgar/data/1318605/000162828026066738/exhibit9914.htm)).

| Concepto | 3T26 | Comparación |
|---|---|---|
| **Ingresos totales** | **US$28,046 M** | ~plano a/a (3T25: 28,095); 2T26: 28,236 |
| Automotriz | 20,560 M (créditos regulatorios 113 M) | 3T25: 21,205 |
| Energía | 2,881 M | 2T26: 3,139 |
| Servicios y otros | 4,605 M | 2T26: 4,581 |
| Margen bruto total | 19.6% (5,494 M) | 2T26: 16.8% |
| Margen automotriz sin créditos | 18.1% | 2T26: 16.3% |
| Gastos operativos | 4,776 M | 2T26: 4,353 |
| Utilidad de operación | 718 M (2.6%) | −322 pb a/a |
| UPA GAAP diluida | 0.22 | 3T25: 0.39 |
| **UPA non-GAAP diluida** | **0.48** | 3T25: 0.50; 2T26: 0.33 |
| FCF | 1,531 M | flujo operativo 6,263; capex 4,732 |
| Entregas / producción | 486,532 (−2%) / 464,391 (+4%) | — |
| Almacenamiento desplegado | 13.7 GWh | 2T26: 13.5 |
| Suscripciones FSD activas | 1.74 M | 2T26: 1.48 |

- **Partidas excluidas de la non-GAAP:** ganancia no realizada en activos digitales de 288 M antes de impuestos (224 netos; −0.06 por acción), pérdida en SpaceX de 142 M (108 netos; +0.03) y partidas fiscales de 44 M netos (+0.01, pilar dos). Sin reestructura.
- **Guía:** sin cifras. "Maximum capacity utilization at our factories"; entregas sujetas a demanda, cadena de suministro y asignación a la flota propia.
- **Reacción (provisional, Yahoo chart, secundaria):** cierre regular de US$386.47; ~US$379.21 a las 21:41 UTC, **−1.9%**, después de tocar ~391.8 a las 20:30. La reacción del día se mide con el cierre del 22-oct.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos totales | 27,800 (26,000-29,500) | 27,524 | 28,046 | −0.88% | −1.86% | Dentro del 80% |
| UPA non-GAAP | 0.38 (0.26-0.50) | 0.4556 | 0.48 | −20.83% | −5.08% | Dentro del 80%, a 0.02 del p90 |
| P(ingresos > 27,524) | 0.55 | — | Sí | — | — | Brier 0.2025 |
| P(UPA non-GAAP > 0.4556) | 0.28 | — | Sí | — | — | Brier 0.5184 |

Brier promedio de los binarios: **0.3605** (el peor de la ronda).

## 3. Matriz y lectura
- **Ingresos: buen proceso, buen resultado.** Punto más cerca que el consenso. Las entregas (486.5 mil) superaron nuestro supuesto (~465 mil) y el ingreso automotriz por unidad fue menor (~41.3 mil contra 42 mil supuesto); se compensaron.
- **UPA non-GAAP: mal proceso, mal resultado.** El binario en 0.28 y el punto ~8 centavos bajo el consenso se anclaron en la decepción del 2T (0.33, −39%), que venía de un cargo de garantía en energía, no repetible. Supusimos margen bruto de 17.5-18.5%; fue 19.6%. La ficha misma decía que el cargo del 2T no se repetiría: el ajuste correcto era revertir hacia la UPA de los trimestres sin cargo (0.41-0.50), no quedarse abajo del consenso.
- **Qué se sabía el 25-sep:** el cargo de garantía del 2T era único; producción limitada por baterías; base difícil del 3T25.
- **Qué se supo el 2-oct (después del registro):** entregas de 486.5 mil, arriba de nuestro punto. Los pronósticos no se modifican, pero la ficha no tenía regla para anotar esa lectura intermedia.
- **Qué no se podía saber:** la recuperación del margen automotriz a 18.1% sin créditos y la caída de energía a 2.9 mil M.
- **Escenario:** entregas estables, energía a la baja t/t y robotaxi sin cifras nuevas. Sigue en el **base**; el FCF positivo (1.5 mil M) contradice por ahora el FCF del 2S de −8 a −10 mil M que inferimos en el expediente.

## 4. Lecciones (cada una cambia algo concreto)
1. **Después de un trimestre con una partida única que la empresa no repite, el punto y el binario parten de la serie sin la partida, no del último dato.** Regla para la rutina de fichas: en §8, documentar la UPA "limpia" de los últimos 4 trimestres antes de fijar el punto.
2. **Un binario muy lejos de 0.5 contra el consenso exige evidencia explícita.** Con 0.28 apostamos fuerte contra 25 analistas sin una causa nueva (solo el ancla del 2T). Propuesta de parámetro: si |p − 0.5| > 0.2 en un binario contra consenso, la ficha debe nombrar la causa concreta; si no, usar la tasa base.
3. **Usar el reporte de entregas (~2 días después del trimestre) como lectura intermedia registrada**, sin modificar el pronóstico original: agregar una adenda con la implicación para ingresos y UPA. Checklist de la ficha de TSLA.
4. **El supuesto de FCF del 2S (−8 a −10 mil M) quedó en duda:** capex del 3T de 4.7 mil M contra >25 mil M anuales guiados. Revisar en la próxima ficha si Tesla bajó la guía de capex (no aparece en el Update).

No hay errores de hecho para `conocimiento/registro-de-errores.md`. Los binarios son del orquestador (autor claude), no votos de comité, así que no se actualiza `competencia/calibracion-agentes.csv`.
