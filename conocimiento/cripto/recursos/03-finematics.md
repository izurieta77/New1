# 03 · Finematics (serie DeFi en YouTube y artículos en finematics.com)

> Ficha de estudio del grupo G3 DeFi, escrita por `analista-cripto` el 25-sep-2026. Es formación, no recomendación.
> **Estado:** estudiado por secciones. Leí completos 13 artículos principales de 62 publicados.
> **Capítulo de síntesis:** [03-defi-mecanica-riesgos-y-academia.md](../03-defi-mecanica-riesgos-y-academia.md).

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2020. El primer artículo DeFi, "What is DEFI?", es del 02-jul-2020. El más reciente que revisé es del 30-nov-2024. |
| Autor | Finematics. Firma "Jakub", quien se presenta como "*software engineer passionate about decentralized finance*" ([About](https://finematics.com/about/)). |
| Tipo | Canal de YouTube y blog. Cada artículo es el texto de un video: la página incrusta el video con su ID. |
| Nivel | Principiante-intermedio |
| Costo | Gratis. Patreon opcional. |
| Idioma | Inglés |
| URL | https://www.youtube.com/@Finematics · https://finematics.com |

**Conflictos de interés (página "About" y artículos):**

- Tiene tres fuentes de ingreso ligadas a su audiencia:
  - Patreon con comunidad privada;
  - donaciones en ETH (finematics.eth) y en BTC;
  - enlaces de referido (Brave, Ledger) y de afiliado ("*affiliate links that help this website to grow*").
- Vende **consultorías DeFi privadas por hora** ([Consultation](https://finematics.com/consultation/)).
- Participó en Gitcoin Grants (ronda 10).
- El artículo de hackeos se escribió en colaboración con rekt.news.
- Declara su postura: "*I believe DeFi is the future*".
- **No verificado:** si los videos llevan patrocinios. YouTube está bloqueado desde aquí.

## 2. Acceso real (consultado el 25-sep-2026)

- Bajé el sitemap (`wp-sitemap-posts-post-1.xml`, 62 entradas) y descargué 22 artículos con curl.
- Los videos no los vi: yt-dlp está bloqueado para YouTube. Los artículos son el equivalente en texto de cada video.

| Artículo (fecha) | Nivel |
|---|---|
| What is DeFi? (02-jul-2020) | Íntegro |
| How Do Liquidity Pools Work? (20-jul-2020) | Íntegro |
| What is Impermanent Loss? (21-ago-2020) | Íntegro |
| Flash Loans Explained (12-oct-2020) | Íntegro |
| Lending and Borrowing in DeFi (16-nov-2020) | Íntegro |
| History of DeFi (04-ene-2021) | Sección: Jueves Negro y DeFi Summer |
| Aave – The Road to $3 Billion (20-ene-2021) | Íntegro |
| Uniswap V3 Explained (23-mar-2021) | Sección: eficiencia de capital, comisiones y oráculos |
| The Truth About DeFi (05-abr-2021) | Sección |
| DeFi Hacks Explained (17-abr-2021) | Íntegro |
| Bank Run in DeFi – Iron Finance (24-jun-2021) | Íntegro |
| Rollups Explained (02-ago-2021) | Sección: optimistas frente a ZK |
| DeFi Past, Present and Future (30-mar-2022) | Sección |
| Decoding MEV (27-oct-2023) | Íntegro |
| The FTX Collapse (16-nov-2022) | Solo búsqueda de términos |

- **Stablecoins:** entre los 62 artículos no encontré un explicativo dedicado. El tema aparece en la introducción a DeFi, en Iron Finance y en Ampleforth; este último no lo leí.
- **Factor de salud:** no lo encontré en los artículos que revisé.
- **Terra:** no tiene artículo propio. Solo lo menciona de paso en los de mar-2022 y FTX.

**Nivel global: sección.**

## 3. Lo esencial

Etiquetas: [H] hecho con fuente · [I] inferencia · [O] opinión del autor.

1. **[H] Qué es DeFi** (02-jul-2020): un sistema financiero abierto, sin intermediarios, construido con contratos inteligentes, entonces casi todo en Ethereum.
   - Categorías: préstamos (Compound, entonces con ~$630 M), stablecoins, DEX, derivados, margen, seguros y oráculos. Se combinan como "*money Legos*".
   - Riesgos que enumera:
     - bugs;
     - llaves de administrador;
     - riesgo sistémico: una caída fuerte puede provocar "*a cascade of liquidations across multiple defi protocols*";
     - congestión de red que impide añadir colateral a tiempo;
     - incentivos cruzados, como el caso de COMP.
2. **[H] Pools de liquidez** (20-jul-2020):
   - Quien aporta liquidez (LP) recibe tokens LP; Uniswap v2 cobra 0.3% por operación y lo reparte entre ellos.
   - El producto constante "*can always provide liquidity, no matter how large a trade*" porque el precio sube de forma asintótica.
   - El deslizamiento depende del tamaño de la operación frente al pool.
   - Curve está hecho para activos de precio similar; Balancer admite hasta 8 tokens.
3. **[H + cálculo] Pérdida impermanente** (21-ago-2020). Pool de 20 ETH y 10,000 DAI a $500; el ETH sube a $550.
   - El arbitrajista compra 0.93 ETH por 488.09 DAI y deja el pool en 10,488.09 DAI y 19.07 ETH. Finematics publica una pérdida de **$23.41**.
   - En Python: las reservas exactas son 19.0693 ETH y 10,488.09 DAI, y la pérdida exacta es **$23.82**. Los $23.41 salen de redondear el ETH a 19.07.
   - El precio medio del arbitrajista es 524.44, no 524.83: el artículo divide entre 0.93 redondeado.
   - [I] La ganancia del arbitrajista, $23.82 antes de comisiones, es exactamente la pérdida del LP.
4. **[H + cálculo] Error de escala.** El artículo dice que "*if the price... goes up by 500% the LPs would experience a 25% impermanent loss*".
   - La fórmula 2√r/(1 + r) − 1 da −25.46% para r = 5, es decir, **+400%**.
   - Con +500% (r = 6) la pérdida es −30.0%.
5. **[H] Cómo se compensa la pérdida.** El LP gana solo si la pérdida impermanente es menor que las comisiones cobradas (más la minería de liquidez).
   - Curve reduce la pérdida al usar activos estables.
   - Balancer permite pesos como 80/20 o 98/2.
   - [O] Dice que Bancor v2, con oráculos, "*can completely mitigate impermanent loss*".
   - [H] Eso envejeció mal: Bancor suspendió su protección contra la pérdida impermanente en junio de 2022 por "*hostile market conditions*" ([The Block](https://www.theblock.co/post/153049/bancor-dex-pauses-impermanent-loss-protection-amid-market-instability); [Cointelegraph](https://cointelegraph.com/news/bancor-pauses-impairment-loss-protection-citing-hostile-market-conditions)).
6. **[H] Préstamos** (16-nov-2020):
   - Todo está sobrecolateralizado. En Compound, el factor de colateral de ETH y DAI era 75%.
   - Las tasas son variables y se calculan por bloque, según la oferta y la demanda.
   - Los cTokens suben su tipo de cambio (arrancan en 0.02); los aTokens se mantienen 1:1 y el saldo crece.
   - Compound usaba su propio oráculo; Aave, Chainlink con respaldo propio.
   - Riesgo poco obvio: la tasa del BAT llegó a más de 40% durante la fiebre del *yield farming*, lo que puede liquidar a quien no la vigila.
7. **[H + cálculo] Ejemplo de cETH.** 10 ETH / 0.021 = 476.19 cETH. Un mes a +0.0000000002 por bloque da 476.19 × 0.02103456 = **10.0164 ETH**: +0.16%.
   - El artículo multiplica por "0.0213456", una errata que daría 10.1646. Su resultado final, "~10.0165", corresponde al factor correcto.
8. **[H + cálculo] Préstamos relámpago** (12-oct-2020):
   - Son atómicos. Aave cobraba **0.09%**. Hubo préstamos de hasta 14 M DAI.
   - Usos: arbitraje, cambio de colateral y autoliquidación.
   - Ejemplo de arbitraje: 100,000 / 0.99 = 101,010.10 USDC; se devuelven 100,090 y quedan **920.10 DAI** de ganancia.
   - Riesgos del arbitrajista: comisión de gas, deslizamiento y bots del mempool que copian la transacción con más gas.
   - [H] Menciona el ataque a bZx, que manipuló el oráculo de Uniswap mediante un flash loan: "*incorrect assumptions when it comes to using Uniswap as a price oracle*".
9. **[H] Hackeos** (17-abr-2021, con rekt.news):
   - *Rug pull* de Meerkat: ~$31 M en un día.
   - Harvest Finance (oct-2020): pérdida de $33.8 M. El atacante usó un flash loan de $50 M en USDT, movió el precio en el pool Y de Curve y repitió el ciclo 32 veces, ganando ~$0.5 M por ciclo.
   - Arbitrajes en el lanzamiento de Saddle: 7.9 BTC en 6 minutos.
   - "*The majority of hacked (or exploited) protocols actually had a security audit*" (leaderboard de rekt.news; no lo verifiqué contra otra base).
10. **[H] Jueves Negro** (04-ene-2021):
    - El ETH cayó más de 30% en menos de 24 horas y el gas pasó de 200 gwei.
    - Los *keepers* de Maker ganaron subastas pujando 0 DAI.
    - Finematics cifra el faltante en "*around $4M*", cubierto subastando MKR nuevo.
    - Contraste con otras fuentes; las cifras miden cosas distintas y en momentos distintos:
      - Glassnode, 17-mar-2020: el ETH cayó 43%, de $194 a $111; quedaron "*$4.5 million worth of DAI... unbacked*"; y "*over $8 million in ETH was liquidated for zero DAI*" ([Glassnode](https://research.glassnode.com/what-really-happened-to-makerdao/)).
      - La subasta de MKR recaudó ~5.3 M DAI ([Blockonomi](https://blockonomi.com/makerdao-emergency-5-million-dai-raised/)).
      - Otras fuentes secundarias dan 5.67 M o 6.65 M DAI de déficit ([Crowdfund Insider](https://www.crowdfundinsider.com/2020/04/160799-makerdao-recommends-safety-measures-to-prevent-debt-crisis-created-following-last-months-historic-cryptocurrency-market-crash/) dice 6.65 M).
      - No encontré la cifra primaria de MakerDAO: su blog ahora redirige a sky.money.
    - La cifra de Finematics coincide con las estimaciones tempranas y queda por debajo de lo que se recaudó después.
11. **[H] Iron Finance, la primera corrida bancaria grande en DeFi** (16-jun-2021):
    - IRON se respaldaba en parte con USDC y en parte con TITAN, el token propio.
    - El TVL pasó de $2 mil millones y TITAN subió de $10 a $64 en una semana.
    - Pagaba 500% anual en IRON/USDC y 1,700% en TITAN/MATIC, y Mark Cuban lo mencionó.
    - El oráculo TWAP reportaba un precio de TITAN rezagado, así que el protocolo acuñaba cada vez más TITAN al redimir. Eso fue una espiral de muerte: TITAN llegó a casi 0.
    - Los tenedores de IRON recuperaron ~$0.75 en USDC.
    - Lecciones del autor:
      - diseñar para el peor escenario;
      - vigilar oráculos rezagados;
      - un LP en un pool con un token que va a 0 pierde casi 100%;
      - no seguir a celebridades;
      - un APR extremo es señal de riesgo.
12. **[H] MEV** (27-oct-2023):
    - Tipos: front-running, back-running, sándwich, censura y front-running generalizado. Distingue MEV "tóxico" y "no tóxico".
    - Historia en tres etapas: la era de las subastas de gas (PGA); Flashbots, cuyo cliente MEV-Geth llegó a ~90% del hashrate; y después del Merge, MEV-Boost, una forma de PBS que usa ~90% de los validadores.
    - Cadena actual: usuario → billetera → mempool público o privado → *searchers* → *builders* → *relays* → proponente.
    - Riesgo: "*the five main builders build around 90% of Ethereum blocks*".
    - Tamaño: más de 320,000 ETH de MEV desde el Merge, "~800 ETH/día". Lo comprobé: son 407 días, 786 ETH/día.
13. **[H] Rollups** (02-ago-2021):
    - Los optimistas usan pruebas de fraude y retiros de 1 a 2 semanas; los ZK, pruebas de validez y retiros rápidos.
    - Escalarían Ethereum de 15-45 a 1,000-4,000 transacciones por segundo.
    - El secuenciador está centralizado al principio.
14. **[H] Estado en 2021** (05-abr-2021): el TVL pasó de ~$15 mil millones a $45 mil millones en pocos meses; los DEX movían más de $50 mil millones al mes; la composabilidad se pierde entre capas 2.
15. **[H] Envejeció mal** (30-mar-2022, seis semanas antes del colapso de Terra):
    - "*DeFi on Avalanche, Fantom, Solana, Terra... rapid growth phase*".
    - "*Lido... Luna staking grew to an astonishing $7.5b*".
    - Presenta la protección de Bancor v3 contra pérdida impermanente como novedad.
16. **[O] Postura del autor:**
    - "*DeFi is the closest thing that can actually disrupt the traditional financial industry*";
    - los hackeos "*make the whole ecosystem... more antifragile*".
    - Ninguna de las dos afirmaciones viene con evidencia.
17. **[I] Mecánica que exige este estudio y el recurso no cubre:**
    - el **factor de salud** (ver [06](06-decentralized-finance-mooc.md), viñeta 6);
    - los datos de **Terra y de USDC/SVB** (ver [06](06-decentralized-finance-mooc.md), viñetas 18-19, y el capítulo).
    - Sí cubre ataques de oráculo y flash loans (bZx y Harvest), MEV y la pérdida impermanente.

## 4. Qué cambia para invertir

- **[I] Señales de alarma que el propio Finematics enseña:**
  - APR de tres o cuatro dígitos;
  - tokens propios que respaldan una stablecoin;
  - oráculos TWAP que se rezagan en caídas;
  - pools con un token que puede ir a 0.
  - Todas se repitieron en Terra (may-2022), con la plantilla de Iron Finance a mucha mayor escala: 18.5 mil M de UST en circulación ([NBER w31160](https://www.nber.org/papers/w31160)) frente a los más de $2 mil M de TVL de Iron.
- **[I] Cascadas y BTC spot.** Finematics describe el mecanismo ("*cascade of liquidations across multiple defi protocols*") pero no lo cuantifica.
  - En el evento del 10-oct-2025, el grueso se liquidó en perpetuos (más de $19 mil millones) y no en préstamos DeFi (Aave, ~$180 M). El BTC tocó −14.5% dentro del día (ver capítulo §4).
  - Para una cuenta spot sin apalancamiento es riesgo de precio, no de liquidación.
- **[I] Por qué no usamos rendimientos DeFi.** La propia pedagogía de Finematics lo explica:
  - el LP pierde frente a HODL en cuanto el precio se mueve;
  - los flash loans permiten manipular pools poco líquidos con capital ajeno;
  - las auditorías no garantizan nada;
  - el MEV le quita valor a quien opera on-chain.
  - Nuestra cuenta es spot en un exchange centralizado: no pagamos MEV on-chain, pero tampoco cobramos esas primas.
- **[I] Señales de riesgo sistémico a vigilar** (tomadas de sus casos):
  1. APR anormales;
  2. desvíos de paridad;
  3. saltos de gas;
  4. concentración de *builders* y *relays* en Ethereum;
  5. hackeos con flash loan en pools grandes.

## 5. Contrapuntos y límites

- **Errores que encontré:**
  - la pérdida impermanente redondeada ($23.41 contra $23.82 exactos);
  - "+500%" donde debía decir 5 veces el precio;
  - la errata en el factor de cETH;
  - el faltante del Jueves Negro con la estimación temprana (~$4 M) y no con lo que se recaudó después (~5.3 M DAI);
  - en la autoliquidación, el préstamo está en Compound pero el texto dice "*allowing the MakerDAO contract to liquidate*".
- **Sesgos:**
  - postura pro-DeFi y pro-Ethereum declarada;
  - dependencia económica de su audiencia (Patreon, referidos, consultorías);
  - muchas cifras vienen sin fuente, como la de 14 M DAI o el TVL.
- **Qué no está probado:**
  - que los hackeos hagan "antifrágil" al ecosistema;
  - que algún mecanismo con oráculo elimine la pérdida impermanente. Bancor lo intentó y lo suspendió.
- **Qué envejeció mal:**
  - el optimismo sobre Terra y Luna (mar-2022);
  - Bancor;
  - "*Ethereum 2.0*" como solución de comisiones.
- **Qué envejeció bien:**
  - la lección de Iron Finance: las stablecoins algorítmicas son difíciles y "*the numbers are not on your side*";
  - la advertencia sobre la centralización de los *builders* en MEV.

## 6. Autoexamen

1. **Con las reservas del ejemplo (20 ETH y 10,000 DAI a $500 → $550), ¿cuál es la pérdida exacta del LP y por qué Finematics publica $23.41?**
   - *Respuesta:* $23.82. HODL = 20 × 550 + 10,000 = $21,000. LP = 2√(200,000 × 550) = $20,976.18.
   - El artículo redondea el ETH del pool a 19.07, con lo que el LP valdría $20,976.59 y la pérdida $23.41.
   - *Fuente:* Finematics (21-ago-2020); cálculo en el apéndice A del capítulo.
2. **¿Qué pérdida impermanente corresponde a "+500%"? ¿Y a 5 veces el precio?**
   - *Respuesta:* +500% es r = 6: −30.0%. Cinco veces es r = 5 (+400%): −25.46%.
   - *Fuente:* fórmula de Angeris et al.; Finematics (21-ago-2020).
3. **En Iron Finance, ¿por qué un oráculo TWAP rezagado aceleró la espiral de muerte?**
   - *Respuesta:* al redimir IRON, el protocolo pagaba una parte en TITAN, calculada con el precio TWAP.
   - Como el TWAP estaba por encima del precio real, el redentor recibía TITAN que vendía de inmediato; eso hundía el precio, obligaba a acuñar más TITAN y volvía rentable redimir.
   - IRON cotizaba en $0.90 y se redimía por $0.75 en USDC más $0.25 en TITAN: el arbitraje empujaba a TITAN a 0.
   - *Fuente:* Finematics (24-jun-2021).
4. **¿Qué es la separación proponente-constructor (PBS) con MEV-Boost, y qué riesgo deja abierto según Finematics?**
   - *Respuesta:* el validador subcontrata la construcción del bloque a *builders* especializados, que compiten por pagarle más a través de *relays*.
   - Riesgo: la centralización. Cinco *builders* hacían ~90% de los bloques, a lo que se suman el flujo exclusivo de órdenes y el MEV entre cadenas.
   - *Fuente:* Finematics (27-oct-2023).

## 7. Grado de evidencia: **C**

- **Por qué C:**
  - es un divulgador con método visible;
  - la mecánica se puede verificar, y la verifiqué: x·y = k, la pérdida impermanente, cETH y el arbitraje con flash loan cuadran salvo redondeos y erratas;
  - pero no es fuente primaria, muchas cifras no traen fuente y tiene incentivos económicos ligados a su audiencia.
- **Grado D:** sus afirmaciones prospectivas ("*DeFi is the future*", "antifrágil").
- **Para qué sirve:** es la mejor puerta de entrada del grupo para la mecánica. Cada cifra se contrasta con el MOOC ([06](06-decentralized-finance-mooc.md)) o con una fuente primaria.
