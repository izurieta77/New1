# Módulo 09 — Frontera: machine learning, LLMs y agentes de IA en inversión

> Nivel: frontera · Actualizado: 2026-09-25 · Grado de evidencia global: **C**. El ML en sección cruzada tiene poder predictivo bruto fuera de muestra, replicado (B). Pero neto de costos, después de publicarse y fuera de microcaps pierde más de la mitad. Predecir precios de corto plazo con un LLM sin datos exclusivos es **D**: hay memorización, el Sharpe decae año con año y en las competencias con dinero real casi todos los modelos pierden. Usar el LLM para procesar texto, dar cobertura y auditar sí está respaldado (B), pero como herramienta, no como fuente de alfa.

---

## 1. Objetivos de dominio (qué debe saber hacer quien "se titula" en este módulo)

1. Plantear la predicción de rendimientos como aprendizaje supervisado, E_t[r_{i,t+1}] = g(z_{i,t}). Calcular R²_OOS contra un pronóstico de cero y traducirlo a Sharpe (Campbell-Thompson).
2. Explicar por qué árboles y redes le ganan a OLS en Gu-Kelly-Xiu (interacciones no lineales) y por qué esa ventaja **bruta** se concentra en acciones difíciles de arbitrar (Avramov-Cheng-Metzker).
3. Reproducir el debate de la "complejidad virtuosa": qué prueban Kelly-Malamud-Zhou, qué demuestra Nagel (RFF con P ≫ T = momentum cronometrado por volatilidad) y qué queda en pie.
4. Distinguir tres enfoques: predecir rendimientos (GKX), estimar el SDF (Chen-Pelger-Zhu) y optimizar pesos netos de costos (Jensen-Kelly-Malamud-Pedersen).
5. Cuantificar el sesgo de look-ahead y la memorización en LLMs. Aplicar las pruebas disponibles: anonimización (Glasserman-Lin), recuerdo con solo la fecha (Gao-Jiang-Yan), modelos point-in-time (ChronoGPT, Look-Ahead-Bench).
6. Leer con escepticismo un paper de agentes LLM (TradingAgents, FinMem, FinAgent, FinCon): ventana de prueba, número de activos, fecha de corte del modelo, costos, benchmark pasivo.
7. Conocer con cifras exactas los resultados de las competencias reales entre IAs con dinero (Alpha Arena T1 y T1.5, Prediction Arena 2026) y sacar las lecciones de comportamiento: sobretrading, apalancamiento, direccionalidad, sensibilidad al prompt.
8. Evaluar los ETFs "gestionados por IA" contra el S&P 500: rendimiento, beta, tracking error, t-stat del alfa.
9. Explicar los mecanismos de crowding y de decaimiento del alfa cuando muchos agentes usan los mismos modelos y datos.
10. Separar las ventajas reales de un inversionista asistido por IA de las falsas.
11. Aplicar el protocolo anti look-ahead de la sección 6.4 a cualquier estrategia que proponga o evalúe una IA, incluido este sistema.

---

## 2. Núcleo teórico

### 2.1 El problema de predicción y sus métricas

- Modelo: r_{i,t+1} = E_t[r_{i,t+1}] + ε_{i,t+1}, con E_t[r_{i,t+1}] = g*(z_{i,t}). Aquí z son características de la empresa (GKX usa 94), interacciones con variables macro y dummies de industria: más de 900 señales base [1].
- **R²_OOS contra cero:** R²_OOS = 1 − Σ(r − r̂)² / Σ r². GKX lo mide contra un pronóstico de cero, no contra la media histórica, porque "la media histórica de una acción es tan ruidosa que baja artificialmente el R²" [1]. Un R²_OOS mensual de 0.4% por acción es alto en esta disciplina.
- **De R² a Sharpe (timing de mercado, Campbell-Thompson):** SR* = √[(SR² + R²)/(1 − R²)]. Ejemplo: SR mensual de comprar y mantener = 0.51/√12 = 0.147. Con R² mensual de 1%, SR* ≈ 0.179 mensual, 0.62 anual. Un R² diminuto mueve mucho el Sharpe porque el ruido domina.
- **Relación señal/ruido baja, datos escasos, no estacionariedad y un mercado adversario.** Son las cuatro razones por las que el ML en finanzas no se parece al de visión o lenguaje (Israel-Kelly-Moskowitz, "Can Machines 'Learn' Finance?", 2020 [29]). La cuarta es la más importante: si una señal funciona, otros la arbitran y desaparece.

### 2.2 Herramientas y por qué funcionan (o no)

- **Regularización.** Ridge (penalización L2), lasso (L1), elastic net, PCR/PLS (reducción de dimensión), árboles con boosting o random forest (interacciones), redes feed-forward (NN1-NN5).
- Los hiperparámetros se eligen con una ventana de validación, y el modelo se re-estima con ventanas crecientes o móviles.
- En GKX, las redes y los árboles ganan porque capturan **interacciones no lineales**. Todos los métodos coinciden en las señales dominantes: variantes de momentum, liquidez y volatilidad [1].
- **Turnover:** las carteras de ML rotan 110-130% al mes; un spread de reversión de corto plazo rota 172.6% y uno de tamaño, 22.9% [1]. *Inferencia:* el ML redescubre sobre todo señales de precio de alta rotación, justo las que más castigan los costos.

### 2.3 Complejidad, "double descent" y la crítica de Nagel

- **Tesis de Kelly-Malamud-Zhou (KMZ, JF 2024).** En regresión ridge con P parámetros y T observaciones, cuando c = P/T > 1 (régimen "sobreparametrizado"), el R² y el Sharpe fuera de muestra pueden **subir** con la complejidad. Empíricamente usan Random Fourier Features (RFF): hasta P = 12,000 transformaciones no lineales de K = 15 predictores (14 de Goyal-Welch más el rendimiento rezagado del índice), con ventanas de T = 12 meses [2][3].
- **Mecánica que expone Nagel (NBER w34104, ago-2025).** Cuando P ≫ T, la regresión *ridgeless* equivale a un promedio ponderado por kernel de los T rendimientos del entrenamiento: r̂_{t+1} = Σ_s w_s(z_t, z_s)·r_{s+1}. La similitud entre z_t y z_s depende sobre todo de la cercanía en el tiempo (los predictores son persistentes) y cae cuando sube la volatilidad de los predictores. El resultado es **momentum cronometrado por volatilidad**, aunque ese efecto no exista en los datos [3].
- **La prueba decisiva de Nagel.** Crea rendimientos artificiales con reversión (un MA(2) negativo) y el método RFF construye la misma estrategia de momentum, que ahí pierde. El modelo no aprendió nada del entrenamiento; es un artefacto mecánico [3].
- **Magnitudes (Nagel, Tabla I).**

  | Estrategia | Alfa anual vs mercado | t | IR |
  |---|---|---|---|
  | RFF de alta complejidad (KMZ) | 3.4% | 2.42 | 0.255 |
  | Momentum cronometrado por volatilidad (regla simple) | 3.4% | 3.68 | 0.388 |
  | RFF controlando por esa regla | 1.2% | 0.95 | 0.100 |

  Con T = 12 y P = 12,000, y bajo el proceso generador calibrado del propio KMZ, el Sharpe teórico alcanzable es de 0.017 anual. KMZ reportan empíricamente ~0.30 [3].
- **Otras críticas** (según la revisión de Nagel): Berk (2023) señala que los Sharpe de KMZ promedian 1,000 sorteos de pesos aleatorios, así que ninguna estrategia individual los alcanza [4]. Cartea-Jin-Shi (2025) y Fallahgoul (2025) ponen cotas al aprendizaje *(citados vía Nagel; no verificados directamente)*.
- **Buncic (2025) — corregido y precisado (adenda 2026-09-25, examen diagnóstico S3-10), verificado contra el resumen de SSRN y la nota de prensa de Stockholm Business School (25-sep-2025):** los resultados empíricos de la "virtud de la complejidad" de KMZ son consecuencia de **dos decisiones de implementación**, no de la complejidad en sí: (1) una **restricción de intercepto cero** impuesta a los modelos de pronóstico, y (2) un **esquema de agregación poco convencional** para construir las métricas de desempeño de los modelos de ML, ambas de las cuales empeoran artificialmente el desempeño de los modelos simples. Un modelo lineal simple de ventana expansiva con encogimiento leve logra un Sharpe de **0.699**, significativamente mayor que el **0.485** del modelo más complejo preferido por KMZ [5]. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5239006
- **La réplica de Kelly-Malamud**, "Understanding the Virtue of Complexity" (documento de trabajo; fecha no verificada), sostiene que las críticas "tienen poco peso" sobre los argumentos teóricos [6].
- *Inferencia:* la teoría del double descent es correcta. Lo que no está demostrado es que la evidencia empírica de timing de mercado venga de la complejidad y no de una regla simple conocida. **Para el sistema:** si un modelo complejo le gana al benchmark, primero hay que ver si una regla de 2 líneas lo replica.

> **Adenda fechada 2026-09-25 (examen diagnóstico S7-02, ficha `conocimiento/fichas/2026-09-25-examen-S7-complejidad-y-0dte.md`).** Verificación de cifras exactas de KMZ y de sus críticas de 2025, con lectura íntegra de los PDF cuando fue posible (`pypdf` sobre el texto extraído; sin `poppler-utils` disponible en el entorno).
> - **KMZ (JF 79(1):459-503), diseño y resultado principal — confirmado con cita textual (lectura íntegra):** "Over the standard Center for Research in Security Prices (CRSP) sample from 1926 to 2020, out-of-sample market timing Sharpe ratio improvements (relative to market buy-and-hold) reach roughly **0.47 per annum with t-statistics near 3.0**." Insumos: **15** predictores estándar de Goyal-Welch (2008); RFF hasta **P = 12,000**; ventanas rodantes **T = 12, 60 y 120** meses (nota 42 de KMZ: Sharpe base de 0.47/0.42/0.41 para T=12/60/120 antes de imponer la restricción de no negatividad de Campbell-Thompson, que lo sube a 0.54/0.50/0.49). El R²oos es "substantially negative for the vast majority of models" — la mejora de Sharpe convive con R² muy negativo, que es justo el punto de partida de la crítica de Nagel. Divestment correcto antes de 14 de 15 recesiones NBER de la muestra de prueba.
> - **GKX, inflación del R² con benchmark de media histórica — confirmado con cita textual y número de nota exacto (lectura íntegra del NBER WP 25398, sección previa a la nota 24 y nota al pie 34):** "there is a roughly 3% inflation in out-of-sample R2s if performance is benchmarked against historical averages. For OLS-3, the R2 relative to the historical mean forecast is **3.74%** per month!"
> - **Buncic (2025), SSRN 5239006, "Simplified: A Closer Look at the Virtue of Complexity in Return Prediction" (Stockholm University) — confirmado por dos vías, PDF bloqueado (SSRN devolvió HTTP 403 dos veces):** (i) el propio texto de Nagel (leído íntegro) cita el mecanismo: "Buncic (2025) shows that the increasing relation between out-of-sample performance and complexity disappears when RFF-based return forecasts are first aggregated across different draws of RFF weights before computing the OOS performance measures"; (ii) el comunicado de prensa de Stockholm Business School (25-sep-2025, `su.se`) cita al autor: una regresión lineal expandida con contracción leve logra Sharpe **0.699** frente a **0.485** del modelo más complejo preferido por KMZ, y atribuye la brecha a dos decisiones de diseño de KMZ (restricción de intercepto cero y el esquema de agregación). **Nivel de acceso real: no es lectura íntegra del PDF de Buncic**, es una combinación de la cita de Nagel (íntegra) y un comunicado institucional que reproduce al autor entre comillas.
> - **Elmore, R., Strauss, J. (2025), "Is Complexity Virtuous?", *Economics Letters* 258:112749, DOI 10.1016/j.econlet.2025.112749 — confirmado a nivel de resumen (abstract completo leído en DigitalCommons de University of Denver, no el cuerpo del artículo):** "the past twelve-month moving average of actual returns is **97.5%** correlated to the forecasts from a twelve-month rolling window of random Fourier features with a large penalty." **Corrección a la nota [5] existente en este capítulo:** Elmore-Strauss **no** son citados dentro del paper de Nagel (se buscó "Elmore" y "Strauss" en el texto íntegro de w34104 y no hay coincidencias); son una crítica publicada de forma independiente, no una referencia de Nagel a un tercero.
> - **Kelly y Malamud (2025), "Understanding the Virtue of Complexity" — la referencia [6] de este capítulo decía "documento de trabajo; fecha no verificada". Ahora verificado vía la bibliografía de Nagel (lectura íntegra):** "Kelly, Bryan T, and Semyon Malamud, 2025, 'Understanding The Virtue of Complexity,' Working paper, **Yale University**." Nagel también reporta su argumento central: para P bajo, el método de agregación de Buncic construye en realidad un ensamble de modelos simples, que es a su vez un modelo complejo — la disputa metodológica entre Buncic y Kelly-Malamud sigue sin resolverse en la literatura.
> - **No verificado en esta pasada:** la fecha/versión exacta de Buncic más allá de "2025"; si la cifra de 97.5% de Elmore-Strauss es robusta a distintas ventanas T (solo se leyó el resumen).

### 2.4 Estimar el SDF en vez de predecir rendimientos

- **Chen-Pelger-Zhu (MS 2024)** imponen la condición de no arbitraje E[M_{t+1} R^e_{i,t+1} g(I_t)] = 0. Con una red adversaria (GAN), buscan los activos de prueba más difíciles de valuar e incorporan 178 series macro y 46 características (1967-2016).
- Sharpe anual fuera de muestra del portafolio SDF: **2.6**. El caso lineal logra 1.7, la red que predice rendimientos 1.5 y FF5 0.8 [7].
- La cifra **cae a 1.4 con las 1,500 acciones más grandes y a 0.9 con las 550 más grandes**. Sin el 40% más pequeño, queda en 1.73 (cota inferior, sin re-estimar) [7].
- *Inferencia:* incluso el mejor modelo de SDF pierde dos tercios del Sharpe al pasar a acciones grandes, que son las que un minorista puede operar a bajo costo.

### 2.5 Costos dentro del objetivo

- **Jensen-Kelly-Malamud-Pedersen (RFS 39(10), 2026)** proponen evaluar estrategias por su rendimiento **neto** para cada nivel de riesgo: la "frontera eficiente implementable".
- El ML que ignora costos se apoya en "características efímeras de pequeña escala" y logra malos rendimientos netos. Aprender directamente los pesos con un objetivo económico que incluye costos domina [8].
- Formalmente: max_w E[w'r] − (γ/2)·w'Σw − TC(w − w_{t−1}).
- *Inferencia para GBM:* con 0.58% por vuelta completa (comisión 0.25% + IVA por lado) más spread, cualquier señal de horizonte diario queda fuera antes de empezar.

### 2.6 Texto como dato: de bolsa de palabras a LLMs

- **Tres generaciones:** (a) diccionarios y bolsa de palabras; (b) embeddings de palabras; (c) representaciones contextuales de LLMs.
- **Chen-Kelly-Xiu** (documento de trabajo, versión de feb-2026) muestran que (c) supera a (a)-(b), sobre todo con negaciones. Cubren 16 mercados y noticias en 13 idiomas. La información de las noticias se incorpora a los precios "con un retraso ineficiente" compatible con límites al arbitraje, y una estrategia con alertas frescas tiene Sharpe aún mayor [9][10]. *(Las cifras de Sharpe del paper no se verificaron: SSRN dio 403.)*
- **LLM como lector (Lopez-Lira-Tang).** GPT-4 califica titulares posteriores a su fecha de corte. La reacción inicial, no operable, se acierta ~90% a nivel portafolio-día. El drift del día siguiente se acierta 58% (noticias nocturnas) y 55% (intradía) [11].

### 2.7 Look-ahead y memorización: por qué un backtest con LLM suele estar mal identificado

- **No identificación.** Si el modelo vio el valor realizado, cualquier salida es compatible con habilidad o con memoria. Lopez-Lira-Tang-Zhu documentan recuerdo de valores exactos antes del corte. Instruir al modelo para que "no use el futuro" no lo evita. Enmascarar tampoco, porque reconstruye entidad y fecha con poco contexto. Después del corte no hay recuerdo [12].
- **Dos sesgos distintos (Glasserman-Lin).** El *look-ahead* es que el modelo conozca el rendimiento posterior. La *distracción* es que el conocimiento general de la empresa contamine la lectura del sentimiento. Dentro de muestra, los titulares anonimizados rinden **más**: domina la distracción, sobre todo en empresas grandes [13].
- **Pruebas formales.**
  - Sarkar-Vafa: pruebas directas con eventos impredecibles [14].
  - Gao-Jiang-Yan, "Lookahead Propensity" (LAP): se pregunta al modelo solo por la fecha. La LAP es positiva dentro de muestra y colapsa a ~0 justo después del corte. Si la interacción LAP × pronóstico es positiva en una regresión de precisión, hay contaminación [15].
- **Modelos point-in-time.**
  - ChronoBERT/ChronoGPT (He-Lv-Manela-Wu) se entrenan solo con texto disponible a cada fecha. Para rendimientos del día siguiente dan Sharpe comparables a Llama, así que en *esa* aplicación el sesgo es "modesto" [16].
  - Look-Ahead-Bench (ene-2026) encuentra sesgo significativo en Llama 3.1 y DeepSeek 3.2, medido como decaimiento del alfa, y no en modelos PiT [17].
  - En modelos de series de tiempo, Chen et al. (sep-2026) muestran que entrenar con datos posteriores al origen **no mejora** la precisión: sube el MSE en 18 de 20 combinaciones en EUA. Es una violación del conjunto de información, pero "no evidencia suficiente de precisión inflada" [18].

### 2.8 Agentes LLM y el problema estadístico de evaluarlos

- **Arquitectura típica** (TradingAgents, FinCon): analistas especializados (fundamental, sentimiento, técnico, noticias), debate "toro contra oso", trader, equipo de riesgo y memoria en capas (FinMem) [19][20][21][22].
- **Error estándar del Sharpe:** SE(SR_anual) ≈ √[(1 + SR²/2)/años]. Con SR ≈ 0:

  | Duración | SE del Sharpe anual |
  |---|---|
  | 17 días (Alpha Arena T1) | ≈ 4.6 |
  | 57 días (Prediction Arena) | ≈ 2.5 |
  | 3 meses | ≈ 2.0 |
  | 6 meses (temporada de la arena) | ≈ 1.4 |

  *Inferencia:* ninguna competencia entre IAs publicada hasta hoy tiene poder estadístico para separar habilidad de suerte. Lo que sí informa son los **patrones de comportamiento** que se repiten entre modelos y torneos.
- **Varianza por diseño.** Un agente LLM es modelo × prompt × herramientas × datos × semilla. Nof1 reporta alta sensibilidad a cambios mínimos del prompt [23]. Nagel-Tseng-Xiu (jul-2026) muestran que las probabilidades de un LLM responden al tono, a anclas, al orden de las etiquetas y a la exposición en el corpus, y no son "creencias" [24].

---

## 3. Literatura canónica

| Autores | Año | Título | Revista/Editorial | Hallazgo clave cuantificado | Enlace/DOI | Grado |
|---|---|---|---|---|---|---|
| Gu, Kelly, Xiu | 2020 | Empirical Asset Pricing via Machine Learning | RFS 33(5):2223-2273 | ~30,000 acciones, 1957-2016 (prueba 1987-2016). R²_OOS mensual 0.33-0.40% (NN). Long-short NN4 con Sharpe **1.35 VW / 2.45 EW** contra 0.61/0.83 de OLS; timing del S&P 0.77 contra 0.51. Todo **bruto**; turnover 110-130% al mes; max DD VW 51.8% | 10.1093/rfs/hhaa009 | B |
| Kelly, Malamud, Zhou | 2024 | The Virtue of Complexity in Return Prediction | JF 79(1):459-503 | Teoría: con P > T, lo complejo supera a lo simple. Timing con RFF: alfa 3.4%, IR 0.255 (réplica de Nagel) | 10.1111/jofi.13298 | C |
| Nagel | 2025 | Seemingly Virtuous Complexity in Return Prediction | NBER w34104 | RFF con P ≫ T = momentum cronometrado por volatilidad. Controlando por la regla simple, el alfa baja a 1.2% (t = 0.95) | 10.3386/w34104 | B (crítica) |
| Chen, Pelger, Zhu | 2024 | Deep Learning in Asset Pricing | MS 70(2):714-750 | SDF con GAN: SR 2.6 contra 1.7 (lineal) y 0.8 (FF5); 1.4 en las 1,500 mayores y 0.9 en las 550 mayores | 10.1287/mnsc.2023.4695 | B |
| Kelly, Xiu | 2023 | Financial Machine Learning | FnT in Finance 13(3-4):205-363 | Revisión de referencia del campo | 10.1561/0500000064 | A (referencia) |
| Jiang, Kelly, Xiu | 2023 | (Re-)Imag(in)ing Price Trends | JF 78(6):3193-3249 | CNN sobre imágenes de precio, 1993-2019. Semanal: SR hasta 7.2 EW (1.5 VW); trimestral: 1.3 EW / 0.5 VW, bruto. Los autores dicen que lo semanal no es "alcanzable en la práctica" | 10.1111/jofi.13268 | B (bruto) / D (minorista) |
| Avramov, Cheng, Metzker | 2023 | Machine Learning vs. Economic Restrictions | MS 69(5):2587-2619 | La rentabilidad del deep learning viene de acciones difíciles de arbitrar. Excluir microcaps, empresas en problemas o episodios de alta volatilidad la atenúa mucho; con costos razonables se deteriora | 10.1287/mnsc.2022.4449 | A (crítica) |
| Leippold, Wang, Zhou | 2022 | Machine Learning in the Chinese Stock Market | JFE 145(2):64-82 | En China la liquidez es el predictor #1. Mercado minorista: más predictibilidad de corto plazo en pequeñas; significativa neta de costos (versión de trabajo) | 10.1016/j.jfineco.2021.08.017 | B |
| Bryzgalova, Pelger, Zhu | 2025 | Forest Through the Trees | JF 80(5):2447-2506 | AP-Trees: carteras interpretables con hasta 3× el SR fuera de muestra de los sorts | 10.1111/jofi.13477 | B |
| Jensen, Kelly, Malamud, Pedersen | 2026 | Machine Learning and the Implementable Efficient Frontier | RFS 39(10):3035-3078 | El ML que ignora costos rinde mal neto; aprender pesos con costos domina | 10.1093/rfs/hhag022 | B |
| Chen, Velikov | 2023 | Zeroing In on the Expected Returns of Anomalies | JFQA 58(3):968-1004 | 204 anomalías: **4 pb al mes** netos de spreads, publicación y era moderna; las mejores, ≤10 pb; combinaciones ~20 pb | 10.1017/S0022109022000874 | A |
| Azevedo, Hoegner, Velikov | 2024 | The Expected Returns on Machine-Learning Strategies | SSRN 4702406 | Costos + decaimiento post-publicación + era de alta liquidez = **−57%**. LSTM: SR esperado 0.94 bruto / **0.84 neto** | 10.2139/ssrn.4702406 | B/C |
| Lopez-Lira, Tang | 2023-25 | Can ChatGPT Forecast Stock Price Movements? | arXiv 2304.07619 (v6, oct-2025) | GPT-4, oct-2021 a may-2024: long-short de drift de 34 pb/día y SR 2.97 **bruto**. Pierde a 20 pb por vuelta. SR 6.54 (4T21) → 3.68 (2022) → 2.33 (2023) → **1.22** (ene-may 2024) | arxiv.org/abs/2304.07619 | B (hecho) / D (para operar) |
| Chen, Kelly, Xiu | 2022-26 | Expected Returns and Large Language Models | SSRN 4416687 (WP feb-2026) | Embeddings de LLM superan a bolsa de palabras en 16 mercados y 13 idiomas; retraso ineficiente | papers.ssrn.com/…4416687 | C (cifras no verificadas) |
| Kim, Muhn, Nikolaev | 2024 | Financial Statement Analysis with LLMs | arXiv 2407.17866 | Afirmaba que GPT-4 supera a analistas. **Retirado el 20-feb-2025** por inconsistencias en datos | arxiv.org/abs/2407.17866 | D |
| Glasserman, Lin | 2023 | Assessing Look-Ahead Bias in Stock Return Predictions Generated by GPT Sentiment Analysis | arXiv 2309.17322 | Dentro de muestra, anonimizar mejora: la distracción pesa más que el look-ahead | arxiv.org/abs/2309.17322 | B |
| Lopez-Lira, Tang, Zhu | 2025 | The Memorization Problem | arXiv 2504.14765 | Recuerdo exacto antes del corte; ni instrucciones ni máscaras lo evitan; nulo después | arxiv.org/abs/2504.14765 | A (metodológico) |
| Zhang, Zhu, Linnainmaa | 2025 | Man versus Machine Learning Revisited | RFS 38(12):3768-3790 | El alfa de 1.54%/mes de van Binsbergen-Han-Lopez-Lira se explica por look-ahead: al quitarlo, **desaparece**; modelos lineales igual de precisos | 10.1093/rfs/hhaf066 | A |
| Li, Kim, Cucuringu, Ma (FINSABER) | 2025-26 | Can LLM-based Financial Investing Strategies Outperform the Market in Long Run? | KDD 2026 (D&B, oral) | En 20 años y más de 100 símbolos, la ventaja reportada de los LLM "se deteriora significativamente". Demasiado conservadores en alzas, demasiado agresivos en bajas | arxiv.org/abs/2505.07078 | B |
| Li, Zeng, Xing, Xu, Xu | 2025 | Profit Mirage | arXiv 2510.07920 | Después del corte de GPT-4o, el Sharpe de 5 agentes cae 51-62% y el rendimiento 50-72% | arxiv.org/abs/2510.07920 | B |
| Karger et al. | 2025 | ForecastBench | arXiv 2409.19839 (v5, feb-2025) | Los superpronosticadores superan al mejor LLM (p < 0.001) en preguntas sin respuesta conocida | arxiv.org/abs/2409.19839 | B |
| Cao, Jiang, Wang, Yang | 2024 | From Man vs. Machine to Man + Machine | JFE 160 | El analista IA le gana a la mayoría de humanos con información voluminosa; humano + IA reduce errores extremos | 10.3386/w28800 | B |

---

## 4. Lo más reciente 2023-2026 (con fecha)

**Debate de complejidad**
- dic-2023: KMZ en línea (JF 79(1), 2024) [2].
- 2023: comentario de Berk [4].
- 2025: Buncic [5].
- 11-ago-2025: Nagel, NBER w34104 [3].
- Réplica de Kelly-Malamud: documento de trabajo, fecha no verificada [6].
- Veredicto vigente: **C**, disputado.

**Retractaciones y correcciones (clave para un sistema de IA)**
- 20-feb-2025: se retira Kim-Muhn-Nikolaev [25].
- 29-abr-2026: retracción en *JAR* de Kim-Nikolaev, "Context-Based Interpretation of Financial Information" (DOI 10.1111/1475-679x.70057, confirmada en Crossref) [26].
- 1-mar-2026: *Expression of Concern* de la RFS sobre van Binsbergen-Han-Lopez-Lira, RFS 39(5):1555 [27].
- 2-sep-2025: se publica Zhang-Zhu-Linnainmaa (RFS 38(12)) [28].
- Lectura: tres de los resultados de "IA gana a analistas" más citados cayeron o están en duda en 18 meses.

**LLMs y rendimientos**
- oct-2025: Lopez-Lira-Tang v6, con el decaimiento del Sharpe conforme se adoptan los LLMs [11].
- feb-2026: versión de Chen-Kelly-Xiu [9].
- Documento de trabajo: Didisheim-Kelly-Pourmohammadi-Tian, "The Inefficient Pricing of News". Al quitarle a las noticias lo predecible por características, los "news shocks" duplican el poder predictivo mensual y predicen hasta 18 meses. Dicen que es mayor que cualquier anomalía del universo JKP [10]. *(Bruto; sin réplica independiente: C.)*

**Look-ahead**
- 2024: Sarkar-Vafa [14].
- feb-2025: ChronoGPT [16].
- abr/dic-2025: The Memorization Problem [12].
- dic-2025 / jun-2026: LAP de Gao-Jiang-Yan [15].
- ene-2026: Look-Ahead-Bench [17].
- "Scaling Point-in-Time Language Models", Kelly-Malamud-Schwab-Xu, listado como NeurIPS en el sitio de Kelly (año no verificado) [10].
- sep-2026: vintages de modelos de series de tiempo [18].

**Agentes y benchmarks**
- FinBen (feb-2024): 36 datasets y 24 tareas. Los LLM van bien en extracción de información y análisis textual, y mal en pronóstico [30].
- InvestorBench (dic-2024): 13 LLMs como base [31].
- StockBench (oct-2025, v2 mar-2026): 20 acciones del DJIA del 3-mar al 30-jun-2025. El mejor modelo gana **+2.5%** contra **+0.4%** del pasivo, con drawdowns de −11% a −15%. GPT-5 ganó +0.3%, por debajo del pasivo [32].
- Agent Market Arena (oct-2025): el marco del agente explica más variación que el modelo base [33].
- LiveTradeBench (nov-2025): 21 LLMs durante 50 días en vivo. "Puntajes altos de LMArena no implican mejores resultados de trading" [34].
- AI-Trader (dic-2025): "la mayoría de los agentes muestra rendimientos pobres y gestión de riesgo débil" [35].
- Gençay (27-ago-2026): con evaluación honesta (herramientas sin look-ahead por construcción y deflación por número de pruebas), **se rechaza toda estrategia descubierta por LLM**. Probó dos modelos de frontera, hasta 100 candidatos y 5 corridas, en 453 acciones point-in-time y 39 ETFs con costos. En cambio, los benchmarks pasivos sí se certifican. **Un oráculo con fuga deliberada y Sharpe de 35 pasa completo el DSR y el PBO** [36].

**Modelos fundacionales de series de tiempo**
- Noguer i Alonso-Franklin (jun-2026): TimesFM, Moirai, Chronos y TimeGPT en 5 acciones. Las ganancias contra la caminata aleatoria son "pequeñas y escasas". Diebold-Mariano solo rechaza en 2 de 10 tareas [37].

**Competencias con dinero real** (detalle en §5.3)
- Alpha Arena T1 (oct-nov 2025) y T1.5 (nov-dic 2025).
- Prediction Arena (12-ene a 9-mar-2026).
- Al 6-ago-2026 no había temporada 2 pública de Alpha Arena [38].

**Crowding, colusión y monocultivo**
- Lopez-Lira-Tang: el Sharpe del mismo prompt cae de 6.54 a 1.22 conforme se adoptan los LLMs [11].
- Dou-Goldstein-Ji (NBER w34054, jul-2025): especuladores con aprendizaje por refuerzo sostienen ganancias colusorias "sin acuerdo, comunicación ni intención" y reducen la eficiencia de precios (teoría y simulación) [39].
- Wang (SSRN 2026, teoría): con proveedores de IA compartidos se forma un "monocultivo": cae la dispersión y sube el error del consenso ("convergencia espuria") [40].
- Zhang-Zhou (SSRN 2026): experimento de herding con LLMs. Son más racionales que los humanos, pero cambiar rol o contexto mueve la conducta hasta 4% y 7.2% [41].
- FMI, *GFSR* oct-2024, cap. 3, sobre IA en mercados de capitales (solo verifiqué la existencia y el resumen) [42].

---

## 5. Evidencia real: qué funciona, qué no, magnitudes netas y decaimiento

### 5.1 ML en sección cruzada

| Resultado | Bruto | Neto / implementable | Post-publicación / grandes | Veredicto |
|---|---|---|---|---|
| GKX, long-short NN | SR 1.35 VW / 2.45 EW | Turnover 110-130% al mes; no reportan neto | EW sin el 20% inferior por tamaño: 1.69 | B |
| Chen-Pelger-Zhu, SDF | SR 2.6 | Sin el 40% más chico: 1.73 | 550 mayores: 0.9 | B |
| Avramov et al. | — | Se deteriora con costos razonables | Atenuado fuera de microcaps y en calma | A (crítica) |
| Azevedo et al., ML esperado | −57% acumulado | LSTM: SR 0.84 neto | Incluye decaimiento | B/C |
| Anomalías en general | — | 4 pb al mes | Chen-Velikov | A |
| JKX, imágenes | SR 7.2 EW semanal | "No alcanzable" (autores) | Transfiere a otros mercados | B/D |

*Inferencia:* el ML sí extrae información real. Lo que un minorista puede capturar, en large caps, long-only, con 0.58% por vuelta y rebalanceo mensual, está más cerca de un factor tilt de bajo turnover (momentum/calidad) que de los Sharpe de los papers.

### 5.2 LLMs como predictores

- **Lopez-Lira-Tang, lo más limpio que existe (post-corte):**
  - SR bruto de 2.97 en noticias nocturnas. Con 5 pb por vuelta, el acumulado pasa de ~700% a >300%; con 10 pb, >100%; con 20 pb, **no es rentable** [11].
  - El short pesa más: 26 pb/día y SR 2.01, contra 8 pb/día y SR 0.78 del long (nocturnas) [11].
  - **GBM cobra ~58 pb por vuelta más spread: 3-6× el punto de equilibrio.**
- **Decaimiento por adopción:** 6.54 → 3.68 → 2.33 → 1.22 [11]. Es el mejor dato público de decaimiento del alfa por IA.
- **Agentes académicos:**
  - TradingAgents reporta +26.6% en AAPL en ene-mar 2024, con **Sharpe 8.21 y max DD 0.91%**, mientras AAPL comprar y mantener perdía −5.2%. Usó 3 acciones y 3 meses [19].
  - Profit Mirage: después del corte, esos agentes pierden 50-72% del rendimiento [43].
  - FINSABER: la ventaja se deteriora con más años y más símbolos [44].
  - *Inferencia:* un Sharpe de 8 en 60 días de 3 acciones es ruido o fuga.

### 5.3 Competencias reales entre IAs con dinero

**Alpha Arena T1 (Nof1)**
- 6 modelos con 10,000 USD reales cada uno, en perpetuos de Hyperliquid (BTC, ETH, SOL, BNB, DOGE, XRP) con apalancamiento.
- Mismo prompt y solo datos numéricos. Inferencia cada ~2-3 min. Cada orden llevaba objetivo, stop y "condición de invalidación".
- Del ~17/18-oct al 3-nov-2025 a las 17:00 ET [23][45].
- Resultado final (API de Nof1 archivada, procesada en `arena/investigacion/03`; contrastada hoy con iWeaver ±0.5 pp) [45][46]:

| Lugar | Modelo | Final (USD) | Rend. | Posiciones observadas (cortos) | Apalancamiento mediano |
|---|---|---|---|---|---|
| 1 | Qwen3 Max | 12,202 | **+22.0%** | 33 (5) | 20x |
| 2 | DeepSeek Chat V3.1 | 10,453 | +4.5% | 43 (2) | 10x |
| 3 | Claude Sonnet 4.5 | 6,890 | −31.1% | 33 (0) | 15x |
| 4 | Grok 4 | 5,456 | −45.4% | 52 (17) | 10x |
| 5 | Gemini 2.5 Pro | 4,376 | −56.2% | 196 (97) | 10x |
| 6 | GPT-5 | 3,734 | −62.7% | 119 (57) | 15x |
| — | Comprar y mantener BTC | 9,994 | −0.1% | — | — |

- Las posiciones salen de capturas horarias, así que son cotas inferiores. iWeaver reporta ~43 operaciones para Qwen [46].
- **Patrones:**
  1. **Sobretrading.** Los dos más activos (Gemini y GPT-5) quedaron últimos. Nof1: "al principio el PnL estaba dominado por costos" [23].
  2. **Direccionalidad.** Claude no abrió ni un corto y perdió 31% en un mercado bajista. Gemini y GPT-5 alternaron mucho entre largo y corto.
  3. **Apalancamiento y stops.** Grok 4 llegó a +50.4% el 21-oct y terminó en −45.4%. Claude llegó a +28.2% y terminó en −31.1%. El ranking del día 3 no predijo el final [45].
  4. **Sensibilidad al prompt** [23].
- **Crítica estadística (Tseitlin):** una sola instancia, dos semanas, cripto sin información y apalancamiento de 15x; para él, eso no es una prueba de inteligencia [47]. Con SE ≈ 4.6 del Sharpe, coincido.

**Alpha Arena T1.5**
- Del 19/20-nov al 3-dic-2025, con acciones de EUA tokenizadas.
- 8 modelos en 4 modalidades (base, "Monk Mode", con ranking visible, apalancamiento máximo) [45].
- **Grok 4.20 ("Mystery Model") ganó con +12.11% agregado** y fue el único positivo en el agregado [38][48]. Las cifras de los demás modelos que circulan están **no verificadas**.

**Prediction Arena (2026, dinero real en Kalshi y Polymarket)** [49]
- 10,000 USD por modelo, con decisiones cada 15-45 min, del 12-ene al 9-mar-2026.
- Resultados en Kalshi:

| Modelo | Rend. total | Operaciones | Max DD |
|---|---|---|---|
| GLM-4.7 | −16.0% | 361 | 16.3% |
| Grok-4.20 (checkpoint) | −20.0% | 424 | 30.9% |
| GPT-5.2 | −20.5% | 452 | 18.4% |
| Claude Opus 4.5 | −25.9% | 886 | 25.9% |
| Gemini 3 Pro | −30.5% | 664 | 30.8% |
| Grok-4.1 fast | −30.8% | 129 | 30.8% |

- **Los 6 perdieron.** Promedio en la fase 1: −13.8%.
- Grok-4.20 lideró la fase 1 (pico de +15.5% el 6-feb) y luego cayó.
- En Polymarket el promedio fue −1.1%.
- "El volumen de investigación no se correlaciona con los resultados." Lo que sí importa es la precisión inicial y saber capitalizar los aciertos.

**Lecciones transferibles** (Inferencia)
- (i) La mayoría de los agentes LLM autónomos pierde dinero real en horizontes cortos.
- (ii) Pierden por costos, apalancamiento, sobretrading y salidas, no por "falta de información".
- (iii) Ir adelante temprano no significa nada.
- (iv) El modelo con menos actividad y reglas más estrictas tiende a sobrevivir.
- (v) Contra rivales IA, **no cometer sus errores ya es una ventaja**: `modo_torneo` de `parametros.json`.

### 5.4 ETFs "gestionados con IA" contra el S&P 500

Cálculo propio con cierres ajustados de Yahoo (dividendos incluidos) al 24-sep-2026 [50]. Datos del emisor de AIEQ [51].

| ETF | Desde | Anual ETF | Anual SPY | Max DD ETF / SPY | Beta | TE | t del alfa (≈ IR·√años) |
|---|---|---|---|---|---|---|---|
| AIEQ (EquBot/IBM Watson; comisión 0.75%) | 18-oct-2017 | **9.62%** | **14.84%** | −39.0% / −33.7% | 1.05 | 10.5% | ≈ −1.3 |
| AMOM (QRAFT AI-Enhanced Momentum) | 21-may-2019 | 17.46% | 16.07% | −40.0% / −33.7% | 1.02 | 16.1% | ≈ +0.4 |
| LQAI (LG QRAFT AI-Powered Core) | 7-nov-2023 | 25.22% | 23.13% | −21.2% / −18.8% | 1.05 | 7.4% | ≈ +0.2 |

- **AIEQ** acumula +127% contra +244% del SPY. Por año: −31.9% contra −18.2% en 2022, y +12.5% contra +24.9% en 2024.
- El emisor reporta al 31-ago-2026: NAV **10.08% anual desde el inicio y 4.18% a 5 años**. SPY en las mismas ventanas: 14.93% y 12.69% (cálculo propio). Activos: 118.9 M USD [51].
- *Inferencia:* ningún ETF de IA muestra alfa estadísticamente distinto de cero. El más grande y antiguo pierde ~5 pp al año con más volatilidad y peores caídas. Hay sesgo de supervivencia en la muestra, porque solo quedan los que siguen listados.

### 5.5 Evidencia en México

No encontré estudios verificados de ML o LLM aplicados a la BMV.
*Inferencia:* por Leippold-Wang-Zhou (China), en mercados dominados por minoristas y poco líquidos la predictibilidad de corto plazo es mayor pero vive en la liquidez. En la BMV, con spreads altos y 0.58% por vuelta en GBM, los costos probablemente se la comen. Grado: no evaluable.

---

## 6. Traducción operable

### 6.1 Principio rector

La IA de este sistema es **analista incansable, auditor y ejecutor de reglas**, no oráculo de precios. Las ventajas están donde la evidencia es B o mejor. Lo que es D no toca capital real.

### 6.2 Ventajas reales explotables frente a lo que NO es ventaja

| Ventaja REAL (usar) | Evidencia | Cómo la usa el sistema |
|---|---|---|
| Procesar texto a escala (10-K/20-F, informes trimestrales de la BMV, transcripciones, 8-K, noticias en español e inglés) | FinBen: fuerte en extracción y análisis textual [30]; Chen-Kelly-Xiu: retraso ineficiente en 13 idiomas [9]; news shocks persistentes [10] | Extracción con cita textual y página, reconciliación contable (`modelo_integrado.py`), alertas de eventos con marca de tiempo |
| Cobertura amplia (emisoras de la BMV poco cubiertas, más universo SIC) | Hombre + máquina reduce errores extremos [52] | Pantallas y fichas (`ficha-empresa`) sobre cientos de emisoras; la IA pre-filtra y el comité decide |
| Disciplina impuesta por código | En Alpha Arena, los LLM *sin* reglas duras sobreoperaron [23][45] | `riesgo.py`, `validar_orden`, cortacircuitos y rachas; la IA no puede saltárselos |
| Velocidad de investigación y replicación | Replicar GKX/Nagel en días | `laboratorio/replicas` con registro de variantes |
| Auditoría adversarial (buscar la falla) | Retracciones de 2025-2026 [25][26][27] | Comité con disenso obligatorio, `registro-de-errores.md` |
| Pronósticos probabilísticos medibles | ForecastBench: el LLM queda por debajo de los expertos [53]; hay que calibrarlo | Bitácora con Brier (`pronosticos.brier_objetivo` = 0.2, `min_pronosticos_para_evaluar` = 50) |

| NO es ventaja (no usar como fuente de alfa) | Evidencia |
|---|---|
| Predecir precios de días o semanas con un LLM sin datos exclusivos | Alpha Arena, Prediction Arena, StockBench, AI-Trader y FINSABER: la mayoría pierde o empata con el pasivo |
| Backtests de LLM dentro de su ventana de entrenamiento | Memorización [12]; Profit Mirage −50-72% [43] |
| Modelos "complejos" por sí mismos | Nagel: una regla de 2 líneas replica el resultado [3] |
| Velocidad tipo HFT o noticias intradía | Punto de equilibrio <20 pb [11]; el dueño ejecuta a mano en GBM |
| Puntajes de razonamiento o benchmarks estáticos | LiveTradeBench: LMArena ≠ trading [34] |
| Marcos multiagente con backtests espectaculares | TradingAgents con Sharpe 8 en 60 días [19] |
| Comprar un ETF "de IA" | AIEQ −5 pp al año contra SPY |

### 6.3 Reglas concretas (coherentes con `config/parametros.json`)

1. **Regla ML-1, sin señal de LLM como único disparador.**
   - Toda señal cuya fuente de alfa sea el juicio predictivo de un LLM tiene edge = 0 por defecto. Con μ = 0, Kelly da tamaño 0, sin importar `kelly.fraccion_max` (0.25 patrimonio / 0.5 arena).
   - Solo entra al satélite (`satelite_max` = 0.3) si pasa todo `validacion_estrategias`.
2. **Regla ML-2, conflicto de horizonte.**
   - `backtest_min_anios` = 10 no se puede cumplir fuera de muestra con un LLM comercial, cuyo corte es reciente.
   - Por eso una señal-LLM solo se valida (a) con un modelo point-in-time sobre ≥10 años, o (b) con papel prospectivo de ≥3 meses y ≥30 operaciones (`paper_trading_min_meses`, `paper_trading_min_operaciones`). Después entra con `fraccion_capital_inicial` = 0.25.
   - *Inferencia:* en la práctica, los LLM quedan en funciones de procesamiento y filtro.
3. **Regla ML-3, filtro de costo y horizonte.**
   - Prohibidas las estrategias de noticias con horizonte diario: el punto de equilibrio es <20 pb por vuelta contra ~58 pb de GBM.
   - En la arena rigen `operaciones_max_mes` = 8, `rotacion_max_mensual_x_capital` = 1.5, `orden_minima_mxn` = 5,000 y movimiento esperado ≥ 5%.
   - Al tope de rotación, el costo de comisiones es de ~5% por temporada (1.5 × 6 × 0.58%, *inferencia*).
4. **Regla ML-4, regla simple primero.** Todo modelo ML o LLM se compara contra (a) comprar y mantener, (b) el benchmark principal (50% S&P 500 TR en MXN + 50% CETES 28d) y (c) la regla simple más parecida (momentum cronometrado por volatilidad, media de 200 días). Si la regla simple explica el alfa (t < 2 del residual), se usa la regla simple.
5. **Regla ML-5, deflación con TODAS las variantes.** Cada idea que genere una IA cuenta como prueba en el registro de variantes (`backtest.py`), incluso las que se descartaron en conversación. DSR ≥ 0.95 y PBO ≤ 0.25 sobre ese N total. El DSR no detecta fuga (el oráculo de Gençay con SR 35 lo pasa): la garantía contra look-ahead es estructural (§6.4).
6. **Regla ML-6, núcleo sin "IA de marca".** El núcleo (`nucleo_min` = 0.7) usa índices de bajo costo. Ningún ETF de IA entra al núcleo; al satélite, solo con la misma validación que cualquier estrategia.
7. **Regla ML-7, trazabilidad del modelo.** Todo análisis de IA registra ID del modelo, fecha de corte declarada, fecha de ejecución, prompt (hash) y fuentes. Si el proveedor cambia el modelo, se re-corren las validaciones: el edge del prompt anterior no se hereda.
8. **Regla ML-8, invariancia al prompt.** Un pronóstico de LLM se registra solo si sobrevive a ≥3 reformulaciones y a cambiar el orden de las opciones. La probabilidad final es la mediana. Si la dispersión entre prompts es >15 pp, se marca "no concluyente" (umbral propio; motivado por Nagel-Tseng-Xiu [24]).
9. **Regla ML-9, ejecución humana y límites duros.** Los límites de pérdida, los cortacircuitos (patrimonio −8/−12/−15/−20%; arena −12/−20/−28/−35%) y las rachas (3 pérdidas → ×0.5; 5 → pausa) aplican sin excepción aunque la IA tenga "alta convicción". Alpha Arena mostró que la convicción del LLM no predice nada.
10. **Regla ML-10, arena contra IAs.** Esperar de los rivales IA sobretrading, apalancamiento (ETFs 3x) y giros direccionales. Nuestra ventaja base es no repetirlos:
    - `etf_apalancado_max` = 0.5 solo con `filtro_apalancados` (subyacente > MA200 y VIX < 25);
    - `riesgo_por_operacion` = 0.03;
    - `modo_torneo`: adelante por ≥5 pp, bajar varianza; atrás por ≥5 pp, subir exposición dentro de límites.
    - No perseguir al líder temprano (T1: el ranking del día 3 no predijo el final).
11. **Regla ML-11, fase 0.** Según `prioridad_actual`, nada de lo anterior propone inversiones reales antes de aprobar el examen (≥90%) y cumplir 3 meses de Brier ≤ 0.2 en papel.

### 6.4 Protocolo anti look-ahead cuando una IA evalúa estrategias (obligatorio)

1. **Declarar el corte.** Se registran el modelo y su fecha de corte C. Toda ventana de evaluación que empiece antes de C + 3 meses se marca como **"contaminada"** y no cuenta como evidencia (el margen es regla propia, porque los cortes declarados son imprecisos [12][15]).
2. **Datos point-in-time.**
   - Precios con cierre ajustado solo hasta t−1. Fundamentales por **fecha de publicación del reporte** (fecha del 10-Q/10-K o del reporte a la BMV), nunca por fecha de cierre del periodo.
   - Sin datos re-expresados. Universo con emisoras deslistadas (sin sesgo de supervivencia).
   - FX al tipo del día de la decisión (FIX como referencia).
3. **Barrera estructural.** La IA solo accede a datos a través del motor (`Historia` en `backtest.py`: pedir `h.activo[t]` lanza error). Las señales precalculadas pasan `auditar_constructor` (invariancia de prefijo). La IA no puede escribir código que lea archivos crudos completos.
4. **Prueba de oráculo con fuga.** Antes de confiar en el pipeline, se inyecta una variable con fuga conocida. El sistema debe detectarla y bloquearla. Si el pipeline la acepta, está roto, aunque el DSR se vea bien [36].
5. **Prueba de memoria.** Para cada par empresa-fecha relevante se pregunta al modelo, solo con la fecha, por el resultado realizado (LAP). Si el recuerdo supera el azar, la ventana está contaminada [15].
6. **Anonimizar no basta.** Ayuda contra la distracción [13], pero no evita la memorización [12]. Se usa como complemento, nunca como garantía.
7. **Pre-registro.** Hipótesis, universo, horizonte, costos (0.29% por lado + spread), métricas y criterio de éxito quedan escritos y con hash (`huellas.py`) **antes** de ver datos fuera de muestra.
8. **Registro de todas las variantes** y DSR/PBO sobre el N total (Regla ML-5).
9. **Costos realistas.** Comisión GBM, spread, FX, impuestos (retención SIC), orden mínima y ejecución manual con rezago. Se usa el escenario de spread "medio" para el caso base.
10. **Benchmarks obligatorios.** Comprar y mantener del activo, benchmark principal, regla simple equivalente y 1/N.
11. **Regímenes.** Reportar por separado alzas, bajas y crisis. FINSABER: los LLM son conservadores en alzas y agresivos en bajas [44].
12. **Replicación del juicio.** Mínimo 2 familias de modelos y 5 corridas o prompts por decisión crítica. Se reportan la dispersión y la mediana.
13. **Validación prospectiva.** Papel ≥3 meses y ≥30 operaciones antes de capital real. Se reporta el SE del Sharpe (§2.8) junto al resultado.
14. **Re-certificación.** Cualquier cambio de modelo, de prompt de sistema o de fuente de datos reinicia los pasos 1, 5 y 13.

### 6.5 Rutinas (fase 0: solo entrenamiento y papel)

- **Diaria (≤30 min de cómputo).** Triage de noticias y reportes (BMV, EDGAR) con marca de tiempo de publicación. Extracción de cifras con cita. Actualización de alertas de eventos. Registro de 1-3 pronósticos probabilísticos con la Regla ML-8.
- **Semanal.**
  - Revisar el desempeño en papel contra los benchmarks.
  - Auditar el pipeline con la prueba de oráculo (paso 4) sobre una señal.
  - Una ficha de lectura de un paper de este módulo (estado: Documentado → Comprendido).
- **Mensual.**
  - Calcular el Brier acumulado y la calibración.
  - Revisar la deriva de los modelos (cambios de versión de los proveedores).
  - Re-correr el decaimiento de la señal por subperiodos.
  - Actualizar el registro de rivales (`competencia/rivales.csv`).
- **Por evento** (cambio de modelo del proveedor): re-certificación (paso 14).

---

## 7. Trampas y errores comunes

1. **Backtest de LLM dentro de su corte.** El caso típico es FinMem o TradingAgents con GPT-4o sobre 2023. Profit Mirage mide una caída de 50-72% después del corte [43].
2. **Confundir la reacción inicial con alfa operable.** El ~90% de acierto de Lopez-Lira-Tang es sobre la reacción **no operable**; el drift se acierta 55-58% [11].
3. **Reportar Sharpe brutos, equiponderados y con microcaps** (2.45 en GKX, 7.2 en JKX) como si fueran implementables.
4. **Creer que la complejidad es la fuente del alfa** sin probar la regla simple equivalente (Nagel).
5. **Sharpe espectacular en ventanas cortas.** El SE del Sharpe anual con 60 días es de ~2.3-2.5. Un SR de 8 en 3 meses es ruido o fuga.
6. **Tomar competencias de IA como ranking de habilidad.** n = 1 corrida, 2 semanas y apalancamiento de 10-20x. El ganador de T1 (Qwen) no repitió el éxito en T1.5 según los resúmenes *(no verificado)*.
7. **Creer que el DSR y el PBO detectan look-ahead.** No lo hacen: el oráculo con fuga pasa [36]. La protección es estructural.
8. **Anonimizar y dar el problema por resuelto.** El LLM reconstruye la entidad con contexto mínimo [12].
9. **Pedirle al LLM que "ignore lo que sabe después de X".** No funciona [12].
10. **Usar la probabilidad del LLM como creencia del mercado.** Responde al tono y al orden de las etiquetas [24].
11. **Citar papers retirados o en duda:** Kim-Muhn-Nikolaev (retirado), Kim-Nikolaev (retractado), van Binsbergen-Han-Lopez-Lira (*Expression of Concern*).
12. **Ignorar el decaimiento por adopción.** Si todos usan el mismo modelo sobre las mismas noticias, el edge converge a cero (6.54 → 1.22) y los drawdowns se correlacionan.
13. **Comparar ETFs de IA sin ajustar por beta y volatilidad.** AMOM "le gana" al SPY con beta 1.02, TE 16% y t ≈ 0.4: eso no es alfa.
14. **Aceptar capturas de pantalla de X o foros** como prueba. Se exige publicación fechada previa, historial completo con pérdidas, reglas previas, capital y costos (ver `ideas-adoptadas`, punto 6).
15. **Creer que "más investigación" del agente mejora el resultado.** En Prediction Arena el volumen de investigación no se correlacionó con los resultados [49].

---

## 8. Examen de titulación

1. **¿Por qué GKX miden el R²_OOS contra cero y no contra la media histórica?** Porque la media histórica por acción es tan ruidosa que pronostica peor que cero y bajaría artificialmente el R². Con ese benchmark, las NN logran 0.33-0.40% mensual.
2. **¿Qué parte de los Sharpe de GKX (1.35 VW / 2.45 EW) es implementable para un minorista?** Poca. Son brutos, long-short, con turnover de 110-130% al mes. Avramov et al. muestran que la rentabilidad del deep learning se atenúa mucho fuera de microcaps y empresas en problemas, y se deteriora con costos.
3. **Explique en una frase la crítica de Nagel a KMZ.** Con P ≫ T y ventanas cortas, la regresión ridgeless con RFF es un promedio de rendimientos recientes ponderado por similitud, es decir, momentum cronometrado por volatilidad. Controlando por esa regla, el alfa cae de 3.4% (t 2.42) a 1.2% (t 0.95).
4. **¿Qué pasa con el Sharpe del SDF de Chen-Pelger-Zhu al restringirse a acciones grandes?** Baja de 2.6 a 1.4 (1,500 mayores) y a 0.9 (550 mayores).
5. **¿Cuánto rinde neta la anomalía promedio en la era moderna?** 4 pb al mes (Chen-Velikov, 204 anomalías). Las mejores rinden ≤10 pb.
6. **Dé las cifras de decaimiento de Lopez-Lira-Tang y su implicación.** El Sharpe del long-short de drift con GPT-4 pasó de 6.54 (4T 2021) a 3.68, 2.33 y 1.22 (ene-may 2024). Deja de ser rentable a 20 pb por vuelta. Implicación: el edge de "LLM lee noticias" se arbitra conforme se adopta, y en GBM (~58 pb) es inoperable.
7. **Diferencie look-ahead y distracción según Glasserman-Lin.** Look-ahead: el modelo conoce el rendimiento posterior. Distracción: el conocimiento de la empresa sesga la lectura. Dentro de muestra, anonimizar mejoró el resultado, así que dominó la distracción.
8. **¿Por qué un backtest de LLM antes de su fecha de corte no es evidencia?** Porque la habilidad contrafactual no está identificada: el modelo memoriza valores realizados, y ni las instrucciones ni las máscaras lo evitan (Lopez-Lira-Tang-Zhu).
9. **¿Qué es la LAP y cómo detecta contaminación?** Es la probabilidad de que el LLM recuerde el resultado de un par empresa-fecha preguntándole solo por la fecha. Si la interacción LAP × pronóstico es positiva en una regresión de precisión, hay look-ahead. La LAP colapsa a ~0 después del corte.
10. **Resultado final de Alpha Arena T1 y lección principal.** Qwen3 Max +22.0%, DeepSeek +4.5%, Claude −31.1%, Grok 4 −45.4%, Gemini −56.2% y GPT-5 −62.7%; BTC −0.1%. Lección: pierden por sobretrading, apalancamiento y salidas; el ranking temprano no predice nada; n = 1 y 17 días no miden habilidad (SE del Sharpe ≈ 4.6).
11. **¿Qué mostró Prediction Arena 2026?** Con dinero real en Kalshi, los 6 modelos de frontera perdieron, de −16.0% a −30.8%, en 57 días. El volumen de investigación no se correlacionó con el resultado.
12. **¿AIEQ le ganó al S&P 500?** No. Desde el 18-oct-2017 rinde 9.62% anual contra 14.84% del SPY, con beta 1.05 y max DD de −39% contra −34%. El emisor reporta 10.08% anual desde el inicio y 4.18% a 5 años (NAV al 31-ago-2026).
13. **¿Por qué el DSR no basta para certificar una estrategia propuesta por un LLM?** Porque corrige la búsqueda, no la fuga. Un oráculo con fuga y Sharpe de 35 pasa DSR y PBO (Gençay 2026). La barrera tiene que ser estructural: acceso a datos solo "as-of".
14. **Nombre tres ventajas reales de un inversionista asistido por IA y una falsa.** Reales: procesar texto a escala, cobertura amplia y disciplina impuesta por código (más velocidad de investigación y auditoría). Falsa: predecir precios de corto plazo con un LLM sin datos exclusivos.
15. **Según `parametros.json`, ¿con qué tamaño entra una señal predictiva de LLM no validada?** Cero. Edge no validado implica μ = 0, y Kelly da 0. Solo tras DSR ≥ 0.95, PBO ≤ 0.25 y papel de ≥3 meses con ≥30 operaciones entra con el 25% del capital asignado, dentro de `satelite_max` = 0.3.

---

## 9. Fuentes

1. Gu, S., Kelly, B., Xiu, D. (2020). Empirical Asset Pricing via Machine Learning. *RFS* 33(5):2223-2273. https://doi.org/10.1093/rfs/hhaa009 · PDF del autor: https://dachxiu.chicagobooth.edu/download/ML.pdf · NBER: https://www.nber.org/papers/w25398
2. Kelly, B., Malamud, S., Zhou, K. (2024). The Virtue of Complexity in Return Prediction. *JF* 79(1):459-503. https://doi.org/10.1111/jofi.13298 · https://www.nber.org/papers/w30217
3. Nagel, S. (2025). Seemingly Virtuous Complexity in Return Prediction. NBER w34104 (11-ago-2025). https://www.nber.org/papers/w34104
4. Berk, J. (2023). Comment on "The Virtue of Complexity in Return Prediction". SSRN. https://doi.org/10.2139/ssrn.4410125
5. Buncic, D. (2025). Simplified: A Closer Look at the Virtue of Complexity in Return Prediction. SSRN 5239006 (abr-2025). https://doi.org/10.2139/ssrn.5239006 [25-sep-2026: SSRN devuelve 403 desde este entorno; cifras (Sharpe 0.699 vs 0.485) verificadas vía cita de Nagel [3] y comunicado de Stockholm Business School, https://www.su.se/english/divisions/stockholm-business-school/news/articles/2025-09-25-new-research-debunks-the-virtue-of-complexity-in-return-prediction-in-finance]
6. Kelly, B., Malamud, S. (2025). Understanding the Virtue of Complexity. Working paper, Yale University [25-sep-2026: año y afiliación confirmados vía la bibliografía de Nagel [3] (antes "fecha no verificada" en esta lista); PDF propio no localizado] (listado en https://www.bryankellyacademic.org/)
5b. Elmore, R., Strauss, J. (2025). Is Complexity Virtuous? *Economics Letters* 258:112749. https://doi.org/10.1016/j.econlet.2025.112749 · SSRN 5376107 · abstract: https://digitalcommons.du.edu/business_info_fac/6/ [25-sep-2026: verificado a nivel de resumen; correlación 97.5% con el promedio móvil de 12 meses de RFF con penalización grande. No aparece citado dentro de Nagel [3], es independiente]
7. Chen, L., Pelger, M., Zhu, J. (2024). Deep Learning in Asset Pricing. *Management Science* 70(2):714-750. https://doi.org/10.1287/mnsc.2023.4695 · https://arxiv.org/abs/1904.00745
8. Jensen, T., Kelly, B., Malamud, S., Pedersen, L. (2026). Machine Learning and the Implementable Efficient Frontier. *RFS* 39(10):3035-3078. https://doi.org/10.1093/rfs/hhag022
9. Chen, Y., Kelly, B., Xiu, D. Expected Returns and Large Language Models (feb-2026). https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4416687 · listado y resumen: https://dachxiu.chicagobooth.edu/
10. Página de investigación de B. Kelly (resúmenes de Chen-Kelly-Xiu, "The Inefficient Pricing of News", "Scaling Point-in-Time Language Models"): https://www.bryankellyacademic.org/
11. Lopez-Lira, A., Tang, Y. Can ChatGPT Forecast Stock Price Movements? Return Predictability and Large Language Models. arXiv 2304.07619 (v6, 28-oct-2025). https://arxiv.org/abs/2304.07619
12. Lopez-Lira, A., Tang, Y., Zhu, M. (2025). The Memorization Problem: Can We Trust LLMs' Economic Forecasts? arXiv 2504.14765. https://arxiv.org/abs/2504.14765
13. Glasserman, P., Lin, C. (2023). Assessing Look-Ahead Bias in Stock Return Predictions Generated By GPT Sentiment Analysis. arXiv 2309.17322. https://arxiv.org/abs/2309.17322
14. Sarkar, S., Vafa, K. (2024). Lookahead Bias in Pretrained Language Models. SSRN. https://doi.org/10.2139/ssrn.4754678
15. Gao, Z., Jiang, W., Yan, Y. Detecting Lookahead Bias in LLM Forecasts. arXiv 2512.23847 (v2, jun-2026). https://arxiv.org/abs/2512.23847
16. He, S., Lv, L., Manela, A., Wu, J. (2025). Chronologically Consistent Large Language Models. arXiv 2502.21206. https://arxiv.org/abs/2502.21206
17. Benhenda, M. (2026). Look-Ahead-Bench. arXiv 2601.13770. https://arxiv.org/abs/2601.13770
18. Chen, H., Chen, L., Chen, Y., Huang, D., Zhang, B. (2026). Does Training on Future Data Pay? Look-Ahead Bias in Forecasting with Pretrained Models. arXiv 2609.20554. https://arxiv.org/abs/2609.20554
19. Xiao, Y., Sun, E., Luo, D., Wang, W. (2024-25). TradingAgents: Multi-Agents LLM Financial Trading Framework. arXiv 2412.20138. https://arxiv.org/abs/2412.20138
20. Yu, Y. et al. (2023). FinMem. arXiv 2311.13743. https://arxiv.org/abs/2311.13743
21. Zhang, W. et al. (2024). A Multimodal Foundation Agent for Financial Trading (FinAgent). arXiv 2402.18485. https://arxiv.org/abs/2402.18485
22. Yu, Y. et al. (2024). FinCon. arXiv 2407.06567. https://arxiv.org/abs/2407.06567
23. Nof1. "Exploring the Limits of LLMs as Quant Traders in Live Markets" (oct-2025). https://nof1.ai/blog/TechPost1 · copia archivada: https://web.archive.org/web/20251028041142/https://nof1.ai/blog/TechPost1 (hoy nof1.ai respondió 429 y un punto de control de Vercel; se usa la lectura documentada en `arena/investigacion/03`)
24. Nagel, S., Tseng, C., Xiu, D. (2026). Completions, Not Convictions: Can LLM Probabilities Proxy for Human Beliefs? SSRN 7265538. https://doi.org/10.2139/ssrn.7265538
25. Kim, A., Muhn, M., Nikolaev, V. Financial Statement Analysis with Large Language Models, arXiv 2407.17866 (v3 retirado, 20-feb-2025). https://arxiv.org/abs/2407.17866
26. Retracción: Kim, A. G., Nikolaev, V. V., "Context-Based Interpretation of Financial Information", *JAR* (29-abr-2026). https://doi.org/10.1111/1475-679x.70057
27. Expression of Concern, *RFS* 39(5):1555 (en línea 1-mar-2026). https://doi.org/10.1093/rfs/hhag017
28. Zhang, Y., Zhu, Z., Linnainmaa, J. (2025). Man versus Machine Learning Revisited. *RFS* 38(12):3768-3790. https://doi.org/10.1093/rfs/hhaf066
29. Israel, R., Kelly, B., Moskowitz, T. (2020). Can Machines "Learn" Finance? SSRN. https://doi.org/10.2139/ssrn.3624052
30. Xie, Q. et al. (2024). FinBen: A Holistic Financial Benchmark for LLMs. arXiv 2402.12659. https://arxiv.org/abs/2402.12659
31. Li, H. et al. (2024). InvestorBench. arXiv 2412.18174. https://arxiv.org/abs/2412.18174
32. Chen, Y. et al. StockBench: Can LLM Agents Trade Stocks Profitably in Real-World Markets? arXiv 2510.02209 (v2, 2-mar-2026). https://arxiv.org/abs/2510.02209
33. Qian, L. et al. (2025). When Agents Trade: Live Multi-Market Trading Benchmark for LLM Agents (Agent Market Arena). arXiv 2510.11695. https://arxiv.org/abs/2510.11695
34. Yu, H., Li, F., You, J. (2025). LiveTradeBench. arXiv 2511.03628. https://arxiv.org/abs/2511.03628
35. Fan, T. et al. (2025). AI-Trader: Benchmarking Autonomous Agents in Real-Time Financial Markets. arXiv 2512.10971. https://arxiv.org/abs/2512.10971
36. Gençay, E. (2026). What Survives Honest Evaluation? Leakage-Safe, Search-Aware Assessment of LLM-Driven Trading Strategy Discovery. arXiv 2608.27734. https://arxiv.org/abs/2608.27734
37. Noguer i Alonso, M., Franklin, R. P. (2026). Pretrained Time-Series Foundation Models for Financial Return Forecasting. arXiv 2606.27100. https://arxiv.org/abs/2606.27100
38. TradeRank. "5 Alpha Arena Alternatives for AI Trading (2026)", actualizado el 14-sep-2026. https://www.traderank.ai/blog/alpha-arena-alternatives-2026 (válido para el estado del leaderboard y el +12.11% de T1.5; su −57.92% de Grok 4 en T1 es erróneo)
39. Dou, W., Goldstein, I., Ji, Y. (2025). AI-Powered Trading, Algorithmic Collusion, and Price Efficiency. NBER w34054. https://doi.org/10.3386/w34054
40. Wang (2026). AI Adoption in Financial Markets and Information Quality. SSRN. https://doi.org/10.2139/ssrn.6417018
41. Zhang, Zhou (2026). AI Herding in Financial Market: An Experiment with Large Language Models. SSRN. https://doi.org/10.2139/ssrn.6805805
42. FMI, *Global Financial Stability Report*, oct-2024, cap. 3, "Advances in Artificial Intelligence: Implications for Capital Market Activities". https://doi.org/10.5089/9798400277573.082.ch003
43. Li, X., Zeng, Y., Xing, X., Xu, J., Xu, X. (2025). Profit Mirage: Revisiting Information Leakage in LLM-based Financial Agents. arXiv 2510.07920. https://arxiv.org/abs/2510.07920
44. Li, W. W., Kim, H., Cucuringu, M., Ma, T. Can LLM-based Financial Investing Strategies Outperform the Market in Long Run? (FINSABER), KDD 2026. arXiv 2505.07078. https://arxiv.org/abs/2505.07078
45. API de Nof1 `account-totals`, T1, marca horaria 407 (3-nov-2025), copia de Wayback: https://web.archive.org/web/20251104022344/https://nof1.ai/api/account-totals?lastHourlyMarker=407 — procesada en `/home/user/New1/arena/investigacion/03-teoria-de-torneos-y-estrategia-competitiva.md` (hoy web.archive.org no fue accesible para re-descargarla)
46. iWeaver. "Alpha Arena Season 1 Results: Final Ranking and Lessons". https://www.iweaver.ai/blog/alpha-arena-ai-trading-season-1-results/
47. Tseitlin, B. (nov-2025). "Why Alpha Arena was a bad benchmark". https://borisagain.substack.com/p/why-alpha-arena-is-literally-the
48. SammyFans (5-dic-2025). "Grok 4.20 beats all other AI models in Alpha Arena test". https://www.sammyfans.com/2025/12/05/grok-4-20-beats-all-other-ai-models-in-alpha-arena-test/
49. Zhang, J. et al. (2026). Prediction Arena: Benchmarking AI Models on Real-World Prediction Markets. arXiv 2604.07355. https://arxiv.org/abs/2604.07355
50. Yahoo Finance, API de gráficas (cierres ajustados de AIEQ, AMOM, LQAI y SPY; descargados el 25-sep-2026). https://query1.finance.yahoo.com/v8/finance/chart/AIEQ
51. Amplify ETFs, AIEQ (inicio 17-oct-2017, comisión 0.75%, desempeño al 31-ago-2026). https://amplifyetfs.com/aieq/
52. Cao, S., Jiang, W., Wang, J., Yang, B. (2024). From Man vs. Machine to Man + Machine: The Art and AI of Stock Analyses. *JFE* 160. https://www.nber.org/papers/w28800
53. Karger, E. et al. (2025). ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities. arXiv 2409.19839. https://arxiv.org/abs/2409.19839
54. Avramov, D., Cheng, S., Metzker, L. (2023). Machine Learning vs. Economic Restrictions. *MS* 69(5):2587-2619. https://doi.org/10.1287/mnsc.2022.4449
55. Leippold, M., Wang, Q., Zhou, W. (2022). Machine Learning in the Chinese Stock Market. *JFE* 145(2):64-82. https://doi.org/10.1016/j.jfineco.2021.08.017
56. Bryzgalova, S., Pelger, M., Zhu, J. (2025). Forest Through the Trees. *JF* 80(5):2447-2506. https://doi.org/10.1111/jofi.13477
57. Chen, A., Velikov, M. (2023). Zeroing In on the Expected Returns of Anomalies. *JFQA* 58(3):968-1004. https://doi.org/10.1017/S0022109022000874
58. Azevedo, V., Hoegner, C., Velikov, M. (2024). The Expected Returns on Machine-Learning Strategies. SSRN. https://doi.org/10.2139/ssrn.4702406
59. Jiang, J., Kelly, B., Xiu, D. (2023). (Re-)Imag(in)ing Price Trends. *JF* 78(6):3193-3249. https://doi.org/10.1111/jofi.13268 · versión de trabajo: https://www.aidf.nus.edu.sg/wp-content/uploads/2022/02/Xiu-Re-Imagining-Price-Trends.pdf
60. Kelly, B., Xiu, D. (2023). Financial Machine Learning. *Foundations and Trends in Finance* 13(3-4):205-363. https://doi.org/10.1561/0500000064 · https://www.nber.org/papers/w31502
61. Kelly, B., Kuznetsov, B., Malamud, S., Xu, T. (2025). Artificial Intelligence Asset Pricing Models. NBER w33351. https://doi.org/10.3386/w33351
62. Didisheim, A., Fraschini, M., Somoza, L. (2025). AI's Predictable Memory in Financial Analysis. *Economics Letters* 256:112602. https://doi.org/10.1016/j.econlet.2025.112602
63. Bybee, L., Kelly, B., Manela, A., Xiu, D. (2024). Business News and Business Cycles. *JF* 79(5):3105-3147. https://doi.org/10.1111/jofi.13377

---

**Nota de verificación (25-sep-2026).**
- La herramienta WebSearch estaba agotada en esta sesión (tope de 200 búsquedas). La verificación se hizo con más de 40 consultas directas a Crossref, a la búsqueda y las páginas de arXiv, a NBER, a los sitios de los autores (Xiu, Kelly), a Hacker News (Algolia), con WebFetch y descargando los PDF (GKX, Nagel, Chen-Pelger-Zhu, JKX, Lopez-Lira-Tang v6, TradingAgents, FinMem, Profit Mirage, StockBench y Prediction Arena), de donde salen las cifras citadas.
- Sin verificar: las cifras de Sharpe de Chen-Kelly-Xiu (SSRN 403); los detalles del capítulo del FMI (403); Cartea-Jin-Shi y Fallahgoul (solo vía Nagel); los resultados por modelo de Alpha Arena T1.5 distintos del ganador; si existe una temporada 2 posterior a ago-2026.

**Adenda de verificación (25-sep-2026, segunda pasada, tarea de huecos del examen S7-02).** Se releyeron íntegros (extracción con `pypdf`, sin `poppler-utils` disponible: `apt-get install poppler-utils` falló por 404 del repositorio) los PDF de KMZ (JF 2024, versión de `economics.yale.edu`) y de Nagel (NBER w34104). Se confirmaron con cita textual: la mejora de Sharpe ≈0.47/año con t≈3.0 de KMZ, el diseño (15 predictores, P≤12,000, T=12/60/120, CRSP 1926-2020), la inflación de ≈3pp del R² de GKX por usar la media histórica (nota 34 exacta, con OLS-3 → 3.74%), y el año/afiliación de la réplica de Kelly-Malamud (2025, Yale). Buncic y Elmore-Strauss se verificaron con nivel de acceso menor (comunicado institucional y resumen, respectivamente; SSRN bloqueó ambos PDF con 403). Detalle completo en `conocimiento/fichas/2026-09-25-examen-S7-complejidad-y-0dte.md`.
