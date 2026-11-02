# Ficha de avance · 2-nov-2026 · Reapertura de Binance, día dos: E1 oficial, forma de la cola y cierres por "hot wallet"

> **Por qué este tema.** Los 35 recursos del dueño están en `estudiado` (`recursos/indice.csv`), así que el plan (`00-plan-de-estudio.md`) manda avanzar la fila abierta del nivel más bajo sin terminar. Es la del cap. 04 (Doctorado, eventos de cola), con su siguiente paso escrito en `estado-de-dominio.csv`, fila del 1-nov: "Fila de 00:00 UTC del 2-nov y del 3-nov (E1 formal y duración de la cola)". La cola académica (prima electoral, IVD ventana *c*) sigue esperando datos del 3-4-nov y del 2-dic. Además, la cifra oficial de E1 la pidió el orquestador (`decisiones-pendientes.md`, 2-nov 02:15 UTC). Corrida de las 08:17 CDMX, **disparada tarde**: programada a las 14:17 UTC, empezó a las 15:22 UTC; las consultas son de 15:23 a 15:25 UTC.

## 0. Preguntas de hoy

1. ¿Qué marca E1 oficial (método F) en la fila del 2-nov?
2. ¿La salida se frena el día dos, como en Bitget, o empeora, como en Bybit?
3. ¿Qué sale el día dos? ¿Siguen siendo stablecoins? ¿Cuánto BTC?
4. ¿Qué dicen los cierres intermitentes de pares ("replenishes the hot wallet") sobre las reservas en caliente?
5. ¿Cómo va BNB/BTC frente al umbral de P0217?

## 1. Acceso y fuentes (declarado)

| Dato | Fuente | Grado | Acceso real |
|---|---|---|---|
| Tenencias por token en las carteras atribuidas a Binance: filas de 00:00 UTC del 25, 26 y 27-oct y del 1 y 2-nov, y la fila intradía de las **14:08:59 UTC del 2-nov** | [api.llama.fi/protocol/binance-cex](https://api.llama.fi/protocol/binance-cex), descargado a las 15:23 UTC | **C** (atribución de carteras) | Íntegro. La agregada `OwnTokens` se excluye para no duplicar el BNB, y E1 da lo mismo con o sin ella. |
| Estado de retiro y motivo de cierre de cada red (991 activos) | [getNetworkCoinAll](https://www.binance.com/bapi/capital/v1/public/capital/getNetworkCoinAll), 15:23 UTC; las horas anteriores salen de las bitácoras del 1 y 2-nov | **A** | Íntegro (campo `withdrawDesc`) |
| Recovery Update #5 (zk de la foto PoR del 31-oct; siguiente fase de retiros "planned for tomorrow"; otra foto el 4-nov; ≈95% cubierto) | [CMS `185bd9a4717f44088b3be70287b8237f`](https://www.binance.com/bapi/composite/v1/public/cms/article/detail/query?articleCode=185bd9a4717f44088b3be70287b8237f), leído a las 15:24 UTC; no hay Update #6 en el catálogo 49 | **A** | Íntegro |
| Bitget (sep-2026) y Bybit (feb-2025) | Foto DefiLlama de la ficha del 30-oct (`2026-10-30-hackeos-exchanges-datos.json`) | **C** | Íntegro |
| BNBBTC y BTCUSDT | data-api.binance.vision `ticker/24hr`, 15:23:54 UTC | **A** como dato | Íntegro |

## 2. Ejercicio numérico (comprobado en Python)

Código: [`2026-11-02-reapertura-binance-dia-dos.py`](2026-11-02-reapertura-binance-dia-dos.py) (solo biblioteca estándar). Se corre con `python3 -I conocimiento/cripto/fichas/2026-11-02-reapertura-binance-dia-dos.py`, que lee la foto [`2026-11-02-reapertura-binance-datos.json`](2026-11-02-reapertura-binance-datos.json); con `--crudo <dir>` la rehace desde los JSON de las APIs. Termina con `OK: todas las comprobaciones pasan` (11 `assert`). E1 se cruzó además con la réplica oficial `bitacora/arbitraje/2026-10-25-e1-metodo-f.py`, que da la misma cifra: −8.78%.

### A. E1 oficial: −8.78%, ROJA

| Fila (método F, sin BNB, 00:00 UTC) | Flujo (mil M USD) | % | Color |
|---|---|---|---|
| 31-oct contra 24-oct | −6.98 | −4.93 | ÁMBAR |
| 1-nov contra 25-oct | −6.70 | −4.74 | ÁMBAR |
| **2-nov contra 26-oct** | **−12.41** | **−8.78** | **ROJA** (< −5.3%, percentil 1) |
| Proyección de la fila del 3-nov si no saliera nada después de las 14:09 (14:09 contra 27-oct) | −14.10 | −9.98 | ROJA |

- La aproximación del vigía (−8.73%) se queda a 0.05 puntos de la cifra oficial; la diferencia viene de la hora de su fila (23:29 contra 00:00).
- **Es la fila n.º 6 de 1,441 ventanas de 7 días desde nov-2022.** Las cinco peores son todas del 16 al 20-dic-2022, la corrida tras FTX y Mazars (−9.51% a −13.73%). **Ninguna semana fuera de dic-2022 fue peor.** La serie de hoy da −13.73% para el 18-dic-2022, y §F daba −13.49%: DefiLlama revisa su historia.
- Cerca de la mitad es el robo: US$6.3 mil M de los 12.41, porque la ventana todavía incluye el 29-30-oct. **Sin el robo, la salida de clientes es ≈−US$6.1 mil M (≈−4.3%)**, que sola ya sería ÁMBAR.
- **E1 sigue contaminado por el robo hasta la fila del 5-nov** (base 29-oct). La primera fila limpia es la del 6-nov (base 30-oct). Hasta entonces, lo que informa es el flujo diario (§B).

### B. La cola se frena el día dos

| Tramo | Horas | Flujo (mil M USD) | % | Ritmo %/h |
|---|---|---|---|---|
| Día uno, 1-nov 06:00 → 2-nov 00:00 | 18 | −6.14 | −4.55 | −0.253 |
| Día dos, 2-nov 00:00 → 14:09 | 14.15 | −1.63 | −1.26 | **−0.089** |

- **El ritmo del día dos es 0.35 veces el del día uno.** El día uno acumula 78% de lo que salió desde la reapertura.
- El día uno se aceleró por la tarde: a las 13:29 iba en −2.78% (ficha del 1-nov) y cerró en −4.55%. En las últimas ≈10.5 h salió ≈−1.8%, unos −0.17%/h, contra −0.37%/h en la mañana. El vigía ya lo había visto en el BTC.
- **Comparación** (DefiLlama, sin token propio):

| Exchange | Día 1 | Día 2 | Día 3 | Día 4 |
|---|---|---|---|---|
| Bitget (pausó; reabrió el 28-sep a las 08:00) | −7.88% | **+0.79%** | −3.47% | +11.25% (reposición) |
| Bybit (no pausó; hackeo el 21-feb ≈14:00) | −16.07% (≈−7.1% sin el robo) | **−24.42%** | +2.09% | +11.13% |
| **Binance** | **−4.55%** | **−1.26% parcial** | — | — |

- La forma de Binance se parece a la de Bitget: un exchange que pausó, reabrió por fases y deja la mayor parte de la salida en el día uno. No se parece a Bybit, que nunca pausó y cuyo día dos fue el peor. Mi lectura [I]: la pausa hace que la cola se acumule y salga junta al abrir; sin pausa, la duda crece a lo largo de 48 h.
- **Bitget, en cambio, volvió a sangrar el día tres (−3.47%)** antes de la reposición. Con n = 2, "día dos tranquilo" no garantiza "día tres tranquilo". La fase dos de Binance, anunciada para el 3-nov, abre más redes y por lo tanto más vías de salida.
- **Corrección a la ficha del 30-oct:** decía "Bybit −27.0% en 2 días", que es la salida de clientes sobre la base previa al robo. Con el método F compuesto y el robo incluido, son −36.7%. No son la misma medida, y las dos cifras se sostienen.

### C. Qué sale: el día dos son stablecoins

| Token | Día uno (mil M) | Día dos (mil M) |
|---|---|---|
| USDT | −2.41 | −1.23 |
| USDC (red principal) | −0.84 | −0.73 |
| BTC | −1.36 | −0.31 |
| ZEC | −0.95 | ≈0 |
| WETH | −0.33 | −0.14 |
| **Stablecoins / neto** | **53%** | **122%** (otros tokens entraron un poco) |

- **BTC en carteras:** 645,048 (1-nov 00:00) → 627,623 (2-nov 00:00) → **623,620 (14:09)**. Son −17,425 BTC el día uno y −4,003 en 14 h del día dos.
  - E2 (BTC a 7 días): −4.02% en la fila del 2-nov y −4.64% a las 14:09 contra el 26-oct. **VERDE, a 0.36 puntos del ÁMBAR (−5%).**
  - El umbral de P0220 (< 620,000 el 8-nov) queda a 3,620 BTC. Al ritmo del día dos (≈280 BTC/h) se cruzaría en ≈13 h. Lo dejo como dato, no como pronóstico: la serie oscila ±15,000 BTC por reclasificación de carteras.
- La salida de ZEC del día uno (−US$0.95 mil M) es demasiado grande para la liquidez de ese token. Puede ser una reasignación de carteras, no una salida de clientes [I]; no lo verifiqué.
- **BNB sobre lo rastreado:** 16.8% (VERDE, umbral 20%).

### D. "Replenishes the hot wallet": el freno lo pone Binance

Motivo de cierre de las redes sin retiro (getNetworkCoinAll, 15:23 UTC):

| Redes | Motivo (`withdrawDesc`) |
|---|---|
| 522 | "The wallet is currently undergoing maintenance" |
| **390** | **"Withdrawals are temporarily halted while Binance replenishes the hot wallet"** |
| 342 | "Withdrawal for this token is not supported, please try other networks" |
| 58 | "systems are currently undergoing maintenance" |
| 49 | "The network is currently experiencing issues" |
| 6 | "high withdrawal volumes, withdrawals have been paused to prevent long wait times" |

- **14 de 991 activos y 30 pares con retiro abierto.** Dentro de esos 14 activos hay **11 redes cerradas por "hot wallet"**: ARB/ETH, BTC/BSC, DOGE/BSC, ETH/BSC, SOL/BSC, SUI/BSC, USDT/AVAXC, USDT/MATIC, XRP/BSC, XRP/ETH y ZEC/BSC. Casi todas son versiones envueltas en BSC o redes secundarias; la red nativa de cada activo sigue abierta.
- **Pares abiertos en el tiempo:** 15/31 (03:02) → 14/30 (06:24; se cae POL/MATIC) → 14/30 (10:20 y 11:43) → **14/29 (13:16; USDT/TRX cerrado)** → **14/30 (15:23; USDT/TRX reabierto)**. USDT/TRX es la red con más volumen de USDT, y se cerró y reabrió en menos de 4 h.
- **Lectura [I]:** la billetera caliente es un inventario por red que Binance rellena desde frío. Cuando un par se cierra por "replenishes", la salida por esa red fue más rápida que el relleno. Eso dice tres cosas:
  1. La salida está **racionada por la oferta (Binance), no solo por la demanda (clientes)**. E1 mide la salida que Binance deja pasar, así que la corrida "real" puede ser mayor que la que se ve.
  2. El relleno ocurre (USDT/TRX volvió en <4 h), lo que es consistente con reservas en frío que existen y se mueven. La PoR del 31-oct con zk (Update #5, A) dice ≥1:1 en los 10 tokens, pero no la verifiqué con la herramienta.
  3. Para el dueño, **un par abierto ahora puede estar cerrado en la siguiente hora.** BTC/BTC (nativa) no ha cerrado ni una vez desde el 1-nov 06:18; BTC/BSC sí está cerrada por "hot wallet". Retirar por la red Bitcoin sigue siendo la ruta.
- Este endpoint no da el saldo de la billetera caliente, así que no se puede medir su tamaño; solo se ve si está "vacía" o no.

### E. BNB/BTC

- **0.009046** (15:23 UTC), **−1.82%** contra la base de P0217 (0.0092134). El umbral −3% (0.0089370) queda a 1.2 puntos.
- La razón empeoró desde el −0.50% de las 13:00 del 1-nov: BNB −1.58% en 24 h contra BTC −0.26%. **El token vuelve a ceder con la salida en curso.** Es el patrón de Bitget (BGB/BTC −2.8% a 7 días de reabrir), que la ficha del 1-nov creía descartado. P0217 se ve **más probable** que ayer.

## 3. Lectura para la decisión [I]

1. **E1 oficial ROJA (−8.78%).** No es un disparador nuevo: la contingencia está cumplida desde el 31-oct, y rige W44 ("retirar, no vender, no depositar"). Sí confirma lo que hay que hacer: **el BTC real del dueño (0.001325) debe salir por la red Bitcoin**, que sigue abierta. La alerta del 1-nov 06:18 UTC sigue sin confirmación.
2. **La cola se frena** (día dos con 0.35 veces el ritmo del día uno, como Bitget y no como Bybit), **pero no terminó**: hay 4,003 BTC menos en 14 h, BNB/BTC cede y la fase dos (3-nov) abre más redes.
3. **El MXN sigue sin salida** (MXN/FIAT_MONEY cerrado por "maintenance", no por "hot wallet"). El Update #5 no menciona el fiat. P0219 (MXN abierto el 8-nov, p 0.60) no cambia: falta saber qué redes trae la fase dos.
4. **Pronóstico nuevo P0221** (ver §5): ¿la semana siguiente (fila del 9-nov contra la del 2-nov) da flujo neto positivo? Prueba si Binance repite la reposición que tuvieron Bitget y Bybit en su día cuatro.

## 4. Límites

- **La fila intradía de DefiLlama (14:08:59) no es de cierre:** puede cambiar, y la API la sustituye. Las horas por cadena no se ven.
- **Atribución C:** si Binance mueve fondos entre carteras rastreadas y no rastreadas (un relleno desde frío hacia una caliente no rastreada, o al revés), aparece como salida o entrada falsa. El ZEC del día uno es sospechoso.
- **Las horas del día uno** suponen que la salida empezó a las 06:00. La fase uno abrió activos de forma progresiva hasta las 13:08.
- **Bitget y Bybit son n = 2,** con mecánicas distintas (Bybit no pausó). La regla "el día uno se lleva la mayor parte" es descriptiva, no una ley.
- **Motivos de cierre:** son textos que Binance pone en el endpoint. "Replenishes the hot wallet" no se puede verificar desde fuera; lo que sí se observa es que el par se cerró y se reabrió.
- La serie de pares por hora la tomé de las bitácoras (consultas manuales, no un registro continuo): un cierre de menos de 2 h pudo no verse.

## 5. Estado

**Documentado con comprobación.**
- Pronóstico P0221 registrado (autor `cripto`; resuelve el 10-nov).
- Siguientes pasos:
  - (a) la fila del 3-nov y la fase dos (qué redes trae y si incluye Lightning o MXN);
  - (b) la fila del 6-nov, la primera de E1 sin el robo en la ventana (base 30-oct);
  - (c) verificar con la herramienta de Binance la foto PoR zk del 31-oct y la del 4-nov (E3);
  - (d) P0207, P0217, P0219 y P0220 siguen abiertos.
