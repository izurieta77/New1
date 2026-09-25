# 14 · Learn Blockchain, Solidity & Full Stack Web3 Development with JavaScript (Patrick Collins, freeCodeCamp, ~32 h)

> **Estado:** estudiado por índice y repositorio · **Acceso:** sección (índice completo de capítulos con marcas de tiempo, README del repositorio y artículos de freeCodeCamp y Chainlink; **no vi el video**) · **Revisado:** 25-sep-2026 por `analista-cripto` · **Grupo:** G6 · **Grado global:** B en contenido y C en vigencia.

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2022. freeCodeCamp lo anunció el 26-may-2022 y Chainlink el 27-may-2022. |
| Autor | Patrick Collins, entonces "Chainlink Labs Software Engineer and Developer Advocate", según el blog de Chainlink. Lo publicó freeCodeCamp. |
| Tipo | Curso completo en YouTube de unas 32 horas, dividido en lecciones 0 a 18, con todo el código en GitHub. |
| Nivel | Principiante a intermedio en desarrollo. |
| Costo | Gratis. |
| Idioma | Inglés. |
| URL | https://www.youtube.com/watch?v=gyMwXuJrbJQ · repositorio: https://github.com/smartcontractkit/full-blockchain-solidity-course-js |
| **Conflictos de interés** | (1) **Chainlink.** El repositorio vive en la organización de GitHub de Chainlink Labs (`smartcontractkit`) y el README agradece a Chainlink Labs "for encouraging this course". El curso enseña oráculos, VRF y Automation de Chainlink (lecciones 4 y 9). (2) **Cyfrin.** El README ahora redirige a Cyfrin Updraft, la plataforma de la empresa de auditoría que fundó Collins (recurso 22 del índice). (3) **Duración.** freeCodeCamp habla de "30-hour course" en el texto y de 32 horas en el título; Chainlink dice "30+ hour". |

## 2. Acceso real

- **Leí completo el README del repositorio** (2,177 líneas), que incluye:
  - el aviso de que ya no se mantiene;
  - el índice de las lecciones 0 a 18 con marcas de tiempo del video;
  - los recursos por lección;
  - la sección de seguridad y auditoría;
  - la lista de "¿qué sigue?".
- **Leí también** el anuncio de freeCodeCamp (26-may-2022) y el del blog de Chainlink (27-may-2022).
- **No vi el video.** yt-dlp está bloqueado aquí y YouTube respondió 429 a la descarga de la página.
- **Nivel de acceso: sección.**

## 3. Lo esencial

1. **[H] Aviso vigente del repositorio:** "This repo is no longer actively maintained…". Motivos:
   - las herramientas de Hardhat cambiaron;
   - "the video is out of sync with the code";
   - "best practices have evolved".
   Recomienda Cyfrin Updraft, que usa Foundry y no Hardhat.
2. **[H] Advertencia del propio curso:** "All code associated with this course is for demo purposes only. They have not been audited and should not be considered production ready."
3. **[H] Índice con marcas de tiempo** (README):

   | Lección | Tema | Inicio |
   |---|---|---|
   | 0 | Bienvenida | 00:00:00 |
   | 1 | Fundamentos de blockchain | 00:09:05 |
   | 2 | Remix, Simple Storage | 02:01:16 |
   | 3 | Storage Factory | 03:05:34 |
   | 4 | Fund Me (primer uso de oráculos Chainlink) | 03:31:55 |
   | 5 | Ethers.js | 05:30:42 |
   | 6 | Hardhat, Simple Storage | 08:20:17 |
   | 7 | Hardhat, Fund Me | 10:00:48 |
   | 8 | Front end en HTML y JavaScript | 12:32:57 |
   | 9 | Lotería (Chainlink VRF y Automation) | 13:41:02 |
   | 10 | Lotería en NextJS | 16:34:07 |
   | 11 | Starter kit | 18:51:36 |
   | 12 | ERC-20 | 18:59:24 |
   | 13 | DeFi y Aave | 19:16:13 |
   | 14 | NFTs | 20:28:51 |
   | 15 | Marketplace de NFTs | 23:37:03 |
   | 16 | Contratos actualizables | 28:53:11 |
   | 17 | DAOs | 29:45:24 |
   | 18 | **Seguridad y auditoría** | **31:28:32** |

4. **[H] Contenido de la lección 18:**
   - guía de preparación para auditorías de OpenZeppelin;
   - **Slither** (análisis estático) y **Echidna** (*fuzzing*), con el *toolbox* de Trail of Bits;
   - buenas prácticas y ataques (reentrada y manipulación de oráculos con préstamos relámpago);
   - Damn Vulnerable DeFi y Ethernaut para practicar;
   - auditores de ejemplo: OpenZeppelin, SigmaPrime y Trail of Bits.
5. **[H] Verificación de contratos.** El curso enseña a verificar contratos en exploradores de bloques desde la interfaz y por programa (Etherscan, `hardhat-etherscan`).
6. **[H] Qué tan completo es.** Recorre el ciclo *full-stack*: contrato, pruebas, despliegue, front end, estándares (ERC-20, NFTs), DeFi (Aave), contratos actualizables y gobernanza. Es el curso gratuito más citado para empezar, aunque hoy está desactualizado.
7. **[I] Qué implican los contratos actualizables (lección 16).** Con un *proxy*, la lógica de un contrato "inmutable" la puede cambiar quien tenga la llave de administración. El inversionista debe buscar quién la tiene y si hay *timelock*.
8. **[I] Cuánto pesa la seguridad.** Llega hasta la hora 31 de 32. El curso forma constructores; la seguridad es un anexo.
9. **[I] Sesgo de proveedor.** El Fund Me y la lotería dependen de Chainlink. El alumno aprende "oráculo = Chainlink" antes de ver alternativas y sus riesgos.
10. **[O] Opinión:** sirve para entender la mecánica. Para aprender a programar hoy, conviene la versión actualizada con Foundry, que el propio repositorio recomienda.

## 4. Qué cambia para invertir: cómo leer un contrato en un explorador de bloques

Es la destreza práctica que deja este curso, combinada con la ficha 19:

1. **Código verificado.** En Etherscan, la pestaña *Contract* debe mostrar el código fuente verificado. Sin eso, el contrato es una "caja negra" de *bytecode*.
2. ***Proxy*.** Si el contrato es un *proxy* ("Read as Proxy"), el código real está en la dirección de implementación, que puede cambiar. Busca quién es el *admin* y si existe *timelock*.
3. ***Read Contract*.** Revisa `owner()`, roles, `paused()`, `totalSupply()` y los parámetros críticos. Sin gas y sin firmar.
4. **Eventos.** Revisa si hubo cambios de dueño, actualizaciones o acuñaciones grandes.
5. ***Write Contract*.** Casi nunca debe usarlo un inversionista. Firmar una aprobación ilimitada a un contrato desconocido es una de las vías de robo más comunes.
6. **Auditorías.** Son un piso, no un techo. El curso lista a los auditores de referencia. El 17-sep-2026, S&P Global anunció la compra de OpenZeppelin. El comunicado dice que sus contratos respaldan "más de US$37 billones (millones de millones) transferidos" y que suma "900+" encargos de seguridad. Es una señal de que la auditoría se institucionaliza, no de que elimine el riesgo.

## 5. Contrapuntos y límites

- **Desactualizado** en herramientas: Hardhat de 2022, redes de prueba retiradas. El propio autor lo dice.
- **Sesgo hacia Chainlink** y ahora redirección comercial a Cyfrin.
- **No vi el video.** Mi lectura sale del índice y de los recursos por lección.
- **La lección de seguridad es breve** frente al resto; no hace auditor a nadie.

## 6. Autoexamen

1. **¿Por qué el repositorio dice que el video ya no coincide con el código y qué recomienda?**
   - Porque las herramientas de Hardhat cambiaron y las buenas prácticas evolucionaron.
   - Recomienda Cyfrin Updraft, con Foundry.
   - *Fuente:* README del repositorio, sección "Update".
2. **¿En qué lección y a qué hora empieza la seguridad y qué herramientas enseña?**
   - En la lección 18, a las 31:28:32.
   - Enseña Slither (análisis estático), Echidna (*fuzzing*) y el *toolbox* de Trail of Bits, además de retos como Damn Vulnerable DeFi y Ethernaut.
   - *Fuente:* README, "Lesson 18: Security & Auditing".
3. **¿Qué relación tenía el autor con Chainlink y qué productos de Chainlink enseña?**
   - Era *Software Engineer and Developer Advocate* de Chainlink Labs.
   - Enseña oráculos o *data feeds* (lección 4), VRF y Automation (lección 9).
   - *Fuente:* blog de Chainlink, 27-may-2022.
4. **Si un contrato de un protocolo es un *proxy*, ¿qué dos cosas revisas en el explorador?**
   - La dirección de implementación actual (y su historial de cambios).
   - Quién controla la llave de *admin* o actualización: si es un multisig, una DAO o un *timelock*.
   - *Fuente:* lección 16 del índice y ficha 19 (clase 11 de ETH Kipu).

## 7. Grado de evidencia: **B** (contenido) · **C** (vigencia e implicaciones)

- **B en contenido:** el índice y el código son fuente primaria verificable.
- **C en vigencia:** el propio autor declara el curso fuera de sincronía, y hay conflicto de interés con Chainlink y Cyfrin.
- **C en implicaciones de inversión:** son inferencia mía, apoyada en hechos verificados, como el comunicado de S&P Global.

### Fuentes

- README: https://raw.githubusercontent.com/smartcontractkit/full-blockchain-solidity-course-js/main/README.md
- freeCodeCamp, 26-may-2022: https://www.freecodecamp.org/news/learn-blockchain-solidity-full-stack-javascript-development/
- Chainlink, 27-may-2022: https://chain.link/blog/learn-blockchain-full-stack-web3-javascript-smart-contract-development
- S&P Global, 17-sep-2026: https://press.spglobal.com/2026-09-17-S-P-Global-Announces-Agreement-to-Acquire-OpenZeppelin
