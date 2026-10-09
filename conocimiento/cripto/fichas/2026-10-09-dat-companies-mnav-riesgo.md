# Ficha de avance · 9-oct-2026 · Frontera nueva: empresas de tesorería de bitcoin ("DAT companies") — mNAV, deuda y riesgo de venta forzada

> Corrida de las 08:17 CDMX (14:19 UTC), `analista-cripto`, estudio profundo. Los 35 recursos del dueño están "estudiado" en `recursos/indice.csv` (verificado hoy: 35/35) y los 6 "temas que no cubren" del plan ya tienen ficha propia (26-sep a 8-oct-2026). **Elección de hoy, con criterio propio:** en vez de seguir ahondando en el hilo de catalizadores de petróleo (ya sometido a prueba dos veces, fichas del 7 y 8-oct, con el mismo resultado de "sin transmisión mecánica"), abro una **frontera genuinamente nueva** que el plan original no contempla: el riesgo de las empresas cotizadas que acumulan bitcoin en su tesorería con deuda y acciones preferentes ("digital asset treasury companies", DAT), con Strategy Inc. (MSTR, antes MicroStrategy) como caso de estudio principal porque es, con mucho, la de mayor tamaño y la única con historial de más de 4 años.

## 0. Por qué este tema y no otro (justificación explícita)

Dos candidatos razonables para hoy eran (a) profundizar la tesis de flujos de ETF con el dato del 8-oct si ya estaba publicado, o (b) abrir esta frontera nueva. Elegí (b) por tres razones:

1. **Robustez marginal decreciente en (a):** las fichas del 7 y 8-oct ya sometieron dos catalizadores de petróleo distintos (Ormuz e Isaías) a la misma prueba de timing horario, con el mismo resultado negativo; el dato de ETF del 8-oct todavía no estaba disponible en `tftc.io` a la hora de esta corrida (ver §5), así que repetir el ejercicio de ayer con el mismo agregador habría añadido poco.
2. **(b) encaja directamente en "doctorado" del plan** (`00-plan-de-estudio.md`): reflexividad y eventos de cola. Las DAT son el mecanismo de transmisión más citado hoy entre "precio de BTC cae → presión de venta corporativa apalancada → precio de BTC cae más": es justo el tipo de bucle reflexivo (Soros) que el plan pide estudiar con evidencia, no con narrativa.
3. **Vigencia:** el mNAV de Strategy (la mayor tenedora corporativa, 848,000 BTC) está hoy por debajo de 1 según la métrica simple de mercado, un umbral que la prensa especializada señala como el punto donde se cierra la vía principal de financiamiento (emisión de acciones vía ATM) de estas empresas. Es información pública, de interés inmediato para entender quién puede verse forzado a vender si BTC sigue cayendo, y nadie en la base lo había tocado.

## 1. Acceso y fuentes (declarado)

- **Acceso íntegro, fuente primaria, verificado en vivo hoy:**
  - SEC EDGAR, Strategy Inc. (CIK 0001050446): 8-K del 5-oct-2026 (`mstr-20261005.htm`, tenencias al 4-oct-2026), 8-K del 14-sep-2026 (`mstr-20260914.htm`, compras del 21-27 sep y reanudación tras pausa), 10-Q del 30-jun-2026 (`mstr-20260630.htm`, balance de deuda convertible, preferentes y BTC).
  - `data-api.binance.vision` (spot BTC/USDT, en vivo).
  - Yahoo Finance `chart v8` (MSTR, cotización en vivo, llamada directa a la API, no un resumen de terceros).
- **Resumen/secundario, explícitamente marcado como tal:** cobertura de prensa (Radom, BlockEden, Nasdaq/Motley Fool, Pepperstone, The Block) para el panorama agregado de "~200 empresas, ~US$150 mil millones" y para el caso de Metaplanet (mNAV<1 en oct-2025); no se verificó ninguna de esas cifras contra el filing primario de cada empresa — se usan solo para dar contexto de magnitud, con grado C/D explícito.
- **No se tocó** ninguna fuente de pago ni información no pública.

## 2. El mecanismo, en una página

1. Una DAT financia la compra de BTC con tres instrumentos, de menor a mayor riesgo de "obligación fija": (a) acciones comunes (vía emisión "at-the-market", ATM, que no obliga a nada, pero diluye); (b) acciones preferentes con dividendo (algunas cumulativas, es decir, si no se paga se acumula la deuda; no tienen vencimiento fijo en todos los casos, pero sí una obligación de caja recurrente); (c) deuda convertible (principal con vencimiento fijo, convertible en acciones si el precio de la acción supera el precio de conversión, o pagadera en efectivo si no).
2. El indicador de mercado que resume si el "motor" de (a) sigue funcionando es el **mNAV simple**: capitalización de mercado de la acción dividida entre el valor de mercado del BTC en tesorería. Si mNAV > 1, emitir acciones nuevas para comprar más BTC **aumenta** el BTC por acción (acreción); si mNAV < 1, emitir acciones **diluye** el BTC por acción — el financiamiento vía ATM deja de tener sentido económico para el accionista existente, y por eso la literatura (Galaxy Research, citado por BlockEden, grado C aquí) dice que mNAV<1 "cierra" la vía principal de crecimiento de estas empresas.
3. El riesgo de **venta forzada** (lo que de verdad le importaría al precio de BTC) no viene de que mNAV caiga —eso solo frena el crecimiento—, sino de que (b) o (c) no se puedan refinanciar o pagar en efectivo y la empresa tenga que vender BTC para cumplir. Por eso hay que mirar **las dos cosas por separado**: el mNAV simple (termómetro de apetito de mercado) y el "NAV de equity ajustado" (BTC menos deuda menos preferentes, entre acciones), que mide cuánto colchón de verdad tiene el accionista común antes de que el balance se vea comprometido.

## 3. Ejercicio numérico con Strategy Inc. (verificado dos veces)

**Cifras primarias, verificadas contra el filing original, no contra un resumen:**

| Dato | Valor | Fuente primaria |
|---|---|---|
| BTC en tesorería (al 4-oct-2026) | **848,000 BTC** (costo acumulado US$63.97 mil millones, promedio US$75,440.70/BTC) | 8-K, 5-oct-2026 |
| Compra de la semana (1-4 oct) | 334 BTC, US$28.7 millones, promedio US$85,838.80/BTC, financiada con US$15.7M de ATM + US$13.0M de caja | 8-K, 5-oct-2026 |
| Notas convertibles, principal total (30-jun-2026) | **US$6,713,659,000** (series 2028 a 2032; red. por serie en la ficha) | 10-Q, 30-jun-2026 |
| Acciones preferentes, valor de liquidación total (30-jun-2026) | **US$15,462,056,000** (153,529 acciones; STRK, STRF, STRC, STRD, STRE) | 10-Q, 30-jun-2026 |
| Acciones en circulación (al 24-jul-2026, portada del 10-Q) | 364,585,501 Clase A + 19,640,250 Clase B = **384,225,751** | 10-Q, 30-jun-2026 |

**Precios de hoy, verificados con llamada directa a la API (no un agregador):**
- BTC/USDT: **US$83,092.80** (`data-api.binance.vision`, 14:19 UTC).
- MSTR: **US$157.33** (Yahoo `chart v8`, 14:23 UTC, barra diaria de hoy).

**Cálculo (script verificado dos veces: a mano y con Python; ambos coinciden a 3 decimales; archivo `scratchpad/.../dat_mstr.py`, fuera del repositorio):**

```
valor_BTC_tesoreria = 848,000 × 83,092.80 = US$70,462,694,400
market_cap          = 384,225,751 × 157.33 = US$60,450,237,405
mNAV_simple          = market_cap / valor_BTC_tesoreria = 0.858  → descuento de 14.2%

NAV_equity_ajustado  = valor_BTC_tesoreria − deuda_convertible − preferentes
                     = 70,462,694,400 − 6,713,659,000 − 15,462,056,000
                     = US$48,286,979,400
NAV_por_accion       = 48,286,979,400 / 384,225,751 = US$125.67
premio_sobre_NAV_ajustado = 157.33/125.67 − 1 = +25.2%
```

**Lectura, con el matiz que casi siempre se omite en la prensa:** con la métrica que todos citan (mNAV simple), Strategy cotiza con un **14.2% de descuento** sobre el valor bruto de su BTC — el "cierre del motor de ATM" del que habla Galaxy Research (secundario). Pero con la métrica que de verdad le importa al accionista común (BTC **menos** lo que hay que pagarle primero a bonistas y preferentes), la acción cotiza con un **25.2% de premio**. Las dos cosas son ciertas a la vez y no se contradicen: el mercado paga una prima por el equity apalancado (la misma palanca que amplifica las ganancias cuando BTC sube, amplifica también cualquier caída), mientras que el BTC bruto por acción ya no crece tan rápido porque emitir acciones nuevas a este precio diluye en vez de acrecentar.

**Sensibilidad declarada (el conteo de acciones de julio está desactualizado 77 días):** si se proyecta el ritmo de emisión ATM observado entre el 10-Q de marzo (330.8M Clase A) y el de junio (364.6M Clase A) —89 días, ~379,500 acciones/día— hacia hoy, las acciones totales serían ~413.4 millones, el mNAV simple subiría a 0.923 (descuento de solo 7.7%) y el premio sobre el NAV ajustado subiría a +34.7%. **Pero esta proyección casi seguro sobreestima la dilución real**: los propios 8-K de septiembre muestran un ritmo mucho más lento que el de abril-julio (pausa de 2 semanas el 7-13 sep; de los US$246.2M de ATM del 21-27 sep, solo US$142.7M fueron a comprar BTC, US$103.5M se usaron para **recomprar** acciones preferentes STRC) — el ritmo de dilución se está frenando justo porque el mNAV cayó, que es el mecanismo que predice la literatura secundaria. El número real de hoy está entre los dos escenarios, probablemente más cerca del de julio (A) que del proyectado (B).

## 4. El umbral que de verdad importaría para una venta forzada

No es mNAV<1 (eso solo frena el crecimiento). El umbral de estrés real de balance es cuando el valor del BTC ya no cubre lo que se le debe a bonistas y preferentes:

```
precio_BTC_critico = (deuda_convertible + preferentes) / BTC_en_tesoreria
                   = (6,713,659,000 + 15,462,056,000) / 848,000
                   = US$26,151 por BTC
caída necesaria desde hoy (83,092.80) = 68.5%
```

**Lectura, sin exagerar ni restar importancia:** BTC tendría que caer **68.5% desde el nivel de hoy** (a ~US$26,151, manteniendo tenencias y deuda constantes) para que el valor bruto del BTC ya no alcance a cubrir el total de deuda convertible más el valor de liquidación de las preferentes. No es un riesgo inminente con los datos de hoy — contradice la narrativa más alarmista que circula en redes de "Strategy está a punto de quebrar" —, pero tampoco es un riesgo nulo: la deuda convertible vence de forma escalonada 2028-2032 (no hay vencimiento antes de 2028), así que el riesgo de corto plazo real **no es este umbral de colateral**, sino el **flujo de caja de los dividendos preferentes** (cumulativos en varias series), que si no se pueden pagar en efectivo obligarían a emitir más acciones (dilución, no venta de BTC) o a recomprar preferentes con descuento (lo que ya se ve en sep-2026). La venta forzada de BTC en sí es, con la estructura actual de Strategy, un escenario de cola lejano, no el riesgo de la semana que entra.

## 5. El panorama más amplio (grado C/D, secundario — no verificado contra cada filing)

- Cobertura de prensa (Nasdaq/Motley Fool, Radom, BlockEden; **no verificado contra un filing primario de cada empresa**) habla de "más de 200 empresas" con cerca de **US$150 mil millones** invertidos en bitcoin de tesorería a nivel agregado, y de que Galaxy Digital advirtió en marzo-2026 que "al menos 5" podrían enfrentar venta forzada o cierre en el año. **No pude verificar el reporte original de Galaxy**, solo su cita en fuentes secundarias — grado D para esa cifra específica.
- **Metaplanet (Japón)** es el segundo caso mejor documentado en prensa: su mNAV cruzó por debajo de 1.0 por primera vez el 14-oct-2025 (hace casi exactamente un año), coincidiendo con una pausa de 2 semanas en sus compras — el mismo patrón que Strategy repitió en sep-2026 (pausa + mNAV débil). Es evidencia de que el patrón "mNAV<1 → pausa en las compras" no es un caso aislado de una sola empresa (n=2 casos distintos, documentados por separado), aunque sigue siendo una muestra pequeña. **No verifiqué las cifras de Metaplanet contra su filing japonés**, solo contra prensa especializada (The Block, Cointelegraph) — grado C.
- **BitMine** (tesorería de ETH, no BTC) tiene, según Nasdaq, unas pérdidas de papel no realizadas de ~US$7.5 mil millones — dato relevante para el caso análogo en ETH, sin verificación primaria propia hoy.

## 6. Qué cambia para invertir (arena-claude-binance y el comité en general)

- **No cambia el filtro de tendencia de la cuenta cripto** (solo mira el precio de cierre de BTC/USDT; no tiene exposición a MSTR ni a ninguna DAT).
- **Sí es relevante para el riesgo de cola de BTC en general** (idea que el plan pide bajo "doctorado: reflexividad y eventos de cola"): si el mNAV de las DAT grandes sigue cayendo, la vía de demanda marginal que representaron en 2024-2025 (comprar BTC con acciones nuevas a múltiplo >1) se cierra, y en el peor caso (preferentes que no se puedan pagar) podría convertirse en **oferta** marginal en vez de demanda — un canal de reflexividad que no está en los 35 recursos del dueño y que merece seguimiento, no una sola ficha.
- **No cambia ningún pronóstico ni boleta de la cuenta hoy.** Se registra un pronóstico nuevo verificable ligado a este tema (ver bitácora de pronósticos), para darle seguimiento cuantitativo en las próximas semanas.

## 7. Contrapuntos

- La narrativa alarmista ("Strategy va a quebrar") no resiste el cálculo del §4: el umbral de colateral insuficiente está a 68.5% de caída, y la deuda no vence antes de 2028.
- La narrativa optimista ("mNAV no importa, Strategy nunca venderá") tampoco resiste del todo: el propio patrón de pausas de compra y recompras de preferentes con descuento en sep-2026 (§3) muestra que el mNAV bajo **ya está cambiando el comportamiento real de la empresa**, no es solo un número de pantalla.
- Ninguna de las dos lecturas es la "oficial"; ambas tienen apoyo parcial en los datos primarios de hoy.

## 8. Autoexamen

- ¿Puedo reproducir cada cifra sin ver la ficha? Sí: los filings primarios de SEC EDGAR (CIK 0001050446) y las dos llamadas de precio en vivo están citados con URL/fuente exacta.
- ¿Qué rompería la lectura del §3? Si las acciones en circulación reales de hoy fueran mucho más altas que el escenario B (algo que no puedo verificar hasta el 10-Q de Q3, esperado ~24-26-oct-2026), el premio sobre NAV ajustado sería menor al estimado.
- ¿Qué rompería la lectura del §4? Un evento de "vencimiento acelerado" por incumplimiento de convenio (covenant) no contemplado en esta ficha; no se revisó el texto íntegro de los convenios de cada serie de notas hoy — pendiente.
- **Grado: A** para las cifras primarias citadas directamente de SEC EDGAR (BTC, deuda, preferentes, acciones al 24-jul); **B** para los precios en vivo y el cálculo de mNAV/NAV ajustado (reproducible, verificado dos veces); **C** para el escenario B (proyección propia, declarada como tal) y para el panorama agregado de DAT y Metaplanet (secundario); **D** para la cifra de "Galaxy: 5 empresas en riesgo" (no verificada en fuente primaria).

## 9. Pendientes

- Verificar el 10-Q de Q3-2026 (esperado ~24-26-oct-2026) para el conteo real de acciones y el BTC/deuda/preferentes actualizados, y recalcular el mNAV y el NAV ajustado con datos contemporáneos (cierra la brecha del escenario A/B).
- Leer el texto de al menos una serie de notas convertibles (prospecto, EDGAR) para verificar si hay convenios de vencimiento acelerado ligados al precio de la acción o al mNAV.
- Verificar directamente en el filing japonés (TDnet/EDINET) las cifras de Metaplanet citadas hoy solo por prensa.
- Buscar el reporte original de Galaxy Digital (mar-2026) sobre "5 empresas en riesgo de venta forzada o cierre" citado hoy solo de forma secundaria.
- Dar seguimiento al pronóstico registrado hoy (ver `bitacora/pronosticos.csv`) sobre el ritmo de acumulación de BTC de Strategy.

Script de esta sesión: `scratchpad/.../dat_mstr.py` (fuera del repositorio).
