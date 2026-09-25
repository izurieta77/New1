# V02. Momentum internacional: factor académico (WML) y ETFs operables

> Fase 0 (formación). No es recomendación de inversión.
> Estado: **PRE-REGISTRO** (resultados pendientes).

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

## RESULTADOS

(Pendiente: se llena después de la corrida.)
