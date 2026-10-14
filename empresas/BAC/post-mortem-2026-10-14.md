# Post-mortem · Bank of America (BAC) · 3T26 (reportado el 14-oct-2026, antes de la apertura)

> Rutina de Cierre, 14-oct-2026. Los pronósticos se registraron el 25-sep en `empresas/BAC/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado. Las resoluciones están en `empresas/BAC/resoluciones.csv`. No hay posición en BAC ni pasó por comité, así que no hay decisión de cartera ni votos de agentes que evaluar: solo pronósticos.

## 1. Resultado real (fuente primaria)
8-K del 14-oct-2026, ex. 99.1 ([comunicado](https://www.sec.gov/Archives/edgar/data/70858/000007085826000481/bac09302026ex991.htm); [índice](https://www.sec.gov/Archives/edgar/data/0000070858/000007085826000481/)). Las cifras se verificaron dos veces en la fuente: en la tabla y en la narrativa.
- **Ingresos netos de gasto por intereses (GAAP):** US$29,958 M. En base FTE son 30,119 M. El 2T26 fue de 31,558 M y el 3T25 de 29,040 M (+3.2% a/a). La narrativa dice "*Revenue, net of interest expense, of $30.0 billion ($30.1 billion FTE)*".
- **Utilidad neta:** US$6,933 M. **UPA diluida GAAP:** 0.91, contra 1.04 en el 3T25 y 1.21 en el 2T26, con 7.22 mil M de acciones diluidas promedio.
- **Partida significativa:** un cargo de US$1.2 mil M en gasto no deducible de impuestos por las multas civiles (*civil money penalties*) de las órdenes de consentimiento de la OCC y FinCEN sobre sus programas BSA/AML y de sanciones económicas. Restó US$0.17 por acción. Sin el cargo, la utilidad sería de 8.1 mil M, la UPA de **1.08**, el gasto de 18.5 mil M, el ROTCE de 14.9% y la eficiencia de 62%.
- **Desglose:** el NII GAAP fue de 16,449 M (16,610 FTE; +8% a/a) y las comisiones de 13,509 M (−2% a/a). El trading (S&T) fue de 5,075 M (renta fija −17% y acciones +11%). Las comisiones de IB, sin las propias, fueron de 1.8 mil M, dentro de la guía de 1.6-1.8. La provisión fue de 1,269 M, con castigos netos (NCO) de 1,349 M (0.44%). El gasto fue de 19,722 M y la tasa efectiva de ~23% (~20% sin el cargo).
- **Capital y otros:** CET1 estandarizado de 10.9% (11.2% en el 2T). Devolvió 8.3 mil M: 6.0 de recompras y 2.2 de dividendos. ROTCE de 12.6%. Préstamos promedio de 1.23 billones (+6%) y depósitos de 2.02 billones (+2%).
- **Reacción del precio (Yahoo, fuente secundaria):** cerró en 51.39, contra 53.96 el 13-oct (**−4.76%**). La multa se anunció el 13-oct después del cierre: el Tesoro informó de FinCEN por 1,200 M, OCC por 750 M y OFAC por 11.66 M, y en el after-hours BAC ya bajaba ~2.3% (`bitacora/pronosticos.csv`, P0118). El reporte no cerró la brecha, sino que la amplió.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro | Consenso | Real | Error nuestro | Error consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos GAAP (punto; p10-p90) | 30,350 (29,600-31,200) | 31,157 | 29,958 | +1.31% | +4.00% | Dentro del intervalo de 80% |
| UPA diluida GAAP (punto; p10-p90) | 1.13 (1.05-1.22) | 1.165 | 0.91 | +24.18% | +28.02% | **Fuera** del intervalo (0.14 bajo el p10) |
| P(ingresos > 31,157) | 0.13 | — | No | — | — | Brier 0.0169 |
| P(UPA GAAP > 1.16) | 0.33 | — | No | — | — | Brier 0.1089 |

El error es (pronóstico − real) / real. El Brier promedio de nuestros dos binarios es **0.0629**. Con la tasa base de FactSet (70% de los reportes superan el consenso de ingresos y 78% el de UPA) habría sido 0.49 y 0.6084 (promedio 0.549). Con 0.50 constante habría sido 0.25.

Los dos binarios resuelven "No" en cualquier base, así que no dependen del criterio:
- Ingresos: los FTE (30,119) también quedan abajo del consenso de 31,157. Este es el problema de base que se vio con JPM el 13-oct, y aquí no cambia el resultado.
- UPA: sin la multa (1.08) también queda abajo de 1.16.

## 3. Matriz y lectura
- **Ingresos: buena decisión y buen resultado.** La apuesta contraria del lote (p = 0.13 de superar el consenso) se apoyaba en un dato público que el consenso no había absorbido: la guía de Moynihan del 14-sep de IB de 1.6-1.8 mil M y trading plano. El dato salió como se guió: IB de 1.8 y S&T de 5.1 contra 5.4 del 3T25. Nuestro punto erró en 1.31% y el consenso en 4.00%. Por componente:
  - NII: modelamos 16.35 y salió 16.45.
  - Comisiones: modelamos 14.0 y salieron 13.5. Renta fija cayó 17%, más de lo que suponía un trading "plano".
- **UPA: decisión razonable en dirección, mala en el intervalo.** Puente aproximado de 1.13 a 0.91 (cálculo propio):

  | Componente | Efecto en UPA |
  |---|---|
  | Multa | −0.17 |
  | Ingresos 392 M abajo | ≈ −0.04 |
  | Gasto sin multa de 18.52 contra 18.30 | ≈ −0.02 |
  | Provisión de 1.27 contra 1.40 | ≈ +0.015 |
  | Acciones de 7.22 contra 7.19 mil M | ≈ −0.005 |
  | **Suma** | **≈ 0.90**, contra 0.91 real |

  Sin la multa, el error habría sido de +4.6% (1.13 contra 1.08), dentro del intervalo y mejor que el consenso. **Casi todo el error y la salida del intervalo vienen de la partida no recurrente.**
- **Suerte contra calidad.** El Brier bajo de los binarios es en parte suerte: la multa empujó la UPA hacia donde ya apostábamos. Aun así, el "No" en UPA se habría cumplido sin la multa (1.08 < 1.16), así que el acierto lo sostiene el modelo y no solo la partida. Lo mismo vale para ingresos, donde la multa no influye.
- **Qué se sabía el 25-sep:**
  - La guía de IB y trading del 14-sep.
  - El NII guiado en la parte alta de 6-8%.
  - Que BAC opera bajo una orden de consentimiento de la OCC sobre BSA/AML (dic-2024, sin multa entonces). Esto es de memoria y no se verificó en fuente hoy.

  Que una orden así termine en multa civil es un riesgo conocido de cola. La ficha no lo listaba entre los riesgos.
- **Qué no se podía saber:** el monto (1.2 mil M, no deducible) ni que se anunciara en esta ventana. Se hizo público el 13-oct después del cierre, 18 días después del registro.
- **Escenario:**
  - El NII de 16.45 mil M es mayor que 16.2, así que no activa el bajista.
  - Las recompras de 6.0 mil M están en línea con el base (~6 por trimestre).
  - Sigue el **base**, con dos salvedades: el CET1 bajó a 10.9%, y el ROTCE ajustado de 14.9% queda abajo de la meta de 16-18%. Si en el 4T26 no regresa a ≥ 16%, el precio deja de descontar que se cumpla la meta (§6 de la ficha).

## 4. Lecciones (cada una cambia algo concreto)
1. **Riesgo regulatorio pendiente: dentro del intervalo de UPA GAAP.** Si una empresa tiene órdenes de consentimiento abiertas o litigios con resolución probable, el p10 de la UPA GAAP se amplía hacia abajo en una cola de multa. Para un banco grande, del orden de 0.5-1.5% del capital tangible del trimestre. Además, se registra por separado un pronóstico de "UPA sin partidas". Se aplica a la plantilla de la §8 de `ficha-empresa` como propuesta; la skill no se modifica sin aprobación. Es la misma lección 2 del post-mortem de JPM (partidas significativas), ahora con n = 2.
2. **Guía pública intratrimestral: el insumo con más valor del lote.** La guía de mediados de trimestre en conferencias (Barclays, 14-sep) pesó más que el consenso de los agregadores. Regla: en la §8 se anota la fecha de la última revisión del consenso contra la fecha de la guía. Si el consenso es anterior, se ajusta el binario hacia el lado de la guía, como se hizo aquí con p = 0.13.
3. **Sesgo optimista acumulado en puntos de UPA:** JPM +7.5%, BAC +24.2% (+4.6% sin multa) y MS +9.6%. Los 6 puntos numéricos del 13 y 14-oct (JPM, BAC y MS) quedaron arriba del real. Parámetro propuesto para el próximo lote de bancos: descontar 3% al punto de UPA del modelo salvo evidencia específica, y revisar en el 4T26 si el sesgo persiste.
4. **Tasa base:** nuestros binarios de BAC ganaron con claridad a la tasa base (0.063 contra 0.549). Fue la única empresa del lote donde nos apartamos fuerte de la tasa base y la razón era un dato concreto. Esto respalda la regla de `conocimiento/fichas/2026-10-13-pronostico-de-resultados-tasa-base.md`: partir de la tasa base y moverse solo con evidencia fechada.

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`: las cifras de la ficha eran correctas y los errores fueron de supuestos (comisiones) y de un riesgo omitido (la multa). Los pronósticos se resolvieron en `empresas/BAC/resoluciones.csv`. No se ejecutó `herramientas/pronosticos.py resolver` porque esta rutina no edita `bitacora/pronosticos.csv`. Como no hubo comité, no se actualiza `competencia/calibracion-agentes.csv`.
