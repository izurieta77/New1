# 01 · Bitcoin: protocolo, dinero y autocustodia (síntesis del grupo G1)

> Capítulo de síntesis · Grupo G1 (Bitcoin) · Escrito el 25-sep-2026 por `analista-cripto` · Integra los recursos **15, 16, 20, 28 y 29** del índice del dueño. Todas las cifras están verificadas con cálculo propio en Python, con datos públicos o con una segunda lectura de la fuente; si algo no lo verifiqué, lo digo.
>
> **Etiquetas:**
> - **[H]** hecho con fuente;
> - **[I]** inferencia (nuestra, salvo que diga otra cosa);
> - **[O]** opinión de un autor.
>
> **Grados:**
> - **A:** identidad o dato oficial;
> - **B:** evidencia sólida con salvedades;
> - **C:** muestra corta o no reproducible;
> - **D:** narrativa sin historial auditado.

## Fichas integradas

| # | Recurso | Acceso real | Grado | Para qué sirve |
|---|---|---|---|---|
| 15 | [Diplomado en Bitcoin v3.0](recursos/15-diplomado-en-bitcoin.md) | Íntegro (texto) | C | Vocabulario básico; cómo NO enseñar custodia (billeteras de papel) |
| 16 | [Mastering Bitcoin, 3.ª ed.](recursos/16-mastering-bitcoin-3-a-edicion.md) | Sección amplia: 10 de 14 capítulos y apéndice B | **A** | La referencia técnica: manda en mecánica |
| 20 | [Plan ₿ Academy](recursos/20-plan-network-plan-academy.md) | Sección: BTC101 íntegro, BTC102 por secciones | C (B en custodia) | Protocolo práctico de semilla, niveles de seguridad y herencia |
| 28 | [Dinero Roto (Broken Money)](recursos/28-dinero-roto.md) | Sección: caps. 1-8 de 30 + resumen del resto | B-C | Por qué existe demanda de Bitcoin; marco de "quién controla el libro contable" |
| 29 | [Diplomado Bitcoin 2025](recursos/29-diplomado-bitcoin-edicion-2025.md) | Íntegro de un sustituto (nov-2025); el PDF 2025 no fue accesible | C-D | Catálogo de errores comunes de divulgación |

## 1. Mapa por niveles

### Licenciatura: qué es, cómo se usa y cómo se guarda

| Tema | Lo que hay que saber | Dónde |
|---|---|---|
| Dinero | Funciones (reserva, medio, unidad de cuenta); atributos (divisible, portable, durable, fungible, verificable, escaso); preferencia temporal; fiat y banca central; EO 6102 y la devaluación de 20.67 a 35 dólares (−40.9%) | 15 caps. 1-3; 29 caps. 1-4; 28 caps. 1-2 y 7 |
| Qué resuelve Bitcoin | Doble gasto sin tercero de confianza: prueba de trabajo + cadena de bloques + reglas validadas por cada nodo | 16 cap. 1; 15 clase 4; 20 BTC101 |
| Emisión | 50 BTC → halving cada 210,000 bloques → máximo de 20,999,999.9769 BTC; 4 halvings: 28-nov-2012, 9-jul-2016, 11-may-2020, 20-abr-2024 | 15 pp. 90-92; 16 cap. 12; [tabla de la ficha 15](recursos/15-diplomado-en-bitcoin.md) |
| Billetera | Una billetera guarda **llaves**, no monedas. Semilla de 12-24 palabras; respaldo en acero; nada de fotos ni billeteras de papel | 20 BTC101; 16 caps. 4-5 |
| Custodia | "Not your keys, not your coins"; los exchanges son el nivel 0 (hackeo, congelamiento, quiebra) | 16 caps. 1 y 13; 20 BTC102; 29 §6.1 |
| Confirmaciones | La reversión cae exponencialmente con cada bloque; 6 confirmaciones para montos relevantes | 15 p. 84; 16 cap. 12 |
| Lightning | Canales de pago de 2 partes; rápido y barato; "menos seguro" que on-chain; limitado por la liquidez | 15 pp. 72-73; 29 cap. 7; 20 BTC101 |

### Maestría: mecanismos

| Tema | Lo que hay que saber | Dónde |
|---|---|---|
| Llaves y direcciones | secp256k1 (SEC 2, no NIST); P2PKH → P2SH (80 bits contra colisiones) → P2WPKH/P2WSH (bech32) → P2TR (bech32m, ≥ 128 bits); se firma, no se cifra | 16 cap. 4 |
| Billeteras HD | BIP32 (derivación endurecida contra la fuga de xpub + una clave hija); BIP39 (128 bits + 4 de checksum en 12 palabras; PBKDF2 con 2,048 rondas; passphrase fuera del checksum); descriptores (BIPs 380-386 y 389) | 16 cap. 5; 20 BTC101 |
| Transacciones | UTXO; peso (4 M WU por bloque; 1 vB = 4 WU); madurez de coinbase de 100 bloques; timelocks (CLTV, CSV); polvo (546 sats) | 16 caps. 6-7 |
| Comisiones | Subasta por espacio de bloque; RBF (full-RBF por defecto desde Core 28.0, 2-oct-2024); CPFP; mempool local con expiración de 336 h | 16 cap. 9 + notas de versión de Core |
| Minería y dificultad | Ajuste cada 2,016 bloques, con error de uno (2,015 intervalos, +0.05%) y límite de 4×; pools y Stratum v1/v2; 51% = doble gasto propio y censura, no robo | 16 cap. 12 y apéndice B |
| Forks | Soft fork = restringe (compatible); hard fork = relaja (split). Activaciones: BIP9 (95%), BIP148 (UASF), BIP8, Speedy Trial | 16 cap. 12 |
| Teoría monetaria | Dinero = libro contable; teoría mercancía frente a crédito; S2F como medida de escasez (oro ~50-67; BTC ≈ 122 hoy) | 28 caps. 2-4 |

### Doctorado: donde está el riesgo fino

| Tema | Lo que hay que saber | Dónde |
|---|---|---|
| Whitepaper §11 y erratas | P(q = 0.1, z = 6) = 0.024%; P(q = 0.3, z = 6) = 13.2%; minería egoísta ~30%; ataque Finney con cualquier número de confirmaciones; "longest chain" → cadena con más trabajo | 16 apéndice B; [banco de examen](examen/banco-g1-bitcoin.md) |
| Taproot y Tapscript | MAST + gasto por clave indistinguible; Schnorr (BIP340) con validación por lotes; OP_CHECKSIGADD; OP_SUCCESSx para soft forks futuros; multisig sin script = sin rendición de cuentas | 16 caps. 7-8 |
| Seguridad económica | Subsidio de 450 BTC/día ≈ US$37.8 M; comisiones 0.63-0.90% de la recompensa; fee sniping "inevitable" cuando dominen las comisiones | 16 caps. 9 y 12 + datos del 25-sep-2026 |
| Canales | Revocación asimétrica con CSV; índice de estado de 48 bits; hay que vigilar la cadena (watchtowers); HTLC; enrutamiento cebolla; liquidez direccional | 16 cap. 14; 28 p. 354 (vía reseña) |
| Gobernanza | "Status quo is the stable state"; los nodos hacen cumplir los 21 M; monocultivo de cliente; guerra del tamaño de bloque (Alden, pequeños bloques, frente a la reseña de "Conflated", grandes bloques) | 16 cap. 12; 28 |
| Historia monetaria fina | Jevons (1875): reservas de 4-7% (apalancamiento de 14-25×); corridas bancarias (gana quien retira primero); hawala como red de canales; brecha entre velocidad de transacción y de liquidación | 28 caps. 5-8 |

### Frontera 2025-2026 (verificado en fuentes primarias el 25-sep-2026)

- **[H] Política de Bitcoin Core** (notas de versión en GitHub y fechas en bitcoincore.org):
  - **29.1 (4-sep-2025):** mínimo de retransmisión por defecto de 0.1 sat/vB;
  - **30.0 (10-oct-2025):** `-datacarriersize` = 100,000, lo que en la práctica quita el límite a OP_RETURN, y se permiten varias salidas OP_RETURN;
  - **31.0 (19-abr-2026)** es la versión mayor más reciente.
- **[H] Diversidad de clientes.** Snapshot de bitnodes/btcnodes del 25-sep-2026 21:59 UTC, sobre 25,521 nodos alcanzables: **Core 83.0%, Knots 16.8%** (cálculo propio). En 2023, MB hablaba de más de 95% Core.
- **[H] Oferta.** El BTC número 20,000,000 (oferta teórica) se emitió hacia la altura **~940,000, el 9-mar-2026**. Próximo halving: altura 1,050,000, **abr-may-2028**.
- **[H] Segunda capa (Plan ₿, texto de 2025):** Ark (may-2023, "joven"), RGB, Taproot Assets y Liquid. Ninguno cambia la oferta de BTC. Todos agregan supuestos de confianza o de datos.
- **Riesgo cuántico: no lo encontré en lo que revisé.** MB solo lo menciona de pasada (cap. 8). Es tema pendiente de otra fuente.

## 2. Las 10 ideas que más importan para invertir en BTC

1. **La oferta es el único parámetro que se verifica con certeza; el precio no.**
   - A la altura 968,589 (25-sep-2026) la oferta teórica es **20,089,343.75 BTC**, el 95.66% del máximo.
   - La emisión es de ≈ 164,000 BTC al año (0.82%) y bajará a ≈ 82,000 (0.40%) tras el halving de la altura 1,050,000 (**ETA 13-abr a 10-may-2028**).
   - El halving es público y predecible. Después de cada uno, el rendimiento a 12 meses fue de **+287%, +559% y +31%**: n = 3 y decreciente, **grado C**. **No hay halving en la temporada del torneo.** *(15, 16, 29; cálculo propio)*
2. **La caída grande es la norma.**
   - **−83.4%** (2017-18) y **−76.6%** (2021-22), sobre cierres; −37.2% en un día (12-mar-2020); volatilidad anualizada de 51.5%.
   - Hoy estamos −32.8% desde el máximo de cierre (US$124,752.53, 6-oct-2025).
   - Los cursos lo subestiman ("hasta 80%", "hasta 20% en un día") o lo niegan ("no es inversión, es ahorro seguro"). El tamaño de la posición lo fijan el tope de pérdida y los cortacircuitos, no la tesis. *(15, 20, 29; datos de Yahoo)*
3. **Custodia es saber quién controla el libro contable.**
   - En Binance tenemos un **asiento en el libro privado** de un exchange que no está supervisado en México (Ley Fintech, art. 30; Circular 4/2019).
   - MB: "don't outsource validation". BTC102: hackeo, embargo, quiebra. Alden: en una corrida gana quien retira primero.
   - Por eso la contingencia (Bitso, SPEI, disparadores) debe **probarse antes del 2-oct** y activarse con **señales tempranas**. *(16 cap. 13; 20; 28 cap. 6)*
4. **Las confirmaciones compran seguridad a un precio conocido.**
   - Con un atacante de 10% del hashrate, la probabilidad de reversión es 5.1% con 2 confirmaciones y **0.024%** con 6. Con uno de 30%, 13.2% con 6, y hacen falta 24 para bajar de 0.1%.
   - En depósitos y retiros de la contingencia: **6 confirmaciones**. El "2 bastan" del Diploma 2025 es para montos pequeños. *(16 apéndice B; whitepaper §11 reproducido)*
5. **La seguridad hoy sale en más de 99% del subsidio.**
   - 450 BTC/día ≈ **US$37.8 M/día** (≈ US$13.8 mil M al año). Las comisiones son solo **0.63%** (30 días) a **0.90%** (144 bloques) de la recompensa.
   - Core 29.1 bajó el mínimo de retransmisión a 0.1 sat/vB.
   - Cada halving parte el subsidio a la mitad. A 10-20 años, la seguridad en dólares exige precio o comisiones más altos; si no, aparece el fee sniping que MB anticipa. **No es un riesgo de 4 meses; sí de la tesis.** *(16 caps. 9 y 12; mempool.space)*
6. **Los 21 M los hacen cumplir los nodos que validan, no "el código".**
   - Un soft fork solo restringe y el status quo es estable. Por eso la oferta es creíble.
   - Pero hay **riesgo de gobernanza**: la guerra del tamaño de bloque (2015-17) y la disputa de OP_RETURN (Core 30.0), que hoy se ve en **Knots con 16.8%** de los nodos alcanzables.
   - Un split contencioso sería un evento de riesgo de precio: con 20% del hashrate, la cadena minoritaria tendría bloques de 50 min durante ~10 semanas. *(16 cap. 12; bitnodes)*
7. **Qué es fundamento y qué es narrativa.**
   - **Fundamento verificable (grado A):** oferta emitida, hashrate y dificultad (por ejemplo, el ajuste de −27.94% del 3-jul-2021 tras la prohibición china), porcentaje de comisiones, llenado de bloques, distribución de clientes y pools.
   - **Narrativa (grado D):** rainbow chart, S2F como **modelo de precio** (el S2F solo mide escasez: BTC ≈ 122 frente a oro ~50-67), "hiperbitcoinización", "el halving sube el precio" y "tendencia casi mecánica". *(15, 16, 20, 28, 29)*
8. **La tesis de largo plazo (Alden) explica la demanda, no el timing.**
   - Bitcoin sería el primer **activo al portador escaso que liquida tan rápido como se transacciona**. Cierra la brecha que, desde el telégrafo, obligó a confiar en bancos y bancos centrales.
   - Da la razón de la demanda estructural: 160 monedas fiat, controles de capital, represión financiera. No dice cuándo sube el precio.
   - La autora está en el consejo de Swan. **Grado C como tesis y D como señal.** *(28)*
9. **Los riesgos técnicos ya ocurrieron; no son teóricos.**
   - Bugs de consenso: CVE-2010-5139 (inflación por desbordamiento), CVE-2012-2459 (Merkle), CVE-2013-3220 (división 0.7/0.8) y CVE-2018-17144 (inflación en versiones anteriores a 0.16.3).
   - Además: monocultivo de cliente, plantillas de bloque en pocos pools (Stratum v1) y más de 100 ataques físicos a poseedores documentados por Lopp (MB).
   - El riesgo cuántico **no está cubierto** por estos recursos. *(16; wiki de Bitcoin, página de CVE)*
10. **Las fuentes educativas de Bitcoin son promotoras: hay que verificar cada cifra.**
    - Las financian actores del sector (IBEX Mercado, Block, HRF, Swan) y tienen misión *bitcoin-only*.
    - Encontré decenas de errores numéricos o conceptuales: oferta en Plan ₿ corrida 2-10 años, mempool de 72 h, 2.5 mil millones de no bancarizados, "el 51% sigue siendo seguro", "cifrar", tabla de halvings corrida una época.
    - **Regla:** en mecánica manda MB y el código; en cifras, el cálculo propio; en precio, nadie de este grupo pasa de grado C.

## 3. Contradicciones entre recursos

| Tema | Postura A | Postura B | Qué es correcto (verificado) |
|---|---|---|---|
| Billeteras de papel | 15 (p. 56): "entre las formas más seguras"; 29 las lista como tipo de billetera | 16 (cap. 4): "OBSOLETE… DO NOT USE" | **16.** No usar |
| Confirmaciones | 29 (§6.4): "al menos 2 (20 min)" | 15 (p. 84), 20 y 16: 6 para montos altos | Depende de q y del monto; con q = 0.1, 2 conf. = 5.1% y 6 conf. = 0.024%. **6** |
| Expiración de la mempool | 15 (p. 66) y 29 (§9.2): "72 horas" | Bitcoin Core: 336 h desde 0.14.0 (8-mar-2017) | **336 h**; 29 lo corrigió en 2026.04 |
| Firma frente a cifrado | 15 (p. 59): "cifrar/descifrar"; 29 (§8.1): "clave pública del **receptor**" | 16 (cap. 4): se firma, no se cifra; se verifica con la clave de quien gasta | **16** |
| Oferta por año | 20 (BTC101): 18.5 M en 2022; 19.5 M en 2025; 20.4 M en 2037 | Cálculo propio: 18.5 M el 25-sep-2020; 19.5 M el 30-sep-2023; 20.86 M en 2037 | **Cálculo propio**; la tabla de halvings de 20 sí es correcta |
| Último bloque con subsidio | 16 (cap. 6): "up until block 6,720,000" | 16 (cap. 12) y cálculo: la época 32 (6,720,000-6,929,999) paga 1 sat; cero desde 6,930,000 | **Cap. 12** |
| Porcentaje emitido en 2028 | 29 (versión 26.04): 98.44% en la altura 1,050,000 | Cálculo: 96.875% al llegar; 98.4375% es la altura 1,260,000 | **Cálculo** |
| Primer bloque de 25 BTC | 15 (p. 90): "bloque 210,001" | `GetBlockSubsidy`: altura 210,000 | **210,000** |
| Ataque del 51% | 20 (BTC101): "la red seguiría segura"; 15 (p. 48): "la criptografía lo previene" | 16 (cap. 12 y apéndice B): doble gasto propio y censura; minería egoísta desde ~30% | **16** |
| Disponibilidad de la red | 15 (p. 97): "ningún ataque la interrumpió"; 29: "decenas de miles de ataques, nadie lo detiene"; 20 (BTC102): "sin tiempos de inactividad" | 20 (BTC101): 99.988% (bitcoinuptime); 16: fork de 2013; wiki: CVE de 2010 y 2018 | **Hubo fallas**: BTC101 y MB |
| Halving y precio | 29 (§9.1): "históricamente, alzas significativas"; 15: rainbow chart; 20: "ciclos, quizá por el halving" | 16: sin modelo de precio ("it remains to be seen"); datos: n = 3 decreciente | **Grado C como mucho**; 29 lo suavizó en 2026.04 |
| ¿Es inversión? | 29 (§5.2): "NO es inversión, es ahorro SEGURO" | 20: "invierta solo lo que pueda perder", "puede caer a 0"; datos: −83% y −77% | **20 y los datos** |
| Nodos | 16 (2023): "~10,000 que escuchan, > 95% Core" | 20: "~45,000 (bitnodes, sep-2023)"; hoy: 25,521 alcanzables, 83% Core y 16.8% Knots | Son **métricas distintas**; hay que citar siempre método y fecha |
| Tamaño de bloque | 15 (p. 82): "~2.5 MB"; 20: "1 MB → 4 MB" y luego "limitados a 1 MB" | 16: límite de 4,000,000 WU; el bloque 968,589 pesó 3,993,589 WU y 1.707 MB | **16** |
| Origen del dinero | 15 y 29: del trueque al dinero, versión de Smith | 28 (cap. 4): el crédito es anterior a la moneda; Smith se equivocó en el orden (Graeber, Selgin) | **28**, aunque Alden conserva el papel del dinero mercancía entre extraños |
| Escala numérica en español | 15 (p. 96): "Tera = **trillón**", un error | 28: escala corta declarada ("billón" = 10^9) | En español correcto, 10^12 = **billón**; hay que leer 28 con cuidado |
| Escalar: capas o bloques | 28 (pp. 341, 348, según la reseña): capas; la base no es para comprar café | Reseña "Conflated": las capas reintroducen custodios; ~200 M transacciones al año no alcanzan | **Debate abierto**: la capacidad es ≈ 180 M transacciones al año (cálculo propio) |
| KYC | 20 (BTC101): "a los avanzados, evitar KYC" | Nuestra cuenta: Binance + Medá con KYC; LFPIORPI en México | Para el dueño: **KYC y cumplimiento** |
| Cita de "nerd money" | 29 (§6.0): de Satoshi | Circula atribuida a Antonopoulos | **Atribución dudosa**; no la encontré en Satoshi |

## 4. Tabla de datos verificados (25-sep-2026, ~21:55 UTC)

| Dato | Valor | Fuente / método |
|---|---|---|
| Altura | 968,589 | mempool.space y blockstream.info coinciden |
| Oferta teórica | 20,089,343.75 BTC (95.66%); 20,089,293.75 sin los 50 BTC de génesis | `GetBlockSubsidy` en Python |
| Máximo | 2,099,999,997,690,000 sats = 20,999,999.9769 BTC | Ídem; MB cap. 12 |
| 99% emitido | Altura 1,411,200 (~2035) | Ídem; MB cap. 1 |
| Subsidio / próximo halving | 3.125 BTC / altura 1,050,000; faltan 81,411 bloques; 13-abr-2028 (600 s) a 10-may-2028 (628.9 s) | Cálculo propio |
| Hashrate / dificultad | ~922.7 EH/s / 132,757,073,449,487.5; próximo ajuste en 969,696, estimado en −4.49% | mempool.space |
| Comisiones / recompensa | 0.90% (144 bloques); 0.63% (4,320 bloques) | mempool.space |
| Subsidio en USD | 450 BTC/día × US$84,045.67 = US$37.8 M/día | Precio de referencia de la decisión del 25-sep-2026 |
| Mayor ajuste de dificultad a la baja | −27.94% (3-jul-2021, altura 689,472) | mempool.space (ajustes) |
| Nodos alcanzables | 25,521; Core 83.0%, Knots 16.8% | Snapshot de bitnodes/btcnodes, 21:59 UTC |
| Caídas máximas | −83.4% (2017-18); −76.6% (2021-22); peor día −37.2% | Yahoo BTC-USD, cierres diarios |
| Máximo histórico de cierre | US$124,752.53 (6-oct-2025); hoy −32.8% | Ídem |

## 5. Riesgos para vigilar (del protocolo a la cuenta)

| Riesgo | Horizonte | Señal para vigilar | Grado |
|---|---|---|---|
| Contraparte (Binance) | Inmediato | Avisos de Binance, SPEI/Medá, acciones de CNBV, FinCEN, OFAC o DOJ | B (precedentes: UE "solo retiros" el 1-jul-2026; Brasil 2022) |
| Error operativo en la contingencia | Inmediato | Dirección de destino, red correcta (BTC on-chain), 6 confirmaciones, retiro de prueba | A (mecánica) |
| Precio y caída | Temporada | SMA200, cortacircuitos, tope de 5,000 MXN | B (historia de drawdowns) |
| Gobernanza y clientes | 1-3 años | Proporción de Core y Knots; propuestas de soft fork; conflictos de política | C |
| Presupuesto de seguridad | 5-20 años | Porcentaje de comisiones; hashrate en USD por halving | B (mecánica) / C (efecto) |
| Bug de consenso | Cualquiera | Avisos de seguridad de Bitcoin Core; divergencias de cadena | B (4 precedentes) |
| Cuántico | Sin fecha | No cubierto en G1 | Sin evaluar |

## 6. Lo que no cubren estos 5 recursos (no lo encontré en lo que revisé)

- Valuación de BTC con evidencia fuera de muestra.
- Flujos de ETF y microestructura de exchanges. Son del G5.
- Riesgo cuántico: solo aparece una mención de pasada en MB, cap. 8.
- Fiscalidad cripto de una persona física en México.
- Prueba de reservas de exchanges. Es del G4.

## 7. Estado y pendientes

- **Estudiado el 25-sep-2026:** las 5 fichas y el [banco de examen G1](examen/banco-g1-bitcoin.md), con 8 preguntas.
- **Pendientes:**
  - MB caps. 8 (MuSig2 y FROST), 2 y 3 a detalle;
  - Plan ₿ CYP201, BTC204, LNP201 y MIN303;
  - Dinero Roto caps. 21-27, si el dueño compra el ebook;
  - el PDF original del Diploma 2025, si reaparece.
- **Candidatos para `registro-de-errores.md`** (los decide el orquestador): los errores de los recursos 15, 20 y 29 marcados en sus fichas. Ninguno es error nuestro.
