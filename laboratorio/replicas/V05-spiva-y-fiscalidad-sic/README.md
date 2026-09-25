# V05. SPIVA (EUA y México) y fiscalidad del SIC

> Fecha: 25-sep-2026. Estado: **Verificado con matices.** Las tres afirmaciones recibidas quedan como **confirmadas con matices**: las cifras existen en PDF oficiales de S&P DJI, pero no son las más recientes y dos etiquetas no corresponden exactamente. La parte fiscal está verificada contra ley, DOF, IRS y tratados (ver el capítulo [27](../../../conocimiento/27-fiscalidad-2026-y-estructura-sic.md)). Esto no es una estrategia ni una recomendación (fase 0).
>
> Para reproducir, desde la raíz del repo: `python3 laboratorio/replicas/V05-spiva-y-fiscalidad-sic/reproducir.py`. No usa red y solo usa la biblioteca estándar. Los PDF, los textos legales y los precios están congelados en `datos/`, con sus huellas y la del pre-registro en `SHA256SUMS.txt`. La salida es `resultados.json`. El script falla si cambia una huella, si no encuentra una cifra de SPIVA o si falta alguna de las 29 citas legales en los textos congelados.

## Resumen

1. **"85.6% de los fondos grandes de EUA debajo del S&P 500 a 10 años": confirmada con matices.** La cifra exacta es **85.59%**, de *All Large-Cap Funds* en el *SPIVA U.S. Scorecard Year-End 2025* (corte al 31-dic-2025, publicado en marzo de 2026). Pero **ya hay una edición más nueva**: la *Mid-Year 2026* (corte al 30-jun-2026, publicada hacia el 16-17 de septiembre de 2026) da **83.33%**. Además, "fondos grandes" en el reporte significa fondos que invierten en empresas grandes, no fondos con mucho dinero.
2. **"82.9% en México debajo de su índice a 10 años": confirmada con matices.** La cifra es **82.93%**, de *Mexico Equity Funds* en el *SPIVA Latin America Year-End 2024* (corte al 31-dic-2024, publicado en abril de 2025). El índice no es el IPC de precio, sino el **S&P/BMV IRT**, que es el IPC con dividendos. La edición siguiente (primer semestre de 2025, PDF oficial en español) da **73.17%**, y la de cierre de 2025 no se pudo descargar. **Trampa:** en la edición de mitad de 2025, **82.93% es la tasa de supervivencia** a 10 años (34 de 41 fondos), no la tasa de fondos que quedaron debajo del índice.
3. **"Los ganadores mexicanos tenían cartera muy distinta al índice y dinero en ETFs extranjeros": confirmada con matices.** S&P DJI lo documenta en la misma edición de cierre de 2024: el **cuartil superior** tenía en promedio **74.3%** en valores fuera del S&P/BMV IRT y **16.4%** en fondos indexados y ETFs extranjeros, casi todos de EUA y Europa (la gráfica dice 16.2%). Pero ese análisis es del **año 2024** (horizonte de 1 año), no de los fondos que ganaron a 10 años. Además, el peso fuera del índice es solo una cota inferior del *active share*, no el *active share* mismo.
4. **La mecánica explica mucho.** Con datos propios, de 2015 a 2024 el IPC (NAFTRAC con dividendos) rindió **3.53%** anual y el S&P 500 en pesos **16.98%**. Un fondo que solo ponía **10%** en el S&P 500 le ganaba al IPC por **1.45 pp** al año. Para cubrir 2 pp de gastos bastaba con **13.8%** en el S&P. En 2024, tener 16.4% en el S&P 500 daba **+8.7 pp** en un solo año (cálculo exploratorio). Conclusión: en SPIVA México, "ganarle al IPC" puede ser una apuesta de país y moneda, no talento para elegir acciones.
5. **Los fondos mexicanos que invierten afuera pierden más.** A 10 años al cierre de 2024, **86.67%** de los fondos mexicanos de acciones de EUA quedaron debajo del S&P 500 en pesos, y **100%** de los fondos globales en pesos quedaron debajo del S&P World en pesos. En promedio equiponderado, los fondos de EUA rindieron **12.65%** contra **17.08%** del índice, y los globales **7.09%** contra **14.33%**.
6. **Fiscalidad verificada en la ley.** El ISR es de **10% definitivo** sobre la ganancia neta anual en BMV y SIC (art. 129 LISR). Las pérdidas solo se restan de ganancias del mismo tipo, **en el mismo año o en los 10 siguientes**, y si no se restan cuando se puede, ese derecho se pierde. La retención sobre intereses en 2026 es **0.90%** anual sobre el capital (art. 24 LIF 2026, DOF 07-11-2025). Los dividendos extranjeros del SIC pagan retención en EUA (**30%**, o **10%** con W-8BEN por el tratado) y en México **10% adicional**, además de acumularse en la declaración anual (art. 142 fr. V). La LISR no se ha reformado desde el DOF del 01-04-2024.
7. **Impuesto sucesorio de EUA (*estate tax*).** Un no residente paga sobre sus activos situados en EUA arriba de **60,000 USD** de umbral (crédito de **13,000 USD**), con tasa marginal de hasta **40%**. **México no tiene tratado sucesorio con EUA**: no aparece en la lista de 15 países de las instrucciones del Form 706-NA. Para el IRS, las acciones de sociedades de EUA están situadas en EUA **"sin importar dónde estén físicamente los certificados"**. No encontré ninguna resolución del IRS ni de un tribunal sobre el SIC o Indeval, así que **no hay certeza formal**. La lectura dominante es que la custodia vía Indeval no cambia el *situs*.
8. **Los ETFs UCITS de Irlanda sí están en el SIC y algunos son líquidos.** **CSPX** (iShares Core S&P 500, Irlanda, acumulación, TER 0.07%) se negocia en 249 de 252 sesiones, con mediana de **47 millones de MXN** al día. **VUAA** (Vanguard S&P 500 UCITS) se negocia en 251 de 252 sesiones, con mediana de **5.3 millones de MXN** y precio de ~2,630 MXN, contra ~14,700 MXN de CSPX. **IUSA** casi no se negocia (14 de 213 sesiones). Al ser acciones de sociedades irlandesas, **no están situados en EUA** para el *estate tax*. Además, Irlanda exenta estos fondos de su impuesto a herencias (CAT) si el causante y el heredero no residen ni tienen domicilio en Irlanda. Lo que se paga dentro del fondo es **15%** de retención de EUA, contra 10% con W-8BEN y 30% sin él. Con un rendimiento por dividendo del S&P de **0.99%**, esa fuga es de **0.15 pp** al año, contra 0.10 pp y 0.30 pp.

## Por qué existe

El resumen de laboratorio recibido el 25-sep-2026 dice: "Confirmé con los PDF oficiales de SPIVA la meta que tenemos que superar: el 85.6% de los fondos grandes de EUA queda debajo del S&P 500 a 10 años, y en México el 82.9% queda debajo de su índice. Los fondos mexicanos que sí ganaron tenían en común una cartera muy distinta a la de su índice y parte de su dinero en fondos o ETFs extranjeros." También dice: "Me falta cerrar los impuestos de 2026 en México, el impuesto sucesorio de EUA sobre acciones del SIC…". La regla del sistema es no adoptar ninguna cifra ajena sin verificarla con documentos, datos y código propios.

Nota de ruta: la tarea pedía el README en `V05-spiva-y-fiscalidad/` y la carpeta en `V05-spiva-y-fiscalidad-sic/`. Se usó solo la segunda para no duplicar la réplica.

---

## PRE-REGISTRO

Lo que sigue es la copia literal de `prerregistro.md`. Se escribió a las 05:37 UTC del 2026-09-25, y su huella SHA-256 (`c31763f3…`) quedó en `SHA256SUMS.txt` a las 05:38 UTC, antes de la primera descarga. La primera versión del manifiesto está guardada en `datos/prerregistro-huella-inicial-0538UTC.txt`. Los encabezados bajaron un nivel para anidarlos aquí.

> Escrito el 2026-09-25 a las 05:37 UTC, **antes** de abrir cualquier PDF de SPIVA, antes de descargar precios y antes de calcular nada. Este archivo no se edita después: su huella SHA-256 queda en `SHA256SUMS.txt` antes de la primera descarga. Cualquier cambio posterior va a "Desviaciones del pre-registro" en `README.md`.
>
> Lo único que se sabe al escribirlo: el texto de las afirmaciones recibidas y que S&P Dow Jones Indices (S&P DJI) publica los *SPIVA Scorecards* en PDF dos veces al año (cierre de año y mitad de año).

### 1. Afirmaciones recibidas (literales, 25-sep-2026)

- **A1.** "el 85.6% de los fondos grandes de EUA queda debajo del S&P 500 a 10 años" (confirmado, según el emisor, "con los PDF oficiales de SPIVA").
- **A2.** "en México el 82.9% queda debajo de su índice" (a 10 años, contra el S&P/BMV IPC).
- **A3.** "Los fondos mexicanos que sí ganaron tenían en común una cartera muy distinta a la de su índice y parte de su dinero en fondos o ETFs extranjeros."

### 2. Fuentes admitidas

- **Primarias para A1 y A2:** solo los PDF de los *SPIVA U.S. Scorecard* y *SPIVA Latin America Scorecard* publicados por S&P DJI en `spglobal.com`. Notas de prensa, blogs o resúmenes de terceros solo sirven como pista, nunca como confirmación.
- **Primarias para A3:** un documento de S&P DJI (scorecard, comentario o investigación) o datos de los propios fondos (prospectos, carteras publicadas, CNBV/AMIB) que documenten *active share* o exposición extranjera **de los fondos que superaron al índice**. Un texto que diga que "algunos fondos tienen exposición extranjera" sin ligarlo a los ganadores no confirma A3.

### 3. Ediciones que se revisan (lista cerrada)

Todas las ediciones de *SPIVA U.S.* y *SPIVA Latin America* publicadas entre el cierre de 2023 y el 25-sep-2026 que se puedan descargar del sitio oficial: Year-End 2023, Mid-Year 2024, Year-End 2024, Mid-Year 2025, Year-End 2025 y Mid-Year 2026 (si ya existe). Para cada una se registra:

- A1: % de fondos de la categoría *All Large-Cap Funds* por debajo del S&P 500 a 10 años (reporte 1, rendimiento absoluto), y la fecha de corte y de publicación.
- A2: % de fondos de la categoría *Mexico Equity* por debajo del S&P/BMV IPC a 10 años, y la fecha de corte y de publicación.
- Las ediciones que no se puedan descargar se listan como "no obtenidas", sin inferir su contenido.

### 4. Criterio de veredicto para A1 y A2

- **Confirmada:** la cifra exacta (con tolerancia de ±0.05 pp por redondeo) aparece en la edición **más reciente** publicada al 25-sep-2026, en la categoría y el horizonte afirmados.
- **Confirmada con matices:** la cifra aparece en una edición oficial pero (a) no es la más reciente, o (b) la categoría, el horizonte o la métrica difieren (por ejemplo, ajustada por riesgo o ponderada por activos), o (c) la etiqueta de la afirmación no corresponde a la del reporte (por ejemplo, "fondos grandes" frente a *All Large-Cap Funds*). El matiz se describe siempre.
- **No confirmada:** la cifra no aparece en ninguna de las ediciones revisadas.
- Se reporta además la cifra de la edición más reciente, aunque la afirmación no se confirme.

### 5. Criterio para A3

- **Confirmada:** una fuente primaria del punto 2 liga a los fondos ganadores con *active share* alto **y** con exposición extranjera.
- **Confirmada con matices:** una fuente primaria documenta solo una de las dos características, o las documenta para la categoría sin distinguir ganadores de perdedores.
- **No confirmada:** no hay fuente primaria que lo documente. Esto no prueba que sea falso.

### 6. Análisis B (mecánico, con datos propios; descriptivo más una prueba)

Pregunta: ¿cuánto ganaría contra el IPC un fondo mexicano que solo cambia una parte de su cartera por el S&P 500, sin talento alguno para elegir acciones?

- **Ventana:** los 10 años que cubre la edición donde aparece A2. Si A2 no aparece, la ventana de la edición más reciente de SPIVA Latin America.
- **Series (en MXN, mensuales, de fin de mes):**
  - IPC con dividendos: `NAFTRAC.MX` de Yahoo, columna `adjclose` (incluye la comisión del ETF, así que queda ligeramente por debajo del índice de rendimiento total).
  - S&P 500 con dividendos en MXN: `SPY` de Yahoo, `adjclose` (dividendos brutos, sin retención) por el tipo de cambio de fin de mes `DEXMXUS` de FRED (último dato hábil del mes).
  - Carteras fijas IPC/S&P con rebalanceo mensual: 100/0, 90/10, 80/20, 70/30 y 50/50.
- **Qué se reporta:** CAGR de cada cartera, diferencia de CAGR contra 100/0 (en pp por año), y la fracción en S&P 500 que haría falta para compensar 1, 2 y 3 pp de gastos anuales (interpolación lineal sobre la diferencia de CAGR).
- **Prueba:** diferencia mensual S&P(MXN) − IPC en la ventana, media, t Newey-West con 6 rezagos e IC 95%. Veredicto: apoyo si el límite inferior > 0, contraria si el superior < 0, inconcluso en otro caso. Es una sola prueba.
- **Conclusión que se permitirá:** solo la mecánica ("con X% en el S&P se superaba al IPC por Y pp en esa ventana"). **No** se concluirá que los fondos ganadores ganaron por eso, a menos que A3 quede confirmada por fuente primaria.

### 7. Parte documental de fiscalidad (sin veredicto estadístico)

Se verifican con fuente primaria (ley, DOF, SAT, IRS, Tesoro de EUA, BMV, emisor del ETF, GBM) y se etiqueta cada punto como **verificado**, **parcialmente verificado** o **no verificado**:

1. ISR de 10% sobre la ganancia en BMV y SIC (persona física residente), sin retención en la venta, y cómo se aplican las pérdidas.
2. Dividendos de emisoras mexicanas y extranjeras del SIC: retención en EUA y 10% en México.
3. Tasa de retención anual de ISR sobre intereses para 2026 según la Ley de Ingresos de la Federación 2026.
4. Constancia fiscal anual de GBM.
5. Impuesto sucesorio de EUA para no residentes: exención de 60,000 USD, existencia o no de tratado México-EUA en sucesiones, y si la custodia vía Indeval/SIC cambia el *situs* de acciones y ETFs de EUA. Si no hay certeza, se dice.
6. ETFs UCITS domiciliados en Irlanda listados en el SIC (existencia verificada en BMV o en datos de mercado) y tratamiento de dividendos (15% en el fondo irlandés frente a 10% del tratado México-EUA con W-8BEN, o 30% sin él).

### 8. Lo que no se hará

- No se adopta ninguna cifra de SPIVA sin haberla leído en el PDF oficial congelado en `datos/`.
- No se da asesoría fiscal: el capítulo describe normas vigentes con fuente y marca lo no verificado. Fase 0: sin recomendaciones reales.

---

## RESULTADOS (después de correr)

### Desviaciones del pre-registro

| # | Qué cambió | Por qué | ¿Afecta el veredicto? |
|---|---|---|---|
| 1 | Los PDF de SPIVA se tomaron de **capturas del Internet Archive** de las URL oficiales de `spglobal.com`, con el sufijo `id_` (bytes originales). | `spglobal.com` responde 403 a clientes que no son navegador, tanto con curl como con WebFetch. Las capturas de EUA venían comprimidas con gzip de transporte y se descomprimieron. | No. Los metadatos (título, autores, fecha de creación) y el contenido son de S&P DJI. Una segunda extracción de texto, con pdfminer en lugar de pypdf, da las mismas cifras clave (85.59, 83.33, 82.93, 74.3%, 16.4%). |
| 2 | **No se obtuvo** SPIVA Latin America Year-End 2025, ni Mid-Year 2024, ni la versión en inglés de Mid-Year 2025. | 403 en el sitio oficial y ninguna captura en el archivo. | No cambia A2: la cifra ya no es la más reciente con la edición de mitad de 2025, que sí se obtuvo. Las cifras de cierre de 2025 de un resumen de buscador se reportan como **no verificadas**. |
| 3 | La edición de EUA de mitad de 2024 es un formato corto ("SPIVA U.S. Focus") **sin Report 1a**. | Así la publicó S&P DJI. | No. ~~Queda como "sin tabla".~~ **Corrección (2026-09-25):** la misma medida está en su Report 3 (*Fund Underperformance Rates*), con 84.71% a 10 años. Ver la tabla 1. |
| 4 | En el análisis B se agregaron **dos ventanas exploratorias**: el año 2024 (con 16.4% en el S&P, el peso de A3) y 2016-2025 (la ventana de la edición de cierre de 2025). | Surgieron **después** de leer A3. | No. Van marcadas como exploratorias. La única prueba pre-registrada es 2015-2024. |
| 5 | Se agregaron descriptivos que no entran a ningún veredicto: fuga por retención de dividendos, liquidez de ETFs UCITS y de EUA en el SIC (Yahoo, 1 año), una ilustración del *estate tax*, rendimientos anualizados de SPIVA (Reports 3 y 4) y una verificación mecánica de 29 citas legales. | Hacen verificable la parte documental (punto 7 del pre-registro). | No. |

### Controles de calidad

- **Huellas:** `herramientas/huellas.py verificar` → OK (57 archivos más el pre-registro).
- **Extracción de texto:** `reproducir.py` re-extrae los 9 PDF con pypdf, si está instalado, y compara byte a byte con los `.txt` congelados: son idénticos. Con **pdfminer**, un extractor distinto, se confirmaron las filas de 85.59 (cierre de 2025) y 83.33 (mitad de 2026), y la presencia de 82.93, 74.3% y 16.4% (cierre de 2024 de América Latina).
- **Doble implementación del análisis B:** un script aparte, que usa el parser del repo (`herramientas/datos_historicos.parsear_yahoo_historia`) y no el código de `reproducir.py`, reproduce los CAGR: 3.53% y 16.98% en 2015-2024 (80/20 → 6.40%); −10.27% y 54.12% en 2024; 6.50% y 15.25% en 2016-2025.
- **Datos propios contra SPIVA (misma ventana, 10 años a 2024):** NAFTRAC da 3.53% contra 4.14% del S&P/BMV IRT según SPIVA. La **brecha de −0.61 pp al año** se debe a la comisión y el *tracking* del ETF y sesga el IPC hacia abajo; por eso la ventaja de las mezclas está sobrestimada en unos 0.1-0.3 pp. SPY × DEXMXUS da 16.98% contra 17.08% del S&P 500 (MXN) de SPIVA (−0.10 pp, el gasto de SPY).

### 1. A1: fondos *All Large-Cap* de EUA por debajo del S&P 500 (Report 1a, rendimiento absoluto, % de fondos)

| Edición | Corte | Publicación | Año corrido | 1 año | 3 años | 5 años | **10 años** | 15 años | 20 años |
|---|---|---|---|---|---|---|---|---|---|
| Year-End 2023 | 31-dic-2023 | mar-2024 | — | 59.68 | 79.78 | 78.68 | **87.42** | 87.98 | 93.03 |
| Focus Mid-Year 2024 | 30-jun-2024 | oct-nov 2024 | 57.31 | 57.05 | 86.08 | 77.26 | **84.71** (Report 3) | 89.54 | 91.77 |
| Year-End 2024 | 31-dic-2024 | ~mar-2025 | — | 65.24 | 84.96 | 76.26 | **84.34** | 89.50 | 91.99 |
| Mid-Year 2025 | 30-jun-2025 | ~sep-2025 | 54.31 | 72.61 | 64.87 | 86.91 | **85.98** | 88.29 | 91.03 |
| **Year-End 2025** | 31-dic-2025 | mar-2026 | — | 78.78 | 66.84 | 88.96 | **85.59** ← afirmación | 89.93 | 92.89 |
| **Mid-Year 2026 (la más reciente)** | 30-jun-2026 | ~16-17 sep 2026 | 67.18 | 78.69 | 76.63 | 89.32 | **83.33** | 90.49 | 92.61 |

Las fechas de publicación salen de los metadatos del PDF, la primera captura del archivo o la nota 1 de la edición *Focus*. Solo la de cierre de 2025 viene de un resumen de buscador (ver `resultados.json`).

**Corrección (2026-09-25, doble ejecución independiente).** La edición *Focus* de mitad de 2024 no tiene un Report 1a, pero sí trae la misma medida en su **Report 3**, *Fund Underperformance Rates – U.S. Equity Categories* (página 8, datos al 30-jun-2024). Ahí la fila *All Large-Cap Funds* contra el S&P 500 da **84.71%** a 10 años. Antes esta fila decía "sin Report 1a (solo gráfica)", porque `reproducir.py` solo buscaba el Report 1a. El veredicto no cambia: 84.71 queda dentro del rango de 83% a 87%, y los valores a 15 años (89.54) y a 20 años (91.77) caen dentro del rango de 88% a 93%. Anotado en `conocimiento/registro-de-errores.md`.

**Veredicto A1: confirmada con matices.** La cifra está en Year-End 2025 (85.59 → 85.6). Hay dos matices: (a) no es la edición más reciente, porque Mid-Year 2026 da 83.33%; (c) "fondos grandes" es *All Large-Cap Funds*. Lo robusto es el rango: en todas las ediciones revisadas, **de 83% a 87%** de los fondos *large-cap* quedaron debajo del S&P 500 a 10 años, y **de 88% a 93%** a 15 y 20 años.

### 2. A2: fondos *Mexico Equity* por debajo del S&P/BMV IRT (Report/Tabla 1a, % de fondos)

| Edición | Corte | Publicación | Año corrido | 1 año | 3 años | 5 años | **10 años** | Supervivencia a 10 años |
|---|---|---|---|---|---|---|---|---|
| Year-End 2023 | 31-dic-2023 | abr-2024 | — | 90.70 | 79.07 | 77.78 | **87.80** | 78.05% (41 fondos) |
| **Year-End 2024** | 31-dic-2024 | abr-2025 | — | 18.60 | 46.51 | 62.79 | **82.93** ← afirmación | 78.05% (41) |
| Primer semestre 2025 (español) | 30-jun-2025 | oct-2025 | 63.64 | 50.00 | 60.47 | 69.05 | **73.17** | **82.93%** (41) ← trampa |
| Year-End 2025 | 31-dic-2025 | 2026 | **no obtenida** (403). Según un resumen de buscador, no verificado: 1 año 75.6, 3 años 69.8, 5 años 77.3 y **10 años 75.6** | | | | | |

**Contexto de la misma serie** (10 años, % de fondos por debajo): fondos mexicanos de acciones de EUA contra el S&P 500 (MXN): **86.67%** en cierre de 2024 y en mitad de 2025. Fondos globales en MXN contra el S&P World (MXN): **100%** en ambas.

**Rendimientos anualizados de SPIVA, 10 años al 31-dic-2024** (Report 3 equiponderado / Report 4 ponderado por activos):

| Serie | 1 año | 3 años | 5 años | 10 años |
|---|---|---|---|---|
| S&P/BMV IRT | −10.70 | 1.07 | 5.83 | **4.14** |
| Fondos Mexico Equity (equiponderado / por activos) | −6.73 / −2.41 | 2.25 / 3.90 | 3.98 / 4.03 | **2.56 / 2.53** |
| S&P 500 (MXN) | 53.51 | 9.60 | 16.79 | **17.08** |
| Fondos U.S. Equity (MXN) | 44.14 / 50.86 | 5.08 / 7.61 | 12.29 / 15.28 | **12.65 / 14.51** |
| S&P World (MXN) | 46.67 | 7.38 | 13.79 | **14.33** |
| Fondos Global Equity (MXN) | 29.89 / 33.53 | 2.41 / 3.57 | 6.55 / 9.06 | **7.09 / 9.26** |

**Veredicto A2: confirmada con matices.** La cifra está en Year-End 2024 (82.93 → 82.9). Los matices: (a) no es la más reciente, porque el primer semestre de 2025 da 73.17%; (b) el índice es el S&P/BMV IRT, con dividendos; y en la edición siguiente la misma cifra, 82.93%, aparece como **supervivencia**, un error fácil de cometer.

### 3. A3: qué tenían los ganadores mexicanos

Fuente: *SPIVA Latin America Year-End 2024*, páginas 7 y 8 y Exhibit 8 (datos al 31-dic-2024). Cita textual: "Revisiting the Mexico Equity category, where only 18.6% of funds underperformed in 2024 […] among top-quartile Mexico Equity funds, the average allocation to securities outside of the S&P/BMV IRT benchmark was 74.3% […] offshore (non-Mexico domiciled) securities consisting almost entirely of U.S. and European-domiciled index funds and ETFs also played a major role in generating outperformance. In fact, top-quartile Mexico Equity funds held an average of 16.4% weight in foreign index funds and ETFs."

| Medida (promedio del cuartil superior, 2024) | Texto | Gráfica (Exhibit 8) |
|---|---|---|
| Valores fuera del S&P/BMV IRT | 74.3% | 74.3% |
| Valores *offshore* (no domiciliados en México) | — | 16.8% |
| Fondos indexados y ETFs extranjeros | **16.4%** | **16.2%** |

**Veredicto A3: confirmada con matices.** La fuente es primaria y dice lo que afirma el resumen, pero hay tres matices: (1) habla del **cuartil superior de 2024, a 1 año**, no de los ganadores a 10 años; (2) mide el peso fuera del índice, que es una cota inferior del *active share*, no el *active share*; (3) texto y gráfica no coinciden por 0.2 pp.

### 4. Análisis B: cuánto "gana" un fondo mexicano solo por comprar S&P 500 (datos propios, MXN, rebalanceo mensual, sin costos)

**Pre-registrado: 2015-01 a 2024-12 (120 meses; la ventana de 10 años de Year-End 2024).**

| Peso en S&P 500 (MXN) | CAGR | Ventaja contra IPC (pp/año) |
|---|---|---|
| 0% (IPC = NAFTRAC con dividendos) | 3.53% | — |
| 10% | 4.98% | +1.45 |
| 20% | 6.40% | +2.88 |
| 30% | 7.81% | +4.29 |
| 50% | 10.56% | +7.03 |
| 100% (S&P 500 en MXN) | 16.98% | +13.46 |

- **Peso en S&P necesario para compensar gastos** (interpolación lineal pre-registrada): **6.9%** para 1 pp, **13.8%** para 2 pp y **20.9%** para 3 pp.
- **Prueba pre-registrada:** diferencia mensual S&P(MXN) − IPC con media de **1.018% al mes**, t Newey-West(6) = **1.99** e IC 95% = **[0.014, 2.021]**, lo que da **apoyo**. Es un apoyo al límite: el intervalo casi toca cero.

**Exploratorio, no pre-registrado:**

| Ventana | IPC | S&P 500 MXN | Ventaja con 10% / 16.4% / 20% en S&P | Peso para compensar 2 pp | t NW(6) de la diferencia | Veredicto |
|---|---|---|---|---|---|---|
| 2024 (12 meses) | −10.27% | 54.12% | +5.22 / **+8.69** / +10.69 pp | 3.8% | 5.48 | apoyo (12 meses: solo descriptivo) |
| 2016-2025 (120 meses) | 6.50% | 15.25% | +1.04 / — / +2.04 pp | 19.6% | 1.20 | **inconcluso** |

**Lectura.** En la ventana de SPIVA a 2024, un fondo sin ningún talento para elegir acciones le ganaba al IPC por 2 pp al año con solo una séptima parte de su cartera en el S&P 500. Los gastos reales de los fondos mexicanos no se midieron aquí. En 2024, el peso extranjero que S&P encontró en los ganadores (16.4%) daba **+8.7 pp**. Eso es más que la ventaja del fondo promedio sobre el IRT ese año: +4.0 pp equiponderado y +8.3 pp ponderado por activos (Reports 3 y 4). Pero la superioridad del S&P en pesos **no es robusta a la ventana**: en 2016-2025 la diferencia mensual queda inconclusa (t = 1.20).

### 5. Fiscalidad: estado de verificación (detalle y fuentes en el capítulo 27)

| Punto | Resultado | Estado |
|---|---|---|
| ISR sobre la ganancia en BMV y SIC (persona física) | 10% definitivo sobre la ganancia neta del año. Incluye "acciones emitidas por sociedades extranjeras cotizadas" y "títulos que representen índices accionarios". Declaración anual junto con la del art. 150 | **Verificado** (art. 129 LISR) |
| Pérdidas | Solo contra ganancias del art. 129, en el mismo año o en los **10 siguientes**, actualizadas por inflación. Si pudiendo no se restan, se pierde ese monto | **Verificado** (art. 129) |
| Constancia | El intermediario calcula la ganancia o pérdida y entrega la constancia. GBM: "Constancias Fiscales (o CFDI) por las ganancias del 2025" en la app. Sin CFDI para Trading USA | **Verificado** (art. 129; FAQ de GBM) |
| Retención de ISR sobre intereses en 2026 | **0.90%** anual sobre el capital (arts. 54 y 135 LISR); es pago provisional | **Verificado** (art. 24 LIF 2026, DOF 07-11-2025) |
| Dividendos de emisoras mexicanas | 10% adicional retenido (definitivo), más acumulación con acreditamiento del ISR corporativo | **Verificado** (art. 140) |
| Dividendos extranjeros (SIC) | EUA retiene 30%, o 10% con W-8BEN (tratado, art. 10). En México, 10% adicional definitivo y acumulación con acreditamiento del impuesto extranjero. GBM retiene el 10% "sobre monto neto" | **Verificado** (art. 142 fr. V; tratado; FAQ de GBM). Base del 10%: la letra del art. 142 fr. V la calcula "sin incluir el monto del impuesto retenido que en su caso se hubiere efectuado", o sea sobre el **neto**, y GBM también dice neto. No se revisó un criterio del SAT. **Corrección (2026-09-25):** antes decía "la ley es ambigua" |
| Reformas 2026 | La LISR sigue con última reforma del DOF 01-04-2024. Los cambios de ISR de 2026 van en la LIF | **Verificado** (textos de la Cámara de Diputados) |
| *Estate tax* EUA: umbral y crédito | Umbral de declaración de 60,000 USD y crédito de 13,000 USD. Tarifa de 18% a 40% | **Verificado** (instrucciones del 706-NA de 09/2025; 26 USC 2102 y 2001(c)) |
| Tratado sucesorio México-EUA | No existe. Lista de 15 países: Australia, Austria, Canadá, Dinamarca, Finlandia, Francia, Alemania, Grecia, Irlanda, Italia, Japón, Países Bajos, Sudáfrica, Suiza y Reino Unido | **Verificado** (706-NA) |
| *Situs* de acciones y ETFs de EUA vía SIC/Indeval | Regla: acciones de sociedad de EUA "sin importar dónde estén los certificados" (26 CFR 20.2104-1(a)(5)). La excepción para fondos RIC venció en 2011 | Regla **verificada**. Su aplicación al SIC: **sin certeza formal** (no hay resolución), la lectura dominante es que sí son activos situados en EUA |
| UCITS irlandeses en el SIC | CSPX, VUAA, IUSA, IWDA, VWRA, ISAC, EIMI y CNDX cotizan en MXN en la BMV según Yahoo | **Verificado** (datos de mercado). Que GBM permita comprarlos desde la app: **no verificado** |
| Dividendos dentro del UCITS irlandés | 15% de retención de EUA al fondo (tratado EUA-Irlanda, art. 10), contra 10% del tratado México-EUA | Tasas **verificadas**. Que el fondo efectivamente pague 15%: inferencia |
| Impuesto sucesorio irlandés (CAT) sobre UCITS | Exento si causante y heredero no tienen domicilio ni residencia en Irlanda | **Verificado** (Revenue, notas de guía de la s.75 CATCA 2003) |
| ISR mexicano sobre ganancias en UCITS del SIC | Por la letra del art. 129 fr. I-II, 10% | **Inferencia**, sin regla ni criterio del SAT específico. No aplica el régimen de REFIPRE sin control efectivo (art. 176) |

### 6. SIC: liquidez de ETFs del S&P 500 y globales (Yahoo, 1 año de sesiones al 24-sep-2026)

| Ticker (Yahoo) | Fondo | Domicilio | Precio (MXN por título) | Sesiones con volumen | Mediana de valor diario (MXN) |
|---|---|---|---|---|---|
| CSPXN.MX | iShares Core S&P 500 UCITS (acumulación, TER 0.07%) | Irlanda | 14,725.50 | 249/252 | 47,066,414 |
| VUAAN.MX | Vanguard S&P 500 UCITS (acumulación) | Irlanda | 2,630.00 | 251/252 | 5,269,476 |
| IUSAN.MX | iShares S&P 500 UCITS (distribución, TER 0.07%) | Irlanda | 1,304.43 | 14/213 | 0 |
| IWDAN.MX | iShares Core MSCI World UCITS | Irlanda | 2,603.90 | 155/249 | 40,049 |
| VWRAN.MX | Vanguard FTSE All-World UCITS | Irlanda | 3,413.86 | 239/252 | 641,284 |
| ISACN.MX | iShares MSCI ACWI UCITS | Irlanda | 2,192.08 | 199/252 | 670,349 |
| EIMIN.MX | iShares Core MSCI EM IMI UCITS | Irlanda | 979.00 | 195/250 | 754,376 |
| CNDXN.MX | iShares NASDAQ 100 UCITS | Irlanda | 31,040.00 | 209/252 | 4,812,577 |
| IVV.MX | iShares Core S&P 500 ETF | EUA | 13,673.23 | 250/252 | 73,814,940 |
| VOO.MX | Vanguard S&P 500 ETF | EUA | 12,552.41 | 250/252 | 35,557,601 |
| SPY.MX | SPDR S&P 500 ETF Trust | EUA | 13,617.49 | 250/252 | 19,440,541 |

El domicilio, el TER y la política de dividendos de CSPX e IUSA están verificados en la página de iShares (ISIN IE00B5BMR087 e IE0031442068). Los de VUAA salen del nombre de la emisora en Yahoo (Vanguard Funds plc); su TER no se verificó. En el SIC solo se compran títulos completos (documento `arena/investigacion/01`): **un título de CSPX equivale a ~74% de una cuenta de 20,000 MXN**, y uno de VUAA a ~13%.

### 7. Impuesto sucesorio de EUA: ilustración (26 USC 2001(c) menos 13,000 USD; sin deducciones; TC 17.2454 MXN/USD del 18-sep-2026)

| Activos situados en EUA | En MXN | Impuesto | Tasa efectiva |
|---|---|---|---|
| 1,160 USD (una cuenta de 20,000 MXN) | 20,000 | 0 | 0% |
| 60,000 USD | 1,034,724 | 0 | 0% |
| 100,000 USD | 1,724,540 | 10,800 USD | 10.8% |
| 250,000 USD | 4,311,350 | 57,800 USD | 23.1% |
| 500,000 USD | 8,622,700 | 142,800 USD | 28.6% |
| 1,000,000 USD | 17,245,400 | 332,800 USD | 33.3% |

## Conclusiones permitidas

1. En SPIVA, **de 83% a 87%** de los fondos *large-cap* activos de EUA quedaron debajo del S&P 500 a 10 años en cada edición de 2023 a 2026. El **85.6%** es de Year-End 2025, y la cifra vigente al 25-sep-2026 es **83.33%** (Mid-Year 2026).
2. En México, **de 73% a 88%** de los fondos activos quedaron debajo del S&P/BMV IRT a 10 años en las ediciones obtenidas. El **82.9%** es de Year-End 2024, y la última cifra obtenida es **73.17%** (primer semestre de 2025).
3. S&P DJI atribuye buena parte de la ventaja de los mejores fondos mexicanos de 2024 a valores fuera del índice, incluyendo en promedio **16.4%** en fondos indexados y ETFs extranjeros.
4. En la ventana 2015-2024, una exposición chica al S&P 500 en pesos bastaba para superar al IPC por más de 1-2 pp al año, sin talento alguno. **Ganarle al IPC no prueba talento de selección.**
5. Los fondos mexicanos que invierten en EUA o globalmente quedaron por debajo de sus índices en pesos en **87% a 100%** de los casos a 10 años, y en promedio por **4.4 a 7.2 pp al año** (equiponderado). Para un inversionista en pesos, la meta no se supera con fondos activos mexicanos, ni domésticos ni internacionales.
6. La fiscalidad de la tabla 5 está verificada en su fuente primaria vigente al 25-sep-2026, salvo los puntos marcados como inferencia o no verificados.
7. Para quien tenga más de ~1.03 millones de MXN en acciones o ETFs de EUA, el *estate tax* es un riesgo material (10.8% efectivo con 100,000 USD y 33% con 1 MUSD). Los UCITS irlandeses del SIC evitan el *situs* de EUA según la regla del IRS, y CSPX y VUAA tienen liquidez diaria.

## Conclusiones que NO se sostienen

1. Que **85.6%** y **82.9%** sean las cifras "vigentes": ambas fueron superadas por ediciones posteriores.
2. Que los fondos mexicanos que ganaron **a 10 años** tuvieran exposición extranjera: el análisis de S&P es del cuartil superior de **2024**, a un año.
3. Que exista un "active share" medido por S&P para México: lo que midió es el peso fuera del índice.
4. Que el S&P 500 en pesos le gane al IPC de forma estadísticamente robusta: el apoyo de 2015-2024 es marginal (t = 1.99) y en 2016-2025 es inconcluso.
5. Que comprar vía SIC en pesos libre del *estate tax* a las acciones y ETFs de EUA. Tampoco lo contrario, con certeza formal: no hay resolución específica sobre el SIC.
6. Que un UCITS irlandés sea siempre mejor: con W-8BEN, el ETF de EUA pierde menos por dividendos (10% contra 15%). Además, CSPX cuesta ~14,700 MXN por título, IUSA no tiene liquidez, y el trato fiscal mexicano de un UCITS en el SIC es inferencia, no regla expresa.
7. Que alguna de estas conclusiones sea una recomendación de inversión (fase 0).

## Estado

- **Afirmación recibida (conjunto):** confirmada con matices.
- **Tabla maestra:** la fila V05 dice "en curso". Veredicto corto propuesto: "A1, A2 y A3 confirmadas con matices; fiscalidad verificada". **Etiqueta propuesta: no aplica**, porque no es una prueba de ventaja. No se editó `laboratorio/tabla-maestra.md` para no chocar con otras sesiones.
- **Pendientes:**
  1. Descargar el PDF oficial de SPIVA Latin America Year-End 2025 desde un navegador y congelarlo; confirmar el 75.6% a 10 años.
  2. Confirmar en GBM (app o contrato) que CSPX y VUAA se pueden comprar en Trading MX.
  3. Buscar un criterio del SAT o una regla de la RMF 2026 sobre ETFs extranjeros de renta fija en el SIC, que no quedan claramente en el art. 129.
  4. Pedir opinión a un abogado fiscal sobre el *situs* de las acciones de EUA custodiadas vía Indeval.
  5. ~~Dar la réplica de este archivo al subagente auditor.~~ Hecho el 2026-09-25: ver "Doble ejecución independiente (2026-09-25)".

## Fuentes

- S&P DJI, *SPIVA U.S. Scorecard* Year-End 2023, Year-End 2024, Mid-Year 2025, Year-End 2025, Mid-Year 2026 y *SPIVA U.S. Focus* Mid-Year 2024: `https://www.spglobal.com/spdji/en/documents/spiva/spiva-us-<edición>.pdf` (capturas del Internet Archive en `datos/procedencia.json`). Página de la serie: https://www.spglobal.com/spdji/en/spiva/article/spiva-us/
- S&P DJI, *SPIVA Latin America Scorecard* Year-End 2023 (https://www.spglobal.com/spdji/en/documents/spiva/spiva-latin-america-scorecard-year-end-2023.pdf), Year-End 2024 (https://www.spglobal.com/spdji/en/documents/spiva/spiva-latin-america-year-end-2024.pdf) y Primer semestre de 2025 en español (https://www.spglobal.com/spdji/es/documents/spiva/spiva-latin-america-mid-year-2025-es.pdf). La edición Year-End 2025 (https://www.spglobal.com/spdji/en/documents/spiva/spiva-latin-america-year-end-2025.pdf) no se obtuvo.
- Ley del ISR, texto vigente (Cámara de Diputados): https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf
- Ley de Ingresos de la Federación 2026: https://www.diputados.gob.mx/LeyesBiblio/pdf/LIF_2026.pdf
- IRS, Instructions for Form 706-NA (09/2025): https://www.irs.gov/instructions/i706na
- 26 CFR 20.2104-1: https://www.ecfr.gov/current/title-26/part-20/section-20.2104-1 · 26 USC 2001, 2102 y 2105: https://www.law.cornell.edu/uscode/text/26/2001, https://www.law.cornell.edu/uscode/text/26/2102, https://www.law.cornell.edu/uscode/text/26/2105
- Tratados del IRS: México (https://www.irs.gov/pub/irs-trty/mexico.pdf) e Irlanda (https://www.irs.gov/pub/irs-trty/ireland.pdf)
- Irish Revenue, *Notes for Guidance CATCA 2003, Part 9* (s.75): https://www.revenue.ie/en/tax-professionals/documents/notes-for-guidance/cat/2024/part09.pdf
- iShares: CSPX (https://www.ishares.com/uk/individual/en/products/253743/ishares-sp-500-b-ucits-etf-acc-fund) e IUSA (https://www.ishares.com/uk/individual/en/products/251900/ishares-sp-500-ucits-etf-inc-fund)
- GBM, FAQ: impuestos en el SIC (https://gbm.com/faqs/como-funcionan-los-impuestos-por-las-acciones-de-empresas-extranjeras-en-el-sic/), dividendos (https://gbm.com/faqs/como-funcionan-los-impuestos-sobre-los-dividendos-en-trading-mx/), W-8BEN (https://gbm.com/faqs/que-es-y-como-funciona-el-w-8ben-para-trading-mx-y-sic/) y constancias (https://gbm.com/faqs/como-y-donde-recibo-los-comprobantes-fiscales-o-cfdi-por-mis-ganancias/)
- Precios: Yahoo Finance chart v8 (NAFTRAC.MX, SPY y ETFs del SIC) y FRED DEXMXUS (https://fred.stlouisfed.org/series/DEXMXUS)
