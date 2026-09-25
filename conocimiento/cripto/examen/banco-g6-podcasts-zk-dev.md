# Banco de examen G6 · Podcasts, pruebas ZK y rutas de desarrollo

> **Autor:** `analista-cripto` · **Fecha:** 25-sep-2026 · **Capítulo:** [06-podcasts-zk-y-rutas-de-desarrollo.md](../06-podcasts-zk-y-rutas-de-desarrollo.md)
>
> **Cómo se califica.** Cada pregunta vale 10 puntos y exige cifras exactas con su fuente. La respuesta de referencia trae los elementos mínimos. Sin fuente primaria, la pregunta vale como máximo la mitad.

---

## P1. Verificar una cifra de podcast (10 pts)

El 17-sep-2026, The Chopping Block afirmó que la Ley CLARITY "got 47" votos. Un día después, Bankless dijo que quedó "11 votes short" de la supermayoría. Una revista jurídica publicó "50 yeas, 49 nays".

(a) ¿Cuál es el conteo correcto y qué fuente primaria lo resuelve?
(b) ¿Qué votación fue exactamente?
(c) ¿Qué regla operativa se deriva para la bitácora?

**Respuesta de referencia.**

- **(a)** **49 a favor y 50 en contra**, rechazada. Fuente primaria: la lista de votaciones nominales del Senado de EUA (119.º Congreso, 2.ª sesión), votación **234**.
- **(b)** Fue la moción de clausura sobre la moción para proceder con **H.R. 3633**, el 15-sep-2026. Se necesitaban 60 votos.
  - Bankless acierta: 60 − 49 = 11.
  - The Chopping Block se equivoca (47), igual que sus notas de episodio en Unchained.
  - La revista invirtió el resultado (50-49). CoinDesk confirma 49-50 y dice que ni siquiera alcanzó mayoría simple.
- **(c)** Ninguna cifra de podcast entra a la bitácora sin fuente primaria. Si dos fuentes secundarias discrepan, decide la primaria, aunque "todos" repitan otra cosa.

*Fuentes:* senate.gov (`vote_menu_119_2.htm`); CoinDesk, 15-sep-2026; fichas [02](../recursos/02-bankless.md) y [09](../recursos/09-the-chopping-block.md).

---

## P2. Conflictos de interés cruzados (10 pts)

Da **tres** conflictos documentados que restan neutralidad a Bankless cuando habla del debate de emisión de ETH (EIP-8363). Da **dos** que afectan a The Chopping Block cuando habla de Hyperliquid, Lighter o tokenización. Para cada uno, di dónde está documentado.

**Respuesta de referencia.**

- **Bankless** (tres de estos):
  1. Bankless LLC es miembro del oDAO de Rocket Pool y "recibe compensación en RPL" (hoja "Bankless LLC disclosures").
  2. Bankless Ventures tiene en portafolio a EtherFi (desde el 1T-2024), Puffer, Renzo, KelpDAO y Swell, cuyo negocio depende del rendimiento de *staking* (hoja "Bankless Ventures disclosures"). El CEO de EtherFi fue el invitado que argumentó contra la propuesta ("The EIP That Destroys DeFi", 10-ago-2026).
  3. Ambos anfitriones son asesores de EigenLayer (*restaking*), según la hoja "Individual disclosures".
  4. Ryan declara ETH como activo material.
- **The Chopping Block** (dos de estos):
  1. En el episodio del 28-ago-2026: "Lighter, in which we are all investors. We're investors in HYPE as well". En el del 17-sep-2026 lo repiten al hablar del caso de los ingenieros de Robinhood.
  2. Robert Leshner es CEO de Superstate, empresa de tokenización, y opinó que el fracaso de CLARITY "changes nothing for tokenization".
  3. El programa es propiedad de "Exuvia, LLC", que declara usar información de "portfolio companies of funds managed by Exuvia".
  4. Tom y Haseeb son socios de Dragonfly, cuyo fondo de US$650 M (feb-2026) apuesta por las finanzas cripto (CoinDesk).

*Fuentes:* hoja pública de divulgaciones de Bankless; notas RSS de Bankless (10-ago-2026); transcripciones propias de The Chopping Block (28-ago y 17-sep-2026); página de divulgaciones de The Chopping Block; CoinDesk, 17-feb-2026.

---

## P3. Medir una tesis vieja de un podcast (10 pts)

Bankless tituló "ETH Goes Ultra Sound" el 11-nov-2022. Con precios de cierre de Coinbase y la serie de oferta de ultrasound.money, calcula:

(a) el múltiplo de ETH y de BTC desde ese día hasta el 25-sep-2026;
(b) el cambio de la razón ETH/BTC;
(c) la oferta de ETH en The Merge, su mínimo posterior (con fecha) y su valor actual.

¿Qué concluyes sobre la tesis?

**Respuesta de referencia.**

- **(a)** ETH pasó de US$1,285.29 a ~US$2,685 (**×2.09**). BTC pasó de US$17,013.62 a ~US$83,920 (**×4.93**).
- **(b)** ETH/BTC bajó de 0.0755 a 0.0320: **−57.6%**.
- **(c)** Oferta de ETH:
  - **120.52 M** en The Merge (15-sep-2022);
  - mínimo de **120.06 M** el 5-abr-2024, tras Dencun;
  - **122.07 M** hoy: +1.29% sobre The Merge (~0.32% anual).
- **Conclusión:**
  - La tesis deflacionaria se cumplió unos 18 meses y luego se revirtió.
  - Como inversión relativa contra BTC fue perdedora.
  - El propio David Hoffman lo admitió el 25-sep-2026 ("we all threw ultrasound money into the garbage").
  - Una narrativa monetaria atractiva no sustituye la medición.

*Fuentes:* velas diarias de Coinbase Exchange; `ultrasound.money/api/v2/fees/supply-over-time`; feed RSS de Bankless; ficha [02](../recursos/02-bankless.md).

---

## P4. Desmontar un folleto "ZK" (10 pts)

Un proyecto dice: "Nuestra L2 usa pruebas de conocimiento cero, así que es privada, poscuántica y a prueba de fallas". Refuta las tres afirmaciones con argumentos del MOOC de Berkeley y un hecho de 2026.

**Respuesta de referencia.**

1. **"Privada."** Un zkRollup usa la **sucintez**: la L1 verifica rápido un lote. No necesita conocimiento cero y publica sus datos. La privacidad es otro uso, como Zcash o Aztec (clase 2, diapositivas 7-8).
2. **"Poscuántica."**
   - Depende por completo del **esquema de compromiso**. KZG y Groth16 (*pairings*) no son poscuánticos. FRI/STARK es plausiblemente poscuántico (clase 8, diapositivas 5 y 7).
   - Aun con pruebas STARK, el sistema no lo es entero. StarkWare admite que las firmas de cuentas de Starknet y el puente y los *blobs* de Ethereum todavía no lo son (The Quantum Insider, 30-jun-2026).
3. **"A prueba de fallas."**
   - La seguridad de FRI en la mayoría de los despliegues descansa en una **conjetura**.
   - Una versión no interactiva con λ bits cae con probabilidad 2^(k−λ) ante 2^k hashes (*grinding*).
   - Los circuitos pueden tener bugs (clase 14).
   - Además está el riesgo operativo: llaves que actualizan el verificador o el puente, y un secuenciador centralizado.

*Fuentes:* rdi.berkeley.edu/zk-learning, diapositivas de las clases 2, 8 y 14; The Quantum Insider, 30-jun-2026; ficha [18](../recursos/18-zero-knowledge-proofs-mooc.md).

---

## P5. Cálculo de seguridad no interactiva (10 pts)

Un sistema de pruebas no interactivo ofrece λ = 100 bits. Un atacante puede hacer 2^90 hashes.

(a) ¿Qué probabilidad de éxito tiene un ataque de *grinding*? ¿Y si λ = 128?
(b) Con el hashrate de Bitcoin del 25-sep-2026 (918 EH/s), ¿cuánto tiempo de toda la red equivale a 2^90 hashes? Es una comparación ilustrativa.
(c) Con FRI a tasa ρ = 1/8, ¿cuántas consultas hacen falta para 100 bits bajo la conjetura?

**Respuesta de referencia.**

- **(a)**
  - Con λ = 100: 2^(90−100) = 2^−10 ≈ **0.098%** (1 en 1,024).
  - Con λ = 128: 2^−38 ≈ **3.6×10^−12**.
- **(b)** 918×10^18 × 3,600 ≈ 3.3×10^24 hashes por hora ≈ 2^81.45. Entonces 2^90 / 2^81.45 = 2^8.55 ≈ **375 horas ≈ 15.6 días** de toda la red.
  - Salvedad: los hashes de un sistema de pruebas no son SHA-256; es solo un orden de magnitud.
  - Moraleja de la clase 8: 60 u 80 bits no interactivos no bastan cuando el premio es grande.
- **(c)** Cada consulta aporta log₂(8) = 3 bits, así que hacen falta ⌈100/3⌉ = **34 consultas**.

*Fuentes:* clase 8 del MOOC (diapositivas 50-53 y 69-79); API de mempool.space; cálculo en Python reproducido en la ficha [18](../recursos/18-zero-knowledge-proofs-mooc.md).

---

## P6. La regulación por agencias (10 pts)

Describe los topes y la duración de la "exención de innovación" de la SEC del 17-sep-2026. Explica qué omitió Bankless y compárala con Regulation Crypto Assets (propuesta del 18-ago-2026). ¿Qué riesgo político comparten ambas?

**Respuesta de referencia.**

- **Exención de innovación** (comunicado 2026-90):
  - Exime a los *Tokenized Securities Venues* (AMMs con acciones tokenizadas) de la definición de "exchange", y a ciertos proveedores de liquidez de la de "dealer".
  - Dura **5 años**, hasta el 17-sep-2031.
  - Exige acceso con permiso y que los contratos sean "auditable, public, and deployed on a public, permissionless distributed ledger".
  - Topes: **nivel 1** (S&P 500, Russell 1000 y ciertos ETPs), 75 símbolos y **0.25%** del volumen diario promedio del mes previo; **nivel 2**, 250 símbolos y **2.5%**.
- **Qué omitió Bankless:** solo citó el 0.25%, y lo presentó como si fuera un tope general.
- **Regulation Crypto Assets** (comunicado 2026-76):
  - Una exención de hasta **US$5 M** una sola vez en un periodo de 4 años.
  - Otra de hasta **US$75 M** cada 12 meses, con estados financieros y reportes continuos.
  - Un puerto seguro condicional respecto de "investment contract".
  - Comentarios hasta el 20-oct-2026.
- **Riesgo compartido:** son acciones de agencia tras el fracaso de CLARITY. Son menos durables que una ley y otra administración puede revertirlas. El precio debe descontar ese riesgo.

*Fuentes:* sec.gov, comunicados 2026-90 y 2026-76; memorandos de Skadden y Dechert (sep-2026); Federal Register, 21-ago-2026.

---

## P7. Leer un contrato y los límites de la auditoría (10 pts)

Un protocolo presume ser "auditado por OpenZeppelin". En Etherscan ves que el contrato principal es un *proxy*, que su *admin* es una sola cuenta externa (EOA) y que no hay *timelock*.

(a) ¿Qué riesgo queda aunque la auditoría sea buena?
(b) ¿Qué revisarías en el explorador, en orden?
(c) ¿Qué dice ETH Kipu sobre lo que una auditoría no cubre?
(d) ¿Qué indica sobre la industria la operación de S&P Global anunciada el 17-sep-2026?

**Respuesta de referencia.**

- **(a)** El *admin* puede cambiar la implementación, así que el código auditado puede dejar de ser el que corre. Si le roban la llave privada, "el protocolo entero cae" (ETH Kipu, clase 16).
- **(b)** Revisaría, en este orden:
  1. código verificado;
  2. "Read as Proxy" y la dirección de implementación;
  3. el historial de eventos de actualización y de cambio de dueño;
  4. `owner()` y los roles en *Read Contract*;
  5. si hay multisig o DAO y *timelock*;
  6. la fecha y la versión auditada frente a la desplegada;
  7. mis permisos (*allowances*), para revocarlos si hace falta.
- **(c)** Una auditoría no protege contra errores de diseño, cambios futuros, nuevas técnicas de ataque, dependencias comprometidas ni problemas operativos. "El objetivo no es alcanzar el riesgo cero (que no existe)" (clase 17).
- **(d)** S&P Global acordó comprar OpenZeppelin, sin revelar términos. OpenZeppelin reportará al presidente de S&P Global Ratings. El comunicado dice que sus contratos respaldan "más de US$37 billones (millones de millones) transferidos" y que suma "900+" encargos de seguridad.
  - La auditoría se institucionaliza y se acerca a las calificadoras, pero **no elimina** el riesgo de *admin* del caso.

*Fuentes:* fichas [19](../recursos/19-eth-kipu-ethereum-developer-pack.md) y [14](../recursos/14-learn-blockchain-solidity-full-stack-web3.md); comunicado de S&P Global del 17-sep-2026.

---

## P8. Un episodio histórico contra lo que pasó (10 pts)

En el ep. 418 de The Chopping Block (9-nov-2022), grabado el día de la carta de intención de Binance para comprar FTX, los participantes hicieron cinco afirmaciones:

1. "60% probability that the deal closes";
2. "FTX US is fine";
3. lo ocurrido "is likely going to be criminal";
4. el valor empresarial de FTX es negativo y sin Binance "FTX is probably toast";
5. Solana "has exit velocity".

(a) Califica cada una como acierto o fallo, con fecha y fuente.
(b) Si en ese momento tenías 1 BTC en FTX, ¿cuánto vale hoy tu recuperación medida en BTC?
(c) ¿Qué regla de custodia se deriva para la cuenta actual?

**Respuesta de referencia.**

- **(a)**
  1. **Fallo.** Binance se retiró ese mismo 9-nov-2022 (CoinDesk, TechCrunch, CNBC).
  2. **Fallo.** FTX US (West Realm Shires Services) suspendió retiros el 10-nov-2022 y entró al Capítulo 11 el 11-nov-2022 (Georgia DBF y otros reguladores estatales).
  3. **Acierto.** SBF fue condenado en nov-2023 y sentenciado a 25 años el 28-mar-2024 (DOJ).
  4. **Acierto.** Nadie compró y FTX pidió el Capítulo 11 el 11-nov-2022.
  5. **Acierto en el largo plazo, con un camino brutal.** SOL pasó de US$13.97 (9-nov-2022) a US$8.00 (29-dic-2022) y a ~US$121.6 (25-sep-2026).

  Balance: 3 aciertos y 2 fallos. Los *insiders* también admitieron que una semana antes creían que FTX "would be fine".
- **(b)** El plan (confirmado el 7-oct-2024) paga ~119% del reclamo al 98% de los acreedores, valuado al precio del 11-nov-2022 (BTC US$16,871). 1.19 × 16,871 = **US$20,076**. Con BTC a ~US$83,920, eso es **23.9% de un BTC**.
- **(c)** El saldo en un exchange es un **reclamo en dólares** contra el exchange, no propiedad de la moneda:
  - mantener en el exchange solo lo necesario para operar;
  - revisar la prueba de reservas, sabiendo su límite: no prueba la ausencia de otros pasivos;
  - para retirar a autocustodia, aplicar la lección de Coldcard: proveedor de *hardware* serio, firmware verificado y semilla generada con buena entropía.

*Fuentes:* transcripción propia del audio público del ep. 418 (RSS de Unchained); DOJ, 28-mar-2024; comunicado de confirmación del plan de FTX, 7-oct-2024; Bitcoin.com, 28-dic-2023 (tabla de conversión); velas diarias de Coinbase; ficha [09](../recursos/09-the-chopping-block.md).

---

## Clave rápida

| P | Tema | Cifra o dato ancla |
|---|---|---|
| 1 | Verificar votos | CLARITY 49-50 (votación 234, 15-sep-2026) |
| 2 | Conflictos | oDAO de Rocket Pool y RPL; EtherFi; "we are all investors in Lighter… HYPE" |
| 3 | Ultra Sound Money | ETH/BTC −57.6%; oferta +1.29% sobre The Merge |
| 4 | Folleto ZK | Sucintez ≠ privacidad; el esquema de compromiso decide lo poscuántico |
| 5 | Grinding | 2^−10; ~15.6 días de red; 34 consultas FRI |
| 6 | Regulación por agencias | 0.25%/75 y 2.5%/250; 5 años; US$5 M y US$75 M |
| 7 | Contrato *proxy* | *Admin* EOA sin *timelock* = riesgo que la auditoría no cubre |
| 8 | FTX | 3 aciertos y 2 fallos; 23.9% de un BTC |
