# Módulo 22 — Fuentes de datos y flujo de investigación asistido por IA

> Nivel: especialidad (doctorado aplicado en finanzas empíricas + mesa de research) · Actualizado: 2026-09-25 · Grado de evidencia global:
> - **A** en la mecánica de las fuentes: endpoints, plazos y rezagos verificados hoy contra la fuente oficial.
> - **B** en que el texto público contiene información de precios: Tetlock, Loughran-McDonald, Lazy Prices y llamadas de resultados.
> - **C** en convertir ese texto en alfa neto para una cuenta de 20 mil pesos en GBM.
> - **D** en usar un LLM como oráculo, o en backtests con un LLM dentro de su ventana de entrenamiento.

**Verificación.** Cada URL, endpoint y cifra se abrió el 25-sep-2026 con WebFetch, con la API de Crossref o con llamadas directas a los endpoints. El buscador web no estuvo disponible en esta sesión (se agotó su cuota). Lo que no se pudo abrir va marcado **(no verificado)**.

**Enlaces (no se repite aquí):**
- **Cap. 25:** caída de la literatura "el LLM le gana al analista", memorización y Look-Ahead-Bench (§2.2); `companyfacts`/`frames`, plazos de la CUE y XBRL `ifrsxbrl` (§6.7).
- **Cap. 15 R7:** Form 4, 13F y eventos relevantes. **Cap. 06, 07 y 20:** decaimiento, backtesting, DSR y PBO. **Cap. 04 y 16:** macro de EUA y del peso. **Cap. 23:** PRisk y GPR.
- **En redacción:** 08, 09, 11, 12 y 13. Este capítulo se limita a fuentes, flujo de trabajo y control de calidad.

---

## 1. Objetivos de dominio

Quien se titula en este módulo sabe:
1. **Dónde está la ventaja de una IA, y dónde no,** con 20 mil pesos, ejecución manual en GBM y 0.58% de comisión por vuelta: en la atención y la cobertura, no en la velocidad ni en datos privados.
2. **Extraer de EDGAR sin memoria del modelo** (filings con hora de aceptación, XBRL, texto completo, Form 4, 13F y datasets) con ≤ 10 solicitudes/s y User-Agent; y lo mismo para emisoras mexicanas en BMV, BIVA y CNBV.
3. **Montar la capa macro** con Banxico SIE, INEGI, FRED/ALFRED, calendarios y el COT, sabiendo cuándo se publica y cuándo se revisa cada dato. Usar French y Damodaran sabiendo que cambian.
4. **Cuantificar la evidencia** de texto, atención, llamadas, datos alternativos y COT, separando IS/OOS, pre/post publicación y bruto/neto.
5. **Explicar la evidencia 2023-2026 con LLMs:** qué muestra, qué se cayó y por qué los costos matan la señal de titulares para nosotros.
6. **Ejecutar** el flujo de una empresa en 60 minutos y el monitoreo macro diario, y **aplicar** los checklists anti-alucinación y anti look-ahead a cualquier agente, incluido este.

---

## 2. Núcleo teórico / marco

### 2.1 Cuatro ventajas posibles y cuál tiene una IA

| Ventaja | Qué es | Evidencia | ¿Es nuestra? |
|---|---|---|---|
| Informacional | Datos que otros no tienen (satélite, tarjetas, geolocalización) | Froot et al. (2017): una medida de ventas en tiempo real dentro del trimestre genera **3.4%** de retorno excedente promedio al anuncio [38]. Katona et al.: las imágenes satelitales dieron estrategias rentables a inversionistas sofisticados, sobre todo con malas noticias [40] | **No.** Cuestan y ya las tienen los fondos. **Inferencia:** lo que miden ya está en el precio el día del reporte |
| Velocidad | Actuar primero sobre información pública | Lopez-Lira y Tang: la estrategia de GPT-4 sobre titulares **deja de ser rentable a 20 pb por vuelta** [50] | **No.** GBM cobra 58 pb por vuelta más spread y el dueño ejecuta a mano |
| Atención y cobertura | Procesar lo público que nadie lee | Lazy Prices: los cambios en 10-K/10-Q predicen retornos **sin reacción al anuncio** [32]. Tetlock (2011): hay sobrerreacción a noticias viejas [25]. Da et al.: atención minorista [30] | **Sí**, en horizontes de semanas a meses. Una IA lee el 100% de los filings a costo marginal casi nulo |
| Control de calidad | No alucinar, no usar datos del futuro, no sobreoperar | FinanceBench: GPT-4-Turbo con recuperación falló o se negó en 81% (2023) [64]. El mejor agente de 2026 acierta 64.37% [65] | **Sí**. No da alfa por sí solo, pero evita pérdidas. **Inferencia:** con capital igual entre IAs, la que no se equivoca de dato gana en términos relativos |

**Inferencia (marco Grossman-Stiglitz, AER 1980; cita no verificada en esta sesión).** La información costosa rinde en equilibrio apenas lo que cuesta. El LLM abarata leer para todos y comprime esa renta: el Sharpe anual de la estrategia de GPT-4 bajó de **6.54** (4T-2021) a **3.68** (2022), **2.33** (2023) y **1.22** (ene-may 2024) [50]. Queda ventaja en lo **lento y tedioso**: comparar el 10-K con el del año anterior, leer la sesión de preguntas, cruzar Form 4 con eventos y verificar cada cifra.

### 2.2 Jerarquía de fuentes

| Nivel | Tipo | Ejemplos | Uso permitido |
|---|---|---|---|
| 1 | Documento primario del emisor o regulador, con hora de publicación | EDGAR, BMV/BIVA/CNBV, Banxico, INEGI, BLS, BEA | Cualquier cifra que entre a una decisión |
| 2 | Agregador oficial con vintages o datasets documentados | FRED/ALFRED, datasets de la SEC, CFTC PRE | Series y paneles; vintage explícito |
| 3 | Bases académicas mantenidas | Kenneth French, Damodaran, diccionario Loughran-McDonald | Factores, primas y múltiplos de referencia, congelando la versión |
| 4 | Proveedor comercial o no documentado | Yahoo, transcripciones de terceros | Precios de trabajo y texto de llamadas. Toda cifra clave se confirma en el nivel 1 |
| 5 | Prensa y redes | Medios, X, foros | Solo alertas. Nunca cifras |
| 6 | **Memoria del modelo** | Lo que "sabe" el LLM | **Prohibida como fuente de cifras o fechas** (cap. 25 §2.2: memorización) |

### 2.3 Los tres relojes de un dato (point-in-time)

Cada dato tiene tres fechas:
- **t_evento:** el periodo que describe.
- **t_publicación:** cuándo se pudo conocer. Por ejemplo, el `acceptanceDateTime` de EDGAR o la hora de difusión de INEGI.
- **t_descarga:** cuándo lo guardó el sistema.

Una decisión en t solo puede usar datos con t_publicación ≤ t, **en la versión vigente en t**.

**Dos ejemplos reales, verificados hoy:**
1. **Form 4 fuera de horario.** El JSON `submissions` de Apple muestra un Form 4 aceptado el `2026-09-24T22:30:07.000Z`. Eso es 18:30 ET, después del cierre, así que el primer precio ejecutable fue la apertura del 25-sep.
2. **`frames` con un valor posterior.** El frame `us-gaap/Revenues/USD/CY2025Q2` devuelve para Acme United un valor con número de acceso `0001193125-26-338211`, es decir, presentado en **2026** para un trimestre de 2025. La SEC documenta que `frames` toma "one fact for each reporting entity that is last filed" [1]. Un backtest que "sabía" ese número en agosto de 2025 usa un dato del futuro.

**Trampa adicional verificada.** En `companyconcept` de Apple, el concepto `Revenues` se detiene en 2018. Después la empresa reporta con `RevenueFromContractWithCustomerExcludingAssessedTax`, desde el 10-K presentado el 31-oct-2019 (último dato: 3T fiscal 2026, presentado el 31-jul-2026). Que falte el concepto no significa que falte el dato. Un LLM que "no lo encuentra" tiende a rellenarlo.

### 2.4 Texto como dato: cuatro generaciones

1. **Diccionarios.** Loughran-McDonald (2011) muestra que casi **tres cuartas partes** de las palabras "negativas" del Harvard Dictionary no son negativas en finanzas (10-K, 1994-2008) [27]. Es transparente, auditable y barato; sus trampas de implementación están en la encuesta de los mismos autores [28]. La versión vigente del diccionario es de **marzo de 2026** y cubre 1993-2025 [20].
2. **Ponderación y ML supervisado.**
   - Jegadeesh y Wu (2013): el esquema de ponderación importa tanto o más que la lista de palabras [29].
   - Ke, Kelly y Xiu (NBER 2019): puntaje supervisado sobre Dow Jones Newswires, explotable "net of transaction costs" con rotación razonable [46].
3. **Transformers de dominio.** FinBERT (Huang, Wang y Yang, CAR 2023) supera al diccionario LM y a otros algoritmos al clasificar sentimiento. Otros enfoques subestiman "por al menos 18%" la informatividad textual de las llamadas [47].
4. **LLM generativos (2023 en adelante).** Leen, extraen, clasifican sin entrenamiento y resumen. Traen riesgos nuevos: alucinación, memorización, efecto distracción y cronología débil (§4).

**Regla.** La generación nueva no jubila a la anterior. El diccionario LM es la **línea base barata**: si un LLM no le gana fuera de muestra y después de su fecha de corte, no se usa el LLM.

### 2.5 La ecuación de costos que filtra todo

Una señal pasa si: alfa bruto esperado − (0.58% de comisión por vuelta + spread + 10% de ISR sobre la ganancia en BMV, cap. 07) ≥ umbral. En la arena, `nota_rotacion` exige **movimiento esperado ≥ 5%**, con `operaciones_max_mes` = 8 y `orden_minima_mxn` = 5,000: caben como máximo 4 posiciones. Consecuencias:
- **Descartadas:** señales de 1-2 días (el drift post-titular de GPT-4 fue de **34 pb/día bruto** [50]).
- **Candidatas, primero como veto:** señales mensuales o trimestrales (cambio en el 10-K, tono de la sesión de preguntas, clústeres de insiders).

---

## 3. Literatura y fuentes canónicas

| Autor(es) · año · revista | Hallazgo cuantificado (verificado en el abstract o en el texto) | IS / OOS · pre / post | Enlace | Grado |
|---|---|---|---|---|
| Tetlock (2007), JF 62(3):1139-1168 | Alto pesimismo en la columna del WSJ predice presión bajista seguida de **reversión a fundamentales**; el pesimismo extremo predice volumen | IS; efecto transitorio | [23] | B |
| Tetlock, Saar-Tsechansky y Macskassy (2008), JF 63(3):1437-1467 | La fracción de palabras negativas en noticias de la empresa predice **utilidades bajas**. El precio subreacciona brevemente | IS | [24] | B |
| Tetlock (2011), RFS 24(5):1481-1512 | Las noticias "viejas" (similares a las 10 anteriores) mueven menos el precio, pero el retorno de ese día **predice negativamente** el de la semana siguiente. Es sobrerreacción minorista | IS | [25] | B |
| Engelberg y Parsons (2011), JF 66(1):67-97 | Los medios locales **causan** operación local tras resultados del S&P 500 | Causal | [26] | A (mecanismo) |
| Loughran y McDonald (2011), JF 66(1):35-65 | ~3/4 de las "negativas" de Harvard no lo son en finanzas; seis listas propias ligadas a retornos, volumen y fraude | IS 1994-2008 | [27] | A (medición) · C (alfa) |
| Da, Engelberg y Gao (2011), JF 66(5):1461-1499 | Russell 3000, 2004-2008: el SVI de Google sube → **precios más altos 2 semanas y reversión dentro del año**. Mide atención minorista | IS | [30] | C |
| Bijl et al. (2016), IRFA 45:150-156 | 2008-2013: el signo **se invierte** (búsquedas altas → retornos negativos). La estrategia **no es rentable con costos** | OOS temporal | [31] | C (contra) |
| Cohen, Malloy y Nguyen (2020), JF 75(3):1371-1415 | Vender "changers" y comprar "nonchangers" rinde hasta **188 pb/mes de alfa (>22%/año)**. Los cambios en el 10-K predicen utilidades y quiebras. **No hay efecto al anuncio** | IS | [32] | B |
| Sadlo (2021), SSRN (réplica) | S&P 1500, 1996-jun 2020: el quintil menos similar tiene alfa **de hasta −5.12%/año**. Es **asimétrico**: los changers pierden, pero los nonchangers no ganan. Persiste en el S&P 500 | Réplica independiente; muestra hasta jun-2020 | [33] | B |
| Price, Doran, Peterson y Bliss (2012), JBF 36(4):992-1011 | El tono de la llamada predice retornos anormales y volumen, y **domina a la sorpresa de utilidades en los 60 días hábiles siguientes**. La sesión de preguntas y respuestas explica el drift, sobre todo en empresas sin dividendo | IS | [34] | B/C |
| Matsumoto, Pronk y Roelofsen (2011), TAR 86(4) | Más de 10,000 transcripciones: la **sesión de preguntas y respuestas es más informativa** que la presentación, sobre todo con mal desempeño | IS | [35] | B |
| Mayew y Venkatachalam (2012), JF 67(1):1-43 | El afecto vocal de los directivos en las llamadas predice fundamentales. Los analistas no incorporan el afecto negativo | IS | [36] | C |
| Larcker y Zakolyukina (2012), JAR 50(2):495-540 | Modelos lingüísticos de engaño: **6-16% mejor que el azar** fuera de muestra. El portafolio de CFOs con más engaño tiene **alfa de −4% a −11% anual** | OOS en la clasificación | [37] | C |
| Froot, Kang, Ozik y Sadka (2017), JFE 125(1):143-162 | Ventas en tiempo real con unos 50 millones de dispositivos: **3.4%** de retorno excedente al anuncio | IS | [38] | B (contenido) · D (para nosotros) |
| Zhu (2019), RFS 32(5):2021-2061 | Los datos alternativos (transacciones y satélite) **aumentan la informatividad del precio** y reducen el trading oportunista de los directivos | Natural experiment | [39] | B |
| Katona, Painter, Patatoukas y Zeng (JFQA 60(2), en línea 2024) | Los satélites dieron estrategias rentables a los sofisticados, más ventas en corto informadas, peor timing minorista y **menos liquidez** en los reportes | Natural experiment | [40] | B |
| Mukherjee, Panayotov y Shon (2021), JFE 141(1):234-254 | Con algunas estimaciones satelitales (crudo en EUA, PMI de China), **el mercado ya no se sorprende** con el dato oficial (identificación por nubosidad) | Causal | [41] | B |
| Dessaint, Foucault y Frésard (2024), JF 79(3):2237-2287 | Los datos alternativos mejoran el pronóstico de **corto** plazo y **empeoran** el de largo plazo de los analistas (efecto horizonte) | Teoría + evidencia | [42] | B |
| Wang (2003), JFM 23(1):1-31 | En 15 futuros de EUA, las posiciones de especuladores se correlacionan positivamente con retornos anormales siguientes, pero **por presión de cobertura**, no por habilidad | IS | [43] | C |
| Kang, Rouwenhorst y Tang (2020), JF 75(1):377-417 | Commodities: los cambios de corto plazo (liquidez de no comerciales) y el nivel de largo plazo (cobertura de comerciales) predicen retornos **con signos opuestos** | IS | [44] | B |
| Tornell y Yuan (2012), JFM 32(2):122-151 | Divisas: los **picos y valles** de posiciones netas predicen el spot. Las demás medidas, poco. Especuladores → continuación; coberturistas → reversión | IS | [45] | C |
| McLean y Pontiff (2016), JF 71(1):5-32 | 97 predictores: **−26% fuera de muestra, −58% post-publicación** | OOS y post | [48] | A |
| Hou, Xue y Zhang (2020), RFS 33(5):2019-2133 | **65% de 452 anomalías** no pasan \|t\| ≥ 1.96 con cortes NYSE y ponderación por valor; con t ≥ 2.78, **82%** | Réplica | [49] | A |

**Lectura de la tabla.**
- **Texto y atención:** casi todo es B o C y está medido antes de 2012 o 2020. Aplicando el descuento de McLean-Pontiff (−58% post-publicación), un efecto de 188 pb/mes in-sample queda en una fracción. La réplica de Sadlo dice que sobrevive sobre todo **el lado corto** (changers). Nosotros solo vamos largos, así que Lazy Prices sirve como **veto**, no como generador de compras.
- **Datos alternativos:** su evidencia es A en que "contienen información" y D en que "un minorista gane con ellos".

---

## 4. Lo más reciente 2023-2026

### 4.1 LLMs que leen noticias y reportes

| Estudio | Qué encontró | Estado y lectura crítica | Enlace | Grado |
|---|---|---|---|---|
| Lopez-Lira y Tang, "Can ChatGPT Forecast Stock Price Movements?" (arXiv v6, 28-oct-2025) | Muestra oct-2021 a may-2024, **posterior al corte** de `gpt-4-0314` (sep-2021): 159,137 observaciones y 4,123 empresas. Acierto diario de portafolio de **93.3% (nocturno) y 88.8% (intradía)** en la reacción inicial, que **no es operable**. Drift: aciertos de 58%/55%, 34/50 pb diarios, **Sharpe 2.97/2.63 antes de costos**. Rotación de ~190%/día. A **5 pb** por vuelta la ganancia acumulada es >300%; a **10 pb**, >100%; a **20 pb, no es rentable**. El Sharpe cae de 6.54 a 1.22 conforme se adoptan los LLM. FinBERT: 90% en la reacción inicial, 48% en el drift (Sharpe −0.33) | Sobrevive en OOS de fecha de corte. Muere con costos minoristas | [50] | B (información) · **D para GBM** |
| Kirtac y Germano, FRL 62 (2024) | 965,375 noticias 2010-2023. Precisión: OPT 74.4%, BERT 72.5%, FinBERT 72.2%, LM 50.1%. Sharpe long-short: OPT **3.05**, LM 1.23 | **Inferencia:** la muestra termina en 2023 y OPT se publicó en 2022 (fecha no verificada en esta sesión), así que hay traslape con el entrenamiento. Sin corrección de look-ahead | [51] | C |
| Jha, Qian, Weber y Yang, "ChatGPT and Corporate Policies" (NBER w32161, feb-2024) | Un puntaje de inversión que ChatGPT extrae de las llamadas predice el capex **hasta 9 trimestres**. Los puntajes altos tienen **retornos anormales futuros negativos** | IS. Útil como **medición**, no como estrategia validada | [52] | B/C |
| de Kok, Management Science 71(9) (2025) | Detecta **no-respuestas** en llamadas con **96% de precisión** y baja 70% el error frente a Gow et al. (2021) | Validación de medición. El mejor uso documentado del LLM: clasificar texto con criterios explícitos | [53] | B |
| Kim, Muhn y Nikolaev, "Bloated Disclosures" (arXiv 2306.10224) | Afirmaba que los resúmenes de ChatGPT son más cortos y más informativos | **Retirado (v5, 9-oct-2025):** "A co-author attempted to independently replicate key results… the analyses did not yield results supporting the reported findings" | [54] | D |
| Kim, Muhn y Nikolaev, "From Transcripts to Insights" (arXiv 2310.17721, v2 19-mar-2025) | Medidas de riesgo político, climático y de IA a partir de llamadas | Sin retiro a la fecha. **Inferencia:** otros tres trabajos de estos autores (o de parte de ellos) están retirados o retractados (arriba y cap. 25), así que queda en D hasta una réplica independiente | [55] | D |

### 4.2 Look-ahead, memoria y cronología: el problema central de 2025-2026

- **Glasserman y Lin (2023).** Los titulares anonimizados **superan** a los que llevan nombre: el "efecto distracción" pesa más que el look-ahead in-sample, sobre todo en empresas grandes. Fuera de muestra el look-ahead deja de ser el problema; la distracción persiste [56].
- **Wu, Yang, Ying y Zhou (rev. 5-sep-2026).** Anonimizar **destruye información**: el texto crudo predice mejor las degradaciones de S&P, y la brecha no viene del look-ahead [60].
- **He, Lv, Manela y Wu (2025).** ChronoBERT/ChronoGPT, entrenados solo con texto disponible en cada fecha, logran en noticias → retorno del día siguiente un Sharpe comparable a un Llama mucho mayor: ahí el look-ahead es "modest" y depende de la aplicación [57].
- **Wongchamcharoen y Glasserman (nov-2025).** GPT-4.1, Claude 3.7 Sonnet y GPT-5 conservan el orden local pero **fallan en la línea de tiempo global** en secuencias largas; el razonamiento explícito lo corrige (GPT-5 con esfuerzo máximo: sin errores) [58].
- **Merchant y Levy (v2 23-sep-2026).** "Olvido" en inferencia ajustando logits con dos modelos chicos; sin réplica, C [59].
- **Li et al., "Profit Mirage" (oct-2025).** La ventaja de los agentes con LLM **se desvanece al terminar su ventana de conocimiento** [61].
- **Kong et al. (feb-2026).** En 164 papers 2023-2025, **ningún sesgo** (look-ahead, supervivencia, narrativa, objetivo, costo) **se discute en más del 28%** [62].
- **Gençay (27-ago-2026).** Con evaluación sin fuga por construcción y ajustada por intensidad de búsqueda (453 acciones y 39 ETFs, dos modelos de frontera, hasta 100 candidatos, 5 corridas) se **rechazan todas las estrategias descubiertas por LLM** y se certifican los pasivos; ni un "oráculo" con fuga y Sharpe 35 pasó [63]. Un solo estudio sin revisión (C), pero converge con [48][49][61][62].

### 4.3 Alucinación en tareas de analista

- **FinanceBench (Islam et al., arXiv 2311.11944, nov-2023).** GPT-4-Turbo con recuperación (RAG) **respondió mal o se negó en 81%** de 150 casos revisados a mano [64].
- **Vals AI, Finance Agent (v1.1, actualizado el 4-jun-2026).** 537 preguntas de analista junior, desde recuperación simple hasta proyecciones. El mejor, Claude Opus 4.7, obtuvo **64.37%**. Los modelos rinden mejor en recuperación simple [65]. **Inferencia:** incluso el mejor agente falla una de cada tres tareas de analista. Toda cifra necesita trazabilidad.
- **Magesh et al., JELS 22(2) (2025).** Herramientas legales comerciales con RAG que se anunciaban "sin alucinaciones" alucinaron **17-33%** [66]. Con LLM generales en preguntas legales, **≥58%** (Dahl et al., JLA 2024) [67]. Es otro dominio, pero el mecanismo es el mismo: el RAG reduce la alucinación y no la elimina.

### 4.4 Cambios en fuentes

- **Google Trends API** en alfa, con acceso por solicitud: 5 años móviles, datos "consistently scaled" que se pueden unir entre consultas. La interfaz pública sigue siendo una **muestra** normalizada de 0 a 100 [19].
- **French** reconstruye toda su historia cada mes ("Historical returns can change, for example, if CRSP revises its database") [16]. **Damodaran** publica una vez al año (9-ene-2026) [17]. **Loughran-McDonald** tiene versión de marzo de 2026 [20]. Detalle y uso en §6.1.

---

## 5. Evidencia real: qué funciona, qué no, magnitudes

| Señal o fuente | Qué funciona | Magnitud documentada | Qué no funciona o decayó | Uso en este sistema | Grado |
|---|---|---|---|---|---|
| Datos primarios (EDGAR, BMV, Banxico, INEGI) | Exactitud, fecha de publicación y trazabilidad | — | Nada. El riesgo es de proceso (look-ahead, etiquetas) | Base obligatoria | A |
| Tono de noticias (Tetlock, LM) | El pesimismo predice presión y utilidades bajas | Transitorio, de días | Se revierte y dura días; con 58 pb por vuelta no alcanza | Contexto de riesgo; nunca gatillo | B / D operable |
| Titulares con LLM | Clasifica la reacción inicial (93%) y parte del drift | Drift de 34 pb/día bruto; Sharpe 2.97 → 1.22 | **No rentable a 20 pb** por vuelta [50] | Descartado para operar; útil para triage de noticias | D operable |
| Lazy Prices (cambio en 10-K/10-Q) | Changers pierden en el futuro, sin efecto al anuncio | 188 pb/mes IS [32]; −5.12%/año en réplica [33] | El lado largo (nonchangers) no gana en la réplica | **Veto**: ninguna compra nueva en el quintil de menor similitud sin explicar el cambio | B |
| Atención (Google Trends) | Mide atención minorista | +2 semanas y reversión (2004-2008) | Signo invertido y no rentable neto (2008-2013) [31] | Termómetro de euforia; nunca señal de compra | C |
| Llamadas: sesión de preguntas y respuestas, tono y no-respuestas | La sesión de preguntas informa más; el tono predice el drift a 60 días; las no-respuestas se detectan al 96% | Alfa del "engaño" de −4% a −11% anual [37] | Evidencia vieja (pre-2012) y probablemente decaída; la voz exige audio | Bandera de riesgo en la ficha; veto si hay no-respuestas en el tema central de la tesis | B/C |
| Datos alternativos (satélite, tarjetas) | Anticipan ventas y utilidades | 3.4% al anuncio [38] | Su valor al anuncio se comprime (el mercado ya no se sorprende [41]) | No accesibles. **Inferencia:** evitar apuestas binarias al reporte; quien tiene los datos ya jugó | B / D operable |
| Horizonte largo | Los analistas descuidan el largo plazo cuando abundan datos de corto [42] | Cualitativa | — | **Inferencia:** nuestra ventaja relativa está en tesis de 3-12 meses | B |
| COT (CFTC) | Los extremos de posición en divisas predicen el spot; en commodities, la cobertura da prima | Signos opuestos por componente [44] | Rezago de 3 días (martes → viernes); cobertura de 70-90% del interés abierto | Contexto para el peso (posicionamiento extremo = riesgo de reversión) | C |
| 13F | Contexto de consenso de largo plazo | — | Hasta 45 días de rezago tras el trimestre, sin cortos [6] | Solo contexto (cap. 15 R7) | C |
| Form 4 (compras P en clúster) | Cap. 15 | Cap. 15 | Ruido en ventas y en planes 10b5-1 | Filtro de papel (cap. 15) | B/C |
| LLM como extractor con verificación | Acelera la lectura; clasifica con criterios explícitos | 96% en no-respuestas [53] | Falla 1 de cada 3 tareas de analista [65] | Sí, con el checklist §6.4 | B |
| LLM como oráculo (pronostica o elige acciones) | — | — | La literatura insignia está retirada o retractada (cap. 25); se desvanece post-corte [61]; la evaluación honesta lo rechaza [63] | **Prohibido** | D |

**Cinco números para memorizar:**
- 58 pb por vuelta en GBM contra los **20 pb** que ya matan la señal de titulares (2.9×) [50].
- −58% de rendimiento post-publicación [48].
- 82% de las anomalías fallan con t ≥ 2.78 [49].
- 64% de aciertos del mejor agente en 2026 [65].
- Ningún sesgo se discute en más del 28% de los papers de LLM en finanzas [62].

---

## 6. Traducción operable

### 6.1 Mapa de fuentes: URL exacta, qué da, rezago y trampa

**Estados Unidos (SEC).**

| Fuente | URL o endpoint (verificado el 25-sep-2026) | Qué da | Rezago | Trampa |
|---|---|---|---|---|
| Historial de filings | `https://data.sec.gov/submissions/CIK##########.json` (CIK de 10 dígitos) | Forma, `filingDate`, **`acceptanceDateTime`**, `items` del 8-K, `isXBRL` | < 1 s [1] | Usar `acceptanceDateTime`, no `filingDate`, para el point-in-time |
| Hechos XBRL | `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` y `.../companyconcept/CIK##########/us-gaap/<Concepto>.json` | `val`, `start`, `end`, **`accn`**, `fy`, `fp`, `form`, **`filed`**, `frame` | < 1 min [1] | Las etiquetas cambian (Apple `Revenues` → otra etiqueta en 2018). Filtrar `filed ≤ t` |
| Corte transversal | `https://data.sec.gov/api/xbrl/frames/us-gaap/<Concepto>/USD/CY2025Q2.json` (`CY####`, `CY####Q#`, `CY####Q#I`) | Un hecho por entidad, el **último presentado** | < 1 min | Incluye cifras reexpresadas posteriores → look-ahead (§2.3) |
| Masivos | `companyfacts.zip` y `submissions.zip` | Todo EDGAR XBRL e historial | Nocturno, ~3:00 a.m. ET [1] | — |
| Texto completo | Interfaz `https://www.sec.gov/edgar/search/` · JSON `https://efts.sec.gov/LATEST/search-index?q="going concern"&forms=10-K&dateRange=custom&startdt=2026-09-01&enddt=2026-09-24` | Filings **y anexos desde 2001**. Admite frase exacta, NOT, OR, NEAR y comodín final `*`. No admite lenguaje natural [3] | Casi inmediato | Prueba de hoy: 45 resultados. El endpoint JSON no está documentado como API oficial: tratarlo como frágil |
| Últimos filings [9] | `https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent` · RSS XBRL `https://www.sec.gov/Archives/edgar/usgaap.rss.xml` | Flujo en vivo | Minutos | EDGAR acepta de 6:00 a 22:00 ET en días hábiles [2] |
| Índices | `/Archives/edgar/daily-index/` y `/Archives/edgar/full-index/` | Índices por día y por trimestre | Nocturno, ~22:00 ET [2] | — |
| Form 3/4/5 | Por emisora vía `submissions`. Dataset: `https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets` | Transacciones de insiders | Form 4 en **2 días hábiles** [7]. Dataset trimestral, ene-2006 a jun-2026 [4] | Ventas en planes 10b5-1 = ruido (cap. 15) |
| 13F | Dataset: `https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets` | Posiciones largas en valores 13(f) de gestores con ≥ US$100 millones | Hasta **45 días** tras el trimestre; tratamiento confidencial de hasta 1 año [6]. Dataset de jul-2013 a ago-2026 [5] | Sin cortos ni opciones vendidas; foto vieja |
| Estados masivos | `https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets` | Estados XBRL aplanados, ene-2009 a jun-2026 | Trimestral [8] | — |
| Reglas de acceso | `https://www.sec.gov/os/accessing-edgar-data` | **≤ 10 solicitudes/s**; User-Agent "Empresa correo@dominio" | — | Sin llave ni CORS [1][2] |

**México.**

| Fuente | URL o endpoint | Qué da | Rezago | Trampa |
|---|---|---|---|---|
| BMV: información de emisoras [10] | `https://www.bmv.com.mx/es/emisoras/informacion-de-emisoras`. Patrones por emisora vistos en el propio sitio: `.../es/emisoras/eventosrelevantes/<CLAVE>-<id>-CGEN_CAPIT` (p. ej. `BOLSA-7029-CGEN_CAPIT`) e `.../es/emisoras/informacionfinanciera/<CLAVE>-<id>-CGEN_CAPIT` | Eventos relevantes, información periódica, XBRL | Plazos de la CUE: cap. 25 §6.7 | **Emisnet** (`emisnet.bmv.com.mx`) es el portal de envío de las emisoras, con login. El público lee en bmv.com.mx |
| BMV XBRL [10] | `https://www.bmv.com.mx/es/empresas-listadas/informacion-financiera-xbrl` | Archivos `ifrsxbrl` (cap. 25) | Con el reporte trimestral | El comunicado de RI sale antes que el XBRL |
| BIVA [11] | `https://www.biva.mx/` (secciones de emisoras: eventos relevantes, banco de información) | Lo mismo para emisoras de BIVA | — | Es una aplicación JS. Las rutas internas `/emisoras/eventos-relevantes` y `/emisoras/banco-informacion/rss` se observaron en el código del portal, **no documentadas como API**. Las emisoras envían por DIV (`div.biva.mx`) |
| CNBV / STIV | `https://www.gob.mx/cnbv` | Regulación y consulta de emisoras | — | Consulta STIV **(no verificado: falló TLS)** |
| Banxico SIE [12] | Portal `https://www.banxico.org.mx/SieInternet/`. API `https://www.banxico.org.mx/SieAPIRest/service/v1/series/<id>/datos/oportuno` | Series oficiales | Diario | **Requiere token**: la API responde "Token inválido" y remite a `/SieAPIRest/service/v1/token`. Nombre del encabezado `Bmx-Token` **(no verificado)** |
| Series Banxico (verificadas en los cuadros CF101, CF102 y CF107) | `SF61745` tasa objetivo · `SF331451` TIIE de fondeo a un día · `SF43783` TIIE 28 · `SF43718` FIX (fecha de determinación) · `SF60653` FIX (fecha de liquidación) · `SF43936` rendimiento en subasta desde 1982 (CETES 28; el plazo se **infiere** del orden del cuadro y de la fecha inicial) · `SF43939` desde 1978 (CETES 91, inferido) | — | — | Para CETES 28 no usar el proxy mensual del FMI salvo que falle Banxico (hoy `herramientas/` lo usa por falta de token) |
| Banxico: encuestas y decisiones [13] | `https://www.banxico.org.mx/publicaciones-y-prensa/encuestas-sobre-las-expectativas-de-los-especialis/encuestas-expectativas-del-se.html` · `.../anuncios-de-las-decisiones-de-politica-monetaria/anuncios-politica-monetaria-t.html` | Expectativas del sector privado y comunicados | Según calendario | — |
| INEGI [14] | API `https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/<id>/es/00/false/BIE/2.0/<token>?type=json` · calendario `https://www.inegi.org.mx/app/saladeprensa/calendario/` | Indicadores BIE/BISE en JSON o XML | Según calendario | **Token** obligatorio. Los identificadores se buscan en el constructor de consultas; no se inventan |

**Macro global y bases académicas.**

| Fuente | URL o endpoint | Qué da | Rezago | Trampa |
|---|---|---|---|---|
| FRED / ALFRED | `https://fred.stlouisfed.org/docs/api/fred/` (`series/observations`, `release/dates`, `series/vintagedates`) · `https://alfred.stlouisfed.org/` · calendario `https://fred.stlouisfed.org/releases/calendar` | Series y **vintages**: `realtime_start` y `realtime_end` reconstruyen "lo que se sabía" en una fecha [15] | Según la fuente | La API pide llave. El CSV `fredgraph.csv` que usa `herramientas/` no, pero da la **última revisión** |
| Calendarios EUA [22] | BLS `https://www.bls.gov/schedule/news_release/` · BEA `https://www.bea.gov/news/schedule` · FOMC `https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm` · subastas `https://www.treasurydirect.gov/auctions/upcoming/` | Fechas de publicación | — | — |
| Kenneth French | `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html` | Factores FF3 y FF5, momentum, regiones | Mensual (hay datos hasta jul-2026) | **La historia cambia cada mes**: congelar con hash (`herramientas/huellas.py`) |
| Damodaran | `https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html` | ERP, costo de capital por industria, primas por país, márgenes y múltiplos | Anual (9-ene-2026) | Datos al 3T del año previo. Fecha de disponibilidad = fecha de publicación |
| CFTC COT | `https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm` · API PRE `https://publicreporting.cftc.gov/` | Legacy, Disaggregated, **TFF** (divisas, bonos del Tesoro, VIX) y Supplemental | Datos del **martes**, publicados el **viernes a las 15:30 ET** [18] | Clasificación autodeclarada; lo reportable es solo 70-90% del interés abierto [18] |
| Google Trends | `https://trends.google.com/trends/` · API alfa `https://developers.google.com/search/apis/trends` | Índice de atención 0-100 | Casi en tiempo real | **Muestra**: descargas distintas dan valores distintos. Horario UTC en rangos ≥ 30 días [19] |
| Loughran-McDonald | `https://sraf.nd.edu/loughranmcdonald-master-dictionary/` | Listas de sentimiento (negativo, positivo, incertidumbre, litigioso, modales fuertes y débiles, restrictivo) | Anual | Usar la versión congelada con fecha |
| Transcripciones [21] | `https://www.fool.com/earnings-call-transcripts/` (gratuitas para las empresas que cubre; p. ej. SNX, PAYX y CTAS del 24-sep-2026) · sitio de RI de la emisora | Texto de la llamada | Horas | Nivel 4: toda cifra citada se confirma en el comunicado o el 10-Q |

### 6.2 Flujo estándar: investigación de una empresa en 60 minutos

**Entrada:** ticker, fecha y hora de corte t (hora de CDMX y ET) y pregunta de decisión. Por ejemplo: "¿entra a la lista de vigilancia de la arena?".
**Salida:**
- ficha en `empresas/<TICKER>/` (skill `ficha-empresa`);
- 2 a 4 pronósticos registrados en `bitacora/pronosticos.csv`;
- veredicto: descartar, vigilar o pasar al comité.

| Min | Paso | Fuente exacta | Herramienta | Criterio de salida |
|---|---|---|---|---|
| 0-5 | **Congelar t y la pregunta.** Anotar qué descuenta el precio (cap. 03 y 25) antes de leer | — | `python3 herramientas/dossier.py TICKER --form4` (o `WALMEX.MX`; o `AMXB.MX --edgar-ticker AMX`) | Dossier generado. Fuentes con error listadas |
| 5-12 | **Inventario de filings**: último 10-K, 10-Q, 8-K Item 2.02 (EX-99.1), DEF 14A. En México: reporte trimestral, eventos relevantes y reporte anual | `data.sec.gov/submissions/CIK….json` (con `acceptanceDateTime`) · páginas de BMV/BIVA de la emisora | `edgar.presentaciones_recientes` | Lista con fecha, hora de aceptación y número de acceso. **Nada con aceptación > t** |
| 12-20 | **Números**: 10 años de ingresos, márgenes, FCF, SBC, dilución, deuda y vencimientos | `companyfacts` (filtro `filed ≤ t`) · `ifrsxbrl` BMV | `edgar.estados_financieros` · `modelo_integrado.py` | Cuadres: activos = pasivos + capital; segmentos = total; Q4 = FY − 9M |
| 20-30 | **Lectura dirigida con LLM**, sección por sección, con cita obligatoria: Item 1A (riesgos), Item 7 (MD&A), notas de deuda, segmentos, arrendamientos y contingencias | HTML del 10-K/10-Q en `Archives/edgar/data/<cik>/<accn>/` | LLM como **extractor**, con respuestas que citen sección y párrafo | Tabla hecho → cita textual → ubicación. Toda cifra reconciliada con XBRL (tolerancia 0.5%) |
| 30-36 | **Lazy Prices**: comparar Item 1A y MD&A contra el filing equivalente previo (similitud y diff de párrafos nuevos o borrados) | Los dos HTML | Diff de texto (coseno o Jaccard) + LLM que **solo describe** los párrafos cambiados | Similitud en percentil bajo del universo → bandera; si no se explica → **veto de compra** |
| 36-44 | **Llamada de resultados**: presentación contra preguntas y respuestas. Cambios de guía, no-respuestas (de Kok), proporción de palabras negativas y de incertidumbre LM contra la llamada anterior | Transcripción (Fool o RI) · comunicado 8-K | Diccionario LM + LLM clasificador con criterio explícito | Lista de no-respuestas en temas de la tesis. Cambio de tono medido, no "sentido" |
| 44-50 | **Dueños e insiders**: Form 4 (compras P en clúster; cap. 15), 13F como contexto y eventos relevantes (recompras, cambios de directivos) | `submissions` + XML del Form 4 · dataset 13F · BMV/BIVA | `edgar.transacciones_form4` | Resumen de 3 líneas. Sin 13F como gatillo |
| 50-55 | **Valuación de cordura**: DCF inverso, múltiplos contra la industria y ERP | `dossier.py` (DCF inverso) · Damodaran (ene-2026) | — | Crecimiento implícito contra el histórico y la guía. Rango, no punto |
| 55-58 | **Equipo rojo**: un segundo agente, solo con los documentos primarios, busca el error de cifra, el dato del futuro y la tesis contraria | Los mismos documentos | Checklist §6.4 y §6.5 | Muestra de ≥ 20% de las cifras verificada; todas las que sostienen la decisión |
| 58-60 | **Registrar**: veredicto y pronósticos con fecha y criterio de resolución | — | `python3 herramientas/pronosticos.py agregar ...` | Ninguna tesis sin pronóstico medible (Brier ≤ 0.20 en `pronosticos`) |

**Reglas del flujo:**
- Si a los 60 minutos faltan datos primarios, el veredicto es "vigilar", nunca "comprar".
- Emisoras del SIC con 10-K: se usa EDGAR. Emisoras BMV sin EDGAR: BMV/BIVA más el XBRL `ifrsxbrl`.
- En fase 0 el veredicto máximo es "pasar al comité en papel" (`prioridad_actual`).

### 6.3 Flujo diario de monitoreo macro

**Horario.** CDMX = ET − 2 h mientras EUA tiene horario de verano, y ET − 1 h en invierno. El dato de EUA de las 8:30 ET cae a las 6:30 o 7:30 en CDMX.

| Hora (CDMX) | Paso | Fuente | Salida |
|---|---|---|---|
| 06:00 | **Tablero de régimen**: tendencia, volatilidad, crédito, curva y dólar-peso | `python3 herramientas/tablero.py --salida bitacora/briefs/AAAA-MM-DD-tablero.md` (13 series de FRED + 8 de Yahoo) | RISK-ON / MIXTO / RISK-OFF. Series con "rezago" señaladas |
| 06:10 | **Calendario del día y de 5 días**: EUA, México y bancos centrales | FRED Release Calendar · BLS · BEA · FOMC · calendario INEGI · anuncios de Banxico · subastas del Tesoro | Lista de eventos que tocan posiciones o pronósticos abiertos |
| 06:20 | **México**: FIX, tasa objetivo, TIIE de fondeo, CETES 28 y la última encuesta de expectativas | Banxico SIE (`SF43718`, `SF61745`, `SF331451`, `SF43936`) · encuestas Banxico | Tabla de 4 números con fecha. Diferencial Banxico-Fed (cap. 16) |
| 06:30 / 07:30 | **Dato de EUA** si lo hay (IPC, empleo, PIB): dato contra consenso y revisión del dato previo | BLS/BEA (primario); FRED solo para la serie | Anotar también la revisión: el dato previo **cambió** |
| 07:00 | **Filings nocturnos** de posiciones y lista de vigilancia: 8-K, 4, SC 13D; eventos relevantes BMV/BIVA | `submissions` por CIK (aceptación > cierre anterior) · páginas BMV/BIVA | Una línea por evento: qué cambia en la tesis |
| Viernes 15:30 ET (13:30 o 14:30 CDMX) | **COT TFF**: peso mexicano, e-mini S&P y bonos del Tesoro. Percentil de 3 años de la posición neta de leveraged funds y asset managers | CFTC PRE | Bandera si está en un extremo (p < 5% o > 95%): riesgo de reversión (Tornell-Yuan) |
| Mensual | French (actualizar y congelar con hash) · encuesta Banxico · revisión de vintages ALFRED de las series del tablero | French · Banxico · ALFRED | Diferencias de versión registradas |
| Enero | Damodaran (ERP, primas por país, múltiplos) | Damodaran | Parámetros de valuación del año |

**Formato del brief (máximo 1 página):**
1. Régimen.
2. Tres cosas que cambiaron, con fuente y hora.
3. Eventos de los próximos 5 días.
4. Pronósticos registrados o resueltos hoy.
5. "Nada que hacer", que es la salida más frecuente.

**Regla:** ningún brief genera una orden. Solo se ejecuta lo que estaba en un plan previo y pasó por el comité (`comite-de-inversion`), dentro de `limites_perdida` y `operaciones_max_mes`.

### 6.4 Checklist anti-alucinación para agentes

Cada respuesta de un agente que contenga cifras pasa estas 14 verificaciones:
1. **Toda cifra tiene cuatro campos:** fuente de nivel 1-2, URL, ubicación (sección y párrafo, etiqueta XBRL + `accn`, o id de serie) y fecha de publicación. Sin los cuatro campos, la cifra no existe.
2. **Cero cifras de memoria.** Si el documento no la trae, se escribe "no está en la fuente" o "(no verificado)". El agente recibe la instrucción explícita de que "no encontrado" es una respuesta válida y preferida.
3. **Doble vía.** Cada número del texto se reconcilia con XBRL, y viceversa, con tolerancia de 0.5%. Si discrepa, se relee y se anota.
4. **Cuadres contables:** activos = pasivos + capital; segmentos = total; conciliación de caja; acciones diluidas contra básicas.
5. **Unidades:** miles contra millones; MXN contra USD; ADR ratio; año fiscal contra calendario; datos por acción ajustados por split.
6. **Citas textuales:** la cita se busca literalmente (grep) en el documento. Si no aparece, se borra.
7. **Etiquetas cambiantes.** Si falta un concepto XBRL, se buscan sus sinónimos (p. ej. `Revenues` contra `RevenueFromContractWithCustomerExcludingAssessedTax`) antes de concluir que falta el dato.
8. **Estado del paper.** Antes de citar evidencia, se revisan los comentarios de arXiv, el `update-to` de Crossref y avisos de retracción. Los retirados o retractados son D (cap. 25; §4.1).
9. **Enlaces abiertos en la sesión.** Si el sitio da 403, se marca; no se "reconstruye" su contenido.
10. **Hecho, "Inferencia:" y opinión** en frases separadas.
11. **Reproducibilidad:**
    - prompts versionados;
    - temperatura baja;
    - insumos guardados con SHA-256 (`herramientas/huellas.py`);
    - la misma extracción, repetida, debe dar lo mismo.
12. **Segundo agente independiente** (equipo rojo) con los mismos documentos, sin ver la respuesta del primero, para las cifras que sostienen la decisión.
13. **Pregunta trampa de control.** En cada lote se pide un dato que **no** está en el documento. Si el agente lo "encuentra", el lote se invalida.
14. **Umbral de confianza.** Ninguna decisión se apoya en una cifra extraída por LLM sin el paso 3. La base es el 64% del mejor agente [65].

### 6.5 Checklist anti look-ahead

1. **t fija y escrita** antes de descargar nada. Todo dato con t_publicación ≤ t: `acceptanceDateTime` (EDGAR), `filed` (XBRL), vintage (ALFRED), hora de difusión (INEGI/Banxico).
2. **Macro con vintages.** En backtests se usa ALFRED (`realtime_start`/`realtime_end`); nunca la serie revisada de hoy.
3. **`frames` y `companyfacts`** traen reexpresiones posteriores (§2.3). Para backtest se filtra por `filed ≤ t` y por `accn` original.
4. **Rezagos legales:** Form 4 = 2 días hábiles; 13F ≤ 45 días; COT del martes al viernes; reporte trimestral BMV = 20 días hábiles (40 en el 4T, cap. 25). La señal empieza **después** de la publicación.
5. **Precio ejecutable:** un filing aceptado después de las 16:00 ET (14:00 CDMX en verano de EUA, 15:00 en invierno) se opera a la apertura siguiente. En la arena, el dueño ejecuta a mano: se suma al menos 1 día de retraso realista.
6. **Precios ajustados:** se recalculan hacia atrás con cada dividendo o split. Las señales se calculan con precios de la fecha y eventos corporativos conocidos en t.
7. **Universo point-in-time:** miembros del IPC, S&P o SIC en t, incluidos los deslistados (sesgo de supervivencia).
8. **Bases que se reescriben:** French cada mes y Damodaran cada año. Se congelan con hash y fecha de descarga; nunca se mezclan versiones.
9. **LLM y fecha de corte:**
   - todo backtest con LLM se hace **solo después** del corte de entrenamiento del modelo, o con modelos cronológicamente consistentes [57];
   - antes del corte, el resultado es D por definición [61];
   - anonimizar ayuda contra la distracción, pero **pierde información** [56][60].
10. **Prueba de memoria:** se pregunta al modelo por el desenlace futuro de un evento anterior a su corte (retorno del mes siguiente, dato publicado después). Si acierta más que el azar, la tarea está contaminada (cap. 25).
11. **Cronología:** en tareas de ordenar eventos, se exige razonamiento explícito y se verifica con fechas de documento [58].
12. **Pre-registro:** la hipótesis, la métrica y los parámetros se escriben antes de ver resultados. Se cuentan **todos** los intentos para el DSR (`deflated_sharpe_min_probabilidad` 0.95, `pbo_max` 0.25) [63].
13. **Costos reales:** 0.58% por vuelta + spread + ISR. Si con esos costos la estrategia no sobrevive, no existe (Lopez-Lira y Tang a 20 pb [50]).
14. **Nuestros pronósticos** se registran con marca de tiempo **antes** del desenlace. Es la única evaluación del sistema libre de look-ahead por construcción.

### 6.6 Reglas de uso y parámetros (coherentes con `config/parametros.json`)

- **R1. Rol del LLM:** lector, extractor, clasificador con criterio explícito y equipo rojo. **Nunca** oráculo de precios ni de utilidades.
- **R2. Señales de texto = vetos o filtros.** Ninguna señal textual, de atención, COT o 13F abre una posición por sí sola. Para ser gatillo tendría que cumplir `validacion_estrategias`: ≥ 10 años, costos incluidos, DSR ≥ 0.95, PBO ≤ 0.25 y 3 meses / 30 operaciones en papel.
- **R3. Vetos activos desde hoy (en papel, fase 0):**
  1. Similitud del 10-K/10-Q en el quintil más bajo del universo seguido sin explicación → no hay compra nueva.
  2. No-respuesta en la sesión de preguntas sobre el motor central de la tesis → no hay compra nueva hasta el siguiente reporte.
  3. Cifra clave sin verificación doble → no hay decisión.
- **R4. Horizonte:** tesis de 3 a 12 meses con movimiento esperado ≥ 5% (`nota_rotacion`). Se descartan titulares, drifts de 1-2 días y apuestas binarias al reporte cuando el sector está cubierto por datos alternativos [41].
- **R5. Presupuesto:** ≤ 8 operaciones al mes y como máximo 4 posiciones (orden mínima de 5,000 sobre 20,000): el cuello de botella es la **calidad** de 4 tesis, no la cantidad de ideas. Criterio: ≤ 10 flujos de 60 minutos por semana.
- **R6. Pronósticos:** cada ficha deja 2 a 4 pronósticos con criterio verificable en fuente de nivel 1. Brier objetivo ≤ 0.20 con ≥ 50 pronósticos (`pronosticos`).
- **R7. Fuentes caídas:** si falla el nivel 1, se degrada a "vigilar". Una fuente de nivel 4-5 no sustituye a una de nivel 1.
- **R8. Torneo.** Las IAs rivales tienen el mismo capital y, probablemente, las mismas fuentes públicas. **Inferencia:** la diferencia sostenible es cometer menos errores de dato y de fecha y cuidar los costos.

---

## 7. Trampas y errores comunes

Las trampas de fecha y de extracción ya están en los checklists (§6.4 y §6.5). Aquí van las de juicio y las que más se repiten:

1. **Pedirle cifras al modelo.** Es la fuente de nivel 6. Aunque acierte, no hay forma de saber cuándo alucina (81% de fallas de GPT-4-Turbo con RAG en 2023 [64]).
2. **Backtest con `frames` o `companyfacts` sin filtrar `filed`**, o con la serie macro revisada de hoy en vez del vintage de ALFRED: resultados que no se podían conocer en su momento.
3. **Concluir que "no hay dato"** porque cambió la etiqueta XBRL (Apple `Revenues`).
4. **French sin congelar:** el mismo backtest da otro número el mes siguiente porque la historia se reconstruyó [16].
5. **Operar el titular:** ignorar que 20 pb ya matan la señal [50] y que GBM cuesta 58 pb más spread.
6. **Creer el Sharpe de un paper con LLM** cuya muestra se traslapa con el entrenamiento [51] o cuyo resultado fue retirado [54].
7. **Anonimizar y dar el problema por resuelto:** se pierde información [60] y la distracción persiste [56].
8. **Señales lentas usadas como gatillo:**
   - Google Trends: el signo se invirtió fuera de muestra, no paga costos y la interfaz es una muestra que cambia entre descargas [19][31].
   - 13F: foto de hasta 45 días y sin cortos [6].
   - COT: dato del martes publicado el viernes, con 70-90% del interés abierto y clasificación autodeclarada [18].
9. **Lazy Prices del lado largo:** en la réplica, los nonchangers no ganan [33]. Es un veto, no una compra.
10. **Leer solo la presentación de la llamada:** la sesión de preguntas y respuestas es la que informa [35]. Además, una transcripción de terceros es nivel 4 y sus cifras se confirman en el comunicado.
11. **Confundir Emisnet con el sitio de consulta:** Emisnet es el portal de envío de las emisoras; el público lee en bmv.com.mx.
12. **Inventar identificadores de series** de INEGI o Banxico. Se buscan en el cuadro o el constructor, se verifican y se anotan.

---

## 8. Examen de titulación

1. **¿Por qué la señal de titulares de GPT-4 (Sharpe 2.97) no sirve en la arena?** Es antes de costos, con rotación de ~190%/día; a 20 pb por vuelta ya no es rentable y GBM cuesta 58 pb más spread con ejecución manual. Además el Sharpe cayó de 6.54 a 1.22 al difundirse los LLM [50].
2. **¿Qué campo da la hora exacta en que un filing se hizo público?** `acceptanceDateTime` en `data.sec.gov/submissions/CIK##########.json`. Define el primer precio ejecutable (Form 4 de Apple a las 18:30 ET → apertura siguiente).
3. **¿Qué trampa tiene `frames`?** Da el hecho **último presentado**, que puede venir de un filing posterior (Acme: 2T-2025 con `accn` de 2026). Filtrar `filed ≤ t`.
4. **Límites de EDGAR.** ≤ 10 solicitudes/s, User-Agent con nombre y correo, sin llave ni CORS; `submissions` < 1 s, XBRL < 1 min, zips cada noche ~3:00 a.m. ET [1][2].
5. **Loughran-McDonald (2011) y su uso hoy.** ~3/4 de las "negativas" de Harvard no lo son en 10-K; hoy es la línea base auditable (versión mar-2026) que un LLM debe superar fuera de muestra [27][20].
6. **Da-Engelberg-Gao contra Bijl et al.** 2004-2008: alza 2 semanas y reversión; 2008-2013: signo inverso y no rentable neto. Termómetro de atención, no estrategia (C) [30][31].
7. **Lazy Prices: magnitud, réplica y uso.** Hasta 188 pb/mes IS sin efecto al anuncio; réplica S&P 1500: −5.12%/año en changers, nonchangers sin ganancia. Uso: veto de compra [32][33].
8. **¿Qué parte de la llamada informa más y qué se mide validadamente con LLM?** La sesión de preguntas y respuestas; con LLM, las no-respuestas (96%, de Kok) [35][53].
9. **¿Por qué los datos alternativos no son nuestra ventaja?** Los tienen los sofisticados, el mercado ya no se sorprende con el dato oficial cuando el satélite lo ve, y cuestan. Inferencia: evitar apuestas binarias al reporte y buscar horizonte largo [40][41][42].
10. **COT: fecha, publicación y evidencia.** Martes → viernes 15:30 ET, 70-90% del interés abierto; en divisas los extremos predicen el spot; en commodities, primas de cobertura y liquidez con signo opuesto. Grado C [18][44][45].
11. **Series Banxico de FIX, tasa objetivo y TIIE de fondeo, y requisito de la API.** `SF43718`, `SF61745`, `SF331451`; token obligatorio (`/SieAPIRest/service/v1/token`).
12. **¿Cómo evitas el look-ahead macro?** Con ALFRED (`realtime_start`/`realtime_end`): el vintage vigente en t, no la serie revisada [15].
13. **¿Qué dicen Glasserman-Lin y Wu et al. sobre anonimizar?** Quita la distracción del nombre, pero pierde información real. No es gratis [56][60].
14. **Sesgos en papers de LLM y evaluación honesta.** Ningún sesgo en más del 28% de 164 papers; la evaluación sin fuga rechazó todas las estrategias de LLM [62][63].
15. **Regla mínima para usar una cifra extraída por LLM.** Fuente nivel 1-2 con URL, ubicación y fecha; reconciliación con XBRL (0.5%); cita literal verificable; segundo agente en las cifras decisivas. El mejor agente de 2026 acierta 64% [65].

---

## 9. Fuentes

1. SEC — EDGAR Application Programming Interfaces: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
2. SEC — Accessing EDGAR Data (10 solicitudes/s, User-Agent, horario, índices): https://www.sec.gov/os/accessing-edgar-data
3. SEC — EDGAR Full-Text Search FAQ: https://www.sec.gov/edgar/search/efts-faq.html · interfaz: https://www.sec.gov/edgar/search/ · endpoint probado: https://efts.sec.gov/LATEST/search-index?q=%22going%20concern%22&forms=10-K&dateRange=custom&startdt=2026-09-01&enddt=2026-09-24
4. SEC — Insider Transactions Data Sets: https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets
5. SEC — Form 13F Data Sets: https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets
6. SEC — Frequently Asked Questions About Form 13F: https://www.sec.gov/rules-regulations/staff-guidance/division-investment-management-frequently-asked-questions/frequently-asked-questions-about-form-13f
7. SEC — Forms 3, 4, 5 (Form 4 en dos días hábiles): https://www.sec.gov/files/forms-3-4-5.pdf
8. SEC — Financial Statement Data Sets: https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets
9. SEC — Latest filings: https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent · RSS XBRL: https://www.sec.gov/Archives/edgar/usgaap.rss.xml · submissions (ejemplo): https://data.sec.gov/submissions/CIK0000320193.json · frames (ejemplo): https://data.sec.gov/api/xbrl/frames/us-gaap/Revenues/USD/CY2025Q2.json
10. BMV — Información de emisoras: https://www.bmv.com.mx/es/emisoras/informacion-de-emisoras · XBRL: https://www.bmv.com.mx/es/empresas-listadas/informacion-financiera-xbrl · eventos relevantes (ejemplo): https://www.bmv.com.mx/es/emisoras/eventosrelevantes/BOLSA-7029-CGEN_CAPIT · Emisnet: https://emisnet.bmv.com.mx
11. BIVA: https://www.biva.mx/ · CNBV: https://www.gob.mx/cnbv
12. Banxico SIE: https://www.banxico.org.mx/SieInternet/ · API: https://www.banxico.org.mx/SieAPIRest/service/v1/ · cuadros: CF101 https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=18&accion=consultarCuadro&idCuadro=CF101&locale=es ; CF102 https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=6&accion=consultarCuadro&idCuadro=CF102&locale=es ; CF107 https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=22&accion=consultarCuadro&idCuadro=CF107&locale=es
13. Banxico — Encuestas de expectativas: https://www.banxico.org.mx/publicaciones-y-prensa/encuestas-sobre-las-expectativas-de-los-especialis/encuestas-expectativas-del-se.html · Anuncios de política monetaria: https://www.banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/anuncios-politica-monetaria-t.html
14. INEGI — API de indicadores: https://www.inegi.org.mx/servicios/api_indicadores.html · calendario: https://www.inegi.org.mx/app/saladeprensa/calendario/
15. FRED — API: https://fred.stlouisfed.org/docs/api/fred/ · periodos real-time: https://fred.stlouisfed.org/docs/api/fred/realtime_period.html · ALFRED: https://alfred.stlouisfed.org/ · calendario: https://fred.stlouisfed.org/releases/calendar
16. Kenneth R. French — Data Library: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
17. Damodaran — Current data: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html
18. CFTC — Commitments of Traders: https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm · Notas explicativas: https://www.cftc.gov/MarketReports/CommitmentsofTraders/ExplanatoryNotes/index.htm · PRE: https://publicreporting.cftc.gov/
19. Google Trends — API (alfa): https://developers.google.com/search/apis/trends · FAQ de datos: https://support.google.com/trends/answer/4365533
20. Loughran-McDonald Master Dictionary (SRAF, Notre Dame): https://sraf.nd.edu/loughranmcdonald-master-dictionary/
21. The Motley Fool — Earnings call transcripts: https://www.fool.com/earnings-call-transcripts/
22. Calendarios: BLS https://www.bls.gov/schedule/news_release/ · BEA https://www.bea.gov/news/schedule · FOMC https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm · TreasuryDirect https://www.treasurydirect.gov/auctions/upcoming/
23. Tetlock, P. (2007). Giving Content to Investor Sentiment. *JF* 62(3):1139-1168. https://doi.org/10.1111/j.1540-6261.2007.01232.x
24. Tetlock, P., Saar-Tsechansky, M., Macskassy, S. (2008). More Than Words. *JF* 63(3):1437-1467. https://doi.org/10.1111/j.1540-6261.2008.01362.x
25. Tetlock, P. (2011). All the News That's Fit to Reprint. *RFS* 24(5):1481-1512. https://doi.org/10.1093/rfs/hhq141
26. Engelberg, J., Parsons, C. (2011). The Causal Impact of Media in Financial Markets. *JF* 66(1):67-97. https://doi.org/10.1111/j.1540-6261.2010.01626.x
27. Loughran, T., McDonald, B. (2011). When Is a Liability Not a Liability? *JF* 66(1):35-65. https://doi.org/10.1111/j.1540-6261.2010.01625.x
28. Loughran, T., McDonald, B. (2016). Textual Analysis in Accounting and Finance: A Survey. *JAR* 54(4):1187-1230. https://doi.org/10.1111/1475-679X.12123
29. Jegadeesh, N., Wu, D. (2013). Word Power. *JFE* 110(3):712-729. https://doi.org/10.1016/j.jfineco.2013.08.018
30. Da, Z., Engelberg, J., Gao, P. (2011). In Search of Attention. *JF* 66(5):1461-1499. https://doi.org/10.1111/j.1540-6261.2011.01679.x
31. Bijl, L., Kringhaug, G., Molnár, P., Sandvik, E. (2016). Google Searches and Stock Returns. *IRFA* 45:150-156. https://doi.org/10.1016/j.irfa.2016.03.015 · resumen: https://ideas.repec.org/a/eee/finana/v45y2016icp150-156.html
32. Cohen, L., Malloy, C., Nguyen, Q. (2020). Lazy Prices. *JF* 75(3):1371-1415. https://doi.org/10.1111/jofi.12885
33. Sadlo, A. (2021). Copy-Paste Outperformance: Lazy Investors and Copied Reports (SSRN). https://doi.org/10.2139/ssrn.3748216
34. Price, S. M., Doran, J., Peterson, D., Bliss, B. (2012). Earnings Conference Calls and Stock Returns. *JBF* 36(4):992-1011. https://doi.org/10.1016/j.jbankfin.2011.10.013 · resumen: https://ideas.repec.org/a/eee/jbfina/v36y2012i4p992-1011.html
35. Matsumoto, D., Pronk, M., Roelofsen, E. (2011). What Makes Conference Calls Useful? *TAR* 86(4):1383-1414. https://doi.org/10.2308/accr-10034
36. Mayew, W., Venkatachalam, M. (2012). The Power of Voice. *JF* 67(1):1-43. https://doi.org/10.1111/j.1540-6261.2011.01705.x
37. Larcker, D., Zakolyukina, A. (2012). Detecting Deceptive Discussions in Conference Calls. *JAR* 50(2):495-540. https://doi.org/10.1111/j.1475-679X.2012.00450.x
38. Froot, K., Kang, N., Ozik, G., Sadka, R. (2017). What Do Measures of Real-Time Corporate Sales Say About Earnings Surprises and Post-Announcement Returns? *JFE* 125(1):143-162. https://doi.org/10.1016/j.jfineco.2017.04.008 · NBER: https://www.nber.org/papers/w22366
39. Zhu, C. (2019). Big Data as a Governance Mechanism. *RFS* 32(5):2021-2061. https://doi.org/10.1093/rfs/hhy081
40. Katona, Z., Painter, M., Patatoukas, P., Zeng, J. On the Capital Market Consequences of Big Data: Evidence from Outer Space. *JFQA* 60(2):551-579. https://doi.org/10.1017/S0022109023001448
41. Mukherjee, A., Panayotov, G., Shon, J. (2021). Eye in the Sky: Private Satellites and Government Macro Data. *JFE* 141(1):234-254. https://doi.org/10.1016/j.jfineco.2021.03.002 · resumen: https://ideas.repec.org/a/eee/jfinec/v141y2021i1p234-254.html
42. Dessaint, O., Foucault, T., Frésard, L. (2024). Does Alternative Data Improve Financial Forecasting? The Horizon Effect. *JF* 79(3):2237-2287. https://doi.org/10.1111/jofi.13323
43. Wang, C. (2003). The Behavior and Performance of Major Types of Futures Traders. *JFM* 23(1):1-31. https://doi.org/10.1002/fut.10056
44. Kang, W., Rouwenhorst, K. G., Tang, K. (2020). A Tale of Two Premiums. *JF* 75(1):377-417. https://doi.org/10.1111/jofi.12845
45. Tornell, A., Yuan, C. (2012). Speculation and Hedging in the Currency Futures Markets. *JFM* 32(2):122-151. https://doi.org/10.1002/fut.20511
46. Ke, Z. T., Kelly, B., Xiu, D. (2019). Predicting Returns with Text Data. NBER w26186. https://www.nber.org/papers/w26186
47. Huang, A., Wang, H., Yang, Y. (2023). FinBERT. *CAR* 40(2):806-841. https://doi.org/10.1111/1911-3846.12832
48. McLean, R. D., Pontiff, J. (2016). Does Academic Research Destroy Stock Return Predictability? *JF* 71(1):5-32. https://doi.org/10.1111/jofi.12365
49. Hou, K., Xue, C., Zhang, L. (2020). Replicating Anomalies. *RFS* 33(5):2019-2133. https://doi.org/10.1093/rfs/hhy131
50. Lopez-Lira, A., Tang, Y. Can ChatGPT Forecast Stock Price Movements? arXiv 2304.07619 (v6, 28-oct-2025). https://arxiv.org/abs/2304.07619
51. Kirtac, K., Germano, G. (2024). Sentiment Trading with Large Language Models. *FRL* 62:105227. https://doi.org/10.1016/j.frl.2024.105227 · https://arxiv.org/abs/2412.19245
52. Jha, M., Qian, J., Weber, M., Yang, B. (2024). ChatGPT and Corporate Policies. NBER w32161. https://www.nber.org/papers/w32161
53. de Kok, T. (2025). ChatGPT for Textual Analysis? *Management Science* 71(9):7888-7906. https://doi.org/10.1287/mnsc.2023.03253
54. Kim, A., Muhn, M., Nikolaev, V. Bloated Disclosures (arXiv 2306.10224; retirado en v5, 9-oct-2025). https://arxiv.org/abs/2306.10224
55. Kim, A., Muhn, M., Nikolaev, V. From Transcripts to Insights (arXiv 2310.17721, v2 19-mar-2025). https://arxiv.org/abs/2310.17721
56. Glasserman, P., Lin, C. (2023). Assessing Look-Ahead Bias in Stock Return Predictions Generated by GPT Sentiment Analysis. arXiv 2309.17322. https://arxiv.org/abs/2309.17322
57. He, S., Lv, L., Manela, A., Wu, J. (2025). Chronologically Consistent Large Language Models. arXiv 2502.21206. https://arxiv.org/abs/2502.21206
58. Wongchamcharoen, P. K., Glasserman, P. (2025). Do Large Language Models (LLMs) Understand Chronology? arXiv 2511.14214. https://arxiv.org/abs/2511.14214
59. Merchant, H., Levy, B. (2025-2026). A Fast and Effective Solution to the Problem of Look-ahead Bias in LLMs. arXiv 2512.06607. https://arxiv.org/abs/2512.06607
60. Wu, K., Yang, B., Ying, Z., Zhou, D. (2025-2026). Anonymization and Information Loss. arXiv 2511.15364. https://arxiv.org/abs/2511.15364
61. Li, X., Zeng, Y., Xing, X., Xu, J., Xu, X. (2025). Profit Mirage: Revisiting Information Leakage in LLM-based Financial Agents. arXiv 2510.07920. https://arxiv.org/abs/2510.07920
62. Kong, Y., Lee, H., et al. (2026). Evaluating LLMs in Finance Requires Explicit Bias Consideration. arXiv 2602.14233. https://arxiv.org/abs/2602.14233
63. Gençay, E. (2026). What Survives Honest Evaluation? arXiv 2608.27734. https://arxiv.org/abs/2608.27734
64. Islam, P., et al. (2023). FinanceBench. arXiv 2311.11944. https://arxiv.org/abs/2311.11944
65. Vals AI — Finance Agent Benchmark (v1.1, actualizado el 4-jun-2026). https://www.vals.ai/benchmarks/finance_agent
66. Magesh, V., et al. (2025). Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools. *JELS* 22(2):216-242. https://doi.org/10.1111/jels.12413
67. Dahl, M., Magesh, V., Suzgun, M., Ho, D. (2024). Large Legal Fictions. *JLA* 16(1):64-93. https://doi.org/10.1093/jla/laae003
