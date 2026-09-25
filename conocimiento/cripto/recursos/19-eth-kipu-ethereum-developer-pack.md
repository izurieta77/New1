# 19 · ETH Kipu: Ethereum Developer Pack

> **Estado:** estudiado · **Acceso:** sección amplia. Leí la estructura completa de los dos niveles y las secciones clave de las clases de seguridad, auditoría, verificación y L2. Es el mismo texto que muestra la aplicación web pública; lo tomé de su paquete JavaScript. No leí cada clase entera. · **Revisado:** 25-sep-2026 por `analista-cripto` · **Grupo:** G6 · **Grado global:** B en contenido; C en resultados.

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2023, según el índice del dueño. El contenido actual menciona la actualización Pectra (2025) y trabajos de 2025 sobre auditoría con IA; la fecha de última revisión no aparece. |
| Autor | ETH Kipu, "una fundación sin fines de lucro que promueve la adopción de Ethereum a través de la educación" (sitio). |
| Tipo | Curso en línea con comunidad: "Ethereum Developer Pack", en dos niveles, con ejercicios, actividades y proyecto final. |
| Nivel | Nivel 1: introducción a Ethereum y Solidity. Nivel 2: *Smart Contract Developer* (profundización). |
| Costo | El índice del dueño dice "Gratis". **En el sitio no encontré** mención de precio ni de gratuidad (busqué "gratis" y "gratuito": cero resultados). |
| Idioma | Español rioplatense, con versión en inglés. |
| URL | https://ethkipu.org/ · https://ethkipu.org/ethereumdeveloperpack |
| **Conflictos de interés** | (1) Su misión declarada es promover la adopción de Ethereum, así que el sesgo pro-Ethereum es explícito. (2) Colabora con el Ministerio de Educación de la Ciudad de Buenos Aires (reporte "ETH Kipu – GCBA", 2024-2025). (3) La clase 18 dedica espacio a Stylus (Arbitrum) y Cairo (StarkWare). **No encontré** en el sitio quién financia la fundación ni si esos ecosistemas la patrocinan. |

## 2. Acceso real

- **Leí completas:**
  - la portada del sitio: misión, niveles y reporte con el gobierno de la Ciudad de Buenos Aires;
  - la estructura de **ambos niveles**: títulos y descripciones de todos los módulos y títulos de las 18 clases del nivel 2.
- **Leí a fondo** las secciones de:
  - vectores de ataque (clase 16);
  - auditoría (clase 17);
  - verificación y depuración (clase 11);
  - la actividad con L2BEAT;
  - la actividad de *bytecode* en Etherscan;
  - la "higiene digital" para usuarios.
- **Cómo lo obtuve:** el sitio es una aplicación que carga su texto desde un archivo JavaScript público. Lo descargué y extraje el texto en español. Es el contenido que cualquiera ve al navegar.
- **No me inscribí** ni entregué el proyecto final. No verifiqué si hay cohortes, tutores o certificados.
- **Nivel de acceso: sección amplia.**

## 3. Lo esencial

1. **[H] Nivel 1: Introducción a Ethereum y Solidity.**
   - Módulo 1: fundamentos de blockchain, Bitcoin y Ethereum, hasta la EVM.
   - Módulo 2: transacciones, *wallets* y gas.
   - Módulo 3: gobernanza, tokenización y escalabilidad (EIPs, The Merge, DAOs, L2).
   - Módulo 4: DeFi y dApps.
   - Módulo 5: desarrollo con Solidity.
2. **[H] Nivel 2: *Smart Contract Developer*, 18 clases.**
   - Módulo 0: introducción y primer contacto con Solidity.
   - Módulo 1: la EVM (storage, memory, opcodes).
   - Módulo 2: estructura, estándares y seguridad en Solidity (librerías, OpenZeppelin, *proxies* actualizables).
   - Módulo 3: frameworks, pruebas y depuración (Hardhat, Foundry con *fuzzing* y *cheatcodes*, verificación de contratos y Tenderly).
   - Módulo 4: dApps y DeFi (Ethers.js/Wagmi, AMMs de Uniswap, oráculos de Chainlink, arquitectura de protocolos).
   - Módulo 5: seguridad, auditoría y gobernanza (vectores de ataque, Slither, gobernanza, Stylus y Cairo).
3. **[H] Vectores de ataque (clase 16):**
   - `receive()`/`fallback()`;
   - validación de entradas;
   - no usar `tx.origin` para autorizar;
   - **reentrada**, "el fantasma de The DAO", con *pull payments* como defensa;
   - *overflows*;
   - **MEV**: *front-running* y *sandwich*;
   - control de acceso;
   - negación de servicio.
   Recomienda que el *owner* sea un **multisig (p. ej., Gnosis Safe) o una DAO**, porque "si la clave privada del owner es robada, el protocolo entero cae".
4. **[H] Auditoría (clase 17).** "El objetivo no es alcanzar el 'riesgo cero' (que no existe), sino reducir la superficie de ataque." Contrasta dos métodos:
   - **análisis estático:** rápido, cubre todo, pero da falsos positivos y no entiende la lógica de negocio;
   - **revisión manual:** detecta fallas de incentivos, manipulación de oráculos y teoría de juegos, pero es lenta y falible.
5. **[H] Slither**, de Trail of Bits, según el curso, "identifica más de 70 vulnerabilidades comunes". Es la cifra del curso; no la verifiqué contra la documentación de Slither.
6. **[H] Lista mínima antes de desplegar** (clase 17):
   - cero advertencias críticas en Slither;
   - al menos **95% de cobertura** de pruebas;
   - documentación NatSpec;
   - control de acceso verificado a mano;
   - patrón *Checks-Effects-Interactions*.
7. **[H] "Una auditoría no garantiza seguridad absoluta"** (clase 17). Los protocolos auditados pueden sufrir incidentes por:
   - errores de diseño;
   - cambios futuros;
   - nuevas técnicas de ataque;
   - dependencias comprometidas;
   - problemas operativos.
8. **[H] Auditoría con IA.** El curso cita AuditGPT (2024) y SmartAuditFlow (2025) como líneas de investigación.
9. **[H] Verificación y exploradores (clase 11).**
   - Sin verificación, el contrato es una "caja negra" de *bytecode*. Verificar vincula el Solidity con ese *bytecode*.
   - En Etherscan, *Read Contract* ejecuta funciones `view` sin gas: `balanceOf`, `owner`, `totalSupply`.
   - *Write Contract* exige conectar la *wallet*, firmar y pagar gas.
   - Tenderly permite simular transacciones y crear "Virtual Testnets" con estado real.
10. **[H] Actividad del nivel 1 en Etherscan.** Abrir un contrato popular (el de USDC), ir a la pestaña *Contract* y observar el *Contract Bytecode*: "eso es lo que la EVM interpreta realmente".
11. **[H] Actividad con L2BEAT** (nivel 1, módulo 3). Analizar Arbitrum, Optimism, zkSync, Starknet y Base, e identificar:
    - TVL;
    - tipo de *rollup*;
    - **tiempo de retiro**;
    - **centralización del secuenciador**;
    - capa de disponibilidad de datos (DA).
12. **[H] Higiene digital para usuarios:**
    - antes de depositar, verificar si el protocolo fue auditado por firmas reconocidas (OpenZeppelin, Trail of Bits);
    - limpiar permisos (*allowances*) viejos o ilimitados con Revoke.cash;
    - usar *hardware wallets*;
    - verificar la URL: el *phishing* "es la causa más común de pérdida de fondos".
13. **[H] Escalabilidad.** Explica Dencun y EIP-4844 (*blobs*, 2024), que abarataron la publicación de datos de las L2, y rollups optimistas (Arbitrum, Optimism) frente a rollups ZK (zkSync, Starknet).
14. **[I] Es la ruta que más se acerca a lo que necesita un inversionista:** exploradores, verificación, riesgos de L2 y límites de las auditorías, en español.
15. **[O] Opinión:** buena primera ruta para el dueño. Nivel 1 completo y, del nivel 2, las clases 11, 16 y 17 aunque no programe.

## 4. Qué cambia para invertir

- **Lista de revisión de un protocolo DeFi o una L2**, basada en el curso:
  1. ¿El contrato está verificado en el explorador?
  2. ¿El *owner* o *admin* es una persona, un multisig o una DAO, y hay *timelock*?
  3. ¿Es actualizable (*proxy*)?
  4. ¿Qué auditorías tiene, de quién y sobre qué versión del código?
  5. En L2BEAT: tiempo de retiro, secuenciador y DA.
  6. ¿Qué permisos le he dado y siguen vivos (Revoke.cash)?
- **Una auditoría reduce riesgo, no lo elimina** (clase 17). El precio de un token de protocolo debe descontar el riesgo técnico residual aunque diga "auditado".
- **Cartera actual (solo BTC spot en Binance):** la sección de higiene digital (*phishing*, *hardware wallets*, permisos) aplica directamente a la custodia de BTC.

## 5. Contrapuntos y límites

- **Transparencia mínima de la fundación:** no encontré en el sitio financiamiento, costo, fecha de actualización ni cifras de alumnos. La sección de impacto muestra etiquetas ("Años de experiencia", "Estudiantes", "Ciudades") pero no vi los números en el texto extraído.
- **Nadie ha evaluado de forma independiente la calidad del curso.**
- **Mi acceso fue por el contenido público de la aplicación, no como alumno inscrito.**
- **Sesgo pro-Ethereum declarado** en su misión.

## 6. Autoexamen

1. **Según el curso, ¿por qué conviene que el *owner* de un protocolo sea un multisig o una DAO?**
   - Porque si roban la clave privada de un *owner* individual, "el protocolo entero cae". Un multisig o una DAO reparten ese punto único de falla.
   - *Fuente:* clase 16, "Gestión de Privilegios y Control de Acceso".
2. **¿Qué cinco datos pide identificar la actividad de L2BEAT y por qué importan dos de ellos al inversionista?**
   - TVL, tipo de *rollup*, tiempo de retiro, centralización del secuenciador y capa de DA.
   - El **tiempo de retiro** dice cuánto tardas en sacar tu dinero a L1.
   - La **centralización del secuenciador** dice si un solo operador puede censurar o detener la red.
   - *Fuente:* nivel 1, módulo 3, "Actividad".
3. **Nombra tres razones por las que un protocolo auditado puede sufrir un incidente.**
   - Errores de diseño, cambios futuros al código, nuevas técnicas de ataque, dependencias comprometidas o problemas operativos (basta con tres).
   - *Fuente:* clase 17, "Una Auditoría No Garantiza Seguridad Absoluta".
4. **¿Qué diferencia hay entre *Read Contract* y *Write Contract* en Etherscan?**
   - *Read* ejecuta funciones `view`/`pure` sin gas ni firma, como `owner` o `totalSupply`.
   - *Write* modifica el estado: exige conectar la *wallet*, firmar y pagar gas.
   - *Fuente:* clase 11, "Exploradores de Bloques y Verificación".

## 7. Grado de evidencia: **B** (contenido) · **C** (resultados e implicaciones)

- **B en contenido:** es fuente primaria sobre su temario, coincide con el consenso técnico de las otras rutas (14, 10, 13) y cita herramientas y trabajos verificables.
- **C en resultados:** no hay evidencia pública de resultados de aprendizaje ni evaluación independiente.
- **C en implicaciones de inversión:** son inferencia mía.

### Fuentes

- https://ethkipu.org/, contenido del Developer Pack en el paquete público `/assets/index-C2UTM4MV.js`, consultado el 25-sep-2026.
- https://l2beat.com: la herramienta que el curso usa en la actividad de L2.
