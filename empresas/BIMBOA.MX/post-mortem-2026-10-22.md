# Post-mortem · Grupo Bimbo (BIMBOA.MX) · 3T26 (reportado el 22-oct-2026, después del cierre)

> Rutina de cierre, 22-oct-2026 (~21:45 UTC). Los pronósticos se registraron el 25-sep en `empresas/BIMBOA.MX/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado, y no se modifican. Las resoluciones están en `empresas/BIMBOA.MX/resoluciones.csv`. Sin posición en BIMBO: no hay decisión de cartera ni votos del comité que evaluar, solo pronósticos del orquestador. No se ejecutó `herramientas/pronosticos.py resolver` ni se tocaron `bitacora/pronosticos.csv` ni `competencia/calibracion-agentes.csv` (fuera del alcance de esta tarea). Fase 0.

## 1. Resultado real (fuente primaria)
- **Comunicado de resultados** en la página de inversionistas de Grupo Bimbo, "Grupo Bimbo Reports 3Q26 Results" (8 pp., fechado el 22-oct-2026; sha256 `d35fa93d…`): [PDF](https://d2rwhogv2mrkk6.cloudfront.net/s3fs-public/eventos-2026/Grupo%20Bimbo%20Reports%203Q26%20Results.pdf?VersionId=sFGKSk8Jl28MvkT9bKXsoSaeviHg_1m8).
- **Reporte trimestral en la BMV** (XBRL IFRS, "Información del trimestre 3 del año 2026", enviado el 22-oct-2026 a las 14:00 hora de CDMX): [ifrsxbrl_1597181_2026-03_1.zip](https://www.bmv.com.mx/docs-pub/ifrsxbrl/ifrsxbrl_1597181_2026-03_1.zip) (sha256 `e81981f1…`). Las ventas y la UN mayoritaria cuadran con el comunicado.

| Concepto | 3T26 | Comparación |
|---|---|---|
| **Ventas netas** | **Ps 106,061 M** (XBRL 106,060.6) | −1.3% en pesos; +3.6% sin tipo de cambio. 3T25 en este reporte: 107,427 (la ficha usaba 107,421) |
| Utilidad bruta | 56,299 M (53.1%) | +80 pb |
| Utilidad de operación | 10,390 M (9.8%) | +10.5%; +100 pb |
| **UAFIDA ajustada** | **16,644 M; margen de 15.7%** (16,644 / 106,061 = 15.69%, cálculo propio) | +5.5% (+9.3% sin tipo de cambio); 3T25: 15,776 (14.7%) |
| Costo financiero neto | 3,142 M | −5.9%: intereses 2,829, pérdida cambiaria 194, posición monetaria 119 |
| Impuestos | 2,682 M; tasa de 37.0% (2,682 / 7,249, cálculo propio) | igual al supuesto |
| Minoritario | 458 M | supuesto: ~460 |
| **UN mayoritaria** | **4,109 M** (XBRL 4,108.5) | +22.1% |
| **UPA reportada en la BMV** | **Ps 0.96** (básica y diluida, XBRL) | 3T25: 0.78. Con 4,304.7 M acciones en circulación al 30-sep: 0.954; neta de 20.2 M recompradas: 0.959 (cálculos propios) |
| Deuda neta / UAFIDA (sin IFRS 16) | 2.4x | dic-25: 2.7x |

- **Regiones (margen UAFIDA ajustada):** Norteamérica 10.8% (+40 pb; ventas +1.0% sin tipo de cambio); México 22.4% (+200 pb; ventas +5.2%); EAA 12.3% (+110 pb); Latinoamérica 7.3% (−130 pb, por Brasil y Wickbold).
- **Reacción del precio:** no observable todavía (el reporte salió tras el cierre del 22-oct).

## 2. Pronósticos contra resultado
El error es (punto − real) / real, con la misma convención que `empresas/AMXB.MX/resoluciones.csv`.

| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ventas netas | 106,300 (103,600-109,000) | 106,340 | 106,061 | +0.23% | +0.26% | Dentro del 80%, casi en el centro |
| UPA (reportada en la BMV) | 0.82 (0.66-0.97) | 0.866 | 0.96 | −14.6% | −9.8% | Dentro, **a un centavo del p90** |
| P(ventas > 106,340) | 0.50 | — | No (106,061) | — | — | Brier 0.2500 |
| P(margen UAFIDA ajustada > 14.7%) | 0.70 | — | Sí (15.69%) | — | — | Brier 0.0900 |

Brier promedio de los dos binarios: **0.1700**.

## 3. Matriz y lectura
- **Ventas: buen proceso, buen resultado.** El punto se construyó región por región, con el efecto cambiario explícito (−7.5% en Norteamérica, −8% en EAA). El total quedó a 0.2% del real, un poco mejor que el consenso. La mezcla salió distinta: Norteamérica creció menos (+1.0% contra +1.5% supuesto), Latinoamérica bastante más (+12.4% en pesos contra +4.5%) y EAA menos (+2.1% sin tipo de cambio contra +8%). Los errores se compensaron, así que parte del acierto en el total fue suerte.
- **Binario de ventas (0.50): proceso correcto, resultado neutro.** El punto estaba a 40 M del umbral, y 0.50 era coherente con el intervalo (la ficha calculó que el intervalo implicaba 0.49). Salió No por 0.26%. Brier 0.25: ni gana ni pierde información, que es lo que se buscaba con una moneda al aire.
- **Binario de margen (0.70): buena decisión, buen resultado.** La guía implicaba ~15.0-15.9% para el 2S26, y el real fue 15.7%. En retrospectiva, 0.70 fue tímido: con la guía subida en julio y el umbral (14.7%) debajo de todo el rango implícito, 0.80-0.85 era defendible.
- **UPA: punto pesimista; el intervalo salvó la puntuación.** Descomposición (cálculo propio):
  - Modelo de la §8 (margen de 15.0%, costo financiero de 3.45 mil M, tasa de 37%, minoritario de 460 M y 4,300 M acciones): ~0.82.
  - Con el margen real (15.7%) y el costo financiero supuesto: ~0.91. **El margen explica ~0.06-0.07.**
  - Con el costo financiero real (3,142 contra 3,450): ~0.96. **El costo financiero explica ~0.04-0.05.**
  - La tasa (37.0%) y el minoritario (458) se acertaron.
  - **Por qué falló:** el margen se puso en el piso del rango que la propia guía implicaba (15.0%), no en el centro. El costo financiero se extrapoló del 2T26 (3,464, inflado por las coberturas de energía), sin tomar en cuenta que la deuda neta bajaba (de 137 a 135 mil M) y que el 3T25 había sido de 3,337.
- **El sesgo histórico no se repitió.** El verificador del 25-sep alertó que el punto (0.82) "parece alto" porque la UPA había quedado debajo del consenso en 8 de 8 trimestres. El resultado superó al consenso por +10.9%. La tasa base apuntaba en la dirección equivocada este trimestre. El punto, debajo del consenso, siguió esa alerta y perdió. **Esto es mala suerte frente a la tasa base, pero también un error de modelo**, porque los dos componentes del fallo (margen y costo financiero) eran visibles en la guía y en el balance.
- **Qué se sabía el 25-sep:**
  - la guía de margen subida (+70-120 pb en el año);
  - el 1S26 en 14.2%, que obligaba a ~15.0-15.9% en el 2S;
  - la tendencia de la deuda neta a la baja;
  - que el costo financiero del 2T26 traía el efecto puntual de las coberturas de energía (VPPA).
- **Qué no se podía saber:** la magnitud de la expansión en México (+200 pb, con menor costo de ventas y gasto administrativo) y una pérdida cambiaria casi nula (194 M).
- **Escenario:** Norteamérica cerró en 10.8%, dentro del rango 10-11% que la ficha fijó como disparador. Deuda neta / UAFIDA de 2.4x, en el rango base (2.3-2.4x). UN de 9M26 de 9,406 M, que anualizada encaja en la parte alta del base (Ps 12-13 mil M) o en el alcista (más de 13.5 mil M) según el 4T. Se mantiene el **escenario base**, con sesgo alcista.

## 4. Lecciones (cada una cambia algo concreto)
1. **Margen de UPA en el centro del rango implícito de la guía, no en el piso.** Regla para la §8 de las fichas con guía de margen anual: calcular el margen implícito del resto del año y usar su punto medio como supuesto central, salvo que haya un argumento cuantificado para desviarse. Aquí, 15.4% en vez de 15.0% habría dado una UPA de ~0.86.
2. **Costo financiero: partir del trimestre comparable y de la tendencia de la deuda, no solo del trimestre previo**, sobre todo cuando el previo trae partidas puntuales (coberturas de energía, tipo de cambio). Checklist de la §8: anotar el costo financiero de los últimos 4 trimestres y la deuda neta junto al supuesto.
3. **Las tasas base de "falla al consenso" se rompen cuando cambian los motores.** Los 8 fallos previos venían del costo financiero y de la tasa fiscal. Cuando la guía de margen sube y la deuda baja, la tasa base pesa menos. La alerta del verificador debe nombrar el mecanismo del sesgo histórico y comprobar si sigue vigente; si no, no debe mover el punto.
4. **Binarios con umbral debajo de todo el rango implícito de la guía:** p ≥ 0.80, salvo un riesgo identificado (aquí, energía y trigo, que no se materializaron en el trimestre).

**Dato a corregir (no se editó ningún otro archivo):** las ventas del 3T25 que este reporte usa como comparación son 107,427 M (XBRL 107,427.3). La ficha y el criterio del binario de margen usaban 107,421. El margen base no cambia (15,776 / 107,427 = 14.69%), así que la resolución del binario no se ve afectada. Queda como candidato para `conocimiento/registro-de-errores.md` (reexpresión o lectura); no se editó por alcance.
