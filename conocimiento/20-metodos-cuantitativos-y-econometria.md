# Módulo 20 — Métodos cuantitativos y econometría para el inversionista

> Nivel: doctorado aplicado (econometría financiera + escritorio sistemático) · Actualizado: 2026-09-25 · Grado de evidencia global: **A** para las herramientas (son teoremas y simulaciones con fallas conocidas) · **B/C** para su capacidad de detectar una ventaja con muestras de inversionista, porque tienen poca potencia · **D** para cualquier conclusión sacada de un solo backtest o de una temporada de 6 meses.
>
> Cifras propias: `laboratorio/ilustraciones/M20_hechos_estilizados.py` (salida en `M20-salida.txt`). Usa datos de French (CRSP, versión 202607) y de Yahoo al 24-sep-2026. Son **ilustraciones de método, no réplicas** del laboratorio. No enseña de nuevo el DSR, el PBO ni la validación cruzada combinatoria (cap. 07), las anomalías (cap. 06), la calibración de pronósticos (cap. 08) ni el *machine learning* (cap. 09). Aquí se ven las bases estadísticas que los sostienen.

---

## 1. Objetivos de dominio

Quien apruebe este módulo puede, con lápiz o con Python estándar:

1. Calcular el error estándar de una media de rendimientos, el t de un Sharpe (t = SR·√T) y los años necesarios para distinguir un Sharpe de cero.
2. Medir colas con curtosis, estimador de Hill y teoría de valores extremos, y explicar por qué la curtosis muestral no es un parámetro estable cuando α ≈ 3.
3. Estimar OLS con errores HAC de Newey-West, elegir rezagos, y detectar observaciones traslapadas y el sesgo de Stambaugh.
4. Correr Fama-MacBeth con la corrección de Shanken e interpretar la prueba GRS como una distancia entre Sharpes.
5. Elegir entre bootstrap iid, de bloques, estacionario, de sección cruzada (KTWW) y *wild*, según la estructura de dependencia.
6. Pronosticar volatilidad con GARCH(1,1) y HAR-RV y evaluar los pronósticos con QLIKE y Diebold-Mariano.
7. Usar modelos de régimen sin *look-ahead*, distinguiendo la probabilidad filtrada de la suavizada.
8. Probar cointegración, calcular la vida media de un spread y explicar por qué el pairs trading decayó.
9. Encoger (*shrinkage*) alfas, Sharpes y covarianzas con un prior explícito.
10. Controlar pruebas múltiples (Bonferroni, Holm, BH, BHY, Reality Check, SPA, StepM) y fijar la vara del t.
11. Evaluar pronósticos con DM, Clark-West y R² fuera de muestra, y traducir un R²_OS en dinero con la razón R²/S².
12. Separar correlación de causalidad, y conocer los "errores no estándar" de los analistas humanos y de las IAs.
13. Decir qué se puede concluir, y qué no, de una temporada de 6 meses en la competencia de GBM.

---

## 2. Núcleo teórico / marco

### 2.1 La media es el parámetro más ruidoso de las finanzas

Con rendimientos iid de media μ y volatilidad σ anual, observados durante T años:

- EE(μ̂) = σ/√T. **Depende del lapso calendario, no del número de observaciones.** Muestrear a diario en vez de mensual no mejora la media. Sí mejora la varianza: es el punto de Merton (1980) [1].
- t(μ̂) = μ/(σ/√T) = SR·√T. Años para t ≥ 1.96: T = (1.96/SR)². Años para una potencia de 80% al 5% bilateral: T = ((1.96 + 0.84)/SR)².

| SR anual verdadero | Años para t ≥ 1.96 | Años para t ≥ 3.0 | Años para potencia de 80% |
|---|---|---|---|
| 0.25 | 61.5 | 144 | 125.6 |
| **0.50** | **15.4** | **36** | **31.4** |
| 0.75 | 6.8 | 16 | 14.0 |
| 1.00 | 3.8 | 9 | 7.8 |
| 1.50 | 1.7 | 4 | 3.5 |
| 2.00 | 1.0 | 2.2 | 2.0 |

- Error estándar del Sharpe estimado (iid; Lo 2002 [2]): EE(SR̂) ≈ √((1 + SR²/2)/T). Con 10 años y SR = 0.5 da ±0.34, y el IC95 va de −0.17 a 1.17. Con 3 años, ±0.61.
- **Anualizar con √12 es incorrecto si hay autocorrelación** (Lo 2002 [2]): SR_anual = η(q)·SR_mensual, con η(q) = q/√(q + 2Σ_{k=1}^{q−1}(q−k)ρ_k). Con un AR(1) mensual, el √12 **infla** el Sharpe anual 9.6% si ρ = 0.1, 20.3% si ρ = 0.2 y 32.5% si ρ = 0.3 (cálculo propio). Los activos con precios suavizados (ilíquidos, valuados a modelo) presentan justo ese sesgo.

**Datos propios (French, mercado de EUA, jul-1926 a jul-2026, 1,201 meses):**

| Tramo | Prima media anual (media mensual × 12, aritmética) | EE | SR |
|---|---|---|---|
| 1926-2026 | 8.33% | 1.84 pp | 0.454 (t IID 4.54; t NW(6) 4.39) |
| 1926-1955 | 10.86% | 4.48 pp | 0.45 |
| 1956-1985 | 4.85% | 2.68 pp | 0.33 |
| 1986-2015 | 7.68% | 2.83 pp | 0.50 |
| 1996-2025 | 8.94% | 2.87 pp | 0.57 |

Con 30 años de datos, el IC95 de la prima todavía mide unos ±5.5 pp. Con un siglo, ±3.6 pp.

**Aplicación a la competencia.** Con σ = 25% anual, el rendimiento de 6 meses tiene σ = 17.7%. Tomemos dos cuentas con correlación de 0.5 y una ventaja **verdadera** de 5 pp anuales para la mejor. La diferencia a 6 meses tiene media de 2.5 pp y σ de 17.7 pp. La mejor gana la temporada con probabilidad **0.556**. Con 10 pp de ventaja, 0.611. Para acumular una evidencia de 95% (una cola) de que es mejor hacen falta **unas 136 temporadas** (68 años) con 5 pp de ventaja, o 34 temporadas con 10 pp (cálculo propio).

### 2.2 Colas, curtosis y valores extremos

**Hechos estilizados** (Cont 2001 [3]): colas pesadas, agrupamiento de volatilidad, asimetría entre ganancias y pérdidas, y autocorrelación lineal casi nula en los rendimientos pero no en |r| ni en r². Mandelbrot (1963) [4] propuso distribuciones estables de Pareto, con α < 2 y varianza infinita. Gopikrishnan et al. (1999) [5] midieron el S&P 500 en 1984-1996, a escalas de 1 minuto a 1 mes. Para Δt ≤ 4 días, las colas siguen una ley de potencia con **α ≈ 3**, fuera del rango estable de Lévy. Arriba de 4 días convergen a la normal, pero más despacio de lo esperado. Gabaix et al. (2003, *Nature*) [6] proponen una teoría para esa "ley cúbica".

**Mediciones propias (rendimientos logarítmicos diarios):**

| Serie | n | Asimetría | Curtosis | Días con \|z\|>4 (normal esperaría) | Días con \|z\|>5 (normal) | Peor día | α de Hill (colas izq. / der.; k = 0.5%-2.5%) |
|---|---|---|---|---|---|---|---|
| Mercado EUA, French 1926-2026 | 26,296 | −0.46 | 20.0 | 192 (1.7) | 104 (0.015) | −19.1% (19-oct-1987), z = −17.8 | 2.74-3.14 / 2.57-3.20 |
| IPC (^MXX) 1991-2026 | 8,733 | −0.01 | 9.8 | 52 (0.55) | 17 (0.005) | −14.3% (27-oct-1997), z = −10.4 | 2.83-4.87 / 2.96-4.09 |
| USD/MXN (MXN=X) 2003-2026 | 5,940 | **+0.94** | 15.1 | 33 (0.38) | 14 (0.003) | +9.3% (9-oct-2008); +8.3% (9-nov-2016) | 3.42-4.01 / **2.45-2.87** |

Para el inversionista en pesos, la cola pesada del tipo de cambio es la **depreciación** del peso (cola derecha de USD/MXN). Sus mayores saltos al alza (9 y 15-oct-2008, 9-nov-2016 y 9-mar-2020) caen en episodios de estrés. *Inferencia:* por eso el dólar funciona como cobertura en las crisis, porque sube justo cuando caen los activos de riesgo (ver cap. 16).

**Consecuencia matemática.** Si la cola tiene índice α, el momento E|r|^k existe solo para k < α. Con α ≈ 3, el cuarto momento poblacional no existe. *Inferencia:* la curtosis muestral no converge y la dominan los días más extremos. "Curtosis = 20" no es un parámetro estable, así que conviene reportar el índice de cola o los cuantiles extremos. La misma fragilidad llega al PSR y al DSR, que usan la curtosis (`herramientas/metricas.py`). Por eso deben validarse con bootstrap.

**Teoría de valores extremos (EVT).** Los máximos por bloques convergen a la GEV (Fisher-Tippett-Gnedenko). Los excesos sobre un umbral alto convergen a la GPD, con parámetro de forma ξ = 1/α (Pickands-Balkema-de Haan). El estimador de Hill (1975) [7] es α̂ = [ (1/k) Σ_{i≤k} ln(X_(i)/X_(k)) ]⁻¹. Es muy sensible a k: en el IPC, α pasa de 4.87 a 2.83 al mover k de 0.5% a 2.5% de la muestra. McNeil y Frey (2000) [8] proponen el GARCH-EVT en dos etapas. Primero se filtra con GARCH y después se ajusta la GPD a los residuos estandarizados. El resultado es un VaR/ES condicional al nivel de volatilidad del momento.

### 2.3 Regresión: OLS, betas, R² y errores estándar que no mienten

r_t = a + b·f_t + e_t, con b̂ = Cov(r, f)/Var(f), R² = b̂²·Var(f)/Var(r) y a = alfa si f es un factor negociable. Hay que corregir tres cosas:

1. **Heteroscedasticidad** (White): la varianza de e_t cambia con el tiempo, y en finanzas siempre cambia.
2. **Autocorrelación → Newey-West (1987)** [9]: Ω̂ = γ̂₀ + 2Σ_{j=1}^{L} (1 − j/(L+1))·γ̂_j. Los pesos de Bartlett garantizan una varianza semidefinida positiva. El L se elige con el procedimiento automático de Newey-West (1994) [10] o, como mínimo, igual al traslape. Con rendimientos de 12 meses muestreados cada mes, las observaciones comparten 11 meses, así que L ≥ 11. `herramientas/estadistica.newey_west` usa Bartlett con la corrección n/(n−1). **Siempre** se reportan el t IID y el t NW (alerta #6 del laboratorio). **Condición de consistencia (adenda 2026-09-25, examen diagnóstico S2-06):** Newey y West (1987), Econometrica 55(3):703-708, exigen L → ∞ pero **L = o(T^(1/4))** para que el estimador sea consistente; las tasas MSE-óptimas de Andrews (1991) (L ∝ T^(1/3) para Bartlett, T^(1/5) para *Quadratic Spectral*) son un refinamiento posterior, no la condición original de consistencia.
3. **Paneles** (Petersen 2009 [11]): hay que agrupar (*cluster*) por empresa y por fecha. Si el efecto empresa es persistente y no se agrupa, el t sale inflado.

**Sesgo de Stambaugh (1999)** [12]. En r_{t+1} = a + b·x_t + u_{t+1}, con x_{t+1} = c + ρ·x_t + v_{t+1}, el sesgo es E[b̂ − b] = (σ_uv/σ_v²)·E[ρ̂ − ρ]. El sesgo del AR(1) es E[ρ̂ − ρ] ≈ −(1 + 3ρ)/T. En el D/P, las innovaciones del precio y del predictor tienen correlación negativa (σ_uv < 0), así que b̂ **se sesga hacia arriba**. Un predictor muy persistente fabrica predictibilidad aparente en muestras cortas.

### 2.4 Fama-MacBeth y GRS

**Fama-MacBeth (1973)** [13] tiene dos pasos:

1. Se estiman las betas por serie de tiempo.
2. Cada mes se corre una regresión de sección cruzada r_{i,t} = λ_{0,t} + λ_t'β_i + e_{i,t}. El premio es λ̂ = promedio de λ_t, con EE = sd(λ_t)/√T.

El método es robusto a la correlación de sección cruzada, pero no a la autocorrelación de λ_t (hay que usar NW sobre λ_t). Además, las betas estimadas tienen error: Shanken (1992) [14] corrige la varianza multiplicándola por (1 + λ'Σ_f⁻¹λ).

**GRS (Gibbons-Ross-Shanken 1989)** [15] prueba H₀: α_i = 0 para las N carteras al mismo tiempo, con L factores:

J = ((T − N − L)/N) · α̂'Σ̂⁻¹α̂ / (1 + μ̄'Ω̂⁻¹μ̄) ~ F(N, T − N − L), con errores normales iid.

α'Σ⁻¹α = SR²(tangente con activos y factores) − SR²(solo factores). La prueba pregunta si los activos de prueba **aumentan el Sharpe alcanzable** más allá de los factores. *Inferencia:* con suficientes carteras de prueba casi todo modelo se rechaza. Conviene usar la GRS para ordenar modelos por SR² incremental y no como veredicto binario.

### 2.5 Bootstrap y Monte Carlo

- **Bootstrap** (Efron 1979) [16]: se aproxima la distribución muestral re-muestreando los datos. El iid destruye la dependencia. Con autocorrelación o volatilidad agrupada se usa el de **bloques** (`herramientas/estadistica.ic_bootstrap_bloques`) o el **estacionario** de Politis-Romano (1994) [17], con bloques de longitud geométrica aleatoria cuya serie re-muestreada es estacionaria.
- **Comparar dos Sharpes:** Ledoit-Wolf (2008) [18] muestran que Jobson-Korkie/Memmel no es válido con colas pesadas ni con series de tiempo. Proponen un intervalo por bootstrap estudentizado de series de tiempo para la diferencia.
- **Habilidad de fondos (sección cruzada de alfas):**
  - KTWW (2006) [19] re-muestrean la distribución conjunta de los alfas de 1975-2002. Encuentran que "una minoría considerable" de gestores cubre sus costos y que esos alfas persisten.
  - Fama-French (2010) [20]: pocos fondos generan lo suficiente para cubrir costos. Antes de comisiones sí aparecen habilidad e inhabilidad en las colas extremas.
  - Harvey-Liu (2022) [21]: el bootstrap de FF2010 tiene poca potencia.
  - Huang, Jiang, Leng y Peng (2023) [22]: los dos bootstraps más usados tienen **tamaño distorsionado** (historiales cortos, residuos asimétricos) y poca potencia cuando abundan los fondos sin habilidad.
  - Hounyo-Lin (2026) [23] proponen un *wild bootstrap* que respeta entradas y salidas de fondos. Tiene un tamaño casi óptimo y más potencia, y con él una fracción medible de fondos supera al mercado.
  - Barras-Scaillet-Wermers (2010) [24], con FDR: 75% de los fondos tiene alfa neto cero. Antes de 1996 había una proporción significativa de fondos con habilidad; para 2006, casi ninguno.
- **Monte Carlo propio.** Se simularon 200 estrategias **sin ventaja** durante 10 años mensuales, repetidas 2,000 veces. El mejor Sharpe anual tiene mediana de **0.87** (p5 = 0.70, p95 = 1.13). La fórmula de E[max] de `metricas.sharpe_maximo_esperado`, con V = 1/T, da 0.875. **Un Sharpe de 0.9 elegido entre 200 variantes es ruido.**

### 2.6 Series de tiempo: ARIMA, GARCH y HAR-RV

- **ARIMA(p,d,q)** (Box-Jenkins). Sirve para series con dinámica lineal, como inflación, tasas o spreads (cap. 04). En los rendimientos de índices la autocorrelación lineal es casi nula [3], así que un ARIMA sobre rendimientos no aporta nada. La información está en el segundo momento.
- **ARCH** (Engle 1982) [25]: σ²_t = ω + Σ α_i e²_{t−i}. **GARCH(1,1)** (Bollerslev 1986) [26]: σ²_t = ω + α·e²_{t−1} + β·σ²_{t−1}. Persistencia α + β, varianza de largo plazo ω/(1 − α − β) y vida media ln(0.5)/ln(α + β). Engle compartió el Nobel 2003 con Granger, el de la cointegración [27].
- **Ajuste propio** (S&P 500, 2000 a sep-2026, MV gaussiana aproximada): α = 0.118, β = 0.863. La persistencia es de **0.981**, la vida media de un choque de volatilidad es de **unos 36 días hábiles** y la volatilidad de largo plazo de 18.0% anual.
- **¿Algo le gana al GARCH(1,1)?** Hansen-Lunde (2005) [28] compararon 330 modelos fuera de muestra. En DM-$ nada le gana. En IBM pierde contra los modelos con efecto apalancamiento (asimétricos). El Reality Check no tuvo potencia para separar modelos buenos de malos. Andersen-Bollerslev (1998) [29] muestran que los modelos estándar pronostican bien si se evalúan contra la **volatilidad realizada**. El r² diario es un proxy tan ruidoso que baja el R² incluso de un modelo correcto.
- **HAR-RV** (Corsi 2009) [30]: RV_{t+1} = c + β_d·RV_t + β_w·RV_{t−4:t} + β_m·RV_{t−21:t} + e. Es un AR en cascada (día, semana, mes) que reproduce memoria larga, colas pesadas y autosimilitud, y se estima por OLS. HARQ (Bollerslev-Patton-Quaedvlieg 2016) [31] ajusta la reacción al error de medición de RV.
- **Ilustración propia.** Se pronosticó la varianza de los 22 días siguientes con un HAR estimado sobre r² diarios (no RV intradía), con ventana expansiva, contra el ingenuo "varianza de los últimos 22 días". En la segunda mitad de 2000-2026 (≈ 2013-2026), la pérdida QLIKE (RV/f − ln(RV/f) − 1) promedió **0.414 con HAR contra 0.645 con el ingenuo**. Diebold-Mariano con NW(22) da **t = 3.23**.
- **Volatilidad para ganar Sharpe.** Moreira-Muir (2017) [32] reportan alfas grandes en regresiones de expansión (*spanning*) en 8 factores. Cederburg et al. (2020) [33] revisan 103 estrategias en tiempo real. Las gestionadas por volatilidad **no** superan sistemáticamente a las originales, y fuera de muestra suelen tener menor CER y menor Sharpe por inestabilidad de las regresiones.

### 2.7 Cambio de régimen

**Hamilton (1989)** [34]: s_t ∈ {1,2} sigue una cadena de Markov con matriz de transición P, y y_t | s_t ~ N(μ_s, σ²_s). El filtro de Hamilton da P(s_t | información hasta t), que es la probabilidad **filtrada**. La probabilidad **suavizada** usa datos futuros y **no sirve para operar**. Ang-Timmermann (2012) [35] documentan regímenes con distintas medias, volatilidades, autocorrelaciones y correlaciones. Esos regímenes reproducen colas pesadas, heteroscedasticidad, asimetría y correlaciones cambiantes, suelen coincidir con periodos de política o regulación y cambian mucho la cartera óptima. Shu-Yu-Mulvey (2024) [36] usan un *statistical jump model* con penalización por cambio de estado, que da regímenes más persistentes que un HMM. Probado en EUA, Alemania y Japón de 1990 a 2023, con costos y retrasos, supera al HMM y a comprar y mantener en volatilidad, drawdown máximo y Sharpe. *Inferencia:* hay pocos cambios de régimen independientes (unas cuantas recesiones por siglo). La evidencia sirve para **reducir riesgo**, no para prometer alfa. La SMA200 del cap. 14 es un modelo de régimen rudimentario.

### 2.8 Cointegración y pairs trading

Dos series I(1) están cointegradas si una combinación lineal de ellas es estacionaria. El procedimiento de Engle-Granger (1987) [37] tiene dos pasos. Primero se regresa y sobre x. Después se aplica un ADF a los residuos, con valores críticos más negativos que los del ADF estándar porque β fue estimada. La vida media del spread sale de ΔS_t = a + b·S_{t−1} + e: HL = −ln 2 / ln(1 + b).

**Evidencia y decaimiento:**

- GGR (2006) [38]: método de distancia, 1962-2002. Las carteras autofinanciadas logran excesos anualizados **de hasta 11%**, por encima de estimaciones conservadoras de costos. El efecto es distinto de la reversión y está ligado a un factor común.
- Do-Faff (2010, 2012) [39][40]: con comisiones, impacto y costo del préstamo de acciones, queda un rendimiento ajustado por riesgo de **~30 pb/mes** en pares bien emparejados dentro de industrias finas. En el 30% de acciones más grandes, el alfa es de 24 pb/mes (versión de trabajo). El pairs trading y la reversión por industria son **en gran medida no rentables después de 2002**.
- Rad-Low-Faff (2016) [41], 1962-2014: excesos mensuales antes y después de costos de 91 y 38 pb (distancia), 85 y 33 pb (cointegración) y 43 y 5 pb (cópula). Desde 2009 caen las oportunidades en distancia y en cointegración.

### 2.9 Inferencia bayesiana y *shrinkage*

Con un prior normal θ ~ N(μ₀, τ²) y un estimador θ̂ con error estándar s, la media posterior es E[θ | θ̂] = μ₀ + [τ²/(τ² + s²)]·(θ̂ − μ₀). Un alfa de backtest de 6% anual con EE de 4% (t = 1.5) y un prior N(0, 2%²) se encoge a **1.2%**. Con EE de 2% (t = 3), a **3.0%**.

- **Medias:** Jorion (1986) [42] aplica Bayes-Stein a las medias esperadas de una cartera.
- **Covarianzas:** Ledoit-Wolf (2003) [43] encogen la covarianza muestral hacia una matriz estructurada. El cap. 02 ya adopta esa contracción.
- **Sección cruzada:** Kozak-Nagel-Santosh (2020) [44] estiman el SDF con un prior económico que penaliza los coeficientes. Jensen-Kelly-Pedersen (2023) [45] usan un modelo bayesiano jerárquico. La mayoría de los factores replica, se agrupan en 13 temas, funcionan en 93 países, y la cantidad de factores **refuerza** la evidencia.
- **Sesgos de publicación:**
  - Chen-Zimmermann (2020) [46]: el sesgo de publicación es de solo **12.3%** (EE de 1.7 pp), mucho menor que el decaimiento posterior a la publicación, lo que apunta a *mispricing*.
  - McLean-Pontiff (2016) [47]: en 97 predictores, los rendimientos son **26% menores fuera de muestra y 58% menores después de la publicación**.
- **Mínimo factor de Bayes** (Harvey 2017) [48]: MBF = exp(−t²/2), con probabilidad posterior de H₀ ≥ (momios previos·MBF)/(1 + momios previos·MBF). Con una probabilidad previa de H₀ de 80%, t = 2 deja P(H₀ | datos) ≥ **35%** y t = 3 deja ≥ 4.3%. Con una previa de 95%, t = 2 deja ≥ 72% y t = 3 deja ≥ 17%.

### 2.10 Pruebas múltiples

- **FWER** (probabilidad de al menos un falso positivo):
  - Bonferroni: p ≤ α/m.
  - Holm (1979) [49]: se ordenan los p y se rechaza mientras p_(k) ≤ α/(m − k + 1). Tiene más potencia que Bonferroni con la misma garantía.
- **FDR** (proporción esperada de falsos descubrimientos):
  - BH (1995) [50]: el mayor k con p_(k) ≤ k·q/m (independencia o dependencia positiva).
  - BHY (2001) [51]: p_(k) ≤ k·q/(m·c(m)), con c(m) = Σ_{i=1}^{m} 1/i. Vale con cualquier dependencia.
- **Con bootstrap, para "la mejor de muchas estrategias":**
  - Reality Check de White (2000) [52].
  - SPA de Hansen (2005) [53]: estudentizada y menos sensible a alternativas malas.
  - StepM de Romano-Wolf (2005) [54]: por pasos, capta la dependencia y tiene más potencia.

Varas t de Bonferroni al 5% bilateral: m = 1: 1.96; 5: 2.58; 10: 2.81; 20: 3.02; 50: 3.29; 100: 3.48; 316: 3.78.

**En finanzas:**

- **HLZ (2016)** [55]: con cientos de factores probados, t > 3.0, y "la mayoría de los hallazgos... probablemente falsos".
- **Harvey (2017)** [48]: incluso t > 3 da muchos falsos positivos si el efecto es raro.
- **Harvey-Liu (2020)** [56]: doble bootstrap para fijar una vara t ligada a un FDR dado, balanceando errores tipo I y II. Los métodos actuales carecen de potencia para detectar buenos gestores.
- **Chordia-Goyal-Saretto (2020)** [57]: con más de 2 millones de estrategias aleatorias, las varas son **3.8 (serie de tiempo) y 3.4 (sección cruzada)**. Sin corrección, ~45% de los rechazos serían falsos.
- **Contrapesos:** Chen-Zimmermann (2020) y JKP (2023), arriba. Chen, Lopez-Lira y Zimmermann (documento de trabajo) [58] minaron 29,000 razones contables con t > 2 y obtuvieron una predictibilidad **similar a la de la revisión por pares**. En ambos casos queda **~50%** de la predictibilidad después de la muestra original. Los predictores con explicación de riesgo rinden **menos** fuera de muestra.

### 2.11 Evaluación de pronósticos

- **Pérdidas:** MSE, MAE, QLIKE (varianzas), Brier y log score (probabilidades; `metricas.brier`, cap. 08).
- **Diebold-Mariano (1995)** [59]: d_t = L(e_{A,t}) − L(e_{B,t}) y DM = d̄/EE_NW(d̄) ~ N(0,1), con L ≥ h − 1 rezagos para horizontes h. Diebold (2015) [60] aclara que la DM compara **pronósticos, no modelos**. Para comparar modelos, las pruebas con muestra completa suelen ser mejores. Un pseudo fuera de muestra no es un seguro garantizado contra el sobreajuste.
- **Clark-West (2007)** [61], para modelos anidados. Bajo H₀, el modelo grande estima parámetros que valen cero, y su MSPE se infla. La prueba ajusta f_t = e²_chico − [e²_grande − (ŷ_chico − ŷ_grande)²] y aplica una prueba t de una cola con valores críticos normales, que queda ligeramente conservadora.
- **Giacomini-White (2006)** [62] evalúan la habilidad **condicional**. **Pesaran-Timmermann (1992)** [63] prueban el acierto de dirección.
- **R² fuera de muestra (Campbell-Thompson 2008)** [64]: R²_OS = 1 − Σ(r_t − r̂_t)²/Σ(r_t − r̄_{t−1})², donde r̄_{t−1} es la media histórica hasta t − 1. Restringir el signo del coeficiente y exigir prima positiva mejora los resultados.
  - **Valor económico:** el aumento proporcional del rendimiento de un inversionista media-varianza es ≈ R²/S². En la versión de trabajo, E/P tiene un R²_OS mensual de 0.25% contra S² = 1.2% (SR mensual de 0.108 desde 1871). El rendimiento sube 21%: unos 3% anuales con aversión de 1 y ~1% con aversión de 3.
  - Un predictor genuino puede fallar durante periodos largos.
- **Welch-Goyal (2008)** [65]: en los 30 años previos, los modelos fallaron dentro y fuera de muestra y fueron inestables. **Goyal-Welch-Zafirov (2024)** [66] revisan 29 variables nuevas y las 17 originales con datos a 2021. La mitad de las nuevas no es significativa ni dentro de muestra. De las que sí, la mitad falla fuera. Unas pocas funcionan.
- **"Virtud de la complejidad":**
  - Kelly-Malamud-Zhou (2024) [67] demuestran que, en teoría, los modelos con más parámetros que observaciones dominan a los simples.
  - Nagel (2025) [68]: con P ≫ T, el pronóstico con RFF es un promedio ponderado de los T rendimientos de entrenamiento según su similitud. En ventanas cortas esa similitud es proximidad temporal, así que el pronóstico se vuelve **momentum cronometrado por volatilidad**. Con datos artificiales de reversión construye la misma estrategia, y le va mal.
  - Buncic (2025) [69] también lo critica (solo título verificado).

### 2.12 Causalidad contra correlación

Un predictor puede servir sin ser causal, pero **solo si es estable**, y la estabilidad requiere un mecanismo. Las amenazas son confusores, causalidad inversa, selección y supervivencia, *look-ahead*, colisionadores y cambios de régimen. Las herramientas son experimentos naturales (inclusiones en índices, cambios regulatorios), diferencias en diferencias, variables instrumentales, regresión discontinua y **DML** (Chernozhukov et al. 2018 [70]). DML usa momentos Neyman-ortogonales y *cross-fitting*, y logra inferencia √N-consistente con ML en los parámetros de estorbo.

López de Prado (2023) [71] observa que la literatura de factores hace afirmaciones de asociación, sin grafo causal y sin experimentos falsables. Distingue afirmaciones espurias de tipo A y de tipo B. Sin teoría causal, dice, los hallazgos "probablemente son falsos".

- **Errores no estándar** (Menkveld et al. 2024) [72]: 164 equipos probaron las mismas hipótesis con los mismos datos. La dispersión entre equipos fue **considerable**, menor en la investigación más reproducible, y la revisión por pares la redujo. Los participantes la **subestimaron**.
- **Errores de IA** (Huang-Menkveld-Yu 2026) [73]: al repetir ese experimento, las IAs se concentran en pocas rutas de análisis y tienen **mucha menos dispersión**. En tareas complejas sus estimaciones se desvían **sistemáticamente** del referente humano, sobre todo por la elección del modelo estadístico.

*Inferencia:* las IAs rivales pueden compartir sesgos, y sus errores estarían correlacionados. La ventaja no vendrá de "ser IA", sino de la disciplina del proceso.

---

## 3. Literatura y fuentes canónicas

| # | Autor(es), año | Revista | Hallazgo cuantificado | Enlace | Grado |
|---|---|---|---|---|---|
| 1 | Merton 1980 | JFE 8(4):323-361 | La precisión de la media depende del lapso; la de la varianza, de la frecuencia | [1] | A (método) |
| 2 | Lo 2002 | FAJ 58(4):36-52 | EE del SR; η(q) con autocorrelación. Con ρ = 0.2, el √12 infla 20% (cálculo propio) | [2] | A |
| 3 | Gopikrishnan et al. 1999 | PRE 60(5):5305-5316 | S&P 500 con Δt ≤ 4 días: α ≈ 3 | [5] | A |
| 4 | McNeil-Frey 2000 | JEF 7(3-4):271-300 | GARCH-EVT en dos etapas para VaR/ES condicional | [8] | A (método) |
| 5 | Newey-West 1987; 1994 | Econometrica 55(3):703; REStud 61(4):631-653 | HAC semidefinido positivo; rezagos automáticos | [9][10] | A |
| 6 | Stambaugh 1999 | JFE 54(3):375-421 | Sesgo hacia arriba con predictores persistentes | [12] | A |
| 7 | Petersen 2009 | RFS 22(1):435-480 | Errores agrupados en paneles | [11] | A |
| 8 | Fama-MacBeth 1973; Shanken 1992 | JPE 81(3):607-636; RFS 5(1):1-33 | Regresiones de sección cruzada; corrección por errores en variables | [13][14] | A |
| 9 | Gibbons-Ross-Shanken 1989 | Econometrica 57(5):1121 | Prueba F conjunta de alfas = distancia entre Sharpes | [15] | A |
| 10 | Politis-Romano 1994 | JASA 89(428):1303-1313 | Bootstrap estacionario | [17] | A |
| 11 | Ledoit-Wolf 2008 | JEF 15(5):850-859 | Diferencia de Sharpes por bootstrap estudentizado | [18] | A |
| 12 | Kosowski-Timmermann-Wermers-White 2006 | JF 61(6):2551-2595 | 1975-2002: una minoría considerable cubre costos y persiste | [19] | B |
| 13 | Fama-French 2010 | JF 65(5):1915-1947 | Pocos fondos cubren costos; hay habilidad antes de comisiones en las colas | [20] | B |
| 14 | Barras-Scaillet-Wermers 2010 | JF 65(1):179-216 | 75% con alfa neto cero; casi ninguno con habilidad para 2006 | [24] | B |
| 15 | Engle 1982; Bollerslev 1986 | Econometrica 50(4):987; JEconom 31(3):307-327 | ARCH y GARCH | [25][26] | A |
| 16 | Hansen-Lunde 2005 | JAE 20(7):873-889 | 330 modelos: nada le gana al GARCH(1,1) en FX; los asimétricos le ganan en IBM | [28] | A |
| 17 | Corsi 2009 | JFEc 7(2):174-196 | HAR-RV: memoria larga aproximada con OLS | [30] | A |
| 18 | Hamilton 1989 | Econometrica 57(2):357 | Cambio de régimen de Markov; filtro | [34] | A (método) |
| 19 | Engle-Granger 1987 | Econometrica 55(2):251 | Cointegración y corrección de errores | [37] | A (método) |
| 20 | Gatev-Goetzmann-Rouwenhorst 2006 | RFS 19(3):797-827 | Hasta 11% anual de exceso, 1962-2002 | [38] | B (histórico) |
| 21 | Do-Faff 2012 | JFR 35(2):261-287 | ~30 pb/mes neto; no rentable después de 2002 | [40] | B (decaimiento) |
| 22 | Rad-Low-Faff 2016 | QF 16(10):1541-1558 | Neto: 38/33/5 pb/mes; menos oportunidades desde 2009 | [41] | B |
| 23 | Holm 1979; BH 1995; BY 2001 | SJS 6(2):65-70; JRSS-B 57(1):289-300; AoS 29(4) | FWER por pasos; FDR; FDR con dependencia arbitraria | [49][50][51] | A |
| 24 | White 2000; Hansen 2005; Romano-Wolf 2005 | Econometrica 68(5); JBES 23(4); Econometrica 73(4) | RC, SPA y StepM | [52][53][54] | A |
| 25 | Harvey-Liu-Zhu 2016 | RFS 29(1):5-68 | Vara t > 3.0 | [55] | A (método) |
| 26 | Chordia-Goyal-Saretto 2020 | RFS 33(5):2134-2179 | Varas de 3.8 y 3.4; 45% de rechazos falsos sin corrección | [57] | A |
| 27 | McLean-Pontiff 2016 | JF 71(1):5-32 | −26% fuera de muestra; −58% después de la publicación | [47] | A |
| 28 | Chen-Zimmermann 2020 | RAPS 10(2):249-289 | Sesgo de publicación de 12.3% | [46] | A |
| 29 | Diebold-Mariano 1995; Clark-West 2007 | JBES 13(3):253-263; JEconom 138(1):291-311 | Igualdad de precisión; ajuste para anidados | [59][61] | A |
| 30 | Campbell-Thompson 2008 | RFS 21(4):1509-1531 | R²_OS; R²/S²; E/P: 0.25% → +21% de rendimiento (versión de trabajo) | [64] | B |
| 31 | Welch-Goyal 2008 | RFS 21(4):1455-1508 | Los predictores fallan dentro y fuera de muestra en los 30 años previos | [65] | A (crítica) |
| 32 | Moreira-Muir 2017 vs Cederburg et al. 2020 | JF 72(4):1611-1644; JFE 138(1):95-117 | Alfas en expansión vs 103 estrategias sin mejora fuera de muestra | [32][33] | C |
| 33 | Ang-Timmermann 2012 | ARFE 4:313-337 | Revisión de regímenes | [35] | B |
| 34 | Brown-Harlow-Starks 1996 | JF 51(1):85-110 | 334 fondos, 1976-1991: los perdedores a mitad de año suben la volatilidad | [74] | B |

---

## 4. Lo más reciente 2023-2026

1. **Jensen-Kelly-Pedersen (JF 2023)** [45]: un marco bayesiano jerárquico concluye que no hay crisis de replicación en factores. Es la respuesta más fuerte a HLZ.
2. **Kelly-Malamud-Zhou (JF 2024)** contra **Nagel (NBER w34104, ago-2025)** y **Buncic (2025)** [67][68][69]. La "complejidad virtuosa" puede ser momentum cronometrado por volatilidad disfrazado. Grado C mientras no se resuelva.
3. **Goyal-Welch-Zafirov (RFS 2024)** [66]: la predicción de la prima sigue siendo frágil con datos a 2021.
4. **Menkveld et al. (JF 2024)** [72]: los errores no estándar son considerables y subestimados.
5. **Huang-Menkveld-Yu (SSRN 2026), "AI 'Errors'"** [73]: las IAs muestran menos dispersión y sesgos sistemáticos en tareas complejas. Aplica directamente a una competencia entre IAs.
6. **Huang-Jiang-Leng-Peng (JEconom 2023)** [22] y **Hounyo-Lin (JEF 2026)** [23]: los bootstraps clásicos de fondos tienen tamaño y potencia defectuosos. Hay correcciones con Hotelling T² y con *wild bootstrap*.
7. **Shu-Yu-Mulvey (JAM 2024)** [36]: los *jump models* dan regímenes persistentes y reducen el riesgo a la baja, netos de costos, en 3 mercados de 1990 a 2023.
8. **López de Prado (Cambridge Elements, 2023)** [71]: pide factores con grafo causal.
9. **Chen-Lopez-Lira-Zimmermann (documento de trabajo, 2022-)** [58]: la minería de datos iguala a la revisión por pares, con decaimiento de ~50% después de la muestra.
10. **Dickerson-Robotti-Rossetti (arXiv 2604.07880, abr-2026)**: en bonos corporativos solo sobreviven a BH 26 de 432 especificaciones (6.0%). Detalle en cap. 04.

---

## 5. Evidencia real: qué funciona, qué no, magnitudes

| Método o uso | Qué muestra la evidencia | Magnitud | Grado |
|---|---|---|---|
| Pronosticar **volatilidad** (GARCH, HAR) | Muy predecible; HAR le gana al ingenuo | Persistencia de 0.98; QLIKE 0.41 vs 0.65, DM t = 3.2 (propio) | **A** |
| Pronosticar la **media** del mercado | R²_OS diminuto e inestable | R²_OS mensual ≈ 0.25% en los mejores casos; +21% de rendimiento relativo en teoría | **C** |
| Volatilidad para subir el Sharpe | Funciona en expansión, no en tiempo real | 103 estrategias sin mejora sistemática fuera de muestra | **C** |
| Modelos de régimen | Reducen drawdown; pocos eventos independientes | Mejor en volatilidad, drawdown máximo y Sharpe, 1990-2023 | **B/C** |
| Pairs trading por distancia o cointegración | Decaimiento fuerte | 11% bruto (1962-2002) → ~30 pb/mes neto → casi nulo después de 2002 | **C** hoy; **D** para nuestra cuenta |
| Habilidad de fondos por bootstrap | Minoría pequeña; métodos con poca potencia | 75% con alfa cero; casi ninguno con habilidad en 2006 | **B** |
| Corrección por pruebas múltiples | Imprescindible; las varas dependen del universo de búsqueda | t de 3.0 a 3.8 para señales sin teoría previa | **A** (método) |
| Shrinkage de covarianzas | Mejora carteras | Ver cap. 02 | **A** |
| Shrinkage de alfas y Sharpes | Coherente con el decaimiento real | −58% después de la publicación | **A/B** |
| Colas | Ley de potencia con α ≈ 3 en acciones; USD/MXN más pesada al alza | z = −17.8 en 1987; 104 días con \|z\|>5 contra 0.015 bajo la normal | **A** |
| ML "complejo" para timing | Disputado | Ver Nagel 2025 | **C** |
| Ranking de IAs en una temporada | Es ruido | P(la mejor gana) = 0.56 con 5 pp de ventaja | **A** (matemática) |

---

## 6. Traducción operable

### 6.1 Reglas

- **R1. Doble t y doble anual.** Toda media se reporta con t IID y t NW (L ≥ traslape; 6 por defecto en mensual), e IC95. Toda cifra anual dice si es "media × 12" o compuesta (alertas #5 y #6 del laboratorio).
- **R2. La vara depende de la búsqueda.** Una señal pre-registrada, con mecanismo y una sola prueba, exige t ≥ 2.0 y además DSR ≥ `validacion_estrategias.deflated_sharpe_min_probabilidad` (0.95). Si se exploró una familia de m ≤ 20 variantes, se aplica **Holm** a toda la familia. En exploración abierta se usa **BHY** con q = 5% y t ≥ 3.0. Una señal sin teoría previa, encontrada por minería, exige **t ≥ 3.4** (vara de sección cruzada de CGS 2020).
- **R3. Recorte para planear.** Para dimensionar, el Sharpe y el alfa de un backtest se multiplican por **0.5**, en línea con el −58% de McLean-Pontiff, o se encogen con un prior N(0, τ²) con τ = 2% anual. El DSR no reemplaza el recorte: el DSR decide si se acepta la señal y el recorte decide cuánto se espera de ella.
- **R4. Lo que puede detectar el backtest mínimo.** Con `backtest_min_anios` = 10, el SR mínimo detectable es 1.96/√10 = **0.62**, y 0.95 para t ≥ 3. Una estrategia con SR verdadero de 0.5 **no se distingue de cero** en 10 años. Solo pasa si su historia es más larga o si se prueba en varios mercados.
- **R5. Colas.** Ningún VaR normal. Los escenarios de estrés mínimos, en rendimiento simple, son −17.4% en un día para el índice de EUA (1987; −19.1% logarítmico), −13.3% para el IPC (1997) y +9.7% en un día para USD/MXN (2008). El stop y el tamaño (`riesgo_por_operacion`) se calculan suponiendo que un salto así atraviesa el stop.
- **R6. Volatilidad.** La exposición de la arena se escala con un pronóstico HAR o GARCH, no con la volatilidad de 22 días a secas. Un choque tarda en disiparse **~36 días hábiles**, así que se revisa cada semana. No se promete mejor Sharpe por esa vía: su objetivo es respetar `limites_perdida` y los cortacircuitos.
- **R7. Régimen sin *look-ahead*.** Solo se usan probabilidades filtradas. Todo modelo de régimen se compara contra la SMA200 (cap. 14) con DM o Clark-West.
- **R8. Nada de pairs trading** en la arena. Necesita venta en corto, y la disponibilidad de corto para personas físicas en GBM no se verificó en esta sesión. Además su rendimiento neto decayó a casi cero después de 2002.
- **R9. Evaluar pronósticos.**
  - Probabilidades: Brier y log score (`metricas.brier`, `metricas.log_score`), con al menos `pronosticos.min_pronosticos_para_evaluar` = 50.
  - Rendimientos: R²_OS contra la media histórica, comparado con S². DM si los modelos no están anidados y Clark-West si lo están.
- **R10. Torneo.** Una temporada (`temporada_meses` = 6) **no** califica a nadie: la mejor IA gana ≈ 56% de las veces con 5 pp de ventaja. El *prior* sobre la habilidad propia y la de los rivales no se actualiza con una sola temporada. `modo_torneo` es consistente con Brown-Harlow-Starks (1996): quien va atrás a mitad del periodo sube la varianza. *Inferencia:* subir la varianza aumenta la probabilidad de terminar primero, pero baja el crecimiento geométrico esperado. Por eso queda acotado por `cortacircuitos_drawdown` y `etf_apalancado_max`.
- **R11. Las rachas son ruido.** Con 48 operaciones por temporada (`operaciones_max_mes` = 8) y una tasa de acierto real de 55%:
  - P(racha de ≥ 3 pérdidas) = **94.5%**: la regla de reducir (`rachas.perdedoras_para_reducir` = 3) se activará casi seguro.
  - P(≥ 5 pérdidas) = **38%**: la pausa se activará en ~4 de cada 10 temporadas **aun con ventaja** (`metricas.prob_racha_perdedora`).
  - El EE de la tasa de acierto con n = 48 es de ±7.2 pp.

  *Inferencia:* esas reglas controlan el riesgo, no diagnostican el edge. Recalibrarlas le toca al dueño y no se cambia aquí.
- **R12. La fase 2 no prueba habilidad.** El requisito de 12 meses con Sharpe > 0.7 da PSR ≈ **0.75** (0.88 con 36 meses), por debajo de 0.95. Es una compuerta de riesgo, no una prueba de habilidad. Así debe comunicarse.
- **R13. Causalidad mínima.** Toda tesis cuantitativa declara su mecanismo, una predicción falsable fuera de la muestra (otro mercado, otro periodo o una consecuencia distinta) y el confusor más probable.
- **R14. No hay doble implementación sin independencia.** Otra IA u otro script con el mismo modelo no es una replicación independiente. Ya se documentaron errores correlacionados en IAs (Huang-Menkveld-Yu 2026).

### 6.2 Checklist de inferencia (antes de afirmar "funciona")

1. ¿Cuántos años calendario hay y qué SR mínimo es detectable?
2. ¿Hay t IID, t NW, IC95 y bootstrap de bloques?
3. ¿Cuántas variantes se probaron, contando las que no quedaron en el registro? ¿Qué dicen Holm, BHY y el DSR?
4. ¿Es neto de costos de GBM, de tipo de cambio y de impuestos?
5. ¿Hay tramo fuera de muestra mirado una sola vez? ¿Hay datos posteriores a la publicación?
6. ¿Hay observaciones traslapadas, predictores persistentes (Stambaugh) o probabilidades suavizadas?
7. ¿Se usa curtosis en la inferencia con α ≈ 3? Si sí, validar con bootstrap.
8. ¿El pronóstico le gana al ingenuo con DM o Clark-West, y en cuánto dinero (R²/S²)?
9. ¿Cuál es el mecanismo causal y qué lo refutaría?
10. ¿Qué resultado haría cambiar de opinión, escrito **antes** de correr?

### 6.3 Código mínimo (Python estándar; probado el 2026-09-25)

```python
import math, statistics as st
from herramientas.estadistica import newey_west   # HAC Bartlett, ya en el repo
N01 = st.NormalDist()

def p_bilateral(t): return 2 * (1 - N01.cdf(abs(t)))

def holm(p, alfa=0.05):                     # FWER por pasos
    orden = sorted(range(len(p)), key=lambda i: p[i]); m = len(p); r = [False] * m
    for k, i in enumerate(orden):
        if p[i] > alfa / (m - k): break
        r[i] = True
    return r

def bhy(p, q=0.05, dependencia_arbitraria=True):   # BH si False, BHY si True
    m = len(p); c = sum(1 / i for i in range(1, m + 1)) if dependencia_arbitraria else 1.0
    orden = sorted(range(m), key=lambda i: p[i])
    kmax = max((k for k in range(1, m + 1) if p[orden[k - 1]] <= k * q / (m * c)), default=0)
    r = [False] * m
    for i in orden[:kmax]: r[i] = True
    return r

def diebold_mariano(perd_a, perd_b, h=1):   # t > 0: B pronostica mejor que A
    return newey_west([a - b for a, b in zip(perd_a, perd_b)], rezagos=max(h - 1, 1))["t"]

def clark_west(y, f_chico, f_grande):       # anidados; una cola, rechazar si t > 1.645
    adj = [(v - a) ** 2 - ((v - b) ** 2 - (a - b) ** 2) for v, a, b in zip(y, f_chico, f_grande)]
    return newey_west(adj, rezagos=1)["t"]

def r2_oos(y, f_modelo, f_media_hist):
    return 1 - sum((a - b) ** 2 for a, b in zip(y, f_modelo)) / sum((a - b) ** 2 for a, b in zip(y, f_media_hist))

def encoger(est, ee, prior=0.0, sd_prior=0.02):
    w = sd_prior ** 2 / (sd_prior ** 2 + ee ** 2); return prior + w * (est - prior)

def mbf(t): return math.exp(-t * t / 2)    # minimo factor de Bayes
```

Prueba con t = [3.4, 2.9, 2.6, 2.2, 2.0, 1.7, 1.2, 0.8, 0.5, 0.1]. Sin corrección, 5 son "significativas". Holm deja 2, BH deja 3 y BHY deja 1. En el repo ya existen el PSR, el DSR y el E[max SR] (`herramientas/metricas.py`), además de NW, el bootstrap de bloques y `veredicto` (`herramientas/estadistica.py`). *Pendiente sugerido:* mover Holm, BHY, DM, Clark-West y R²_OS a `herramientas/estadistica.py`, con pruebas unitarias.

---

## 7. Trampas y errores comunes

1. **Usar probabilidades suavizadas** de un modelo de régimen para operar. Tienen *look-ahead* por construcción.
2. **Rendimientos traslapados con errores OLS.** El t sale inflado aproximadamente por √(horizonte).
3. **Anualizar con √12** una serie autocorrelacionada: el Sharpe sale inflado entre 10% y 30% con ρ de 0.1 a 0.3.
4. **Tratar la curtosis como parámetro** cuando α ≈ 3. Da un PSR o DSR engañoso y conviene hacer bootstrap.
5. **Bootstrap iid** con volatilidad agrupada: los intervalos salen demasiado estrechos.
6. **DM con modelos anidados.** Está sesgada contra el modelo grande: se usa Clark-West.
7. **Reportar el R² dentro de muestra** de un predictor persistente (Stambaugh) sin R²_OS.
8. **Elegir los rezagos de NW, la ventana o la muestra después de ver el t.** Es p-hacking y cuenta como variante.
9. **Fama-MacBeth sin Shanken ni NW:** los errores estándar quedan subestimados.
10. **Cointegración encontrada dentro de muestra** que se rompe fuera. En pares, la ruptura es la regla después de 2002.
11. **Olvidar el denominador de la búsqueda.** Un Sharpe de 0.9 elegido entre 200 variantes es la mediana del ruido (Monte Carlo propio).
12. **Confundir "× 12" con compuesto**, o bruto con neto. Ya ocurrió en V01 (ver registro de errores).
13. **Tratar el GARCH como pronóstico de dirección.** Pronostica el segundo momento, no el signo.
14. **Leer una temporada de 6 meses como veredicto** sobre el sistema o sobre un rival.
15. **Suponer que dos IAs que coinciden se confirman entre sí.** Sus errores están correlacionados, y la independencia exige otro código, otros datos y otra fuente.

---

## 8. Examen de titulación

1. **Una estrategia tiene SR verdadero de 0.5. ¿Cuántos años se necesitan para t ≥ 1.96, t ≥ 3 y una potencia de 80%?** 15.4, 36 y 31.4 años. T = (z/SR)².
2. **¿Por qué muestrear a diario no mejora la estimación de la media?** EE(μ̂) = σ/√T depende del lapso calendario T. La frecuencia mejora la varianza, no la media (Merton 1980).
3. **Los rendimientos mensuales tienen un AR(1) con ρ = 0.2. ¿Qué sesgo tiene anualizar el Sharpe con √12?** Lo infla ≈ 20% (η(12) = 2.88 en lugar de 3.46; Lo 2002).
4. **α de Hill ≈ 3. ¿Qué implica para la curtosis?** El cuarto momento poblacional no existe. La curtosis muestral no converge, y hay que reportar el índice de cola o los cuantiles.
5. **¿Cuántos rezagos de NW usar con rendimientos anuales muestreados cada mes?** Al menos 11, por el traslape de 12 meses. Reportar también el t IID.
6. **¿Qué es el sesgo de Stambaugh y hacia dónde va en D/P?** Es el sesgo de b̂ por la correlación entre las innovaciones y un ρ̂ sesgado. Como σ_uv < 0, b̂ se sesga hacia arriba.
7. **¿Qué mide la GRS en términos de Sharpe?** (T−N−L)/N · (SR²_tangente con activos − SR²_factores)/(1 + SR²_factores) ~ F(N, T−N−L). Pregunta si los activos aumentan el Sharpe más allá de los factores.
8. **¿Qué corrige Shanken (1992) en Fama-MacBeth?** Los errores en las betas estimadas. Multiplica la varianza por (1 + λ'Σ_f⁻¹λ).
9. **GARCH(1,1) con α + β = 0.981. ¿Cuál es la vida media de un choque de volatilidad?** ln 0.5/ln 0.981 ≈ 36 días hábiles.
10. **¿Por qué no usar DM al comparar la media histórica con una regresión que la anida?** Bajo H₀, el modelo grande agrega ruido de estimación y su MSPE sale inflado. Se usa Clark-West.
11. **E/P tiene R²_OS mensual de 0.25% y el mercado tiene S² = 1.2%. ¿Cuál es el valor económico?** Un aumento proporcional de ≈ R²/S² = 21% del rendimiento de un inversionista media-varianza (Campbell-Thompson).
12. **Diez pruebas con t = 3.4, 2.9, 2.6, 2.2, 2.0, … ¿Cuántas rechazan Holm, BH y BHY al 5%?** Holm 2, BH 3 y BHY 1. Sin corrección serían 5.
13. **¿Qué vara t proponen Chordia-Goyal-Saretto y qué fracción de rechazos sería falsa sin corrección?** 3.8 en serie de tiempo y 3.4 en sección cruzada. Alrededor de 45%.
14. **¿Qué quedó del pairs trading de GGR después de costos y después de 2002?** De hasta 11% anual bruto (1962-2002) a ~30 pb/mes ajustado por riesgo después de costos, y casi nada después de 2002 (Do-Faff). Neto, 38/33/5 pb/mes según el método (Rad-Low-Faff).
15. **Dos IAs con σ = 25% y ρ = 0.5, una con 5 pp anuales de ventaja. ¿Con qué probabilidad gana una temporada de 6 meses?** ≈ 0.556. Se necesitan ~136 temporadas para una evidencia de 95%.

---

## 9. Fuentes

Método de verificación: el presupuesto de WebSearch de la sesión ya estaba agotado cuando empezó este módulo. Se verificó con los metadatos y resúmenes de Crossref, las páginas de NBER, arXiv, Oxford Academic y Wikipedia vía WebFetch, un PDF de NBER leído directamente (Campbell-Thompson) y cálculos propios con datos públicos. Las cifras que no se confirmaron se omiten o se marcan.

1. Merton (1980), JFE 8(4):323-361 — https://doi.org/10.1016/0304-405X(80)90007-0
2. Lo (2002), FAJ 58(4):36-52 — https://doi.org/10.2469/faj.v58.n4.2453
3. Cont (2001), Quantitative Finance 1(2):223-236 — https://doi.org/10.1080/713665670
4. Mandelbrot (1963), Journal of Business 36(4):394 — https://doi.org/10.1086/294632
5. Gopikrishnan, Plerou, Amaral, Meyer, Stanley (1999), PRE 60(5):5305-5316 — https://arxiv.org/abs/cond-mat/9905305 ; https://doi.org/10.1103/PhysRevE.60.5305
6. Gabaix, Gopikrishnan, Plerou, Stanley (2003), Nature 423:267-270 — https://doi.org/10.1038/nature01624
7. Hill (1975), Annals of Statistics 3(5) — https://doi.org/10.1214/aos/1176343247
8. McNeil, Frey (2000), JEF 7(3-4):271-300 — https://doi.org/10.1016/S0927-5398(00)00012-8
9. Newey, West (1987), Econometrica 55(3):703 — https://doi.org/10.2307/1913610
10. Newey, West (1994), REStud 61(4):631-653 — https://doi.org/10.2307/2297912
11. Petersen (2009), RFS 22(1):435-480 — https://doi.org/10.1093/rfs/hhn053
12. Stambaugh (1999), JFE 54(3):375-421 — https://doi.org/10.1016/S0304-405X(99)00041-0
13. Fama, MacBeth (1973), JPE 81(3):607-636 — https://ideas.repec.org/a/ucp/jpolec/v81y1973i3p607-36.html
14. Shanken (1992), RFS 5(1):1-33 — https://doi.org/10.1093/rfs/5.1.1
15. Gibbons, Ross, Shanken (1989), Econometrica 57(5):1121 — https://doi.org/10.2307/1913625
16. Efron (1979), Annals of Statistics 7(1) — https://doi.org/10.1214/aos/1176344552
17. Politis, Romano (1994), JASA 89(428):1303-1313 — https://doi.org/10.1080/01621459.1994.10476870
18. Ledoit, Wolf (2008), JEF 15(5):850-859 — https://doi.org/10.1016/j.jempfin.2008.03.002
19. Kosowski, Timmermann, Wermers, White (2006), JF 61(6):2551-2595 — https://doi.org/10.1111/j.1540-6261.2006.01015.x
20. Fama, French (2010), JF 65(5):1915-1947 — https://doi.org/10.1111/j.1540-6261.2010.01598.x
21. Harvey, Liu (2022), JF 77(3):1921-1966 — https://doi.org/10.1111/jofi.13123
22. Huang, Jiang, Leng, Peng (2023), JEconom 235(1):239-255 — https://doi.org/10.1016/j.jeconom.2022.03.011
23. Hounyo, Lin (2026), JEF 85:101673 — https://doi.org/10.1016/j.jempfin.2025.101673
24. Barras, Scaillet, Wermers (2010), JF 65(1):179-216 — https://doi.org/10.1111/j.1540-6261.2009.01527.x
25. Engle (1982), Econometrica 50(4):987 — https://doi.org/10.2307/1912773
26. Bollerslev (1986), JEconom 31(3):307-327 — https://doi.org/10.1016/0304-4076(86)90063-1
27. Nobel 2003 (Engle y Granger) — https://en.wikipedia.org/wiki/Clive_Granger
28. Hansen, Lunde (2005), JAE 20(7):873-889 — https://doi.org/10.1002/jae.800
29. Andersen, Bollerslev (1998), IER 39(4):885 — https://doi.org/10.2307/2527343
30. Corsi (2009), JFEc 7(2):174-196 — https://doi.org/10.1093/jjfinec/nbp001
31. Bollerslev, Patton, Quaedvlieg (2016), JEconom 192(1):1-18 — https://doi.org/10.1016/j.jeconom.2015.10.007
32. Moreira, Muir (2017), JF 72(4):1611-1644 — https://doi.org/10.1111/jofi.12513
33. Cederburg, O'Doherty, Wang, Yan (2020), JFE 138(1):95-117 — https://doi.org/10.1016/j.jfineco.2020.04.015
34. Hamilton (1989), Econometrica 57(2):357 — https://doi.org/10.2307/1912559
35. Ang, Timmermann (2012), ARFE 4:313-337 — https://doi.org/10.1146/annurev-financial-110311-101808
36. Shu, Yu, Mulvey (2024), J. of Asset Management 25(5):493-507 — https://doi.org/10.1057/s41260-024-00376-x ; https://arxiv.org/abs/2402.05272
37. Engle, Granger (1987), Econometrica 55(2):251 — https://doi.org/10.2307/1913236
38. Gatev, Goetzmann, Rouwenhorst (2006), RFS 19(3):797-827 — https://doi.org/10.1093/rfs/hhj020 ; https://www.nber.org/papers/w7032
39. Do, Faff (2010), FAJ 66(4):83-95 — https://doi.org/10.2469/faj.v66.n4.1
40. Do, Faff (2012), JFR 35(2):261-287 — https://doi.org/10.1111/j.1475-6803.2012.01317.x
41. Rad, Low, Faff (2016), QF 16(10):1541-1558 — https://doi.org/10.1080/14697688.2016.1164337
42. Jorion (1986), JFQA 21(3):279 — https://doi.org/10.2307/2331042
43. Ledoit, Wolf (2003), JEF 10(5):603-621 — https://doi.org/10.1016/S0927-5398(03)00007-0
44. Kozak, Nagel, Santosh (2020), JFE 135(2):271-292 — https://doi.org/10.1016/j.jfineco.2019.06.008
45. Jensen, Kelly, Pedersen (2023), JF 78(5):2465-2518 — https://doi.org/10.1111/jofi.13249 ; https://www.nber.org/papers/w28432
46. Chen, Zimmermann (2020), RAPS 10(2):249-289 — https://doi.org/10.1093/rapstu/raz011
47. McLean, Pontiff (2016), JF 71(1):5-32 — https://doi.org/10.1111/jofi.12365
48. Harvey (2017), JF 72(4):1399-1440 — https://doi.org/10.1111/jofi.12530
49. Holm (1979), Scandinavian Journal of Statistics 6(2):65-70 — https://en.wikipedia.org/wiki/Holm%E2%80%93Bonferroni_method
50. Benjamini, Hochberg (1995), JRSS-B 57(1):289-300 — https://doi.org/10.1111/j.2517-6161.1995.tb02031.x
51. Benjamini, Yekutieli (2001), Annals of Statistics 29(4) — https://doi.org/10.1214/aos/1013699998
52. White (2000), Econometrica 68(5):1097-1126 — https://doi.org/10.1111/1468-0262.00152
53. Hansen (2005), JBES 23(4):365-380 — https://doi.org/10.1198/073500105000000063
54. Romano, Wolf (2005), Econometrica 73(4):1237-1282 — https://doi.org/10.1111/j.1468-0262.2005.00615.x
55. Harvey, Liu, Zhu (2016), RFS 29(1):5-68 — https://doi.org/10.1093/rfs/hhv059 ; https://www.nber.org/papers/w20592
56. Harvey, Liu (2020), JF 75(5):2503-2553 — https://doi.org/10.1111/jofi.12951
57. Chordia, Goyal, Saretto (2020), RFS 33(5):2134-2179 — https://doi.org/10.1093/rfs/hhaa018
58. Chen, Lopez-Lira, Zimmermann, "Does Peer-Reviewed Research Help Predict Stock Returns?" (documento de trabajo) — https://doi.org/10.2139/ssrn.4308069
59. Diebold, Mariano (1995), JBES 13(3):253-263 — https://doi.org/10.1080/07350015.1995.10524599
60. Diebold (2015), JBES 33(1) — https://doi.org/10.1080/07350015.2014.983236
61. Clark, West (2007), JEconom 138(1):291-311 — https://doi.org/10.1016/j.jeconom.2006.05.023
62. Giacomini, White (2006), Econometrica 74(6):1545-1578 — https://doi.org/10.1111/j.1468-0262.2006.00718.x
63. Pesaran, Timmermann (1992), JBES 10(4):461-465 — https://doi.org/10.1080/07350015.1992.10509922
64. Campbell, Thompson (2008), RFS 21(4):1509-1531 — https://doi.org/10.1093/rfs/hhm055 ; versión de trabajo con las cifras citadas: https://www.nber.org/papers/w11468
65. Welch, Goyal (2008), RFS 21(4):1455-1508 — https://doi.org/10.1093/rfs/hhm014
66. Goyal, Welch, Zafirov (2024), RFS 37(11) — https://academic.oup.com/rfs/article/37/11/3490/7749383
67. Kelly, Malamud, Zhou (2024), JF 79(1):459-503 — https://doi.org/10.1111/jofi.13298
68. Nagel (2025), "Seemingly Virtuous Complexity in Return Prediction", NBER w34104 — https://www.nber.org/papers/w34104
69. Buncic (2025), "Simplified: A Closer Look at the Virtue of Complexity in Return Prediction" — https://doi.org/10.2139/ssrn.5239006
70. Chernozhukov et al. (2018), Econometrics Journal 21(1):C1-C68 — https://doi.org/10.1111/ectj.12097
71. López de Prado (2023), *Causal Factor Investing*, Cambridge Elements — https://doi.org/10.1017/9781009397315
72. Menkveld et al. (2024), "Nonstandard Errors", JF 79(3):2339-2390 — https://doi.org/10.1111/jofi.13337
73. Huang, Menkveld, Yu (2026), "AI 'Errors'" — https://doi.org/10.2139/ssrn.6408138
74. Brown, Harlow, Starks (1996), JF 51(1):85-110 — https://doi.org/10.1111/j.1540-6261.1996.tb05203.x
75. Cálculos propios: `laboratorio/ilustraciones/M20_hechos_estilizados.py` y `M20-salida.txt`. Datos: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html (versión 202607) y Yahoo Finance (^GSPC, ^MXX, MXN=X) al 24-sep-2026.
