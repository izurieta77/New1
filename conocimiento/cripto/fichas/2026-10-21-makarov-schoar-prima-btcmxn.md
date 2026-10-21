# Ficha de avance · 21-oct-2026 · Arbitraje entre exchanges: Makarov y Schoar (JFE 2020) y la prima de BTCMXN

> Corrida de las 08:17 CDMX (14:2x UTC), estudio profundo. Nivel **Doctorado** (literatura de microestructura y arbitraje), grupo G5 (mercado, on-chain e institucional).
>
> **Por qué este tema.** Los 35 recursos están `estudiado`. La cola académica del plan, fijada el 19-oct, sigue con Makarov-Schoar (JFE 2020), y `estado-de-dominio.csv` lo pedía "con la prima de BTCMXN". Hoy además es útil: la señal E9 (liquidez de BTCMXN) lleva dos episodios ÁMBAR en dos días, y el paper es la referencia para separar un **precio desalineado** de un **libro delgado**.

## 0. Preguntas de hoy

1. ¿Qué encontraron Makarov y Schoar sobre las primas entre países, y en particular sobre México (Bitso)?
2. ¿Existe hoy una prima de BTC en pesos en Binance? ¿Cuánto dura y qué la mueve?
3. ¿Qué dice esto de E9 y de cómo salir de la posición si llega a hacer falta?

## 1. Acceso y fuentes (declarado)

- **Makarov, I. y Schoar, A. (2020). "Trading and arbitrage in cryptocurrency markets".** *Journal of Financial Economics* 135(2):293-319, [doi:10.1016/j.jfineco.2019.07.001](https://doi.org/10.1016/j.jfineco.2019.07.001).
  - **Acceso: íntegro de la versión aceptada del autor** (LSE Research Online, CC BY-NC-ND, 57 págs., [PDF](https://researchonline.lse.ac.uk/id/eprint/100409/1/Cryptocurrency_Markets_JFE_final_v4.pdf)). Se extrajo el texto completo. Se leyeron la introducción, la 8.2 y las tablas 1, 5 y A2, y el resto se buscó por palabra clave. La versión publicada en Elsevier no se leyó: puede haber diferencias.
  - También se descargó el documento de discusión FMG DP782 (LSE, 56 págs.). Solo se usó para cotejar que el resumen dice "up to 85%" y el JFE "80%".
- **Datos de la réplica, grado A:**
  - velas 1h BTCMXN y BTCUSDT de [`data-api.binance.vision`](https://data-api.binance.vision/api/v3/klines?symbol=BTCMXN&interval=1h&limit=1000);
  - USD/MXN 1h de [Yahoo MXN=X](https://query1.finance.yahoo.com/v8/finance/chart/MXN=X?interval=1h&range=90d);
  - foto del libro de [Binance BTCMXN](https://data-api.binance.vision/api/v3/depth?symbol=BTCMXN&limit=100) y de [Bitso btc_mxn](https://api.bitso.com/v3/order_book/?book=btc_mxn&aggregate=true).
- **Conflictos de interés:** son académicos (LSE y MIT Sloan) y los datos los dio Kaiko, un proveedor comercial. No se declara ninguna tenencia.

## 2. Lo que dice el paper [H, grado A en el texto de la versión aceptada]

- **Muestra:** 34 exchanges de 19 países, con datos de operación por operación, de ene-2017 a feb/abr-2018. **México entra con Bitso** (tabla 1).
- **Primas grandes y repetidas, mucho mayores entre países que dentro de un mismo país.**
  - Corea sobre EUA: más de 15% en promedio de dic-2017 a feb-2018, con picos de 40% (la "prima kimchi"). Japón ~10% y Europa ~3%.
  - Dentro de un mismo país, la desviación promedio "typically does not exceed 1%".
  - Ganancia potencial mínima de US$2 mil millones entre dic-2017 y feb-2018.
- **Las primas son asimétricas** (fuera de EUA y Europa casi nunca hay descuento) **y se mueven juntas.** Se abren cuando BTC sube rápido.
  - La "beta de arbitraje" de cada país es la pendiente de su prima contra la desviación del log precio de EUA respecto de su tendencia Hodrick-Prescott semanal.
  - **Tabla 5, México: prima 0.027 (2.7%) y beta 0.078.** Corea: 0.066 y 0.22. EUR y CAD: cerca de cero.
  - En el corte transversal, la prima sube con la beta: pendiente 0.3, t 4.6, R² 0.56 (fig. 8).
  - Tabla A2: la prima de MXN tiene correlación de 0.65 con la de KRW y de 0.67 con la de JPY.
- **El mecanismo son los controles de capital, no los costos de transacción.**
  - La correlación entre las primas de dos países sube con el producto de sus índices de control de capital (Fernández et al. 2015): pendiente 0.29, t 3, R² 0.07 (fig. 9).
  - Entre dos criptos en el mismo exchange la prima es un orden de magnitud menor: ETH/BTC ~3% cuando USD/KRW-BTC pasaba de 20%.
  - Los costos de un participante grande son de 50-75 pb ida y vuelta (sección 8.2). No explican primas de 10-40%.
- **Flujo de órdenes.**
  - El componente común del volumen firmado explica ~50% de los rendimientos a 5 min y 1 h, y hasta 80-85% a nivel diario.
  - Comprar 10,000 BTC en un día sube el precio ~3-4%, y el efecto es casi permanente.
  - Los residuos de volumen de cada exchange explican su prima propia, y una prima positiva predice que ese exchange rendirá menos después.
- **Su predicción para el futuro (sección 1):** las stablecoins (tether, la versión digital del dólar de Circle) "pueden disminuir el papel de los controles de capital".

## 3. Ejercicio numérico: la prima de BTCMXN en Binance, 23-jul a 21-oct-2026 (comprobado en Python)

Código: [`2026-10-21-makarov-schoar-prima-btcmxn.py`](2026-10-21-makarov-schoar-prima-btcmxn.py), solo con datos públicos. Se corre con `python3 -I`.

Definición: prima_t = ln(cierre BTCMXN / (cierre BTCUSDT × USD/MXN)), por hora, solo en horas con al menos una operación en BTCMXN y con barra de USD/MXN. No hay fines de semana porque Yahoo no tiene FX esos días.

| Medida | Resultado | Comprobación |
|---|---|---|
| Muestra | 1,524 horas con FX; 1,486 con operación (98%); volumen medio 1.07 BTC/día | — |
| Prima media / mediana | **+0.034% / +0.042%** | Prima simple, no log: +0.034% / +0.042% |
| Dispersión | p5 −0.215%, p95 +0.276%, desviación estándar 0.175% | Mínimo −2.64%, máximo +0.72% |
| Horas con \|prima\| > 0.5% / > 1% | **1.3% / 0.1%** | 62.7% de las horas con prima positiva |
| Persistencia AR(1) horaria | rho **0.214**, vida media **0.4 h** (n = 1,442) | `corrcoef`: 0.21, 0.44 h |
| Cambio de la prima contra ΔUSD/MXN y ΔBTC en la hora | **b_fx −0.30 (t −6.0)**, b_btc −0.04 (t −3.0), R² 0.03 | — |
| "Beta de presión" diaria: prima contra el rendimiento de 7 días de BTCUSDT | pendiente **+0.0045**, correlación +0.32 (78 días) | Paper: 0.078 contra la desviación HP (otro regresor) |

**Foto de hoy (14:3x UTC).** Implícito: 84,102.00 × 18.6130 = 1,565,391 MXN.

| Libro | Compra (vs. implícito) | Venta | Diferencial | Compra a −0.5% del implícito |
|---|---|---|---|---|
| Binance BTCMXN | 1,560,423 (−0.32%) | 1,566,656 (+0.08%) | 0.399% | 39,770 MXN |
| Bitso btc_mxn (plan B) | 1,563,440 (−0.12%) | 1,564,770 (−0.04%) | **0.085%** | **1,126,901 MXN** |

Una venta a mercado de los 0.001325 BTC de la cuenta en Binance daría 2,068 MXN contra 2,074 al implícito: **−0.32%**, más 0.1% de comisión.

**Lectura.**

1. **La prima mexicana de 2017-18 desapareció en el par de Binance:** pasó de 2.7% (Bitso, en el paper) a +0.03%. Una prima de 2.7% hoy estaría 15 desviaciones estándar horarias arriba de la media. Es lo que el paper anticipó: con USDT como puente, los controles de capital ya no amarran el arbitraje. México además no tiene controles relevantes.
2. **La beta de presión casi desapareció.** Una semana de +10% en BTC sube la prima ~0.045 pp. Con la beta del paper serían ~0.8 pp, aunque el regresor es distinto. Grado B en la comparación.
3. **Las desviaciones se cierran en minutos:** la vida media es de 0.4 h. Lo que la señal E9 ve como "diferencial > 0.5%" es casi siempre un libro delgado entre arbitrajes, no un precio mal puesto.
4. **El rezago del libro en pesos es real pero parcial.** Cuando el USD/MXN sube 1% en una hora, la prima en esa hora baja 0.30 pp: el libro en pesos absorbe ~70% del movimiento en la misma hora. Hoy, con el peso 0.8% más débil, eso explica unos −0.25 pp en la compra. Coincide con la hipótesis del pulso de las 04:17.

## 4. Qué cambia para invertir [I/O]

- **E9 debe medirse contra el precio implícito, no contra el punto medio.** Esto respalda la propuesta que ya está con el gestor de riesgo. Con la distribución de 90 días, un umbral ÁMBAR de **compra < −1.0% del implícito** saltaría en ~0.1% de las horas según la prima de cierre (con la de compra serán más; hay que medirla una semana) y separa "libro delgado" de "precio roto". La ROJA sigue siendo "libro vacío o par suspendido". [O]
- **Salida de la posición (si el filtro la manda): orden límite en BTCMXN al implícito −0.3%,** con hasta 1 h para llenarse (vida media de 0.4 h). Si no se llena, se pasa a BTC/USDT y luego USDT/MXN, o a Bitso. Con ~2,000 MXN el costo de la ruta lenta no cambia el resultado. [O]
- **Plan B (Bitso):** hoy su libro en pesos tiene diferencial de 0.085% y ~28 veces más profundidad a −0.5%. Es un argumento operativo a favor de tenerlo probado (punto del comité del 9-oct) y no un cambio de exchange: el riesgo de contraparte es otro tema. [I]
- **No hay estrategia de arbitraje para la cuenta.** Con 0.1% de comisión por lado y una dispersión p5-p95 de ±0.25%, no queda nada después de costos, igual que en los costos de 50-75 pb del paper. [I]

## 5. Contrapuntos y límites

- **El cierre de la vela es la última operación, no el bid/ask.** Con ~1 BTC/día puede tener minutos de antigüedad dentro de la hora: eso agranda la dispersión y baja la rho. La prima "de ejecución" (compra contra implícito) es peor que la prima de cierre. La foto de hoy da −0.32% en la compra contra +0.03% en la prima media.
- **USDT no es USD:** con Kraken USDT/USD en 0.9988, la prima contra el dólar sale ~0.1 pp más alta. Yahoo MXN=X es un precio indicativo, no el FIX de Banxico.
- **90 días sin estrés:** no incluye un evento de cola en México ni en Binance. En una corrida, el libro en pesos es justo lo que se vacía primero (ROJA de E9).
- **Regresor distinto al del paper** (rendimiento de 7 días contra desviación HP semanal): la comparación de betas es de orden de magnitud, no punto a punto.
- **El paper es de 2017-18,** cuando no había ETF ni stablecoins dominantes. Su mensaje sobre controles de capital se aplica a Corea o Argentina, no a MXN en 2026.

## 6. Autoexamen

1. ¿Por qué las primas entre países eran más grandes que dentro de un país, según Makarov-Schoar? → Controles de capital y capital de arbitraje "atrapado"; los costos de transacción (50-75 pb) no alcanzan a explicarlas.
2. ¿Cuál era la prima de México en la tabla 5? → 2.7%, con beta de 0.078.
3. ¿Cuál es hoy la vida media de la prima horaria de BTCMXN en Binance? → ~0.4 h (rho 0.21).
4. Si el USD/MXN sube 1% en una hora, ¿qué pasa con la prima? → Baja ~0.30 pp en esa hora (el libro en pesos se rezaga ~30%).
5. ¿Por qué E9 debe medirse contra el implícito? → Porque el punto medio de un libro delgado se mueve con una sola postura. El riesgo para la cuenta es cuánto se pierde al vender contra el precio justo.

## 7. Estado

- **Documentado con comprobación.** Grado A en el paper (versión aceptada) y en los datos; B en la comparación de betas; C en la causa de cada episodio de E9.
- **Siguiente paso:** Griffin-Shams (JF 2020) sobre Tether y manipulación; atención (Google Trends, §4.2 de Liu-Tsyvinski); repetir la réplica con bid/ask y no con cierres (`depth` cada hora, una semana).
- **Pronóstico ligado:** ninguno sobre la prima, porque sería un pronóstico de microestructura sin utilidad para decidir. El de hoy es P0160 (acciones de IBIT).
