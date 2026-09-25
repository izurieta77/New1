# 29 · Diplomado Bitcoin, edición 2025 (My First Bitcoin)

> Ficha de recurso · Grupo G1 (Bitcoin) · Estudiada el 25-sep-2026 por `analista-cripto` · **Acceso: íntegro del texto sustituto** (repo oficial, commit `c752b65`, contenido actualizado a nov-2025) + comparación con la versión vigente **2026.04**. **El PDF original de la edición 2025 no fue accesible** · **Grado global: C-D**. **C** en conceptos básicos de dinero y custodia; **D** en todo lo que dice de inversión y precio.
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
>
> Las secciones se citan como "§ capítulo.sección" según los archivos del repo (por ejemplo, §5.2 = `5-an-introduction-to-bitcoin/2-bitcoin-as-sound-digital-money.md`).

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | Edición 2025. Según fuentes secundarias, se lanzó el 9-ene-2025 como libro de 176 pp. en 10 capítulos y 10 semanas, con cambios "menores" frente a 2024; esto **no lo verifiqué en fuente primaria**. Google Books registra "Bitcoin Diploma: Financial Education for the Bitcoin Era", 30-jun-2025, ISBN 9798999387400. La URL del índice hoy sirve la **versión 2026.04** |
| Autor | My First Bitcoin (Mi Primer Bitcoin), la misma organización del recurso 15. Según su propia historia: fundada en 2021; en jun-2022 graduó 38 alumnos en una escuela pública de El Salvador; currículo abierto desde sep-2022; se actualiza dos veces al año; más de 40,000 aprendices; red de educadores en 39-41 países |
| Tipo | Libro de trabajo y curso de 10 capítulos, con guías para educadores, audiolibros y curso autodidacta |
| Nivel | Principiante |
| Costo | Gratis. CC BY-SA 4.0 |
| Idioma | Inglés como original. La versión 2026.04 tiene 42 idiomas, con traducción por IA "with planned human editorial review", y un PDF en español de 132 pp. |
| URL | https://programs.myfirstbitcoin.org/programs/bitcoin-diploma/ · Repo vigente: https://github.com/MyFirstBitcoin/mfb-curriculum |
| **Conflictos de interés** | Organización *bitcoin-only*. Su web lista como socios o donantes a Reynolds American Foundation, Human Rights Foundation (HRF), Paystand, **Block** (empresa con negocios en Bitcoin) y Start Small Foundation. Declara excluir trading, altcoins y asesoría de inversión, pero el texto afirma que Bitcoin "no es una inversión sino una forma SEGURA de ahorrar". Promueve su propia red de proyectos: "73 proyectos en más de 38 países" a nov-2025 |

## 2. Acceso real

- **Repo de la edición 2025** (`MyFirstBitcoin/Bitcoin-Diploma-2025`): **sin acceso**.
  - `git clone` pidió credenciales, WebFetch dio 404 y `add_repo` respondió "not found".
  - archive.org respondió 429 (límite de tasa).
  - **No leí el PDF 2025 original.**
- **Sustituto leído completo.** Commit `c752b65` (30-ene-2026, "Initial commit of Bitcoin Diploma… in English") del repo vigente `mfb-curriculum`: los 10 capítulos, los apéndices y el glosario.
  - [I] Los títulos de los 10 capítulos coinciden con la edición 2025, y el texto dice "As of November 2025, 73 projects from over 38 countries". Por eso lo trato como **la edición 2025 en su forma final**. Es una inferencia, no una identidad comprobada.
- **Versión 2026.04 (commit "26.04", 4-may-2026; último commit 16-jul-2026).**
  - Comparé qué errores corrigió y cuáles persisten.
  - 26.04 reescribió 79 archivos en inglés: +1,727 y −1,948 líneas frente al commit inicial.
- **Nivel:** íntegro del sustituto; sobre la edición 2025 exacta, **sección o inferencia**.

## 3. Lo esencial

### Dinero, fiat y banca central (caps. 1-4)

- **[H] Conceptos básicos correctos (caps. 1-2):**
  - funciones del dinero: reserva de valor, medio de intercambio y unidad de cuenta;
  - propiedades: durabilidad, divisibilidad, portabilidad, aceptabilidad, escasez y fungibilidad;
  - preferencia temporal y costo de oportunidad;
  - Bretton Woods (1944, US$35 por onza) y Nixon (1971).
- **[H] Orden Ejecutiva 6102 (1933) y Gold Reserve Act (1934)** (§3.1): el oro pasa de 20.67 a 35 dólares la onza, así que los ahorros en efectivo **perdieron más de 40%** en oro.
  - [H, cálculo propio] 20.67 / 35 − 1 = **−40.9%**, el mismo número que en Dinero Roto, cap. 7.
- **[H] Inflación en EUA (§4.1).**
  - Precios "~30 veces" los de 1913: el IPC pasó de 9.9 en 1913 a 304.7 en 2023, **30.8×**.
  - Un Hershey de US$1 en 1913 costaría US$26.14 en 2020.
  - La deuda federal pasó de ~US$23 billones a **US$37 billones**, nivel que se alcanzó hacia ago-2025. Es una de las marcas de que el texto es de 2025.
- **[H, error y envejecido] Objetivos de la Fed (§3.2):** "desempleo < 6.5%, PIB 2-3%, inflación subyacente 2.0-2.5%".
  - La meta de la Fed es **2% de inflación PCE**. El umbral de 6.5% fue una guía de dic-2012, ya abandonada.
  - En la misma sección, el apartado "Central Bank" **repite el texto de "Wealthy Individuals"**, un error de edición.
- **[O] Tono militante (§3.1-§4.1):**
  - el fiat es "outright—yet legal—fraud and theft";
  - el IPC "can be manipulated", sin evidencia;
  - la banca central tiene "a more sinister side".
- **[H con errores de atribución]:**
  - fecha el *Cypherpunk's Manifesto* en **1992**; es de **1993**, y Plan ₿ lo da bien;
  - atribuye a **Satoshi** la frase "Why would anyone trust nerd money… Nerds brought you the internet. Banks brought you the Great Depression" (§6.0). Circula atribuida a **Andreas Antonopoulos** (por ejemplo, en un tuit de FTX de 2021) y **no la encontré** en los escritos de Satoshi citados;
  - las citas de Satoshi (P2P Foundation, feb-2009) y de Hayek (1984) sí son reales.

### Bitcoin, uso y custodia (caps. 5-7)

- **[O, grado D] "Bitcoin is NOT an investment but rather a SAFE… way of saving"** (§5.2).
  - Choca con los datos: −83.4% (2017-18) y −76.6% (2021-22) sobre cierres, y −37.2% en un día (ficha 15).
  - Sigue igual en 2026.04.
- **[O/H sin fuente] Afirmaciones sin respaldo (§5.1-§5.2):**
  - "Desde 2009, Bitcoin ha resistido **decenas de miles** de intentos de hackeo… nadie puede detenerlo". No da fuente y omite los CVE de inflación de 2010 y 2018 (ficha 15).
  - "2.5 mil millones de no bancarizados". Es la cifra del Findex de 2011; el **Findex 2021** da ~1.4 mil millones de adultos.
  - "By code impossible to increase [the supply]". Es impreciso: la regla la hacen cumplir los nodos que validan (MB, caps. 1 y 12).
- **[H] Portabilidad (§5.2).** En jul-2025 se movieron más de US$1,000 M por ~US$10.
  - [H, cálculo propio] La proporción, 1 × 10^-8, es correcta, pero la operación no trae fuente.
- **[H] Exchanges centralizados (§6.1).** Advierte que implican KYC (riesgo de robo de identidad) y custodia, y que "can misappropriate users' funds or sell more bitcoin than they have in reserves until they collapse — just like banks!".
  - En 6.2 aparece "Not your keys, not your coins".
- **[H, dato peligroso] "Wait for at least TWO confirmations (~20 min)"** (§6.4).
  - El Diplomado v3 (p. 84), Plan ₿ y MB recomiendan **6** para montos relevantes.
  - Con un atacante de 10% del hashrate, la probabilidad de reversión es **5.1%** con 2 confirmaciones y **0.024%** con 6 (whitepaper §11, cálculo propio).
  - Sigue igual en 2026.04.
- **[H] Lightning (cap. 7).**
  - Dice con honestidad que es "más rápido y barato pero **menos seguro**" que on-chain.
  - Acepta billeteras LN custodiales solo para montos pequeños.
  - Ejemplo de McDonald's: canal de 0.001 BTC; hamburguesa de 0.00005 y malteada de 0.00003 → saldo de 0.00092. La aritmética es correcta.
  - [O] Operar un nodo de ruteo como "steady source of income" es dudoso.

### Técnica y minería (caps. 8-9)

- **[H] Mejora frente a la v3.0 en criptografía.** Aclara que en Bitcoin "public/private key cryptography is **not** used to send encrypted messages".
  - Pero después dice que los nodos usan "the **recipient's** public key to verify the signature". Es **error**: se verifica con la clave pública **de quien gasta**.
  - Llama "encrypting" al hashing de la clave. 26.04 corrigió lo del receptor.
- **[H] UTXO bien explicado (§8.2):** 6 BTC → 5 a Bob + 0.99 de cambio + 0.01 de comisión.
- **[O, grado D] "Historically, halving events have led to significant price increases due to the reduced supply"** (§9.1).
  - Es causalidad no probada, con n = 3-4 y retornos decrecientes.
  - 26.04 lo suavizó a "if demand increases, the price of Bitcoin can rise", que es correcto.
- **[H, errores] Mempool y minería (§9.1-§9.2):**
  - un ejemplo de dificultad con un "hash más largo" que usa caracteres no hexadecimales: los hashes tienen **longitud fija**;
  - "if the majority of nodes agree" para entrar en la mempool: no hay votación, cada nodo aplica su política;
  - "72 hours": Bitcoin Core usa 336 h desde 0.14.0.
  - 26.04 corrigió el hash y las 72 h.
- **[H, error en 2026.04] La tabla de halvings nueva desplaza una época los porcentajes de oferta emitida.**
  - Dice 5.º halving (altura 1,050,000) → "98.44% minado"; 6.º → 99.22%; 7.º → 99.61%.
  - Mi cálculo: en la altura 1,050,000 se habrá emitido **96.875%** (20,343,750 BTC). El 98.4375% corresponde al **6.º** halving (1,260,000) y el 99.22% al **7.º** (1,470,000).

### Futuro, CBDC y casos (cap. 10 y apéndices)

- **[H, atribución probablemente incorrecta] CBDC** (§10.1): "134 países y uniones monetarias = 98% del PIB mundial; 35 en may-2020; 66 en fase avanzada; 19 del G20 avanzados", atribuido a **HRF**.
  - Estas cifras coinciden con el **CBDC Tracker del Atlantic Council** (actualización citada por la prensa: 134 países, 98% del PIB, 35 en may-2020). Según publicaciones del propio Atlantic Council, en 2025 ya contaba 137 países.
- **[H, error conceptual] "Los mineros… ofrecen a la red eléctrica el exceso de energía que crean"** (§10.3). Los mineros **no generan** energía; pueden **reducir su demanda** cuando la red la necesita.
- **[H, errores] Casos de estudio (apéndices):**
  - Indonesia "graduated over 2 students", corregido en 2026.04;
  - "students who grew up in a **communist** country" sobre Indonesia, que **no** es un país comunista. Sigue en 2026.04.
- **[O] Recursos adicionales sesgados (apéndices).** Boyapati ("strong investment opportunity"), *The Bitcoin Standard* y "Austrian thought"; incluyen un video de **RT**, medio estatal ruso, y un "Alex Swan: Grounded-Encounter Therapy" sin relación con el tema.
  - Recomienda *Broken Money* (recurso 28).
- **[H, errores del glosario]:**
  - "seed derived from the user's private key": es al revés, las claves se derivan de la semilla;
  - "address derived from private key": se deriva de la **clave pública**;
  - "nonce: random number";
  - unidad "sat/b": hoy se usa sat/vB.

## 4. Qué cambia para invertir

- **Es el recurso más peligroso del grupo si se toma al pie de la letra [I, nuestra].** Tres consejos contradicen la gestión de riesgo de la cuenta:
  1. **"No es una inversión, es ahorro seguro"**, contra un drawdown máximo de −83% y un tope de pérdida de 5,000 MXN;
  2. **"2 confirmaciones bastan"**, contra 6 para montos relevantes en la contingencia;
  3. **"el halving históricamente sube el precio"**, contra n = 3 decreciente y ningún halving en la temporada.
- **Rescatable para la cuenta.** El §6.1 describe el mecanismo exacto del riesgo de exchange: apropiación indebida y venta de más BTC de los que hay en reservas "hasta colapsar, igual que los bancos". Es la razón de la contingencia con Bitso y de no dejar la cuenta sin tope.
- **Calendario de emisión [H, cálculo propio].** Las cifras correctas para citar:

  | Halving | Altura | Emitido al llegar | Emitido al final de su época |
  |---|---|---|---|
  | 5.º | 1,050,000 | **96.875%** | 98.4375% |
  | 6.º | 1,260,000 | 98.4375% | 99.21875% |
  | 7.º | 1,470,000 | 99.21875% | 99.609375% |

  La tabla de 2026.04 muestra la columna "al final", pero la rotula como "al llegar".
- **Fundamentos frente a narrativa.** Nada de este recurso sirve como señal de mercado. Sus cifras verificables (IPC, oro en 1934, deuda) son de contexto macro, no de BTC.

### Ejercicio numérico (verificado en Python)

- **Probabilidad de reversión** de un depósito con z confirmaciones y un atacante con fracción q del hashrate (whitepaper §11, reproducido):

  | Atacante (q) | 2 conf. | 6 conf. |
  |---|---|---|
  | 0.10 | **5.10%** | **0.0243%** |
  | 0.30 | 44.6% | 13.2% |

- **Conclusión:** esperar 6 confirmaciones en lugar de 2 reduce el riesgo ~210 veces con q = 0.1. Cuesta ~40 min más de espera.

## 5. Contrapuntos y límites

- **No leí el PDF 2025 original.** Todo lo "2025" sale de un sustituto con contenido de nov-2025 [I]. Algún error podría haberse introducido o corregido entre versiones.
- **Financiamiento de la industria** (Block, HRF, Paystand) y misión militante. El recurso no distingue entre educación financiera y promoción.
- **Calidad editorial baja:**
  - fechas inconsistentes en el caso "Jaime" (2023, 2024 y 2026);
  - errata "Systematically" en Basilea III;
  - bloques de texto duplicados;
  - traducciones por IA con revisión humana "planeada", no hecha.
- **Mejoras reales de 2026.04:** corrigió las 72 h, la clave del receptor, el hash "más largo", la causalidad del halving y los "2 students".
- **Lo que sigue igual en 2026.04:** "2 confirmaciones", "no es inversión", "2.5 mil millones", "decenas de miles de ataques", "comunista", 6.5%, la cita de "nerd money", la atribución a HRF, el "exceso de energía" y el video de RT.

## 6. Autoexamen

1. **El Diploma dice "espera al menos dos confirmaciones (20 min)". ¿Cuándo es suficiente y cuándo no? Cuantifica.**
   - *Respuesta:* con un atacante de 10% del hashrate, la probabilidad de reversión es 5.1% con 2 confirmaciones y 0.024% con 6; con 30%, 44.6% y 13.2%.
   - Dos confirmaciones bastan para montos pequeños. Para montos relevantes, 6 o más, y el ataque Finney es posible con cualquier número si el atacante preminó un bloque.
   - *Fuente:* whitepaper §11 (cálculo propio); MB, cap. 12 y apéndice B.
2. **¿Qué está mal en la tabla de halvings de 2026.04 y cuál es la cifra correcta en la altura 1,050,000?**
   - *Respuesta:* rotula como "emitido al llegar" el porcentaje de la época siguiente. Al llegar a 1,050,000 se ha emitido 20,343,750 BTC (**96.875%**); 98.4375% corresponde a 1,260,000.
   - *Fuente:* §9.1 de la versión 26.04; `GetBlockSubsidy`.
3. **"Los nodos usan la clave pública del receptor para verificar la firma": corrige la frase.**
   - *Respuesta:* la firma se verifica con la clave pública de **quien gasta**, la dueña de la UTXO: revelada en el witness o el scriptSig en P2WPKH/P2PKH, o como clave de salida en P2TR. El receptor solo aporta la dirección, que es el hash de su clave pública o su clave ajustada, y firmará cuando a su vez gaste.
   - *Fuente:* MB, caps. 4 y 7.
4. **¿De dónde salen las cifras de CBDC que el Diploma atribuye a HRF?**
   - *Respuesta:* coinciden con el CBDC Tracker del Atlantic Council (134 países y uniones monetarias, 98% del PIB mundial; 35 países en may-2020). La atribución a HRF parece incorrecta; según publicaciones del Atlantic Council, en 2025 ya contaba 137 países.
   - *Fuente:* §10.1 del Diploma; atlanticcouncil.org/cbdctracker y prensa que lo cita (consultado el 25-sep-2026).

## 7. Grado de evidencia

- **B-C:** conceptos básicos de dinero, fiat, EO 6102 e IPC. Sus cifras son correctas.
- **C:** mecánica de billeteras y UTXO, con errores de glosario y de firma.
- **D:** inversión ("no es inversión", "ahorro seguro"), halving y precio, "decenas de miles de ataques", energía y CBDC atribuidas.
- **Global: C-D.** Sirve para ver cómo se enseña Bitcoin a principiantes y qué errores comunes corregir. **No** sirve como fuente de cifras ni de reglas operativas.

**Estado:** estudiado el 25-sep-2026. El PDF 2025 original sigue pendiente si reaparece en un repo o sitio oficial. Síntesis en [01-bitcoin-protocolo-dinero-y-autocustodia.md](../01-bitcoin-protocolo-dinero-y-autocustodia.md).
