# V01. Verificación independiente: momentum (MOM) y rentabilidad (RMW)

> **Estado vigente (2026-09-25, después de la doble ejecución independiente AC-01, AC-02 y AC-03): Replicado con diferencias.** Por parte: MOM de EUA, **replicado y auditado con segunda fuente** (AQR concuerda en los 4 veredictos). RMW de EUA, **replicado con diferencias**: la cifra de French se reproduce exacta, pero su significancia desde 2000 **no** se sostiene en las fuentes independientes (Hou-Xue-Zhang y AQR QMJ). Momentum internacional (adenda), **replicado y auditado**; emergentes no tiene segunda fuente independiente. Detalle en la sección "Doble ejecución independiente y segunda fuente (2026-09-25)", al final.
>
> Fecha: 25-sep-2026. Estado original (05:21 UTC, sustituido por la línea anterior): **Replicado** en lo estadístico (factor académico). **No** es una estrategia operable en GBM.
> Reproducir desde la raíz del repo: `python3 laboratorio/replicas/V01-momentum-y-rentabilidad/reproducir.py`. No usa red: los datos están congelados en `datos/` y sus huellas en `SHA256SUMS.txt`.

## Por qué existe

Revisamos dos cifras aportadas por otros sistemas antes de usarlas:

1. El factor MOM de Kenneth French pagó 0.80%/mes entre 1984 y 2006 y casi nada después (reportado en el LAB-003 de ChatGPT).
2. RMW (empresas muy rentables menos poco rentables) paga ~4.5% anual desde 2000 y es significativo (reportado por otro rival).

Regla del sistema: no se usa ninguna cifra ajena sin verificarla con datos y código propios.

## Datos

- **Fuente:** Kenneth French Data Library, archivos `F-F_Momentum_Factor_CSV.zip` y `F-F_Research_Data_5_Factors_2x3_CSV.zip`, versión "CRSP 202607".
- **Huella del zip de momentum:** `7ee14e89…`. Es idéntica a la del paquete del rival, así que ambos usamos la misma versión de los datos.
- **Qué son estas series:** diferenciales largo-corto académicos de EUA, **sin costos**, antes de impuestos y en USD.

## Método

- **Inferencia:** media mensual, error estándar Newey-West con 6 rezagos (kernel de Bartlett y corrección n/(n−1)) e intervalo de confianza al 95%, calculados con `herramientas/estadistica.py`.
- **Doble implementación del error estándar:** la suma de autocovarianzas se comparó contra la matriz de Bartlett completa (`herramientas/tests/test_estadistica.py`).
  - **Corrección (2026-09-25).** Esto **no** era una doble implementación de V01. Es una prueba unitaria que compara dos fórmulas del mismo error estándar dentro de la misma herramienta (`herramientas/estadistica.py`), sobre una serie sintética de 60 datos. No usó otro código de lectura, otros datos ni otra persona. La doble ejecución independiente de V01 son las auditorías ciegas AC-01 y AC-02 (código propio sin `herramientas/`, descarga propia y fuentes B y C); ver la última sección. Queda en `conocimiento/registro-de-errores.md`.
- **Estimador exacto (agregado el 2026-09-25).** t convencional (IID) = media / (DE/√n), con DE muestral (divisor n−1). t Newey-West(6) = media / EE_NW, con kernel de Bartlett w_j = 1 − j/7, corrección n/(n−1) y z = 1.959964 para el IC95. Son **estimadores distintos** y se reportan los dos.
- **"Anual" (agregado el 2026-09-25).** "×12" es la media mensual aritmética × 12: **no es CAGR**. "Anual compuesto" es (∏(1 + r_t))^(12/n) − 1 de la serie largo-corto: **no es el rendimiento de una cuenta** (no hay costos, préstamo de acciones ni impuestos).
- **Veredicto pre-definido:** "apoyo" si el límite inferior del intervalo es mayor que 0, "contraria" si el límite superior es menor que 0, "inconcluso" en cualquier otro caso.

## Resultados

| Factor | Ventana | n (meses) | Media %/mes | ×12 (no es CAGR) | t NW(6) | IC 95% | Veredicto |
|---|---|---|---|---|---|---|---|
| MOM | 1984-01 a 2006-09 | 273 | 0.798 | 9.58% | 3.37 | [0.335, 1.262] | apoyo |
| MOM | 2006-10 a 2025-12 | 231 | 0.088 | 1.06% | 0.26 | [−0.566, 0.742] | inconcluso |
| MOM | 2006-10 a 2015-12 | 111 | 0.152 | 1.82% | 0.25 | [−1.051, 1.355] | inconcluso |
| MOM | 2016-01 a 2025-12 | 120 | 0.029 | 0.34% | 0.09 | [−0.578, 0.635] | inconcluso |
| RMW | 1963-07 a 1999-12 | 438 | 0.173 | 2.07% | 1.90 | [−0.005, 0.351] | inconcluso |
| RMW | 2000-01 a 2025-12 | 312 | 0.397 | 4.76% | 2.43 | [0.076, 0.717] | apoyo |
| RMW | 2015-01 a 2025-12 | 132 | 0.274 | 3.29% | 1.59 | [−0.064, 0.611] | inconcluso |
| RMW | 2016-01 a 2025-12 | 120 | 0.296 | 3.55% | 1.57 | [−0.074, 0.666] | inconcluso |

Con la serie hasta julio de 2026, RMW desde 2000 da 4.48% anual y t = 2.28. Eso implica que en 2026 el factor ha tenido meses negativos.

### Resultados ampliados (2026-09-25, segunda corrida de `reproducir.py`)

La tabla de arriba se conserva tal como se publicó a las 05:21 UTC. Esta tabla agrega la t convencional (IID) y el anual compuesto, calculados con el mismo `reproducir.py` (versión 2), los mismos datos congelados y los mismos valores en todas las columnas anteriores.

| Factor | Ventana | n | Media %/mes | DE %/mes | t convencional (IID) | t Newey-West(6) | IC 95% NW (%/mes) | ×12 (no es CAGR) | Anual compuesto (serie L-C; no es cuenta) | Peor mes | Mejor mes | Veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MOM | 1984-01 a 2006-09 | 273 | 0.798 | 4.345 | **3.04** | **3.37** | [0.335, 1.262] | 9.58% | 8.76% | −25.36 (2001-01) | 18.05 (2000-02) | apoyo |
| MOM | 2006-10 a 2025-12 | 231 | 0.088 | 4.501 | 0.30 | 0.26 | [−0.566, 0.742] | 1.06% | −0.26% | −34.36 (2009-04) | 12.73 (2008-06) | inconcluso |
| MOM | 2006-10 a 2015-12 | 111 | 0.152 | 5.135 | 0.31 | 0.25 | [−1.051, 1.355] | 1.82% | 0.05% | −34.36 (2009-04) | 12.73 (2008-06) | inconcluso |
| MOM | 2016-01 a 2025-12 | 120 | 0.029 | 3.844 | 0.08 | 0.09 | [−0.578, 0.635] | 0.34% | −0.55% | −16.21 (2023-01) | 8.20 (2020-03) | inconcluso |
| RMW | 1963-07 a 1999-12 | 438 | 0.173 | 1.600 | 2.26 | 1.90 | [−0.005, 0.351] | 2.07% | 1.93% | −8.07 (1999-12) | 5.01 (1974-05) | inconcluso |
| RMW | 2000-01 a 2025-12 | 312 | 0.397 | 2.872 | 2.44 | 2.43 | [0.076, 0.717] | **4.76%** | **4.35%** | −18.93 (2000-02) | 13.04 (2000-11) | apoyo |
| RMW | 2015-01 a 2025-12 | 132 | 0.274 | 2.129 | 1.48 | 1.59 | [−0.064, 0.611] | 3.29% | 3.06% | −5.25 (2025-10) | 7.19 (2021-11) | inconcluso |
| RMW | 2016-01 a 2025-12 | 120 | 0.296 | 2.197 | 1.48 | 1.57 | [−0.074, 0.666] | 3.55% | 3.32% | −5.25 (2025-10) | 7.19 (2021-11) | inconcluso |
| RMW (sensibilidad, no pre-registrada) | 2000-01 a 2026-07 | 319 | 0.373 | 2.974 | 2.24 | 2.28 | [0.052, 0.694] | 4.48% | 4.02% | −18.93 (2000-02) | 13.04 (2000-11) | apoyo |

Fuente: `resultados.json`, claves `MOM`, `RMW` y `sensibilidad`.

**Cómo leer estas cifras (aclaraciones explícitas):**

- **t = 3.04 y t = 3.37 son dos estimadores distintos de la misma ventana (MOM, 1984-01 a 2006-09).** 3.04 es la t **convencional (IID)**, que supone meses independientes. 3.37 es la t **Newey-West con 6 rezagos**, la única que usó V01 para su veredicto. No son "la misma t" y no deben compararse con la t de otra fuente sin decir cuál es. La frase "la misma t" de las conclusiones de abajo no decía qué estimador tenía la cifra del rival; ese archivo no está en el repositorio y no se puede verificar.
- **El "4.8% anual" de RMW desde 2000 era la media mensual × 12 (4.76%), no un rendimiento anual compuesto.** El compuesto de la serie largo-corto en 2000-01 a 2025-12 es **4.35%**, que queda fuera del rango "4.5–4.8%". Con la serie hasta 2026-07, el "~4.5%" (4.48%) también es media × 12; su compuesto es 4.02%. Ninguna de estas cifras es lo que ganaría una cuenta.
- **"t ≈ 2.3–2.4"** corresponde a la t Newey-West de 2000-2025 (2.43) y de 2000-01 a 2026-07 (2.28). Las t convencionales son 2.44 y 2.24.
- **La frase "en 2026 el factor ha tenido meses negativos" se verificó:** de enero a julio de 2026, RMW tuvo 4 meses negativos de 7. La suma fue −4.80 pp y el compuesto −5.82%. En julio subió +11.05% después de −8.16% en mayo y −5.07% en junio (`resultados.json`, `sensibilidad`).
- En MOM 2006-10 a 2025-12 y 2016-01 a 2025-12, la media × 12 es positiva (1.06% y 0.34%), pero el compuesto es negativo (−0.26% y −0.55%). Es la diferencia entre la media aritmética y la geométrica de una serie con DE de 4-5% al mes y media cercana a cero (alerta #5 de `laboratorio/alertas-de-datos.md`).

**Reproducción de esta versión.** `python3 laboratorio/replicas/V01-momentum-y-rentabilidad/reproducir.py`. Dos corridas seguidas dieron el mismo `resultados.json` (SHA-256 `bbe22e8f…158c`). Las claves de la versión 1 (`n`, `media`, `se`, `t`, `t_iid`, `ic95`, `rezagos` y `veredicto`) no cambiaron de valor: se compararon contra la copia anterior, con 0 diferencias. `SHA256SUMS.txt` incluye ahora `reproducir.py` (`d476930e…b552`) además de los dos zips, que no cambiaron. El script se detiene si cambian los datos o el código.

## Conclusiones permitidas

- **MOM:** las cifras publicadas por el rival se reproducen exactamente, con la misma media, la misma t y el mismo intervalo. Desde octubre de 2006 no hay evidencia estadística de una media positiva del factor MOM de EUA. Eso **no prueba** que el efecto haya desaparecido: el intervalo es amplio.
- **RMW:** se **confirma** que desde 2000 paga ~4.5–4.8% anual con significancia (t ≈ 2.3–2.4). **Matiz decisivo:** después de su publicación (Fama-French, 2015) baja a ~3.3–3.6% anual y **deja de ser significativo** (t ≈ 1.6). Antes de 2000 también fue débil.

> **Precisiones del 2026-09-25 a estas dos conclusiones** (no se borran; se acotan con AC-01 y AC-02):
>
> - **MOM.** "La misma t" no decía qué estimador tenía la cifra del rival. V01 solo reportaba la t Newey-West (3.37); la convencional es 3.04. AC-01 reproduce la media, las dos t y el intervalo con código propio, y AQR da el mismo veredicto en las 4 ventanas.
> - **RMW, "~4.5–4.8% anual".** Es media × 12 (4.76% en 2000-2025; 4.48% hasta 2026-07). El compuesto es 4.35% y 4.02%.
> - **RMW, "se confirma ... con significancia".** Vale **solo para el RMW 2x3 de French** (t NW 2.43). Con medidas independientes del premio de rentabilidad/calidad, 2000-2025 es **inconcluso**: R_ROE de Hou-Xue-Zhang da t NW 1.84 y QMJ USA de AQR da t NW 1.81 (AC-02).
> - **RMW, "baja a ~3.3–3.6%".** Son estimaciones puntuales (media × 12). No se probó que el premio haya bajado: la media de 2000-2025 (0.397%/mes) cae dentro del IC95 de 2015-2025 ([−0.064, 0.611]). Lo único que se puede decir es que la muestra posterior a 2015 no alcanza para distinguirlo de cero.
> - **RMW, "antes de 2000 también fue débil".** Solo con RMW (t NW 1.90; la t IID es 2.26). R_ROE (1967-1999, t NW 6.68) y QMJ USA (1963-1999, t NW 3.61) fueron fuertes en ese periodo. Es una diferencia de constructo, no un hecho sobre "la rentabilidad".

## Conclusiones que NO se sostienen

- Que momentum o rentabilidad sean estrategias rentables en GBM. Estas series son largo-corto, sin costos y en USD, y con 20,000 MXN no se puede ir en corto.
- Que RMW sea una ventaja segura hacia adelante. La evidencia posterior a su publicación es inconclusa.
- Que una media multiplicada por 12 sea un CAGR o la riqueza que obtendría un inversionista.

## Siguiente prueba (pendiente)

1. Momentum y rentabilidad **fuera de EUA** con los factores internacionales de French (Developed, Europe, Japan, Asia Pacific ex Japan y Emerging), antes y después de su publicación.
2. **Versiones implementables** vía ETFs disponibles en el SIC (por ejemplo, ETFs de momentum y de calidad frente al mercado), en MXN y con costos de GBM.
3. Doble ejecución independiente de este archivo por el subagente `auditor-de-replicas`.

**Estado de estos pendientes (2026-09-25):**

- **1. Hecho solo para momentum:** V02 y AC-03. La rentabilidad fuera de EUA sigue pendiente.
- **2. Hecho en parte:** V02 probó seis ETFs de momentum internacional; ninguno tiene ventaja significativa y ninguno está verificado en el SIC. Los ETFs de calidad siguen pendientes. V03 mostró que el quintil de alta rentabilidad contra el mercado (long-only) da ~1% al año sin significancia.
- **3. Hecho:** auditorías ciegas AC-01, AC-02 y AC-03 (sección final).

## Adenda (25-sep-2026): verificación rápida del momentum internacional

Se descargaron los factores momentum (WML) regionales de Kenneth French (versión a ago-2026) y se calcularon con Newey-West de 6 rezagos (`herramientas/estadistica.py`). Son diferenciales largo-corto, sin costos y en USD. La réplica formal, con datos congelados y doble ejecución, es **V02** (en curso).

| Región | 2000-01 a 2026-08: ×12 / t | 2010-01 a 2026-08: ×12 / t | 2016-2025: ×12 / t | Veredicto |
|---|---|---|---|---|
| Emergentes | 9.6% / 4.21 | 12.3% / 5.47 | 10.3% / 3.76 | apoyo |
| Asia Pacífico ex Japón | 10.7% / 3.66 | 12.5% / 4.99 | 9.0% / 3.41 | apoyo |
| Europa (2000-2025) | 8.9% / 2.99 | 10.2% / 4.84 (hasta 2025) | 7.4% / 2.69 | apoyo |
| Desarrollados ex EUA (2000-2025) | 6.9% / 2.50 | 8.3% / 4.27 (hasta 2025) | 5.7% / 2.27 | apoyo |
| Norteamérica | 3.0% / 1.00 | 4.2% / 1.74 | 2.0% / 0.58 | inconcluso |
| Japón | −0.2% / −0.09 | 1.0% / 0.40 | −1.1% / −0.37 | inconcluso |

**Conclusión:** la cifra recibida para emergentes (9.6% desde 2000 y 12.3% desde 2010, con datos hasta agosto de 2026) **se reproduce exactamente**.

El momentum académico sigue con evidencia fuerte fuera de EUA (emergentes, Asia ex Japón, Europa), y es inconcluso en Norteamérica y Japón.

**No se sostiene todavía:** que eso sea capturable en GBM. En emergentes los costos de transacción son altos, no se puede vender en corto y hay que verificar si existe un ETF de momentum de emergentes en el SIC y cómo le ha ido neto de su gasto. Eso lo resuelve V02.

### Adenda ampliada (2026-09-25): mismas regiones con t convencional y anual compuesto

La tabla de la adenda mezclaba fines de ventana: Europa y Desarrollados ex EUA terminaban en 2025-12 y las demás regiones en 2026-08. Esta tabla da las dos versiones de cada ventana para todas las regiones.

- Las cifras de 2000 y 2010 salen de V02 (`../V02-momentum-internacional/resultados.json`, ventanas W1, W1b, W2 y W2b).
- Las de 2016-2025 salen de la fuente A de AC-03 (`../../auditorias/AC-03-momentum-internacional/resultados.json`, ventana V3).
- Los zips de French de las dos son byte a byte los mismos: French 202608, base Bloomberg, con idéntico SHA-256.

WML es largo-corto, en USD y sin costos.

| Región | Ventana | n | ×12 (no es CAGR) | Anual compuesto (serie L-C; no es cuenta) | t convencional (IID) | t Newey-West(6) | Veredicto | Origen de la cifra |
|---|---|---|---|---|---|---|---|---|
| Emergentes | 2000-01 a 2025-12 | 312 | 8.97% | 8.84% | 4.77 | 4.10 | apoyo | V02 (W1) |
| Emergentes | 2000-01 a 2026-08 | 320 | 9.59% | 9.37% | 4.60 | 4.21 | apoyo | V02 (W1b) |
| Emergentes | 2010-01 a 2025-12 | 192 | 11.40% | 11.62% | 5.42 | 5.74 | apoyo | V02 (W2) |
| Emergentes | 2010-01 a 2026-08 | 200 | 12.30% | 12.40% | 4.80 | 5.47 | apoyo | V02 (W2b) |
| Emergentes | 2016-01 a 2025-12 | 120 | 10.32% | 10.41% | 3.74 | 3.76 | apoyo | AC-03 (A, V3) |
| Asia Pacífico ex Japón | 2000-01 a 2025-12 | 312 | 10.58% | 10.30% | 4.50 | 3.56 | apoyo | V02 (W1) |
| Asia Pacífico ex Japón | 2000-01 a 2026-08 | 320 | 10.67% | 10.38% | 4.53 | 3.66 | apoyo | V02 (W1b) |
| Asia Pacífico ex Japón | 2010-01 a 2025-12 | 192 | 12.41% | 12.57% | 4.88 | 4.86 | apoyo | V02 (W2) |
| Asia Pacífico ex Japón | 2010-01 a 2026-08 | 200 | 12.48% | 12.60% | 4.82 | 4.99 | apoyo | V02 (W2b) |
| Asia Pacífico ex Japón | 2016-01 a 2025-12 | 120 | 9.02% | 8.87% | 2.88 | 3.41 | apoyo | AC-03 (A, V3) |
| Europa | 2000-01 a 2025-12 | 312 | 8.95% | 8.20% | 3.22 | 2.99 | apoyo | V02 (W1) |
| Europa | 2000-01 a 2026-08 | 320 | 8.99% | 8.25% | 3.28 | 3.05 | apoyo | V02 (W1b) |
| Europa | 2010-01 a 2025-12 | 192 | 10.19% | 10.06% | 3.87 | 4.84 | apoyo | V02 (W2) |
| Europa | 2010-01 a 2026-08 | 200 | 10.21% | 10.06% | 3.90 | 4.77 | apoyo | V02 (W2b) |
| Europa | 2016-01 a 2025-12 | 120 | 7.41% | 7.05% | 2.20 | 2.69 | apoyo | AC-03 (A, V3) |
| Desarrollados ex EUA | 2000-01 a 2025-12 | 312 | 6.85% | 6.29% | 2.92 | 2.50 | apoyo | V02 (W1) |
| Desarrollados ex EUA | 2000-01 a 2026-08 | 320 | 7.01% | 6.43% | 2.98 | 2.59 | apoyo | V02 (W1b) |
| Desarrollados ex EUA | 2010-01 a 2025-12 | 192 | 8.30% | 8.20% | 3.73 | 4.27 | apoyo | V02 (W2) |
| Desarrollados ex EUA | 2010-01 a 2026-08 | 200 | 8.50% | 8.35% | 3.67 | 4.22 | apoyo | V02 (W2b) |
| Desarrollados ex EUA | 2016-01 a 2025-12 | 120 | 5.75% | 5.48% | 2.04 | 2.27 | apoyo | AC-03 (A, V3) |
| Norteamérica | 2000-01 a 2025-12 | 312 | 2.86% | 1.42% | 0.86 | 0.95 | inconcluso | V02 (W1) |
| Norteamérica | 2000-01 a 2026-08 | 320 | 2.97% | 1.51% | 0.90 | 1.00 | inconcluso | V02 (W1b) |
| Norteamérica | 2010-01 a 2025-12 | 192 | 4.03% | 3.53% | 1.52 | 1.73 | inconcluso | V02 (W2) |
| Norteamérica | 2010-01 a 2026-08 | 200 | 4.18% | 3.58% | 1.50 | 1.74 | inconcluso | V02 (W2b) |
| Norteamérica | 2016-01 a 2025-12 | 120 | 1.97% | 1.32% | 0.54 | 0.58 | inconcluso | AC-03 (A, V3) |
| Japón | 2000-01 a 2025-12 | 312 | −0.51% | −1.35% | −0.20 | −0.18 | inconcluso | V02 (W1) |
| Japón | 2000-01 a 2026-08 | 320 | −0.24% | −1.19% | −0.09 | −0.09 | inconcluso | V02 (W1b) |
| Japón | 2010-01 a 2025-12 | 192 | 0.60% | 0.08% | 0.24 | 0.26 | inconcluso | V02 (W2) |
| Japón | 2010-01 a 2026-08 | 200 | 0.98% | 0.28% | 0.34 | 0.40 | inconcluso | V02 (W2b) |
| Japón | 2016-01 a 2025-12 | 120 | −1.08% | −1.57% | −0.34 | −0.37 | inconcluso | AC-03 (A, V3) |

**Precisión a la conclusión de la adenda.** "Se reproduce exactamente" vale solo como media × 12 y con French 202608 hasta 2026-08. Con años completos (2000-2025 y 2010-2025), emergentes da 8.97% y 11.40%. Todos los veredictos se mantienen con cualquiera de los dos fines de ventana.

## Doble ejecución independiente y segunda fuente (2026-09-25)

Tres auditorías ciegas repitieron las preguntas de V01 sin leer este archivo. En las tres:

- La especificación (ventanas, estadísticos, regla de veredicto y conclusiones permitidas) se escribió **antes** de descargar y calcular.
- Cada auditor descargó sus propios datos y los congeló con SHA-256.
- El código es propio: Python 3.11, solo biblioteca estándar, sin importar `herramientas/`.
- Cada una usó tres fuentes:
  - **A**, la serie publicada.
  - **B**, una reconstrucción desde las carteras de la misma base. Confirma la aritmética, pero **no** es un dato independiente.
  - **C**, una construcción distinta de otro proveedor. Es la **segunda fuente**.

Las fuentes A de AC-01 y AC-02 se descargaron por separado y resultaron byte a byte iguales a los zips congelados de V01 (`7ee14e89…` y `b8653b41…`). Por eso la diferencia con V01 está en el código y en las fuentes B y C, no en la versión de los datos.

| Auditoría | Pregunta de V01 que repite | A | B | C (segunda fuente) | Resultado |
|---|---|---|---|---|---|
| [AC-01](../../auditorias/AC-01-momentum-eua/README.md) | MOM de EUA en 1984-01 a 2006-09, 2006-10 a 2025-12, 2006-10 a 2015-12 y 2016-01 a 2025-12 | French `Mom`, CRSP 202607 | 6 carteras tamaño × momentum (VW), CRSP 202607 | AQR, hoja UMD, columna USA (datos a 2026-07) | **Mismo veredicto en las 3 fuentes y las 4 ventanas**: apoyo en 1984-2006; inconcluso en las otras tres |
| [AC-02](../../auditorias/AC-02-rentabilidad-eua/README.md) | RMW de EUA en 1963-1999, 2000-2025, 2015-2025 y 2016-2025 | French FF5 `RMW`, CRSP 202607 | 6 carteras tamaño × OP (VW), CRSP 202607 | C1: Hou-Xue-Zhang `R_ROE` (release 2026-07-30). C2: AQR QMJ, columna USA | **Discrepa en 2000-2025**: A y B dan apoyo, C1 y C2 dan inconcluso. Coinciden en inconcluso después de 2015 |
| [AC-03](../../auditorias/AC-03-momentum-internacional/README.md) | Adenda: momentum internacional (emergentes 9.6% y 12.3%; Japón y Norteamérica inconclusos) | French WML regional, 202608 Bloomberg | 6 carteras tamaño × momentum regionales (VW) | AQR UMD: 24 países y agregados (sin emergentes) | Coincide en casi todo. **Excepciones:** emergentes sin segunda fuente; AQR North America da apoyo marginal en 2010-2026 |

### AC-01: momentum de EUA

- **A reproduce V01 con código independiente.** Da las mismas cifras en las 4 ventanas: 1984-01 a 2006-09, 0.798%/mes, t IID 3.04, t NW 3.37, IC95 [0.335, 1.262], ×12 9.58%, compuesto 8.76%.
- **B reproduce A dentro del redondeo.** Correlación 1.0000, |dif| máxima 0.01 pp y ningún mes arriba de la cota de redondeo de 0.015 pp.
- **C (AQR) concuerda en los veredictos.** Correlación con A de 0.965 a 0.991 según la ventana. Su media es 0.02 a 0.08 pp/mes mayor en las 4 ventanas. En 1984-2006 da 0.851%/mes y t NW 3.76; en 2006-10 a 2025-12 da 0.140%/mes y t NW 0.41.
- **Diferencias mensuales.** La mayor es de 4.81 pp, en 2021-01: A +4.34 y C −0.47. Causas probables, documentadas por AQR y no verificadas mes a mes: orden dependiente contra independiente, y universo y fuentes distintos (Compustat/XpressFeed desde 1998).
- **Lo que no permite:** decir que el momentum de EUA "murió" después de 2006. Tampoco que hubo un cambio significativo entre ventanas: no se hizo esa prueba.

### AC-02: rentabilidad de EUA

- **A y B reproducen exactamente la tabla de V01.** 2000-2025: ×12 4.76%, compuesto 4.35%, t IID 2.44, t NW 2.43, IC95 [0.076, 0.717], apoyo. B es igual a A hasta el redondeo (|dif| máxima 0.005 pp), pero sale de las mismas carteras.
- **La segunda fuente no confirma la significancia desde 2000.**
  - R_ROE: ×12 4.03%, compuesto 3.50%, t IID 1.92, t NW 1.84, inconcluso.
  - QMJ USA: ×12 4.21%, compuesto 3.74%, t IID 2.08, t NW 1.81, inconcluso. Aquí el veredicto depende del estimador: con la t IID sería significativo.
  - Las dos tienen correlación de 0.72-0.73 con RMW.
- **En 1963-1999 el patrón se invierte.** RMW es inconcluso (t NW 1.90), mientras R_ROE (t NW 6.68) y QMJ (t NW 3.61) dan apoyo.
- **Después de 2015 coinciden las cuatro series:** inconcluso en 2015-2025 y en 2016-2025.
- **Veredicto de la auditoría:** "~4.5-4.8% anual desde 2000 y significativo; no significativo después de 2015" **no se sostiene en las tres fuentes**. Se sostiene en French como media × 12. Como compuesto (4.35%) solo entra en la tolerancia pre-registrada [4.0, 5.3], no en el rango literal.

### AC-03: momentum internacional (adenda)

- **A y B reproducen la tabla de la adenda.** Correlación 1.00000 en las 6 regiones y diferencias de a lo más 0.02 pp por mes. Emergentes da 9.59% (A) y 9.58% (B) desde 2000, y 12.30% y 12.29% desde 2010, con fin en 2026-08.
- **Las cifras de emergentes dependen del mes final.** Con fin en 2025-12 dan 8.97% y 11.40%. Con fin en 2026-07, 9.31% y 11.87%. En 2026 están el mejor mes (+12.84%, abril) y el peor (−16.84%, julio) de toda la ventana desde 2000.
- **AQR no publica emergentes.** No hay confirmación independiente de esas cifras.
- **Donde se puede comparar, AQR coincide en los veredictos:**
  - Japón (correlación 0.98-0.99): inconcluso en las 3 ventanas.
  - Europa y Desarrollados ex EUA: apoyo. AQR sale ~3 pp al año más alto en media × 12.
- **Norteamérica:** French es inconcluso en las 3 ventanas. AQR "North America" da **apoyo marginal en 2010-01 a 2026-07** (IC95 [0.010, 0.909], t NW 2.01) por el peso de Canadá. AQR USA sola es inconcluso en las 3.
- **Asia Pacífico ex Japón no se puede comparar:** AQR "Pacific" incluye a Japón.

### Contraste automático dentro de `reproducir.py`

La versión 2 del script lee los `resultados.json` de AC-01 y AC-02 y compara su fuente A con V01. La diferencia máxima es:

- AC-01: 0.000023, en media, t IID, t NW, compuesto y límites del IC.
- AC-02: 0.000007.

Las 8 ventanas tienen el mismo n y el mismo veredicto. La diferencia en el IC viene de que las auditorías usan z = 1.96 y V01 usa 1.959964. El script guarda en `resultados.json` (`contraste_auditorias`) la huella SHA-256 de cada archivo contrastado.

### Estado de V01 después de las auditorías

| Parte | Estado anterior | Estado nuevo | Por qué |
|---|---|---|---|
| MOM de EUA | Replicado | **Replicado y auditado con segunda fuente** | Código independiente y AQR dan los mismos veredictos en las 4 ventanas |
| RMW de EUA | Replicado ("se confirma ... con significancia") | **Replicado con diferencias** | La cifra de French se reproduce exacta, pero su significancia desde 2000 depende del constructo: R_ROE y QMJ no la tienen. El "4.8%" era media × 12 |
| Momentum internacional (adenda) | "Se reproduce exactamente" | **Replicado y auditado**; emergentes **sin segunda fuente independiente** | A y B coinciden; AQR coincide donde hay comparable, salvo el apoyo marginal de North America en 2010-2026 |
| **V01 en conjunto** | Replicado | **Replicado con diferencias** | Se toma el estado más débil de sus partes |

Nada de esto cambia la parte operable. Las tres series son largo-corto, en USD y sin costos, préstamo de acciones ni impuestos. Ninguna es comprable en GBM.

Las correcciones de comunicación ("4.8% anual" sin decir que era media × 12, y la "doble implementación" que era una prueba unitaria) quedan en `conocimiento/registro-de-errores.md`. La fila de cada prueba está en `laboratorio/tabla-maestra.md`.
