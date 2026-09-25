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
| Estado | **Replicado** en el periodo del artículo (H1 y H2 dentro de la tolerancia pre-registrada). **Después de la publicación, negativo:** H3 refutada (el probit en tiempo real no le gana a la climatología en 1998-2025, por el falso positivo de 2022-2024) y H6 refutada (ninguna regla de salida por curva supera a comprar y mantener fuera de muestra). No es candidata para dinero (secciones 16 y 17) |

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

> Corrida final: `python3 laboratorio/replicas/R07.py`, el 2026-09-25 a las 06:37 UTC (unos 15 s). La salida completa está en `R07-salida.txt`, las cifras clave en `R07-resultados.json` y la verificación sin el motor en `R07_verificacion.py`. Las tablas de esta sección se copiaron de esas salidas, sin redondear a mano.

### Desviaciones del pre-registro

| Fecha | Qué cambió | Por qué | ¿Invalida el tramo de prueba? |
|---|---|---|---|
| 2026-09-25 | Antes de la corrida final se corrió **una vez** `R07.py --humo`: el mismo código con `id_replica=None` (no registra en el CSV) y la salida descartada (no se imprimió ningún resultado). También se probó el estimador probit con **datos simulados** (no con los datos reales). | Detectar errores de programación sin ver resultados ni ensuciar el registro | No: no se vio ningún resultado real antes de la corrida final, y no se cambió ninguna regla, parámetro, dato ni ventana entre ambas corridas |
| 2026-09-25 | Se agregaron al script columnas de "no convergió" en las tablas de evaluación (antes de la corrida de humo) | Transparencia del estimador. Resultado: 0 casos | No |
| 2026-09-25 | Se agregó una tabla descriptiva **no pre-registrada** de rendimiento neto en 5 ventanas (2000-2002, 2007-2009, 2019-2020, 2022-2024 y 2025-2026) | Mostrar dónde gana o pierde cada regla | No: es descriptiva y no se usa para seleccionar |
| 2026-09-25 | Se agregó `R07_verificacion.py` **después** de ver los resultados. Recalcula sin el motor comprar y mantener, `inv3` e `inv_fuera12`, y reporta un descriptivo **post hoc**: meses con S < 0 antes de 1966, y el mínimo de S y la probabilidad máxima en tiempo real en los 24 meses previos a cada pico del NBER | Segunda implementación y contexto de calibración | No: no registra corridas y no cambia ninguna regla. Lo post hoc se marca como tal |
| 2026-09-25 | El script (escrito antes de la corrida) incluyó dos cortes que el pre-registro no lista: (a) el probit mensual **dentro de muestra** solo con orígenes 1998-03 a 2025-08, y (b) la evaluación fuera de muestra con orígenes 1998-03 a **2021-10** (sin el episodio 2022-2024 como origen) | Aislar cuánto pesa 2022-2024 | No: son descriptivos. El veredicto de H3 usa la ventana pre-registrada (orígenes hasta 2025-08) |
| 2026-09-25 | Revisión de GS10 y TB3MS en ALFRED: no se buscó el "primer vintage disponible". Se usaron los vintages 1996-12-31, 1998-02-27, 2000-01-15, 2008-12-31, 2020-06-30 y 2026-09-24 (todos existieron) | Simplificación del código | No |
| 2026-09-25 | En la tabla de A4, el script llena con 0 los objetivos posteriores a 2026-08 (desconocidos) solo para poder calcular las probabilidades de los orígenes 2025-09 a 2026-08. Esos 0 **no** entran a ninguna evaluación y se imprimen como "desconocido" | Mostrar la probabilidad actual | No |

### 10. Variantes probadas

- Archivo: `replicas/R07-variantes.csv`, con 111 filas y 37 corridas. Cada corrida tiene 3 segmentos: `completo`, `dentro_muestra` (1971-01 a 1998-02) y `fuera_muestra` (1998-03 a 2026-07).
- Variantes con `es_prueba=1`: **8** (`inv1`, `inv3`, `inv3_medio`, `probit50`, `probit30`, `probit_cont`, `inv_fuera12` y `desinv12`), cada una registrada una sola vez.
- Corridas con `es_prueba=0`: 29. Son 3 reglas sencillas, 20 de costos (10 reglas × spread medio y bruto), 3 con el spread en base descuento y 3 en MXN.
- Pruebas fuera del registro: las de la parte A (probits de la réplica estadística; no son estrategias) y la corrida de humo sin registro. No hubo pruebas en otra sesión. El N conservador pre-registrado es 16.
- Salida de `sharpe_deflactado_de_registro`:

| Lectura | segmento | variante | DSR | cumple 0.95 | N | V (SR periodo) | SR anual | SR0 anual | n | PSR sin deflactar |
|---|---|---|---|---|---|---|---|---|---|---|
| dentro_N_registrado | dentro_muestra | inv_fuera12 | 0.9947 | True | 8 | 0.000228 | 0.6143 | 0.0763 | 326 | 0.9982 |
| dentro_N_conservador | dentro_muestra | inv_fuera12 | 0.9933 | True | 16 | 0.000228 | 0.6143 | 0.0941 | 326 | 0.9982 |
| fuera_N_registrado | fuera_muestra | inv_fuera12 | 0.9728 | True | 8 | 0.000112 | 0.4331 | 0.0535 | 341 | 0.9859 |
| fuera_N_conservador | fuera_muestra | inv_fuera12 | 0.9685 | True | 16 | 0.000112 | 0.4331 | 0.0660 | 341 | 0.9859 |

- **Cómo leerlo.** La variante elegida dentro de muestra es `inv_fuera12`, con Sharpe neto de 0.6143. Su DSR es ≥ 0.95 dentro y fuera de muestra, con N = 8 y con N = 16. Pero **el DSR se mide contra un Sharpe de cero, no contra comprar y mantener**. Fuera de muestra, comprar y mantener tuvo Sharpe 0.5092 y `inv_fuera12` 0.4331: el DSR alto no dice que la regla le gane al índice.

### 11. Resultados

#### 11.0 Datos y verificaciones

- French `F-F_Research_Data_Factors`: CRSP 202607, sha256 `b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb`, 1926-07-31 a 2026-07-31.
- GS10 de 1953-04 a 2026-08; TB3MS de 1934-01 a 2026-08; spread de 1953-04 a 2026-08 (881 meses). USREC hasta 2026-08; USRECQ hasta 2026T2. T10Y3M diario de 1982-01-04 a 2026-09-24 (11,185 observaciones). DEXMXUS hasta 2026-09-18.
- **Control del spread.** S = GS10 − BEY(TB3MS) contra el promedio mensual de T10Y3M, en 536 meses (1982-01 a 2026-08): diferencia media +0.0089 pp, máxima |dif| 0.1345 pp, correlación 0.99987. Con la base descuento sin convertir, la diferencia media es +0.1161 pp. **Hay 4 meses con signo distinto:** 2019-05 (S +0.00, T10Y3M −0.01), 2025-06 (S +0.04, T10Y3M −0.04), 2025-07 (S +0.03, T10Y3M −0.02) y 2025-08 (S +0.04, T10Y3M −0.04).
- **Revisiones (ALFRED).** GS10: 0 diferencias en los vintages de 1996-12-31, 1998-02-27, 2000-01-15, 2008-12-31, 2020-06-30 y 2026-09-24. TB3MS: 0 diferencias, salvo el vintage de 2008-12-31, con 2 valores distintos (diferencia máxima 0.0100 pp). Las tasas prácticamente no se revisan.
- **Etiquetas en tiempo real contra ALFRED.** En los 17 vintages de USREC probados (fin de año de 2014 a 2025; 5 y 10 de junio de 2020; 16 y 21 de julio de 2021; 24 de septiembre de 2026), la etiqueta construida con los anuncios del NBER coincidió con ALFRED en **todos** los meses comparados (0 discrepancias; de 668 a 812 meses por fecha).
- Giros usados (1959 en adelante) y fecha en que se consideran conocidos: pico 1960-04 → 1961-04-30 (supuesto de 12 meses); valle 1961-02 → 1962-02-28 (supuesto); pico 1969-12 → 1970-12-31 (supuesto); valle 1970-11 → 1971-11-30 (supuesto); pico 1973-11 → 1974-11-30 (supuesto); valle 1975-03 → 1976-03-31 (supuesto); de 1980 en adelante, las fechas de anuncio del NBER de la sección 3.

#### 11.1 Periodo del artículo, dentro de muestra (A1, H1)

Probit trimestral, spread = GS10 − BEY(TB3MS) en promedio trimestral. Ventana principal: origen q en [1959T1, 1995T1 − k].

| k | n | n recesión | a | b | pseudo R² | Artículo R² | t MV | t NW(k-1) | t NW(k) | Artículo t | R² ventana objetivo | t NW(k-1) ventana objetivo | R² spread descuento |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 144 | 21 | -0.7738 | -0.2995 | 0.061 | 0.071 | -2.88 | -2.87 | -2.64 | -2.71 | 0.061 | -2.87 | 0.048 |
| 2 | 143 | 21 | -0.6238 | -0.5958 | 0.197 | 0.211 | -4.58 | -4.27 | -4.24 | -4.21 | 0.196 | -4.28 | 0.172 |
| 3 | 142 | 21 | -0.5893 | -0.7456 | 0.269 | 0.271 | -5.00 | -5.08 | -5.03 | -4.71 | 0.269 | -5.11 | 0.247 |
| 4 | 141 | 21 | -0.5881 | -0.7838 | **0.287** | **0.296** | -5.08 | **-4.72** | -4.97 | **-4.57** | 0.286 | -4.75 | 0.272 |
| 5 | 140 | 21 | -0.6061 | -0.6779 | 0.234 | 0.256 | -4.79 | -4.03 | -4.15 | -3.87 | 0.231 | -4.07 | 0.227 |
| 6 | 139 | 21 | -0.6679 | -0.4782 | 0.136 | 0.149 | -3.94 | -3.86 | -4.00 | -4.13 | 0.133 | -3.92 | 0.133 |
| 7 | 138 | 20 | -0.7678 | -0.3440 | 0.075 | 0.078 | -3.05 | -2.93 | -2.90 | -3.02 | 0.070 | -2.94 | 0.072 |
| 8 | 137 | 19 | -0.8831 | -0.2176 | 0.031 | 0.031 | -2.02 | -1.58 | -1.58 | -1.63 | 0.024 | -1.45 | 0.029 |

Contraste con *Current Issues* 1996 (k = 4):

| Ventana | a | b | spread con p=10% | spread con p=50% | spread con p=90% |
|---|---|---|---|---|---|
| origen 1960T1 a 1994T1 | -0.6597 | -0.8084 | 0.77 | -0.82 | -2.40 |
| objetivo 1960T1 a 1995T1 | -0.5881 | -0.7838 | 0.88 | -0.75 | -2.39 |
| Current Issues 1996 (tabla) | -0.6651 (implícito) | -0.8111 (implícito) | 0.76 | -0.82 | -2.40 |

- **H1: Replicado.** Con k = 4, pseudo R² de 0.287 contra 0.296 (−0.009) y t NW(3) de −4.72 contra −4.57. El patrón también se reproduce: el máximo está en k = 4 y los valores de k = 1 (0.061) y k = 8 (0.031) son menores que 0.10. Los 8 pseudo R² quedan a 0.022 o menos de los del artículo, y los t tienen el mismo signo y significancia (k = 8 no es significativo en ninguno de los dos).
- La tabla de *Current Issues* se reproduce casi exacta con orígenes desde 1960T1: el spread que da 50% es −0.82 y el que da 90% es −2.40.

#### 11.2 Periodo del artículo, fuera de muestra (A2, H2)

Objetivos 1971T1-1995T1, estimación recursiva con s + k ≤ q (cronología final).

| k | n | n recesión | pseudo R² (L_c ex post) | Artículo | pseudo R² (L_c recursiva) | Brier | Brier clima recursiva | AUC | fallos / no convergió |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 97 | 14 | 0.041 | 0.072 | 0.053 | 0.1224 | 0.1250 | 0.7151 | 0 / 0 |
| 2 | 97 | 14 | 0.218 | 0.236 | 0.246 | 0.0964 | 0.1271 | 0.8761 | 0 / 0 |
| 3 | 97 | 14 | 0.296 | 0.328 | 0.332 | 0.0809 | 0.1283 | 0.9148 | 0 / 0 |
| 4 | 97 | 14 | **0.294** | **0.295** | 0.333 | 0.0816 | 0.1289 | 0.9131 | 0 / 0 |
| 5 | 97 | 14 | 0.280 | 0.155 | 0.318 | 0.0862 | 0.1288 | 0.8855 | 0 / 0 |
| 6 | 97 | 14 | 0.175 | 0.141 | 0.209 | 0.0995 | 0.1283 | 0.8124 | 0 / 0 |
| 7 | 97 | 14 | -0.004 | negativo | 0.030 | 0.1238 | 0.1281 | 0.6145 | 0 / 0 |
| 8 | 97 | 14 | -0.215 | negativo | -0.182 | 0.1459 | 0.1284 | 0.3718 | 0 / 0 |

- **H2: Replicado.** Con k = 4, 0.294 contra 0.295. Positivo en k = 2, 3 y 4, y negativo en k = 7 y 8, como en el artículo. **Diferencias no explicadas:** k = 5 da 0.280 contra 0.155, y k = 1 da 0.041 contra 0.072.

#### 11.3 Extensión mensual, 12 meses adelante, y después de la publicación (A3, H3)

Dentro de muestra:

| Ventana de origen | n | n recesión | a | b | pseudo R² | t MV | t NW(11) | t NW(12) |
|---|---|---|---|---|---|---|---|---|
| 1959-01 a 1994-03 (era del artículo) | 423 | 67 | -0.5695 | -0.6726 | 0.250 | -8.54 | -4.10 | -4.12 |
| 1959-01 a 2025-08 (muestra completa) | 800 | 95 | -0.7692 | -0.5530 | 0.155 | -9.63 | -4.54 | -4.53 |
| 1998-03 a 2025-08 (solo post-publicación) | 330 | 28 | -1.0546 | -0.3274 | 0.049 | -3.79 | -1.94 | -1.93 |

Fuera de muestra (estimación recursiva; el objetivo se evalúa con la cronología final de hoy):

| Pronóstico | n | n recesión | pseudo R² (L_c ex post) | pseudo R² (L_c recursiva) | Brier | Brier clima recursiva | Brier constante ex post | AUC | VP/FP/FN/VN (p>0.5) | VP/FP/FN/VN (p>0.3) | fallos / no convergió |
|---|---|---|---|---|---|---|---|---|---|---|---|
| era 1970-01 a 1998-02, cronología final | 338 | 46 | 0.2510 | 0.2910 | 0.0850 | 0.1230 | 0.1176 | 0.9033 | 19/14/27/278 | 27/22/19/270 | 0 / 0 |
| era 1970-01 a 1998-02, tiempo real | 338 | 46 | 0.2780 | 0.3174 | 0.0807 | 0.1232 | 0.1176 | 0.9054 | 21/13/25/279 | 27/20/19/272 | 0 / 0 |
| **post 1998-03 a 2025-08, tiempo real (PRINCIPAL H3)** | 330 | 28 | **-0.0336** | 0.0045 | **0.0899** | **0.0819** | 0.0776 | **0.7092** | 0/17/28/285 | 8/34/20/268 | 0 / 0 |
| post 1998-03 a 2025-08, cronología final | 330 | 28 | -0.0311 | 0.0015 | 0.0898 | 0.0812 | 0.0776 | 0.7157 | 0/17/28/285 | 8/34/20/268 | 0 / 0 |
| post 1998-03 a 2025-08, coeficientes fijos 1959-01 a 1994-03 | 330 | 28 | -0.0183 | 0.0293 | 0.0910 | 0.0831 | 0.0776 | 0.7372 | 0/19/28/283 | 10/36/18/266 | 0 / 0 |
| post 1998-03 a 2024-02, tiempo real (sensibilidad) | 312 | 28 | 0.0048 | 0.0415 | 0.0872 | 0.0858 | 0.0817 | 0.7369 | 0/13/28/271 | 8/26/20/258 | 0 / 0 |
| post 1998-03 a 2021-10, tiempo real (sin el episodio 2022-2024 como origen) | 284 | 28 | 0.0949 | 0.1293 | 0.0764 | 0.0927 | 0.0889 | 0.7828 | 0/0/28/256 | 8/10/20/246 | 0 / 0 |

- **H3: refutada** con la métrica principal: pseudo R² de −0.0336 (≤ 0) y Brier de 0.0899, peor que el 0.0819 de la climatología recursiva. Con L_c recursiva el pseudo R² es apenas positivo (0.0045). El AUC de 0.709 dice que las probabilidades ordenan mejor que el azar, pero no están calibradas.
- **El resultado depende del episodio 2022-2024.** Si se excluyen los orígenes desde 2021-11, el pseudo R² es 0.0949 y el Brier (0.0764) le gana a la climatología (0.0927). Es una sensibilidad (declarada en el pre-registro solo hasta 2024-02); no cambia el veredicto.
- **Nunca pasó de 0.5 antes de una recesión después de 1998.** Con umbral 0.5 hubo 0 aciertos y 17 falsas alarmas, todas en 2023-2024. Las probabilidades máximas en tiempo real en los 24 meses previos a cada pico fueron (descriptivo post hoc, `R07_verificacion.py`): 0.791 antes de 1973-11, 0.918 antes de 1980-01, 0.999 antes de 1981-07, **0.306 antes de 1990-07, 0.436 antes de 2001-03, 0.403 antes de 2007-12 y 0.377 antes de 2020-02**. El máximo posterior a 1998 fue **0.713 (origen 2023-05), sin recesión**.
- La versión de etiquetas en tiempo real y la de cronología final dan casi lo mismo (−0.0336 contra −0.0311): el rezago del NBER no explica el fracaso.
- **Descriptivo post hoc:** de 1953-04 a 1965-12 no hubo ningún mes con S < 0. En los 24 meses previos a los picos de 1957-08 y 1960-04, el mínimo de S fue +0.17 y +0.09: con esta medida, esas dos recesiones no tuvieron inversión previa.

#### 11.4 El episodio 2022-2024 (A4, H4)

- **Meses invertidos.** S < 0 en 27 meses: de 2022-11 a 2024-11 (25 seguidos) más 2025-03 y 2025-04. El promedio mensual de T10Y3M fue < 0 en 30 meses: los mismos más 2025-06, 2025-07 y 2025-08. El mínimo mensual de S fue −1.71 (2023-05).
- **Racha diaria de T10Y3M < 0:** 534 sesiones seguidas, del 2022-10-25 al 2024-12-12, con mínimo de −1.89 el 2023-05-04. Es la racha más larga desde 1982; siguen 217 sesiones en 2006-2007 (mínimo −0.64), 127 en 2000-2001 (−0.95) y 56 y 41 en 2019. **Esto confirma las cifras del cap. 04 §5.1.**
- **Resultado:** en la ventana de verificación 2022-12 a 2026-04 (del mes siguiente a la primera inversión a 12 meses después de la última), USREC = 1 en **0 meses**, y la tabla de anuncios no tiene picos posteriores a abr-2020. **Veredicto H4: falso positivo a la fecha (2026-09-25).** Salvedad: el NBER anunció sus picos de 1980-2020 entre unos 4 y 12 meses después del mes del pico; un pico en 2025-2026 todavía podría fecharse.
- **Probabilidad en tiempo real:** máximo de 0.713 en 2023-05; 17 meses con P > 0.5 y 24 con P > 0.3 (orígenes 2021-01 a 2025-12). Con los coeficientes fijos de 1959-1994, el máximo fue 0.719, también en 2023-05.
- **Lectura actual:** con origen en 2026-08 y S = +0.87, P(recesión en 12 meses) = **0.105** en tiempo real y 0.124 con los coeficientes de 1959-1994. El promedio de T10Y3M en septiembre de 2026 (17 sesiones) es +0.87, lo que en el mismo modelo da 0.105. Último dato diario: T10Y3M = +0.94 el 2026-09-24.

#### 11.5 Rendimiento del mercado después del inicio de una inversión (A5, H5)

Inicio = primer mes con S < 0 tras ≥ 12 meses con S ≥ 0. Rendimiento compuesto de French (Mkt-RF + RF, USD), desde el mes siguiente al inicio.

| Inicio | S | 6 m | 12 m | 18 m | 24 m | exceso 12 m | MDD en 24 m | meses al máximo (24 m) | meses hasta el pico NBER |
|---|---|---|---|---|---|---|---|---|---|
| 1966-01 | -0.10 | -8.00% | -2.06% | 11.43% | 11.87% | -6.86% | -15.49% | 23 | 47 |
| 1968-12 | -0.11 | -7.46% | -10.95% | -31.14% | -10.87% | -17.52% | -31.14% | 0 | 12 |
| 1973-06 | -0.52 | -4.26% | -15.62% | -30.88% | 0.41% | -23.64% | -41.20% | 3 | 5 |
| 1978-11 | -0.15 | 9.69% | 22.17% | 31.03% | 72.68% | 11.97% | -11.99% | 24 | 14 |
| 1989-06 | -0.16 | 10.62% | 13.04% | 3.96% | 21.02% | 4.90% | -16.92% | 23 | 13 |
| 2000-07 | -0.09 | -5.26% | -15.77% | -20.00% | -34.55% | -21.10% | -39.14% | 1 | 8 |
| 2006-08 | -0.21 | 9.79% | 15.38% | 5.54% | 3.82% | 10.31% | -16.28% | 14 | 16 |
| 2019-06 | -0.14 | 10.02% | 7.89% | 36.49% | 56.46% | 6.55% | -20.22% | 24 | 8 |
| 2022-11 | -0.36 | 2.73% | 13.06% | 31.74% | 53.09% | 8.22% | -9.12% | 24 | ninguno |

| Horizonte | n eventos | media eventos | mediana eventos | eventos > 0 | n ventanas incond. | media incond. | desv. est. incond. | t aprox. |
|---|---|---|---|---|---|---|---|---|
| 6 m | 9 | 1.99% | 2.73% | 5 | 862 | 6.07% | 11.38% | -1.08 |
| 12 m | 9 | 3.01% | 7.89% | 5 | 856 | 12.38% | 16.71% | -1.68 |
| 18 m | 9 | 4.24% | 5.54% | 6 | 850 | 18.81% | 20.80% | -2.10 |
| 24 m | 9 | 19.32% | 11.87% | 7 | 844 | 25.42% | 23.99% | -0.76 |

- **H5: se sostiene mi expectativa** en el horizonte pre-registrado de 12 meses: la media (3.01%) es menor que la incondicional (12.38%), pero con t aproximado de −1.68 (> −2). En 18 meses el t es −2.10; ese horizonte no era el principal y el t ignora el traslape.
- La dispersión es enorme: a 12 meses, de −15.77% (2000-07) a +22.17% (1978-11); 5 de 9 inicios tuvieron rendimiento positivo. En 5 de 9 casos (1966-01, 1978-11, 1989-06, 2019-06 y 2022-11) el índice hizo su máximo de 24 meses en el mes 23 o 24: la bolsa siguió subiendo casi dos años después del inicio de la inversión.
- 2022-11: +13.06% a 12 meses y +53.09% a 24 meses, con MDD de −9.12%.

#### 11.6 Reglas operables contra las reglas sencillas (motor, USD, costos por defecto; H6)

Primera decisión 1971-01-31 (`min_historia` = 534); corte 1998-02-28.

**`dentro_muestra` (1970-12-31 a 1998-02-28, n = 326)**

| Variante | CAGR | Vol | Sharpe | Sortino | MDD | Calmar | Exposición media | Rotación anual | Costo anual | Cambios de señal |
|---|---|---|---|---|---|---|---|---|---|---|
| inv1 | 14.70% | 13.38% | 0.6002 | 0.9435 | -29.85% | 0.4926 | 0.844 | 0.552 | 0.188% | 15 |
| inv3 | 15.25% | 14.28% | 0.6043 | 0.9573 | -29.85% | 0.5109 | 0.883 | 0.331 | 0.113% | 9 |
| inv3_medio | 14.41% | 14.59% | 0.5430 | 0.8481 | -36.54% | 0.3942 | 0.942 | 0.196 | 0.067% | 9 |
| probit50 | 15.41% | 14.44% | 0.6097 | 0.9597 | -32.85% | 0.4690 | 0.896 | 0.626 | 0.213% | 17 |
| probit30 | 14.70% | 13.58% | 0.5929 | 0.9330 | -29.85% | 0.4924 | 0.856 | 0.479 | 0.163% | 13 |
| probit_cont | 14.10% | 13.18% | 0.5660 | 0.8891 | -29.62% | 0.4760 | 0.860 | 0.499 | 0.170% | 326 |
| **inv_fuera12** | 14.01% | 11.76% | **0.6143** | 0.9678 | -29.85% | 0.4694 | 0.709 | 0.258 | 0.088% | 7 |
| desinv12 | 12.51% | 13.23% | 0.4589 | 0.6734 | -34.47% | 0.3630 | 0.844 | 0.331 | 0.113% | 9 |
| comprar_y_mantener | 13.47% | 15.46% | 0.4676 | 0.7030 | -46.51% | 0.2897 | 1.000 | 0.037 | 0.013% | 1 |
| efectivo | 6.84% | 0.78% | 0.0000 | 0.0000 | 0.00% | inf | 0.000 | 0.000 | 0.000% | 0 |
| sma10 | 11.63% | 12.62% | 0.4123 | 0.5914 | -24.84% | 0.4683 | 0.767 | 1.436 | 0.488% | 39 |

**`fuera_muestra` (1998-02-28 a 2026-07-31, n = 341)**

| Variante | CAGR | Vol | Sharpe | Sortino | MDD | Calmar | Exposición media | Rotación anual | Costo anual | Cambios de señal |
|---|---|---|---|---|---|---|---|---|---|---|
| inv1 | 8.54% | 14.73% | 0.4899 | 0.7231 | -50.31% | 0.1697 | 0.856 | 0.422 | 0.144% | 12 |
| inv3 | 8.41% | 15.23% | 0.4715 | 0.6887 | -50.31% | 0.1672 | 0.889 | 0.282 | 0.096% | 8 |
| inv3_medio | 8.87% | 15.39% | 0.4961 | 0.7236 | -50.31% | 0.1764 | 0.944 | 0.151 | 0.051% | 8 |
| probit50 | 8.74% | 15.70% | 0.4817 | 0.6991 | -50.31% | 0.1737 | 0.950 | 0.211 | 0.072% | 6 |
| probit30 | 7.89% | 15.22% | 0.4401 | 0.6386 | -50.31% | 0.1569 | 0.877 | 0.282 | 0.096% | 8 |
| probit_cont | 8.10% | 14.01% | 0.4794 | 0.6942 | -49.22% | 0.1646 | 0.867 | 0.236 | 0.080% | 341 |
| **inv_fuera12** | 7.15% | 13.21% | **0.4331** | 0.6225 | **-46.06%** | 0.1552 | 0.707 | 0.282 | 0.096% | 8 |
| desinv12 | 9.39% | 14.45% | 0.5521 | 0.8125 | -41.62% | 0.2256 | 0.859 | 0.282 | 0.096% | 8 |
| comprar_y_mantener | 9.28% | 15.91% | **0.5092** | 0.7409 | **-50.31%** | 0.1845 | 1.000 | 0.000 | 0.000% | 0 |
| efectivo | 2.09% | 0.58% | 0.0000 | 0.0000 | 0.00% | inf | 0.000 | 0.000 | 0.000% | 0 |
| sma10 | 8.20% | 10.88% | **0.5881** | 0.8916 | **-19.31%** | 0.4245 | 0.751 | 1.548 | 0.526% | 44 |

La tabla del segmento `completo` (1971-01 a 2026-07) está en `R07-salida.txt`: ahí comprar y mantener tiene Sharpe 0.4894 y MDD −50.31%, y la SMA10 0.4945 y −24.84%.

**Veredictos mecánicos de H6:**

- La elegida dentro de muestra es `inv_fuera12` (Sharpe 0.6143 contra 0.4676 de comprar y mantener).
- Fuera de muestra tuvo Sharpe 0.4331, contra 0.5092 de comprar y mantener y 0.5881 de la SMA10, y MDD de −46.06%, contra −50.31% y −19.31%.
- **No agrega valor** frente a comprar y mantener ni frente a la regla sencilla. **H6 queda refutada** (Sharpe fuera ≤ comprar y mantener).
- **El uso como freno no se refuta** para `inv_fuera12`: su MDD fue menor en ambos tramos (−29.85% contra −46.51% dentro, y −46.06% contra −50.31% fuera). Pero la SMA10 frena mucho más fuera de muestra (−19.31%).
- Solo `desinv12` superó a comprar y mantener fuera de muestra en Sharpe (0.5521) y en MDD (−41.62%). Fue la **peor** dentro de muestra (0.4589, debajo de comprar y mantener), así que elegirla sería usar el tramo de prueba para seleccionar.
- **Verificaciones:** `R07_verificacion.py` recalculó sin el motor comprar y mantener, `inv3` e `inv_fuera12`. Coinciden a 4 decimales en Sharpe y a 2 en MDD, en ambos tramos. La exposición de `probit50` del motor coincidió con el cálculo externo en las 114 decisiones comparadas (0 discrepancias).

**Rendimiento neto en ventanas descriptivas (no pre-registradas):**

| Variante | 2000-03 a 2002-09 | 2007-10 a 2009-02 | 2019-06 a 2020-12 | 2022-11 a 2024-12 | 2025-01 a 2026-07 |
|---|---|---|---|---|---|
| inv1 | -30.08% | -49.26% | 63.10% | 15.89% | 21.31% |
| inv3 | -29.23% | -49.26% | 40.37% | 15.67% | 28.43% |
| inv3_medio | -35.64% | -49.26% | 43.30% | 34.89% | 28.64% |
| probit50 | -41.80% | -49.26% | 46.28% | 35.46% | 28.86% |
| probit30 | -32.66% | -49.26% | 42.29% | 11.85% | 28.86% |
| probit_cont | -36.03% | -48.29% | 38.94% | 31.78% | 24.08% |
| inv_fuera12 | -22.93% | -45.08% | 8.30% | 15.89% | 9.43% |
| desinv12 | -34.79% | -40.04% | 29.66% | 56.15% | 13.52% |
| comprar_y_mantener | -41.80% | -49.26% | 46.28% | 56.15% | 28.86% |
| efectivo | 10.39% | 2.55% | 1.58% | 11.14% | 6.45% |
| sma10 | -8.96% | -1.81% | 29.81% | 26.47% | 9.98% |

- En 2007-10 a 2009-02, `inv1`, `inv3`, `inv3_medio`, `probit50` y `probit30` perdieron 49.26%, igual que el índice; `probit_cont`, `inv_fuera12` y `desinv12` perdieron 48.29%, 45.08% y 40.04%. La racha diaria de T10Y3M < 0 terminó el 2007-05-29, y S ya era positivo en 2007-07 (+0.05) y en 2008-01 (+0.93) (salida de A3 en `R07-salida.txt`): las reglas de inversión estaban de vuelta en el mercado antes de la caída.
- En 2022-11 a 2024-12, la regla del sistema (`inv3`) ganó 15.67% contra 56.15% del índice.

### 12. Sensibilidad

**Costos (Sharpe dentro / fuera, MDD y CAGR fuera):**

| Variante | Escenario | Sharpe dentro | Sharpe fuera | MDD fuera | CAGR fuera | Costo anual fuera |
|---|---|---|---|---|---|---|
| inv1 | spread_medio | 0.5959 | 0.4871 | -50.31% | 8.49% | 0.186% |
| inv3 | spread_medio | 0.6019 | 0.4696 | -50.31% | 8.38% | 0.124% |
| inv3_medio | spread_medio | 0.5416 | 0.4951 | -50.31% | 8.86% | 0.066% |
| probit50 | spread_medio | 0.6053 | 0.4803 | -50.31% | 8.72% | 0.093% |
| probit30 | spread_medio | 0.5895 | 0.4381 | -50.31% | 7.86% | 0.124% |
| probit_cont | spread_medio | 0.5622 | 0.4777 | -49.23% | 8.08% | 0.104% |
| inv_fuera12 | spread_medio | 0.6122 | 0.4309 | -46.12% | 7.12% | 0.124% |
| desinv12 | spread_medio | 0.4564 | 0.5502 | -41.62% | 9.36% | 0.124% |
| comprar_y_mantener | spread_medio | 0.4674 | 0.5092 | -50.31% | 9.28% | 0.000% |
| sma10 | spread_medio | 0.4007 | 0.5734 | -19.79% | 8.03% | 0.681% |
| inv1 | bruto | 0.6143 | 0.4996 | -50.31% | 8.69% | 0.000% |
| inv3 | bruto | 0.6125 | 0.4780 | -50.31% | 8.51% | 0.000% |
| inv3_medio | bruto | 0.5476 | 0.4996 | -50.31% | 8.93% | 0.000% |
| probit50 | bruto | 0.6246 | 0.4861 | -50.31% | 8.82% | 0.000% |
| probit30 | bruto | 0.6045 | 0.4466 | -50.31% | 8.00% | 0.000% |
| probit_cont | bruto | 0.5790 | 0.4851 | -49.19% | 8.19% | 0.000% |
| inv_fuera12 | bruto | 0.6211 | 0.4406 | -45.88% | 7.25% | 0.000% |
| desinv12 | bruto | 0.4676 | 0.5585 | -41.62% | 9.49% | 0.000% |
| comprar_y_mantener | bruto | 0.4683 | 0.5092 | -50.31% | 9.28% | 0.000% |
| sma10 | bruto | 0.4512 | 0.6374 | -17.64% | 8.77% | 0.000% |

- Las reglas de curva giran poco (de 0.151 a 0.422 de rotación anual fuera de muestra, contra 1.548 de la SMA10); los costos no cambian ninguna conclusión. Aun **en bruto**, ninguna regla de inversión ni de probit supera a comprar y mantener fuera de muestra (la mejor es 0.4996 contra 0.5092). La excepción es `desinv12` (0.5585).

**Spread con el T-bill en base descuento (GS10 − TB3MS):**

| Variante | Sharpe dentro | MDD dentro | Sharpe fuera | MDD fuera | Cambios de señal |
|---|---|---|---|---|---|
| inv1 | 0.6273 | -29.85% | 0.4847 | -50.31% | 19 |
| inv3 | 0.5912 | -29.85% | 0.4333 | -50.31% | 15 |
| inv3_medio | 0.5361 | -36.54% | 0.4760 | -50.31% | 15 |

Cambia el número de cambios de señal en todo el periodo: de 27, 17 y 17 (spread BEY) a 19, 15 y 15 (base descuento), según el conteo del segmento `completo`. El veredicto no cambia: fuera de muestra, las tres quedan debajo de comprar y mantener.

**Definición de la tasa corta.** Con el promedio mensual de T10Y3M (3 meses CMT), jun-ago 2025 fueron negativos (−0.04, −0.02, −0.04). Con S (BEY del secundario) fueron positivos (+0.04, +0.03, +0.04). Con T10Y3M, la regla 6(1) del cap. 04 ("≥ 3 meses < 0") se habría encendido en 2025-08; con S, no. La diferencia media entre ambas medidas es de 0.009 pp, pero cerca de cero decide el signo.

**MXN (DEXMXUS; RF en USD convertida):**

| Variante | Segmento | CAGR | Vol | Sharpe | MDD |
|---|---|---|---|---|---|
| inv_fuera12 | fuera_muestra (1998-03 a 2026-07) | 9.85% | 12.98% | 0.3786 | -29.62% |
| comprar_y_mantener | fuera_muestra | 12.04% | 14.00% | 0.4465 | -39.86% |
| sma10 | fuera_muestra | 10.93% | 12.65% | 0.5472 | -24.01% |

- El tramo `dentro_muestra` en MXN tiene solo 51 meses (1993-12 a 1998-02) sin ninguna inversión, así que `inv_fuera12` es igual a comprar y mantener.
- En pesos se repite el patrón: la regla de curva pierde Sharpe frente al índice y frena menos que la SMA10.

**Subperiodos.** Dentro de muestra (1971-1998), todas las reglas de inversión y de probit, salvo `desinv12`, tuvieron mejor Sharpe que comprar y mantener; fuera de muestra, ninguna salvo `desinv12`. No se calculó el rendimiento por subperiodo dentro de 1971-1998, así que no se sabe qué años explican la ventaja. Lo que sí se midió (post hoc, `R07_verificacion.py`): antes de los picos de 1973, 1980 y 1981, el mínimo de S en los 24 meses previos fue de −1.59 a −3.51 y la probabilidad máxima en tiempo real de 0.791 a 0.999. Antes de los picos de 1990, 2001, 2007 y 2020, el mínimo fue de −0.16 a −0.70 y la probabilidad máxima de 0.306 a 0.436. En 2022-2024 el mínimo fue −1.71 sin recesión.

### 13. Diferencia frente al artículo

| Aspecto | Artículo | Réplica | ¿Explica la diferencia? |
|---|---|---|---|
| Versión del texto | REStat 80(1), 1998. Cifras tomadas del RP 9609 (abril/mayo de 1996) | Las del RP 9609 | No se comprobó que REStat tenga las mismas tablas (texto de pago) |
| Datos / versión | Tasas de la Fed de la época; "3-month Treasury bill, market yield, bond equivalent" | FRED GS10 y TB3MS de hoy. Rendimiento equivalente calculado con 365·d/(360 − 91·d). ALFRED: casi sin revisiones (TB3MS: 2 valores distintos en 2008) | Puede explicar diferencias de milésimas en el pseudo R² |
| Periodo | "1959T1 a 1995T1", sin decir si se refiere al origen o al objetivo | Ambas ventanas. Se replica con las dos (0.287 y 0.286 con k = 4) | No cambia el resultado |
| NBER | Cronología de 1995-96, trimestral | USRECQ de hoy (misma cronología para 1959-1995) | No cambia |
| Errores estándar | NW sobre las condiciones de primer orden, sin decir los rezagos | NW con k−1 y k rezagos | t de −4.72 y −4.97 contra −4.57 con k = 4. No se identificó el número exacto de rezagos |
| Pseudo R² fuera de muestra | Fórmula de Estrella; no se dice qué L_c se usa | L_c ex post (principal) y recursiva | Con k = 4 la principal coincide (0.294 contra 0.295). **No explicado:** k = 5 (0.280 contra 0.155) y k = 1 (0.041 contra 0.072) |
| Frecuencia | Trimestral (nota 8: mensual "the same" en orden, con peor ajuste) | Trimestral para replicar; mensual para extender (pseudo R² 0.250 en 1959-1994) | Coincide con la nota 8: el ajuste mensual es menor que el trimestral |
| Costos / estrategia | No hay estrategia | 8 reglas con costos GBM | Es una extensión, no parte del artículo |

### 14. Conclusiones permitidas

Alcance: EUA, recesiones del NBER, 1959-2026. Estrategias sobre el índice CRSP de French (no invertible), en USD (MXN como sensibilidad), con costos GBM declarados (comisión como hecho, spread como supuesto), sin impuestos ni costo cambiario.

1. **El hallazgo de Estrella y Mishkin se reproduce en su periodo con datos de hoy.** Con k = 4 trimestres: pseudo R² de 0.287 (artículo: 0.296) y t NW de −4.72 (−4.57) dentro de muestra; fuera de muestra (1971T1-1995T1), 0.294 (0.295). La tabla de *Current Issues* 1996 se reproduce: 50% ↔ −0.82 pp y 90% ↔ −2.40 pp.
2. **Después de la publicación, el probit en tiempo real no le ganó a la tasa base.** Con orígenes de 1998-03 a 2025-08 y objetivos de 1999-03 a 2026-08: pseudo R² de −0.034 y Brier de 0.0899, contra 0.0819 de la climatología. Conserva poder de ordenamiento (AUC 0.709), pero sus probabilidades no están calibradas.
3. **El fracaso se concentra en 2022-2024.** Sin esos orígenes (1998-03 a 2021-10), pseudo R² de 0.095 y Brier de 0.0764, contra 0.0927 de la climatología. Pero ahí el modelo tampoco pasó de 0.44 antes de ninguna recesión: con umbral 0.5 no dio ninguna alarma correcta después de 1998.
4. **2022-2024 fue un falso positivo a la fecha.** Hubo 534 sesiones con T10Y3M < 0 (2022-10-25 a 2024-12-12; mínimo de −1.89 el 2023-05-04), 25 meses seguidos con S < 0 y una probabilidad en tiempo real de hasta 0.713 (2023-05). USREC = 0 de 2022-12 a 2026-04, y el NBER no ha anunciado un pico posterior a feb-2020.
5. **Después de una inversión, el mercado de EUA rindió menos en promedio, pero no significativamente, y con dispersión enorme.** Fueron 9 inicios desde 1954. A 12 meses: media de 3.01% contra 12.38% incondicional (t ≈ −1.68), mediana de 7.89% y 5 de 9 positivos.
6. **Salir del mercado solo por la curva no mejoró el Sharpe fuera de muestra.** La regla elegida dentro de muestra (`inv_fuera12`) tuvo 0.4331 contra 0.5092 de comprar y mantener. La regla del sistema (`inv3`) tuvo 0.4715 y la misma MDD que el índice (−50.31%). La SMA10 dominó a todas fuera de muestra (0.5881 y −19.31%).
7. **Hoy la curva no da señal.** S = +0.87 en ago-2026 y T10Y3M = +0.94 el 2026-09-24. El modelo en tiempo real da P(recesión en 12 meses) = 0.105, pero esa cifra hereda la mala calibración del punto 2.

### 15. Conclusiones que NO se sostienen

- **"La curva ya no predice recesiones."** Después de 1998 hay solo 3 recesiones y un falso positivo mayor. Sin 2022-2024, el modelo tuvo pseudo R² positivo y Brier mejor que la climatología. Un solo episodio no demuestra un cambio estructural.
- **"2022-2024 fue definitivamente un falso positivo."** Lo es a la fecha. El NBER tardó de unos 4 a 12 meses en anunciar sus picos en 1980-2020 y podría fechar uno en 2025-2026.
- **"Una inversión anticipa una caída de la bolsa."** La media a 12 meses es menor, pero no es significativa con 9 eventos; en 5 de 9 casos el índice hizo su máximo de 24 meses en el mes 23 o 24.
- **"Salir con la curva invertida mejora el rendimiento ajustado por riesgo."** Queda refutado fuera de muestra para las 7 reglas de inversión y de probit. `desinv12` es la excepción ex post, pero fue la peor dentro de muestra: adoptarla sería seleccionar con el tramo de prueba.
- **"El DSR de 0.97-0.99 valida `inv_fuera12`."** El DSR se mide contra un Sharpe de cero; contra el índice, la regla pierde.
- **"La curva protege en las crisis."** En 2007-10 a 2009-02, `inv1`, `inv3`, `inv3_medio`, `probit50` y `probit30` perdieron 49.26%, igual que el índice; la MDD fuera de muestra de 5 de las 8 reglas fue la del índice (−50.31%).
- **"Funciona en pesos."** En MXN, fuera de muestra, `inv_fuera12` tuvo Sharpe 0.3786 contra 0.4465 del índice. Es una sensibilidad con DEXMXUS, que no es un tipo de cambio ejecutable.
- **"La probabilidad de 10.5% de hoy es un pronóstico calibrado."** Después de 1998 el modelo dio menos de 0.44 antes de cada recesión y más de 0.5 en 17 meses sin recesión.
- **"Toda recesión desde 1950 fue precedida por una inversión."** Con S mensual (post hoc), 1957 y 1960 no tuvieron ningún mes invertido en los 24 meses previos; el FAQ de Estrella dice "essentially every". La cifra del cap. 04 ("4 de 4 en 1989-2020") sí se confirma.

### 16. Estado y reproducción

- **Estado: Replicado.**
  - H1 y H2: el pseudo R² de k = 4 cae dentro de la tolerancia pre-registrada, dentro y fuera de muestra, en el periodo del artículo.
  - **Después de la publicación el resultado es negativo:** H3 queda refutada (pseudo R² −0.034; Brier peor que la climatología) y H6 también (ninguna regla supera a comprar y mantener fuera de muestra).
  - H4: falso positivo a la fecha. H5: sin diferencia significativa a 12 meses.
  - Diferencias no explicadas: k = 1 y k = 5 fuera de muestra.
  - No es candidata para dinero.
- Comando que reproduce todo: `python3 laboratorio/replicas/R07.py` (unos 15 s con caché; cada corrida agrega 37 corridas al CSV). La verificación sin el motor es `python3 laboratorio/replicas/R07_verificacion.py`.
- **Huella de datos:** `huella_datos` e85ac74d630dff95 (USD) y 6f7a2f88fb30b19e (MXN). Son las mismas de R05, porque usan el mismo archivo de French y el mismo DEXMXUS.
- **Archivos:**
  - French (CRSP 202607): `sha256` b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb.
  - FRED (GS10, TB3MS, USREC, USRECQ, T10Y3M y DEXMXUS) y ALFRED: descargados el 2026-09-25.
- Fecha de la corrida final: 2026-09-25, 06:37:09 UTC.
- **Evidencia del pre-registro:** el pre-registro (secciones 1 a 9) y `R07.py` quedaron en el commit `ae0d4f5` ("Avance de agentes", 2026-09-25 06:36:16 UTC), antes de la corrida final. `git diff` contra ese commit muestra que en la ficha solo se reemplazaron los dos marcadores ("(se llena al final)" y "(pendiente)"), y que `R07.py` no cambió.
- Pendiente:
  - Revisión independiente (`auditor-de-replicas`).
  - Fila de R07 en `laboratorio/tabla-maestra.md`.
  - Leer las tablas de la versión REStat 1998.
  - Condiciones de uso de FRED y French.
  - Probar el tablero completo de recesión del cap. 04 (5 señales), no solo la curva.
  - Probar el *near-term forward spread* de Engstrom y Sharpe, que el cap. 04 §2.11 cita como menos contaminado por la prima por plazo.

### 17. Conclusión operable

La réplica afecta tres puntos del sistema: el cap. 04 §5.1 y §7 (trampa 3); la **regla 6 (tablero de recesión)** y la **regla 10 (pronósticos registrados)** de §6.1; y la dimensión "Curva" de `herramientas/tablero.py`.

- **Confirma:**
  - Las cifras del cap. 04 §5.1: 534 sesiones (25-oct-2022 a 12-dic-2024), mínimo de −1.89 el 4-may-2023, inversión antes de las recesiones de 1990, 2001, 2008 y 2020, y 2 falsos positivos desde 1966 (1966 y 2022).
  - La trampa 3 ("leer la curva invertida como fecha de recesión"). Además, cuantifica que la curva **tampoco da una probabilidad calibrada** después de 1998.
- **Modifica la regla 6(1).** La curva queda como **1 punto de 5, nunca como disparador suficiente**, y se fija la serie. Texto propuesto:
  > (1) T10Y3M con promedio mensual < 0 por ≥ 3 meses (1 punto). **R07:** la curva sola no se usa para bajar exposición. Como regla aislada (`inv3`, w = 0 o 0.5), fuera de muestra (1998-2026) tuvo Sharpe de 0.4715 o 0.4961, contra 0.5092 de comprar y mantener, **sin reducir la caída máxima** (−50.31%, la misma del índice). En 2022-11 a 2024-12 ganó 15.67% contra 56.15% del índice. La definición importa cerca de cero: con T10Y3M, jun-ago 2025 cuentan como inversión; con GS10 − BEY(TB3MS), no.
  - El umbral de ≥ 3 puntos del tablero **no está validado**: los otros 4 componentes no se han replicado. Queda como pendiente de réplica, no como regla probada.
- **Modifica la regla 10 (pronóstico mensual de P(recesión en 12 m)).** Todo pronóstico de recesión se compara contra la climatología, no solo contra Brier ≤ 0.2. En 1998-2025, el probit de la curva tuvo Brier de 0.0899, que pasa el umbral absoluto de 0.2 pero es **peor** que la tasa base (0.0819). El probit de la curva puede ser un insumo, pero no el pronóstico registrado por sí solo.
- **Descarta:**
  - Como fuente de rendimiento, cualquier salida del mercado basada solo en la curva: `inv1`, `inv3`, `inv3_medio`, `probit50`, `probit30`, `probit_cont` e `inv_fuera12`. Ninguna superó a comprar y mantener fuera de muestra ni a la SMA10 (R01) en Sharpe y MDD.
  - La regla de "des-inversión" (`desinv12`): fue la peor dentro de muestra, y su buen resultado fuera de muestra no se puede usar sin un tramo nuevo de prueba.
- **Dimensión "Curva" de `tablero.py`:** se mantiene como descripción del régimen, sin peso de decisión.
- **Estado actual (2026-09-25):** la curva no aporta puntos al tablero. Los últimos 3 meses de T10Y3M y de S son positivos, T10Y3M = +0.94 y P = 0.105.
- **No se modificaron** el capítulo 04, `herramientas/tablero.py` ni `config/parametros.json`. Los textos de arriba quedan como propuesta para quien mantiene esos archivos.
