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

  Las probabilidades salen de P(ver alguna vez x·W₀) = x^(2/c − 1), para un movimiento browniano con deriva, horizonte infinito y parámetros conocidos (derivación propia). En el caso binario (p = 0.55, b = 1), la simulación exacta da 43.7% del crecimiento con c = 0.25, 74.9% con c = 0.5 y −2.8% con c = 2.
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
- **Cederburg-O'Doherty-Wang-Yan (2020, JFE):** revisan 103 estrategias de acciones. Las versiones gestionadas **no superan sistemáticamente** a las originales en comparación directa. Los alfas de las regresiones de *spanning* no se pueden implementar en tiempo real. Las versiones fuera de muestra razonables ganan **menos** Sharpe y menos equivalente cierto. La causa es la inestabilidad estructural de esas regresiones.
- **Barroso-Detzel (2021, JFE):** netos de costos, solo sobrevive la gestión por volatilidad del **mercado**, y su ventaja se concentra en periodos de sentimiento alto. En los demás factores, el alfa neto es ≈ 0 y el Sharpe baja.
- **Harvey et al. (2018, JPM):** el targeting sube el Sharpe solo en activos de riesgo (acciones y crédito) por el *leverage effect*. En bonos, divisas y materias primas el efecto sobre el Sharpe es despreciable. En **todas** las clases reduce las colas izquierdas.
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
- **MinBTL** (Bailey-Borwein-López de Prado-Zhu 2014, Notices AMS): con 5 años de datos, **no más de 45 configuraciones independientes**; si no, se obtiene casi con seguridad un SR IS de 1 con SR OOS esperado de 0. Con 2 años, basta con 7 pruebas.
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
| 2026 (CFR 15, 179-207) | Xu, *Improving volatility-managed portfolios in real time* | 197 factores: 148 suben el Sharpe y 165 dan alfa positivo en tiempo real; robusto a costos y apalancamiento | Publicado → C (contradice a Cederburg; pendiente de replicar) |
| 2026 (Empirical Economics 70) | Trucíos, *Hierarchical risk clustering versus traditional risk-based portfolios* | Sin evidencia de que HRP supere a los métodos de riesgo tradicionales OOS | Publicado |
| 2026 (SSRN) | Nefedov, *How Much Sharpe is Illusory?* | Cripto: el protocolo ingenuo infla el SR 3.6×; ningún factor sobrevive | WP → C |
| 2026 (SSRN) | Sadaqat, Butt, Demirer | Stop-loss en momentum asiático: 2.8% a 5.3% mensual | WP → D |
| 2022-2026 (datos propios) | RPAR, ALLW, LETF, correlación SPY-IEF, VM SPY después de publicación | Ver §2.1, §2.4 y §2.5 | Cálculo reproducible |

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
   - SE del Sharpe con autocorrelación (Lo) y pruebas de diferencia de Sharpe robustas (Ledoit-Wolf 2008).
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
12. Wang, Yan (2021). J. Banking & Finance 131, 106198 (cita verificada; hallazgo no leído). https://doi.org/10.1016/j.jbankfin.2021.106198
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

**Nota de verificación (25-sep-2026):** la herramienta WebSearch agotó su presupuesto de sesión (200/200) antes de este módulo. Las citas se verificaron por otras vías:
- Metadatos (autores, año, revista, volumen, páginas, DOI) con la API de Crossref.
- Abstracts con Semantic Scholar, OpenAlex y Crossref.
- Textos completos de NBER w22208, los preprints de Bailey y López de Prado, el PDF de Harvey y Liu en Duke, Lo (2002) y la LISR.

Las cifras propias son reproducibles con `herramientas/datos.py` y `herramientas/metricas.py`. Quedaron sin verificar:
- La pérdida del fondo institucional All Weather en 2022.
- El nivel de 97.5% del ES de Basilea.
- El volumen y las páginas del artículo de PBO.
- Las cifras de Han-Zhou-Zhu.
- El hallazgo de Wang-Yan (2021).
- La existencia de una regla *wash sale* mexicana fuera del art. 129.
