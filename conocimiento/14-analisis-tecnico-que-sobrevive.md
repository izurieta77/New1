# Módulo 14 — Análisis técnico: qué sobrevive a la evidencia

> Nivel: maestría aplicada / doctorado de practicante · Actualizado: 2026-09-25 · Grado de evidencia global: **B/D (bimodal)**. Sobrevive, fuera de muestra y neto de costos pero con magnitudes modestas y decaimiento, la **tendencia de mediano plazo** (medias móviles lentas, momentum de series de tiempo, cercanía al máximo de 52 semanas, indicadores técnicos agregados como predictores de la prima de mercado): **B**. No sobrevive a la corrección por *data snooping* ni a costos: reglas diarias de corto plazo en índices maduros, velas japonesas, patrones gráficos a ojo, Fibonacci, Elliott y métodos de practicante vendidos como paquete: **D**. Las señales de *machine learning* sobre gráficas son potentes en bruto pero dependen de rotación alta y de ponderar igual a las acciones pequeñas: **C** para una cuenta de MXN 20,000 ejecutada a mano.

---

## 1. Objetivos de dominio

Quien apruebe este módulo debe poder, con números y sin ayuda:

1. Formular una regla técnica como pronóstico E[r | historia] y separar su ganancia en timing, menor exposición y costos.
2. Distinguir los mecanismos que generan predictibilidad real (aprendizaje, anclaje, microestructura de órdenes, cobertura gamma, prima de riesgo variable) de los que la fabrican (data snooping, trading no sincrónico, look-ahead).
3. Reproducir el arco BLL 1992 → Bessembinder-Chan 1998 → STW 1999 → Ready 2002 → Bajgrowicz-Scaillet 2012 → Rink 2023 con sus cifras clave.
4. Calcular el costo de equilibrio de una regla y descartarla si no cubre 3 veces el costo por lado en GBM.
5. Cuantificar por qué una media móvil sobre el índice mejora más el drawdown que el CAGR (Faber: 83.66% → 42.24%; 9.32% → 10.18%, bruto).
6. Graduar cada señal de sección cruzada (52 semanas, volumen, MAD, *trend factor*, CNN) y su viabilidad en una cuenta chica.
7. Explicar por qué velas, figuras, Fibonacci y Elliott están prohibidos como señal de decisión.
8. Auditar un backtest técnico contra `validacion_estrategias` de `config/parametros.json`.
9. Justificar con evidencia el `filtro_apalancados` de la cuenta arena y proponer mejoras falsables.
10. Recitar la lista de indicadores permitidos (grado y función) y la de prohibidos.

---

## 2. Núcleo teórico / marco

### 2.1 Definición operacional

Una regla técnica es un mapeo S_t = f(P_{t}, P_{t-1}, …, V_t, V_{t-1}, …) → {exposición}. Su ganancia esperada frente a *buy-and-hold* es, por construcción:

E[R_regla] − E[R_B&H] = Cov(S_t, r_{t+1}) + (E[S] − 1)·E[r] − costos, con r = rendimiento en exceso sobre efectivo (CETES) y S entre 0 y 1.

El primer término es el único "alfa de timing"; el segundo es simplemente estar menos invertido (y ganar menos prima en promedio); el tercero casi siempre se subestima. Cualquier backtest que no separe estos tres términos no dice nada. La forma débil de eficiencia (Fama 1970; ver Cap. 01) predice Cov(S_t, r_{t+1}) ≈ 0 después de costos.

### 2.2 Mecanismos que generan predictibilidad real

| Mecanismo | Predicción | Evidencia ancla |
|---|---|---|
| Aprendizaje racional gradual / incertidumbre sobre parámetros | Las medias móviles agregan valor a reglas de asignación fija cuando hay predictibilidad o incertidumbre del modelo | Zhu-Zhou 2009 [13] (teoría); Detzel et al. 2021 [63] (modelo de equilibrio + Bitcoin y acciones difíciles de valuar) |
| Anclaje | Precio cercano al máximo de 52 semanas → subreacción a buenas noticias | George-Hwang 2004 |
| Microestructura de órdenes | Órdenes *stop-loss* y *take-profit* agrupadas en números redondos: *take-profit* frena tendencias en soportes/resistencias; *stop-loss* las acelera al romperlos | Osler 2000, 2003 |
| Flujos de cobertura | La cobertura gamma de *market makers* de opciones y ETFs apalancados empuja el cierre en la dirección del día | Baltussen-Da-Lammers-Martens 2021 |
| Clientelas overnight vs intradía | Momentum se gana de noche; casi todo lo demás, de día | Lou-Polk-Skouras 2019 |
| Prima de riesgo variable | Los indicadores técnicos detectan la caída de la prima cerca de picos del ciclo | Neely-Rapach-Tu-Zhou 2014 |

### 2.3 Mecanismos que fabrican predictibilidad falsa

1. **Data snooping.** Si se prueban K reglas sobre la misma serie, la mejor tendrá un p-valor nominal ínfimo aunque ninguna sirva. Sullivan-Timmermann-White (1999) usaron 7,846 reglas; el White *Reality Check* ajusta el p-valor por el universo completo del que se eligió la regla. Sucesores: SPA de Hansen, *stepwise* SPA (Hsu-Hsu-Kuan 2010), *False Discovery Rate* (Bajgrowicz-Scaillet 2012). En el sistema: `herramientas/metricas.py → sharpe_deflactado` (ver Cap. 07).
2. **Trading no sincrónico.** Un índice o portafolio con componentes ilíquidos incorpora información con rezago; su rendimiento tiene autocorrelación positiva mecánica que una media móvil "captura" pero nadie puede operar. Bessembinder-Chan (1998) atribuyen parte (no todo) del poder de BLL a este error de medición.
3. **Look-ahead.** Calcular la señal con el cierre de hoy y asignar el rendimiento de hoy. Zakamulin mostró que el desempeño extraordinario reportado por Glabadanidis para medias móviles venía de ese sesgo; sin él, el timing es apenas mejor e indistinguible estadísticamente de *buy-and-hold*.

### 2.4 La matemática que sí juega a favor de la tendencia: volatility drag

El crecimiento geométrico ≈ μ − σ²/2 (Cap. 01). Una regla que sale del mercado en regímenes de alta volatilidad puede **igualar la media aritmética y subir la geométrica**. Faber (actualización 2013, S&P 500 1901-2012): media aritmética 11.26% (B&H) vs 11.22% (timing), pero CAGR 9.32% vs 10.18% y drawdown máximo 83.66% vs 42.24%, con ~70% del tiempo invertido y menos de una ida y vuelta al año (bruto de impuestos, comisiones y deslizamiento).

Para un ETF apalancado L× con rebalanceo diario, el drag aproximado es L²σ²/2: con σ = 20% anual, 1× pierde ~2% por drag y 3× pierde ~18%; con σ = 12%, 3× pierde ~6.5%. *Inferencia:* como la volatilidad se agrupa y los precios bajo su media de 200 días coinciden con regímenes de mayor volatilidad (ver 2.2 y el patrón recesivo de Neely et al.), un filtro de tendencia es mucho más valioso sobre un apalancado que sobre el índice 1×. Ese es el fundamento del `filtro_apalancados` de la cuenta arena.

### 2.5 Costo de equilibrio (*break-even cost*, BETC)

BETC por operación (un sentido) = exceso de rendimiento anual bruto / número de operaciones de un sentido por año.

- BLL sobre el Dow: BETC de un sentido de 0.39% en toda la muestra y 0.22% desde 1975 (Bessembinder-Chan 1998).
- Media de 10 días de Han-Yang-Zhou: ~20% de los días con operación y BETC de ~29 a 65 puntos base por operación según el decil.
- GBM (persona física): comisión de 0.25% a 0.10% por operación según el saldo promedio de 3 meses, más IVA (verificar en la guía vigente de GBM [64]; detalle en Cap. 11), más *spread*. *Inferencia:* con MXN 20,000 el costo realista es ≥ 0.3% por lado (≥ 0.6% ida y vuelta) antes de *spread*. **Regla de las 3×:** el BETC por operación de un sentido debe ser ≥ 3 veces el costo por lado, es decir ≥ ~0.9%; si no, la regla queda fuera.

### 2.6 Taxonomía que usa el sistema

**Time-series** (timing de un activo contra efectivo: medias móviles, signo del rendimiento de 12 meses, rupturas de rango) · **cross-section** (ordenar activos: momentum 12-1, 52 semanas, MAD, volumen) · **intradía/microestructura** (momentum intradía, overnight vs intradía, soportes y resistencias) · **patrones y narrativas** (velas, figuras, Fibonacci, Elliott) · **contexto** (amplitud y sentimiento).

---

## 3. Literatura y fuentes canónicas

### 3.1 Reglas sobre índices y el problema de data snooping

| Estudio | Muestra | Hallazgo cuantificado | IS/OOS · bruto/neto | Grado | Fuente |
|---|---|---|---|---|---|
| Brock-Lakonishok-LeBaron 1992, JF 47(5) | Dow 1897-1986, 26 reglas (VMA, FMA, ruptura de rango) | Días de compra +0.042% diario (~12% anual); días de venta −0.025% (~−7% anual); menos volatilidad en días de compra; rechaza caminata aleatoria, AR(1), GARCH-M, EGARCH por bootstrap (cifras vía resumen secundario [3]) | IS, bruto | C (histórico) | [1] |
| Bessembinder-Chan 1998, FM 27(2) | Mismas reglas | BETC de un sentido 0.39% (total) y 0.22% (desde 1975); parte del poder viene de trading no sincrónico | IS, break-even | B (como refutación) | [4] |
| Sullivan-Timmermann-White 1999, JF 54(5) | Dow 1897-1996, 7,846 reglas | Mejor regla 1897-1986: 18.65% anual, *Reality Check* p≈0. Fuera de muestra 1987-1996: la mejor da 14.41% pero con p = 0.341 (p nominal 0.004); futuros S&P 500 1984-1996: p = 0.908 | IS vs OOS, bruto | A (el método) | [5][6] |
| Ready 2002, FM | Dow; compara BLL con reglas de algoritmo genético | El éxito de BLL después de costos es probablemente espurio (snooping); deslizamiento entre señal y ejecución; 0.1% de costo es demasiado bajo; la capacidad de las reglas cayó drásticamente en los 6-8 años previos | OOS, neto | A | [7] |
| Park-Irwin 2007, JES 21(4) | Revisión de 95 estudios "modernos" | 56 de 95 con resultados positivos; en acciones de EUA, rentables hasta finales de los 80; problemas recurrentes: snooping, selección ex post, costos | Revisión | A (diagnóstico) | [8] |
| Ratner-Leal 1999, JBF 23 | 10 reglas VMA, 10 mercados emergentes, 1982-1995 | Después de costos, solo **Taiwán, México y Tailandia** conservan rentabilidad | IS, neto | C (histórico, pre-ETF) | [9] |
| Hsu-Kuan 2005 (SSRN) | DJIA, S&P 500, NASDAQ, Russell 2000 | Con Reality Check: reglas rentables en NASDAQ y Russell 2000, no en DJIA ni S&P 500 | IS y OOS, neto | B− | [10] |
| Hsu-Hsu-Kuan 2010, JEF 17(3) | Índices de crecimiento y emergentes y sus ETFs | *Stepwise* SPA: poder predictivo significativo que **se debilita tras la introducción de los ETFs** | IS/OOS | A (el patrón de decaimiento) | [11] |
| Bajgrowicz-Scaillet 2012, JFE 106(3) | Dow 1897-2011, FDR | Nadie habría podido elegir ex ante las mejores reglas futuras; aun dentro de muestra, costos bajos eliminan el desempeño | IS/OOS, neto | A | [12] |
| Neely-Rapach-Tu-Zhou 2014, MS 60(7) | S&P 500 1950:12-2011:12; 14 indicadores (MA(s,l) s=1,2,3, l=9,12 meses; MOM 9 y 12; OBV) | Los 14 tienen R²_OS > 0 (1966-2011); PC-TECH R²_OS 0.65%; PC-ALL (técnicos + macro) 1.79%, **11.24% en recesiones y −2.80% en expansiones**; ganancia CER hasta 317 pb, hasta 282 pb neta de 50 pb por operación | IS y OOS, neto | B+ | [14][15] |
| Faber 2007/2013 | S&P 500 1901-2012, SMA 10 meses mensual | CAGR 10.18% vs 9.32%; DD 42.24% vs 83.66%; ~70% invertido; < 1 ida y vuelta al año | Bruto (sin costos ni impuestos) | B (drawdown) / C (CAGR) | [16] |
| Zakamulin (SSRN 2743119) | S&P 500, *forward testing*, costos | Sin look-ahead, la media móvil apenas supera a B&H e **indistinguible estadísticamente** | OOS, neto | A (corrección) | [17] |

### 3.2 Sección cruzada, volumen y microestructura

| Estudio | Muestra | Hallazgo cuantificado | IS/OOS · bruto/neto | Grado | Fuente |
|---|---|---|---|---|---|
| George-Hwang 2004, JF 59(5) | EUA 1963-2001 | Estrategias (6,6) de JT, industria y 52 semanas ~0.45% mensual cada una; en regresión conjunta 52 semanas 0.65% vs JT 0.38% vs industria 0.25% (fuera de enero 1.06% vs 0.46% vs 0.22%); **sin reversión de largo plazo** | IS, bruto | B | [18] |
| Lee-Swaminathan 2000, JF 55(5) | EUA | Alta rotación = acciones "glamour" con menor rendimiento futuro; ganadores de bajo volumen y perdedores de alto volumen continúan hasta 3 años; momentum revierte en 5 años | IS, bruto | B− | [19] |
| Gervais-Kaniel-Mingelgrin 2001, JF 56(3) | EUA | Volumen inusualmente alto en un día o semana → apreciación en el mes siguiente (efecto visibilidad) | IS, bruto | C+ | [20] |
| Han-Yang-Zhou 2013, JFQA 48(5) | Deciles por volatilidad, jul-1963 a dic-2009 | MA de 10 días vs B&H: 8.42% a 18.70% anual; alfa FF3 de 9.80% a 23.54%; con MA de 200 días, mayormente > 5%; BETC ~29-65 pb | IS, break-even | C (nivel portafolio; en acciones individuales no se sostiene) | [21][22] |
| Han-Zhou-Zhu 2016, JFE 122(2) | Sección cruzada EUA | *Trend factor* (combina medias móviles de horizontes corto, intermedio y largo): 1.63% mensual, Sharpe mensual 0.47 vs 0.23 (reversión corta), 0.10 (momentum), 0.10 (reversión larga); en la crisis financiera +0.75% mensual vs momentum −3.88% | IS, bruto | C+ | [23][24] |
| Avramov-Kaplanski-Subrahmanyam 2021, RFE 39(2) | Sección cruzada EUA | MAD = MA21/MA200; alfa ponderado por valor ~9% anual; sobrevive costos institucionales; más fuerte del lado largo | IS, neto institucional | B− | [25] |
| Gao-Han-Li-Zhou 2018, JFE 129(2) | SPY 1993-2013 | El rendimiento de la primera media hora (desde el cierre previo) predice la última media hora; más fuerte con volatilidad, volumen, recesión y días de noticias macro | IS y OOS | B (existencia) | [26] |
| Baltussen-Da-Lammers-Martens 2021, JFE 142 | 60+ futuros 1974-2020 | Últimos 30 minutos predichos por el resto del día; revierte en días siguientes; ligado a cobertura gamma | IS/OOS | B | [27] |
| Lou-Polk-Skouras 2019, JFE 134(1) | EUA 1993-2013, 14 estrategias | **Momentum se gana íntegro overnight**; las demás estrategias, intradía. Decil ganador-perdedor overnight: alfa overnight 3.47% mensual, alfa intradía −3.02% mensual | IS, bruto | B (conocimiento) | [28] |
| Osler 2000, FRBNY EPR 6(2) | Niveles S/R publicados por 6 firmas, USD/JPY, USD/GBP, USD/DEM, 1996-98 | Predicen interrupciones de tendencia intradía durante al menos 5 días hábiles; poder muy desigual entre firmas | IS | C+ (FX intradía) | [29][30] |
| Osler 2003, JF 58(5) | Órdenes de un banco de FX | *Stop-loss* y *take-profit* agrupados en números redondos; explica rebotes en S/R y aceleración al romperlos | Mecanismo | B | [31] |

### 3.3 Patrones, velas y métodos de practicante

| Estudio | Muestra | Hallazgo | Grado | Fuente |
|---|---|---|---|---|
| Lo-Mamaysky-Wang 2000, JF | Acciones EUA 1962-1996, reconocimiento por regresión kernel | Varios patrones cambian la distribución condicional de rendimientos (información incremental); **no prueba rentabilidad neta**; los patrones clásicos pueden no ser óptimos | C | [32][33] |
| Chang-Osler 1999, EJ 109 | H&S en FX diario 1973-1994 | Rentable en algunas monedas, pero **dominado por reglas más simples** (medias móviles, momentum) | C− | [34] |
| Savin-Weller-Zvingelis 2007, JFEc 5(2) | S&P 500 y Russell 2000, 1990-1999 | Poca o nula rentabilidad como estrategia aislada; exceso ajustado por riesgo de 5-7% anual condicionado al patrón, **en parte por identificar momentum negativo** | C− | [35][36] |
| Marshall-Young-Rose 2006, JBF 30 | Acciones del DJIA 1992-2001, bootstrap | Las velas japonesas **no superan al trading aleatorio** | D (señal) / A (el resultado negativo) | [37] |
| Olson et al. 1998 (vía resumen secundario; revista no verificada) | S&P 500, 1984-1992 | CAN SLIM: 1.81% mensual ajustado por mercado | D (IS, pequeño, sin réplica OOS) | [38] |
| FFTY (IBD 50) en vivo | abr-2015 a sep-2026 | 3.47% anual desde el inicio (al 2026-09-25), gasto 0.80%; de abr-2015 a dic-2016, −3.4% vs +11.1% del S&P 500; el índice "reconstruido" 2003-2015 superaba al S&P ~9% anual | D | [39][40] |
| Chague-De-Losso-Giovannetti 2019 (WP) | Day traders de futuros del índice en Brasil que empezaron en 2013-2015 | 97% de quienes persistieron más de 300 días perdió dinero; ~1.1% ganó más que el salario mínimo; sin evidencia de aprendizaje | A (resultado negativo) | [41] |

### 3.4 Tendencia multiactivo, amplitud y sentimiento

| Estudio | Hallazgo | Grado | Fuente |
|---|---|---|---|
| Hurst-Ooi-Pedersen 2017, JPM | 67 mercados, 1880-2016: momentum de series de tiempo con rendimiento promedio positivo en **cada década**; bien en 8 de las 10 peores crisis de un 60/40 | B | [42] |
| Huang-Li-Wang-Zhou 2020, JFE 135(3) | El t-estadístico de la regresión *pooled* no es confiable frente a bootstrap; activo por activo hay **poca evidencia** de TSM dentro y fuera de muestra | A (crítica) | [43] |
| Baker-Wurgler 2006, JF 61(4) | Con sentimiento inicial bajo, las acciones pequeñas, jóvenes, volátiles, no rentables, sin dividendo, de crecimiento extremo y en problemas rinden relativamente más; con sentimiento alto, relativamente menos | B | [44] |
| Huang-Jiang-Tu-Zhou 2015, RFS 28(3) | Índice de sentimiento "alineado" (PLS sobre 6 proxies) predice el mercado agregado | B− | [45] |
| Zaremba et al. 2021, Economic Modelling | Amplitud (avances − retrocesos) predice rendimientos de índices e industrias en 64 países, 1973-2018; robusto a tamaño, estilo, momentum y tendencia; **la rentabilidad cae ~50% con tenencias de 2-3 meses** | B− | [46] |

---

## 4. Lo más reciente 2023-2026

1. **Rink 2023, *Financial Markets and Portfolio Management* 37(4).** 6,406 reglas, 23 mercados desarrollados y 18 emergentes, hasta 66 años de datos, prueba SPA de última generación. Dentro de muestra, mayoría de mercados con reglas superiores a B&H, más en emergentes; **la predictibilidad cae drásticamente con el tiempo en todos los mercados**; muy sensible a costos moderados; fuera de muestra, las reglas recientemente ganadoras rinden **significativamente peor** que B&H [47]. Es la mejor síntesis vigente: el análisis técnico sobre índices amplios es una anomalía histórica en extinción.
2. **Goyal-Welch-Zafirov 2024, RFS 37(11).** Reexaminan 29 predictores publicados después de 2008 más los 17 originales, con datos a 2021: más de un tercio ya no es significativo ni dentro de muestra y la mitad de los que sí lo son fallan fuera de muestra [48]. En la presentación de los autores, los **14 indicadores técnicos de Neely et al.** aparecen entre sus "favoritos", el ~10% de variables que siguen funcionando [49]. Esto sube la regla de tendencia agregada a B+: sobrevive a publicación y a la prueba más hostil de la literatura, con R² de un dígito bajo.
3. **Jiang-Kelly-Xiu 2023, JF 78(6).** Redes convolucionales sobre imágenes de 5, 20 y 60 días con OHLC, volumen y media móvil. Deciles long-short con Sharpe **bruto** fuera de muestra de hasta 7.2 equiponderado y 1.7 ponderado por valor; los mejores rivales tradicionales (TREND y reversión semanal) logran 2.9 y 2.8 equiponderado (0.7 y 0.8 por valor) [50][51]. Lectura correcta: hay estructura no lineal en las gráficas, pero *inferencia* (por la brecha entre equiponderado y ponderado por valor): la cifra espectacular vive en acciones pequeñas con rotación semanal; neta y en una cuenta chica, no aplica.
4. **Murray-Xia-Xiao 2024, JFE 153 ("Charting by machines").** ML sobre rendimientos pasados predice la sección cruzada **incluso entre las 500 mayores acciones**; no linealidades estables en el tiempo y distintas de momentum, reversión y señales técnicas conocidas [52]. Es la evidencia más fuerte a favor de que "la gráfica contiene información"; no de que un humano o un LLM la extraiga mirando.
5. **Réplica del momentum intradía (Limkriangkrai-Chai-Zheng 2023, PBFJ 80).** EUA 1996-2013: R² dentro de muestra 1.7% con la primera media hora; R²_OS 1.7% y 2.3% combinando la penúltima media hora; persiste en EUA durante el COVID. En Asia-Pacífico solo China y Japón; nada en Hong Kong ni Singapur [53].
6. **Overnight drift: descubrimiento y muerte.** Boyarchenko-Larsen-Whelan (RFS 2023) documentan que casi toda la prima de renta variable de EUA se ganaba entre 2:00 y 3:00 a.m. ET, en la apertura europea [54]. Los mismos autores (Liberty Street, julio 2026): ~3.7% anualizado en esa ventana en 1998-2020 (más del 60% del 5.9% anual cierre a cierre del futuro), **cerca de cero desde 2021**; la dispersión del desequilibrio de órdenes al cierre cayó de 6.5% a 2.9%; dos ETFs lanzados en 2022 para capturarlo cerraron a los 14 meses [55]. Caso de libro de decaimiento post-publicación.
7. **Sentimiento AAII (Gómez-Martínez et al. 2026, IREF).** 25 años semanales, reglas contrarias sobre el diferencial alcista-bajista, netas de costos: utilidades positivas en los extremos y mejor eficiencia de drawdown, pero **ninguna supera el Sharpe de estar largo pasivo** [56].
8. **Tendencia multiactivo en vivo.** SG Trend Index (10 mayores CTAs de tendencia): +2.4% en 2024; −15.05% en los 12 meses a junio de 2025, con drawdown de 20.61%; 4.90% anualizado desde 2000 [57]. Diversifica crisis largas; no es una máquina de rendimiento.
9. **LLMs y modelos de visión leyendo gráficas.** Benchmark de 2026 sobre velas: exactitud direccional de 49% a 53.5% (mejor: Claude Sonnet 4.5 con razonamiento, 53.48%, vs XGBoost 50.87%), IC ≈ 0.05 en el mejor caso, y más correlación con el rendimiento a 5 días que a 30 aunque se pidió 30 [58]. LiveTradeBench (2025): 21 LLMs, 50 días en vivo; un puntaje alto en LMArena no implica mejor trading [59]. *Inferencia:* un rival de la arena que "lea gráficas" con un LLM tiene, en el mejor caso, 1 a 3 puntos de ventaja direccional, que las comisiones se comen.

---

## 5. Evidencia real: qué funciona, qué no, magnitudes

### 5.1 Tendencia lenta sobre índices (TS): B

- **Funciona para lo que realmente hace:** cortar la cola izquierda. Faber: drawdown a la mitad (83.66% → 42.24%) con CAGR similar o apenas mayor, bruto. Zakamulin: sin look-ahead y con costos, rendimiento estadísticamente indistinguible de B&H. *Inferencia:* su valor está en la **geometría** (menos varianza, menos drawdown, más supervivencia en torneo), no en la media.
- **Como predictor de prima:** R² fuera de muestra de 0.65% a 1.79% (Neely et al.), concentrado en recesiones; sobrevive a Goyal-Welch-Zafirov 2024; ganancias de CER de cientos de puntos base, netas de costos, para un inversionista media-varianza con aversión relativa de 5.
- **Costo de la tendencia:** latigazos (*whipsaws*) en mercados laterales, meses fuera durante rebotes en V. Faber: el timing queda por debajo del índice en ~la mitad de los años.

### 5.2 Reglas diarias de corto plazo sobre índices maduros: D

Hecho estadístico real en 1897-1986 (BLL), muerto después: sin significancia fuera de muestra (STW), BETC debajo de costos (Bessembinder-Chan), no ejecutable al precio de la señal (Ready), sin persistencia (Bajgrowicz-Scaillet; Rink en 41 mercados). **Prohibidas.**

### 5.3 Tendencia multiactivo (TSMOM): B

Siglo de evidencia positiva (Hurst et al.), pero la significancia activo por activo es débil (Huang et al. 2020) y el desempeño 2024-2025 de los CTAs fue pobre. Se usa como **filtro y diversificador**, no como fuente principal de rendimiento (detalle en Cap. 06 y Cap. 12).

### 5.4 Sección cruzada técnica: B/C

- **52 semanas:** B. Domina al momentum clásico en la muestra original y no revierte. Barato de calcular y compatible con pocas operaciones al mes.
- **MAD 21/200:** B−. ~9% de alfa ponderado por valor, sobrevive costos institucionales; más fuerte del lado largo, justo el único lado que opera una cuenta sin cortos.
- **Trend factor:** C+. Cifras brutas sobre universo amplio; útil como idea (combinar horizontes), no como estrategia para 20k.
- **MA sobre deciles de volatilidad (HYZ):** C. Opera sobre portafolios con componentes ilíquidos (autocorrelación mecánica); en acciones individuales la evidencia es no concluyente [22].
- **CNN sobre imágenes:** C. Enorme en bruto y equiponderado; en valor, Sharpe 1.7 bruto con rotación semanal. Para nosotros: conocimiento, no operación.

### 5.5 Volumen: C/B−

Útil **condicionando** momentum (Lee-Swaminathan) y como señal de atención (Gervais et al.). El OBV como indicador aislado no tiene evidencia propia fuerte; solo aporta dentro del agregado de Neely et al. Rol: desempate.

### 5.6 Intradía y overnight: existe, no para nosotros

El momentum intradía es real (B en existencia), pero exige ejecución en la última media hora, costos bajísimos y apalancamiento para que valga la pena. El overnight drift ya murió. La descomposición overnight/intradía de Lou-Polk-Skouras es conocimiento estructural valioso (el momentum se paga de noche), no una regla operable manual. **Veredicto:** prohibido operar intradía en la cuenta arena.

### 5.7 Soportes, resistencias y números redondos: C+ como microestructura, D como sistema

Osler muestra poder predictivo real en FX intradía (1996-98) y el mecanismo (órdenes agrupadas en números redondos). No hay evidencia comparable, neta de costos, de sistemas S/R en acciones con horizonte de días. Uso permitido: **dónde NO poner un stop** (justo en el número redondo o el soporte obvio) y dónde esperar liquidez.

### 5.8 Patrones y narrativas: D

- **Velas:** Marshall-Young-Rose, sin valor frente a series aleatorias con bootstrap (DJIA 1992-2001). Los resultados positivos aislados en otros mercados no han replicado de forma robusta. Prohibidas.
- **Figuras chartistas (H&S, etc.):** con algoritmos objetivos hay algo de información (LMW, SWZ), pero dominada por reglas más simples (Chang-Osler) y en buena parte "momentum negativo con otro nombre" (SWZ). A ojo son infalsables. Prohibidas como señal; se permite que el sistema ya capture su contenido vía momentum y tendencia.
- **Fibonacci:** un estudio en tres mercados accionarios no encuentra diferencia estadística entre zonas Fibonacci y no Fibonacci [60]; un documento de trabajo (Shanaev-Gibson 2022) reporta alfa con los niveles ~38%, 50% y ~61% [61], sin réplica independiente y con un backtest ilustrativo con drawdown extremo. D.
- **Elliott:** no se encontró ninguna prueba rigurosa fuera de muestra; los estudios disponibles son de revistas de bajo nivel y con conteo de ondas discrecional [62]. Teoría infalsable (el conteo se ajusta ex post). D.

### 5.9 Métodos de practicante con momentum de crecimiento: componentes B, paquetes D

- **CAN SLIM / IBD:** el único estudio académico citado (Olson et al. 1998) es dentro de muestra, 1984-1992; el vehículo en vivo (FFTY) rindió 3.47% anual desde 2015, contra un S&P 500 que compuso a dos dígitos anuales en el mismo periodo (no verificado con precisión), después de un "backtest" del índice que superaba al mercado ~9% anual. Es el ejemplo canónico de backtest vs vivo.
- **Minervini / Weinstein (etapa 2, "trend template"):** no se encontró prueba académica del paquete. Sus componentes (precio sobre medias de 50/150/200 días, cercanía al máximo de 52 semanas, fuerza relativa) coinciden con señales de grado B (tendencia, 52 semanas, momentum). *Inferencia:* el sistema usa los componentes con evidencia, no el paquete ni sus reglas discrecionales de "patrones de contracción de volatilidad".
- **Day trading:** Brasil, 97% de los persistentes pierde. D definitivo.

### 5.10 Mercados emergentes y México: C y en decaimiento

México estaba entre los tres mercados donde las medias móviles sobrevivían costos en 1982-1995 (Ratner-Leal). Después: los ETFs debilitan la predictibilidad (Hsu-Hsu-Kuan) y Rink documenta caída drástica en todos los mercados, emergentes incluidos. No se encontró estudio reciente, riguroso y neto de costos sobre el S&P/BMV IPC. *Inferencia:* no asumir que la ventaja de los noventa existe hoy en el IPC; tratarla como hipótesis a validar con el protocolo de 6.3.

### 5.11 Cripto: C+

Detzel et al. 2021 [63]: razones precio/media móvil (5 a 100 días) pronostican Bitcoin dentro y fuera de muestra, con mejoras en alfa, Sharpe y drawdown; lo mismo en acciones pequeñas, jóvenes y poco cubiertas. Coherente con la teoría de aprendizaje: donde los fundamentales son difíciles de valuar, la tendencia pesa más. Relevante porque `arena_agresivo.concentracion.cripto_max` = 0.30.

### 5.12 Amplitud y sentimiento: C (moduladores)

La amplitud predice a corto plazo entre países e industrias (Zaremba et al.), con vida media corta. El sentimiento de Baker-Wurgler es un modulador de **sección cruzada** (qué tipo de acción sufre cuando la euforia se revierte), no un reloj de mercado. AAII solo aporta en extremos y no supera al pasivo en Sharpe. Rol: confirmar o dudar de un cambio de régimen, nunca disparar una operación por sí solos.

### 5.13 Tabla de magnitudes para decisiones

| Señal | Magnitud documentada | Neto de costos | Estado post-publicación | Grado |
|---|---|---|---|---|
| SMA 10 meses sobre S&P 500 | DD −50% relativo; CAGR +0.9 pp (bruto) | Sí con < 1 ida y vuelta al año (inferencia) | CAGR indistinguible sin look-ahead; drawdown robusto | B |
| 14 técnicos NRTZ (prima de mercado) | R²_OS 0.65%; CER de PC-TECH 2.49 pp bruto; individuales hasta 2.82 pp neto | Sí (50 pb) | Sobrevive en GWZ 2024 | B+ |
| 52 semanas (CS) | ~0.45-0.65% mensual | No reportado | Hay réplicas internacionales publicadas (no revisadas en detalle aquí) | B |
| MAD 21/200 (CS) | ~9% anual de alfa VW | Sí (institucional) | No se encontró réplica independiente | B− |
| Reglas diarias BLL | +12% vs −7% anual (compra vs venta) | No (BETC 0.22% desde 1975) | Muertas desde 1987 | D |
| Momentum intradía | R²_OS ~1.7-2.3% | Requiere costos institucionales y ejecución al cierre (inferencia) | Persiste en EUA; débil en APAC | C (para nosotros D) |
| Overnight drift | ~3.7% anual (1998-2020) | — | ≈0 desde 2021 | D |
| Velas japonesas | 0 frente a aleatorio | — | — | D |
| CAN SLIM / IBD 50 | +1.81% mensual IS 1984-92; FFTY 3.47% anual en vivo | En vivo, bajo el mercado | Fracaso en vivo | D |

---

## 6. Traducción operable

**Principio rector:** el análisis técnico entra al sistema en tres roles y solo en esos: (1) **filtro de régimen y riesgo** sobre índices y apalancados; (2) **inclinación de sección cruzada** para elegir entre candidatos; (3) **disciplina de ejecución** (dónde no poner stops, cuándo no operar). Nunca como fuente de alfa independiente sin pasar el protocolo 6.3.

### 6.1 Reglas de filtro de régimen

- **R1 — Filtro principal (núcleo y satélite):** exposición plena a un índice accionario solo si su precio *total return* del último día hábil del mes está por encima de su SMA de 10 meses. Evaluación **mensual**. Grado B (drawdown). Por debajo: la porción táctica pasa a CETES; el núcleo del patrimonio principal sigue su política estratégica (Cap. 02).
- **R2 — Filtro de apalancados (cuenta arena, vigente en `parametros.json`):** ETF apalancado solo si el subyacente está sobre su media de 200 días y VIX < 25; se vende al perder el filtro. Fundamento: drag L²σ²/2 (sección 2.4) + tendencia como detector de régimen (5.1). Evaluación **diaria**, porque en 3× un mes de retraso en un régimen de alta volatilidad es caro.
  - **Propuesta de ajuste (requiere backtest y aprobación antes de tocar `parametros.json`):** histéresis de ±1% alrededor de la media de 200 días (la banda de 1% es la variante de BLL y la de Siegel citada por Faber) o dos cierres consecutivos para reducir latigazos. El umbral VIX 25 es un parámetro, no un hallazgo: probar robustez en 20/25/30 y aceptar solo si el resultado no depende del valor exacto.
  - Las señales se calculan sobre el subyacente en USD (S&P 500, Nasdaq-100), no sobre el precio convertido a MXN. *Inferencia:* el tipo de cambio mete ruido que no tiene que ver con la tendencia del activo; además, el peso tiende a depreciarse en episodios de aversión al riesgo, lo que amortigua en MXN las caídas de activos en USD, así que el beneficio del filtro medido en MXN será menor que el medido en USD (detalle en Cap. 11).
- **R3 — Confirmación de régimen (moduladores C):** si R1 o R2 dan salida **y además** la amplitud es débil (menos de la mitad de los componentes sobre su media de 200 días) o el sentimiento está en euforia extrema, no se anticipa el regreso. Si hay pánico extremo en AAII (diferencial bajista ≥ 2 desviaciones estándar) con precio aún sobre la media, **no** se reduce exposición por miedo. Los moduladores nunca abren ni cierran posiciones por sí solos.
- **R4 — Cortacircuitos:** coherente con `arena_agresivo.cortacircuitos_drawdown`: a −20%, sin apalancados y solo posiciones con filtro de tendencia positivo. El filtro técnico es la **condición de reentrada** después de un cortacircuitos, nunca el motivo para saltárselo.

### 6.2 Reglas de selección (sección cruzada)

- **R5 — Ranking compuesto para candidatos del satélite:** z-score de (a) momentum 12-1 (Cap. 06), (b) precio / máximo de 52 semanas, (c) MAD 21/200. Ponderación sugerida por grado: 40/40/20. Condición de elegibilidad: precio sobre SMA 200 días. Solo largos.
- **R6 — Volumen como desempate:** entre candidatos empatados, preferir el ganador con rotación **no** extrema (Lee-Swaminathan) y evitar el perdedor de alto volumen. No es señal de entrada.
- **R7 — Cripto (tope 30% en arena):** exposición solo con precio sobre su media móvil, con un **único** parámetro elegido ex ante dentro del rango de 5 a 100 días documentado por Detzel et al. [63] (propuesta: 50 días), registrado antes de probarlo y sin optimizarlo sobre la misma muestra.

### 6.3 Protocolo de validación para cualquier regla técnica nueva

Obligatorio, en este orden, con los valores de `validacion_estrategias`:

1. **Pre-registro:** hipótesis, mecanismo (sección 2.2), parámetros y universo **antes** de ver resultados. Registrar el número total de variantes probadas (N) en `bitacora/decisiones`.
2. **Datos:** ≥ 10 años (`backtest_min_anios`), *total return*, sin sesgo de supervivencia, señal al cierre de t y ejecución en la apertura de t+1 (nunca en el mismo cierre).
3. **Costos:** comisión GBM + IVA + *spread* observado + deslizamiento; reportar el BETC por operación de un sentido. **Regla de las 3×:** BETC ≥ 3 veces el costo por lado (≥ ~0.9% con los costos actuales), o se descarta.
4. **Snooping:** Sharpe deflactado con N variantes (`herramientas/metricas.py → sharpe_deflactado`), probabilidad ≥ 0.95; PBO ≤ 0.25; para familias de reglas, White *Reality Check* o SPA.
5. **Robustez:** vecindad de parámetros (p. ej., medias de 150-250 días deben dar resultados parecidos a 200); submuestras por década; mercado alterno (si se diseñó en S&P 500, probar en IPC y en MSCI EM).
6. **Descomposición:** separar el rendimiento en exposición promedio × prima + covarianza de timing (sección 2.1). Si todo viene de "estar menos invertido", no es timing.
7. **Papel:** ≥ 3 meses y ≥ 30 operaciones (`paper_trading_min_*`); luego 25% del capital (`fraccion_capital_inicial`).
8. **Límite operativo:** máximo 8 operaciones al mes en la arena (`operaciones_max_mes`). Una regla que requiera más queda rechazada por diseño.

### 6.4 Reglas de ejecución y stops

- **R8 — Tamaño:** unidades = (capital × riesgo por operación) / (entrada − stop). Arena: 3% (`arena_agresivo.riesgo_por_operacion`); patrimonio principal: 1% (0.5% en fase de prueba).
- **R9 — Ubicación del stop:** a una distancia basada en volatilidad (p. ej., 2-3 ATR de 20 días) y **desplazado del número redondo o soporte obvio** donde se agrupan los stops (Osler 2003). Un stop exactamente en 100.00 o en el mínimo evidente está donde lo pone todo el mercado.
- **R10 — Sin intradía:** no se abren ni cierran posiciones tácticas con base en señales intradía. *Inferencia:* en ejecución manual, evitar órdenes a mercado en los primeros minutos de la sesión (spreads más amplios) y usar límites.
- **R11 — Nada de LLM-chartismo:** ninguna lectura de gráfica hecha por un modelo de lenguaje o de visión entra como señal sin pasar 6.3; su evidencia actual es de 1 a 3 puntos de exactitud direccional sobre el azar.

### 6.5 Checklist de 10 preguntas antes de usar una señal técnica

1. ¿Cuál es el mecanismo económico (2.2) y quién pierde del otro lado?
2. ¿La evidencia es fuera de muestra y posterior a su publicación?
3. ¿Neta de costos a la escala de GBM y MXN 20,000?
4. ¿Cuántas variantes se probaron? ¿DSR ≥ 0.95?
5. ¿Funciona en activos individuales o solo en portafolios con componentes ilíquidos?
6. ¿Depende de microcaps o de equiponderar?
7. ¿La ganancia es covarianza de timing o menor exposición?
8. ¿Sobrevive a mover el parámetro ±25%?
9. ¿Cuántas operaciones al mes genera? ¿Cabe en 8?
10. ¿Qué haría el sistema si la señal deja de funcionar? (criterio de muerte: 5 pérdidas seguidas = pausa, según `rachas`).

### 6.6 Lista oficial: indicadores que el sistema USA

| # | Indicador | Rol | Grado |
|---|---|---|---|
| 1 | SMA 10 meses (≈200 días) sobre índices, evaluación mensual | Filtro de régimen (R1) | B |
| 2 | Media de 200 días + VIX < 25, evaluación diaria | Filtro de apalancados (R2) | B (mecanismo) / C (umbral VIX) |
| 3 | Signo del rendimiento de 12 meses (TSMOM) | Filtro y diversificador multiactivo | B |
| 4 | Conjunto de 14 indicadores de Neely et al. (MA 1-3 vs 9-12 meses, MOM 9/12, OBV) | Pronóstico de prima de mercado (insumo para asignación y pronósticos calibrados) | B+ |
| 5 | Momentum 12-1 de sección cruzada | Ranking (R5) | B |
| 6 | Cercanía al máximo de 52 semanas | Ranking (R5) | B |
| 7 | MAD 21/200 | Ranking secundario (R5) | B− |
| 8 | Volatilidad realizada / VIX | Escalador de exposición (ver Cap. 07) | B |
| 9 | Media móvil 50 o 100 días en cripto | Filtro de la porción cripto (R7) | C+ |
| 10 | Volumen anómalo / rotación | Desempate (R6) | C |
| 11 | Amplitud (% sobre media de 200, avances-retrocesos) | Modulador de régimen (R3) | C |
| 12 | Sentimiento extremo (AAII, Baker-Wurgler, HJTZ) | Modulador contrario, solo en extremos (R3) | C |
| 13 | Ruptura de rango de 52 semanas (Donchian largo) | Confirmación de tendencia, nunca sola | C |

### 6.7 Lista oficial: indicadores PROHIBIDOS como señal de decisión

| Indicador / método | Motivo | Grado |
|---|---|---|
| Velas japonesas (patrones de 1-3 velas) | Sin valor frente a aleatorio (MYR 2006) | D |
| Ondas de Elliott | Infalsable; sin prueba rigurosa fuera de muestra | D |
| Retrocesos y extensiones de Fibonacci | Sin diferencia frente a niveles no Fibonacci; alfa aislado sin réplica | D |
| Figuras chartistas identificadas a ojo (H&S, triángulos, banderas, cuñas, tazas) | Subjetivas; con algoritmo, dominadas por reglas simples o reducibles a momentum | D |
| Cruces diarios de medias cortas (1-5 días) en índices grandes | Muertos desde 1987; BETC bajo el costo real | D |
| Osciladores de reversión como señal autónoma (RSI 14, estocástico, cruces diarios de MACD, Bollinger) | Sin evidencia robusta neta de costos y snooping en índices maduros | D |
| Day trading, scalping, momentum intradía, overnight drift | Costos, ejecución manual, 97% de perdedores; el drift ya murió | D |
| Paquetes de practicante (CAN SLIM, listas IBD, "trend template" completo con reglas discrecionales) | Sin evidencia OOS; fracaso en vivo (FFTY) | D |
| Gann, ciclos, niveles "mágicos", astrología financiera | Sin evidencia verificable | D |
| Lecturas de gráficas por LLM o modelos de visión | 49-53.5% de exactitud; sin validación en vivo | D (hasta pasar 6.3) |
| Cualquier regla con BETC < 3× el costo por lado o > 8 operaciones al mes | Incompatible con GBM y con `parametros.json` | D por construcción |

---

## 7. Trampas y errores comunes

1. **Confundir significancia nominal con real.** La mejor de 7,846 reglas siempre se ve genial (STW: p nominal 0.004 → p ajustado 0.341).
2. **Look-ahead.** Señal y rendimiento del mismo cierre. Ya invalidó resultados publicados (Zakamulin).
3. **Portafolios con precios rancios.** Timing sobre índices equiponderados, de small caps o de mercados emergentes ilíquidos "funciona" por autocorrelación mecánica (Bessembinder-Chan; HYZ en acciones individuales).
4. **Bruto vs neto.** Un Sharpe de 7.2 bruto, equiponderado y con rotación semanal no existe en una cuenta de GBM.
5. **Confundir reducción de riesgo con alfa.** La media móvil vende seguro contra colas; su "costo" son los latigazos. Evaluar con drawdown, Calmar y CAGR en MXN, no con la media.
6. **Olvidar el régimen.** La predictibilidad técnica de la prima vive en recesiones; años enteros de bajo desempeño son normales.
7. **Decaimiento post-publicación.** Overnight drift a cero; reglas de índice tras los ETFs; Rink: caída en todos los mercados. La media histórica no es la esperanza futura.
8. **Backtest del vendedor.** IBD 50: +9% anual en la reconstrucción, 3.47% anual en vivo.
9. **Optimizar el parámetro.** "La de 187 días es la mejor" = sobreajuste. Si 150-250 no dan resultados parecidos, no hay regla.
10. **Stops donde están todos.** Números redondos y mínimos obvios son imanes de liquidez (Osler 2003).
11. **Narrativa sobre la gráfica.** Elliott y Fibonacci siempre "funcionan" ex post porque el analista elige el conteo y el punto de anclaje.
12. **Tendencia + apalancamiento en mercado lateral.** Latigazos × 3 con drag de volatilidad = la peor combinación; por eso la histéresis propuesta en R2 y el tope de 8 operaciones al mes.
13. **Medir en USD y reportar en MXN.** *Inferencia:* el filtro en USD puede sacarte justo cuando el peso se deprecia y amortigua la caída; evaluar siempre en MXN.
14. **Creer que "la IA ve patrones".** Los modelos que sí extraen información de gráficas (CNN, redes neuronales) se entrenan con décadas de datos de miles de acciones y se validan fuera de muestra; un LLM mirando una imagen no es eso.

---

## 8. Examen de titulación

1. **¿Qué mostró STW 1999 que BLL 1992 no podía mostrar?** Que al ajustar por el universo de 7,846 reglas con el *Reality Check*, la mejor regla sigue siendo significativa en 1897-1986 pero no fuera de muestra (1987-1996, p = 0.341) ni en futuros del S&P 500 (p = 0.908).
2. **¿Cuál es el BETC de las reglas de BLL y por qué importa?** 0.39% por lado en toda la muestra y 0.22% desde 1975 (Bessembinder-Chan): menor que los costos reales, así que no había dinero neto.
3. **Menciona dos fuentes de predictibilidad espuria en reglas técnicas.** Trading no sincrónico (autocorrelación mecánica en índices y portafolios) y look-ahead (señal y rendimiento del mismo cierre); también el data snooping.
4. **¿Qué encontraron Neely et al. 2014 fuera de muestra y dónde se concentra?** R²_OS positivo para los 14 indicadores; PC-TECH 0.65%, PC-ALL 1.79%; concentrado en recesiones (11.24%) y negativo en expansiones (−2.80%); ganancias CER netas de costos.
5. **¿Por qué el filtro de 10 meses de Faber mejora el CAGR sin mejorar la media aritmética?** Porque reduce la volatilidad y los drawdowns (83.66% → 42.24%) y así el volatility drag; la media aritmética quedó igual (11.26% vs 11.22%) y la geométrica subió (9.32% → 10.18%), bruto.
6. **¿Por qué el filtro de tendencia es más valioso en un ETF 3× que en uno 1×?** El drag escala con L²σ²/2: con σ = 20%, ~18% anual en 3× vs ~2% en 1×; salir en regímenes de alta volatilidad evita la zona donde el drag destruye capital.
7. **¿Qué dice Rink 2023 sobre persistencia?** Con 6,406 reglas en 41 mercados, las recientemente ganadoras rinden significativamente peor que B&H fuera de muestra; la predictibilidad cae drásticamente con el tiempo y es sensible a costos moderados.
8. **¿En qué horario se gana el momentum según Lou-Polk-Skouras?** Íntegramente overnight; el resto de las estrategias estudiadas, intradía.
9. **¿Qué pasó con el overnight drift después de publicarse?** De ~3.7% anual (1998-2020) en la ventana de 2 a 3 a.m. ET a cerca de cero desde 2021, por la compresión del desequilibrio de órdenes al cierre; los ETFs creados para capturarlo cerraron en 14 meses.
10. **¿Qué evidencia hay sobre velas japonesas?** Marshall-Young-Rose 2006: en acciones del DJIA 1992-2001, sin valor frente a series aleatorias con bootstrap. Grado D, prohibidas.
11. **¿Por qué la señal de 52 semanas es preferible al momentum clásico en la muestra de George-Hwang?** En regresión conjunta rinde 0.65% mensual vs 0.38% de JT, y no revierte a largo plazo.
12. **¿Qué enseña el caso FFTY?** Que un método con backtest brillante (IBD 50 reconstruido, ~+9% anual sobre el S&P 500) puede rendir 3.47% anual en vivo: backtest ≠ vivo, y los paquetes de practicante sin validación OOS son D.
13. **¿Qué muestra Osler 2003 y cómo se usa en el sistema?** Que los stops y take-profits se agrupan en números redondos: explica rebotes en soportes y aceleraciones al romperlos. En el sistema: poner stops lejos de números redondos y mínimos obvios.
14. **Una regla da 4% anual bruto sobre B&H con 12 operaciones de un sentido al año. ¿Pasa el filtro de costos en GBM?** BETC = 4%/12 ≈ 0.33% por operación. El costo por lado es ~0.29% (0.25% + IVA) más *spread*, así que 3× exige ≥ ~0.9%: se rechaza (y neta de costos apenas empata).
15. **¿Qué conclusión sobre análisis técnico en México da la literatura?** México era uno de los tres emergentes donde las medias móviles sobrevivían costos en 1982-1995 (Ratner-Leal), pero la evidencia posterior muestra que la ventaja se debilita tras los ETFs y cae con el tiempo (Hsu-Hsu-Kuan, Rink); hoy es una hipótesis a validar, no un hecho.

---

## 9. Fuentes

1. Brock, Lakonishok, LeBaron (1992), JF 47(5): https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1992.tb04681.x
2. BLL (PDF escaneado): https://finance.martinsewell.com/stylized-facts/dependence/BrockLakonishokLeBaron1992.pdf
3. Resumen secundario de BLL con cifras de días de compra y venta (tesis, Lund University): https://lup.lub.lu.se/student-papers/record/1692405/file/1692415.pdf
4. Bessembinder, Chan (1998), Financial Management 27(2): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=107672
5. Sullivan, Timmermann, White (1999), JF 54(5): https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00163
6. Tablas de STW reproducidas (D. Donoho, Stats 207, Stanford 2020): https://cs.idc.ac.il/~kipnis/notes/STATS_207_L18.pdf
7. Ready (2002), Financial Management, "Profits from Technical Trading Rules": https://ideas.repec.org/a/fma/fmanag/ready02.html
8. Park, Irwin (2007), Journal of Economic Surveys 21(4): https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-6419.2007.00519.x
9. Ratner, Leal (1999), JBF 23: https://econpapers.repec.org/RePEc:eee:jbfina:v:23:y:1999:i:12:p:1887-1905
10. Hsu, Kuan, "Re-Examining the Profitability of Technical Analysis with White's Reality Check": https://homepage.ntu.edu.tw/~ckuan/pdf/snoop01.pdf
11. Hsu, Hsu, Kuan (2010), Journal of Empirical Finance 17(3): https://www.sciencedirect.com/science/article/abs/pii/S0927539810000022
12. Bajgrowicz, Scaillet (2012), JFE 106(3): https://www.sciencedirect.com/science/article/abs/pii/S0304405X1200116X
13. Zhu, Zhou (2009), JFE 92(3): https://www.sciencedirect.com/science/article/abs/pii/S0304405X09000361
14. Neely, Rapach, Tu, Zhou (2014), Management Science 60(7): https://pubsonline.informs.org/doi/10.1287/mnsc.2013.1838
15. Versión de trabajo con tablas (Fed de St. Louis): https://files.stlouisfed.org/files/htdocs/wp/2010/2010-008.pdf
16. Faber, "A Quantitative Approach to Tactical Asset Allocation" (actualización 2013): https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf
17. Zakamulin, "Revisiting the Profitability of Market Timing with Moving Averages": https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2743119
18. George, Hwang (2004), JF 59(5): https://www.bauer.uh.edu/tgeorge/papers/gh4-paper.pdf
19. Lee, Swaminathan (2000), JF 55(5): https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00280
20. Gervais, Kaniel, Mingelgrin (2001), JF 56(3): https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00349
21. Han, Yang, Zhou (2013), JFQA 48(5): https://www.kevinsheppard.com/files/teaching/mfe/advanced-econometrics/Han_Yang_Zhou.pdf
22. MA timing en acciones individuales vs portafolios (Reino Unido): https://www.researchgate.net/publication/327769177_Performance_of_Moving_Average_Investment_Timing_Strategy_in_UK_Stock_Market_Individual_Stocks_versus_Portfolios
23. Han, Zhou, Zhu (2016), JFE 122(2): https://www.sciencedirect.com/science/article/abs/pii/S0304405X16301271
24. Resumen con cifras del trend factor (CXO Advisory): https://www.cxoadvisory.com/technical-trading/trend-factor-and-stock-returns/
25. Avramov, Kaplanski, Subrahmanyam (2021), Review of Financial Economics 39(2): https://onlinelibrary.wiley.com/doi/abs/10.1002/rfe.1118
26. Gao, Han, Li, Zhou (2018), JFE 129(2): https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301351
27. Baltussen, Da, Lammers, Martens (2021), JFE 142: https://www3.nd.edu/~zda/intramom.pdf
28. Lou, Polk, Skouras (2019), JFE 134(1): https://personal.lse.ac.uk/polk/research/TugOfWar.pdf
29. Osler (2000), FRBNY Economic Policy Review 6(2): https://www.newyorkfed.org/medialibrary/media/research/epr/2000/eprvol6no2.pdf
30. Resumen del estudio de Osler (Fed de Nueva York): https://www.newyorkfed.org/newsevents/news/research/2000/rp000622a
31. Osler (2003), JF 58(5): https://onlinelibrary.wiley.com/doi/abs/10.1111/1540-6261.00588
32. Lo, Mamaysky, Wang (2000), JF: https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00265
33. NBER WP 7613: https://www.nber.org/papers/w7613
34. Chang, Osler (1999), Economic Journal 109: https://onlinelibrary.wiley.com/doi/abs/10.1111/1468-0297.00466
35. Savin, Weller, Zvingelis (2007), Journal of Financial Econometrics 5(2): https://academic.oup.com/jfec/article-abstract/5/2/243/785044
36. Versión de trabajo de SWZ: https://www.biz.uiowa.edu/faculty/gsavin/papers/hsrevision_paw_10%2019%2006.pdf
37. Marshall, Young, Rose (2006), JBF 30: https://ideas.repec.org/a/eee/jbfina/v30y2006i8p2303-2323.html
38. Lutey (resume Olson et al. 1998 sobre CAN SLIM): http://www.na-businesspress.com/JAF/LuteyM_LWeb14_5_.pdf
39. FFTY, métricas al 2026-09-25 (StockAnalysis): https://stockanalysis.com/etf/ffty/
40. "Has The IBD 50 ETF Rediscovered Its Magic Touch?" (2017): https://finance.yahoo.com/news/ibd-50-etf-rediscovered-magic-100214330.html
41. Chague, De-Losso, Giovannetti, "Day Trading for a Living?": https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101
42. Hurst, Ooi, Pedersen (2017), JPM: https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing
43. Huang, Li, Wang, Zhou (2020), JFE 135(3): https://ink.library.smu.edu.sg/lkcsb_research/6521/
44. Baker, Wurgler (2006), JF 61(4): https://pages.stern.nyu.edu/~jwurgler/papers/wurgler_baker_cross_section.pdf
45. Huang, Jiang, Tu, Zhou (2015), RFS 28(3): https://academic.oup.com/rfs/article-abstract/28/3/791/1576380
46. Zaremba, Szyszka, Karathanasopoulos, Mikutowski, "Herding for profits", Economic Modelling: https://www.sciencedirect.com/science/article/pii/S0264999319312982
47. Rink (2023), Financial Markets and Portfolio Management 37(4): https://www.econstor.eu/bitstream/10419/312389/1/s11408-023-00433-2.pdf
48. Goyal, Welch, Zafirov (2024), RFS 37(11): https://academic.oup.com/rfs/article/37/11/3490/7749383
49. Goyal, Welch, Zafirov, presentación "Equity Premium Prediction" (marzo 2023): https://www.ivo-welch.info/research/presentations/99-stanford-prediction.pdf
50. Jiang, Kelly, Xiu (2023), JF 78(6): https://onlinelibrary.wiley.com/doi/10.1111/jofi.13268
51. Versión de trabajo de JKX (NUS AIDF): https://www.aidf.nus.edu.sg/wp-content/uploads/2022/02/Xiu-Re-Imagining-Price-Trends.pdf
52. Murray, Xia, Xiao (2024), JFE 153, "Charting by machines": https://www.sciencedirect.com/science/article/abs/pii/S0304405X2400014X
53. Limkriangkrai, Chai, Zheng (2023), Pacific-Basin Finance Journal 80: https://researchmgt.monash.edu/ws/files/519509174/494419119_oa.pdf
54. Boyarchenko, Larsen, Whelan (2023), RFS 36(9), "The Overnight Drift": https://academic.oup.com/rfs/article-abstract/36/9/3502/7076616
55. Boyarchenko, Larsen, Whelan, "The Disappearing Overnight Drift", Liberty Street Economics (julio 2026): https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/
56. Gómez-Martínez et al. (2026), "Can AAII beat the market?", International Review of Economics & Finance: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6143986
57. Top Traders Unplugged, Trend Following Performance Report, junio 2025: https://www.toptradersunplugged.com/trend-following-performance-report-june-2025/
58. "Do VLMs Truly 'Read' Candlesticks?" (arXiv 2604.12659, 2026): https://arxiv.org/html/2604.12659v1
59. Yu, Li, You, "LiveTradeBench" (arXiv 2511.03628, 2025): https://arxiv.org/pdf/2511.03628
60. "Automatic identification and evaluation of Fibonacci retracements: Empirical evidence from three equity markets", Expert Systems with Applications (2021): https://www.sciencedirect.com/science/article/abs/pii/S0957417421012495
61. Shanaev, Gibson (2022), "Can Returns Breed Like Rabbits? Econometric Tests for Fibonacci Retracements" (resumen): https://paperswithbacktest.com/strategies/can-returns-breed-like-rabbits-econometric-tests-for-fibonacci-retracements
62. D'Angelo (2017), "The Effectiveness of the Elliott Waves Theory to Forecast Financial Markets", International Business Research 10(6): https://ideas.repec.org/a/ibn/ibrjnl/v10y2017i6p1-18.html
63. Detzel, Liu, Strauss, Zhou, Zhu (2021), Financial Management 50(1): https://onlinelibrary.wiley.com/doi/abs/10.1111/fima.12310
64. GBM, comisiones (centro de ayuda): https://gbm.com/faqs/que-comisiones-cobran-al-invertir-en-gbm/
