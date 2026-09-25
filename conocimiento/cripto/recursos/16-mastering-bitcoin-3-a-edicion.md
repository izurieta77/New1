# 16 · Mastering Bitcoin, 3.ª edición (Antonopoulos y Harding)

> Ficha de recurso · Grupo G1 (Bitcoin) · Estudiada el 25-sep-2026 por `analista-cripto` · **Acceso: sección amplia**: 10 de 14 capítulos y el apéndice B completos, el resto por encabezados · **Grado global: A** en la mecánica del protocolo (verificable en código y BIPs); **B** en cifras del estado de la red, que envejecen; **C-D** en las opiniones de los autores.
>
> **Etiquetas:**
> - **[H]** hecho con fuente y capítulo;
> - **[I]** inferencia o interpretación (digo si es del autor o nuestra);
> - **[O]** opinión o pronóstico del autor.
>
> **Grados:**
> - **A:** identidad o dato oficial;
> - **B:** evidencia sólida con salvedades;
> - **C:** muestra corta o no reproducible;
> - **D:** narrativa sin historial auditado.

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 3.ª ed. impresa en dic-2023 (O'Reilly, ISBN 978-1-098-15009-9, © 2024 David Harding). Repo leído: commit `275c4eb` del 26-dic-2024 ("2024-12-cc-by-sa") |
| Autor | Andreas M. Antonopoulos y David A. Harding |
| Tipo | Libro técnico para programadores: llaves, billeteras, transacciones, Script y Taproot, firmas, comisiones, red, blockchain, minería y consenso, seguridad, segunda capa |
| Nivel | Avanzado: maestría a doctorado |
| Costo | Gratis en GitHub con licencia CC BY-SA 4.0 (antes era no comercial). El impreso cuesta ~US$50 según el índice del dueño |
| Idioma | Inglés |
| URL | https://github.com/bitcoinbook/bitcoinbook |
| **Conflictos de interés** | Los dos autores viven de educar sobre Bitcoin: libros, charlas y documentación técnica. Antonopoulos acuñó "Your keys, your coins. Not your keys, not your coins" (cap. 1). En lo que revisé **no encontré** una declaración de tenencias. El libro no hace recomendaciones de precio ni de inversión, lo que reduce el sesgo práctico |

## 2. Acceso real

- **Leído completo (prosa) en AsciiDoc, en el scratchpad, el 25-sep-2026:**
  - cap. 4 (llaves y direcciones);
  - cap. 5 (recuperación de billeteras);
  - cap. 6 (transacciones);
  - cap. 7 (autorización y autenticación: Script, timelocks, SegWit, MAST, Taproot, Tapscript);
  - cap. 9 (comisiones);
  - cap. 10 (red);
  - cap. 11 (blockchain);
  - cap. 12 (minería y consenso);
  - cap. 13 (seguridad);
  - cap. 14 (segunda capa);
  - apéndice B (erratas del whitepaper).
- **Leído en parte:**
  - cap. 1: secciones clave;
  - cap. 8 (firmas): introducción, reutilización del nonce y Schnorr por encabezados.
- **Por encabezados y puntos clave:** cap. 2 (panorama), cap. 3 (Bitcoin Core), apéndice A (whitepaper) y apéndice C (BIPs).
- **Contraste:** verifiqué las afirmaciones que envejecen con las notas de versión de Bitcoin Core (raw.githubusercontent.com y bitcoincore.org) y con datos de mempool.space y blockstream.info del 25-sep-2026.
- **Nivel: sección (amplia).** No afirmo lectura íntegra. No copié texto del libro al repo.

## 3. Lo esencial

### Llaves, direcciones y billeteras (caps. 4-5)

- **[H] La criptografía asimétrica de Bitcoin sirve para firmar, no para cifrar** (cap. 4).
  - La clave privada es un número aleatorio; la curva es secp256k1 con p = 2^256 − 2^32 − 2^9 − 2^8 − 2^7 − 2^6 − 2^4 − 1, que verifiqué.
  - Dos erratas del cap. 4: dice que el rango válido es "0 a n − 1" (es 1 a n − 1) y que secp256k1 la "estableció NIST". La curva está en SEC 2, del SECG; la de NIST es P-256 = secp256r1.
- **[H] Historia de los tipos de salida:**
  - P2PK → P2PKH (HASH160 = RIPEMD160(SHA256)) → P2SH (BIP16, 2012; direcciones "3") → SegWit v0 con bech32 (P2WPKH de 20 B, P2WSH de 32 B) → Taproot con bech32m (P2TR).
  - bech32 detecta cualquier error de hasta 4 caracteres. Una falla de longitud llevó a bech32m (BIP350, constante 0x2bc830a3).
- **[H] Resistencia a colisiones (cap. 4).**
  - En P2SH, si el atacante controla parte del script (por ejemplo, en un multisig), una colisión cuesta **2^80** operaciones. "A inicios de 2023 los mineros hacían ~2^80 hashes por hora."
  - Las direcciones nuevas (P2WSH, P2TR) dan ≥ 128 bits, que costarían ~32 mil millones de años.
- **[H] "DO NOT USE PAPER WALLETS"** (cap. 4). Contradice al Diplomado v3, p. 56.
- **[H] BIP32 (cap. 5): todas las billeteras modernas son HD.**
  - Exportar la **xpub** junto con **una** clave privada hija no endurecida compromete todas las claves de esa rama. La derivación endurecida (índices ≥ 2^31) lo evita.
  - BTCPay usa la xpub en el servidor: si lo hackean, solo se pierden los pagos futuros.
- **[H] BIP39 (cap. 5).**
  - 128-256 bits de entropía + checksum de ENT/32 bits, en palabras de 11 bits.
  - PBKDF2 con 2,048 rondas, que el libro llama "débil para estándares modernos", da una semilla de 512 bits.
  - La seguridad de una clave pública es de 128 bits: más de 128 bits de entropía casi no aporta.
  - La passphrase no entra en el checksum. Eso da negación plausible, pero un error de tecleo equivale a fondos "perdidos".
- **[H] Descriptores (BIPs 380-386 y 389) y respaldos de datos (cap. 5).**
  - En multisig hay que respaldar las claves públicas de todos y las condiciones del script, no solo la semilla. Lo repite el cap. 13.
  - [O] "Una de las principales causas de pérdida de bitcoins, quizá LA principal, es la pérdida de datos."
- **[H] Riesgo físico (cap. 5).** Jameson Lopp documentó **más de 100 ataques físicos** contra poseedores de cripto, con al menos 3 muertes (cifra del momento de redacción, ~2023).

### Transacciones, Script y Taproot (caps. 6-8)

- **[H] Una transacción no es efectivo al portador (cap. 6).**
  - Es un mensaje que convence a los nodos completos de actualizar su base de UTXO (> 5 GB "al escribir").
  - Las salidas van de 0 a 21 M BTC por consenso. Polvo: < 546 sats en muchos programas.
  - La coinbase madura a las **100** confirmaciones. El bloque admite hasta **4,000,000** unidades de peso (WU).
- **[H] SegWit: la idea es de 2011, el soft fork se describió a fines de 2015 y se activó en 2017.**
  - Elimina la maleabilidad de terceros, requisito para Lightning.
  - Los soft forks **solo restringen** reglas (caps. 6 y 12).
- **[H] Script (cap. 7).**
  - Es deliberadamente **no Turing completo**: tiempos de ejecución predecibles y validación sin estado.
  - Límites: multisig "bare" hasta 3 claves por política, P2SH hasta 15.
  - Timelocks: CLTV (BIP65, dic-2015) y CSV (BIP68/112).
  - Ejemplo de herencia/contingencia: 2-de-3 socios; a los 30 días, abogado + 1; a los 90 días, el abogado solo.
- **[H] Taproot, activado en nov-2021 (cap. 7).**
  - Una clave ajustada compromete un árbol MAST; el gasto por clave hace que todos los gastos se vean iguales.
  - Tapscript cambia OP_CHECKMULTISIG por OP_CHECKSIGADD, usa Schnorr (BIP340) con validación por lotes y deja OP_SUCCESSx para futuros soft forks.
- **[H] Reutilizar el nonce de una firma con la misma clave expone la clave privada (cap. 8)** y ha causado robos reales. Se evita con RFC6979 o BIP340.

### Comisiones, red, minería y consenso (caps. 9-12)

- **[H] La comisión es una puja en una subasta por espacio de bloque (cap. 9).**
  - Los mineros pueden excluir cualquier transacción.
  - RBF (BIP125) y CPFP.
  - [O/I del autor] El **fee sniping** "hoy no es lucrativo porque el subsidio es mucho mayor que las comisiones… cuando las comisiones sean la mayor parte de la recompensa, este escenario se vuelve inevitable". Bitcoin Core lo mitiga con nLockTime anti-fee-sniping.
- **[H] Red (cap. 10).**
  - "~10,000 nodos que escuchan"; ">95% de los nodos completos corren Bitcoin Core", un **monocultivo** de implementación.
  - SPV prueba que una transacción existe, pero **no** puede probar que no hubo doble gasto.
  - Los filtros bloom (BIP37) fallaron en privacidad; los reemplazan los compact block filters (BIP157/158).
- **[H] Blockchain (cap. 11).**
  - El encabezado mide 80 B, contra ~4 MB de un bloque (50,000×).
  - Hubo una falla de diseño en Merkle (CVE-2012-2459).
  - La testnet muestra que el PoW sin valor económico es atacable: la seguridad **depende de incentivos económicos**.
- **[H] Emisión (cap. 12).**
  - 50 → 25 (nov-2012) → 12.5 (jul-2016) → 6.25 (may-2020) → 3.125 (abr-2024).
  - Máximo de 2,099,999,997,690,000 sats; el 99% se alcanza en el bloque ~1,411,200, hacia 2035 (cap. 1).
  - "Las comisiones suelen ser un porcentaje pequeño del ingreso del minero."
- **[H] Ajuste de dificultad cada 2,016 bloques, con un error de uno (cap. 12).**
  - Usa 2,015 intervalos, lo que da un sesgo de +0.05%; el ajuste está limitado a un factor de 4.
  - [O] "Bitcoin puede escalar y seguir seguro sin más hashrate que el actual."
  - Pools: un minero con 0.0001% del hashrate encontraría un bloque cada ~19-20 años. En Stratum v1 el operador del pool elige las transacciones; Stratum v2 devuelve esa elección a los mineros.
- **[H] Ataques de hashrate (cap. 12 y apéndice B).**
  - Con mayoría se puede hacer **doble gasto de transacciones propias y censurar**, pero no robar ni crear valor.
  - La investigación ubica ataques rentables desde ~**30%** (minería egoísta).
  - Recomendación: ≥ 6 confirmaciones para montos altos.
  - [O] "Un ataque serio erosionaría la confianza… con posible caída significativa del precio."
- **[H] Forks y gobernanza (cap. 12).**
  - La división accidental de la red por la base de datos en la migración 0.7 → 0.8 (2013).
  - Un split 80/20 dejaría la cadena minoritaria en 50 min por bloque y ~10 semanas hasta su ajuste.
  - Mecanismos de activación: BIP9 (95% = 1,916 de 2,016 bloques), BIP148 (UASF), BIP8 y Speedy Trial.
  - "Status quo is the stable state."

### Seguridad y segunda capa (caps. 13-14)

- **[H] Principios (cap. 13):**
  - "En Bitcoin la posesión es diez décimas de la ley": no hay recurso dentro del protocolo;
  - para quien diseña sistemas: "don't take control of keys away from users and don't outsource validation";
  - los exchanges con una sola hot wallet "fueron hackeados con consecuencias desastrosas";
  - un proyecto educativo perdió ~7,000 BTC en jul-2011 por respaldos cifrados cuya clave se perdió;
  - [O] tener "quizá menos de 5%" en billetera caliente como "cambio de bolsillo";
  - herencia con multisig y un ejecutor digital.
- **[H] Canales de pago y Lightning (cap. 14).**
  - Revocación asimétrica con CSV e índice de estado de 48 bits. La víctima **debe vigilar la cadena** para castigar a quien publique un estado viejo.
  - HTLC y enrutamiento cebolla. Poon y Dryja lo describieron en feb-2015; hay ≥ 5 implementaciones.
  - "El único activo nativo de Bitcoin es el bitcoin": RGB y Taproot Assets viven fuera del protocolo.

## 4. Qué cambia para invertir

### Presupuesto de seguridad (datos de mempool.space, 25-sep-2026 ~21:55 UTC; cálculo propio)

| Medida | Valor |
|---|---|
| Subsidio diario | 144 × 3.125 = **450 BTC** ≈ **US$37.8 M/día** a US$84,045.67 ≈ **US$13.8 mil M/año** |
| Comisiones, últimos 144 bloques | 4.069 BTC de 454.069 = **0.90%** de la recompensa |
| Comisiones, últimos 4,320 bloques (~30 días) | 85.30 BTC de 13,585.30 = **0.63%** |
| Recompensa por bloque | ≈ US$265,000; MB estimaba ~US$150,000 en 2023 |
| Hashrate / dificultad | ~922.7 EH/s; 132.76 T; siguiente ajuste en la altura 969,696, estimado en **−4.49%** |
| Bloque 968,589 | 3,420 transacciones; peso 3,993,589 WU (lleno); mediana ≈ 1.13 sat/vB |

- **[I, nuestra] La seguridad depende hoy en más de 99% del subsidio**, que se reduce a la mitad en BTC cada ~4 años.
  - Un aviso de política: Bitcoin Core **29.1 (4-sep-2025)** bajó el mínimo de retransmisión por defecto a **100 sat/kvB (0.1 sat/vB)** (PR #33106).
  - No es un riesgo para la temporada de 4 meses. Sí lo es para la tesis de 10-20 años: la seguridad en dólares exige un precio más alto o comisiones más altas, y el fee sniping es la falla que MB anticipa si no ocurre.

### Autocustodia frente a exchange: la cuenta Binance

- **[I, nuestra] La cuenta de torneo viola a propósito la regla de MB** ("not your keys"): se opera spot en un exchange que no está supervisado en México.
- La aceptamos porque el filtro SMA200 y los cortacircuitos exigen poder vender rápido. MB describe justo el riesgo que se asume: hot wallets centralizadas y confianza fuera de la cadena.
- **Mitigación coherente con MB, cap. 13:**
  - tope de tamaño (10,000 MXN; pérdida máxima de 5,000 MXN);
  - ruta alterna probada (Bitso por SPEI, o BTC on-chain a Bitso);
  - **verificar la dirección de destino completa** antes de enviar, sin confiar en el portapapeles.
- **Costo on-chain de la contingencia [cálculo propio].** Una transacción P2WPKH de 1 entrada y 2 salidas pesa **140.5 vB**: 10.5 de base + 68 de entrada + 2 × 31 de salidas (pesos del cap. 6).

  | Tasa | Costo |
  |---|---|
  | 1 sat/vB | 140 sats ≈ US$0.12 |
  | 2 sat/vB | 281 sats ≈ US$0.24 |
  | 50 sat/vB (día congestionado) | 7,025 sats ≈ US$5.90 |

  La comisión de retiro que cobre Binance es aparte y **no la verifiqué**.

### Confirmaciones: cuánto esperar en un depósito o retiro (whitepaper §11, reproducido en Python)

| Atacante (q) | 1 conf. | 2 conf. | 6 conf. | Confirmaciones para P < 0.1% |
|---|---|---|---|---|
| 10% | 20.5% | 5.1% | **0.024%** | 5 |
| 20% | 41.6% | 20.4% | 1.4% | 11 |
| 30% | 62.8% | 44.6% | **13.2%** | 24 |

- **[I, nuestra] Para montos que importan, esperar 6 confirmaciones (~1 h)**, como el Diplomado v3 y MB. Las "2 confirmaciones" del Diploma 2025 solo son razonables para montos pequeños.
- Salvedad de MB (apéndice B): el ataque Finney funciona con **cualquier** número de confirmaciones si el atacante preminó un bloque.

### Qué fundamentos importan y cuáles son narrativa

- **Importan, y se pueden verificar con un nodo o una API:**
  - oferta emitida (identidad de `GetBlockSubsidy`);
  - hashrate y dificultad. Ejemplo de estrés: el ajuste de **−27.94%** del 3-jul-2021 (altura 689,472), el mayor de la historia, tras la prohibición china;
  - participación de las comisiones;
  - llenado de bloques;
  - distribución de clientes y de pools.
- **MB no ofrece ningún modelo de precio.** El recuadro sobre "dinero deflacionario" termina en "It remains to be seen". Cualquier S2F, rainbow chart o ciclo es narrativa de otros recursos (grado D).

### Riesgos de protocolo que vigilar

- **Monocultivo y divergencia de clientes.** MB decía > 95% Bitcoin Core (2023). En el snapshot de nodos alcanzables de bitnodes/btcnodes (25-sep-2026 21:59 UTC, 25,521 nodos), Core es el **83.0%** y **Bitcoin Knots el 16.8%** [cálculo propio sobre los user agents].
  - [I, nuestra] La causa probable es el desacuerdo de política tras Core **30.0 (10-oct-2025)**, que subió `-datacarriersize` a 100,000 por defecto, lo que en la práctica quita el límite a OP_RETURN (notas de versión de la 30.0).
  - Es un riesgo de gobernanza y no un fork de consenso, pero vale vigilarlo.
- **Plantillas de bloque en pocos pools** (Stratum v1) → riesgo de censura.
- **Bugs de consenso con precedente:** CVE-2010-5139, CVE-2012-2459, CVE-2013-3220 y CVE-2018-17144 (wiki de Bitcoin, página de CVE).
- **Riesgo cuántico:** MB solo lo menciona de pasada en el cap. 8 ("other algorithms may provide more efficient security against quantum computers"). **No encontré** un análisis en lo que revisé.

### Ejercicio numérico (verificado en Python)

1. **2^80 hashes.** A inicios de 2023, ~2^80 por hora equivale a 335.8 EH/s, cifra consistente con MB. Hoy, a 922.7 EH/s, 2^80 toma **~21.8 min**.
   - Es una comparación de órdenes de magnitud, porque SHA-256d no es HASH160. Moraleja: los multisig nuevos deben usar P2WSH o P2TR, con 128 bits, no P2SH.
2. **Oferta máxima.** El `max_money.py` del libro, corrido en Python 3, imprime `2100000000000000.0`, porque usa `/=`. Con división entera da **2,099,999,997,690,000** sats. Es una errata de código.
3. **Último subsidio.** La época 32 (alturas 6,720,000-6,929,999) paga 1 sat; desde **6,930,000** el subsidio es 0. El cap. 12 lo dice bien; el cap. 6 ("up until block 6,720,000") es impreciso.

## 5. Contrapuntos y límites

- **Envejeció, según las notas de versión de Bitcoin Core que verifiqué:**
  - full-RBF "desactivado por defecto" (cap. 9): la **28.0 (2-oct-2024)** cambió `-mempoolfullrbf` a 1 (#30493);
  - Core "se comunica en claro" (cap. 10): el cifrado BIP324 llegó opcional en la **26.0 (6-dic-2023)** y por defecto en la **27.0 (2-abr-2024)**;
  - testnet3 como red de pruebas principal: **testnet4 (BIP94)** llegó en la 28.0;
  - Lightning como "a proposed routed network" (cap. 14): opera desde hace años;
  - "over the past three years" en el cap. 13 es un resto de la 1.ª edición.
- **Erratas internas:**
  - compact blocks "en 2015" (cap. 10). El apéndice C del propio libro dice v0.13.0, publicada el **23-ago-2016**;
  - CSV "activado en mayo de 2016" (cap. 7) contra "julio de 2016" (cap. 12); es julio;
  - 90 días = 7,760,000 s (cap. 7); son **7,776,000** s;
  - "fee rate = size divided by weight" (cap. 9); es comisión ÷ tamaño;
  - OP_EQUAL en lugar de OP_EQUALVERIFY en un listado P2PKH (cap. 4).
- **[O] Sesgo tecno-optimista:** "the perfect form of money for the internet" (cap. 1) y la idea de escalar sin más hashrate. Sobre precio, fiscalidad y regulación no dice nada útil para un inversionista.
- **El libro no cuantifica el riesgo de mercado.** Para eso están los recursos del G5 y los datos propios.

## 6. Autoexamen

1. **Un pool con 51% del hashrate, ¿puede robar tus BTC de una dirección P2WPKH? ¿Qué sí puede hacer?**
   - *Respuesta:* no puede, porque gastar exige una firma válida y los nodos rechazan bloques con transacciones inválidas.
   - Sí puede reorganizar para hacer doble gasto de **sus** transacciones y censurar (excluir) las de otros.
   - Con ~30% ya puede hacer minería egoísta.
   - *Fuente:* MB, cap. 12 y apéndice B ("an attacker can't create value out of thin air or take money that never belonged to him").
2. **Tu billetera exporta la xpub a un servidor y una clave privada hija no endurecida se filtra. ¿Qué se compromete y qué lo evita?**
   - *Respuesta:* con la xpub (clave pública + chain code) y una clave privada hija no endurecida se reconstruye la clave privada extendida del padre, y con ella todas las hermanas.
   - Lo evita la derivación **endurecida** (índices ≥ 2^31), que los estándares usan en los niveles de cuenta.
   - *Fuente:* MB, cap. 5.
3. **¿Por qué P2SH ofrece solo ~80 bits contra colisiones en un multisig y P2WSH ~128? ¿Qué implica hoy?**
   - *Respuesta:* por la paradoja del cumpleaños. Si el atacante elige parte del script, colisionar un hash de 160 bits cuesta ~2^80; con 256 bits (SHA256 en P2WSH) cuesta ~2^128.
   - La red hacía ~2^80 hashes por hora en 2023 y hoy en ~22 min. Los multisig deben usar P2WSH o P2TR.
   - *Fuente:* MB, cap. 4; cálculo propio con el hashrate de mempool.space.
4. **Define soft fork y hard fork, y calcula qué le pasa a la cadena minoritaria en un split 80/20.**
   - *Respuesta:* un soft fork **restringe** las reglas: los nodos viejos siguen aceptando los bloques nuevos. Un hard fork las **relaja**: los nodos viejos rechazan los bloques nuevos.
   - Con 20% del hashrate, la minoritaria mina un bloque cada 50 min; completar 2,016 bloques hasta su ajuste le toma 70 días (~10 semanas), con 1/5 de la capacidad.
   - La mayoritaria, con 80%, va a 12.5 min por bloque, y 2,016 bloques le toman 17.5 días.
   - *Fuente:* MB, cap. 12.

## 7. Grado de evidencia

- **A:** reglas de consenso, emisión, formatos de dirección, BIP32/39, Script, Taproot y la matemática del §11. Todo es verificable en el código, en los BIPs y en mis cálculos.
- **B:** cifras de estado de la red: nodos, costo por bloque, tamaño de UTXO, adopción de funciones. Eran ciertas en 2023 y ya envejecieron; aquí están actualizadas.
- **C-D:** opiniones sobre dinero ideal, deflación y escalabilidad sin más hashrate.
- **Global: A.** Es la referencia técnica del grupo. Cuando un recurso de divulgación (15, 20 o 29) lo contradice en mecánica, manda MB, salvo las erratas listadas en la §5.

**Estado:** estudiado el 25-sep-2026 (sección amplia). Pendiente: completar el cap. 8 (firmas: MuSig2 y FROST) y los caps. 2-3 a detalle. Síntesis en [01-bitcoin-protocolo-dinero-y-autocustodia.md](../01-bitcoin-protocolo-dinero-y-autocustodia.md).
