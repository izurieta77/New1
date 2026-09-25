# 27 · Mastering Ethereum, 2.ª edición (Parisi, Mazza y Pozzolini, sobre Antonopoulos y Wood)

> Ficha del grupo G2 Ethereum. Estudiada el 25-sep-2026 por el analista cripto. Estado: **estudiado**. Acceso: **sección**, con 3 capítulos íntegros y 7 por secciones.
> Capítulo de síntesis: [02-ethereum-historia-protocolo-y-hoja-de-ruta.md](../02-ethereum-historia-protocolo-y-hoja-de-ruta.md).

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2025 |
| Publicación | Texto abierto en GitHub el **26-nov-2025**: commit "second edition (#1260)" y etiqueta `second-edition`, verificados con `git log` del repositorio. Según búsqueda web, la edición digital salió el 6-oct-2025 y la impresa en Amazon el 11-nov-2025; la página de O'Reilly devolvió 403 y **no pude confirmarlo con la editorial**. El prefacio dice "Copyright 2026 … ISBN 978-1-098-16842-1". |
| Autores | Carlo Parisi, Alessandro Mazza y Niccolò Pozzolini, sobre la 1.ª ed. (2016-2019) de Andreas M. Antonopoulos y Gavin Wood. Revisores técnicos: Ben Edgington, Caleb Lent, Brian Wu y Gonçalo Magalhães. |
| Tipo | Libro técnico (O'Reilly); 17 capítulos y prefacio, ~159 mil palabras |
| Nivel | Avanzado |
| Costo | Gratis en GitHub y en masteringethereum.xyz; impreso ~US$54, según el índice del dueño |
| Idioma | Inglés |
| URL | https://github.com/ethereumbook/ethereumbook |
| Licencia | CC BY-NC-ND 4.0 durante los 12 meses posteriores a la publicación; después, CC BY-SA 4.0 (README). Por eso esta ficha **resume** y no reproduce el texto. |
| Conflictos de interés | Parisi tiene un canal de YouTube cripto y Mazza uno de desarrollo; el prefacio lo declara. El libro no tiene sesgo hacia un producto, pero sí hacia Ethereum como plataforma y a favor de los desarrolladores. En el cap. 13 declara: "we do not support legal actions taken against individuals for writing decentralized code". Gavin Wood (coautor de la 1.ª ed.) fundó después Polkadot; aparece como autor, pero no escribió la 2.ª ed. |

## 2. Acceso real

- **Nivel: sección.** Cloné el repositorio (`git clone --depth 1`, commit 32a057a del 22-sep-2026) en el scratchpad el 25-sep-2026. Leí:
  - **Íntegros:** cap. 15, Consensus; cap. 16, Scaling Ethereum; cap. 13, Decentralized Finance.
  - **Por secciones:**
    - Prefacio.
    - Cap. 1: nacimiento de Ethereum, etapas y cultura.
    - Cap. 6: tipos de transacción, gas, EIP-1559, ciclo de vida, MEV y PBS, multisig.
    - Cap. 7: qué es un contrato inteligente, ciclo de vida, gas.
    - Cap. 9: buenas prácticas, reentrancy y The DAO, Parity, manipulación de precios y Mango, mala configuración, recursos.
    - Cap. 10: "Utility, Equity, or Cash Grab?" y "It's a Duck!".
    - Cap. 14: qué es la EVM, estado, statelessness, gas, límite de gas, EOF, futuro.
    - Cap. 17: historia, definición, uso en Ethereum, SNARK frente a STARK, zkEVM y zkVM; el ejemplo de partición solo lo hojeé.
  - **No leí:** caps. 2, 3, 4 (salvo lo citado en otros), 5, 8, 11 y 12.
- Los temas que el dueño pidió leer a fondo quedaron cubiertos: PoS (cap. 15), EVM, gas, EIP-1559 y quema (caps. 6, 7 y 14), contratos y seguridad (caps. 7 y 9), DeFi (cap. 13), ZK y rollups (caps. 16 y 17).
- El texto está fechado "at the time of writing (June 2025)" en varios capítulos; el de rollups, "February 2025".

## 3. Lo esencial

**Historia y cultura (cap. 1)**
1. [H] Etapas de Ethereum según el libro:

   | Etapa | Fecha y bloque | Qué incluyó |
   |---|---|---|
   | Frontier | 30-jul-2015 | Límite de gas inicial de 5,000 |
   | Homestead | 14-mar-2016, bloque 1,150,000 | — |
   | Metropolis | 16-oct-2017, bloque 4,370,000 | Byzantium, Constantinople e Istanbul |
   | Serenity | 15-sep-2022 | Subetapas Merge, Surge, Scourge, Verge, Purge y Splurge |

   La historia de la wiki del EPF coincide en génesis, Homestead y Merge.
2. [O] Cultura: la de Ethereum sería "move fast and break things", frente al conservadurismo de Bitcoin. Advierte que la autonomía "requires a bit more stability in the platform than you're likely to get in Ethereum in the next few years" (cap. 1).

**Prueba de participación (cap. 15, íntegro)**
3. [H] El Beacon Chain arrancó el 1-dic-2020 con depósitos de 32 ETH. El Merge fue el 15-sep-2022. Shapella (12-abr-2023) habilitó los retiros. El protocolo se llama Gasper = LMD-GHOST (fork choice) + Casper FFG (finalidad) (cap. 15). Las fechas coinciden con la configuración de mainnet: Capella en la época 194048, que corresponde al 12-abr-2023.
4. [H] Slot de 12 s y época de 32 slots. Hay un proponente por slot y cada validador atestigua una vez por época. LMD-GHOST cuenta solo el último mensaje de cada validador y elige la rama más pesada desde el último checkpoint justificado (cap. 15).
5. [H] Casper FFG tolera menos de 1/3 de validadores bizantinos y da "seguridad responsable": para revertir un checkpoint finalizado hay que hacer slashing de al menos 1/3 del stake. Justificar toma una época y finalizar otra: ~12.8 min en total. Gracias al pipeline, se finaliza un checkpoint cada 6.4 min. Las reglas de slashing prohíben el doble voto y el voto envolvente (cap. 15).
6. [H] Se necesitan dos fases, justificación y finalización, porque la justificación es local y reversible. Sin ella, un nodo con retraso de red habría "finalizado" algo que el resto nunca vio (cap. 15, ejemplo de cuatro validadores).
7. [H] Riesgo de cliente con supermayoría: un cliente con más de 2/3 de los validadores y con un bug podría finalizar una cadena inválida. El libro reporta que Geth pasó de 63% a 41%, con Nethermind en 38% (cap. 15). El bug de Prysm del 5-dic-2025 bajó la participación a 74.7%; Lighthouse tenía 52.55% de los nodos de consenso (Cointelegraph).

**EVM, gas, EIP-1559 y quema (caps. 6, 7 y 14)**
8. [H] EIP-1559 (London, 5-ago-2021) duplicó el límite de gas de 15 M a 30 M, con objetivo en la mitad. La base fee "is immediately burned, reducing the total supply of ETH"; la priority fee va al validador. Una transferencia simple cuesta 21,000 gas (cap. 6). Parámetros del texto de EIP-1559: la base fee cambia como máximo ±12.5% por bloque (`BASE_FEE_MAX_CHANGE_DENOMINATOR` = 8) y `ELASTICITY_MULTIPLIER` = 2.
9. [H] Tipos de transacción (EIP-2718): 0x00 legacy, 0x01 access lists, 0x02 EIP-1559, 0x03 blobs (Cancun, 13-mar-2024) y 0x04 EIP-7702 (Pectra, 7-may-2025). Un blob pesa ~131 mil bytes (cap. 6; el cap. 16 dice ~125 KB). El blob gas tiene su propio mercado (cap. 6). La wiki del EPF confirma que la comisión de blobs "is fully burned by the protocol".
10. [H] Gas: ADD cuesta 3; Keccak, 30 más 6 por palabra; una transacción, 21,000. El reembolso máximo es 1/5 del gas. SELFDESTRUCT quedó deprecado por EIP-6780. Tangerine Whistle (2016) corrigió opcodes mal tarificados tras ataques DoS (cap. 14).
11. [O/H] Un argumento clave para la tesis de quema (cap. 14, citando a James Prestwich): con separación entre proponente y constructor (PBS) hay incentivo a **subir el límite de gas manteniendo el uso**. Si el objetivo supera con creces el uso, la base fee cae y casi toda la comisión va al validador en vez de quemarse.
12. [H] Límite de gas: el libro dice "36 million gas at the time of writing (June 2025)". El límite subió en varios pasos, que verifiqué en cadena con RPC público:

    | Periodo | Límite | Evidencia en cadena |
    |---|---|---|
    | Hasta feb-2025 | 30 M | — |
    | Desde 4-feb-2025 | 36 M | Cruza 33 M en el bloque 21,770,182 |
    | Desde 21-jul-2025 | 45 M | Cruza 40.5 M en el bloque 22,967,156 |
    | Desde 25-nov-2025 | ~60 M | Cruza 52.5 M en el bloque 23,878,946 |
    | 25-sep-2026 | 60 M | Bloque 26,057,325 |

**Contratos inteligentes y seguridad (caps. 7 y 9)**
13. [H] Un contrato inteligente, en Ethereum, es un programa inmutable y determinista que corre en la EVM. "Neither smart nor legal contracts". Las transacciones son atómicas; si fallan, se revierten pero se cobra el gas (cap. 7).
14. [H] The DAO (2016): "the contract held more than $150 million, 15% of the circulating supply of ether". El hard fork creó Ethereum Classic en la cadena original (cap. 9). La fuente primaria (SEC, Release 81207, 25-jul-2017) da ~12 M ETH (~US$150 M), un ataque del 17-jun-2016 por ~3.6 M ETH (1/3) y el fork del 20-jul-2016.
15. [H] Ataques de precio y de oráculos:
    - Mango Markets: extracción de más de $116 M inflando 2,300% el precio del oráculo de MNGO; el atacante devolvió $67 M y se quedó $47 M.
    - Mobius (may-2025): $2.1 M.
    - Errores de configuración: yUSDT ($11.6 M, más de 1,000 días sin detectarse), Ronin (ago-2024; un bot white-hat devolvió 4,000 ETH) y Sonne ($20 M) (cap. 9).

**DeFi (cap. 13, íntegro)**
16. [O] "Currently, the primary users of DeFi are probably not the underbanked… but rather individuals from first-world nations looking to capitalize on the highly speculative nature of cryptocurrencies". DeFi "has yet to find a proper market fit beyond token exchanges, stablecoins, and derivative creation" (cap. 13).
17. [H] AMM x·y = k: en un pool de 100 ETH y 200 USDC, vender 1 ETH da 1.98 USDC y vender 50 ETH da 66.67 USDC (recalculado con Δy = yΔx/(x+Δx)). Préstamos sobrecolateralizados (ejemplo: 150%) con liquidaciones. Riesgo de oráculo por préstamos flash (cap. 13).
18. [H] Staking líquido: stETH "acts like a stablecoin pegged to the price of ETH" más el riesgo de slashing.
    - El libro dice: "Lido has 29% of all staked ETH"; más de 33% podría detener la finalización.
    - En jun-2022 no pasó la votación en Lido para autolimitarse (cap. 13).
    - Mi medición del 25-sep-2026: Lido tiene 9.78 M ETH (`getTotalPooledEther` en cadena), frente a 43.52 M en staking activo, es decir **~22.5%**.
19. [H] Algorítmicas: "There has not been a successful and well-capitalized algorithmic stablecoin" (UST colapsó). Alexey Pertsev, desarrollador de Tornado Cash, fue condenado a 64 meses en Países Bajos (cap. 13).

**ZK y rollups (caps. 16 y 17)**
20. [H] Rollups optimistas (Arbitrum, Optimism, Base; ventana de desafío de ~1 semana) frente a rollups ZK (ZKsync, Starknet, Scroll, Aztec; finalidad al verificar la prueba). "As of this writing (February 2025), Arbitrum is a stage 1 rollup". En jun-2025 había "far more optimistic rollups than ZK rollups" (caps. 16 y 17).
21. [H] Proto-danksharding (EIP-4844):
    - los blobs se borran tras 4,096 épocas (~18 días; recalculado: 4,096 × 6.4 min = 18.2 días);
    - aportan ~1 MB por slot de ancho de banda;
    - la EVM solo ve el compromiso KZG (cap. 16).
22. [H] Cronología ZK:
    - 1985 Goldwasser-Micali-Rackoff;
    - 2011 SNARKs (BIT+11);
    - 2013 Pinocchio;
    - 2016 Groth16;
    - 2017 Bulletproofs;
    - 2018 STARKs, transparentes y poscuánticos;
    - 2019 PLONK.

    Los SNARKs requieren una ceremonia de confianza de tipo 1-de-N y no son poscuánticos. Los zkVM (SP1, RISC Zero) buscan "one circuit to rule them all" (cap. 17).
23. [H] Riesgo criptográfico: en 2018 Ariel Gabizon encontró una falla que permitía falsificar monedas en el zk-SNARK original de Zcash. Se corrigió en Sapling y no se explotó aparentemente (cap. 16).

## 4. Qué cambia para invertir

- **Economía de ETH.**
  - [H] El libro enseña que la base fee y la comisión de blobs se queman. Pero el mecanismo solo reduce la oferta si la quema supera la emisión.
  - [H] Al 25-sep-2026:
    - base fee de ~0.12-0.14 gwei;
    - quema de 30 días de 1,297 ETH;
    - emisión de ~1.07 M ETH al año;
    - inflación neta de **+0.87% al año** (ultrasound.money).
  - [I] El argumento de Prestwich (punto 11) es relevante hoy: el límite pasó de 30 M a 60 M, Glamsterdam apunta a un "~200M gas floor" y la demanda usa ~50% del límite, así que la base fee no sube. Escalar abarata la unidad; la quema solo aumenta si la demanda crece más que la oferta.
  - [H] Staking: el libro explica la recompensa del proponente (priority fees más ETH nuevo) y el slashing. El rendimiento actual es ~2.5% bruto (APR máximo de consenso 2.52%; stETH 2.25% neto).
- **Captura de valor de las L2.**
  - [O] El libro describe a Ethereum como "settlement layer", pero no cuantifica cuánto pagan las L2.
  - [H] Hoy las L2 pagan ~0.04 ETH al día en blobs (muestra de 1,024 bloques, 25-sep-2026).
  - [I] La principal captura para ETH es monetaria (gas y colateral en ETH dentro de las L2), no la renta de DA.
  - [H] El libro advierte que la mayoría de las L2 tienen secuenciador centralizado (cap. 16). Según L2BEAT, ninguna grande está en etapa 2 (25-sep-2026).
- **Catalizadores del torneo.**
  - [I] El libro no los cubre: la versión es de jun-2025.
  - [H] Lo verificado:
    - Glamsterdam en Sepolia el 6-oct-2026;
    - Hoodi el 27-oct-2026, tentativo;
    - mainnet sin fecha, con objetivo de la EF en dic-2026;
    - contenido: ePBS, BAL y el reajuste de gas.
  - [I] Las lecciones del cap. 15 (riesgo de cliente con supermayoría) y del cap. 6 (MEV) indican que el riesgo operativo se concentra alrededor de los forks: los incidentes en testnets de Pectra, en Holesky y Sepolia, y el bug de Prysm post-Fusaka.
- **Razón ETH/BTC.**
  - [I] Nada en el libro sirve para predecirla.
  - [H] Dato útil del periodo que cubre el libro: entre su redacción (jun-2025) y hoy, ETH/BTC pasó por su máximo de 12 meses (0.0376, 6-oct-2025) y su mínimo (0.0258, 6-jun-2026). Hoy está en 0.0320 (Binance).
- **Qué haría falta para que ETH vuelva al universo.**
  - [I] Desde este recurso, entender el protocolo no basta. Tendría que verse la condición económica: quema que reduzca la inflación neta y blobs sobre su objetivo.
  - [I] Y la operativa: Glamsterdam sin incidentes en Sepolia y Hoodi, sin un cliente con más de 2/3.
  - [I] Criterios completos en el capítulo 02, §8.

## 5. Contrapuntos y límites

1. **Errores o imprecisiones que encontré** (se verifican uno por uno):
   - [H] Cap. 14: "36 million gas… meaning that around 1,428 basic… transactions". 36,000,000/21,000 = **1,714**; 1,428 corresponde a 30 M. Es un dato viejo que no se actualizó.
   - [H] Cap. 15: dice que Dencun añadió el "proposer boost". El `PROPOSER_SCORE_BOOST` = 40 está en la especificación de fork choice de phase0 (consensus-specs). No es una característica del hard fork Dencun. [I] Se adoptó antes, como regla de fork choice en los clientes. Probablemente el libro lo mezcla con la reorganización de bloques tardíos; no verifiqué la fecha exacta de adopción.
   - [H] Cap. 1: afirma que "Istanbul… introduced zero-knowledge cryptographic proofs (zk-SNARKs and STARKs)". Istanbul abarató precompilados y calldata que usan las pruebas; no las "introdujo". Dice también "five Serenity substages" y lista seis. Describe el Surge como "sharding" y el Verge como "Verkle trees", una simplificación desactualizada frente a Vitalik (2024).
   - [H] Cap. 16: en las lecturas escribe "BLS12-318"; la curva es BLS12-381.
   - [H] Cap. 17: dice que NP-completo significa que "an algorithm doesn't exist" en tiempo polinomial. Lo correcto: no se conoce, salvo que P = NP.
2. **Envejeció.**
   - [H] Límite de gas (36 M → 60 M).
   - [H] Participación de Lido (29% → ~22.5%).
   - [H] "Statelessness… a few years away" sigue vigente.
   - [H] EOF: el libro ya lo reporta pospuesto.
   - [H] El marco de etapas de los rollups cambió: el libro mismo lo advierte y contradice la versión de Vitalik; ver el capítulo 02, §7.
3. **Sesgos.**
   - [O] Libro para desarrolladores: muy fuerte en mecánica, débil en economía del activo.
   - [O] Es pro-Ethereum y la toma de postura sobre Tornado Cash es explícita. Aun así, es honesto sobre DeFi, porque reconoce que su uso es mayormente especulativo.
4. **Lo que no leí** y podría cambiar la ficha: los capítulos sobre nodos, wallets, oráculos y dapps (3, 5, 11 y 12) y la mayor parte del cap. 4 (criptografía y KZG).

## 6. Autoexamen

1. **¿Por qué Casper FFG necesita justificar y luego finalizar, y cuánto tarda?**
   Justificar es ver una supermayoría de 2/3 desde la vista local del nodo, y todavía se puede revertir. Finalizar es ver que 2/3 ya vieron esa justificación: para revertir, al menos 1/3 tendría que sufrir slashing. Cada ronda toma una época: ~12.8 min en total, con un checkpoint finalizado cada 6.4 min gracias al pipeline.
   Fuente: cap. 15.
2. **Con un límite de 60 M de gas, ¿cuántas transferencias simples caben en un bloque, y qué error tiene el libro con 36 M?**
   60,000,000/21,000 = 2,857. Con 36 M caben 1,714, no 1,428; 1,428 es la cifra con 30 M.
   Fuente: cap. 14 y cálculo propio.
3. **¿Por qué el libro dice que stETH se comporta como una stablecoin ligada a ETH, y qué riesgo sistémico señala?**
   Porque representa ETH en staking y debe mantener paridad con ETH, con riesgo de perder la paridad y de slashing. El riesgo sistémico: si un operador supera 33% del stake podría detener la finalización. Lido tenía 29% cuando escribieron y la autolimitación se rechazó en jun-2022.
   Fuente: cap. 13. Hoy Lido tiene ~22.5% (cálculo propio en cadena).
4. **¿Qué argumento del cap. 14 debilita la idea de que "más uso = más quema" cuando se sube el límite de gas?**
   Con PBS, los validadores tienen incentivo a subir el límite con uso constante. Si el objetivo supera al uso, la base fee baja y la comisión se va en propinas en vez de quemarse.
   Fuente: cap. 14, citando a James Prestwich.

## 7. Grado de evidencia: **B**

- Es un libro técnico de editorial seria, revisado por especialistas y verificable contra especificaciones y datos en cadena.
- Lo bajan de A cinco errores factuales detectados, el corte temporal de jun-2025, en un protocolo que cambia cada 6-7 meses, y la ausencia de análisis económico del activo.
- Para mecánica de PoS, EVM y seguridad lo uso como **B+**; para cifras de mercado o del estado de la red, como **C**, porque requieren verificación actual.
