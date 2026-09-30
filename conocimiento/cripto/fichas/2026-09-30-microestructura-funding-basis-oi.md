# Ficha de avance · 30-sep-2026 · G5 Mercado (microestructura de derivados: funding, base e interés abierto)

> Corrida de las 08:17 CDMX (14:18 UTC), `analista-cripto`. Toma el **tema 1** de "Temas que no cubren los 35 recursos y que el torneo necesita" (`00-plan-de-estudio.md`): *"Microestructura de exchanges cripto. Funding, base, interés abierto, cascadas de liquidación (10-oct-2025) y profundidad de los pares MXN en Binance"*. La cascada de liquidaciones del 10-oct-2025 ya está documentada a fondo en el capítulo `03-defi-mecanica-riesgos-y-academia.md` §4 (con cifras de CoinGlass/CoinDesk/CNN). Lo que faltaba, y que esta ficha cubre con cálculo propio de hoy, es **funding, base (basis) e interés abierto en vivo**, más la **profundidad del par BTC/MXN** — el hueco explícito que señaló el pulso de esta misma corrida sobre la geo-restricción de la API de futuros de Binance.

## 1. Acceso real y el problema de origen

- **`fapi.binance.com` (API de futuros de Binance) está geo-restringida desde este entorno.** Verificado hoy: `GET /fapi/v1/premiumIndex`, `/fapi/v1/openInterest` y `/fapi/v1/fundingRate` devuelven los tres `{"code":0,"msg":"Service unavailable from a restricted location according to 'b. Eligibility'..."}`. Es el mismo bloqueo que ya reporta el pulso de esta rutina cuando toca derivados de Binance; no es nuevo hoy.
- **`api.bybit.com` también está bloqueada** por el CDN (CloudFront) desde este entorno ("configured to block access from your country").
- **Fuentes que sí funcionan hoy, públicas y sin clave:**
  - **Deribit** (`www.deribit.com/api/v2/public/...`): funding histórico y actual, open interest y mark/index price del perpetuo BTC y de futuros con vencimiento fijo. Deribit es el mercado de referencia histórico de opciones/futuros de BTC (antes de que CME y Binance crecieran) y su API pública no exige registro.
  - **OKX** (`www.okx.com/api/v5/public/...`): funding rate y open interest del perpetuo BTC-USDT, como segunda fuente independiente para verificar que el número de Deribit no es un artefacto de un solo exchange.
  - **`data-api.binance.vision`** (mercado **spot**, no futuros): sigue disponible sin restricción; de ahí sale el precio spot de referencia y la profundidad del libro BTC/MXN.
- **Lo que no se pudo conseguir gratis:** interés abierto agregado multi-exchange (CoinGlass pide API key de pago: `{"code":"30001","msg":"API key missing."}`, verificado hoy) y el feed de liquidaciones en vivo (depende de Binance Futures o de CoinGlass, ambos bloqueados o de pago desde aquí). Se declara como hueco, igual que hace el capítulo 03 con el interés abierto del 10-oct-2025.

## 2. Metodología (declarada antes de calcular)

1. Leer el **funding rate** del perpetuo BTC de Deribit (actual y promedio de 7 y 30 días, anualizado a 3 pagos de 8h × 365) y de OKX (actual, anualizado igual), para verificación cruzada.
2. Leer el **open interest** del perpetuo BTC de Deribit y de OKX (ambos en USD nocional).
3. Calcular la **base (basis)** del futuro con vencimiento fijo más próximo a "trimestral" de Deribit (`BTC-25DEC26`, vence 25-dic-2026, 85.7 días) contra (a) el índice de Deribit y (b) el spot de Binance, anualizada con `basis × 365 / días_a_vencimiento`.
4. Medir la **profundidad del libro BTC/MXN** en Binance spot (`/api/v3/depth`, 200 niveles), con el mismo método que ya usa `lista-senales-de-alerta.md` (E9): notional acumulado a ±0.5% del punto medio, para comparar con la lectura del 25-sep-2026 (18,786 MXN del lado de compra).
5. Todo con una sola corrida de script (sin librerías externas, solo `urllib`/`json`/`statistics`), sello de hora UTC declarado, sin reprocesar después de ver el resultado.

## 3. Resultados (30-sep-2026, ~14:21:44 UTC)

### 3.1 Funding del perpetuo BTC (dos exchanges)

| Fuente | Funding actual (8h) | Anualizado (× 3 × 365) | Ventana adicional |
|---|---|---|---|
| **Deribit** BTC-PERPETUAL | +0.01204% | **+13.2%/año** (instantáneo) | Media de 7 días: +0.00086%/8h → **+0.95%/año**; media de 30 días: +0.0036%/8h → **+3.94%/año** (min −0.0046%, máx +0.030% por periodo de 8h; 13.2% de los 720 periodos de 30 días fueron negativos) |
| **OKX** BTC-USDT-SWAP | +0.00481% | **+5.27%/año** | Premium instantáneo del contrato: **−0.0446%** (el swap cotiza ligeramente *bajo* el índice en este instante, aunque el funding sigue positivo) |

- **Lectura:** funding **positivo pero moderado** en ambos exchanges (0.95-13.2%/año según ventana, sin acercarse a los niveles de estrés de dos dígitos altos o negativos profundos que suelen acompañar euforia o pánico apalancado). El funding negativo aparece en 13.2% de los periodos del último mes (mínimo −0.0046%/8h), lo que indica que hubo tramos cortos con más presión vendedora en perpetuos, coherente con la caída de BTC a ~83,000 el 28-29-sep documentada en la ficha del 29-sep. **No hay señal de apalancamiento largo extremo** que por sí sola anticipe una cascada como la del 10-oct-2025 (que llegó con interés abierto récord y funding positivo persistente, según el capítulo 03).

### 3.2 Open interest del perpetuo BTC (dos exchanges, solo nocional en USD porque no hay agregador gratuito)

| Fuente | OI del perpetuo (USD) | OI del futuro dic-2026 (USD) |
|---|---|---|
| Deribit | **US$793.1 millones** | US$312.6 millones |
| OKX | **US$2,329.2 millones** (27,686 BTC) | — |

- **Límite explícito:** esto **no es el interés abierto total del mercado** (falta Binance, Bybit, CME, Bitget y otros; CoinGlass, que sí los agrega, pide clave de pago). Son dos piezas del mosaico, útiles para ver la dirección del funding y confirmar que no hay una anomalía aislada de un solo exchange, no para calibrar un umbral absoluto de "interés abierto récord" como el que precedió al 10-oct-2025.

### 3.3 Base (basis) del futuro a 85.7 días de Deribit

| Referencia | Base simple | Base anualizada |
|---|---|---|
| Futuro (85,157.55) vs. índice Deribit (84,135.01) | +1.215% | **+5.17%/año** |
| Futuro (85,157.55) vs. spot Binance (84,174.67) | +1.168% | **+4.97%/año** |

- **Contexto:** una tasa libre de riesgo en dólares de corto plazo ronda ~3.5-4% anualizada (Cetes/T-bills a un lado; en EUA la tasa de fondos federales está por debajo de 4% tras el ciclo de bajas de 2025-26). Una base de ~5% está **ligeramente por encima** del puro costo de acarreo (arbitraje de "cash and carry"), consistente con una demanda moderada de posiciones largas apalancadas vía futuros, pero **lejos** de los +20-40% anualizados que se ven en euforia especulativa (ej. finales de 2024) o de una base negativa (contango invertido) típica de pánico. Verificación cruzada: el índice de Deribit (84,135.01) y el spot de Binance (84,174.67) difieren solo 0.05%, así que la base no depende de qué "spot" se use.

### 3.4 Profundidad del libro BTC/MXN en Binance (spot)

| Fecha | Spread | Notional de compra a ±0.5% | Notional de venta a ±0.5% |
|---|---|---|---|
| 25-sep-2026 (bitácora previa) | 0.19% | 18,786 MXN | — |
| **30-sep-2026 (hoy)** | **0.0275%** | **37,274 MXN** | 526,958 MXN |

- El libro de compra se **duplicó** frente al 25-sep y el spread se comprimió 7×. Sigue siendo un libro **delgado en términos absolutos** (decenas de miles de pesos, no millones) frente al libro USDT/MXN (2.4-2.7 millones de MXN por lado, según la ficha de contraparte del 28-sep citada en `lista-senales-de-alerta.md`), lo que **confirma la regla operativa vigente**: si el libro BTC/MXN se vacía en una salida de emergencia, la ruta es vía USDT/MXN, no BTC/MXN directo. No cambia ninguna decisión, pero es la primera medición de seguimiento desde el 25-sep y no muestra deterioro — al contrario, mejoró.

## 4. Verificación numérica (script)

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
days = (1798185600000 - now_ms) / 1000 / 86400
basis_idx  = fut["mark_price"] / fut["index_price"] - 1
basis_spot = fut["mark_price"] / spot - 1
print("anualizado vs indice:", basis_idx * 365 / days, "vs spot:", basis_spot * 365 / days)

week_ms, month_ms = now_ms - 7*86400*1000, now_ms - 30*86400*1000
r7  = [x["interest_8h"] for x in get(f"https://www.deribit.com/api/v2/public/get_funding_rate_history?instrument_name=BTC-PERPETUAL&start_timestamp={week_ms}&end_timestamp={now_ms}")["result"]]
r30 = [x["interest_8h"] for x in get(f"https://www.deribit.com/api/v2/public/get_funding_rate_history?instrument_name=BTC-PERPETUAL&start_timestamp={month_ms}&end_timestamp={now_ms}")["result"]]
print("funding 7d anualizado:", statistics.mean(r7) * 3 * 365, "| 30d:", statistics.mean(r30) * 3 * 365)

okx_fr = float(get("https://www.okx.com/api/v5/public/funding-rate?instId=BTC-USDT-SWAP")["data"][0]["fundingRate"])
print("OKX funding anualizado:", okx_fr * 3 * 365)
```

**Resultado de la corrida completa** (30-sep-2026, 14:21:44 UTC; script y salida cruda en `scratchpad/g5_micro/derivados_deribit_okx.py`, fuera del repo): reproduce exactamente los números de §3.1-§3.3. No usa ninguna librería de terceros; corrido una sola vez, sin reprocesar.

## 5. Contrapuntos y límites

- **Cobertura parcial del mercado.** Solo Deribit y OKX; falta el grueso del volumen de perpetuos de BTC, que históricamente está en Binance (geo-restringido) y Bybit (bloqueado por CDN). Los niveles de funding/OI de hoy **no representan el mercado global**, solo confirman que no hay una anomalía aislada visible en dos exchanges grandes e independientes.
- **CoinGlass, el agregador estándar de la industria para funding/OI/liquidaciones multi-exchange, es de pago desde este entorno** (`API key missing`). Si el comité autoriza una clave de pago en el futuro, esta ficha se puede repetir con cobertura completa.
- **El feed de liquidaciones en vivo no es accesible legalmente y gratis hoy.** Por eso esta ficha no intenta cuantificar liquidaciones de hoy; solo usa el precedente ya documentado del 10-oct-2025 (capítulo 03) como referencia de qué aspecto tiene una cascada real (>US$19 mil M, funding positivo persistente e interés abierto récord antes del evento).
- **Un solo corte en el tiempo.** No hay serie histórica propia de funding/OI de Deribit-OKX construida todavía; sin eso no se puede decir si el funding de hoy es alto o bajo en términos relativos de estos dos exchanges (sí se pudo con la ventana de 30 días de Deribit, que muestra rango de −0.0046% a +0.030% por periodo).
- **Grado B** para los números (reproducibles, dos fuentes independientes, fórmulas estándar de la industria); **grado C** para la lectura de "no hay señal de estrés", porque la cobertura de exchanges es parcial y un solo corte no captura un cambio de régimen intradía.

## 6. Qué cambia para invertir

- **Para la cuenta `arena-claude-binance`:** nada cambia hoy en el filtro de tendencia (que solo mira el precio de BTC/USDT en Binance). El funding y la base de hoy no muestran el patrón de apalancamiento extremo que precedió al 10-oct-2025, lo que es un dato tranquilizador de contexto, no una señal de entrada o salida.
- **Para la vigilancia de contraparte:** la mejora en la profundidad del libro BTC/MXN (37,274 MXN de compra a ±0.5%, contra 18,786 el 25-sep) es una lectura positiva de liquidez operativa, sin que cambie la regla vigente de usar USDT/MXN como ruta de salida principal si el libro BTC/MXN se vacía.
- **Para el plan de estudio:** queda abierta la puerta a que, si el comité autoriza gasto (clave de CoinGlass) o si se libera la geo-restricción de `fapi.binance.com`, esta ficha se repita con el interés abierto agregado real del mercado y con el feed de liquidaciones, que son los dos insumos que de verdad predijeron el 10-oct-2025 según el capítulo 03.

## 7. Autoexamen

- ¿Puedo reproducir el número sin ver la ficha? Sí: tres APIs públicas sin clave (Deribit, OKX, Binance spot) y aritmética estándar de funding anualizado y basis anualizado, documentadas en §4.
- ¿Qué rompería la conclusión? Si Deribit u OKX tuvieran un libro muy delgado que distorsionara su mark price (no verificado a fondo hoy; el volumen de Deribit en las últimas 24h fue de 11,077 BTC según su propio ticker, que es significativo).
- **Grado: B** para el cálculo, **C** para la lectura de ausencia de estrés (cobertura parcial de exchanges, un solo corte de tiempo).

## 8. Estado del pendiente

- Tema 1 de "Temas que no cubren los 35 recursos" (`00-plan-de-estudio.md`): **iniciado con datos en vivo de dos exchanges y profundidad de BTC/MXN, verificado hoy.** Pendiente para una corrida futura: repetir con una clave de CoinGlass (si el comité la autoriza) para tener interés abierto agregado y liquidaciones en vivo; construir una serie propia de funding/OI de Deribit-OKX día a día para poder comparar "hoy" contra su propia historia, igual que ya se hace con MVRV (§4 del capítulo 05).
- Actualiza el capítulo de síntesis `05-mercado-on-chain-stablecoins-e-institucional.md` (adenda fechada 30-sep-2026, §10) y `conocimiento/estado-de-dominio.csv` (fila `cripto/05`).

Script y datos crudos de esta sesión: `scratchpad/g5_micro/` (fuera del repositorio).
