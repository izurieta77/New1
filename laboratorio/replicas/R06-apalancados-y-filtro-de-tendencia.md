# Réplica R06: ETFs apalancados 2x y 3x y filtro de tendencia de 200 días (Gayed y Bilello, 2016)

| Campo | Valor |
|---|---|
| ID | `R06`. El registro de variantes es `replicas/R06-variantes.csv`; el nombre largo del archivo es `R06-apalancados-y-filtro-de-tendencia` |
| Artículo o hallazgo | Gayed, Michael A. y Charlie Bilello (2016), "Leverage for the Long Run – A Systematic Approach to Managing Risk and Magnifying Returns in Stocks". Trabajo presentado al Charles H. Dow Award 2016 (CMT Association). SSRN 2741701, DOI 10.2139/ssrn.2741701. Versión consultada: PDF de la CMT Association, https://docs.cmtassociation.org/dow-award/2016-gayed-bilello.pdf, 19 páginas, sha256 `c181b05d60649ee96df7e7fab08c59f7afd3b1ee9847f3d4952edc29f0c6703e`. Texto extraído con pypdf el 2026-09-25. La página de SSRN respondió 403 y no se abrió. No es un artículo con revisión de pares: es un trabajo de premio de una asociación profesional. |
| Fecha de publicación (primera versión pública) | 2016-03-03 en SSRN, según el resultado de búsqueda de SSRN. CXO Advisory lo resume como "March 2016 paper". La muestra del artículo termina en octubre de 2015. |
| Pre-registro escrito el | 2026-09-25, terminado a las 06:13 UTC (sha256 de las secciones 1 a 9: `b12cbc772436d4c0f6b02f4f1284c636e663041d0c92080b69d8b6e2e4797699`; el script se detiene si cambia), **antes de cualquier corrida de backtest**. Antes de escribirlo solo se descargaron los datos y se revisaron rangos, versiones y huecos (lista en la sección 3). No se calculó ninguna métrica de ninguna regla ni de ninguna serie apalancada. |
| Responsable | Claude (laboratorio de réplicas, fase 0). Mandato: Eduardo Iván Izurieta Martínez |
| Estado | **Replicado con diferencias** (2026-09-25). Veredicto fuera de muestra: **"Solo protección"**. Conclusión operable: el filtro de 200 días se confirma como protección; el VIX < 25 se propone quitarlo; el tope de 50% es "sensato" para 3x del S&P, con reservas para TQQQ (sección 17) |

---

## PRE-REGISTRO (secciones 1 a 9; no se editan después de la primera corrida)

### 1. Hipótesis previa y mecanismo

**Resultado declarado en el artículo.** Lo verifiqué hoy en el PDF (texto extraído con pypdf; los números de página son los del PDF).

*Datos y convenciones del artículo* (pp. 5, 7 y 15):

- Índice: S&P 500 Total Return (Gross Dividends) de Bloomberg, cierres diarios, octubre de 1928 a octubre de 2015 (nota 9, p. 5).
- La media móvil se calcula sobre el cierre diario de la serie de **rendimiento total** (nota 15, p. 7). T-bills de la biblioteca de Kenneth French (nota 16, p. 7).
- Apalancamiento con **re-apalancamiento diario** del múltiplo (p. 5).
- Tabla 1: "We assume no cost to using leverage in this section" (nota 10, p. 5).
- Tablas 7 y 8: "a leverage fee of 1% per year, which approximates the current expense ratio for the largest leveraged ETFs" (p. 15). La nota 23 cita SSO (0.89%) y UPRO (0.95%) al 30-nov-2015.
- Costos de transacción: no incluidos ("This analysis assumes no cost to execute", p. 7; CXO: "ignores switching costs").
- Retraso de ejecución: el texto no menciona ninguno. Supongo ejecución al cierre del día de la señal.

*Regla (p. 12):* "When the S&P 500 Index is above its Moving Average, rotate into the S&P 500 and use leverage to magnify returns. When the S&P 500 Index is below its Moving Average, rotate into Treasury bills."

*Tabla 1 (p. 5), crecimiento de 1 dólar, oct-1928 a oct-2015, sin costo de apalancamiento:* S&P 500 $1,969; 1.25x $8,060; 2x $169,000; 3x $570,965. Múltiplo contra comprar y mantener: 1, 4, 86 y 290.

*Tabla 6 (p. 13), sin apalancamiento, oct-1928 a oct-2015:*

| Métrica | S&P 500 | SMA 10 d | SMA 20 d | SMA 50 d | SMA 100 d | SMA 200 d |
|---|---|---|---|---|---|---|
| Rendimiento anual | 9.1% | 11.7% | 10.4% | 10.3% | 10.8% | 10.9% |
| Volatilidad anual | 18.9% | 12.1% | 11.7% | 11.7% | 12.2% | 12.4% |
| Sharpe | 0.30 | 0.69 | 0.60 | 0.59 | 0.60 | 0.60 |
| Drawdown máximo | −86.2% | −49.5% | −46.6% | −46.6% | −46.5% | −49.5% |
| Operaciones por año | 0 | 38 | 26 | 15 | 10 | 5 |

*Tablas 7 y 8 (pp. 14-15), oct-1928 a oct-2015, comisión de apalancamiento de 1% anual:*

| Métrica | S&P 500 | 2x comprar y mantener | 3x comprar y mantener | LRS 200 d 1.25x | LRS 200 d 2x | LRS 200 d 3x |
|---|---|---|---|---|---|---|
| Rendimiento anual | 9.1% | 13.7% | 15.3% | 12.5% | 19.1% | 26.8% |
| Volatilidad anual | 18.9% | 37.8% | 56.7% | 15.5% | 24.9% | 37.3% |
| Sharpe | 0.30 | 0.27 | 0.21 | 0.53 | 0.51 | 0.47 |
| Sortino | 0.43 | 0.39 | 0.30 | 0.83 | 0.90 | 0.90 |
| Drawdown máximo | −86.2% | −98.8% | −99.9% | −59.0% | −78.7% | −92.2% |
| Operaciones por año | 0 | 0 | 0 | 5 | 5 | 5 |

(La tabla 7 también trae 1.25x comprar y mantener: 9.8%, 23.6%, 0.27, −92.4%.)

*Tabla 9 (p. 17), drawdown máximo en los cuatro peores mercados bajistas (LRS 200 d):* 1929-32: S&P −86.2%, 2x −35.3%, 3x −49.8%. 1973-74: −44.8%, −25.1%, −36.7%. 2000-02: −47.4%, −31.0%, −45.8%. 2007-09: −55.2%, −21.3%, −31.1%.

*Texto:* el LRS supera al S&P 500 en 80% de los periodos móviles de 3 años (p. 16). En la muestra hubo 14 recesiones; en recesión el S&P estuvo bajo su media de 200 días 69% del tiempo y en expansión 19% (p. 9).

**Comprobación propia de las cifras del artículo (solo con sus números, antes de correr).** Con crecimiento geométrico g ≈ μ − σ²/2 y re-apalancamiento diario, un L× financiado **sin costo** crece a g_L ≈ L·g_1 + (L − L²)·σ²/2 − comisión. Con g_1 = 9.1%, σ = 18.9% y comisión de 1%:

- 2x: 2(9.1%) − 3.57% − 1% = 13.6%. El artículo reporta 13.7%.
- 3x: 3(9.1%) − 10.72% − 1% = 15.6%. El artículo reporta 15.3%.

Si además se pagara el financiamiento de la parte prestada a la tasa de T-bills (≈ 3.4% promedio en 1928-2015, cifra que el script verifica con RF de French), las cifras serían ≈ 10.2% (2x) y ≈ 8.8% (3x). **Inferencia:** las Tablas 7 y 8 **no cobran el costo de financiamiento** (L − 1)·r_f que sí pagan los ETFs apalancados reales a través de sus swaps y futuros. Es la diferencia de método más importante frente a un ETF real, y el script la mide.

**Inconsistencia interna, anotada antes de correr.** Los Sharpe de las Tablas 6 y 7 coinciden con (CAGR − r̄_f)/vol con r̄_f ≈ 3.4%: (9.1 − 3.4)/18.9 = 0.30; (10.9 − 3.4)/12.4 = 0.60; (15.3 − 3.4)/56.7 = 0.21. Los del LRS de la Tabla 8 no: (19.1 − 3.4)/24.9 = 0.63 contra 0.51 reportado, y (26.8 − 3.4)/37.3 = 0.63 contra 0.47. No encontré en el texto la fórmula que usaron para esa tabla. Se reporta como discrepancia no explicada de la fuente.

**Hipótesis (previas a correr).**

- **H1, mecanismo del decaimiento.** Para un L× diario financiado a r_f y sin comisión, la brecha anual en logaritmos contra "L veces el índice" es ≈ −L(L−1)/2 × varianza realizada. En la regresión por año calendario de la brecha contra la varianza realizada del exceso diario, la pendiente estará dentro de ±20% de −1 (2x) y de −3 (3x), con R² ≥ 0.80. Con σ ≈ 19% anual, el decaimiento esperado en 1928-2015 es ≈ 3.6%/año en 2x y ≈ 10.7%/año en 3x.
- **H2, régimen.** La volatilidad anualizada del mercado en los días en que la señal (al cierre de *t-1*) está arriba de la media de 200 días es menor que en los días en que está abajo. Espero un cociente abajo/arriba ≥ 1.3. En consecuencia, el decaimiento por año de un 3x en días "arriba" es menor que en días "abajo".
- **H3, réplica bajo la convención del artículo** (sin financiamiento, comisión de 1% en 2x y 3x, sin costos de transacción, ejecución al cierre, oct-1928 a oct-2015). Las cifras quedan dentro de las tolerancias de la sección 2, usando el mercado CRSP de French en lugar del S&P 500 de Bloomberg.
- **H4, implementación realista dentro de muestra** (financiamiento (L−1)·RF + gasto de 0.9% anual + costos GBM por defecto, ejecución al cierre). LRS 2x y LRS 3x siguen superando a comprar y mantener 1x en CAGR y en Sharpe, pero con CAGR bastante menor que en el artículo. Espero LRS 2x entre 13% y 17% y LRS 3x entre 15% y 22%. Espero que 3x comprar y mantener realista quede **por debajo** del índice 1x (CAGR entre 4% y 10%, drawdown ≈ −99.9%).
- **H5, fuera de muestra (2015-11 a 2026-07, posterior a la muestra y a la publicación).** Expectativa firme: el filtro reduce el drawdown máximo frente a comprar y mantener del mismo apalancamiento, en 2x y en 3x. Expectativa moderada: el CAGR de LRS 3x queda por debajo del de 3x comprar y mantener, por los latigazos (2016, 2018, 2022-2023) y las recuperaciones en V (2020). Frente al índice 1x espero más CAGR; sobre el Sharpe no tengo expectativa firme.
- **H6, simulador contra ETFs reales.** El simulador (L × subyacente − (L−1)·RF − 0.9%/año) reproduce SSO, UPRO, QLD y TQQQ con correlación diaria ≥ 0.99 y diferencia de CAGR |sim − real| ≤ 1.5 pp/año en 2x y ≤ 2.5 pp/año en 3x. Espero que el simulador **sobreestime** a los ETFs reales (sim − real > 0), porque los swaps se financian arriba de la T-bill y el fondo guarda efectivo.
- **H7, retraso de ejecución.** Decidir con el cierre de *t-1* y ejecutar al cierre de *t* reduce el CAGR dentro de muestra del LRS 2x entre 1 y 4 pp. La razón esperada es la autocorrelación diaria positiva del índice antes de los años setenta (trading no sincrónico, cap. 14 §2.3).
- **H8, filtro de VIX < 25 (1990-2026).** Agregarlo a la media de 200 días reduce el tiempo invertido y el drawdown máximo. Sobre el Sharpe no tengo expectativa firme.
- **H9, límite de la cuenta arena.** Con 50% de la cuenta en un 3x filtrado (media de 200 días y VIX < 25), en temporadas de 6 meses de 1990-2026, la frecuencia de un drawdown de temporada de −20% o peor es ≤ 10%, y la de −35% o peor es ≈ 0.

**Mecanismo económico.**

1. **Matemática del re-apalancamiento diario.** Por Itô, d ln V_L − L·d ln S = −(L−1)·r·dt − L(L−1)·σ²/2·dt. El costo crece con el cuadrado de la volatilidad y es casi cuadrático en L. No hay "decaimiento con el tiempo": hay decaimiento con la **varianza**. El artículo lo dice así (p. 7).
2. **Agrupamiento de volatilidad y efecto apalancamiento.** Los días bajo la media de 200 días coinciden con volatilidad alta (recesiones, p. 9). Salir en esos regímenes evita justo la parte de la muestra donde el término L²σ²/2 es más caro. Por eso el filtro debería valer más en 3x que en 1x (cap. 14 §2.4).
3. **Tendencia o subreacción** (capítulos 06 y 14), mecanismo compartido con R01.

**Por qué no se arbitra.** El artículo propone aversión al apalancamiento, conductual e institucional: mandatos que prohíben pedir prestado y llamadas de margen (pp. 3-4). A eso sumo tres costos reales: los latigazos (el filtro queda debajo del índice en años alcistas, Tabla 4 del artículo), el riesgo de carrera y la dependencia de pocos episodios extremos (1929-32, 2008). **Hipótesis alternativa que compite:** la media de 200 días se eligió porque funcionó en esta misma historia (la Tabla 6 prueba 5 longitudes). Por eso se registran longitudes vecinas y se deflacta.

### 2. Criterio de refutación

**Métrica principal.** Sharpe del exceso sobre la T-bill (métrica `sharpe` del motor) y CAGR del LRS 2x contra comprar y mantener 1x, en `dentro_muestra` (1928-10 a 2015-10), con **implementación realista** y neto de costos GBM por defecto. Métricas secundarias: drawdown máximo, Sharpe al estilo del artículo ((CAGR − CAGR de RF)/vol), operaciones por año y tiempo invertido.

**Tolerancias para "Replicado".** Se evalúan con la **convención del artículo** (bloque C: sin financiamiento, comisión de 1% anual en 2x y 3x, 0 en 1x, sin costos de transacción, ejecución al cierre), en 1928-10-01 a 2015-10-30. Deben cumplirse todas:

| # | Criterio | Rango aceptado | Cifra del artículo |
|---|---|---|---|
| C1 | Datos: CAGR y volatilidad de comprar y mantener 1x | CAGR en 9.1% ± 1.0 pp; vol en 18.9% ± 1.5 pp | 9.1%, 18.9% |
| C2 | CAGR de LRS 200 d 2x | 19.1% ± 3.0 pp, **y** mayor que el CAGR de 1x y de 2x comprar y mantener | 19.1% |
| C3 | CAGR de LRS 200 d 3x | 26.8% ± 4.0 pp, **y** mayor que el de LRS 2x | 26.8% |
| C4 | Drawdown máximo de LRS 200 d 2x | −78.7% ± 10 pp, **y** menos profundo que el de 2x comprar y mantener | −78.7% |
| C5 | Sharpe (fórmula del artículo) de LRS 2x mayor que el de 1x comprar y mantener | mismo signo | 0.51 contra 0.30 |
| C6 | Mecanismo (H1 y H2) | pendiente de la regresión dentro de ±20% de −L(L−1)/2 y R² ≥ 0.80, en 2x y en 3x; cociente de volatilidad abajo/arriba ≥ 1.3 | no lo reporta como cifra; lo muestra en su Gráfica 1 |

**Resultado que refuta la hipótesis ("No replicado").** Basta cualquiera, en `dentro_muestra`, con implementación realista y costos por defecto (bloque A contra bloque B):

- a) CAGR de LRS 200 d 2x ≤ CAGR de comprar y mantener 1x.
- b) Sharpe de LRS 200 d 2x ≤ Sharpe de comprar y mantener 1x.

**"Replicado con diferencias".** Aplica cuando no hay refutación y falla alguno de C1 a C6. También aplica si el efecto aparece solo en algunos subperiodos. Operacionalización fijada aquí: 9 ventanas dentro de muestra (1928-10 a 1929-12, las décadas de 1930 a 1990 y 2000-01 a 2015-10). Si el CAGR neto realista de LRS 2x supera al de comprar y mantener 1x en **menos de 5 de las 9**, el efecto está "solo en algunos subperiodos".

**Interpretación sobre los datos, fijada de antemano.** Usar el mercado CRSP de French (Mkt-RF + RF) en lugar del S&P 500 Total Return de Bloomberg es una **diferencia de datos explicada**, no "requiere datos distintos". Es el mismo mercado (acciones de EUA ponderadas por capitalización), la misma frecuencia y la misma regla, y el artículo usa las T-bills de French. Si C1 falla, se reporta como diferencia de datos y se usan las diferencias contra el propio 1x para leer C2 a C5.

**Veredicto fuera de muestra (2015-11-02 a 2026-07-31), implementación realista, neto, ejecución al cierre:**

| Veredicto | Condición |
|---|---|
| "Se sostiene" | LRS 2x **y** LRS 3x tienen Sharpe ≥ el de 1x comprar y mantener **y** CAGR > el de 1x comprar y mantener |
| "Solo protección" | No se cumple lo anterior, pero el MDD de LRS L es menos profundo que el de L× comprar y mantener, en L = 2 **y** L = 3 |
| "No se sostiene" | Ninguna de las dos |

El mismo veredicto se calcula, como corroboración que **no** cambia el estado, sobre los ETFs reales en el mismo tramo: SSO y UPRO contra SPY, QLD y TQQQ contra QQQ.

**Sharpe deflactado.** `sharpe_deflactado_de_registro("R06", segmento="dentro_muestra", variante=...)` para `sma200_L2`, `sma200_L3` y la mejor variante, con N = variantes distintas con `es_prueba=1` (22: bloques A y F). Sensibilidad con N = 50, que representa la búsqueda de la literatura (longitudes de media, apalancamientos y filtros). Umbral: 0.95 (`config/parametros.json`). **Advertencia fijada de antemano:** el DSR contrasta el Sharpe del exceso sobre la T-bill contra 0, **no** contra comprar y mantener. Por eso se agrega una prueba Newey-West (10 rezagos, datos diarios, `herramientas/estadistica.py`) de la diferencia diaria de rendimientos netos en cada segmento: LRS L menos comprar y mantener L, para L = 2 y 3, y LRS 2x menos comprar y mantener 1x.

**Cómo se traduce a la conclusión operable.** Las reglas afectadas son: `perfiles_riesgo.arena_agresivo.filtro_apalancados` ("solo con el subyacente sobre su media móvil de 200 días y VIX < 25; se venden al perder el filtro"), `concentracion.etf_apalancado_max` = 0.5, los cortacircuitos de −20% (sin apalancados) y −35% (límite duro), y R2 del capítulo 14 §6.1. Esta réplica **no** modifica `config/parametros.json`: solo propone.

1. **Filtro de 200 días.**
   - **Se confirma** si el estado no es "No replicado", el veredicto fuera de muestra (simulado) es "Se sostiene" o "Solo protección", y en UPRO y TQQQ reales, fuera de muestra, el MDD de `sma200` es menos profundo que el de comprar y mantener del mismo ETF, **también con rezago de 1 día**.
   - **Se modifica** si la reducción del MDD en los ETFs reales solo aparece con ejecución al cierre y desaparece con rezago de 1 día. En ese caso se declara que la regla exige ejecutar el mismo día, con su costo.
   - **Se descarta** si el veredicto fuera de muestra es "No se sostiene", o si en UPRO y TQQQ reales el filtro no reduce el MDD con ninguna de las dos ejecuciones.
2. **VIX < 25.** Se mantiene si, en 1990-2026 y en los dos segmentos, `sma200_vix25_L3` reduce el MDD en al menos 5 pp frente a `sma200_L3` (misma ventana) sin bajar el Sharpe más de 0.05, **y** los umbrales 20 y 30 dan el mismo signo. Si no, se propone quitarlo o dejarlo como opcional: sería un parámetro sin evidencia.
3. **`etf_apalancado_max` = 0.5.** Se evalúa con temporadas de 6 meses (una por cada mes de inicio) de la cartera con 50% en 3x filtrado y el resto en efectivo:
   - **"Sensato"** si, con media de 200 días y VIX < 25 en 1990-2026 (ejecución al cierre y con rezago), la frecuencia de un drawdown de temporada de −20% o peor es ≤ 10% y la de −35% o peor es ≤ 1%, **y** con media de 200 días sola en 1928-2026 la de −35% o peor es ≤ 2%.
   - **"Demasiado alto"** si la frecuencia de −35% o peor es mayor que 2% en cualquiera de esas corridas, o la de −20% o peor es mayor que 20%.
   - En otro caso, **"aceptable con reservas"**.
   - Se reporta también la frecuencia de días con pérdida de 5% o más (el `limites_perdida.diaria` de la arena).

En cualquier caso, ninguna regla pasa a dinero sin los requisitos de la sección 1 del README del laboratorio: papel durante 3 meses y 30 operaciones.

### 3. Datos y licencia

| Serie | Fuente y archivo | Versión / huella | Frecuencia | Condiciones de uso |
|---|---|---|---|---|
| Mercado (Mkt-RF + RF) y RF, **principal** | French, `F-F_Research_Data_Factors_daily_CSV.zip`, caché de `herramientas/datos_historicos.py`; se congela en `replicas/R06-datos/` con `SHA256SUMS.txt` | CRSP 202607, sha256 `1916d331c2c51d2aee3d00215897d2b8e5995cb387f1f4569ba46bff5fb049a8`; 1926-07-01 a 2026-07-31, 26,296 días, 0 faltantes | diaria | "Copyright Eugene F. Fama and Kenneth R. French"; otras condiciones pendientes de verificar |
| SPY, QQQ (subyacentes reales, con dividendos) | Yahoo chart v8, `adjclose` | Hash de la serie en la corrida. SPY 1993-01-29 a 2026-09-24 (8,471 días); QQQ 1999-03-10 a 2026-09-24 (6,929) | diaria | Pendiente de verificar |
| SSO, UPRO, QLD, TQQQ (ETFs apalancados reales) | Yahoo chart v8, `adjclose` | SSO y QLD desde 2006-06-21 (5,097 días); UPRO desde 2009-06-25 (4,338; cierre nulo el 2026-09-22); TQQQ desde 2010-02-11 (4,180) | diaria | Pendiente de verificar |
| ^GSPC y ^NDX (índices de precio, sin dividendos) | Yahoo chart v8 | ^GSPC desde 1927-12-30; ^NDX desde 1985-10-01 (10,324 días). Ambos con cierre nulo el 2026-09-22 | diaria | Pendiente de verificar |
| VIX | FRED `VIXCLS` (cierre) | 1990-01-02 a 2026-09-22 (9,279 observaciones) | diaria | Pendiente de verificar |
| MXN por USD | FRED `DEXMXUS` | 1993-11-08 a 2026-09-18 | diaria | Pendiente de verificar |
| Tasa de Cetes (aproximación) | FRED `INTGSTMXM193N` (IMF IFS, Treasury Bill Rate de México, % anual) | 1986-10 a 2026-07 | mensual | Pendiente de verificar |

**Formato de French.** El archivo diario actual declara en su preámbulo "created by using the 202607 CRSP database" y que "The Tbill return is the simple daily rate that, over the number of trading days in the month, compounds to 1-month TBill rate", con Ibbotson hasta 202405 e ICE BofA desde 202406. El parser de `datos_historicos.py` detecta encabezado y filas numéricas sin depender de números de línea. El cambio a CRSP CIZ desde enero de 2025 afecta cómo se reinvierten los dividendos (ver R01 §3); aquí no se corre sensibilidad de vintage diario.

### 4. Universo

- **Serie larga (bloques A a F, I y J):** un solo activo de riesgo, el mercado accionario de EUA de French (CRSP: NYSE, AMEX y NASDAQ, ponderado por capitalización). **No** es el S&P 500 del artículo. No tiene sesgo de supervivencia. Los "ETFs apalancados" de 1928 a 2006 son **simulados**: no existían.
- **ETFs reales (bloque G):** SSO (2x S&P 500), UPRO (3x S&P 500), QLD (2x Nasdaq-100) y TQQQ (3x Nasdaq-100), que pide la tarea. Hay sesgo de supervivencia de producto: se eligieron ETFs que siguen vivos y son grandes (Direxion cerró 10 ETFs en abril de 2026, `arena/investigacion/02-universo-sic-bmv-agresivo.md`). SPXL, que sí está listado en la BMV, no entra; UPRO es su equivalente en ProShares.
- **Nasdaq-100 largo (bloque H):** ^NDX de precio, **sin dividendos** (subestima el rendimiento total en ≈ 0.5-1% anual; supuesto no verificado). Se incluye porque TQQQ es la base agresiva que propone el documento 02 de la arena y la caída de 2000-2002 no está en la historia de TQQQ.
- **Disponibilidad para la arena:** TQQQ y SPXL están listados y activos en el SIC; UPRO, SSO y QLD tienen poca o ninguna liquidez local, o listado no verificado (documentos 01 y 02 de la arena). La réplica mide el mecanismo; no afirma que se puedan comprar.

### 5. Fecha de disponibilidad

- **Estructura.** El activo del motor es la serie diaria del ETF (simulado o real). La señal lee el **subyacente** a través de `extras` (`sub`: nivel del índice de rendimiento total por fecha de negociación) y, cuando aplica, `vix` (cierre de VIXCLS). El motor solo entrega entradas con fecha ≤ la fecha de *t-1*. La señal es una función pura de su argumento: sin capturas de series.
- **Ejecución al cierre (convención del artículo y principal).** La decisión para el día *t* usa el cierre de *t-1* y se ejecuta a ese mismo cierre. Es optimista, porque hay que conocer el cierre para calcular la media. El VIX cierra 15 minutos después que las acciones: con ejecución al cierre, el filtro de VIX también es optimista.
- **Ejecución con rezago de 1 día (realista).** La decisión para *t* usa el subyacente y el VIX hasta *t-2*, es decir, se ejecuta al cierre del día siguiente a la señal. Es lo que puede hacer una persona en GBM que revisa la señal después del cierre.
- **Revisiones.** French revisa sus series entre versiones (R01 §3). En tiempo real se conocía el nivel del índice al cierre, así que el rezago de publicación no afecta la regla.
- **Tipo de cambio.** `DEXMXUS` entra como `fx` del motor, con el último dato ≤ la fecha y 10 días de antigüedad máxima. La señal ve rendimientos en USD.
- **Cetes.** La tasa mensual de `INTGSTMXM193N` se aplica a los días de su mismo mes. Solo es el rendimiento del efectivo, no entra en la señal. Es una aproximación declarada.

### 6. Periodo

- **Periodo del artículo:** octubre de 1928 a octubre de 2015.
- **Periodo propio total (serie larga):** del 1928-10-01 al 2026-07-31. La curva arranca al cierre del último día de septiembre de 1928; hay más de 200 días previos desde julio de 1926 para la primera media.
- **Corte:** uno, en **2015-10-31** (fin de la muestra del artículo).
  - `dentro_muestra`: 1928-10-01 a 2015-10-30 (el tramo del artículo).
  - `fuera_muestra`: 2015-11-02 a 2026-07-31, posterior a la muestra; la publicación en SSRN fue el 2016-03-03. Como sensibilidad sin registro adicional se reporta el tramo posterior a la publicación, 2016-03-04 a 2026-07-31.
  - Las primeras medias de noviembre de 2015 usan datos de antes del corte. Es legítimo y se declara.
- **Ventana VIX (bloques F y J):** del 1990-01-03 al 2026-07-31, con el mismo corte.
- **ETFs reales (bloque G):** desde el día siguiente al inicio de cada ETF hasta el 2026-07-31 (último día con RF de French), con el mismo corte. El tramo `fuera_muestra` es idéntico para los cuatro ETFs.
- **Nasdaq-100 largo (bloque H):** del 1986-08-01 al 2026-07-31, con el mismo corte.
- **MXN (bloque I):** desde el 1993-11-10 (dos días después del primer `DEXMXUS`) hasta el 2026-07-31.

### 7. Limpieza

- Mercado = Mkt-RF + RF, aditivo, como lo construye French. Con cualquier faltante (−99.99 o −999) el script se detiene; no se imputa. Se listan los huecos de más de 4 días naturales entre fechas (cierres conocidos como marzo de 1933 o septiembre de 2001) sin modificar nada.
- Yahoo: rendimiento = `adjclose_t / adjclose_{t-1} − 1`. Si hay `fechas_sin_precio` dentro de la ventana usada, el script se detiene. Se listan los rendimientos diarios con |r| > 25% en 1x y > 60% en 3x como alerta de *splits* mal ajustados, sin modificarlos. La ventana termina el 2026-07-31, así que el cierre nulo de Yahoo del 2026-09-22 queda fuera.
- Alineación: el motor usa la intersección de fechas del activo y del efectivo (RF de French). Las fechas descartadas se reportan.
- No se eliminan valores extremos: 1929-1933, 1987, 2008 y 2020 se quedan.
- El cambio de fuente de la T-bill en 202406 se declara, sin ajuste.
- Ninguna observación se elimina después de ver resultados.

### 8. Regla y variantes planeadas

**Serie del ETF apalancado simulado (por día *t*, con Δd_t = días naturales desde la fecha anterior):**

```
realista:              r_L,t = L * M_t - (L - 1) * RF_t - GA_L * Δd_t / 365.25
convencion articulo:   r_L,t = L * M_t - C_L * Δd_t / 365.25          # sin financiamiento
  M_t = Mkt-RF + RF (French) o rendimiento del subyacente (SPY, QQQ, ^NDX)
  GA_L = 0.9% anual si L >= 2, 0 si L = 1          (gasto anual del ETF, supuesto de la tarea)
  C_L  = 1% anual si L >= 2, 0 si L = 1            (comision de apalancamiento del articulo)
  sensibilidad: financiamiento a RF + 0.50% anual sobre la parte prestada
```

**Regla (media móvil de n días sobre el subyacente de rendimiento total):**

```
S_s = nivel del subyacente al cierre de s (producto acumulado de 1 + M)
al cierre de t-1-k (k = 0 ejecucion al cierre; k = 1 rezago de un dia):
    SMA_n = media(S_{t-n-k}, ..., S_{t-1-k})
    filtro = S_{t-1-k} > SMA_n                        (empate -> fuera)
    con VIX: filtro = filtro y VIX_{t-1-k} < umbral
w_t = 1 si filtro, si no 0        (1 = 100% en el ETF L x; 0 = 100% en T-bills)
costo_t = |w_t - w_pre_t| * (comision + spread) sobre el valor de la cartera (motor)
```

**Cartera de la arena (bloque J):** peso objetivo k en el 3x cuando el filtro está activo y 0 cuando no. Con el filtro activo solo se rebalancea si el peso a la deriva se sale de k ± 5 pp (`rebalanceo.banda_absoluta` = 0.05). El resto va en efectivo.

**Corridas planeadas (lista cerrada; todo lo demás es desviación).** Todas usan `id_replica="R06"`, `cortes=["2015-10-31"]`, exposición mínima 0, máxima 1 e inicial 0, y costos por defecto, salvo donde se indica otra cosa.

| Bloque | Corridas | `es_prueba` | Datos y costos |
|---|---|---|---|
| A. Principal | `sma{50,100,150,200,250}_L{1,2,3}` = 15 | **1** | French, realista, 1928-10 a 2026-07 |
| B. Referencias | `bh_L1`, `bh_L2`, `bh_L3`, `efectivo` = 4 | 0 | Igual que A |
| C. Convención del artículo | `art_bh_L{1,2,3}`, `art_sma200_L{1,2,3}`, `art_bh_L{2,3}_sin_comision` (Tabla 1), `art_sma{10,20,50,100}_L1` (Tabla 6) = 12 | 0 | Sin financiamiento, comisión de 1% en L ≥ 2, **sin** costos de transacción |
| D. Costos | `sma200_L{1,2,3}` sin costos de transacción (3); `sma200_L{1,2,3}` con spread medio (3); `sma200_L{2,3}` y `bh_L{2,3}` con financiamiento a RF + 0.50% (4); `sma200_L{2,3}` con doble pierna (0.58% + 0.10% por cambio, efectivo en un ETF de T-bills) (2) = 12 | 0 | Según el escenario |
| E. Ejecución | `sma200_L{1,2,3}` con rezago de 1 día = 3 | 0 | Realista |
| F. VIX, 1990-2026 | `sma200_vix{20,25,30}_L{2,3}` (6) y `vix25_solo_L3` (1) con `es_prueba=1`; `bh_L{1,2,3}` y `sma200_L{1,2,3}` en la misma ventana (6) con `es_prueba=0` = 13 | 7 de 13 | Realista |
| G. ETFs reales | {SSO, UPRO, QLD, TQQQ} × {`bh`, `sma200`, `sma200` con rezago} (12); {SPY, QQQ} × {`bh`, `sma200`} desde 2006-06-22 (4); simulado desde SPY o QQQ en la misma ventana de cada ETF × {`bh`, `sma200`} (8); `sma200` de UPRO con señal sobre ^GSPC de precio y de TQQQ sobre ^NDX de precio (2) = 26 | 0 | Rendimientos reales de Yahoo; efectivo RF de French; señal sobre SPY o QQQ `adjclose` |
| H. Nasdaq-100 largo | {`bh`, `sma200`} × L{1,2,3} = 6 | 0 | ^NDX de precio, realista, 1986-08 a 2026-07 |
| I. MXN | Efectivo = Cetes en MXN: `bh_L1`, `bh_L3`, `sma200_L2`, `sma200_L3` (4); efectivo = RF en USD convertido: `sma200_L3` (1) = 5 | 0 | French realista, `fx` = DEXMXUS, desde 1993-11 |
| J. Arena | 3x con peso k y bandas de ±5 pp: `arena_k{025,050,100}_sma200_vix25_L3` (1990-2026) (3); `arena_k050_sma200_vix25_L3` con rezago (1); `arena_k050_sma200_L3` (1928-2026) (1); `arena_k050_bh_L3` sin filtro (1928-2026) (1); `arena_k050_sma200_vix25` sobre UPRO real y sobre TQQQ real (señal sobre SPY o QQQ y VIX) (2) = 8 | 0 | Realista y ETFs reales |

Total planeado: 104 corridas registradas, de las cuales 22 configuraciones tienen `es_prueba=1`.

**Análisis sin registro adicional** (se calculan sobre las series de las corridas o directamente de los datos):

- Decaimiento por volatilidad (H1): brecha anual en logaritmos de 2x y 3x brutos (financiados a RF, sin gasto) contra L veces el índice, regresión contra la varianza realizada por año calendario completo (1927-2025), promedio anual por década y descomposición en días arriba y abajo de la media de 200 días.
- Régimen (H2): volatilidad anualizada y exceso medio del mercado en días con la señal arriba o abajo, dentro y fuera de muestra.
- Validación del simulador (H6): para cada ETF real, correlación diaria, error de seguimiento anualizado, diferencia media anualizada (sim − real) y diferencia de CAGR, con el subyacente real (SPY o QQQ), con el mercado de French (solo SSO y UPRO) y con ^NDX de precio (solo QLD y TQQQ). También la brecha realizada de UPRO y TQQQ contra 3 veces su subyacente.
- Tramos del artículo: Tabla 1 (crecimiento de 1 dólar), Tabla 9 (MDD en los cuatro mercados bajistas, fechas del artículo) y Tabla 10 (fecha del nuevo máximo), sobre las series del bloque C y del bloque A.
- Subperiodos por década (9 ventanas dentro de muestra más las ventanas fuera de muestra).
- Newey-West de las diferencias diarias (10 rezagos) y DSR.
- Temporadas de 6 meses para el bloque J y sus referencias (`bh_L1`, `sma200_L3` en la misma ventana): mediana, percentil 5, frecuencia de drawdown de temporada de −12%, −20%, −28% y −35% o peor, y días con pérdida de 5% o más.

**Parámetros del artículo:** media simple de 200 días sobre el S&P 500 TR, apalancamiento diario de 1.25x, 2x y 3x, efectivo en T-bills, comisión de 1% anual. 1.25x no se replica porque no existe como ETF de uso en la arena.

### 9. Costos y comparación simple

**Costos por defecto:**

- Comisión GBM de 0.29% por lado. Es un hecho: 0.25% + IVA, Guía de Servicios GBM V1025, `arena/investigacion/01-gbm-operativa-y-costos.md` §2.1.
- Spread de 0.05% por lado. Es un supuesto [I] no verificado (§3). La liquidez local de los apalancados en el SIC es baja (TQQQ ≈ 4.7 M MXN/día y desviación mediana de 0.17% contra el valor justo, documento 02 de la arena). Por eso el escenario de spread medio (0.15%) es relevante.
- El costo es |Δw| × 0.34% sobre el valor de la cartera.
- Gasto anual del ETF: 0.9% (supuesto de la tarea; SSO 0.89% y UPRO 0.95% en 2015 según el artículo). Financiamiento: (L − 1) × RF de French. Ambos van dentro de la serie simulada, no en el motor.

**No se incluye:** el spread cambiario (no publicado, §2.3), los impuestos (capa separada), la venta final, la retención de dividendos de los ETFs (tasa de 10% no modelada) y el costo de margen (no se usa margen: el apalancamiento está dentro del ETF).

**Reglas sencillas con idénticas condiciones:** comprar y mantener 1x (`bh_L1`), 100% efectivo (`efectivo`), comprar y mantener del mismo apalancamiento (`bh_L2`, `bh_L3`) y la misma media de 200 días sin apalancamiento (`sma200_L1`, la regla sencilla del mismo tipo, comparable con R01).

---

## RESULTADOS (se llenan después de correr)

### Desviaciones del pre-registro

| Fecha | Qué cambió | Por qué | ¿Invalida el tramo de prueba? |
|---|---|---|---|
| 2026-09-25, 06:13 UTC, fuera de las secciones 1 a 9 | En el encabezado, "Pre-registro escrito el" pasó de un rango estimado a la hora real de cierre (06:13 UTC) y se agregó el sha256 de las secciones 1 a 9. | Dejar la hora exacta y la huella. | No: el encabezado está fuera del bloque con hash |
| 2026-09-25, ~06:20 UTC, **antes de la primera corrida con datos reales** (06:21:56 UTC) | `arena_k050_sma200_vix25_L3\|rezago1` empieza el 1990-01-04 (`min_historia = mh_vix + 1`) en lugar del 1990-01-03. | Con rezago de 1 día, la primera decisión necesita el VIX del día anterior al primer dato de VIXCLS (1990-01-02). Lo detectó la prueba con datos sintéticos (`--prueba-sintetica`, datos aleatorios, registro en un directorio temporal). | No: cambia un día del inicio de una corrida que no es de prueba |
| 2026-09-25, 06:22 a 06:25 UTC, **después** de la corrida 1 | Se agregó a `R06.py` la función `post_hoc()`, **no pre-registrada**: (a) diagnóstico de la anualización de la volatilidad (French contra ^GSPC); (b) 4 corridas con la convención del artículo sobre ^GSPC de precio; (c) 2 corridas de la cartera de la arena con 3x del Nasdaq-100 simulado; (d) temporadas adicionales y rebalanceos por año. Se volvió a correr el script completo (corrida 2, 06:25:57 UTC). | C1 y C4 fallaron y había que saber si la causa era el índice. Además, el documento 02 de la arena propone TQQQ, y la prueba pre-registrada de la arena usa un 3x tipo S&P. También se aclara que la columna `camb/a` del motor cuenta la deriva que la banda deja pasar. | No cambia ninguna regla, variante, corte ni criterio. La corrida 2 volvió a registrar las mismas 104 corridas y agregó 6 post-hoc con `es_prueba=0`. `diff` de `R06-salida.txt` entre las corridas 1 y 2: fuera de la marca de tiempo y la sección POST-HOC nueva, todas las líneas son idénticas. Lo post-hoc **no** entra en el estado ni en los veredictos |
| 2026-09-25, 06:27 UTC | Se agregó `R06_verificacion.py`: recálculo independiente, sin el motor, de `bh_L1`, `bh_L3`, `sma200_L2` y `sma200_L3\|rezago1`. | Auditoría del motor. | No es una variante nueva ni registra nada. Diferencia máxima de CAGR y MDD contra el motor: 0.00e+00 |

### 10. Variantes probadas

- **Archivo:** `replicas/R06-variantes.csv`, con 642 filas: 214 corridas × 3 segmentos (completo, `dentro_muestra` y `fuera_muestra`).
  - Corrida 1: 104 corridas (2026-09-25T06:21:56Z).
  - Corrida 2: 110 corridas (06:25:57Z), que son las mismas 104 más 6 post-hoc con `es_prueba=0` y la nota "POST-HOC no pre-registrado".
- **Variantes con `es_prueba=1`:** 22 distintas: `sma{50,100,150,200,250}_L{1,2,3}` (15) y `1990_sma200_vix{20,25,30}_L{2,3}` más `1990_vix25_solo_L3` (7). Cada una aparece dos veces con parámetros idénticos, y el DSR la cuenta una vez.
- **Pruebas fuera del registro:** ninguna variante nueva.
  - Las dos ejecuciones de `--prueba-sintetica` usaron datos aleatorios en un directorio temporal.
  - `R06_verificacion.py` recalcula variantes ya registradas.
  - Antes de la corrida 1 solo se cargaron datos y metadatos.
  - Por eso `n_pruebas` = 22. Como sensibilidad se usa N = 50.
- **Salida de `sharpe_deflactado_de_registro`**, copiada de `R06-salida.txt`:

```
--- Sharpe deflactado (Bailey y Lopez de Prado) ---
  sma200_L2 dentro N=registradas   variante=sma200_L2                DSR=0.9925 cumple(>=0.95)=True N=22 (registradas 22) V=1.108e-04 SR=0.0366/dia (0.582 anual) SR0=0.0204/dia (0.325 anual) T=22923 asim=-0.299 curt=20.23 PSR=1.0000
  sma200_L3 dentro N=registradas   variante=sma200_L3                DSR=0.9973 cumple(>=0.95)=True N=22 (registradas 22) V=1.108e-04 SR=0.0390/dia (0.619 anual) SR0=0.0204/dia (0.325 anual) T=22923 asim=-0.297 curt=20.27 PSR=1.0000
  mejor dentro N=registradas       variante=sma150_L3                DSR=0.9985 cumple(>=0.95)=True N=22 (registradas 22) V=1.108e-04 SR=0.0401/dia (0.637 anual) SR0=0.0204/dia (0.325 anual) T=22923 asim=-0.070 curt=22.34 PSR=1.0000
  sma200_L3 dentro N=50            variante=sma200_L3                DSR=0.9879 cumple(>=0.95)=True N=50 (registradas 22) V=1.108e-04 SR=0.0390/dia (0.619 anual) SR0=0.0240/dia (0.380 anual) T=22923 asim=-0.297 curt=20.27 PSR=1.0000
  sma200_L2 dentro N=50            variante=sma200_L2                DSR=0.9715 cumple(>=0.95)=True N=50 (registradas 22) V=1.108e-04 SR=0.0366/dia (0.582 anual) SR0=0.0240/dia (0.380 anual) T=22923 asim=-0.299 curt=20.23 PSR=1.0000
  sma200_L3 fuera N=registradas    variante=sma200_L3                DSR=0.8406 cumple(>=0.95)=False N=22 (registradas 22) V=1.206e-04 SR=0.0409/dia (0.649 anual) SR0=0.0213/dia (0.339 anual) T=2701 asim=-0.930 curt=7.58 PSR=0.9814
  sma200_L2 fuera N=registradas    variante=sma200_L2                DSR=0.8100 cumple(>=0.95)=False N=22 (registradas 22) V=1.206e-04 SR=0.0385/dia (0.612 anual) SR0=0.0213/dia (0.339 anual) T=2701 asim=-0.932 curt=7.58 PSR=0.9753
  mejor fuera N=registradas        variante=sma200_L3                DSR=0.8406 cumple(>=0.95)=False N=22 (registradas 22) V=1.206e-04 SR=0.0409/dia (0.649 anual) SR0=0.0213/dia (0.339 anual) T=2701 asim=-0.930 curt=7.58 PSR=0.9814
```

**Lectura del DSR.**

- Dentro de muestra, las variantes fijadas de antemano pasan el umbral de 0.95: `sma200_L2` con 0.9925 (N = 22) y 0.9715 (N = 50); `sma200_L3` con 0.9973 y 0.9879. La mejor dentro de muestra fue `sma150_L3` (0.9985).
- Fuera de muestra **no** pasan: `sma200_L3` 0.8406 y `sma200_L2` 0.8100.
- **Advertencia pre-registrada.** El DSR contrasta el Sharpe del exceso sobre la T-bill contra 0, **no** contra comprar y mantener. Fuera de muestra, `bh_L1` tiene Sharpe 0.712, **mayor** que el de `sma200_L2` (0.612) y el de `sma200_L3` (0.649). Pasar el DSR dentro de muestra no dice que la regla le gane al índice.

### 11. Resultados

**Resumen de las hipótesis previas.**

| Hipótesis | Qué se esperaba | Qué dio el código | ¿Se cumplió? |
|---|---|---|---|
| H1, decaimiento | Pendiente en ±20% de −L(L−1)/2 y R² ≥ 0.80 | Pendiente/teórica 1.0021 (2x) y 1.0116 (3x); R² 0.9972 y 0.9935. Brecha anual dentro de muestra: 2x −3.09% (teórica −3.06%) y 3x −9.35% (teórica −9.19%) | Sí |
| H2, régimen | Cociente de volatilidad abajo/arriba ≥ 1.3 | 1.813 dentro y 2.376 fuera. Brecha de 3x por año: −5.34% arriba y −17.73% abajo (dentro) | Sí |
| H3, réplica con la convención del artículo | C1 a C6 | C2, C3, C5 y C6 se cumplen; C1 (vol) y C4 (MDD) fallan | Parcial |
| H4, realista dentro de muestra | LRS 2x entre 13% y 17%; LRS 3x entre 15% y 22%; 3x comprar y mantener debajo de 1x (4% a 10%) | LRS 2x 15.27%; LRS 3x 20.93%; 3x comprar y mantener 10.47%, **arriba** de 1x (9.31%) | Parcial: la parte de 3x comprar y mantener falló |
| H5, fuera de muestra | Menos MDD que comprar y mantener del mismo apalancamiento; CAGR de LRS 3x menor que el de 3x | MDD de 2x −37.86% contra −59.71%; de 3x −50.96% contra −77.18%. CAGR de LRS 3x 21.02% contra 28.40% | Sí |
| H6, simulador | Correlación ≥ 0.99; diferencia de CAGR ≤ 1.5 pp (2x) y ≤ 2.5 pp (3x); sim > real | Correlación de 0.99561 a 0.99895. Diferencias: SSO +0.72 pp, QLD +0.79 pp, UPRO +1.63 pp y TQQQ +1.56 pp | Sí |
| H7, rezago | LRS 2x pierde entre 1 y 4 pp dentro de muestra | −2.19 pp (15.27% a 13.08%) | Sí |
| H8, VIX < 25 | Menos tiempo invertido y menos MDD | Tiempo invertido de 74.7% a 69.6% (dentro) y de 81.3% a 76.2% (fuera). MDD +2.94 pp mejor dentro y 4.92 pp **peor** fuera | Parcial: el MDD no mejora de forma consistente |
| H9, arena | Con k = 0.5, temporadas con DD ≤ −20% en ≤ 10% y DD ≤ −35% ≈ 0 | 3.0% y 0.0% (1990-2026) | Sí |

#### 11.1 Tramo del artículo con su convención (sin financiamiento, comisión de 1%, sin costos de transacción)

```
--- Bloque C: convencion del articulo (sin financiamiento, comision 1%, sin costos de transaccion) [dentro_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
art_bh_L1                                1928-09-29 2015-10-30  22923    9.32%  17.12%   0.402   0.351  -84.07%  100.0%    0.01   0.000%
art_bh_L2                                1928-09-29 2015-10-30  22923   14.71%  34.23%   0.465   0.333  -98.32%  100.0%    0.01   0.000%
art_bh_L3                                1928-09-29 2015-10-30  22923   17.79%  51.35%   0.505   0.282  -99.88%  100.0%    0.01   0.000%
art_bh_L2_sin_comision                   1928-09-29 2015-10-30  22923   15.86%  34.23%   0.493   0.367  -98.27%  100.0%    0.01   0.000%
art_bh_L3_sin_comision                   1928-09-29 2015-10-30  22923   18.98%  51.35%   0.523   0.305  -99.87%  100.0%    0.01   0.000%
art_sma10_L1                             1928-09-29 2015-10-30  22923   14.81%  10.88%   0.984   1.058  -40.40%   59.5%   37.15   0.000%
art_sma20_L1                             1928-09-29 2015-10-30  22923   12.88%  10.64%   0.851   0.900  -45.12%   61.6%   26.08   0.000%
art_sma50_L1                             1928-09-29 2015-10-30  22923   12.08%  10.49%   0.796   0.835  -36.92%   64.3%   14.41   0.000%
art_sma100_L1                            1928-09-29 2015-10-30  22923   11.55%  10.71%   0.740   0.770  -41.00%   67.1%    9.82   0.000%
art_sma200_L1                            1928-09-29 2015-10-30  22923   11.28%  11.17%   0.693   0.714  -33.56%   70.9%    5.75   0.000%
art_sma200_L2                            1928-09-29 2015-10-30  22923   20.18%  22.34%   0.761   0.755  -59.61%   70.9%    5.75   0.000%
art_sma200_L3                            1928-09-29 2015-10-30  22923   29.00%  33.51%   0.804   0.767  -77.38%   70.9%    5.75   0.000%

Cifras del articulo (oct-1928 a oct-2015): bh_L1: CAGR 9.1% vol 18.9% Sh 0.3 MDD -86.2%; bh_L2: CAGR 13.7% vol 37.8% Sh 0.27 MDD -98.8%; bh_L3: CAGR 15.3% vol 56.7% Sh 0.21 MDD -99.9%; sma200_L1: CAGR 10.9% vol 12.4% Sh 0.6 MDD -49.5% oper/a 5; sma200_L2: CAGR 19.1% vol 24.9% Sh 0.51 MDD -78.7% oper/a 5; sma200_L3: CAGR 26.8% vol 37.3% Sh 0.47 MDD -92.2% oper/a 5; sma10_L1: CAGR 11.7% vol 12.1% Sh 0.69 MDD -49.5% oper/a 38; sma20_L1: CAGR 10.4% vol 11.7% Sh 0.6 MDD -46.6% oper/a 26; sma50_L1: CAGR 10.3% vol 11.7% Sh 0.59 MDD -46.6% oper/a 15; sma100_L1: CAGR 10.8% vol 12.2% Sh 0.6 MDD -46.5% oper/a 10
```

| Métrica | Artículo | Réplica (French CRSP) | Post-hoc: ^GSPC de precio, sin dividendos |
|---|---|---|---|
| 1x: CAGR, vol, MDD | 9.1%, 18.9%, −86.2% | 9.32%, 17.12%, −84.07% | 5.38%, 19.07%, −86.19% |
| 2x comprar y mantener: CAGR, vol, MDD | 13.7%, 37.8%, −98.8% | 14.71%, 34.23%, −98.32% | 5.98%, 38.15%, −98.86% |
| LRS 200 d 1x: CAGR, vol, MDD, operaciones por año | 10.9%, 12.4%, −49.5%, 5 | 11.28%, 11.17%, −33.56%, 5.75 | — |
| LRS 200 d 2x: CAGR, vol, MDD | 19.1%, 24.9%, −78.7% | 20.18%, 22.34%, −59.61% | 12.58%, 24.45%, −78.84% |
| LRS 200 d 3x: CAGR, vol, MDD | 26.8%, 37.3%, −92.2% | 29.00%, 33.51%, −77.38% | 16.48%, 36.68%, −93.41% |
| Sharpe de LRS 2x / 1x (fórmula del artículo) | 0.51 / 0.30 | 0.755 / 0.351 | 0.380 / 0.109 |

Las operaciones por año coinciden con el artículo en todas las longitudes: 5.75 contra 5 (200 d), 9.82 contra 10 (100 d), 14.41 contra 15 (50 d), 26.08 contra 26 (20 d) y 37.15 contra 38 (10 d).

```
--- Tabla 1 del articulo: crecimiento de 1 dolar, 1928-10-01 a 2015-10-30, sin costo de apalancamiento ---
  1x: replica $2,337 (multiplo contra 1x: 1.0) | articulo $1,969 (multiplo 1.0)
  2x: replica $370,251 (multiplo contra 1x: 158.4) | articulo $169,000 (multiplo 85.8)
  3x: replica $3,731,497 (multiplo contra 1x: 1,596.8) | articulo $570,965 (multiplo 290.0)

--- Tabla 9 del articulo: MDD dentro de cada mercado bajista (fechas del articulo) ---
  1929-09-16 a 1932-06-01: articulo S&P -86.2% 2x -35.3% 3x -49.8% | replica (conv. art.) 1x -83.9% 2x -37.8% 3x -52.6% | realista 2x -40.9% 3x -55.3% | con rezago 2x -40.0% 3x -54.2% | 3x sin filtro -99.9%
  1973-01-11 a 1974-10-03: articulo S&P -44.8% 2x -25.1% 3x -36.7% | replica (conv. art.) 1x -48.2% 2x -19.8% 3x -29.9% | realista 2x -23.4% 3x -34.0% | con rezago 2x -26.7% 3x -38.3% | 3x sin filtro -90.9%
  2000-03-24 a 2002-10-09: articulo S&P -47.4% 2x -31.0% 3x -45.8% | replica (conv. art.) 1x -49.2% 2x -50.1% 3x -67.0% | realista 2x -56.7% 3x -72.2% | con rezago 2x -51.0% 3x -66.6% | 3x sin filtro -93.3%
  2007-10-09 a 2009-03-09: articulo S&P -55.2% 2x -21.3% 3x -31.1% | replica (conv. art.) 1x -54.6% 2x -23.2% 3x -33.7% | realista 2x -26.9% 3x -37.2% | con rezago 2x -32.9% 3x -44.7% | 3x sin filtro -95.2%
```

#### 11.2 Criterios pre-registrados

La regla se aplica en el código (`R06.py`, al final de `principal`). No hay juicio manual.

```
================ CRITERIOS PRE-REGISTRADOS ================
C1 datos: CAGR 1x 9.32% (9.1% +- 1 pp) y vol 17.12% (18.9% +- 1.5 pp)? False
C2 LRS 2x CAGR 20.18% en 19.1% +- 3 pp y > 1x (9.32%) y > 2x B&H (14.71%)? True
C3 LRS 3x CAGR 29.00% en 26.8% +- 4 pp y > LRS 2x? True
C4 LRS 2x MDD -59.61% en -78.7% +- 10 pp y menos profundo que 2x B&H (-98.32%)? False
C5 Sharpe (articulo) LRS 2x 0.755 > 1x 0.351? True
C6 mecanismo: pendientes/teorica 1.002 y 1.012 (+-20%), R2 0.997 y 0.994 (>= 0.80), cociente vol abajo/arriba 1.813 (>= 1.3)? True
Refutacion a) dentro_muestra realista neto: CAGR sma200_L2 15.27% <= bh_L1 9.31%? False
Refutacion b) dentro_muestra realista neto: Sharpe sma200_L2 0.582 <= bh_L1 0.402? False
Subperiodos: CAGR sma200_L2 > bh_L1 en 8 de 9 ventanas; 'solo en algunos subperiodos' (< 5)? False
ESTADO segun reglas pre-registradas: Replicado con diferencias
Fuera de muestra (2015-11 a 2026-07, realista, neto): sma200_L2 CAGR 15.11% Sh 0.612 MDD -37.86%; sma200_L3 CAGR 21.02% Sh 0.649 MDD -50.96%; bh_L1 CAGR 14.54% Sh 0.712; bh_L2 MDD -59.71%; bh_L3 MDD -77.18% -> Solo proteccion
Corroboracion con ETFs reales fuera de muestra: SSO/UPRO contra SPY -> Solo proteccion; QLD/TQQQ contra QQQ -> Solo proteccion
Reduccion del MDD fuera de muestra en ETFs reales: {'UPRO': {'cierre': True, 'rezago1': True}, 'TQQQ': {'cierre': True, 'rezago1': True}}
Regla 1 (filtro de 200 dias para apalancados): Se confirma
  VIX dentro_muestra: MDD vix25 - MDD sma200 = +2.94 pp (>= +5), Sharpe -0.090 (>= -0.05), dif MDD con umbral 20 +0.13 pp y 30 -2.43 pp (> 0) -> False
  VIX fuera_muestra: MDD vix25 - MDD sma200 = -4.92 pp (>= +5), Sharpe -0.104 (>= -0.05), dif MDD con umbral 20 -14.75 pp y 30 -4.39 pp (> 0) -> False
Regla 2 (VIX < 25): Se propone quitarlo o dejarlo opcional
  k=0.5 SMA200+VIX25 1990-2026: DD<=-20% 3.0%, DD<=-35% 0.0%; con rezago: 3.0%, 0.0%; SMA200 sola 1928-2026: DD<=-20% 7.1%, DD<=-35% 0.8%
Regla 3 (etf_apalancado_max = 0.5): Sensato
```

- **Se reproduce:** el signo y la magnitud de los CAGR del LRS (C2 y C3), la ventaja de Sharpe (C5), el mecanismo (C6) y la frecuencia de operación.
- **No se reproduce con French:**
  - La volatilidad del índice (C1): 17.12% contra 18.9%.
  - El MDD del LRS 2x (C4): −59.61% contra −78.7%.
- **Explicación post-hoc de C1 y C4 (sección 11.9).** Con ^GSPC de precio, que antes de 1957 es el S&P 90, la volatilidad es 19.07% y los MDD del LRS son −78.84% (2x) y −93.41% (3x). Son casi los del artículo. El MDD del índice es −86.19% contra −86.2%. *Inferencia post-hoc:* la diferencia viene del índice usado (CRSP contra S&P), no de la regla.
- **Refutación:** no se cumple. Dentro de muestra, con implementación realista, LRS 2x tiene CAGR de 15.27% contra 9.31% y Sharpe de 0.582 contra 0.402.

#### 11.3 Implementación realista (financiamiento (L−1)·RF + 0.9% anual + costos GBM), mercado de French

```
--- Bloques A y B: implementacion realista (financiamiento (L-1)*RF + 0.9%/anio, costos GBM) [dentro_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
bh_L1                                    1928-09-29 2015-10-30  22923    9.31%  17.12%   0.402   0.351  -84.07%  100.0%    0.01   0.004%
bh_L2                                    1928-09-29 2015-10-30  22923   11.14%  34.24%   0.376   0.229  -98.40%  100.0%    0.01   0.004%
bh_L3                                    1928-09-29 2015-10-30  22923   10.47%  51.35%   0.385   0.139  -99.89%  100.0%    0.01   0.004%
efectivo                                 1928-09-29 2015-10-30  22923    3.31%   0.20%   0.000   0.000    0.00%    0.0%    0.00   0.000%
sma50_L1                                 1928-09-29 2015-10-30  22923    6.71%  10.53%   0.347   0.323  -47.37%   64.3%   14.41   4.900%
sma100_L1                                1928-09-29 2015-10-30  22923    7.89%  10.74%   0.440   0.426  -50.45%   67.1%    9.82   3.338%
sma150_L1                                1928-09-29 2015-10-30  22923    8.80%  10.98%   0.506   0.499  -51.65%   69.2%    7.48   2.542%
sma200_L1                                1928-09-29 2015-10-30  22923    9.12%  11.18%   0.525   0.520  -38.19%   70.9%    5.75   1.956%
sma250_L1                                1928-09-29 2015-10-30  22923    9.45%  11.35%   0.544   0.541  -53.21%   72.2%    4.54   1.542%
sma50_L2                                 1928-09-29 2015-10-30  22923   13.77%  20.99%   0.545   0.498  -68.61%   64.3%   14.41   4.900%
sma100_L2                                1928-09-29 2015-10-30  22923   14.40%  21.42%   0.563   0.518  -73.65%   67.1%    9.82   3.338%
sma150_L2                                1928-09-29 2015-10-30  22923   15.33%  21.92%   0.591   0.548  -74.95%   69.2%    7.48   2.542%
sma200_L2                                1928-09-29 2015-10-30  22923   15.27%  22.34%   0.582   0.535  -62.45%   70.9%    5.75   1.956%
sma250_L2                                1928-09-29 2015-10-30  22923   15.42%  22.67%   0.582   0.534  -78.47%   72.2%    4.54   1.542%
sma50_L3                                 1928-09-29 2015-10-30  22923   20.60%  31.47%   0.629   0.550  -82.87%   64.3%   14.41   4.900%
sma100_L3                                1928-09-29 2015-10-30  22923   20.58%  32.12%   0.622   0.538  -86.28%   67.1%    9.82   3.338%
sma150_L3                                1928-09-29 2015-10-30  22923   21.47%  32.87%   0.637   0.552  -87.30%   69.2%    7.48   2.542%
sma200_L3                                1928-09-29 2015-10-30  22923   20.93%  33.50%   0.619   0.526  -79.35%   70.9%    5.75   1.956%
sma250_L3                                1928-09-29 2015-10-30  22923   20.85%  33.99%   0.613   0.516  -90.85%   72.2%    4.54   1.542%

--- Bloques A y B: implementacion realista (financiamiento (L-1)*RF + 0.9%/anio, costos GBM) [fuera_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
bh_L1                                    2015-10-30 2026-07-31   2701   14.54%  18.37%   0.712   0.669  -34.22%  100.0%    0.00   0.000%
bh_L2                                    2015-10-30 2026-07-31   2701   22.87%  36.73%   0.687   0.561  -59.71%  100.0%    0.00   0.000%
bh_L3                                    2015-10-30 2026-07-31   2701   28.40%  55.10%   0.695   0.474  -77.18%  100.0%    0.00   0.000%
efectivo                                 2015-10-30 2026-07-31   2701    2.26%   0.13%   0.000   0.000    0.00%    0.0%    0.00   0.000%
sma50_L1                                 2015-10-30 2026-07-31   2701    3.76%  11.08%   0.188   0.136  -29.08%   72.8%   15.72   5.344%
sma100_L1                                2015-10-30 2026-07-31   2701    6.85%  11.66%   0.436   0.394  -31.19%   78.6%    9.30   3.162%
sma150_L1                                2015-10-30 2026-07-31   2701    6.78%  12.13%   0.418   0.372  -25.42%   81.0%    7.81   2.656%
sma200_L1                                2015-10-30 2026-07-31   2701    8.63%  12.16%   0.560   0.524  -22.00%   81.3%    5.77   1.961%
sma250_L1                                2015-10-30 2026-07-31   2701    8.02%  12.60%   0.500   0.457  -26.10%   82.6%    6.32   2.150%
sma50_L2                                 2015-10-30 2026-07-31   2701    9.01%  22.06%   0.402   0.306  -46.29%   72.8%   15.72   5.344%
sma100_L2                                2015-10-30 2026-07-31   2701   12.87%  23.27%   0.543   0.456  -48.55%   78.6%    9.30   3.162%
sma150_L2                                2015-10-30 2026-07-31   2701   12.01%  24.16%   0.500   0.403  -44.23%   81.0%    7.81   2.656%
sma200_L2                                2015-10-30 2026-07-31   2701   15.11%  24.27%   0.612   0.529  -37.86%   81.3%    5.77   1.961%
sma250_L2                                2015-10-30 2026-07-31   2701   13.90%  25.15%   0.557   0.463  -43.52%   82.6%    6.32   2.150%
sma50_L3                                 2015-10-30 2026-07-31   2701   13.84%  33.07%   0.493   0.350  -60.31%   72.8%   15.72   5.344%
sma100_L3                                2015-10-30 2026-07-31   2701   18.42%  34.89%   0.599   0.463  -62.15%   78.6%    9.30   3.162%
sma150_L3                                2015-10-30 2026-07-31   2701   16.60%  36.20%   0.547   0.396  -59.51%   81.0%    7.81   2.656%
sma200_L3                                2015-10-30 2026-07-31   2701   21.02%  36.38%   0.649   0.516  -50.96%   81.3%    5.77   1.961%
sma250_L3                                2015-10-30 2026-07-31   2701   19.05%  37.71%   0.596   0.445  -57.26%   82.6%    6.32   2.150%
```

Cómo leer las tablas:

- `inicio` es la fecha base de la curva (valor 1.0).
- `Sh_art` es (CAGR − CAGR de la T-bill)/vol, la fórmula que reproduce las Tablas 6 y 7 del artículo.
- `camb/a` son los cambios de exposición por año.

Cuánto le quita a la cifra del artículo la implementación realista, dentro de muestra:

- **LRS 2x:** 20.18% (convención del artículo), 17.55% (financiamiento y gasto, sin costos de transacción) y 15.27% (con costos GBM).
- **LRS 3x:** 29.00%, 23.32% y 20.93%.
- Al cobrar el financiamiento y cambiar la comisión de 1% por el gasto de 0.9%, el CAGR baja 2.63 pp en 2x y 5.68 pp en 3x. Los costos GBM restan otros 2.28 y 2.39 pp: 5.75 cambios por año × 0.34% ≈ 1.96% del valor por año.

Fechas de los drawdowns máximos:

```
--- Fechas de los drawdowns maximos (dentro y fuera de muestra) ---
  bh_L1                  dentro MDD -84.07% pico 1929-09-03 valle 1932-07-08 recuperacion 1945-02-06
  bh_L1                  fuera  MDD -34.22% pico 2020-02-19 valle 2020-03-23 recuperacion 2020-08-05
  bh_L2                  dentro MDD -98.40% pico 1929-09-03 valle 1932-07-08 recuperacion 1951-01-27
  bh_L2                  fuera  MDD -59.71% pico 2020-02-19 valle 2020-03-23 recuperacion 2020-08-28
  bh_L3                  dentro MDD -99.89% pico 1929-09-03 valle 1932-07-08 recuperacion 1954-12-29
  bh_L3                  fuera  MDD -77.18% pico 2020-02-19 valle 2020-03-23 recuperacion 2020-12-03
  sma200_L1              dentro MDD -38.19% pico 1933-07-18 valle 1935-04-11 recuperacion 1936-01-29
  sma200_L1              fuera  MDD -22.00% pico 2021-11-08 valle 2023-03-22 recuperacion 2024-03-21
  sma200_L2              dentro MDD -62.45% pico 1933-07-18 valle 1935-04-11 recuperacion 1936-02-10
  sma200_L2              fuera  MDD -37.86% pico 2021-11-08 valle 2023-03-22 recuperacion 2024-06-12
  sma200_L3              dentro MDD -79.35% pico 1933-07-18 valle 1935-04-11 recuperacion 1936-04-06
  sma200_L3              fuera  MDD -50.96% pico 2021-11-08 valle 2023-03-22 recuperacion 2024-06-17
  art_sma200_L2          dentro MDD -59.61% pico 1932-09-07 valle 1933-03-17 recuperacion 1933-07-01
  art_sma200_L2          fuera  MDD -34.37% pico 2020-02-19 valle 2020-05-21 recuperacion 2020-11-16
  art_sma200_L3          dentro MDD -77.38% pico 1932-09-07 valle 1933-03-17 recuperacion 1933-07-06
  art_sma200_L3          fuera  MDD -47.43% pico 2020-02-19 valle 2020-05-21 recuperacion 2020-11-24
  real_UPRO_bh           dentro MDD -51.73% pico 2011-04-29 valle 2011-10-03 recuperacion 2012-04-02
  real_UPRO_bh           fuera  MDD -76.82% pico 2020-02-19 valle 2020-03-23 recuperacion 2021-01-08
  real_UPRO_sma200       dentro MDD -54.11% pico 2010-04-23 valle 2011-12-28 recuperacion 2013-05-17
  real_UPRO_sma200       fuera  MDD -53.72% pico 2022-01-03 valle 2023-03-17 recuperacion 2024-06-12
  real_TQQQ_bh           dentro MDD -43.91% pico 2011-07-22 valle 2011-08-19 recuperacion 2012-02-08
  real_TQQQ_bh           fuera  MDD -81.66% pico 2021-11-19 valle 2022-12-28 recuperacion 2024-12-04
  real_TQQQ_sma200       dentro MDD -57.41% pico 2010-04-23 valle 2010-09-07 recuperacion 2013-10-16
  real_TQQQ_sma200       fuera  MDD -57.79% pico 2018-08-29 valle 2019-06-04 recuperacion 2020-08-04
  ndx_bh_L3              dentro MDD -99.98% pico 2000-03-27 valle 2009-03-09 recuperacion None
  ndx_bh_L3              fuera  MDD -81.55% pico 2021-11-19 valle 2022-12-28 recuperacion 2024-12-04
  ndx_sma200_L3          dentro MDD -96.14% pico 2000-03-27 valle 2009-05-22 recuperacion None
  ndx_sma200_L3          fuera  MDD -56.60% pico 2021-11-19 valle 2023-03-13 recuperacion 2023-12-15
```

#### 11.4 Mecanismo: decaimiento por volatilidad y régimen

```
--- H1: decaimiento por volatilidad (L x financiado a RF, sin gasto, contra L veces el indice) ---
años calendario usados: (1927, 2025, 99)
  L=2: brecha_log_anual = -0.00023 + (-1.0021) x varianza_realizada_anual; R2=0.9972; pendiente teorica -1.0; pendiente/teorica = 1.0021
  L=3: brecha_log_anual = -0.00059 + (-3.0347) x varianza_realizada_anual; R2=0.9935; pendiente teorica -3.0; pendiente/teorica = 1.0116
  dentro_muestra (87.08 años): brecha anual 2x -3.09% (teorica -3.06%); 3x -9.35% (teorica -9.19%)
  fuera_muestra (10.74 años): brecha anual 2x -3.42% (teorica -3.37%); 3x -10.36% (teorica -10.11%)
  completo (97.83 años): brecha anual 2x -3.13% (teorica -3.10%); 3x -9.46% (teorica -9.29%)
  por decada (vol anual del mercado, brecha anual 2x y 3x en logaritmos):
    1920s: vol 21.9%  2x -5.08%  3x -15.68%  (3 años)
    1930s: vol 30.2%  2x -9.01%  3x -27.06%  (10 años)
    1940s: vol 13.6%  2x -1.89%  3x -5.73%  (10 años)
    1950s: vol 10.2%  2x -1.06%  3x -3.19%  (10 años)
    1960s: vol 9.9%  2x -0.98%  3x -2.95%  (10 años)
    1970s: vol 13.3%  2x -1.76%  3x -5.29%  (10 años)
    1980s: vol 15.4%  2x -2.52%  3x -7.87%  (10 años)
    1990s: vol 13.4%  2x -1.80%  3x -5.41%  (10 años)
    2000s: vol 22.3%  2x -4.99%  3x -15.05%  (10 años)
    2010s: vol 15.2%  2x -2.33%  3x -7.03%  (10 años)
    2020s: vol 21.4%  2x -4.68%  3x -14.20%  (6 años)

--- H2: regimen segun la senal de 200 dias al cierre de t-1 (1 = arriba, 0 = abajo) ---
  dentro_muestra: arriba 70.9% de los dias, vol 13.26%, exceso medio 10.92%/año, brecha 3x -5.34%/año | abajo vol 24.04%, exceso -2.97%/año, brecha 3x -17.73%/año | cociente vol abajo/arriba 1.813
  fuera_muestra: arriba 81.3% de los dias, vol 13.44%, exceso medio 10.79%/año, brecha 3x -5.53%/año | abajo vol 31.93%, exceso 22.98%/año, brecha 3x -31.47%/año | cociente vol abajo/arriba 2.376
  completo: arriba 72.0% de los dias, vol 13.28%, exceso medio 10.91%/año, brecha 3x -5.36%/año | abajo vol 24.68%, exceso -1.14%/año, brecha 3x -18.70%/año | cociente vol abajo/arriba 1.858
```

- **H1.** La brecha anual de un L× diario contra "L veces el índice" es −L(L−1)/2 × varianza realizada, año por año, durante 99 años. No hay "decaimiento con el tiempo": en los años cincuenta y sesenta la brecha de un 3x fue ≈ −3% anual, y en los treinta, −27% anual.
- **H2.** Dentro de muestra, cuando la señal está abajo, el mercado tuvo 1.8 veces la volatilidad y un exceso medio negativo (−2.97% anual). Ahí la brecha de un 3x fue −17.73% por año, contra −5.34% arriba.
- **Fuera de muestra el signo del exceso cambia:** con la señal abajo, el exceso medio fue de **+22.98% anual**. Son los rebotes en V de 2020 y 2025, que el filtro se perdió. Esto explica por qué fuera de muestra el filtro protege pero cuesta rendimiento.

#### 11.5 ETFs reales y validación del simulador

```
--- H6: validacion del simulador (sim = L x subyacente - (L-1) RF - 0.9%/año) contra el ETF real ---
  SSO con_subyacente_real  2006-06-22 a 2026-07-31 n=5058: corr=0.99561 TE=3.66% dif media sim-real=0.85%/año CAGR real 15.58% sim 16.30% (dif +0.72 pp) MDD real -84.67% sim -84.30%
  SSO con_mercado_french   2006-06-22 a 2026-07-31 n=5058: corr=0.99317 TE=4.73% dif media sim-real=1.33%/año CAGR real 15.58% sim 16.51% (dif +0.93 pp) MDD real -84.67% sim -83.74%
  SSO brecha realizada contra 2 x subyacente - (2-1) RF: -5.31%/año; teorica por varianza (sin gasto) -3.76%/año; vol del subyacente 19.39%
  UPRO con_subyacente_real  2009-06-26 a 2026-07-31 n=4300: corr=0.99828 TE=3.01% dif media sim-real=1.25%/año CAGR real 32.58% sim 34.21% (dif +1.63 pp) MDD real -76.82% sim -76.27%
  UPRO con_mercado_french   2009-06-26 a 2026-07-31 n=4300: corr=0.99437 TE=5.83% dif media sim-real=1.81%/año CAGR real 32.58% sim 33.68% (dif +1.09 pp) MDD real -76.82% sim -77.18%
  UPRO brecha realizada contra 3 x subyacente - (3-1) RF: -11.03%/año; teorica por varianza (sin gasto) -8.77%/año; vol del subyacente 17.09%
  QLD con_subyacente_real  2006-06-22 a 2026-07-31 n=5058: corr=0.99597 TE=3.96% dif media sim-real=0.71%/año CAGR real 24.74% sim 25.53% (dif +0.79 pp) MDD real -83.13% sim -82.50%
  QLD con_ndx_precio       2006-06-22 a 2026-07-31 n=5058: corr=0.99579 TE=4.22% dif media sim-real=-0.55%/año CAGR real 24.74% sim 23.47% (dif -1.27 pp) MDD real -83.13% sim -83.18%
  QLD brecha realizada contra 2 x subyacente - (2-1) RF: -6.44%/año; teorica por varianza (sin gasto) -4.88%/año; vol del subyacente 22.09%
  TQQQ con_subyacente_real  2010-02-12 a 2026-07-31 n=4141: corr=0.99895 TE=2.95% dif media sim-real=1.61%/año CAGR real 41.81% sim 43.36% (dif +1.56 pp) MDD real -81.66% sim -80.97%
  TQQQ con_ndx_precio       2010-02-12 a 2026-07-31 n=4141: corr=0.99860 TE=3.55% dif media sim-real=-0.69%/año CAGR real 41.81% sim 39.64% (dif -2.17 pp) MDD real -81.66% sim -81.55%
  TQQQ brecha realizada contra 3 x subyacente - (3-1) RF: -14.99%/año; teorica por varianza (sin gasto) -12.84%/año; vol del subyacente 20.69%

--- Bloque G: ETFs reales, sus subyacentes y el simulador en la misma ventana [fuera_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
real_SPY_bh                              2015-10-30 2026-07-31   2701   14.50%  17.77%   0.727   0.689  -33.72%  100.0%    0.00   0.000%
real_SPY_sma200                          2015-10-30 2026-07-31   2701    9.05%  11.90%   0.602   0.571  -24.52%   83.0%    5.58   1.897%
real_QQQ_bh                              2015-10-30 2026-07-31   2701   19.12%  22.24%   0.800   0.758  -35.12%  100.0%    0.00   0.000%
real_QQQ_sma200                          2015-10-30 2026-07-31   2701   13.67%  16.50%   0.726   0.691  -25.61%   82.4%    4.84   1.644%
real_SSO_bh                              2015-10-30 2026-07-31   2701   22.27%  35.55%   0.684   0.563  -59.34%  100.0%    0.00   0.000%
sim_SSO_bh                               2015-10-30 2026-07-31   2701   23.06%  35.54%   0.702   0.585  -58.90%  100.0%    0.00   0.000%
real_SSO_sma200                          2015-10-30 2026-07-31   2701   15.58%  23.63%   0.639   0.564  -40.63%   83.0%    5.58   1.897%
sim_SSO_sma200                           2015-10-30 2026-07-31   2701   15.98%  23.75%   0.652   0.578  -40.82%   83.0%    5.58   1.897%
real_SSO_sma200|rezago1                  2015-10-30 2026-07-31   2701   13.74%  23.72%   0.570   0.484  -45.67%   83.0%    5.58   1.897%
real_UPRO_bh                             2015-10-30 2026-07-31   2701   27.33%  53.25%   0.684   0.471  -76.82%  100.0%    0.00   0.000%
sim_UPRO_bh                              2015-10-30 2026-07-31   2701   29.17%  53.31%   0.710   0.505  -76.27%  100.0%    0.00   0.000%
real_UPRO_sma200                         2015-10-30 2026-07-31   2701   21.52%  35.42%   0.669   0.544  -53.72%   83.0%    5.58   1.897%
sim_UPRO_sma200                          2015-10-30 2026-07-31   2701   22.49%  35.62%   0.689   0.568  -53.96%   83.0%    5.58   1.897%
real_UPRO_sma200|rezago1                 2015-10-30 2026-07-31   2701   18.65%  35.56%   0.600   0.461  -59.69%   83.0%    5.58   1.897%
real_QLD_bh                              2015-10-30 2026-07-31   2701   30.08%  44.43%   0.767   0.626  -63.68%  100.0%    0.00   0.000%
sim_QLD_bh                               2015-10-30 2026-07-31   2701   30.84%  44.47%   0.780   0.643  -63.03%  100.0%    0.00   0.000%
real_QLD_sma200                          2015-10-30 2026-07-31   2701   23.78%  32.87%   0.749   0.655  -43.83%   82.4%    4.84   1.644%
sim_QLD_sma200                           2015-10-30 2026-07-31   2701   24.06%  32.96%   0.755   0.661  -44.00%   82.4%    4.84   1.644%
real_QLD_sma200|rezago1                  2015-10-30 2026-07-31   2701   23.44%  33.61%   0.732   0.630  -46.33%   82.4%    4.84   1.644%
real_TQQQ_bh                             2015-10-30 2026-07-31   2701   35.99%  65.81%   0.768   0.513  -81.66%  100.0%    0.00   0.000%
sim_TQQQ_bh                              2015-10-30 2026-07-31   2701   37.82%  66.71%   0.787   0.533  -80.97%  100.0%    0.00   0.000%
real_TQQQ_sma200                         2015-10-30 2026-07-31   2701   32.13%  48.88%   0.774   0.611  -57.79%   82.4%    4.84   1.644%
sim_TQQQ_sma200                          2015-10-30 2026-07-31   2701   32.65%  49.42%   0.779   0.615  -58.38%   82.4%    4.84   1.644%
real_TQQQ_sma200|rezago1                 2015-10-30 2026-07-31   2701   31.17%  49.99%   0.754   0.578  -61.24%   82.4%    4.84   1.644%
real_UPRO_sma200|senal_GSPC_precio       2015-10-30 2026-07-31   2701   16.82%  34.77%   0.561   0.419  -53.06%   81.5%    6.70   2.277%
real_TQQQ_sma200|senal_NDX_precio        2015-10-30 2026-07-31   2701   34.15%  48.64%   0.807   0.656  -55.44%   81.7%    4.84   1.644%
```

- **Simulador contra ETF real.** El simulador desde SPY o QQQ sobreestima el CAGR real entre 0.72 y 1.63 pp por año. La diferencia media anual va de +0.71% a +1.61%. *Inferencia:* los swaps y futuros cuestan más que la T-bill, y la sobreestimación crece con L. La sensibilidad de financiamiento a RF + 0.50% (bloque D) se parece a esa diferencia.
- **Estrategia simulada contra estrategia real, misma ventana y misma señal.** Fuera de muestra: UPRO 22.49% contra 21.52%; TQQQ 32.65% contra 32.13%. Los MDD difieren en 0.2 a 0.6 pp.
- **Filtro sobre ETFs reales, fuera de muestra:**
  - Reduce el MDD: UPRO de −76.82% a −53.72%, o −59.69% con rezago; TQQQ de −81.66% a −57.79%, o −61.24% con rezago.
  - Baja el CAGR: UPRO de 27.33% a 21.52% (18.65% con rezago); TQQQ de 35.99% a 32.13% (31.17% con rezago).
  - Sharpe: UPRO 0.669 contra 0.684 del ETF comprado y mantenido; TQQQ 0.774 contra 0.768.
  - El veredicto de corroboración es "Solo protección" para SSO/UPRO contra SPY y para QLD/TQQQ contra QQQ.

#### 11.6 Subperiodos (realista, neto)

```
--- Subperiodos: realista, neto (CAGR y MDD) ---
ventana                      bh_L1  sma200_L1    bh_L2  sma200_L2    bh_L3  sma200_L3  MDD bh_L1  MDD s200L2  MDD s200L3  MDD bh_L3
1928-10-01 a 1929-12-31     -2.42%     12.95%  -18.31%     19.73%  -38.53%     23.99%    -43.70%     -33.73%     -46.96%    -86.69%
1930-01-01 a 1939-12-31     -0.45%      5.98%  -10.60%      9.96%  -25.97%     10.52%    -80.24%     -62.45%     -79.35%    -99.69%
1940-01-01 a 1949-12-31      9.08%      7.95%   15.71%     17.16%   21.46%     26.83%    -31.26%     -34.44%     -45.39%    -73.53%
1950-01-01 a 1959-12-31     18.18%     14.39%   34.64%     29.14%   53.13%     45.71%    -20.65%     -27.53%     -36.84%    -51.83%
1960-01-01 a 1969-12-31      8.28%      8.59%   10.79%     14.10%   13.25%     20.20%    -27.70%     -24.66%     -35.25%    -65.44%
1970-01-01 a 1979-12-31      6.07%      8.32%    3.06%     11.32%   -0.72%     14.22%    -48.16%     -35.87%     -48.60%    -90.93%
1980-01-01 a 1989-12-31     16.80%     17.47%   21.16%     25.79%   23.29%     33.92%    -33.11%     -30.25%     -43.92%    -77.90%
1990-01-01 a 1999-12-31     17.89%     14.14%   29.05%     23.45%   39.97%     32.76%    -21.92%     -26.66%     -37.85%    -56.63%
2000-01-01 a 2015-10-31      4.56%      1.29%    2.18%      1.69%   -3.40%      1.35%    -54.57%     -61.79%     -76.92%    -97.83%
2015-11-01 a 2019-12-31     13.52%      6.84%   23.92%     12.96%   34.03%     18.93%    -20.45%     -30.13%     -41.48%    -52.30%
2020-01-01 a 2026-07-31     15.19%      9.79%   22.21%     16.49%   24.96%     22.37%    -34.22%     -37.86%     -50.96%    -77.18%
Ventanas dentro de muestra con CAGR sma200_L2 > bh_L1: 8 de 9
```

- **Dentro de muestra:** LRS 2x supera en CAGR al índice 1x en 8 de 9 ventanas; la excepción es 2000-2015 (1.69% contra 4.56%).
- **Tramo 2000-01 a 2015-10:** el MDD de LRS 3x fue −76.92%.
- **Fuera de muestra:** en 2015-11 a 2019-12, LRS 2x tuvo menos CAGR que 1x (12.96% contra 13.52%) y más MDD (−30.13% contra −20.45%).

#### 11.7 Diferencias diarias con Newey-West (pre-registrado)

```
--- Diferencia diaria de rendimientos netos, media y error estandar Newey-West (10 rezagos) ---
  sma200_L2 - bh_L2                    dentro_muestra  n=22923  media=+0.0004%/dia (x252 +0.10%) t_NW=+0.04 IC95=[-0.0208, +0.0217]%/dia
  sma200_L2 - bh_L2                    fuera_muestra   n=2701   media=-0.0412%/dia (x252 -10.39%) t_NW=-1.47 IC95=[-0.0963, +0.0138]%/dia
  sma200_L2 - bh_L2                    completo        n=25624  media=-0.0040%/dia (x252 -1.00%) t_NW=-0.39 IC95=[-0.0239, +0.0159]%/dia
  sma200_L3 - bh_L3                    dentro_muestra  n=22923  media=+0.0038%/dia (x252 +0.97%) t_NW=+0.24 IC95=[-0.0280, +0.0356]%/dia
  sma200_L3 - bh_L3                    fuera_muestra   n=2701   media=-0.0583%/dia (x252 -14.68%) t_NW=-1.39 IC95=[-0.1406, +0.0241]%/dia
  sma200_L3 - bh_L3                    completo        n=25624  media=-0.0027%/dia (x252 -0.68%) t_NW=-0.18 IC95=[-0.0325, +0.0270]%/dia
  sma200_L2 - bh_L1                    dentro_muestra  n=22923  media=+0.0243%/dia (x252 +6.12%) t_NW=+3.33 IC95=[+0.0100, +0.0386]%/dia
  sma200_L2 - bh_L1                    fuera_muestra   n=2701   media=+0.0071%/dia (x252 +1.78%) t_NW=+0.34 IC95=[-0.0339, +0.0480]%/dia
  sma200_L2 - bh_L1                    completo        n=25624  media=+0.0225%/dia (x252 +5.66%) t_NW=+3.26 IC95=[+0.0090, +0.0360]%/dia
  sma200_L3 - bh_L1                    dentro_muestra  n=22923  media=+0.0550%/dia (x252 +13.86%) t_NW=+4.92 IC95=[+0.0331, +0.0769]%/dia
  sma200_L3 - bh_L1                    fuera_muestra   n=2701   media=+0.0419%/dia (x252 +10.55%) t_NW=+1.27 IC95=[-0.0230, +0.1068]%/dia
  sma200_L3 - bh_L1                    completo        n=25624  media=+0.0536%/dia (x252 +13.51%) t_NW=+5.06 IC95=[+0.0329, +0.0744]%/dia
  sma200_L1 - bh_L1                    dentro_muestra  n=22923  media=-0.0040%/dia (x252 -1.01%) t_NW=-0.73 IC95=[-0.0147, +0.0067]%/dia
  sma200_L1 - bh_L1                    fuera_muestra   n=2701   media=-0.0248%/dia (x252 -6.26%) t_NW=-1.75 IC95=[-0.0527, +0.0030]%/dia
  sma200_L1 - bh_L1                    completo        n=25624  media=-0.0062%/dia (x252 -1.56%) t_NW=-1.21 IC95=[-0.0162, +0.0038]%/dia
  sma200_L3|rezago1 - bh_L3            dentro_muestra  n=22923  media=-0.0066%/dia (x252 -1.66%) t_NW=-0.40 IC95=[-0.0386, +0.0255]%/dia
  sma200_L3|rezago1 - bh_L3            fuera_muestra   n=2701   media=-0.0555%/dia (x252 -14.00%) t_NW=-1.27 IC95=[-0.1415, +0.0304]%/dia
  sma200_L3|rezago1 - bh_L3            completo        n=25624  media=-0.0117%/dia (x252 -2.96%) t_NW=-0.76 IC95=[-0.0418, +0.0184]%/dia
  real_UPRO_sma200 - real_UPRO_bh      dentro_muestra  n=1598   media=-0.0688%/dia (x252 -17.33%) t_NW=-1.81 IC95=[-0.1431, +0.0056]%/dia
  real_UPRO_sma200 - real_UPRO_bh      fuera_muestra   n=2701   media=-0.0506%/dia (x252 -12.74%) t_NW=-1.30 IC95=[-0.1271, +0.0260]%/dia
  real_UPRO_sma200 - real_UPRO_bh      completo        n=4299   media=-0.0573%/dia (x252 -14.45%) t_NW=-2.03 IC95=[-0.1128, -0.0019]%/dia
  real_TQQQ_sma200 - real_TQQQ_bh      dentro_muestra  n=1439   media=-0.1032%/dia (x252 -26.02%) t_NW=-2.75 IC95=[-0.1767, -0.0298]%/dia
  real_TQQQ_sma200 - real_TQQQ_bh      fuera_muestra   n=2701   media=-0.0503%/dia (x252 -12.69%) t_NW=-1.19 IC95=[-0.1331, +0.0324]%/dia
  real_TQQQ_sma200 - real_TQQQ_bh      completo        n=4140   media=-0.0687%/dia (x252 -17.32%) t_NW=-2.25 IC95=[-0.1285, -0.0090]%/dia
```

- **Contra comprar y mantener del mismo apalancamiento:**
  - Dentro de muestra, la media diaria de la diferencia es ≈ 0: +0.10% anual en 2x (t = 0.04) y +0.97% anual en 3x (t = 0.24). La ventaja de CAGR del filtro (15.27% contra 11.14% en 2x) viene de **menos varianza y menos decaimiento**, no de más rendimiento medio.
  - Fuera de muestra es negativa: −10.39% anual en 2x (t = −1.47) y −14.68% en 3x (t = −1.39).
  - En UPRO y TQQQ reales, en toda su historia, es negativa y significativa: t = −2.03 y −2.25.
- **LRS 2x contra 1x:** +6.12% anual con t = 3.33 dentro de muestra, y +1.78% anual con t = 0.34 fuera.

#### 11.8 Filtro de VIX y cartera de la arena

```
--- Bloque F: VIX (1990-01-03 a 2026-07-31) [dentro_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
1990_bh_L1                               1990-01-02 2015-10-30   6510    9.46%  17.94%   0.433   0.365  -54.57%  100.0%    0.04   0.013%
1990_bh_L2                               1990-01-02 2015-10-30   6510   11.72%  35.88%   0.409   0.245  -87.12%  100.0%    0.04   0.013%
1990_bh_L3                               1990-01-02 2015-10-30   6510   11.33%  53.82%   0.417   0.156  -97.83%  100.0%    0.04   0.013%
1990_sma200_L1                           1990-01-02 2015-10-30   6510    6.01%  11.49%   0.315   0.269  -38.10%   74.7%    6.62   2.251%
1990_sma200_L2                           1990-01-02 2015-10-30   6510    9.49%  22.93%   0.385   0.286  -61.79%   74.7%    6.62   2.251%
1990_sma200_L3                           1990-01-02 2015-10-30   6510   12.32%  34.38%   0.428   0.273  -76.92%   74.7%    6.62   2.251%
1990_sma200_vix20_L2                     1990-01-02 2015-10-30   6510    2.46%  16.45%   0.056  -0.028  -63.79%   55.8%   13.05   4.437%
1990_sma200_vix25_L2                     1990-01-02 2015-10-30   6510    6.61%  20.61%   0.274   0.179  -58.15%   69.6%    9.64   3.278%
1990_sma200_vix30_L2                     1990-01-02 2015-10-30   6510    8.20%  22.45%   0.336   0.235  -63.55%   73.7%    8.02   2.725%
1990_sma200_vix20_L3                     1990-01-02 2015-10-30   6510    3.73%  24.64%   0.156   0.033  -76.79%   55.8%   13.05   4.437%
1990_sma200_vix25_L3                     1990-01-02 2015-10-30   6510    8.87%  30.91%   0.338   0.193  -73.98%   69.6%    9.64   3.278%
1990_sma200_vix30_L3                     1990-01-02 2015-10-30   6510   10.69%  33.65%   0.386   0.231  -79.35%   73.7%    8.02   2.725%
1990_vix25_solo_L3                       1990-01-02 2015-10-30   6510    6.52%  35.38%   0.275   0.102  -93.21%   81.2%    8.95   3.041%

--- Bloque F: VIX (1990-01-03 a 2026-07-31) [fuera_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
1990_bh_L1                               2015-10-30 2026-07-31   2701   14.54%  18.37%   0.712   0.669  -34.22%  100.0%    0.00   0.000%
1990_bh_L2                               2015-10-30 2026-07-31   2701   22.87%  36.73%   0.687   0.561  -59.71%  100.0%    0.00   0.000%
1990_bh_L3                               2015-10-30 2026-07-31   2701   28.40%  55.10%   0.695   0.474  -77.18%  100.0%    0.00   0.000%
1990_sma200_L1                           2015-10-30 2026-07-31   2701    8.63%  12.16%   0.560   0.524  -22.00%   81.3%    5.77   1.961%
1990_sma200_L2                           2015-10-30 2026-07-31   2701   15.11%  24.27%   0.612   0.529  -37.86%   81.3%    5.77   1.961%
1990_sma200_L3                           2015-10-30 2026-07-31   2701   21.02%  36.38%   0.649   0.516  -50.96%   81.3%    5.77   1.961%
1990_sma200_vix20_L2                     2015-10-30 2026-07-31   2701   -0.19%  19.08%  -0.031  -0.129  -53.24%   66.5%   16.74   5.692%
1990_sma200_vix25_L2                     2015-10-30 2026-07-31   2701   10.86%  21.60%   0.484   0.398  -42.42%   76.2%    9.67   3.289%
1990_sma200_vix30_L2                     2015-10-30 2026-07-31   2701   13.04%  23.43%   0.547   0.460  -41.91%   80.0%    7.25   2.467%
1990_sma200_vix20_L3                     2015-10-30 2026-07-31   2701    0.36%  28.58%   0.079  -0.066  -65.71%   66.5%   16.74   5.692%
1990_sma200_vix25_L3                     2015-10-30 2026-07-31   2701   15.67%  32.39%   0.545   0.414  -55.87%   76.2%    9.67   3.289%
1990_sma200_vix30_L3                     2015-10-30 2026-07-31   2701   18.25%  35.13%   0.593   0.455  -55.35%   80.0%    7.25   2.467%
1990_vix25_solo_L3                       2015-10-30 2026-07-31   2701   16.50%  37.74%   0.538   0.377  -66.04%   86.0%    9.86   3.352%

--- Bloque J: cartera de la arena (peso k en 3x, bandas de 5 pp) [fuera_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
arena_k025_sma200_vix25_L3               2015-10-30 2026-07-31   2701    6.74%   8.47%   0.550   0.528  -16.86%   76.2%  196.16   0.834%
arena_k050_sma200_vix25_L3               2015-10-30 2026-07-31   2701   10.31%  16.54%   0.543   0.487  -32.22%   76.2%  196.16   1.661%
arena_k100_sma200_vix25_L3               2015-10-30 2026-07-31   2701   15.67%  32.39%   0.545   0.414  -55.87%   76.2%    9.67   3.289%
arena_k050_sma200_vix25_L3|rezago1       2015-10-30 2026-07-31   2701    7.83%  16.56%   0.404   0.336  -36.36%   76.2%  196.16   1.671%
arena_k050_sma200_L3                     2015-10-30 2026-07-31   2701   13.21%  18.37%   0.648   0.596  -28.86%   81.3%  207.13   1.006%
arena_k050_bh_L3                         2015-10-30 2026-07-31   2701   18.97%  27.61%   0.689   0.605  -48.04%  100.0%  251.03   0.110%
arena_k050_real_UPRO_sma200_vix25        2015-10-30 2026-07-31   2701   10.81%  16.00%   0.584   0.534  -32.28%   77.8%  200.06   1.659%
arena_k050_real_TQQQ_sma200_vix25        2015-10-30 2026-07-31   2701   13.49%  21.66%   0.592   0.518  -34.76%   75.9%  195.32   1.660%

--- Temporadas de 6 meses (inicio cada mes; ventanas traslapadas) ---
variante                                      desde      hasta    n  mediana       p5      p95   %neg  DD<=12  DD<=20  DD<=28  DD<=35   peorDD dias<=-5%  peor dia
1990_bh_L1                               1990-01-03 2026-07-31  434     6.7%   -11.3%    22.4%    24%   27.9%   11.8%    3.9%    1.4%   -46.3%     0.27%    -12.0%
1990_sma200_L3                           1990-01-03 2026-07-31  434     7.5%   -30.5%    57.1%    36%   81.8%   47.7%   21.9%    8.1%   -57.2%     2.50%    -20.2%
1990_bh_L3                               1990-01-03 2026-07-31  434    15.2%   -38.5%    70.5%    30%   92.2%   59.9%   35.5%   26.0%   -89.3%     5.47%    -36.0%
arena_k025_sma200_vix25_L3               1990-01-03 2026-07-31  434     2.8%    -6.1%    13.1%    28%    0.7%    0.0%    0.0%    0.0%   -13.9%     0.00%     -4.9%
arena_k050_sma200_vix25_L3               1990-01-03 2026-07-31  434     3.9%   -13.1%    24.4%    35%   33.2%    3.0%    0.0%    0.0%   -26.3%     0.11%     -9.8%
arena_k100_sma200_vix25_L3               1990-01-03 2026-07-31  434     4.8%   -27.2%    49.5%    38%   77.9%   46.1%   20.3%    6.2%   -47.6%     1.97%    -19.7%
arena_k050_sma200_vix25_L3|rezago1       1990-01-04 2026-07-31  434     3.6%   -13.4%    24.1%    36%   30.2%    3.0%    0.0%    0.0%   -24.9%     0.12%     -9.8%
bh_L1                                    1928-10-01 2026-07-31 1169     6.6%   -18.1%    25.5%    29%   30.0%   13.9%    6.0%    2.7%   -47.9%     0.26%    -17.4%
arena_k050_sma200_L3                     1928-10-01 2026-07-31 1169     4.9%   -13.0%    34.1%    33%   30.2%    7.1%    2.1%    0.8%   -46.7%     0.28%    -13.8%
arena_k050_bh_L3                         1928-10-01 2026-07-31 1169     8.8%   -26.7%    39.9%    31%   52.1%   25.5%   14.5%    9.0%   -62.9%     0.81%    -24.1%
arena_k050_real_UPRO_sma200_vix25        2009-06-29 2026-07-31  201     6.1%   -11.5%    22.1%    30%   32.3%    1.5%    0.0%    0.0%   -20.9%     0.09%     -5.8%
arena_k050_real_TQQQ_sma200_vix25        2010-02-16 2026-07-31  193     8.9%   -17.2%    28.5%    28%   50.8%   13.5%    3.1%    0.0%   -30.9%     0.43%     -7.5%
real_UPRO_bh                             2009-06-29 2026-07-31  201    19.6%   -30.1%    65.5%    23%   89.6%   59.2%   32.8%   21.9%   -76.8%     4.82%    -34.9%
real_TQQQ_bh                             2010-02-16 2026-07-31  193    26.0%   -29.8%    87.0%    21%   96.4%   81.9%   57.0%   35.8%   -74.5%     7.78%    -34.5%
```

- **VIX.** Agregar VIX < 25 a la media de 200 días en 3x (1990-2026):
  - Baja el Sharpe en 0.090 (dentro) y 0.104 (fuera).
  - Baja el CAGR de 12.32% a 8.87% (dentro) y de 21.02% a 15.67% (fuera).
  - Cambia el MDD en +2.94 pp (dentro) y −4.92 pp (fuera).
  - Con umbral de 20, el CAGR de 3x cae a 2.73% en 1990-2026.
  - Sube los cruces del filtro a 9.6 por año, contra 5.7 de la media sola (post-hoc, sección 11.9).
- **Arena, cartera con 50% en 3x filtrado y el resto en efectivo:**
  - Temporadas de 6 meses de 1990-2026: la frecuencia de DD de −20% o peor es 3.0% y la de −35% o peor, 0.0%. El peor DD de temporada fue −26.3% y los días con pérdida de 5% o más, 0.11%.
  - Con UPRO real (2009-2026): 1.5% y 0.0%. Con **TQQQ real (2010-2026): 13.5% y 0.0%**, con peor DD de temporada de −30.9%.
  - La misma cartera tuvo **menos CAGR que el índice 1x**. En 1990-2026: 8.11% contra 10.93%. Fuera de muestra: 10.31% contra 14.54%. Con ETFs reales, fuera de muestra: UPRO al 50% 10.81% contra SPY 14.50%, y TQQQ al 50% 13.49% contra QQQ 19.12%.
  - Sin VIX (media de 200 días sola, k = 0.5), fuera de muestra: 13.21% de CAGR, Sharpe 0.648 y MDD −28.86%. Es mejor que con VIX en las tres métricas y sigue por debajo del CAGR de 1x (14.54%).
- **Lectura de `camb/a` en el bloque J.** La columna cuenta cada día en que la banda deja pasar la deriva como un "cambio". Los rebalanceos reales están en la sección 11.9 (d): 11.46 por año con k = 0.5, de los cuales 9.62 son cruces del filtro.

#### 11.9 POST-HOC (no pre-registrado; agregado después de la corrida 1)

```
================ POST-HOC (no pre-registrado; agregado despues de la corrida 1) ================
(a) Volatilidad anual 1928-10-01 a 2015-10-30 (articulo: 18.9% con S&P 500 TR de Bloomberg):
    French mercado: diaria x raiz(252) 17.12%; sesiones por año 263.2 (sabados en el tramo: 1051); diaria x raiz(sesiones) 17.49%; mensual x raiz(12) 18.78%
    ^GSPC (precio; S&P 90 antes de 1957): diaria x raiz(252) 19.07%; sesiones por año 251.2; mensual x raiz(12) 18.86%
(b) Convencion del articulo sobre ^GSPC de precio (sin dividendos), desde 1928-10-18; corridas registradas con es_prueba=0:
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
art_bh_L1                                1928-09-29 2015-10-30  22923    9.32%  17.12%   0.402   0.351  -84.07%  100.0%    0.01   0.000%
posthoc_art_gspc_bh_L1                   1928-10-17 2015-10-30  21860    5.38%  19.07%   0.201   0.109  -86.19%  100.0%    0.01   0.000%
art_bh_L2                                1928-09-29 2015-10-30  22923   14.71%  34.23%   0.465   0.333  -98.32%  100.0%    0.01   0.000%
posthoc_art_gspc_bh_L2                   1928-10-17 2015-10-30  21860    5.98%  38.15%   0.260   0.070  -98.86%  100.0%    0.01   0.000%
art_sma200_L2                            1928-09-29 2015-10-30  22923   20.18%  22.34%   0.761   0.755  -59.61%   70.9%    5.75   0.000%
posthoc_art_gspc_sma200_L2               1928-10-17 2015-10-30  21860   12.58%  24.45%   0.476   0.380  -78.84%   66.3%    5.94   0.000%
art_sma200_L3                            1928-09-29 2015-10-30  22923   29.00%  33.51%   0.804   0.767  -77.38%   70.9%    5.75   0.000%
posthoc_art_gspc_sma200_L3               1928-10-17 2015-10-30  21860   16.48%  36.68%   0.514   0.360  -93.41%   66.3%    5.94   0.000%
    posthoc_art_gspc_sma200_L2: MDD dentro de muestra -78.84% pico 1929-09-16 valle 1933-03-20
    posthoc_art_gspc_sma200_L3: MDD dentro de muestra -93.41% pico 1929-09-03 valle 1935-05-16
(c) Arena con 50% en 3x del Nasdaq-100 simulado (^NDX de precio, sin dividendos), corridas registradas con es_prueba=0:

--- post-hoc arena Nasdaq-100 [completo] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
ndx_bh_L1                                1986-07-31 2026-07-31  10076   14.09%  26.05%   0.521   0.424  -82.90%  100.0%    0.03   0.008%
ndx_sma200_L3                            1986-07-31 2026-07-31  10076   17.48%  54.17%   0.516   0.267  -96.14%   75.3%    6.92   2.354%
posthoc_arena_k050_ndx_sma200_vix25_L3   1990-01-02 2026-07-31   9211   10.10%  24.07%   0.409   0.306  -65.96%   68.7%  178.32   1.829%
posthoc_arena_k050_ndx_sma200_L3         1986-07-31 2026-07-31  10076   14.27%  27.23%   0.517   0.413  -74.27%   75.3%  193.12   1.247%

--- post-hoc arena Nasdaq-100 [dentro_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
ndx_bh_L1                                1986-07-31 2015-10-30   7375   12.58%  27.26%   0.451   0.340  -82.90%  100.0%    0.03   0.012%
ndx_sma200_L3                            1986-07-31 2015-10-30   7375   12.43%  55.78%   0.433   0.163  -96.14%   73.0%    7.69   2.616%
posthoc_arena_k050_ndx_sma200_vix25_L3   1990-01-02 2015-10-30   6510    8.73%  24.93%   0.345   0.233  -65.96%   66.0%  171.90   1.900%
posthoc_arena_k050_ndx_sma200_L3         1986-07-31 2015-10-30   7375   12.23%  28.00%   0.436   0.318  -74.27%   73.0%  187.77   1.377%

--- post-hoc arena Nasdaq-100 [fuera_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
ndx_bh_L1                                2015-10-30 2026-07-31   2701   18.28%  22.44%   0.763   0.714  -35.56%  100.0%    0.00   0.000%
ndx_sma200_L3                            2015-10-30 2026-07-31   2701   32.38%  49.50%   0.774   0.609  -56.60%   81.7%    4.84   1.644%
posthoc_arena_k050_ndx_sma200_vix25_L3   2015-10-30 2026-07-31   2701   13.45%  21.85%   0.587   0.512  -36.78%   75.2%  193.74   1.660%
posthoc_arena_k050_ndx_sma200_L3         2015-10-30 2026-07-31   2701   20.02%  24.99%   0.769   0.711  -32.48%   81.7%  207.69   0.895%
    posthoc_arena_k050_ndx_sma200_vix25_L3: MDD completo -65.96% pico 2000-03-27 valle 2010-02-05 recuperacion 2017-10-17
    posthoc_arena_k050_ndx_sma200_L3: MDD completo -74.27% pico 2000-03-27 valle 2003-03-31 recuperacion 2017-05-25
(d) Temporadas de 6 meses adicionales (mismo calculo que la seccion pre-registrada):
variante                                      desde      hasta    n  mediana       p5      p95   %neg  DD<=12  DD<=20  DD<=28  DD<=35   peorDD dias<=-5%  peor dia
arena_k050_sma200_L3 desde 1990          1990-01-03 2026-07-31  433     5.1%   -15.2%    27.6%    33%   34.4%    6.9%    2.3%    0.0%   -33.3%     0.24%     -9.8%
arena_k050_bh_L3 desde 1990              1990-01-03 2026-07-31  433     8.8%   -18.8%    33.6%    26%   49.2%   24.5%   12.9%    6.0%   -61.6%     0.84%    -18.0%
ndx_bh_L1                                1986-08-01 2026-07-31  475     9.5%   -22.5%    35.0%    25%   45.5%   18.7%   10.7%    7.2%   -58.7%     0.68%    -15.1%
posthoc_arena_k050_ndx_sma200_vix25_L3   1990-01-03 2026-07-31  434     4.3%   -20.6%    37.2%    38%   60.8%   19.4%    3.9%    1.2%   -49.4%     0.75%    -11.1%
posthoc_arena_k050_ndx_sma200_L3         1986-08-01 2026-07-31  475     6.2%   -20.5%    43.0%    36%   66.3%   21.7%    6.1%    2.1%   -56.1%     1.05%    -14.1%
real_QQQ_bh                              2006-06-23 2026-07-31  237    10.4%   -13.4%    28.3%    21%   37.6%   15.6%    5.5%    2.1%   -49.4%     0.36%    -12.0%
real_SPY_bh                              2006-06-23 2026-07-31  237     7.3%   -11.2%    20.8%    22%   27.8%    8.9%    5.5%    2.5%   -45.8%     0.36%    -10.9%
    Rebalanceos con costo por año y cruces del filtro por año (la columna camb/a del motor cuenta tambien la deriva que la banda deja pasar):
    arena_k025_sma200_vix25_L3                 rebalanceos/año 10.88  cruces del filtro/año 9.62
    arena_k050_sma200_vix25_L3                 rebalanceos/año 11.46  cruces del filtro/año 9.62
    arena_k100_sma200_vix25_L3                 rebalanceos/año 9.65  cruces del filtro/año 9.62
    arena_k050_sma200_vix25_L3|rezago1         rebalanceos/año 11.46  cruces del filtro/año 9.62
    arena_k050_sma200_L3                       rebalanceos/año 8.30  cruces del filtro/año 5.74
    arena_k050_bh_L3                           rebalanceos/año 6.10  cruces del filtro/año 0.00
    arena_k050_real_UPRO_sma200_vix25          rebalanceos/año 10.76  cruces del filtro/año 8.95
    arena_k050_real_TQQQ_sma200_vix25          rebalanceos/año 12.82  cruces del filtro/año 9.11
    posthoc_arena_k050_ndx_sma200_vix25_L3     rebalanceos/año 14.35  cruces del filtro/año 10.50
    posthoc_arena_k050_ndx_sma200_L3           rebalanceos/año 11.97  cruces del filtro/año 6.90
```

- **(a) Volatilidad.** La diaria de French anualizada con raíz de 252 (17.12%) es menor que su mensual anualizada (18.78%). En ^GSPC ambas coinciden (19.07% y 18.86%). *Inferencia:* los rendimientos diarios de CRSP tienen autocorrelación positiva, por trading no sincrónico en las décadas tempranas y por las 1,051 sesiones de sábado del tramo. Eso **subestima la varianza diaria** y, por tanto, el decaimiento de los apalancados simulados con French. Las cifras largas de 2x y 3x con French son **optimistas** frente a un fondo real sobre el S&P. Por la misma razón, la media de 10 días luce tan bien con French (14.81% contra 11.7% del artículo).
- **(b) Convención del artículo sobre ^GSPC de precio.** Se reproducen los MDD del artículo casi exactos: índice −86.19% (−86.2%), LRS 2x −78.84% (−78.7%) y LRS 3x −93.41% (−92.2%). Los CAGR no son comparables porque ^GSPC no trae dividendos.
- **(c) Arena con 3x del Nasdaq-100 simulado** (^NDX de precio, 50% y bandas):
  - Con media de 200 días y VIX < 25 (1990-2026): MDD de −65.96%, con pico el 2000-03-27, valle el 2010-02-05 y recuperación hasta 2017-10-17. Temporadas con DD ≤ −20%: 19.4%; con DD ≤ −35%: 1.2%; peor temporada −49.4%.
  - Con la media sola (1986-2026): MDD −74.27%; temporadas 21.7% y 2.1%; peor temporada −56.1%.
  - La serie larga de 3x del Nasdaq con filtro y **sin** tope de peso (`ndx_sma200_L3`, bloque H) tuvo MDD de −96.14% entre 2000 y 2009.
- **(d)** Temporadas adicionales y rebalanceos reales por año, en la salida de arriba.

### 12. Sensibilidad

**Costos (bloque D) y ejecución (bloque E):**

```
--- Bloque D: costos [dentro_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
sma200_L1|sin_costos_tx                  1928-09-29 2015-10-30  22923   11.28%  11.17%   0.693   0.714  -33.56%   70.9%    5.75   0.000%
sma200_L2|sin_costos_tx                  1928-09-29 2015-10-30  22923   17.55%  22.34%   0.666   0.637  -59.59%   70.9%    5.75   0.000%
sma200_L3|sin_costos_tx                  1928-09-29 2015-10-30  22923   23.32%  33.51%   0.675   0.597  -77.37%   70.9%    5.75   0.000%
sma200_L1|spread_medio                   1928-09-29 2015-10-30  22923    8.49%  11.20%   0.475   0.463  -40.53%   70.9%    5.75   2.531%
sma200_L2|spread_medio                   1928-09-29 2015-10-30  22923   14.60%  22.34%   0.557   0.505  -63.49%   70.9%    5.75   2.531%
sma200_L3|spread_medio                   1928-09-29 2015-10-30  22923   20.23%  33.50%   0.602   0.505  -79.93%   70.9%    5.75   2.531%
sma200_L2|fin_rf_mas_50pb                1928-09-29 2015-10-30  22923   14.86%  22.34%   0.566   0.517  -62.64%   70.9%    5.75   1.956%
sma200_L3|fin_rf_mas_50pb                1928-09-29 2015-10-30  22923   20.07%  33.50%   0.598   0.500  -79.56%   70.9%    5.75   1.956%
bh_L2|fin_rf_mas_50pb                    1928-09-29 2015-10-30  22923   10.59%  34.24%   0.362   0.213  -98.42%  100.0%    0.01   0.004%
bh_L3|fin_rf_mas_50pb                    1928-09-29 2015-10-30  22923    9.37%  51.36%   0.366   0.118  -99.89%  100.0%    0.01   0.004%
sma200_L2|doble_pierna                   1928-09-29 2015-10-30  22923   13.02%  22.37%   0.497   0.434  -70.73%   70.9%    5.75   3.912%
sma200_L3|doble_pierna                   1928-09-29 2015-10-30  22923   18.57%  33.52%   0.563   0.455  -82.86%   70.9%    5.75   3.912%

--- Bloque D: costos [fuera_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
sma200_L1|sin_costos_tx                  2015-10-30 2026-07-31   2701   10.79%  12.12%   0.724   0.703  -18.63%   81.3%    5.77   0.000%
sma200_L2|sin_costos_tx                  2015-10-30 2026-07-31   2701   17.39%  24.24%   0.694   0.624  -34.43%   81.3%    5.77   0.000%
sma200_L3|sin_costos_tx                  2015-10-30 2026-07-31   2701   23.42%  36.37%   0.704   0.582  -47.86%   81.3%    5.77   0.000%
sma200_L1|spread_medio                   2015-10-30 2026-07-31   2701    8.01%  12.18%   0.511   0.471  -23.40%   81.3%    5.77   2.537%
sma200_L2|spread_medio                   2015-10-30 2026-07-31   2701   14.45%  24.28%   0.588   0.502  -38.97%   81.3%    5.77   2.537%
sma200_L3|spread_medio                   2015-10-30 2026-07-31   2701   20.33%  36.39%   0.633   0.496  -51.84%   81.3%    5.77   2.537%
sma200_L2|fin_rf_mas_50pb                2015-10-30 2026-07-31   2701   14.64%  24.27%   0.595   0.510  -37.98%   81.3%    5.77   1.961%
sma200_L3|fin_rf_mas_50pb                2015-10-30 2026-07-31   2701   20.05%  36.38%   0.627   0.489  -51.15%   81.3%    5.77   1.961%
bh_L2|fin_rf_mas_50pb                    2015-10-30 2026-07-31   2701   22.26%  36.73%   0.673   0.544  -59.73%  100.0%    0.00   0.000%
bh_L3|fin_rf_mas_50pb                    2015-10-30 2026-07-31   2701   27.12%  55.10%   0.677   0.451  -77.20%  100.0%    0.00   0.000%
sma200_L2|doble_pierna                   2015-10-30 2026-07-31   2701   12.86%  24.32%   0.530   0.436  -41.57%   81.3%    5.77   3.921%
sma200_L3|doble_pierna                   2015-10-30 2026-07-31   2701   18.66%  36.42%   0.595   0.450  -53.88%   81.3%    5.77   3.921%

--- Bloque E: ejecucion con rezago de 1 dia [dentro_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
sma200_L1                                1928-09-29 2015-10-30  22923    9.12%  11.18%   0.525   0.520  -38.19%   70.9%    5.75   1.956%
sma200_L1|rezago1                        1928-09-29 2015-10-30  22923    8.11%  11.34%   0.440   0.423  -44.92%   70.9%    5.75   1.956%
sma200_L2                                1928-09-29 2015-10-30  22923   15.27%  22.34%   0.582   0.535  -62.45%   70.9%    5.75   1.956%
sma200_L2|rezago1                        1928-09-29 2015-10-30  22923   13.08%  22.63%   0.497   0.432  -70.22%   70.9%    5.75   1.956%
sma200_L3                                1928-09-29 2015-10-30  22923   20.93%  33.50%   0.619   0.526  -79.35%   70.9%    5.75   1.956%
sma200_L3|rezago1                        1928-09-29 2015-10-30  22923   17.37%  33.94%   0.534   0.414  -85.81%   70.9%    5.75   1.956%

--- Bloque E: ejecucion con rezago de 1 dia [fuera_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
sma200_L1                                2015-10-30 2026-07-31   2701    8.63%  12.16%   0.560   0.524  -22.00%   81.3%    5.77   1.961%
sma200_L1|rezago1                        2015-10-30 2026-07-31   2701    8.88%  12.20%   0.577   0.542  -26.24%   81.3%    5.77   1.961%
sma200_L2                                2015-10-30 2026-07-31   2701   15.11%  24.27%   0.612   0.529  -37.86%   81.3%    5.77   1.961%
sma200_L2|rezago1                        2015-10-30 2026-07-31   2701   15.62%  24.33%   0.629   0.549  -44.43%   81.3%    5.77   1.961%
sma200_L3                                2015-10-30 2026-07-31   2701   21.02%  36.38%   0.649   0.516  -50.96%   81.3%    5.77   1.961%
sma200_L3|rezago1                        2015-10-30 2026-07-31   2701   21.83%  36.47%   0.667   0.537  -58.51%   81.3%    5.77   1.961%
```

- **Spread medio (0.15% por lado):** el CAGR de LRS 2x baja a 14.60% dentro de muestra, y sigue arriba de 1x.
- **Doble pierna (el efectivo es un ETF de T-bills):** LRS 2x 13.02%.
- **Financiamiento a RF + 0.50%:** LRS 3x 20.07% dentro y 20.05% fuera.
- **Rezago de 1 día:**
  - Dentro de muestra, LRS 3x pierde 3.56 pp (20.93% a 17.37%) y su MDD pasa de −79.35% a −85.81%.
  - Fuera de muestra, el CAGR casi no cambia (21.02% a 21.83%) y el MDD empeora (−50.96% a −58.51%).

**Otros mercados, moneda y tramos:**

```
--- Bloque H: Nasdaq-100 largo (^NDX de precio, sin dividendos) [dentro_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
ndx_bh_L1                                1986-07-31 2015-10-30   7375   12.58%  27.26%   0.451   0.340  -82.90%  100.0%    0.03   0.012%
ndx_sma200_L1                            1986-07-31 2015-10-30   7375    8.40%  18.61%   0.351   0.273  -59.95%   73.0%    7.69   2.616%
ndx_bh_L2                                1986-07-31 2015-10-30   7375   12.84%  54.52%   0.435   0.175  -98.88%  100.0%    0.03   0.012%
ndx_sma200_L2                            1986-07-31 2015-10-30   7375   12.01%  37.19%   0.404   0.233  -86.00%   73.0%    7.69   2.616%
ndx_bh_L3                                1986-07-31 2015-10-30   7375    5.76%  81.78%   0.440   0.030  -99.98%  100.0%    0.03   0.012%
ndx_sma200_L3                            1986-07-31 2015-10-30   7375   12.43%  55.78%   0.433   0.163  -96.14%   73.0%    7.69   2.616%

--- Bloque H: Nasdaq-100 largo (^NDX de precio, sin dividendos) [fuera_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
ndx_bh_L1                                2015-10-30 2026-07-31   2701   18.28%  22.44%   0.763   0.714  -35.56%  100.0%    0.00   0.000%
ndx_sma200_L1                            2015-10-30 2026-07-31   2701   13.60%  16.53%   0.721   0.686  -23.85%   81.7%    4.84   1.644%
ndx_bh_L2                                2015-10-30 2026-07-31   2701   28.89%  44.89%   0.743   0.593  -63.69%  100.0%    0.00   0.000%
ndx_sma200_L2                            2015-10-30 2026-07-31   2701   23.90%  33.01%   0.750   0.656  -42.01%   81.7%    4.84   1.644%
ndx_bh_L3                                2015-10-30 2026-07-31   2701   34.56%  67.33%   0.750   0.480  -81.55%  100.0%    0.00   0.000%
ndx_sma200_L3                            2015-10-30 2026-07-31   2701   32.38%  49.50%   0.774   0.609  -56.60%   81.7%    4.84   1.644%

--- Bloque I: en MXN (DEXMXUS) [fuera_muestra] ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
mxn_cetes_bh_L1                          2015-10-30 2026-07-31   2701   15.04%  18.44%   0.454   0.402  -30.63%  100.0%    0.00   0.000%
mxn_cetes_bh_L3                          2015-10-30 2026-07-31   2701   28.96%  52.47%   0.611   0.407  -69.21%  100.0%    0.00   0.000%
mxn_cetes_sma200_L2                      2015-10-30 2026-07-31   2701   17.22%  23.31%   0.484   0.411  -37.62%   81.3%    5.77   1.961%
mxn_cetes_sma200_L3                      2015-10-30 2026-07-31   2701   23.24%  34.68%   0.567   0.450  -50.29%   81.3%    5.77   1.961%
mxn_rfusd_sma200_L3                      2015-10-30 2026-07-31   2701   21.55%  35.35%   0.616   0.533  -56.30%   81.3%    5.77   1.961%

--- Tramo posterior a la publicacion (2016-03-04 a 2026-07-31), sin registro ---
variante                                     inicio        fin      n     CAGR     vol  Sharpe  Sh_art      MDD  invert  camb/a  costo/a
bh_L1                                    2016-03-03 2026-07-31   2617   15.51%  18.35%   0.754   0.718  -34.22%  100.0%    0.00   0.000%
bh_L2                                    2016-03-03 2026-07-31   2617   24.88%  36.70%   0.729   0.614  -59.71%  100.0%    0.00   0.000%
bh_L3                                    2016-03-03 2026-07-31   2617   31.51%  55.05%   0.737   0.530  -77.18%  100.0%    0.00   0.000%
sma200_L1                                2016-03-03 2026-07-31   2617    9.93%  12.29%   0.645   0.618  -22.00%   83.0%    5.09   1.731%
sma200_L2                                2016-03-03 2026-07-31   2617   17.45%  24.54%   0.687   0.616  -37.86%   83.0%    5.09   1.731%
sma200_L3                                2016-03-03 2026-07-31   2617   24.48%  36.79%   0.721   0.602  -50.96%   83.0%    5.09   1.731%
sma200_L2|rezago1                        2016-03-03 2026-07-31   2617   17.88%  24.55%   0.701   0.633  -44.43%   83.0%    5.09   1.731%
sma200_L3|rezago1                        2016-03-03 2026-07-31   2617   25.18%  36.81%   0.735   0.621  -58.51%   83.0%    5.09   1.731%
real_SPY_bh                              2016-03-03 2026-07-31   2617   15.38%  17.75%   0.767   0.735  -33.72%  100.0%    0.00   0.000%
real_QQQ_bh                              2016-03-03 2026-07-31   2617   20.59%  22.23%   0.852   0.821  -35.12%  100.0%    0.00   0.000%
real_SSO_bh                              2016-03-03 2026-07-31   2617   24.08%  35.50%   0.723   0.612  -59.34%  100.0%    0.00   0.000%
real_SSO_sma200                          2016-03-03 2026-07-31   2617   17.75%  23.79%   0.711   0.648  -40.63%   84.4%    5.09   1.731%
real_UPRO_bh                             2016-03-03 2026-07-31   2617   30.12%  53.17%   0.724   0.522  -76.82%  100.0%    0.00   0.000%
real_UPRO_sma200                         2016-03-03 2026-07-31   2617   24.79%  35.66%   0.739   0.630  -53.72%   84.4%    5.09   1.731%
real_UPRO_sma200|rezago1                 2016-03-03 2026-07-31   2617   22.49%  35.75%   0.685   0.564  -59.69%   84.4%    5.09   1.731%
real_QLD_bh                              2016-03-03 2026-07-31   2617   33.20%  44.42%   0.818   0.695  -63.68%  100.0%    0.00   0.000%
real_QLD_sma200                          2016-03-03 2026-07-31   2617   25.81%  33.09%   0.793   0.710  -43.83%   83.3%    4.90   1.666%
real_TQQQ_bh                             2016-03-03 2026-07-31   2617   40.84%  65.78%   0.820   0.585  -81.66%  100.0%    0.00   0.000%
real_TQQQ_sma200                         2016-03-03 2026-07-31   2617   35.27%  49.21%   0.818   0.669  -57.79%   83.3%    4.90   1.666%
real_TQQQ_sma200|rezago1                 2016-03-03 2026-07-31   2617   35.55%  50.25%   0.817   0.661  -61.24%   83.3%    4.90   1.666%
```

- **Nasdaq-100 (1986-2015):**
  - 3x comprar y mantener: CAGR 5.76% y MDD −99.98%, sin recuperarse dentro de muestra.
  - 3x con filtro: CAGR 12.43% y MDD −96.14%, casi igual que el índice 1x (12.58%) y con mucho más riesgo.
  - Fuera de muestra el filtro sobre 3x dio Sharpe de 0.774 contra 0.763 de 1x, con MDD de −56.60% contra −35.56%.
- **En MXN con Cetes como efectivo (fuera de muestra):** LRS 3x 23.24% (Sharpe 0.567, MDD −50.29%) contra índice 1x 15.04% (0.454, −30.63%). *Inferencia:* el Sharpe se mide contra Cetes, y en pesos el ordenamiento cambia frente al de USD.
- **Tramo posterior a la publicación (2016-03-04 a 2026-07-31):** LRS 3x 24.48% (Sharpe 0.721) contra índice 0.754 y 3x comprar y mantener 31.51%. Es el mismo patrón que `fuera_muestra`.
- **Señal sobre índice de precio en lugar del ETF de rendimiento total, fuera de muestra:** UPRO 16.82% (contra 21.52% con SPY) y TQQQ 34.15% (contra 32.13% con QQQ). La regla es sensible a qué serie define el cruce.

### 13. Diferencia frente al artículo

| Aspecto | Artículo | Réplica | ¿Explica la diferencia? |
|---|---|---|---|
| Datos | S&P 500 TR diario de Bloomberg; antes de 1957 es el S&P 90 | Mercado CRSP de French (Mkt-RF + RF), CRSP 202607, con sábados hasta 1952 | **Sí para C1 y C4 (post-hoc).** Con ^GSPC se reproducen la volatilidad y los MDD del artículo. French subestima la varianza diaria y hace optimistas los apalancados simulados |
| Periodo | Oct-1928 a oct-2015 | Igual (1928-10-01 a 2015-10-30) y fuera de muestra hasta 2026-07-31 | — |
| Financiamiento | No lo cobra: solo una comisión de 1% anual (verificado con sus propias cifras, sección 1) | (L−1)·RF + 0.9% anual | **Sí:** explica 2.6 pp (2x) y 5.7 pp (3x) de CAGR dentro de muestra |
| Costos de transacción | Ninguno | 0.29% + 0.05% por lado; 5.75 cambios por año | **Sí:** ≈ 2.3 pp de CAGR por año |
| Ejecución | Al cierre, sin rezago declarado | Al cierre (principal) y con rezago de 1 día | Con rezago, 2.19 pp (2x) y 3.56 pp (3x) menos de CAGR dentro de muestra |
| Sharpe | Tabla 8 no reproducible con su propia fórmula (sección 1) | Motor (exceso diario) y fórmula del artículo | **No explicada:** discrepancia interna de la fuente |
| ETFs reales | Solo los menciona (SSO, UPRO) | SSO, UPRO, QLD y TQQQ reales, 2006-2026 | El simulador sobreestima 0.7 a 1.6 pp por año |

### 14. Conclusiones permitidas

Todas valen para el mercado accionario de EUA, en USD salvo donde se indica, con los costos declarados y sin impuestos.

1. **El mecanismo del decaimiento está replicado.** Un apalancado L× con re-apalancamiento diario pierde ≈ L(L−1)σ²/2 por año frente a "L veces el índice". En 99 años, la pendiente medida es 1.00 a 1.01 veces la teórica, con R² ≥ 0.99. Con σ de 20%, un 3x pierde ≈ 12% anual solo por varianza.
2. **La media de 200 días separa regímenes de volatilidad.** Dentro de muestra, abajo de la media la volatilidad fue 1.8 veces la de arriba, y un 3x perdió 17.7% por año por varianza, contra 5.3% arriba. Es la razón por la que el filtro vale más en 3x que en 1x.
3. **El hallazgo del artículo se reproduce en signo y magnitud con su convención** (LRS 2x 20.18% contra 19.1%; 3x 29.00% contra 26.8%). Esa convención **omite el financiamiento** de la parte prestada y todos los costos de transacción.
4. **Con implementación realista, en 1928-10 a 2015-10, el filtro sigue ganándole al índice 1x:** LRS 2x 15.27% (Sharpe 0.582, MDD −62.45%) y LRS 3x 20.93% (0.619, −79.35%), contra 9.31% (0.402, −84.07%). Esto con datos de French, que hacen optimistas a los apalancados (sección 11.9 a).
5. **Fuera de muestra (2015-11 a 2026-07) el veredicto pre-registrado es "Solo protección".** El filtro redujo el drawdown frente al mismo apalancado comprado y mantenido, en la simulación y en SSO, UPRO, QLD y TQQQ reales, también con rezago de 1 día. En cambio, el Sharpe quedó debajo del índice 1x y el CAGR debajo del ETF comprado y mantenido.
6. **El simulador reproduce a los ETFs reales** con correlación diaria ≥ 0.9956 y sobreestima su CAGR entre 0.7 pp (2x) y 1.6 pp (3x) por año.
7. **El VIX < 25 no mejoró la regla** en 1990-2026: bajó el Sharpe en ≈ 0.1 y no redujo el MDD de forma consistente.
8. **Con 50% en un 3x tipo S&P filtrado, las temporadas de 6 meses casi nunca tocaron −20%** (3.0%) ni −35% (0.0%). La misma cartera rindió menos que el índice 1x en 1990-2026 y fuera de muestra.

### 15. Conclusiones que NO se sostienen

- **"El filtro de 200 días aumenta el rendimiento de un apalancado."** Dentro de muestra, la diferencia media diaria contra el mismo apalancado es ≈ 0 (t = 0.04 y 0.24). Fuera de muestra y en UPRO y TQQQ reales es negativa. La ventaja de CAGR viene de menos varianza, y no apareció después de 2015.
- **"LRS le gana al S&P ajustado por riesgo después de publicarse."** Fuera de muestra, el Sharpe fue 0.612 (2x) y 0.649 (3x), contra 0.712 del índice.
- **"Con ETFs se pueden lograr 19.1% (2x) o 26.8% (3x) anual."** Las cifras del artículo no cobran el financiamiento ni los costos.
- **"El VIX < 25 reduce el riesgo del apalancado."** El MDD mejoró +2.94 pp dentro de muestra y empeoró 4.92 pp fuera; los umbrales 20 y 30 no dan el mismo signo.
- **"El límite de 50% es igual de seguro con TQQQ."** No se probó con criterio pre-registrado. Los datos apuntan a lo contrario: TQQQ real al 50% tocó −20% en 13.5% de las temporadas, y el Nasdaq simulado al 50% tuvo MDD de −66% (post-hoc).
- **"Un 3x sin filtro siempre pierde contra 1x."** Con French, 3x comprar y mantener realista rindió 10.47% contra 9.31% dentro de muestra y 28.40% contra 14.54% fuera, pero con MDD de −99.89% y −77.18%.
- **"DSR ≥ 0.95 prueba que la regla supera al índice."** El DSR contrasta contra 0, y fuera de muestra tampoco pasa (0.84).
- **"Funciona en MXN", "funcionará en el futuro" o "tiene ventaja con dinero real".** Nada de esto se probó: no hay impuestos, spread cambiario de GBM, liquidez real del SIC ni papel.

### 16. Estado y reproducción

- **Estado: Replicado con diferencias**, según las reglas pre-registradas: C1 y C4 fallan, no hay refutación y el efecto aparece en 8 de 9 ventanas. Los datos explican C1 y C4 (post-hoc: ^GSPC reproduce la volatilidad y los MDD). Queda sin explicar la inconsistencia del Sharpe de la Tabla 8 del artículo.
- **Veredicto fuera de muestra:** "Solo protección", simulado y en ETFs reales.
- **Estados de conocimiento:**
  - El decaimiento L(L−1)σ²/2 pasa a **Replicado**.
  - "Apalancar solo sobre la media de 200 días" pasa a **Replicado con diferencias**, con el matiz de que protege y no agrega rendimiento después de 2015.
- **Comando que reproduce todo:** `python3 laboratorio/replicas/R06.py`, desde `/home/user/New1`; tarda ≈ 35 s. Verificación: `python3 laboratorio/replicas/R06_verificacion.py`. Prueba sin red: `python3 laboratorio/replicas/R06.py --prueba-sintetica`.
- **Huellas:**
  - French diario CRSP 202607: sha256 `1916d331c2c51d2aee3d00215897d2b8e5995cb387f1f4569ba46bff5fb049a8`, congelado en `R06-datos/`.
  - `huella_datos` del CSV: `bh_L1` a167a7fa2e659d4e, `sma200_L2` 300a19978ac2f280, `real_UPRO_bh` 266703968d2c90c1 y `real_TQQQ_bh` 21966bdd0b86ed1d.
  - Yahoo y FRED no se congelan; su huella está en `R06-salida.txt`.
- **Fecha de la corrida final:** 2026-09-25T06:25:57Z (corrida 2).

### 17. Conclusión operable

Se aplican las reglas fijadas en la sección 2. `config/parametros.json` **no** se modificó. Las propuestas van al comité.

1. **`filtro_apalancados`, parte de la media de 200 días (R2 del cap. 14): se confirma**, como regla de **protección**, no de rendimiento.
   - Condiciones cumplidas: el estado no es "No replicado", el veredicto fuera de muestra es "Solo protección" y el MDD baja en UPRO y TQQQ reales con las dos ejecuciones.
   - Beneficio fuera de muestra: MDD de UPRO de −76.82% a −53.72% (−59.69% con rezago) y de TQQQ de −81.66% a −57.79% (−61.24%).
   - Costo fuera de muestra: CAGR de UPRO de 27.33% a 21.52% (18.65% con rezago) y de TQQQ de 35.99% a 32.13% (31.17%).
   - La ejecución real en GBM será al día siguiente de la señal. En apalancados sobre el S&P eso costó de 1.84 a 3.56 pp por año: SSO y UPRO reales fuera de muestra −1.84 y −2.87 pp; 2x y 3x simulados dentro de muestra −2.19 y −3.56 pp.
2. **`filtro_apalancados`, parte de VIX < 25: se propone quitarla o dejarla opcional.**
   - No pasó el criterio: el MDD no mejora ≥ 5 pp en los dos segmentos, el Sharpe baja 0.09 y 0.10, y los umbrales 20 y 30 no dan el mismo signo.
   - Con k = 0.5, fuera de muestra, la media sola dio más CAGR (13.21% contra 10.31%), más Sharpe (0.648 contra 0.543) y menos MDD (−28.86% contra −32.22%).
   - Matiz post-hoc: en el Nasdaq simulado el VIX sí bajó el MDD de la cartera al 50% (−74.27% a −65.96%). La decisión es del comité.
3. **`concentracion.etf_apalancado_max` = 0.5: "Sensato"** según la prueba pre-registrada (3x tipo S&P).
   - Temporadas con DD ≤ −20%: 3.0%, también 3.0% con rezago. Con DD ≤ −35%: 0.0%. Con la media sola en 1928-2026: 7.1% y 0.8%.
   - **Reserva 1:** con TQQQ real, la frecuencia de −20% fue 13.5%, arriba del 10% que define "sensato". En el Nasdaq simulado (post-hoc) fue 19.4%, con un MDD de −66% entre 2000 y 2010. Para 3x sobre el Nasdaq-100 la evidencia **no** respalda 0.5. Queda pendiente probar un tope menor para TQQQ; no se probó ningún valor.
   - **Reserva 2:** para el objetivo de la arena (máximo TWR), 50% en 3x filtrado y el resto en efectivo rindió **menos** que el índice 1x en 1990-2026 y fuera de muestra. El límite es prudente como tope de riesgo, pero esa configuración no gana sola. Qué hacer con el otro 50% (por ejemplo, índice 1x dentro de `etf_indice_max`) no se probó.
4. **Cortacircuito de −20% ("sin ETFs apalancados") y límite diario de 5%: coherentes.**
   - Con 50% en 3x filtrado, el −20% se tocó en 3.0% de las temporadas (1.5% con UPRO y 13.5% con TQQQ).
   - Los días con pérdida de 5% o más fueron 0.11% (simulado), 0.09% (UPRO) y 0.43% (TQQQ).
5. **Ninguna regla pasa a dinero** sin papel durante 3 meses y 30 operaciones (README del laboratorio, sección 1). Faltan también la liquidez real en el SIC y el spread cambiario de GBM.
