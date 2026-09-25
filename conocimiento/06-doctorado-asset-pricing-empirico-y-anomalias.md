# Módulo 06 — Asset pricing empírico avanzado y anomalías: del SDF al zoológico de factores y a lo que sobrevive neto

> Nivel: doctorado · Actualizado: 2026-09-25 · Grado de evidencia global: **B**. La teoría es exacta: SDF, cota de Hansen-Jagannathan e identidad de Campbell-Shiller. Que las primas históricas existen y replican en bruto es grado A (Chen-Zimmermann, Jensen-Kelly-Pedersen). Lo que un minorista puede cobrar en GBM, neto de costos, después de publicarse y solo en largo, es grado **C**. La anomalía promedio rinde 4 pb/mes neta (Chen-Velikov 2023), y en la réplica interna V03 ninguna pierna long-only de EUA tuvo apoyo estadístico desde 2000.

**Método de verificación de esta versión.** El presupuesto de WebSearch de la sesión estaba agotado (200/200). Las citas se confirmaron consultando directamente la API de Crossref (metadatos y resúmenes), las páginas y PDFs de NBER, IDEAS/RePEc, arXiv, los PDFs de los autores (Stern, Harvard, Yale), AQR, openassetpricing.com, jkpfactors.com y la Fed (FEDS). Lo que no se pudo confirmar se marca "(no verificado)". Las cifras propias salen de `laboratorio/replicas/C06-predictibilidad-y-momentum/reproducir.py`. Es un cálculo **exploratorio, sin pre-registro**, con datos congelados y huellas en `SHA256SUMS.txt`.

---

## 1. Objetivos de dominio (qué debe saber hacer quien "se titula" en este módulo)

1. Escribir todo modelo de valuación como E[m·R] = 1, derivar de ahí la representación beta, la tasa libre de riesgo y la equivalencia "factor lineal ⇔ SDF lineal", y explicar por qué el Sharpe máximo alcanzable es σ(m)/E(m).
2. Calcular la cota de Hansen-Jagannathan con datos y mostrar con números por qué el consumo CRRA no la cumple (equity premium puzzle y risk-free rate puzzle).
3. Explicar los mecanismos de hábito, riesgo de largo plazo y desastres raros, qué predice cada uno y qué dato los pone en aprietos.
4. Derivar la descomposición de Campbell-Shiller y el argumento de Cochrane de que casi toda la variación de P/D es tasa de descuento. Correr una regresión predictiva, medir el R² fuera de muestra (Goyal-Welch) y traducirlo a valor económico (Campbell-Thompson: R²/S²).
5. Dominar la crisis de replicación: pruebas múltiples (t > 3), microcaps, decaimiento post-publicación, sesgo de publicación, replicación bayesiana. Reconciliar HXZ (65% falla) con JKP (≈85% replica) con cifras.
6. Conocer los métodos de alta dimensión (Kozak-Nagel-Santosh, Feng-Giglio-Xiu, Bryzgalova-Huang-Julliard, IPCA, ML) y sus críticas recientes (Nagel 2025).
7. Separar momentum de sección cruzada, de series de tiempo y de factores. Saber cuándo se estrella el momentum y cuánto.
8. Evaluar BAB, carry, intermediary asset pricing y demand-system asset pricing: qué es señal operable y qué es teoría de precios.
9. Calcular costos de implementación y decidir si una anomalía sobrevive neta, en largo solamente, en pesos y en GBM.
10. Convertir lo anterior en reglas del sistema coherentes con `config/parametros.json`.

---

## 2. Núcleo teórico

### 2.1 El SDF: una sola ecuación

Todo precio cumple p_t = E_t[m_{t+1} x_{t+1}]. Para rendimientos brutos, **E[m R] = 1**. Para excesos, **E[m R^e] = 0**. De ahí salen cuatro resultados:

- **Tasa libre de riesgo:** R_f = 1/E[m].
- **Prima de riesgo:** E[R^e] = −R_f · Cov(m, R^e). Un activo paga prima si rinde poco justo cuando m es alto, es decir, en "malos tiempos" (alta utilidad marginal).
- **Representación beta:** E[R^e_i] = β_{i,m} · λ_m, con λ_m = −Var(m)/E(m).
- **Modelo de factores ⇔ SDF lineal:** m = a − b'f equivale a E[R^e_i] = β_i'λ. CAPM, FF3, FF5 y q son supuestos sobre qué f entra en m.

En el modelo de consumo con utilidad CRRA, m_{t+1} = β (C_{t+1}/C_t)^{−γ}. Con lognormalidad, la prima es aproximadamente γ · Cov(Δc, r).

### 2.2 Cota de Hansen-Jagannathan (1991)

Como E[m R^e] = 0, y por Cauchy-Schwarz:

  **σ(m)/E(m) ≥ |E(R^e)| / σ(R^e) = Sharpe de cualquier activo**.

Por lo tanto, la volatilidad del SDF acota el Sharpe de *todo* portafolio. El Sharpe máximo del mercado es σ(m)/E(m) (el portafolio tangente lo alcanza si está en el span).

**Cálculo con datos.** Campbell-Thompson reportan para acciones de EUA desde 1871 un Sharpe mensual de 0.108, o **0.374 anual**. Con E(m) ≈ 1, la cota exige σ(m) ≥ 0.37 anual. Con CRRA, σ(m) ≈ γ·σ(Δc). Mehra-Prescott miden σ(Δc) = 3.6% en 1889-1978, así que γ ≥ 0.374/0.036 ≈ **10** (cálculo propio con cifras verificadas).

**Inferencia operable.** Si un backtest promete un Sharpe sostenido de 2 o más (por ejemplo, los "mosaicos" de Cong et al. 2026, con Sharpe ≈ 2 fuera de muestra), implica un SDF con σ(m) ≥ 2. Eso es casi arbitraje. O existen fricciones que impiden explotarlo (costos, capacidad, microcaps), o el número está inflado.

### 2.3 Equity premium puzzle (Mehra-Prescott 1985)

Datos de EUA de 1889 a 1978 (Mehra 2003, Tabla 4):

| Dato | Valor |
|---|---|
| R_f | 0.80% |
| E(R_e) | 6.98% |
| Prima | **6.18%** |
| σ del crecimiento del consumo | 3.6% |

Con γ = 10 y β = 0.99, el modelo da **R_f = 12.7%** y una prima de **1.4 pp**. Es decir, hacen falta γ enormes para la prima, y esos mismos γ disparan la tasa libre de riesgo (el risk-free rate puzzle). Actualización del mismo autor, en prima sobre el activo "relativamente libre de riesgo":

| Periodo | Prima |
|---|---|
| 1802-1998 | 4.1 pp |
| 1889-2000 | 6.9 pp |
| 1926-2000 | 8.0 pp |
| 1947-2000 | 7.8 pp |

### 2.4 Tres familias de soluciones

**Hábito (Campbell-Cochrane 1999).** m_{t+1} = β[(S_{t+1}/S_t)(C_{t+1}/C_t)]^{−γ}, donde S = (C − X)/C es el consumo por encima de un hábito externo que se mueve lento. La aversión efectiva es γ/S y se dispara en recesiones. Con consumo i.i.d. y R_f constante y baja, el modelo genera:

- precios procíclicos;
- predictibilidad de largo plazo por D/P;
- volatilidad contracíclica.

Según los autores, "los inversionistas temen a las acciones porque les va mal en recesiones", no por riesgo de crecimiento de largo plazo.

**Riesgo de largo plazo (Bansal-Yaron 2004).** Usa preferencias de Epstein-Zin (1989), que separan la aversión al riesgo (γ) de la elasticidad de sustitución intertemporal (ψ). Su especificación:

- Δc_{t+1} = μ + x_t + σ_t η_{t+1}
- x_{t+1} = ρ x_t + φ_e σ_t e_{t+1}, con ρ cercano a 1

El componente persistente x es pequeño y la volatilidad σ_t es estocástica. Las noticias sobre crecimiento futuro mueven mucho a m. Con eso el modelo explica la prima, la R_f baja, la volatilidad y la predictibilidad por D/P. La calibración típica es ψ ≈ 1.5 y γ ≈ 10 (no verificado en el texto primario).

**Inferencia:** el punto débil es que x_t casi no se detecta en los datos, y el modelo implica que P/D predice crecimiento, algo que Cochrane (2008) no encuentra en dividendos.

**Desastres raros (Rietz 1988; Barro 2006; Wachter 2013).** Una probabilidad pequeña de colapso del consumo explica la prima, la R_f baja y la volatilidad. La versión de trabajo de Barro (NBER w11310, 2005) calibra:

- p = 1% anual de una contracción de 50% del PIB per cápita (b = ln 2);
- σ del crecimiento = 0.072, contra 0.061 en el G7 entre 1890 y 2004.

Wachter hace variable la probabilidad del desastre. Eso genera la volatilidad del mercado y la predictibilidad de los excesos.

**Inferencia (peso problem):** cualquier backtest sin desastres en la muestra sobreestima el Sharpe de estrategias que venden cola (carry, venta de volatilidad, apalancamiento).

### 2.5 Predictibilidad del mercado

**Identidad de Campbell-Shiller (1988).** Linealizando r_{t+1} ≈ k + ρ p_{t+1} + (1−ρ) d_{t+1} − p_t e iterando:

  dp_t ≈ const + Σ_{j≥1} ρ^{j−1} (r_{t+j} − Δd_{t+j}).

Un D/P alto tiene que predecir rendimientos altos, o dividendos bajos, o una burbuja. Cochrane (2008) muestra que el crecimiento de dividendos **no** es predecible. Por la identidad, eso es evidencia más fuerte de predictibilidad de rendimientos que la regresión directa. Cochrane (2011) concluye: "toda la variación de P/D corresponde a variación de tasas de descuento".

**Regresión predictiva:** r_{t+1} = a + b·x_t + ε. Tiene dos problemas:

1. **Sesgo de Stambaugh (1999).** Si x es persistente y sus innovaciones se correlacionan con las de r, b está sesgado y los t-estadísticos se inflan.
2. **Inestabilidad.** El R² dentro de muestra no es el R² que se puede cobrar.

**Métrica de Goyal-Welch:** R²_OOS = 1 − Σ(r − r̂)²/Σ(r − r̄_t)², donde r̄_t es la media histórica disponible en t.

**Valor económico (Campbell-Thompson 2008).** La ganancia proporcional de un inversionista media-varianza es ≈ R²/S², donde S es el Sharpe del activo. En datos mensuales desde 1871, S² = 1.2%. Un R²_OOS de 0.25% (E/P) sube el rendimiento del portafolio 0.25/1.2 = **21%**: unos 3% al año con aversión 1, o 1% con aversión 3 (versión NBER w11468). **Un R² mensual diminuto puede valer dinero, pero solo si es estable fuera de muestra.**

**Cota de Martin (2017).** Da un piso a la prima del mercado a partir de opciones del índice. Es proporcional a la varianza riesgo-neutral, SVIX². En promedio vale ≈ 5% y pasó de 20% en el pico de 2008.

### 2.6 Sección cruzada y alta dimensión

- **Pruebas múltiples.** Harvey-Liu-Zhu (2016) piden **t > 3.0** a un factor nuevo. Harvey-Liu (2020) calibran errores tipo I y II con doble bootstrap y encuentran que los métodos actuales tienen poca potencia para detectar gestores buenos.
- **Replicación bayesiana (JKP 2023).** El alfa posterior queda entre 0 y el alfa OLS. Por eso un decaimiento post-publicación *atenuado* es lo que se espera de efectos reales, no prueba de falsedad. Con un prior jerárquico, muchos factores del mismo tema *refuerzan* la evidencia.
- **SDF con muchas características:**
  - **Kozak-Nagel-Santosh (2020):** encogen el SDF hacia los componentes principales de alta varianza. Un SDF de pocas características (FF4 o FF5) *no* resume la sección cruzada; pocos PCs sí.
  - **Feng-Giglio-Xiu (2020):** doble selección con LASSO. La mayoría de los factores nuevos es redundante; profitability sí aporta.
  - **Bryzgalova-Huang-Julliard (2023):** estiman 2.25 cuatrillones de modelos. Su BMA-SDF supera a los modelos existentes dentro y fuera de muestra.
  - **Kelly-Pruitt-Su (2019, IPCA):** las características son covarianzas que varían en el tiempo.
  - **Kelly-Moskowitz-Pruitt (2021):** momentum y reversal predicen betas futuras. Buena parte es compensación condicional por riesgo.
- **ML.** Gu-Kelly-Xiu (2020) encuentran que árboles y redes neuronales duplican en algunos casos el desempeño de las regresiones. Todos los métodos coinciden en las señales dominantes: variantes de momentum, liquidez y volatilidad.

### 2.7 Momentum de series de tiempo y tendencia

**Moskowitz-Ooi-Pedersen (2012).** La regla es r^{TSMOM}_{t+1} = sign(r_{t−12,t}) · (40%/σ_t) · r_{t+1}. Los resultados (verificados contra el PDF en la réplica interna R02):

- los 58 futuros tienen TSMOM positivo, y 52 son significativos al 5%;
- el portafolio diversificado tiene un Sharpe mayor a 1 bruto en 1985-2009;
- el intercepto mensual es de 1.58% (t = 7.99).

**Hurst-Ooi-Pedersen (2017)** extienden la muestra a 1880. Según AQR, la estrategia fue "consistentemente rentable" durante 110 años. Las cifras de 67 mercados, promedio positivo en cada década y buen desempeño en 8 de las 10 peores crisis de un 60/40 vienen del Cap. 14 (no reverificadas aquí).

**Crítica de Huang-Li-Wang-Zhou (2020).** Activo por activo casi no hay predictibilidad. El t del panel no supera los valores críticos del bootstrap, y la estrategia TSMOM rinde "virtualmente lo mismo" que una basada en la media histórica, que no requiere predictibilidad.

### 2.8 Momentum de factores

- **Ehsani-Linnainmaa (2022).** El factor promedio rinde **6 pb/mes tras un año de pérdidas y 51 pb tras un año positivo**. El momentum de acciones individuales es sobre todo el *timing* de otros factores.
- **Gupta-Kelly (2019).** En 65 factores globales, un portafolio TS de factor momentum tiene **Sharpe 0.84**.
- **Arnott-Kalesnik-Linnainmaa (2023).** El momentum *transversal* de factores subsume al momentum de industria, se concentra en los primeros factores de mayor eigenvalor y es distinto del momentum TS de factores.

### 2.9 Betting against beta y el debate de baja volatilidad

**El mecanismo (Frazzini-Pedersen 2014).** Los inversionistas que no pueden apalancarse sobrepagan la beta alta, y la SML queda plana. El factor es:

  BAB = (1/β_L)(r_L − r_f) − (1/β_H)(r_H − r_f).

En EUA, BAB tuvo **Sharpe 0.78 entre 1926 y marzo de 2012**, el doble que value y 40% más que momentum en el mismo periodo. En Treasuries, el Sharpe fue 0.81.

**Las críticas:**
- **Novy-Marx-Velikov (2022).** La construcción equipondera en la práctica: por cada dólar en BAB hay **US$1.05 en el 1% más pequeño del mercado**. Neto de costos gana, pero porque se inclina hacia profitability e investment. Además, sesgos predecibles del estimador de beta generan la evidencia a favor de la teoría.
- **Cederburg-O'Doherty (2016).** Con CAPM condicional, la anomalía desaparece.
- **Schneider-Wagner-Zechner (2020).** Controlando por coskewness, los alfas de BAB y de baja volatilidad dejan de ser significativos.
- **Liu-Stambaugh-Yuan (2018).** La anomalía viene de la correlación beta-IVOL entre acciones sobrevaluadas.

### 2.10 Crashes del momentum y gestión de volatilidad

**Daniel-Moskowitz (2016).** Los crashes son parcialmente predecibles: ocurren en "estados de pánico", después de caídas del mercado y con volatilidad alta, y coinciden con los rebotes. Dos episodios:

| Episodio | Mercado | Deciles perdedores | Deciles ganadores |
|---|---|---|---|
| Jul-ago 1932 | +82% | +232% | +32% |
| Mar-may 2009 | +26% | +163% | +8% |

Una estrategia dinámica, que usa pronósticos de media y varianza, **aproximadamente duplica** el alfa y el Sharpe.

**Barroso-Santa-Clara (2015).** Gestionar el riesgo del momentum casi elimina los crashes y casi duplica el Sharpe.

**Generalizar no funciona.** Moreira-Muir (2017) encuentran alfas en factores gestionados por volatilidad. Pero Cederburg-O'Doherty-Wang-Yan (2020) revisan **103 estrategias**: los portafolios gestionados por volatilidad no superan sistemáticamente a los originales, y en versiones fuera de muestra suelen dar menor Sharpe y menor equivalente cierto. **Excepciones confirmadas (adenda 2026-09-25, examen diagnóstico S4-08), verificadas contra el resumen del artículo:** "volatility management enhances the performance of **momentum (in particular), profitability, and BAB** strategies, but has not added value when used with the other six commonly used factors." https://www.sciencedirect.com/science/article/abs/pii/S0304405X2030132X ; https://ideas.repec.org/a/eee/jfinec/v138y2020i1p95-117.html **Inferencia:** el escalamiento por volatilidad se justifica en momentum (sobre todo), *profitability* y BAB, donde el crash o la reversión son más predecibles, y no como regla universal.

### 2.11 Carry

El rendimiento esperado se descompone en **carry** (lo que se gana si el precio no cambia) más la apreciación esperada. En futuros, C_t = (S_t − F_t)/F_t.

**Koijen-Moskowitz-Pedersen-Vrugt (2018).** El carry predice rendimientos, en sección cruzada y en series de tiempo, en acciones globales, bonos, divisas, materias primas, Treasuries, crédito y opciones. En la versión de julio de 2012, el Sharpe va de 0.6 a 0.9 dentro de cada clase y llega a 1.5 en el portafolio diversificado (bruto). Todas las clases pierden al mismo tiempo en **recesiones globales**. Para el peso mexicano, ver el Cap. 16.

### 2.12 Intermediary asset pricing

- **He-Krishnamurthy (2013).** El inversionista marginal es un intermediario con restricción de capital. Cuando esa restricción se activa, las primas suben de forma no lineal. Inyectar capital a los intermediarios es la política más efectiva.
- **Adrian-Etula-Muir (2014).** Un solo factor, choques al apalancamiento de los broker-dealers, valúa portafolios de tamaño, B/M, momentum y bonos con **R² de 77% y un error promedio de 1% anual**.
- **He-Kelly-Manela (2017).** Los choques al capital de los *primary dealers* tienen un precio de riesgo positivo y de magnitud similar en acciones, bonos soberanos y corporativos, derivados, materias primas y divisas. Su factor es procíclico, lo que implica apalancamiento contracíclico.
- **Haddad-Muir (JEL, 2026).** Revisan la evidencia: exceso de volatilidad, diferencias entre clases de activos, arbitrajes rotos y el papel de la política monetaria y regulatoria.

### 2.13 Demand-system asset pricing y mercados inelásticos

- **Koijen-Yogo (2019).** Demanda por características, heterogénea entre inversionistas, estimada con variables instrumentales y diseñada para ajustar las tenencias de instituciones y hogares.
- **Gabaix-Koijen (NBER w28967, 2021).** **US$1 de flujo al mercado accionario sube su valor en ≈ US$5.** Los precios los mueven flujos de instituciones con mandatos rígidos.
- **Haddad-Huebner-Loualiche (AER 2025).** La respuesta estratégica de otros inversionistas solo compensa **dos tercios** de un cambio de conducta. El auge pasivo hizo la demanda por acciones individuales **11% más inelástica**.
- **Koijen-Richmond-Yogo (REStud 2024).** La migración de activo a pasivo tuvo un impacto grande en precios y pequeño en la informatividad.
- **Críticas 2025-2026.** van Binsbergen-David-Opp (NBER w34528) muestran que los instrumentos usados violan condiciones necesarias: las elasticidades estimadas "no guardan relación" con las verdaderas y pueden tener el signo equivocado. He-Kondor-Li (w34450) encuentran que la pendiente medida es ≈ **40%** de la conceptual, lo que implica curvas de demanda más empinadas.

### 2.14 Costos de implementación

- **Novy-Marx-Velikov (2016).** Casi todas las anomalías con rotación mensual (un lado) menor a 50% conservan diferenciales netos significativos si se diseñan para mitigar costos. Pocas con más rotación lo logran. La mitigación simple más eficaz es el **buy/hold spread**: exigir más para entrar que para mantener.
- **Frazzini-Israel-Moskowitz.**
  - En 2012, con casi US$1 billón (10¹²) de operaciones reales de AQR (1998-2011, 19 mercados), encontraron costos "muchas veces menores" que los de la literatura. Size, value y momentum sobreviven a gran escala; short-term reversal no.
  - En 2018 ("Trading Costs"), con US$1.7 billones en 19 años y 21 mercados, los costos resultaron un orden de magnitud menores. Son datos institucionales, no de minorista.
- **Chen-Velikov (2023).** En 204 anomalías, neto de spreads efectivos, del efecto de publicación y de la era tecnológica, el retorno esperado es **4 pb/mes**. Las más fuertes dan como máximo 10 pb y las combinaciones, ≈ 20 pb.
- **Detzel-Novy-Marx-Velikov (2023).** Ignorar costos favorece a los modelos con factores caros. Con costos, FF5 tiene un Sharpe² significativamente mayor que el q-factor y que el modelo de seis factores de Barillas-Shanken.

---

## 3. Literatura canónica

| Autores | Año | Título | Revista | Hallazgo clave cuantificado | DOI / enlace | Grado |
|---|---|---|---|---|---|---|
| Mehra, Prescott | 1985 | The Equity Premium: A Puzzle | JME 15(2):145-161 | Prima de 6.18% (1889-1978). Con γ=10, el modelo da 1.4 pp y R_f 12.7% | 10.1016/0304-3932(85)90061-3 | A (hecho) |
| Rietz | 1988 | The Equity Risk Premium: A Solution | JME 22(1):117-131 | Desastres de baja probabilidad explican la prima | 10.1016/0304-3932(88)90172-9 | B |
| Campbell, Shiller | 1988 | The Dividend-Price Ratio and Expectations… | RFS 1(3):195-228 | Identidad log-lineal de dp | 10.1093/rfs/1.3.195 | A (identidad) |
| Campbell, Shiller | 1988 | Stock Prices, Earnings, and Expected Dividends | JF 43(3):661-676 | Utilidades promediadas como predictor (origen del CAPE) | 10.1111/j.1540-6261.1988.tb04598.x | B |
| Epstein, Zin | 1989 | Substitution, Risk Aversion… | Econometrica 57(4):937 | Separan γ de ψ | 10.2307/1913778 | A (método) |
| Hansen, Jagannathan | 1991 | Implications of Security Market Data… | JPE 99(2):225-262 | σ(m)/E(m) ≥ Sharpe | 10.1086/261749 | A (método) |
| Campbell, Shiller | 1998 | Valuation Ratios and the Long-Run Stock Market Outlook | JPM 24(2):11-26 | Razones de valuación y rendimiento de largo plazo | 10.3905/jpm.24.2.11 | B |
| Campbell, Cochrane | 1999 | By Force of Habit | JPE 107(2):205-251 | Hábito: prima contracíclica y predictibilidad con consumo i.i.d. | 10.1086/250059 | B |
| Stambaugh | 1999 | Predictive Regressions | JFE 54(3):375-421 | Sesgo con regresor persistente | 10.1016/s0304-405x(99)00041-0 | A (método) |
| Bansal, Yaron | 2004 | Risks for the Long Run | JF 59(4):1481-1509 | Crecimiento persistente + EZ explican prima, R_f y volatilidad | 10.1111/j.1540-6261.2004.00670.x | B/C |
| Barro | 2006 | Rare Disasters and Asset Markets in the 20th Century | QJE 121(3):823-866 | Borrador: p = 1%/año de caída de 50%; σ 0.072 vs 0.061 del G7 | 10.1162/qjec.121.3.823 | B/C |
| Welch, Goyal | 2008 | A Comprehensive Look at… Equity Premium Prediction | RFS 21(4):1455-1508 | Los predictores fallan dentro y fuera de muestra; no sirven para *timing* | 10.1093/rfs/hhm014 | A |
| Campbell, Thompson | 2008 | Predicting Excess Stock Returns Out of Sample | RFS 21(4):1509-1531 | Con restricciones, R²_OOS chico pero valioso: R²/S², E/P +21% | 10.1093/rfs/hhm055 | B |
| Cochrane | 2008 | The Dog That Did Not Bark | RFS 21(4):1533-1575 | Los dividendos no predecibles implican rendimientos predecibles | 10.1093/rfs/hhm046 | A |
| Cochrane | 2011 | Discount Rates (discurso presidencial de la AFA) | JF 66(4):1047-1108 | Casi toda la variación de P/D es tasa de descuento | 10.1111/j.1540-6261.2011.01671.x | A |
| Moskowitz, Ooi, Pedersen | 2012 | Time Series Momentum | JFE 104(2):228-250 | 58 instrumentos positivos (52 sig.), Sharpe > 1 bruto (1985-2009) | 10.1016/j.jfineco.2011.11.003 | B |
| Asness, Moskowitz, Pedersen | 2013 | Value and Momentum Everywhere | JF 68(3):929-985 | Value y momentum en 8 mercados, correlacionados negativamente | 10.1111/jofi.12021 | A/B |
| He, Krishnamurthy | 2013 | Intermediary Asset Pricing | AER 103(2):732-770 | Primas no lineales en crisis por capital escaso | 10.1257/aer.103.2.732 | B |
| Wachter | 2013 | Can Time-Varying Risk of Rare Disasters… | JF 68(3):987-1035 | La probabilidad variable de desastre da volatilidad y predictibilidad | 10.1111/jofi.12018 | B/C |
| Frazzini, Pedersen | 2014 | Betting Against Beta | JFE 111(1):1-25 | BAB EUA Sharpe 0.78 (1926-2012), 20 mercados | 10.1016/j.jfineco.2013.10.005 | C (disputa) |
| Adrian, Etula, Muir | 2014 | Financial Intermediaries and the Cross-Section… | JF 69(6):2557-2596 | Un factor de apalancamiento: R² 77%, error de 1%/año | 10.1111/jofi.12189 | B/C |
| Barroso, Santa-Clara | 2015 | Momentum Has Its Moments | JFE 116(1):111-120 | Gestionar el riesgo casi duplica el Sharpe | 10.1016/j.jfineco.2014.11.010 | B |
| Harvey, Liu, Zhu | 2016 | …and the Cross-Section of Expected Returns | RFS 29(1):5-68 | Vara de t > 3.0 | 10.1093/rfs/hhv059 | A (método) |
| McLean, Pontiff | 2016 | Does Academic Research Destroy… Predictability? | JF 71(1):5-32 | 97 predictores: −26% fuera de muestra y −58% después de publicarse | 10.1111/jofi.12365 | A |
| Novy-Marx, Velikov | 2016 | A Taxonomy of Anomalies and Their Trading Costs | RFS 29(1):104-147 | Rotación < 50%/mes suele sobrevivir; el buy/hold spread es la mejor mitigación | 10.1093/rfs/hhv063 | A |
| Daniel, Moskowitz | 2016 | Momentum Crashes | JFE 122(2):221-247 | Crashes en pánico. La estrategia dinámica duplica el Sharpe | 10.1016/j.jfineco.2015.12.002 | A (patrón) |
| Cederburg, O'Doherty | 2016 | Does It Pay to Bet Against Beta? | JF 71(2):737-774 | El CAPM condicional resuelve la anomalía de beta | 10.1111/jofi.12383 | B |
| Martin | 2017 | What Is the Expected Return on the Market? | QJE 132(1):367-433 | Piso SVIX ≈ 5% promedio, > 20% en 2008 | 10.1093/qje/qjw034 | B/C |
| Moreira, Muir | 2017 | Volatility-Managed Portfolios | JF 72(4):1611-1644 | Alfa por *timing* de volatilidad | 10.1111/jofi.12513 | C |
| He, Kelly, Manela | 2017 | Intermediary Asset Pricing: New Evidence… | JFE 126(1):1-35 | Precio del capital de dealers positivo en 7 clases | 10.1016/j.jfineco.2017.08.002 | B |
| Hurst, Ooi, Pedersen | 2017 | A Century of Evidence on Trend-Following | JPM 44(1):15-29 | Rentable 110 años desde 1880 (AQR) | 10.3905/jpm.2017.44.1.015 | B |
| Koijen, Moskowitz, Pedersen, Vrugt | 2018 | Carry | JFE 127(2):197-225 | Carry predice en 8 clases. Borrador 2012: Sharpe 0.6-0.9 por clase, 1.5 diversificado | 10.1016/j.jfineco.2017.11.002 | B |
| Liu, Stambaugh, Yuan | 2018 | Absolving Beta of Volatility's Effects | JFE 128(1):1-15 | La anomalía de beta es IVOL en sobrevaluadas | 10.1016/j.jfineco.2018.01.003 | B |
| Koijen, Yogo | 2019 | A Demand System Approach to Asset Pricing | JPE 127(4):1475-1515 | Demanda por características con IV | 10.1086/701683 | B |
| Gupta, Kelly | 2019 | Factor Momentum Everywhere | JPM 45(3):13-36 | 65 factores, TS factor momentum con Sharpe 0.84 | 10.3905/jpm.2019.45.3.013 | B/C |
| Kelly, Pruitt, Su | 2019 | Characteristics Are Covariances | JFE 134(3):501-524 | IPCA | 10.1016/j.jfineco.2019.05.001 | B |
| Hou, Xue, Zhang | 2020 | Replicating Anomalies | RFS 33(5):2019-2133 | 65% de 452 falla con \|t\| ≥ 1.96 y 82% con 2.78 | 10.1093/rfs/hhy131 | A |
| Feng, Giglio, Xiu | 2020 | Taming the Factor Zoo | JF 75(3):1327-1370 | La mayoría de los factores nuevos es redundante; profitability no | 10.1111/jofi.12883 | A (método) |
| Kozak, Nagel, Santosh | 2020 | Shrinking the Cross-Section | JFE 135(2):271-292 | Un SDF de pocas características no basta; pocos PCs sí | 10.1016/j.jfineco.2019.06.008 | B |
| Gu, Kelly, Xiu | 2020 | Empirical Asset Pricing via Machine Learning | RFS 33(5):2223-2273 | Árboles y redes neuronales duplican algunas estrategias | 10.1093/rfs/hhaa009 | B |
| Chen, Zimmermann | 2020 | Publication Bias and the Cross-Section… | RAPS 10(2):249-289 | Sesgo de publicación de −12.3%, menor que el decaimiento post-publicación | 10.1093/rapstu/raz011 | B |
| Jacobs, Müller | 2020 | Anomalies Across the Globe | JFE 135(1):213-230 | 241 anomalías en 39 mercados: solo EUA decae de forma confiable después de publicarse | 10.1016/j.jfineco.2019.06.004 | B |
| Huang, Li, Wang, Zhou | 2020 | Time Series Momentum: Is It There? | JFE 135(3):774-794 | TSMOM débil activo por activo, ≈ estrategia de media histórica | 10.1016/j.jfineco.2019.08.004 | B |
| Cederburg, O'Doherty, Wang, Yan | 2020 | On the Performance of Volatility-Managed Portfolios | JFE 138(1):95-117 | 103 estrategias: fuera de muestra no ganan | 10.1016/j.jfineco.2020.04.015 | A (crítica) |
| Schneider, Wagner, Zechner | 2020 | Low-Risk Anomalies? | JF 75(5):2673-2718 | La coskewness explica BAB y BAV | 10.1111/jofi.12910 | B |
| Harvey, Liu | 2020 | False (and Missed) Discoveries | JF 75(5):2503-2553 | Vara con FDR por doble bootstrap | 10.1111/jofi.12951 | A (método) |
| Baltussen, Swinkels, van Vliet | 2021 | Global Factor Premiums | JFE 142(3):1128-1154 | 24 primas, 1800-2016: poco decaimiento fuera de muestra | 10.1016/j.jfineco.2021.06.030 | B |
| Kelly, Moskowitz, Pruitt | 2021 | Understanding Momentum and Reversal | JFE 140(3):726-743 | Momentum ≈ riesgo condicional (IPCA) | 10.1016/j.jfineco.2020.06.024 | B |
| Gabaix, Koijen | 2021 | …The Inelastic Markets Hypothesis | NBER w28967 | US$1 de flujo → ≈ US$5 de valor | nber.org/papers/w28967 | C |
| Ehsani, Linnainmaa | 2022 | Factor Momentum and the Momentum Factor | JF 77(3):1877-1919 | 6 pb tras un año malo vs 51 pb tras uno bueno | 10.1111/jofi.13131 | B |
| Chen, Zimmermann | 2022 | Open Source Cross-Sectional Asset Pricing | CFR 11(2):207-264 | 319 características. 98% de 161 claramente significativas replica. Pendiente de 0.90 y R² de 83% | 10.1561/104.00000112 | A |
| Novy-Marx, Velikov | 2022 | Betting Against Betting Against Beta | JFE 143(1):80-106 | US$1.05 en el 1% más chico. Neto de costos se explica por profitability e investment | 10.1016/j.jfineco.2021.05.023 | A (crítica) |
| Dong, Li, Rapach, Zhou | 2022 | Anomalies and the Expected Market Return | JF 77(1):639-681 | 100 anomalías predicen el mercado fuera de muestra | 10.1111/jofi.13099 | C |

---

## 4. Lo más reciente 2023-2026

| Fecha | Trabajo | Qué aporta | Grado |
|---|---|---|---|
| ene-2023 (RFS 36(8)) | Arnott, Kalesnik, Linnainmaa, "Factor Momentum" | El momentum transversal de factores subsume al de industria y se concentra en los factores de mayor eigenvalor | B |
| 2023 (JF 78(1)) | Bryzgalova, Huang, Julliard, "Bayesian Solutions for the Factor Zoo" | 2.25 cuatrillones de modelos; el BMA-SDF supera a los modelos existentes | B (método) |
| abr-2023 (JF 78(3)) | Detzel, Novy-Marx, Velikov | Con costos, FF5 domina a q y a Barillas-Shanken | A (método) |
| 2023 (JFQA 58(3)) | Chen, Velikov, "Zeroing In…" | 204 anomalías: **4 pb/mes** netas en la era moderna | A |
| jun-2023 (JF 78(5)) | Jensen, Kelly, Pedersen | 153 factores, 13 temas, 93 países. Versión NBER: tasa de replicación de 35% (HXZ) → 56.9% en su muestra → 64.7% sin los nunca significativos → **84.9%** con alfas CAPM. Alfa promedio de 0.45%/mes dentro de muestra y 0.31% fuera | A (bruto) |
| jun-2023 (JF 78(5), **versión publicada**) | Jensen, Kelly, Pedersen | **Adenda 2026-09-25 (examen diagnóstico S3-06).** La escalera de la Figura 1 de la versión publicada en el JF (distinta de la NBER 2021 de arriba) es: **35%** (HXZ) → **55.6%** (muestra más larga, holding de 1 mes en vez de 1/6/12, VW topada al percentil 80 NYSE, breakpoints de no-microcaps, 15 factores adicionales) → **61.3%** (excluye 34 factores que el original nunca encontró significativos) → **82.4%** (alfa CAPM en vez de rendimiento crudo) → **75.6%** (corrección Benjamini-Yekutieli; la analogía de HXZ baja de 35% a 18% con esta corrección) → **82.4%** (modelo bayesiano jerárquico con prior de alfa cero) → **82.4% global** (93 países ponderados por capitalización). FDR posterior en EUA: **0.1%** [IC 0.0%-1.0%]; fracción esperada de factores verdaderos: **94%**. https://research-api.cbs.dk/ws/portalfiles/portal/95651880/theis_ingerslev_jensen_et_al_is_there_a_replication_crisis_in_finance_publishersversion.pdf | A (bruto) |
| 2023 (SSRN 4586652) | Dick-Nielsen, Feldhütter, Pedersen, Stolborg | En bonos corporativos, la literatura de factores tiene "fallas de replicación"; solo una minoría de factores es robusta | B |
| ene-2024 (JF 79(1)) | Kelly, Malamud, Zhou, "The Virtue of Complexity" | Modelos con más parámetros que observaciones predicen mejor el mercado | C |
| 2024 (REStud 91(4)) | Koijen, Richmond, Yogo | El paso de activo a pasivo movió mucho los precios y poco la informatividad | B |
| sep-2024 (RFS 37(11)) | Goyal, Welch, Zafirov | 29 predictores nuevos + 17 originales con datos a 2021: **más de un tercio** ya no es significativo ni dentro de muestra, y **la mitad** de los restantes falla fuera. En la presentación de 2023: "las variables anuales tendieron a predecir mejor"; el SVIX de Martin "no predice ni dentro de muestra" con significancia; y Welch dice "2023: no sé qué puedo recomendar con confianza" | A |
| ene-2025 (NBER w33351) | Kelly, Kuznetsov, Malamud, Xu, "AI Asset Pricing Models" | Transformer dentro del SDF: "grandes reducciones" de errores de valuación frente a ML previo | C (sin historial) |
| mar-2025 (AER 115(3)) | Haddad, Huebner, Loualiche | La respuesta estratégica compensa 2/3 del cambio; el pasivo volvió la demanda 11% más inelástica | B |
| ago-2025 (NBER w34104) | Nagel, "Seemingly Virtuous Complexity" | Con P ≫ T y ventanas cortas, el RFF de KMZ se reduce a **momentum ajustado por volatilidad**. Con datos artificiales de reversión, falla | A (crítica) |
| 2025 (ARFE) | Haddad, Muir, "Market Macrostructure" | El pasivo, las compras de bancos centrales y los intermediarios apalancados mueven precios | B |
| oct-2025 | Open Source Asset Pricing, nueva versión | Señales traducidas a Python | Dato |
| nov/dic-2025 (NBER w34450, w34528) | He-Kondor-Li; van Binsbergen-David-Opp | Las elasticidades de demand-system están mal identificadas: pendiente ≈ 40% de la real, instrumentos inválidos | A (crítica) |
| dic-2025 (arXiv 2212.10317 v7) | Chen, Lopez-Lira, Zimmermann | Minar 29,000 razones contables con t > 2 iguala a la revisión por pares: queda **≈ 50%** de la predictibilidad después de la muestra | B |
| feb-2026 (NBER w34814) | Gormsen, Lazarus | Solo el "descuento puro" pasa 1 a 1 a valuaciones. Explica 80% de los cambios entre países desde 1990; en EUA, 35% de la baja de tasas | B |
| mar-2026 (RFS 39(10)) | Jensen, Kelly, Malamud, Pedersen | Frontera eficiente *implementable*: el ML que ignora costos sobrepondera características efímeras de baja capitalización | A (método) |
| abr-2026 | jkpfactors.com | Datos globales actualizados a dic-2025 | Dato |
| may-2026 (NBER w35158) | Cong, Feng, He, Wang, "Mosaics of Predictability" | Panel Tree: Sharpe fuera de muestra ≈ 2 | D hasta replicar (viola la intuición de HJ, §2.2) |
| 2026 (JEL 64(3)) | Haddad, Muir, "Intermediaries and Asset Prices" | Revisión del enfoque de intermediarios | B |
| jul-2026 (NBER w35413) | Haddad, He, Huebner, Kondor, Loualiche | Qué identifican los experimentos naturales en demanda de activos | B (método) |
| jul-2026 (NBER w35431) | Koijen, Levy | Benchmark en tiempo real para IA agéntica: R² en anuncios de resultados de 8% → ≈ 20% | C |
| jul-2026 (French, CRSP 202607) | Dato propio | UMD **−12.2%** en julio de 2026, 15° peor mes desde mediados de 1928, **fuera** del estado bear | Hecho |

---

## 5. Evidencia real: qué funciona, qué no, magnitudes netas y decaimiento

### 5.1 Replicación y decaimiento: las cifras compatibles

| Hecho | Cifra | Fuente |
|---|---|---|
| Caída fuera de muestra | −26% | McLean-Pontiff (97 predictores de EUA) |
| Caída después de publicarse | −58% (32 pp atribuibles a la publicación) | McLean-Pontiff |
| Anomalías que fallan (VW, microcaps controladas) | 65% con 1.96 y 82% con 2.78; 96% de las de fricciones | HXZ 2020 |
| Reproducción original | 98% de las 161 claramente significativas | Chen-Zimmermann 2022 |
| Replicación con alfas y método robusto | 84.9% (EUA, NBER) | JKP 2023 |
| Alfa dentro → fuera de muestra | 0.45 → 0.31 %/mes (−31%) | JKP 2023 |
| Sesgo de publicación estimado | −12.3% (EE 1.7 pp) | Chen-Zimmermann 2020 |
| Minado de 29,000 razones vs revisión por pares | ≈ 50% sobrevive en ambos | CLLZ 2025 |
| Fuera de EUA | Solo EUA decae de forma confiable (39 mercados) | Jacobs-Müller 2020 |
| 1800-2016, 24 primas globales | Poco decaimiento fuera de muestra | Baltussen et al. 2021 |

**Reconciliación.** No se contradicen:

- HXZ usan rendimientos brutos VW con cortes NYSE e incluyen factores que nunca fueron significativos y horizontes de 6 y 12 meses.
- JKP usan alfas, un ponderado VW con tope y solo 1 mes. La descomposición está en su Fig. 1.
- Las señales "fuertes" replican. Las débiles, las de microcaps y las de fricciones no.
- La caída post-publicación es de 30-60%, y es mayor para las señales con mayor rendimiento dentro de muestra y concentradas en acciones ilíquidas o de alto riesgo idiosincrático (McLean-Pontiff).

### 5.2 Neto de costos y para un minorista

- **Institucional:** 4 pb/mes en promedio y ≤ 10 pb las mejores (Chen-Velikov). Size, value y momentum sobreviven a gran escala con costos de AQR (FIM); short-term reversal no.
- **Minorista en GBM, solo largos (réplica interna V03, EUA):**
  - la pierna buena contra el mercado, VW, rinde entre **+0.8 y +2.1 pp/año desde 2000, sin significancia**;
  - después de publicarse, entre **+0.15 y +0.72 pp**;
  - en MXN, **0 de 15** pruebas tuvieron apoyo;
  - lo único robusto, emisión neta largo-corto equiponderada (10.7%/año, t 2.63), requiere cortos y microcaps. No es operable.
- **Momentum de EUA (V01, French):** 0.80%/mes (t 3.37) en 1984-2006 y **0.09%/mes (t 0.26)** en 2006-2025.

### 5.3 Predictibilidad del mercado: cifras propias (datos de Shiller a sep-2024)

| Prueba | Resultado |
|---|---|
| log D/P → mes siguiente, dentro de muestra (1871-2024) | R² = **0.09%** |
| Ídem, fuera de muestra desde 1927 / 1950 / 1990 | R²_OOS = **−0.35% / −0.22% / −1.04%** (con restricciones de Campbell-Thompson: −0.11% / −0.22% / −1.04%) |
| ln(CAPE) → rendimiento real a 10 años, dentro de muestra (inicios 1881-2014) | r10 = 25.6% − 6.94%·ln(CAPE), R² = 0.28 (observaciones traslapadas) |
| CAPE fuera de muestra, ventana expansiva, inicios 1950-2014 | R²_OOS = 0.18 en total. **Por subperiodo: 1950-69: +0.41; 1970-89: +0.32; 1990-2014: −0.32** (pronóstico medio 1.7% contra 6.65% realizado) |
| Sep-2014: CAPE 25.9 | Pronóstico dentro de muestra ≈ 3.0%; realizado **9.6% real anual** en 2014-2024 |
| CAPE en sep-2024 = 35.2 | Mapeo dentro de muestra ≈ 0.9% real anual con σ residual de 4.4 pp. **No se usa para operar** (§6) |

**Lectura.** La evidencia coincide con Welch-Goyal y GWZ 2024. El D/P mensual no gana a la media histórica fuera de muestra, ni con restricciones. El CAPE ordena bien los horizontes largos en la mitad de la historia, pero **falló por completo en la era 1990-2014**, que es la relevante para el presente. Además, con ~13 décadas independientes, el R² de 10 años tiene muy pocos grados de libertad efectivos. Grado B para "valuación alta → rendimiento de largo plazo menor en promedio" y D para *timing* táctico.

### 5.4 Momentum y crashes: cifras propias (French, CRSP 202607)

El estado bear se define como rendimiento acumulado del mercado de t−24 a t−1 menor a 0 (indicador de Daniel-Moskowitz). Cubre 16.2% de los meses desde mediados de 1928.

| UMD | n | Media %/mes | t NW(6) |
|---|---|---|---|
| Estado bear | 191 | **−0.78** | −1.29 |
| No bear | 986 | **+0.88** | 8.73 |
| No bear, 1927-1999 | 729 | +1.01 | 9.03 |
| No bear, 2000-2026 | 257 | +0.51 | 2.53 |
| Bear y el mercado sube en el mes (rebote, contemporáneo) | 105 | **−4.05** | −3.85 |

- **16 de los 20 peores meses** de UMD ocurrieron en estado bear: ago-1932 −52.6%, jul-1932 −45.6%, abr-2009 −34.4%, ene-2023 −16.2%, entre otros.
- Hubo excepciones que el filtro no atrapa: ene-2001 −25.4%, nov-2020 −12.6% y **jul-2026 −12.2%**.
- **Lectura:** el patrón de Daniel-Moskowitz se reproduce. Aun fuera del estado bear, la prima del momentum en EUA se redujo a la mitad después de 2000.

**TSMOM (réplica interna R02).**

| Muestra | Regla | Sharpe neto | t |
|---|---|---|---|
| EUA 1927-2011 | Regla del artículo | 0.33 | 2.97 |
| EUA 2012-2026 | Regla del artículo | 0.38 | 1.23 |
| 8 ETFs multiactivo 2012-2026 | Regla del artículo | **0.21** | 0.88 |
| EUA 1927-2011 | Solo largos a 12 meses | 0.51 | — |
| EUA 1927-2011 | Comprar y mantener | 0.39 | — |
| EUA 2012-2026 | Solo largos a 12 meses | 0.71 | — |
| EUA 2012-2026 | Comprar y mantener | 0.93 | — |

El MDD de la versión solo largos fue −45% contra −84% de comprar y mantener en 1927-2011, y casi igual en 2012-2026 (−24.5% contra −24.8%). Conclusión: **después de publicarse, la tendencia sirve como control de riesgo, no como fuente de rendimiento**.

### 5.5 Momentum de factores: cifras propias (SMB, HML, RMW, CMA, UMD)

| Periodo | Tras año + (pb/mes) | Tras año − (pb/mes) | Portafolio TS (pb/mes) | t |
|---|---|---|---|---|
| 1964-2026 | 45.2 | 7.7 | 26.4 | 4.32 |
| 1964-1999 | 53.8 | 2.6 | 35.9 | 4.84 |
| 2000-2026 | 32.0 | 13.0 | 13.8 | 1.43 |
| 2016-2026 | 17.1 | −5.8 | 11.6 | 0.80 |

La muestra completa reproduce la magnitud de Ehsani-Linnainmaa (51 vs 6). Después de 2000 el efecto persiste en signo, pero **ya no es significativo como estrategia**, porque todos los factores de EUA se debilitaron. Grado B como regla de desempate y C como estrategia independiente.

### 5.6 Resumen operativo por idea

| Idea | ¿Existe (bruto, histórico)? | ¿Sobrevive post-publicación? | ¿Neta y solo largos en GBM? | Uso en el sistema |
|---|---|---|---|---|
| Prima de mercado | A | A (con alta varianza) | Sí (ETF) | **Motor principal** del núcleo |
| *Timing* por valuación (D/P, CAPE) | B dentro de muestra | D fuera de muestra desde 1990 | No | Solo supuestos de largo plazo |
| TSMOM / tendencia | A (siglo) | C (Sharpe ≈ 0.2-0.4) | Como filtro | Control de riesgo y de apalancados |
| Momentum transversal | A | C en EUA (0.09%/mes) | Débil (ETF momentum) | Satélite chico con control de crash |
| Momentum de factores | A | C | Débil | Desempate entre ETFs de factores |
| Value, size, profitability, investment | A/B | B-C | Pierna larga ≈ 1 pp/año sin significancia | Inclinación del núcleo solo si el costo < 0.2%/año |
| BAB / baja volatilidad | C (disputa) | C | Solo baja vol sin apalancamiento | Reductor de drawdown, no alfa |
| Carry | B | B (crashes en recesión) | CETES vs T-bill | Ver Cap. 16 |
| Intermediarios / flujos | B (teoría y precio de riesgo) | — | No es señal directa | Bandera de régimen |
| Volatility management (general) | B dentro de muestra | C (103 estrategias) | — | Solo para momentum |
| ML complejo | B académico | C / D | Sin historial | Solo con línea base de momentum y vol |

---

## 6. Traducción operable (cómo lo usa el sistema para ganar)

**Estado actual.** Fase 0 (`prioridad_actual`): nada de esto se ejecuta con dinero real. Estas reglas gobiernan el laboratorio y el portafolio de papel, y se usarán en la arena y en el núcleo cuando el sistema salga de fase 0.

### 6.1 Reglas

1. **Vara estadística para señales propias.** Deben cumplir todo lo siguiente (de `validacion_estrategias`):
   - t ≥ 3.0 (Harvey-Liu-Zhu);
   - Sharpe deflactado ≥ 0.95 con el N de *todas* las variantes registradas;
   - PBO ≤ 0.25;
   - backtest ≥ 10 años con costos y slippage;
   - papel ≥ 3 meses y ≥ 30 operaciones.

   Si falla cualquiera, no pasa.
2. **Recorte obligatorio de prima.** μ_usable = 0.5 × μ_dentro_de_muestra para cualquier señal publicada o minada (CLLZ ≈ 50%; JKP −31%; McLean-Pontiff −58%). Para señales de EUA concentradas en microcaps o ilíquidas, el factor es 0.42 (1 − 0.58). Después se restan los costos de ida y vuelta en GBM. Si el resultado es ≤ 0, se descarta. Este μ_usable es el que entra en Kelly (≤ 0.25 en el perfil estándar y ≤ 0.5 en la arena).
3. **Solo cuenta la pierna larga.** En GBM no hay cortos, así que toda anomalía se evalúa como "quintil bueno − mercado, VW, neto". El diferencial largo-corto de un paper **no** es evidencia operable (V03).
4. **Prohibido el *timing* táctico por valuación.** D/P, CAPE, E/P, Fed model y SVIX no mueven el peso entre núcleo y satélite ni la exposición mensual. El CAPE solo alimenta el supuesto de rendimiento real a 10 años del núcleo, con banda de ±2σ (±8.8 pp). Evidencia: R²_OOS del D/P < 0; CAPE en 1990-2014 −0.32; GWZ 2024.
5. **Tendencia como control de riesgo.** Filtro solo-largos a 12 meses o media de 200 días sobre el subyacente para el satélite. Para los ETFs apalancados de la arena ya es obligatorio (`filtro_apalancados`: subyacente sobre su media de 200 días y VIX < 25). La expectativa registrada es **menor drawdown, no más rendimiento** (R02: Sharpe 0.71 contra 0.93 de comprar y mantener en 2012-2026).
6. **Control de crash de momentum (pre-registrar antes de usar).** Toda exposición a momentum (ETF de momentum, selección por rendimiento de 12-1 meses) se reduce 50% cuando el mercado viene de 24 meses con rendimiento acumulado negativo. La base es el cálculo C1: −0.78%/mes contra +0.88%, y 16 de los 20 peores meses en ese estado. Además, la exposición se escala a volatilidad objetivo (Barroso-Santa-Clara). **No** se extiende el escalamiento por volatilidad a otras estrategias sin validación propia (Cederburg et al. 2020).
7. **Momentum de factores solo como desempate.** Entre ETFs de factores equivalentes (value, quality, low vol, momentum, size) se prefiere el de rendimiento positivo en 12 meses. No se opera como estrategia independiente (2016-2026: t = 0.80).
8. **BAB / baja volatilidad sin apalancamiento.** Con `apalancamiento.bruto_max_fase_1` = 1.0, BAB no es implementable. La baja volatilidad long-only se clasifica como **reductor de drawdown** (V03: −36.5% contra −50.3% en USD y −17.0% contra −39.9% en MXN), con prima esperada ≈ 0.
9. **Presupuesto de rotación.** Ninguna estrategia satélite con rotación mensual (un lado) > 50% se acepta sin evidencia neta propia (Novy-Marx-Velikov). En la arena, además, `operaciones_max_mes` = 8. El rebalanceo por bandas (±5 pp absolutas o ±25% relativas) es el buy/hold spread del sistema.
10. **Bandera de estrés de intermediarios.** Si caen el capital de los primary dealers o el apalancamiento de los broker-dealers, suben los spreads de fondeo y el VIX pasa de 25, no se abre riesgo táctico nuevo. Esto es coherente con los cortacircuitos y con `filtro_apalancados`. **Inferencia:** después del pico de estrés el rendimiento esperado es alto (piso de Martin > 20% en 2008), pero el *timing* fuera de muestra es débil. Por eso se captura con **rebalanceo del núcleo por bandas**, no con apalancamiento táctico.
11. **Flujos e inelasticidad.** **Inferencia:** si US$1 mueve ≈ US$5 (Gabaix-Koijen) y la demanda es más inelástica por el pasivo (HHL, −11%), los flujos mecánicos grandes (rebalanceos de índices, entradas y salidas de ETFs) mueven precios a corto plazo. No se opera en contra de un flujo mecánico conocido y fechado, y se consulta el calendario de eventos del Cap. 15. Las elasticidades publicadas no se usan como parámetros: están mal identificadas (2025-2026).
12. **Líneas base obligatorias para ML o modelos "complejos"** de papers o rivales: (a) media histórica; (b) momentum ajustado por volatilidad (Nagel 2025); (c) comprar y mantener. Si no les gana neto, el modelo se descarta.
13. **Filtro HJ de credibilidad.** Todo backtest con Sharpe > 1.5 neto, en una sola clase de activo y con posiciones solo largas, se trata como error o sobreajuste hasta que se replique con datos propios. Precedentes: V01 a V03.
14. **Moneda.** Toda evidencia de EUA se re-evalúa en MXN con 1 + R_MXN = (1 + R_USD)(FX_1/FX_0) antes de usarse. En V03, ninguna anomalía long-only sobrevivió en MXN.

### 6.2 Checklist para aceptar una anomalía (todo "sí" o se rechaza)

- [ ] ¿Replica en Chen-Zimmermann y en JKP, fuera de microcaps y con ponderación VW o VW con tope?
- [ ] ¿Tiene t ≥ 3 en la muestra original y un signo consistente fuera de muestra *y* fuera de EUA?
- [ ] ¿Cuánto rinde después de publicarse? Anotar la fecha de publicación y comparar antes contra después.
- [ ] ¿Es positiva la pierna larga contra el mercado, neta de costos de GBM, en USD **y** en MXN?
- [ ] ¿Rotación < 50%/mes? ¿Existe un ETF líquido en el SIC o en la BMV que la capture con costo total < 0.2-0.3%/año?
- [ ] ¿Se aplicó el recorte de prima (regla 2) antes de dimensionar?
- [ ] ¿Se conoce el riesgo de cola (crash de momentum o carry en recesión) y hay regla escrita para él?
- [ ] ¿Está pre-registrada, con todas las variantes en el registro del Sharpe deflactado?
- [ ] ¿Cabe en los límites de `concentracion` y del satélite (≤ 30%)?

### 6.3 Dónde está la ventaja para competir

**Inferencia.**
- Los rivales con el mismo capital de MXN 20,000 no pueden cobrar anomalías de sección cruzada netas. La prima es de pocos puntos base y requiere cortos.
- La diferencia de TWR en 6 meses la dominarán (a) la exposición a beta y a tendencia, (b) evitar los crashes (momentum en rebotes, apalancados sin filtro) y (c) el manejo del torneo (`modo_torneo`).
- La ventaja de este módulo es **defensiva y de filtrado**: no pagar por anomalías muertas, no hacer *timing* con valuación, y cortar exposición en los estados donde la evidencia de crash es fuerte.

---

## 7. Trampas y errores comunes

1. **Tomar el diferencial largo-corto por lo que cobra un minorista.** El diferencial académico no descuenta costos, cortos ni el efecto de publicación.
2. **Usar R² dentro de muestra** o t de regresiones con regresores persistentes (sesgo de Stambaugh) como prueba de *timing*.
3. **Leer el CAPE como señal táctica.** En 1990-2014 su pronóstico medio fue de 1.7% real contra 6.65% realizado.
4. **Confundir "replica" con "es rentable hoy".** JKP replica en bruto, mientras que Chen-Velikov encuentran 4 pb netos. Las dos cosas son ciertas a la vez.
5. **Ignorar las pruebas múltiples.** Probar 20 variantes y reportar la mejor con t = 2.1 no vale nada. Hacen falta t ≥ 3 y el Sharpe deflactado con el N real.
6. **Ignorar la fecha de publicación.** El rendimiento anterior a la publicación no es fuera de muestra.
7. **Generalizar el volatility management.** Funciona en momentum (crash predecible), no en general (Cederburg et al.: 103 estrategias).
8. **Creer que BAB es "baja volatilidad".** BAB es apalancado, largo-corto y cargado a microcaps. La baja volatilidad long-only es otra cosa: menos drawdown, prima incierta.
9. **Tratar la tendencia como alfa asegurado.** Después de 2012 se debilitó (R02). Hay que esperar años malos, como el SG Trend Index con −15% en los 12 meses a jun-2025 (Cap. 14).
10. **Aceptar Sharpe ≈ 2 de ML o de "mosaicos".** La cota de HJ implica un SDF volátil casi imposible. Primero va la línea base de momentum ajustado por volatilidad (Nagel).
11. **Peso problem.** Un backtest de carry o de venta de volatilidad sin 2008, 1998 o ago-2024 sobreestima el Sharpe (Barro y Wachter).
12. **Asumir que la evidencia de EUA aplica a México.** Jacobs-Müller encuentran que el decaimiento post-publicación es fenómeno de EUA, y en MXN V03 no halló apoyo. No hay evidencia verificada en este capítulo de anomalías específicas de la BMV.
13. **Usar elasticidades de demand-system como parámetros.** Están mal identificadas (w34450, w34528).
14. **Comparar Sharpe de estimadores distintos.** Declarar siempre el tipo de error estándar (NW con rezagos, bootstrap) y si los datos están traslapados.

---

## 8. Examen de titulación

1. **Escribe la ecuación fundamental y deriva R_f y la prima de riesgo.** E[mR] = 1. De ahí R_f = 1/E(m) y E[R^e] = −R_f·Cov(m, R^e).
2. **Enuncia la cota de Hansen-Jagannathan y calcula el γ mínimo con CRRA si el Sharpe es 0.37 y σ(Δc) = 3.6%.** σ(m)/E(m) ≥ Sharpe. Como σ(m) ≈ γσ(Δc), γ ≥ 0.37/0.036 ≈ 10.
3. **¿Qué dicen los números de Mehra-Prescott y qué es el risk-free rate puzzle?** La prima observada fue de 6.18% (1889-1978). Con γ = 10 el modelo da 1.4 pp y una R_f de 12.7% contra 0.8% observada: los γ altos hacen la tasa libre de riesgo absurdamente alta.
4. **Mecanismo del hábito en una línea.** La aversión efectiva γ/S sube cuando el consumo se acerca al hábito, en recesiones. Eso da primas contracíclicas y predictibilidad con consumo i.i.d.
5. **¿Por qué Cochrane dice que el perro "no ladró"?** Por la identidad de Campbell-Shiller, si el D/P varía y no predice dividendos, tiene que predecir rendimientos. La ausencia de predictibilidad en dividendos es la evidencia más fuerte.
6. **Define R²_OOS y cómo lo traduce Campbell-Thompson a dinero.** R²_OOS = 1 − SSE_modelo/SSE_media_histórica. La ganancia proporcional es ≈ R²/S². Con S² mensual de 1.2% y R² de 0.25%, la ganancia es ≈ 21%.
7. **¿Qué encontraron Goyal-Welch-Zafirov (2024)?** Revisaron 29 predictores nuevos y 17 originales con datos a 2021. Más de un tercio ya no es significativo dentro de muestra, y la mitad de los que sí lo son falla fuera de muestra.
8. **Cifras exactas de McLean-Pontiff.** Revisan 97 predictores. El rendimiento cae 26% fuera de muestra y 58% después de publicarse; se atribuye 32% al aprendizaje por publicación.
9. **Reconcilia HXZ con JKP.** HXZ: 65% falla con rendimiento bruto VW, horizontes de 1, 6 y 12 meses, e incluyen factores nunca significativos. JKP: sube a 84.9% con alfa CAPM, VW con tope, un mes y sin esos factores. Las señales fuertes replican; las débiles y de microcaps no.
10. **¿Cuánto rinde neta la anomalía promedio hoy?** ≈ 4 pb/mes; las mejores, ≤ 10 pb (Chen-Velikov 2023, 204 anomalías).
11. **¿Cuándo se estrella el momentum y con qué magnitud?** En estados de pánico (mercado en caída con vol alta) y durante el rebote. En jul-ago 1932 los perdedores subieron 232% y los ganadores 32%. En el cálculo propio, UMD rinde −0.78%/mes en estado bear contra +0.88% fuera de él.
12. **Dos críticas publicadas a BAB, con cifra.** Novy-Marx-Velikov: US$1.05 por dólar en el 1% más chico; neto de costos se explica por profitability e investment. Schneider-Wagner-Zechner: controlando por coskewness, el alfa deja de ser significativo.
13. **¿Qué dicen Gabaix-Koijen y qué objeción recibió el enfoque en 2025?** US$1 de flujo sube ≈ US$5 el valor del mercado. He-Kondor-Li y van Binsbergen-David-Opp muestran que los instrumentos y la dinámica sesgan las elasticidades medidas: la pendiente es ≈ 40% de la real.
14. **¿Por qué el sistema no usa el CAPE para *timing*?** Su R² fuera de muestra fue −0.32 en 1990-2014, GWZ encuentran predictores inestables y la regla 4 lo prohíbe. Solo sirve como supuesto de largo plazo con banda amplia.
15. **¿Qué línea base debe superar un modelo ML de predicción del mercado, según Nagel (2025)?** Un momentum ajustado por volatilidad (y la media histórica). Con P ≫ T y ventanas cortas, el RFF se reduce a eso.

---

## 9. Fuentes

1. Mehra, Prescott (1985), JME — https://doi.org/10.1016/0304-3932(85)90061-3 ; Mehra (2003), "The Equity Premium: Why Is It a Puzzle?" — https://www.nber.org/papers/w9512
2. Rietz (1988), JME — https://doi.org/10.1016/0304-3932(88)90172-9
3. Campbell, Shiller (1988), RFS — https://doi.org/10.1093/rfs/1.3.195
4. Campbell, Shiller (1988), JF — https://doi.org/10.1111/j.1540-6261.1988.tb04598.x
5. Campbell, Shiller (1998), JPM — https://doi.org/10.3905/jpm.24.2.11
6. Epstein, Zin (1989), Econometrica — https://doi.org/10.2307/1913778
7. Hansen, Jagannathan (1991), JPE — https://doi.org/10.1086/261749 ; resumen: https://ideas.repec.org/a/ucp/jpolec/v99y1991i2p225-62.html
8. Campbell, Cochrane (1999), JPE — https://doi.org/10.1086/250059 ; https://www.nber.org/papers/w4995
9. Stambaugh (1999), JFE — https://doi.org/10.1016/s0304-405x(99)00041-0
10. Bansal, Yaron (2004), JF — https://doi.org/10.1111/j.1540-6261.2004.00670.x ; https://www.nber.org/papers/w8059
11. Barro (2006), QJE — https://doi.org/10.1162/qjec.121.3.823 ; borrador: https://www.nber.org/papers/w11310
12. Wachter (2013), JF — https://doi.org/10.1111/jofi.12018 ; https://www.nber.org/papers/w14386
13. Welch, Goyal (2008), RFS — https://doi.org/10.1093/rfs/hhm014 ; https://ideas.repec.org/a/oup/rfinst/v21y2008i4p1455-1508.html
14. Campbell, Thompson (2008), RFS — https://doi.org/10.1093/rfs/hhm055 ; PDF: https://www.nber.org/papers/w11468
15. Cochrane (2008), RFS — https://doi.org/10.1093/rfs/hhm046
16. Cochrane (2011), JF — https://doi.org/10.1111/j.1540-6261.2011.01671.x ; https://www.nber.org/papers/w16972
17. Goyal, Welch, Zafirov (2024), RFS 37(11):3490-3557 — https://doi.org/10.1093/rfs/hhae044 ; presentación: https://www.ivo-welch.info/research/presentations/99-stanford-prediction.pdf
18. Martin (2017), QJE — https://doi.org/10.1093/qje/qjw034
19. Harvey, Liu, Zhu (2016), RFS — https://doi.org/10.1093/rfs/hhv059 ; https://www.nber.org/papers/w20592
20. Harvey, Liu (2020), JF — https://doi.org/10.1111/jofi.12951
21. McLean, Pontiff (2016), JF — https://doi.org/10.1111/jofi.12365
22. Hou, Xue, Zhang (2020), RFS — https://doi.org/10.1093/rfs/hhy131
23. Chen, Zimmermann (2020), RAPS — https://doi.org/10.1093/rapstu/raz011
24. Chen, Zimmermann (2022), CFR — https://doi.org/10.1561/104.00000112 ; https://www.federalreserve.gov/econres/feds/open-source-cross-sectional-asset-pricing.htm ; https://www.openassetpricing.com/
25. Jensen, Kelly, Pedersen (2023), JF 78(5):2465-2518 — https://doi.org/10.1111/jofi.13249 ; https://www.nber.org/papers/w28432 ; https://jkpfactors.com/
26. Chen, Lopez-Lira, Zimmermann, "Does Peer-Reviewed Research Help Predict Stock Returns?" (v7, dic-2025) — https://arxiv.org/abs/2212.10317
27. Jacobs, Müller (2020), JFE — https://doi.org/10.1016/j.jfineco.2019.06.004
28. Baltussen, Swinkels, van Vliet (2021), JFE — https://doi.org/10.1016/j.jfineco.2021.06.030
29. Feng, Giglio, Xiu (2020), JF — https://doi.org/10.1111/jofi.12883 ; https://www.nber.org/papers/w25481
30. Kozak, Nagel, Santosh (2020), JFE — https://doi.org/10.1016/j.jfineco.2019.06.008
31. Bryzgalova, Huang, Julliard (2023), JF 78(1):487-557 — https://doi.org/10.1111/jofi.13197
32. Kelly, Pruitt, Su (2019), JFE — https://doi.org/10.1016/j.jfineco.2019.05.001
33. Kelly, Moskowitz, Pruitt (2021), JFE — https://doi.org/10.1016/j.jfineco.2020.06.024
34. Gu, Kelly, Xiu (2020), RFS — https://doi.org/10.1093/rfs/hhaa009
35. Kelly, Malamud, Zhou (2024), JF 79(1):459-503 — https://www.nber.org/papers/w30217
36. Nagel (2025), "Seemingly Virtuous Complexity in Return Prediction" — https://www.nber.org/papers/w34104
37. Moskowitz, Ooi, Pedersen (2012), JFE — https://doi.org/10.1016/j.jfineco.2011.11.003
38. Hurst, Ooi, Pedersen (2017), JPM — https://doi.org/10.3905/jpm.2017.44.1.015 ; https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing
39. Huang, Li, Wang, Zhou (2020), JFE — https://doi.org/10.1016/j.jfineco.2019.08.004
40. Ehsani, Linnainmaa (2022), JF — https://doi.org/10.1111/jofi.13131
41. Gupta, Kelly (2019), JPM — https://doi.org/10.3905/jpm.2019.45.3.013 (resumen vía Crossref, SSRN 3300728)
42. Arnott, Kalesnik, Linnainmaa (2023), RFS 36(8):3034-3070 — https://doi.org/10.1093/rfs/hhad006
43. Asness, Moskowitz, Pedersen (2013), JF — https://doi.org/10.1111/jofi.12021
44. Frazzini, Pedersen (2014), JFE — https://doi.org/10.1016/j.jfineco.2013.10.005 ; PDF: https://pages.stern.nyu.edu/~lpederse/papers/BettingAgainstBeta.pdf
45. Novy-Marx, Velikov (2022), JFE — https://doi.org/10.1016/j.jfineco.2021.05.023
46. Cederburg, O'Doherty (2016), JF — https://doi.org/10.1111/jofi.12383
47. Schneider, Wagner, Zechner (2020), JF — https://doi.org/10.1111/jofi.12910
48. Liu, Stambaugh, Yuan (2018), JFE — https://doi.org/10.1016/j.jfineco.2018.01.003
49. Daniel, Moskowitz (2016), JFE — https://doi.org/10.1016/j.jfineco.2015.12.002 ; PDF: https://www.nber.org/papers/w20439
50. Barroso, Santa-Clara (2015), JFE — https://doi.org/10.1016/j.jfineco.2014.11.010
51. Moreira, Muir (2017), JF — https://doi.org/10.1111/jofi.12513
52. Cederburg, O'Doherty, Wang, Yan (2020), JFE — https://doi.org/10.1016/j.jfineco.2020.04.015
53. Koijen, Moskowitz, Pedersen, Vrugt (2018), JFE — https://doi.org/10.1016/j.jfineco.2017.11.002 ; borrador jul-2012: https://pages.stern.nyu.edu/~lpederse/papers/Carry.pdf
54. He, Krishnamurthy (2013), AER — https://doi.org/10.1257/aer.103.2.732
55. Adrian, Etula, Muir (2014), JF — https://doi.org/10.1111/jofi.12189
56. He, Kelly, Manela (2017), JFE — https://doi.org/10.1016/j.jfineco.2017.08.002
57. Haddad, Muir, "Intermediaries and Asset Prices", JEL 64(3) (2026) — https://www.nber.org/papers/w34146 ; "Market Macrostructure", ARFE (2025) — https://www.nber.org/papers/w33434
58. Koijen, Yogo (2019), JPE — https://doi.org/10.1086/701683
59. Gabaix, Koijen (2021), NBER w28967 — https://www.nber.org/papers/w28967
60. Koijen, Richmond, Yogo (2024), REStud 91(4):2387-2424 — https://www.nber.org/papers/w27402
61. Haddad, Huebner, Loualiche (2025), AER 115(3):975-1018 — https://doi.org/10.1257/aer.20230505
62. He, Kondor, Li (2025), NBER w34450 — https://www.nber.org/papers/w34450 ; van Binsbergen, David, Opp (2025), NBER w34528 — https://www.nber.org/papers/w34528 ; Haddad et al. (2026), NBER w35413 — https://www.nber.org/papers/w35413
63. Novy-Marx, Velikov (2016), RFS — https://doi.org/10.1093/rfs/hhv063 ; https://www.nber.org/papers/w20721
64. Frazzini, Israel, Moskowitz, "Trading Costs of Asset Pricing Anomalies" (2012) — https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies ; "Trading Costs" (2018) — https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs
65. Chen, Velikov (2023), JFQA 58(3):968-1004 — https://doi.org/10.1017/s0022109022000874
66. Detzel, Novy-Marx, Velikov (2023), JF 78(3):1743-1775 — https://doi.org/10.1111/jofi.13225
67. Jensen, Kelly, Malamud, Pedersen (2026), RFS 39(10):3035-3078 — https://doi.org/10.1093/rfs/hhag022
68. Dong, Li, Rapach, Zhou (2022), JF — https://doi.org/10.1111/jofi.13099
69. Dick-Nielsen, Feldhütter, Pedersen, Stolborg (2023), "Corporate Bond Factors: Replication Failures and a New Framework" — https://doi.org/10.2139/ssrn.4586652
70. Kelly, Kuznetsov, Malamud, Xu (2025), NBER w33351 — https://www.nber.org/papers/w33351 ; Koijen, Levy (2026), NBER w35431 — https://www.nber.org/papers/w35431 ; Cong, Feng, He, Wang (2026), NBER w35158 — https://www.nber.org/papers/w35158 ; Gormsen, Lazarus (2026), NBER w34814 — https://www.nber.org/papers/w34814
71. Kenneth French Data Library (CRSP 202607) — https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html ; Shiller, ie_data.xls (datos a sep-2024) — http://www.econ.yale.edu/~shiller/data/ie_data.xls
72. Réplicas internas: `laboratorio/replicas/R02-momentum-series-de-tiempo.md`, `V01-momentum-y-rentabilidad/`, `V03-anomalias-long-only-eua/` y `C06-predictibilidad-y-momentum/` (esta última, exploratoria)

**No verificado en esta versión.**
- La calibración publicada de Barro 2006 (probabilidades y tamaños de desastre de la versión QJE): se usó el borrador de 2005.
- Los parámetros ψ ≈ 1.5 y γ ≈ 10 de Bansal-Yaron.
- Las cifras de 67 mercados, "cada década" y "8 de 10 crisis" de Hurst-Ooi-Pedersen (tomadas del Cap. 14).
- Los Sharpe de la versión publicada de "Carry" (2018): se usó el borrador de 2012.
- Las tasas de replicación de la versión publicada de JKP (se usó la versión NBER).
- La cifra de 316 factores de Harvey-Liu-Zhu.
- Los costos por operación de Novy-Marx-Velikov 2016.
- Si México forma parte de los 93 países de JKP y de los 39 de Jacobs-Müller.
- El estado de publicación de Gabaix-Koijen después de 2021.
