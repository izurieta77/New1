# Post-mortem · JPMorgan Chase (JPM) · 3T26 (reportado el 13-oct-2026, antes de la apertura)

> Rutina de Cierre, 13-oct-2026. Los pronósticos se registraron el 25-sep, en `empresas/JPM/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado. Las resoluciones están en `empresas/JPM/resoluciones.csv`. Sin posición en JPM y sin comité: no hay decisión de cartera ni votos de agentes que evaluar, solo pronósticos.

## 1. Resultado real (fuente primaria)
8-K del 13-oct-2026, ex. 99.1 ([comunicado](https://www.sec.gov/Archives/edgar/data/0000019617/000162828026065582/a3q26erfexhibit991narrative.htm)) y ex. 99.2 ([suplemento](https://www.sec.gov/Archives/edgar/data/0000019617/000162828026065582/a3q26erfex992supplement.htm)); las cifras coinciden en los dos:
- **Ingresos netos totales:** US$50,172 M reportados (GAAP) y US$50,907 M administrados (managed, base equivalente fiscal; ajuste FTE de 735).
- **Utilidad neta:** US$15,305 M. **UPA diluida GAAP:** 5.57 (5.07 en el 3T25), con 2,683.0 M de acciones diluidas promedio.
- **Partida significativa:** pérdidas netas de US$658 M en valores de inversión en Corporate (−US$0.18 de UPA). Sin ella, utilidad de 15.8 mil M y UPA de 5.75.
- **Desglose (administrado):** NII de 27.1 mil M (+13%); NII sin Markets de 24.7 (+6%); Markets de 10.3 (+15%; renta fija −4% y acciones +49%); comisiones de IB de 3.0 (+14%). Gasto de 27,295 M; provisión de 2,743 M (castigos netos de 2.2 mil M y creación de reserva de 539 M).
- **Capital y otros:** CET1 estandarizado de 13.9%; NCO de tarjeta de 2.91%; ROTCE de 20% (21% sin la partida). Recompras netas de solo US$664 M: Dimon dijo que "reducimos las recompras" para desplegar capital en el negocio.
- **Reacción del precio:** no consultada en fuente verificable al cierre de esta rutina; no se reporta. **[Nota, conciliación 14-oct-2026 ~03:00 UTC, Yahoo chart v8 1d, consultado 03:0x UTC; fuente secundaria; `bitacora/arbitraje/2026-10-13.md` §6]:** abrió en 339.97 (+1.7% contra el cierre del 12-oct, 334.30) y cerró en 331.43 (−0.86%); es el mismo cierre que resolvió P0064 en NO.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro | Consenso | Real | Error nuestro | Error consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos reportados (punto; p10-p90) | 50,800 (49,400-52,300) | 50,847 | 50,172 | +1.25% | +1.35% | Dentro del intervalo de 80% |
| UPA diluida GAAP (punto; p10-p90) | 5.99 (5.53-6.48) | 5.91 | 5.57 | +7.54% | +6.10% | Dentro del intervalo de 80%, en el borde bajo |
| P(ingresos reportados > 50,847) | 0.50 | — | No | — | — | Brier 0.2500 |
| P(UPA GAAP > 5.91) | 0.60 | — | No | — | — | Brier 0.3600 |

Error = (pronóstico − real) / real. Brier promedio de los dos binarios: **0.305**. Con la tasa base de FactSet (0.70 ingresos y 0.78 UPA) habría sido 0.49 y 0.6084 (promedio 0.549); con 0.50 constante, 0.25.

## 3. Matriz y lectura
- **Proceso razonable, resultado malo en UPA y engañoso en ingresos.** Los dos numéricos cayeron dentro del intervalo y los binarios acertaron que no había "beat" claro, pero el punto de UPA quedó 7.5% arriba y peor que el consenso.
- **Ingresos: el punto era correcto sin la partida significativa.** El modelo administrado tenía NII sin Markets de 24.5 (real 24.7), Markets de 10.4 (10.3), IB de 3.0 (3.0) y resto de 13.5 (12.9; 13.6 sin la pérdida de 658 M en valores). Sin esa pérdida, los ingresos reportados habrían sido ~50,830, prácticamente nuestro 50,800. **El error de +1.25% es casi todo la partida no recurrente**, que el modelo no contemplaba.
- **UPA: el error se reparte en cuatro supuestos optimistas.** Puente aproximado de 5.99 a 5.57 (cálculo propio): partida significativa −0.18; gasto de 27.3 contra 27.0 (≈−0.08); provisión de 2.74 contra 2.5, con creación de reserva por crecimiento de préstamos (≈−0.07); tasa efectiva de ~24.0% contra 23% (≈−0.08); preferentes y acciones casi se compensan. Incluso sin la partida (5.75) la UPA quedó abajo del consenso de 5.91 (Yahoo) y de 5.84 (Zacks): el binario resuelve "No" en cualquier base, así que su resultado no depende del criterio.
- **Binario de ingresos: depende del criterio.** El criterio registrado dice "reportado", y 50,172 < 50,847 → No. Pero los **administrados (50,907) sí superan** el consenso. El consenso de Yahoo para JPM probablemente está en base administrada (no verificado en la metodología del agregador). El binario comparó, entonces, cifras en bases distintas, con ~1.5% de diferencia, casi del tamaño de una sorpresa típica.
- **Qué se sabía el 25-sep:** la guía de NII sin Markets (~96.5 anual), la indicación de Petno de IB y Markets "mid- to high-teens" (resultó mid-teens), que JPM reporta partidas significativas con frecuencia (4T25: reserva de Apple Card, −0.60; 2T26: canje de Visa, +), y que el FTE separa reportado de administrado.
- **Qué no se podía saber:** la venta discrecional de valores con pérdida en Corporate (decisión de la tesorería dentro del trimestre) ni la decisión de recortar recompras.
- **Escenario:** NII de 27.1 mil M (> 26, no activa el bajista); Markets +15% a/a (< 20%, no activa el alcista); NCO de tarjeta de 2.91% (lejos de 3.6%). Sigue el escenario **base**, con una salvedad: el base suponía recompras de ~7 mil M por trimestre y en el 3T fueron de 0.66 mil M. Si el recorte persiste, la UPA 2027 del base (24.5-25.5) pierde parte del apoyo de la recompra.

## 4. Lecciones (cada una cambia algo concreto)
1. **Binarios contra consenso en bancos: misma base que el consenso.** Para JPM (y cualquier banco con ajuste FTE), el binario "ingresos > consenso" se define sobre ingresos **administrados** si el consenso del agregador está en esa base, y el numérico puede seguir en reportados. Además, nuestro propio modelo daba 51.4 administrados (+1.1% sobre el consenso), así que el p = 0.50 era incoherente con el modelo: en base administrada correspondía p ≈ 0.60-0.65; en reportada, ≈ 0.40. Se aplica en la plantilla de la §8 de `ficha-empresa`: anotar la base del consenso junto al umbral (propuesta; la skill no se modifica sin aprobación).
2. **UPA GAAP de JPM: modelar las partidas significativas.** Hubo partidas significativas en 3 de los últimos 4 trimestres (4T25, 2T26 y 3T26), con signo variable. El intervalo GAAP debe ampliarse hacia el lado de la partida probable y el punto debe separar "UPA sin partidas" (comparable con el consenso) de "UPA GAAP". Aquí el p10 de 5.53 cubrió el dato por solo 0.04.
3. **Provisión y gasto con crecimiento de préstamos de +10%:** no repetir la provisión del trimestre anterior; agregar creación de reserva proporcional al crecimiento de la cartera y gasto ligado a ingresos. Parámetro concreto para el próximo pronóstico de JPM: provisión = castigos esperados + ~1% del crecimiento trimestral de préstamos.
4. **Tasa base:** hoy el 0.50 y el 0.60 ganaron en Brier a 0.70 y 0.78 (0.305 contra 0.549). Con n = 2 no se concluye nada; la regla de partir de la tasa base (`conocimiento/fichas/2026-10-13-pronostico-de-resultados-tasa-base.md`) sigue en pie, ajustada por la lección 1.

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`: las cifras de la ficha eran correctas; los errores fueron de supuestos y de definición del criterio. Los pronósticos se resolvieron en `empresas/JPM/resoluciones.csv`; no se ejecutó `herramientas/pronosticos.py resolver` porque esta rutina no edita `bitacora/pronosticos.csv`.
