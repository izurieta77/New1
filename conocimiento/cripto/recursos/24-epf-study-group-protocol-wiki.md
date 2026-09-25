# 24 · EPF Study Group / Protocol Wiki (Ethereum Protocol Fellowship, EF)

> Ficha del grupo G2 Ethereum. Estudiada el 25-sep-2026 por el analista cripto. Estado: **estudiado (parcial)**. Acceso: **sección**.
> Capítulo de síntesis: [02-ethereum-historia-protocolo-y-hoja-de-ruta.md](../02-ethereum-historia-protocolo-y-hoja-de-ruta.md).

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2024: el grupo de estudio arrancó en 2024. La wiki se sigue editando; el último commit que cloné es del 17-may-2026 |
| Autor | Ethereum Protocol Fellowship (programa de la Ethereum Foundation) y la comunidad del grupo de estudio. Ponentes del currículo original: Mario Havel (introducción y taller de clientes), Alex Stokes, lightclient, Hsiao-Wei Wang, Ben Edgington, Dankrad Feist, Barnabé Monnot, Piper Merriam, Francesco D'Amato, entre otros |
| Tipo | Curso (clases grabadas en YouTube y StreamEth) más una wiki técnica comunitaria |
| Nivel | Experto: pensado para quien quiere contribuir al núcleo del protocolo, no para programar dapps |
| Costo | Gratis. Wiki bajo CC BY-SA 4.0 (archivo LICENSE del repositorio) |
| Idioma | Inglés |
| URL | https://epf.wiki/ (fuente: https://github.com/eth-protocol-fellows/protocol-studies); currículo 2026 en https://study.epf.wiki |
| Conflictos de interés | Lo produce la EF, que tiene tesorería en ETH (no la verifiqué para esta ficha). Es material de ingeniería, no de inversión, pero su marco es el de quien construye Ethereum. La wiki la escribe la comunidad y se advierte "still under construction". |

## 2. Acceso real

- **Nivel: sección.** Cloné el repositorio (`git clone --depth 1`, commit bd55164 del 17-may-2026; 109 páginas, ~143 mil palabras) el 25-sep-2026.
- **Leí completas:**
  - `readme`, `eps/intro` (grupo de estudio 2026) y `eps/archive` (currículo original de 10 semanas y 16 sesiones);
  - `wiki/protocol/history` (es un esbozo, un "stub");
  - `wiki/research/roadmap`, `wiki/testing/incidents`, `wiki/dev/core-development` y `wiki/dev/pm`;
  - la primera mitad de `wiki/research/eODS` y de `wiki/research/PBS/ePBS`;
  - la parte inicial de `wiki/research/PBS/mev` y de `wiki/research/peerdas`.
- **Por búsqueda de texto:** `wiki/pectra-faq`, `wiki/CL/overview` (finalidad, penalizaciones y slashing), `wiki/protocol/design-rationale`, `wiki/EL/el-specs` y `wiki/EL/transaction` (quema de la base fee y de los blobs).
- **No vi los videos** del grupo de estudio, que son lo central del "curso". Tampoco leí las páginas largas de criptografía (KZG, BLS), SSZ, devp2p, Engine API ni la especificación de la capa de ejecución (EL), salvo las líneas citadas.
- Contrasté el estado de las actualizaciones con la configuración de mainnet de dos nodos beacon (publicnode y Lodestar) y con el blog de la EF.

## 3. Lo esencial

1. [H] El grupo de estudio es abierto y sin requisitos de admisión. La edición 2026 empezó el 23-feb-2026 y duró 8 semanas, con currículo en study.epf.wiki. Módulos nuevos de 2026: criptografía (Matan Prasma, del 9-mar al 7-abr) y zkEVM/Lean Ethereum, con una sesión de criptografía post-cuántica a cargo de Justin Drake el 9-abr-2026 (`eps/intro`).
2. [H] El currículo original tiene tres bloques: introducción al protocolo, capas de consenso (CL) y de ejecución (EL), e investigación (sharding y DAS, Verkle, MEV y censura, Purge y Portal, SSF). Cada bloque lo imparte un desarrollador del núcleo o un investigador (`eps/archive`).
3. [H] La fellowship (EPF) dura 5 meses, normalmente de junio a noviembre, y es sin permiso: cualquiera puede participar (`readme`).
4. [H] Gobernanza técnica. No hay hoja de ruta oficial ni autoridad que la dicte. Hay unos 200 contribuidores repartidos en ~20 equipos. La coordinación ocurre en llamadas públicas All Core Devs (ACD, de ejecución y de consenso) registradas en el repositorio ethereum/pm. El financiamiento de los mantenedores pasa en parte por Protocol Guild (`research/roadmap`, `dev/pm`, `dev/core-development`).
5. [H] Cronología (`protocol/history`):
   - génesis el 30-jul-2015 a las 03:26:13 UTC, con límite de gas de 5,000, que subió a 3,141,592 con "Frontier thawing";
   - Homestead el 14-mar-2016 (EIP-2, EIP-7 con DELEGATECALL, EIP-8);
   - Merge el 15-sep-2022 (EIP-3675);
   - Beacon Chain en marcha desde el 1-dic-2020.
6. [H] El Merge ocurrió el 15-sep-2022 a las 06:42:42 UTC y redujo el consumo eléctrico anualizado "by more than 99.988%" (`research/roadmap`). El primer bloque PoS en cadena, el 15,537,394, tiene sello 06:42:59 UTC (RPC público).
7. [H] Las tablas por "urge" del roadmap marcan como implementados el Beacon Chain, el Merge, los retiros, proto-danksharding, MEV-Boost ("The majority of MEV goes now to Validators"), MaxEB (EIP-7251), EIP-1559 y ERC-4337. Marcan como pendientes SSF, SSLE, firmas cuánticamente seguras, ePBS, quema de MEV, tickets de ejecución, listas de inclusión, tope al conjunto de validadores u Orbit, combate a la centralización de los LST, Verkle, SNARK del Beacon Chain y de la EVM, expiración de historial y de estado, EOF y gas multidimensional (`research/roadmap`).
8. [H] Pectra se activó en la época 364032, el **7-may-2025 a las 10:05 UTC**. Trajo EIP-7251 (hasta 2,048 ETH por validador con credenciales 0x02), EIP-7702 (las EOA delegan en código), EIP-7002 (salidas iniciadas desde la EL) y EIP-6110 (depósitos visibles en menos de 20 min) (`pectra-faq`). El nodo beacon coincide: `ELECTRA_FORK_EPOCH` = 364032.
9. [H] Quema. La base fee se quema: la wiki dice que así da "economic benefit to holders of Eth… counterbalancing inflation" y evita la manipulación de comisiones. La comisión de blobs "is fully burned by the protocol" (`EL/transaction`, `EL/el-specs`).
10. [H] ePBS lleva al protocolo la separación entre proponente y constructor (PBS) que hoy hace MEV-Boost fuera de él. Elimina la dependencia de relays externos y busca menos centralización y más resistencia a la censura. La quema de MEV sería un complemento (`research/PBS/ePBS`). ePBS (EIP-7732) es titular de Glamsterdam ([EF, 17-ago-2026](https://blog.ethereum.org/2026/08/17/plataberget-testnet)).
11. [H] PeerDAS reparte los blobs en columnas con codificación Reed-Solomon. Cada nodo custodia unas columnas y reconstruye el blob con más de 50% de ellas. Las etapas son: 0 (EIP-4844, sin DAS), 1 (1D) y 2 (2D, danksharding completo) (`research/peerdas`). La etapa 1 llegó con Fusaka el 3-dic-2025 ([EF](https://blog.ethereum.org/2025/11/06/fusaka-mainnet-announcement)).
12. [H/O] eODS. El staking delegado es un problema principal-agente. La propuesta tiene dos niveles de stake: uno "pesado" de ~10,000 participantes con slashing y otro "ligero" sin slashing.
    - Vitalik (oct-2023) plantea dos escenarios: (a) con un tope de slashing de 2 ETH, Rocket Pool absorbería el 100% del stake; (b) con el stake topado en 6.25 M ETH y retorno de 1% para el operador. Ambos dan el mismo resultado.
    - De ahí la conclusión: "Delegators should be doing something that actually matters".
    - Se cita la emisión mínima viable (Minimum Viable Issuance, de Elowsson) (`research/eODS`).
13. [H] Finalidad y penalizaciones (`CL/overview`):
    - la wiki estima la finalidad de una transacción en "2.5 epochs: 16 minutes";
    - estar desconectado penaliza poco;
    - el slashing "loses at least 1/32 of their balance". **Desactualizado:** desde Pectra el castigo inicial es 1/4096 (`MIN_SLASHING_PENALTY_QUOTIENT_ELECTRA` = 4096 en la configuración de mainnet), más una penalización correlacionada de 3 veces la fracción castigada (`PROPORTIONAL_SLASHING_MULTIPLIER_BELLATRIX` = 3).
14. [H] Incidentes (`testing/incidents`):
    - The DAO (2016): ~3.6 M ETH, hard fork y ETC;
    - ataques DoS de Shanghai (2016): llevaron a Tangerine Whistle y Spurious Dragon;
    - división minoritaria de Geth (27-ago-2021);
    - pérdida de finalidad en mainnet (11/12-may-2023): "recovered without intervention";
    - DoS latente con bloques de más de 5 MB (feb-2024);
    - blobs lentos tras Dencun (mar-2024);
    - finalidad en Holesky con Pectra (24-feb-2025);
    - raíz de estado incorrecta en Reth (1-sep-2025).
15. [H] Expiración de historial: la tabla del Purge describe EIP-4444 como dejar de guardar historial de más de un año, bajando de terabytes a gigabytes (`research/roadmap`). La expiración parcial, sin los bloques anteriores al Merge (300-500 GB), ya la soportan todos los clientes ([EF, 8-jul-2025](https://blog.ethereum.org/2025/07/08/partial-history-exp)). Lo comprobé: el RPC público no devuelve bloques anteriores al Merge.
16. [O] Filosofía: "Ethereum is NOT a zero sum game with a clear finish line… the Infinite Garden needs to upgrade regularly… until it reaches ossification" (`research/roadmap`).

## 4. Qué cambia para invertir

- **Economía de ETH.**
  - [H] La wiki fija el mecanismo: la base fee y los blobs se queman y la emisión paga el consenso. No da cifras actuales.
  - [H] Al 25-sep-2026:
    - staking de 43.52 M ETH (35.7% de la oferta; 894,331 validadores);
    - el 36% del stake ya está en validadores consolidados 0x02 (23,085 validadores con 15.64 M ETH), gracias a EIP-7251;
    - emisión de ~1.07 M ETH al año;
    - quema de 30 días anualizada en ~15.8 mil ETH;
    - inflación neta de +0.87% al año (ultrasound.money).
  - [I] Consolidar en 0x02 reduce el número de validadores que hay que procesar, un paso hacia SSF u Orbit. No cambia la emisión, que depende del ETH total en staking.
  - [I] El castigo inicial por slashing ahora es mucho menor (1/4096), aunque se mantiene el castigo correlacionado. Eso baja el costo de cola para quien hace staking, pero preserva el costo de un ataque coordinado.
- **Captura de valor de las L2.**
  - [H] PeerDAS y los forks BPO multiplicaron por ~2.3 el espacio de blobs frente a Pectra: el objetivo pasó de 6 a 14 y el máximo de 9 a 21. La EF habla de una capacidad teórica 8 veces mayor con PeerDAS.
  - [H] La demanda está en 4.85 blobs por bloque.
  - [I] Con oferta muy por encima de la demanda, el precio del blob se queda en el piso (EIP-7918). La L2 paga ~0.04 ETH al día a L1 por disponibilidad de datos.
  - [I] La tesis de "ETH se lleva el valor de las L2 por los blobs" no tiene sustento con los números de hoy.
- **Catalizadores del torneo.**
  - [H] La wiki no tiene fechas de 2026; su tabla de roadmap es anterior a Pectra.
  - [H] Fechas verificadas:
    - Glamsterdam en Sepolia el **6-oct-2026 a las 13:53:36 UTC**;
    - en Hoodi el **27-oct-2026 (tentativo)**;
    - en mainnet **sin época**: `GLOAS_FORK_EPOCH` = FAR_FUTURE en dos nodos; objetivo de la EF en dic-2026.
  - [I] Lo que enseña `testing/incidents`: los forks traen incidentes en testnets (Holesky y Sepolia con Pectra) y a veces en mainnet (Prysm tras Fusaka, 5-dic-2025). Un fork dentro del torneo es riesgo de cola además de catalizador.
- **Razón ETH/BTC.**
  - [I] La wiki no la trata.
  - [H] Dato: 0.0320 hoy; −57% desde el Merge; 52 días sobre su SMA200 (Binance).
  - [I] La lección útil del recurso es institucional: Ethereum cambia seguido y reordena sus prioridades. El plan de la EF exige un fork cada 7.2 meses en promedio para llegar a L* en dic-2029. La prima o el descuento frente a BTC depende de si el mercado paga por esa capacidad de cambio o la castiga como riesgo. No hay evidencia aquí para decidirlo.
- **Qué haría falta para que ETH vuelva al universo.**
  - [I] Desde la óptica de este recurso: que Glamsterdam (ePBS y BAL) complete Sepolia y Hoodi sin pérdida de finalidad, y que los clientes publiquen la época de mainnet con diversidad sana (ningún cliente de consenso por encima de 2/3).
  - [I] Criterios completos en el capítulo 02, §8.

## 5. Contrapuntos y límites

1. [H] **Desactualizada en partes:**
   - la tabla del roadmap lista PeerDAS (EIP-7594) como "in research" y EIP-7702 como pendiente, pero ambos ya están en mainnet;
   - `CL/overview` da el castigo de slashing previo a Pectra;
   - `protocol/history` e `incidents` son esbozos.

   Úsese como mapa conceptual, no como estado actual.
2. [H] **Tres cifras de finalidad distintas** según la fuente: 16 min (EPF, `CL/overview`), ~15 min (Vitalik, 2024) y 12.8 min (Mastering Ethereum). Son convenciones distintas:
   - posición media de la transacción dentro de la época, más dos épocas;
   - dos o tres épocas;
   - exactamente dos épocas.
3. [O] **Sesgo de constructor.** La wiki trata cada mejora como deseable. No evalúa si el mercado la valora ni el costo de complejidad para el activo.
4. [I] **No probado:** que ePBS reduzca la centralización de constructores. La propia wiki advierte sobre la concentración de los ganadores de la subasta, como también Vitalik en la parte 3 de su serie.
5. [H] **Lo que no cubrí:** los videos, que son el núcleo del curso. Mi acceso real es la wiki, no las clases.

## 6. Autoexamen

1. **¿Quién decide la hoja de ruta de Ethereum y dónde se registra?**
   No hay hoja de ruta oficial ni autoridad. Unos 200 contribuidores en ~20 equipos coordinan en las llamadas All Core Devs (de ejecución y de consenso), públicas y registradas en ethereum/pm.
   Fuente: `wiki/research/roadmap`, `wiki/dev/pm`.
2. **¿Qué trajo Pectra para quien hace staking y cuándo se activó?**
   - EIP-7251: saldo efectivo de hasta 2,048 ETH con credenciales 0x02, consolidaciones incluidas.
   - EIP-7002: salidas iniciadas desde la EL.
   - EIP-6110: depósitos en menos de 20 min.

   Se activó en la época 364032, el 7-may-2025 a las 10:05 UTC.
   Fuente: `wiki/pectra-faq`, más la configuración de un nodo beacon.
3. **¿Por qué la wiki afirma que ePBS es deseable y qué riesgo deja abierto?**
   Deseable porque quita la dependencia de relays externos y lleva las reglas de construcción al consenso. El riesgo abierto: los constructores que ganan la subasta tienden a concentrarse.
   Fuente: `wiki/research/PBS/ePBS`; Vitalik, parte 3.
4. **¿Qué dato de slashing de la wiki está desactualizado y cuál es el vigente?**
   La wiki dice "at least 1/32". Desde Pectra, el castigo inicial es 1/4096 del saldo efectivo (`MIN_SLASHING_PENALTY_QUOTIENT_ELECTRA` = 4096), más el castigo correlacionado (multiplicador 3).
   Fuente: `wiki/CL/overview`; configuración de mainnet (`/eth/v1/config/spec`, 25-sep-2026).

## 7. Grado de evidencia: **B en mecánica, C en estado del protocolo**

- La mecánica que describe coincide con las especificaciones y la escriben o revisan personas del núcleo: grado B.
- El estado del protocolo (qué ya está en mainnet, parámetros, fechas) está desfasado en varias páginas: grado C, verifíquese siempre contra la configuración del nodo o el blog de la EF.
- No sirve como evidencia sobre precio ni valuación.
