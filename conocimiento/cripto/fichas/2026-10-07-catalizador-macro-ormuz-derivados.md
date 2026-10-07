# Ficha de avance · 7-oct-2026 · G5 Mercado (contraste del catalizador macro Irán/Ormuz y lectura de derivados durante la caída sostenida)

> Corrida de las 08:17 CDMX (14:18 UTC), `analista-cripto`, estudio profundo. No toma un recurso nuevo de los 35 (todos "estudiado" en `recursos/indice.csv`): continúa y pone a prueba, con datos en vivo, la hipótesis que dejó la corrida de inteligencia de las 07:05 CDMX de hoy (`bitacora/inteligencia/2026-10-07.md`, filas 13-15 y 27) — que la caída sostenida de BTC/ETH del 6-7 de octubre se transmite desde un shock de petróleo por la escalada Irán/Ormuz, sin catalizador cripto-específico — y repite el tema 1 del plan (microestructura de derivados) con una lectura en vivo durante el episodio, no en calma como las del 30-sep.

## 1. Pregunta y método (declarados antes de mirar el resultado)

1. ¿El petróleo (Brent, el referente del crudo marítimo que pasa por Ormuz, y WTI como contraste) tuvo un movimiento medible y con el momento (timing) correcto para transmitirse a BTC el 6-7 de octubre?
2. ¿El resto del complejo macro (VIX, dólar DXY, Treasury a 10 años, oro) muestra la firma de un "risk-off" clásico (equities nerviosas, dólar fuerte, oro refugio) o algo distinto?
3. ¿Los derivados de BTC (funding, interés abierto, base) muestran una cascada de apalancamiento forzado, o la caída es de tipo "venta de spot ordenada"?
4. ¿La cita de inteligencia del *working paper* del Chicago Fed (wp2026-16) es verificable y dice lo que se le atribuye?
5. Revisión semanal de contraparte (Binance) de la corrida de las 08:17, con la lista de señales.

Todo con fuentes públicas sin clave: Yahoo Finance (chart v8, velas de 1h) para Brent (`BZ=F`), WTI (`CL=F`), VIX (`^VIX`), DXY (`DX-Y.NYB`), el 10 años (`^TNX`) y oro (`GC=F`); Deribit y OKX para derivados de BTC; `data-api.binance.vision` para el spot y el filtro; DefiLlama para el TVL de Binance; búsquedas dirigidas para el PoR y el DOJ; y la página oficial del Chicago Fed para el paper.

## 2. Recálculo completo del filtro de tendencia (reconfirmación de la corrida de las 08:17)

Con `data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=201`, descartando la vela del día en curso (7-oct, todavía abierta):

- **200 cierres diarios usados:** del 21-mar-2026 al 6-oct-2026 (inclusive), último cierre completo = **85,549.93** (6-oct, 00:00 UTC).
- **SMA200 = 71,693.21** (idéntica a la vigente desde la cascada del 6-oct 18:42 CDMX, porque el conjunto de 200 cierres no cambió: la vela del 7-oct todavía no cierra). **Sin "roll" en esta corrida.**
- **Salida = SMA200 × 0.97 = 69,542.41.** **Reentrada = SMA200 × 1.03 = 73,844.00.**
- **Precio de referencia (14:20 UTC, Binance ticker 24h):** BTC/USDT **83,068.01** (−3.47% 24h). Colchón sobre la salida: **+19.45%**.
- **Filtro: ENCENDIDO**, sin ambigüedad (el colchón de 19.45% está muy lejos de 0%; no hay caso límite que decidir).
- **Próximo roll esperado:** cuando cierre la vela diaria del 7-oct (00:00 UTC del 8-oct = 18:00 CDMX del 7-oct), que la cascada de las 18:42 CDMX de hoy ya alcanzará a recoger (cierra 42 minutos antes de esa corrida). Si el cierre del 7-oct queda muy por debajo del cierre más antiguo que sale de la ventana (que viene de finales de marzo, un periodo de precio más bajo), la SMA200 podría incluso subir un poco a pesar de la caída de hoy; se confirmará en la cascada de la noche.

## 3. Petróleo: Brent sí se movió, con el timing adecuado para el titular, no para una transmisión mecánica e instantánea a BTC

**Error metodológico propio, corregido antes de escribir esta sección:** el primer corte que hice comparando cierres *diarios* de WTI (CL=F: 89.43 el 5-oct, 89.44 el 6-oct, 89.93 el 7-oct) parecía "plano", lo que me hizo dudar del catalizador. Repetir con velas **horarias** mostró que esa lectura diaria escondía un patrón intradía real: WTI y Brent cayeron la mañana del 6-oct y repuntaron con fuerza esa misma tarde-noche. La lección operativa (aplicable a futuras verificaciones): un cierre diario no basta para juzgar el timing de un shock intradía; hace falta la vela horaria.

| Hora UTC | Brent (BZ=F) | WTI (CL=F) | BTC/USDT (Binance) |
|---|---|---|---|
| 6-oct 12:00 (mínimo local) | 97.39 | 87.13 | 86,214.01 |
| 6-oct 20:00 | 101.15 (+3.86%) | 89.91 (+3.19%) | 85,611.41 (−0.70%) |
| 7-oct 00:00 | 101.40 | 90.13 | 85,540.01 |
| 7-oct 14:00 | 101.81 (+0.67% vs. 20:00) | 89.81 (−0.11% vs. 20:00) | 83,131.65 (−2.90% vs. 20:00) |

- **El petróleo (ambos referentes) sí subió de forma medible:** Brent +3.86% y WTI +3.19% entre el mínimo del 6-oct (12:00 UTC) y la noche de ese mismo día, consistente con la cobertura de gCaptain de nuevos incidentes en Ormuz el 5-6 de octubre (dos fuentes independientes: tanquero con 12 heridos y agotamiento del almacenamiento costa afuera de Irán).
- **El desajuste de tiempos es el hallazgo central de esta ficha:** la subida del petróleo ocurrió entre las 12:00 y las 20:00 UTC del 6-oct, ventana en la que BTC apenas se movió (−0.70%). La caída fuerte de BTC (−2.90% adicional) llegó **después**, entre las 20:00 UTC del 6-oct y las 14:00 UTC del 7-oct — precisamente la ventana en la que el petróleo ya estaba **plano** (Brent +0.67%, WTI −0.11%). Si la transmisión fuera mecánica e inmediata (oro/yields/dólar → BTC en el mismo corte horario), se esperaría que ambos se movieran juntos, no con un desfase de 6-13 horas donde el más grande de los dos movimientos de BTC llega cuando el petróleo ya se estabilizó.
- **Lectura:** el catalizador petrolero es real y verificable (grado B, como ya lo calificó inteligencia), pero el desfase de tiempos pesa contra una transmisión mecánica de "mismo corte horario"; es más consistente con que el mercado de BTC (24/7, con liquidez más delgada en horario asiático) reaccionó con rezago a una noticia que ya estaba completa, o con que una parte relevante de la caída de BTC tiene una causa adicional no capturada por el petróleo solo.

## 4. El resto del complejo macro no tiene la firma de un "risk-off" clásico

| Variable | Rango 5-6→7-oct (UTC) | Lectura |
|---|---|---|
| **VIX** | 15.00 (6-oct 18:00) → 15.86 (7-oct 11:00) | Calma casi total. Un shock de risk-off en equities suele mover el VIX varios puntos (a 18-25+); aquí el rango completo de 48 horas es de 0.86 puntos. **Sin pánico accionario.** |
| **DXY (dólar)** | 101.80 (mín. 6-oct) → 102.44 (7-oct 12:00) | +0.63%. Dirección consistente con "dólar más fuerte", pero de magnitud modesta, no un salto. |
| **Treasury 10 años (^TNX)** | 5.26-5.35% (5 y 6-oct) | Rango de 9 puntos base en dos días: ruido, no un salto de "yields al alza" que respalde la narrativa de inflación por petróleo. |
| **Oro (GC=F)** | 4,203.80 (6-oct, pico) → 4,124.80 (7-oct 14:00) | **−1.88%, cayendo junto con BTC**, no como refugio. Si el canal fuera "petróleo → inflación → tasas reales más altas", una caída del oro es coherente (el oro es sensible al costo de oportunidad), pero entonces se esperaría un salto más claro del 10 años, que no se observó. Si el canal fuera "miedo geopolítico", se esperaría que el oro subiera, no que cayera. Ninguna de las dos lecturas calza del todo. |

**Conclusión de esta sección:** no hay una firma de risk-off de manual (equities nerviosas + dólar fuerte + bonos comprados + oro buscado). Lo único que se movió con una magnitud clara fue el petróleo (ambos referentes) y, en menor medida, BTC y ETH (mayor caída relativa que cualquier otro activo de la tabla). Esto es consistente con la idea de que BTC/ETH están amplificando (beta alto) una señal macro real pero modesta — o con que una porción de la caída de cripto es idiosincrática y no está explicada por el petróleo.

## 5. Derivados de BTC en vivo (Deribit + OKX): sin señal de cascada de apalancamiento

Mismo método que la ficha del 30-sep (`fichas/2026-09-30-microestructura-funding-basis-oi.md`), repetido hoy **durante** la caída, no en un día de calma:

```python
import json, urllib.request, statistics, datetime

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "estudio-cripto"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

now_ms = int(datetime.datetime.utcnow().timestamp() * 1000)
spot = float(get("https://data-api.binance.vision/api/v3/ticker/price?symbol=BTCUSDT")["price"])
perp = get("https://www.deribit.com/api/v2/public/ticker?instrument_name=BTC-PERPETUAL")["result"]
fut  = get("https://www.deribit.com/api/v2/public/ticker?instrument_name=BTC-25DEC26")["result"]
exp_ms = 1798185600000
days = (exp_ms - now_ms) / 1000 / 86400
basis_idx  = fut["mark_price"] / fut["index_price"] - 1
basis_spot = fut["mark_price"] / spot - 1

week_ms, month_ms = now_ms - 7*86400*1000, now_ms - 30*86400*1000
r7  = [x["interest_8h"] for x in get(f"https://www.deribit.com/api/v2/public/get_funding_rate_history?instrument_name=BTC-PERPETUAL&start_timestamp={week_ms}&end_timestamp={now_ms}")["result"]]
r30 = [x["interest_8h"] for x in get(f"https://www.deribit.com/api/v2/public/get_funding_rate_history?instrument_name=BTC-PERPETUAL&start_timestamp={month_ms}&end_timestamp={now_ms}")["result"]]
okx_fr = float(get("https://www.okx.com/api/v5/public/funding-rate?instId=BTC-USDT-SWAP")["data"][0]["fundingRate"])
```

**Resultado de la corrida (7-oct-2026, 14:21:16 UTC; salida cruda en `scratchpad/g5_1007/derivados.py`, fuera del repo):**

| Métrica | Hoy (7-oct, durante la caída) | 30-sep (referencia, calma) |
|---|---|---|
| Funding Deribit instantáneo (8h) | **0.0000%** | +0.01204% |
| Funding Deribit anualizado 7d | **+3.41%/año** | +0.95%/año |
| Funding Deribit anualizado 30d | **+4.05%/año** (mín. −0.0046%, máx. +0.0303% por periodo de 8h; 8.9% de los 720 periodos negativos) | +3.94%/año (12.8% de periodos negativos) |
| Funding OKX instantáneo | **+0.0000159%** (+1.74%/año anualizado) | +0.00481% (+5.27%/año) |
| Base futuro dic-2026 vs. índice Deribit | **+5.18%/año** | +5.17%/año |
| Base futuro dic-2026 vs. spot Binance | **+4.94%/año** | +4.97%/año |
| OI perpetuo Deribit (USD) | **US$841.5 M** | US$793.1 M |
| OI perpetuo OKX | 3,044,177 contratos (unidad ambigua en la respuesta de hoy, ver límite abajo) | US$2,329.2 M (27,686 BTC) |

- **Lectura:** el funding está **tranquilo y positivo en ambos exchanges**, ni cerca de los valores negativos profundos que acompañarían un *short squeeze* o una capitulación apalancada, ni en los niveles altos que acompañarían euforia. La base del futuro de diciembre es **prácticamente idéntica** a la de hace una semana (+4.9-5.2%/año en ambos cortes): no hay señal de contango invertido (pánico) ni de una base extrema (euforia). El interés abierto de Deribit incluso **subió** ligeramente (US$793→841 M) durante la caída, lo normal si la caída es sobre todo venta de spot y no una liquidación forzada de posiciones largas en perpetuos.
- **Conclusión:** la caída del 6-7 de octubre **no tiene la firma de una cascada de liquidaciones apalancadas** como la del 10-oct-2025 (que llegó con funding positivo persistente e interés abierto récord antes del evento, documentado en el capítulo 03). Es más compatible con venta ordenada de spot — en los dos exchanges donde se puede medir hoy sin clave de pago.
- **Límite:** cobertura parcial (solo Deribit y OKX; Binance Futures y Bybit siguen geo-restringidos/bloqueados; CoinGlass sigue de pago). El campo `oiCcy` de OKX de hoy (30,441.77) es inconsistente en unidades con el de la ficha del 30-sep (que daba US$2,329.2 M con el mismo endpoint); no se resolvió la discrepancia en esta corrida y se declara como hueco de datos, no se usa el número de hoy de OKX para ninguna conclusión. **Grado B** para Deribit (reproducible, consistente con su propia historia reciente); **grado C** para "sin estrés" en el agregado del mercado, por la cobertura parcial.

## 6. Verificación de la cita académica de inteligencia (Chicago Fed, wp2026-16)

Inteligencia citó este *working paper* como marco para "BTC se transmite sin necesitar catalizador cripto-específico". Verificación directa en `chicagofed.org/publications/working-papers/2026/2026-16`:

- **Existe y es real:** *"Crypto Is Coming of Age: The Case of Bitcoin's Rising Beta"*, de Alejandro H. Drexler, Andre Guettler y Angela Sun (Reserva Federal de Chicago, clasificación JEL de economía financiera y macroeconomía/monetaria).
- **Lo que dice de verdad:** estima betas de BTC frente a NASDAQ, Dow Jones y bonos del Tesoro que **varían con el tiempo** y documenta que la exposición de BTC a las acciones **aumentó sustancialmente desde ~2020**, hasta volverse estadísticamente significativa; y que BTC responde más al **sentimiento general del mercado accionario** que a un sector tecnológico específico.
- **Lo que NO dice:** no menciona el petróleo, el Estrecho de Ormuz ni ningún canal específico de "shock geopolítico petrolero → BTC". Es evidencia legítima de que BTC tiene beta alto a activos de riesgo en general (coincide con el hallazgo propio del 29-sep sobre beta BTC-Nasdaq y con el de 5-oct sobre BTC-S&P500), **no** evidencia directa del mecanismo petróleo-específico que se le atribuyó. La cita de inteligencia no es falsa, pero **generaliza** un poco más de lo que el paper mismo sostiene: el paper da el "por qué BTC podría amplificar cualquier shock de riesgo", no el "por qué este shock de petróleo en particular ya se transmitió". Dado que el VIX (la medida de sentimiento accionario que el propio paper usa como ancla) no se movió esta vez (§4), el mecanismo que el paper describe no tiene, hoy, una señal clara que transmitir.
- **Búsqueda de un paper 2025-2026 específico sobre transmisión de shocks petroleros geopolíticos puntuales a BTC** (pendiente abierto desde la ficha del 28-sep, `estado-de-dominio.csv` fila cripto/01): sigue sin encontrarse un paper revisado por pares con ese enfoque exacto. Se encontró `arXiv:2409.17057` ("The Impact of Geopolitical Risks on Bitcoin Volume Growth: Evidence from a Panel Data Analysis", panel de 33 países + UE), que documenta que el índice de riesgo geopolítico (GPR) tiene un efecto positivo sobre el **volumen** de operación de BTC, sobre todo en países en desarrollo — un hallazgo sobre actividad, no sobre dirección de precio, así que tampoco cierra el pendiente. **El pendiente queda abierto otra vez; grado D para la transmisión precio-específica petróleo→BTC, sin cambio desde el 28-sep.**

## 7. Contraparte (revisión semanal, corrida de las 08:17): sin disparador

- **E3 (PoR mensual):** búsqueda dirigida hoy ("Binance proof of reserves 47th report October 2026") sigue sin encontrar el 47.º reporte; solo aparecen coberturas del 45.º (ago-2026). Sigue vigente el 46.º (snapshot 1-sep-2026, ~682,000 BTC, ratio "al menos 1:1"). Consistente con la ventana proyectada desde el 3-oct (~15-21-oct-2026). **Limpio.**
- **E5:** búsqueda dirigida hoy no encontró ningún acto procesal nuevo con fecha verificable de oct-2026 contra la entidad (solo cobertura reciclada de la ronda de 2023, ya registrada en A8, y la investigación por sanciones a Irán ya conocida desde el 21/22-sep). **ÁMBAR sin cambio desde el 25-sep.**
- **E1/E2 (indicio):** TVL total de `api.llama.fi/protocol/binance-cex` = **US$174.09 mil millones** (7-oct, 14:22 UTC), −2.68% frente a los US$178.87 mil millones del 6-oct. La caída es del mismo orden que la del precio de BTC/ETH en 24h (−3.5%/−5.4%), así que es consistente con el **efecto precio** sobre activos custodiados, no con una salida neta de unidades (que requeriría la metodología exacta de la sección F, no disponible hoy). **Sin disparador**, con la misma salvedad metodológica que vienen repitiendo las entradas anteriores.
- **E6, E10:** sin novedad en las búsquedas de hoy.
- **Conclusión: sin disparador.** Ninguna señal ROJA; ÁMBAR solo en E5 y A9, sin cambio desde el 25-sep. No se cumple ningún disparador de `bitacora/decisiones/2026-09-25-CRIPTO-inicial.md`.

## 8. Qué cambia para invertir

- **Para la cuenta `arena-claude-binance`:** nada cambia en el filtro (sigue ENCENDIDO, colchón de 19.45%, sin caso límite). La ausencia de señal de cascada en derivados (§5) es un dato ligeramente tranquilizador: si el filtro llegara a dispararse, sería por el nivel de precio, no porque el mercado ya esté en pánico de apalancamiento, lo que en principio deja más margen de ejecución ordenada si se llegara a ese escenario.
- **Para la lectura del catalizador:** se mantiene como lo calificó inteligencia (grado B, "probable, no cripto-específico"), pero con dos matices que esta ficha agrega y que vale la pena pasar a la próxima corrida de inteligencia: (a) el petróleo sí se movió, pero con 6-13 horas de desfase frente al tramo más fuerte de la caída de BTC, lo que debilita una lectura de transmisión mecánica e instantánea; (b) el resto del complejo macro (VIX, 10 años) no confirma un "risk-off" de manual, así que BTC/ETH están cayendo más de lo que el movimiento observado en el resto de los activos de riesgo sugeriría por sí solo. **No se encontró ningún catalizador cripto-específico** (confirmado de nuevo hoy en la lista de señales, §7): sin hackeo, sin salida anómala de ETF confirmada con fuente primaria (ver límite del §9), sin regulación nueva, sin depeg de stablecoin.
- **Para el plan de estudio:** el pendiente de "buscar un paper 2025-2026 sobre transmisión de shocks petroleros geopolíticos puntuales a BTC" sigue abierto (§6); se intentó de nuevo hoy sin éxito.

## 9. Límite explícito: flujos de ETF spot, sin dato verificado hoy

Los tres rastreadores habituales (Farside, SoSoValue, el tablero mensual de TFTC) devolvieron **403 Forbidden** desde este entorno en los tres intentos de hoy. Las búsquedas web dieron cifras contradictorias entre sí para el 6-oct (desde "+US$1.19 mil M" hasta referencias a una "racha de salidas de 6 días") sin que ninguna fuente primaria las respaldara de forma verificable en esta corrida; **se descartan explícitamente, no se usa ninguna cifra de flujo de ETF de hoy** (ni para esta ficha ni para el pronóstico de abajo). Pendiente para la próxima corrida: reintentar con Farside/SoSoValue, o con prensa seria que cite explícitamente la cifra de SoSoValue con fecha clara (regla ya anotada en la adenda del 2-oct, §11 de este capítulo).

## 10. Autoexamen

- ¿Puedo reproducir cada número sin ver la ficha? Sí: velas horarias de Yahoo (`BZ=F`, `CL=F`, `^VIX`, `DX-Y.NYB`, `GC=F`), Deribit/OKX con las mismas llamadas de la ficha del 30-sep, y la página oficial del Chicago Fed para el paper. Scripts en `scratchpad/g5_1007/` (fuera del repo).
- ¿Qué rompería la conclusión del §3? Si hubiera una vela de minutos (no horaria) que mostrara a BTC cayendo en el mismo instante en que Brent subía, el argumento del desfase se debilitaría; no se verificó a nivel de minuto por el límite de esta corrida.
- **Grado: B** para los datos de precio y derivados (reproducibles, múltiples fuentes independientes); **C** para la lectura de "el petróleo no explica toda la caída" (depende de que el desfase de horas sea informativo y no ruido de un solo episodio, n=1); **D** para la transmisión petróleo-específica en la literatura académica (sigue sin encontrarse el paper exacto).

## 11. Estado del pendiente

- Pendiente de `estado-de-dominio.csv` (fila cripto/01, 28-sep-2026): "buscar un paper 2025-2026 que mida transmisión de shocks petroleros geopolíticos puntuales a BTC" — **se repitió la búsqueda hoy, sin éxito** (sigue grado D; se encontró un paper relacionado pero no equivalente, arXiv:2409.17057, sobre volumen y no sobre precio).
- Actualiza el capítulo de síntesis `05-mercado-on-chain-stablecoins-e-institucional.md` (adenda fechada 7-oct-2026, §13) y `conocimiento/estado-de-dominio.csv` (fila cripto/05).
- Actualiza `lista-senales-de-alerta.md` con el seguimiento semanal de contraparte del 7-oct (§7 de esta ficha, copiado ahí).

Scripts y salidas crudas de esta sesión: `scratchpad/g5_1007/` y `scratchpad/g5_micro_1007/` (fuera del repositorio).
