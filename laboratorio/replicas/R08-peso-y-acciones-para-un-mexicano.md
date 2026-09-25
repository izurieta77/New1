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
| Estado | (se llena al final) |

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

### Desviaciones del pre-registro

| Fecha | Qué cambió | Por qué | ¿Invalida el tramo de prueba? |
|---|---|---|---|

### 10. Variantes probadas

(pendiente)

### 11. Resultados

(pendiente)

### 12. Sensibilidad

(pendiente)

### 13. Diferencia frente al artículo y al capítulo

(pendiente)

### 14. Conclusiones permitidas

(pendiente)

### 15. Conclusiones que NO se sostienen

(pendiente)

### 16. Estado y reproducción

(pendiente)
