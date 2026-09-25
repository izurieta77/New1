# Módulo 04 — Renta fija, tasas y macroeconomía para inversionistas: duración, curva, crédito, r* y el régimen de correlación

> Nivel: maestría · Actualizado: 2026-09-25 · Grado de evidencia global: **B**. La matemática es exacta y la estructura de tres factores de la curva es grado A (98.4% de la varianza en el cálculo propio 1993-2026). Lo que sirve para *predecir* (curva→recesión, term premium, carry, r*, factores de crédito) es B o C: en 2022-2024 la curva dio su falso positivo más largo, y solo el 6% de 432 especificaciones de factores de bonos corporativos sobrevive a datos corregidos (Dickerson-Robotti-Rossetti 2026).

Convenciones: "cálculo propio" = datos de FRED, NY Fed o Yahoo descargados el 25-sep-2026. EUA salvo que se indique otra cosa. Los ETFs son netos de su comisión y brutos de costos de transacción e impuestos.

---

## 1. Objetivos de dominio (qué debe saber hacer quien "se titula" en este módulo)

1. Valuar un bono con cupón y un CETE. Calcular a mano la duración Macaulay y la modificada, la convexidad y el DV01, y estimar ±100 y ±200 pb con y sin convexidad.
2. Construir las curvas spot y forward, y replicar con PCA nivel, pendiente y curvatura (Litterman-Scheinkman 1991).
3. Descomponer un rendimiento largo en tasa esperada + term premium (ACM, Kim-Wright), y calcular el carry, el roll-down y el colchón de tasa.
4. Evaluar la curva invertida como predictor de recesión (Harvey; Estrella-Mishkin) con su historial y el caso 2022-2024.
5. Descomponer un spread de crédito (Merton 1974, credit spread puzzle) y tratar el HY como exposición a factores.
6. Leer TIPS, breakevens y UDIBONOS, y saber qué contamina al breakeven.
7. Estimar la postura monetaria con Taylor y r* (LW, HLW), y cuantificar QE/QT por canales.
8. Explicar el cambio de signo de la correlación acciones-bonos (Campbell-Pflueger-Viceira 2020) y el 60/40 de 2022.
9. Clasificar el régimen macro, leer indicadores adelantados y evaluar lo fiscal y la oferta de Treasuries.
10. Aplicar todo a CETES, Bonos M, UDIBONOS y Bondes F en MXN.

---

## 2. Núcleo teórico

### 2.1 Precio y rendimiento

- Bono con cupón c, pago f veces al año, rendimiento y y N periodos: P = Σ_{k=1..N} (c/f)·F/(1+y/f)^k + F/(1+y/f)^N. Precio y rendimiento se mueven en sentido contrario, y la relación es convexa.
- El YTM es la TIR del bono. Supone reinvertir los cupones a la misma y, así que solo un cupón cero mantenido al vencimiento lo realiza exacto.
- **CETES:** son cupón cero a descuento con valor nominal de $10 y plazos de 28, 91, 182, 364 y 728 días (Cetesdirecto). Con la convención mexicana de 360 días, P = 10/(1 + r·t/360).
- **Bonos M:** tasa fija con cupón semestral (cada 182 días) y plazos de 3, 5, 10, 20 y 30 años. **UDIBONOS:** denominados en UDIs, con tasa real fija semestral, así que el principal se ajusta por inflación. **Bondes F:** cupón cada 28 días ligado a la TIIE de Fondeo, a plazos de 1 a 10 años (Cetesdirecto).

> **Adenda 2026-09-25 (examen diagnóstico S4-02, ficha `conocimiento/fichas/2026-09-25-examen-S1-S5-huecos.md`): TIIE de Fondeo a un día.** Es la tasa de referencia libre de riesgo en pesos que publica Banxico desde enero de 2020 (con historia reconstruida desde 2006), calculada como la **mediana ponderada por volumen** de las operaciones de reporto a un día hábil con valores del **Gobierno Federal, el IPAB y el propio Banxico** (no incluye colateral bancario) que pactan bancos y casas de bolsa, liquidadas en Indeval, excluyendo operaciones entre partes relacionadas. Sigue de cerca el objetivo de Banxico para la tasa interbancaria a un día. Por la **Circular 3/2023** de Banxico, las TIIE a plazo (que se fijaban con posturas/cotizaciones bancarias, no con transacciones) se descontinúan para contratos nuevos: TIIE a **91 y 182 días desde el 1-ene-2024**, TIIE a **28 días desde el 1-ene-2025**. Los contratos nuevos referencian la TIIE de Fondeo compuesta al plazo correspondiente **más un diferencial promedio de ~24 pb** (metodología de respaldo, al estilo de la reforma LIBOR→SOFR). Fuentes: IMEF, https://www.revista.imef.org.mx/articulo/la-nueva-tasa-de-referencia-tiie-de-fondeo/ ; BDO México (resumen de la Circular 3/2023), https://www.bdomexico.com/es-mx/publicaciones/boletines-de-precios-de-transferencia/2025/tiie-de-fondeo ; Banxico, serie SIE CA684. La fecha exacta de "publicación desde enero de 2020, historia desde 2006" queda **(no verificada de forma primaria contra banxico.org.mx en esta tarea)**; se apoya en las dos fuentes secundarias citadas.

### 2.2 Duración, convexidad y DV01

- **Macaulay:** D_Mac = Σ t_k·PV(CF_k)/P, el plazo promedio ponderado de los flujos (Macaulay 1938).
- **Modificada:** D_mod = D_Mac/(1+y/f). Da la sensibilidad porcentual: ΔP/P ≈ −D_mod·Δy.
- **Convexidad:** C = (1/P)·∂²P/∂y². Entra en la aproximación de segundo orden: ΔP/P ≈ −D_mod·Δy + ½·C·Δy².
- **DV01** = D_mod·P·0.0001, el cambio de precio por 1 pb. **Duración de un portafolio** = Σ w_i·D_i. **Duración efectiva:** se usa en instrumentos con opciones (MBS, callables), cuya convexidad es negativa.

**Ejemplo (cálculo propio con la curva de EUA del 23-sep-2026).** Un bono a 10 años con cupón de 5% y rendimiento de 5.11% tiene P = 99.147, D_Mac = 7.98, D_mod = 7.78, C = 73.4 y DV01 = 0.0771 por cada 100 (US$771 por millón).

| Δy | Exacto | Solo duración | Duración + convexidad |
|---|---|---|---|
| +100 pb | −7.43% | −7.78% | −7.41% |
| −100 pb | +8.16% | +7.78% | +8.15% |
| +200 pb | −14.19% | −15.56% | −14.09% |

Un bono a 30 años con cupón de 4.75% y rendimiento de 5.40% tiene D_mod = 15.2 y C = 343. Con +100 pb pierde 13.6% y con −100 pb gana 17.0%, así que la asimetría es grande. Un Bono M hipotético a 10 años con cupón de 8% y rendimiento de 9% tiene D_mod = 6.66 y DV01 = 0.062 por 100. A la misma madurez, un cupón y una tasa más altos dan menos duración.

**Intuición:** la duración es el "beta" del bono frente a la tasa, y la convexidad es gamma larga.

### 2.3 La curva: spot, forward, nivel, pendiente, curvatura

- Tasa spot z(t) = rendimiento de un cupón cero. Forward entre t₁ y t₂: (1+z₂)^{t₂} = (1+z₁)^{t₁}·(1+f)^{t₂−t₁}. La curva se ajusta con Nelson-Siegel (1987) o Svensson. La Fed publica la curva de Gürkaynak-Sack-Wright (2007) desde 1961.
- **Litterman-Scheinkman (1991, JFI):** tres factores (nivel, pendiente y curvatura) explican casi toda la variación de los rendimientos de los Treasuries. **Réplica propia** con PCA de los cambios semanales de 1, 2, 3, 5, 7, 10, 20 y 30 años (oct-1993 a sep-2026, n = 1,649):

| Periodo | Nivel (PC1) | Pendiente (PC2) | Curvatura (PC3) | Total |
|---|---|---|---|---|
| 1993-2026 | 86.1% | 10.0% | 2.3% | 98.4% |
| 1993-2007 | 90.0% | 7.2% | 1.4% | 98.6% |
| 2008-2021 (tasa cero y QE) | 82.7% | 12.4% | 2.9% | 98.0% |
| 2022-sep 2026 | 87.8% | 9.7% | 1.7% | 99.2% |

Las cargas de PC1 tienen todas el mismo signo. Las de PC2 van de −0.48 en 1 año a +0.47 en 30 años, y las de PC3 tienen forma de mariposa. *Inferencia:* cubrir solo el nivel con DV01 deja sin cubrir 10-17% de la varianza, y esa porción es mayor con la tasa en su límite inferior.

### 2.4 Hipótesis de expectativas y term premium

y_n,t = (1/n)·Σ E_t[r_{t+i}] + TP_n,t. La hipótesis de expectativas pura (TP constante) se rechaza en los datos. Fama-Bliss (1987) y Campbell-Shiller (1991) muestran que cuando el spread de forwards es alto, los bonos largos rinden de más, en vez de que las tasas suban como anticipaba la curva. Por eso la pendiente contiene prima de riesgo, no solo expectativas.

> **Adenda 2026-09-25 (examen diagnóstico S1-07, ficha `conocimiento/fichas/2026-09-25-examen-S1-S5-huecos.md`).**
> - **Litterman-Scheinkman (1991), JFI 1:54-61 (fuente original, no solo la réplica propia):** los tres factores explican **más de 96%** de la variabilidad de los rendimientos del Tesoro.
> - **Fama-Bliss (1987), AER 77(4):680-692:** con muestra 1965-1985, al regresar el exceso de rendimiento a 1 año sobre el diferencial forward-spot, Cochrane-Piazzesi (2005) reportan un R² de ~18%. Al regresar los **cambios de la tasa de 1 año** (de 1 a 4 años de anticipación) sobre ese mismo diferencial, los coeficientes son **0.09, 0.69, 1.30 y 1.61**, con R² de **0%, 8%, 24% y 48%**: poco poder a 1 año y mucho a 3-4 años, por reversión a la media de la tasa corta.
> - **Cochrane-Piazzesi (2005), AER 95(1):138-160 (texto verificado con `pypdf`/lectura directa del PDF, muestra 1964-2003):** un solo factor en forma de "tienda" (*tent*) construido con 5 forwards predice el exceso de rendimiento a 1 año de bonos de 2 a 5 años con R² de hasta **0.44** (Tabla 5: sube de 0.35 a 0.44 con 3 rezagos). Nivel, pendiente, curvatura, 4º y 5º componente principal explican **98.6%, 1.4%, 0.03%, 0.02% y 0.01%** de la varianza de los *yields*, pero **9.1%, 58.7%, 7.6%, 24.3% y 0.3%** de la varianza del factor CP: el factor depende sobre todo de la pendiente (58.7%), no de componentes "de orden superior" en general. R² de nivel+pendiente = 22%; con curvatura, 26%. Un modelo de tres factores que ajusta bien los *yields* puede omitir información sobre las primas de riesgo. https://web.stanford.edu/~piazzesi/cp.pdf

- **ACM (Adrian-Crump-Moench 2013, JFE):** modelo afín sin arbitraje de 5 componentes principales, estimado por regresiones lineales. **Kim-Wright (2005, FEDS 2005-33):** modelo de 3 factores que usa encuestas.
- **Hoy (cálculo propio con los datos del NY Fed y FRED):** el 23-sep-2026 el rendimiento ajustado a 10 años de ACM es **5.07% = 4.43% de tasa corta esperada + 0.65% de term premium**. El term premium ACM promedió −0.46% en 2023, +0.60% en 2025 y tocó 0.89% el 17-ago-2026. Kim-Wright marcó **0.97% el 16-sep-2026, el máximo desde feb-2011**.
- Del 2-mar al 23-sep-2026 el 10 años ajustado de ACM subió de 4.10% a 5.07%. De esos +97 pb, **+94 pb vienen de la tasa esperada y solo +3 pb del term premium** (0.62% → 0.65%). *Inferencia:* la subida de 2026 es sobre todo la trayectoria esperada de la Fed, no una prima fiscal.

### 2.5 Carry y roll-down

Si la curva no cambia, el rendimiento en exceso de mantener un bono financiado a corto plazo es: carry ≈ (y_n − r_corto) + roll-down, con roll-down ≈ D_mod·(y_n − y_{n−h}) (Koijen-Moskowitz-Pedersen-Vrugt 2018 lo derivan igual). El colchón es cuánto puede subir la tasa en el horizonte antes de que el exceso llegue a cero: Δy* = (carry + roll)/D_mod.

**Ejemplo (23-sep-2026):** 10 años a 5.11% contra 3 meses a 4.19% da carry = 0.92%/año. La pendiente entre 7 y 10 años es de ~2 pb/año, así que el roll ≈ 7.78 × 0.02 = 0.16%. El total es ≈1.08%/año y Δy* ≈ **14 pb en 12 meses**. La σ del cambio anual del 10 años fue de 0.76 pp en 2000-2026 (cálculo propio), así que el colchón equivale a ~0.2σ. *Inferencia:* hoy el carry no protege contra un movimiento normal de tasas.

### 2.6 Riesgo de crédito

- **Merton (1974, JF):** el capital es una call sobre los activos de la empresa, y la deuda riesgosa equivale a deuda libre de riesgo menos una put. El spread sube con el apalancamiento, la volatilidad de los activos y el plazo.
- **Descomposición del spread:** pérdida esperada (PD × LGD) + prima de riesgo + liquidez + impuestos. Elton et al. (2001): el default esperado es una "fracción sorprendentemente pequeña", los impuestos estatales pesan y el resto se parece a una prima de riesgo accionaria. Longstaff-Mithal-Neis (2005), con CDS: la mayor parte es default y el resto, liquidez. Huang-Huang (2012): en IG el crédito explica poco y en HY mucho más (el **credit spread puzzle**).
- **Giesecke et al. (2011, JFE), 1866-2008:** spreads ≈ 2× las pérdidas por default, es decir, una prima de ~80 pb. En 1873-75 los defaults sumaron 36% del valor nominal del mercado.
- **IG vs HY:** en la frontera BBB−/BB+ cambian la base de inversionistas y la liquidez, y el HY se comporta como una mezcla de acciones y Treasuries (§5.4). **Excess bond premium** (Gilchrist-Zakrajšek 2012): la parte del spread no explicada por el default esperado predice actividad y precios, y refleja la capacidad de riesgo del sector financiero.
- **Hoy:** OAS del HY de EUA = 2.73% y OAS de IG = 0.77% (ICE BofA, 23-sep-2026). Son spreads estrechos a pesar del choque de energía de 2026.

### 2.7 Inflación: TIPS, breakevens, UDIBONOS

- Fisher: y_nominal ≈ y_real + E[π] + prima de riesgo inflacionario. **Breakeven** = y_nominal − y_TIPS = E[π] + IRP − prima de liquidez de los TIPS.
- Fleckenstein-Longstaff-Lustig (2014, JF): un Treasury y un TIPS con swap de inflación que replica exactamente sus flujos llegaron a diferir en **más de US$20 por cada 100 nominales**. El mispricing total superó US$56 mil millones (~8% de los TIPS en circulación) y se cerraba cuando entraba capital. El breakeven "puro" es entonces una medida contaminada.
- **Hoy:** breakeven a 10 años de 2.33%, 5y5y forward de 2.33% y rendimiento real a 10 años de 2.76%, el más alto desde nov-2008 (FRED, 23/24-sep-2026). El IPC de EUA está en 3.71% a/a (ago-2026). *Inferencia:* el mercado no extrapola el choque de energía al largo plazo, así que las expectativas siguen ancladas.
- **UDIBONOS:** breakeven MX = Bono M − UDIBONO al mismo plazo. Se compara con la meta de Banxico (3% ±1 pp) y con las encuestas. A plazos cortos, TIPS y UDIBONOS se comportan como duración real, no como cobertura de inflación: el ETF TIP cayó −12.3% en 2022 con la inflación de EUA en máximos de 40 años.

### 2.8 Política monetaria: r*, Taylor, QE/QT

- **r* (tasa natural):** es la tasa real corta compatible con producción en su potencial e inflación estable (Laubach-Williams 2003; Holston-Laubach-Williams 2017, 2023). No es observable. **Estimaciones del NY Fed publicadas el 27-ago-2026 (dato 2026T2):** HLW EUA = **1.01%** (era 1.27% en 2019T4 y 2.61% en 2007T4), zona euro 0.09% y Canadá 1.76%. LW de un solo lado = 1.65%. La tasa de largo plazo de la mediana del FOMC de sep-2026 = 3.2%, que implica un r* de ≈1.2%. La dispersión entre métodos (~0.6 pp) es del tamaño de dos o tres movimientos de la Fed.
- **Taylor (1993):** i = r* + π + 0.5(π − 2) + 0.5·brecha. Taylor usó r* = 2 y el deflactor del PIB. **Aplicación a sep-2026** (variante con el PCE subyacente de 3.34% a/a de jul-2026):
  - r* = 1.01 (HLW) y brecha de −0.11 (HLW): i = 1.01 + 3.34 + 0.67 − 0.055 ≈ **4.97%**.
  - r* = 2 (Taylor original) y la misma brecha: **≈5.96%**.
  - r* = 1.65 y brecha de +1.20 (LW): **6.26%**.
  - Fondos federales: 3.75-4.00% después del alza de 25 pb del 16-sep-2026 (votación 12-0).
  - *Inferencia:* con cualquier r* razonable la Fed está por debajo de Taylor. El propio FOMC proyecta otra alza: mediana del SEP de 4.1% para fin de 2026.
- **Trayectoria:** recortes en sep, oct y dic-2025 (a 3.50-3.75%). En 2026 llegó un choque de energía (conflicto con Irán según el TBAC; Brent de US$138.21 el 7-abr-2026), el IPC pasó de 2.66% (feb) a 4.27% (may) y la Fed subió en septiembre.
- **QE:** Gagnon-Raskin-Remache-Sack (2011): en 8 anuncios de LSAP1 el 10 años bajó 91 pb, y el term premium a 10 años cayó entre 50 y 100 pb (entre 30 y 100 pb según el método), sobre todo por menor prima y no por expectativas. En series de tiempo, **+1% del PIB de oferta de deuda larga eleva el term premium ~4.4 pb** (6.4 pb en equivalentes a 10 años). Krishnamurthy-Vissing-Jorgensen (2011): QE opera por señalización, demanda de activos seguros e inflación, y el efecto depende de qué se compra (MBS en QE1, solo Treasuries en QE2). La base teórica son Greenwood-Vayanos (2014) y Vayanos-Vila (2021): la oferta de duración mueve el term premium.
- **QT:** terminó el **1-dic-2025** (comunicado del 29-oct-2025), y el 10-dic-2025 empezaron compras de Treasuries cortos para mantener reservas amplias. No se verificó un consenso sobre su efecto. *Inferencia:* menor y asimétrico frente a QE (grado C).

### 2.9 Correlación acciones-bonos

- **Campbell-Pflueger-Viceira (2020, JPE):** la correlación entre inflación y brecha del producto pasó de negativa a positiva en 2001T2. Con eso, la correlación trimestral bonos-acciones pasó de **+0.21 (1979T3-2001T1) a −0.64 (2001T2-2011T4)** y la beta de los bonos frente a las acciones de +0.11 a −0.19 (datos). El modelo de hábitos lo replica (+0.50 → −0.66) solo si las primas de riesgo son endógenas. El mecanismo: si la inflación es contracíclica (choques de oferta), bonos y acciones caen juntos; si es procíclica (choques de demanda y una Fed creíble), los bonos cubren.
- **Réplica propia (1962-2026):** correlación diaria entre el rendimiento del S&P 500 y −Δy del 10 años (aproximación del rendimiento del bono):

| Periodo | Correlación |
|---|---|
| 1970-1999 | +0.28 |
| 2000-2020 | −0.38 |
| 2022-2023 | +0.14 |
| 2024-sep 2026 | +0.05 |
| 2026 a la fecha | **+0.44** |

Con datos mensuales SPY-IEF: −0.30 en 2004-2021 y +0.56 en 2022-ago 2026. *Inferencia:* en 2026 los bonos no cubren a las acciones; es un régimen de choque de oferta, como el de 1970-1999.
- **Brixton et al. (2023):** acciones y bonos reaccionan con signo opuesto a las noticias de crecimiento y con el mismo signo a las de inflación; manda la volatilidad relativa de ambas (§4).

### 2.10 Regímenes macro (crecimiento × inflación)

Hay cuatro cuadrantes (Ilmanen-Maloney-Ross 2014):
- Crecimiento ↑ e inflación ↓: ganan las acciones y los bonos ayudan.
- Crecimiento ↓ e inflación ↓: ganan los bonos largos.
- Crecimiento ↑ e inflación ↑: ganan las materias primas y los bonos pierden.
- Crecimiento ↓ e inflación ↑ (estanflación): pierden los activos tradicionales.

Neville et al. (2021), con 95 años de datos de EUA, Reino Unido y Japón, encuentran que la inflación inesperada daña a bonos y acciones, que las materias primas ganan con alta dispersión y que el **trend-following fue la protección más confiable**.

### 2.11 Indicadores adelantados

- **Curva 10a−3m:** es el mejor predictor individual de recesión a más de un trimestre fuera de muestra (Estrella-Mishkin 1998), con AUC de 0.85-0.89 (Bauer-Mertens, FRBSF EL 2018-20). El **near-term forward spread** de Engstrom-Sharpe (forward a 6 trimestres del 3m menos el 3m spot) lo distorsiona menos el term premium.
- **Regla de Sahm** (FRED SAHMREALTIME): llegó a 0.53 en jul-2024 y a 0.57 en ago-2024 sin que hubiera recesión, y hoy está en −0.07 (ago-2026). **Solicitudes iniciales de desempleo:** 197 mil (semana al 19-sep-2026).
- **LEI de The Conference Board:** la regla de las 3D pide que la tasa semestral anualizada caiga por debajo de −4.3% y que el índice de difusión sea ≤ 50. En ago-2026 el LEI estaba en 99.5, con −0.1% en el mes y −0.1% en 6 meses, y **sin señal**.
- **ISM manufacturero:** el umbral es 50 (cifras recientes no verificadas).

### 2.12 Sostenibilidad fiscal y oferta de Treasuries

- **Datos (FRED/OMB):** el déficit federal fue de 6.07% del PIB en el año fiscal 2023, 6.20% en 2024 y 5.77% en 2025. El gasto en intereses fue de 2.37%, 3.00% y 3.15% del PIB. La deuda en manos del público es de 98.7% del PIB (2026T1). El déficit de 12 meses a ago-2026 es de US$1.77 billones (≈5.4% del PIB, cálculo propio).
- **Moody's** bajó a EUA de Aaa a Aa1 el 16-may-2025, con lo que las tres calificadoras quedaron por debajo de AAA.
- **Refinanciamiento del Tesoro (5-ago-2026):** US$125 mil millones, con los tamaños de cupón fijos "al menos por los próximos trimestres". Endeudamiento de US$739 mil millones en jul-sep-2026 (+US$68 mil millones contra lo estimado en mayo) y US$628 mil millones en oct-dic. El TBAC ve que las proyecciones "podrían justificar aumentos de cupones en el año fiscal 2027". Próximo anuncio: 4-nov-2026.
- **Covitz-Engstrom (FEDS Note, 12-feb-2026):** el forward de 9 a 10 años subió ~200 pb en cinco años, el mayor aumento desde finales de los setenta, todo por **prima de riesgo real**. Las expectativas de inflación (~2%) y la prima inflacionaria (~0) no cambiaron. Lo atribuyen al riesgo de choques de oferta y a la preocupación fiscal (la CBO proyecta la deuda hacia ~120% del PIB en una década).
- *Inferencia:* con Gagnon et al. (+4.4 pb de term premium por cada 1% del PIB de oferta larga), un aumento acumulado de 5% del PIB en deuda larga equivale a ~20-30 pb de term premium. Es relevante, pero menor que el efecto de la trayectoria de la Fed en 2026.

### 2.13 Aplicación conceptual a México (datos vigentes en el módulo 11)

- **Benchmark del sistema:** 50% S&P 500 TR en MXN + 50% **CETES 28**. La parte de renta fija tiene una duración de ≈0.08 años (28 días), así que **toda duración adicional es una apuesta activa**.
- **CETES:** su riesgo es de reinversión (Banxico recorta y el rendimiento cae al renovar). **Bonos M:** la duración es la apuesta al ciclo de Banxico y al term premium local, y el carry, el roll-down y el colchón se calculan como en §2.5. **UDIBONOS:** ganan contra los Bonos M si la inflación realizada supera el breakeven MX; a plazos cortos dominan la duración real y la liquidez. **Bondes F:** casi sin riesgo de tasa, pero con riesgo de spread.
- *Inferencia:* para un inversionista en MXN, los Bonos M son "risk-on" en una crisis global (el peso se deprecia y las tasas locales suben con la salida de flujos), así que no replican la cobertura que dieron los Treasuries en USD en 2000-2020. Los Treasuries comprados desde México traen la beta de USD/MXN: el 60/40 de EUA rindió −16.1% en USD y **−20.2% en MXN** en 2022, y +15.5% en USD y **+40.5% en MXN** en 2024 (cálculo propio).

---

## 3. Literatura canónica

| Autores | Año | Título | Revista/Editorial | Hallazgo clave cuantificado | Enlace/DOI | Grado |
|---|---|---|---|---|---|---|
| Macaulay | 1938 | Some Theoretical Problems Suggested by the Movements of Interest Rates, Bond Yields and Stock Prices in the US since 1856 | NBER | Definición de duración | 10.4324/9781315145976-2 (reimpr.) | A (identidad) |
| Merton | 1974 | On the Pricing of Corporate Debt: The Risk Structure of Interest Rates | JF 29(2):449-470 | Deuda = libre de riesgo − put. El spread depende del apalancamiento y la volatilidad | 10.1111/j.1540-6261.1974.tb03058.x | A (teoría); C para explicar el nivel de spreads IG |
| Harvey | 1986 | Recovering Expectations of Consumption Growth from an Equilibrium Model of the Term Structure of Interest Rates | Tesis, U. Chicago | La pendiente real anticipa el consumo | people.duke.edu/~charvey | B |
| Harvey | 1988 | The Real Term Structure and Consumption Growth | JFE 22(2):305-333 | La curva real predice el crecimiento del consumo | 10.1016/0304-405X(88)90073-6 | B |
| Fama, Bliss | 1987 | The Information in Long-Maturity Forward Rates | AER 77(4):680-692 | El spread forward predice rendimientos en exceso a 1 año (rechaza expectativas puras) | ideas.repec.org/a/aea/aecrev/v77y1987i4p680-92.html | B |
| Estrella, Hardouvelis | 1991 | The Term Structure as a Predictor of Real Economic Activity | JF 46(2):555-576 | Pendiente positiva → más consumo e inversión. Poder adicional sobre el LEI, también fuera de muestra | 10.1111/j.1540-6261.1991.tb02674.x | B |
| Campbell, Shiller | 1991 | Yield Spreads and Interest Rate Movements: A Bird's Eye View | REStud 58(3):495 | Los largos no suben como predice la curva, lo que confirma un term premium variable | 10.2307/2298008 | A (hecho) |
| Litterman, Scheinkman | 1991 | Common Factors Affecting Bond Returns | JFI 1(1):54-61 | 3 factores ≈ toda la varianza. Réplica propia: 98.4% | 10.3905/jfi.1991.692347 | A |
| Taylor | 1993 | Discretion versus Policy Rules in Practice | Carnegie-Rochester 39:195-214 | i = r* + π + 0.5(π−2) + 0.5·brecha, con r* = 2 | 10.1016/0167-2231(93)90009-L | B (descriptiva) |
| Estrella, Mishkin | 1996 | The Yield Curve as a Predictor of U.S. Recessions | NY Fed Current Issues 2(7) | 10a−3m supera a otros indicadores a 2-6 trimestres | newyorkfed.org/research/current_issues/ci2-7.html | B |
| Estrella, Mishkin | 1998 | Predicting U.S. Recessions: Financial Variables as Leading Indicators | REStat 80(1):45-61 | Fuera de muestra, más allá de 1 trimestre, la pendiente es el mejor predictor individual | nber.org/papers/w5379 | B |
| Elton, Gruber, Agrawal, Mann | 2001 | Explaining the Rate Spread on Corporate Bonds | JF 56(1):247-277 | El default esperado explica una fracción pequeña del spread; impuestos y prima de riesgo, el resto | 10.1111/0022-1082.00324 | B |
| Collin-Dufresne, Goldstein, Martin | 2001 | The Determinants of Credit Spread Changes | JF 56(6):2177-2207 | Las variables teóricas explican poco. Los residuos siguen un factor común no identificado | 10.1111/0022-1082.00402 | A (hecho) |
| Laubach, Williams | 2003 | Measuring the Natural Rate of Interest | REStat 85(4):1063-1070 | r* con filtro de Kalman. Hoy 1.65% (2026T2) | 10.1162/003465303772815934 | C (incertidumbre enorme) |
| Cochrane, Piazzesi | 2005 | Bond Risk Premia | AER 95(1):138-160 | Un factor en forma de tienda de forwards predice los excesos. Cuestionado por Bauer-Hamilton | 10.1257/0002828053828581 | C (fuera de muestra) |
| Longstaff, Mithal, Neis | 2005 | Corporate Yield Spreads: Default Risk or Liquidity? | JF 60(5):2213-2253 | Con CDS: la mayor parte del spread es default, y lo no-default es liquidez | 10.1111/j.1540-6261.2005.00797.x | B |
| Kim, Wright | 2005 | An Arbitrage-Free Three-Factor Term Structure Model… | FEDS 2005-33 | Term premium con encuestas. Hoy 0.97%, máximo desde 2011 | federalreserve.gov (ver §9) | B (modelo) |
| Giesecke, Longstaff, Schaefer, Strebulaev | 2011 | Corporate Bond Default Risk: A 150-Year Perspective | JFE 102(2):233-250 | Spread ≈ 2× pérdidas. Prima de crédito ≈ 80 pb (1866-2008) | 10.1016/j.jfineco.2011.01.011 | A |
| Gagnon, Raskin, Remache, Sack | 2011 | The Financial Market Effects of the Fed's LSAPs | IJCB (SR 441, 2010) | LSAP1: −91 pb en el 10 años. Term premium −30 a −100 pb. +1% del PIB de oferta = +4.4 pb | newyorkfed.org SR 441 | B |
| Krishnamurthy, Vissing-Jorgensen | 2011 | The Effects of QE on Interest Rates | BPEA 2011(2):215-287 | Canales de señal, escasez de activos seguros e inflación. Importa qué se compra | 10.1353/eca.2011.0019 | B |
| Gilchrist, Zakrajšek | 2012 | Credit Spreads and Business Cycle Fluctuations | AER 102(4):1692-1720 | El excess bond premium predice actividad y precios | 10.1257/aer.102.4.1692 | B |
| Huang, Huang | 2012 | How Much of the Corporate-Treasury Yield Spread Is Due to Credit Risk? | RAPS 2(2):153-202 | En IG, el crédito explica una fracción pequeña (credit spread puzzle) | 10.1093/rapstu/ras011 | B |
| Adrian, Crump, Moench | 2013 | Pricing the Term Structure with Linear Regressions | JFE 110(1):110-138 | Term premium con 5 componentes principales. Hoy 0.65% | 10.1016/j.jfineco.2013.04.009 | B (modelo) |
| Fleckenstein, Longstaff, Lustig | 2014 | The TIPS-Treasury Bond Puzzle | JF 69(5):2151-2197 | Mispricing de más de US$20 por 100. Más de US$56 mil millones (~8% de los TIPS) | 10.1111/jofi.12032 | A (hecho) |
| Greenwood, Vayanos | 2014 | Bond Supply and Excess Bond Returns | RFS 27(3):663-713 | La oferta de duración predice el term premium | 10.1093/rfs/hht133 | B |
| Holston, Laubach, Williams | 2017 | Measuring the Natural Rate of Interest: International Trends | JIE 108:S59-S75 | r* bajo en EUA, Canadá y la zona euro | 10.1016/j.jinteco.2017.01.004 | C |
| Koijen, Moskowitz, Pedersen, Vrugt | 2018 | Carry | JFE 127(2):197-225 | Carry con Sharpe promedio de **0.8** y diversificado de **1.2** (corregido 2026-09-25; ver adenda). En bonos globales ≈ pasivo | 10.1016/j.jfineco.2017.11.002 | B |
| Bauer, Hamilton | 2018 | Robust Bond Risk Premia | RFS 31(2):399-448 | Con pruebas robustas, la evidencia más allá de nivel, pendiente y curvatura "es mucho más débil" | 10.1093/rfs/hhx096 | A (crítica) |
| Gargano, Pettenuzzo, Timmermann | 2019 | Bond Return Predictability: Economic Value… | Mgmt Sci 65(2):508-540 | Solo con volatilidad dinámica y factor macro hay ganancia económica fuera de muestra | 10.1287/mnsc.2017.2829 | C |
| Campbell, Pflueger, Viceira | 2020 | Macroeconomic Drivers of Bond and Equity Risks | JPE 128(8):3148-3185 | Correlación bonos-acciones: +0.21 → −0.64 con quiebre en 2001T2 | 10.1086/707766 | A (hecho) / B (mecanismo) |

---

## 4. Lo más reciente 2023-2026

1. **Covitz y Engstrom (FEDS Note, 12-feb-2026):** +200 pb en el forward de 9 a 10 años, todo por prima real (§2.12). *Inferencia:* el "piso" del rendimiento largo es hoy más alto.
2. **Dickerson, Robotti y Rossetti (arXiv 2604.07880, 9-abr-2026), "The Corporate Bond Factor Replication Crisis":** de 108 señales y 432 especificaciones, solo **26 (6.0%)** alfas del CAPM de bonos sobreviven a la corrección FDR (Benjamini-Hochberg), sobre todo value basado en spreads. La reversión de corto plazo baja de −0.99% a −0.09% al mes al corregir el error de medición. En un año típico **70% de los bonos cotiza 10 días o menos**.
3. **Dickerson, Mueller y Robotti (2023, JFE 150(2)):** la mayoría de los factores propuestos no agrega poder de valuación más allá del factor de mercado de bonos, con la liquidez como excepción marginal. **Dick-Nielsen, Feldhütter, Pedersen y Stolborg (2023, SSRN 4586652):** documentan fallas de replicación en los factores de bonos corporativos. Solo una minoría es robusta, sobre todo dentro de la misma empresa, y proponen un modelo de 4 factores.
4. **Pflueger (2025, JFE 167, 104027; NBER w30921 de 2023):** el riesgo de los bonos nominales es un indicador adelantado del riesgo de estanflación. La correlación positiva de los años ochenta surgió de choques de oferta combinados con una política monetaria reactiva, no de uno solo de los dos.
5. **Rogoff, Rossi y Schmelzing (2024, AER 114(8)):** con 700 años de datos, las tasas reales largas son estacionarias en tendencia y **bajan desde el Renacimiento**, sin que la demografía ni la productividad sean impulsores convincentes. Choca con la tasa real de 2.76% de 2026, la más alta desde 2008.
6. **Holston, Laubach y Williams (2023, NY Fed SR 1063):** a fines de 2022 el r* seguía cerca de su nivel prepandemia y no hay evidencia de que haya terminado la era de r* bajo (actualización de ago-2026: 1.01%).
7. **Brixton, Brooks, Hecht, Ilmanen, Maloney y McQuinn (2023, JPM 49(4)):** su modelo de volatilidad relativa de crecimiento e inflación explica ~70% de la variación de largo plazo de la correlación acciones-bonos. Si sube la incertidumbre inflacionaria, recomiendan diversificadores alternativos (líquidos dinámicos, materias primas).
8. **Acharya y Laarits (NBER w31863, 2023):** el convenience yield de los Treasuries cae cuando la covarianza acciones-bonos es alta, con más expectativas de inflación, antes de disputas del techo de deuda y con más oferta. *Inferencia:* es el canal por el que la oferta y la inflación de 2025-26 encarecen la deuda de EUA.
9. **Duffee (2022/2023, Review of Finance 27(5)):** con revisiones de encuestas como noticias, ni las teorías centradas en la inflación ni las centradas en tasas reales explican la comovimiento acciones-bonos. El hecho es robusto; la causa sigue en disputa. En la misma línea está Molenaar, Senechal, Swinkels y Wang (2024, FAJ 80(3)); sus hallazgos específicos **no se verificaron** en esta sesión.
10. **Datos de política 2025-2026 (fuente primaria, detalle en §2.8 y §2.12):** Moody's retiró la Aaa, la Fed terminó QT y en 2026 subió la tasa, y el TBAC anticipa más cupones. El 10 años llegó a 5.11% (máximo desde jul-2007) y el 30 años a 5.40% (máximo desde jul-2004).
11. **Lacava y Otranto (arXiv 2601.21447, ene-2026):** la incertidumbre de política comercial altera la correlación dinámica acciones-bonos (DCC). En abril de 2025 el 10 años pasó de 4.01% (4-abr) a 4.48% (11-abr) mientras caía la bolsa.

---

## 5. Evidencia real: qué funciona, qué no, magnitudes netas y decaimiento

### 5.1 Curva invertida → recesión (grado B, con un falso positivo mayor reciente)

Cálculo propio: episodios en que el promedio mensual de T10Y3M fue menor que cero (FRED, desde 1982) contra el inicio de recesión según NBER/USREC.

| Inversión (prom. mensual) | Mínimo | Inicio de la recesión | Anticipación |
|---|---|---|---|
| jun-ago y nov-dic 1989 | −0.16 | ago-1990 | ~14 m |
| jul-2000 a ene-2001 | −0.70 | abr-2001 | ~9 m |
| ago-2006 a may-2007 | −0.52 | ene-2008 | ~17 m |
| may-sep 2019 | −0.36 | mar-2020 (COVID, exógena) | ~10 m |
| **nov-2022 a nov-2024** | **−1.73** | **ninguna a ago-2026** | falso positivo |
| mar-abr y jun-ago 2025 | −0.06 | ninguna | ruido |

- 2022-2024 fue la inversión más larga del registro: **534 sesiones seguidas** (25-oct-2022 a 12-dic-2024), con un mínimo de −1.89 el 4-may-2023. El 10a−2a estuvo invertido de abr-2022 a sep-2024. La serie GS10−TB3MS desde 1953 muestra otro falso positivo en 1966-67.
- **Recuento:** 4 de 4 recesiones en 1989-2020, con 9-17 meses de anticipación, y 2 falsos positivos desde 1966. Con tan pocos eventos, los intervalos de confianza son enormes.
- **Caso 2022-2024 (Inferencia):** el term premium negativo (ACM promedió −0.46% en 2023) invirtió la curva sin que el mercado esperara recortes, que es la distorsión que corrige el spread de Engstrom-Sharpe. Además, los déficits de 6.1-6.2% del PIB sostuvieron la demanda y la deuda a tasa fija frenó la transmisión. La regla de Sahm también dio una falsa alarma (0.57 en ago-2024).
- **Uso correcto:** es una probabilidad condicional, no una fecha. Se combina con indicadores laborales y de crédito y se registra con Brier.

### 5.2 Predecir rendimientos de bonos (grado C)

- Dentro de muestra, el spread de forwards (Fama-Bliss), el factor de Cochrane-Piazzesi y los factores macro (Ludvigson-Ng) predicen los excesos.
- Bauer-Hamilton (2018) revisan seis estudios publicados: con pruebas robustas a sesgos de muestra pequeña, la evidencia contra la hipótesis de que la curva basta ("spanning") es "mucho más débil".
- Gargano-Pettenuzzo-Timmermann (2019): la ganancia económica fuera de muestra aparece solo con volatilidad dinámica y factores macro no contenidos en la curva.
- **Conclusión:** no se opera una predicción de rendimientos de bonos basada solo en la curva.

### 5.3 Carry y tendencia en bonos (grado B, bruto)

> **Adenda 2026-09-25 (examen diagnóstico S3-08, ficha `conocimiento/fichas/2026-09-25-examen-S1-S5-huecos.md`).** El resultado *principal* del artículo publicado (JFE 127(2):197-225), verificado con `pypdf` sobre el PDF, es: "a carry trade that goes long high-carry assets and shorts low-carry assets earns significant returns in each asset class with an annualized Sharpe ratio of **0.8 on average**. Further, a diversified portfolio of carry strategies across all asset classes earns a Sharpe ratio of **1.2**." La cifra de 0.74/1.1 que tenía antes esta tabla corresponde al borrador NBER de 2013 o se confunde con la variante que reduce rotación ("carry1-12", que sí da Sharpe 1.1 según el propio artículo). Se corrigió la tabla de fuentes arriba.

- **Koijen et al. (2018),** bruto de costos y dentro de muestra: Sharpe del carry1-12 de 0.46 en bonos globales a 10 años, 0.40 en pendiente 10a−2a, 0.78 en Treasuries por plazo y 0.46 en crédito. En nivel y pendiente de bonos globales no supera al pasivo, y la señal tiene correlación de 0.90 con el spread 10a−3m: en la práctica es "comprar pendiente".
- **Tendencia (réplica propia):** mantener el ETF si está sobre su promedio de 12 meses y efectivo si no, con 10 pb por cambio, sep-2003 a ago-2026 (42 cambios en IEF).

| Instrumento | Estrategia | Sharpe | Max drawdown | 2022 |
|---|---|---|---|---|
| IEF | Comprar y mantener | 0.32 | −23.2% | −15.2% |
| IEF | Tendencia 12 m | 0.31 | **−8.7%** | **+1.3%** |
| TLT | Comprar y mantener | 0.20 | −47.6% | −31.2% |
| TLT | Tendencia 12 m | 0.14 | −22.7% | −2.7% |

  **Veredicto:** la tendencia no agrega Sharpe, pero reduce el drawdown ~60%: es control de riesgo, no alfa. El parámetro es estándar y no se optimizó, pero la muestra tiene un solo gran mercado bajista de bonos.

### 5.4 Crédito: IG vs HY (grado B para la prima; C/D para los factores)

Cálculo propio, jul-2007 a ago-2026, mensual, en exceso de BIL:

| ETF | CAGR | Volatilidad | Sharpe | Max drawdown |
|---|---|---|---|---|
| SPY | 11.11% | 15.5% | 0.67 | −50.8% |
| HYG | 5.32% | 10.2% | 0.43 | −30.2% |
| LQD | 4.15% | 8.3% | 0.37 | −23.3% |
| AGG | 2.99% | 4.6% | 0.37 | −17.1% |
| TIP | 3.34% | 5.8% | 0.36 | −13.9% |
| IEF | 3.16% | 6.7% | 0.30 | −23.2% |
| TLT | 2.82% | 14.1% | 0.17 | −47.6% |

- **Regresión HYG = α + β₁·SPY + β₂·IEF (excesos):** α = **−1.13%/año (t = −0.71)**, β_SPY = 0.49, β_IEF = 0.20, R² = 0.56. **LQD:** α = −1.36%/año (t = −1.19), β_SPY = 0.26, β_IEF = 0.84.
- Correlaciones: HYG-SPY 0.73 y HYG-IEF 0.08. En 2008: HYG −17.6%, LQD +2.4%, IEF +17.9%.
- **Veredicto:** el crédito en ETF no aporta nada que no dé una mezcla de acciones y Treasuries; neto de comisiones, el alfa es negativo (no significativo). La prima de crédito existe en el largo plazo (~80 pb, Giesecke et al.), pero los factores dentro de bonos corporativos no sobreviven a datos limpios (§4).

### 5.5 El 60/40 y 2022 (hecho, grado A de datos)

- 60/40 SPY/AGG con rebalanceo anual en 2022: **−16.1%** (SPY −18.2%, AGG −13.0%). En la muestra 2004-2025 solo 2008 fue peor (−18.9%), y 2022 es el único año con ambos componentes abajo más de 10%. **En MXN: −20.2%.**
- **TLT** cayó 47.6% (jul-2020 a oct-2023) y en sep-2026 seguía 43.7% abajo de su máximo. **TMF (3× bonos largos)** perdió 72.6% en 2022 y **92.9%** desde jul-2020.
- 2023-2025 (en USD): +18.0%, +15.5% y +13.5%.
- **Lección:** la diversificación del 60/40 depende del régimen de correlación (§2.9), no de una ley.

### 5.6 QE y política monetaria (grado B)

El QE bajó el term premium entre 30 y 100 pb en 2008-09. El efecto de la oferta es pequeño por unidad (4.4 pb por cada 1% del PIB), pero acumulable. La regla de Taylor describe a la Fed en promedio, pero no sirve como señal de trading. En dic-2021, aun con brecha cero, daba 1.73 + 5.21 + 1.61 ≈ 8.5% contra una tasa de 0-0.25% (r* HLW y PCE subyacente), y en 2026 la Fed volvió a quedar debajo.

### 5.7 Regímenes inflacionarios (grado B)

Ver §2.10 (Neville et al. 2021). 2022 lo confirmó en bonos: la regla de tendencia de §5.3 estuvo en efectivo y ganó 1.3% contra −15.2%.

---

## 6. Traducción operable (cómo lo usa el sistema para ganar)

Todas las cifras de riesgo vienen de `config/parametros.json`. En **fase 0** (`prioridad_actual`) estas reglas se aplican solo al portafolio de papel. Los umbrales marcados como "por validar" son parámetros del sistema, no hallazgos de un paper, y deben pasar `validacion_estrategias` (≥10 años, costos, DSR ≥ 0.95, PBO ≤ 0.25).

### 6.1 Reglas

1. **Duración neutral = cero** (el benchmark usa CETES 28). Todo Bono M, UDIBONO o Treasury largo es una apuesta activa y va en el **satélite** (≤ `estructura.satelite_max` = 30% en el perfil estándar).
2. **Presupuesto de duración por riesgo:**
   - Pérdida por un movimiento de 2σ mensual ≈ D_port × 0.5 pp. En EUA, la σ mensual del 10 años es de 0.22-0.27 pp (cálculo propio); para los Bonos M se calibra en el módulo 11.
   - Esa pérdida debe ser ≤ `riesgo_por_operacion`. Límite: **D_port ≤ 2.0 años en el perfil estándar** (1%) y **≤ 6.0 años en `arena_agresivo`** (3%).
   - Ejemplo: con un bono de D_mod ≈ 15 (TLT es de este tipo), el peso máximo es ≈13% en el estándar y ≈40% en la arena, sujeto también al `etf_indice_max` de la arena (60%).
3. **Semáforo para agregar duración** (por validar; se requieren ≥ 3 de 4):
   - (a) carry + roll-down > 0 frente al instrumento de fondeo (CETES 28 o T-bill);
   - (b) tendencia: el precio del ETF o índice del bono está sobre su promedio de 12 meses (§5.3);
   - (c) correlación diaria de 12 meses entre las acciones y el bono < 0 (el bono sí cubre);
   - (d) inflación subyacente ≤ 3% y bajando 3 meses seguidos.
   - **Estado al 25-sep-2026 en EUA:** (a) sí (+1.08%/año); (b) no (IEF, TLT, AGG y TIP bajo su promedio de 12 meses); (c) no (+0.44); (d) no (3.34%). **Resultado: 1 de 4. No se agrega duración en USD;** la renta fija se queda en T-bills/CETES.
4. **ETFs de bonos apalancados (TMF y similares) en la arena:** además del `filtro_apalancados` (subyacente sobre su media de 200 días y VIX < 25), se exigen **4 de 4** en el semáforo de la regla 3. Se venden al perder cualquiera de las cuatro condiciones. El peso máximo es `etf_apalancado_max` = 50%, con el tope de la regla 2 aplicado a la duración efectiva (3× la del subyacente). Historial: −92.9% desde jul-2020.
5. **Crédito:**
   - No se usan ETFs de HY ni de IG en el núcleo, porque replican 0.49 SPY + 0.20 IEF con alfa negativo (§5.4).
   - Un emisor privado individual (por ejemplo, un corporativo mexicano) no puede pasar de `emisor_deuda_privada_max` = 5%.
   - Una tesis de crédito requiere un spread por encima de su mediana de 10 años y la tendencia de spreads a la baja. Hoy el OAS de HY es de 2.73%: se compra poco colchón.
6. **Tablero de recesión (mensual; cada señal vale 1 punto):**
   - (1) T10Y3M con promedio mensual < 0 por ≥ 3 meses;
   - (2) SAHMREALTIME ≥ 0.5;
   - (3) regla de las 3D del LEI activa;
   - (4) solicitudes iniciales con promedio de 4 semanas ≥ 20% sobre su mínimo de 52 semanas (por validar);
   - (5) OAS de HY +150 pb en 6 meses (por validar).
   - **Con ≥ 3 puntos:** la beta accionaria del satélite baja 50% (igual que `rachas.factor_reduccion`) y el efectivo se va a CETES. **Con ≤ 1:** no hay acción. **Estado hoy: 0 de 5** (10a−3m en +0.94; solicitudes con promedio de 4 semanas de 202 mil, 2% sobre su mínimo; OAS de HY −46 pb en 6 meses).
   - Este tablero no reemplaza los `cortacircuitos_drawdown`; opera antes que ellos.
7. **Inflación:** UDIBONOS y TIPS se usan como ancla real solo si el horizonte es ≥ a su duración. Contra choques inflacionarios la evidencia favorece la tendencia y las materias primas (Neville et al.). Se prefiere el UDIBONO al Bono M si el breakeven MX es menor que las expectativas de encuestas + 0.5 pp (por validar; calibración en el módulo 11).
8. **Todo se mide en MXN** (`moneda_base`). Un Treasury es una posición en tasa de EUA × USD/MXN. En 2024 el tipo de cambio agregó 25 pp al 60/40. El riesgo cambiario se reporta aparte de la duración.
9. **Calendario de eventos:** FOMC (27-28 oct y 8-9 dic de 2026), refinanciamiento del Tesoro (2 y 4 de nov de 2026), IPC y PCE de EUA, y Banxico. No se abren posiciones de duración en las 24 h previas. Es higiene operativa, no una ventaja demostrada.
10. **Pronósticos registrados** (según `pronosticos`): cada mes, P(recesión NBER en 12 m), un intervalo del 80% para el 10 años de EUA y el Bono M a 10 años a 3 meses, y la decisión de la Fed y de Banxico. Se evalúa con Brier ≤ 0.2 después de ≥ 50 pronósticos. No hay escala a fase 2 sin esa calibración.
11. **Arena:** una operación de duración cuenta dentro de `operaciones_max_mes` = 8 y respeta `limites_perdida` (5% diario, 10% semanal y 18% mensual). En modo torneo, si el sistema va adelante del mejor rival por ≥ 5 pp, la duración se reduce primero, porque es la fuente de varianza con correlación incierta.

### 6.2 Checklist antes de cualquier posición de renta fija

- [ ] ¿Qué factor compro: nivel, pendiente, crédito, inflación o USD/MXN? Escribirlo.
- [ ] DV01 en MXN de la posición y del portafolio. D_port dentro de la regla 2.
- [ ] Carry + roll-down y colchón Δy* en pb, comparado con la σ del horizonte.
- [ ] Semáforo de la regla 3, con su fecha y fuente.
- [ ] Qué pasa en el peor escenario de correlación (acciones y bonos −10% juntos, como en 2022), y si se respetan `limites_perdida` y `drawdown_objetivo`.
- [ ] Liquidez: spread de compra-venta del instrumento en GBM, y si es fondo, su TER.
- [ ] Salida escrita: nivel de tasa o pérdida máxima, y fecha de revisión.

---

## 7. Trampas y errores comunes

1. **Olvidar la convexidad en movimientos grandes.** La duración sola exagera la pérdida en 1.4 pp (10 años, +200 pb) y en 1.6 pp (30 años, +100 pb).
2. **Creer que los bonos siempre cubren a las acciones.** Solo cubren con inflación procíclica y una Fed creíble. La correlación fue de +0.28 en 1970-1999 y es de +0.44 en 2026.
3. **Leer la curva invertida como fecha de recesión.** En 2022-2024 hubo 534 sesiones invertidas y ninguna recesión (a ago-2026).
4. **Tratar las salidas de modelos como datos.** El term premium de ACM y el de Kim-Wright difieren ~30 pb. El r* de HLW (1.0%), el de LW (1.65%) y el del SEP (≈1.2%) difieren ~0.6 pp y se revisan cada trimestre.
5. **Tomar el breakeven como expectativa pura.** Lo contaminan la liquidez de los TIPS y la prima inflacionaria.
6. **Comprar HY "por el rendimiento".** Equivale a 0.49 de beta accionaria, con −30% de drawdown y −1.1%/año de alfa.
7. **Extrapolar factores publicados de bonos corporativos.** El 94% de las especificaciones no sobrevive a datos corregidos.
8. **Comprar ETFs de bonos apalancados por "reversión a la media".** TMF perdió 92.9% desde 2020 y TBT perdió 94.6% en 2008-2020.
9. **Olvidar el tipo de cambio.** USD/MXN se movió ±13-22% por año en 2023-2025, más que cualquier Treasury.
10. **Suponer que el carry protege.** El colchón actual del 10 años es de ~14 pb por año (~0.2σ).
11. **Suponer que UDIBONOS y TIPS protegen en el corto plazo.** TIP cayó 12.3% en 2022 porque dominó la duración real.
12. **Ignorar la oferta y lo fiscal.** Déficits de 5.4-6.2% del PIB y la posibilidad de más cupones en el año fiscal 2027 presionan el term premium, aunque poco por unidad (4.4 pb por cada 1% del PIB).
13. **Backtests de bonos que empiezan en 1982 o 2003.** Capturan la caída secular del 10 años de 15.84% (30-sep-1981) a 0.52% (4-ago-2020).

---

## 8. Examen de titulación

1. **Bono a 10 años con cupón de 5% y rendimiento de 5.11% (D_mod = 7.78, C = 73.4): ¿cuánto cambia con +100 pb?** −7.78% + ½·73.4·0.0001 = −7.41% (el exacto es −7.43%).
2. **¿Cuál es el DV01 de US$1 millón de ese bono?** 7.78 × 99.147 × 0.0001 = 0.0771 por 100, es decir ≈ US$771 por pb.
3. **¿Cuánto explican nivel, pendiente y curvatura?** ~98% de los cambios de la curva. En 1993-2026 (cálculo propio): 86.1%, 10.0% y 2.3%.
4. **Descompón el 10 años del 23-sep-2026 con ACM.** 5.07% = 4.43% de tasa esperada + 0.65% de term premium. Kim-Wright da 0.97%, máximo desde 2011.
5. **Calcula carry, roll-down y colchón con el 3m en 4.19% y una pendiente de 7 a 10 años de 2 pb/año.** 0.92% + 0.16% = 1.08%, así que Δy* ≈ 1.08/7.78 ≈ 14 pb en 12 meses.
6. **¿Qué historial tiene la curva 10a−3m?** Anticipó las recesiones de 1990, 2001, 2008 y 2020 con 9-17 meses de anticipación. En 2022-2024 estuvo invertida 25 meses sin recesión. Es una probabilidad, no una fecha.
7. **¿Qué es la deuda en Merton y qué es el credit spread puzzle?** Deuda = libre de riesgo − put. El puzzle: las pérdidas esperadas explican poco del spread IG. Históricamente, spread ≈ 2× pérdidas, con una prima de ~80 pb.
8. **¿Por qué el breakeven no es la inflación esperada?** Porque es E[π] + prima de inflación − prima de liquidez de los TIPS. El mispricing llegó a más de US$20 por cada 100 (FLL 2014).
9. **Calcula Taylor con r* = 1.01, un PCE subyacente de 3.34% y una brecha de −0.11.** 1.01 + 3.34 + 0.67 − 0.055 ≈ 4.97%, contra 3.75-4.00% de la Fed: está por debajo de la regla.
10. **¿Por qué cambia de signo la correlación acciones-bonos?** Porque cambia la covarianza entre inflación y brecha. En 2001T2 pasó de negativa a positiva y la correlación bonos-acciones fue de +0.21 a −0.64 (CPV 2020). Con choques de oferta vuelve a ser positiva.
11. **¿Cuánto movió el QE1 el term premium y cuánto lo mueve la oferta?** QE1: −30 a −100 pb (−91 pb en el 10 años). Oferta: +4.4 pb por cada 1% del PIB de deuda larga.
12. **¿Un ETF de HY en el núcleo?** No: equivale a 0.49 SPY + 0.20 IEF con α = −1.13%/año (t = −0.71).
13. **¿Cuánto rindió el 60/40 en 2022?** −16.1% en USD y −20.2% en MXN: acciones y bonos cayeron juntos por la inflación y las alzas de la Fed, y el peso se apreció.
14. **¿Cuánta duración permite el sistema y cuánta agrega hoy?** Hasta 2 años (estándar) o 6 (arena). Hoy no agrega en USD, porque el semáforo marca 1 de 4.
15. **¿Qué duración tiene el benchmark y qué implica?** ≈0 (CETES 28), así que todo Bono M o Treasury largo es una apuesta activa contra CETES en MXN.

---

## 9. Fuentes

1. Litterman, Scheinkman (1991), JFI — https://doi.org/10.3905/jfi.1991.692347
2. Macaulay (1938), capítulo reimpreso — https://doi.org/10.4324/9781315145976-2
3. Merton (1974), JF — https://doi.org/10.1111/j.1540-6261.1974.tb03058.x
4. Harvey (1986), tesis — https://people.duke.edu/~charvey/Research/Thesis/Thesis.htm
5. Harvey (1988), JFE — https://doi.org/10.1016/0304-405X(88)90073-6
6. Fama, Bliss (1987), AER — https://ideas.repec.org/a/aea/aecrev/v77y1987i4p680-92.html
7. Nelson, Siegel (1987) — https://doi.org/10.1086/296409
8. Estrella, Hardouvelis (1991), JF — https://doi.org/10.1111/j.1540-6261.1991.tb02674.x
9. Campbell, Shiller (1991), REStud — https://doi.org/10.2307/2298008
10. Taylor (1993) — https://doi.org/10.1016/0167-2231(93)90009-L ; Fed, reglas de política — https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm ; Atlanta Fed — https://www.atlantafed.org/cqer/research/taylor-rule
11. Estrella, Mishkin (1996) — https://www.newyorkfed.org/research/current_issues/ci2-7.html
12. Estrella, Mishkin (1998) — https://direct.mit.edu/rest/article/80/1/45/57058/Predicting-U-S-Recessions-Financial-Variables-as ; https://www.nber.org/papers/w5379
13. Elton, Gruber, Agrawal, Mann (2001) — https://doi.org/10.1111/0022-1082.00324
14. Collin-Dufresne, Goldstein, Martin (2001) — https://doi.org/10.1111/0022-1082.00402
15. Laubach, Williams (2003) — https://doi.org/10.1162/003465303772815934
16. Cochrane, Piazzesi (2005) — https://doi.org/10.1257/0002828053828581
17. Longstaff, Mithal, Neis (2005) — https://doi.org/10.1111/j.1540-6261.2005.00797.x
18. Kim, Wright (2005) — https://www.federalreserve.gov/data/three-factor-nominal-term-structure-model.htm ; FRED THREEFYTP10 — https://fred.stlouisfed.org/series/THREEFYTP10
19. Gürkaynak, Sack, Wright (2007) — https://doi.org/10.1016/j.jmoneco.2007.06.029
20. Ludvigson, Ng (2009) — https://doi.org/10.1093/rfs/hhp081
21. Giesecke, Longstaff, Schaefer, Strebulaev (2011) — https://doi.org/10.1016/j.jfineco.2011.01.011 ; https://www.nber.org/papers/w15848
22. Gagnon, Raskin, Remache, Sack (SR 441) — https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr441.pdf
23. Krishnamurthy, Vissing-Jorgensen (2011) — https://doi.org/10.1353/eca.2011.0019 ; https://www.nber.org/papers/w17555
24. Gilchrist, Zakrajšek (2012) — https://doi.org/10.1257/aer.102.4.1692
25. Huang, Huang (2012) — https://doi.org/10.1093/rapstu/ras011
26. Moskowitz, Ooi, Pedersen (2012) — https://doi.org/10.1016/j.jfineco.2011.11.003
27. Adrian, Crump, Moench (2013) — https://doi.org/10.1016/j.jfineco.2013.04.009 ; datos — https://www.newyorkfed.org/research/data_indicators/term-premia-tabs
28. Fleckenstein, Longstaff, Lustig (2014) — https://doi.org/10.1111/jofi.12032
29. Greenwood, Vayanos (2014) — https://doi.org/10.1093/rfs/hht133
30. Ilmanen, Maloney, Ross (2014) — https://doi.org/10.3905/jpm.2014.40.3.087
31. Holston, Laubach, Williams (2017) — https://doi.org/10.1016/j.jinteco.2017.01.004 ; HLW (2023) SR 1063 — https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1063.pdf ; estimaciones — https://www.newyorkfed.org/research/policy/rstar
32. Koijen, Moskowitz, Pedersen, Vrugt (2018) — https://doi.org/10.1016/j.jfineco.2017.11.002 ; https://www.nber.org/papers/w19325
33. Bauer, Hamilton (2018) — https://doi.org/10.1093/rfs/hhx096 ; https://www.nber.org/papers/w23480
34. Bauer, Mertens (2018), FRBSF EL 2018-20 — https://www.frbsf.org/research-and-insights/publications/economic-letter/2018/08/information-in-yield-curve-about-future-recessions/
35. Engstrom, Sharpe (2018/2019), FEDS 2018-055r1 — https://doi.org/10.17016/FEDS.2018.055r1
36. Gargano, Pettenuzzo, Timmermann (2019) — https://doi.org/10.1287/mnsc.2017.2829
37. Campbell, Pflueger, Viceira (2020) — https://doi.org/10.1086/707766 ; https://www.nber.org/papers/w20070
38. Vayanos, Vila (2021) — https://doi.org/10.3982/ECTA17440
39. Neville, Draaisma, Funnell, Harvey, Van Hemert (2021) — https://doi.org/10.2139/ssrn.3813202 ; https://www.man.com/insights/best-strategies-for-inflationary-times
40. Duffee (2022), Review of Finance — https://doi.org/10.1093/rof/rfac066
41. Brixton et al. (2023), JPM — https://doi.org/10.3905/jpm.2023.1.459 ; https://www.aqr.com/Insights/Research/Journal-Article/A-Changing-Stock-Bond-Correlation
42. Dickerson, Mueller, Robotti (2023), JFE — https://doi.org/10.1016/j.jfineco.2023.103707
43. Dick-Nielsen, Feldhütter, Pedersen, Stolborg (2023) — https://doi.org/10.2139/ssrn.4586652
44. Acharya, Laarits (2023) — https://www.nber.org/papers/w31863
45. Molenaar, Senechal, Swinkels, Wang (2024), FAJ — https://doi.org/10.1080/0015198X.2024.2317333
46. Rogoff, Rossi, Schmelzing (2024), AER — https://doi.org/10.1257/aer.20221352
47. Pflueger (2025), JFE — https://doi.org/10.1016/j.jfineco.2025.104027 ; https://www.nber.org/papers/w30921
48. Dickerson, Robotti, Rossetti (2026) — https://arxiv.org/abs/2604.07880
49. Lacava, Otranto (2026) — https://arxiv.org/abs/2601.21447
50. Covitz, Engstrom (2026), FEDS Note — https://www.federalreserve.gov/econres/notes/feds-notes/why-have-far-forward-nominal-treasury-rates-increased-so-much-in-the-past-few-years-20260212.html
51. FOMC 16-sep-2026 — https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm ; SEP — https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm
52. FOMC 29-oct-2025 (fin de QT) — https://www.federalreserve.gov/newsevents/pressreleases/monetary20251029a.htm ; FOMC 10-dic-2025 — https://www.federalreserve.gov/newsevents/pressreleases/monetary20251210a.htm
53. Tesoro, refinanciamiento 3T-2026 — https://home.treasury.gov/news/press-releases/sb0590 ; estimaciones — https://home.treasury.gov/news/press-releases/sb0584 ; TBAC — https://home.treasury.gov/news/press-releases/sb0591
54. The Conference Board, LEI de EUA — https://www.conference-board.org/topics/us-leading-indicators
55. Moody's, rebaja de 16-may-2025 (CNBC) — https://www.cnbc.com/2025/05/16/moodys-downgrades-united-states-credit-rating-on-increase-in-government-debt.html
56. FRED (T10Y3M, T10Y2Y, DGS1-30, GS10, TB3MS, DFII10, T10YIE, T5YIFR, BAMLH0A0HYM2, BAMLC0A0CM, ICSA, SAHMREALTIME, USREC, CPIAUCSL, PCEPILFE, UNRATE, DFEDTARU, FYFSGDA188S, FYOIGDA188S, FYGFGDQ188S, MTSDS133FMS, GDP, DCOILBRENTEU) — https://fred.stlouisfed.org/
57. Cetesdirecto, descripción de CETES, Bonos, Bondes F y UDIBONOS — https://www.cetesdirecto.com/sites/portal/productos.cetesdirecto
58. Yahoo Finance (precios ajustados de SPY, AGG, IEF, TLT, TMF, TBT, HYG, LQD, TIP, SHY, BIL, MXN=X y ^GSPC) para los cálculos propios — https://finance.yahoo.com
