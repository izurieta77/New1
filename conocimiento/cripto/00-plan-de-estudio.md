# Plan de estudio cripto: carrera continua del `analista-cripto`

Creado el 25-sep-2026 por el orquestador. Su columna vertebral son los **35 recursos del dueño** (`recursos/00-indice.md`, `recursos/indice.csv`).

**Lo sigue la rutina 8 (Cripto):**
- en la corrida de las 08:17 avanza un tema;
- en cada corrida actualiza el estado.

**Objetivo.** Dominio de nivel doctorado sobre lo que mueve el **precio y el riesgo de BTC** (y de ETH cuando el comité lo reabra), aplicado a la cuenta `arena-claude-binance`, que opera solo spot. El segundo objetivo es la **vacuna contra fraude y contraparte**. No se estudia para opinar, sino para decidir mejor y equivocarse menos.

## Cómo se estudia (cada sesión profunda)

1. Toma el siguiente recurso o tema **pendiente** del nivel más bajo sin terminar. El estado está en `recursos/indice.csv` (columnas `estado` y `acceso`).
2. **Acceso legal únicamente:**
   - repositorios abiertos, PDFs oficiales y páginas del autor o de la editorial;
   - transcripciones oficiales, temarios, SSRN y arXiv.
   - En libros de pago se declara el acceso como "resumen" o "sección". Nunca se afirma una lectura íntegra que no hubo.
3. Escribe o amplía la ficha del recurso en `recursos/NN-*.md` con este formato:
   - ficha y conflictos de interés;
   - acceso real;
   - lo esencial, etiquetado [H]/[I]/[O];
   - qué cambia para invertir;
   - contrapuntos;
   - autoexamen;
   - grado A-D.
4. Actualiza el capítulo de síntesis del grupo (`01`-`06`) si la idea cambia algo, con una adenda fechada.
5. Actualiza `conocimiento/estado-de-dominio.csv` y el `estado` del recurso en `recursos/indice.csv`.
6. Cada cifra se verifica dos veces: segunda lectura o cálculo propio. Los errores van a `conocimiento/registro-de-errores.md`.

## Niveles

### Licenciatura: fundamentos y cultura del riesgo

| # | Recurso | Qué deja |
|---|---|---|
| 15, 29 | Diplomado en Bitcoin (v3.0 y 2025), en español | Dinero, historia monetaria, billeteras, autocustodia y Lightning |
| 20 | Plan ₿ Academy (BTC101) | Ruta Bitcoin en español |
| 03 | Finematics | DeFi explicado: AMM, préstamos, MEV y rollups |
| 01, 11 | The Infinite Machine, The Cryptopians | Historia de Ethereum, The DAO, ICOs y la primera burbuja |
| 17 | Number Go Up | FTX, Tether y estafas: la vacuna escéptica |
| 21 | Read Write Own | La tesis optimista de un fondo del sector, leída con espíritu crítico |

### Maestría: mecanismos, mercado y riesgos

| # | Recurso | Qué deja |
|---|---|---|
| 16 | Mastering Bitcoin, 3.ª ed. | El protocolo: llaves, transacciones, Script, Taproot, minería y red |
| 27 | Mastering Ethereum, 2.ª ed. | Prueba de participación, EVM, gas y quema, contratos y DeFi |
| 07, 12 | Harvey et al. y la especialización de Duke | DeFi con rigor de finanzas |
| 28 | Dinero Roto / Broken Money | La tesis monetaria de Bitcoin, contrastada con evidencia |
| 05, 34 | Glassnode y Charting Crypto Q3 2026 | Métricas on-chain y de derivados, más su reproducción con datos gratuitos |
| 26, 30 | State of Crypto 2025 (a16z) y FMI sobre stablecoins | Adopción, stablecoins y regulación |
| 32, 08 | Chainalysis 2026 y ZachXBT | Crimen, hackeos y estafas con datos |
| 02, 09 | Bankless y The Chopping Block | Narrativas del mercado, con reglas para no contagiarse |

### Doctorado: protocolo, microestructura y seguridad

| # | Recurso | Qué deja |
|---|---|---|
| 06 | MOOC de DeFi de Berkeley (2021) | DEX, préstamos, oráculos, MEV y seguridad, a nivel académico |
| 18 | MOOC de pruebas ZK de Berkeley (2023) | SNARKs, PLONK, KZG y STARKs |
| 23, 24 | Vitalik, "Possible futures" y EPF Wiki | Hoja de ruta y clientes de Ethereum |
| 25, 22, 33 | Damn Vulnerable DeFi v4, Cyfrin Updraft y el curso de Solana | Clases de vulnerabilidad y auditoría |

### Frontera: lo que cambia en 2026-2027

| # | Recurso | Qué deja |
|---|---|---|
| 35 | Galaxy, 26 predicciones para 2026 | Historial de un tercero, calificado al 31-dic-2026 |
| 31 | Zero Knowledge, Infinite Trust | ZK para escalar y dar privacidad |
| — | Regulación: GENIUS, CLARITY (votación de cloture fallida el 15-sep-2026), MiCA, Circular 4/2019 de Banxico | Riesgo regulatorio y de contraparte |
| — | Papers nuevos (SSRN, arXiv q-fin y NBER) sobre precios cripto, flujos de ETF y microestructura | Actualiza la evidencia |

### Ruta opcional de desarrollo: leer contratos, no programarlos para el torneo

- 10 Speedrun Ethereum;
- 13 Alchemy University;
- 14 Patrick Collins en freeCodeCamp;
- 19 ETH Kipu, en español.

## Temas que no cubren los 35 recursos y que el torneo necesita

1. **Microestructura de exchanges cripto.** Funding, base, interés abierto, cascadas de liquidación (10-oct-2025) y profundidad de los pares MXN en Binance.
2. **Ciclos y halving.** Qué dice la evidencia, con solo 3-4 ciclos: grado C como máximo.
3. **BTC frente a tasa real, Nasdaq y USD/MXN.** Betas y correlaciones, medidas en MXN.
4. **Flujos de los ETF spot** como variable de demanda.
5. **Prueba de reservas y riesgo de exchange.** Ver `lista-senales-de-alerta.md`.
6. **Fiscalidad cripto de una persona física en México.** ISR y actividad vulnerable según el art. 17, fr. XVI, de la LFPIORPI.

## Evaluación

- Bancos de preguntas en `examen/banco-g1` a `banco-g6`.
- El examen mensual (rutina 5) incluye 5 preguntas cripto a libro cerrado.
- Meta: ≥ 90% global y ≥ 85% por grupo.
