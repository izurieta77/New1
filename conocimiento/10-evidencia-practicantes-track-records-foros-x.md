# 10 — Evidencia real de practicantes: historiales, foros y X

> Nivel: aplicado · Actualizado: 2026-09-25 · Grado de evidencia global: **B**. La evidencia agregada (SPIVA, Morningstar, brechas de comportamiento, *day traders*) es **A**: grandes muestras, corregidas por supervivencia, replicadas en varios mercados y años. Los historiales individuales de "leyendas" son **C**, porque casi todos son de Nivel 2 o 3 (sección 2.5). Las señales de foros y redes son **B/C**: tienen poder predictivo documentado, pero pequeño, y decae cuando la plataforma se masifica.

Capítulos relacionados que aquí no se repiten: [02](02-maestria-portafolio-y-asset-pricing.md) (Carhart, Fama-French 2010, Berk-Green, SPIVA México), [06](06-doctorado-asset-pricing-empirico-y-anomalias.md) (decaimiento post-publicación, Sharpe deflactado), [09](09-frontera-ia-ml-llm-en-inversion.md) (competencias entre IAs con dinero real: Alpha Arena, StockBench, LiveTradeBench), [14](14-analisis-tecnico-que-sobrevive.md) (tendencia, CAN SLIM), [18](18-grandes-inversionistas-decodificados.md) (fichas de Buffett, Simons, Soros, Druckenmiller, Dalio y otros; jerarquía de auditabilidad) y [19](19-biblioteca-esencial.md) (Schwager). Parámetros: `config/parametros.json`.

**Nota de método.** La cuota de WebSearch de la sesión estaba agotada. Cada dato se confirmó por otra vía: el PDF o la página primaria, Crossref (metadatos y *abstracts*), Google Scholar vía WebFetch, Wikipedia con su referencia, o un cálculo propio con Yahoo y la biblioteca de Kenneth French. Cada *handle* de X se comprobó el 25-sep-2026 con la API pública de fxtwitter (nombre, seguidores, fecha de alta, sitio web) y el oEmbed de publish.x.com. Lo que no se pudo confirmar dice **(no verificado)**.

---

## 1. Objetivos de dominio

Quien se titula en este módulo debe saber hacer lo siguiente:

1. Leer un SPIVA o un Barómetro Activo/Pasivo de Morningstar y explicar por qué la tasa a 1 año engaña. También distinguir ponderación igual de ponderación por activos y cuantificar el sesgo de supervivencia.
2. Separar el rendimiento del fondo (TWR) del rendimiento del inversionista (MWR/TIR). Estimar la brecha de comportamiento y saber por qué DALBAR y Morningstar dan magnitudes tan distintas.
3. Clasificar cualquier historial en la jerarquía de auditabilidad (Nivel 1, 2 o 3) antes de creerle una sola cifra.
4. Calcular cuántos años de historial hacen falta para distinguir habilidad de suerte: t ≈ IR·√T.
5. Explicar con números los casos canónicos: la apuesta Buffett-Protégé, el decaimiento de Berkshire, Medallion, Magellan, Druckenmiller, Soros, Dalio, CTAs en 2022, AQR 2018-2020, ARK, *hedge funds* agregados y *private equity* (PME).
6. Evaluar gurús, concursos y *finfluencers* con tasas base (CXO: 47% de aciertos) y con el hallazgo de que en redes la audiencia no premia la habilidad.
7. Usar foros (Value Investors Club, Seeking Alpha, StockTwits, WallStreetBets) como fuente de ideas sin confundir señal agregada con consejo individual, y reconocer el decaimiento post-masificación.
8. Mantener una lista curada de X con sesgo conocido y nivel de historial de cada cuenta, y detectar impostores.
9. Convertir todo lo anterior en reglas coherentes con `config/parametros.json`.

---

## 2. Núcleo teórico

### 2.1 TWR, MWR y la brecha de comportamiento

- **TWR (rendimiento ponderado por tiempo):** $\prod_t (1+r_t) - 1$. Mide al gestor, porque no le afectan las entradas y salidas de dinero. Es la métrica de la competencia (`metrica_competencia`: TWR en MXN).
- **MWR (ponderado por dinero, una TIR):** es la tasa $k$ que resuelve $\sum_t \frac{CF_t}{(1+k)^t} + \frac{V_T}{(1+k)^T} = V_0$. Mide al inversionista.
- **Brecha** = TWR − MWR. Es positiva cuando el dinero entra después de subidas y sale después de caídas. Es un costo real, aunque el fondo no tenga la culpa.

*Intuición:* un fondo puede ganar 14% anual y su inversionista promedio perder dinero, si la mayor parte del capital entró en el pico. Así le pasó a ARKK (sección 5.6).

### 2.2 Sesgo de supervivencia y ponderación

Un universo que solo incluye fondos vivos sobreestima el rendimiento. SPIVA cuenta desde el inicio a los fondos liquidados o fusionados. Al cierre de 2024, **solo 36.4%** de los fondos domésticos de EUA sobrevivió 20 años (32.95% en *large-cap*) [2]. El promedio ponderado por activos pesa más a los fondos grandes y baratos. En *large-cap* a 20 años, el promedio ponderado por activos rindió 9.09% anual y el igual 8.48%, contra 10.35% del S&P 500 [2].

### 2.3 Suerte contra habilidad

- Estadístico de un historial: $t \approx IR \cdot \sqrt{T}$, con IR = alfa / error de seguimiento, anualizados.
- Años necesarios para t = 2: $T = (2/IR)^2$. **IR 0.3 → 44 años; IR 0.5 → 16 años; IR 1.0 → 4 años** (cálculo propio).
- **Máximo de N gestores sin habilidad:** $E[\max] \approx \sigma\sqrt{2\ln N}$. Con N = 1,000, el "mejor" queda ~3.7σ arriba solo por azar (cálculo propio).
- **Falsos positivos:** en el universo de 29,475 *finfluencers* [41], con α = 5% bilateral, unos **737 parecerían hábiles** aunque ninguno lo fuera (cálculo propio).

*Inferencia:* ningún historial de 1 a 3 años, por espectacular que sea, prueba habilidad, salvo que el IR sea enorme y además haya un mecanismo verificable. Por eso `validacion_estrategias.backtest_min_anios` = 10.

### 2.4 Rendimiento de mercados privados: PME

Kaplan-Schoar [24] definen la PME como el cociente entre distribuciones y aportaciones, ambas descontadas con el índice público:

$$PME = \frac{\sum_t D_t / I_t}{\sum_t C_t / I_t}$$

Con PME > 1, el fondo le ganó al índice con el mismo calendario de flujos. La TIR sola engaña, porque depende del *timing* de las llamadas de capital y de las líneas de crédito de suscripción.

### 2.5 Jerarquía de auditabilidad (se reutiliza la del cap. 18)

| Nivel | Qué es | Ejemplos | Qué NO prueba |
|---|---|---|---|
| **1** | Precio público diario, NAV de fondo registrado o 10-K auditado | Berkshire, Magellan, ARKK, QSPIX, PSH, ETFs | Que el método sea transferible; el MWR del inversionista |
| **2** | Fondo privado auditado para sus socios y reportado por prensa, cartas o libros | Medallion, Quantum, Duquesne, Pure Alpha | Comparabilidad: periodo, comisiones y vehículo los elige quien reporta |
| **3** | Autorreportado sin auditoría: concursos, cursos, redes, "mis operaciones" | Campeonatos, *finfluencers*, gurús | Casi nada: selección, sobrevivencia y posible fraude |

### 2.6 Sesgos de las bases de *hedge funds*

- **Suavizamiento:** los activos ilíquidos generan autocorrelación positiva en los rendimientos reportados. Eso reduce la volatilidad medida e infla el Sharpe (Getmansky-Lo-Makarov [28]).
- **Autoselección y fondos muertos:** los fondos que dejan de reportar a las bases comerciales tienen rendimientos trimestrales "dramáticamente más bajos" que los que siguen reportando. Con datos autorreportados, la habilidad estimada está sesgada al alza y el riesgo de cola a la baja (Aiken-Clifford-Ellis [27]).
- **Brecha de dinero:** los rendimientos ponderados por dinero de los inversionistas de *hedge funds* quedan **3 a 7 pp anuales** debajo de los de comprar y mantener (Dichev-Yu [25]).

### 2.7 Economía de las redes: atención ≠ habilidad

*Inferencia:* en una plataforma que maximiza la interacción, el seguidor marginal premia la certeza, el optimismo y la frecuencia, no el alfa. Por eso el número de seguidores puede tener correlación **negativa** con la habilidad, y así lo encuentran los datos [41]. Cuando una plataforma se masifica, cambian los incentivos de quienes publican y la señal agregada decae [34].

---

## 3. Literatura canónica

| Autores | Año | Título | Revista/Editorial | Hallazgo clave cuantificado | Enlace/DOI | Grado |
|---|---|---|---|---|---|---|
| Carhart | 1997 | On Persistence in Mutual Fund Performance | JF 52(1):57-82 | La persistencia se explica por factores y gastos, salvo en los peores fondos | 10.1111/j.1540-6261.1997.tb03808.x | A |
| Barber, Odean | 2000 | Trading Is Hazardous to Your Wealth | JF 55(2):773-806 | 66,465 hogares (1991-1996). Los que más operan ganan 11.4% anual; el mercado, 17.9%. Rotación media de 75% anual | 10.1111/0022-1082.00226 | A |
| Barber, Lee, Liu, Odean | 2009 | Just How Much Do Individual Investors Lose by Trading? | RFS (según el archivo del autor) | Taiwán: los individuos pierden 3.8 pp anuales en agregado, equivalente a 2.2% del PIB. Las instituciones ganan 1.5 pp | [46] | A |
| Barber, Lee, Liu, Odean | 2014 | The Cross-Section of Speculator Skill | J. Financial Markets 18:1-24 | *Day traders* de Taiwán (1992-2006): **menos de 1%** gana de forma predecible neto de comisiones. Los 500 mejores del año anterior ganan 61.3 pb/día brutos y 37.9 netos | 10.1016/j.finmar.2013.05.006 | A |
| Chague, De-Losso, Giovannetti | 2019 | Day Trading for a Living? | SSRN WP | Brasil (2013-2015): **97%** de quienes persistieron más de 300 días perdió dinero. Solo 1.1% ganó más que el salario mínimo | 10.2139/ssrn.3423101 | A/B (WP) |
| Kaplan, Schoar | 2005 | Private Equity Performance: Returns, Persistence, and Capital Flows | JF 60(4):1791-1823 | Rendimiento neto promedio ≈ S&P 500, con persistencia entre fondos del mismo GP | 10.1111/j.1540-6261.2005.00780.x | A |
| Harris, Jenkinson, Kaplan | 2014 | Private Equity Performance: What Do We Know? | JF 69(5):1851-1882 | ~1,400 fondos (Burgiss): *buyout* supera al S&P por 20-27% en la vida del fondo (>3% anual). VC gana en los 90 y pierde en los 2000 | 10.1111/jofi.12154 | A (periodo) / B (hoy) |
| Phalippou | 2020 | An Inconvenient Fact: Private Equity Returns and the Billionaire Factory | J. of Investing 30(1):11-39 | Desde 2006, MoM netos de 1.51-1.63 ≈ **11% anual, igual que los índices públicos** (confirmado con PME). *Carry* estimado de US$230 mil millones. Multimillonarios de PE: de 3 (2005) a 22 (2020) | 10.3905/joi.2020.1.153 | B |
| Getmansky, Lo, Makarov | 2004 | An Econometric Model of Serial Correlation and Illiquidity in Hedge Fund Returns | JFE 74(3):529-609 | Suavizamiento → Sharpe inflado (resumen propio; solo metadatos verificados) | 10.1016/j.jfineco.2004.04.001 | A |
| Dichev, Yu | 2011 | Higher Risk, Lower Returns: What Hedge Fund Investors Really Earn | JFE 100(2):248-263 | MWR **3-7 pp** anuales debajo del *buy-and-hold*. Alfa real del inversionista ≈ 0. A fines de 2008, apenas arriba de la tasa libre de riesgo | 10.1016/j.jfineco.2011.01.003 | A |
| Aiken, Clifford, Ellis | 2010 (WP) | Out of the Dark: Hedge Fund Reporting Biases and Commercial Databases | SSRN | La habilidad estimada con datos autorreportados está sesgada al alza. Los fondos que dejan de reportar rinden mucho menos | 10.2139/ssrn.1571981 | A/B |
| Bollen, Joenväärä, Kauppila | 2021 | Hedge Fund Performance: End of an Era? | FAJ 77(3):109-132 | Declive agregado. Desde 2008, asignar a *hedge funds* bajó la volatilidad pero **no mejoró el Sharpe** | 10.1080/0015198x.2021.1921564 | B |
| Chen, De, Hu, Hwang | 2014 | Wisdom of Crowds: The Value of Stock Opinions Transmitted Through Social Media | RFS 27(5):1367-1403 | En Seeking Alpha, las opiniones de artículos y comentarios predicen rendimientos futuros y sorpresas de utilidades | 10.1093/rfs/hhu001 | B |
| Bartov, Faurel, Mohanram | 2018 | Can Twitter Help Predict Firm-Level Earnings and Stock Returns? | Accounting Review 93(3):25-57 | 2009-2012: la opinión agregada de tuits previos al reporte predice utilidades y rendimientos del anuncio | 10.2308/accr-51865 | B |
| Renault | 2017 | Intraday Online Investor Sentiment and Return Patterns | JBF 84:25-40 | StockTwits: el cambio de sentimiento en la primera media hora predice el rendimiento de SPY en la última media hora. Lo mueven los novatos | 10.1016/j.jbankfin.2017.07.002 | B/C |
| Cookson, Niessner | 2020 | Why Don't We Agree? | JF 75(1):173-228 | El desacuerdo se reparte entre información distinta e interpretación distinta. El de información mueve más el volumen | 10.1111/jofi.12852 | B |
| Crawford, Gray, Kern | 2017 | Why Do Fund Managers Identify and Share Profitable Ideas? | JFQA 52(5):1903-1926 | Club privado de ideas (VIC; ver sección 5.10): BHAR ajustado a 1 año de **+13.3%** en compras y **−6.18%** en ventas (cifras del resumen de Scholar) | 10.1017/s0022109017000588 | B |
| Bollen, Mao, Zeng | 2011 | Twitter Mood Predicts the Stock Market | J. Comput. Sci. 2(1):1-8 | "87.6%" de acierto direccional del DJIA, dentro de muestra y con datos de 2008 | 10.1016/j.jocs.2010.12.007 | **D** |
| Schwager | 1989-2020 | *Market Wizards* (1989), *New* (1992), *Stock* (2001), *Unknown* (2020) | Libros | Entrevistas a sobrevivientes, sin grupo de control | [31] | C/D |
| Zuckerman | 2019 | *The Man Who Solved the Market* | Portfolio/Penguin | Medallion 1988-2018: **66.1% bruto y 39.1% neto** anual | [13] | C (Nivel 2) |

---

## 4. Lo más reciente, 2023-2026

Las cifras completas están en la sección 5. Aquí va la cronología.

- **2-feb-2024 y 21-jul-2026, Morningstar.** Estudios de destrucción de riqueza de los inversionistas en 10 años. En el de 2024, ARKK destruyó ~US$7.1 mil millones [8]. En el de 2026, SQQQ encabeza con ~US$12.5 mil millones, ARKK baja a ~US$5.0 mil millones y 7 de los 15 peores son inversos apalancados [9].
- **27-dic-2024 (versión AEA 2025), "Finfluencers".** El primer estudio que mide la habilidad de cada *finfluencer* con un modelo de mezcla: la mayoría no tiene habilidad o la tiene negativa, y la audiencia premia a los peores [41].
- **2023-2024, RFS y JFE.** WallStreetBets pierde su poder predictivo después de GameStop [34]. StockTwits funciona como cámara de eco [36]. La atención se mueve junta entre plataformas y el sentimiento no [37].
- **2025, JPM 52(3).** Value Investors Club conserva alfa en ~3,200 recomendaciones [43].
- **2026, datos agregados.** Primera carta de Greg Abel (28-feb) [12]. Barómetros de Morningstar de cierre de 2025 (18-feb) y de mitad de 2026 (6-ago) [4][5]. DALBAR QAIB (16-abr) [10]. SPIVA EUA de cierre de 2025 [1]. *Mind the Gap* 2026 (6-ago), que por primera vez mide ETFs cripto, *buffer* y apalancados de una sola acción [6].
- **7-ago y 8-sep-2026, HFR.** HFRI FWC: +6.2% en 2026 a julio; −1.1% en julio (Tecnología −7.0%, el peor mes desde 2008) y +1.7% en agosto [19].
- **24/25-ago-2026.** El WSJ publicó un artículo de opinión de Druckenmiller ("Let the Bond Market Speak") y al día siguiente informó que lo había redactado con ayuda de IA. Él dijo estar "orgulloso" de usarla (Nivel 3, vía Wikipedia) [15]. *Inferencia:* la autoría de un texto ya no garantiza que el pensamiento sea de quien lo firma.
- **25-sep-2026, X.** La cuenta de Cliff Asness (@CliffordAsness) devuelve "User not found". Existe @cliffasness con el nombre "Cliff Asness", pero tiene 0 tuits desde 2014 y **no es él** [49]. Su canal verificable es el blog de AQR.
- **SPIVA EUA de mitad de 2026:** no localizado. El sitio de S&P bloqueó el acceso y solo se vieron los de Asia ex-Japón e India, del 21 al 23-sep-2026.

---

## 5. Evidencia real: qué funciona, qué no, magnitudes netas y decaimiento

### 5.1 Fondos activos contra índices: EUA, global y México

**SPIVA EUA, cierre 2025 [1]** (datos al 31-dic-2025):

| Categoría | % que perdió contra su índice en 2025 |
|---|---|
| *Large-cap* vs S&P 500 | **79%** (65% en 2024; 54% en el 1S-2025) |
| *Mid-cap* / *small-cap* | 55% / 41% |
| Internacional / global / emergentes / internacional *small* | 63% / 76% / 53% / 70% |
| Grado de inversión / *high yield* / deuda emergente | 82% / 76% / 31% |

El reporte da contexto. El S&P subió ~18% con 39 cierres récord. Solo **30% de sus acciones** le ganó al índice. El S&P 500 superó por 10 pp al MidCap 400 y por 12 pp al SmallCap 600. En promedio perdieron 70% de los fondos de bonos y 62% de los de acciones [1].

**SPIVA EUA, cierre 2024, horizontes largos [2]** (tabla 1a, PDF completo):

| Categoría | 1 año | 5 años | 10 años | 15 años | 20 años |
|---|---|---|---|---|---|
| Todos los domésticos vs S&P 1500 | 78.65% | 84.69% | 89.70% | 93.23% | **94.11%** |
| *Large-cap* vs S&P 500 | 65.24% | 76.26% | 84.34% | 89.50% | **91.99%** |
| *Small-cap* vs S&P 600 | 29.69% | 60.37% | 82.22% | 90.68% | 90.80% |

Ajustado por riesgo, 98.13% de los *large-cap* pierde a 15 años [2].

**Morningstar, Barómetro Activo/Pasivo** [4][5]. Compara contra el promedio de los fondos pasivos de la misma categoría, un rival más duro y más realista que el índice sin costos. En 2025, solo 38% de 3,140 fondos activos sobrevivió y le ganó a su par pasivo; a junio de 2026, poco más de 40%. A 10 años gana ~1 de cada 5. El quintil más barato tuvo 31% de éxito y el más caro 17%. Elegir un gestor activo al azar implica 60% de probabilidad de perder contra el pasivo. A mitad de 2026, *large growth* tuvo 5% de éxito a 10 años, con distribución de excesos sesgada a la baja [5].

**México [3]** (verificado en el cap. 02, no re-verificado aquí porque el PDF de S&P devolvió 403). En 2025 el S&P/BMV IRT subió 35.2%. El **75.6%** de los fondos activos de renta variable mexicana quedó por debajo en 1 año, y 69.8%, 77.3% y 75.6% en 3, 5 y 10 años.

**Persistencia.** La persistencia de ganadores es casi nula fuera de los peores fondos (Carhart [48]). Desaparece en 1994-2018 (Choi-Zhao, cap. 02). En *hedge funds* se debilitó con rendimientos decrecientes a escala (Bollen et al., WP 2023 [26]). El U.S. Persistence Scorecard más reciente **no se pudo verificar** (S&P bloqueado).

**Grado: A.** Se replica en EUA, global y México, en 1 a 20 años, neto de costos y corregido por supervivencia.

### 5.2 La brecha de comportamiento: el costo que pone el inversionista

| Fuente | Periodo | Fondo (TWR) | Inversionista (MWR) | Brecha |
|---|---|---|---|---|
| Morningstar *Mind the Gap* 2025 [7] | 10 años a dic-2024 | 8.2% | 7.0% | **1.2 pp/año** |
| Morningstar *Mind the Gap* 2026 [6] | 10 años a dic-2025 | 9.9% | 8.7% | **1.2 pp/año** (~12% del rendimiento) |
| — Solo fondos de acciones de EUA [6] | 10 años a dic-2025 | 13.3% | 12.8% | 0.5 pp |
| — ETFs cripto *spot* [6] | ene-2024 a jun-2026 | +8.5%/año | **−5.8%/año** | >14 pp |
| DALBAR QAIB 2026 [10] | solo 2025 | S&P 17.88% | 17.16% | 0.72 pp |
| DALBAR QAIB 2026 [10] | solo 2024 | — | — | 8.48 pp |

**Regularidades de Morningstar** [6][7]:

- La brecha es menor en fondos de asignación (*target-date*), que se usan con aportaciones automáticas.
- Crece con la volatilidad del fondo.
- Crece con el error de seguimiento: menos de 1 pp en el quintil de menor TE contra casi el doble en el de mayor TE.

**Crítica a DALBAR.** DALBAR compara el rendimiento del "inversionista promedio" contra el S&P 500, no contra los fondos que ese inversionista tenía. Su serie salta de 848 pb a 72 pb de un año al siguiente. *Inferencia:* una brecha que cambia 12 veces de tamaño en un año mide sobre todo el diseño de la comparación, no la conducta. Varios autores del medio han cuestionado su metodología; los nombres y textos específicos quedaron **(no verificado)**. **Para decidir se usa Morningstar (A/B), no DALBAR (C).**

**Complemento con cuentas individuales.**

- Los hogares que más operan quedan 6.5 pp anuales debajo del mercado [44].
- En Taiwán, los individuos pierden 3.8 pp anuales en agregado [46].
- Menos de 1% de los *day traders* es rentable de forma predecible [45].
- En Brasil, 97% de los *day traders* persistentes pierde [47].

**Grado: A**, en dirección y en magnitud aproximada (1-4 pp anuales).

### 5.3 Historiales individuales: qué es dato y qué es leyenda

| Caso | Dato verificado | Nivel | Lección |
|---|---|---|---|
| **Apuesta Buffett-Protégé** (19-dic-2007 a 2017) [11] | Fondo índice del S&P: **+125.8%, 8.5% anual**. Cinco fondos de fondos (más de 200 *hedge funds*): de +2.8% a +87.7%, **0.3% a 6.5% anual**, con comisiones fijas de ~2.5% anual. La beneficiaria recibió **US$2,222,279**. En cada uno de los 9 años posteriores a 2008, los fondos de fondos en conjunto quedaron debajo | 1 (auditorías entregadas a Buffett) | Costos de dos capas contra beta barata: gana la beta |
| **Berkshire** [12] | 1965-2025: **19.7% vs 10.5%** anual; acumulado de 6,099,294% vs 46,061%. En 2025: +10.9% vs +17.9%. **Cálculo propio con la tabla de la carta:** 1996-2025, 11.1% vs 10.4%; 2006-2025, 11.3% vs 11.0%; **2016-2025, 14.3% vs 14.8%** | 1 | El alfa decae con el tamaño. La década reciente queda ≈ índice. Abel es CEO desde el 1-ene-2026 y Buffett es presidente emérito desde el 18-sep-2026 (cap. 18) |
| **Medallion** [13] | 66.1% bruto y 39.1% neto anual (1988-2018, Zuckerman); 71.8% bruto (1994 a mediados de 2014). Cerrado a externos desde 1993 | 2 | Existe alfa extremo, pero no se puede comprar: el fondo para externos (RIEF) cayó ~20% en 2020 (cap. 18) |
| **Lynch / Magellan** [14] | 29.2% anual (1977-1990); activos de US$18 millones a US$14 mil millones | 1 | Rendimiento del fondo ≠ rendimiento del inversionista. El estudio de Fidelity sobre las pérdidas de los inversionistas de Magellan sigue **(no verificado)** |
| **Druckenmiller / Duquesne** [15] | "30% anual promedio sin ningún año perdedor"; cerró en 2010 | 2 | Concentración y salida rápida; no se puede replicar sin su proceso |
| **Soros / Quantum** (cap. 18) | ~20% anual en cuatro décadas; pérdidas grandes en 1987, 1994 y 1998 | 2 | Macro reflexivo, con pérdidas grandes incluidas |
| **Dalio / Bridgewater** [16] | Pure Alpha +33% en 2025 (Reuters); "4.5% anual desde 2005, debajo de los índices" (Wikipedia; fuente primaria no verificada). *All Weather*: RPAR −22.8% en 2022 (cap. 18) | 2-3 | La paridad de riesgo sufre cuando bonos y acciones caen juntos (2022) |

*Inferencia:* los historiales de Nivel 1 más largos (Berkshire, Magellan) muestran alfa real que decae con los activos. Los de Nivel 2 (Medallion, Duquesne) no se pueden invertir. Para el sistema, **ninguno sirve como señal copiable. Sirven como mecanismos** (cap. 18).

### 5.4 Seguimiento de tendencia (CTAs): 2022 y 2023-2026

| Año | SG Trend Index | BTOP50 | S&P 500 TR | 60/40 SPY/AGG (cálculo propio) |
|---|---|---|---|---|
| 2022 | **+27.3%** [18a] | +13.8% | −18.1% | −16.1% |
| 2023 | −4.16% [18b] | −1.70% | +26.3% | — |
| 2024 | +2.42% [18c] | +4.44% | +25.0% | — |
| 2025 | +2.39% [18d] | +2.81% | +17.9% | +13.5% |
| 2026 a ago | +11.07% [18e] | +11.13% | +13.14% | — |
| **CAGR desde 2000** | **5.60%**, DD máx. 20.61% | 4.40%, DD 15.94% | **8.27%**, DD 50.95% | — |

Los ETFs de futuros gestionados muestran lo mismo (cálculo propio con Yahoo, precios ajustados) [21]:

- **DBMF:** +21.6% (2022), −8.9% (2023), +7.2% (2024), +13.8% (2025), +17.8% (2026 al 24-sep).
- **KMLM:** +24.2%, −5.7%, −1.7%, −3.0% y +19.7% en los mismos periodos.

*Inferencia:* la tendencia es un **seguro de crisis prolongadas** con prima de años planos. Rinde menos que la renta variable en el largo plazo, pero cae 20% en vez de 50%. **Grado: B** (robusto en 100+ años, decaído después de 2012; cap. 06 y 14). En una temporada de 6 meses solo gana si hay crisis o tendencias fuertes.

### 5.5 AQR y el invierno del *value* (2018-2020)

- **QSPIX** (AQR Style Premia, Nivel 1, cálculo propio): **−41.4%** de ene-2018 a dic-2020. Después: +24.9% (2021), +30.8% (2022), +12.5% (2023), +21.5% (2024) y +14.8% (2025).
- **HML de Fama-French (EUA, largo-corto, bruto, sin costos)**, con la biblioteca de French a jul-2026 [20]: −57.8% de dic-2006 a sep-2020, el peor episodio desde 1926. Rebotó +68.5% hasta dic-2022. En jul-2026 seguía **29.6% debajo del pico de 2006**.

*Inferencia:* un factor con Sharpe histórico decente puede pasar 14 años bajo el agua. El gestor que sobrevivió (AQR) lo logró con diversificación entre factores y capital paciente. Un inversionista con horizonte de 6 meses no puede depender de eso. **Grado: B** (el *value* existe, está decaído y depende del régimen).

### 5.6 ARK Innovation: rendimiento del fondo contra dinero del inversionista

| Métrica (Nivel 1) | ARKK | SPY | QQQ |
|---|---|---|---|
| CAGR del 31-oct-2014 al 24-sep-2026 (cálculo propio) | **14.5%** | 13.8% | 19.1% |
| Máximo *drawdown* | **−80.9%** (12-feb-2021 a 28-dic-2022) | −33.7% | −35.1% |
| CAGR desde el cierre de 2020 | **−4.9%** | +14.9% | +16.9% |

Según Morningstar [9], ARKK subió +35.7% en 2019 y +152.5% en 2020. Captó ~US$14.1 mil millones en 2020-2021 y cayó **−67.0% en 2022**. Aun con un rendimiento positivo a 10 años, destruyó **~US$5.0 mil millones** de dinero de sus inversionistas, porque la mayoría entró después del pico. **Lección A:** el rendimiento publicado de un fondo "estrella" no es lo que ganó su inversionista, y los flujos récord son una señal de alerta, no de confirmación.

### 5.7 *Hedge funds* agregados contra 60/40

- **HFRI FWC 2025: +12.5%**, "el mejor año desde 2009" [19c]. Contra el S&P TR +17.9% y un 60/40 SPY/AGG +13.5% (cálculo propio). En 2026 a julio: HFRI +6.2% contra 60/40 +5.9%.
- **Costos:** comisión de administración promedio de 1.32% y de desempeño de 15.78% (1T-2026) [19b]. Capital de la industria: US$5.6 billones al 2T-2026, con entradas de US$115.8 mil millones en 2025 [19d].
- **Sesgos** (sección 2.6): el índice es autorreportado; los rendimientos de los inversionistas quedan 3-7 pp debajo [25]; desde 2008, los *hedge funds* no mejoran el Sharpe de un portafolio [26].

**Veredicto: C** como clase de activo para un particular. La apuesta Buffett-Protégé es el experimento natural más limpio [11].

### 5.8 *Private equity* contra mercados públicos

- **Phalippou [22]:** desde 2006, ~11% anual, igual que los índices públicos comparables (confirmado con PME). El *carry* suma US$230 mil millones; con todas las cosechas hasta 2015, US$370 mil millones.
- **Harris-Jenkinson-Kaplan [23]:** *buyout* > S&P por más de 3% anual, con datos hasta ~2010. VC pierde en los 2000.
- **Kaplan-Schoar [24]:** neto ≈ S&P 500.
- La literatura de 2025 (tesis y WPs) apunta a un rezago reciente contra el S&P; sin cifra verificada **(no verificado)**.

**Grado: B** para "PE ≈ público después de comisiones desde mediados de los 2000". *Inferencia:* en México, los CKDs y CERPIs no dan alfa por ser ilíquidos; la iliquidez es un costo que se cobra, no un premio que se gana.

### 5.9 Gurús y concursos

- **CXO Advisory, Guru Grades [29].** 6,582 pronósticos públicos del mercado de EUA hechos por 68 expertos (fin de 1998 a 2012). **Acierto agregado de 46.9%, promedio por gurú de 47.4%**. El mejor: Nassar, 68.2% en 44 pronósticos. Ken Fisher: 66.4% en 120. Jim Cramer: 46.8% en 62. El peor: Prechter, 20.8% en 24. CXO advierte que los pronósticos consecutivos no son independientes, así que la muestra efectiva es menor. **Grado A** para "el gurú promedio no le gana a una moneda".
- **Concursos.** Larry Williams convirtió US$10,000 en US$1,137,600 (**11,376%**) en la *World Cup Championship of Futures Trading* de 1987, un concurso de 12 meses. Su hija lo ganó 10 años después. Tuvo problemas por no presentar a tiempo sus declaraciones de impuestos de 1999-2001 [30].
- **U.S. Investing Championship.** Las cifras de Minervini siguen **(no verificado)**. Su propio sitio usa una cita elogiosa del fundador del concurso (Norm Zadeh), lo cual es un conflicto de interés [30].

*Inferencia:* en un concurso de 12 meses con cuentas pequeñas y apalancamiento, el ganador es por construcción un extremo de la distribución. Es selección sin denominador (Nivel 3, **D** como evidencia de método).

- **Lecciones de *Market Wizards*** (síntesis del panel; C/D por falta de grupo de control) [31]:
  1. Controlar el riesgo antes que buscar rendimiento.
  2. Cortar pérdidas y dejar correr ganancias.
  3. Riesgo por operación pequeño y fijo.
  4. Un método que calce con la personalidad y el horizonte.
  5. Reducir tamaño en rachas perdedoras.
  6. Paciencia para esperar la operación de alta convicción.

  Coinciden con reglas que el sistema ya tiene (`riesgo_por_operacion`, `rachas`). No agregan evidencia nueva.

### 5.10 Foros y comunidades: dónde hay señal

| Comunidad | Evidencia | Magnitud | Decaimiento | Grado |
|---|---|---|---|---|
| **Value Investors Club** (ideas largas, curadas, por invitación) | Crawford-Gray-Kern [42]; Curac-Lobe-Walkshäusl [43] | BHAR a 1 año de +13.3% en compras y −6.18% en ventas. ~3,200 recomendaciones con alfa significativo | Sin evidencia de decaimiento en la muestra de 2025 (no verificado a detalle) | **B** |
| **Seeking Alpha** | Chen et al. [32]; Farrell et al. [33] | El texto predice rendimientos y sorpresas. El flujo de órdenes minoristas se vuelve más informativo el día de publicación (el doble, según el WP) | — | **B** |
| **StockTwits / X** (sentimiento agregado) | Renault [38]; Bartov et al. [39]; Cookson et al. [35][36][37] | Predicción intradía o de 1 día. Atención alta → caídas. Los alcistas siguen 5 veces más a otros alcistas (~400,000 usuarios) | Intradía: los costos de GBM (0.58% por vuelta) se comen el efecto | **C** para GBM |
| **WallStreetBets** | Bradley et al. [34] | Predictivo antes de GME | **Se elimina después de GME** | **D** hoy |
| ***Finfluencers*** individuales | Kakhbod et al. [41] | 72 M de tuits de más de 29,000 usuarios: 28% hábiles (hasta +2.6% mensual), 17% sin habilidad y 55% con habilidad negativa (−2.3% mensual). Menos seguidores cuanto más hábil; los hábiles son contrarios | — | **D** (seguir al popular) / **B** (señal contraria, sin validar) |
| **Bogleheads** | Sin estudio académico propio localizado. Su doctrina (índices baratos, pocas decisiones) coincide con SPIVA y *Mind the Gap* | Hereda la evidencia A de 5.1 y 5.2 | — | **A** como doctrina / n.a. como fuente de señales |
| **Twitter "mood"** | Bollen-Mao-Zeng [40] | 87.6% dentro de muestra | Sin historial fuera de muestra verificable | **D** |

Nota: en VIC la organización se identifica por la búsqueda en Scholar; el resumen de Crossref la describe como "organización donde gestores comparten ideas en privado".

*Inferencia:* la señal vive en los textos **largos, curados y con reputación en juego** (VIC, artículos de Seeking Alpha). Se diluye en mensajes cortos con incentivos de interacción. Toda ventaja documentada de redes es de horizonte corto (intradía a días), justo el horizonte que los costos de GBM hacen inviable.

### 5.11 X (Twitter): lista curada y verificada al 25-sep-2026

Verificación con fxtwitter y oEmbed [49]: el nombre, la biografía y el sitio de cada *handle* coinciden con la persona. Los seguidores son aproximados. **Historial:** N1 = vehículo con NAV público (Nivel 1); N2 = fondo privado reportado; Op = opinión sin historial verificable.

| Cuenta | Quién | Por qué seguirla | Sesgo conocido | Historial |
|---|---|---|---|---|
| @AswathDamodaran | A. Damodaran, NYU (514 mil) | Datos de valuación (ERP, betas, múltiplos) y razonamiento público | Narrativa + números; sus operaciones personales son autorreportadas | Op |
| @camharvey | C. Harvey, Duke (13 mil; 309 tuits) | Pruebas múltiples, sobreajuste de *backtests* | Poca actividad | Op (académico) |
| @JohnHCochrane | J. Cochrane, Hoover (63 mil) | *Asset pricing*, macro-fiscal | Opiniones de política | Op (académico) |
| @mjmauboussin | M. Mauboussin, Counterpoint Global (161 mil) | Habilidad contra suerte, tasas base | Trabaja en un gestor activo | Op |
| @larryswedroe | L. Swedroe (20 mil) | Resúmenes semanales de papers | Defensor de factores; sin sello de verificación | Op |
| @choffstein | C. Hoffstein, Newfound (86 mil) | Tendencia, *rebalance timing luck*, construcción | Vende *Return Stacked ETFs* | N1 (ETFs) |
| @alphaarchitect | Wes Gray, PhD (49 mil) | Investigación de factores; coautor del paper de VIC [42] | Vende ETFs de factores | N1 (ETFs) |
| @MebFaber | M. Faber, Cambria (144 mil) | Tendencia, *shareholder yield*, *value* global | Vende sus ETFs | N1 (ETFs) |
| @BillAckman | B. Ackman, Pershing Square (3.0 M) | Activismo con NAV público (PSH) | Habla de sus posiciones; política | N1 (PSH) |
| @biancoresearch | J. Bianco (780 mil) | Tasas y datos macro | Sesgo inflacionario; su índice lo replica el ETF WTBN | N1 (desde el lanzamiento) |
| @verdadcap | D. Rasmussen, Verdad (48 mil) | *Value* apalancado *small*, crítica al PE | *Value* | N2/N3 |
| @jposhaughnessy | J. O'Shaughnessy (193 mil) | *What Works on Wall Street* | Hoy centrado en IA y *venture* | Op hoy |
| @profplum99 | M. Green, Tier1 (244 mil) | Crítica a los flujos pasivos | Tesis contraria y disputada (C) | Op |
| @KrisAbdelmessih | Kris, Moontower (52 mil) | Volatilidad y opciones | Visión centrada en opciones | Op |
| @nntaleb | N. Taleb (1.16 M) | Colas gordas y ruina | Combativo; defiende la cobertura de cola (Universa, N2-3) | Op |
| @RealJimChanos | J. Chanos (69 mil; cuenta de 2024) | Contabilidad forense en cortos | Vendedor en corto; cerró sus fondos a fines de 2023 [51] | N2 |
| @LizAnnSonders | L. A. Sonders, Schwab (818 mil) | Datos macro y de mercado | Institucional | Op |
| @TimmerFidelity | J. Timmer, Fidelity (221 mil) | Gráficas de ciclos largos | Institucional | Op |
| @charliebilello | C. Bilello, Creative Planning (866 mil) | Gráficas de rendimientos y *drawdowns* | Pasivo; *marketing* de su firma de asesoría (RIA) | Op |
| @EricBalchunas | E. Balchunas, Bloomberg (623 mil) | Flujos, comisiones y lanzamientos de ETFs | Pro-ETF | Op (datos) |
| @elerianm | M. El-Erian (1.1 M) | Bancos centrales y macro | Muchos cargos a la vez | Op |
| @LynAldenContact | L. Alden (1.1 M) | Macro fiscal | Defiende bitcoin (socia general de un fondo cripto) | Op |
| @jasonzweigwsj | J. Zweig, WSJ (235 mil) | Conducta, comisiones, fraudes | Escéptico de la gestión activa | Op |
| @awealthofcs | B. Carlson, RWM (380 mil) | Historia de mercado y tasas base | Comprar y mantener | Op |
| @matt_levine | M. Levine, Bloomberg (327 mil) | Estructura de mercado, fraudes, mecánica de tratos | Ninguno de *trading* | Op |
| @RobinWigg | R. Wigglesworth, FT Alphaville (83 mil) | Indexación y mercados | Periodístico | Op |
| @Banxico | Banco de México (912 mil; cuenta gubernamental) | Decisiones y datos oficiales | — | Oficial |
| @G_Casillas | G. Casillas, economista en jefe para Latinoamérica de Barclays; comité de fechado de ciclos de México (12 mil) | Macro de México | *Sell-side* | Op (se puede medir contra las encuestas) |
| @macariomx | M. Schettino (339 mil) | Economía y política de México | Opinión política | Op |
| @E_Q_ | E. Quintana, El Financiero (204 mil) | Coyuntura de México | Periodístico | Op |
| @esquivelgerardo | G. Esquivel, Colmex y FE-UNAM (180 mil) | Macro y distribución en México | Perfil político | Op |
| @juanrallo | J. R. Rallo, España (494 mil) | Economía en español | Escuela austriaca y liberal | Op |

**Impostores y homónimos detectados el 25-sep-2026** [49]:

- @cliffasness: "Cliff Asness", 0 tuits.
- @damodaran: 0 tuits.
- @jasonzweig: persona distinta.
- @BMV_MX: "carlos flores", 1 seguidor. No es la Bolsa Mexicana.
- @RobArnott: persona distinta.
- @GABRIELCASILLAS: 0 tuits.
- @alejandrowerner: "craftsman jeweler".
- @CNBV_mx: 0 tuits y sin verificar.

*Inferencia:* en 2026, uno de cada tres nombres famosos que se buscaron tenía un homónimo o impostor al alcance de un error de dedo.

---

## 6. Traducción operable

**Contexto de parámetros.** Fase actual: 0. El sistema no propone operaciones reales al dueño, así que estas reglas se aplican primero al portafolio de papel. Arena: capital de 20,000 MXN; 0.58% por vuelta más *spread*; máximo 8 operaciones al mes y rotación ≤1.5x del capital.

**R1. El índice es el rival por defecto.** Toda estrategia del satélite (patrimonio) y toda operación de la arena se mide contra comprar y mantener su ETF equivalente, **neto de 0.58% por vuelta**. Si después de `paper_trading_min_operaciones` (30) y `paper_trading_min_meses` (3) no le gana al ETF equivalente, se descarta. Evidencia: 79-94% de los activos pierde (sección 5.1). Para el núcleo (≥70% del patrimonio), la opción por defecto es el ETF más barato de su categoría: el quintil de menor costo tiene casi el doble de éxito que el más caro (31% vs 17%) [4].

**R2. Reportar TWR y MWR cada mes.** El TWR califica al sistema en la competencia. El MWR califica las decisiones de aportación del dueño. Si MWR − TWR < −1.2 pp anualizados (brecha promedio de Morningstar), se revisa el *timing* de aportaciones y retiros. En `competencia/rivales.csv` se registran `aportaciones_netas_mxn` para neutralizar los flujos.

**R3. Un historial solo cuenta si es de Nivel 1 y suficientemente largo.**

- Nivel 1 con ≥10 años (`backtest_min_anios`) puede inspirar una hipótesis de factor.
- Nivel 2 solo sirve como mecanismo.
- Nivel 3 (concursos, *finfluencers*, capturas de pantalla) pesa **cero**.
- Umbral: t = IR·√T ≥ 2. Con IR 0.5 se necesitan 16 años.

**R4. Los pronósticos de terceros entran al registro, no al portafolio.** Un gurú o cuenta de X que dé llamadas de mercado se registra en `pronosticos` con fecha y horizonte. Pesa cero hasta acumular ≥50 llamadas (`min_pronosticos_para_evaluar`) con Brier ≤0.20 (`brier_objetivo`). Tasa base de referencia: 47% de aciertos (CXO) [29].

**R5. Los seguidores no son señal y lo viral es una alerta.** Se prohíbe ponderar una idea por la popularidad de quien la publica: la habilidad se relaciona negativamente con los seguidores [41] y la atención alta predice caídas [37].

- **Recomendación:** no abrir un largo en un *ticker* durante los 5 días hábiles siguientes a que se vuelva tendencia en X o StockTwits, salvo que la tesis esté registrada antes de la viralidad. *Inferencia*, sin *backtest*.
- La versión contraria ("apostar contra lo viral") se manda al laboratorio. Solo entra si pasa DSR ≥0.95 y PBO ≤0.25 con 10 años de datos y costos de GBM.

**R6. Apalancados e inversos.** Los inversos apalancados son la categoría que más riqueza destruye (SQQQ: −US$12.5 mil millones) [9]. La volatilidad agranda la brecha del inversionista [6].

- Se mantienen `filtro_apalancados` (subyacente sobre su MM200 y VIX < 25) y `etf_apalancado_max` = 0.5 en la arena.
- **Recomendación adicional:** ningún inverso apalancado como posición direccional. Como cobertura, máximo 5 días hábiles y dentro de `riesgo_por_operacion` (arena 0.03; patrimonio 0.01, o 0.005 en fase de prueba). *Inferencia.*

**R7. Evitar temas con flujos récord.** Si la tesis depende de un tema o fondo con +100% en 12 meses y entradas récord (patrón ARKK 2020-2021), el tamaño se limita a **la mitad** del máximo que permite `riesgo_por_operacion`. *Inferencia*, basada en el caso ARKK (−67% en 2022; −80.9% de pico a valle).

**R8. Tendencia como seguro, no como motor.** En el patrimonio, un sleeve de futuros gestionados es un candidato de diversificación del núcleo: +27% en 2022 cuando el 60/40 cayó −16%, pero con un CAGR de 5.6% contra 8.3% del S&P. Su disponibilidad en el SIC está **(no verificado)**. En la arena (temporada de 6 meses) no se usa como fuente principal de rendimiento. La tendencia se aprovecha con el filtro MM200 ya existente.

**R9. Nada de 2/20 ni de iliquidez "premium".** Se descartan *hedge funds*, fondos de fondos, CKDs y CERPIs que se vendan por alfa. Evidencia: Buffett-Protégé; HFRI ≈ 60/40 en 2025-2026; MWR 3-7 pp menor; PE ≈ índice público (PME ≈ 1).

**R10. Foros como embudo de ideas, con jerarquía.** Orden de prioridad: VIC y artículos largos de Seeking Alpha > documentos regulatorios y cartas > X y StockTwits. Toda idea externa pasa por `ficha-empresa` y `comite-de-inversion`. Si la plataforma se masifica o cambia su composición, la señal se da por decaída hasta demostrar lo contrario (lección WSB post-GME) [34].

**R11. Protocolo anti-impostor para X.** Antes de seguir o citar una cuenta:

1. Verificar con fxtwitter o oEmbed el nombre, la fecha de alta, los seguidores y el sitio web.
2. Confirmar que el sitio web enlaza de regreso a la cuenta, o que la biografía nombra una institución verificable.
3. Registrar la fecha de verificación.
4. Excluir cuentas con <1,000 seguidores o sin sitio, salvo académicos confirmados por su página institucional.
5. Re-verificar cada 6 meses (la cuenta de Asness desapareció).

**R12. Lo que el sistema publica debe ser auditable (Nivel 1 propio).** Cada operación y pronóstico se registra *ex ante*, con fecha, en la bitácora. Los rendimientos se reportan con los estados de cuenta de GBM. Así el sistema cumple la regla que exige a los demás. *Inferencia:* es la única forma de que el dueño distinga habilidad de suerte al comparar contra otras IAs.

**Checklist para evaluar cualquier historial (10 preguntas):**

1. ¿Nivel 1, 2 o 3?
2. ¿Periodo completo o elegido por quien reporta?
3. ¿Bruto o neto de comisiones?
4. ¿TWR o MWR?
5. ¿Contra qué *benchmark*, en qué moneda?
6. ¿Incluye los fondos o cuentas que murieron?
7. ¿Cuántos años y qué IR, es decir, qué t?
8. ¿Cuántos "competidores" hubo? (Máximo de N.)
9. ¿El mecanismo es verificable y sigue vigente (capacidad, tamaño)?
10. ¿El autor gana por la atención (curso, fondo, *engagement*)?

---

## 7. Trampas y errores comunes

1. **Citar la tasa de 1 año de SPIVA como tendencia.** 2025 (79%) y 2024 (65%) dependen del régimen: concentración en megacaps y *small caps* rezagadas. La señal robusta está en 10-20 años (84-94%).
2. **Comparar un fondo contra el índice sin costos cuando la alternativa real es otro fondo.** Por eso el Barómetro usa pares pasivos.
3. **Confundir el rendimiento del fondo con el del inversionista.** ARKK tiene un CAGR de 14.5% desde su inicio y aun así destruyó US$5 mil millones de sus inversionistas.
4. **Usar DALBAR como cifra exacta.** Su brecha varía de 72 a 848 pb entre años consecutivos.
5. **Creerle al "Medallion accesible".** El vehículo para externos se comportó distinto.
6. **Extrapolar Berkshire 1965-2025 (19.7%) al futuro.** La última década quedó en 14.3% contra 14.8% del índice.
7. **Tratar la tendencia como máquina de rendimiento.** Después de 2022 vinieron −4.2%, +2.4% y +2.4%.
8. **Concluir que el *value* "murió" en 2020 o que "revivió" en 2022.** HML sigue 29.6% debajo de su pico de 2006.
9. **Seguir al *finfluencer* con más seguidores.** Los datos muestran lo contrario de lo que sugiere la intuición.
10. **Confiar en un estudio de redes dentro de muestra** (87.6% de Bollen-Mao-Zeng) o en uno anterior a la masificación (WSB antes de GME).
11. **Tomar un concurso de 12 meses como prueba de método.** 11,376% en un año es un extremo de la distribución, no una tasa.
12. **Seguir un *handle* sin verificarlo.** @cliffasness, @damodaran y @BMV_MX no son quienes parecen.
13. **Tomar el PE por su TIR.** La TIR depende del *timing* y de las líneas de crédito; hay que pedir la PME.
14. **Atribuir una opinión a su firmante sin más.** El texto de Druckenmiller en el WSJ se redactó con IA [15].

---

## 8. Examen de titulación

1. **¿Qué porcentaje de fondos *large-cap* activos perdió contra el S&P 500 en 2025 y a 20 años (cierre 2024)?** 79% en 2025 [1]; 91.99% a 20 años [2].
2. **¿Por qué el Barómetro de Morningstar es un rival más exigente que SPIVA?** Compara contra el promedio de fondos pasivos reales, con costos, de la misma categoría, y exige sobrevivir. A 10 años gana ~1 de cada 5 [4].
3. **Da la brecha de *Mind the Gap* 2026 y un caso donde fue extrema.** 1.2 pp anuales (8.7% contra 9.9%) en 10 años a 2025. En ETFs cripto, el inversionista perdió 5.8% anual mientras el ETF ganó 8.5% [6].
4. **¿Cómo terminó la apuesta Buffett-Protégé?** Índice +125.8% (8.5% anual) contra fondos de fondos de +2.8% a +87.7% (0.3%-6.5% anual). Girls Inc. recibió US$2,222,279 [11].
5. **¿Cuántos años de historial se necesitan para t = 2 con IR = 0.5?** (2/0.5)² = 16 años.
6. **¿Qué demuestra la tabla de Berkshire 2016-2025?** Un alfa que decae con el tamaño: 14.3% contra 14.8% del S&P (cálculo propio con la carta) [12].
7. **Cifras de Medallion y su nivel de auditabilidad.** 66.1% bruto y 39.1% neto (1988-2018), según Zuckerman. Nivel 2: auditado para sus socios, no invertible [13].
8. **¿Qué hizo el SG Trend Index en 2022 y cuál es su CAGR desde 2000?** +27.3% en 2022; 5.60% anual con DD máximo de 20.61%, contra 8.27% y 50.95% del S&P TR [18].
9. **¿Cuánto cayó QSPIX en 2018-2020 y dónde está HML frente a su pico?** −41.4%. HML seguía 29.6% debajo del pico de dic-2006 en jul-2026 [20][21].
10. **¿Qué muestran Dichev-Yu sobre los *hedge funds*?** El MWR de los inversionistas queda 3-7 pp anuales debajo del *buy-and-hold*, con alfa real ≈ 0 [25].
11. **Define la PME y resume a Phalippou 2020.** PME = distribuciones sobre aportaciones, ambas descontadas con el índice; >1 le gana al índice. Desde 2006, PE ≈ 11% anual ≈ índices públicos, con US$230 mil millones de *carry* [22][24].
12. **¿Qué acierto tuvieron los gurús de CXO?** 46.9% agregado y 47.4% promedio en 6,582 pronósticos de 68 expertos [29].
13. **Da las proporciones de *Finfluencers* y su relación con los seguidores.** 28% hábiles (hasta +2.6% mensual), 17% sin habilidad y 55% con habilidad negativa (−2.3% mensual). Los hábiles tienen menos seguidores [41].
14. **¿Qué pasó con la señal de WallStreetBets después de GameStop?** Su poder predictivo desapareció y aumentaron los posts de presión de precio [34].
15. **¿Cómo verificas que @X es quien dice ser?** fxtwitter u oEmbed (nombre, alta, seguidores, sitio), más un enlace recíproco desde el sitio institucional, con fecha de verificación. Ejemplo: @cliffasness tiene 0 tuits y no es Asness [49].

---

## 9. Fuentes

1. SPIVA U.S. Scorecard Year-End 2025, S&P DJI (texto completo reproducido por Markets Group): https://www.marketsgroup.org/strategic-insights/spiva-u-s-scorecard · original: https://www.spglobal.com/spdji/en/spiva/article/spiva-us/
2. SPIVA U.S. Scorecard Year-End 2024, PDF (tablas 1a, 1b, 3, 4 y supervivencia): https://requisitecm.com/pdf/SPIVA-US-Scorecard-Year-End-2024.pdf
3. SPIVA Latin America Year-End 2025 (cifras de México vía el cap. 02; el PDF devolvió 403 en esta sesión): https://www.spglobal.com/spdji/en/documents/spiva/spiva-latin-america-year-end-2025.pdf
4. Armour, B. (18-feb-2026). "Better Conditions Did Not Yield Better Results for Active Managers in 2025", Morningstar: https://www.morningstar.com/funds/better-conditions-did-not-yield-better-results-active-managers-2025
5. Morningstar (6-ago-2026). "Active Fund Manager Success Rates Ticked Up in 2026, but Passive Funds Still Hold the Advantage": https://www.morningstar.com/funds/active-fund-manager-success-rates-ticked-up-2026-passive-funds-still-hold-advantage
6. Ptak, J. (6-ago-2026). "The Winning Formula for Fund Investors, and Why Others Left Money on the Table" (*Mind the Gap* 2026): https://www.morningstar.com/funds/winning-formula-fund-investors-why-others-left-money-table
7. Ptak, J. (13-ago-2025). "The More Investors Traded, the Less Their Average Dollar Made" (*Mind the Gap* 2025): https://www.morningstar.com/financial-advisors/volatility-bedevils-fund-investors · pódcast del 7-nov-2025: https://www.morningstar.com/podcasts/investing-insights/investors-still-need-mind-gap-their-funds-returns
8. Arnott, A. (2-feb-2024). "15 Funds That Have Destroyed the Most Wealth Over the Past Decade", Morningstar: https://www.morningstar.com/funds/15-funds-that-have-destroyed-most-wealth-over-past-decade
9. Arnott, A., Ptak, J. (21-jul-2026). "These 15 Funds Cost Investors Billions Over the Past Decade", Morningstar: https://www.morningstar.com/funds/these-15-funds-cost-investors-billions-over-past-decade
10. DALBAR (16-abr-2026). "DALBAR's 2026 QAIB Report Shows Narrower Investor Gap…": https://www.dalbar.com/press-release/dalbars-2026-qaib-report-shows-narrower-investor-gap-amid-a-complex-and-volatile-market-year/
11. Berkshire Hathaway, carta anual 2017 ("The Bet"): https://www.berkshirehathaway.com/letters/2017ltr.pdf
12. Berkshire Hathaway, carta anual 2025 (firmada por G. Abel): https://www.berkshirehathaway.com/letters/2025ltr.pdf
13. Wikipedia, Jim Simons (cita a Zuckerman 2019): https://en.wikipedia.org/wiki/Jim_Simons · Renaissance Technologies: https://en.wikipedia.org/wiki/Renaissance_Technologies
14. Wikipedia, Peter Lynch: https://en.wikipedia.org/wiki/Peter_Lynch
15. Wikipedia, Stanley Druckenmiller (Duquesne; controversia del WSJ del 24/25-ago-2026): https://en.wikipedia.org/wiki/Stanley_Druckenmiller
16. Wikipedia, Bridgewater Associates (Pure Alpha, *All Weather*, Reuters 2025): https://en.wikipedia.org/wiki/Bridgewater_Associates
17. Cap. 18 de este repositorio (Soros, Dalio 2020, RPAR, ALLW, Medallion RIEF, transición en Berkshire): 18-grandes-inversionistas-decodificados.md
18. Top Traders Unplugged, *Trend Following Performance Report*: (a) dic-2022 https://www.toptradersunplugged.com/trend-following-performance-report-december-2022/ · (b) dic-2023 https://www.toptradersunplugged.com/trend-following-performance-report-december-2023/ · (c) dic-2024 https://www.toptradersunplugged.com/trend-following-performance-report-december-2024/ · (d) dic-2025 https://www.toptradersunplugged.com/trend-following-performance-report-december-2025/ · (e) ago-2026 https://www.toptradersunplugged.com/trend-following-performance-report-august-2026/
19. HFR: (a) *HFRI Flash* de julio 2026 (7-ago-2026): https://hfr-wp-s3.s3.amazonaws.com/wp-content/uploads/2026/08/10083350/2026.07_HFRI-Flash.pdf · (b) *Market Microstructure* 2026 (comisiones): https://www.hfr.com/media/market-commentary/hedge-fund-launches-liquidations-rise-to-begin-volatile-2026/ · (c) Boletín ene-feb 2026 (HFRI FWC 2025 +12.5%): https://hfr-wp-s3.s3.amazonaws.com/wp-content/uploads/2026/02/11135532/HFR-Newsletter-JanFeb2026-rev.pdf · (d) activos 2T-2026: https://www.hfr.com/media/market-commentary/hedge-fund-industry-asset-growth-shatters-records/ · agosto 2026: https://www.hfr.com/media/market-commentary/macro-hedge-funds-surge-in-august-as-interest-rates-rise-iran-conflict-escalates/
20. Kenneth R. French Data Library, *F-F Research Data Factors* (mensual, a jul-2026; cálculo propio de HML): https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
21. Yahoo Finance, API chart v8, vía `herramientas/datos_historicos.py` (ARKK, SPY, QQQ, AGG, DBMF, KMLM, QSPIX, ^SP500TR; cálculos del 25-sep-2026): https://query1.finance.yahoo.com/v8/finance/chart/ARKK
22. Phalippou, L. (2020). "An Inconvenient Fact: Private Equity Returns and the Billionaire Factory". *Journal of Investing* 30(1):11-39. https://doi.org/10.3905/joi.2020.1.153 · resumen: https://doi.org/10.2139/ssrn.3623820
23. Harris, R., Jenkinson, T., Kaplan, S. (2014). "Private Equity Performance: What Do We Know?" *JF* 69(5):1851-1882. https://doi.org/10.1111/jofi.12154
24. Kaplan, S., Schoar, A. (2005). "Private Equity Performance: Returns, Persistence, and Capital Flows". *JF* 60(4):1791-1823. https://doi.org/10.1111/j.1540-6261.2005.00780.x
25. Dichev, I., Yu, G. (2011). "Higher Risk, Lower Returns: What Hedge Fund Investors Really Earn". *JFE* 100(2):248-263. https://doi.org/10.1016/j.jfineco.2011.01.003
26. Bollen, N., Joenväärä, J., Kauppila, M. (2021). "Hedge Fund Performance: End of an Era?" *FAJ* 77(3):109-132. https://doi.org/10.1080/0015198x.2021.1921564 · WP 2023 sobre persistencia: https://doi.org/10.2139/ssrn.4596230
27. Aiken, A., Clifford, C., Ellis, J. "Out of the Dark: Hedge Fund Reporting Biases and Commercial Databases" (WP). https://doi.org/10.2139/ssrn.1571981
28. Getmansky, M., Lo, A., Makarov, I. (2004). *JFE* 74(3):529-609. https://doi.org/10.1016/j.jfineco.2004.04.001
29. CXO Advisory, *Guru Grades*: https://www.cxoadvisory.com/gurus/
30. Wikipedia, Larry R. Williams: https://en.wikipedia.org/wiki/Larry_R._Williams · Minervini (cita de N. Zadeh): https://www.minervini.com/
31. Wikipedia, Jack D. Schwager (bibliografía de *Market Wizards*): https://en.wikipedia.org/wiki/Jack_D._Schwager
32. Chen, H., De, P., Hu, Y., Hwang, B.-H. (2014). "Wisdom of Crowds…". *RFS* 27(5):1367-1403. https://doi.org/10.1093/rfs/hhu001
33. Farrell, M., Green, T. C., Jame, R., Markov, S. (2022). "The Democratization of Investment Research and the Informativeness of Retail Investor Trading". *JFE* 145(2):616-641. https://doi.org/10.1016/j.jfineco.2021.07.018 · WP: http://russelljame.com/seeking_alpha_may_2019.pdf
34. Bradley, D., Hanousek, J., Jame, R., Xiao, Z. (2024). "Place Your Bets? The Value of Investment Research on Reddit's Wallstreetbets". *RFS* 37(5):1409-1459. https://doi.org/10.1093/rfs/hhad098
35. Cookson, J. A., Niessner, M. (2020). "Why Don't We Agree?" *JF* 75(1):173-228. https://doi.org/10.1111/jofi.12852
36. Cookson, J. A., Engelberg, J., Mullins, W. (2023). "Echo Chambers". *RFS* 36(2):450-500. https://academic.oup.com/rfs/article-abstract/36/2/450/6670640
37. Cookson, J. A., Lu, R., Mullins, W., Niessner, M. (2024). "The Social Signal". *JFE*. https://www.sciencedirect.com/science/article/pii/S0304405X2400093X
38. Renault, T. (2017). *JBF* 84:25-40. https://doi.org/10.1016/j.jbankfin.2017.07.002
39. Bartov, E., Faurel, L., Mohanram, P. (2018). *The Accounting Review* 93(3):25-57. https://doi.org/10.2308/accr-51865
40. Bollen, J., Mao, H., Zeng, X. (2011). "Twitter Mood Predicts the Stock Market". *J. Computational Science* 2(1):1-8. https://doi.org/10.1016/j.jocs.2010.12.007 · arXiv: https://arxiv.org/abs/1010.3003
41. Kakhbod, A., Kazempour, S., Livdan, D., Schürhoff, N. "Finfluencers" (versión del 27-dic-2024; AEA 2025): https://www.aeaweb.org/conference/2025/program/paper/i3ry3n4t · SSRN/SFI 23-30: https://doi.org/10.2139/ssrn.4428232
42. Crawford, S., Gray, W., Kern, A. (2017). "Why Do Fund Managers Identify and Share Profitable Ideas?" *JFQA* 52(5):1903-1926. https://doi.org/10.1017/s0022109017000588
43. Curac, C., Lobe, S., Walkshäusl, C. (2025). "Beyond Conventional Wisdom: How Self-Described Value Investors Tilt toward Growth and Outperform". *JPM* 52(3):219-242. https://doi.org/10.3905/jpm.2025.1.791
44. Barber, B., Odean, T. (2000). *JF* 55(2):773-806. https://doi.org/10.1111/0022-1082.00226
45. Barber, B., Lee, Y.-T., Liu, Y.-J., Odean, T. (2014). *J. Financial Markets* 18:1-24. https://doi.org/10.1016/j.finmar.2013.05.006 · PDF: https://faculty.haas.berkeley.edu/odean/papers/Day%20Traders/The%20Cross-Section%20of%20Speculator%20Skill.pdf
46. Barber, B., Lee, Y.-T., Liu, Y.-J., Odean, T. "Just How Much Do Individual Investors Lose by Trading?" (RFS 2009, según el archivo del autor): https://faculty.haas.berkeley.edu/odean/Papers%20current%20versions/JustHowMuchDoIndividualInvestorsLose_RFS_2009.pdf
47. Chague, F., De-Losso, R., Giovannetti, B. (2019). "Day Trading for a Living?" https://doi.org/10.2139/ssrn.3423101
48. Carhart, M. (1997). *JF* 52(1):57-82. https://doi.org/10.1111/j.1540-6261.1997.tb03808.x
49. Verificación de *handles* de X del 25-sep-2026: API de fxtwitter (https://api.fxtwitter.com/{handle}) y oEmbed de X (https://publish.x.com/oembed?url=https://x.com/{handle}); Wikidata P2002 como contraste (https://www.wikidata.org/wiki/Property:P2002)
50. Google Scholar (búsquedas de confirmación de VIC, WSB, *Echo Chambers*, *The Social Signal*, Renault y Bollen et al. 2021): https://scholar.google.com/
51. Wikipedia, Jim Chanos (cierre de fondos, WSJ nov-2023): https://en.wikipedia.org/wiki/Jim_Chanos

### Registro de lo no verificado

- El SPIVA EUA de mitad de 2026 y el U.S. Persistence Scorecard más reciente (el sitio de S&P devolvió 403).
- Las cifras de México del SPIVA Latinoamérica: vienen del cap. 02 y no se re-verificaron aquí.
- Los autores y textos de la crítica metodológica a DALBAR.
- El estudio de Fidelity sobre las pérdidas de los inversionistas de Magellan.
- El "4.5% anual desde 2005" de Pure Alpha (Wikipedia sin fuente primaria confirmada).
- Las cifras de Minervini y de otros ganadores del U.S. Investing Championship. Que Schwager verificara estados de cuenta en *Unknown Market Wizards*.
- El rendimiento del HFRI FWC en 2022. El SG CTA Index (distinto del SG Trend) por año.
- Que los ETFs de futuros gestionados (DBMF, KMLM) coticen en el SIC.
- El PME reciente (2015-2025) del *private equity*.
- El periodo muestral exacto de *Finfluencers* y de Chen et al. 2014.
- Que la organización de Crawford-Gray-Kern sea VIC: se infiere del resultado de Scholar, no del *abstract*.
- Cargos actuales de @ValeriaMoy y el antecedente de Banxico de @esquivelgerardo (no se afirman en la tabla).
