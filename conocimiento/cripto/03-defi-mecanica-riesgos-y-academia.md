# 03 · DeFi: mecánica, riesgos y academia

> Carrera cripto del grupo G3 DeFi, escrita por `analista-cripto` el 25-sep-2026. Es formación, no recomendación. Nuestra cuenta en Binance es **solo spot** (hoy solo BTC): sin DeFi, sin préstamos y sin staking con bloqueo.
> **Recursos integrados (con su ficha):**
>
> | # | Recurso | Acceso |
> |---|---|---|
> | [03](recursos/03-finematics.md) | Finematics | sección |
> | [04](recursos/04-a16z-crypto-startup-school-2020.md) | a16z Crypto Startup School 2020 | resumen |
> | [06](recursos/06-decentralized-finance-mooc.md) | MOOC DeFi de Berkeley, 2021 | sección; diapositivas completas |
> | [07](recursos/07-defi-and-the-future-of-finance.md) | Harvey, Ramachandran y Santoro | documento de trabajo no leído; material del autor |
> | [12](recursos/12-decentralized-finance-the-future-of-finance.md) | Especialización de Duke en Coursera | temario y láminas |
>
> **Grado global: A** en la mecánica (verificada en Python, apéndice A); **B-C** en los casos (datos de fuentes primarias y de prensa con fuente, con discrepancias anotadas); **C-D** en las tesis prospectivas.
> **Etiquetas:** [H] hecho con fuente · [I] inferencia · [O] opinión del autor.

## 0. En una página

- **Rendimiento.** DeFi reemplaza intermediarios por contratos, pero no elimina el riesgo: lo transforma. Cada rendimiento DeFi paga riesgos que se pueden nombrar: pérdida impermanente, liquidación, contrato, oráculo, pérdida de paridad y MEV. [I]
- **Cascadas.** El mecanismo que más importa para el precio de BTC es la **cascada de liquidaciones**. El 10-oct-2025:
  - hubo más de $19 mil M de liquidaciones entre el 10 y el 11-oct, casi todas en perpetuos;
  - Aave, el mayor protocolo de préstamos, liquidó ~$180 M;
  - el BTC bajó de $122,574 a $104,782 dentro del día: −14.5% (§4).
- **Stablecoins.** Pierden la paridad por dinámica de corrida:
  - de forma **reflexiva** si el colateral es endógeno: UST cayó a $0.75 el 9-may-2022 y quedó bajo $0.20 el 13-may;
  - por **liquidez** si el colateral es bancario: USDC en $0.87-0.88 el 11-mar-2023, por debajo incluso de su valor en el peor caso fundamental, $0.92 (§2.6).
- **Aprendizaje.** El MOOC de Berkeley es la base rigurosa. Finematics es la puerta de entrada. Harvey es el marco de riesgos (con conflictos de interés). a16z es la lente del fondo de capital de riesgo.

## 1. Mapa: licenciatura → maestría → doctorado → frontera

| Nivel | Qué hay que dominar | Dónde está (fichas) | Cómo lo verifiqué |
|---|---|---|---|
| **Licenciatura** | Qué es DeFi frente a las finanzas centralizadas. Contratos y gas. Tipos de stablecoin. AMM x·y = k. Préstamo sobrecolateralizado. Préstamo relámpago como concepto. Riesgos básicos: bugs y llaves de administrador | [03](recursos/03-finematics.md) (artículos de 2020); [12](recursos/12-decentralized-finance-the-future-of-finance.md) cursos C1-C2; [06](recursos/06-decentralized-finance-mooc.md) clase 1; [04](recursos/04-a16z-crypto-startup-school-2020.md) clases 1-2 (solo temario) | Ejemplos de swap y de cETH recalculados |
| **Maestría** | Derivación de la pérdida impermanente y umbral de comisiones. Factor de salud, umbral de liquidación, *close factor* y bono. Subasta frente a *spread* fijo. Oráculos: mediana, TWAP y la condición costo de corrupción < ganancia. MEV y PBS. Diseño de stablecoins (colateral exógeno o endógeno; trilema). Rehipotecación. Gobernanza | [06](recursos/06-decentralized-finance-mooc.md) clases 5-8, 12 y 13; [07](recursos/07-defi-and-the-future-of-finance.md) decks 4-6; [12](recursos/12-decentralized-finance-the-future-of-finance.md) cursos C3-C4; [03](recursos/03-finematics.md) (MEV e Iron) | Apéndice A: pérdida impermanente, factor de salud, sándwich, rehipotecación |
| **Doctorado** | Angeris et al. (no arbitraje en mercados de función constante). Qin et al. (liquidaciones, flash loans, MEV). Daian et al. (*Flash Boys 2.0*). Perez et al. (*knife-edge*). Gudgeon et al. (crisis DeFi: gobernanza y estrés). Klages-Mundt y Minca (espirales de desapalancamiento). Liu, Makarov y Schoar (la corrida de Terra) | Lecturas de [06](recursos/06-decentralized-finance-mooc.md); [NBER w31160](https://www.nber.org/papers/w31160) | Qin et al.: leídos §1-5. Angeris: §2. NBER: pasajes clave. **Klages-Mundt y Minca: no leídos** (solo las láminas) |
| **Frontera** | PBS/MEV-Boost y concentración de *builders*. Perpetuos on-chain y desapalancamiento automático (ADL). Dólares sintéticos y oráculos internos de exchange (USDe en Binance, 10-oct-2025). LVR, *loss-versus-rebalancing*, el sucesor académico de la pérdida impermanente. Harvey, Hasbrouck y Saleh (2026) sobre la evolución de los DEX | [03](recursos/03-finematics.md) (MEV 2023); §3-§4 de este capítulo | **LVR** (Milionis et al., 2022) y **Harvey, Hasbrouck y Saleh**, *Research Policy* 55(3), listado en el CV de Harvey: **no leídos**; son la siguiente lectura |

**Ruta sugerida:**

1. Finematics: pools, pérdida impermanente, préstamos y flash loans.
2. MOOC, clases 5, 6 y 7.
3. Qin et al. sobre liquidaciones.
4. Harvey, deck 6 (riesgos).
5. NBER sobre Terra.
6. Clases 8 y 13 del MOOC (oráculos y MEV).
7. Frontera.

## 2. Mecánica esencial (verificada)

### 2.1 AMM de producto constante

- **[H]** El pool mantiene x·y = k. El precio marginal de X es y/x. Una compra de Δx con comisión f entrega Δy = y·(1 − f)Δx / (x + (1 − f)Δx). La comisión se queda en el pool y k crece ([06](recursos/06-decentralized-finance-mooc.md); Angeris et al.).
- **[H] Ejemplo (Python):** pool de 200,000 USDC y 100 ETH (precio 2,000). Una compra de 10,000 USDC:
  - entrega 4.748297 ETH, a un precio efectivo de 2,106.02;
  - el precio marginal pasa a 2,204.68;
  - sin comisión, el precio efectivo sería exactamente 2,000 × (1 + 10,000/200,000) = 2,100.
- **[H] No arbitraje** (Angeris et al., ec. 3): γ·m_p ≤ m_u ≤ m_p/γ, con γ = 1 − f. El precio del pool solo puede alejarse del precio externo tanto como la comisión.

### 2.2 Pérdida impermanente: derivación

1. Si no hay arbitraje ni comisiones, el precio del pool es igual al externo: p = y/x. Además x·y = k.
2. Por lo tanto y = √(k·p) y x = √(k/p). El valor del pool es V = p·x + y = **2√(k·p)** (Angeris et al., ec. 10).
3. Si el precio pasa de p₀ a p₁ = r·p₀: V₁/V₀ = √r. Mantener la mezcla inicial 50/50 (HODL) vale V₀·(1 + r)/2.
4. **IL(r) = 2√r/(1 + r) − 1.** Es simétrica: IL(r) = IL(1/r).

| r | 0.5 | 1.25 | 1.5 | 2 | 3 | 4 | 5 | 6 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| IL | −5.72% | −0.62% | −2.02% | −5.72% | −13.40% | −20.00% | −25.46% | −30.02% | −42.50% |

**Tres ejemplos de los recursos, reconciliados en Python:**

- **MOOC** (clase 5, lámina 47): 10 ETH y 1,000 DAI; el ETH pasa de 100 a 400. El pool queda en 5 ETH y 2,000 DAI; el 10% del LP vale $400 frente a $500 de HODL: **−20.00%**. Una simulación de 200,000 pasos de arbitraje coincide.
- **Finematics** (21-ago-2020): 20 ETH y 10,000 DAI; el ETH pasa de $500 a $550. La pérdida exacta es **$23.82**. Los $23.41 publicados salen de redondear el ETH a 19.07.
- **Harvey** (deck 5, Balancer): con un aumento de 5 veces, −25.46% en un pool 50/50 y −3.89% en uno 95/5, con el 95% en el activo que sube.

**Lo que hay que retener:**

- **[I] La pérdida impermanente es exactamente la ganancia del arbitrajista.** En el ejemplo de Finematics ambas valen $23.82. Ser LP es **vender volatilidad** a cambio de comisiones.
- **[H + cálculo] Umbral de comisiones.** Para compensar r = 2 con una comisión de 0.30%, el volumen acumulado debe ser **19.1 veces el TVL**; para r = 5, 84.9 veces.
- **[I] Frontera.** La literatura posterior (LVR) mide la pérdida frente a una estrategia que rebalancea, no frente a HODL. No la leí y no la uso aquí.

### 2.3 Préstamos: factor de salud y liquidación

- **[H] Definiciones** (Qin et al., arXiv 2106.06389):
  - capacidad de préstamo: BC = Σ colateralᵢ·LTᵢ;
  - **HF = BC/Σ deudaᵢ**, liquidable si HF < 1;
  - el liquidador paga hasta el *close factor* (50% en Aave y Compound; 100% en dYdX) y recibe colateral por deuda × (1 + bono), con bono de 5-15% en Aave.
  - En la notación de Maker, con colateralización de 150%, HF = CR/1.5.
- **[H + cálculo] Precio de liquidación** = deuda/(cantidad × LT). **Caída tolerable = 1 − 1/HF.** Ejemplo: 1 BTC a $110,000, LT 0.78 y deuda de $50,000 dan HF 1.716 y aguantan −41.7% (precio de liquidación: $64,103).
- **[H] Ejemplo de Qin et al., comprobado en Python:**
  - 3 ETH a $3,500, LT 0.8, deuda 8,400: HF 1.000. A $3,300, HF 0.943.
  - El liquidador paga 4,200, recibe 1.4 ETH y gana $420. El HF queda en 1.0057.
- **[H + cálculo] Sobreliquidación.** Con 2 BTC a $100,000, LT 0.80 y deuda de 110,000, bastaba repagar **7,500** para volver a HF = 1 cuando el BTC cae a $68,000. El *close factor* permite repagar 55,000: 7.3 veces más colateral vendido con bono de lo necesario.
  - Coincide con el hallazgo de Qin et al.: el *spread* fijo con *close factor* favorece al liquidador.
- **[H] Subasta frente a *spread* fijo:**
  - Maker usaba subastas en dos fases (*tend* y *dent*), que expusieron a los postores al riesgo de precio: 641 liquidaciones con pérdida.
  - En el Jueves Negro, la congestión dejó ganar subastas pujando 0 (§3).
  - Aave y Compound liquidan en una sola transacción, a menudo con flash loan.
- **[H] Sensibilidad.**
  - Un −43% del ETH volvería liquidables 1.07 mil M USD en Maker (datos a abr-2021).
  - Tras el lanzamiento de COMP, un −3% en DAI volvía liquidables más de 10 M USD en Compound (Perez et al.).

### 2.4 Préstamos relámpago, oráculos y gobernanza

- **[H] Atomicidad.** Si el préstamo no se devuelve en la misma transacción, todo revierte. Para el prestamista no hay riesgo de impago, salvo bugs; el atacante solo arriesga el gas.
- **[H] bZx, 18-feb-2020** (Qin et al., §3.2):
  - flash loan de 7,500 ETH;
  - 540 ETH en Uniswap y 360 ETH en Kyber: el oráculo de bZx baja de 268.30 a 106.05-108.44 sUSD/ETH;
  - 3,517.86 ETH en Synthetix, al precio justo;
  - todo el sUSD se usa como colateral para pedir prestados 6,799.27 ETH;
  - ganancia: 6,799.27 − 3,517.86 − 360 − 540 = **2,381.41 ETH** (verificado). Los prestamistas perdieron 2,699.97 ETH.
- **[H] Defensas:**
  - la **mediana** de varios nodos queda acotada por valores honestos si los malos son minoría (Juels);
  - el **TWAP** encarece la manipulación, a cambio de rezago;
  - condición de Harvey: el oráculo es vulnerable si su **costo de corrupción es menor que la ganancia de corromperlo**.
- **[H] El rezago también mata.** En Iron Finance (16-jun-2021), el TWAP rezagado sobrevaloró TITAN; el protocolo acuñó cada vez más y TITAN llegó a ~0 ([03](recursos/03-finematics.md)).
- **[H] Gobernanza comprable.** En Beanstalk (17-abr-2022), un flash loan compró votos para aprobar una propuesta maliciosa: el protocolo perdió $182 M y el atacante se quedó con ~$80 M ([CoinDesk](https://www.coindesk.com/tech/2022/04/17/attacker-drains-182m-from-beanstalk-stablecoin-protocol)). Harvey lo había anticipado en mar-2021 ([07](recursos/07-defi-and-the-future-of-finance.md)).

### 2.5 MEV

- **[H] Definición.** Es el valor que puede extraer quien ordena, incluye o excluye transacciones: front-running, back-running, sándwich, liquidaciones, arbitraje y censura.
- **[H] Tamaño** (Qin, Zhou y Gervais): en 32 meses (dic-2018 a ago-2021) sumó **540.54 M USD**: sándwiches 174.34 M, liquidaciones 89.18 M y arbitraje 277.02 M. Finematics estima más de 320,000 ETH desde el Merge hasta oct-2023 (~786 ETH/día, verificado).
- **[H] Arquitectura.** Se pasó de subastas públicas de gas (PGA) a Flashbots (~90% del hashrate) y luego a MEV-Boost y PBS (~90% de los validadores). Cinco *builders* construían ~90% de los bloques (Finematics, oct-2023).
- **[I] Regla del sándwich** (simulación, apéndice A): el atacante puede extraer, aproximadamente, **la tolerancia de deslizamiento por el monto de la víctima**.
  - $50k con 1% de tolerancia en un pool de $2M con comisión de 0.30%: ~$448.
  - En un pool de $20M con comisión de 0.30% no es rentable; con comisión de 0.05%, ~$400.

### 2.6 Stablecoins: cómo se pierde la paridad

- **[H] Taxonomía** (Klages-Mundt en [06](recursos/06-decentralized-finance-mooc.md); Harvey en [12](recursos/12-decentralized-finance-the-future-of-finance.md)):
  - **Custodial**: riesgo de contraparte, bancario y de censura.
  - **No custodial**:
    - con colateral **exógeno** (ETH en DAI): riesgo de desapalancamiento;
    - con colateral **endógeno** (LUNA para UST; TITAN para IRON): riesgo **reflexivo**;
    - con colateral implícito o nulo.
  - Trilema: estabilidad, eficiencia de capital y descentralización; no se logran las tres.
- **[I] Mecanismo común.** La paridad depende de que el mercado crea que la redención a $1 es posible e inmediata. Una corrida se autocumple cuando:
  - el respaldo cae junto con la stablecoin (endógeno);
  - el respaldo queda congelado (banco en quiebra, fin de semana);
  - la liquidez del mercado secundario se agota (Curve, límites diarios de canje).
- **Terra/UST, mayo de 2022** ([NBER w31160](https://www.nber.org/papers/w31160), salvo indicación):

  | Dato | Valor | Fuente |
  |---|---|---|
  | Oferta de UST antes del colapso | 18.5 mil M | NBER |
  | UST en Anchor | ~12 mil M (~65%) | NBER |
  | Rendimiento de Anchor | 19.5%, subsidiado | NBER |
  | Primer retiro | 375 M UST de 2 direcciones, 7-may | NBER |
  | Cruce clave | La capitalización de LUNA iguala la oferta de UST la noche del 9-may; UST cae a **$0.75** | NBER |
  | UST al cierre del 13-may | < $0.20 | NBER |
  | UST canjeados por LUNA (7-13-may) | 7.42 mil M UST por $4.65 mil M: **$0.627 por UST** (cálculo) | NBER |
  | Reservas de LFG | ~80,300 BTC el 6-may; **313 BTC** el 16-may | NBER; [CoinDesk](https://www.coindesk.com/business/2022/05/16/luna-foundation-guard-left-with-313-bitcoin-after-ust-crash) (80,394 → 313) |
  | Oferta de LUNA | De ~350 M a **más de 6.5 billones** | [The Block](https://www.theblock.co/post/146762/luna-supply-soared-to-6-5-trillion-coins-before-terras-latest-halt) |
  | Valuación antes del colapso | $50 mil M | NBER |

  - Contagio: el colapso desató en cadena las caídas de Celsius y Three Arrows y contribuyó a la de FTX (NBER).
  - El MOOC lo había advertido en oct-2021 (Klages-Mundt, lámina 77). Iron Finance fue el ensayo a menor escala (jun-2021).
- **USDC y SVB, marzo de 2023:**

  | Dato | Valor | Fuente |
  |---|---|---|
  | Exposición a SVB | $3.3 mil M, "*about 8%*" de la reserva | [Circle](https://www.circle.com/pressroom/3-3-billion-of-usdc-reserve-risk-removed-dollar-de-peg-closes) |
  | Composición de la reserva | $32.4 mil M en letras del Tesoro (77%) y $9.7 mil M en efectivo (23%) | Circle |
  | Mínimo de USDC | ≈ $0.87-0.88 el 11-mar | [CNN](https://www.cnn.com/2023/03/11/business/stablecoin-circle-silicon-valley-bank) ($0.88); otras fuentes, $0.8726 |
  | Contagio a DAI | ≈ $0.88-0.89, por su respaldo en USDC vía el PSM | [CoinDesk](https://www.coindesk.com/markets/2023/03/11/dai-depegs-as-stablecoin-rout-plagues-crypto) |
  | Rescate | Declaración conjunta de Tesoro, Fed y FDIC el 12-mar-2023, 18:15 EDT: todos los depositantes protegidos, acceso desde el 13-mar | [Fed](https://www.federalreserve.gov/newsevents/pressreleases/monetary20230312b.htm) |

  - **[I] Cálculo:** SVB era 7.84% de la reserva, así que el valor justo en el peor caso era 0.9216. El mínimo de 0.8726 implicaba perder 1.63 veces toda la exposición: fue un **descuento de liquidez y pánico** en fin de semana, sin redención primaria.
  - **[H]** El MOOC (oct-2021) había señalado que Maker "*has tethered to USDC (+ custodial risks)*".

## 3. Casos verificados (orden cronológico)

| Caso | Mecanismo | Datos clave | Fuentes | Verificación |
|---|---|---|---|---|
| Jueves Negro, Maker (12 y 13-mar-2020) | Congestión: los *keepers* fallan y hay subastas ganadas con pujas de 0 | ETH −43% (de $194 a $111). Estimación temprana: $4.5 M de DAI sin respaldo; más de $8 M de ETH adjudicados en cero. La subasta de MKR recaudó ~5.3 M DAI | [Glassnode](https://research.glassnode.com/what-really-happened-to-makerdao/) (17-mar-2020); [Blockonomi](https://blockonomi.com/makerdao-emergency-5-million-dai-raised/); Qin et al. (ganancia de liquidadores en Maker en mar-2020: 13.13 M USD) | Cifras discrepantes entre fuentes secundarias; **no encontré la cifra primaria de MakerDAO** |
| bZx (15 y 18-feb-2020) | Flash loan con bombeo del precio o manipulación del oráculo | 1,193.69 ETH y 2,381.41 ETH de ganancia | Qin et al. (arXiv 2003.03810) | Aritmética en ETH verificada. En USD el artículo no cuadra con su propio precio de ETH |
| Iron Finance (16-jun-2021) | Colateral endógeno más TWAP rezagado | TITAN de $64 a ~0; IRON recuperó ~$0.75 | Finematics | Una sola fuente, sin verificación independiente |
| Terra (7 a 13-may-2022) | Corrida reflexiva | Ver §2.6 | NBER, CoinDesk, The Block | Dos fuentes en los datos clave |
| Beanstalk (17-abr-2022) | Gobernanza comprada con flash loan | $182 M perdidos; ~$80 M para el atacante | CoinDesk, Cointelegraph, Bloomberg | Varias fuentes coinciden |
| USDC y SVB (10 a 13-mar-2023) | Riesgo bancario y liquidez en fin de semana | Ver §2.6 | Circle, Fed, CNN, CoinDesk | Primarias (Circle, Fed) |
| 10 y 11-oct-2025 | Cascada de liquidaciones en perpetuos | Ver §4.1 | CoinGlass (vía CoinGecko y CoinShares), CNN (corte de $18.28 mil M), CoinDesk (Aave) | BTC y total: dos fuentes. El interés abierto y la compensación de Binance discrepan entre fuentes |

## 4. Qué cambia para invertir

### 4.1 Cómo el apalancamiento y las cascadas mueven el BTC spot

**[I] Mecanismo:**

1. Un choque exógeno baja el precio.
2. Bajan los HF de los préstamos DeFi y el margen de los perpetuos.
3. Los liquidadores y los motores de riesgo venden a mercado.
4. El precio cae más, las posiciones siguientes llegan a su umbral y se repite.
5. El arbitraje entre mercados transmite la presión al spot de todos los exchanges.

Es la "*deleveraging spiral*" del MOOC y la "*liquidation sensitivity*" de Qin et al.

**[I] Es no lineal.** Modelo de juguete, no calibrado (apéndice A): 4,000 posiciones con umbrales entre −3% y −25% y un choque inicial de −5%.

| Profundidad del mercado | Caída final |
|---|---|
| $2 mil M por cada 1% de movimiento | −5.7% |
| $1 mil M por 1% | −7.2% |
| $0.5 mil M por 1% | −27.1%, con todo el libro liquidado |

Mismo choque, resultados muy distintos: lo que decide es cuánto apalancamiento está cerca del precio y cuánta liquidez hay.

**[H] 10 y 11-oct-2025:**

- **Detonante:** la tarde del viernes 10-oct (hora de EUA), Trump amenazó con un arancel adicional de 100% a las importaciones de China ([CNN](https://www.cnn.com/2025/10/11/business/trump-tariffs-crypto-selloff)), efectivo desde el 1-nov según CoinGecko.
- **Liquidaciones:** más de **$19 mil M** en 10 y 11-oct, "*the largest liquidation event in crypto history*" según CoinGlass (cifra citada por [CoinGecko](https://www.coingecko.com/learn/october-10-crypto-crash-explained) y [CoinShares](https://coinshares.com/corp/insights/knowledge/billions-in-liquidations-what-happened/), 20-oct-2025).
  - Corte intermedio de CNN: $18.28 mil M a las 15:47 ET del 11-oct, con ~$5 mil M en BTC, ~$4 mil M en ETH y ~$2 mil M en SOL en 24 h.
- **BTC:** de **$122,574 a $104,782 dentro del día: −14.5%** (CoinGecko; CoinShares). CNN registra un mínimo de $103,000 el viernes a las 17:15 ET; la diferencia se explica por el mercado de referencia de cada fuente.
- **Interés abierto:** de $175 mil M a $125 mil M en menos de un día (CoinShares). CoinGecko cita un récord previo de $217 mil M: dato discrepante.
- **Aave:** ~**$180 M** liquidados en una hora, "*without any human intervention*" ([CoinDesk](https://www.coindesk.com/markets/2025/10/11/aave-sees-64-flash-crash-as-defi-protocol-endures-largest-stress-test); la cita es de su fundador, Stani Kulechov, parte interesada). Fue **menos de 1%** del total.
- **Oráculos de exchange:** USDe cotizó en $0.65 **solo en Binance**, entre las 21:36 y las 22:16 UTC, junto con wBETH y BNSOL, por usar el libro interno como oráculo. Binance compensó a los usuarios de futuros, margen y préstamos afectados ([CoinGecko](https://www.coingecko.com/learn/october-10-crypto-crash-explained); CoinShares). El monto de la compensación varía según la fuente ($283-328 M) y no lo verifiqué en una fuente primaria.
- **Otros mercados:** Hyperliquid activó el desapalancamiento automático (ADL); dYdX estuvo fuera de línea cerca de 8 horas (CoinShares).
- **No uso:** la cifra de CoinGecko de que "70% ($6.93 mil M)" ocurrió en 40 minutos. Sus propios números no cuadran: 6.93 de 19 es 36%.

**Lecturas [I] para nuestra cuenta:**

1. Para el BTC, el apalancamiento que mueve el precio vive en los **perpetuos** de exchanges y de plataformas on-chain. Hay que vigilar interés abierto y *funding*; el TVL de DeFi no sirve para esto.
2. Una cuenta spot sin apalancamiento **no puede ser liquidada**. La cascada es riesgo de precio y de ejecución: el deslizamiento se dispara y los libros se vacían.
3. El exchange es un riesgo en sí mismo. Binance fue el mercado de los precios locales anómalos, y es nuestro custodio. El riesgo relevante es el de custodia y operación, el mismo que Harvey ilustra con Mt. Gox y Bitfinex.

### 4.2 Por qué nuestra cuenta no usa rendimientos DeFi

- **Mandato.** Solo spot: sin DeFi, sin préstamos y sin staking con bloqueo. Esto no es una opinión: es la regla.
- **[I] Incluso sin la regla, la apuesta es asimétrica.**
  - 5% anual sobre 5,000 MXN son 250 MXN al año, unos 21 MXN al mes.
  - Un evento de −20% (la pérdida impermanente con el precio ×4, o la caída de USDC) cuesta 1,000 MXN: cuatro años de rendimiento.
  - Un hackeo o una corrida (Terra, Fei/Rari, Beanstalk) puede costar 100%.
- **[H] Los rendimientos altos suelen ser subsidios.** Anchor pagaba 19.5% financiado con emisión (NBER). Iron Finance pagaba 500% y 1,700% (Finematics).
- **[H] Las auditorías no bastan.** "*The majority of hacked protocols had a security audit*" (rekt.news, citado por Finematics). "*DeFi attacks stole over $1B in 2021*" (MOOC, clase 1).
- **[I] Otros costos no estudiados aquí:** complejidad fiscal y regulatoria en México. Quedan fuera del alcance del grupo.

### 4.3 Señales de riesgo sistémico a vigilar

Los umbrales son **tentativos, míos y sin prueba histórica**. Sirven para abrir una alerta, no para operar.

| Señal | Umbral tentativo [I] | Datos públicos | Por qué (evidencia) |
|---|---|---|---|
| Paridad de USDT, USDC, DAI/USDS y USDe | Desvío mayor de 0.5% sostenido 1 h en varios mercados; mayor de 2% es evento | Precios de Curve y de exchanges; DefiLlama | USDC en $0.87 (2023); UST (2022); USDe en $0.65 solo en Binance (2025) |
| Rendimiento de stablecoins frente a letras del Tesoro | Mucho mayor que la tasa libre de riesgo (Anchor: 19.5%) | Tasas de protocolos; DefiLlama | Subsidio y corrida (NBER) |
| Interés abierto y *funding* de perpetuos | Récord de interés abierto con *funding* positivo persistente | CoinGlass | 10-oct-2025: más de $19 mil M liquidados |
| Colateral liquidable ante −10% y −20% | Aumentos bruscos de la concentración cerca del precio | Mapas de liquidación; paneles de riesgo de Aave | Sensibilidad (Qin et al.); modelo §4.1 |
| Gas y congestión | Varias veces el promedio del día | Rastreadores de gas | Jueves Negro: gas medio 6 veces mayor, picos horarios de ~200 gwei (Glassnode) |
| Desvío entre oráculos y mercado | Precio local distinto del de otros mercados | Comparar mercados; feeds de Chainlink | bZx (2020); Iron (2021); Binance (2025) |
| Hackeos grandes y de puentes | Más de $100 M o en un protocolo sistémico | rekt.news; DefiLlama (hackeos) | Beanstalk, Rari y The DAO |
| Concentración | Un protocolo con más de 50% de una stablecoin; pocos *builders* | DefiLlama; paneles de MEV | Anchor tenía ~65% de UST; 5 *builders* hacían ~90% de los bloques |
| TVL que crece más rápido que el capital | TVL/capitalización al alza con rehipotecación | Paneles de TVL | $5,500 de TVL con $2,500 comprometidos (Harvey, [12](recursos/12-decentralized-finance-the-future-of-finance.md)) |

## 5. Las 10 ideas que más importan para invertir

1. **Todo rendimiento DeFi es una prima por riesgos concretos:** pérdida impermanente, liquidación, contrato, oráculo, paridad y MEV. Si no puedes nombrarlo, no sabes qué estás vendiendo. El 19.5% de Anchor era subsidio (NBER). [H/I]
2. **Ser LP es vender volatilidad.** La pérdida impermanente, 2√r/(1 + r) − 1, es la ganancia del arbitrajista. Compensar una duplicación del precio con comisión de 0.30% exige 19 veces el TVL en volumen. [H + cálculo]
3. **Las stablecoins se rompen por dinámica de corrida.** Con colateral endógeno la corrida es reflexiva: UST cayó a $0.75 cuando la capitalización de LUNA igualó su oferta. Con colateral bancario, por liquidez: USDC en $0.87, por debajo de su peor caso de $0.92. [H]
4. **Las cascadas son no lineales.** El mismo −5% termina en −5.7% o en −27% según el apalancamiento cercano al precio y la profundidad del mercado. [I, modelo]
5. **Para el BTC, el apalancamiento que mueve el precio está en los perpetuos.** El 10-oct-2025 hubo más de $19 mil M liquidados frente a ~$180 M en Aave, y el BTC tocó −14.5% dentro del día. [H]
6. **Sin apalancamiento no te liquidan.** En una cascada, el riesgo de una cuenta spot es de precio y de ejecución: no hay que vender a mercado dentro de la cascada. [I]
7. **Oráculos y precios locales son el eslabón débil:** bZx (2020), el TWAP de Iron (2021) y USDe en $0.65 solo en Binance (2025). El riesgo del exchange aplica a nuestro propio custodio. [H]
8. **La tolerancia de deslizamiento es, aproximadamente, lo que se regala** a un atacante de sándwich. On-chain conviene operar en pools profundos o con límites estrictos. [I + simulación]
9. **La gobernanza se compra y las llaves de administrador son riesgo de equipo.** Beanstalk perdió $182 M; las auditorías no garantizan nada (rekt.news). [H]
10. **La divulgación DeFi se descuenta por conflictos de interés y por fecha.** Chainlink, Paradigm, Fei, a16z y Ripple/UBRI tienen intereses. Lo que en 2021 era "la solución" (Fei, la protección de Bancor, el crecimiento de Terra) colapsó en 2022. Cada cifra lleva fecha y fuente. [H/I]

## 6. Contradicciones entre recursos

| Tema | Postura A | Postura B | Qué concluyo |
|---|---|---|---|
| Costo del Jueves Negro | Finematics: "*around $4M*" | MOOC (Klages-Mundt): "*$8m*"; Qin et al.: 13.13 M USD de ganancia de liquidadores en Maker ese mes | Miden cosas distintas. ~$4-4.5 M es el déficit en la estimación temprana (Glassnode); >$8 M es el ETH adjudicado en cero; la subasta de MKR recaudó ~5.3 M DAI. **Sin cifra primaria de Maker** |
| Comisión de flash loan en Aave | MOOC, clase 6, lámina 50: "*Aave – 0.3% fees*" | Qin et al. (lectura del mismo curso), Finematics y Harvey: 0.09% (9 pb) | 0.09%: tres fuentes independientes. La lámina está mal |
| Ganancia de bZx en USD | Qin et al.: 350k y 634.9k | Juels (MOOC): $673k; mi cálculo con el precio de ETH del artículo: $316k y $674k | Uso ETH como unidad: 1,193.69 y 2,381.41 |
| *Relays* de MEV | MOOC (Gervais, Qin y Zhou): los *relays* "*aggravate the consensus layer attacks*" y centralizan | Finematics (2023): Flashbots y MEV-Boost resolvieron las externalidades de las subastas de gas | Coinciden en la centralización y difieren en el efecto neto. **No resuelto** |
| Oráculos | Juels (Chainlink): redes de oráculos con mediana robusta | Harvey: "*the largest systemic threat to DeFi*" | Los incidentes (bZx, Iron, Binance 2025) vinieron de oráculos de DEX, TWAP o internos, no de redes descentralizadas. Ambos tienen parte de razón |
| Fei | Harvey (2021), coautor de Santoro: "*decentralized and scalable*" | MOOC (Klages-Mundt, 2021, lámina 76): la curva de redención implícita de Fei es "*very steep to $0*" | Fei cerró en ago-2022: la crítica académica envejeció mejor que la promoción |
| UST en Anchor | Harvey (2024): "*almost 80%*" | NBER: ~12 de 18.5 mil M, ~65% | Uso el NBER, que mide on-chain |
| Mínimo de UST el 9-may-2022 | Harvey y CoinDesk: $0.35 | NBER: $0.75 la noche del 9-may | Posibles mínimos intradía por mercado. **No resuelto** |
| Pérdida de Terra | Harvey: ~$40 mil M | NBER: $50 mil M de valuación previa | Miden cosas distintas: pérdida contra valuación |
| Pérdida impermanente con "+500%" | Finematics: 25% | Fórmula: 25.46% es 5 veces (+400%); +500% da 30.0% | Error de redacción de Finematics |
| Escalabilidad | Harvey (2021) y Coursera (2026): "15 TPS"; los rollups optimistas "*have yet to deliver*" | Finematics (ago-2021): rollups de 1,000-4,000 TPS; Optimism y Arbitrum en uso | El dato de Harvey envejeció y el curso vigente no lo actualizó |
| Estabilidad financiera | Harvey (2024): con un TVL de $57 mil M, DeFi "*not in the realm of a financial stability concern*" | MOOC (Gudgeon et al.): prueba de estrés de crisis DeFi; NBER: Terra desató las caídas de Celsius y Three Arrows y contribuyó a la de FTX | El contagio ocurrió por canales cripto-cripto y de CeFi cripto. El TVL mide mal el riesgo |
| Descentralización y regulación | a16z (Walden y Kupor): con descentralización suficiente, el token "*can change from security to non-security*" | Harvey: dictamen de la SEC sobre The DAO (2017), cierre de Basis y escrutinio a los tokens de gobernanza | Tesis de un fondo interesado frente a riesgo regulatorio documentado |
| Inclusión | Harvey: "1.7 mil millones de no bancarizados" como argumento | La mecánica de todos los recursos exige sobrecolateralización | [I] El préstamo DeFi no atiende a quien no tiene colateral |
| Protección contra pérdida impermanente | Finematics (2020 y 2022): Bancor la "*can completely mitigate*" | Bancor la suspendió en jun-2022 ([The Block](https://www.theblock.co/post/153049/bancor-dex-pauses-impermanent-loss-protection-amid-market-instability)) | No existe almuerzo gratis: la protección la pagaban con emisión de BNT |

## 7. Límites de este capítulo y siguientes pasos

- **Sin acceso:**
  - el documento de trabajo de SSRN del recurso 07: Cloudflare 403; la copia de terceros tiene captcha; el PDF del libro en GitHub lo descarté por pirata;
  - los videos de YouTube (03, 04 y 06) y de Coursera (12);
  - diapositivas o transcripciones oficiales de a16z;
  - Internet Archive.
- **Sin verificar con segunda fuente:**
  - la cifra primaria del Jueves Negro;
  - los datos de Iron Finance (solo Finematics);
  - el interés abierto del 10-oct-2025 (fuentes discrepantes);
  - el monto de la compensación de Binance;
  - las caídas de acciones y oro en mar-2020 que cita Harvey.
- **Siguiente prueba** para subir el tema a "Contrastado":
  1. reconstruir con datos on-chain de Aave la sensibilidad de liquidación actual del colateral en BTC (WBTC y cbBTC);
  2. medir cuánto se movió el spot en los 10 días de mayores liquidaciones de perpetuos frente a su interés abierto previo;
  3. leer LVR y a Klages-Mundt y Minca.
- **No toqué** `estado-de-dominio.csv` ni el índice (regla de esta tarea). Propuesta para el orquestador: "DeFi: AMM, pérdida impermanente, factor de salud, stablecoins y MEV" → Comprendido con comprobación (apéndice A).

## Apéndice A. Código de verificación (Python, solo biblioteca estándar, semilla 20260925)

Todo número marcado "verificado" o "cálculo" en este capítulo y en las fichas sale de este código o de su versión ampliada, que corrió en el scratchpad de la sesión.

```python
import math, random

def swap_in(x, y, dx, fee=0.003):
    """Entra dx del activo X al pool (x, y); devuelve (dy, x_nuevo, y_nuevo). Uniswap v2."""
    dxe = dx * (1 - fee)
    dy = y * dxe / (x + dxe)
    return dy, x + dx, y - dy

def il(r):
    """Perdida impermanente de un pool 50/50 x*y=k sin comisiones; r = P1/P0."""
    return 2 * math.sqrt(r) / (1 + r) - 1

def hf(qty, price, lt, debt):
    return qty * price * lt / debt

# 1) Swap: pool 200,000 USDC / 100 ETH; compra con 10,000 USDC
dy, x1, y1 = swap_in(200_000, 100, 10_000)
print("swap:", round(dy, 6), "ETH; efectivo", round(10_000 / dy, 2), "; marginal", round(x1 / y1, 2))

# 2) IL: formula vs simulacion de arbitraje en 200,000 pasos (MOOC: 10 ETH/1,000 DAI, 100 -> 400)
k, x, y = 10 * 1000, 10.0, 1000.0
for i in range(1, 200_001):
    p = 100 * 4 ** (i / 200_000)
    x = math.sqrt(k / p); y = k / x
print("pool final", round(x, 4), "ETH /", round(y, 2), "DAI; IL sim", round(0.1 * (400 * x + y) / 500 - 1, 4), "; formula", round(il(4), 4))
print("tabla IL:", {r: round(il(r), 4) for r in (0.5, 1.25, 2, 4, 5, 6)})
k = 20 * 10_000                                   # Finematics: 20 ETH / 10,000 DAI, 500 -> 550
lp = 2 * math.sqrt(k * 550); hodl = 20 * 550 + 10_000
print("Finematics IL exacta", round(hodl - lp, 2), "; con 19.07 ETH", round(hodl - (19.07 * 550 + math.sqrt(k * 550)), 2))
print("comisiones para compensar r=2 con 0.30%:", round(-il(2) / 0.003, 1), "x TVL")

# 3) Factor de salud y liquidacion (Qin et al. 2021): 3 ETH, LT 0.8, deuda 8,400; ETH 3,500 -> 3,300
q, lt, d, p, cf, ls = 3.0, 0.8, 8_400.0, 3_300.0, 0.5, 0.10
seized = cf * d * (1 + ls) / p
print("HF", round(hf(q, 3500, lt, d), 4), "->", round(hf(q, p, lt, d), 4), "; ganancia liquidador", round(seized * p - cf * d, 2),
      "; HF despues", round(hf(q - seized, p, lt, d * (1 - cf)), 4))
print("caida tolerable con HF 1.716:", round(1 - 1 / 1.716, 3))

# 4) Sandwich: ganancia maxima del atacante acotada por la tolerancia de la victima
def best_sandwich(X, Y, V, tol, fee):
    v0, _, _ = swap_in(X, Y, V, fee)
    lo, hi = 0.0, X
    for _ in range(200):                           # front-run maximo que respeta la tolerancia
        m = (lo + hi) / 2
        _, a, b = swap_in(X, Y, m, fee)
        if swap_in(a, b, V, fee)[0] >= v0 * (1 - tol): lo = m
        else: hi = m
    best = 0.0
    for i in range(1, 401):
        a = lo * i / 400
        e, x2, y2 = swap_in(X, Y, a, fee)
        _, x3, y3 = swap_in(x2, y2, V, fee)
        best = max(best, swap_in(y3, x3, e, fee)[0] - a)
    return best
for X, Y, V, fee in [(20e6, 1e4, 5e4, 0.003), (20e6, 1e4, 5e4, 0.0005), (2e6, 1e3, 5e4, 0.003)]:
    print("sandwich pool", X / 1e6, "M, victima", V / 1e3, "k, fee", fee, "tol 1%:", round(best_sandwich(X, Y, V, 0.01, fee), 2))

# 5) Cascada de liquidaciones: modelo de juguete (4,000 posiciones, impacto lineal), NO calibrado
random.seed(20260925)
P0 = 120_000.0
pos = [(P0 * (1 - random.uniform(0.03, 0.25)), random.lognormvariate(math.log(2e6), 1.0)) for _ in range(4000)]
def cascade(shock, depth):
    price, done = P0 * (1 - shock), set()
    while True:
        new = [i for i, (pl, n) in enumerate(pos) if pl >= price and i not in done]
        if not new: return price / P0 - 1, sum(pos[i][1] for i in done)
        done.update(new)
        price *= 1 - 0.01 * sum(pos[i][1] for i in new) / depth
for depth in (2e9, 1e9, 5e8):
    r, liq = cascade(0.05, depth)
    print("choque -5%, profundidad", depth / 1e9, "mil M por 1%: caida final", round(r, 3), "; liquidado", round(liq / 1e9, 2), "mil M")

# 6) USDC/SVB: reserva 32.4 (T-bills) + 9.7 (efectivo); 3.3 en SVB
tot, svb = 32.4 + 9.7, 3.3
print("USDC: SVB =", round(svb / tot, 4), "de la reserva; valor justo con 0/50/100% de recuperacion:",
      [round(1 - svb / tot * (1 - rec), 4) for rec in (0, 0.5, 1)], "; minimo 0.8726 =", round((1 - 0.8726) / (svb / tot), 2), "x la exposicion")
```

**Salida (corrida del 25-sep-2026):**

```
swap: 4.748297 ETH; efectivo 2106.02 ; marginal 2204.68
pool final 5.0 ETH / 2000.0 DAI; IL sim -0.2 ; formula -0.2
tabla IL: {0.5: -0.0572, 1.25: -0.0062, 2: -0.0572, 4: -0.2, 5: -0.2546, 6: -0.3001}
Finematics IL exacta 23.82 ; con 19.07 ETH 23.41
comisiones para compensar r=2 con 0.30%: 19.1 x TVL
HF 1.0 -> 0.9429 ; ganancia liquidador 420.0 ; HF despues 1.0057
caida tolerable con HF 1.716: 0.417
sandwich pool 20.0 M, victima 50.0 k, fee 0.003 tol 1%: 0.0
sandwich pool 20.0 M, victima 50.0 k, fee 0.0005 tol 1%: 400.36
sandwich pool 2.0 M, victima 50.0 k, fee 0.003 tol 1%: 448.41
choque -5%, profundidad 2.0 mil M por 1%: caida final -0.057 ; liquidado 1.57 mil M
choque -5%, profundidad 1.0 mil M por 1%: caida final -0.072 ; liquidado 2.32 mil M
choque -5%, profundidad 0.5 mil M por 1%: caida final -0.271 ; liquidado 13.06 mil M
USDC: SVB = 0.0784 de la reserva; valor justo con 0/50/100% de recuperacion: [0.9216, 0.9608, 1.0] ; minimo 0.8726 = 1.63 x la exposicion
```

**Segunda comprobación:**

- La pérdida impermanente se comprobó por tres vías: fórmula cerrada, simulación de arbitraje en 200,000 pasos y los ejemplos de tres recursos distintos.
- El factor de salud reproduce el ejemplo publicado por Qin et al.
- Las cifras de USDC se cruzaron con el comunicado de Circle, que dice "*about 8%*" (el cálculo da 7.84%).
- **Límite:** yo mismo hice la comprobación; no la hizo un agente independiente.

## Apéndice B. Fuentes principales (consultadas el 25-sep-2026)

- **MOOC de Berkeley:** temario (https://berkeley-defi.github.io/f21_syllabus) y PDFs en `berkeley-defi.github.io/assets/material/`.
- **Artículos académicos:**
  - Qin et al., arXiv 2106.06389, 2003.03810 y 2101.05511;
  - Angeris et al., arXiv 1911.03380;
  - Perez et al., arXiv 2009.13235;
  - Gudgeon et al., arXiv 2002.08099;
  - Liu, Makarov y Schoar, [NBER w31160](https://www.nber.org/papers/w31160).
- **Finematics:** https://finematics.com (sitemap y 22 artículos).
- **Harvey:**
  - [foro de Harvard Law, 14-ene-2021](https://corpgov.law.harvard.edu/2021/01/14/defi-and-the-future-of-finance/);
  - decks de 2021 (`people.duke.edu/~charvey/Teaching/562F_2021/Public_Presentations_562F/`) y de 2024 (`.../697_2024/Public_Presentations_697/`);
  - [CV](https://people.duke.edu/~charvey/vitae.htm) y [Disclosure](https://people.duke.edu/~charvey/Disclosure.htm).
- **Coursera:** página de la especialización y de los 4 cursos.
- **a16z:** [anuncio](https://a16z.com/introducing-a16z-crypto-startup-school/), [videos](https://a16zcrypto.com/posts/article/crypto-startup-school-online/) y [Walden 2020](https://a16zcrypto.com/posts/article/progressive-decentralization-crypto-product-management/); notas de TechCrunch del 13-may, 27-may, 10-jun y 24-jun-2020.
- **Casos:** Circle, Fed, CNN, CoinDesk, The Block, Glassnode, CoinGecko, CoinShares y SEC (Release 34-81207), con enlaces en el texto.
