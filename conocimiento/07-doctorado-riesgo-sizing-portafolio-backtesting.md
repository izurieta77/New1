# Módulo 07 — Gestión de riesgo, sizing, construcción de portafolio y backtesting

> Nivel: doctorado · Actualizado: 2026-09-25 · Grado de evidencia global: **B**. Las matemáticas son exactas bajo sus supuestos (grado A): crecimiento geométrico, Kelly, rachas, error estándar del Sharpe, DSR y MinBTL. Casi toda la evidencia sobre qué mejora el desempeño neto fuera de muestra cae en B o C. Hay tres ejemplos. La gestión por volatilidad perdió su ventaja en Sharpe después de publicarse. Risk parity perdió 22.8% en 2022. HRP no le gana a métodos más simples fuera de muestra. Lo que sí sobrevive con claridad es el control de pérdidas: menos drawdown, sizing fraccional y validación estricta.

---

## 1. Objetivos de dominio (qué debe saber hacer quien "se titula" en este módulo)

1. Derivar el crecimiento geométrico g ≈ μ − σ²/2 y cuantificar el *volatility drag* de un portafolio y de un ETF apalancado (L×).
2. Derivar Kelly (binario y continuo), el crecimiento de Kelly fraccional (fracción 2c − c² del crecimiento máximo) y la probabilidad de tocar un nivel de pérdida, x^(2/c − 1). Con esto, justificar `kelly.fraccion_max` = 0.25 (patrimonio) y 0.5 (arena).
3. Calcular por programación dinámica la probabilidad de rachas perdedoras. Convertir una racha en drawdown con (1 − r)^k y elegir el riesgo por operación para que las rachas inevitables no toquen los cortacircuitos.
4. Explicar qué hacen el *volatility targeting* y los *volatility-managed portfolios*, y cuándo mejoran el Sharpe y cuándo solo reducen colas, con evidencia fuera de muestra, neta de costos y posterior a la publicación.
5. Construir portafolios robustos al error de estimación (1/N, shrinkage de Ledoit-Wolf, Black-Litterman, HRP, risk parity) y saber cuándo cada uno falla.
6. Medir el riesgo con VaR, Expected Shortfall/CVaR, drawdown y CDaR. Conocer sus propiedades (coherencia) y sus fallas con colas gruesas y correlaciones que suben en crisis.
7. Evaluar reglas de stop-loss con el marco de Kaminski-Lo: cuándo agregan y cuándo restan rendimiento esperado.
8. Auditar un backtest: número de pruebas, DSR, PBO/CSCV, MinBTL, *haircut* de Harvey-Liu, *purged k-fold* con embargo, CPCV frente a walk-forward, sesgos de supervivencia y de look-ahead, costos, capacidad y decaimiento después de publicar.
9. Calcular el error estándar del Sharpe (Lo 2002), el PSR y el MinTRL. Saber cuánto historial hace falta para distinguir habilidad de suerte, incluida la duración de una temporada de la arena.
10. Diseñar el rebalanceo (bandas frente a calendario, región de no-transacción) y la cosecha de pérdidas fiscales bajo el art. 129 de la LISR.
11. Traducir todo lo anterior a las reglas de `config/parametros.json` y a las funciones de `herramientas/` (`riesgo.py`, `metricas.py`, `backtest.py`).

---

## 2. Núcleo teórico

### 2.1 Crecimiento geométrico y volatility drag

- En tiempo continuo (lognormal): g = E[ln(1+R)] ≈ μ − σ²/2. Con σ = 20%, el drag es 2 pp al año; con σ = 50%, 12.5 pp.
- Con apalancamiento L rebalanceado a diario: g_L ≈ r + L(μ − r) − L²σ²/2 − comisiones − costo de financiamiento. El castigo crece con **L²**. Con σ = 20%, un 3× pierde (9 − 3)·0.04/2 = **12 pp al año adicionales** frente a 3 veces el crecimiento del subyacente. La trayectoria importa: un ETF apalancado depende del camino que siguen los precios, no solo del rendimiento final (Avellaneda-Zhang 2010).
- **Dato propio (Yahoo, cierre ajustado, 31-dic-2021 a 24-sep-2026):** QQQ +91.7%, QLD (2×) +118.7%, **TQQQ (3×) +98.7%**. En 2022: QQQ −32.6%, QLD −60.5%, TQQQ −79.1%. En casi 5 años, el 3× apenas superó al 1× y quedó por debajo del 2×.
- *Inferencia:* el apalancamiento óptimo de crecimiento es L* = (μ − r)/σ² (Kelly continuo). Supón una prima de 5% y σ = 16% para un índice amplio. Entonces L* ≈ 1.95, y eso **con parámetros conocidos**. Con la σ de Nasdaq en 2022, L* cae muy por debajo de 3. Por eso un 3× permanente destruye crecimiento. Solo tiene sentido cuando un filtro reduce la exposición en los regímenes de volatilidad alta.

### 2.2 Criterio de Kelly y Kelly fraccional

- **Binario** (ganar b por unidad arriesgada con probabilidad p, perder 1 con q = 1 − p): f* = p − q/b. Con p = 0.55 y b = 1, f* = 10% del capital en riesgo.
- **Continuo** (Kelly 1956; Thorp 2008): f* = (μ − r)/σ². En varios activos, **f* = Σ⁻¹(μ − r)**, que es el portafolio tangente apalancado.
- **Crecimiento con fracción c de Kelly** (derivación propia en el modelo lognormal): g(c) − r = SR²·(c − c²/2). Frente al máximo SR²/2 queda la fracción **2c − c²**:

| c (fracción de Kelly) | % del crecimiento máximo | Volatilidad relativa | P(tocar alguna vez −20% desde el inicio) | P(−35%) | P(−50%) |
|---|---|---|---|---|---|
| 1.00 | 100% | 1.00 | 80% | 65% | 50% |
| 0.50 | 75% | 0.50 | 51% | 27.5% | 12.5% |
| 0.25 | 43.8% | 0.25 | 21% | 4.9% | 0.8% |
| 2.00 | 0% (crecimiento nulo) | 2.00 | — | — | — |

  Las probabilidades salen de P(ver alguna vez x·W₀) = x^(2/c − 1), para un movimiento browniano con deriva, horizonte infinito y parámetros conocidos (derivación propia). **Supuesto implícito, explicitado el 2026-09-25:** la riqueza se mide en exceso sobre el efectivo (r = 0, o en términos reales si la tasa real es cero). Con r > 0 en términos nominales, el exponente es 2g/(c·SR)², con g = r + SR²(c − c²/2), y las probabilidades bajan mucho: con r = 4% y c = 0.5, P(−35%) = 6.7% en lugar de 27.5%. En un horizonte finito de 30 años con pasos mensuales, la simulación da valores algo menores que la fórmula (c = 0.5: P(−35%) = 22.8%). Ver `fichas/2026-09-25-kelly-fraccional.md`. En el caso binario (p = 0.55, b = 1), la simulación exacta da 43.7% del crecimiento con c = 0.25, 74.9% con c = 0.5 y −2.8% con c = 2.
- **Buenas y malas propiedades** (MacLean-Thorp-Ziemba 2010, QF): Kelly maximiza la tasa límite de crecimiento, pero sus apuestas son grandes y la riqueza oscila con violencia en horizontes finitos. El Kelly fraccional cambia crecimiento por seguridad.
- **Incertidumbre de parámetros** (Baker-McHale 2013): usar p estimado en lugar del verdadero empeora el desempeño fuera de muestra. La apuesta óptima se **encoge** según la varianza del estimador.
  - *Inferencia clave:* si crees estar a 0.5 Kelly pero tu ventaja real es la mitad de la estimada, en realidad estás a **1.0 Kelly**, y P(−35%) pasa de 27.5% a 65%. El error de estimación siempre empuja hacia el sobreapostar, así que el tope fraccional es obligatorio.
- **Kelly con restricción de drawdown** (Busseti-Ryu-Boyd 2016): acotar la probabilidad de un drawdown da un problema convexo. Con el mismo riesgo de drawdown, sus apuestas superan al Kelly fraccional.

### 2.3 Matemática de rachas perdedoras

La probabilidad exacta de al menos una racha de k pérdidas en n operaciones independientes se calcula con una cadena de Markov cuyo estado es la longitud de la racha vigente (`metricas.prob_racha_perdedora`). Resultados propios:

| Aciertos | n | P(racha ≥ 3) | P(racha ≥ 5) | P(racha ≥ 8) | E[racha máxima] |
|---|---|---|---|---|---|
| 55% | 100 | 99.8% | **64.7%** | 8.4% | 5.25 |
| 60% | 100 | 98.8% | **45.9%** | 3.6% | 4.61 |
| 50% | 48 (una temporada de la arena: 8 ops/mes × 6) | 98.0% | 53.6% | — | 4.95 |
| 55% | 48 | 94.5% | 38.2% | — | 4.35 |
| 60% | 48 | 87.6% | 24.7% | — | 3.82 |

**Del sizing al drawdown:** k pérdidas seguidas con riesgo r cuestan 1 − (1 − r)^k.
- r = 1%: 5 pérdidas = −4.90%; 10 = −9.56%.
- r = 3%: 5 pérdidas = −14.13%; 10 = −26.26%.
- Con la regla de rachas de `parametros.json` (tras 3 pérdidas, riesgo ×0.5; pausa a la 5.ª), la peor racha antes de la pausa cuesta **−3.94%** con r = 1% y **−11.45%** con r = 3%.

Con 55% de aciertos, una racha de 5 es más probable que no en 100 operaciones. El sizing decide si esa racha es una anécdota (−4.9%) o un evento que dispara cortacircuitos (−14%).

### 2.4 Volatility targeting y volatility-managed portfolios

- **Moreira-Muir (2017, JF):** peso w_t = c/σ̂²_{t−1}, donde σ̂² es la varianza realizada del mes anterior y c iguala la volatilidad no condicional. En el mercado (1926-2015, versión NBER w22208), el alfa es **4.86% anual**, el appraisal ratio 0.33 y el Sharpe sube **+25%**. Funciona porque los cambios de volatilidad no se compensan con cambios proporcionales en el rendimiento esperado.
- **Cederburg-O'Doherty-Wang-Yan (2020, JFE):** revisan 103 estrategias de acciones. Las versiones gestionadas **no superan sistemáticamente** a las originales en comparación directa. Los alfas de las regresiones de *spanning* no se pueden implementar en tiempo real. Las versiones fuera de muestra razonables ganan **menos** Sharpe y menos equivalente cierto. La causa es la inestabilidad estructural de esas regresiones. **Excepciones (adenda 2026-09-25, examen diagnóstico S4-08), verificadas contra el resumen del artículo:** "volatility management enhances the performance of **momentum (in particular), profitability, and BAB** strategies, but has not added value when used with the other six commonly used factors." https://ideas.repec.org/a/eee/jfinec/v138y2020i1p95-117.html
- **Barroso-Detzel (2021, JFE):** netos de costos, solo sobrevive la gestión por volatilidad del **mercado**, y su ventaja se concentra en periodos de sentimiento alto. En los demás factores, el alfa neto es ≈ 0 y el Sharpe baja.
- **Harvey et al. (2018, JPM):** el targeting sube el Sharpe solo en activos de riesgo (acciones y crédito) por el *leverage effect*. En bonos, divisas y materias primas el efecto sobre el Sharpe es despreciable. En **todas** las clases reduce las colas izquierdas.
- **Hood-Raughtigan (2025, JPM 52(1), 100-121; doi:10.3905/jpm.2025.1.764; WP SSRN 4773781, abr-2024) (laboratorio 2026-09-30):** atribuyen el "alfa" del targeting a una **exposición a tendencia**. Réplica de MM con Mkt-Rf de FF (may-1927 a dic-2023, volatilidad de 3 meses, 1 día de rezago): α = 3.15% (t 3.0). Al agregar una tendencia simple (Hurst-Ooi-Pedersen, signo promedio a 1/3/12 meses), el α baja a **1.19% (t 1.2), −62%**, con β_tendencia 0.30 (t 12.0). El mecanismo es el *leverage effect* (corr(rend. 1m, Δvol) = −0.31): en acciones, la volatilidad sube cuando el precio cae. En 50 futuros (2001-2023), la tendencia explica el α solo en acciones (panel: β_tend 0.35, el intercepto cae 2/3) y algo en energía. En bonos, divisas y la mayoría de las materias primas no cambia nada.
  - **Acceso:** se leyeron íntegras las láminas del autor (R/Finance 2024, 25 págs., con tablas) más los metadatos de Crossref. No se leyó el artículo publicado (SSRN 403, pm-research 429). Según el resumen, la versión JPM usa 14 futuros de índices accionarios, así que las cifras de la versión final pueden diferir.
  - **Limitaciones:** es una descomposición in-sample con un solo factor de tendencia, sin costos ni réplica independiente.
  - **Grado B** para el mecanismo, porque coincide con Harvey et al. 2018 y con R05, donde el α se concentra en 1928-37. **Grado C** para las magnitudes.
  - **Implicación:** refuerza "freno, no alfa" (AC-06). El targeting y el filtro de tendencia (cap. 14, R2) son en buena parte **la misma apuesta**, así que no se cuentan como diversificación independiente al combinarlos en acciones. No cambia ningún criterio.
- **Božović (2024), "VIX-managed portfolios", *International Review of Financial Analysis* 95, art. 103353, doi:10.1016/j.irfa.2024.103353 (investigador vespertino, nota 2026-10-03).** Publicado; una sola autoría (U. de Belgrado).
  - **Método:** el peso es w_t = c_t/σ̂²_t, con σ̂²_t = (1/12)·Σ_d VIX²_d del mes t, sin topes de apalancamiento. c_t iguala la desviación estándar del portafolio gestionado y la del original **con información hasta t** (ventana expansiva, 36 meses de arranque), lo que atiende la crítica de Cederburg et al. sobre pesos ex post. La muestra es 1990-01 a 2023-04: 10 factores, 7 portafolios MVE y 176 anomalías de Chen-Zimmermann. El modelo de costos sigue a Wang-Yan (1 a 50 pb por unidad de rotación).
  - **Hallazgos para el mercado (MKT):** α de spanning = **3.07% anual** (EE 1.44, t ≈ 2.1). La versión con VIX a la baja da 3.39% y la de varianza realizada 3.13%. **ΔSharpe = +0.10 sobre 0.54, no significativo** (estadístico de Wright 0.62). Un dólar crece a 14.29 contra 8.63 sin gestionar (1993-2023). La ventaja frente a la varianza realizada está en la **rotación**: con 25 pb el α de MKT sigue siendo significativo y el punto de equilibrio es de 91 pb. El autor cita a Clarke et al. (2020): escalar un 50/50 S&P/efectivo con el inverso del VIX de fin de mes sube el Sharpe ≈ 0.09 (cita de segunda mano, no leída).
  - **Acceso:** se leyó íntegra la versión de trabajo (EFMA 2024, 30+ págs.: método, tablas 1-3 y costos). No se leyó la versión publicada, de pago; su resumen es idéntico. La Figura 2 (orden por quintiles del VIX del mes previo) no se pudo leer como imagen.
  - **Limitaciones:** pesos sin topes, cuando la cuenta tiene tope de 1.0 (fase 1); en el mercado el resultado es α de spanning y no ΔSharpe significativo; revista de rango medio; sin réplica independiente.
  - **Contradicción interna y comprobación propia:** el texto afirma que "el VIX rezagado se relaciona **inversamente** con el rendimiento medio de MKT". En la introducción, en cambio, dice que el VIX se correlaciona **positivamente** con los rendimientos futuros (Bekaert-Hoerova 2014). Lo comprobé con la misma definición (VIX² promedio del mes t, quintiles, rendimientos diarios del mes t+1, ^GSPC de Yahoo sin dividendos, 1990-01 a 2023-04, 399 meses): el **quintil más alto (VIX ≈ 32) tiene la media más alta**, 17.5% anualizada con σ de 23.6%, contra 10.5% y 9.4% del quintil más bajo. La afirmación de la media **no se reproduce**. Lo que sí se reproduce es lo que importa para el targeting: μ/σ² cae de ≈ 1.19 a ≈ 0.31 entre el primer y el último quintil. Es comprobación rápida, sin script versionado: grado D.
  - **Grado C.** Coincide en dirección con Moreira-Muir y Barroso-Detzel (solo sobrevive el mercado). El VIX es una mejor señal que la RV **por costo de rotación**, no por un Sharpe mayor.
  - **Implicación para `filtro_apalancados`:** la literatura respalda **escalar** la exposición de forma continua con 1/VIX² para mejorar Sharpe y colas. **No** respalda **salir** de golpe con VIX ≥ 25 para mejorar el rendimiento. Para un 3x, el crecimiento es ≈ 3μ − 4.5σ², y en mis quintiles queda prácticamente igual en ambos extremos: ≈ 27.5% anual con VIX bajo y ≈ 27.4% con VIX alto (sin r_f ni costos). La salida binaria renuncia a la media alta de los rebotes a cambio de quitarse varianza. Esto coincide con la ficha `fichas/2026-10-03-vrp-vix.md` y matiza la frase de R8 (§6.3) "es coherente con Harvey et al.": Harvey et al. y Moreira-Muir prueban escalamiento continuo, no un umbral de salida. No cambia ningún criterio. Es un insumo para el comité del 9-oct.
- **Bongaerts, Kang, van Dijk (2020), "Conditional Volatility Targeting", *Financial Analysts Journal* 76(4), 54-71, doi:10.1080/0015198X.2020.1790853 (investigador vespertino, nota 2026-10-04).** Publicado, con arbitraje doble ciego (revisora: Lisa Goldberg) y acceso abierto CC BY-NC-ND (repositorio de Erasmus, repub.eur.nl/pub/130215).
  - **Método:** el peso mensual es w = σ_obj/σ̂_{t−1}, es decir **1/σ, no 1/σ²**. σ̂ es la volatilidad realizada del mes previo (sin el último día) y σ_obj la volatilidad de largo plazo con datos hasta t−1, sin escalado ex post. La versión **condicional** solo escala si la σ̂ del mes previo cae en el quintil superior (reduce) o inferior (apalanca hasta L_max = 2) de su historia expansiva; en los quintiles 2-4 se queda en 1x. Muestra: futuros e índices de 10 mercados (estrategia 1982-2019), con factores FF de acciones grandes (EUA 1973-2019 y regiones 1995-2019). Netos de costos: 3-5 pb en futuros y 25 pb más el rebalanceo en factores.
  - **Hallazgos para el mercado (tablas 1, 3 y 4):** en EUA (Sharpe original 0.59, MDD 52.8%), el targeting convencional da +0.15 de Sharpe (significativo al 5%) y −7.0 pp de MDD, pero **sube** el expected shortfall y gira 2.4 veces al año. El condicional da **+0.16 (5%)**, **−8.3 pp** de MDD, −1.7 pp de ES y gira 1.6 veces. En el promedio de los 10 mercados, el condicional da +0.07 de Sharpe y −6.6 pp de MDD (mejora el Sharpe en 10 de 10, pero solo es significativo en EUA y Hong Kong). El convencional da +0.04 y +2.3 pp de MDD, y la empeora en 4 mercados. El resultado es robusto a cuartiles y a umbrales fijos de σ̂/σ_obj (>1.0 o 1.2 para reducir): en EUA, +0.15 a +0.17 de Sharpe. El mecanismo: corr(σ̂, rendimiento futuro) es −0.22 en el quintil alto de EUA y ≈ 0 en los demás; la autocorrelación de la volatilidad es 0.43 contra 0.14-0.22. En factores, el método solo sirve para el **momentum**, como en Cederburg et al. y Barroso-Detzel.
  - **Acceso:** lectura íntegra del PDF publicado, 19 págs. con tablas 1-4, A1 y A2 y notas. No se leyó el apéndice suplementario en línea (tablas S1 y S2).
  - **Limitaciones:** no reporta CAGR ni crecimiento, solo Sharpe, MDD, ES y giro. **No prueba una salida binaria a efectivo.** La versión que solo reduce sin apalancar (nota 6, tabla A2) se reporta **solo para momentum**, no para el mercado. Usa volatilidad realizada, no VIX. Sin réplica independiente localizada.
  - **Grado C.** Es publicado y arbitrado, pero en el mercado la mejora de Sharpe es significativa en 2 de 10 países, es una sola muestra de los autores y no responde la pregunta del crecimiento.
  - **Qué aporta a `filtro_apalancados`:** (i) **el lugar** del umbral se parece al nuestro. En mi comprobación rápida (^VIX de Yahoo, 1990-01-02 a 2026-10-02, 9,258 días, percentil de la muestra completa, solo para ubicar), el VIX está ≥ 25 el 17.3% de los días y su p80 es 24.2. Nuestro umbral cae, por tanto, en el "quintil alto" de BKvD. Grado D, sin script versionado. (ii) **La acción no es la nuestra:** en ese régimen ellos **reducen en proporción** a σ_obj/σ̂ (por ejemplo, a 0.5x si σ̂ duplica el objetivo; el paper no reporta la distribución de pesos), no salen a cero. Su evidencia respalda condicionar el escalado a los extremos. **No** respalda el interruptor 1/0 y no lo contradice directamente, porque nunca lo prueba. Es coherente con la ficha `fichas/2026-10-04-escalado-vix-3x.md`: escalar cuesta menos crecimiento que salir. (iii) Su ganancia de MDD (−8.3 pp en 1x) es **sin** filtro de tendencia. Con la banda SMA200 ya puesta, la ganancia marginal esperada es menor, porque el targeting y la tendencia son en buena parte la misma apuesta (Hood-Raughtigan). Eso coincide con la ficha: K=22 sobre la banda no mejora la MDD. No cambia ningún criterio. Es un insumo para el comité del 9-oct.
- **Evidencia propia post-publicación (SPY en USD, exceso sobre T-bill de 3 meses, c estimado en tiempo real con ventana expansiva, 10 pb por unidad de rotación):**

| Periodo | B&H: SR / MDD | VM tope 1.0×: SR / MDD | VM sin tope: SR / MDD |
|---|---|---|---|
| mar-1998 a dic-2016 | 0.33 / −55.8% | **0.54 / −24.4%** | 0.54 / −24.4% |
| ene-2017 a ago-2026 | 0.84 / −24.7% | **0.81 / −9.9%** | 0.56 / **−46.1%** |

  Después de 2017, la ventaja en Sharpe desapareció. La reducción de drawdown se mantuvo solo **con el apalancamiento topado**. Sin tope, la estrategia se apalanca después de meses tranquilos y sufre en los choques (feb-2018, mar-2020).

### 2.5 Risk parity

- **Idea:** se iguala la contribución al riesgo de cada activo, w_i·(Σw)_i = w'Σw/N. La versión ingenua es w_i ∝ 1/σ_i. Asness-Frazzini-Pedersen (2012, FAJ) lo justifican por la *aversión al apalancamiento*: los activos seguros deben ofrecer mayor rendimiento ajustado por riesgo, y aprovecharlo requiere apalancar.
- **La falla estructural** es el supuesto de correlación acciones-bonos negativa. **Dato propio:** la correlación mensual SPY-IEF fue **−0.31** entre ago-2002 y dic-2021, y **+0.56** entre ene-2022 y ago-2026 (+0.61 solo en 2022). Brixton et al. (2023, JPM) documentan que la correlación positiva fue la norma en los 70, 80 y 90, y que la incertidumbre inflacionaria la trae de regreso.
- **Desempeño real en 2022 (cálculo propio, cierre ajustado):**

| Vehículo | 2022 | MDD 2022 | Acumulado ene-2022 a 24-sep-2026 |
|---|---|---|---|
| RPAR (ETF de risk parity) | **−22.8%** | −29.0% | **−1.4%** |
| AOR (asignación ~60/40) | −15.7% | −21.5% | +35.1% |
| SPY | −18.2% | −24.5% | +72.1% |
| TLT | −31.2% | −36.6% | −36.4% |

  ALLW (ETF All Weather de SPDR y Bridgewater, primer dato 6-mar-2025) acumula +21.9% al 24-sep-2026, contra AOR +23.4% y SPY +36.6% en el mismo lapso. La cifra de 2022 del fondo institucional All Weather queda **(no verificado)**.

### 2.6 Error de estimación y construcción robusta

- **1/N (DeMiguel-Garlappi-Uppal 2009, RFS):** evaluaron 14 modelos en 7 bases de datos, y **ninguno** le gana consistentemente a 1/N en Sharpe, equivalente cierto o rotación. Para que la media-varianza muestral supere a 1/N se necesitan **≈3,000 meses** de datos con 25 activos y **≈6,000** con 50.
- **Kan-Zhou (2007, JFQA):** con incertidumbre de parámetros conviene combinar la tangente muestral con el portafolio de mínima varianza (regla de tres fondos).
- **Shrinkage de covarianzas:** Σ̂ = δF + (1 − δ)S, con δ óptimo estimado de los datos y F un objetivo estructurado, por ejemplo correlación constante (Ledoit-Wolf 2004, JPM). La versión no lineal ajusta cada eigenvalor por separado (Ledoit-Wolf 2017, RFS; guía en J. Fin. Econometrics 20(1)).
- **Black-Litterman (1992, FAJ):** los rendimientos de equilibrio salen de optimización inversa, Π = δΣw_mkt. La posterior es E[R] = [(τΣ)⁻¹ + P'Ω⁻¹P]⁻¹[(τΣ)⁻¹Π + P'Ω⁻¹Q]. Así las opiniones con confianza Ω se incorporan sin soluciones de esquina.
- **HRP (López de Prado 2016, JPM):** (1) agrupamiento jerárquico con distancia d_ij = √((1 − ρ_ij)/2); (2) cuasi-diagonalización; (3) bisección recursiva con pesos de varianza inversa. No invierte Σ.
  - *Evidencia posterior:* Trucíos (2026, Empirical Economics) no encuentra evidencia de que HRP supere a los métodos de riesgo tradicionales fuera de muestra, y lo ve sensible al estimador de covarianza. En Brasil, Reis et al. (2023) ven desempeño comparable, no superior.
- **Trading dinámico con costos (Gârleanu-Pedersen 2013, JF):** se apunta *delante* del objetivo y se opera solo *parcialmente* hacia él. Las señales que decaen lento pesan más.

### 2.7 Medidas de riesgo

- **VaR_α:** es el cuantil de la pérdida. No es **coherente**, porque no cumple la subaditividad (Artzner-Delbaen-Eber-Heath 1999). Ignora el tamaño de la cola.
- **ES/CVaR_α:** es la pérdida esperada dado que se rebasa el VaR. Rockafellar-Uryasev (2000, 2002) la reescriben como CVaR_α = min_ζ {ζ + (1/(1 − α))·E[(L − ζ)⁺]}, que con escenarios es un programa lineal.
  - Basilea (BCBS, estándar de mercado de ene-2016 y ene-2019) cambió el VaR por un ES bajo estrés en el enfoque de modelos internos. El nivel de 97.5% queda **(no verificado en fuente primaria en esta sesión)**.
- **Drawdown:** DD_t = 1 − W_t/max_{s≤t} W_s. La recuperación necesaria es 1/(1 − DD) − 1: −12% pide +13.6%; −20% pide +25%; −35% pide +53.8%; −50% pide +100%.
  - Sin deriva, E[MDD] = √(π/2)·σ√T ≈ 1.25σ√T (Magdon-Ismail et al. 2004). Mi simulación da 1.21 con 1,000 pasos; la discretización sesga el resultado hacia abajo.
- **CDaR** (Chekhlov-Uryasev-Zabarankin 2005): es el CVaR de la distribución de drawdowns. Se optimiza como programa lineal.
- **Grossman-Zhou (1993):** con la restricción W_t ≥ α·M_t (M_t = máximo histórico), lo óptimo es invertir en riesgo en proporción al colchón W_t − α·M_t. Es un CPPI con piso que sube con cada máximo.
  - *Inferencia:* los cortacircuitos escalonados de `parametros.json` son una aproximación discreta de esta política.

### 2.8 Stop-loss

- **Kaminski-Lo (2014, J. Financial Markets):** proponen un marco analítico para medir cuánto suma o resta un stop-loss al rendimiento esperado y a la volatilidad. Con futuros de índices y a frecuencias largas, algunas políticas **suben el rendimiento esperado y bajan mucho la volatilidad**.
- *Derivación e inferencia:* si el rendimiento es una caminata aleatoria sin memoria y el activo tiene prima positiva, salir al tocar el stop te pasa a un activo de menor rendimiento esperado sin ganar poder predictivo. El rendimiento esperado **baja**. El stop agrega valor solo si hay persistencia (momentum, cambio de régimen). Xiang-Deng (2024, QF) formalizan esto: con memoria larga (Hurst > 0.5) el stop da prima positiva.
- En momentum, el stop-loss recorta los crashes (Han-Zhou-Zhu, SSRN; cifras **no verificadas**). Sadaqat-Butt-Demirer (2026, SSRN, sin arbitraje) reportan 2.8% a 5.3% **mensual** en 5 mercados asiáticos.
  - *Inferencia:* cifras de ese tamaño son implausibles netas de costos. Se tratan como hipótesis, grado D.

### 2.9 Colas gruesas y correlaciones en crisis

- **Hechos estilizados** (Cont 2001, QF): colas gruesas, agrupamiento de volatilidad, asimetría ganancia/pérdida y *leverage effect*.
- **Dato propio (SPY diario, 29-ene-1993 a 24-sep-2026, n = 8,470):**
  - La curtosis es **14.8**.
  - Hubo **54 días más allá de 4σ**; una normal esperaría 0.54. Hubo **25 más allá de 5σ**; una normal esperaría 0.005.
  - El VaR 99% histórico es 3.20%, contra 2.67% bajo normalidad.
  - El ES 97.5% histórico es 3.50%, contra 2.68% bajo normalidad.
  - Peor día: −10.94% (16-mar-2020). MDD: −55.2% (mar-2009).
- **Correlaciones en crisis:**
  - Longin-Solnik (2001, JF): con teoría de valores extremos, la correlación internacional sube en mercados bajistas, no en alcistas.
  - Ang-Chen (2002, JFE): las correlaciones con el mercado son mayores a la baja.
  - Consecuencia: la diversificación medida con Σ de tiempos normales sobrestima la protección justo cuando hace falta.

### 2.10 Estadística del backtest

- **Error estándar del Sharpe** (Lo 2002, FAJ): con rendimientos iid, SE(SR) = √((1 + SR²/2)/T), con T en las mismas unidades que el SR.
  - Con SR anual 1.0 y 5 años de datos, SE ≈ 0.55.
  - Con autocorrelación, el SR anual de un hedge fund puede estar inflado hasta 65%, y la regla √12 deja de ser válida.
- **PSR** (Bailey-López de Prado 2012): PSR(SR*) = Φ[(SR − SR*)√(T − 1)/√(1 − γ₃SR + (γ₄ − 1)/4·SR²)], con γ₃ = asimetría y γ₄ = curtosis cruda.
  - **MinTRL** = 1 + (1 − γ₃SR + (γ₄ − 1)/4·SR²)·(z_α/(SR − SR*))².
  - **Cálculo propio** con rendimientos normales, 95% y SR* = 0: SR 0.5 → 11.0 años; 0.7 → 5.7 años; 1.0 → 2.9 años; 2.0 → 0.9 años.
  - Con datos diarios, **seis meses (~126 días) prueban habilidad solo si el SR anual es ≥ ~2.3**.
- **DSR** (Bailey-López de Prado 2014, JPM): es el PSR evaluado en SR₀ = √V·[(1 − γ)Φ⁻¹(1 − 1/N) + γΦ⁻¹(1 − 1/(Ne))], el máximo Sharpe esperado entre N pruebas sin habilidad (γ = 0.5772).
  - **Ejemplo del paper, reproducido con `metricas.dsr_desde_estadisticos`:** SR anual 2.5, T = 1,250 días, N = 100, V[SR] = 0.5, asimetría −3, curtosis 10. Da SR₀ anual = 1.79 y **DSR = 0.900**, que no es significativo al 95%. Con N = 46 da 0.9505. Con rendimientos normales, el umbral se alcanza hasta N = 88.
- **MinBTL** (Bailey-Borwein-López de Prado-Zhu 2014, Notices AMS): con 5 años de datos, **no más de 45 configuraciones independientes**; si no, se obtiene casi con seguridad un SR IS de 1 con SR OOS esperado de 0. Con 2 años, basta con 7 pruebas. *Comprobado el 2026-09-29 (`fichas/2026-09-29-dsr-minbtl.md`): N = 45 → 5.00 años, N = 7 → 1.92 años (SR objetivo 1, V = 1). La fórmula de E[max] sobrestima el Monte Carlo en 1-3%, del lado conservador.*
- **PBO/CSCV** (Bailey et al., J. Computational Finance): se parte la matriz de desempeño en S bloques y se forman todas las combinaciones de mitades IS/OOS. En cada una se ve el rango OOS de la mejor estrategia IS, con logit λ = ln(ω/(1 − ω)). **PBO = P(λ ≤ 0)**, es decir, la frecuencia con que la ganadora IS queda por debajo de la mediana OOS.
- **Haircut de Harvey-Liu (2015, JPM):** el 50% fijo "es un error serio". El castigo **no es lineal**: casi siempre supera 50% cuando el SR anual es < 0.4, y es de 25% como máximo cuando SR > 1.0. Harvey-Liu-Zhu (2016, RFS) documentan ≥ 316 factores probados y piden **t > 3.0** para un factor nuevo.
- **Validación cruzada financiera** (López de Prado 2018, AFML):
  - *Purging:* quitar del entrenamiento las observaciones cuyas etiquetas se traslapan con el periodo de prueba.
  - *Embargo:* excluir un tramo posterior a cada bloque de prueba.
  - **CPCV:** genera múltiples trayectorias OOS.
  - Arian-Norouzi-Seco (2024, Knowledge-Based Systems), en un entorno sintético controlado: CPCV da menor PBO y mejor estadístico DSR. **Walk-forward** muestra debilidades notables para prevenir falsos descubrimientos.
- **Comparar dos Sharpe:** Ledoit-Wolf (2008, JEF) proponen pruebas robustas (HAC o bootstrap) de la diferencia de Sharpe. Suponer iid es incorrecto.
- **Nuevo estándar:** López de Prado, Lipton y Zoonekynd (2026, JPM 52(6)) derivan una distribución en forma cerrada del SR con rendimientos no normales y autocorrelacionados. Enumeran 5 errores:
  1. Reportar el punto sin significancia.
  2. Suponer iid normal.
  3. Ignorar la potencia de la prueba y la longitud mínima.
  4. Leer el p-value como la probabilidad de que H₀ sea cierta.
  5. No corregir por pruebas múltiples.

### 2.11 Sesgos, costos, capacidad y decaimiento

- **Supervivencia:** los fondos desaparecen por mal desempeño (Elton-Gruber-Blake 1996, RFS). Un universo "S&P 500 actual" hacia atrás mete sesgo.
- **Look-ahead:** hay que usar datos *point-in-time*, rezagar la señal al menos 1 periodo (`backtest.con_rezago`) y rezagar los contables hasta su fecha de publicación. En pesos, el tipo de cambio debe ser el disponible en ese momento.
- **Costos:** Novy-Marx-Velikov (2016, RFS) encuentran que la mayoría de las anomalías con **< 50% de rotación mensual** conserva spreads netos significativos si se diseñan para mitigar costos, y pocas con más rotación. La técnica más eficaz es un buy/hold spread, con umbral de entrada más exigente que el de permanencia.
- **Decaimiento:** McLean-Pontiff (2016, JF) estudian 97 predictores. Rinden **26% menos fuera de muestra** y **58% menos después de publicarse**.
- **Replicación:**
  - Hou-Xue-Zhang (2020, RFS): 65% de 452 anomalías no pasan |t| ≥ 1.96, y 82% no pasan con 2.78.
  - Jensen-Kelly-Pedersen (2023, JF), con un enfoque bayesiano: la mayoría de los factores sí se replica, se agrupa en 13 temas y funciona fuera de muestra en 93 países.
  - La discrepancia depende del método y de los microcaps.
- **Cripto:** Nefedov (2026, SSRN) encuentra que la evaluación ingenua infla el Sharpe **3.6×** en promedio. Con protocolo riguroso, ninguno de 6 factores sobrevive la deflación y 4 quedan con Sharpe OOS negativo, sobre todo por fricciones.

### 2.12 Rebalanceo e impuestos
- **Perold y Sharpe (1988, FAJ), "Dynamic Strategies for Asset Allocation"** (adenda del examen 2026-10, grado A como resultado teórico):
  - Comprar y mantener paga de forma **lineal**.
  - La mezcla constante paga de forma **cóncava**: compra al bajar y vende al subir, lo que equivale a vender opciones. Gana en mercados que oscilan o revierten y pierde con tendencia.
  - CPPI paga de forma **convexa**: compra al subir, lo que equivale a comprar un put. Gana con tendencia y pierde en mercados laterales.
  - Lo que una estrategia convexa gana, alguien con estrategia cóncava lo paga.
  - Conexión con el sistema: el rebalanceo por bandas es mezcla constante (cóncavo); los filtros de tendencia y los cortacircuitos son convexos (R06, AC-07, AC-09).

- **Teoría:** Davis-Norman (1990) muestran que, con costos proporcionales, la política óptima es una **región de no-transacción** en forma de cuña. Solo se opera en sus fronteras, es decir, se lleva la posición **al borde** de la banda y no al objetivo.
- **Práctica:**
  - Zhang-Ahluwalia-Daga-Zi (2025, JPM) proponen un rebalanceo por umbral óptimo que equilibra costos y desviación, y lo comparan con rebalanceo mensual y trimestral.
  - Bai et al. (2025, FMPM): agregar bandas a un target-volatility reduce costos sin perder el control de riesgo.
- **Cosecha de pérdidas fiscales:**
  - En EUA, de 1926 a 2018, rinde **1.08% anual** antes de costos, y **0.82%** con la regla *wash sale* (Chaudhuri-Burnham-Lo 2020, FAJ; tasas de 15% y 35%).
  - **México (art. 129 LISR, texto con última reforma del DOF del 01-04-2024):** la ganancia en bolsa concesionada paga **10% definitivo**. Esto incluye acciones extranjeras cotizadas en esas bolsas (SIC) y títulos referenciados a índices. La ganancia se calcula por emisora con **costo promedio** de adquisición actualizado. La pérdida del ejercicio solo se disminuye contra ganancias de la misma sección **en el ejercicio o en los diez siguientes**.
  - *Inferencia:* con tasa de 10% y costo promedio (no por lote), el valor de la cosecha es menor que en EUA. No localicé en el art. 129 una regla *wash sale* equivalente; si otras disposiciones aplican queda **(no verificado)**.

---

## 3. Literatura canónica

| Autores | Año | Título | Revista/Editorial | Hallazgo clave cuantificado | Enlace/DOI | Grado |
|---|---|---|---|---|---|---|
| Kelly | 1956 | A New Interpretation of Information Rate | Bell System Tech. J. 35, 917-926 | Apostar f* maximiza la tasa de crecimiento del capital | 10.1002/j.1538-7305.1956.tb03809.x | A (matemática) |
| Thorp | 2008 | The Kelly criterion in blackjack, sports betting and the stock market | Handbook of Asset & Liability Mgmt., Elsevier, 385-428 | f* = (μ − r)/σ²; aplicación a acciones | 10.1016/B978-044453248-0.50015-0 | A/B |
| MacLean, Thorp, Ziemba | 2010 | Long-term capital growth: the good and bad properties of the Kelly and fractional Kelly… | Quantitative Finance 10(7), 681-687 | Kelly maximiza el crecimiento límite; el fraccional cambia crecimiento por seguridad | 10.1080/14697688.2010.506108 | A |
| Baker, McHale | 2013 | Optimal Betting Under Parameter Uncertainty: Improving the Kelly Criterion | Decision Analysis 10(3), 189-199 | Encoger la apuesta mejora el desempeño OOS | 10.1287/deca.2013.0271 | B |
| Busseti, Ryu, Boyd | 2016 | Risk-Constrained Kelly Gambling | J. of Investing 25(3), 118-134 | Kelly convexo con restricción de drawdown; supera al fraccional con el mismo riesgo | 10.3905/joi.2016.25.3.118 | B |
| Moreira, Muir | 2017 | Volatility-Managed Portfolios | J. of Finance 72(4), 1611-1644 | Mercado: α 4.86%/año, Sharpe +25% (1926-2015, IS) | 10.1111/jofi.12513 | C |
| Cederburg, O'Doherty, Wang, Yan | 2020 | On the performance of volatility-managed portfolios | JFE 138(1), 95-117 | 103 estrategias: no superan OOS a las originales | 10.1016/j.jfineco.2020.04.015 | A/B |
| Barroso, Detzel | 2021 | Do limits to arbitrage explain the benefits of volatility-managed portfolios? | JFE 140(3), 744-767 | Netas de costos solo sobrevive la del mercado | 10.1016/j.jfineco.2021.02.009 | B |
| Harvey et al. | 2018 | The Impact of Volatility Targeting | JPM 45(1), 14-33 | Sharpe ↑ solo en acciones y crédito; colas ↓ en todas las clases | 10.3905/jpm.2018.45.1.014 | B |
| Asness, Frazzini, Pedersen | 2012 | Leverage Aversion and Risk Parity | FAJ 68(1), 47-59 | Los activos seguros pagan más por unidad de riesgo; RP los apalanca | 10.2469/faj.v68.n1.1 | B |
| DeMiguel, Garlappi, Uppal | 2009 | Optimal Versus Naive Diversification: How Inefficient is the 1/N…? | RFS 22(5), 1915-1953 | 0 de 14 modelos le ganan a 1/N; se necesitan ~3,000 meses con 25 activos | 10.1093/rfs/hhm075 | A |
| Kan, Zhou | 2007 | Optimal Portfolio Choice with Parameter Uncertainty | JFQA 42(3), 621-656 | Regla de tres fondos | 10.1017/S0022109000004129 | A |
| Ledoit, Wolf | 2004 | Honey, I Shrunk the Sample Covariance Matrix | JPM 30(4), 110-119 | Shrinkage hacia correlación constante | 10.3905/jpm.2004.110 | A |
| Ledoit, Wolf | 2017 | Nonlinear Shrinkage… Markowitz Meets Goldilocks | RFS 30(12), 4349-4388 | Shrinkage no lineal para portafolios grandes | 10.1093/rfs/hhx052 | A |
| Black, Litterman | 1992 | Global Portfolio Optimization | FAJ 48(5), 28-43 | Equilibrio más opiniones; evita soluciones de esquina | 10.2469/faj.v48.n5.28 | B |
| López de Prado | 2016 | Building Diversified Portfolios that Outperform Out of Sample | JPM 42(4), 59-69 | HRP sin invertir Σ (evidencia Monte Carlo del autor) | 10.3905/jpm.2016.42.4.059 | C |
| Gârleanu, Pedersen | 2013 | Dynamic Trading with Predictable Returns and Transaction Costs | JF 68(6), 2309-2340 | "Apunta delante del objetivo, opera parcialmente" | 10.1111/jofi.12080 | A/B |
| Artzner, Delbaen, Eber, Heath | 1999 | Coherent Measures of Risk | Mathematical Finance 9(3), 203-228 | Axiomas de coherencia; el VaR no es subaditivo | 10.1111/1467-9965.00068 | A |
| Rockafellar, Uryasev | 2000 / 2002 | Optimization of CVaR / CVaR for general loss distributions | J. of Risk 2(3), 21-41 / JBF 26(7), 1443-1471 | El CVaR se optimiza como programa lineal | 10.21314/JOR.2000.038 | A |
| Chekhlov, Uryasev, Zabarankin | 2005 | Drawdown Measure in Portfolio Optimization | IJTAF 8(1), 13-58 | CDaR | 10.1142/S0219024905002767 | B |
| Grossman, Zhou | 1993 | Optimal Investment Strategies for Controlling Drawdowns | Mathematical Finance 3(3), 241-276 | Exposición ∝ colchón sobre α·máximo | 10.1111/j.1467-9965.1993.tb00044.x | A (teoría) |
| Magdon-Ismail, Atiya, Pratap, Abu-Mostafa | 2004 | On the maximum drawdown of a Brownian motion | J. Applied Probability 41(1), 147-161 | Sin deriva: E[MDD] ≈ 1.25σ√T | 10.1017/S0021900200014108 | A |
| Kaminski, Lo | 2014 | When do stop-loss rules stop losses? | J. Financial Markets 18, 234-254 | Frecuencias largas: rendimiento ↑ y volatilidad ↓ con algunos stops | 10.1016/j.finmar.2013.07.001 | B |
| Longin, Solnik | 2001 | Extreme Correlation of International Equity Markets | JF 56(2), 649-676 | La correlación sube en mercados bajistas | 10.1111/0022-1082.00340 | A |
| Ang, Chen | 2002 | Asymmetric correlations of equity portfolios | JFE 63(3), 443-494 | La correlación es mayor a la baja | 10.1016/S0304-405X(02)00068-5 | A |
| Cont | 2001 | Empirical properties of asset returns: stylized facts… | Quantitative Finance 1(2), 223-236 | Colas gruesas y agrupamiento de volatilidad | 10.1080/713665670 | A |
| Lo | 2002 | The Statistics of Sharpe Ratios | FAJ 58(4), 36-52 | SE = √((1 + SR²/2)/T); SR inflado hasta 65% por autocorrelación | 10.2469/faj.v58.n4.2453 | A |
| Bailey, López de Prado | 2012 | The Sharpe Ratio Efficient Frontier | J. of Risk 15(2), 3-44 | PSR y MinTRL | 10.21314/JOR.2012.255 | A |
| Bailey, López de Prado | 2014 | The Deflated Sharpe Ratio | JPM 40(5), 94-107 | Ejemplo: SR 2.5 con N = 100 → DSR 0.90 | 10.3905/jpm.2014.40.5.094 | A |
| Bailey, Borwein, López de Prado, Zhu | 2014 | Pseudo-Mathematics and Financial Charlatanism | Notices AMS 61(5), 458- | 5 años de datos → ≤ 45 pruebas | 10.1090/noti1105 | A |
| Bailey, Borwein, López de Prado, Zhu | 2016-17 | The Probability of Backtest Overfitting | J. Computational Finance (vol./págs. no verificados) | PBO por CSCV | 10.21314/JCF.2016.322 | B |
| Harvey, Liu | 2015 | Backtesting | JPM 42(1), 13-28 | Haircut no lineal: > 50% si SR < 0.4; ≤ 25% si SR > 1 | 10.3905/jpm.2015.42.1.013 | A/B |
| Harvey, Liu, Zhu | 2016 | …and the Cross-Section of Expected Returns | RFS 29(1), 5-68 | ≥ 316 factores; umbral t > 3.0 | 10.1093/rfs/hhv059 | A |
| López de Prado | 2018 | Advances in Financial Machine Learning | Wiley | Purged k-fold, embargo, CPCV | reseña: 10.1080/14697688.2019.1703030 | B |
| Arnott, Harvey, Markowitz | 2019 | A Backtesting Protocol in the Era of Machine Learning | J. Financial Data Science 1(1), 64-74 | Protocolo y lista de verificación | 10.3905/jfds.2019.1.064 | B |
| Ledoit, Wolf | 2008 | Robust performance hypothesis testing with the Sharpe ratio | J. Empirical Finance 15(5), 850-859 | Prueba robusta de la diferencia de Sharpe | 10.1016/j.jempfin.2008.03.002 | A |
| McLean, Pontiff | 2016 | Does Academic Research Destroy Stock Return Predictability? | JF 71(1), 5-32 | −26% OOS; −58% post-publicación | 10.1111/jofi.12365 | A |
| Hou, Xue, Zhang | 2020 | Replicating Anomalies | RFS 33(5), 2019-2133 | 65% de 452 fallan con t de 1.96; 82% con 2.78 | 10.1093/rfs/hhy131 | A |
| Novy-Marx, Velikov | 2016 | A Taxonomy of Anomalies and Their Trading Costs | RFS 29(1), 104-147 | < 50% de rotación mensual sobrevive neto | 10.1093/rfs/hhv063 | A |
| Elton, Gruber, Blake | 1996 | Survivor Bias and Mutual Fund Performance | RFS 9(4), 1097-1120 | Estimación precisa del sesgo de supervivencia | 10.1093/rfs/9.4.1097 | A |
| Davis, Norman | 1990 | Portfolio Selection with Transaction Costs | Math. of Operations Research 15(4), 676-713 | Región de no-transacción en cuña | 10.1287/moor.15.4.676 | A (teoría) |
| Avellaneda, Zhang | 2010 | Path-Dependence of Leveraged ETF Returns | SIAM J. Financial Math. 1(1), 586-603 | El rendimiento depende de la trayectoria y de la varianza realizada | 10.1137/090760805 | A |
| Chaudhuri, Burnham, Lo | 2020 | An Empirical Evaluation of Tax-Loss-Harvesting Alpha | FAJ 76(3), 99-108 | 1.08%/año (0.82% con wash sale), antes de costos, EUA | 10.1080/0015198X.2020.1760064 | B |
| Brown, Harlow, Starks | 1996 | Of Tournaments and Temptations | JF 51(1), 85-110 | Los que van perdiendo a mitad de año suben el riesgo | 10.1111/j.1540-6261.1996.tb05203.x | B |
| Dachraoui | 2018 | On the Optimality of Target Volatility Strategies | JPM 44(5), 58-67 | Condición necesaria y suficiente: el *target volatility* mejora si la covarianza entre volatilidad y rendimiento ajustado por riesgo es negativa. Cifras de segunda mano: S&P 500 1990-2015, Sharpe 0.34 contra 0.30 (adenda 2026-10-05) [solo abstract] | 10.3905/jpm.2018.44.5.058 | C (condición) / D (cifras) |
| Liu, Tang, Zhou | 2019 | Volatility-Managed Portfolio: Does It Really Work? | JPM 46(1), 38-51 | La versión de Moreira-Muir aplicada al mercado tiene *look-ahead*. Corregida, la MDD es de 68% a 93% y solo gana en la crisis de 2008 (adenda 2026-10-05) [solo abstract] | 10.3905/jpm.2019.1.107 | C |
| Wang, Yan | 2021 | Downside risk and the performance of volatility-managed portfolios | J. Banking & Finance 131, 106198 | Escalar con semivolatilidad supera a escalar con volatilidad total: en tiempo real gana en 70 de 103 estrategias contra 50. En el **mercado**, Sharpe de 0.46 contra 0.51, sin significancia (adenda 2026-10-05) | 10.1016/j.jbankfin.2021.106198 | B |

---

## 4. Lo más reciente 2023-2026

| Fecha | Trabajo | Qué aporta | Estado |
|---|---|---|---|
| 2023 (JPM 49(4)) | Brixton, Brooks, Hecht, Ilmanen, Maloney, McQuinn, *A Changing Stock-Bond Correlation* | La correlación acciones-bonos negativa de 2000-2020 es la excepción; la incertidumbre inflacionaria la vuelve positiva | Publicado |
| jun-2023 (JF 78(5)) | Jensen, Kelly, Pedersen, *Is There a Replication Crisis in Finance?* | La mayoría de los factores se replica; 13 temas; 93 países | Publicado |
| 2024 (JF 79(6), 3859-3891) | DeMiguel, Martín-Utrera, Uppal, *A Multifactor Perspective on Volatility-Managed Portfolios* | Un portafolio multifactor condicional supera al incondicional **fuera de muestra y neto de costos**; los precios de riesgo de los factores bajan cuando sube la volatilidad | Publicado; un solo estudio → C |
| 2024 (JPM 50) | Filho, Gaspar, *On Risk Parity Performance* | 1990-2019, 5 clases de activos: algunos RP ganan en ajuste por riesgo, pero no en horizontes de 10-20 años; robusto a costos | Publicado |
| 2024 (KBS 305, 112477) | Arian, Norouzi Mobarekeh, Seco, *Backtest overfitting in the ML era* | CPCV > purged k-fold ≈ k-fold > walk-forward en PBO y DSR (sintético) | Publicado |
| 2024 (QF 24, 253-263) | Xiang, Deng, *Optimal stop-loss rules in markets with long-range dependence* | El stop tiene prima positiva solo con memoria larga (Hurst) | Publicado |
| 2025 (JPM 51(9)) | Zhang, Ahluwalia, Daga, Zi, *Optimizing TDF Rebalancing through Threshold-Based Strategies* | Umbral óptimo que equilibra costo y desviación, frente a rebalanceo mensual y trimestral | Publicado |
| 2025 (FMPM 40) | Bai, Pachamanova, Steblovskaya, Wallbaum | Bandas en target-volatility: menos costos, mismo control | Publicado |
| 2025 (JRFM 19, 20) | Trainor, *Beyond Volatility Decay* | El método estándar de los proveedores para estimar el rendimiento esperado de los LETF se desvía mucho | Publicado; revista de menor rango → C |
| 2026 (JPM 52(6), 6-50) | López de Prado, Lipton, Zoonekynd, *Sharpe Ratio Inference: A New Standard…* | Distribución cerrada del SR no normal y autocorrelacionado; 5 errores comunes | Publicado; **frontera** |
| 2024 (IRFA 95, 103353) | Božović, *VIX-managed portfolios* | Escalar con 1/VIX² en tiempo real: α de MKT 3.07% (t ≈ 2.1), ΔSharpe +0.10 no significativo; menos rotación que con la RV, punto de equilibrio de 91 pb (§2.4, nota 2026-10-03) | Publicado; revista de rango medio, sin réplica → C |
| 2020 (FAJ 76(4), 54-71; doi:10.1080/0015198X.2020.1790853; anterior al periodo, se incluye por pertinencia) | Bongaerts, Kang, van Dijk, *Conditional Volatility Targeting* | Escalar con σ_obj/σ̂ **solo** en el quintil extremo de volatilidad (1x en el resto): mercado de EUA 1982-2019, +0.16 de Sharpe (5%) y −8.3 pp de MDD con giro de 1.6 al año. En el promedio de 10 mercados, +0.07 de Sharpe (significativo solo en 2) y −6.6 pp de MDD. Reduce en proporción, **no** sale a cero, y no reporta CAGR (§2.4, nota 2026-10-04) | Publicado y arbitrado; leído íntegro (acceso abierto); sin réplica → C |
| 2026 (CFR 15, 179-207) | Xu, *Improving volatility-managed portfolios in real time* | 197 factores: 148 suben el Sharpe y 165 dan alfa positivo en tiempo real; robusto a costos y apalancamiento | Publicado → C (contradice a Cederburg; pendiente de replicar) |
| jul-2026 (Annals of Finance 22(2); doi:10.1007/s10436-026-00487-y; CC BY 4.0) | Bermin, *Kelly trading and expected utility* | Teoría en tiempo continuo con oportunidades estocásticas: la estrategia óptima de utilidad potencia **no** es Kelly en general, porque agrega una cobertura intertemporal contra cambios del Sharpe máximo. Bajo condiciones de colinealidad o diagonales, cada componente es un **escalamiento** del componente Kelly, lo que da un fundamento al Kelly fraccional. El ajuste puede no ser pequeño con varios activos, y la aversión al riesgo implícita puede depender del horizonte | Publicado; teórico, sin datos. Leído solo el resumen (Crossref, 2026-09-25) → B. Añadido el 2026-09-25 (ficha `fichas/2026-09-25-kelly-fraccional.md`) |
| sep-2026 (arXiv:2609.29530 [cs.LG; q-fin.ST], 2-sep) | Li, *The Impossible Trinity of Time-Series Validation* | Demuestra α + β ≤ 1 + Λ: ningún esquema de validación temporal logra a la vez fracción de entrenamiento suficiente (α), cobertura de prueba (β) y causalidad (Λ = fuga de datos futuros). Walk-forward es la frontera de Pareto causal; k-fold maximiza el uso de datos futuros; purged k-fold con embargo cambia cantidad por distancia. Sobre ruido puro, el 5-fold barajado da IC = +0.32 y el 5-fold contiguo +0.004 | Preprint teórico. Leído solo el resumen (arxiv.org, 28-sep-2026) → C. **Confirma** las reglas de este capítulo (walk-forward o CPCV; nunca validación barajada en series de tiempo); no cambia ningún criterio. Añadido el 2026-09-28 (laboratorio) |
| may-2025 (J. of Financial Research 49(1), 286-325; doi:10.1111/jfir.12466) | Chrétien, Coggins, Deslauriers, *Tournament effects in equity mutual funds: Impact of economic conditions and investment styles* | Con medidas tradicionales aparece una "respuesta racional" de los fondos ganadores, que también suben su riesgo. Al controlar por variaciones de estilo, los efectos se debilitan mucho y queda sobre todo **el aumento de riesgo de los perdedores** | Publicado. Leído solo el resumen (Crossref, 29-sep-2026) → B. Matiza a Brown-Harlow-Starks y **respalda R11** (modo torneo acotado por cortacircuitos): la conducta documentada es la del que va perdiendo. Añadido el 2026-09-29 (laboratorio) |
| 2026 (Empirical Economics 70) | Trucíos, *Hierarchical risk clustering versus traditional risk-based portfolios* | Sin evidencia de que HRP supere a los métodos de riesgo tradicionales OOS | Publicado |
| 2026 (SSRN) | Nefedov, *How Much Sharpe is Illusory?* | Cripto: el protocolo ingenuo infla el SR 3.6×; ningún factor sobrevive | WP → C |
| 2026 (SSRN) | Sadaqat, Butt, Demirer | Stop-loss en momentum asiático: 2.8% a 5.3% mensual | WP → D |
| 2022-2026 (datos propios) | RPAR, ALLW, LETF, correlación SPY-IEF, VM SPY después de publicación | Ver §2.1, §2.4 y §2.5 | Cálculo reproducible |
| sep-2026 (JFE 185, 104364; doi:10.1016/j.jfineco.2026.104364) | Laarits, *Discounting timing strategies* | 39 estrategias de *timing*: el Sharpe promedio baja de 0.57 a 1 mes a 0.38 a 10 años y el alfa FF4 de 5.5% a 2.1%. En el mercado gestionado por volatilidad, el alfa CAPM baja de 4.63% a 1.25% (adenda 2026-10-05) | Publicado; leída la versión del autor (may-2026) → B |
| sep-2026 (arXiv 2609.07946 [q-fin.PM]) | Devanathan, Tzikas, Boyd, *Simple Dynamic Stock/Bond/Gold Portfolios* | 2006-2026, con costos de 5 pb: el 60/40 con control de volatilidad al 7% sube el Sharpe de 0.56 a 0.71, baja la MDD de 33.7% a 16.9% y deja el rendimiento de 8.1% en 7.1% (adenda 2026-10-05) | Preprint; leído íntegro → C |
| abr-2025 (arXiv 2504.20116 [q-fin.ST]; anterior al periodo, venía en la cola) | Hsieh, Chang, Chen, *Compounding Effects in Leveraged ETFs* | El efecto compuesto **esperado** (aritmético) de un LETF depende de la autocorrelación, no solo del *drag*: favorece al 3x con tendencia y lo castiga con reversión (adenda 2026-10-05) | Preprint; leído íntegro → C |
| oct-2026 (arXiv 2610.01115 [stat.ME]) | Bonacorsi, *Certified Alpha Capacity* | Una señal con Sharpe anual de 1 necesita una vida media de ≥ 11.9 años para certificarse al 5% con potencia de 90% (adenda 2026-10-05) | Preprint de un solo autor; leído (secciones 1-3, 5, 6.3, 7 y 9) → D |
| sep-2026 (SSRN 7542498) | Strahle, *How Does Reducing Exposure During Drawdowns Impact Portfolio Performance?* | SPY 2000-2025: las tres reglas bajan la MDD (con media móvil, de −55.2% a −22.0%) y el CAGR (de 8.03% a 5.27%-7.41%). Ninguna mejora el Sharpe (adenda 2026-10-05) | WP; [solo abstract] → D |

### Adenda 2026-10-05 (barrido trimestral 2026-Q4)

Se agregan cinco trabajos de la cola de las corridas vespertinas y dos del trimestre. **Acceso:** SSRN devolvió 403 todo el barrido, y los PDF de NBER del trimestre piden suscripción. Por eso se buscaron versiones de los autores y se marca **[solo abstract]** lo que no se leyó completo.

**1. Wang, Feifei y Xuemin (Sterling) Yan (2021), "Downside risk and the performance of volatility-managed portfolios", *Journal of Banking & Finance* 131, 106198. doi:10.1016/j.jbankfin.2021.106198.**
- **Tipo y acceso:** publicado y arbitrado. Se leyó íntegro el PDF publicado (18 págs.) en el sitio del autor: https://www.lehigh.edu/~xuy219/research/Downside.pdf
- **Muestra:** 9 factores (MKT, SMB y HML desde ago-1926) y 94 anomalías, hasta dic-2018.
- **Método:** el escalamiento usa la **semivolatilidad** (solo los días negativos del mes) en vez de la volatilidad total. Se evalúa de tres formas: *spanning*, Sharpe directo y estrategias en tiempo real como las de Cederburg et al. (entrenamiento de 120 meses con ventana expansiva, γ = 5 y |w| ≤ 5). Costos de 1 a 50 pb.
- **Hallazgos:**
  - *Spanning*, MKT: α = 3.34% anual (t 3.39) con volatilidad total y **4.83% (t 4.10)** con semivolatilidad.
  - Tiempo real con pesos estimados: la combinación gana al original en **50 de 103** estrategias con volatilidad total y en **70 de 103** con semivolatilidad (prueba binomial, p < 1%).
  - **MKT en tiempo real (tabla 7):** Sharpe de 0.46 sin gestionar, 0.48 con volatilidad total y 0.51 con semivolatilidad. Las diferencias **no son significativas** (p 0.76 y 0.63).
  - **Pesos fijos (tabla 9):** con 25% gestionado y 75% sin gestionar, el Sharpe de MKT sube **+0.05 (p 0.03)** con semivolatilidad y +0.03 (p 0.14) con volatilidad total. En las 94 anomalías, la semivolatilidad con pesos fijos da 72 diferencias positivas (29 significativas) contra 22 negativas.
  - Con costos de 25-50 pb, la mayoría de los α de *spanning* de los factores se vuelve negativa con volatilidad total.
- **Limitaciones:**
  - Las pruebas en tiempo real **no** descuentan costos y permiten apalancamiento de hasta 5x.
  - La mejora viene del *return timing*: la semivolatilidad predice rendimientos con signo negativo. Esa es justo la parte que Cederburg et al. encuentran inestable.
  - No se localizó una réplica independiente para el mercado. Mao et al. (EFMA 2025) extienden el resultado; no se leyó.
- **Grado B.**
- **Qué cambia:** ningún criterio. Para el **mercado**, la ganancia en tiempo real es de +0.05 de Sharpe como máximo, así que "freno, no alfa" sigue en pie (R05 y AC-06). Quedan dos insumos para el comité del 9-oct:
  - (a) si se mide el régimen con volatilidad realizada, la semivolatilidad es la variante con mejor evidencia;
  - (b) mezclar en proporción fija una parte gestionada y una sin gestionar es más robusto que optimizar el peso. Eso equivale a **escalar parcialmente**, como en la ficha `fichas/2026-10-04-escalado-vix-3x.md`, y no a un interruptor 1/0.
- Con esto queda verificado el pendiente de §9 ("hallazgo no leído").

**2. Liu, Fang, Xiaoxiao Tang y Guofu Zhou (2019), "Volatility-Managed Portfolio: Does It Really Work?", *Journal of Portfolio Management* 46(1), 38-51. doi:10.3905/jpm.2019.1.107. [solo abstract]**
- **Acceso:** abstract y "Key Findings" vía Semantic Scholar. La vista previa de ProQuest solo trae metadatos y el WP (SSRN 3283395) dio 403.
- **Qué dice:** la aplicación típica al mercado (Moreira-Muir) tiene sesgo de *look-ahead*, porque la constante de escala usa toda la muestra. Corregido ese sesgo, la **MDD es de 68% a 93%** "en casi todos los casos", y la estrategia solo le gana al mercado en la crisis de 2008. Tres variantes alternativas tampoco le ganan. Wang-Yan (leído) lo citan en el mismo sentido.
- **Grado C:** revista de practicantes y sin lectura íntegra.
- **Qué cambia:** nada. Confirma la tabla propia de §2.4 (sin tope, MDD de −46.1% en 2017-2026) y el apalancamiento bruto máximo de 1.0x.

**3. Dachraoui, Kais (2018), "On the Optimality of Target Volatility Strategies", *Journal of Portfolio Management* 44(5), 58-67. doi:10.3905/jpm.2018.44.5.058. [solo abstract]**
- **Acceso:** abstract del editor y un resumen secundario en chino (Sina Finanzas, 2-ago-2019). El artículo es de pago; Semantic Scholar lo marca como cerrado.
- **Qué dice:**
  - El *target volatility* mejora a la cartera estática **si y solo si** la covarianza entre la volatilidad y el rendimiento ajustado por riesgo es negativa. No hace falta una relación inversa entre volatilidad y rendimiento.
  - Cifras de **segunda mano, no verificadas:** S&P 500 1990-2015, Sharpe de 0.34 contra 0.30; el S&P GSCI no mejora; el índice de bonos de JP Morgan sí.
- **Grado:** C para la condición, D para las cifras.
- **Qué cambia:** nada. La condición equivale a lo que comprobé en Božović (μ/σ² baja de ≈ 1.19 a ≈ 0.31 entre el quintil bajo y el alto del VIX). Crossref registra un trabajo nuevo del mismo autor, SSRN 7459731 (2026), "Target Volatility Strategies as Mean-Preserving Contractions". No se leyó (403) y queda como candidato.

**4. Laarits, Toomas (2026), "Discounting timing strategies", *Journal of Financial Economics* 185, 104364. doi:10.1016/j.jfineco.2026.104364.**
- **Tipo y acceso:** publicado (en línea el 19-sep-2026). Se leyó íntegra la versión del autor del 12-may-2026 (76 págs., enlazada desde https://sites.google.com/view/toomaslaarits/). La versión final de la revista no se leyó.
- **Muestra y método:** replica 39 estrategias de *timing*, todas publicadas: calendario, estacionalidad del mismo mes, gestión por volatilidad de 12 factores al estilo Moreira-Muir, eventos (resultados, FOMC), día de la semana, *value spreads* y ML. Usa CRSP desde 1926. Acumula los rendimientos mensuales rebalanceados a 12, 60 y 120 meses y mide Sharpe, α FF4 y *variance ratios*.
- **Hallazgos:**
  - Al pasar de 1 a 120 meses, el Sharpe promedio baja de **0.57 a 0.38**, el α FF4 de **5.5% a 2.1%** y el *appraisal ratio* de 0.6 a ≈ 0.2. El VR(120) promedio es 2.1, y 79% de las estrategias tiene VR(60) > 1: sus rendimientos tienen autocorrelación positiva.
  - **Mercado gestionado por volatilidad (mktrf):** Sharpe de 0.49 a 1 mes. El α CAPM pasa de **4.63% → 3.46% → 2.46% → 1.25%** (1, 12, 60 y 120 meses). El α FF4 ya es de 2.30% a 1 mes (t 1.29, no significativo) y baja a 1.03%.
  - **"Sell in May"** (en el mercado de noviembre a mayo): α CAPM de 2.63% (t 3.3) a 1 mes y 1.96% a 10 años.
  - **Cambio de mes:** 5.43% → 4.70%. Es el más robusto del grupo en la muestra completa.
  - Después de la publicación, el intercepto es de −1.1% (t 1.2): pierden poco en promedio.
- **Limitaciones:**
  - A 10 años hay pocas observaciones independientes.
  - Su interpretación (compensación por riesgo de largo plazo) es un modelo, no un hecho.
  - No analiza 2013-2026 por separado. Nuestro cálculo del cap. 26 §5.3 da el cambio de mes y Halloween ≈ 0 o invertidos en EUA desde 2013.
- **Grado B.**
- **Qué cambia:** ningún criterio. Agrega una **prueba** al protocolo de §6.4 como propuesta (no modifica `parametros.json`). Toda estrategia de *timing* (volatilidad, calendario o filtro) se evalúa también con rendimientos acumulados a la duración de la temporada y a 3-5 años, con su *variance ratio*, y no solo con el Sharpe mensual. Un Sharpe mensual alto con VR > 1 sobrestima lo que gana quien mantiene la estrategia varios años. Es coherente con R05: el α del mercado gestionado ya era débil a 1 mes.

**5. Devanathan, Nikhil, Alexandros E. Tzikas y Stephen P. Boyd (2026), "Simple Dynamic Stock/Bond/Gold Portfolios", arXiv:2609.07946 [q-fin.PM], v1 7-sep-2026.**
- **Tipo y acceso:** preprint. Se leyó íntegro (43 págs.: tablas 1, 2 y 13 y apéndices de robustez). El código es abierto.
- **Muestra y método:** SPY, AGG, GLD y efectivo, 2006-2026, rebalanceo mensual, costos de 5 pb, objetivo de volatilidad de 7%.
- **Hallazgos (tabla 1):**

| Cartera | Rendimiento | Volatilidad | Sharpe | MDD | Rotación |
|---|---|---|---|---|---|
| 60/40 | 8.1% | 11.3% | 0.56 | 33.7% | 3.4% |
| 60/40 con control de volatilidad | 7.1% | 7.4% | 0.71 | 16.9% | 85% |
| 50/30/20 (con oro) | 9.1% | 10.3% | 0.70 | 27.1% | 4.0% |
| 50/30/20 con control de volatilidad | 7.8% | 7.3% | 0.82 | 15.9% | 79% |
| "Markowitz" con pronóstico de rendimientos | 11.6% | 9.0% | 1.08 | 18.1% | 284% |

  - Por quinquenio, el 60/40 con control de volatilidad da 0.35, 0.99, 0.96 y 0.57 de Sharpe, contra 0.13, 0.99, 0.87 y 0.48 del 60/40 simple.
  - Elegir la especificación de Markowitz año con año (*walk-forward*) da 0.93-1.00 de Sharpe, contra 1.00-1.08 de la especificación fija. Los autores reportan un DSR > 0.99 con 17 especificaciones, pero admiten que lo subestiman porque los ensayos están muy correlacionados.
- **Limitaciones:** es una sola trayectoria de 20 años, en USD y sin impuestos. El Markowitz depende de pronósticos de rendimiento, y en este capítulo no aceptamos pronósticos de rendimiento sin réplica.
- **Grado C.**
- **Qué cambia:** nada. Confirma "freno con costo": el control de volatilidad reduce la MDD a la mitad y sube el Sharpe, pero cuesta ≈ 1 pp de rendimiento. Con nuestro objetivo de máximo CAGR sujeto a drawdown, solo conviene cuando la restricción de drawdown está activa. El Markowitz con oro queda como **candidato de laboratorio**: el código es abierto y habría que replicarlo en MXN con los costos de GBM. No se adopta.

**6. Hsieh, Chung-Han, Jow-Ran Chang y Hui Hsiang Chen (2025), "Compounding Effects in Leveraged ETFs: Beyond the Volatility Drag Paradigm", arXiv:2504.20116 [q-fin.ST], v1 28-abr-2025.**
- **Tipo y acceso:** preprint en revisión. Se leyó íntegro (34 págs.). Es anterior al periodo, pero venía en la cola.
- **Método:** define el efecto compuesto como el rendimiento del LETF **menos β veces** el rendimiento acumulado del subyacente. Deriva E[CE_n] ≈ −nf + Σ_k (n−k)[β(β−1)γ_k − 2βfμ], donde γ_k es la autocovarianza a k rezagos, y usa modelos AR(1), AR-GARCH y de cambio de régimen. La parte empírica cubre SPY y QQQ, de 2006 a 2023, en seis regímenes.
- **Hallazgos:**
  - Sin costos y con rendimientos independientes, E[CE] = 0. Es una esperanza **aritmética** de la riqueza final.
  - Con autocorrelación positiva (tendencia), el 3x supera a 3 veces el subyacente; con reversión, queda por debajo.
  - Recuperación 2009-13, 3x sobre SPY: +1.86 (sintético). Lateral 2014-15: −0.064.
  - El AR(1) diario de SPY en 2010-2023 es −0.049, con α+β de GARCH ≈ 0.97.
  - Media simulada de CE: SPXL +0.244 (d.e. 0.638) y TQQQ +0.403 (d.e. 0.965). Fricciones de 0.8-1.0 pp al año.
- **Limitaciones:** la media aritmética la domina la cola derecha (la d.e. es mayor que la media). No mide la mediana ni el crecimiento geométrico, que es lo que optimiza el sistema.
- **Grado C.**
- **Qué cambia:** nada; **acota** §2.1. La fórmula g_L ≈ r + L(μ − r) − L²σ²/2 supone rendimientos independientes y sigue siendo la referencia para la mediana. Omite un término de autocorrelación: con tendencia diaria persistente un 3x rinde más que la fórmula, y con reversión diaria (SPY 2010-2023) rinde menos. Eso da otra razón para el filtro de tendencia de R8: selecciona los tramos donde la autocorrelación favorece al apalancado.

**7. Bonacorsi, Nicolò (2026), "Certified Alpha Capacity: Statistical Evidence, Economic Lifetime, and Arbitrage under Decay", arXiv:2610.01115 [stat.ME], v1 1-oct-2026.**
- **Tipo y acceso:** preprint de un solo autor (Columbia, Física Aplicada). Se leyeron las secciones 1-3, 5.4-5.5, 6.3, 7 y 9 de 39 páginas.
- **Hallazgos teóricos:** con una señal que decae exponencialmente, certificarla al nivel α con potencia 1−β exige una vida media h ≥ 2·ln2·(z_{1−α} + z_{1−β})²/S², donde S es el Sharpe instantáneo. Con α = 5% y potencia de 90%:

| Sharpe anual | Vida media mínima |
|---|---|
| 1.0 | **11.9 años** |
| 1.5 | 5.3 años |
| 2.0 | 3.0 años |
| 3.0 | 1.3 años |

  Probar M candidatas con Bonferroni sube el umbral.
- **Hallazgos empíricos:**
  - En 205 predictores de Open Source Asset Pricing, su proxy de factibilidad **no** predice cuánto decae la señal después de publicarse (Spearman 0.059, IC de [−0.086, 0.199]).
  - En las *funding rates* de BTC y ETH (6 exchanges, 543 eventos), su puntaje de vida tiene ρ = 0.476 con el *funding* de los 7 días siguientes.
- **Limitaciones:** un solo autor, sin revisión, el modelo es gaussiano y los ejercicios son retrospectivos.
- **Grado D.**
- **Qué cambia:** nada. Es otra forma de MinBTL (§2.10): una señal con Sharpe anual de 1 que se muere en menos de ~12 años no se puede certificar antes de que muera. Respalda `backtest_min_anios` = 10 más el periodo en papel, y la desconfianza ante señales de vida corta. El hallazgo de *funding* no aplica, porque la cuenta cripto es solo spot.

**8. Strahle, Oscar (2026), "How Does Reducing Exposure During Drawdowns Impact Portfolio Performance?", SSRN 7542498 (30-sep-2026). [solo abstract]**
- **Acceso:** SSRN dio 403; el resumen se obtuvo vía buscador.
- **Qué dice:** compara tres reglas en SPY de 2000 a 2025: umbrales fijos de *drawdown*, escalamiento lineal y medias móviles.
  - Todas bajan la volatilidad y la MDD. Con medias móviles, la volatilidad pasa de 19.38% a 9.35% y la MDD de −55.19% a −21.97%.
  - Todas bajan el CAGR: de 8.03% a entre 5.27% y 7.41%. **Ninguna** mejora el Sharpe ni el Sortino.
  - El Calmar sube (0.24 contra 0.15 con medias móviles).
  - Las pérdidas vienen de quedarse subexpuesto en las recuperaciones y de latigazos en caídas poco profundas.
- **Grado D:** documento de trabajo de un solo autor, sin lectura íntegra.
- **Qué cambia:** nada. Coincide con R01/AC-09 ("solo protección") y con los cortacircuitos como freno, no como fuente de rendimiento.

**Revisados sin agregarse:** Bongiorno-Manolakis-Mantegna (arXiv 2607.23068, "volatility drag" con apalancamiento). Es sobre una red neuronal de mínima varianza, no sobre ETF apalancados, así que no es material para R8.

---

## 5. Evidencia real: qué funciona, qué no, magnitudes netas y decaimiento

| Tema | Veredicto | Magnitud y contexto | Grado |
|---|---|---|---|
| Kelly fraccional (≤ 0.5) frente a Kelly completo | **Funciona** | 75% del crecimiento con 50% de la volatilidad (c = 0.5); P(tocar −50%) baja de 50% a 12.5% (matemática) | A |
| Encoger la apuesta por incertidumbre | Funciona | Mejora OOS (Baker-McHale) | B |
| Volatility management del **mercado**, sin apalancamiento | Funciona **para drawdown**, no para Sharpe | Propio, 2017-2026: MDD −9.9% frente a −24.7%; SR 0.81 frente a 0.84 | B |
| Volatility management de **factores** long-short | No funciona neto (salvo la versión multifactor condicional) | Cederburg: 103 estrategias; Barroso-Detzel: α neto ≈ 0; DMU 2024 y Xu 2026 lo discuten | C |
| Risk parity apalancado | Depende del régimen | RPAR 2022 −22.8% frente a AOR −15.7%; 2022-2026 acumulado −1.4% frente a +35.1% | C |
| Optimización media-varianza con medias muestrales | **No funciona** | Ninguno de 14 modelos le gana a 1/N; ~3,000 meses necesarios | A |
| Shrinkage de covarianzas | Funciona (mínima varianza, riesgo) | Estándar de la industria | A |
| HRP | Sin ventaja demostrada | Trucíos 2026; Reis et al. 2023 | C |
| Stop-loss en activo sin persistencia | Resta rendimiento esperado | Derivación y Xiang-Deng 2024 | B |
| Stop-loss / filtro de tendencia en activos con persistencia | Puede sumar y reduce la volatilidad | Kaminski-Lo 2014 (frecuencias largas) | B |
| ETF 3× permanente | **Destruye crecimiento** en volatilidad alta | TQQQ 2022 −79.1%; 2022-2026 +98.7% frente a QLD +118.7% | A (matemática) / B (datos) |
| Backtest con muchas variantes sin DSR | Falso descubrimiento casi seguro | MinBTL: 45 pruebas / 5 años; haircut > 50% si SR < 0.4 | A |
| Anomalías publicadas | Decaen | −26% OOS, −58% post-publicación; 65-82% no replican (HXZ) frente a mayoría replica (JKP) | A/B |
| Cosecha de pérdidas fiscales | Funciona, pequeño | EUA 0.82-1.08%/año bruto; en México menor (10%, costo promedio) | B |
| Rebalanceo por bandas frente a calendario | Bandas ≥ calendario neto de costos | Davis-Norman (teoría); Zhang et al. 2025 | B |

**Decaimiento después de publicar, caso de estudio:** la gestión por volatilidad se publicó en 2016-2017. Las críticas de 2020-2021 y mi cálculo con datos posteriores a 2017 coinciden: la mejora en Sharpe del mercado **se esfumó** (0.54 frente a 0.33 antes; 0.81 frente a 0.84 después). La reducción de drawdown **se mantuvo**. Ese es el patrón típico: el "alfa" decae y la gestión de riesgo permanece.

---

## 6. Traducción operable

Todo límite sale de `config/parametros.json`. No se inventan otros.

### 6.1 Fórmula de sizing (cada operación)

```
riesgo_$ = capital × r_base × m_racha × m_drawdown × m_limite
    r_base      = 0.005 en fase de prueba / 0.01 patrimonio estándar / 0.03 arena
    m_racha     = 0.5 tras 3 pérdidas seguidas; vuelve a 1.0 tras 2 ganadoras; pausa a la 5.ª pérdida
    m_drawdown  = según cortacircuitos (p. ej. 0.5 del satélite a −8% estándar; exposición táctica ×0.5 a −12% en la arena)
    m_limite    = 0 si se tocó el límite diario, semanal o mensual

acciones = floor(riesgo_$ / |entrada − stop|)             (riesgo.tamano_por_stop)

tope_kelly: riesgo_op ≤ fraccion_kelly × f*_encogido
    fraccion_kelly = 0.25 estándar / 0.5 arena
    f*_encogido    = p_enc − (1 − p_enc)/b
    p_enc          = límite inferior del intervalo de 80% de la tasa de aciertos estimada (Baker-McHale)

tamaño final = min(tamaño_stop, tamaño_kelly, tope_concentración, tope_vol_objetivo)
```

**Regla R1:** si f*_encogido ≤ 0, no hay operación: no hay ventaja demostrada.

**Regla R2 (arena):** 3% por operación solo se permite si 3% ≤ 0.5 × f*_encogido, es decir, si f*_encogido ≥ 6%. Con b = 1 eso pide p_enc ≥ 53%; con b = 2, p_enc ≥ 37.3%. Si no se cumple, el riesgo baja a 0.5·f*.

### 6.2 Presupuesto de rachas (antes de activar una estrategia)

- **Estándar (r = 1%):** la peor racha antes de la pausa cuesta −3.94%, dentro del límite mensual de 6% y lejos del cortacircuitos de −8%.
- **Arena (r = 3%):**
  - La peor racha con la regla cuesta −11.45%, justo debajo del cortacircuitos de −12%.
  - P(racha ≥ 5 en una temporada de 48 operaciones con 55% de aciertos) = 38%.
  - *Inferencia:* con esos parámetros, la arena tocará el primer cortacircuitos en ~1 de cada 3 temporadas **solo por rachas**, aunque tenga ventaja real. Es el precio del 3%; el dueño lo aceptó en `tolerancia_riesgo`.
- **Regla R3:** no abrir 2 operaciones correlacionadas (ρ > 0.7, mismo subyacente o factor) como si fueran independientes. Suman un solo presupuesto de riesgo. La matemática de rachas supone independencia, y la correlación la empeora.

### 6.3 Construcción de portafolio

- **R4 — Núcleo (≥ 70% del patrimonio estándar):** partir de 1/N por clase de activo o de pesos de mercado. La covarianza se estima con shrinkage de Ledoit-Wolf, nunca con la muestral cruda. Media-varianza con medias históricas está prohibida.
- **R5 — Opiniones tácticas:** entran por Black-Litterman con Ω explícita, nunca modificando pesos a mano.
- **R6 — Risk parity:** solo sin apalancamiento en fase 1 (`bruto_max_fase_1` = 1.0). Hay que revisar la correlación rodante de 36 meses entre acciones y bonos: si es > 0, los bonos no cubren y su peso de "cobertura" se reevalúa.
- **R7 — Volatility targeting:** se usa como **freno**, no como acelerador. Exposición = min(1.0, σ_objetivo/σ̂_{t−1}), con un tope de 1.0 en fase 1 y 1.3 en fase 2. La evidencia post-publicación dice que el valor está en el drawdown, no en el Sharpe.
- **R8 — ETF apalancados (arena):**
  - Filtro de `filtro_apalancados`: subyacente sobre su media móvil de 200 días y VIX < 25; se venden al perder el filtro. Es coherente con Harvey et al. (reducir la exposición en volatilidad alta).
  - Tope de `etf_apalancado_max` = 0.5.
  - Preferir 2× sobre 3× si la σ realizada de 20 días del subyacente es > 25% anual. Esto es una *Inferencia* de L* = (μ − r)/σ² y de los datos de 2022-2026.

### 6.4 Protocolo de validación de estrategias (checklist obligatorio)

1. **Hipótesis previa** escrita, con mecanismo económico (Arnott-Harvey-Markowitz). Registrar **todas** las variantes con `backtest.registrar_variante`.
2. **Datos:**
   - *Point-in-time* y sin sesgo de supervivencia (incluir emisoras deslistadas).
   - Señal rezagada al menos 1 día (`con_rezago`) y contables desde su fecha de publicación.
   - Rendimientos en MXN con el tipo de cambio de ese momento.
3. **Historia ≥ 10 años** (`backtest_min_anios`). Para usar 5 años, MinBTL limita a ≤ 45 configuraciones independientes.
4. **Costos:** comisión de GBM + IVA + spread + deslizamiento (Cap. 14) + ISR de 10%. Prueba de estrés con costos ×2.
5. **Partición:** walk-forward **y** CPCV con purging y embargo ≥ horizonte de tenencia. Si discrepan, gana el más conservador.
6. **Estadística:**
   - DSR ≥ 0.95 (`deflated_sharpe_min_probabilidad`), con N = número de variantes registradas.
   - PBO ≤ 0.25 (`pbo_max`).
   - t > 3 para una señal nueva (HLZ).
   - SE del Sharpe con autocorrelación (Lo) y pruebas de diferencia de Sharpe robustas (Ledoit-Wolf 2008). **Fórmulas (adenda 2026-09-25, examen diagnóstico S2-11):** Jobson-Korkie (1981, JF 36:889-908) con la corrección de Memmel (2003, Finance Letters 1:21-23): √T(ŜR_B − ŜR_A) → N(0, V), V = 2 − 2ρ + 0.5(SR_A² + SR_B² − 2·SR_A·SR_B·ρ²), Sharpes en la frecuencia de los datos. Con colas pesadas, heterocedasticidad o dependencia serial (fondos ilíquidos, momentum), esta prueba pierde validez y Ledoit-Wolf (2008, J. Empirical Finance 15(5):850-859) recomienda un intervalo de confianza con *bootstrap* studentizado de bloques circulares en su lugar. Para desuavizar rendimientos con autocorrelación positiva por iliquidez, Getmansky, Lo y Makarov (2004, JFE 74(3):529-609) modelan el rendimiento observado como una media móvil de rendimientos verdaderos, R_obs,t = θ₀R_t + θ₁R_{t−1} (Σθᵢ=1): con ρ₁ observada, θ₀θ₁/(θ₀²+θ₁²) = ρ₁ da los pesos, y σ_verdadera = σ_obs/√(θ₀²+θ₁²).
7. **Robustez:** meseta de parámetros (sin picos aislados), subperiodos (antes y después de 2008, y 2022), otros mercados (EUA, México), y quitar los 5 mejores meses.
8. **Descuento por decaimiento:** para anomalías publicadas, el rendimiento esperado en vivo es ≤ 50% del backtest (McLean-Pontiff: −58%).
9. **Paper trading** ≥ 3 meses **y** ≥ 30 operaciones. Luego 25% del capital (`fraccion_capital_inicial`).
10. **Criterio para matar la estrategia:** 5 pérdidas seguidas (pausa y revisión), o un desempeño en vivo por debajo del percentil 5 de la distribución simulada del backtest ajustado por costos.

### 6.5 Evaluación de desempeño (propio y de rivales)

- **R9:** nunca reportar un Sharpe sin su SE, su PSR contra 0 y el número de pruebas.
- **R10 (MinTRL):** una temporada de 6 meses con datos diarios demuestra habilidad al 95% solo si el SR anual es ≥ ~2.3. Ganar o perder una temporada es, casi siempre, ruido.
  - El requisito de fase 2 (12 meses con Sharpe > 0.7) es una **compuerta operativa, no una prueba estadística**: el MinTRL con SR 0.7 es 5.7 años.
  - *Inferencia:* al presentar el paso a fase 2, reportar el PSR junto con el criterio del archivo.
- **R11 — Modo torneo (arena):** está en `modo_torneo` (±5 pp contra el mejor rival). La evidencia de Brown-Harlow-Starks muestra que los que van perdiendo suben el riesgo. Aquí esa conducta queda **acotada** por los cortacircuitos y el límite duro de −35%. Nunca se "apuesta para resucitar" más allá del límite.

### 6.6 Rebalanceo e impuestos

- **R12:** bandas 5/25 de `rebalanceo`, con revisión mensual. Se rebalancea si la desviación supera min(5 pp, 25% × peso objetivo). Con costos proporcionales, **llevar la posición al borde de la banda**, no al objetivo (Davis-Norman).
- **R13:** usar los flujos (aportes, dividendos) para rebalancear antes que vender.
- **R14 (cosecha de pérdidas):**
  - En noviembre-diciembre, revisar posiciones con pérdida latente. Realizarlas si la pérdida fiscal a 10% supera el costo ida y vuelta, y sustituir con un instrumento de exposición similar pero otra emisora o índice.
  - Las pérdidas solo compensan ganancias de la misma sección del art. 129, en el ejercicio o en los 10 siguientes.
  - El costo es promedio por emisora: vender una parte no permite elegir el lote.

### 6.7 Tablero de riesgo mínimo (diario)

Mostrar: drawdown vigente frente a cortacircuitos (`riesgo.estado_cortacircuitos`), P&L del día, semana y mes frente a sus límites, racha vigente y multiplicador (`riesgo.factor_por_rachas`), concentración por emisora, sector, ETF apalancado y cripto, exposición bruta, ES 97.5% histórico del portafolio y correlación rodante de 60 días entre las posiciones principales.

---

## 7. Trampas y errores comunes

1. **Usar Kelly completo con p estimado:** el error de estimación duplica la fracción efectiva sin que lo notes.
2. **Confundir el promedio aritmético con el geométrico:** +50% y −50% dan −25%, no 0.
3. **Tratar operaciones correlacionadas como independientes:** 5 posiciones en semiconductores son una sola apuesta.
4. **Poner stops dentro del ruido:** un stop menor a ~1 ATR convierte la volatilidad normal en pérdidas realizadas, y su costo se paga en comisiones y spread.
5. **Mover el stop a favor de la pérdida:** destruye el cálculo de riesgo de §6.1.
6. **Aplicar volatility targeting sin tope de apalancamiento:** propio, 2017-2026: MDD −46.1% frente a −24.7% del buy-and-hold.
7. **Suponer correlación acciones-bonos negativa:** desde 2022 fue +0.56 mensual.
8. **Calcular el VaR bajo normalidad:** subestima la cola (VaR 99% de SPY: 3.20% histórico frente a 2.67% normal; 54 días > 4σ contra 0.54 esperados).
9. **Reportar el mejor de N backtests sin DSR:** con 5 años y más de 45 variantes, el SR IS de 1 es ruido.
10. **Aplicar el haircut fijo de 50%:** es demasiado indulgente con SR < 0.4 y demasiado severo con SR > 1.
11. **Hacer validación cruzada k-fold ordinaria con etiquetas traslapadas:** filtra información; hay que purgar y embargar.
12. **Usar el universo actual hacia atrás:** sesgo de supervivencia.
13. **Rebalancear al objetivo con costos proporcionales:** opera de más; basta llevar la posición al borde de la banda.
14. **Anualizar el Sharpe mensual con √12 cuando hay autocorrelación:** sesgo de hasta 65% (Lo).
15. **Leer un año bueno de risk parity, HRP o gestión por volatilidad como prueba:** los tres fallan fuera de muestra o por régimen.
16. **Mantener un ETF 3× sin filtro:** −79.1% en 2022 exige +378% para recuperarse.
17. **Juzgar a un rival o a uno mismo por una temporada:** el MinTRL dice que 6 meses no bastan salvo con SR ≥ ~2.3.

---

## 8. Examen de titulación

1. **Una estrategia gana 55% de las veces con pago 1:1. ¿Cuál es f* y cuánto crecimiento conservas con c = 0.25?**
   f* = 0.55 − 0.45 = 10%. Con c = 0.25 se conserva ≈ 44% del crecimiento máximo (43.7% exacto en el caso binario; 2c − c² = 43.75% en el continuo).
2. **¿Qué pasa si apuestas 2× Kelly?**
   El crecimiento esperado del exceso es ≈ 0 (en el caso binario, ligeramente negativo) con el doble de volatilidad. Es la frontera de ruina en el largo plazo.
3. **Con 55% de aciertos y 100 operaciones independientes, P(racha ≥ 5) y P(racha ≥ 3)?**
   ≈ 64.7% y ≈ 99.8%. Con 60% de aciertos: 45.9% y 98.8%.
4. **¿Cuánto cuestan 5 pérdidas a 1% y a 3% de riesgo? ¿Y con la regla de rachas?**
   −4.90% y −14.13%. Con la regla (×0.5 tras la 3.ª): −3.94% y −11.45%.
5. **Deriva la fracción de crecimiento de Kelly fraccional en tiempo continuo.**
   g(c) − r = c·SR² − c²·SR²/2. Dividido entre SR²/2 queda 2c − c².
6. **¿Qué encontró Cederburg et al. (2020) y por qué contradice a Moreira-Muir?**
   En 103 estrategias, las versiones gestionadas por volatilidad no superan OOS a las originales. Los alfas de spanning requieren conocer ex post la combinación óptima, y esas regresiones son estructuralmente inestables.
7. **¿Por qué 1/N le gana a la media-varianza muestral?**
   Por el error de estimación de las medias. Con 25 activos harían falta ~3,000 meses para que la optimización gane (DeMiguel-Garlappi-Uppal 2009).
8. **¿Por qué el VaR no es coherente y qué lo sustituye?**
   No es subaditivo: la diversificación puede "aumentar" el VaR, y además ignora la severidad de la cola. El ES/CVaR es coherente y se optimiza como programa lineal (Rockafellar-Uryasev).
9. **¿Cuándo resta valor un stop-loss?**
   Cuando el activo no tiene persistencia y paga prima positiva: salir cambia la prima por el activo seguro sin ganar poder predictivo. Solo suma con momentum o memoria larga (Kaminski-Lo 2014; Xiang-Deng 2024).
10. **Calcula el SE del Sharpe anual con SR = 1.0 y 5 años, y di qué implica.**
    √((1 + 0.5)/5) ≈ 0.55. El intervalo del 95% va de ≈ −0.07 a 2.07: 5 años apenas distinguen SR 1 de 0.
11. **Un analista reporta SR 2.5 con 5 años diarios, tras 100 pruebas (V = 0.5, asimetría −3, curtosis 10). ¿Se acepta?**
    No: DSR = 0.90 < 0.95. Con 46 pruebas habría pasado (0.9505).
12. **¿Qué es PBO y qué umbral usa el sistema?**
    La probabilidad de que la mejor configuración IS quede por debajo de la mediana OOS, estimada por CSCV. El sistema exige PBO ≤ 0.25.
13. **¿Por qué no aplicar un haircut fijo de 50% al Sharpe?**
    Harvey-Liu (2015): el haircut es no lineal. Supera 50% cuando SR < 0.4 y es ≤ 25% cuando SR > 1.0.
14. **¿Cuánto decaen las anomalías publicadas?**
    26% menos fuera de muestra y 58% menos después de publicarse (McLean-Pontiff 2016, 97 predictores).
15. **En México, ¿cómo se usan las pérdidas de acciones en bolsa?**
    Art. 129 LISR: 10% definitivo sobre la ganancia neta del ejercicio. Las pérdidas se disminuyen solo contra ganancias de esa sección en el mismo ejercicio o en los 10 siguientes, actualizadas. El costo es promedio por emisora.

---

## 9. Fuentes

1. Kelly, J. L. (1956). Bell System Technical Journal 35. https://doi.org/10.1002/j.1538-7305.1956.tb03809.x
2. Thorp, E. O. (2008). Handbook of Asset and Liability Management, Elsevier. https://doi.org/10.1016/B978-044453248-0.50015-0
3. MacLean, Thorp, Ziemba (2010). Quantitative Finance 10(7). https://doi.org/10.1080/14697688.2010.506108
4. Baker, McHale (2013). Decision Analysis 10(3). https://doi.org/10.1287/deca.2013.0271
5. Busseti, Ryu, Boyd (2016). J. of Investing 25(3). https://doi.org/10.3905/joi.2016.25.3.118
6. Moreira, Muir (2017). JF 72(4). https://doi.org/10.1111/jofi.12513 — NBER w22208: https://www.nber.org/papers/w22208
7. Cederburg, O'Doherty, Wang, Yan (2020). JFE 138(1). https://doi.org/10.1016/j.jfineco.2020.04.015
8. Barroso, Detzel (2021). JFE 140(3). https://doi.org/10.1016/j.jfineco.2021.02.009
9. Harvey, Hoyle, Korgaonkar, Rattray, Sargaison, Van Hemert (2018). JPM 45(1). https://doi.org/10.3905/jpm.2018.45.1.014
10. DeMiguel, Martín-Utrera, Uppal (2024). JF 79(6). https://doi.org/10.1111/jofi.13395
11. Xu (2026). Critical Finance Review 15. https://doi.org/10.1108/cfr-03-2023-2491
12. Wang, Yan (2021). J. Banking & Finance 131, 106198 (cita verificada; hallazgo no leído). https://doi.org/10.1016/j.jbankfin.2021.106198 — **Actualización 2026-10-05:** leído íntegro, ver la adenda de §4 y la ref. 71.
13. Asness, Frazzini, Pedersen (2012). FAJ 68(1). https://doi.org/10.2469/faj.v68.n1.1
14. Filho, Gaspar (2024). JPM 50. https://doi.org/10.3905/jpm.2024.1.585
15. DeMiguel, Garlappi, Uppal (2009). RFS 22(5). https://doi.org/10.1093/rfs/hhm075
16. Kan, Zhou (2007). JFQA 42(3). https://doi.org/10.1017/S0022109000004129
17. Ledoit, Wolf (2004). JPM 30(4). https://doi.org/10.3905/jpm.2004.110
18. Ledoit, Wolf (2017). RFS 30(12). https://doi.org/10.1093/rfs/hhx052
19. Ledoit, Wolf. The Power of (Non-)Linear Shrinking. J. Financial Econometrics 20(1), 187-218. https://doi.org/10.1093/jjfinec/nbaa007
20. Black, Litterman (1992). FAJ 48(5). https://doi.org/10.2469/faj.v48.n5.28
21. López de Prado (2016). JPM 42(4). https://doi.org/10.3905/jpm.2016.42.4.059
22. Trucíos (2026). Empirical Economics 70. https://doi.org/10.1007/s00181-026-02900-x
23. Reis, Sobreira, Trucíos, Asrilhant (2023). Brazilian Review of Finance 21(4). https://doi.org/10.12660/rbfin.v21n4.2023.89848
24. Gârleanu, Pedersen (2013). JF 68(6). https://doi.org/10.1111/jofi.12080
25. Artzner, Delbaen, Eber, Heath (1999). Mathematical Finance 9(3). https://doi.org/10.1111/1467-9965.00068
26. Rockafellar, Uryasev (2000). J. of Risk 2(3). https://doi.org/10.21314/JOR.2000.038
27. Rockafellar, Uryasev (2002). JBF 26(7). https://doi.org/10.1016/S0378-4266(02)00271-6
28. Chekhlov, Uryasev, Zabarankin (2005). IJTAF 8(1). https://doi.org/10.1142/S0219024905002767
29. Grossman, Zhou (1993). Mathematical Finance 3(3). https://doi.org/10.1111/j.1467-9965.1993.tb00044.x
30. Magdon-Ismail, Atiya, Pratap, Abu-Mostafa (2004). J. Applied Probability 41(1). https://doi.org/10.1017/S0021900200014108
31. Kaminski, Lo (2014). J. Financial Markets 18. https://doi.org/10.1016/j.finmar.2013.07.001 — MIT DSpace: https://dspace.mit.edu/handle/1721.1/114876
32. Han, Zhou, Zhu. Taming Momentum Crashes: A Simple Stop-Loss Strategy (SSRN WP). https://doi.org/10.2139/ssrn.2407199
33. Xiang, Deng (2024). Quantitative Finance 24. https://doi.org/10.1080/14697688.2024.2306830
34. Sadaqat, Butt, Demirer (2026). SSRN WP. https://doi.org/10.2139/ssrn.7511970
35. Longin, Solnik (2001). JF 56(2). https://doi.org/10.1111/0022-1082.00340
36. Ang, Chen (2002). JFE 63(3). https://doi.org/10.1016/S0304-405X(02)00068-5
37. Cont (2001). Quantitative Finance 1(2). https://doi.org/10.1080/713665670
38. Brixton, Brooks, Hecht, Ilmanen, Maloney, McQuinn (2023). JPM 49(4). https://doi.org/10.3905/jpm.2023.1.459
39. Lo (2002). FAJ 58(4). https://doi.org/10.2469/faj.v58.n4.2453
40. Bailey, López de Prado (2012). J. of Risk 15(2). https://doi.org/10.21314/JOR.2012.255 — preprint: https://www.davidhbailey.com/dhbpapers/sharpe-frontier.pdf
41. Bailey, López de Prado (2014). JPM 40(5). https://doi.org/10.3905/jpm.2014.40.5.094 — preprint: https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
42. Bailey, Borwein, López de Prado, Zhu (2014). Notices AMS 61(5). https://doi.org/10.1090/noti1105 — preprint: https://www.davidhbailey.com/dhbpapers/backtest-pseudo.pdf
43. Bailey, Borwein, López de Prado, Zhu. The Probability of Backtest Overfitting. J. Computational Finance. https://doi.org/10.21314/JCF.2016.322 — preprint: https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf
44. Harvey, Liu (2015). JPM 42(1). https://doi.org/10.3905/jpm.2015.42.1.013 — PDF: https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF
45. Harvey, Liu, Zhu (2016). RFS 29(1). https://doi.org/10.1093/rfs/hhv059
46. Harvey, Liu (2020). JF 75(5). https://doi.org/10.1111/jofi.12951
47. López de Prado (2018). Advances in Financial Machine Learning, Wiley. Reseña: https://doi.org/10.1080/14697688.2019.1703030
48. Arian, Norouzi Mobarekeh, Seco (2024). Knowledge-Based Systems 305. https://doi.org/10.1016/j.knosys.2024.112477
49. Arnott, Harvey, Markowitz (2019). J. Financial Data Science 1(1). https://doi.org/10.3905/jfds.2019.1.064
50. López de Prado, Lipton, Zoonekynd (2026). JPM 52(6). https://doi.org/10.3905/jpm.2026.1.837
51. Ledoit, Wolf (2008). J. Empirical Finance 15(5). https://doi.org/10.1016/j.jempfin.2008.03.002
52. McLean, Pontiff (2016). JF 71(1). https://doi.org/10.1111/jofi.12365
53. Hou, Xue, Zhang (2020). RFS 33(5). https://doi.org/10.1093/rfs/hhy131
54. Jensen, Kelly, Pedersen (2023). JF 78(5). https://doi.org/10.1111/jofi.13249
55. Novy-Marx, Velikov (2016). RFS 29(1). https://doi.org/10.1093/rfs/hhv063
56. Elton, Gruber, Blake (1996). RFS 9(4). https://doi.org/10.1093/rfs/9.4.1097
57. Nefedov (2026). SSRN WP. https://doi.org/10.2139/ssrn.7350238
58. Davis, Norman (1990). Math. of Operations Research 15(4). https://doi.org/10.1287/moor.15.4.676
59. Zhang, Ahluwalia, Daga, Zi (2025). JPM 51(9). https://doi.org/10.3905/jpm.2025.51.9.183
60. Bai, Pachamanova, Steblovskaya, Wallbaum (2025). FMPM 40. https://doi.org/10.1007/s11408-025-00486-5
61. Chaudhuri, Burnham, Lo (2020). FAJ 76(3). https://doi.org/10.1080/0015198X.2020.1760064
62. Ley del Impuesto sobre la Renta, art. 129 (Cámara de Diputados; última reforma DOF 01-04-2024). https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf
63. Avellaneda, Zhang (2010). SIAM J. Financial Mathematics 1(1). https://doi.org/10.1137/090760805
64. Trainor (2025). J. Risk and Financial Management 19, 20. https://doi.org/10.3390/jrfm19010020
65. Brown, Harlow, Starks (1996). JF 51(1). https://doi.org/10.1111/j.1540-6261.1996.tb05203.x
66. BCBS (2019). Minimum capital requirements for market risk. https://www.bis.org/bcbs/publ/d457.htm
67. Datos de precios (cálculos propios de RPAR, AOR, SPY, AGG, TLT, IEF, QQQ, QLD, TQQQ, SSO, UPRO, ALLW, GLD y USDMXN; cierre ajustado): Yahoo Finance chart API, https://query1.finance.yahoo.com/v8/finance/chart/SPY (y los demás tickers)
68. Tasa libre de riesgo para el backtest de gestión por volatilidad: FRED TB3MS. https://fred.stlouisfed.org/series/TB3MS
69. Liu, Tang, Zhou (2019). JPM 46(1), 38-51. https://doi.org/10.3905/jpm.2019.1.107 (adenda 2026-10-05; solo abstract)
70. Dachraoui (2018). JPM 44(5), 58-67. https://doi.org/10.3905/jpm.2018.44.5.058 (adenda 2026-10-05; solo abstract) · resumen secundario: https://finance.sina.com.cn/stock/stockzmt/2019-08-02/doc-ihytcitm6334416.shtml
71. Wang, Yan (2021), PDF publicado en el sitio del autor (leído íntegro el 2026-10-05). https://www.lehigh.edu/~xuy219/research/Downside.pdf
72. Laarits (2026). JFE 185, 104364. https://doi.org/10.1016/j.jfineco.2026.104364 · versión del autor (may-2026): https://sites.google.com/view/toomaslaarits/
73. Devanathan, Tzikas, Boyd (2026). arXiv:2609.07946. https://arxiv.org/abs/2609.07946
74. Hsieh, Chang, Chen (2025). arXiv:2504.20116. https://arxiv.org/abs/2504.20116
75. Bonacorsi (2026). arXiv:2610.01115. https://arxiv.org/abs/2610.01115
76. Strahle (2026). SSRN 7542498. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7542498 (solo abstract)

**Nota de verificación (25-sep-2026):** la herramienta WebSearch agotó su presupuesto de sesión (200/200) antes de este módulo. Las citas se verificaron por otras vías:
- Metadatos (autores, año, revista, volumen, páginas, DOI) con la API de Crossref.
- Abstracts con Semantic Scholar, OpenAlex y Crossref.
- Textos completos de NBER w22208, los preprints de Bailey y López de Prado, el PDF de Harvey y Liu en Duke, Lo (2002) y la LISR.

Las cifras propias son reproducibles con `herramientas/datos.py` y `herramientas/metricas.py`. Quedaron sin verificar:
- La pérdida del fondo institucional All Weather en 2022.
- El nivel de 97.5% del ES de Basilea.
- El volumen y las páginas del artículo de PBO.
- Las cifras de Han-Zhou-Zhu.
- El hallazgo de Wang-Yan (2021). **Verificado el 2026-10-05** (lectura íntegra; adenda de §4).
- La existencia de una regla *wash sale* mexicana fuera del art. 129.
