# Módulo 25 — Pronóstico de resultados empresariales y análisis de estados financieros

> Nivel: especialidad (posgrado en contabilidad financiera + mesa de análisis fundamental) · Actualizado: 2026-09-25 · Grado de evidencia global: **B** en los hechos sobre pronósticos (el consenso es optimista a un año y pesimista justo antes del reporte, el random walk es difícil de vencer a un año y el PEAD clásico murió en las grandes) · **C** en convertir un pronóstico propio en alfa neto desde GBM · **D** en usar un LLM como oráculo de utilidades: los tres estudios insignia están retirados, retractados o bajo expresión de preocupación.

Enlaces (no se repiten aquí):
- Cap. 03: DCF, DCF inverso (§2.7), M-score, accruals, F-score (§2.10), vetos y reglas de compra (§6.1).
- Cap. 15: eventos corporativos y debate PEAD 2025 (§4).
- Cap. 16: macro, divisas y peso.
- Cap. 17: crisis.
- Cap. 23: geopolítica.
- Cap. 24: política pública y regulación.
- En redacción: 04 (renta fija/macro), 11 (México: SIC, BMV/BIVA, fiscalidad), 13 (estado del mercado) y 22 (fuentes de datos con IA).

---

## 1. Objetivos de dominio

Quien se titula en este módulo sabe:
1. Explicar por qué una utilidad solo mueve el precio en relación con lo que el precio ya descuenta, y medir esa brecha en tres capas: consenso del trimestre, guía y DCF inverso.
2. Elegir el benchmark de pronóstico según horizonte, tamaño y cobertura: random walk, consenso, modelo transversal (EP/RI) o combinación.
3. Cuantificar los sesgos del consenso (optimismo a 12 meses y *walk-down* a metas superables) y leer un "beat" con esa tasa base.
4. Construir un modelo de tres estados por drivers que cuadre y termine en FCF. Los drivers son volumen × precio × mezcla × FX, apalancamiento operativo, capex con vidas útiles y días de capital de trabajo.
5. Reconciliar GAAP con non-GAAP, tratar la SBC como costo, aislar las ganancias no operativas y detectar cambios de estimación contable.
6. Aplicar el checklist de alertas: DSO, DIO, capitalización, auditor y reexpresiones.
7. Traducir un hecho político o geopolítico a una línea del estado de resultados y a una sensibilidad numérica.
8. Valuar con escenarios bear/base/bull cuyas probabilidades suman 100% y contrastarlos con las expectativas implícitas.
9. Registrar el pronóstico antes del reporte y evaluarlo con Brier, skill contra la tasa base, error escalado por precio y cobertura de intervalos.
10. Extraer los datos de la SEC (companyfacts, frames) y de BMV/Emisnet (XBRL `ifrsxbrl`) sin usar la memoria del modelo.

---

## 2. Marco teórico

### 2.1 La ecuación que gobierna todo
La reacción a un reporte es función de **real − esperado**, no del real. Lo esperado tiene tres capas:
- **Capa 1: el consenso del trimestre.** UPA, ingresos y la métrica clave del sector: ventas mismas tiendas, tráfico de pasajeros, NIM o EBITDA.
- **Capa 2: guía y número "susurrado".** No es observable. Se infiere de la reacción y del historial.
- **Capa 3: la trayectoria de 3 a 10 años implícita en el precio.** Se mide con el DCF inverso (cap. 03 §2.7).

Un beat que no mueve la capa 3 casi no mueve el precio. Un miss acompañado de una guía que sube la capa 3 puede subirlo.

**Inferencia:** para un inversionista sin terminal ni latencia, la ventaja rara vez está en adivinar el centavo del trimestre. Está en detectar que la capa 3 está mal por un driver que se puede medir mejor que el mercado.

- **Edge esperado** ≈ (E[valor propio] − precio) × P(el mercado lo reconoce dentro del horizonte) − costos.
- En la arena, el horizonte es de 6 meses (`perfiles_riesgo.arena_agresivo.temporada_meses`). Eso da dos reportes por emisora, es decir, dos verificaciones fechadas de la tesis.

### 2.2 Jerarquía de modelos de pronóstico (de lo robusto a lo frágil)

**1. Random walk (RW).**
- Anual: E_{t+1} = E_t. Trimestral estacional: E_q = E_{q−4} (+ deriva).
- Gerakos y Gramacy: a un año, el RW rinde igual que métodos sofisticados con muchos predictores [16].
- Bradshaw, Drake, Myers y Myers (2012) encuentran que el RW es **más preciso que los analistas** [15]:
  - en horizontes largos;
  - en empresas chicas o jóvenes;
  - cuando los analistas pronostican cambios grandes o negativos.
- En el mismo estudio, extrapolar el pronóstico a un año de los analistas fue lo más preciso a 2-3 años [15].

**2. Consenso de analistas.** Tiene ventaja de oportunidad a horizonte corto, pero trae dos sesgos opuestos según el horizonte:
- **Optimismo a 12 meses.** FactSet (5-dic-2025), sobre 2000-2024:
  - el UPA anual bottom-up del S&P 500 estimado al 31-dic del año previo superó al final en **6.2%** en promedio, y lo sobreestimó en 17 de 25 años;
  - sin 2001, 2008-2009 y 2020, el sesgo baja a **0.9%** [37].
- **Walk-down hacia metas superables.**
  - La estimación agregada del trimestre suele bajar durante los dos primeros meses. Las caídas promedio son de 1.7% (5 años), 2.1% (10), 2.6% (15) y 3.1% (20) [36]. En el 1T26 bajó 1.5% [38], y en el 2T26 y 3T26 subió.
  - Por eso la tasa de "beat" del S&P 500 es de **78%** (promedio de 5 años) y **76%** (10 años) [35].
  - Richardson, Teoh y Wysocki (2004) muestran que el pesimismo previo al anuncio surge en los noventa. Es más pronunciado cuando la empresa va a emitir acciones o sus insiders venden después del reporte [10].
  - Matsumoto (2002) encuentra que las empresas evitan sorpresas negativas por dos vías: suben las utilidades y guían a la baja [27].
  - Bartov, Givoly y Hayn (2002) documentan un **premio por cumplir o superar** aunque se logre con manejo, y ese premio anticipa el desempeño futuro [26].
- **Inferencia:** el beat es la norma. La información está en el miss, en un beat de magnitud anómala y en la guía.

**3. Modelos transversales.** Tienen cobertura universal, lo que sirve en México, donde hay pocos analistas.
- **HVZ, Hou, van Dijk y Zhang (2012)** [11].
  - Especificación: E_{i,t+τ} = a₀ + a₁A + a₂D + a₃DD + a₄E + a₅NegE + a₆AC, con τ = 1…5.
  - Las variables: A = activo total, D = dividendos, DD = dummy de pagador, NegE = dummy de pérdida y AC = accruals.
  - Se estima con datos agrupados (pooled) de los 10 años previos. Muestra: 1968-2008.
  - Es **menos preciso** que los analistas, pero con mucho menos sesgo y mayor ERC.
- **Li y Mohanram (2014)** [12]:
  - HVZ **rinde peor que el random walk**.
  - Proponen dos modelos: EP, E_{t+τ} = β₀ + β₁NegE + β₂E + β₃NegE×E, y RI, que agrega el libro B_t y los accruals totales TACC.
  - RI es **28-38% más preciso** que HVZ a 1-3 años, y hasta 45% en empresas chicas o sin cobertura. Su ERC es 18-85% mayor.
- **So (2013)** [13]:
  - Construye *characteristic forecasts* con utilidades, libro, accruals, crecimiento de activos, dividendos y precio, y con ellos predice el error del consenso.
  - Los inversionistas **sobreponderan** al consenso. La estrategia rinde **5.8% anual** fuera de muestra (9.4% en empresas de alta sensibilidad), en términos brutos.

**4. Datos de alta frecuencia y combinación.**
- Ball y Ghysels (2018) pronostican con MIDAS (regresiones con datos de frecuencia mixta) a horizontes de un trimestre o menos [14].
  - Superan al analista cuando la dispersión es alta y la empresa es chica.
  - **La combinación MIDAS + analistas supera sistemáticamente a los analistas solos.**
- **Combinar pronósticos es el resultado más robusto de toda esta literatura.**

**5. Machine learning.**
- Chen, Cho, Dou y Lev (JAR 2022) usan random forest y gradient boosting sobre datos financieros XBRL de alta dimensión, con más de 12,000 variables **(conteo no verificado; el abstract solo dice "high-dimensional detailed financial data")** [17]:
  - predicen la dirección del cambio de utilidad a un año con un AUC de **67.5-68.7%**;
  - los portafolios de cobertura rinden **5.0-9.7% anual** ajustado por tamaño, en bruto;
  - superan a los analistas.
- Cao, Jiang, Wang y Yang (JFE 2024) comparan un analista de IA con los humanos en 2001-2016 [18]:
  - la IA supera al **53.7%** de los precios objetivo;
  - "hombre + máquina" supera al **57.3%** y reduce los errores extremos;
  - el humano gana con intangibles, distress y poca información.

**6. LLMs.**
- Kim, Muhn y Nikolaev (jul-2024): GPT-4 superaba a los analistas en la dirección del cambio de utilidades. **Retirado (temporalmente, según la nota de arXiv) el 20-feb-2025**: un coautor encontró inconsistencias en datos y análisis al replicarlo [3].
- Kim y Nikolaev (JAR, en línea desde el 18-dic-2024): **retractado el 29-abr-2026** (aviso de retracción confirmado en Crossref, DOI 10.1111/1475-679x.70057). La cita textual "no reproducible ni cuantitativa ni cualitativamente" **(no verificado: Wiley dio 403)** [4].
- Van Binsbergen, Han y Lopez-Lira (RFS 2023), el benchmark de ML de sesgos del consenso: **Expresión de Preocupación** publicada en línea el 1-mar-2026 y en el número de mayo de 2026, RFS 39(5) [5]. Antecedentes: réplica crítica "Man versus Machine Learning Revisited" (Zhang, Zhu y Linnainmaa, SSRN 2024) y un corrigendum de los autores (SSRN 2025) (metadatos de Crossref).
- **Memorización.** Los LLM reproducen casi literalmente valores anteriores a su fecha de corte. Enmascarar entidades no lo evita, y "post-cutoff, we observe no recall" (Lopez-Lira, Tang y Zhu, 2025) [6].
  - Liang (SSRN 2026), con GPT-4 (corte: 30-sep-2021): el error absoluto en utilidades trimestrales es ~11% menor antes de la fecha de corte; ~18% en niveles diarios de índices y ~16% en precios mensuales. El pre-corte reduce artificialmente la brecha GPT-analista, sobre todo en trimestres de alta sorpresa (resumen confirmado vía Crossref; texto completo no leído) [9].
  - Pruebas formales de look-ahead: [7][8].
- Veredicto: **D.** El LLM lee, extrae, reconcilia y genera hipótesis con cita. No prueba capacidad predictiva antes de su fecha de corte.

### 2.3 Sorpresas, deriva y revisiones
- **SUE** = (real − esperado)/σ (o /precio). Hay dos benchmarks: el RW estacional y el consenso. La deriva es mayor con la sorpresa medida contra analistas (Livnat y Mendenhall, 2006) [21].
- **Origen.** Bernard y Thomas (1989): el diferencial entre deciles extremos de SUE fue positivo en 41 de 48 trimestres (1974-1985) **(no verificado en fuente primaria)** y decrece con el tamaño [20].
- **Muerte en las grandes.** Martineau (CFR 2022): fuera de las microcaps la deriva desapareció hacia 2006 (decimalización y negociación de alta frecuencia) [1]. Debate de 2025:
  - Dickerson-Julliard-Mueller (aceptado en JFE) y Hirshleifer-Peng-Wang (RFS 38(3), 2025; t ≈ 14) sostienen que sigue vivo.
  - Subrahmanyam (SSRN, dic-2025; reseña de UCLA Anderson del 21-ene-2026) muestra que solo sobrevive en microcaps, que son ~3% del valor de mercado. Sin ellas, el t cae a 1.43 [2].
  - Detalle en el cap. 15 §4.
- **Por qué murió.** Kettell, McInnis y Zhao (WP, 2022): la persistencia de la SUE cayó. Al controlarla, la tendencia descendente del PEAD deja de ser significativa [22]. Inferencia: hoy la sorpresa de este trimestre predice menos la del siguiente, así que hay menos que "subreaccionar".
- **Deriva por texto.** Meursault, Liang, Routledge y Scanlon (JFQA 2023) miden la sorpresa con el texto de la llamada (SUE.txt) [23]:
  - PEAD.txt, quintiles, 2010-2019: **2.87/4.61/6.51/8.01%** a 63/126/189/252 días;
  - PEAD clásico en el mismo periodo: 1.54/2.70/3.87/4.63%;
  - los rendimientos son brutos, ajustados por tamaño y B/M, antes de costos y sin réplica independiente: **C**.
- **Revisiones.**
  - Chan, Jegadeesh y Lakonishok (1996): el diferencial entre extremos de SUE es de **7.5%** a 6 meses (1973-1993) **(cifra no verificada en fuente primaria)**. Verificado en el abstract: el rendimiento pasado y la sorpresa pasada predicen cada uno una deriva grande controlando por el otro, sin reversión posterior, y los analistas también ajustan lento [19].
  - Stickel (1991): el precio deriva unos 6 meses en la dirección de la revisión **(horizonte no verificado en fuente primaria)** [25].
  - Gleason y Lee (2003): el mercado no distingue bien las revisiones con información nueva de las que solo se acercan al consenso. El ajuste es más lento con menos cobertura y con analistas precisos pero poco famosos [25].
  - Novy-Marx (2015): el momentum de utilidades **subsume** al de precio. Una estrategia de momentum de utilidades que controla por el rendimiento pasado baja su volatilidad y elimina los crashes sin perder rendimiento promedio [24].

### 2.4 Guía de la dirección
- Hutton, Lee y Shu (2012) comparan la guía anual con el analista promedio [28]:
  - la guía es más precisa ~**50%** de las veces **(no verificado: el abstract no da la cifra y SSRN dio 403)**;
  - la dirección gana en lo propio de la firma: inventarios anormales, exceso de capacidad, pérdidas;
  - el analista gana cuando la firma se mueve con la macro (PIB, energía).
- Definición operativa de FactSet: una guía es negativa si su punto medio queda debajo del consenso medio [36].
- **2025, la niebla arancelaria** (verificado en documentos presentados a la SEC, salvo donde se indica):
  - GM retiró su guía 2025 con su reporte del 1T el 29-abr-2025 (Fortune, 30-abr-2025) [52].
  - Stellantis suspendió su guía 2025 "due to tariff-related uncertainties" (6-K, 30-abr-2025) [52].
  - Cummins: "Due to growing economic uncertainty driven by tariffs we have withdrawn our full year forecast" (8-K Item 2.02, 5-may-2025) [52].
  - JetBlue no reafirmó su guía anual "given the macroeconomic uncertainty" (8-K, 29-abr-2025). No citó aranceles de forma explícita [52].
  - Mercedes-Benz: retiro por aranceles **(no verificado: no presenta ante la SEC y su sitio dio 403)**.
  - FactSet (14-abr-2025): al 10-abr-2025, 2 de las 23 empresas del S&P 500 que ya habían reportado retiraron su guía anual. Walgreens lo hizo por su venta a Sycamore, no por aranceles, y Delta por "current uncertainty" [39]. **Corrección:** era una muestra de 23 reportes en la primera semana de la temporada. No sirve para concluir que el pánico fue "de narrativa". A fines de abril y en mayo se sumaron retiros explícitos por aranceles.
- **3T 2026** (FactSet, 4-sep-2026): 70 guías positivas y 41 negativas, es decir **63%** positivas contra 41% de promedio a 5 años y 42% a 10. 44 de las 70 son de Tecnologías de la Información [36]. Al 18-sep-2026 eran 72 positivas y 43 negativas, todavía 63% [40].
- Regla: la guía vale lo que vale el **historial de promesas contra resultados** de esa dirección (expediente de 10 puntos).

### 2.5 Tono, voz y texto
- **Diccionario.** Loughran y McDonald (2011): ~**3/4** de las palabras "negativas" de Harvard no lo son en finanzas. Se usa el diccionario LM [30].
- **Voz.** Mayew y Venkatachalam (2012): el afecto vocal de los directivos anticipa el desempeño. Los analistas no lo incorporan en sus pronósticos de corto plazo, y en sus recomendaciones solo incorporan el positivo [29].
- **Engaño.** Larcker y Zakolyukina (2012): 50-65% de exactitud **(no verificado)**, 6-16% sobre el azar fuera de muestra (verificado en el abstract). Las respuestas engañosas mencionan más "lo que todos saben" y menos el valor para el accionista [31].
- **Reacción de los analistas.** Matera (arXiv, nov-2025): **sobrerreaccionan al sentimiento** y **subreaccionan a las narrativas de riesgo** [32].
- Uso: priorizar la lectura y ensanchar intervalos. No es señal de operación: grado C, sin réplica neta.

### 2.6 El estado financiero como sistema: modelo por drivers
**Ingresos** = Σ segmentos Σ geografías (volumen × precio × mezcla) × FX.
- **Conversión cambiaria.** En una emisora que reporta en MXN con una fracción w de ingresos en USD: Δ% ingresos en MXN por conversión ≈ w × Δ% del USDMXN **promedio** del trimestre. Con w = 60% y USDMXN −10%, la conversión resta ~6 pp.
- **Efecto transaccional.** Los costos en USD pueden compensar en el margen lo que la conversión quita en ingresos (cap. 16).
- Dato 2T26: Monex estimó una apreciación promedio del peso de **10.8%** contra el 2T25 (6.7% al cierre del periodo). Con ella proyectó para el IPC ventas de +6.5%, EBITDA de +12.8% y utilidad neta de +14.1%, con margen EBITDA de 23.2% contra 21.9% [45].

**Márgenes.**
- Separa costos fijos y variables. El grado de apalancamiento operativo es DOL = %ΔEBIT / %ΔVentas.
- **Márgenes récord + RW = sesgo al alza.** El margen neto del S&P 500 fue de **17.0%** en el 2T26, récord desde 2009, contra 12.4% de promedio a 5 años [36]. La reversión de márgenes es un driver, no un supuesto.

**D&A = f(capex, vidas útiles).** Cambiar la vida útil mueve la UPA sin mover la caja (§2.7).

**Capex** = mantenimiento (proxy imperfecto: D&A) + crecimiento. El programa lo anuncia la dirección y se contrasta con el historial.

**Capital de trabajo.**
- DSO = CxC/Ventas × días; DIO = Inventario/Costo × días; DPO = CxP/Costo × días.
- CCC = DSO + DIO − DPO. ΔCT ≈ (días/365) × Δventas.

**FCF** = CFO − capex − capitalización de software − principal de arrendamientos (para comparar IFRS 16 con US GAAP) − SBC (costo económico).
- La conversión es FCF/utilidad neta. Veto del cap. 03: menos de 0.7 dos años seguidos.

**Cuadre obligatorio.**
- Activo = pasivo + capital.
- Caja final del flujo = caja del balance.
- RE_t = RE_{t−1} + UN − dividendos (± otros).
- Acciones diluidas = básicas + RSU/opciones por el método de acciones en tesorería. **Recompra neta** = recompras − emisión por SBC.

### 2.7 GAAP vs non-GAAP, ganancias no operativas y estimaciones contables
- **Magnitud.** Calcbench y Suffolk (16-jul-2026) [34]:
  - **361 de 500** empresas del S&P 500 (72%) ajustaron su utilidad del ejercicio 2025;
  - la utilidad ajustada quedó **US$271 mil millones** por encima de la GAAP, y en 87% de los casos la ajustada es mayor;
  - AbbVie, Broadcom, Capital One, GM y Pfizer reportaron utilidades ajustadas varias veces mayores que las GAAP.
- **La SBC sí se ve.** McInnis y Griffin (JAE 2025) estudian más de 70,000 anuncios de 2003-2021 [33]:
  - un aumento inesperado de SBC resta **1-2 pp** de rendimiento de corto plazo;
  - el castigo es igual aunque la empresa la excluya de su cifra non-GAAP.
  - Inferencia: excluir la SBC no engaña al precio. Solo engaña al modelo propio si lo copia.
- **El trimestre de las ganancias no operativas (2T26, FactSet, 7-ago-2026)** [35]:
  - Alphabet registró **US$98 mil millones** en otros ingresos, sobre todo ganancias no realizadas en valores de capital.
  - Amazon registró **US$53.4 mil millones**, sobre todo por sus inversiones en Anthropic.
  - El crecimiento combinado del S&P 500 fue de **50.4%**, y de **32.0%** sin ellas. La sorpresa agregada fue de 29.2%, y de 10.9% sin ellas.
  - Hecho: para el 2T27 el consenso espera un crecimiento de apenas **1.2%** [36]. Inferencia: es sobre todo efecto de base por esas ganancias no operativas; FactSet no lo atribuye explícitamente.
  - Regla: el modelo separa la utilidad operativa del mark-to-market. Para cada proveedor de consenso, se verifica si su "actual" las incluye.
- **Vidas útiles** (10-K, verificado en el texto del 10-K el 25-sep-2026):
  - Meta extendió la mayoría de sus servidores y equipo de red a **5.5 años** desde el 1-ene-2025: −US$2.92 mil millones de depreciación, +US$2.59 mil millones de utilidad neta y **+US$1.00 por acción diluida** en 2025 [47].
  - Amazon subió la vida útil de sus servidores de 5 a 6 años desde el 1-ene-2024: −US$3.2 mil millones de D&A y +US$2.5 mil millones de utilidad neta en 2024. Desde el 1-ene-2025 la bajó de 6 a 5 años para un subconjunto de servidores y equipo de red, por "an increased pace of technology development, particularly in the area of artificial intelligence and machine learning". Efecto estimado: −US$0.7 mil millones de utilidad operativa en 2025, más −US$0.6 mil millones por retiros anticipados [47].
  - Brecha capex/D&A de los cuatro hyperscalers, en los cuatro trimestres a mar-2026. **Verificado con XBRL de la SEC (companyfacts, cálculo propio):**
    - El capex suma **US$433.9 mil millones**: MSFT 97.2, AMZN 151.0, GOOGL 109.9 y META 75.7. Es la compra de PP&E en efectivo, sin arrendamientos financieros.
    - La depreciación suma **~US$145-149 mil millones** según la definición. Con la de MSFT (solo depreciación) da 144.6; si se suma la amortización de sus arrendamientos financieros, 149.4.
    - El capex es ~2.9-3.0× la depreciación [42][48].
  - Burry (nov-2025) estimó una subestimación de ~US$176 mil millones de depreciación en 2026-2028 **(no verificado: solo fuentes secundarias; la fecha exacta tampoco se confirmó)** [48].
  - Inferencia: en un ciclo de capex, la UPA subestima el costo económico. El FCF y la brecha capex/D&A son la métrica de control.

### 2.8 Alertas de calidad (lo que se revisa antes de creer un número)

| Alerta | Qué indica | Dónde se ve |
|---|---|---|
| DSO sube más rápido que las ventas | Ventas empujadas al canal, crédito laxo, reconocimiento anticipado | Balance y notas de ingresos |
| Inventario crece más que el costo de ventas | Demanda más débil que lo que dice la dirección; riesgo de castigo | Balance, DIO |
| Capitalización nueva o creciente (software, costos de adquisición de clientes, intereses) | Gasto que pasa al balance | Notas de política contable, CF de inversión |
| Cambio de vida útil o de método | UPA sin caja (§2.7) | Notas de PP&E y MD&A |
| Cambio de auditor | Desacuerdo o riesgo | EUA: 8-K Item 4.01 |
| Reexpresión "Big R" (8-K Item 4.02) contra "little r" (corrección en el siguiente reporte) | Error material contra inmaterial | 8-K y notas [51] |
| Brecha non-GAAP/GAAP creciente o partidas "no recurrentes" recurrentes | Utilidad de menor calidad | Conciliación en el comunicado |
| FCF/UN < 0.7, dilución > 3%, SBC > 10% de ingresos | Vetos del cap. 03 | `dossier.py` |

Según Ideagen Audit Analytics y el CAQ (resumen del 15-jul-2024, datos a 2023), el número de reexpresiones está cerca de mínimos históricos: 458 en 2022 y 430 en 2023. Pero las **Big R subieron** de 191 a 209, y su proporción de 44% a 52% [51]. El M-score, los accruals y el F-score están en el cap. 03 §2.10.

### 2.9 Política y geopolítica dentro del modelo
Cadena causal obligatoria: acontecimiento → exposición → efecto económico → **línea del estado financiero** → valuación → diferencia contra lo que descuenta el precio. Mapeo de hechos verificados de 2025-2026:

| Hecho (fecha, fuente) | Línea que mueve | Cómo entra al modelo |
|---|---|---|
| Aranceles de 2025: retiros de guía (abr-may 2025) [39][52] | Costo, precio, volumen | Escenarios con arancel explícito; intervalos más anchos cuando no hay guía |
| Petróleo del 3T26 (promedio a la fecha) en US$81.45 contra US$64.97 del 3T25 (+25%); se espera que Energía crezca **102.5%** [36] | Precio (energía) y costo (transporte, químicos, aerolíneas) | Sensibilidad por cada US$10/barril, separada por sector |
| T-MEC: en la reunión de la Comisión de Libre Comercio del 1-jul-2026, la USTR no aceptó la extensión automática a 16 años (art. 34.7) y activó las revisiones anuales. El tratado sigue vigente; siguiente ronda anunciada para el 20-jul-2026 en México (El Financiero, 2-jul-2026) [46] | Tasa de descuento, capex de nearshoring, volumen exportador | Prima de incertidumbre en exportadores y parques industriales. Inferencia: menos visibilidad = más guías conservadoras en México |
| Peso: apreciación promedio de 10.8% en el 2T26 contra el 2T25 (Monex) [45] | Conversión de ingresos USD → MXN | w × Δ%USDMXN promedio (§2.6) |
| SEC: propuesta de reporte semestral opcional (Form 10-S; Release 33-11414, 5-may-2026; comentarios hasta el 6-jul-2026). Al 25-sep-2026 la página de rulemaking de la SEC la lista como "Proposed Rule" (S7-2026-15), sin regla final [41] | Frecuencia de información | Si se adopta: 2 datos al año en lugar de 4, sorpresas más grandes y 1T/3T solo por 8-K voluntario. El pronóstico se ajusta al régimen de cada emisora |
| IFRS 18 (emitida en abr-2024), vigente para ejercicios que inicien desde el 1-ene-2027: subtotales obligatorios de "utilidad de operación" y "utilidad antes de financiamiento e impuestos"; medidas de desempeño definidas por la administración (MPM) reveladas en notas, que quedan dentro de los estados auditados; los comparativos 2026 se reexpresan (aplicación retrospectiva) [49] | Presentación del resultado de las emisoras IFRS (México) | Ruptura de series: rehacer el mapeo XBRL y no comparar 2027 contra 2026 sin reexpresión |

Ventaja del dueño (ex funcionario federal): la lectura de calendarios regulatorios, concesiones, tarifas reguladas y contratos públicos (cap. 24) es un driver legítimo **con información pública**. La LMV sanciona el uso de información privilegiada. El edge legal es interpretar mejor y antes lo que ya es público.

### 2.10 Valuación por escenarios y DCF inverso
- **Valor esperado** = Σ pᵢVᵢ, con Σpᵢ = 1. También se reporta E[ln(V/P)], que es lo que capitaliza (criterio geométrico del objetivo del sistema).
- **Ejemplo** (cálculo propio): precio 100; bear 70 (25%), base 105 (50%), bull 150 (25%).
  - EV = **107.5** (+7.5%) y E[ln] = +3.7%.
  - **No pasa** la regla de compra del cap. 03 §6.1: el precio de 100 supera 0.8 × 105 = 84. Con un EV positivo no alcanza.
- **DCF inverso** (cálculo propio): precio 100, FCF por acción de 3 (rendimiento FCF de 3%), 10 años explícitos y g terminal de 3%.
  - Crecimiento anual implícito del FCF: **9.1% / 11.7% / 14.0%** con WACC de 8% / 9% / 10%.
  - El terminal pesa 63-68% del valor.
  - Lección: **100 pb de WACC mueven 2.3-2.6 pp de crecimiento implícito**. Discutir la tasa es discutir la expectativa.
- El crecimiento implícito se compara con las tasas base del sector y el tamaño (cap. 03 §2.7). Solo hay oportunidad cuando el escenario propio difiere del implícito **por un driver fechado y medible**.

---

## 3. Literatura canónica

| Autores | Año | Título | Revista | Hallazgo cuantificado | Enlace | Grado |
|---|---|---|---|---|---|---|
| Bernard, Thomas | 1989 | Post-Earnings-Announcement Drift: Delayed Price Response or Risk Premium? | JAR 27 | Diferencial entre extremos de SUE positivo en 41/48 trimestres (1974-85) (no verificado); cae con el tamaño | [20] | A (histórico) |
| Stickel | 1991 | Common Stock Returns Surrounding Earnings Forecast Revisions | TAR | El precio deriva ~6 meses tras la revisión (no verificado) | [25] | B (histórico) |
| Chan, Jegadeesh, Lakonishok | 1996 | Momentum Strategies | JF 51(5) | 7.5% a 6 meses entre extremos de SUE (1973-93) (no verificado); momentum de precio y de utilidades predicen por separado (abstract) | [19] | A (histórico) |
| Bartov, Givoly, Hayn | 2002 | The Rewards to Meeting or Beating Earnings Expectations | JAE 33 | Premio por cumplir o superar aun con manejo; anticipa desempeño | [26] | B |
| Matsumoto | 2002 | Management's Incentives to Avoid Negative Earnings Surprises | TAR 77(3) | Guía a la baja y manejo de utilidades para no fallar | [27] | B |
| Gleason, Lee | 2003 | Analyst Forecast Revisions and Market Price Discovery | TAR 78 | Subreacción mayor a revisiones de alta innovación y con poca cobertura | [25] | B |
| Richardson, Teoh, Wysocki | 2004 | The Walk-down to Beatable Analyst Forecasts | CAR 21(4) | Pesimismo previo al anuncio desde los 90; mayor si la empresa o sus insiders venden | [10] | A |
| Livnat, Mendenhall | 2006 | Comparing the PEAD for Surprises from Analyst and Time Series Forecasts | JAR 44(1) | Deriva mayor con la sorpresa medida contra analistas | [21] | B |
| Loughran, McDonald | 2011 | When Is a Liability Not a Liability? | JF 66 | ~3/4 de las palabras negativas de Harvard mal clasificadas en finanzas | [30] | A |
| Hou, van Dijk, Zhang | 2012 | The Implied Cost of Capital: A New Approach | JAE 53 | Modelo transversal con menos sesgo y más ERC, pero menos preciso que los analistas | [11] | C |
| Mayew, Venkatachalam | 2012 | The Power of Voice | JF 67(1) | El afecto vocal anticipa el desempeño; los analistas ignoran el negativo | [29] | C |
| Larcker, Zakolyukina | 2012 | Detecting Deceptive Discussions in Conference Calls | JAR 50(2) | 50-65% de exactitud (no verificado); 6-16% sobre el azar fuera de muestra | [31] | C |
| Hutton, Lee, Shu | 2012 | Do Managers Always Know Better? | JAR 50(5) | La guía supera al analista ~50% de las veces (no verificado); la dirección gana en lo propio de la firma y el analista en lo macro (abstract) | [28] | B |
| Bradshaw, Drake, Myers, Myers | 2012 | A Re-examination of Analysts' Superiority over Time-Series Forecasts | RAST 17(4) | El RW supera al analista a largo plazo, en empresas chicas o jóvenes y en cambios grandes | [15] | A |
| So | 2013 | A New Approach to Predicting Analyst Forecast Errors | JFE 108(3) | Los inversionistas sobreponderan al consenso; 5.8% anual fuera de muestra (bruto) | [13] | B |
| Gerakos, Gramacy | 2013 | Regression-Based Earnings Forecasts | WP SSRN | A un año, el RW iguala a métodos sofisticados | [16] | A |
| Li, Mohanram | 2014 | Evaluating Cross-Sectional Forecasting Models for ICC | RAST 19(3) | HVZ < RW (errores del RW 13-37% menores); RI 28-38% más preciso que HVZ a 1-3 años, hasta 45% en chicas; ERC 18-85% mayor | [12] | B |
| Novy-Marx | 2015 | Fundamentally, Momentum Is Fundamental Momentum | NBER w20984 | El momentum de utilidades subsume al de precio | [24] | B |
| Ball, Ghysels | 2018 | Automated Earnings Forecasts: Beat Analysts or Combine and Conquer? | MS 64(10) | A un trimestre o menos, MIDAS supera al analista con alta dispersión o en empresas chicas; combinar supera sistemáticamente al analista solo | [14] | B |
| Chen, Cho, Dou, Lev | 2022 | Predicting Future Earnings Changes Using ML and Detailed Financial Data | JAR 60(2) | AUC 67.5-68.7%; cobertura 5.0-9.7% anual (bruto) | [17] | B |
| Martineau | 2022 | Rest in Peace Post-Earnings Announcement Drift | CFR 11(3-4) | Sin PEAD en grandes desde 2006 | [1] | A |
| Kettell, McInnis, Zhao | 2022 | Why Has PEAD Declined Over Time? | WP UT Austin | La caída de la persistencia de SUE explica la caída del PEAD | [22] | C |
| Meursault et al. | 2023 | PEAD.txt | JFQA 58(6) | 8.01% contra 4.63% a 252 días (2010-19, bruto) | [23] | C |
| van Binsbergen, Han, Lopez-Lira | 2023 | Man versus Machine Learning: The Term Structure of Earnings Expectations and Conditional Biases | RFS 36(6) | Consenso sesgado al alza según el benchmark de ML. **Expresión de Preocupación: en línea 1-mar-2026, RFS 39(5), may-2026** | [5] | D hasta resolverse |
| Cao, Jiang, Wang, Yang | 2024 | From Man vs. Machine to Man + Machine | JFE 160 | IA > 53.7% de los precios objetivo de analistas (2001-16); hombre + máquina 57.3% (cifras del documento de trabajo) | [18] | B |
| Kim, Muhn, Nikolaev | 2024 | Financial Statement Analysis with LLMs | arXiv 2407.17866 | **Retirado el 20-feb-2025** | [3] | D |
| Kim, Nikolaev | 2024 | Context-Based Interpretation of Financial Information | JAR | **Retractado el 29-abr-2026**: no reproducible | [4] | D |
| Lopez-Lira, Tang, Zhu | 2025 | The Memorization Problem | arXiv 2504.14765 | Recuerdo casi literal antes de la fecha de corte; nulo después | [6] | B |
| Liang | 2026 | Look-Ahead Bias in Financial Forecasts Generated by LLMs | SSRN 6772819 | GPT-4: error ~11% menor pre-corte en utilidades trimestrales; ~18% en índices y ~16% en precios | [9] | C (un estudio, sin réplica) |
| McInnis, Griffin | 2025 | Gone but Not Forgotten | JAE | SBC inesperada: −1 a −2 pp, aunque se excluya | [33] | B |

---

## 4. Lo más reciente 2023-2026 (con fecha)

1. **La literatura de IA en pronóstico de utilidades se cayó en 2025-2026** (retiro, retracción y Expresión de Preocupación; §2.2) [3][4][5]. Queda en pie Cao et al. (2024), cuyo mensaje es hombre + máquina [18]. Todo resultado de "IA le gana al analista" exige código, datos *point-in-time* y periodo posterior a la fecha de corte.
2. **Pruebas de look-ahead** [6][8]. Look-Ahead-Bench (Benhenda, 20-ene-2026, arXiv 2601.13770) es una de las fuentes que citó el rival, y se verificó que existe [7].
3. **PEAD.** El debate de 2025 se resume en §2.3 y en el cap. 15 [2].
4. **SBC y non-GAAP**: ver §2.7 [33][34].
5. **Consenso 2026.**
   - Al 5-dic-2025, el UPA bottom-up de 2026 era de US$309.22 [37]. Al 31-ago-2026 era de **US$361.38**, +6.1% solo en jul-ago [36]. Frente al estimado de diciembre, eso es **+16.9%** (cálculo propio).
   - Es lo contrario de la tasa base de sobreestimación de 6.2%.
   - Inferencia: una parte relevante viene de ganancias no operativas del 2T26 y del ciclo de IA y energía. Las tasas base se rompen por régimen, y la de sobreestimación no se aplica mecánicamente.
6. **Temporada 2T26 en EUA** (FactSet, 7-ago y 4-sep-2026) [35][36]: 86-87% superó el UPA estimado (promedio de 5 años: 78%) y 76-77% superó en ingresos (5 años: 70%).
7. **3T26** [36]:
   - La estimación **subió** 1.2% (US$88.64 → US$89.69) en jul-ago, contra la caída promedio de 1.7% a 5 años. Es el segundo trimestre seguido al alza.
   - Crecimiento esperado: 28.5% (26.6% al 30-jun). P/U a 12 meses: 19.5 (promedio de 5 años: 19.8).
   - Los analistas subieron estimaciones pese a la preocupación por el precio del petróleo.
   - Actualización al 18-sep-2026, verificada en el PDF de FactSet: crecimiento esperado de 28.9% (el dato al 30-jun se revisó a 26.7%) y P/U a 12 meses de 19.1. Guías: 72 positivas y 43 negativas, 63% [40].
8. **Temporada 2T26 en México.**
   - Monex (14-jul-2026) esperaba en el IPC ventas de +6.5%, EBITDA de +12.8% y utilidad neta de +14.1%, con fecha límite de reporte el 28-jul [45].
   - El Financiero (20-jul-2026) calificó los primeros reportes de "balances modestos" [45]. Hay que separar dato reportado de estimado:
     - **Aeroméxico, reportado:** el flujo operativo cayó 35.5% en el 2T26. El diario lo atribuye a que el segmento corporativo no viajó en junio por el Mundial 2026. Es un ejemplo de un evento que pega en el trimestre de un sector que parecía beneficiado.
     - **Chedraui, estimado:** ingresos −0.9% y utilidad neta −0.8%. Es la **estimación de Ve por Más**, no un resultado.
     - **GAP, preliminar:** ingresos +3.7% y flujo operativo ~+9%, en condicional ("se habrían expandido").
   - Resumen del reporte de cierre de Monex (27-jul-2026): ventas del IPC +4.9% y EBITDA +12.1%; 22.0% de las emisoras arriba de lo estimado, 54.3% en línea y 25.7% abajo. **(No verificado: el PDF volvió a dar 403 el 25-sep-2026 y los porcentajes suman 102%, así que al menos una cifra está mal transcrita. No se usa como tasa base.)**
9. **Regulación y T-MEC** (detalle en §2.9).
   - SEC: Release 33-11414 (5-may-2026) propone el Form 10-S con plazo de 40/45 días e Inline XBRL [41].
   - IFRS 18 [49].
   - T-MEC con revisiones anuales [46], que restan visibilidad a la guía de los exportadores mexicanos (cap. 11/23).

---

## 5. Evidencia real: qué funciona, qué no, neto

### 5.1 Catálogo

| Señal o método | Evidencia | Grado | ¿Implementable neto desde GBM? | Qué no demuestra |
|---|---|---|---|---|
| El consenso como benchmark de corto plazo | [10][15][35] | A | Sí, como referencia | Que batirlo dé rendimiento |
| RW a 1 año / extrapolar el consenso a 2-3 años | [15][16] | A | Sí | Que sirva en cambios de régimen |
| Optimismo a 12 meses y walk-down | [10][36][37] | A | Sí, como corrección de lectura | Que se cumpla cada año (2026 lo rompió) |
| EP/RI como ancla neutral | [12] | B | Sí (datos XBRL gratuitos) | Alfa por sí mismo |
| Error predecible del consenso (So) | [13] | B en muestra, C hoy | Difícil: requiere historia de I/B/E/S | Supervivencia después de 2013 |
| Combinación (MIDAS + analistas; hombre + máquina) | [14][18] | B | Parcial: datos mensuales públicos | Rendimiento neto |
| ML con XBRL detallado | [17] | B | Laboratorio | Réplica independiente neta de costos |
| LLM como pronosticador | [3][4][5][6] | D | No, como evidencia | Cualquier cosa antes de la fecha de corte |
| PEAD clásico en grandes | [1] | D (muerto desde 2006) | No | — |
| PEAD en microcaps | [2] | C bruto | No: costo y liquidez | Neto de costos |
| PEAD.txt | [23] | C | No probado | Réplica fuera de 2010-2019 |
| Momentum de revisiones | [19][24][25] | B histórico, C hoy | Solo como filtro | Magnitud después de 2015 (no verificada) |
| Tono y voz | [29][31][32] | C | Como alerta | Rendimiento neto |
| Premio por cumplir o superar | [26] | B | Ya descontado | Que el beat de hoy sea información |
| La SBC reduce el valor | [33] | B | Sí, en el modelo | — |

Costos: desde el SIC, la ida y vuelta cuesta ~0.58% (cap. 15). Cualquier señal de reporte con menos de 1% de alfa bruto por evento queda muerta al neto.

### 5.2 Tasas base que calibran los pronósticos propios
- **"¿Supera el consenso de UPA?"** en el S&P 500: 76-78% (FactSet, 10 y 5 años) [35].
  - Un pronosticador que siempre dice 0.78 obtiene un Brier de 0.78 × 0.22 = **0.172**.
  - Eso **ya cumple** `pronosticos.brier_objetivo = 0.20` sin saber nada.
  - Conclusión: en este tipo de preguntas el objetivo de 0.20 es **necesario pero no suficiente**. Se exige skill contra la tasa base (§6.5).
- **Ingresos** en el S&P 500: 68-70%, con Brier de referencia de ~0.21-0.22 [35].
- **México, 2T26:** ~22% "arriba" con la definición de Monex **(no verificado; la fuente suma 102%)**. Si se confirmara, el Brier de referencia sería ~0.17. Hasta verificarlo con el PDF, no se usa como tasa base; se construye la propia con los reportes de Emisnet.
  - Inferencia: con pocos analistas y una banda de "en línea", el juego del walk-down es menos visible.
  - No se importa la tasa de EUA a México.
- **Guía positiva del 3T26:** 63% contra 41-42% histórico [36]. Una tasa base se actualiza con el régimen, no se fija para siempre.

### 5.3 Lo que el 2T26 enseña
- En el agregado, la sorpresa fue de 29.2%. Sin dos empresas, fue de 10.9% [35].
- Un sistema que pronostica "Street EPS" sin separar las ganancias por valuación de inversiones habría registrado ese "beat" como acierto operativo. Fue contabilidad a valor razonable.
- **Regla:** cada pronóstico declara la base: GAAP, ajustada del proveedor o ajustada de la empresa.

---

## 6. Traducción operable

En fase 0 (`prioridad_actual.fase = 0`) nada de esto genera operaciones reales. Genera dossiers, pronósticos registrados y su evaluación.

### 6.1 Protocolo del dossier estándar (se integra en `empresas/<TICKER>/ficha.md` con la skill `ficha-empresa`)

| Momento | Tarea | Herramienta o fuente |
|---|---|---|
| T−30 (o al entrar al universo) | Datos de 8 trimestres y 5 años; segmentos y geografía; modelo por drivers (§6.2); matriz de exposición política y geopolítica (§2.9); historial de promesas contra resultados; DCF inverso | EUA: `python3 herramientas/dossier.py TICKER` (y `edgar.py --periodo trimestral`). México: Emisnet/BMV XBRL, comunicado de RI y 20-F/6-K si reporta a la SEC (`--edgar-ticker`) |
| T−10 | Actualizar drivers con datos de alta frecuencia: FX promedio del trimestre, commodities, datos sectoriales mensuales publicados (p. ej., tráfico mensual de los grupos aeroportuarios, ANTAD en autoservicio) | Lógica MIDAS [14] |
| T−2 | **Congelar el pronóstico**: puntos e intervalo de 80% más binarios; foto del consenso con fuente, fecha y hora | `herramientas/pronosticos.py` y `empresas/<T>/pronosticos.csv` |
| T0 | Leer el comunicado: conciliación non-GAAP, partidas no operativas, FCF, guía contra consenso, alertas §2.8 | 8-K Item 2.02 / Emisnet |
| T+1 | Registrar la reacción; **no operar PEAD en grandes** [1]; actualizar escenarios con fecha, sin sobrescribir | Ficha |
| T+10 a T+45 | Llegan el 10-Q o el reporte CNBV con XBRL: conciliar y resolver los pronósticos numéricos; post-mortem | skill `post-mortem` |

### 6.2 Plantilla mínima del modelo de tres estados

| Bloque | Driver | Regla |
|---|---|---|
| Ingresos | Volumen, precio, mezcla y FX por segmento | Cada driver con fuente y un rango; FX con **promedio** del periodo, no cierre |
| Margen bruto | Costo variable por unidad; insumos en USD | Sensibilidad ±10% en el insumo principal |
| Gastos de operación | Fijo + variable; SBC separada | La SBC se trata como gasto |
| D&A | Capex histórico / vida útil | Cualquier cambio de vida útil se modela aparte |
| Financiamiento | Deuda por moneda y vencimiento; tasa | Cruce con cap. 04/16 |
| Impuestos | Tasa efectiva de 3 años; cambios de ley | Riesgo fiscal explícito |
| Balance | DSO, DIO, DPO; capex; deuda | ΔCT derivado de días |
| Flujo | CFO − capex − arrendamientos − SBC | Conversión FCF/UN |
| Acciones | Diluidas, recompra neta | Dilución neta anual |
| Cuadre | Balance cuadra, caja concilia | Sin cuadre no hay pronóstico |

Principio de parsimonia: 5 a 8 drivers explican casi todo. Un modelo de 60 líneas con supuestos no documentados es falsa precisión.

### 6.3 Checklist de alertas con umbrales (heurísticos, del sistema)
- [ ] ΔDSO interanual > +10% **y** mayor que el crecimiento de ventas.
- [ ] Crecimiento del inventario > crecimiento del costo de ventas + 10 pp.
- [ ] Nueva capitalización, o una que crece más que los ingresos.
- [ ] Cambio de vida útil, de método o de estimación con efecto > 3% de la UPA.
- [ ] Cambio de auditor, 8-K Item 4.02, o debilidad material de control.
- [ ] Utilidad ajustada > 1.3 × GAAP en 2 de los últimos 4 trimestres.
- [ ] Vetos del cap. 03: FCF/UN < 0.7 dos años, dilución neta > 3% o SBC > 10% de ingresos.
- [ ] Partidas no operativas > 10% de la utilidad del trimestre.

Dos o más alertas: la tesis se veta hasta que el comité (skill `comite-de-inversion`) documente una excepción.

### 6.4 Formato de registro del pronóstico previo al reporte

**Binarios** en `bitacora/pronosticos.csv` (el formato ya existe), con criterio exacto:
```
python3 herramientas/pronosticos.py agregar \
  --pregunta "¿UPA ajustada 3T26 de <EMISORA> > consenso 1.23 (Yahoo, 2026-10-20 18:00 CT)?" \
  --probabilidad 0.72 --fecha-resolucion 2026-10-28 \
  --criterio "UPA ajustada del comunicado 8-K > 1.23; empate = no; base ajustada" \
  --autor claude --notas "tasa base 0.78; mi punto 1.27 [1.15,1.36]"
```

Plantillas de preguntas:
- (a) ¿UPA > consenso?
- (b) ¿Ingresos > consenso?
- (c) ¿Punto medio de la guía del siguiente periodo > consenso?
- (d) ¿Margen bruto > año anterior?
- (e) ¿Reacción del cierre T−1 → T+1 > 0? Su tasa base es de ~50% y es la más difícil.

**Numéricos** en `empresas/<TICKER>/pronosticos.csv`. Columnas propuestas:
```
id,fecha_creacion,emisora,periodo,metrica,base,punto,p10,p90,consenso,fuente_consenso,hora_consenso,real,fuente_real,fecha_resuelto,notas
```

Reglas del registro:
- **No se sobrescribe nunca.** Una revisión va en una fila nueva con su fecha.
- La base (GAAP, ajustada de la empresa o del proveedor) se declara y se resuelve con la **misma** fuente del consenso.
- En México, el consenso publicado por casas de bolsa (Monex, Banorte, BX+) se registra con fecha y el número de analistas cuando se conozca.

### 6.5 Evaluación del propio pronóstico
- **Binarios.**
  - Brier = media de (p − o)². Skill contra la tasa base: BSS = 1 − Brier/[p̄(1 − p̄)], donde p̄ es la tasa base **histórica** del tipo de pregunta (§5.2).
  - **Corrección (verificado en el código el 25-sep-2026):** `pronosticos.py puntuar` calcula la skill contra la **climatología de la propia muestra**, es decir, la frecuencia observada de "sí" entre los pronósticos resueltos. No la calcula contra la tasa base histórica, y agrupa por autor, no por tipo de pregunta. Hasta que se agregue la tasa base histórica por tipo, el BSS contra 0.78 (UPA) o 0.70 (ingresos) se calcula aparte.
  - Se evalúa por tipo de pregunta y con un mínimo de `pronosticos.min_pronosticos_para_evaluar` = 50.
- **Numéricos.**
  - Error escalado por precio: |F − A|/P. Se usa en lugar del error porcentual cuando |A| es chico o está cerca de cero.
  - Error porcentual absoluto |F − A|/|A|, solo para ingresos.
  - **Precisión relativa**: fracción de casos con |F − A| < |consenso − A|.
- **Intervalos de 80%.**
  - La cobertura esperada es de 80%.
  - Con n = 50 son aceptables **34 a 45** aciertos (68-90%); con n = 20, de 12 a 19. Son rangos binomiales centrales de 95%, cálculo propio.
  - Se complementa con el *interval score* de Gneiting y Raftery (2007), que penaliza el ancho y los fallos [50]: IS = (u − l) + (2/α)(l − y)·1{y < l} + (2/α)(y − u)·1{y > u}, con α = 0.2.
- **Recomendación: criterio para que un pronóstico propio influya en una decisión** (fase ≥ 1):
  - ≥ 50 binarios resueltos con BSS ≥ 0.05 e intervalo bootstrap de 90% por encima de cero;
  - ≥ 30 numéricos con precisión relativa contra el consenso ≥ 55% (prueba de signo, p < 0.05);
  - cobertura de intervalos dentro de la banda binomial;
  - además, el Brier ≤ 0.20 de la configuración.

### 6.6 Dimensionamiento alrededor de un reporte (solo después de la fase 0)
- El stop **no protege** contra el hueco (gap) del día del reporte.
- Regla: tamaño ≤ riesgo_por_operación / |percentil 5 del movimiento histórico de la emisora el día del reporte|.
  - Arena: 3% / 12% = 25%, bajo el tope de 30% por acción.
  - Patrimonio estándar: 1% / 12% = 8.3%, bajo el tope de 10%.
- Máximo de 8 operaciones al mes en la arena. Una apuesta binaria al reporte gasta una.
- En el satélite, ningún evento de resultados entra como estrategia sin cumplir `validacion_estrategias`.

### 6.7 Datos: SEC y México
- **SEC (data.sec.gov)** [42]:
  - `companyfacts/CIK##########.json` trae todos los hechos XBRL de una empresa.
  - `frames/us-gaap/<concepto>/USD/CY2019Q1I.json` da un corte transversal del hecho "last filed" que mejor se ajusta al periodo calendario.
  - Retraso de menos de un minuto; `companyfacts.zip` se recompila cada noche. Límites: ≤ 10 solicitudes/s y User-Agent con correo.
- **Limitaciones:**
  - El comunicado del 8-K Item 2.02 no trae los estados en XBRL; llegan con el 10-Q/10-K. **Verificado en la norma**: 17 CFR 229.601(b)(101) exige el Interactive Data File en un 8-K solo cuando trae estados anuales auditados reexpresados (operación discontinuada, cambio de segmentos o de principio contable). El 8-K solo etiqueta la portada (Exhibit 104). Ejemplo: el 8-K Item 2.02 de Cummins del 5-may-2025 trae un XBRL con una sola vista (portada) y los estados en el Exhibit 99 en HTML.
  - `edgar.py` usa solo hechos no dimensionales, así que los segmentos se leen de la nota.
  - `frames` da el último valor presentado, con reexpresiones. Para evitar el look-ahead se usa la fecha `filed`.
- **México:**
  - Plazo (Circular Única de Emisoras, art. 33): 20 días hábiles tras el 1T-3T y 40 tras el 4T, que es preliminar. Está verificado en el resumen de la BMV, un documento de 2017; vigencia actual no re-verificada contra el DOF [44].
  - Se entrega por STIV-2 (CNBV) y Emisnet (BMV).
  - XBRL IFRS en archivos `ifrsxbrl_<clave>_<año>-<trimestre>`. **Obligatorio desde el 1T16 (no verificado):** solo lo sostiene una fuente secundaria (ITAM, 503 el 25-sep-2026). Las páginas de la BMV y la CNBV no dan la fecha de entrada en vigor, y el buscador histórico de la BMV muestra archivos desde 2017 [43].
  - El comunicado de RI sale antes que el XBRL. IFRS 18 obligará a rehacer el mapeo.
- **IA:** el LLM extrae y cita página; nunca aporta cifras de memoria (cap. 03 §6.1 regla 10).

---

## 7. Trampas

1. **Comparar bases distintas:** GAAP contra consenso ajustado, o "actual" de un proveedor contra consenso de otro.
2. **Celebrar el beat.** Con el walk-down, 76-78% de las empresas lo logra. Lo informativo es el miss, la magnitud anómala o la guía.
3. **Un Brier "bueno" por tasa base.** Decir 0.78 siempre ya da 0.172. Sin BSS no hay skill.
4. **Aplicar la tasa base de sobreestimación en un régimen que la rompe.** En 2026 el consenso anual subió ~17% desde diciembre.
5. **Contar ganancias por valuación de inversiones como operación** (2T26: Alphabet y Amazon).
6. **Ignorar vidas útiles y capitalizaciones.** La UPA sube sin caja (Meta: +US$1.00 por acción diluida en 2025; Amazon: +US$2.5 mil millones de utilidad neta en 2024).
7. **Excluir la SBC y la dilución.** El mercado la castiga aunque la empresa la excluya [33].
8. **Convertir con el FX de cierre** en lugar del promedio, o confundir el efecto de conversión con el transaccional.
9. **Márgenes récord + random walk.** Se extrapola un pico (margen neto récord de 17.0% en el 2T26).
10. **LLM con memoria.** Backtests "brillantes" antes de la fecha de corte; papers retirados usados como evidencia.
11. **Operar PEAD en grandes, o en microcaps** que no se pueden operar desde el SIC.
12. **Falsa precisión:** modelos de 60 líneas con supuestos no documentados; valores puntuales sin intervalo.
13. **Creer en una guía sin historial**, o no ajustar los intervalos cuando la empresa retira la guía.
14. **Olvidar el régimen regulatorio:** reporte semestral opcional, IFRS 18 y revisiones anuales del T-MEC rompen la comparabilidad y la frecuencia.
15. **Sobrescribir un pronóstico o resolverlo con otra fuente.** Eso es sesgo retrospectivo.
16. **Tratar el consenso mexicano como el de EUA:** pocos analistas, datos gratuitos atrasados, otra definición de "en línea".

---

## 8. Examen de titulación

1. **¿Por qué un beat del 2T26 con 86-87% de las empresas arriba del consenso no es una señal positiva?**
   Porque el promedio histórico es de 76-78% por el walk-down [10][35]. Además, la sorpresa agregada de 29.2% bajaba a 10.9% sin las ganancias no operativas de dos empresas.
2. **Según Li y Mohanram, ¿qué modelo transversal usar y por qué no HVZ?**
   EP o RI. HVZ rinde peor que el random walk, y RI es 28-38% más preciso que HVZ a 1-3 años [12].
3. **¿En qué condiciones el random walk supera al analista?**
   En horizontes largos, en empresas chicas o jóvenes y en cambios grandes o negativos [15].
4. **¿Cuál es el estado de la evidencia de "LLM supera al analista" al 25-sep-2026?**
   D. KMN se retiró el 20-feb-2025 y Kim-Nikolaev fue retractado el 29-abr-2026. Van Binsbergen et al. está en Expresión de Preocupación desde el 1-mar-2026 (en línea; número de mayo de 2026). La memorización está documentada: Liang estima un error ~11% menor antes de la fecha de corte en utilidades trimestrales [3][4][5][6][9].
5. **Calcule el Brier de referencia para "¿UPA > consenso?" en el S&P 500 y diga qué implica para el objetivo de 0.20.**
   0.78 × 0.22 = 0.172. El objetivo se cumple sin saber nada, así que se exige BSS > 0 contra la tasa base.
6. **Una emisora reporta en MXN con 60% de ingresos en USD y el USDMXN promedio cae 10%. ¿Cuál es el efecto de conversión?**
   ≈ −6 pp en ingresos. El margen depende de los costos en USD.
7. **¿Qué explica la desaparición del PEAD además del arbitraje?**
   La menor persistencia de la SUE (Kettell-McInnis-Zhao). Martineau la fecha en 2006 para las grandes [1][22].
8. **¿Cuánto rindió PEAD.txt contra PEAD a 252 días y qué grado tiene?**
   8.01% contra 4.63% en 2010-2019, en bruto. Grado C: un estudio, sin costos y sin réplica [23].
9. **Meta extendió sus vidas útiles a 5.5 años. ¿Qué efecto tuvo y qué se hace en el modelo?**
   −US$2.92 mil millones de depreciación, +US$2.59 mil millones de utilidad neta y +US$1.00 por acción diluida en 2025. El cambio se modela aparte, se mira el FCF y la brecha capex/D&A (~3× en los cuatro hyperscalers a mar-2026) [47].
10. **Precio 100; escenarios 70/105/150 con probabilidades de 25/50/25. ¿Cuál es el EV y pasa la regla del cap. 03?**
    El EV es 107.5. No pasa, porque el precio de 100 supera 0.8 × 105 = 84.
11. **DCF inverso con FCF de 3, g terminal de 3% y WACC de 9%: ¿qué crecimiento implica y cuánto cambia con ±100 pb?**
    11.7% anual por 10 años; 9.1% con 8% de WACC y 14.0% con 10%.
12. **¿Qué propone la SEC el 5-may-2026 y qué cambia para el pronosticador?**
    Un Form 10-S semestral opcional, con Q1 y Q3 solo por 8-K voluntario. Habría menos datos y sorpresas mayores. La regla no es final.
13. **¿Qué plazo tiene una emisora de la BMV para su reporte del 3T y dónde se obtiene el XBRL?**
    20 días hábiles (40 en el 4T). Se obtiene de Emisnet/BMV, archivo `ifrsxbrl_<clave>_<año>-<trim>` [43][44].
14. **¿Cuándo influye un pronóstico propio en una decisión?**
    Con ≥ 50 binarios y BSS ≥ 0.05 (intervalo bootstrap > 0), ≥ 30 numéricos con precisión relativa ≥ 55% contra el consenso, cobertura de intervalos dentro de la banda binomial y Brier ≤ 0.20.
15. **¿Por qué el stop no limita el riesgo de un reporte y cómo se dimensiona?**
    Por el hueco (gap). Tamaño ≤ riesgo / |P5 del movimiento del día del reporte|; por ejemplo, 3%/12% = 25% en la arena.

---

## 9. Fuentes

[1] Martineau, C. (2022). Rest in Peace Post-Earnings Announcement Drift. *Critical Finance Review* 11(3-4), 613-646. https://www.nowpublishers.com/article/Details/CFR-0122 · https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3111607
[2] Subrahmanyam, A. (2025). Keeping it Simple: How Can Post-Earnings Return Drift Exist and Not Exist Simultaneously? https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5930255 · UCLA Anderson Review: https://anderson-review.ucla.edu/is-post-earnings-announcement-drift-a-thing-again/
[3] Kim, A., Muhn, M., Nikolaev, V. Financial Statement Analysis with Large Language Models, arXiv 2407.17866 (v3 del 20-feb-2025, retirado). https://arxiv.org/abs/2407.17866
[4] Retracción de Kim, A. G. y Nikolaev, V. V., Context-Based Interpretation of Financial Information, *JAR* (29-abr-2026). https://onlinelibrary.wiley.com/doi/10.1111/1475-679x.70057
[5] van Binsbergen, J., Han, X., Lopez-Lira, A. (2023). Man versus Machine Learning: The Term Structure of Earnings Expectations and Conditional Biases. *RFS* 36(6), 2361-2396. https://academic.oup.com/rfs/article/36/6/2361/6782974 · Expresión de Preocupación, *RFS* 39(5), 1555 (en línea 1-mar-2026; impresa may-2026; DOI 10.1093/rfs/hhag017): https://academic.oup.com/rfs/article/39/5/1555/8502599
[6] Lopez-Lira, A., Tang, Y., Zhu, M. (2025). The Memorization Problem: Can We Trust LLMs' Economic Forecasts? https://arxiv.org/abs/2504.14765
[7] Benhenda, M. (2026). Look-Ahead-Bench. https://arxiv.org/abs/2601.13770
[8] Gao, Z., Jiang, W., Yan, Y. (2025). Detecting Lookahead Bias in LLM Forecasts. https://arxiv.org/abs/2512.23847
[9] Liang, C. (2026). Look-Ahead Bias in Financial Forecasts Generated by Large Language Models. SSRN 6772819 (abstract verificado vía Crossref, DOI 10.2139/ssrn.6772819; SSRN dio 403). https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6772819
[10] Richardson, S., Teoh, S. H., Wysocki, P. (2004). *CAR* 21(4), 885-924. https://onlinelibrary.wiley.com/doi/abs/10.1506/KHNW-PJYL-ADUB-0RP6
[11] Hou, K., van Dijk, M., Zhang, Y. (2012). *JAE* 53, 504-526. https://www.sciencedirect.com/science/article/abs/pii/S0165410111000966
[12] Li, K., Mohanram, P. (2014). Evaluating Cross-Sectional Forecasting Models for ICC. *RAST* 19(3), 1152-1185. https://www-2.rotman.utoronto.ca/facbios/file/Li%20and%20Mohanram%20RAST%202014.pdf
[13] So, E. (2013). *JFE* 108(3), 615-640. https://www.sciencedirect.com/science/article/abs/pii/S0304405X13000329 · Digest de CFA: https://rpc.cfainstitute.org/research/cfa-digest/2013/08/a-new-approach-to-predicting-analyst-forecast-errors-do-investors-overweight-analyst-forecasts
[14] Ball, R., Ghysels, E. (2018). *Management Science* 64(10), 4936-4952. https://pubsonline.informs.org/doi/10.1287/mnsc.2017.2864
[15] Bradshaw, M., Drake, M., Myers, J., Myers, L. (2012). *RAST* 17(4), 944-968. https://link.springer.com/article/10.1007/s11142-012-9185-8
[16] Gerakos, J., Gramacy, R. Regression-Based Earnings Forecasts. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2112137
[17] Chen, X., Cho, T., Dou, Y., Lev, B. (2022). *JAR* 60(2), 467-515. https://onlinelibrary.wiley.com/doi/abs/10.1111/1475-679X.12429
[18] Cao, S., Jiang, W., Wang, J., Yang, B. (2024). *JFE* 160, 103910. https://www.sciencedirect.com/science/article/abs/pii/S0304405X24001338 · Resumen en el HLS Forum: http://corpgov.law.harvard.edu/2021/05/27/from-man-vs-machine-to-man-machine-the-art-and-ai-of-stock-analyses/
[19] Chan, L., Jegadeesh, N., Lakonishok, J. (1996). *JF* 51(5), 1681-1713. https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1996.tb05222.x
[20] Bernard, V., Thomas, J. (1989). *JAR* 27, 1-36. https://ideas.repec.org/a/bla/joares/v27y1989ip1-36.html
[21] Livnat, J., Mendenhall, R. (2006). *JAR* 44(1), 177-205. https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1475-679X.2006.00196.x
[22] Kettell, L., McInnis, J., Zhao, W. (2022). Why Has PEAD Declined Over Time? https://business.columbia.edu/sites/default/files-efs/imce-uploads/CEASA/Events%20Page/PEAD_Declined_over_time.pdf
[23] Meursault, V., Liang, P. J., Routledge, B., Scanlon, M. (2023). PEAD.txt. *JFQA* 58(6), 2299-2326. https://doi.org/10.1017/S0022109022001181
[24] Novy-Marx, R. (2015). NBER w20984. https://www.nber.org/papers/w20984
[25] Stickel (1991), *TAR*: https://www.researchgate.net/publication/245704132 · Gleason, C., Lee, C. (2003), *TAR* 78, 193-225: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=370425
[26] Bartov, E., Givoly, D., Hayn, C. (2002). *JAE* 33, 173-204. https://www.sciencedirect.com/science/article/abs/pii/S0165410102000459
[27] Matsumoto, D. (2002). *TAR* 77(3), 483-514. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=298868
[28] Hutton, A., Lee, L. F., Shu, S. (2012). *JAR* 50(5), 1217-1244. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2047107
[29] Mayew, W., Venkatachalam, M. (2012). *JF* 67(1), 1-43. https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2011.01705.x
[30] Loughran, T., McDonald, B. (2011). *JF* 66, 35-65. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1331573 · Diccionario: https://sraf.nd.edu/loughranmcdonald-master-dictionary/
[31] Larcker, D., Zakolyukina, A. (2012). *JAR* 50(2), 495-540. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1572705
[32] Matera, G. (2025). Corporate Earnings Calls and Analyst Beliefs. https://arxiv.org/abs/2511.15214
[33] McInnis, J., Griffin, L. (2025). Gone but Not Forgotten. *JAE* (vía Phys.org, oct-2025). https://phys.org/news/2025-10-companies-omit-stock-based-compensation.html
[34] Calcbench / Suffolk University (16-jul-2026). https://www.prweb.com/releases/calcbench-72-percent-of-sp-500-companies-reported-adjusted-earnings-in-2025-pushing-non-gaap-net-income-higher-than-traditional-gaap-net-income-by-271-billion-302827722.html
[35] FactSet, S&P 500 Earnings Season Update (7-ago-2026). https://insight.factset.com/sp-500-earnings-season-update-august-7-2026
[36] FactSet, Earnings Insight (4-sep-2026). https://advantage.factset.com/hubfs/Website/Resources%20Section/Research%20Desk/Earnings%20Insight/EarningsInsight_090426.pdf
[37] FactSet (5-dic-2025). Are Industry Analysts Overestimating S&P 500 EPS for 2026? https://insight.factset.com/are-industry-analysts-overestimating-sp-500-eps-for-2026
[38] FactSet (2-mar-2026). Analysts Lowering Quarterly EPS Estimates for First Time Since Q2 2025. Q1 2026: −1.5% (US$71.57 → US$70.50) contra promedios de 1.2% (5 años) y 3.2% (20 años). https://insight.factset.com/analysts-lowering-quarterly-eps-estimates-for-first-time-since-q2-2025
[39] FactSet (14-abr-2025). Will S&P 500 Companies Withdraw EPS Guidance for 2025? https://insight.factset.com/will-sp-500-companies-withdraw-eps-guidance-for-2025
[40] FactSet, Earnings Insight (18-sep-2026), primaria: https://advantage.factset.com/hubfs/Website/Resources%20Section/Research%20Desk/Earnings%20Insight/EarningsInsight_091826.pdf · Motley Fool (22-sep-2026), secundaria: https://www.fool.com/investing/2026/09/22/s-and-p-500-profits-are-on-track-for-a-third-straight-quarter-of-25-growth-the-index-hasn-t-kept-up/
[41] SEC, propuesta de reporte semestral (5-may-2026). https://www.sec.gov/newsroom/press-releases/2026-42-sec-proposes-amendments-permit-optional-semiannual-reporting-public-companies · https://www.sec.gov/files/rules/proposed/2026/33-11414.pdf · Deloitte: https://dart.deloitte.com/USDART/home/publications/deloitte/heads-up/2026/sec-proposes-semi-annual-reporting
[42] SEC, EDGAR APIs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces · Acceso justo (10 solicitudes/s, User-Agent): https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data · companyfacts de MSFT, AMZN, GOOGL y META (CIK 789019, 1018724, 1652044, 1326801): https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json · XBRL en el 8-K: 17 CFR 229.601(b)(101) y (b)(104), https://www.ecfr.gov/current/title-17/chapter-II/part-229/subpart-229.600/section-229.601
[43] BMV, archivos XBRL: https://www.bmv.com.mx/es/emisoras/archivos-estadar-xbrl · CNBV, taxonomías: https://www.gob.mx/cnbv/acciones-y-programas/taxonomias-reporte-anual · ITAM: http://direccionestrategica.itam.mx/xbrl-su-desarrollo-y-aplicacion-en-mexico/
[44] BMV, resumen de la Circular Única de Emisoras, art. 33 (información periódica; documento de may-2017). https://www.bmv.com.mx/docs-pub/SERVICIOS_EMISORAS/5x77w2olfaeh3y4850gq.pdf
[45] Monex vía Industrial News (14-jul-2026): https://www.industrialnewsbc.com/2026/07/14/impulsara-tipo-de-cambio-los-reportes-trimestrales-de-las-emisoras-de-la-bmv-monex/ · El Financiero (20-jul-2026): https://www.elfinanciero.com.mx/empresas/2026/07/20/empresas-en-la-bolsa-mexicana-de-valores-tuvieron-balances-modestos-durante-el-2t26/ · Monex, Reportes al 2T26 (27-jul-2026; 403): https://www.monex.com.mx/portal/download/reportes/Reportes%202T26%20260727.pdf
[46] El Financiero (2-jul-2026). EU rechaza extender el T-MEC; solicita revisiones anuales. https://www.elfinanciero.com.mx/economia/2026/07/02/eu-rechaza-extender-el-t-mec-solicita-revisiones-anuales/
[47] Amazon, 10-K del ejercicio 2024: https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm · Meta, 10-K del ejercicio 2025: https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm · Hudson Labs: https://hudson-labs.com/research/meta-financials-meta
[48] La brecha capex/D&A se verificó con companyfacts de la SEC [42]. Burry: secundarias, no verificadas: https://siliconanalysts.com/analysis/hyperscaler-ai-capex-depreciation-wall-2026 · https://chipstockinvestor.com/metas-ai-data-center-depreciation-problem-breaking-down-michael-burrys-argument-so-far-against-the-hyperscalers-and-nvidia/
[49] IFRS Foundation, IFRS 18 Presentation and Disclosure in Financial Statements: https://www.ifrs.org/issued-standards/list-of-standards/ifrs-18-presentation-and-disclosure-in-financial-statements/ · PwC, IFRS 18 is here (403 el 25-sep-2026): https://www.pwc.com/mt/en/publications/other/ifrs18-is-here.html
[50] Gneiting, T., Raftery, A. (2007). *JASA* 102, 359-378. https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf
[51] Audit Update (15-jul-2024), resumen de Ideagen Audit Analytics (2004-2023) y CAQ (2013-2022): https://www.auditupdate.com/post/two-studies-find-that-restatements-rates-remain-low-although-big-r-restatements-have-begun-to-incre · Audit Analytics (27-ago-2020), antecedentes a 2019: https://blog.auditanalytics.com/error-corrections-a-look-at-adjustment-and-restatement-trends-2/
[52] Fortune (30-abr-2025), GM retira su guía: https://www.fortune.com/2025/04/30/general-motors-withdraws-guidance-massive-tariff-uncertainty-cfo-analyst · Stellantis, 6-K (30-abr-2025): https://www.sec.gov/Archives/edgar/data/1605484/000160548425000030/stellantisnvq12025pressrel.htm · Cummins, 8-K Ex. 99 (5-may-2025): https://www.sec.gov/Archives/edgar/data/26172/000002617225000010/cmi2025q18-kex99.htm · JetBlue, 8-K Ex. 99.1 (29-abr-2025): https://www.sec.gov/Archives/edgar/data/1158463/000115846325000064/ex991-earningsreleaseq12025.htm · Descartada: la nota de MarketMinute/FinancialContent (23-ene-2026) no tiene autor, no menciona a Stellantis, Mercedes ni JetBlue, y fecha mal el retiro de Cummins ("late 2025").

---

## Registro de verificacion (2026-09-25)

Verificación adversarial del 25-sep-2026. Se usaron WebFetch sobre fuentes primarias, la API de EDGAR (submissions y companyfacts), eCFR, Crossref y arXiv. Se revisaron más de 50 elementos. Quedaron 38 grupos confirmados, 8 correcciones en sitio y 12 elementos sin verificar, marcados "(no verificado)". Algunos elementos corregidos también llevan marca.

**Confirmados en fuente primaria o prensa seria con fecha:**
1. FactSet 4-sep-2026 (PDF, re-leído):
   - walk-down de 1.7/2.1/2.6/3.1%;
   - 3T26: +1.2% (US$88.64 → 89.69); crecimiento de 28.5% (26.6% al 30-jun);
   - P/U de 19.5 (5 años: 19.8; 10 años: 19.0);
   - guías 70/41 = 63% (5 años: 41%; 10 años: 42%); 44 de 70 en TI;
   - margen récord de 17.0% en el 2T26 (5 años: 12.4%);
   - CY2026 de US$361.38 (+6.1% en jul-ago);
   - Energía +102.5%; petróleo US$81.45 contra 64.97;
   - 2T27 +1.2%.
2. FactSet 18-sep-2026 (PDF primario; antes solo vía Motley Fool): 28.9%, P/U de 19.1, guías 72/43.
3. FactSet 7-ago-2026:
   - 86% arriba en UPA (5 años: 78%; 10 años: 76%) y 76% en ingresos (5 años: 70%; 10 años: 68%);
   - Alphabet: US$98 mil millones; Amazon: US$53.4 mil millones (Anthropic);
   - crecimiento de 50.4/32.0% y sorpresa de 29.2/10.9%.
4. FactSet 5-dic-2025: US$309.22; 6.2%; 17/25; 0.9% sin 2001, 2008, 2009 y 2020.
5. FactSet 2-mar-2026: 1T26 −1.5% (US$71.57 → 70.50).
6. FactSet 14-abr-2025: 2 retiros (Walgreens y Delta) entre 23 reportes al 10-abr.
7. Retiros de guía en 2025:
   - GM, 29-abr (Fortune);
   - Stellantis, 30-abr (6-K);
   - Cummins, 5-may (8-K; cita textual sobre aranceles);
   - JetBlue, 29-abr (8-K; "macroeconomic uncertainty", sin mención de aranceles).
8. SEC, reporte semestral:
   - comunicado 2026-42 del 5-may-2026; Release 33-11414; Form 10-S con plazo de 40/45 días;
   - comentarios hasta el 6-jul-2026 (Deloitte); Q1/Q3 por 8-K voluntario; Inline XBRL;
   - estatus "Proposed Rule" en la página de rulemaking de la SEC (consultada el 25-sep-2026).
9. XBRL en el 8-K: 17 CFR 229.601(b)(101) y (b)(104) en eCFR, más una prueba empírica con el 8-K de Cummins. Antes era "práctica general".
10. API de EDGAR: frames "last filed", retraso menor a un minuto, `companyfacts.zip` nocturno, 10 solicitudes/s y User-Agent.
11. Meta, 10-K 2025: vidas útiles de 5.5 años; −US$2.92 mil millones de depreciación; +US$2.59 mil millones de utilidad neta; +US$1.00 por acción diluida.
12. Amazon, 10-K 2024: de 5 a 6 años en 2024 (−US$3.2 mil millones de D&A) y de 6 a 5 años en 2025 (−US$0.7 mil millones de utilidad operativa), más −US$0.6 mil millones por retiros anticipados.
13. Capex de los hyperscalers a mar-2026: US$433.9 mil millones, cálculo propio con companyfacts (coincide exactamente con la cifra secundaria). D&A de US$144.6-149.4 mil millones según la definición.
14. Calcbench/Suffolk (16-jul-2026): 361/500; US$271 mil millones; 87%; AbbVie, Broadcom, Capital One, GM y Pfizer.
15. McInnis y Griffin (JAE 2025, vía Phys.org del 29-oct-2025): más de 70,000 anuncios de 2003-2021; −1 a −2 pp aunque la SBC se excluya.
16. Monex (vía Industrial News, 14-jul-2026): +6.5/12.8/14.1%; margen de 23.2 contra 21.9%; peso +10.8% promedio y 6.7% al cierre; fecha límite 28-jul.
17. El Financiero (2-jul-2026), T-MEC: sin extensión automática, revisiones anuales, reunión de la CLC del 1-jul y siguiente ronda el 20-jul.
18. IFRS.org, IFRS 18: vigente para ejercicios desde el 1-ene-2027; dos subtotales nuevos; MPM en notas; emitida en abr-2024.
19. Resumen de la CUE en la BMV: 20 y 40 días hábiles; STIV-2 y Emisnet.
20. Audit Update (15-jul-2024): datos a 2023, no "a 2024"; Big R de 209 (52%).
21. Retiro de KMN en arXiv: 20-feb-2025, "temporalmente".
22. Retracción de Kim y Nikolaev en JAR: 29-abr-2026 (Crossref); en línea desde el 18-dic-2024.
23. Expresión de Preocupación en RFS: DOI 10.1093/rfs/hhag017; en línea el 1-mar-2026; número de mayo de 2026.
24. Lopez-Lira, Tang y Zhu: arXiv 2504.14765 (20-abr-2025); texto del abstract.
25. Benhenda: arXiv 2601.13770 (20-ene-2026).
26. Gao, Jiang y Yan: arXiv 2512.23847 (29-dic-2025; revisado el 12-jun-2026).
27. Liang: SSRN 6772819; abstract vía Crossref; ~11/16/18%; corte del 30-sep-2021.
28. Matera: arXiv 2511.15214 (19-nov-2025).
29. Martineau: CFR 11(3-4), 613-646. Subrahmanyam: SSRN 5930255 y UCLA Anderson Review (21-ene-2026; 3% del valor; t de 1.43).
30. Kettell, McInnis y Zhao (abr-2022): abstract textual.
31. Meursault et al. (JFQA 58(6)): 2.87/4.61/6.51/8.01 contra 1.54/2.70/3.87/4.63 (WP de la Fed de Filadelfia).
32. Li y Mohanram: RAST 19(3); 28-38%; hasta 45%; ERC 18-85%; RW 13-37% mejor que HVZ.
33. So (JFE 108(3)): 5.8% y 9.4% fuera de muestra, 1980-2009 (CFA Digest).
34. Ball y Ghysels: MS 64(10); abstract.
35. Chen, Cho, Dou y Lev: JAR 60(2); AUC de 67.52-68.66% y 5.02-9.74%.
36. Cao, Jiang, Wang y Yang: JFE 160; 53.7 y 57.3% (versión WP, HLS Forum).
37. Abstracts vía Crossref:
    - Loughran y McDonald: ~3/4;
    - Mayew y Venkatachalam;
    - Larcker y Zakolyukina: 6-16%;
    - Hutton, Lee y Shu: ventaja micro contra macro;
    - Matsumoto;
    - Gleason y Lee;
    - Richardson, Teoh y Wysocki;
    - Chan, Jegadeesh y Lakonishok (cualitativo);
    - HVZ (1968-2008);
    - Novy-Marx (con matiz sobre los crashes).
38. Cálculos propios re-ejecutados:
    - EV de 107.5 y E[ln] de 3.66%;
    - DCF inverso de 9.08/11.68/14.03% con terminal de 63-68%;
    - Brier de 0.1716;
    - bandas binomiales de 34-45 (n = 50) y 12-19 (n = 20);
    - +16.9% frente a diciembre;
    - 3%/12% = 25% y 1%/12% = 8.3%;
    - parámetros coherentes con `config/parametros.json`.

**Corregidos en sitio:**
1. §2.4: la inferencia "el pánico fue más de narrativa que de conteo" se basaba en 23 reportes y en un retiro de Walgreens ajeno a los aranceles. Se eliminó. GM se fecha el 29-abr, no el 30.
2. §2.4 y [52]: los retiros de Stellantis, Cummins y JetBlue pasan de fuente secundaria a primaria. JetBlue citó incertidumbre macro, no aranceles. La fuente secundaria [52] se descarta: sin autor, no menciona a tres de las cuatro empresas y da una fecha errónea.
3. §4.8: las cifras de Chedraui son una **estimación de Ve por Más**, no un dato reportado. La de Aeroméxico sí es reportada (−35.5%, atribuida al Mundial 2026).
4. §6.5: `pronosticos.py puntuar` no usa la tasa base histórica; usa la frecuencia observada en la muestra y agrupa por autor.
5. §2.2 y [5]: la Expresión de Preocupación salió en línea el 1-mar-2026, no en "mayo" (mayo es el número impreso). Se completó el título del artículo.
6. §2.8: los datos de Audit Analytics llegan a 2023, no a 2024. Se agregaron las cifras.
7. §2.3: se matizó Novy-Marx. La eliminación de crashes corresponde al momentum de utilidades que controla por el rendimiento pasado.
8. §2.7: Meta es +US$1.00 por acción **diluida**, con +US$2.59 mil millones de utilidad neta. Se agregó el efecto de Amazon de 2024.

**Siguen sin verificar (marcados inline):**
1. Cierre de Monex 2T26: el PDF da 403 y la suma es de 102%. Se prohíbe usarlo como tasa base.
2. Burry: ~US$176 mil millones y la fecha.
3. XBRL de la CNBV obligatorio desde el 1T16. Tampoco se encontró la taxonomía de ~890 elementos, que no aparece en este capítulo.
4. Mercedes-Benz: retiro de guía por aranceles.
5. Bernard y Thomas: 41/48.
6. Chan, Jegadeesh y Lakonishok: 7.5%.
7. Stickel: ~6 meses.
8. Hutton, Lee y Shu: ~50%.
9. Larcker y Zakolyukina: 50-65%.
10. Chen et al.: "más de 12,000 variables".
11. La cita textual de la retracción de Kim y Nikolaev (Wiley, 403).
12. Magnitud del momentum de revisiones después de 2015 (ya marcada).

Sin marca inline por no tener cifra, con abstract inaccesible (Springer, SSRN o JSTOR bloqueados): Bradshaw et al. (2012), Gerakos y Gramacy, Livnat y Mendenhall, Bartov, Givoly y Hayn. Los metadatos (revista, volumen y páginas) sí se confirmaron en Crossref. La aplicación retrospectiva de IFRS 18 proviene de PwC (403 en esta sesión) y no se re-leyó en la norma.

**Impacto en el grado:** sin cambios en el grado global (B/C/D). La corrección de §2.4 cambia una lectura: los retiros de guía por aranceles en 2025 fueron reales y documentados en presentaciones a la SEC. La regla "ensanchar intervalos cuando se retira la guía" se sostiene con más fuerza.
