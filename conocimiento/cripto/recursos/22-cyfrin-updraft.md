# 22 · Cyfrin Updraft (plataforma de cursos)

- **Estado:** estudiado. **Acceso:** sección. Revisé el temario completo del curso de seguridad y de los dos de seguridad de carteras, y leí el texto de las lecciones clave. No vi los videos.
- **Grupo:** G4. **Autor de la ficha:** `analista-cripto`, 25-sep-2026.
- **Etiquetas:** [H] hecho con fuente · [I] inferencia · [O] opinión.

## 1. Ficha

| Campo | Valor |
|---|---|
| Año | 2024 según el índice del dueño. Algunos contenidos del curso de seguridad citan datos "a octubre de 2023". |
| Autor | Cyfrin, empresa de auditoría. Patrick Collins y equipo; hay lecciones con invitados (Tincho Abbate, Pashov, JohnnyTime y otros). |
| Tipo | Plataforma de cursos en video con lección escrita, repositorios en GitHub y certificaciones |
| Nivel | Intermedio-Avanzado. El catálogo va de principiante a avanzado. |
| Costo | Cursos gratis. Las certificaciones son exámenes: Solidity Smart Contract Developer (120 min, 80 preguntas) y Qualified Web3 Signer (60 min, 20 preguntas). **No verifiqué su precio.** |
| Idioma | Inglés, con subtítulos en "20+ idiomas" según la página del curso |
| URL | https://updraft.cyfrin.io/ · curso de seguridad: https://updraft.cyfrin.io/courses/security |
| Conflictos de interés | **Medios:** **1.** Cyfrin vende auditorías, herramientas (el analizador **Aderyn**) y auditorías competitivas (**CodeHawks**), y promueve **Solodit**; el curso los enseña. **2.** Cada sección abre con "un mensaje de" un patrocinador (GMX, Rocket Pool, Ankr, Curve), lo que genera sesgo favorable. **3.** Le conviene decir que la seguridad Web3 está "objetivamente mal" y que auditar vale la pena. |

## 2. Acceso real (25-sep-2026)

**Catálogo** (https://updraft.cyfrin.io/courses): **26 cursos**. Los relevantes para G4 son:
- Smart Contract Security;
- Assembly and Formal Verification;
- Web3 Wallet Security Basics;
- Advanced Web3 Wallet Security;
- Solana (ficha 33).

**Smart Contract Security.** La página indica "24 h, 281 lecciones, 6 proyectos, avanzado".
- Extraje el temario completo de 10 secciones, con los títulos de ~255 lecciones que están en la página.
- Leí el texto de estas lecciones:
  - "What is a Smart Contract Audit?";
  - "The Audit Process";
  - "Rekt Test";
  - "Top Web3 Attacks";
  - "Current State of Web3 Security";
  - "What if a Protocol I audit Gets Hacked?";
  - los estudios de caso (DoS, The DAO, Meebits, Sushi, Oasis, Parity y Polygon).

**Web3 Wallet Security Basics** (1 h, 17 lecciones) y **Advanced Web3 Wallet Security** (2 h, 13 lecciones).
- Revisé el temario y el texto de "Browser and Hardware Wallets", "Multi Signature Wallets", "Disaster Recovery", "Introduction Transactions Verification" y "Dont Trust the Website".
- El **estudio de caso de Bybit** solo existe en video y **no lo vi**.

**Certificaciones:** página leída.

**No revisé:** Assembly and Formal Verification, ni el resto de los cursos de desarrollo.

**Nivel: sección.**

## 3. Lo esencial

### El curso de seguridad

1. [H] **Temario del curso** (10 secciones):
   1. introducción;
   2. repaso (ERC-20 y 721, almacenamiento, codificación ABI, contratos actualizables);
   3. qué es una auditoría;
   4. primera auditoría (PasswordStore);
   5. PuppyRaffle;
   6. TSwap (AMM);
   7. ThunderLoan (préstamos relámpago);
   8. BossBridge (puente);
   9. MEV y gobernanza;
   10. cierre de la parte 1.
2. [H] **"Auditoría" es un nombre engañoso**; el curso prefiere "revisión de seguridad". Es **acotada en tiempo y no da garantías**: el término "auditoría" "puede insinuar una garantía o implicaciones legales" (lección "What is a Smart Contract Audit?").
3. [H] **El proceso tiene 3 fases:**
   - revisión inicial: alcance, reconocimiento, identificación de vulnerabilidades y reporte;
   - correcciones del protocolo;
   - revisión de las correcciones (lección "The Audit Process").
4. [H] **La "Rekt Test"** de Trail of Bits trae 11 preguntas de preparación ("Rekt Test"):
   - ¿están documentados los roles y privilegios?;
   - ¿y los servicios externos y oráculos?;
   - ¿hay un plan de respuesta a incidentes probado?;
   - ¿se documentan las mejores formas de atacar el sistema?;
   - ¿hay verificación de antecedentes del personal?;
   - ¿alguien del equipo tiene la seguridad en su rol?;
   - ¿se exigen **llaves de hardware** en producción?;
   - ¿hay invariantes probados en cada commit?;
   - ¿se usan herramientas automáticas?;
   - ¿hay auditorías externas y recompensas por fallos?;
   - ¿se mitigó el abuso contra los usuarios?
5. [H] **Principales vectores según la lección, con cifras de 2023 sin fuente primaria citada** ("Top Web3 Attacks"):
   - llaves privadas robadas: US$243 millones;
   - manipulación de recompensas: US$200 millones;
   - manipulación de oráculos: ~US$146 millones;
   - controles de acceso insuficientes: US$17 millones;
   - reentrada, incluida la de solo lectura: US$20.5 millones.
6. [H] **La lección sobre el estado de la seguridad Web3** dice:
   - "US$3.1 mil millones robados en hackeos cripto en 2022";
   - "~7% del valor total de DeFi" se lo llevan los hackers;
   - vectores principales: oráculos, recompensas y llaves robadas.
   - [I] Los US$3.1 mil millones coinciden con la cifra **solo DeFi** de Chainalysis. El total de 2022 fue **US$3.8 mil millones** ([Chainalysis, 1-feb-2023](https://www.chainalysis.com/blog/2022-biggest-year-ever-for-crypto-hacking/)), así que la lección confunde el alcance de la cifra.
7. [H] **Clases de vulnerabilidad que cubre el temario:**
   - control de acceso;
   - datos "privados" legibles on-chain;
   - DoS;
   - lógica de negocio;
   - **reentrada** (caso The DAO: en may-2016 tenía ~14% de todo el ETH, según la lección);
   - aleatoriedad débil (Meebits, may-2021: un NFT raro vendido en US$700 mil);
   - desbordamiento de enteros y conversiones inseguras;
   - mal manejo de ETH (el `batch` de Sushi);
   - **centralización** (caso Oasis);
   - **falla de inicialización** (Parity);
   - **manipulación de oráculos**;
   - "depositar en vez de pagar";
   - **colisión de almacenamiento**;
   - firmas y EIP-712 (caso Polygon: recompensa de US$2.2 millones por un fallo "de US$7 mil millones", según la lección);
   - `transferFrom` arbitrario;
   - acuñación infinita;
   - **repetición de firmas**;
   - llamada de bajo nivel a sí mismo;
   - "gas bomb";
   - MEV;
   - ataque de gobernanza (Beanstalk).
8. [H] **Herramientas:** Slither, Aderyn (de Cyfrin), fuzzing sin estado y con estado, invariantes y Solodit.
9. [H] **Postura ante un hackeo en código auditado** (Tincho, en "What if a Protocol I audit Gets Hacked?"):
   - el auditor es un eslabón, no el único responsable;
   - hay que acompañar al cliente en la crisis.

### Los cursos de seguridad de carteras

10. [H] **Concepto de "small monies"** ("Browser and Hardware Wallets"): la cantidad que uno aceptaría perder.
    - La cartera de navegador es "dinero de bolsillo".
    - Montos que dolerían van a hardware o multisig.
11. [H] **Multisig "X de Y":**
    - es un contrato, no una cuenta con una sola llave;
    - exige X firmas de Y firmantes;
    - es la opción favorita del instructor para montos altos y para protocolos.
12. [H] **Regla de oro** ("Dont Trust the Website"): **"No confíes en lo que muestra el sitio web; confía solo en tu cartera".**
    - El ejercicio: el sitio muestra 5 ETH cuando la intención era enviar 0.5.
    - El dispositivo de hardware es "la fuente de verdad".
13. [H] **Recuperación ante desastres:**
    - la frase semilla y las llaves privadas nunca se comparten;
    - se respaldan en varios lugares seguros;
    - "no hay soporte ni botón de 'olvidé mi contraseña'".
14. [H] **El curso avanzado** enseña:
    - a configurar una Safe;
    - a verificar las firmas de una multisig (EIP-712: hash de dominio y de mensaje);
    - el caso Bybit (solo video).

### Opiniones e inferencias

15. [O] "El estado actual de la seguridad Web3 es objetivamente terrible" ("Current State of Web3 Security").
16. [O] "Gastar US$1 millón en seguridad ahora vale más que ahorrar US$100 millones perdidos en un hackeo" (misma lección).
17. [I] **Para un inversionista, lo más valioso no es el Solidity**, sino:
    - (a) la Rekt Test como **lista de debida diligencia** de un proyecto;
    - (b) la diferencia entre "auditoría" y garantía;
    - (c) los cursos de carteras para verificar lo que se firma.

## 4. Qué cambia para invertir

### Riesgo de exchange (lección de FTX aplicada a Binance)
- [I] **Adaptar la Rekt Test a un exchange centralizado:**
  - ¿tiene plan de incidentes probado?;
  - ¿llaves de hardware?;
  - ¿verificación de antecedentes?;
  - ¿responsable de seguridad?;
  - ¿recompensas por fallos?
- [H] **Dos casos muestran que la falla estaba en las personas:**
  - Coinbase: sobornos a personal de soporte (8-K del 14-may-2025);
  - Corea del Norte: infiltra trabajadores de TI en exchanges (Chainalysis, ficha 32).
- [H] FTX no tenía controles básicos (declaración del nuevo director, ficha 17).
- [H] **Binance dice que 1,500 personas, ~25% de su plantilla, trabajan en cumplimiento** (blog de feb-2026, citado por [CoinDesk](https://www.coindesk.com/policy/2026/09/22/binance-probed-by-u-s-federal-prosecutors-for-sanctions-violations-bloomberg)). Es un dato de la propia empresa.
- [I] No encontré evidencia independiente de la calidad de sus controles. El historial público es la declaración de culpabilidad de 2023 (ficha 17).

### Riesgo de stablecoin
- [H] **El estudio de caso Oasis enseña el riesgo de centralización:** un protocolo que se decía "descentralizado" usó sus permisos de administrador, por orden de un tribunal, para mover los fondos de un atacante (lección "Case Study: Oasis").
- [I] Todo emisor de stablecoin y todo token con funciones de administración puede congelar o mover saldos. En un evento de 2026, Circle y Tether congelaron fondos del hackeo a Bitget (ficha 32).

### Hackeos de exchanges y de puentes
- [H] **BossBridge enseña los ataques de puente de libro:**
  - `transferFrom` arbitrario;
  - acuñación infinita;
  - repetición de firmas;
  - llamada de bajo nivel a sí mismo.
- [H] **En producción:**
  - Ronin (5 de 9 llaves, 2022);
  - KelpDAO (un solo verificador, 2026) (fichas 17 y 25).
- [I] **Preguntas de diligencia para un puente:**
  - ¿cuántos firmantes o verificadores hay y quién los opera?;
  - ¿hay límites de flujo y cortacircuitos? Tras el hackeo, Ronin anunció que subiría el umbral a 8 de 9 ([post-mortem](https://roninchain.com/blog/posts/back-to-building-ronin-security-breach-6513cc78a5edc1001b03c364)).

### Autocustodia
- [H] **Reglas prácticas del curso:**
  1. "Small monies" en cartera de navegador; lo que duela, en hardware o multisig.
  2. **Verificar en la pantalla del dispositivo**, no en el sitio.
  3. Respaldar la frase semilla fuera de línea y en varios lugares.
  4. En una multisig, verificar los hashes EIP-712.
- [I] Encaja con Bybit: los firmantes aprobaron en una interfaz comprometida lo que su verificación no revisó (ficha 25).
- [I] **Para nuestra cuenta:** si algún día se retira BTC a autocustodia, usar hardware con verificación en pantalla y probar la recuperación con un monto mínimo antes de mover el resto.

### Cómo leer una prueba de reservas
- [I] **La lección central se traslada tal cual:** una revisión es **acotada en tiempo y en alcance** y **no es una garantía**.
- [I] **Con PoR y atestaciones hay que preguntar:**
  - ¿qué alcance tiene?;
  - ¿quién la hizo?;
  - ¿qué no revisó?
- [I] Ejemplos de esa distinción:
  - la atestación de BDO de Tether frente a la auditoría de KPMG (ficha 17);
  - Mazars dejó de hacer PoR para exchanges en dic-2022 por cómo "el público las entendía" (lista de señales).

## 5. Contrapuntos y límites
- **Material de un proveedor:** promueve sus herramientas y a sus patrocinadores.
- **Estadísticas sin fuente primaria** y con alcances confundidos (la de 2022). No usarlas sin verificar.
- **Parte del contenido es de 2023.** La foto de "principales vectores" no refleja 2025-2026, cuando dominaron ataques operativos a exchanges y puentes (Chainalysis).
- **Solo lo técnico:** no cubre el riesgo de contraparte de exchanges centralizados, ni la regulación, ni la solvencia.
- **No vi videos**, y el caso Bybit solo está en video.

## 6. Autoexamen

**1. ¿Por qué Cyfrin prefiere "revisión de seguridad" a "auditoría" y qué implica al leer "auditado por X" en un proyecto?**
- Porque "auditoría" puede insinuar garantía o responsabilidad legal. Una revisión es acotada en tiempo y busca el mayor número de fallos, sin garantizar que no haya más.
- "Auditado" no equivale a "seguro"; hay que preguntar alcance, fecha, hallazgos pendientes y monitoreo posterior.
- Fuente: Updraft, "What is a Smart Contract Audit?".

**2. Menciona 5 preguntas de la Rekt Test y cómo las aplicarías a un exchange.**
- Plan de incidentes probado; llaves de hardware en producción; verificación de antecedentes; responsable de seguridad; recompensas por fallos y auditorías externas. También invariantes probados, documentación de roles y privilegios y mitigación del abuso contra usuarios.
- En un exchange: ¿qué pasó en su último incidente?, ¿quién firma retiros y con qué dispositivos?, ¿cómo controla al personal de soporte?
- Fuente: Updraft, "Rekt Test".

**3. ¿Qué error de alcance tiene la cifra de "US$3.1 mil millones robados en 2022" del curso?**
- Esos US$3.1 mil millones son lo robado **a protocolos DeFi** (82.1% del total).
- El total de hackeos cripto de 2022 fue **US$3.8 mil millones**, y 64% de lo robado en DeFi vino de puentes.
- Fuente: Chainalysis (1-feb-2023); Updraft, "Current State of Web3 Security".

**4. ¿Cuál es la "regla de oro" de los cursos de carteras y qué caso de 2025 la ilustra?**
- "No confíes en el sitio web, confía solo en lo que muestra tu cartera o dispositivo".
- Bybit (21-feb-2025): la interfaz de Safe{Wallet} fue alterada y los firmantes aprobaron una transacción que cambió la lógica de su cold wallet. Costó ~US$1.46 mil millones.
- Fuentes: Updraft, "Dont Trust the Website"; Sygnia y Bybit.

## 7. Grado de evidencia: **B** (contenido técnico) / **C** (cifras de las lecciones)
- **B:** lo imparten practicantes reconocidos, el contenido técnico es verificable (código, EIP) y los repositorios son públicos.
- **C:** las estadísticas de las lecciones no citan fuente primaria, o confunden su alcance.
