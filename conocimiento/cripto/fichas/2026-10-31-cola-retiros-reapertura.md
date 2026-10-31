# Ficha de avance · 31-oct-2026 · La cola de retiros y el precio al reabrir (Bitget 2026, Bybit 2025) y la ruta Lightning/SPEI a Bitso

> **Por qué este tema y no el siguiente de la cola.** La cola académica del plan (`00-plan-de-estudio.md`, fila de literatura) sigue sin datos: la prima electoral necesita los diarios del 3-4-nov y la ventana *c* del IVD llega hacia el 2-dic. El estudio de eventos con el EPU diario no sirve para la decisión de mañana. Lo que sí sirve es esto: el Update #2 de Binance anuncia la reanudación por fases hacia las **05:33 UTC del 1-nov**, y la regla W44 dice "retirar, no vender, no depositar". La ficha del 30-oct midió **cuánto** se va el cliente al reabrir (Bitget −10.2% en 3 días, Bybit −27.0% en 2). Hoy se mide **cómo**: si se abre un descuento del BTC dentro del exchange pausado, dónde se ve el estrés, qué tan concentrada en el tiempo está la cola, y qué cuesta cada ruta de salida para nuestros saldos. Es un tema complementario del cap. 04, nivel Doctorado (eventos de cola), con aplicación operativa inmediata.

## 0. Preguntas de hoy

1. Mientras los retiros están cerrados, ¿el BTC dentro del exchange cotiza con descuento frente al mercado externo? ¿Y al reabrir?
2. Si no se ve en el BTC, ¿dónde se ve el estrés del exchange?
3. ¿Qué tan concentrada en el tiempo está la cola de retiros al reabrir?
4. Para 0.001325 BTC y 3,001.83 MXN (real) y 0.002698 BTC (papel), ¿qué cuesta y qué límites tiene cada ruta: Lightning, red BTC o vender + SPEI?

## 1. Acceso y fuentes (declarado)

| Dato | Fuente | Grado | Acceso real |
|---|---|---|---|
| Velas de 1 h de Bitget BTCUSDT y BGBUSDT, 19-sep a 5-oct-2026 | [Bitget API v2 `history-candles`](https://api.bitget.com/api/v2/spot/market/history-candles?symbol=BTCUSDT&granularity=1h&limit=200) | **A** como dato de precio | Íntegro (400 velas por par) |
| Velas de 1 h de Binance BTCUSDT (sep y oct-2026) y BNBUSDT (22 al 31-oct) | [data-api.binance.vision klines](https://data-api.binance.vision/api/v3/klines?symbol=BNBUSDT&interval=1h&limit=1000) | **A** | Íntegro |
| Flujos diarios de Bitget y Bybit (método F) | Foto DefiLlama de la ficha del 30-oct (`2026-10-30-hackeos-exchanges-datos.json`) | **C** (atribución de carteras) | Íntegro |
| Reapertura de Bitget por fases: BTC el 28-sep a las 08:00 UTC, ETH el 29, USDT el 30 y fiat/P2P el 2-oct | BleepingComputer y crypto.news (ficha del 30-oct) | **B** | Resúmenes |
| Parámetros de retiro de Binance: Lightning (comisión 0.000001 BTC, mínimo 0.00002, **máximo 0.01 BTC por retiro**; no acepta facturas con *feature bits* no estándar), red BTC (comisión 0.00002, mínimo 0.0001) y MXN/FIAT_MONEY (comisión 0) | [getNetworkCoinAll](https://www.binance.com/bapi/capital/v1/public/capital/getNetworkCoinAll), 31-oct 14:20 UTC | **A** | Íntegro; hoy todos con `withdrawEnable=false` |
| Bitso recibe por Lightning: factura con monto, mínimo 0.00000001 BTC, llega "almost immediately", las facturas caducan y no se reutilizan, no es intercambiable con la red BTC; "transaction limits can vary depending on network conditions" | [Bitso, How to receive Bitcoin using the Lightning Network](https://support.bitso.com/hc/en-us/articles/52653682361492-How-to-receive-Bitcoin-using-the-Lightning-Network-on-Bitso) y [What is the Lightning Network](https://support.bitso.com/hc/en-us/articles/32048877697172-What-is-the-Lightning-Network-for-Bitcoin) (ambas actualizadas el 28-oct-2026), leídas con la API pública de Zendesk | **A** (documento de la empresa) | Íntegro. **No publica un máximo por depósito.** |
| SPEI opera 24/7; desde dic-2017 los bancos deben liquidar en tiempo real los SPEI de menos de 8,000 MXN a toda hora | [Expansión, 6-dic-2017](https://expansion.mx/economia/2017/12/06/las-transacciones-interbancarias-estaran-disponibles-todo-el-dia-todos-los-dias) | **B** (prensa; la regla vigente de Banxico no se leyó) | Resumen |
| Foto de hoy: Binance BTCUSDT 77,487.18; Kraken USDT/USD 0.99885; índice Deribit 77,345.63; BTCMXN de Binance 1,456,220 / 1,457,247 (6 muestras idénticas, 14:20:39-14:22:23 UTC); Bitso 1,454,960 / 1,454,970 | APIs públicas de cada venue | **A** | Íntegro |

**Hora del choque.** Ni Bitget ni Binance dan la hora exacta en una fuente que yo haya leído. Uso la vela de 1 h con la mayor caída del token propio: BGB −5.36% en la vela que abre a las 20:00 UTC del 24-sep-2026 y BNB −6.29% en la que abre a las 20:00 UTC del 29-oct-2026 (consistente con los "≈21:50 UTC" de la alerta del 30-oct). Es una inferencia [I].

## 2. Ejercicio numérico (comprobado en Python)

Código: [`2026-10-31-cola-retiros-reapertura.py`](2026-10-31-cola-retiros-reapertura.py) (solo biblioteca estándar). Corre con `python3 -I conocimiento/cripto/fichas/2026-10-31-cola-retiros-reapertura.py`, que lee la foto [`2026-10-31-cola-retiros-datos.json`](2026-10-31-cola-retiros-datos.json); con `--crudo <dir>` la rehace desde los JSON de las APIs. Termina con `OK: todas las comprobaciones pasan` (seis `assert` que sostienen el texto).

### A. El BTC dentro del exchange pausado no se abarata

Bitget BTCUSDT contra Binance BTCUSDT, cierres de 1 h, en puntos base (pb):

| Tramo | n | Mediana | p5 | p95 | Máx. \|x\| |
|---|---|---|---|---|---|
| 5 días antes del choque | 120 | +0.10 | −0.66 | +1.24 | 2.0 |
| **Pausa** (24-sep 20:00 → 28-sep 08:00 UTC) | 84 | **+0.62** | −0.97 | +2.39 | 5.6 (prima, a las 07:00 del 28-sep) |
| 5 días tras reabrir BTC | 120 | +0.17 | −0.96 | +1.69 | 3.8 |

**Binance hoy, con 0/990 retiros:** BTCUSDT × USDT/USD de Kraken contra el índice de Deribit da **+6.8 pb**; el BTCMXN medio contra el de Bitso, **+12.2 pb**. No hay descuento: hay una prima mínima.

**Por qué [I].** Con los retiros cerrados, el BTC y el USDT (o el MXN) del cliente quedan atrapados juntos, así que el precio *relativo* entre ellos lo siguen arbitrando los creadores de mercado que tienen inventario en varios venues y cubren sin mover fondos. Los depósitos siguieron abiertos (706 activos en Binance), y eso pone un techo a cualquier prima, no un piso a un descuento. El descuento de un saldo atrapado solo aparece cuando una pata sale y la otra no (el caso Mt.Gox de 2014, con el fiat atrapado) o cuando el mercado duda de la solvencia; ninguna de las dos cosas pasó aquí.

### B. El estrés se ve en el token propio

Razón token/BTC; base: cierre de la vela previa al choque.

| | +1 h | +24 h | Reapertura | Reapertura +72 h | Reapertura +7 d |
|---|---|---|---|---|---|
| **BGB/BTC** (Bitget) | **−5.31%** | −1.74% | +0.01% | −1.84% | **−2.80%** |
| **BNB/BTC** (Binance) | **−3.92%** | −1.16% | hoy 14:00 UTC, ~42 h de pausa: **−1.45%** | — | — |

En Bitget, el token se recuperó entero durante la pausa y volvió a ceder casi 3% en la semana de la cola. BNB va por el mismo camino hasta ahora. De ahí sale **P0217**.

### C. La cola se concentra en el primer día

Flujo diario sin token propio (método F; la fila *d* es el flujo de *d−1* a *d*; se le suma de vuelta el robo el día del robo):

| Bitget | mil M USD | | Bybit | mil M USD |
|---|---|---|---|---|
| 25-sep (robo) | +0.03 | | 21-feb | −0.03 |
| 26 a 28-sep (pausa) | +0.00 a +0.01 | | **22-feb** (robo; ~10 h después del hackeo) | **−1.09** |
| **29-sep** (28-sep: reabre BTC) | **−0.46** | | **23-feb** | **−3.28** |
| 30-sep (abre ETH) | +0.04 | | 24-feb | +0.21 |
| 1-oct (abre USDT) | −0.19 | | 25-feb | +1.08 (reposición) |
| 2-oct (abre fiat) | +0.59 (reposición) | | | |

- **Bitget: 71% de la salida de los tres primeros días ocurrió el día uno** (−0.46 mil M, igual a los US$463 M en 24 h de Bloomberg, B). Lo demás llegó cuando abrió el USDT.
- **Bybit, que no pausó: 100% de la salida cayó en las primeras ~34 h** (25% en la fila del 22 y 75% en la del 23). Al tercer día ya había entradas.
- La cola es un pulso de 24-36 h, no un goteo. Para un saldo chico la cola no es de *monto*, sino de *proceso*: tiempos de revisión, límites del nodo Lightning y fallas de interfaz en el pico.

### D. La ruta para nuestros saldos

| Saldo | En MXN (BTCMXN medio de hoy) | Lightning | Red BTC | Vender en BTCMXN + SPEI |
|---|---|---|---|---|
| Real, 0.001325 BTC | ≈ 1,930 | **0.075%**, una factura (máx. 0.01 BTC) | 1.51% | ≈ 0.135% (0.1% + medio diferencial), y además es enajenación |
| Papel, 0.002698 BTC | ≈ 3,930 | **0.037%**, una factura | 0.74% | ≈ 0.135% |
| Real, 3,001.83 MXN | — | — | — | SPEI con comisión 0 en el endpoint, por debajo de los 8,000 MXN del SPEI en tiempo real 24/7 (B) |

Lightning cuesta 20 veces menos que la red BTC para el saldo real, no realiza la ganancia o pérdida fiscal y llega en segundos. La red BTC queda de respaldo si falla el pago Lightning. El costo de ese respaldo, 1.51% (≈29 MXN), es más bajo que un día de exposición al riesgo de contraparte con cuatro ROJAS.

## 3. Lectura para la decisión de mañana [I]

1. **No hay razón de precio para vender dentro de Binance antes de salir.** El BTC interno cotiza a +7 pb del mercado (+12 pb en pesos). La regla W44 ("retirar, no vender") no le cuesta nada al precio.
2. **El orden probable de la reapertura es BTC primero y fiat al final** (Bitget: BTC al día 4, ETH al 5, USDT al 6 y fiat al 8). Lo más probable es que mañana se abra la rama "abre BTC → retirar en especie a Bitso en la primera hora" y que los **3,001.83 MXN se queden atrapados unos días más**. Convertirlos a BTC para sacarlos por Lightning subiría la exposición cripto y es una decisión de cartera: **no la tomo yo**. Queda como pregunta al decisor en `bitacora/decisiones-pendientes.md`.
3. **La primera hora importa por proceso, no por monto.** En Bitget, 71% de la salida de tres días ocurrió en las primeras ~16 h de reapertura. Lo práctico: (a) generar la factura de Bitso **en el momento** de retirar, porque caducan y no se reutilizan; (b) si Binance rechaza la factura ("non-standard feature bits") o el pago falla dos veces, usar la red BTC (mínimo 0.0001 BTC, comisión 0.00002); (c) no cambiar contraseñas ni 2FA (Bitso bloquea retiros 24 h después de un cambio, regla W44).
4. **Lo que sigue sin probarse:** que el dueño tenga Bitso en nivel ≥2 con CLABE, y que una factura de Bitso (Lightspark) sea compatible con el retiro Lightning de Binance. La prueba de 0.00002 BTC que planteó el doc. 10 de arena no consta como hecha. Si falla, el respaldo es la red BTC.
5. **Señal de contraparte para la semana:** BNB/BTC (−1.45% hoy). En el análogo de Bitget, el token cedió −2.8% a 7 días de reabrir. Si BNB/BTC pasa de −3% (P0217), el mercado está cobrando la cola de retiros o una duda sobre la PoR del lunes.

## 4. Límites

- **n = 1 para la pausa** (Bitget) y n = 1 sin pausa (Bybit). Las velas de Bybit no se pudieron bajar desde aquí (CloudFront bloquea el país), así que para Bybit solo hay flujos, no precio interno.
- La comparación es contra Binance, que era el venue sano en septiembre. Hoy es el venue pausado, y por eso la comparación de hoy va contra Deribit y Bitso.
- La hora del choque se infiere del token propio, no de un comunicado.
- DefiLlama ve solo carteras atribuidas (C) y da filas diarias; el reparto por hora de la cola no se puede medir con esta fuente.
- Bitso no publica un máximo por depósito Lightning, y la capacidad del nodo Lightning de Binance en el pico de reapertura no es observable. Para 0.0013-0.0027 BTC el riesgo es bajo, pero no es cero.
- El SPEI 24/7 con el tope de 8,000 MXN viene de prensa de 2017 (B); la regla vigente de Banxico no se leyó.

## 5. Estado

**Documentado con comprobación.** Siguientes pasos:
- (a) medir el mismo diferencial (Binance contra Deribit y Bitso) en la hora de la reapertura y a +24 h;
- (b) medir el perfil diario de E1 de Binance en la semana de la reapertura (P0207) y BNB/BTC (P0217);
- (c) cuando haya una vía, bajar velas de Bybit (feb-2025) y del token MNT para tener n = 2 en precio;
- (d) leer la norma vigente de Banxico sobre el horario del SPEI.
