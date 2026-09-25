# 23 · Possible futures of the Ethereum protocol (Vitalik Buterin, 2024)

> Ficha del grupo G2 Ethereum. Estudiada el 25-sep-2026 por el analista cripto. Estado: **estudiado**. Acceso: **íntegro**.
> Capítulo de síntesis: [02-ethereum-historia-protocolo-y-hoja-de-ruta.md](../02-ethereum-historia-protocolo-y-hoja-de-ruta.md). Banco de examen: [banco-g2-ethereum.md](../examen/banco-g2-ethereum.md).

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2024: seis entregas publicadas el 14, 17, 20, 23, 26 y 29 de octubre |
| Autor | Vitalik Buterin, cofundador de Ethereum. Cada entrega agradece revisiones de investigadores de la Ethereum Foundation (EF) y del ecosistema: Justin Drake, Hsiao-wei Wang, Francesco D'Amato, Anders Elowsson, Tim Beiko, Dankrad Feist, entre otros |
| Tipo | Serie de 6 ensayos técnicos en el blog personal del autor |
| Nivel | Experto |
| Costo | Gratis |
| Idioma | Inglés |
| URLs | [1 Merge](https://vitalik.eth.limo/general/2024/10/14/futures1.html) · [2 Surge](https://vitalik.eth.limo/general/2024/10/17/futures2.html) · [3 Scourge](https://vitalik.eth.limo/general/2024/10/20/futures3.html) · [4 Verge](https://vitalik.eth.limo/general/2024/10/23/futures4.html) · [5 Purge](https://vitalik.eth.limo/general/2024/10/26/futures5.html) · [6 Splurge](https://vitalik.eth.limo/general/2024/10/29/futures6.html) |
| Conflictos de interés | El autor es cofundador y la voz más influyente del protocolo. Su reputación y, según reportes públicos, parte de su patrimonio dependen de ETH; **no verifiqué sus tenencias**. Los revisores son en su mayoría investigadores de la EF. No es una hoja de ruta oficial: la wiki del EPF recuerda que "there is no official roadmap and no authority which could dictate it" ([epf.wiki, roadmap](https://epf.wiki/#/wiki/research/roadmap)). |

## 2. Acceso real

- **Nivel: íntegro.** Descargué el 25-sep-2026 los seis artículos desde vitalik.eth.limo, convertí el HTML a texto y leí completo el cuerpo de cada entrega: Merge (~3,700 palabras), Surge (~6,400), Scourge (~4,300), Verge (~6,000), Purge (~5,700) y Splurge (~5,900).
- No vi las imágenes incrustadas (diagramas en base64). No seguí la mayoría de los enlaces a ethresear.ch. Las cifras que cito las **recalculé en Python** cuando eran aritmética del autor.
- Lo que pasó después de oct-2024 lo contrasté con fuentes primarias: la configuración de dos nodos beacon de mainnet (publicnode y Lodestar), un RPC de ejecución, anuncios del blog de la EF, el repositorio ethereum/pm y la API pública de L2BEAT.

## 3. Lo esencial

**The Merge (parte 1)**
1. [H] En oct-2024 finalizar un bloque tomaba 2-3 épocas (~15 min) y hacía falta 32 ETH para ser validador. Las metas son finalidad en un solo slot (SSF) y stake mínimo de 1 ETH. Las dos chocan con el costo de procesar firmas (parte 1).
2. [H] Hay cuatro caminos: status quo, SSF por fuerza bruta (agregar más de 1 millón de firmas en 5-10 s), Orbit SSF (comités medianos) y staking en dos niveles. EIP-7251 (consolidación de saldos) es la etapa inicial de Orbit (parte 1). EIP-7251 entró en mainnet con Pectra: el tope efectivo subió a 2,048 ETH (config `MAX_EFFECTIVE_BALANCE_ELECTRA`, nodo beacon, 25-sep-2026).
3. [O] Orbit acepta un costo de ataque unas 10 veces menor: "$2.5 billion cost of attack instead of $25 billion". Según el autor, "It's a common view that Ethereum today has far more economic finality than it needs" (parte 1).
4. [H] Bajar el slot de 12 a 4 s exigiría acotar la latencia de red a 2 s, con riesgo de centralización geográfica. Las preconfirmaciones mejoran el caso promedio (0.5 s contra ~6 s), no el peor caso (12 s) (parte 1). Al 25-sep-2026 el slot sigue en 12 s (`SECONDS_PER_SLOT` = 12).
5. [H/O] Propone subir el quórum de 67% a 80%; así bastaría 21% de solo stakers para bloquear una "victoria limpia" de un ataque. Afirma que hubo "only one (very brief) finality failure in all of Ethereum's history" (parte 1). Ver el contrapunto 5.2.

**The Surge (parte 2)**
6. [H] Con Dencun (13-mar-2024) había ~3 blobs de ~125 kB por slot: 375 kB por slot, que dan 173.6 TPS con transferencias ERC-20 de ~180 bytes (recalculado: 375,000/12/180 = 173.6). Con PeerDAS el plan era un objetivo de 8-16 blobs (463-926 TPS). A mediano plazo, 16 MB por slot y ~58,000 TPS con compresión (recalculado: 16e6/12/23 bytes ≈ 57,971) (parte 2).
7. [H] PeerDAS es muestreo 1D: cada blob es un polinomio de grado 4096 y basta con 64 de 128 muestras para recuperarlo (EIP-7594). Después vendría el muestreo 2D (parte 2). PeerDAS llegó con Fusaka el 3-dic-2025. Dos forks BPO subieron objetivo y máximo a 10/15 (9-dic-2025) y a 14/21 (7-ene-2026) ([EF, 6-nov-2025](https://blog.ethereum.org/2025/11/06/fusaka-mainnet-announcement); `BLOB_SCHEDULE` del nodo beacon).
8. [H] Etapas de los rollups:
   - **Etapa 1:** sistema de pruebas; un consejo de seguridad puede anularlo con 75%, y al menos 26% del consejo debe ser externo.
   - **Etapa 2:** el consejo solo interviene ante bugs demostrables.
   - En oct-2024, entre los rollups EVM completos solo Optimism y Arbitrum estaban en etapa 1 (parte 2).
9. [O] Si todo se va a L2 y L1 no escala, "the economic situation of ETH the asset becomes more risky" y cae el incentivo a ser L2 en vez de L1 (parte 2). Es la base del giro de 2025-26 hacia escalar L1.

**The Scourge (parte 3)**
10. [H] "Two actors are choosing the contents of roughly 88% of Ethereum blocks". Si censuran, una transacción espera en promedio ~9 slots (114 s contra 6 s) (parte 3).
11. [H] La solución líder combina listas de inclusión por comité (FOCIL: si k = 16, retrasar un bloque requiere que los 16 censuren) con subasta en protocolo del constructor (APS). Las alternativas son BRAID o proponentes concurrentes, y los mempools cifrados (parte 3). FOCIL (EIP-7805) es el titular de capa de consenso de Hegotá, el fork posterior a Glamsterdam ([EF, 7-sep-2026](https://blog.ethereum.org/2026/09/07/protocol-priorities)).
12. [H] En oct-2024 ~30% del ETH estaba en staking. El autor teme que casi todo se stakee: el staking se volvería un deber, se debilitaría la credibilidad del slashing, un solo token de staking líquido (LST) absorbería la función de "dinero" y habría una emisión innecesaria de "~1m ETH/year" (parte 3). Al 25-sep-2026 hay 43.52 M ETH en staking: **35.7% de la oferta** (cálculo propio con el conjunto de validadores de un nodo beacon).
13. [O] El staking en dos niveles equivale a reducir la emisión: un mundo con 3.4% de rendimiento para el nivel con riesgo y 2.6% para el nivel sin riesgo es económicamente igual a uno con 0.8% y 0% (parte 3).
14. [H] El MEV es opaco para el protocolo. Además es volátil: cada validador propone un bloque cada ~4 meses. Por eso dificulta topar el stake. Las propuestas son el suavizado de MEV y la quema de MEV (Drake) (parte 3).
15. [H] Un VPS para nodo cuesta ~$60 al mes. Con 32 ETH = $84,000, eso resta ~0.85% de APY (recalculado: 720/84,000 = 0.857%). Si el rendimiento total baja de ~0.85%, el staking en solitario deja de ser viable (parte 3).

**The Verge (parte 4)**
16. [H] El estado crece ~30 GB al año. Peor caso del testigo sin estado:
    - con el Merkle-Patricia actual: 330 MB;
    - con árbol binario y código merkelizado: 10.4 MB;
    - con Verkle: ~1.3 MB, o 2.6 MB con prefijos minados adversarialmente.

    Recalculé las tres cifras. Verkle no resiste computadoras cuánticas. La alternativa son los árboles binarios de hash con STARK (parte 4).
17. [H] En oct-2024 el prover de EVM más rápido tardaba ~15 s en probar un bloque promedio con cientos de GPUs; la meta es menos de 4 s (parte 4). [O] "EVM validity proofs at L1 can enable considerable L1 gas limit increases".

**The Purge (parte 5)**
18. [H] Un nodo ocupaba ~1.1 TB: ~300 GB de estado y ~800 GB de historial. Los datos de consenso se guardan ~6 meses y los blobs ~18 días. EIP-4444 propone expirar el historial (parte 5). La expiración parcial (quitar los bloques anteriores al Merge, 300-500 GB) ya la soportan todos los clientes ([EF, 8-jul-2025](https://blog.ethereum.org/2025/07/08/partial-history-exp)). Lo comprobé: el RPC público ya no devuelve bloques anteriores al Merge.
19. [H] Encontrar una colisión de direcciones cuesta hoy ~2^80 hashes, al alcance de actores muy ricos: todas las GPUs del mundo tardarían ~1/4 de año (recalculado: 2^80 / (2^27·3.15e7·2^30) ≈ 0.25). Por eso el problema del espacio de direcciones es inevitable (parte 5).

**The Splurge (parte 6)**
20. [H] EIP-1559 apunta en realidad a bloques llenos al ~50-53%, por la desigualdad AM-GM, y se ajusta lento en extremos. EIP-4844 usa una fórmula más limpia. El gas multidimensional aparece en EIP-7706 y EIP-7623 (parte 6). EIP-7623 entró con Pectra.
21. [H] En oct-2024 el autor escribió que EOF estaba "scheduled to be included in the next hard fork" y que EIP-7702 entraría en el siguiente fork (parte 6). EIP-7702 sí entró en Pectra (7-may-2025, época 364032). **EOF no**: en jun-2025 estaba "postponed indefinitely" (Mastering Ethereum 2.ª ed., cap. 14) y no figura en la lista de Glamsterdam ([EF, 17-ago-2026](https://blog.ethereum.org/2026/08/17/plataberget-testnet)).
22. [O] Las "Egyptian god protocols" son ZK-SNARKs (maduros), FHE e iO; a ellas se suman las firmas de un solo uso cuánticas. El autor compara el efecto de los SNARKs con el de los transformers en IA. La iO sigue siendo "millions of times too slow" (parte 6).

## 4. Qué cambia para invertir

Datos al 25-sep-2026. La tabla completa y la verificación están en el [capítulo 02](../02-ethereum-historia-protocolo-y-hoja-de-ruta.md#datos-verificados-al-25-sep-2026).

- **Economía de ETH.**
  - [H] El temor de la parte 3 se cumplió a medias: el staking subió de ~30% a 35.7%, sin llegar a "casi todo".
  - [H] Con 43.52 M ETH en staking, la emisión máxima de consenso es ~1.10 M ETH al año y el APR máximo de consenso es 2.52%. Uso la fórmula de consensus-specs (`BASE_REWARD_FACTOR` = 64), que da ≈166.3·√S ETH al año. ultrasound.money reporta una emisión real de 1.07 M al año. El stETH de Lido rinde 2.25% neto de su comisión (media de 7 días).
  - [H] La quema se desplomó. En los últimos 30 días sumó 1,297 ETH, unos 15.8 mil ETH al año anualizados.
  - [H] Resultado: inflación neta de **+0.87% al año** en 30 días. Desde el Merge la oferta subió **+1.29%**, de 120.52 M a 122.07 M.
  - [I] La emisión de "~1 M ETH al año" que el autor llamaba "innecesaria" hoy casi no se compensa con quema. Quien no hace staking se diluye ~0.9% al año. Quien sí lo hace gana ~2.5% bruto, **~1.6% por encima de la dilución**.
  - [I] Nuestra cuenta es solo spot y no captura ese rendimiento. Un ETH sin stakear tiene un arrastre de ~0.9% al año frente al ETH stakeado.
- **Captura de valor de las L2.**
  - [H] La parte 2 entregó lo prometido en oferta de blobs: objetivo 14 y máximo 21.
  - [H] La demanda no la siguió. En 1,024 bloques del 25-sep-2026 hubo **4.85 blobs por bloque**, a ~1.0e-6 ETH por blob, es decir **~0.04 ETH al día** de quema por blobs, contra ~29.5 ETH al día por base fee en la misma muestra.
  - [I] Hoy la L2 casi no paga renta a L1 por disponibilidad de datos. Solo a partir de 14 blobs de demanda sostenida el precio deja el piso de EIP-7918 (base fee/16 por unidad de blob gas).
  - [I] El vínculo de valor de las L2 con ETH pasa por ETH como dinero y colateral en las L2 y por el gas de liquidación en L1, no por comisiones de DA.
  - [H] Ninguna L2 grande está en etapa 2. Según la API de L2BEAT (25-sep-2026), Base ($16.4 mil millones), Arbitrum One ($11.7 mil millones) y OP Mainnet ($2.0 mil millones) siguen en etapa 1.
- **Catalizadores del torneo (28-sep-2026 → 28-ene-2027).**
  - [H] Glamsterdam en la testnet Sepolia: **6-oct-2026, 13:53:36 UTC** (época 353024). Así lo confirma el ACDT #97 del 21-sep-2026 ([ethereum/pm #2225](https://github.com/ethereum/pm/issues/2225)); verifiqué el sello de tiempo con la génesis de Sepolia.
  - [H] Hoodi: **27-oct-2026, tentativo**.
  - [H] Mainnet: **sin fecha**. En los nodos, `GLOAS_FORK_EPOCH` sigue en FAR_FUTURE. La EF planea "Shipping Glamsterdam in December 2026" ([EF, 7-sep-2026](https://blog.ethereum.org/2026/09/07/protocol-priorities)).
  - [H] Contenido de Glamsterdam: ePBS (EIP-7732) y BAL (EIP-7928), más un reajuste de precios de gas "aimed at a ~200M gas floor" (EIP-8007, 8037 y 8038). Ese reajuste da "roughly a 3x increase in base throughput" ([EF, 24-ago-2026](https://blog.ethereum.org/2026/08/24/glamsterdam-repricing-testing)).
  - [I] Base empírica: de Hoodi a mainnet pasaron 42 días en Pectra y 36 en Fusaka. Si Hoodi sale el 27-oct, mainnet caería hacia el 2-8 de diciembre de 2026, dentro del torneo.
  - [H] Riesgo de retraso alto: en feb-2026 la EF apuntaba a "first half of 2026".
  - [I] FOCIL (Hegotá) y el trabajo post-cuántico **no** caen dentro del torneo.
- **Razón ETH/BTC.**
  - [H] ETH/BTC está en 0.0320, 57% abajo del nivel del Merge (0.0747).
  - [H] Lleva 52 días sobre su SMA200 (0.0294).
  - [H] Tras el Merge, el retorno a 122 días de ETH/BTC fue negativo en 79% de las ventanas (mediana −9.3%; datos diarios de Binance).
  - [I] La tesis del autor se centra en la seguridad y en que el protocolo sea neutral. Nada en la serie promete que el valor fluya hacia ETH frente a BTC. Una hoja de ruta exitosa no implica que ETH/BTC suba.
- **Qué haría falta para que ETH vuelva al universo.**
  - [I] Leída con este recurso, la condición técnica sería que Glamsterdam pase Sepolia y Hoodi sin incidentes de finalidad y que los clientes publiquen una época de mainnet.
  - [I] La condición económica sería evidencia de demanda que devuelva la quema: por ejemplo, inflación neta de 30 días menor a +0.5% al año o blobs promedio por encima del objetivo de 14.
  - [I] Las demás condiciones de mercado y de tamaño están en el capítulo 02, §8.

## 5. Contrapuntos y límites

1. **Sesgo del autor.**
   - [O] Es un menú de opciones técnicas escrito por quien más influye en el protocolo: "not meant as an exhaustive list". El tono sobreestima la capacidad de coordinar cambios; el propio autor reconoce que la interoperabilidad entre L2 es "primarily" un problema social.
   - [O] El autor casi no toca el precio de ETH. Cuando lo toca (parte 2) es de pasada.
2. **Datos que envejecieron o no cuadran.**
   - [H] EOF, "programado", no llegó.
   - [H] "Only one (very brief) finality failure" no cuadra con dos pérdidas de finalidad en 24 h en mayo de 2023, de 25 min y de más de 1 h ([EPF wiki, incidentes](https://epf.wiki/#/wiki/testing/incidents); crypto.news). Puede ser una diferencia de conteo; no lo resolví.
   - [H] Después vino el bug de Prysm del 5-dic-2025: la participación cayó a 74.7%, a ~9 pp de perder la finalidad (Cointelegraph).
3. **Lo que no está probado.**
   - [I] La seguridad de Orbit SSF, el efecto de topar el stake sobre quién se queda, el muestreo 2D y las pruebas zkEVM obligatorias en L1. Estas llegarían en K* o L*, según la EF (7-sep-2026).
   - [I] Tampoco está probado que escalar L1 aumente el valor capturado por ETH. Con más oferta de espacio de bloque y sin más demanda, el precio por unidad cae; el argumento de James Prestwich aparece en Mastering Ethereum 2.ª ed., cap. 14.
4. **Supuestos de cifras.**
   - [I] Los TPS asumen transferencias ERC-20 de ~180 bytes.
   - [I] El dato de 607 TPS con calldata usa el **objetivo** de 15 M de gas, no el máximo. Con 30 M la cuenta da 1,042 (cálculo propio).
   - [I] En la parte 4 escribe 4,800,800 bytes; la cuenta da 4,800,000.
5. **Qué sí se cumplió.**
   - [H] Blobs al objetivo de 14 (dentro del rango 8-16 que anticipaba).
   - [H] EIP-7702 y EIP-7251 en mainnet.
   - [H] Expiración parcial del historial.
   - [H] FOCIL como titular de Hegotá.

## 6. Autoexamen

1. **¿Por qué, según la parte 3, "casi todo el ETH en staking" es un riesgo y no un logro?**
   Porque:
   - el staking se volvería un deber y se delegaría a quien sea más cómodo;
   - el slashing pierde credibilidad;
   - un LST dominante podría quedarse con la función de dinero de ETH;
   - se emitirían ~1 M ETH al año de más.

   Fuente: [parte 3](https://vitalik.eth.limo/general/2024/10/20/futures3.html), sección "Fixing staking economics".
2. **Calcula los TPS máximos de rollups con 16 MB por slot, sin compresión y con compresión ideal con estado (~23 bytes).**
   16,000,000/12/180 = 7,407 TPS sin compresión. 16,000,000/12/23 ≈ 57,971, es decir ~58,000 TPS.
   Fuente: [parte 2](https://vitalik.eth.limo/general/2024/10/17/futures2.html) y recálculo propio.
3. **¿Qué exige la etapa 1 de un rollup y qué agrega la etapa 2, según Vitalik?**
   - Etapa 1: un sistema de pruebas sin confianza. El consejo solo puede anularlo con 75% de los votos, y al menos 26% del consejo debe ser externo a la empresa. Las actualizaciones de gobernanza más débiles deben tener un retraso que permita salir.
   - Etapa 2: el consejo solo interviene ante bugs demostrables, y las actualizaciones tienen un retraso muy largo.

   Fuente: parte 2, "Maturing L2 proof systems".
4. **¿Qué pasó con EOF y con EIP-7702 respecto de lo que anunciaba la parte 6?**
   EIP-7702 sí entró en Pectra, el 7-may-2025. EOF quedó "postponed indefinitely" en jun-2025 y no está en la lista de Glamsterdam.
   Fuentes: parte 6; Mastering Ethereum 2.ª ed., cap. 14 (nota de jun-2025); [EF, 17-ago-2026](https://blog.ethereum.org/2026/08/17/plataberget-testnet).

## 7. Grado de evidencia: **B**

- **A** en la mecánica del protocolo y en la aritmética: está verificable contra especificaciones y la recalculé.
- **C** en los pronósticos de la hoja de ruta: son intenciones del autor, no compromisos; varias ya se movieron, como EOF, la posición de Verkle y los tiempos de Glamsterdam.
- El promedio queda en B porque la lectura fue íntegra, la fuente es primaria para las intenciones de diseño y las cifras clave aguantaron el recálculo. Aun así, no es evidencia sobre el valor del activo.
