# V02. Momentum internacional: factor académico (WML) y ETFs operables

> Fase 0 (formación). No es recomendación de inversión.
> Estado: **Replicado** (factor académico: la cifra recibida se reproduce al centésimo, con matices). **Versión operable: sin evidencia de ventaja y sin listado en el SIC verificado.**
> Reproducir desde la raíz del repo: `python3 laboratorio/replicas/V02-momentum-internacional/reproducir.py`. No usa red: datos congelados en `datos/`, huellas en `SHA256SUMS.txt` y todas las pruebas en `variantes.csv` (154 filas).

| Campo | Valor |
|---|---|
| ID | V02-momentum-internacional |
| Afirmación a verificar | "Momentum en emergentes paga 9.6% anual desde 2000 con t muy alta y 12.3% desde 2010; en otros desarrollados sigue funcionando". Cifra de otro sistema, sin código ni datos adjuntos |
| Pre-registro escrito el | 2026-09-25, 05:24 UTC, **antes** de descargar series de rendimientos o calcular algo. Una copia sin cambios está en `preregistro.md`, con su huella en `SHA256SUMS.txt` |
| Responsable | Claude (subagente del laboratorio) |

---

## PRE-REGISTRO (no se edita después de la primera corrida; los cambios van a "Desviaciones")

### 1. Hipótesis y mecanismo

- **H1 (académica, por región).** La media mensual del factor WML de French es mayor que 0 en Developed, Developed ex US, Europe, Japan, Asia Pacific ex Japan, North America y Emerging.
- **H2 (decaimiento después de publicarse).** La media es menor después de cada publicación clave que antes de ella (McLean y Pontiff, 2016). Es descriptiva: no hay prueba formal de diferencia de medias.
- **H3 (Japón).** WML de Japón no es distinto de cero. Fama y French (2012) reportan "Except for Japan, there is return momentum everywhere".
- **H4 (operable).** Un ETF de momentum, emergente o desarrollado ex EUA, rinde más que su ETF de mercado comparable desde que sigue un índice de momentum. Se mide en MXN y neto de costos de GBM.
- **Mecanismo propuesto en la literatura.** Hay dos explicaciones: subreacción conductual a la información y riesgo de *crash*. La segunda dice que el momentum pierde mucho en los rebotes después de caídas del mercado (Daniel y Moskowitz, 2016). Aquí no se prueba el mecanismo.

### 2. Datos (fuentes fijadas antes de descargar)

| Serie | Fuente y archivo | Uso |
|---|---|---|
| WML por región | French: `Developed_Mom_Factor_CSV.zip`, `Developed_ex_US_Mom_Factor_CSV.zip`, `Europe_Mom_Factor_CSV.zip`, `Japan_Mom_Factor_CSV.zip`, `Asia_Pacific_ex_Japan_MOM_Factor_CSV.zip`, `North_America_Mom_Factor_CSV.zip` y `Emerging_MOM_Factor_CSV.zip` | H1, H2, H3, afirmación |
| Mercado regional (Mkt-RF, RF) | French: `<Región>_5_Factors_CSV.zip`. Emerging solo tiene la versión de 5 factores, así que se usa la de 5 en todas las regiones por uniformidad | Correlación, beta y peores meses |
| 6 carteras por tamaño y momentum | French: `<Región>_6_Portfolios_ME_Prior_12_2_CSV.zip` y `Emerging_Markets_6_Portfolios_ME_Prior_12_2_CSV.zip` | Pierna larga académica |
| ETFs | Yahoo chart v8, diario, `events=div,split`, `adjclose`. JSON crudo congelado | H4 |
| Tipo de cambio | FRED `DEXMXUS` (CSV crudo congelado). Yahoo `MXN=X` como verificación | Conversión a MXN |

- **Unidades.** Todas las series de French están en USD, incluyen dividendos, no tienen costos y la RF es la T-bill de EUA.
- **Nota del sitio de French** (consultado el 2026-09-25): WML = ½(Small High + Big High) − ½(Small Low + Big Low), con ordenamientos 2×3 mensuales y momentum de t−12 a t−2. En emergentes los cortes de momentum se calculan **por país**.
- **Huellas.** Cada archivo se congela en `datos/` con su SHA-256. Se registra la versión que declara el preámbulo.

### 3. Ventanas (todas se reportan, para las 7 regiones)

"Fin" es el último mes disponible en el archivo. "Inicio" es el primer mes con dato.

| Clave | Ventana | Motivo |
|---|---|---|
| W0 | Inicio a Fin | Todo el periodo disponible |
| W1 | 2000-01 a 2025-12 | Afirmación "desde 2000" (años completos) |
| W1b | 2000-01 a Fin | Sensibilidad de la afirmación |
| W2 | 2010-01 a 2025-12 | Afirmación "desde 2010" (años completos) |
| W2b | 2010-01 a Fin | Sensibilidad de la afirmación |
| R98-pre / R98-post | Inicio a 1998-02 / 1998-03 a Fin | Rouwenhorst (1998), *International Momentum Strategies*, JF 53(1):267-284, feb-1998. Su muestra: 1980-1995, 12 países europeos |
| R99-pre / R99-post | Inicio a 1999-08 / 1999-09 a Fin | Rouwenhorst (1999), *Local Return Factors and Turnover in Emerging Stock Markets*, JF 54(4):1439-1464, ago-1999. **Solo Emerging** |
| FF12-in / FF12-out | 1990-11 a 2011-03 / 2011-04 a Fin | Fama y French (2012), *Size, value, and momentum in international stock returns*, JFE 105(3):457-472. Construyen estos mismos datos; sus pruebas cubren nov-1990 a mar-2011. 2011-04 en adelante es fuera de su muestra. Para Emerging no es fuera de muestra (el artículo no lo cubre); se reporta por comparabilidad |
| AMP13-pre / AMP13-post | Inicio a 2013-06 / 2013-07 a Fin | Asness, Moskowitz y Pedersen (2013), *Value and Momentum Everywhere*, JF 68(3):929-985, jun-2013 |
| AMP09-post | 2009-04 a Fin | Sensibilidad: primera versión pública en SSRN (abstract 1363476), fechada el 6-mar-2009 según el buscador; no verificada en la página de SSRN |

El mes de publicación pertenece al tramo "pre", según la convención del laboratorio.

### 4. Inferencia y veredicto

- **Por ventana:** n, media mensual, t Newey-West con 6 rezagos (`herramientas/estadistica.py`), IC95, t iid y media ×12.
- **CAGR.** También se reporta la tasa compuesta del factor, (∏(1+WML))^(12/n) − 1. **La media ×12 no es CAGR**, y ninguna de las dos es la riqueza de un inversionista: WML es largo-corto, sin costos y en USD.
- **Veredicto:** "apoyo" si el límite inferior del IC95 NW(6) es mayor que 0, "contraria" si el límite superior es menor que 0, "inconcluso" en cualquier otro caso.
- **Pruebas múltiples.** Se reportan todas las ventanas (unas 80 pruebas). No se elige la mejor. Se informa cuáles también pasarían con Bonferroni al 5% sobre las 7 regiones en W1 (|t| > 2.69).

### 5. Criterio para la afirmación recibida (fijado antes de calcular)

- **A1a "9.6% anual desde 2000" (Emerging).** Se reproduce si la media ×12 **o** el CAGR del factor, en W1 **o** en W1b, queda dentro de ±0.5 pp de 9.6%. Se informa qué medida y qué ventana coinciden.
- **A1b "t muy alta".** Se interpreta como t NW(6) ≥ 3.0 en W1. Si 1.96 ≤ t < 3.0, es significativo pero no "muy alto". Si t < 1.96, no es significativo.
- **A1c "12.3% desde 2010".** El mismo criterio de ±0.5 pp en W2 o W2b. Además se reporta su t.
- **A2 "en otros desarrollados sigue funcionando".** Se interpreta como Developed ex US con veredicto "apoyo" en W2 **y** en AMP13-post. Las subregiones (Europe, Japan, Asia Pacific ex Japan, North America) se reportan como detalle.
  - Confirmada: Developed ex US con "apoyo" en ambas ventanas.
  - Con matices: "apoyo" en una sola.
  - No confirmada: inconcluso o contraria en ambas.
- **Etiqueta global.** "Confirmada" si A1a, A1b, A1c y A2 se confirman. "Confirmada con matices" si se confirman los números de emergentes pero no todo lo demás. "No confirmada" si A1a o A1c fallan.

### 6. Riesgo de *crash* y relación con el mercado (descriptivo, sin veredicto)

- Los 5 peores meses de WML en W0, con el rendimiento Mkt-RF de la región en ese mismo mes.
- Caída máxima del índice compuesto ∏(1+WML), con sus fechas de pico y valle.
- Peor rendimiento compuesto en 12 meses.
- Asimetría.
- Correlación de Pearson y beta MCO de WML contra Mkt-RF regional, en W0 y en W1.
- Beta condicional según el estado del mercado (Daniel y Moskowitz, 2016). El estado es "bajista" si el rendimiento acumulado de Mkt-RF regional en los 24 meses previos (t−24 a t−1) es menor que 0 y "normal" en otro caso. Se reportan ambas betas y la media de WML en cada estado.

### 7. Pierna larga académica (paso intermedio, no operable)

- **Serie:** "Big High" (grandes ganadoras, ponderada por valor) de las 6 carteras de tamaño y momentum de cada región, menos el mercado regional (Mkt-RF + RF).
- **Qué mide:** si la parte "solo compra" del momentum supera al mercado, sin costos y con rebalanceo mensual.
- **Ventanas:** W0, W1, W2 y AMP13-post. Mismo veredicto que el punto 4.
- **Advertencia:** sigue sin ser operable. No tiene costos de rotación y usa rebalanceo mensual.

### 8. Versión operable: ETFs (lista cerrada)

**Candidatos de momentum.** Fechas y gastos tomados de buscadores y emisores el 2026-09-25; se verifican en la corrida.

| Ticker | Qué es | Inicio como momentum |
|---|---|---|
| EEMO | Invesco S&P Emerging Markets Momentum | Fue EEHB (High Beta) hasta el cierre del 18-mar-2016 (SEC 497, 21-dic-2015). Momentum desde abr-2016 |
| PIE | Invesco Dorsey Wright Emerging Markets Momentum | Lanzado el 28-dic-2007. Momentum desde 2008-01 |
| IMTM | iShares MSCI Intl Momentum Factor | Lanzado el 13-ene-2015. Desde 2015-02 |
| PIZ | Invesco Dorsey Wright Developed Markets Momentum | Lanzado el 28-dic-2007. Desde 2008-01 |
| IDMO | Invesco S&P International Developed Momentum | Fue IDHB (High Beta) hasta el 18-mar-2016. Desde abr-2016 |
| IMOM | Alpha Architect International Quantitative Momentum | Lanzado el 23-dic-2015. Desde 2016-01 |

- **Comparables de mercado:** EEM para emergentes; EFA y VEA para desarrollados ex EUA.
- **Excluido:** PDN es Invesco RAFI Developed Markets ex-US Small-Mid, un índice fundamental y no de momentum. No entra en la comparación.

**Pares.** Cada uno va desde el primer mes completo como momentum hasta el último mes completo (2026-08):

- EEMO contra EEM
- PIE contra EEM
- IMTM contra EFA y contra VEA
- PIZ contra EFA y contra VEA
- IDMO contra EFA y contra VEA
- IMOM contra EFA y contra VEA

Además hay una **ventana común** de 2016-04 a 2026-08 para los seis ETFs.

**Medición:**

- **Rendimiento en USD:** mensual, con el `adjclose` de Yahoo al último día hábil de cada mes. El gasto del ETF ya está descontado del NAV y del precio, así que **no se vuelve a restar**.
- **Conversión a MXN:** 1 + R_MXN = (1 + R_USD) × FX_t / FX_{t−1}, con FX = última observación del mes de DEXMXUS.
- **Costos de GBM:** comprar al inicio y vender al final, cobrados sobre el valor en cada momento.
  - Comisión: 0.29% por lado (0.25% + IVA).
  - Spread por lado: 0.05% en EEM, EFA y VEA; 0.15% en los ETFs de momentum (caso base) y 0.30% en la sensibilidad.
  - No se incluye el costo cambiario implícito del SIC (pendiente en el laboratorio).
- **Sensibilidad de impuestos (solo esta):** retención de 30% en EUA sobre los dividendos (sin W-8BEN). El rendimiento del mes se calcula como (close_t + 0.7·div_mes)/close_{t−1} − 1. El ISR mexicano no se modela.

**Métricas por par, en MXN y netas de costos:**

- CAGR.
- Riqueza final de 20,000 MXN.
- Volatilidad anualizada.
- Caída máxima mensual.

**Prueba (H4).** Diferencia mensual en USD (ETF − comparable): media, t NW(6), IC95 y veredicto con la regla del punto 4. Como descripción, también se reporta la beta de esa diferencia contra WML de la región, para comprobar que el ETF sí captura momentum.

**SIC.** El listado de cada ticker se da por verificado si se cumple una de dos condiciones:

- Hay una página o aviso de la BMV para esa clave con serie `*`.
- Yahoo `<TICKER>.MX` muestra precios en 2026 con bolsa MEX.

En otro caso queda como "no verificado" y la comparación se reporta igual, marcada como no confirmada como operable vía SIC.

### 9. Limpieza (reglas fijas)

- Faltantes de French (−99.99 / −999) se excluyen y se reporta su número.
- Meses incompletos de Yahoo se descartan.
- En días sin precio de Yahoo se usa el último cierre del mes con precio, y se reporta.
- No se eliminan valores extremos.
- Una ventana solo se calcula si tiene al menos 24 meses.

---

## RESULTADOS (corrida del 2026-09-25, después del pre-registro de las 05:24 UTC)

### Datos efectivamente usados

**French (21 zips).** Todos declaran "created using the **202608 Bloomberg** database". Las series internacionales de French vienen de Bloomberg, no de CRSP.

| Serie | Rango | Faltantes |
|---|---|---|
| WML de las regiones desarrolladas | 1990-11 a 2026-08 (430 meses) | 0 |
| WML de Emerging | 1990-01 a 2026-08 (440 meses) | 0 |
| Mkt-RF de 5 factores | desarrollados desde 1990-07; Emerging desde 1989-07 | En Emerging los faltantes están solo en RMW y CMA, que aquí no se usan |

Huellas: Emerging_MOM `5316f98a…`, Developed_ex_US_Mom `0b0941b3…`.

**Yahoo (JSON diario congelado).**

| Ticker | Primer día |
|---|---|
| EEMO | 2012-02-24 |
| PIE | 2008-01-07 |
| IMTM | 2015-01-27 |
| PIZ | 2008-01-07 |
| IDMO | 2012-02-24 |
| IMOM | 2015-12-23 |
| EEM | 2003-04-14 |
| EFA | 2001-08-27 |
| VEA | 2007-07-26 |

- Todos traen un día sin precio (2026-09-22), que no cae en ningún mes usado.
- Se usan meses completos hasta 2026-08.

**FRED `DEXMXUS`.** Del 1993-11-08 al 2026-09-18. Fin de mes: 2008-01 = 10.8190; 2016-03 = 17.2140; 2026-08 = 17.0081.

**Controles.**

- El rendimiento reconstruido con cierre + dividendos coincide con `adjclose`: diferencia media < 0.01 pp al mes y máxima de 0.29 pp. El split 3:1 de EEM en 2008 está bien tratado.
- DEXMXUS contra Yahoo MXN=X, en cambios mensuales: correlación de 0.982 y diferencia absoluta media de 0.47 pp. Se explica por la hora de la cotización. No afecta la comparación entre ETFs, porque ambos lados se convierten con el mismo tipo de cambio.
- **Verificación independiente.** Un script aparte, sin `herramientas/`, con su propio lector de CSV y JSON y NW calculado con la suma doble completa de Bartlett, da las mismas cifras. Coinciden al tercer decimal en Emerging W1, W1b, W2 y W2b y en Developed ex US W2 y AMP13-post, y al peso en la riqueza final de IDMO, EFA, EEMO, EEM, IMTM y PIZ.


#### Fuente A

| serie | V | periodo | n | media %/mes | DE | t IID | t NW(6) | IC95 NW %/mes | media x12 % (no es CAGR) | compuesto anual % (serie L-C; no es rendimiento de cuenta) | peor mes | mejor mes | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A:Emerging | V1 | 2000-01–2026-08 | 320 | 0.799 | 3.10 | 4.60 | 4.21 | [0.427, 1.171] | 9.59 | 9.37 | -16.84 (2026-07) | 12.84 (2026-04) | apoyo |
| A:Emerging | V2 | 2010-01–2026-08 | 200 | 1.025 | 3.02 | 4.80 | 5.47 | [0.658, 1.391] | 12.30 | 12.40 | -16.84 (2026-07) | 12.84 (2026-04) | apoyo |
| A:Emerging | V3 | 2016-01–2025-12 | 120 | 0.860 | 2.52 | 3.74 | 3.76 | [0.412, 1.309] | 10.32 | 10.41 | -9.15 (2022-11) | 7.03 (2021-01) | apoyo |
| A:Developed_ex_US | V1 | 2000-01–2026-08 | 320 | 0.584 | 3.51 | 2.98 | 2.59 | [0.141, 1.028] | 7.01 | 6.43 | -22.52 (2009-04) | 10.06 (2000-02) | apoyo |
| A:Developed_ex_US | V2 | 2010-01–2026-08 | 200 | 0.708 | 2.73 | 3.67 | 4.22 | [0.379, 1.038] | 8.50 | 8.35 | -12.31 (2020-11) | 7.21 (2020-03) | apoyo |
| A:Developed_ex_US | V3 | 2016-01–2025-12 | 120 | 0.479 | 2.57 | 2.04 | 2.27 | [0.064, 0.893] | 5.75 | 5.48 | -12.31 (2020-11) | 7.21 (2020-03) | apoyo |
| A:Europe | V1 | 2000-01–2026-08 | 320 | 0.749 | 4.08 | 3.28 | 3.05 | [0.267, 1.230] | 8.99 | 8.25 | -26.09 (2009-04) | 13.65 (2002-09) | apoyo |
| A:Europe | V2 | 2010-01–2026-08 | 200 | 0.851 | 3.08 | 3.90 | 4.77 | [0.501, 1.200] | 10.21 | 10.06 | -18.39 (2020-11) | 8.94 (2012-04) | apoyo |
| A:Europe | V3 | 2016-01–2025-12 | 120 | 0.618 | 3.08 | 2.20 | 2.69 | [0.168, 1.067] | 7.41 | 7.05 | -18.39 (2020-11) | 8.50 (2019-05) | apoyo |
| A:Asia_Pacific_ex_Japan | V1 | 2000-01–2026-08 | 320 | 0.889 | 3.51 | 4.53 | 3.66 | [0.413, 1.365] | 10.67 | 10.38 | -18.03 (2009-05) | 7.99 (2013-04) | apoyo |
| A:Asia_Pacific_ex_Japan | V2 | 2010-01–2026-08 | 200 | 1.040 | 3.05 | 4.82 | 4.99 | [0.631, 1.448] | 12.48 | 12.60 | -8.37 (2020-11) | 7.99 (2013-04) | apoyo |
| A:Asia_Pacific_ex_Japan | V3 | 2016-01–2025-12 | 120 | 0.751 | 2.86 | 2.88 | 3.41 | [0.319, 1.183] | 9.02 | 8.87 | -8.37 (2020-11) | 7.65 (2020-07) | apoyo |
| A:Japan | V1 | 2000-01–2026-08 | 320 | -0.020 | 3.96 | -0.09 | -0.09 | [-0.481, 0.440] | -0.24 | -1.19 | -18.28 (2026-07) | 14.80 (2000-02) | inconcluso |
| A:Japan | V2 | 2010-01–2026-08 | 200 | 0.082 | 3.40 | 0.34 | 0.40 | [-0.324, 0.488] | 0.98 | 0.28 | -18.28 (2026-07) | 14.30 (2026-04) | inconcluso |
| A:Japan | V3 | 2016-01–2025-12 | 120 | -0.090 | 2.89 | -0.34 | -0.37 | [-0.570, 0.391] | -1.08 | -1.57 | -8.50 (2016-08) | 8.44 (2016-06) | inconcluso |
| A:North_America | V1 | 2000-01–2026-08 | 320 | 0.248 | 4.93 | 0.90 | 1.00 | [-0.239, 0.735] | 2.97 | 1.51 | -25.00 (2009-04) | 29.32 (2000-02) | inconcluso |
| A:North_America | V2 | 2010-01–2026-08 | 200 | 0.348 | 3.29 | 1.50 | 1.74 | [-0.044, 0.740] | 4.18 | 3.58 | -12.98 (2026-07) | 11.35 (2026-04) | inconcluso |
| A:North_America | V3 | 2016-01–2025-12 | 120 | 0.164 | 3.32 | 0.54 | 0.58 | [-0.389, 0.718] | 1.97 | 1.32 | -12.72 (2023-01) | 6.94 (2020-03) | inconcluso |

#### Fuente B

| serie | V | periodo | n | media %/mes | DE | t IID | t NW(6) | IC95 NW %/mes | media x12 % (no es CAGR) | compuesto anual % (serie L-C; no es rendimiento de cuenta) | peor mes | mejor mes | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B:Emerging | V1 | 2000-01–2026-08 | 320 | 0.799 | 3.10 | 4.60 | 4.21 | [0.427, 1.170] | 9.58 | 9.37 | -16.84 (2026-07) | 12.84 (2026-04) | apoyo |
| B:Emerging | V2 | 2010-01–2026-08 | 200 | 1.024 | 3.02 | 4.79 | 5.48 | [0.658, 1.390] | 12.29 | 12.39 | -16.84 (2026-07) | 12.84 (2026-04) | apoyo |
| B:Emerging | V3 | 2016-01–2025-12 | 120 | 0.860 | 2.52 | 3.74 | 3.76 | [0.412, 1.309] | 10.32 | 10.41 | -9.15 (2022-11) | 7.02 (2021-01) | apoyo |
| B:Developed_ex_US | V1 | 2000-01–2026-08 | 320 | 0.583 | 3.51 | 2.97 | 2.58 | [0.140, 1.026] | 7.00 | 6.42 | -22.52 (2009-04) | 10.05 (2000-02) | apoyo |
| B:Developed_ex_US | V2 | 2010-01–2026-08 | 200 | 0.707 | 2.73 | 3.67 | 4.21 | [0.378, 1.036] | 8.49 | 8.34 | -12.31 (2020-11) | 7.21 (2020-03) | apoyo |
| B:Developed_ex_US | V3 | 2016-01–2025-12 | 120 | 0.478 | 2.57 | 2.04 | 2.26 | [0.064, 0.892] | 5.74 | 5.47 | -12.31 (2020-11) | 7.21 (2020-03) | apoyo |
| B:Europe | V1 | 2000-01–2026-08 | 320 | 0.749 | 4.08 | 3.28 | 3.05 | [0.267, 1.230] | 8.98 | 8.24 | -26.09 (2009-04) | 13.65 (2002-09) | apoyo |
| B:Europe | V2 | 2010-01–2026-08 | 200 | 0.850 | 3.08 | 3.90 | 4.77 | [0.501, 1.199] | 10.20 | 10.06 | -18.39 (2020-11) | 8.93 (2012-04) | apoyo |
| B:Europe | V3 | 2016-01–2025-12 | 120 | 0.617 | 3.08 | 2.20 | 2.69 | [0.168, 1.067] | 7.41 | 7.04 | -18.39 (2020-11) | 8.49 (2019-05) | apoyo |
| B:Asia_Pacific_ex_Japan | V1 | 2000-01–2026-08 | 320 | 0.888 | 3.51 | 4.53 | 3.65 | [0.412, 1.364] | 10.66 | 10.37 | -18.02 (2009-05) | 7.99 (2013-04) | apoyo |
| B:Asia_Pacific_ex_Japan | V2 | 2010-01–2026-08 | 200 | 1.039 | 3.05 | 4.82 | 4.99 | [0.631, 1.447] | 12.47 | 12.59 | -8.38 (2020-11) | 7.99 (2013-04) | apoyo |
| B:Asia_Pacific_ex_Japan | V3 | 2016-01–2025-12 | 120 | 0.750 | 2.86 | 2.88 | 3.41 | [0.319, 1.182] | 9.01 | 8.86 | -8.38 (2020-11) | 7.63 (2020-07) | apoyo |
| B:Japan | V1 | 2000-01–2026-08 | 320 | -0.021 | 3.96 | -0.09 | -0.09 | [-0.481, 0.439] | -0.25 | -1.20 | -18.27 (2026-07) | 14.79 (2000-02) | inconcluso |
| B:Japan | V2 | 2010-01–2026-08 | 200 | 0.082 | 3.40 | 0.34 | 0.39 | [-0.324, 0.487] | 0.98 | 0.28 | -18.27 (2026-07) | 14.29 (2026-04) | inconcluso |
| B:Japan | V3 | 2016-01–2025-12 | 120 | -0.090 | 2.89 | -0.34 | -0.37 | [-0.570, 0.390] | -1.08 | -1.57 | -8.49 (2016-08) | 8.43 (2016-06) | inconcluso |
| B:North_America | V1 | 2000-01–2026-08 | 320 | 0.247 | 4.92 | 0.90 | 1.00 | [-0.240, 0.734] | 2.97 | 1.50 | -25.00 (2009-04) | 29.32 (2000-02) | inconcluso |
| B:North_America | V2 | 2010-01–2026-08 | 200 | 0.348 | 3.29 | 1.50 | 1.74 | [-0.044, 0.740] | 4.17 | 3.58 | -12.97 (2026-07) | 11.36 (2026-04) | inconcluso |
| B:North_America | V3 | 2016-01–2025-12 | 120 | 0.165 | 3.32 | 0.54 | 0.58 | [-0.389, 0.718] | 1.98 | 1.32 | -12.72 (2023-01) | 6.95 (2020-03) | inconcluso |

#### Fuente C — agregados AQR y comparables directos

| serie | V | periodo | n | media %/mes | DE | t IID | t NW(6) | IC95 NW %/mes | media x12 % (no es CAGR) | compuesto anual % (serie L-C; no es rendimiento de cuenta) | peor mes | mejor mes | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C:Global Ex USA | V1 | 2000-01–2026-07 | 319 | 0.838 | 3.61 | 4.15 | 3.50 | [0.369, 1.308] | 10.06 | 9.66 | -23.53 (2009-04) | 11.09 (2000-02) | apoyo |
| C:Global Ex USA | V2 | 2010-01–2026-07 | 199 | 0.953 | 2.64 | 5.10 | 5.82 | [0.632, 1.274] | 11.43 | 11.59 | -12.06 (2020-11) | 6.92 (2019-05) | apoyo |
| C:Global Ex USA | V3 | 2016-01–2025-12 | 120 | 0.721 | 2.57 | 3.07 | 3.50 | [0.317, 1.126] | 8.66 | 8.58 | -12.06 (2020-11) | 6.92 (2019-05) | apoyo |
| C:Europe | V1 | 2000-01–2026-07 | 319 | 1.006 | 4.22 | 4.26 | 3.85 | [0.494, 1.519] | 12.08 | 11.53 | -27.06 (2009-04) | 14.62 (2002-09) | apoyo |
| C:Europe | V2 | 2010-01–2026-07 | 199 | 1.123 | 2.93 | 5.41 | 6.66 | [0.792, 1.454] | 13.48 | 13.74 | -18.88 (2020-11) | 8.61 (2019-05) | apoyo |
| C:Europe | V3 | 2016-01–2025-12 | 120 | 0.855 | 2.99 | 3.13 | 3.98 | [0.433, 1.276] | 10.25 | 10.14 | -18.88 (2020-11) | 8.61 (2019-05) | apoyo |
| C:Pacific | V1 | 2000-01–2026-07 | 319 | 0.485 | 3.39 | 2.55 | 2.14 | [0.040, 0.929] | 5.81 | 5.23 | -17.47 (2009-04) | 11.42 (2000-02) | apoyo |
| C:Pacific | V2 | 2010-01–2026-07 | 199 | 0.617 | 2.78 | 3.13 | 3.38 | [0.260, 0.974] | 7.40 | 7.16 | -10.74 (2026-07) | 8.36 (2026-04) | apoyo |
| C:Pacific | V3 | 2016-01–2025-12 | 120 | 0.454 | 2.54 | 1.96 | 2.07 | [0.024, 0.883] | 5.44 | 5.18 | -7.46 (2024-09) | 7.84 (2024-01) | apoyo |
| C:JPN | V1 | 2000-01–2026-07 | 319 | 0.087 | 3.85 | 0.40 | 0.37 | [-0.369, 0.543] | 1.04 | 0.14 | -17.49 (2009-04) | 11.92 (2004-03) | inconcluso |
| C:JPN | V2 | 2010-01–2026-07 | 199 | 0.114 | 3.23 | 0.50 | 0.57 | [-0.278, 0.507] | 1.37 | 0.74 | -14.41 (2026-07) | 11.55 (2026-04) | inconcluso |
| C:JPN | V3 | 2016-01–2025-12 | 120 | -0.056 | 2.91 | -0.21 | -0.22 | [-0.544, 0.432] | -0.67 | -1.17 | -8.76 (2021-02) | 8.72 (2016-06) | inconcluso |
| C:North America | V1 | 2000-01–2026-07 | 319 | 0.343 | 5.01 | 1.22 | 1.22 | [-0.207, 0.893] | 4.12 | 2.54 | -34.16 (2009-04) | 16.65 (2000-02) | inconcluso |
| C:North America | V2 | 2010-01–2026-07 | 199 | 0.460 | 3.70 | 1.76 | 2.01 | [0.010, 0.909] | 5.52 | 4.78 | -16.88 (2020-11) | 10.77 (2015-07) | apoyo |
| C:North America | V3 | 2016-01–2025-12 | 120 | 0.110 | 3.89 | 0.31 | 0.35 | [-0.514, 0.734] | 1.32 | 0.39 | -16.88 (2020-11) | 8.48 (2019-05) | inconcluso |
| C:USA | V1 | 2000-01–2026-07 | 319 | 0.275 | 5.05 | 0.97 | 0.98 | [-0.272, 0.822] | 3.30 | 1.68 | -34.62 (2009-04) | 17.01 (2000-02) | inconcluso |
| C:USA | V2 | 2010-01–2026-07 | 199 | 0.386 | 3.70 | 1.47 | 1.69 | [-0.062, 0.833] | 4.63 | 3.86 | -16.77 (2020-11) | 10.40 (2015-07) | inconcluso |
| C:USA | V3 | 2016-01–2025-12 | 120 | 0.052 | 3.90 | 0.15 | 0.17 | [-0.570, 0.675] | 0.63 | -0.30 | -16.77 (2020-11) | 8.48 (2019-05) | inconcluso |
| C:CAN | V1 | 2000-01–2026-07 | 319 | 1.320 | 5.85 | 4.03 | 3.44 | [0.568, 2.072] | 15.84 | 14.63 | -29.32 (2009-04) | 22.57 (2001-02) | apoyo |
| C:CAN | V2 | 2010-01–2026-07 | 199 | 1.453 | 5.18 | 3.96 | 3.89 | [0.720, 2.186] | 17.44 | 17.02 | -19.00 (2020-11) | 16.05 (2015-07) | apoyo |
| C:CAN | V3 | 2016-01–2025-12 | 120 | 1.116 | 4.96 | 2.46 | 2.26 | [0.149, 2.083] | 13.39 | 12.56 | -19.00 (2020-11) | 12.76 (2020-03) | apoyo |
| C:Global | V1 | 2000-01–2026-07 | 319 | 0.551 | 4.17 | 2.36 | 2.24 | [0.069, 1.033] | 6.61 | 5.66 | -28.48 (2009-04) | 14.16 (2000-02) | apoyo |
| C:Global | V2 | 2010-01–2026-07 | 199 | 0.649 | 3.08 | 2.97 | 3.46 | [0.282, 1.016] | 7.78 | 7.45 | -14.72 (2020-11) | 7.77 (2019-05) | apoyo |
| C:Global | V3 | 2016-01–2025-12 | 120 | 0.337 | 3.18 | 1.16 | 1.32 | [-0.162, 0.837] | 4.05 | 3.48 | -14.72 (2020-11) | 7.77 (2019-05) | inconcluso |

#### Fuente C — paises AQR

| serie | V | periodo | n | media %/mes | DE | t IID | t NW(6) | IC95 NW %/mes | media x12 % (no es CAGR) | compuesto anual % (serie L-C; no es rendimiento de cuenta) | peor mes | mejor mes | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C:AUS | V1 | 2000-01–2026-07 | 319 | 1.449 | 4.31 | 6.01 | 5.44 | [0.927, 1.971] | 17.39 | 17.54 | -17.19 (2000-04) | 14.79 (2013-04) | apoyo |
| C:AUS | V2 | 2010-01–2026-07 | 199 | 1.383 | 3.79 | 5.14 | 5.88 | [0.922, 1.843] | 16.59 | 16.92 | -13.48 (2020-11) | 14.79 (2013-04) | apoyo |
| C:AUS | V3 | 2016-01–2025-12 | 120 | 0.953 | 3.38 | 3.09 | 4.86 | [0.568, 1.338] | 11.44 | 11.30 | -13.48 (2020-11) | 9.28 (2020-03) | apoyo |
| C:AUT | V1 | 2000-01–2026-07 | 319 | 0.571 | 5.76 | 1.77 | 1.40 | [-0.230, 1.372] | 6.85 | 4.81 | -39.69 (2009-04) | 21.56 (2008-11) | inconcluso |
| C:AUT | V2 | 2010-01–2026-07 | 199 | 0.625 | 4.87 | 1.81 | 1.56 | [-0.160, 1.409] | 7.50 | 6.23 | -23.06 (2020-11) | 16.10 (2026-05) | inconcluso |
| C:AUT | V3 | 2016-01–2025-12 | 120 | -0.017 | 4.53 | -0.04 | -0.04 | [-0.944, 0.909] | -0.21 | -1.47 | -23.06 (2020-11) | 7.69 (2025-05) | inconcluso |
| C:BEL | V1 | 2000-01–2026-07 | 319 | 0.735 | 5.14 | 2.56 | 2.25 | [0.096, 1.375] | 8.83 | 7.42 | -30.98 (2009-04) | 19.34 (2008-10) | apoyo |
| C:BEL | V2 | 2010-01–2026-07 | 199 | 0.613 | 4.26 | 2.03 | 2.36 | [0.105, 1.122] | 7.36 | 6.44 | -19.03 (2020-11) | 12.80 (2012-04) | apoyo |
| C:BEL | V3 | 2016-01–2025-12 | 120 | 0.343 | 4.05 | 0.93 | 0.95 | [-0.366, 1.051] | 4.11 | 3.15 | -19.03 (2020-11) | 12.58 (2018-01) | inconcluso |
| C:CHE | V1 | 2000-01–2026-07 | 319 | 0.780 | 4.68 | 2.98 | 2.94 | [0.260, 1.300] | 9.36 | 8.32 | -25.28 (2009-04) | 22.69 (2001-09) | apoyo |
| C:CHE | V2 | 2010-01–2026-07 | 199 | 0.722 | 3.38 | 3.02 | 3.93 | [0.361, 1.082] | 8.66 | 8.27 | -16.67 (2020-11) | 9.47 (2020-03) | apoyo |
| C:CHE | V3 | 2016-01–2025-12 | 120 | 0.516 | 3.51 | 1.61 | 2.12 | [0.040, 0.993] | 6.19 | 5.58 | -16.67 (2020-11) | 9.47 (2020-03) | apoyo |
| C:DEU | V1 | 2000-01–2026-07 | 319 | 1.425 | 5.59 | 4.56 | 4.33 | [0.780, 2.071] | 17.10 | 16.30 | -23.21 (2009-08) | 26.89 (2008-10) | apoyo |
| C:DEU | V2 | 2010-01–2026-07 | 199 | 1.399 | 3.53 | 5.60 | 5.86 | [0.931, 1.866] | 16.79 | 17.27 | -15.15 (2020-11) | 11.29 (2026-01) | apoyo |
| C:DEU | V3 | 2016-01–2025-12 | 120 | 0.958 | 3.66 | 2.87 | 3.38 | [0.402, 1.515] | 11.50 | 11.23 | -15.15 (2020-11) | 11.13 (2019-05) | apoyo |
| C:DNK | V1 | 2000-01–2026-07 | 319 | 1.441 | 4.93 | 5.22 | 5.19 | [0.897, 1.986] | 17.30 | 17.03 | -22.25 (2009-04) | 14.15 (2022-04) | apoyo |
| C:DNK | V2 | 2010-01–2026-07 | 199 | 1.554 | 4.65 | 4.71 | 5.09 | [0.956, 2.152] | 18.65 | 18.82 | -14.63 (2022-05) | 14.15 (2022-04) | apoyo |
| C:DNK | V3 | 2016-01–2025-12 | 120 | 1.293 | 5.00 | 2.83 | 2.98 | [0.442, 2.144] | 15.51 | 14.97 | -14.63 (2022-05) | 14.15 (2022-04) | apoyo |
| C:ESP | V1 | 2000-01–2026-07 | 319 | 0.825 | 5.33 | 2.76 | 2.68 | [0.221, 1.428] | 9.90 | 8.42 | -28.87 (2020-11) | 14.89 (2020-07) | apoyo |
| C:ESP | V2 | 2010-01–2026-07 | 199 | 1.166 | 5.30 | 3.10 | 3.03 | [0.411, 1.920] | 13.99 | 12.96 | -28.87 (2020-11) | 14.89 (2020-07) | apoyo |
| C:ESP | V3 | 2016-01–2025-12 | 120 | 0.854 | 4.91 | 1.91 | 1.87 | [-0.040, 1.748] | 10.25 | 9.09 | -28.87 (2020-11) | 14.89 (2020-07) | inconcluso |
| C:FIN | V1 | 2000-01–2026-07 | 319 | 0.858 | 5.27 | 2.91 | 3.29 | [0.347, 1.370] | 10.30 | 9.00 | -19.06 (2001-10) | 26.09 (2001-08) | apoyo |
| C:FIN | V2 | 2010-01–2026-07 | 199 | 0.883 | 3.86 | 3.23 | 3.50 | [0.389, 1.378] | 10.60 | 10.16 | -10.09 (2026-07) | 13.10 (2012-04) | apoyo |
| C:FIN | V3 | 2016-01–2025-12 | 120 | 0.543 | 3.30 | 1.80 | 2.33 | [0.086, 1.000] | 6.51 | 6.03 | -8.20 (2025-07) | 11.84 (2019-05) | apoyo |
| C:FRA | V1 | 2000-01–2026-07 | 319 | 0.887 | 4.90 | 3.23 | 3.25 | [0.352, 1.421] | 10.64 | 9.56 | -26.67 (2009-04) | 20.66 (2002-09) | apoyo |
| C:FRA | V2 | 2010-01–2026-07 | 199 | 0.935 | 3.40 | 3.88 | 5.41 | [0.596, 1.274] | 11.22 | 11.03 | -21.28 (2020-11) | 8.00 (2019-05) | apoyo |
| C:FRA | V3 | 2016-01–2025-12 | 120 | 0.814 | 3.59 | 2.48 | 3.53 | [0.362, 1.266] | 9.76 | 9.34 | -21.28 (2020-11) | 8.00 (2019-05) | apoyo |
| C:GBR | V1 | 2000-01–2026-07 | 319 | 1.016 | 5.00 | 3.63 | 3.08 | [0.370, 1.662] | 12.19 | 11.11 | -34.19 (2009-04) | 12.46 (2000-02) | apoyo |
| C:GBR | V2 | 2010-01–2026-07 | 199 | 1.171 | 3.89 | 4.25 | 4.23 | [0.628, 1.714] | 14.06 | 13.92 | -26.21 (2020-11) | 10.85 (2020-07) | apoyo |
| C:GBR | V3 | 2016-01–2025-12 | 120 | 0.755 | 3.99 | 2.07 | 2.12 | [0.057, 1.453] | 9.06 | 8.34 | -26.21 (2020-11) | 10.85 (2020-07) | apoyo |
| C:GRC | V1 | 2000-01–2026-07 | 319 | 0.518 | 7.50 | 1.23 | 1.21 | [-0.321, 1.358] | 6.22 | 2.65 | -35.93 (2012-01) | 35.15 (2015-08) | inconcluso |
| C:GRC | V2 | 2010-01–2026-07 | 199 | 0.759 | 7.97 | 1.34 | 1.42 | [-0.289, 1.807] | 9.11 | 5.24 | -35.93 (2012-01) | 35.15 (2015-08) | inconcluso |
| C:GRC | V3 | 2016-01–2025-12 | 120 | 0.046 | 5.53 | 0.09 | 0.09 | [-0.930, 1.021] | 0.55 | -1.34 | -25.06 (2020-11) | 17.45 (2016-06) | inconcluso |
| C:HKG | V1 | 2000-01–2026-07 | 319 | 0.802 | 5.46 | 2.62 | 2.48 | [0.169, 1.435] | 9.63 | 8.02 | -28.43 (2009-05) | 20.72 (2000-02) | apoyo |
| C:HKG | V2 | 2010-01–2026-07 | 199 | 0.927 | 4.67 | 2.80 | 3.35 | [0.385, 1.470] | 11.13 | 10.22 | -22.09 (2024-09) | 12.07 (2024-01) | apoyo |
| C:HKG | V3 | 2016-01–2025-12 | 120 | 0.870 | 4.85 | 1.96 | 2.47 | [0.179, 1.561] | 10.44 | 9.34 | -22.09 (2024-09) | 12.07 (2024-01) | apoyo |
| C:IRL | V1 | 2000-01–2026-07 | 319 | 0.713 | 10.56 | 1.21 | 1.20 | [-0.453, 1.878] | 8.55 | 0.96 | -59.46 (2011-10) | 37.56 (2009-02) | inconcluso |
| C:IRL | V2 | 2010-01–2026-07 | 199 | 0.742 | 9.73 | 1.07 | 1.22 | [-0.452, 1.935] | 8.90 | 2.29 | -59.46 (2011-10) | 30.76 (2014-01) | inconcluso |
| C:IRL | V3 | 2016-01–2025-12 | 120 | -0.234 | 7.13 | -0.36 | -0.45 | [-1.263, 0.795] | -2.81 | -5.82 | -28.51 (2020-11) | 20.41 (2016-05) | inconcluso |
| C:ISR | V1 | 2000-01–2026-07 | 319 | 1.373 | 4.85 | 5.05 | 4.64 | [0.793, 1.952] | 16.47 | 16.10 | -24.66 (2009-04) | 13.00 (2008-06) | apoyo |
| C:ISR | V2 | 2010-01–2026-07 | 199 | 1.612 | 4.31 | 5.27 | 4.91 | [0.968, 2.255] | 19.34 | 19.82 | -18.62 (2020-11) | 12.10 (2017-08) | apoyo |
| C:ISR | V3 | 2016-01–2025-12 | 120 | 1.426 | 4.12 | 3.79 | 3.24 | [0.563, 2.289] | 17.11 | 17.33 | -18.62 (2020-11) | 12.10 (2017-08) | apoyo |
| C:ITA | V1 | 2000-01–2026-07 | 319 | 1.009 | 5.06 | 3.56 | 3.59 | [0.459, 1.560] | 12.11 | 11.09 | -21.12 (2009-03) | 20.09 (2000-02) | apoyo |
| C:ITA | V2 | 2010-01–2026-07 | 199 | 1.351 | 4.46 | 4.28 | 5.22 | [0.844, 1.858] | 16.21 | 16.09 | -18.88 (2020-11) | 14.89 (2010-11) | apoyo |
| C:ITA | V3 | 2016-01–2025-12 | 120 | 1.530 | 4.36 | 3.84 | 4.44 | [0.855, 2.204] | 18.36 | 18.63 | -18.88 (2020-11) | 12.68 (2016-06) | apoyo |
| C:NLD | V1 | 2000-01–2026-07 | 319 | 0.486 | 5.72 | 1.52 | 1.49 | [-0.153, 1.125] | 5.83 | 3.87 | -31.17 (2009-04) | 17.88 (2013-02) | inconcluso |
| C:NLD | V2 | 2010-01–2026-07 | 199 | 0.645 | 4.93 | 1.85 | 1.96 | [-0.000, 1.291] | 7.74 | 6.46 | -21.39 (2020-11) | 17.88 (2013-02) | inconcluso |
| C:NLD | V3 | 2016-01–2025-12 | 120 | 0.618 | 4.88 | 1.39 | 1.34 | [-0.286, 1.523] | 7.42 | 6.12 | -21.39 (2020-11) | 12.00 (2019-05) | inconcluso |
| C:NOR | V1 | 2000-01–2026-07 | 319 | 1.553 | 5.63 | 4.92 | 4.79 | [0.918, 2.189] | 18.64 | 18.08 | -22.44 (2001-11) | 20.12 (2002-12) | apoyo |
| C:NOR | V2 | 2010-01–2026-07 | 199 | 1.480 | 4.68 | 4.46 | 4.18 | [0.786, 2.174] | 17.76 | 17.73 | -19.98 (2020-11) | 16.22 (2020-03) | apoyo |
| C:NOR | V3 | 2016-01–2025-12 | 120 | 1.527 | 4.63 | 3.61 | 3.34 | [0.632, 2.422] | 18.33 | 18.43 | -19.98 (2020-11) | 16.22 (2020-03) | apoyo |
| C:NZL | V1 | 2000-01–2026-07 | 319 | 1.240 | 3.52 | 6.29 | 6.66 | [0.875, 1.605] | 14.88 | 15.10 | -11.10 (2014-04) | 13.96 (2001-09) | apoyo |
| C:NZL | V2 | 2010-01–2026-07 | 199 | 1.299 | 3.52 | 5.21 | 5.54 | [0.840, 1.758] | 15.59 | 15.91 | -11.10 (2014-04) | 11.10 (2020-12) | apoyo |
| C:NZL | V3 | 2016-01–2025-12 | 120 | 1.247 | 3.74 | 3.65 | 4.30 | [0.679, 1.815] | 14.96 | 15.10 | -9.43 (2020-11) | 11.10 (2020-12) | apoyo |
| C:PRT | V1 | 2000-01–2026-07 | 319 | 0.972 | 6.13 | 2.83 | 3.03 | [0.342, 1.602] | 11.67 | 9.80 | -23.97 (2020-11) | 18.02 (2011-10) | apoyo |
| C:PRT | V2 | 2010-01–2026-07 | 199 | 1.086 | 6.48 | 2.37 | 2.67 | [0.289, 1.883] | 13.03 | 11.02 | -23.97 (2020-11) | 18.02 (2011-10) | apoyo |
| C:PRT | V3 | 2016-01–2025-12 | 120 | 0.595 | 6.61 | 0.98 | 1.22 | [-0.358, 1.547] | 7.13 | 4.57 | -23.97 (2020-11) | 16.38 (2020-03) | inconcluso |
| C:SGP | V1 | 2000-01–2026-07 | 319 | 0.851 | 4.34 | 3.50 | 3.01 | [0.297, 1.406] | 10.22 | 9.40 | -31.70 (2009-05) | 14.52 (2020-07) | apoyo |
| C:SGP | V2 | 2010-01–2026-07 | 199 | 1.027 | 3.24 | 4.47 | 5.36 | [0.652, 1.402] | 12.33 | 12.35 | -9.07 (2013-10) | 14.52 (2020-07) | apoyo |
| C:SGP | V3 | 2016-01–2025-12 | 120 | 0.907 | 3.22 | 3.09 | 3.94 | [0.456, 1.359] | 10.89 | 10.78 | -9.00 (2016-03) | 14.52 (2020-07) | apoyo |
| C:SWE | V1 | 2000-01–2026-07 | 319 | 1.057 | 5.79 | 3.26 | 3.26 | [0.421, 1.693] | 12.68 | 11.13 | -29.43 (2009-04) | 22.36 (2000-02) | apoyo |
| C:SWE | V2 | 2010-01–2026-07 | 199 | 1.205 | 3.27 | 5.19 | 6.99 | [0.868, 1.543] | 14.46 | 14.74 | -10.63 (2012-01) | 13.16 (2021-07) | apoyo |
| C:SWE | V3 | 2016-01–2025-12 | 120 | 1.000 | 3.38 | 3.25 | 4.77 | [0.589, 1.411] | 12.00 | 11.95 | -7.18 (2022-01) | 13.16 (2021-07) | apoyo |

V1 {'apoyo': 17, 'inconcluso': 4} ['AUT', 'GRC', 'IRL', 'NLD']
V2 {'apoyo': 17, 'inconcluso': 4} ['AUT', 'GRC', 'IRL', 'NLD']
V3 {'apoyo': 14, 'inconcluso': 7} ['AUT', 'BEL', 'ESP', 'GRC', 'IRL', 'NLD', 'PRT']

**Rango de fechas de la Tabla 2.** R98: pre = inicio a 1998-02; post = 1998-03 a 2026-08. AMP13: pre = inicio a 2013-06; post = 2013-07 a 2026-08. AMP09: post = 2009-04 a 2026-08. "inc." = inconcluso.

**Estados de mercado de la Tabla 3.** "Bajista" significa Mkt-RF regional acumulado en t−24 a t−1 < 0. En Emerging, los primeros 18 meses de WML no tienen estado.

### Veredicto sobre la afirmación recibida (regla del punto 5 del pre-registro)

| Parte | Criterio | Resultado | Cumple |
|---|---|---|---|
| A1a "9.6% anual desde 2000" | ±0.5 pp en W1 o W1b, con ×12 o CAGR | W1b ×12 = **9.59%**; W1b CAGR = 9.37%. W1 (2000–2025): ×12 = 8.97% y CAGR = 8.84%, fuera de tolerancia | Sí (solo con datos a ago-2026) |
| A1b "t muy alta" | t NW(6) ≥ 3 en W1 | t = **4.10** (IC95 de 0.39 a 1.10 %/mes). También pasa Bonferroni (\|t\| > 2.69) | Sí |
| A1c "12.3% desde 2010" | ±0.5 pp en W2 o W2b | W2b ×12 = **12.30%**; CAGR = 12.40%. W2 (2010–2025): ×12 = 11.40% y CAGR = 11.62%, fuera de tolerancia | Sí (solo con datos a ago-2026) |
| A2 "en otros desarrollados sigue funcionando" | Developed ex US con "apoyo" en W2 y en AMP13-post | W2: t = 4.27, apoyo. AMP13-post: t = 3.08, apoyo | Sí |

**Etiqueta según la regla pre-registrada: CONFIRMADA.** Las cifras de la afirmación salen exactas con la **media aritmética ×12** y datos **hasta agosto de 2026**. Antes de usarla hay que tomar en cuenta estos matices:

1. **La cifra depende de 8 meses muy volátiles de 2026.** WML emergente en 2026 (análisis descriptivo fuera del pre-registro):

   | Mes | ene | feb | mar | abr | may | jun | jul | ago |
   |---|---|---|---|---|---|---|---|---|
   | WML (%) | +8.02 | +5.53 | −5.03 | +12.84 | +9.58 | +0.36 | −16.84 | +8.02 |

   La media de esos 8 meses es 2.81% al mes. Con años completos, las cifras son 8.97% (2000–2025) y 11.40% (2010–2025). Siguen siendo altas y muy significativas, pero **no son 9.6% y 12.3%**.
2. **Es media ×12, no CAGR, y no es un rendimiento invertible.** WML es largo-corto, en USD, sin costos ni impuestos, y con rebalanceo mensual de miles de acciones en 24 países. En GBM no se puede ir en corto.
3. **"Otros desarrollados" es cierto solo en parte.** Hay apoyo en Developed ex US, Europe y Asia Pacific ex Japan. **Japón** no tiene momentum en ninguna ventana (t de −0.62 a 0.68), como reportan Fama y French (2012). **Norteamérica** es inconclusa desde 2000 y después de cada publicación. El factor **Developed global** (incluye EUA) es inconcluso en 2000–2025 y en AMP13-post. En W1, Developed ex US (t = 2.50) no pasa Bonferroni; Europe, Asia Pacific ex Japan y Emerging sí.

### Hipótesis del pre-registro

- **H1:** apoyo en W0 para 6 de 7 regiones. Japón es inconcluso.
- **H2 (decaimiento después de publicarse):** no es uniforme.
  - **Emerging** no decae: 0.79 → 0.94 %/mes alrededor de AMP13 y 0.76 → 1.02 fuera de la muestra de FF2012. Solo baja con el corte de Rouwenhorst (1998): 1.11 → 0.77, y sigue significativo.
  - **Europe** baja (0.94 → 0.72) y sigue significativo.
  - **Norteamérica** cae y deja de ser significativa: 0.63 → 0.31, t = 1.26. Es coherente con V01 (EUA).
  - **Asia Pacific ex Japan** sube.
- **H3 (Japón sin momentum):** consistente; inconcluso en las 12 ventanas.
- **Crash.** Todas las regiones tienen asimetría negativa, de −0.22 a −2.67.
  - **Peor mes en los desarrollados:** abril de 2009, de −22% a −26%, mientras el mercado subía de +10% a +14%.
  - **Peor mes de Emerging:** julio de 2026, −16.84% con el mercado en −4.2%. Le siguen mayo y abril de 2009 (−14.8% y −14.4%, con el mercado en +18% y +17%).
  - **Caídas máximas del factor:** −37% (Emerging) a −53% (Asia Pacific ex Japan).
  - **Correlación con el mercado:** negativa en todas las regiones. En W0 va de −0.12 (Emerging) a −0.34 (Europe), con betas de −0.07 a −0.27. En W1 va de −0.07 (Japan) a −0.45 (Europe).
  - **Estado bajista (Daniel y Moskowitz):** la beta se vuelve más negativa (Emerging −0.26; desarrollados de −0.33 a −0.57) y la media de WML es menor (Emerging 0.49 contra 1.11 %/mes). El riesgo es perder cuando el mercado rebota desde abajo.
- **Pierna larga académica (Tabla 4).** Solo en **Emerging** la cartera de grandes ganadoras le gana al mercado de forma significativa: 0.30 a 0.39 %/mes, o 3.6% a 4.7% ×12, con "apoyo" en las 4 ventanas. Eso es alrededor del 40% del largo-corto, antes de costos de rotación. En desarrollados, la pierna larga es inconclusa en casi todas las ventanas. Las excepciones son Europe W2 y Asia Pacific ex Japan W0, que apenas pasan.
- **H4 (ETFs).** **Inconclusa en los 10 pares y en todas las sensibilidades.**
  - **Emergentes:** EEMO quedó 1.32 pp al año por debajo de EEM en MXN neto (2016-04 a 2026-08). PIE quedó 0.79 pp por debajo desde 2008-02, con una caída máxima de −56.9% contra −40.3% de EEM.
  - **Desarrollados, en su historia completa:** IDMO (+2.05 a +2.81 pp), IMTM (+0.22 a +1.04) y PIZ (+0.50 a +1.07) quedaron arriba. PIZ contra VEA en la ventana común quedó en −0.17. IMOM quedó debajo (−2.20 a −3.03). Ninguna diferencia es significativa: la t va de −0.86 a 1.15, incluidas las sensibilidades.
  - **Exposición:** la beta de la diferencia contra WML de la región es de 0.28 a 0.61. Los ETFs sí toman exposición a momentum, pero diluida.
- **Periodo contra implementación (descriptivo, fuera del pre-registro).** En la misma ventana de 2016-04 a 2026-08, la pierna larga académica emergente le ganó al mercado por 0.46 %/mes (5.5% ×12, t = 2.33) y WML emergente pagó 12.7% ×12. En cambio, EEMO − EEM fue −0.05 %/mes y PIE − EEM +0.12 %/mes. La falta de ventaja de los ETFs **no se explica por un mal periodo para el momentum emergente**. Queda una brecha de implementación, cuyos componentes no se miden aquí:
  - La metodología del índice y su frecuencia de rebalanceo.
  - Las restricciones por país.
  - El gasto: 0.29% EEMO y 0.90% PIE, según buscadores; no verificado en Invesco.
  - Los costos internos.
- **Moneda.** El peso casi no cambió entre 2016-03 y 2026-08 (−1.2%). Entre 2008-01 y 2026-08 se depreció de 10.82 a 17.01 por dólar. Por eso PIE pasa de 3.49% de CAGR en USD bruto a 5.99% en MXN neto. La diferencia contra el comparable apenas cambia, porque ambos lados se convierten con el mismo tipo de cambio.

### SIC

Con el criterio pre-registrado, **ninguno de los 6 ETFs de momentum queda verificado como listado en el SIC**. Evidencia en `datos/verificacion_sic_2026-09-25.json`:

| Fuente | ETFs de momentum | EEM, EFA y VEA |
|---|---|---|
| Yahoo `.MX` | EEMO, IMTM, IDMO e IMOM responden 404. PIE.MX y PIZ.MX existen como símbolos de la bolsa MEX con el nombre antiguo ("POWERSHARES DWA …"), pero sin ningún precio | Tienen precios en MXN en 2026 |
| TradingView `BMV:<ticker>` | 404 en los 6 | Existen |
| Buscador oficial de la BMV | HTTP 500; no se pudo consultar | — |

Que no aparezcan en agregadores **no prueba** que no estén listados (ver `arena/investigacion/02-universo-sic-bmv-agresivo.md`, §3). Tampoco se verificó si GBM los ofrece por Trading USA.

### Desviaciones del pre-registro

| Fecha | Qué cambió | Por qué | ¿Invalida algo? |
|---|---|---|---|
| 2026-09-25 | PIE y PIZ empiezan en 2008-02, no en 2008-01 | Yahoo empieza el 2008-01-07, así que enero no es un mes completo | No: se pierde un mes |
| 2026-09-25 | Se agregó TradingView como evidencia adicional del SIC | El buscador oficial de la BMV devolvió HTTP 500 | No: el veredicto "no verificado" sale igual con el criterio original |
| 2026-09-25 | Se agregaron dos análisis descriptivos (WML emergente de 2026 y la ventana de los ETFs), marcados en `resultados.json` como `descriptivo_no_preregistrado` | Explican la sensibilidad de la afirmación y la brecha de implementación | No: no tienen veredicto. Las salidas pre-registradas son idénticas antes y después de agregarlos |
| 2026-09-25 | Los gastos de EEMO, PIE, PIZ, IDMO e IMOM vienen de buscadores. IMTM (0.30%, iShares), EEM (0.72%, iShares) y EFA (0.32%, iShares) sí se verificaron con el emisor | Invesco devolvió 406 y etfdb 403 | No: el gasto ya está en el precio y no entra en el cálculo |
| 2026-09-25 | La fecha SSRN de AMP (6-mar-2009) sale del resumen del buscador | SSRN devolvió 403 | Solo afecta a la ventana de sensibilidad AMP09 |

## Conclusiones permitidas

- **El factor académico de momentum emergente (WML, French, USD, largo-corto, sin costos) tiene media positiva y muy significativa.**
  - 1990–2026: 0.85 %/mes (t = 5.08).
  - 2000–2025: 0.75 %/mes (t = 4.10).
  - 2010–2025: 0.95 %/mes (t = 5.74).
  - Después de AMP (2013): 0.94 %/mes (t = 4.28).
  - La afirmación recibida se reproduce **exactamente** como media ×12 con datos hasta agosto de 2026: 9.59% y 12.30%.
- Con años completos, la cifra es **~9.0% (2000–2025) y ~11.4% (2010–2025)**. Esas son las cifras que conviene citar.
- El momentum académico **sí sigue funcionando fuera de EUA** en Developed ex US, Europe y Asia Pacific ex Japan, también después de 2013. **No funciona en Japón** en ningún periodo. En **Norteamérica** no hay evidencia desde 2000.
- El momentum tiene riesgo de *crash*: el peor mes de cada región va de −17% a −37%, caídas del factor de 37% a 53% y betas negativas que empeoran en mercados bajistas. En emergentes, el peor mes de 36 años fue **julio de 2026**.
- En versión solo compra y académica, **solo emergentes** conserva una ventaja significativa: ~3.6–4.7% al año sobre su mercado, antes de costos de rotación.
- Con los ETFs reales, **no hay evidencia estadística de que ninguno de los 6 le gane a su comparable**, en MXN y neto de costos de GBM. Los dos ETFs de momentum emergente (EEMO y PIE) **quedaron por debajo** de EEM en sus historias completas.

## Conclusiones que NO se sostienen

- Que "momentum en emergentes paga 9.6% al año" para un inversionista. Esa cifra es la media ×12 de un largo-corto académico en USD, sin costos, e incluye 8 meses extremos de 2026. No es un CAGR y no es operable en GBM.
- Que exista hoy una forma verificada de capturar momentum emergente desde el SIC. No hay listado verificado, y los dos ETFs que existen le rindieron menos a un inversionista en MXN que EEM.
- Que los ETFs de momentum desarrollado (IDMO, IMTM, PIZ) "le ganan" a EFA o VEA. Las diferencias positivas son inconclusas (t ≤ 1.15) y no están verificadas en el SIC.
- Que el momentum funcione "en todos los desarrollados". No funciona en Japón, y en Norteamérica no hay evidencia desde 2000.
- Que la ventaja académica vaya a seguir. Ninguna prueba aquí es un pronóstico, y el riesgo de *crash* es alto: el −16.8% de julio de 2026 es reciente.
- Que una media ×12 sea un CAGR, o que la riqueza de un factor largo-corto sea la de una cartera.

## Estado y siguientes pasos

- **Estado:**
  - **Replicado**, para el factor académico internacional y la afirmación numérica.
  - **Sin evidencia de ventaja**, para la versión operable con ETFs.
  - **Pendiente**, para el listado en el SIC.
- **Pendientes:**
  1. Confirmar en la app de GBM (Trading MX/SIC y Trading USA) si EEMO, PIE, IMTM, PIZ, IDMO o IMOM se pueden comprar, y con qué spread.
  2. Consultar el catálogo oficial de la BMV cuando el buscador responda.
  3. Verificar el gasto de EEMO, PIE, PIZ, IDMO e IMOM en los documentos del emisor.
  4. Medir la brecha de implementación del momentum emergente: índice S&P Momentum y Dorsey Wright contra la pierna larga de French.
  5. Doble ejecución independiente de este archivo por `auditor-de-replicas`. Las cifras clave ya se verificaron con un script aparte.
- **Corrida final:** 2026-09-25. El pre-registro está en `preregistro.md` (SHA-256 `2a9aa15f…`).
