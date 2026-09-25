# Módulo 02 — Teoría de portafolio y asset pricing clásico: de Markowitz al zoológico de factores

> Nivel: maestría · Actualizado: 2026-09-25 · Grado de evidencia global: **B**. La matemática de media-varianza y la separación de Tobin son exactas bajo sus supuestos. La prima de mercado y el fracaso neto de la mayoría de los gestores activos son hechos de grado A. En cambio, el CAPM falla en los datos (la SML es demasiado plana) y las primas long-short de EUA decayeron después de publicarse: el promedio de SMB, HML, RMW, CMA y Mom en 2016-2025 fue ≈0 bruto (t = 0.07, cálculo propio con la French Data Library).

---

## 1. Objetivos de dominio (qué debe saber hacer quien "se titula" en este módulo)

1. Construir a mano y en código la frontera eficiente, el portafolio de mínima varianza y el portafolio tangente. Explicar por qué el optimizador con medias muestrales amplifica el error de estimación y cuánta historia haría falta para que le gane a 1/N.
2. Derivar la CML y la separación de Tobin, y conectar el peso óptimo en riesgo, w* = (μ − r_f)/(A·σ²), con el Kelly fraccional de `config/parametros.json`.
3. Enunciar el CAPM, estimar betas, trazar la SML y explicar con datos por qué falla en la sección cruzada (Black-Jensen-Scholes 1972, Fama-French 1992, 2004). Enunciar la crítica de Roll y lo que implica para elegir benchmark en MXN.
4. Distinguir APT, ICAPM y modelos de factores empíricos (FF3, Carhart, FF5, FF6, q, q5, Stambaugh-Yuan), y cómo se construye un factor 2×3.
5. Explicar la eficiencia de mercado (Fama 1970), el problema de la hipótesis conjunta y la paradoja de Grossman-Stiglitz, y derivar de ella dónde puede existir ventaja.
6. Citar con cifras la vida de cada prima (mercado, size, value, momentum, profitability, investment, low vol/BAB): muestra original, fuera de muestra, después de publicarse, neta de costos, EUA vs global vs emergentes.
7. Medir desempeño con Sharpe, Treynor, alfa de Jensen, M², information ratio, tracking error y ley fundamental, y saber cuántos años hacen falta para distinguir habilidad de suerte.
8. Resumir la evidencia sobre fondos activos (Carhart 1997, Fama-French 2010, Berk-Green 2004, Berk-van Binsbergen 2015, Choi-Zhao, SPIVA 2025 incluido México).
9. Convertir todo lo anterior en reglas del sistema: núcleo, satélite, validación, dimensionamiento y evaluación de rivales.

---

## 2. Núcleo teórico

### 2.1 Media-varianza (Markowitz 1952)

El inversionista elige pesos **w** para maximizar E(R_p) − (A/2)·σ²_p.
- E(R_p) = Σ w_i·μ_i ; σ²_p = Σ_i Σ_j w_i·w_j·σ_ij = **w'Σw**.
- Dos activos: σ²_p = w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρσ₁σ₂. Con σ₁ = 20%, σ₂ = 10%, ρ = 0.2 y 50/50, σ_p = **12.04%**, menos que el promedio simple de 15%. Esa diferencia es el beneficio de diversificar.
- Mínima varianza (dos activos): w₁ = (σ₂² − ρσ₁σ₂)/(σ₁² + σ₂² − 2ρσ₁σ₂). En el ejemplo, w₁ = 0.006/0.042 = **14.3%**.
- N activos con pesos iguales: σ²_p = (1/N)·var̄ + (1 − 1/N)·cov̄. Con acciones de 30% de volatilidad y correlación media de 0.3, el límite cuando N → ∞ es √(0.3·0.09) = **16.4%**, y con N = 20 ya se llega a 17.4%. El riesgo idiosincrático se elimina diversificando. El sistemático no.
- Frontera eficiente: es el conjunto de portafolios con la mínima σ para cada μ. Sin activo libre de riesgo es una hipérbola en el plano (σ, μ).

**Intuición económica:** lo que se paga es la contribución de un activo al riesgo del portafolio (su covarianza), no su varianza aislada.

**El problema práctico:** el optimizador trata las medias estimadas como verdad y concentra el peso en los activos con más error positivo. DeMiguel, Garlappi y Uppal (2009) prueban 14 modelos en 7 bases de datos y ninguno le gana de manera consistente a 1/N en Sharpe, equivalente cierto ni turnover. Para que la media-varianza muestral supere a 1/N harían falta unos **3,000 meses** de datos con 25 activos y unos **6,000** con 50. Los remedios estándar son la contracción de la covarianza (Ledoit-Wolf 2004), los priors de equilibrio (Black-Litterman 1992, que parte de los rendimientos implícitos en el CAPM global) y las restricciones de peso.

### 2.2 Activo libre de riesgo, CML y separación de Tobin (1958)

Si se añade un activo libre de riesgo r_f, todos los inversionistas eficientes combinan **el mismo** portafolio riesgoso tangente T con r_f. Esa es la separación de Tobin: la decisión de *qué* portafolio riesgoso tener es independiente de *cuánto* riesgo tomar.
- CML: E(R_p) = r_f + [(E(R_T) − r_f)/σ_T]·σ_p. La pendiente es el Sharpe del tangente.
- Peso óptimo en T: w* = (E(R_T) − r_f)/(A·σ²_T).
- **Puente a Kelly:** con utilidad logarítmica (A = 1), w*_Kelly = (μ − r_f)/σ², y el Kelly fraccional es f·w*_Kelly. Ejemplo con el mercado de EUA 1963-2026 (prima aritmética de 7.19% y σ de 15.45%, cálculo propio): Kelly completo = 0.0719/0.0239 = **3.0×** y ¼ de Kelly = **0.75**. Si la prima se recorta a 5%, Kelly completo = 2.09× y ¼ de Kelly = **0.52**. *Inferencia:* el benchmark del sistema (50% acciones / 50% CETES) equivale casi exactamente a ¼ de Kelly con una prima recortada. El `kelly.fraccion_max = 0.25` del perfil estándar es coherente con la teoría.

### 2.3 CAPM (Sharpe 1964; Lintner 1965; Mossin 1966), SML y beta

Supuestos: media-varianza, expectativas homogéneas, préstamo y endeudamiento ilimitados a r_f, sin fricciones. En equilibrio el portafolio tangente es el de mercado M, y:
- **SML:** E(R_i) = r_f + β_i·[E(R_M) − r_f] ; β_i = Cov(R_i, R_M)/Var(R_M).
- Riesgo total = β²σ²_M + σ²_ε. Solo se paga β.
- Alfa ex-ante = rendimiento esperado propio − rendimiento de la SML. Ejemplo: con r_f = 4%, E(R_M) = 10% y β = 1.3, la SML da **11.8%**. Si el análisis propio espera 14%, α = +2.2% y el activo queda por encima de la SML (subvaluado).
- **Evidencia:** Black, Jensen y Scholes (1972) y Fama-MacBeth (1973) encuentran una SML más plana que la teórica. Fama y French (1992) reportan que la relación entre β y rendimiento promedio es plana cuando β varía independientemente del tamaño, y en 2004 concluyen que el historial empírico del CAPM es "lo bastante pobre para invalidar la forma en que se usa en aplicaciones". Grado **D** para el CAPM como modelo de la sección cruzada. Grado **A** para su núcleo: la prima de mercado existe y la diversificación es gratis.

### 2.4 Extensiones teóricas
- **Black (1972), CAPM de beta cero:** si el endeudamiento está restringido, la SML parte de E(R_z) > r_f y es más plana. Es la raíz teórica de "betting against beta": los inversionistas que no pueden apalancarse sobrepagan las acciones de beta alta.
- **Merton (1973), ICAPM:** cuando las oportunidades de inversión cambian en el tiempo, se pagan también las covarianzas con las variables de estado. Justifica en teoría los modelos multifactoriales, pero no dice cuáles son los factores.

### 2.5 Crítica de Roll (1977)
La linealidad entre rendimiento y beta es matemáticamente equivalente a que el proxy de mercado sea eficiente en media-varianza. El portafolio de mercado verdadero incluye todos los activos (capital humano, bienes raíces, empresas privadas) y no es observable. Por eso el CAPM no es comprobable, y el "alfa" depende del benchmark elegido. **Implicación para el sistema:** el alfa se mide siempre contra el benchmark declarado (50% S&P 500 TR en MXN + 50% CETES 28), nunca contra uno elegido después de ver los resultados.

### 2.6 APT (Ross 1976)
Si los rendimientos siguen R_i = E(R_i) + Σ_k β_ik·F_k + ε_i y no hay arbitraje, entonces E(R_i) ≈ r_f + Σ_k β_ik·λ_k. No exige que el mercado sea eficiente ni dice cuáles son los factores, que pueden ser macroeconómicos, estadísticos (componentes principales) o de características. Es la base de los modelos de riesgo comerciales y de la lógica de "cobertura de factores".

### 2.7 Eficiencia de mercado (Fama 1970) y Grossman-Stiglitz (1980)
- Tres formas: **débil** (los precios pasados no predicen), **semifuerte** (la información pública ya está en el precio) y **fuerte** (también la privada).
- **Hipótesis conjunta:** toda prueba de eficiencia es también una prueba del modelo de equilibrio. Una anomalía puede ser un modelo de riesgo mal especificado o un error de precios.
- **Grossman-Stiglitz:** si los precios reflejaran toda la información, nadie pagaría por conseguirla, y entonces no podrían reflejarla. En equilibrio los mercados son *casi* eficientes, y el rendimiento de informarse apenas compensa su costo. **Consecuencia operable:** la ventaja existe, pero es pequeña y se la llevan quienes tienen menos costos, más capacidad o más paciencia. Una ventaja que no supera nuestros costos totales (comisión, spread, impuestos y tiempo) no es ventaja.

### 2.8 Modelos de factores empíricos
Construcción estándar 2×3: las acciones se clasifican en junio de cada año por tamaño (mediana del NYSE) y por la característica (percentiles 30/70 del NYSE). Se forman seis portafolios ponderados por valor, y el factor es el promedio de los "altos" menos el promedio de los "bajos". **Son long-short, brutos y sin costos.**

| Modelo | Ecuación (exceso de rendimiento R_i − r_f) |
|---|---|
| FF3 (1993) | α + b·MKT + s·SMB + h·HML |
| Carhart (1997) | FF3 + m·MOM (ganadores 12-2 meses menos perdedores) |
| FF5 (2015) | α + b·MKT + s·SMB + h·HML + r·RMW + c·CMA |
| FF6 (2018) | FF5 + m·UMD |
| q-factor HXZ (2015) | MKT + ME + I/A + ROE |
| q5 HMXZ (2021) | q + EG (crecimiento esperado) |
| Stambaugh-Yuan (2017) | MKT + SMB + MGMT + PERF (11 anomalías agrupadas en dos clusters) |

**Base teórica de FF5:** a partir del modelo de dividendos, M_t/B_t = Σ E(Y_{t+τ} − dB_{t+τ})/(1+r)^τ / B_t. Con todo lo demás constante, un B/M alto, una rentabilidad alta o una inversión baja implican un r (rendimiento esperado) alto. La teoría q de inversión (HXZ) llega a las mismas predicciones desde el lado de la empresa. En FF5, HML se vuelve **redundante** en la muestra 1963-2013, porque RMW y CMA la absorben.

### 2.9 ¿Riesgo o error? Por qué existiría cada prima
- **Riesgo:** value como riesgo de dificultades financieras o de desinversión costosa; momentum como riesgo de choques (Daniel-Moskowitz: pagos tipo opción corta en estados de pánico).
- **Error:** LSV (1994) atribuyen value a la extrapolación del crecimiento pasado. Jegadeesh-Titman (1993, 2001) atribuyen momentum a una subreacción seguida de una reversión parcial.
- **Restricciones:** los inversionistas que no pueden apalancarse sobrepagan la beta alta (Frazzini-Pedersen 2014). Los mandatos contra un benchmark limitan el arbitraje de baja volatilidad (Baker-Bradley-Wurgler 2011).
- *Inferencia:* las primas por riesgo o por restricciones persisten mejor después de publicarse que las que vienen de un error fácil de arbitrar. Esto concuerda con lo que se observa: sobreviven mejor market, momentum global, value en emergentes y profitability. Size en EUA y la mayoría de las anomalías de fricción no sobreviven.

### 2.10 Medición de desempeño
- **Sharpe** = (R_p − r_f)/σ_p. Para portafolios completos. Supone una distribución aproximadamente normal.
- **Treynor** = (R_p − r_f)/β_p. Solo sirve para un componente de un portafolio ya diversificado.
- **Alfa de Jensen** = R_p − [r_f + β_p(R_M − r_f)]. Es el intercepto de la regresión y se extiende a multifactor (alfa FF5/FF6).
- **M²** = r_f + Sharpe_p·σ_M. Es el rendimiento del portafolio escalado a la volatilidad del benchmark.
- **Tracking error** TE = σ(R_p − R_B). **Information ratio** IR = (R_p − R_B)/TE. **Appraisal ratio** = α/σ_ε.
- **Ley fundamental (Grinold 1989):** IR ≈ IC·√BR. Con IC = 0.05 y 100 apuestas independientes al año, IR = 0.5. La versión del currículo CFA multiplica por el coeficiente de transferencia (TC) cuando hay restricciones, así que un TC de 0.5 deja el IR en 0.25.
- **¿Cuántos años para demostrar habilidad?** t ≈ IR·√T. Para un IR de 0.5 hacen falta 16 años para llegar a t = 2 y **36 años** para t = 3. La mayoría de los "track records" no distingue habilidad de suerte. **Refinamiento (adenda 2026-09-25, examen diagnóstico S3-04):** la versión más exacta del t del alfa de una regresión de expansión (B sobre A) divide además entre √(1 + SR_A²); ese SR_A debe estar en la **misma frecuencia que los datos de la regresión** (mensual si T se cuenta en meses), no en su versión anualizada — usar el anualizado por error infla o desinfla el t calculado.
- **Prueba de diferencia de dos Sharpes (Jobson-Korkie 1981, JF 36:889-908, con la corrección de Memmel 2003, Finance Letters 1:21-23):** bajo normalidad i.i.d. bivariada, √T(ŜR_B − ŜR_A) → N(0, V) con V = 2 − 2ρ + 0.5(SR_A² + SR_B² − 2·SR_A·SR_B·ρ²), Sharpes en la frecuencia de los datos. Con series de colas pesadas, heterocedasticidad o dependencia serial (p. ej. estrategias de momentum), esta prueba pierde validez; Ledoit y Wolf (2008), *"Robust Performance Hypothesis Testing with the Sharpe Ratio"*, J. Empirical Finance 15(5):850-859, proponen en su lugar un intervalo de confianza con *bootstrap* studentizado de bloques circulares. https://www.econ.uzh.ch/dam/jcr:ffffffff-935a-b0d6-0000-00007214c2bc/jef_2008pdf.pdf
- Ejemplo integrado: R_p = 12%, σ_p = 18%, β = 1.2, r_f = 4%, R_M = 10%, σ_M = 15%. Sharpe 0.444 vs 0.40 del mercado. Treynor 6.67 vs 6.0. α de Jensen = 12 − 11.2 = **+0.8%**. M² = 4 + 0.444·15 = 10.67%, es decir +0.67% sobre el mercado a igual riesgo.

### 2.11 Gestión activa en equilibrio (Berk-Green 2004)
Si los gestores tienen habilidad con rendimientos decrecientes a escala y el capital persigue el desempeño, los flujos entran hasta que el alfa neto del inversionista es cero. **Consecuencia:** la ausencia de persistencia en el alfa neto no prueba que no haya habilidad. Berk-van Binsbergen (2015) la miden como valor extraído, en promedio unos **US$3.2 millones al año por fondo**, pero esa habilidad la cobra el gestor en comisiones, no el cliente. *Inferencia para el sistema:* nuestro capital pequeño (20,000 MXN en la arena) no sufre de escala. Esa es una ventaja estructural real frente a los fondos grandes, pero solo en estrategias de baja capacidad que sigan siendo rentables netas de costos minoristas.

---

## 3. Literatura canónica

| Autores | Año | Título | Revista/Editorial | Hallazgo clave cuantificado | Enlace/DOI | Grado |
|---|---|---|---|---|---|---|
| Markowitz | 1952 | Portfolio Selection | JF 7(1):77-91 | Media-varianza. Se paga la covarianza, no la varianza | 10.1111/j.1540-6261.1952.tb01525.x | A (teoría) |
| Tobin | 1958 | Liquidity Preference as Behavior Towards Risk | RES 25(2):65-86 | Separación: un solo portafolio riesgoso + r_f | academic.oup.com/restud/article-abstract/25/2/65/1550009 | A (teoría) |
| Sharpe | 1964 | Capital Asset Prices… | JF 19(3):425-442 | CAPM: E(R_i) lineal en β | 10.1111/j.1540-6261.1964.tb02865.x | D empírico |
| Lintner | 1965 | The Valuation of Risk Assets… | REStat 47(1):13-37 | Derivación independiente del CAPM | semanticscholar (ver §9) | D empírico |
| Mossin | 1966 | Equilibrium in a Capital Asset Market | Econometrica 34(4):768-783 | Equilibrio general. "Línea de mercado" | econometricsociety.org | D empírico |
| Treynor | 1965 | How to Rate Management of Investment Funds | HBR 43:63-75 | Rendimiento por unidad de β | Wiley (reimpr.) | A (medida) |
| Sharpe | 1966 | Mutual Fund Performance | J. Business 39(1):119-138 | Razón recompensa/variabilidad | ideas.repec.org | A (medida) |
| Jensen | 1968 | The Performance of Mutual Funds 1945-1964 | JF 23(2):389-416 | Alfa. 115 fondos sin habilidad predictiva neta | 10.1111/j.1540-6261.1968.tb00815.x | A |
| Fama | 1970 | Efficient Capital Markets | JF 25(2):383-417 | Formas débil, semifuerte y fuerte | 10.1111/j.1540-6261.1970.tb00518.x | B |
| Black | 1972 | Capital Market Equilibrium with Restricted Borrowing | J. Business 45(3):444-455 | CAPM de beta cero. SML más plana | ideas.repec.org | B |
| Black, Jensen, Scholes | 1972 | The CAPM: Some Empirical Tests | Studies in the Theory of Capital Markets (Jensen, ed.):79-121 | Pendiente de la SML menor que la teórica | SSRN 908569 | A (hecho) |
| Fama, MacBeth | 1973 | Risk, Return, and Equilibrium | JPE 81(3):607-636 | Método de regresiones cruzadas | ideas.repec.org | A (método) |
| Merton | 1973 | An Intertemporal CAPM | Econometrica 41(5):867-887 | Se pagan también las variables de estado | econometricsociety.org | B (teoría) |
| Ross | 1976 | The Arbitrage Theory of Capital Asset Pricing | JET 13(3):341-360 | APT por no arbitraje | 10.1016/0022-0531(76)90046-6 | A (teoría) |
| Roll | 1977 | A Critique of the Asset Pricing Theory's Tests | JFE 4(2):129-176 | CAPM incomprobable sin el mercado verdadero | ideas.repec.org | A (lógica) |
| Basu | 1977 | Investment Performance… P/E Ratios | JF 32(3):663-682 | P/E bajo → alfa mayor | 10.1111/j.1540-6261.1977.tb01979.x | B |
| Grossman, Stiglitz | 1980 | On the Impossibility of Informationally Efficient Markets | AER 70(3):393-408 | Equilibrio con ineficiencia que paga la información | aeaweb.org | A (teoría) |
| Banz | 1981 | Return and Market Value of Common Stocks | JFE 9(1):3-18 | Efecto tamaño concentrado en las muy pequeñas | 10.1016/0304-405X(81)90018-0 | D (post) |
| Grinold | 1989 | The Fundamental Law of Active Management | JPM 15(3):30-37 | IR = IC·√BR | 10.3905/jpm.1989.409211 | A (identidad aprox.) |
| Fama, French | 1992 | The Cross-Section of Expected Stock Returns | JF 47(2):427-465 | β plana. Tamaño y B/M explican la sección cruzada | 10.1111/j.1540-6261.1992.tb04398.x | A (hecho) |
| Black, Litterman | 1992 | Global Portfolio Optimization | FAJ 48(5):28-43 | Prior de equilibrio + vistas | 10.2469/faj.v48.n5.28 | B (práctica) |
| Fama, French | 1993 | Common Risk Factors in… Stocks and Bonds | JFE 33(1):3-56 | FF3. Primas de 43/27/40 pb al mes (Rm-Rf/SMB/HML, 1963-91) | sciencedirect 0304405X93900235 | B |
| Jegadeesh, Titman | 1993 | Returns to Buying Winners and Selling Losers | JF 48(1):65-91 | 3-12 meses. ~1% mensual (6/6, t≈3.07; 1965-89) | 10.1111/j.1540-6261.1993.tb04702.x | B |
| Lakonishok, Shleifer, Vishny | 1994 | Contrarian Investment, Extrapolation, and Risk | JF 49(5):1541-1578 | Value 19.8% vs glamour 9.3% anual (+10.5 pp) | 10.1111/j.1540-6261.1994.tb04772.x | B |
| Carhart | 1997 | On Persistence in Mutual Fund Performance | JF 52(1):57-82 | Diferencial top-bottom de 8%/año: 4.6 factores, 2.0 costos, 1.4 sin explicar | 10.1111/j.1540-6261.1997.tb03808.x | A |
| Jegadeesh, Titman | 2001 | Profitability of Momentum Strategies | JF 56(2):699-720 | Momentum persiste en 1990-98 (fuera de muestra) | 10.1111/0022-1082.00342 | B |
| Berk, Green | 2004 | Mutual Fund Flows and Performance in Rational Markets | JPE 112(6):1269-1295 | Los flujos eliminan el alfa neto aunque haya habilidad | 10.1086/424739 | A (teoría) |
| Fama, French | 2004 | The CAPM: Theory and Evidence | JEP 18(3):25-46 | Evidencia "pobre" para el CAPM | 10.1257/0895330042162430 | A |
| Ledoit, Wolf | 2004 | Honey, I Shrunk the Sample Covariance Matrix | JPM 30(4):110-119 | La contracción baja el TE y sube el IR | ledoit.net/honey.pdf | A (práctica) |
| Ang, Hodrick, Xing, Zhang | 2006 | The Cross-Section of Volatility and Expected Returns | JF 61(1):259-299 | Volatilidad idiosincrática alta → rendimientos bajos | 10.1111/j.1540-6261.2006.00836.x | C |
| DeMiguel, Garlappi, Uppal | 2009 | Optimal Versus Naive Diversification | RFS 22(5):1915-1953 | Ningún modelo le gana a 1/N. Harían falta ~3,000 meses | academic.oup.com (ver §9) | A |
| Cremers, Petajisto | 2009 | How Active Is Your Fund Manager? | RFS 22(9):3329-3365 | Active Share. Umbral de closet indexer ~60% | academic.oup.com (ver §9) | C |
| Barras, Scaillet, Wermers | 2010 | False Discoveries in Mutual Fund Performance | JF 65(1):179-216 | ~75% alfa cero, ~1/5 alfa negativo, pocos hábiles | 10.1111/j.1540-6261.2009.01527.x | A |
| Fama, French | 2010 | Luck versus Skill… Mutual Fund Returns | JF 65(5):1915-1947 | Pocos fondos cubren sus costos. Habilidad solo en las colas (bruto) | 10.1111/j.1540-6261.2010.01598.x | A |
| Baker, Bradley, Wurgler | 2011 | Benchmarks as Limits to Arbitrage | FAJ 67(1) | La beta y la vol altas rinden menos. Los benchmarks limitan el arbitraje | 10.2469/faj.v67.n1.4 | B |
| Novy-Marx | 2013 | The Other Side of Value: Gross Profitability | JFE 108(1):1-28 | GP/activos predice tanto como B/M | sciencedirect S0304405X13000044 | B |
| Asness, Moskowitz, Pedersen | 2013 | Value and Momentum Everywhere | JF 68(3):929-985 | 8 mercados. Corr V-M ≈ −0.6. Combinación 50/50 con Sharpe 1.42 (bruto) | 10.1111/jofi.12021 | A/B |
| Frazzini, Pedersen | 2014 | Betting Against Beta | JFE 111(1):1-25 | BAB en EUA con Sharpe 0.78 (1926-2012) | stern.nyu.edu (ver §9) | C (disputa) |
| Fama, French | 2015 | A Five-Factor Asset Pricing Model | JFE 116(1):1-22 | HML redundante con RMW y CMA | sciencedirect S0304405X14002323 | B |
| Hou, Xue, Zhang | 2015 | Digesting Anomalies | RFS 28(3):650-705 | Q-factor. ~½ de ~80 anomalías no son significativas | academic.oup.com (ver §9) | B (modelo) |
| Berk, van Binsbergen | 2015 | Measuring Skill in the Mutual Fund Industry | JFE 118(1):1-20 | La habilidad existe como valor extraído (~US$3.2 M/año por fondo) y la cobra el gestor | sciencedirect S0304405X15000628 | B |
| Harvey, Liu, Zhu | 2016 | …and the Cross-Section of Expected Returns | RFS 29(1):5-68 | Vara de t > 3.0 por pruebas múltiples | academic.oup.com (ver §9) | A (método) |
| McLean, Pontiff | 2016 | Does Academic Research Destroy Predictability? | JF 71(1):5-32 | 97 predictores: −26% fuera de muestra y −58% después de publicarse | 10.1111/jofi.12365 | A |
| Novy-Marx, Velikov | 2016 | A Taxonomy of Anomalies and Their Trading Costs | RFS 29(1):104-147 | Con turnover <50%/mes suelen sobrevivir netas. Costos de 20-57 pb por operación (turnover medio) | academic.oup.com (ver §9) | A |
| Daniel, Moskowitz | 2016 | Momentum Crashes | JFE 122(2):221-247 | Crashes tras caídas y con vol alta, en los rebotes | sciencedirect S0304405X16301490 | A |
| Stambaugh, Yuan | 2017 | Mispricing Factors | RFS 30(4):1270-1315 | MGMT/PERF con 11 anomalías superan a FF5 y q | academic.oup.com (ver §9) | B (modelo) |
| Moreira, Muir | 2017 | Volatility-Managed Portfolios | JF 72(4):1611-1644 | Escalar por 1/vol genera alfa (in-sample) | 10.1111/jofi.12513 | C |
| Fama, French | 2018 | Choosing Factors | JFE 128(2):234-252 | FF6 (+momentum). Criterio del Sharpe² máximo | sciencedirect S0304405X18300515 | B |
| Asness et al. | 2018 | Size Matters, if You Control Your Junk | JFE 129(3):479-509 | El tamaño revive controlando por calidad (24 países) | econpapers (ver §9) | C |
| Alquist, Israel, Moskowitz | 2018 | Fact, Fiction, and the Size Effect | JPM | Size débil desde su descubrimiento. Enero e iliquidez | 10.3905/jpm.2018.1.082 | A (sobre su debilidad) |
| Asness, Frazzini, Pedersen | 2019 | Quality Minus Junk | RAS 24(1):34-112 | QMJ significativo en EUA y 24 países | 10.1007/s11142-018-9470-2 | B |
| Hou, Xue, Zhang | 2020 | Replicating Anomalies | RFS 33(5):2019-2133 | 65% de 452 falla con \|t\|≥1.96 y 82% con 2.78 | academic.oup.com (ver §9) | A |
| Cederburg et al. | 2020 | On the Performance of Volatility-Managed Portfolios | JFE 138(1):95-117 | 103 estrategias: fuera de muestra no le ganan al original | sciencedirect S0304405X2030132X | A |
| Feng, Giglio, Xiu | 2020 | Taming the Factor Zoo | JF 75(3):1327-1370 | La mayoría de los factores nuevos son redundantes | 10.1111/jofi.12883 | A (método) |
| Gu, Kelly, Xiu | 2020 | Empirical Asset Pricing via Machine Learning | RFS 33(5):2223-2273 | Árboles y redes neuronales, a veces con el doble de desempeño (bruto) | academic.oup.com (ver §9) | C (neto) |
| Fama, French | 2021 | The Value Premium | RAPS 11(1):105-121 | Prima de value mucho menor en 1991-2019 vs 1963-1991 | academic.oup.com (ver §9) | B |
| Arnott, Harvey, Kalesnik, Linnainmaa | 2021 | Reports of Value's Death May Be Greatly Exaggerated | FAJ 77(1):44-67 | Drawdown de HML de 55% a mediados de 2020. Lo explica el diferencial de valuación | 10.1080/0015198X.2020.1842704 | B |
| Baltussen, Swinkels, van Vliet | 2021 | Global Factor Premiums | JFE 142(3):1128-1154 | 24 primas, 1800-2016. Poco decaimiento fuera de muestra | sciencedirect S0304405X21003007 | A |
| Hou, Mo, Xue, Zhang | 2021 | An Augmented q-Factor Model with Expected Growth | RoF 25(1):1-41 | Factor EG de 0.84%/mes (t = 10.27) | academic.oup.com (ver §9) | C (reciente) |
| Ilmanen et al. | 2021 | How Do Factor Premia Vary Over Time? | JoIM 19(4) | Un siglo, 6 clases de activo. La variación no se liga a la macro | joim.com | A |
| Ehsani, Linnainmaa | 2022 | Factor Momentum and the Momentum Factor | JF 77(3):1877-1919 | Factor tras un año malo: 6 pb/mes. Tras uno bueno: 51 pb | 10.1111/jofi.13131 | B |
| Harvey, Liu | 2022 | Luck versus Skill… Reexamining the Evidence | JF 77(3):1921-1966 | El bootstrap de FF2010 tiene poca potencia (submuestreo) | 10.1111/jofi.13123 | B |
| Chen, Zimmermann | 2022 | Open Source Cross-Sectional Asset Pricing | CFR 11(2):207-264 | 319 señales. 98% de las claramente significativas replica | openassetpricing.com | A |
| Novy-Marx, Velikov | 2022 | Betting Against Betting Against Beta | JFE 143(1):80-106 | BAB ≈ equiponderado. US$1.05 por dólar en el 1% más pequeño | sciencedirect S0304405X21002051 | A (crítica) |

---

## 4. Lo más reciente 2023-2026

- **Jensen, Kelly y Pedersen (JF, oct-2023), "Is There a Replication Crisis in Finance?"** La mayoría de los factores se replica. Se agrupan en 13 temas, la mayoría de ellos parte significativa del portafolio tangente, y funcionan fuera de muestra en 93 países. El número de factores *refuerza* la evidencia en un marco bayesiano. Código abierto en GitHub (bkelly-lab). Grado A como replicación bruta. No dice nada sobre la rentabilidad neta para un minorista.
- **Chen y Velikov (JFQA 58(3), 2023), "Zeroing In on the Expected Returns of Anomalies".** Toman 204 anomalías y descuentan el spread efectivo, el efecto de la publicación y la era de trading moderno (desde principios de los 2000). El rendimiento esperado de la anomalía promedio queda en **4 pb al mes**. Es la cifra más sobria de la literatura.
- **Detzel, Novy-Marx y Velikov (JF 78(3), 2023), "Model Comparison with Transaction Costs".** Ignorar costos sesga las comparaciones a favor de los factores caros. Con costos, FF5 tiene un Sharpe² significativamente mayor que el q-factor y que el modelo de seis factores de Barillas-Shanken.
- **Bryzgalova, Huang y Julliard (JF 78(1), 2023).** Evalúan 2.25 cuatrillones de modelos. El SDF promediado por modelos bayesianos (BMA) supera a los modelos existentes dentro y fuera de muestra.
- **Fama y French (dic-2023), "Production of U.S. Rm-Rf, SMB, and HML in the Fama-French Data Library"** (Chicago Booth 23-22). Las correcciones de CRSP y Compustat y los cambios de reglas (FASB 106, FASB 109, vínculos CRSP) mueven poco los promedios entre las versiones de 2002-12 y 2023-07: HML +3.03 pb al mes, SMB −0.77 y Rm-Rf +0.35. Las primas originales de FF93 (1963-91) eran de 43, 27 y 40 pb al mes. La biblioteca recalcula la historia en cada versión.
- **Kelly, Malamud y Zhou (JF 79(1), 2024), "The Virtue of Complexity in Return Prediction".** Prueban en teoría que los modelos con más parámetros que observaciones pueden superar a los simples al predecir el mercado. **Contrapunto de 2026:** Guo, Huang, Li y Yu (arXiv 2608.23761, 24-ago-2026) documentan el "double descent", pero concluyen que ni ridge ni ridgeless le ganan al promedio histórico. Grado C, en disputa activa.
- **Jensen, Kelly, Malamud y Pedersen, "Machine Learning and the Implementable Efficient Frontier"** (RFS, 2026). Proponen evaluar estrategias por su rendimiento neto de costos para cada nivel de riesgo. El ML que ignora costos sobrepondera características efímeras de baja capitalización. Aprender directamente los pesos con un objetivo económico mejora la frontera neta.
- **Chen, Lopez-Lira y Zimmermann (arXiv 2212.10317, versión del 29-dic-2025), "Does Peer-Reviewed Research Help Predict Stock Returns?"** Minar 29,000 razones contables con t > 2 produce una predictibilidad similar a la de las señales publicadas. En ambos casos sobrevive ~**50%** después de la muestra original. *Inferencia:* el descuento correcto para cualquier señal "descubierta" es de ~50%, venga de un journal o de un backtest propio.
- **Dickerson, Julliard y Mueller (JFE 2026, "The Co-Pricing Factor Zoo").** Evalúan 18 cuatrillones de modelos conjuntos para bonos corporativos y acciones. Los factores de acciones y no negociables bastan para los bonos una vez controlado el riesgo de plazo. El SDF BMA logra un Sharpe fuera de muestra de 1.5-1.8, **bruto y teórico**.
- **van Vliet, Baltussen, Dom y Vidojevic (SSRN 5561720, ago-2025; JPM dic-2025), "Momentum Factor Investing: Evidence and Evolution".** Encuentran soporte robusto para momentum en hasta ~150 años de datos locales y globales. El momentum con gestión de riesgo mitiga los crashes.
- **Datos nuevos:** la French Data Library tiene datos de EUA hasta **julio de 2026** (CRSP 202607) e internacionales hasta 2026-08 (Bloomberg). Desde 2025 usa el formato CIZ de CRSP, en el que los rendimientos mensuales se componen de rendimientos diarios con dividendos reinvertidos en la fecha ex. Es otra razón por la que la historia cambia entre versiones.
- **SPIVA EUA, cierre 2025:** 79% de los fondos large-cap activos quedó por debajo del S&P 500 en 2025 (65% en 2024), el cuarto peor año en 25. En 20 años, ~92% de los fondos domésticos quedó por debajo de su benchmark (según resúmenes del reporte; el PDF bloqueó la descarga).
- **SPIVA Latinoamérica, cierre 2025 (México):** el S&P/BMV IRT subió 35.2% en 2025. El **75.6%** de los fondos activos de renta variable mexicana quedó por debajo en 1 año, y 69.8%, 77.3% y 75.6% en 3, 5 y 10 años. La mediana quedó 3.0% abajo en 2025 y 3.1% abajo en 10 años.
- **Morningstar Active/Passive Barometer, cierre 2025:** solo **21%** de los fondos activos sobrevivió y superó a sus pares pasivos en 10 años. El quintil más barato tuvo 31% de éxito y el más caro 17%.
- **Currículo CFA 2026:** el Nivel III se divide en un núcleo (65-70%: asignación de activos, construcción de portafolio, medición de desempeño, derivados y riesgo, ética) y tres pathways (30-35%: Portfolio Management, Private Wealth y Private Markets). El pathway de PM cubre indexación de mercado vs factores, tracking error, Active Share y presupuesto de riesgo. No hubo cambios en el Nivel III respecto a 2025. Los Niveles I-II cubren media-varianza, CAPM, SML y medidas de desempeño (lo que cubre §2 de este módulo), y el Nivel II agrega la ley fundamental de gestión activa (según material de preparación y la lectura de repaso de CFA Institute 2026 "Analysis of Active Portfolio Management").

---

## 5. Evidencia real: qué funciona, qué no, magnitudes y decaimiento

### 5.1 Primas de factores en EUA, medidas hasta julio de 2026 (cálculo propio)
Fuente: archivos `F-F_Research_Data_5_Factors_2x3` y `F-F_Momentum_Factor` (CRSP 202607), descargados el 2026-09-25. Media aritmética anualizada en % (estadístico t). **Brutas, long-short, sin costos.**

| Factor | 1963/07-2026/07 | 1963/07-1991/06 (≈muestra original) | 1992/01-2026/07 (post-FF93) | 2016-2025 (última década) | 2021-2025 | Ene-jul 2026 (acumulado) |
|---|---|---|---|---|---|---|
| Mkt-RF | 7.19 (3.70) | 4.55 (1.52) | 9.06 (3.54) | **12.96 (2.60)** | 10.42 | +7.4 |
| SMB | 2.25 (1.71) | 3.68 (1.89) | 1.14 (0.63) | −2.21 (−0.68) | −4.66 | +6.6 |
| HML | 3.59 (2.77) | 4.96 (2.98) | 2.81 (1.45) | **−0.49 (−0.12)** | 8.07 | +12.3 |
| RMW | 3.08 (3.10) | 2.39 (2.34) | 3.58 (2.22) | 3.55 (1.48) | 5.85 | −5.8 |
| CMA | 2.96 (3.27) | 3.76 (2.97) | 2.51 (1.95) | −0.65 (−0.24) | 1.30 | +7.2 |
| Mom | 7.25 (3.96) | 9.55 (4.20) | 4.92 (1.77) | **0.34 (0.08)** | 2.31 | +10.2 |

Series largas (archivo de 3 factores + Mom, desde 1926):
- **HML:** 4.26%/año (t = 3.46) en 1926-2026. Antes de 1992, 5.02% (t = 3.18). De 1992 en adelante, 2.81% (t = 1.45). Peor drawdown: **−57.8% de dic-2006 a sep-2020**, 14 años.
- **Mom:** 7.41% (t = 4.55) en 1927-2026. En 1927-1989 (antes de JT93), 8.53% (t = 4.15). En 1994-2026, 4.49% (t = 1.54). Desde 2000, 2.47% (t = 0.72). Drawdowns: **−78.4% (1932-06 a 1939-09)** y **−57.8% (2008-11 a 2009-09)**. Solo abril de 2009 fue −34.4%, y de marzo a septiembre de 2009 se acumuló −56.4%.
- **SMB:** 1.99% (t = 1.82) en 1926-2026. De 1992 en adelante, **0.66% (t = 0.36)**. El efecto tamaño de EUA **no existe estadísticamente desde su publicación**.
- **Combinaciones:** HML+Mom 50/50 en 1963-2026 dio 5.42% (t = 5.34, Sharpe 0.67), con una correlación HML-Mom de −0.19 (−0.30 en 2016-25). En **2016-2025 dio −0.07% (Sharpe −0.01)**. El promedio equiponderado de los cinco factores sin mercado tuvo Sharpe 0.84 (t = 6.65) en toda la muestra y **0.11%/año (t = 0.07) en 2016-2025**.

**Lectura:** en la última década de EUA solo pagó bien la prima de mercado (12.96%/año). Profitability fue positiva pero no significativa, y value, momentum, size e investment fueron ≈0 o negativos. El rebote de value en 2021-22 y 2026 muestra que los drawdowns de factores terminan, pero no permite anticipar cuándo.

### 5.2 Internacional (French, en USD, brutas)

| Región / periodo | HML | RMW | WML (momentum) | SMB |
|---|---|---|---|---|
| Desarrollados 1990/07-2015 | 3.87 (2.39) | 4.36 (4.27) | 7.82 (2.85) | 1.20 (0.86) |
| Desarrollados 2016-2025 | 0.54 (0.16) | 2.56 (1.60) | 2.98 (0.96) | −3.20 (−1.82) |
| **Emergentes** 1990/07-2015 | 7.70 (4.56) | 2.64 (1.95) | 9.47 (4.50) | 2.24 (1.34) |
| **Emergentes 2016-2025** | **7.71 (3.04)** | 2.32 (1.69) | **10.32 (3.74)** | −2.19 (−1.32) |

México forma parte de la muestra de emergentes de French junto con otros 25 países. **En emergentes, value y momentum no decayeron.** Su t es mayor que 3 en la última década, en datos posteriores a su publicación. *Inferencia:* esto es consistente con límites al arbitraje más altos (costos, acceso, capacidad), así que parte de esa prima no es capturable neta por un minorista. Aun así es el lugar donde la evidencia post-publicación de estos dos factores es más fuerte. Grado B.

### 5.3 Magnitudes netas y decaimiento (resumen cuantitativo)
- **Decaimiento por publicación:** −26% fuera de muestra y −58% después de publicarse, en 97 predictores (McLean-Pontiff). En señales publicadas y minadas sobrevive ~50% (Chen-Lopez-Lira-Zimmermann).
- **Replicación:** HXZ 2020 encuentra que 65% de 452 anomalías falla con microcaps controladas, y 96% de las de fricciones de trading. Chen-Zimmermann 2022 encuentra que 98% de las claramente significativas se reproduce. JKP 2023 encuentra que la mayoría replica en 93 países. **Son compatibles:** las anomalías "fuertes" replican y las "débiles" o dominadas por microcaps no.
- **Neto:** la anomalía promedio rinde 4 pb al mes neta (Chen-Velikov). Solo sobreviven netas las de turnover < 50% mensual con reglas de mitigación (Novy-Marx-Velikov 2016). Size, value y profitability tienen la mayor capacidad.
- **Low vol / BAB:** el Sharpe de BAB de 0.78 (1926-2012) depende de una construcción que en la práctica es equiponderada y cargada a microcaps (Novy-Marx-Velikov 2022). Neta de costos, sigue positiva pero explicada por profitability e investment. Una cartera long-only de baja volatilidad no requiere apalancamiento y funciona como defensa. Primer trimestre de 2025: el S&P 500 Low Volatility le ganó al índice por 6% en marzo, mientras que momentum y quality fueron de los peores factores del trimestre (Morningstar / S&P DJI). Grado C como fuente de alfa y B como reductor de drawdown.
- **Gestión por volatilidad:** in-sample genera alfas (Moreira-Muir). En tiempo real, 103 estrategias no le ganan al original (Cederburg et al. 2020). Grado C como alfa y útil como control de riesgo.
- **Fondos activos:** Carhart encuentra que la persistencia se explica casi toda por factores y gastos, salvo en los peores fondos. La persistencia **desaparece en 1994-2018** (Choi-Zhao, NBER w26707). En México, 75.6% queda por debajo en 10 años (SPIVA 2025). Grado A: **no se compran fondos activos por su historial.**
- **Market timing con factores:** la variación temporal de las primas no se liga a la macro (Ilmanen et al. 2021). La única regla de timing con respaldo publicado es el *factor momentum* (Ehsani-Linnainmaa 2022: 51 vs 6 pb al mes según el año previo). Grado B-C.

### 5.4 La perspectiva MXN (cálculo propio: French Mkt en USD + FRED DEXMXUS de cierre de mes)
- Correlación entre el mercado de EUA en USD y la variación de USD/MXN: **−0.37** (1994-2026), **−0.51** (2000-2026) y **−0.40** (2016-2025). El peso se deprecia cuando caen las acciones de EUA.
- Volatilidad del mercado de EUA en 2000-2026: **15.7% en USD vs 13.8% en MXN**.
- Ejemplos: en oct-2008 fue −17.1% en USD y **−4.0% en MXN**. En mar-2020 fue −13.2% en USD y **+3.1% en MXN**.
- CAGR 2016-2025: 14.7% en USD y 15.3% en MXN.
- *Inferencia:* para un inversionista en MXN, la renta variable de EUA **sin cubrir** trae una cobertura natural contra las crisis. Cubrir el tipo de cambio por sistema aumentaría el drawdown en MXN justo en los peores meses. Grado B: robusto en 30 años, pero la relación puede cambiar de régimen.

---

## 6. Traducción operable (cómo lo usa el sistema para ganar)

Todas las cifras de riesgo vienen de `config/parametros.json`. En **fase 0** (`prioridad_actual`) estas reglas se aplican solo al portafolio de papel.

### 6.1 Reglas
1. **Núcleo = beta barata.** La única prima de grado A que se captura casi gratis es la de mercado. En el perfil estándar, el núcleo (≥ `estructura.nucleo_min` = 70%) replica o se acerca al benchmark principal (50% S&P 500 TR en MXN + 50% CETES 28) con ETFs indexados de bajo costo. *Inferencia:* 50% en acciones ≈ ¼ de Kelly con una prima recortada a 5% (§2.2), coherente con `kelly.fraccion_max = 0.25`.
2. **Sin cobertura cambiaria por defecto** en la renta variable de EUA (correlación de −0.4 a −0.5 con USD/MXN, §5.4). Cubrir solo si una estrategia validada lo justifica.
3. **Tilts de factores solo long-only, de bajo turnover y dentro del satélite** (≤ `estructura.satelite_max` = 30%). La prioridad sigue la evidencia post-publicación neta: (a) profitability/quality, (b) momentum con control de crash, (c) value con énfasis en emergentes y en medidas que incluyan intangibles. **Size aislado se excluye** (t = 0.36 desde 1992). Se excluyen también BAB apalancado y las estrategias long-short, porque `apalancamiento.bruto_max_fase_1 = 1.0`.
4. **Recorte obligatorio de primas** antes de dimensionar: μ_usable = 0.5 × μ_backtest para cualquier señal publicada o minada (Chen-Lopez-Lira-Zimmermann ~50%; McLean-Pontiff −58%). Después se restan los costos estimados de ida y vuelta. Si μ_usable neto ≤ 0, se descarta.
5. **Umbral estadístico:** t ≥ 3.0 en el backtest (HLZ 2016). Además aplican `validacion_estrategias`: ≥10 años, costos y slippage incluidos, probabilidad de Deflated Sharpe ≥ 0.95, PBO ≤ 0.25, papel ≥ 3 meses y ≥ 30 operaciones, y capital inicial al 25%. **Umbrales completos de HLZ (adenda 2026-09-25, examen diagnóstico S2-08), NBER w20592 §4.7, con 316 factores publicados hasta 2012:** sin pruebas ocultas, Bonferroni 3.78, Holm 3.64, BHY (FDR 1%) 3.39, BHY (FDR 5%) 2.78. Ajustando por el ≈71% de pruebas no publicadas que HLZ documentan (minería de datos oculta): Bonferroni **4.01**, Holm **3.96**, BHY 1% **3.68**, **BHY 5% = 3.18** — este último es el umbral concreto que sustenta la regla "t ≥ 3.0" de esta base. https://www.nber.org/system/files/working_papers/w20592/w20592.pdf
6. **Dimensionamiento:** w = f·μ_usable/σ², con f ≤ 0.25 en el perfil estándar y ≤ 0.5 en `arena_agresivo`, sujeto a `concentracion` (acción ≤ 10% estándar y ≤ 30% arena; sector ≤ 25%) y a `riesgo_por_operacion` (1% estándar, 3% arena).
7. **Control de crash de momentum:** si el mercado viene de una caída fuerte y la volatilidad realizada está alta (los estados de pánico de Daniel-Moskowitz), la exposición a momentum se reduce 50%. Los umbrales exactos (por ejemplo, rendimiento de 24 meses < 0 y volatilidad de 1 mes > percentil 80) son **parámetros del sistema por validar, no del paper**. Esto es consistente con el `filtro_apalancados` de la arena (subyacente sobre su media de 200 días y VIX < 25).
8. **Construcción:** nunca media-varianza con medias históricas. Se usan pesos 1/N o paridad de riesgo dentro de cada bloque, covarianza con contracción Ledoit-Wolf, y Black-Litterman si hay vistas explícitas. Límites duros de `concentracion`.
9. **Rebalanceo por bandas** (`rebalanceo`: ±5 pp absolutas o ±25% relativas, revisión mensual). Es la versión minorista del *buy/hold spread* de Novy-Marx-Velikov: más exigencia para entrar que para mantener.
10. **Vol-targeting como freno, no como fuente de alfa.** Se permite reducir exposición cuando la volatilidad sube para respetar `drawdown_objetivo = 12%` y los `cortacircuitos_drawdown`, pero ningún backtest puede atribuirle alfa (Cederburg et al.).
11. **Evaluación contra rivales:** en una temporada de 6 meses (`temporada_meses`), con σ = 16%/año y correlación de 0.8 entre dos portafolios, la σ de la diferencia es de ≈7.2% en 6 meses. Una ventaja real de 3%/año (1.5% en el semestre) gana la temporada solo el **~58%** de las veces. *Inferencia:* el torneo corto se decide sobre todo por la varianza y la beta, no por la habilidad. Por eso `modo_torneo` baja la varianza cuando va adelante por ≥ 5 pp y la sube, dentro de los límites, cuando va atrás por ≥ 5 pp. La habilidad solo se declara con varias temporadas y con un IR medido contra el benchmark.
12. **No se compran fondos activos mexicanos ni de EUA** por su historial (§5.3). Solo ETFs indexados o de factores con TER bajo.

### 6.2 Checklist de admisión de un factor o ETF al satélite
- [ ] Prima con grado A/B en ≥ 2 regiones y después de publicarse (tabla §5).
- [ ] μ_usable neto > 0 tras el recorte de 50% y los costos. Turnover del índice < 50% mensual (idealmente anual).
- [ ] Correlación con el núcleo < 0.9 y contribución marginal positiva al Sharpe del portafolio total (usar el criterio de Sharpe² de FF 2018, no el Sharpe aislado).
- [ ] Drawdown histórico del factor compatible con los cortacircuitos (HML −58% y Mom −58%/−78% long-short; las versiones long-only caen menos en relativo, pero con toda la beta).
- [ ] ETF disponible en GBM (SIC) con liquidez; verificar TER, spread y retención fiscal.
- [ ] Regla de salida escrita antes de entrar (tesis invalidada, límite de pérdida o racha según `rachas`).

### 6.3 Plantilla de evaluación de desempeño (mensual)
TWR en MXN · exceso vs benchmark principal · TE · IR · α y β del CAPM y de FF5+Mom (regresión sobre los factores de French convertidos a MXN) · Sharpe y Sortino · máximo drawdown vs `drawdown_objetivo` · t del alfa = IR·√años. No se declara habilidad con t < 2.

---

## 7. Trampas y errores comunes

1. **Optimizar con medias históricas.** El optimizador maximiza el error. Con 25 activos harían falta ~3,000 meses para ganarle a 1/N.
2. **Tratar los factores de French como rendimientos invertibles.** Son long-short, brutos, sin costos, sin impuestos y con cortos. Un ETF long-only captura solo una parte y trae toda la beta.
3. **Creer en la prima de tamaño.** En EUA fue 0.66%/año (t = 0.36) desde 1992. Solo reaparece controlando por calidad.
4. **Leer el Sharpe de BAB (0.78) sin ver su construcción.** Es en la práctica equiponderado, está cargado a microcaps y requiere apalancamiento.
5. **Ignorar el crash de momentum.** Llegó a −34% en un solo mes (abr-2009) y a −78% entre 1932 y 1939.
6. **Confundir dentro de muestra con después de publicar.** Al alfa de un paper hay que restarle ~50-58% y luego los costos. La anomalía promedio neta rinde 4 pb al mes.
7. **Elegir el benchmark después de ver el resultado** (crítica de Roll). Siempre se usa el benchmark declarado y en MXN.
8. **Usar Treynor o alfa CAPM para un portafolio concentrado.** El riesgo idiosincrático existe y cuenta. Usar Sharpe, IR y drawdown.
9. **Suponer normalidad en el Sharpe.** Las estrategias de venta de opciones o de carry lo inflan. Usar Deflated Sharpe y ver colas y drawdown.
10. **Perseguir fondos o estrategias ganadoras recientes.** La persistencia desapareció después de 1994 (Choi-Zhao), y los flujos de Berk-Green borran el alfa.
11. **Ignorar las versiones de los datos.** La biblioteca de French reescribe la historia (correcciones, FASB 109, CIZ 2025). Guarda la fecha de descarga en cada backtest.
12. **Sesgo de supervivencia y de look-ahead.** Hay que usar universos históricos, fechas de publicación contable reales y fondos que desaparecieron.
13. **Timing de factores por valuación.** La evidencia es débil. Solo el factor momentum tiene soporte publicado, y es moderado.
14. **Tomar un semestre de TWR como prueba de habilidad.** Con una ventaja real de 3%/año se gana solo el ~58% de las temporadas (§6.1, regla 11).
15. **Cubrir el tipo de cambio por reflejo.** Para un inversionista en MXN, el dólar es un amortiguador en las crisis (oct-2008: −17.1% en USD vs −4.0% en MXN).

---

## 8. Examen de titulación

1. **Dos activos con σ₁ = 20%, σ₂ = 10%, ρ = 0.2 y pesos 50/50. ¿Cuánto vale σ_p y cuál es el peso del activo 1 en mínima varianza?** σ_p = √0.0145 = 12.04%. w₁ = 0.006/0.042 = 14.3%.
2. **¿Qué dice la separación de Tobin y cómo se conecta con Kelly?** Todos tienen el mismo portafolio riesgoso tangente y solo cambia la mezcla con r_f. w* = (μ − r_f)/(Aσ²). Con A = 1 se obtiene Kelly completo, y el sistema usa f ≤ 0.25 (estándar).
3. **Si r_f = 4%, E(R_M) = 10%, β = 1.3 y se espera 14%, ¿cuál es el alfa ex-ante?** SML = 11.8%, así que α = +2.2% (el activo está subvaluado).
4. **¿Por qué el CAPM se considera fallido empíricamente si su lógica es correcta?** La SML observada es más plana (BJS 1972). β no explica la sección cruzada una vez que se controla por tamaño (FF 1992). FF 2004 lo califican de "pobre". La prima de mercado sí existe.
5. **Enuncia la crítica de Roll y su consecuencia práctica.** Probar el CAPM equivale a probar que el proxy de mercado es eficiente, y el mercado verdadero no es observable. El alfa depende del benchmark, así que se fija de antemano.
6. **¿Qué resuelve Grossman-Stiglitz y qué implica para el sistema?** Un mercado perfectamente eficiente es imposible si la información cuesta. Hay ventaja, pero solo compensa costos, así que la ventaja neta de costos es la única que cuenta.
7. **¿Por qué HML es redundante en FF5?** Sus rendimientos quedan explicados por sus exposiciones a RMW y CMA (y al mercado), con alfa ≈ 0 en 1963-2013.
8. **¿Cuánto decae una anomalía después de publicarse y cuánto rinde neta en promedio?** Rinde −26% fuera de muestra y −58% después de publicarse (McLean-Pontiff). La anomalía promedio neta, después de publicarse y en la era moderna, rinde ≈ 4 pb al mes (Chen-Velikov 2023).
9. **Con datos de French a jul-2026, ¿cuánto rindieron HML, Mom y SMB en EUA en 2016-2025?** −0.49%, +0.34% y −2.21% anual, todos con t no significativo. El mercado rindió 12.96%.
10. **¿Dónde sobrevivieron con fuerza value y momentum después de 2015?** En emergentes: HML 7.71% (t = 3.04) y WML 10.32% (t = 3.74) en 2016-2025, brutos y en USD.
11. **Portafolio: R = 12%, σ = 18%, β = 1.2, r_f = 4%, R_M = 10%, σ_M = 15%. Calcula Sharpe, Treynor, Jensen y M².** Sharpe 0.444 (mercado 0.40). Treynor 6.67 (mercado 6.0). α = +0.8%. M² = 10.67%.
12. **¿Cuántos años hacen falta para que un IR de 0.5 sea significativo con t = 3?** T = (3/0.5)² = 36 años.
13. **¿Qué predice Berk-Green sobre la persistencia y qué encuentran Choi-Zhao?** Los flujos eliminan el alfa neto aunque haya habilidad, así que no hay persistencia. Choi-Zhao replican la persistencia de Carhart en 1963-93, pero esta desaparece en 1994-2018.
14. **¿Por qué el BAB de Frazzini-Pedersen no se implementa tal cual en el sistema?** Requiere apalancamiento (bruto máximo de 1.0 en fase 1) y cortos. Su construcción es casi equiponderada y cargada a microcaps (US$1.05 por dólar en el 1% más pequeño). Neto, su alfa se explica por profitability e investment.
15. **¿Por qué no se cubre por defecto el USD en la renta variable de EUA para un inversionista en MXN?** La correlación entre el mercado de EUA y USD/MXN es de −0.4 a −0.5, porque el peso cae en las crisis. En oct-2008 la caída fue de −17.1% en USD y solo −4.0% en MXN. Cubrir aumentaría el drawdown en MXN.

---

## 9. Fuentes

1. Markowitz (1952) — https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1952.tb01525.x
2. Tobin (1958) — https://academic.oup.com/restud/article-abstract/25/2/65/1550009
3. Sharpe (1964) — https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1964.tb02865.x
4. Lintner (1965) — https://www.semanticscholar.org/paper/THE-VALUATION-OF-RISK-ASSETS-AND-THE-SELECTION-OF-Lintner/b3799991fae921c15d053ec2a693bfd0472f61d3
5. Mossin (1966) — https://www.econometricsociety.org/publications/econometrica/1966/10/01/equilibrium-capital-asset-market
6. Treynor (1965) — https://onlinelibrary.wiley.com/doi/10.1002/9781119196679.ch10
7. Sharpe (1966) — https://ideas.repec.org/a/ucp/jnlbus/v39y1965p119.html
8. Jensen (1968) — https://onlinelibrary.wiley.com/doi/full/10.1111/j.1540-6261.1968.tb00815.x
9. Fama (1970) — https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1970.tb00518.x
10. Black (1972) — https://ideas.repec.org/a/ucp/jnlbus/v45y1972i3p444-55.html
11. Black, Jensen, Scholes (1972) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=908569
12. Fama, MacBeth (1973) — https://ideas.repec.org/a/ucp/jpolec/v81y1973i3p607-36.html
13. Merton (1973) — https://www.econometricsociety.org/publications/econometrica/1973/09/01/intertemporal-capital-asset-pricing-model
14. Ross (1976) — https://www.sciencedirect.com/science/article/abs/pii/0022053176900466
15. Roll (1977) — https://ideas.repec.org/a/eee/jfinec/v4y1977i2p129-176.html
16. Basu (1977) — https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1977.tb01979.x
17. Grossman, Stiglitz (1980) — https://www.aeaweb.org/aer/top20/70.3.393-408.pdf
18. Banz (1981) — https://ideas.repec.org/a/eee/jfinec/v9y1981i1p3-18.html
19. Grinold (1989) — https://scispace.com/papers/the-fundamental-law-of-active-management-3sgb3bdt9p
20. Fama, French (1992) — https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1992.tb04398.x
21. Black, Litterman (1992) — https://www.tandfonline.com/doi/abs/10.2469/faj.v48.n5.28
22. Fama, French (1993) — https://www.sciencedirect.com/science/article/abs/pii/0304405X93900235
23. Jegadeesh, Titman (1993) — https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1993.tb04702.x
24. Lakonishok, Shleifer, Vishny (1994) — https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1994.tb04772.x
25. Carhart (1997) — https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1997.tb03808.x
26. Jegadeesh, Titman (2001) — https://www.nber.org/papers/w7159
27. Berk, Green (2004) — https://www.journals.uchicago.edu/doi/abs/10.1086/424739
28. Fama, French (2004) — https://www.aeaweb.org/articles?id=10.1257%2F0895330042162430
29. Ledoit, Wolf (2004) — http://www.ledoit.net/honey.pdf
30. Ang, Hodrick, Xing, Zhang (2006) — https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.2006.00836.x
31. DeMiguel, Garlappi, Uppal (2009) — https://academic.oup.com/rfs/article-abstract/22/5/1915/1592901
32. Cremers, Petajisto (2009) — https://academic.oup.com/rfs/article-abstract/22/9/3329/1574080
33. Barras, Scaillet, Wermers (2010) — https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2009.01527.x
34. Fama, French (2010) — https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2010.01598.x
35. Baker, Bradley, Wurgler (2011) — https://pages.stern.nyu.edu/~jwurgler/papers/faj-benchmarks.pdf
36. Novy-Marx (2013) — https://www.sciencedirect.com/science/article/abs/pii/S0304405X13000044
37. Asness, Moskowitz, Pedersen (2013) — https://onlinelibrary.wiley.com/doi/10.1111/jofi.12021 ; resumen CFA: https://rpc.cfainstitute.org/research/cfa-digest/2013/11/value-and-momentum-everywhere-digest-summary
38. Frazzini, Pedersen (2014) — https://pages.stern.nyu.edu/~lpederse/papers/BettingAgainstBeta.pdf
39. Fama, French (2015) — https://www.sciencedirect.com/science/article/abs/pii/S0304405X14002323
40. Hou, Xue, Zhang (2015) — https://academic.oup.com/rfs/article-abstract/28/3/650/1574802
41. Harvey, Liu, Zhu (2016) — https://academic.oup.com/rfs/article/29/1/5/1843824
42. McLean, Pontiff (2016) — https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12365
43. Novy-Marx, Velikov (2016) — https://academic.oup.com/rfs/article-abstract/29/1/104/1844518
44. Daniel, Moskowitz (2016) — https://www.sciencedirect.com/science/article/pii/S0304405X16301490
45. Stambaugh, Yuan (2017) — https://academic.oup.com/rfs/article/30/4/1270/2965095
46. Moreira, Muir (2017) — https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12513
47. Fama, French (2018) — https://www.sciencedirect.com/science/article/abs/pii/S0304405X18300515
48. Asness, Frazzini, Israel, Moskowitz, Pedersen (2018) — https://econpapers.repec.org/RePEc:eee:jfinec:v:129:y:2018:i:3:p:479-509
49. Alquist, Israel, Moskowitz (2018) — https://jpm.pm-research.com/content/early/2018/10/05/jpm.2018.1.082
50. Asness, Frazzini, Pedersen (2019) — https://link.springer.com/article/10.1007/s11142-018-9470-2
51. Hou, Xue, Zhang (2020) — https://academic.oup.com/rfs/article-abstract/33/5/2019/5236964
52. Cederburg, O'Doherty, Wang, Yan (2020) — https://www.sciencedirect.com/science/article/abs/pii/S0304405X2030132X
53. Feng, Giglio, Xiu (2020) — https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12883
54. Gu, Kelly, Xiu (2020) — https://academic.oup.com/rfs/article/33/5/2223/5758276
55. Choi, Zhao (2020) — https://www.nber.org/papers/w26707
56. Fama, French (2021) — https://academic.oup.com/raps/article-abstract/11/1/105/6033665
57. Arnott, Harvey, Kalesnik, Linnainmaa (2021) — https://www.tandfonline.com/doi/full/10.1080/0015198X.2020.1842704
58. Baltussen, Swinkels, van Vliet (2021) — https://www.sciencedirect.com/science/article/pii/S0304405X21003007
59. Hou, Mo, Xue, Zhang (2021) — https://academic.oup.com/rof/article-abstract/25/1/1/5727769
60. Ilmanen, Israel, Moskowitz, Thapar, Lee (2021) — https://joim.com/how-do-factor-premia-vary-over-time-a-century-of-evidence/
61. Ehsani, Linnainmaa (2022) — https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.13131
62. Harvey, Liu (2022) — https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.13123
63. Chen, Zimmermann (2022) — https://www.openassetpricing.com/
64. Novy-Marx, Velikov (2022) — https://www.sciencedirect.com/science/article/abs/pii/S0304405X21002051
65. Jensen, Kelly, Pedersen (2023) — https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.13249 ; https://www.nber.org/papers/w28432
66. Chen, Velikov (2023) — https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/zeroing-in-on-the-expected-returns-of-anomalies/945133D5A3ECEEAF466AEE91551FD225
67. Detzel, Novy-Marx, Velikov (2023) — https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.13225
68. Bryzgalova, Huang, Julliard (2023) — https://onlinelibrary.wiley.com/doi/10.1111/jofi.13197
69. Fama, French (2023), Production of U.S. Rm-Rf, SMB, and HML — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4629613
70. Kelly, Malamud, Zhou (2024) — https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.13298
71. Jensen, Kelly, Malamud, Pedersen (2026) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4187217 ; https://research.cbs.dk/en/publications/machine-learning-and-the-implementable-efficient-frontier-2/
72. Chen, Lopez-Lira, Zimmermann (2025) — https://arxiv.org/abs/2212.10317
73. Dickerson, Julliard, Mueller (2026) — https://www.sciencedirect.com/science/article/pii/S0304405X26000668 ; https://arxiv.org/abs/2604.04430
74. Guo, Huang, Li, Yu (2026) — https://arxiv.org/abs/2608.23761
75. van Vliet, Baltussen, Dom, Vidojevic (2025) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5561720
76. Kenneth R. French Data Library (datos a jul-2026) — https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html ; países emergentes: http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_5emerging.html
77. FRED, DEXMXUS (USD/MXN diario) — https://fred.stlouisfed.org/series/DEXMXUS
78. SPIVA U.S. Year-End 2025 — https://www.spglobal.com/spdji/en/spiva/article/spiva-us/ ; resumen: https://www.investmentnews.com/equities/active-managers-stumble-again-in-2025-as-large-caps-dominate/265541
79. SPIVA Latin America Year-End 2025 — https://www.spglobal.com/spdji/en/documents/spiva/spiva-latin-america-year-end-2025.pdf
80. Morningstar US Active/Passive Barometer Year-End 2025 — https://www.morningstar.com/business/insights/research/active-passive-barometer
81. Morningstar Factor Monitor Q1 2025 — https://indexes.morningstar.com/insights/markets-review/bltd9a242a7280e6745/morningstar-factor-monitor-q1-2025
82. CFA Institute, Level III exam — https://www.cfainstitute.org/programs/cfa-program/candidate-resources/level-iii-exam ; cambios 2026: https://300hours.com/cfa-curriculum-changes-2026/
83. Berk, van Binsbergen (2015) — https://www.sciencedirect.com/science/article/abs/pii/S0304405X15000628
