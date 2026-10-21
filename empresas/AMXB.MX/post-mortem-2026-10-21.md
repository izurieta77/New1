# Post-mortem · América Móvil (AMXB.MX) · 3T26 (reportado el 20-oct-2026, después del cierre)

> Rutina de Cierre, 21-oct-2026 (~17:50 UTC). Los pronósticos se registraron el 25-sep, en `empresas/AMXB.MX/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado. El 13-oct solo se movió su `fecha_resolucion`, sin tocar punto, intervalo ni probabilidades (adenda de esa fecha). Las resoluciones están en `empresas/AMXB.MX/resoluciones.csv`. Sin posición en AMX: no hay decisión de cartera ni votos del comité que evaluar, solo pronósticos. No se ejecutó `herramientas/pronosticos.py resolver` ni se tocaron `bitacora/pronosticos.csv` ni `competencia/calibracion-agentes.csv` (fuera del alcance de esta tarea).

## 1. Resultado real (fuente primaria)
**Fuente:** BMV, evento relevante del 20-10-2026 a las 15:37, "Reporte Financiero y Operativo del 3er Trimestre del 2026": [eventemi_1596486_1.pdf](https://www.bmv.com.mx/docs-pub/eventemi/eventemi_1596486_1.pdf) (36 pp., sha256 `a55be5d8…`). Se cotejó con el XBRL IFRS del trimestre que la emisora entregó a la BMV: [ifrsxbrl_1596479_2026-03_1.zip](https://www.bmv.com.mx/docs-pub/ifrsxbrl/ifrsxbrl_1596479_2026-03_1.zip) (sha256 `03b6f943…`).

Al 21-oct, ~17:50 UTC, todavía no había 6-K en EDGAR (el último es del 2-oct) ni PDF en `s22.q4cdn.com/.../2026/q3/3Q26.pdf` (404).

- **Ingresos totales:** Ps 250,634 M (+7.6% a/a; +4.0% t/t contra 241,071, cálculo propio).
  - Servicios: 211,392 (+7.2%); equipo: 37,959 (+11.4%).
  - Servicios a tipo de cambio constante: +5.3%, sin Argentina.
- **EBITDA:** 102,156 M (+8.9%), con margen de 40.8% (+0.5 pp). EBIT: 57,113 M (+13.9%; margen de 22.8%).
- **Financiamiento:**
  - Intereses netos: 11,796 M.
  - Otros gastos financieros: 7,169 M.
  - **Pérdida cambiaria:** 3,603 M, contra una ganancia de 6,301 M un año antes y de 8,275 M en el 2T26.
  - Costo integral: 22,568 M.
- **Impuestos:** 8,728 M. La tasa efectiva fue de **25.3%** (8,728 / 34,545; cálculo propio).
- **Utilidad neta mayoritaria** (atribuible a la controladora): **Ps 24,282 M** (+7.0%). El XBRL da `ProfitLossAttributableToOwnersOfParent` = 24,281.93 M.
- **Acciones y UPA:**
  - Acciones promedio: 59.9 mil M; al cierre, 59.7 mil M (59,747 M en el XBRL).
  - **UPA reportada: Ps 0.41** (XBRL básica y diluida: 0.41). Con la definición del pronóstico (UN mayoritaria / acciones promedio): 24,282 / 59.9 = **0.405** (cálculo propio), que se redondea a la misma cifra.
  - Por ADS: US$0.47.
- **Participación no controladora:** −1,621 M en resultados (3T25: −1,701). Utilidad consolidada de 25,903 M (XBRL `ProfitLoss`). Ver la §5.
- **Líneas de Telcel:**
  - Suscriptores celulares de México al 30-sep-2026: **81,781 mil**, contra 84,531 en junio (**−2,750 mil; −3.3%**) y 84,345 en sep-25.
  - En el trimestre hubo +144 mil altas de pospago y −2.9 M de bajas de prepago. AMX atribuye las bajas a "depuraciones de la base de suscriptores" y al registro de usuarios.
- **México:** ingresos de 90,295 M (+5.6%), servicios +5.2% (contra +4.4% en el 2T), servicio móvil +5.4% (pospago +8.0%, prepago +3.5%) y EBITDA de 37,486 M (+6.0%; margen de 41.5%).
- **Deuda:**
  - Total: 483,910 M; caja e inversiones: 83,829 M.
  - **Deuda neta: 400,081 M**, sin arrendamientos (2T26: 400,984; dic-25: 447,522).
  - Apalancamiento: 1.21x deuda neta / EBITDAaL, contra 1.52x al cierre de 2025.
  - En 9M: capex de 75.9 mil M y 27.5 mil M distribuidos en recompras y dividendos.
- **Evento posterior:** compra de 72.83% de Desktop (Brasil), anunciada el 1-oct.
- **Reacción del precio:** no verificada; Yahoo no respondió.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro | Consenso | Real | Error nuestro | Error consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos totales (punto; p10-p90) | 243,000 (238,000-248,000) | 243,980 | 250,634 | −3.05% | −2.65% | **Fuera** del intervalo de 80% (por arriba del p90) |
| UPA (punto; p10-p90) | 0.33 (0.25-0.41) | 0.344 | 0.41 (0.405 calculada) | −19.5% | −16.1% | Dentro, **justo en el p90** |
| P(ingresos > 243,980) | 0.45 | — | Sí | — | — | Brier 0.3025 |
| P(líneas Telcel 30-sep < 84,531 mil) | 0.50 | — | Sí (81,781) | — | — | Brier 0.2500 |

**Brier promedio de los dos binarios: 0.2763**, peor que 0.25 (moneda al aire). El error = (punto − real) / real, con la misma convención que `empresas/JNJ/resoluciones.csv`.

## 3. Matriz y lectura
- **Ingresos: mal proceso, mal resultado.**
  - El supuesto era +0.8% t/t (efecto cambiario "casi neutro"), y el real fue +4.0% t/t.
  - El punto, el intervalo y el binario apostaron contra una tasa base de 7/7 trimestres arriba del consenso. Ahora son **8/8**, con una sorpresa de +2.7%, en la parte alta del rango previo (+0.1% a +2.8%).
  - El verificador lo advirtió el 25-sep ("la apuesta más expuesta de la ficha").
  - Equipo creció 11.4% a/a, y Argentina se reporta bajo NIC 29. Desglosar el +4.0% t/t por país y por tipo de cambio queda pendiente: no se tiene aquí el detalle del 2T26 por línea.
- **UPA: buen resultado por el intervalo, mal punto.** El punto (0.33) quedó debajo de todas las fuentes de consenso, y el real tocó el p90. Descomposición (cálculo propio):
  - Modelo de la ficha: EBIT ~52 mil M, intereses 11.8, otros 6.5, cambiario ~−1 y tasa de 36% → ~0.32-0.33.
  - Con los componentes reales y la misma tasa de 36% sale **0.343**.
  - El resto (**~0.06**) viene de la tasa efectiva: 25.3% contra 36%.
  - La otra parte (~0.02) viene de un EBIT más alto (57.1 contra 52 mil M).
  - Los intereses (11.796 contra 11.8) se acertaron. La pérdida cambiaria (3.6 mil M) quedó apenas fuera del rango supuesto (−3 a +1): el signo de la cadena B se cumplió.
  - **La sorpresa vino de la operación y de impuestos, no del tipo de cambio.**
- **Binario de ingresos (0.45): mala decisión, mal resultado.** Partir de la tasa base (~0.85 con 7/7, suavizada) habría dado un Brier de ~0.02.
- **Binario de líneas (0.50): proceso defendible, Brier neutro.**
  - La lógica del verificador (la suspensión es reversible y solo caen dos cohortes en el 3T) era correcta sobre el registro.
  - Lo que no se anticipó: AMX aprovechó para **depurar prepago** (2.9 M de bajas), además del registro, y lo hizo también en Colombia (−2.4 M).
  - El 0.60 original habría puntuado mejor (0.16). Con la información del 25-sep, 0.50 no era irrazonable.
- **Qué se sabía el 25-sep:**
  - la tasa base de sorpresas de ingresos (7/7);
  - la reversión del cambiario (cadena B, confirmada);
  - el calendario del registro.
- **Qué no se podía saber:**
  - la tasa fiscal del trimestre;
  - la decisión de depurar prepago;
  - el +11% del ingreso por equipo.
- **Escenario:**
  - La ficha decía que lo cambiaría: "bajas de Telcel mayores a 2 M líneas en 3T26-4T26". **El umbral se rebasó en un solo trimestre (−2.75 M).**
  - Pero la cadena causal A ("el ingreso cae menos que las líneas porque muchas son inactivas") se confirmó con creces: el servicio móvil en México creció 5.4% y el EBITDA de México 6.0%.
  - **Lectura (inferencia):** las bajas fueron de líneas sin ingreso, así que el disparador por líneas estaba mal especificado. Se mantiene el **escenario base**, con el 4T26 como prueba, porque los plazos de registro siguen hasta el 31-dic.

## 4. Lecciones (cada una cambia algo concreto)
1. **Binarios de "supera al consenso": partir de la tasa base.** Este es el cuarto caso, después de MU, GS y JNJ. Con 7/7 previos, un 0.45 exige un argumento cuantificado que explique por qué este trimestre es distinto. Aquí el argumento (efecto cambiario neutro) era sobre el nivel y no sobre la sorpresa: el consenso ya incorporaba los tipos de cambio. Refuerza `conocimiento/fichas/2026-10-13-pronostico-de-resultados-tasa-base.md` §7.
2. **Punto de UPA:** si queda debajo de todas las fuentes de consenso, la §8 debe nombrar qué supuesto lo explica y su tasa histórica. Aquí fue la tasa efectiva de 36%, sin contrastar con la del trimestre previo. Checklist de la §8: anotar la tasa efectiva de los últimos 4 trimestres junto al supuesto.
3. **Disparadores de escenario en ingreso, no en volumen.** En la ficha de AMX, cambiar "bajas de Telcel > 2 M líneas" por "ingreso por servicio móvil de México < +2% a/a" (parámetro propuesto, no aplicado), y anotar las líneas solo como dato.
4. **Leer el renglón de minoritarios antes de puntuar la UPA** (ficha C4). Aquí no cambió el resultado (6.3% de la utilidad consolidada), pero el criterio del CSV ya usaba la utilidad mayoritaria. Se mantiene como paso fijo.

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`: la cifra de líneas del 2T26 de la ficha (84,531 mil) coincide con la columna de junio de este reporte. El sesgo fue de juicio. La fecha del calendario de registro (15-ago según AMX, contra 31-ago según Expansión) ya estaba anotada en la ficha.

## 5. Nota: participación no controladora (IFRS 10 B94; ficha C4)
- **En resultados:** utilidad consolidada (`ProfitLoss`) de 25,903 M = 24,282 de la controladora + 1,621 de la no controladora.
  - La no controladora es **6.3%** de la consolidada (3T25: 1,701 de 24,401, 7.0%); en 9M26, 4,376 M.
  - Viene sobre todo de las subsidiarias con socios relevantes: **A1 Telekom Austria (61.0%)** y **EuroTeleSites (57.0%)**. El resto de las operaciones está entre 97.9% y 100% (tabla de subsidiarias del reporte).
  - El reporte no desglosa la no controladora por subsidiaria; la atribución a A1 es inferencia.
- **En balance (XBRL):** participación no controladora de **Ps 64,974 M** al 30-sep-2026 (dic-25: 65,602). El capital de la controladora es de 402,402 M y el total de 467,376 M.
- **Implicaciones (C4, uso en el sistema):**
  - El P/U se mide sobre los 24,282 M, que ya es la cifra de la controladora: el pronóstico y la UPA reportada usan la misma definición, así que no hay problema de comparabilidad.
  - El **VE de la §6 de la ficha debe sumar ~65 mil M de minoritarios en libros** (A1 cotiza en Viena; a mercado sería otra cifra, no consultada), porque el EBITDA consolidado incluye el 100% de A1.
  - Con un VE de ~1,793 mil M, la diferencia es de ~3.6% del múltiplo (cálculo propio). Queda pendiente verificar si el VE de la ficha ya la incluía.
- **Partes relacionadas (IAS 24; ficha C9):**
  - El XBRL trimestral da saldos corrientes con relacionadas de 1,642 M por cobrar y 3,207 M por pagar al 30-sep. Son menores a 1% de la deuda total.
  - No hay detalle de operaciones con Carso o Inbursa en el trimestral.
  - El informe del comité de auditoría y de prácticas societarias (LMV art. 43) es anual y **no se revisó**: queda pendiente para la ficha de 2027.
