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

> **Corrida única:** 2026-09-25, de 05:56:41 a 05:56:45 UTC. Todas las cifras son las que imprimió `python3 laboratorio/replicas/R03.py`, sin redondear a mano. La salida completa, con todas las tablas, está en `laboratorio/replicas/R03-salida.txt`, y las cifras en formato de máquina en `R03-resultados.json`.
>
> **Huella del pre-registro.** El archivo con las secciones 1 a 9 terminó de escribirse a las 05:48:00 UTC. Su sha256 a las 05:48:04 UTC, antes de cualquier cálculo, fue `ca284534568dd6dd7114d0e201a44bb634df3f9293a0f936fa739ccaa88b33d7`. Los primeros 29,551 bytes de esta ficha deben conservar esa huella: `head -c 29551 R03-primas-de-factores-pre-post-publicacion.md | sha256sum`.
>
> **Convenciones.** Cifras brutas, largo-corto y en USD. "Media" es el promedio mensual en %. El t NW usa 6 rezagos. Sharpe = media/desv·√12. "Geo" es el rendimiento geométrico anual de Π(1+F). D es el decaimiento como fracción de la media dentro de muestra.

### Desviaciones del pre-registro

| Fecha | Qué cambió | Por qué | ¿Invalida el tramo de prueba? |
|---|---|---|---|
| 2026-09-25 | **Tolerancia del bloque C.** El texto "±0.01 en el último dígito reportado" es ambiguo. Se aplicó como **1 unidad del último dígito publicado**: 0.01 si la cifra trae dos decimales y 0.1 si trae uno. Con la lectura literal (±0.01 absoluto), 12 de las 116 cifras (todas publicadas con un decimal; diferencia máxima 0.0463) serían "diferencia menor" en vez de "reproducida" | Ambigüedad del texto | No. No cambia datos, reglas, corridas ni el estado |
| 2026-09-25 | **Archivo para H1-magnitud.** El pre-registro no fijó el archivo. Se usó el de 5 factores porque es la construcción de la tabla 4 de FF 2015 (SMB promedio de tres ordenamientos). Con el SMB del archivo de 3 factores, la diferencia sería −0.060 pp (0.230 contra 0.29), fuera de tolerancia. Aun así quedarían 3 de 4 dentro, y la condición A se sostiene igual | Aclaración | No |
| 2026-09-25 | **"A falla para 2 o más factores".** Se contó el número de factores distintos que fallan cualquiera de las dos partes de A (t ≥ 2 o magnitud). No hubo fallas, así que la aclaración no cambia nada | Aclaración | No |
| 2026-09-25 | **Ventanas de 6 meses (B.7).** El código, escrito antes de correr, define "antes" como las ventanas que terminan en o antes de la publicación y "después" como las que empiezan después. Las ventanas que cruzan la fecha se excluyen. El texto del pre-registro no daba ese detalle | Definición | No; es un diagnóstico |
| 2026-09-25 | **Bootstrap de D_oos (H3).** En 893 de 5,000 repeticiones algún factor quedó sin meses OOS. D_oos agrupado se calculó con los factores que sí tenían meses OOS; el pre-registro decía excluir la repetición para esa estadística. Por factor, las repeticiones sin OOS sí se excluyeron | Detalle de implementación | No. D_oos es descriptivo (H3) y no entra en el estado |

No hubo corridas fallidas. El CSV tiene exactamente una ejecución: 68 corridas × 4 segmentos = 272 filas.

### 10. Variantes probadas

- **Archivo.** `laboratorio/replicas/R03-variantes.csv`: 272 filas y 68 corridas. Cada corrida tiene 4 filas: completo, desarrollo, validación y prueba.
- **Variantes con `es_prueba=1`: 10** (las que deduplica `sharpe_deflactado_de_registro`):
  - `F_SMB`, `F_HML`, `F_MOM`, `F_RMW`, `F_CMA` y `F_EW5`.
  - `MOM_ctrl_osovol_50`, `MOM_ctrl_oso_50`, `MOM_ctrl_osovol_0` y `MOM_ctrl_oso_0`.
- **Referencias y sensibilidades:** 58 corridas con `es_prueba=0` y nota.
  - 10 referencias.
  - 40 de costos: 20 × {defecto, medio}.
  - 3 con fecha alternativa, 2 con el archivo de 5 factores y 3 con historia completa.
- **Pruebas fuera del registro:** ninguna corrida de estrategia. Después de la corrida se hicieron dos verificaciones aritméticas independientes, sin variantes nuevas:
  - El índice Π(1+Mom) en 2026-07 está 31.94% abajo de su pico de 2008-11. El máximo desde 2009 es 505.21 contra 521.37 del pico.
  - La lista de meses "oso" en el tramo de prueba.
  - Se usa N = 10.

**Salida de `sharpe_deflactado_de_registro`** (umbral 0.95; SR anualizado):

| Lectura | Segmento | Variante | DSR | ¿Cumple? | N | V por periodo | SR anual | SR0 anual | n_obs | PSR sin deflactar |
|---|---|---|---|---|---|---|---|---|---|---|
| Por defecto: mejor de las 10, V de todas | desarrollo | F_EW5 | 1.0000 | Sí | 10 | 0.004836 | 1.0544 | 0.3793 | 606 | 1.0000 |
| Mejor de la familia F, V de F | desarrollo | F_EW5 | 0.9999 | Sí | 10 | 0.007497 | 1.0544 | 0.4723 | 606 | 1.0000 |
| Mejor de la familia MOM, V de MOM | desarrollo | MOM_ctrl_oso_0 | 1.0000 | Sí | 10 | 0.000919 | 0.8708 | 0.1653 | 1025 | 1.0000 |
| Pre-especificada, V de todas | desarrollo | F_SMB | 0.1134 | No | 10 | 0.004836 | 0.1936 | 0.3793 | 480 | 0.8961 |
| Pre-especificada, V de todas | desarrollo | F_HML | 0.8440 | No | 10 | 0.004836 | 0.5752 | 0.3793 | 330 | 0.9985 |
| Pre-especificada, V de todas | desarrollo | F_MOM | 0.9741 | Sí | 10 | 0.004836 | 0.8028 | 0.3793 | 300 | 0.9999 |
| Pre-especificada, V de todas | desarrollo | F_RMW | 0.5900 | No | 10 | 0.004836 | 0.4130 | 0.3793 | 606 | 0.9973 |
| Pre-especificada, V de todas | desarrollo | F_CMA | 0.9047 | No | 10 | 0.004836 | 0.5618 | 0.3793 | 606 | 1.0000 |
| Pre-especificada, V de todas | desarrollo | MOM_ctrl_osovol_50 (regla 7) | 0.9721 | Sí | 10 | 0.004836 | 0.6215 | 0.3793 | 1025 | 1.0000 |
| Por defecto: mejor de las 10, V de todas | prueba | MOM_ctrl_oso_0 | 0.7392 | No | 10 | 0.002526 | 0.4920 | 0.2742 | 116 | 0.9262 |
| Mejor de la familia F, V de F | prueba | F_RMW | 0.6241 | No | 10 | 0.001671 | 0.3160 | 0.2230 | 135 | 0.8588 |
| Mejor de la familia MOM, V de MOM | prueba | MOM_ctrl_oso_0 | 0.8735 | No | 10 | 0.000360 | 0.4920 | 0.1036 | 116 | 0.9262 |
| Pre-especificada, V de todas | prueba | F_EW5 | 0.3733 | No | 10 | 0.002526 | 0.1778 | 0.2742 | 135 | 0.7245 |
| Pre-especificada, V de todas | prueba | MOM_ctrl_osovol_50 (regla 7) | 0.5901 | No | 10 | 0.002526 | 0.3502 | 0.2742 | 116 | 0.8530 |

Las demás lecturas en prueba: `F_SMB` 0.0419, `F_HML` 0.3139, `F_MOM` 0.5163, `F_RMW` 0.5566, `F_CMA` 0.1482, `MOM_ctrl_oso_50` 0.6154 y `MOM_ctrl_osovol_0` 0.6958.

**Lectura conservadora:**

- **Desarrollo (dentro de muestra).** `F_EW5` pasa aun con la lectura menor (0.9999). También pasan `F_MOM` (0.9741) y la regla 7 (0.9721).
- **Prueba (después de publicar).** Ninguna de las 10 variantes llega a 0.95. La mejor es 0.8735 (`MOM_ctrl_oso_0`, V de su familia). Con V de todas, esa misma variante tiene 0.7392.
- **Ninguna variante es candidata.** Además, ninguna es implementable en GBM: son largo-corto, sin costos internos y con cortos.

### 11. Resultados

#### 11.1 Primas por tramo de McLean-Pontiff (tabla A.1)

| Factor | Tramo | Ventana | n | Media %/mes | t iid | t NW | Sharpe | Geo % | Veredicto | Mkt-RF en la ventana: media (Sharpe) |
|---|---|---|---|---|---|---|---|---|---|---|
| SMB | PRE | 1926-07 a 1935-12 | 114 | 0.335 | 0.72 | 0.68 | 0.232 | 2.70 | inconcluso | 0.666 (0.231) |
| SMB | IS | 1936-01 a 1975-12 | 480 | 0.157 | 1.22 | 1.10 | 0.194 | 1.43 | inconcluso | 0.663 (0.492) |
| SMB | OOS | 1976-01 a 1981-03 | 63 | 1.223 | 3.62 | 4.14 | 1.581 | 15.22 | apoyo | 0.739 (0.572) |
| SMB | POST | 1981-04 a 2026-07 | 544 | 0.015 | 0.12 | 0.13 | 0.017 | −0.34 | inconcluso | 0.723 (0.560) |
| HML | PRE | 1926-07 a 1963-06 | 444 | 0.450 | 2.17 | 2.12 | 0.357 | 4.43 | apoyo | 0.856 (0.456) |
| HML | IS | 1963-07 a 1990-12 | 330 | 0.425 | 3.02 | 2.63 | 0.575 | 4.81 | apoyo | 0.347 (0.262) |
| HML | OOS | 1991-01 a 1992-06 | 18 | 0.682 | 1.04 | 0.74 | 0.849 | 8.04 | inconcluso | 1.266 (1.105) |
| HML | POST | 1992-07 a 2026-07 | 409 | 0.181 | 1.12 | 0.93 | 0.191 | 1.54 | inconcluso | 0.773 (0.612) |
| MOM | PRE | 1927-01 a 1964-12 | 456 | 0.638 | 2.55 | 2.74 | 0.414 | 5.69 | apoyo | 0.856 (0.463) |
| MOM | IS | 1965-01 a 1989-12 | 300 | 0.821 | 4.01 | 4.31 | 0.803 | 9.49 | apoyo | 0.361 (0.268) |
| MOM | OOS | 1990-01 a 1993-03 | 39 | 1.167 | 2.24 | 1.82 | 1.242 | 14.24 | inconcluso | 0.598 (0.492) |
| MOM | POST | 1993-04 a 2026-07 | 400 | 0.389 | 1.63 | 1.60 | 0.282 | 3.27 | inconcluso | 0.759 (0.596) |
| RMW | IS | 1963-07 a 2013-12 | 606 | 0.268 | 2.94 | 2.57 | 0.413 | 2.95 | apoyo | 0.501 (0.387) |
| RMW | OOS | 2014-01 a 2015-04 | 16 | 0.088 | 0.20 | 0.39 | 0.177 | 0.89 | inconcluso | 0.876 (1.077) |
| RMW | POST | 2015-05 a 2026-07 | 135 | 0.228 | 1.06 | 1.23 | 0.316 | 2.39 | inconcluso | 1.007 (0.773) |
| CMA | IS | 1963-07 a 2013-12 | 606 | 0.324 | 3.99 | 3.48 | 0.562 | 3.72 | apoyo | 0.501 (0.387) |
| CMA | OOS | 2014-01 a 2015-04 | 16 | −0.391 | −1.43 | −2.38 | −1.241 | −4.65 | contraria | 0.876 (1.077) |
| CMA | POST | 2015-05 a 2026-07 | 135 | −0.027 | −0.13 | −0.13 | −0.039 | −0.67 | inconcluso | 1.007 (0.773) |

El tramo COMPLETO de cada factor, el IC 95% y la desviación estándar están en la tabla A.1 de `R03-salida.txt`.

#### 11.2 H1: la muestra del artículo con los datos de hoy

| Factor | Muestra del artículo | Media hoy %/mes (t iid; t NW) | Cifra del artículo | ¿Media > 0 y t iid ≥ 2? |
|---|---|---|---|---|
| SMB | 1936-01 a 1975-12 | 0.157 (1.22; 1.10) | Banz: γ₁ = −0.00052 (t −2.92); muy pequeñas − muy grandes 1.52%/mes | **No** |
| HML | 1963-07 a 1990-12 | 0.425 (3.02; 2.63) | FF92: 1.53%/mes entre deciles de BE/ME; pendiente 0.50 (t 5.71) | Sí |
| MOM | 1965-01 a 1989-12 | 0.821 (4.01; 4.31) | JT93: 6/6, 0.95%/mes (t 3.07) | Sí |
| RMW | 1963-07 a 2013-12 | 0.268 (2.94; 2.57) | FF2015: 0.25 (t 2.92) | Sí |
| CMA | 1963-07 a 2013-12 | 0.324 (3.99; 3.48) | FF2015: 0.33 (t 4.07) | Sí |

**H1-magnitud contra FF 2015, tabla 4** (1963-07 a 2013-12, 606 meses, archivo de 5 factores). Los 4 factores quedan dentro de ±0.05 pp:

| Factor | Artículo | Hoy (CRSP 202607) | Δ pp/mes |
|---|---|---|---|
| SMB | 0.29 (2.31) | 0.280 (2.26) | −0.010 |
| HML | 0.37 (3.20) | 0.382 (3.36) | +0.012 |
| RMW | 0.25 (2.92) | 0.268 (2.94) | +0.018 |
| CMA | 0.33 (4.07) | 0.324 (3.99) | −0.006 |
| Mkt-RF (ref.) | 0.50 (2.74) | 0.501 (2.75) | +0.001 |

**Condición A: se cumple.** Ningún factor falla. H1 **no** se cumple para SMB en la ventana de Banz (t = 1.22).

#### 11.3 Decaimiento post-publicación (la réplica de McLean-Pontiff)

| Factor | n IS / OOS / POST | Media IS | Media POST | Decaimiento POST [IC95 bootstrap] | Rep. con media IS ≤ 0 | Δ POST−IS pp/mes (t NW) |
|---|---|---|---|---|---|---|
| SMB | 480 / 63 / 544 | 0.157 | 0.015 | 90.5% [−511.0%, 695.3%] **(no informativo)** | 13.52% | −0.143 (−0.77) |
| HML | 330 / 18 / 409 | 0.425 | 0.181 | 57.5% [−143.9%, 164.8%] | 0.34% | −0.244 (−0.97) |
| MOM | 300 / 39 / 400 | 0.821 | 0.389 | 52.6% [−24.0%, 112.4%] | 0.00% | −0.432 (−1.40) |
| RMW | 606 / 16 / 135 | 0.268 | 0.228 | 15.1% [−393.8%, 167.6%] | 0.58% | −0.040 (−0.19) |
| CMA | 606 / 16 / 135 | 0.324 | −0.027 | 108.4% [−55.5%, 288.7%] | 0.00% | −0.352 (−1.48) |

- **Regresión agrupada** (4,097 obs., 1,087 meses, errores agrupados por mes): a = 1.000000 y b₂ = −0.6808 (ee 0.3682, t −1.85). Por lo tanto, **D = 68.1%**, con IC95 bootstrap de **[−174.3%, 287.9%]**. McLean-Pontiff reportan 58%.
- **Fuera de muestra, antes de publicar:** b₁ = +2.6832 (ee 1.0034, t 2.67), así que D_oos = −268.3%, con IC95 [−3033.5%, 2997.4%]. McLean-Pontiff reportan 26%. El signo al revés se debe a SMB: en 1976-01 a 1981-03, la euforia de las pequeñas, SMB rindió 1.223%/mes (t 3.62), 7.8 veces su media dentro de muestra.
- **Promedio simple de los cinco decaimientos:** 64.8%, con IC95 [−133.5%, 211.9%].
- **Los cinco factores** tienen media POST < media IS. Ninguna diferencia individual es significativa: el |t| NW máximo es 1.48, de CMA.

#### 11.4 Primas por década (media %/mes con t NW / Sharpe / geo anual %)

| Década | Mkt-RF | SMB | HML | MOM | RMW | CMA |
|---|---|---|---|---|---|---|
| 1926-07 a 1929 | 1.16 (1.30) / 0.70 / 12.6 | −1.05 (−1.69) / −1.31 / −12.3 | 0.23 (0.54) / 0.31 / 2.4 | 1.91 (5.01) / 2.49 / 25.0 | — | — |
| 1930s | 0.46 (0.47) / 0.15 / −0.8 | 0.84 (1.88) / 0.53 / 8.8 | 0.33 (0.49) / 0.15 / 1.0 | −0.02 (−0.03) / −0.01 / −6.9 | — | — |
| 1940s | 0.83 (1.86) / 0.64 / 9.0 | 0.40 (1.64) / 0.59 / 4.5 | 0.80 (2.99) / 1.04 / 9.6 | 0.56 (2.74) / 0.70 / 6.4 | — | — |
| 1950s | 1.31 (4.08) / 1.40 / 16.2 | −0.06 (−0.47) / −0.14 / −0.9 | 0.30 (1.34) / 0.46 / 3.3 | 0.89 (6.41) / 1.36 / 10.9 | — | — |
| 1960s | 0.41 (1.14) / 0.39 / 4.2 | 0.40 (1.31) / 0.54 / 4.5 | 0.28 (1.44) / 0.51 / 3.2 | 0.91 (4.42) / 1.17 / 11.1 | 0.12 (0.58) / 0.25 / 1.3 | −0.08 (−0.38) / −0.14 / −1.2 |
| 1970s | 0.10 (0.20) / 0.07 / −0.3 | 0.29 (0.81) / 0.29 / 2.8 | 0.65 (2.32) / 0.83 / 7.7 | 0.82 (2.73) / 0.75 / 9.3 | −0.05 (−0.30) / −0.11 / −0.7 | 0.52 (2.10) / 0.94 / 6.2 |
| 1980s | 0.71 (1.59) / 0.51 / 7.3 | −0.00 (−0.02) / −0.01 / −0.4 | 0.49 (1.66) / 0.62 / 5.6 | 0.75 (2.40) / 0.73 / 8.6 | 0.41 (2.96) / 0.97 / 4.9 | 0.46 (2.53) / 0.90 / 5.5 |
| 1990s | 1.07 (3.62) / 0.93 / 12.5 | −0.13 (−0.45) / −0.15 / −2.1 | 0.00 (0.01) / 0.01 / −0.4 | 1.13 (3.29) / 1.21 / 13.7 | 0.19 (0.93) / 0.39 / 2.2 | 0.01 (0.08) / 0.02 / −0.1 |
| 2000s | −0.14 (−0.27) / −0.10 / −3.1 | 0.42 (1.71) / 0.37 / 4.2 | 0.66 (1.74) / 0.62 / 7.4 | 0.08 (0.13) / 0.04 / −2.0 | 0.69 (1.97) / 0.62 / 7.6 | 0.55 (2.10) / 0.81 / 6.5 |
| 2010s | 1.09 (4.31) / 1.01 / 13.0 | −0.02 (−0.09) / −0.03 / −0.5 | −0.20 (−0.92) / −0.30 / −2.6 | 0.27 (1.09) / 0.29 / 2.6 | 0.11 (0.86) / 0.26 / 1.2 | 0.02 (0.11) / 0.04 / 0.1 |
| 2020-01 a 2026-07 | 1.07 (2.26) / 0.73 / 11.9 | −0.16 (−0.47) / −0.19 / −2.4 | 0.22 (0.37) / 0.18 / 1.5 | 0.30 (0.70) / 0.24 / 2.5 | 0.28 (0.93) / 0.32 / 2.9 | 0.06 (0.18) / 0.07 / 0.2 |

En las tres décadas más recientes (1990s, 2000s y 2010s) y en 2020-2026, ninguna prima de factor tiene t NW ≥ 2, salvo MOM en los 1990s (3.29) y CMA en los 2000s (2.10). RMW en los 2000s queda en 1.97.

#### 11.5 Crashes de momentum (H4: confirmada)

- **Peores meses de Mom en 1927-01 a 2026-07.** En 12 de los 15 el mercado venía de un acumulado de 24 meses < 0 ("oso"). En 14 de los 15 el mercado subió ese mismo mes. 9 de los 15 están en la tabla 2 de DM.
- **En la ventana de DM** (1927-01 a 2013-03) son 13 osos de 15, 15 de 15 con el mercado al alza y **10 de los 15 de DM** entre los 15 peores de Mom.
- **Magnitud.** Es menor que la del WML de deciles de DM. En 1932-08, Mom perdió −52.61% contra −74.36% en DM. En 1932-07, −45.63% contra −60.98%. En 2009-04, −34.36% contra −45.52%.
- **Oso contra normal** (regresión con NW):

  | Ventana | Media oso %/mes (n) | Media normal %/mes (n) | Diferencia (t NW) |
  |---|---|---|---|
  | 1928-07 a 2026-07 | −0.775 (191) | 0.877 (986) | −1.652 (−2.69) |
  | 1928-07 a 2013-03 (DM) | −0.665 (183) | 0.957 (834) | −1.622 (−2.55) |
  | 2013-04 a 2026-07 | −3.297 (8) | 0.438 (152) | −3.735 (−1.65) |

- **Después de DM.** Los peores meses son 2023-01 (−16.21%, oso con −0.81% de mercado a 24 meses), 2020-11 (−12.60%, no oso), **2026-07 (−12.25%, no oso, mercado −0.27%)**, 2019-01 (−8.64%) y 2021-02 (−7.99%). Solo 1 de 5 fue en estado oso: los crashes recientes **no** siguen el patrón de DM.
- **Drawdowns de Π(1+Mom).**
  - El peor fue −78.4%, de 1932-06 a 1939-09, y se recuperó hasta 1956-12.
  - El segundo fue −57.8%, de 2008-11 a 2009-09, y **no se ha recuperado a 2026-07**: el índice sigue 31.94% abajo del pico de 2008-11 (verificación independiente).

#### 11.6 "Muerte del value" (H5: confirmada)

- **Π(1+HML)** (idéntico con los archivos de 3 y de 5 factores): pico en **2006-12**, valle en **2020-09**, **−57.8%** en 165 meses. Del valle a 2026-07 subió **+66.8%**, y sigue **−29.6%** abajo del pico. No recuperó el máximo previo.
- **Curva RF+HML del motor** (sensibilidad; incluye el rendimiento de la T-bill del colateral): pico en 2007-02, valle en 2020-09, −52.5%. Desde el valle subió +99.0% y está a −5.4% del pico.

| Ventana | n | HML media %/mes (t NW) | Sharpe | Geo anual % | Mkt-RF %/mes |
|---|---|---|---|---|---|
| 1992-01 a 2006-12 | 180 | 0.663 (2.21) | 0.717 | 7.61 | 0.623 |
| 2007-01 a 2020-12 | 168 | −0.443 (−1.74) | −0.532 | −5.67 | 0.841 |
| 2021-01 a 2026-07 | 67 | 0.780 (1.57) | 0.660 | 8.71 | 0.893 |
| 2020-10 a 2026-07 (desde el valle) | 70 | 0.813 (1.69) | 0.698 | 9.17 | 1.069 |

HML por año (%):

| Año | 2007 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 |
|---|---|---|---|---|---|---|---|---|---|---|
| HML | −15.7 | 2.2 | −3.6 | −3.9 | −8.1 | 8.7 | 2.1 | −2.1 | −9.8 | 20.6 |

| Año | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (ene-jul) |
|---|---|---|---|---|---|---|---|---|---|---|
| HML | −10.8 | −10.5 | −8.1 | −30.7 | 22.2 | 31.7 | −11.1 | −7.0 | 6.6 | 12.3 |

#### 11.7 Motor: tenencia de cada factor después de publicar, contra el mercado en la misma ventana (segmento prueba, brutas)

| Variante | Ventana | n | CAGR (RF+F) | Sharpe | MDD | t NW | Mercado: Sharpe / MDD |
|---|---|---|---|---|---|---|---|
| F_SMB | 1981-04 a 2026-07 | 544 | 0.0347 | 0.0175 | −0.3058 | 0.13 | 0.5602 / −0.5031 |
| F_HML | 1992-07 a 2026-07 | 409 | 0.0405 | 0.1913 | −0.5247 | 0.93 | 0.6123 / −0.5031 |
| F_MOM | 1993-04 a 2026-07 | 400 | 0.0580 | 0.2817 | −0.5774 | 1.60 | 0.5956 / −0.5031 |
| F_RMW | 2015-05 a 2026-07 | 135 | 0.0450 | 0.3160 | −0.2051 | 1.23 | 0.7725 / −0.2484 |
| F_CMA | 2015-05 a 2026-07 | 135 | 0.0138 | −0.0389 | −0.1745 | −0.13 | 0.7725 / −0.2484 |
| F_EW5 | 2015-05 a 2026-07 | 135 | 0.0278 | 0.1778 | −0.0869 | 0.53 | 0.7725 / −0.2484 |

`F_EW5` en desarrollo (1963-07 a 2013-12) tuvo Sharpe 1.0544 y MDD −0.1345. Después de 2015-04 cayó a 0.1778.

#### 11.8 Control de crash de momentum (H6)

| Variante | Desarrollo 1927-11 a 2013-03: Sharpe / MDD / meses activa | Prueba 2016-12 a 2026-07: Sharpe / MDD / meses activa |
|---|---|---|
| MOM_ctrl_osovol_50 (regla 7 del cap. 02) | 0.6215 / −0.5063 / 74 | 0.3502 / −0.2536 / 2 |
| MOM_ctrl_oso_50 | 0.6916 / −0.4477 / 183 | 0.3724 / −0.2536 / 8 |
| MOM_ctrl_osovol_0 | 0.7290 / −0.4846 / 74 | 0.4471 / −0.2536 / 2 |
| MOM_ctrl_oso_0 | 0.8708 / −0.2482 / 183 | 0.4920 / −0.2536 / 8 |
| MOM_ref_siempre (Mom siempre) | 0.4771 / −0.7816 | 0.2482 / −0.2536 |
| MOM_ref_sma10 (regla sencilla) | 0.4825 / −0.7290 | 0.0953 / −0.1586 |
| MKT_ref_mom (mercado) | 0.3944 / −0.8365 | 0.8097 / −0.2484 |

- **Validación** (2013-04 a 2016-11): la regla nunca se activó. Las cuatro variantes son idénticas a Mom siempre: Sharpe 0.1506, MDD −0.1907.
- **Prueba.** Hubo 8 meses oso: 2020-04, 2023-01, 2023-05, 2023-06, 2023-09, 2023-10, 2023-11 y 2023-12. Con volatilidad alta solo hubo 2 (el último fue 2023-01).
- **Veredicto H6** (regla fijada antes):
  - **Confirmada dentro de muestra:** Sharpe 0.6215 contra 0.4771 y MDD −0.5063 contra −0.7816.
  - **No confirmada fuera de muestra:** el Sharpe mejora (0.3502 contra 0.2482), pero el MDD es **idéntico** (−0.2536). El criterio pedía un MDD menos negativo, y la mejora sale de 2 meses activos.
- **Costos del *overlay*** (defecto y medio): en prueba bajan el Sharpe de la regla 7 a 0.3445 y 0.3428.

### 12. Sensibilidad

| Sensibilidad (lista cerrada) | D post-publicación [IC95 bootstrap] | b₂ (t agrupado) | Lectura |
|---|---|---|---|
| Principal | 68.1% [−174.3%, 287.9%] | −0.6808 (−1.85) | IC dominado por la media dentro de muestra inestable de SMB |
| S1. Fechas alternativas (Banz 1979-06; FF2015 2014-10) | 62.3% [−188.9%, 299.3%] | −0.6227 (−1.70) | Igual signo; SMB baja a 70.7%, RMW 16.1% y CMA 115.9% |
| S2. SMB y HML del archivo de 5 factores (SMB IS = 1963-07 a 1975-12) | 66.1% [−95.5%, 214.6%] | −0.6611 (−2.42) | 22.14% de las repeticiones con media IS de SMB ≤ 0 |
| S3. Sin SMB (t iid < 2 dentro de muestra) | 56.8% [−59.9%, 122.9%] | −0.5675 (−2.28) | Cerca del 58% de MP; D_oos = 21.0% [−210.6%, 186.1%], cerca del 26% de MP |
| S4. Pre-muestra | — | — | HML en 1926-07 a 1963-06: 0.450 (t NW 2.12). Mom en 1927-01 a 1964-12: 0.638 (t NW 2.74). SMB en 1926-07 a 1935-12: 0.335 (t NW 0.68). HML y Mom existían **antes** de la muestra de sus artículos |
| Costos del motor (defecto y medio; solo *overlay*) | — | — | En la familia F el costo solo se cobra al entrar (desarrollo): el Sharpe de prueba no cambia. No se modela la rotación interna del factor |
| Historia completa (`F_*_hist`) | — | — | El desarrollo con la pre-muestra baja el Sharpe de HML (0.4107 contra 0.5752) y de MOM (0.5228 contra 0.8028). La prueba es idéntica |

**Ventanas de 6 meses con acumulado > 0** (relevante para `temporada_meses` = 6):

| Factor | Antes | Después |
|---|---|---|
| SMB | 52.1% | 47.3% |
| HML | 60.7% | 57.2% |
| MOM | 76.1% | 66.8% |
| RMW | 64.0% | 62.3% |
| CMA | 61.4% | 40.8% |

**Bloque C.** Las **116 de 116** cifras publicadas en `conocimiento/02` (§5.1) y `conocimiento/03` (§5.1 y §5.4) se reproducen con la tolerancia aplicada. La tabla completa está en `R03-salida.txt`. Las definiciones que usa el sistema quedaron identificadas:

- En la tabla del cap. 02: media ×12 y t iid, con SMB y HML del archivo de 5 factores.
- En la tabla del cap. 03: rendimiento geométrico anual, Sharpe = media/desv·√12 y t iid.

Con la lectura literal de ±0.01, 12 cifras de un decimal serían "diferencia menor" (ver desviaciones).

### 13. Diferencia frente al artículo

| Aspecto | Artículo | Réplica | ¿Explica la diferencia? |
|---|---|---|---|
| Datos / versión | MP: 97 predictores reconstruidos con CRSP/Compustat de su época. FF2015: datos de 2014 | Biblioteca French, CRSP 202607, formato CIZ desde enero de 2025, con revisiones de 2015, 2018, 2020 y 2021 | Para FF 2015, las medias de hoy quedan a ≤ 0.018 pp/mes de la tabla 4: el cambio de versión mueve poco estos promedios. **El efecto del cambio CIZ no se midió** (no hay versión anterior disponible) |
| Construcción | MP: quintiles extremos o pendientes de Fama-MacBeth. Banz: muy pequeñas contra muy grandes. FF92: deciles y FM. JT93: deciles equiponderados | Factores 2×3 ponderados por valor, con cortes del NYSE | Sí, para la magnitud. SMB en 1936–1975 (t 1.22) es mucho más débil que el efecto de Banz (t −2.92; 1.52%/mes en los extremos). Mom es menos extremo que el WML de DM (−52.61% contra −74.36% en 1932-08). No se cuantificó cuánto explica la construcción |
| Periodo y fechas | Muestra y publicación de cada estudio | Las mismas fechas de muestra y publicación de los artículos originales, con datos hasta 2026-07 | Los tramos OOS son cortos: 16 a 63 meses |
| Universo de predictores | 97 predictores: el promedio diluye la varianza de cada uno | 5 factores | **Explica la imprecisión**: con 5 series, el decaimiento agrupado tiene un IC de más de 400 pp de ancho |
| Resultado | −26% fuera de muestra y −58% post-publicación. Las versiones de trabajo de 2012 y 2013 decían ~10% y ~35% | OOS: −268% (+21% sin SMB). POST: 68.1% (56.8% sin SMB) | La magnitud post-publicación es compatible, pero el IC no excluye 0. El OOS lo domina SMB en 1976–1981 |
| Costos | Brutos | Brutos. El costo del motor solo cubre el *overlay* | No aplica: la comparación es bruta contra bruta |
| DM (crashes) | WML de deciles, 1927:01 a 2013:03; 14 de 15 osos | Mom 2×3: 13 de 15 osos en la misma ventana, 10 de 15 meses coincidentes | Construcción distinta. El patrón se reproduce |

### 14. Conclusiones permitidas

Alcance: EUA, factores largo-corto de French (CRSP 202607), brutos, en USD, hasta 2026-07.

1. **Los cinco factores rindieron menos después de su publicación que en la muestra del artículo original.** SMB bajó de 0.157 a 0.015%/mes, HML de 0.425 a 0.181, MOM de 0.821 a 0.389, RMW de 0.268 a 0.228 y CMA de 0.324 a −0.027.
   - El decaimiento agrupado estilo McLean-Pontiff es **68.1%** (56.8% sin SMB). Es compatible en magnitud con el 58% de McLean-Pontiff.
   - Es **estadísticamente impreciso**: el IC 95% bootstrap incluye 0 en todas las especificaciones, y ninguna diferencia individual tiene |t| ≥ 2.
   - El t agrupado de b₂ va de −1.70 a −2.42 según la especificación, pero ese t ignora la incertidumbre de la media dentro de muestra.
2. **Después de publicarse, ninguno de los cinco factores tiene una media estadísticamente distinta de cero** (t NW: 0.13, 0.93, 1.60, 1.23 y −0.13). En las mismas ventanas, el mercado tuvo un Sharpe mayor que cada factor: de 0.56 a 0.77, contra −0.04 a 0.32.
3. **El efecto tamaño de Banz no se reproduce con SMB** ni siquiera en su propia muestra (1936–1975: t 1.22). Después de 1981, SMB es ≈ 0 (0.015%/mes, Sharpe 0.017).
4. **HML y Mom ya existían antes de la muestra de sus artículos** (pre-muestra con t NW 2.12 y 2.74). Por eso la caída posterior no se explica solo por minería de datos dentro de la muestra original. Esta réplica **no** separa la causa.
5. **Los crashes de momentum se concentran en estados "oso" con rebote del mercado** (13 de los 15 peores meses en la ventana de DM). En esos meses, Mom promedió −1.65 pp/mes menos (t NW −2.69, 1928–2026).
   - Los peores meses posteriores a 2013 (2020-11 y 2026-07) **no** fueron en estado oso.
   - El índice de Mom **sigue 31.9% debajo de su pico de noviembre de 2008**.
6. **La "muerte del value" mide −57.8%** (Π(1+HML), de 2006-12 a 2020-09). Desde entonces subió +66.8% y sigue −29.6% abajo del pico. Con el colateral en T-bills (RF+HML) fue −52.5%, con +99.0% después y −5.4% abajo del pico.
7. **Las 116 cifras de factores publicadas en los capítulos 02 y 03 se reproducen** con código y datos propios.
8. **La regla 7 del cap. 02 (control de crash) mejoró Sharpe y MDD dentro de muestra** (1927–2013: 0.6215 contra 0.4771; −50.6% contra −78.2%), con DSR 0.9721 en desarrollo. **Fuera de muestra no hay evidencia suficiente:** solo 2 meses activos y el MDD es idéntico.

### 15. Conclusiones que NO se sostienen

- **"La publicación destruyó las primas" como causa.** No se controló por tendencias comunes: el abaratamiento del *trading*, la decimalización, los flujos a ETFs de factores ni los regímenes de tasas. El diseño solo mide antes y después.
- **"El decaimiento es 58%" o "es 68%".** El IC va de −174% a +288% (de −60% a +123% sin SMB).
- **"Los factores murieron" o "value ya se recuperó".**
  - Las medias post-publicación son positivas y no significativas en HML, MOM y RMW, así que tampoco se rechaza que sigan siendo positivas.
  - HML sigue debajo de su pico de 2006.
- **"Los ETFs de factores en GBM ganarían X."** Las series son largo-corto, brutas, sin rotación interna ni costos de préstamo, en USD. Un ETF long-only captura otra cosa. Nada de esto se probó en MXN ni con los costos de GBM.
- **"El control de crash funciona fuera de muestra" o "usar `MOM_ctrl_oso_0` porque fue la mejor".** Elegirla después de ver los resultados es selección. Su DSR en prueba es 0.7392 (0.8735 con V de su familia), bajo 0.95.
- **"`F_EW5` es candidata porque su DSR en desarrollo es 1.0."** Después de 2015-04 su Sharpe es 0.1778 (t 0.53), contra 0.7725 del mercado.
- **"El OOS negativo (−268%) contradice a McLean-Pontiff."** Es un artefacto de SMB en 1976–1981 y de tramos OOS de 16 a 63 meses.

### 16. Estado y reproducción

- **Estado: Replicado con diferencias**, según la regla pre-registrada:
  - Se cumple la condición A.
  - D = 68.1% > 0 y los cinco factores bajan después de publicarse.
  - **Pero** el IC 95% bootstrap de D, [−174.3%, 287.9%], incluye 0. El 58% de McLean-Pontiff sí está dentro del IC.
  - Veredictos separados: H4 confirmada; H5 confirmada; H6 confirmada dentro de muestra y no confirmada fuera de muestra. H1 no se cumple para SMB.
- **Comando:** `python3 laboratorio/replicas/R03.py`, desde `/home/user/New1`. Tarda unos 5 s con el caché de French, que no caduca (`cache_horas=None`).
- **Huellas de datos (sha256):**
  - `F-F_Research_Data_Factors` `b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb`
  - `F-F_Momentum_Factor` `7ee14e892b0f7044902fdbc4e25cfaf175b73d4eda0ae6f4a0354a4433afe065`
  - `F-F_Research_Data_5_Factors_2x3` `b8653b411cc5e28917e7ef643bb42f6d2d3703f84bc170eb6ae38d5267c65807`
  - `F-F_Research_Data_Factors_daily` `1916d331c2c51d2aee3d00215897d2b8e5995cb387f1f4569ba46bff5fb049a8`
  - Todas son CRSP 202607. La `huella_datos` de cada corrida está en el CSV.
- **Fecha de la corrida final:** 2026-09-25 05:56:41–05:56:45 UTC. Fue una sola ejecución.

### Conclusión operable (qué regla del sistema confirma, modifica o descarta)

> Fase 0: nada de esto es una recomendación de inversión ni habilita dinero real.

1. **MODIFICA la regla 4 del cap. 02** (recorte obligatorio: μ_usable = 0.5 × μ_backtest).
   - En los factores de EUA, el decaimiento puntual fue ≥ 50% en 4 de 5: SMB 90.5%, HML 57.5%, MOM 52.6% y CMA 108.4%. RMW fue 15.1%, y el agrupado 68.1%.
   - Un recorte de 50% **no es conservador** para primas largo-corto de EUA. Propuesta de regla:
     - Si la señal tiene ≥ 10 años de historia post-publicación, μ_usable = la media **post-publicación** medida, y se exige t NW ≥ 2 en ese tramo antes de dimensionar.
     - El 50% queda solo como tope máximo para señales sin historia post-publicación.
   - Con esa regla, **ninguno de los cinco factores de EUA pasa hoy** (t NW post de 0.13 a 1.60).
2. **CONFIRMA la regla 3 del cap. 02** (excluir size aislado) y **la amplía a CMA en EUA.**
   - SMB post-1981 tiene t 0.13 y Sharpe 0.017.
   - CMA post-2015 tiene media −0.027%/mes y solo 40.8% de ventanas de 6 meses positivas.
   - El orden de prioridad del cap. 02 (profitability > momentum con control > value) es **consistente** con los decaimientos medidos (RMW el menor), pero **no está respaldado estadísticamente**: ninguno es significativo después de publicarse.
3. **La regla 7 del cap. 02 (control de crash de momentum) queda "confirmada dentro de muestra, pendiente fuera de muestra".**
   - Se conserva como **freno de riesgo**, no como fuente de alfa.
   - No se cambia al umbral "oso → 0" aunque haya sido mejor: sería selección después de ver resultados.
   - Hace falta evidencia nueva (otros mercados o el tiempo real).
   - Advertencia nueva: los dos peores meses recientes (2020-11 y 2026-07) ocurrieron **sin** estado oso, así que la regla no los habría evitado.
4. **CONFIRMA el checklist §6.2 del cap. 02 y §5.4 del cap. 03** (drawdowns de −57.8% en HML y de −78.4% y −57.8% en Mom; value como prima de alta varianza que "no cabe" en una temporada).
   - En ventanas de 6 meses posteriores a la publicación, HML fue positivo solo 57.2% de las veces, SMB 47.3% y CMA 40.8%.
   - Para la arena (`temporada_meses` = 6), **ninguna inclinación a factores de EUA se justifica por su prima**.
5. **Estado de conocimiento.** Las cifras de factores de los capítulos 02 y 03 (116 verificadas) pasan a **Replicado**. El hallazgo de McLean-Pontiff aplicado a estos cinco factores pasa a **Replicado con diferencias**: la magnitud es compatible y la precisión es insuficiente. Su ficha propia sigue pendiente en `laboratorio/README.md`.
