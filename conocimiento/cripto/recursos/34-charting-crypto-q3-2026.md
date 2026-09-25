# 34 · Charting Crypto Q3 2026 (Coinbase Institutional y Glassnode)

> Ficha de recurso · Grupo G5 · Estudiada el 25-sep-2026 por `analista-cripto` · **Acceso: íntegro** (PDF de 34 páginas: texto y todas las gráficas) · **Grado global: C** (lo publica un exchange; las zonas de "acumulación" se definen dentro de la muestra).
>
> **Etiquetas:**
> - **[H]** hecho con fuente y página;
> - **[I]** inferencia (digo si es del autor o nuestra);
> - **[O]** opinión o pronóstico del autor.
>
> **Grados:** A = identidad o dato oficial · B = evidencia sólida con salvedades · C = muestra corta o no reproducible · D = narrativa.
>
> **"p. N"** es la página del PDF, que coincide con la numeración del índice del reporte. Los números marcados **"lectura de gráfica"** los leí a ojo sobre la imagen; su error puede ser de ±5-10%.

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2026. Edición Q3 2026 con datos al **30-jun-2026** (p. 3); el PDF se creó el 13-jul-2026 |
| Autor | Coinbase Institutional (Colin Basco, estratega cuantitativo) y Glassnode Analyst Team (p. 4) |
| Tipo | Reporte trimestral con 30 gráficas sobre mercado, macro, flujos, on-chain y derivados |
| Costo | Gratis |
| URL | https://assets.ctfassets.net/k3n74unfin40/1E4sJdvhe38EFmPmjrczSq/6cd4e695f812889938b702fd487e184d/Charting_Crypto_3Q26.pdf |
| **Conflictos de interés** | **Coinbase es un exchange.** Gana con el volumen de trading, los derivados (Coinbase Financial Markets es una FCM registrada ante la CFTC; p. 34), la custodia y los ingresos por USDC. Opera Base y creó el estándar x402, que el reporte presenta como "fuente durable de demanda on-chain" (p. 4). El aviso legal admite que "Coinbase may have financial interests in… some of the assets" (p. 34). **Glassnode vende datos.** Incentivo común: que lo "estructural" se vea siempre al alza |

## 2. Acceso real

- **Cómo lo obtuve:** descargué el PDF oficial (3.8 MB) al scratchpad. Tiene 34 páginas; `pypdf` extrajo todo el texto.
- **Gráficas:** las rendericé con PyMuPDF y **las revisé una por una**. Varias cifras solo existen en la gráfica y vienen marcadas como "lectura de gráfica".
- **Nivel: íntegro.**

## 3. Lo esencial

- **[O] Perspectiva para 3T26: "neutral"** (pp. 4 y 6).
  - Según el reporte, BTC pasa "from a corrective phase toward accumulation", aunque la liquidez macro "keeps us disciplined".
  - Recomienda sumar exposición de forma paciente y con riesgo definido, en vez de perseguir rebotes.
- **[H] Macro (p. 4):**
  - en junio, en la primera reunión que presidió Kevin Warsh, la Fed dejó la tasa en 3.50-3.75% por cuarta vez seguida;
  - subió su pronóstico de inflación 2026 a **3.6%** y la mediana de tasa para 2026 a **3.8%**, lo que dejó abierta la puerta a un alza.
- **[H] Mercado:**
  - en el 2T26 la capitalización cripto sin stablecoins cayó ≈ 12%;
  - la oferta de stablecoins marcó récord y su dominancia subió (p. 8).
- **[O] Ciclo (p. 9):** "the top has almost certainly been put in during October 2025". El propio reporte admite que "it is unclear if these patterns are still relevant".
- **[H] Correlaciones diarias del 1-abr al 30-jun-2026 (p. 11):**
  - **BTC/S&P 0.12**, contra 0.58 en el 4T25;
  - **BTC/oro 0.57**;
  - BTC/ETH 0.87;
  - BTC/DXY −0.38;
  - BTC/bono de EUA a 2 años −0.39.
- **[H] Volatilidad realizada de 90 días al cierre de junio: BTC ≈ 38%, ETH ≈ 52% y SOL ≈ 57%** (p. 12, lectura de gráfica).
- **[H] Flujos de ETF (pp. 4, 6 y 13):**
  - los ETF spot de BTC en EUA tuvieron **flujos netos negativos en el 1S26**, aunque las salidas "show early signs of exhausting";
  - sus activos pasaron de un pico de ≈ US$180-190 mil M en oct-2025 a ≈ US$85-90 mil M en jul-2026 (p. 13, lectura de gráfica).
- **[H] Stablecoins (p. 14, lectura de gráfica):**
  - oferta de ≈ US$310-315 mil M;
  - su crecimiento a 30 días fue **negativo (≈ −2 a −3%) al cierre de junio**;
  - el volumen de transferencias ajustado del último mes fue ≈ US$1.8 billones.
- **[H] Oferta de BTC (p. 16):**
  - circulante 20.05 M, el 95.5% del total;
  - inflación anual 0.8%.
  - Comprobación propia: 3.125 BTC × 144 bloques × 365 = 164,250 BTC al año, que sobre 20.05 M da **0.819%**. Coin Metrics da una oferta de 20,050,326 al 30-jun.
- **[H] NUPL ajustada por entidad:** bajó de "Optimism/Anxiety" a "Hope/Fear" y quedó "just above the Capitulation threshold" (pp. 17-18).
- **[H] MVRV y precio realizado (p. 19):**
  - "MVRV approached 1" en el 2T26;
  - el precio realizado ≈ US$53 mil (lectura de gráfica).
  - Comprobación propia con Coin Metrics al 30-jun-2026: **MVRV 1.103 y precio realizado US$53,070**.
- **[H] Oferta en ganancia (p. 20):**
  - cayó **debajo de su banda de −1 desviación estándar**, calculada con 4 años móviles: la "zona histórica de acumulación";
  - tocó ≈ 47-50% al cierre de junio (lectura de gráfica).
- **[H] Monedas dormidas y activas (p. 21):**
  - las que se movieron en los últimos 3 meses están en mínimos de varios años (≈ 2.4-2.6 M BTC, lectura de gráfica);
  - la oferta sin moverse por más de un año **sube** (≈ 12.2 M, lectura de gráfica).
- **[H] Puell Multiple ≈ 0.7:** el ingreso minero va ≈ 30% debajo de su promedio anual (p. 22).
- **[H] Tenedores de largo plazo (más de 155 días) (p. 23):**
  - acumularon en abril y mayo;
  - en junio volvieron monedas a los exchanges aunque sus saldos seguían subiendo.
- **[H] Interés abierto total de BTC (perpetuos, futuros a plazo y opciones) (pp. 17 y 24):**
  - ≈ US$65 mil M al cierre de junio, contra ≈ US$113 mil M en oct-2025 (lectura de gráfica);
  - según el reporte, el apalancamiento "stayed subdued".
- **[H] ETH (pp. 26-31):**
  - su NUPL volvió a "Capitulation" y su MVRV quedó debajo de 1, con precio realizado ≈ US$2.2 mil (lectura de gráfica, p. 29);
  - TVL en DeFi de **US$38.9 mil M** e inflación de 0.86% (p. 26).
- **[H] Actividad en Ethereum (pp. 27 y 33):** bajó la razón de actividad L2/L1 y la de stablecoins en L2 frente a L1: el capital se concentra en la capa base.
- **[O] Qué los volvería más constructivos (p. 6):**
  - una Fed más blanda;
  - recuperar las resistencias;
  - que vuelvan las entradas a los ETF.
- **[O] Qué los preocuparía (p. 6):** un alza de tasas, otro episodio de desapalancamiento o la ruptura del soporte.

## 4. Qué cambia para invertir

- **Lo que se puede comprobar se comprobó.** Coin Metrics confirma el MVRV de 1.10 y el precio realizado de ≈ 53 mil al 30-jun. El precio nunca cerró debajo del precio realizado en 2026: el MVRV mínimo del año fue 1.103, ese mismo 30-jun. Glassnode (semana 38) dice lo mismo.
- **La lectura de "acumulación" acertó ex post, pero el reporte no prometía nada.**
  - El 30-jun (58,525) resultó ser el mínimo de cierre del año hasta hoy. Al 24-sep BTC va en 84,387 (+44%).
  - [I, nuestra] Sin embargo, el mismo reporte era "neutral" y exigía recuperar resistencias. La zona de acumulación por oferta en ganancia está definida con una banda de 4 años ajustada en muestra, y su historial tiene ≈ 4 episodios comparables. Un acierto no valida el indicador: es grado C.
- **Macro:**
  - la correlación BTC/S&P cayó a 0.12 y la de BTC/oro subió a 0.57 (p. 11);
  - [I, del autor] BTC reacciona a la tasa real y al dólar, igual que el oro.
  - Para nosotros: en esta temporada el riesgo de tasas (alza de la Fed, bono a 10 años en 4.8% según la semana 36 de Glassnode) pesa más que cualquier señal on-chain.
- **Derivados:** con el interés abierto ≈ 40% debajo del pico, el mercado está menos expuesto a cascadas de liquidación. La lección del 10-oct-2025, que registró el comité, es que con apalancamiento alto las caídas intradía se amplifican.
- **Para la cuenta de Binance:**
  - el reporte no contradice el filtro SMA200;
  - al 24-sep el precio está ≈ 19% arriba de la SMA200 (84,387 contra 70,848 con Coin Metrics), así que el filtro dice "invertido";
  - la referencia on-chain más cercana es el costo base STH, ≈ 71.3-71.6 mil (fichas 05 y cap. 05).

## 5. Contrapuntos y límites

- **Conflicto de interés.** Un exchange tiene incentivos para que "the structural story, meanwhile, continues to broaden" (p. 4), por ejemplo con perpetuos regulados y x402, productos que Coinbase vende o promueve.
- **Analogías de ciclo con n = 4.** El propio reporte duda de ellas (p. 9).
- **Contradicción interna sobre stablecoins.** El texto habla de oferta récord en el trimestre (p. 8), pero la gráfica muestra un crecimiento a 30 días **negativo** al 30-jun (p. 14). Las dos cosas son ciertas: con DefiLlama, el pico fue de US$322.4 mil M el 17-may-2026 y al 30-jun la oferta había caído 3.5%, a 311.1.
- **Muchas cifras solo están en gráficas,** sin tablas ni datos descargables.
- **Datos al 30-jun.** No ve el squeeze de agosto ni el rally de septiembre.

## 6. Autoexamen

1. **¿Qué significa un MVRV de 0.85 según el reporte y qué valor tuvo BTC al cierre del 2T26?**
   - *Respuesta:* que el precio está 15% debajo del costo base promedio (el tenedor promedio pierde 15%). BTC "approached 1"; con Coin Metrics, 1.103 al 30-jun-2026.
   - *Fuente:* p. 19; API de Coin Metrics.
2. **¿Cómo cambió la correlación de BTC con el S&P y con el oro, y qué interpreta el reporte?**
   - *Respuesta:* S&P de 0.58 (4T25) a 0.12 (2T26); oro, 0.57. BTC y oro cayeron juntos por la tasa real y el dólar.
   - *Fuente:* p. 11.
3. **¿Qué es el Puell Multiple y qué valor tenía?**
   - *Respuesta:* el valor diario de la emisión de BTC en USD dividido entre su media de 365 días. Estaba cerca de 0.7: el ingreso minero iba ≈ 30% debajo de su promedio anual.
   - *Fuente:* p. 22.
4. **Encuentra la aparente contradicción del reporte sobre stablecoins y resuélvela con datos.**
   - *Respuesta:* p. 8 habla de oferta récord; la p. 14 muestra un crecimiento a 30 días negativo al cierre de junio.
   - Con DefiLlama, el pico fue de US$322.4 mil M el 17-may y al 30-jun había 311.1 (−3.5%).
   - *Fuente:* pp. 8 y 14; API de DefiLlama.

## 7. Grado de evidencia

- **B:** los datos descriptivos, como MVRV, precio realizado y oferta, verificados con Coin Metrics.
- **C:** las zonas de acumulación y las analogías de ciclo.
- **D:** la narrativa "estructural" (x402, economía de máquinas).
- **Global: C.**
