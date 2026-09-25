# 18 · Zero Knowledge Proofs MOOC (UC Berkeley RDI, primavera 2023)

> **Estado:** estudiado · **Acceso:** sección (temario completo y diapositivas de 13 clases; sin videos) · **Revisado:** 25-sep-2026 por `analista-cripto` · **Grupo:** G6 · **Grado global:** A en la criptografía; C en lo que implica para precios.

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2023. Primera clase el 17-ene-2023; última clase listada el 9-may-2023. |
| Autor | UC Berkeley RDI. Instructores: Dan Boneh (Stanford), Shafi Goldwasser (UC Berkeley), Dawn Song (UC Berkeley), Justin Thaler (Georgetown) y Yupeng Zhang (Texas A&M). Invitados, entre otros: Ye Zhang (Scroll), en zkEVM, y Zac Williamson (Aztec), en privacidad. |
| Tipo | MOOC universitario: videos en YouTube, diapositivas en PDF, cuestionarios semanales, un laboratorio de programación y una tarea con soluciones. |
| Nivel | Experto: campos finitos, polinomios, curvas elípticas y probabilidad. |
| Costo | Gratis. La constancia es un NFT por niveles ("Legendary", "Ninja", "Trailblazer"). |
| Idioma | Inglés. |
| URL | https://rdi.berkeley.edu/zk-learning/ |
| **Conflictos de interés** | (1) Justin Thaler es *research partner* de a16z crypto y Dan Boneh es *senior research advisor* de a16z crypto, según las páginas del equipo de a16z. Ese fondo invierte en empresas de pruebas ZK. (2) Las clases de zkEVM y de privacidad las dieron fundadores de proyectos comerciales que venden justo esa tecnología: Ye Zhang (Scroll) y Zac Williamson (Aztec). (3) El curso entregaba NFTs de finalización y promovía un hackathon ZKP/Web3. La matemática no depende de esto, pero sí el encuadre de qué problemas parecen "resueltos". |

## 2. Acceso real

- **Leí completa** la página del curso: temario, lecturas por clase, reglas de los NFTs, calendario del laboratorio y de la tarea.
- **Descargué 13 PDFs de diapositivas** y extraje su texto: clases 1, 2, 4, 5, 6, 7, 8, 9, 10, 12, la de zkEVM por opcodes, la de privacidad y la 14.
  - **A fondo:** 2 (panorama de SNARKs, Boneh), 5 (PLONK y KZG, Boneh), 8 (FRI, STARKs y Fiat-Shamir, Thaler), 12 (zkEVM, Ye Zhang) y la de privacidad (Zac Williamson).
  - **Por encima:** el resto.
- **Límite técnico:** algunas tablas numéricas vienen incrustadas como objetos que no se ven en el PDF. Ejemplo: tamaños de prueba y tiempos del verificador de la clase 2, diapositivas 29 a 31. Rendericé las diapositivas y las celdas salen vacías, así que **no cito esas cifras**.
- **No vi los videos** (YouTube bloquea desde la nube) y no hice cuestionarios ni laboratorio.
- **Nivel de acceso: sección.**

## 3. Lo esencial

1. **[H] Definición.** Una prueba de conocimiento cero demuestra que una afirmación o un cálculo es correcto sin revelar los datos que lo sustentan. Nace con Goldwasser-Micali-Rackoff (1985). El curso subraya que pasó de ser "impráctica" a estar desplegada gracias a mejoras de eficiencia de la última década (descripción del curso).
2. **[H] SNARK.** Es un argumento *sucinto*, *no interactivo*, de *conocimiento*: la prueba es corta y se verifica rápido. Es zk-SNARK si además no revela el testigo (clase 2).
3. **[H] Dos usos en blockchain que no hay que confundir** (clase 2, diapositivas 7 y 8):
   - **Verificar cómputo** (zkRollups, zkBridge): "no se necesita conocimiento cero", solo sucintez.
   - **Privacidad:** transacciones privadas (Zcash, Tornado Cash, Aleo, IronFish) y cumplimiento privado, como probar que un exchange es solvente sin revelar cuentas.
4. **[H] Receta moderna.** SNARK = IOP polinomial (objeto de teoría de la información) + esquema de compromiso polinomial (objeto criptográfico). La interacción se elimina con la transformación de Fiat-Shamir (clases 2 y 5).
5. **[H] KZG (Kate-Zaverucha-Goldberg, 2010).**
   - Comprometerse a un polinomio es publicar f(τ)·G.
   - La prueba de una evaluación es **un solo elemento de grupo**, sin importar el grado. Varias pruebas se agregan en uno.
   - Exige una **configuración confiable**: la diapositiva dice literalmente "delete τ !!".
   - El verificador usa *pairings*.
   - Los parámetros públicos crecen en proporción al grado (clase 5, diapositivas 4-13).
6. **[H] PLONK (eprint 2019/953)** (clase 5):
   - Compila el circuito a una traza de cómputo codificada en un polinomio.
   - Prueba cuatro cosas: entradas correctas, compuertas bien evaluadas (con un polinomio selector), cableado correcto (verificación de permutación prescrita) y salida final igual a cero.
   - Su preprocesamiento del circuito es no confiable. La confianza la pone el esquema de compromiso que se use.
7. **[H] PLONK es modular** (clase 5, diapositiva 40):
   - PLONK + KZG (Aztec, JellyFish): configuración confiable universal.
   - PLONK + Bulletproofs (Halo2): sin configuración confiable, pero verificador lento.
   - PLONK + FRI (Plonky2): sin configuración confiable, basado en hashes.
8. **[H] Tres familias de compromisos polinomiales** (clase 8, Thaler):
   - *Pairings* + configuración confiable (KZG): pruebas de tamaño constante; ni transparente ni poscuántico.
   - Logaritmo discreto (IPA/Bulletproofs, Hyrax, Dory): transparente, no poscuántico.
   - IOPs + hashing (FRI, Ligero, Brakedown, Orion): transparente y plausiblemente poscuántico.
9. **[H]** "La transparencia y la seguridad poscuántica plausible las determina **por completo** el esquema de compromiso usado" (clase 8, diapositiva 5).
10. **[H] Groth16 contra PLONK-KZG** (clase 8, diapositivas 13-14).
    - Groth16 tiene las pruebas más cortas (3 elementos de grupo) y el verificador más rápido. A cambio, exige configuración confiable **por circuito**, su probador es lento y no es poscuántico.
    - PLONK-KZG tiene configuración universal, pero sus pruebas son unas 4-6 veces más grandes que las de Groth16.
11. **[H] STARKs = IOP + FRI.** Tienen las pruebas más cortas entre los sistemas plausiblemente poscuánticos, pero aun así son grandes: "cientos de KB según la seguridad" (clase 8, diapositiva 11).
12. **[H] Seguridad de FRI.**
    - Cada consulta del verificador aporta unos log₂(1/ρ) bits de seguridad, donde ρ es la tasa del código Reed-Solomon. Con ρ = 1/4 son unos 2 bits por consulta.
    - Ese resultado está demostrado solo hasta cierta distancia y se **conjetura** para el resto. "La seguridad de la mayoría de los despliegues de FRI se analiza bajo esta conjetura" (clase 8, diapositivas 50-53).
13. **[H] Fiat-Shamir y ataques de "grinding"** (clase 8, diapositivas 69-79).
    - Al volver no interactivo un protocolo con λ bits de seguridad, quien haga 2^k hashes lo rompe con probabilidad 2^(k−λ), y puede intentarlo en silencio.
    - La diapositiva lo ilustra así: en 2023 la red de Bitcoin hacía unos 2^80 hashes SHA-256 por hora.
    - Conclusión literal: 60 bits no interactivos "no están bien, salvo que el premio del ataque sea mínimo".
14. **[H] Recursión.** Una prueba puede verificar otras pruebas: se agregan lotes y se abarata la verificación en L1. En la arquitectura de Aztec el esquema es circuito *kernel* → *rollup* → *root rollup* (clase 10 y clase de privacidad).
15. **[H] Tres sabores de zkEVM**, según la clasificación de Justin Drake que usa la clase 12:
    - **De lenguaje:** Matter Labs y StarkWare.
    - **De bytecode:** Scroll, Hermez y Consensys.
    - **De consenso:** probar las raíces de estado de la propia L1. Es la ruta de "SNARK-ificar todo" de Ethereum.
16. **[H] Privacidad en contratos** (clase de Aztec):
    - El estado privado va cifrado en árboles de solo agregado.
    - Se "borra" con *nullifiers*, lo que obliga a una estructura tipo UTXO.
    - Hace falta mezclar estado privado y público, y las funciones privadas se ejecutan y prueban **en el dispositivo del usuario**.
17. **[H] Verificación formal** (clase 14, leída por encima). Un circuito ZK puede tener bugs, como restricciones insuficientes, aunque la criptografía sea sólida.
18. **[I] ZK es infraestructura, no activo.** El valor económico se lo queda quien controla la secuencia, los datos o los usuarios, no necesariamente el token de la L2. Dato de mercado: STRK, el token de Starknet (StarkWare), cotiza a US$0.040, −99.1% contra su máximo de US$4.41 del 20-feb-2024 (CoinGecko, 25-sep-2026).
19. **[I] Dónde falla en la práctica un rollup ZK.** Más que en la matemática, falla en los bugs de circuito, las llaves que pueden actualizar el verificador o el puente, el secuenciador centralizado y los parámetros de seguridad bajos. Este curso da el vocabulario para preguntar por cada uno.

**Ejercicio numérico comprobado en Python (25-sep-2026).**

- **Consultas de FRI necesarias para 100 bits:**
  - ρ = 1/2: 100 consultas.
  - ρ = 1/4: 50.
  - ρ = 1/8: 34.
  - ρ = 1/16: 25.
- **Hashrate de Bitcoin hoy:** mempool.space da 918 EH/s. Eso son unos 3.3×10^24 hashes por hora ≈ 2^81.5; la diapositiva de 2023 decía 2^80.
- **Presupuesto del atacante:** un año entero de ese hashrate equivale a unos 2^94.5 hashes. Con él, la probabilidad de romper un sistema no interactivo sería:
  - de 80 bits: prácticamente segura, porque 2^14.5 > 1;
  - de 100 bits: ≈ 2^−5.5, un 2%;
  - de 128 bits: ≈ 2^−33.5, despreciable.
- **Advertencia:** es ilustrativo. El hash de un sistema de pruebas no es SHA-256 y el atacante necesitaría hardware propio.

```python
import math
for rho in [1/2,1/4,1/8,1/16]: print(rho, math.ceil(100/math.log2(1/rho)))
k = math.log2(918e18*3600*24*365)              # ≈ 94.5
print({lam: round(k-lam,1) for lam in [80,100,128]})   # log2 de la probabilidad de éxito
```

## 4. Qué cambia para invertir

- **Preguntas obligatorias antes de invertir en algo que se venda como "ZK"**, con L2BEAT y la documentación del proyecto:
  - ¿Qué sistema de pruebas y qué compromiso usa: Groth16, PLONK-KZG o FRI/STARK?
  - ¿Requirió ceremonia de configuración confiable?
  - ¿Cuántos bits de seguridad declara y bajo qué conjetura?
  - ¿El verificador en L1 se puede actualizar, y quién tiene esa llave?
- **"ZK" no significa privado.** La mayoría de los zkRollups publican sus datos. La privacidad es otro producto, con otro riesgo regulatorio.
- **"Poscuántico" se juzga en el sistema completo, no solo en la prueba.**
  - StarkWare admite que las pruebas STARK ya lo son, porque se basan en hashes.
  - En cambio, las firmas de cuentas de Starknet, el puente con Ethereum y los datos en *blobs* todavía no lo son (The Quantum Insider, 30-jun-2026).
  - Para BTC, la exposición cuántica relevante está en las firmas ECDSA/Schnorr, no en la prueba de trabajo. Es inferencia mía, no verificada en esta sesión; corresponde a G1.
- **Para la cartera actual** (solo BTC spot en Binance), ZK no es una posición. Sirve para vigilar:
  - rotaciones narrativas hacia privacidad, como ZEC: US$1,534 y capitalización de US$26,000 M según CoinGecko al 25-sep-2026;
  - las L2 de Ethereum.
  Una tesis sobre esos activos debe pasar la lista de arriba.
- **Calidad técnica ≠ rendimiento del token.** El curso eleva la confianza en la tecnología, no en el precio de ningún token.

## 5. Contrapuntos y límites

- **Es de 2023.** No cubre lo posterior, como zkVMs de uso general, nuevos esquemas de *folding* y *lookups*, ni la evolución de la conjetura de FRI. **No verifiqué** cómo evolucionó esa conjetura después de 2023.
- **Las comparaciones son asintóticas o cualitativas.** El desempeño real depende de la implementación y del hardware.
- **Encuadre comercial:** clases invitadas de fundadores (Scroll, Aztec) y dos instructores ligados a a16z crypto.
- **No vi los videos:** mi lectura es solo de diapositivas, y algunas tablas numéricas no se pudieron leer.
- **Entender ZK no da ventaja de precio.** Los tokens de infraestructura ZK tuvieron un desempeño pésimo aunque la tecnología funcione (STRK −99%).

## 6. Autoexamen

1. **¿Por qué KZG necesita configuración confiable y qué pasa si alguien conserva τ?**
   - El compromiso es f(τ)·G y su seguridad supone que nadie conoce τ. Por eso la diapositiva dice "delete τ".
   - Quien conserve τ puede fabricar pruebas de evaluación falsas, es decir, "demostrar" valores que el polinomio no tiene.
   - PLONK-KZG hereda esa dependencia de la ceremonia.
   - *Fuente:* clase 5, diapositivas 4-8, y clase 8, diapositiva 7.
2. **Un STARK usa FRI con ρ = 1/8. ¿Cuántas consultas necesita para unos 100 bits y bajo qué supuesto?**
   - log₂(8) = 3 bits por consulta, así que unas 34 consultas.
   - Supone la conjetura de proximidad que usan la mayoría de los despliegues. Con solo lo demostrado harían falta más.
   - Además, al volverlo no interactivo se necesita más margen por los ataques de *grinding*.
   - *Fuente:* clase 8, diapositivas 50-53 y 76-79.
3. **¿Por qué un zkRollup puede no necesitar "conocimiento cero" y qué necesita en cambio?**
   - Su objetivo es que la L1 verifique rápido que un lote se procesó bien, así que necesita **sucintez**. No oculta datos: los publica.
   - El conocimiento cero hace falta en aplicaciones de privacidad.
   - *Fuente:* clase 2, diapositivas 7-8.
4. **¿Qué componente decide si un SNARK es transparente y plausiblemente poscuántico? Da un ejemplo de cada familia.**
   - Lo decide el esquema de compromiso polinomial.
   - KZG: ni transparente ni poscuántico.
   - Bulletproofs/IPA: transparente, no poscuántico.
   - FRI: transparente y plausiblemente poscuántico.
   - *Fuente:* clase 8, diapositivas 5 y 7.

## 7. Grado de evidencia: **A** en contenido técnico · **C** en implicaciones de inversión

- **A en lo técnico:**
  - es la fuente primaria académica;
  - las diapositivas las firman investigadores que crearon o analizaron estos sistemas;
  - cada tema remite a artículos revisados o a eprints (PLONK, KZG, FRI, Groth16).
- **Menos que A en lo reciente,** porque es de 2023 y no cubre lo posterior.
- **C en implicaciones de inversión:** el curso no habla de precios. Lo que deduzco para invertir es inferencia mía, apoyada en datos de mercado (CoinGecko) y en una fuente de prensa especializada (The Quantum Insider).

### Fuentes

- **Curso** (temario y reglas), consultado el 25-sep-2026: https://rdi.berkeley.edu/zk-learning/
- **Diapositivas en PDF:**
  - clase 2: `.../assets/Lecture2-2023.pdf`
  - clase 5: `.../assets/lecture5-2023.pdf`
  - clase 8: `.../assets/lecture8.pdf`
  - clase 12: `.../assets/lecture12.pdf`
  - privacidad: `.../assets/lecture_privacy.pdf`
  - clase 14: `.../assets/lecture14.pdf`
- **a16z crypto, equipo:** https://a16zcrypto.com/team/justin-thaler y https://a16zcrypto.com/team/dan-boneh/
- **Hashrate:** mempool.space API, consultado el 25-sep-2026.
- **Precios y máximos:** CoinGecko, 25-sep-2026 (STRK y ZEC).
- **StarkWare y computación cuántica:** The Quantum Insider, 30-jun-2026: https://thequantuminsider.com/2026/06/30/starkware-releases-roadmap-to-make-starknet-quantum-safe/
