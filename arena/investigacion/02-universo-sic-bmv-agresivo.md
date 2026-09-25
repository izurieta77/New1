# Universo agresivo SIC/BMV vía GBM para la cuenta arena

**Fecha:** 2026-09-25 · **Tarea:** A2 · **Cuenta:** `arena-claude` (20,000 MXN, perfil `arena_agresivo` PROVISIONAL)
**Alcance:** qué instrumentos agresivos puede comprar una persona física en México a través de GBM, en el SIC y en la BMV. Incluye ETFs apalancados, cripto, sectoriales, commodities, México, bonos, acciones de EUA y ADRs. Cubre disponibilidad, restricciones de perfil, liquidez local, formación del precio en MXN y riesgos específicos.

**Convenciones**
- **[H]** Hecho con fuente y fecha.
- **[C]** Cálculo propio sobre datos con fuente. El método está explicado.
- **[I]** Inferencia.
- **[R]** Recomendación para la cuenta arena.
- Salvo otra indicación, los datos de mercado son del **cierre del 24-sep-2026**, tomados de StockAnalysis (datos de S&P Global) [30].
- "Liquidez 30d" = mediana del importe diario operado en BMV (precio × volumen) del 25-ago al 24-sep-2026, 22 sesiones [C][30].
- Los costos de operación (0.25% + IVA por lado, sin fracciones en el SIC, horarios, W-8BEN) están en `01-gbm-operativa-y-costos.md`. Aquí solo se citan.

---

## Resumen ejecutivo

1. **[H] Los ETFs apalancados 3x más usados sí están listados y activos en el SIC de la BMV:** SOXL (estatus "ACTIVA" en BMV [2]), TQQQ (aviso de split de la BMV, serie `*` [3]), SPXL, TECL, QLD, SPUU, TNA, FAS, LABU, NUGT, YINN, TSLL y los inversos SOXS y SQQQ. Todos operaron en la BMV en sep-2026 [30][31].
2. **[H] No encontré ninguna regla de la CNBV o la BMV que impida a una persona física no calificada comprarlos por ejecución de operaciones.** El SIC está abierto a "cualquier tipo de inversionista" desde 2014 [1]. La restricción del Anexo 6 aplica a lo que el intermediario *comercializa o promueve*, no a lo que el cliente instruye [10]. En la app, GBM presta "Ejecución de Operaciones" y el cliente firma una carta donde asume la responsabilidad [11]. Si la app bloquea algo o muestra advertencias por perfil: **no verificado**.
3. **[H] Los ETFs spot de bitcoin (IBIT, FBTC, etc.) GBM los ofrece por Trading Global/USA (DriveWealth, en USD) desde ene-2024, no por el SIC** [14][15][16]. No encontré evidencia de que estén listados en el SIC (**no verificado**). Dentro del SIC, la exposición cripto disponible es indirecta: MSTR y COIN [30].
4. **[C] La liquidez local se concentra en muy pocos apalancados.** SOXL mueve ~87.5 M MXN/día (mediana) y SOXS ~26 M. SPXL ~7 M y TQQQ ~4.7 M. QLD, SPUU, DDM, EWW y KWEB operan ≤0.4 M MXN/día o no operan todos los días [30].
5. **[C] El precio en MXN sigue al de EUA × tipo de cambio.** En los líquidos, la desviación mediana contra el valor justo es de 0.07% a 0.2%. En los poco operados la mediana sube a 0.4%–1.0%, con máximos de 3% a 9% [30].
6. **[C] El decaimiento por volatilidad es el riesgo dominante.** A 6 meses, con el índice plano, un 3x pierde ~3.3% si el subyacente tiene 15% de volatilidad, ~8.9% con 25% y ~36.5% con 55%. Con la volatilidad de 2026, SOXX (55%) está en el peor rango. En los 6 meses a sep-2026, SOXL tuvo un **drawdown máximo de −69.4%** (SOXX: −29%). En julio de 2026 cayó **−57%** en un mes [30].
7. **[H] Riesgo de cierre o cambio del instrumento:** Direxion cerró 10 ETFs en abr-2026 [27]. BMO redimió el ETN FNGU en 2025 [26]. DriveWealth se reserva el derecho de retirar apalancados de su plataforma sin aviso [22].
8. **[R]** Para `arena-claude`: la base agresiva líquida está en **TQQQ/SPXL** (menos decaimiento por punto de apalancamiento). **SOXL** queda como la palanca de máxima varianza, con un tope menor. Siempre con órdenes limitadas contra el valor justo. Evitar los apalancados con liquidez muy baja (QLD, SPUU, DDM) y no depender de UPRO, SSO ni ARKK: su disponibilidad no está verificada.

---

## 1. Dos vías dentro de GBM

| Aspecto | Trading MX (BMV/BIVA + SIC) | Trading USA / Global (DriveWealth) | Fuente |
|---|---|---|---|
| Moneda | MXN | USD | [13][17] |
| Custodia | Mexicana, vía Indeval | DriveWealth (bróker de EUA) | [11][17][18] |
| Fracciones | **No** (en el SIC solo títulos completos) | Sí | [19][20] |
| ETFs de bitcoin spot | No verificado (sin evidencia de listado) | **Sí** (11 ETFs desde el 12-ene-2024) | [14][15] |
| ETFs apalancados | **Sí** (SOXL, TQQQ, SPXL…) | Presumiblemente sí, pero DriveWealth puede retirarlos sin aviso | [2][3][22] |
| Fiscal (persona física) | 10% definitivo sobre la ganancia (art. 129 LISR) en el SIC | Tratamiento distinto, sin constancia mexicana | [18][33] |

- [I] La métrica de la competencia es TWR en MXN. Una posición en Trading USA también se valúa en MXN al convertirse, así que en ambas vías la cuenta queda larga en USD. La diferencia real está en la fricción (conversión cambiaria, tipos de orden) y en qué instrumentos hay en cada vía.
- [R] Operar por **Trading MX (SIC)**. Trading USA solo se justifica para lo que no esté en el SIC (ETFs de bitcoin spot) y con conversión cambiaria agrupada (ver `01`).

---

## 2. Marco regulatorio: ¿quién puede comprar qué?

### 2.1 Hechos

- **[H] El SIC está abierto a cualquier inversionista.** La BMV dice: "Desde enero de 2014, cualquier tipo de inversionista puede participar en el SIC" [1].
- **[H] La restricción por perfil de la CNBV aplica a la comercialización, no a la ejecución.** La reforma a las Disposiciones de servicios de inversión (DOF 09-feb-2016), en su Anexo 6, dice: "Las Entidades financieras únicamente podrán Comercializar o promover a clientes que no sean considerados como Clientes sofisticados, los Valores siguientes:" [10]. En el mismo anexo aparecen los "Valores emitidos en el extranjero reconocidos por la Comisión en términos de las Disposiciones de carácter general aplicables al Sistema Internacional de Cotizaciones" [10].
- **[H] La app de GBM es ejecución de operaciones.** La Guía de Servicios de GBM (versión V0424, PDF del 14-nov-2024) clasifica el servicio que presta "a través de las plataformas electrónicas de operación en línea nombrada GBM y GBM+" como **Ejecución de Operaciones**. En ese servicio, "el cliente toma sus decisiones de inversión, sin asesoría ni intervención por parte de la Casa de Bolsa". El cliente debe "asumir completa y exclusiva […] responsabilidad sobre sus decisiones de inversión […] y manifestarlo así a la Casa de Bolsa mediante la carta correspondiente" [11].
- **[H] GBM perfila al cliente**, pero para sus servicios asesorados y discrecionales. Hay tres niveles de conocimiento (Básico, Medio y Alto). Los perfiles de cuenta van de "Liquidez/Muy conservador" a "Bolsa/Muy agresivo" [11]. La guía no liga el perfil a la ejecución de operaciones en la app [11].
- **[H] Los apalancados están listados y activos.** La ficha de la BMV de SOXL dice: "DIREXION DAILY SEMICONDUCTOR BULL 3X ETF", tipo "CANASTAS DE ACCIONES (TRAC´S EXTRANJEROS)", ISIN US25459W4583, estatus "ACTIVA" [2]. La BMV también publica avisos de derechos para apalancados e inversos de ProShares en el SIC: TQQQ, REW y SMN, todos con serie `*` [3][4][5].
- **[H] DriveWealth** (la vía Trading USA) describe los apalancados e inversos como "complex investments that come with a unique set of risks". Se reserva el derecho de "remove leveraged or inverse ETFs from the platform" [22].

### 2.2 Inferencias y huecos

- [I] Con [1], [2], [10] y [11], la barrera para comprar un apalancado del SIC en la app de GBM no es regulatoria. Si existe, es una política interna de GBM (una advertencia o un bloqueo por perfil), y **no está verificada**.
- **No verificado:** el texto vigente de las *Disposiciones de carácter general aplicables a los sistemas internacionales de cotizaciones* de la CNBV. El sitio cnbv.gob.mx respondió 503 y tuvo errores de TLS durante esta investigación. No pude confirmar si hay artículos sobre ETFs apalancados o inversos ni el procedimiento exacto de cancelación del listado.
- [I] Que no haya ETFs de bitcoin spot en el SIC es coherente con el régimen de Banxico. La Circular 4/2019 limita a bancos e ITFs en operaciones con activos virtuales [34]. No encontré una resolución que prohíba expresamente listar esos ETFs en el SIC, así que la causa es inferida.

---

## 3. Nomenclatura: cómo reconocer un valor del SIC

| Serie | Qué indica | Ejemplos con fuente BMV |
|---|---|---|
| `*` | Serie única, típica de emisoras y ETFs de EUA en el SIC | `TQQQ *` [3], `SOXL *` [2], `REW *` [4], `SMN *` [5], `BERY *` [6] |
| `N` | Emisoras extranjeras no estadounidenses en el SIC | `SONY N`, `PHIA N` (Philips), `WPM N` (Wheaton), `SW1 N` (Smurfit Westrock) [6] |

- [H] La BMV identifica cada valor con "CLAVE DE COTIZACIÓN" + "SERIE" + ISIN + "MERCADO PRINCIPAL" (NASDAQ, NYSE, etc.) [3][6].
- [I] En la app, un valor del SIC aparece en Trading MX con su clave y la serie `*` o `N`, y cotiza en MXN. Que la app muestre exactamente así la serie: **no verificado** (no encontré documentación de GBM sobre la nomenclatura).
- [H] **Los agregadores no están completos.** StockAnalysis y TradingView no tienen páginas BMV de OXY [30][31], pero la BMV reportó a Occidental Petroleum entre los valores del SIC más operados de 2021 [8]. Que un ticker no aparezca en un agregador **no prueba** que no esté listado.
- [R] Protocolo de verificación en la app, antes de cada instrumento nuevo:
  1. Buscar la clave en Trading MX.
  2. Confirmar que cotice en MXN, con serie `*` o `N` y con posturas de compra y venta visibles.
  3. Si no aparece, anotar "no disponible en SIC vía GBM" en la bitácora con la fecha.
  4. Revisar si la app pide alguna aceptación de riesgo al comprar un apalancado.

---

## 4. ETFs apalancados e inversos

Método de la desviación contra el valor justo [C]. Para cada día con operación en BMV desde el 24-jun-2026 se calculó |(cierre BMV / cierre EUA) / TC implícito − 1|. El TC implícito es el promedio de SPY e IVV (BMV/EUA) del mismo día. Es una aproximación al spread más el desfase intradía, no el spread cotizado. Precios de EUA: [30].

| Instrumento | Subyacente / apalancamiento | ¿Operó en BMV? (fuente) | Precio BMV (MXN) | 1 título = % de 20k | Liquidez 30d (mediana MXN/día; días con operación) | Desviación contra el valor justo, mediana / máx. |
|---|---|---|---|---|---|---|
| **SOXL** | Semiconductores (NYSE Semiconductor) 3x | Sí, estatus ACTIVA [2][30] | 2,593.45 | 13.0% | **87.5 M** (21/22) | 0.39% / 2.9% |
| **SOXS** | Semiconductores −3x | Sí [30] | 595.40 | 3.0% | 26.4 M (22/22) | 0.48% / 3.3% |
| **SPXL** | S&P 500 3x | Sí [30][31] | 5,090 | 25.4% | 7.0 M (21/22) | 0.17% / 2.1% |
| **TQQQ** | Nasdaq-100 3x | Sí, aviso BMV serie `*` [3][30] | 1,392.75 | 7.0% | 4.7 M (22/22) | 0.17% / 1.0% |
| NUGT | Mineras de oro 2x | Sí [30] | 2,980 | 14.9% | 2.5 M (20/22) | 0.56% / 4.9% |
| SQQQ | Nasdaq-100 −3x | Sí [30] | 605.05 | 3.0% | 1.6 M (21/22) | 0.43% / 3.8% |
| TECL | Tecnología (Select Sector) 3x | Sí [30] | 3,942 | 19.7% | 1.0 M (20/22) | 0.45% / 3.8% |
| FAS | Financieras 3x | Sí [30] | 2,660 | 13.3% | 0.85 M (18/22) | 0.29% / 2.3% |
| YINN | China FTSE 3x | Sí [30] | 453.17 | 2.3% | 0.59 M (20/22) | 0.31% / 3.8% |
| LABU | Biotecnología 3x | Sí [30] | 4,590 | 23.0% | 0.47 M (18/22) | 1.00% / 5.2% |
| TSLL | Tesla 2x (acción única) | Sí [30] | 183.20 | 0.9% | 0.27 M (21/22) | 0.56% / 2.6% |
| TNA | Russell 2000 3x | Sí [30] | 1,066 | 5.3% | 0.23 M (17/22) | 0.74% / 6.1% |
| TMF | Treasuries 20+ años 3x | Sí [30] | 486.16 | 2.4% | 0.22 M (18/22) | 0.29% / 1.4% |
| SPUU | S&P 500 2x | Sí, pero poco operado [30] | 3,983 | 19.9% | 0.36 M (**11/22**) | 0.21% / 1.3% |
| QLD | Nasdaq-100 2x | Sí, pero poco operado [30] | 1,673.59 | 8.4% | 0.08 M (**12/22**) | 0.41% / 3.7% |
| DDM | Dow 30 2x | Casi sin operación [30] | 1,070 | 5.4% | 0.04 M (**4/22**) | n.d. |
| UPRO | S&P 500 3x | **No verificado**: sin página BMV en [30][31] | — | — | — | — |
| SSO | S&P 500 2x | **No verificado** (mismo caso) | — | — | — | — |
| FNGU | FANG+ 3x (ETN de BMO) | **No verificado**. El ETN original se redimió en may-2025 [26] | — | — | — | — |
| NVDL / NVDU | NVIDIA 2x | **No verificado**: sin página BMV en [30] | — | — | — | — |
| DFEN | Defensa aeroespacial 3x | Sí, según prensa (+97.49% en MXN a 12 meses, may-2026) [28] | n.d. | — | n.d. | — |

**Rendimiento y drawdown reales, 24-mar a 24-sep-2026 (en USD, cierres ajustados) [C][30]**

| Par | Volatilidad anualizada del subyacente | Rendimiento del subyacente | L × subyacente (lo "esperado") | Rendimiento real del apalancado | Drawdown máximo del apalancado | Drawdown máximo del subyacente |
|---|---|---|---|---|---|---|
| TQQQ / QQQ | 22.3% | +27.2% | +81.5% | **+81.2%** | **−33.6%** | −11.2% |
| QLD / QQQ | 22.3% | +27.2% | +54.4% | +53.6% | −22.8% | −11.2% |
| SPXL / SPY | 13.5% | +18.0% | +54.1% | +52.7% | −13.3% | −4.5% |
| SSO / SPY | 13.5% | +18.0% | +36.1% | +34.4% | −9.0% | −4.5% |
| TECL / XLK | 30.1% | +43.3% | +130.0% | +144.1% | −45.0% | −15.9% |
| **SOXL / SOXX** | **55.1%** | +66.2% | +198.5% | **+166.4%** | **−69.4%** | −29.0% |
| SOXL / SOXX, solo del 30-jun al 31-jul-2026 | 61.9% | −21.2% | −63.6% | **−57.0%** | −65.5% | −27.4% |

- [H] SOXL: +838.49% en pesos en los 12 meses a finales de abr-2026 (Morningstar, vía El Cronista, 26-may-2026) [28]. Su rango de 52 semanas en BMV va de 520.01 a 5,238 MXN [30].
- [I] SOXL ofrece la mayor convexidad al alza del universo SIC y el mayor riesgo de ruina parcial. En 6 meses, un subyacente +66% dejó a SOXL en 2.5x y no en 3x, con un −69% intermedio.

---

## 5. Sectoriales, temáticos, commodities, México y bonos

| Instrumento | Tipo | ¿Operó en BMV? | Precio BMV (MXN) | 1 título = % de 20k | Liquidez 30d (mediana MXN/día; días) | Desviación, mediana / máx. |
|---|---|---|---|---|---|---|
| SMH | Semiconductores 1x | Sí [30] | 10,580 | **52.9%** | 2.4 M (21/22) | 0.18% / 1.2% |
| SOXX | Semiconductores 1x | Sí [30] | 9,875 | **49.4%** | 5.7 M (22/22) | 0.31% / 2.1% |
| XLK | Tecnología EUA | Sí [30] | 3,449.99 | 17.2% | 2.1 M (22/22) | 0.25% / 2.8% |
| IGV | Software | Sí [30] | 1,944.99 | 9.7% | 1.6 M (21/22) | 0.22% / 5.5% |
| URA | Uranio | Sí [30] | 725 | 3.6% | 0.31 M (20/22) | 0.32% / 1.7% |
| COPX | Mineras de cobre | Sí [30] | 1,549.39 | 7.7% | 0.91 M (20/22) | 0.44% / **9.5%** |
| GDX | Mineras de oro | Sí [30] | 1,635 | 8.2% | 0.59 M (21/22) | 0.28% / 3.1% |
| XLE | Energía | Sí [30] | 1,110 | 5.5% | 1.2 M (21/22) | 0.20% / 1.1% |
| KWEB | Internet China | Sí, poco operado [30] | 435.40 | 2.2% | 0.09 M (19/22) | 0.23% / 1.3% |
| ARKK | Innovación (activo) | **No verificado**: sin página BMV en [30][31] | — | — | — | — |
| GLD | Oro | Sí [30] | 6,950 | 34.8% | 6.9 M (21/22) | 0.10% / 1.6% |
| IAU | Oro (unidad barata) | Sí [30] | 1,423.63 | 7.1% | 5.0 M (22/22) | 0.12% / 0.5% |
| SLV | Plata | Sí [30] | 1,021 | 5.1% | 3.4 M (22/22) | 0.19% / 0.8% |
| NAFTRAC | IPC México (ETF local) | Sí, BMV local [30] | 63.97 | 0.3% | **114 M** (22/22) | n.a. (local) |
| EWW | MSCI México (en USD) | Sí, poco operado [30] | 1,270 | 6.3% | 0.16 M (**11/22**) | 0.59% / 5.6% |
| TLT | Treasuries 20+ años | Sí [30] | 1,419.99 | 7.1% | 2.2 M (22/22) | 0.11% / 0.7% |
| REMX, RARE | Tierras raras / materiales críticos | Sí, según prensa (+151% y +126% a 12 meses, may-2026) [28] | n.d. | — | n.d. | — |

Referencias de índice amplio (para medir el costo de oportunidad): SPY 26.1 M, IVV **92.0 M**, VOO 31.5 M, QQQ 24.1 M, QQQM 2.9 M y SPLG 2.2 M MXN/día de mediana. Sus desviaciones medianas van de 0.07% a 0.12% [C][30].

- [H] Según la prensa, en 2026 los ETFs son ~36% del volumen operado en México (Cumbre BMV–S&P DJI, 11-may-2026) [29].
- [H] Fiscal: los ETFs de bonos y commodities (TLT, GLD, SLV) "no encajan con claridad" en el art. 129 de la LISR, según Rankia (11-jun-2026) [33]. [I] Esto no afecta el TWR de la competencia, pero sí el resultado después de impuestos del dueño.

---

## 6. Cripto

| Instrumento | Vía en GBM | Estado | Fuente |
|---|---|---|---|
| IBIT, FBTC, GBTC, ARKB, BITB, HODL, EZBC, BTCO, BTCW, BRRR, DEFI (bitcoin spot) | **Trading Global/USA (USD, DriveWealth)** | Disponibles desde el 12-ene-2024 | [14][15][16] |
| ETFs de Ethereum | Trading USA (la página de GBM menciona "ETFs de Bitcoin y Ethereum") | Tickers no verificados | [13] |
| IBIT, FBTC y demás en el SIC | — | **No verificado**. Sin página BMV en [30][31] y GBM los canaliza por Trading Global | [14][30][31] |
| MSTR (Strategy) | SIC | Sí. 2,879.93 MXN; liquidez 30d 8.6 M MXN/día | [30] |
| COIN (Coinbase) | SIC | Sí. 3,499.99 MXN; liquidez 30d 2.0 M MXN/día | [30] |
| BITO, BITX, BITU, ETHU (futuros o apalancados cripto) | — | No verificado: sin página BMV en [30] | [30] |

- [I] MSTR es un proxy apalancado de BTC con riesgo de emisora. COIN depende del volumen cripto. Ninguno replica BTC 1:1.
- [R] Si la estrategia pide BTC puro, usar IBIT por Trading USA, con una sola conversión MXN→USD por temporada (costos en `01`). Dentro del SIC, MSTR es la alternativa líquida.

---

## 7. Acciones individuales de EUA y ADRs en el SIC

- [H] En ene-2022 el SIC tenía 3,000 valores: 55% acciones y 45% ETFs, 57% de emisores norteamericanos, 37% europeos, y más de 73,000 millones de USD en custodia. El SIC pasó de 30% a 53% del volumen negociado en la BMV entre 2016 y 2021 [8].
- [C] Cobertura mínima con los datos de StockAnalysis: su lista de la BMV tiene 927 acciones. **Al menos 395 de las 503 del S&P 500 (79%) y 84 de las 101 del Nasdaq-100 (83%)** tienen cotización BMV ahí [30]. Es una **cota inferior**: el agregador omite valores que sí están en el SIC, como OXY [8] y probablemente las series `N` (ADRs y emisoras no estadounidenses).
- [H] Hay emisoras extranjeras no estadounidenses con serie `N`: Sony, Philips, Wheaton y Smurfit Westrock [6]. TSM, BABA, MELI, ASML, NU y ARM no tienen página BMV en StockAnalysis ni en TradingView, así que su disponibilidad **no está verificada**.
- Liquidez de acciones de alto beta en BMV (liquidez 30d) [30]: NVDA 106 M, AAPL ~40 M (un día), TSLA ~11 M (un día), PLTR ~9.6 M (un día), MSTR 8.6 M, SMCI ~4 M (un día) y COIN 2.0 M MXN/día.
- [R] En el SIC, una acción individual de mega-cap tiene igual o más liquidez que la mayoría de los apalancados sectoriales.

---

## 8. Liquidez, spreads y formadores de mercado

- [H] La BMV define al formador de mercado como el miembro "aprobado por la misma para promover la liquidez y establecer precios de referencia". Sus obligaciones incluyen montos mínimos y un spread máximo de ~0.25% a 7.0% según el valor [9]. La tabla pública de formadores lista sobre todo ETFs locales (ISHRS) [9]. **No encontré formadores de mercado con obligaciones publicadas para los apalancados del SIC.**
- [I] En los apalancados del SIC, el precio local lo arbitran los intermediarios contra el mercado de origen. Por eso la desviación sube en los ETFs poco operados: TNA, LABU, NUGT y COPX con máximos de 5% a 9.5% [C].
- [H] En el SIC no hay fracciones [19][20]. [C] Con 20,000 MXN, SMH, SOXX, SPY, IVV, QQQ y VOO son posiciones de 50% a 68% por título. GLD es 35%. SOXL, TQQQ, IAU, SLV, SPLG y QQQM permiten incrementos de 5% a 27%.
- [H] Costo de ida y vuelta en Trading MX: 0.58% con IVA, antes del spread (ver `01`).
- [C] Referencia: rotar la posición completa 8 veces por temporada (8 idas y vueltas) cuesta ~4.6% del capital en comisiones (8 × 0.58%). Con desviaciones de 0.2%–0.4% por lado, la fricción total queda en ~6%–8% por temporada. El tope `operaciones_max_mes` = 8 permite hasta ~48 operaciones por temporada, así que la fricción puede ser bastante mayor si se usa completo.

---

## 9. Precio en MXN = precio en USD × tipo de cambio

- [C] TC implícito (cierre BMV / cierre EUA) con SPY: 17.35 (31-jul), 16.97 (31-ago), 17.50 (23-sep) y 17.75 (24-sep-2026). SOXL, SPXL, SMH, GLD e IVV dan el mismo TC con ±0.2% en los días líquidos [30].
- [H] Referencia de mercado: el peso abrió el 24-sep-2026 en ~17.50 por dólar (El Informador, 07:57) [32]. [I] El salto a ~17.72–17.75 al cierre (depreciación de ~1.3%) coincide con lo que reporta la prensa del día [32].
- [I] Toda posición en el SIC es una posición larga en USD. Entre el 30-jun y el 31-ago-2026, el TC implícito bajó de 17.52 a 16.97 (−3.1%). Ese movimiento resta directo al TWR en MXN, aunque el activo no se mueva en USD.
- [H] La BMV opera de 7:30 a 14:00 (CDMX) mientras EUA está en horario de verano. Eso alinea el cierre local con el de EUA [30] (detalle y fechas de cambio en `01`).

---

## 10. Riesgos específicos

### 10.1 Decaimiento por volatilidad (volatility decay)

**Fórmula.** Para un ETF con rebalanceo diario a L veces, con volatilidad anualizada σ del índice, horizonte T en años y sin costos:

ln(1 + R_ETF) ≈ L · ln(1 + R_índice) − ((L² − L) / 2) · σ² · T

El término (L² − L)/2 · σ² vale σ² para un 2x y 3σ² para un 3x. El arrastre de un 3x es 3 veces el de un 2x, no 1.5 veces [24][25].

- [C] **Validación contra el prospecto de TQQQ** [23]. Con el índice plano a 1 año, la fórmula da −17.1% (σ = 25%), −52.8% (σ = 50%) y −95.0% (σ = 100%). La tabla oficial da **exactamente** −17.1%, −52.8% y −95.0% [23].
- [H] Tabla del prospecto de TQQQ, rendimiento esperado del fondo a 1 año [23]:

| Índice a 1 año | 3x ingenuo | σ = 10% | σ = 25% | σ = 50% | σ = 75% |
|---|---|---|---|---|---|
| −20% | −60% | −50.3% | −57.6% | −75.8% | −90.5% |
| 0% | 0% | −3.0% | −17.1% | −52.8% | −81.5% |
| +20% | +60% | +67.7% | +43.3% | −18.4% | −68.0% |
| +40% | +120% | +166.3% | +127.5% | +29.6% | −49.2% |

- [H] En el mismo prospecto, la volatilidad anualizada del Nasdaq-100 a 5 años (al 31-may-2025) fue 23.90% [23]. REX Shares estima ~9% de decaimiento anual para un 2x con subyacente de 30% de volatilidad y ~63% con 100% [24].
- [C] **Arrastre a 6 meses (temporada), índice plano, sin costos:**

| σ del subyacente | Ejemplo 2026 | 2x | 3x |
|---|---|---|---|
| 15% | SPY (13.5%) | −1.1% | −3.3% |
| 25% | QQQ (22.3%) | −3.1% | −8.9% |
| 40% | — | −7.7% | −21.3% |
| 55% | SOXX (55.1%) | −14.0% | **−36.5%** |
| 75% | — | −24.5% | −57.0% |

- [H] **Costos adicionales:** TQQQ tiene un gasto neto de 0.82% (0.97% bruto, con exención hasta el 30-sep-2026) [23], más el financiamiento implícito del apalancamiento. [C] En 6 meses de 2026, TQQQ rindió +81.2% contra +90.8% de la fórmula sin costos. El faltante (~9.6 pp) es costo de financiamiento, comisiones y tracking [30].
- [H] **Riesgo de gap:** "If the Index approaches a 33% loss at any point in the day, you could lose your entire investment" (prospecto de TQQQ) [23].
- [I] La tendencia favorece al apalancado: TECL rindió 3.3x a XLK en 6 meses de tendencia. El rango lateral con volatilidad lo destruye. Por eso el `filtro_apalancados` de `parametros.json` (subyacente sobre su MM200 y VIX < 25) apunta al riesgo correcto.

### 10.2 Suspensión, cierre, deslistado y eventos corporativos

- [H] **Cierres de fondos:** Direxion anunció el 13-mar-2026 el cierre de 10 ETFs por falta de activos, con último día el 10-abr-2026 y liquidación del 10 al 17-abr-2026 [27]. Antes cerró 2 ETFs (jul-2025) y 3 (oct-2025) [27].
- [H] **ETNs:** BMO redimió el ETN FNGU (FANG+ 3x) con último día de operación esperado el 14-may-2025. Lo sustituyó con un ETN nuevo (FNGB) que reusaría el ticker FNGU [26]. Un ETN también tiene riesgo de crédito del emisor.
- [H] **Splits y reverse splits en el SIC:** la BMV replica los eventos del mercado de origen. TQQQ hizo un split 2:1 efectivo el 20-nov-2025 [3]. REW (inverso) y SMN hicieron reverse splits, con fracciones pagadas en efectivo ("CashInLieuOfFraction") [4][5]. [I] Los inversos (SOXS, SQQQ) hacen reverse splits con frecuencia. Hay que conciliar la posición y el precio después de cada aviso.
- [H] **Plataforma:** DriveWealth puede retirar los apalancados sin aviso (vía Trading USA) [22].
- [I] Si el fondo cierra en EUA, el listado en el SIC se cancela y la posición se liquida al NAV final. Si el fondo solo se deslista del SIC, la posición seguiría viva en EUA pero sin mercado local. El procedimiento de cancelación en la CNBV y la BMV **no está verificado** (ver §2.2).
- [R] Solo usar apalancados con AUM grande y listado activo en BMV (SOXL, TQQQ, SPXL, TECL). Nada de ETNs ni de fondos nuevos o chicos.

### 10.3 Riesgo de liquidez local en estrés

- [I] En el SIC la liquidez viene de los intermediarios que arbitran contra EUA. En una apertura con gap o en una sesión de pánico, la desviación de los ETFs poco operados puede superar con facilidad los máximos observados (hasta 9.5%). Una orden a mercado en QLD, SPUU, TNA o LABU puede ejecutarse varios puntos lejos del valor justo.

---

## 11. Tabla final

Leyenda de liquidez (mediana del importe diario en BMV, 30 días) [C][30]: **Muy alta** > 50 M MXN · **Alta** 5–50 M · **Media** 1–5 M · **Baja** 0.2–1 M · **Muy baja** < 0.2 M o menos de 15 de 22 días con operación.

"Restricción de perfil" [H][1][10][11]: en la app de GBM (ejecución de operaciones) no hay una restricción regulatoria identificada; basta la carta de ejecución de operaciones. Advertencias o bloqueos propios de GBM: no verificado. En la tabla, "Carta EO" significa esto.

| Instrumento | Tipo | ¿Disponible en SIC vía GBM? (fuente) | Restricción de perfil | Liquidez estimada |
|---|---|---|---|---|
| SOXL | ETF 3x semiconductores | **Sí**: listado activo en BMV [2]; opera diario [30] | Carta EO | **Muy alta** (87.5 M) |
| SOXS | ETF −3x semiconductores | **Sí** [30] | Carta EO | Alta (26.4 M) |
| SPXL | ETF 3x S&P 500 | **Sí** [30][31] | Carta EO | Alta (7.0 M) |
| TQQQ | ETF 3x Nasdaq-100 | **Sí**: aviso BMV serie `*` [3]; opera diario [30] | Carta EO | Media-alta (4.7 M; promedio 11.2 M) |
| TECL | ETF 3x tecnología | **Sí** [30] | Carta EO | Media (1.0 M) |
| QLD | ETF 2x Nasdaq-100 | **Sí**, poco operado [30] | Carta EO | Muy baja (0.08 M; 12/22 días) |
| SPUU | ETF 2x S&P 500 | **Sí**, poco operado [30] | Carta EO | Muy baja (0.36 M; 11/22 días) |
| UPRO | ETF 3x S&P 500 | **No verificado** [30][31] | — | — |
| SSO | ETF 2x S&P 500 | **No verificado** [30][31] | — | — |
| FNGU | ETN 3x FANG+ | **No verificado**; el ETN original se redimió en 2025 [26] | — | — |
| SQQQ | ETF −3x Nasdaq-100 | **Sí** [30] | Carta EO | Media (1.6 M) |
| NUGT | ETF 2x mineras de oro | **Sí** [30] | Carta EO | Media (2.5 M) |
| FAS / LABU / TNA / YINN / TMF | ETFs 3x sectoriales y regionales | **Sí** [30] | Carta EO | Baja (0.2–0.9 M) |
| TSLL | ETF 2x Tesla | **Sí** [30] | Carta EO | Baja (0.27 M) |
| DDM | ETF 2x Dow 30 | **Sí**, casi sin operación [30] | Carta EO | Muy baja (4/22 días) |
| IBIT / FBTC / otros BTC spot | ETF bitcoin spot | **No verificado en SIC**; **Sí en Trading USA** [14][15] | Sin restricción mencionada [14] | n.a. en BMV |
| MSTR | Acción (proxy BTC) | **Sí** [30] | Carta EO | Alta (8.6 M) |
| COIN | Acción (cripto) | **Sí** [30] | Carta EO | Media (2.0 M) |
| SMH | ETF semiconductores | **Sí** [30] | Carta EO | Media (2.4 M); 1 título = 53% de la cuenta |
| SOXX | ETF semiconductores | **Sí** [30] | Carta EO | Alta (5.7 M); 1 título = 49% |
| XLK | ETF tecnología | **Sí** [30] | Carta EO | Media (2.1 M) |
| IGV | ETF software | **Sí** [30] | Carta EO | Media (1.6 M) |
| ARKK | ETF temático activo | **No verificado** [30][31] | — | — |
| URA | ETF uranio | **Sí** [30] | Carta EO | Baja (0.31 M) |
| COPX | ETF mineras de cobre | **Sí** [30] | Carta EO | Baja (0.91 M); desviación máx. 9.5% |
| GDX | ETF mineras de oro | **Sí** [30] | Carta EO | Baja (0.59 M) |
| XLE | ETF energía | **Sí** [30] | Carta EO | Media (1.2 M) |
| KWEB | ETF internet China | **Sí** [30] | Carta EO | Muy baja (0.09 M) |
| GLD | ETF oro | **Sí** [30] | Carta EO | Alta (6.9 M); 1 título = 35% |
| IAU | ETF oro | **Sí** [30] | Carta EO | Alta (5.0 M) |
| SLV | ETF plata | **Sí** [30] | Carta EO | Media (3.4 M) |
| NAFTRAC | ETF IPC (local BMV) | **Sí** (BMV local) [30] | Carta EO | **Muy alta** (114 M) |
| EWW | ETF MSCI México | **Sí**, poco operado [30] | Carta EO | Muy baja (0.16 M; 11/22 días) |
| TLT | ETF Treasuries 20+ | **Sí** [30] | Carta EO | Media (2.2 M) |
| Acciones S&P 500 / Nasdaq-100 | Acciones EUA serie `*` | **Sí**, ≥79% del S&P 500 y ≥83% del NDX con cotización BMV (cota inferior) [30][8] | Carta EO | Varía; mega-caps de Alta a Muy alta |
| ADRs / emisoras no estadounidenses | Serie `N` | **Sí** existen (SONY N, PHIA N, WPM N) [6]; TSM, BABA y MELI **no verificados** | Carta EO | No verificada |

---

## Implicaciones para la cuenta arena

1. **[R] El canal es Trading MX (SIC).** Opera en MXN, sin conversión por operación, con órdenes limitadas y stops (ver `01`) y dentro del régimen del art. 129 LISR. Trading USA solo para BTC spot, si la estrategia lo pide.
2. **[R] Hay dos niveles de agresividad**, porque el decaimiento crece con σ² y no con L:
   - **Base agresiva: TQQQ y SPXL.** Volatilidad del subyacente de 13%–22%. Arrastre esperado a 6 meses de ~3%–9% con el mercado plano. En 2026 entregaron ~3x su índice. Liquidez local de 4.7–7 M MXN/día, suficiente para órdenes de 2k–10k MXN.
   - **Palanca de varianza: SOXL.** Tiene la mayor liquidez local de todo el universo apalancado, pero su subyacente tiene 55% de volatilidad. Implica ~36% de arrastre a 6 meses con el mercado plano, −57% en un mes (jul-2026) y −69% de drawdown máximo en 6 meses.
3. **[R] Propuesta de ajuste a `parametros.json` → `arena_agresivo` (sigue provisional).** Hoy `etf_apalancado_max` = 0.5 sin distinguir subyacente. Un 50% en SOXL en un mes como julio de 2026 le quitaría ~28%–33% a la cuenta en semanas. Eso rebasaría el cortacircuitos de −28% con una sola posición. Propuesta:
   - Tope de 0.5 para 3x con σ del subyacente < 30% (TQQQ, SPXL).
   - Tope de **0.25** para 3x con σ ≥ 30% (SOXL, TECL, LABU, NUGT).
   - Suma de apalancados ≤ 0.6.
   - Validar contra la teoría de torneos (tarea aparte) antes de fijarlo.
4. **[R] Ejecución:** solo órdenes limitadas. El precio límite se calcula como precio en EUA × USD/MXN spot del mismo minuto, con tolerancia de 0.3% en SOXL, TQQQ y SPXL y de 1% en ilíquidos. No usar órdenes a mercado en QLD, SPUU, DDM, TNA, LABU, EWW, KWEB ni COPX.
5. **[R] Granularidad:** no hay fracciones en el SIC. Preferir IAU sobre GLD, QQQM o SPLG sobre QQQ o SPY, y SOXL o TQQQ sobre SMH o SOXX para las exposiciones 1x. Si no, una sola unidad se come 35% a 68% de la cuenta.
6. **[R] Sustitutos por disponibilidad:** para S&P 3x, SPXL (UPRO no verificado). Para S&P 2x, SPUU con límite (SSO no verificado). Para Nasdaq 2x, QLD solo con límite y paciencia, o bien TQQQ en menor tamaño. Para temático tipo ARKK: no hay equivalente verificado; IGV o XLK como proxy. Para cripto dentro del SIC: MSTR (y COIN como segunda opción).
7. **[I] El TC es un factor común.** El rival usa la misma casa de bolsa. Si también opera en el SIC, el TC afecta a ambos por igual. Si Grok se queda en activos en MXN (CETES, NAFTRAC), un peso apreciándose (como el −3.1% del TC implícito entre el 30-jun y el 31-ago-2026) mueve el marcador en su favor sin que nadie opere.
8. **[R] Pendientes antes del primer fondeo** (registrar en la bitácora):
   - Confirmar en la app que aparecen `SOXL *`, `TQQQ *`, `SPXL *`, `TECL *`, `MSTR *` e `IAU *` en Trading MX.
   - Probar si comprar un apalancado muestra una advertencia o pide un cambio de perfil.
   - Buscar UPRO, SSO, ARKK e IBIT en Trading MX y anotar el resultado.
   - Revisar si hay un reverse split pendiente en los inversos antes de usarlos.

---

## No verificado (resumen)

- El texto vigente de las Disposiciones SIC de la CNBV (cnbv.gob.mx no accesible: 503/TLS) y el procedimiento de cancelación del listado.
- Si la app de GBM bloquea o advierte en los ETFs apalancados según el perfil del cliente.
- Que UPRO, SSO, FNGU (nuevo), ARKK, NVDL, BITO, IBIT, FBTC, ETHA, TSM, BABA y MELI estén en el SIC. No aparecen en StockAnalysis ni en TradingView, pero esos agregadores omiten valores que sí están listados.
- La nomenclatura exacta con que la app de GBM muestra la serie (`*`/`N`).
- Que existan formadores de mercado con obligaciones para los apalancados del SIC.
- Los tickers de los ETFs de Ethereum en Trading USA.

---

## Fuentes

1. BMV, "Mercado Global (SIC)". https://www.bmv.com.mx/es/mercados/mercado-global (consultado el 25-sep-2026)
2. BMV, Estadísticas de Operación, "SOXL *" (DIREXION DAILY SEMICONDUCTOR BULL 3X ETF, ISIN US25459W4583, estatus ACTIVA). https://www.bmv.com.mx/es/emisoras/estadisticas/SOXL%20*-33387 (consultado el 25-sep-2026)
3. BMV, Aviso de Derechos SIC, TQQQ serie *, split 2:1, fecha 06/11/2025. https://www.bmv.com.mx/docs-pub/sicderec/sicderec_1506126_1.pdf
4. BMV, Aviso de Derechos SIC, REW (ProShares UltraShort Technology) serie *, reverse split, 05/11/2025. https://www.bmv.com.mx/docs-pub/sicderec/sicderec_1505588_1.pdf
5. BMV, Aviso de Derechos SIC, SMN (ProShares UltraShort Materials) serie *, reverse split, 12/05/2026. https://www.bmv.com.mx/docs-pub/sicderec/sicderec_1559127_1.pdf
6. BMV, Avisos de Derechos SIC: SONY N (03/10/2025) https://www.bmv.com.mx/docs-pub/sicderec/sicderec_1497360_1.pdf ; WPM N (09/05/2025) https://bmv.com.mx/docs-pub/sicderec/sicderec_1464345_1.pdf ; PHIA N (13/05/2025) https://www.bmv.com.mx/docs-pub/sicderec/sicderec_1464806_1.pdf ; SW1 N (08/09/2025) https://bmv.com.mx/docs-pub/sicderec/sicderec_1491843_1.pdf ; BERY * (30/01/2025) https://www.bmv.com.mx/docs-pub/sicderec/sicderec_1437900_1.pdf
7. BMV, Información adicional de avisos de derechos del SIC, SPYM serie * (26/03/2026). https://www.bmv.com.mx/docs-pub/infderec/infderec_1544429_1.pdf
8. BMV, comunicado "3 mil valores listados en el SIC de la BMV", 04-ene-2022. https://www.bmv.com.mx/docs-pub/SALA_PRENSA/CTEN_BOLE/3%20mil%20valores%20listados%20en%20el%20SIC%20de%20BMV%20040122.pdf
9. BMV, "Formador de Mercado". https://bmv.com.mx/es/Grupo_BMV/Formador_de_mercado (consultado el 25-sep-2026)
10. DOF, Resolución que modifica las Disposiciones de carácter general aplicables a las entidades financieras y demás personas que proporcionen servicios de inversión (Anexo 6), 09-feb-2016. https://dof.gob.mx/nota_detalle.php?codigo=5424746&fecha=09/02/2016
11. GBM, Guía de Servicios de Inversión (versión V0424; PDF modificado el 14-nov-2024). https://assets.gbm.com/docs/Guia-de-Servicios-GBM.pdf
12. GBM, FAQ "¿Qué comisiones cobran al invertir en GBM?". https://gbm.com/faqs/que-comisiones-cobran-al-invertir-en-gbm/ (consultado el 25-sep-2026)
13. GBM, "Trading en México y Estados Unidos". https://gbm.com/trading/ (consultado el 25-sep-2026)
14. GBM Academy, "ETFs de Bitcoin, disponibles en Trading Global de GBM", 12-ene-2024. https://gbm.com/media/the-academy/etfs-de-bitcoin-disponibles-en-trading-global-de-gbm-2/
15. GBM Academy, "¿Cómo acceder a ETFs de Bitcoin para inversionistas?", 23-ene-2024. https://gbm.com/media/the-academy/acceso-a-etfs-de-bitcoin-a-traves-de-gbm/
16. DPL News, "ETFs de Bitcoin: mexicanos ya pueden invertir en GBM+", 24-ene-2024. https://dplnews.com/etfs-de-bitcoin-mexicanos-ya-pueden-invertir-en-gbm/
17. GBM Academy, "Trading Global: ¿Qué es y cómo empezar?", 16-nov-2022. https://gbm.com/media/the-academy/trading-global-que-es-y-como-empezar/
18. InvestorHouse, "Trading MX vs Trading USA en la Casa de Bolsa GBM", 19-dic-2025. https://www.investorhouse.com.mx/blog/explicacion-trading-mx-trading-usa-gbm/
19. Eduardo Rosas, "Cómo invertir en acciones fraccionadas en GBM" (el SIC no permite fracciones), 09-dic-2021. https://eduardorosas.mx/como-invertir-en-acciones-fraccionadas-en-gbm/
20. Finantres, "Acciones fraccionadas en GBM", actualizado el 16-sep-2026. https://finantres.mx/acciones-fraccionadas-en-gbm/
21. Finantres, "Mejores ETFs apalancados en México 2026", actualizado el 16-sep-2026. https://finantres.mx/mejores-etfs-apalancados/
22. DriveWealth Legal Hub, "Investment Products", 10-oct-2025. https://legal.drivewealth.com/investment-products
23. ProShares, TQQQ Summary Prospectus (26-sep-2025) con suplemento del 18-feb-2026. https://www.proshares.com/globalassets/proshares/prospectuses/tqqq_summary_prospectus.pdf
24. REX Shares, "How Leveraged ETFs Work" (revisado en ago-2026). https://www.rexshares.com/how-leveraged-etfs-work/
25. Pomegra Wiki, "Leveraged ETF Decay" (fórmula (σ²/2)·L(L−1), atribuida a Cheng y Madhavan, 2009). https://pomegra.io/wiki/leveraged-etf-decay/ (fórmula validada contra [23])
26. BMO, "BMO Announces Upcoming Redemption and Ticker Symbol Change for MicroSectors FANG+ Index 3x Leveraged ETNs (FNGU)…", 19-feb-2025. https://newsroom.bmo.com/2025-02-19-BMO-Announces-Upcoming-Redemption-and-Ticker-Symbol-Change-for-MicroSectorsTM-FANG-TM-Index-3x-Leveraged-ETNs-Ticker-FNGU-as-well-as-the-Launch-of-a-New-MicroSectorsTM-Exchange-Traded-Note-ETN-,-the-MicroSectorsTM-FANG-TM-3x-Leveraged-ETNs-Tick
27. Direxion, "Direxion Closing Ten ETFs", 13-mar-2026 (vía Yahoo Finance). https://finance.yahoo.com/news/direxion-closing-ten-etfs-212400721.html ; cierres de 2025: https://www.direxion.com/press-release/direxion-closing-two-etfs y https://finance.yahoo.com/news/direxion-closing-three-etfs-125200518.html
28. El Cronista México, "Inversionistas en México se refugian en IA y defensa: fondos globales de microchips ganan más de 800%", 26-may-2026 (datos de Morningstar). https://www.cronista.com/mexico/finanzas-economia/inversionistas-en-mexico-se-refugian-en-ia-y-defensa-fondos-globales-de-microchips-ganan-mas-de-800/
29. NotiMx, "Grupo BMV y S&P Dow Jones Indices celebran la Cumbre Anual de Índices & ETFs en México 2026", 12-may-2026. https://www.notimx.mx/2026/05/grupo-bolsa-mexicana-de-valores-y-s-dow.html
30. StockAnalysis (datos de S&P Global), páginas de cotización e historial BMV y EUA consultadas el 25-sep-2026. Formato BMV: https://stockanalysis.com/quote/bmv/{TICKER}/history/ (p. ej. https://stockanalysis.com/quote/bmv/SOXL/history/, https://stockanalysis.com/quote/bmv/TQQQ/). Formato EUA: https://stockanalysis.com/etf/{ticker}/history/. Listas: https://stockanalysis.com/list/mexican-stock-exchange/, https://stockanalysis.com/list/sp-500-stocks/, https://stockanalysis.com/list/nasdaq-100-stocks/
31. TradingView, páginas BMV (p. ej. https://www.tradingview.com/symbols/BMV-TQQQ/, BMV-SOXL, BMV-SPXL; y 404 para BMV-UPRO, BMV-SSO, BMV-ARKK, BMV-IBIT, BMV-FNGU), consultado el 25-sep-2026.
32. El Informador, "Dólar HOY: el tipo de cambio este 24 de septiembre amanece en 17.50 pesos", 24-sep-2026. https://www.informador.mx/economia/dolar-hoy-el-tipo-de-cambio-este-24-de-septiembre-amanece-en-17.50-pesos-por-billete-verde-20260924-0049.html
33. Rankia México, "Impuestos por vender acciones y ETFs en México: guía de ISR", 11-jun-2026. https://www.rankia.mx/blog/como-comenzar-invertir-bolsa/7335308-que-impuestos-pagas-vender-acciones-etfs-mexico
34. DOF, Circular 4/2019 de Banco de México (operaciones con activos virtuales), 08-mar-2019. https://www.dof.gob.mx/nota_detalle.php?codigo=5552303&fecha=08/03/2019
35. CNBV, Disposiciones de carácter general aplicables a los sistemas internacionales de cotizaciones (PDF). https://www.cnbv.gob.mx/Normatividad/Disposiciones%20de%20car%C3%A1cter%20general%20aplicables%20a%20los%20sistemas%20internacionales%20de%20cotizaciones.pdf (**no accesible** el 25-sep-2026: HTTP 503 y error TLS)
