# Ficha: magnitudes verificadas para los huecos de S7-02 y S7-12 (complejidad/ML y opciones 0DTE)

- **Fecha:** 2026-09-25.
- **Origen:** `conocimiento/examenes/2026-09-25-diagnostico/S7/acta.md`, preguntas S7-02 (hueco de 0.75 pts: incisos a, c, d) y S7-12 (hueco de 0.5 pts: inciso d). El acta ya traía las cifras en la "Clave" del examen; esta ficha las verifica de forma independiente contra fuente primaria (o la fuente más cercana accesible) y anota el nivel de acceso real logrado hoy, con herramientas de red disponibles para esta tarea (el sustentante del examen no tenía acceso a red; este verificador sí).
- **Método:** para cada cita se intentó (1) bajar el PDF, (2) extraer texto con `pypdf` cuando `pdftotext`/`poppler-utils` no estaban disponibles en el entorno (no se pudo instalar: `apt-get install poppler-utils` falló por 404 del repositorio), y (3) `grep` sobre el texto extraído para ubicar la cifra exacta con su contexto. Cuando SSRN devolvió 403 (bloqueo del proxy/anonimización), se usó WebSearch/WebFetch sobre resúmenes, comunicados de prensa institucionales o páginas de reproducción académica, y se marca explícitamente como nivel de acceso menor.
- **Archivos de trabajo (no en el repo, en el scratchpad de la sesión):** `nagel_full.txt`, `kmz_full.txt`, `gkx_nber.txt`, `amaya_full.txt` (texto extraído de los PDF originales con `pypdf`).

---

## S7-02 — Complejidad, KMZ y sus críticas

### (a) GKX 2020: la media histórica infla el R²oos de acciones individuales en ~3pp

- **Pregunta:** ¿la cifra "≈3 puntos porcentuales" y el ejemplo "OLS-3 a 3.74%" son reales?
- **Fuente y versión:** Gu, S., Kelly, B., Xiu, D., "Empirical Asset Pricing via Machine Learning", NBER Working Paper 25398 (versión de trabajo; la RFS 2020 33(5):2223-2273 es la versión publicada con el mismo contenido en esta sección). **Nivel de acceso: lectura íntegra del PDF del WP** (80 páginas, texto extraído completo con `pypdf` desde `https://www.nber.org/system/files/working_papers/w25398/w25398.pdf`).
- **Hallazgo con cifras (cita textual):**
  > "We avoid this pitfall by benchmarking our R2 against a forecast value of zero. To give an indication of the importance of this choice, when we benchmark model predictions against historical mean stock returns, the out-of-sample monthly R2 of all methods rises by roughly three percentage points." (cuerpo del texto, antes de la nota 24)
  > Nota al pie **34** (numeración exacta, coincide con la citada en la clave del examen): "As an aside, it is useful to know that there is a roughly 3% inflation in out-of-sample R2s if performance is benchmarked against historical averages. For OLS-3, the R2 relative to the historical mean forecast is 3.74% per month!"
- **Límites:** verificado sobre el WP de NBER, no sobre el PDF final de Oxford/RFS (que debería tener texto idéntico en esta sección, pero la paginación cambia; no se descargó el PDF de Oxford Academic por paywall).
- **Contraejemplo:** ninguno encontrado.
- **Estado:** **confirmado, grado A** (cifra exacta con cita textual y número de nota al pie).

### (c) KMZ (JF 2024): mejora de Sharpe ≈0.47/año, t≈3, muestra CRSP 1926-2020, 15 predictores, P≤12,000, T=12/60/120

- **Pregunta:** ¿son reales el diseño (15 predictores de Goyal-Welch, RFF hasta P=12,000, T=12/60/120 meses) y el resultado (mejora de Sharpe ≈0.47 anual con t≈3.0) atribuidos a Kelly-Malamud-Zhou?
- **Fuente y versión:** Kelly, B., Malamud, S., Zhou, K. (2024), "The Virtue of Complexity in Return Prediction", *Journal of Finance* 79(1):459-503, DOI 10.1111/jofi.13298. **Nivel de acceso: lectura íntegra** del PDF alojado en `economics.yale.edu` (45 páginas, texto extraído con `pypdf`; la paginación coincide con la revista, ej. "494 The Journal of Finance").
- **Hallazgo con cifras (cita textual):**
  > "Over the standard Center for Research in Security Prices (CRSP) sample from 1926 to 2020, out-of-sample market timing Sharpe ratio improvements (relative to market buy-and-hold) reach roughly 0.47 per annum with t-statistics near 3.0."
  > "The data inputs to our models are 15 standard predictor variables from the finance literature compiled by Goyal and Welch (2008)."
  > Nota al pie 42: "Strictly imposing the Campbell and Thompson (2008) constraint boosts the Sharpe ratio from 0.47 to 0.54 in the T = 12 case, from 0.42 to 0.50 for T = 60, and from 0.41 to 0.49 for T = 120." — confirma las tres ventanas T=12/60/120 con Sharpe base 0.47/0.42/0.41 antes de imponer no negatividad.
  > P llega hasta 12,000 RFF (confirmado en múltiples pasajes, ej. "ranging from P = 2 to P = 12,000").
  > Divestment antes de recesiones: "successfully doing so in 14 out of 15 recessions in our test sample."
- **Límites:** el R²oos es "substantially negative for the vast majority of models" según el propio texto — la mejora de Sharpe no viene acompañada de R² positivo; eso es justo el punto que motiva la crítica de Nagel.
- **Contraejemplo:** ninguno dentro del propio paper (es la fuente primaria del resultado).
- **Estado:** **confirmado, grado B** (resultado publicado en revista top, pero con las críticas de 2025 abajo).

### (d) Críticas de 2025: Nagel, Buncic, Elmore-Strauss

**Nagel (2025), "Seemingly Virtuous Complexity in Return Prediction"**
- **Fuente y versión:** NBER Working Paper 34104 (ago-2025); también SSRN 5335012/5386615. **Nivel de acceso: lectura íntegra** (53 páginas, PDF de `nber.org/system/files/working_papers/w34104/w34104.pdf`, texto extraído con `pypdf`).
- **Hallazgo con cifras:**
  - Mecanismo confirmado: con P≫T, el pronóstico RFF es un promedio ponderado por kernel de los T rendimientos de entrenamiento; con T=12 la similitud refleja cercanía temporal ⇒ momentum cronometrado por volatilidad.
  - Tabla I de Nagel (réplica de la Figura 8 de KMZ): alfa de la estrategia RFF de alta complejidad = 3.4% anual, **t = 2.417**, IR = 0.255 (cifra textual: "the first column shows the result from KMZ that the high-complexity RFF strategy produces positive alpha, with high t-statistic (2.417) and information ratio (0.255)"). Esto coincide con la tabla ya existente en `conocimiento/09-frontera-ia-ml-llm-en-inversion.md` §2.3.
  - Con σ²=5 (la calibración del DGP de KMZ), el Sharpe alcanzable teórico con T=12, P grande es de solo 0.017 anualizado — "más de 20 veces menor" que lo que KMZ reportan empíricamente.
- **Estado:** confirmado, grado B (crítica).

**Buncic (2025), "Simplified: A Closer Look at the Virtue of Complexity in Return Prediction"**
- **Fuente y versión:** SSRN 5239006 (abr-2025, actualizado); afiliación Stockholm Business School, Stockholm University. En la bibliografía de Nagel aparece exactamente como "Buncic, Daniel, 2025, 'Simplified: A Closer Look at the Virtue of Complexity in Return Prediction,' Working paper, Stockholm University." **Nivel de acceso: NO lectura íntegra** — SSRN devolvió HTTP 403 (bloqueo de acceso desde este entorno) en dos intentos. La verificación se apoya en (i) el propio texto de Nagel, que sí se leyó íntegro y cita a Buncic dos veces con su hallazgo metodológico, y (ii) el comunicado de prensa de Stockholm University (`su.se`, sección Stockholm Business School News, fechado 25-sep-2025), que cita al autor entre comillas.
- **Hallazgo con cifras:**
  - Cita de Nagel (texto propio, leído íntegro): "Buncic (2025) shows that the increasing relation between out-of-sample performance and complexity disappears when RFF-based return forecasts are first aggregated across different draws of RFF weights before computing the OOS performance measures, but Kelly and Malamud (2025) argue that for low P this approach effectively constructs an ensemble of many simple models."
  - Cita del comunicado de la universidad (no del PDF): "a simple expanding-window linear regression model with mild shrinkage achieves a Sharpe ratio of 0.699," frente a 0.485 del "KMZ's preferred complex model." Las dos "decisiones de diseño" que critica son (1) la restricción de intercepto cero y (2) el esquema de agregación de KMZ.
- **Límites:** el mecanismo de Buncic que aparece EN el paper de Nagel (agregación de pronósticos antes de medir desempeño) es ligeramente distinto del que resalta el comunicado de prensa (regresión lineal simple con contracción leve, Sharpe 0.699 vs 0.485); pueden ser dos resultados del mismo paper (uno metodológico sobre agregación, otro de comparación directa de Sharpe), pero no se confirmó con el texto completo del propio Buncic cuál sección contiene cada cifra.
- **Contraejemplo/matiz:** Nagel registra la réplica de Kelly y Malamud (2025), "Understanding the Virtue of Complexity" (working paper, Yale University — año y afiliación **ahora confirmados** vía la bibliografía de Nagel, que antes el cap. 09 marcaba como "fecha no verificada"): sostienen que, para P bajo, el método de agregación de Buncic construye en realidad un ensamble de muchos modelos simples, que a su vez es un modelo complejo. Es decir, la disputa metodológica sigue abierta.
- **Estado:** cifras 0.699/0.485 y las dos decisiones de diseño — **confirmadas por fuente secundaria fuerte (comunicado institucional que cita al autor), no por lectura íntegra del PDF (bloqueado). El mecanismo de agregación — confirmado por lectura íntegra de Nagel**. Grado C (falta la lectura del PDF original de Buncic).

**Elmore y Strauss (2025), "Is Complexity Virtuous?"**
- **Fuente y versión:** *Economics Letters* 258:112749, DOI 10.1016/j.econlet.2025.112749; también SSRN 5376107 y `digitalcommons.du.edu/business_info_fac/6/`. **Nivel de acceso: resumen (abstract)**, no el artículo completo (ScienceDirect y SSRN no se pudieron descargar en esta sesión; el abstract se leyó completo en DigitalCommons de University of Denver).
- **Hallazgo con cifras (cita textual del abstract):** "the past twelve-month moving average of actual returns is 97.5% correlated to the forecasts from a twelve-month rolling window of random Fourier features with a large penalty." El abstract añade que la alta complejidad no supera comprar-y-mantener ni genera Sharpe, alfa o utilidad superiores.
- **Nota importante:** Elmore y Strauss **no aparecen citados en la bibliografía de Nagel** (se buscó explícitamente "Elmore" y "Strauss" en el texto completo de Nagel y no hay coincidencias) — son dos líneas de crítica independientes, publicadas por separado, no una cita dentro de la otra. Esto matiza la nota de la clave del examen, que las lista juntas sin indicar que Nagel no las menciona.
- **Estado:** cifra del 97.5% **confirmada** (nivel: resumen, no cuerpo completo), grado B/C (Economics Letters es una revista con revisión por pares pero de formato corto; no se verificó la robustez del resultado en el cuerpo del artículo).

---

## S7-12 — Opciones 0DTE y gamma de los OMM (2021-2025)

### Ni, Pearson, Poteshman, White (2021)

- **Fuente y versión:** "Does Option Trading Have a Pervasive Impact on Underlying Stock Prices?", *Review of Financial Studies* 34(4):1952-1986. **Nivel de acceso: resumen** (Oxford Academic, página de abstract; el cuerpo está tras paywall).
- **Hallazgo:** relación negativa, estadística y económicamente significativa, entre la volatilidad de rendimiento de la acción y las posiciones netas compradas de inversionistas que probablemente cubren (gamma positiva de los cubridores ⇒ menor volatilidad).
- **Límite:** no se confirmó una magnitud puntual (ej. "x pp de volatilidad por unidad de posición neta") porque no se accedió al cuerpo del artículo.
- **Estado:** dirección del hallazgo confirmada, grado B (magnitud exacta no verificada en esta sesión).

### Baltussen, Da, Lammers, Martens (2021)

- **Fuente y versión:** "Hedging Demand and Market Intraday Momentum", *Journal of Financial Economics* 142(1):377-403, DOI 10.1016/j.jfineco.2021.04.029. **Nivel de acceso: resumen** (ScienceDirect/SSRN abstract, `www3.nd.edu/~zda/intramom.pdf` no se descargó completo en esta sesión).
- **Hallazgo:** más de 60 futuros de acciones, bonos, materias primas y divisas, 1974-2020; el rendimiento de los últimos 30 minutos antes del cierre se predice por el rendimiento del resto del día, ligado a la demanda de cobertura de gamma corta de OMM y ETFs apalancados.
- **Estado:** confirmado (dirección y diseño), grado A. Ya está en `conocimiento/05-maestria-derivados-y-volatilidad.md` §2.7 y en la tabla canónica.

### Adams, Fontaine, Ornthanalai (2024)

- **Fuente y versión:** "The Market for 0DTE: The Role of Liquidity Providers in Volatility Attenuation", SSRN 4881008 (mayo-2024, Bank of Canada / University of Toronto). **Nivel de acceso: resumen vía búsqueda** — SSRN devolvió HTTP 403; la cifra se confirmó por triangulación de varios resúmenes de búsqueda que citan el mismo texto casi literal, no por lectura del PDF.
- **Hallazgo con cifras:** la volatilidad del índice **baja 60-90 puntos base anualizados** en días con trading 0DTE. Identificación: las opciones SPXW con vencimiento martes y jueves no existían hasta el 26-abr y 19-may-2022 respectivamente (fecha exacta del "quasi-experimento" de introducción escalonada).
- **Estado:** confirmado con nivel de acceso limitado (resumen de búsqueda, no PDF), grado B. Ya citado como fuente #47 en `conocimiento/05-maestria-derivados-y-volatilidad.md` §9, pero **sin la cifra de 60-90 pb en el cuerpo del capítulo** — ese es exactamente el hueco que señaló el acta.

### Dim, Eraker, Vilkov (2024) y la fusión de 2025

- **Fuente y versión:** "0DTEs: Trading, Gamma Risk and Volatility Propagation", SSRN 4692190 (nov-2023/2024). **Nivel de acceso: resumen** (SSRN, ResearchGate). Confirmado además que este paper **se fusionó** con Adams-Fontaine-Ornthanalai y se resometió a la RFS bajo el título "Do S&P500 Options Increase Market Volatility? Evidence from 0DTEs" (Adams, Dim, Eraker, Fontaine, Ornthanalai, Vilkov), SSRN 5641974 — ya citado como fuente #49 en el cap. 05.
- **Hallazgo:** la gamma neta de open interest 0DTE no propaga volatilidad pasada de forma incondicional; la gamma agregada de los OMM en 0DTE es, en promedio, positiva.
- **Estado:** confirmado (dirección y filiación del paper fusionado), grado B/C (working paper).

### Amaya, Garcia-Ares, Pearson, Vasquez (2025)

- **Fuente y versión:** "0DTE Index Options and Market Volatility: How Large is Their Impact?", investigación patrocinada por Cboe, fechada **25-ene-2025**, PDF alojado en `cdn.cboe.com/resources/education/research_publications/gammasqueezes.pdf`; el mismo trabajo está en SSRN 5113405 con el orden de autores "Vasquez, Amaya, Pearson, Garcia-Ares" (orden distinto en SSRN vs. la portada del PDF, mismo contenido). **Nivel de acceso: lectura íntegra** (48 páginas, texto extraído con `pypdf` desde el PDF de Cboe).
- **Hallazgo con cifras (cita textual):**
  > "the maximum impact of OMM gamma on annualized daily volatility is to increase it by 3.3 percentage points... The maximum impact of OMM gamma on annualized 30-minute volatility is to increase it by 6.4 percentage points."
  > "[the average] impact being to reduce volatility by 0.2 percentage points. But OMM gamma is sometimes..." (efecto medio de −0.2pp, con el máximo de +3.3pp en ciertos episodios).
- **Muestra:** datos propietarios de Cboe con dirección de la operación (signo firmado comprador/vendedor) de julio de 2020 a junio de 2023 (confirmado: "during the period running from July 2020 through June 2023").
- **Estado:** **confirmado con lectura íntegra, grado A** (dato primario de Cboe con metodología transparente, aunque los datos no son públicos y el efecto máximo es condicional a episodios específicos, no la norma).

### Brogaard, Han, Won (SSRN 4426358)

- **Fuente y versión:** "Does 0DTE Options Trading Increase Volatility?", SSRN 4426358. El repo (cap. 05) lo fecha "2023, WP"; el propio sustentante lo citó como "(2024)" en la defensa y la clave del examen como "(2024)". **No se resolvió la discrepancia de año** entre "publicado/circulado en 2023" (primer SSRN post) y una posible revisión de 2024 — **(no verificado)** cuál es la fecha de la versión con la cifra de 9.10% citada.
- **Hallazgo con cifras:** una desviación estándar más de participación 0DTE en el volumen de opciones de índice eleva la volatilidad **9.10%** respecto de su media. Volumen mensual de 0DTE: de 0.08 millones de contratos (ene-2011) a 34.4 millones (ago-2023), 48% del volumen de opciones de índice.
- **Estado:** cifra confirmada por múltiples resúmenes de búsqueda independientes, grado B (resumen, no PDF completo). Ya está en `conocimiento/05-maestria-derivados-y-volatilidad.md` §4.

### Participación de 0DTE en 2025

- **Fuente y versión:** Cboe, "The State of the Options Industry: 2025" y el post de blog "SPX® 0DTE Options Jump to Record 62% Share in August" (`cboe.com/insights`). **Nivel de acceso: lectura de sección primaria** (ambas páginas se leyeron vía WebFetch directamente en el sitio de Cboe).
- **Hallazgo con cifras (citas textuales):**
  > "August was another record month for SPX 0DTE options trading, averaging ~2.4M contracts a day and now making up a record 62.4% of overall SPX volume."
  > Informe anual 2025: "2.3 million contracts daily" y "59% of the total product volume" del SPX.
- **Estado:** confirmado, grado A (fuente primaria del operador del mercado). Coincide exactamente con lo ya escrito en `conocimiento/05-maestria-derivados-y-volatilidad.md` línea 192.

---

## Resumen de qué queda "(no verificado)"

| Cifra/afirmación | Estado |
|---|---|
| GKX: inflación ≈3pp del R² con media histórica; OLS-3 → 3.74% | Confirmado, cita textual y nota 34 |
| KMZ: mejora de Sharpe ≈0.47/año, t≈3.0, CRSP 1926-2020, 15 predictores, P≤12,000, T=12/60/120 | Confirmado, cita textual |
| Nagel: alfa RFF 3.4%, t=2.417, IR=0.255; mecanismo de kernel/recencia | Confirmado, cita textual |
| Buncic: Sharpe 0.699 vs 0.485; intercepto cero y agregación como decisiones de diseño | Confirmado por comunicado institucional citando al autor; **no** por PDF íntegro (403) |
| Elmore-Strauss: correlación 97.5% con el promedio móvil de 12 meses | Confirmado, nivel resumen/abstract |
| Elmore-Strauss citados dentro de Nagel | **Falso** — no aparecen en la bibliografía de Nagel; son líneas independientes |
| Kelly-Malamud (2025) "Understanding the Virtue of Complexity": año y afiliación (Yale) | Confirmado vía bibliografía de Nagel (antes: "fecha no verificada" en cap. 09) |
| Adams-Fontaine-Ornthanalai: 60-90 pb, identificación por SPXW mar/jue de 2022 | Confirmado por triangulación de resúmenes; SSRN bloqueado (403), no PDF íntegro |
| Amaya et al. (2025): −0.2pp medio, +3.3pp diario máx., +6.4pp 30-min máx.; muestra jul-2020 a jun-2023 | Confirmado, lectura íntegra del PDF de Cboe |
| Brogaard-Han-Won: 9.10%, 34.4 millones de contratos, 48% | Confirmado por resúmenes; **año exacto de la versión citada (2023 vs 2024) no verificado** |
| Ni-Pearson-Poteshman-White: dirección del hallazgo | Confirmado (resumen); magnitud puntual no verificada |
| Cboe 2025: 59% anual, 62.4% récord agosto, ADV 2.3M/2.4M | Confirmado, lectura directa de la fuente primaria (Cboe) |
