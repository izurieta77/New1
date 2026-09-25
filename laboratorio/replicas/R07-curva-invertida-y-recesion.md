# Réplica R07: la curva 10a−3m como predictor de recesión (Estrella y Mishkin, 1998), la inversión de 2022-2024 y el rendimiento accionario después de una inversión

> Fase 0: formación. Esta ficha no recomienda inversiones. Las secciones 1 a 9 son el pre-registro. Se escribieron el 2026-09-25, antes de estimar cualquier probit, calcular cualquier probabilidad, rendimiento o Sharpe con datos, y no se editan después. Cualquier cambio posterior va a "Desviaciones del pre-registro", con fecha.

| Campo | Valor |
|---|---|
| ID | `R07` (registro: `laboratorio/replicas/R07-variantes.csv`; script: `laboratorio/replicas/R07.py`) |
| Artículo replicado | Estrella, A. y Mishkin, F. S. (1998). "Predicting U.S. Recessions: Financial Variables as Leading Indicators". *The Review of Economics and Statistics* 80(1), 45–61, febrero de 1998. doi:10.1162/003465398557320. NBER Working Paper 5379 (fecha de emisión: diciembre de 1995). Federal Reserve Bank of New York Research Paper 9609 (portada de mayo de 1996; primera página interior "April 1996"). Ficha verificada con WebSearch/WebFetch el 2026-09-25 (página del NBER w5379, EconPapers `RePEc:tpr:restat:v:80:y:1998:i:1:p:45-61`) |
| Artículos de contraste | (a) Estrella, A. y Mishkin, F. S. (1996). "The Yield Curve as a Predictor of U.S. Recessions". FRBNY *Current Issues in Economics and Finance* 2(7), junio de 1996. (b) Estrella, A. (2005). "The Yield Curve as a Leading Indicator: Frequently Asked Questions", FRBNY, octubre de 2005. (c) Estrella, A. (1998). "A New Measure of Fit for Equations with Dichotomous Dependent Variables". *Journal of Business & Economic Statistics* 16(2), 198–205 (versión FRBNY Research Paper 9716), de donde sale la fórmula del pseudo R² |
| Acceso al texto | **RP 9609 (abril/mayo de 1996):** el PDF de la Fed de NY es un escaneo sin capa de texto; se extrajeron las imágenes de las páginas y se **leyeron visualmente** las secciones 2, 3 y 5, las tablas 1, 2, 3, 4, 5, A1 y A8, las notas 3-15 y el apéndice B. **El PDF de NBER w5379 es un escaneo con OCR ilegible** (texto invertido). **El artículo publicado en REStat no se pudo leer** (MIT Press respondió 403, de pago). Por eso las cifras de abajo son de la versión RP 9609 y **no se comprobó que coincidan con las de REStat 1998**. *Current Issues* 1996 y el FAQ de 2005 se leyeron completos en PDF con capa de texto (`pypdf`). La fórmula del pseudo R² se leyó en las páginas 5-8 del RP 9716 (escaneo, lectura visual) |
| Fecha de publicación | Primera versión pública verificada: NBER WP 5379, diciembre de 1995. Revista: febrero de 1998. El hallazgo general (la pendiente predice recesiones) es anterior: Estrella y Hardouvelis (1991, *Journal of Finance*); Harvey (1988) |
| Pre-registro escrito el | 2026-09-25, antes de cualquier corrida con datos |
| Responsable | Claude (laboratorio del sistema). Revisión independiente pendiente (`auditor-de-replicas`) |
| Estado | (se llena al final) |

**Conocimiento previo declarado.** Este pre-registro no es ciego. Antes de escribirlo ya conocía:

1. Las cifras de los artículos que se transcriben en la sección 1.
2. El capítulo `conocimiento/04-maestria-renta-fija-tasas-macro.md` §2.11, §5.1, §6.1 (regla 6, "tablero de recesión") y §7 (trampa 3). Ahí están, como "cálculo propio" sin script en el laboratorio: la tabla de inversiones de T10Y3M desde 1982 (4 de 4 recesiones en 1989-2020 con 9-17 meses de anticipación; 2022-2024 como falso positivo), "534 sesiones seguidas (25-oct-2022 a 12-dic-2024)" con mínimo de −1.89 el 4-may-2023, y "2 falsos positivos desde 1966". También sé, en general, que el NBER no ha fechado una recesión posterior a la de 2020 y que la curva estuvo invertida en 2022-2024.
3. El tablero del sistema (`herramientas/tablero.py`, dimensión "Curva") y el brief `bitacora/briefs/2026-09-25-tablero-v2.md`: T10Y3M = +0.94 pp el 2026-09-24.
4. Para comprobar acceso a datos (no resultados), descargué y vi solo el primer y el último dato de FRED `USREC` (1854-12 a 2026-08, último = 0), `USRECQ` (1854-10 a 2026-04), `GS10` (1953-04 a 2026-08), `TB3MS` (1934-01 a 2026-08), `T10Y3M` (1982-01-04 a 2026-09-24), `DTB3` y `DGS10`. Comprobé que ALFRED tiene vintages de `USREC` desde el 2014-09-18 (el primero encontrado por búsqueda binaria) y que el vintage del 2020-06-01 marca 0 en 2020-03..05 y el del 2020-06-10 marca 1 (el anuncio del NBER fue el 8-jun-2020). No he estimado ningún probit, ni calculado ninguna probabilidad, rendimiento, pseudo R² o Sharpe con estos datos.

---

## PRE-REGISTRO (secciones 1 a 9; no se editan después de la primera corrida)

### 1. Hipótesis previa y mecanismo

**Resultado declarado en el artículo (RP 9609, cifras textuales leídas en las imágenes).**

- **Modelo (sección 2.1, ec. 1):** P(R_{t+k} = 1) = F(β′x_t), con F la normal acumulada, estimado por máxima verosimilitud. R_t = 1 si la economía está en recesión en el trimestre t según las fechas estándar del NBER. *Current Issues* 1996 precisa: los trimestres de recesión van "starting with the first quarter after a business cycle peak and continuing through the trough quarter".
- **Datos (sección 3, tabla 1 y apéndice B):** SPREAD = "10-year Treasury bond minus 3-month Treasury bill (BOND − BILL)"; BILL = "3-month Treasury bill, market yield, bond equivalent". Tasas en promedio trimestral, rezago de información 0. Estimación con datos trimestrales "from the first quarter of 1959 to the first quarter of 1995". Nota 8: con datos mensuales "the results were the same" en el orden de las variables, pero el pseudo R² "was better with the quarterly data in the vast majority of cases".
- **Medida de ajuste (sección 2.2, nota 4; Estrella 1998):** pseudo R² = 1 − (log L_u / log L_c)^(−(2/n)·log L_c), donde L_u es la verosimilitud del modelo y L_c la del modelo con solo constante. Fuera de muestra puede ser negativo.
- **Estadístico t (nota 3):** errores estándar con la técnica de Newey-West (1987) aplicada a las condiciones de primer orden del probit (método de Estrella y Rodrigues). El artículo no dice el número de rezagos.
- **Tabla 2 (= tabla A1), SPREAD, dentro de muestra, k = 1 a 8 trimestres:**

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Pseudo R² | 0.071 | 0.211 | 0.271 | **0.296** | 0.256 | 0.149 | 0.078 | 0.031 |
| t | −2.71 | −4.21 | −4.71 | **−4.57** | −3.87 | −4.13 | −3.02 | −1.63 |

- **Fuera de muestra (sección 5 y tabla 4):** se estima con datos "from the beginning of the sample up to a particular quarter", se pronostica k trimestres adelante y se agrega un trimestre a la vez; "Data that became available subsequent to the prediction date are not used". Primer trimestre pronosticado: 1971T1; último: 1995T1. Pseudo R² de SPREAD fuera de muestra:

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Pseudo R² fuera | 0.072 | 0.236 | 0.328 | **0.295** | 0.155 | 0.141 | negativo | negativo |

- **Conclusión textual (resumen):** "Beyond 1 quarter, however, the slope of the yield curve emerges as the clear individual choice and typically performs better by itself out of sample than in conjunction with other variables."
- **Tabla de *Current Issues* 1996** (probit con SPREAD, 4 trimestres adelante, datos 1960T1-1995T1, ambas tasas "on a bond-equivalent basis"): probabilidad 5% ↔ 1.21 pp; 10% ↔ 0.76; 15% ↔ 0.46; 20% ↔ 0.22; 25% ↔ 0.02; 30% ↔ −0.17; 40% ↔ −0.50; **50% ↔ −0.82**; 60% ↔ −1.13; 70% ↔ −1.46; 80% ↔ −1.85; **90% ↔ −2.40**. Ejemplos: spread de 2.74 en 1994T3 → 0.2%; −2.18 en 1981T1 → 86.5%. *Cálculo mío a partir de la tabla (no es cifra del artículo):* con Φ⁻¹(0.5) = 0 y Φ⁻¹(0.9) = 1.281552, los coeficientes implícitos son β = −1.281552/(2.40 − 0.82) = −0.8111 y α = 0.82·β = −0.6651; con ellos, 0.76 pp da z = −1.2816 (10%), consistente con la tabla.
- **FAQ de 2005 (Estrella):** "The yield curve has predicted essentially every U.S. recession since 1950 with only one 'false' signal, which preceded the credit crunch and slowdown in production in 1967." La versión mensual usa "monthly averages of daily rates", el 10 años de vencimiento constante y el 3 meses "on a bond-equivalent basis", y predice la recesión 12 meses adelante.

**Mecanismo económico.** (1) Expectativas: una curva invertida dice que el mercado espera tasas cortas más bajas, lo que ocurre cuando espera debilidad. (2) Política monetaria: la Fed sube la tasa corta, aplana la curva y frena la actividad con rezago de 4-6 trimestres. (3) Crédito: los bancos fondean corto y prestan largo; con curva invertida el margen cae y el crédito se contrae. (4) Prima por plazo: si la prima es muy negativa (compras de bonos de la Fed, demanda de refugio), la curva puede invertirse sin que el mercado espere recortes; eso debilita la señal (es la explicación más citada para 2022-2024; *inferencia*, no se prueba aquí). **Por qué no se "arbitra":** es un pronóstico macro, no un precio mal fijado. Para las acciones, una recesión probable puede estar ya parcialmente descontada y el rezago es largo e incierto (6-24 meses), así que una regla de salida del mercado puede costar más de lo que ahorra.

**Hipótesis (signo y magnitud esperados, antes de ver datos):**

- **H1, réplica dentro de muestra (trimestral, 1959T1-1995T1, k = 4):** β < 0 con |t| NW ≥ 2 y pseudo R² dentro de 0.296 ± 0.05. Patrón secundario: el pseudo R² máximo está en k = 3, 4 o 5 y el de k = 1 y k = 8 es menor que 0.10. Contraste con *Current Issues*: el spread que da 50% (−α/β) cae dentro de −0.82 ± 0.25 pp.
- **H2, réplica fuera de muestra al estilo del artículo (trimestral, pronósticos para 1971T1-1995T1, cronología final del NBER):** pseudo R² fuera de muestra con k = 4 dentro de 0.295 ± 0.05; positivo en k = 2, 3 y 4; negativo o casi cero en k = 7 y 8.
- **H3, después de publicarse (mensual, 12 meses adelante, estimación en tiempo real, orígenes 1998-03 a 2025-08 y objetivos 1999-03 a 2026-08):** *expectativa previa:* el probit conserva poder de ordenamiento (AUC > 0.70) pero su pseudo R² fuera de muestra cae mucho frente al de dentro de muestra, y puede ser negativo, por el falso positivo de 2022-2024. Criterios en la sección 2.
- **H4, el episodio 2022-2024:** *expectativa previa:* con la cronología del NBER vigente al 2026-09-25 (último pico anunciado: feb-2020), fue un falso positivo: ningún mes con USREC = 1 en la ventana de 12 meses posterior a cualquier mes invertido. El probit en tiempo real dio probabilidades altas (> 0.5) durante varios meses.
- **H5, rendimiento accionario después de una inversión:** *expectativa previa:* el rendimiento del mercado de EUA en los 12 meses posteriores al inicio de una inversión **no** es significativamente menor que el incondicional; la caída llega, cuando llega, más tarde y con rezago variable.
- **H6, versión operable (motor, mercado de EUA contra T-bill, costos GBM):** *expectativa previa:* ninguna de las 8 reglas supera a comprar y mantener en Sharpe neto fuera de muestra (1998-03 a 2026-07); alguna puede reducir la caída máxima por 2008.

### 2. Criterio de refutación

**Métricas principales:** pseudo R² de Estrella (dentro y fuera de muestra) y t de Newey-West del coeficiente de la pendiente; fuera de muestra, además, Brier (media de (p − y)²) contra la climatología y AUC (Mann-Whitney). Para H5, rendimiento compuesto del mercado a 12 meses. Para H6, Sharpe neto del exceso sobre RF y caída máxima (MDD) de la curva neta.

**Criterios:**

- **H1 "Replicado":** β < 0, |t| NW ≥ 2 y pseudo R² (k = 4) en [0.246, 0.346]. **Replicado con diferencias:** β < 0 y |t| ≥ 2, pero pseudo R² fuera de la tolerancia. **No replicado:** β ≥ 0 o |t| < 2 con k = 4.
- **H2 "Replicado":** pseudo R² fuera de muestra (k = 4) en [0.245, 0.345]. **Con diferencias:** positivo pero fuera de la tolerancia. **No replicado:** ≤ 0.
- **H3 (post-publicación), métrica principal: variante con etiquetas en tiempo real.** "El spread sigue prediciendo" si el pseudo R² fuera de muestra > 0 **y** el Brier < Brier de la climatología recursiva. **Se refuta** si el pseudo R² ≤ 0 **y** el Brier ≥ el de la climatología. Cualquier otra combinación es "mixto".
- **H4:** falso positivo si ningún mes entre el mes siguiente a la primera inversión mensual del episodio y 12 meses después de la última tiene USREC = 1 en la serie vigente de FRED, **y** la lista de anuncios del NBER no tiene un pico posterior a feb-2020. Se reporta el rezago del NBER (4-21 meses en 1980-2021): un "no" hoy puede cambiar si el NBER fecha después un pico en 2025-2026.
- **H5:** se refuta mi expectativa ("no es menor") si la media del rendimiento a 12 meses después del inicio de las inversiones es menor que la incondicional con t aproximado ≤ −2 (t = diferencia / (desv. est. incondicional de las ventanas de 12 meses / √n_eventos); ignora el traslape y es solo indicativo).
- **H6 (operable):** para la variante con el mayor Sharpe neto **dentro de muestra** (1971-01 a 1998-02) entre las 8 de prueba:
  - "Agrega valor frente a comprar y mantener" solo si **fuera de muestra** (1998-03 a 2026-07) tiene Sharpe neto > comprar y mantener **y** una MDD menor en valor absoluto.
  - "Agrega valor frente a la regla sencilla" solo si además supera a la SMA10 en Sharpe **y** en MDD fuera de muestra.
  - Para ser candidata hace falta además DSR ≥ 0.95 (`validacion_estrategias.deflated_sharpe_min_probabilidad`) con N = 8 y con N conservador = 16.
  - **Se refuta H6** (como regla que mejora el Sharpe) si el Sharpe neto fuera de muestra es ≤ el de comprar y mantener. **Se refuta el uso como freno** si su MDD fuera de muestra **y** dentro de muestra no son menores que las de comprar y mantener.

### 3. Datos y licencia

| Serie | Fuente y archivo | Versión / huella | Frecuencia | Condiciones de uso |
|---|---|---|---|---|
| 10 años CMT | FRED `GS10` (promedio mensual de datos diarios) | fecha de descarga; se compara con vintages de ALFRED | mensual | Pendiente de verificar (datos de la Junta de la Fed vía FRED) |
| T-bill 3 meses | FRED `TB3MS` (mercado secundario, **base descuento**, promedio mensual) | ídem | mensual | Pendiente de verificar |
| 10a − 3m diario | FRED `T10Y3M` (10 años CMT − 3 meses CMT), desde 1982-01-04 | fecha de descarga | diaria | Pendiente de verificar |
| Recesión mensual | FRED `USREC` (del mes siguiente al pico hasta el valle) | fecha de descarga | mensual | Pendiente de verificar |
| Recesión trimestral | FRED `USRECQ` (misma definición, fechas trimestrales del NBER) | fecha de descarga | trimestral | Pendiente de verificar |
| Recesión en tiempo real | ALFRED `USREC`, vintages desde 2014-09-18 (verificación) + fechas de anuncio del NBER (tabla abajo) | `vintage_date` | mensual | Pendiente de verificar |
| Mercado y RF | French `F-F_Research_Data_Factors` (Mkt-RF + RF; RF) | `version_crsp` y `sha256` que imprime el script | mensual | Pendiente de verificar (README §7) |
| MXN por USD | FRED `DEXMXUS` (solo sensibilidad) | fecha de descarga | diaria | Pendiente de verificar |

**Fechas de anuncio del NBER** (página "Business Cycle Dating Committee Announcements", consultada el 2026-09-25; las de 1980-1983 se contrastaron con una segunda búsqueda porque el resumen de la página salió confuso): pico ene-1980 → 3-jun-1980; valle jul-1980 → 8-jul-1981; pico jul-1981 → 6-ene-1982; valle nov-1982 → 8-jul-1983; pico jul-1990 → 25-abr-1991; valle mar-1991 → 22-dic-1992; pico mar-2001 → 26-nov-2001; valle nov-2001 → 17-jul-2003; pico dic-2007 → 1-dic-2008; valle jun-2009 → 20-sep-2010; pico feb-2020 → 8-jun-2020; valle abr-2020 → 19-jul-2021. La página no lista anuncios posteriores al 19-jul-2021; la página principal dice "the most recent peak occurred in February 2020. The most recent trough occurred in April 2020". Antes de 1979 no hubo anuncios formales.

### 4. Universo

- **Predicción:** la economía de EUA (recesiones del NBER). No hay sesgo de supervivencia.
- **Acciones:** el mercado total de EUA de French (CRSP, ponderado por valor, con dividendos); efectivo = RF de French (Ibbotson hasta 202405, ICE BofA desde 202406). El índice **no es invertible directamente**; el proxy operable sería un ETF del S&P 500 en el SIC (no probado aquí).

### 5. Fecha de disponibilidad

- **Tasas:** el promedio mensual del mes m se conoce al cierre del último día hábil de m. FRED fecha el dato el día 1 del mes; el script lo **re-fecha al fin de mes calendario de m**. En el motor, la decisión del mes t solo ve spreads con fecha ≤ fin de mes de t−1. Los rendimientos de Treasuries no se revisan en principio; **se verifica** comparando GS10 y TB3MS actuales con vintages de ALFRED (primer vintage disponible, 2008-12-31, 2020-06-30 y el último), y se reporta la diferencia máxima.
- **Recesiones:** la cronología del NBER se conoce con rezago (de 4 a 21 meses en 1980-2021). Dos versiones:
  - **Cronología final** (la de hoy): es la que usaron Estrella y Mishkin en 1995-96. Se usa en H1 y H2 para replicar el artículo. Es look-ahead en las etiquetas; se declara.
  - **Tiempo real** (H3, H4 y el motor): en la fecha D, un mes es "recesión" si está entre un pico anunciado en o antes de D y su valle anunciado en o antes de D; si el valle aún no se anuncia, todos los meses desde el pico hasta D cuentan como recesión. Un mes posterior a D no se conoce. **Supuesto para 1959-1978** (sin anuncios formales): cada pico o valle se considera conocido **12 meses después** del mes del giro. Solo afecta decisiones anteriores a 1980 (tramo dentro de muestra del motor).
  - **Verificación con ALFRED:** para varias fechas desde 2014-12-31 (y los días alrededor de los anuncios de 2020 y 2021), se compara la etiqueta en tiempo real construida con los anuncios contra el vintage de `USREC` en ALFRED de esa fecha, en todos los meses que ambos cubren. Se reportan las discrepancias.
- **Probit en tiempo real:** en el origen m se usan solo pares (S_s, R_{s+h}) con s + h ≤ m (etiqueta observada) y con la etiqueta conocida en la fecha de fin de mes de m. El pronóstico usa S_m.
- **French:** CRSP revisa datos; la versión 202607 no es exactamente lo que se conocía en cada fecha. Se declara; no se corrige.

### 6. Periodo

- **Artículo:** trimestral 1959T1-1995T1; fuera de muestra, objetivos 1971T1-1995T1.
- **H1 principal:** pares con origen q en [1959T1, 1995T1 − k], de modo que spread y recesión caen dentro de 1959T1-1995T1. **Sensibilidad:** objetivos q + k en [1959T1, 1995T1].
- **H2:** objetivos τ en [1971T1, 1995T1]; origen q = τ − k; estimación con s ≥ 1959T1 y s + k ≤ q.
- **Modelo mensual (extensión, 12 meses adelante):** en muestra 1959-01 a 1994-03 como origen (objetivos hasta 1995-03), y muestra completa con orígenes 1959-01 a 2025-08 (objetivo = último USREC, 2026-08). Fuera de muestra "era del artículo": orígenes 1970-01 a 1998-02. **Post-publicación: orígenes 1998-03 a 2025-08** (el corte es la publicación en REStat, febrero de 1998). Sensibilidad: orígenes solo hasta 2024-02 (objetivos hasta 2025-02), para excluir los últimos 18 meses que el NBER todavía podría reclasificar.
- **Motor (H6):** decisiones mensuales de 1971-01 a 2026-07 (último mes de French CRSP 202607). Un corte en **1998-02-28**: `dentro_muestra` 1971-01 a 1998-02 y `fuera_muestra` 1998-03 a 2026-07.
- **H5:** inversiones desde 1954 (GS10 empieza en 1953-04 y se exigen 12 meses previos sin inversión).

### 7. Limpieza

- **Spread principal:** S_m = GS10_m − BEY(TB3MS_m), con BEY = 365·d / (360 − 91·d) y d = TB3MS/100 (T-bill de 91 días; conversión estándar de base descuento a rendimiento equivalente de bono para plazos menores a medio año). Se reporta la diferencia media contra el promedio mensual de T10Y3M en 1982-2026 como control. **Sensibilidad:** spread con base descuento sin convertir (GS10 − TB3MS).
- **Trimestral:** promedio simple de los 3 meses del trimestre (GS10 y BEY por separado; spread = diferencia de promedios). El trimestre debe tener sus 3 meses; si falta alguno, el script se detiene.
- Si falta un mes de GS10 o TB3MS dentro del periodo, el script se detiene y no se imputa.
- USREC y USRECQ deben ser 0/1; si no, el script se detiene.
- No se elimina ni winsoriza ninguna observación.
- El último mes con USREC (2026-08) y los meses recientes son provisionales (rezago del NBER). No se reclasifican.
- **Probit:** Newton-Raphson con gradiente y hessiano analíticos, arranque en (Φ⁻¹(ȳ), 0), tolerancia 1e-10 en el paso, máximo 100 iteraciones. Si en una ventana no hay unos o no converge, la probabilidad es la frecuencia de unos (modelo con constante); se cuentan y reportan esos casos.
- **Errores estándar:** inversa del hessiano (MV) y sándwich de Newey-West (Bartlett) sobre los scores. Rezagos: **k − 1** en trimestral (k = 1 → White) y **11** en mensual; sensibilidad con k y 12.
- **Pseudo R² fuera de muestra:** L_u = verosimilitud de las probabilidades pronosticadas; L_c = verosimilitud de una constante igual a la frecuencia de recesión **en la ventana evaluada** (análogo a la varianza de la variable dependiente en la nota 5 del artículo). Sensibilidad: L_c con la climatología recursiva (frecuencia conocida en cada origen). Las probabilidades se acotan a [1e-12, 1 − 1e-12] para el logaritmo.

### 8. Regla y variantes planeadas

**Parte A: réplica estadística (no es estrategia, no entra al CSV).**

- A1: probit trimestral P(R_{q+k}) = Φ(α + β S_q), k = 1 a 8, dentro de muestra (H1), con pseudo R², t MV y t NW; sensibilidades de ventana, de rezagos y de spread en base descuento.
- A2: fuera de muestra al estilo del artículo, k = 1 a 8 (H2).
- A3: mensual 12 meses adelante: dentro de muestra (1959-01 a 1994-03 y muestra completa); fuera de muestra recursivo con cronología final y con cronología en tiempo real; orígenes 1970-01 a 1998-02 y 1998-03 a 2025-08 (H3); versión con coeficientes fijos de 1959-01 a 1994-03 aplicados después de 1998. Pseudo R², Brier (y Brier de la climatología recursiva), AUC, aciertos con umbrales 0.3 y 0.5.
- A4: episodio 2022-2024 (H4): meses invertidos (spread principal y promedio mensual de T10Y3M), racha más larga de sesiones negativas de T10Y3M diario con fechas y mínimo, probabilidades en tiempo real 2022-01 a 2025-08, USREC en FRED y en el último vintage de ALFRED. Además, la probabilidad actual con el último spread.
- A5: rendimiento del mercado después del inicio de cada inversión (H5). Inicio = primer mes con S < 0 después de al menos 12 meses consecutivos con S ≥ 0. Rendimiento compuesto de French (Mkt-RF + RF) en los 6, 12, 18 y 24 meses siguientes al mes de inicio (la señal se conoce al cierre del mes de inicio), exceso sobre RF, caída máxima en los 24 meses, meses hasta el máximo del índice dentro de esos 24 meses, y meses hasta el siguiente pico del NBER. Incondicional: todas las ventanas mensuales desde 1954.

**Parte B: reglas operables en el motor (H6).** Activo: French Mkt-RF + RF. Efectivo: RF. Exposición en [0, 1], sin cortos ni apalancamiento. S_{t−1} es el spread principal del mes previo a la decisión. Lista cerrada de 8 variantes de prueba (`es_prueba=True`, costos por defecto):

| Variante | Regla (decisión del mes t) |
|---|---|
| `inv1` | w = 0 si S_{t−1} < 0; si no, 1 |
| `inv3` | w = 0 si S_{t−1}, S_{t−2} y S_{t−3} < 0; si no, 1 (regla 6(1) del tablero del cap. 04) |
| `inv3_medio` | w = 0.5 si se cumple la condición de `inv3`; si no, 1 (la "beta baja 50%" de la regla 6) |
| `probit50` | w = 0 si P_{t−1} > 0.5; si no, 1. P_{t−1} = probit mensual 12 meses adelante estimado en tiempo real (etiquetas en tiempo real) y evaluado en S_{t−1} |
| `probit30` | igual con umbral 0.3 |
| `probit_cont` | w = 1 − P_{t−1} |
| `inv_fuera12` | w = 0 si algún S de t−12 a t−1 es < 0; si no, 1 |
| `desinv12` | w = 0 si en algún mes j de t−12 a t−1 la curva se "des-invirtió": S_j ≥ 0 con S_{j−1}, S_{j−2} y S_{j−3} < 0; si no, 1 |

- Parámetros del artículo que se usan: spread 10a − 3m (bond equivalent), horizonte de 12 meses (4 trimestres), probit por MV. Los umbrales 0.3 y 0.5 y las reglas de inversión no son del artículo: son las reglas del sistema (cap. 04) o convenciones comunes.
- Reglas sencillas con las mismas fechas y costos (`es_prueba=False`): comprar y mantener, 100% efectivo y SMA10 (`senal_media_movil(10)`).
- Sensibilidades (`es_prueba=False`, con nota): las 8 variantes con spread "medio" y en bruto; `inv1`, `inv3` e `inv3_medio` con el spread en base descuento; y en MXN (DEXMXUS, desde la primera decisión con tipo de cambio disponible) la variante elegida, comprar y mantener y SMA10.
- DSR con N = 8 registradas y con **N conservador = 16**: al diseñar consideré y no corrí umbrales 0.2 y 0.4, inversión de 6 meses, spread 10a − 2a, salida de 24 meses y otras combinaciones; se duplica N para cubrirlas.

### 9. Costos y comparación simple

- Costos: comisión 0.29% por lado (GBM V1025, hecho) + spread 0.05% por lado (supuesto [I]); escenario "medio" de 0.15% por lado; y bruto (0) como referencia. Sin costo cambiario (no publicado por GBM), sin impuestos.
- Reglas sencillas con idénticas condiciones: comprar y mantener, 100% efectivo y SMA10.

---

## RESULTADOS (se llenan después de correr)

(pendiente)
