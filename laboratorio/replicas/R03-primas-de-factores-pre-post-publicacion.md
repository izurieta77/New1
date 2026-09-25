# Réplica R03: primas de factores de EUA antes y después de su publicación (decaimiento McLean-Pontiff, crashes de momentum y "muerte del value")

> Fase 0: formación. Esta ficha no recomienda inversiones. Las secciones 1 a 9 son el pre-registro. Se escribieron el 2026-09-25, antes de calcular cualquier estadístico de los factores, y no se editan después. Cualquier cambio posterior va a "Desviaciones del pre-registro", con fecha.

| Campo | Valor |
|---|---|
| ID | `R03` (registro: `laboratorio/replicas/R03-variantes.csv`; script: `laboratorio/replicas/R03.py`) |
| Hallazgo a replicar | McLean, R. D. y Pontiff, J. (2016). "Does Academic Research Destroy Stock Return Predictability?". *Journal of Finance* 71(1), 5–32. doi:10.1111/jofi.12365. Resumen publicado (Wiley y SSRN 2156623, consultados con WebSearch el 2026-09-25): 97 predictores; rendimientos **26% menores fuera de muestra** y **58% menores después de la publicación**; 32% (58 − 26) atribuido al *trading* informado por la publicación. El método se leyó en las versiones de trabajo en PDF (23-oct-2012, HEC Montréal; 16-may-2013, FMG-LSE). El texto completo de la versión publicada **no** se leyó |
| Artículos originales de cada factor | Banz (1981) para SMB; Fama y French (1992) para HML; Jegadeesh y Titman (1993) para Mom; Fama y French (2015) para RMW y CMA. Crashes: Daniel y Moskowitz (2016). Detalle y cifras en la sección 1 |
| Fecha de publicación | Ver tabla de la sección 6 (convención de McLean-Pontiff: año y número de la revista) |
| Pre-registro escrito el | 2026-09-25, antes de calcular cualquier estadístico de los factores. Lo único que se ejecutó antes fue la carga de **metadatos** de los cuatro archivos French desde el caché (rango de fechas, columnas, versión CRSP 202607 y sha256), para fijar las ventanas |
| Responsable | Claude (laboratorio del sistema). Revisión independiente pendiente (`auditor-de-replicas`) |
| Estado | Pendiente (se asigna en la sección 16) |

**Conocimiento previo declarado.** Este pre-registro **no** es ciego. Los capítulos `conocimiento/02` (§5.1) y `conocimiento/03` (§5.1 y §5.4) ya reportan cifras calculadas con la misma versión de datos (CRSP 202607): por ejemplo, HML 2.81% anual (t = 1.45) desde 1992, SMB 0.66% (t = 0.36) desde 1992, Mom 4.49% (t = 1.54) en 1994-2026, RMW y CMA más débiles desde 2014, HML −57.8% de dic-2006 a sep-2020 y el crash de Mom de 2009. La réplica V01 encontró Mom ≈ 0 desde oct-2006. Por eso esta réplica (a) fija ventanas y reglas antes de correr, (b) usa el diseño de McLean-Pontiff y no ventanas elegidas a la vista, y (c) somete esas cifras del sistema a verificación (sección 8, bloque C).

---

## PRE-REGISTRO (secciones 1 a 9)

### 1. Hipótesis previa y mecanismo

**Resultados declarados en los artículos** (verificados en el PDF salvo donde se marca [I]):

| Artículo | Revista y fecha | Muestra | Hallazgo principal cuantificado (textual) | Fuente consultada |
|---|---|---|---|---|
| Banz, R. W. (1981). "The relationship between return and market value of common stocks" | *JFE* 9(1), 3–18, **marzo de 1981**. Recibido en junio de 1979; versión final en septiembre de 1980 | Acciones del NYSE; datos 1926–1975; pruebas **1936–1975** | Tabla I: prima de tamaño γ₁ = **−0.00052 (t = −2.92)** en 1936–1975; −0.00043 (t = −2.12) en 1936–1955 y −0.00062 (t = −2.09) en 1956–1975. "The difference in returns between the smallest firms and the remaining ones is, on average, about 0.4 percent per month". Tabla 3: muy pequeñas largas y muy grandes cortas, **1.52% al mes** (19.8% anualizado) | PDF (copia en un expediente de la Florida PSC), leído con `pypdf` |
| Fama, E. F. y French, K. R. (1992). "The Cross-Section of Expected Stock Returns" | *JF* 47(2), 427–465, **junio de 1992** | NYSE, AMEX y NASDAQ no financieras, **julio de 1963 a diciembre de 1990** | "Average returns rise from 0.30% for the lowest BE/ME portfolio to 1.83% for the highest, a difference of **1.53% per month**". Pendiente de Fama-MacBeth de ln(BE/ME): **0.50% (t = 5.71)**; ln(ME): t = −2.58 | PDF (people.hec.edu/rosu), leído con `pypdf` |
| Jegadeesh, N. y Titman, S. (1993). "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency" | *JF* 48(1), 65–91, **marzo de 1993** | NYSE y AMEX, **enero de 1965 a diciembre de 1989** | Tabla I, panel A, J = 6 y K = 6: comprar-vender **0.0095 al mes (t = 3.07)**. "Realizes a compounded excess return of 12.01% per year on average". Deciles equiponderados | PDF (copia JSTOR en bauer.uh.edu), leído con `pypdf` |
| Fama, E. F. y French, K. R. (2015). "A five-factor asset pricing model" | *JFE* 116(1), 1–22. Recibido el 12-may-2014; **en línea el 29-oct-2014**; número de **abril de 2015** [I: el mes del número no se leyó en la fuente primaria; es consistente con el CFA Digest 2015/04] | **Julio de 1963 a diciembre de 2013, 606 meses** | Tabla 4, panel A, factores 2×3 (% al mes, t): Mkt-RF 0.50 (2.74), SMB **0.29 (2.31)**, HML **0.37 (3.20)**, RMW **0.25 (2.92)**, CMA **0.33 (4.07)** | PDF (tevgeniou.github.io), leído con `pypdf` |
| Daniel, K. y Moskowitz, T. J. (2016). "Momentum crashes" | *JFE* 122(2), 221–247, 2016 (mes del número: noviembre [I]). Versión NBER w20439, agosto de 2014 | EUA, **1927:01 a 2013:03** | Tabla 2 (WML de deciles 12-2): peores meses 1932-08 **−74.36%**, 1932-07 −60.98%, 2001-01 −49.19%, 2009-04 −45.52%, 1939-09 −43.83%, 1933-04 −43.14%, 2009-03 −42.28%, 2002-11 −37.04%, 1938-06 −33.36%, 2009-08 −30.54%, 1931-06 −29.72%, 1933-05 −28.90%, 2001-11 −25.31%, 2001-10 −24.98%, 1974-01 −24.04%. "Fourteen of the 15 worst momentum returns occur when the lagged two-year market return is negative. All occur in months where the market rose contemporaneously" | PDF NBER w20439, leído con `pypdf` |
| McLean y Pontiff (2016) | *JF* 71(1), 5–32 | 97 predictores; muestra de cada estudio original | Resumen: **−26%** fuera de muestra y **−58%** después de publicar. Método (versión de trabajo de 2013): cada rendimiento mensual se divide entre la media dentro de muestra del predictor; se regresa sobre una dummy "post-muestra" (después del fin de la muestra y antes de publicar) y otra "post-publicación"; errores agrupados por mes. Fecha de publicación = año y número de la revista; alternativa, la fecha de SSRN. **Las versiones de trabajo (2012 y 2013, 82 características) reportaban ~10% y ~35%**: las cifras cambiaron entre versiones | Resumen de la versión publicada (WebSearch). PDFs de las versiones de trabajo leídos con `pypdf` |

**Advertencia de construcción.** Ninguno de los artículos originales usa la construcción de la biblioteca de French: SMB, HML y Mom son 2×3, ponderados por valor, con cortes del NYSE (30/70 o mediana). Banz y JT usan portafolios extremos (muy pequeñas o deciles equiponderados); FF92 usa deciles y regresiones de Fama-MacBeth. **Solo FF 2015 (tabla 4) usa la misma construcción** que los archivos de hoy. Por eso la magnitud solo se compara contra FF 2015. Contra los demás se compara el signo y la significancia.

**Mecanismo económico.**

- **Sesgo estadístico.** El artículo original elige muestra y especificación con los datos a la vista. Fuera de su muestra, la prima debería bajar aunque nadie opere la anomalía. McLean-Pontiff atribuyen a esto el −26%, que es una cota superior.
- **Aprendizaje y arbitraje.** Si la prima es un error de precio, publicarla atrae capital que la arbitra, y cae más: −58% en total. Si la prima es compensación por riesgo, publicar no debería cambiarla, salvo por el sesgo estadístico. Los límites al arbitraje (riesgo idiosincrático, iliquidez, cortos caros) frenan la corrección.
- **Crashes de momentum.** En mercados bajistas, los perdedores se comportan como una opción de compra sobre el mercado: el portafolio largo-corto pierde mucho cuando el mercado rebota (DM 2016).
- **"Muerte del value" 2007–2020.** El capítulo 03 cita a Arnott et al. (contracción del múltiplo relativo entre value y growth) y a los intangibles mal medidos. **Aquí no se prueba el mecanismo**: solo se miden magnitud, fechas y lo ocurrido después.

**Hipótesis (signo y magnitud esperados):**

- **H1, datos de hoy contra el artículo.** En la muestra original de cada artículo, la media mensual del factor en los datos de hoy es > 0 con t iid ≥ 2 para HML (1963-07 a 1990-12), Mom (1965-01 a 1989-12), RMW y CMA (1963-07 a 2013-12). Para SMB (1936-01 a 1975-12) también se espera > 0 con t ≥ 2, aunque SMB es una construcción más suave que la de Banz. **H1-magnitud:** en 1963-07 a 2013-12, las medias de hoy de SMB, HML, RMW y CMA quedan a ±0.05 pp mensuales de la tabla 4 de FF 2015 (0.29, 0.37, 0.25 y 0.33).
- **H2, decaimiento post-publicación (la réplica de McLean-Pontiff).** El coeficiente agrupado de la dummy post-publicación es b₂ < 0, con decaimiento D = −b₂ cercano a 0.58. Además, cada uno de los cinco factores tiene una media post-publicación menor que su media dentro de muestra.
- **H3, decaimiento fuera de muestra y antes de publicar.** b₁ < 0, cerca de −0.26. Es muy imprecisa: solo son 152 meses-factor (63 + 18 + 39 + 16 + 16). Es descriptiva y no entra en el estado.
- **H4, crashes de momentum.** En el Mom de French (1927-01 a 2026-07): (a) al menos 10 de los 15 peores meses tienen un rendimiento de mercado acumulado negativo en los 24 meses previos; (b) al menos 12 de los 15 tienen un rendimiento de mercado positivo en el mismo mes; (c) en la ventana de DM (1927-01 a 2013-03), al menos 8 de los 15 peores meses de DM están entre los 15 peores de Mom; (d) la media de Mom en meses "osos" (mercado de 24 meses < 0) es menor que en los demás meses.
- **H5, "muerte del value".** El índice Π(1+HML) tiene, entre 2007-01 y 2020-12, una caída desde su máximo previo de al menos −50%. La media de HML en 2007-01 a 2020-12 es < 0. Desde el valle hasta 2026-07, el acumulado es positivo, pero el índice sigue por debajo de su máximo previo.
- **H6, regla 7 del capítulo 02 (control de crash).** Reducir a la mitad la exposición a Mom cuando el mercado acumula < 0 en 24 meses **y** la volatilidad del mes previo supera su percentil 80 (`MOM_ctrl_osovol_50`) produce un Sharpe mayor y un MDD menos severo que mantener Mom siempre. Se prueba en el tramo de DM (desarrollo) y después de DM (prueba).

### 2. Criterio de refutación

- **Métrica principal.** D = −b₂: el decaimiento post-publicación agrupado, como fracción de la media dentro de muestra.
  - Se estima con la regresión de McLean-Pontiff sobre los meses dentro de muestra, fuera de muestra y post-publicación de los cinco factores: y_it = r_it / media_IS_i = a + b₁·PostMuestra + b₂·PostPub + e. La fórmula es exacta: a = 1, y b₂ = media de y en post − 1.
  - Error estándar agrupado por mes, con la corrección G/(G−1)·(N−1)/(N−K), para comparar con el artículo.
  - Para decidir se usa un **IC 95% por bootstrap de bloques móviles**: bloques de 12 meses calendario sobre todo el panel, 5,000 repeticiones y semilla 20260925. El bootstrap vuelve a estimar la media dentro de muestra en cada repetición, así que recoge la incertidumbre del denominador, que la regresión trata como fija.
- **Secundarias.**
  - Decaimiento por factor, 1 − media_post/media_IS, con IC bootstrap.
  - Promedio simple de los cinco decaimientos.
  - Diferencia de medias (post − IS) en pp mensuales, con t = Δ/√(ee_NW,post² + ee_NW,IS²), usando el EE de Newey-West con 6 rezagos de cada tramo.
  - Sharpe anualizado (media/desv·√12), rendimiento geométrico anual, t iid y t NW(6).
- **Condición A (datos).** HML, Mom, RMW y CMA tienen media > 0 con t iid ≥ 2 en su muestra original. Además, H1-magnitud se cumple para al menos 3 de 4 factores (SMB, HML, RMW y CMA contra FF 2015).
- **Estado de la réplica** (regla fijada ahora):
  - **Replicado:** se cumple A; D > 0; el límite inferior del IC 95% de D es > 0; el IC contiene 0.58; y los cinco factores tienen media_post < media_IS.
  - **Replicado con diferencias:**
    - Se cumple A (o falla para un solo factor) y D > 0, pero el IC de D incluye 0 o excluye 0.58.
    - O se cumple todo lo de "Replicado" salvo que algún factor tiene media_post ≥ media_IS.
  - **No replicado:** D ≤ 0, o A falla para 2 o más factores.
- **Razones inestables.** Si en más de 2.5% de las repeticiones del bootstrap la media dentro de muestra de un factor es ≤ 0, el IC de la razón de ese factor se marca "no informativo". También se reporta D agrupado sin los factores cuya t iid dentro de muestra sea < 2 (sensibilidad; no cambia el estado).
- **Veredictos separados** (no cambian el estado principal): H4 y H5 quedan "confirmada" o "no confirmada" según los umbrales de la sección 1.
- **H6:**
  - "Confirmada dentro de muestra" si en desarrollo `MOM_ctrl_osovol_50` tiene Sharpe mayor **y** MDD menos negativo que `MOM_ref_siempre`.
  - "Confirmada fuera de muestra" si además ocurre lo mismo en prueba.
  - "No informativa fuera de muestra" si la regla nunca se activa en prueba (w = 1 todos los meses).
  - "No confirmada" en cualquier otro caso.
  - Aunque se confirme, la regla **no** es candidata para dinero si su DSR es < 0.95.
- **DSR.** Se reporta el DSR con N = número de variantes con `es_prueba=1`, que por diseño es 10 (sección 8, bloque D), en el segmento de selección `desarrollo`. Siguiendo la práctica de R02, también se reporta con V por familia (tenencia de factores y control de crash), y **se decide con el DSR menor**.
- **Bloque C (afirmaciones del sistema).** Cada cifra se considera "reproducida" si coincide a ±0.01 en el último dígito reportado con alguna de las definiciones declaradas (media ×12 o geométrica anual; t iid o t NW(6)). Se dice cuál coincidió. Entre ±0.01 y ±0.05 es "diferencia menor". Por encima de ±0.05 es "discrepancia", y se registra en el registro de errores del sistema.

### 3. Datos y licencia

| Serie | Fuente y archivo | Versión / huella | Frecuencia | Condiciones de uso |
|---|---|---|---|---|
| Mkt-RF, SMB, HML y RF | French `F-F_Research_Data_Factors_CSV.zip` | CRSP 202607; sha256 `b840dba55d319f48…` (prefijo visto al cargar metadatos); el script imprime el completo | mensual (1926-07 a 2026-07, 1201 meses) | Pendiente de verificar |
| Mom | French `F-F_Momentum_Factor_CSV.zip` | CRSP 202607; sha256 `7ee14e892b0f7044…` (el mismo prefijo que V01) | mensual (1927-01 a 2026-07, 1195 meses) | Pendiente de verificar |
| SMB, HML, RMW, CMA (2×3) y RF | French `F-F_Research_Data_5_Factors_2x3_CSV.zip` | CRSP 202607; sha256 `b8653b411cc5e289…` | mensual (1963-07 a 2026-07, 757 meses) | Pendiente de verificar |
| Mkt-RF diario (volatilidad del mes) | French `F-F_Research_Data_Factors_daily_CSV.zip` | CRSP 202607; sha256 `1916d331c2c51d2a…` | diaria (1926-07-01 a 2026-07-31) | Pendiente de verificar |

**Versión de datos.** La página de la biblioteca (consultada el 2026-09-25) documenta varios cambios:

- Desde enero de 2025 usa el formato CIZ de CRSP: los rendimientos mensuales ahora son rendimientos diarios compuestos, con dividendos reinvertidos en la fecha ex.
- Hubo revisiones previas: enero de 2015 (acciones en circulación de 1925 a 1946), agosto de 2018 (definición de OP, que afecta RMW), septiembre de 2020 (se retira el ajuste FASB 106 del *book equity*, que afecta HML) y septiembre de 2021 (vínculos CRSP-Compustat).

No se consiguió una versión anterior de los archivos: la Wayback Machine no tiene copias del zip y su índice CDX está bloqueado por la política de red. Por eso **el efecto de esos cambios no se mide directamente**. La comparación contra la tabla 4 de FF 2015, que usa datos de 2014, es la única medida indirecta de la diferencia de versión.

### 4. Universo

- **Factores de French**, largo-corto de acciones de EUA (NYSE, AMEX y NASDAQ en CRSP). La historia viene de CRSP, que incluye las empresas deslistadas, así que no hay sesgo de supervivencia en el sentido clásico. **No son invertibles:** son brutos, sin costos, con cortos y con rebalanceo interno. Ningún ETF en GBM los replica.
- **Definición principal de cada factor:**
  - SMB y HML: archivo de 3 factores, porque tiene historia desde 1926.
  - RMW y CMA: archivo de 5 factores 2×3.
  - Mom: archivo de momentum.
  - Sensibilidad: SMB y HML del archivo de 5 factores (desde 1963-07).
- **Mercado:** Mkt-RF + RF. Se usa como referencia y para el estado "oso".

### 5. Fecha de disponibilidad

- **Parte descriptiva (bloques A, B y C).** No hay decisiones de *trading*: se miden promedios históricos. La serie es la versión de hoy (CRSP 202607), no la que se conocía en cada fecha. La biblioteca recalcula la historia en cada versión (sección 3). Es una limitación declarada.
- **Tenencia de factores con el motor (bloque D, familia F).** La exposición es siempre 1, así que no depende de información.
- **Control de crash (bloque D, familia MOM).** Al cierre del mes t−1 se decide w_t. La señal ve dos `extras` fechados al último día calendario del mes de cálculo:
  - `mkt`: el rendimiento mensual del mercado. El estado "oso" es Π(1+mkt) − 1 < 0 sobre los últimos 24 meses visibles (t−24 a t−1).
  - `vol`: la desviación estándar de Mkt-RF diario dentro de cada mes calendario, con al menos 15 días.

  El motor solo entrega entradas con fecha ≤ fin de t−1. El Mom de French del mes t se forma con rendimientos de t−12 a t−2, conocidos al inicio de t.
- **Ejecución.** Al cierre del mes, igual que en R02. No se modela el rezago de ejecución.

### 6. Periodo

**Tramos de McLean-Pontiff por factor.** Un mes con fecha ≤ al corte pertenece al tramo anterior. El mes de publicación queda en el tramo "antes", según la convención del laboratorio.

| Factor | Primer dato | Pre-muestra (sensibilidad) | Muestra original (IS) | Fuera de muestra, antes de publicar (OOS) | Publicación (corte) | Post-publicación |
|---|---|---|---|---|---|---|
| SMB (Banz 1981) | 1926-07 | 1926-07 a 1935-12 | 1936-01 a 1975-12 (480) | 1976-01 a 1981-03 (63) | 1981-03-31 | 1981-04 a 2026-07 (544) |
| HML (FF 1992) | 1926-07 | 1926-07 a 1963-06 | 1963-07 a 1990-12 (330) | 1991-01 a 1992-06 (18) | 1992-06-30 | 1992-07 a 2026-07 (409) |
| Mom (JT 1993) | 1927-01 | 1927-01 a 1964-12 | 1965-01 a 1989-12 (300) | 1990-01 a 1993-03 (39) | 1993-03-31 | 1993-04 a 2026-07 (400) |
| RMW y CMA (FF 2015) | 1963-07 | — | 1963-07 a 2013-12 (606) | 2014-01 a 2015-04 (16) | 2015-04-30 | 2015-05 a 2026-07 (135) |

Entre paréntesis va el número de meses esperado. El script verifica cada conteo y se detiene si alguno no coincide.

- **Fechas alternativas** (sensibilidad; solo donde la fecha temprana está verificada):
  - Banz, 1979-06-30: recepción del manuscrito.
  - FF 2015, 2014-10-31: publicación en línea.
  - Para FF 1992 y JT 1993 no hay una fecha de versión de trabajo verificada, así que no hay sensibilidad.
- **Décadas.** 1926-07 a 1929-12 (parcial), 1930–1939, …, 2010–2019 y 2020-01 a 2026-07 (parcial), para cada factor desde su primer dato.
- **"Muerte del value".** 2007-01 a 2020-12. Se reportan también 1992-01 a 2006-12 y 2021-01 a 2026-07, y el tramo desde el mes siguiente al valle hasta 2026-07.
- **Control de crash (familia MOM).** Mom desde 1927-01 con `min_historia` = 10, así que el primer mes evaluado es 1927-11. Cortes:
  - 2013-03-31: fin de la muestra de DM.
  - 2016-11-30: número de la JFE.

  Quedan desarrollo = 1927-11 a 2013-03, validación = 2013-04 a 2016-11 y prueba = 2016-12 a 2026-07. La prueba se mira una sola vez.

### 7. Limpieza

Reglas fijadas antes de ver los resultados:

- Los faltantes −99.99 y −999 se convierten en faltantes y se omiten; la carga de metadatos reportó 0.
- El script verifica varias cosas y se detiene si alguna falla:
  - Fechas mensuales estrictamente crecientes y en fin de mes.
  - Tabla principal mensual separada de la anual (formato posterior a 2025).
  - Conteos 1201, 1195 y 757.
- **Sin cambios después de ver resultados.** No se eliminan valores extremos: los crashes **son** el objeto de estudio.
- **Ancla del motor.** Para que el motor evalúe desde el primer mes de la muestra original, cada serie de la familia F lleva al inicio un periodo ancla con rendimiento 0.0 (activo y efectivo), fechado en el fin del mes previo. Ese periodo solo fija la fecha inicial de la curva; no entra en ninguna métrica y la señal de comprar y mantener no lo lee. El script verifica que el Sharpe del motor en `desarrollo` coincide con el cálculo directo (diferencia < 1e-9) y se detiene si no.

### 8. Regla y variantes planeadas

**Bloque A: primas y decaimiento (cálculo directo, sin motor).**

- **Por factor y por tramo** (pre-muestra, IS, OOS, post y completo) y **por década** se calculan:
  - n y media mensual (%).
  - Desviación estándar.
  - t iid y t NW(6) (`herramientas/estadistica.newey_west`).
  - Sharpe anualizado (media/desv·√12), media ×12 y rendimiento geométrico anual (Π(1+F)^(12/n) − 1).
- **Decaimiento.**
  - Regresión agrupada de McLean-Pontiff (sección 2).
  - Decaimiento por factor y promedio simple.
  - Diferencia de medias con t NW.
  - IC por bootstrap de bloques de 12 meses (5,000 repeticiones, semilla 20260925). Si en una repetición un tramo queda sin observaciones, esa repetición se excluye solo para esa estadística y se reporta cuántas se excluyeron.
- **Sensibilidades del bloque A** (lista cerrada):
  1. Fechas de publicación alternativas (Banz 1979-06 y FF 2015 2014-10).
  2. SMB y HML del archivo de 5 factores.
  3. D agrupado sin los factores con t iid < 2 dentro de muestra.
  4. Pre-muestra como tramo adicional (media y t), para HML (1926-07 a 1963-06), Mom (1927-01 a 1964-12) y SMB (1926-07 a 1935-12).

**Bloque B: crashes y "muerte del value" (diagnósticos).**

- **Crashes.**
  - Los 15 peores meses de Mom, en toda la muestra y en la ventana de DM (1927-01 a 2013-03). Para cada uno: el mercado acumulado en los 24 meses previos, el mercado del mes y la bandera "oso".
  - Coincidencias con la tabla 2 de DM.
  - Los 5 peores meses después de 2013-03.
  - Media de Mom en meses "oso" contra "normal", con t NW(6), para toda la muestra, 1927-01 a 2013-03 y 2013-04 a 2026-07.
  - Los 3 peores *drawdowns* de Π(1+F) de cada factor.
- **"Muerte del value".** Sobre Π(1+HML):
  - Máximo previo, valle, profundidad y meses entre pico y valle.
  - Rendimiento desde el valle hasta 2026-07 y distancia al máximo en 2026-07.
  - HML por año calendario de 2007 a 2026 (2026 hasta julio).
  - La misma medición con HML del archivo de 5 factores y con la curva RF+HML del motor.
- **Temporada de 6 meses.** Para cada factor, la fracción de ventanas de 6 meses traslapadas con acumulado > 0, antes y después de la publicación. Es relevante para `temporada_meses` = 6 de la arena.

**Bloque C: afirmaciones del sistema que se verifican** (cifras textuales de los capítulos):

| # | Fuente | Afirmación (serie, ventana: cifra) |
|---|---|---|
| C1 | cap. 02 §5.1, tabla (archivo de 5 factores + Mom; "media aritmética anualizada en % (t)") | 1963/07–2026/07: Mkt-RF 7.19 (3.70), SMB 2.25 (1.71), HML 3.59 (2.77), RMW 3.08 (3.10), CMA 2.96 (3.27), Mom 7.25 (3.96) |
| C2 | ídem | 1963/07–1991/06: Mkt-RF 4.55 (1.52), SMB 3.68 (1.89), HML 4.96 (2.98), RMW 2.39 (2.34), CMA 3.76 (2.97), Mom 9.55 (4.20) |
| C3 | ídem | 1992/01–2026/07: Mkt-RF 9.06 (3.54), SMB 1.14 (0.63), HML 2.81 (1.45), RMW 3.58 (2.22), CMA 2.51 (1.95), Mom 4.92 (1.77) |
| C4 | ídem y examen P9 | 2016–2025: Mkt-RF 12.96 (2.60), SMB −2.21 (−0.68), HML −0.49 (−0.12), RMW 3.55 (1.48), CMA −0.65 (−0.24), Mom 0.34 (0.08) |
| C5 | ídem | 2021–2025: Mkt-RF 10.42, SMB −4.66, HML 8.07, RMW 5.85, CMA 1.30, Mom 2.31. Ene–jul 2026 acumulado: +7.4, +6.6, +12.3, −5.8, +7.2, +10.2 |
| C6 | cap. 02 §5.1, series largas (archivo de 3 factores + Mom) | HML 4.26 (3.46) en 1926–2026; 5.02 (3.18) antes de 1992; 2.81 (1.45) de 1992 en adelante; peor DD −57.8% de dic-2006 a sep-2020 |
| C7 | ídem | Mom 7.41 (4.55) en 1927–2026; 8.53 (4.15) en 1927–1989; 4.49 (1.54) en 1994–2026; 2.47 (0.72) desde 2000 |
| C8 | ídem | DD de Mom −78.4% (1932-06 a 1939-09) y −57.8% (2008-11 a 2009-09); abril de 2009 −34.4%; marzo a septiembre de 2009 acumulado −56.4% |
| C9 | ídem | SMB 1.99 (1.82) en 1926–2026; 0.66 (0.36) desde 1992 |
| C10 | ídem | HML+Mom 50/50 en 1963–2026: 5.42% (t 5.34, Sharpe 0.67); correlación HML-Mom −0.19 (−0.30 en 2016–25); 2016–2025: −0.07% (Sharpe −0.01). Promedio equiponderado de los cinco factores: Sharpe 0.84 (t 6.65) en toda la muestra y 0.11%/año (t 0.07) en 2016–2025 |
| C11 | cap. 03 §5.1 ("rend. geom. anual / Sharpe") | HML 1963-07–1991-12: 4.23% / 0.52 (t 2.75); 1992-01–2026-07: 2.19% / 0.25 (t 1.45); 1992–2006: 7.61% / 0.72; 2007–2020: −5.67% |
| C12 | ídem | RMW 1963-07–2013-12: 2.95% / 0.41 (t 2.94); 2014-01–2026-07: 2.23% / 0.30 (t 1.08). CMA en las mismas ventanas: 3.72% / 0.56 y −1.10% / −0.10 |
| C13 | cap. 03 §5.4 y examen P12 | HML −57.8% de dic-2006 a sep-2020; +66.8% desde entonces; −29.6% bajo el pico a jul-2026 |

En C1–C5 se prueban el archivo de 5 factores y el de 3 factores para SMB y HML. En C10 y C13 se prueban ambos archivos para HML. Se reporta qué combinación coincide.

**Bloque D: corridas del motor** (`herramientas/backtest.backtest_senal`, `id_replica="R03"`). La lista es cerrada. El activo es RF + F, el efectivo es RF (French) y la moneda es USD.

| # | Variante (`es_prueba=1`) | Activo y periodo | Señal | Cortes |
|---|---|---|---|---|
| 1 | `F_SMB` | RF+SMB, IS a 2026-07 (ancla 1935-12-31) | w = 1 | 1975-12-31, 1981-03-31 |
| 2 | `F_HML` | RF+HML (3 factores), ancla 1963-06-30 | w = 1 | 1990-12-31, 1992-06-30 |
| 3 | `F_MOM` | RF+Mom, ancla 1964-12-31 | w = 1 | 1989-12-31, 1993-03-31 |
| 4 | `F_RMW` | RF+RMW, ancla 1963-06-30 | w = 1 | 2013-12-31, 2015-04-30 |
| 5 | `F_CMA` | RF+CMA, ancla 1963-06-30 | w = 1 | 2013-12-31, 2015-04-30 |
| 6 | `F_EW5` | RF + promedio de SMB, HML (3 factores), Mom, RMW y CMA, ancla 1963-06-30 | w = 1 | 2013-12-31, 2015-04-30 (el combo es conocible completo solo después de FF 2015) |
| 7 | `MOM_ctrl_osovol_50` (regla 7 del cap. 02) | RF+Mom desde 1927-01, `min_historia` = 10 | w = 0.5 si oso **y** vol_{t−1} > p80; si no, 1 | 2013-03-31, 2016-11-30 |
| 8 | `MOM_ctrl_oso_50` | ídem | w = 0.5 si oso; si no, 1 | ídem |
| 9 | `MOM_ctrl_osovol_0` | ídem | w = 0 si oso **y** vol > p80; si no, 1 | ídem |
| 10 | `MOM_ctrl_oso_0` | ídem | w = 0 si oso; si no, 1 | ídem |

**Definiciones de la familia MOM:**

- "Oso" exige 24 meses visibles de `mkt`. Sin ellos, oso = falso.
- p80 es el percentil 80 de rango más cercano (el elemento ⌈0.8·n⌉ de la lista ordenada) de **todas** las `vol` visibles, incluida la de t−1, y exige al menos 60 valores. Sin ellos, vol alta = falso.
- Las familias 1–6 corren **brutas** (comisión y spread en 0), igual que los artículos. Las 7–10, también.

**Referencias** (`es_prueba=0`, nota "referencia"):

- `REF_MKT_<F>` para F en SMB, HML, MOM, RMW, CMA y EW5: mercado Mkt-RF+RF con la misma ancla, periodo y cortes que la variante F.
- `MOM_ref_siempre` (w = 1), `MOM_ref_efectivo` (w = 0), `MOM_ref_sma10` (`senal_media_movil(10)` sobre el índice RF+Mom; es la regla sencilla del mismo tipo) y `MKT_ref_mom` (mercado con el periodo y los cortes de la familia MOM).

**Sensibilidades del motor** (`es_prueba=0`, con nota; lista cerrada):

1. Las 10 variantes y las 10 referencias con costos por defecto (0.29% + 0.05%) y con spread "medio" (0.29% + 0.15%).
2. `F_SMB` y `F_RMW` con los cortes de las fechas alternativas (1975-12-31 y 1979-06-30; 2013-12-31 y 2014-10-31). `F_CMA` también, con la fecha alternativa de FF 2015.
3. `F_SMB_ff5` y `F_HML_ff5` (archivo de 5 factores, ancla 1963-06-30, mismos cortes que `F_SMB` y `F_HML`). El desarrollo de `F_SMB_ff5` empieza en 1963-07, no en 1936.
4. Historia completa: `F_SMB_hist` (desde 1926-07), `F_HML_hist` (desde 1926-07) y `F_MOM_hist` (desde 1927-01), con los mismos cortes. Su desarrollo incluye la pre-muestra.

**Exposición, efectivo y moneda.** w ∈ [0, 1]. El efectivo es la RF de French. Todo en USD, sin conversión a MXN: el factor es un diferencial largo-corto sin inversión; convertir RF+F a pesos solo agregaría varianza cambiaria al colateral, y no aporta a la pregunta del decaimiento. Se declara como **no probado**.

### 9. Costos y comparación simple

- **Costos.** Los artículos no descuentan costos, y las corridas principales tampoco (brutas). Las sensibilidades cobran el costo de GBM por defecto y el "medio", pero **solo sobre cambios en la exposición al factor** (el *overlay*). **No incluyen la rotación interna del factor**, que en Mom es mensual y alta. Cambiar la exposición a un largo-corto real requiere operar las dos patas: el costo real sería del orden del doble. Por eso esas corridas **subestiman** el costo y solo sirven para cumplir el protocolo.
- **No implementable en GBM.** Requiere cortos y apalancamiento bruto > 1; `apalancamiento.bruto_max_fase_1` = 1.0.
- **Reglas sencillas con idénticas condiciones.**
  - Familia F: mercado comprar y mantener (`REF_MKT_<F>`) y efectivo.
  - Familia MOM: Mom siempre, efectivo, SMA10 sobre Mom y mercado.

---

## RESULTADOS (se llenan después de correr)

