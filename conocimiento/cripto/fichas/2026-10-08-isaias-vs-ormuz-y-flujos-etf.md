# Ficha de avance · 8-oct-2026 · G5 Mercado (huracán Isaías vs. Irán/Ormuz: ¿cuál catalizador de petróleo pesa más en la caída de BTC de hoy?, más flujos de ETF)

> Corrida de las 08:17 CDMX (14:18 UTC), `analista-cripto`, estudio profundo. No toma un recurso nuevo de los 35 (todos "estudiado" en `recursos/indice.csv`): continúa el hilo de la ficha de ayer ([`fichas/2026-10-07-catalizador-macro-ormuz-derivados.md`](2026-10-07-catalizador-macro-ormuz-derivados.md)) con un catalizador de petróleo **nuevo y distinto** confirmado hoy por el dueño (`datos/entrada-dueno/2026-10-08.md`): el huracán Isaías, que cerró producción del Golfo de EUA y subió el Brent de forma clara desde la medianoche UTC de hoy. Pregunta: ¿el shock climático (Isaías) explica la caída de BTC de hoy, mejor o peor que el shock geopolítico (Ormuz) que ya se puso a prueba ayer?

## 1. Pregunta y método (declarados antes de mirar el resultado)

1. ¿El timing de Isaías (se volvió huracán la madrugada del 8-oct) coincide, con rezago razonable, con el tramo de caída de BTC de hoy?
2. ¿Hay una correlación medible, hora por hora, entre el movimiento del Brent de hoy y el de BTC?
3. ¿El resto del complejo macro (VIX, Nasdaq, 10 años) confirma un "risk-off" generalizado hoy, o el movimiento de hoy sigue acotado al petróleo?
4. ¿Hay algo cripto-específico (on-chain, flujos de ETF, derivados) que explique mejor la continuación de la caída que cualquiera de los dos catalizadores externos?
5. Recálculo completo del filtro de tendencia (SMA200, salida, reentrada) y el "roll" frente al vigente.
6. Revisión de contraparte (Binance) y de los pronósticos cripto abiertos (P0077, P0083 y el resto).

Fuentes públicas sin clave: `data-api.binance.vision` (spot y klines BTC/ETH), Yahoo Finance chart v8 (`BZ=F` Brent horario, `^VIX`, `^IXIC`, `^TNX`), Deribit (`public/ticker`, perpetuo BTC), `api.llama.fi/protocol/binance-cex` (TVL Binance), `tftc.io/bitcoin-etf-flows/october-2026` (flujos diarios de ETF spot BTC, agregador de SoSoValue/Farside), y el procesamiento ya hecho hoy por el sistema en `datos/entrada-dueno/2026-10-08.md` (verificación del huracán Isaías con CNBC/NPR/CBS/CNN).

## 2. Recálculo completo del filtro de tendencia: SIN "roll" — mismo motivo que ayer

Con `data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=201`, descartando la vela del día en curso (8-oct, todavía abierta a las 14:18 UTC):

- **200 cierres diarios usados:** del 22-mar-2026 al 7-oct-2026 (inclusive), último cierre completo = **83,321.81** (7-oct, 00:00-23:59:59 UTC).
- **SMA200 = 71,765.23** — **idéntica a la vigente** desde la cascada del 7-oct 18:42 CDMX (71,765.23) y a la que calculó la ficha del 7-oct a las 08:17 (71,693.21, ligera diferencia por la vela que entraba/salía de la ventana ese día). El conjunto de 200 cierres que usa esta corrida es el mismo que usó la cascada de ayer: la vela del 8-oct (hoy) todavía no cierra (cierra a las 00:00 UTC del 9-oct = 18:00 CDMX de hoy). **Sin "roll" en esta corrida — segundo día consecutivo sin cambio en la SMA200**, no porque el dato esté estancado, sino porque la ventana de 200 días completos no se ha movido desde la cascada de ayer.
- **Salida = SMA200 × 0.97 = 69,612.27.** **Reentrada = SMA200 × 1.03 = 73,918.18.** Sin cambio frente al nivel vigente.
- **Precio de referencia (14:18 UTC, Binance ticker 24h):** BTC/USDT **82,492.01** (−0.83% 24h, tras un mínimo de 24h de 81,773.43). ETH/USDT **2,527.56** (−1.53% 24h).
- **Colchón sobre la salida:** (82,492.01 − 69,612.27) / 69,612.27 = **+18.50%**. Sigue reduciéndose de forma gradual (19.10% a las 00:17 → 19.20% a las 04:17 → 18.71% a las 05:41 → 18.50% ahora), en línea con la caída continua del precio, no con un salto del nivel de salida (que no se mueve hasta que cierre la vela de hoy).
- **Filtro: ENCENDIDO, sin ambigüedad.** El colchón de 18.50% está lejos de 0%; no hay caso límite que decidir hoy. **Caso límite distinto y más cercano:** el umbral absoluto de 82,000 de P0077 está a solo **+0.60%** del precio en vivo (82,492.01 vs. 82,000); no es el filtro de la cuenta (que usa SMA200×0.97=69,612, muy lejos), sino el nivel de un pronóstico abierto — se detalla en §6.
- **Próximo "roll" esperado:** cuando cierre la vela diaria de hoy (00:00 UTC del 9-oct = 18:00 CDMX de hoy), que la cascada de las 18:42 CDMX alcanzará a recoger. Si el cierre de hoy (8-oct) queda bien por debajo del cierre que sale de la ventana (del 22-mar-2026, un periodo de precio distinto), la dirección exacta de la SMA200 no se puede adelantar sin ver ambos valores; se confirmará en la cascada de la noche.

## 3. Timing: Isaías se volvió huracán esta madrugada; Ormuz lleva 4 días sin incidente nuevo — ¿cuál pesa más hoy?

**Contexto de ambos catalizadores, ya verificados por otras corridas del sistema:**
- **Irán/Ormuz:** alerta Alta abierta desde fines de sep; el barrido de inteligencia de las 07:05 de hoy confirma el **cuarto día consecutivo sin un incidente cinético nuevo** (el último confirmado fue el del 5-oct, UKMTO Advisory 156-26, vía gCaptain — ver `bitacora/alertas.md`). Es un catalizador que **pierde intensidad marginal** día a día, no uno que se refuerza hoy.
- **Huracán Isaías:** se formó el 6-oct en el Golfo, se volvió huracán **la madrugada de hoy, 8-oct** (primero de la temporada 2026, empatando el récord de primer huracán más tardío desde 1905), con landfall previsto para el viernes/sábado en la costa norte del Golfo. Es un catalizador **nuevo, que se refuerza hora a hora hoy** (confirmado por el dueño y verificado por el sistema esta mañana, `datos/entrada-dueno/2026-10-08.md`).

**Velas horarias de hoy (Brent `BZ=F`, Yahoo; BTC/USDT, Binance), script verificado dos veces (Python puro con `statistics` y con NumPy, coinciden a 3 decimales; salida cruda en `scratchpad/g5_1008/isaias_vs_btc.py`, fuera del repo):**

| Hora UTC | Brent | BTC/USDT |
|---|---|---|
| 7-oct 23:00 (referencia, antes de que Isaías mueva el crudo) | 101.00 | 83,321.81 |
| 8-oct 00:00 (empieza a subir el Brent) | 101.24 | 83,369.84 |
| 8-oct 06:00 | 103.56 | 82,885.38 |
| 8-oct 10:00 (máximo del día hasta ahora) | 105.21 | 82,734.00 |
| 8-oct 13:00 (mínimo de BTC hasta ahora) | 104.53 | 82,182.01 |
| 8-oct 14:00 | 104.87 | 82,656.81 (último cierre horario completo) |

- **El Brent sube de forma monótona y clara desde las 00:00 UTC de hoy** (101.24 → 104.87 a las 14:00, **+3.58%** en 14 horas), con la aceleración más fuerte entre las 05:00 y las 10:00 UTC (102.78 → 105.21, +2.36% en 5 horas) — coincide bien con la ventana en que se habría confirmado y difundido la noticia de que Isaías se volvió huracán.
- **BTC, en cambio, no sigue ese patrón monótono:** cae de 83,370 (00:00) a 82,652 (04:00) —ya antes de que el Brent acelere—, luego **se recupera** levemente a 83,119 (09:00) mientras el Brent sigue subiendo con fuerza, y **cae a su mínimo del día (82,182, 13:00) precisamente cuando el Brent está plano** (104.42 → 104.53 entre las 09:00 y las 13:00). El peor tramo de BTC de hoy (09:00-13:00 UTC, −1.13%) ocurre con el petróleo sin movimiento neto.
- **Correlación de retornos horarios, 7-oct 04:00 a 8-oct 14:00 (n=33 pares, mismo método que la ficha del 7-oct §3, verificado con `statistics.pstdev`/`numpy.corrcoef`):**
  - Correlación contemporánea (mismo corte horario): **r = −0.03** (prácticamente nula; numpy: −0.030, Python puro: −0.033).
  - Correlación con el Brent liderando 1 hora (Brent(t−1→t) vs. BTC(t→t+1)): **r = −0.12** (numpy: −0.117, Python puro: −0.124) — **signo negativo, no positivo**: si la hipótesis de transmisión mecánica fuera correcta, se esperaría una correlación negativa entre el *retorno* del petróleo y el *retorno* de BTC (petróleo sube → BTC baja) con magnitud apreciable; aquí el signo es el correcto pero la magnitud es tan baja que es indistinguible de ruido con esta muestra (n=33).
- **Lectura:** igual que con Ormuz ayer, **el timing no sostiene una transmisión mecánica e instantánea**. La subida del Brent por Isaías es real, clara y acelerándose hoy — mucho más nítida en su propio gráfico horario que la de Ormuz hace dos días —, pero BTC no está siguiendo ese movimiento hora por hora; sus peores tramos de hoy coinciden con momentos en que el Brent está plano o incluso cuando BTC se recupera mientras el Brent sube. **Veredicto comparativo: ninguno de los dos catalizadores de petróleo (Ormuz, que se enfría, o Isaías, que se acelera) explica bien el patrón intradía de BTC de hoy**; Isaías es el más "fresco" y mediático de los dos, pero no pasa la misma prueba de timing que ya reprobó Ormuz ayer.

## 4. El resto del complejo macro: tampoco hay risk-off generalizado hoy

| Variable | Valor | Lectura |
|---|---|---|
| **VIX** | 15.08 (7-oct) → 15.40 (8-oct) | +2.1%. Movimiento menor; muy lejos de un salto de pánico (18-25+). |
| **Nasdaq (^IXIC)** | 27,538.69 (7-oct) → 27,473.50 (8-oct) | −0.24%. Casi plano. |
| **10 años (^TNX)** | 5.277% (7-oct) → 5.278% (8-oct) | Sin cambio. |
| **Deribit funding BTC** | instantáneo 1.27e-4, 8h 5.67e-5 (hoy 14:19 UTC) | Positivo y moderado, en línea con el resto de la semana (00:17: 5.49e-05; 04:17: 1.35e-05; 05:41: 1.08e-04). Sin tendencia clara a negativo (que delataría pánico de cortos) ni a extremo positivo (euforia). |
| **OI perpetuo Deribit** | US$824.84 M (hoy 14:19 UTC) | Dentro del rango de los últimos 4 pulsos de hoy (US$821.6-839.3 M): estable, sin caída abrupta que delate una cascada de cierre de posiciones. |

**Conclusión de esta sección:** igual que ayer con Ormuz, el shock de Isaías/petróleo de hoy **no viene acompañado de una firma de risk-off generalizado** (VIX, Nasdaq y 10 años casi inmóviles) ni de una firma de cascada de apalancamiento en derivados de BTC (funding y OI estables). Dos catalizadores externos distintos, dos veces la misma conclusión de timing: **ninguno de los dos explica mecánicamente el ritmo intradía de la caída de BTC**.

## 5. Lo cripto-específico que sí cuadra mejor: flujos de ETF spot girando a salida neta fuerte

Fuente: `tftc.io/bitcoin-etf-flows/october-2026` (agregador de datos de SoSoValue/Farside), consultado hoy. Complementa el límite explícito que dejó abierto la ficha de ayer (§9: los tres rastreadores habituales dieron 403 el 7-oct).

| Fecha | Flujo neto ETF spot BTC EUA (US$M) | Detalle |
|---|---|---|
| 1-oct | +102.7 | — |
| 2-oct | +189.8 | — |
| 5-oct | −89.9 | — |
| 6-oct | +118.9 | IBIT +122.0, MSTY/MSBT +7.8, GBTC Mini −11.0 |
| **7-oct** | **−487.1** | **IBIT −207.7, FBTC −105.1, ARKB −101.7, GBTC −39.3, BITB −27.6** (salida amplia, no concentrada en un solo fondo) |

- **Suma acumulada de octubre al 7-oct: +102.7+189.8−89.9+118.9−487.1 = −165.6 M USD** (verificado dos veces, suma manual y con `sum()` en Python). El mes, que llevaba saldo positivo hasta el 6-oct, **se volvió negativo de golpe con el outflow del 7-oct**, el día más fuerte de salida de la muestra reciente y el único de los últimos 5 días con salida de más de 5 fondos a la vez (no solo IBIT, el patrón habitual).
- **A diferencia de los dos catalizadores de petróleo (§3-4), el timing de este dato sí cuadra con el precio:** el 7-oct fue el día de la caída más fuerte de BTC en esta racha (ver tabla horaria de la ficha de ayer: −2.90% entre las 20:00 UTC del 6-oct y las 14:00 del 7-oct) y también el día de la salida de ETF más grande registrada en esta tabla. No se puede establecer causalidad con un solo día (n=1 para este tamaño de outflow), pero es el primer dato de esta semana que es **simultáneo y de magnitud proporcional** a la caída de precio, algo que ninguno de los dos catalizadores de petróleo logró mostrar en los cortes horarios.
- **Verificación de fecha (regla operativa fijada en la adenda del 2-oct, §11 del capítulo 05):** la tabla de tftc.io etiqueta explícitamente cada fila con su fecha de calendario; no se detectó la discrepancia de corte intradía que sí apareció el 30-sep/1-oct. **Grado C** (un solo agregador, sin segunda fuente de prensa cruzada hoy por límite de tiempo de esta corrida; pendiente cruzar con una nota de prensa que cite la cifra exacta del 7-oct).
- **Conexión con P0059** (pronóstico abierto, `autor=cripto`, "flujo neto acumulado de octubre positivo", vence 3-nov): con el dato de hoy, el acumulado del mes ya es negativo (−165.6M) a la mitad de la primera semana. No se resuelve (vence hasta el 3-nov), pero el patrón se debilitó frente a la lectura del 4-oct que lo originó.

## 6. Pronósticos abiertos: P0077 y P0083 se acercan, el resto sin cambios materiales

- **P0077** (vigía, BTC FRED CBBTCUSD ≤82,000 entre el 7 y el 21-oct, p=0.65): el último dato publicado de FRED es **83,239.49 (7-oct)**. El precio en vivo de hoy (82,492.01, Binance) está a solo **+0.60%** del umbral de 82,000, y el mínimo de 24h de hoy ya tocó 81,773.43 — **por debajo** del umbral, aunque FRED usa el índice de Coinbase (CBBTCUSD) con un corte de día distinto al de Binance, así que ese mínimo intradía de Binance no resuelve el pronóstico por sí solo. Sigue sin resolverse, pero la distancia al umbral es la más corta desde que se abrió.
- **P0083** (vigía, BTC Yahoo cierre diario UTC del 8-oct < 83,239.49, p=0.52, vence 9-oct): con el precio rondando 82,200-83,370 todo el día de hoy y el último cierre horario en 82,656.81 (14:00 UTC), el cierre del día está casi con certeza por debajo de 83,239.49 salvo un repunte fuerte en las ~10 horas que faltan para el cierre UTC (00:00 del 9-oct). No se resuelve en esta corrida (falta el cierre del día), pero la dirección favorece claramente el "SÍ" con el que se registró.
- **P0082** (cripto, OI Deribit ≥85% del valor del 7-oct para el 10-oct, p=0.80): OI actual US$824.84M vs. línea base US$841.50M = **98.0%** del valor base, muy por encima del umbral de 85% (US$715.3M). Sin cambio de lectura, tendencia favorable al "SÍ".
- **P0057** (PoR 47.º reporte, vence 2-nov), **P0059** (flujo ETF octubre positivo, vence 3-nov, ver §5), **P0065** (correlación BTC-SP500 >0.468, vence 5-nov) y **P0076** (fecha fija de Glamsterdam, vence 5-nov): sin novedad que cambie su lectura hoy; no vencen en esta corrida.

## 7. Contraparte (revisión semanal, corrida de las 08:17): sin disparador

- **E1/E2 (indicio, TVL DefiLlama):** `api.llama.fi/protocol/binance-cex` hoy (8-oct, 12:41 UTC) = **US$172.37 mil millones**, −2.85% frente a los US$177.42 mil millones del 7-oct 00:00 UTC. BTC cayó ~3.4% en la misma ventana (85,540→82,600 aprox.): la caída de TVL es, otra vez, del mismo orden que el efecto precio, no una señal de salida neta de unidades por encima del precio. **Limpio**, mismo patrón que el 7-oct.
- **E3 (PoR mensual):** sin novedad hoy (no se repitió la búsqueda dirigida completa por límite de tiempo de esta corrida, dado el enfoque en el catalizador de Isaías); sigue vigente el 46.º reporte, ventana proyectada del 47.º ~15-21-oct. **Sin cambio.**
- **E5, E6, E10:** sin búsqueda dirigida nueva hoy; última revisión (7-oct) sin hallazgos. **Sin cambio declarado** (sin verificación nueva, no se afirma "limpio" sin haberlo revisado hoy).
- **Conclusión: sin disparador nuevo identificado hoy**, con la salvedad explícita de que E3/E5/E6/E10 no se repitieron con búsqueda dirigida en esta corrida (tiempo dedicado al catalizador de Isaías, prioridad de la tarea de hoy).

## 8. Qué cambia para invertir

- **Para la cuenta `arena-claude-binance`:** nada cambia en el filtro (sigue ENCENDIDO, colchón 18.50%, sin caso límite; "roll" nulo por segundo día consecutivo, ver §2). El caso límite que sí vale la pena vigilar en las próximas corridas es el del propio precio frente al umbral absoluto de 82,000 de P0077 (no es un umbral de la cuenta, pero es la referencia psicológica/mediática más próxima).
- **Para la lectura del catalizador:** con dos episodios distintos (Ormuz el 6-7-oct, Isaías hoy) sometidos al mismo examen de timing horario, **ningún shock de petróleo pasa la prueba de coincidencia intradía con el movimiento de BTC**. El dato que sí calza en magnitud y tiempo con el tramo más fuerte de la caída (7-oct) es la salida de ETF de −487.1M del mismo día. Esto no prueba causalidad (podría ser que el ETF saliera *porque* el precio ya bajaba, no al revés — un fondo que crea/redime en efectivo reacciona al precio tanto como lo mueve), pero es la primera variable de esta semana que es cripto-específica, medible y simultánea.
- **Para el plan de estudio:** se repite y refuerza, con un segundo catalizador externo distinto, el hallazgo metodológico de la ficha del 7-oct: un shock de petróleo real y bien documentado en prensa no implica automáticamente una transmisión mecánica al precio de BTC en el mismo día; hace falta la vela horaria para comprobarlo caso por caso, no asumirlo por la coincidencia de fechas en los titulares.

## 9. Autoexamen

- ¿Puedo reproducir cada número sin ver la ficha? Sí: velas horarias de Yahoo (`BZ=F`) y Binance (klines 1h), Deribit (`public/ticker`), DefiLlama (`protocol/binance-cex`) y la tabla de tftc.io. Scripts en `scratchpad/g5_1008/` (fuera del repo).
- ¿Qué rompería la conclusión del §3? Una vela de minutos que mostrara a BTC cayendo en el mismo instante en que el Brent acelera (05:00-10:00 UTC) debilitaría el argumento del desfase; no se verificó a nivel de minuto por el límite de tiempo de esta corrida (mismo límite que declaró la ficha del 7-oct).
- ¿Qué rompería la lectura del §5 (ETF)? Un segundo día de outflow grande sin que el precio siga cayendo (o un repunte de precio pese al outflow) debilitaría la lectura de "coincidencia proporcional"; con n=1 día de outflow grande, esto es una observación, no un patrón.
- **Grado: B** para los datos de precio, Brent y derivados (reproducibles, fuentes independientes verificadas dos veces); **C** para la lectura comparativa Isaías-vs-Ormuz (dos episodios, n=2, mismo límite que el resto del capítulo); **C** para el dato de flujos de ETF (un solo agregador, sin segunda fuente de prensa cruzada hoy); **D** seguiría para cualquier intento de atribuir causalidad (no solo coincidencia) a los flujos de ETF.

## 10. Estado del pendiente

- Actualiza el capítulo de síntesis `05-mercado-on-chain-stablecoins-e-institucional.md` (adenda fechada 8-oct-2026, §14) y `conocimiento/estado-de-dominio.csv` (fila cripto/05).
- Actualiza `lista-senales-de-alerta.md` con el seguimiento semanal de contraparte del 8-oct (§7 de esta ficha, copiado ahí), señalando explícitamente qué señales no se revisaron hoy.
- Pendiente para la próxima corrida: cruzar el outflow del 7-oct (−487.1M) con una segunda fuente de prensa (CoinDesk, The Block) con fecha explícita; repetir la correlación horaria Brent-BTC cuando haya datos de Isaías tocando tierra (viernes/sábado) para ver si el patrón de desfase se repite una tercera vez.

Scripts y salidas crudas de esta sesión: `scratchpad/g5_1008/` (fuera del repositorio).
