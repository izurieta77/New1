# 06 · Podcasts, pruebas de conocimiento cero y rutas de desarrollo (grupo G6)

> **Nivel:** licenciatura → maestría aplicada · **Actualizado:** 25-sep-2026 por `analista-cripto` · **Grado de evidencia global: C.**
> - **A** en la criptografía de las pruebas ZK (MOOC de Berkeley).
> - **B** en el contenido de las rutas de desarrollo (fuentes primarias de su propio temario).
> - **B-** en los hechos noticiosos que traen los podcasts, que hubo que verificar uno por uno.
> - **D** en sus tesis de mercado: no tienen historial auditado y sí conflictos materiales.
> - El libro de Ben-Sasson es **C**: el relato de una empresa contado por su CEO.
>
> **Regla de uso:** nada de este capítulo autoriza una operación. La cuenta Binance es solo spot y hoy solo tiene BTC. Este material sirve para filtrar narrativas, medir riesgo técnico y registrar pronósticos verificables.

## 0. Fichas del grupo y acceso real

| # | Recurso | Ficha | Acceso real | Grado |
|---|---|---|---|---|
| 02 | Bankless (podcast) | [02-bankless.md](recursos/02-bankless.md) | Sección: 26 notas de episodio (ago-sep 2026), 4 transcripciones públicas (cortadas hacia el minuto 50-60) y la hoja pública de divulgaciones. | D en tesis; B- en hechos |
| 09 | The Chopping Block (Unchained) | [09-the-chopping-block.md](recursos/09-the-chopping-block.md) | Íntegro en 5 episodios: 4 de ago-sep 2026 y el de FTX (9-nov-2022). La transcripción oficial es Premium, así que transcribí yo el audio público. | C- (D en pronósticos) |
| 18 | Zero Knowledge Proofs MOOC (UC Berkeley RDI, 2023) | [18-zero-knowledge-proofs-mooc.md](recursos/18-zero-knowledge-proofs-mooc.md) | Sección: temario y diapositivas de 13 clases, sin videos. | A técnico; C para invertir |
| 31 | *Zero Knowledge, Infinite Trust* (Ben-Sasson y Jeffay, 2026) | [31-zero-knowledge-infinite-trust.md](recursos/31-zero-knowledge-infinite-trust.md) | **Resumen**: capítulo 1, índice general e índice analítico gratuitos de Wiley, más el sitio, una reseña y prensa. | C |
| 10 | Speedrun Ethereum | [10-speedrun-ethereum.md](recursos/10-speedrun-ethereum.md) | Sección: temario y README de los repositorios. | B / C |
| 13 | Alchemy University: Ethereum Developer Bootcamp | [13-alchemy-university-ethereum-developer-bootcamp.md](recursos/13-alchemy-university-ethereum-developer-bootcamp.md) | Sección: temario y dos repositorios de proyectos. | B / C |
| 14 | Curso de 32 h de Patrick Collins (freeCodeCamp) | [14-learn-blockchain-solidity-full-stack-web3.md](recursos/14-learn-blockchain-solidity-full-stack-web3.md) | Sección: README e índice de capítulos, sin video (yt-dlp y YouTube bloqueados). | B / C |
| 19 | ETH Kipu: Ethereum Developer Pack | [19-eth-kipu-ethereum-developer-pack.md](recursos/19-eth-kipu-ethereum-developer-pack.md) | Sección amplia: estructura de los 2 niveles y clases de seguridad, auditoría, verificación y L2. | B / C |

## 1. Mapa del tema

El grupo junta tres cosas distintas que se tocan en un punto: **cómo se forma la narrativa, en qué tecnología se apoya y cómo se verifica.**

```
          NARRATIVA (qué se dice)                 VERIFICACIÓN (cómo se comprueba)
   ┌──────────────────────────────────┐      ┌──────────────────────────────────────┐
   │ Bankless (02): tesis pro-ETH,    │      │ Rutas de desarrollo (10,13,14,19):   │
   │ minorista, patrocinios           │─────▶│ leer contratos, exploradores,        │
   │ Chopping Block (09): VCs y       │      │ auditorías, L2BEAT, riesgos de       │
   │ fundadores que debaten           │      │ proxies, oráculos y liquidaciones    │
   └──────────────┬───────────────────┘      └───────────────┬──────────────────────┘
                  │ hablan de L2, privacidad,                │ enseñan que "auditado"
                  │ tokenización, poscuántico                │ y "ZK" no son garantía
                  ▼                                          ▼
          TECNOLOGÍA (qué hay debajo)
   ┌───────────────────────────────────────────────────────────────────────┐
   │ Pruebas ZK (18, 31): SNARK = IOP + compromiso polinomial.             │
   │  - KZG/Groth16: pruebas mínimas, configuración confiable, no poscuánt.│
   │  - FRI/STARK: transparentes, plausiblemente poscuánticas, grandes.    │
   │ Usos: escalar (rollups, sin privacidad) y privacidad (Zcash, Aztec).  │
   └───────────────────────────────────────────────────────────────────────┘
```

- **Los podcasts** fijan la agenda: de qué se habla y qué activos "están de moda".
- **ZK** es la tecnología detrás de dos narrativas grandes de 2026: escalar Ethereum con rollups y la ola de privacidad (ZEC y NEAR como "privacy trade").
- **Las rutas de desarrollo** no hacen programador al dueño en un mes. Sí le dan el vocabulario y la destreza para **verificar**: leer un contrato en Etherscan, detectar un *proxy* con *admin* peligroso, entender por qué una auditoría no basta y medir el riesgo de una L2 en L2BEAT.

## 2. Cómo usar los podcasts sin contagiarse de narrativa (reglas)

Estas reglas salen de lo que encontré en 5 episodios de The Chopping Block y 4 de Bankless.

- **R1. Mirar primero quién paga y quién tiene posición.**
  - Bankless publica una hoja con patrocinadores, tenencias e inversiones. NEAR, Venice y The DeFi Report son patrocinadores y aparecen elogiados o citados como "confirmación" en los mismos episodios.
  - Los anfitriones de The Chopping Block dicen al aire que son "early-stage investors". El 28-ago-2026 declararon: "Lighter, in which we are all investors. We're investors in HYPE as well".
  - Si el activo mencionado está en la lista de conflictos, la mención vale cero como señal.
- **R2. Separar hechos de tesis y verificar cada cifra en la fuente primaria antes de anotarla.** En solo 8 semanas encontré estos errores:
  - **CLARITY:** The Chopping Block dijo 47 votos. El Senado registra **49-50** (votación 234, 15-sep-2026).
  - **Coldcard:** se dijo "$100M" y "$130M". TRM Labs y Galaxy Research cuentan **~1,816 BTC ≈ US$116 M**.
  - **Fed:** "first hike since 2022". Fue la primera en más de tres años; la anterior fue de 2023.
  - **Exención de innovación de la SEC:** Bankless citó solo el tope de 0.25%. Existe también un nivel 2 con 2.5% y 250 símbolos.
- **R3. Convertir las tesis en pronósticos con fecha y umbral y registrarlos.** Anotarlos en `bitacora/pronosticos.csv` con autor externo y resolverlos. Ejemplos abiertos:
  - "Muy improbable que BTC baje de 60 mil este año" (Haseeb Qureshi en Bankless, 28-ago-2026).
  - "No habrá cambios de emisión en ETH; EIP-8363 tiene menos de 5% de probabilidad" (Ryan Sean Adams, 7-ago-2026).
  - "S&P 500 arriba de 8,200 al cierre de 2026" (Tom Lee, citado el 18-sep-2026).
  - Sin historial auditado, la tesis es D.
- **R4. La narrativa sigue al precio: úsala como termómetro contrario.**
  - El 7-ago-2026, con BTC en US$64.9 k, Bankless decía que el ciclo "no se ve terminado" y que podía faltar medio año.
  - El 6-ago, en The Chopping Block, Haseeb decía que "retail is genuinely not here" y que la volatilidad tardaría "9, 12, maybe 18 months" en volver.
  - Tres semanas después (28-ago), Haseeb ya hablaba en Bankless de reflexividad y de vendedores agotados. A las siete semanas, con BTC en US$83.9 k (+29%), Bankless hablaba de "early bull".
  - Cuando todos los analistas de ciclo coinciden ("85% probability"), hasta el anfitrión admite que eso "raise[s] an eyebrow".
- **R5. Enfriamiento de 48 horas.** Ninguna idea escuchada en un podcast llega al comité antes de 48 horas, y nunca sin fuente primaria ni sin pasar por `gestor-de-riesgo`.
- **R6. Contrastar siempre dos podcasts y una fuente primaria.** The Chopping Block y Bankless se contradicen en cifras y en tesis (§6). La contradicción es información.
- **R7. Desconfiar de la palabra "insider".** El incentivo del *insider* es el valor de su portafolio, no el rendimiento del oyente.
  - Dragonfly, la firma de Haseeb y Tom, levantó un cuarto fondo de US$650 M en feb-2026 con la tesis de que "non-financial crypto has failed". Su enfoque son stablecoins, DeFi y mercados de predicción, justo los temas que más elogian.
- **R8. Para qué sí sirven:**
  1. agenda de investigación semanal;
  2. explicación de mecanismos, como el emparejamiento de *memecoins* con acciones tokenizadas o el MEV en *routers* de inferencia;
  3. debates internos de protocolos que cambian el riesgo del activo (EIP-8363);
  4. pulso regulatorio (CLARITY, exención de innovación, Regulation Crypto Assets).
  Para lo que no sirven: *timing* y selección de activos.
- **R9. Regla específica de la cuenta actual** (solo BTC spot):
  - Las rotaciones que proponen los podcasts ("this is not Bitcoin's cycle", ZEC, NEAR, HYPE, *tokens* con ingresos) no generan operaciones.
  - Como mucho, generan un escenario de riesgo para BTC, que se contrasta con flujos de ETFs y datos en cadena (G5).

## 3. ZK para inversionistas

### 3.1 Qué es y para qué se usa

Una prueba ZK demuestra que un cálculo es correcto sin revelar los datos. En blockchain tiene **dos usos distintos** (MOOC, clase 2):

1. **Escalar o verificar cómputo** (zkRollups, zkBridges, zkEVM). Aquí no hace falta conocimiento cero, solo **sucintez**: la L1 verifica rápido y barato un lote que costó mucho calcular. Los datos se publican.
2. **Privacidad:** Zcash, Tornado Cash, Aztec, pruebas de solvencia de un exchange sin revelar cuentas.

"ZK" en un folleto no dice cuál de los dos es. Casi siempre es el primero.

### 3.2 Las familias y lo que cuestan

MOOC, clases 5 y 8:

| Sistema | Configuración | Tamaño de prueba | ¿Poscuántico? | Dónde aparece |
|---|---|---|---|---|
| Groth16 | Confiable **por circuito** | El más corto (3 elementos de grupo) | No | El MOOC no da ejemplos de despliegue; no lo verifiqué en esta sesión |
| PLONK + KZG | Confiable **universal** (ceremonia) | ~4-6 veces Groth16 | No | Aztec, JellyFish |
| PLONK/Halo2 + IPA | Transparente | Corto, pero verificador lento | No | Halo2 (Zcash) |
| STARK (IOP + FRI) | Transparente | Grande: "cientos de KB" | Plausiblemente sí | StarkWare/Starknet, Plonky2 |

- **La regla que ordena la tabla:** "la transparencia y la seguridad poscuántica las determina por completo el esquema de compromiso" (clase 8).
- **La otra regla:** la seguridad de FRI se analiza en la mayoría de los despliegues bajo una **conjetura**. En versión no interactiva, λ bits de seguridad se rompen con probabilidad 2^(k−λ) si el atacante hace 2^k hashes.
- **Ejercicio verificado (ficha 18):** con un año del hashrate actual de Bitcoin (918 EH/s ≈ 2^94.5 hashes), un sistema de 80 bits cae casi seguro, uno de 100 bits con ~2% y uno de 128 bits de forma despreciable.

### 3.3 Lista de preguntas antes de invertir en algo "ZK"

1. ¿Es escalabilidad o privacidad? Si es privacidad, ¿qué riesgo regulatorio carga? El MOOC cita Tornado Cash solo como ejemplo técnico de transacciones privadas; su historia regulatoria no la verifiqué en esta sesión.
2. ¿Qué sistema de pruebas y qué compromiso usa? ¿Hubo ceremonia de configuración confiable?
3. ¿Cuántos bits de seguridad declara y bajo qué conjetura?
4. ¿Quién puede **actualizar** el verificador o el puente, y hay *timelock*? (L2BEAT; fichas 14 y 19)
5. ¿El secuenciador está centralizado? ¿Cuánto tarda un retiro forzado a L1? (actividad de L2BEAT de ETH Kipu)
6. ¿Qué fracción del valor que genera la red llega al tenedor del *token*?

### 3.4 Lo que el inversionista suele entender mal

- **"Buena tecnología = buen *token*".** Es falso.
  - STRK (Starknet, la red de StarkWare, "empresa de US$8,000 M" según el libro 31) cotiza a **US$0.040**, **−99.1%** contra su máximo del 20-feb-2024 (CoinGecko, 25-sep-2026).
  - La valuación de US$8,000 M es una ronda privada de 2022, no un precio.
- **"STARK = poscuántico".** Es solo en parte. Las pruebas lo son (hashes), pero StarkWare admite que las firmas de cuentas de Starknet y el puente y los *blobs* de Ethereum todavía no (The Quantum Insider, 30-jun-2026).
  - Para BTC, la exposición cuántica relevante está en las firmas (ECDSA/Schnorr), no en la prueba de trabajo. Esto es inferencia mía, no verificada en esta sesión; corresponde a G1.
- **"Privacidad = narrativa ganadora".** En 2026, ZEC llegó a US$26,000 M de capitalización (US$1,534, CoinGecko 25-sep-2026). Bankless lo presenta como el nuevo aspirante a reserva de valor. Es una rotación narrativa sin historial auditado y con riesgo regulatorio propio.
- **"Una prueba ZK elimina el riesgo".** No. Los circuitos pueden tener bugs (clase 14, verificación formal), y el riesgo operativo (llaves de actualización, secuenciador) suele ser mayor que el criptográfico.

## 4. Qué ruta de desarrollo seguir si el dueño quisiera aprender a programar

**Objetivo realista para un inversionista:** no escribir protocolos, sino **leer y verificar**. La ruta tiene dos salidas.

### Ruta A: "inversionista que verifica" (sin volverse programador)

1. **ETH Kipu, nivel 1 completo** (ficha 19). Está en español, cubre blockchain, *wallets* y gas, L2 con la actividad de L2BEAT y la exploración de *bytecode* en Etherscan.
2. **ETH Kipu, nivel 2, solo las clases 11, 16 y 17:** verificación y depuración, vectores de ataque, y auditoría con la lista de verificación antes de desplegar.
3. **Curso de Collins (ficha 14):** usar solo el índice como mapa y ver la lección 16 (contratos actualizables) y la 18 (seguridad).
4. **Práctica semanal:** revisar en Etherscan 1 contrato de un protocolo mencionado en los podcasts con la lista de la ficha 14, §4: código verificado, *proxy*, *admin* y *timelock*, `owner()`, eventos.

### Ruta B: "aprender a programar contratos"

1. **Si no programa en JavaScript:** "Learn JavaScript" de Alchemy University (49 lecciones, ficha 13).
2. **Base conceptual:** ETH Kipu nivel 1 más la sección de criptografía del Bootcamp de Alchemy (hashes, firmas, Merkle).
3. **Aprender construyendo:** Speedrun Ethereum, retos 0 a 7 (ficha 10): NFT, *crowdfunding*, ERC-20, aleatoriedad, DEX, oráculos, préstamos y stablecoin.
4. **Profesionalizar:** ETH Kipu nivel 2 completo (Foundry, *fuzzing*, Slither, Tenderly).
5. **Herramientas actuales:** Cyfrin Updraft, recurso 22 de otro grupo, que el propio repositorio de Collins recomienda en lugar de su video de 2022 con Hardhat. El video de 32 h queda solo como referencia.

**Por qué este orden:**

- ETH Kipu está en español y es el más cercano a lo que usa un inversionista (exploradores, auditorías, L2).
- Speedrun obliga a construir los mecanismos donde más dinero se pierde (oráculos, liquidaciones, aleatoriedad).
- El curso de Collins está desactualizado por declaración de su autor.
- Alchemy enseña con su propia infraestructura (AlchemySDK), lo que es aceptable pero hay que saberlo.

**Límite:** no verifiqué la duración real de las rutas de Kipu, Alchemy y Speedrun. Ninguna la publica de forma confiable, así que no doy estimados de horas.

## 5. Las 10 ideas que más importan para invertir

1. **Los podcasts cripto son *sell-side*.** Sus anfitriones tienen posiciones, fondos y patrocinadores declarados. Lo que dicen de un activo vale como agenda, no como señal (grado D).
2. **Toda cifra de podcast se verifica en la fuente primaria.** En 8 semanas aparecieron errores en votos del Senado, montos de hackeos y fechas de la Fed.
3. **La narrativa sigue al precio.** El mismo programa pasó de "el ciclo no ha terminado" a "early bull market" en siete semanas y con un alza de 29%. El consenso de los expertos en ciclos es un dato de sentimiento, no una predicción.
4. **Las grandes tesis de los podcasts se prueban con el tiempo y conviene medirlas.**
   - "Ultra Sound Money" (Bankless, 2021-2022): la oferta de ETH bajó hasta abril de 2024 y hoy está **+1.29%** sobre The Merge.
   - ETH/BTC cayó **57.6%** desde el ROLLUP "ETH Goes Ultra Sound" (11-nov-2022).
5. **Recuperación en dólares no es recuperación en cripto.**
   - El 98% de los acreedores de FTX recibe ~119% de su reclamo, pero valuado al precio del 11-nov-2022 (BTC a US$16,871).
   - Un reclamo de 1 BTC vale hoy ~24% de un BTC (ficha 09).
   - La custodia en un exchange es riesgo de contraparte, no "tener bitcoin".
6. **Autocustodia no es automáticamente segura.** Coldcard: ~1,816 BTC drenados porque un firmware de 2021 generó semillas con entropía débil (de 128 a unos 40 bits). La calidad del proveedor de hardware importa tanto como "no tus llaves, no tus monedas".
7. **"Auditado" es un piso, no un techo.** Una auditoría no protege contra cambios futuros, dependencias ni errores operativos (ETH Kipu, clase 17). En un contrato actualizable, lo que manda es quién tiene la llave de *admin* y si hay *timelock*. El 17-sep-2026 S&P Global anunció la compra de OpenZeppelin: la auditoría se institucionaliza, pero no elimina el riesgo.
8. **ZK es infraestructura, no activo.** Escalar no es privacidad, "poscuántico" se juzga en el sistema completo y la calidad técnica no garantiza valor para el *token* (STRK −99%).
9. **La regulación de EUA avanza por la vía de las agencias, no del Congreso.**
   - CLARITY cayó 49-50 (15-sep-2026).
   - La SEC dio una exención de 5 años para acciones tokenizadas en AMMs, con topes de 0.25% y 2.5% del volumen.
   - La SEC propuso Regulation Crypto Assets: US$5 M una vez cada 4 años y US$75 M por año con estados financieros; comentarios hasta el 20-oct-2026.
   - Lo que hace una agencia lo puede revertir la siguiente administración. Hay que descontar ese riesgo político.
10. **El dinero del minorista migra a donde está la volatilidad.** En Robinhood (2T-2026), los contratos de eventos (US$156 M) ya superan a acciones (US$129 M) y cripto (US$100 M, −38% anual). The Chopping Block (6-ago) sostuvo que los institucionales amortiguaron la volatilidad de cripto y que el minorista se fue. Es una hipótesis: quién es el comprador marginal de BTC se mide con flujos de ETFs y datos en cadena (G5), no con podcasts.

## 6. Contradicciones entre recursos

| Tema | Fuente A | Fuente B | Qué verifiqué y quién tiene razón |
|---|---|---|---|
| Votos de CLARITY (15-sep-2026) | Chopping Block: "It got 47" | Bankless: "11 votes short" de 60 | Senado, votación 234: **49 sí, 50 no**. Bankless tiene razón. National Law Review lo invirtió (50-49). |
| Monto del *hack* de Coldcard | Chopping Block (6-ago): "almost $100 million" | Bankless (7-ago): "$130M" | TRM Labs (5-ago) con el conteo de Galaxy: **~1,816 BTC ≈ US$116 M**. Ninguno exacto: el conteo creció por oleadas. |
| Fondo de Aschenbrenner (Situational Awareness) en su máximo | Chopping Block: ~US$45,000 M | Bankless: "$20 to $30 billion" | **No lo verifiqué**; no lo uso. |
| Fecha de EIP-8363 | Bankless: "On August 4th… proposed" | Archivo del EIP: `created: 2026-07-14` | Ambas pueden ser ciertas (borrador y difusión pública). Para citar, uso la del archivo. |
| Calidad de EIP-8363 | Chopping Block (un anfitrión): "reads like shit… Solana proposals better researched" | Bankless (David): "technical purity… good in a vacuum" | Opiniones (O). Coinciden en que no pasará. Sigue en **Draft** al 25-sep-2026. |
| STARK contra SNARK | Libro 31 (según la reseña): la configuración de los SNARKs "puede ser fuente de problemas"; los STARKs "pueden ser más eficientes" | MOOC 18: STARKs transparentes pero con pruebas de "cientos de KB"; seguridad de FRI bajo conjetura; Groth16, las pruebas más cortas | Es un intercambio de ventajas, no una superioridad. El MOOC es la fuente neutral. |
| Inmutabilidad | Libro 31, cap. 1: "they simply can't" cambiar lo escrito | EIP-8363 cita la bifurcación de The DAO (EIP-779) como precedente de que la capa social anula reglas | El libro exagera. La inmutabilidad es social y económica, no absoluta. |
| Cronología de StarkEx | Sitio del libro 31: "2019 StarkEx Goes Live… dYdX migrates" | Documentación de StarkWare: en red principal desde **jun-2020**; dYdX desde **abr-2021** | Manda la documentación. El sitio promocional comprime la historia. |
| Régimen de mercado (ago-2026) | Chopping Block (6-ago, Haseeb): "retail is genuinely not here"; 9-18 meses para que vuelva la volatilidad | Bankless (21-ago): "Is the Bull Market Back?"; (18-sep) "earliest innings" | BTC: US$64.9 k (7-ago) → US$83.9 k (25-sep). Haseeb cambió a "reflexivity breeds reflexivity" el 28-ago (en Bankless). Ambos siguen al precio. |
| Acciones tokenizadas | Bankless (David): las *offshore* sin KYC son mejores; las permitidas por la SEC son "strictly an inferior product" | Chopping Block (Robert Leshner, CEO de Superstate, empresa de tokenización): el fracaso de CLARITY "changes nothing for tokenization"; Haseeb (en Bankless): los *tokens* de acciones "not that big of a deal", hay más demanda de derivados | Opiniones con conflicto (Superstate; $HOOD en tenencias de David). Dato: la exención de la SEC limita el volumen (0.25% o 2.5%), así que en el corto plazo pesa más lo *offshore*. |
| Cifras de Alchemy University | Cabecera: "91 lessons" | Temario: "96 lessons, 14 videos" (las secciones suman 96 lecciones y 8 videos) | Inconsistencia interna de marketing. |
| Duración del curso de Collins | freeCodeCamp: "30-hour course" (texto) | Título: "32-Hour Course"; Chainlink: "30+ hour" | Según el índice, la lección 18 empieza a las 31:28:32. "~32 h" es lo correcto. |

## 7. Qué hacer con esto en el sistema

- **Pronósticos externos a registrar como práctica** (autor externo, no del comité):
  - BTC no toca menos de US$60,000 (mínimo diario en Coinbase) entre el 28-ago y el 31-dic-2026. Operacionaliza el "very unlikely that we tread below 60 this year" de Haseeb (28-ago-2026).
  - EIP-8363 sin activarse en la red principal al 31-dic-2026 (Ryan Sean Adams, 7-ago-2026).
  - S&P 500 > 8,200 al 31-dic-2026 (Tom Lee, citado el 18-sep-2026).
- **Vigilancia de riesgo para BTC** (no son órdenes):
  - la narrativa "this is not Bitcoin's cycle" y la rotación hacia ZEC y NEAR;
  - la recuperación de la media de 50 semanas (≈ US$78.1 k al 25-sep-2026, cálculo propio con cierres de Coinbase);
  - el mínimo anual de US$57.7 k (1-jul-2026).
- **Custodia:** antes de cualquier retiro de BTC de Binance a autocustodia, revisar la lección de Coldcard. Qué *hardware* se usa, qué firmware y cómo se generó la semilla.

### Fuentes principales (detalle en cada ficha)

- **Senado de EUA**, votación 234 del 119.º Congreso, 2.ª sesión (15-sep-2026).
- **SEC:** comunicados 2026-90 (exención de innovación, 17-sep-2026) y 2026-76 (Regulation Crypto Assets, 18-ago-2026).
- **Fed**, nota de implementación del 16-sep-2026.
- **S&P Global**, comunicado del 17-sep-2026.
- **TRM Labs**, 5-ago-2026 (Coldcard).
- **Robinhood**, resultados del 2T-2026 (29-jul-2026).
- **CoinDesk**, 17-feb-2026 (Dragonfly).
- **ultrasound.money** (oferta de ETH).
- **Precios:** Coinbase, Kraken y CoinGecko (25-sep-2026).
- **FTX:** comunicado de confirmación del plan (7-oct-2024) y *Digital Assets Conversion Table* (reportada por Bitcoin.com y Cointelegraph).
- **Material del grupo:** MOOC de UC Berkeley RDI; extractos de Wiley del libro 31; repositorios y sitios de las rutas 10, 13, 14 y 19.
