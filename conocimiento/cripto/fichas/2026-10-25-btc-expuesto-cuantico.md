# Ficha de avance · 25-oct-2026 · ¿Cuánto BTC está expuesto al riesgo cuántico? Conteo propio de las P2PK de coinbase

> **Por qué este tema.** Es el primer punto de la cola que dejó la ficha del 24-oct (`fichas/2026-10-24-poscuantica-bitcoin.md`, §7): "contar, con un nodo o con un conjunto de datos público verificable, el BTC en P2PK, en P2TR y en direcciones reusadas". Las cifras del cap. 05 (6.65 M BTC, Galaxy) y de la prensa (~1 M de Satoshi, ~1.7 M en P2PK) seguían en grado C, sin verificación propia.

## 0. Preguntas de hoy

1. ¿Cuánto BTC sigue en salidas P2PK de coinbase sin gastar? Es la parte más grande de la exposición larga y la única que se puede contar sin nodo propio.
2. ¿Coincide con la cifra publicada de "más de 1.7 M BTC en P2PK"?
3. ¿Cuánto tardaría una sola máquina en barrerlo? ¿Qué escala tiene frente a los flujos de los ETF?

## 1. Acceso y fuentes (declarado)

| Fuente | Grado | Acceso real |
|---|---|---|
| **Datos de la cadena** vía las API públicas de Esplora: [blockstream.info/api](https://blockstream.info/api/blocks/tip/height) y [mempool.space/api](https://mempool.space/api/blocks/tip/height). Endpoints `/block-height/h`, `/block/<hash>/txid/0`, `/tx/<txid>` y `/tx/<txid>/outspends`. Punta: altura 973,080 (25-oct-2026, 14:3x UTC) [Nota conciliación 26-oct-2026 03:0x UTC, `bitacora/arbitraje/2026-10-25.md` §1: "14:3x" es posterior al commit `7c11e2b` (14:28:00 UTC). Esplora da el bloque 973,080 con marca de tiempo 14:21:36 y el 973,081 con 14:38:21, así que la lectura fue entre 14:21:36 y 14:28:00 UTC. La altura y los resultados no cambian.] | **A** (dato de la cadena; cualquiera lo reproduce con un nodo) | Íntegro para la muestra: 360 coinbases |
| **Babbush, Zalcman, Gidney, …, Drake y Boneh**, "Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities", [arXiv 2603.28846](https://arxiv.org/abs/2603.28846) v2 (15-abr-2026). Es el trabajo de Google Quantum AI que la ficha del 24-oct citó como IACR 2026/625 | **B** (preprint de autores primarios; el dato sale de `bigquery-public-data.crypto_bitcoin`) | **Sección**: PDF leído en §1 (dormidos), la sección de tipos de script (tabla I, figs. 5, 7 y 13) y §VIII.A. No leí el resto del PDF (~290 mil caracteres) |
| Consejo asesor cuántico de Coinbase, vía [The Block](https://www.theblock.co/post/404685) (13-jun-2026) | **C** (secundaria; el [original](https://www.coinbase.com/blog/coinbase-quantum-advisory-council-post-quantum-migration-and-abandoned-coins) responde 403) | Resumen de prensa |
| Chaincode Labs, vía [ForkLog](https://forklog.com/en/chaincode-labs-sizes-up-the-quantum-threat-to-bitcoin/) y newsbeep | **C** | Resumen; no encontré el original |

**Lo que no logré:** las consultas agregadas de Blockchair (`outputs?q=type(pubkey),is_spent(false)&a=sum(value)`) devolvieron el error 430 ("IP bloqueada temporalmente; pida una API key"). No lo rodeé. Sin nodo ni BigQuery, no conté **P2TR** ni **reusadas**: esas dos siguen en B (paper) y C (prensa).

## 2. Lo que dicen las fuentes [H]

- **Paper de Google (B):**
  - "P2PK locking scripts, which secure **over 1.7 million BTC**" (casi 9% del BTC);
  - "the total amount of **dormant** quantum-vulnerable bitcoin may reach **2.3 million BTC**" (fig. 13: top 100,000 direcciones vulnerables sin gasto en 5 años);
  - "at the time of writing **∼6.9M** total bitcoin across all protocols are vulnerable" (fig. 5). La fig. 7 da ~6.7 M para el top 100,000.
  - Criterio: P2PK, P2TR y P2MS cuentan como 100% vulnerables. Los demás tipos, solo si la dirección ya apareció en una entrada (llave revelada) y conserva saldo.
  - P2TR movió ~16.8 M BTC en 2025 y fue el 21.68% de las transacciones (tabla I, bloques 877,259-930,340). Ese dato es de flujo, no del saldo en P2TR.
- **Coinbase (C, vía The Block):** ~1.7 M BTC en P2PK repartidos en ~20,000 direcciones y ~5 M por reuso (cifra de Project Eleven); en total, ~7 M. Gran parte está en carteras frías de exchanges conocidos, sin nombre ni monto.
- **Chaincode (C, vía newsbeep):** 6.36 M vulnerables (32.7%): 4.49 M por reuso y 1.87 M en P2PK.

## 3. Ejercicio numérico (comprobado en Python)

Código: [`2026-10-25-btc-expuesto-cuantico.py`](2026-10-25-btc-expuesto-cuantico.py). Muestra cruda: [`2026-10-25-btc-expuesto-cuantico-muestra.jsonl`](2026-10-25-btc-expuesto-cuantico-muestra.jsonl), 360 coinbases con el tipo de cada salida y si ya se gastó. Se reproduce con `python3 -I 2026-10-25-btc-expuesto-cuantico.py 2026-10-25-btc-expuesto-cuantico-muestra.jsonl`.

**Diseño:** muestra estratificada de los bloques 0-419,999, en 6 estratos con 60 bloques cada uno (semilla 20261025). Para cada coinbase se leen el tipo de salida (`scriptpubkey_type`) y su estado de gasto. El estimador suma, por estrato, el número de bloques por el promedio de BTC en P2PK sin gastar. El intervalo sale de un bootstrap estratificado con 4,000 réplicas.

| Estrato (alturas) | Coinbases P2PK | BTC que sigue en P2PK | BTC estimado |
|---|---|---|---|
| 0-52,499 (2009-abr-2010) | 100% | 46.7% | 1,225,000 |
| 52,500-104,999 (abr-dic 2010) | 100% | 16.7% | 437,500 |
| 105,000-157,499 (ene-dic 2011) | 100% | 0.0% | 0 |
| 157,500-209,999 (2012) | 66.7% | 1.7% | 43,826 |
| 210,000-314,999 | 10.0% | 0.0% | 0 |
| 315,000-419,999 | 0.0% | 0.0% | 0 |
| **Total** | | | **1,706,326 (IC 95%: 1.27-2.14 M)** |

**Resultados:**

1. **Hay ~1.71 M BTC en P2PK de coinbase sin gastar, ≈8.5% de la oferta emitida** (20,103,378 BTC por calendario a la altura 973,080). El cálculo propio confirma la cifra del paper ("over 1.7 M"), que también cuenta las P2PK que no vienen de coinbase. **La cifra de P2PK sube de C a A/B.** El intervalo es ancho (±25%) porque el saldo va en bloques de 50 BTC, todo o nada.
2. **Casi todo está en 2009-2010.** Las coinbases de 2011 (bloques 105,000-157,499) eran P2PK pero ya se gastaron todas en la muestra; en 2012 dos tercios seguían siendo P2PK, y desde 2013 casi ninguna. Encaja con la tesis de monedas dormidas o perdidas, incluidas las ~1 M de "Patoshi", que siguen en C. La exposición larga en P2PK es un **saldo fijo que no crece**; lo que crece es P2TR.
3. **Llaves por barrer: ~34,125**, casi todas con 50 BTC. La prensa habla de ~20,000 direcciones; la diferencia puede venir de llaves repetidas entre bloques, porque cuento salidas y no direcciones. Tiempo de barrido con una sola máquina y en secuencia:
   - a 10 min por llave (reloj rápido), **237 días**;
   - a 1 h por llave, 3.9 años;
   - a 26 días por llave (reloj lento), 2,431 años.

   La ficha del 24-oct tenía razón: lo que manda es el reloj de la máquina. Con reloj rápido, las monedas dormidas saldrían al mercado **en menos de un año**.
4. **Escala de mercado:** 1.71 M BTC equivalen a **216 días** de la salida de los ETF del 22-oct (−US$635.5 M ≈ 7,914 BTC a 80,304). Los dormidos del paper (2.3 M, 11.4%) equivalen a **~14 años de la emisión actual** (3.125 BTC × 52,560 bloques = 164,250 BTC al año).
5. **Cifras totales (34% de la oferta: 6.9 M según el paper y ~7 M según Coinbase):** la mayor parte es reuso de **dueños activos que sí pueden migrar**, entre ellos los exchanges. No es oferta en riesgo de salir de golpe. **La cifra que importa para el precio es la de los dormidos (~2.3 M, B), no la de 6.9 M.**

## 4. Qué cambia para invertir [I/O]

- **Riesgo de cola, no de temporada.** Nada operativo antes del 28-ene-2027. La tesis de cola queda cuantificada: en el escenario de reloj rápido sin congelamiento (sin BIP-361), hasta **~2.3 M BTC (11% de la oferta)** podrían venderse en meses. Con congelamiento, no, pero eso abre un riesgo de **gobernanza**: el "contrato social" del que habló la ficha del 24-oct.
- **Señal para vigilar:** la proporción de oferta en P2TR (crece con Taproot) y los mensajes de los exchanges sobre migrar carteras frías reusadas. Si un top-5 anuncia esa migración, la cifra de 6.9 M baja sin que cambie el riesgo de los dormidos.
- **Nuestra cuenta:** sin cambio. El BTC está en Binance y no sabemos cómo administra sus llaves (Coinbase dice que hay carteras frías de exchanges expuestas por reuso). Esto entra como nota en E3/E6 de la lista de señales, no como disparador.

## 5. Contrapuntos y límites

- **Muestra de 360 bloques:** el IC de 95% va de 1.27 a 2.14 M. Para una cifra exacta hace falta recorrer el conjunto UTXO con un nodo (`dumptxoutset`) o con BigQuery.
- **No conté P2PK fuera de coinbase, P2MS, P2TR ni reusadas.** Esas cifras (2.3 M dormidos y 6.9 M totales) son del paper (B), que usa BigQuery, y no las reproduje.
- **"Sin gastar" no quiere decir "perdido":** un dueño vivo puede mover sus P2PK mañana. Este ejercicio no separa las monedas perdidas de las dormidas; el paper usa 5 años sin gasto como proxy.
- **Conflicto de interés:** Google Quantum AI tiene interés en el tema; Project Eleven y Coinbase, en vender productos o en un estándar. El conteo de la cadena no tiene ese sesgo.
- Las API de Esplora dependen de dos operadores (Blockstream y mempool.space). Los resultados se cruzaron entre los dos con rotación de host, pero no con un nodo propio.

## 6. Autoexamen

1. ¿Por qué una salida P2PK está expuesta y una P2WPKH nueva no? (En P2PK la llave pública está en la salida; en P2WPKH solo aparece el hash hasta que se gasta).
2. ¿Por qué casi todo el saldo P2PK está antes del bloque 105,000? (Los mineros de 2011 gastaron sus coinbases, y desde 2013 casi ninguna coinbase usa P2PK.)
3. ¿Qué cifra importa para la oferta en un escenario de robo: 6.9 M o 2.3 M? (2.3 M: los dueños activos pueden migrar; los dormidos no).
4. ¿Cuánto tarda una máquina de 10 min por llave en barrer 34,125 llaves? (≈237 días).

## 7. Estado

- **Documentado con comprobación** (Doctorado: seguridad del protocolo). La cifra de P2PK pasa a A/B y la de 6.65-6.9 M BTC totales, a B (paper).
- **Siguiente prueba:**
  1. contar P2TR y reusadas con un conjunto UTXO verificable (nodo propio o BigQuery, si hay vía legal sin costo);
  2. microestructura de opciones: DVOL y prima de evento (siguiente punto de la cola);
  3. vigilar BIP-360/361 y los anuncios de migración de los exchanges.
