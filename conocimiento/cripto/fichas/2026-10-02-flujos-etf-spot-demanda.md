# Ficha de avance · 02-oct-2026 · G5 Mercado (flujos de los ETF spot de BTC como variable de demanda)

> Corrida de las 08:17 CDMX (14:18:45 UTC), `analista-cripto`. Toma el **tema 4** de "Temas que no cubren los 35 recursos y que el torneo necesita" (`00-plan-de-estudio.md`): *"Flujos de los ETF spot como variable de demanda."* Es el siguiente pendiente de menor número: el tema 1 (microestructura) se cubrió el 30-sep, el tema 2 (ciclos y halving) el 1-oct y el tema 3 (BTC vs. tasa real/Nasdaq/USD-MXN) el 29-sep. El capítulo `05-mercado-on-chain-stablecoins-e-institucional.md` ya trataba los ETF como "comprador marginal" (§2, idea 4) y marcaba la fuente de flujos como un **hueco** sin resolver (§3.3, §7): "Farside respondió 403 y SoSoValue estaba bloqueado por el proxy." Esta ficha no resuelve el acceso directo (sigue bloqueado hoy), pero construye el primer ejercicio numérico propio con los datos de flujo diario más recientes disponibles por prensa, cruzados con precio y volumen reales.

## 1. Acceso real y el problema de origen (sin cambios desde el 25-sep-2026)

- **`farside.co.uk/btc/`**: HTTP 403 (verificado hoy con `curl`, con y sin cabecera `User-Agent`).
- **`api-v2.sosovalue.com`** y **`sosovalue.com/assets/etf/us-btc-spot`**: sin respuesta o 403 (bloqueados por el proxy/CDN desde este entorno).
- **`open-api.coinglass.com/public/v2/bitcoin_etf`**: responde, pero con error 500 interno (no es un dato usable).
- **Vía legal usada hoy:** búsqueda web (`WebSearch`/`WebFetch`) de prensa especializada que cita explícitamente a SoSoValue o Farside como fuente primaria de los datos (The Block, Chaincatcher, Panews, Bloomingbit, KuCoin/ME News, CryptoTimes). Es exactamente la misma vía que ya usaba el capítulo 05 para los flujos ("notas de prensa que citan Farside o Bloomberg, con fecha y fuente"), aquí aplicada con una verificación cruzada de 4 fuentes independientes para el mismo día, que el capítulo no había hecho todavía.
- **Grado de acceso:** resumen de prensa secundaria con atribución a fuente primaria (SoSoValue), no el dato directo de la API. Se declara así, sin afirmar una lectura íntegra que no hubo.

## 2. El mecanismo (por qué un flujo de ETF es, en teoría, demanda real de BTC)

- Los ETF spot de BTC en EUA (IBIT, FBTC, ARKB, BITB, GBTC convertido, etc.) operan por **creación y redención en efectivo** (*cash create/redeem*), no en especie: un participante autorizado (AP) entrega dólares al emisor, el emisor (vía su agente de ejecución, p. ej. Coinbase Prime para IBIT) compra BTC en el mercado abierto con ese efectivo, y a cambio entrega acciones nuevas del ETF al AP. La redención es el proceso inverso: el emisor vende BTC en el mercado y entrega el efectivo.
- Esto es distinto de un fondo cerrado como GBTC antes de su conversión a ETF en ene-2024, que podía cotizar con descuento o premio frente al BTC subyacente sin que eso moviera una sola compra o venta real de BTC.
- **Implicación [H, mecanismo estándar de la industria]:** un flujo neto positivo (creaciones > redenciones) **sí** debería corresponder, con un rezago de liquidación de T+1 a T+2, a compras reales de BTC en el mercado spot por un monto similar en dólares. Es la base de la idea 4 del capítulo 05 ("los ETF son el comprador marginal").
- **Matiz que el capítulo 05 no detallaba:** el flujo diario reportado por SoSoValue/Farside se basa en el cambio de acciones en circulación multiplicado por el NAV del día, **no** en el momento exacto de la ejecución de la compra. Por eso el flujo de "hoy" puede reflejar una orden colocada ayer y ejecutada hoy, o viceversa: es una variable **coincidente o con rezago corto**, no necesariamente una señal que se adelanta al precio. Esto es consistente con la conclusión ya registrada en el capítulo ("los flujos confirman tendencias, no las anticipan").

## 3. Datos de hoy: reconciliación de una discrepancia real entre fuentes de prensa

Al buscar el flujo del "1-oct-2026" aparecieron dos cifras contradictorias en la prensa:

| Fuente | Cifra citada | A qué día corresponde en realidad |
|---|---|---|
| CryptoTimes (titular fechado 2-oct, cita SoSoValue "al 1-oct 18:00 UTC") | "≈ −149M USD el 1-oct" | **Error de etiqueta**: 18:00 UTC = 14:00 hora de Nueva York, con el mercado de EUA todavía abierto; a esa hora el dato disponible es el cierre **del día anterior** (30-sep), no el de hoy |
| KuCoin/ME News (cita SoSoValue) | "+103M USD el 1-oct (hora del Este)", IBIT +196M, FBTC −60.73M, GBTC +14.59M | Correcto: es el flujo de la sesión que cerró el 1-oct |
| The Block (2026-10-01), Chaincatcher, Panews, Bloomingbit (las 4 citan SoSoValue) | "−148.7M a −149M USD", con FBTC −125.6M, BITB −13.6M, IBIT −9.5M, "rompe racha de 9 días y 3,100M USD" | Es el flujo del **30-sep** (el propio pronóstico P0047 de esta bitácora, registrado el 1-oct, ya había tomado "−148.7M USD el 30-sep" correctamente) |

**Verificación cruzada de la cifra del 30-sep** (4 fuentes de prensa independientes, todas atribuidas a SoSoValue): −148.70M, −149.0M, −148.70M y −148.69M. Desviación máxima entre las 4: **0.31M USD (0.21% del valor)**. Es un nivel de concordancia alto para datos de prensa secundaria, y confirma que el número es sólido; lo que no era sólido era la **fecha** que le puso un agregador (CryptoTimes).

**Conclusión del ejercicio de reconciliación:** el "hueco" del capítulo 05 no es solo de acceso a la API; también hay riesgo de **mal etiquetado de fecha** en la prensa secundaria cuando se cita un corte de hora intradía antes del cierre de EUA. Regla operativa para la rutina: al tomar un flujo "del día anterior" de una nota de prensa, verificar que al menos dos fuentes independientes coincidan en la fecha, no solo en la cifra.

## 4. Ejercicio numérico (cálculo propio, verificado con script)

```python
import json, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "estudio-cripto"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

# Cierres diarios reales (data-api.binance.vision, klines 1d, velas completas)
cierres = {
    "2026-09-28": 83500.01, "2026-09-29": 83663.66,
    "2026-09-30": 83623.60, "2026-10-01": 84880.05,
}
# Flujos netos diarios de ETF spot BTC en EUA, en USD (prensa que cita SoSoValue)
flujos_usd = {"2026-09-30": -148.7e6, "2026-10-01": 103e6}
vol_binance_24h_btc = 22903.61  # ticker 24hr, solo Binance spot, 2-oct 14:23 UTC

fechas_precio = sorted(cierres)
for d in sorted(flujos_usd):
    precio_d = cierres[d]
    flujo_btc = flujos_usd[d] / precio_d
    idx = fechas_precio.index(d)
    ret = cierres[fechas_precio[idx]] / cierres[fechas_precio[idx - 1]] - 1
    print(d, f"{flujos_usd[d]/1e6:+.1f}M USD", f"{flujo_btc:+,.1f} BTC",
          f"retorno mismo dia {ret:+.2%}", f"flujo/vol.Binance24h {flujo_btc/vol_binance_24h_btc:+.2%}")
```

**Resultado (verificado dos veces: a mano con calculadora y con el script; `scratchpad/g5_etf/flujos_etf_vs_precio.py`, fuera del repo):**

| Día | Flujo ETF (USD) | Flujo en BTC (al precio del día) | Retorno de BTC el mismo día | Flujo ÷ volumen 24h de Binance spot (solo 1 exchange) |
|---|---|---|---|---|
| 30-sep-2026 | −148.7M | **−1,778.2 BTC** | −0.05% (prácticamente plano) | **−7.76%** |
| 1-oct-2026 | +103.0M | **+1,213.5 BTC** | +1.50% | **+5.30%** |

- **Contexto de magnitud:** el peor mes de 2026 para los ETF (junio, −65,800 BTC acumulados, ya citado en el capítulo 05) equivale a un promedio de **−2,193 BTC/día**, del mismo orden de magnitud que los −1,778 BTC del 30-sep. Es decir, el día "malo" de esta semana no es un evento atípico frente a lo peor que ya vivió el año; es ruido normal.
- **Lectura del cruce flujo-retorno (n=2, no se puede generalizar):** el día de salida neta (30-sep) el precio quedó plano (−0.05%) y el día de entrada neta (1-oct) el precio subió 1.50%. La dirección es la misma, pero con solo 2 observaciones esto es puramente **anecdótico**; no contradice ni confirma nada por sí solo. Se anota como punto de partida de una serie que la rutina puede seguir construyendo día a día (igual que ya hace con MVRV en el capítulo 05, §3.2).
- **Lectura de magnitud relativa:** un flujo de ETF de 100-150M USD equivale a 5-8% del volumen de 24 horas de **un solo exchange** (Binance spot). Frente al volumen global de BTC (que incluye muchos más exchanges, aunque con el problema conocido de volumen inflado/"wash trading" en varios de ellos, documentado en otra parte de la literatura), la fracción real es menor. Esto cuantifica, con números de hoy, la idea ya registrada en el capítulo 05: **los ETF son un comprador marginal relevante pero no dominante** en un día cualquiera; su peso relativo sube mucho en los meses de flujo extremo (jun-2026) o en rachas largas (los 9 días y 3,100M USD que precedieron al 30-sep).

## 5. Qué cambia para invertir

- **Para la cuenta `arena-claude-binance`:** nada cambia en el filtro de tendencia (que solo mira el precio de BTC/USDT). Los flujos de ETF no son un insumo de la regla de salida/reentrada ni deberían serlo: son coincidentes, no líderes (idea 4 del capítulo 05, ahora con un cálculo propio que la respalda con datos de esta semana).
- **Para la vigilancia de datos:** se agrega una regla operativa nueva (§3): un flujo "del día anterior" citado por una sola nota de prensa, sin verificar la fecha contra una segunda fuente, puede estar mal etiquetado si el corte es intradía antes del cierre de EUA. Vale para el pulso de cripto de cada corrida.
- **Para el pronóstico:** esta ficha no genera por sí sola un pronóstico nuevo (el de hoy se registra por separado), pero deja una serie de 2 puntos que, si se repite varias corridas, podría sostener un pronóstico futuro sobre si el signo del flujo de ETF del día predice el signo del retorno del día siguiente (con n suficiente para no caer en el mismo problema de muestra pequeña que ya documentó el capítulo 05 en sus tasas base de MVRV).

## 6. Contrapuntos y límites

- **n=2.** Es el límite más importante: todo lo de §4 es una fotografía de 2 días, no una serie. No se puede extraer una correlación ni un patrón con esto solo.
- **Sigue sin haber acceso directo y reproducible a la API de flujos de ETF** desde este entorno (Farside 403, SoSoValue 403/bloqueado, CoinGlass gratis con error 500). El ejercicio depende de que la prensa siga publicando y de que cite su fuente con claridad.
- **El volumen de "un exchange" (Binance) no es el volumen total del mercado.** Usarlo como denominador da una cota de orden de magnitud, no una fracción exacta del mercado global; el capítulo mismo ya advierte del problema del volumen inflado en otros exchanges.
- **El mecanismo de creación/redención en efectivo (§2) es el estándar documentado para IBIT y FBTC, pero no se verificó hoy para cada uno de los ETF menores (BITB, ARKB, etc.); se asume igual por ser el régimen típico de los ETF de materias primas en EUA desde la aprobación de la SEC en ene-2024.**
- **Grado B** para los números de flujo y precio (reproducibles, 4 fuentes de prensa independientes que concuerdan dentro de 0.21% para el 30-sep, cálculo propio verificado dos veces). **Grado D** para cualquier lectura predictiva del cruce flujo-retorno, por el tamaño de muestra (n=2).

## 7. Autoexamen

- ¿Puedo reproducir el número sin ver la ficha? Sí: tomar el flujo en USD de una fuente de prensa con fecha verificada contra una segunda fuente, dividir entre el precio de cierre del mismo día (Yahoo o `data-api.binance.vision`) para obtener BTC equivalente, y comparar contra el volumen de 24h de Binance (`/api/v3/ticker/24hr`).
- ¿Qué rompería la conclusión? Si una tercera fuente primaria (p. ej. Farside, si algún día deja de dar 403) reportara una cifra distinta a las 4 de prensa para el 30-sep, o si el mecanismo de creación en efectivo no aplicara igual para todos los ETF menores.
- **Grado: B** para el ejercicio numérico; **D** si se usa para predecir el retorno del día siguiente con solo 2 observaciones.

## 8. Estado del pendiente

- Tema 4 de "Temas que no cubren los 35 recursos" (`00-plan-de-estudio.md`): **iniciado con reconciliación de fuentes y primer ejercicio numérico propio (n=2).** Pendiente para corridas futuras: acumular el flujo diario día a día (con verificación de fecha de dos fuentes) para construir una serie propia de al menos 20-30 observaciones antes de intentar cualquier lectura predictiva; probar de nuevo el acceso directo a Farside/SoSoValue/CoinGlass por si el bloqueo se levanta.
- Actualiza el capítulo de síntesis `05-mercado-on-chain-stablecoins-e-institucional.md` (adenda fechada 2-oct-2026, §11) y `conocimiento/estado-de-dominio.csv` (fila `cripto/05`).

Script y datos crudos de esta sesión: `scratchpad/g5_etf/` (fuera del repositorio).
