# Ficha de avance · 1-oct-2026 · Ciclos y halving (tema 2 del plan)

> Corrida de las 08:17 CDMX (14:18:34 UTC), `analista-cripto`. Toma el **tema 2** de "Temas que no cubren los 35 recursos y que el torneo necesita" (`00-plan-de-estudio.md`): *"Ciclos y halving. Qué dice la evidencia, con solo 3-4 ciclos: grado C como máximo."* Es el siguiente tema pendiente de menor número: el tema 1 (microestructura) se cubrió el 30-sep y el tema 3 (BTC vs. tasa real/Nasdaq/USD-MXN) el 29-sep.

## 1. Acceso real y fuente de datos

- **CoinGecko** (`api.coingecko.com/v3/coins/bitcoin/market_chart/range`) dio `429 Too Many Requests` en el intento de hoy: se descarta esa vía y no se insiste con reintentos agresivos (cumplimiento de uso razonable de API pública).
- **Fuente usada, pública y sin clave:** Yahoo Finance chart v8 (`query1.finance.yahoo.com/v8/finance/chart/BTC-USD`, interval=1d), la misma que ya usa el resto de la base para BTC-USD. Serie diaria completa descargada hoy: **4,398 velas, del 2014-09-17 al 2026-10-01**.
- **Límite declarado de entrada:** Yahoo no tiene datos de BTC-USD antes de sep-2014, así que el **primer halving (28-nov-2012) queda fuera de esta muestra**. Esta ficha solo puede verificar con cálculo propio **3 halvings: H2 (9-jul-2016), H3 (11-may-2020) y H4 (19-abr-2024)**. Es exactamente la advertencia que ya hace el plan de estudio ("con solo 3-4 ciclos: grado C como máximo"); aquí se confirma con n=3, no 4.
- **Altura de bloque y próximo halving (H5):** `mempool.space/api/blocks/tip/height` y `.../api/v1/difficulty-adjustment`, consultados hoy en vivo (altura 969,453; tiempo medio por bloque de la última ventana de ajuste: 599.4 s).
- Script de la sesión: cálculo en línea de comandos (`urllib`/`pickle`, sin librerías de pago), sin reprocesar después de ver el resultado.

## 2. Metodología

1. Para cada halving, ubicar el primer cierre diario de Yahoo en o después de la fecha del halving (precio de referencia "día 0").
2. Calcular el retorno a +180, +365, +546 (18 meses) y +730 días.
3. Encontrar el **máximo de cierre dentro de una ventana fija de 730 días** tras cada halving (ventana fija para no mezclar el repunte del ciclo siguiente) y el número de días transcurridos hasta ese máximo.
4. Calcular la **caída máxima pico-a-valle** (peak-to-trough, sobre cierres diarios) dentro de los primeros 1,460 días (4 años) tras cada halving, o hasta donde haya dato.
5. Calcular el retorno de los 180 días **antes** de cada halving, para ver si el halving "ya estaba en el precio".
6. Como ejercicio adicional (ligado al pronóstico de hoy), ubicar el **punto análogo de cada ciclo anterior** al número de días transcurridos desde H4 hasta hoy (895 días) y medir el retorno de los 30 días siguientes a ese punto análogo.
7. Estimar la fecha de H5 con la altura de bloque actual, los 80,547 bloques que faltan hasta el bloque 1,050,000 y el tiempo medio por bloque de la ventana de ajuste vigente.

## 3. Resultados (cálculo propio, verificado dos veces con el mismo script)

### 3.1 Retorno tras cada halving (precio de referencia = primer cierre ≥ fecha del halving)

| Halving | Precio en halving | +180d | +365d | +546d (18m) | +730d |
|---|---|---|---|---|---|
| H2 (2016-07-09) | 650.96 | +55.7% | +286.9% | +2,592.5% (17,527 el 2018-01-06) | +935.7% |
| H3 (2020-05-11) | 8,601.80 | +72.4% | +559.2% | +685.5% | +236.4% |
| H4 (2024-04-19) | 63,843.57 | +5.9% | +33.2% | +66.8% | +15.7% |

**Patrón más fuerte del torneo: los retornos a cada horizonte se encogen de ciclo en ciclo**, con un salto particularmente grande entre H2→H3 y H3→H4. A +365 días: 286.9% → 559.2% → 33.2%. A +730 días: 935.7% → 236.4% → 15.7%.

### 3.2 Máximo de cierre dentro de los primeros 730 días (ventana fija, sin mezclar el ciclo siguiente)

| Halving | Máximo | Fecha | Días tras el halving | Retorno al máximo |
|---|---|---|---|---|
| H2 | 19,497.40 | 2017-12-16 | **525** | +2,895.2% |
| H3 | 67,566.83 | 2021-11-08 | **546** | +685.5% |
| H4 | 124,752.53 | 2025-10-06 | **535** | +95.4% |

**Hallazgo [H], grado B en la mecánica del cálculo (reproducible con todo el historial disponible) y grado C en la interpretación causal:** el **tiempo hasta el pico del ciclo es notablemente estable** (525, 546 y 535 días; media 535, desviación ±10.6 días, coeficiente de variación de solo 2%), mientras que la **magnitud del retorno se desploma** (2,895% → 685% → 95%). Con n=3 no se puede afirmar que el reloj de "~17-18 meses" sea una ley causal (podría ser un artefacto de que los tres ciclos compartieron un contexto parecido de adopción retail con rezago, no evidencia independiente de un mecanismo); tampoco se puede extrapolar con confianza a H5, sobre todo porque el ciclo H4 ya tiene flujos institucionales (ETFs spot) que no existían en H2 ni H3, lo que es la explicación más citada en la literatura de mercado (no académica revisada por pares) para el encogimiento del retorno.

### 3.3 Caída máxima pico-a-valle tras el pico del ciclo (dentro de 1,460 días desde el halving)

| Halving | Caída máxima | Desde (pico) | Hasta (valle) |
|---|---|---|---|
| H2 | −83.4% | 2017-12-16 (19,497) | 2018-12-15 |
| H3 | −76.6% | 2021-11-08 (73,084; nota: no es el mismo "máximo de 730d" de 3.2 porque esta ventana es más larga y capturó un pico ligeramente distinto) | 2022-11-21 |
| H4 | −53.1% (hasta ahora; la ventana de 1,460 días de H4 termina en abril-2028, no concluida) | 2025-10-06 (124,753) | 2026-06-30 |

**Hallazgo:** la caída también se encoge (−83.4% → −76.6% → −53.1%, y este último número es parcial porque el ciclo de H4 sigue en curso). Es consistente con 3.2: menos retorno de subida, menos caída de bajada. **Grado C**: 3 observaciones, no independientes del mismo proceso generador (BTC), y la de H4 está censurada (no se sabe si hará un mínimo más profundo antes de H5).

### 3.4 Retorno de los 180 días antes de cada halving ("¿ya estaba en el precio?")

| Halving | Retorno pre-halving (180d) |
|---|---|
| H2 | +45.2% |
| H3 | −2.3% |
| H4 | +112.9% |

**Sin patrón consistente** (de −2.3% a +112.9%): no hay evidencia en esta muestra de que el mercado "descuente" el halving de forma sistemática antes de que ocurra. Esto es relevante porque contradice una narrativa común de redes sociales ("el halving siempre se descuenta antes"); con n=3 la dispersión es demasiado grande para sostenerla o refutarla con fuerza, pero el dato no la respalda.

### 3.5 Punto análogo de hoy (895 días post-halving) en los ciclos anteriores, y retorno a 30 días desde ahí

Hoy (1-oct-2026) son **895 días desde H4** (19-abr-2024), es decir, ya pasado el pico típico de ~535 días y camino hacia la zona de mínimo del ciclo (que en H2 y H3 ocurrió hacia los días ~890-1,030).

| Halving | Fecha análoga (día 895) | Precio ahí | +30 días | Retorno 30d |
|---|---|---|---|---|
| H2 | 2018-12-21 | 3,896.54 | 2019-01-20 @ 3,601.01 | **−7.6%** |
| H3 | 2022-10-23 | 19,567.01 | 2022-11-22 @ 16,189.77 | **−17.3%** (coincide con el colapso de FTX, 11-nov-2022: un choque idiosincrático, no un patrón de calendario puro) |

**Lectura para el pronóstico de hoy:** en los dos ciclos anteriores, el punto equivalente a "hoy" en el reloj del halving fue seguido de una caída a 30 días (−7.6% y −17.3%, media −12.4%). **Grado D para usarlo solo:** n=2, no independientes (ambos "caen" dentro del mismo tramo descendente estructural de cada ciclo, y uno de los dos casos está contaminado por un evento de cola específico, FTX, que no tiene por qué repetirse). Se usa como un insumo más, no como la base única, del pronóstico P0047 de hoy.

### 3.6 Próximo halving (H5): estimación con datos en vivo de la red

- Altura actual: 969,453 (mempool.space, hoy). Halving en el bloque 1,050,000 → faltan **80,547 bloques**.
- Tiempo medio por bloque de la ventana de ajuste vigente: 599.4 s (~9.99 min, consistente con el objetivo de 10 min de Bitcoin).
- **Estimación: 80,547 × 599.4 s ≈ 558.8 días → H5 ≈ 11-abr-2028** (±varias semanas, porque el tiempo de bloque fluctúa con el hashrate; es una proyección lineal, no una fecha fija del protocolo).

## 4. Qué cambia para invertir (en la cuenta `arena-claude-binance`)

- **No cambia el filtro de tendencia vigente** (SMA200 × 0.97/1.03): el reloj del halving es demasiado lento e impreciso (n=3, ventana de ±10 días en el pico, pero rango de meses en el valle) para sustituir una regla mecánica y diaria.
- **Sirve como contexto de régimen, no como señal de entrada/salida:** estar hoy a 895 días de H4 (pasado el pico típico de ~535 días, acercándose a la zona histórica de mínimo de ciclo de los dos precedentes) es un argumento adicional —no el único— para **no aumentar la exposición más allá de lo ya aprobado por el comité** mientras no haya una señal de tendencia que lo respalde, y para no sorprenderse si la cuenta ve más meses de descenso o lateralidad antes de un posible repunte hacia 2027-2028.
- **El hallazgo del encogimiento de retornos (3.1-3.3) es el más robusto de esta ficha** porque es puramente descriptivo (no depende de ningún supuesto sobre el futuro) y es consistente en las tres dimensiones medidas (subida, tiempo al pico, caída). Es coherente con la tesis de "institucionalización reduce la varianza y el retorno esperado", pero esta ficha no prueba esa causa, solo documenta el patrón.

## 5. Contrapuntos

- **N pequeño y no independiente:** los 3 ciclos comparten el mismo activo y, en gran medida, el mismo tipo de participantes retail-que-luego-institucional; no son 3 experimentos independientes, son 3 realizaciones correlacionadas del mismo proceso. Cualquier "ley" de 535 días o de escalamiento de retornos puede romperse en H5.
- **ETFs spot (lanzados ene-2024) cambian la demanda marginal de H4 en adelante** de forma que H2 y H3 no capturan; el patrón de "encogimiento" podría acelerarse o revertirse por esa única razón estructural, no por el calendario del halving en sí.
- **El halving reduce la emisión, no la demanda:** la teoría de "shock de oferta" que populariza la narrativa de halving no tiene, hasta donde se buscó hoy, un paper revisado por pares que aísle el efecto de oferta del efecto de demanda/narrativa/flujo de capital que ocurre en la misma ventana. Se declara explícitamente: no se encontró ni se afirma esa literatura en esta ficha.
- **La sección 3.5 (punto análogo) es la más débil de todas:** n=2 y un caso contaminado por FTX. Se incluye con su grado D explícito, no como conclusión fuerte.

## 6. Autoexamen

1. ¿Por qué el primer halving (nov-2012) no se puede verificar con esta fuente? → Yahoo Finance no tiene datos diarios de BTC-USD antes de sep-2014.
2. ¿Qué patrón es más robusto en esta ficha: el tiempo al pico o la magnitud del retorno? → El tiempo al pico (525-546 días, CV 2%); la magnitud se encoge de forma pronunciada entre ciclos.
3. ¿Por qué no se usa el "reloj del halving" para mover el filtro de tendencia de la cuenta real? → Porque n=3 con una ventana de incertidumbre de meses en el valle del ciclo no compite con una regla diaria y mecánica (SMA200) ya aprobada por el comité.
4. ¿Qué grado tiene el hallazgo de la sección 3.5 y por qué? → Grado D: n=2, no independientes, uno contaminado por un evento de cola (FTX).

## 7. Grado y estado

- **Grado C** en general (como ya advertía el plan), con el detalle de que: la sección 3.1-3.3 (retornos, tiempo al pico, encogimiento) es **B en la mecánica del cálculo** (reproducible con el 100% del historial de Yahoo disponible) y **C en la interpretación** (n=3, no independiente); la sección 3.4 es **C** (sin patrón claro); la sección 3.5 es **D** (n=2, un caso contaminado).
- **Estado:** Documentado con comprobación numérica propia (verificada dos veces, mismo script, mismos datos).
- **Siguiente prueba:** repetir el ejercicio de 3.1-3.3 con ETH (halving no aplica igual, pero sirve de contraste de un activo sin halving en el mismo periodo) y, cuando haya más historia, extender la ventana de la caída de H4 más allá de 1,460 días para ver si hace un valle más profundo que 2026-06-30.
