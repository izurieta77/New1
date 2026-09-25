# Historial de pronósticos de un tercero: Galaxy Research, "26 Crypto, Bitcoin, DeFi, and AI Predictions for 2026"

**Qué es y qué no es:**
- Es el seguimiento del **historial de pronósticos de Galaxy Research**, un tercero, al **25-sep-2026**.
- **No son pronósticos nuestros:** no se registran en `bitacora/pronosticos.csv` ni cuentan para nuestro Brier.
- Los estudió `analista-cripto` para el recurso 35 del índice (`conocimiento/cripto/recursos/35-26-predictions-for-crypto-in-2026.md`).

**Fuente:**
- https://www.galaxy.com/insights/research/predictions-2026-crypto-bitcoin-defi, publicado el **18-dic-2025**.
- Autores: Alex Thorn (director de investigación), Jianing Wu, Zack Pokorny, Lucas Tcheyan, Christopher Rosa, Will Owens, Marc Hochstein y Thaddeus Pinakiewicz.
- Acceso: **íntegro**. Leí el texto web completo, con la revisión de las predicciones de 2025 y los avisos legales.

**Reglas de este seguimiento:**
- **Texto literal:** es la frase principal de cada predicción, copiada del original en inglés.
- **Criterio de resolución:** lo fijé yo antes de calificar, para que cualquiera pueda verificarlo. Donde el original es vago, lo digo.
- **Fecha de resolución:** 31-dic-2026 salvo otra indicación.
- **Estados:**
  - **cumplida:** el criterio ya se satisfizo;
  - **fallida:** el criterio ya es imposible o ya se violó;
  - **en curso:** ninguna de las dos.
- Galaxy **no asigna probabilidades**, así que no hay Brier: solo tasa de aciertos.

## Resumen al 25-sep-2026

| Estado | n | Predicciones |
|---|---|---|
| **Cumplidas** | **4** | #7 exención de innovación de la SEC · #10 consolidación de stablecoins con socios de TradFi · #23 ≥5 DAT forzadas a vender o cerrar · #25 investigación federal sobre mercados de predicción |
| **Fallidas** | **2** | #4 ninguna reducción de inflación de Solana en 2026 (SGP-0002 aprobada el 28-ago) · #16 tasas de préstamo en DeFi ≤10% (abr-2026: más de 12.6%) |
| **En curso** | **20** | Todas las demás. De ellas, **8 van claramente atrás de su meta**: #12, #15, #17, #19, #20, #22, #26 y #1 (esta resuelve en 2027). Otras 7 no tienen un dato público que yo haya podido verificar: #2, #3, #5, #6, #14, #21 y #24 |

**Lectura [I, nuestra]:**
- Acertó en **tendencias institucionales y regulatorias**: exención de la SEC, consorcios bancarios, cierres de DAT e investigaciones.
- Falló en dos predicciones de **"no pasará nada"** (inflación de Solana, tasas tranquilas), justo las que se rompen con un evento de cola.
- Las predicciones de **flujos y precios** van muy por debajo de su meta: ETF, préstamos, monedas de privacidad y BTC. El sesgo es alcista, como era de esperar de una casa con posiciones.
- **Historial previo:** según su propia calificación, Galaxy acertó **7 de 23** predicciones para 2025 (30%) y falló 16. Es autoevaluación; no la audité.

## Conflictos de interés y antecedentes (verificados)

- **Caso LUNA con la Fiscalía General de Nueva York (fuente primaria).**
  - **Documento:** *Assurance of Discontinuance* No. 25-011 de la Fiscalía General de Nueva York (Letitia James), firmado por Galaxy el 24-mar-2025 y por la Fiscalía el **27-mar-2025**: https://ag.ny.gov/sites/default/files/settlements-agreements/galaxy-digital-holding-ltd-et-al-assurance-of-discontinuance-2025.pdf
  - **Acuerdo:** Galaxy Digital Holdings Ltd. y cuatro filiales pagan al Estado de Nueva York **US$200,000,000 como devolución de ganancias** para cerrar la investigación (¶122, p. 37 del PDF).
  - **Conducta investigada:** promovió LUNA mientras vendía sin revelar que tenía la intención de hacerlo. La ley aplicada es la Martin Act y el art. 63(12) de la Ley Ejecutiva de Nueva York. El periodo va del 27-oct-2020 al 18-may-2022.
  - **Compra en el origen:** Galaxy compró 18,513,120 LUNA a Terraform a US$0.22, ≈ 30% debajo del mercado.
  - **Admisión:** los demandados "neither admit nor deny" los hallazgos (¶118).
  - **Precisión sobre la frase del índice** ("Galaxy pagó US$200 M en 2025"): el acuerdo se **firmó** en 2025 por US$200 M, pero se paga en **cuatro partes**:
    - US$40 M a 15 días;
    - US$40 M al año;
    - US$60 M a los dos años;
    - US$60 M a los tres años, es decir, en 2028.
  - Lo correcto es "acordó pagar US$200 M en 2025". The Block y Debevoise publicaron la noticia en mar-abr-2025.
- **Posiciones propias:** el aviso legal del artículo dice que "Participants, along with Galaxy Digital, hold a financial interest in Bitcoin, Ethereum, Hyperliquid, Solana, and Tether". Galaxy también opera y cubre esos activos y da servicios a vehículos que invierten en ellos, "If the value of such assets increases… Galaxy Digital's service fees may increase accordingly".
- **Salida a bolsa:** Galaxy cotiza en EUA desde 2025. En el mismo texto cuenta que "10 crypto-related companies (including Galaxy) successfully IPO'd or uplisted in the U.S." en 2025.

## Las 26 predicciones

### Precio de bitcoin

**#1** — "BTC will hit $250k by year-end 2027. 2026 is too chaotic to predict, though Bitcoin making new all-time highs in 2026 is still possible." (Alex Thorn)
- **Criterio:**
  - Principal: cierre diario de BTC-USD ≥ US$250,000 en o antes del 31-dic-2027 (Coin Metrics `PriceUSD` o Yahoo).
  - Secundario (no binario): nuevo máximo histórico en 2026.
- **Estado: en curso.**
  - BTC cerró en **US$84,386.58** el 24-sep-2026 (Coin Metrics); para llegar a la meta necesita **+196%**.
  - En 2026 el máximo de cierre fue US$97,044 (14-ene). El máximo histórico de cierre sigue siendo US$124,824 (6-oct-2025); Galaxy dice que el intradía fue US$126,080. **No hubo nuevo máximo histórico en 2026** hasta la fecha.
  - Contexto: el texto decía que las opciones daban "about equal odds of $70k or $130k for month-end June 2026". BTC cerró junio en **US$58,525**, debajo de los dos.
- **Resolución:** 31-dic-2027.

### Capas 1 y capas 2

**#2** — "The total market cap of Internet Capital Markets on Solana will surge to $2 billion (it's currently ~$750 million)." (Lucas Tcheyan)
- **Criterio:** capitalización agregada de los tokens de "Internet Capital Markets" en Solana ≥ US$2 mil M al 31-dic-2026, medida con la misma fuente que usó Galaxy.
  - El texto **no dice qué fuente ni qué lista de tokens usó**. Sin eso, la predicción no se puede verificar tal como está escrita.
- **Estado: en curso, sin dato verificable.** No encontré un índice público de "ICM en Solana" en lo que revisé. El token llamado "ICM" no sirve como medida porque es un token aislado.
- **Resolución:** 31-dic-2026.

**#3** — "At least one live, general-purpose Layer-1 blockchain will enshrine a revenue-generating application to funnel value directly back to its native token." (Lucas Tcheyan)
- **Criterio:** una L1 de propósito general ya en producción (no una L1 de una sola app, como Hyperliquid) activa en 2026, por gobernanza o por una actualización del protocolo, una aplicación nativa que genere ingresos y los canalice a su token (quema, reparto o recompra).
- **Estado: en curso.** No lo encontré en lo que revisé.
- **Resolución:** 31-dic-2026.

**#4** — "No Solana inflation reduction proposal will pass in 2026 and the current proposal, SIMD-0411, will be withdrawn without a vote." (Lucas Tcheyan)
- **Criterio:** cumplida solo si **ninguna** propuesta de reducir la inflación de SOL se aprueba en 2026 **y** SIMD-0411 se retira sin votarse.
- **Estado: FALLIDA el 28-ago-2026.**
  - La votación SGP-0002, que implementa la **SIMD-0550** ("Double Disinflation Rate": la desinflación pasa de −15% a −30% anual), se **aprobó con 67.001%**, contra un umbral de dos tercios.
  - Votaron 176.29 M SOL a favor, 66.19 M en contra y 20.63 M en abstención, de 1,326 validadores.
  - Fuentes: resultados de P2P.org y crypto.news/Crowdfund Insider; el texto de la SIMD-0550 está en github.com/solana-foundation/solana-improvement-documents.
- **Matiz:** la segunda mitad sí se cumplió. La SIMD-0550 dice que "the same change was previously proposed as SIMD-0411" y que regresa "now that governance tooling is ready", así que la 0411 se cerró sin votarse. Pero la predicción es una conjunción.
- **Resolución:** ya resuelta.

**#5** — "Corporate L1s will graduate from pilots to real settlement infrastructure. At least one Fortune 500 bank, cloud provider, or ecommerce platform will launch a branded corporate L1 that settles more than $1 billion of real economic activity in 2026 and runs a production bridge into public DeFi." (Christopher Rosa)
- **Criterio:** se cumplen las tres cosas en 2026:
  1. un banco, proveedor de nube o plataforma de comercio electrónico de la Fortune 500 lanza una L1 con su marca;
  2. esa L1 liquida más de US$1 mil M de actividad real en 2026, según un dato publicado;
  3. tiene un puente en producción hacia DeFi pública.
- **Estado: en curso.**
  - La nota de Fortune del 21-sep-2026 da la foto: Arc, de Circle, arrancó su red principal en septiembre (Circle es emisor de stablecoins, no banco, nube ni comercio electrónico); Tempo, de Stripe, y Robinhood Chain seguían sin lanzarse; Canton está respaldada por JPMorgan, pero no es una L1 con marca de un banco.
  - No encontré ninguna que cumpla las tres condiciones.
- **Resolución:** 31-dic-2026.

**#6** — "The ratio of application revenue to network revenue will double in 2026." (Lucas Tcheyan)
- **Criterio:** la razón agregada ingresos de aplicaciones ÷ ingresos de red en 2026 es ≥ 2 veces la de 2025, con la misma fuente (Blockworks o Token Terminal).
- **Estado: en curso.** No encontré en lo que revisé un dato comparable para 2025 y 2026.
- **Resolución:** 31-dic-2026; el dato completo estará en ene-2027.

### Stablecoins y tokenización

**#7** — "The SEC will grant some form of exemptive relief for expanding the use of tokenized securities in DeFi under its "innovation exemption" program." (Alex Thorn)
- **Criterio:** la SEC emite en 2026 una exención (orden, no-action letter o "innovation exemption") que permite negociar valores tokenizados on-chain con AMM o pools de liquidez.
- **Estado: CUMPLIDA el 17-sep-2026.**
  - Comunicado **2026-90** de la SEC, "SEC Issues 'Innovation Exemption' to Facilitate the Trading of Tokenized NMS Stock".
  - Es una exención temporal de 5 años (al 17-sep-2031):
    - libera de la definición de "exchange" a los *Tokenized Securities Venues* que usan AMM y pools;
    - libera de la definición de "dealer" a los proveedores de liquidez.
  - Pide comentarios del público.
- **Matiz:** el entorno es **con permisos**, con KYC. Los contratos deben estar en un "public, permissionless distributed ledger", pero no es DeFi abierta. La parte del texto sobre "DeFi markets on public blockchains" se cumple **parcialmente**.
- **Resolución:** ya resuelta.

**#8** — "The SEC will face a lawsuit by a traditional market participant or trade group over the innovation exemption." (Alex Thorn)
- **Criterio:** en 2026 una empresa o gremio de las finanzas tradicionales presenta ante un tribunal federal una demanda o una petición de revisión contra la exención de innovación.
- **Estado: en curso.**
  - Al 25-sep no encontré ninguna demanda.
  - SIFMA emitió un comunicado crítico el 17-sep-2026 ("concerned about its impact on investor protection and market integrity"), pero **no anunció litigio**.
  - CoinDesk reportó el 13-ago-2026 que Citadel y SIFMA habían cabildeado contra la exención.
- **Resolución:** 31-dic-2026.

**#9** — "Stablecoins will overtake ACH in transaction volume." (Thad Pinakiewicz)
- **Criterio estricto:** volumen de stablecoins de **todo 2026** (Artemis, ajustado) > volumen de ACH de 2026 (reporte anual de Nacha).
- **Estado: en curso, adelantada.**
  - Con Artemis, citado por CoinMarketCap, el volumen ajustado de 30 días fue de **US$7.2 billones en feb-2026 contra 6.8 billones de ACH**: la primera vez que las stablecoins lo superaron en un mes. En marzo sumó 7.5 billones, "matching" a ACH.
  - La comparación anual se resuelve con los datos de Nacha a inicios de 2027.
- **Advertencia:** la definición de "ajustado" de Artemis no es la de a16z/Allium, que daba US$9 billones **en 12 meses** a sep-2025. Ver cap. 05.
- **Resolución:** 31-dic-2026; el dato llega en 2027.

**#10** — "TradFi-partnered stablecoins will consolidate." (Jianing Wu)
- **Criterio:** la predicción es vaga. Defino: en 2026 se anuncia al menos una fusión o integración entre emisores, o un consorcio de 5 o más instituciones financieras tradicionales para emitir **una sola** stablecoin en común.
- **Estado: CUMPLIDA el 1-sep-2026** (con un criterio laxo).
  - **21 bancos y gestoras** (Bank of America, Citi, Goldman Sachs, Wells Fargo, UBS, Deutsche Bank, Santander y Fidelity, entre otros) se comprometieron a crear una empresa conjunta que emitirá una stablecoin en USD, con lanzamiento en el 1S27 (Fintech Futures y Blockhead, 1-2-sep-2026).
  - Antes, en jun-2026, más de 140 empresas presentaron el consorcio Open USD.
- **Matiz:** la participación de las stablecoins de TradFi sigue siendo marginal. Con CoinGecko al 25-sep: PYUSD US$2.70 mil M y USDG US$3.25 mil M, contra US$183.75 mil M de USDT.
- **Resolución:** ya resuelta.

**#11** — "A major bank/broker will accept tokenized equities as collateral." (Thad Pinakiewicz)
- **Criterio:** un banco o casa de bolsa relevante de las finanzas tradicionales (no un exchange cripto ni un protocolo DeFi) acepta en 2026 depósitos on-chain de acciones tokenizadas como garantía, con el mismo trato que las acciones tradicionales.
- **Estado: en curso.** Hay avances cerca del criterio, pero ninguno lo cumple:
  - Bybit, un exchange cripto, aceptó acciones tokenizadas como garantía el 31-jul-2026;
  - Coinbase lanzó acciones tokenizadas en Base para clientes fuera de EUA en ago-2026;
  - Aave V4 en Base las aceptó como garantía el 25-sep-2026 (The Block).
  - No encontré a un banco o bróker tradicional.
- **Resolución:** 31-dic-2026.

**#12** — "Card networks will plug into public blockchain rails. At least one top three global card network will route more than 10% of its cross-border settlement volume through public-chain stablecoins in 2026…" (Christopher Rosa)
- **Criterio:** Visa, Mastercard u otra de las tres primeras reporta que más de 10% de su volumen de liquidación transfronteriza de 2026 pasó por stablecoins en cadenas públicas.
- **Estado: en curso, muy improbable.**
  - La liquidación con stablecoins de Visa superó un ritmo anualizado de **US$20 mil M** (The Block, 8-sep-2026; era 7 mil M en abr-2026 según CoinDesk). Eso es **0.12%** de su volumen total del año fiscal 2025, que fue US$16.7 billones.
  - Visa no publica en dólares su volumen de liquidación transfronteriza, así que el 10% **no se puede verificar directamente**.
- **Resolución:** 31-dic-2026.

### DeFi

**#13** — "Decentralized exchanges will capture more than 25% of combined spot trading volume by the end of 2026." (Will Owens)
- **Criterio:** en dic-2026, volumen spot en DEX ÷ (DEX + CEX) > 25% (The Block).
  - Si se usa la serie DEX/CEX de The Block, que parece ser la base de Galaxy ("15%-17%"), se reportan ambas.
- **Estado: en curso.**
  - The Block, 3-ago-2026: la razón DEX/CEX de julio fue **24%**, récord (contra 17% un año antes).
  - Como proporción del total combinado equivale a 0.24/1.24 ≈ **19.5%**.
- **Resolución:** 31-dic-2026.

**#14** — "There will be more than $500 million worth of DAO treasury assets governed exclusively by futarchy." (Zack Pokorny)
- **Criterio:** la suma de las tesorerías de DAO gobernadas **solo** por futarquía es > US$500 M al 31-dic-2026. La base de Galaxy era ≈ US$47 M.
- **Estado: en curso, sin dato agregado.** Solo encontré la tesorería propia de MetaDAO, de ≈ US$11-12 M. No encontré el agregado.
- **Resolución:** 31-dic-2026.

**#15** — "Total crypto-backed loans outstanding will clear $90 billion using an end-of-quarter snapshot." (Zack Pokorny)
- **Criterio:** el reporte trimestral de préstamos de Galaxy muestra más de US$90 mil M al cierre del 3T26 o del 4T26.
- **Estado: en curso, improbable.**
  - Según el propio reporte de Galaxy para el 2T26 (Cryptobriefing y Yahoo Finance), los préstamos con garantía cripto **bajaron US$11.33 mil M (−16.78%), a US$56.16 mil M**.
  - El pico fue de 78.69 mil M en el 3T25.
  - Llegar a la meta exige +60%.
- **Resolución:** 31-dic-2026; el dato llega en 2027.

**#16** — "Stablecoin interest rate volatility will remain tame and borrow costs will not exceed 10% through DeFi applications." (Zack Pokorny)
- **Criterio:** la tasa variable de préstamo en USDC o USDT de los grandes mercados DeFi (Aave v3 en Ethereum) no supera 10% en ningún dato diario de 2026.
- **Estado: FALLIDA el 19-abr-2026.**
  - El 18-abr-2026 hackearon el puente de rsETH de KelpDAO. Los mercados de ETH, USDT y USDC de Aave llegaron al **100% de utilización**; USDT se quedó arriba de 99% durante 135 horas seguidas (CoinDesk, 20 y 21-abr-2026).
  - Con DefiLlama, el rendimiento **para el depositante** de USDC en Aave v3 Ethereum fue de **12.60%** el 19 y 20-abr y estuvo arriba de 10% durante 6 días. Como la tasa del prestatario siempre es mayor que la del depositante, la de préstamo pasó de 12.6%.
  - Cálculo propio con la API gratuita de DefiLlama: el endpoint de tasa de préstamo es de pago, así que usé el de depósito.
- **Resolución:** ya resuelta.

**#17** — "The combined market cap of privacy tokens will exceed $100b by end of 2026." (Christopher Rosa)
- **Criterio:** capitalización de la categoría "privacy" de CoinMarketCap > US$100 mil M al 31-dic-2026. Galaxy partía de US$63 mil M con esa misma categoría.
- **Estado: en curso, lejos.**
  - Con CoinGecko al 25-sep-2026: la categoría amplia "Privacy" suma **US$62.8 mil M** y la estrecha "Privacy Coins" **US$37.0 mil M**.
  - Faltan +59% en la amplia.
  - No consulté CoinMarketCap.
- **Resolución:** 31-dic-2026.

**#18** — "Weekly trading volumes on Polymarket will consistently exceed $1.5 billion in 2026." (Will Owens)
- **Criterio:** "consistently" es vago. Defino: al menos 80% de las semanas de 2026 con volumen de Polymarket (internacional más EUA) > US$1.5 mil M, según Dune o DeFi Rate.
- **Estado: en curso, con datos parciales.**
  - Récord de US$2.1 mil M en una semana de marzo (Dune, vía Bitget).
  - US$1.9 mil M en la semana al 10-may.
  - Más de US$4 mil M combinados en julio (Proactive Investors).
  - En agosto: EUA US$870 M y la plataforma internacional ≈ US$1.2 mil M.
  - No verifiqué semana por semana, y enero-febrero probablemente estuvieron por debajo.
- **Resolución:** 31-dic-2026.

### Finanzas tradicionales

**#19** — "More than 50 spot altcoin ETFs, and another 50 crypto ETFs (excluding spot single-coin products), will launch in the U.S." (Jianing Wu)
- **Criterio:** en 2026 se lanzan en EUA 51 o más ETF spot de altcoins **y** 51 o más ETF cripto de otro tipo (multiactivo, apalancados, etc.).
- **Estado: en curso, atrasada.**
  - A mediados de mayo iban **10 lanzamientos** spot de altcoins en 2026: 8 previos (Chainlink, Avalanche, Sui, Polkadot) más 2 de HYPE (CryptoSlate, 17-may-2026). Después salió el de Zcash (ZCSH).
  - Morningstar cuenta 140 ETP cripto listados en total en EUA (sep-2026), pero no todos son de 2026.
  - No encontré un conteo oficial de 2026.
- **Resolución:** 31-dic-2026.

**#20** — "U.S. spot crypto ETF net inflows will exceed $50 billion." (Jianing Wu)
- **Criterio:** la suma de flujos netos de 2026 de todos los ETF spot cripto en EUA (BTC, ETH y altcoins) es > US$50 mil M (Farside o SoSoValue).
- **Estado: en curso, muy improbable.**
  - Los ETF de BTC llegaron a **−US$5.69 mil M** en el año el 13-jul-2026.
  - El acumulado volvió a positivo el 22-sep: **+US$0.887 mil M** con Farside (CoinMarketCap) y ≈ +US$0.32 mil M con Bloomberg (Bitcoin.com, 24-sep).
  - No encontré el acumulado 2026 de ETH y altcoins.
  - Faltan ≈ US$49 mil M en 14 semanas.
- **Resolución:** 31-dic-2026.

**#21** — "A major asset-allocation platform will add bitcoin to its standard model portfolios." (Jianing Wu)
- **Criterio:** en 2026, una casa de bolsa tradicional (wirehouse) o una plataforma importante de asignación de activos anuncia que incluye un producto de BTC en sus portafolios modelo **estándar**.
- **Estado: en curso.**
  - No lo encontré para 2026. BlackRock ya había metido IBIT (1-2%) en sus modelos que admiten alternativos en feb-2025, antes de la ventana de la predicción.
  - Morgan Stanley lanzó su propio ETP de BTC (MSBT) el 8-abr-2026, pero eso no es incluirlo en portafolios modelo.
- **Resolución:** 31-dic-2026.

**#22** — "15+ crypto companies will IPO or uplist in the U.S." (Jianing Wu)
- **Criterio:** 15 o más empresas cripto o blockchain completan una IPO o un uplisting en bolsas de EUA en 2026.
- **Estado: en curso, atrasada.**
  - La única IPO grande que confirmé es **BitGo**, que debutó en NYSE el 22-ene-2026.
  - Grayscale pausó su IPO (CoinDesk, 28-may-2026). Kraken la pausó en marzo, Consensys la movió a otoño y Ledger la archivó.
  - No encontré un conteo de uplistings.
- **Resolución:** 31-dic-2026.

**#23** — "Five or more digital asset treasury companies (DATs) will be forced to sell assets, be acquired, or shut down completely." (Jianing Wu)
- **Criterio:** 5 o más DAT venden activos por necesidad (pagar deuda o capital de trabajo), son adquiridas o cierran en 2026, según reportes de prensa o documentos oficiales.
- **Estado: CUMPLIDA a más tardar en la semana del 21-jul-2026.** CoinDesk (2-abr y 24-jul-2026) reporta cinco casos:
  - **Empery Digital:** vendió 370 BTC para liquidar un crédito;
  - **Genius Group:** vendió sus últimos 84 BTC para pagar US$8.5 M de deuda;
  - **Nakamoto:** vendió ≈ 284 BTC en marzo para capital de trabajo;
  - **Smarter Web Company:** vendió 178 BTC el 23-jul para pagar un convertible;
  - **Satsuma:** sus accionistas aprobaron liquidar los 668 BTC y deslistarse de Londres.
  - Además, **Strategy** vendió BTC por primera vez: 32 BTC a fines de mayo, 1,638 a inicios de agosto y 1,690 a mediados de agosto, para dividendos de sus preferentes y recompras de STRC. Lo reporta CoinDesk con base en sus 8-K.
- **Resolución:** ya resuelta.

### Política

**#24** — "Some Democrats will take up debanking as an issue – and warm to cryptocurrency as an answer." (Marc Hochstein; el propio autor la llama "a longshot")
- **Criterio:** en 2026 al menos un legislador federal demócrata vincula públicamente el "debanking" de inmigrantes o trabajadores de bajos ingresos con las criptos o stablecoins como solución, en una declaración, un proyecto de ley o una audiencia.
- **Estado: en curso.**
  - No lo encontré en lo que revisé.
  - Hay un indicio en contra: The American Prospect publicó el 10-ago-2026 "Crypto Democrats Are Ghosting the Industry".
- **Resolución:** 31-dic-2026.

**#25** — "There will be a federal investigation into insider trading or game fixing connected to a prediction market." (Thad Pinakiewicz)
- **Criterio:** una autoridad federal de EUA (Congreso, DOJ, CFTC, SEC o FBI) abre en 2026 una investigación pública sobre uso de información privilegiada o arreglo de resultados ligado a un mercado de predicción.
- **Estado: CUMPLIDA el 22-may-2026.**
  - El presidente del Comité de Supervisión de la Cámara, James Comer, **abrió una investigación** sobre "the use of online prediction market platforms by some users to conduct insider trading", dirigida a Polymarket y Kalshi. Es fuente primaria: oversight.house.gov.
  - Contexto: la CFTC publicó un aviso de su división de enforcement sobre información privilegiada en mercados de predicción (25-feb-2026). Hay además reportes de sondeos federales (Forbes, 26-jun; NPR, 13-ago) y de que Polymarket remitió casos al DOJ (CNN, 21-ago).
- **Resolución:** ya resuelta.

### IA

**#26** — "Payments following the x402 standard will reach 30% of Base daily transactions and 5% of Solana non-vote transactions in 2026…" (Lucas Tcheyan)
- **Criterio:** los pagos x402 son al menos 30% de las transacciones diarias de Base **y** al menos 5% de las transacciones no-voto de Solana, en promedio de 30 días en algún momento de 2026. Un pico de un día no cuenta.
- **Estado: en curso, lejos.**
  - Con Artemis (CoinDesk, 11-mar-2026): ≈ **131 mil transacciones x402 al día** en marzo. El pico fue de 3.8 M en un día de febrero, "much of that… infrastructure testing", y ≈ la mitad de la actividad observada parece artificial.
  - En agosto Solana superó a Base en transacciones x402 diarias.
  - No encontré el porcentaje sobre el total de cada red.
- **Resolución:** 31-dic-2026.

## Cómo usar este historial

- **Para el torneo:** ninguna predicción de Galaxy es una señal de operación.
  - Su tasa de aciertos (30% en 2025, según ellos mismos) y su sesgo alcista las ponen en **grado D** como pronóstico.
  - Sirven como mapa de temas y como fuente de datos (su reporte de préstamos cripto es útil).
- **Revisión:** calificación final el **31-dic-2026**. Es un pendiente de la rutina 8 en la corrida de estudio de la primera semana de ene-2027; la #1 se revisa el 31-dic-2027.
- **Errores posibles de esta calificación:**
  - en las predicciones vagas (#10 y #18) el criterio lo fijé yo; otra persona podría calificar distinto;
  - la #16 se basa en la tasa del depositante de DefiLlama, que es una cota inferior de la tasa de préstamo.
