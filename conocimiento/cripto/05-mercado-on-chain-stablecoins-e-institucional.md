# 05 · Mercado, on-chain, stablecoins e institucional (grupo G5)

> **Nivel:** maestría con frontera · **Actualizado:** 9-oct-2026 por `analista-cripto` (adenda §15) · **Grado de evidencia global: C.**
> - Las identidades on-chain (precio realizado, MVRV, NUPL) son exactas y se reproducen con datos gratuitos: grado A-B.
> - Su poder para **predecir** a 1-4 meses es débil o nulo en el rango de hoy: grado C por nuestro propio cálculo.
> - Las narrativas de proveedores con conflicto de interés son grado D.
>
> **Fichas de este grupo:**
> - [05 · The Week On-chain (Glassnode)](recursos/05-the-week-on-chain.md)
> - [26 · State of Crypto 2025 (a16z)](recursos/26-state-of-crypto-2025.md)
> - [30 · Understanding Stablecoins (FMI)](recursos/30-understanding-stablecoins.md)
> - [34 · Charting Crypto Q3 2026 (Coinbase y Glassnode)](recursos/34-charting-crypto-q3-2026.md)
> - [35 · 26 Predictions for 2026 (Galaxy)](recursos/35-26-predictions-for-crypto-in-2026.md)
> - Seguimiento de las 26 predicciones: `arena/investigacion/fuentes-terceros/2026-09-25-galaxy-predicciones-2026.md`
>
> **Examen:** [banco-g5-mercado](examen/banco-g5-mercado.md)
> - **Adenda (29-sep-2026):** [ficha del 29-sep · BTC frente a Nasdaq, USD/MXN y tasa real](fichas/2026-09-29-btc-nasdaq-usdmxn-beta.md), ver §9.
> - **Adenda (30-sep-2026):** [ficha del 30-sep · funding, base e interés abierto en vivo](fichas/2026-09-30-microestructura-funding-basis-oi.md), ver §10.
> - **Adenda (2-oct-2026):** [ficha del 2-oct · flujos de ETF spot como variable de demanda](fichas/2026-10-02-flujos-etf-spot-demanda.md), ver §11.
> - **Adenda (5-oct-2026):** [ficha del 5-oct · beta y correlación de BTC con S&P 500 y oro, 5 años, días de estrés](fichas/2026-10-05-beta-correlacion-oro-sp500.md), ver §12.
> - **Adenda (7-oct-2026):** [ficha del 7-oct · contraste del catalizador macro Irán/Ormuz y derivados durante la caída sostenida](fichas/2026-10-07-catalizador-macro-ormuz-derivados.md), ver §13.
> - **Adenda (8-oct-2026):** [ficha del 8-oct · huracán Isaías vs. Ormuz y primer indicio de flujos de ETF](fichas/2026-10-08-isaias-vs-ormuz-y-flujos-etf.md), ver §14.
> - **Adenda (9-oct-2026):** [ficha del 9-oct · empresas de tesorería de bitcoin (DAT), mNAV y riesgo de venta forzada](fichas/2026-10-09-dat-companies-mnav-riesgo.md), ver §15.

## 0. En una página

- **BTC al 24-sep-2026** (Coin Metrics, cierre UTC):
  - precio **US$84,386.58**;
  - **MVRV 1.5773**;
  - **precio realizado US$53,500.49**;
  - oferta **20,088,857 BTC**;
  - NUPL (sin ajuste por entidad) **0.366**.
  - El MVRV de hoy está en el **percentil 42** de toda su historia y en el 39 desde 2017: valuación "media", ni barata ni cara.
- **Tasas base.** Cuando el MVRV estuvo a ±0.10 del de hoy, el rendimiento a 30, 90 y 120 días **no fue mejor que el de un día cualquiera**:
  - mediana a 120 días de +0.9%, contra +15.4% incondicional;
  - solo 11 episodios independientes;
  - aun sumando la condición "MVRV subiendo", como hoy, la ventaja cabe en el error de muestreo.
- **El 2025 fue de institucionalización y el 2026 la puso a prueba:**
  - los ETF de BTC en EUA llegaron a −US$5.69 mil M en el año (13-jul) y recién volvieron a positivo el 22-sep;
  - las stablecoins crecieron +49.6% en 2025 y solo +1.9% en 2026;
  - al menos cinco DAT vendieron BTC por necesidad o cerraron.
- **Para la cuenta de Binance (solo BTC, filtro SMA200), en resumen:**
  - el on-chain **no contradice** el filtro: la SMA200 está en 70,848 y el costo base STH en ≈ 71.3-71.6 mil. Son casi la misma línea, no dos confirmaciones;
  - el riesgo de tasas pesa más que cualquier señal on-chain;
  - la reserva debe seguir en MXN, no en USDT.

## 1. Mapa del tema, de licenciatura a frontera

| Nivel | Qué hay que dominar | Dónde está |
|---|---|---|
| **Licenciatura** | Diferencia entre capitalización de mercado y realizada. Qué es un ETF o ETP spot y quién custodia. Qué es una stablecoin (7 rasgos, respaldo, canje) | FMI pp. 8-15; a16z láms. 14 y 18-23; Glassnode, guía de realized cap |
| **Maestría: on-chain** | MVRV, precio realizado, NUPL (= 1 − 1/MVRV), SOPR y aSOPR, cohortes STH/LTH (155 días), oferta en ganancia, Puell, flujos a exchanges y sus sesgos de etiquetado | Guías de Glassnode; recurso 34, pp. 18-23; §3-§4 de este capítulo |
| **Maestría: mercado** | Flujos de ETF como demanda marginal, derivados (interés abierto, funding), correlaciones con S&P, oro, DXY y tasas, liquidez en stablecoins | 34, pp. 11-14 y 24; semanas 31-38 de Glassnode; a16z lám. 8 |
| **Doctorado** | Qué predicen de verdad estas métricas: traslape, pocos episodios, revisión de datos, umbrales ajustados en muestra. Dinámica de corridas en stablecoins (arbitrajistas, ventaja del primero). Efecto en los T-bills. Reflexividad de las DAT | §4; FMI pp. 9, 23-24 (Ma-Zeng-Zhang, NBER 33882; Ahmed-Aldasoro, BIS WP 1270) |
| **Frontera, 2026** | Implementación de GENIUS; MiCA; CLARITY (cloture fallida, 15-sep-2026); exención de innovación de la SEC (17-sep-2026); acciones tokenizadas como garantía; consorcios bancarios de stablecoins; x402; riesgo cuántico (6.65 M BTC expuestos) | 30, pp. 40-47; 35 y su seguimiento en `arena`; a16z lám. 40 |

## 2. Las 10 ideas que más importan para invertir

1. **El precio realizado es el costo base agregado; el MVRV mide cuánto se aleja el precio de él. Solo los extremos han dicho algo.**
   - Hoy: MVRV 1.58, precio realizado 53.5 mil.
   - Con MVRV < 1 hubo 7 episodios desde 2011: el rendimiento a 365 días tuvo **mediana de +122.7%** y P(>0) de 99%.
   - En el rango medio de hoy no hay ventaja (§4). **Grado C.**
2. **Los umbrales fijos se degradan.** El pico de MVRV de cada ciclo fue bajando:
   - 7.74 (2011), 5.88 (2013), 4.72 (2017), 3.96 (2021) y 2.78 (2024);
   - el techo de precio del 6-oct-2025 llegó con MVRV de **2.29**;
   - la regla "> 3.5 = techo" de la guía de Glassnode **no se activó** en este ciclo (Coin Metrics).
   - Para detectar un techo, un percentil móvil o un z-score sirve más que un número fijo. [I, nuestra; sin probar todavía]
3. **Los niveles de costo base son mapas de riesgo, no pronósticos.**
   - Niveles vigentes:
     - costo base STH ≈ 71.3-71.6 mil (Glassnode semana 37; BGeometrics 18-sep);
     - True Market Mean 77 mil;
     - costo base de las tesorerías corporativas 80.5 mil;
     - bloque de LTH en 83-86 mil;
     - punto de equilibrio de los ETF ≈ 86 mil;
     - "mean MVRV price" 96.7 mil.
   - Sirven para fijar dónde se invalida una tesis y para dimensionar el riesgo. La semana 38 los usa así.
4. **Los ETF son el comprador marginal y son procíclicos.**
   - Junio de 2026 fue su peor mes registrado (≈ −65.8 mil BTC; Glassnode semana 31), justo en el mínimo (58,525 el 30-jun).
   - En el año llegaron a −US$5.69 mil M el 13-jul y volvieron a positivo el 22-sep: +0.89 mil M con Farside y ≈ +0.32 mil M con Bloomberg.
   - Los flujos **confirman** tendencias, no las anticipan. **Grado C.**
5. **Las stablecoins son la liquidez en dólares del sistema cripto, y en 2026 esa liquidez se estancó.**
   - DefiLlama: 205.9 mil M (fin de 2024) → 308.0 (fin de 2025), **+49.6%**; al 25-sep-2026, 313.9 mil M, **+1.9%** en el año, con pico de 322.4 el 17-may.
   - Sin dólares nuevos, un rally depende de la rotación y de los ETF. La banda de 1.5-2.9% de crecimiento a 30 días de Glassnode es grado C.
6. **La correlación de BTC cambia de régimen y no sirve como supuesto fijo.**
   - 2025: BTC/Nasdaq ≈ 0.47 y BTC/oro ≈ 0.06 (a16z, lám. 8).
   - 2T26: BTC/S&P 0.12 y BTC/oro 0.57 (Coinbase, p. 11).
   - Los reportes coinciden en que lo que manda es la **tasa real y el dólar**: el bono a 10 años de EUA estaba en 4.8% según la semana 36.
7. **Pérdida de paridad: las colas son cortas, pero hay tres mecanismos.**
   - Banco custodio: USDC −12% durante ≈ 2 días en mar-2023.
   - Contagio del ecosistema: USDT con Terra en 2022.
   - Congelamiento de DeFi: Aave al 100% de utilización ≈ 135 horas en abr-2026.
   - El 99% de las desviaciones intradía quedaron dentro de 1% (FMI, p. 16).
   - El minorista no puede canjear: USDT pide un **mínimo de US$100 mil** (FMI, p. 9).
   - **Regla: la reserva va en MXN; USDT se usa solo para cruzar MXN→USDT→BTC.**
8. **Regulación: avanza en dos velocidades.**
   - GENIUS es ley desde el 18-jul-2025, pero se sigue implementando. Por ejemplo, la propuesta de FinCEN y OFAC sobre AML de emisores salió en el Federal Register el 10-abr-2026.
   - El FMI dice que Tether "not subject to a full, independent audit or 1:1 backing… at this time" (p. 44).
   - MiCA es el marco más completo (p. 47).
   - CLARITY **falló** en el Senado (cloture 49-50, 15-sep-2026).
   - La SEC aprobó la **exención de innovación** para acciones tokenizadas (17-sep-2026).
   - El riesgo regulatorio corre para los dos lados; no es solo viento a favor.
9. **Los datos on-chain dependen del proveedor y se revisan después.**
   - Precio realizado y MVRV coinciden entre Coin Metrics, Glassnode y BGeometrics con ±1% de diferencia.
   - Los **flujos a exchanges no coinciden**:
     - el 13-ago-2026, con Coin Metrics, el saldo en exchanges subió 46,954 BTC con un flujo neto de solo +3,192 (reetiquetado);
     - Glassnode veía entradas netas cuando Coin Metrics veía salidas.
   - Solo usamos métricas **reproducibles** (§3). Las propietarias se tratan como contexto.
10. **Los pronósticos de terceros con posiciones son grado D. Las colas pesan más que la narrativa.**
    - Galaxy se calificó 7/23 en 2025. En 2026 lleva 4 cumplidas, 2 fallidas y 20 en curso, con sus predicciones de flujos y precios muy por debajo de la meta.
    - Sus dos fallas fueron de "no pasará nada" y las rompió un evento de cola.
    - Las DAT pasaron de comprador estructural a vendedor forzado. Strategy vendió BTC por primera vez en may-ago-2026, según CoinDesk con base en sus 8-K.

## 3. Receta de datos on-chain gratuitos y reproducibles

### 3.1 Coin Metrics, API comunitaria (sin llave). Probado el 25-sep-2026

- **Endpoint:** `https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets=btc&metrics=PriceUSD,CapMrktCurUSD,CapMVRVCur,SplyCur&frequency=1d&start_time=2010-07-18&page_size=10000`. Hay que paginar con `next_page_url`.
- **Catálogo gratis:** `https://community-api.coinmetrics.io/v4/catalog-v2/asset-metrics?assets=btc`. Lista **31 métricas gratuitas para BTC**, entre ellas:
  - `PriceUSD`, `CapMrktCurUSD`, `CapMVRVCur` y `SplyCur`;
  - `FlowInExNtv/USD`, `FlowOutExNtv/USD` y `SplyExNtv/USD`;
  - `IssTotNtv/USD`, `FeeTotNtv`, `HashRate`, `AdrActCnt`, `TxCnt`, `ROI30d` y `ROI1yr`;
  - `ReferenceRate`, que en todas sus frecuencias (1 s a 1 d) solo cubre los últimos ≈ 7 días.
- **Responden 403 en el plan gratuito:** `CapRealUSD`, `CapMVRVFF`, `CapMrktFFUSD`, `SplyFF`, `NVTAdj`, `RevUSD`, `FeeTotUSD` y `SplyAct1yr`.
- **Métricas que se derivan:**
  - capitalización realizada = `CapMrktCurUSD / CapMVRVCur`;
  - precio realizado = capitalización realizada ÷ `SplyCur` (= `PriceUSD / CapMVRVCur`);
  - NUPL = 1 − 1/MVRV;
  - Puell = `IssTotUSD` ÷ su media de 365 días. Con esto se reproduce el 0.665 (media de 30 días) al 30-jun-2026 del recurso 34, p. 22 ("near 0.7"). Hoy está en 0.995.
- **Límites:**
  - la documentación dice "10 requests per 6 seconds per IP address";
  - el encabezado que observé fue `x-ratelimit-limit: 6000;w=20` (plan "download");
  - la historia completa de 7 métricas bajó en **una sola llamada de 0.59 s** (3.2 MB).
- **Latencia:** el dato del día D, marcado 00:00 UTC, es el cierre del día D UTC. Llega ≈ 02:00-03:00 UTC de D+1.
  - Ejemplo: los flujos del 24-sep se publicaron el 25-sep a las 01:58-02:51 UTC, con estado `flash` y revisables.
  - En hora del centro de México (UTC−6) llega ≈ 20:00-21:00 del mismo día D, así que **todas las corridas de la rutina desde las 00:17 ya ven el cierre del día anterior**.
  - La resolución es diaria, no de 4 horas.
- **Licencia:** CC BY-NC 4.0 (atribución, uso no comercial), según la documentación de Coin Metrics.

### 3.2 Script mínimo (stdlib; copia de trabajo fuera del repo)

```python
import json, statistics, urllib.parse, urllib.request

URL = "https://community-api.coinmetrics.io/v4/timeseries/asset-metrics"
q = {"assets": "btc", "metrics": "PriceUSD,CapMrktCurUSD,CapMVRVCur,SplyCur",
     "frequency": "1d", "start_time": "2010-07-18", "page_size": "10000"}
url, filas = URL + "?" + urllib.parse.urlencode(q), []
while url:  # pagina hasta agotar next_page_url
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "estudio"}), timeout=60) as r:
        d = json.load(r)
    filas += d["data"]
    url = d.get("next_page_url")
s = [(x["time"][:10], float(x["PriceUSD"]), float(x["CapMVRVCur"]), float(x["CapMrktCurUSD"]), float(x["SplyCur"]))
     for x in filas if x.get("PriceUSD") and x.get("CapMVRVCur")]
fecha, precio, mvrv, cap, oferta = s[-1]
cap_real = cap / mvrv                      # CapRealUSD no es gratis: se deriva
print(fecha, f"precio {precio:,.2f} | MVRV {mvrv:.4f} | precio realizado {cap_real / oferta:,.2f} | "
      f"NUPL {1 - 1 / mvrv:.3f} | oferta {oferta:,.0f}")
for h in (30, 90, 120):                    # tasa base: dias con MVRV a +-0.10 del de hoy
    r = [s[i + h][1] / s[i][1] - 1 for i in range(len(s) - h) if abs(s[i][2] - mvrv) <= 0.10]
    print(f"{h} d: n={len(r)} (traslapados) mediana {statistics.median(r):+.1%} P(>0) {sum(x > 0 for x in r) / len(r):.0%}")
```

- **Salida del 25-sep-2026:** `2026-09-24 precio 84,386.58 | MVRV 1.5773 | precio realizado 53,500.49 | NUPL 0.366 | oferta 20,088,857`.
- **Tasa base:** a 30 días, n=581, mediana +1.7%, P(>0) 54%. A 90 días, +0.0% y 50%. A 120 días, +0.9% y 51%.
- **Versión completa:** en el scratchpad de la sesión (`g5/onchain_coinmetrics.py`) está la versión con flujos a exchanges, submuestra sin traslape, conteo de episodios, variantes desde 2017 y "MVRV subiendo", y salida a CSV. **No está en el repo.** Si la rutina la adopta, primero debe pasar la revisión de código del sistema.

### 3.3 Alternativas y huecos

| Fuente | Qué da gratis | Límites (verificados el 25-sep-2026) |
|---|---|---|
| **BGeometrics** (`bitcoin-data.com/v1/<métrica>/last`) | Precio realizado del STH, SOPR, STH-SOPR, MVRV, precio realizado y NUPL | **10 llamadas por hora y 15 al día.** Los últimos 7 días requieren suscripción, así que el dato gratis llega **con ≈ 7 días de retraso** (último: 18-sep). Úsala 1 vez al día, en la corrida de las 08:17 |
| **DefiLlama** (`stablecoins.llama.fi/stablecoincharts/all`) | Oferta total de stablecoins diaria desde 2017 | Sin llave. El endpoint de tasas de préstamo de `yields.llama.fi` es **de pago** (402); `yields.llama.fi/chart/<pool>` sí es gratis |
| **CoinGecko** (`api.coingecko.com/api/v3/coins/categories`) | Capitalización por categoría (stablecoins, USD, privacidad, "GENIUS Act compliant") | Límite de llamadas bajo |
| **mempool.space** | Hashrate, comisiones y bloques | Sin llave |
| **Flujos de ETF** | — | **Hueco.** Farside respondió 403 y el proxy bloqueó `api-v2.sosovalue.com`. Por ahora hay que tomarlos de notas de prensa que citen Farside o Bloomberg, con fecha y fuente |
| **Cohortes por entidad, True Market Mean, costo base de ETF y tesorerías** | — | Son de Glassnode, de pago. Se leen en el boletín como contexto (grado C-D) |

### 3.4 Cifras de hoy y comparación con los reportes 34 y 05

| Métrica | Coin Metrics (gratis) | Glassnode o Coinbase | Otra fuente gratis | Diferencia |
|---|---|---|---|---|
| MVRV al 30-jun-2026 | 1.103 | "approached 1" (34, p. 19) | — | Coherente |
| Precio realizado al 30-jun-2026 | 53,070 | ≈ 53 mil (34, p. 19, lectura de gráfica) | — | < 1% |
| Precio realizado, ≈ 10-ago | 52,720 | ≈ 52.8 mil (Glassnode semana 32) | — | 0.15% |
| Precio realizado al 18-sep | 53,247.55 | — | 52,850.93 (BGeometrics) | 0.75% |
| MVRV al 18-sep | 1.5201 | — | 1.5305 (BGeometrics) | 0.010 |
| NUPL al 18-sep | 0.342 (sin ajuste por entidad) | — | 0.3466 (BGeometrics) | 0.004 |
| "Mean MVRV price" al 21-sep | 96,726 (MVRV medio desde 2011 = 1.812) | 96.7 mil (Glassnode semana 38) | — | Coincide, pero **depende de la ventana**: 91.9 mil desde 2014 y 104.7 mil desde 2010 |
| Puell (media de 30 días) al 30-jun | 0.665 | "near 0.7" (34, p. 22) | — | Coherente |
| Costo base STH | No disponible | 71.3 mil (semana 37, dato del 15-sep) | 71,636 (BGeometrics, 18-sep) | 0.5% |
| Oferta de BTC al 30-jun | 20,050,326 | 20.05 M (34, p. 16) | — | Igual |

**Precio nunca debajo del precio realizado en 2026:** con Coin Metrics, el MVRV mínimo del año fue 1.103, el 30-jun. Coincide con Glassnode (semana 38: "never closed below the Realized Price") y con la NUPL siempre positiva.

## 4. Tasas base: qué hizo BTC después de un MVRV como el de hoy

**Método (cálculo propio, dos implementaciones independientes: stdlib y pandas, con los mismos resultados):**
- **Datos:** Coin Metrics diario del 18-jul-2010 al 24-sep-2026, 5,913 días.
- **Estado de hoy:** MVRV = 1.5773 (24-sep-2026).
- **Condición:** días con MVRV en [1.477, 1.677], es decir, ±0.10.
- **Resultado medido:** rendimiento del precio a 30, 90 y 120 días.
- **Comparación:** el rendimiento incondicional de todos los días del mismo periodo.

**⚠ Traslape:**
- Los días consecutivos comparten casi toda su ventana futura, así que las "n días" **no son independientes**.
- Reporto también:
  - la submuestra **sin traslape**: tomo un día y salto h días;
  - los **episodios**: rachas en la banda separadas por más de h días.
- Con 15 observaciones independientes, el error estándar de una proporción cercana a 50% es ≈ **12.9 pp**. Diferencias de ±10 pp en P(>0) son **ruido**.

### 4.1 Historia completa, solo con la banda de MVRV

| Horizonte | n días (traslapados) | Sin traslape | Episodios | Mediana | Media | P(>0) | p10 | p90 | P(≤ −20%) | Incondicional (mediana / P>0) |
|---|---|---|---|---|---|---|---|---|---|---|
| 30 d | 581 | 43 | 25 | +1.7% | +0.4% | 54% | −23.4% | +23.1% | 16% | +3.2% / 57% |
| 90 d | 578 | 24 | 15 | −0.0% | +5.6% | 50% | −29.3% | +56.2% | 30% | +12.8% / 61% |
| 120 d | 578 | 22 | 11 | +0.9% | +20.0% | 51% | −42.3% | +77.6% | 25% | +15.4% / 63% |

### 4.2 Banda y "MVRV subiendo contra hace 90 días" (así está hoy: 1.127 el 26-jun → 1.577)

| Horizonte | n días | Sin traslape | Episodios | Mediana | P(>0) | p10 | p90 | P(≤ −20%) |
|---|---|---|---|---|---|---|---|---|
| 30 d | 230 | 23 | 18 | −0.8% | 47% | −23.7% | +27.0% | 14% |
| 90 d | 227 | 15 | 11 | +8.8% | 59% | −39.9% | +36.1% | 20% |
| 120 d | 227 | 14 | 9 | +13.1% | 69% | −35.9% | +65.1% | 14% |

- La mediana **sin traslape** es de +1.6% a 90 días y +10.3% a 120 días.

### 4.3 Desde 2017, solo con la banda (la era con ETF y derivados maduros se parece más a hoy)

| Horizonte | n días | Sin traslape | Episodios | Mediana | P(>0) | Incondicional (mediana / P>0) |
|---|---|---|---|---|---|---|
| 30 d | 402 | 28 | 15 | −0.7% | 47% | +2.2% / 55% |
| 90 d | 399 | 15 | 9 | −10.0% | 40% | +7.1% / 57% |
| 120 d | 399 | 13 | 6 | −3.6% | 43% | +5.8% / 56% |

### 4.4 Sensibilidad y extremos

- **La conclusión cambia de signo con supuestos razonables. Es frágil.** Por ejemplo, la mediana a 120 días con historia completa:
  - banda ±0.05: −3.4% (P>0 48%);
  - banda ±0.05 y "subiendo": +30.9% (P>0 78%), pero solo con 11 observaciones independientes;
  - banda ±0.15: +5.2% (P>0 56%).
- **Extremos:**
  - MVRV < 1: 775 días en **7 episodios** (2011, 2012, 2014, 2014-15, 2018-19, mar-2020 y 2022-23). A 365 días, mediana **+122.7%**, P(>0) 99% y el peor caso −27.2%.
  - Desde 2017 (3 episodios): mediana +91.9% y el peor caso +13.5%.
  - MVRV > 3: los episodios de 2010-2013 dominan la muestra y a 365 días dieron **mediana positiva** (+219.8%). Es la prueba de que la muestra temprana contamina las reglas de "techo".
- **Conclusión para la temporada del 28-sep-2026 al 28-ene-2027 (≈ 120 días):**
  - [I, nuestra] El MVRV de hoy **no da ventaja direccional**. La distribución a 120 días es ancha: p10 de −36 a −42% y p90 de +65 a +78%.
  - P(caída ≥ 20% al cierre del horizonte) fue de 14-25%. Este dato es a horizonte fijo, **no** la probabilidad de tocar −20% en algún momento, que es mayor.
  - Esto apoya la decisión del comité: la cuenta se juega por **supervivencia** (filtro, reserva en MXN y cortacircuitos), no por señales on-chain.
  - Estado de la idea: **replicado internamente, grado C.**

## 5. Stablecoins: liquidez, paridad y regulación

- **Tamaño y concentración al 25-sep-2026:**
  - DefiLlama: US$313.9 mil M.
  - CoinGecko, categoría "Stablecoins": US$292.7 mil M, con USDT 183.75 (62.8%) y USDC 75.26 (25.7%).
  - Glassnode (semana 37): ≈ 301 mil M.
  - Las diferencias de hasta ≈ 7% vienen de qué monedas cuenta cada proveedor. **Usa siempre la misma serie** (DefiLlama en la rutina).
- **Monedas:** el USD es 97% según el FMI (p. 15), 99.8% según a16z con Artemis (lám. 23) y 99.1% según la categoría de CoinGecko de hoy. Las stablecoins en MXN suman ≈ US$0.26 M.
- **Uso:**
  - ≈ 80% de las transacciones son de bots (FMI, p. 14);
  - los pagos transfronterizos crecen: ≈ US$1.5 billones en 2024 (FMI, p. 17);
  - en feb-2026, con Artemis, el volumen mensual superó al de ACH (ficha 35, #9).
- **Riesgo para nuestra cuenta** (el comité ya lo decidió; aquí queda el fundamento):
  - el minorista no puede canjear (mínimo de US$100 mil en USDT);
  - las pérdidas de paridad son cortas pero reales;
  - DeFi puede congelar liquidez;
  - Tether no tiene auditoría completa (FMI, p. 44). **Adenda (25-sep-2026, G4):** desactualizado desde el 13-ago-2026; Tether tiene una opinión sin salvedades de KPMG EUA sobre 2025. No cambia la decisión de reserva en MXN: ver `conocimiento/cripto/04-riesgos-fraude-hackeos-y-seguridad.md`, contradicción #11.
  - **Por eso la reserva va en MXN.**
- **Regulación:**
  - GENIUS: reservas líquidas, sin intereses, emisores extranjeros con régimen comparable, bancos solo por medio de una subsidiaria (FMI, pp. 40-44).
  - MiCA: capital de al menos 2% de las reservas (3% si el emisor es significativo, con un piso de €350 mil), ≥ 30% en efectivo o equivalentes (60% si es significativo) y prohibición de pagar intereses también a los CASP (FMI, pp. 42-43, notas 78-79).
  - En México se aplica la Circular 4/2019 de Banxico; ver la decisión del comité del 25-sep-2026.

## 6. Contradicciones entre recursos

| Tema | Recurso A | Recurso B | Cómo se resuelve |
|---|---|---|---|
| Correlación de BTC | a16z: BTC/Nasdaq ≈ 0.47 y BTC/oro ≈ 0.06 en 2025 (lám. 8) | Coinbase: BTC/S&P 0.12 y BTC/oro 0.57 en 2T26 (p. 11) | No es error sino cambio de régimen. No fijar un "papel" para BTC |
| Proporción USD de las stablecoins | FMI 97% (p. 15) | a16z 99.8% (lám. 23); CoinGecko hoy 99.1% | Cambia el universo de monedas contado |
| USDT + USDC | FMI ≈ 90% (p. 14) | a16z 87% (web); CoinGecko hoy 88.5% | Igual; fecha y universo distintos |
| "Volumen ajustado" de stablecoins | a16z/Allium: US$9 billones en **12 meses** a sep-2025 (lám. 18) | Artemis: US$7.2 billones en **un mes** (feb-2026) | Definiciones de "ajuste" incompatibles, ≈ 10× de diferencia. Compara solo dentro de una misma fuente |
| Oferta de stablecoins en el 2T26 | Coinbase: "record highs" (p. 8) | La gráfica del mismo reporte muestra crecimiento a 30 días negativo al 30-jun (p. 14) | Las dos son ciertas: pico de 322.4 mil M el 17-may y −3.5% al 30-jun (DefiLlama) |
| Oferta de stablecoins hoy | DefiLlama 313.9 mil M | CoinGecko 292.7; Glassnode ≈ 301 | Diferencias de metodología |
| Flujos a exchanges | Glassnode: entradas netas la mayoría de los días de 2026 (semana 32) | Coin Metrics: salidas netas todos los meses de jun a sep (−141.8 mil BTC entre jul y sep) mientras el saldo **subía** | Las etiquetas difieren y hay reetiquetados (+46,954 BTC el 13-ago). La métrica no sirve como señal |
| Momento del ciclo | Coinbase: "top almost certainly… October 2025" y "bottoming process" (pp. 4 y 9) | Glassnode semana 33 (19-ago): "The bottoming process is underway, exhaustion is not" | Son compatibles. Ninguno se comprometió con una fecha y los dos dejan la tesis abierta |
| Adopción de stablecoins | a16z: "will accelerate" (lám. 53) | 2026: oferta +1.9% en el año (DefiLlama), aunque el volumen sí creció | Pronóstico fallido en oferta; en volumen, depende de la fuente |
| Estado de la regulación | a16z: "bipartisan consensus", CLARITY en camino (web) | Cloture fallida 49-50 el 15-sep-2026 | El pronóstico de a16z no se cumplió en 2026 |

## 7. Qué no pude consultar

- El tablero interactivo de a16z. El reporte y las láminas sí los revisé completos.
- El archivo completo de The Week On-chain de 2020-2026: leí las 8 ediciones de ago-sep-2026 sin las gráficas, más 9 guías de métricas.
- Glassnode Studio y su API, que son de pago.
- Las páginas HTML del FMI y de elibrary, bloqueadas por el CDN. El PDF oficial sí lo obtuve.
- **Flujos de ETF desde la fuente:** Farside respondió 403 y SoSoValue estaba bloqueado por el proxy. Usé notas de prensa que citan Farside o Bloomberg.
- La tasa de **préstamo** histórica de Aave en DefiLlama, que es de pago. Usé la tasa del depositante como cota inferior.
- **Datos que no encontré:**
  - acumulado de 2026 de los ETF de ETH y de altcoins;
  - número exacto de ETF cripto lanzados en 2026;
  - capitalización de "Internet Capital Markets" en Solana;
  - volumen de liquidación transfronteriza de Visa en dólares;
  - total de tesorerías gobernadas por futarquía.

## 8. Siguientes pasos para la rutina 8

1. **Corrida de las 08:17:** correr la receta de §3.2. Anotar en el pulso MVRV, precio realizado y distancia a la SMA200, más el costo base STH de BGeometrics (1 llamada).
2. **Semanal (miércoles):** leer la edición de The Week On-chain y anotar solo los niveles reproducibles.
3. **Pendientes de verificación:**
   - probar si un **percentil móvil de MVRV** mejora la señal de techos fuera de muestra, con pre-registro;
   - fuente estable para flujos de ETF;
   - calificación final de Galaxy el 31-dic-2026.

## 9. Adenda (29-sep-2026): beta y correlación de BTC con el Nasdaq y con la tasa real, en MXN

Cálculo propio (ficha completa: [fichas/2026-09-29-btc-nasdaq-usdmxn-beta.md](fichas/2026-09-29-btc-nasdaq-usdmxn-beta.md)), motivado por el tema 3 de "temas que no cubren los 35 recursos" (`00-plan-de-estudio.md`) y por la caída conjunta de hoy de BTC (~−1.3%) y el Nasdaq, con el 10 años nominal en su nivel más alto desde 2007.

- **Muestra completa (2 años, 444 días hábiles comunes, Yahoo Finance):** correlación BTC(USD)-QQQ(USD) = **0.424**, beta = **0.886**; en MXN, correlación 0.441 y beta 0.936. BTC-USD/MXN: correlación débil, −0.066.
- **Rodante de 90 días:** hoy la correlación con el Nasdaq (0.322) y la beta (0.602) están **por debajo** de su mediana de 2 años (0.491 y 1.046); nunca se ha vuelto negativa (mín. 0.142) — a diferencia de BTC-DXY, que sí cambia de signo (ficha del 28-sep-2026).
- **Últimos 30 días:** beta = **1.580**, muy por encima de la mediana de 2 años: régimen de "beta alta" reciente, aunque la correlación (0.454) no es excepcional.
- **Tasa real (FRED DFII10):** subió de 2.18% (19-may) a 2.83% (25-sep-2026). Correlación de su cambio diario con el retorno diario de BTC: ≈0 en la muestra completa (−0.005), pero −0.232 en los últimos 90 días — el canal "tasa real más alta presiona a BTC" tiene el signo correcto hoy, pero no es estable en 2 años de historia.
- **Conclusión aplicada:** confirma la idea #6 de este capítulo (la correlación de BTC cambia de régimen) con cálculo propio y con la versión en MXN que faltaba, y añade que el acoplamiento con el Nasdaq de hoy **no** está en un extremo histórico pese a la narrativa de prensa. No cambia el filtro de tendencia de la cuenta (solo mira el precio de BTC). **Grado B** para el cálculo, **C** para su uso predictivo (mismo patrón de inestabilidad que el resto del capítulo).

## 10. Adenda (30-sep-2026): funding, base e interés abierto en vivo, con la API de futuros de Binance geo-restringida

Cálculo propio (ficha completa: [fichas/2026-09-30-microestructura-funding-basis-oi.md](fichas/2026-09-30-microestructura-funding-basis-oi.md)), motivado por el tema 1 de "temas que no cubren los 35 recursos" (`00-plan-de-estudio.md`): *funding, base, interés abierto, cascadas de liquidación y profundidad de pares MXN*. La cascada de liquidaciones del 10-oct-2025 ya está documentada en el capítulo `03-defi-mecanica-riesgos-y-academia.md` §4; aquí solo se completa la parte de derivados en vivo que faltaba.

- **`fapi.binance.com` confirmado geo-restringido hoy** (los tres endpoints de futuros probados devuelven "Service unavailable from a restricted location"); `api.bybit.com` también bloqueado por CDN. Fuentes usadas en su lugar, públicas y sin clave: **Deribit** y **OKX** (perpetuos BTC), más `data-api.binance.vision` para el spot y la profundidad de BTC/MXN.
- **Funding del perpetuo BTC:** Deribit +13.2%/año instantáneo (media de 7 días +0.95%/año; de 30 días +3.94%/año, con 13.2% de periodos negativos); OKX +5.27%/año instantáneo. Positivo pero moderado en ambos: no hay señal de apalancamiento largo extremo como el que precedió al 10-oct-2025 (funding positivo persistente e interés abierto récord, según el capítulo 03).
- **Base del futuro a 85.7 días de Deribit:** +5.17%/año contra el índice de Deribit y +4.97%/año contra el spot de Binance (difieren apenas 0.05% entre sí). Es un carry ligeramente por encima de la tasa libre de riesgo en dólares, sin señal de euforia (+20-40%/año) ni de pánico (base negativa).
- **Open interest:** Deribit US$793.1 M (perpetuo) + US$312.6 M (futuro dic-2026); OKX US$2,329.2 M (27,686 BTC). Cobertura parcial (falta Binance y Bybit, geo-restringidos; CoinGlass, el agregador estándar, pide clave de pago), así que sirve para descartar una anomalía aislada, no para fijar un umbral absoluto de "récord".
- **Profundidad de BTC/MXN en Binance:** notional de compra a ±0.5% subió de 18,786 MXN (25-sep) a 37,274 MXN (30-sep), con spread de 0.0275% (vs. 0.19%). Mejora, sin cambiar la regla de usar USDT/MXN como ruta de salida si el libro BTC/MXN se vacía.
- **Grado B** para los números, **C** para la lectura de "sin señal de estrés" (cobertura parcial de exchanges, un solo corte de tiempo). No cambia ninguna decisión de la cuenta `arena-claude-binance`.

## 11. Adenda (2-oct-2026): flujos de ETF spot como variable de demanda

Cálculo propio (ficha completa: [fichas/2026-10-02-flujos-etf-spot-demanda.md](fichas/2026-10-02-flujos-etf-spot-demanda.md)), motivado por el tema 4 de "temas que no cubren los 35 recursos" (`00-plan-de-estudio.md`): *flujos de los ETF spot como variable de demanda*. El acceso directo a la API de flujos sigue bloqueado hoy (Farside 403, SoSoValue 403/sin respuesta, CoinGlass gratis con error 500 interno), igual que documenta §3.3 y §7 de este capítulo; la novedad de hoy es (a) una reconciliación de una discrepancia real de fecha entre fuentes de prensa y (b) el primer ejercicio numérico propio que convierte el flujo en USD a BTC equivalente y lo compara con el precio y el volumen.

- **Mecanismo:** los ETF spot de BTC en EUA crean/redimen en efectivo (un participante autorizado entrega dólares, el emisor compra BTC en el mercado abierto y entrega acciones), a diferencia de un fondo cerrado con descuento/premio. Por eso el flujo neto debería reflejar, con rezago de liquidación de T+1-T+2, compra o venta real de BTC — pero es una variable **coincidente o con rezago corto**, no líder, consistente con la idea 4 de §2.
- **Discrepancia de fecha resuelta:** una nota (CryptoTimes) etiquetó "−149M USD el 1-oct" citando un corte de SoSoValue a las 18:00 UTC (14:00 hora de Nueva York, mercado de EUA aún abierto); en realidad esa cifra es el cierre del **30-sep**, confirmada por 4 fuentes de prensa independientes (The Block, Chaincatcher, Panews, Bloomingbit) con una desviación máxima entre ellas de solo 0.21%. El flujo real del **1-oct** fue **+US$103M** (IBIT +196M, FBTC −60.73M, GBTC +14.59M, según KuCoin/ME News vía SoSoValue).
- **Ejercicio numérico (verificado dos veces, script en `scratchpad/g5_etf/flujos_etf_vs_precio.py`):** el outflow del 30-sep (−148.7M USD) equivale a **−1,778.2 BTC** al precio de ese día (−7.76% del volumen de 24h de Binance spot, un solo exchange); el inflow del 1-oct (+103.0M USD) equivale a **+1,213.5 BTC** (+5.30% del mismo volumen de referencia). Para contexto de magnitud, el peor mes de 2026 (junio, −65,800 BTC) promedia −2,193 BTC/día, del mismo orden que el 30-sep: el día "malo" de esta semana no es atípico.
- **Lectura con n=2 (grado D si se usa para predecir):** el día de salida neta el precio quedó plano (−0.05%) y el día de entrada neta subió +1.50%. Dirección consistente, pero el tamaño de muestra no permite ninguna conclusión; es el inicio de una serie que la rutina puede seguir acumulando.
- **Regla operativa nueva para el pulso:** verificar la fecha de un flujo de ETF citado por una sola nota de prensa contra una segunda fuente antes de usarlo, porque un corte intradía citado como "de hoy" puede en realidad ser el cierre del día anterior.
- **Grado B** para los números de flujo y precio; **grado D** para cualquier lectura predictiva del cruce flujo-retorno con esta muestra. No cambia ninguna decisión de la cuenta `arena-claude-binance` (el filtro de tendencia solo mira precio).

## 12. Adenda (5-oct-2026): beta y correlación de BTC con el S&P 500 y el oro, ventana de 5 años, con análisis de días de estrés

Cálculo propio (ficha completa: [fichas/2026-10-05-beta-correlacion-oro-sp500.md](fichas/2026-10-05-beta-correlacion-oro-sp500.md)), que avanza el pendiente que dejó la ficha del 29-sep-2026 (§8 de esa ficha y fila cripto/05 de `estado-de-dominio.csv`): extender la ventana más allá de 2 años y agregar oro y S&P 500 al cruce con BTC.

- **Muestra completa de 5 años (1,107 retornos diarios comunes, 2021-10-06 a 2026-10-05, Yahoo Finance):** correlación BTC(USD)-S&P 500(USD) = **0.438**, beta = **1.359** (más alta que la beta de 2 años sobre el Nasdaq de la ficha del 29-sep, 0.886). Correlación BTC(USD)-oro(USD) = **0.123**, beta = **0.343**: sin acoplamiento estable con el oro en 5 años. En MXN: correlación BTC-S&P 500 0.424, beta 1.257.
- **Rodante de 90 días sobre 5 años (1,017 ventanas, no solo 355):** mediana de correlación con el S&P 500 de 0.468 (rango −0.131 a 0.746) — **corrige a la ficha del 29-sep, que con solo 2 años de historia no vio ninguna ventana con correlación negativa frente al Nasdaq; con 5 años sí hay un 7.2% de ventanas negativas.** La correlación BTC-oro de la última ventana (0.448) está muy por encima de su mediana histórica (0.098): régimen reciente de mayor acoplamiento con el oro, sin que sea un parámetro estable.
- **Por año calendario:** 2022 (ciclo de alzas de la Fed y colapso de Terra/FTX) tuvo la correlación BTC-S&P 500 más alta del quinquenio (0.646), muy por encima de 2023-2026 (0.07-0.45).
- **Nuevo: condicionado a días de estrés del S&P 500** (retorno diario ≤ −1%, n=162 de 1,254 días): BTC cayó en promedio **−2.43%** esos días (contra +0.47% en un día normal) y su correlación con el S&P 500 fue **más alta**, no más baja (0.333 vs 0.293): no hay evidencia de que BTC diversifique en promedio cuando más se necesita. En los **10 peores días** del S&P 500 de 5 años, el patrón depende del tipo de choque: en el choque arancelario de abril de 2025 BTC **subió** (+0.89%, +0.75%) mientras el índice y el oro caían; en los 6 peores días de 2022 (Fed + congelamiento de Celsius) BTC **amplificó** la caída, llegando a **−22.68% en un solo día** (13-jun-2022) con el S&P 500 en "solo" −3.88%.
- **Aplicación al comité del 9-oct-2026** (BTC 40%→65% de `arena-claude-binance`, con la cuenta GBM ya en UPRO 3x desde la decisión W40): el escenario de cola más relevante no es "BTC diversifica una caída del S&P 500", sino un choque tipo 2022 que golpee a las dos cuentas a la vez con la cripto cayendo proporcionalmente más. Verificado dos veces (Python puro y NumPy, coinciden a 3-4 decimales). **Grado B** para el cálculo, **C** para la lectura de comportamiento en choques (descansa en solo 2 episodios distintos). No cambia el filtro de tendencia (solo mira precio de BTC).

## 13. Adenda (7-oct-2026): contraste del catalizador macro Irán/Ormuz y derivados en vivo durante la caída sostenida

Cálculo propio (ficha completa: [fichas/2026-10-07-catalizador-macro-ormuz-derivados.md](fichas/2026-10-07-catalizador-macro-ormuz-derivados.md)), que pone a prueba con datos en vivo la hipótesis de inteligencia (`bitacora/inteligencia/2026-10-07.md`) de que la caída sostenida de BTC/ETH del 6-7 de octubre se transmite desde un shock de petróleo por la escalada Irán/Ormuz.

- **El petróleo sí se movió** (Brent +3.86%, WTI +3.19% entre el mínimo del 6-oct 12:00 UTC y esa misma noche; una vela diaria lo esconde, hace falta la vela horaria), pero con **6-13 horas de desfase** frente al tramo más fuerte de la caída de BTC (−2.90% entre las 20:00 UTC del 6-oct y las 14:00 UTC del 7-oct, justo cuando el petróleo ya estaba plano). Pesa contra una transmisión mecánica e instantánea.
- **El resto del complejo macro no tiene la firma de un "risk-off" de manual:** VIX casi inmóvil (15.00→15.86 en 48 horas), 10 años plano (rango de 9 puntos base), dólar (DXY) solo +0.63%, y el **oro cayó junto con BTC** (−1.88%) en vez de actuar como refugio. BTC/ETH cayeron más que cualquier otro activo del cruce.
- **Derivados de BTC en vivo (Deribit y OKX, mismo método que la adenda §10) durante la caída, no en calma:** funding positivo y moderado en ambos exchanges (Deribit +4.05%/año a 30 días, con 8.9% de periodos negativos; OKX +1.74%/año), base del futuro de diciembre casi igual a la de hace una semana (+4.9-5.2%/año) y open interest de Deribit incluso **subiendo** (US$793→841 M). **Sin firma de cascada de liquidaciones apalancadas** como la del 10-oct-2025; más consistente con venta ordenada de spot.
- **Verificación de la cita de inteligencia (Chicago Fed, wp2026-16):** el paper existe y es real ("Crypto Is Coming of Age: The Case of Bitcoin's Rising Beta", Drexler, Guettler y Sun), y documenta que la beta de BTC frente a acciones (NASDAQ/Dow) creció desde 2020 y responde al sentimiento accionario general. **No menciona petróleo ni Ormuz**: es evidencia legítima de "BTC amplifica riesgo general", no del canal petróleo-específico que se le atribuyó. El pendiente de buscar un paper 2025-2026 sobre transmisión de shocks petroleros geopolíticos puntuales a BTC (abierto desde el 28-sep, `estado-de-dominio.csv` fila cripto/01) **sigue sin resolverse**; se encontró `arXiv:2409.17057` sobre volumen (no precio) de BTC y riesgo geopolítico, que no lo cierra.

## 14. Adenda (8-oct-2026): segundo catalizador de petróleo (huracán Isaías) sometido a la misma prueba de timing, y primer indicio cripto-específico (flujos de ETF)

Cálculo propio (ficha completa: [fichas/2026-10-08-isaias-vs-ormuz-y-flujos-etf.md](fichas/2026-10-08-isaias-vs-ormuz-y-flujos-etf.md)), motivada por un catalizador de petróleo **nuevo y distinto** confirmado hoy por el dueño (`datos/entrada-dueno/2026-10-08.md`): el huracán Isaías (climático, no geopolítico), que se volvió huracán la madrugada del 8-oct y subió el Brent de forma clara y acelerada (+3.58% entre las 00:00 y las 14:00 UTC de hoy).

- **Filtro de tendencia: sin "roll" por segundo día consecutivo.** SMA200 = 71,765.23 (idéntica a la vigente desde la cascada del 7-oct), salida = 69,612.27, reentrada = 73,918.18 — la vela diaria de hoy (8-oct) todavía no cierra, así que la ventana de 200 cierres completos no cambió desde ayer. Colchón sobre la salida con el precio en vivo (82,492.01): **+18.50%**, reduciéndose de forma gradual con el precio (no con un salto del nivel de salida). **ENCENDIDO, sin caso límite.**
- **Timing Isaías vs. BTC (correlación horaria, n=33 pares, 7-oct 04:00 a 8-oct 14:00 UTC, verificado dos veces con `statistics` y `numpy`, coinciden a 3 decimales):** correlación contemporánea r=−0.03, correlación con el Brent liderando 1 hora r=−0.12 (signo correcto pero magnitud indistinguible de ruido con esta muestra). El Brent sube de forma monótona desde la medianoche UTC de hoy, pero el peor tramo de BTC de hoy (09:00-13:00 UTC, −1.13%) ocurre precisamente cuando el Brent está plano, y BTC incluso se recupera entre 05:00-09:00 UTC mientras el Brent acelera más fuerte. **Misma conclusión que con Ormuz ayer: el shock de petróleo (este u otro) no pasa la prueba de coincidencia intradía con BTC.** Dos catalizadores externos distintos, dos veces el mismo resultado de timing.
- **Resto del complejo macro, tampoco risk-off hoy:** VIX 15.08→15.40 (+2.1%), Nasdaq 27,538.69→27,473.50 (−0.24%), 10 años sin cambio (5.277%→5.278%). Derivados BTC (Deribit) estables: funding positivo moderado, OI US$824.84M dentro del rango de los últimos 4 pulsos del día (US$821.6-839.3M). Sin firma de cascada ni de pánico accionario generalizado.
- **Primer indicio cripto-específico que sí calza en timing y magnitud: flujos de ETF spot BTC.** Con `tftc.io/bitcoin-etf-flows/october-2026` (SoSoValue/Farside): 1-oct +102.7M, 2-oct +189.8M, 5-oct −89.9M, 6-oct +118.9M, **7-oct −487.1M** (salida amplia: IBIT −207.7M, FBTC −105.1M, ARKB −101.7M, GBTC −39.3M, BITB −27.6M — no concentrada en un solo fondo). Suma acumulada de octubre al 7-oct: **−165.6M USD** (verificado dos veces), negativa por primera vez el mes tras el outflow del 7-oct. El 7-oct fue también el día del tramo de caída más fuerte de BTC de toda la racha (ficha del 7-oct, §3): es el primer dato de la semana simultáneo y proporcional en magnitud a la caída de precio, a diferencia de los dos catalizadores de petróleo. No establece causalidad con n=1 (un ETF que crea/redime en efectivo reacciona al precio tanto como lo mueve), pero es la pista más prometedora para seguir.
- **Contraparte (TVL DefiLlama):** US$172.37 mil millones (8-oct, 12:41 UTC) vs. US$177.42 mil millones (7-oct 00:00 UTC), −2.85%, del mismo orden que la caída de precio de BTC en la misma ventana (~−3.4%): **sin señal de salida neta de unidades por encima del efecto precio**, mismo patrón que el 7-oct. E3/E5/E6/E10 no se repitieron hoy con búsqueda dirigida (prioridad de tiempo en el catalizador de Isaías); se declara explícitamente, no se afirma "limpio" sin haberlo revisado.
- **P0077 y P0083 (pronósticos abiertos) muy cerca de resolverse:** precio en vivo (82,492.01) a solo +0.60% del umbral de 82,000 de P0077 (mínimo intradía de hoy ya tocó 81,773.43, aunque en Binance, no en el índice FRED/Coinbase que usa el pronóstico); P0083 (cierre Yahoo del 8-oct < 83,239.49) con dirección clara a favor del "SÍ" dado el rango de precio de todo el día (82,182-83,370).
- **Grado B** para los datos de precio, Brent y derivados; **C** para la lectura comparativa Isaías-vs-Ormuz (n=2 episodios) y para el dato de flujos de ETF (un solo agregador, sin segunda fuente de prensa cruzada hoy); **D** para cualquier intento de atribuir causalidad (no solo coincidencia) a los flujos de ETF. No cambia el filtro de tendencia (solo mira precio de BTC) ni ninguna decisión de la cuenta `arena-claude-binance`.
- **Lectura para invertir:** el catalizador se mantiene en grado B (real, pero el desfase de tiempos y la ausencia de pánico en VIX/10 años dejan una porción de la caída sin explicar por el petróleo solo); sin catalizador cripto-específico (confirmado de nuevo en la revisión semanal de contraparte de hoy, sin señales rojas, ámbar sin cambio en E5 y A9). No cambia el filtro de tendencia (ENCENDIDO, colchón 19.45% sobre la salida de 69,542.41; SMA200 sin "roll" hoy porque la vela del 7-oct aún no cierra). **Grado B** para los datos de precio y derivados; **C** para la lectura "el petróleo no explica toda la caída"; **D** para la transmisión petróleo-específica en la literatura (sin paper exacto encontrado).

## 15. Adenda (9-oct-2026): empresas de tesorería de bitcoin (DAT) — mNAV, deuda y riesgo de venta forzada

Frontera nueva, no contemplada por los 35 recursos ni por los 6 "temas que no cubren" del plan original (ficha completa: [fichas/2026-10-09-dat-companies-mnav-riesgo.md](fichas/2026-10-09-dat-companies-mnav-riesgo.md)). Motivación: el mNAV de Strategy Inc. (MSTR, 848,000 BTC, la mayor tenedora corporativa) está hoy por debajo de 1 con la métrica simple de mercado, el umbral que la literatura secundaria (Galaxy Research, vía BlockEden) señala como el punto donde se cierra la vía principal de financiamiento (ATM) de estas empresas — un mecanismo de reflexividad (precio de BTC cae → presión sobre el balance de sus mayores tenedores corporativos → posible presión adicional sobre el precio) que encaja directamente en el objetivo de "doctorado" del plan (reflexividad, eventos de cola) y que nadie en la base había tocado.

- **Cifras primarias verificadas en SEC EDGAR (CIK 0001050446), no en resúmenes de prensa:** BTC en tesorería al 4-oct-2026 = **848,000** (8-K, 5-oct-2026); notas convertibles, principal total al 30-jun-2026 = **US$6,713,659,000** (10-Q); acciones preferentes, valor de liquidación al 30-jun-2026 = **US$15,462,056,000** (10-Q); acciones en circulación al 24-jul-2026 = **384,225,751** (portada del 10-Q).
- **Ejercicio numérico (verificado dos veces, a mano y con script; precios en vivo de hoy: BTC US$83,092.80 vía `data-api.binance.vision`, MSTR US$157.33 vía Yahoo `chart v8`):** el **mNAV simple** (capitalización de mercado ÷ valor del BTC en tesorería) = **0.858**, es decir, un **descuento de 14.2%** sobre el BTC bruto — confirma que Strategy cotiza hoy por debajo de su respaldo bruto de BTC, igual que reportó la prensa para otras DAT en 2025-2026. Pero el **NAV de equity ajustado** (BTC **menos** deuda convertible **menos** preferentes, entre acciones) = **US$125.67/acción**, y el precio de mercado (US$157.33) está **25.2% por encima** de ese NAV ajustado: el mercado paga una prima por el equity apalancado (que amplifica tanto ganancias como pérdidas), aunque el BTC bruto por acción ya casi no crece porque emitir acciones a este nivel diluye en vez de acrecentar. Las dos lecturas son correctas a la vez y no se contradicen.
- **Umbral real de estrés de balance** (no mNAV<1, que solo frena el crecimiento, sino el punto donde el BTC ya no cubre deuda+preferentes): BTC tendría que caer **68.5% desde hoy** (a ~US$26,151) para llegar ahí, con la deuda convertible vigente sin vencimientos antes de 2028. **No es un riesgo inminente con los datos de hoy** (contradice la narrativa más alarmista), pero el riesgo de corto plazo real es otro: el flujo de caja de los dividendos preferentes cumulativos, que ya está cambiando el comportamiento observable de la empresa (pausa de compras del 7-13-sep; de US$246.2M de ATM del 21-27-sep, solo US$142.7M fueron a comprar BTC y US$103.5M a **recomprar** preferentes STRC con descuento).
- **Contexto más amplio, explícitamente secundario (grado C/D, no verificado contra cada filing):** prensa especializada habla de >200 empresas con ~US$150 mil millones en BTC de tesorería a nivel agregado, y Metaplanet (Japón) cruzó el mismo umbral de mNAV<1 el 14-oct-2025 —casi un año antes que Strategy— con el mismo patrón de pausa en las compras, evidencia (n=2 casos distintos) de que el patrón no es exclusivo de una sola empresa, aunque la muestra sigue siendo pequeña.
- **Qué cambia para invertir:** nada en el filtro de tendencia de `arena-claude-binance` (no tiene exposición a MSTR ni a ninguna DAT; el filtro solo mira el precio de cierre de BTC/USDT). Sí es relevante como canal de riesgo de cola a vigilar para el precio de BTC en general: si el mNAV de las DAT grandes sigue cayendo, la demanda marginal que representaron en 2024-2025 podría convertirse en oferta marginal en un escenario de cola (no hoy, con los números de esta ficha). Se registró un pronóstico verificable ligado al ritmo de acumulación de BTC de Strategy (`bitacora/pronosticos.csv`, autor=cripto) para dar seguimiento cuantitativo.
- **Grado A** para las cifras primarias de SEC EDGAR; **B** para los precios en vivo y el cálculo de mNAV/NAV ajustado (reproducible, verificado dos veces); **C** para el escenario de sensibilidad de dilución y el panorama agregado de DAT/Metaplanet (secundario); **D** para la cifra de "Galaxy: 5 empresas en riesgo" (no verificada en fuente primaria). Pendiente: el 10-Q de Q3-2026 (esperado ~24-26-oct-2026) permitirá recalcular con el conteo de acciones y la deuda/preferentes contemporáneos.

### Adenda (10-oct-2026): se leyó el texto de dos indentures — no hay disparador de default ligado al precio ni al mNAV

Avance de uno de los pendientes de la adenda anterior (ficha completa: [fichas/2026-10-10-covenants-notas-convertibles-mstr.md](fichas/2026-10-10-covenants-notas-convertibles-mstr.md)). Se leyó íntegro, directo de SEC EDGAR (sin resumen de prensa), el texto de los **Events of Default** y **Acceleration** de dos indentures distintos de Strategy Inc.: la Serie A ("0.625% Convertible Senior Notes due 2030", indenture 11-mar-2024, accession 0001193125-24-064321) y la Serie B ("0% Convertible Senior Notes due 2030", indenture 21-feb-2025, accession 0001193125-25-032800).

- **Hallazgo central:** en ninguna de las dos series el precio de la acción, el mNAV o el precio de BTC aparecen como condición de un *Event of Default*. El precio de la acción solo aparece en los derechos de **conversión** del tenedor y en la opción de **redención anticipada a favor de la empresa** (si el precio supera 130% del precio de conversión) — nunca como gatillo de incumplimiento. La "Fundamental Change" (cambio de control, venta de activos, liquidación, deslistado) tampoco usa precio ni mNAV, y da al tenedor solo un **derecho de recompra** (a su elección), no una aceleración automática.
- **El único mecanismo real de contagio es el cross-default**, por impago de "indebtedness for money borrowed" de la Compañía o de una filial significativa por encima de un umbral en dólares fijo: **US$30,000,000** en la Serie A (mar-2024) y **US$200,000,000** en la Serie B (feb-2025) — un crecimiento de 6.67x en 11 meses. Hoy, US$200M representa solo **2.98%** de los US$6,713,659,000 de deuda convertible total (30-jun-2026; cálculo verificado dos veces, `scratchpad/g4calc/cross_default.py`, fuera del repositorio).
- **Matiz declarado como pendiente, no cerrado:** el término usado es "deuda por dinero prestado", que por convención estándar de mercado **no** incluiría los dividendos de acciones preferentes (STRK, STRF, STRC, STRD) — pero no se encontró una definición explícita de "Indebtedness" en las secciones leídas que lo confirme con el 100% de certeza. Si esa lectura se sostiene, el riesgo de caja de los preferentes (señalado ayer) queda más aislado del riesgo de default en las notas de lo que una lectura superficial sugeriría.
- **Qué cambia:** refuerza con evidencia primaria directa (no inferencia) la lectura de la adenda del 9-oct: la venta forzada de BTC por un covenant ligado al precio **no existe** en el texto de estas dos series; sigue siendo un escenario de cola lejano, no el riesgo de la semana que entra. **Grado A** para las citas literales; **B** para el cálculo del umbral; **C** para la lectura convencional del término "indebtedness". Pendiente: leer las series restantes (2028, 2031, 2032) para generalizar más allá de n=2, y localizar la definición exacta de "Indebtedness".

### Adenda (11-oct-2026): se cerró el pendiente de Galaxy Digital, y un hallazgo no buscado — Strategy ya vendió BTC dos veces en 2026

Se cerró uno de los pendientes de las dos adendas anteriores (ficha completa: [fichas/2026-10-11-galaxy-prediccion-23-ventas-forzadas-dat.md](fichas/2026-10-11-galaxy-prediccion-23-ventas-forzadas-dat.md)); el otro pendiente (Metaplanet vía EDINET/TDnet) sigue abierto por tercer día (EDINET no resuelve DNS, TDnet da HTTP 403 desde este entorno; ver `bitacora/decisiones-pendientes.md`, 11-oct).

- **El "reporte de Galaxy Digital de marzo-2026" citado el 9-oct no existe como reporte aislado.** Es la predicción **#23** de "26 Predictions for Crypto in 2026" (recurso #35 del dueño, Galaxy Research, publicada el **18-dic-2025**, no marzo), ya evaluada **"cumplida"** en nuestra propia base desde el 25-sep-2026 (`arena/investigacion/fuentes-terceros/2026-09-25-galaxy-predicciones-2026.md`): "Five or more digital asset treasury companies (DATs) will be forced to sell assets, be acquired, or shut down completely." Cumplida a más tardar en la semana del 21-jul-2026, con 5 casos documentados vía CoinDesk (secundario, grado C, no re-verificado hoy contra el artículo original): Empery Digital (370 BTC), Genius Group (84 BTC), Nakamoto (≈284 BTC), Smarter Web Company (178 BTC) y Satsuma (668 BTC, liquidación aprobada por accionistas) — 1,584 BTC en conjunto.
- **Hallazgo no buscado, verificado hoy con 2 8-K primarios de SEC EDGAR:** la misma nota de `arena/` del 25-sep menciona, de paso, que Strategy también vendió BTC en 2026. Verifiqué hoy las dos semanas de agosto contra el filing primario: **1,638 BTC vendidos el 3-ago-2026** (promedio US$63,957/BTC, US$104.73M) y **1,690 BTC vendidos el 10-ago-2026** (promedio US$64,262/BTC, US$108.6M) — total **3,328 BTC / US$213.33M** (cálculo verificado dos veces, `scratchpad/g4calc/galaxy_p23_strategy_sales.py`, fuera del repositorio), usados para financiar dividendos de acciones preferentes y recompras de STRC, **no** por un *default* de deuda.
- **Qué cambia (matiza, no revierte, las adendas del 9 y 10-oct):** Strategy ya demostró que, con el mNAV deprimido, prefiere vender una porción pequeña de BTC (0.39% de sus 848,000 BTC actuales) a diluir con más acciones ATM para cubrir obligaciones de preferentes — el mismo canal de "presión de caja de preferentes" que la adenda del 9-oct identificó como el riesgo de corto plazo real, ya materializado en pequeño, no solo hipotético. Ningún 8-K desde el 10-ago (incluido el del 5-oct, última revisión) vuelve a reportar venta, solo compras — el episodio parece puntual hasta ahora, no recurrente (se registró un pronóstico verificable sobre esto, P0103, `bitacora/pronosticos.csv`).
- **Grado A** para los dos 8-K de Strategy y para la identificación correcta de la predicción #23 (recurso #35, ya "estudiado", fecha de publicación verificada). **C** para los 5 casos no-Strategy (secundario, nuestra propia nota del 25-sep, no re-verificada hoy contra CoinDesk). Pendiente: Metaplanet vía EDINET/TDnet (tercer intento fallido); re-verificar los 5 casos contra el artículo original de CoinDesk; confirmar si hubo venta de BTC de Strategy antes de 2026.

### Adenda (12-oct-2026): no existe un término "Indebtedness" definido en los dos indentures de Strategy; Metaplanet sigue bloqueado por cuarto día

Se cerró, con certeza (no solo inferencia), el pendiente explícito de la adenda del 10-oct (ficha completa: [fichas/2026-10-12-indebtedness-no-definido-y-metaplanet-bloqueado.md](fichas/2026-10-12-indebtedness-no-definido-y-metaplanet-bloqueado.md)).

- **Hallazgo:** se descargó el texto **completo** (no por tramos) de los dos indentures de Strategy ya identificados (Serie A, 2024, "0.625% due 2030"; Serie B, 2025, "0% due 2030") y se buscó, con dos métodos independientes de Python (listar términos definidos que empiezan con "I"; contar ocurrencias de "indebtedness" y verificar si alguna sigue el patrón de definición formal `"X" means`), si el Artículo 1 define un término capitalizado "Indebtedness". **Ninguno de los dos documentos lo define.** Los únicos términos definidos que empiezan con "I" son `Indenture`, `Interest Payment Date` (Serie A) y además `Initial Purchasers`, `Issue Date` (Serie B). La palabra "indebtedness" aparece 8 y 9 veces respectivamente, siempre en lenguaje llano, casi siempre dentro de la cláusula de cross-default ("indebtedness for money borrowed"/"for borrowed money" por encima de US$30M/US$200M).
- **Por qué importa:** refuerza, con evidencia directa (ausencia verificada de una definición ampliatoria) en vez de con la "convención de mercado" declarada como supuesto el 10-oct, la lectura de que un impago de dividendos de acciones preferentes (STRK, STRF, STRC, STRD, que son obligaciones de capital, no "deuda por dinero prestado") no activaría, por el propio texto de estos dos indentures, el cross-default de la deuda convertible. El riesgo de caja de los preferentes —el riesgo de corto plazo real que esta serie de fichas documenta desde el 9-oct— queda más claramente aislado del riesgo de *default* de la deuda.
- **Metaplanet, cuarto intento fallido:** EDINET sigue sin resolver DNS, TDnet sigue en HTTP 403; la IR oficial en inglés (`metaplanet.jp/en/ir`) solo lista títulos de avisos de oct-2026 (compra de BTC del 5-oct, resultados 3T, recompra de acciones), sin enlaces a PDF ni cifras extraíbles. Declarado en `bitacora/decisiones-pendientes.md` (12-oct-2026) como bloqueo de entorno, no de esfuerzo; se deja de reintentar a diario hasta tener una vía nueva o el documento del dueño.
- **Grado A** para la ausencia verificada de la definición (reproducible, dos métodos, mismo resultado en los dos documentos). **B** para la inferencia de que esa ausencia acota el alcance del cross-default (técnica de redacción contractual razonable, no una certeza jurídica — no se consultó jurisprudencia de NY/Delaware). **D** para cualquier generalización a las series 2028/2031/2032, todavía no leídas. Pendiente: leerlas para generalizar de n=2 a la familia completa; el 10-Q de Q3-2026 (~24-26-oct); re-verificar los 5 casos de Galaxy contra CoinDesk; una búsqueda de hoy (grado D, no verificada) sugiere que Strategy pudo haber vendido BTC por primera vez en **mayo-2026**, no agosto como se escribió el 11-oct — fecha en disputa, sin resolver.

### Adenda (13-oct-2026): texto primario de la GENIUS Act; la vigencia quedó fija el 18-ene-2027

- **Fuente:** texto íntegro de la Public Law 119-27, en las copias de govinfo y de congress.gov, que son idénticas byte por byte. Se agregaron dos búsquedas independientes en la API del Federal Register. Ficha: [`fichas/2026-10-13-genius-reloj-de-vigencia-y-reservas.md`](fichas/2026-10-13-genius-reloj-de-vigencia-y-reservas.md).
- **Hallazgo [H/I, B]:** la Sec. 20 pone la vigencia en la primera de dos fechas: 18 meses después de la promulgación (18-ene-2027) o 120 días después de las reglas finales de los reguladores primarios.
  - Al 13-oct-2026, OCC, FDIC, Fed y NCUA solo tienen propuestas en el Federal Register.
  - Para adelantar la vigencia, la regla final tenía que salir a más tardar el 20-sep-2026 (cálculo propio, verificado dos veces).
  - Por lo tanto, la vigencia ya **no puede adelantarse**: queda fija el 18-ene-2027, a 97 días.
  - El plazo de reglamentación de la Sec. 13 (18-jul-2026) va 87 días incumplido.
  - La prohibición a intermediarios de la Sec. 3(b) empieza el 18-jul-2028.
- **Del texto [H, A]:**
  - Las reservas forman una lista cerrada: efectivo, depósitos, T-bills/notes/bonds con vencimiento ≤ 93 días, repos y reverse repos *overnight*, fondos de mercado de dinero de gobierno y sus versiones tokenizadas. No incluyen BTC, oro ni préstamos.
  - El emisor publica sus reservas cada mes, con plazo promedio y ubicación de la custodia, y el CEO y el CFO las certifican con responsabilidad penal.
  - La prohibición de intereses de la Sec. 4(a)(11) se dirige al **emisor**, no a terceros.
  - El texto oficial cita "(1)(D)" en la Sec. 4(a)(3)(A), aunque el reporte mensual está en (1)(C): es una referencia mal numerada.
- **Para la cuenta [I]:** no hay catalizador regulatorio de stablecoins en EUA en los próximos 30 días que cambie el riesgo de USDT en Binance para una cuenta mexicana. El evento abierto es la regla final de la OCC (P0117, p=0.30 al 12-nov). La CFTC publicó hoy un ANPRM sobre mercados de criptoactivos (2026-20888); es solo el inicio de un proceso.
- **Pendientes:** Circular 4/2019 de Banxico (DOF), MiCA (EUR-Lex), el estado de CLARITY y el texto completo del ANPRM de la CFTC.

### Adenda (14-oct-2026): Circular 4/2019 de Banxico, el perímetro mexicano deja fuera a Binance por diseño

- **Fuente:** texto compilado oficial de Banxico (Circular 4/2019 más la 37/2020), cotejado contra el facsímil del DOF del 8-mar-2019 (pp. 90-92). La lista oficial de normativa de Banxico se revisó hasta la 12/2026. Se leyeron íntegros la LRITF (arts. 30-34 y 88; última reforma DOF 14-11-2025, sin cambios en ese capítulo) y el comunicado conjunto del 28-jun-2021. Ficha: [`fichas/2026-10-14-circular-4-2019-banxico-perimetro-mexicano.md`](fichas/2026-10-14-circular-4-2019-banxico-perimetro-mexicano.md).
- **Del texto [H, A]:**
  - La circular solo aplica a "Instituciones", es decir, bancos e ITF. Solo permite "Operaciones Internas", con autorización previa, y obliga a impedir que el riesgo pase a los clientes.
  - La 3.a declara **no elegibles** los servicios directos de intercambio, transmisión o custodia de activos virtuales a clientes.
  - La única reforma es la 37/2020 (11.a, fr. II, de forma).
  - El compilado coincide con el DOF en 18 de 19 disposiciones; la 11.a difiere solo por esa reforma (verificado en Python con dos métodos).
  - Lleva 2,776 días en vigor y 2,204 sin cambios.
- **Hallazgo [H/I, B]:** la LRITF (arts. 31-33) contempla la custodia y la compraventa de cripto por ITF con clientes, pero la circular la vuelve no autorizable. En México **no hay vía supervisada** para ofrecer al público intercambio o custodia de cripto.
  - Binance no es "Institución": la circular no le aplica, y su único régimen mexicano es la LFPIORPI (art. 17, fr. XVI), que no protege al cliente.
  - El punto frágil mexicano es el riel de pesos (Medá, IFPE): es una "Institución" y está sujeta a la "sana distancia" de 2021. Es grado C y no hay acción observada.
- **Para la cuenta [I]:** no hay catalizador regulatorio mexicano a 30 días. El riesgo es operativo (SPEI/Medá) y lo mide el disparador "SPEI > 48 h" del plan de contingencia. El tope de 10,000 MXN sigue siendo la única defensa de contraparte.
- **Pendientes:** MiCA (EUR-Lex), CLARITY, el ANPRM de la CFTC 2026-20888, las Disposiciones de la CNBV para IFPE y las iniciativas mexicanas de 2026.

### Adenda (15-oct-2026): MiCA, títulos III-IV y art. 143; Binance fuera del registro de ESMA

- **Fuente:** Reglamento (UE) 2023/1114, texto del DOUE (L 150, 9-jun-2023) en inglés y en español, más la consolidación vigente 02023R1114-20240109, de la Oficina de Publicaciones de la UE (Cellar). EUR-Lex directo dio HTTP 202 vacío. Registro provisional de MiCA de ESMA (`CASPS.csv` y `EMTWP.csv`, última actualización 6-oct-2026). Ficha: [`fichas/2026-10-15-mica-stablecoins-y-transicion-casp.md`](fichas/2026-10-15-mica-stablecoins-y-transicion-casp.md).
- **Del texto [H, A]:**
  - EMT: solo la emite una entidad de crédito o de dinero electrónico (art. 48). Reembolso a la par, en cualquier momento y sin comisión (art. 49). **Al menos 30% de los fondos en depósitos bancarios** separados y el resto en activos líquidos de la misma moneda (art. 54).
  - **Prohibición de intereses también para los CASP** (arts. 40(2) y 50(2)), con una definición amplia de "interés" que incluye cualquier beneficio ligado al tiempo de tenencia (ap. 3). GENIUS solo se la dirige al emisor.
  - Tope de uso como medio de cambio: 1 millón de operaciones y 200 millones de EUR diarios (art. 23), aplicable a las EMT en moneda no-UE (art. 58(3)).
  - Transición de los CASP: **hasta el 1-jul-2026** o hasta la decisión sobre la autorización, lo que ocurra antes (art. 143(3)). Títulos III-IV aplicables desde el 30-jun-2024 y el resto desde el 30-dic-2024 (art. 149).
- **Del registro [H, A]:** 365 CASP únicos; **ningún Binance** (dos métodos). Coinbase, Kraken, OKX, Crypto.com, Bybit, Bitstamp, Gemini, KuCoin y Revolut sí están; Bitget no. EMT: 25 emisores; Circle y Paxos sí, Tether no. Hay 75 autorizaciones en jun-2026 y ~16-17 al mes después del precipicio. El registro trae dos fechas imposibles (errores de captura).
- **Para la cuenta [I]:** no hay acción. Confirma con fuente primaria el ÁMBAR de E5 (Binance fuera de la UE) y propone `CASPS.csv` como fuente de E5. La diferencia MiCA-GENIUS sobre el rendimiento es la misma disputa que frena CLARITY.
- **Pendientes:** CLARITY después del 15-sep; normas técnicas de la EBA (art. 36(4)) y directrices de ESMA sobre la solicitud inversa (art. 61); ANPRM de la CFTC 2026-20888; reintentar EUR-Lex directo.

### Adenda (16-oct-2026, investigador vespertino): flujos de ETF spot y precio de BTC. Mazur y Polyzos (2025)
- **Fuente:** Mazur, M. y Polyzos, E. (2025), "Spot Bitcoin ETFs: The Effect of Fund Flows on Bitcoin Price Formation", *Journal of Alternative Investments* 27(4): 110-123, doi:10.3905/jai.2025.1.239. Solo se leyó el resumen (página institucional de Zayed University). **Grado D** para su cifra principal.
- **Qué afirma:** los flujos netos a los ETF spot "predicen" el **nivel** del precio de BTC con R² de 95%. Además, la mayor parte del cambio de precio ocurre fuera del horario de los ETF, las subidas de precio generan volumen anormal en los ETF y las entradas a ETF de BTC coinciden con salidas de ETF de oro. La muestra son las primeras semanas de 2024; el periodo exacto no está en el resumen.
- **Por qué grado D:** una regresión de niveles (o de flujos acumulados) contra niveles de dos series con tendencia da R² altos aunque no haya relación: es el problema de la regresión espuria de Granger y Newbold. Además, que el precio se mueva fuera del horario de los ETF y que las subidas atraigan volumen sugiere causalidad **del precio a los flujos**, no al revés.
- **Para el sistema:** no usar "los flujos de ETF predicen el precio" como argumento de una tesis ni de un pronóstico. Los flujos diarios (P0087 y similares) sirven como termómetro de demanda, no como señal adelantada. Ninguna regla cambia.

### Adenda (16-oct-2026): CLARITY Act (H.R. 3633), estado, división SEC/CFTC y rendimiento sobre stablecoins
- **Fuente:** textos EH (Cámara, 17-jul-2025) y RS (Senado, reportado por Banking el 1-jun-2026, Calendar No. 423) de GPO/govinfo; voto 00234 y el índice de votaciones de la sesión 119-2 en senate.gov. congress.gov dio 403/429. Ficha: [`fichas/2026-10-16-clarity-act-estado-y-division-sec-cftc.md`](fichas/2026-10-16-clarity-act-estado-y-division-sec-cftc.md).
- **Estado [H, A]:** el 15-sep-2026 se rechazó, **49-50**, la cloture sobre la moción para proceder (49 R a favor; en contra 44 D, 2 I y 4 R: Collins, Hawley, Moran y Tillis). No hubo ninguna votación nominal sobre H.R. 3633 hasta el 16-oct; la última votación del Senado es del 30-sep. Faltan 7 votos demócratas e independientes si votan los 53 republicanos. El 119.º Congreso termina en 79 días.
- **Texto [H, A]:**
  - La Cámara reparte las competencias en un solo texto: SEC en el título III y CFTC en el título IV (registro de exchanges, brokers y dealers de *digital commodities*).
  - El texto de Banking del Senado solo cubre valores: crea el "ancillary asset" (nueva sec. 4B de la Securities Act) y da por hecho el registro en la CFTC, que vive en el texto de Agricultura (12-11, ene-2026, grado C).
  - Sec. 105(b)(2): no es valor un token que el 1-ene-2026 era el activo principal de un ETP listado (BTC y ETH seguro).
  - Sec. 404: prohíbe a los exchanges y sus afiliadas pagar rendimiento sobre stablecoins a clientes de EUA, salvo las recompensas por actividad de buena fe (queda a medio camino entre GENIUS 4(a)(11) y MiCA 50(2)).
  - Sec. 605: protege la autocustodia.
  - Sec. 906: vigencia a los 360 días.
- **Para la cuenta [I]:**
  - Sin efecto a 30 días.
  - Aun firmada en el *lame duck*, la ley no regiría antes de dic-2027.
  - P0019 se mantiene en 0.04 (Kalshi 5.9% medio, Polymarket 6.05%).
  - Nuevo P0134: ¿hay una votación nominal sobre H.R. 3633 antes del 15-nov?

### Adenda (18-oct-2026): ETF spot de ether con staking (ETHB), rendimiento realizado y liquidez

Ficha [`fichas/2026-10-18-etf-ether-staking.md`](fichas/2026-10-18-etf-ether-staking.md). Es el punto 5 del plan de cobertura.
- **Texto [H, A], según el prospecto 424B3 del 11-mar-2026 y el 10-Q del 30-jun-2026 en SEC EDGAR (CIK 0002099103):**
  - 18% de la recompensa bruta queda en el patrocinador y el agente;
  - el fondo stakea entre 70% y 95% (86.9% al 30-jun);
  - la comisión es de 0.25%, con exención a 0.12% por 12 meses desde el 12-mar;
  - si el colchón sin stakear no alcanza, el fondo puede buscar retrasar la liquidación de reembolsos con los AP.
- **Cálculo [I, dos métodos]:** en el 2T-2026 el ingreso por staking fue de 0.85-0.86% anualizado del activo neto, frente a 2.43% teórico (APR medio de la red de 2.79% × 86.9%). Es decir, 35% del teórico. La espera media de entrada a staking entre el 12-mar y el 30-jun fue de 54 días (validatorqueue.com, grado B): es la explicación más probable (B-C).
- **Liquidez [H, B]:** hoy desstakear toma ~24.4 días (16.1 de cola, 1.1 de retraso y 7.2 de barrido). El máximo histórico es de 46.4 días (13-sep-2025). La cola de salida saltó de 166k a 851k ETH entre el 29-sep y el 2-oct; no se sabe quién sale (D).
- **Para la cuenta [I]:** sin efecto. ETH no está en el universo y el ETH de spot sin staking se queda así. ETHA y ETHB en el SIC siguen [NV].
- **Pronóstico nuevo:** P0141 (cola de salida al 16-nov < 928,024 ETH, p=0.65).

### Adenda (19-oct-2026): momentum de serie de tiempo en BTC, Liu y Tsyvinski (RFS 2021) fuera de muestra

Ficha [`fichas/2026-10-19-momentum-serie-de-tiempo-liu-tsyvinski.md`](fichas/2026-10-19-momentum-serie-de-tiempo-liu-tsyvinski.md). Es el primer paper de factores cripto en la base (nivel Doctorado).
- **Texto [H, A], NBER WP 24877 (sección):** con datos de 2011 a may-2018, el rendimiento semanal de BTC predice el de 1 a 4 semanas después, con betas de 0.19, 0.22, 0.21 y 0.09. BTC no tiene exposición a los factores de acciones ni macro. LTW (JF 2022, WP 25882): mercado, tamaño y momentum explican el corte transversal; el momentum funciona solo entre las monedas grandes.
- **Réplica [I, B], 438 semanas BTCUSDT de Binance (jun-2018 a oct-2026):** solo sobrevive h = 1 (beta 0.117, t NW 2.58); h = 2 y 3 dan cero. Desde ago-2022 la beta baja a 0.061 (t 1.07, no significativa). Q5−Q1 da +4.27 pp por semana, pero no es monótono y lo cargan pocas semanas. Una regla de "largo si la semana fue positiva" rinde menos que comprar y mantener aun sin costos (Sharpe 0.72 contra 0.77), con ~27 cambios al año.
- **Para la cuenta [I]:** sin cambio. El filtro SMA200 es una tendencia de unos 7 meses y no se apoya en este paper; no se debe citar como su respaldo.
- **Pronóstico nuevo:** P0148 (vela semanal BTCUSDT del 19 al 25-oct > 82,116.00, p=0.52).

### Adenda (19-oct-2026, laboratorio): la "prima de tamaño" cripto vive donde no se puede operar (Ballis e Ioannidis, arXiv:2610.23283, 16-oct-2026)

- **Fuente y acceso [H]:** HTML completo de arXiv (155 mil caracteres). Leídos el resumen, §2 (datos), §4.1-4.3 (prima en papel, deslistados, margen invertible), §7.5 (limitaciones) y §8 (conclusiones). **Grado B:** usan toda la población de CoinMarketCap (8,970 activos, 690 cortes semanales de 2013 a jul-2026, con entradas y salidas observadas) y declaran los sesgos. No se replicó.
- **Hallazgo [H]:**
  - **En papel:** el decil más chico rinde **27.5% por semana** (ajustado por mercado) en la era inicial, 8.0% en la de expansión y 2.8% en la de consolidación.
  - **Con un filtro mínimo** (más de 10 mil USD de volumen diario), la prima de la era inicial cae a cero: el decil tenía 2 monedas en promedio y solo se podía formar en 35 semanas.
  - **Deciles formados dentro del universo operable:** en la era de consolidación no hay gradiente de tamaño. La versión que sobrevive tiene una capacidad mediana de **293 mil USD**: 1.28% por semana sobre 293 mil son unos 3,757 USD.
  - **Eficiencia débil:** la asimetría de movilidad entre deciles cae ~70% desde su máximo de 2014. El mercado se acerca a la eficiencia, y lo que converge es la rotación por entrada de monedas nuevas.
- **Lectura para el sistema [I]:**
  - Confirma la regla de usar solo activos líquidos (la cuenta Binance opera BTC; ETH queda en estudio).
  - Cualquier backtest cripto que muestre rendimientos enormes en monedas chicas debe pasar tres pruebas antes de creerse: universo operable, capacidad y deslistados tratados como pérdida.
  - **Sin cambio de regla.**

### Adenda (20-oct-2026): el ANPRM de la CFTC sobre spot cripto minorista apalancado (91 FR 64811, RIN 3038-AF80)

Ficha [`fichas/2026-10-20-cftc-anprm-spot-apalancado.md`](fichas/2026-10-20-cftc-anprm-spot-apalancado.md). Cierra el pendiente "texto completo del ANPRM de la CFTC 2026-20888", abierto desde el 13-oct.
- **Texto [H, A], leído por sección (PDF de govinfo):**
  - Es un aviso previo, no una regla. Comentarios hasta el 14-dic-2026. Votó solo el presidente Selig.
  - **Regulation CTX:** la oferta de margen en los documentos del exchange es una "covered offer" que mete en la sección 2(c)(2)(D) de la CEA aun las compras pagadas al 100% de un minorista de EUA.
  - **"Actual delivery":** según *Monex*, de forma preliminar exige poseer las llaves privadas. Un saldo en el libro interno del exchange es entrega constructiva y sigue sujeto al régimen de futuros.
  - **Regulation CAM:** una subcategoría de bolsa registrada (DCM) con modelos integrados y un FCM obligatorio. El régimen de margen sigue abierto (~105 preguntas en IV-V).
- **Ejercicio [I, A en los datos]:** probabilidad de liquidación en 28 días de un largo en BTC. A 5x, la fórmula con la vol30 de hoy (32%) da 1.6%; la historia de Binance con mínimos diarios da 21% (2017-2026) y 11% (desde ago-2022). A 10x, 46% y 36%. La fórmula subestima la cola.
- **Fecha más temprana de vigencia [I]:** ~ago-2027, con una ruta mínima propia.
- **Para la cuenta [I]:** nada directo; es solo spot y no está en EUA. Refuerza que el saldo en el exchange es riesgo de contraparte. E5 sigue en ÁMBAR, sin cambio.
- **Pendientes:** V.B, V.E-V.H y el Apéndice A; los comentarios en regulations.gov; la URL del episodio de Bankless con Selig (grado C hasta verificarlo).

### Adenda (21-oct-2026): arbitraje entre exchanges, Makarov y Schoar (JFE 2020), y la prima de BTCMXN

Ficha [`fichas/2026-10-21-makarov-schoar-prima-btcmxn.md`](fichas/2026-10-21-makarov-schoar-prima-btcmxn.md) (+ `.py`). Segundo paper de la cola académica del Doctorado.
- **Paper [H, A; versión aceptada íntegra, LSE]:**
  - En 2017-18 las primas entre países fueron grandes y se movían juntas: Corea >15% y Japón ~10%. Dentro de un mismo país, <1%.
  - **México (Bitso): prima 2.7% y beta de arbitraje 0.078** (tabla 5).
  - La causa son los controles de capital, no los costos (50-75 pb).
  - El volumen firmado común explica 80-85% del rendimiento diario: 10,000 BTC mueven ~3-4%.
- **Réplica en BTCMXN de Binance, 90 días [I, A en datos]:**
  - prima media +0.034%, p5/p95 ±0.25%, vida media 0.4 h;
  - −0.30 pp de prima por cada +1% del USD/MXN en la hora: el libro en pesos se rezaga ~30%;
  - beta de presión ~0.0045 contra el rendimiento de 7 días.
  - La prima mexicana desapareció, como anticipaba el paper con las stablecoins.
- **Para la cuenta [O]:** E9 es liquidez, no precio. Hay que medirla contra el implícito, con un umbral ÁMBAR de compra < −1.0% (propuesta con el gestor de riesgo). La salida va con orden límite al implícito −0.3%. Bitso hoy tiene un libro en pesos ~28 veces más profundo a −0.5%.

### Adenda (22-oct-2026): ¿Tether infla el precio? Griffin y Shams (JF 2020) fuera de muestra

Ficha [`fichas/2026-10-22-griffin-shams-tether.md`](fichas/2026-10-22-griffin-shams-tether.md) (+ `.py`). Es el tercer paper de la cola académica del Doctorado.

- **Paper [H]:** según el resumen oficial (A; solo se tuvo acceso al resumen), las compras con Tether en 2017-18 llegaron después de caídas, se atribuyen a una sola entidad y subieron el precio. Eso favorece la hipótesis de oferta. Las magnitudes vienen de un resumen secundario (C): unas 87 horas explican ~50% del rendimiento de BTC.
  - La CFTC (8450-21, A) confirmó que las reservas no alcanzaban: hubo respaldo completo solo 27.6% de los días de 2016-2018. La manipulación no la confirmó.
- **Prueba propia, 2,334 días de jun-2020 a oct-2026 [I, A en datos]:**
  - La emisión de USDT llega **después de alzas** (t NW de 2.0 a 4.5), lo que es la huella de la demanda.
  - La emisión **no predice** el día siguiente (t 1.18).
  - Emisión neta de −0.73 mm en 30 días.
- **Para la cuenta [O]:** no entra ninguna señal de emisión en el filtro. En E8 se vigilan la paridad y las reservas, no la emisión. Una quema de más de 2-3 mm en un día, junto con un descuento de más de 1%, sería un evento de cola.

### Adenda (23-oct-2026): ¿la atención predice? Liu y Tsyvinski (§4.2) con visitas a Wikipedia, 2015-2026

Ficha [`fichas/2026-10-23-atencion-wikipedia-liu-tsyvinski.md`](fichas/2026-10-23-atencion-wikipedia-liu-tsyvinski.md) (+ `.py`). Es el cuarto paper de la cola académica del Doctorado.

- **Paper [H, A]:** en 2011-may-2018, una σ más de búsquedas de "Bitcoin" (contra las 4 semanas previas) sube el rendimiento +1.84 pp a 1 semana y +2.30 pp a 2 (tabla 19); quintil alto menos bajo, +7.39 pp sin mirar adelante (tabla 22). La atención también sigue al precio (tabla 25).
- **Prueba propia, 589 semanas con Wikipedia "Bitcoin" (Wikimedia REST, agente `user`) [I, B]:**
  - en el traslape con el paper replica: +2.75 pp a 1 semana (t NW 2.99);
  - **fuera de muestra (jun-2018 a oct-2026) desaparece:** −0.43 pp (t −0.99) en niveles y −0.16 (t −0.42) en log; Q5−Q1 de **−0.32 pp** (t −0.25). En 2022+ todo es cero. Un b positivo a 4 semanas (t ~2.2) sale entre 24 pruebas y se esfuma en 2022+.
  - Hoy la atención está en el percentil 4 de la serie (semana al 18-oct). No es señal.
- **Para la cuenta [O]:** nada entra al filtro ni al pulso. "Nadie mira bitcoin, es el piso" es una narrativa sin respaldo fuera de muestra.

### Adenda (26-oct-2026): DVOL, prima de riesgo de volatilidad y prima de evento del FOMC

Ficha [`fichas/2026-10-26-dvol-prima-de-evento.md`](fichas/2026-10-26-dvol-prima-de-evento.md) (+ `.py` y foto `.json`). Es el siguiente punto de la cola académica del Doctorado (microestructura de opciones).

- **Qué es el DVOL [H, A]:** índice de Deribit a 30 días con la fórmula de variance swap del VIX (dos vencimientos alrededor de 30 días, solo OTM con delta ≥ 5%, precio por profundidad hasta 2 BTC). Movimiento diario de 1σ ≈ DVOL/√365.
- **Prima de riesgo de volatilidad [I, A], 2021-2026:** el DVOL supera la realizada de los 30 días siguientes por **+8.4 pts en promedio** (t 4.5 sin traslape; 72% de los días). Se encogió con los años y **en 2026 es −0.3**. Cuando la realizada pasada es < 35 (hoy 24.8), la realizada siguiente promedió 44.6 contra un DVOL de 41.4: **VRP −3.2; la calma no dura**. El DVOL pronostica mejor que la realizada pasada (R² 0.37 contra 0.17).
- **Prima de evento del FOMC [I, A]:** en 46 decisiones (2021-2026), la varianza 08:00→08:00 UTC del día FOMC fue **0.75×** la de un día hábil normal (IC 0.47-1.11), con movimientos medianos algo mayores y menos colas. La cadena del 26-oct cobra **1.48×** para el tramo 28→29-oct (σ 2.07%): prima cara frente a la historia. Pronóstico **P0184** (p = 0.22).
- **Para la cuenta [O]:** nada operativo (solo spot). El colchón del filtro (−11.2% hasta la salida) es ~1.1 σ mensual con el DVOL, no ~1.7 σ como sugiere la vol30. El pulso reporta DVOL y vol30 juntos.

### Adenda (27-oct-2026): variance swap propio y prima de evento de la elección de EUA (3-nov)

Ficha [`fichas/2026-10-27-variance-swap-eleccion.md`](fichas/2026-10-27-variance-swap-eleccion.md) (+ `.py` y foto `.json`). Sigue la cola académica del Doctorado (microestructura de opciones).

- **Réplica del DVOL [I, A]:** con la fórmula del VIX sobre la cadena pública de Deribit (precio en USD a plazo = `mark_price` × F), el swap a 30 días da **39.12**; con la regla del DVOL (solo |Δ| ≥ 5%) da **37.49 contra 37.47 publicado**. Las alas profundas que el DVOL excluye pesan 8.2% de la varianza. Swap − IV ATM: +1.4 a +5.4 pts según el plazo.
- **Elección intermedia (martes 3-nov, 2 U.S.C. § 7) [I, A]:** el tramo 31-oct→6-nov cotiza una vol a plazo de 42.3 contra 35.3 de la base 6→13-nov: **salto de 1σ ~3.0%**, el día de resultados vale **3.6×** un día base. Historia (día de resultados contra 20 días previos, sin 2022 por FTX): mediana **~1×** en 5 elecciones, intermedias 1.0-4.2×, 2024 sola en 22.6×. Muestra insuficiente para llamarla cara.
- **FOMC con swap [I, A]:** razón 1.35 contra la base 6→13-nov (ATM 1.24): sigue arriba del techo histórico 1.11. La lectura del 26-oct se mantiene.
- **Para la cuenta [O]:** nada operativo (spot, sin opciones). Un salto electoral de 3σ (~9%) no alcanza la salida del filtro (colchón +13.3%). Pronóstico **P0190**.

### Adenda (27-oct-2026, investigador vespertino): la volatilidad cripto del fin de semana anticipa la varianza del lunes en el S&P desde 2024. Ebadollahyvahed y Umeorah (arXiv:2610.35702 v1, 26-oct-2026)
- **[H, C]** Con la varianza Garman-Klass de sábado y domingo de BTC, ETH y XRP como factor común, la varianza intradía del lunes del S&P 500 sube **~28% por cada 1σ** después de 2024 (γ = 0.256, p = 0.005; ~115 lunes). Antes de 2024 la relación es nula. La ruptura cae a fines de 2023, con los ETF spot en puerta, pero los flujos de los ETF no explican el efecto.
- **[C]** Fuera de muestra: QLIKE −22% en el S&P, con DM p = 0.066. Es una muestra corta y la ruptura se elige dentro de la propia muestra.
- **[I, A en datos]** **Comprobación propia** con BTC solo y Yahoo (`fichas/2026-10-27-fin-de-semana-cripto-lunes.py`): post-2024, corr 0.413 y γ 0.254 (t 2.81), +30% por 1σ; pre-2024, corr −0.01. **Reproduce.**
- **Límite:** es varianza dentro de la sesión, **sin el hueco de apertura**.
- **Para la cartera [O]:** ninguna regla. Sirve como alerta de contexto para la supervisión del lunes del UPRO (riesgo intradía de acercarse al stop).
