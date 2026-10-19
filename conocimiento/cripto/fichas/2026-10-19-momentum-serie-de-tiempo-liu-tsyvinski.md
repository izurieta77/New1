# Ficha de avance · 19-oct-2026 · Momentum de serie de tiempo en BTC: Liu y Tsyvinski (RFS 2021) replicado fuera de muestra

> Corrida de las 08:17 CDMX (14:2x UTC), estudio profundo. Nivel **Doctorado** (literatura académica sobre factores cripto), grupo G5 (mercado, on-chain e institucional).
>
> **Por qué este tema.** Los 35 recursos del dueño están en `estudiado`, los 6 temas del plan tienen ficha y el punto 5 del plan de cobertura (ETFs de ether) se cerró ayer. En el temario del rol, el Doctorado pide "literatura académica (JF, RFS, JFE, NBER, SSRN) sobre valuación, factores cripto, manipulación y microestructura". Una búsqueda en `conocimiento/` no encontró ni una cita de Liu-Tsyvinski, Makarov-Schoar ni Griffin-Shams: es el hueco académico más grande de la carrera. Se empieza por el factor que más toca la cuenta, el momentum, porque el filtro SMA200 de `arena-claude-binance` es una regla de tendencia.

## 0. Preguntas de hoy

1. ¿Qué afirman, con sus números, los dos papers de referencia sobre factores cripto?
2. ¿Sobrevive el momentum semanal de BTC fuera de su muestra (jun-2018 a oct-2026)?
3. ¿Qué dice esto del filtro de tendencia de la cuenta y del pronóstico de hoy?

## 1. Acceso y fuentes (declarado)

- **Liu, Y. y Tsyvinski, A. "Risks and Returns of Cryptocurrency".** NBER WP 24877 (ago-2018), publicado en *The Review of Financial Studies* 34(6):2689-2727 (2021). [Página NBER](https://www.nber.org/papers/w24877) y [PDF](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf), 68 páginas. **Acceso: sección.** Se extrajo el texto completo y se leyeron el resumen, la sección 2 (datos) y la 4.1 (momentum, tablas 14-18). **No se leyó la versión publicada en la RFS**, que puede tener otros números. La página de NBER nombra a Itay Goldstein junto a la cita de la RFS; lo más probable es que sea el editor y no un coautor (sin verificar).
- **Liu, Y., Tsyvinski, A. y Wu, X. "Common Risk Factors in Cryptocurrency".** NBER WP 25882 (may-2019), publicado en *The Journal of Finance* 77(2):1133-1177 (2022). [Página NBER](https://www.nber.org/papers/w25882) y [PDF](https://www.nber.org/system/files/working_papers/w25882/w25882.pdf), 48 páginas. **Acceso: sección** (resumen e introducción, págs. 1-5).
- **Datos para la réplica, grado A:** klines semanales BTCUSDT de [`data-api.binance.vision`](https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1w&limit=1000). Son 478 semanas cerradas, del 27-ago-2017 al 18-oct-2026. El paper usa CoinDesk con corte del domingo a las 23:59:59 UTC; la vela semanal de Binance cierra a la misma hora.
- **Conflictos de interés:** ninguno declarado en el WP (académicos de Yale).

## 2. Lo que dicen los papers [H, grado A en el texto del WP]

**Liu y Tsyvinski (2021).** Muestra de BTC del 1-ene-2011 al 31-may-2018 (CoinDesk).
- Las criptomonedas "have no exposure to most common stock market and macroeconomic factors" y su rendimiento se predice con factores propios: el **momentum de serie de tiempo** y la **atención de los inversionistas** (búsquedas en Google y Twitter).
- **Tabla 14, panel B (semanal):** el rendimiento de esta semana predice el de 1, 2, 3 y 4 semanas después, con betas de **0.19, 0.22, 0.21 y 0.09** (t de 3.73, 4.52, 4.26 y 1.72; con bootstrap, 2.17, 2.73, 2.47 y 1.40). El R² es de 0.01-0.05. Con una σ semanal de 16.64%, una σ más de rendimiento hoy suma 3.16 pp a la semana siguiente.
- **Tabla 15 (quintiles):** a una semana, el quintil alto rinde 11.22% semanal (Sharpe semanal 0.45) y el bajo 2.60%. **Tabla 17 (cortes con los primeros 2 años, sin mirar adelante):** diferencia Q5−Q1 de **+4.53 pp por semana**.
- **Tabla 16 (desde 2013):** el efecto se mantiene, "of somewhat smaller magnitude".
- En ETH el momentum diario solo es significativo a 1 y 5 días, y a 5 días con signo negativo.

**Liu, Tsyvinski y Wu (2022).** Corte transversal de 109 a 1,583 monedas (2014-2018).
- Tres factores (mercado cripto, tamaño y momentum) explican las nueve estrategias largo-corto rentables.
- El momentum de 1 a 4 semanas da 2.5-4.1% semanal largo-corto, y funciona **solo entre las monedas grandes**: 4.2% semanal sobre la mediana de tamaño contra un 0.6% no significativo debajo de ella.
- Los modelos de acciones (Fama-French 3 y 5, Carhart) no explican esos rendimientos.

## 3. Ejercicio numérico: réplica fuera de muestra (comprobado en Python)

Script: [`2026-10-19-momentum-serie-de-tiempo-liu-tsyvinski.py`](2026-10-19-momentum-serie-de-tiempo-liu-tsyvinski.py) (`python3 -I ...`, solo biblioteca estándar). Se corrió el 19-oct hacia las 14:25 UTC. Toma 438 semanas cerradas después del fin de la muestra del paper (desde el 3-jun-2018). Se usa MCO con t ordinaria y t de Newey-West (rezagos h+3).

**[1] Regresión R_{t+h} = a + b·R_t.**

| h | beta paper (2011-2018) | beta fuera de muestra | t MCO | t Newey-West | R² |
|---|---|---|---|---|---|
| 1 | +0.19 | **+0.117** | +2.46 | **+2.58** | 0.014 |
| 2 | +0.22 | +0.016 | +0.33 | +0.31 | 0.000 |
| 3 | +0.21 | −0.029 | −0.61 | −0.67 | 0.001 |
| 4 | +0.09 | +0.076 | +1.59 | +1.60 | 0.006 |

- La σ semanal bajó de 16.64% a **8.27%**. Una σ más de rendimiento hoy suma **+0.97 pp** a la semana siguiente (el paper daba 3.16).
- **Solo sobrevive h = 1**, con una beta 40% menor. Los horizontes de 2 y 3 semanas, que en el paper eran los más fuertes, desaparecen.

**[2] El efecto se está apagando.** Beta a una semana por mitades:
- 3-jun-2018 a 7-ago-2022: **+0.143** (t NW +2.38, n=218);
- 14-ago-2022 a 18-oct-2026: **+0.061** (t NW +1.07, n=218), **no significativo**.

**[3] Quintiles sin mirar adelante** (cortes con jun-2018 a may-2020: −5.35%, −0.62%, +2.68% y +7.06%; evaluación en 333 semanas):

| Quintil | n | R_{t+1} medio | t |
|---|---|---|---|
| Q1 | 49 | −0.64% | −0.56 |
| Q2 | 88 | +1.17% | +1.48 |
| Q3 | 80 | +1.04% | +1.35 |
| Q4 | 55 | −1.11% | −1.18 |
| Q5 | 61 | **+3.63%** | **+3.31** |

- Q5−Q1 = **+4.27 pp por semana**, cerca del +4.53 del paper. **Pero no es monótono:** Q4 rinde menos que Q2 y Q3, así que todo el efecto está en las semanas extremas al alza.
- Sin sus 5 mejores semanas siguientes, Q5 baja de +3.63% a **+2.16%**: la cola pesa mucho.

**[4] Una regla operable: largo solo si la semana anterior fue positiva**, sin costos.
- CAGR de **+25.0%** y Sharpe anual de **0.72**, contra +32.5% y 0.77 de comprar y mantener.
- Está largo 230 de 437 semanas y **cambia de posición 227 veces** (unas 27 al año). Con 0.1% por lado en Binance son ~5.4% al año de costos; con 0.29% en GBM, ~16%.
- **La regla simple pierde contra comprar y mantener aun sin costos.**

**[5] Tasa base binaria para el pronóstico de hoy.** La semana del 12 al 18-oct cerró en −1.98% (82,116.00), es decir, en Q2.
- P(semana siguiente > 0): **52.4%** en todas las semanas (n=437, ee 2.4 pp); **57.3%** tras una semana en Q2 (n=110, ee 4.7 pp); **54.6%** tras cualquier semana negativa (n=207).
- Que una semana negativa preceda a más subidas que el promedio **contradice el signo del momentum** en lectura binaria: el efecto vive en la magnitud de las semanas extremas, no en la dirección.

## 4. Qué cambia para invertir [I/O]

1. **El filtro SMA200 de la cuenta no se apoya en este paper.** Liu y Tsyvinski miden momentum de 1 a 4 semanas; el filtro es una tendencia de unos 7 meses con banda de ±3%. Su respaldo está en otro lado (literatura de tendencia en futuros y la decisión del comité). Esta ficha no lo refuerza ni lo debilita, pero sí prohíbe citar "Liu-Tsyvinski" como respaldo académico del filtro.
2. **No hay que operar el momentum semanal.** La beta se redujo a menos de la mitad desde 2022, el efecto lo cargan pocas semanas y la regla simple pierde contra mantener aun sin costos. Con la comisión de GBM sería peor. [I, B]
3. **Lectura útil:** una semana muy fuerte (> +7%) ha tendido a seguir con otra semana arriba del promedio. Sirve para **no vender por "ya subió mucho"** en el pulso, no para comprar.
4. **Patrón de decaimiento:** es lo que esperaría la literatura sobre anomalías publicadas, en la que el rendimiento baja después de la publicación (McLean y Pontiff, JF 2016, ya citados en la base). Lo de cripto es [I], sin prueba formal de quiebre estructural.

## 5. Contrapuntos y límites

- **Fuente de precios distinta:** el paper usa CoinDesk (índice de varios exchanges); la réplica, Binance BTCUSDT (un solo exchange, en USDT). Antes de 2019 la diferencia pudo ser de varios puntos en semanas de estrés.
- **Rendimiento simple, no logarítmico ni en exceso de la tasa libre.** El paper habla de rendimientos sin definirlos con detalle en la sección leída. Con tasas de hasta 5%, el ajuste semanal es de ~0.1 pp y no cambia el signo.
- **Comparaciones múltiples:** se probaron 4 horizontes, 5 quintiles y 2 mitades. Un t de 2.5 en uno de 4 horizontes es evidencia moderada, no fuerte.
- **No se replicaron** la atención (Google Trends) ni el corte transversal de LTW (2022), que necesita cientos de monedas con capitalización histórica.
- **Solo WP:** no se leyó la versión publicada en la RFS ni la del JF.

## 6. Autoexamen

1. ¿Qué tres factores explican el corte transversal cripto en LTW (2022)? → Mercado, tamaño y momentum.
2. ¿Cuál era la beta semanal a 1 semana en Liu-Tsyvinski y cuál es fuera de muestra? → 0.19 contra 0.117; desde ago-2022, 0.061 sin significancia.
3. ¿Por qué la diferencia Q5−Q1 parecida a la del paper no prueba que el efecto siga igual? → Porque no es monótona (Q4 < Q3), la cargan las semanas extremas y la regla operable pierde contra mantener.
4. ¿Respalda este paper el filtro SMA200? → No: mide 1 a 4 semanas, no 200 días.

## 7. Estado

- **Estado:** Documentado con comprobación (texto del WP leído en sección y réplica en Python con datos primarios).
- **Grado:** A en lo que dice el WP; B en la réplica (un exchange, rendimiento simple); C en la explicación del decaimiento.
- **Pendientes de Doctorado (cola):**
  - Makarov y Schoar (JFE 2020), arbitraje y segmentación entre exchanges, con la prima de BTCMXN como caso;
  - Griffin y Shams (JF 2020), ¿Tether infló el precio en 2017?: manipulación;
  - atención de los inversionistas (Google Trends) como predictor, sección 4.2 del WP;
  - la versión publicada en la RFS (cotejar las tablas).
- **Pronóstico:** P0148 (la vela semanal BTCUSDT del 19 al 25-oct cierra arriba de 82,116.00, p=0.52).
