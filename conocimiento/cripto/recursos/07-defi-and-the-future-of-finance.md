# 07 · DeFi and the Future of Finance (Harvey, Ramachandran y Santoro)

> Ficha de estudio del grupo G3 DeFi, escrita por `analista-cripto` el 25-sep-2026. Es formación, no recomendación.
> **Advertencia de acceso:** **no leí el documento de trabajo de SSRN (3711777) ni el libro de Wiley.** Lo que sigue sale de tres fuentes legales del propio autor (ver §2):
>
> - el resumen que los tres autores publicaron;
> - un ensayo de Harvey de 2022;
> - las seis presentaciones públicas con que Harvey enseña cada capítulo (2021).
>
> **Estado:** pendiente de acceso al documento de trabajo; material del autor estudiado.
> **Capítulo de síntesis:** [03-defi-mecanica-riesgos-y-academia.md](../03-defi-mecanica-riesgos-y-academia.md).

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2021. El documento de trabajo SSRN 3711777 tiene fecha de 5-abr-2021 según la API de Semantic Scholar; la página de SSRN no la pude abrir. El resumen de los autores en el foro de Harvard Law es del 14-ene-2021, y el libro de Wiley salió en 2021. |
| Autores | **Campbell R. Harvey** (Duke Fuqua y NBER). **Ashwin Ramachandran**: en 2021 se presentaba como "*independent researcher*" (foro de Harvard Law); según [vcsheet](https://www.vcsheet.com/who/ashwin-ramachandran) es socio general de Dragonfly Capital, un fondo cripto, sin fecha verificada. **Joey Santoro**, "*founder of Fei Protocol*" (foro de Harvard Law). |
| Tipo | Libro de Wiley (ISBN 978-1-119-83602-5 según el CV de Harvey) y documento de trabajo en SSRN. El CV de Harvey llama a la versión de SSRN "**SSRN (excerpt)**": un extracto, no el libro completo ([CV](https://people.duke.edu/~charvey/vitae.htm)). |
| Nivel | Intermedio |
| Costo | Libro: ~US$30. Documento de trabajo: gratis en SSRN. |
| Idioma | Inglés. Hay traducción al coreano (2022). |
| URL | [Wiley](https://www.wiley.com/en-us/DeFi+and+the+Future+of+Finance-p-9781119836025) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3711777) |

**Conflictos de interés verificados:**

- **Santoro fundó Fei Protocol**, una stablecoin.
  - El deck de infraestructura de Harvey (2021, lámina 24) dice: "*It is still an open problem to create a decentralized stablecoin which both scales efficiently and is resistant to collapse... Fei Protocol is an example of a new initiative that is both decentralized and scalable*".
  - Es decir, el material promueve el protocolo del coautor.
  - Fei sufrió un hackeo de $80 M en abr-2022 (Rari Fuse) y Fei Labs abandonó el proyecto el 19-ago-2022. Lo documenta el propio Harvey en su deck de 2024; ver [12](12-decentralized-finance-the-future-of-finance.md).
- **Ramachandran** es inversionista de capital de riesgo cripto (vcsheet; no confirmé la fecha de ingreso).
- **Harvey:**
  - Declara asesorías con Man Group y Research Affiliates ([Disclosure](https://people.duke.edu/~charvey/Disclosure.htm)).
  - Su CV lista una beca de la University Blockchain Research Initiative (2022-2026) y el premio "*UBRI Educator, Blockchain Teacher of the Year*" (2020). **La UBRI la financia Ripple** ([Ripple](https://ripple.com/impact/ubri/)).
  - Vende el libro y dicta la especialización de Coursera ([12](12-decentralized-finance-the-future-of-finance.md)).
- **No verificado:** Amazon lista a Fred Ehrsam y Vitalik Buterin como colaboradores del libro (prólogos). No lo comprobé en el libro.

## 2. Acceso real (consultado el 25-sep-2026)

**Qué intenté, y fallé, para leer el documento de trabajo:**

- `papers.ssrn.com` y `ssrn.com`: 403, por el reto anti-bots de Cloudflare, con curl y con WebFetch.
- ResearchGate: 403.
- Internet Archive: la conexión se reinicia y WebFetch lo tiene bloqueado.
- Semantic Scholar y OpenAlex no registran otro PDF abierto; OpenAlex solo apunta a SSRN.
- El sitio del autor en Duke no aloja el documento de trabajo.
- Hay una copia de terceros ("*Duke University, August 2021*", en compoundmaven.com) detrás de un captcha. **No lo eludí.**
- Un PDF del **libro de Wiley** en un repositorio de GitHub de terceros: **lo descarté por ser piratería.**

**Qué sí leí, todo legal y del propio autor:**

| Fuente | Fecha | Nivel |
|---|---|---|
| Resumen de los 3 autores en el foro de Harvard Law, "*based on their recent paper*" ([enlace](https://corpgov.law.harvard.edu/2021/01/14/defi-and-the-future-of-finance/)) | 14-ene-2021 | Íntegro |
| Harvey, "*DeFi and the foundation of a new finance*", VBA Journaal 150, pp. 28-30 ([PDF en el sitio de Duke](https://people.duke.edu/~charvey/Research/Published_Papers/F7_DeFi_and_the.pdf)) | 2022 | Íntegro |
| Deck 4, "Problems DeFi Solves" (42 láminas), del curso 562F de Duke | 6-mar-2021 | Íntegro (texto) |
| Deck 6, "Risks" (92 láminas) | 16-mar-2021 | Íntegro (texto) |
| Deck 5, "Deep Dive" (210 láminas): MakerDAO, Compound, Aave, Uniswap, Balancer, Yield, dYdX, Synthetix | 8-mar-2021 | Sección: ~45 láminas, localizadas por búsqueda de términos |
| Deck 2, "Infrastructure" (28 láminas) y Deck 3, "Primitives" (84 láminas) | 27-feb-2021 | Sección: stablecoins, MEV y pérdida impermanente |
| Deck 1, "Origins" (49 láminas) | 27-feb-2021 | No leído |

Los decks están en `people.duke.edu/~charvey/Teaching/562F_2021/Public_Presentations_562F/`. Los descargué al scratchpad; no se suben al repo.

**Nivel: resumen** (del documento de trabajo) **+ sección** (material del autor). **Nada de esta ficha debe citarse como "el documento de trabajo dice".**

## 3. Lo esencial

Etiquetas: [H] hecho con fuente · [I] inferencia · [O] opinión del autor.

1. **[O] Tesis** (foro de Harvard Law; deck 4). DeFi resuelve cinco problemas de las finanzas centralizadas: **control centralizado, acceso limitado, ineficiencia, falta de interoperabilidad y opacidad**. Las fintech que se montan en la banca actual "*are likely to be fleeting*"; las descentralizadas "*have the best chance to define the future of finance*".
2. **[H] Cifras de motivación:**
   - "*1.7 billion are unbanked*"; los comercios pierden 3% por venta con tarjeta; un emprendedor con un proyecto que rinde 20% no lo financia si la tarjeta le cobra 24% (foro de Harvard Law).
   - La transferencia de Western Union de 1873: $300 con $9.34 de comisión, 3.11% (cálculo propio). Hoy cuesta $46.99 en efectivo y $19.99 a cuenta (VBA 2022).
3. **[H] Contenido declarado del documento.** Según el resumen, cubre flash loans, *flash swaps*, AMM, DEX, gobernanza descentralizada, *initial DeFi offerings*, y análisis a fondo de Uniswap, MakerDAO, Compound, Aave, Yield Protocol, dYdX y Synthetix, más riesgos y "*winners and losers*".
4. **[H + cálculo] MakerDAO** (deck 5, láminas 8-14), comprobado en Python:
   - 5 ETH a $200 y colateralización mínima de 150% permiten acuñar hasta 666.67 DAI.
   - Con 500 DAI de deuda y el ETH a $150 (−25%), el cociente queda justo en 150%.
   - El *keeper* vende 3.333 ETH para cubrir 500 DAI, cobra 0.2 ETH y devuelve 1.467 ETH ($220). El incentivo equivale a **6% de la deuda**.
   - Equivalencia con Aave: HF = CR/1.5. El término "factor de salud" no aparece en estos decks.
5. **[H + cálculo] Compound** (láminas 31-35):
   - El factor de colateral va de 0 a 90, y el cociente requerido es 100/CF.
   - 100 DAI (CF 90) más 2 ETH a $200 (CF 60): 100/(0.8 × 60 + 0.2 × 90) = **151.5%**.
   - La gobernanza puede cambiar parámetros, congelar mercados y actualizar código (lámina 56).
6. **[H] Aave** (láminas 67-80): flash loans por **9 pb**; refinanciar una posición apalancada de Compound a Aave con un solo flash loan de 10,000 DAI; tasas estables; delegación de crédito.
7. **[H] Uniswap** (láminas 81-109):
   - k = x·y, y el precio implícito es el cociente de reservas.
   - "*The fees earned from trading volume must exceed impermanent loss*"; los pares de stablecoins minimizan la pérdida.
   - *Flash swap*: se devuelve en el otro activo del par. En el ejemplo de arbitraje se retiran 950 USDC, se compran 1,000 DAI y se devuelven 963, con 37 DAI de ganancia; la comisión es 0.30% × 960 ≈ 3 DAI.
8. **[H + cálculo] Balancer** (lámina 115). Con un aumento de 5 veces, la pérdida es 25.5% en un pool 50/50 y 3.88% en uno 95/5. Mi cálculo da −25.46% y −3.89%, este último si el 95% está en el activo que sube; con 5% en ese activo sería −9.68%.
9. **[H] dYdX** (láminas 143-168):
   - flash loans gratuitos ("*driven to zero given that they are near risk free*");
   - perpetuos con índice de 7 exchanges;
   - margen de mantenimiento de 5%: con el BTC a 10,500, un corto queda en 11,000/10,500 − 1 = 4.76% y se liquida.
10. **[H + error] Yield Protocol** (lámina 128): un yToken a 0.92 asegura 8.7% fijo. La lámina escribe "[(0.08/0.92) − 1]", que no da 8.7%. La expresión correcta es 1/0.92 − 1 = 8.70%.
11. **[H] Taxonomía de riesgos** (deck 6):
    - contrato inteligente: error lógico o explotación económica (*flash attack*);
    - gobernanza;
    - DNS;
    - oráculo: un oráculo es vulnerable "*if an oracle's Cost of Corruption is ever less than an attacker's potential Profit from Corruption*";
    - escalabilidad;
    - DEX;
    - custodia;
    - regulación.
12. **[O] Oráculos:** "*Oracles, as they exist today, represent the highest risk to DeFi protocols... the largest systemic threat to DeFi today*" (deck 6, lámina 54). Esto contrasta con la clase de Juels ([06](06-decentralized-finance-mooc.md)).
13. **[O→H] Predicción de gobernanza que se cumplió.** En mar-2021 escribió: "*We have not yet experienced a successful governance attack on any Ethereum-based DeFi project, but little doubt exists that a financially equipped adversary will eventually attack a protocol*".
    - El 17-abr-2022, un atacante usó un flash loan para comprar votos en Beanstalk: el protocolo perdió $182 M y el atacante se quedó con ~$80 M ([CoinDesk](https://www.coindesk.com/tech/2022/04/17/attacker-drains-182m-from-beanstalk-stablecoin-protocol); [Cointelegraph](https://cointelegraph.com/news/beanstalk-farms-loses-182m-in-defi-governance-exploit)).
14. **[H + error] The DAO** (deck 6):
    - ~$150 M, 14% de todo el ether, reunidos en abr-2016;
    - el ataque de reentrada del 17-jun-2016 se llevó ~$50 M, 30% del contrato;
    - el *hard fork* del 20-jul-2016, en el bloque 1,920,000, creó ETC.
    - La lámina fecha el dictamen de la SEC el "*July 26, 2016*". El *Report of Investigation* (Release 34-81207) es del **25-jul-2017** ([SEC](https://www.sec.gov/files/litigation/investreport/34-81207.pdf)).
15. **[H] Stablecoins en 2021** (deck 2):
    - USDT: $24 mil M de capitalización, "*no regular audit*";
    - USDC: $5 mil M;
    - DAI: $1.5 mil M.
    - Las algorítmicas se describen como modelos de señoreaje con bonos; el problema de una stablecoin descentralizada que escale "*is still an open problem*". Aquí es donde aparece Fei, el conflicto de interés de §1.
16. **[H] MEV** (deck 3, láminas 9-11): "*Miner extractable value... a measure of the profit that the miner could make by including, excluding or re-ordering transactions... a drawback to the proof-of-work model*". Se mitiga ocultando transacciones; cita a Paradigm Research.
17. **[H] Escalabilidad** (deck 6): "*Ethereum is currently limited to a maximum of 15 TPS*", contra 65,000 de Visa; "*Optimistic rollups have yet to deliver functional mainnets*" (mar-2021). Envejeció rápido: en ago-2021 Finematics ya presentaba Optimism y Arbitrum como "*the most popular options*" entre los rollups optimistas ([03](03-finematics.md)).
18. **[H] Custodia** (deck 6): hackeos de exchanges:
    - Mt. Gox (2011-2014): 850k BTC;
    - Bitfinex (2016): 120k BTC;
    - Coincheck (2018): ~$500 M en NEM;
    - Binance (2019): 7k BTC.
    - "*The insurance is only as good as the health of the insurer*".
19. **[O] Visión:** "*DeFi is set to revolutionize finance*"; "*I believe we are less than 1% into the DeFi disruption*" (VBA 2022).
20. **[I] Cobertura de lo que exige este estudio:**
    - Terra y USDC/SVB son posteriores a este material (ver [12](12-decentralized-finance-the-future-of-finance.md), que sí los trata, y [06](06-decentralized-finance-mooc.md)).
    - La derivación de la pérdida impermanente no aparece en lo que leí: solo definición y ejemplos.
    - Los ataques de oráculo y flash loan aparecen como *flash attack* sobre bZx (deck 6, lámina 13).

## 4. Qué cambia para invertir

- **[I] Lista de riesgos útil para BTC.** La taxonomía de ocho riesgos sirve para evaluar cualquier vehículo DeFi que toque BTC. Por ejemplo, un BTC envuelto como WBTC suma riesgo de custodia, de contrato y de gobernanza al riesgo de precio del BTC. Nuestra cuenta tiene BTC nativo en Binance: su riesgo relevante es el **custodial** del exchange, que Harvey ilustra con Mt. Gox y Bitfinex.
- **[I] Cascadas.** El ejemplo de Maker muestra el canal: la liquidación vende ETH y "*exerts positive price pressure on DAI*". Agregado a escala, presiona a la baja el precio del colateral.
  - El 10-oct-2025 el canal dominante no fue DeFi sino los perpetuos: más de $19 mil M liquidados frente a ~$180 M en Aave. El BTC cayó de $122,574 a $104,782, −14.5% dentro del día (ver capítulo §4).
- **[I] Por qué no usamos rendimientos DeFi.** Harvey enumera el *yield farming* entre cuatro formas de "invertir en DeFi" (deck de 2024, en [12](12-decentralized-finance-the-future-of-finance.md)).
  - Nuestro mandato es spot.
  - Su propia lista de riesgos muestra que ese rendimiento paga contrato, oráculo, gobernanza y pérdida impermanente: primas que no sabemos valuar y cuya pérdida es de cola.
  - El caso Fei (§1) muestra que ni los autores del libro evaluaron bien su propio diseño.
- **[I] Señales derivadas de su marco:**
  1. oráculos cuyo costo de corrupción sea menor que la ganancia posible, como precios de pools poco líquidos;
  2. tokens de gobernanza baratos frente al valor que controlan (Beanstalk);
  3. stablecoins respaldadas por su propio token;
  4. concentración custodial.

## 5. Contrapuntos y límites

- **Límite de acceso:** no leí el documento de trabajo. Las diapositivas pueden simplificar o diferir del texto.
- **Tesis no probada:** que DeFi reduzca costos y desigualdad no se demuestra con datos en el material que leí.
  - [I] El préstamo DeFi exige sobrecolateralización, así que no atiende a quien no tiene activos: choca con el argumento de inclusión de "1.7 mil millones de no bancarizados".
- **Conflictos:**
  - el coautor promovía Fei;
  - el autor principal recibe fondos de la UBRI (Ripple) y vende libro y curso.
- **Errores detectados:**
  - la fecha del dictamen de la SEC sobre The DAO (2016 en lugar de 2017);
  - la fórmula del yToken;
  - "15 TPS" como techo, que envejeció.
- **Qué envejeció bien:**
  - el énfasis en el riesgo de oráculo: Iron Finance cayó con un TWAP rezagado (ver [03](03-finematics.md));
  - la predicción del ataque de gobernanza: Beanstalk (2022).
- **Qué envejeció mal:**
  - Fei como stablecoin "*decentralized and scalable*";
  - el pesimismo sobre los rollups optimistas;
  - la hoja de ruta de "Ethereum 2.0" con fragmentación (*sharding*).

## 6. Autoexamen

1. **Con 5 ETH a $200 y colateralización de 150%, ¿cuánto DAI se puede acuñar? Si se acuñan 500 y el ETH baja a $150, ¿qué pasa, y cuánto cobra el *keeper* como porcentaje de la deuda?**
   - *Respuesta:* hasta 666.67 DAI. A $150 el cociente es 750/500 = 150%, justo en el umbral.
   - Se venden 3.333 ETH para pagar 500 DAI, el *keeper* recibe 0.2 ETH ($30, 6% de la deuda) y se devuelven 1.467 ETH ($220).
   - *Fuente:* Harvey, deck 5 (2021), láminas 8-14; cálculo propio.
2. **En Compound, con $100 en DAI (CF 90) y $400 en ETH (CF 60), ¿cuál es el cociente de colateralización requerido?**
   - *Respuesta:* 100/(0.8 × 60 + 0.2 × 90) = 100/66 = 151.5%.
   - *Fuente:* deck 5, lámina 35.
3. **¿Cuál es la condición de Harvey para que un oráculo sea vulnerable, y cómo la ilustra el ataque a bZx?**
   - *Respuesta:* que el costo de corromperlo sea menor que la ganancia posible.
   - En bZx, mover el precio de sUSD/ETH en Uniswap y Kyber, pools poco líquidos, costaba poco comparado con lo que se podía pedir prestado contra ese precio. El flash loan eliminó incluso el costo de capital.
   - *Fuente:* deck 6, láminas 10-13 y 50; Qin et al. (ver [06](06-decentralized-finance-mooc.md)).
4. **¿Por qué el pasaje sobre Fei del deck de 2021 es una bandera roja metodológica, y qué pasó después?**
   - *Respuesta:* presenta como solución al "problema abierto" de las stablecoins descentralizadas el protocolo fundado por uno de los coautores, sin declarar el conflicto en la lámina.
   - Fei tuvo un arranque inestable, sufrió el hackeo de $80 M de Rari Fuse (abr-2022) y cerró en ago-2022.
   - *Fuente:* deck 2 (2021), lámina 24; deck de Infraestructura de 2024, láminas 124-130.

## 7. Grado de evidencia: **C**

- **Por qué C:** es un académico con método visible, y la mecánica es verificable; la verifiqué.
- **Por qué no más alto:**
  - el material es divulgativo y no revisado por pares;
  - la tesis central (DeFi resuelve cinco problemas) es normativa y viene sin evidencia empírica en lo que leí;
  - hay conflictos serios (Fei, Ripple/UBRI) y errores de fecha y fórmula;
  - no leí el documento de trabajo. **Pendiente:** volver a intentar SSRN desde un navegador con sesión humana y leerlo completo antes de subir el grado.
