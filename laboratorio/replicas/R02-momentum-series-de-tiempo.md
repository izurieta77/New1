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

> Corridas del 2026-09-25 (UTC 05:27 y 05:28). Todas las cifras son las que imprimió `python3 laboratorio/replicas/R02.py`, sin redondear a mano. Rendimientos en USD salvo que se diga MXN. El Sharpe es el del exceso mensual sobre RF anualizado; `nw_t` es el t de Newey-West con 6 rezagos de la media del exceso mensual neto. MDD = drawdown máximo.

### Desviaciones del pre-registro

| Fecha | Qué cambió | Por qué | ¿Invalida el tramo de prueba? |
|---|---|---|---|
| 2026-09-25 | **Primera ejecución: las 81 corridas quedaron registradas y el script falló al imprimir el reporte.** La falla fue una división entre cero en `estadistica.newey_west`: el exceso de `A_ref_efectivo` es idéntico a 0 y su desviación estándar es 0. Se agregó una guarda **solo** en la función de reporte `ventana` (t = NA si el exceso es constante) y se re-ejecutó todo el script. | Error de código del reporte | **No.** No cambian reglas, datos ni corridas. El CSV conserva las dos ejecuciones (486 filas = 2 × 81 corridas × 3 segmentos). Las 243 parejas (variante, parámetros, segmento) son idénticas en cagr, sharpe, mdd, vol_anual, sharpe_periodo, huella_datos, n_periodos y fechas: 0 diferencias. `sharpe_deflactado_de_registro` deduplica por variante + parámetros, así que N sigue en 15 |
| 2026-09-25 | **Aclaración del DSR.** El pre-registro fijó N = 15, pero no qué varianza V de los Sharpes usar. Se reportan dos lecturas: V de las 15 variantes (el valor por defecto de la función) y V por familia (A o B). **Para decidir se aplica el DSR menor.** | Las familias tienen muestras de muy distinta longitud dentro de muestra: 1,014 meses en (a) y 58 en (b). Mezclarlas infla V | No: se toma la lectura más conservadora |
| 2026-09-25 | **Aclaración de "órdenes por mes".** Cuenta los activos con \|ΔW\| > 0 e incluye el rebalanceo de la deriva hacia el peso objetivo, porque el motor rebalancea cada mes. Con las bandas de `rebalanceo` de `parametros.json` habría menos órdenes; eso no se probó. | Definición del diagnóstico | No |

### 10. Variantes probadas

- **Archivo.** `laboratorio/replicas/R02-variantes.csv`: 486 filas, 2 ejecuciones idénticas.
- **Corridas por ejecución: 81.**
  - 15 variantes candidatas y 10 referencias, con 3 escenarios de costo cada una: 75.
  - Más 6 corridas en MXN.
- **Variantes con `es_prueba=1`: 15.** Son 6 de (a) y 9 de (b).
  - Referencias y sensibilidades van con `es_prueba=0` y con nota: "referencia", "sensibilidad: spread medio", "sensibilidad: bruto" y "sensibilidad: MXN".
- **Pruebas fuera del registro:** ninguna corrida de estrategia con datos reales. Solo se corrieron dos pruebas con datos **sintéticos**, sin registrar (`id_replica=None`): la de consistencia del motor de cartera (diferencia máxima 0.000e+00 contra `backtest_senal`, con y sin FX) y la auditoría de la EWMA. Se usa `n_pruebas` = 15.

**Salida de `sharpe_deflactado_de_registro`** (umbral 0.95; SR anualizado):

| Lectura | Segmento | Variante | DSR | ¿Cumple? | N | V por periodo | SR anual | SR0 anual | n_obs | PSR sin deflactar |
|---|---|---|---|---|---|---|---|---|---|---|
| Por defecto: mejor de las 15, V de todas | dentro_muestra | B_lo_vt10_L3 | 0.8831 | No | 15 | 0.008262 | 1.0912 | 0.5575 | 58 | 0.9925 |
| Mejor de la familia A, V de A | dentro_muestra | A_lo_L12 | 0.9731 | Sí | 15 | 0.002143 | 0.5073 | 0.2839 | 1014 | 1.0000 |
| Mejor de la familia B, V de B | dentro_muestra | B_lo_vt10_L3 | 0.9599 | Sí | 15 | 0.002501 | 1.0912 | 0.3067 | 58 | 0.9925 |
| Pre-especificada, V de todas | dentro_muestra | A_ls_vt40_L12 | 0.0234 | No | 15 | 0.008262 | 0.3348 | 0.5575 | 1014 | 0.9986 |
| Pre-especificada, V de todas | dentro_muestra | A_lo_L12 | 0.3322 | No | 15 | 0.008262 | 0.5073 | 0.5575 | 1014 | 1.0000 |
| Pre-especificada, V de todas | dentro_muestra | B_ls_vt40_L12 | 0.6863 | No | 15 | 0.008262 | 0.7887 | 0.5575 | 58 | 0.9511 |
| Pre-especificada, V de todas | dentro_muestra | B_lo_vt10_L12 | 0.7600 | No | 15 | 0.008262 | 0.8863 | 0.5575 | 58 | 0.9715 |
| Pre-especificada, V de todas | dentro_muestra | B_lo_L12 | 0.5276 | No | 15 | 0.008262 | 0.5907 | 0.5575 | 58 | 0.8913 |
| Mejor de la familia A, V de A | fuera_muestra | A_lo_L3 | 0.8822 | No | 15 | 0.004754 | 0.7428 | 0.4229 | 175 | 0.9971 |
| Mejor de la familia B, V de B | fuera_muestra | B_lo_L12 | 0.7264 | No | 15 | 0.004234 | 0.5591 | 0.3991 | 175 | 0.9823 |
| Pre-especificada, V de todas | fuera_muestra | A_ls_vt40_L12 | 0.4293 | No | 15 | 0.004844 | 0.3790 | 0.4269 | 175 | 0.9207 |
| Pre-especificada, V de todas | fuera_muestra | A_lo_L12 | 0.8399 | No | 15 | 0.004844 | 0.7052 | 0.4269 | 175 | 0.9941 |
| Pre-especificada, V de todas | fuera_muestra | B_ls_vt40_L12 | 0.2009 | No | 15 | 0.004844 | 0.2071 | 0.4269 | 175 | 0.7852 |
| Pre-especificada, V de todas | fuera_muestra | B_lo_vt10_L12 | 0.5892 | No | 15 | 0.004844 | 0.4874 | 0.4269 | 175 | 0.9653 |
| Pre-especificada, V de todas | fuera_muestra | B_lo_L12 | 0.6905 | No | 15 | 0.004844 | 0.5591 | 0.4269 | 175 | 0.9823 |

**Lectura conservadora:** ninguna variante alcanza DSR ≥ 0.95 con V de todas las variantes, ni dentro ni fuera de muestra.

- `A_lo_L12` pasa solo con V de su familia (0.9731) y dentro de muestra. Fuera de muestra, las cinco variantes pre-especificadas no pasan con V de todas; la mejor es `A_lo_L12` con 0.8399.
- La mejor variante de (b) dentro de muestra (`B_lo_vt10_L3`, SR 1.09) sale de solo 58 meses. Fuera de muestra su Sharpe cae a 0.2902.

### 11. Resultados

#### 11.1 Parte (a): mercado de EUA, costos por defecto

**Dentro de muestra, 1927-07 a 2011-12 (n = 1014 meses)**

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | rotacion_anual | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| A_ls_vt40_L3 | -0.0838 | 0.5038 | 0.0407 | 0.3354 | 0.0559 | -0.9999 | 1.1256 | 23.9289 | 0.0814 |
| A_ls_vt40_L6 | -0.0053 | 0.5031 | 0.2046 | 1.6646 | 0.2857 | -0.9971 | 1.4992 | 17.0550 | 0.0580 |
| A_ls_vt40_L12 | 0.0641 | 0.4998 | 0.3348 | 2.9707 | 0.4833 | -0.9848 | 1.7135 | 11.8942 | 0.0404 |
| A_lo_L3 | 0.0698 | 0.1321 | 0.3115 | 2.6452 | 0.4553 | -0.5969 | 0.6154 | 2.8283 | 0.0096 |
| A_lo_L6 | 0.0786 | 0.1244 | 0.3890 | 3.1728 | 0.5529 | -0.5675 | 0.6578 | 1.7751 | 0.0060 |
| A_lo_L12 | 0.0953 | 0.1261 | 0.5073 | 4.5870 | 0.7619 | -0.4517 | 0.6824 | 0.8639 | 0.0029 |
| A_ref_comprar_mantener | 0.0947 | 0.1900 | 0.3862 | 3.3739 | 0.5794 | -0.8365 | 1.0000 | 0.0118 | 0.0000 |
| A_ref_efectivo | 0.0358 | 0.0088 | 0.0000 | NA | 0.0000 | -0.0009 | 0.0000 | 0.0000 | 0.0000 |
| A_ref_sma10 | 0.0903 | 0.1278 | 0.4672 | 3.8977 | 0.6870 | -0.4350 | 0.7110 | 1.4674 | 0.0050 |
| A_ref_largo_vt40 | 0.1206 | 0.5003 | 0.4395 | 3.5840 | 0.6433 | -0.9859 | 3.3112 | 6.1137 | 0.0208 |

**Fuera de muestra (post-publicación), 2012-01 a 2026-07 (n = 175 meses)**

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | rotacion_anual | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| A_ls_vt40_L3 | 0.0252 | 0.3757 | 0.2165 | 0.8091 | 0.3055 | -0.7410 | 1.8055 | 15.2021 | 0.0517 |
| A_ls_vt40_L6 | 0.0227 | 0.3781 | 0.2152 | 0.6704 | 0.2929 | -0.8927 | 2.1107 | 10.6769 | 0.0363 |
| A_ls_vt40_L12 | 0.0893 | 0.3757 | 0.3790 | 1.2341 | 0.5494 | -0.8186 | 2.2196 | 8.5735 | 0.0291 |
| A_lo_L3 | 0.0909 | 0.1033 | 0.7428 | 2.7295 | 1.2132 | -0.1838 | 0.7714 | 2.1945 | 0.0075 |
| A_lo_L6 | 0.0826 | 0.1164 | 0.6054 | 2.1287 | 0.8856 | -0.3052 | 0.8114 | 1.4402 | 0.0049 |
| A_lo_L12 | 0.1003 | 0.1248 | 0.7052 | 2.6129 | 1.0822 | -0.2452 | 0.8457 | 0.9601 | 0.0033 |
| A_ref_comprar_mantener | 0.1494 | 0.1452 | 0.9282 | 4.6174 | 1.4968 | -0.2484 | 1.0000 | 0.0000 | 0.0000 |
| A_ref_efectivo | 0.0159 | 0.0055 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| A_ref_sma10 | 0.1030 | 0.1098 | 0.8032 | 3.0275 | 1.2720 | -0.1931 | 0.8400 | 1.5773 | 0.0054 |
| A_ref_largo_vt40 | 0.2843 | 0.3666 | 0.8349 | 3.6439 | 1.2775 | -0.5497 | 2.7996 | 4.5589 | 0.0155 |

**Ventana del artículo, 1985-01 a 2009-12 (n = 300 meses). Arriba neto y abajo bruto (H1b).**

| variante | neto: cagr | neto: sharpe | neto: nw_t | neto: mdd | bruto: cagr | bruto: sharpe | bruto: nw_t | bruto: mdd |
|---|---|---|---|---|---|---|---|---|
| A_ls_vt40_L3 | -0.1156 | -0.1511 | -0.75 | -0.9881 | -0.0416 | 0.0371 | 0.19 | -0.9624 |
| A_ls_vt40_L6 | -0.0276 | 0.0800 | 0.37 | -0.9865 | 0.0295 | 0.2118 | 1.00 | -0.9735 |
| A_ls_vt40_L12 | 0.1226 | 0.4091 | 2.02 | -0.8173 | 0.1586 | 0.4836 | 2.45 | -0.7823 |
| A_lo_L3 | 0.0704 | 0.2832 | 1.34 | -0.2631 | 0.0819 | 0.3817 | 1.85 | -0.2424 |
| A_lo_L6 | 0.0866 | 0.4074 | 1.96 | -0.2424 | 0.0941 | 0.4673 | 2.28 | -0.2424 |
| A_lo_L12 | 0.1043 | 0.5315 | 2.79 | -0.2424 | 0.1071 | 0.5530 | 2.93 | -0.2424 |
| A_ref_comprar_mantener | 0.1046 | 0.4375 | 2.07 | -0.5031 | 0.1046 | 0.4375 | 2.07 | -0.5031 |
| A_ref_sma10 | 0.1043 | 0.5304 | 2.61 | -0.2484 | 0.1091 | 0.5674 | 2.84 | -0.2433 |
| A_ref_largo_vt40 | 0.1754 | 0.5212 | 2.57 | -0.7417 | 0.1938 | 0.5580 | 2.75 | -0.7351 |

**Pre-artículo, 1927-07 a 1984-12 (n = 690), neto:**

| variante | sharpe | nw_t | mdd |
|---|---|---|---|
| A_ls_vt40_L12 | 0.3096 | 2.26 | −0.9848 |
| A_lo_L12 | 0.4966 | 3.59 | −0.4517 |
| A_ref_comprar_mantener | 0.3666 | 2.63 | −0.8365 |
| A_ref_sma10 | 0.4619 | 3.10 | −0.4350 |
| A_ref_largo_vt40 | 0.4153 | 2.72 | −0.9859 |

> **CAGR y MDD de las variantes `*_vt40`.** Con volatilidad objetivo de 40% sobre un solo activo, el peso medio es |w| = 3.236 y el máximo 8.320. El peor mes neto fue −86.01% (mayo de 1940). Su CAGR y su MDD dependen de esa escala: el artículo la llama "inconsequential" para el Sharpe, pero no lo es para la riqueza. En esas variantes solo el Sharpe y el t son comparables. El tope |w| ≤ 10 nunca se activó en (a).

#### 11.2 Parte (b): 8 ETFs, costos por defecto

Muestra común de 2006-03-31 a 2026-07-31 (245 meses). El primer mes evaluado es 2007-03.

**Dentro de muestra, 2007-03 a 2011-12 (n = 58 meses)**

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | rotacion_anual | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| B_ls_vt40_L3 | 0.1726 | 0.2024 | 0.8299 | 2.1053 | 1.5613 | -0.1725 | 0.6259 | 14.3560 | 0.0488 |
| B_ls_vt40_L6 | 0.0942 | 0.1759 | 0.5359 | 1.3482 | 0.8612 | -0.2017 | 0.7708 | 11.6324 | 0.0396 |
| B_ls_vt40_L12 | 0.1381 | 0.1685 | 0.7887 | 1.6059 | 1.3004 | -0.2575 | 1.4612 | 7.4379 | 0.0253 |
| B_lo_vt10_L3 | 0.0515 | 0.0359 | 1.0912 | 2.6752 | 2.2183 | -0.0341 | 0.3351 | 1.5628 | 0.0053 |
| B_lo_vt10_L6 | 0.0408 | 0.0322 | 0.9157 | 2.5942 | 1.6682 | -0.0241 | 0.3541 | 1.3683 | 0.0047 |
| B_lo_vt10_L12 | 0.0456 | 0.0386 | 0.8863 | 2.3384 | 1.5898 | -0.0261 | 0.4230 | 0.9281 | 0.0032 |
| B_lo_L3 | 0.0874 | 0.0803 | 0.9385 | 2.1249 | 1.6934 | -0.1107 | 0.6056 | 2.6471 | 0.0090 |
| B_lo_L6 | 0.0737 | 0.0697 | 0.8938 | 2.3087 | 1.6541 | -0.0486 | 0.6379 | 2.1586 | 0.0073 |
| B_lo_L12 | 0.0605 | 0.0866 | 0.5907 | 1.5587 | 0.9287 | -0.0916 | 0.7177 | 1.3707 | 0.0047 |
| B_ref_1N | 0.0566 | 0.1507 | 0.3663 | 0.6810 | 0.5088 | -0.3457 | 1.0000 | 0.6665 | 0.0023 |
| B_ref_1N_sin_rebalanceo | 0.0538 | 0.1363 | 0.3703 | 0.7136 | 0.5022 | -0.3011 | 1.0000 | 0.2067 | 0.0007 |
| B_ref_efectivo | 0.0115 | 0.0049 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| B_ref_1N_sma10 | 0.0702 | 0.0764 | 0.7781 | 1.7509 | 1.3948 | -0.0843 | 0.6853 | 1.9498 | 0.0066 |
| B_ref_1N_vt10 | 0.0460 | 0.0481 | 0.7201 | 1.4728 | 1.1259 | -0.0822 | 0.5216 | 0.5589 | 0.0019 |
| B_ref_largo_vt40 | 0.1475 | 0.1945 | 0.7487 | 1.5092 | 1.1727 | -0.3163 | 2.2772 | 3.2219 | 0.0110 |

**Fuera de muestra (post-publicación), 2012-01 a 2026-07 (n = 175 meses). Es el tramo de prueba, mirado una sola vez.**

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | rotacion_anual | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| B_ls_vt40_L3 | -0.0329 | 0.2057 | -0.1380 | -0.5639 | -0.1996 | -0.5866 | 0.6200 | 21.8126 | 0.0742 |
| B_ls_vt40_L6 | 0.0025 | 0.1967 | 0.0309 | 0.1203 | 0.0437 | -0.4073 | 0.7573 | 16.1016 | 0.0547 |
| B_ls_vt40_L12 | 0.0380 | 0.1920 | 0.2071 | 0.8764 | 0.3103 | -0.4532 | 0.6363 | 11.7637 | 0.0400 |
| B_lo_vt10_L3 | 0.0257 | 0.0356 | 0.2902 | 1.2582 | 0.4126 | -0.0711 | 0.4208 | 2.3175 | 0.0079 |
| B_lo_vt10_L6 | 0.0298 | 0.0381 | 0.3772 | 1.5768 | 0.5573 | -0.0521 | 0.4332 | 1.7606 | 0.0060 |
| B_lo_vt10_L12 | 0.0337 | 0.0375 | 0.4874 | 2.0844 | 0.7416 | -0.0669 | 0.4229 | 1.2711 | 0.0043 |
| B_lo_L3 | 0.0366 | 0.0545 | 0.3987 | 1.5966 | 0.5987 | -0.1096 | 0.5893 | 3.0525 | 0.0104 |
| B_lo_L6 | 0.0388 | 0.0562 | 0.4260 | 1.6468 | 0.6547 | -0.0763 | 0.5979 | 2.3033 | 0.0078 |
| B_lo_L12 | 0.0454 | 0.0540 | 0.5591 | 2.2562 | 0.8843 | -0.0852 | 0.5893 | 1.5500 | 0.0053 |
| B_ref_1N | 0.0633 | 0.0928 | 0.5406 | 2.3735 | 0.8163 | -0.1922 | 1.0000 | 0.2992 | 0.0010 |
| B_ref_1N_sin_rebalanceo | 0.0652 | 0.0940 | 0.5550 | 2.4028 | 0.8396 | -0.2150 | 1.0000 | 0.0000 | 0.0000 |
| B_ref_efectivo | 0.0159 | 0.0055 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| B_ref_1N_sma10 | 0.0421 | 0.0552 | 0.4906 | 2.0041 | 0.7386 | -0.0696 | 0.6436 | 2.1158 | 0.0072 |
| B_ref_1N_vt10 | 0.0393 | 0.0563 | 0.4373 | 1.8876 | 0.6302 | -0.1108 | 0.6997 | 0.5042 | 0.0017 |
| B_ref_largo_vt40 | 0.0895 | 0.2338 | 0.4192 | 1.8165 | 0.6017 | -0.4395 | 3.1966 | 3.4181 | 0.0116 |

#### 11.3 Veredicto por hipótesis (criterios de la sección 2)

| Hipótesis | Criterio pre-registrado | Resultado | Veredicto |
|---|---|---|---|
| H1b (ventana del artículo) | `A_ls_vt40_L12` bruto, Sharpe > 0 en 1985–2009 | Sharpe 0.4836, t 2.45 | **Cumple** (condición i) |
| H1 (historia de EUA) | `A_ls_vt40_L12` neto, Sharpe > 0 y t ≥ 2 en 1927-07 a 2011-12 | Sharpe 0.3348, t 2.9707 | **Cumple** (condición ii) |
| H2 (EUA post-publicación) | Mismo, Sharpe neto > 0 en 2012-01 a 2026-07 | Sharpe 0.3790, t 1.2341 | Cumple el signo, **no** es significativo. Queda debajo de comprar y mantener (0.9282) y del largo con volatilidad objetivo (0.8349) |
| H3 (8 ETFs post-publicación) | `B_ls_vt40_L12` neto, Sharpe > 0 y t ≥ 2 en 2012-01 a 2026-07 | Sharpe 0.2071, t 0.8764 | Signo positivo, **no cumple la significancia** (condición iii) |
| H4 (operable) | `B_lo_vt10_L12` supera a `B_ref_1N` en Sharpe **y** MDD fuera de muestra, y también a `B_ref_1N_sma10` | Contra 1/N: Sharpe 0.4874 frente a 0.5406 (peor) y MDD −0.0669 frente a −0.1922 (mejor). Contra 1/N-SMA10: Sharpe 0.4874 frente a 0.4906 (peor) y MDD −0.0669 frente a −0.0696 (mejor) | **Refutada**: no agrega valor frente a 1/N ni frente a la regla sencilla |

**Diferencias frente a la cifra del artículo.**

- **Por instrumento.** Para el S&P 500 no hay cifra en el texto (Fig. 2): solo se verifica el signo, que coincide.
- **Portafolio diversificado.** El artículo reporta un Sharpe "greater than one" para 58 futuros, bruto, en 1985–2009. La réplica con 8 ETFs da:
  - 0.9386 bruto en 2007–2011, con 58 meses que incluyen 2008.
  - 0.5329 bruto en todo 2007–2026.
  - 0.4159 bruto en 2012–2026.
  - 0.2071 neto en 2012–2026.
- **Magnitud.** No es comparable (otro universo y otro periodo). La caída hacia el periodo post-publicación sí es un resultado.

### 12. Sensibilidad

**Costos** (Sharpe; columnas: por defecto 0.34% por lado / spread medio 0.44% por lado / bruto 0):

| variante | dentro: defecto | dentro: medio | dentro: bruto | fuera: defecto | fuera: medio | fuera: bruto |
|---|---|---|---|---|---|---|
| A_ls_vt40_L3 | 0.0407 | -0.0072 | 0.2028 | 0.2165 | 0.1755 | 0.3548 |
| A_ls_vt40_L6 | 0.2046 | 0.1703 | 0.3205 | 0.2152 | 0.1872 | 0.3107 |
| A_ls_vt40_L12 | 0.3348 | 0.3104 | 0.4167 | 0.3790 | 0.3559 | 0.4573 |
| A_lo_L3 | 0.3115 | 0.2900 | 0.3842 | 0.7428 | 0.7203 | 0.8191 |
| A_lo_L6 | 0.3890 | 0.3746 | 0.4379 | 0.6054 | 0.5929 | 0.6474 |
| A_lo_L12 | 0.5073 | 0.5005 | 0.5301 | 0.7052 | 0.6975 | 0.7314 |
| A_ref_comprar_mantener | 0.3862 | 0.3862 | 0.3864 | 0.9282 | 0.9282 | 0.9282 |
| A_ref_sma10 | 0.4672 | 0.4555 | 0.5067 | 0.8032 | 0.7881 | 0.8541 |
| A_ref_largo_vt40 | 0.4395 | 0.4272 | 0.4812 | 0.8349 | 0.8224 | 0.8774 |
| B_ls_vt40_L3 | 0.8299 | 0.7591 | 1.0643 | -0.1380 | -0.2450 | 0.2231 |
| B_ls_vt40_L6 | 0.5359 | 0.4681 | 0.7654 | 0.0309 | -0.0511 | 0.3102 |
| B_ls_vt40_L12 | 0.7887 | 0.7442 | 0.9386 | 0.2071 | 0.1453 | 0.4159 |
| B_lo_vt10_L3 | 1.0912 | 1.0498 | 1.2296 | 0.2902 | 0.2240 | 0.5149 |
| B_lo_vt10_L6 | 0.9157 | 0.8703 | 1.0708 | 0.3772 | 0.3304 | 0.5361 |
| B_lo_vt10_L12 | 0.8863 | 0.8623 | 0.9674 | 0.4874 | 0.4531 | 0.6036 |
| B_lo_L3 | 0.9385 | 0.9072 | 1.0432 | 0.3987 | 0.3423 | 0.5894 |
| B_lo_L6 | 0.8938 | 0.8610 | 1.0055 | 0.4260 | 0.3847 | 0.5657 |
| B_lo_L12 | 0.5907 | 0.5753 | 0.6426 | 0.5591 | 0.5301 | 0.6573 |
| B_ref_1N | 0.3663 | 0.3619 | 0.3814 | 0.5406 | 0.5373 | 0.5515 |
| B_ref_1N_sin_rebalanceo | 0.3703 | 0.3688 | 0.3756 | 0.5550 | 0.5550 | 0.5550 |
| B_ref_1N_sma10 | 0.7781 | 0.7515 | 0.8689 | 0.4906 | 0.4521 | 0.6211 |
| B_ref_1N_vt10 | 0.7201 | 0.7077 | 0.7618 | 0.4373 | 0.4282 | 0.4682 |
| B_ref_largo_vt40 | 0.7487 | 0.7312 | 0.8082 | 0.4192 | 0.4045 | 0.4690 |

- **Costos en las variantes largo/corto.** Pesan mucho: rotación anual de 8.6 a 23.9 veces el capital y costo anual de 2.9% a 8.1%. Por ejemplo, `B_ls_vt40_L3` pasa de 0.2231 bruto a −0.1380 neto fuera de muestra.
- **Costos en las variantes solo-largos.** Cuestan de 0.29% a 1.04% al año. La costo-sensibilidad no cambia ninguna comparación relevante.
- **Sin costos, H4 sigue fallando.** Brutas, `B_lo_vt10_L12` da 0.6036 frente a 0.5515 de 1/N y 0.6211 de 1/N-SMA10.

**Moneda (MXN con DEXMXUS; efectivo = T-bill en USD convertida; costos por defecto), fuera de muestra 2012-01 a 2026-07:**

| variante | cagr | vol_anual | sharpe | nw_t | mdd | exposicion_media |
|---|---|---|---|---|---|---|
| B_ls_vt40_L12 | 0.0535 | 0.2324 | 0.2119 | 0.9015 | -0.4343 | 0.6363 |
| B_lo_vt10_L12 | 0.0492 | 0.1084 | 0.4410 | 1.8869 | -0.2464 | 0.4229 |
| B_lo_L12 | 0.0610 | 0.1058 | 0.5082 | 2.0612 | -0.2171 | 0.5893 |
| B_ref_1N | 0.0793 | 0.1016 | 0.4739 | 2.0938 | -0.2720 | 1.0000 |
| B_ref_1N_sma10 | 0.0577 | 0.1117 | 0.4509 | 1.8513 | -0.2267 | 0.6436 |
| B_ref_1N_vt10 | 0.0549 | 0.0989 | 0.3722 | 1.5995 | -0.2343 | 0.6997 |

En MXN la ventaja de drawdown del filtro casi desaparece. `B_lo_vt10_L12` tiene un MDD de −24.64% frente a −27.20% de 1/N, cuando en USD era −6.69% frente a −19.22%. El tipo de cambio domina la volatilidad. En MXN, H4 también falla en Sharpe (0.4410 frente a 0.4739).

**Subperiodos de la parte (a), por décadas** (Sharpe neto con costos por defecto; en la década de 1920 solo hay 30 meses):

| década | A_ls_vt40_L12 | A_lo_L12 | A_ref_comprar_mantener |
|---|---|---|---|
| 1920s | 1.0032 | 0.5450 | 0.5737 |
| 1930s | 0.3507 | 0.4462 | 0.1512 |
| 1940s | 0.3680 | 0.5425 | 0.6426 |
| 1950s | 0.7354 | 1.2606 | 1.4019 |
| 1960s | -0.0359 | 0.2750 | 0.3900 |
| 1970s | 0.1910 | 0.2499 | 0.0693 |
| 1980s | 0.0745 | 0.3533 | 0.5071 |
| 1990s | 0.4030 | 0.7572 | 0.9267 |
| 2000s | 0.5014 | 0.2686 | -0.1022 |
| 2010s | 0.5018 | 0.7397 | 1.0142 |
| 2020s | 0.2188 | 0.5910 | 0.7299 |

- `A_lo_L12` supera a comprar y mantener en Sharpe solo en las décadas de 1930, 1970 y 2000, es decir, en los mercados bajistas largos.
- Sus MDD por década siempre son menores o iguales: por ejemplo, −32.30% frente a −79.37% en los treinta y −16.51% frente a −50.31% en los dos mil.

**Mitades del tramo fuera de muestra de la parte (b)** (Sharpe neto; MDD entre paréntesis):

| variante | 2012–2019 | 2020–2026-07 |
|---|---|---|
| B_ls_vt40_L12 | 0.1756 (−0.4532) | 0.2492 (−0.2705) |
| B_lo_vt10_L12 | 0.5033 (−0.0669) | 0.4657 (−0.0285) |
| B_lo_L12 | 0.5326 (−0.0852) | 0.5899 (−0.0617) |
| B_ref_1N | 0.6133 (−0.1185) | 0.5031 (−0.1922) |
| B_ref_1N_sma10 | 0.3694 (−0.0696) | 0.6078 (−0.0599) |
| B_ref_1N_vt10 | 0.5638 (−0.0806) | 0.3251 (−0.1108) |

**Descomposición de las variantes solo-largos** (bruta, anualizada ×12): exposición media × prima + covarianza de *timing*.

| variante | dentro: exp × prima | dentro: timing | fuera: exp × prima | fuera: timing |
|---|---|---|---|---|
| A_lo_L3 | 0.0453 | 0.0057 | 0.1039 | -0.0196 |
| A_lo_L6 | 0.0484 | 0.0062 | 0.1093 | -0.0338 |
| A_lo_L12 | 0.0502 | 0.0169 | 0.1139 | -0.0227 |
| A_ref_sma10 | 0.0523 | 0.0125 | 0.1132 | -0.0192 |
| B_lo_L3 | 0.0386 | 0.0464 | 0.0337 | -0.0016 |
| B_lo_L6 | 0.0411 | 0.0286 | 0.0347 | -0.0030 |
| B_lo_L12 | 0.0473 | 0.0085 | 0.0358 | -0.0004 |
| B_lo_vt10_L3 | 0.0232 | 0.0216 | 0.0230 | -0.0049 |
| B_lo_vt10_L6 | 0.0242 | 0.0096 | 0.0242 | -0.0039 |
| B_lo_vt10_L12 | 0.0295 | 0.0076 | 0.0249 | -0.0025 |
| B_ref_1N_sma10 | 0.0455 | 0.0206 | 0.0368 | -0.0026 |
| B_ref_1N_vt10 | 0.0342 | 0.0025 | 0.0333 | -0.0072 |

**Fuera de muestra, la covarianza de *timing* es negativa en todas las variantes solo-largos.** Lo que protegen esas reglas después de 2012 viene de estar menos invertidas, no de acertar el momento. Dentro de muestra el *timing* fue positivo (+1.69% anual en `A_lo_L12`).

**Otros diagnósticos:**

- **Apalancamiento de (b).** `B_ls_vt40_*` y `B_ref_largo_vt40` tienen una exposición bruta media de 2.968, con máximo 5.090. El tope de 10/N se activó en 9 activo-meses.
- **Órdenes por mes** (incluyen el rebalanceo de la deriva):
  - `B_lo_*` y `B_lo_vt10_*`: entre 5.19 y 6.07.
  - `B_ls_vt40_*`, `B_ref_1N` y `B_ref_1N_vt10`: 8.00.
  - Ningún mes supera 8 órdenes (`operaciones_max_mes`).
- **Calidad de los datos:**
  - La diferencia máxima entre el rendimiento `1mo` y el de precios diarios a fin de mes fue ≤ 2.36e-06.
  - `fechas_sin_precio` diarias: solo el 2026-09-22 en EFA, EEM, IEF, DBC y VNQ, fuera de la muestra.
  - No hubo faltantes en French.

### 13. Diferencia frente al artículo

| Aspecto | Artículo | Réplica | ¿Explica la diferencia? |
|---|---|---|---|
| Datos / versión | 58 futuros y forwards (24 materias primas, 12 divisas, 9 índices accionarios, 13 bonos); rendimientos en exceso de futuros | (a) Mercado total de EUA de French, CRSP 202607, rendimiento total de contado. (b) 8 ETFs de Yahoo (adjclose), sin divisas | Sí: universo mucho menos diverso. El artículo atribuye buena parte del Sharpe > 1 a la diversificación entre clases de activos |
| Periodo | 1985-01 a 2009-12 (y 1966–1985 como muestra antigua) | (a) 1927-07 a 2026-07. (b) 2007-03 a 2026-07 | Parcial: la ventana 1985–2009 de (a) coincide en el tiempo, pero es un solo instrumento |
| Costos | Brutos (sin costos de transacción) | Netos de comisión GBM de 0.29% más spread de 0.05% por lado, más la sensibilidad bruta | Sí: en las variantes largo/corto los costos restan de 0.05 a 0.36 de Sharpe |
| Regla | sign(r_{t−12,t}) · 40%/σ_{t−1}, EWMA de 60 días de centro de masa y ×261 | Igual. Tres diferencias: el exceso se calcula como cociente compuesto contra RF; la σ de los ETFs usa rendimiento total diario; hay un tope de \|w\| ≤ 10 (inactivo en (a) y activo en 9 activo-meses en (b)) | No material para el signo; no medido |
| Métrica | t del alfa contra MSCI World, bonos, GSCI, SMB, HML y UMD (Tabla 2), y Sharpe | Sharpe del exceso y t de Newey-West de la media del exceso. **No se estimó el alfa por factores** | Sí: un t de la media no es un t del alfa. Pendiente |
| Comparación con el largo pasivo | "Positive alpha in 90% of the cases" frente a siempre largo con la misma escala (p. 236) | En EUA el Sharpe de TSMOM-12 es **menor** que el del largo con volatilidad objetivo en las tres ventanas: 1927–2011 da 0.3348 frente a 0.4395; 1985–2009 bruto da 0.4836 frente a 0.5580; 2012–2026 da 0.3790 frente a 0.8349. En (b), fuera de muestra y bruto: 0.4159 frente a 0.4690 | Es coherente con Kim-Tse-Wald (2016) y Huang et al. (2020). Aquí el signo no mejoró sobre el largo escalado por volatilidad en el Sharpe. El alfa por regresión no se calculó |
| Horizonte | En índices accionarios, t de 1.48 (k = 3), 3.50 (k = 6) y 3.77 (k = 12), con h = 1 | En EUA, bruto 1985–2009, t de 0.19 (L3), 1.00 (L6) y 2.45 (L12) | Mismo orden: el horizonte de 3 meses es el más débil y el de 12 el más fuerte. Magnitudes menores (un instrumento contra nueve) |

### 14. Conclusiones permitidas

Alcance: USD, costos GBM declarados (el spread es un supuesto), frecuencia mensual, ejecución al cierre de la señal.

1. **El efecto histórico se reproduce en el mercado de EUA.** La regla de MOP (TSMOM-12, largo/corto, 40%/σ) tiene un Sharpe neto de 0.3348 (t = 2.97) en 1927–2011. En la ventana del artículo, bruto, es 0.4836 (t = 2.45). Coincide en signo con la afirmación de que los 58 instrumentos son positivos, para el único instrumento replicable aquí.
2. **El orden de horizontes se reproduce.** 12 meses > 6 > 3 en (a), dentro de muestra y en la ventana del artículo, con L3 cerca de 0 o negativo neto. Coincide con la Tabla 2, panel C.
3. **Después de la publicación (2012-01 a 2026-07) el efecto se debilita y deja de ser significativo.** En EUA el Sharpe es 0.3790 (t 1.23). En los 8 ETFs es 0.2071 (t 0.88), y L3 queda negativo (−0.1380). En los dos casos la regla del artículo queda **debajo** del largo pasivo y del 1/N.
4. **La versión largo/corto no supera al largo escalado por volatilidad** en Sharpe en ninguna ventana de EUA ni fuera de muestra en (b). En estos datos el signo del momentum no agregó Sharpe sobre el escalamiento.
5. **Solo-largos en EUA (`A_lo_L12`):**
   - En 1927–2011 tuvo mayor Sharpe (0.5073 frente a 0.3862) y mucho menor MDD (−45.17% frente a −83.65%) que comprar y mantener, neto de costos GBM.
   - En 2012–2026 tuvo menor Sharpe (0.7052 frente a 0.9282) y un MDD casi igual (−24.52% frente a −24.84%).
   - En 2012–2026 perdió contra SMA10 en Sharpe (0.8032) y en MDD (−19.31%).
6. **Solo-largos multiactivo (`B_lo_vt10_L12`, pre-registrada como operable), fuera de muestra:**
   - Tiene MDD menor que 1/N (−6.69% frente a −19.22%), pero Sharpe menor (0.4874 frente a 0.5406) y CAGR de alrededor de la mitad (3.37% frente a 6.33%). La exposición media es de 0.42.
   - **No supera** a 1/N ni a 1/N-SMA10 en el criterio doble.
   - Sí supera al control 1/N con volatilidad objetivo y sin filtro (0.4373; −11.08%).
7. **Fuera de muestra, la reducción de drawdown de las reglas solo-largos se explica por menor exposición.** La covarianza de *timing* es negativa en todas.
8. **Ninguna variante alcanza DSR ≥ 0.95** en la lectura conservadora (N = 15, V de todas).

### 15. Conclusiones que NO se sostienen

- "TSMOM tiene un Sharpe mayor que 1": esa cifra es de 58 futuros diversificados, brutos, en 1985–2009. Con 8 ETFs y costos GBM, fuera de muestra, el Sharpe fue 0.21.
- "TSMOM funciona igual después de su publicación": fuera de muestra ninguna variante largo/corto es significativa.
- "El filtro TSMOM-12 mejora el rendimiento ajustado por riesgo de un portafolio 1/N de ETFs": no lo hizo en 2012–2026 (criterio doble), ni en USD ni en MXN.
- "TSMOM-12 es mejor filtro que la media de 10 meses": fuera de muestra no lo fue en EUA (pierde en Sharpe y MDD) ni en (b), donde hubo un empate técnico.
- "Reduce el drawdown en pesos": en MXN la reducción fue de −27.20% a −24.64%, muy inferior a la reducción en USD.
- "Hay alfa por factores": no se estimó la regresión contra MSCI World, bonos, GSCI, SMB, HML y UMD.
- "La réplica prueba que el efecto desapareció": los intervalos post-2012 son amplios. Con 175 meses, un Sharpe verdadero de 0.3 a 0.4 no se distingue de cero.
- "La variante con mejor Sharpe fuera de muestra (`B_lo_L12`, 0.5591) es la buena": elegirla mirando el tramo de prueba es selección en el tramo de prueba. Además su DSR es 0.6905 y su ventaja sobre 1/N (0.5406) es mínima.
- Cualquier afirmación sobre dinero real, ejecución en GBM (disponibilidad de los 8 ETFs en el SIC, fracciones, spread cambiario) o impuestos.

### 16. Estado y reproducción

- **Estado: Replicado con diferencias.** La regla de la sección 2 da este resultado:
  - (i) se cumple: Sharpe bruto 0.4836 > 0 en 1985–2009.
  - (ii) se cumple: Sharpe neto 0.3348, t 2.97 en 1927–2011.
  - (iii) no cumple la significancia: Sharpe neto 0.2071 > 0, pero t 0.88 < 2 en 2012–2026 con 8 ETFs.
  - Además, el efecto es débil o nulo en el tramo post-publicación.
- **Estado del concepto "momentum de series de tiempo":** Replicado con diferencias, por esta ficha.
- **Pendientes:**
  - Estimar el alfa por factores, como la Tabla 3.
  - Probar un universo con divisas o futuros.
  - Ejecutar en la apertura siguiente.
  - Usar CETES como efectivo en MXN.
  - Hacer la revisión independiente (`auditor-de-replicas`).
  - Verificar las condiciones de uso de French y Yahoo.
- **Comando:** `python3 laboratorio/replicas/R02.py` desde `/home/user/New1`. Tarda unos 7 s con caché y agrega 81 corridas al CSV.
- **Huellas:**
  - `huella_datos`: (a) `e85ac74d630dff95`; (b) USD `0e6d3baabe3fe595`; (b) MXN `b25e21ccd88eba01`.
  - French mensual (CRSP 202607): sha256 `b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb`.
  - French diario (CRSP 202607): sha256 `1916d331c2c51d2aee3d00215897d2b8e5995cb387f1f4569ba46bff5fb049a8`.
  - Yahoo: descarga del 2026-09-25, sin huella propia. Una re-ejecución puede cambiar si Yahoo re-ajusta el adjclose.
- **Fecha de la corrida final:** 2026-09-25 (segunda ejecución, UTC 05:28).

### 17. Conclusión operable

Ninguna regla de esta réplica es candidata para dinero:

- DSR < 0.95 en la lectura conservadora.
- No supera a la regla sencilla fuera de muestra.
- La versión del artículo requiere cortos y apalancamiento, que están fuera de `apalancamiento.bruto_max_fase_1` = 1.0.

No se modificó `config/parametros.json`.

1. **Se modifica el indicador #3 del capítulo 14 (§6.6), "Signo del rendimiento de 12 meses (TSMOM): filtro y diversificador multiactivo, grado B".**
   - **Se confirma como filtro de drawdown histórico:** en EUA 1927–2011 bajó el MDD de −83.65% a −45.17% con mayor Sharpe, neto de costos GBM.
   - **No se confirma como fuente de rendimiento ajustado por riesgo después de 2012.** En EUA perdió contra comprar y mantener y contra SMA10. En los 8 ETFs no superó a 1/N ni a 1/N-SMA10, y la covarianza de *timing* fue negativa.
   - **Propuesta para el autor del capítulo** (no aplicada): bajar el rol "diversificador multiactivo" a grado C, porque no mostró valor neto post-publicación en ETFs, y dejar "filtro de drawdown" en B, advirtiendo que su efecto viene de reducir la exposición.
2. **Regla R1 (filtro de SMA de 10 meses): se mantiene.** R02 no da razón para sustituirla por TSMOM-12. SMA10 fue igual o mejor fuera de muestra en EUA (Sharpe 0.8032 frente a 0.7052; MDD −19.31% frente a −24.52%). En (b) quedaron empatadas.
3. **Se descarta para el sistema la versión largo/corto con 40%/σ (la del artículo).**
   - Fuera de muestra, neta de costos GBM, da Sharpe 0.2071 (t 0.88) en ETFs y 0.3790 (t 1.23) en EUA.
   - Con 3 meses es negativa en ETFs.
   - Rota de 8.6 a 23.9 veces el capital al año.
   - Además no es implementable en fase 1.
4. **Tensión con el objetivo del sistema.** El objetivo es maximizar el CAGR en MXN sujeto al drawdown. En MXN, la versión solo-largos con volatilidad objetivo redujo poco el drawdown (−24.64% frente a −27.20%) y sacrificó CAGR (4.92% frente a 7.93%). **No se recomienda usar TSMOM-12 multiactivo como núcleo del portafolio en MXN** con la evidencia actual.
5. **Fuera del alcance de R02:** R2 (`filtro_apalancados`, media de 200 días más VIX, diaria, sobre ETFs apalancados). R02 ni lo confirma ni lo descarta.
