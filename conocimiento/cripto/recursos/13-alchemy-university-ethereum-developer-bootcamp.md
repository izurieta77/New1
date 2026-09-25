# 13 · Alchemy University: Ethereum Developer Bootcamp

> **Estado:** estudiado · **Acceso:** sección (temario público y repositorios de dos proyectos; no me inscribí: el curso pide cuenta) · **Revisado:** 25-sep-2026 por `analista-cripto` · **Grupo:** G6 · **Grado global:** B/C

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2022, según el índice del dueño. La página actual no muestra fecha de última actualización. |
| Autor | Alchemy, empresa de infraestructura: nodos, APIs y SDKs para desarrolladores. |
| Tipo | Bootcamp en línea a tu ritmo: lecciones interactivas, videos, guías, proyectos semanales y un proyecto final. |
| Nivel | Intermedio. JavaScript es requisito previo. |
| Costo | Gratis ("Totally free"). La certificación es un NFT. |
| Idioma | Inglés. |
| URL | https://www.alchemy.com/university · curso: https://www.alchemy.com/university/courses/ethereum |
| **Conflictos de interés** | (1) Alchemy vende la infraestructura con la que se enseña. En el proyecto del explorador de bloques, el código inicial usa **AlchemySDK** en lugar de ethers.js puro, lo que crea dependencia comercial. (2) Las métricas de la página (1.6 M+ lecciones completadas, 108 k+ estudiantes, 28 k+ inscritos al bootcamp) son de marketing. (3) La "certificación oficial" la emite el mismo proveedor. |

## 2. Acceso real

- **Leí completas:**
  - la portada de Alchemy University: cursos, métricas y oferta;
  - la página del Ethereum Bootcamp: descripción, temario por secciones, número de lecciones, videos y proyectos.
- **Leí dos proyectos del bootcamp** por `raw.githubusercontent.com`:
  - el README de `alchemyplatform/ecdsa-node`, "Project 1: Build a Web App using ECDSA";
  - el README de `alchemyplatform/blockexplorer`.
- **No me inscribí.** Las lecciones requieren cuenta, así que no vi su contenido interno.
- **Nivel de acceso: sección.**

## 3. Lo esencial

1. **[H] Temario del bootcamp por secciones** (página del curso, 25-sep-2026):

   | Sección | Lecciones | Videos | Proyectos |
   |---|---|---|---|
   | Criptografía de blockchain | 15 | 5 | — |
   | Almacenamiento: balances y estructuras de datos | 13 | 3 | — |
   | Ethereum: la máquina de estados | 17 | — | — |
   | Bases de contratos inteligentes | 20 | — | 2 |
   | Solidity | 10 | — | 1 |
   | Núcleo de Solidity | 15 | — | 2 |
   | Gobierno de contratos | 6 | — | 2 |

2. **[H] Las cifras de la misma página no cuadran.** La cabecera dice "91 lessons". El temario anuncia "96 lessons, 14 videos, 7 projects". Las secciones suman **96 lecciones y 7 proyectos**, pero solo **8 videos**. Es una inconsistencia menor, pero dice cuánto cuidado hay en las cifras de marketing.
3. **[H] Oferta completa de AU:**
   - Introduction to Blockchain (43 lecciones);
   - Learn Solidity (11);
   - Learn JavaScript (49);
   - AA Fundamentals (ERC-4337, 3 horas de video);
   - Smart Accounts (ERC-6900).
4. **[H] Proyecto 1: web app con firmas ECDSA.**
   - Un servidor solo acepta transferencias firmadas por el dueño de la dirección.
   - El README reconoce que el diseño es "clearly very centralized" y que no trata el consenso distribuido.
5. **[H] Proyecto del explorador de bloques.**
   - Hay que construir un explorador propio "usando Etherscan como guía": datos de la red, bloques, transacciones y cuentas, con la API JSON-RPC y ethers.js.
   - El código inicial usa AlchemySDK, que "envuelve casi toda" la funcionalidad de ethers.js.
6. **[H] Proyecto final** para "official Alchemy certification" y certificado NFT al terminar.
7. **[H] Señal de mantenimiento pobre.** El pie de página de 2026 aún enlaza un "Mumbai Faucet". La propia Alchemy anunció el fin del soporte a la red de pruebas Mumbai de Polygon el 13-abr-2024 (migración a Amoy).
8. **[I] La sección de criptografía** (hashes, firmas y árboles de Merkle) es la base para entender la custodia de llaves y las pruebas de reservas de un exchange. Es la parte más útil para un inversionista.
9. **[I] El proyecto ECDSA muestra en pequeño la diferencia entre firmar y custodiar.** Aunque las firmas sean válidas, si un servidor central lleva el libro mayor, el riesgo es de contraparte. Es la lógica de un exchange centralizado.
10. **[I] El explorador de bloques es un buen ejercicio para dejar de depender de *dashboards* de terceros:** consultar tú mismo bloques, transacciones y saldos.
11. **[O] Opinión:** es buena ruta estructurada si ya sabes JavaScript. El sesgo hacia las herramientas de Alchemy es moderado y visible.

## 4. Qué cambia para invertir

- **Custodia.** Entender cómo se generan y usan las llaves (ECDSA) ayuda a juzgar riesgos como el de Coldcard (recurso 09): 1,816 BTC drenados por entropía débil al generar semillas, según TRM Labs y Galaxy Research.
- **Pruebas de reservas.** Los árboles de Merkle permiten a un cliente verificar que su saldo está incluido en el pasivo que declara un exchange. No prueban que no haya otros pasivos ocultos.
- **Dependencia de proveedores de nodos.** Muchas dApps leen la cadena a través de pocos proveedores (Alchemy, Infura y otros). Si el proveedor falla o censura, la interfaz falla aunque la cadena funcione.
- **Cartera actual (solo BTC spot en Binance):** refuerza la regla de retirar o no retirar a autocustodia con criterio. No tus llaves, no tus monedas. Y tus llaves mal generadas tampoco son tuyas.

## 5. Contrapuntos y límites

- **Es un proveedor que enseña con sus productos.**
- **No vi las lecciones**, solo el temario y dos proyectos.
- **Hay señales de contenido sin actualizar** (pie de página con Mumbai) y cifras inconsistentes en la misma página.
- **Una certificación NFT del proveedor no es una credencial independiente.**

## 6. Autoexamen

1. **¿Por qué el proyecto 1 (ECDSA) sigue siendo "muy centralizado" aunque use firmas digitales?**
   - Porque un solo servidor lleva los saldos y decide las transferencias. La firma prueba quién autoriza, pero no elimina la confianza en quien lleva el libro mayor.
   - *Fuente:* README de `alchemyplatform/ecdsa-node`.
2. **¿Qué inconsistencia hay entre la cabecera y el temario del bootcamp?**
   - La cabecera dice 91 lecciones. El temario dice 96 lecciones y 14 videos, pero las secciones suman 96 lecciones y 8 videos.
   - *Fuente:* página del curso, 25-sep-2026.
3. **¿Qué API estudian las lecciones y qué usa el código inicial del explorador de bloques?**
   - Las lecciones estudian JSON-RPC de Ethereum con ethers.js. El código inicial usa AlchemySDK.
   - *Fuente:* README de `alchemyplatform/blockexplorer`.

## 7. Grado de evidencia: **B/C**

- **B:** es fuente primaria sobre su temario y el código es abierto, pero las cifras de la página son inconsistentes y de marketing.
- **C en implicaciones para invertir:** son inferencia mía.

### Fuentes

- https://www.alchemy.com/university y https://www.alchemy.com/university/courses/ethereum, consultados el 25-sep-2026.
- https://raw.githubusercontent.com/alchemyplatform/ecdsa-node/main/README.md
- https://raw.githubusercontent.com/alchemyplatform/blockexplorer/main/README.md
- Alchemy, "Polygon Mumbai Support Ending April 13th": https://www.alchemy.com/blog/polygon-mumbai-testnet-deprecation
- TRM Labs sobre Coldcard, 5-ago-2026 (ver ficha 09).
