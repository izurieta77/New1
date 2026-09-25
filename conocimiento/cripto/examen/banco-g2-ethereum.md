# Banco de examen G2 · Ethereum (8 preguntas difíciles)

> Autor: analista cripto, 25-sep-2026. Se usa **a libro cerrado**. Material de estudio: [capítulo 02](../02-ethereum-historia-protocolo-y-hoja-de-ruta.md) y las fichas [01](../recursos/01-the-infinite-machine.md), [11](../recursos/11-the-cryptopians.md), [21](../recursos/21-read-write-own.md), [23](../recursos/23-possible-futures-of-the-ethereum-protocol.md), [24](../recursos/24-epf-study-group-protocol-wiki.md) y [27](../recursos/27-mastering-ethereum-2-a-edicion.md).
> Cada pregunta vale 10 puntos. Los datos "de hoy" son del 25-sep-2026. Si el banco se reutiliza después, el examinador debe actualizar las cifras de mercado y calificar el **método** con los datos nuevos.
> **Aviso:** este archivo contiene la clave. Si se usa para un examen con compromiso previo, sepárense preguntas y clave según `conocimiento/examenes/PROTOCOLO.md`.

---

## P1. Emisión, quema e inflación neta (cálculo)

**Pregunta.** La especificación de consenso fija `BASE_REWARD_FACTOR` = 64 y `EFFECTIVE_BALANCE_INCREMENT` = 10⁹ Gwei, y el año tiene ~82,181 épocas. Con S = 43.52 M ETH en staking y 98% de participación:
- (a) deriva la emisión anual máxima de consenso;
- (b) calcula el APR máximo de consenso;
- (c) calcula la inflación neta anual si la quema de los últimos 30 días fue de 1,297 ETH y la oferta es de 122.07 M;
- (d) calcula qué quema anual haría falta para que la inflación neta baje de 0.5%.

**Respuesta de referencia.**
- (a) Recompensa base por incremento = 10⁹·64/√(S·10⁹) Gwei. Emisión por época ≈ 64·√(S·10⁹) Gwei ≈ 0.002024·√S ETH. Al año: ≈ **166.3·√S**, es decir 166.3·6,597 ≈ **1.097 M ETH al año** al 100%; ≈ 1.075 M al 98%. ultrasound.money reporta 1.07 M.
- (b) 166.3/√S = **2.52%** máximo (≈2.47% con 98% de participación).
- (c) Quema anualizada = 1,297·(365/30) ≈ 15.8 mil ETH. Inflación neta ≈ (1.075 M − 15.8 mil)/122.07 M ≈ **+0.87% al año**.
- (d) Inflación < 0.5% exige un aumento neto < 610 mil ETH (0.5% × 122.07 M). Por lo tanto, quema > 1.075 M − 610 mil ≈ **465 mil ETH al año**, ~29 veces la quema actual.

**Fuente.** consensus-specs (phase0 y altair, `get_base_reward_per_increment`); ultrasound.money (gauge-rates y burn-sums, 25-sep-2026); capítulo 02, §3 y §5.

**Rúbrica.** (a) fórmula y orden de magnitud: 4 pts; (b) 2 pts; (c) 2 pts; (d) 2 pts. Penalizar si se confunde la emisión con la inflación neta.

---

## P2. Blobs, EIP-7918 y captura de valor de las L2

**Pregunta.** Tras BPO2, el objetivo es de 14 blobs y el máximo de 21. Hoy se usan 4.85 blobs por bloque y la base fee de ejecución es de 0.117 gwei.
- (a) Explica por qué la comisión de blobs no cae a 1 wei y calcula su nivel de referencia por unidad de blob gas y por blob (131,072 de blob gas por blob).
- (b) Estima la quema diaria por blobs con 7,200 bloques al día.
- (c) Concluye qué implica esto para la tesis de que "ETH captura el valor de las L2".

**Respuesta de referencia.**
- (a) Sin EIP-7918, un uso debajo del objetivo bajaría el precio del blob hasta 1 wei. EIP-7918 (Fusaka) impone un precio de reserva: si GAS_PER_BLOB·blob_fee < BLOB_BASE_COST·base_fee, con BLOB_BASE_COST = 2¹³, ya no se resta el objetivo del exceso y el precio vuelve a subir. El precio gravita alrededor de base_fee·8192/131072 = base_fee/16 ≈ **0.0073 gwei por blob gas**, o sea ≈ 9.6e-7 ETH por blob. El dato observado ronda ~1.0e-6 ETH por blob.
- (b) 4.85 × 7,200 × ~1e-6 ≈ **0.035 ETH al día**. La muestra de RPC dio 0.036 ETH al día, frente a ~29.5 ETH al día por base fee en la misma muestra (0.12%).
- (c) La oferta de espacio de blobs (PeerDAS + BPO) creció más que la demanda. Las L2 casi no pagan renta a L1 por disponibilidad de datos. La captura de valor por comisiones **no está demostrada**; lo que queda es la demanda monetaria de ETH (gas y colateral dentro de las L2) y el gas de liquidación en L1. Sube solo si la demanda de blobs supera el objetivo de 14.

**Fuente.** Texto de EIP-7918 (BLOB_BASE_COST 2¹³); anuncio de Fusaka de la EF (6-nov-2025); `eth_feeHistory` (25-sep-2026); capítulo 02, §5 y §6 (ideas 3 y 4).

**Rúbrica.** Mecanismo de reserva: 4 pts; cálculo: 3 pts; conclusión con matiz (sin decir "ETH no captura nada"): 3 pts.

---

## P3. Finalidad, incidentes y un error del libro

**Pregunta.**
- (a) ¿Por qué Casper FFG necesita justificar y luego finalizar, y qué garantiza la finalidad?
- (b) ¿Qué pasa si más de 1/3 del stake se desconecta?
- (c) Enumera los incidentes de finalidad en mainnet y el casi-incidente de 2025, con fechas y cifras.
- (d) *Mastering Ethereum* 2.ª ed. afirma que el "proposer boost" se añadió en el hard fork Dencun. ¿Es correcto?

**Respuesta de referencia.**
- (a) Justificar es observar un enlace de supermayoría (2/3 del stake) desde la vista local del nodo, que todavía se puede revertir. Finalizar es justificar el checkpoint hijo directo, lo que prueba que 2/3 ya vieron la justificación. Revertir un checkpoint finalizado exige slashing de al menos 1/3 del stake (seguridad responsable y finalidad económica). Toma ~2 épocas: 12.8 min, con un checkpoint cada 6.4 min.
- (b) La cadena sigue produciendo bloques porque LMD-GHOST da vivacidad, pero no finaliza. Se activa la fuga por inactividad, que va reduciendo el saldo de los inactivos hasta que los activos vuelven a sumar 2/3.
- (c) Dos pérdidas de finalidad en 24 h, el 11 y 12-may-2023: 25 min y más de 1 h, por bugs de Prysm y Teku con atestaciones viejas. El 5-dic-2025, tras Fusaka, un bug de Prysm v7.0.0 bajó la participación a 74.7%, a ~9 pp de perder la finalidad, sin perderla. Nota: Vitalik (oct-2024) dice "only one (very brief) finality failure"; es una discrepancia de conteo.
- (d) **No.** `PROPOSER_SCORE_BOOST` = 40 está en la especificación de fork choice de phase0 y se adoptó antes, como regla de fork choice en los clientes. No es una característica de Dencun; es un error del libro.

**Fuente.** *Mastering Ethereum* 2.ª ed., cap. 15; consensus-specs (phase0, `fork-choice.md`); wiki del EPF, `testing/incidents`; Cointelegraph (dic-2025); Vitalik, parte 1.

**Rúbrica.** (a) 3 pts; (b) 2 pts; (c) 3 pts; (d) 2 pts.

---

## P4. The DAO: hechos, fork y la atribución de *The Cryptopians*

**Pregunta.**
- (a) Según la SEC, ¿cuánto recaudó The DAO, cuándo, cuánto se desvió y cuándo se activó el hard fork?
- (b) ¿Qué concluyó la SEC y por qué importa para un inversionista en ETH?
- (c) Laura Shin atribuye el ataque a un exdirectivo. ¿A quién, con qué evidencia, qué grado le das y por qué el titular de "US$11 mil millones" es engañoso?

**Respuesta de referencia.**
- (a) Del 30-abr al 28-may-2016 vendió ~1.15 mil millones de tokens por ~12 M ETH (~US$150 M). El 17-jun-2016 se desviaron ~3.6 M ETH (1/3), y el código impidió moverlos durante 27 días. El hard fork se activó el 20-jul-2016; la minoría siguió en Ethereum Classic.
- (b) Que los tokens DAO eran valores y su oferta debía registrarse (SEC Release No. 81207, 25-jul-2017). Importa porque es el precedente del riesgo regulatorio de los tokens emitidos en Ethereum y anticipó el fin de la era de las ICOs. Además, el fork mostró que las reglas de Ethereum son sociales y modificables.
- (c) A Toby Hoenisch, ex-CEO de TenX. La evidencia es un rastreo con Chainalysis: ETC → BTC (ShapeShift) → Wasabi → exchanges → Grin, hasta el nodo "grin.toby.ai" y una IP asociada a "TenX". Hoenisch lo niega y no hay resolución judicial: **grado C**. El titular es engañoso porque, tras el fork, en la cadena ETH los fondos se devolvieron. El botín utilizable estaba en **ETC**; los US$11 mil millones son una valuación nocional de 3.6 M ETH a precios de 2022.

**Fuente.** SEC Release No. 81207; The Block (22-feb-2022); Stockhead (22-feb-2022); fichas 11 y 01.

**Rúbrica.** (a) 4 pts, con cifras y fechas exactas; (b) 2 pts; (c) 4 pts, con grado justificado y el matiz ETC/ETH.

---

## P5. Economía del staking: el argumento de la parte 3 y el estado actual

**Pregunta.**
- (a) Enumera los cuatro riesgos que Vitalik asocia con que "casi todo el ETH" esté en staking.
- (b) Explica su argumento de que el staking en dos niveles equivale a bajar la emisión, con su ejemplo numérico.
- (c) Con los datos de hoy (staking de 35.7% de la oferta, Lido ~22.5%, 36% del stake en credenciales 0x02, castigo inicial de slashing 1/4096), evalúa si el riesgo aumentó o disminuyó desde oct-2024.

**Respuesta de referencia.**
- (a) Cuatro riesgos:
  - el staking se vuelve un deber y se delega en operadores centralizados cómodos;
  - pierde credibilidad el slashing;
  - un LST dominante absorbe la función de "dinero" de ETH;
  - se emite de más (~1 M ETH al año), valor que podría capturar el LST.
- (b) Si el nivel con riesgo rinde 3.4% y el nivel sin riesgo, en el que participan todos, rinde 2.6%, la situación es económicamente igual a un 0.8% por hacer staking y 0% por solo tener ETH. La dinámica del nivel con riesgo es la misma, así que es más simple reducir la emisión (o topar el stake). Contraargumento: dar al nivel "sin riesgo" algún papel y algún riesgo reales.
- (c) Balance:
  - **Aumentó** la fracción en staking: de ~30% a 35.7%.
  - **Bajó** la concentración en Lido: de 29% en el libro a ~22.5%, lejos del umbral de 33%.
  - La consolidación 0x02 (EIP-7251) reduce la carga de mensajes, un paso hacia SSF u Orbit, pero no cambia la emisión.
  - El castigo inicial de 1/4096 abarata el error aislado; el castigo correlacionado (×3) preserva el costo de un ataque.
  - La emisión (~1.07 M ETH al año) casi no se compensa con quema: inflación de +0.87%.
  - Conclusión: el riesgo de "emisión innecesaria" hoy es **mayor** en efecto económico, aunque el de LST dominante sea menor.

**Fuente.** Vitalik, parte 3; *Mastering Ethereum*, cap. 13; configuración de mainnet (`MIN_SLASHING_PENALTY_QUOTIENT_ELECTRA`, `PROPORTIONAL_SLASHING_MULTIPLIER_BELLATRIX`); nodo beacon; `eth_call` a stETH; ultrasound.money.

**Rúbrica.** (a) 3 pts; (b) 3 pts; (c) 4 pts, con evaluación en dos sentidos.

---

## P6. Etapas de los rollups: tres versiones y el estado real

**Pregunta.**
- (a) Define las etapas 0, 1 y 2 según Vitalik (oct-2024).
- (b) ¿En qué difiere la etapa 1 según *Mastering Ethereum* (feb-2025)?
- (c) ¿Qué L2 grandes están hoy en etapa 1 o 2 según L2BEAT, y qué implica eso para el riesgo de un usuario de L2 y para la tesis de ETH?

**Respuesta de referencia.**
- (a) Según Vitalik:
  - Etapa 0: la validación es de confianza.
  - Etapa 1: sistema de pruebas sin confianza; el consejo de seguridad solo lo anula con 75% y al menos 26% del consejo es externo; las actualizaciones débiles tienen un retraso que permite salir.
  - Etapa 2: el consejo solo interviene ante bugs demostrables (por ejemplo, pruebas en conflicto), con un retraso de actualización muy largo.
- (b) El libro pide al menos 5 actores externos que puedan enviar pruebas, salir sin el operador, ventana de salida de al menos 7 días y un consejo con al menos 50% de 8 o más firmantes, la mitad externos. Para la etapa 2: pruebas abiertas, al menos 30 días para salir y consejo limitado a errores de solidez. El libro advierte que los requisitos cambiaron. Conclusión: el marco evoluciona y hay que consultar L2BEAT al día.
- (c) Datos de L2BEAT:
  - En etapa 1: Base (~US$16.4 mil millones), Arbitrum One (~11.7), OP Mainnet (~2.0), Starknet, Ink y Unichain.
  - En etapa 2 solo hay proyectos marginales (~US$1 M en total).
  - En etapa 0 hay 71 proyectos.

  Implicaciones:
  - Para el usuario de L2 persiste el riesgo de consejos de seguridad y actualizaciones.
  - Para ETH, la meta de L2 que "hereden por completo" la seguridad de L1 sigue sin cumplirse en las grandes, y el pago de las L2 a L1 por datos es mínimo (~0.04 ETH al día).

**Fuente.** Vitalik, parte 2; *Mastering Ethereum*, cap. 16; API de L2BEAT (25-sep-2026).

**Rúbrica.** (a) 3 pts; (b) 3 pts; (c) 4 pts.

---

## P7. Glamsterdam dentro del torneo (28-sep-2026 → 28-ene-2027)

**Pregunta.**
- (a) ¿Qué trae Glamsterdam?
- (b) Da las fechas verificadas de testnets y el estado de mainnet, con la evidencia de que mainnet no está programado.
- (c) Estima cuándo caería mainnet usando los intervalos Hoodi → mainnet de Pectra y Fusaka, y lista tres razones para dudar de esa estimación.
- (d) ¿Por qué un fork es a la vez catalizador y riesgo de cola para una posición en ETH?

**Respuesta de referencia.**
- (a) Contenido:
  - ePBS (EIP-7732): la separación entre proponente y constructor pasa a ser parte del protocolo.
  - Listas de acceso a nivel de bloque (EIP-7928, BAL): paralelización y sincronización.
  - Reajuste de gas (EIP-8007, 8037, 8038) "aimed at a ~200M gas floor", con "roughly 3x base throughput" y una dimensión de gas de estado.
  - Contratos más grandes (EIP-7954) y EIP-7688.
- (b) Fechas y estado:
  - Sepolia: **6-oct-2026 13:53:36 UTC**, época 353024, confirmado en el ACDT #97 del 21-sep-2026.
  - Hoodi: **27-oct-2026, tentativo**.
  - Mainnet: sin época. `GLOAS_FORK_EPOCH` = FAR_FUTURE en dos nodos beacon (25-sep-2026). La EF (7-sep-2026) apunta a "December 2026".
- (c) Estimación: Pectra tardó 42 días de Hoodi a mainnet (26-mar → 7-may-2025) y Fusaka 36 (28-oct → 3-dic-2025). Si Hoodi sale el 27-oct, mainnet caería hacia el **2-8 de diciembre de 2026**, dentro del torneo. Razones para dudar:
  1. El fork ya se retrasó del primer semestre (EF, 18-feb-2026) a diciembre (EF, 7-sep-2026).
  2. Pectra tuvo incidentes en Holesky y Sepolia.
  3. Según la cobertura de prensa del ACDT #97, ningún devnet privado había logrado una activación estable, y la fecha de Hoodi es tentativa.
- (d) Es catalizador porque ePBS, más capacidad y precios de gas nuevos pueden cambiar las expectativas. Es riesgo de cola porque los forks han traído pérdidas de finalidad y casi-pérdidas (Prysm tras Fusaka), y un bug en un cliente con supermayoría (Lighthouse corría en 52.55% de los nodos de consenso en dic-2025) podría finalizar una cadena inválida si superara 2/3. Además, el estudio de eventos (n = 5) no muestra un efecto consistente en ETH/BTC.

**Fuente.** EF (17-ago, 24-ago y 7-sep-2026; 18-feb-2026; 6-nov-2025; Pectra 2025); ethereum/pm #2225; configuración de nodos beacon; capítulo 02, §9.

**Rúbrica.** (a) 2 pts; (b) 3 pts, con la prueba de "sin programar"; (c) 3 pts; (d) 2 pts.

---

## P8. ETH/BTC, reentrada y dimensionamiento (con un error que detectar)

**Pregunta.**
- (a) Resume la evidencia sobre ETH/BTC desde el Merge (nivel, tendencia, retornos a 122 días y efecto del filtro SMA200).
- (b) Con una cuenta cripto de 10,000 MXN y un tope de pérdida de 5,000 MXN, ¿qué peso máximo de ETH propones y por qué?
- (c) *Mastering Ethereum* dice que con un límite de 36 M de gas caben "around 1,428" transferencias simples por bloque. Corrige el dato y explica por qué subir el límite de gas no garantiza más quema.

**Respuesta de referencia.**
- (a) ETH/BTC:
  - Pasó de 0.0747 en el Merge a 0.0320 hoy: −57%.
  - Mínimo de 0.01805 el 21-abr-2025; rango de 12 meses de 0.0258 a 0.0376.
  - Lleva 52 días sobre su SMA200 (0.0294), con la SMA50 por encima.
  - Retornos a 122 días desde el Merge: mediana de −9.3% y P(>0) = 20.7%.
  - Condicionando en estar sobre la SMA200, P(>0) = 9% (ventanas traslapadas, grado C). El filtro de tendencia **no bastó** desde el Merge, así que hacen falta condiciones de protocolo y de economía (capítulo 02, §8).
- (b) Peso de **10-20%**. ETH tiene una beta de 1.28 respecto a BTC y una volatilidad de 64%, y cayó 50% o más en 26.7% de las ventanas de 122 días desde 2017. Con 20%, un −50% cuesta 1,000 MXN; con 10%, 500 MXN. Eso deja margen para que BTC también caiga (correlación de 0.91) sin tocar el tope de 5,000 MXN ni los cortacircuitos. Además hay que exigir salida si ETH/BTC cierra bajo su SMA200 y cuatro votos del comité con confianza de al menos 60.
- (c) 36,000,000/21,000 = **1,714**; 1,428 corresponde a 30 M. Con 60 M caben 2,857. Subir el límite aumenta la oferta de espacio de bloque. Si la demanda no crece igual, el uso queda debajo del objetivo, la base fee baja y la quema cae. Con PBS, los validadores incluso prefieren subir el límite para cobrar propinas en vez de quemar (argumento de Prestwich). Hoy: límite de 60 M, uso de ~50% y base fee de ~0.12 gwei.

**Fuente.** Datos diarios de Binance (cálculo propio); *Mastering Ethereum*, cap. 14; decisión del comité del 25-sep-2026; capítulo 02, §5, §6 y §8.

**Rúbrica.** (a) 4 pts; (b) 3 pts, con cálculo y regla de salida; (c) 3 pts.
