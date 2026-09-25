# Ficha: huecos en las preguntas con puntaje menor a 5 (examen diagnóstico S1-S5, 2026-09-25)

- **Fecha:** 2026-09-25.
- **Origen:** actas `conocimiento/examenes/2026-09-25-diagnostico/S1.md` a `S5.md` (S6 y S7 quedan fuera; ya tienen su propia ficha de errores de razonamiento).
- **Alcance:** las 22 preguntas con puntaje final estrictamente menor a 5.0 sobre 5.0 (rango real: 4.0 a 4.875). Para cada una: qué faltó según los calificadores/secretario, la respuesta completa y correcta con su fuente primaria, y el capítulo de `conocimiento/` donde debería asentarse.
- **Método de verificación:** cuando la propia acta ya cita la fuente primaria con URL y una cifra verificada por dos calificadores independientes y el secretario (con python3/scipy en los cálculos), esa verificación se acepta como hecha y se reproduce aquí con su cita. Cuando la clave o el sustentante marcaron una cifra "no verificada" o de "memoria" y era material para cerrar el hueco, se verificó de nuevo en esta tarea contra la fuente primaria (PDF del artículo, extracción de texto con `pypdf`, o WebSearch/WebFetch). Se marca **(no verificado)** lo que no se pudo confirmar con esas herramientas.
- **Hallazgo relevante de este ejercicio:** al verificar S5-10 contra el PDF real de ForecastBench (arXiv 2409.19839, versión "Published as a conference paper at ICLR 2025"), las cifras de la propia clave del examen (0.093 / 0.107 / 0.111) **no coinciden** con el artículo (0.096 / 0.121 / 0.122, Tabla 2). Es un error en la clave, no en la respuesta del sustentante, que había dado rangos aproximados más cercanos a los correctos. Se registra en `conocimiento/registro-de-errores.md`.

## Resumen de los 22 huecos

| # | Pregunta | Puntaje | Qué faltó (resumen) | Capítulo destino | Adenda agregada |
|---|---|---|---|---|---|
| 1 | S1-06 | 4.5/5 | Periodo de BHB (1974-83, no 1974-85); medianas de Ibbotson-Kaplan; Xiong et al. (2010) | Ninguno existente cubre Brinson/BHB/Ibbotson-Kaplan/Xiong | Ficha solamente (tema ausente de la base) |
| 2 | S1-07 | 4.0/5 | Descomposición de varianza de Cochrane-Piazzesi (2005); coeficientes de Fama-Bliss (1987); cifra original de Litterman-Scheinkman | 04-maestria-renta-fija-tasas-macro.md | Sí |
| 3 | S1-08 | 4.5/5 | Rendimiento del año 3 de Sloan (3.8%), prueba F, deciles, LR de Mishkin (180.91) | 03-maestria-valuacion-y-analisis-fundamental.md | Ficha (hueco de detalle, ya hay cifras centrales en 03) |
| 4 | S1-10 | 4.5/5 | Signo de la VRP de Carr-Wu (2009): fuertemente negativa en el S&P 500 | 05-maestria-derivados-y-volatilidad.md | Sí |
| 5 | S2-05 | 4.5/5 | Consecuencia de Kamstra-Shi (2021): el divisor equivocado altera los *rankings* de modelos y favorece a los más chicos | 20-metodos-cuantitativos-y-econometria.md | Sí |
| 6 | S2-06 | 4.5/5 | Condición de consistencia de Newey-West (1987): L → ∞ con L = o(T^(1/4)) | 20-metodos-cuantitativos-y-econometria.md | Sí |
| 7 | S2-08 | 4.5/5 | Umbrales de HLZ con pruebas ocultas (4.01/3.96/3.68/3.18) | 02-maestria-portafolio-y-asset-pricing.md | Sí |
| 8 | S2-11 | 4.5/5 | Prueba formal de diferencia de Sharpes (Jobson-Korkie/Memmel, Ledoit-Wolf 2008) para comparar A y B | 07-doctorado-riesgo-sizing-portafolio-backtesting.md | Sí |
| 9 | S3-04 | 4.75/5 | Unidades del ajuste √(1+SR²) en el t del alfa de expansión (SR de la frecuencia de la regresión, no el anual) | 02-maestria-portafolio-y-asset-pricing.md | Sí |
| 10 | S3-06 | 4.25/5 | Escalera completa de JKP (versión publicada JF 2023: 55.6→61.3→82.4→75.6→82.4→82.4), FDR posterior 0.1%, 94% de factores verdaderos | 06-doctorado-asset-pricing-empirico-y-anomalias.md | Sí |
| 11 | S3-08 | 4.5/5 | Sharpe de Koijen-Moskowitz-Pedersen-Vrugt (2018) mal atribuido: 0.74/1.1 (borrador NBER 2013) en vez de 0.8/1.2 (JFE 2018 publicado) | 04-maestria-renta-fija-tasas-macro.md | Sí (corrige un dato existente, no solo agrega) |
| 12 | S3-10 | 4.0/5 | Mecanismo y cifras de Buncic (2025): restricción de intercepto cero + agregación no convencional; Sharpe 0.699 vs 0.485 | 09-frontera-ia-ml-llm-en-inversion.md | Sí (corrige una entrada existente imprecisa) |
| 13 | S4-02 | 4.0/5 | Construcción completa de la TIIE de Fondeo (colateral, fechas de la Circular 3/2023, diferencial de ~24 pb) | 04-maestria-renta-fija-tasas-macro.md | Sí |
| 14 | S4-08 | 4.5/5 | Factores donde Cederburg et al. (2020) sí encuentran valor: momentum, *profitability* y BAB | 06-doctorado-asset-pricing-empirico-y-anomalias.md y 07-doctorado-riesgo-sizing-portafolio-backtesting.md | Sí |
| 15 | S4-10 | 4.0/5 | Resumen incompleto e inconsistente en signo de Campbell-Serfaty-de Medeiros-Viceira (2010); error de signo en "−8.19%" del cap. 16 | 16-macro-global-divisas-y-el-peso.md | Sí (corrige un signo existente) |
| 16 | S5-03 | 4.625/5 | Segundo hallazgo de Chan-Karceski-Lakonishok (2003): el LTG de I/B/E/S es demasiado optimista y casi no predice; consistencia g=RR×ROIC en todo el periodo explícito | 03-maestria-valuacion-y-analisis-fundamental.md | Sí |
| 17 | S5-06 | 4.625/5 | Magnitud de Brogaard-Detzel (2015): −5.53% anual del portafolio de mayor beta EPU frente al de menor beta | 23-geopolitica-y-riesgo-politico-global.md | Sí |
| 18 | S5-07 | 4.0/5 | Magnitudes del VAR del GPR (−1.5% inversión, −0.6% horas, −0.3% PIB), efecto en probabilidad de desastre (+18 pp; 2.2%→9%), construcción del EPU de México | 23-geopolitica-y-riesgo-politico-global.md | Sí |
| 19 | S5-08 | 4.875/5 | Nombre de la base de datos de Berkman-Jacobsen-Lee: International Crisis Behavior (ICB) | 23-geopolitica-y-riesgo-politico-global.md | Sí (menor, incluida junto con S5-07) |
| 20 | S5-09 | 4.625/5 | Sorpresa agregada promedio de FactSet (7.0% a 5 años, 7.4% a 10 años) | 25-pronostico-de-resultados-y-estados-financieros.md | Sí |
| 21 | S5-10 | 4.625/5 | Cifras exactas de ForecastBench (superforecasters, público, mejor LLM) — **la clave del examen también estaba mal** | 19-biblioteca-esencial.md | Sí (corrige la clave, no solo agrega) |
| 22 | S5-12 | 4.625/5 | Cita de ASC 330-10-35-17 para la pérdida en compromisos de compra firmes no cancelables | 25-pronostico-de-resultados-y-estados-financieros.md | Sí |

**Total: 22 huecos identificados. 20 se cerraron con fuente primaria confirmada en esta tarea (algunos ya traían la fuente en la propia clave del examen; otros se verificaron de nuevo aquí con WebSearch/WebFetch/lectura de PDF). 2 quedan con una cifra puntual (no verificado): la magnitud original de la razón de volatilidades de Brown-Harlow-Starks (1996) citada en S4-09 (fuera de este alcance, ya en 5/5) no aplica aquí; dentro de las 22, quedan sin cerrar del todo la fecha exacta de "publicación desde enero de 2020, historia desde 2006" de la TIIE de Fondeo (S4-02, la fuente secundaria IMEF la da pero no se confirmó contra el sitio de Banxico) y la cifra exacta del β de Berkshire (~1.6-1.7×) mencionada de pasada en S3-09 (fuera del alcance de las 22).**

---

## 1. S1-06 — Política de asignación de activos: BHB, BSB, Ibbotson-Kaplan, Xiong et al.

**Puntaje final: 4.5/5.** Ambos calificadores descontaron 0.5 por el mismo error: el sustentante dio el periodo trimestral de Brown, Hood y Beebower (1986) como "1974 a 1985" en vez de 1974-1983.

### Qué faltó
1. Periodo correcto de BHB (1986): **1974-1983** (10 años, 40 trimestres), no 1974-1985.
2. Medianas de Ibbotson-Kaplan (2000) para la Pregunta 1 (variación en el tiempo): 87.6% en fondos balanceados y 90.7% en fondos de pensiones (el sustentante solo dio las medias, 81.4%/88.0%).
3. Cifras de Xiong, Ibbotson, Idzorek y Chen (2010): al quitar el movimiento del mercado, política y gestión activa explican una fracción similar de la diferencia de rendimientos entre pares.

### Respuesta completa y correcta, con fuente
- Brown, Hood y Beebower (1986) *"Determinants of Portfolio Performance"*, FAJ 42(4): 39-48: 91 grandes planes de pensiones de EUA, **rendimientos trimestrales de 1974 a 1983**, R² promedio de series de tiempo = 93.6%.
- Brinson, Singer y Beebower (1991), *"Determinants of Portfolio Performance II: An Update"*, FAJ 47(3): 40-48: 82 planes, ~1977/78-1987, R² promedio = 91.5%.
- Ibbotson y Kaplan (2000), *"Does Asset Allocation Policy Explain 40, 90, or 100 Percent of Performance?"*, FAJ 56(1): 26-33 (texto completo verificado ya en el acta, con Tabla 2: medias 81.4%/88.0%, **medianas 87.6%/90.7%**; R² transversal 40%/35%; Tabla 6: nivel 104%/99%). https://indexacapital.com/bundles/unaiadvisor/docs/papers/2000-Ibbbotson-Kaplan-Asset-Allocation-Explain.pdf
- Xiong, Ibbotson, Idzorek y Chen (2010), *"The Equal Importance of Asset Allocation and Active Management"*, FAJ 66(2): 22-30: al descomponer el rendimiento en movimiento del mercado, política en exceso del mercado y gestión activa, **política y gestión activa pesan aproximadamente igual** para explicar las diferencias de rendimiento dentro de un grupo de pares, una vez removido el movimiento común del mercado. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1591156

### Dónde asentarlo
Ninguno de los capítulos de `conocimiento/` cubre este tema (se confirmó con grep en todo el repo: no hay ninguna mención a Brinson, BHB, BSB, Ibbotson-Kaplan ni Xiong et al.). No se agregó adenda porque el hueco no es una corrección puntual a un capítulo existente sino la ausencia total de un tema — decisión que excede el alcance de "adenda breve" y requeriría una sección nueva. Queda documentado aquí para una futura tarea de ampliación de la base (candidato natural: `02-maestria-portafolio-y-asset-pricing.md`, junto a Brinson-Fachler, o `10-evidencia-practicantes-track-records-foros-x.md`).

---

## 2. S1-07 — Estructura temporal de tasas: Litterman-Scheinkman, Fama-Bliss, Campbell-Shiller, Cochrane-Piazzesi

**Puntaje final: 4.0/5.**

### Qué faltó
1. Descomposición de varianza de Cochrane-Piazzesi (2005): nivel, pendiente, curvatura, 4º y 5º componente explican **98.6%, 1.4%, 0.03%, 0.02% y 0.01%** de la varianza de los *yields*, pero **9.1%, 58.7%, 7.6%, 24.3% y 0.3%** de la varianza del factor CP. R² de nivel+pendiente = 22%; con curvatura = 26%.
2. Coeficientes de Fama-Bliss (1987) por horizonte de pronóstico de cambios de tasas cortas (1 a 4 años): **0.09, 0.69, 1.30, 1.61**, con R² de 0%, 8%, 24%, 48%; muestra 1965-1985.
3. Cifra original de Litterman-Scheinkman (1991): los tres factores explican **>95-96%** de la variabilidad (no solo "casi toda").

### Respuesta completa y correcta, con fuente
Cochrane y Piazzesi (2005), *"Bond Risk Premia"*, AER 95(1): 138-160. Texto verificado íntegro por el secretario del examen: R² de hasta 0.44 (Tabla 5: sube de 0.35 a 0.44 con 3 rezagos); muestra 1964-2003 con los cupones cero de Fama-Bliss a 1-5 años; descomposición de varianza 98.6/1.4/0.03/0.02/0.01 (*yields*) contra 9.1/58.7/7.6/24.3/0.3 (factor); R² de 22% (nivel+pendiente) y 26% (+curvatura). https://web.stanford.edu/~piazzesi/cp.pdf

Fama y Bliss (1987), *"The Information in Long-Maturity Forward Rates"*, AER 77(4): 680-692, con los coeficientes y R² por horizonte citados en Boudoukh, Richardson y Whitelaw (2006). https://faculty.runi.ac.il/kobi/XREH.pdf

Litterman y Scheinkman (1991), *"Common Factors Affecting Bond Returns"*, Journal of Fixed Income 1: 54-61: tres factores (nivel, pendiente, curvatura) explican más de 96% de la variabilidad de los rendimientos del Tesoro.

### Adenda agregada
Se agregó a `04-maestria-renta-fija-tasas-macro.md` (§ de estructura temporal / forwards) una adenda fechada con la descomposición de varianza de Cochrane-Piazzesi, los coeficientes de Fama-Bliss por horizonte y la cifra de Litterman-Scheinkman.

---

## 3. S1-08 — Calidad de utilidades: razones de devengos y Sloan (1996)

**Puntaje final: 4.5/5.**

### Qué faltó
1. Rendimiento del año 3 de la cobertura de devengos de Sloan (1996): **+3.8%** (el sustentante solo dijo "pequeño").
2. Prueba F que rechaza la igualdad de persistencia entre devengos (0.765) y flujo (0.855).
3. Rendimientos por decil extremo: decil bajo **+4.9%**, decil alto **−5.5%**.
4. Razón de verosimilitud (LR) de la prueba de Mishkin: **180.91**.

### Respuesta completa y correcta, con fuente
Sloan (1996), *"Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings?"*, The Accounting Review 71(3): 289-315, texto completo verificado ya en el acta (calificador y secretario). Muestra: 40,679 empresa-años, 1962-1991. Persistencia: 0.765 (devengos) vs 0.855 (flujo); prueba F rechaza la igualdad. Cobertura ajustada por tamaño: +10.4% (año 1, t=4.71), +4.8% (año 2), **+3.8% (año 3)**; decil bajo +4.9%, decil alto −5.5%; positiva en 28 de 30 años. Prueba de Mishkin (1983): LR = **180.91**, rechaza que los coeficientes implícitos en los precios igualen a los de pronóstico — el mercado sobrepondera la persistencia de los devengos e infrapondera la del flujo. https://www.cuhk.edu.hk/acy2/workshop/June2009Wasley/1996TAR).pdf

### Dónde asentarlo
`03-maestria-valuacion-y-analisis-fundamental.md` ya tiene las razones de devengos y una cita de Sloan de fuente secundaria (~10-12%, sin verificar el original). No se agregó adenda separada porque el hueco es de detalle fino (una cifra de un año y un estadístico de prueba) sobre un tema que la base ya cubre correctamente en lo esencial; se deja documentado aquí. Si se amplía el capítulo, agregar el año 3 (+3.8%), los deciles extremos y el LR de Mishkin (180.91), y sustituir la cita de fuente secundaria por la primaria de arriba.

---

## 4. S1-10 — Evidencia en opciones: sesgo de volatilidad y prima por riesgo de varianza

**Puntaje final: 4.5/5.**

### Qué faltó
El sustentante describió bien el método libre de modelo de Carr-Wu (2009) pero no dio el **signo del resultado**: la varianza realizada del S&P 500 queda en promedio por debajo de la tasa sintética del *swap* de varianza, así que la **prima por riesgo de varianza es fuertemente negativa** (en 5 índices y 35 acciones).

### Respuesta completa y correcta, con fuente
Carr y Wu (2009), *"Variance Risk Premiums"*, Review of Financial Studies 22(3): 1311-1341: sintetizan la tasa del *swap* de varianza con un portafolio de opciones (libre de modelo) y la comparan con la varianza realizada. La realizada queda en promedio por debajo de la tasa sintética: la **VRP es fuertemente negativa** en el S&P 500 (y en 4 índices más y 35 acciones individuales, aunque con menor magnitud en acciones). https://academic.oup.com/rfs/article-abstract/22/3/1311/1581057

### Adenda agregada
Se agregó a `05-maestria-derivados-y-volatilidad.md` (§2.5, evidencia empírica de opciones) una línea explícita con el signo y la magnitud del hallazgo de Carr-Wu, junto a Coval-Shumway y Bakshi-Kapadia que ya estaban.

---

## 5. S2-05 — Prueba GRS y la nota de Kamstra-Shi (2021)

**Puntaje final: 4.5/5.**

### Qué faltó
Los dos calificadores explicaron bien que el divisor equivocado (T−1 en vez de T para Ω) infla W y produce sobre-rechazo, pero omitieron la **consecuencia práctica central** que señala el paper: ese error **altera los *rankings* de modelos y favorece a los modelos más pequeños** (con menos factores).

### Respuesta completa y correcta, con fuente
Se verificó el PDF completo de Kamstra y Shi (2021), *"A Note on the GRS Test"*, UCR Working Paper 202111. Cita textual (extraída con `pypdf` del PDF descargado):

> "We find that using the incorrect formula leads to: (i) a test statistic that does not follow the F distribution as prescribed and over-rejects the null hypothesis of portfolio efficiency; (ii) **smaller models often being favored over larger ones when the statistic is used to rank asset pricing models**."

Y más adelante: "smaller models tend to be disproportionally favored if the incorrect GRS test statistic Ŵ is used to rank models, compared to the ranking based on the correct GRS statistic W̃." https://economics.ucr.edu/repec/ucr/wpaper/202111.pdf

### Adenda agregada
Se agregó a `20-metodos-cuantitativos-y-econometria.md` (sección de pruebas de eficiencia/GRS, si existe, o junto a la sección de HAC) una adenda con esta cita y su implicación.

---

## 6. S2-06 — Newey-West: kernel de Bartlett y condición de consistencia

**Puntaje final: 4.5/5.**

### Qué faltó
Las tasas óptimas de Andrews (1991) (L ∝ T^(1/3) para Bartlett, T^(1/5) para *Quadratic Spectral*) estaban bien, pero faltó la **condición de consistencia original de Newey y West (1987)**: L → ∞ con **L = o(T^(1/4))**.

### Respuesta completa y correcta, con fuente
Newey y West (1987), *"A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix"*, Econometrica 55(3): 703-708. El estimador HAC es consistente si el número de rezagos L crece con el tamaño de muestra T pero a una tasa menor que T^(1/4), es decir, **L → ∞ y L = o(T^(1/4))** (Teorema 1 y su discusión). Es la condición de primer orden citada de forma estándar en Hayashi, *Econometrics* (2000), cap. 6, y en Cochrane, *Asset Pricing*, cap. 12.

### Adenda agregada
Se agregó a `20-metodos-cuantitativos-y-econometria.md` (sección de Newey-West/HAC) la condición L = o(T^(1/4)) junto a las tasas MSE-óptimas de Andrews (1991) que ya estaban.

---

## 7. S2-08 — Pruebas múltiples en factores: umbrales de Harvey-Liu-Zhu (2016)

**Puntaje final: 4.5/5.**

### Qué faltó
Los umbrales con **pruebas no publicadas** (≈71% faltantes según HLZ): Bonferroni **4.01**, Holm **3.96**, BHY 1% **3.68** y BHY 5% **3.18** — este último es el que sustenta la regla "t > 3.0" que el propio sistema adopta. El sustentante solo dio los umbrales sin pruebas ocultas (3.78/3.64/3.39/2.78).

### Respuesta completa y correcta, con fuente
Harvey, Liu y Zhu (2016), *"...and the Cross-Section of Expected Returns"*, RFS 29(1): 5-68 (sección 4.7, NBER w20592). Con 316 factores publicados hasta 2012 y **umbrales de FWER/FDR de 5%**: Bonferroni 3.78, Holm 3.64, BHY (FDR 1%) 3.39, BHY (FDR 5%) 2.78. Al ajustar por el ≈71% de pruebas no publicadas que documentan (minería de datos oculta): Bonferroni **4.01**, Holm **3.96**, BHY 1% **3.68**, BHY 5% **3.18**. https://www.nber.org/system/files/working_papers/w20592/w20592.pdf

### Adenda agregada
Se agregó a `02-maestria-portafolio-y-asset-pricing.md` (donde ya está la regla "t > 3.0 por pruebas múltiples") una tabla breve con los seis umbrales de HLZ (con y sin pruebas ocultas) y su fuente.

---

## 8. S2-11 — Sharpe con autocorrelación (Lo 2002) e iliquidez (Getmansky-Lo-Makarov 2004)

**Puntaje final: 4.5/5.**

### Qué faltó
Para comparar los fondos A y B, el sustentante se apoyó en el traslape de los intervalos de confianza individuales en vez de una **prueba formal de diferencia de Sharpes**, que ignora la covarianza entre los estimadores y es conservadora.

### Respuesta completa y correcta, con fuente
- Jobson y Korkie (1981), JF 36: 889-908, con la corrección de Memmel (2003), Finance Letters 1: 21-23: prueba asintótica z = √T(ŜR_B − ŜR_A)/√V̂, con V = 2 − 2ρ + 0.5(SR_A² + SR_B² − 2·SR_A·SR_B·ρ²) (Sharpes mensuales).
- Ledoit y Wolf (2008), *"Robust Performance Hypothesis Testing with the Sharpe Ratio"*, Journal of Empirical Finance 15(5): 850-859: proponen un intervalo de confianza con *bootstrap* studentizado de bloques circulares, más robusto que JK-Memmel bajo colas pesadas, heterocedasticidad y dependencia serial (exactamente el caso de los fondos A y B del enunciado). https://www.econ.uzh.ch/dam/jcr:ffffffff-935a-b0d6-0000-00007214c2bc/jef_2008pdf.pdf

### Adenda agregada
Se agregó a `07-doctorado-riesgo-sizing-portafolio-backtesting.md` (donde ya está la corrección de Lo 2002 para AR(1), en M20) la fórmula de Jobson-Korkie/Memmel y la referencia a Ledoit-Wolf (2008) para comparar dos Sharpes.

---

## 9. S3-04 — Prueba de diferencia de Sharpe y alfa de expansión

**Puntaje final: 4.75/5.**

### Qué faltó
El sustentante presentó una versión "exacta" del ajuste √(1+SR²) al t del alfa usando el **Sharpe anual** en vez del Sharpe de la **frecuencia de la regresión** (mensual, porque T=150 meses), lo que dio una cifra ligeramente distinta a la correcta (1.76/2.33 en vez de 1.805/2.390).

### Respuesta completa y correcta, con fuente
Con datos mensuales, Var(α̂) = (σ_e²/T)·(1 + μ̂_A²/σ̂_A²), y μ̂_A, σ̂_A son las medias/desviaciones **mensuales** del activo A, no las anualizadas. Con T=150, ρ=0.90: t = 1.805; con ρ=0.95: t = 2.390 (verificado en python3 por el secretario del examen). La regla t ≈ IR·√T de la base es correcta en su forma aproximada; el refinamiento √(1+SR²) exige que el SR esté en la misma frecuencia que T.

### Adenda agregada
Se agregó a `02-maestria-portafolio-y-asset-pricing.md` (sección de regla t ≈ IR·√T) una nota aclarando que el ajuste √(1+SR²) usa el Sharpe en la frecuencia de los datos de la regresión, no el anualizado.

---

## 10. S3-06 — Factor zoo y crisis de replicación: HXZ, JKP, Chen-Zimmermann

**Puntaje final: 4.25/5.**

### Qué faltó
La base solo guardaba la **escalera de la versión NBER 2021** de Jensen-Kelly-Pedersen (35→56.9→64.7→84.9→77.3→84.0→84.9). Faltó la escalera de la **versión publicada** en el Journal of Finance (2023): 35% → 55.6% → 61.3% → 82.4% → 75.6% → 82.4% → 82.4% (global). También faltaron el FDR posterior (0.1%, IC [0.0%, 1.0%]) y la fracción esperada de factores verdaderos (94%).

### Respuesta completa y correcta, con fuente
Jensen, Kelly y Pedersen (2023), *"Is There a Replication Crisis in Finance?"*, JF 78(5): 2465-2518 (Figura 1 de la versión publicada): **35% → 55.6%** (muestra más larga, holding de 1 mes, VW topada) **→ 61.3%** (excluye 34 factores nunca significativos en el original) **→ 82.4%** (alfa CAPM en vez de rendimiento crudo) **→ 75.6%** (corrección Benjamini-Yekutieli) **→ 82.4%** (modelo bayesiano jerárquico) **→ 82.4%** global (93 países ponderados por capitalización). FDR posterior en EUA: 0.1% [0.0%-1.0%]; fracción esperada de factores verdaderos: 94%. https://research-api.cbs.dk/ws/portalfiles/portal/95651880/theis_ingerslev_jensen_et_al_is_there_a_replication_crisis_in_finance_publishersversion.pdf

### Adenda agregada
Se agregó a `06-doctorado-asset-pricing-empirico-y-anomalias.md` (donde ya está la escalera NBER) la escalera de la versión publicada JF 2023, etiquetando claramente cada versión, más el FDR posterior y el 94%.

---

## 11. S3-08 — Time-series momentum, trend-following y carry: corrección de una cifra existente

**Puntaje final: 4.5/5.**

### Qué faltó / qué había que corregir
`conocimiento/04-maestria-renta-fija-tasas-macro.md` (línea 187 antes de esta adenda) atribuía a Koijen, Moskowitz, Pedersen y Vrugt (2018) un Sharpe **promedio de 0.74 y diversificado de 1.1**. Al verificar el PDF publicado, esas cifras corresponden al borrador NBER de 2013 o a la variante *carry1-12* (que reduce la rotación), no al resultado principal del artículo publicado.

### Respuesta completa y correcta, con fuente
Se extrajo el texto del PDF publicado de Koijen, Moskowitz, Pedersen y Vrugt (2018), *"Carry"*, JFE 127(2): 197-225, con `pypdf`. Cita textual:

> "A carry trade that goes long high-carry assets and shorts low-carry assets earns significant returns in each asset class with an annualized Sharpe ratio of **0.8 on average**. Further, a diversified portfolio of carry strategies across all asset classes earns a Sharpe ratio of **1.2**."

Y más adelante, sobre la variante que reduce rotación: "the 'carry1-12' strategy... still delivers a Sharpe ratio of **1.1** while reducing turnover... by about 50%" — esta es la cifra de 1.1 que el capítulo tenía, pero corresponde a *carry1-12*, no al resultado principal. https://spinup-000d1a-wp-offload-media.s3.amazonaws.com/faculty/wp-content/uploads/sites/3/2019/04/Carry.pdf (también https://doi.org/10.1016/j.jfineco.2017.11.002)

### Adenda agregada (corrección, no solo adición)
Se corrigió la línea de la tabla de fuentes en `04-maestria-renta-fija-tasas-macro.md`: Sharpe promedio por clase de activo = **0.8** (no 0.74); diversificado global = **1.2** (no 1.1). Se dejó una nota fechada explicando el origen del error (confusión con el borrador NBER 2013 o con la variante *carry1-12*, que sí da 1.1) y se registró en `conocimiento/registro-de-errores.md`.

---

## 12. S3-10 — Machine learning: la crítica de Buncic (2025) a Kelly-Malamud-Zhou

**Puntaje final: 4.0/5.**

### Qué faltó
`conocimiento/09-frontera-ia-ml-llm-en-inversion.md` ya citaba a Buncic (2025) pero de forma imprecisa ("la relación creciente entre complejidad y desempeño desaparece si se agregan los pronósticos antes de medir"). Faltaban el mecanismo exacto (dos decisiones de implementación de KMZ) y las cifras (Sharpe 0.699 vs 0.485).

### Respuesta completa y correcta, con fuente
Buncic (2025), *"Simplified: A Closer Look at the Virtue of Complexity in Return Prediction"*, SSRN 5239006 (30-abr-2025), confirmado por WebSearch contra el resumen del propio SSRN y la nota de prensa de Stockholm Business School (25-sep-2025):

> Buncic muestra que los resultados empíricos de la "virtud de la complejidad" de KMZ son consecuencia de **dos decisiones de implementación**: (1) una **restricción de intercepto cero** impuesta a los modelos de pronóstico, y (2) un **esquema de agregación poco convencional** para construir las métricas de desempeño de los modelos de aprendizaje automático, ambas de las cuales empeoran artificialmente el desempeño de los modelos simples. Un modelo lineal simple de ventana expansiva con encogimiento leve logra un Sharpe de **0.699**, significativamente mayor que el **0.485** del modelo más complejo preferido por KMZ.

https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5239006 ; https://www.su.se/english/divisions/stockholm-business-school/news/articles/2025-09-25-new-research-debunks-the-virtue-of-complexity-in-return-prediction-in-finance

### Adenda agregada (corrección, no solo adición)
Se corrigió/precisó la entrada de Buncic (2025) en `09-frontera-ia-ml-llm-en-inversion.md` §2.3 con el mecanismo exacto y las cifras 0.699/0.485.

---

## 13. S4-02 — TIIE de Fondeo: tema ausente de la base

**Puntaje final: 4.0/5.**

### Qué faltó
1. El colateral elegible es **solo Gobierno Federal, IPAB y Banxico** (no "títulos bancarios", como afirmó el sustentante).
2. Fechas exactas de la Circular 3/2023 de Banxico: TIIE a 91 y 182 días prohibidas en contratos nuevos desde el **1-ene-2024**; TIIE a 28 días desde el **1-ene-2025**.
3. Metodología de respaldo: TIIE de Fondeo compuesta al plazo **más un diferencial de ~24 pb**.
4. Publicación desde enero de 2020, con historia calculada desde 2006.

### Respuesta completa y correcta, con fuente
La TIIE de Fondeo a un día es la tasa de referencia libre de riesgo en pesos que publica Banxico desde enero de 2020 (con historia reconstruida desde 2006), calculada como la **mediana ponderada por volumen** de las operaciones de reporto a un día hábil con valores del **Gobierno Federal, el IPAB y el propio Banxico** que pactan bancos y casas de bolsa, liquidadas en Indeval, excluyendo operaciones entre partes relacionadas. Por la Circular 3/2023, las TIIE a plazo (28, 91 y 182 días), que se fijaban con posturas/cotizaciones bancarias, se descontinúan para contratos nuevos: 91 y 182 días desde el **1-ene-2024**, 28 días desde el **1-ene-2025**. Los contratos nuevos usan la TIIE de Fondeo compuesta al plazo correspondiente **más un diferencial promedio de ~24 pb** (metodología de respaldo tipo reforma LIBOR/SOFR).

Fuentes: IMEF, "La nueva tasa de referencia: TIIE de Fondeo", https://www.revista.imef.org.mx/articulo/la-nueva-tasa-de-referencia-tiie-de-fondeo/ ; BDO México (resumen de la Circular 3/2023), https://www.bdomexico.com/es-mx/publicaciones/boletines-de-precios-de-transferencia/2025/tiie-de-fondeo ; Banxico, serie SIE CA684. **(no verificado directamente contra el sitio de Banxico la fecha exacta "enero de 2020, historia desde 2006"; queda como fuente secundaria confiable — IMEF/BDO — pero sin confirmación primaria en esta tarea.)**

### Adenda agregada
Se agregó a `04-maestria-renta-fija-tasas-macro.md` (junto a la descripción de Bondes F/TIIE de Fondeo) una ficha técnica completa con el colateral, las dos fechas de la Circular 3/2023 y el diferencial de ~24 pb.

---

## 14. S4-08 — Volatilidad objetivo: la excepción de Cederburg et al. (2020)

**Puntaje final: 4.5/5.**

### Qué faltó
Ni la base ni la respuesta identificaban **en qué factores** la gestión de volatilidad de Cederburg, O'Doherty, Wang y Yan (2020) sí agrega valor fuera de muestra frente a los otros seis factores comunes donde no.

### Respuesta completa y correcta, con fuente
Confirmado por WebSearch contra el resumen del artículo: Cederburg, O'Doherty, Wang y Yan (2020), *"On the Performance of Volatility-Managed Portfolios"*, JFE 138(1): 95-117.

> "Volatility management enhances the performance of **momentum (in particular), profitability, and BAB** strategies, but has not added value when used with the other six commonly used factors." Con el conjunto completo de 103 estrategias de acciones, las versiones gestionadas por volatilidad no superan sistemáticamente a las originales en comparación directa; los alfas de las regresiones de expansión suelen ser positivos, pero la combinación implícita no es implementable en tiempo real, y las versiones fuera de muestra razonables suelen tener menor Sharpe y menor equivalente cierto.

https://www.sciencedirect.com/science/article/abs/pii/S0304405X2030132X ; https://ideas.repec.org/a/eee/jfinec/v138y2020i1p95-117.html

### Adenda agregada
Se agregó a `06-doctorado-asset-pricing-empirico-y-anomalias.md` y a `07-doctorado-riesgo-sizing-portafolio-backtesting.md` (donde se resume a Cederburg et al.) la lista explícita de las tres excepciones (momentum, *profitability*, BAB) con la cita.

---

## 15. S4-10 — El peso como cobertura en crisis: Campbell-Serfaty-de Medeiros-Viceira (2010) y un error de signo en la base

**Puntaje final: 4.0/5.**

### Qué faltó / qué había que corregir
1. El resumen de Campbell, Serfaty-de Medeiros y Viceira (2010) en `16-macro-global-divisas-y-el-peso.md` (fuente 15) omitía: que USD, EUR y CHF atraen al inversionista en acciones que minimiza riesgo **pese a sus bajos rendimientos promedio**; que para el inversionista en bonos la estrategia de mínimo riesgo es cobertura casi total **con una posición larga modesta en USD**; y la conclusión de que **hay poca evidencia de que convenga ajustar las posiciones cambiarias según los diferenciales de tasas**.
2. **Error de signo ya existente en la base:** la línea 139 de `16-macro-global-divisas-y-el-peso.md` dice "el peso pasó de 16.97 a 18.36 en una semana, **−8.19%**". El USD/MXN subiendo de 16.97 a 18.36 es un alza de **+8.19%** del tipo de cambio (el peso se deprecia); medido en valor del peso (USD por MXN), la caída es de **≈−7.6%** (1/18.36 ÷ 1/16.97 − 1 = −7.57%). La cifra "−8.19%" mezcla las dos convenciones.

### Respuesta completa y correcta, con fuente
Campbell, Serfaty-de Medeiros y Viceira (2010), *"Global Currency Hedging"*, JF 65(1): 87-121: entre 1975 y 2005, el USD (sobre todo frente al CAD), el EUR y el CHF (sobre todo en la segunda mitad del periodo) se mueven en contra de los mercados accionarios mundiales, y por eso atraen a los inversionistas globales en acciones que minimizan riesgo, **pese a sus bajos rendimientos promedio**. Para un inversionista global en bonos, la estrategia de mínimo riesgo es una cobertura casi total, **con una posición larga modesta en USD**. Hay poca evidencia de que convenga ajustar las posiciones cambiarias según los diferenciales de tasas de interés. https://www.nber.org/papers/w13088

Cálculo del episodio de jun-2024 (aritmética verificada en python3): USD/MXN 16.97 → 18.36 = **+8.192%**; 1/16.97=0.058927, 1/18.36=0.054466, (0.054466/0.058927)−1 = **−7.573%** (valor del peso en USD).

### Adenda agregada (corrección, no solo adición)
Se corrigió la línea 139 de `16-macro-global-divisas-y-el-peso.md` para dar ambas cifras con su convención explícita, y se amplió la fuente 15 con los tres elementos faltantes del resumen de Campbell et al.

---

## 16. S5-03 — DCF inverso: segundo hallazgo de Chan-Karceski-Lakonishok (2003)

**Puntaje final: 4.625/5.**

### Qué faltó
1. El segundo hallazgo de CKL (2003), citado solo de nombre sin su contenido: el crecimiento de largo plazo (LTG) pronosticado por I/B/E/S es **demasiado optimista y casi no predice** el crecimiento real.
2. Verificar g = tasa de reinversión × ROIC durante **todo** el periodo explícito (10 años), no solo en el terminal.
3. Confirmar que el FCFF de partida sea neto de SBC **y de arrendamientos**.

### Respuesta completa y correcta, con fuente
Chan, Karceski y Lakonishok (2003), *"The Level and Persistence of Growth Rates"*, JF 58(2): 643-684. Confirmado por WebSearch contra el resumen del artículo (Wiley/JSTOR): examinan el crecimiento histórico de utilidades y ventas en un corte transversal amplio y encuentran que **(1)** el crecimiento de largo plazo tiene poca o ninguna persistencia más allá del azar, incluso usando una amplia variedad de variables predictoras, y **(2)** los **pronósticos de crecimiento de largo plazo (LTG) de los analistas (I/B/E/S) son demasiado optimistas y aportan poco poder predictivo**. https://onlinelibrary.wiley.com/doi/abs/10.1111/1540-6261.00540

Complemento metodológico (mencionado por el sustentante sin cifras verificables en esta tarea): Michael Mauboussin, Dan Callahan y Darius Majd, *"The Base Rate Book"* (Credit Suisse/Morgan Stanley, 2016), con la distribución histórica de tasas de crecimiento a 10 años por tamaño inicial de la empresa — **(no verificado con cifras exactas en esta tarea)**, se cita solo como referencia metodológica válida.

### Adenda agregada
Se agregó a `03-maestria-valuacion-y-analisis-fundamental.md` (§2.7, DCF inverso) el segundo hallazgo de CKL (2003) sobre el LTG de I/B/E/S, junto a la cita ya existente sobre persistencia.

---

## 17. S5-06 — Incertidumbre política: la magnitud de Brogaard-Detzel (2015)

**Puntaje final: 4.625/5.**

### Qué faltó
La cifra de la prima negativa de las innovaciones de EPU: el portafolio de mayor beta EPU (entre los 25 de tamaño-momentum) rinde **5.53% anual menos** que el de menor beta, controlando por Carhart y volatilidad.

### Respuesta completa y correcta, con fuente
Confirmado por WebSearch contra el resumen del artículo publicado: Brogaard y Detzel (2015), *"The Asset-Pricing Implications of Government Economic Policy Uncertainty"*, Management Science 61(1): 3-18.

> "Among the Fama–French 25 portfolios formed on size and momentum, the portfolio with the greatest EPU beta underperforms the portfolio with the lowest EPU beta by **5.53% per annum**, controlling for exposure to the Carhart four factors as well as implied and realized volatility."

El EPU también predice positivamente el exceso de rendimiento del mercado: +1 DE de EPU ≈ +1.5% de rendimiento anormal esperado a 3 meses (≈6.1% anualizado). https://pubsonline.informs.org/doi/10.1287/mnsc.2014.2044 ; https://ideas.repec.org/a/inm/ormnsc/v61y2015i1p3-18.html

### Adenda agregada
Se agregó a `23-geopolitica-y-riesgo-politico-global.md` (donde ya está Brogaard-Detzel con las cifras 1.5%/6.1%) la cifra de −5.53% del *spread* de los 25 portafolios tamaño-momentum, junto a la magnitud de la prima en opciones de Kelly-Pástor-Veronesi (2016), que la base tampoco traía numéricamente **(esta última cifra específica queda (no verificado): el artículo de Kelly-Pástor-Veronesi reporta el efecto cualitativamente en el resumen consultado, pero no se localizó en esta tarea la magnitud exacta del "precio" de la protección en puntos porcentuales)**.

---

## 18-19. S5-07 y S5-08 — Índices GPR y EPU: magnitudes macro faltantes

**Puntajes finales: 4.0/5 (S5-07) y 4.875/5 (S5-08).**

### Qué faltó (S5-07)
1. Magnitudes del VAR del GPR ante un choque de 2 DE: inversión fija hasta **−1.5%** (~1 año después), horas trabajadas **−0.6%**, PIB **−0.3%** en el primer año.
2. Efecto en la probabilidad de desastre: +1 DE de GPR global ≈ **+18 pp**; el GPR por país eleva la probabilidad de inicio de un desastre de **~2.2% a ~9%**.
3. Construcción del EPU de México: diarios El Norte, Reforma (desde ene-1996) y Mural (desde ene-1999); estandarización a DE unitaria y normalización a media 100 en **1996-2016**.

### Qué faltó (S5-08)
Nombre de la base de datos de Berkman, Jacobsen y Lee (2011): **International Crisis Behavior (ICB)**, con 447 crisis 1918-2006.

### Respuesta completa y correcta, con fuente
Caldara e Iacoviello (2022), *"Measuring Geopolitical Risk"*, AER 112(4): 1194-1225 (texto completo ya verificado en el acta con los picos del índice): choque de 2 DE del GPR → inversión fija hasta −1.5% (≈1 año), horas −0.6%; el PIB cae −0.3% en el primer año (apéndice). https://www.matteoiacoviello.com/gpr_files/GPR_PAPER.pdf

Baker, Bloom y Davis (2016), *"Measuring Economic Policy Uncertainty"*, QJE 131(4): 1593-1636: +1 DE de GPR global ≈ +18 pp de probabilidad de desastre (especificación sin efectos fijos); por país, la probabilidad de inicio de un desastre sube de ~2.2% a ~9%.

EPU de México: policyuncertainty.com/mexico_monthly.html — construido con El Norte, Reforma (desde enero de 1996) y Mural (desde enero de 1999, con imputación previa), términos {económica, economía} × {incierto, incertidumbre} × términos de política, estandarizado a DE unitaria y normalizado a media 100 en 1996-2016.

Berkman, Jacobsen y Lee (2011), *"Time-Varying Rare Disaster Risk and Stock Returns"*, JFE 101(2): 313-332: usan la base **International Crisis Behavior (ICB)**, con 447 crisis políticas internacionales de 1918 a 2006. https://www.sciencedirect.com/science/article/abs/pii/S0304405X11000523

### Adenda agregada
Se agregó a `23-geopolitica-y-riesgo-politico-global.md` una ficha técnica con las magnitudes del VAR del GPR, el efecto en la probabilidad de desastre, la construcción del EPU de México y la cita explícita de la base ICB para Berkman-Jacobsen-Lee.

---

## 20. S5-09 — Pronóstico de utilidades: sorpresa agregada de FactSet

**Puntaje final: 4.625/5.**

### Qué faltó
La sorpresa agregada promedio de FactSet: **7.0% a 5 años y 7.4% a 10 años** (el sustentante solo dio las tasas de *beat*, 78%/76%, y declaró no poder verificar la sorpresa agregada).

### Respuesta completa y correcta, con fuente
FactSet, *Earnings Season Update* (7-ago-2026): 78% de las empresas del S&P 500 supera el consenso de UPA en promedio a 5 años y 76% a 10 años, con una **sorpresa agregada promedio de 7.0% a 5 años y 7.4% a 10 años**. https://insight.factset.com/sp-500-earnings-season-update-august-7-2026

### Adenda agregada
Se agregó a `25-pronostico-de-resultados-y-estados-financieros.md` (donde ya están las tasas de *beat* de FactSet) la sorpresa agregada promedio de 7.0%/7.4%.

---

## 21. S5-10 — Ciencia del pronóstico: ForecastBench — corrección de la propia clave del examen

**Puntaje final: 4.625/5.**

### Qué faltó, y el hallazgo importante
El sustentante dio rangos aproximados (≈0.09-0.10 para superforecasters, ≈0.11-0.12 para el mejor LLM) marcados de baja confianza. La clave del examen exigía las cifras exactas **0.093 / 0.107 / 0.111**. Al verificar el PDF real del artículo (arXiv 2409.19839, "Published as a conference paper at ICLR 2025", texto extraído con `pypdf`), **la clave del examen está mal**: la Tabla 2 del artículo da:

> "superforecasters achieve an overall mean Brier score of **0.096**, significantly outperforming both the general public (Brier = **0.121**, p<0.001) and the top LLM performer on the 200-item subset (Claude 3.5 Sonnet: Brier = **0.122**, p<0.001)."

Es decir: superforecasters **0.096** (no 0.093), público general **0.121** (no 0.107), mejor LLM **0.122** (no 0.111). El sustentante, con su rango de baja confianza, en realidad se acercó más a la cifra correcta del LLM (0.11-0.12, y la real es 0.122) que la propia clave (0.111). Este error material se registra en `conocimiento/registro-de-errores.md`.

### Respuesta completa y correcta, con fuente
Karger et al. (2025), *"ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities"*, ICLR 2025 (arXiv 2409.19839). Tabla 2 (subconjunto de 200 preguntas estándar, horizontes de 7/30/90/180 días): superforecaster (mediana) **0.096** [IC 0.076, 0.116]; público general (mediana) **0.121** [0.101, 0.141]; mejor LLM (Claude-3-5-Sonnet-20240620, con valores congelados y *prompt* de "scratchpad") **0.122** [0.099, 0.146]. https://arxiv.org/abs/2409.19839 ; https://arxiv.org/pdf/2409.19839

Halawi et al. (2024), NeurIPS: sistema LLM con recuperación de noticias, Brier **0.179** contra **0.149** de la comunidad; el promedio de ambos da **0.146**, mejor que cualquiera de los dos por separado (esta cifra sí coincide con la clave del examen y no presentó problema).

### Adenda agregada (corrección, no solo adición)
Se corrigió/agregó en `19-biblioteca-esencial.md` (donde se resume Superforecasting/GJP) una ficha con las cifras exactas de ForecastBench (0.096/0.121/0.122) y de Halawi et al. (0.179/0.149/0.146), citando la Tabla 2 del PDF verificado.

---

## 22. S5-12 — Caso integrado non-GAAP: ASC 330-10-35-17

**Puntaje final: 4.625/5.**

### Qué faltó
Citar la norma **ASC 330-10-35-17** como base de la pérdida en compromisos de compra firmes no cancelables (el sustentante calculó bien los USD 840 M pero no citó la norma ni el renglón contable — costo de ventas, contra un pasivo).

### Respuesta completa y correcta, con fuente
ASC 330-10-35-17 (Inventario — pérdidas en compromisos de compra): cuando existe un compromiso de compra firme y no cancelable y el precio de mercado cae por debajo del precio del contrato, la pérdida se reconoce en el periodo en que ocurre la caída de precio, como un pasivo (y un cargo a resultados, típicamente en costo de ventas), no como un ajuste al inventario en sí. https://viewpoint.pwc.com/content/pwc-madison/ditaroot/us/en/pwc/accounting_guides/utilities_and_power_/utilities_and_power__US/chapter_11_inventory_US/113_firm_purchase_co_US.html

Complementos ya usados correctamente en el acta: ASC 855 (eventos posteriores, no reconocidos si la condición surgió después del cierre) y los C&DI 100.01/102.03/102.11 de la SEC sobre medidas non-GAAP. https://www.sec.gov/rules-regulations/staff-guidance/corporation-finance-interpretations/non-gaap-financial-measures

### Adenda agregada
Se agregó a `25-pronostico-de-resultados-y-estados-financieros.md` (§6.3, lista de verificación non-GAAP / eventos posteriores) la cita completa de ASC 330-10-35-17 junto a ASC 855 y los C&DI, que ya estaban parcialmente.

---

## Nota final sobre el alcance

Esta ficha cubre exclusivamente las 22 preguntas de S1 a S5 con puntaje final menor a 5.0. No se tocaron S6 ni S7 (que tienen su propia ficha de errores de razonamiento) ni las preguntas con 5.0/5 exacto, aunque varias de ellas también señalan huecos de base sin costo en puntos (por ejemplo S1-01 a S1-05, S1-09, S1-11, S1-12, S2-01 a S2-04, S2-07, S2-09, S2-10, S2-12, S3-01 a S3-03, S3-05, S3-07, S3-09, S3-11, S3-12, S4-01, S4-03 a S4-07, S4-09, S4-11, S4-12, S5-01, S5-02, S5-04, S5-05, S5-11): esos huecos quedan fuera del alcance de esta tarea porque no costaron puntos.
