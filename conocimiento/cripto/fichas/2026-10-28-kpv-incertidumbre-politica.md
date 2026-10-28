# Ficha de avance · 28-oct-2026 · Kelly-Pástor-Veronesi (JF 2016): el precio de la incertidumbre política en opciones, replicado con el VIX (1990-2024) y el DVOL

> **Por qué este tema.** Es el siguiente punto de la cola académica del plan (`00-plan-de-estudio.md`, fila "Literatura académica…": "Kelly-Pástor-Veronesi (JF 2016, elecciones y opciones) si hay copia legal") y el punto 2 de la §7 de la ficha del 27-oct. Ayer se midió la prima electoral de BTC en corte transversal y quedó sin veredicto (5 elecciones). KPV dan el diseño de referencia; hoy se replica en EUA, dentro y fuera de su muestra, y se lleva a BTC.

## 0. Preguntas de hoy

1. ¿Qué afirman KPV, con qué diseño y qué tan grande es el efecto?
2. ¿Su medida (IVD) se reproduce en EUA con datos públicos y **sobrevive fuera de su muestra** (2014-2024)?
3. ¿Hay algo parecido en BTC y qué dice la cadena hoy para el 3-nov?

## 1. Acceso y fuentes (declarado)

| Fuente | Grado | Acceso real |
|---|---|---|
| **Kelly, Pástor y Veronesi, "The Price of Political Uncertainty: Theory and Evidence from the Option Market"**, NBER WP 19812 (ene-2014, rev. jul-2015), [nber.org/papers/w19812](https://www.nber.org/papers/w19812). Publicado en *Journal of Finance* 71(5), 2016 | **A** (revista de primer nivel; el WP es la versión del autor) | **Íntegro el WP** (PDF oficial de NBER, ~70 págs.): leídos completos la introducción, §2 (diseño), §3 (resultados) y §6 (conclusiones), además de las tablas 2 y 3. La teoría (§4-5) se leyó por encima. **La versión publicada en JF no se leyó**: las cifras citadas son las del WP |
| **Yahoo `^VIX`** (chart v8, 1d, 1990-2026). El VIX de CBOE es una varianza de swap a 30 días naturales, recalculada hacia atrás hasta 1990 | **A/B** (dato del índice vía agregador) | Íntegro; foto del 28-oct 14:28 UTC en [`2026-10-28-kpv-incertidumbre-politica-datos.json`](2026-10-28-kpv-incertidumbre-politica-datos.json). El último dato (28-oct) es **intradía** |
| **Deribit** `public/get_volatility_index_data` (DVOL 1D, 24-mar-2021 a 28-oct-2026) y `public/get_book_summary_by_currency` (474 opciones de 6 vencimientos, `mark_iv` y `open_interest`) | **A** | Íntegro (en el `.json`) |
| **2 U.S.C. § 7**: la elección es el martes siguiente al primer lunes de noviembre de los años pares (ficha del 27-oct) | **A** (ley) | Íntegro |

## 2. Lo esencial de KPV

- **[H] Diseño.** Hay 271 eventos políticos (64 elecciones nacionales y 216 cumbres) en 20 países, con opciones de índice de OptionMetrics de 1990 a 2012. EUA aporta 11 elecciones (tabla 2). Para cada evento τ, el vencimiento mensual *b* es el primero después de τ, *a* el anterior y *c* el siguiente a *b*. La medida es **IVD = IV_b − ½(IV_a + IV_c)**, donde cada IV promedia las opciones ATM (0.4 < |Δ| < 0.5, OI > 0) **con el mismo plazo** en los 20 días hábiles antes de τ (ec. 1-2). Comparar opciones del mismo plazo neutraliza la estructura de plazo. Por eso KPV **rechazan** el diseño de corte transversal (dos vencimientos el mismo día, §2.1.4), que es el que usó la ficha del 27-oct.
- **[H] Resultado 1.** El IVD medio es **+1.43 pts** de vol anual (t = 4.43): las opciones cuya vida abarca el evento son **~5.1% más caras** (1.43 / 27.8 del grupo de control). En elecciones solas es **+1.63** (t = 3.13, n = 64). El caso extremo es la elección de EUA de 2008 combinada con el G20: **+12.2 pts**.
- **[H] Resultado 2.** La prima de riesgo de varianza también sube (VRPD 0.0107, t = 2.61) y la pendiente put también (SlopeD +1.73 ×100, t = 3.59). Un put a 5% OTM que abarca el evento es 9.6% más caro, y uno a 10% OTM, 16.0%. Se paga **protección de cola**, no solo nivel.
- **[H] Resultado 3.** El efecto es mayor con la economía débil: ATM ~8% más caro con economía débil contra ~1% con economía fuerte. También es mayor cuando la encuesta está cerrada: la relación es significativa para IV y VRP, no para la pendiente.
- **[I] Mecanismo (modelo de Pástor-Veronesi).** El gobierno elige una política y el mercado no sabe cuál. La incertidumbre política es un **salto en fecha conocida** y tiene prima porque los cambios de política son más probables en malos tiempos.

## 3. Ejercicio numérico (comprobado en Python)

Código: [`2026-10-28-kpv-incertidumbre-politica.py`](2026-10-28-kpv-incertidumbre-politica.py). Se reproduce con `python3 -I conocimiento/cripto/fichas/2026-10-28-kpv-incertidumbre-politica.py` (y con `… descargar` para una foto nueva).

**Adaptación (declarada).** No hay OptionMetrics. En su lugar se usa un índice de **plazo constante** de 30 días naturales: el VIX para el S&P y el DVOL para BTC. Así la comparación entre plazos iguales que buscan KPV sale por construcción.
- **Tratamiento:** días hábiles [τ−20, τ−1]. Toda ventana de 30 días que empieza ahí abarca τ.
- **Control *a*:** días hábiles [τ−41, τ−22]. La ventana termina antes de τ.
- **Control *c*:** días hábiles [τ+1, τ+20].
- **Agregación:** igual que KPV, la raíz del promedio de varianzas.
- **Diferencia con KPV:** el VIX es una varianza de swap, no una IV ATM. Además, todo es un solo país.

### A. Comprobación de la conversión de KPV

- 1.43 / 27.8 = **5.14%**.
- La elasticidad precio-vol de un put ATM a plazo (σ 27.8%, 1 mes) es **0.9995**, así que subir σ de 27.8 a 29.23 encarece el put **+5.14%**.
- Reproduce la cifra de KPV y su nota 18.

### B. IVD con el VIX en las 18 elecciones federales de 1990 a 2024

| Año | Tipo | IV_b | IV_a | IV_c | **IVD** | IVD / control |
|---|---|---|---|---|---|---|
| 1990 | intermedia | 30.29 | 28.75 | 23.62 | +4.11 | +15.7% |
| 1992 | presidencial | 17.60 | 14.19 | 14.03 | +3.49 | +24.8% |
| 1994 | intermedia | 15.34 | 14.31 | 16.49 | −0.06 | −0.4% |
| 1996 | presidencial | 16.65 | 16.12 | 16.10 | +0.54 | +3.4% |
| 1998 | intermedia | 35.67 | 38.73 | 26.11 | +3.25 | +10.0% |
| 2000 | presidencial | 25.99 | 20.35 | 26.94 | +2.35 | +9.9% |
| 2002 | intermedia | 34.18 | 37.45 | 27.95 | +1.47 | +4.5% |
| 2004 | presidencial | 15.25 | 13.97 | 13.29 | +1.62 | +11.9% |
| 2006 | intermedia | 11.11 | 11.93 | 10.83 | −0.27 | −2.4% |
| 2008 | presidencial | 64.46 | 34.44 | 64.40 | **+15.04** | +30.4% |
| 2010 | intermedia | 20.21 | 22.43 | 20.07 | −1.04 | −4.9% |
| 2012 | presidencial | 16.68 | 15.14 | 16.58 | +0.82 | +5.2% |
| 2014 | intermedia | 18.69 | 14.12 | 13.25 | +5.00 | +36.6% |
| 2016 | presidencial | 16.59 | 14.39 | 13.25 | +2.77 | +20.0% |
| 2018 | intermedia | 21.34 | 12.70 | 19.42 | +5.28 | +32.8% |
| 2020 | presidencial | 30.47 | 27.48 | 23.57 | +4.94 | +19.4% |
| 2022 | intermedia | 28.85 | 28.91 | 22.33 | +3.23 | +12.6% |
| 2024 | presidencial | 20.17 | 17.51 | 14.95 | +3.93 | +24.2% |

**Segunda lectura:** 2016 y 2024 se recalcularon con un código aparte, con índices escritos a mano. Las ventanas de 2024 fueron 8-oct a 4-nov (*b*), 9-sep a 4-oct (*a*) y 6-nov a 4-dic (*c*). Las cifras coinciden al centésimo.

| Muestra | n | Media IVD | t | Mediana | Positivos | Relativa | p placebo* |
|---|---|---|---|---|---|---|---|
| 1990-2012 (muestra de KPV) | 12 | **+2.61** | 2.14 | +1.55 | 9/12 | +9.0% | 0.007 |
| **2014-2024 (fuera de muestra)** | 6 | **+4.19** | 9.87 | +4.44 | **6/6** | **+24.3%** | 0.008 |
| 1990-2024 | 18 | +3.14 | 3.77 | +3.00 | 15/18 | +14.1% | < 0.001 |
| Intermedias | 9 | +2.33 | 2.94 | +3.23 | — | — | 0.019 |
| Presidenciales | 9 | +3.95 | 2.69 | +2.77 | — | — | 0.002 |

\* Distribución nula: el mismo IVD calculado en los 7,576 días a más de 45 hábiles de una elección (media −0.04, desviación 2.85). Se sacan 20,000 grupos de *n* pseudo-eventos y se cuenta cuántos tienen una media igual o mayor que la observada, como en la tabla 8 de KPV.

- **Robustez, dejando uno fuera:** dentro de la muestra, la media va de +1.48 (sin 2008) a +2.94; fuera de la muestra, de +3.98 a +4.48. **Fuera de la muestra, ningún año sostiene el resultado por sí solo.**
- **Placebo de calendario** (el mismo martes de noviembre en los 18 años impares de 1991 a 2025): media **−0.40** (t −0.77), con 9/18 positivos. **Pares menos impares: +3.54 pts (t de Welch +3.61).** La prima no es estacionalidad de octubre ni el FOMC de principios de noviembre, que cae tanto en años pares como impares.
- **De dónde sale la prima:** fuera de la muestra, IV_b − IV_a = +3.50 e IV_b − IV_c = +4.89. La vol sube antes de la elección y cae después.

### C. 2026, lo que ya se observa (τ = martes 3-nov)

- **VIX:** hay 17 de los 20 días del tratamiento (el 28-oct es intradía). IV_b parcial **17.04** contra IV_a **15.95**: **+1.09**. En el mismo tramo parcial de las elecciones de 1990 a 2024, la media es +3.21 y la mediana +1.32. **2026 queda en el percentil 39: prima electoral normal tirando a baja en el S&P.**
- **DVOL (BTC):** hay 15 de los 20 días naturales. IV_b parcial **37.98** contra IV_a **36.19**: **+1.79**.

### D. BTC con el DVOL (solo 2 elecciones)

| Elección | IV_b | IV_a | IV_c | IVD | Lectura |
|---|---|---|---|---|---|
| 2022 | 60.00 | 73.82 | 85.58 | −19.70 | **Contaminada:** FTX quebró del 8 al 11-nov-2022 |
| 2024 | 57.98 | 52.96 | 57.87 | **+2.56** (+4.6%) | Percentil 71 de la nula del DVOL (n 1,696, desviación 6.30): **no se distingue del ruido** |

### E. Pendiente put de KPV en la cadena de BTC (foto del 28-oct 14:28 UTC; corte transversal)

Regresión de la IV (`mark_iv`) sobre la Δ de Black-76 de los puts con −0.5 < Δ < −0.1 y OI > 0:

| Vencimiento | Días | n | Pendiente | IV(Δ −0.10) − IV(Δ −0.50) | IV ATM |
|---|---|---|---|---|---|
| 30-oct | 1.7 | 5 | 0.137 | +5.5 pts | 36.2 |
| 31-oct | 2.7 | 6 | 0.129 | +5.2 | 34.8 |
| **6-nov** (abarca la elección) | 8.7 | 7 | **0.165** | **+6.6** | **38.2** |
| 13-nov | 15.7 | 6 | 0.130 | +5.2 | 36.6 |
| 27-nov | 29.7 | 12 | 0.186 | +7.4 | 35.9 |
| 25-dic | 57.7 | 9 | 0.201 | +8.0 | 36.9 |

- El vencimiento del 6-nov tiene **más pendiente put que sus dos vecinos**: +0.035 contra su promedio, que en las unidades de KPV (×100) son +3.5, contra el SlopeD medio de +1.73 en acciones.
- El 13-nov también abarca la elección y no muestra el salto. A partir del 27-nov la pendiente crece con el plazo.
- **Lectura [I]:** la cadena concentra la protección de cola en el vencimiento más próximo después del 3-nov, como predicen KPV. Es **una sola foto**, con 5 a 7 puts por vencimiento y una IV de modelo, así que **no es una prueba**.

## 4. Qué cambia para invertir [I/O]

- **La prima electoral en opciones de índice de EUA es un hecho robusto y sigue vigente.** Fuera de la muestra de KPV es incluso mayor: +4.2 pts y 6 de 6 positivos, contra +2.6 dentro. El patrón es **vol que sube antes y cae después**. Para el sistema esto se vuelve una **regla de lectura**: un VIX o un DVOL altos en los 20 días previos a una elección son en parte prima de seguro que **se espera que se desinfle**, no una señal de riesgo nuevo. No hay que leerlos como alarma de régimen.
- **En BTC no hay evidencia propia**: con una elección limpia (2024, +2.6, percentil 71) no se puede afirmar nada. Lo único verificable es la mecánica: cuando la elección sale de la ventana de 30 días, el DVOL baja ~1.5 pts si el resto queda igual (varianza extra de 8.86 %² de la ficha del 27-oct; 37.7 → 36.2).
- **Pronóstico P0196** (DVOL del 4-nov < DVOL del 2-nov, p = 0.70). Con él se mide la predicción "IV_c < IV_b" en BTC con un evento nuevo.
- **2026 en el S&P:** prima en el percentil 39, sin miedo electoral extra. El VIX va en 17.34 en la foto (intradía), lejos de los 20 de P0183. **Ninguna acción.** La cuenta cripto es spot y no puede vender opciones. El filtro sigue con colchón de +13.7%.
- **[O] Relevancia cripto específica:** la intermedia decide la composición del Congreso que retomaría la CLARITY (cloture fallida el 15-sep-2026, plan §Frontera). Es incertidumbre de política **sectorial**, que KPV no miden. Queda como hipótesis.

## 5. Contrapuntos y límites

- **El VIX no es la IV ATM de KPV:** es una varianza de swap y pesa las alas. Parte del IVD puede venir de la cola (lo que KPV miden aparte con SlopeD). Las dos medidas no son idénticas.
- **Fuera de muestra son 6 eventos**, y en 2 de ellos hubo choques de octubre no políticos (flash crash del 15-oct-2014 y venta de oct-2018), que inflan IV_b. El placebo de años impares controla la estación, pero no esos choques. El t de 9.87 sale de 6 datos; el p de placebo (0.008) es la cifra honesta.
- **La ventana *c* usa información posterior al evento** (igual que KPV). Sirve para medir, no para operar en tiempo real. La versión que sí se puede usar en tiempo real es IV_b − IV_a, y en 2026 da +1.09.
- **BTC:** el DVOL existe desde mar-2021, así que solo hay 2 elecciones y una está contaminada. La pendiente del corte transversal usa `mark_iv` (modelo de Deribit) y pocos puts.
- **No se leyó la versión publicada en JF**, que pudo cambiar cifras respecto del WP de jul-2015.

## 6. Autoexamen

1. ¿Por qué KPV comparan opciones del mismo plazo en fechas distintas y no dos vencimientos el mismo día? (Para que la estructura de plazo, que cambia con la economía, no contamine la prueba de "economía débil → prima mayor".)
2. ¿Por qué un IVD de 1.43 pts equivale a ~5.1% de precio en un put ATM? (La elasticidad precio-vol del put ATM a plazo es ≈ 1: 1.43 / 27.8.)
3. ¿Qué descarta el placebo de años impares? (Que la prima sea estacionalidad de octubre-noviembre o efecto del FOMC de noviembre.)
4. ¿Por qué el DVOL debería bajar ~1.5 pts después del 3-nov aunque nada cambie? (La varianza extra del evento sale de la ventana de 30 días: √((37.7² × 30/365 − 8.86) × 365/30) ≈ 36.2.)

## 7. Estado

- **Documentado con comprobación** (Doctorado: literatura académica, incertidumbre política y opciones). Paper leído íntegro en su versión WP (A). Réplica propia en EUA, dentro y fuera de muestra, con dos placebos, robustez dejando uno fuera y segunda lectura de 2 filas. En BTC solo hay descripción.
- **Hallazgo:** la prima electoral de KPV **sobrevive fuera de muestra** en el VIX: 2014-2024 da +4.19 pts, 6/6 positivos y p placebo 0.008, contra −0.40 en años impares. En 2026 va en el percentil 39. En BTC no hay muestra.
- **Siguiente prueba:**
  1. resolver P0196 (5-nov), P0190 (4-nov) y P0184 (29-oct);
  2. completar el IVD de 2026 con *c* (vigésimo día hábil después del 3-nov, ~2-dic) en el VIX y el DVOL;
  3. el SlopeD de KPV en serie histórica para BTC, que requiere cadenas históricas sin vía gratuita conocida;
  4. Pástor-Veronesi (JFE 2013, "Political uncertainty and risk premia"), si hay copia legal.
