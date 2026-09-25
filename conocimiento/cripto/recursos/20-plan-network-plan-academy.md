# 20 · Plan ₿ Network / Plan ₿ Academy (BTC101 «El viaje de Bitcoin» y catálogo)

> Ficha de recurso · Grupo G1 (Bitcoin) · Estudiada el 25-sep-2026 por `analista-cripto` · **Acceso: sección**: BTC101 íntegro en español, BTC102 por secciones y catálogo de 50 cursos · **Grado global: C**. **B** en prácticas de autocustodia y herencia, que coinciden con MB; **D** en ciclos, precio y política.
>
> **Etiquetas:**
> - **[H]** hecho con fuente y sección;
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
| Año | Plataforma viva. BTC101 se publicó el 29-abr-2023 y su versión en español la revisaron el 6-nov-2025. Último commit del repo que usé: `3a00990`, 25-sep-2026 ("add min303"; publica gratis el curso MIN303 de minería) |
| Autor | Plan ₿ Network. Según su página "About", es "un proyecto común de tres entidades" que no nombra. Directivos: Giacomo Zucco (director y cofundador; también colaboró con Mi Primer Bitcoin, recurso 15), Rogzy (cofundador y producto; profesor de BTC101) y Asi0 |
| Tipo | Plataforma de cursos abiertos. El repo tiene **50 cursos** (`course.yml`) sobre Bitcoin, negocio, minería, protocolo, seguridad y ciencias sociales |
| Nivel | Principiante a experto. Ejemplos: BTC101 (7 h, principiante), BTC102 (14 h), BTC202 nodo (10 h), BTC204 privacidad (16 h), CYP201 arquitectura de billeteras (10 h), CYP302 criptografía (9 h), LNP201 teoría de Lightning (6 h), MIN303 minería (16 h), CSV402 RGB, CSV404 Taproot Assets, ECO201/205 escuela austriaca, BIZ205 (102 h) |
| Costo | Mayormente gratis. Contenido CC BY-SA 4.0. A los revisores de traducciones se les paga una "reward" (modelo *value-for-value*) |
| Idioma | Multilingüe; leí la versión en español |
| URL | https://planb.academy/es · Repo: https://github.com/PlanB-Network/bitcoin-educational-content |
| **Conflictos de interés** | Es un proyecto de empresas del ecosistema bitcoin-only; no encontré fuentes de financiamiento en lo que revisé. El README dice inspirarse en el *Cypherpunk Manifesto* y busca "revolucionar el mundo". BTC102 lo admite: "No existe la información puramente neutral. Incluso este curso, BTC102, tiene un objetivo claro". Recomienda plataformas y marcas concretas (Kraken, Bitstamp, Paymium, Ledger, Coldcard, Jade, entre otras) y **no declara si tiene relación comercial con ellas**. Tiene curso de afiliación política (SOC104) y cursos de escuela austriaca |

## 2. Acceso real

- **Repo oficial.** Clon *sparse* en el scratchpad el 25-sep-2026, commit `3a00990`, con licencia CC BY-SA 4.0.
- **Leído completo:** BTC101 en español, sus 25 capítulos.
- **BTC102, leídas completas estas secciones:**
  - resumen;
  - estafas;
  - industria (exchanges, ecosistema, Bitcoin Core);
  - hodler.
  - La herencia la hojeé; el resto, por encabezados.
- **Por encabezados:** CYP201 y LNP201.
- **Catálogo:** extraje título, nivel, horas y fecha de los 50 `course.yml`.
- **Página "About":** la leí con WebFetch porque se renderiza con JavaScript.
- **Nivel: sección.** No hice los cursos avanzados (BTC202/204, CYP302, MIN303, SID, CSV).

## 3. Lo esencial

### Dinero e historia (BTC101)

- **[H] Prehistoria cypherpunk:**
  - Eric Hughes, *A Cypherpunk's Manifesto* (1993); Tim May (1992); John Perry Barlow (1996);
  - DigiCash y b-money como antecedentes.
  - Da bien el año del manifiesto (1993); el Diploma 2025 dice 1992.
- **[H] Hiperinflaciones con cifras que coinciden con la tabla de Hanke-Krus:**
  - Weimar, oct-1923: **29,500% mensual**, 20.9% diario, precios que se duplican cada ~3.7 días;
  - Hungría, jul-1946: 4.19 × 10^16 % mensual, **207% diario**, duplicación cada ~15 h;
  - Zimbabue, nov-2008: 79,600 millones % mensual.
  - [H, cálculo propio] 296^(1/30) − 1 = 20.9%; con 4.19 × 10^14 se obtiene 3.07× diario, es decir +207%.
- **[H con matiz] "El dólar perdió 98% de su valor en 100 años"** (§ Monedas fiduciarias).
  - Con el IPC de EUA, 1923-2023 es ≈ **−94%** y 1913-2023 ≈ **−97%** (30.8×). El 98% es exagerado si se mide con IPC, aunque es plausible medido en oro.
- **[O] Visión austriaca y normativa.** "Ningún individuo o grupo puede crear dinero"; "moneda que depende de un tercero… defectuosa".
  - Cita a Voltaire con una frase de **atribución dudosa** ("el papel moneda vuelve a su valor intrínseco, cero").

### Oferta de 21 M (BTC101, § "21 millones")

- **[H] La tabla de halvings con oferta acumulada es correcta:** 10.5 M, 15.75 M, 18.375 M, 19.6875 M, 20.34375 M, 20.671875 M…
- **[H] Enseña a auditar la oferta con un nodo propio** (`bitcoin-cli gettxoutsetinfo`). El ejemplo de la altura 710,560 tiene un hash ilustrativo.
- **[H] Tres errores en el texto de la curva de emisión, contra mi cálculo con `GetBlockSubsidy` y fechas de blockstream.info:**
  - "en 2022 había ~18.5 M": 18.5 M se alcanzó en la altura ~650,000, el **25-sep-2020**; en 2022 la oferta iba de 18.92 a 19.25 M;
  - "en 2025 habrá ~19.5 M (93%)": 19.5 M se alcanzó en la altura ~810,000, el **30-sep-2023**; durante 2025 iba de ~19.80 a 19.97 M;
  - "en 2037, 20.4 M": 20.4 M llegará hacia la altura ~1,086,000 (fines de 2028); en 2037 habrá ≈ **20.86 M**.

### Monederos y autocustodia (lo mejor del recurso)

- **[H] Escala de seguridad en 5 niveles** (§ Monederos Bitcoin y seguridad):
  - 0: custodia de terceros ("el tercero puede restringir el acceso, como un banco");
  - 1: billetera caliente;
  - 2: billetera de hardware;
  - 3: hardware con passphrase (respaldar ambas por separado);
  - 4: multisig para montos grandes.
  - La advertencia: el exceso de complejidad también es riesgo de pérdida.
- **[H] Protocolo de semilla.**
  - Sin fotos ni teclearla en la computadora o el teléfono; en papel o **acero**, dos copias en lugares distintos.
  - Desconfiar de billeteras sin frase semilla.
  - Plan de sucesión: carta manuscrita, notario sin darle las llaves; remite al libro de Pamela Morgan.
- **[H con error] "Frase secreta de recuperación (clave privada)".** Confunde semilla y clave privada: la frase codifica la **entropía** de la que se derivan las claves (MB, cap. 5).
  - "Desde 2017 se representa con 12-24 palabras": BIP39 es de **2013**.
  - "Adivinarla es 1 entre 2^256": una frase de 12 palabras tiene **128 bits** de entropía.
- **[H] "Evite dejar sus bitcoins en plataformas de intercambio"** (resumen de BTC101).
  - BTC102 detalla tres riesgos de exchange: **hackeo** (Mt. Gox), **embargo o congelamiento gubernamental** y **quiebra o fraude** (FTX). "Retira siempre tus fondos a una wallet personal lo antes posible."

### Protocolo y minería

- **[H con error] "El 31-oct-2008 Satoshi envió el whitepaper a la lista de cypherpunks"** (§ Lanzamiento). Fue la **Cryptography Mailing List** de metzdowd.com.
  - El resto de la cronología es correcto: génesis el 3-ene-2009, bloque 170 a Hal Finney, pizza el 22-may-2010, último post de Satoshi el 12-dic-2010.
- **[H] Disponibilidad de 99.988% desde el inicio** (bitcoinuptime.com). A diferencia del Diplomado v3 y de su propio BTC102 ("más de una década sin tiempos de inactividad"), **reconoce caídas**.
- **[H con errores de unidades]:**
  - "hash de **256 caracteres**": son 256 bits, 64 caracteres hexadecimales;
  - "el hashrate superó los **500 TH/s** = 500,000 billones de intentos por segundo": la red iba en cientos de **EH/s** y hoy en ~922.7 EH/s ≈ 9.2 × 10^20 H/s;
  - "bloque de 1 MB ampliado a 4 MB con SegWit": son 4 M unidades de peso. Más adelante, en la sección de Lightning, dice "bloques limitados a 1 MB" y **se contradice**.
- **[H] Error de seguridad: "Incluso con un ataque del 51%, la red seguiría siendo segura porque el atacante debe gastar tanta energía como todos los mineros"** (§ Mineros).
  - Es engañoso: con mayoría se puede hacer doble gasto de transacciones propias y censurar (MB, cap. 12; whitepaper, §11).
- **[H] Nodos.**
  - "~45,000 nodos en sep-2023 (bitnodes)"; blockchain de ~500 GB; nodo en Raspberry Pi 4 con SSD de 2 TB.
  - Argumenta que bloques 100 veces mayores (50 TB) centralizarían la validación [I del autor, coherente con MB].

### Mercado, compra y regulación

- **[H] Advertencias explícitas** (§ ahorro):
  - "invierta solo lo que pueda perder";
  - "puede caer hasta 0";
  - Plan ₿ "no da asesoría de inversión".
  - BTC102 "desaconseja encarecidamente el trading… apalancamiento y derivados".
- **[O/I] Ciclos.** "Equivalentes a la duración entre halvings, quizá porque el halving actúa como detonante"; "tendencia al alza de forma casi mecánica".
  - No presenta ninguna prueba: grado D.
- **[H] El Salvador.** Ley de enero de 2025 que quitó el curso legal (aceptación voluntaria). La atribuye "supuestamente" a la presión del FMI. Es un dato que el Diplomado v3 no tenía.
- **[O, riesgo legal] "Aconsejamos a los usuarios avanzados evitar plataformas KYC."**
  - Lista entre las opciones de compra "plataformas ilegales y no reguladas", alternativas sin KYC (Bisq, RoboSats, Peach, HodlHodl) y cajeros.
- **[H] Lightning y más allá (texto actualizado en 2025):**
  - capacidad frente a liquidez de un canal, HTLC atómico y penalización;
  - billeteras custodiales frente a no custodiales (Phoenix, Zeus);
  - implementaciones LND, Core Lightning, Eclair y LDK;
  - Liquid (federación identificada), Ark (Burak, may-2023; "aún joven"), RGB y Taproot Assets.

## 4. Qué cambia para invertir

- **La escala de 5 niveles aplicada a nuestra cuenta [I, nuestra]:**
  - `arena-claude-binance` está en el **nivel 0** (custodia de terceros), a propósito: es una cuenta de trading spot con filtro SMA200 y cortacircuitos que exigen vender rápido.
  - Plan ₿ y MB coinciden en que es el nivel más frágil.
  - Por eso la cuenta tiene tope de 10,000 MXN, la pérdida máxima es de 5,000 MXN y la contingencia (Bitso, SPEI, disparadores) debe **probarse antes del 2-oct**, como exige la decisión.
- **Los tres riesgos de exchange de BTC102 son las tres ramas de la contingencia [I, nuestra]:**

  | Riesgo | Respuesta |
  |---|---|
  | Hackeo o insolvencia del exchange | La contingencia pone el tope de tamaño y el retiro a otra plataforma. **Un congelamiento total arriesga los 10,000 MXN**; el tope no cubre el riesgo de contraparte, como ya dice la decisión |
  | Embargo o congelamiento (OFAC, DOJ, regulador) | Disparadores definidos en la decisión |
  | Bloqueo del riel fiat (SPEI por Medá caído más de 48 h) | Mover BTC on-chain a Bitso y retirar por SPEI desde ahí |

- **Autocustodia de largo plazo.** Si el dueño decidiera guardar BTC fuera del torneo, el protocolo mínimo es el nivel 2 o 3: hardware con semilla en acero y sucesión documentada.
- **No seguir el consejo "sin KYC".** En México el régimen de actividad vulnerable (LFPIORPI, art. 17, fr. XVI) y la fiscalidad hacen que operar sin identificación sea un riesgo legal y reputacional para el dueño.
- **Qué fundamentos importan y cuáles son narrativa.**
  - Se puede verificar: la oferta con `gettxoutsetinfo` en un nodo propio (grado A).
  - No se puede verificar: los ciclos atados al halving y la "tendencia casi mecánica" (grado D).
  - Nuestra evidencia de retornos post-halving es n = 3 y decreciente: +287%, +559% y +31% a 12 meses (ficha 15).
- **Riesgo de protocolo que Plan ₿ minimiza.** Presenta la guerra del tamaño de bloque como triunfo de "nodos y usuarios" y BTC102 menciona Bitcoin Knots como alternativa.
  - [I, nuestra] Hoy Knots es el **16.8%** de 25,521 nodos alcanzables (snapshot de bitnodes/btcnodes del 25-sep-2026).
  - La diversidad de clientes es sana, pero una disputa de política puede escalar a riesgo de fork. Conviene vigilarla (ficha 16, §4).

### Ejercicio numérico (verificado en Python)

- **¿Qué fecha corresponde a cada cifra de oferta?** Busqué la altura a la que la oferta teórica cruza cada umbral y su fecha en blockstream.info:
  - **18.5 M** → altura ~650,000, el 25-sep-2020;
  - **19.5 M** → ~810,000, el 30-sep-2023;
  - **20.0 M** → ~940,000, el **9-mar-2026**;
  - **20.4 M** → ~1,086,000, después del halving de 2028;
  - **2037** (altura ~1,522,000) → **20.86 M**.
- **Conclusión:** las tres cifras del texto de BTC101 están corridas 2-10 años. Conviene usar siempre la función de subsidio, no las cifras redondeadas de los cursos.

## 5. Contrapuntos y límites

- **Promoción e ideología declaradas.** Cursos de escuela austriaca y de afiliación política, más "la mayoría de las criptodivisas son poco más que estafas" [O] y "Bitcoin ya no puede detenerse ni censurarse" [O].
  - Para el inversionista, el punto de control real son las **rampas fiat y los exchanges**, que sí se regulan. Plan ₿ minimiza ese punto: "regular exchanges tiene impacto marginal".
- **Cifras sin fuente o envejecidas:**
  - "2,400 millones sin cuenta bancaria": Global Findex 2021 da ~1,400 millones de adultos;
  - "más del 80% de los empleos desaparecerá por IA", sin fuente;
  - "~45,000 nodos" en sep-2023: es una métrica distinta a los "~10,000 que escuchan" de MB. Los números de nodos dependen del método.
- **Inconsistencias internas:**
  - disponibilidad de 99.988% (BTC101) contra "sin tiempos de inactividad" (BTC102);
  - 4 MB contra 1 MB;
  - lista de mantenedores de Bitcoin Core en 2025 (Stepanov, Ford, Chow, Zhao, Ofsky) que **no verifiqué**.
- **Sesgo de supervivencia.** "El hodling ha sido históricamente el método más rentable para no profesionales" depende del punto de entrada: quien compró en dic-2017 esperó ~3 años para recuperar.

## 6. Autoexamen

1. **Plan ₿ dice que adivinar una frase semilla es "1 entre 2^256". ¿Cuál es el espacio real de una frase BIP39 de 12 palabras y por qué?**
   - *Respuesta:* 12 palabras × 11 bits = 132 bits: **128 de entropía + 4 de checksum**. El espacio real es 2^128; con 24 palabras, 2^256.
   - Además, la seguridad de cualquier clave pública de secp256k1 es ~128 bits, así que más entropía casi no suma.
   - *Fuente:* MB, cap. 5; BTC101, § Monederos.
2. **¿Qué tres riesgos de exchange enumera BTC102 y con qué ejemplos?**
   - *Respuesta:* hackeo (Mt. Gox), embargo o congelamiento gubernamental, y quiebra o fraude (FTX). La recomendación es retirar a una billetera personal cuanto antes.
   - *Fuente:* BTC102, § industria/exchanges.
3. **Corrige la frase "incluso con un ataque del 51% la red seguiría segura".**
   - *Respuesta:* con más de 50% del hashrate se puede reorganizar la cadena para hacer doble gasto de transacciones propias y censurar otras. No se pueden falsificar firmas ni violar reglas de consenso que los nodos validan.
   - *Fuente:* MB, cap. 12 y apéndice B.
4. **¿Cuántos BTC habrá en 2037 y en qué altura se superan los 20 M?**
   - *Respuesta:* ≈ 20.86 M en 2037 (altura ~1,522,000). Los 20 M se cruzaron en la altura ~940,000, el 9-mar-2026.
   - *Fuente:* cálculo propio con `GetBlockSubsidy`; fecha del bloque 940,000 en blockstream.info.

## 7. Grado de evidencia

- **B:** autocustodia, semilla, niveles de seguridad, sucesión y riesgos de exchange. Coinciden con MB, caps. 5 y 13.
- **B-C:** historia e hiperinflaciones; las cifras coinciden con Hanke-Krus, aunque hay una cita apócrifa.
- **C:** oferta (tabla correcta, texto equivocado) y protocolo con errores de unidades.
- **D:** ciclos, precio, "tendencia mecánica", política y consejos sin KYC.
- **Global: C.** Buen mapa de temas y excelente para custodia práctica; cada cifra hay que verificarla.

**Estado:** estudiado el 25-sep-2026 (sección). Pendiente para la ruta de doctorado: CYP201 (arquitectura de billeteras), BTC204 (privacidad), LNP201 y MIN303 (publicado el 25-sep-2026). Síntesis en [01-bitcoin-protocolo-dinero-y-autocustodia.md](../01-bitcoin-protocolo-dinero-y-autocustodia.md).
