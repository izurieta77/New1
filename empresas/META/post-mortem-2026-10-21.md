# Post-mortem · Meta Platforms (META) · 3T26 (reportado el 21-oct-2026, después del cierre)

> Rutina de cierre, 21-oct-2026 (~21:40 UTC). Los pronósticos se registraron el 25-sep en `empresas/META/pronosticos.csv`, antes del resultado. Las resoluciones están en `empresas/META/resoluciones.csv`. La ficha estimaba el reporte para el 28-oct; Meta publicó una semana antes. P0159 de `bitacora/pronosticos.csv` no se toca: lo resuelve el cierre del 22-oct. Fase 0.

## 1. Resultado real (fuente primaria)
8-K del 21-oct-2026 (ítems 1.01, 2.02, 8.01 y 9.01), comunicado Ex. 99.1 ([SEC](https://www.sec.gov/Archives/edgar/data/1326801/000162828026066700/meta-09302026xexhibit991.htm)).

| Concepto | 3T26 | Comparación |
|---|---|---|
| **Ingresos** | **US$64,601 M** | +26% (también a tipo de cambio constante); 3T25: 51,242 |
| Costos y gastos | 51,613 M | +68%; incluye el cargo legal |
| Utilidad de operación | 12,988 M (margen 20%) | 3T25: 20,535 (40%) |
| Utilidad neta | 9,860 M | 3T25: 2,709 (cargo fiscal OBBBA) |
| **UPA diluida GAAP** | **3.83** | 3T25: 1.05; 2,573 M de acciones diluidas |
| Tasa efectiva | 24% | 17% sin el cargo |
| Reality Labs | pérdida operativa de −4,129 M | 3T25: −4,432 |
| FCF (definición de Meta) | −2.12 mil M | flujo operativo 32.79 mil M |

- **Partida única:** cargo de **US$9.89 mil M** en gastos generales por el acuerdo con 52 fiscales estatales (pagos de hasta ~US$18.59 mil M). Sin él: utilidad de operación de 22.88 mil M y **UPA de 7.40** (+3.57).
- **Datos operativos:** 3.64 mil M de personas activas diarias (+3%); impresiones +10%; precio por anuncio +14%; plantilla de 66,775 (−15%). Sin recompras en el trimestre; dividendos de 1,361 M.
- **Guía (CFO Outlook):** ingresos del 4T26 de **US$73-76 mil M** (punto medio 74.5; tipo de cambio −1%); gastos 2026 de **175-179 mil M** (antes 165-169, sube para incluir el cargo); capex de 135-145 mil M (antes 130-145); pérdida de Reality Labs de 18-19 mil M; tasa del 4T de 15-17%. Sin el cargo, la utilidad operativa 2026 seguiría arriba de la de 2025.
- **Otro evento material (ítem 1.01):** recapitalización con una nueva **acción clase C sin voto** y un dividendo en acciones de una clase C por cada acción A y B, efectivo a partir del 19-ene-2027, con un acuerdo con Zuckerberg ("Founder Alignment Agreement"). Afecta conteos de acciones y UPA por acción desde 2027; revisar antes de la próxima ficha.
- **Reacción (provisional, Yahoo chart, secundaria):** cierre regular de US$697.52; ~US$724.00 a las 21:41 UTC en operación posterior al cierre, **+3.8%**. La reacción del día se mide con el cierre del 22-oct.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos | 63,800 (62,600-64,900) | 63,317 | 64,601 | −1.24% | −1.99% | Dentro del 80%, a 299 del p90 |
| UPA diluida GAAP | 3.20 (2.50-3.95) | 6.404 | 3.83 | −16.45% | +67.21% | Dentro del 80% |
| P(ingresos > 63,317) | 0.72 | — | Sí | — | — | Brier 0.0784 |
| P(punto medio guía 4T > 73,695) | 0.40 | — | Sí (74,500) | — | — | Brier 0.3600 |

Brier promedio de los binarios: **0.2192**.

## 3. Matriz y lectura
- **Ingresos: buen proceso, buen resultado.** El método (punto medio de la guía +2.1%) fue más cerca que el consenso, pero la superación real fue de **+3.4%** sobre el punto medio (64.6 contra 62.5), arriba de los dos trimestres previos (+2.4%, +2.2%) y más cerca de los de 2025 (+4.8%, +4.2%). El real quedó en la parte alta del intervalo.
- **UPA: buen proceso, resultado dentro.** Incluir el cargo legal fue lo correcto: el consenso promedio (6.40) lo excluía y erró por 67%. El error de −16% viene de gastos menores a lo supuesto: sin el cargo, la UPA fue 7.40, contra ~6.6 implícita en nuestro punto. La tasa efectiva (24%) fue mayor a la supuesta (16%) y aun así quedamos cortos: los gastos operativos sin el cargo (~41.7 mil M) fueron menores que nuestro reparto del 2S.
- **Guía del 4T: mal proceso, mal resultado (Brier 0.36).** Asignamos 0.40 con el argumento de que "Meta guía por debajo de lo que termina reportando". Eso describe la relación guía → real, no guía → consenso. El consenso del 4T (73.7) ya descontaba la superación habitual, pero la propia superación del 3T y el impulso de precio por anuncio (+14%) empujaban la guía al alza. El punto medio quedó +1.1% sobre el consenso.
- **Qué se sabía el 25-sep:** la guía del 3T (61-64), el cargo de ~US$10 mil M (26-ago), las cuatro superaciones previas de la guía y la aceleración del precio por anuncio.
- **Qué no se podía saber:** la recapitalización con clase C, el monto exacto del cargo (9.89) y la caída de plantilla a 66,775.
- **Escenario:** guía del 4T de 73-76 (no < 72) y capex acotado a 135-145. Sigue en el **base**; el dato que decide es la guía de gastos y capex 2027 de enero.

## 4. Lecciones (cada una cambia algo concreto)
1. **Separar "la empresa supera su guía" de "la guía supera al consenso".** Para binarios de guía contra consenso, partir de la tasa base histórica de esa relación (no verificada aún para META) y no del sesgo guía → real. Checklist de la ficha: registrar en §8 la serie "punto medio de guía vs consenso previo" de 4 trimestres antes de fijar p.
2. **Cuando hay una partida única anunciada, registrar la UPA en dos bases** (con y sin el cargo). Aquí el pronóstico GAAP era correcto en concepto, pero el error de gastos quedó oculto tras el cargo. Próxima ficha de META: pronóstico adicional de UPA sin partidas únicas.
3. **Fecha del reporte:** la ficha estimaba 28-oct (Yahoo) y Meta publicó el 21-oct. Regla para la rutina de fichas: si la emisora no ha anunciado la fecha, tomar como resolución la más temprana plausible y revisar la página de IR una semana antes.
4. **La recapitalización (clase C) cambia el conteo de acciones desde ene-2027.** Agregar a §9 de la ficha y ajustar UPA por acción en la próxima actualización.

No hay errores de hecho para `conocimiento/registro-de-errores.md` (la fecha estaba marcada como estimada). Los binarios son del orquestador (autor claude), no votos de comité, así que no se actualiza `competencia/calibracion-agentes.csv`.
