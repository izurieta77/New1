# 01 · The Infinite Machine (Camila Russo, 2020)

> Ficha del grupo G2 Ethereum. Estudiada el 25-sep-2026 por el analista cripto. Estado: **estudiado (sin el texto del libro)**. Acceso: **resumen**.
> Capítulo de síntesis: [02-ethereum-historia-protocolo-y-hoja-de-ruta.md](../02-ethereum-historia-protocolo-y-hoja-de-ruta.md).

## 1. Ficha

| Campo | Dato |
|---|---|
| Título | *The Infinite Machine: How an Army of Crypto-Hackers Is Building the Next Internet with Ethereum*. Edición en español: *La máquina infinita*, La Esfera de los Libros, 11-ene-2023, 368 pp., ISBN 9788413844893, según fichas de librerías (Ecobook, Librería Luque) |
| Año | 2020, Harper Business (HarperCollins), **14-jul-2020**. Hay dos cifras de páginas: xv + 332 pp. según Open Library y 352 pp. según Porchlight. ISBN tapa dura: 9780062886149 |
| Autora | Camila Russo: 8 años en Bloomberg News, luego fundadora y editora de The Defiant (medio cripto) |
| Tipo | Libro de periodismo narrativo basado en entrevistas |
| Nivel | Principiante |
| Costo | De pago (~US$20-30) |
| Idioma | Inglés, con traducción al español |
| URL | https://www.harpercollins.com/products/the-infinite-machine-camila-russo (la página devolvió 403 por el bloqueo anti-bots de la editorial; usé fichas de librerías y Open Library) |
| Conflictos de interés | - La autora dirige un medio que vive del sector cripto (The Defiant). **No encontré una declaración de sus tenencias** en lo que revisé.<br>- Varios de los que respaldan el libro invierten en el sector: Michael Novogratz (Galaxy), Chris Burniske (Placeholder), Jesse Walden (Variant) y Erik Voorhees (ShapeShift). Fuente: camirusso.com/book. |

## 2. Acceso real

- **Nivel: resumen.** No leí el texto del libro. Consulté el 25-sep-2026:
  1. el **índice completo, con páginas**, en el registro de Open Library (OL32282829M, JSON): 6 partes y 30 capítulos;
  2. la **descripción de la editorial**, reproducida en Porchlight y en camirusso.com/book;
  3. la **reseña de Decrypt** de Adriana Hamacher (14-jul-2020);
  4. datos de la edición en español en fichas de librerías.
- No encontré un extracto oficial gratuito. La vista previa de Google Books no fue accesible (API con cuota agotada) y la de HarperCollins estaba bloqueada.
- Los hechos que el libro narra los **verifiqué con fuentes primarias**: el blog de la EF de 2014, la plantilla oficial de ethereum.org, el informe de la SEC de 2017 sobre The DAO y precios diarios de Binance.
- **Todo lo que digo sobre el enfoque del libro sale del índice, la descripción y la reseña, no de haberlo leído.**

## 3. Lo esencial

**Qué cubre el libro** (según el índice, la descripción y la reseña)
1. [H] Seis partes. Groundwork (caps. 1-5), Prelaunch (6-15), Launch (16-19), Lunar Orbit (20-22), Near-Landing (23-28) y Back to Earth (29-30). Capítulos relevantes:
   - 6 "The White Paper", 9 "The Announcement", 10 "The Town of Zug", 13 "The Red Wedding", 15 "The Ether Sale";
   - 20 "The DAO Wars", 21 "The Fork", 22 "The Shanghai Attacks";
   - 25 "The New IPO", 27 "The Boom", 28 "Futures and Cats", 29 "The Crash".

   Fuente: índice de Open Library.
2. [H] La descripción de la editorial habla de un Buterin de diecinueve años que imagina una "super-charged, global computer". La historia combina innovación, escrutinio regulatorio y la llegada de Wall Street, y convirtió a los primeros participantes en millonarios y a algunos en "criminals" (descripción de Porchlight).
3. [O] Según la reseña de Decrypt:
   - un tema central es la elección de una **fundación sin fines de lucro** en vez de una empresa, impulsada por Buterin y Mihai Alisie, frente a la visión de "crypto Google" de Charles Hoskinson;
   - Russo pinta a Buterin como líder a regañadientes, con "very transparent intentions, which are always for Ethereum";
   - el cierre enfatiza que DeFi probaría que "Ethereum is actually capable of what it set out to do".

**Hechos del relato, verificados con fuentes primarias**
4. [H] Buterin compartió el whitepaper en dic-2013 (Mastering Ethereum 2.ª ed., cap. 1). Presentó Ethereum en la North American Bitcoin Conference de Miami el **26-ene-2014**; esto último solo lo verifiqué con una fuente secundaria: Wikipedia, que cita la crónica de Fortune del 28-ene-2014.
5. [H] **Venta de ether (cap. 15).**
   - Duró 42 días: del 22-jul-2014 a las 23:59, hora de Zug, del 2-sep-2014.
   - Precio: 2,000 ETH por BTC durante 14 días, luego baja lineal hasta 1,337.
   - Recaudó **31,531 BTC (US$18,439,086)** a cambio de **~60,102,216 ETH**.
   - Además se crearon dos fondos de 0.099x lo vendido: uno para contribuyentes tempranos y otro para la fundación.
   - Emisión anual prevista (diseño PoW): 0.26x lo vendido.

   Fuentes: [EF, 22-jul-2014](https://blog.ethereum.org/2014/07/22/launching-the-ether-sale); plantilla ether-sale del repositorio ethereum/ethereum.org. Génesis resultante ≈ 60.1 M × 1.198 ≈ 72 M ETH (cálculo propio).
6. [H] **Lanzamiento (cap. 16).** El bloque génesis es del 30-jul-2015 a las 03:26:13 UTC, con límite de gas de 5,000 (wiki del EPF, `protocol/history`).
7. [H] **The DAO (caps. 20-21).** Datos del informe de la SEC ([Release No. 81207, 25-jul-2017](https://www.sec.gov/litigation/investreport/34-81207.pdf)):
   - del 30-abr al 28-may-2016 vendió ~1.15 mil millones de tokens DAO por **~12 M ETH (~US$150 M)**;
   - el **17-jun-2016** un atacante desvió **~3.6 M ETH, 1/3 del total**;
   - el propio código le impidió moverlos durante 27 días;
   - el **20-jul-2016** se activó el hard fork;
   - una minoría siguió en la cadena original, "Ethereum Classic";
   - la SEC concluyó que los tokens DAO eran valores (securities).
8. [I] "The Magic Lock" (cap. 19) probablemente alude a Slock.it, la empresa de "cerraduras inteligentes" cuyos cofundadores crearon The DAO, según el informe de la SEC. No leí el capítulo.
9. [H] **Ataques de Shanghai (cap. 22).** Durante DevCon2 (2016) hubo ataques DoS con opcodes mal tarificados, como EXTCODESIZE. Respuesta: los hard forks Tangerine Whistle y Spurious Dragon (wiki del EPF, `testing/incidents`).
10. [H] **Boom de ICOs (caps. 25 y 27).** Howell, Niessner y Yermack estudian más de 1,500 ICOs que recaudaron **US$12.9 mil millones** (*Review of Financial Studies* 33(9), 2020). El éxito real se asocia con divulgación, compromiso creíble y señales de calidad.
11. [H] **Congestión (cap. 28, "Futures and Cats").** CryptoKitties (2017) congestionó la red y disparó el gas (Mastering Ethereum 2.ª ed., cap. 16). [I] El "Futures" del título probablemente alude al lanzamiento de futuros de bitcoin en dic-2017; no lo verifiqué en el libro.
12. [H] **Crash (cap. 29).** Cierre de ETHUSDT en Binance de **US$1,388.02 el 13-ene-2018**, contra **US$83.76 el 15-dic-2018**: **−94.0%** (cálculo propio con datos diarios).
13. [H] **ETH/BTC en la burbuja.** El cierre máximo del par ETHBTC en Binance fue 0.1132 (1-feb-2018) y el mínimo 0.0164 (6-sep-2019). La serie de Binance empieza el 15-jul-2017; el pico histórico de mediados de 2017 en otros exchanges no está en estos datos.
14. [I] "The Friendly Ghost" (cap. 26) probablemente alude a Casper, el "Friendly Finality Gadget", o a la línea de investigación de Vlad Zamfir. Es inferencia por el título.
15. [O] Literary Hub lo describió como "a fast-paced, Michael Lewis-style history" (citado en resultados de búsqueda; no leí la reseña original).

## 4. Qué cambia para invertir

- **Economía de ETH.**
  - [H] El libro narra el diseño original: preminado de ~72 M ETH y emisión PoW. Hoy la oferta es de 122.07 M ETH (ultrasound.money; CoinGecko da 122.08 M).
  - [H] Desde el Merge la oferta creció +1.29%; la inflación neta de los últimos 30 días es +0.87% al año.
  - [H] Staking de 35.7% de la oferta con APR máximo de consenso de 2.52% (capítulo 02).
  - [I] La lección del libro para la economía del activo: la política monetaria de ETH **ha cambiado varias veces por decisión social** (preminado, PoW, EIP-1559, PoS). La "oferta" de ETH es una regla de gobernanza, no una constante física como el tope de 21 M de BTC. Es un riesgo y una opción a la vez.
- **Captura de valor de las L2.**
  - [I] El libro es anterior a la hoja de ruta centrada en rollups: la reseña cierra con DeFi en L1.
  - [H] Hoy las L2 pagan ~0.04 ETH al día a L1 por blobs (capítulo 02).
  - [I] La "máquina infinita" de 2020 era L1. La de 2026 reparte la actividad en L2 que casi no le pagan renta.
- **Catalizadores del torneo.**
  - [I] El libro enseña que las actualizaciones se retrasan (Serenity y Casper tardaron años) y que los eventos traumáticos (The DAO, Shanghai) llegaron de sorpresa.
  - [H] Fechas del torneo: Glamsterdam en Sepolia el 6-oct-2026 y en Hoodi el 27-oct-2026 (tentativo). Mainnet sin fecha; objetivo de la EF, dic-2026.
- **Razón ETH/BTC.**
  - [H] La burbuja que narra llevó ETH/BTC a 0.1132 (feb-2018) y el crash lo hundió a 0.0164 (sep-2019).
  - [I] ETH/BTC ha sido una apuesta **procíclica** a la especulación en tokens, el ciclo de las ICOs. Hoy está en 0.0320. Un repunte fuerte del par ha requerido históricamente una ola de emisión o especulación sobre Ethereum. Con la muestra 2017-2026 de Binance no pude aislar esa relación; es una inferencia.
- **Qué haría falta para que ETH vuelva al universo.**
  - [I] Este libro no aporta criterios cuantitativos.
  - [I] Su lección de riesgo sí: el drawdown de 2018 (−94%) muestra que ETH puede perder casi todo en un año. Cualquier reentrada tiene que dimensionarse para sobrevivir a un −50% en 4 meses. Eso pasó en 26.7% de las ventanas de 122 días desde 2017 (Binance, USD).
  - [I] Criterios completos en el capítulo 02, §8.

## 5. Contrapuntos y límites

1. [O] **Sesgo de la autora.** Periodista dentro del ecosistema, con acceso privilegiado a sus protagonistas. La reseña de Decrypt no le encuentra críticas, y los que respaldan el libro son del sector. Es probable un encuadre heroico de Buterin; no pude contrastarlo sin leer el texto.
2. [H] **Qué envejeció.** El título promete "the next internet". Seis años después, el uso de DeFi sigue siendo mayormente especulativo, según Mastering Ethereum 2.ª ed., cap. 13: "has yet to find a proper market fit beyond token exchanges, stablecoins, and derivative creation". ETH quedó 44.5% abajo de su cierre máximo (cierre de ~US$2,681 frente a 4,832.07 el 22-ago-2025, Binance).
3. [I] **Qué no está probado.** Que la narrativa fundacional (idealismo, fundación sin fines de lucro) se traduzca en valor para el tenedor de ETH. El libro es historia, no tesis de inversión.
4. [H] **Límites de mi acceso.** No leí el libro. Las inferencias sobre capítulos (8, 11, 14) se basan en títulos. Para pasar de "resumen" a "sección" habría que conseguir la edición en español en una biblioteca o comprarla.
5. [I] **Contraste con *The Cryptopians*.** Shin (2022) se enfoca más en los conflictos y la codicia, y retrata a Hoskinson y Wood como villanos (reseña de Decrypt, 2022). Russo (2020) parece más celebratoria. Leer ambos corrige el sesgo de cada uno.

## 6. Autoexamen

1. **¿Cuánto recaudó la venta de ether de 2014, a qué precio y cuánto ETH se vendió?**
   31,531 BTC (US$18,439,086) por ~60,102,216 ETH. El precio fue de 2,000 ETH/BTC los primeros 14 días y bajó lineal hasta 1,337 ETH/BTC. Duró 42 días, del 22-jul al 2-sep-2014.
   Fuentes: EF blog (22-jul-2014); plantilla ether-sale de ethereum.org.
2. **Según la SEC, ¿cuánto recaudó The DAO, cuánto se desvió y cuándo se activó el hard fork?**
   ~12 M ETH (~US$150 M), del 30-abr al 28-may-2016. El 17-jun-2016 se desviaron ~3.6 M ETH (1/3). El hard fork se activó el 20-jul-2016; la minoría siguió como Ethereum Classic.
   Fuente: SEC Release No. 81207.
3. **¿Qué caída tuvo ETH entre el pico de la burbuja de ICOs y el fondo de 2018?**
   De 1,388.02 (13-ene-2018) a 83.76 (15-dic-2018) en cierres de ETHUSDT: −94.0%.
   Fuente: datos diarios de Binance (data-api.binance.vision), cálculo propio.
4. **¿Qué decisión institucional temprana, según las reseñas del libro, separó a Buterin de Hoskinson?**
   Constituir Ethereum como fundación sin fines de lucro, en vez de una empresa con fines de lucro ("crypto Google").
   Fuente: reseña de Decrypt (Hamacher, 14-jul-2020). No verificado en el texto.

## 7. Grado de evidencia: **C**

- El libro es periodismo narrativo con entrevistas, útil para entender motivos y personas.
- Para este sistema vale C por dos razones: mi acceso es solo resumen, y los relatos de testigos no son datos auditados.
- Los hechos clave de su historia sí quedan en **A**, porque los verifiqué con fuentes primarias (EF, SEC, Binance).
- Para decisiones de inversión aporta contexto de ciclos y riesgo de cola, no señales.
