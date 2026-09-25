# Réplica R06: ETFs apalancados 2x y 3x y filtro de tendencia de 200 días (Gayed y Bilello, 2016)

| Campo | Valor |
|---|---|
| ID | `R06`. El registro de variantes es `replicas/R06-variantes.csv`; el nombre largo del archivo es `R06-apalancados-y-filtro-de-tendencia` |
| Artículo o hallazgo | Gayed, Michael A. y Charlie Bilello (2016), "Leverage for the Long Run – A Systematic Approach to Managing Risk and Magnifying Returns in Stocks". Trabajo presentado al Charles H. Dow Award 2016 (CMT Association). SSRN 2741701, DOI 10.2139/ssrn.2741701. Versión consultada: PDF de la CMT Association, https://docs.cmtassociation.org/dow-award/2016-gayed-bilello.pdf, 19 páginas, sha256 `c181b05d60649ee96df7e7fab08c59f7afd3b1ee9847f3d4952edc29f0c6703e`. Texto extraído con pypdf el 2026-09-25. La página de SSRN respondió 403 y no se abrió. No es un artículo con revisión de pares: es un trabajo de premio de una asociación profesional. |
| Fecha de publicación (primera versión pública) | 2016-03-03 en SSRN, según el resultado de búsqueda de SSRN. CXO Advisory lo resume como "March 2016 paper". La muestra del artículo termina en octubre de 2015. |
| Pre-registro escrito el | 2026-09-25, terminado a las 06:13 UTC (sha256 de las secciones 1 a 9: `b12cbc772436d4c0f6b02f4f1284c636e663041d0c92080b69d8b6e2e4797699`; el script se detiene si cambia), **antes de cualquier corrida de backtest**. Antes de escribirlo solo se descargaron los datos y se revisaron rangos, versiones y huecos (lista en la sección 3). No se calculó ninguna métrica de ninguna regla ni de ninguna serie apalancada. |
| Responsable | Claude (laboratorio de réplicas, fase 0). Mandato: Eduardo Iván Izurieta Martínez |
| Estado | Pendiente (se llena al final, en la sección 16) |

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

### 10. Variantes probadas

### 11. Resultados

### 12. Sensibilidad

### 13. Diferencia frente al artículo

### 14. Conclusiones permitidas

### 15. Conclusiones que NO se sostienen

### 16. Estado y reproducción
