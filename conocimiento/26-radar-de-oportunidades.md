# 26 — Radar de oportunidades: dónde están y cómo cazarlas con método

> Nivel: experto · Actualizado 2026-09-25 · Grado global: **B−**. El marco ("¿quién está del otro lado?", las restricciones institucionales como fuente de precios equivocados) es B. Casi todas las oportunidades concretas, **netas de costos y ejecutables desde GBM**, bajan a C. Las famosas de los 90 (inclusión en índices, deriva pre-FOMC, calendario en EUA) hoy son D. La ventaja real de este sistema está en tres cosas: **capacidad** (20,000 MXN no mueven precios), **ausencia de *benchmark* y de redenciones** (puede ser el comprador de quien está obligado a vender) y **disciplina registrada** (pronósticos con fecha, papel antes que dinero).

Convenciones: **Hecho** con fecha y fuente [n]. **Inferencia:** razonamiento propio. **Recomendación:** regla operable. **Cálculo propio:** datos de Yahoo Finance chart v8 al cierre del 24-sep-2026, precio sin dividendos, en la moneda del índice [38]. Este módulo no repite los capítulos 02 (factores), 03 (valuación), 14 (técnico), 15 (eventos corporativos), 16 (peso), 17 (crisis), 23 (geopolítica) ni 24 (política pública): los enlaza y se concentra en **priorizar**.

---

## 1. Objetivos de dominio

Quien se titula en este módulo debe poder:

1. Responder por escrito, antes de cualquier operación, **quién está del otro lado y por qué acepta perder**: restricción, mandato, sesgo o falta de atención. Si no hay respuesta, no hay operación.
2. Clasificar una oportunidad en la taxonomía BAIT (*Behavioral, Analytical, Informational, Technical*) [1] y decir cuál de las ventajas propias la explota.
3. Citar con cifras la evidencia de las ventas forzadas (Coval-Stafford [2]) y su crítica (Wardlaw [3]), la difusión lenta de la información (Hong-Lim-Stein [6]) y la desaparición del efecto índice [7].
4. Calcular si el *edge* esperado supera **2 veces** el costo total de ida y vuelta en GBM.
5. Puntuar y ordenar candidatos con el sistema de §6.2 y llevarlos por el *pipeline* de §6.3 sin saltarse etapas.
6. Saber qué oportunidades aparecen en cada régimen (§6.5) y cuáles ya murieron (§5.4).
7. Escribir los criterios para matar una tesis **antes** de entrar.

---

## 2. Marco teórico

### 2.1 Una oportunidad es una transferencia de riqueza con causa identificable

En un mercado sin fricciones, el rendimiento esperado de exceso es compensación por riesgo; todo lo que exceda eso sale del bolsillo de alguien. Si compras o vendes esperando un rendimiento de exceso, debes poder responder "¿quién está del otro lado?", y al responder especificas tu ventaja [1]. **Hecho:** la versión verificada es de BlueMountain (12-feb-2019) y solo la firma Mauboussin; la coautoría de Callahan queda **(no verificada)**.

Las cuatro fuentes de ineficiencia [1]:

| Fuente | Mecanismo | Quién pierde | Persistencia |
|---|---|---|---|
| **Conductual (B)** | Sobreextrapolación, creencias correlacionadas, miedo o euforia colectivos | La multitud que persigue desempeño | La más persistente y la más difícil de capturar, porque exige ir contra el consenso en el peor momento [1] |
| **Analítica (A)** | Mejor análisis, pesos distintos a la información, mejor actualización, **otro horizonte (arbitraje de tiempo)**, anticipar el cambio de narrativa | Quien procesa mal o con prisa | Media; se erosiona con la IA (§4.4) |
| **Informacional (I)** | Atención limitada y complejidad: la información existe, es pública y nadie la lee | Quien no mira | Media-alta en lo complejo y lo local |
| **Técnica (T)** | Vendedores o compradores forzados, flujos de fondos, arbitrajistas sin capital | Quien está obligado por mandato, apalancamiento o redenciones | Alta mientras existan las reglas que la causan |

**Hecho:** el *checklist* original [1] tiene 15 preguntas, una o más por fuente. Van desde "¿hay persecución de desempeño?" hasta "¿operas contra vendedores forzados?", "¿puedes tomar el otro lado de los flujos?" y "¿obtuviste **legalmente** información que otros no tienen?". El sistema lo adapta en §6.7.

**Hecho:** según datos de Taiwán citados en [1], los institucionales ganan 1.5 pp de exceso y los individuos pierden 3.8 pp. Barber-Odean [27] estudian 66,465 hogares (1991-1996): los que más operan ganan 11.4% anual contra 17.9% del mercado, con una rotación de alrededor de 75% al año. **Inferencia:** el minorista promedio es la contraparte que los demás explotan. Este sistema debe dejar de serlo antes de pretender explotar a alguien.

### 2.2 Las ventajas reales de un inversionista pequeño asistido por IA

| Ventaja | Mecanismo | Evidencia | Qué NO es |
|---|---|---|---|
| **Capacidad** | El rendimiento cae con el tamaño del fondo, sobre todo en acciones chicas | Chen-Hong-Huang-Kubik 2004 [26]; Berk-Green (cap. 02) | No da acceso a microcaps fuera del SIC |
| **Sin *benchmark* ni riesgo de carrera** | Puede concentrarse o quedarse en efectivo sin que lo despidan | Apéndice de agencia en [1] | El marcador de la arena sí es un *benchmark* (arena/investigacion/03) |
| **Sin redenciones ni margen** | Compra cuando otros están obligados a vender | [2][5] | Solo si hay efectivo en el estrés |
| **Horizonte flexible** | Arbitraje de tiempo contra quien se evalúa por trimestre | [1] | Se pierde si el sistema entra en pánico por su *drawdown* |
| **Amplitud de análisis con LLM** | Lee estados financieros y documentos regulatorios a escala; supera al analista mediano en dirección de utilidades | Kim-Muhn-Nikolaev [29] | **No** es velocidad de ejecución: sin API, la orden en GBM es manual |
| **Lectura político-regulatoria del dueño** | Proceso, tiempos e incentivos del gobierno (cap. 24 §6.2) | Cap. 24 | **Nunca** información privilegiada: la LMV sanciona su uso (artículos no verificados) |

Desventajas que hay que asumir: no hay corto en el SIC (cap. 15), el SIC no permite fracciones y un solo título de una acción cara puede superar el tope de concentración (arena/investigacion/04), la comisión es de 0.25% + IVA por lado (≈0.58% de ida y vuelta, más un *spread* de 0.10-0.60%; arena/investigacion/01) y el tipo de cambio mete un ruido trimestral de ±8-11% en MXN (cap. 15 §5.2).

### 2.3 La ecuación de la oportunidad

Edge neto por operación = (probabilidad de acierto × ganancia) − (probabilidad de fallo × pérdida) − costos totales.

Una oportunidad vale la pena si cumple cuatro condiciones:
- (a) El *edge* neto es ≥ 2 veces los costos.
- (b) La contraparte tiene una razón **estructural** para perder, no solo mala suerte.
- (c) Hay un reloj: un catalizador con fecha o un plazo de reversión conocido.
- (d) La pérdida está acotada y cabe en `riesgo_por_operacion` de `config/parametros.json`: 1% en el perfil estándar (0.5% en fase de prueba) y 3% en `arena_agresivo`.

**Inferencia:** el orden importa. La mayoría de las "oportunidades" del flujo de noticias falla en (b), y la mayoría de las académicas falla en (a) una vez que se aplican los costos del minorista mexicano.

### 2.4 Ciclo de vida de una ineficiencia

Una ineficiencia pasa por cuatro etapas: descubrimiento → publicación → arbitraje → residuo (o inversión: se vuelve trampa). **Hecho:** en 97 predictores, los rendimientos son 26% menores fuera de muestra y 58% menores después de la publicación. Los que más caen son los de mayor rendimiento en muestra, y lo que queda se concentra en acciones ilíquidas y de alto riesgo idiosincrático [12]. Harvey-Liu-Zhu piden un estadístico t > 3.0 para aceptar un factor nuevo [13]. Jensen-Kelly-Pedersen encuentran que la mayoría de los factores sí replica, en 13 temas y 93 países [14] (cap. 02 §5.3). **Inferencia:** lo publicado y famoso vale la mitad, y lo que sobrevive vive donde es caro operar. La oportunidad para un inversionista chico no está en el anuncio de la anomalía, sino en **las restricciones que no cambian** (mandatos, reglas de índices, regulación de aseguradoras, redenciones) y en **lo que nadie lee**.

---

## 3. Literatura canónica

| Obra | Hallazgo cuantificado | Enlace | Grado (para nosotros) |
|---|---|---|---|
| Mauboussin 2019, *Who Is On the Other Side?* | Taxonomía BAIT y *checklist* de 15 preguntas. Institucionales +1.5 pp vs individuos −3.8 pp (Taiwán) | [1] | B (marco) |
| Coval-Stafford 2007, JFE | 1980-2003. Venta forzada (≥15% de dueños con salidas ≥5%): −10.1% anormal en el trimestre (t = −11.5) y +7.74% de rebote en los meses 4-12. Umbrales más duros: −18.1% y +15.0%. Estrategia *long-short* de adelantarse: 27.9-45.4% anual anormal, **factible solo 95 de 168 meses** y sin costos de información | [2] | B en teoría, C ejecutable |
| Wardlaw 2020, JF | La medida estándar de presión por flujos contiene mecánicamente el rendimiento realizado. Corregida, la caída trimestral es "bastante despreciable" y **sin reversión posterior** | [3] | A como crítica |
| Lou 2012, RFS | Los flujos predecibles de fondos pronostican rendimientos a un año y luego revierten. Explican la persistencia de fondos, el *smart money* y parte del momentum | [4] | B |
| Ellul-Jotikasthira-Lundblad 2011, JFE | Las aseguradoras tienen más de un tercio de los bonos corporativos grado inversión. Las degradaciones fuerzan ventas, con caída y reversión, mayores cuando la industria está en problemas | [5] | B (bonos; no accesible desde GBM) |
| Hong-Lim-Stein 2000, JF | El momentum cae con el tamaño. Con baja cobertura residual de analistas rinde 1.13% al mes, contra 0.72% con alta cobertura (diferencia t = 3.50). El efecto es más fuerte en perdedores. Empresas sin analistas: 77.3% (1976) → 36.9% (1996) | [6] | B |
| Chan-Jegadeesh-Lakonishok 1996, JF | El rendimiento pasado y la sorpresa de utilidades predicen derivas por separado. Los analistas ajustan lento, sobre todo en los perdedores | [23] | B |
| Greenwood-Sammon 2025, JF | Inclusión en el S&P 500: 3.4% (80s) y 7.6% (90s) → 0.8% en 2010-2020 (versión NBER 2022); la versión publicada reporta 7.4% → 0.3%. Exclusiones: −0.6%. Causas: migraciones desde el MidCap, predictibilidad y *front-running* | [7] | A (como muerte) |
| Petajisto 2011, JEF | 1990-2005. Russell 2000: +4.7% en altas y −4.6% en bajas. S&P 500: +8.8% y −15.1%. Costo oculto para el fondo indexado: 38-77 pb al año (Russell 2000) y 21-28 pb (S&P 500) | [8] | B (histórico) |
| Harvey-Mazzoleni-Melone 2025, NBER w33554 | US$20 billones en pensiones y *target date* rebalancean a pesos fijos. Con acciones sobreponderadas, el rendimiento accionario cae 17 pb al día siguiente. Costo de ~US$16 mil millones al año | [9] | B (C ejecutable) |
| Alldredge-Blank 2019, JFR | 52,532 *insiders*, 1986-2014. Compras dentro de 2 días de la compra de un colega: +2.1% anormal el mes siguiente, 0.9 pp más que las compras solitarias | [15] | B bruto / C neto |
| Brune-Hens-Rieger-Wang 2015 | "*War puzzle*": si hay fase previa, la probabilidad creciente de guerra baja los precios y el estallido los **sube**. Una guerra sorpresa los baja | [16] | B |
| Berkman-Jacobsen-Lee 2011, JFE | 447 crisis políticas (1918-2006). El riesgo de crisis sube el E/P y el rendimiento por dividendo. Las industrias más expuestas pagan más | [17] | B |
| Daniel-Moskowitz 2016, JFE | El momentum se desploma en estados de pánico, tras caídas y con alta volatilidad, **cuando el mercado rebota**. La versión dinámica duplica el Sharpe | [24] | A (como riesgo) |
| Asness-Frazzini-Pedersen 2019, RAS | QMJ rinde en EUA y 24 países. La calidad se paga poco. La prima tocó mínimos en la burbuja de internet. Las valuaciones bajas de la calidad predicen más QMJ | [25] | B |
| Keloharju-Linnainmaa-Nyberg 2016, JF | Comprar por el rendimiento histórico del mismo mes calendario: 13% anual | [18] | C (costos, rotación) |
| Xu-McConnell 2008, FAJ | 1926-2005: todo el exceso de mercado ocurrió en los 4 días de cambio de mes. Se observa en 31 de 35 países | [20] | C hoy (ver §5.3) |
| Lucca-Moench 2015 / Kurov et al. 2021 | +49 pb en las 24 h previas al FOMC (1994-2011). **Desaparece** después de 2015 | [22] | D |

---

## 4. Lo más reciente 2023-2026

### 4.1 Flujos mecánicos: más grandes, más predecibles, más disputados

- **Hecho:** los activos pasivos en EUA llegaron a US$19.1 billones contra US$16.2 billones de los activos (oct-2025). En 2025 solo 38% de los fondos activos le ganó a su par pasivo, contra 42% en 2024. A 10 años, solo 21% sobrevivió y le ganó (Morningstar, vía [36]).
- **Hecho:** la inclusión en el S&P 500 dejó de pagar [7], a pesar de que hay más dinero indexado que nunca. **Inferencia:** más dinero mecánico no significa más oportunidad. Significa más competencia para adelantarse, porque la regla es pública.
- **Hecho:** desde 2026 el Russell se reconstituye **dos veces al año**. La reconstitución de diciembre, la primera en más de tres décadas, tiene *rank day* el 30-oct-2026, listas preliminares el 13-nov, bloqueo desde el 30-nov y entrada en vigor al cierre del 11-dic-2026 [11].
- **Hecho:** el rebalanceo de pensiones a pesos fijos es predecible y cuesta ~US$16 mil millones al año [9].
- **Hecho (arXiv, sin revisión de pares):** en Corea, en 2026, especuladores se adelantaron al rebalanceo de cierre de ETFs apalancados. Las acciones afectadas revierten ~75% de su reacción inicial al cierre siguiente, y a los tenedores minoristas les costó 17.6% de lo invertido [10]. **Inferencia:** los apalancados que permite el perfil arena tienen contraparte depredadora al cierre; no se opera en los últimos minutos del día en sus subyacentes.

### 4.2 Desarmes de *crowding*: la venta forzada moderna

- **Hecho:** entre el 1-jun y el 25-jul-2025 los *quants* de renta variable perdieron ~4.2% (Goldman Sachs, prima de corretaje, citado por MSCI). Ganaron las acciones de baja calidad, alta beta y mucho *short interest*. La interacción entre el *short interest* y los factores amplificó las pérdidas [32].
- **Hecho:** en octubre de 2025 hubo otro desplome del momentum (Bloomberg, 24-oct-2025, titular) [35]. En la primera quincena de 2026 los *quants* perdieron alrededor de 1% según Goldman y 2.8% según UBS, en "el mayor desapalancamiento de un día desde fines de diciembre" (Hedgeweek, 22-ene-2026) [33].
- **Hecho:** julio de 2026 fue el peor mes de la canasta VIP de *hedge funds* de Goldman contra el S&P 500 en más de 20 años (CNBC, 21-ago-2026, titular verificado) [34]. El detonante fue la reversión del *trade* de IA, no un deterioro de ingresos (fuente secundaria, no verificado).
- **Inferencia:** en 2025-2026 la venta forzada relevante para las acciones grandes del SIC la hacen los *hedge funds* que recortan apalancamiento bruto, no los fondos mutuos. Se reconoce porque las acciones más populares caen juntas, sin noticia de fundamentales, y las correlaciones se rompen [32]. Es la oportunidad técnica más frecuente del periodo y la trampa más frecuente para quien compra momentum tarde [24].

### 4.3 Caídas del mercado 2025-2026: qué pagó comprar

**Cálculo propio [38]:**

| Episodio | Cierre | Caída desde máximo | +1 mes | +3 meses | +12 meses |
|---|---|---|---|---|---|
| S&P 500, aranceles (8-abr-2025) | 4,982.8 | −18.9% | +13.7% | +26.0% | +36.8% |
| S&P 500, guerra de Irán (30-mar-2026) | 6,343.7 | −9.1% | +12.5% | +18.2% | — |
| IPC, aranceles (8-abr-2025) | 50,316.6 | −14.3% | +12.8% | +12.7% | +38.3% |
| IPC, elección y reforma judicial (3-jun-2024) | 51,807.6 | −11.8% | +0.3% | +2.6% | +11.5% (−3.9% a 6 meses) |
| IPC, guerra de Irán (20-mar-2026) | 64,134.9 | −10.4% | +7.3% | +4.7% | −1.2% a 6 meses |

**Inferencia:** los *shocks* externos de tipo C (aranceles) y de tipo B (guerra lejana), según la taxonomía del cap. 23, revirtieron rápido. El *shock* político **doméstico e institucional** de México en 2024 no revirtió en seis meses, porque cambiaba el flujo de efectivo descontado (Estado de derecho y prima de riesgo), no solo el sentimiento. **Regla:** la sobrerreacción se compra cuando el *shock* no altera las instituciones que generan los flujos; si las altera, se trata como cambio de valor fundamental (cap. 24 §2.4).

**Estado al 24-sep-2026 (cálculo propio):**
- S&P 500 en 7,704.1, −1.2% de su máximo (7,799.0).
- IPC en 64,264.2, **−10.2%** de su máximo del 11-feb-2026 (71,601.4).
- VIX en 15.67.

El contexto macro está en los caps. 16, 23 y 24: la Fed subió 25 pb el 16-sep y el bono a 10 años está en 5.11%.

### 4.4 IA: la ventaja de velocidad sobre noticias públicas ya se compitió

- **Hecho:** Lopez-Lira y Tang (v6, 28-oct-2025) encuentran que GPT-4 acierta ~90% en la reacción inicial, **no operable**, y predice la deriva siguiente, sobre todo en acciones chicas y noticias negativas. Pero los rendimientos de la estrategia **caen a medida que sube la adopción de LLMs** [28].
- **Hecho:** con estados financieros anónimos, GPT-4 supera al analista mediano en la dirección de las utilidades, iguala a un modelo de ML especializado y produce estrategias con mayor Sharpe [29].
- **Hecho:** los pronósticos de un LLM sobre periodos anteriores a su fecha de corte están contaminados por información del futuro. Esa "propensión de anticipación" colapsa a cero después del corte, y con ella la ventaja de precisión (Gao-Jiang-Yan, 29-dic-2025, revisado el 12-jun-2026) [30].
- **Hecho:** un artículo de arXiv sobre el "decaimiento del alfa por *crowding*" (dic-2025) fue **retirado** a los 16 días por validación empírica insuficiente [31].
- **Inferencia:** la IA no da ventaja por leer titulares más rápido; en eso compite contra todos. La ventaja está en leer lo **largo, complejo, local y en español** que casi nadie procesa: reportes a la BMV, eventos relevantes, DOF, iniciativas y resoluciones regulatorias (cap. 22). Además, hay que hacerlo con pronósticos fechados fuera de muestra y sin creerle al *backtest* de un LLM sobre fechas anteriores a su corte.

### 4.5 Cobertura de analistas

- **Hecho:** tras MiFID II, la cobertura de las pymes europeas no cayó al principio, pero sí cayó después de que se permitió volver a agrupar el pago de investigación y ejecución (estudio de largo plazo, Springer 2024) [37]. **(No verificado:** las cifras de cobertura de emisoras mexicanas medianas en 2026).
- **Inferencia:** en la BMV hay emisoras con uno o ningún analista. Ahí aplica Hong-Lim-Stein [6], con dos matices: el efecto es más fuerte en **malas noticias** (las omisiones y los perdedores tardan más en reflejarse) y la liquidez puede comerse el *edge* (cap. 11).

---

## 5. Evidencia real

### 5.1 Catálogo de oportunidades con su contraparte

| Oportunidad | Quién está del otro lado y por qué pierde | Magnitud documentada | Hoy, neta y ejecutable desde GBM | Grado |
|---|---|---|---|---|
| **Ventas forzadas de fondos** | Fondo con redenciones: vende lo líquido, no lo que quiere | −10.1% y +7.74% [2] | Tenencias con 45-60 días de rezago; Wardlaw [3] cuestiona la medida. Marco, no señal | C |
| **Desapalancamiento de *hedge funds*** | Fondo con límite de bruto o margen | Caídas agudas 2025-2026 [32]-[35] | Visible al día: las acciones "populares" caen sin noticia. Puede seguir cayendo | C |
| **Rebalanceos e índices** | Fondo indexado que minimiza *tracking error* | S&P: 7.6% → 0.3-0.8% [7]; Russell 2000: ±4.7% [8]; pensiones: −17 pb [9] | El anuncio ya no paga. Anticipar exige modelar la elegibilidad | D (anuncio) / C |
| **Sobrerreacción geopolítica o política** | Volatilidad objetivo y paridad de riesgo que recortan por regla; minorista en pánico | Mediana −6% en 17 días hábiles (cap. 23); *war puzzle* [16] | Sirve en índices y *shocks* externos, no en *shocks* institucionales (§4.3) | B (índice) / C |
| **Comprar tras caídas grandes** | Vendedores con límite de VaR, margen u horizonte corto | §5.2 | −10%: nada. −20%/−30%: mejor mediana, cola brutal | B− (índice) |
| **Baja cobertura de analistas** | Nadie: atención limitada | +0.42 pp/mes de momentum [6] | BMV y mid caps del SIC; decide la liquidez | C |
| **Momentum de revisiones** | Analistas anclados [23] | Señal compuesta B (cap. 15) | Filtro de selección; PEAD muerto en large caps | B |
| ***Insiders* en *cluster*** | Vendedor sin información | +2.1%/mes [15] | Small caps casi fuera del SIC | C neto |
| ***Spin-offs*** | Accionista de la matriz que vende por mandato | Cap. 15 | Vehículo 2016-2026 bajo el mercado | C |
| **Calidad a precio razonable** | Buscador de lotería que sobrepaga la "basura" | QMJ en 25 países [25] | Accesible; sufre en rallies de basura [32] | B |
| **Tendencia y momentum** | Subreacción y luego sobrerreacción | Cap. 14 | Accesible; *crash* en rebotes [24] | B |
| **Estacionalidad** | Poco clara | §5.3 | Muerta en EUA desde 2013 | D / C (México) |

### 5.2 Comprar después de caídas: la evidencia completa (cálculo propio [38])

Método. Un evento es el **primer cierre** que queda X% debajo del máximo histórico previo. No se cuenta otro evento del mismo umbral hasta que haya un máximo nuevo; por eso el periodo 1929-1954 aporta uno solo. Se usa el índice de precio y se reporta el rendimiento a H días hábiles.

**S&P 500 (1927-2026):**

| Condición | n | 3 meses (mediana) | 12 meses (mediana / media / % > 0 / peor) | 3 años (mediana / % > 0) | Caída adicional (mediana / peor) |
|---|---|---|---|---|---|
| Incondicional | ~24,500 días | +2.6% | +9.6% / +8.2% / 70% | +26.1% / 79% | — |
| Primer −10% | 26 | +2.5% | +11.4% / +5.3% / 65% / −39.5% | +26.0% / 72% | −16.0% / −84.6% |
| Primer −20% | 12 | +5.1% (83% > 0) | +19.8% / +11.6% / 67% / −29.1% | +35.4% / 83% | −9.0% / −80.7% |
| Primer −30% | 7 | +8.1% | +12.8% / +15.8% / 57% / −16.2% | +20.1% / 86% | −25.2% / −78.5% |

**IPC (1991-2026, en MXN):**

| Condición | n | 3 meses (mediana / % > 0) | 12 meses (mediana / % > 0) | 3 años (mediana / % > 0) | Caída adicional (mediana) |
|---|---|---|---|---|---|
| Incondicional | ~8,700 días | +2.8% / 62% | +8.8% / 70% | +26.7% / 89% | — |
| Primer −10% | 24 | +3.6% / 71% | +6.6% / 61% | +27.6% / 91% | −11.5% |
| Primer −20% | 9 | +14.3% / 89% | +5.5% / 56% | +42.9% / 100% | −19.5% |
| Primer −30% | 6 | +13.0% / 100% | +34.6% / 100% | +66.8% / 100% | −16.2% |

Lectura (Inferencia):
1. **Un −10% no es señal.** En ambos mercados, el rendimiento posterior es igual o peor que el incondicional. El IPC está hoy en −10.2%: por sí solo, eso no justifica nada.
2. **−20% y −30% mejoran la mediana, no la media ni la cola.** En el S&P, después del primer −20% todavía hubo una caída adicional mediana de −9%, y de −80.7% en 1929. En la cuenta arena, el cortacircuitos de −12% se activa antes de que llegue la recompensa. **Recomendación:** comprar caídas grandes solo en índices amplios, escalonado (tercios en −20%, −30% y confirmación de tendencia; cap. 14) y con un tamaño que sobreviva a otro −25%.
3. **En el IPC la señal es más fuerte a 3 años** (100% de episodios positivos en −20% y −30%), pero con n = 6-9 y dentro de muestra. Grado B− y no más.
4. Complementos: comprar tras un pico de VIX ≥ 30 (cap. 17 §5.5) y la estadística de *shocks* geopolíticos (cap. 23 §5.1).
5. **No se aplica a acciones individuales.** Una acción puede ir a cero; un índice se reconstituye (cap. 01, Bessembinder).

### 5.3 Estacionalidad: lo que queda (cálculo propio [38])

| Efecto | Periodo | Resultado | Lectura |
|---|---|---|---|
| **Cambio de mes (TOM)** en el S&P 500. Día TOM = último día hábil y 3 primeros | 1950-1999 | 14.0 pb/día vs 1.6 pb en el resto (t = 6.5) | Fuerte |
| | 2000-2012 | 6.3 vs −0.5 pb (t = 1.1) | Débil |
| | 2013-2026 | 5.2 vs 5.5 pb (t ≈ 0) | **Muerto** |
| TOM en el IPC | 1992-2008 | 25.2 vs 3.7 pb (t = 3.3) | Fuerte |
| | 2009-2026 | 8.2 vs 1.7 pb (t = 1.5) | Débil, no significativo |
| **Halloween** (nov-abr vs may-oct) en el S&P 500 | 1950-1999 | 8.0% vs 1.9%; el invierno gana 33 de 50 | Fuerte |
| | 2013-2025 | 6.0% vs 6.6%; el invierno gana 5 de 13 | **Invertido** |
| Halloween en el IPC | 2009-2025 | 5.4% vs 2.2%; el invierno gana 9 de 17 | Moneda al aire |

**Veredicto:** Xu-McConnell [20] y Bouman-Jacobsen [21] describen un mundo que ya no existe en EUA. La estacionalidad del mismo mes (Keloharju et al. [18], Heston-Sadka [19]) es transversal, exige rotación alta y queda fuera de alcance con los costos de GBM. **Grado D como señal de entrada.** Sirve, cuando mucho, para **no pelear** con flujos de fin de mes o de fin de año en el momento de ejecutar.

### 5.4 Oportunidades que murieron o se volvieron trampas

| Antes | Ahora | Causa | Fuente |
|---|---|---|---|
| Comprar el anuncio de inclusión en el S&P 500 | 0.3-0.8% | Predictibilidad y *front-running* | [7] |
| Deriva pre-FOMC | Desaparecida después de 2015 | Publicación y menos incertidumbre | [22] |
| TOM y Halloween en EUA | ≈0 o invertidos desde 2013 | Publicación | §5.3 |
| Señales de titulares con LLM | Caen al subir la adopción | Competencia | [28] |
| PEAD en large caps, recompras, clones de 13F, Congreso | C o D | Ver cap. 15 §5.1 | Cap. 15 |
| Comprar el momentum más popular entre *hedge funds* | Desplomes en 2025-2026 | *Crowding* | [32]-[35] |
| "Comprar la caída" de 10% | Sin ventaja | No es una venta forzada | §5.2 |
| Medir la presión de ventas forzadas con la fórmula clásica | Artefacto mecánico | Contiene el rendimiento realizado | [3] |

---

## 6. Traducción operable

### 6.1 Principios

1. **Sin contraparte nombrada no hay tesis.** Se escribe en una línea: "Del otro lado está ___, que opera por ___ (restricción, mandato, sesgo o falta de atención) y deja de hacerlo cuando ___".
2. **Lo que la ventaja propia permite explotar:** restricciones ajenas (T), complejidad y abandono (I), horizonte (A). La velocidad no está en la lista.
3. **El costo manda.** Umbral mínimo: *edge* neto esperado ≥ 2 × (0.58% de comisión de ida y vuelta + *spread* estimado + costo cambiario si hay conversión). Con una orden de 5,000 MXN y *spread* de 0.30%, el costo es 0.88%: se exige un *edge* neto ≥ 1.76%, es decir, bruto ≥ ≈2.6% por operación.
4. **Un pronóstico registrado antes de la operación**, siempre (`herramientas/pronosticos.py`).
5. **Ningún dinero real en fase 0.** `prioridad_actual.fase = 0` en `config/parametros.json`.

### 6.2 Sistema de puntuación (Puntaje de Oportunidad, 0-100)

**Puertas eliminatorias.** Todas deben cumplirse; si una falla, el candidato se descarta sin puntuar:

| Puerta | Criterio |
|---|---|
| P1 Contraparte | Nombrada, con su restricción o sesgo y la condición en que deja de operar |
| P2 Evidencia | ≥ C para papel y ≥ B para dinero real (fase 1+) |
| P3 Ejecutable | Existe en el SIC o la BMV vía GBM, es *long-only* (o ETF inverso) y un título cabe en `concentracion.accion_individual_max` (0.10 estándar, 0.30 arena) |
| P4 Costos | *Edge* neto esperado ≥ 2 × costo total de ida y vuelta |
| P5 Salida | *Stop* de precio, *stop* de tiempo y el hecho que refuta la tesis, escritos antes de entrar |
| P6 Legalidad | Cero información privilegiada. Ante la duda, no se opera |

**Puntaje:**

| Componente | Peso | Escala |
|---|---|---|
| *Edge* neto esperado / costo | 25 | 2-3× = 10 · 3-5× = 18 · > 5× = 25 |
| Grado de evidencia | 15 | A = 15 · B = 11 · C = 5 |
| Catalizador con fecha | 10 | Fecha fija ≤ 3 meses = 10 · ventana de 3-6 meses = 6 · reversión sin fecha = 2 |
| Asimetría (ganancia en escenario favorable / pérdida al *stop*) | 15 | ≥ 3:1 = 15 · 2:1 = 10 · 1.5:1 = 6 · < 1.5:1 = 0 |
| Liquidez en SIC/BMV | 5 | *Spread* ≤ 0.10% y volumen alto = 5 · medio = 3 · bajo = 0 |
| Costos (incluido FX) | 5 | ≤ 0.7% de ida y vuelta = 5 · 0.7-1.2% = 3 · > 1.2% = 0 |
| Correlación con la cartera (60 días, en MXN) | 10 | ρ < 0.3 = 10 · 0.3-0.6 = 6 · 0.6-0.8 = 2 · > 0.8 = 0 |
| Riesgo geopolítico o regulatorio (inverso) | 10 | Se califica con el cap. 24 §6.4 (0-3 por renglón) y el árbol del cap. 23 §6.1. Bajo = 10 · medio = 5 · alto = 0 |
| Ventaja propia verificable | 5 | T o I que exploten capacidad, ausencia de mandato o lectura local o política = 5 · solo A = 2 · ninguna = 0 |
| **Penalización por *crowding*** | −10 a 0 | Posición popular entre *hedge funds*, momentum extremo con dispersión que se rompe, o narrativa dominante en medios [32] |

**Umbrales y tamaño (Recomendación, coherente con `parametros.json`):**
- **≥ 80:** dossier y comité prioritarios. El riesgo es hasta el 100% de `riesgo_por_operacion` del perfil (estándar 1%, o 0.5% en fase de prueba; arena 3%), con topes de Kelly (`kelly.fraccion_max` 0.25; arena 0.5).
- **70-79:** dossier y comité. Hasta 50% del riesgo máximo.
- **55-69:** vigilancia, con alerta del disparador que la subiría de rango.
- **< 55:** descarte, registrado con su razón. Se revisa solo si cambia la contraparte o el catalizador.

Máximo 8 operaciones al mes en la arena (`operaciones_max_mes`). Si hay más candidatos ≥ 70 que cupo, se elige por puntaje ajustado por correlación: se toma el mejor y se vuelve a puntuar el resto con la cartera nueva.

### 6.3 *Pipeline*

| Etapa | Qué produce | Herramienta | Criterio para avanzar | Plazo |
|---|---|---|---|---|
| **0. Radar** | Candidatos con puntaje preliminar y contraparte | `tablero.py` (régimen), `arena/investigacion/pantalla.py`, `edgar.py` (Forms 4, 13D, 10), `geopolitica.py`, calendario §6.6 | Puertas P1-P6 y ≥ 55 | Semanal y por evento |
| **1. Dossier** | Cadena causal, qué descuenta el precio, escenarios que suman 100%, contraparte | Skill `ficha-empresa`, o ficha de oportunidad con la misma estructura | ≥ 70 con datos primarios | 48 h |
| **2. Comité** | Votos, disenso y tamaño | Skill `comite-de-inversion` | Sin veto de riesgo; mayoría y confianza ≥ 55 | Antes de cualquier orden |
| **3. Pronóstico** | Probabilidad, fecha, criterio e intervalo de 80% | `pronosticos.py` → `bitacora/pronosticos.csv` | Registrado **antes** de operar; nunca se sobrescribe | El mismo día |
| **4. Papel** | Operación con *stop* y tesis | `portafolio.py registrar` | Por estrategia: ≥ 3 meses, ≥ 30 operaciones, DSR ≥ 0.95, PBO ≤ 0.25 | Continuo |
| **5. Real** | Orden para capturar a mano en GBM | Solo fase 1+, 25% del capital, con aprobación del dueño | Salida de fase 0: examen ≥ 90%, Brier ≤ 0.20 | — |
| **6. Post-mortem** | Decisión contra suerte; peso de cada agente | Skill `post-mortem` | Obligatorio al cerrar | ≤ 7 días |

### 6.4 Criterios de descarte y de muerte de una tesis

**Se descarta en el radar si:**
- La contraparte es "el mercado" o "los que no entienden".
- La tesis depende de ser más rápido con una noticia pública [28].
- La única evidencia es un *backtest* de LLM anterior a su corte [30], un pantallazo o un artículo retirado [31].
- El catalizador ya ocurrió y el precio ya se movió más de la mitad del objetivo.
- El instrumento no cabe en el tope de concentración o el *spread* supera 1%.

**Se mata la tesis abierta, sin discusión, si:**
1. Toca el *stop* de precio.
2. Vence el *stop* de tiempo: 1.5 veces el horizonte del pronóstico sin que se cumpla el catalizador.
3. Se refuta el hecho central. Ejemplos: el vendedor "forzado" no lo estaba, la revisión de estimados se revierte, el *shock* resultó institucional y no transitorio (§4.3).
4. Desaparece la contraparte: el flujo ya ocurrió o la regla del índice cambió.
5. La correlación de la posición con la cartera supera 0.8, o el sector supera `sector_max`.
6. El evento geopolítico o regulatorio se reclasifica a un tipo más grave (cap. 23 §6.1).

**Se pausa la estrategia completa si:**
- Hay 5 pérdidas seguidas (`rachas.perdedoras_para_pausa`).
- El Brier de sus pronósticos es > 0.25 con ≥ 50 pronósticos.
- El DSR fuera de muestra cae bajo 0.95.
- El *edge* neto medido en papel es < 1× costos durante 3 meses.

### 6.5 Oportunidades típicas por régimen

**Advertencia de evidencia:** Ilmanen et al. (2021, cap. 02 §5.3) encuentran que las primas de factores casi no se ligan a los regímenes macro. La tabla describe **qué tipo de oportunidad aparece** en cada régimen, no qué factor gana. Grado C como guía de asignación y B como guía de *dónde buscar*.

| Régimen (identificación) | Oportunidades que aparecen | Evidencia | Qué falla | Riesgo dominante |
|---|---|---|---|---|
| **Expansión**: ISM > 50 y subiendo, revisiones de utilidades positivas, *spreads* HY estrechos, índice > SMA200, VIX < 20 | Tendencia y momentum (cap. 14); revisiones al alza [23]; calidad a precio razonable sin pagar de más [25]; eventos corporativos (fusiones, cap. 15) | B | Comprar caídas pequeñas (§5.2); *value* profundo sin catalizador | *Crowding* y desarmes [32]-[35] |
| **Desaceleración**: ISM bajando, revisiones negativas en aumento, curva invirtiéndose o Fed subiendo con inflación | Calidad y baja volatilidad como defensa (cap. 02); dólar como cobertura en MXN (cap. 16); vigilar a los vendedores forzados que vienen | B (defensa) | Momentum de alta beta; cíclicas apalancadas | Error de *timing*: salir demasiado pronto |
| **Estrés**: VIX > 30, *spreads* HY abriéndose rápido, correlaciones → 1, redenciones y llamadas de margen | **Ventas forzadas** [2][5]; primeras compras escalonadas en índices después de −20% (§5.2) o de un VIX ≥ 30 (cap. 17); *shocks* externos que no cambian instituciones (cap. 23) | B− (índice) | Comprar acciones individuales apalancadas; confiar en el bono largo si el *shock* es inflacionario (cap. 17) | Caída adicional de −25% o más; quedarse sin efectivo |
| **Recuperación**: índice recupera la SMA200, *spreads* se cierran, amplitud > 60% | Calidad y valor castigados; *small caps* y baja cobertura [6]; volver a tendencia cuando se confirme | B | **Momentum**: su *crash* típico ocurre aquí [24] | Llegar tarde o quedarse defensivo |

**Diagnóstico al 25-sep-2026 (Inferencia, a validar con `tablero.py` y el cap. 13):** EUA está en **expansión tardía con endurecimiento monetario**, en la frontera con la desaceleración: S&P a −1.2% del máximo, VIX en 15.7, Fed subiendo, bono a 10 años en máximos de 12 meses y desarmes de *crowding* recurrentes. México está en **corrección** (IPC −10.2%) sin señal de estrés. Consecuencias:
- tendencia y momentum solo con penalización por *crowding*;
- preparar efectivo y un protocolo para ventas forzadas;
- ninguna compra "porque bajó 10%".

### 6.6 Calendario del radar (temporada octubre 2026 a abril 2027)

| Fecha | Evento | Tipo de oportunidad | Fuente |
|---|---|---|---|
| 30-oct-2026 | *Rank day* del Russell (diciembre) | Flujos de índice (T) | [11] |
| 3-nov-2026 | Intermedias de EUA | *Shock* político tipo C | Caps. 23 y 24 |
| 4-nov-2026 | *Refunding* del Tesoro | Tasas | Cap. 24 |
| 13-nov-2026 | Listas preliminares del Russell | Flujos (T); en el SIC solo los nombres listados | [11] |
| nov-dic 2026 | Venta de pérdidas fiscales en EUA | Estacionalidad (D como señal) | §5.3 |
| 11-dic-2026 | Reconstitución efectiva del Russell al cierre | No operar al cierre de ese día | [11] |
| dic-2026 | Rebalanceo trimestral del S&P (convención del tercer viernes: 18-dic; fecha no confirmada) | Flujos (D para anuncios) | [7] |
| 10-ene-2027 | Vence la tregua arancelaria EUA-China | *Shock* tipo C/D en tecnología | Cap. 23 §6.6 |
| Continuo | Temporadas de reportes (oct-nov y ene-feb) | Revisiones y sorpresas (B compuesta) | Cap. 15 |
| Disparadores | S&P o IPC en −20% o −30%; VIX ≥ 30; caída de las acciones populares entre *hedge funds* sin noticia | Estrés y ventas forzadas | §5.2, cap. 17 |

### 6.7 *Checklist* de 12 preguntas antes de subir un candidato al dossier

1. ¿Quién está del otro lado, qué lo obliga o lo engaña y cuándo deja de hacerlo?
2. ¿Es B, A, I o T? ¿Cuál de mis ventajas (§2.2) la explota?
3. ¿Qué grado tiene la evidencia neta de costos, y fuera de muestra, después de la publicación?
4. ¿El *edge* esperado es ≥ 2× el costo total en GBM, incluido el tipo de cambio?
5. ¿Qué descuenta el precio hoy (cap. 03, DCF inverso)?
6. ¿Cuál es el catalizador y cuál es su fecha?
7. ¿Cuál es la asimetría entre el escenario favorable y el *stop*?
8. ¿Cómo se correlaciona con lo que ya tengo, medido en MXN?
9. ¿Qué evento geopolítico o regulatorio la mata, y con qué probabilidad (mercados de predicción, cap. 23)?
10. ¿Está congestionada?
11. ¿Qué hecho observable refuta la tesis y cuándo lo sabré?
12. ¿La registré como pronóstico con probabilidad y fecha?

### 6.8 Parámetros propuestos (para revisión con el dueño; no modifican `config/parametros.json`)

```json
"radar": {
  "edge_min_multiplo_costos": 2.0,
  "umbral_dossier": 70,
  "umbral_vigilancia": 55,
  "tamano_por_puntaje": {"70-79": 0.5, "80+": 1.0},
  "stop_tiempo_multiplo_horizonte": 1.5,
  "correlacion_max_nueva_posicion": 0.8,
  "compra_caidas_indice": {"umbrales": [-0.20, -0.30], "tramos": 3, "solo_indices_amplios": true},
  "brier_pausa_estrategia": 0.25,
  "no_operar_cierre_en_fechas_de_rebalanceo": true
}
```

---

## 7. Trampas

1. **"Está barato porque bajó."** Un −10% no tiene *edge* (§5.2). Sin vendedor forzado identificable, la caída es información.
2. **Confundir la contraparte.** Si quien vende está informado, el que pierde eres tú.
3. **Artefactos de medición.** La fórmula clásica de presión por flujos se contamina con el rendimiento [3]. Los *backtests* de LLM anteriores a su corte ven el futuro [30].
4. **Anomalías publicadas como si fueran nuevas.** Descuenta ~58% de lo publicado [12], y más si la regla es sencilla y famosa.
5. **Comprar el momentum del *crowding* justo antes del desarme** (2025-2026 [32]-[35]). El momentum se desploma en los rebotes [24].
6. **Tratar un *shock* institucional como si fuera transitorio.** La reforma judicial de 2024 no revirtió en seis meses (§4.3).
7. **Operar al cierre en días de rebalanceo con ETFs apalancados.** Ahí está el depredador [10].
8. **Ignorar el tipo de cambio.** Un *edge* de 2-4% en USD puede desaparecer con ±8-11% trimestral de USDMXN (cap. 16).
9. **Citar fuentes retiradas o sin revisión de pares como si fueran A** [31][10].
10. **Confundir la ventaja política del dueño con información privilegiada.** La primera es análisis de procesos públicos; la segunda es delito.
11. **Sobreoperar para "aprovechar todo".** Los que más operan pierden 6.5 pp al año contra el mercado [27]. En la arena, el tope es de 8 operaciones al mes.

---

## 8. Examen de titulación

**1. ¿Qué es la taxonomía BAIT y cuál de sus fuentes es la más persistente y cuál la más explotable para esta cuenta?**
R: Son las ineficiencias conductuales, analíticas, informacionales y técnicas [1]. La conductual es la más persistente, pero la más difícil de capturar. Para una cuenta chica sin mandato ni redenciones, las más explotables son la técnica (restricciones ajenas) y la informacional (lo complejo y local que nadie lee).

**2. Da las magnitudes de Coval-Stafford y la crítica de Wardlaw.**
R: En 1980-2003, las acciones con ventas forzadas generalizadas caen −10.1% anormal en el trimestre y rebotan +7.74% en los meses 4-12 (+15% con umbrales más duros). La estrategia *long-short* rinde 27.9-45.4% anual anormal, pero solo es factible en 95 de 168 meses y sin costos de información [2]. Wardlaw muestra que la medida contiene mecánicamente el rendimiento realizado; corregida, la presión es despreciable y sin reversión [3]. Grado para nosotros: C.

**3. ¿Por qué desapareció el efecto de inclusión en el S&P 500 si hay más dinero indexado que nunca?**
R: Porque las inclusiones se volvieron predecibles (muchas son migraciones desde el MidCap) y los arbitrajistas compran antes del anuncio. El efecto pasó de 7.4-7.6% en los 90 a 0.3-0.8% en 2010-2020 [7].

**4. ¿Qué encontró Hong-Lim-Stein y dónde aplica hoy?**
R: El momentum es más fuerte en acciones con baja cobertura residual (1.13% contra 0.72% al mes) y el efecto se concentra en los perdedores: las malas noticias viajan lento [6]. Aplica a emisoras de la BMV y a mid caps del SIC poco cubiertas, siempre que la liquidez no se coma el *edge*.

**5. El IPC está en −10.2% de su máximo. ¿Es señal de compra?**
R: No. En el IPC, desde 1991, el primer −10% lleva a una mediana de +6.6% a 12 meses con 61% de episodios positivos, peor que el incondicional (+8.8% y 70%). En el S&P tampoco hay ventaja (§5.2).

**6. ¿Qué mejora al comprar tras un −20% en el S&P y qué no?**
R: Mejora la mediana a 12 meses (+19.8% contra +9.6%). No mejora la probabilidad de ganar (67% contra 70%) ni la cola: la caída adicional mediana es de −9% y la peor de −80.7%. Por eso se compra escalonado, solo en índices y con un tamaño que sobreviva.

**7. Explica el *war puzzle* y cómo se usa.**
R: Cuando hay una fase previa, la probabilidad creciente de guerra baja los precios y el estallido los sube (se resuelve la incertidumbre). Una guerra sorpresa los baja [16]. Se usa para no vender en el estallido de un conflicto anticipado y para comprar el *shock* sorpresa externo con el protocolo del cap. 23.

**8. ¿Por qué el *shock* político mexicano de 2024 no se compró igual que el de aranceles de 2025?**
R: Porque cambió las instituciones que generan los flujos (Estado de derecho, prima de riesgo), no solo el sentimiento. El IPC estaba en −3.9% seis meses después del 3-jun-2024. Tras el 8-abr-2025, en cambio, subió +38.3% en 12 meses (§4.3).

**9. ¿Qué ventaja da la IA y cuál ya no?**
R: Ya no da ventaja la velocidad sobre titulares públicos: su rendimiento cae con la adopción [28]. Sí la da el análisis amplio y profundo de información compleja o local [29], con pronósticos fuera de muestra. Hay que desconfiar de los *backtests* anteriores al corte del modelo [30].

**10. Enumera las 6 puertas del sistema de puntuación.**
R: Contraparte nombrada; evidencia ≥ C (papel) o ≥ B (real); ejecutable en GBM dentro del tope de concentración; *edge* ≥ 2× costos; salida definida (precio, tiempo y hecho que refuta); legalidad (cero información privilegiada).

**11. Una tesis tiene puntaje 74, ρ = 0.85 con la cartera y el catalizador en 5 meses. ¿Qué haces?**
R: La correlación de 0.85 da 0 en su componente y dispara el criterio de muerte (> 0.8), así que no entra como posición nueva. Se vuelve a puntuar como **sustituto** de la posición correlacionada; si no la supera, queda en vigilancia.

**12. ¿En qué régimen se desploma el momentum y qué haces?**
R: En la recuperación posterior a un pánico, cuando el mercado rebota tras caídas con volatilidad alta [24]. Se reduce el momentum (o se usa con control de volatilidad) y se sube la prioridad de calidad y valor castigados.

**13. ¿Por qué la ventaja de "no tener redenciones" puede ser ilusoria?**
R: Porque solo existe si hay efectivo cuando llegan las ventas forzadas y si los cortacircuitos propios no obligan a vender en ese mismo momento.

**14. ¿Qué evidencia hay de estacionalidad hoy?**
R: En EUA, el cambio de mes pasó de t = 6.5 (1950-1999) a t ≈ 0 (2013-2026), y Halloween se invirtió desde 2013. En México ambos efectos son débiles y no significativos después de 2009 (§5.3). Grado D como señal.

**15. ¿Qué pasa en la arena si ves 12 candidatos con puntaje ≥ 70 en un mes?**
R: Caben 8 operaciones al mes. Se toma el mejor, se vuelve a puntuar el resto con la cartera nueva y se repite. Lo demás queda en vigilancia, registrado como pronóstico para medir la calidad del radar.

---

## 9. Fuentes

1. Mauboussin (12-feb-2019), *Who Is On the Other Side?*, BlueMountain. https://macro-ops.com/wp-content/uploads/2019/02/Who-Is-On-the-Other-Side.pdf
2. Coval y Stafford (2007), *JFE* 86(2). https://www.sciencedirect.com/science/article/abs/pii/S0304405X07001158 · NBER w11357 (cifras del texto): https://www.nber.org/papers/w11357
3. Wardlaw (2020), *JF* 75. https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12962
4. Lou (2012), *RFS* 25(12). https://ideas.repec.org/a/oup/rfinst/v25y2012i12p3457-3489.html
5. Ellul, Jotikasthira y Lundblad (2011), *JFE* 101(3). https://ideas.repec.org/a/eee/jfinec/v101y2011i3p596-620.html
6. Hong, Lim y Stein (2000), *JF* 55(1). https://www.columbia.edu/~hh2679/jf-badnews.pdf
7. Greenwood y Sammon (2025), *JF*. https://onlinelibrary.wiley.com/doi/10.1111/jofi.13410 · NBER w30748: https://www.nber.org/system/files/working_papers/w30748/w30748.pdf
8. Petajisto (2011), *JEF* 18(2). https://ideas.repec.org/a/eee/empfin/v18y2011i2p271-288.html
9. Harvey, Mazzoleni y Melone (2025, rev. ene-2026), NBER w33554. https://www.nber.org/papers/w33554
10. Zhao (4-ago-2026), arXiv 2608.03703, sin revisión de pares. https://arxiv.org/abs/2608.03703
11. FTSE Russell (1-sep-2026), calendario de la reconstitución de diciembre. https://www.lseg.com/en/media-centre/press-releases/ftse-russell/2026/ftse-russell-announces-december-2026-russell-us-indexes-reconstitution-schedule
12. McLean y Pontiff (2016), *JF* 71(1). https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12365
13. Harvey, Liu y Zhu (2016), *RFS* 29(1); NBER w20592. https://www.nber.org/papers/w20592
14. Jensen, Kelly y Pedersen (2023), *JF*. https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.13249
15. Alldredge y Blank (2019), *JFR* 42(2). https://onlinelibrary.wiley.com/doi/abs/10.1111/jfir.12172
16. Brune, Hens, Rieger y Wang (2015), *Int. Rev. Economics*. https://link.springer.com/article/10.1007/s12232-014-0215-7
17. Berkman, Jacobsen y Lee (2011), *JFE* 101(2). https://ideas.repec.org/a/eee/jfinec/v101y2011i2p313-332.html
18. Keloharju, Linnainmaa y Nyberg (2016), *JF* 71(4). https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12398
19. Heston y Sadka (2008), *JFE* 87(2); magnitud no verificada. https://ideas.repec.org/a/eee/jfinec/v87y2008i2p418-445.html
20. Xu y McConnell (2008), *FAJ* 64(2). https://www.tandfonline.com/doi/abs/10.2469/faj.v64.n2.11
21. Bouman y Jacobsen (2002), *AER* 92(5); contrastado con el cálculo de §5.3. https://ideas.repec.org/a/aea/aecrev/v92y2002i5p1618-1635.html
22. Lucca y Moench (2015), *JF*: https://onlinelibrary.wiley.com/doi/10.1111/jofi.12196 · Kurov, Wolfe y Gilbert (2021), *FRL*: https://www.sciencedirect.com/science/article/pii/S1544612320315956
23. Chan, Jegadeesh y Lakonishok (1996), *JF* 51(5). https://ideas.repec.org/a/bla/jfinan/v51y1996i5p1681-1713.html
24. Daniel y Moskowitz (2016), *JFE* 122(2). https://ideas.repec.org/a/eee/jfinec/v122y2016i2p221-247.html
25. Asness, Frazzini y Pedersen (2019), *RAS* 24(1). https://ideas.repec.org/a/spr/reaccs/v24y2019i1d10.1007_s11142-018-9470-2.html
26. Chen, Hong, Huang y Kubik (2004), *AER* 94(5). https://www.aeaweb.org/articles?id=10.1257%2F0002828043052277
27. Barber y Odean (2000), *JF* 55(2). https://ideas.repec.org/a/bla/jfinan/v55y2000i2p773-806.html
28. Lopez-Lira y Tang (v6, 28-oct-2025), arXiv 2304.07619. https://arxiv.org/abs/2304.07619
29. Kim, Muhn y Nikolaev (2024), arXiv 2407.17866. https://arxiv.org/abs/2407.17866
30. Gao, Jiang y Yan (29-dic-2025, rev. 12-jun-2026), arXiv 2512.23847. https://arxiv.org/abs/2512.23847
31. Lee (dic-2025), arXiv 2512.11913, **retirado** el 27-dic-2025. https://arxiv.org/abs/2512.11913
32. MSCI (2025), *Unraveling Summer 2025's Quant Fund Wobble*. https://www.msci.com/research-and-insights/blog-post/unraveling-summer-2025s-quant-fund-wobble
33. Hedgeweek (22-ene-2026). https://www.hedgeweek.com/quant-hedge-funds-see-worst-drawdown-since-october-as-crowded-trades-unwind/
34. CNBC (21-ago-2026), solo el titular verificado: https://www.cnbc.com/2026/08/21/goldman-hedge-funds-historic-underperformance-sp500-degrossing.html · Detalle secundario: https://www.wallstreetsync.com/the-ai-unwind-hedge-funds-wrong-side-best-trade-2026/
35. Bloomberg, solo titulares (24-oct-2025): https://www.bloomberg.com/news/articles/2025-10-24/fast-money-quants-stumble-as-momentum-bust-roils-strategies · (6-jul-2026): https://www.bloomberg.com/news/articles/2026-07-06/quant-hedge-funds-extend-worst-run-since-2023-as-momentum-slides
36. Morningstar, *Active/Passive Barometer* de cierre de 2025: https://www.morningstar.com/business/insights/research/active-passive-barometer · CNBC (25-feb-2026): https://www.cnbc.com/2026/02/25/active-managers-vs-index-funds.html (cifras vía resumen de búsqueda)
37. Estudio de largo plazo sobre MiFID II (2024), *J. Business Economics*. https://link.springer.com/article/10.1007/s11573-024-01205-8
38. Cálculo propio: Yahoo Finance chart v8 (^GSPC desde 1927, ^MXX desde 1991, ^VIX), cierres al 24-sep-2026, con `herramientas/datos_historicos.yahoo_historia`. Índices de precio.
39. Fidelity vía Motley Fool (8-sep-2026): +37% promedio a un año desde el **mínimo** (1950-2022). Grado D como regla, porque el mínimo se conoce después. https://www.fool.com/investing/2026/09/08/if-stock-market-drops-history-says-this-happen/

**Capítulos y archivos enlazados:** 01, 02, 03, 04, 11, 13, 14, 15, 16, 17, 22, 23 y 24; `arena/investigacion/01` a `04`.

**No verificado:** la coautoría de Callahan en [1]; la magnitud de Heston-Sadka; el detalle de julio de 2026 más allá del titular; la cobertura de analistas de emisoras mexicanas en 2026; los artículos de la LMV sobre información privilegiada; la fecha del rebalanceo del S&P de diciembre de 2026.
