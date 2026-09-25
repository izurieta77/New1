# V02. Momentum internacional: factor académico (WML) y ETFs operables

> Fase 0 (formación). No es recomendación de inversión.
> Estado: **Replicado** (factor académico: la cifra recibida se reproduce al centésimo, con matices). **Versión operable: sin evidencia de ventaja y sin listado en el SIC verificado.**
> Reproducir desde la raíz del repo: `python3 laboratorio/replicas/V02-momentum-internacional/reproducir.py`. No usa red: datos congelados en `datos/`, huellas en `SHA256SUMS.txt` y todas las pruebas en `variantes.csv` (154 filas).
> Doble ejecución independiente: `python3 laboratorio/replicas/V02-momentum-internacional/independiente.py` (código escrito desde cero, sin leer `reproducir.py`; salida en `independiente_resultados.json`).

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
- **Verificación independiente.** Un script aparte, sin `herramientas/`, con su propio lector de CSV y JSON y NW calculado con la suma doble completa de Bartlett, da las mismas cifras. Coinciden al tercer decimal en Emerging W1, W1b, W2 y W2b y en Developed ex US W2 y AMP13-post, y al peso en la riqueza final de IDMO, EFA, EEMO, EEM, IMTM y PIZ. *Nota del 2026-09-25: ese script no quedó guardado en el repositorio, así que esta frase no se puede verificar. La doble ejecución verificable es `independiente.py` (ver "Doble ejecución independiente (2026-09-25)").*


#### Tabla 1. WML por región (French, USD, largo-corto, sin costos)

| Región | Ventana | Periodo | n | Media %/mes | t IID | t NW(6) | IC95 NW %/mes | Media ×12 % (no es CAGR) | Compuesto anual % | Veredicto |
|---|---|---|---|---|---|---|---|---|---|---|
| Developed | W0 | 1990-11 a 2026-08 | 430 | 0.544 | 3.01 | 2.80 | [0.163, 0.924] | 6.52 | 5.81 | apoyo |
| Developed | W1 | 2000-01 a 2025-12 | 312 | 0.352 | 1.58 | 1.55 | [−0.094, 0.799] | 4.23 | 3.32 | inconcluso |
| Developed | W1b | 2000-01 a 2026-08 | 320 | 0.366 | 1.64 | 1.62 | [−0.077, 0.809] | 4.39 | 3.46 | inconcluso |
| Developed | W2 | 2010-01 a 2025-12 | 192 | 0.462 | 2.39 | 2.69 | [0.126, 0.797] | 5.54 | 5.23 | apoyo |
| Developed | W2b | 2010-01 a 2026-08 | 200 | 0.479 | 2.35 | 2.71 | [0.133, 0.825] | 5.75 | 5.37 | apoyo |
| Developed ex US | W0 | 1990-11 a 2026-08 | 430 | 0.662 | 4.03 | 3.46 | [0.287, 1.038] | 7.95 | 7.48 | apoyo |
| Developed ex US | W1 | 2000-01 a 2025-12 | 312 | 0.571 | 2.92 | 2.50 | [0.124, 1.018] | 6.85 | 6.29 | apoyo |
| Developed ex US | W1b | 2000-01 a 2026-08 | 320 | 0.584 | 2.98 | 2.59 | [0.141, 1.028] | 7.01 | 6.43 | apoyo |
| Developed ex US | W2 | 2010-01 a 2025-12 | 192 | 0.692 | 3.73 | 4.27 | [0.374, 1.010] | 8.30 | 8.20 | apoyo |
| Developed ex US | W2b | 2010-01 a 2026-08 | 200 | 0.708 | 3.67 | 4.22 | [0.379, 1.038] | 8.50 | 8.35 | apoyo |
| Europe | W0 | 1990-11 a 2026-08 | 430 | 0.858 | 4.68 | 4.27 | [0.464, 1.251] | 10.29 | 9.81 | apoyo |
| Europe | W1 | 2000-01 a 2025-12 | 312 | 0.746 | 3.22 | 2.99 | [0.257, 1.234] | 8.95 | 8.20 | apoyo |
| Europe | W1b | 2000-01 a 2026-08 | 320 | 0.749 | 3.28 | 3.05 | [0.267, 1.230] | 8.99 | 8.25 | apoyo |
| Europe | W2 | 2010-01 a 2025-12 | 192 | 0.849 | 3.87 | 4.84 | [0.505, 1.193] | 10.19 | 10.06 | apoyo |
| Europe | W2b | 2010-01 a 2026-08 | 200 | 0.851 | 3.90 | 4.77 | [0.501, 1.200] | 10.21 | 10.06 | apoyo |
| Japan | W0 | 1990-11 a 2026-08 | 430 | 0.082 | 0.40 | 0.37 | [−0.351, 0.515] | 0.98 | −0.13 | inconcluso |
| Japan | W1 | 2000-01 a 2025-12 | 312 | −0.043 | −0.20 | −0.18 | [−0.500, 0.415] | −0.51 | −1.35 | inconcluso |
| Japan | W1b | 2000-01 a 2026-08 | 320 | −0.020 | −0.09 | −0.09 | [−0.481, 0.440] | −0.24 | −1.19 | inconcluso |
| Japan | W2 | 2010-01 a 2025-12 | 192 | 0.050 | 0.24 | 0.26 | [−0.330, 0.430] | 0.60 | 0.08 | inconcluso |
| Japan | W2b | 2010-01 a 2026-08 | 200 | 0.082 | 0.34 | 0.40 | [−0.324, 0.488] | 0.98 | 0.28 | inconcluso |
| Asia Pacific ex Japan | W0 | 1990-11 a 2026-08 | 430 | 0.853 | 4.26 | 3.99 | [0.434, 1.272] | 10.24 | 9.51 | apoyo |
| Asia Pacific ex Japan | W1 | 2000-01 a 2025-12 | 312 | 0.882 | 4.50 | 3.56 | [0.396, 1.367] | 10.58 | 10.30 | apoyo |
| Asia Pacific ex Japan | W1b | 2000-01 a 2026-08 | 320 | 0.889 | 4.53 | 3.66 | [0.413, 1.365] | 10.67 | 10.38 | apoyo |
| Asia Pacific ex Japan | W2 | 2010-01 a 2025-12 | 192 | 1.034 | 4.88 | 4.86 | [0.617, 1.452] | 12.41 | 12.57 | apoyo |
| Asia Pacific ex Japan | W2b | 2010-01 a 2026-08 | 200 | 1.040 | 4.82 | 4.99 | [0.631, 1.448] | 12.48 | 12.60 | apoyo |
| North America | W0 | 1990-11 a 2026-08 | 430 | 0.514 | 2.33 | 2.30 | [0.075, 0.953] | 6.17 | 5.01 | apoyo |
| North America | W1 | 2000-01 a 2025-12 | 312 | 0.238 | 0.86 | 0.95 | [−0.253, 0.729] | 2.86 | 1.42 | inconcluso |
| North America | W1b | 2000-01 a 2026-08 | 320 | 0.248 | 0.90 | 1.00 | [−0.239, 0.735] | 2.97 | 1.51 | inconcluso |
| North America | W2 | 2010-01 a 2025-12 | 192 | 0.336 | 1.52 | 1.73 | [−0.045, 0.718] | 4.03 | 3.53 | inconcluso |
| North America | W2b | 2010-01 a 2026-08 | 200 | 0.348 | 1.50 | 1.74 | [−0.044, 0.740] | 4.18 | 3.58 | inconcluso |
| Emerging | W0 | 1990-01 a 2026-08 | 440 | 0.848 | 5.62 | 5.08 | [0.521, 1.176] | 10.18 | 10.00 | apoyo |
| Emerging | W1 | 2000-01 a 2025-12 | 312 | 0.747 | 4.77 | 4.10 | [0.390, 1.105] | 8.97 | 8.84 | apoyo |
| Emerging | W1b | 2000-01 a 2026-08 | 320 | 0.799 | 4.60 | 4.21 | [0.427, 1.171] | 9.59 | 9.37 | apoyo |
| Emerging | W2 | 2010-01 a 2025-12 | 192 | 0.950 | 5.42 | 5.74 | [0.626, 1.274] | 11.40 | 11.62 | apoyo |
| Emerging | W2b | 2010-01 a 2026-08 | 200 | 1.025 | 4.80 | 5.47 | [0.658, 1.391] | 12.30 | 12.40 | apoyo |

#### Tabla 2. Antes y después de cada publicación (media %/mes, con t NW(6) entre paréntesis)

| Región | R98 pre | R98 post | FF12 dentro | FF12 fuera | AMP13 pre | AMP13 post | AMP09 post |
|---|---|---|---|---|---|---|---|
| Developed | 0.69 (2.91) apoyo | 0.51 (2.14) apoyo | 0.62 (2.00) apoyo | 0.44 (2.35) apoyo | 0.63 (2.25) apoyo | 0.39 (1.87) inc. | 0.27 (1.07) inc. |
| Developed ex US | 0.58 (1.94) inc. | 0.68 (2.98) apoyo | 0.64 (2.08) apoyo | 0.69 (3.83) apoyo | 0.71 (2.50) apoyo | 0.59 (3.08) apoyo | 0.51 (2.13) apoyo |
| Europe | 1.02 (3.96) apoyo | 0.82 (3.35) apoyo | 0.91 (2.80) apoyo | 0.79 (4.27) apoyo | 0.94 (3.18) apoyo | 0.72 (3.55) apoyo | 0.63 (2.39) apoyo |
| Japan | −0.27 (−0.62) inc. | 0.17 (0.68) inc. | 0.08 (0.23) inc. | 0.08 (0.37) inc. | 0.14 (0.43) inc. | −0.02 (−0.08) inc. | −0.04 (−0.17) inc. |
| Asia Pacific ex Japan | 0.99 (3.09) apoyo | 0.82 (3.12) apoyo | 0.67 (2.01) apoyo | 1.09 (4.99) apoyo | 0.79 (2.54) apoyo | 0.96 (4.27) apoyo | 0.82 (2.97) apoyo |
| North America | 0.84 (2.97) apoyo | 0.43 (1.59) inc. | 0.66 (1.86) inc. | 0.32 (1.48) inc. | 0.63 (1.96) apoyo | 0.31 (1.26) inc. | 0.13 (0.49) inc. |
| Emerging | 1.11 (3.66) apoyo | 0.77 (3.95) apoyo | 0.76 (3.06) apoyo | 1.02 (5.09) apoyo | 0.79 (3.46) apoyo | 0.94 (4.28) apoyo | 0.85 (3.49) apoyo |

Solo Emerging, corte de Rouwenhorst (1999): R99 pre (inicio a 1999-08) 0.89 (2.62) apoyo; R99 post (1999-09 a 2026-08) 0.83 (4.42) apoyo.

#### Tabla 3. Riesgo de *crash* y relación con el mercado regional (W0, descriptivo)

| Región | Peor mes WML (Mkt-RF ese mes) | Caída máxima del factor (pico a valle) | Peor 12 meses (termina) | Asimetría | Corr / beta W0 | Corr / beta W1 | Beta bajista / normal | Media WML bajista / normal %/mes (n) |
|---|---|---|---|---|---|---|---|---|
| Developed | −24.26% en 2009-04 (11.41%) | −43.6% (2008-11 a 2009-09) | −42.3% (2009-11) | −0.96 | −0.22 / −0.20 | −0.32 / −0.28 | −0.53 / 0.02 | 0.02 / 0.67 (81 / 329) |
| Developed ex US | −22.52% en 2009-04 (12.38%) | −40.9% (2009-02 a 2009-09) | −38.8% (2009-11) | −1.05 | −0.27 / −0.20 | −0.36 / −0.26 | −0.42 / 0.02 | 0.31 / 0.82 (129 / 281) |
| Europe | −26.09% en 2009-04 (13.67%) | −45.6% (2009-02 a 2009-09) | −41.9% (2010-02) | −1.36 | −0.34 / −0.27 | −0.45 / −0.35 | −0.50 / −0.07 | 0.74 / 0.88 (118 / 292) |
| Japan | −19.83% en 1998-01 (10.55%) | −42.0% (2000-02 a 2012-02) | −39.0% (2001-02) | −0.50 | −0.13 / −0.11 | −0.07 / −0.06 | −0.33 / 0.26 | 0.05 / 0.12 (162 / 248) |
| Asia Pacific ex Japan | −36.77% en 1998-10 (18.07%) | −52.8% (1998-08 a 2000-11) | −48.0% (1999-08) | −2.67 | −0.17 / −0.12 | −0.10 / −0.06 | −0.43 / 0.10 | 0.36 / 1.04 (131 / 279) |
| North America | −25.00% en 2009-04 (10.49%) | −50.0% (2008-06 a 2009-09) | −46.0% (2009-11) | −0.22 | −0.14 / −0.15 | −0.25 / −0.27 | −0.57 / 0.04 | −0.58 / 0.74 (71 / 339) |
| Emerging | −16.84% en 2026-07 (−4.22%) | −37.3% (2008-11 a 2009-10) | −36.8% (2009-10) | −1.17 | −0.12 / −0.07 | −0.32 / −0.15 | −0.26 / 0.08 | 0.49 / 1.11 (155 / 267) |

Los 5 peores meses de cada región, con el Mkt-RF del mismo mes, están en `resultados.json` (`crash.<región>.peores_5`).

#### Tabla 4. Pierna larga académica: Big High − (Mkt-RF + RF), USD, sin costos (media %/mes, t NW(6) y veredicto)

| Región | W0 | W1 (2000-2025) | W2 (2010-2025) | AMP13 post | Media ×12 %, rango en las 4 ventanas |
|---|---|---|---|---|---|
| Developed | 0.15 (1.46) inc. | 0.02 (0.20) inc. | 0.10 (0.92) inc. | 0.10 (0.75) inc. | 0.3 a 1.8 |
| Developed ex US | 0.15 (1.48) inc. | 0.06 (0.51) inc. | 0.17 (1.79) inc. | 0.13 (1.11) inc. | 0.7 a 2.1 |
| Europe | 0.20 (1.91) inc. | 0.14 (1.07) inc. | 0.21 (2.05) apoyo | 0.15 (1.31) inc. | 1.6 a 2.5 |
| Japan | 0.07 (0.48) inc. | −0.10 (−0.76) inc. | −0.02 (−0.15) inc. | −0.02 (−0.16) inc. | −1.2 a 0.8 |
| Asia Pacific ex Japan | 0.24 (2.00) apoyo | 0.22 (1.62) inc. | 0.20 (1.36) inc. | 0.16 (0.89) inc. | 1.9 a 2.9 |
| North America | 0.18 (1.47) inc. | 0.05 (0.34) inc. | 0.07 (0.58) inc. | 0.11 (0.75) inc. | 0.5 a 2.2 |
| Emerging | 0.33 (3.74) apoyo | 0.30 (3.15) apoyo | 0.36 (3.36) apoyo | 0.39 (2.40) apoyo | 3.6 a 4.6 |

#### Tabla 5. ETFs: caso base, historia completa como momentum hasta 2026-08 (MXN neto de costos GBM; prueba en USD)

| Par | Periodo | n | CAGR MXN neto ETF / comparable % | Diferencia pp/año | Riqueza final de 20,000 MXN (ETF / comparable) | Vol. anual MXN % | Caída máx. MXN % | Dif. USD %/mes | t NW(6) | IC95 NW | Veredicto | Beta de la dif. contra WML |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EEMO − EEM | 2016-04 a 2026-08 | 125 | 7.49 / 8.81 | −1.32 | 42,447 / 48,192 | 18.3 / 15.0 | −41.2 / −38.2 | −0.046 | −0.18 | [−0.544, 0.452] | inconcluso | 0.61 |
| PIE − EEM | 2008-02 a 2026-08 | 223 | 5.99 / 6.78 | −0.79 | 58,950 / 67,648 | 18.5 / 16.3 | −56.9 / −40.3 | −0.020 | −0.10 | [−0.402, 0.363] | inconcluso | 0.34 |
| IMTM − EFA | 2015-02 a 2026-08 | 139 | 10.26 / 9.22 | 1.04 | 61,977 / 55,548 | 12.7 / 12.7 | −30.1 / −29.0 | 0.070 | 0.54 | [−0.183, 0.323] | inconcluso | 0.42 |
| IMTM − VEA | 2015-02 a 2026-08 | 139 | 10.26 / 10.04 | 0.22 | 61,977 / 60,560 | 12.7 / 13.0 | −30.1 / −29.4 | 0.001 | 0.00 | [−0.253, 0.254] | inconcluso | 0.37 |
| PIZ − EFA | 2008-02 a 2026-08 | 223 | 8.88 / 7.81 | 1.07 | 97,188 / 80,917 | 16.4 / 13.4 | −41.0 / −32.2 | 0.128 | 0.89 | [−0.153, 0.409] | inconcluso | 0.29 |
| PIZ − VEA | 2008-02 a 2026-08 | 223 | 8.88 / 8.38 | 0.50 | 97,188 / 89,220 | 16.4 / 13.6 | −41.0 / −32.0 | 0.079 | 0.56 | [−0.196, 0.354] | inconcluso | 0.28 |
| IDMO − EFA | 2016-04 a 2026-08 | 125 | 12.12 / 9.31 | 2.81 | 65,874 / 50,554 | 13.6 / 12.9 | −26.8 / −29.0 | 0.212 | 1.12 | [−0.158, 0.583] | inconcluso | 0.41 |
| IDMO − VEA | 2016-04 a 2026-08 | 125 | 12.12 / 10.08 | 2.05 | 65,874 / 54,374 | 13.6 / 13.2 | −26.8 / −29.4 | 0.146 | 0.76 | [−0.231, 0.523] | inconcluso | 0.35 |
| IMOM − EFA | 2016-01 a 2026-08 | 128 | 6.62 / 8.82 | −2.20 | 39,635 / 49,265 | 16.0 / 12.8 | −38.4 / −29.0 | −0.123 | −0.50 | [−0.611, 0.364] | inconcluso | 0.59 |
| IMOM − VEA | 2016-01 a 2026-08 | 128 | 6.62 / 9.65 | −3.03 | 39,635 / 53,423 | 16.0 / 13.2 | −38.4 / −29.4 | −0.195 | −0.86 | [−0.637, 0.248] | inconcluso | 0.54 |

Región de WML para la beta: Emerging en EEMO y PIE; Developed ex US en los demás.

**Sensibilidades (diferencia de CAGR MXN neto en pp/año; t NW(6) de la diferencia mensual en USD entre paréntesis).**

| Par | Base | Spread de 0.30% en el ETF de momentum | Retención de 30% sobre dividendos | Ventana común 2016-04 a 2026-08 |
|---|---|---|---|---|
| EEMO − EEM | −1.32 (−0.18) inc. | −1.35 (−0.18) inc. | −1.80 (−0.31) inc. | −1.32 (−0.18) inc. |
| PIE − EEM | −0.79 (−0.10) inc. | −0.81 (−0.10) inc. | −0.57 (−0.01) inc. | 1.16 (0.50) inc. |
| IMTM − EFA | 1.04 (0.54) inc. | 1.01 (0.54) inc. | 1.11 (0.58) inc. | 0.99 (0.50) inc. |
| IMTM − VEA | 0.22 (0.00) inc. | 0.19 (0.00) inc. | 0.33 (0.06) inc. | 0.22 (0.02) inc. |
| PIZ − EFA | 1.07 (0.89) inc. | 1.05 (0.89) inc. | 1.50 (1.13) inc. | 0.60 (0.44) inc. |
| PIZ − VEA | 0.50 (0.56) inc. | 0.48 (0.56) inc. | 0.95 (0.82) inc. | −0.17 (0.13) inc. |
| IDMO − EFA | 2.81 (1.12) inc. | 2.78 (1.12) inc. | 2.87 (1.15) inc. | 2.81 (1.12) inc. |
| IDMO − VEA | 2.05 (0.76) inc. | 2.01 (0.76) inc. | 2.13 (0.80) inc. | 2.05 (0.76) inc. |
| IMOM − EFA | −2.20 (−0.50) inc. | −2.23 (−0.50) inc. | −1.89 (−0.41) inc. | −1.86 (−0.37) inc. |
| IMOM − VEA | −3.03 (−0.86) inc. | −3.06 (−0.86) inc. | −2.69 (−0.76) inc. | −2.62 (−0.69) inc. |

Las tablas "Fuente A / B / C" (ventanas V1-V3 y series de AQR) pertenecen a la auditoría ciega [AC-03](../../auditorias/AC-03-momentum-internacional/README.md) y se consultan allá. Se habían pegado aquí por error; ver `conocimiento/registro-de-errores.md`.


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
  - **Emerging** no decae: 0.79 → 0.94 %/mes alrededor de AMP13 y 0.76 → 1.02 fuera de la muestra de FF2012. Baja con los dos cortes de Rouwenhorst: 1.11 → 0.77 (1998) y 0.89 → 0.83 (1999), y sigue significativo en ambos.
  - **Europe** baja alrededor de AMP13 (0.94 → 0.72) y sigue significativo.
  - **Norteamérica** cae alrededor de AMP13 y deja de ser significativa: 0.63 → 0.31, t = 1.26. Es coherente con V01 (EUA).
  - **Asia Pacific ex Japan** sube alrededor de AMP13 (0.79 → 0.96) y de FF2012 (0.67 → 1.09). Con el corte de Rouwenhorst (1998) baja (0.99 → 0.82) y sigue significativo.
- **H3 (Japón sin momentum):** consistente; inconcluso en las 12 ventanas.
- **Crash.** Todas las regiones tienen asimetría negativa, de −0.22 a −2.67.
  - **Peor mes en Developed, Developed ex US, Europe y North America:** abril de 2009, de −22.52% a −26.09%, mientras el mercado subía de +10.49% a +13.67%. En **Japan** el peor mes fue enero de 1998 (−19.83%, con el mercado en +10.55%) y en **Asia Pacific ex Japan**, octubre de 1998 (−36.77%, con el mercado en +18.07%).
  - **Peor mes de Emerging:** julio de 2026, −16.84% con el mercado en −4.2%. Le siguen mayo y abril de 2009 (−14.8% y −14.4%, con el mercado en +18% y +17%).
  - **Caídas máximas del factor:** −37% (Emerging) a −53% (Asia Pacific ex Japan).
  - **Correlación con el mercado:** negativa en todas las regiones. En W0 va de −0.12 (Emerging) a −0.34 (Europe), con betas de −0.07 a −0.27. En W1 va de −0.07 (Japan) a −0.45 (Europe).
  - **Estado bajista (Daniel y Moskowitz):** la beta se vuelve más negativa (Emerging −0.26; desarrollados de −0.33 a −0.57) y la media de WML es menor (Emerging 0.49 contra 1.11 %/mes). El riesgo es perder cuando el mercado rebota desde abajo.
- **Pierna larga académica (Tabla 4).** Solo en **Emerging** la cartera de grandes ganadoras le gana al mercado de forma significativa: 0.30 a 0.39 %/mes, o 3.6% a 4.6% ×12, con "apoyo" en las 4 ventanas. Eso es alrededor del 40% del largo-corto, antes de costos de rotación. En desarrollados, la pierna larga es inconclusa en casi todas las ventanas. Las excepciones son Europe W2 y Asia Pacific ex Japan W0, que apenas pasan.
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
- En versión solo compra y académica, **solo emergentes** conserva una ventaja significativa: ~3.6–4.6% al año sobre su mercado (media ×12), antes de costos de rotación.
- Con los ETFs reales, **no hay evidencia estadística de que ninguno de los 6 le gane a su comparable**, en MXN y neto de costos de GBM. Los dos ETFs de momentum emergente (EEMO y PIE) **quedaron por debajo** de EEM en sus historias completas.

## Conclusiones que NO se sostienen

- Que "momentum en emergentes paga 9.6% al año" para un inversionista. Esa cifra es la media ×12 de un largo-corto académico en USD, sin costos, e incluye 8 meses extremos de 2026. No es un CAGR y no es operable en GBM.
- Que exista hoy una forma verificada de capturar momentum emergente desde el SIC. No hay listado verificado, y los dos ETFs que existen le rindieron menos a un inversionista en MXN que EEM.
- Que los ETFs de momentum desarrollado (IDMO, IMTM, PIZ) "le ganan" a EFA o VEA. Las diferencias positivas son inconclusas (t ≤ 1.15) y no están verificadas en el SIC.
- Que el momentum funcione "en todos los desarrollados". No funciona en Japón, y en Norteamérica no hay evidencia desde 2000.
- Que la ventaja académica vaya a seguir. Ninguna prueba aquí es un pronóstico, y el riesgo de *crash* es alto: el −16.8% de julio de 2026 es reciente.
- Que una media ×12 sea un CAGR, o que la riqueza de un factor largo-corto sea la de una cartera.

## Doble ejecución independiente (2026-09-25)

**Qué se hizo.** El auditor de réplicas escribió `independiente.py` desde cero. Solo leyó el pre-registro y los datos congelados en `datos/`; no abrió `reproducir.py`. El script tiene su propio lector de los CSV de French (por bloques), del JSON de Yahoo y del CSV de FRED. Alinea por índice de mes y toma como fin de mes el último día con precio. Convierte a MXN y cobra los costos de GBM según el punto 8. Calcula el error estándar Newey-West(6) con dos fórmulas propias: la suma doble de Bartlett sobre pares (i, j) y las autocovarianzas ponderadas. Las dos coinciden entre sí y con `herramientas/estadistica.py` (diferencia máxima de 8.9e−16). `resultados.json` y `variantes.csv` se leyeron solo después de calcular todo, para el cotejo. Las 42 huellas de `datos/` coinciden con `SHA256SUMS.txt`, y la sección PRE-REGISTRO de este README es idéntica a `preregistro.md` (SHA-256 `2a9aa15f…`).

**Tolerancias.** 0.01 pp en medias mensuales, errores estándar e IC; 0.05 en t; 0.1 pp en CAGR, caídas máximas y medias ×12. Si el README publica una cifra con menos decimales, la tolerancia es media unidad del último decimal publicado. Por ejemplo, "−37%" admite ±0.5.

**Resumen de la comparación.**

| Qué se comparó | Cifras | Coinciden | Mayor diferencia |
|---|---|---|---|
| Cifras y afirmaciones propias de V02 en este README: datos, veredicto, hipótesis, SIC y conclusiones, con el texto ya corregido | 200 | 200 | Dentro de tolerancia (0.26 en "−37%", que admite ±0.5) |
| Las mismas afirmaciones en el texto **anterior** a la corrección (ver abajo) | 4 | 0 | — |
| Celdas de las tablas "Fuente A" y "Fuente B" de AC-03 que estaban pegadas aquí (French, V1-V3) | 540 | 540 | 0.005 (redondeo) |
| `resultados.json` de `reproducir.py`, cifra por cifra: WML 1,032; pierna larga 336; *crash* 154; mercado 98; ETFs 1,080; controles 40; descriptivos 28; afirmación 11; versiones 14 | 2,793 | 2,793 | 2.3e−14 en los estadísticos; 0.0008 pp en la media absoluta de un control de EFA |
| `variantes.csv` (154 filas completas) | 154 | 154 | 5e−7 (el CSV redondea a 6 decimales) |

Las tablas "Fuente C" (AQR) no se pueden cotejar con los datos de V02, porque aquí no están congeladas. Se verificaron en AC-03.

**Cifras clave: README contra ejecución independiente.**

| Cifra | README | Independiente | Diferencia | Tolerancia |
|---|---|---|---|---|
| Emerging W1b (2000-01 a 2026-08), media ×12 % | 9.59 | 9.5858 | −0.0042 | 0.1 |
| Emerging W1b, compuesto anual % | 9.37 | 9.3744 | 0.0044 | 0.1 |
| Emerging W1 (2000-2025), media ×12 % | 8.97 | 8.9669 | −0.0031 | 0.1 |
| Emerging W1, compuesto anual % | 8.84 | 8.8362 | −0.0038 | 0.1 |
| Emerging W1, t NW(6) | 4.10 | 4.0964 | −0.0036 | 0.05 |
| Emerging W1, IC95 inferior %/mes | 0.39 | 0.3897 | −0.0003 | 0.01 |
| Emerging W1, IC95 superior %/mes | 1.10 | 1.1048 | 0.0048 | 0.01 |
| Emerging W2b (2010-01 a 2026-08), media ×12 % | 12.30 | 12.2952 | −0.0048 | 0.1 |
| Emerging W2b, compuesto anual % | 12.40 | 12.3953 | −0.0047 | 0.1 |
| Emerging W2 (2010-2025), media ×12 % | 11.40 | 11.4025 | 0.0025 | 0.1 |
| Emerging W2, compuesto anual % | 11.62 | 11.6246 | 0.0046 | 0.1 |
| Emerging W2, t NW(6) | 5.74 | 5.7444 | 0.0044 | 0.05 |
| Emerging W0, media %/mes | 0.85 | 0.8484 | −0.0016 | 0.01 |
| Emerging W0, t NW(6) | 5.08 | 5.0762 | −0.0038 | 0.05 |
| Emerging AMP13 post, t NW(6) | 4.28 | 4.2816 | 0.0016 | 0.05 |
| Developed ex US W2, t NW(6) | 4.27 | 4.2697 | −0.0003 | 0.05 |
| Developed ex US AMP13 post, t NW(6) | 3.08 | 3.0813 | 0.0013 | 0.05 |
| Developed ex US W1, t NW(6) | 2.50 | 2.5046 | 0.0046 | 0.05 |
| Japan, t NW(6) mínima en 12 ventanas | −0.62 | −0.6164 | 0.0036 | 0.05 |
| Japan, t NW(6) máxima en 12 ventanas | 0.68 | 0.6757 | −0.0043 | 0.05 |
| North America AMP13 post, t NW(6) | 1.26 | 1.2608 | 0.0008 | 0.05 |
| WML Emerging ene-ago 2026, media %/mes | 2.81 | 2.8100 | 0.0000 | 0.01 |
| Caída máxima del factor, Emerging % | −37 | −37.2595 | −0.2595 | 0.5 |
| WML Emerging en estado bajista, media %/mes | 0.49 | 0.4922 | 0.0022 | 0.01 |
| Pierna larga Emerging 2016-04 a 2026-08, %/mes | 0.46 | 0.4561 | −0.0039 | 0.01 |
| Pierna larga Emerging 2016-04 a 2026-08, t NW(6) | 2.33 | 2.3344 | 0.0044 | 0.05 |
| EEMO − EEM, dif. CAGR MXN neto, pp/año | −1.32 | −1.3179 | 0.0021 | 0.1 |
| PIE − EEM, dif. CAGR MXN neto, pp/año | −0.79 | −0.7879 | 0.0021 | 0.1 |
| PIE, caída máxima MXN neta % | −56.9 | −56.8779 | 0.0221 | 0.1 |
| EEM (ventana de PIE), caída máxima MXN neta % | −40.3 | −40.3328 | −0.0328 | 0.1 |
| PIE, CAGR MXN neto % | 5.99 | 5.9893 | −0.0007 | 0.1 |
| PIZ − VEA ventana común, dif. CAGR pp/año | −0.17 | −0.1671 | 0.0029 | 0.1 |
| DEXMXUS fin de mes 2026-08 | 17.0081 | 17.0081 | 0.0000 | 5e-05 |
| DEXMXUS contra MXN=X, correlación | 0.982 | 0.9823 | 0.0003 | 0.0005 |
| t NW(6) de las diferencias de ETFs (pares, ventanas y sensibilidades), rango | −0.86 a 1.15 | −0.8621 a 1.1543 | −0.0021 / 0.0043 | 0.05 |
| Beta de la diferencia de ETFs contra WML, rango | 0.28 a 0.61 | 0.2751 a 0.6147 | −0.0049 / 0.0047 | 0.005 |

El detalle cifra por cifra está en `independiente_resultados.json`: `comparacion_readme`, `afirmaciones_anteriores_del_readme`, `comparacion_tablas_ac03`, `cotejo_resultados_json_original` y `cotejo_variantes_csv`.

**Diferencias encontradas y corrección.** Ninguna es de cálculo: todos los estadísticos, los veredictos y la etiqueta global se reproducen. Las diferencias estaban en el texto y en la estructura del README.

| # | Qué decía el README | Qué dan los datos | Causa | Corrección |
|---|---|---|---|---|
| 1 | Tablas "Fuente A / B / C" de AC-03 en lugar de las tablas propias de V02, que el texto cita como "Tabla 2", "Tabla 3" y "Tabla 4" | Las cifras de V02 estaban solo en `resultados.json` y `variantes.csv` | Pegado de otro archivo en el commit `44d5a61` (ya registrado como pendiente) | Se restauraron las Tablas 1 a 5 desde `resultados.json`, cotejado 2,793 de 2,793 contra la ejecución independiente. Las tablas de AC-03 quedan como enlace |
| 2 | "Peor mes en los desarrollados: abril de 2009, de −22% a −26%, mientras el mercado subía de +10% a +14%" | Solo es cierto en Developed, Developed ex US, Europe y North America (−22.52% a −26.09%). En Japan fue 1998-01 (−19.83%) y en Asia Pacific ex Japan 1998-10 (−36.77%). Además −22.52 no redondea a −22 | Se generalizó de 4 regiones a 6, y el extremo se truncó en vez de redondearse | Texto corregido en "Hipótesis del pre-registro" |
| 3 | Emerging: "Solo baja con el corte de Rouwenhorst (1998)" | También baja con el corte R99 pre-registrado: 0.89 → 0.83 %/mes, y sigue con "apoyo" | Se omitió el corte R99 | Texto corregido |
| 4 | "Europe baja (0.94 → 0.72)", "Norteamérica cae (0.63 → 0.31)" y "Asia Pacific ex Japan sube", sin decir el corte | Las cifras son del corte AMP13. Asia Pacific ex Japan sube con AMP13 y FF12, pero baja con R98 (0.99 → 0.82) | Se omitió qué corte se usaba | Texto corregido para nombrar el corte |
| 5 | Pierna larga emergente "3.6% a 4.7% ×12" | El máximo es 4.6496% | Doble redondeo (4.6496 → 4.65 → 4.7). Está dentro de la tolerancia | Corregido a "3.6% a 4.6%" en "Hipótesis" y en "Conclusiones permitidas" |
| 6 | "Un script aparte [...] da las mismas cifras" | Ese script no está en el repositorio | Afirmación sin evidencia guardada | Se agregó una nota. La doble ejecución verificable es `independiente.py` |

Las conclusiones permitidas y las que no se sostienen **no cambian**. La etiqueta de la regla pre-registrada sigue siendo "CONFIRMADA", con los mismos matices: la cifra se reproduce como media ×12 solo con fin en 2026-08, no es un CAGR y no es operable.

**Límites de esta doble ejecución.**

- Usa los mismos datos congelados y las mismas fuentes: French (base Bloomberg 202608), Yahoo y FRED. Confirma el cálculo, no los datos. La segunda fuente para WML es AC-03 (AQR), que no publica emergentes: **las cifras de emergentes siguen sin fuente independiente**.
- Donde el pre-registro deja margen, las elecciones del script independiente coincidieron con las del original (lo confirma el cotejo). Ninguna de las alternativas cambia un veredicto:
  - Estado bajista: Mkt-RF compuesto de t−24 a t−1. Con la suma simple, la beta bajista de Emerging pasa de −0.26 a −0.29 y la de los desarrollados queda entre −0.35 y −0.55.
  - Asimetría: se usa la poblacional (g1). La versión ajustada difiere en 0.01 o menos.
  - Volatilidad: se calcula con rendimientos mensuales en MXN sin costos. Con los costos, cambia 0.04 pp o menos.
  - Caída máxima: se mide desde los 20,000 MXN iniciales. Sin ese punto da lo mismo.
- No prueba nada sobre el listado en el SIC ni sobre los spreads reales en GBM. Esos siguen pendientes.

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
  5. ~~Doble ejecución independiente de este archivo por `auditor-de-replicas`.~~ Hecha el 2026-09-25 con `independiente.py`: ver la sección "Doble ejecución independiente (2026-09-25)".
- **Corrida final:** 2026-09-25. El pre-registro está en `preregistro.md` (SHA-256 `2a9aa15f…`).
