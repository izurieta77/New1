# Réplica R02: momentum de series de tiempo (TSMOM, Moskowitz-Ooi-Pedersen 2012)

> Fase 0: formación. Esta ficha no recomienda inversiones. Las secciones 1 a 9 son el pre-registro. Se escribieron el 2026-09-25, antes de cualquier corrida, y no se editan después. Cualquier cambio posterior va a "Desviaciones del pre-registro", con fecha.

| Campo | Valor |
|---|---|
| ID | `R02` (registro: `laboratorio/replicas/R02-variantes.csv`; script: `laboratorio/replicas/R02.py`) |
| Artículo | Moskowitz, T. J., Ooi, Y. H. y Pedersen, L. H. (2012). "Time series momentum". *Journal of Financial Economics* 104(2), 228–250. doi:10.1016/j.jfineco.2011.11.003. Versión consultada: PDF de la versión publicada (23 páginas) en https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf, consultado el 2026-09-25 con WebSearch/WebFetch y leído con `pypdf` |
| Fecha de publicación | Recibido el 16-ago-2010, revisado el 11-jul-2011, aceptado el 12-ago-2011, **disponible en línea el 11-dic-2011** y publicado en el número de mayo de 2012 (datos de la primera página del PDF). Hubo una versión de trabajo en 2010 (presentada en la AFA de enero de 2011, según los agradecimientos) |
| Pre-registro escrito el | 2026-09-25, antes de descargar los ETFs y antes de calcular cualquier rendimiento de las estrategias |
| Responsable | Claude (laboratorio del sistema). Revisión independiente pendiente (`auditor-de-replicas`) |
| Estado | Pendiente (se asigna en la sección 16) |

**Conocimiento previo declarado.** El pre-registro no es "ciego" a la historia pública. Antes de correr ya sabía cuatro cosas. (1) Los CTAs de tendencia tuvieron un periodo débil entre 2012 y 2019 y uno fuerte en 2022. (2) El S&P 500 subió mucho entre 2012 y 2026. (3) El capítulo 14 del sistema reporta al SG Trend Index con −15.05% en los 12 meses a junio de 2025. (4) Existen críticas publicadas (Huang et al. 2020; Kim-Tse-Wald 2016). Las hipótesis se escriben igual, con el signo que predice el artículo.

---

## PRE-REGISTRO (secciones 1 a 9)

### 1. Hipótesis previa y mecanismo

**Resultado declarado en el artículo** (cifras textuales, sin redondear):

- **Muestra.** 58 futuros y forwards líquidos: 24 materias primas, 12 pares de divisas, 9 índices accionarios y 13 bonos. Datos desde 1965 y análisis principal de enero de 1985 a diciembre de 2009 (p. 235).
- **Regla TSMOM (ec. 5, p. 236).** r^TSMOM,s_{t,t+1} = sign(r^s_{t−12,t}) · (40%/σ^s_t) · r^s_{t,t+1}. El signo es el del rendimiento en exceso de los últimos 12 meses. La posición se escala a una volatilidad ex ante de 40% anual. Se mantiene 1 mes (k = 12, h = 1). El portafolio diversificado promedia con igual peso los S_t instrumentos disponibles.
- **Volatilidad ex ante (ec. 1, p. 233).** σ²_t = 261 Σ_{i≥0} (1−δ) δ^i (r_{t−1−i} − r̄_t)², con rendimientos diarios, r̄_t la media exponencial y centro de masa δ/(1−δ) = 60 días. Se usa σ_{t−1} para el rendimiento de t.
- **Por instrumento (p. 236, Fig. 2, p. 237).** "All 58 futures contracts exhibit positive time series momentum returns and 52 are statistically different from zero at the 5% significance level". Sharpe bruto anualizado entre 1985 y 2009. La cifra del S&P 500 aparece solo como barra de la Fig. 2: **no hay número en el texto**, así que no se puede comparar la magnitud de ese instrumento.
- **Tabla 2 (p. 235).** Es el t del alfa contra MSCI World, bonos Barclays, S&P GSCI, SMB, HML y UMD, con h = 1 mes:

  | Panel | k = 3 | k = 6 | k = 12 |
  |---|---|---|---|
  | Panel A, todos los activos | 5.35 | 5.03 | 6.61 |
  | Panel C, índices accionarios | 1.48 | 3.50 | 3.77 |

- **Tabla 3, panel A (p. 238).** El TSMOM diversificado tiene un intercepto mensual de **1.58%** (t = 7.99) y R² de 14%. En trimestral es 4.75% (t = 7.73). Las betas son MSCI World 0.09 (t = 1.89) y UMD 0.28 (t = 6.78).
- **Volatilidad del factor (p. 236).** El factor diversificado tiene una volatilidad anual de 12% en 1985–2009.
- **Sharpe del factor (p. 230).** El portafolio diversificado da "a Sharpe ratio greater than one on an annual basis, or roughly 2.5 times the Sharpe ratio for the equity market portfolio".
- **Muestra antigua (p. 238).** En 1966–1985 el Sharpe anualizado es 1.1.
- **Costos.** El artículo **no** descuenta costos de transacción. Sus cifras son brutas y con futuros, cuyo costo es muy inferior al de un ETF comprado en GBM. La nota 8 (p. 236) estima un uso de margen de 5–20%.

**Mecanismo económico.** El artículo lo atribuye a una sub-reacción inicial y una sobre-reacción tardía: el efecto persiste hasta 12 meses y revierte parcialmente después (p. 228). Los especuladores ganan a costa de los coberturistas, que pagan por transferir riesgo. Hay dos razones por las que no se arbitraría del todo. La primera es el riesgo de reversiones bruscas al terminar una crisis (pérdidas de marzo a mayo de 2009, p. 238). La segunda es la demanda de cobertura. Hay evidencia contraria que se contrasta en la sección 13:

- **Huang, Li, Wang y Zhou (2020), JFE 135(3), 774–794.** Activo por activo hay poca evidencia de TSM, dentro y fuera de muestra. El t de la regresión *pooled* no supera los valores críticos por bootstrap. La estrategia rinde casi lo mismo que una basada en la media histórica.
- **Kim, Tse y Wald (2016), Journal of Financial Markets 30.** El alfa de TSMOM se debe sobre todo al escalamiento por volatilidad. Sin escalar, no es mejor que comprar y mantener.

**Hipótesis (signo y magnitud esperados):**

- **H1, efecto histórico en el mercado de EUA.** Es la parte (a). La regla del artículo (TSMOM-12 largo/corto, volatilidad objetivo de 40%) aplicada al mercado total de EUA de French tiene un Sharpe del exceso, **neto** de costos por defecto, **> 0 con t de Newey-West ≥ 2** en 1927-07 a 2011-12. Magnitud esperada: entre 0.2 y 0.5. No hay cifra del artículo para este instrumento.
- **H1b, ventana del artículo.** La misma regla, **bruta**, tiene Sharpe > 0 en 1985-01 a 2009-12. Es la afirmación de que "los 58 instrumentos son positivos", aplicada al único instrumento replicable aquí.
- **H2, post-publicación en el mercado de EUA.** La misma regla tiene Sharpe neto > 0 en 2012-01 a 2026-07. Se espera más débil que antes, por el decaimiento post-publicación (McLean-Pontiff, 2016).
- **H3, multiactivo con ETFs.** Es la parte (b). La regla del artículo sobre 8 ETFs (promedio igual de sign·40%/σ_i) tiene Sharpe neto **> 0 con t de NW ≥ 2** en 2012-01 a 2026-07. Magnitud esperada: muy por debajo de 1, porque son 8 activos correlacionados y no 58 futuros.
- **H4, versión operable en GBM.** Es la versión sin cortos y sin apalancamiento. La versión solo-largos de TSMOM-12 sobre los 8 ETFs, con volatilidad objetivo de 10% por activo y tope de 1, supera a **1/N rebalanceado mensualmente** en **Sharpe y en drawdown máximo** en 2012-01 a 2026-07, neta de costos GBM. También debe superar a la regla sencilla del mismo tipo: 1/N con filtro de media móvil de 10 meses por activo.

### 2. Criterio de refutación

- **Métrica principal.** Sharpe anualizado del exceso mensual sobre RF (`sharpe` del motor), neto de costos por defecto. Secundarias:
  - t de Newey-West con 6 rezagos de la media del exceso mensual (`herramientas/estadistica.newey_west`).
  - MDD, CAGR y Sortino.
- **Tolerancia.** Solo se exige el mismo signo y la significancia indicada. El artículo no trae la cifra de un instrumento aislado ni la de un universo de 8 ETFs, así que no hay magnitud contra la cual medir. **No se exige** acercarse al Sharpe > 1 del factor de 58 futuros.
- **Estado final** (regla fijada ahora):
  - **Replicado** si se cumplen las tres condiciones: (i) H1b con Sharpe bruto > 0 en 1985–2009; (ii) H1 con Sharpe neto > 0 y t de NW ≥ 2 en 1927-07 a 2011-12; (iii) H3 con Sharpe neto > 0 y t de NW ≥ 2 en 2012-01 a 2026-07.
  - **Replicado con diferencias** si se cumple (i) y al menos uno de (ii) o (iii) tiene Sharpe > 0 pero no cumple la significancia, o si el efecto aparece en unos segmentos y no en otros.
  - **No replicado** si (i) falla (Sharpe bruto ≤ 0 del mercado de EUA en la ventana del artículo) o si (ii) y (iii) tienen ambos Sharpe neto ≤ 0.
- **Refutación de H4 (conclusión operable).** Si la variante solo-largos TSMOM-12 con volatilidad objetivo no supera a 1/N en Sharpe **y** en MDD fuera de muestra, la conclusión es "no agrega valor frente a 1/N". Si no supera a 1/N-SMA10, la conclusión es "no agrega valor frente a la regla sencilla". También se reporta la comparación contra el control 1/N con volatilidad objetivo sin filtro, que separa el efecto del momentum del efecto de escalar por volatilidad.
- **DSR.** Se reporta el DSR con N = número de variantes con `es_prueba=1` del registro, que es 15 por diseño. Si DSR < 0.95, la regla **no** es candidata para dinero, cualquiera que sea el estado de la réplica.

### 3. Datos y licencia

| Serie | Fuente y archivo | Versión / huella | Frecuencia | Condiciones de uso |
|---|---|---|---|---|
| Mercado EUA (Mkt-RF + RF) y RF | French `F-F_Research_Data_Factors_CSV.zip` | `version_crsp` y `sha256` que imprime el script | mensual | Pendiente de verificar |
| Mkt-RF diario (volatilidad ex ante) | French `F-F_Research_Data_Factors_daily_CSV.zip` | `version_crsp` y `sha256` | diaria | Pendiente de verificar |
| SPY, EFA, EEM, TLT, IEF, GLD, DBC, VNQ | Yahoo chart v8 (`yahoo_historia`, adjclose: incluye dividendos y splits) | URL; primer y último dato; `fechas_sin_precio` | mensual (`1mo`) para rendimientos y diaria (`1d`) para la volatilidad | Pendiente de verificar |
| MXN por USD (solo sensibilidad) | FRED `DEXMXUS` | fecha de descarga | diaria | Dominio público según FRED (la serie es de la Fed H.10); se usa solo como referencia |

Los datos crudos no se redistribuyen: el caché está en `.gitignore`.

### 4. Universo

- **(a)** Un solo activo: el mercado total de EUA de French (CRSP, todas las acciones de NYSE, AMEX y NASDAQ ponderadas por valor). No tiene sesgo de supervivencia, pero **no es invertible directamente**. El proxy invertible más cercano sería un ETF del mercado total.
- **(b)** 8 ETFs fijados por la instrucción de la tarea: SPY (S&P 500), EFA (desarrollados ex-EUA), EEM (emergentes), TLT (Tesoros de más de 20 años), IEF (Tesoros de 7 a 10 años), GLD (oro), DBC (materias primas) y VNQ (REITs de EUA).
  - **Sesgo de selección con información de hoy.** Son ETFs grandes que sobrevivieron y se eligieron hoy. No se agrega ni se quita ninguno.
  - **No hay divisas.** El artículo sí las incluye, pero no hay un ETF simple de divisas con historia comparable. Es una diferencia declarada.
  - **Disponibilidad.** Todos existen desde el alta de DBC (febrero de 2006). La muestra común empieza en el primer fin de mes en que los 8 tienen un rendimiento mensual completo y RF existe. Se espera 2006-03-31.
- **Disponibilidad en GBM.** No se verifica aquí que los 8 estén en el SIC. Queda como pendiente de la conclusión operable.

### 5. Fecha de disponibilidad

- **Decisión mensual.** Al cierre del último día del mes t−1 se decide el peso del mes t. El motor (`backtest_senal`) y el motor de cartera de `R02.py` solo entregan a la señal datos hasta t−1: las vistas se llenan después de decidir.
- **Volatilidad ex ante.** La media y la varianza exponenciales se calculan en cada día *d* con rendimientos ≤ *d*. Se entregan como `extras` con fecha *d*, y la señal ve solo *d* ≤ fin del mes t−1. Antes de usarlas, la construcción se prueba con `auditar_constructor` (invariancia de prefijo).
- **RF de French.** Es la T-bill del mes t, conocida al inicio del mes; es el rendimiento del efectivo durante t. La señal solo ve la RF hasta t−1.
- **Ejecución.** Se supone al cierre del mismo día de la señal, igual que en el artículo. El protocolo 6.3 del capítulo 14 pide ejecutar en la apertura siguiente. Esta optimización queda **declarada** y no se corrige (en frecuencia mensual su efecto esperado es chico, pero no está medido).

### 6. Periodo

- **Periodo del artículo:** 1985-01 a 2009-12. Hay además una muestra antigua, 1966–1985.
- **Periodo propio total:**
  - (a) de 1926-07 a 2026-07. Con `min_historia` = 12 meses, el primer mes evaluado es 1927-07 para **todas** las variantes de (a).
  - (b) desde el inicio común de los 8 ETFs (se espera 2006-03) hasta el último mes común con RF (se espera 2026-07). El primer mes evaluado es el decimotercero de la muestra común; se espera 2007-03.
- **Corte único:** 2011-12-31. El artículo estuvo en línea desde el 11-dic-2011.
  - `dentro_muestra` va hasta 2011-12.
  - `fuera_muestra` va de 2012-01 al final. Es la prueba post-publicación y se mira una sola vez.
  - En (b) el tramo dentro de muestra dura solo unos 58 meses (2007-03 a 2011-12). Por eso la prueba relevante de (b) es fuera de muestra.
- **Ventanas de reporte**, fijadas ahora y calculadas sobre las mismas corridas, sin nuevas variantes:
  - (a) 1927-07 a 1984-12, 1985-01 a 2009-12 (la del artículo), 2012-01 a 2026-07 y, además, por décadas.
  - (b) 2012-01 a 2019-12 y 2020-01 a 2026-07 (dos mitades del tramo fuera de muestra).

### 7. Limpieza

Reglas fijadas antes de ver los resultados:

- **French.** Los valores −99.99 y −999 se convierten en faltantes y se omiten; no se espera ninguno. La fuente de la T-bill cambia en 202406 (de Ibbotson a ICE BofA) y no se ajusta. Se registran la versión CRSP y el sha256.
- **Yahoo mensual.** Se usa la barra `1mo` re-etiquetada a fin de mes. Se descarta el mes en curso (`solo_periodos_completos`). Los meses en `fechas_sin_precio` se reportan: el rendimiento siguiente abarca dos meses y se acepta así.
- **Yahoo diaria.** Solo alimenta la volatilidad. Si hay huecos, el rendimiento siguiente abarca dos días y se acepta así.
- **Chequeo cruzado.** Se reporta la diferencia máxima entre el rendimiento mensual `1mo` y el que resulta de los precios diarios a fin de mes. No cambia los datos.
- **Sin cambios después de ver resultados.** No se eliminan valores extremos. Se usa la intersección de fechas entre activos y RF.

### 8. Regla y variantes planeadas

**Definiciones comunes:**

- L ∈ {3, 6, 12} meses.
- Exceso acumulado: `s_L = +1` si Π(1+r_activo) > Π(1+RF) en los últimos L meses visibles; si no, −1. En largo/corto s ∈ {−1, +1}; en solo-largos se usa 1{s = +1}.
- σ = volatilidad anualizada EWMA de rendimientos diarios, con 261 días y δ = 60/61. Se calcula como varianza ponderada normalizada: media exponencial de r² menos el cuadrado de la media exponencial de r, dividido entre el peso acumulado 1 − δ^n. Se exigen al menos 120 días de historia.
- Rebalanceo mensual hacia el peso objetivo, con deriva de pesos entre meses (modelo del motor). No hay bandas de rebalanceo.

**Parte (a): mercado de EUA.** El activo es Mkt-RF + RF mensual de French y el efectivo es RF. σ sale de Mkt-RF diario.

| # | Variante (`es_prueba=1`) | Peso w_t |
|---|---|---|
| 1-3 | `A_ls_vt40_L{3,6,12}` (regla del artículo) | s_L · 0.40/σ, con tope \|w\| ≤ 10 (se reporta cuántos meses toca el tope) |
| 4-6 | `A_lo_L{3,6,12}` (solo largos, sin apalancamiento) | 1{s_L = +1} ∈ {0, 1} |

**Parte (b): 8 ETFs.** N = 8. El efectivo es RF de French. σ_i sale de los rendimientos diarios del ETF (rendimiento total, no exceso; la diferencia en varianza es despreciable).

| # | Variante (`es_prueba=1`) | Peso W_i,t del ETF i |
|---|---|---|
| 7-9 | `B_ls_vt40_L{3,6,12}` (regla del artículo) | s_{i,L} · min(0.40/σ_i, 10) / N. Apalancamiento bruto sin tope de cartera |
| 10-12 | `B_lo_vt10_L{3,6,12}` (operable) | 1{s_{i,L} = +1} · min(1, 0.10/σ_i) / N. Sin cortos ni apalancamiento |
| 13-15 | `B_lo_L{3,6,12}` (operable, sin volatilidad objetivo) | 1{s_{i,L} = +1} / N |

**Referencias.** Se registran con `es_prueba=0` y la nota "referencia": no son candidatas a selección.

- Parte (a):
  - `A_ref_comprar_mantener` (w = 1).
  - `A_ref_efectivo` (w = 0).
  - `A_ref_sma10` (`senal_media_movil(10)`, la regla sencilla del mismo tipo).
  - `A_ref_largo_vt40` (w = 0.40/σ siempre largo: el comparativo "pasivo con igual riesgo" del artículo, tope 10).
- Parte (b):
  - `B_ref_1N` (1/N rebalanceado cada mes).
  - `B_ref_1N_sin_rebalanceo` (1/N comprado al inicio y mantenido: "comprar y mantener" literal).
  - `B_ref_efectivo`.
  - `B_ref_1N_sma10` (1/N con filtro de media de 10 meses por activo; es la regla sencilla del mismo tipo, estilo Faber).
  - `B_ref_1N_vt10` (min(1, 0.10/σ_i)/N siempre largo; es el control del efecto del escalamiento).
  - `B_ref_largo_vt40` (min(0.40/σ_i, 10)/N siempre largo).

**Sensibilidades.** Se registran con `es_prueba=0` y una nota. Es una lista cerrada:

1. Todas las variantes y referencias, con spread "medio" (0.15% por lado).
2. Todas las variantes y referencias, brutas (comisión y spread en 0), para comparar con el artículo.
3. En MXN (con `DEXMXUS`, efectivo en USD convertido): `B_ls_vt40_L12`, `B_lo_vt10_L12`, `B_lo_L12`, `B_ref_1N`, `B_ref_1N_sma10` y `B_ref_1N_vt10`, con costos por defecto.

**Diagnósticos** (solo se reportan):

- El t de NW del exceso mensual.
- La descomposición de las variantes solo-largos en exposición media × prima + covarianza de *timing* (protocolo 6.3, paso 6).
- El número medio de órdenes por mes (activos con |ΔW| > 0), contra `operaciones_max_mes` = 8.
- Los meses en que el tope de apalancamiento está activo.

**Motor de cartera.** `herramientas/backtest.py` modela un solo activo contra efectivo. Para (b), `R02.py` implementa `backtest_cartera`, que:

- Replica exactamente el modelo de costos y de tiempo del motor:
  - w_pre = w·(1+r_i)/(1+r_b).
  - costo = Σ|W_i − W_pre,i|·(comisión + spread).
  - r_neto = r_b − costo·(1+r_b).
- Da a la señal vistas de solo lectura hasta t−1 y aplica `buscar_capturas`.
- Calcula las métricas con `metricas_de_periodos` y registra con `registrar_variante`.

Antes de cualquier corrida con datos reales, el script comprueba que `backtest_cartera`, con un solo activo, reproduce `backtest_senal` con una diferencia menor a 1e-12. Si no, se detiene.

**Exposición, efectivo y moneda.** Todo se mide en USD con efectivo en T-bills (RF de French). El MXN va solo como sensibilidad.

### 9. Costos y comparación simple

- **Costos.**
  - Por defecto: comisión de 0.29% por lado (GBM, 0.25% + IVA: hecho) más spread de 0.05% por lado (supuesto [I]), sobre |ΔW|.
  - Escenario "medio": spread de 0.15%.
  - Bruto: cero.
  - No se modelan el costo de financiar el apalancamiento por encima de RF, el préstamo de títulos para los cortos, el spread cambiario ni los impuestos. **Por eso las variantes `*_ls_vt40` no son implementables en GBM**: requieren cortos y apalancamiento, que el sistema no permite en fase 1 (`apalancamiento.bruto_max_fase_1` = 1.0).
- **Reglas sencillas con idénticas condiciones.** Comprar y mantener (w = 1 en (a); 1/N en (b)), 100% efectivo, SMA10, y el control de volatilidad objetivo sin momentum.

---

## RESULTADOS (se llenan después de correr)

(pendiente)
