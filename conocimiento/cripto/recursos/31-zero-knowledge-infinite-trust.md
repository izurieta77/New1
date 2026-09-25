# 31 · Zero Knowledge, Infinite Trust (Ben-Sasson y Jeffay, Wiley, 2026)

> **Estado:** estudiado en lo público · **Acceso:** **resumen**. No leí el libro: leí el capítulo 1 completo, el índice general y el índice analítico que Wiley publica gratis, más el sitio del libro, la ficha de la editorial, una reseña independiente y cobertura de prensa. · **Revisado:** 25-sep-2026 por `analista-cripto` · **Grupo:** G6 · **Grado global:** C

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2026. Según Wiley, el libro electrónico salió en abril de 2026 (ISBN 978-1-394-37384-0) y la tapa dura en mayo de 2026 (ISBN 978-1-394-37382-6). El sitio del libro fecha la tapa dura el 12-may-2026. |
| Autor | **Eli Ben-Sasson**: CEO, cofundador y presidente de StarkWare; coinventor de STARK, FRI y Zerocash; científico fundador de Zcash; consejero de la Starknet Foundation. **Nathan Jeffay** figura "(With)": periodista y, según el sitio del libro, **jefe de medios de StarkWare**. |
| Tipo | Libro de divulgación. John Wiley & Sons, 224 páginas: 15 capítulos, un apéndice ("Questions About STARK Proofs Answered"), glosario, notas e índice. |
| Nivel | Intermedio o divulgativo. El sitio promete "No computer science degree required". |
| Costo | Pago. Precios de Wiley: tapa dura US$30.00, libro electrónico US$18.00. El sitio ofrece 50% de descuento a oyentes de Real Vision. |
| Idioma | Inglés. |
| URL | https://blockchainthebook.com/ · https://www.wiley.com/en-us/Zero+Knowledge%2C+Infinite+Trust%3A+The+Evolution+and+Revolution+of+Blockchain+Technology-p-9781394373826 |
| **Conflictos de interés** | **Altos.** (1) Los autores son el CEO y el jefe de medios de StarkWare. El capítulo 12 se titula "StarkWare: From Genesis to $8 Billion". (2) La biografía de Jeffay en Wiley no menciona su cargo en StarkWare; el sitio del libro sí. (3) Los pedidos al mayoreo se tramitan en `book@starkware.co` e incluyen sesiones privadas con los autores, así que el libro funciona también como herramienta comercial. (4) Hay una página "Redpill your friends & family". (5) Relación cruzada con el recurso 09: según su biografía en Unchained, Haseeb Qureshi, anfitrión de The Chopping Block, lideró inversiones tempranas en StarkWare cuando estaba en Metastable. |

## 2. Acceso real

- **Leí completo (fuentes legales y gratuitas de la editorial):**
  - el índice general (PDF de Wiley);
  - el **capítulo 1**, "Why Blockchain Matters", pp. 1-6 (PDF de Wiley);
  - el **índice analítico**, pp. 195 y siguientes (PDF de Wiley).
- **Leí además:**
  - el sitio del libro: guía de capítulos, cronología, biografías, prensa y ventas al mayoreo;
  - la ficha de Wiley: descripción, precios, páginas y biografías;
  - una reseña independiente (Oleksandr Romanov, *Test Engineering Notes*, 11-jun-2026);
  - un artículo de Investing.com (Hillary Remy, 8-jun-2026) sin declaración de conflictos.
- **Verifiqué** contra la documentación de StarkWare la cronología que publica el sitio.
- **No compré el libro ni leí los capítulos 2 a 15.** Todo lo que diga de ellos sale de los títulos, el índice analítico, la guía del sitio y la reseña.
- **Nivel de acceso: resumen.**

## 3. Lo esencial

1. **[H] Estructura** (índice general de Wiley). Los capítulos siguen este arco:
   - por qué importa blockchain (cap. 1);
   - Bitcoin (caps. 2 y 4);
   - panorama técnico (cap. 3);
   - usos fuera del dinero (caps. 5 y 6);
   - obstáculos para la adopción masiva (cap. 7);
   - **"The Magic of Proofs"** (cap. 8, p. 71);
   - personas sin banco (cap. 9);
   - usabilidad, escala y privacidad (cap. 10);
   - la historia de la investigación (cap. 11);
   - StarkWare (cap. 12, p. 117);
   - "The Harshest Critique: Do We Even Need Crypto?" (cap. 13);
   - stablecoins y memecoins (cap. 14);
   - "The Integrity Web" (cap. 15).
2. **[H] La metáfora de "IntegrityLand".** El capítulo 1 presenta blockchain como lo contrario de "lo que pasa en Las Vegas se queda en Las Vegas": un lugar donde los acuerdos "se pegan como pegamento" y se cumplen solos. La tesis se ordena en tres pilares: **dinero**, **documentos y datos** (quién es "la fuente de verdad") y **coordinación social**.
3. **[O] Tesis central del capítulo 1:** "What blockchain offers is such a unique fit for the deep needs of humanity that its mass adoption is inevitable". Es una afirmación de fe, sin evidencia en el capítulo.
4. **[O] Exageración técnica del capítulo 1.** Dice que, una vez escrito algo en la cadena, nadie puede cambiarlo o borrarlo en secreto: "they simply can't". Contraejemplo documentado: la bifurcación que revirtió el hackeo de The DAO. El propio EIP-8363 de Ethereum la cita (EIP-779) como precedente de que "la capa social" puede anular las reglas del protocolo.
5. **[H] El argumento económico de fondo** (cap. 1). Además de robos, habrá delitos de "trampa en el cálculo". Las auditorías tradicionales "no pueden seguir el ritmo" de miles de millones de cómputos, así que hacen falta sistemas donde cada resultado se verifique criptográficamente. Es el puente hacia los STARKs: **pruebas de integridad computacional**.
6. **[H] La promesa editorial** (Wiley): "Skipping the speculative frenzy and political manifestos". Aplicaciones prometidas: privacidad, identidad digital e "integridad electoral".
7. **[H] Cronología del sitio:**
   - 2013: la "eureka" en una conferencia de Bitcoin.
   - 2017: Uri Kolodny se une como cofundador; una conferencia en el Technion espera 150 asistentes y llegan más de 900.
   - 2018: ronda semilla de US$6 M, "tasada" por Vitalik Buterin.
   - 2021: Serie B de US$75 M liderada por Paradigm y Serie C con valuación de US$2,000 M liderada por Sequoia.
   - 2022: Serie D de US$100 M a una valuación de **US$8,000 M** (Greenoaks y Coatue), con la decisión de "no patents, open-source".
8. **[H] Error en esa cronología.** El sitio pone bajo **2019** "StarkEx Goes Live" y "dYdX migrates to StarkEx". La documentación oficial de StarkWare dice otra cosa: StarkEx está en la red principal "since June 2020" (primer cliente: DeversiFi, hoy rhino.fi), dYdX llegó en **abril de 2021** y Sorare en junio de 2021. El sitio promocional comprime la historia a favor del relato.
9. **[H] Qué no aparece en el índice analítico.** Revisé el índice (pp. 195 y siguientes) y **no encontré** entradas para STRK (el token de Starknet), *airdrop*, Terra o Luna, hackeos, *exploits*, bugs ni "risk". La regulación aparece solo "as roadblock". Sí hay entradas para FTX (p. 119), la crítica de Krugman (pp. 135-136), computadoras cuánticas (pp. 174-175) y "post-quantum secure" (p. 176).
   - *Salvedad:* un índice no prueba que el texto omita esos temas; solo dice que no están indexados.
10. **[H] Mercado del token vinculado.** Según CoinGecko (25-sep-2026), STRK cotiza a US$0.040, contra un máximo de US$4.41 el 20-feb-2024: **−99.1%**. Su mínimo, US$0.0222, fue del 18-ago-2026. La valuación de US$8,000 M es una marca privada de 2022 y no es un precio de mercado.
11. **[H] La reseña independiente** (Romanov) le reconoce ser accesible, usar buenas analogías (como el muestreo "en una alberca") y contar bien la historia "del rechazo académico a la empresa de US$8,000 M". Le señala que **no trae**: la matemática de los ZK-STARK, ejemplos de código ni explicaciones técnicas detalladas. Según la reseña, el autor sostiene que la configuración compleja de los zk-SNARKs "puede ser fuente de problemas y vulnerabilidades".
12. **[H] Cobertura de prensa del sitio.** El sitio anuncia que entró a la lista de más vendidos de *USA Today* el 21-may-2026. La prensa que cita incluye muchas entrevistas y podcasts del propio autor (Aleph, Real Vision, Quadrillions, The Money Block), o sea, promoción y no reseña.
13. **[H] Calidad desigual de esa prensa.** El artículo de Investing.com (8-jun-2026) repite la tesis ("the next blockchain race isn't speed, it's trust"), no trae cifras y no declara conflictos.
14. **[H] Punto técnico relevante, confirmado fuera del libro.** Las pruebas STARK son plausiblemente poscuánticas porque se basan en hashes (recurso 18, clase 8). Pero StarkWare admite que las firmas de cuentas de Starknet y el puente o los datos en Ethereum todavía no lo son (The Quantum Insider, 30-jun-2026).
15. **[I] Uso correcto del libro.** Sirve como mapa de la narrativa del bando STARK: transparencia, sin configuración confiable, poscuántico, "integridad verificable". El contrapeso neutral está en el recurso 18. Ahí se ve que las pruebas STARK son mucho más grandes ("cientos de KB") y que su seguridad práctica descansa en una conjetura sobre FRI.
16. **[I] La lección central para invertir no está en el libro.** Una empresa con tecnología de punta y valuación privada alta puede coexistir con un token que pierde 99%. **Tecnología ≠ captura de valor para el tenedor del token.**

## 4. Qué cambia para invertir

- **Leer "US$8,000 M" como marca privada de 2022, no como precio.** El minorista no puede comprar ese capital. El vehículo líquido vinculado (STRK) es otro activo, con otra dilución y otro destino.
- **Separar visión de rendimiento.** "Integrity Web" puede ser correcta como tecnología y aun así no pagar a ningún token. En cualquier activo ligado a ZK, la pregunta es qué flujo de dinero llega al tenedor: comisiones, quema o *staking* real.
- **Vigilar "poscuántico" como argumento de venta.** Aplica a la capa de pruebas, no al sistema completo.
- **Cartera actual (solo BTC spot):** no hay acción. Si algún día se evalúa STRK, ETH o una L2, el libro sirve solo para entender el discurso del emisor. El análisis lo decide la ficha 18 más datos de mercado.

## 5. Contrapuntos y límites

- **No leí el libro.** Puede tratar riesgos, el token o sus fracasos sin que el índice analítico lo refleje.
- **La crítica viene incluida.** El capítulo 13, "The Harshest Critique", indica que el autor responde a los escépticos, pero no sé con qué profundidad.
- **Solo encontré una reseña independiente, y es de un blog personal.** No hallé reseñas de prensa de referencia (FT, WSJ, NYT) en lo que revisé.
- **La cronología del sitio es imprecisa** en al menos un punto (StarkEx y dYdX), como se detalla en el punto 8.
- **El conflicto de interés es estructural:** es el relato de una empresa contado por su CEO y su jefe de medios.

## 6. Autoexamen

1. **¿Por qué el acceso a este recurso se declara "resumen" y no "sección" o "íntegro"?**
   - Porque solo se leyeron el capítulo 1, el índice general y el índice analítico que publica Wiley gratis, más fuentes secundarias.
   - Los capítulos 2 a 15 no se leyeron. Es un libro de pago y la regla prohíbe afirmar una lectura íntegra que no hubo.
   - *Fuente:* ficha de Wiley con extractos PDF; regla de acceso de `00-indice.md`.
2. **Da un dato del sitio promocional que contradiga una fuente primaria y di cuál es la correcta.**
   - El sitio pone "StarkEx Goes Live" y la migración de dYdX en 2019.
   - La documentación de StarkWare dice que StarkEx está en la red principal desde junio de 2020 y que dYdX llegó en abril de 2021.
   - *Fuente:* docs.starkware.co/starkex.
3. **¿Qué afirmación del capítulo 1 es exagerada y qué contraejemplo la refuta?**
   - Que lo escrito en blockchain nadie puede cambiarlo o borrarlo ("they simply can't").
   - Contraejemplo: la bifurcación de Ethereum que revirtió el hackeo de The DAO, citada como precedente en EIP-8363 (EIP-779).
   - *Fuente:* capítulo 1, p. 2; `eip-8363.md` en github.com/ethereum/EIPs.
4. **¿Por qué la valuación de US$8,000 M de StarkWare no dice nada sobre el rendimiento de STRK?**
   - Porque es una ronda privada de capital (Serie D, 2022) y no un precio de mercado del token.
   - STRK es otro activo, con otra oferta y otros incentivos: hoy está −99.1% contra su máximo.
   - *Fuente:* cronología del sitio del libro; CoinGecko, 25-sep-2026.

## 7. Grado de evidencia: **C**

- **Hechos biográficos y de la empresa:** son fuente primaria, pero interesada. En ese sentido son C+: útiles, aunque necesitan verificación, y ya se detectó un error de cronología.
- **Predicciones:** grado D. La "adopción masiva inevitable" no trae evidencia en lo leído.
- **Contenido técnico:** no pude juzgarlo sin leer los capítulos 8 y el apéndice. Para lo técnico, usar el recurso 18 (grado A).

### Fuentes

- **Sitio del libro:** https://blockchainthebook.com/ y https://blockchainthebook.com/press, consultados el 25-sep-2026.
- **Wiley:** ficha del libro y extractos gratuitos.
  - Índice general: https://media.wiley.com/product_data/excerpt/21/13943738/1394373821-10.pdf
  - Capítulo 1: `.../1394373821-175.pdf`
  - Índice analítico: `.../1394373821-219.pdf`
- **Reseña:** Oleksandr Romanov, 11-jun-2026: https://testengineeringnotes.com/posts/2026-06-11-zero-knowledge-review/
- **Artículo de Investing.com** (8-jun-2026): https://www.investing.com/analysis/the-next-blockchain-race-isnt-speed-its-trust-200681685
- **StarkEx:** https://docs.starkware.co/starkex/index.html
- **StarkWare y computación cuántica:** The Quantum Insider, 30-jun-2026.
- **Precios de STRK:** CoinGecko, API consultada el 25-sep-2026.
- **Biografía de Haseeb Qureshi:** https://unchainedcrypto.com/the-chopping-block/
- **EIP-8363:** https://github.com/ethereum/EIPs, archivo `EIPS/eip-8363.md`.
