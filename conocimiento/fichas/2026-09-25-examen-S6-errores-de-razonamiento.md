# Ficha: errores de razonamiento de S6 en la defensa oral

- **Fecha:** 2026-09-25 (tarea RM-B).
- **Origen:** `conocimiento/examenes/2026-09-25-diagnostico/S6/acta.md`, preguntas S6-01, S6-02 y S6-04. Las cifras cuestan 2.5 de los 60 puntos de S6: 0.5 por omitir el RF en S6-01 y 2.0 por las afirmaciones que cayeron en la defensa de S6-01, S6-02 y S6-04. Esta ficha cubre las de S6-02 y S6-04 y la omisión de S6-01. La frase del "mercado bajista" de S6-01 ya quedó resuelta en el acta y no se repite aquí.
- **Ejercicio reproducible:** `laboratorio/ilustraciones/S6_errores_de_razonamiento.py` (sha256 `65477f8b33611f266540bb93cb306b2efc90bf87167f2f38a1a97270599f3f2e`). Su salida está en `laboratorio/ilustraciones/S6_errores_de_razonamiento-salida.txt` (sha256 `a517c5d0b74044a2b6efb390e7033cd4cb3fddf14d3e1283d781111216e65662`). Las semillas son fijas y dos corridas dan una salida idéntica.
- **Datos:** los congelados de `laboratorio/examen-datos/S6/`; `sha256sum -c SHA256SUMS.txt` da los 11 archivos OK. Hay un dato externo nuevo, la tasa call de Japón (FRED), guardado en `laboratorio/ilustraciones/datos/fred_IRSTCI01JPM156N.csv`.
- **Herramienta:** `herramientas/estadistica.py` tiene 4 funciones nuevas: `pesos_bartlett(L)`, `autocovarianzas(x, L)`, `contribuciones_nw(x, L, kernel)` y `se_diferencia(se_a, se_b, corr)`. `herramientas/tests/test_estadistica.py` tiene 4 pruebas nuevas. Con ellas, la suite completa de `herramientas/tests` da 237 pruebas OK.

## Resumen

| # | Pregunta | Lo que se afirmó o se omitió | Lo correcto | Cifra decisiva |
|---|---|---|---|---|
| 1 | S6-01 | Omitió cuál es el RF. | El RF de los factores regionales de French es la **T-bill de EUA a 1 mes**. Todo está en USD. | 431 de 433 meses con RF idéntico al archivo de EUA. RF ×12 = 2.541 %, contra 0.632 % de la tasa call de Japón. |
| 2a | S6-02 | "gamma_6 compensa buena parte de rho1" | Con Bartlett y L = 6, gamma_6 pesa **1 − 6/7 = 1/7** y gamma_1 pesa 6/7. La frase solo es cierta con kernel uniforme. | Aporte a S: −0.421 contra +2.747. Quitar gamma_6 mueve el SE 1.9 % y la t 0.03. |
| 2b | S6-02 | El mínimo de 1,034 ventanas "casi garantiza" una t negativa significativa bajo una prima positiva. | Con la prima histórica, la probabilidad es **4.5 % a 12.8 %**. Solo con una prima de cero llega a 66 %. | Unas 56 a 61 pruebas independientes equivalentes, no 1,034. |
| 3 | S6-04 | "Tratar el benchmark como fijo subestima el SE" | Lo **sobrestima** cuando corr(rho_down, BGL) > se_BGL / (2·se_rho_down). Aquí la prueba de Fisher es **conservadora**. | corr = 0.74 contra un umbral de 0.46. sd(exceso) = 0.030 contra 0.035 de Fisher. Tamaño real bajo H0 normal: 2.0 % en vez de 5 %. |

---

## 1. La tasa libre de riesgo (RF) de los factores regionales de French (S6-01)

### El hecho, en la fuente primaria

Kenneth R. French, *Description of Fama/French 3 Factors for Developed Markets*, https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_3developed.html. La página se descargó completa (HTML) el 2026-09-25 a las 06:54 UTC; su sha256 es `28c2590f093caf91f16f26c206852123dcc4d97c8968a63fa6e143bfa1af3f37`. Texto literal:

> "All returns are in U.S. dollars, include dividends and capital gains, and are not continuously compounded. The market factor is the return on a region's value-weight market portfolio minus the U.S. one month T-bill rate."

La misma página confirma la construcción que en S6-11 se citó "de memoria" (el acta lo marca como hueco de base):

> "Big stocks are those in the top 90% of June market cap for the region, and small stocks are those in the bottom 10%. The B/M breakpoints for a region are the 30th and 70th percentiles of B/M for the big stocks of the region."

**El preámbulo del CSV regional no lo dice.** `Japan_3_Factors.csv` y `Europe_3_Factors.csv` solo traen "This file was created using the 202608 Bloomberg database" y "Missing data are indicated by -99.99". En cambio, `F-F_Research_Data_Factors.csv` sí describe su T-bill (Ibbotson hasta 202405 e ICE BofA US 1-Month Treasury Bill Index desde 202406). Quien lea solo el archivo regional no se entera de qué RF trae.

### Comprobación con los datos congelados

Comparé mes a mes la columna RF de los archivos regionales con la de `F-F_Research_Data_Factors.csv`:

| Archivo | Meses comunes | RF idéntico | Distintos |
|---|---|---|---|
| Japan_3_Factors (Bloomberg 202608) | 433 (1990-07 a 2026-07) | 431 | 1995-04 (0.45 contra 0.44) y 2025-07 (0.35 contra 0.34) |
| Europe_3_Factors (Bloomberg 202608) | 433 | 431 | los mismos dos meses |

Las dos diferencias son de 0.01 puntos, en el último decimal publicado. Su causa (redondeo o una versión distinta de la serie de T-bill entre la base Bloomberg 202608 y la CRSP 202607) queda **(no verificado)**.

### Por qué importa: ejercicio numérico

Japón en USD, de 1991-01 a 2025-12, n = 420 (salida E1):

| Concepto | Valor |
|---|---|
| Media del RF (T-bill de EUA) | 0.2118 %/mes, 2.541 % ×12. CAGR del RF: 2.569 % |
| Media ×12 de Mkt-RF (exceso sobre la T-bill **de EUA**) | 2.377 % |
| Media ×12 de R = Mkt-RF + RF | 4.919 % (= 2.377 + 2.541) |
| CAGR de R | 3.386 % (el valor comprometido en la clave) |
| Tasa call de Japón, OECD MEI vía FRED `IRSTCI01JPM156N` (media anual, 420 meses) | 0.632 % |

Consecuencias:

1. R_t = Mkt-RF + RF es la experiencia de un **inversionista en dólares**: acciones japonesas convertidas a USD, con el colateral en T-bills de EUA. Más de la mitad de la media aritmética de R (2.541 de 4.919 pp) es la T-bill de EUA, no la bolsa japonesa.
2. Mkt-RF **no** es el exceso sobre el efectivo en yenes. En el periodo, la T-bill de EUA rindió en promedio 1.9 pp al año más que la tasa call japonesa (2.541 contra 0.632). Quien lea Mkt-RF como "prima de riesgo japonesa local" se equivoca en el nivel y en la moneda.
3. Para la experiencia de un inversionista en yenes hacen falta el tipo de cambio JPY/USD y la tasa local. El JPY/USD no está en `examen-datos/S6/` y no se calculó **(no verificado)**.

**Regla operativa:** al citar un factor regional de French hay que escribir "en USD; RF = T-bill de EUA a 1 mes (French, página de construcción)". Para México (inversionista en MXN desde el SIC), el rendimiento relevante se arma aparte, con el tipo de cambio y Cetes (ver `laboratorio/tabla-maestra.md`, R01).

---

## 2a. El peso de Bartlett de gamma_6 con L = 6 (S6-02)

### Derivación

Newey y West (1986, NBER Technical Working Paper 55, p. 3, ec. 5) definen:

  S = gamma_0 + Σ_{j=1..L} w(j, L)·2·gamma_j,  con w(j, L) = 1 − j/(L+1)

(en la notación del artículo, m = L y Ω_j + Ω_j' = 2·gamma_j en el caso escalar). El enunciado de S6-02 usa exactamente estos pesos. Con L = 6:

| j | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| w_j = 1 − j/7 | 6/7 = 0.857 | 5/7 = 0.714 | 4/7 = 0.571 | 3/7 = 0.429 | 2/7 = 0.286 | **1/7 = 0.143** |

Tres propiedades se siguen directamente:

- **Peso relativo:** por unidad de autocovarianza, el rezago 6 pesa w_6/w_1 = 1/6 de lo que pesa el rezago 1.
- **Participación del último rezago:** Σ_{j=1..L} w_j = L/2, así que el último rezago tiene 1/(L+1) ÷ (L/2) = 2/(L(L+1)) del peso total: 4.8 % con L = 6, 1.3 % con L = 12 y 0.3 % con L = 24.
- **Efecto en el error estándar:** SE_NW = raíz(S/(n−1)), así que ∂ln SE/∂gamma_6 = (∂S/∂gamma_6)/(2S) = (2/7)/(2S) = 1/(7S).

### Ejercicio numérico: HML de EUA, 2007-01 a 2020-12, n = 168 (salida E2)

| j | gamma_j | rho_j | w_j Bartlett | aporte 2·w_j·gamma_j | aporte con kernel uniforme 2·gamma_j |
|---|---|---|---|---|---|
| 0 | 8.271 | 1.000 | 1 | 8.271 | 8.271 |
| 1 | 1.602 | 0.194 | 0.857 | **+2.747** | +3.204 |
| 2 | 0.435 | 0.053 | 0.714 | +0.622 | +0.871 |
| 3 | 0.174 | 0.021 | 0.571 | +0.198 | +0.347 |
| 4 | −0.461 | −0.056 | 0.429 | −0.395 | −0.921 |
| 5 | −0.257 | −0.031 | 0.286 | −0.147 | −0.514 |
| 6 | −1.472 | −0.178 | **0.143** | **−0.421** | −2.944 |
| **S** | | | | **10.875 (t = −1.736)** | **8.313 (t = −1.986)** |

- Con Bartlett, gamma_6 resta 0.421, que es el 15 % de lo que suma gamma_1 (2.747). Con el kernel uniforme resta 2.944, el 92 % de 3.204. "Compensa buena parte" describe el uniforme, no el estimador que se usó.
- Los rezagos 4 a 6 restan juntos 0.962, contra +3.567 de los rezagos 1 a 3.
- **Cuánto pesa gamma_6 en el SE:** si se fija gamma_6 = 0, S sube a 11.296, el SE pasa de 0.25519 a 0.26008 (+1.9 %) y la t de −1.736 a −1.704 (0.033 de diferencia). La aproximación lineal 1/(7S)·gamma_6 = 0.01314 × (−1.472) = −1.93 % coincide con el cambio exacto en logaritmos, −1.90 %.
- El SE de NW es 14.7 % mayor que el IID (cociente de varianzas 1.315) por gamma_1 a gamma_3, no por gamma_6.

### Por qué Bartlett no puede dar S < 0 y el kernel uniforme sí

Newey y West (1986, p. 4, Teorema 1 y ec. 6) demuestran que S = e'Pe/(L+1) ≥ 0, donde P es la matriz de Toeplitz (L+1)×(L+1) con P_ij = gamma_|i−j|, que es semidefinida positiva, y e es un vector de unos. Comprobación numérica: e'Pe/7 = 10.875135 = S, y el eigenvalor mínimo de P es 5.27 > 0. El kernel uniforme truncado (su ec. 4) "need not be positive semi-definite in any finite sample" (p. 2). En la prueba unitaria, una serie alternante (+1, −1, …) con L = 1 da S_uniforme = −0.8 y S_Bartlett = +0.1. Con datos centrados y L = n−1, el uniforme da exactamente 0.

---

## 2b. "Casi garantiza": probabilidad de una t negativa significativa en ventanas móviles bajo una prima positiva (S6-02)

### Derivación

Sea HML_t iid con media mu > 0 y desviación sigma. En una ventana de W meses, t ≈ N(delta, 1) con delta = mu·raíz(W)/sigma.

- **Una ventana:** p1 = P(t < −1.96) = Phi(−1.96 − delta).
- **K ventanas traslapadas:** consecutivas comparten W−1 de W meses. La probabilidad del mínimo está entre dos cotas. La inferior es la de las ventanas disjuntas, 1 − (1 − p1)^floor(N/W), porque el mínimo sobre todas es menor o igual que el mínimo sobre las disjuntas. La superior es la de Bonferroni, K·p1. El valor exacto se obtiene por simulación y se resume como un número de pruebas independientes equivalentes: M_ef = ln(1 − P_min)/ln(1 − p1).

### Ejercicio numérico: HML de EUA, 1926-07 a 2026-07, N = 1,201, W = 168, K = 1,034 (salida E3)

Media 0.355 %/mes, sigma = 3.552, así que delta = 0.355·raíz(168)/3.552 = **1.295**, y p1 = Phi(−3.255) = **0.00057**.

| Cálculo | P(mín t < −1.96) |
|---|---|
| 7 ventanas disjuntas (cota inferior, normal) | 0.40 % |
| Cota de Bonferroni 1,034·p1 (no informativa) | ≤ 58.6 % |
| Bootstrap iid, prima 0.355, t IID (B = 4,000) | **4.55 % ± 0.65** (mediana del mínimo −0.74; M_ef ≈ 61) |
| Bootstrap iid, prima 0.355, t NW(6) | 5.75 % ± 0.72 (M_ef ≈ 56) |
| Bootstrap circular por bloques de 24, t IID | **12.78 % ± 1.03** (mediana del mínimo −1.04; M_ef ≈ 61) |
| Bootstrap circular por bloques de 24, t NW(6) | 8.00 % ± 0.84 (M_ef ≈ 59) |
| Bootstrap iid con prima 0.20 / 0.10 / 0.00 (t IID, B = 2,000) | 21.7 % / 40.0 % / **66.4 %** |

Observado: la ventana 2007-01 a 2020-12 da t_IID = −1.991. El mínimo de las 1,034 ventanas es −2.065 (2006-10 a 2020-09), con p = 3.4 % (iid) a 10.1 % (bloques de 24). Con NW, el mínimo es −1.764, en la misma ventana, con p = 9.3 % a 12.6 %. Validación cruzada: la t_NW(6) por sumas acumuladas da −1.7364 en 2007-01, idéntica a `herramientas.estadistica.newey_west`.

**Conclusión:** bajo la prima histórica, el mínimo de las ventanas da una t significativa negativa entre 5 % y 13 % de las veces. No lo "garantiza". Solo se vuelve probable si la prima verdadera está cerca de cero, y eso es justamente lo que se quería probar. La corrección por *data snooping* reduce la evidencia de 2007-2020, pero no la anula. Las cifras coinciden, dentro del error de simulación, con las que el sustentante dio en la defensa (4.5 %, 12.8 %, 68 %, 41 %, 21 %; 45 a 80 pruebas). Para prima 0, 66.4 % contra 68 % es una diferencia de 1.5 errores estándar con B = 2,000.

---

## 3. Benchmark fijo: la dirección del sesgo del error estándar (S6-04)

### Derivación

Sea d = r − b, con r = rho_down estimada y b = el benchmark de Boyer, Gibson y Loretan (BGL) estimado con **la misma muestra**. Entonces:

  Var(d) = Var(r) + Var(b) − 2·Cov(r, b)

La prueba de Fisher con benchmark fijo usa solo Var(r): 1/(n_A − 3) en la escala z, que equivale a (1 − r²)²/(n_A − 3) en la escala rho por el método delta. Si λ = sd(b)/sd(r) y c = corr(r, b):

  Var(d)/Var(r) = 1 + λ² − 2cλ,  que es > 1  si y solo si  **c < λ/2**

Fijar el benchmark tiene dos efectos opuestos: ignora Var(b), que subiría el SE, e ignora la covarianza positiva, que lo bajaría. **Subestima el SE solo si c < sd(b)/(2·sd(r)).** Con sd(b) ≈ sd(r), el umbral es ≈ 0.5. Un benchmark independiente (de otra muestra, c = 0) sí haría que la prueba subestimara el SE. Un benchmark calculado con los mismos datos suele tener c alta y hace la prueba conservadora.

¿Por qué es positiva la covarianza? El BGL es rho·[rho² + (1 − rho²)·q]^(−1/2), con q = Var(X)/Var(X|A). La rho total incluye los meses de caída, que tienen |X| grande y pesan mucho en la covarianza. En el bootstrap, corr(rho_down, rho total) = 0.61. Cuando una réplica sube rho_down, sube también el benchmark. Es la misma lógica de una prueba pareada contra una no pareada.

La herramienta: `estadistica.se_diferencia(se_a, se_b, corr)`. En el punto del umbral, se_diferencia = se_a.

### Ejercicio numérico: EUA (X) contra Europa (Y), Mkt-RF, 1990-07 a 2025-12, n = 426 (salida E4)

rho = 0.7948. Hay 154 meses con X < 0, en los que rho_down = 0.7574 y BGL = 0.6901, así que el exceso es 0.0674. La prueba de Fisher con benchmark fijo da z = 1.745 (p = 0.081), con un SE implícito en la escala rho de (1 − 0.7574²)/raíz(151) = **0.0347**.

| Método | sd(rho_down) | sd(BGL) | corr | umbral c* | sd(exceso) | IC95 del exceso |
|---|---|---|---|---|---|---|
| Bootstrap iid de pares (B = 5,000) | 0.0436 | 0.0400 | **0.741** | 0.459 | **0.0303** | [0.0090, 0.1282] |
| Bootstrap circular por bloques de 12 (B = 2,000) | 0.0490 | 0.0455 | 0.835 | 0.465 | 0.0274 | [0.0121, 0.1181] |
| Bootstrap circular por bloques de 24 (B = 2,000) | 0.0492 | 0.0492 | 0.800 | 0.500 | 0.0311 | [0.0104, 0.1321] |

- En los tres casos c > c*, así que la sd real del exceso (0.027 a 0.031) es **menor** que el 0.0347 de Fisher. Con la sd del bootstrap iid, z = 0.0674/0.0303 = 2.23, contra 1.745 de Fisher. Esto reconcilia lo que la respuesta escrita no reconcilió: el bootstrap excluía el 0 y Fisher no rechazaba.
- Hay un segundo sesgo, en sentido contrario. Por colas gruesas y agrupamiento de volatilidad, el SE normal de rho_down (0.0347) subestima su sd real (0.044 a 0.049). En estos datos pesa más la covarianza, así que el efecto neto es conservador.

### Comprobación bajo H0 (Monte Carlo, R = 20,000)

El modelo es una normal bivariada con rho = 0.795 constante, así que el BGL es exacto. n = 426, y la media de X está fijada para que P(X < 0) = 154/426 (en promedio, n_down = 154.0).

- Media de rho_down: 0.5766. Media del BGL: 0.5769. El sesgo del exceso es −0.0003, así que BGL centra bien.
- sd(rho_down) = 0.0574, contra 0.0543 implícito en Fisher: por el truncamiento de X, Fisher subestima 6 % incluso con normalidad. sd(BGL) = 0.0343, corr = 0.601, contra un umbral de 0.299. sd(exceso) = 0.0459.
- **El tamaño real de la prueba de Fisher con benchmark fijo, al 5 % nominal, es 1.97 % ± 0.30.** La sd del estadístico z es 0.843, no 1. La prueba es conservadora, como dijo la defensa.

**Cómo debió redactarse la limitación (1):** "Tratar el benchmark como fijo omite su varianza (lo que subestimaría el SE) y su covarianza positiva con rho_down, porque las dos salen de la misma muestra (lo que lo sobrestima). Aquí la correlación es de ≈ 0.74 y supera el umbral de ≈ 0.46, así que la prueba de Fisher es conservadora: el bootstrap que re-estima el benchmark da z ≈ 2.2. Aparte, las colas gruesas hacen que el SE normal de rho_down sea bajo." Aun así, la conclusión sustantiva sigue siendo prudente: pocas crisis (1998, 2001-02, 2008, 2020) dominan el resultado.

---

## Comprobación

1. **Pruebas unitarias** (`python3 -m unittest herramientas.tests.test_estadistica`: 9 OK; la suite completa de `herramientas/tests` da 237 OK):
   - `test_pesos_bartlett`: w_6 = 1/7 con L = 6, y Σ w_1..w_L = L/2 para L = 0..24.
   - `test_contribuciones_coinciden_con_newey_west`: `contribuciones_nw` reproduce el SE y la t de `newey_west` (12 decimales) para L = 0, 1, 6 y 12, y c_L = 2·gamma_L/(L+1).
   - `test_bartlett_semidefinido_uniforme_no`: S_Bartlett = e'Pe/(L+1) ≥ 0 (NW, Teorema 1). La serie alternante da un S uniforme negativo, y el uniforme con L = n−1 da 0.
   - `test_se_diferencia_y_benchmark_fijo`: con c = 0 el SE de la diferencia supera a se_a (fijar subestima); en c* = se_b/(2se_a) es igual a se_a; con c = 0.75 es menor (fijar sobrestima).
2. **Reproducción del acta:** t_NW(6) = −1.7364, S = 10.875, gamma_6 = −1.472, aporte de −0.42 contra +2.75, S uniforme = 8.31 y t = −1.99. En E3: 4.5 % (iid) y 12.8 % (bloques de 24). En E4: z = 1.745, corr ≈ 0.74 y sd(exceso) ≈ 0.030. Todo coincide con las cifras del juez y de la defensa.
3. **Doble cálculo interno:** la t_NW por sumas acumuladas en ventanas coincide con `newey_west` (−1.7364). La fórmula `se_diferencia` sobre los momentos del bootstrap (0.0303) coincide con la sd directa del exceso (0.0303). Ambos son el mismo cálculo con los mismos datos, no una segunda fuente independiente (ver `conocimiento/registro-de-errores.md`, 2026-09-25).

## Reglas que deja esta ficha

1. Antes de decir que un rezago "compensa" a otro, escribe su peso: con Bartlett, w_L = 1/(L+1). `contribuciones_nw` da el aporte de cada rezago.
2. "Casi garantiza", "casi seguro" y frases parecidas exigen un número: simula la probabilidad bajo la hipótesis que se critica y reporta M_ef.
3. Si el benchmark se estima con la misma muestra, calcula corr(estimador, benchmark) y compárala con se_b/(2·se_a) antes de decir en qué dirección está sesgado el SE. Sin ese cálculo, di solo "el SE ignora la incertidumbre del benchmark; la dirección del sesgo depende de la covarianza".
4. Factores regionales de French: USD y RF = T-bill de EUA a 1 mes. Hay que decirlo siempre, porque el CSV regional no lo trae.

## Fuentes y nivel de acceso

| Fuente | Qué se verificó | Acceso real |
|---|---|---|
| French, *Fama/French 3 Factors for Developed Markets*, https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_3developed.html | Todo está en USD; Mkt-RF se mide contra la "U.S. one month T-bill rate"; Big = 90 % superior; cortes de B/M 30/70 sobre las grandes | Página completa (HTML), 2026-09-25 06:54 UTC, sha256 `28c2590f…3f37` |
| French Data Library: `Japan_3_Factors_CSV.zip`, `Europe_3_Factors_CSV.zip` (Bloomberg 202608) y `F-F_Research_Data_Factors_CSV.zip` (CRSP 202607) | RF idéntico en 431 de 433 meses; series de E1 a E4 | Datos primarios congelados; `sha256sum -c` OK |
| Newey, W. y West, K. (1986), "A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix", NBER Technical Working Paper 55, https://www.nber.org/system/files/working_papers/t0055/t0055.pdf | Ec. (4): el uniforme no es semidefinido positivo. Ec. (5): w(j, m) = 1 − j/(m+1). Teorema 1 y ec. (6): S = e'Pe/(m+1) ≥ 0 | PDF escaneado de 14 páginas, sin capa de texto (sha256 `c93e71c7…017`), 2026-09-25 06:55 UTC. Se leyeron como imagen las páginas 1, 4, 5 y 6 del PDF (portada y páginas impresas 2, 3 y 4) |
| Newey y West (1987), Econometrica 55(3):703-708 | La versión publicada | **(no verificado en esta sesión)**: se leyó el working paper de 1986, no el artículo publicado |
| Boyer, Gibson y Loretan (1997, rev. 1999), IFDP 597, https://www.federalreserve.gov/pubs/ifdp/1997/597/ifdp597.pdf | Teorema 1, ec. (1): rho_A = rho·[rho² + (1 − rho²)·Var(x)/Var(x∣A)]^(−1/2) | Texto completo (PDF), sha256 `f70113bb…a7d743` |
| FRED `IRSTCI01JPM156N`, "Interest Rates: Immediate Rates (< 24 Hours): Call Money/Interbank Rate: Total for Japan", en %, mensual, fuente OECD MEI | Media de 1991-01 a 2025-12: 0.632 % anual (420 meses) | CSV y página de la serie (actualizada el 15 de septiembre de 2026), 2026-09-25 06:59 UTC, sha256 `41c22221…cd3` |
| Fisher (1915, 1921), la transformación z y el SE 1/raíz(n−3) | Se usó la fórmula del enunciado. Su comportamiento se comprobó por Monte Carlo: sd(rho_down) = 0.0574 contra 0.0543 implícito | Fuente original **(no verificado)** |

**No verificado o fuera de alcance:** la causa de las dos diferencias de 0.01 en el RF (1995-04 y 2025-07); el rendimiento de un inversionista en yenes (no hay JPY/USD en los datos); el crítico sup-Wald de 8.85 de Andrews (1993) y el crítico *fixed-b* de ≈ 2.08 de Kiefer y Vogelsang, que se citaron de memoria en la defensa y no se revisaron aquí; y las citas de Longin y Solnik (2001) y de Ang y Chen (2002), que no se volvieron a leer.
