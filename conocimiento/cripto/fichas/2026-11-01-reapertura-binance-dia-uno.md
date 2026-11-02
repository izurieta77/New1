# Ficha de avance · 1-nov-2026 · Reapertura de Binance, día uno: velocidad de salida, BNB/BTC y precio interno

> **Por qué este tema.** La cola académica del plan (`00-plan-de-estudio.md`, fila de literatura) sigue esperando datos: la prima electoral necesita los diarios del 3-4-nov y la ventana *c* del IVD llega hacia el 2-dic. Hoy, en cambio, hay un dato que no se repite: el primer día de reapertura de un exchange top-1 después del mayor hackeo registrado. La ficha del 31-oct dejó tres pasos pendientes: (a) medir el precio de Binance contra el mercado externo en la hora de la reapertura; (b) medir el perfil de E1 en la semana de la reapertura; y vigilar BNB/BTC (P0217). Esta ficha mide esas tres cosas con la fila intradía de DefiLlama de las 13:29 UTC, unas 7.5 h después de que abrió la fase uno, y las compara con Bitget (sep-2026). Es una continuación del cap. 04, nivel Doctorado (eventos de cola), con uso operativo inmediato: el MXN del dueño sigue atrapado y E1 está por cruzar a ROJA.

## 0. Preguntas de hoy

1. ¿Qué tan rápido reabrió Binance, comparado con Bitget?
2. ¿Cuánto salió en las primeras horas, y a qué ritmo por hora comparado con Bitget?
3. ¿Qué va a marcar E1 formal en la fila del 2-nov?
4. ¿BNB/BTC repite el patrón de BGB/BTC (se recupera en la pausa y vuelve a ceder al reabrir)?
5. ¿El BTC de Binance se abarató o se encareció al reabrir?

## 1. Acceso y fuentes (declarado)

| Dato | Fuente | Grado | Acceso real |
|---|---|---|---|
| Activos con retiro abierto (990 en total) y parámetros por red | [getNetworkCoinAll](https://www.binance.com/bapi/capital/v1/public/capital/getNetworkCoinAll): consultas de las bitácoras del 31-oct y el 1-nov, más la de esta corrida (14:20 UTC) | **A** | Íntegro |
| Fase uno de 06:00 a 09:00 UTC con 17 redes; ≈95% de lo robado cubierto; Lightning y fiat fuera de la fase uno; fases siguientes por X | [Recovery Update #4](https://www.binance.com/bapi/composite/v1/public/cms/article/detail/query?articleCode=73911fb819b240f88b88256bdd318eda), 04:08:56 UTC, versión 1 (sin edición a las 14:2x UTC [Conciliación 2-nov-2026 03:05 UTC, `bitacora/arbitraje/2026-11-01.md` M1: hora vaga, la exacta no es verificable; cota del commit `7676860`: antes de 14:28 UTC]) | **A** | Íntegro |
| Tenencias por token en las carteras atribuidas a Binance: filas de 00:00 UTC del 25, 26, 29, 30 y 31-oct y del 1-nov, y la fila intradía de las **13:29:11 UTC del 1-nov** | [api.llama.fi/protocol/binance-cex](https://api.llama.fi/protocol/binance-cex), descargado a las 14:20 UTC | **C** (atribución de carteras) | Íntegro; 45 cadenas en las dos filas del 1-nov, ninguna falta |
| Flujos de Bitget (sep-2026) | Foto DefiLlama de la ficha del 30-oct (`2026-10-30-hackeos-exchanges-datos.json`) | **C** | Íntegro |
| Velas de 1 h de BTCUSDT y BNBUSDT (Binance), BTC-USD (Coinbase) y USDT/USD (Kraken), del 27-oct 00:00 al 1-nov 13:00 UTC | data-api.binance.vision, api.exchange.coinbase.com y api.kraken.com | **A** como dato de precio | Íntegro |
| Prensa del día: Reuters (05:49 UTC), CoinDesk (10:40), WSJ (12:03), BBC (13:11), Forbes (12:56) | Titulares en Google News | **B** | Solo titulares; no cambian ninguna cifra |

**Hora del choque.** Uso la misma inferencia que la ficha del 31-oct: la vela de 1 h con la mayor caída de BNB abre a las 20:00 UTC del 29-oct, y la alerta del 30-oct da "≈21:50 UTC" para la pausa [I].

## 2. Ejercicio numérico (comprobado en Python)

Código: [`2026-11-01-reapertura-binance-dia-uno.py`](2026-11-01-reapertura-binance-dia-uno.py) (solo biblioteca estándar). Corre con `python3 -I conocimiento/cripto/fichas/2026-11-01-reapertura-binance-dia-uno.py`, que lee la foto [`2026-11-01-reapertura-binance-datos.json`](2026-11-01-reapertura-binance-datos.json); con `--crudo <dir>`, la rehace desde los JSON de las APIs. Termina con `OK: todas las comprobaciones pasan` (12 `assert` que sostienen el texto). Una de mis hipótesis previas resultó falsa: suponía que Binance perdía más rápido por hora que Bitget, y el `assert` se corrigió para reflejar el dato (§B).

### A. Calendario: Binance reabrió BTC antes que Bitget

| Hora UTC | Activos con retiro abierto |
|---|---|
| 31-oct 14:20 · 1-nov 02:59 | 0/990 |
| 1-nov 06:18 | 1 (BTC por la red BTC) |
| 10:19 | 7 |
| 11:42 | 13 |
| 13:08 · 14:20 | 15 (ARB, AVAX, BNB, BTC, DOGE, ETH, GRAM, POL, SOL, SUI, TRX, USDC, USDT, XRP y ZEC) |

- **Pausa hasta el primer BTC:** Bitget, 84 h. Binance, **≤56.5 h**: es una cota superior, porque las 06:18 son la primera consulta y no la hora de apertura.
- Siguen cerrados **BTC/LIGHTNING** y **MXN/FIAT_MONEY** (SPEI). BTC por la red BTC: comisión 0.00002 BTC, mínimo 0.0001 y máximo 1,286 BTC.
- Hay 704 activos con depósito abierto.

### B. Velocidad de salida: grande en dólares y más lenta por hora que Bitget

Método F (DefiLlama, sin BNB): Σ (u_t − u_t0) × p_t, en % de Σ u_t0 × p_t.

| Ventana | Flujo (mil M USD) | % |
|---|---|---|
| Último día de pausa (31-oct 00:00 → 1-nov 00:00) | +0.003 | +0.00 |
| **Día uno, 1-nov 00:00 → 13:29 UTC (≈7.5 h de reapertura)** | **−3.75** | **−2.78** |
| Bitget, primer día (fila del 29-sep, 16 h de reapertura) | −0.46 | −7.88 |

- **Por token:** USDT −1.74 mil M, BTC −1.06, USDC −0.60, WETH −0.20 y GRAM −0.05. Las stablecoins son el 62% de la salida.
- **BTC en carteras:** 645,048 → 631,450, es decir, **−13,597 BTC (−2.11%)** en 7.5 h.
- **Ritmo por hora de reapertura:** Binance **−0.37%/h** y Bitget −0.49%/h, o 0.8 veces el de Bitget. En dólares, Binance pierde ≈US$0.5 mil M por hora, unas 17 veces lo de Bitget (≈US$0.03 mil M por hora), porque su base es unas 23 veces más grande (US$135 mil M contra ≈US$5.8 mil M).
- Lo que sale es sobre todo lo que se puede mover hoy: el 62% son stablecoins, y USDT y USDC abrieron en varias redes. Del BTC sale la mitad que de USDT, en dólares.

**E1 formal y lo que viene:**
- La fila de hoy (1-nov 00:00 contra 25-oct 00:00) da **−4.74%: ÁMBAR**. Casi todo es el robo del 29-30-oct; durante la pausa no hubo flujo.
- **Si no saliera nada más después de las 13:29, la fila de mañana (2-nov 00:00 contra 26-oct 00:00) ya daría −7.09%: ROJA** (umbral −5.3%, percentil 1). Lo más probable es que la salida siga hasta medianoche, así que **E1 marcará ROJA en la fila del 2-nov**, salvo que entren fondos de reposición o haya una reasignación de carteras.
- **E2:** lo rastreado pasa de US$160.5 mil M a US$157.5 mil M; **BNB 16.6%: VERDE**. El BTC en carteras va −3.3% contra el 25-oct (ÁMBAR en −5%): VERDE, pero se acerca.

### C. BNB/BTC no repite a BGB: se recupera al reabrir

Razón BNBUSDT/BTCUSDT; base: el cierre de la vela de las 19:00 UTC del 29-oct (0.0092134).

| Momento | Razón | Δ |
|---|---|---|
| Choque +1 h | 0.0088520 | −3.92% |
| Pausa, 31-oct 00:00 | 0.0091377 | −0.82% |
| Vela de las 05:00 del 1-nov (antes de abrir) | 0.0090528 | −1.74% |
| Vela de las 06:00 (abre) | 0.0090525 | **−1.75%** (el mínimo tras abrir) |
| Vela de las 13:00 (última completa) | 0.0091678 | **−0.50%** |

- En Bitget, el token llegó a ~0% al reabrir y luego cedió −2.8% en 7 días.
- En Binance pasó lo contrario: el token cedió en la víspera, cuando la reapertura aún era promesa, y **repuntó 1.25 puntos en las primeras 7 horas** con la reapertura cumplida.
- A las 14:20 UTC, la razón era 715.96 / 78,091.49 = **−0.49%**. El umbral de P0217 (0.0089370, −3%) queda a 2.5 puntos.
- Una lectura posible [I]: con la reapertura cumplida, el mercado le cobra a BNB menos riesgo de solvencia, aunque los clientes sigan saliendo (§B). **El token propio y el flujo se separaron:** BNB/BTC no está midiendo la cola de retiros, sino la duda de solvencia.

### D. Precio interno: la prima de la pausa se achica al reabrir

Binance BTCUSDT × USDT/USD de Kraken contra Coinbase BTC-USD, cierres de 1 h, en puntos base:

| Tramo | n | Mediana | Mín. | Máx. |
|---|---|---|---|---|
| Antes del choque (27-oct 00:00 → 29-oct 20:00) | 68 | +1.3 | −1.4 | +3.3 |
| **Pausa** (29-oct 20:00 → 1-nov 06:00) | 58 | **+8.1** | +1.2 | +14.7 |
| **Reabierto** (1-nov 06:00 → 13:00) | 8 | **+6.3** | +5.0 | +11.3 |

- Durante la pausa, el BTC de Binance cotizó con **prima**, no con descuento: es el mismo resultado de Bitget, ahora con n = 2.
- Al reabrir, la prima se achica (de +11 pb en la vela de las 06:00 a +5 pb a las 13:00) en vez de abrirse un descuento.
- Foto de las 14:20 UTC:
  - Binance × USDT/USD (0.99865) contra el índice de Deribit (77,984.67): **+0.2 pb**;
  - BTCMXN medio (1,469,137.5) contra Bitso (1,466,725): **+16 pb**.
- Para el dueño, salir en especie no le cuesta nada en precio. El costo es solo la comisión de la red.

## 3. Lectura para la decisión [I]

1. **La corrida existe, pero es ordenada:** −2.78% en 7.5 h, menos por hora que Bitget, sin descuento en el BTC interno y con el token propio al alza. No es la firma de una duda de solvencia (FTX: token −80% y descuento). Es la cola de retiros que la ficha del 30-oct ya esperaba.
2. **E1 cruzará a ROJA mañana**, casi seguro. Eso no agrega un disparador nuevo: la contingencia ya está cumplida desde el 31-oct ("retiros suspendidos más de 24 h"), y la respuesta que rige es la regla W44 ("retirar, no vender, no depositar"). Lo que cambia es que **el MXN es el único saldo del dueño que no tiene salida**, y queda en el exchange que más pierde clientes esta semana.
3. **El MXN (≈3,001.83).** Bitget abrió el fiat 4 días después del BTC; si Binance sigue el mismo orden, sería hacia el 5-nov. La ruta "convertir a BTC y retirar por la red BTC" existe hoy:
   - costo: ≈0.1% de comisión + 0.03% de medio diferencial + 0.00002 BTC (≈29 MXN, ≈1%), en total ≈1.1%, unos 34 MXN;
   - no es enajenación al comprar; sí lo será al vender en Bitso;
   - pero sube la exposición cripto del dueño: es una **decisión de cartera** (punto (3) del decisor) y no la tomo yo. La dejo en `decisiones-pendientes.md` con estas cifras.
4. **El BTC real (0.001325)** sigue con la ruta de la red BTC abierta. La propuesta de retirarlo (alerta del 1-nov 06:18 UTC) sigue sin confirmación del dueño.

## 4. Límites

- **La fila intradía de DefiLlama no es una fila de cierre:** puede cambiar, y la API la sustituye por la de 00:00 del día siguiente. Las 45 cadenas están presentes, pero la hora de lectura de cada cadena no se ve.
- **DefiLlama solo ve las carteras atribuidas (C).** Si Binance mueve fondos a carteras nuevas (reposición, reorganización tras el hackeo), aparecen como salida o entrada falsas. El robo de 6.3 mil M ya cae dentro de la ventana de E1 de la fila del 1-nov.
- **El ritmo por hora supone que la salida empezó a las 06:00.** La fase uno abrió activos de forma progresiva entre las 06:00 y las 13:08, así que el ritmo efectivo por activo abierto fue mayor. En Bitget, la fila del 29-sep también mezcla horas.
- **n = 2** (Bitget y Binance) para la prima de la pausa y para el token propio. Las conclusiones de §C son de una sola mañana.
- Coinbase y Kraken son la referencia externa; no se midió la prima contra Bitso por hora (no hay velas públicas de Bitso en la vía usada).

## 5. Estado

**Documentado con comprobación.** Siguientes pasos:
- (a) leer la fila de 00:00 UTC del 2-nov (E1 formal; se espera ROJA) y la del 3-nov, para medir si la cola dura 24-36 h, como en Bitget y Bybit;
- (b) P0219: la fecha de reapertura del MXN/SPEI;
- (c) P0217 y P0207 siguen abiertos; con lo de hoy, P0217 se ve menos probable y P0207, más;
- (d) cruzar con la prueba zk de PoR prometida para el 3-nov (E3).
