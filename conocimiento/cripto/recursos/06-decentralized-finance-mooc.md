# 06 · Decentralized Finance MOOC (otoño 2021, UC Berkeley RDI)

> Ficha de estudio del grupo G3 DeFi, escrita por `analista-cripto` el 25-sep-2026. Es formación, no recomendación.
> **Estado:** estudiado por secciones. Las seis áreas pedidas están leídas completas en diapositivas; de las lecturas asignadas, solo leí algunas partes.
> **Capítulo de síntesis:** [03-defi-mecanica-riesgos-y-academia.md](../03-defi-mecanica-riesgos-y-academia.md). El código de verificación está en su apéndice A.

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2021. Clases del 26-ago al 9-dic-2021, los jueves de 10:30 a 12:30 (hora del Pacífico). También se puede cursar asíncrono, con video. |
| Autor | UC Berkeley RDI, con 5 instructores: Dan Boneh (Stanford), Arthur Gervais (Imperial College London), Andrew Miller (UIUC), Christine Parlour (UC Berkeley) y Dawn Song (UC Berkeley). Asistentes voluntarios: Kaihua Qin, Liyi Zhou y Yongzheng Jia. Ponentes invitados: Dan Robinson (Paradigm), Ariah Klages-Mundt (Cornell), Ari Juels, samczsun y Aaron Wright. |
| Tipo | MOOC universitario con 13 clases con cuestionario, 1 clase de regulación sin cuestionario, 2 laboratorios y un proyecto opcional. |
| Nivel | Avanzado: informática y finanzas. |
| Costo | Gratis. Videos en YouTube; diapositivas y lecturas en PDF abiertos en `berkeley-defi.github.io`. |
| Idioma | Inglés |
| URL | https://defi-learning.org/f21. El temario vive en un iframe: https://berkeley-defi.github.io/f21_syllabus |

**Conflictos de interés verificados:**

- **Ari Juels**, ponente de la clase de oráculos, es científico jefe de Chainlink Labs y coautor del whitepaper de Chainlink de 2017 ([Wikipedia](https://en.wikipedia.org/wiki/Ari_Juels); [Chainlink Labs](https://chainlinklabs.com/research)).
  - Su clase asigna como lectura "Chainlink 2.0" y dos artículos suyos (Town Crier y DECO).
  - Busqué "Chainlink" en el texto de las 101 láminas y no aparece: la relación no se declara en las diapositivas.
- **Dan Robinson**, ponente del caso Uniswap, es socio general y jefe de investigación de Paradigm, y coautor del whitepaper de Uniswap v3 ([Columbia](https://godigital.engineering.columbia.edu/events/dan-robinson-paradigm)). Su última lámina lleva un aviso legal de Paradigm: declaración parcial.
- **samczsun**, ponente de seguridad, era investigador de Paradigm, un fondo cripto ([The Block](https://www.theblock.co/post/349698/prominent-crypto-researcher-samczsun-steps-down-from-paradigm-to-focus-on-seal-911-security-initiative)).
- **Ariah Klages-Mundt**, ponente de stablecoins, participa en Gyroscope, una stablecoin. Lo declara en su lámina 84.
- **Dawn Song** es fundadora y CEO de Oasis Labs, empresa blockchain ([Wikipedia](https://en.wikipedia.org/wiki/Dawn_Song)).
- **Sesgo de selección, no financiero:** Gervais, Qin y Zhou firman buena parte de las lecturas de préstamos, flash loans y MEV.
- **Incentivo menor:** el curso entrega NFT por completarlo.

## 2. Acceso real (consultado el 25-sep-2026)

Descargué 33 PDFs desde `berkeley-defi.github.io/assets/material/` al scratchpad; no se suben al repo. Los leí con pypdf. **Límite:** muchas láminas son imágenes; solo leí el texto extraíble, sin OCR. Los videos de YouTube no los vi, porque yt-dlp está bloqueado aquí.

| Clase (fecha) | Qué leí | Nivel |
|---|---|---|
| 1. Introducción, Dawn Song (26-ago) | 49 láminas y resumen de 12 | Íntegro (texto) |
| 5. DEX (23-sep) | 67 láminas de los instructores y 31 de Dan Robinson (Uniswap) | Íntegro (texto) |
| Lecturas de la clase 5 | Angeris et al., *An analysis of Uniswap markets* (arXiv 1911.03380): §2.1 arbitraje óptimo y rendimiento del LP (ec. 9-10). *Uniswap v3 Core*: §1-2 | Sección |
| 6. Préstamos y liquidaciones (30-sep) | 57 láminas y resumen de 9 | Íntegro (texto) |
| Lecturas de la clase 6 | Qin et al. (arXiv 2106.06389): §1-5. Qin et al. (arXiv 2003.03810): §1-5. Perez et al. (arXiv 2009.13235): resumen, §5.4-5.5 y conclusión. Gudgeon et al. (arXiv 2002.08099): resumen e introducción | Qin: íntegro §1-5; los demás, sección |
| 7. Stablecoins (7-oct) | Introducción (21 láminas) y Klages-Mundt (84 láminas) | Íntegro (texto). Lecturas: no leídas |
| 8. Oráculos, Ari Juels (14-oct) | 101 láminas | Íntegro (texto). Lecturas: no leídas |
| 12. Seguridad práctica, samczsun (18-nov) | ~85 de 151 láminas: llamadas externas inseguras, bug de 4 años y "CTF de 20 millones" | Sección |
| 13. Seguridad DeFi II (2-dic) | 93 láminas. Qin, Zhou y Gervais (arXiv 2101.05511): resumen, fig. 1 y periodo. Daian et al., *Flash Boys 2.0*: resumen | Láminas íntegras; lecturas, sección |
| Clases 2, 3, 4, 9, 10, 11 y 14 | No leídas: fuera del alcance pedido | — |

**Nivel global: sección.**

## 3. Lo esencial

Etiquetas: [H] hecho con fuente · [I] inferencia · [O] opinión del autor.

### AMM y pérdida impermanente

1. **[H] Producto constante.** Un AMM de producto constante mantiene x·y = k.
   - El precio marginal es y/x. Comprar X sube su precio, y siempre hay liquidez para cualquier tamaño, pero con un deslizamiento creciente (clase 5, láminas 14-15; Robinson, láminas 10-19).
   - Con una comisión f y γ = 1 − f: Δy = y·γΔx / (x + γΔx).
   - Ejemplo propio, comprobado en Python: pool de 100 ETH y 200,000 USDC. Una compra de 10,000 USDC con comisión de 0.30% entrega 4.748297 ETH, a un precio efectivo de 2,106.02. El precio marginal sube de 2,000 a 2,204.68, y k crece de 20,000,000 a 20,002,857.55 por la comisión.
2. **[H] Derivación de la pérdida impermanente** (Angeris et al., ec. 9-10, sin comisiones y con arbitraje).
   - Arbitraje y producto constante implican y = √(k·p) y x = √(k/p). Por lo tanto, el valor del LP es **V = 2√(k·p)**, proporcional a √p.
   - Mantener los activos (HODL) vale V₀(1 + r)/2, con r = P₁/P₀.
   - **IL = 2√r/(1 + r) − 1.** Valores: r = 1.25 → −0.62%; r = 2 → −5.72%; r = 4 → −20.00%; r = 5 → −25.46%; r = 0.5 → −5.72%. Es simétrica en logaritmos.
3. **[H] Ejemplo del curso, comprobado en Python** (clase 5, lámina 47).
   - Pool de 10 ETH y 1,000 DAI. El ETH sube de 100 a 400 y el arbitraje deja el pool en 5 ETH y 2,000 DAI.
   - La posición de 10% vale 0.5 ETH + 200 DAI = $400. Mantener 1 ETH + 100 DAI valdría $500: −20%, igual a IL(4).
   - Simulé 200,000 arbitrajes pequeños y coincide con la fórmula a 4 decimales.
   - La lámina tiene una errata: escribe "1 ETH + 1 USD == 500 USD" donde debe decir 100 DAI.
4. **[I] La pérdida impermanente es la ganancia del arbitrajista.**
   - El pool vende el activo que sube por debajo del precio externo. En el ejemplo de Finematics ($500 → $550) ambas cantidades valen $23.82 (ver [03-finematics.md](03-finematics.md)).
   - La comisión solo la compensa si comisión × volumen acumulado ≥ |IL|. Con 0.30% y r = 2, el volumen debe ser 19.1 veces el TVL; con r = 5, 84.9 veces (cálculo propio).
5. **[H] Stablecoins en AMM.** Para activos que deben valer lo mismo, el producto constante desperdicia liquidez; StableSwap (Curve) aplana la curva cerca de 1:1 (clase 5, láminas 31-39).
   - La lámina de pros y contras advierte "*Danger of impermanent loss/coin de-peg. Total loss of funds possible*".
   - Las láminas preguntan qué pasa si una moneda pierde la paridad o entra en lista negra. La intro de stablecoins registra que USDT puso en lista negra más de 400 cuentas y destruyó más de 44 M USDT (clase 7, lámina 19).

### Préstamos, factor de salud y liquidaciones

6. **[H] Definiciones** (Qin et al., arXiv 2106.06389, ec. 1-4):
   - Capacidad de préstamo: BC = Σ colateralᵢ × LTᵢ.
   - Factor de salud: **HF = BC / Σ deudaᵢ**. La posición es liquidable si HF < 1.
   - El liquidador paga deuda y recibe colateral por deuda × (1 + LS), donde LS es el bono (*liquidation spread*).
   - El *close factor* es la fracción máxima de la deuda por liquidación: 50% en Aave y Compound, 100% en dYdX.
   - El bono va de 5% a 15% en Aave y es de 5% en dYdX.
7. **[H] Ejemplo del artículo, comprobado en Python.**
   - 3 ETH a $3,500, LT 0.8 y deuda de 8,400 USDC: HF = 1.000. Con ETH a $3,300, HF = 0.943.
   - El liquidador paga 4,200 y recibe 1.4 ETH ($4,620): gana $420, que es 4.24% del colateral del deudor. Después, HF = 1.0057.
   - Regla que se deduce: **caída tolerable = 1 − 1/HF**. Un HF de 1.716 aguanta −41.7%.
8. **[H] Magnitudes** (Qin et al., de abr-2019 a abr-2021, en Aave, Compound, dYdX y MakerDAO):
   - 28,138 liquidaciones que vendieron 807.46 M USD de colateral.
   - 63.59 M USD de ganancia para los liquidadores, 7.88% del colateral (cálculo propio).
   - 2,011 liquidadores; 73.97% pagó una comisión de gas superior al promedio, señal de competencia.
9. **[H] Sensibilidad.**
   - Una caída inmediata de 43% del ETH, como la del 13-mar-2020, volvería liquidables hasta 1.07 mil M USD en MakerDAO (Qin et al., §4.5.1).
   - En Compound, tras el lanzamiento de COMP, un movimiento de solo 3% en el precio de DAI volvía liquidables más de 10 M USD (Perez et al., FC 2021).
10. **[H] Espiral de desapalancamiento.** La liquidación vende colateral, el precio cae y eso provoca más liquidaciones (clase 6, lámina 42; Klages-Mundt, láminas 42-60).
    - El modelo *fixed spread* con *close factor* **sobreliquida**: vende más colateral del necesario y favorece al liquidador. Qin et al. muestran además una estrategia de dos liquidaciones que evade el *close factor*.
11. **[H] Jueves Negro (12 y 13-mar-2020).**
    - Por la congestión de la red, las transacciones de los bots de MakerDAO no entraron a tiempo.
    - Otros liquidadores ganaron subastas "a costo despreciable": la ganancia de liquidadores en Maker ese mes fue de 13.13 M USD (Qin et al., §4.3.1).
    - Klages-Mundt (lámina 34) cifra el costo en "$8m" y lo atribuye a manipulación del mempool.

### Flash loans y oráculos

12. **[H] Préstamo relámpago.** Se toma y se paga dentro de la misma transacción; si no se paga, todo se revierte.
    - Para el prestamista no hay riesgo de impago, salvo bugs; no pide colateral; el tamaño llega al pool entero.
    - Usos: arbitraje, liquidación, cambio de colateral y ataques (Qin et al., arXiv 2003.03810, §2).
13. **[H] Ataques a bZx** (Qin et al., §3).
    - *Pump and arbitrage* (15-feb-2020):
      - pidió 10,000 ETH prestados en dYdX;
      - abrió un corto 5x en bZx que compró WBTC en Uniswap a 109.79 ETH/WBTC, con 200% de deslizamiento;
      - ganó 1,193.69 ETH.
    - Manipulación de oráculo (18-feb-2020):
      - pidió 7,500 ETH;
      - con compras de sUSD llevó el precio de Uniswap y Kyber, el oráculo de bZx, de 268.30 a 106-108 sUSD/ETH;
      - pidió prestados 6,799.27 ETH contra 1,099,841 sUSD;
      - ganó 2,381.41 ETH pagando 0.42 ETH de comisión.
    - Los parámetros óptimos habrían dado 2.37 y 1.73 veces más.
    - **Inconsistencia:** las cifras en USD del artículo (350k y 634.9k) no cuadran con el precio de ETH que el propio artículo reporta: 1,193.69 × 264.71 = $316k y 2,381.41 × 282.91 = $674k. La lámina de Juels usa $673k.
14. **[H] Diseño de oráculos** (Juels, clase 8).
    - Firmas de varios nodos, respaldo si un nodo cae y varias fuentes.
    - Se agrega con la **mediana**: "*given a minority of bad values, median is an honest value or bounded by honest values*". Con la media, un solo dato de $40,000 lleva el promedio de ~$2,000 a $7,427 (lámina 36).
    - Un DEX usado como oráculo es rápido y componible, pero manipulable. El remedio, el TWAP, es "*less accurate than current price*" (láminas 47-53).

### MEV

15. **[H] Cuánto vale el MEV** (Qin, Zhou y Gervais, arXiv 2101.05511), en 32 meses (1-dic-2018 a 5-ago-2021):
    - sándwiches: 174.34 M USD;
    - liquidaciones: 89.18 M USD;
    - arbitraje: 277.02 M USD;
    - total: 540.54 M USD, repartido en 11,289 direcciones. La suma la comprobé.
    - El mayor caso vale 4.1 M USD, 616.6 veces la recompensa de bloque.
    - Un minero con 10% del hashrate tendría incentivo a bifurcar la cadena si una oportunidad supera 4 veces la recompensa de bloque.
    - [O] Los autores sostienen que los *relays* privados, como Flashbots, agravan los ataques de consenso y centralizan la red (clase 13, lámina 90).
16. **[H→I] Tolerancia de deslizamiento.**
    - [H] El atacante de sándwich "maximiza el deslizamiento de la víctima"; la protección es la tolerancia (clase 13, láminas 53-67).
    - [I] Mis simulaciones sobre x·y = k (apéndice A del capítulo) dan dos reglas:
      - cuando el ataque es rentable, la ganancia del atacante es aproximadamente la tolerancia por el monto de la víctima (1% de tolerancia sobre $50k da unos $450);
      - con una comisión de 0.30% y una operación de 0.25% del pool, el ataque no es rentable; con comisión de 0.05%, sí.

### Stablecoins

17. **[H] Taxonomía de Klages-Mundt.**
    - Custodiales: riesgo de contraparte, de censura y de las finanzas tradicionales, "*well understood*".
    - No custodiales, según su colateral: exógeno, endógeno o implícito. Traen riesgos nuevos: desapalancamiento, oráculos, gobernanza, MEV y bugs.
    - Desde el Jueves Negro, Maker "*has tethered to USDC (+ custodial risks)*" mediante el PSM (lámina 63).
18. **[H] Advertencia que envejeció bien** (lámina 77, oct-2021): las "*seigniorage shares*" (UST, Titan) prometen redención a $1 respaldada por un activo endógeno volátil, y "*a speculative attack could cause collapse of this asset value*". En mayo de 2022 ocurrió:
    - la oferta de UST era de 18.5 mil M, con ~12 mil M en Anchor, que pagaba 19.5%;
    - UST cayó a $0.75 la noche del 9-may, cuando la capitalización de LUNA igualó la oferta de UST, y quedó bajo $0.20 al cierre del 13-may ([NBER w31160](https://www.nber.org/papers/w31160));
    - LFG tenía ~80,300 BTC el 6-may (auditoría JS Held, citada por el NBER) y le quedaban 313 BTC el 16-may ([CoinDesk](https://www.coindesk.com/business/2022/05/16/luna-foundation-guard-left-with-313-bitcoin-after-ust-crash));
    - la oferta de LUNA pasó de ~350 M a más de 6.5 billones ([The Block](https://www.theblock.co/post/146762/luna-supply-soared-to-6-5-trillion-coins-before-terras-latest-halt)).
19. **[H] El canal DAI–USDC que el curso señaló se materializó en marzo de 2023.**
    - Circle tenía $3.3 mil M, "*about 8%*" de su reserva, en SVB ([Circle](https://www.circle.com/pressroom/3-3-billion-of-usdc-reserve-risk-removed-dollar-de-peg-closes)).
    - USDC tocó ≈ $0.87-0.88 el 11-mar ([CNN](https://www.cnn.com/2023/03/11/business/stablecoin-circle-silicon-valley-bank)). DAI, con más de la mitad de su respaldo en USDC vía el PSM, cayó a ≈ $0.88-0.89 ([CoinDesk](https://www.coindesk.com/markets/2023/03/11/dai-depegs-as-stablecoin-rout-plagues-crypto)).
    - La paridad volvió tras la declaración conjunta de Tesoro, Fed y FDIC del 12-mar-2023, 18:15 EDT, que protegió a todos los depositantes ([Fed](https://www.federalreserve.gov/newsevents/pressreleases/monetary20230312b.htm)).
    - [I] El mínimo implicaba perder 12.7% de la reserva, 1.63 veces todo lo depositado en SVB. Fue un descuento de liquidez en fin de semana, no de solvencia.

### Seguridad

20. **[H] La seguridad DeFi es multicapa** (clase 13):
    - red: eclipse;
    - consenso: doble gasto y *selfish mining*;
    - contratos: reentrada (The DAO, 3.6 M ETH) y escritura sin privilegios ($32 M);
    - protocolo: flash loans y sándwich;
    - terceros: oráculo y gobernanza.
    - samczsun añade que la mayoría de los bugs son simples, que toda llamada externa es insegura y que el "*exploit chaining*" une tres fallas menores en una crítica: el caso Pickle, en la clase "*The 20 Million Dollar CTF*" (clase 12).
21. **[H] Riesgo sistémico** (clase 1, láminas 36-39):
    - "*DeFi attacks stole over $1B in 2021*";
    - caídas de −30% (12-mar-2020) y −40% (19-may-2021) desataron liquidaciones y desapalancamiento, con comisiones de más de $100 por transferencia;
    - "*Stock markets have circuit breakers*": DeFi no los tiene.

## 4. Qué cambia para invertir

- **[I] Cómo una cascada llega al BTC spot.** Si el precio cae, bajan los HF; los liquidadores venden colateral (ETH, WBTC) en DEX y CEX; el arbitraje transmite esa presión al spot; y eso activa más liquidaciones. Es la espiral de las viñetas 10 y 11.
  - El 10-oct-2025 la cascada vino sobre todo de los **perpetuos**:
    - más de $19 mil millones liquidados en 24 horas (CoinGlass, citado por [CNN](https://www.cnn.com/2025/10/11/business/trump-tariffs-crypto-selloff) y [CoinShares](https://coinshares.com/corp/insights/knowledge/billions-in-liquidations-what-happened/));
    - Aave liquidó ~$180 M en una hora ([CoinDesk](https://www.coindesk.com/markets/2025/10/11/aave-sees-64-flash-crash-as-defi-protocol-endures-largest-stress-test)), menos de 1% del total;
    - el BTC bajó de $122,574 a $104,782 dentro del día: −14.5% ([CoinGecko](https://www.coingecko.com/learn/october-10-crypto-crash-explained), CoinShares).
  - Para el BTC spot, el termómetro de apalancamiento es el interés abierto y el *funding* de los perpetuos. El TVL de DeFi no sirve para eso.
- **[I] "Sensibilidad de liquidación".** El concepto de Qin et al. (colateral liquidable por cada punto de caída) es el mismo que los mapas de liquidación que publican los agregadores. Lo útil es saber en qué niveles de precio se concentra el apalancamiento.
- **[I] Por qué nuestra cuenta no usa rendimientos DeFi:**
  - El mandato es solo spot, sin préstamos ni staking con bloqueo.
  - Cada punto de rendimiento DeFi paga un riesgo que este curso mide:
    - contrato: más de $1 mil millones robados en 2021;
    - pérdida impermanente: −5.7% si el precio se duplica;
    - bono de liquidación: 5-15%;
    - pérdida de paridad: USDC en $0.87;
    - oráculo y MEV.
  - Es asimétrico. Un 5% anual sobre 5,000 MXN son 250 MXN al año. Un solo evento de −20% cuesta 1,000 MXN, cuatro años de rendimiento.
  - El 19.5% de Anchor era un subsidio, no un rendimiento (NBER).
- **[I] Señales de riesgo sistémico a vigilar** (de las más a las menos líquidas):
  1. desvíos de paridad de USDT, USDC, DAI y USDe en Curve y en exchanges;
  2. rendimientos en stablecoins muy por encima de la tasa libre de riesgo;
  3. interés abierto y *funding* de perpetuos;
  4. colateral liquidable ante caídas de −10% y −20%;
  5. picos de gas y congestión, como en el Jueves Negro;
  6. desvíos entre oráculos y precio de mercado;
  7. hackeos grandes;
  8. concentración: un solo protocolo que absorbe la mayor parte de una stablecoin, como Anchor con ~65% de UST, o pocos *builders* de bloques.

## 5. Contrapuntos y límites

- **Fecha.** El curso es de 2021: antes del Merge, de Terra, de FTX y de MEV-Boost.
  - Las cifras de liquidaciones llegan a abr-2021. El TVL "*over $80 billion*" y los volúmenes de DEX (lámina 12) son de esa época.
  - La crítica a los *relays* de BEV es anterior a la separación proponente-constructor (PBS) posterior al Merge, que ya adoptó ~90% de la red (Finematics, oct-2023; ver [03-finematics.md](03-finematics.md)).
- **Errores internos:**
  - La lámina 50 de la clase 6 dice que Aave cobra 0.3% por flash loan. La lectura de Qin et al., Harvey y Finematics dicen 0.09%.
  - Las cifras en USD de bZx no cuadran (viñeta 13).
  - La errata de la lámina 47 (viñeta 3).
- **Sesgos:**
  - conflictos no declarados: Juels y Chainlink;
  - autocitas del equipo de Imperial en las lecturas;
  - enfoque de informática, con poca valuación.
- **Qué no está probado:**
  - qué mecanismo de liquidación es óptimo. Las subastas parecen favorecer al deudor, pero el Jueves Negro mostró que son frágiles cuando la red se congestiona;
  - si la PBS reduce o solo desplaza la centralización que provoca el MEV.
- **Qué envejeció bien:**
  - la advertencia sobre UST y las *seigniorage shares*;
  - la dependencia de DAI respecto de USDC, que se cumplió en mar-2023;
  - el MEV como riesgo de consenso.
- **Qué envejeció mal:** las cifras de mercado de 2021, que hoy son solo históricas.

## 6. Autoexamen

1. **Un pool 50/50 x·y = k. El activo riesgoso cae a la mitad (r = 0.5) y no hay comisiones. ¿Cuánto pierde el LP frente a HODL, y por qué la pérdida es igual que si el precio se duplica?**
   - *Respuesta:* IL = 2√0.5/1.5 − 1 = −5.72%.
   - La fórmula depende de √r/(1 + r), que es simétrica ante r ↔ 1/r: IL(2) = IL(0.5).
   - *Fuente:* Angeris et al., ec. 9-10; cálculo en el apéndice A del capítulo.
2. **3 ETH a $3,500, LT 0.8 y deuda de 8,400. El ETH cae a $3,300. ¿HF? Con un *close factor* de 50% y bono de 10%, ¿cuánto gana el liquidador y cuál es el HF después?**
   - *Respuesta:* HF = 0.943. El liquidador paga 4,200, recibe 1.4 ETH ($4,620) y gana $420. El HF queda en 1.0057.
   - *Fuente:* Qin et al., arXiv 2106.06389, §3.2.2.
3. **¿Por qué un préstamo relámpago vuelve casi sin riesgo un ataque de oráculo, y qué hacen la mediana y el TWAP?**
   - *Respuesta:* por la atomicidad. Si el ataque no deja ganancia, la transacción revierte y el atacante solo pierde la comisión de gas; el capital prestado le da tamaño para mover un precio de poca liquidez.
   - La mediana de varios nodos limita el daño de una minoría de datos malos.
   - El TWAP obliga a sostener la manipulación durante varios bloques, lo que cuesta capital y riesgo, a cambio de menos precisión.
   - *Fuente:* Qin et al., arXiv 2003.03810, §3.2; Juels, clase 8, láminas 44-53.
4. **¿Qué predijo el curso en oct-2021 sobre UST y cómo se cumplió?**
   - *Respuesta:* que la redención a $1 contra un activo endógeno volátil podía colapsar ante un ataque especulativo.
   - Entre el 7 y el 13-may-2022, UST pasó de $1 a $0.75 (9-may) y luego a menos de $0.20. LFG gastó ~80,000 BTC y quedó con 313. La oferta de LUNA se multiplicó ~18,600 veces.
   - *Fuente:* Klages-Mundt, lámina 77; NBER w31160; CoinDesk (16-may-2022).

## 7. Grado de evidencia: **A** en mecánica y datos; **C** en las opiniones

- **A:**
  - la mecánica (x·y = k, factor de salud, flash loans) es matemática verificable, y la reproduje en Python;
  - las cifras vienen de datos on-chain medidos con método publicado: artículos de Qin, Zhou, Gervais, Perez y Angeris, con versión en arXiv.
- **C:** las opiniones de los ponentes invitados, por sus conflictos (Chainlink, Paradigm, Gyroscope), y las valoraciones sobre los *relays*.
- **Sin grado propio:** los videos no los vi; lo que no está en las diapositivas o en las lecturas que leí queda fuera de esta ficha.
