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
| Estado | Pendiente (se llena en la sección 16) |

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

_Pendiente: se llena al terminar la corrida de `python3 laboratorio/replicas/R05.py`._
