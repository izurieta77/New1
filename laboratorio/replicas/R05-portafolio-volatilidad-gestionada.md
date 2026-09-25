# Réplica R05: portafolios con volatilidad gestionada (Moreira y Muir, 2017) frente a la crítica de Cederburg, O'Doherty, Wang y Yan (2020)

> Fase 0: formación. Esta ficha no recomienda inversiones. Las secciones 1 a 9 son el pre-registro. Se escribieron el 2026-09-25, antes de calcular cualquier varianza realizada, rendimiento, alfa o Sharpe con datos, y no se editan después. Cualquier cambio posterior va a "Desviaciones del pre-registro", con fecha.

| Campo | Valor |
|---|---|
| ID | `R05` (registro: `laboratorio/replicas/R05-variantes.csv`; script: `laboratorio/replicas/R05.py`) |
| Artículo replicado | Moreira, A. y Muir, T. (2017). "Volatility-Managed Portfolios". *The Journal of Finance* 72(4), 1611–1644, agosto de 2017. doi:10.1111/jofi.12513. Ficha verificada con WebSearch el 2026-09-25 (Wiley Online Library, IDEAS/RePEc: v72y2017i4p1611-1644, NBER w22208, SSRN 2659431) |
| Artículo de contraste | Cederburg, S., O'Doherty, M. S., Wang, F. y Yan, X. S. (2020). "On the performance of volatility-managed portfolios". *Journal of Financial Economics* 138(1), 95–117 (número de octubre de 2020; en línea el 1 de mayo de 2020). Recibido el 19-nov-2018. Verificado en el PDF publicado |
| Acceso al texto | **MM:** se leyó con `pypdf` la versión NBER Working Paper 22208 (abril de 2016), 57 páginas. **El PDF del JF no se pudo leer** (Wiley, de pago). Las cifras de abajo son de la versión NBER; Cederburg et al. citan la versión JF (p. 1618) con la misma frase sobre el mercado, pero no se comprobó que las tablas del JF sean idénticas. **Cederburg et al.:** se leyó con `pypdf` el PDF del artículo publicado en el JFE (23 páginas), alojado en la página de X. Yan en Lehigh (`lehigh.edu/~xuy219/research/COWY.pdf`). Las páginas de SSRN (3357038) y Alpha Architect respondieron 403 |
| Fecha de publicación | MM: NBER WP 22208, abril de 2016 (primera versión pública verificada; SSRN 2659431 existe, pero su fecha no se pudo verificar). JF: número de agosto de 2017. Cederburg et al.: JFE, en línea el 2020-05-01 |
| Pre-registro escrito el | 2026-09-25, antes de cualquier corrida con datos |
| Responsable | Claude (laboratorio del sistema). Revisión independiente pendiente (`auditor-de-replicas`) |
| Estado | **Replicado** en el periodo del artículo (H1 y H3 dentro de la tolerancia pre-registrada). **Fuera de muestra, negativo**: H2 y H4 refutadas. No es candidata para dinero (secciones 16 y 17) |

**Conocimiento previo declarado.** Este pre-registro no es ciego. Antes de escribirlo ya conocía:

1. Las cifras de MM y de Cederburg et al. que se transcriben en la sección 1.
2. La regla 10 de `conocimiento/02-maestria-portafolio-y-asset-pricing.md` §6.1: "Vol-targeting como freno, no como fuente de alfa [...] ningún backtest puede atribuirle alfa (Cederburg et al.)". También la línea de §5.3: "Grado C como alfa y útil como control de riesgo".
3. Un resultado relacionado de R02: la referencia `A_ref_largo_vt40` (mercado de EUA siempre largo, peso 0.40/σ, tope 10) tuvo Sharpe 0.4395 dentro de muestra (1927-2011) y 0.8349 fuera de muestra (2012-01 a 2026-07), contra 0.9282 de comprar y mantener en 2012-2026. Esa regla usa otra σ y otro objetivo, pero apunta a que escalar por volatilidad no le ganó al mercado en 2012-2026.
4. Los rangos de los archivos de French en caché (README del laboratorio §7): diarios de 1926-07-01 a 2026-07-31 y mensuales de 1926-07 a 2026-07, ambos CRSP 202607. No se ha calculado ninguna varianza realizada ni ningún rendimiento con ellos para esta réplica.

---

## PRE-REGISTRO (secciones 1 a 9; no se editan después de la primera corrida)

### 1. Hipótesis previa y mecanismo

**Resultado declarado en el artículo (MM, NBER WP 22208, cifras textuales).**

- **Regla.** f^σ_{t+1} = (c / σ̂²_t(f)) · f_{t+1}, con σ̂²_t(f) = RV²_t(f) = Σ_{d=1/22}^{1} ( f_{t+d} − Σ_{d} f_{t+d}/22 )² (ec. 2, p. 6): la suma de desviaciones cuadradas de los rendimientos diarios en exceso del mes previo respecto a su media del mes. "We choose c so that the managed portfolio has the same unconditional standard deviation as the buy-and-hold portfolio" (p. 6). Nota 5: "c has no effect on our strategy's Sharpe ratio, thus the fact that we use the full sample to compute c does not impact our results". Rebalanceo mensual.
- **Prueba.** Regresión de series de tiempo f^σ_{t+1} = α + β f_{t+1} + ε_{t+1} (ec. 3). Errores estándar "adjust for heteroscedasticity"; cifras anualizadas ×12 en % (tabla 1).
- **Tabla 1, panel A, columna Mkt^σ (1926-2015):** β = **0.61** (0.05); α = **4.86** (1.56) % anual; N = **1,065**; R² = **0.37**; rmse = **51.39**. Panel B (controlando por FF3): α = 5.45 (1.56).
- **Tabla 2, columna Mkt:** Sharpe original **0.42**; appraisal ratio **0.33**. El texto dice 0.34 (p. 8) y la introducción "alpha of 4.9%, an Appraisal ratio of 0.33, and an overall 25% increase in the buy-and-hold Sharpe ratio" (p. 1).
- **Tabla 5, panel A (mercado):**

| w_t | α (e.e.) | Sharpe | Appraisal | P50 | P75 | P90 | P99 |
|---|---|---|---|---|---|---|---|
| 1/RV² (varianza realizada) | 4.86 (1.56) | 0.52 | 0.34 | 0.93 | 1.59 | 2.64 | 6.39 |
| 1/RV (volatilidad realizada) | 3.30 (1.02) | 0.53 | 0.33 | 1.23 | 1.61 | 2.08 | 3.36 |
| 1/E[RV²] (AR(1)) | 3.85 (1.36) | 0.51 | 0.30 | 1.11 | 1.71 | 2.38 | 4.58 |
| min(c/RV², 1) sin apalancamiento | 2.12 (0.71) | 0.52 | 0.30 | 0.93 | 1 | 1 | 1 |
| min(c/RV², 1.5) | 3.10 (0.98) | 0.53 | 0.33 | 0.93 | 1.5 | 1.5 | 1.5 |

- **Tabla 4 (costos, mercado):** |Δw| mensual y α antes y después de costos de 1, 10 y 14 pb: 1/RV² 0.73, α 4.86% → 4.77/3.98/3.63%, punto de equilibrio 56 pb. 1/RV 0.38, α 3.85% → 3.80/3.39/3.21%, 84 pb. Sin apalancamiento 0.16, α 2.12% → 1.93% con 10 pb, 110 pb. Tope 1.5: 0.16, α 3.10% → 2.91% con 10 pb, 161 pb. **Inconsistencia interna de la versión NBER:** la tabla 4 da α = 3.85% para "Realized Vol" y 3.30% para "Expected Variance", y la tabla 5 los da al revés (3.30% y 3.85%). Se registra; la comparación usa la tabla 5.

**Resultado del artículo de contraste (Cederburg et al., JFE 2020, cifras textuales).**

- Muestra: agosto de 1926 a diciembre de 2016 para MKT. Varianza realizada **sin desmediar y reescalada a 22 días**: σ̂²_t = (22/J_t) Σ_j (f^j_t)² (ec. 4). c* con la muestra completa.
- **Tabla 1 (comparación directa, MKT):** original: media 7.80, desviación 18.61, Sharpe **0.42**. Gestionada: media 9.55, Sharpe **0.51**. Diferencia **0.09**, p = [0.30] (Jobson-Korkie con corrección de Memmel). Correlación 0.63. Pesos c*/σ̂²: P01 0.04, P50 0.96, P99 6.47.
- **Tabla 3 (regresión de expansión, MKT):** α = **4.63%** (t White = 3.08); β = 0.63; R² = 0.40; AR = 0.32; c* = 10.33; combinación ex post óptima con γ = 5: 72% en la gestionada y 28% en la original; Sharpe **0.53 contra 0.42**; CER 2.79% contra 1.76%.
- **Tabla 5 (combinación en tiempo real, MKT):** entrenamiento inicial K = 120 meses, ventana expansiva, γ = 5, |y_t| ≤ 5. En cada mes t: c_t iguala la varianza de la gestionada y la original en el entrenamiento; [x_σ,t, x_t]' = (1/γ) Σ̂_t⁻¹ μ̂_t; y_t = x_σ,t · c_t/σ̂²_{t−1} + x_t; rendimiento y_t·f_t (ecs. 15-16). Resultado: **[S1] combinación en tiempo real, Sharpe 0.42; [S2] original en tiempo real, 0.46; diferencia −0.04 [p = 0.64]**. CER 1.56% contra 1.75% (−0.19 [0.83]). [S3] combinación ex post óptima en el periodo fuera de muestra: 0.53. Explicación de los autores (p. 107-108): el buen desempeño del MKT gestionado dentro de muestra "is concentrated in the period surrounding the Great Depression", y el MKT gestionado "underperforms the original MKT factor after the first ten years of the sample".
- Conclusión general: en 103 estrategias, las versiones fuera de muestra "generally earn lower certainty equivalent returns and Sharpe ratios than do simple investments in the original, unmanaged portfolios" (resumen).

**Mecanismo económico (MM).** La varianza es muy persistente y predecible a un mes, pero predice poco los rendimientos. Por eso la razón μ_t/σ²_t empeora cuando la volatilidad sube, y un inversionista media-varianza debería reducir exposición en esos meses. ¿Por qué no se arbitra? Porque exige apalancamiento en meses tranquilos (limitado para muchos inversionistas), contradice la idea de comprar en las caídas y los meses de alta volatilidad coinciden con crisis en las que los modelos de riesgo predicen primas mayores (inferencia, no hecho). **Mecanismo de la crítica (Cederburg et al.).** Un α > 0 en la regresión de expansión solo dice que la combinación ex post óptima de gestionada y original expande la frontera. Esos pesos no se conocen en tiempo real, y la relación riesgo-rendimiento del mercado es inestable: el α del mercado se concentra en la Gran Depresión.

**Hipótesis (signo y magnitud esperados, antes de ver datos):**

- **H1, réplica estadística de MM** (1926-08 a 2015-12, c con la muestra completa, sin tope, RV de MM). α > 0 con t (White/HC0) ≥ 2, dentro de 4.86 ± 1.56 pp (un error estándar del artículo), β cerca de 0.61 y Sharpe de la gestionada 0.52 ± 0.05. Secundarias (tabla 5): 1/RV con α en 3.30 ± 1.02; tope 1 en 2.12 ± 0.71; tope 1.5 en 3.10 ± 0.98.
- **H2, MM después de publicarse** (2017-08 a 2026-07, con la c fijada en 1926-08 a 2015-12). Expectativa previa: α > 0 pero **no significativo** (t < 2), por tener solo ~108 meses. Se reporta la diferencia de Sharpe gestionada − mercado con su p de Jobson-Korkie.
- **H3, crítica de Cederburg et al. para el mercado** (combinación en tiempo real, K = 120, γ = 5, |y| ≤ 5, RV de Cederburg; OOS 1936-08 a 2016-12). Sharpe [S1] − [S2] < 0, con S1 dentro de 0.42 ± 0.05 y S2 dentro de 0.46 ± 0.05. Después se extiende a 2026-07 y al tramo 2017-08 a 2026-07.
- **H4, versión operable** (motor `herramientas/backtest.py`, solo largos, tope de exposición 1/1.5/2, c estimada en tiempo real, costos GBM). Expectativa previa: la variante sin apalancamiento (`var_c1`) **reduce la caída máxima** frente a comprar y mantener y tiene un Sharpe neto parecido (±0.10); **no** tiene DSR ≥ 0.95 frente a su propio Sharpe cero ni un α contra el mercado con t ≥ 3.

### 2. Criterio de refutación

**Métricas principales:**

- H1 y H2: α anual (%) de la regresión de expansión y su t HC0. Como robustez: t de Newey-West con 12 rezagos y t HC1.
- H3: Sharpe anual (media/desviación × √12 del exceso) de S1 y S2, más el p de Jobson-Korkie-Memmel de su diferencia.
- H4: Sharpe neto del exceso sobre RF, caída máxima (MDD) de la curva neta, α anual contra el mercado (regresión del exceso neto de la estrategia sobre Mkt-RF) con t HC0 y NW(12), y DSR del registro.

**Criterios:**

- **H1 "Replicado":** α con el mismo signo, t HC0 ≥ 2 y dentro de [3.30, 6.42] %. **Replicado con diferencias:** mismo signo y t ≥ 2, pero fuera de la tolerancia. **No replicado (refuta):** α ≤ 0 o t HC0 < 2 en 1926-08 a 2015-12.
- **H2:** "se sostiene después de publicarse" si α > 0 **y** Sharpe de la gestionada > Sharpe del mercado en 2017-08 a 2026-07. "Significativo" solo con t HC0 ≥ 2. Se refuta si α ≤ 0 o Sharpe de la gestionada ≤ Sharpe del mercado.
- **H3 (crítica replicada):** S1 − S2 < 0 en 1936-08 a 2016-12, con S1 y S2 dentro de ±0.05 de 0.42 y 0.46. Si solo coincide el signo, "Replicado con diferencias". **La crítica se refuta para el mercado** si S1 − S2 > 0 con p de Jobson-Korkie < 0.10.
- **H4 (operable):** para la variante que tenga el mayor Sharpe neto **dentro de muestra** (1936-08 a 2015-12) entre las 7 de prueba:
  - "Agrega valor frente a comprar y mantener" solo si **fuera de muestra** (2017-08 a 2026-07) tiene Sharpe neto > comprar y mantener **y** una MDD menor en valor absoluto.
  - "Agrega valor frente a la regla sencilla" solo si además supera a la SMA10 en Sharpe **y** en MDD fuera de muestra.
  - Para hablar de "alfa" hace falta además t ≥ 3 en el α contra el mercado (regla 5 del cap. 02, HLZ 2016) y DSR ≥ 0.95 (`validacion_estrategias.deflated_sharpe_min_probabilidad`).
  - **Se refuta H4** si el Sharpe neto fuera de muestra es ≤ el de comprar y mantener. Por separado, **se refuta el uso como freno** si la MDD fuera de muestra **y** la MDD de 1936-08 a 2015-12 no son menores que las de comprar y mantener.

### 3. Datos y licencia

| Serie | Fuente y archivo | Versión / huella | Frecuencia | Condiciones de uso |
|---|---|---|---|---|
| Mkt-RF y RF diarios | French `F-F_Research_Data_Factors_daily` | `version_crsp` y `sha256` que imprime el script (se espera CRSP 202607) | diaria | Pendiente de verificar (README §7) |
| Mkt-RF y RF mensuales | French `F-F_Research_Data_Factors` | ídem | mensual | Pendiente de verificar |
| MXN por USD | FRED `DEXMXUS` | fecha de descarga | diaria (se toma el último dato ≤ fin de mes en el motor) | Pendiente de verificar |

El script imprime las notas de encabezado de ambos archivos de French (formato vigente desde 2025: preámbulo con versión CRSP y nota de la T-bill) y verifica que el mensual y el diario tengan la misma versión CRSP. Si no coinciden, se detiene.

### 4. Universo

Un solo activo de riesgo: el mercado total de EUA de French (CRSP, ponderado por valor, con dividendos). Rendimiento total mensual = Mkt-RF + RF; efectivo = RF (T-bill a un mes: Ibbotson hasta 202405 e ICE BofA desde 202406). CRSP no tiene sesgo de supervivencia, pero el índice **no es invertible directamente**. El proxy operable sería un ETF del S&P 500 en el SIC (no probado aquí). Para medir el riesgo, un inversionista real calcularía la varianza con el índice (p. ej. ^GSPC diario), no con French. Se declara como diferencia.

### 5. Fecha de disponibilidad

- RV²_{t−1} se calcula con los rendimientos diarios del mes t−1. Se conoce al cierre del último día hábil de t−1 y se fecha en el fin de mes calendario de t−1, que es la misma fecha del dato mensual t−1.
- En el motor, la señal del mes t recibe `extras['rv2']` y `extras['rv']` con fecha ≤ fecha_{t−1}, más los rendimientos mensuales hasta t−1 (garantía estructural del motor). c_t y los pesos de la combinación se estiman solo con meses ≤ t−1.
- En H1 y H2 (réplica estadística), c usa toda la muestra de la regresión. **Es look-ahead a propósito:** es la estadística del artículo, no una estrategia. Se reporta como tal y no entra al registro del motor.
- French publica con rezago y CRSP revisa datos: la versión 202607 no es exactamente lo que se conocía en cada fecha. Se declara; no se corrige.

### 6. Periodo

- **Periodo de MM:** 1926-2015 (N = 1,065 en su tabla 1). Aquí: 1926-08 a 2015-12. Es el primer mes con RV del mes previo, porque los diarios empiezan el 1926-07-01. Resultan 1,073 meses; la diferencia de 8 meses con el artículo no está explicada de antemano.
- **Periodo de Cederburg et al.:** 1926-08 a 2016-12, con fuera de muestra desde 1936-08 (K = 120).
- **Periodo propio total:** 1926-07 a 2026-07 (último mes de French CRSP 202607).
- **Cortes del motor (H3 extendida y H4):** 2015-12-31 (fin de la muestra de MM) y 2017-07-31 (mes previo al número del JF de agosto de 2017). Segmentos: `dentro_muestra` 1936-08 a 2015-12, `hueco_2016_2017` 2016-01 a 2017-07 y `fuera_muestra` 2017-08 a 2026-07. La primera decisión es para 1936-08, con min_historia = 121 meses visibles (1926-07 a 1936-07), para que el entrenamiento de c_t tenga 120 meses, como en Cederburg et al. Nota: la versión NBER circula desde abril de 2016, así que el "hueco" ya es posterior a la primera versión pública.
- **Subperiodos de sensibilidad (H1, c de la muestra completa de cada ventana):** 1926-08 a 1955-12, 1956-01 a 1985-12, 1986-01 a 2015-12, 2016-01 a 2026-07 y 1926-08 a 2026-07.

### 7. Limpieza

- Los faltantes de French (−99.99 / −999) se omiten. La API los devuelve como `None`.
- Un mes necesita J_t ≥ 15 días con dato para calcular RV. Si algún mes no cumple, **el script se detiene y lo reporta**; no se imputa.
- Si algún RV² es 0, el script se detiene.
- No se winsoriza ni se elimina ninguna observación extrema: los meses de 1929-1932, 1987 y 2008 son el corazón del efecto.
- Se exige que las fechas mensuales de rendimientos y de RV coincidan. El último mes con RV debe ser el último mes con rendimiento.

### 8. Regla y variantes planeadas

**Definiciones (d_j = Mkt-RF diario del mes; f_t = Mkt-RF mensual del archivo mensual):**

- RV²_MM(t) = Σ_{j=1}^{J_t} (d_j − d̄_t)², sobre los J_t días reales del mes. Es la ec. 2 de MM con los días efectivos en lugar de 22.
- RV²_COWY(t) = (22/J_t) Σ_{j=1}^{J_t} d_j². Es la ec. 4 de Cederburg et al.
- RV(t) = √RV²(t).

**Parte A: réplica estadística de MM (H1, H2; no es estrategia, no entra al CSV).**

- f^σ_t = (c/RV²_MM(t−1)) f_t, con c tal que sd(f^σ) = sd(f) en la ventana de la regresión (desviación muestral n−1).
- MCO f^σ = α + β f + ε: α anual = 12 × α mensual (%); errores MCO, HC0, HC1 y NW(12); R²; rmse anual = 12 × σ_ε (%); AR = α/rmse × √12; Sharpe anual de f y de f^σ; percentiles P50/P75/P90/P99 de c/RV²; p de Jobson-Korkie-Memmel de la diferencia de Sharpe (comparación directa, como la tabla 1 de Cederburg).
- Variantes de la tabla 5 de MM con la c de la muestra completa: A1 1/RV², A2 1/RV, A3 min(c/RV², 1) y A4 min(c/RV², 1.5). En A3 y A4 se usa la c sin tope, como en MM.
- Sensibilidad A1 con RV²_COWY (comparable con la tabla 3 de Cederburg: α 4.63, t 3.08, en 1926-08 a 2016-12).
- H2: A1 con c fija de 1926-08 a 2015-12, evaluada en 2017-08 a 2026-07 (y en 2016-01 a 2026-07).

**Parte B: combinación en tiempo real de Cederburg et al. (H3), implementada como señal del motor.**

- En cada mes t, con los meses de entrenamiento s ≤ t−1 que tienen f_s y RV²(s−1) (el primero es 1926-08):
  - g_s = f_s / RV²_COWY(s−1).
  - μ̂ y Σ̂ (n−1) de (g_s, f_s).
  - [x_σ, x]' = (1/γ) Σ̂⁻¹ μ̂ con γ = 5.
  - y_t = clip(x_σ / RV²_COWY(t−1) + x, −5, 5).
- c_t no hace falta: y_t es invariante a c_t, porque x_σ escala con 1/c_t. **S2:** z_t = clip((1/γ) μ̂_f / σ̂²_f, −5, 5).
- Corren en el motor con exposicion_min = −5 y exposicion_max = 5. Los dos corren con costos cero, `es_prueba=False` y la nota "contraste Cederburg"; S1 corre además con costos por defecto, también `es_prueba=False`.
- S3 (ex post) = √(μ' Σ⁻¹ μ) × √12 con los momentos de (f^σ, f) del mismo tramo fuera de muestra, sin restricción de apalancamiento.
- Sensibilidad: S1 con RV²_MM.
- Las cifras de Sharpe de S1/S2 se calculan sobre r_neto − r_efectivo del motor y se recortan a la ventana 1936-08 a 2016-12 para comparar con el artículo.

**Parte C: versión operable (H4), en el motor, registrada. Lista cerrada de variantes de prueba (`es_prueba=True`, costos por defecto, USD):**

| # | variante | exposición al mercado en t (resto en RF) |
|---|---|---|
| 1 | `var_c1` | min(1, c_t / RV²_MM(t−1)) |
| 2 | `var_c1.5` | min(1.5, c_t / RV²_MM(t−1)) |
| 3 | `var_c2` | min(2, c_t / RV²_MM(t−1)) |
| 4 | `vol_c1` | min(1, k_t / RV_MM(t−1)) |
| 5 | `vol_c1.5` | min(1.5, k_t / RV_MM(t−1)) |
| 6 | `vol_c2` | min(2, k_t / RV_MM(t−1)) |
| 7 | `var_c1_rvCOWY` | min(1, c_t / RV²_COWY(t−1)) |

- c_t = sd(f_s) / sd(f_s / RV²(s−1)) y k_t = sd(f_s) / sd(f_s / RV(s−1)), con todos los s ≤ t−1 disponibles (ventana expansiva, primer s = 1926-08, al menos 120). Es el c_t de Cederburg et al.: iguala la volatilidad de la gestionada **sin tope** y la del mercado en el entrenamiento. El tope se aplica después.
- Exposición mínima 0 (sin cortos). Exposición inicial 0: todas las reglas pagan la entrada. Efectivo = RF de French. El apalancamiento se financia a RF (supuesto del motor).
- Reglas sencillas con idénticas condiciones (`es_prueba=False`): `comprar_y_mantener`, `efectivo` y `sma10` (`senal_media_movil(10)`). Mismas fechas, min_historia = 121 y cortes.
- **Selección:** la variante con mayor Sharpe neto en `dentro_muestra`, que es la que `sharpe_deflactado_de_registro` elige por defecto.

**Sensibilidades (`es_prueba=False`, con nota):**

1. Costos: las variantes 1-7, comprar y mantener y la SMA10 con spread "medio" (0.15%) y "bruto" (0 comisión y 0 spread).
2. MXN: `var_c1`, `vol_c1`, `comprar_y_mantener` y `sma10` con fx = DEXMXUS (efectivo RF en USD convertido), costos por defecto. Empieza cuando hay FX (1993-11).
3. Costo del apalancamiento (fuera del motor, **no registrado en el CSV** porque no es una corrida nueva): a las variantes con tope 1.5 y 2 se les resta max(w−1, 0) × 3%/12 al mes. El 3% anual sobre RF es un **supuesto** (GBM no publica esa tasa en el documento de costos). Se reporta el Sharpe y el CAGR ajustados.

**Qué no se prueba (desviación si se hace):** AR(1) de la varianza esperada, ventanas de RV distintas de un mes, otros factores (SMB, HML, Mom...), γ distinto de 5, K distinto de 120, rebalanceo por bandas.

### 9. Costos y comparación simple

- Costos: comisión 0.29% por lado (GBM, hecho) + spread 0.05% por lado (supuesto) y escenario "medio" de 0.15% y "bruto". El costo por periodo del motor es |w_t − w_pre_t| × (comisión + spread). No hay spread cambiario, costo de margen (solo la sensibilidad 3 de la sección 8), préstamo de títulos, venta final ni impuestos.
- Nota de contexto: `config/parametros.json` fija `apalancamiento.bruto_max_fase_1` = 1.0 y la regla 18.3 del cap. 18 prohíbe el margen. **Las variantes con tope 1.5 y 2 no son operables en el sistema** en fase 1; se corren solo para compararlas con el artículo.
- Reglas sencillas con idénticas condiciones: comprar y mantener, 100% efectivo y SMA10.
- Registro de corridas: `N` de prueba = 7 (`es_prueba=True`). N conservador = 13 = 7 + 4 variantes estadísticas de la parte A (A1-A4) + 2 de la parte B (S1 y S1 con RV de MM). Se reporta el DSR con ambos.

---

## RESULTADOS (se llenan después de correr)

> Corrida final: `python3 laboratorio/replicas/R05.py`, el 2026-09-25 (registro de 06:09 a 06:10 UTC, unos 40 s). La salida completa está en `R05-salida.txt`, las cifras clave en `R05-resultados.json` y la verificación sin el motor en `R05_verificacion.py`. Las tablas de esta sección se copiaron por script de esas salidas, sin redondear a mano.

### Desviaciones del pre-registro

| Fecha | Qué cambió | Por qué | ¿Invalida el tramo de prueba? |
|---|---|---|---|
| 2026-09-25 | **Falló la primera corrida.** `R05.py` se detuvo en una función de reporte: `ols2` dividió entre cero al calcular R² y Jobson-Korkie para la regla `efectivo`, cuyo exceso es idénticamente 0. Para entonces ya había registrado 10 corridas (las 7 de prueba y las 3 reglas sencillas; 40 filas). Se agregaron guardas en `ols2`, `alfa_contra_mercado`, `tabla_motor` y `resumen`. No cambió ninguna regla, parámetro, dato ni ventana. La corrida final volvió a registrar esas 10 configuraciones con la misma `huella_datos` (e85ac74d630dff95) y el mismo `parametros_json`. Por eso el CSV tiene 47 corridas y 188 filas; el DSR cuenta cada variante una sola vez (N = 7) | Error de programación en el reporte | No. Antes de la corrección ya se habían impreso y visto los resultados de la parte A (H1, H2 y subperiodos). Después de verlos no se modificó nada del pre-registro |
| 2026-09-25 | Se agregaron filas estadísticas que no estaban en la lista: A1 con la RV de Cederburg en la ventana de MM, A1 con la RV de MM en 1926-08 a 2016-12, y A2, A3 y A4 después del JF (H2). Son las mismas reglas de la parte A en otras ventanas | Comparar cada definición de RV contra cada artículo y completar H2 | No: son descriptivas y no se usan para seleccionar |
| 2026-09-25 | También se corrió S2 con costos por defecto. El pre-registro solo listaba S1 con costos | Comparar S1 y S2 netos en las mismas condiciones | No (`es_prueba=False`) |
| 2026-09-25 | Se agregó `R05_verificacion.py`. Recalcula sin el motor las 9 series operables y reporta las fechas de pico y valle de la caída máxima | Tener una segunda implementación y las fechas que el CSV no guarda | No: no registra corridas |

### 10. Variantes probadas

- Archivo: `replicas/R05-variantes.csv`, con 188 filas y 47 corridas. Cada corrida tiene 4 segmentos: `completo`, `dentro_muestra`, `hueco_2016_2017` y `fuera_muestra`.
- Variantes con `es_prueba=1`: **7** (`var_c1`, `var_c1.5`, `var_c2`, `vol_c1`, `vol_c1.5`, `vol_c2` y `var_c1_rvCOWY`). Cada una quedó registrada 2 veces con una configuración idéntica (ver las desviaciones).
- Corridas con `es_prueba=0` en la corrida final: 30. Son 3 reglas sencillas, 18 de costos, 4 en MXN y 5 de Cederburg.
- Pruebas fuera del registro: las de la parte A (A1-A4 y sus filas de verificación). Son la estadística del artículo, con c de toda la muestra. No hubo pruebas en otra sesión. El N conservador pre-registrado es 13.
- Salida de `sharpe_deflactado_de_registro`:

| Lectura | segmento | variante | DSR | cumple 0.95 | N | V (SR periodo) | SR anual | SR0 anual | n | PSR sin deflactar |
|---|---|---|---|---|---|---|---|---|---|---|
| dentro_N_registrado | dentro_muestra | vol_c1 | 0.9999 | True | 7 | 0.000093 | 0.4914 | 0.0464 | 953 | 1.0000 |
| dentro_N_conservador | dentro_muestra | vol_c1 | 0.9999 | True | 13 | 0.000093 | 0.4914 | 0.0570 | 953 | 1.0000 |
| fuera_N_registrado | fuera_muestra | vol_c1 | 0.9325 | False | 7 | 0.001490 | 0.7130 | 0.1854 | 108 | 0.9783 |
| fuera_N_conservador | fuera_muestra | vol_c1 | 0.9154 | False | 13 | 0.001490 | 0.7130 | 0.2277 | 108 | 0.9783 |

- **Cómo leerlo.** La variante elegida dentro de muestra es `vol_c1`, con Sharpe neto de 0.4914. Su DSR dentro de muestra es 0.9999 con N = 7 o con N = 13. Pero **el DSR se mide contra un Sharpe de cero, no contra comprar y mantener**, que tiene Sharpe 0.4820 en el mismo tramo. Fuera de muestra el DSR es 0.9325 (N = 7) y 0.9154 (N = 13): no llega a 0.95.

### 11. Resultados

#### 11.1 Periodo del artículo (parte A: estadística de MM, con c de toda la ventana; no es una estrategia)

| Caso | Ventana | N | α %/año (e.e. HC0) | t HC0 / t NW12 | β | R² | rmse | AR | SR mercado | SR gestionada | ΔSR [p JK] | P50/P75/P90/P99 de w | frac. en tope |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1_var | 1926-08 a 2015-12 | 1073 | 4.88 (1.56) | 3.13 / 2.78 | 0.601 | 0.362 | 51.68 | 0.327 | 0.415 | 0.511 | 0.096 [0.31] | 0.94/1.62/2.71/7.27 | 0.000 |
| A2_vol | 1926-08 a 2015-12 | 1073 | 3.38 (1.02) | 3.32 / 2.88 | 0.844 | 0.712 | 34.72 | 0.338 | 0.415 | 0.532 | 0.116 [0.05] | 1.24/1.64/2.12/3.47 | 0.000 |
| A3_var_tope1 | 1926-08 a 2015-12 | 1073 | 2.05 (0.71) | 2.86 / 2.46 | 0.440 | 0.589 | 23.79 | 0.298 | 0.415 | 0.510 | 0.094 [0.19] | 0.94/1.00/1.00/1.00 | 0.468 |
| A4_var_tope1.5 | 1926-08 a 2015-12 | 1073 | 3.11 (0.95) | 3.26 / 2.77 | 0.511 | 0.519 | 31.82 | 0.338 | 0.415 | 0.534 | 0.119 [0.14] | 0.94/1.50/1.50/1.50 | 0.275 |
| A1_var_rvCOWY_MMventana | 1926-08 a 2015-12 | 1073 | 4.56 (1.51) | 3.01 / 2.62 | 0.630 | 0.397 | 50.22 | 0.314 | 0.415 | 0.506 | 0.091 [0.32] | 0.96/1.59/2.65/6.07 | 0.000 |
| A1_var_rvCOWY_1926_2016 | 1926-08 a 2016-12 | 1085 | 4.61 (1.50) | 3.07 / 2.67 | 0.631 | 0.398 | 50.03 | 0.319 | 0.420 | 0.513 | 0.092 [0.31] | 0.96/1.59/2.65/6.00 | 0.000 |
| A1_var_rvMM_1926_2016 | 1926-08 a 2016-12 | 1085 | 4.93 (1.54) | 3.20 / 2.83 | 0.602 | 0.362 | 51.48 | 0.332 | 0.420 | 0.518 | 0.098 [0.30] | 0.93/1.62/2.71/7.26 | 0.000 |

Comparación con las cifras de los artículos (salida del script):

Cifras de MM (tabla 1 y 5, NBER WP 22208) para comparar:
- A1_var: α artículo 4.86 (1.56) vs réplica 4.88 (1.56); diferencia 0.02 pp; dentro de ±1 e.e.: True; t HC0 3.13; Sharpe gestionada artículo 0.52 vs 0.511; AR 0.34 vs 0.327
- A2_vol: α artículo 3.3 (1.02) vs réplica 3.38 (1.02); diferencia 0.08 pp; dentro de ±1 e.e.: True; t HC0 3.32; Sharpe gestionada artículo 0.53 vs 0.532; AR 0.33 vs 0.338
- A3_var_tope1: α artículo 2.12 (0.71) vs réplica 2.05 (0.71); diferencia -0.07 pp; dentro de ±1 e.e.: True; t HC0 2.86; Sharpe gestionada artículo 0.52 vs 0.510; AR 0.3 vs 0.298
- A4_var_tope1.5: α artículo 3.1 (0.98) vs réplica 3.11 (0.95); diferencia 0.01 pp; dentro de ±1 e.e.: True; t HC0 3.26; Sharpe gestionada artículo 0.53 vs 0.534; AR 0.33 vs 0.338
- A1: β 0.61 vs 0.601; N 1065 vs 1073; R² 0.37 vs 0.362; rmse 51.39 vs 51.68; SR mercado 0.42 vs 0.415
- Cederburg tabla 3 (RV COWY, 1926-08 a 2016-12): α 4.63 (t 3.08) vs 4.61 (t HC0 3.07); β 0.63 vs 0.631; R² 0.4 vs 0.398; AR 0.32 vs 0.319; c* 10.33 vs c×10⁴ 10.31
- Cederburg tabla 1 (comparación directa): SR 0.42 vs 0.420; SR gestionada 0.51 vs 0.513; ΔSR 0.09 [p 0.3] vs 0.092 [p 0.31]; pesos P01/P50/P99 0.04/0.96/6.47 vs 0.04/0.96/6.00; media gestionada 9.53 vs 9.55; media mercado 7.81 vs 7.80; sd 18.60 vs 18.61; corr 0.631 vs 0.63

**Cómo leerlo (hechos).**

- **α de MM reproducido.** En 1926-08 a 2015-12 el α de 1/RV² es 4.88% anual (e.e. HC0 de 1.56; t HC0 3.13; t NW12 2.78). El artículo da 4.86 (1.56): diferencia de +0.02 pp.
- **Otras cifras de la tabla 1 de MM.** β = 0.601 contra 0.61; R² 0.362 contra 0.37; rmse 51.68 contra 51.39. El appraisal ratio es 0.327, contra 0.33 en la tabla 2 y 0.34 en el texto.
- **Variantes de la tabla 5.** Las tres caen dentro de ±1 e.e. del artículo: 1/RV 3.38 contra 3.30; tope 1 2.05 contra 2.12; tope 1.5 3.11 contra 3.10.
- **Percentiles de los pesos.** Salen 0.94/1.62/2.71/7.27, contra 0.93/1.59/2.64/6.39 en el artículo. La cola alta es mayor aquí.
- **Tablas 1 y 3 de Cederburg.** Con su RV y su ventana (1926-08 a 2016-12) salen: α 4.61 (t 3.07) contra 4.63 (3.08); c×10⁴ de 10.31 contra 10.33; ΔSR directo de 0.092 [p 0.31] contra 0.09 [0.30].
- **La comparación directa no es significativa ni dentro de muestra.** A igual volatilidad, la gestionada con 1/RV² tiene Sharpe 0.511 contra 0.415 del mercado (p 0.31). Con 1/RV sale 0.532 contra 0.415 (p 0.05). Es la distinción de Cederburg et al.: un α significativo en la regresión de expansión no es lo mismo que un Sharpe significativamente mayor.

#### 11.2 Después de publicarse (H2: c fija de 1926-08 a 2015-12)

| Caso | Ventana | N | α %/año (e.e. HC0) | t HC0 / t NW12 | β | R² | rmse | AR | SR mercado | SR gestionada | ΔSR [p JK] | P50/P75/P90/P99 de w | frac. en tope |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1_post_JF_2017-08 | 2017-08 a 2026-07 | 108 | -0.75 (5.11) | -0.15 / -0.14 | 0.587 | 0.356 | 45.83 | -0.056 | 0.758 | 0.407 | -0.352 [0.25] | 0.64/1.19/2.06/3.61 | 0.000 |
| A1_post_NBER_2016-01 | 2016-01 a 2026-07 | 127 | 1.48 (4.55) | 0.32 / 0.28 | 0.597 | 0.357 | 43.88 | 0.117 | 0.825 | 0.587 | -0.238 [0.40] | 0.67/1.35/2.24/3.79 | 0.000 |
| A2_vol_post_JF_2017-08 | 2017-08 a 2026-07 | 108 | -0.30 (3.12) | -0.10 / -0.10 | 0.846 | 0.729 | 29.88 | -0.035 | 0.758 | 0.629 | -0.129 [0.48] | 1.03/1.41/1.84/2.44 | 0.000 |
| A3_tope1_post_JF_2017-08 | 2017-08 a 2026-07 | 108 | 0.34 (1.89) | 0.18 / 0.22 | 0.420 | 0.632 | 18.61 | 0.064 | 0.758 | 0.642 | -0.117 [0.59] | 0.64/1.00/1.00/1.00 | 0.315 |
| A4_tope1.5_post_JF_2017-08 | 2017-08 a 2026-07 | 108 | -0.33 (2.67) | -0.12 / -0.14 | 0.474 | 0.545 | 25.12 | -0.046 | 0.758 | 0.529 | -0.230 [0.35] | 0.64/1.19/1.50/1.50 | 0.167 |

- **Después del JF (2017-08 a 2026-07, 108 meses).** α = −0.75% anual (e.e. 5.11, t −0.15). La gestionada tiene Sharpe 0.407 contra 0.758 del mercado (ΔSR −0.352, p 0.25).
- **Desde la versión NBER (2016-01).** α = 1.48 (t 0.32); Sharpe 0.587 contra 0.825.
- **Resultado:** H2 queda **refutada** según el criterio pre-registrado (α ≤ 0 y Sharpe de la gestionada menor que el del mercado), sin significancia en ninguna dirección.

#### 11.3 Crítica de Cederburg et al.: combinación en tiempo real (H3)

Verificación: máx |y_motor − y_directo|: S1 8.88e-16, S1_rvMM 8.88e-16, S2 1.11e-16

| Ventana | n | S1 comb. tiempo real | S2 original tiempo real | S1−S2 [p JK] | CER S1 | CER S2 | S3 ex post | S1 RV MM | S1 neto GBM | S2 neto GBM | S1−S2 neto [p JK] | y medio S1 | frac. |y|=5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cederburg OOS 1936-08 a 2016-12 | 965 | 0.415 | 0.458 | -0.043 [0.62] | 1.54 | 1.76 | 0.528 | 0.436 | 0.292 | 0.454 | -0.163 [0.05] | 0.733 | 0.003 |
| dentro_muestra 1936-08 a 2015-12 | 953 | 0.407 | 0.450 | -0.042 [0.62] | 1.45 | 1.72 | 0.521 | 0.429 | 0.284 | 0.446 | -0.162 [0.06] | 0.734 | 0.003 |
| fuera_muestra 2017-08 al final | 108 | 0.577 | 0.751 | -0.174 [0.42] | 3.23 | 4.35 | 0.759 | 0.551 | 0.466 | 0.747 | -0.281 [0.19] | 0.591 | 0.000 |
| completo 1936-08 al final | 1080 | 0.439 | 0.502 | -0.063 [0.44] | 1.82 | 2.06 | 0.553 | 0.453 | 0.316 | 0.498 | -0.182 [0.02] | 0.721 | 0.003 |
| 2017-01 al final (post-Cederburg) | 115 | 0.675 | 0.792 | -0.117 [0.58] | 4.11 | 4.58 | 0.807 | 0.646 | 0.561 | 0.788 | -0.228 [0.28] | 0.620 | 0.000 |

Cederburg tabla 5 (MKT): S1 0.42, S2 0.46, dif -0.04 [p 0.64], CER S1 1.56, CER S2 1.75, S3 0.53

- **Réplica en la ventana del artículo.** En 1936-08 a 2016-12 hay 965 meses, igual que T − K en el artículo. S1 = 0.415 contra S2 = 0.458, con diferencia −0.043 [p 0.62]; el artículo da −0.04 [p 0.64]. CER: 1.54% contra 1.76% (artículo: 1.56 contra 1.75). S3 ex post: 0.528 (artículo 0.53). Con la RV de MM, S1 sale 0.436. Resultado: **H3 replicada**, dentro de ±0.05.
- **Con costos GBM la brecha crece.** S1 = 0.292 contra S2 = 0.454, con diferencia −0.163 [p 0.05]. La razón es la rotación: según el registro, S1 rota 3.913 veces al año con costo de 1.33% anual en `completo`; S2 rota 0.058 veces con 0.02%.
- **Después de 2017-08.** S1 = 0.577 contra S2 = 0.751, bruto (diferencia −0.174 [p 0.42]).

#### 11.4 Versión operable (H4) contra las reglas sencillas (USD, costos por defecto)

Nota: en la fila `comprar_y_mantener` la regresión es la identidad (y = x). Su α es 0 y los t que aparecen (±1.00; 1.56) son ruido numérico, no un resultado.

Segmento completo: 1936-07-31 (cierre base) a 2026-07-31, n=1080

| variante | CAGR | vol | Sharpe | Sortino | MDD | Calmar | expos. media | rotación/año | costo/año | α vs mercado %/año (t HC0; t NW12) | β | ΔSR vs CyM [p JK] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| var_c1 | 0.0823 | 0.1116 | 0.4605 | 0.6747 | -0.5044 | 0.1632 | 0.7718 | 1.8869 | 0.0064 | 0.04 (0.07; 0.07) | 0.621 | -0.062 [0.25] |
| var_c1.5 | 0.0886 | 0.1429 | 0.4293 | 0.6253 | -0.6902 | 0.1283 | 0.9888 | 3.5118 | 0.0119 | -0.03 (-0.03; -0.02) | 0.750 | -0.093 [0.14] |
| var_c2 | 0.0898 | 0.1683 | 0.3971 | 0.5723 | -0.7935 | 0.1131 | 1.1387 | 4.9858 | 0.0170 | -0.23 (-0.18; -0.16) | 0.840 | -0.125 [0.07] |
| vol_c1 | 0.1012 | 0.1377 | 0.5234 | 0.7747 | -0.4223 | 0.2397 | 0.9221 | 0.8160 | 0.0028 | 0.25 (0.62; 0.60) | 0.848 | 0.001 [0.97] |
| vol_c1.5 | 0.1101 | 0.1741 | 0.4941 | 0.7253 | -0.6536 | 0.1684 | 1.2065 | 2.3536 | 0.0080 | 0.11 (0.15; 0.13) | 1.034 | -0.028 [0.47] |
| vol_c2 | 0.1115 | 0.1953 | 0.4692 | 0.6824 | -0.7679 | 0.1453 | 1.3570 | 3.7468 | 0.0127 | -0.08 (-0.08; -0.07) | 1.125 | -0.053 [0.25] |
| var_c1_rvCOWY | 0.0827 | 0.1123 | 0.4622 | 0.6790 | -0.4894 | 0.1691 | 0.7720 | 1.8429 | 0.0063 | 0.05 (0.08; 0.07) | 0.626 | -0.060 [0.26] |
| comprar_y_mantener | 0.1090 | 0.1572 | 0.5222 | 0.7737 | -0.5031 | 0.2166 | 1.0000 | 0.0111 | 0.0000 | -0.00 (-1.00; -1.00) | 1.000 | — |
| sma10 | 0.0926 | 0.1158 | 0.5306 | 0.7821 | -0.4314 | 0.2147 | 0.7426 | 1.5222 | 0.0052 | 1.73 (1.91; 1.64) | 0.538 | 0.008 [0.91] |
| efectivo | 0.0346 | 0.0088 | 0.0000 | 0.0000 | -0.0009 | 38.4020 | 0.0000 | 0.0000 | 0.0000 | nan (nan; nan) | nan | — |

Segmento dentro_muestra: 1936-07-31 (cierre base) a 2015-12-31, n=953

| variante | CAGR | vol | Sharpe | Sortino | MDD | Calmar | expos. media | rotación/año | costo/año | α vs mercado %/año (t HC0; t NW12) | β | ΔSR vs CyM [p JK] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| var_c1 | 0.0828 | 0.1148 | 0.4408 | 0.6458 | -0.5044 | 0.1642 | 0.7883 | 1.7489 | 0.0059 | 0.16 (0.24; 0.22) | 0.647 | -0.041 [0.45] |
| var_c1.5 | 0.0900 | 0.1475 | 0.4185 | 0.6113 | -0.6902 | 0.1304 | 1.0155 | 3.3471 | 0.0114 | 0.21 (0.21; 0.18) | 0.787 | -0.064 [0.32] |
| var_c2 | 0.0912 | 0.1739 | 0.3881 | 0.5612 | -0.7935 | 0.1149 | 1.1743 | 4.8486 | 0.0165 | 0.04 (0.03; 0.03) | 0.884 | -0.094 [0.19] |
| vol_c1 | 0.0991 | 0.1400 | 0.4914 | 0.7245 | -0.4223 | 0.2346 | 0.9298 | 0.7500 | 0.0025 | 0.32 (0.76; 0.73) | 0.866 | 0.009 [0.73] |
| vol_c1.5 | 0.1086 | 0.1783 | 0.4701 | 0.6897 | -0.6536 | 0.1662 | 1.2267 | 2.2100 | 0.0075 | 0.30 (0.39; 0.35) | 1.067 | -0.012 [0.76] |
| vol_c2 | 0.1102 | 0.2005 | 0.4482 | 0.6522 | -0.7679 | 0.1436 | 1.3869 | 3.6284 | 0.0123 | 0.16 (0.15; 0.13) | 1.164 | -0.034 [0.47] |
| var_c1_rvCOWY | 0.0832 | 0.1155 | 0.4421 | 0.6495 | -0.4894 | 0.1701 | 0.7886 | 1.7209 | 0.0059 | 0.16 (0.25; 0.23) | 0.653 | -0.040 [0.46] |
| comprar_y_mantener | 0.1038 | 0.1572 | 0.4820 | 0.7084 | -0.5031 | 0.2064 | 1.0000 | 0.0126 | 0.0000 | -0.00 (-1.00; -1.00) | 1.000 | — |
| sma10 | 0.0922 | 0.1161 | 0.5126 | 0.7515 | -0.4314 | 0.2137 | 0.7345 | 1.4732 | 0.0050 | 1.85 (1.93; 1.64) | 0.542 | 0.031 [0.71] |
| efectivo | 0.0363 | 0.0090 | 0.0000 | 0.0000 | -0.0009 | 40.2850 | 0.0000 | 0.0000 | 0.0000 | nan (nan; nan) | nan | — |

Segmento hueco_2016_2017: 2015-12-31 (cierre base) a 2017-07-31, n=19

| variante | CAGR | vol | Sharpe | Sortino | MDD | Calmar | expos. media | rotación/año | costo/año | α vs mercado %/año (t HC0; t NW12) | β | ΔSR vs CyM [p JK] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| var_c1 | 0.1319 | 0.0538 | 2.2776 | 6.2944 | -0.0213 | 6.1980 | 0.8047 | 2.4267 | 0.0083 | 4.80 (3.38; 3.81) | 0.497 | 0.644 [0.21] |
| var_c1.5 | 0.1804 | 0.0730 | 2.2771 | 8.2361 | -0.0213 | 8.4774 | 1.0604 | 4.2786 | 0.0145 | 7.58 (3.29; 3.54) | 0.603 | 0.643 [0.31] |
| var_c2 | 0.2127 | 0.0920 | 2.1179 | 9.3134 | -0.0213 | 9.9967 | 1.2390 | 6.7832 | 0.0231 | 8.97 (2.87; 3.85) | 0.702 | 0.484 [0.48] |
| vol_c1 | 0.1473 | 0.0751 | 1.8288 | 3.6161 | -0.0442 | 3.3280 | 0.9326 | 0.9513 | 0.0032 | 1.63 (2.43; 2.99) | 0.809 | 0.195 [0.20] |
| vol_c1.5 | 0.2056 | 0.0901 | 2.0948 | 4.8441 | -0.0448 | 4.5835 | 1.2409 | 2.7640 | 0.0094 | 5.09 (3.29; 3.50) | 0.921 | 0.461 [0.16] |
| vol_c2 | 0.2343 | 0.1043 | 2.0509 | 5.4098 | -0.0448 | 5.2237 | 1.3960 | 4.9520 | 0.0168 | 6.24 (2.78; 3.87) | 1.012 | 0.417 [0.33] |
| var_c1_rvCOWY | 0.1302 | 0.0547 | 2.2138 | 5.7636 | -0.0234 | 5.5744 | 0.8071 | 2.4220 | 0.0082 | 4.43 (3.31; 3.54) | 0.512 | 0.580 [0.23] |
| comprar_y_mantener | 0.1597 | 0.0915 | 1.6340 | 3.0915 | -0.0577 | 2.7693 | 1.0000 | 0.0000 | 0.0000 | 0.00 (0.00; 0.00) | 1.000 | — |
| sma10 | 0.1493 | 0.0567 | 2.4324 | 8.5081 | -0.0199 | 7.5028 | 0.8421 | 1.2638 | 0.0043 | 8.05 (2.69; 4.76) | 0.384 | 0.798 [0.31] |
| efectivo | 0.0035 | 0.0006 | 0.0000 | 0.0000 | 0.0000 | inf | 0.0000 | 0.0000 | 0.0000 | nan (nan; nan) | nan | — |

Segmento fuera_muestra: 2017-07-31 (cierre base) a 2026-07-31, n=108

| variante | CAGR | vol | Sharpe | Sortino | MDD | Calmar | expos. media | rotación/año | costo/año | α vs mercado %/año (t HC0; t NW12) | β | ΔSR vs CyM [p JK] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| var_c1 | 0.0690 | 0.0878 | 0.5242 | 0.7497 | -0.1074 | 0.6424 | 0.6207 | 3.0101 | 0.0102 | -0.69 (-0.36; -0.42) | 0.417 | -0.234 [0.28] |
| var_c1.5 | 0.0606 | 0.1067 | 0.3738 | 0.5036 | -0.1902 | 0.3184 | 0.7403 | 4.8303 | 0.0164 | -1.98 (-0.74; -0.79) | 0.471 | -0.385 [0.12] |
| var_c2 | 0.0572 | 0.1219 | 0.3162 | 0.4155 | -0.2611 | 0.2192 | 0.8067 | 5.8799 | 0.0200 | -2.56 (-0.76; -0.76) | 0.507 | -0.442 [0.09] |
| vol_c1 | 0.1124 | 0.1266 | 0.7130 | 1.0913 | -0.1618 | 0.6951 | 0.8521 | 1.3746 | 0.0047 | 0.05 (0.04; 0.04) | 0.709 | -0.045 [0.71] |
| vol_c1.5 | 0.1065 | 0.1457 | 0.6003 | 0.8728 | -0.1778 | 0.5989 | 1.0226 | 3.5491 | 0.0121 | -1.21 (-0.57; -0.63) | 0.787 | -0.158 [0.30] |
| vol_c2 | 0.1026 | 0.1573 | 0.5452 | 0.7696 | -0.2417 | 0.4244 | 1.0864 | 4.5795 | 0.0156 | -1.84 (-0.67; -0.67) | 0.823 | -0.213 [0.21] |
| var_c1_rvCOWY | 0.0703 | 0.0891 | 0.5321 | 0.7665 | -0.1079 | 0.6517 | 0.6190 | 2.8176 | 0.0096 | -0.65 (-0.34; -0.39) | 0.425 | -0.226 [0.29] |
| comprar_y_mantener | 0.1465 | 0.1667 | 0.7584 | 1.1919 | -0.2484 | 0.5897 | 1.0000 | 0.0000 | 0.0000 | 0.00 (1.56; 1.67) | 1.000 | — |
| sma10 | 0.0864 | 0.1215 | 0.5380 | 0.8175 | -0.1931 | 0.4477 | 0.7963 | 2.0002 | 0.0068 | -0.00 (-0.00; -0.00) | 0.519 | -0.220 [0.39] |
| efectivo | 0.0252 | 0.0055 | 0.0000 | 0.0000 | 0.0000 | inf | 0.0000 | 0.0000 | 0.0000 | nan (nan; nan) | nan | — |

Distribución de exposiciones (fracción de meses en el tope; P50) por segmento:
- var_c1: completo tope 0.535, P50 1.000, min 0.013; dentro_muestra tope 0.559, P50 1.000, min 0.017; fuera_muestra tope 0.315, P50 0.642, min 0.013
- var_c1.5: completo tope 0.354, P50 1.076, min 0.013; dentro_muestra tope 0.374, P50 1.122, min 0.017; fuera_muestra tope 0.157, P50 0.642, min 0.013
- var_c2: completo tope 0.248, P50 1.076, min 0.013; dentro_muestra tope 0.265, P50 1.122, min 0.017; fuera_muestra tope 0.102, P50 0.642, min 0.013
- vol_c1: completo tope 0.709, P50 1.000, min 0.145; dentro_muestra tope 0.731, P50 1.000, min 0.168; fuera_muestra tope 0.509, P50 1.000, min 0.145
- vol_c1.5: completo tope 0.407, P50 1.369, min 0.145; dentro_muestra tope 0.429, P50 1.402, min 0.168; fuera_muestra tope 0.204, P50 1.032, min 0.145
- vol_c2: completo tope 0.199, P50 1.369, min 0.145; dentro_muestra tope 0.214, P50 1.402, min 0.168; fuera_muestra tope 0.083, P50 1.032, min 0.145
- var_c1_rvCOWY: completo tope 0.524, P50 1.000, min 0.014; dentro_muestra tope 0.549, P50 1.000, min 0.018; fuera_muestra tope 0.296, P50 0.621, min 0.014

**Verificación del motor.** Una segunda implementación, sin el motor, obtiene los mismos pesos y los mismos rendimientos netos. Estas son las mismas métricas, con las fechas de la caída máxima:

Verificación: máx |w_motor − w_directo| por variante: var_c1 2.22e-16, var_c1.5 2.22e-16, var_c2 2.22e-16, vol_c1 1.11e-16, vol_c1.5 2.22e-16, vol_c2 2.22e-16, var_c1_rvCOWY 1.11e-16

| variante | segmento | Sharpe indep. | dif. vs CSV | CAGR indep. | dif. vs CSV | MDD indep. | dif. vs CSV | pico | valle | recuperación |
|---|---|---|---|---|---|---|---|---|---|---|
| var_c1 | completo | 0.4605 | 0.0e+00 | 0.0823 | 0.0e+00 | -0.5044 | 0.0e+00 | 1937-02-28 | 1942-04-30 | 1944-12-31 |
| var_c1 | dentro_muestra | 0.4408 | 0.0e+00 | 0.0828 | 0.0e+00 | -0.5044 | 0.0e+00 | 1937-02-28 | 1942-04-30 | 1944-12-31 |
| var_c1 | fuera_muestra | 0.5242 | 0.0e+00 | 0.0690 | 0.0e+00 | -0.1074 | 0.0e+00 | 2018-09-30 | 2020-03-31 | 2021-06-30 |
| var_c1.5 | completo | 0.4293 | 0.0e+00 | 0.0886 | 0.0e+00 | -0.6902 | 0.0e+00 | 1937-02-28 | 1942-04-30 | 1945-09-30 |
| var_c1.5 | dentro_muestra | 0.4185 | 0.0e+00 | 0.0900 | 0.0e+00 | -0.6902 | 0.0e+00 | 1937-02-28 | 1942-04-30 | 1945-09-30 |
| var_c1.5 | fuera_muestra | 0.3738 | 0.0e+00 | 0.0606 | 0.0e+00 | -0.1902 | 0.0e+00 | 2018-09-30 | 2020-10-31 | 2024-02-29 |
| var_c2 | completo | 0.3971 | 0.0e+00 | 0.0898 | 0.0e+00 | -0.7935 | 0.0e+00 | 1937-02-28 | 1942-04-30 | 1945-11-30 |
| var_c2 | dentro_muestra | 0.3881 | 0.0e+00 | 0.0912 | 0.0e+00 | -0.7935 | 0.0e+00 | 1937-02-28 | 1942-04-30 | 1945-11-30 |
| var_c2 | fuera_muestra | 0.3162 | -5.6e-17 | 0.0572 | 0.0e+00 | -0.2611 | 0.0e+00 | 2018-09-30 | 2020-10-31 | 2024-08-31 |
| vol_c1 | completo | 0.5234 | 0.0e+00 | 0.1012 | 0.0e+00 | -0.4223 | 0.0e+00 | 1937-02-28 | 1938-03-31 | 1943-05-31 |
| vol_c1 | dentro_muestra | 0.4914 | 0.0e+00 | 0.0991 | 0.0e+00 | -0.4223 | 0.0e+00 | 1937-02-28 | 1938-03-31 | 1943-05-31 |
| vol_c1 | fuera_muestra | 0.7130 | 0.0e+00 | 0.1124 | 0.0e+00 | -0.1618 | 0.0e+00 | 2021-12-31 | 2022-09-30 | 2023-06-30 |
| vol_c1.5 | completo | 0.4941 | 0.0e+00 | 0.1101 | 0.0e+00 | -0.6536 | 0.0e+00 | 1937-02-28 | 1942-04-30 | 1945-02-28 |
| vol_c1.5 | dentro_muestra | 0.4701 | 0.0e+00 | 0.1086 | 0.0e+00 | -0.6536 | 0.0e+00 | 1937-02-28 | 1942-04-30 | 1945-02-28 |
| vol_c1.5 | fuera_muestra | 0.6003 | 0.0e+00 | 0.1065 | 0.0e+00 | -0.1778 | 0.0e+00 | 2018-09-30 | 2020-03-31 | 2021-02-28 |
| vol_c2 | completo | 0.4692 | 0.0e+00 | 0.1115 | 0.0e+00 | -0.7679 | 0.0e+00 | 1937-02-28 | 1942-04-30 | 1945-08-31 |
| vol_c2 | dentro_muestra | 0.4482 | 0.0e+00 | 0.1102 | 0.0e+00 | -0.7679 | 0.0e+00 | 1937-02-28 | 1942-04-30 | 1945-08-31 |
| vol_c2 | fuera_muestra | 0.5452 | 0.0e+00 | 0.1026 | 0.0e+00 | -0.2417 | 0.0e+00 | 2018-09-30 | 2020-03-31 | 2021-06-30 |
| var_c1_rvCOWY | completo | 0.4622 | 0.0e+00 | 0.0827 | 0.0e+00 | -0.4894 | 0.0e+00 | 1937-02-28 | 1942-04-30 | 1944-11-30 |
| var_c1_rvCOWY | dentro_muestra | 0.4421 | 0.0e+00 | 0.0832 | 0.0e+00 | -0.4894 | 0.0e+00 | 1937-02-28 | 1942-04-30 | 1944-11-30 |
| var_c1_rvCOWY | fuera_muestra | 0.5321 | 0.0e+00 | 0.0703 | 0.0e+00 | -0.1079 | 0.0e+00 | 2018-09-30 | 2020-03-31 | 2021-06-30 |
| comprar_y_mantener | completo | 0.5222 | 0.0e+00 | 0.1090 | 0.0e+00 | -0.5031 | 0.0e+00 | 2007-10-31 | 2009-02-28 | 2012-02-29 |
| comprar_y_mantener | dentro_muestra | 0.4820 | 0.0e+00 | 0.1038 | 0.0e+00 | -0.5031 | 0.0e+00 | 2007-10-31 | 2009-02-28 | 2012-02-29 |
| comprar_y_mantener | fuera_muestra | 0.7584 | 0.0e+00 | 0.1465 | 0.0e+00 | -0.2484 | 0.0e+00 | 2021-12-31 | 2022-09-30 | 2023-12-31 |
| sma10 | completo | 0.5306 | 0.0e+00 | 0.0926 | 0.0e+00 | -0.4314 | 0.0e+00 | 1938-12-31 | 1941-11-30 | 1945-02-28 |
| sma10 | dentro_muestra | 0.5126 | 0.0e+00 | 0.0922 | 0.0e+00 | -0.4314 | 0.0e+00 | 1938-12-31 | 1941-11-30 | 1945-02-28 |
| sma10 | fuera_muestra | 0.5380 | 0.0e+00 | 0.0864 | 0.0e+00 | -0.1931 | 0.0e+00 | 2018-09-30 | 2019-08-31 | 2020-11-30 |

Diferencia máxima absoluta contra el registro: 5.55e-17

**Cómo leerlo (hechos).**

- **Variante seleccionada: `vol_c1`**, que es w = min(1, k_t/RV_{t−1}).
  - Fuera de muestra: Sharpe 0.7130, contra 0.7584 de comprar y mantener y 0.5380 de la SMA10. MDD −16.18%, contra −24.84% y −19.31%. CAGR 11.24%, contra 14.65% y 8.64%. α contra el mercado 0.05% anual (t 0.04). ΔSR contra comprar y mantener −0.045 [p 0.71].
  - Dentro de muestra: Sharpe 0.4914, contra 0.4820 y 0.5126. MDD −42.23% (1937-02 a 1938-03), contra −50.31% (2007-10 a 2009-02) y −43.14%. α 0.32% (t 0.76).
- **Ninguna de las 7 variantes tiene α contra el mercado con |t HC0| > 0.76**, ni dentro ni fuera de muestra.
- **`var_c1`** es la regla de MM "No Leverage" (1/RV², tope 1) en tiempo real.
  - Dentro de muestra: Sharpe 0.4408, debajo de comprar y mantener. MDD −50.44%, entre 1937-02 y 1942-04, **igual o peor que la del índice**.
  - Fuera de muestra: MDD −10.74% y CAGR 6.90%, con exposición media de 0.62.
- **Las versiones apalancadas tienen menor Sharpe** que su versión con tope 1 y que comprar y mantener en `dentro_muestra`, `fuera_muestra` y `completo`. Fuera de muestra, `var_c2` tiene ΔSR −0.442 [p 0.09].
- **Hueco 2016-01 a 2017-07 (19 meses).** Todas las variantes tuvieron Sharpe mayor que 1.8 en un mercado tranquilo. No se usa para ninguna conclusión.

#### 11.5 Veredictos mecánicos del pre-registro

- H1 (MM 1926-2015): Replicado. α 4.88 (t HC0 3.13) vs 4.86 ± 1.56
- H2 (post JF 2017-08 a 2026-07-31): refutada (no significativo). α -0.75 (t HC0 -0.15); SR gestionada 0.407 vs mercado 0.758 [p JK 0.25]
- H3 (Cederburg): Replicado. S1 0.415 vs S2 0.458 (artículo 0.42 vs 0.46); dif -0.043 [p 0.62]
- H4 (operable): seleccionada vol_c1. Fuera: Sharpe 0.7130 vs CyM 0.7584 vs SMA10 0.5380; MDD -0.1618 vs -0.2484 vs -0.1931. Agrega valor vs CyM: False; vs SMA10: False; H4 refutada por Sharpe: True; freno refutado: False; α fuera 0.05 (t 0.04), α dentro 0.32 (t 0.76); DSR dentro 0.9999

Sobre H4 frente a la SMA10: fuera de muestra, `vol_c1` sí supera a la SMA10 en Sharpe (0.7130 contra 0.5380) y en MDD (−16.18% contra −19.31%). El veredicto "agrega valor frente a la regla sencilla" sale `False` porque el pre-registro lo condiciona a superar **además** a comprar y mantener, y eso no ocurre.

### 12. Sensibilidad

**Costos: spread "medio" (0.15% por lado) y "bruto" (sin comisión ni spread).**

Segmento dentro_muestra: 1936-07-31 (cierre base) a 2015-12-31, n=953

| variante | CAGR | vol | Sharpe | Sortino | MDD | Calmar | expos. media | rotación/año | costo/año | α vs mercado %/año (t HC0; t NW12) | β | ΔSR vs CyM [p JK] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| var_c1|spread_medio | 0.0809 | 0.1149 | 0.4254 | 0.6219 | -0.5107 | 0.1585 | 0.7883 | 1.7489 | 0.0077 | -0.02 (-0.03; -0.03) | 0.647 | -0.057 [0.30] |
| var_c1.5|spread_medio | 0.0864 | 0.1475 | 0.3956 | 0.5757 | -0.6973 | 0.1239 | 1.0155 | 3.3471 | 0.0147 | -0.13 (-0.13; -0.11) | 0.786 | -0.086 [0.18] |
| var_c2|spread_medio | 0.0859 | 0.1739 | 0.3601 | 0.5180 | -0.8001 | 0.1074 | 1.1743 | 4.8486 | 0.0213 | -0.45 (-0.34; -0.30) | 0.884 | -0.122 [0.09] |
| vol_c1|spread_medio | 0.0982 | 0.1399 | 0.4860 | 0.7159 | -0.4231 | 0.2322 | 0.9298 | 0.7500 | 0.0033 | 0.24 (0.58; 0.56) | 0.866 | 0.004 [0.88] |
| vol_c1.5|spread_medio | 0.1062 | 0.1783 | 0.4577 | 0.6700 | -0.6592 | 0.1611 | 1.2267 | 2.2100 | 0.0097 | 0.07 (0.10; 0.09) | 1.066 | -0.024 [0.53] |
| vol_c2|spread_medio | 0.1062 | 0.2005 | 0.4300 | 0.6236 | -0.7737 | 0.1373 | 1.3869 | 3.6284 | 0.0160 | -0.21 (-0.20; -0.18) | 1.164 | -0.052 [0.27] |
| var_c1_rvCOWY|spread_medio | 0.0814 | 0.1155 | 0.4271 | 0.6260 | -0.4959 | 0.1641 | 0.7886 | 1.7209 | 0.0076 | -0.01 (-0.02; -0.02) | 0.652 | -0.055 [0.31] |
| comprar_y_mantener|spread_medio | 0.1038 | 0.1572 | 0.4819 | 0.7083 | -0.5031 | 0.2063 | 1.0000 | 0.0126 | 0.0001 | -0.01 (-1.00; -1.00) | 1.000 | — |
| sma10|spread_medio | 0.0906 | 0.1161 | 0.4995 | 0.7314 | -0.4365 | 0.2075 | 0.7345 | 1.4732 | 0.0065 | 1.70 (1.77; 1.50) | 0.542 | 0.018 [0.83] |

Segmento fuera_muestra: 2017-07-31 (cierre base) a 2026-07-31, n=108

| variante | CAGR | vol | Sharpe | Sortino | MDD | Calmar | expos. media | rotación/año | costo/año | α vs mercado %/año (t HC0; t NW12) | β | ΔSR vs CyM [p JK] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| var_c1|spread_medio | 0.0658 | 0.0877 | 0.4898 | 0.6965 | -0.1134 | 0.5802 | 0.6207 | 3.0101 | 0.0132 | -0.99 (-0.53; -0.59) | 0.417 | -0.269 [0.22] |
| var_c1.5|spread_medio | 0.0554 | 0.1067 | 0.3280 | 0.4386 | -0.2022 | 0.2742 | 0.7403 | 4.8303 | 0.0213 | -2.47 (-0.92; -0.97) | 0.471 | -0.430 [0.08] |
| var_c2|spread_medio | 0.0510 | 0.1220 | 0.2675 | 0.3488 | -0.2749 | 0.1856 | 0.8067 | 5.8799 | 0.0259 | -3.15 (-0.94; -0.92) | 0.507 | -0.491 [0.06] |
| vol_c1|spread_medio | 0.1109 | 0.1265 | 0.7022 | 1.0728 | -0.1626 | 0.6822 | 0.8521 | 1.3746 | 0.0060 | -0.08 (-0.06; -0.07) | 0.708 | -0.056 [0.65] |
| vol_c1.5|spread_medio | 0.1026 | 0.1457 | 0.5758 | 0.8335 | -0.1845 | 0.5559 | 1.0226 | 3.5491 | 0.0156 | -1.56 (-0.74; -0.80) | 0.786 | -0.183 [0.23] |
| vol_c2|spread_medio | 0.0975 | 0.1573 | 0.5158 | 0.7245 | -0.2504 | 0.3895 | 1.0864 | 4.5795 | 0.0201 | -2.30 (-0.84; -0.82) | 0.823 | -0.243 [0.16] |
| var_c1_rvCOWY|spread_medio | 0.0673 | 0.0891 | 0.5002 | 0.7169 | -0.1137 | 0.5922 | 0.6190 | 2.8176 | 0.0124 | -0.93 (-0.49; -0.56) | 0.425 | -0.258 [0.23] |
| comprar_y_mantener|spread_medio | 0.1465 | 0.1667 | 0.7584 | 1.1919 | -0.2484 | 0.5897 | 1.0000 | 0.0000 | 0.0000 | 0.00 (1.56; 1.67) | 1.000 | — |
| sma10|spread_medio | 0.0843 | 0.1217 | 0.5210 | 0.7895 | -0.1979 | 0.4257 | 0.7963 | 2.0002 | 0.0088 | -0.20 (-0.07; -0.07) | 0.519 | -0.237 [0.36] |

Segmento dentro_muestra: 1936-07-31 (cierre base) a 2015-12-31, n=953

| variante | CAGR | vol | Sharpe | Sortino | MDD | Calmar | expos. media | rotación/año | costo/año | α vs mercado %/año (t HC0; t NW12) | β | ΔSR vs CyM [p JK] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| var_c1|bruto | 0.0893 | 0.1148 | 0.4928 | 0.7280 | -0.4822 | 0.1852 | 0.7883 | 1.7489 | 0.0000 | 0.75 (1.16; 1.06) | 0.648 | 0.010 [0.85] |
| var_c1.5|bruto | 0.1025 | 0.1475 | 0.4960 | 0.7342 | -0.6650 | 0.1541 | 1.0155 | 3.3471 | 0.0000 | 1.35 (1.37; 1.23) | 0.787 | 0.014 [0.83] |
| var_c2|bruto | 0.1094 | 0.1740 | 0.4833 | 0.7107 | -0.7696 | 0.1421 | 1.1743 | 4.8486 | 0.0000 | 1.70 (1.31; 1.17) | 0.885 | 0.001 [0.99] |
| vol_c1|bruto | 0.1019 | 0.1400 | 0.5095 | 0.7538 | -0.4197 | 0.2427 | 0.9298 | 0.7500 | 0.0000 | 0.57 (1.37; 1.31) | 0.866 | 0.027 [0.31] |
| vol_c1.5|bruto | 0.1170 | 0.1784 | 0.5124 | 0.7574 | -0.6340 | 0.1846 | 1.2267 | 2.2100 | 0.0000 | 1.05 (1.40; 1.26) | 1.067 | 0.030 [0.44] |
| vol_c2|bruto | 0.1240 | 0.2007 | 0.5099 | 0.7504 | -0.7468 | 0.1661 | 1.3869 | 3.6284 | 0.0000 | 1.40 (1.36; 1.21) | 1.165 | 0.028 [0.56] |
| var_c1_rvCOWY|bruto | 0.0896 | 0.1155 | 0.4929 | 0.7299 | -0.4665 | 0.1921 | 0.7886 | 1.7209 | 0.0000 | 0.75 (1.15; 1.07) | 0.653 | 0.011 [0.84] |
| comprar_y_mantener|bruto | 0.1039 | 0.1572 | 0.4823 | 0.7088 | -0.5031 | 0.2065 | 1.0000 | 0.0126 | 0.0000 | 0.00 (0.00; 0.00) | 1.000 | — |
| sma10|bruto | 0.0977 | 0.1159 | 0.5565 | 0.8196 | -0.4137 | 0.2361 | 0.7345 | 1.4732 | 0.0000 | 2.35 (2.45; 2.14) | 0.541 | 0.074 [0.37] |

Segmento fuera_muestra: 2017-07-31 (cierre base) a 2026-07-31, n=108

| variante | CAGR | vol | Sharpe | Sortino | MDD | Calmar | expos. media | rotación/año | costo/año | α vs mercado %/año (t HC0; t NW12) | β | ΔSR vs CyM [p JK] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| var_c1|bruto | 0.0800 | 0.0880 | 0.6405 | 0.9342 | -0.0948 | 0.8439 | 0.6207 | 3.0101 | 0.0000 | 0.34 (0.18; 0.22) | 0.417 | -0.118 [0.59] |
| var_c1.5|bruto | 0.0782 | 0.1068 | 0.5289 | 0.7310 | -0.1599 | 0.4889 | 0.7403 | 4.8303 | 0.0000 | -0.32 (-0.12; -0.14) | 0.471 | -0.230 [0.35] |
| var_c2|bruto | 0.0786 | 0.1219 | 0.4815 | 0.6494 | -0.2246 | 0.3500 | 0.8067 | 5.8799 | 0.0000 | -0.53 (-0.16; -0.17) | 0.506 | -0.277 [0.30] |
| vol_c1|bruto | 0.1177 | 0.1267 | 0.7494 | 1.1546 | -0.1590 | 0.7401 | 0.8521 | 1.3746 | 0.0000 | 0.50 (0.38; 0.45) | 0.710 | -0.009 [0.94] |
| vol_c1.5|bruto | 0.1199 | 0.1459 | 0.6833 | 1.0082 | -0.1635 | 0.7334 | 1.0226 | 3.5491 | 0.0000 | -0.00 (-0.00; -0.00) | 0.788 | -0.075 [0.62] |
| vol_c2|bruto | 0.1199 | 0.1574 | 0.6448 | 0.9259 | -0.2114 | 0.5673 | 1.0864 | 4.5795 | 0.0000 | -0.27 (-0.10; -0.10) | 0.824 | -0.114 [0.51] |
| var_c1_rvCOWY|bruto | 0.0807 | 0.0892 | 0.6401 | 0.9382 | -0.0961 | 0.8394 | 0.6190 | 2.8176 | 0.0000 | 0.32 (0.17; 0.21) | 0.424 | -0.118 [0.59] |
| comprar_y_mantener|bruto | 0.1465 | 0.1667 | 0.7584 | 1.1919 | -0.2484 | 0.5897 | 1.0000 | 0.0000 | 0.0000 | 0.00 (1.56; 1.67) | 1.000 | — |
| sma10|bruto | 0.0939 | 0.1212 | 0.5955 | 0.9128 | -0.1764 | 0.5320 | 0.7963 | 2.0002 | 0.0000 | 0.66 (0.22; 0.23) | 0.521 | -0.163 [0.53] |

- **Sin costos, dentro de muestra.** Las 7 variantes tienen Sharpe entre 0.4833 y 0.5124, contra 0.4823 de comprar y mantener. ΔSR entre +0.001 y +0.030; ninguna tiene p menor que 0.31.
- **Con costos por defecto, dentro de muestra.** Solo `vol_c1` queda arriba, por +0.009 (p 0.73). Con spread medio, `vol_c1` queda en +0.004 (p 0.88).
- **Fuera de muestra**, ni siquiera sin costos supera ninguna a comprar y mantener: `vol_c1` bruto tiene 0.7494 contra 0.7584.
- **Tamaño de los costos.** Los costos de GBM por lado (0.34% por defecto, 0.44% con spread medio) son 2.4 y 3.1 veces el peor escenario de la tabla 4 de MM (14 pb).

**Costo del apalancamiento de 3% anual sobre RF (post-proceso, supuesto).**

| variante | segmento | Sharpe motor | Sharpe ajustado | CAGR motor | CAGR ajustado | MDD ajustado |
|---|---|---|---|---|---|---|
| var_c1.5 | completo | 0.4293 | 0.3842 | 0.0886 | 0.0815 | -0.7012 |
| var_c1.5 | dentro_muestra | 0.4185 | 0.3727 | 0.0900 | 0.0827 | -0.7012 |
| var_c1.5 | fuera_muestra | 0.3738 | 0.3395 | 0.0606 | 0.0568 | -0.1980 |
| var_c2 | completo | 0.3971 | 0.3322 | 0.0898 | 0.0779 | -0.8069 |
| var_c2 | dentro_muestra | 0.3881 | 0.3221 | 0.0912 | 0.0787 | -0.8069 |
| var_c2 | fuera_muestra | 0.3162 | 0.2700 | 0.0572 | 0.0513 | -0.2742 |
| vol_c1.5 | completo | 0.4941 | 0.4452 | 0.1101 | 0.1007 | -0.6693 |
| vol_c1.5 | dentro_muestra | 0.4701 | 0.4204 | 0.1086 | 0.0989 | -0.6693 |
| vol_c1.5 | fuera_muestra | 0.6003 | 0.5644 | 0.1065 | 0.1009 | -0.1861 |
| vol_c2 | completo | 0.4692 | 0.4027 | 0.1115 | 0.0972 | -0.7850 |
| vol_c2 | dentro_muestra | 0.4482 | 0.3802 | 0.1102 | 0.0952 | -0.7850 |
| vol_c2 | fuera_muestra | 0.5452 | 0.4996 | 0.1026 | 0.0949 | -0.2538 |

**MXN (DEXMXUS, efectivo RF en USD convertido).**

```
DEXMXUS: 1993-11-08 a 2026-09-18 (8239 obs)
variante                          cagr  vol_anual    sharpe       mdd  exposicion_media  costo_anual
var_c1|mxn|rf_usd               0.1277     0.1419    0.5528   -0.1669            0.6260       0.0086
vol_c1|mxn|rf_usd               0.1553     0.1496    0.5943   -0.2927            0.8516       0.0043
comprar_y_mantener|mxn|rf_us    0.1694     0.1669    0.5377   -0.3986            1.0000       0.0001
sma10|mxn|rf_usd                0.1567     0.1558    0.6460   -0.2401            0.7679       0.0051
  (completo: 1993-11-30 a 2026-07-31)

variante                          cagr  vol_anual    sharpe       mdd  exposicion_media  costo_anual
var_c1|mxn|rf_usd               0.1519     0.1505    0.5107   -0.1669            0.6153       0.0079
vol_c1|mxn|rf_usd               0.1734     0.1575    0.5143   -0.2927            0.8456       0.0042
comprar_y_mantener|mxn|rf_us    0.1791     0.1727    0.4265   -0.3986            1.0000       0.0002
sma10|mxn|rf_usd                0.1868     0.1592    0.6482   -0.1530            0.7509       0.0045
  (dentro_muestra: 1993-11-30 a 2015-12-31)

variante                          cagr  vol_anual    sharpe       mdd  exposicion_media  costo_anual
var_c1|mxn|rf_usd               0.0654     0.1155    0.4662   -0.1580            0.6207       0.0102
vol_c1|mxn|rf_usd               0.1087     0.1279    0.6504   -0.2024            0.8521       0.0047
comprar_y_mantener|mxn|rf_us    0.1426     0.1552    0.6941   -0.2725            1.0000       0.0000
sma10|mxn|rf_usd                0.0828     0.1451    0.5046   -0.2401            0.7963       0.0068
  (fuera_muestra: 2017-07-31 a 2026-07-31)
```

- **Fuera de muestra.** `vol_c1` tuvo Sharpe 0.6504, CAGR 10.87% y MDD −20.24%. Comprar y mantener tuvo 0.6941, 14.26% y −27.25%. La SMA10 tuvo 0.5046, 8.28% y −24.01%.
- **Dentro de muestra (cierre base 1993-11-30 a 2015-12).** `vol_c1` tuvo 0.5143, 17.34% y −29.27%. Comprar y mantener tuvo 0.4265, 17.91% y −39.86%. La SMA10 tuvo 0.6482, 18.68% y −15.30%.

**Subperiodos de la estadística de MM (A1, con c de cada ventana).**

| Caso | Ventana | N | α %/año (e.e. HC0) | t HC0 / t NW12 | β | R² | rmse | AR | SR mercado | SR gestionada | ΔSR [p JK] | P50/P75/P90/P99 de w | frac. en tope |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1926-08 a 1955-12 | 1926-08 a 1955-12 | 353 | 11.03 (3.65) | 3.02 / 2.53 | 0.552 | 0.305 | 70.49 | 0.542 | 0.443 | 0.697 | 0.254 [0.15] | 1.03/1.85/3.63/7.01 | 0.000 |
| 1956-01 a 1985-12 | 1956-01 a 1985-12 | 360 | 1.35 (1.86) | 0.73 / 0.70 | 0.717 | 0.514 | 35.50 | 0.132 | 0.330 | 0.329 | -0.001 [0.99] | 0.79/1.35/2.21/6.34 | 0.000 |
| 1986-01 a 2015-12 | 1986-01 a 2015-12 | 360 | 4.79 (2.05) | 2.34 / 2.14 | 0.695 | 0.483 | 38.70 | 0.429 | 0.495 | 0.653 | 0.158 [0.27] | 0.88/1.53/2.29/5.63 | 0.000 |
| 2016-01 al final | 2016-01 a 2026-07 | 127 | 1.48 (4.55) | 0.32 / 0.28 | 0.597 | 0.357 | 43.90 | 0.117 | 0.825 | 0.587 | -0.238 [0.40] | 0.67/1.35/2.24/3.79 | 0.000 |
| 1926-08 al final | 1926-08 a 2026-07 | 1200 | 4.52 (1.46) | 3.09 / 2.70 | 0.601 | 0.361 | 50.91 | 0.307 | 0.452 | 0.517 | 0.065 [0.47] | 0.90/1.60/2.68/6.99 | 0.000 |

- **El α no es estable.** Es de 11.03 (t 3.02) en 1926-1955, 1.35 (t 0.73) en 1956-1985, 4.79 (t 2.34) en 1986-2015 y 1.48 (t 0.32) en 2016-2026.
- **Coincide en parte con Cederburg et al.** El mayor α está en el tramo de la Gran Depresión. Pero 1986-2015 también tiene un α significativo al 5% (HC0).

**Definición de la RV.** Pasar de la RV de MM a la de Cederburg cambia poco la versión operable. El Sharpe de `var_c1_rvCOWY` es 0.4421 contra 0.4408 dentro de muestra y 0.5321 contra 0.5242 fuera. En la estadística A1, α pasa de 4.88 a 4.56.

### 13. Diferencia frente al artículo

| Aspecto | Artículo | Réplica | ¿Explica la diferencia? |
|---|---|---|---|
| Datos / versión | MM: CRSP vía French hasta 2015 (versión de 2016). Cederburg et al.: hasta 2016-12 | French CRSP 202607 (sha256 mensual b840dba5…, diario 1916d331…). T-bill de ICE BofA desde 202406 | Las diferencias de α son ≤ 0.08 pp en la tabla 5 de MM y de 0.02 pp en la tabla 3 de Cederburg. No se atribuyen a una causa concreta |
| Periodo | MM 1926-2015, N = 1,065 | 1926-08 a 2015-12, N = 1,073 | 8 meses de diferencia **no explicados**: MM no documenta el mes inicial en la tabla |
| Varianza realizada | MM: desviaciones respecto a la media del mes, con 22 días. Cederburg: (22/J) Σ d², sin desmediar | Ambas. La de MM con los J_t días reales | En la ventana de MM, α cambia de 4.88 a 4.56. El P99 de los pesos pasa de 7.27 (MM) a 6.07 (Cederburg) |
| Errores estándar | "adjust for heteroscedasticity" (MM); White (Cederburg) | HC0 (White), además de HC1 y NW12 | El e.e. coincide a 2 decimales en A1 |
| c | Muestra completa | Muestra completa en la parte A; ventana expansiva en B y C | En C el α desaparece. *Inferencia:* C empieza en 1936-08 porque los 120 meses previos son entrenamiento, y el subperiodo 1926-1955 concentra el mayor α (11.03). No se cuantificó cuánto de la diferencia viene de la ventana, de c_t o del tope |
| Costos | Tabla 4 de MM: 1, 10 y 14 pb. El α de 1/RV² baja a 3.63% con 14 pb | GBM 0.29% + 0.05% por lado (34 pb); medio, 44 pb | Con costos GBM, el ΔSR bruto de +0.010 de `var_c1` dentro de muestra se vuelve −0.041 |
| Regla | Sin tope (además de topes 1 y 1.5), con c de muestra completa y apalancamiento a RF | Topes 1, 1.5 y 2 con c_t en tiempo real, solo largos. Apalancamiento a RF, más la sensibilidad de +3% | Es la versión operable del sistema, no la del artículo |
| Combinación (Cederburg) | K = 120, γ = 5, \|y\| ≤ 5, sin costos | Igual, más una versión con costos GBM | Se replica: 0.415/0.458 contra 0.42/0.46 |

### 14. Conclusiones permitidas

Alcance: mercado total de EUA (índice CRSP de French, no invertible), 1926-2026, USD. Costos GBM declarados (comisión como hecho, spread como supuesto), sin impuestos ni costo cambiario.

1. **La estadística de MM para el mercado se reproduce en su periodo.** α = 4.88% anual (e.e. 1.56, t 3.13), contra 4.86 (1.56). También se reproducen las variantes de su tabla 5 (dentro de ±1 e.e.) y las cifras de las tablas 1 y 3 de Cederburg et al.
2. **Dentro de muestra, la mejora directa del Sharpe es modesta.** A igual volatilidad, la diferencia no es significativa para 1/RV² (0.511 contra 0.415, p 0.31) y es marginal para 1/RV (p 0.05).
3. **Después de la publicación en el JF, el α de MM no aparece.** En 2017-08 a 2026-07, α = −0.75% (t −0.15), y el Sharpe de la gestionada es 0.407 contra 0.758 del mercado. Con 108 meses no se puede afirmar que el efecto haya desaparecido, pero no hay evidencia a favor.
4. **La crítica de Cederburg et al. para el mercado se replica.** La combinación en tiempo real tuvo Sharpe 0.415 contra 0.458 del original (p 0.62). Con costos GBM la diferencia crece a −0.163 (p 0.05).
5. **La versión operable no genera alfa ni le gana al índice fuera de muestra.** Con costos GBM, 1936-08 a 2026-07, ninguna de las 7 variantes tiene α contra el mercado distinguible de cero (|t| ≤ 0.76), y ninguna supera a comprar y mantener en Sharpe fuera de muestra.
6. **`vol_c1` funcionó como freno con costo.** Con 1/RV del mes previo y tope 1, redujo la caída máxima frente a comprar y mantener en ambos tramos: −42.23% contra −50.31% dentro de muestra y −16.18% contra −24.84% fuera. A cambio, el CAGR fue menor: −0.47 pp/año dentro y −3.41 pp/año fuera.
7. **Las versiones con apalancamiento de 1.5x y 2x fueron peores.** Su Sharpe quedó debajo del de la versión sin apalancamiento y del de comprar y mantener en todos los segmentos, y más aún con un costo de margen de 3%.

### 15. Conclusiones que NO se sostienen

- **"La gestión por volatilidad genera alfa."** El α de MM usa c con toda la muestra y se concentra en 1926-1955 y 1986-2015. En tiempo real y neto de costos es ≈ 0.
- **"`vol_c1` le gana a comprar y mantener."** Fuera de muestra tiene menor Sharpe (0.713 contra 0.758) y menor CAGR. Dentro de muestra su ventaja es de +0.009 (p 0.73).
- **"Un DSR de 0.9999 valida la regla."** Ese DSR se mide contra un Sharpe de 0, y comprar y mantener tiene un Sharpe parecido. No es evidencia de ventaja sobre el índice. Además, fuera de muestra el DSR es 0.93 o menos.
- **"Mantiene la caída dentro de los límites del sistema."** Dentro de muestra, la MDD de `vol_c1` fue −42.23%, más del doble del `drawdown_maximo_duro` de 20%.
- **"La versión de MM sin apalancamiento protege en las caídas."** Dentro de muestra, `var_c1` tuvo una MDD de −50.44% (1937-02 a 1942-04), igual o peor que la del índice.
- **"Funciona en pesos."** En MXN, fuera de muestra, `vol_c1` quedó debajo de comprar y mantener en Sharpe (0.650 contra 0.694) y en CAGR. Sí redujo la MDD (−20.24% contra −27.25%). Es solo una sensibilidad: usa DEXMXUS, que no es un tipo de cambio ejecutable, y RF en USD.
- **"Es mejor que la SMA10."** Dentro de muestra, la SMA10 tuvo mejor Sharpe (0.5126 contra 0.4914). Fuera de muestra, `vol_c1` fue mejor en Sharpe y en MDD. Ninguna domina a la otra.
- **"Tiene ventaja con dinero real."** El índice CRSP no es invertible, la varianza se calculó con datos de French publicados con rezago, el spread es un supuesto y no hay impuestos ni costo cambiario.

### 16. Estado y reproducción

- **Estado: Replicado.**
  - H1: el α de MM en su periodo cae dentro de la tolerancia pre-registrada (+0.02 pp).
  - H3: la crítica de Cederburg et al. para el mercado también se replica, dentro de ±0.05 en S1 y S2.
  - **Fuera de muestra el resultado es negativo:** H2 y H4 (Sharpe) quedan refutadas.
  - No es candidata para dinero: no supera a comprar y mantener fuera de muestra, y su DSR fuera de muestra es menor que 0.95.
- Comando que reproduce todo: `python3 laboratorio/replicas/R05.py` (unos 40 s; cada corrida agrega 37 corridas al CSV). La verificación sin el motor es `python3 laboratorio/replicas/R05_verificacion.py`.
- **Huella de datos:** `huella_datos` e85ac74d630dff95 (USD) y 6f7a2f88fb30b19e (MXN).
- **Archivos French (CRSP 202607):**
  - `sha256` mensual: b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb
  - `sha256` diario: 1916d331c2c51d2aee3d00215897d2b8e5995cb387f1f4569ba46bff5fb049a8
- DEXMXUS de FRED se descargó el 2026-09-25; su último dato es del 2026-09-18.
- Fecha de la corrida final: 2026-09-25.
- Pendiente:
  - Revisión independiente (`auditor-de-replicas`).
  - Fila de R05 en `laboratorio/tabla-maestra.md`.
  - Condiciones de uso de French.
  - Probar con un ETF del SIC y la varianza de un índice disponible en tiempo real (^GSPC diario).

### 17. Conclusión operable

La réplica afecta la **regla 10** de `conocimiento/02-maestria-portafolio-y-asset-pricing.md` §6.1 ("Vol-targeting como freno, no como fuente de alfa") y la nota de §5.3 ("Grado C como alfa y útil como control de riesgo").

- **Confirma la parte "no como fuente de alfa"**, ahora con réplica propia y no solo con la cita de Cederburg et al.:
  - El α de MM se reproduce solo con c de toda la muestra, y después de 2017 vale −0.75% (t −0.15).
  - La combinación en tiempo real le queda debajo al original (0.415 contra 0.458).
  - Las 7 versiones operables tienen α ≈ 0 (|t| ≤ 0.76).
- **Modifica la parte "como freno"**, porque no toda versión frena y la que frena cuesta rendimiento. Texto propuesto:
  > 10. **Vol-targeting como freno, no como fuente de alfa (R05).** Si se usa, la forma es w = min(1, k_t/σ_{mes previo}), con k_t estimada solo con datos pasados y sin apalancamiento. Costo esperado (réplica R05, EUA, USD, con costos GBM): menos CAGR (−0.47 pp/año en 1936-2015 y −3.41 pp/año en 2017-2026) con un Sharpe igual o menor que el del índice (fuera de muestra 0.713 contra 0.758). Redujo la MDD (−42% contra −50%; −16% contra −25%), pero **no sustituye a los `cortacircuitos_drawdown`**: la caída histórica sigue siendo más del doble del límite duro de 20%. No hay evidencia de que sea mejor freno que la SMA10 (R01): cada una ganó en un tramo distinto.
- **Descarta:**
  1. La forma 1/σ² de MM como freno único: sin apalancamiento no redujo la MDD en 1936-2015 (−50.44% contra −50.31%).
  2. Cualquier versión apalancada (1.5x y 2x). Tienen peor Sharpe en todos los segmentos y, además, las prohíben `apalancamiento.bruto_max_fase_1` = 1.0 y la regla 18.3 del cap. 18.
  3. La combinación media-varianza en tiempo real (S1): con costos GBM su Sharpe fue 0.292 contra 0.454 del original.
- **No se modificaron** el capítulo 02 ni `config/parametros.json`. El texto de arriba queda como propuesta para quien mantiene el capítulo.

