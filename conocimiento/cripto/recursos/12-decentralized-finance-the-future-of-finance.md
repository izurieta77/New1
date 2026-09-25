# 12 · Decentralized Finance (DeFi): The Future of Finance (especialización de Duke en Coursera)

> Ficha de estudio del grupo G3 DeFi, escrita por `analista-cripto` el 25-sep-2026. Es formación, no recomendación.
> **Acceso:** temario público completo y presentaciones públicas del instructor. **No me registré** en Coursera ni vi los videos.
> **Estado:** estudiado por resumen y secciones.
> **Capítulo de síntesis:** [03-defi-mecanica-riesgos-y-academia.md](../03-defi-mecanica-riesgos-y-academia.md).

## 1. Ficha

| Campo | Dato (página de Coursera, 25-sep-2026) |
|---|---|
| Año | 2022, según el índice del dueño. Las reseñas visibles son de abr-2022 en adelante. La siguiente cohorte aparece como "*Starts Sep 25*". |
| Autor | Duke University. Único instructor: Campbell R. Harvey (Fuqua y NBER). |
| Tipo | Especialización de 4 cursos y 17 módulos: *Infrastructure* (6 h), *Primitives* (6 h), *Deep Dive* (8 h) y *Opportunities and Risks* (6 h). Unos **1,019 minutos de video** (~17 h), sumando lo que declara el temario, con un cuestionario por módulo. |
| Nivel | Coursera dice "*Beginner level*". El índice del dueño dice "Intermedio". |
| Costo | **Ambiguo en la propia página.** El botón y los metadatos dicen "*Enroll for free*" (`isAccessibleForFree`), pero el FAQ dice "*No, you cannot take this course for free... you can apply for financial aid*". El certificado es de pago. |
| Idioma | Inglés, con 24 idiomas de subtítulos |
| Alcance | 45,911 inscritos; 4.8 de 2,178 reseñas. Dice "*16 weeks to complete at 2 hours a week*", pero el FAQ dice "*Approximately 4 weeks*". |
| URL | https://www.coursera.org/specializations/decentralized-finance-duke |

**Conflictos de interés:**

- Los de Harvey:
  - beca de la UBRI, que financia Ripple, de 2022 a 2026;
  - asesorías con Man Group y Research Affiliates;
  - coautor con el fundador de Fei.
  - Ver [07](07-defi-and-the-future-of-finance.md), §1.
- El curso es un producto comercial de Coursera y Duke (certificado de pago) y promueve el libro del instructor: cada módulo trae la lectura "*DeFi and the Future of Finance*".
- En el deck de 2024, Harvey trata el caso Fei de forma crítica (ver viñeta 9): un punto a su favor.

## 2. Acceso real (consultado el 25-sep-2026)

| Fuente | Qué leí | Nivel |
|---|---|---|
| Página de la especialización y de los 4 cursos (`/learn/decentralized-finance-infrastructure-duke`, `-primitives-duke`, `-deep-dive-duke` y `-opportunities-and-risk-duke`) | Descripción, módulos y títulos y duración de cada video y lectura | Temario íntegro |
| 16 decks públicos de Harvey, curso 697 de Duke (2024): `people.duke.edu/~charvey/Teaching/697_2024/Public_Presentations_697/DeFi_{Infrastructure,Primitives,Deep,Risks}_Module_{1-4}.pdf`. Son 842 láminas, creadas entre ene y feb de 2024. | Títulos de las 16. Íntegras: Infraestructura M2 §stablecoins (láminas ~77-162), Profundidad M2 §rehipotecación y Riesgos M4 §inversión. Por búsqueda de términos: Profundidad M1 (MakerDAO, Compound, Aave) y Primitivas M1 (MEV). | Sección |
| Videos y cuestionarios de Coursera | No vistos: requieren inscribirse | — |

- **[I]** Los decks de 2024 tienen exactamente la estructura de la especialización (4 partes × 4 módulos, con los mismos títulos). Infiero que son el material de los videos, pero no lo confirmé viendo los videos.
- **Nivel global: resumen** (del curso) **+ sección** (del material del instructor).

**Temario público** (videos por módulo):

- **C1 · Infrastructure:**
  - M1 Historia (71 min): de la barata al paper de Nakamoto de 2008.
  - M2 Fundamentos (78 min): blockchain, hashing, cripto, contratos, gas, oráculos, stablecoins y dApps.
  - M3 Problemas que resuelve (51 min): ineficiencia, acceso, opacidad, control e interoperabilidad.
  - M4 Mitos (28 min).
- **C2 · Primitives:**
  - M1 Mecánica (48 min): transacciones, tokens fungibles y NFT, y **MEV**.
  - M2 Oferta y propiedad (43 min): custodia, acuñar y quemar, *bonding curves* y *keepers*.
  - M3 Swaps y préstamos (56 min): CEX, DEX, **AMM**, préstamos colateralizados y **flash loans**.
  - M4 (90 min): MetaMask, firmas y consenso.
- **C3 · Deep Dive:**
  - M1 Crédito (118 min): MakerDAO con **liquidación**, Compound y Aave.
  - M2 DEX (64 min): Uniswap v2/v3, **pérdida impermanente**, *flash swaps*, Balancer y **rehipotecación**.
  - M3 Derivados (106 min): Yield, dYdX y Synthetix.
  - M4 Tokenización (41 min): Set y WBTC.
- **C4 · Opportunities and Risks:**
  - M1 Contrato inteligente (82 min).
  - M2 Gobernanza, DNS, **oráculo**, DEX y custodia (50 min).
  - M3 Escalabilidad (29 min).
  - M4 Regulación y ambiente (45 min).
  - M5 Ganadores y perdedores (19 min).

## 3. Lo esencial

Etiquetas: [H] hecho con fuente · [I] inferencia · [O] opinión del autor.

1. **[H] Promesa del curso** (página de C1): DeFi resuelve cinco problemas de las finanzas centralizadas:
   - ineficiencia ("*costly, slow, and insecure*");
   - acceso limitado ("*1.7 billion are unbanked*");
   - opacidad ("*regulators have mixed records*");
   - control centralizado ("*oligopolistic*");
   - falta de interoperabilidad.
2. **[H] MEV actualizado tras el Merge** (C2 M1, deck de 2024, láminas 9-10): "*Maximal extractable value (MEV) is a theoretical measure of the profit that the builder/proposer could make by including, excluding or re-ordering transactions... Realized extractable value (REV) is now the most popular measure*".
   - En 2021 decía "*miner*" y lo llamaba "*a drawback to the proof-of-work model*" ([07](07-defi-and-the-future-of-finance.md), viñeta 16).
3. **[H + cálculo] Liquidación en MakerDAO** (C3 M1): el mismo ejemplo de 2021.
   - 5 ETH a $200 permiten hasta 666.67 DAI. A $150, con 500 DAI de deuda, se venden 3.333 ETH, el *keeper* cobra 0.2 ETH (6% de la deuda) y se devuelven 1.467 ETH.
   - Compound: cociente requerido de 151.5% para 20% en DAI (CF 90) y 80% en ETH (CF 60). Ambos comprobados en Python.
   - Si el colateral no alcanza, se genera "*Protocol Debt*" y se cubre acuñando MKR ("*Global Settlement*" como último recurso).
4. **[H] Debilidad de DAI** (C3 M1, lámina 29): "*No clear arbitrage loop exists to maintain the peg*". USDC, en cambio, se redime a $1 en Coinbase. [I] Esa falta de ancla explica por qué Maker terminó respaldando DAI con USDC mediante el PSM, y por qué DAI cayó con USDC en mar-2023 (ver [06](06-decentralized-finance-mooc.md), viñeta 19).
5. **[H + cálculo] Rehipotecación** (C3 M2, láminas 45-46):
   - Se depositan $1,500 en WETH en Maker, con un préstamo de 1,000 DAI (150%).
   - Se aportan 1,000 DAI y 1,000 USDC a Uniswap, que entrega $2,000 en tokens LP.
   - Esos tokens LP vuelven a Maker como colateral de 1,960 DAI (102%).
   - El TVL suma **$5,500 con solo $2,500 comprometidos: 2.2 veces**. Lo comprobé.
   - [I] El TVL exagera el capital real y esconde apalancamiento en capas.
6. **[H] Stablecoins en 2024** (C1 M2, láminas 80-162):
   - Tipos: respaldadas por dinero fiduciario (USDT, USDC), por materias primas, por cripto (DAI, FEI, FRAX) y algorítmicas (AMPL, UST).
   - El "trilema" de la stablecoin: estabilidad de precio, eficiencia de capital y descentralización; no se logran las tres.
   - Riesgo de "*stablecoin run*" (corrida) como el de un banco.
7. **[H] Circle y SVB** (láminas 99-108). La meta era 80% de la reserva en un fondo de mercado de dinero regulado por la SEC y 20% como liquidez para redenciones; "*March 2023 $3.3b in float on deposit at SVB!*".
   - Circle lo confirmó: $3.3 mil M, "*about 8%*" de su reserva ([Circle](https://www.circle.com/pressroom/3-3-billion-of-usdc-reserve-risk-removed-dollar-de-peg-closes)).
   - [I] La reserva total era de $42.1 mil M: 32.4 en letras del Tesoro y 9.7 en efectivo. SVB equivalía a 7.84%.
   - USDC tocó ≈ $0.87-0.88 el 11-mar-2023, una pérdida implícita 1.63 veces mayor que toda la exposición a SVB. La paridad volvió tras la declaración conjunta del 12-mar ([Fed](https://www.federalreserve.gov/newsevents/pressreleases/monetary20230312b.htm)).
8. **[H + cálculo] Terra: el mecanismo** (láminas 142-144): "1 UST = $1 en LUNA".
   - Con UST en $1.05 y LUNA en $10: se compran 0.1 LUNA, se queman por 1 UST y se vende en $1.05, ganando **$0.05**.
   - Con UST en $0.95: se compra UST, se quema por $1 en LUNA y se vende la LUNA, ganando **$0.05**.
   - [O] "*LUNA looks like a Ponzi*" (lámina 148): unos $20 de cada $100 van a LFG y $80 a inversionistas tempranos.
   - [H] La correlación UST–LUNA es el defecto: "*if terra is doing poorly... LUNA will also be doing poorly*" (lámina 149).
9. **[H] Terra: el colapso** (láminas 146-156), cotejado con otras fuentes:
   - **Anchor:** "*close to 20% APR*" y "*almost 80% of UST supply was in Anchor*". El NBER mide 19.5% y ~12 de 18.5 mil M de UST en Anchor antes del colapso: **~65%**, no 80% ([NBER w31160](https://www.nber.org/papers/w31160)).
   - **Detonante:** el 7-may, retiros de Anchor (el NBER identifica 2 direcciones con 375 M de UST); Terraform retiró $150 M de Curve para un nuevo pool y alguien cambió ~$84 M de UST por USDC.
   - **Caída de UST:** el deck, citando a CoinDesk, dice $0.35 el 9-may. El NBER registra $0.75 la noche del 9-may y menos de $0.20 al cierre del 13-may. La diferencia puede deberse a mínimos intradía en distintos mercados; no la resolví.
   - **Reservas de LFG:** "*more than 80,000 bitcoin to just 313*" (confirmado: [CoinDesk](https://www.coindesk.com/business/2022/05/16/luna-foundation-guard-left-with-313-bitcoin-after-ust-crash), 80,394 → 313 BTC).
   - **Oferta de LUNA:** de ~340 M a 6.5 billones (The Block).
   - **Pérdida total:** "*approximately $40b*". El NBER habla de $50 mil M de valuación combinada antes del colapso.
10. **[H] Fei, el proyecto del coautor Santoro** (láminas 121-130): arranque inestable; hackeo de $80 M por reentrada en Rari Fuse (abr-2022); Fei Labs abandonó TRIBE DAO el 19-ago-2022.
    - Razones que cita: "*Potential Regulatory risks*" y "*The PCV model could not find a suitable product market*".
    - [I] Contraste con 2021, cuando lo presentaba como la solución (ver [07](07-defi-and-the-future-of-finance.md)).
11. **[H] Otras stablecoins cripto:**
    - FPI de Frax apunta al índice de precios (CPI) mediante un oráculo de Chainlink. Para seguir 100% colateralizada, su balance debe crecer al menos al ritmo de la inflación.
    - RAI tiene un precio de redención flotante.
    - OHM usa valor controlado por el protocolo (PCV).
12. **[H] Riesgos (C4).**
    - La descripción de M3 aún dice "*Ethereum blockchain is only about 15 transactions per second whereas the Visa network is 65,000*": un dato de 2021 mantenido en 2026.
    - Casos: The DAO, dForce, Yearn (préstamo relámpago), C.R.E.A.M. v1, ataque de gobernanza a $TSD y ataque de DNS.
13. **[O] Estabilidad financiera** (lámina 161): "*TVL in DeFi protocols was $57 billion as January 25, 2024. This level of TVL is not in the realm of a financial stability concern*".
    - Contraste: el NBER documenta que Terra provocó en cadena las caídas de Celsius y Three Arrows y contribuyó a la de FTX.
14. **[H] Inversión** (C4 M5, láminas 43-46):
    - "*Cryptos are not one thing*"; son difíciles de valuar; "*quality data only exists from 2013*".
    - En mar-2020 "*stocks dropped 35%, gold dropped 20% and crypto plunged over 50%*", por lo que el mercado las trata como activos de riesgo. **No verifiqué** estas tres cifras con datos.
    - [O] "*Too much attention is paid to Bitcoin which is mainly a speculative asset*".
    - Propone cuatro vías: especulación, tokens de gobernanza, capital de *startups* y ***yield farming***.
15. **[O] Ambiente** (C4 M4): la minería migrará a energía limpia, y "*bitcoin will survive the short to medium term environmental risk*".
16. **[I] Cobertura de lo que exige este estudio:**
    - **x·y = k y pérdida impermanente:** definición y ejemplos en C2 M3 y C3 M2. La derivación formal está en [06](06-decentralized-finance-mooc.md).
    - **Liquidaciones:** por cociente de colateral; el término "factor de salud" no aparece.
    - **Terra y USDC:** sí los cubre (viñetas 7-9).
    - **Oráculo y flash loan:** módulos "*Oracle Attack*" y "*Flash Loans*".
    - **MEV:** C2 M1.

## 4. Qué cambia para invertir

- **[I] Cascadas y BTC spot.** El curso explica la liquidación de una posición, pero no cómo la agregación de posiciones mueve el precio.
  - Para eso: la "sensibilidad de liquidación" de Qin et al. ([06](06-decentralized-finance-mooc.md)) y el evento del 10-oct-2025.
  - Ese día hubo más de $19 mil M de liquidaciones, casi todas en perpetuos; Aave liquidó ~$180 M; el BTC tocó −14.5% dentro del día (ver capítulo §4).
  - La rehipotecación (viñeta 5) explica por qué el apalancamiento real es mayor de lo que sugiere el TVL.
- **[I] Por qué no usamos rendimientos DeFi,** aunque Harvey proponga el *yield farming* como vía de inversión:
  - nuestro mandato es spot;
  - su propio curso muestra que ese rendimiento se paga con riesgo de corrida (Terra), de custodia bancaria (USDC/SVB), de hackeo (Fei/Rari) y de rehipotecación;
  - en una cuenta de 5,000 MXN, una comisión de rendimiento de 3-5% anual no compensa un evento de cola de −20% a −100%.
- **[I] Señales de riesgo sistémico** (del curso):
  1. stablecoins respaldadas por su propio token (correlación endógena);
  2. rendimientos subsidiados como el ~20% de Anchor;
  3. concentración del respaldo en un banco (Circle en SVB) o en un protocolo (Anchor);
  4. TVL que crece más rápido que el capital comprometido (rehipotecación);
  5. propuestas de gobernanza que cambian parámetros de riesgo.

## 5. Contrapuntos y límites

- **Acceso:** no vi los videos ni los cuestionarios. Las láminas son un sustituto razonable, pero no idéntico.
- **Desactualizaciones en 2024:**
  - "15 TPS";
  - las cifras de capitalización de USDT ($66 mil M) y USDC ($26 mil M) de la lámina 82, sin fecha de corte;
  - partes que siguen describiendo el mundo de 2021.
- **Discrepancias con otras fuentes:** el porcentaje de UST en Anchor (80% contra 65%), el mínimo del 9-may ($0.35 contra $0.75) y la pérdida total ($40 mil M contra $50 mil M).
- **La página de Coursera se contradice:** gratuidad, duración (4 contra 16 semanas) y nivel (principiante contra el "intermedio" del índice).
- **Opiniones no probadas:** que DeFi no es un riesgo de estabilidad financiera; que el *yield farming* es una vía de inversión razonable; que BTC es "*mainly a speculative asset*".
- **Qué envejeció bien:** el caso Terra está bien explicado; el análisis de Fei es autocrítico.
- **Qué envejeció mal:** las cifras de escalabilidad y de capitalización, que se quedaron congeladas en 2021-2022 dentro de un curso vigente en 2026.

## 6. Autoexamen

1. **Explica el arbitraje UST–LUNA con UST en $0.95 y LUNA en $10. ¿Por qué deja de funcionar en una corrida?**
   - *Respuesta:* se compra 1 UST en $0.95, se quema por $1 en LUNA (0.1 LUNA) y se vende: ganancia de $0.05. Cada redención acuña LUNA y la diluye.
   - Si la capitalización de LUNA se acerca a la oferta de UST, la redención presiona el precio de LUNA, que respalda a UST: la espiral es reflexiva. El NBER fecha ese cruce la noche del 9-may-2022, con UST en $0.75.
   - *Fuente:* Harvey, C1 M2 (2024), láminas 143-149; NBER w31160.
2. **En el ejemplo de rehipotecación, ¿cuánto TVL se registra y cuánto capital se comprometió realmente?**
   - *Respuesta:* $1,500 (WETH) + $1,000 (USDC) + $1,000 (DAI en Uniswap) + $2,000 (tokens LP en Maker) = $5,500 de TVL. El capital comprometido es de $2,500 (1,500 + 1,000): 2.2 veces.
   - *Fuente:* C3 M2 (2024), láminas 45-46.
3. **Circle tenía $3.3 mil M en SVB con una reserva de $42.1 mil M. ¿Qué precio de USDC era "justo" si SVB pagaba 0%, 50% o 100%, y qué dice el mínimo de $0.87?**
   - *Respuesta:* 0.9216, 0.9608 y 1.0000. Un precio de $0.8726 implica perder 12.7% de la reserva, 1.63 veces lo expuesto: fue un descuento de liquidez y pánico en fin de semana, no el peor caso fundamental.
   - *Fuente:* Circle (12-mar-2023); cálculo en el apéndice A del capítulo.
4. **¿Qué es el trilema de las stablecoins? Ubica a USDC, DAI y UST.**
   - *Respuesta:* no se pueden tener a la vez estabilidad de precio, eficiencia de capital y descentralización.
   - USDC: estable y eficiente (1:1), pero centralizado.
   - DAI: más descentralizado, pero ineficiente (150% de colateral), y terminó apoyándose en USDC.
   - UST: prometía eficiencia y descentralización, y sacrificó la estabilidad: colapsó.
   - *Fuente:* C1 M2 (2024), lámina 159 (que cita el whitepaper de stablecoins de Coinbase); lámina 29 de C3 M1.

## 7. Grado de evidencia: **C**

- **Por qué C:** es el mismo académico con método visible que en [07](07-defi-and-the-future-of-finance.md), actualizado a 2024 y más crítico: trata Fei, Terra y SVB.
- **Por qué no más alto:**
  - el material es divulgativo y no revisado por pares;
  - las cifras de mercado vienen de prensa y agregadores, con discrepancias frente al NBER;
  - hay conflictos (UBRI/Ripple, libro propio);
  - solo accedí al temario y a las láminas, no a los videos.
- **A en la mecánica verificada:** Maker, Compound, rehipotecación y el arbitraje de Terra.
