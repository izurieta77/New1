# Post-mortem · UnitedHealth Group (UNH) · 3T26 (reportado el 13-oct-2026, antes de la apertura)

> Rutina de Cierre, 13-oct-2026. Los pronósticos se registraron el 25-sep, en `empresas/UNH/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado. Las resoluciones están en `empresas/UNH/resoluciones.csv`. Sin posición en UNH: no hay decisión de cartera que evaluar, solo pronósticos.

## 1. Resultado real (fuente primaria)
Comunicado 8-K (Items 2.02 y 9.01), ex. 99.1, del 13-oct-2026 ([SEC](https://www.sec.gov/Archives/edgar/data/731766/000073176626000255/earningsrelease3q26unh.htm)):
- **Total revenues:** US$112,694 M (−0.4% a/a contra 113,161; +0.6% t/t contra 112,032). Los *adjusted revenues* fueron 112,715 M, pero el criterio usa *total revenues*.
- **UPA:** 4.56 GAAP diluida y **4.69 ajustada** (*adjusted net earnings per share*; 2.92 un año antes). Acciones diluidas promedio: 902 M.
- **Índice médico (MCR):** 88.4% contra 89.9% en el 3T25, con **US$610 M de desarrollo favorable neto de reservas** de fechas de servicio de 2026. Índice de costos operativos de 12.8% (13.5% un año antes).
- **Guía 2026:** UPA ajustada de **al menos US$20.50** (antes 19.50-20.00) y GAAP de al menos 19.50.
- **Operación:** UnitedHealthcare, ingresos de 86.3 mil M y utilidad de 2.8 mil M; Optum, 66.9 mil M y 3.7 mil M. MA se contrajo 935 mil personas desde dic-25. Stars 2027: al menos 69% de los afiliados en planes de 4+ estrellas, "en línea con lo esperado". Recompras de US$5.0 mil M. Flujo operativo de 5.1 mil M (1.2x la utilidad neta).
- **Reacción del precio:** no verificada al cierre de esta nota. **[Nota, conciliación 14-oct-2026 ~03:00 UTC, Yahoo chart v8 1d, consultado 03:0x UTC; fuente secundaria; `bitacora/arbitraje/2026-10-13.md` §6]:** abrió en 397.63 (+5.0% contra el cierre del 12-oct, 378.52) y cerró en 377.76 (−0.20%).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro | Consenso | Real | Error nuestro | Error consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos (punto; p10-p90) | 111,900 (110,300-113,300) | 111,489 | 112,694 | −0.70% | −1.07% | Dentro del intervalo de 80% |
| UPA ajustada (punto; p10-p90) | 4.40 (3.90-4.95) | 4.149 | 4.69 | −6.18% | −11.54% | Dentro del intervalo de 80% |
| P(ingresos > 111,489) | 0.62 | — | Sí | — | — | Brier 0.1444 |
| P(UPA ajustada > 4.149) | 0.66 | — | Sí | — | — | Brier 0.1156 |

## 3. Matriz y lectura
- **Buen proceso, resultado correcto pero con poca convicción, por segunda vez.** Los dos puntos le ganaron al consenso (por 0.4 pp en ingresos y 5.4 pp en UPA), los dos reales cayeron dentro del intervalo y los dos binarios acertaron la dirección. Pero **los dos puntos volvieron a salir sesgados a la baja**, igual que en MU el 30-sep.
- **Tasa base que no se usó:** según FactSet, en 5 años el 70% de las empresas del S&P 500 supera el consenso de ingresos y el 78% el de UPA. Además, la propia ficha decía que UNH superó el consenso de UPA en 4 de 4 trimestres. Con un 0.70 y un 0.78 constantes, el Brier habría sido 0.0900 y 0.0484 (promedio 0.069), contra **0.130 nuestro**. Las p de 0.62 y 0.66 quedaron *por debajo* de la tasa base genérica, sin una razón específica registrada para descontarla.
- **Qué se sabía el 25-sep:** la guía había sido conservadora (dos subidas en 2026), el 2T traía US$860 M de reservas favorables y el riesgo central era el MCR.
- **Qué pasó:** el MCR fue de 88.4%, mejor que el ~89.2% que suponía el punto y aun que el ~88.5% asociado al p90. Aun así, la UPA (4.69) quedó por debajo del p90 (4.95): el mapeo MCR → UPA de la ficha (~US$0.78 por punto) no se cumplió uno a uno, porque también se mueven el índice de costos, Optum y los ajustes no-GAAP. *Inferencia:* sin los US$610 M de reservas favorables (~US$0.55 por acción después de impuestos, con una tasa de 18.5% y 902 M de acciones), la UPA ajustada habría sido de ~4.14, casi igual al consenso. La sorpresa depende otra vez de liberar reservas, y esa fuente no es recurrente.
- **Qué no se podía saber:** el monto del desarrollo de reservas y el momento de reconocerlo.
- **Escenario:** la guía de al menos 20.50 supera el rango del escenario **base** (20.0-20.3), pero el **alcista** exige una guía 2027 mayor a 23.5 y un MCR anual de 88% o menos, que aún no se conocen. Queda en **base con sesgo alcista** hasta la guía 2027 (ene-2027). El disparador bajista (MCR mayor a 90%) no ocurrió.

## 4. Lecciones (cada una cambia algo concreto)
1. **Binarios de "supera al consenso": el piso es la tasa base.** Es la misma lección de MU (30-sep) y no se había aplicado porque los pronósticos de UNH son del 25-sep. Regla para la plantilla de `ficha-empresa`: anotar la tasa base de FactSet (70% ingresos y 78% UPA) y el historial de la emisora antes de fijar p; para bajar de la tasa base hay que registrar por escrito la causa específica. Para UNH, con 4 de 4 sorpresas de UPA y una guía conservadora, lo coherente era p ≈ 0.80 en UPA y ≈ 0.70 en ingresos.
2. **Aseguradoras: separar las reservas en el pronóstico de UPA.** Pronosticar la UPA "antes de desarrollo de reservas" y sumar aparte un supuesto explícito de liberación (mediana de los últimos trimestres: 860 M en el 2T y 610 M en el 3T) [nota, conciliación 14-oct-2026: con dos trimestres la "mediana" es el promedio, **735 M**; con n = 2 tómese como referencia, no como tasa base]. Así se ve qué parte de la sorpresa es operación y qué parte es contable.
3. **Brier de estos dos binarios:** 0.130 promedio. Con MU, n = 4 y un promedio de 0.157, peor que la tasa base constante. La muestra es pequeña, pero el sesgo tiene la misma dirección en los 4 casos: puntos bajos y p tímidas.

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`. Una discrepancia menor: la §1 de la ficha dice que MA bajó 965 mil personas desde dic-25 al 30-jun, y el comunicado del 3T dice 935 mil al 30-sep, con una definición que incluye programas para poblaciones complejas de Medicaid. Por eso no son comparables directamente; no se corrige sin revisar la definición.
