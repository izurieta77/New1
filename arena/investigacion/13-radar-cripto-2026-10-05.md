# Radar cripto 2026-10-05 (Binance spot; puntaje §6.2 y niveles del pre-registro + adenda)

> Fase 0. Material para el comité del 9-oct. **No es recomendación de compra.** Niveles según la adenda del dueño (Diamante > +40% en 2-3 meses; Platino > +50% en 3-5; Oro +20% a +30% en 5-7), puertas P1-P6 y puntaje de `conocimiento/26-radar-de-oportunidades.md` §6.2. Etiquetas: [V] verificado hoy con fuente · [I] inferencia mía · [NV] no verificado (valor más bajo de la escala).
> Datos vivos: `data-api.binance.vision` (5-oct ~22:30 UTC), Coin Metrics community, Deribit, OKX, DefiLlama, Bitso API pública, iShares. Scripts en el scratchpad de la sesión (fuera del repo); backtest con dos implementaciones (Python puro y NumPy) que coinciden en retorno, caída máxima y número de cambios.

## 1. Veredicto

**No hay Diamantes, Platinos ni Oros hoy.** Los 8 candidatos quedan **sin nivel**. Puntaje máximo 34/100 (BTC y ETH), muy bajo el umbral de 55. Razones, en orden de peso:
1. **P1 (contraparte):** en spot de BTC/ETH/altcoins no hay un vendedor con restricción o sesgo identificable que sale de su posición en una fecha. Es prima de riesgo de mercado, no transferencia de riqueza.
2. **P4 (costos/edge):** el edge no está demostrado. La diferencia de retorno a 30 días en régimen encendido contra todos los días tiene IC 80% que incluye 0 en BTC, ETH, BNB, ADA, LINK y AVAX (§4). Con probabilidad recortada a la mitad (supervivencia y muestra dentro de periodo), el valor esperado neto es negativo en todos los objetivos de Diamante y Platino de BTC (-0.4% y -1.5%).
3. **Asimetría (adenda, mín. 2:1):** el stop del perfil (cierre diario < SMA200×0.97) está 17-33% abajo. Con ese stop **ningún objetivo Oro (+20/+30%) llega a 2:1** (mejor caso: BTC +30% = 1.57:1; XRP 1.70:1).
4. **P2 (evidencia):** BTC y ETH grado C como máximo (filtro de tendencia = protección, sin ventaja demostrada; tabla maestra: 0 ventajas demostradas de 26). Altcoins grado D (muestra con sesgo de supervivencia). Para dinero real se exige B: ninguno cumple.
5. **P3:** SOL tiene par MXN; XRP/MXN está en estado BREAK [V]; BNB, LINK, AVAX, ADA solo vía USDT (doble conversión MXN-USDT). Tope altcoin: 20% de la cuenta cripto = 1,000 MXN.

## 2. Liquidez y costos actuales (data-api.binance.vision, 24 h) [V]

| Par | Estado | Precio | Spread | Vol. 24 h | Profundidad ±0.5% (compra / venta) |
|---|---|---|---|---|---|
| BTC/MXN | TRADING | 1,548,963 | 0.052% | 2.18 M MXN | 33.8 k / 29.1 k MXN |
| BTC/USDT | TRADING | 85,759 | ~0.000% | 1,395 M USD | 10.7 M / 13.1 M USD |
| ETH/MXN | TRADING | 49,157 | **0.453%** | 0.087 M MXN | 35.6 k / 38.4 k MXN |
| ETH/USDT | TRADING | 2,711.95 | 0.0004% | 733 M USD | 6.4 M / 7.8 M USD |
| SOL/MXN | TRADING | 2,182 | 0.184% | 0.046 M MXN | 38.5 k / 32.1 k MXN |
| SOL/USDT | TRADING | 120.65 | 0.008% | 193 M USD | 3.3 M / 4.8 M USD |
| XRP/MXN | **BREAK** | n/a | n/a | n/a | n/a |
| XRP/USDT | TRADING | 1.5077 | 0.007% | 150 M USD | 1.5 M / 1.4 M USD |
| BNB/USDT | TRADING | 786.95 | 0.001% | 113 M USD | 2.0 M / 1.7 M USD |
| LINK/USDT | TRADING | 13.854 | 0.007% | 23 M USD | 0.34 M / 0.33 M USD |
| AVAX/USDT | TRADING | 11.098 | 0.009% | 35 M USD | 0.44 M / 0.37 M USD |
| ADA/USDT | TRADING | 0.2702 | 0.037% | 88 M USD | 0.42 M / 0.52 M USD |
| USDT/MXN (puente) | TRADING | 18.062 | 0.039% | 20.9 M MXN | 0.78 M / 3.6 M MXN |

- BNB, LINK, AVAX, ADA no tienen par MXN en Binance [V]. Los volúmenes MXN de ETH y SOL son minúsculos: operables con órdenes límite pequeñas, no con mercado.
- **Costo de ida y vuelta** [I, comisión 0.10% por lado de `parametros.json`; la tarifa real de la app no está verificada, la boleta real usó 0.075% estimado]: BTC/MXN 0.25%; ETH/MXN 0.65%; SOL/MXN 0.38%; vía USDT (4 patas + puente): BNB 0.44%, XRP 0.45%, LINK 0.45%, AVAX 0.45%, ADA 0.48%. No incluye SPEI de salida (~5 MXN) ni slippage.
- Que la app de Binance México muestre cada par **[NV]**: la API es global; solo se confirmó que el par existe y cotiza.
- Bitso (plan B), API pública [V]: libros MXN para BTC, ETH, SOL, XRP, LTC, TRX (no LINK, ADA, AVAX, BNB). Spreads BTC 0.068%, SOL 0.016%; comisión 0.60-0.78% por lado según `10-exchange-cripto-mexico.md` (1.2-1.6% ida y vuelta).

## 3. Posicionamiento del ciclo [V salvo nota]

| Variable | Dato | Fuente / fecha |
|---|---|---|
| Días desde el halving H4 (19-abr-2024) | **899** (pico típico del ciclo: 525-546 días; el pico fue el 6-oct-2025, 124,658) | cálculo propio; ficha 1-oct |
| Precio BTC / drawdown desde el máximo | 85.8 k; **-31%** (cierre 4-oct 86,530) | Binance klines |
| Precio realizado BTC / MVRV | **53,704** / **1.611** (4-oct); MVRV 1.575 el 2-oct | Coin Metrics (precio / MVRV) |
| ETH: MVRV / precio realizado | 1.157 / 2,357 (precio 2,728) | Coin Metrics, 4-oct |
| Otros MVRV | XRP 1.012, LINK 1.201, ADA 0.700, DOGE 0.814; SOL, BNB, AVAX sin dato | Coin Metrics |
| BTC vs SMA200 | SMA200 71,538.83; salida 69,392.66; reentrada 73,684.99; precio **+24.7% sobre la salida**; filtro ENCENDIDO | Binance 1d, 200 cierres; coincide con la bitácora |
| Volatilidad realizada BTC 30 / 90 d | 37.2% / 38.2% (condición de tramos 2-3: ≤ 45%, cumple); DVOL Deribit 36.1 | Binance, Deribit |
| Funding BTC | Deribit 7 d +3.2%/año, 30 d +3.95%/año; OKX ≈ 0 (-0.0000008 por 8 h); ETH OKX +6.7%/año; XRP OKX +9.8%/año; SOL OKX +2.0%/año | Deribit, OKX |
| Base de futuros Deribit (anualizada) | 5.6% (9-oct), 6.1% (16-oct); 5.17% a diciembre el 30-sep | Deribit |
| Interés abierto (solo 2 exchanges) | Deribit perp 820.8 M USD; OKX 2,445 M USD (28,521 BTC). **Total de mercado [NV]**: CoinGlass pide clave; fapi de Binance responde 451 | Deribit, OKX |
| Flujos ETF spot BTC | 1-oct +102.7 M (tftc; SoSoValue +103 M); 2-oct **+189.8 M (tftc) contra +627 M (resumen de búsqueda atribuido a SoSoValue)**: conflicto sin resolver; Farside 403 | tftc.io; prensa |
| Análogo de ciclo (día ~899) | Ventanas de 90 d desde el día 899 de H2 y H3: máximo +9.9% y +13.6%; ninguna llegó a +40% (n=2, grado D) | Binance klines |

Lectura [I]: ciclo avanzado, valuación media (MVRV 1.61, lejos de < 1 y del techo 2.29 de 2025), derivados sin apalancamiento eufórico (funding y base cerca del costo de acarreo). No hay señal de extremo en ninguna dirección. El único extremo con evidencia (MVRV < 1: 7 episodios, mediana +122.7% a 365 d, cap. 05) exigiría precio < ~53.7 k, es decir, con el filtro SMA apagado: hoy contradice la regla del perfil y requeriría excepción del comité.

## 4. Evidencia propia (backtest en muestra, Binance 1d; costo 0.2% por cambio; ejecución al cierre siguiente)

| Activo (inicio+200 d) | Filtro SMA200±3%: retorno / MDD / cambios | Comprar y mantener: retorno / MDD | Dif. fwd 30 d (encendido menos todos) [IC 80% bootstrap por bloques] |
|---|---|---|---|
| BTC (2018-03) | +918% / -52.6% / 27 | +656% / -76.6% | +1.82 pp [-0.11, +3.69] |
| ETH (2018-03) | +706% / -78.3% / 29 | +221% / -90.1% | +1.97 pp [-0.68, +4.54] |
| SOL (2021-02) | +3,132% / -67.5% / 25 | +822% / -96.3% | +5.67 pp [+1.03, +10.40] |
| XRP (2018-11) | -45% / -93.0% / 51 | +243% / -83.2% | -4.03 pp [-7.35, -0.44] |
| BNB (2018-05) | +1,716% / -78.5% / 57 | +6,013% / -76.1% | +1.97 pp [-0.71, +4.69] |
| LINK (2019-08) | +127% / -92.1% / 43 | +469% / -90.2% | 0.00 pp [-3.30, +3.21] |
| ADA (2018-11) | +1,490% / -80.5% / 27 | +262% / -95.2% | +2.65 pp [-1.18, +7.08] |
| AVAX (2021-04) | -28% / -75.6% / 33 | -65% / -95.6% | -1.99 pp [-7.44, +3.37] |

Límites: dentro de muestra; los activos son supervivientes de hoy (sesgo de supervivencia fuerte en altcoins; SOL "gana" porque sobrevivió); ventanas traslapadas; pocos ciclos. El filtro reduce caídas (replica R01/R06 de la tabla maestra: "solo protección") pero no prueba edge en BTC/ETH. Solo SOL tiene IC > 0, y es el caso con más sesgo de supervivencia: sin peso.

## 5. Tasas base de objetivos (ventanas diarias, entrada en régimen encendido, stop = cierre < SMA200×0.97 del día)

Pérdida en el stop con precio de hoy y SMA de los cierres hasta el 4-oct: BTC 19.1%, ETH 24.2%, SOL 30.9%, XRP 17.6%, BNB 21.3%, LINK 33.0%, AVAX 29.3%, ADA 23.5% (no incluye brecha).

"Prob. base" = fracción de entradas en régimen encendido que tocan el objetivo (cierre diario) antes del stop y del plazo. "Prob. honesta" = base × 0.5 [I: recorte por supervivencia, solapamiento y fase de ciclo]. EV neto = prob × objetivo + (1 - prob) × resultado medio de los casos no exitosos, menos costo ida y vuelta.

| Activo | Tier / objetivo / plazo | Precio objetivo | Asimetría (obj./pérdida stop) | Prob. base | Prob. honesta | EV neto base | EV neto honesto |
|---|---|---|---|---|---|---|---|
| BTC | Diamante +40% / 90 d | 120,081 | **2.09:1** | 26% | 13% | +5.6% | **-0.4%** |
| BTC | Platino +50% / 150 d | 128,658 | **2.62:1** | 30% | 15% | +7.6% | **-1.5%** |
| BTC | Oro +30% / 210 d | 111,504 | 1.57:1 (falla) | 40% | 20% | +2.5% | -6.6% |
| ETH | Diamante +40% / 90 d | 3,797 | 1.65:1 (falla) | 39% | 19% | +6.8% | -3.4% |
| ETH | Platino +50% / 150 d | 4,068 | 2.07:1 | 39% | 19% | +8.6% | -4.2% |
| SOL | Platino +50% / 150 d | 181.0 | 1.62:1 (falla) | 43% | 21% | +10.2% | -4.5% |
| XRP | Platino +50% / 150 d | 2.262 | 2.83:1 | 29% | 15% | **-1.5%** | -12.1% |
| BNB | Platino +50% / 150 d | 1,180 | 2.35:1 | 35% | 17% | +5.7% | -6.0% |
| LINK | Platino +50% / 150 d | 20.78 | 1.51:1 (falla) | 46% | 23% | +10.1% | -6.6% |
| AVAX | Platino +50% / 150 d | 16.65 | 1.71:1 (falla) | 32% | 16% | -3.1% | -15.6% |
| ADA | Platino +50% / 150 d | 0.4053 | 2.13:1 | 34% | 17% | -0.8% | -13.8% |

Ventanas "cualquier día" (sin filtro): BTC toca +40% en 90 d en 28.6% de 3,047 ventanas, +50% en 150 d 33.3%, +20% en 210 d 67.3%; ETH 40.5% / 45.4% / 72.8%; SOL 41.2% / 44.9% / 72.1%; XRP 37.2% / 40.4% / 70.7%; BNB 33.6% / 40.7% / 73.2%; LINK 41.9% / 46.7% / 77.9%; ADA 38.1% / 44.1% / 70.1%; AVAX 37.8% / 43.6% / 71.2%. Ventanas independientes efectivas: unas 8 a 34 por celda. Las tasas altas de LINK/SOL reflejan 2020-21 y supervivencia.

Hay EV positivo con la probabilidad base en BTC/ETH/SOL/LINK/BNB, pero esa cifra depende de 2020-21 y de que el pasado se repita; con el recorte pasa a negativo. No se infla ningún objetivo para entrar a un nivel.

## 6. Candidatos: puertas, contraparte, puntaje, nivel

Puertas: S = pasa, N = falla, P = parcial. Contraparte (P1): quién está del otro lado.

| | BTC | ETH | SOL | XRP | BNB | LINK | AVAX | ADA |
|---|---|---|---|---|---|---|---|---|
| P1 contraparte | N: vendedores marginales (tenedores que realizan ganancia, redenciones de ETF, mineros); sin restricción ni fecha | N: igual; stakers y redenciones de ETF | N: vendedores de un token con narrativa | N | N: además el emisor es el exchange (señal A1 de la lista) | N | N | N |
| P2 evidencia | P: C solo papel; real exige B | P: C solo papel | N: D | N: D | N: D | N: D | N: D | N: D |
| P3 ejecutable | S: BTC/MXN, tramo ≤ 65% de la cuenta | S: universo inicial; par MXN con spread 0.45% | P: requiere comité y tope 1,000 MXN; MXN con vol. 46 k/día | N: par MXN en BREAK; vía USDT con comité | P: solo USDT, comité | P: solo USDT, comité | P: solo USDT, comité | P: solo USDT, comité |
| P4 costos/edge | N: edge no demostrado (IC incluye 0; EV honesto negativo) | N | N | N (EV base negativo) | N | N | N | N |
| P5 salida | S: stop SMA200×0.97 = 69,393; tiempo 90/150 d; refutación abajo | S: 2,056 (propuesto, el filtro oficial es solo de BTC) [I] | S: 83.4 [I] | S: 1.242 [I] | S: 619 [I] | S: 9.28 [I] | S: 7.84 [I] | S: 0.207 [I] |
| P6 legalidad | S | S | S | S | S | S | S | S |

**Puntaje §6.2** (se llena como si las puertas se cumplieran, solo para ordenar; el nivel manda la puerta):

| Componente (máx.) | BTC | ETH | SOL | XRP | BNB | LINK | AVAX | ADA |
|---|---|---|---|---|---|---|---|---|
| Edge/costo (25): EV neto honesto ≤ 0 = 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Evidencia (15): C = 5, D = 0 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| Catalizador con fecha (10): sin fecha verificada = 2 [NV; el fork de Glamsterdam en mainnet no tiene fecha verificada] | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| Asimetría (15): mejor de 40%/50% | 10 (2.62) | 10 (2.07) | 6 (1.62) | 10 (2.83) | 10 (2.35) | 6 (1.51) | 6 (1.71) | 10 (2.13) |
| Liquidez (5): spread ≤ 0.10% y profundidad ≥ 1 M USD = 5; si no 3 | 5 | 5 | 5 | 5 | 5 | 3 | 3 | 3 |
| Costos (5): ≤ 0.7% = 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| Correlación (10): ρ 60 d con BTC (USDT) | 0 (1.00) | 0 (0.88) | 0 (0.82) | 0 (0.88) | 2 (0.69) | 2 (0.63) | 6 (0.48) | 0 (0.81) |
| Riesgo regulatorio/geopolítico (10) | 5 | 5 | 0 [NV] | 0 [NV] | 0 (token del exchange con investigación del DOJ) | 0 [NV] | 0 [NV] | 0 [NV] |
| Ventaja propia (5): solo A = 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| Crowding (-10 a 0) [I] | 0 | 0 | 0 | 0 | 0 | 0 | -5 (+50% en 30 d, vol. 105%) | 0 |
| **Total** | **34** | **34** | **18** | **22** | **24** | **18** | **17** | **20** |
| **Nivel** | **Sin nivel** | **Sin nivel** | Sin nivel | Sin nivel | Sin nivel | Sin nivel | Sin nivel | Sin nivel |

## 7. Alertas por candidato (propuestas [I]; el comité las ratifica o cambia)

**BTC** (precio 85,772; real 0.001325 BTC = 2,052 MXN, 41% de la cuenta; papel 0.002698 BTC = 4,179 MXN, 41%)
- Entrada que lo subiría de nivel: (a) cierre diario > 91,642 (50% de retroceso de 58,625-124,659; 13 de 17 episodios lo recuperaron) con ETF 5 días acumulado > +1,000 M USD y funding Deribit 7 d < +15%/año; con esos tres, se registra pronóstico y se reevalúa Diamante (+40% = 120,081); (b) MVRV < 1 (< ~53.7 k) con excepción del comité, porque contradice el filtro.
- Salida: cierre diario < 69,393 (SMA200×0.97; recalcular a diario) = vender el 100% al día siguiente; reentrada > 73,685. Tiempo: 90 d sin tocar 120 k, revisar tesis. Refutan: ETF 5 días acumulado < -1,500 M USD; funding 7 d > +25%/año; MVRV > 2.29; cualquier ROJA de Binance.
- Tamaño máximo del perfil: exposición hasta 65% = 3,250 MXN; ya hay 2,052, margen 1,198 MXN; tramos 2 (750) y 3 (500) no antes del 30-oct y 5-nov, con las 4 condiciones (la 4.ª, ir 5 pp detrás del rival, sin dato). Por riesgo: 10% de 5,000 = 500 MXN / 19.1% = 2,618 MXN a 100%; 1,309 a 50%.
- Encaje: es lo que ya se tiene; añadir BTC sube la concentración, no la diversifica (ρ = 1).

**ETH** (2,712): entrada: cierre > 2,900 con ETH/BTC subiendo y flujos de ETF de ether 5 días > +300 M USD [I]; salida: cierre < 2,056 [I]; refutan: ETH/MXN con spread > 1% o par suspendido. Tamaño: dentro del tope total 65% (margen 1,198 MXN junto con BTC). Mayor beta, peor tasa base de reversión que BTC (90 d: 53.3% contra 76.5%; ficha 27-sep).

**SOL**: entrada: tendría que mostrar edge fuera de muestra y producto regulado (ETF spot en EUA [NV]); salida: cierre < 83.4; tope 1,000 MXN (20%); MXN/SOL con volumen 46 k MXN/día, solo límite.
**XRP**: par MXN en BREAK; salida: cierre < 1.242; tope 1,000 MXN; funding OKX el más alto (9.8%/año).
**BNB**: descartar por diseño: es el token del exchange y la contraparte (A1/E2: 15.4% de lo rastreado en Binance; la alerta ÁMBAR de E2 es > 20%). Salida: cierre < 619 o BNB > 20% de lo rastreado.
**LINK, AVAX, ADA**: sin par MXN, correlaciones y asimetrías insuficientes; salida: LINK < 9.28, AVAX < 7.84, ADA < 0.207. Tope 1,000 MXN cada una, solo con comité.

## 8. (a) ETF spot de Ether en EUA y la decisión de "dejar en spot"

- Flujos: 1-oct **+80.8 M USD** (SoSoValue vía MEXC; ETHA +26.2 M, FETH +36.8 M; ETHA acumulado 13,466 M) [una fuente de prensa]; julio +452.7 M; categoría ~17.8 mil M USD a fines de septiembre [prensa, no verificado en primaria]. Farside da 403.
- ETHA (iShares): comisión **0.25%**, activos 9,795 M USD al 2-oct, **sin staking** [V, página de iShares].
- Staking permitido: SEC/CFTC emitieron el 17-mar-2026 una interpretación conjunta de que las recompensas no son valores [prensa secundaria]. ETHB de BlackRock (lanzado 12-mar-2026): comisión 0.25%, **0.12% el primer año** sobre los primeros 2.5 mil M; stakea 70-95% y pasa 82% de recompensas cada mes [resumen de búsqueda de la página de BlackRock]; ETHE de Grayscale con staking desde oct-2025. Rendimiento bruto 3.1-3.3%, neto 1.9-2.6% [prensa].
- Implicación para "dejar en spot": en Binance spot el ETH **no rinde** (el perfil prohíbe staking con bloqueo y Earn a plazo). Un ETF con staking rinde ~2% neto pero cuesta 0.25% anual + comisión de GBM 0.25%+IVA por lado + tipo de cambio, y no se compra en Binance; si está en el SIC de GBM es **[NV]** (en `10-exchange-cripto-mexico.md`, IBIT no estaba en el SIC). Para BTC/ETH la diferencia de costo (0.2-0.65% vía Binance contra ~0.7%+ vía GBM) y de contraparte (ETF quita el riesgo Binance y suma DriveWealth/EUA) no justifica mover nada hoy. Decisión sugerida para el comité: **dejar en spot**; el ETF solo si Binance pasa a ROJA.

## 9. (c) Contraparte Binance (E1-E10) y plan B Bitso, 5-oct

| Señal | Estado hoy | Nota |
|---|---|---|
| E1 flujo semanal | LIMPIA [indicio] | TVL DefiLlama `binance-cex` **179.87 mil M USD** (rango 177.5-179.8 del 25-sep al 5-oct); BTC 54.80 mil M ≈ 638,900 BTC; método ex-BNB exacto pendiente |
| E2 composición | LIMPIA [NV exacta] | BNB sin recalcular hoy (15.4% el 25-sep; umbral ámbar 20%) |
| E3 PoR | LIMPIA | 47.º reporte no aparece; ventana 15-21 oct; el 46.º (1-sep) sigue vigente |
| E4 SAFU | LIMPIA | 15,000 BTC ≈ 1.29 mil M USD; umbral ámbar BTC < 53,333 |
| E5 acciones penales | **ÁMBAR** | investigación del DOJ por Irán sin cargos; decomiso civil US$61 M (14-sep) |
| E6 retiros/SPEI | LIMPIA [sin prueba propia hoy] | sin pausas reportadas |
| E7 incidentes | LIMPIA | ninguno en Binance |
| E8 stablecoins | LIMPIA | USDC/USDT 1.00003; FDUSD 0.9988 (-0.12%) |
| E9 liquidez BTC/MXN | LIMPIA | spread 0.052%; profundidad 33.8 k / 29.1 k MXN (umbral ámbar 0.5%) |
| E10 contagio | vigilar | Bitget (hackeo 24-sep, retiros suspendidos), AscendEX y BitMart |
| A9 licencia | **ÁMBAR** | sin supervisión en México; UE solo retiros desde el 1-jul |

Sin ROJA ni disparador de contingencia. Plan B Bitso: sin cambio (rutas y disparadores en `parametros.json` → `contingencia_contraparte`); su libro MXN existe para BTC, ETH, SOL, XRP; para LINK, AVAX, ADA, BNB no hay salida en pesos directa en Bitso, otra razón para no agregar altcoins con comisión 0.6-0.78% por lado. Riesgo de contraparte: ÁMBAR por dos señales (regla: votar con el gestor de riesgo, que tiene veto).

## 10. Lectura en 15 líneas

1. No hay Diamantes, Platinos ni Oros hoy; los 8 candidatos quedan sin nivel; el mejor puntaje es 34 (BTC y ETH).
2. BTC es el único candidato cuyo objetivo Diamante (+40% = 120,081) pasa 2:1 (2.09) y casi toca el máximo de 124,659; pero la prob. honesta es ~13% y el EV neto honesto -0.4%.
3. Platino BTC (+50% = 128,658, exige nuevo máximo histórico en 5 meses): 2.62:1, prob. ~15%, EV neto -1.5%.
4. Ningún Oro cumple 2:1 con el stop del perfil, que está 17-33% abajo; achicar el stop contradice la regla de tendencia (los stops intradía fallan por ruido).
5. Las tasas base altas (BTC +20% en 210 d: 67%) son tocar el nivel una vez, no ganar dinero con el stop activo (EV bruto ≈ 0).
6. Ciclo: día 899 posterior al halving, pico ya pasado; MVRV 1.61, funding y base sin euforia; sin extremo accionable.
7. Los análogos de ciclo al día 899 (2018, 2022) dieron +10% y +14% máximo en 90 d: ninguno fue Diamante (n=2, grado D).
8. Altcoins: grado D, sesgo de supervivencia, correlación 0.48-0.88 con BTC, sin par MXN (salvo SOL; XRP en BREAK); no aportan diversificación ni edge.
9. BNB es la peor idea: token del propio exchange que ya está en ÁMBAR.
10. ETF de ether: flujos positivos pequeños, ETHA sin staking (0.25%), ETHB con staking neto ~2%; no cambia dejar en spot; no está verificado que existan en el SIC.
11. Binance: sin ROJA; dos ÁMBAR (E5, A9); la PoR 47.º (15-21 oct) es el siguiente dato a mirar.
12. Con 5,000 MXN el costo importa: BTC/MXN 0.25%, ETH/MXN 0.65%, altcoins vía USDT ~0.45%, Bitso 1.2-1.6%.
13. Lo ya tenido (BTC 41% real y papel) está dentro del perfil; el margen hasta 65% es 1,198 MXN, sin presión de comprar.
14. Si el comité del 9-oct sube a Platino/Diamante, debe hacerlo por una tesis con contraparte, no por beta de precio.
15. Hechos que cambiarían esta lectura: cierre BTC > 91,642 con flujos de ETF fuertes y funding bajo; MVRV < 1 con excepción de filtro; cualquier ROJA de Binance.

## 11. Bloqueos y límites

- Farside, SoSoValue y CoinGlass inaccesibles; flujos de ETF solo por prensa/agregador; el 2-oct de BTC tiene dos cifras en conflicto (189.8 M contra 627 M).
- Interés abierto total y funding de Binance no disponibles (451 en fapi); solo Deribit y OKX.
- Tarifa real de la app, existencia de cada par en la app de México y ETF de ether en el SIC: [NV].
- Correlaciones calculadas en USDT, no en MXN; la cartera completa incluye el libro GBM aún sin fondear.
- Backtest dentro de muestra con sesgo de supervivencia; el recorte de 0.5 a las probabilidades es mío [I].
