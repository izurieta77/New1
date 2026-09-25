# Módulo 05 — Derivados y volatilidad: futuros, opciones, prima de volatilidad y qué usos le sirven a un inversionista individual

> Nivel: maestría · Actualizado: 2026-09-25 · Grado de evidencia global: **B**. La teoría de no arbitraje (acarreo, paridad put-call, Black-Scholes-Merton) es exacta bajo sus supuestos. Que las opciones de índice han estado históricamente caras es un hecho de grado A (Coval-Shumway 2001; Bakshi-Kapadia 2003). Pero esa prima **se comprimió**: Dew-Becker y Giglio (2025) encuentran alfas de opciones de índice indistinguibles de cero en los últimos 15 años. En cambio, que casi todos los usos minoristas típicos destruyen valor (comprar opciones cortas, 0DTE, ETPs de VIX largos) es evidencia A.

---

## 1. Objetivos de dominio (qué debe saber hacer quien "se titula" en este módulo)

1. Valuar forwards y futuros por costo de acarreo (índice, divisa, commodity), calcular la base y descomponer el rendimiento de un futuro en cambio de spot más roll yield (carry). Explicar contango y backwardation y por qué el roll yield no es una "comisión" sino una prima o un costo esperado.
2. Dibujar el payoff y el P&L de calls, puts, spreads, straddles, collars, covered calls y put-writes. Usar la paridad put-call para detectar precios inconsistentes y sintetizar posiciones.
3. Derivar la intuición de Black-Scholes-Merton (réplica dinámica), calcular a mano precio y griegas de una opción ATM y explicar la identidad P&L ≈ ½·Γ·S²·(σ²_realizada − σ²_implícita)·dt.
4. Distinguir volatilidad implícita, realizada y esperada; explicar el smile/skew del S&P 500 después de 1987 y sus dos explicaciones (riesgo de salto y presión de demanda).
5. Medir la volatility risk premium (VRP) con variance swaps sintéticos (Carr-Wu 2009) y delta-hedged gains (Bakshi-Kapadia 2003). Saber cuánto vale hoy y por qué se comprimió.
6. Evaluar con números netos las estrategias con opciones: BXM, PUT, collars, puts protectores, tail hedging, ETPs de VIX, 0DTE y ETFs de "income".
7. Explicar la mecánica de la gamma de los dealers y lo que sí y no predice.
8. Conocer los derivados en México (MexDer: futuros del IPC, dólar, mini dólar, TIIE; Asigna; tratamiento fiscal del art. 129 y del art. 146 de la LISR) y el acceso real de una persona física con GBM.
9. Traducir todo a reglas del sistema coherentes con `config/parametros.json`: qué usos tienen ventaja y cuáles están prohibidos.

---

## 2. Núcleo teórico

### 2.1 Forwards y futuros: costo de acarreo, base y roll yield

**Payoff:** un forward largo paga S_T − F_0 al vencimiento. El futuro es lo mismo, pero estandarizado, con cámara de compensación (en México, Asigna) y liquidación diaria de pérdidas y ganancias (*mark-to-market*). Con tasas deterministas, forward y futuro valen lo mismo. Cuando las tasas son estocásticas y están correlacionadas con el subyacente, difieren un poco.

**No arbitraje (costo de acarreo):**
- Índice accionario con rendimiento por dividendo q: F = S·e^{(r − q)T}.
- Divisa (pesos por dólar): F = S·(1 + r_MXN·T)/(1 + r_USD·T).
- Commodity con costo de almacenaje u y *convenience yield* y: F = S·e^{(r + u − y)T}.

**Base:** base = S − F (algunos textos usan F − S). La base converge a cero al vencimiento. El riesgo de base es el que queda cuando se cubre con un futuro cuyo subyacente o vencimiento no coincide exactamente con la exposición.

**Contango y backwardation:** hay contango cuando F > S, o cuando la curva de futuros tiene pendiente positiva. Hay backwardation en el caso inverso.

**Descomposición del rendimiento (Koijen, Moskowitz, Pedersen y Vrugt, 2018):** rendimiento del futuro = carry + cambio esperado del precio. El carry se observa por adelantado: es el rendimiento que se obtiene si el spot no se mueve y el futuro "rueda" por la curva hacia el spot. En backwardation el carry es positivo (roll yield positivo). En contango es negativo.

**Ejemplos con datos verificados al 23-25 de septiembre de 2026:**
- **Futuro del dólar, 1 año.** Spot USD/MXN = 17.71 (Yahoo, 25-sep-2026). Tasa interbancaria a 3 meses de México = 6.79% (OCDE/FRED, ago-2026). T-bill de EUA a 3 meses = 4.04% (FRED DTB3, 23-sep-2026). F ≈ 17.71 × 1.0679/1.0404 = **18.18**. *Inferencia:* quien compra dólares a futuro para cubrirse paga ≈ **2.7% al año**. Quien los vende a futuro (el exportador) cobra ese diferencial. Esta es la misma prima de carry del peso.
- **Futuro del IPC, 3 meses.** IPC = 64,264 (Yahoo, 24-sep-2026). Con r = 6.79% y un supuesto de q = 3% (no verificado), F ≈ 64,264·e^{(0.0679 − 0.03)·0.25} = **64,876**. Tamaño del contrato de MexDer: $10 MXN × IPC, lo que da un nocional ≈ **MXN 642,640** por contrato, **32 veces** la cuenta arena de MXN 20,000.
- **Apalancamiento implícito:** con un margen inicial del m% del nocional, el apalancamiento es 1/m. Un movimiento adverso del IPC de 3% hace perder 3% × 642,640 = MXN 19,279 por contrato. En la cuenta arena eso es prácticamente todo el capital.

### 2.2 Opciones: payoffs y paridad put-call

- Call: max(S_T − K, 0). Put: max(K − S_T, 0). La prima es la pérdida máxima del comprador. La pérdida del vendedor descubierto es ilimitada con el call y llega hasta K con el put.
- **Paridad put-call (Stoll, 1969)** para opciones europeas: C − P = S·e^{−qT} − K·e^{−rT}. De ella salen tres equivalencias:
  - put-write colateralizado (vender put + tener K·e^{−rT} en T-bills) ≡ covered call (acción larga + call vendido) con el mismo strike;
  - put protector (acción + put) ≡ call + bono;
  - collar ≡ acción + put comprado + call vendido.
  **Inferencia:** el BXM y el PUT son, casi, la misma apuesta: beta accionaria reducida más venta de volatilidad. Sus diferencias históricas vienen de los detalles de implementación (strikes, fechas, colateral), no de una ventaja económica distinta.

### 2.3 Black-Scholes-Merton (1973)

Supuestos: log-precio con volatilidad σ constante, negociación continua sin costos, tasa r constante y posibilidad de vender en corto. Con una cartera de réplica (Δ acciones + bono) el riesgo se elimina, y el precio no depende del rendimiento esperado μ.

- C = S·e^{−qT}·N(d₁) − K·e^{−rT}·N(d₂) ; P = K·e^{−rT}·N(−d₂) − S·e^{−qT}·N(−d₁)
- d₁ = [ln(S/K) + (r − q + σ²/2)T]/(σ√T) ; d₂ = d₁ − σ√T

**Ejemplo (cálculo propio):** S = K = 100, T = 1 mes, r = 4%, q = 0, σ = 16%.
- Call = **2.01**, put = **1.68**. Su diferencia, 0.333, es igual a S − K·e^{−rT}, como exige la paridad.
- Δ_call = 0.538 ; Γ = 0.086 ; vega = 0.115 por punto de volatilidad ; θ_call = −0.036 por día.
- Regla rápida para una opción ATM: precio ≈ 0.4·σ·√T·S = 1.85.

**Griegas y P&L de una opción con cobertura delta.** Si la posición se cubre en delta, el P&L diario ≈ ½·Γ·S²·(σ²_realizada − σ²_implícita)·Δt. El comprador gana solo si la volatilidad realizada supera a la implícita que pagó. El vendedor cobra theta y paga gamma. **Esta identidad es el núcleo económico de todo el módulo.**

Extensiones con la cita confirmada:
- Árbol binomial de Cox, Ross y Rubinstein (1979), para opciones americanas.
- Saltos (Merton, 1976), que generan colas gruesas y smile.
- Volatilidad estocástica con fórmula cerrada (Heston, 1993). Una correlación negativa entre precio y varianza produce el skew.
- Árboles implícitos (Rubinstein, 1994) y volatilidad local de Dupire (1994, *Risk*; referencia no verificada por búsqueda).

### 2.4 Volatilidad implícita vs realizada; smile y skew

- La **IV** es la σ que iguala el precio de BSM con el de mercado. Es un precio: incluye la volatilidad esperada más una prima de riesgo. La **RV** es la desviación estándar anualizada de los rendimientos que efectivamente ocurrieron.
- **Skew del índice:** los puts OTM del S&P 500 tienen una IV mucho mayor que los calls OTM. Hay dos explicaciones con evidencia:
  - **riesgo de salto o *crash*:** Bates (2000) documenta "*post-'87 crash fears*" en las opciones sobre futuros del S&P 500, y Jackwerth y Rubinstein (1996) recuperan las distribuciones neutrales al riesgo implícitas en esos precios;
  - **presión de demanda:** en Bollen y Whaley (2004) los cambios de la IV del S&P 500 responden sobre todo a la compra neta de puts de índice por el público, y las estrategias de venta delta-neutral generan rendimientos anormales del tamaño de la brecha entre la IV y la volatilidad realizada. Gârleanu, Pedersen y Poteshman (2009) formalizan el precio basado en demanda (hallazgo cuantitativo no verificado aquí).
- En acciones individuales la demanda dominante es de calls (Bollen-Whaley 2004). Por eso el skew es menos pronunciado.

### 2.5 La volatility risk premium (VRP)

**Definición:** VRP = E^Q[RV] − E^P[RV], es decir, la varianza neutral al riesgo menos la varianza física esperada.
- El **variance swap rate** puede replicarse con una franja de opciones OTM, sin necesidad de un modelo (Demeterfi, Derman, Kamal y Zou, 1999; Britten-Jones y Neuberger, 2000). Carr y Wu (2009) usan esa réplica sintética para medir la VRP en 5 índices y 35 acciones.
- El **VIX** es, en esencia, la raíz de la tasa de un variance swap a 30 días sobre el S&P 500.
- Bakshi y Kapadia (2003): las carteras de opciones del S&P 500 cubiertas en delta rinden por debajo de cero, y rinden peor cuando la volatilidad es mayor. Es evidencia de una prima de riesgo de volatilidad negativa, que el comprador paga.
- Coval y Shumway (2001): los straddles ATM de beta cero sobre el S&P pierden **≈3% por semana**. Algún factor adicional, como la volatilidad estocástica sistemática, está siendo pagado.
- Dew-Becker, Giglio, Le y Rodriguez (2017): en 1996-2014 el mercado de variance swaps **solo pagó** por la varianza realizada transitoria e inesperada. Las noticias sobre la varianza futura, en horizontes de 1 mes a 14 años, no tuvieron precio. **Implicación:** la prima está concentrada en el plazo más corto.

**Cálculo propio: VIX contra la volatilidad realizada de los 21 días hábiles siguientes del S&P 500 (Yahoo, diario, 1990-01 a 2026-08, 9,227 días).**

| Periodo | VIX medio | RV futura media | VIX − RV (media) | % de días con VIX > RV | Peor diferencia (fecha) |
|---|---|---|---|---|---|
| 1990-2026 | 19.44 | 15.34 | **+4.10** | **85.9%** | −72.0 (20-feb-2020) |
| 1990-1999 | 18.47 | 13.02 | +5.44 | 92.4% | −16.0 (oct-1997) |
| 2000-2009 | 22.12 | 18.76 | +3.35 | 81.5% | −49.9 (16-sep-2008) |
| 2010-2019 | 16.86 | 13.18 | +3.68 | 84.3% | −28.3 (jul-2011) |
| 2020-2026 | 20.79 | 16.96 | +3.83 | 84.8% | −72.0 (feb-2020) |

En unidades de varianza, la brecha media (VIX² − RV²)/100 cayó de 1.75 en los noventa a 0.74 en 2020-2026. **Lectura:** el vendedor de volatilidad gana casi siempre y poco, y pierde rara vez y mucho. El 20-feb-2020 el VIX estaba en 15.56 y la volatilidad realizada del mes siguiente fue 87.5. El VIX no es negociable directamente, así que esta brecha es una cota bruta, no un P&L implementable.

### 2.6 VIX, futuros de VIX y ETPs

- El VIX se lanzó en 1993 sobre el OEX y se rediseñó en 2003 sobre el SPX. Los futuros de VIX existen desde el 26-mar-2004 y las opciones desde febrero de 2006 (Wikipedia, "VIX"). Máximo de cierre: **82.69** el 16-mar-2020.
- El futuro de VIX converge al VIX al vencer, no antes. Como el VIX regresa a su media y la curva suele estar en contango, un ETP que compra el futuro de 1 mes y lo rueda cada día pierde por *roll-down*. **Cálculo propio:** el VIX3M superó al VIX en el **87.7%** de los cierres mensuales de 2006-08 a 2026-09.
- **Evidencia:**
  - Eraker y Wu (2017): una cartera de futuros de VIX de 1 mes con madurez constante pierde **≈30% al año** en 2006-2013.
  - Whaley (2013): los ETPs ligados a los índices de futuros de VIX de corto plazo acumularon pérdidas de **casi US$4 mil millones** desde su lanzamiento en 2009, y los describe como "virtually guaranteed to lose money through time".
  - Cálculo propio: **VXX −99.0%** de ene-2018 a sep-2026 (−41% anual) y **UVXY −67% anual** de mar-2018 a sep-2026.
- Simon y Campasano (2014): la base de los futuros de VIX **no** predice el VIX spot, pero **sí** predice el rendimiento de los futuros (2006-2011), porque refleja una prima de riesgo cosechable.

### 2.7 Gamma de los dealers

Si los market makers están **largos** en gamma, cubren vendiendo en las subidas y comprando en las caídas, y el mercado tiende a revertir. Si están **cortos**, cubren en la dirección del movimiento y lo amplifican (momentum intradía).

Evidencia confirmada:
- Baltussen, Da, Lammers y Martens (2021, JFE) estudian más de 60 futuros de 1974 a 2020. El rendimiento de los últimos 30 minutos lo predice el rendimiento del resto del día, y ese efecto se liga a la demanda de cobertura de gamma de market makers de opciones y de ETFs apalancados.
- Barbon y Buraschi (2020, WP): la gamma negativa de los dealers interactuando con iliquidez explica el momentum intradía y se relaciona con los *flash crashes*.
- Dim, Eraker y Vilkov (2024): en los 0DTE la gamma neta de los market makers es, en promedio, **positiva** y se relaciona negativamente con la volatilidad intradía futura.
- Adams, Dim, Eraker, Fontaine, Ornthanalai y Vilkov (2025): los 0DTE **amortiguan** la volatilidad del mercado.

*Inferencia:* la gamma de los dealers ayuda a explicar la microestructura intradía. No hay evidencia publicada que la haga una señal diaria rentable para un minorista.

---

## 3. Literatura canónica

| Autores | Año | Título | Revista | Hallazgo clave cuantificado | DOI | Grado |
|---|---|---|---|---|---|---|
| Stoll | 1969 | The Relationship Between Put and Call Option Prices | JF 24(5) | Paridad put-call | 10.2307/2325677 | A |
| Black, Scholes | 1973 | The Pricing of Options and Corporate Liabilities | JPE 81(3):637-654 | Precio por réplica dinámica; μ no entra al precio | 10.1086/260062 | A (teoría) |
| Merton | 1973 | Theory of Rational Option Pricing | Bell J. Econ. 4(1) | Cotas de no arbitraje; generaliza BS | 10.2307/3003143 | A (teoría) |
| Merton | 1976 | Option pricing when underlying stock returns are discontinuous | JFE 3(1-2):125-144 | Saltos → colas gruesas y smile | 10.1016/0304-405X(76)90022-2 | A (teoría) |
| Cox, Ross, Rubinstein | 1979 | Option pricing: A simplified approach | JFE 7(3):229-263 | Árbol binomial | 10.1016/0304-405X(79)90015-1 | A (teoría) |
| Heston | 1993 | A Closed-Form Solution for Options with Stochastic Volatility… | RFS 6(2):327-343 | Volatilidad estocástica con fórmula cerrada | 10.1093/rfs/6.2.327 | A (teoría) |
| Rubinstein | 1994 | Implied Binomial Trees | JF 49(3):771-818 | Árboles consistentes con el smile | 10.1111/j.1540-6261.1994.tb00079.x | A |
| Jackwerth, Rubinstein | 1996 | Recovering Probability Distributions from Option Prices | JF 51(5):1611-1631 | Distribución neutral al riesgo del S&P a partir de opciones | 10.1111/j.1540-6261.1996.tb05219.x | A |
| Demeterfi, Derman, Kamal, Zou | 1999 | A Guide to Volatility and Variance Swaps | J. Derivatives 6(4):9-32 | Réplica del variance swap con una franja de opciones | 10.3905/jod.1999.319129 | A |
| Bates | 2000 | Post-'87 crash fears in the S&P 500 futures option market | J. Econometrics 94:181-238 | El miedo a un crash se incorpora al precio después de 1987 | 10.1016/S0304-4076(99)00021-4 | A |
| Britten-Jones, Neuberger | 2000 | Option Prices, Implied Price Processes, and Stochastic Volatility | JF 55(2):839-866 | Varianza implícita libre de modelo | 10.1111/0022-1082.00228 | A |
| Coval, Shumway | 2001 | Expected Option Returns | JF 56(3):983-1009 | Straddles ATM de beta cero: **−3%/semana** | 10.1111/0022-1082.00352 | A |
| Whaley | 2002 | Return and Risk of CBOE Buy Write Monthly Index | J. Derivatives 10(2):35-42 | BXM con mejor rendimiento ajustado por riesgo que el S&P 500 (1988-2001; cifras exactas no verificadas) | 10.3905/jod.2002.319194 | B |
| Bakshi, Kapadia | 2003 | Delta-Hedged Gains and the Negative Market Volatility Risk Premium | RFS 16(2):527-566 | Ganancias con cobertura delta < 0 y peores con más volatilidad | 10.1093/rfs/hhg002 | A |
| Bollen, Whaley | 2004 | Does Net Buying Pressure Affect the Shape of IVFs? | JF 59(2):711-753 | La compra de puts de índice mueve la IV; la venta delta-neutral gana | 10.1111/j.1540-6261.2004.00647.x | A |
| Gorton, Rouwenhorst | 2006 | Facts and Fantasies about Commodity Futures | FAJ 62(2):47-68 | 1959-2004: futuros colateralizados ≈ misma prima y Sharpe que acciones, con correlación negativa | NBER w10595 | B |
| Carr, Wu | 2009 | Variance Risk Premiums | RFS 22(3):1311-1341 | Variance swap ≈ cartera de opciones; VRP medida en 5 índices y 35 acciones | 10.1093/rfs/hhn038 | A |
| Goyal, Saretto | 2009 | Cross-section of option returns and volatility | JFE 94(2):310-326 | Long-short de straddles según RV − IV: rendimiento mensual "económicamente importante" (cifra no verificada) | 10.1016/j.jfineco.2009.01.001 | B |
| Gârleanu, Pedersen, Poteshman | 2009 | Demand-Based Option Pricing | RFS 22(10):4259-4299 | La demanda de usuarios finales afecta los precios (cifras no verificadas) | 10.1093/rfs/hhp005 | B |
| Szado | 2009 | VIX Futures and Options: A Case Study… 2008 | J. Alt. Inv. 12(2):68-85 | En 2008 los calls de VIX diversificaron más por dólar que los puts del SPX; largo en volatilidad pierde en el largo plazo | 10.3905/jai.2009.12.2.068 | B (un episodio) |
| Whaley | 2013 | Trading Volatility: At What Cost? | JPM 40(1):95-108 | ETPs de VIX: **≈US$4 mil millones** perdidos | 10.3905/jpm.2013.40.1.095 | A |
| Simon, Campasano | 2014 | The VIX Futures Basis | J. Derivatives | La base predice el rendimiento de los futuros, no el VIX | 10.3905/jod.2014.2014.1.034 | B |
| Israelov, Nielsen | 2015 | Covered Calls Uncovered | FAJ 71(6):44-57 | La pata de volatilidad corta tiene Sharpe ≈1.0 pero es <10% del riesgo; la pata de reversión es ≈¼ del riesgo y casi no paga | 10.2469/faj.v71.n6.1 | B |
| Dew-Becker, Giglio, Le, Rodriguez | 2017 | The Price of Variance Risk | JFE 123(2):225-250 | 1996-2014: solo se paga la varianza realizada transitoria e inesperada | 10.3386/w21182 | A |
| Eraker, Wu | 2017 | Explaining the negative returns to volatility claims | JFE 125(1):72-98 | Futuros de VIX de 1 mes: **≈−30%/año** (2006-2013) | 10.1016/j.jfineco.2017.04.007 | A |
| Koijen, Moskowitz, Pedersen, Vrugt | 2018 | Carry | JFE 127(2):197-225 | El carry predice rendimientos en muchas clases de activos (incluidas opciones de índice); falla en recesiones globales | 10.1016/j.jfineco.2017.11.002 | A |
| Israelov | 2018 | Pathetic Protection: The Elusive Benefits of Protective Puts | J. Alt. Inv. 21(3):6-33 | Los puts protectores dan beneficios "elusivos" (cifras no verificadas) | 10.3905/jai.2018.1.066 | B |
| Harvey, Hoyle, Rattray, Sargaison, Taylor, van Hemert | 2019 | The Best of Strategies for the Worst of Times | JPM 45(5):7-28 | 1985-2018, 8 peores drawdowns: los puts son caros y el trend es defensivo (detalle no verificado) | 10.3905/jpm.2019.45.5.007 | B |
| Muravyev, Pearson | 2020 | Options Trading Costs Are Lower than You Think | RFS 33(11):4973-5014 | Quien temporiza paga un spread efectivo **<40%** del convencional | 10.1093/rfs/hhaa010 | A |
| Baltussen, Da, Lammers, Martens | 2021 | Hedging demand and market intraday momentum | JFE 142(1):377-403 | Momentum intradía en más de 60 futuros (1974-2020), ligado a la cobertura de gamma | 10.1016/j.jfineco.2021.04.029 | A |
| Ilmanen, Thapar, Tummala, Villalon | 2021 | Tail Risk Hedging: Contrasting Put and Trend Strategies | J. Systematic Inv. 1(1):111-124 | La ventaja de costo favorece el trend sobre los puts | 10.52354/jsi.1.1.vi | B |

---

## 4. Lo más reciente 2023-2026

**Minoristas y 0DTE**
- **Bryzgalova, Pavlova y Sikorskaya (JF, dic-2023).** El trading minorista en opciones de EUA superó el 60% del volumen de mercado. Cerca del 90% del pago por flujo de órdenes (PFOF) viene de tres *wholesalers*. Los minoristas prefieren opciones semanales baratas, con un **spread promedio de 12.6%**, y pierden dinero en promedio.
- **Beckmeyer, Branger y Gayda (WP, versión del 15-dic-2023).**
  - Más de 75% de las operaciones minoristas en opciones del S&P 500 son 0DTE.
  - Entre feb-2021 y sep-2023 perdieron **US$241,000 por día** en promedio. Desde mayo de 2022, cuando empezaron los vencimientos diarios, la cifra subió a **US$350,000 por día**.
  - De las pérdidas acumuladas (más de US$125 millones), más de US$90 millones son costos de transacción. Cerca del 60% de la pérdida diaria es costo y otro 60% se concentra en puts 0DTE (los cortes se traslapan).
  - Pagan un spread efectivo de 6.0% en calls y 5.0% en puts.
  - Pierden en operaciones de una pata, en posiciones que requieren pago inicial y en opciones con IV alta. Las operaciones multi-pata que cobran la prima de volatilidad y de salto son "significativamente más rentables".
- **Brogaard, Han y Won (WP, 2023).** El volumen mensual de 0DTE pasó de 0.08 millones de contratos (ene-2011) a 34.4 millones (ago-2023), 48% del volumen de opciones de índice. Una desviación estándar más de 0DTE eleva la volatilidad 9.10% respecto de su media, impulsada por minoristas especulativos.
- **Dim, Eraker y Vilkov (WP, 2024)** y **Adams, Dim, Eraker, Fontaine, Ornthanalai y Vilkov (WP, 2025)** llegan a la conclusión opuesta a Brogaard et al.: la gamma de los market makers es positiva en promedio y los 0DTE reducen la volatilidad. El mecanismo son las posiciones de más largo plazo que se convierten en 0DTE. *Inferencia:* el debate sigue abierto (C). La mayor parte de la evidencia más reciente no apoya que los 0DTE desestabilicen el mercado.
- **Almeida, Freire y Hizmeri (WP, 2024).** En los 0DTE la VRP es alta y se explica sobre todo por compensación por riesgo **al alza**. Una estrategia que explotaba violaciones de cotas de precio fue "muy rentable hasta 2022" y **se disipó** con los vencimientos diarios.
- **Vilkov, "0DTE Trading Rules" (WP de 2023, revisado con datos de 09/2016 al 2-feb-2026).** La VRP de 0DTE es positiva, pero "pequeña y difícil de monetizar después de fricciones realistas". Los P&L están dominados por las colas. Algunas reglas condicionales a las 10:00 ET, bajo un protocolo estricto fuera de muestra, dan desempeño neto "económicamente significativo". Conclusión del autor: hay oportunidades selectivas de timing, **no una ventaja incondicional amplia**.
- **Kam (WP, 2026).** Revisa 3,909 backtests de 0DTE de OptionAlpha, 78.7% de ellos de venta de prima. El 99.9% son "rentables", con un profit factor mediano de 1.98 y valores de hasta 138. El autor advierte sobre sesgo de selección y sobreajuste. Es un ejemplo de manual de por qué los backtests publicados en foros no cuentan como evidencia.
- **O'Donovan (WP, 2026).** Desde el 16-may-2022, con vencimientos todos los días, el skew de puts del SPX se comprimió hasta 72 pb a 30 días. Estima un abaratamiento de la protección de cola de US$0.9-1.5 mil millones entre may-2022 y jun-2024. Es un solo autor y no tiene revisión por pares (grado C).
- **Elms (WP, 2026).** Con datos de 2016-2025 no encuentra *pinning* al vencimiento. Los días de mayor open interest ATM tienen rangos 16% más amplios, lo que sugiere un cambio hacia amplificación (C).
- **Hu, Kirilova, Park y Ryu (Management Science, jul-2024).** Con datos por cuenta de un mercado líder de derivados (el mercado no se confirmó en el resumen), el 66% de los minoristas activos tiene posiciones simples de un solo lado y pierden contra el resto del mercado. Para minoristas e institucionales, **vender volatilidad es el estilo más exitoso**.
- **Eaton, Green, Roseman y Wu (JFE, mar-2026).** Los minoristas compran opciones cortas y OTM y venden las de plazo largo. Durante las caídas de plataformas minoristas la IV de las opciones que compran baja, lo que indica que la demanda minorista encarece esas opciones.

**La prima de volatilidad se comprime**
- **Dew-Becker y Giglio (Chicago Fed WP 2025-17 / SSRN 2025).** Las opciones de índice tuvieron históricamente rendimientos y alfas CAPM muy negativos, pero **en los últimos 15 años los alfas son indistinguibles de cero**. Unas opciones "sintéticas" construidas con 100 años de datos nunca tuvieron alfa negativo. Su explicación es un modelo de intermediarios. **Es el hallazgo más importante del módulo para decidir si vender volatilidad.**
- **Clark y Dickson (WP, 2026).** Descomponen 50 estrategias de covered call sobre SPY, QQQ, IWM, GLD y TLT en 2010-2026. El precio del *variance carry* cayó significativamente en 4 de los 5 subyacentes, incluido IWM, que queda fuera de la huella de los ETFs de overwriting. Concluyen que hubo una revalorización amplia, no solo presión de oferta de los ETFs.
- **Opciones en sección cruzada:**
  - Heston, Jones, Khorram, Li y Mo (JF, 2023) documentan *option momentum*: los straddles con rendimientos pasados altos siguen superando a los de rendimientos bajos a 6-36 meses, sin reversión y con costos no relacionados con la magnitud.
  - Bali, Beckmeyer, Mörke y Weigert (RFS, 2023) usan más de 12 millones de observaciones de 1996-2020 y obtienen ganancias long-short con machine learning "después de costos".
  Ambos son grado B y solo implementables con acceso institucional a opciones sobre acciones.

**Datos de mercado**
- **Cboe, 2025:** 15.2 mil millones de contratos de opciones en EUA (+26% contra 2024). El SPX promedió 3.9 millones de contratos diarios y los **0DTE, 2.3 millones diarios (59%)**, con un récord mensual de 62.4% en agosto de 2025. Las opciones de VIX promediaron 858 mil diarios.
- **SEBI (India):** 93% de los operadores individuales de F&O perdieron dinero entre FY22 y FY24, con pérdidas agregadas de más de ₹1.8 lakh crore. En FY25 perdió el **91%**, y las pérdidas netas crecieron 41% a ≈₹1.06 lakh crore. Es la muestra poblacional más grande disponible y no es un estudio de caso.
- **México:**
  - MexDer lanzó el **mini futuro del dólar** (US$1,000 frente a US$10,000 del estándar), con liquidación por diferencias vía Asigna, hacia fines de mayo de 2025.
  - CME listó un **E-mini del IPC** en pesos el 18-ago-2025.
  - En 2024 MexDer negoció 8.6 millones de contratos de futuros, frente a 9,814 millones en Brasil. En palabras de su director: "el mercado de derivados de México es enorme, pero… no opera en México" (Expansión, 5-ene-2026).

**Buffer ETFs**
- Garcia-Feijoo y Silverstein (WP, 2023) reportan rendimientos ajustados por riesgo atractivos solo si se compra en la fecha de reinicio, y riesgo de opciones hacia el final del periodo.
- Hill y Moore, "Evaluating Defined Outcome Buffer Strategies" (JPM, 18-sep-2026): resultados no verificados.

---

## 5. Evidencia real: qué funciona, qué no, magnitudes netas y decaimiento

### 5.1 Put-write (Cboe PUT) — cálculo propio con Yahoo ^PUT y ^SP500TR, mensual, índices brutos

El índice PUT vende puts ATM del S&P 500 colateralizados en T-bills. Descripción estándar; la metodología no se verificó en el sitio de Cboe.

| Periodo | PUT CAGR | S&P 500 TR CAGR | PUT vol | SPTR vol | Sharpe PUT | Sharpe SPTR | MDD PUT | MDD SPTR |
|---|---|---|---|---|---|---|---|---|
| oct-1996 a sep-2026 | 8.45% | 10.26% | 10.5% | 15.4% | 0.61 | 0.57 | −32.7% | −50.9% |
| oct-1996 a dic-2006 | 10.90% | 8.84% | 10.2% | 15.4% | 0.72 | 0.40 | −29.0% | −44.7% |
| dic-2006 a dic-2016 | 6.10% | 6.94% | 11.6% | 15.3% | 0.51 | 0.47 | −32.7% | −50.9% |
| dic-2016 a sep-2026 | 8.36% | 15.29% | 9.8% | 15.4% | 0.62 | **0.84** | −20.7% | −23.9% |

- Beta del PUT contra el SPTR = 0.58 y correlación de 0.85.
- En las crisis no protege: oct-2008 −17.7% (SPTR −16.8%) y mar-2020 −13.4% (SPTR −12.4%).
- **Lectura:** el PUT es beta ~0.6 más prima de volatilidad. Su ventaja en Sharpe fue grande antes de 2007 y **desapareció** después de 2016, lo que coincide con Dew-Becker y Giglio (2025).
- Son índices sin costos de ejecución ni impuestos. Replicarlo como minorista cuesta además el spread (Bryzgalova et al.: 12.6% en las opciones que prefieren los minoristas; en el SPX ATM mensual es mucho menor, sin cifra verificada). **Grado B (decaído).**

### 5.2 Covered call / buy-write

- En Whaley (2002) el BXM mostró mejor rendimiento ajustado por riesgo que el S&P 500 entre 1988 y 2001.
- Israelov y Nielsen (2015) descomponen la estrategia: casi todo el riesgo y el rendimiento vienen de la beta accionaria. La volatilidad corta tuvo Sharpe ≈1.0 con menos de 10% del riesgo. La "reversión" implícita es ≈¼ del riesgo y casi no paga. Israelov, Klein y Tummala (2017) replican el resultado en 11 índices globales.
- **ETFs de "income" (cálculo propio, precios ajustados por distribuciones, USD, antes de impuestos):**
  - JEPI: 10.7% anual (jun-2020 a sep-2026), contra 17.1% del SPY.
  - QYLD: 9.9%, contra 21.1% del QQQ (oct-2016 a sep-2026).
  - XYLD: 8.65%, contra 15.5% del SPY. Su drawdown máximo fue −23.5%, contra −23.9% del SPY: **cedió la mitad del rendimiento y no redujo el drawdown**.
- **Grado:** B para la pata de volatilidad corta y D para vender el covered call como "ingreso". Para un objetivo de CAGR es un recorte de upside que se paga caro.

### 5.3 Puts protectores y collars

- Una put ATM a 1 mes con volatilidad de 16% cuesta ≈1.7-1.85% del nocional (cálculo propio con BSM). Rodarla todo el año suma ≈20% bruto de prima; el costo neto es la VRP más el skew.
- Israelov y Nielsen (2015, WP "Still Not Cheap", 10 índices): la protección es cara en promedio incluso en mercados calmados. "Option prices may be low, but their expected values tend to be even lower."
- Israelov (2018): los beneficios de los puts protectores son "elusivos".
- AQR (2012) y Ilmanen et al. (2021): las coberturas con opciones de índice tienen rendimiento esperado negativo, son más caras cuando más se necesitan, y el costo favorece al trend.
- **Collar:** compra un put OTM (IV alta) y vende un call OTM (IV baja). *Inferencia:* con skew, el collar "sin costo" paga el skew al renunciar a más upside esperado del que protege. No hay evidencia académica fuerte a favor (C).
- **Grado A** para "comprar protección permanente con puts destruye CAGR".

### 5.4 Tail hedging: el caso Universa contra la evidencia sistemática

**A favor (datos del gestor, no auditables):**
- Universa reportó **+3,612%** sobre el capital invertido en marzo de 2020 (Wikipedia, que cita la carta a inversionistas; Bloomberg lo reportó "con asterisco").
- Según Institutional Investor (1-jul-2020), +4,144% en lo que iba del año a marzo y un promedio de **76% anual sobre el capital invertido, neto**.
- Universa recomienda 3.33% en su estrategia y 96.67% en el S&P 500. El WSJ (2018) reportó para esa mezcla un 12.3% anual en los 10 años a feb-2018.
- **Problemas:** "capital invertido" es el presupuesto de primas, no el portafolio. Los números son del propio gestor, sin réplica independiente, y la estrategia no está disponible para una persona física.

**En contra (sistemático):**
- Ilmanen, Thapar, Tummala y Villalon (2021): el put cuesta más en el largo plazo y el trend sale mejor en costo.
- Harvey et al. (2019), con 8 drawdowns de 1985-2018: los puts son caros y las estrategias de trend y de calidad son las defensas más eficientes (detalle numérico no verificado).
- Szado (2009): en 2008 los calls de VIX dieron diversificación más eficiente que los puts del SPX, pero es un solo episodio.

**Grado C** para "el tail hedging mejora el CAGR del portafolio". Depende de puts muy OTM, de un timing de monetización y de una ejecución institucional que no se pueden verificar.

### 5.5 Venta de volatilidad y blow-ups: febrero de 2018 y después

- El **5-feb-2018** el VIX cerró en **37.32**, desde 17.31 el día 2 (**+115.6%**, cálculo propio con Yahoo).
- **XIV** (ETN inverso de VIX de Credit Suisse) tenía US$1.9 mil millones y perdió **96.3%** ese día (ETF.com). Su valor indicativo cayó por debajo del 20% del cierre previo (108.37 al 2-feb), lo que activó un **evento de aceleración**: valuación el 15-feb y liquidación el 21-feb-2018 (aviso de Credit Suisse ante la SEC).
- **SVXY:** subió 63.5% anual de nov-2011 a ene-2018 y cayó **−89.6% en febrero de 2018** (cálculo propio). ProShares bajó su objetivo de −1x a **−0.5x** desde el cierre del 27-feb-2018. De nov-2011 a sep-2026 su CAGR fue 12.2% con un drawdown máximo de **−94%**. Después del cambio (mar-2018 a sep-2026): 12.4% anual, volatilidad de 31.8% y MDD de −52.5%, contra 15.0%, 16.2% y −23.9% del SPY. **Asumió el doble de riesgo para ganar menos.**
- **Episodios posteriores (cálculo propio):**
  - 5-ago-2024: el VIX pasó de 23.39 (2-ago) a 38.57, y el USD/MXN subió 10.6% entre jun y ago-2024;
  - 8-abr-2025: VIX en 52.33;
  - 26-mar-2025: VIX de 18.33 contra una volatilidad realizada del mes siguiente de 48.2.
- **Regla empírica:** vender volatilidad es una distribución con sesgo negativo. El Sharpe histórico sobreestima su calidad porque la muestra rara vez contiene la cola.

### 5.6 0DTE y opciones minoristas

- Evidencia A de que el minorista típico pierde:
  - Bryzgalova et al. (2023);
  - Beckmeyer et al. (2023): US$350k al día, ≈60% por costos;
  - Hu et al. (2024);
  - SEBI: 91-93% de los operadores individuales pierden.
- La venta sistemática de 0DTE tiene una VRP positiva pero pequeña después de fricciones (Vilkov 2026). Los backtests de plataformas están sobreajustados (Kam 2026) y la anomalía de precio que existía desapareció en 2022 (Almeida et al. 2024).
- **Grado D** para comprar 0DTE y **C** para venderlos de forma sistemática.

### 5.7 Futuros y carry

- El carry es un predictor robusto en muchas clases de activos (Koijen et al. 2018, **A**), pero sufre en recesiones globales.
- Commodities: una prima comparable a la de las acciones en 1959-2004 (Gorton y Rouwenhorst 2006). El desempeño posterior a 2004 no se verificó aquí (actualización de Bhardwaj, Gorton y Rouwenhorst 2015: cifras no verificadas).
- **Carry del peso:** 6.79% contra 4.04% (sep-2026). Cubrir el dólar cuesta ≈2.7% al año. En las crisis el peso se deprecia: USD/MXN **+35.2%** del 19-feb al 23-mar-2020 y **+25.5%** de sep a oct-2008 (FRED DEXMXUS, cálculo propio). *Inferencia:* para un inversionista en MXN, la exposición en USD sin cubrir actúa como un tail hedge con carry negativo moderado.

### 5.8 Resumen: usos con ventaja y usos que destruyen valor (inversionista individual)

| Uso | Evidencia | Veredicto |
|---|---|---|
| Futuros o forwards para cubrir una exposición real (divisa, índice) | Teoría exacta; costo = carry | **Útil** si la exposición existe; el costo se conoce de antemano |
| Venta de volatilidad con riesgo definido (spreads), tamaño pequeño y validada | VRP positiva pero comprimida (DBG 2025) | **Edge marginal (B/C)**; solo con validación |
| Put-write o covered call como sustituto de acciones | Sharpe similar, menor CAGR desde 2017 | **Neutral para Sharpe y negativo para CAGR** |
| ETFs de covered call por "ingreso" | JEPI/QYLD/XYLD muy por debajo de su subyacente | **Destruye CAGR** |
| Puts protectores permanentes | Costo sistemático (A) | **Destruye CAGR** |
| ETPs largos de VIX sostenidos | −30 a −67% anual | **Destruye valor (A)** |
| ETPs cortos de VIX con apalancamiento | Colas de −90% | **Ruina probable sin límite de tamaño** |
| Compra de opciones cortas o 0DTE | Pérdidas minoristas (A) | **Destruye valor** |
| Venta descubierta de opciones | Pérdida ilimitada o de gap | **Prohibido** |

---

## 6. Traducción operable (cómo lo usa el sistema para ganar)

**Restricciones reales antes de cualquier regla:**
1. **Fase.** `prioridad_actual.fase = 0`: ningún derivado con dinero real. Todo lo de esta sección se ejecuta primero en el portafolio de papel.
2. **Acceso.** La ejecución es manual en la app GBM+. Según fuentes secundarias (finantres.mx, 2024-2025), la cuenta estándar de GBM **no da acceso** a opciones ni futuros listados; el acceso a MexDer requiere esquemas especializados. **Hay que verificarlo directamente con GBM.** Mientras no se verifique, el universo de derivados del sistema son los **ETPs que el SIC tenga listados** (también por verificar ticker por ticker).
3. **Tamaño.** El futuro del IPC equivale a ≈MXN 642,640 nocionales (32 veces la cuenta arena) y el del dólar a ≈MXN 177,000. **Ambos son inoperables en la cuenta arena.** El mini dólar (≈MXN 17,700) solo sería viable con un intermediario de MexDer.

**Reglas (recomendaciones del panel; los límites numéricos provienen de `config/parametros.json`):**

- **R1 — Tamaño por riesgo de gap.** Para cualquier instrumento con colas de salto, tamaño máximo = `riesgo_por_operacion` / pérdida en el peor gap histórico. No basta la pérdida hasta el stop, porque un stop no se ejecuta dentro de un gap.
  - Arena (3%): para SVXY (−0.5x), con un gap supuesto de −50% (la mitad de lo que perdió XIV el 5-feb-2018), el máximo es 0.03/0.50 = **6% del capital**.
  - Perfil estándar (1%): 2%.
  Esto rige aunque `etf_apalancado_max` permita 50%.
- **R2 — Prima en riesgo.** Si en el futuro hay opciones listadas, la suma de primas largas no pasa de `concentracion.opciones_prima_en_riesgo_max` = **2%** del capital, y cada operación no pasa de `riesgo_por_operacion` (1%, o 0.5% en fase de prueba). El perfil arena no define un límite de prima. **Mientras el dueño no lo calibre, se aplica el 2%** (interpretación conservadora, no un parámetro nuevo).
- **R3 — Nada de riesgo indefinido.** Prohibidas las ventas descubiertas de calls o puts y los ETPs inversos de volatilidad sin R1. Las ventas de volatilidad solo se hacen como spreads de riesgo definido, cuya pérdida máxima es el riesgo de la operación.
- **R4 — 0DTE descalificados por validación.** `validacion_estrategias.backtest_min_anios = 10`. Los vencimientos diarios del SPX existen desde el 16-may-2022, así que **ninguna estrategia 0DTE puede validarse antes de 2032**. Comprar 0DTE también está excluido por la evidencia A de pérdidas.
- **R5 — ETPs largos de VIX (VXX, UVXY).** Nunca se mantienen como posición. Solo se admiten como cobertura táctica con horizonte de días y con presupuesto contado como prima (R2). Si hace falta estar largo en volatilidad, se prefiere la opción de riesgo acotado, cuando haya acceso.
- **R6 — Filtro de régimen con VIX.** Ya es vigente en `filtro_apalancados`: VIX < 25 y subyacente sobre su media de 200 días. **Propuesta para el comité (no vigente):** tratar como estrés, y no abrir apalancados nuevos, cuando VIX > VIX3M. Esa curva invertida se observó en solo ≈12% de los meses desde 2006 y es un indicador de estrés de mercado (cálculo propio).
- **R7 — ETFs de covered call o "income".** Excluidos del núcleo, del satélite y de la arena mientras el objetivo sea el CAGR. La evidencia es de 6.4 a 11.3 pp anuales por debajo de su subyacente (JEPI 2020-2026; QYLD y XYLD 2016-2026; cálculo propio).
- **R8 — Sin protección permanente con puts.** La defensa del sistema son los `cortacircuitos_drawdown`, las `rachas` y el filtro de tendencia, que son más baratos según Ilmanen et al. (2021) y AQR (2012). Si el comité quiere una cobertura puntual antes de un evento binario (elección, decisión de Banxico o Fed), su costo se registra como prima (R2).
- **R9 — Divisa.** El núcleo **no cubre el USD** por defecto. La cobertura cuesta ≈2.7% al año y elimina el colchón del peso en las crisis (+35% en 2020, +25.5% en 2008). Se revisa si el diferencial de tasas cambia más de 2 pp o si el dueño tiene pasivos en USD.
- **R10 — Impuestos (persona física).** Los derivados de capital sobre acciones o índices de la BMV en mercados reconocidos pagan **10% definitivo** sobre la ganancia neta del ejercicio (art. 129, fracción IV, LISR). Los demás derivados (deuda, divisas) se acumulan a la tarifa, con una retención provisional de **25%** (art. 146 LISR; texto con última reforma del DOF del 01-04-2024, por lo que conviene revisar las reformas de 2025-2026). El rendimiento que se compara es el neto de impuestos.
- **R11 — Modo torneo.** Ir atrás del mejor rival (`desventaja_para_subir_exposicion_pp = 5`) **nunca** autoriza vender volatilidad descubierta ni violar R1. El perfil de pago de la venta de volatilidad (ganar poco casi siempre y perder todo rara vez) es justo el que deja a un competidor "fuera del juego", que es la única condición que el objetivo de la arena prohíbe.
- **R12 — Gamma de dealers y GEX.** No se usan como señal de entrada: la evidencia es intradía y de grado B/C, y los datos no son públicos ni verificables. Se registran como contexto en la bitácora.

**Checklist previo a cualquier operación con derivados o ETPs de volatilidad (todas en "sí"):**
1. ¿Está permitida en la fase actual?
2. ¿El instrumento se puede operar en GBM y se verificó su prospecto (factor, reinicio diario, cláusula de aceleración)?
3. ¿El tamaño cumple R1 con un gap histórico documentado?
4. ¿La pérdida máxima está definida y es ≤ `riesgo_por_operacion`?
5. ¿La prima acumulada es ≤ 2%?
6. ¿Pasa los filtros de VIX y de media de 200 días?
7. ¿La estrategia tiene 10 años de backtest con costos, Sharpe deflactado ≥ 0.95 y PBO ≤ 0.25?
8. ¿Hay tesis escrita con el escenario de cola y la salida?
9. ¿Se calculó el impacto fiscal?

---

## 7. Trampas y errores comunes

1. **Confundir alta tasa de acierto con ventaja.** La venta de opciones gana 85-90% de las veces (el VIX > RV el 85.9% de los días desde 1990) y aun así puede tener una esperanza nula o negativa después de las colas y los costos.
2. **Leer el Sharpe de estrategias con sesgo negativo.** Sin la cola en la muestra, el Sharpe miente. SVXY rindió 63% anual hasta enero de 2018 y perdió 90% en un mes.
3. **Creer que el roll yield es un costo "técnico" evitable.** Es la prima misma. VXX perdió 99% en ocho años sin que el VIX tuviera una tendencia a la baja.
4. **Llamar "ingreso" a la prima de un covered call.** Es una venta de upside. XYLD dio la mitad del rendimiento del SPY con el mismo drawdown.
5. **Comprar protección cuando el VIX ya subió.** Es cuando más cara está. El VRP de corto plazo se paga sobre todo por el shock inesperado (Dew-Becker et al. 2017).
6. **Tratar un stop como protección en productos con gap.** XIV cayó 96% en una sesión y su nota se aceleró.
7. **Usar el spread cotizado como costo real, o ignorarlo.** Los minoristas pagan 5-12.6%. Quien temporiza paga menos de 40% del spread convencional (Muravyev-Pearson 2020), pero un minorista con ejecución manual no temporiza.
8. **Extrapolar backtests de foros o plataformas.** Kam (2026) documenta profit factors de hasta 138 en muestras pequeñas: es sobreajuste.
9. **Suponer que la VRP de los noventa sigue viva.** Los alfas de las opciones de índice son ≈0 en los últimos 15 años (Dew-Becker y Giglio 2025). La ventaja del PUT sobre el SPTR desapareció después de 2016.
10. **Ignorar el tamaño del contrato.** Un futuro del IPC es 32 veces la cuenta arena. El apalancamiento no es opcional.
11. **Confundir el VIX con un activo.** El VIX no se compra; se compran futuros que convergen al VIX al vencer.
12. **Aceptar cifras de gestores estrella sin auditoría.** El 3,612% de Universa es sobre la prima, no sobre el portafolio, y no hay réplica independiente.
13. **Olvidar impuestos y moneda.** Una estrategia en USD se mide en MXN (ver `ideas-adoptadas`, punto 7) y neta del 10% o de la tarifa, según el instrumento.

---

## 8. Examen de titulación

1. **Con S = 17.71, r_MXN = 6.79% y r_USD = 4.04%, ¿cuál es el forward a 1 año y quién paga el carry?** F ≈ 18.18. Paga el comprador de dólares a futuro (≈2.7% al año) y lo cobra el vendedor.
2. **Enuncie la paridad put-call y muestre por qué el PUT y el BXM son casi equivalentes.** C − P = S·e^{−qT} − K·e^{−rT}. Por eso put vendido + T-bills ≡ acción + call vendido.
3. **¿Por qué el precio de BSM no depende de μ?** Porque la cartera de réplica elimina el riesgo, y un instrumento libre de riesgo rinde r.
4. **Escriba el P&L de una opción con cobertura delta.** ≈ ½·Γ·S²·(σ²_real − σ²_impl)·dt. El comprador gana si la volatilidad realizada supera a la implícita.
5. **Dé dos explicaciones con evidencia del skew del S&P 500.** El miedo a un crash después de 1987 (Bates 2000) y la presión de compra de puts de índice (Bollen-Whaley 2004).
6. **¿Qué encontraron Coval y Shumway (2001)?** Que los straddles ATM de beta cero pierden ≈3% por semana, lo que implica que se paga el riesgo de volatilidad.
7. **¿Cuál es el hallazgo de Dew-Becker y Giglio (2025) y qué implica?** Los alfas de las opciones de índice son ≈0 en los últimos 15 años. Vender volatilidad ya no es un almuerzo gratis; su ventaja es marginal.
8. **¿Por qué VXX pierde en el largo plazo?** Por el contango de los futuros de VIX (VIX3M > VIX en ≈88% de los meses) y la reversión a la media: rueda comprando caro. Eraker-Wu: −30% al año; cálculo propio: −41% al año en 2018-2026.
9. **¿Qué pasó con XIV el 5-feb-2018?** El VIX subió de 17.31 a 37.32. XIV perdió 96.3%, su valor indicativo cayó por debajo del 20% del cierre previo y Credit Suisse aceleró la nota (liquidación el 21-feb).
10. **¿Cuánto pierden los minoristas en 0DTE y por qué?** US$350k al día desde mayo de 2022 (Beckmeyer et al.). Cerca del 60% por costos de transacción, y sobre todo en operaciones de una pata y opciones con IV alta.
11. **¿Por qué el sistema no puede operar estrategias 0DTE aunque un backtest salga bien?** Porque exige 10 años de backtest y los vencimientos diarios existen desde mayo de 2022.
12. **Con riesgo por operación de 3% y un gap histórico de 50%, ¿cuál es el tamaño máximo?** 6% del capital (R1).
13. **¿Cómo tributa en México la ganancia de un futuro del IPC en MexDer para una persona física?** 10% definitivo sobre la ganancia neta anual (art. 129, fracción IV, LISR). Un futuro de TIIE o de dólar se acumula, con una retención provisional de 25% (art. 146).
14. **¿Por qué el núcleo no cubre el USD por defecto?** La cobertura cuesta ≈2.7% al año y el peso se deprecia en las crisis (+35% en 2020), lo que amortigua las caídas en MXN.
15. **¿Qué dice la evidencia sistemática sobre puts contra trend como coberturas de cola?** Que el put cuesta más en el largo plazo y el trend tiene ventaja de costo (Ilmanen et al. 2021). Las cifras de Universa no son auditables ni replicables.

---

## 9. Fuentes

**Artículos académicos**
1. Stoll (1969) — https://doi.org/10.2307/2325677
2. Black, Scholes (1973) — https://doi.org/10.1086/260062
3. Merton (1973) — https://doi.org/10.2307/3003143
4. Merton (1976) — https://doi.org/10.1016/0304-405X(76)90022-2
5. Cox, Ross, Rubinstein (1979) — https://doi.org/10.1016/0304-405X(79)90015-1
6. Heston (1993) — https://doi.org/10.1093/rfs/6.2.327
7. Rubinstein (1994) — https://doi.org/10.1111/j.1540-6261.1994.tb00079.x
8. Jackwerth, Rubinstein (1996) — https://doi.org/10.1111/j.1540-6261.1996.tb05219.x
9. Demeterfi, Derman, Kamal, Zou (1999) — https://doi.org/10.3905/jod.1999.319129
10. Bates (2000) — https://doi.org/10.1016/S0304-4076(99)00021-4
11. Britten-Jones, Neuberger (2000) — https://doi.org/10.1111/0022-1082.00228
12. Coval, Shumway (2001) — https://doi.org/10.1111/0022-1082.00352
13. Whaley (2002) — https://doi.org/10.3905/jod.2002.319194
14. Bakshi, Kapadia (2003) — https://doi.org/10.1093/rfs/hhg002 ; https://ideas.repec.org/a/oup/rfinst/v16y2003i2p527-566.html
15. Bollen, Whaley (2004) — https://doi.org/10.1111/j.1540-6261.2004.00647.x
16. Gorton, Rouwenhorst (2006) — https://www.nber.org/papers/w10595
17. Carr, Wu (2009) — https://doi.org/10.1093/rfs/hhn038 ; https://ideas.repec.org/a/oup/rfinst/v22y2009i3p1311-1341.html
18. Goyal, Saretto (2009) — https://doi.org/10.1016/j.jfineco.2009.01.001
19. Gârleanu, Pedersen, Poteshman (2009) — https://doi.org/10.1093/rfs/hhp005
20. Szado (2009) — https://doi.org/10.3905/jai.2009.12.2.068
21. Ilmanen (2012), FAJ 68(5) (título confirmado; hallazgo no usado) — https://doi.org/10.2469/faj.v68.n5.7
22. Whaley (2013) — https://doi.org/10.3905/jpm.2013.40.1.095
23. Simon, Campasano (2014) — https://doi.org/10.3905/jod.2014.2014.1.034
24. Israelov, Nielsen (2015), Covered Calls Uncovered — https://doi.org/10.2469/faj.v71.n6.1
25. Israelov, Nielsen (2015), Still Not Cheap (WP) — https://doi.org/10.2139/ssrn.2579232
26. Dew-Becker, Giglio, Le, Rodriguez (2017) — https://www.nber.org/papers/w21182
27. Eraker, Wu (2017) — https://doi.org/10.1016/j.jfineco.2017.04.007
28. Israelov, Klein, Tummala (2017, WP) — https://doi.org/10.2139/ssrn.2990522
29. Koijen, Moskowitz, Pedersen, Vrugt (2018) — https://doi.org/10.1016/j.jfineco.2017.11.002
30. Israelov (2018) — https://doi.org/10.3905/jai.2018.1.066
31. Harvey, Hoyle, Rattray, Sargaison, Taylor, van Hemert (2019) — https://doi.org/10.3905/jpm.2019.45.5.007
32. Muravyev, Pearson (2020) — https://doi.org/10.1093/rfs/hhaa010
33. Barbon, Buraschi (2020, WP) — https://doi.org/10.2139/ssrn.3725454
34. Baltussen, Da, Lammers, Martens (2021) — https://doi.org/10.1016/j.jfineco.2021.04.029
35. Ilmanen, Thapar, Tummala, Villalon (2021) — https://doi.org/10.52354/jsi.1.1.vi
36. Bryzgalova, Pavlova, Sikorskaya (2023) — https://doi.org/10.1111/jofi.13285
37. Heston, Jones, Khorram, Li, Mo (2023) — https://doi.org/10.1111/jofi.13279
38. Bali, Beckmeyer, Mörke, Weigert (2023) — https://doi.org/10.1093/rfs/hhad017
39. Beckmeyer, Branger, Gayda (2023, WP) — https://doi.org/10.2139/ssrn.4404704 ; PDF: https://wp.lancs.ac.uk/fofi2024/files/2024/04/FoFI-2024-146-Leander-Gayda.pdf
40. Brogaard, Han, Won (2023, WP) — https://doi.org/10.2139/ssrn.4426358
41. Bandi, Fusari, Renò (2023, WP) — https://doi.org/10.2139/ssrn.4503344
42. Vilkov (2023, rev. 2026, WP) — https://doi.org/10.2139/ssrn.4641356
43. Garcia-Feijoo, Silverstein (2023, WP) — https://doi.org/10.2139/ssrn.4371346
44. de Silva, Smith, So (2022, WP), "Losing is Optional" (título confirmado; hallazgos no verificados) — https://doi.org/10.2139/ssrn.4050165
45. Dim, Eraker, Vilkov (2024, WP) — https://doi.org/10.2139/ssrn.4692190
46. Almeida, Freire, Hizmeri (2024, WP) — https://doi.org/10.2139/ssrn.4701401
47. Adams, Fontaine, Ornthanalai (2024, WP) — https://doi.org/10.2139/ssrn.4881008
48. Hu, Kirilova, Park, Ryu (2024) — https://doi.org/10.1287/mnsc.2023.4916
49. Adams, Dim, Eraker, Fontaine, Ornthanalai, Vilkov (2025, WP) — https://doi.org/10.2139/ssrn.5641974
50. Vasquez, Amaya, Pearson, Garcia-Ares (2025, WP; resumen no verificado) — https://doi.org/10.2139/ssrn.5113405
51. Dew-Becker, Giglio (2025, WP) — https://doi.org/10.2139/ssrn.5525882 ; https://doi.org/10.21033/wp-2025-17
52. Eaton, Green, Roseman, Wu (2026) — https://doi.org/10.1016/j.jfineco.2026.104238
53. Clark, Dickson (2026, WP) — https://doi.org/10.2139/ssrn.7124759
54. O'Donovan (2026, WP) — https://doi.org/10.2139/ssrn.6836498
55. Kam (2026, WP) — https://doi.org/10.2139/ssrn.7055179
56. Elms (2026, WP) — https://doi.org/10.2139/ssrn.6564078
57. Hill, Moore (2026) — https://doi.org/10.3905/jpm.2026.066

**Datos, mercado y regulación**

58. Cboe, "The State of the Options Industry: 2025" (22-ene-2026) — https://www.cboe.com/insights/posts/the-state-of-the-options-industry-2025/
59. Cboe, récord de 0DTE de agosto de 2025 — https://www.cboe.com/insights/posts/spx-0-dte-options-jump-to-record-62-share-in-august/ ; volumen de 2025: https://www.prnewswire.com/news-releases/cboe-global-markets-reports-trading-volume-for-december-and-full-year-2025-302654309.html
60. Wikipedia, "VIX" (fechas de lanzamiento y máximos) — https://en.wikipedia.org/wiki/VIX
61. ETF.com, "Inverse VIX ETN Shuts Down" — https://www.etf.com/sections/news/inverse-vix-etn-shuts-down
62. Credit Suisse, aviso de aceleración de XIV (SEC, 6-feb-2018) — https://www.sec.gov/Archives/edgar/data/1053092/000095010318001572/dp86358_ex9901.htm
63. AMF (Francia), la volatilidad de febrero de 2018 y los productos de VIX — https://www.amf-france.org/sites/institutionnel/files/contenu_simple/lettre_ou_cahier/risques_tendances/Heightened%20volatility%20in%20early%20February%202018%20the%20impact%20of%20VIX%20products.pdf
64. ProShares, SVXY (−0.5x desde el 27-feb-2018) — https://www.proshares.com/our-etfs/strategic/svxy ; CNBC: https://www.cnbc.com/2018/02/27/firm-swoops-in-to-ensure-volatility-is-a-trade-for-another-day.html
65. Wikipedia, "Universa Investments" — https://en.wikipedia.org/wiki/Universa_Investments
66. Institutional Investor (1-jul-2020), Universa — https://www.institutionalinvestor.com/article/b1m9rt53wxyns9/You-re-Doing-It-Wrong-A-Tail-Risk-Hedger-Calls-Out-His-Industry
67. AQR, "Tail-Hedging Strategies" (4T-2012) — https://www.aqr.com/Insights/Research/Alternative-Thinking/Tail-Hedging-Strategies
68. SEBI, estudio de F&O FY22-FY24 (23-sep-2024) — https://www.sebi.gov.in/media-and-notifications/press-releases/sep-2024/updated-sebi-study-reveals-93-of-individual-traders-incurred-losses-in-equity-fando-between-fy22-and-fy24-aggregate-losses-exceed-1-8-lakh-crores-over-three-years_86906.html
69. SEBI, FY25 (vía Business Standard, 7-jul-2025) — https://www.business-standard.com/markets/news/net-losses-of-traders-in-fo-widens-in-fy25-sebi-study-125070701221_1.html
70. Grupo BMV, mini futuro del dólar (30-may-2025) — https://blog.bmv.com.mx/el-nuevo-contrato-mini-del-futuro-del-dolar-cobertura-cambiaria-accesible-para-mas-inversionistas/ ; boletín: https://www.bmv.com.mx/docs-pub/SALA_PRENSA/CTEN_BOLE/Nuevo%20Contrato%20Mini%20Futuro%20D%C3%B3lar%2028.05.25.pdf
71. Expansión (5-ene-2026), mini dólar, E-mini IPC y volúmenes de MexDer — https://expansion.mx/mercados/2026/01/05/mini-dolar-futuros-ipc-plan-bmv-reactivar-derivados
72. MexDer, especificaciones del futuro del IPC ($10 × IPC; documento alojado por CME) — https://www.cmegroup.com/education/files/contrato-de-futuro-del-indice-de-precios-y-cotizaciones.pdf ; catálogo: http://www.mexder.com.mx/wb3/wb/MEX/contratos_futuro
73. Ley del Impuesto sobre la Renta, arts. 129 y 146 (Cámara de Diputados; última reforma DOF 01-04-2024) — https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf
74. Finantres, "¿Se puede operar con opciones con GBM?" (fuente secundaria) — https://finantres.mx/opciones-gbm/
75. Yahoo Finance: ^PUT, ^SP500TR, ^VIX, ^VIX3M, ^GSPC, ^MXX, SVXY, VXX, UVXY, JEPI, QYLD, XYLD, SPY y QQQ (descargados el 25-sep-2026 con `herramientas/datos.py`) — https://finance.yahoo.com
76. FRED: DEXMXUS, DTB3, TB3MS e IR3TIB01MXM156N — https://fred.stlouisfed.org/series/DEXMXUS ; https://fred.stlouisfed.org/series/IR3TIB01MXM156N

**Pendiente de verificación:**
- las cifras exactas de Whaley (2002), Goyal-Saretto (2009), Israelov (2018) y Harvey et al. (2019);
- la metodología exacta de los índices PUT y BXM en la documentación de Cboe;
- la oferta de derivados de GBM para personas físicas;
- el margen vigente de los contratos de MexDer;
- el futuro de TIIE de Fondeo;
- las reformas a la LISR posteriores al 01-04-2024;
- el mercado exacto que estudian Hu et al. (2024);
- la venue de Dupire (1994).
