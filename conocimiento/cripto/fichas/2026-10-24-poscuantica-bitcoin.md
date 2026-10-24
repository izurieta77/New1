# Ficha de avance · 24-oct-2026 · Criptografía poscuántica en bitcoin: qué está expuesto, cuánto cuesta migrar y cuándo importa

> Corrida de las 08:17 CDMX (14:2x UTC), estudio profundo. Nivel **Doctorado** (protocolo y seguridad), grupo G1 (Bitcoin) con cruce a G6 (podcasts).
>
> **Por qué este tema.** Es el siguiente de la cola que dejó el plan el 23-oct. Además cierra un hueco declarado: el cap. 01, §5 y §6, dice "Cuántico · Sin fecha · No cubierto en G1 · Sin evaluar". El detonante fue el episodio de Unchained del 21/22-oct (Laura Shin con Project Eleven).

## 0. Preguntas de hoy

1. ¿Qué rompe exactamente una computadora cuántica relevante (CRQC) en bitcoin, y qué no?
2. ¿Cuánto bajó en 2017-2026 la estimación de recursos para romper secp256k1?
3. ¿Qué proponen BIP-360 y BIP-361, y cuánto cuesta en espacio de bloque firmar con los estándares del NIST?
4. ¿Cambia algo para `arena-claude-binance` o para la tesis de BTC a 4 meses?

## 1. Acceso y fuentes (declarado)

| Fuente | Grado | Acceso |
|---|---|---|
| **BIP-360, "Pay-to-Merkle-Root (P2MR)"**, v0.12.1 (24-jul-2026), estatus *Draft*. Hunter Beast, Ethan Heilman e Isabel Foxen Duke. [raw en bitcoin/bips](https://raw.githubusercontent.com/bitcoin/bips/master/bip-0360.mediawiki) | A (texto de la propuesta) | **Íntegro** (36,968 bytes) |
| **BIP-361, "Post Quantum Migration and Legacy Signature Sunset"**, *Draft*, asignado el 11-feb-2026. Jameson Lopp y otros. [raw](https://raw.githubusercontent.com/bitcoin/bips/master/bip-0361.mediawiki) | A (texto de la propuesta) | Resumen, motivación y tabla de fases |
| **NIST FIPS 204 (ML-DSA)** y **FIPS 205 (SLH-DSA)**, ago-2024. [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) | A | Tablas 2 de ambos (tamaños de llave y firma), extraídas del PDF |
| **Roetteler, Naehrig, Svore y Lauter (2017)**, "Quantum resource estimates for computing elliptic curve discrete logarithms", [arXiv 1706.06752](https://arxiv.org/abs/1706.06752) | A (preprint, publicado en ASIACRYPT 2017) | Solo el resumen (trae la fórmula) |
| **Babbush, Zalcman, Gidney, …, Drake y Boneh (2026)**, "Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities", [IACR ePrint 2026/625](https://eprint.iacr.org/2026/625) | A en lo que dice; las cifras se validan con una prueba de conocimiento cero, sin publicar el circuito | Solo el resumen |
| **Gidney (2025)**, RSA-2048 con menos de un millón de qubits ruidosos, [arXiv 2505.15917](https://arxiv.org/abs/2505.15917) | A | Solo el resumen (supuestos de hardware) |
| **IonQ (3-sep-2026)**, secp256k1 en 26 días con ~20,000 qubits físicos de iones atrapados ([blog de IonQ](https://ionq.com/blog/the-first-full-stack-blueprint-for-breaking-256-bit-elliptic-curve-signatures); [The Quantum Insider](https://thequantuminsider.com/2026/09/08/ionq-estimates-20000-qubit-ma)) | **C**: es una empresa que vende computadoras cuánticas; sin arXiv en lo que vi | Prensa y resumen del buscador |
| **Unchained, "How Crypto Can Survive If AI or Quantum Computers Break Its Cryptography"** (feed del 21-oct, 04:49 UTC; [feed](https://feeds.megaphone.fm/LSHML4761942757)) | **C/D**: los invitados (Project Eleven) venden productos poscuánticos; episodio patrocinado por Nexo | **Solo las notas del episodio**: la transcripción es de pago |

**Lo que no logré:** el rastreador de BTC expuesto de Project Eleven respondió 403. La cifra de **6.65 M BTC expuestos** que trae el cap. 05 (recurso 30, Galaxy) sigue sin verificación propia y queda en C.

## 2. Lo que dicen las fuentes [H]

- **Qué rompe Shor y qué no.** BIP-360: el riesgo principal es la *quantum key recovery*, sacar la llave privada de la pública en la curva elíptica (ECDSA y Schnorr). La prueba de trabajo (SHA-256) no está en juego: Grover solo da una ventaja cuadrática. Esto ya lo había anotado como inferencia el cap. 06; hoy queda confirmado con fuente A.
- **Dos ataques distintos (BIP-360, glosario).**
  - **Exposición larga:** contra llaves públicas que ya están en la cadena. Afecta las salidas **P2PK** ("Satoshi's coins, CPU miners"), las **reusadas**, las **P2MS** y **las Taproot (bc1p)**, porque P2TR pone la llave en la salida. En P2PKH, P2SH, P2WPKH y P2WSH la llave solo aparece al gastar, así que esas salidas no son vulnerables mientras nadie reuse la dirección. Las xpubs también delatan las llaves.
  - **Exposición corta (*on-spend*):** el atacante saca la llave del mempool, entre el anuncio de la transacción y su confirmación. Pide una máquina más rápida.
- **BIP-360 (P2MR) solo arregla la exposición larga.** Es P2TR **sin la ruta de llave**: la salida compromete la raíz de Merkle del árbol de scripts (SegWit v2, direcciones `bc1z`). Para la exposición corta "may require the introduction of post-quantum signatures", y los autores dicen que esa propuesta vendrá por separado. **No hay opcode poscuántico en ningún BIP activo.** La historia de nombres (P2QRH → P2TSH → P2MR, v0.8 a v0.11) muestra que el diseño todavía se mueve.
- **BIP-361 (Lopp y otros) le pone fecha a la migración.** Fase A: 160,000 bloques (~3 años) después de su activación, no se puede enviar a direcciones vulnerables. Fase B: dos años después, los gastos ECDSA/Schnorr quedan restringidos a un protocolo de rescate. Depende de un BIP de firmas poscuánticas que todavía no existe ("Requires: TBD"). En la práctica, congela las monedas que no migren, incluidas las P2PK sin dueño activo. Eso sería un **cambio social del contrato de bitcoin**, no solo uno técnico.
- **Los recursos necesarios caen rápido.** Roetteler (2017): 2,330 qubits lógicos y 1.29 × 10¹¹ Toffoli para n = 256. Babbush et al. (2026): **≤ 1,200 qubits lógicos y ≤ 90 M Toffoli**, o ≤ 1,450 y ≤ 70 M, y "en minutos" con menos de medio millón de qubits físicos superconductores a 10⁻³ de error. El paper distingue arquitecturas de **reloj rápido** (superconductoras y fotónicas), que harían posible el ataque *on-spend*, de las de **reloj lento** (átomos neutros e iones). IonQ, que es de reloj lento, habla de 26 días por llave.
- **Fechas, de partes interesadas.** Pruden (Project Eleven, C/D) pone el "Q-Day" en 2030 como muy pronto y en 2033-2035 como más probable que no. Justin Drake (coautor de 2026/625, de la EF) propone un "modo búnker" y advierte que la IA podría romper curvas antes. En contra, Deegan dice que "ningún esquema en producción está roto"; Hawk y McEliece cayeron ante ataques con IA, pero no están en producción. El NIST pide dejar ECC en el gobierno federal después de 2035 (NIST IR 8547, citado por BIP-360; no lo leí).

## 3. Ejercicio numérico (comprobado en Python)

Script [`2026-10-24-poscuantica-bitcoin.py`](2026-10-24-poscuantica-bitcoin.py), corrido el 24-oct a las 14:3x UTC (`python3 -I`). Las partes A, B, D y E son deterministas; la parte C usa 300 intervalos reales de bloque de [mempool.space](https://mempool.space/api/v1/blocks/972929), hasta la altura 972,929.

**A. Caída de los recursos (n = 256).** Roetteler: 9n + 2⌈log₂n⌉ + 10 = **2,330 qubits** y 448n³log₂n + 4090n³ = **1.287 × 10¹¹ Toffoli**. Babbush 2026 los divide **÷1.9 en qubits y ÷1,431 en Toffoli** (÷1,839 con la variante de 1,450 qubits); IonQ, ÷3,301 (C). En nueve años, el costo en compuertas bajó tres órdenes de magnitud. El hardware no avanzó igual, pero la meta se acercó.

**B. Espacio de bloque.** Transacción de 1 entrada y 2 salidas, con 4 M de unidades de peso por bloque:

| Entrada | Testigo | vB | Veces P2TR | tx/bloque | tx/s | Comisión a 2 sat/vB |
|---|---|---|---|---|---|---|
| P2TR, ruta de llave (Schnorr 64 B) | 66 B | 154.0 | ×1.00 | 6,494 | 10.8 | 308 sats |
| P2MR, hoja ML-DSA-44 (pk 1,312 + firma 2,420) | 3,777 B | 1,081.8 | **×7.0** | 924 | 1.5 | 2,164 sats |
| P2MR, hoja SLH-DSA-128s (pk 32 + firma 7,856) | 7,929 B | 2,119.8 | **×13.8** | 472 | 0.8 | 4,240 sats |

El descuento del testigo (÷4) ya está incluido y aun así la capacidad cae 7-14 veces. Migrar unos 50 M de UTXOs con firmas de este tamaño ocuparía meses de bloques llenos. Esto es inferencia mía [I]: el número de UTXOs no lo verifiqué hoy. Por eso BIP-361 habla de años y por eso subirían las comisiones. El opcode y la hoja son hipotéticos: ningún BIP los define todavía.

**C. Exposición corta: P(el atacante termina antes de la 1.ª confirmación).**

| Minutos que tarda el ataque | Poisson (10 min) | Empírica, instante al azar (300 bloques, media 9.17 min) |
|---|---|---|
| 1 | 0.905 | 0.901 |
| 5 | 0.607 | 0.581 |
| 9 | 0.407 | 0.379 |
| 10 | 0.368 | 0.342 |
| 20 | 0.135 | 0.107 |
| 60 | 0.002 | — |

Si el ataque tarda "minutos", como dice 2026/625 para reloj rápido, **un tercio o más** de los gastos de salidas no expuestas quedaría a merced de quien pueda reemplazar la transacción con más comisión. Esto vale también para P2WPKH, que hoy se considera "segura". Una máquina de 26 días (IonQ) no hace este ataque. La empírica queda un poco abajo de Poisson porque la red va más rápido que 10 min (hashrate al alza). Los *timestamps* de bloque son ruidosos, así que la diferencia no es significativa.

**D. Exposición larga: cuántas llaves barre una sola máquina, en secuencia.** A 26 días por llave, 14 llaves al año, o ~700 BTC al año si cada salida P2PK trae 50 BTC (recompensa de 2009-2012). A 10 minutos por llave, 52,560 llaves y **2.6 M BTC al año**. Lo que decide el riesgo es el **reloj de la máquina** (los dos casos difieren por un factor de 3,700), más que la "llegada" de la primera CRQC.

**E. Calendario de BIP-361.** 160,000 bloques son 3.04 años. Si se activara en 2027, la fase A llegaría en ~2030 y la fase B en ~2032; activado en 2029, en ~2032 y ~2034. Esas fechas se empalman con la ventana 2030-2035 de Pruden (C/D). Pero no hay ni siquiera un BIP de firmas, y los soft forks de bitcoin han tardado años: Taproot, de la propuesta (2018) a la activación (nov-2021).

## 4. Qué cambia para invertir [I/O]

- **Para `arena-claude-binance` (temporada al 28-ene-2027): nada operativo.** Ningún escenario serio pone una CRQC antes de 2030. El filtro SMA200 × 0.97/1.03 sigue mandando y no se agrega regla.
- **Custodia.** Nuestro BTC está en Binance (custodia del exchange), y la exposición de las llaves depende de cómo administra Binance sus carteras: reuso, Taproot, P2PK. No es público. En un ETF, el custodio (p. ej. Coinbase Custody para IBIT) tiene el mismo problema. Si algún día se pasa a autocustodia: **nunca reusar direcciones** y preferir P2WPKH/P2WSH sobre P2TR mientras no exista P2MR. Esto protege contra la exposición larga, no contra la corta.
- **Riesgo de cola de largo plazo, para el cap. 01 §5.** Hay dos canales con signo opuesto:
  - **robo:** ~1 M BTC en P2PK atribuidos a Satoshi, cifra de prensa (C), que entrarían al mercado;
  - **congelamiento por BIP-361:** oferta efectiva menor, pero con daño a la neutralidad del protocolo.

  Ninguno se puede valorar con datos hoy. La señal medible sería la **adopción**: que un BIP de firmas pase a *Proposed* o que Bitcoin Core fusione P2MR. Se vigila como frontera, no como señal de precio.
- **Narrativa contra evidencia.** El episodio de Unchained tiene invitados que venden PQC y un patrocinador cripto. Sus fechas (Q-Day 2030-2035) son grado C/D y no tienen historial auditado. Lo único A de hoy son los BIPs, los FIPS y los resúmenes de los papers.

## 5. Contrapuntos y límites

- Los recursos de 2026/625 se validan con una prueba ZK, **sin publicar el circuito**. Es una disclosure responsable, pero nadie lo ha replicado de forma independiente.
- Los qubits **lógicos** no son físicos: el salto de ~100 qubits de alta calidad (2024-2026) a ~500,000 físicos con corrección de errores es el verdadero cuello de botella, y aquí no lo cuantifico.
- Las tallas de la parte B suponen una hoja mínima (`<pk> OP_CHECKSIG_PQ`) con profundidad 1. Las agregaciones de firmas o los esquemas más compactos (FN-DSA/Falcon, ~666 B por firma, FIPS 206 todavía en borrador) bajarían el múltiplo, que es una cota superior razonable, no exacta.
- La parte C supone que el atacante puede reemplazar la transacción (RBF) y que el minero toma la de mayor comisión. Un minero que respete la transacción original, o un acuerdo fuera del mempool, reduce el riesgo.
- No verifiqué la cifra de BTC expuesto (6.65 M en el cap. 05, C) ni la de P2PK.

## 6. Autoexamen

1. *¿Por qué P2WPKH no tiene exposición larga pero sí corta?* La salida solo trae el hash de la llave. La llave aparece al gastar y queda en el mempool hasta que se confirma.
2. *¿Qué quita P2MR respecto de P2TR?* La ruta de llave: compromete solo la raíz de Merkle (SegWit v2, `bc1z`).
3. *Con ML-DSA-44, ¿cuántas veces crece una transacción 1-2?* ~7.0× (154 → 1,082 vB).
4. *Si un ataque tarda 10 min y los bloques son Poisson de 10 min, ¿qué probabilidad tiene de llegar antes de la confirmación?* e⁻¹ ≈ 0.37.
5. *¿Por qué importa el reloj y no solo los qubits?* Porque fija cuántas llaves se barren al año (14 contra 52,560) y si el ataque *on-spend* es posible.

## 7. Estado

- **Documentado con comprobación** (nivel Doctorado: seguridad del protocolo). Cierra la fila "Cuántico · Sin evaluar" del cap. 01 §5 con una adenda.
- **Siguiente prueba:**
  1. contar, con un nodo o con un conjunto de datos público verificable, el BTC en P2PK, en P2TR y en direcciones reusadas;
  2. leer completos 2026/625 y NIST IR 8547;
  3. vigilar el estatus de BIP-360 y BIP-361 y el primer BIP de firmas poscuánticas.
