# 02 · Ethereum: historia, protocolo y hoja de ruta

> Capítulo de síntesis del grupo G2 Ethereum de la carrera cripto. Lo escribió el analista cripto el 25-sep-2026 y todos los datos de mercado y de red son de las ~22:00 UTC de ese día. Estado: **documentado**.
> Integra 6 recursos del dueño. Cada cifra lleva su fuente, y las que se pudieron verificar con una segunda vía o con un cálculo propio lo dicen. Etiquetas: **[H]** hecho con fuente, **[I]** inferencia propia, **[O]** opinión del autor citado.
> Contexto: el comité del 25-sep-2026 dejó **ETH fuera** de la cuenta cripto (`bitacora/decisiones/2026-09-25-CRIPTO-inicial.md`). La §8 fija qué tendría que pasar para reevaluarlo.

## 0. Los seis recursos y cuánto se leyó de cada uno

| # | Recurso | Acceso real | Grado | Ficha |
|---|---|---|---|---|
| 01 | *The Infinite Machine*, Camila Russo (2020) | Resumen: índice, descripción y reseñas | C | [01-the-infinite-machine.md](recursos/01-the-infinite-machine.md) |
| 11 | *The Cryptopians*, Laura Shin (2022) | Resumen: editorial, reseñas y cobertura del extracto en Forbes | C | [11-the-cryptopians.md](recursos/11-the-cryptopians.md) |
| 21 | *Read Write Own*, Chris Dixon (2024) | Sección: introducción oficial, 16 extractos con página e índice | D para inversión / C como marco | [21-read-write-own.md](recursos/21-read-write-own.md) |
| 23 | *Possible futures of the Ethereum protocol*, Vitalik Buterin (2024), 6 partes | **Íntegro**: las 6 partes | B | [23-possible-futures-of-the-ethereum-protocol.md](recursos/23-possible-futures-of-the-ethereum-protocol.md) |
| 24 | EPF Study Group / Protocol Wiki (2024-2026) | Sección: ~12 de 109 páginas; sin videos | B en mecánica / C en estado | [24-epf-study-group-protocol-wiki.md](recursos/24-epf-study-group-protocol-wiki.md) |
| 27 | *Mastering Ethereum*, 2.ª ed. (2025) | Sección: caps. 13, 15 y 16 íntegros; 1, 6, 7, 9, 10, 14 y 17 por secciones | B | [27-mastering-ethereum-2-a-edicion.md](recursos/27-mastering-ethereum-2-a-edicion.md) |

Banco de examen del grupo: [examen/banco-g2-ethereum.md](examen/banco-g2-ethereum.md).

## 1. Mapa del tema en niveles

| Nivel | Qué hay que dominar | Dónde está | Prueba de dominio |
|---|---|---|---|
| **Licenciatura** | Historia de 2013 a 2022 (whitepaper, venta de 2014, génesis, The DAO y el fork, ICOs, Merge); cuentas EOA y contratos; transacciones y gas; EIP-1559 y quema; qué es un contrato inteligente; tokens ERC-20 y ERC-721; staking básico (32 ETH, slashing) | 01, 11, 27 (caps. 1, 6, 7, 10, 13), 24 (`protocol/history`) | Contar con fechas y cifras de fuente primaria la venta de 2014 y The DAO; calcular una comisión EIP-1559 |
| **Maestría** | Gasper (LMD-GHOST + Casper FFG) y los tiempos de finalidad; fórmula de emisión (≈166.3·√S ETH al año); MEV, PBS y MEV-Boost; rollups optimistas frente a ZK; blobs (EIP-4844), PeerDAS y BPO; staking líquido (Lido) y su riesgo sistémico; seguridad de contratos (reentrancy, oráculos, mala configuración); etapas de L2BEAT | 23 (partes 2-3), 24, 27 (caps. 9, 13-17) | Derivar la emisión y el APR con un stake dado; explicar por qué la comisión de blobs está en el piso |
| **Doctorado** | Construcción de bloques y centralización (APS, FOCIL, BRAID, mempools cifrados); topar el stake frente a staking en dos niveles y la emisión mínima viable; muestreo 1D y 2D; ausencia de estado (Verkle frente a árboles binarios con STARK); pruebas de validez de la EVM y del consenso; riesgo de cliente con supermayoría; economía del activo (quema frente a emisión; captura de valor de L2) | 23 (partes 1-5), 24 (`eODS`, `ePBS`, `peerdas`), 27 (caps. 14-17) | Argumentar con números por qué escalar L1 no garantiza más quema; comparar Orbit SSF con SSF por fuerza bruta |
| **Frontera** | Glamsterdam (ePBS EIP-7732, BAL EIP-7928, reajuste de gas hacia "~200M gas floor"); Hegotá (FOCIL EIP-7805 + Frame Transaction EIP-8141); plan post-cuántico al dic-2029; zkEVM obligatorio en L1 (K* o L*); rollups nativos y *based*; iO, FHE y firmas de un solo uso | 23 (partes 2, 4 y 6), blog de la EF 2026, ethereum/pm | Dar el calendario verificado de Glamsterdam y su probabilidad de caer dentro del torneo |

## 2. Historia verificada (2013-2026)

| Fecha | Hecho | Fuente |
|---|---|---|
| Dic-2013 | Buterin comparte el whitepaper; Gavin Wood se suma como cofundador y CTO | [H] 27, cap. 1 |
| 26-ene-2014 | Presentación pública en la North American Bitcoin Conference de Miami | [H] fuente secundaria (Wikipedia, que cita a Fortune del 28-ene-2014) |
| 22-jul → 2-sep-2014 | Venta de ether: 31,531 BTC (US$18,439,086) por ~60,102,216 ETH, a 2,000 → 1,337 ETH/BTC | [H] [EF](https://blog.ethereum.org/2014/07/22/launching-the-ether-sale) y plantilla de ethereum.org |
| 30-jul-2015 03:26:13 UTC | Génesis (Frontier), con límite de gas de 5,000 | [H] 24 `protocol/history`; 27, cap. 1 |
| 14-mar-2016 | Homestead (bloque 1,150,000) | [H] 24; 27 |
| 30-abr → 28-may-2016 | The DAO vende ~1.15 mil millones de tokens por ~12 M ETH (~US$150 M) | [H] [SEC Rel. 81207](https://www.sec.gov/litigation/investreport/34-81207.pdf) |
| 17-jun-2016 | Ataque a The DAO: ~3.6 M ETH (1/3) | [H] SEC; 24 `incidents` |
| 20-jul-2016 | Hard fork; la minoría sigue como Ethereum Classic | [H] SEC |
| Sep-oct 2016 | Ataques DoS de Shanghai; Tangerine Whistle y Spurious Dragon | [H] 24 `incidents`; 27, cap. 14 |
| 2017-2018 | Boom de ICOs: más de 1,500 ICOs y US$12.9 mil millones en la muestra académica | [H] Howell, Niessner y Yermack, *RFS* 33(9), 2020 |
| 25-jul-2017 | La SEC declara valores (securities) a los tokens DAO | [H] SEC |
| 13-ene → 15-dic-2018 | ETH cae de 1,388.02 a 83.76 en cierres: **−94.0%** | [H] Binance, cálculo propio |
| 1-dic-2020 | Arranca el Beacon Chain | [H] 27, cap. 15; 24 |
| 5-ago-2021 | London / EIP-1559: base fee quemada; límite de 30 M con objetivo de 15 M | [H] 27, cap. 6 |
| 15-sep-2022 06:42:42 UTC | Merge (PoS); consumo eléctrico −99.988% | [H] 24 `roadmap`; primer bloque PoS 15,537,394 (RPC) |
| 12-abr-2023 | Shapella (retiros) | [H] 27, cap. 15; época 194048 (nodo beacon) |
| 11/12-may-2023 | Dos pérdidas de finalidad en 24 h (25 min y más de 1 h) | [H] 24 `incidents`; prensa |
| 13-mar-2024 | Dencun / EIP-4844 (blobs) | [H] 27, cap. 6; época 269568 |
| 4-feb / 21-jul / 25-nov-2025 | Límite de gas: 30 M → 36 M → 45 M → ~60 M | [H] bloques 21,770,182 / 22,967,156 / 23,878,946 (RPC) |
| 7-may-2025 10:05:11 UTC | Pectra (EIP-7702, 7251, 7002, 6110, 7691, 7623) | [H] 24 `pectra-faq`; época 364032 en 2 nodos |
| 8-jul-2025 | Todos los clientes soportan la expiración parcial del historial (−300-500 GB) | [H] [EF](https://blog.ethereum.org/2025/07/08/partial-history-exp) |
| 22/24-ago-2025 | Máximo de ETH: cierre de 4,832.07 e intradía de 4,956.78 (Binance); CoinGecko: 4,946.05 | [H] |
| 3-dic-2025 21:49:11 UTC | Fusaka (PeerDAS; límite de 60 M; tope por transacción de 16,777,216 gas; EIP-7918) | [H] [EF](https://blog.ethereum.org/2025/11/06/fusaka-mainnet-announcement); época 411392 en 2 nodos |
| 5-dic-2025 | Bug de Prysm: la participación baja a 74.7%, sin perder la finalidad | [H] Cointelegraph |
| 9-dic-2025 / 7-ene-2026 | BPO1 (10/15 blobs) y BPO2 (14/21) | [H] EF; `BLOB_SCHEDULE` en 2 nodos |
| 18-feb-2026 | La EF apunta Glamsterdam al primer semestre de 2026 | [H] [EF](https://blog.ethereum.org/2026/02/18/protocol-priorities-update-2026) |
| 25-jun-2026 | Mínimo de cierre de 12 meses: 1,567.84 (−67.6% desde el máximo) | [H] Binance |
| 20-ago-2026 | Glamsterdam en la testnet comunitaria Platåberget | [H] [EF, 17-ago-2026](https://blog.ethereum.org/2026/08/17/plataberget-testnet) |
| 7-sep-2026 | La EF: "Shipping Glamsterdam in December 2026"; Hegotá = FOCIL + Frame Tx; post-cuántico al dic-2029 | [H] [EF](https://blog.ethereum.org/2026/09/07/protocol-priorities) |
| 21-sep-2026 | ACDT #97: Sepolia el 6-oct (época 353024), Hoodi el 27-oct (tentativo) | [H] [ethereum/pm #2225](https://github.com/ethereum/pm/issues/2225) |

## 3. Cómo funciona el protocolo

**Consenso (27, cap. 15; 24; 23, parte 1)**
- [H] Slot de 12 s y época de 32 slots. Hay un proponente por slot y cada validador atestigua una vez por época.
- [H] Gasper = LMD-GHOST para elegir la punta de la cadena + Casper FFG para dar finalidad.
- [H] Para justificar un checkpoint se necesita una supermayoría de 2/3 del stake. Se finaliza cuando el checkpoint hijo directo también queda justificado. Revertir un checkpoint finalizado exige slashing de al menos 1/3 del stake ("seguridad responsable").
- [H] Si falla la finalidad, la cadena sigue viva gracias a LMD-GHOST y a la fuga por inactividad.
- [H] **Tiempos de finalidad:** 12.8 min según 27, ~15 min según 23, 16 min según 24 (ver §7).
- [H] **Parámetros vigentes** (configuración de mainnet, 25-sep-2026):

  | Parámetro | Valor |
  |---|---|
  | `SECONDS_PER_SLOT` | 12 |
  | `PROPOSER_SCORE_BOOST` | 40 |
  | `MAX_EFFECTIVE_BALANCE_ELECTRA` | 2,048 ETH |
  | Castigo inicial de slashing (desde Pectra) | 1/4096 |
  | Multiplicador de castigo correlacionado | 3 |

**Emisión (consensus-specs)**
- [H] `get_base_reward_per_increment` = 10⁹ × 64 / √(balance activo total en Gwei). Con participación plena, la emisión anual ≈ **166.3·√S** ETH, donde S es el ETH en staking. Lo derivé en Python con 82,181.25 épocas por año.
- [H] Con S = 43.52 M, la emisión máxima es ~1.10 M ETH al año y el APR máximo de consenso es 2.52%.

**EVM, gas, EIP-1559 y quema (27, caps. 6, 7 y 14; 23, parte 6; 24)**
- [H] El gas mide el cómputo. Una transferencia simple cuesta 21,000 gas.
- [H] EIP-1559:
  - la base fee se ajusta como máximo ±12.5% por bloque, apuntando al 50% del límite;
  - la base fee **se quema**; la priority fee va al validador.
- [H] Blobs:
  - tienen su propio mercado de gas;
  - su comisión **también se quema** (24, `el-specs`);
  - desde Fusaka, EIP-7918 les pone un piso ligado a la base fee: BLOB_BASE_COST = 2¹³, equivalente a 1/16 de la base fee por unidad de blob gas.
- [O/H] Argumento de Prestwich (27, cap. 14): con PBS, los validadores prefieren subir el límite con uso constante, y la base fee cae.

**Contratos y seguridad (27, caps. 7 y 9)**
- [H] Programas inmutables, deterministas y atómicos.
- [H] Los riesgos que más han costado son:
  - reentrancy (The DAO);
  - uso fuera de contexto (Parity);
  - manipulación de oráculos (Mango: más de $116 M);
  - mala configuración (yUSDT $11.6 M, Ronin, Sonne $20 M).

**DeFi (27, cap. 13)**
- [H] AMM x·y = k, préstamos sobrecolateralizados, liquidaciones, stablecoins y staking líquido.
- [O] "yet to find a proper market fit beyond token exchanges, stablecoins, and derivative creation".
- [H] Lido tiene **~22.5%** del stake: 9.78 M ETH (`getTotalPooledEther`) frente a 43.52 M activos. En 2025 el libro reportaba 29%.

**Rollups, disponibilidad de datos (DA) y ZK (23, parte 2; 27, caps. 16-17; 24)**
- [H] Tipos de rollup:
  - optimistas: ventana de desafío de ~1 semana;
  - ZK: validez inmediata al verificar la prueba; prueba agregada ~1 vez por hora.
- [H] Disponibilidad de datos:
  - un blob es un polinomio de grado 4096 y se borra a los ~18 días;
  - PeerDAS (1D) permite muestrear y reconstruir con más de 50% de las columnas.
- [H] ZK: los SNARKs requieren ceremonia de confianza (1-de-N) y no son poscuánticos; los STARKs son transparentes y poscuánticos.

## 4. Hoja de ruta: los seis frentes y su estado al 25-sep-2026

| Frente | Meta (23) | Ya en mainnet | Pendiente / en prueba | Evidencia |
|---|---|---|---|---|
| Merge | SSF, stake de 1 ETH, confirmación rápida, resistencia a ataques del 51% | PoS (2022); retiros (2023); MaxEB de 2,048 ETH (2025): **36% del stake ya en 0x02** | SSF, Orbit, SSLE, slots más cortos (siguen en 12 s), firmas post-cuánticas (plan al dic-2029) | Nodo beacon; EF 7-sep-2026 |
| Surge | 100,000+ TPS en L1+L2; L2 que hereden la seguridad | Blobs (2024); PeerDAS (dic-2025); blobs objetivo/máx. 14/21 (ene-2026); límite de 60 M | DAS 2D; etapa 2 en L2 grandes (**ninguna**); BAL y ~200M de piso de gas (Glamsterdam) | L2BEAT; EF |
| Scourge | Menos centralización en MEV y staking | MEV-Boost (fuera del protocolo) | ePBS (Glamsterdam), FOCIL (Hegotá), quema de MEV y tope al stake (investigación) | EF; pm #2225 |
| Verge | Verificar la cadena en un reloj; clientes sin estado | — | Verkle o árbol binario con STARK; zkEVM obligatorio (K* o L*) | EF 7-sep-2026 |
| Purge | Menos almacenamiento y complejidad | SELFDESTRUCT limitado (EIP-6780); expiración parcial del historial (jul-2025) | EIP-4444 completo; expiración de estado | EF 8-jul-2025 |
| Splurge | EVM final; abstracción de cuentas; comisiones; criptografía | EIP-7702 (Pectra) | EOF (**no llegó**: "postponed indefinitely"); gas multidimensional (Glamsterdam agrega una dimensión de gas de estado) | 27, cap. 14; EF 17-ago-2026 |

<a id="datos-verificados-al-25-sep-2026"></a>
## 5. Datos verificados al 25-sep-2026

| Métrica | Valor | Fuente principal | Segunda verificación |
|---|---|---|---|
| Precio ETH | US$2,680 (47,409 MXN) | Binance data-api | CoinGecko US$2,680.89 ✓ |
| ETH/BTC | 0.03200 | Binance | CoinGecko 0.03197 ✓ |
| Oferta | 122,074,463 ETH | ultrasound.money (saldos EL + beacon − depósitos) | CoinGecko 122,078,905 ✓ |
| Oferta en el Merge | 120,520,222 ETH (+1.29% desde entonces) | ultrasound.money | Fuente única |
| ETH en staking | 43,523,612 ETH efectivos (**35.7%**), 894,331 validadores | Nodo beacon (publicnode, `/validators`) | La emisión observada implica S ≈ 41.6 M (orden coherente) |
| Emisión | ~1.07 M ETH al año (7 y 30 días) | ultrasound.money | Fórmula: 1.10 M máx. con S = 43.52 M (participación ~98%) ✓ |
| Quema | 1,297 ETH en 30 días (≈15.8 mil al año); 620 ETH en 7 días | ultrasound.money | RPC: base fee 0.117-0.137 gwei, ~30 ETH al día en la muestra (orden coherente) |
| Inflación neta | **+0.87% al año** (30 días); +0.32% al año promedio desde el Merge | ultrasound.money | Cálculo propio: (1.0749 M − 15.8 mil)/122.07 M = 0.868% ✓ |
| Base fee | 0.1255 gwei | ultrasound.money | RPC 0.117 gwei; media de 1,024 bloques 0.137 ✓ |
| Límite de gas | 60,000,000 | RPC publicnode | RPC drpc ✓ |
| Blobs | 4.85 por bloque (objetivo 14, máx. 21); ~1.0e-6 ETH por blob; ~0.04 ETH al día quemados | RPC `eth_feeHistory` (1,024 bloques, ~3.4 h) | Objetivo/máx.: `BLOB_SCHEDULE` en 2 nodos + EF ✓; la quema es de una muestra corta |
| Rendimiento del staking | APR máx. de consenso 2.52%; stETH 2.25% neto (media de 7 días) | Fórmula de specs | API de Lido ✓ (coherente con una comisión de 10%) |
| Lido | 9,778,639 ETH (~22.5% del stake) | `eth_call` a stETH | — |
| L2 | Valor asegurado (TVS) US$44.4 mil millones; 71 en etapa 0, 6 en etapa 1, 4 en etapa 2; Base 16.4, Arbitrum 11.7 y OP 2.0 mil millones de US$ (todas en etapa 1) | API pública de L2BEAT | Fuente única |
| Riesgo relativo | Últimos 365 días: vol. de ETH 63.9% contra 45.2% de BTC; beta 1.28; correlación 0.91 | Binance, cálculo propio | — |
| Caídas en ventanas de 122 días (USD, desde 2017) | Mediana: ETH −37.2%, BTC −26.8%. P(≤ −50%): ETH 26.7%, BTC 14.4% | Binance, cálculo propio | — |

## 6. Las 10 ideas que más importan para invertir en ETH

1. **Hoy ETH es inflacionario, no "ultrasound money".**
   - [H] Inflación neta de +0.87% al año en 30 días. La oferta subió +1.29% desde el Merge.
   - [H] La quema casi desapareció: la base fee ronda 0.12 gwei. (ultrasound.money)
   - [I] Mientras la base fee siga en el piso, la narrativa de escasez no se sostiene con datos.
2. **El rendimiento del staking compensa sobre todo la dilución.**
   - [H] ~2.5% bruto (APR máx. de consenso 2.52%; stETH 2.25% neto).
   - [I] Descontada la inflación, el que hace staking gana ~1.6% real en ETH; el que no, pierde ~0.9% al año.
   - [I] Nuestra cuenta spot **no** captura ese rendimiento, y los productos de staking líquido suman riesgo de contraparte y de perder la paridad (27, cap. 13).
3. **Hoy las L2 casi no le pagan a ETH por disponibilidad de datos.**
   - [H] 4.85 blobs por bloque frente a un objetivo de 14; ~0.04 ETH al día (RPC).
   - [I] La hoja de ruta centrada en rollups aumentó la oferta de espacio de blobs más rápido que la demanda.
   - [I] Donde sí hay vínculo es en ETH como dinero y colateral dentro de las L2 y en el gas de liquidación en L1.
4. **Escalar L1 no garantiza más quema.**
   - [H] El límite subió de 30 M a 60 M y Glamsterdam apunta a un "~200M gas floor", con "roughly 3x base throughput" (EF).
   - [I] Más oferta de espacio de bloque baja el precio por unidad. La quema solo sube si la demanda crece más que la capacidad. Es el argumento de Prestwich (27, cap. 14).
5. **Las actualizaciones se retrasan y no mueven el precio de forma confiable.**
   - [H] Glamsterdam pasó de "first half of 2026" a "December 2026". EOF se anunció y nunca llegó.
   - [H] Estudio de eventos propio (n = 5, grado D): ETH/BTC a 30 días de cada fork fue −10.6%, +5.2%, −12.0%, +27.2% y +1.8%.
6. **ETH es más riesgoso que BTC y hay que dimensionarlo así.**
   - [H] Beta de 1.28, volatilidad de 64% frente a 45%.
   - [H] En 26.7% de las ventanas de 122 días desde 2017, ETH cayó 50% o más; BTC, en 14.4%.
   - [H] Caídas de ciclo: −94% (2018), −79% (2021-22) y −68% (2025-26).
7. **La tendencia de ETH/BTC desde el Merge es bajista, con un rebote reciente.**
   - [H] 0.0747 → 0.0320 (−57%). Lleva 52 días sobre su SMA200.
   - [H] Desde el Merge, el retorno a 122 días fue negativo en 79% de las ventanas. Estar sobre la SMA200 no ayudó: P(>0) = 9%, en ventanas traslapadas; grado C.
8. **El riesgo operativo se concentra alrededor de los forks.**
   - [H] Pérdidas de finalidad en mayo de 2023.
   - [H] Incidentes en testnets con Pectra (Holesky y Sepolia).
   - [H] Bug de Prysm tras Fusaka (participación de 74.7%).
   - [H] Lighthouse corría en 52.55% de los nodos de consenso en dic-2025 (Cointelegraph).
   - [I] Un fork en mainnet dentro del torneo, probable en diciembre, es catalizador y riesgo de cola a la vez.
9. **Hay centralización real y el protocolo apenas empieza a corregirla.**
   - [H] Dos constructores armaban ~88% de los bloques (23, parte 3, oct-2024).
   - [H] Lido tiene ~22.5% del stake.
   - [H] ePBS entra en Glamsterdam; FOCIL, en Hegotá, fuera del torneo.
   - [H] Ninguna L2 grande está en etapa 2.
10. **Separar historia, tecnología y precio.**
    - [I] Los libros (01, 11, 21) enseñan que el precio de ETH se ha movido por olas especulativas (ICOs: US$12.9 mil millones en más de 1,500 ofertas), crashes y shocks no programados.
    - [I] También muestran que los promotores tienen conflictos: a16z tiene más de US$7.6 mil millones en fondos cripto y ninguna divulgación en el libro.
    - [I] La tecnología avanza según lo prometido (blobs, PeerDAS, 7702), pero la captura de valor para ETH **no está demostrada**.

## 7. Contradicciones entre recursos

| Tema | Recurso A | Recurso B | Resolución |
|---|---|---|---|
| Fallas de finalidad | 23 (oct-2024): "only one (very brief) finality failure in all of Ethereum's history" | 24 `incidents` y prensa: dos pérdidas en 24 h en mayo de 2023 (25 min y más de 1 h) | [I] Diferencia de conteo o imprecisión. Para riesgo cuento **dos** eventos en 2023 más el casi-evento de dic-2025 |
| Tiempo de finalidad | 27: 12.8 min (2 épocas); cap. 6: "around 12 minutes" | 23: 2-3 épocas (~15 min); 24: 2.5 épocas (16 min) | [H] Convenciones distintas de medición; el mínimo técnico es de 2 épocas |
| Requisitos de la etapa 1 | 23: el consejo anula con 75%; al menos 26% externo | 27 (feb-2025): ≥ 5 actores externos que envían pruebas, ventana de salida ≥ 7 días, consejo con ≥ 50% de ≥ 8 firmantes y la mitad externos; advierte que el marco cambió | [I] El marco de L2BEAT evoluciona; para decidir se usa el **estado actual de L2BEAT**, no los libros |
| Verge | 27, cap. 1: "The Verge implements Verkle trees" | 23, parte 4: Verkle no es poscuántico; la alternativa son árboles binarios con STARK | [I] Hasta sep-2026 ninguno está en mainnet ni en Glamsterdam |
| Surge | 27, cap. 1: "The Surge introduces sharding" | 23, parte 2, y 27, cap. 16: hoja de ruta de rollups + DAS; el sharding "puro" no llegará | [H] Vigente: rollups + blobs + PeerDAS |
| EOF | 23, parte 6: "scheduled to be included in the next hard fork" | 27, cap. 14 (jun-2025): "postponed indefinitely"; 24: pendiente | [H] No está en mainnet ni en la lista de Glamsterdam |
| Proposer boost | 27, cap. 15: "added in the Dencun hard fork" | consensus-specs: `PROPOSER_SCORE_BOOST` = 40 en el fork choice de phase0 | [H] No es de Dencun; error del libro |
| Castigo de slashing | 24 `CL/overview`: "at least 1/32" | Configuración de mainnet: 1/4096 desde Pectra | [H] La wiki está desactualizada |
| Participación de Lido | 27, cap. 13: 29% | En cadena (25-sep-2026): ~22.5% | [H] Bajó; el umbral de riesgo citado es 33% |
| ¿Blockchains "inviolables"? | 21: "establish inviolable rules in software" | 01, 11 y SEC: el fork de The DAO cambió el estado por decisión social; 24: forks cada ~7 meses | [O] vs [H]: las reglas de Ethereum son **sociales y actualizables** |
| ¿Para qué sirve DeFi hoy? | 21: redes con "persistently lower take rates" para todo tipo de aplicaciones | 27, cap. 13: uso mayormente especulativo; sin encaje más allá de intercambio, stablecoins y derivados | [I] El marco optimista de 21 no trae evidencia; 27 es más creíble en este punto |
| Héroes del relato | 01 (según Decrypt): Buterin reticente con intenciones transparentes; la fundación como decisión correcta | 11 (según Decrypt): Hoskinson y Wood como villanos; Ming Chan con influencia "de culto" | [I] Relatos con sesgos opuestos; ninguno se usa para decidir |
| Los "US$11 mil millones" de The DAO | Titular del extracto de 11 en Forbes (2022) | SEC: el fork devolvió los fondos en ETH; el botín quedó en ETC | [H] Es una valuación nocional, no una ganancia realizada |

## 8. Qué haría falta para que ETH vuelva a entrar al universo

Reglas propuestas para el próximo comité. Son inferencias [I] mías y deben pasar por el abogado del diablo.

- **A. Mercado.** Se requieren las dos condiciones:
  1. ETH/BTC cierra por encima de su SMA200 durante al menos 30 días seguidos y la SMA50 está sobre la SMA200.
  2. ETHUSDT cierra por encima de su SMA200.

  **Estado al 25-sep-2026: cumple.** Lleva 52 días; SMA50 0.0312 > SMA200 0.0294; ETH está 28% sobre su SMA200. Advertencia: después del Merge este filtro no funcionó (P(>0) = 9%). Por eso la condición A **no basta sola**.
- **B. Ejecución del protocolo.** Glamsterdam debe activarse en Sepolia (6-oct-2026) y en Hoodi (27-oct-2026, tentativo) sin pérdida de finalidad, y los clientes deben publicar la época de mainnet.
  **Estado: pendiente.** Se sabrá entre el 6-oct y fines de noviembre.
- **C. Economía.** Se requiere al menos una:
  1. inflación neta de 30 días menor a +0.5% al año, lo que exige una quema de ≥ ~460 mil ETH al año, unas 29 veces la actual;
  2. blobs promedio de 7 días de al menos 14 por bloque (el objetivo);
  3. crecimiento sostenido de la demanda de gas, con la base fee de 7 días por encima de 1 gwei.

  **Estado: no cumple.** Inflación de +0.87% al año, 4.85 blobs por bloque y base fee de ~0.12 gwei.
- **D. Tamaño y salida.**
  - ETH no debe pasar del **10-20% de la cuenta cripto**. Con 20%, una caída de 50% de ETH (26.7% de probabilidad histórica en 4 meses) cuesta 1,000 MXN; con 10%, 500 MXN. Eso cabe dentro del tope de 5,000 MXN aunque BTC también caiga (correlación de 0.91).
  - La salida es obligatoria si ETH/BTC cierra bajo su SMA200.
  - Se opera solo en spot (par ETHMXN en TRADING, según la verificación del comité).
- **E. Regla del comité.** Cuatro votos con confianza de al menos 60, y que la propuesta sobreviva al abogado del diablo.

**Veredicto de hoy.** Solo se cumple la condición A. **ETH sigue fuera.** La primera revisión útil es después del 6-oct (Sepolia) y la segunda después del 27-oct (Hoodi).

## 9. Catalizadores dentro del torneo (28-sep-2026 → 28-ene-2027)

| Fecha | Evento | Estado | Fuente |
|---|---|---|---|
| 29-sep-2026 | Versiones de clientes para Sepolia | Programado | [H] pm #2225 |
| **6-oct-2026 13:53:36 UTC** | Glamsterdam en Sepolia (época 353024) | Confirmado el 21-sep | [H] pm #2225; sello verificado con la génesis de Sepolia |
| **27-oct-2026** | Glamsterdam en Hoodi | Tentativo | [H] pm #2225 |
| ~2-8 dic-2026 | Glamsterdam en mainnet, si repite el intervalo Hoodi → mainnet de Fusaka (36 días) o Pectra (42 días) | **Sin fecha**; la EF apunta a diciembre | [I] con base en [H] de la EF |
| Q4-2026 | Arranca la implementación de Hegotá (FOCIL + Frame Tx) | Sin efecto en mainnet dentro del torneo | [H] EF 7-sep-2026 |
| Ene-2027 | Revisión del plan post-cuántico de la EF | Documental | [H] EF 7-sep-2026 |

[I] **Probabilidad de que Glamsterdam llegue a mainnet antes del 28-ene-2027:** la estimo en ~55%. A favor pesan que Sepolia ya está confirmado y que la EF apunta a diciembre. En contra pesan que ningún devnet privado había logrado una activación estable según la cobertura del ACDT #97, que Pectra y Fusaka tuvieron incidentes en testnet y que este fork ya se retrasó del primer al segundo semestre. Queda como **pronóstico subjetivo sin registrar**; lo registrará el agente dueño de la bitácora si lo aprueba.

## 10. Límites y pendientes

- **Acceso.**
  - Tres libros los estudié solo como resumen o sección (01, 11, 21). Para subir a "sección", o a "íntegro" en 01 y 11, hay que leer los libros.
  - De la wiki del EPF (24) no vi los videos.
  - De Mastering Ethereum (27) faltan los caps. 2-5, 8, 11 y 12.
- **Fuente única.** Tres datos dependen de una sola fuente: la oferta en el Merge, el total de L2BEAT y la quema de blobs (muestra de 3.4 h). La cifra de quema de 30 días también es de fuente única, aunque su orden es coherente con el RPC.
- **No verificado.** El detalle de Stage 1 vigente en L2BEAT. Los flujos de ETFs de ETH no los verifiqué en esta sesión; los cita la decisión del comité (SoSoValue).
