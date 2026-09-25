# 10 · Speedrun Ethereum (Austin Griffith y BuidlGuidl)

> **Estado:** estudiado · **Acceso:** sección (temario público completo y repositorios; no completé retos) · **Revisado:** 25-sep-2026 por `analista-cripto` · **Grupo:** G6 · **Grado global:** B como descripción de su contenido; C como evidencia para invertir.

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2021, según el índice del dueño. La versión actual usa Scaffold-ETH 2. |
| Autor | Austin Griffith y BuidlGuidl. |
| Tipo | Curso práctico por retos: se construye y despliega una dApp en cada uno. |
| Nivel | Intermedio: exige saber JavaScript o TypeScript y usar la terminal. |
| Costo | Gratis. Solo pide una wallet y ETH de red de pruebas. |
| Idioma | Inglés. |
| URL | https://speedrunethereum.com/ · retos: https://github.com/scaffold-eth/se-2-challenges |
| **Conflictos de interés** | (1) BuidlGuidl se presenta como "socio técnico de largo plazo de la Ethereum Foundation" y cobra por construir herramientas y cursos para L2s, DAOs y empresas: el sesgo es pro-Ethereum. (2) El curso se enseña con su propio kit (Scaffold-ETH 2), que así gana adopción. (3) Las métricas que publica (10k visitas al mes a SpeedRunEthereum; 1.5k instalaciones semanales de Scaffold-ETH 2) son propias y sin auditar. No encontré token ni patrocinio de exchanges. |

## 2. Acceso real

- **Leí completos:**
  - la portada de speedrunethereum.com: los 10 retos, ETH Tech Tree, un CTF y guías;
  - el README de `scaffold-eth/se-2-challenges`, con la descripción de cada reto y el punto de control de "Onboarding batches";
  - el README de `scaffold-eth/scaffold-eth-2`: stack y requisitos;
  - la portada de buidlguidl.com: quién financia y a quién sirve.
- **No hice ningún reto** ni desplegué contratos. No leí el código de cada rama de reto.
- La API de GitHub estaba bloqueada en esta sesión; los README los leí por `raw.githubusercontent.com`.
- **Nivel de acceso: sección.**

## 3. Lo esencial

1. **[H] Los 10 retos, en orden** (portada, 25-sep-2026):
   - #0 Tokenización: acuñar un NFT.
   - #1 Crowdfunding.
   - #2 Token Vendor: un ERC-20 con el patrón `approve`.
   - #3 Dice Game: atacar aleatoriedad débil.
   - #4 DEX: un AMM de reservas.
   - #5 Oráculos: lista blanca → *staking* → optimista con periodo de disputa.
   - #6 Préstamos sobrecolateralizados, con liquidación.
   - #7 Stablecoin: "MyUSD" colateralizada, con liquidación.
   - #8 Mercados de predicción.
   - #9 Votación con pruebas ZK.
2. **[H] Premisa del curso:** con Ethereum "los usuarios solo tienen que confiar en el código, no entre ellos" (reto #1). Si el código falla, en el peor caso cada quien recupera su dinero.
3. **[H] Aleatoriedad.** El reto #3 enseña que el *hash* del bloque es aleatoriedad "muy débil": el alumno ataca el juego con su propio contrato, que predice la tirada.
4. **[H] Precio del DEX.** En el reto #4 el precio sale de la razón entre las reservas del contrato, y los proveedores de liquidez reciben un token por su parte de reservas y comisiones.
5. **[H] Oráculos.** El reto #5 compara tres diseños y sus concesiones de seguridad: lista blanca, *staking* con penalizaciones y oráculo optimista con disputa.
6. **[H] Colateral.** Los retos #6 y #7 obligan a pensar qué pasa cuando cae el colateral: umbrales, liquidaciones y quién las ejecuta.
7. **[H] Mentoría.** Después del DEX hay un punto de control, "Onboarding batches", con mentoría de miembros de BuidlGuidl.
8. **[H] Stack.** Scaffold-ETH 2 usa NextJS, RainbowKit, Foundry o Hardhat, Wagmi, Viem y TypeScript, y pide Node ≥ v22.10. Se anuncia "AI-ready", con carpetas de configuración para agentes.
9. **[H] Extras:** "ETH Tech Tree" (retos avanzados) y un CTF de 12 retos para hackear contratos.
10. **[I] Los retos #3, #5, #6 y #7 son, en miniatura, los mecanismos por donde más dinero se ha perdido en DeFi:** aleatoriedad manipulable, oráculos manipulables, cascadas de liquidación y stablecoins que pierden la paridad. Hacerlos entrena la intuición de riesgo mejor que leer sobre ellos.
11. **[I] Velocidad antes que seguridad.** El kit (recarga en caliente, *burner wallets*, *faucet* local) está hecho para construir rápido. Es lo contrario de la disciplina de producción. El curso forma constructores, no auditores.
12. **[O] Opinión:** es la mejor ruta de "aprender haciendo" para quien ya programa en JavaScript. Para un inversionista sin experiencia de programación es empinada.

## 4. Qué cambia para invertir

- **Si "confías en el código", el código es tu contraparte.** Antes de depositar en un protocolo, pregunta:
  - ¿Quién puede cambiar el código o sus parámetros?
  - ¿Qué oráculo usa?
  - ¿Qué pasa con tu posición si el colateral cae 30% en una hora?
- **Lectura de un protocolo de préstamos** después de hacer los retos #5-#7: fuente del precio, umbral y penalización de liquidación, quién liquida y qué pasa si nadie liquida a tiempo.
- **Todo juego o lotería en cadena que use datos del bloque como azar es manipulable** (reto #3). Aplica a promesas de "rendimiento" basadas en sorteos.
- **Con AMMs:** entender que el precio sale de las reservas explica el deslizamiento y por qué el TVL no es ingreso.
- **Cartera actual (solo BTC spot):** no hay acción directa. El valor está en no comprar productos DeFi o de rendimiento sin esta lista.

## 5. Contrapuntos y límites

- **No es un curso de seguridad.** Enseña a construir, no a auditar.
- **Todo pasa en redes de prueba** y no simula el comportamiento adversarial real de un mercado con dinero.
- **Sesgo pro-Ethereum** (EF, L2s). No cubre Bitcoin, Solana ni otras cadenas.
- **Métricas de uso autodeclaradas.**
- **No completé los retos:** mi lectura es del temario y los README.

## 6. Autoexamen

1. **¿Por qué el *hash* del bloque es mala fuente de aleatoriedad y cómo lo muestra el curso?**
   - Es público y determinista: otro contrato en la misma transacción puede calcularlo y decidir apostar solo si gana. Además, quien produce el bloque tiene influencia sobre él.
   - En el reto #3 el alumno ataca el Dice Game con un contrato que predice la tirada.
   - *Fuente:* README de se-2-challenges (Dice Game) y portada del sitio.
2. **En el DEX del reto #4, ¿de dónde sale el precio y qué recibe el proveedor de liquidez?**
   - El precio sale de la razón de reservas ETH/token del contrato.
   - El proveedor recibe un token que representa su parte de reservas y comisiones.
   - *Fuente:* README de se-2-challenges (Build a DEX).
3. **¿Qué tres diseños de oráculo recorre el reto #5 y cuál añade un periodo de disputa?**
   - Lista blanca, *staking* (con incentivos y penalizaciones) y optimista, que es el que añade el periodo de disputa.
   - *Fuente:* portada de speedrunethereum.com (Challenge #5).

## 7. Grado de evidencia: **B** (contenido) · **C** (implicaciones)

- **B en contenido:** es fuente primaria sobre su propio temario, con código abierto verificable. No es A porque las métricas de uso son autodeclaradas y no auditadas.
- **C en implicaciones de inversión:** son inferencia mía a partir de los mecanismos que enseña. No hay datos empíricos de mercado en el curso.

### Fuentes

- https://speedrunethereum.com/, consultado el 25-sep-2026.
- https://raw.githubusercontent.com/scaffold-eth/se-2-challenges/main/README.md
- https://raw.githubusercontent.com/scaffold-eth/scaffold-eth-2/main/README.md
- https://buidlguidl.com/, consultado el 25-sep-2026.
