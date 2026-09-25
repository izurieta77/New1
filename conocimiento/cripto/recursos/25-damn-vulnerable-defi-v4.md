# 25 · Damn Vulnerable DeFi v4 (The Red Guild)

- **Estado:** estudiado. **Acceso:** íntegro para los enunciados y el código de los 18 retos. No ejecuté las soluciones.
- **Grupo:** G4. **Autor de la ficha:** `analista-cripto`, 25-sep-2026.
- **Etiquetas:** [H] hecho con fuente (aquí, casi siempre el código del repositorio) · [I] inferencia · [O] opinión.

## 1. Ficha

| Campo | Valor |
|---|---|
| Año | 2024. La v4.0.0 salió el 16-jul-2024 y la v4.1.0 el 21-mar-2025. La v1.0.0 es del 21-sep-2020. Fechas tomadas de las etiquetas de git. |
| Autor | The Red Guild. El proyecto lo creó Martín Abbatemarco ("tinchoabbate"), autor del commit v1.0.0. |
| Tipo | Retos de seguridad tipo CTF en Solidity 0.8.25 con Foundry |
| Nivel | Avanzado |
| Costo | Gratis. Licencia MIT (©2021 Damn Vulnerable DeFi). |
| Idioma | Inglés |
| URL | https://www.damnvulnerabledefi.xyz/ · https://github.com/theredguild/damn-vulnerable-defi |
| Conflictos de interés | Bajos. Es material educativo abierto. Los retos integran librerías reales (Safe, Uniswap v1/v2/v3, Curve, Permit2), así que **los fallos están en los contratos del reto, no en esas librerías**. |

## 2. Acceso real (25-sep-2026)

**Cómo lo obtuve:**
- `git clone --depth 1` en el scratchpad (`g4/damn-vulnerable-defi`), en el commit `64fddf9` (v4.1.0, 21-mar-2025);
- consulté las etiquetas con `git ls-remote` y `git fetch --depth 1` para fechar las versiones.

**Qué leí:**
- el README y el CHANGELOG;
- los **18 enunciados** (`src/*/README.md`);
- las **funciones vulnerables de cada reto**, identificadas en el código (fragmentos en la tabla);
- la página oficial, que confirma el orden 1-18 y la versión v4.1.0.

**Qué no hice:**
- no compilé ni ejecuté las soluciones: Foundry no está instalado y dos retos requieren una bifurcación de mainnet con RPC;
- **la clase de vulnerabilidad sale de leer el código, no de haber probado el exploit.**

**Nivel: íntegro** (enunciados y código).

## 3. Lo esencial

### 3.1 Los 18 retos y la clase de vulnerabilidad que enseñan

Todos los fragmentos de código están verificados en el repositorio. La columna de caso real es una **analogía mía [I]** con su fuente.

| # | Reto | Clase de vulnerabilidad | Qué falla en el código | Caso real análogo [I] |
|---|---|---|---|---|
| 1 | Unstoppable | **Denegación de servicio** por un invariante contable estricto | `flashLoan` revierte si `convertToShares(totalSupply) != totalAssets()`. Una transferencia directa de tokens al vault rompe la igualdad y lo apaga. | Un protocolo puede quedar inservible sin que nadie robe nada |
| 2 | Naive Receiver | **Callbacks sin control de acceso** más **suplantación del remitente** en metatransacciones (ERC-2771 + multicall) | El receptor no verifica quién inició el préstamo y paga 1 WETH de comisión cada vez. `_msgSender()` toma los últimos 20 bytes del calldata cuando llama el forwarder, y el multicall con `delegatecall` permite anexar la dirección de otro depositante. | Permisos delegados mal acotados |
| 3 | Truster | **Llamada externa arbitraria** | `flashLoan` ejecuta `target.functionCall(data)` con datos del usuario, lo que permite que el pool se apruebe tokens a sí mismo a favor del atacante | — |
| 4 | Side Entrance | **Contabilidad inconsistente** y reentrada entre funciones | La devolución se verifica con `address(this).balance`. Depositar el ETH prestado "cuenta" como pago y además acredita saldo al atacante. | — |
| 5 | The Rewarder | **Error lógico en reclamos por lote** (doble reclamo) | `_setClaimed` solo se evalúa al cambiar de token o en el último elemento, así que repetir el mismo reclamo dentro del lote paga varias veces | — |
| 6 | Selfie | **Gobernanza tomada con préstamo relámpago** | `_hasEnoughVotes` usa `getVotes` del momento (>50% del supply). Préstamo, `delegate`, `queueAction(emergencyExit)`. | **Beanstalk**, 17-abr-2022: ~US$182 millones con votos prestados ([CoinDesk](https://www.coindesk.com/tech/2022/04/17/attacker-drains-182m-from-beanstalk-stablecoin-protocol)) |
| 7 | Compromised | **Llaves privadas filtradas** de 2 de 3 reportadores de un oráculo, con lo que se controla la mediana | La respuesta de un servidor web contiene las llaves codificadas (hex, luego base64, luego llave privada; lo comprobé decodificando el primer bloque) | **Ronin**, mar-2022: 5 de 9 llaves de validadores, ~US$625 millones ([post-mortem](https://roninchain.com/blog/posts/back-to-building-ronin-security-breach-6513cc78a5edc1001b03c364)) |
| 8 | Puppet | **Oráculo de precio spot** en un pool con poca liquidez | Precio = saldo de ETH / saldo de DVT del par de Uniswap v1, con solo 10 ETH y 10 DVT | **Mango Markets** (oct-2022, ~US$110 millones de ganancia del atacante). **Las condenas penales se anularon el 23-may-2025**: el juez invocó la sede judicial y pruebas insuficientes de falsedad ([TRM Labs](https://www.trmlabs.com/resources/blog/breaking-federal-judge-overturns-all-criminal-convictions-in-mango-markets-case-against-avraham-eisenberg)) |
| 9 | Puppet V2 | Igual que Puppet, con reservas de Uniswap v2 y "las librerías recomendadas" | `UniswapV2Library.quote` sobre las reservas del momento | Como el anterior |
| 10 | Free Rider | **Reutilización de `msg.value` en un bucle** y **pago a la parte equivocada**; se financia con un flash swap | `_buyOne` compara `msg.value` con el precio de cada NFT, no con la suma. Paga al dueño *después* de transferir, es decir, al comprador. | Caso del `batch` de Sushi: `delegatecall` más `msg.value` (estudio de caso de Cyfrin, ficha 22) |
| 11 | Backdoor | **Inicialización insegura**: módulo con `delegatecall` en el `setup` de una Safe | El registro valida el selector, el umbral, los dueños y el fallback, pero **no los parámetros `to` y `data`** del `setup` | — |
| 12 | Climber | **Validar después de ejecutar**, más mejora UUPS | `execute()` hace las llamadas y *después* verifica que la operación estaba programada. El atacante se da el rol de proponente, pone el retraso en 0, programa su propia operación y mejora el vault. | Los timelocks solo protegen si el orden de las comprobaciones es correcto |
| 13 | Wallet Mining | **Colisión de almacenamiento** en un proxy (reinicialización) y **dirección CREATE2 precomputable** | La variable `upgrader` del proxy ocupa el slot 0, el mismo de `needsInit` en la implementación, y `init()` se puede volver a llamar. El nonce de la Safe de la usuaria se puede buscar. | **Parity** (nov-2017): una librería sin inicializar se "mató" y congeló cientos de millones en ETH ([TechCrunch](https://techcrunch.com/2017/11/07/a-major-vulnerability-has-frozen-hundreds-of-millions-of-dollars-of-ethereum)) |
| 14 | Puppet V3 | **TWAP corto** en un pool delgado | `TWAP_PERIOD = 10 minutes` sobre un pool de Uniswap v3 con 100 WETH y 100 DVT | **Drift** (1-abr-2026): colateral falso con precio fabricado en un pool de ~US$500 ([Chainalysis](https://www.chainalysis.com/blog/lessons-from-the-drift-hack/)) |
| 15 | ABI Smuggling | **Autorización que lee el selector en una posición fija** del calldata | `calldataOffset = 4 + 32*3`. El calldata dinámico puede validar `withdraw` y ejecutar `sweepFunds`. | **Bybit** (feb-2025): lo que los firmantes aprobaron no era lo que se ejecutó; un `delegatecall` cambió la implementación ([Sygnia](https://www.sygnia.co/blog/sygnia-investigation-bybit-hack/)) |
| 16 | Shards | **Redondeo inconsistente** | `fill` cobra `mulDivDown(...)`, que puede dar 0 con compras chicas; `cancel` reembolsa con `mulDivUp(shards, rate, 1e6)`, otra fórmula. La ventana de cancelación está mal escrita. | — |
| 17 | Curvy Puppet | **Reentrada de solo lectura** en el precio de LP de Curve | El precio usa `curvePool.get_virtual_price()`, manipulable durante `remove_liquidity` | Cyfrin lista la reentrada, incluida la de solo lectura, entre los vectores de 2023 (ficha 22) |
| 18 | Withdrawal | **Validación de mensajes de un puente** con operador privilegiado; **llamadas fallidas que se dan por finalizadas** | El operador finaliza sin prueba Merkle. `finalizedWithdrawals[leaf] = true` va antes de la llamada y no se revisa `success`. | **KelpDAO** (18-abr-2026): un solo verificador aceptó una quema inexistente, ~US$292 millones ([Chainalysis](https://www.chainalysis.com/blog/kelpdao-bridge-exploit-april-2026/)) |

### 3.2 Lo que enseña el conjunto

1. [H] **18 retos** en v4. La v4 migró de Hardhat a Foundry y a solc 0.8.25, y **añadió Withdrawal, Curvy Puppet y Shards** (CHANGELOG).
2. [H] **Desde la v4**, cada reto exige depositar lo "rescatado" en una cuenta de recuperación: el enfoque es de rescate de sombrero blanco (CHANGELOG).
3. [I] **Frecuencia de temas** (conteo propio):
   - **5 retos giran en torno a precios u oráculos:** Compromised, Puppet, Puppet V2, Puppet V3 y Curvy Puppet;
   - **6 usan préstamos relámpago o flash swaps:** Unstoppable, Naive Receiver, Truster, Side Entrance, Selfie y Free Rider;
   - **5 tocan gobernanza, actualización o permisos:** Selfie, Backdoor, Climber, Wallet Mining y ABI Smuggling;
   - **3 son de contabilidad o matemática:** Side Entrance, The Rewarder y Shards;
   - **1 es de puente:** Withdrawal.
4. [I] **Lección central:** casi todos los fallos son **supuestos implícitos** que el código no verifica:
   - "el saldo solo cambia por mis funciones" (Unstoppable, Side Entrance);
   - "el precio del pool es el precio del mercado" (serie Puppet);
   - "quien firma sabe lo que firma" (ABI Smuggling, Backdoor);
   - "el mensaje del otro lado es válido" (Withdrawal).
5. [I] **Un préstamo relámpago no es la vulnerabilidad:** es el **amplificador**. Da capital ilimitado por una transacción, así que cualquier supuesto que dependa del "capital del atacante" (votos, precio de un pool) deja de valer.
6. [H] **Solo 1 de 18 retos** (Compromised) es de **seguridad operativa**: llaves filtradas.
7. [I] En contraste, según Chainalysis, **el riesgo dominante de 2025 fue operativo**: llaves, firmas y personas en servicios centralizados (ficha 32). **DVDF entrena para leer código, no para evaluar la operación.**
8. [H] **Puppet V3 muestra que un TWAP no basta:** con 10 minutos y 100 WETH de liquidez el promedio también se manipula.
9. [H] **Withdrawal describe en miniatura el riesgo de un puente:**
   - un operador que puede saltarse la prueba;
   - un mensaje de retiro que vaciaría el puente;
   - un estado "finalizado" aunque la llamada falle.
10. [H] **Wallet Mining y Climber** muestran que los **contratos actualizables** son un vector propio. La actualización es una llave maestra y el orden de las comprobaciones importa.
11. [H] **ABI Smuggling** muestra que **lo que se valida puede no ser lo que se ejecuta**. Es la misma familia de problema que la firma a ciegas de Bybit, aunque allá el vector fue una interfaz web comprometida.
12. [I] **Para leer una auditoría de un proyecto**, estos 18 patrones sirven como lista mínima de preguntas:
    - ¿de dónde sale el precio?;
    - ¿quién puede actualizar y con qué retraso?;
    - ¿se valida cada mensaje entre cadenas?;
    - ¿hay redondeos a favor del usuario?;
    - ¿qué pasa si alguien manda tokens directo al contrato?

## 4. Qué cambia para invertir

### Riesgo de exchange (lección de FTX aplicada a Binance)
- [I] **DVDF no trata exchanges centralizados**, pero una lección se traslada directo: **el oráculo de precios del exchange**.
- [H] **Binance, 10-oct-2025:** Binance compensó ~US$283 millones a usuarios de futuros, margen y préstamos que usaban USDe, BNSOL o WBETH como colateral. Estos activos perdieron la paridad **en su propio mercado** durante una cascada ([The Block](https://www.theblock.co/post/374295/binance-pays-283-million-in-compensation-following-fridays-depegs-covering-user-losses); [CoinDesk](https://www.coindesk.com/markets/2025/10/12/binance-to-compensate-users-affected-by-crash-in-wbeth-bnsol-and-ethena-s-usde)).
  - Según la cobertura, USDe bajó de US$0.66 en Binance, y el exchange lo atribuyó a liquidez escasa, órdenes límite inactivas desde 2019 y errores de visualización.
  - [I] Valuar colateral con el precio de un mercado delgado es el patrón Puppet, ahora dentro de un exchange centralizado.
- [I] **Para la cuenta:** solo spot, sin apalancamiento ni colateral. Esta clase de riesgo nos afecta solo por reputación y por el mercado. **No usar Earn ni colaterales sintéticos.**

### Riesgo de stablecoin
- [I] Las stablecoins sintéticas o con colateral cripto dependen de **oráculos y de liquidación** (serie Puppet, Curvy Puppet). Heredan esta superficie de ataque. Las respaldadas por efectivo y bonos no, pero tienen el riesgo del emisor (ficha 17).

### Hackeos de exchanges y de puentes
- [H] **Withdrawal y KelpDAO:**
  - un puente es un invariante: **lo liberado debe ser igual a lo quemado o bloqueado**;
  - si la validación depende de un solo operador o verificador, el invariante depende de una sola llave o de un solo nodo.
- [I] **No mantener BTC envuelto o puenteado** en otras cadenas (por ejemplo, BTCB) sin necesidad. Suma el riesgo del puente o del custodio al del BTC.

### Autocustodia
- [I] **ABI Smuggling y Backdoor → firmar solo lo que se entiende**:
  - verificar en la pantalla del dispositivo el destino, el monto y la función;
  - en una multisig, revisar los módulos y los parámetros de `setup`.
  - Es la misma recomendación que da Cyfrin ("confía en tu cartera, no en el sitio"; ficha 22).

### Cómo leer una prueba de reservas
- [I] **Una PoR es un invariante tipo Withdrawal:** activos ≥ pasivos. Su valor depende de **quién alimenta los datos**.
  - KelpDAO cayó por nodos RPC envenenados.
  - Una PoR depende de qué carteras se incluyen y de qué pasivos se reportan.
  - **Preguntar siempre qué supuestos no se verifican.**

## 5. Contrapuntos y límites
- **Es un entrenamiento, no estadística:**
  - no dice qué tan frecuente es cada clase en la realidad;
  - los retos son simplificados y a propósito vulnerables.
- **Cubre poco lo operativo:** llaves, firmas, personas, proveedores. Según Chainalysis, eso concentró las pérdidas de 2025.
- **No ejecuté los exploits.** La clase de cada reto la inferí del código; los retos admiten "más de una solución" (README).
- **Mi conteo de temas** es una clasificación propia y discutible: varios retos caen en dos clases.
- **Relevancia directa para nuestra cuenta** (BTC spot): baja. Aporta criterio para juzgar protocolos, puentes y stablecoins que el comité no aprobaría hoy.

## 6. Autoexamen

**1. En Puppet, ¿por qué es explotable el oráculo y qué cambia en Puppet V3?**
- En Puppet el precio es el cociente de saldos de un par con solo 10 ETH y 10 DVT: vendiendo DVT al pool se hunde el precio y se piden prestados todos los DVT con poco colateral.
- En V3 se usa un TWAP de 10 minutos sobre 100 WETH y 100 DVT. Un promedio corto sobre poca liquidez también se manipula.
- Fuente: `src/puppet/PuppetPool.sol` y `src/puppet-v3/PuppetV3Pool.sol`.

**2. ¿Qué error de orden hay en Climber y por qué anula el timelock?**
- `execute()` hace las llamadas antes de verificar que la operación estaba "lista". Dentro de la misma ejecución, el atacante se da el rol de proponente, pone el retraso en 0 y programa su propia operación, que así pasa la verificación posterior.
- Fuente: `src/climber/ClimberTimelock.sol`, líneas 72-99.

**3. ¿Qué tienen en común el reto Withdrawal y el hackeo a KelpDAO?**
- En ambos, el lado de destino libera fondos confiando en una validación que un solo actor puede saltarse o falsear: el operador sin prueba Merkle en el reto; un único verificador alimentado por nodos RPC comprometidos en KelpDAO.
- El invariante "liberado = quemado" no se comprueba de forma independiente.
- Fuentes: `src/withdrawal/L1Gateway.sol`; Chainalysis (23-abr-2026).

**4. ¿Por qué el reto Compromised es el más cercano a las pérdidas reales de 2025?**
- Es el único de los 18 sobre seguridad operativa: llaves de 2 de 3 reportadores del oráculo filtradas en una respuesta web.
- En 2025, las pérdidas se concentraron en ataques a llaves y procesos de firma de servicios centralizados (88% en el 1T-2025; Bybit).
- Fuentes: `src/compromised/README.md`; Chainalysis (18-dic-2025).

## 7. Grado de evidencia: **A** (contenido técnico) / **C** (relevancia para invertir)
- **A:** el código es público y verificable. Cada clase de esta ficha se comprobó leyendo la función vulnerable.
- **C:** trasladarlo a decisiones de inversión es inferencia mía. DVDF no mide frecuencias ni pérdidas.
