# Banco de examen G3 · DeFi (8 preguntas difíciles)

> Autor: `analista-cripto`, 25-sep-2026. Se usa **a libro cerrado**, con calculadora.
> **Material de estudio:** [capítulo 03](../03-defi-mecanica-riesgos-y-academia.md) y las fichas [03](../recursos/03-finematics.md), [04](../recursos/04-a16z-crypto-startup-school-2020.md), [06](../recursos/06-decentralized-finance-mooc.md), [07](../recursos/07-defi-and-the-future-of-finance.md) y [12](../recursos/12-decentralized-finance-the-future-of-finance.md).
> **Puntaje:** cada pregunta vale 10 puntos. Las cifras numéricas de las respuestas se verificaron en Python; el código está en el apéndice A del capítulo 03.
> **Aviso:** este archivo contiene la clave. Si se usa para un examen con compromiso previo, sepárense preguntas y clave según `conocimiento/examenes/PROTOCOLO.md`.

---

## P1. AMM x·y = k: ejecución y pérdida impermanente (cálculo)

**Pregunta.** Un pool de Uniswap v2 tiene 1,000,000 USDC y 400 ETH (precio 2,500), con comisión de 0.30% sobre la entrada.

- (a) ¿Cuántos ETH recibe quien compra con 50,000 USDC? Da el precio efectivo y el precio marginal después de la compra. ¿Cuál sería el precio efectivo sin comisión, y por qué es exactamente 2,500 × 1.05?
- (b) Parte otra vez del pool original, sin la compra de (a). El precio externo sube a 3,600 y los arbitrajistas alinean el pool (ignora comisiones). Deriva las reservas finales y la pérdida impermanente de un LP con 1% del pool, en % y en dólares.
- (c) Repite (b) con el precio en 1,600. Demuestra que la pérdida en dólares es x₀·(√p − √p₀)² por unidad de participación, y explica por qué ambos casos dan la misma pérdida en dólares.
- (d) ¿Cuánto volumen total del pool haría falta, con comisión de 0.30%, para que las comisiones del LP compensen la pérdida de (b)?

**Respuesta de referencia.**

- **(a)** Δy = y·(0.997·Δx)/(x + 0.997·Δx) = 400·49,850/1,049,850 = **18.9932 ETH**.
  - Precio efectivo: 50,000/18.9932 = **2,632.52**.
  - Reservas después: 1,050,000 USDC y 381.0068 ETH, así que el precio marginal es **2,755.86**.
  - Sin comisión: 400·50,000/1,050,000 = 19.0476 ETH, a un precio de **2,625**. Es exacto porque, sin comisión, precio efectivo = P₀·(1 + Δx/x) = 2,500 × (1 + 0.05).
- **(b)** k = 4×10⁸. Con arbitraje, x = √(k/p) = **333.3333 ETH** y y = √(k·p) = **1,200,000 USDC**.
  - El LP con 1% vale 2√(k·p)·1% = **$24,000**. HODL (4 ETH + 10,000 USDC) vale 4·3,600 + 10,000 = **$24,400**.
  - IL = 2√1.44/2.44 − 1 = **−1.639%**, es decir **−$400**.
- **(c)** Con r = 0.64: IL = 2(0.8)/1.64 − 1 = **−2.439%**. El LP vale $16,000 y HODL, $16,400: de nuevo **−$400**.
  - Demostración: HODL = x₀·p + x₀·p₀ y LP = 2√(k·p) = 2x₀√(p₀·p), porque k = x₀²·p₀. Entonces HODL − LP = x₀·(√p − √p₀)².
  - Con x₀ = 4 ETH (1% de 400): 4·(60 − 50)² = 4·(40 − 50)² = **400**. La pérdida en dólares es simétrica en √p, no en p.
- **(d)** Las comisiones del LP deben sumar ≥ $400. Con 0.30%, su parte del volumen debe ser $400/0.003 = $133,333; con 1% del pool, el pool debe mover **$13.33 millones**, 6.67 veces el TVL inicial de $2 M.

**Fuente.** Angeris et al., arXiv 1911.03380, ec. 3, 9 y 10; MOOC de Berkeley, clase 5, lámina 47 ([06](../recursos/06-decentralized-finance-mooc.md)); capítulo 03, §2.1-2.2 y apéndice A.

**Rúbrica.** (a) 3 pts: 2 por el cálculo con comisión y 1 por la explicación sin comisión; (b) 3 pts; (c) 3 pts: 2 por la demostración; (d) 1 pt. Restar 2 pts si se trata la pérdida impermanente como pérdida realizada sin mencionar que la contrapartida es la ganancia del arbitrajista.

---

## P2. Factor de salud, liquidación y sobreliquidación (cálculo)

**Pregunta.** Un protocolo tipo Aave tiene umbral de liquidación LT = 0.80, bono de liquidación de 5% y *close factor* de 50%. Un usuario deposita 2 BTC a $100,000 y pide prestados 110,000 USDC.

- (a) Calcula el HF inicial, el precio de liquidación y la caída tolerable. Muestra que la caída tolerable es 1 − 1/HF.
- (b) El BTC cae a $68,000. Calcula el HF. El liquidador repaga el máximo permitido: ¿cuánto BTC recibe y cuánto gana (antes de gas y deslizamiento)?
- (c) Después de la liquidación: ¿cuánto colateral y cuánta deuda quedan, cuál es el HF y cuál el nuevo precio de liquidación?
- (d) ¿Cuál es el repago mínimo que habría devuelto el HF a 1? Compáralo con lo que permite el *close factor* y explica qué es la "sobreliquidación".

**Respuesta de referencia.**

- **(a)** HF = 2·100,000·0.80/110,000 = **1.4545**. Precio de liquidación = 110,000/(2·0.80) = **$68,750**. Caída tolerable = 1 − 68,750/100,000 = **31.25%**, que es igual a 1 − 1/1.4545.
- **(b)** HF = 2·68,000·0.80/110,000 = **0.9891**: liquidable.
  - El liquidador repaga 50%: **55,000 USDC**. Recibe 55,000·1.05/68,000 = **0.849265 BTC** ($57,750).
  - Gana **$2,750**.
- **(c)** Quedan 1.150735 BTC ($78,250) y una deuda de 55,000.
  - HF = 78,250·0.8/55,000 = **1.1382**.
  - Nuevo precio de liquidación: 55,000/(1.150735·0.8) = **$59,744**.
- **(d)** Se busca r tal que (q·P − r·1.05)·0.8 = D − r. Resulta r = (110,000 − 108,800)/(1 − 0.84) = **7,500 USDC**.
  - El *close factor* permite 55,000: **7.3 veces más**.
  - El costo del bono para el deudor sube de $375 (7,500 × 5%) a $2,750.
  - Qin et al. llaman a esto *over-liquidation*: el diseño de *spread* fijo con *close factor* favorece al liquidador sobre el deudor.

**Fuente.** Qin, Zhou, Gamito, Jovanovic y Gervais, *An Empirical Study of DeFi Liquidations*, arXiv 2106.06389, ec. 1-4 y §4.4.1; capítulo 03, §2.3 y apéndice A.

**Rúbrica.** (a) 3 pts; (b) 3 pts; (c) 2 pts; (d) 2 pts. Restar 2 pts si se confunde el LT con el LTV máximo de originación, o el bono con la comisión del protocolo.

---

## P3. USDC y SVB: valor fundamental contra precio de pánico (cálculo e interpretación)

**Pregunta.** El 12-mar-2023, Circle informó que su reserva era de $32.4 mil M en letras del Tesoro y $9.7 mil M en efectivo, y que $3.3 mil M estaban en SVB.

- (a) Calcula el valor "justo" de 1 USDC si SVB pagaba 0%, 50% o 100%.
- (b) USDC tocó $0.8726 el 11-mar. ¿Qué pérdida de reserva implica ese precio, y cuántas veces la exposición a SVB?
- (c) Explica por qué el precio cayó por debajo del peor caso fundamental, y por qué DAI también perdió la paridad.
- (d) ¿Qué evento restauró la paridad y cuándo?

**Respuesta de referencia.**

- **(a)** La reserva total es de $42.1 mil M y SVB representa 7.84% (Circle dice "*about 8%*"). Los valores justos son **0.9216, 0.9608 y 1.0000**.
- **(b)** 1 − 0.8726 = 12.74% de la reserva, **1.63 veces** todo lo depositado en SVB (con $0.88: 1.53 veces).
- **(c)** Fue un descuento de **liquidez y pánico**, no de solvencia:
  - la noticia llegó en fin de semana, con las transferencias bancarias cerradas y sin redención primaria;
  - los formadores de mercado no podían arbitrar contra el emisor;
  - había incertidumbre sobre otros bancos: Signature fue cerrado el 12-mar.
  - DAI cayó (≈ $0.88-0.89) porque más de la mitad de su respaldo era USDC vía el PSM: el "*tethering*" a USDC que el MOOC señalaba desde 2021.
- **(d)** La declaración conjunta de Tesoro, Fed y FDIC del **12-mar-2023, 18:15 EDT**, con la excepción de riesgo sistémico: todos los depositantes de SVB y de Signature quedaron protegidos, con acceso desde el 13-mar. Circle confirmó que los $3.3 mil M estarían disponibles, y la paridad volvió el 13-mar.

**Fuente.** [Circle](https://www.circle.com/pressroom/3-3-billion-of-usdc-reserve-risk-removed-dollar-de-peg-closes); [Fed](https://www.federalreserve.gov/newsevents/pressreleases/monetary20230312b.htm); [CNN](https://www.cnn.com/2023/03/11/business/stablecoin-circle-silicon-valley-bank); [CoinDesk sobre DAI](https://www.coindesk.com/markets/2023/03/11/dai-depegs-as-stablecoin-rout-plagues-crypto); Klages-Mundt, MOOC, lámina 63; capítulo 03, §2.6.

**Rúbrica.** (a) 3 pts; (b) 2 pts; (c) 3 pts: se exige la distinción entre liquidez y solvencia, y el canal del PSM; (d) 2 pts.

---

## P4. Terra/UST: cuándo el arbitraje estabilizador se vuelve una espiral (análisis con cifras)

**Pregunta.** Explica el mecanismo de acuñación y quema UST ↔ LUNA con un ejemplo numérico de cada lado de la paridad. Identifica la **condición** bajo la cual el mismo arbitraje desestabiliza, y fecha cuándo se cruzó en mayo de 2022. Usa los datos del NBER y de la prensa: oferta de UST, depósitos y rendimiento de Anchor, reservas de LFG, volumen canjeado y oferta de LUNA. Explica por qué la crisis de mayo de 2021 no terminó en colapso. Clasifica el colateral según la taxonomía de Klages-Mundt.

**Respuesta de referencia.**

- **Mecanismo.** 1 UST se canjea por $1 en LUNA, y viceversa.
  - Con UST en $1.05 y LUNA en $10: se compran 0.1 LUNA, se queman por 1 UST y se vende: **+$0.05**. Esto contrae LUNA y expande UST.
  - Con UST en $0.95: se compra UST, se quema por $1 en LUNA (0.1) y se vende: **+$0.05**. Esto contrae UST y **acuña LUNA**.
- **Condición de inestabilidad.** El respaldo es endógeno: su valor depende de la confianza en el propio sistema.
  - Cuando la capitalización de LUNA se acerca a la oferta de UST, cada redención diluye LUNA, su precio cae, baja el respaldo y la redención deja de ser creíble.
  - El NBER fecha el cruce la noche del **9-may-2022**: la capitalización de LUNA igualó la oferta de UST y UST cayó a **$0.75**. Al cierre del 13-may estaba **por debajo de $0.20**.
- **Cifras:**
  - oferta de UST: **18.5 mil M**; en Anchor, **~12 mil M (~65%)** al **19.5%** subsidiado;
  - primer retiro: 375 M de UST de 2 direcciones el 7-may;
  - del 7 al 13-may se canjearon **7.42 mil M de UST por $4.65 mil M** ($0.627 por UST);
  - LFG pasó de ~80,300 BTC (6-may) a **313 BTC** (16-may);
  - la oferta de LUNA subió de ~350 M a **más de 6.5 billones**.
- **Mayo de 2021.** El sistema era mucho más pequeño y Terraform pudo actuar como prestamista de última instancia. La nueva paridad se leyó como señal de estabilidad. En 2022, el mercado sabía que la oferta de UST y lo depositado en Anchor superaban con mucho los recursos para defender la paridad (NBER).
- **Taxonomía.** Colateral **endógeno**, en el esquema de "*seigniorage shares*". Klages-Mundt (MOOC, oct-2021, lámina 77) advirtió que un ataque especulativo podía colapsar el valor de ese respaldo, y nombró a UST y a Titan.

**Fuente.** Liu, Makarov y Schoar, [NBER w31160](https://www.nber.org/papers/w31160), pp. 3-4 y 22; Harvey, deck de Infraestructura 2024, láminas 142-154 ([12](../recursos/12-decentralized-finance-the-future-of-finance.md)); [CoinDesk, 16-may-2022](https://www.coindesk.com/business/2022/05/16/luna-foundation-guard-left-with-313-bitcoin-after-ust-crash); [The Block](https://www.theblock.co/post/146762/luna-supply-soared-to-6-5-trillion-coins-before-terras-latest-halt).

**Rúbrica.** Mecanismo con ambos ejemplos: 3 pts. Condición y fecha: 3 pts. Al menos cuatro cifras correctas con su fuente: 2 pts. Contraste con 2021 y taxonomía: 2 pts. Restar 2 pts si se dice que "80% de UST estaba en Anchor" sin notar que el NBER mide ~65%.

---

## P5. Ataque de oráculo con préstamo relámpago: bZx, 18-feb-2020 (análisis y aritmética)

**Pregunta.** El atacante pidió prestados 7,500 ETH en un flash loan. Cambió 540 ETH por sUSD en Uniswap y 360 ETH en Kyber, con lo que el precio de esos mercados, que eran el oráculo de bZx, bajó de 268.30 a 106.05-108.44 sUSD/ETH. Compró sUSD con 3,517.86 ETH en Synthetix, a precio justo. Depositó 1,099,841.39 sUSD como colateral en bZx, pidió prestados 6,799.27 ETH y devolvió el flash loan.

- (a) Calcula la ganancia del atacante y la pérdida de los prestamistas de bZx, valuando el sUSD a 268.30.
- (b) ¿Por qué la atomicidad vuelve el ataque casi sin riesgo?
- (c) Propón dos defensas y el costo de cada una. Enuncia la condición de Harvey para que un oráculo sea vulnerable.
- (d) El artículo reporta "c. 634.9k USD" de ganancia con ETH en 282.91. ¿Qué haces con esa cifra?

**Respuesta de referencia.**

- **(a)** Ganancia = 6,799.27 − 3,517.86 − 360 − 540 = **2,381.41 ETH**. Pérdida de los prestamistas = 6,799.27 − 1,099,841.39/268.30 = 6,799.27 − 4,099.30 = **2,699.97 ETH**.
- **(b)** Todo ocurre en una sola transacción. Si al final no hay ganancia o el flash loan no se devuelve, la transacción revierte y el atacante solo pierde el gas: pagó 0.42 ETH. El préstamo le da el tamaño necesario para mover un mercado de poca liquidez.
- **(c)** Defensas:
  1. **Mediana de varias fuentes independientes**, algunas fuera de la cadena: una minoría de datos manipulados no mueve la mediana más allá de los honestos (Juels). Costo: confiar en operadores de oráculos y en su disponibilidad.
  2. **TWAP**: la manipulación debe sostenerse durante varios bloques, lo que expone al atacante a arbitraje y cuesta capital. Costo: precio rezagado, que en Iron Finance aceleró la espiral.
  - Otras válidas: límites de préstamo por bloque y cotas de desvío.
  - **Condición de Harvey:** el oráculo es vulnerable si su **costo de corrupción es menor que la ganancia de corromperlo**.
- **(d)** 2,381.41 × 282.91 = **$673,725**, que no cuadra con $634.9k (esa cifra implica ~$266.6 por ETH). La lámina de Juels usa $673k. Se reporta en ETH, la unidad del ataque, y se anota la inconsistencia.

**Fuente.** Qin, Zhou, Livshits y Gervais, arXiv 2003.03810, §3.2; Juels, MOOC clase 8, láminas 44-53; Harvey, deck 6, lámina 50 ([07](../recursos/07-defi-and-the-future-of-finance.md)); Finematics sobre Iron Finance ([03](../recursos/03-finematics.md)).

**Rúbrica.** (a) 3 pts; (b) 2 pts; (c) 3 pts, con los costos de cada defensa; (d) 2 pts.

---

## P6. MEV: el ataque sándwich y la tolerancia de deslizamiento (cálculo guiado e interpretación)

**Pregunta.** Una víctima compra ETH con 50,000 USDC en un pool de 2,000,000 USDC y 1,000 ETH (comisión de 0.30%), con tolerancia de deslizamiento de 1%.

- (a) Describe el sándwich paso por paso y explica por qué la tolerancia acota la ganancia del atacante.
- (b) Una simulación da una ganancia bruta máxima del atacante de ≈ $448 con 1% de tolerancia y ≈ $1,344 con 3%. En un pool de 20,000,000 USDC con comisión de 0.30% el ataque no es rentable; con comisión de 0.05%, ≈ $400. Interpreta los tres resultados.
- (c) Pon el sándwich en contexto con la medición histórica del MEV y con la arquitectura actual de Ethereum.
- (d) ¿Qué implica para nuestra cuenta, que opera spot en un exchange centralizado?

**Respuesta de referencia.**

- **(a)** Pasos:
  1. El atacante ve la orden en el mempool y compra antes, subiendo el precio.
  2. La víctima ejecuta a un precio peor.
  3. El atacante vende después, al precio inflado.
  - La orden de la víctima revierte si recibe menos del mínimo que fijó (su tolerancia). Por lo tanto, el atacante solo puede empujar el precio hasta ese límite.
- **(b)** Interpretación:
  - La ganancia es aproximadamente **tolerancia × monto de la víctima**: 0.9% con 1% de tolerancia, 2.7% con 3%. La tolerancia es lo que se regala.
  - En un pool profundo, una operación de 0.25% del pool mueve poco el precio, y las dos comisiones de 0.30% del atacante superan el movimiento: no es rentable.
  - Con comisión de 0.05%, el costo es menor y vuelve a ser rentable.
  - Conclusión: el riesgo crece con el tamaño relativo de la operación, con la tolerancia y con comisiones bajas.
- **(c)** Contexto:
  - Qin, Zhou y Gervais miden en 32 meses (dic-2018 a ago-2021) **$174.34 M** en sándwiches, dentro de **$540.54 M** de MEV total (con liquidaciones por $89.18 M y arbitraje por $277.02 M).
  - Hoy el MEV pasa por PBS/MEV-Boost (~90% de los validadores), con cinco *builders* haciendo ~90% de los bloques (Finematics, oct-2023).
  - Existen mempools privados, como Flashbots Protect, que evitan exponer la orden.
- **(d)** En un exchange centralizado no hay mempool público ni sándwich on-chain; el análogo es el diferencial y el impacto en el libro de órdenes.
  - Conviene usar órdenes límite y no operar a mercado en momentos de libro delgado, como una cascada.
  - Si algún día se opera on-chain: pools profundos, tolerancia estrecha y RPC privado.

**Fuente.** MOOC clase 13, láminas 53-73; Qin, Zhou y Gervais, arXiv 2101.05511, fig. 1; Finematics, *Decoding MEV* (27-oct-2023); capítulo 03, §2.5 y apéndice A.

**Rúbrica.** (a) 3 pts; (b) 3 pts; (c) 2 pts; (d) 2 pts. Restar 2 pts si se afirma que una tolerancia alta "protege" la ejecución.

---

## P7. 10-oct-2025: ¿dónde estaba el apalancamiento que movió al BTC? (análisis con cifras)

**Pregunta.** Con estos datos:

- más de $19 mil M liquidados el 10 y 11-oct (CoinGlass, vía CoinGecko y CoinShares); CNN daba $18.28 mil M en un corte del 11-oct;
- Aave liquidó ~$180 M en una hora;
- el BTC pasó de $122,574 a $104,782 dentro del día (CNN registra un mínimo de $103,000);
- el interés abierto bajó de $175 mil M a $125 mil M según CoinShares, pero CoinGecko cita un récord previo de $217 mil M;
- USDe cotizó en $0.65 solo en Binance, entre las 21:36 y las 22:16 UTC, mientras valía ~$1 en otros mercados.

Preguntas:

- (a) ¿Qué fracción del evento fueron liquidaciones de préstamos DeFi? ¿Qué concluyes sobre dónde vigilar el apalancamiento de BTC?
- (b) Describe la cascada y cómo se transmite al spot.
- (c) ¿Por qué USDe valió $0.65 solo en Binance, y qué enseña sobre el diseño de oráculos y sobre nuestro custodio?
- (d) ¿Cuál era el riesgo para una cuenta solo spot, y qué señales debían vigilarse antes?

**Respuesta de referencia.**

- **(a)** 0.18/19 ≈ **0.9-1%**. El BTC cayó **−14.5%** dentro del día.
  - El apalancamiento que mueve el precio del BTC está en los **perpetuos**, de exchanges y de plataformas on-chain (Hyperliquid activó ADL), no en los préstamos DeFi.
  - Hay que vigilar interés abierto y *funding*; el TVL no sirve para esto.
- **(b)** Mecanismo:
  1. El choque (el anuncio arancelario contra China) baja el precio.
  2. Las posiciones con margen justo son liquidadas a mercado.
  3. El libro se vacía y el precio cae más.
  4. Se alcanzan los umbrales siguientes.
  - El arbitraje entre mercados lleva la presión al spot de todos los exchanges.
  - Es no lineal: el modelo del capítulo da de −5.7% a −27% ante el mismo −5% inicial, según la profundidad del mercado. Es la "*deleveraging spiral*" del MOOC.
- **(c)** Binance valuaba el colateral de margen con su **propio libro de órdenes**, que se quedó sin compradores. Fue un oráculo de un solo mercado, sin mediana ni cotas.
  - En términos de Juels, faltó agregar varias fuentes. En términos de Harvey, el costo de corromper el oráculo era bajo en un libro delgado.
  - Binance compensó a los afectados en futuros, margen y préstamos. El monto ($283-328 M) varía según la fuente; no lo verifiqué en fuente primaria.
  - Para nosotros: el exchange es un **punto de riesgo operativo y de custodia**.
- **(d)** Una cuenta spot sin apalancamiento **no se liquida**. Su riesgo es de precio y de ejecución: el deslizamiento se dispara. Vender a mercado dentro de la cascada materializa el peor precio.
  - Señales previas: interés abierto en récord con *funding* persistentemente positivo, concentración de umbrales de liquidación cerca del precio y libros delgados en fin de semana o tarde de viernes.
  - Se exige notar que los umbrales del capítulo son tentativos y sin prueba histórica, y que hay datos discrepantes (interés abierto, cifra total, mínimo del BTC).

**Fuente.** [CoinGecko](https://www.coingecko.com/learn/october-10-crypto-crash-explained); [CoinShares](https://coinshares.com/corp/insights/knowledge/billions-in-liquidations-what-happened/) (20-oct-2025); [CNN](https://www.cnn.com/2025/10/11/business/trump-tariffs-crypto-selloff); [CoinDesk sobre Aave](https://www.coindesk.com/markets/2025/10/11/aave-sees-64-flash-crash-as-defi-protocol-endures-largest-stress-test); capítulo 03, §4.1.

**Rúbrica.** (a) 3 pts; (b) 3 pts; (c) 2 pts; (d) 2 pts. Restar 2 pts si se atribuye la cascada a DeFi sin cuantificar.

---

## P8. Jueves Negro de MakerDAO: liquidación por subasta y cifras que no cuadran (análisis)

**Pregunta.**

- (a) Explica la subasta en dos fases de Maker (*tend* y *dent*) y por qué el 12 y 13-mar-2020 hubo subastas ganadas pujando 0 DAI.
- (b) Reconcilia estas cifras: Finematics, "*around $4M*"; MOOC, "*$8m*"; Glassnode (17-mar-2020), "$4.5 M de DAI sin respaldo" y "más de $8 M de ETH liquidados por 0 DAI"; ~5.3 M DAI recaudados en la subasta de MKR; Qin et al., 13.13 M USD de ganancia de liquidadores en Maker ese mes.
- (c) ¿Qué concluye Qin et al. al comparar subastas y *spread* fijo?
- (d) ¿Qué cambió Maker después, y qué nuevo riesgo introdujo que se materializó en 2023?

**Respuesta de referencia.**

- **(a)** Las dos fases:
  - *Tend*: los postores ofrecen pagar más deuda por todo el colateral.
  - *Dent*: ya con la deuda completa, ofrecen aceptar menos colateral.
  - Cada fase requiere varias transacciones y la subasta dura horas.
  - Con el ETH −43% (de $194 a $111) y el gas medio 6 veces mayor, con picos horarios de ~200 gwei, los bots de los *keepers* no lograron incluir sus pujas. Un postor ganó subastas pujando 0: la subasta terminó con una sola oferta.
- **(b)** Las cifras miden cosas distintas:
  - $4-4.5 M: estimación temprana del **déficit** (DAI sin respaldo);
  - ~5.3 M DAI: lo que se **recaudó** después acuñando MKR;
  - más de $8 M (Glassnode) o $8.32 M (otro análisis): el **ETH adjudicado en cero**;
  - 13.13 M USD: la **ganancia** de todos los liquidadores de Maker en marzo (Qin et al.).
  - No hay una cifra primaria de MakerDAO disponible: su blog redirige a sky.money.
- **(c)** Qin et al.:
  - el *spread* fijo con *close factor* sobreliquida y favorece al liquidador;
  - las subastas parecen más favorables al deudor en promedio, pero exponen al liquidador al riesgo de precio (641 liquidaciones con pérdida) y son **frágiles ante la congestión**.
- **(d)** Cambios en Maker:
  - Adoptó **subastas holandesas** (desde abr-2021): liquidación instantánea en una transacción, préstamo relámpago del colateral y precio que baja con el tiempo, "*nobody can get the collateral for free by accident*" (MOOC, clase 6, lámina 33).
  - Ancló DAI a **USDC mediante el PSM** ("*tethered to USDC (+ custodial risks)*", Klages-Mundt, lámina 63).
  - Ese riesgo custodial se materializó el 11-mar-2023: DAI cayó a ≈ $0.88-0.89 junto con USDC.

**Fuente.** Qin et al., arXiv 2106.06389, §3.2.1, §4.3 y §5.1; MOOC clase 6, láminas 32-39; [Glassnode](https://research.glassnode.com/what-really-happened-to-makerdao/); [Blockonomi](https://blockonomi.com/makerdao-emergency-5-million-dai-raised/); Finematics, *History of DeFi* ([03](../recursos/03-finematics.md)); Klages-Mundt, MOOC clase 7 ([06](../recursos/06-decentralized-finance-mooc.md)).

**Rúbrica.** (a) 3 pts; (b) 3 pts: se exige distinguir déficit, recaudación, ETH en cero y ganancia; (c) 2 pts; (d) 2 pts.
