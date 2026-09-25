# Réplica R08: el peso y las acciones de EUA para un inversionista que mide en pesos (cobertura natural del dólar)

> Fase 0: formación. Esta ficha no recomienda inversiones. Las secciones 1 a 9 son el pre-registro. Se escribieron el 2026-09-25 (≈06:40 UTC), antes de calcular cualquier rendimiento, correlación, volatilidad, caída o Sharpe con los datos de esta réplica. No se editan después. Cualquier cambio posterior va a "Desviaciones del pre-registro", con fecha.

| Campo | Valor |
|---|---|
| ID | `R08` (registro: `laboratorio/replicas/R08-variantes.csv`; script: `laboratorio/replicas/R08.py`; datos congelados: `laboratorio/replicas/R08-datos/`) |
| Hallazgo replicado | **Hallazgo del sistema:** `conocimiento/16-macro-global-divisas-y-el-peso.md` §5.4 ("La cobertura natural: el dólar como seguro del mexicano"), §6.2 regla 4 y §6.4. Son cálculos propios del capítulo, **sin script en el laboratorio**, hechos con el índice de **precio** `^GSPC` y FRED `DEXMXUS` |
| Artículo de referencia (mecanismo) | Campbell, J. Y., Serfaty-de Medeiros, K. y Viceira, L. M. (2010). "Global Currency Hedging". *The Journal of Finance* 65(1): 87-121, febrero de 2010. doi:10.1111/j.1540-6261.2009.01524.x. Versión leída: NBER Working Paper 13088 (mayo de 2007, revisada en enero de 2009), texto completo en https://www.nber.org/system/files/working_papers/w13088/w13088.pdf. Cita y resumen verificados con WebSearch y WebFetch el 2026-09-25 (páginas del NBER, Wiley y RePEc). La versión publicada en la revista no se leyó (de pago): las cifras de abajo son de la versión NBER revisada de 2009 |
| Fecha de publicación (primera versión pública) | NBER WP 13088, mayo de 2007. Revista: febrero de 2010 |
| Pre-registro escrito el | 2026-09-25, antes de cualquier corrida con datos |
| Responsable | Claude (laboratorio del sistema). Revisión independiente pendiente (`auditor-de-replicas`) |
| Estado | **No replicado** (criterio pre-registrado: H4 refutada en la muestra completa 1994-2026; H1, H2, H3 y H6 fuera de muestra sí se cumplen). Ver §16 |

**Conocimiento previo declarado.** Este pre-registro no es ciego. Antes de escribirlo ya conocía:

1. Las cifras del capítulo 16 §5.4 que se transcriben en la sección 1 (correlaciones, volatilidades, caídas, episodios y CAGR con `^GSPC` precio × `DEXMXUS`).
2. Las cifras de V04 (`replicas/V04-benchmarks-en-pesos-y-sma10-senal-mxn/README.md`, puntos 1 y 4 del resumen): con SPY `adjclose` × DEXMXUS, la caída diaria **dentro de 2008** fue −47.6% en USD contra −34.9% en MXN, y la caída mensual de la crisis −50.8% contra −31.2%. El S&P TR en MXN rindió 13.97% anual del 31-dic-2007 al 31-ago-2026.
3. La tabla VII de Campbell et al. (sección 1).
4. Para comprobar acceso a datos (no resultados) vi solo el rango de fechas y el número de observaciones de: FRED `DEXMXUS` (1993-11-08 a 2026-09-18, 8239 obs.), `INTGSTMXM193N` (1986-10 a 2026-07), `IR3TIB01MXM156N` (1997-01 a 2026-08), `IR3TIB01USM156N` (1964-06 a 2026-08), `TB3MS`; Yahoo `IVVPESO.MX` (2014-11-05 a 2026-09-23, 2965 días, MXN, 23 fechas sin precio), `^SP500TR` (1988-01-04 a 2026-09-24), `^GSPC` (1927-12-30 a 2026-09-24) y `MXN=X` (2003-12-01 a 2026-09-24); French `F-F_Research_Data_Factors` mensual y diario (CRSP 202607; 1926-07 a 2026-07). También vi el encabezado y las primeras y últimas filas de los CSV de Banxico que V04 congeló (FIX SF43718 desde el 12/11/1991; CETES 28 SF43936, subastas semanales), para conocer su formato. No he calculado ningún rendimiento, correlación, volatilidad, caída ni Sharpe con estos datos.

---

## PRE-REGISTRO (secciones 1 a 9; no se editan después de la primera corrida)

### 1. Hipótesis previa y mecanismo

**Qué se pregunta.** Para una persona que mide su patrimonio en pesos: (a) ¿cuánto rindió el mercado accionario de EUA en USD y en MXN desde 1994?; (b) ¿el peso se deprecia cuando las acciones de EUA caen fuerte?; (c) ¿cuánto amortiguó el dólar las caídas de 2008, 2020 y 2022?; (d) ¿cubrir el tipo de cambio (pasar la exposición a pesos) reduce o aumenta el riesgo, y cuánto cuesta no cubrir?

**Resultado declarado en el artículo de referencia (NBER WP 13088, revisión de enero de 2009, cifras textuales).**

- Resumen: "Over the period 1975 to 2005, the US dollar (particularly in relation to the Canadian dollar) and the euro and Swiss franc (particularly in the second half of the period) have moved against world equity markets. Thus these currencies should be attractive to risk-minimizing global equity investors despite their low average returns."
- Tabla VII (desviación estándar anualizada, rendimientos trimestrales, cartera global de acciones con pesos iguales, 1975-2005), por moneda base: **EUA** sin cobertura 15.05%, media cobertura 13.91%, cobertura total 13.86%, cobertura óptima 12.51%. **Canadá** sin cobertura 13.74%, media 13.22%, total **13.86%** (cubrir todo **aumenta** el riesgo). Australia 15.00 / 13.52 / 13.86 / 12.51. Eurozona 17.67 / 15.47 / 13.86 / 12.51.
- Sección VII y conclusión: "the optimal currency hedging strategy reduces the standard deviation of a global equity portfolio by 135 basis points relative to a strategy of fully hedging all currency risk, and by over 250 basis points (for a US investor) relative to a strategy of leaving currency risk unhedged". Texto: "full currency hedging actually increases risk for a Canadian investor", porque su moneda "is positively correlated with their equity positions".
- **El peso mexicano no está en la muestra del artículo** (siete monedas desarrolladas). El artículo aporta el **mecanismo**; las cifras que se replican son las del capítulo 16.

**Afirmaciones del capítulo 16 §5.4 que se ponen a prueba** (índice de **precio** `^GSPC`, DEXMXUS; periodos exactos no documentados en el capítulo):

- **A1.** Correlación mensual de Δln(USD/MXN) con el S&P 500: **−0.50** (1996-2026), **−0.56** (2008-2026), **−0.42** (2016-2026), **−0.44** (2023-2026).
- **A2.** Volatilidad anual del S&P en USD contra MXN: 15.3% contra **13.6%** (1996-2026); 15.6 contra 13.4 (2008-2026); 15.0 contra 14.9 (2016-2026); 12.3 contra 11.6 (2023-2026).
- **A3.** Meses con el S&P abajo más de 5% (n = 40, 1996-2026): S&P **−7.8%** en USD, USD/MXN **+3.7%**, S&P en MXN **−4.5%** ("el dólar absorbió alrededor de 40% del golpe").
- **A4.** Caída máxima del S&P (precio): 2007-09 **−56.8% en USD contra −39.8% en MXN**; 2020 **−33.9% contra −15.0%**; 2022 **−25.4% contra −27.4%** (falló).
- **A5.** Episodios, del inicio al mínimo del S&P: Lehman −46.6% en USD y −18.2% en MXN; COVID −33.9% y −10.7% (fechas de inicio no documentadas en el capítulo).
- **A6.** CAGR del S&P (precio) 1996-2026: 8.17% en USD y 11.06% en MXN (USD/MXN +2.67% anual); 2016-2026: 13.48% y 11.41%.

**Mecanismo económico.** El peso es una moneda "de riesgo": en episodios de aversión global al riesgo (caída de acciones, alza del VIX, cierre de fondeo) los inversionistas salen de monedas emergentes líquidas y el peso se deprecia (Brunnermeier, Nagel y Pedersen, 2008; capítulo 16 §2). Para quien mide en MXN, un activo en USD sin cubrir recibe (1 + R_USD)(1 + x), donde x es la variación de USD/MXN. Si x sube cuando R_USD cae, el producto amortigua la caída. Es el caso "Canadá/Australia" de Campbell et al., más extremo. No se arbitra porque no es una anomalía de precio: es una propiedad de covarianza. Su costo es el *carry*: quien cubre recibe el diferencial de tasas (CETES − T-bill) y, si la paridad descubierta falla (capítulo 16 §2.1), el diferencial excede en promedio la depreciación, así que no cubrir cuesta rendimiento esperado. **Cuándo falla:** choques con origen en México (1994-95, cuando el peso se desplomó sin caída de acciones de EUA), choques de inflación y tasas con Banxico más restrictivo que la Fed (2022) y choques contra el dólar (abril de 2025).

**Hipótesis (especificación principal: sección 8).** Notación: R = rendimiento total mensual del mercado de EUA en USD; x = S_t/S_{t−1} − 1 con S en MXN por USD (x > 0: el peso se deprecia); U = (1 + R)(1 + x) − 1 (sin cubrir, en MXN).

- **H1 (correlación).** corr(R, x) es negativa en la muestra completa 1994-01 a 2026-07, con valor esperado entre **−0.35 y −0.60**. También es negativa en `dentro_muestra` (1994-01 a 2007-05), en `fuera_muestra` (2007-06 a 2026-07), en 2008-2026 y en 2016-2026. Espero que 1994-2007 sea la más débil, por la devaluación de 1994-95 (choque mexicano sin caída de acciones de EUA).
- **H2 (caídas grandes).** En los meses con R < −5%, la media de x es positiva, entre **+2% y +5%**, y la amortiguación A = 1 − media(U)/media(R) está entre **0.25 y 0.60**. Lo mismo, con signo, en el peor decil de meses de R.
- **H3 (caídas de 2008, 2020 y 2022; diario, French rendimiento total).** La caída máxima en MXN sin cubrir es **menos profunda que en USD por al menos 10 pp** en la ventana de la crisis financiera (2007-07-01 a 2009-12-31) y en la de 2020 (2020-01-01 a 2020-12-31). En la ventana de 2022 (2022-01-01 a 2022-12-31) la caída en MXN **no es mejor por más de 5 pp** (espero igual o peor).
- **H4 (la cobertura aumenta el riesgo).** La volatilidad anual de la versión cubierta al 100% (h = 1) excede a la sin cubrir (h = 0) por **al menos 1.0 pp** en completo, dentro y fuera de muestra. La caída máxima con h = 1 es más profunda que con h = 0 por al menos 5 pp en completo y fuera de muestra. La volatilidad crece con h (h = 0 < 0.25 < 0.5 < 0.75 < 1) en completo. La razón de cobertura de mínima varianza estimada en la muestra completa (sin recortar) es **≤ 0.25**.
- **H5 (costo de no cubrir; secundaria).** El CAGR con h = 1 supera al de h = 0 en 1994-2026, por **+0.5 a +4 pp** al año. Equivale a que la media mensual de (f − x) sea positiva, donde f es la prima *forward* por paridad cubierta. Sin expectativa firme por segmento ni sobre el Sharpe.
- **H6 (a nivel del benchmark del sistema; secundaria).** El benchmark 50% acciones de EUA + 50% CETES tiene menor volatilidad y caída máxima con la parte accionaria sin cubrir que cubierta, en completo y fuera de muestra.
- **H7 (regla dinámica; secundaria).** La cobertura de mínima varianza con ventana expansiva **no** reduce la volatilidad fuera de muestra en 0.5 pp o más frente a h = 0 (espero que su h se quede cerca de 0).

### 2. Criterio de refutación

- **Métricas principales:** corr(R, x) mensual y su IC 95% por *bootstrap* de bloques; diferencia de volatilidad anual vol(h = 1) − vol(h = 0) y su IC 95% por *bootstrap* de bloques pareado; caídas máximas por ventana de crisis.
- **Refuta H1 (núcleo):** corr completa ≥ 0, **o** su IC 95% (bloques de 12 meses, 5000 repeticiones, semilla 20260925) incluye el 0.
- **Refuta H4 (núcleo):** vol(h = 1) ≤ vol(h = 0) en la muestra completa **o** en `fuera_muestra`.
- **Refuta H3:** en la crisis financiera o en 2020, la caída máxima en MXN no es menos profunda que en USD por al menos 5 pp.
- **Estado.**
  - **No replicado:** se cumple la refutación de H1 o de H4.
  - **Replicado:** H1 a H4 se cumplen con magnitudes dentro de los rangos esperados **y** las cifras del capítulo calculadas a su manera (S3b: `^GSPC` precio × DEXMXUS) caen dentro de tolerancia en A1 (±0.05), A2 (±0.5 pp), A3 (±1.0 pp en cada media), A4 (±1.0 pp en cada caída) y A6 (±0.30 pp).
  - **Replicado con diferencias:** H1 a H4 tienen el signo esperado pero alguna magnitud cae fuera de rango o de tolerancia, o el efecto aparece solo en algunos segmentos o ventanas.
- H5, H6 y H7 no deciden el estado: deciden la conclusión operable (sección 8).
- **Sesgo declarado:** las correlaciones condicionadas a meses volátiles están sesgadas hacia arriba en valor absoluto (Forbes y Rigobon, 2002). Por eso H2 usa medias condicionales, no correlaciones condicionales.

### 3. Datos y licencia

Todo lo descargado se congela en `R08-datos/` con `SHA256SUMS.txt` en la primera corrida. Las corridas siguientes leen los archivos congelados y verifican las huellas.

| Serie | Fuente y archivo | Versión / huella | Frecuencia | Condiciones de uso |
|---|---|---|---|---|
| Mercado de EUA, rendimiento total (Mkt-RF + RF) y RF | French `F-F_Research_Data_Factors` y `_daily` | `version_crsp` y `sha256` (se registran) | mensual y diaria | pendiente de verificar |
| USD/MXN (principal) | FRED `DEXMXUS` (Fed H.10, mediodía en Nueva York) | sha256 del CSV | diaria | serie del Board of Governors; pendiente de verificar |
| USD/MXN FIX (sensibilidad y extensión 1991-1993) | Banxico SIE, cuadro CF102, `SF43718` | sha256 | diaria | pendiente de verificar |
| CETES 28 (efectivo en MXN y tasa para la cobertura) | Banxico SIE, cuadro CF107, `SF43936` (tasa de rendimiento de la subasta semanal) | sha256 | semanal | pendiente de verificar |
| CETES aproximado (sensibilidad) | FRED `INTGSTMXM193N` (FMI) | sha256 | mensual | pendiente de verificar |
| Tasas interbancarias a 3 meses (sensibilidad de la cobertura) | FRED `IR3TIB01MXM156N` e `IR3TIB01USM156N` (OCDE) | sha256 | mensual | pendiente de verificar |
| S&P 500 rendimiento total (sensibilidad) | Yahoo `^SP500TR` | sha256 del JSON | diaria → fin de mes | pendiente de verificar |
| S&P 500 precio (cifras del capítulo) | Yahoo `^GSPC` | sha256 | diaria | pendiente de verificar |
| ETF cubierto real (sensibilidad) | Yahoo `IVVPESO.MX` (iShares S&P 500 Peso Hedged TRAC; IVV del SIC más *forward* MXN/USD; gasto 0.49%; constituido el 2014-11-05, según su ficha de BlackRock México) | sha256 | diaria → fin de mes | pendiente de verificar |

Si la descarga de Banxico falla, se usa `INTGSTMXM193N` como CETES y DEXMXUS sin extensión 1991-1993, y se anota como desviación.

### 4. Universo

Un solo activo de riesgo: el mercado accionario de EUA ponderado por valor (CRSP, todas las acciones de NYSE, AMEX y NASDAQ) de French. **No es el S&P 500**: el S&P 500 TR (`^SP500TR`) entra como sensibilidad. No hay sesgo de supervivencia (CRSP incluye empresas deslistadas), pero **no es invertible directamente**. Sus proxies operables son IVV, VOO o SPY en el SIC (sin cubrir) y `IVVPESO` en la BMV (cubierto). Que estén disponibles en GBM **no está verificado**. La moneda del inversionista es el MXN. El efectivo es CETES 28.

**Tipo de cambio antes de 1994.** Hasta el 10-nov-1991 hubo control de cambios con mercados controlado y libre (1982-1991), así que **no existe una serie única de mercado confiable**. El control se abrogó el 11-nov-1991 (Banxico, "Regímenes cambiarios en México a partir de 1954", 2009) y el FIX empieza el 12-nov-1991. De 1991-11 al 1994-12-21 hubo bandas con desliz controlado; la libre flotación empieza el 1994-12-22. Por eso: la muestra principal empieza en 1994-01 con DEXMXUS (como pide la tarea), y 1991-12 a 1993-12 se agrega **solo como sensibilidad** con el FIX (régimen de bandas, no comparable con la flotación). Antes de 1991-11 no se usa.

### 5. Fecha de disponibilidad

- **R (French):** el rendimiento del mes t se conoce al cierre de t (French lo publica con rezago de un mes; la única regla que lo usa para decidir, la de mínima varianza, lo usa con rezago de al menos un mes: ver abajo).
- **RF (French):** rendimiento de la T-bill a un mes comprada al inicio del mes t: se conoce en t−1.
- **DEXMXUS:** tipo de mediodía en Nueva York del día d. La Fed lo publica en el H.10 semanal (lunes). El FIX de Banxico se conoce el mismo día.
- **CETES 28:** la tasa aplicable al mes t es la de la **última subasta con fecha ≤ último día del mes t−1** (conocida al inicio de t). Rendimiento del mes: tasa/100 × días naturales del mes/360.
- **Prima *forward*:** f_t = (1 + i^MX_t)/(1 + i^US_t) − 1, con i^MX_t = CETES del mes t (fijada en t−1) e i^US_t = RF_t. Se fija al inicio del mes (paridad cubierta; es una aproximación: los *forwards* reales se valúan con tasas interbancarias, lo que se prueba en S4).
- **Señales.** Las variantes de razón fija son constantes. La de mínima varianza (P6) calcula h_t solo con meses ≤ t−1 y se audita con `auditar_constructor` (invariancia de prefijo). Aunque en tiempo real French se publica con rezago, la estimación usa ≥ 36 meses y una versión en tiempo real podría usar `^SP500TR` o el ETF; se declara como aproximación.

### 6. Periodo

- Periodo del artículo: 1975-2005 (sin peso mexicano). Periodo del capítulo: "1996-2026", "2008-2026", "2016-2026" y "2023-2026", sin fechas exactas.
- **Periodo propio principal (mensual):** base 1993-12-31; rendimientos de **1994-01 a 2026-07** (último mes de French CRSP 202607).
- **Corte:** **2007-05-31**, primera versión pública de Campbell et al. (NBER WP 13088, mayo de 2007). `dentro_muestra` = 1994-01 a 2007-05; `fuera_muestra` = 2007-06 a 2026-07. El tramo fuera de muestra contiene las tres crisis (2008, 2020, 2022).
- **Ventanas calendario descriptivas** (para comparar con el capítulo): 1996-01 a 2026-07, 2008-01 a 2026-07, 2016-01 a 2026-07 y 2023-01 a 2026-07.
- **Diario (caídas de crisis):** 1994-01-03 a 2026-07-31. Ventanas fijas: **crisis financiera** 2007-07-01 a 2009-12-31; **año 2008** 2007-12-31 a 2008-12-31 (para comparar con V04); **2020** 2020-01-01 a 2020-12-31; **2022** 2022-01-01 a 2022-12-31.
- **Episodios (del pico al valle del S&P, fechas fijadas aquí):** COVID 2020-02-19 → 2020-03-23; Lehman 2008-09-12 (último cierre antes de la quiebra del 15-sep) → 2009-03-09. El capítulo no documenta su fecha de inicio para Lehman, así que ahí la comparación es solo indicativa.
- **Extensión FIX:** 1991-12 a 2026-07 (sensibilidad S2), con submuestra de bandas 1991-12 a 1994-11 (descriptiva).
- **IVVPESO:** 2014-12 a 2026-07 (primer mes completo tras su constitución, hasta el último mes de French).

### 7. Limpieza

- Tipo de cambio: para cada fecha se toma el último dato ≤ esa fecha con antigüedad ≤ 10 días (lo que hace el motor con `max_dias_fx=10`). Fin de mes = último dato ≤ último día del mes calendario.
- French: se omiten −99.99/−999 (la versión 202607 no tiene faltantes en estas columnas).
- Yahoo: se descartan `fechas_sin_precio`; el precio de fin de mes es el último válido ≤ fin de mes con antigüedad ≤ 10 días; si no existe, el mes se omite y se reporta.
- CETES: la tasa vigente es la de la última subasta ≤ la fecha.
- No se eliminan valores extremos: la devaluación de 1994-95, 2008 y 2020 se quedan. Ninguna observación se elimina después de ver resultados.

### 8. Regla y variantes planeadas

**Rendimiento cubierto (pseudocódigo, mensual):**

```
x_t  = S_t / S_{t-1} - 1                         # S = MXN por USD a fin de mes
U_t  = (1 + R_t)(1 + x_t) - 1                    # sin cubrir, en MXN
f_t  = (1 + cetes_t) / (1 + rf_t) - 1            # prima forward (paridad cubierta), fijada en t-1
H_t  = (1 + x_t) - (1 + f_t)                     # pago por USD vendido a plazo (en MXN por USD inicial)
R^h_t = U_t - h * H_t - h * c / 12               # h = razon de cobertura; c = costo anual de la cobertura
```

Con h = 1 queda R^1 = R·(1 + x) + f: el inversionista recibe el rendimiento de EUA más el diferencial de tasas, con un residuo cambiario sobre R (se cubre el valor inicial, no la ganancia del mes). **Mínima varianza (P6):** h_t = Cov(U, H)/Var(H) con los meses 1994-01 … t−1 (ventana expansiva), mínimo 36 meses (antes, h = 0), recortada a [0, 1] (con `apalancamiento.bruto_max_fase_1` = 1.0 no cabe sobre ni sub-cobertura).

**Motor.** `herramientas/backtest.py`, `id_replica="R08"`, mensual, `cortes=[2007-05-31]`, efectivo = CETES 28 en MXN (`efectivo_en_mxn=True`), exposición constante (comprar y mantener: solo se paga la entrada) salvo el benchmark 50/50 (rebalanceo mensual a 0.5 con deriva). La variante sin cubrir se calcula con el `fx` del motor. Las cubiertas se construyen fuera del motor con la fórmula de arriba y entran como activo en MXN. Se verifica que la construcción propia de h = 0 coincida con la del motor (tolerancia 1e-12).

**Variantes de prueba (`es_prueba=1`; lista cerrada; N = 8):**

| ID | Variante | Descripción |
|---|---|---|
| P1 | `mxn_h000` | Mercado de EUA sin cubrir en MXN (motor con `fx` = DEXMXUS) |
| P2 | `mxn_h025` | Cobertura fija de 25% |
| P3 | `mxn_h050` | Cobertura fija de 50% |
| P4 | `mxn_h075` | Cobertura fija de 75% |
| P5 | `mxn_h100` | Cobertura total |
| P6 | `mxn_hminvar_exp36` | Cobertura de mínima varianza, ventana expansiva, mínimo 36 meses, recortada a [0, 1] |
| P7 | `bench50_h000` | 50% mercado de EUA sin cubrir + 50% CETES, rebalanceo mensual |
| P8 | `bench50_h100` | 50% mercado de EUA cubierto + 50% CETES, rebalanceo mensual |

**Referencias y sensibilidades (`es_prueba=0`; lista cerrada; todo lo demás es desviación):**

| ID | Qué cambia | Variantes |
|---|---|---|
| S0 | Referencias | `usd_referencia` (mercado de EUA en USD contra RF); `cetes_100` (100% CETES) |
| S1 | FX = FIX de Banxico (fin de mes) | P1 y P5 |
| S2 | Extensión 1991-12 a 2026-07 con FIX | P1, P5 y `usd_referencia` |
| S3a | Activo = `^SP500TR` (S&P 500 TR) | P1, P5 y `usd_referencia` |
| S3b | Cifras del capítulo: `^GSPC` precio × DEXMXUS; correlaciones con Δln(USD/MXN) en las ventanas calendario; caídas diarias por ventana | `gspc_precio_usd` y `gspc_precio_mxn_h000` en el motor; el resto, descriptivo |
| S4 | Tasas de la cobertura: interbancarias a 3 meses de México y EUA (OCDE), valor del mes t−1/1200; 1997-02 a 2026-07 | P3 y P5 (y P1 en la misma ventana, para comparar) |
| S5 | CETES = FRED `INTGSTMXM193N` (valor del mes t−1/1200), para el efectivo y la cobertura | P1 y P5 |
| S6 | Costo de la cobertura c = 0.5% y 1.0% anual sobre lo cubierto (0.5% ≈ gasto de IVVPESO 0.49% menos el de IVV) | P2 a P6 y P8 |
| S7 | Spread "medio" 0.15% por lado | P1 a P8 |
| S8 | Frecuencia diaria (French diario, DEXMXUS diario, CETES devengado por día natural, cobertura renovada a diario) | `usd_referencia`, P1 y P5 |
| S9 | Instrumento real: `IVVPESO.MX` contra el S&P 500 TR cubierto sintético y sin cubrir (`^SP500TR` × DEXMXUS), 2014-12 a 2026-07 | `ivvpeso_real`, `sp500tr_mxn_h100_sintetico`, `sp500tr_mxn_h000` |

**Estadística descriptiva pre-registrada (fuera del motor):**

- corr(R, x) de Pearson en completo, dentro, fuera y en las ventanas calendario, con IC 95% por *bootstrap* de bloques móviles (12 meses, 5000 repeticiones, semilla 20260925); beta de x sobre R por MCO con t de Newey-West(6); betas separadas en meses con R < 0 y R ≥ 0.
- Meses con R < −5%, peor decil de R, meses con R > +5% y mejor decil: n, media de R, de x, de U y de R^1; proporción de meses con x > 0; amortiguación A.
- Caídas por ventana (diarias y mensuales) para USD, MXN sin cubrir y MXN cubierto: caída máxima dentro de la ventana con fechas de pico y valle; cambio entre el pico y el valle de USD medido en las otras dos series; cambio entre extremos de la ventana.
- Diferencia de volatilidad vol(h = 1) − vol(h = 0) con IC 95% por *bootstrap* de bloques **pareado** (mismos bloques para las dos series), en completo y fuera.
- Media de (f − x) = R^1 − U con t de Newey-West(6) y t IID (prueba de H5).
- h de mínima varianza: completo, dentro y fuera (sin recortar), y la distribución de la h expansiva (mínimo, mediana, máximo).
- Sharpe deflactado con `sharpe_deflactado_de_registro("R08")`, N = 8 y segmento `dentro_muestra`, para la variante elegida (la de mayor Sharpe), para P1 y para P5. **El DSR no decide nada aquí**: contrasta el Sharpe contra 0, no el riesgo entre coberturas.

**Exposición:** mínima 0 y máxima 1 (sin apalancamiento). Moneda: MXN (USD solo en la referencia).

**Reglas de decisión para la conclusión operable (fijadas antes de ver resultados).** La regla del sistema bajo prueba es la del capítulo 16 §6.2 regla 4 ("Acciones de EUA: nunca se cubren en el patrimonio principal") y §6.4 ("acciones globales, horizonte de más de 1 año: no cubrir").

- **Se confirma** si H1, H3 (crisis financiera y 2020), H4 y H6 se cumplen **fuera de muestra**. En ese caso, la cobertura natural es una propiedad de **riesgo**, no de rendimiento, y su costo esperado es el de H5.
- **Se modifica** si H4 se cumple en completo pero alguna cobertura parcial (h = 0.25 o 0.5) tiene menor volatilidad **y** menor caída máxima que h = 0 fuera de muestra (sería "cubrir parcialmente"). También se modifica si H5 muestra un costo de no cubrir mayor a 3 pp anuales con significancia (t NW ≥ 2): la regla se conserva, pero con su costo explícito.
- **Se descarta** si se refuta H4 (cubrir no aumenta el riesgo).
- **Cobertura dinámica (P6):** solo se adopta si reduce la volatilidad fuera de muestra ≥ 0.5 pp frente a h = 0 sin empeorar la caída máxima más de 2 pp. Si no, se descarta.

### 9. Costos y comparación simple

- **Costos:** comisión 0.29% por lado (GBM, hecho) + spread 0.05% por lado (supuesto); escenario "medio" 0.15% (S7). Con exposición constante solo se paga la entrada; el 50/50 paga el rebalanceo mensual con deriva. **No se modelan:** el spread cambiario implícito del SIC (no publicado), el costo de renovar *forwards* (solo como c en S6), el gasto de los ETF (salvo S9, que usa el precio real de IVVPESO), la venta final, ni impuestos (ISR de 10% sobre ganancias del SIC y la BMV, retención de dividendos de EUA). Los impuestos van en una capa aparte.
- **Reglas sencillas con idénticas condiciones:** comprar y mantener sin cubrir (P1, que es la regla sencilla de este caso), 100% CETES (`cetes_100`), cobertura total (P5) y el benchmark principal de `parametros.json` (P7: 50% S&P TR en MXN + 50% CETES 28).

---

## RESULTADOS (se llenan después de correr)

> Corrida final: 2026-09-25 06:56 UTC (corrida 3). Las tablas de esta sección se copiaron de `R08-salida.txt` con un script, sin transcribirlas a mano. Todas las cifras son históricas: no son pronósticos ni recomendaciones.

### Desviaciones del pre-registro

| Fecha | Qué cambió | Por qué | ¿Invalida el tramo de prueba? |
|---|---|---|---|
| 2026-09-25 06:51 UTC | La corrida 1 se detuvo en la sensibilidad S4, después de registrar 69 filas: P1-P8, S0, S8, S3b, S1, S2 y S3a. | FRED `IR3TIB01USM156N` tiene vacío el mes 2020-04, y el código exigía el dato exacto del mes t−1. | No. Las 69 filas se conservan en el CSV. Las corridas 2 (06:52) y 3 (06:56) las repiten con los mismos datos congelados y los mismos parámetros. Entre corridas no hay ninguna diferencia en CAGR, volatilidad, MDD, Sharpe ni huella de datos. N sigue en 8. |
| 2026-09-25 | S4: si falta el dato del mes t−1, se usa el último valor conocido con antigüedad de 62 días o menos. | Mismo hueco. Solo afecta a 2020-05, que usa el dato de 2020-03 (1.35%). Sigue siendo causal. | No: S4 es una sensibilidad. |
| 2026-09-25 06:56 UTC | Corrida 3: se corrigió la fórmula de la correlación **diaria** entre R y x. Esa correlación no estaba pre-registrada y el script la imprime "solo como referencia". Las corridas 1 y 2 usaban U/(1+R) − 1 en lugar de (1+U)/(1+R) − 1 e imprimieron **+0.744**. El valor corregido es **−0.228**. | Error de código detectado al revisar la salida. | No. El resto de la salida de las corridas 2 y 3 es idéntico (comprobado con `diff`). |
| 2026-09-25 | Aclaración de implementación, fijada en el código antes de la primera corrida real: en las ventanas de crisis, el nivel inicial es el último dato ≤ fecha de inicio. Aplica en diario, mensual e IVVPESO. | El pre-registro decía "caída máxima dentro de la ventana" sin definir el punto de partida. | No. |
| 2026-09-25 | **Defecto del pre-registro: las reglas de decisión operable chocan.** Se cumplen a la vez las cuatro condiciones de "se confirma" (fuera de muestra) y la condición de "se descarta" (H4 refutada en la muestra completa). El pre-registro no fijó cuál manda. El código aplica "descarta" primero. | Error de diseño: no preví que H4 pudiera cumplirse fuera de muestra y refutarse en la muestra completa. | No cambia ninguna cifra. La resolución se declara como post-hoc en §16 ("Conclusión operable"). |
| 2026-09-25 | Análisis **post-hoc**, no pre-registrados y sin efecto en el estado: (a) fechas de la caída máxima mensual de cada serie en 1994-2026; (b) los meses de mayor depreciación del peso; (c) volatilidad de 1994-01 a 1995-12; (d) lectura de la ficha oficial de IVVPESO (BlackRock México, datos al 31-ago-2026), descargada el 2026-09-25. | Explicar por qué se refuta H4 y de dónde sale la brecha de IVVPESO. | No. |

### 10. Variantes probadas

- Archivo: `replicas/R08-variantes.csv`. Tiene 363 filas de 3 corridas: 69 de la corrida 1 (abortada), 147 de la 2 y 147 de la 3.
- Variantes con `es_prueba=1`: **8**, exactamente las pre-registradas (P1 a P8). Variantes con `es_prueba=0`: 43 (referencias S0 y sensibilidades S1 a S9).
- **Pruebas fuera del registro con datos reales: 0.** El modo `--prueba-sintetica` usa números aleatorios y escribe en un directorio temporal. Los análisis post-hoc son descriptivos: no son variantes de regla. Por eso `n_pruebas` = 8.
- Controles (salida del script):
  - Mensual: `|U propio - r_activo del motor| max = 0.000e+00; |CETES propio - r_efectivo| max = 0.000e+00`.
  - Diario: `|U propio - r_activo del motor| max = 0.000e+00`.
  - Auditoría de prefijo del constructor de mínima varianza: `causal=True`, 23 cortes, sin fallos.
- `sharpe_deflactado_de_registro("R08")`, segmento `dentro_muestra`, N = 8, V = 0.001 (varianza del Sharpe por periodo):

| Variante | SR anual | SR0 anual | DSR | ¿≥ 0.95? | PSR sin deflactar |
|---|---|---|---|---|---|
| `mxn_h100` (elegida: el mayor Sharpe) | 0.504 | 0.161 | 0.8787 | no | 0.9569 |
| `mxn_h000` | 0.237 | 0.161 | 0.6201 | no | 0.8292 |

  Como se pre-registró, el DSR **no decide nada en R08**: contrasta el Sharpe contra 0, no el riesgo entre coberturas. Ninguna variante llega a 0.95.

### 11. Resultados

#### 11.1 Rendimiento del mercado de EUA en USD y en MXN (series brutas, sin costos; mensual; French rendimiento total; DEXMXUS; CETES 28)

| ventana | base a fin | CAGR USD | CAGR MXN sin cubrir | CAGR MXN cubierto | USD/MXN anual | CETES | T-bill | MDD USD (mensual) | MDD MXN sin cubrir | MDD MXN cubierto |
|---|---|---|---|---|---|---|---|---|---|---|
| completo | 1993-12 a 2026-07 | 10.92% | 16.93% | 19.30% | 5.41% | 11.17% | 2.46% | -50.3% | -39.9% | -48.7% |
| dentro_muestra | 1993-12 a 2007-05 | 11.15% | 21.91% | 25.91% | 9.68% | 18.37% | 3.94% | -45.0% | -39.9% | -36.2% |
| fuera_muestra | 2007-05 a 2026-07 | 10.76% | 13.56% | 14.89% | 2.53% | 6.39% | 1.43% | -50.3% | -30.0% | -48.7% |
| 1996-2026 | 1995-12 a 2026-07 | 10.54% | 13.49% | 17.48% | 2.67% | 9.75% | 2.31% | -50.3% | -39.9% | -48.7% |
| 2008-2026 | 2007-12 a 2026-07 | 11.31% | 14.11% | 15.49% | 2.52% | 6.36% | 1.35% | -47.7% | -27.7% | -46.3% |
| 2016-2026 | 2015-12 a 2026-07 | 14.85% | 14.93% | 19.95% | 0.07% | 7.66% | 2.19% | -24.8% | -27.2% | -22.0% |
| 2023-2026 | 2022-12 a 2026-07 | 22.05% | 18.09% | 27.55% | -3.25% | 10.04% | 4.62% | -9.1% | -13.1% | -8.0% |

Lectura:

- Desde 1994, el mercado de EUA rindió 10.92% anual en USD y 16.93% en MXN sin cubrir, porque el USD/MXN subió 5.41% anual.
- La versión cubierta rindió 19.30%: el diferencial CETES − T-bill promedió 8.22% anual (media de f × 12), más que la depreciación medida igual (media de x × 12: 6.17%).
- Fuera de muestra (2007-06 a 2026-07): 10.76% en USD, 13.56% sin cubrir y 14.89% cubierto.
- **Todo esto es sin costos de la cobertura.** Con el instrumento real (S9), la ventaja teórica desaparece.

#### 11.2 H1: correlación mensual entre R (EUA, USD) y x (variación de USD/MXN)

| segmento | meses | n | corr(R,x) | IC95 bootstrap | corr(R,Δln S) | beta de x sobre R | beta R<0 / R≥0 | vol USD | vol MXN sin cubrir | vol MXN cubierto | vol x |
|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | 1994-01 a 2026-07 | 391 | -0.370 | [-0.571, -0.211] | -0.389 | -0.336 (t NW -6.60) | -0.541 / -0.373 | 15.4% | 16.7% | 16.1% | 14.0% |
| dentro_muestra | 1994-01 a 2007-05 | 161 | -0.174 | [-0.466, -0.036] | -0.192 | -0.197 (t NW -3.09) | -0.240 / -0.456 | 14.6% | 20.2% | 15.8% | 16.4% |
| fuera_muestra | 2007-06 a 2026-07 | 230 | -0.557 | [-0.686, -0.391] | -0.556 | -0.416 (t NW -6.64) | -0.701 / -0.324 | 16.0% | 13.8% | 16.4% | 12.0% |
| 1996-2026 | 1996-01 a 2026-07 | 367 | -0.503 | [-0.612, -0.364] | -0.501 | -0.343 (t NW -6.72) | -0.565 / -0.292 | 15.8% | 14.0% | 16.2% | 10.8% |
| 2008-2026 | 2008-01 a 2026-07 | 223 | -0.556 | [-0.684, -0.393] | -0.555 | -0.418 (t NW -6.59) | -0.703 / -0.325 | 16.2% | 13.9% | 16.5% | 12.1% |
| 2016-2026 | 2016-01 a 2026-07 | 127 | -0.415 | [-0.563, -0.183] | -0.414 | -0.323 (t NW -3.74) | -0.696 / -0.254 | 15.7% | 15.5% | 16.0% | 12.2% |
| 2023-2026 | 2023-01 a 2026-07 | 43 | -0.448 | [-0.737, -0.050] | -0.452 | -0.311 (t NW -3.39) | -0.726 / -0.375 | 13.2% | 12.2% | 13.1% | 9.2% |

- **H1 se cumple.** La correlación es de −0.370 en 1994-2026, con IC 95% por *bootstrap* de [−0.571, −0.211], que excluye el 0. Cae dentro del rango esperado (−0.60 a −0.35).
- Es negativa en los cuatro segmentos pre-registrados. Como se esperaba, 1994-2007 es la más débil (−0.174), por el choque mexicano de 1994-95. Desde 2007 es de −0.557.
- La beta de x sobre R es −0.336 (t NW −6.60): por cada 10% que caen las acciones de EUA, el USD/MXN sube en promedio alrededor de 3.4%.
- La beta es más negativa en meses con R < 0 que con R ≥ 0 en completo, fuera de muestra y 2008-2026. En 1994-2007 es al revés.

#### 11.3 H2: meses de caída y de alza grandes (1994-01 a 2026-07)

| grupo | n | media R (USD) | media x (USD/MXN) | media MXN sin cubrir | media MXN cubierto | % meses con x > 0 | amortiguación A |
|---|---|---|---|---|---|---|---|
| R < -5% | 38 | -8.06% | 3.68% | -4.74% | -7.86% | 78.9% | 0.411 |
| peor decil de R | 39 | -7.98% | 3.65% | -4.69% | -7.77% | 79.5% | 0.413 |
| R > +5% | 62 | 7.11% | -1.67% | 5.32% | 7.74% | 19.4% | 0.252 |
| mejor decil de R | 39 | 8.04% | -1.60% | 6.30% | 8.70% | 20.5% | 0.216 |
| todos | 391 | 0.97% | 0.51% | 1.42% | 1.59% | 49.1% | -0.468 |

Meses con R < −5% por segmento:

| segmento | n | media R | media x | media MXN sin cubrir | A |
|---|---|---|---|---|---|
| dentro_muestra | 13 | -8.06% | 1.93% | -6.35% | 0.213 |
| fuera_muestra | 25 | -8.06% | 4.59% | -3.91% | 0.515 |

Los 10 peores meses de R:

| mes | R (USD) | x (USD/MXN) | MXN sin cubrir | MXN cubierto |
|---|---|---|---|---|
| 2008-10 | -17.12% | 15.79% | -4.03% | -19.20% |
| 1998-08 | -15.62% | 11.94% | -5.55% | -16.20% |
| 2020-03 | -13.25% | 18.84% | 3.10% | -15.27% |
| 2002-09 | -10.20% | 2.96% | -7.54% | -10.08% |
| 2000-11 | -10.19% | -1.61% | -11.64% | -9.13% |
| 2009-02 | -10.13% | 5.27% | -5.40% | -10.11% |
| 2001-02 | -9.65% | 0.14% | -9.52% | -8.63% |
| 2022-04 | -9.41% | 2.25% | -7.37% | -9.08% |
| 2018-12 | -9.36% | -3.26% | -12.32% | -8.56% |
| 2008-09 | -9.20% | 6.56% | -3.24% | -9.27% |

- **H2 se cumple.** En los 38 meses con R < −5%, el USD/MXN subió en promedio **+3.68%** (rango esperado: +2% a +5%). En 78.9% de esos meses el peso se depreció. La amortiguación fue **A = 0.411** (rango esperado: 0.25 a 0.60).
- La cobertura natural es **simétrica**. En los 62 meses con R > +5%, el peso se apreció (−1.67%) y el mexicano recibió 5.32% en vez de 7.11%.
- En octubre de 2008 el mercado cayó −17.12% en USD y solo −4.03% en MXN. En marzo de 2020 cayó −13.25% en USD y **subió** +3.10% en MXN.

#### 11.4 H3: caídas de 2008, 2020 y 2022 (diario, French rendimiento total)

| ventana | serie | MDD en la ventana | pico | valle | cambio entre pico y valle de USD | cambio punta a punta |
|---|---|---|---|---|---|---|
| crisis_financiera | usd | -54.6% | 2007-10-09 | 2009-03-09 | -54.6% | -19.6% |
| crisis_financiera | mxn_sin_cubrir | -38.3% | 2007-10-09 | 2008-11-20 | -35.5% | -2.7% |
| crisis_financiera | mxn_cubierto | -51.7% | 2007-10-09 | 2009-03-09 | -51.7% | -11.4% |
| anio_2008 | usd | -47.7% | 2007-12-31 | 2008-11-20 | -47.7% | -36.5% |
| anio_2008 | mxn_sin_cubrir | -35.1% | 2007-12-31 | 2008-11-20 | -35.1% | -19.5% |
| anio_2008 | mxn_cubierto | -45.8% | 2007-12-31 | 2008-11-20 | -45.8% | -33.5% |
| 2020 | usd | -34.2% | 2020-02-19 | 2020-03-23 | -34.2% | 24.2% |
| 2020 | mxn_sin_cubrir | -16.2% | 2020-02-20 | 2020-03-16 | -11.1% | 31.0% |
| 2020 | mxn_cubierto | -35.1% | 2020-02-19 | 2020-03-23 | -35.1% | 25.9% |
| 2022 | usd | -25.4% | 2022-01-03 | 2022-10-14 | -25.4% | -20.0% |
| 2022 | mxn_sin_cubrir | -27.5% | 2022-01-03 | 2022-10-11 | -27.3% | -23.9% |
| 2022 | mxn_cubierto | -23.0% | 2022-01-03 | 2022-06-16 | -22.1% | -15.4% |

Episodios con fechas fijadas en el pre-registro:

| episodio | desde | hasta | usd | mxn_sin_cubrir | mxn_cubierto |
|---|---|---|---|---|---|
| Lehman | 2008-09-12 | 2009-03-09 | -45.0% | -20.0% | -43.9% |
| COVID | 2020-02-19 | 2020-03-23 | -34.2% | -11.1% | -35.1% |

Las mismas ventanas con datos mensuales:

| ventana | serie | MDD en la ventana | pico | valle | cambio entre pico y valle de USD | cambio punta a punta |
|---|---|---|---|---|---|---|
| crisis_financiera | usd | -50.3% | 2007-10-31 | 2009-02-28 | -50.3% | -19.8% |
| crisis_financiera | mxn_sin_cubrir | -30.0% | 2007-09-30 | 2009-02-28 | -29.9% | -3.0% |
| crisis_financiera | mxn_cubierto | -48.7% | 2007-10-31 | 2009-02-28 | -48.7% | -13.8% |
| anio_2008 | usd | -37.8% | 2007-12-31 | 2008-11-30 | -37.8% | -36.7% |
| anio_2008 | mxn_sin_cubrir | -23.7% | 2007-12-31 | 2008-11-30 | -23.7% | -19.7% |
| anio_2008 | mxn_cubierto | -36.8% | 2007-12-31 | 2008-11-30 | -36.8% | -35.3% |
| 2020 | usd | -20.2% | 2020-01-31 | 2020-03-31 | -20.2% | 24.1% |
| 2020 | mxn_sin_cubrir | -8.2% | 2020-08-31 | 2020-10-31 | -1.0% | 30.9% |
| 2020 | mxn_cubierto | -22.0% | 2020-01-31 | 2020-03-31 | -22.0% | 25.1% |
| 2022 | usd | -24.8% | 2021-12-31 | 2022-09-30 | -24.8% | -19.9% |
| 2022 | mxn_sin_cubrir | -26.3% | 2021-12-31 | 2022-09-30 | -26.3% | -23.9% |
| 2022 | mxn_cubierto | -21.5% | 2021-12-31 | 2022-09-30 | -21.5% | -15.3% |

- **H3 se cumple.** La caída en MXN sin cubrir fue menos profunda que en USD por **16.2 pp** en la crisis financiera (−38.3% contra −54.6%) y por **18.0 pp** en 2020 (−16.2% contra −34.2%).
- En 2022 la cobertura natural **falló**: −27.5% en MXN contra −25.4% en USD (-2.0 pp).
- En las tres ventanas, la versión cubierta cayó casi lo mismo que la de USD. En 2022 cayó un poco menos (−23.0%), porque el *carry* del peso fue positivo.

#### 11.5 H4 y H5: la cobertura (motor, neto de costos; P1 a P8 y referencias)

Muestra completa, 1994-01 a 2026-07:

| variante | inicio (base) | fin | n | CAGR | vol | Sharpe vs efectivo | MDD | Calmar | CAGR efectivo | costo anual |
|---|---|---|---|---|---|---|---|---|---|---|
| mxn_h000 | 1993-12-31 | 2026-07-31 | 391 | 16.92% | 16.71% | 0.383 | -39.86% | 0.424 | 11.17% | 0.010% |
| mxn_h025 | 1993-12-31 | 2026-07-31 | 391 | 17.70% | 15.41% | 0.452 | -38.20% | 0.463 | 11.17% | 0.010% |
| mxn_h050 | 1993-12-31 | 2026-07-31 | 391 | 18.36% | 14.85% | 0.508 | -39.72% | 0.462 | 11.17% | 0.010% |
| mxn_h075 | 1993-12-31 | 2026-07-31 | 391 | 18.89% | 15.11% | 0.536 | -44.31% | 0.426 | 11.17% | 0.010% |
| mxn_h100 | 1993-12-31 | 2026-07-31 | 391 | 19.29% | 16.15% | 0.535 | -48.70% | 0.396 | 11.17% | 0.010% |
| mxn_hminvar_exp36 | 1993-12-31 | 2026-07-31 | 391 | 19.13% | 17.35% | 0.489 | -44.01% | 0.435 | 11.17% | 0.010% |
| bench50_h000 | 1993-12-31 | 2026-07-31 | 391 | 14.33% | 8.67% | 0.379 | -11.87% | 1.207 | 11.17% | 0.038% |
| bench50_h100 | 1993-12-31 | 2026-07-31 | 391 | 15.48% | 8.54% | 0.530 | -23.67% | 0.654 | 11.17% | 0.041% |
| usd_referencia | 1993-12-31 | 2026-07-31 | 391 | 10.91% | 15.43% | 0.594 | -50.31% | 0.217 | 2.46% | 0.010% |
| cetes_100 | 1993-12-31 | 2026-07-31 | 391 | 11.17% | 2.88% | 0.000 | 0.00% | inf | 11.17% | 0.000% |

Dentro de muestra, 1994-01 a 2007-05:

| variante | inicio (base) | fin | n | CAGR | vol | Sharpe vs efectivo | MDD | Calmar | CAGR efectivo | costo anual |
|---|---|---|---|---|---|---|---|---|---|---|
| mxn_h000 | 1993-12-31 | 2007-05-31 | 161 | 21.88% | 20.17% | 0.237 | -39.86% | 0.549 | 18.37% | 0.025% |
| mxn_h025 | 1993-12-31 | 2007-05-31 | 161 | 23.11% | 17.76% | 0.312 | -38.20% | 0.605 | 18.37% | 0.025% |
| mxn_h050 | 1993-12-31 | 2007-05-31 | 161 | 24.20% | 16.07% | 0.394 | -37.50% | 0.646 | 18.37% | 0.025% |
| mxn_h075 | 1993-12-31 | 2007-05-31 | 161 | 25.13% | 15.37% | 0.466 | -36.83% | 0.682 | 18.37% | 0.025% |
| mxn_h100 | 1993-12-31 | 2007-05-31 | 161 | 25.88% | 15.77% | 0.504 | -36.20% | 0.715 | 18.37% | 0.025% |
| mxn_hminvar_exp36 | 1993-12-31 | 2007-05-31 | 161 | 26.38% | 20.72% | 0.419 | -36.56% | 0.721 | 18.37% | 0.025% |
| bench50_h000 | 1993-12-31 | 2007-05-31 | 161 | 20.58% | 10.55% | 0.233 | -11.60% | 1.774 | 18.37% | 0.048% |
| bench50_h100 | 1993-12-31 | 2007-05-31 | 161 | 22.36% | 8.78% | 0.499 | -12.20% | 1.832 | 18.37% | 0.047% |
| usd_referencia | 1993-12-31 | 2007-05-31 | 161 | 11.12% | 14.55% | 0.536 | -44.99% | 0.247 | 3.94% | 0.025% |
| cetes_100 | 1993-12-31 | 2007-05-31 | 161 | 18.37% | 3.71% | 0.000 | 0.00% | inf | 18.37% | 0.000% |

Fuera de muestra, 2007-06 a 2026-07:

| variante | inicio (base) | fin | n | CAGR | vol | Sharpe vs efectivo | MDD | Calmar | CAGR efectivo | costo anual |
|---|---|---|---|---|---|---|---|---|---|---|
| mxn_h000 | 2007-05-31 | 2026-07-31 | 230 | 13.56% | 13.75% | 0.543 | -29.97% | 0.452 | 6.39% | 0.000% |
| mxn_h025 | 2007-05-31 | 2026-07-31 | 230 | 14.05% | 13.48% | 0.583 | -34.93% | 0.402 | 6.39% | 0.000% |
| mxn_h050 | 2007-05-31 | 2026-07-31 | 230 | 14.43% | 13.87% | 0.596 | -39.72% | 0.363 | 6.39% | 0.000% |
| mxn_h075 | 2007-05-31 | 2026-07-31 | 230 | 14.71% | 14.86% | 0.583 | -44.31% | 0.332 | 6.39% | 0.000% |
| mxn_h100 | 2007-05-31 | 2026-07-31 | 230 | 14.89% | 16.35% | 0.555 | -48.70% | 0.306 | 6.39% | 0.000% |
| mxn_hminvar_exp36 | 2007-05-31 | 2026-07-31 | 230 | 14.30% | 14.44% | 0.570 | -44.01% | 0.325 | 6.39% | 0.000% |
| bench50_h000 | 2007-05-31 | 2026-07-31 | 230 | 10.15% | 6.86% | 0.538 | -11.87% | 0.855 | 6.39% | 0.031% |
| bench50_h100 | 2007-05-31 | 2026-07-31 | 230 | 10.90% | 8.17% | 0.550 | -23.67% | 0.460 | 6.39% | 0.037% |
| usd_referencia | 2007-05-31 | 2026-07-31 | 230 | 10.76% | 16.04% | 0.631 | -50.31% | 0.214 | 1.43% | 0.000% |
| cetes_100 | 2007-05-31 | 2026-07-31 | 230 | 6.39% | 0.71% | 0.000 | 0.00% | inf | 6.39% | 0.000% |

Diferencias de volatilidad (series brutas; IC por *bootstrap* de bloques pareado), razón de mínima varianza y *carry*:

| segmento | n | vol(h=1) − vol(h=0) | IC95 bootstrap pareado | h mín. varianza (sin recortar) | media f ×12 | media x ×12 | media (f − x) ×12 | t NW(6) / t IID |
|---|---|---|---|---|---|---|---|---|
| completo | 391 | -0.56% | [-5.52%, 3.32%] | 0.547 | 8.22% | 6.17% | 2.05% | 0.79 / 0.83 |
| dentro_muestra | 161 | -4.40% | [-13.42%, 2.59%] | 0.785 | 13.13% | 10.43% | 2.70% | 0.56 / 0.59 |
| fuera_muestra | 230 | 2.60% | [0.00%, 5.21%] | 0.227 | 4.79% | 3.19% | 1.59% | 0.56 / 0.58 |

h dinamica (P6, recortada [0,1]) desde 1997-01-31: {"desde": "1997-01-31", "n": 355, "min": 0.5408, "mediana": 0.6145, "max": 0.9253, "crudo_min": 0.5408, "crudo_mediana": 0.6145, "crudo_max": 0.9253, "frac_en_cero": 0.0, "ultimo": 0.5465, "ultimo_crudo": 0.5465}

**H4 queda refutada según el criterio pre-registrado.** En la muestra completa, vol(h = 1) = 16.15% es **menor** que vol(h = 0) = 16.71% (-0.56 pp). El IC de la diferencia es [-5.52%, 3.32%], así que no se distingue de cero.

- Dentro de muestra, cubrir **redujo** la volatilidad 4.40 pp.
- Fuera de muestra la **aumentó** 2.60 pp, con IC [0.0015%, 5.21%]: el límite inferior está prácticamente en cero.
- La caída máxima sí fue más profunda cubierto: −48.70% contra −39.86% en la muestra completa (-8.84 pp) y −48.70% contra −29.97% fuera de muestra (-18.73 pp).
- La volatilidad no crece de forma monótona con h: es mínima en h = 0.5 en la muestra completa (14.85%) y en h = 0.25 fuera de muestra (13.48%).
- La razón de mínima varianza es inestable: 0.547 en la muestra completa, 0.785 dentro y 0.227 fuera. El rango esperado era ≤ 0.25.

Por qué se refuta (análisis post-hoc):

- En dic-1994 el USD/MXN subió **45.35%**, y el mercado de EUA medido en pesos ganó **+47.24%** en ese mes.
- De 1994-01 a 1995-12, la volatilidad sin cubrir fue de 37.15% contra 13.11% cubierta.
- En la ventana 1996-2026, que empieza donde empezaba el capítulo, el orden se invierte: 14.0% sin cubrir contra 16.2% cubierto (tabla 11.2).
- La volatilidad castiga igual los saltos a favor. En un choque de origen mexicano, la exposición en USD **sube** el valor en pesos.
- La peor caída sin cubrir de toda la muestra (−39.86%) fue de **2000-06 a 2002-09**, en el mercado bajista de EUA. En esos meses el mercado cayó −42.04% en USD y el USD/MXN solo subió 3.7% (de 9.843 a 10.212). La peor caída cubierta (−48.70%) fue de 2007-10 a 2009-02.

**H5 (secundaria) se cumple en signo y rango, sin significancia.** Cubrir rindió **+2.38 pp** anuales más que no cubrir en la muestra completa (19.29% contra 16.92%). La media de (f − x) fue 2.05% anual, con t NW(6) = 0.79 y t IID = 0.83: la ventaja no es estadísticamente distinguible de cero. Fuera de muestra fue +1.33 pp de CAGR y 1.59% de media, con t NW 0.56.

#### 11.6 H6: el benchmark del sistema (50% acciones de EUA + 50% CETES)

- **Muestra completa:** `bench50_h000` tuvo volatilidad de 8.67% y caída máxima de **−11.87%**. `bench50_h100` tuvo 8.54% y **−23.67%**.
- **Fuera de muestra:** 6.86% y −11.87% sin cubrir, contra 8.17% y −23.67% cubierto.
- **H6 se cumple fuera de muestra** en volatilidad y en caída. En la muestra completa solo se cumple en caída: por 0.13 pp, la volatilidad fue menor cubierta.
- Contra `config/parametros.json`: el benchmark sin cubrir quedó dentro de `drawdown_objetivo` (0.12). El cubierto **rebasó `drawdown_maximo_duro` (0.20)**.

#### 11.7 H7: cobertura dinámica de mínima varianza (P6)

- Estimada con datos que incluyen 1994-95, la h expansiva quedó entre 0.54 y 0.93 desde 1997.
- Fuera de muestra, P6 tuvo +0.69 pp de volatilidad y -14.04 pp de caída máxima frente a no cubrir (14.44% y −44.01%, contra 13.75% y −29.97%).
- **H7 se cumple:** P6 no reduce la volatilidad. Por la regla pre-registrada, **P6 se descarta**.

#### 11.8 Cifras del capítulo 16 recalculadas a su manera (S3b: `^GSPC` precio × DEXMXUS)

| ventana | corr(r, Δln S) propia | capítulo | ±0.05 | vol USD / MXN propia | capítulo | ±0.5 pp |
|---|---|---|---|---|---|---|
| 1996-2026 | -0.502 | -0.50 | sí | 15.3% / 13.6% | 15.3% / 13.6% | sí |
| 2008-2026 | -0.558 | -0.56 | sí | 15.7% / 13.5% | 15.6% / 13.4% | sí |
| 2016-2026 | -0.415 | -0.42 | sí | 15.2% / 15.0% | 15.0% / 14.9% | sí |
| 2023-2026 | -0.437 | -0.44 | sí | 12.7% / 12.0% | 12.3% / 11.6% | sí |

A3 (meses con ^GSPC < -5%, 1996-01 a 2026-07): n=40 (capítulo 40); R USD -7.78% (−7.8%); x 3.68% (+3.7%); MXN -4.46% (−4.5%); dentro de ±1 pp: sí

| ventana | base a fin | CAGR USD / MXN / USD-MXN propio | capítulo | ±0.30 pp |
|---|---|---|---|---|
| 1996-2026 | 1995-12-31 a 2026-07-31 | 8.51% / 11.41% / 2.67% | 8.17% / 11.06% / 2.67% | no |
| 2016-2026 | 2015-12-31 a 2026-07-31 | 13.06% / 13.14% / 0.07% | 13.48% / 11.41% / -1.82% | no |

| ventana | serie | MDD en la ventana | pico | valle | cambio entre pico y valle de USD | cambio punta a punta |
|---|---|---|---|---|---|---|
| crisis_financiera | usd | -56.8% | 2007-10-09 | 2009-03-09 | -56.8% | -25.8% |
| crisis_financiera | mxn_sin_cubrir | -39.8% | 2007-10-09 | 2008-11-20 | -38.6% | -10.2% |
| anio_2008 | usd | -48.8% | 2007-12-31 | 2008-11-20 | -48.8% | -38.5% |
| anio_2008 | mxn_sin_cubrir | -36.3% | 2007-12-31 | 2008-11-20 | -36.3% | -22.1% |
| 2020 | usd | -33.9% | 2020-02-19 | 2020-03-23 | -33.9% | 16.3% |
| 2020 | mxn_sin_cubrir | -15.0% | 2020-02-20 | 2020-03-16 | -10.7% | 22.6% |
| 2022 | usd | -25.4% | 2022-01-03 | 2022-10-12 | -25.4% | -19.4% |
| 2022 | mxn_sin_cubrir | -27.4% | 2022-01-03 | 2022-10-11 | -27.4% | -23.4% |

A4 crisis_financiera: propio -56.8% / -39.8%; capítulo -56.8% / -39.8%; ±1 pp: sí
A4 2020: propio -33.9% / -15.0%; capítulo -33.9% / -15.0%; ±1 pp: sí
A4 2022: propio -25.4% / -27.4%; capítulo -25.4% / -27.4%; ±1 pp: sí

| episodio | desde | hasta | usd | mxn_sin_cubrir |
|---|---|---|---|---|
| Lehman | 2008-09-12 | 2009-03-09 | -46.0% | -21.4% |
| COVID | 2020-02-19 | 2020-03-23 | -33.9% | -10.7% |

- A1, A2, A3 y A4 se reproducen dentro de tolerancia. A4 coincide al décimo de punto: −56.8/−39.8, −33.9/−15.0 y −25.4/−27.4.
- A6 **no** se reproduce. En 1996-2026 salen 8.51% en USD y 11.41% en MXN, contra 8.17% y 11.06% del capítulo; el USD/MXN coincide (2.67%). En 2016-2026, el USD/MXN da +0.07% anual contra −1.82% del capítulo.
- Las fechas exactas del capítulo no están documentadas, así que la diferencia de A6 queda **no explicada**.
- A5 (indicativa): COVID coincide (−33.9% y −10.7%). Lehman da −46.0% y −21.4%, contra −46.6% y −18.2% del capítulo, que no documenta su fecha de inicio.

#### 11.9 Veredicto por hipótesis

| Hipótesis | Resultado | ¿Se cumple? |
|---|---|---|
| H1 correlación | −0.370, IC [−0.571, −0.211]; negativa en los 4 segmentos | Sí |
| H2 caídas grandes | x = +3.68%, A = 0.411; peor decil x = +3.65%, A = 0.413 | Sí |
| H3 crisis | +16.2 pp (2007-09), +18.0 pp (2020), −2.0 pp (2022) | Sí |
| **H4 la cobertura aumenta el riesgo** | Volatilidad: −0.56 pp en completo (**refutación**), −4.40 pp dentro, +2.60 pp fuera. Caída máxima: −8.8 pp en completo y −18.7 pp fuera. Monotonía: no. h* = 0.547 | **Refutada** |
| H5 costo de no cubrir | +2.38 pp de CAGR; (f − x) = 2.05%/año, t NW 0.79 | Signo y rango sí; significancia no |
| H6 benchmark 50/50 | Fuera: vol y caída menores sin cubrir. Completo: solo la caída | Sí fuera de muestra |
| H7 regla dinámica | +0.69 pp de volatilidad y −14.0 pp de caída fuera de muestra | Sí (P6 se descarta) |
| Tolerancias del capítulo | A1 4/4, A2 4/4, A3 sí, A4 3/3, A6 0/2 | No (falla A6) |

Estado que asigna el script con las reglas pre-registradas: **No replicado**. Decisión operable que asigna el script: **descarta**, con el conflicto descrito en las desviaciones.

### 12. Sensibilidad

Todas son `es_prueba=0`. Tablas completas en `R08-salida.txt`.

| Sensibilidad | vol h = 0 / h = 1 (completo) | vol h = 0 / h = 1 (fuera) | MDD h = 0 / h = 1 (completo) | ¿Cambia algo? |
|---|---|---|---|---|
| Principal (DEXMXUS, CETES Banxico, French) | 16.71% / 16.15% | 13.75% / 16.35% | −39.86% / −48.70% | — |
| S1 FIX de Banxico | 16.74% / 16.15% | 13.72% / 16.35% | −39.64% / −48.68% | No. corr = −0.368 |
| S2 desde 1991-12 con FIX | 16.41% / 15.84% | 13.72% / 16.35% | −39.64% / −48.68% | No. corr 1991-2026 = −0.363, IC [−0.570, −0.209]. En bandas (1991-12 a 1994-11, n = 36): −0.323 |
| S3a `^SP500TR` | 16.49% / 15.71% | 13.41% / 15.87% | −40.05% / −49.31% | No. corr = −0.366; correlación con French: 0.989 |
| S4 tasas interbancarias (desde 1997-02) | 14.05% / 16.33% | 13.75% / 16.38% | −39.86% / −49.43% | **Sí, en el orden de la volatilidad.** Sin 1994-96, cubrir la aumenta 2.3 pp. (f − x) = 3.47%/año, t NW 1.65 |
| S5 CETES del FMI | 16.71% / 16.14% | 13.75% / 16.35% | −39.86% / −48.76% | No |
| S6 costo de cobertura de 0.5% y 1.0% anual | vol igual | vol igual | h = 1: −49.05% y −49.41% | CAGR de h = 1 en completo: 19.29% → 18.70% → 18.12% (h = 0: 16.92%). Fuera de muestra: 14.89% → 14.32% → 13.76% (h = 0: 13.56%) |
| S7 spread "medio" 0.15% | vol igual | vol igual | igual | CAGR −0.01 a −0.02 pp: con comprar y mantener solo se paga la entrada |
| S8 diario (cobertura renovada a diario) | 20.83% / 18.77% | 19.69% / 20.17% | −45.67% / −51.66% | Mismo patrón. La correlación diaria asincrónica es de −0.228 (DEXMXUS al mediodía contra el cierre) |

S3a (`^SP500TR`), fuera de muestra:

| variante | inicio (base) | fin | n | CAGR | vol | Sharpe vs efectivo | MDD | Calmar | CAGR efectivo | costo anual |
|---|---|---|---|---|---|---|---|---|---|---|
| mxn_h000_sp500tr | 2007-05-31 | 2026-07-31 | 230 | 13.52% | 13.41% | 0.550 | -31.22% | 0.433 | 6.39% | 0.000% |
| mxn_h100_sp500tr | 2007-05-31 | 2026-07-31 | 230 | 14.89% | 15.87% | 0.567 | -49.31% | 0.302 | 6.39% | 0.000% |
| usd_referencia_sp500tr | 2007-05-31 | 2026-07-31 | 230 | 10.73% | 15.58% | 0.643 | -50.95% | 0.211 | 1.43% | 0.000% |

S4 (tasas interbancarias), fuera de muestra:

| variante | inicio (base) | fin | n | CAGR | vol | Sharpe vs efectivo | MDD | Calmar | CAGR efectivo | costo anual |
|---|---|---|---|---|---|---|---|---|---|---|
| mxn_h000_desde1997 | 2007-05-31 | 2026-07-31 | 230 | 13.56% | 13.75% | 0.543 | -29.97% | 0.452 | 6.39% | 0.000% |
| mxn_h050_interbancaria | 2007-05-31 | 2026-07-31 | 230 | 14.47% | 13.88% | 0.598 | -40.14% | 0.360 | 6.39% | 0.000% |
| mxn_h100_interbancaria | 2007-05-31 | 2026-07-31 | 230 | 14.96% | 16.38% | 0.558 | -49.43% | 0.303 | 6.39% | 0.000% |

S6 (costo de la cobertura), fuera de muestra:

| variante | inicio (base) | fin | n | CAGR | vol | Sharpe vs efectivo | MDD | Calmar | CAGR efectivo | costo anual |
|---|---|---|---|---|---|---|---|---|---|---|
| mxn_h025_costo050 | 2007-05-31 | 2026-07-31 | 230 | 13.91% | 13.48% | 0.574 | -35.04% | 0.397 | 6.39% | 0.000% |
| mxn_h050_costo050 | 2007-05-31 | 2026-07-31 | 230 | 14.15% | 13.87% | 0.578 | -39.93% | 0.354 | 6.39% | 0.000% |
| mxn_h075_costo050 | 2007-05-31 | 2026-07-31 | 230 | 14.29% | 14.86% | 0.558 | -44.60% | 0.320 | 6.39% | 0.000% |
| mxn_h100_costo050 | 2007-05-31 | 2026-07-31 | 230 | 14.32% | 16.35% | 0.524 | -49.05% | 0.292 | 6.39% | 0.000% |
| mxn_hminvar_exp36_costo050 | 2007-05-31 | 2026-07-31 | 230 | 13.96% | 14.44% | 0.549 | -44.30% | 0.315 | 6.39% | 0.000% |
| bench50_h100_costo050 | 2007-05-31 | 2026-07-31 | 230 | 10.63% | 8.17% | 0.520 | -23.93% | 0.444 | 6.39% | 0.037% |
| mxn_h025_costo100 | 2007-05-31 | 2026-07-31 | 230 | 13.77% | 13.48% | 0.565 | -35.15% | 0.392 | 6.39% | 0.000% |
| mxn_h050_costo100 | 2007-05-31 | 2026-07-31 | 230 | 13.87% | 13.87% | 0.560 | -40.13% | 0.346 | 6.39% | 0.000% |
| mxn_h075_costo100 | 2007-05-31 | 2026-07-31 | 230 | 13.87% | 14.86% | 0.533 | -44.88% | 0.309 | 6.39% | 0.000% |
| mxn_h100_costo100 | 2007-05-31 | 2026-07-31 | 230 | 13.76% | 16.35% | 0.494 | -49.41% | 0.278 | 6.39% | 0.000% |
| mxn_hminvar_exp36_costo100 | 2007-05-31 | 2026-07-31 | 230 | 13.62% | 14.45% | 0.528 | -44.60% | 0.305 | 6.39% | 0.000% |
| bench50_h100_costo100 | 2007-05-31 | 2026-07-31 | 230 | 10.35% | 8.17% | 0.489 | -24.19% | 0.428 | 6.39% | 0.037% |

**S9: el instrumento cubierto real, IVVPESO (2014-12 a 2026-07, mensual)**

| variante | inicio (base) | fin | n | CAGR | vol | Sharpe vs efectivo | MDD | Calmar | CAGR efectivo | costo anual |
|---|---|---|---|---|---|---|---|---|---|---|
| ivvpeso_real | 2014-11-30 | 2026-07-31 | 140 | 15.49% | 15.47% | 0.562 | -22.71% | 0.682 | 7.22% | 0.029% |
| sp500tr_mxn_h100_sintetico | 2014-11-30 | 2026-07-31 | 140 | 18.46% | 15.18% | 0.740 | -21.20% | 0.871 | 7.22% | 0.029% |
| sp500tr_mxn_h000 | 2014-11-30 | 2026-07-31 | 140 | 15.74% | 14.62% | 0.597 | -25.42% | 0.619 | 7.22% | 0.029% |

corr(IVVPESO, cubierto sintetico) = 0.986; corr(IVVPESO, sin cubrir) = 0.689; error de seguimiento anual = 2.60%; media de la diferencia x12 = -2.53%; meses con precio de mas de 3 dias = 0 (max 3 dias)

| ventana | IVVPESO | S&P TR cubierto sintético | S&P TR sin cubrir |
|---|---|---|---|
| 2020 | -22.1% | -21.2% | -8.9% |
| 2022 | -22.7% | -20.5% | -25.3% |

- IVVPESO se movió como la cobertura sintética (correlación de 0.986), pero rindió **2.53 pp anuales menos** (media × 12), con un error de seguimiento de 2.60%.
- **Contra el S&P 500 TR sin cubrir, IVVPESO rindió 15.49% contra 15.74%**, con más volatilidad (15.47% contra 14.62%). En este tramo tuvo menor caída máxima (−22.7% contra −25.4%), porque 2022 fue un año de choque de tasas.
- En 2020, IVVPESO cayó −22.1% (mensual) y el S&P sin cubrir −8.9%.
- **Contraste post-hoc con la ficha oficial de BlackRock (al 31-ago-2026).** La rentabilidad anualizada del NAV desde su creación es de **15.77%**, contra **18.96%** de su índice (S&P 500 100% MXN Hedged). A 10 años: 17.37% contra 20.91%. A 5 años: 14.51% contra 18.69%. En 2022: −17.15% contra −12.85%. La comisión de gestión es de 0.49%.
- **La brecha contra el índice es del emisor, no un defecto de los datos de Yahoo.** La comisión explica 0.49 pp. El resto (unos 2.7 pp anuales) queda **no explicado** aquí; candidatos no verificados: retenciones sobre dividendos, costo de ejecución de los *forwards* y efectivo.

### 13. Diferencia frente al artículo y al capítulo

| Aspecto | Campbell et al. (2010) | Capítulo 16 §5.4 | Réplica R08 | ¿Explica la diferencia? |
|---|---|---|---|---|
| Inversionista y monedas | Siete monedas desarrolladas; cartera global de acciones con pesos iguales; **sin MXN** | Mexicano, S&P 500 | Mexicano, mercado de EUA (CRSP) | El artículo solo aporta el mecanismo |
| Datos / versión | Rendimientos trimestrales (detalle de fuentes no verificado aquí) | `^GSPC` **precio** × DEXMXUS | French CRSP 202607 **rendimiento total** × DEXMXUS; S3b reproduce el cálculo del capítulo | Los dividendos cambian el CAGR, no las correlaciones ni las caídas |
| Periodo | 1975-2005 | "1996-2026" y otras, sin fechas exactas | 1994-01 a 2026-07 (S2 desde 1991-12) | **Sí.** Empezar en 1994 incluye la devaluación de 1994-95, que produce la refutación de H4. Empezando en 1996, la conclusión del capítulo sobre volatilidad sí se sostiene |
| Medida de riesgo | Desviación estándar | Volatilidad, caídas y episodios | Volatilidad (criterio de H4), caída máxima y medias condicionales | Parcial: la volatilidad castiga los saltos a favor en pesos; la caída máxima no |
| Resultado principal | EUA: sin cubrir 15.05%, cobertura total 13.86%, óptima 12.51%. Canadá: la cobertura total **aumenta** el riesgo (13.74% → 13.86%) | Cubrir aumenta el riesgo del mexicano | 1994-2026: cubrir **reduce** la volatilidad 0.56 pp (no significativo) y aumenta la caída 8.8 pp. 2007-2026: la aumenta 2.60 pp y aumenta la caída 18.7 pp. h* = 0.55 (completo), 0.79 (dentro) y 0.23 (fuera) | Es el caso "Canadá" fuera de muestra, más extremo, pero no en toda la muestra. Como en el artículo, la cobertura óptima es parcial e inestable entre submuestras |
| Costos | No revisado en esta réplica | Sin costos | Comisión GBM + spread; costo de cobertura como sensibilidad; ETF real (S9) | Con el ETF real, el *carry* teórico no llegó al inversionista |

### 14. Conclusiones permitidas

Alcance: mercado accionario de EUA (CRSP; S&P 500 TR como sensibilidad), mensual 1994-01 a 2026-07, DEXMXUS (mediodía en Nueva York; no es un precio ejecutable en GBM), CETES 28, costos de GBM sin spread cambiario ni impuestos.

1. **Rendimiento.** El mercado de EUA rindió 10.92% anual en USD y 16.93% en MXN sin cubrir (1994-2026). La diferencia es la depreciación del peso: 5.41% anual, de 3.108 (1993-12-30) a 17.3235 (2026-07-31). El 53% del cambio logarítmico ocurrió en 1994-95, cuando pasó de 3.108 a 7.74 (post-hoc). En 2007-2026 fue de 10.76% en USD y 13.56% en MXN.
2. **El peso se deprecia cuando caen las acciones de EUA.** La correlación mensual es de −0.370 en 1994-2026 (IC [−0.571, −0.211]) y de −0.557 desde 2007-06. En los meses con caída de más de 5% (n = 38), el USD/MXN subió en promedio 3.68% y la pérdida en pesos fue 41% menor. La relación es simétrica: en los meses de alza grande el peso se aprecia y el inversionista en pesos gana menos.
3. **Choques globales.** En 2007-09 la caída en MXN sin cubrir fue de −38.3%, contra −54.6% en USD. En 2020 fue de −16.2% contra −34.2% (diario, rendimiento total).
4. **Choques no globales.** En 2022, un choque de tasas, fue −27.5% contra −25.4%. En el mercado bajista de 2000-06 a 2002-09, el USD/MXN solo subió 3.7% y la caída sin cubrir llegó a −39.9% (−42.0% en USD).
5. **Fuera de muestra (2007-06 a 2026-07), cubrir al 100% aumentó el riesgo.** La volatilidad subió +2.60 pp, con IC que apenas excluye el 0, y la caída máxima fue de −48.7% contra −30.0%. En el benchmark 50/50 del sistema, la caída máxima fue de −23.7% cubierto contra −11.9% sin cubrir, y la versión cubierta habría rebasado el `drawdown_maximo_duro` de 20%.
6. **En toda la muestra 1994-2026, cubrir no aumentó la volatilidad** (−0.56 pp, IC [−5.5, +3.3] pp), por la devaluación de 1994-95. Con la caída máxima como medida, cubrir sí fue peor (−48.7% contra −39.9%).
7. **La razón de cobertura "óptima" es inestable** (0.79 en 1994-2007 y 0.23 en 2007-2026). Estimarla con la historia disponible (P6) empeoró la volatilidad y la caída fuera de muestra.
8. **El costo de no cubrir** fue de +2.05% anual de *carry* teórico en 1994-2026, sin significancia (t NW 0.79). **El ETF cubierto real (IVVPESO) no entregó ese *carry*:** rindió 15.49% contra 15.74% del S&P TR sin cubrir en 2014-12 a 2026-07, y el emisor reporta 3.19 pp anuales por debajo de su índice desde la creación.
9. Las cifras del capítulo 16 sobre correlación, volatilidad, meses de caída y caídas de 2008, 2020 y 2022 (A1 a A4) **se reproducen** con su propio método. Las de CAGR (A6) no.

### 15. Conclusiones que NO se sostienen

- **"Cubrir el dólar siempre aumenta el riesgo"** o **"el dólar siempre reduce la volatilidad del mexicano".** En 1994-2026 la cobertura total tuvo menor volatilidad, por la crisis de origen mexicano de 1994-95. La afirmación del capítulo depende de empezar en 1996.
- **"La cobertura natural protege en cualquier mercado bajista".** Falló en 2022 y en 2000-2002. Funcionó con fuerza en los choques globales de aversión al riesgo (1998-08, 2008-09, 2008-10, 2009-02 y 2020-03 en la tabla de peores meses); en 2000-11 y 2018-12 el peso se apreció y la caída en pesos fue mayor; en 2001-02 casi no amortiguó (−9.52% en MXN contra −9.65% en USD).
- **"La correlación del peso con las acciones es estable en −0.5".** Fue −0.17 en 1994-2007 y −0.56 en 2007-2026.
- **"Cubrir es mejor ajustado por riesgo"** (el Sharpe contra CETES de h = 1 es 0.535, contra 0.383 de h = 0). La ventaja de *carry* no es significativa, depende de 1994-2007, se reduce fuera de muestra (0.555 contra 0.543) y no se materializó con el instrumento real.
- **"Hay una razón de cobertura óptima utilizable"** (0.5, 0.25 o cualquier otra). Es inestable, y la regla dinámica perdió fuera de muestra.
- **"Esto vale para la cuenta arena"** (temporadas de 6 meses, medidas contra rivales). No se probó.
- **"Es ejecutable tal cual en GBM".** DEXMXUS no es un precio de GBM. El spread cambiario implícito del SIC, los impuestos (ISR de 10% y retenciones) y la disponibilidad de IVVPESO e IVV en GBM no están verificados.
- **"Replicado", "funcionará en el futuro" o "tiene ventaja con dinero real".** Nada de esto se sostiene. El DSR de la variante elegida es de 0.88, debajo de 0.95, aunque aquí no es el criterio.

### 16. Estado y reproducción

- **Estado: No replicado**, según el criterio pre-registrado: la refutación de H4 en la muestra completa ("vol(h = 1) ≤ vol(h = 0) en la muestra completa o en `fuera_muestra`" → 16.15% ≤ 16.71%).
  - Matiz obligatorio: H1, H2, H3 y H6 (fuera de muestra) sí se cumplen, y A1 a A4 del capítulo se reproducen.
  - Lo que no se sostiene es la generalización "cubrir aumenta el riesgo" en toda la muestra desde 1994, ni las cifras de CAGR (A6).
  - Diferencias no explicadas: A6 (fechas del capítulo) y unos 2.7 pp anuales de la brecha de IVVPESO contra su índice, además de su comisión.
- Comando que reproduce todo: `python3 laboratorio/replicas/R08.py` (desde `/home/user/New1`). Sin red: lee `R08-datos/` y verifica `SHA256SUMS.txt`. Prueba del código sin datos reales: `python3 laboratorio/replicas/R08.py --prueba-sintetica`.
- Huella del pre-registro (secciones 1 a 9): `b3364065cc61a703daface2964d14bd49769f437a06ab0b549844975faca47e5`, verificada por el script en cada corrida.
- `huella_datos` en el CSV: `d93425e0e4741dff` (P1 y P7) y `0fba6fc05d1b0c8b` (P5).
- French: `F-F_Research_Data_Factors_CSV.zip`, CRSP 202607, sha256 `b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb`; `_daily_CSV.zip`, sha256 `1916d331c2c51d2aee3d00215897d2b8e5995cb387f1f4569ba46bff5fb049a8`.
- Resto de las huellas: `R08-datos/SHA256SUMS.txt`.
- Fecha de la corrida final: 2026-09-25 06:56 UTC.
- Revisión independiente (`auditor-de-replicas`): pendiente. No hay segunda implementación con código independiente. La segunda fuente de datos (S1 FIX, S3a `^SP500TR`) solo concuerda con los mismos cálculos.

#### Conclusión operable

La regla bajo prueba es la del capítulo 16: §6.2, regla 4 ("Acciones de EUA: nunca se cubren en el patrimonio principal"), y §6.4 ("acciones globales, horizonte de más de 1 año: no cubrir").

1. **Salida literal de las reglas pre-registradas: conflicto.**
   - Se cumplen las cuatro condiciones de "se confirma" fuera de muestra:
     - H1: −0.557, IC que excluye el 0.
     - H3: +16.2 pp y +18.0 pp.
     - H4 fuera de muestra: +2.60 pp de volatilidad y −18.7 pp de caída.
     - H6 fuera de muestra.
   - También se cumple la condición de "se descarta": H4 refutada en la muestra completa.
   - El script da precedencia a "descarta".
2. **Resolución (post-hoc, declarada): se DESCARTA la forma absoluta ("nunca") y se propone MODIFICAR la regla a:**
   > "Por defecto, no cubrir el tipo de cambio de la renta variable de EUA en el patrimonio principal. El motivo es **controlar caídas en choques globales de aversión al riesgo**: en 2008 y 2020 hubo 16-18 pp menos de caída en MXN, y el benchmark 50/50 cayó −11.9% sin cubrir contra −23.7% cubierto. **No es una regla de menor volatilidad en todo régimen.** Hay tres excepciones documentadas. (a) En choques de origen mexicano (1994-95), el USD sube el valor en pesos: agrega volatilidad, pero a favor, así que ahí la justificación por "menor volatilidad" no aplica. (b) En mercados bajistas de EUA con el peso casi estable no protege (2000-06 a 2002-09: USD/MXN +3.7% y −39.9% en MXN). (c) En choques de tasas con Banxico más restrictivo que la Fed tampoco protege (2022: −27.5% en MXN contra −25.4% en USD). No se usa cobertura dinámica por mínima varianza. Si se cubre por un pasivo en MXN, el costo real de IVVPESO se trata como unos 3 pp anuales contra su índice, no como el *carry* teórico."
3. **Qué NO cambia:** `config/parametros.json` no se modificó. La propuesta es una hipótesis para una nueva prueba pre-registrada; no es una regla replicada. La prueba siguiente tendría como métrica principal la caída máxima o la pérdida condicional en MXN (en lugar de la volatilidad) y un tramo nuevo de datos (2026-08 en adelante), o la misma pregunta con otras monedas emergentes.
4. **Regla sencilla:** no cubrir (P1) es la regla sencilla de este caso. Ninguna cobertura fija ni la dinámica la superó fuera de muestra en caída máxima.
