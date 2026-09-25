# Módulo 15 — Eventos corporativos, situaciones especiales y señales de insiders: qué sobrevive a la publicación, a la latencia de los datos y a los costos desde México

> Nivel: especialidad (posgrado + mesa event-driven) · Actualizado: 2026-09-25 · Grado de evidencia global: **C** — Lo que sobrevive con grado B o mejor son dos cosas: las primas por *vender seguro o proveer liquidez* (merger arbitrage, comprimidas pero vivas) y los *filtros de exclusión* (no comprar IPOs ni deSPACs en el mercado secundario, no comprar picos de atención/meme, castigar a los emisores netos de acciones). Casi todas las señales *de compra* famosas (spin-offs, recompras, PEAD, inclusión en índices, prima de anuncio de resultados, 13F, congresistas) decayeron tras publicarse, quedaron confinadas a microcaps o desaparecen netas de costos y latencia. Desde el SIC, sin venta en corto práctica, con ~0.58% de comisión ida y vuelta y riesgo USDMXN, varias ni siquiera son implementables.

Prerrequisitos: Módulo 06 (asset pricing empírico: decaimiento post-publicación, factor zoo), Módulo 07 (backtesting, deflated Sharpe, PBO), Módulo 08 (sesgos conductuales y pronóstico calibrado), Módulo 11 (México: SIC, fiscalidad, BMV/BIVA). Aquí no se repiten; se usan.

---

## 1. Objetivos de dominio

Quien se titula en este módulo debe poder, sin consultar:

1. **Descomponer** el rendimiento de cualquier evento en anticipación (antes del anuncio), reacción (ventana del anuncio) y deriva (después), y decir qué parte es capturable con la **latencia real** del dato: Form 4 (2 días hábiles), 13D (5 días hábiles), 13F (hasta 45 días después del trimestre), reportes del Congreso de EUA (hasta 45 días).
2. **Valuar un merger arbitrage u OPA**: spread bruto y anualizado, probabilidad implícita, pérdida si el trato se cae, tamaño por riesgo, y explicar por qué el perfil equivale a vender un seguro con cola izquierda correlacionada con las crisis.
3. **Recitar** para cada señal del catálogo (§5): magnitud original, magnitud post-publicación, costos, fuente de datos, si es explotable vía SIC y su grado.
4. **Clasificar** cada anomalía por su motor económico (prima de riesgo o liquidez, presión de precio, asimetría de información, atención limitada) y predecir con eso si sobrevive al arbitraje.
5. **Detectar marketing**: ETFs de congresistas, clones de 13F, "backtests" de insiders sin placebo, estudios de largo plazo con CAR y benchmark de mercado.
6. **Operar el pipeline de datos**: EDGAR (Form 4, 13F-HR, SC 13D/13G, 8-K, S-1/424B, DEFM14A, SC TO-T), PTRs del Congreso, FINRA; en México, eventos relevantes y folletos de OPA.
7. **Decidir la explotabilidad desde México**: SIC, sin cortos, costo de ida y vuelta, ISR y riesgo cambiario (que puede superar al spread).
8. **Convertir** todo lo anterior en reglas compatibles con `config/parametros.json` (perfil estándar y `arena_agresivo`) y con el `modo_torneo`.

---

## 2. Núcleo teórico / marco

### 2.1 Anatomía de un evento: qué parte es tuya

CAR(−τ, +T) = **anticipación** (fugas, rumores, acumulación del activista) + **reacción** (día del anuncio) + **deriva** (post-anuncio).

- En un mercado eficiente la deriva es cero y todo el valor se reparte entre quien tenía información privada (anticipación) y quien reacciona en milisegundos (reacción).
- Un inversionista sin información privada y con ejecución manual en GBM solo puede cobrar la **deriva que empieza después de que él procesa el dato**. Esa ventana es la que decae primero.
- Evidencia directa: en microcaps, la reacción a compras de insiders se concentra en 2-3 sesiones y en calendar-time sin el primer día no hay alfa (Zhao 2026 [23]); en las inclusiones al S&P 500 anunciadas el viernes 5-sep-2025 tras el cierre, el salto ocurrió en after-hours (magnitud en after-hours no reverificada [49]) y al cierre de la primera sesión (8-sep) ya era de +15.8% en Robinhood y +11.6% en AppLovin (cierres de Yahoo Finance [71]), antes de que un operador manual pudiera actuar.

### 2.2 Cuatro motores económicos (y su pronóstico de supervivencia)

| Motor | Ejemplos | Por qué paga | ¿Sobrevive? |
|---|---|---|---|
| **Prima por seguro/liquidez** | Merger arbitrage, OPAs | Alguien debe cargar el riesgo de que el trato se caiga mientras los tenedores originales venden; la correlación con el mercado sube en caídas [1] | Sí, pero **comprimida** cuando entra capital (spread −400 pb desde 2002 [3]) |
| **Presión de precio** (curvas de demanda con pendiente negativa) | Inclusión en índices, venta forzada de spin-offs, lockups | Compradores o vendedores forzados que no negocian precio | **Muere** cuando aparecen proveedores de liquidez especializados (Greenwood-Sammon [9]) |
| **Asimetría de información / timing corporativo** | Insiders, activistas, emisores que venden caro (IPO/SEO) y recompran barato | El insider sabe más; el emisor vende cuando su acción está cara | Lado **corto** persistente (difícil de arbitrar: hay que vender en corto acciones caras); lado largo decae |
| **Atención limitada / preferencia por lotería** | PEAD, IPOs calientes, SPACs, meme stocks | Minoristas compran lo que llama la atención y pagan una prima negativa | Sobrevive como **lo que no hay que hacer** [44][45] |

Regla mental: (1) sobrevive comprimida; (2) muere cuando se profesionaliza; (3) sobrevive donde explotarla requiere vender en corto; (4) sobrevive como filtro de exclusión.

### 2.3 Ciclo de vida de una anomalía de evento

Descubrimiento → publicación → entrada de capital → compresión → residuo en microcaps o en valores ilíquidos, donde el costo de transacción se lo come. Aparece en casi todo el catálogo: merger arbitrage [3], índice [9], recompras [17][18], PEAD [34][35], prima de anuncio [33]. Para PEAD existe una explicación alternativa al arbitraje: las sorpresas de utilidades se volvieron menos persistentes y, controlando por eso, la tendencia a la baja deja de ser significativa (Kettell-McInnis-Zhao [36]). El mecanismo general de decaimiento post-publicación está en el Módulo 06.

### 2.4 La trampa metodológica del largo plazo

Los estudios de evento a 3-5 años dependen del benchmark:

- IPOs 1980-2024 (Ritter [12]): 3 años desde el primer cierre = **−20.5%** contra el mercado, pero **−8.9%** contra firmas pareadas por tamaño y book-to-market. La mitad de la "anomalía" es exposición a small-growth.
- Spin-offs: los primeros estudios encuentran excesos grandes; con pruebas refinadas (calendar-time, BHAR con pareo) el efecto de largo plazo ya no aparece (revisión de Veld y Veld-Merkoulova [7]). En cambio, una tesis de maestría de 2023 con modelo de mercado reporta +28.5% a 36 meses para 609 spin-offs de Norteamérica y Europa Occidental, 2000-2022 [50]; el contraste muestra cuánto infla el método.
- Exigencia mínima del sistema: (a) portafolio de calendar-time con alfa multifactorial, (b) BHAR contra firmas pareadas, (c) subperiodo post-publicación, (d) neto de costos. Si falta cualquiera, el grado máximo es C.

### 2.5 Matemática del merger arbitrage (y de una OPA)

Notación: O = contraprestación por acción (efectivo, o razón de canje × precio del adquirente); P = precio actual del objetivo; B = precio si el trato se cae (proxy: precio previo al anuncio ajustado por el movimiento del sector); d = días al cierre esperado.

- Ganancia si cierra: G = (O − P)/P. Pérdida si se cae: L = (P − B)/P.
- Spread anualizado simple: G × 365/d. Compuesto: (1 + G)^(365/d) − 1.
- Probabilidad implícita (neutral al riesgo, sin valor temporal): **p\* = (P − B)/(O − B)**.
- Valor esperado con tu probabilidad p: E[r] = p·G − (1 − p)·L. **Solo hay ventaja si p > p\*** o si hay una prima de riesgo sistemática, que es lo que Mitchell-Pulvino miden como pago por proveer liquidez [1].
- Trato en acciones: largo objetivo y corto (razón × adquirente). Sin corto (caso SIC) la posición queda expuesta al precio del adquirente: deja de ser arbitraje.

Ejemplo: O = 50, P = 48.50, B = 38, d = 120. G = 3.09% (≈9.4% anual simple); p\* = 10.5/12 = 87.5%; L = 21.6%. Con p = 90%: E = 0.9×1.50 − 0.1×10.50 = 0.30 por acción (0.62%). Cada punto porcentual de probabilidad vale (O − B)/100 = 0.12 por acción (0.25% del precio). **Todo el edge está en estimar p mejor que el mercado por unos pocos puntos.** Un sistema con LLM logró un Brier balanceado por clase de 0.151 sobre más de 400 tratos grandes en 42 países, con tres desenlaces (cierre en términos anunciados, oferta superior, terminación): 24% por debajo de las probabilidades implícitas calibradas del mercado, 19% debajo de XGBoost y 25-42% debajo de LLMs de frontera sin ajuste (Jajal et al., ICML 2026 [46]). Inferencia: para una IA, el único edge escalable en situaciones especiales es la estimación de probabilidades, y se mide con Brier antes de arriesgar capital.

Perfil de pagos: cóncavo, con muchas ganancias chicas y pocas pérdidas grandes. Mitchell-Pulvino lo modelan con contingent claims: la correlación con el mercado es casi nula en mercados planos o alcistas y sube en caídas severas [1]. En ETFs de merger arbitrage, la beta diaria contra el SPY en 2016-2026 fue de 0.08-0.18 (cálculo propio, §5.2). Inferencia: se comporta como vender puts sobre "que la economía y el crédito no se rompan", no como un sustituto de CETES.

### 2.6 Latencia de la información: el reloj que decide qué es explotable

| Evento | Documento | Plazo vigente | Consecuencia práctica |
|---|---|---|---|
| Compra/venta de insider | Form 4 | 2 días hábiles (SOX §403; antes, 10 días tras el cierre del mes) [51] | La reacción ocurre en 1-3 sesiones tras publicarse [23] |
| Planes 10b5-1 de consejeros y directivos | Plan + casilla en Form 4 + 10-Q/10-K | Cooling-off de 90-120 días; vigente desde 27-feb-2023 [52] | Las ventas bajo plan son ruido; la señal está en las compras discrecionales |
| Activista >5% | Schedule 13D | 5 días hábiles (antes 10 días naturales); enmiendas en 2 días hábiles; vigente desde 5-feb-2024 [53] | Menos acumulación previa; la reacción se concentra en el filing |
| Institucional pasivo >5% (QII) | Schedule 13G | 45 días después del fin de **trimestre** desde 30-sep-2024 [53] | — |
| Tenencias institucionales >US$100M | 13F-HR | Hasta 45 días después del trimestre [26] | Posiciones con 45-135 días de antigüedad |
| Congreso de EUA (y cónyuges) | Periodic Transaction Report | 30 días desde la notificación y nunca más de 45 días tras la operación; operaciones >US$1,000; monto en **rangos** [54][74] | Señal vieja e imprecisa |
| Cortos institucionales grandes | Form SHO (Regla 13f-2) | Primer reporte pospuesto al 14-feb-2028 tras la remisión del Quinto Circuito (ago-2025) [55] | Hoy solo hay short interest agregado de FINRA |
| México: OPA | Aviso y folleto informativo (BMV/CNBV) | Según folleto | Spread en MXN, sin riesgo cambiario |

---

## 3. Literatura y fuentes canónicas

| Autores | Año | Trabajo | Revista | Hallazgo cuantificado | Fuente | Grado |
|---|---|---|---|---|---|---|
| Mitchell, Pulvino | 2001 | Characteristics of Risk and Return in Risk Arbitrage | JF 56(6) | 4,750 fusiones 1963-1998; **4%/año** de exceso **neto de costos** tras controlar la no linealidad (contingent claims); correlación positiva con el mercado solo en caídas severas; perfil "similar a vender puts de índice descubiertos" | [1] | B |
| Baker, Savasoglu | 2002 | Limited Arbitrage in Mergers and Acquisitions | JFE 64(1) | Cartera diversificada: 0.6-0.9%/mes anormal, 1981-1996 (no verificado: abstract inaccesible en esta sesión); más alto con mayor riesgo de cierre y objetivo más grande (no verificado) | [2] | B |
| Jetley, Ji | 2010 | The Shrinking Merger Arbitrage Spread: Reasons and Implications | FAJ 66(2) | Spread −**400 pb** desde 2002, en paralelo a menores rendimientos agregados de los hedge funds de merger arb y mayores entradas de capital; recomiendan usar solo rendimientos post-2002. La cifra de caída del alfa en pb/mes no se verificó | [3] | A (decaimiento) |
| Ricks, Lin | 2024 | How Deals Die | HLS Forum | 5,058 acuerdos definitivos con objetivo público de EUA 1996-2020: no consumación de ~**9%** (calma) a ~**12%** (turbulencia), "en gran medida sin cambio" en 25 años | [4] | B |
| Cusatis, Miles, Woolridge | 1993 | Restructuring through Spinoffs | JFE 33(3) | 146 spin-offs 1965-1988: exceso **+25.5%** (2 años) y **+33.6%** (3 años) en subsidiarias (cifras vía la tabla de revisión de [50], no del artículo original) | [5] | C hoy |
| McConnell, Ovtchinnikov | 2004 | Predictability of Long-Term Spinoff Returns | JIM 2(3) | 311 spin-offs de EUA 1965-2000: excesos positivos y significativos en subsidiarias (vía tabla de [50]) | [6] | C |
| Veld, Veld-Merkoulova | 2009 | Value Creation through Spin-offs: A Review | IJMR 11(4) | 26 estudios: **+3.02%** en el anuncio; el exceso de largo plazo **ya no aparece** con pruebas estadísticas refinadas | [7] | B |
| Shleifer | 1986 | Do Demand Curves for Stocks Slope Down? | JF 41(3) | Inclusiones al S&P 500 desde sept-1976: retorno anormal positivo y significativo en el anuncio (≈3%, según la cita de Greenwood-Sammon [9]; la cifra exacta del artículo no se verificó) que no desaparece en al menos 10 días; relacionado con compras de fondos índice, no con la calificación crediticia | [8] | A (histórico) |
| Greenwood, Sammon | 2025 | The Disappearing Index Effect | JF 80(2) | Adiciones: 3.4% (80s, versión NBER) → **7.4%** (90s; 7.6% en la versión NBER) → **<1%** (2010-2020; 0.8% en NBER); eliminaciones: promedio de solo 0.1% en 2010-2020 (−0.6% en la versión NBER de 2022) | [9] | A |
| Ritter | 1991 | The Long-Run Performance of IPOs | JF 46(1) | 1,526 IPOs 1975-84: **34.47%** a 3 años desde el primer cierre vs **61.86%** de las pareadas por industria y valor de mercado (riqueza relativa 0.831) | [10] | A |
| Ritter (base viva) | 2026 | IPO Statistics / Long-run Statistics | U. Florida | 9,253 IPOs 1980-2024: primer día 18.9%; 3 años desde el 1er cierre +19.1%, **−20.5%** vs mercado, **−8.9%** vs estilo | [11][12] | A |
| Loughran, Ritter | 1995 | The New Issues Puzzle | JF 50(1) | 1970-1990, 5 años: **5%/año** IPOs y **7%/año** SEOs, muy debajo de los no emisores | [13] | B |
| Pontiff, Woodgate; Daniel, Titman | 2008; 2006 | Share Issuance and Cross-sectional Returns; Market Reactions to Tangible and Intangible Information | JF | La emisión neta predice negativamente el rendimiento post-1970, con más significancia que tamaño, B/M o momentum | [14] | A/B |
| Ikenberry, Lakonishok, Vermaelen | 1995 | Market Underreaction to Open Market Share Repurchases | JFE 39 | 1980-1990: BHAR a 4 años **+12.1%**; value **+45.3%**; glamour ~0 | [15] | C hoy |
| Peyer, Vermaelen | 2009 | The Nature and Persistence of Buyback Anomalies | RFS 22(4) | Rechazan la desaparición con datos hasta inicios de los 2000; las recompras responden a sobrerreacción a malas noticias | [16] | B/C |
| Fu, Huang | 2016 | The Persistence of Long-Run Abnormal Returns Following Stock Repurchases and Offerings | MS 62(4) | Los excesos de largo plazo tras recompras **y** SEOs **desaparecen** para eventos de 2003-2012; lo asocian a más inversión institucional, menores costos y mejor liquidez (tamaño de muestra no verificado) | [17] | B (decaimiento) |
| Lee, Park, Pearson | 2020 | Repurchases after Being Well Known as Good News | JCF 62 | Exceso post-2001 mucho menor; más recompras motivadas por la compensación de directivos | [18] | B |
| Lakonishok, Lee | 2001 | Are Insider Trades Informative? | RFS 14(1) | 1975-1995: solo **compras** informan; el efecto se concentra en firmas **pequeñas**; ventas sin poder predictivo | [19] | B |
| Jeng, Metrick, Zeckhauser | 2003 | Estimating the Returns to Insider Trading | REStat 85(2) | Compras: **>6%/año** anormal (rendimiento del insider, no del imitador); ventas ~0 | [20] | B |
| Cohen, Malloy, Pomorski | 2012 | Decoding Inside Information | JF 67(3) | Compras "oportunistas": **+82 pb/mes** ponderado por valor; "rutinarias": ~0 | [21] | B |
| Oenschläger, Möllenhoff | 2025 | Insider Filings as Trading Signals — Does It Pay to Be Fast? | FRL 72 | Rendimiento positivo pero menor; **se vuelve negativo** al limitar el monto por señal a un tamaño razonable | [22] | B |
| Zhao | 2026 | Insider Purchases Far Below the 52-Week High (microcaps) | arXiv (v2 sep-2026) | 13,534 compras 2018-2024: primer día +4.13% (quintil más castigado) vs +0.86%; sin alfa en calendar-time excluyendo el primer día | [23] | C (preprint) |
| Cohen, Polk, Silli / Antón, Cohen, Polk | 2010/2021 | Best Ideas | WP (LSE, HBS) | La "mejor idea" de cada gestor: **+2.8 a 4.5%/año**; el resto de la cartera, sin alfa | [24] | C |
| Martin, Puthenpurackal | 2008 | Imitation Is the Sincerest Form of Flattery: Warren Buffett and Berkshire Hathaway | WP SSRN (2005, rev. 2008) | Imitar a Berkshire el mes siguiente a su divulgación: +10.75% a +14.26%/año según la medida (1976-2006); reacción de +4.03% el día de la divulgación (cifras no verificadas: SSRN inaccesible) | [25] | C |
| Angelini, Iqbal, Jivraj | 2019 | Systematic 13F Hedge Fund Alpha | WP Barclays/Novus | Convicción + consenso de gestores de horizonte largo: **+3.80%/año** sobre el S&P 500, Sharpe 0.75 (may-2004 a jun-2019) | [26] | C |
| Rapach, Ringgenberg, Zhou | 2016 | Short Interest and Aggregate Stock Returns | JFE 121(1) | Short interest agregado: R² anual **12.89%** in-sample y **13.24%** out-of-sample (OOS dentro de la muestra original); >300 pb/año de ganancia de utilidad media-varianza; canal de flujos de caja | [27] | B (sin prueba post-publicación verificada) |
| Boehmer, Jones, Zhang | 2008 | Which Shorts Are Informed? | JF 63(2) | NYSE 2000-2004: muy shorteadas rinden **−1.16%** ajustado por riesgo en 20 días vs poco shorteadas (15.6% anualizado); con cortos institucionales fuera de programa, −1.43% el mes siguiente (19.6% anualizado) | [28] | B (dato propietario) |
| Hong, Li, Ni, Scheinkman, Yan | 2015 | Days to Cover and Stock Returns | NBER w21166 | Long-short por días para cubrir: **1.2%/mes**; mejor predictor que el short ratio | [29] | B |
| Brav, Jiang, Partnoy, Thomas | 2008 | Hedge Fund Activism, Corporate Governance, and Firm Performance | JF 63(4) | 2001-2006: **≈7%** anormal alrededor del anuncio, sin reversión en el año siguiente; éxito total o parcial en 2/3 de los casos | [30] | B |
| Becht, Franks, Grant, Wagner | 2017 | Returns to Hedge Fund Activism: An International Study | RFS 30(9) | 1,740 intervenciones en 23 países, 2000-2010: Norteamérica **7.0%** en (−20, +20) días, Asia 6.4%, Europa 4.8% | [31] | B |
| Savor, Wilson | 2016 | Earnings Announcements and Systematic Risk | JF 71(1) | Firmas por anunciar: **9.9%** anual anormal; explicación por riesgo sistemático | [32] | C hoy |
| Heitz, Narayanamoorthy, Zekhnini | 2018-2020 | Filings of Material Information and the Disappearing Earnings Announcement Premium | WP SSRN | La prima **desapareció en EUA** y migró a las fechas de 8-K tras la regla de divulgación de 2004; sigue robusta fuera de EUA (detalle no reverificado en esta sesión; el título del WP es coherente con el mecanismo 8-K) | [33] | C (WP sin publicar) |
| Martineau | 2022 | Rest in Peace Post-Earnings Announcement Drift | CFR 11(3-4) | PEAD **inexistente en large caps desde 2006**; recientemente desapareció también en microcaps | [34] | B |
| Jegadeesh, Kim, Krische, Lee | 2004 | Analyzing the Analysts | JF 59 | El **cambio** trimestral del consenso predice de forma robusta; el **nivel** solo añade valor en acciones value o con momentum positivo | [37] | B |
| Ziobrowski et al. | 2004 | Abnormal Returns from the Common Stock Investments of the U.S. Senate | JFQA 39(4) | 1993-1998: compras **+85 pb/mes** sobre el mercado (≈10%/año); ventas −12 pb/mes; diferencia cercana a 1 pp/mes (el "12%/año" es el resumen del autor ante el Congreso) | [38][39] | D hoy |
| Eggers, Hainmueller | 2013 | Capitol Losses | JOP 75(2) | 2004-2008: portafolio promedio **−2 a −3%/año** vs índice (alfa −0.23 pp/mes ≈ −2.8%/año); sin ventaja informativa tampoco en 1985-2001; los autores de 2004 se negaron a compartir datos | [39] | B |
| Wei, Zhou | 2025 | "Captain Gains" on Capitol Hill | NBER w34524 (nov-2025) | Legisladores que ascienden al liderazgo: **+47 pp/año** vs pares pareados tras el ascenso; canales de influencia política y acceso corporativo (número de líderes y periodo muestral no verificados) | [40] | C |
| Klausner, Ohlrogge, Ruan | 2022 | A Sober Look at SPACs | Yale J. on Reg. 39 | SPACs fusionados ene-2019 a jun-2020: efectivo neto por acción, mediana **US$5.70** y media US$4.10 por cada US$10; post-fusión ≈**−50%** ajustado por mercado a 18 meses | [41][42] | A |
| Gahng, Ritter, Zhang | 2023 | SPACs | RFS (sep-2023) | 458 IPOs de SPACs 2010-2020, comprando la unidad en la IPO y vendiendo o redimiendo 5 días antes del cierre ("redención óptima"): **23.9%** anual promedio EW (33.2% si fusiona, 2% si liquida); advierten que las cohortes 2021+ rendirán mucho menos. El **9.3%** del artículo es el rendimiento a un año de los inversionistas **PIPE**, no del de la IPO | [43] | B |
| Barber, Huang, Odean, Schwarz | 2022 | Attention-Induced Trading and Returns: Robinhood | JF 77(6) | Top compras diarias: **−4.7%** anormal a 20 días; herding extremo: +42% el día y −9% a 20 días | [44] | B |
| Bali, Hirshleifer, Peng, Tang, Wang | 2021 (rev. nov-2025) | Social Interactions and Lottery Stock Mania | NBER w29543 | Más actividad en redes predice alzas diarias extremas; esas acciones reciben más compras minoristas (sobre todo de Robinhood) y luego rinden menos | [45] | B |
| Jajal et al. | 2026 | Global Merger-Arbitrage Forecasting with Language Models | ICML 2026 / arXiv | Brier balanceado por clase **0.151** (3 desenlaces, >400 tratos, 42 países); 24% debajo de las probabilidades implícitas calibradas del mercado | [46] | C |

---

## 4. Lo más reciente 2023-2026

1. **El efecto índice ya es historia académica.** Greenwood y Sammon (JF 80(2), abril 2025): de 7.4% en los 90 a menos de 1% en 2010-2020, pese a que hay más dinero indexado que nunca; la causa es que mesas de trading e indexadores anticipan y proveen liquidez [9]. Los saltos idiosincráticos siguen existiendo (Robinhood +15.8% y AppLovin +11.6% del cierre del 5-sep al del 8-sep-2025, anuncio tras el cierre del viernes [49][71]), pero ocurren en after-hours y en la primera sesión: no son capturables para un operador manual.
2. **PEAD: guerra de diseño de investigación.** Dickerson-Julliard-Mueller (JFE, en prensa en 2025) y Hirshleifer-Peng-Wang (RFS 38(3), 2025, t≈14) sostienen que la deriva está viva. Subrahmanyam la replica para feb-2001 a dic-2024: t = 2.18 con todas las acciones y **t = 1.43 sin microcaps** (el 20% inferior por capitalización de la NYSE, ~3% del valor de mercado) [35]. Veredicto operativo: muerta en lo invertible; viva, si acaso, donde el costo la anula.
3. **Insiders tras la reforma 10b5-1 (vigente desde feb-2023).** Kim, Kim y Rajgopal (2025): las ventas ejecutadas dentro de los 90 días posteriores a adoptar un plan pasaron de **31.1% a 1.7%**; el uso de planes bajó de 52.5% a 50.3% de las ventas; los retornos anormales negativos tras ventas bajo plan se volvieron planos o ligeramente positivos [47]. Ese estudio trata solo **ventas**; la afirmación de que el contenido informativo de las **compras** no cambió tras la reforma no tiene fuente verificada y no se usa en ninguna regla (no verificado). Oenschläger-Möllenhoff (FRL 2025): con montos por señal realistas, la ganancia se vuelve negativa [22]. Zhao (arXiv 2026): la reacción se agota en 2-3 sesiones [23].
4. **Estudio de proveedor (grado D, útil como contraste):** 47,458 compras de insiders (2020-2025): +2.56% a un año sobre la acción mediana, pero **no sobrevive a un placebo** de ventana desplazada 180 días (t < 2), y las compras más grandes rinden 17.1 pp **menos** que las más chicas [48]. Sin ajuste por riesgo y con sesgo de supervivencia.
5. **Reglas de divulgación.** 13D a 5 días hábiles (antes 10 días), enmiendas en 2 días hábiles (feb-2024); 13G acelerado con cumplimiento desde el 30-sep-2024 [53]. Form SHO (cortos institucionales): el Quinto Circuito remitió la Regla 13f-2 a la SEC el 25-ago-2025 y el primer reporte se pospuso al 14-feb-2028 (antes 17-feb-2026) [55].
6. **Congreso.** Wei-Zhou (NBER, 2025): los líderes superan a sus pares por **47 pp/año** después de ascender, por canales de influencia política y acceso corporativo [40]. En contraste, los ETFs de "copiar al Congreso" desde su lanzamiento (7-feb-2023) al 24-sep-2026: NANC +108.8% (CAGR 22.5%), GOP (antes KRUZ) +81.9% (17.9%), SPY +93.7% (20.0%), QQQ +144.3% (27.9%) (cálculo propio, §5.2). NANC tiene ~30% en cinco megacaps tecnológicas (NVDA 8.67%, MSFT 6.45%, GOOG 5.92%, AMZN 4.80%, AAPL 4.52%) y un TER de 0.72% [56]. Inferencia: su resultado es beta tecnológica, no información privilegiada.
7. **Merger arbitrage: régimen regulatorio.** En 2023-2024, la FTC y la CMA tomaron una postura agresiva en tratos emblemáticos (iRobot/Amazon terminado en ene-2024; demanda contra Kroger/Albertsons en feb-2024: fechas no reverificadas en esta sesión) y, según Associated Capital (Gabelli), al cierre de 2024 "los spreads están en sus niveles más anchos en años" [57]. En 2025 hubo pocas rupturas y el HFRI ED: Merger Arbitrage ganó **8.2%** hasta septiembre, su mejor arranque de tres trimestres desde 2021 [58] (fuente no reverificada: 403). Lección: el riesgo principal del merger arb es **regulatorio y de régimen**, no de mercado.
8. **SPAC 2.0.** Reglas de la SEC vigentes desde julio de 2024 (sin safe harbor para proyecciones). Según FTI, 138 SPACs recaudaron US$25.8 mil millones en 2025, casi el triple de los US$8.7 mil millones de 2024, y fueron el 40% de las IPOs de EUA por número (27% en 2024); en ene-feb de 2026, 50 SPACs más recaudaron US$10 mil millones [59]. La participación de patrocinadores seriales y las estructuras con menos warrants no se verificaron. Pero los deSPACs siguen destruyendo valor: **−59.1%** (cohorte 2023, 98 tratos), **−62.0%** (2024, 71) y **−55.7%** (2025, 43), medido desde un precio supuesto de US$10 hasta el cierre del 31 de diciembre (Ritter, Tabla 15c, actualizada el 29-jul-2026 [60]).
9. **IPOs.** 2025: 90 IPOs de empresas operativas, primer día promedio **29.3%** (15.3% en 2024; promedio 1980-2025 de 19.0%, mediana 7.0%) [11]. Cohortes 2012-2024 (1,645 IPOs): 3 años desde el primer cierre +7.6% bruto, **−25.5%** vs mercado y **−16.7%** vs estilo [12].
10. **Meme stocks, versión 2025.** Opendoor pasó de US$0.53 (cierre del 30-jun-2025) a US$3.21 el 21-jul (≈6 veces) y cerró julio en US$1.84 (≈3.5 veces) (Yahoo [71]); la cifra de ~49% del flotante de Kohl's en corto y ~21% de Opendoor viene de [61] (no reverificada: fuente con error 503). La evidencia académica sobre compras por atención es consistentemente negativa: las posiciones abiertas cuando la atención en r/wallstreetbets está en su máximo realizan **−8.5%** (Warkulat-Pelster, IRFA 2024 [62]); las recomendaciones de Reddit muestran alfa positivo a 1-3 meses y negativo y significativo a un año (Reichenbach-Walther, Digital Finance 2023 [63]).
11. **México: OPAs vivas.** Vinte adquirió el 99.92% de Javer (4,288 mdp) vía OPA forzosa y el desliste de la BMV se aprobó con 99.94% de los votos (nota del 5-feb-2025) [64]. Pantera Holdings (vehículo de accionistas existentes, vinculado a Aby Lijtszain Chernizky, presidente ejecutivo y cofundador de Traxión) lanzó una **OPA voluntaria a MXN 13.18** por hasta 542.38 millones de acciones (7,148.6 mdp), prima de 20.4% sobre el precio promedio ponderado por volumen de 60 días (10.95); periodo de aceptación del 22-sep al 20-oct-2026, liquidación prevista el 23-oct-2026 y opinión del consejo hacia el 6-oct; la oferente declara que **no** busca cancelar la inscripción [65][66]. El precio saltó de 11.06 a 12.53 (+13.3%) el 15-sep-2026, antes del periodo de aceptación (Yahoo [71]). Es el caso de laboratorio del §6.
12. **IA aplicada.** Un sistema LLM ajustado queda 24% por debajo (Brier balanceado por clase) de las probabilidades implícitas calibradas del mercado para predecir el desenlace de fusiones [46]. Es la primera evidencia seria de que la lectura masiva de documentos (proxy, acuerdos, condicionantes regulatorios) da ventaja en esta clase de activos. Grado C mientras no haya track record fuera de muestra con dinero real.

---

## 5. Evidencia real: qué funciona, qué no, magnitudes

### 5.1 Catálogo de señales (el mapa que hay que memorizar)

| Señal | Magnitud original | Hoy (post-publicación, neto) | Latencia / costos | Datos | ¿Vía SIC en GBM? | Grado |
|---|---|---|---|---|---|---|
| **Merger arb en efectivo (EUA)** | 4%/año sobre riesgo tras costos (1963-98) [1]; 0.6-0.9%/mes (1981-96, no verificado) [2] | ETFs 2016-2026: CAGR 2.8-4.2% vs 2.3-2.8% de T-bills [§5.2]; spread −400 pb desde 2002 [3] | Spread de 2-5% por trato (práctica de mercado, no verificado); no consumación de 9-12% [4] | 8-K, DEFM14A, SC TO-T | Solo si el objetivo está en el SIC; **el riesgo USDMXN domina el spread**. MNA, MRGR y ARB no aparecen con cotización .MX en Yahoo (indicio, no prueba de que falten en el SIC) | B |
| **Merger arb en acciones** | Igual | Igual | Requiere corto del adquirente | S-4, 425 | **En la práctica, no**: GBM ofrece venta en corto con margen solo en emisoras que selecciona y con mínimo de 10,000 MXN (parcialmente verificado en `arena/investigacion/01-gbm-operativa-y-costos.md`); no hay garantía de poder shortear un adquirente específico | — |
| **OPA en BMV/BIVA** | Sin estudio académico local verificado | Caso a caso (prima de 20.4% sobre el VWAP de 60 días en Traxión [66]; el rango 20-35% es inferencia, no verificado) | Spread en MXN; 0.29% por lado; costo de aceptar la OPA en GBM no verificado | Eventos relevantes, folleto | **Sí** | C |
| **Spin-offs (comprar la hija)** | +33.6% a 3 años (1965-88) [5] | No sobrevive a pruebas refinadas [7]; CSD 2016-2026: CAGR 12.4% vs 15.3% del SPY, beta 1.15, MDD −57.5% [§5.2]; hijas de la década previa −2.7%/año vs S&P a 2019 [67] | Presión vendedora de 1-3 semanas; −1.7% a 14 días [50] | Form 10, 8-K | Si listada en el SIC (con rezago) | C |
| **Inclusión en el S&P 500 (post-anuncio)** | ≈3% (Shleifer, 1976-83) → 7.4% (90s) [8][9] | **<1%** (2010-2020) [9] | Salto en after-hours | Comunicados de S&P DJI | Sí, pero no capturable | D |
| **Anticipar inclusiones** | — | Sin estudio verificado de rendimiento neto | Requiere modelar elegibilidad | Reglas del índice | Sí | C (no verificado) |
| **Comprar IPOs en el aftermarket** | 34.47% vs 61.86% a 3 años [10] | 1980-2024: −20.5% vs mercado, −8.9% vs estilo; 2012-2024: −25.5% / −16.7% [12]; no rentables: −30.7% / −23.4% | Primer día promedio 18.9% capturado solo por quien recibe asignación | S-1, 424B | Sí (evitar) | **B como filtro** |
| **Asignación en IPO a precio de oferta** | Primer día promedio 19.0% (1980-2025) [11] | 2025: 29.3% | Inaccesible para minoristas en México | — | No | A (inaccesible) |
| **SEOs / emisión neta** | 7%/año vs no emisores (5 años) [13] | Emisión neta sigue como predictor negativo [14] | Largo plazo | 424B, Compustat | Solo como filtro | B |
| **Recompras (anuncio)** | +12.1% a 4 años; value +45.3% [15] | **Desaparece post-2002/2003** [17][18]; PKW 2016-2026: 13.2% vs 15.3% del SPY [§5.2] | — | 8-K, 10-Q | Sí | C |
| **Compras de insiders** | >6%/año (retorno del insider) [20]; oportunistas +82 pb/mes [21] | Positivo bruto y concentrado en small/microcaps; **negativo al escalar** [22]; reacción de 1-3 días [23] | 2 días hábiles; microcaps ilíquidas | Form 4 | Mayormente **no**: el SIC cubre sobre todo grandes caps (al menos 395 de las 503 del S&P 500 [72]); que las microcaps no estén es inferencia no verificada. GBM Trading USA (custodia DriveWealth) podría dar acceso fuera del SIC; cobertura no verificada | B bruto / C neto |
| **Ventas de insiders** | ~0 [19][20] | Aún menos tras la reforma 10b5-1 [47] | — | Form 4 | — | D |
| **Clonar 13F / best ideas** | +2.8-4.5%/año (best ideas) [24]; +3.8%/año (Barclays) [26] | GVIP 2016-2026: 16.1% vs 15.5% del SPY con beta 1.11 (≈0 alfa); GURU: 12.0% vs 15.3% [§5.2] | 45-135 días de rezago | 13F-HR | Sí (grandes caps) | C |
| **Short interest agregado (timing)** | R² OOS 13.24% anual [27] (OOS dentro de la muestra original) | Sin evidencia post-publicación verificada | Mensual/quincenal | FINRA | Solo como insumo de exposición | **C** (B el paper; sin prueba post-publicación no puede ser B operativo) |
| **Short interest / DTC transversal** | −1.16% en 20 días [28]; DTC 1.2%/mes [29] | Vivo en el lado corto (caro) | Préstamo de acciones | FINRA | **Solo como filtro** | B como filtro |
| **Activismo 13D** | ≈7% en (−20, +20) [30][31] | Buena parte ocurre antes del filing; el plazo ahora es de 5 días hábiles | Filing público | SC 13D | Sí (large/mid caps) | B anuncio / C post-filing |
| **Prima de anuncio de resultados** | 9.9% anual [32] | **Desaparecida en EUA**, migró a los 8-K [33] (WP, detalle no reverificado) | Rotación alta | Calendario de resultados | Sí | C |
| **PEAD** | Clásico | Muerto en large caps desde 2006 [34]; t = 1.43 sin microcaps [35] | Rotación alta | 8-K / consenso | Sí | C |
| **Revisiones de analistas** | Cambios del consenso: predictor robusto [37] | Proveedor: decil superior − inferior 7.6%/año bruto de costos, sep-2003 a ene-2023, universo global (~60% fuera de EUA) [68] | Datos de pago (I/B/E/S) | Consenso | Sí | B (señal compuesta) |
| **Copiar al Congreso** | Senado +85 pb/mes (1993-98) [38] | Congreso −2 a −3%/año (2004-08) [39]; ETFs = beta tecnológica | 45 días; montos en rangos | PTRs | NANC y GOP sin cotización .MX en Yahoo (indicio, no prueba; no verificado en BMV) | D |
| **Líderes del Congreso** | +47 pp/año vs pares [40] | Sin prueba implementable con 45 días de rezago | 45 días | PTRs | — | C |
| **Comprar deSPACs** | −50% ajustado a 18 meses [41] | −55.7% a −62.0% desde US$10 al cierre de diciembre (cohortes 2023-2025) [60] | — | S-4, 8-K | Sí (evitar) | **A como filtro** |
| **SPAC antes de la fusión (con redención)** | 23.9% anual EW, IPOs de SPAC 2010-2020 [43] | Los autores advierten rendimientos mucho menores desde 2021; sin cifra post-2021 verificada | Unidades y warrants; compra en la IPO | S-1 | Que unidades y warrants de SPACs se negocien en el SIC: no verificado (asignación en la IPO: inaccesible) | B (inaccesible) |
| **Comprar picos de atención/meme** | Robinhood: −4.7% a 20 días [44] | WSB en pico: −8.5% [62] | Volatilidad extrema | Redes, flujos | Sí (evitar) | **B como filtro** |

### 5.2 Lo que dicen los vehículos reales (dinero invertible, neto de TER)

Cálculo propio con precios ajustados de Yahoo Finance al 24-sep-2026, en USD y con dividendos reinvertidos. En MXN hay que sumar la variación del USDMXN, cuya volatilidad realizada fue de 10.8% anual en 5 años y ≈8.1-8.2% en el último año; en la ventana de 5 años, el cambio a 84 días hábiles tuvo p5 = −7.6% y p95 = +10.7% (en 10 años: −8.9% y +12.3%). Recalculado en la verificación del 25-sep-2026 con la misma fuente: CAGR, beta, MDD, Sharpe y años sueltos coinciden con la tabla dentro de ±0.1 pp.

| Vehículo | Qué replica | Periodo | CAGR | SPY mismo periodo | Beta vs SPY | MDD |
|---|---|---|---|---|---|---|
| MNA | Merger arbitrage (índice) | sep-2016 a sep-2026 | 2.8% | 15.3% (BIL 2.3%) | 0.18 | −16.7% |
| MRGR | Merger arbitrage | sep-2016 a sep-2026 | 3.6% | 15.3% | 0.10 | −13.2% |
| ARB | Merger arbitrage activo | may-2020 a sep-2026 | 4.2% | 18.0% (BIL 2.8%) | 0.08 | −5.6% |
| CSD | Spin-offs ≤4 años, >US$1 mil millones | sep-2016 a sep-2026 | 12.4% | 15.3% | 1.15 | −57.5% |
| IPO | IPOs recientes | sep-2016 a sep-2026 | 10.0% | 15.3% | 1.30 | −68.8% |
| PKW | Recompras | sep-2016 a sep-2026 | 13.2% | 15.3% | 0.99 | −40.9% |
| GURU | Clon de 13F | sep-2016 a sep-2026 | 12.0% | 15.3% | 1.03 | −38.5% |
| GVIP | "VIP" de hedge funds | nov-2016 a sep-2026 | 16.1% | 15.5% | 1.11 | −37.1% |
| NANC | Congreso, demócratas | feb-2023 a sep-2026 | 22.5% | 20.0% (QQQ 27.9%) | — | −20.9% |
| GOP (ex-KRUZ) | Congreso, republicanos | feb-2023 a sep-2026 | 17.9% | 20.0% | — | −20.7% |

Lecturas (Inferencia):
- **Merger arb** en vehículos líquidos entregó T-bills + ~0.5-1.5 pp con Sharpe contra BIL de 0.11 (MNA) y 0.27 (MRGR), frente a 0.76 del SPY. Sigue siendo una prima, pero pequeña después de TER. Años negativos: 2021 (−3.2%) y 2022 (−1.6%) en MNA. En MXN, el ruido cambiario de un trimestre (±8-11%) es varias veces el spread típico de un trato estadounidense.
- **Spin-offs, IPOs, clones de 13F y recompras**: todos por debajo del SPY o iguales con más beta. Ninguno muestra alfa invertible en la década.
- **GVIP** es el único arriba del SPY, y con beta de 1.11 eso es aproximadamente cero alfa. Los años 2022 (−31.9%) y 2020 (+44.1%) muestran que es una apuesta de factor (crecimiento/momentum de megacaps).
- **ETFs del Congreso**: NANC le gana al SPY, pero pierde contra el QQQ; es un portafolio tech ponderado.

### 5.3 Magnitudes que no están en la tabla

- **Asimetría del merger arb**: se gana 2-5% por trato en 3-9 meses; un objetivo roto cae típicamente 20-40% en una sesión (práctica de mercado, **no verificado**: no se encontró estudio académico con esa distribución). Ejemplo: Shutterstock (SSTK) cayó −29.0% el 1-jul-2026 (precios de Yahoo [71]); que la causa fuera la terminación del trato con Getty no se verificó con fuente primaria. Con G de 2-5% y L de 20-40%, un trato roto borra entre 4 y 20 éxitos (L/G). El sustituto operativo de esa cifra es B, el precio previo al anuncio, que se mide caso por caso.
- **IPOs**: medido desde el **precio de oferta**, el rendimiento ajustado por estilo a 3 años es +8.3%; desde el primer cierre, −8.9% [12]. Todo el valor está en la asignación. Las no rentables con ventas <US$100 millones: −40.9% vs mercado.
- **deSPACs 2012-2022** (451): −46.3% a un año (−49.4% ajustado por mercado) y −57.7% a tres años (−74.7% ajustado) en promedio [60].

---

## 6. Traducción operable (reglas, checklists, parámetros)

Todas las cifras de riesgo vienen de `config/parametros.json`. En **fase 0** (`prioridad_actual`) nada de esto se ejecuta con dinero: se opera en papel, se registran pronósticos y se mide el Brier. Este módulo no crea límites nuevos; donde propongo un umbral de selección, lo marco como **criterio**.

**R1. Prueba de vida de una señal de evento (obligatoria antes de cualquier backtest).** Una señal entra al satélite solo si pasa las seis preguntas:
1. ¿Tiene evidencia **post-publicación** positiva (no solo el paper original)?
2. ¿Sobrevive **sin microcaps** (sin el 20% inferior por capitalización de la NYSE)?
3. ¿La deriva empieza **después** de mi latencia real (dato público + mi tiempo de proceso + ejecución manual al día siguiente)?
4. ¿Es rentable con **0.29% por lado** (comisión GBM de 0.25% + IVA, en montos de 1 mil a 1 millón de pesos [69]) más el spread bid-ask del SIC?
5. ¿La emisora está en el **SIC** y la estrategia **no requiere corto**?
6. ¿El **riesgo USDMXN** del horizonte es menor que el edge esperado? Medir siempre 1 + R_MXN = (1 + R_USD) × (FX_final/FX_inicial). Si no, la señal es una apuesta cambiaria disfrazada.
Además: `validacion_estrategias` (≥10 años de backtest con costos, deflated Sharpe ≥0.95, PBO ≤0.25, ≥3 meses y ≥30 operaciones en papel).
Resultado actual del catálogo: ninguna señal de compra de §5.1 pasa las seis. Las OPAs mexicanas pasan de la 3 a la 6, pero no tienen evidencia sistemática (pregunta 1): se tratan como pronósticos en papel hasta acumular historial propio. Los filtros de exclusión no son señales de compra y se aplican de inmediato.

**R2. Filtros de exclusión permanentes (aplican a todo el portafolio, núcleo y satélite).** Son la parte de grado A/B del módulo:
- No comprar IPOs en sus primeros **36 meses** de cotización, salvo evidencia fundamental excepcional documentada. Prioridad de exclusión: empresas no rentables con ventas <US$100 millones [12].
- No comprar **deSPACs** en sus primeros 36 meses [60].
- No abrir posiciones en una acción **el día** de un pico de atención (top de volumen minorista, tendencia en redes, +20% o más en el día) ni en los 20 días siguientes [44][62]. **Criterio**: el umbral de +20% es mío, no del paper.
- Castigar en el ranking a los emisores netos de acciones (SEO, ATM, dilución por compensación) [13][14].
- Evitar posiciones largas en acciones con **days-to-cover** en el decil superior, salvo tesis de squeeze explícita y dimensionada como lotería [29].
- Ignorar ventas de insiders (sobre todo bajo 10b5-1) y ETFs de "copiar al Congreso" como fuentes de señal.

**R3. Merger arbitrage / OPA: calculadora obligatoria.** Para cada situación se registra en la bitácora:
- O, P, B (precio previo al anuncio, ajustado por el sector), d (días a la liquidación según el folleto), condiciones (mínimo de aceptación, autorizaciones de COFECE/CNBV/FTC/DOJ, financiamiento, voto).
- G, L, p\*, anualizado y **p propia** con justificación escrita. Base de referencia: 88-91% de consumación [4] (Ricks-Lin miden no consumación; la tasa de cierre **en los términos originales** es menor e incluye renegociaciones: no verificada), ajustada por riesgo regulatorio, financiamiento y régimen de crédito. Es una tasa de EUA con acuerdos definitivos; para OPAs mexicanas no hay tasa base verificada.
- Operar solo si: (a) p − p\* ≥ 3 pp (**criterio**); (b) anualizado neto de costos e ISR > CETES 28 + 3 pp (**criterio**); (c) trato en efectivo o canje cubrible; (d) para objetivos de EUA vía SIC, G del plazo > 2 × σ_USDMXN × √(d/365); con σ ≈ 10% y d = 120 días se necesita G > 11%, lo que en la práctica excluye el arbitraje estadounidense sin cobertura, salvo que se acepte explícitamente como apuesta al USD.

**R4. Tamaño por pérdida en ruptura (no por volatilidad).** El "stop" real de un arbitraje es el precio de ruptura B.
- Nocional máximo = (riesgo por operación × Capital) / L.
- Perfil `arena_agresivo`: riesgo por operación 0.03 y acción individual ≤ 0.30. Perfil estándar: 0.01 (0.005 en fase de prueba) y ≤ 0.10.
- Kelly: en apuestas binarias con G chico y L grande, el Kelly teórico sale con apalancamiento; está **acotado** por `kelly.fraccion_max` (0.25 estándar, 0.5 arena) y por la concentración. La incertidumbre sobre p domina: usar Kelly sobre p − 5 pp (**criterio**).
- Límite de cartera: suma de L × nocional de todos los arbitrajes abiertos ≤ límite mensual de pérdida (0.06 estándar, 0.18 arena), porque las rupturas se correlacionan en crisis de crédito y cambios de régimen regulatorio [1][57].

**R5. Caso de laboratorio en papel: OPA de Traxión (fase 0, sin dinero real).** Datos al 24-sep-2026: P = 12.90 (último precio del 24-sep, Yahoo; igual al cierre del 23-sep); O = 13.18 [65][66]; B ≈ 11.00 (cierres del 8 al 14 de septiembre, entre 10.90 y 11.09; VWAP de 60 días de 10.95 según [66]); liquidación prevista el 23-oct-2026 (29 días naturales).
- G = 2.17% bruto; neto de 0.29% de compra ≈ 1.88% (costo de aceptar la OPA en GBM: **no verificado**); ≈24% anualizado simple en 28-29 días.
- ISR: el 10% definitivo del art. 129 LISR aplica a enajenaciones en bolsa concesionada. El propio art. 129 lo **excluye** cuando la enajenación se hace "fuera de las bolsas señaladas" o "como operaciones de registro o cruces protegidos" que impidan aceptar ofertas más competitivas (numeral 3), y la LISR vigente (últ. ref. DOF 01-04-2024) no contiene una disposición expresa sobre OPAs [73]. Si la aceptación de esta OPA se liquida como operación en bolsa que califique para el 10%, o cae en la exclusión, depende de la mecánica del folleto y de reglas misceláneas: **no verificado; consultar con contador antes de cualquier operación real** [70][73]. Para el marcador (TWR) no cambia nada durante la temporada, porque el ISR se paga en la declaración anual.
- p\* = 1.90/2.18 = **87%**; L = 14.7%.
- Tamaño arena teórico = 0.03 × 20,000 / 0.147 ≈ **4,080 MXN** (20% de la cuenta, debajo del 30% individual). **Choque con `orden_minima_mxn` = 5,000**: la orden mínima del perfil arena excede el tamaño por riesgo; con 5,000 MXN el riesgo de ruptura sería 5,000 × 0.147 ≈ 735 MXN = **3.7% del capital > 3%** permitido. Con los parámetros actuales esta OPA **no es ejecutable** en la cuenta arena salvo que L baje (P más cerca de B) o se cambie el parámetro con el dueño. Ganancia esperada si cierra con 4,080 ≈ 77 MXN neta de la compra. Inferencia: con 20 mil pesos, las situaciones especiales valen como **sustituto de CETES con cola**, no como motor de ganancia.
- Tarea: registrar hoy p propia, fecha y fuentes; al liquidarse, calcular el Brier. En el folleto quedan **sin verificar**: condiciones de terminación, mínimo de aceptación y prorrateo. Liquidez residual: la regulación exige mantener al menos 12% del capital entre el público y un mínimo de 100 inversionistas para conservar el listado [65]; si el flotante baja de ahí, la permanencia en bolsa podría reconsiderarse aunque la oferente declare que no busca deslistar [65][66].

**R6. Uso en el torneo (`modo_torneo`).**
- **Adelante del mejor rival por ≥5 pp**: se permite rotar parte de la liquidez a OPAs o arbitrajes en MXN con p\* ≥ 85% y d ≤ 60 días, que bajan la varianza relativa frente a rivales que probablemente estén en renta variable. **Criterio.**
- **Atrás por ≥5 pp**: está prohibido "buscar la remontada" con IPOs, meme stocks o deSPACs; su valor esperado es negativo [12][44][60]. Subir exposición se hace con los instrumentos y filtros de otros módulos, dentro de los límites de `arena_agresivo`.
- Cada arbitraje consume `operaciones_max_mes` (8): la entrada y la salida (venta en mercado o aceptación de la OPA) cuentan como dos operaciones (**criterio**: que la aceptación de una OPA cuente como operación no está definido en `config/parametros.json`). También debe respetar `orden_minima_mxn` (5,000) y `rotacion_max_mensual_x_capital` (1.5).

**R7. Pipeline de datos (para la rutina de escaneo, en papel).**
- **EDGAR**: feed de filings recientes por tipo (`https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4&output=atom`, cambiando `type`); JSON por emisora en `https://data.sec.gov/submissions/CIK##########.json` (CIK de 10 dígitos con ceros a la izquierda); conjuntos trimestrales de Forms 3/4/5 [51]. La SEC exige un User-Agent identificable. (Los tres endpoints respondieron HTTP 200 el 25-sep-2026.)
- **Filtro Form 4 útil**: código P (compra en mercado abierto), no 10b5-1, consejero o directivo, clúster de ≥2 insiders en 30 días, empresa **en el SIC**. Registrar la señal y medir la deriva a 1, 5, 20 y 60 días en papel antes de considerarla. Hipótesis a falsar con placebo de ventana desplazada [48].
- **13F**: solo como contexto (consenso de gestores de horizonte largo), nunca como gatillo; el dato tiene 45-135 días.
- **Congreso**: `https://disclosures-clerk.house.gov/FinancialDisclosure` (Cámara) y `https://efdsearch.senate.gov/search/` (Senado; redirige a una página de aceptación de términos); ambos respondieron el 25-sep-2026. Uso analítico, no operativo.
- **FINRA**: `https://www.finra.org/finra-data/browse-catalog/equity-short-interest` (respondió el 25-sep-2026).
- **Short interest FINRA** agregado: insumo para el módulo de exposición (Módulo 06/08), no gatillo transversal.
- **México**: eventos relevantes BMV/BIVA con alertas por "OPA", "oferta pública de adquisición", "desliste", "escisión", "fusión".

**R8. Registro y calibración.** Toda situación especial genera un pronóstico probabilístico (cierre en términos / mejora / ruptura) que entra al contador de `pronosticos` (Brier objetivo ≤0.20, mínimo 50 pronósticos). Referencia, no meta directa: el 0.151 de Jajal et al. [46] es un Brier **balanceado por clase sobre tres desenlaces**, no comparable uno a uno con el Brier binario del contador. La prueba correcta es relativa: si después de 50 pronósticos nuestro Brier no es menor que el Brier de p\* (la probabilidad implícita del mercado) en los mismos tratos, no hay edge y la estrategia no pasa a capital real.

**Checklist de 60 segundos ante cualquier "noticia corporativa":**
1. ¿Qué motor es (seguro, presión, información, atención)? 2. ¿Qué parte del CAR ya pasó? 3. ¿Mi latencia me deja la deriva? 4. ¿Está en el SIC y es solo largo? 5. ¿Costos + FX + ISR < edge? 6. ¿Qué dice el filtro de exclusión R2? 7. ¿Cuál es mi p y cuál es p\*? Si alguna respuesta es "no sé", no hay operación.

---

## 7. Trampas y errores comunes

1. **Confundir el retorno del insider con el del imitador.** Jeng-Metrick-Zeckhauser miden lo que gana el insider [20]; el imitador llega 2 días hábiles tarde y paga la reacción [22][23].
2. **Backtests sin placebo.** Las compras de insiders "ganan" a la mediana también cuando la ventana se desplaza 180 días: la señal es el tipo de empresa, no el momento [48].
3. **Incluir microcaps y reportar "significancia".** El PEAD pasa de t = 2.18 a 1.43 al excluirlas [35]; las compras de insiders viven en firmas pequeñas [19]; esas firmas casi nunca están en el SIC.
4. **Benchmark equivocado en largo plazo.** IPOs: −20.5% vs mercado, pero −8.9% vs estilo [12]. Exigir calendar-time con factores.
5. **Tratar el merger arb como renta fija.** Es un put vendido: correlación que sube en crisis [1], rupturas agrupadas por régimen regulatorio [57], y en MXN, riesgo cambiario mayor que el spread.
6. **Arbitrar un trato en acciones sin cubrir.** Sin corto del adquirente es una posición direccional.
7. **Anualizar spreads cortos sin sumar la cola.** El 24% anualizado de una OPA con L = 14.7% es un rendimiento **condicional** a que cierre.
8. **Creer en ETFs temáticos por su narrativa.** NANC = beta tecnológica; GVIP ≈ SPY con beta 1.11; CSD, IPO, GURU y PKW por debajo del SPY en 10 años [§5.2].
9. **Perseguir la inclusión al índice o un caso famoso** (Robinhood +16%, Opendoor ×5). El salto ocurre en after-hours; el efecto promedio post-anuncio es <1% [9][49]. El promedio es lo que paga; el caso es lo que se recuerda.
10. **Leer 13F como si fueran posiciones actuales.** Llegan hasta 45 días después del trimestre, sin cortos ni derivados completos, y el gestor puede haber salido ya.
11. **Olvidar las condiciones del folleto.** Mínimos de aceptación, autorizaciones (COFECE, CNBV, FTC/DOJ), MAC, financiamiento y prorrateo definen p; el titular de prensa no.
12. **Dar por muerta toda señal.** Las **primas** (merger arb) y los **filtros** siguen vivos; lo que murió fue la deriva fácil de capturar.

---

## 8. Examen de titulación

1. **Una OPA en efectivo ofrece 13.18; la acción cotiza en 12.90 y cotizaba en 11.00 antes del anuncio. ¿Cuáles son p\*, G y L?**
   p\* = (12.90 − 11.00)/(13.18 − 11.00) = **87%**; G = **2.17%**; L = **14.7%**.

2. **En el ejemplo anterior, con perfil `arena_agresivo` y capital de 20,000 MXN, ¿cuál es el nocional máximo por riesgo?**
   0.03 × 20,000 / 0.147 ≈ **4,080 MXN**, debajo del 30% de acción individual, pero **debajo de `orden_minima_mxn` (5,000)**: con la orden mínima el riesgo sería ≈3.7% del capital (> 3%), así que con los parámetros actuales no se ejecuta.

3. **¿Qué encontraron Mitchell y Pulvino sobre la correlación del merger arb con el mercado y cuánto exceso queda neto de costos?**
   Nula en mercados planos o alcistas y **positiva en caídas severas** (como vender puts de índice descubiertos); **4%/año** de exceso tras controlar la no linealidad y los costos.

4. **¿Cuánto se comprimió el spread de merger arb después de 2002 y por qué?**
   Más de **400 pb**; coincide con más entradas de capital a fondos de merger arb, más volumen negociado en las acciones objetivo tras el anuncio, menores costos de transacción y cambios en el riesgo (Jetley-Ji, FAJ 2010).

5. **¿Cuál era el efecto de inclusión al S&P 500 en los 90 y cuál en 2010-2020? ¿Por qué cayó?**
   **7.4% → <1%**; mejor anticipación y provisión de liquidez por mesas y grandes indexadores (Greenwood-Sammon, JF 2025).

6. **Según los datos de Ritter (1980-2024), ¿cuánto rinde una IPO a 3 años desde su primer cierre contra el mercado y contra el estilo? ¿Qué implica esa diferencia?**
   **−20.5%** vs mercado y **−8.9%** vs firmas pareadas por tamaño y B/M; buena parte de la "anomalía" es exposición a small-growth.

7. **¿Qué parte de las operaciones de insiders contiene información según Lakonishok-Lee y Cohen-Malloy-Pomorski?**
   Las **compras** (no las ventas), concentradas en firmas pequeñas; dentro de ellas, las **oportunistas** (+82 pb/mes VW); las rutinarias, ~0.

8. **¿Por qué no basta que las compras de insiders predigan rendimientos para que imitarlas sea rentable hoy?**
   Latencia de 2 días hábiles, reacción concentrada en 1-3 sesiones y ganancia que se vuelve negativa con montos realistas (Oenschläger-Möllenhoff 2025; Zhao 2026).

9. **¿Qué pasó con la anomalía de recompras de Ikenberry-Lakonishok-Vermaelen después de 2002?**
   Fu-Huang (MS 2016) y Lee-Park-Pearson (JCF 2020) documentan que el exceso de largo plazo **desaparece** o se reduce mucho después de 2001-2003.

10. **¿Qué predictor agregado propusieron Rapach-Ringgenberg-Zhou y con qué R² fuera de muestra?**
    Short interest agregado; **13.24%** anual fuera de muestra (12.89% in-sample).

11. **¿Por qué un ETF de "copiar al Congreso" que le gana al S&P 500 no prueba información privilegiada?**
    Porque su exceso se explica por concentración en megacaps tecnológicas (NANC < QQQ desde 2023), porque el promedio del Congreso perdió 2-3%/año (Eggers-Hainmueller) y porque los PTRs llegan con hasta 45 días de rezago y en rangos.

12. **¿Qué predice el efectivo neto por acción de un SPAC y cuál fue el rendimiento a un año de los deSPACs 2023-2025?**
    Predice casi uno a uno el valor posterior a la fusión: un dólar menos de efectivo neto, un dólar menos de valor (mediana de US$5.70 por cada US$10 en ene-2019 a jun-2020); **−59.1%, −62.0% y −55.7%**, medidos desde US$10 al cierre de diciembre (Ritter, Tabla 15c).

13. **Robinhood: ¿qué rendimiento anormal siguen las acciones más compradas del día?**
    **−4.7% a 20 días**; en herding extremo, +42% el día y −9% a 20 días.

14. **¿Está vivo el PEAD? Da la respuesta operativa en una línea.**
    No en lo invertible: muerto en large caps desde 2006 (Martineau) y no significativo sin microcaps en 2001-2024 (t = 1.43).

15. **¿Por qué un arbitraje de un objetivo estadounidense vía SIC puede no ser "bajo riesgo" medido en MXN?**
    Porque el cambio del USDMXN a ~4 meses tuvo p5/p95 de −7.6%/+10.7% (volatilidad de 8-11% anual), varias veces el spread típico de 2-5%.

---

## 9. Fuentes

1. Mitchell, Pulvino (2001), JF 56(6): https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00401 ; AQR: https://www.aqr.com/Insights/Research/Journal-Article/Characteristics-of-Risk-and-Return-in-Risk-Arbitrage
2. Baker, Savasoglu (2002), JFE 64(1): https://ideas.repec.org/a/eee/jfinec/v64y2002i1p91-115.html ; HBS: https://www.hbs.edu/faculty/Pages/item.aspx?num=9180
3. Jetley, Ji (2010), FAJ 66(2): https://rpc.cfainstitute.org/research/financial-analysts-journal/2010/the-shrinking-merger-arbitrage-spread-reasons-and-implications
4. Ricks, Lin (2024), "How Deals Die", Harvard Law School Forum: https://corpgov.law.harvard.edu/2024/10/15/how-deals-die/
5. Cusatis, Miles, Woolridge (1993), JFE 33(3): https://www.sciencedirect.com/science/article/abs/pii/0304405X9390009Z
6. McConnell, Ovtchinnikov (2004), JIM 2(3): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=569283
7. Veld, Veld-Merkoulova (2009), IJMR: https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-2370.2008.00243.x
8. Shleifer (1986), JF 41(3): https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1986.tb04518.x
9. Greenwood, Sammon (2025), JF: https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.13410 ; NBER w30748: https://www.nber.org/system/files/working_papers/w30748/w30748.pdf
10. Ritter (1991), JF 46(1): https://site.warrington.ufl.edu/ritter/files/The-Long-Run-Performance-of-Initial-Public-Offerings-1991-03.pdf
11. Ritter, IPO Data (página actualizada el 9-mar-2026): https://site.warrington.ufl.edu/ritter/ipo-data/ ; "Initial Public Offerings: Updated Statistics" (14-sep-2026; Tabla 1 del 13-jul-2026): https://site.warrington.ufl.edu/ritter/files/IPO-Statistics.pdf
12. Ritter, "Initial Public Offerings: Updated Long-run Statistics" (27-ago-2026): https://site.warrington.ufl.edu/ritter/files/IPOs-long-run-returns-on-IPOs.pdf
13. Loughran, Ritter (1995), JF 50(1): https://onlinelibrary.wiley.com/doi/full/10.1111/j.1540-6261.1995.tb05166.x
14. Pontiff, Woodgate (2008) y Daniel, Titman (2006), citados en: https://www.sciencedirect.com/science/article/abs/pii/S0304405X09001007 ; https://www.semanticscholar.org/paper/Share-Issuance-and-Cross%E2%80%90sectional-Returns-Pontiff-Woodgate/a49487518f8adde358fc15f79aefc2329b2cc02e
15. Ikenberry, Lakonishok, Vermaelen (1995), JFE 39: https://www.sciencedirect.com/science/article/abs/pii/0304405X9500826Z ; NBER w4965: https://www.nber.org/papers/w4965
16. Peyer, Vermaelen (2009), RFS 22(4): https://academic.oup.com/rfs/article-abstract/22/4/1693/1567717
17. Fu, Huang (2016), Management Science 62(4): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1936187 ; reseña: https://www.tandfonline.com/doi/full/10.1080/23322039.2015.1119461
18. Lee, Park, Pearson (2020), JCF 62: https://ideas.repec.org/a/eee/corfin/v62y2020ics0929119919309368.html
19. Lakonishok, Lee (2001), RFS 14(1): https://academic.oup.com/rfs/article-abstract/14/1/79/1587398
20. Jeng, Metrick, Zeckhauser (2003), REStat 85(2): https://direct.mit.edu/rest/article/85/2/453/57400/Estimating-the-Returns-to-Insider-Trading-A
21. Cohen, Malloy, Pomorski (2012), JF 67(3): https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2012.01740.x ; NBER: https://www.nber.org/digest/apr11/decoding-inside-information
22. Oenschläger, Möllenhoff (2025), Finance Research Letters 72: https://ideas.repec.org/a/eee/finlet/v72y2025ics1544612324015435.html
23. Zhao (2026), "Insider Purchases Far Below the 52-Week High", arXiv: https://arxiv.org/abs/2602.06198
24. Antón, Cohen, Polk, "Best Ideas": https://personal.lse.ac.uk/polk/research/bestideas.pdf ; versión Cohen-Polk-Silli: https://eprints.lse.ac.uk/24471/1/Best%20ideas(published).pdf
25. Martin, Puthenpurackal (2005, rev. 2008), "Imitation is the Sincerest Form of Flattery: Warren Buffett and Berkshire Hathaway", SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=806246
26. Angelini, Iqbal, Jivraj (2019), "Systematic 13F Hedge Fund Alpha": http://wp.lancs.ac.uk/fofi2020/files/2020/04/FoFI-2020-090-Farouk-Jivraj.pdf
27. Rapach, Ringgenberg, Zhou (2016), JFE 121(1): https://www.sciencedirect.com/science/article/abs/pii/S0304405X16300320
28. Boehmer, Jones, Zhang (2008), JF 63(2): https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2008.01324.x
29. Hong, Li, Ni, Scheinkman, Yan (2015), NBER w21166: https://www.nber.org/papers/w21166
30. Brav, Jiang, Partnoy, Thomas (2008), JF 63: https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2008.01373.x
31. Becht, Franks, Grant, Wagner (2017), RFS 30(9): https://academic.oup.com/rfs/article/30/9/2933/3852480
32. Savor, Wilson (2016), JF 71(1): https://onlinelibrary.wiley.com/doi/10.1111/jofi.12361
33. Heitz, Narayanamoorthy, Zekhnini, "Filings of Material Information and the Disappearing Earnings Announcement Premium" (SSRN 2018): https://doi.org/10.2139/ssrn.3296537 ; PDF (403 al verificar): https://www.iimb.ac.in/ARC2020/Papers/The_Disappearing_Earnings_Announcement_Premium.pdf
34. Martineau (2022), Critical Finance Review 11(3-4), 613-646: https://doi.org/10.1561/104.00000122 (el enlace anterior a cfr.pub redirige hoy a un sitio ajeno; se eliminó)
35. UCLA Anderson Review, "Is Post-Earnings Announcement Drift a Thing? Again?" (Subrahmanyam; Dickerson-Julliard-Mueller; Hirshleifer-Peng-Wang): https://anderson-review.ucla.edu/is-post-earnings-announcement-drift-a-thing-again/
36. Kettell, McInnis, Zhao (2022), "Why Has PEAD Declined Over Time?": https://business.columbia.edu/sites/default/files-efs/imce-uploads/CEASA/Events%20Page/PEAD_Declined_over_time.pdf
37. Jegadeesh, Kim, Krische, Lee (2004), JF 59: https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2004.00657.x
38. Ziobrowski, Cheng, Boyd, Ziobrowski (2004), JFQA 39: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/A39406479940758D59E09FDCB8EE9BEC/S0022109000003161a.pdf/abnormal_returns_from_the_common_stock_investments_of_the_us_senate.pdf
39. Eggers, Hainmueller (2013), JOP 75(2): https://j-hai.github.io/assets/pdf/capitol.pdf ; https://www.journals.uchicago.edu/doi/abs/10.1017/s0022381613000194
40. Wei, Zhou (2025), NBER w34524: https://www.nber.org/papers/w34524
41. Klausner, Ohlrogge, Ruan (2022), Yale J. on Regulation 39: https://www.yalejreg.com/print/a-sober-look-at-spacs/ ; https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3720919
42. Klausner, Ohlrogge (2023), "Was the SPAC Crash Predictable?", Yale J. on Reg. Bulletin: https://www.yalejreg.com/bulletin/was-the-spac-crash-predictable/
43. Ritter, "SPACs" (Gahng, Ritter, Zhang; RFS 2023): https://site.warrington.ufl.edu/ritter/files/SPACs.pdf
44. Barber, Huang, Odean, Schwarz (2022), JF 77(6): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3715077 ; https://newsroom.haas.berkeley.edu/how-robinhoods-trading-app-spurs-investors-herding-instincts-prof-terrance-odean/
45. Bali, Hirshleifer, Peng, Tang, Wang, "Social Interactions and Lottery Stock Mania", NBER w29543 (dic-2021, rev. nov-2025): https://www.nber.org/papers/w29543
46. Jajal et al. (2026), "Global Merger-Arbitrage Forecasting with Language Models", ICML 2026: https://arxiv.org/abs/2607.09921
47. Kim (Sehwa), Kim (Seil), Rajgopal (2025), "Insider Trading After the 2022 Rule 10b5-1 Amendment", CLS Blue Sky: https://clsbluesky.law.columbia.edu/2025/07/31/insider-trading-after-the-2022-rule-10b5-1-amendment/ ; versión en revista (que sea JAE no se verificó): https://www.sciencedirect.com/science/article/abs/pii/S0165410126000765
48. Equibles (2025), "What Happens After an Insider Buys?" (proveedor, sin revisión por pares): https://equibles.com/research/what-happens-after-an-insider-buys-evidence-from-47-458-open-market-purchases
49. CNBC (5-sep-2025), AppLovin y Robinhood al S&P 500: https://www.cnbc.com/2025/09/05/applovin-robinhood-sp-500.html
50. Tesis CBS (2023), "Spin-off performance: An unrelenting anomaly": https://research-api.cbs.dk/ws/portalfiles/portal/98732383/1643122_Spin_off_performance_An_unrelenting_anomaly.pdf
51. SEC, Insider Transactions Data Sets: https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets ; SOX y Form 4: https://corpgov.law.harvard.edu/2009/10/30/sox-and-insider-trades/
52. SEC, enmiendas a la Regla 10b5-1 (comunicado 2022-222): https://www.sec.gov/newsroom/press-releases/2022-222 ; Skadden: https://www.skadden.com/insights/publications/2022/12/sec-amends-rules-for-rule-10b51-trading-plans-and-adds-new-disclosure-requirement
53. SEC, beneficial ownership (comunicado 2023-219): https://www.sec.gov/newsroom/press-releases/2023-219 ; Skadden: https://www.skadden.com/insights/publications/2024/02/reminders-amended-beneficial-ownership-rules-effective
54. CRS, "Taking Stock of the STOCK Act": https://www.congress.gov/crs-product/TE10119 ; https://www.congress.gov/crs_external_products/R/HTML/R47818.html
55. Morgan Lewis (dic-2025), Form SHO pospuesto a 2028: https://www.morganlewis.com/pubs/2025/12/short-sale-reporting-on-form-sho-compliance-date-further-extended-to-2028 ; SEC 34-104303: https://www.sec.gov/files/rules/exorders/2025/34-104303.pdf
56. StockAnalysis, NANC (24-sep-2026): https://stockanalysis.com/etf/nanc/ ; ETF.com, NANC vs KRUZ: https://www.etf.com/sections/etf-basics/nanc-vs-kruz-battle-congress-stock-trackers
57. Associated Capital Group, Form ARS FY2024 ("deal spreads are at the widest levels in years"; "aggressive regulator that challenged several headline deals"): https://www.sec.gov/Archives/edgar/data/1642122/000143774925013369/acars.pdf ; contexto general (no contienen las cifras ni los casos citados en el texto): InsideArbitrage (2025) https://www.insidearbitrage.com/2025/04/merger-arbitrage-risk-analysis/ ; Sculptor (2024) https://www.sculptor.com/news/2024-04-03-merger-arbitrage-revisited
58. LPL Research, "Merger Arbitrage 2025 Performance": https://www.lpl.com/research/blog/merger-arbitrage-rebound.html
59. FTI Consulting, "SPAC comeback: what's different this time" (138 SPACs y US$25.8 mil millones en 2025; US$8.7 mil millones en 2024): https://www.fticonsulting.com/insights/articles/spac-comeback-whats-different-time ; With Intelligence (no contiene las cifras trimestrales antes citadas): https://www.withintelligence.com/insights/a-cautious-rebound-spacs-enjoy-renewed-interest-in-2025/
60. Ritter, Tabla 15c "Post-merger Returns on deSPACs, 2012-2025" (29-jul-2026), en [12]
61. Reuters vía U.S. News (24-jul-2025), Opendoor y Kohl's: https://money.usnews.com/investing/news/articles/2025-07-24/opendoor-kohls-resume-rally-as-meme-stock-frenzy-continues
62. Warkulat, Pelster (2024), "Social media attention and retail investor behavior: Evidence from r/wallstreetbets", IRFA 96, 103721: https://doi.org/10.1016/j.irfa.2024.103721
63. Reichenbach, Walther (2023), "Financial recommendations on Reddit, stock returns and cumulative prospect theory", Digital Finance: https://pmc.ncbi.nlm.nih.gov/articles/PMC10111308/
64. Real Estate Market (5-feb-2025), Vinte deslista a Javer: https://realestatemarket.com.mx/noticias/mercado-inmobiliario/47318-vinte-deslista-a-javer-de-la-bmv-tras-adquirir-el-99-92-de-su-capital
65. Expansión (22-sep-2026), OPA de Pantera Holdings por Traxión: https://expansion.mx/mercados/2026/09/22/traxion-opa-acciones-desliste-bmv
66. Investing.com México, OPA de Traxión a 13.18: https://mx.investing.com/news/stock-market-news/opa-de-traxion-pantera-holdings-ofrece-1318-pesos-por-accion-no-sale-de-la-bmv-3772903 ; El Congresista: https://elcongresista.mx/finanzas/pantera-holdings-opera-opa-traxion
67. Boyar Research, "Spinoffs have dramatically underperformed": https://boyarresearch.substack.com/p/spinoffs-have-dramatically-underperformed
68. Mill Street Research (proveedor), "Do Analyst Estimate Revisions (Still) Help Forecast Relative Stock Returns?": https://www.millstreetresearch.com/do-analyst-estimate-revisions-still-help-forecast-relative-stock-returns/
69. GBM, comisiones: https://gbm.com/faqs/que-comisiones-cobran-al-invertir-en-gbm/ ; Awake Trader (2026): https://www.awaketrader.com/educacion/gbm-review-mexico
70. GBM, impuestos en el SIC: https://gbm.com/faqs/como-funcionan-los-impuestos-por-las-acciones-de-empresas-extranjeras-en-el-sic/ ; SOLTUM, art. 129 LISR: https://soltum.com.mx/tratamiento-fiscal-de-la-enajenacion-de-acciones-extranjeras-en-el-sic/
71. Datos de precios (cálculo propio de CAGR, beta, MDD y volatilidad USDMXN): Yahoo Finance chart API, series ajustadas de MNA, MRGR, ARB, CSD, IPO, PKW, GURU, GVIP, NANC, GOP, SPY, QQQ, BIL, MXN=X y TRAXIONA.MX al 24/25-sep-2026; en la verificación también HOOD, APP (sep-2025), OPEN (jul-2025), SSTK (2024-2026) y la búsqueda de sufijos .MX.
72. Universo SIC del proyecto (cota inferior de cobertura con datos de StockAnalysis): `arena/investigacion/02-universo-sic-bmv-agresivo.md`; costos y venta en corto de GBM: `arena/investigacion/01-gbm-operativa-y-costos.md`.
73. LISR, texto vigente, última reforma DOF 01-04-2024, art. 129 (copia congelada en `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/datos/legal/LISR.txt`; fuente: Cámara de Diputados).
74. 5 U.S.C. § 13105(l) (plazo de los PTR): https://www.law.cornell.edu/uscode/text/5/13105
