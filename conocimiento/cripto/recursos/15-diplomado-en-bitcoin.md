# 15 · Diplomado en Bitcoin v3.0 (Mi Primer Bitcoin)

> Ficha de recurso · Grupo G1 (Bitcoin) · Estudiada el 25-sep-2026 por `analista-cripto` · **Acceso: íntegro (texto)** · **Grado global: C**. Sube a **A** en el calendario de emisión, que reproduje con cálculo propio, y baja a **D** en todo lo que dice del precio.
>
> **Etiquetas:**
> - **[H]** hecho con fuente y página;
> - **[I]** inferencia o interpretación (digo si es del autor o nuestra);
> - **[O]** opinión o pronóstico del autor.
>
> **Grados:**
> - **A:** identidad o dato oficial;
> - **B:** evidencia sólida con salvedades;
> - **C:** muestra corta o no reproducible;
> - **D:** narrativa sin historial auditado.
>
> Las páginas son las **impresas** del libro (página del PDF − 6).

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 3.ª edición, "Septiembre 2022" (portada). El PDF se generó el 24-oct-2022; último commit del repo: `d4c0859`, 3-mar-2023 |
| Autor | Mi Primer Bitcoin (El Salvador). Equipo: Dalia Platt, Gloriana Solano, Raúl Guirola y Robert Malka; colaboradores, entre ellos Giacomo Zucco (también cofundador de Plan ₿, recurso 20). Fundador: John Dennehy |
| Tipo | Libro de trabajo para un curso de 10 clases más una clase adicional; 130 páginas de PDF |
| Nivel | Principiante (se pensó para bachillerato público) |
| Costo | Gratis. La licencia es CC BY-SA 4.0 según `LICENSE.md` y la p. 4 del PDF, pero la frase en español del `README` dice "Reconocimiento-NoComercial-SinObraDerivada 4.0": **contradicción interna** |
| Idioma | Español |
| URL | https://github.com/MiPrimerBitcoin/Diplomado_v3.0 |
| **Conflictos de interés** | Organización educativa *bitcoin-only* que vive de donaciones: más de 400 donantes, y el PDF trae su dirección de donación. El piloto de La Pacheco (San Marcos, El Salvador; inicio en feb-2022, clases desde abril, graduación en junio) lo financió en parte **IBEX Mercado**, empresa de pagos Lightning, que pagó la cafetería y otros gastos. Tiene incentivos para presentar Bitcoin de forma favorable. En las fuentes (pp. 120-121) mezcla material educativo de la Fed con videos de YouTube, cryptopotato, capital.com, un influencer (Lark Davis) y el "rainbow chart" |

## 2. Acceso real

- **Qué leí.** Cloné el repo (`git clone --depth 1`) en el scratchpad el 25-sep-2026. Extraje con `pypdf` el texto de "Mi Primer Bitcoin - Libro de Trabajo (V3.0) - FINAL.pdf" y **lo leí completo**: 10 clases, clase adicional, glosario y fuentes.
- **Qué no vi.** Gráficos e imágenes. De la gráfica de halvings y precio (p. 91) solo leí los rótulos.
- **Nivel: íntegro (texto).**
- **Sin copias en el repo.** El PDF quedó solo en el scratchpad.

## 3. Lo esencial

### Estructura y enfoque

- **[H] Temario** (índice del PDF):
  - clases 1-3: dinero; historia del dinero, fiat, banca central y reserva fraccionaria; inflación, vigilancia y restricción;
  - clase 4: por qué Bitcoin (generales bizantinos; BTC frente a fiat);
  - clase 5: compra, custodia, transacción y UTXO;
  - clase 6: doble gasto, mempool, nodos y Lightning;
  - clase 7: minería, hash, nonce y árbol de Merkle;
  - clase 8: escasez, halving, precio, dificultad y ataques;
  - clase 9: energía, innovación (SegWit, Taproot, Schnorr, "Taro") y El Salvador;
  - clase 10: ensayo final;
  - clase adicional: firmas digitales.
- **[O] Enfoque normativo, no neutral.**
  - "El dólar al borde del colapso" (p. 104).
  - "Cesará el deseo de imprimir dinero" (p. 105).
  - La hiperbitcoinización haría subir el precio "exponencialmente" (p. 95).

### Emisión y escasez (lo más sólido)

- **[H] Emisión.** Empieza en 50 BTC por bloque, se reduce a la mitad cada 210,000 bloques y termina ~2140 con 21 M (pp. 90-92).
  - [H, cálculo propio] El máximo exacto es **20,999,999.9769 BTC** (2,099,999,997,690,000 sats), porque el subsidio se redondea hacia abajo al satoshi.
- **[H] "~19,101,000 BTC a jul-2022" (p. 92).** Es consistente con mi cálculo: 19,104,344 BTC al bloque 746,695 (26-jul-2022).
- **[H] Error de uno en la p. 90.** Dice que "el bloque 210,001 solo otorgó 25 BTC". El primer bloque de 25 BTC es la **altura 210,000**, minada el 28-nov-2012 a las 15:24 UTC según mempool.space.
- **[H] Inflación del dólar (p. 32).** US$1 de 1920 equivale a US$1.94 en 1970, 1.33% anual; US$1 de 1970 equivale a US$6.67 en 2020, 3.87% anual.
  - [H, cálculo propio] 1.9372^(1/50) − 1 = 1.33% y 6.666^(1/50) − 1 = 3.87%. La aritmética es correcta.
- **[H] Error de traducción de unidades (p. 96).** Traduce "TH/s (Tera = **trillón**)". En español, 10^12 es un **billón**.

### Custodia y transacciones

- **[H] Custodia (pp. 55-56).**
  - Distingue autocustodia de custodia de terceros, y billetera fría de caliente.
  - Aclara que la comisión depende del tamaño en bytes, no del monto. Es correcto y coincide con MB, cap. 9.
- **[H] Error: billeteras de papel.** La p. 56 las pone entre "las formas más seguras". Mastering Bitcoin (cap. 4) las declara **obsoletas y peligrosas**: "DO NOT USE PAPER WALLETS".
- **[H] Error conceptual en la p. 59.** Llama a la dirección "llave pública" y describe la transacción como "cifrar/descifrar".
  - Bitcoin **firma, no cifra**. La clave pública (o su hash, en la dirección) sirve para verificar la firma (MB, cap. 4).
- **[H] Semilla y rango de claves (p. 116).**
  - La semilla tiene 12 a 24 palabras.
  - Las claves privadas válidas van de 1 a 115792089237316195423570985008687907852837564279074904382605163141518161494336, que es **n − 1 de secp256k1**. El número es exacto (verificado).
  - Aquí el Diplomado acierta y MB se equivoca: MB escribe "entre 0 y n − 1".
- **[H] Dato envejecido: mempool de "hasta 72 horas" (p. 66).**
  - Bitcoin Core expira las transacciones a las **336 h (2 semanas)** desde la versión 0.14.0 (8-mar-2017; PR #9312).
  - El código actual lo confirma: `DEFAULT_MEMPOOL_EXPIRY_HOURS{336}` en `src/kernel/mempool_options.h`.
- **[H] Confirmaciones.** Recomienda esperar **6** (p. 84) y dice bien que "cada confirmación reduce exponencialmente el riesgo" (p. 69).
  - "Todos los nodos deben aceptar unánimemente" es impreciso: no hay votación.
- **[H] Lightning (pp. 72-73).** No es crédito, sus transacciones son transacciones Bitcoin válidas y el canal se puede cerrar de forma unilateral. Es correcto a este nivel.

### Minería, seguridad y energía

- **[H] Error conceptual en la tabla BTC frente a fiat (p. 48).** Dice que la "criptografía… previene el ataque del 51% de los nodos".
  - El 51% se mide en **hashrate**, no en nodos, y la criptografía no lo impide.
  - Lo que sí permite un atacante con mayoría: doble gasto de **sus propias** transacciones y censura, no robar (MB, cap. 12 y apéndice B).
- **[H] Errores de orden de magnitud y de concepto.**
  - Los mineros prueban "varios miles de veces por segundo" (p. 83). La red va en **~922.7 EH/s**, es decir ~9.2 × 10^20 hashes por segundo (mempool.space, 25-sep-2026).
  - Pregunta "con cuántos ceros comienza el **nonce**" (p. 87). Lo que debe quedar debajo del objetivo es el **hash** del encabezado.
- **[H] Omisión: "ningún ataque ha podido interrumpir la red" (p. 97).** Deja fuera fallas reales documentadas en el wiki de Bitcoin (lista de CVE):
  - CVE-2010-5139 (15-ago-2010): inflación por desbordamiento de salidas;
  - CVE-2013-3220 (11-mar-2013): división de la red 0.7/0.8, que MB también narra en el cap. 12;
  - CVE-2018-17144 (17-sep-2018): inflación por entradas duplicadas en versiones anteriores a la 0.16.3.
- **[H] Energía (p. 102).**
  - Cifra 59.5% de renovables en abr-2022 **sin fuente**; es el autorreporte del Bitcoin Mining Council.
  - Da un "0.16% de la energía mundial" = 247 / 154,750 TWh. La aritmética es correcta, pero compara con la energía primaria total, no con la electricidad.
- **[O, grado D] Precio (pp. 91-95).**
  - Rotula los halvings con sus precios: US$12 (28-nov-2012), US$658 (9-jul-2016) y US$8,572 (11-may-2020).
  - Recomienda el rainbow chart como "información valiosa para comprar o vender".
  - Subestima el riesgo: caídas "de hasta 80%" y "hasta 20% en un día" (p. 93).

## 4. Qué cambia para invertir

### Calendario de emisión (verificado con `GetBlockSubsidy`, en Python, y fechas de mempool.space)

| Evento | Altura | Fecha (UTC) | Subsidio después | Oferta emitida al llegar | Época anterior |
|---|---|---|---|---|---|
| Génesis | 0 | 3-ene-2009 18:15 | 50 | 0 | — |
| 1.er halving | 210,000 | 28-nov-2012 15:24 | 25 | 10,500,000 | 3.90 años; bloque medio de 586 s |
| 2.º | 420,000 | 9-jul-2016 16:46 | 12.5 | 15,750,000 | 3.61 años; 543 s |
| 3.º | 630,000 | 11-may-2020 19:23 | 6.25 | 18,375,000 | 3.84 años; 577 s |
| 4.º | 840,000 | 20-abr-2024 00:09 | 3.125 | 19,687,500 | 3.94 años; 592 s |
| **5.º** | **1,050,000** | **ETA 13-abr-2028** (600 s por bloque) a **10-may-2028** (628.9 s, el ritmo actual) | 1.5625 | 20,343,750 | — |

- **Hoy (altura 968,589, 25-sep-2026):**
  - oferta teórica: **20,089,343.75 BTC**, el 95.66% del máximo;
  - faltan ~910,656 BTC y **81,411 bloques** para el halving;
  - emisión actual ≈ 164,000 BTC/año (0.82%), que baja a ≈ 82,000 BTC/año (0.40%) después de 2028.
- **[I, nuestra] No hay halving dentro de la temporada del torneo** (28-sep-2026 a 28-ene-2027). Cualquier "efecto halving" queda fuera del horizonte de la cuenta.
- **[H, cálculo propio con Yahoo BTC-USD] Lo que pasó después de cada halving:**
  - rendimiento a 12 meses: +287% (2016), +559% (2020) y +31% (2024);
  - la serie decrece, n = 3, y el halving de 2012 queda fuera de la serie, que empieza el 17-sep-2014;
  - veredicto: **grado C**. No es un modelo de precio.

### Riesgo que el Diplomado subestima

- **[H, cálculo propio] Caídas reales, sobre cierres de Yahoo:**
  - **−83.4%** del 16-dic-2017 al 15-dic-2018;
  - **−76.6%** del 8-nov-2021 al 21-nov-2022;
  - peor día: **−37.2%** el 12-mar-2020;
  - volatilidad anualizada a 5 años (√365): **51.5%**.
- **[I, nuestra] Contra lo que dice el libro:** su "hasta 80%" y "hasta 20% en un día" no deben usarse para dimensionar posiciones. Para eso existen el tope de pérdida (5,000 MXN) y los cortacircuitos de la decisión del 25-sep-2026.

### Autocustodia frente a exchange, aplicado a la cuenta Binance

- **[I, nuestra] Un saldo en Binance es custodia de terceros**, el nivel más débil del marco del Diplomado.
  - El exchange **no está supervisado en México y no puede estarlo** (Ley Fintech, art. 30; Circular 4/2019 de Banxico). Los pesos pasan por Medá, IFPE autorizada por la CNBV (`bitacora/decisiones/2026-09-25-CRIPTO-inicial.md`).
- **La lección útil del libro es operativa:** quien no controla las llaves depende de que el custodio le deje retirar. Eso respalda la contingencia ya aprobada:
  - abrir y **probar** Bitso;
  - disparadores: aviso de Binance, SPEI caído más de 48 h, o acción de CNBV, FinCEN, OFAC o DOJ;
  - respuesta: vender a MXN y retirar por SPEI, o mover BTC a Bitso.
- **No seguir el consejo de la p. 56:** nada de billeteras de papel. Si algún día hay autocustodia, se usa una billetera de hardware con semilla respaldada en acero, como en el recurso 20 y en MB, cap. 5.

### Qué fundamentos importan y cuáles son narrativa

- **Sirven:** la oferta emitida y el calendario (grado A), el hashrate y la dificultad (grado A como dato) y las confirmaciones.
- **Narrativa (grado D):** rainbow chart, "hiperbitcoinización" y "el precio es el mismo en todos los países" (p. 47). Esto último es falso: hay primas locales.

### Ejercicio numérico (verificado en Python)

1. **Valor de un satoshi.**
   - La p. 54 da 1 BTC = US$21,464 y "≈ US$0.0003" por sat. Con ese precio, 1 sat = US$0.000215: **el libro sobrestima 40%**.
   - Con el precio de referencia de la decisión (US$84,045.67, 25-sep-2026 20:29 UTC), 1 sat = **US$0.00084**.
2. **ETA del 5.º halving.** Faltan 81,411 bloques:
   - × 600 s = 48.8 millones de s ≈ 565.4 días → **13-abr-2028**;
   - × 628.9 s ≈ 592.6 días → **10-may-2028**.
   - Segunda verificación con un bloque medio de 590 s: 3-abr-2028. La ventana probable es **abr-may-2028**.

## 5. Contrapuntos y límites

- **Promoción con financiamiento del sector** (IBEX Mercado) y fuentes de calidad desigual. Sus cifras de precio y energía no tienen fuente primaria.
- **Envejeció rápido:**
  - reserva bancaria de "10%" en EUA (p. 24): la Fed la bajó a **0% desde el 26-mar-2020** (federalreserve.gov, *Reserve Requirements*), dos años antes de esta edición;
  - mempool de 72 h;
  - "Taro", que hoy se llama Taproot Assets (MB, cap. 14);
  - un precio de sep-2022.
- **Cifra dudosa sobre China (p. 34).** Dice "hasta $50,000 de renminbi (aprox. 8,000 USD)". La cuota anual de compra de divisas por persona es el **equivalente a US$50,000** (SAFE, según fuentes secundarias consultadas el 25-sep-2026).
- **Remesas de El Salvador: 23% del PIB y ~US$6 mil M en 2020 (p. 34).** Sin fuente en el libro y no lo verifiqué.
- **Satoshi con ~980,000 BTC (p. 42).** Estimación sin fuente. Además escribe "Gavin **Andersen**"; es Andresen.
- **Imprecisiones:**
  - un bloque de "~2.5 MB" (p. 82): el límite es de 4 M unidades de peso;
  - "los mineros siempre ejecutan un nodo completo" (p. 78): muchos hashers dependen del pool (MB, apéndice B);
  - "los mineros verifican la firma" (p. 117): la verifica cada nodo.

## 6. Autoexamen

1. **¿En qué altura empezó el subsidio de 25 BTC y qué error comete el Diplomado?**
   - *Respuesta:* en la altura **210,000** (28-nov-2012, 15:24 UTC). El libro dice "210,001" (p. 90).
   - La fórmula es `subsidio = 50 BTC >> (altura // 210,000)`: la división entera cambia de 0 a 1 justo en 210,000.
   - *Fuente:* MB, cap. 12 (`GetBlockSubsidy`); mempool.space.
2. **¿Por qué "cifrar/descifrar" (p. 59) describe mal una transacción?**
   - *Respuesta:* porque Bitcoin usa criptografía asimétrica para **firmar**. La clave privada produce la firma, y cualquier nodo la verifica con la clave pública revelada en el gasto. Nada del monto ni del destino se cifra; todo es público.
   - *Fuente:* MB, cap. 4 ("not used to encrypt") y cap. 8.
3. **El libro dice que la mempool guarda las transacciones "hasta 72 horas". ¿Qué pasa en Bitcoin Core y qué puede hacer quien envió una transacción con comisión baja?**
   - *Respuesta:* cada nodo tiene su propia mempool y expira las transacciones a las **336 h** por defecto (desde 0.14.0).
   - Para acelerarla se usa RBF (desde Core 28.0 hay full-RBF por defecto) o CPFP desde una salida propia.
   - *Fuente:* código de Bitcoin Core; notas de las versiones 0.14.0 y 28.0; MB, cap. 9.
4. **¿Qué está mal en "la criptografía previene el ataque del 51% de los nodos" (p. 48)?**
   - *Respuesta:* el umbral se mide en **hashrate**, no en nodos. Con mayoría de hashrate se puede hacer doble gasto de transacciones propias y censurar, pero no falsificar firmas ni crear monedas fuera de las reglas, porque los nodos validan.
   - Según el apéndice B de MB, la minería egoísta ya es rentable con ~30%.
   - *Fuente:* MB, cap. 12 y apéndice B; whitepaper, §11.

## 7. Grado de evidencia

- **A:** calendario de emisión, 21 M, halvings y rango de claves de la p. 116. Coinciden con el código y con mi cálculo.
- **B:** conceptos básicos de custodia, UTXO y confirmaciones, con la excepción grave de las billeteras de papel.
- **C:** historia monetaria e inflación, con cifras correctas pero fuentes secundarias.
- **D:** precio, rainbow chart, energía sin fuente y "el dólar al borde del colapso".
- **Global: C.** Sirve para enseñar vocabulario, no como fuente de cifras.

**Estado:** estudiado completo el 25-sep-2026. Los errores de las pp. 24, 34, 48, 56, 59, 66, 83, 87, 90, 96 y 97 son candidatos para `registro-de-errores.md`; los anota el orquestador. Síntesis en [01-bitcoin-protocolo-dinero-y-autocustodia.md](../01-bitcoin-protocolo-dinero-y-autocustodia.md).
