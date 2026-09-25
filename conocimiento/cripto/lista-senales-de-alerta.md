# Lista de señales de alerta: exchanges, stablecoins, tokens y proyectos

- **Uso:** la aplica el comité **antes de aprobar** un exchange, una stablecoin, un token o un protocolo. En el caso de Binance, también **cada semana** mientras la cuenta `arena-claude-binance` tenga saldo.
- **Autor:** `analista-cripto` (G4), 25-sep-2026. Se construyó con las fichas 08, 17, 22, 25, 32 y 33 de `recursos/`.
- **Etiquetas:** [H] hecho con fuente · [I] inferencia o umbral propuesto por mí (hay que calibrarlo) · [O] opinión.

## Cómo se aplica

1. Cada señal se califica **ROJA**, **ÁMBAR** o **LIMPIA**, y la calificación se anota con fecha y fuente.
2. **Regla de decisión** [I]:
   - una señal ROJA basta para no aprobar, salvo una excepción votada y documentada;
   - dos o más ÁMBAR obligan a votar en el comité con el gestor de riesgo, que tiene veto.
3. **Para lo ya aprobado:** una ROJA activa la contingencia de `bitacora/decisiones/2026-09-25-CRIPTO-inicial.md`, que dice: vender a MXN y retirar por SPEI; si falla, mover el BTC a Bitso.
4. **Fuentes aceptadas:** reguladores, tribunales, el propio emisor, datos on-chain reproducibles y prensa seria.
   - Las alertas de redes sociales valen como disparador de revisión, no como prueba. ZachXBT solo cuenta cuando trae una segunda fuente.
5. **Riesgo legal:** **no se acusa a personas** sin sentencia o fuente oficial. Se distingue entre acusado, demandado, sentenciado y absuelto.

---

## A. Exchange o custodio

| # | Señal | Nivel | Caso real que la respalda (fuente, fecha) |
|---|---|---|---|
| A1 | **Los activos del exchange o de su afiliada dependen de su token propio** | ROJA si es >25% del patrimonio o de las reservas | [H] **FTX:** el mayor activo de Alameda eran US$3.66 mil millones de FTT "desbloqueado", más US$2.16 mil millones de FTT como colateral, frente a US$8 mil millones de pasivos ([CoinDesk, 2-nov-2022](https://www.coindesk.com/business/2022/11/02/divisions-in-sam-bankman-frieds-crypto-empire-blur-on-his-trading-titan-alamedas-balance-sheet)). Quiebra el 11-nov-2022. [H] **AscendEX:** el 8-jul-2026, más de US$12 millones de sus ~US$13.45 millones estaban en su token ASD y en otro token ilíquido ([TechTimes, 12-jul-2026](https://www.techtimes.com/articles/320217/20260712/ascendex-froze-withdrawals-may-not-return-user-funds-after-mica-miss.htm)). |
| A2 | **Retiros lentos, "pendientes" o sin hash** mientras se siguen aceptando depósitos | ROJA | [H] **AscendEX:** restricciones desde may-2026 según un usuario; alerta pública el 26-jun; **cierre el 1-jul-2026** ([Cointelegraph, 26-jun y 9-jul-2026](https://cointelegraph.com/news/ascendex-exchange-reportedly-faces-liquidity-issues-claims-zachxbt)). [H] **Celsius** pausó retiros, intercambios y transferencias el 12-jun-2022 por "condiciones extremas de mercado" ([CoinDesk, 13-jun-2022](https://www.coindesk.com/policy/2022/06/13/crypto-lending-service-celsius-pauses-withdrawals-citing-extreme-market-conditions)). [H] **WOO X:** retiros pendientes 3 días en sep-2026; dijo que revisa los casos. |
| A3 | **Salidas netas anormales** de las carteras rastreadas | ÁMBAR con un flujo semanal < −2.1%; ROJA con < −5.3% (sección F) | [H] **Binance, dic-2022:** salidas netas de ~US$6 mil millones en 72 horas, según Nansen ([CoinDesk, 13-dic-2022](https://www.coindesk.com/markets/2022/12/13/binance-withdrawals-surge-as-concerns-about-its-reserve-report-spook-traders)). [I] En DefiLlama, la peor semana fue de −13.5% sin BNB (18-dic-2022). [H] **AscendEX:** reservas −US$240 millones el 20-jun-2026 (TechTimes). |
| A4 | **El auditor o atestador se retira**, o la PoR se suspende | ROJA | [H] **Mazars** pausó el 16-dic-2022 su trabajo de prueba de reservas para Binance, KuCoin y Crypto.com, por cómo "el público entiende" esos reportes ([CoinDesk, 16-dic-2022](https://www.coindesk.com/business/2022/12/16/binance-proof-of-reserves-auditor-mazars-pauses-all-work-for-crypto-clients)). |
| A5 | **PoR o "verificación" en fecha anunciada**, sin serie, con colchón mínimo o con **inyecciones temporales** | ÁMBAR | [H] **Tether, 2017:** "verificó" efectivo depositado esa misma mañana. **2018:** al día siguiente de la carta de Deltec, movió cientos de millones a Bitfinex ([NYAG, 23-feb-2021](https://ag.ny.gov/press-release/2021/attorney-general-james-ends-virtual-currency-trading-platform-bitfinexs-illegal)). [H] Bitfinex transfirió US$382 millones a Tether antes de una revisión programada ([CFTC, 15-oct-2021](https://www.cftc.gov/PressRoom/PressReleases/8450-21)). [H] **AscendEX:** una inyección de ~US$240 millones "llegó y se fue" en semanas (TechTimes). |
| A6 | **Empresa de trading afiliada** con privilegios, o **mezcla de fondos** de clientes | ROJA | [H] **FTX/Alameda:** SBF, **sentenciado** a 25 años (28-mar-2024; confirmado por el 2.º Circuito el 12-jun-2026). [H] **Tether/Bitfinex:** la CFTC encontró reservas mezcladas con los fondos operativos y de clientes de Bitfinex (15-oct-2021). |
| A7 | **Controles corporativos débiles:** sin estados auditados, sin conciliación, llaves mal resguardadas | ROJA | [H] **FTX:** su nuevo director declaró que nunca vio "un fracaso tan completo de los controles corporativos" (tribunal de quiebras, 17-nov-2022; [CNBC](https://www.cnbc.com/2022/11/17/ftx-ceo-shreds-bankman-fried-never-seen-such-a-failure-of-controls-.html)). |
| A8 | **Historial penal o regulatorio**, o **investigación abierta** | ÁMBAR con investigación; ROJA con cargos nuevos | [H] **Binance se declaró culpable** (AML y sanciones): US$4.3 mil millones en total, US$3.4 mil millones a FinCEN, US$968 millones a OFAC y un monitor por 5 años ([Tesoro, 21-nov-2023](https://home.treasury.gov/news/press-releases/jy1925)). [H] **Investigación del DOJ por sanciones a Irán, sin cargos** (Bloomberg, 22-sep-2026, vía [CoinDesk](https://www.coindesk.com/policy/2026/09/22/binance-probed-by-u-s-federal-prosecutors-for-sanctions-violations-bloomberg)). |
| A9 | **Sin licencia en tu jurisdicción**, o licencias retiradas o negadas | ÁMBAR; ROJA con aviso de restricción | [H] **Binance no está supervisada en México** (verificación del 25-sep-2026 en la bitácora). [H] **UE:** Binance retiró su solicitud MiCA el 24-jun-2026 y **desde el 1-jul-2026 solo permite retiros**, con ~6 días de aviso ([CoinDesk, 26-jun-2026](https://www.coindesk.com/policy/2026/06/26/binance-tells-eu-users-it-will-no-longer-provide-services-after-failing-to-secure-mica-license); Euronews, 25-jun-2026). [H] AscendEX cerró citando la falta de autorización MiCA. |
| A10 | **Hackeos no divulgados** o divulgados tarde | ROJA | [H] **CoinDCX:** ZachXBT alertó ~US$44 millones drenados antes del anuncio; luego CoinDCX confirmó ~US$44 millones (19-jul-2025; [CoinDesk](https://www.coindesk.com/web3/2025/07/19/indian-crypto-exchange-coindcx-suffers-44m-hack)). [H] Noones y BitoPro, "sin divulgar" según ZachXBT (una sola fuente, 2025). |
| A11 | **Hackeo mayor que el fondo de protección** o que el capital | ÁMBAR si el fondo lo cubre; ROJA si no | [H] **Bitget, 24-sep-2026:** US$351.6 millones en hot y warm wallets, con **retiros suspendidos**. Dice que su fondo de más de US$464 millones lo cubre ([CoinDesk, 25-sep-2026](https://www.coindesk.com/markets/2026/09/25/bitget-s-usd351-million-hack-happened-via-spoofed-transfers-not-private-keys-ceo-gray-chen-says)). [H] **Bybit, 21-feb-2025:** perdió US$1.46 mil millones, pero procesó el 99.994% de más de 350,000 retiros en 10 horas y reunió US$1.23 mil millones en ETH en dos días ([cronología de Bybit](https://www.bybit.com/en/learn/this-week-in-bybit/bybit-security-incident-timeline)). |
| A12 | **El token propio del exchange se desploma** o hay anuncio de cierre o "reestructura" | ROJA | [H] **BitMart** anunció su cierre ordenado el 26-jul-2026 y **BMX cayó 58%** ([CoinDesk](https://www.coindesk.com/markets/2026/07/26/crypto-exchange-bitmart-to-shut-down-after-nine-years-bmx-token-crashes-58)). Los retiros siguen abiertos hasta el 31-ene-2027. |
| A13 | **Fuga de datos de clientes** o personal sobornado | ÁMBAR | [H] **Coinbase, 8-K del 14-may-2025:** agentes de soporte sobornados filtraron datos de clientes; costo estimado de US$180-400 millones ([SEC](https://www.sec.gov/Archives/edgar/data/1679788/000167978825000094/coin-20250514.htm)). [H] Una filtración del fisco francés amplió las víctimas de ataques físicos (Chainalysis, 6-ago-2026). |
| A14 | **Colateral valuado con precios internos de mercados delgados** (margen, Earn, préstamos) | ÁMBAR, solo si se usan esos productos | [H] **Binance, 10-oct-2025:** USDe, BNSOL y WBETH perdieron la paridad en su mercado; **compensó ~US$283 millones** ([The Block](https://www.theblock.co/post/374295/binance-pays-283-million-in-compensation-following-fridays-depegs-covering-user-losses)). |
| A15 | **Comunicados vagos** ("los fondos están seguros") sin datos verificables, o avisos tardíos | ÁMBAR | [H] **AscendEX** avisó a los usuarios 5 días después de cerrar (TechTimes). [H] **Bitfinex** dijo en abr-2019 que los fondos de Crypto Capital estaban "incautados y resguardados", cuando no sabía dónde estaban (NYAG, 23-feb-2021). |

## B. Stablecoin

| # | Señal | Nivel | Caso real (fuente, fecha) |
|---|---|---|---|
| B1 | **Estabilidad "algorítmica"** o respaldo con un token propio; **rendimiento "sin riesgo" alto** | ROJA | [H] **UST/Terra:** Anchor pagaba 19.5% "libre de riesgo". En su pico había ~US$18 mil millones de UST, con US$16 mil millones en Anchor. El 9-may-2022, UST tocó **US$0.60 en Binance**, y la defensa de US$1.5 mil millones equivalía al 8.3% del circulante ([Fed de Richmond, jul-2022](https://www.richmondfed.org/publications/research/economic_brief/2022/eb_22-24)). |
| B2 | **Afirmaciones de respaldo falsas en el pasado** o sin auditoría | ROJA sin auditoría; ÁMBAR con historial pero auditado hoy | [H] **Tether:** reservas suficientes solo el 27.6% de los días de una muestra de 26 meses (CFTC, 15-oct-2021); multa de la fiscalía de Nueva York (23-feb-2021). **Mitigante:** KPMG emitió una opinión sin salvedades sobre los estados de 2025 ([CoinDesk, 13-ago-2026](https://www.coindesk.com/business/2026/08/13/tether-says-it-completed-long-promised-big-four-audit-of-finances-behind-usd180-billion-usdt-stablecoin)). |
| B3 | **Colchón delgado frente a activos volátiles** | ÁMBAR si una caída conjunta de <20% en los activos volátiles borra el excedente | [H] **Tether, 2T-2026:** excedente de US$4.11 mil millones (2.2% de los pasivos); BTC más oro suman US$24.64 mil millones. [I] Una caída conjunta de 16.7% borra el excedente (cálculo propio con la atestación de BDO; [CoinDesk, 31-jul-2026](https://www.coindesk.com/business/2026/07/31/tether-posts-usd1-5-billion-operating-profit-in-q2-as-reserve-buffer-falls-by-half)). |
| B4 | **Concentración en un banco** o custodio | ÁMBAR | [H] **USDC:** tenía US$3.3 mil millones en SVB, ~8% de sus reservas. Cayó a ~US$0.87-0.88 el 11-mar-2023 y recuperó la paridad cuando se garantizaron los depósitos ([Circle, 13-mar-2023](https://www.circle.com/pressroom/3-3-billion-of-usdc-reserve-risk-removed-dollar-de-peg-closes); CNN). |
| B5 | **Emisor en disputa** o con acusaciones públicas de insolvencia | ÁMBAR | [H] **FDUSD** perdió la paridad el 2-abr-2025 tras acusaciones públicas de insolvencia contra su emisor, que las negó. La caída fue de ~9% según [The Block](https://www.theblock.co/news/regulation/2025-04-02-tron-justin-sun-trueusd-fiduciary-insolvent-techteryx-tusd-first-digital-aria-349289), y llegó a US$0.87 en algunos mercados según BeInCrypto (extractos; discrepancia no resuelta). Decrypt la tituló "Binance-Backed FDUSD", es decir, respaldada por Binance. |
| B6 | **"Dólar sintético"** con colateral cripto o de derivados | ÁMBAR | [H] **USDe** bajó de US$0.66 en Binance el 10-oct-2025, según la cobertura (evento A14). |
| B7 | **Capacidad del emisor para congelar**, que puede usarse o no | ÁMBAR para montos grandes | [H] Circle y Tether congelaron ~US$318 mil del hackeo a Bitget (25-sep-2026). A Circle se le criticó no congelar ~US$232 millones de Drift (abr-2026) ([CoinDesk](https://www.coindesk.com/markets/2026/09/25/circle-and-tether-step-in-to-freeze-hacker-wallet-after-massive-bitget-crypto-heist)). |
| B8 | **Uso ilícito concentrado o sanciones** | ROJA si está sancionada | [H] Las stablecoins son el **84% del volumen ilícito**. **A7A5** movió US$93.3 mil millones y fue designada por OFAC en ago-2025 y por la UE en oct-2025 (Chainalysis, 8-ene y 5-mar-2026). |

## C. Token o protocolo (DeFi, puentes, proyectos)

| # | Señal | Nivel | Caso real (fuente, fecha) |
|---|---|---|---|
| C1 | **Llave de administrador con umbral bajo y sin timelock** | ROJA | [H] **Drift, 1-abr-2026:** multisig 2 de 5 **sin timelock**; prefirmas con "durable nonces"; ~US$285 millones, más de 50% del TVL ([Chainalysis, 9-abr-2026](https://www.chainalysis.com/blog/lessons-from-the-drift-hack/)). |
| C2 | **Un solo verificador o validador ("1 de 1")**, o quórum concentrado en una organización | ROJA | [H] **KelpDAO, 18-abr-2026:** un solo verificador con nodos RPC comprometidos; ~US$292 millones ([Chainalysis, 23-abr-2026](https://www.chainalysis.com/blog/kelpdao-bridge-exploit-april-2026/)). [H] **Ronin, mar-2022:** 5 de 9 llaves, 4 de ellas de la misma empresa; ~US$625 millones ([post-mortem](https://roninchain.com/blog/posts/back-to-building-ronin-security-breach-6513cc78a5edc1001b03c364)). |
| C3 | **Oráculo de precio spot o TWAP corto** con poca liquidez; **colateral nuevo aprobado sin control** | ROJA | [H] **Drift:** token falso (CVT) con un pool de ~US$500 aceptado como colateral (Chainalysis). [H] **Mango Markets** (oct-2022): manipulación de precio, ~US$110 millones. **Las condenas penales se anularon el 23-may-2025**; el juez invocó la sede y pruebas insuficientes de falsedad ([TRM Labs](https://www.trmlabs.com/resources/blog/breaking-federal-judge-overturns-all-criminal-convictions-in-mango-markets-case-against-avraham-eisenberg)). [H] Retos Puppet de DVDF (ficha 25). |
| C4 | **Gobernanza por votos del momento**, que se pueden conseguir con préstamo relámpago | ROJA | [H] **Beanstalk, 17-abr-2022:** ~US$182 millones ([CoinDesk](https://www.coindesk.com/tech/2022/04/17/attacker-drains-182m-from-beanstalk-stablecoin-protocol)). Reto Selfie de DVDF. |
| C5 | **Contratos actualizables sin retraso** o sin inicializar | ÁMBAR; ROJA si no hay timelock | [H] **Parity, nov-2017:** una librería sin inicializar se "mató" y congeló cientos de millones en ETH ([TechCrunch, 7-nov-2017](https://techcrunch.com/2017/11/07/a-major-vulnerability-has-frozen-hundreds-of-millions-of-dollars-of-ethereum)). Retos Climber y Wallet Mining de DVDF. |
| C6 | **"Auditado" presentado como garantía** | ÁMBAR | [H] Cyfrin: una revisión de seguridad es "acotada en tiempo" y no garantiza (ficha 22). [H] **KelpDAO:** "no fue una vulnerabilidad de contrato inteligente" (Chainalysis). |
| C7 | **Oferta concentrada**, actividad inorgánica, **liquidez on-chain mínima** frente a la capitalización | ROJA | [H] **MemeCore (M)** cayó más de 75%, de US$14 mil millones a US$3.8 mil millones de FDV (25-jun-2026), tras señalamientos públicos. Liquidez on-chain menor a US$100 mil, según ZachXBT (una sola fuente; ficha 08). |
| C8 | **Promoción por influencers** o "caridad" como gancho | ROJA | [H] **"Save the Kids" (2021):** tras el esquema de "pump and dump", FaZe Clan expulsó a un miembro y suspendió a tres ([Newsweek, jul-2021](https://www.newsweek.com/faze-clan-drop-kay-suspend-three-others-amid-crypto-scandal-1606251)). |
| C9 | **Rendimiento "garantizado"** de dos dígitos sobre dólares | ROJA | [H] Anchor, 19.5% (B1); **Celsius** pausó retiros el 12-jun-2022 (A2). |
| C10 | **El equipo no divulga incidentes** | ROJA | [H] **TeleSwap:** un exploit de más de US$735 mil el 15-jul-2026 seguía sin divulgarse 5 días después (ZachXBT, una sola fuente). |

## D. Operación propia y autocustodia

| # | Señal | Nivel | Caso real (fuente, fecha) |
|---|---|---|---|
| D1 | **Cualquier "soporte"** que pida la frase semilla, códigos o mover fondos a una "cartera segura" | ROJA: cortar el contacto | [H] Robos por suplantación de soporte:<br>• **US$243 millones** (ago-2024). En el proceso hay 18 acusados; el principal se declaró culpable el 8-sep-2026 ([Fortune](https://fortune.com/2026/09/07/malone-lam-bitcoin-rico-plea-doj-crypto-unit/)).<br>• **US$91.4 millones** (ago-2025).<br>• **US$282 millones** (ene-2026) ([CoinDesk](https://www.coindesk.com/business/2026/01/16/hacker-steals-usd282-milion-in-hardware-wallet-social-engineering-attack)). |
| D2 | **Firmar sin verificar en el dispositivo**, o firmas pendientes y prefirmadas | ROJA | [H] **Bybit, 21-feb-2025:** se alteró el JavaScript de la interfaz de Safe{Wallet} y la firma cambió la lógica de la cold wallet ([Sygnia](https://www.sygnia.co/blog/sygnia-investigation-bybit-hack/); [FBI](https://www.ic3.gov/PSA/2025/PSA250226)). [H] **Drift:** "durable nonces" (C1). |
| D3 | **Revelar tenencias** o tener datos KYC expuestos | ÁMBAR | [H] **Ataques físicos:** US$58 millones en 2025 y más de US$30 millones en el 1S-2026. Una filtración fiscal en Francia amplió las víctimas ([Chainalysis, 6-ago-2026](https://www.chainalysis.com/blog/violent-crypto-wrench-attacks-2026/)). |
| D4 | **Apps o extensiones** no oficiales, o actualizaciones sospechosas | ROJA | [H] Una falsa Ledger Live en la App Store se ligó a US$9.5 millones (abr-2026, ZachXBT, una sola fuente). Hubo drenajes de usuarios de Trust Wallet tras una actualización de su extensión (dic-2025, alerta de ZachXBT, causa no determinada). |
| D5 | **Dejar saldo en stablecoin o en BTC envuelto o puenteado** sin necesidad | ÁMBAR | [I] Suma el riesgo del emisor (B2-B7) o del puente (C2) al del BTC. Para nuestra cuenta, la reserva va en MXN, como decidió el comité. |

---

## E. Señales para vigilar Binance hoy (datos públicos al 25-sep-2026)

**Frecuencia:** semanal, y también el día de cualquier evento. Los umbrales son propuestas mías [I] y los calibra el gestor de riesgo.

| # | Señal | Dónde se mide | Valor actual | ÁMBAR | ROJA |
|---|---|---|---|---|---|
| E1 | **Flujo neto semanal sin BNB** (método en F) | API de DefiLlama `protocol/binance-cex` | **+0.46% en 7 días** (+US$0.64 mil millones). **−0.55% en 3 días** desde el reporte de Bloomberg del 22-sep (−US$0.84 mil millones). **+1.18% en 30 días.** | < −2.1% en 7 días (percentil 5 de 1,405 semanas desde nov-2022) | < −5.3% en 7 días (percentil 1). Referencia: −13.5% en dic-2022. |
| E2 | **Activos rastreados y composición** | DefiLlama | US$179.4 mil millones. BTC 30.1% (643,038 BTC), USDT 22.7%, **BNB 15.4%**, WETH 10.5%, USDC 4.7% | BNB > 20% de lo rastreado, o BTC on-chain −5% en 7 días | BNB > 30% |
| E3 | **Prueba de reservas mensual** | https://www.binance.com/en/proof-of-reserves y la prensa que la resume | **46.º reporte:** foto del 1-sep-2026, publicado el 17-sep (16 días de rezago). **~682,000 BTC** de usuarios; ratio "de al menos 1:1" ([PANews, 17-sep-2026](https://panews.io/articles/01a0add9-878d-72a6-96d2-70123d73707b)). **45.º reporte** (1-ago): ~657,000 BTC; ratio de BTC **100.25%** y de USDT 103.62% (CoinAlert/crypto.news, 19-ago-2026). | Ratio de BTC < 100.5% dos meses seguidos, o rezago > 30 días | Ratio < 100% en cualquier activo, o un reporte suspendido o retirado |
| E4 | **Fondo SAFU** | Anuncios de Binance | **15,000 BTC** tras convertir US$1 mil millones de stablecoins (feb-2026), con **compromiso de reponerlo si baja de US$800 millones** ([CoinDesk, 12-feb-2026](https://www.coindesk.com/business/2026/02/12/binance-converts-its-usd1-billion-safu-fund-into-15-000-btc)). [I] Hoy vale ~US$1.26 mil millones con BTC a 84,000. | BTC < ~US$53,333, el nivel donde el fondo toca US$800 millones, sin reposición anunciada | Uso del fondo por un hackeo sin reposición |
| E5 | **Acciones regulatorias y penales** | DOJ, FinCEN, OFAC, CFTC, SEC; CNBV y Banxico; reguladores de la UE | [H] Investigación del DOJ por Irán, **sin cargos**. [H] El estado de los monitores de 2023 **no está confirmado**: un senador lo preguntó el 17-abr-2026 ([Fortune](https://fortune.com/2026/04/17/senator-blumenthal-binance-doj-fincen-treasury-monitorships-status/)). [H] La SEC desistió el 29-may-2025. [H] CZ (se declaró culpable en 2023; 4 meses) fue **indultado** el 23-oct-2025 (CNN, PBS). [H] UE: solo retiros desde el 1-jul-2026. | Citación, acusación a directivos, cierre en otro país grande o reporte de "acuerdo" en curso | **Cargos penales contra la entidad**, o **aviso de restricción para México**. Este segundo ya es disparador de contingencia en la bitácora. |
| E6 | **Retiros y SPEI** | Prueba propia antes de operar; página de estado de Binance | Retiros activos. SPEI vía Medá (IFPE autorizada por la CNBV; bitácora del 25-sep-2026). | Retiro de BTC > 2 h, o SPEI > 48 h | Retiros suspendidos o "en revisión" (A2) |
| E7 | **Incidentes de seguridad** | Comunicados de Binance; alertas de ZachXBT o SEAL-911 con segunda fuente | No hay incidente público de Binance en el archivo revisado (jun-2023 a sep-2026) | Incidente cubierto por SAFU con comunicado en menos de 24 h | Incidente mayor que el SAFU, o sin comunicado en 24 h |
| E8 | **Stablecoins en Binance** | Precios USDT/USD y USDC/USD; composición en DefiLlama | USDT 22.7%, USDC 4.7% y USD1 1.7% de lo rastreado | Pérdida de paridad > 1% | Pérdida de paridad > 3%, o congelamiento que afecte a Binance |
| E9 | **Liquidez de BTCMXN** | Libro de órdenes | Diferencial de 0.19%; 18,786 MXN del lado de compra a ±0.5% (bitácora del 25-sep-2026) | Diferencial > 0.5% | Libro vacío o par suspendido |
| E10 | **Noticias de cierre o restricción de rivales** (contagio) | CoinDesk, The Block | [H] **Bitget:** hackeo el 24-sep-2026 y retiros suspendidos. [H] AscendEX cerró el 1-jul-2026. [H] BitMart en cierre ordenado. | Pausa de retiros en un top-10 | Corrida generalizada: salidas en E1 de varios exchanges a la vez |

**Lectura al 25-sep-2026** [I]:
- **Sin señales ROJAS.**
- **ÁMBAR:**
  - E5, por la investigación del DOJ y la incertidumbre sobre los monitores;
  - A9: sin licencia en México y solo retiros en la UE.
- **Limpias:** flujos (E1), PoR (E3), retiros (E6) y liquidez (E9).
- El contagio por el hackeo a Bitget (E10) se vigila día a día.

---

## F. Método reproducible de flujos (E1 y E2)

- **Fuente:** `https://api.llama.fi/protocol/binance-cex`, pública y sin clave. Da las tenencias diarias por cadena y por token en las carteras que DefiLlama atribuye a Binance.
- **Flujo neto de *t−7* a *t*** = Σ por token de (unidades_t − unidades_{t−7}) × precio_t. Así se separa la entrada o salida real del efecto precio. El precio es el valor en USD entre las unidades del día *t*.
- **Se excluye BNB:**
  - las peores "salidas" de 2024 (−US$13.25 mil millones en abr-2024 y −US$9.67 mil millones en oct-2024) fueron **casi solo BNB**. Lo más probable es que fueran reclasificaciones de carteras, no una corrida, pero no lo verifiqué;
  - además, el token propio no mide la confianza de los clientes. Es la lección de FTT.
- **Resultados** (1,405 ventanas de 7 días, nov-2022 a sep-2026, sin BNB):
  - mediana: +0.04%;
  - percentil 5: −2.11%;
  - percentil 1: −5.28%;
  - peor semana: −13.49% (18-dic-2022, la corrida tras FTX y Mazars).
- **Script:** `scratchpad/g4/calc/flujos_binance_defillama.py`. Está fuera del repositorio; si el comité lo adopta, conviene moverlo a `herramientas/`.
- **Límites:**
  - DefiLlama solo ve las carteras que conoce;
  - las reasignaciones internas crean saltos;
  - los datos del día en curso llegan con retraso;
  - no ve pasivos, así que se usa **junto con** la PoR (E3), no en su lugar.

## G. Cómo leer una prueba de reservas (lista corta)

1. **Alcance:**
   - ¿qué activos cubre?;
   - ¿se incluyen los pasivos a clientes? El árbol de Merkle con zk-SNARK de Binance prueba la inclusión de saldos de usuario.
   - **Una PoR no muestra otras deudas del exchange.**
2. **Fecha y rezago:** foto del 1-sep publicada el 17-sep. Una foto se puede maquillar (A5).
3. **Ratio por activo:** 100.25% es un colchón de ~1,642 BTC sobre 657,000 (cálculo propio). Es suficiente, pero delgado.
4. **Composición:** ¿token propio o de afiliadas? (A1).
5. **Quién la firma:** atestación contra auditoría. Mazars se retiró en 2022; Tether pasó de atestaciones de BDO a una auditoría de KPMG en 2026.
6. **Serie de tiempo y retiros reales:** la PoR se cruza con E1 y E6. **Si los retiros no fluyen, la PoR no sirve.**
7. **Verificación propia:** el usuario puede comprobar que su saldo está incluido con la prueba de Merkle que publica el exchange.
