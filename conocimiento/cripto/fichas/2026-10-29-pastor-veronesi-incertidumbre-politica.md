# Ficha de avance · 29-oct-2026 · Pástor-Veronesi (JFE 2013): incertidumbre política, volatilidad y prima de riesgo, replicado fuera de muestra y llevado a BTC

> **Por qué este tema.** Es el siguiente punto viable de la cola académica del plan (`00-plan-de-estudio.md`, fila "Literatura académica…": "Pástor-Veronesi (JFE 2013) si hay copia legal"), y el punto 4 de la §7 de la ficha del 28-oct. Los dos puntos anteriores de la cola, la prima electoral con los diarios del 3-4-nov y la ventana *c* del IVD (~2-dic), todavía no tienen datos. Los 35 recursos del índice ya están en `estudiado`. KPV (ayer) mide la incertidumbre política **en fecha conocida** (elecciones). PV 2013 da el modelo de fondo y una prueba en **serie de tiempo** con el índice de Baker-Bloom-Davis (BBD). Esa prueba sí se puede llevar a BTC.

## 0. Preguntas de hoy

1. ¿Qué predice el modelo de PV y qué tan fuerte es su evidencia empírica (§7, tablas 2-5)?
2. ¿Se reproduce con datos públicos en su muestra (1985-2010) y **sobrevive fuera de ella** (2011-2026)?
3. ¿La incertidumbre de política de EUA mueve la volatilidad de BTC o su correlación con el S&P?

## 1. Acceso y fuentes (declarado)

| Fuente | Grado | Acceso real |
|---|---|---|
| **Pástor y Veronesi, "Political Uncertainty and Risk Premia"**, NBER WP 17464 (sep-2011, **rev. abr-2013**), [nber.org/papers/w17464](https://www.nber.org/papers/w17464). Publicado en *Journal of Financial Economics* 110(3), 2013 | **A** (revista de primer nivel; el WP es la versión del autor) | **Sección amplia del WP** (PDF oficial de NBER, 48 págs.): leídos completos el resumen, la introducción, §7 (análisis empírico, págs. 33-38), las conclusiones y las tablas 1-5. El modelo (§2-6) se leyó por encima. **La versión publicada en JFE no se leyó**: las cifras citadas son las del WP de abr-2013 |
| **Baker, Bloom y Davis, índice EPU de EUA** ([policyuncertainty.com](https://www.policyuncertainty.com/media/US_Policy_Uncertainty_Data.xlsx), xlsx del 28-sep-2026). Hoja "Legacy Three Component EPU" (1985-2026) y hoja "Main News Index" (1900-2026) | **A** (dato de los autores, uso libre con atribución) | Íntegro. **La añada no es la de PV:** ellos bajaron el índice el 17-oct-2011, y la versión de hoy está revisada |
| **FRED**: CFNAI, USREC, INDPRO, BAA y AAA (mensuales) | **A** | Íntegro. CFNAI e INDPRO son añadas de hoy, no las de 2011 |
| **Yahoo** `^GSPC` (1985-2026), `^VIX` (1990-2026) y `BTC-USD` (2014-2026), diarios. **Deribit** DVOL 1D (2021-2026) | **A/B** | Íntegro. Foto del 29-oct 14:53 UTC en [`2026-10-29-pastor-veronesi-incertidumbre-politica-datos.json`](2026-10-29-pastor-veronesi-incertidumbre-politica-datos.json) |

## 2. Lo esencial de PV

- **[H] Modelo.** El gobierno elige entre políticas cuyo efecto en la rentabilidad agregada es incierto. Los inversionistas aprenden de señales políticas. Hay dos clases de choque: de **impacto** (qué hará la política) y **político** (qué política se elegirá). El gobierno cambia de política sobre todo cuando la economía va mal, y eso equivale a una **opción put implícita** a favor del mercado.
- **[H] Predicciones (§7).**
  1. La incertidumbre política (PU) es mayor con la economía débil.
  2. Con más PU, las acciones son más volátiles.
  3. Con más PU, las acciones están más correlacionadas.
  4. La PU tiene prima de riesgo.
  5. Los efectos 2-4 son mayores con la economía débil.

  El put del gobierno empuja la prima de riesgo en sentido contrario, así que el signo de la predicción 4 sin condicionar es ambiguo.
- **[H] Evidencia (EUA, mensual, 1985-2010; índice BBD como proxy de PU).**
  - **Tabla 2:** PU sobre condiciones económicas, b < 0 en 10 de 10 especificaciones y 8 significativas (CFI: −0.31, t −7.24).
  - **Tabla 3:** volatilidad (realizada e implícita) y correlación sobre PU, b > 0 en 8 de 8, todas significativas (VIX: t 5.27; con rezago, 2.53).
  - **Tabla 4:** interacción PU·E sobre la volatilidad, 20 de 20 negativas y 18 significativas. Sobre la correlación es débil: 5 de 20 significativas.
  - **Tabla 5:** la prima de riesgo sin condicionar es positiva pero **no significativa**. Condicionada (PU·E), 15 de 15 negativas, pero solo 6 significativas.
  - Los autores llaman a todo esto "simple exploratory" e "illustrative", y advierten que el índice BBD también capta incertidumbre económica general.

## 3. Ejercicio numérico (comprobado en Python)

Código: [`2026-10-29-pastor-veronesi-incertidumbre-politica.py`](2026-10-29-pastor-veronesi-incertidumbre-politica.py) (solo biblioteca estándar; MCO con Newey-West escrito a mano). Se reproduce con `python3 -I conocimiento/cripto/fichas/2026-10-29-pastor-veronesi-incertidumbre-politica.py` (y con `… descargar` para una foto nueva).

**Adaptación (declarada).**
- PU = índice de tres componentes / 100 (principal) o índice de noticias / 100 (robustez).
- E = CFI, −REC, IPG y −DEF (BAA − AAA de Moody's; PV usan AAA − BBB). **Sin P/E de Shiller.**
- RV = desviación de los rendimientos log diarios del S&P del mes, anualizada en decimal. IV = promedio mensual del VIX / 100.
- La tabla 5 usa el rendimiento de **precio** del S&P, no el exceso de CRSP.
- **No se replica la correlación entre acciones** (requiere los rendimientos de los 500 componentes).
- Las escalas de PV no están documentadas (su b del VIX es 0.08 y el mío 0.15). Por eso se comparan **signos y t**, no niveles.

### A. Dentro de la muestra de PV (1985-2010): reproduce

| Prueba | PV | Réplica (PU tres comp.) |
|---|---|---|
| T2 PU sobre CFI, esp. 1 | −0.31 (t −7.24) | −0.20 (t −7.16) |
| T2 PU sobre −DEF, esp. 1 | −0.75 (t −8.61) | −0.40 (t −7.58) |
| T2, 8 especificaciones (sin P/E) | 8/8 negativas, 7 con \|t\| > 1.96 | 8/8 negativas, 6 con \|t\| > 1.96 |
| T3 RV sobre PU, esp. 1 / esp. 2 | t 4.81 / 3.45 | t 3.30 / 2.48 |
| T3 VIX sobre PU, esp. 1 / esp. 2 | t 5.27 / 2.53 | t 4.47 / 1.93 |
| T4 vol sobre PU·E (16 especificaciones, sin P/E) | 16/16 negativas, 14 significativas | **16/16 negativas, 12 significativas** |
| T5 h = 12, PU·CFI | −0.09 (t −2.41) | −0.16 (t −2.29) |

**Segunda lectura:** la pendiente T3 (VIX) recalculada por cov/var da 0.1513, igual que la matricial. La RV de oct-2008 recalculada a mano da 0.7995, igual que la de la función.

### B. Fuera de muestra (2011-01 a 2026-09, 189 meses): se rompe una parte

| Predicción | Dentro | **Fuera** | Veredicto |
|---|---|---|---|
| (1) PU mayor con economía débil (T2) | CFI t −7.16; −DEF t −7.58; IPG t −4.11 | CFI **t −0.32**; −DEF **t −0.29**; IPG **t −0.14** | **No sobrevive.** Solo queda la recesión del COVID (−REC t −15.5, pero son **2 meses** de recesión, así que es degenerada) |
| (2) más PU → más vol (T3) | RV t 3.30; VIX t 4.47 | RV **t 3.47**; VIX **t 4.38**; con rezago 2.65 y 2.51 | **Sobrevive**, con la mitad de la pendiente |
| (2) robustez fuera | — | Con tendencia lineal: RV t 3.63, VIX t 4.56. Quitando la media de cada año: RV t 5.19, VIX t 5.29 | **Sólida** |
| (5) efecto mayor con economía débil (T4) | 16/16 negativas, 12 significativas | **12/12 negativas, 6 significativas** (sin −REC) | Sobrevive el signo; la fuerza baja a la mitad |
| (4) prima condicional (T5) | 2 de 4 significativas a h = 12 | CFI +0.016 (t +0.92), IPG t −0.93, −DEF t −2.30 | **No se sostiene** (solo −DEF) |

Con el índice de noticias pasa lo mismo: T3 fuera de muestra, RV t 2.98 y VIX t 3.53; T2, CFI t −0.62 y −DEF t +0.39.

### C. BTC (2014-10 a 2026-09, 144 meses; DVOL desde 2021-04, 66 meses)

| Variable sobre PU (tres comp.) | Esp. 1 | Esp. 2 (con rezago) | Robustez |
|---|---|---|---|
| Vol realizada de BTC | −0.027 (t −0.53) | −0.020 (t −0.51) | Con tendencia: t +0.84. **Intra-año: +0.111 (t +2.47)** |
| DVOL | −0.077 (t −2.15) | −0.013 (t −1.67) | 66 meses, todos en el régimen de vol cripto decreciente |
| Correlación BTC–S&P (diaria, en el mes) | **+0.165 (t +4.04)** | +0.107 (t +2.95) | **Con tendencia: t +1.39. Intra-año: t +0.46.** 2014-2019: −0.08 (t −0.78). 2020-2026: +0.06 (t +1.25). 2022-2026: +0.07 (t +1.29) |
| Control: vol del S&P, misma ventana | +0.066 (t +2.96) | +0.045 (t +2.25) | — |
| Interacción PU·CFI (vol BTC / correlación) | −0.042 (t −1.24) / −0.035 (t −1.12) | — | — |

- **La correlación BTC–S&P "explicada" por la PU es un espejismo de régimen.** La PU y la correlación subieron las dos después de 2020: la correlación por la entrada institucional y la PU por el COVID, los aranceles y 2025-2026. Al controlar la tendencia, o al comparar meses dentro del mismo año, el efecto desaparece (t 1.39 y 0.46). En cada submuestra no es significativo.
- **La vol de BTC no responde a la PU en el agregado.** Dentro de cada año hay una señal positiva (+11 pts de vol por cada +100 puntos del índice, t 2.47), pero sobre una media de 60 pts es pequeña y no aparece en las otras especificaciones. Se toma como indicio, no como hecho.
- **Hoy:** el índice de tres componentes de sep-2026 está en **175.2 (percentil 90 desde 1985)** y el de noticias en **218.9 (p91)**. Venía de 247.6 (p97) en mayo. El CFNAI de sep-2026 es +0.07 (economía normal).

## 4. Qué cambia para invertir [I/O]

- **Regla de lectura para el S&P (sólida dentro y fuera de muestra):** con la PU alta, se espera más vol en las acciones de EUA. En 2014-2026, +1σ de PU (63 puntos) equivale a **+4.2 pts de vol realizada del S&P** sobre una media de 14.7. Le toca a la supervisión del UPRO (3x), donde la vol erosiona por decaimiento, no a cripto.
- **Para BTC: la PU de EUA no es una variable útil.** No mueve su volatilidad de forma robusta, y el aparente "BTC se correlaciona más con las acciones cuando hay incertidumbre política" no sobrevive al control de régimen. **No se agrega ninguna regla a la cuenta cripto.** El filtro de tendencia sigue siendo la única regla de salida (colchón +14.6% hoy).
- **La pieza del modelo que no sobrevive** es justamente la que conecta la política con el ciclo: en 2011-2026 la PU dejó de subir con la economía débil, salvo en el COVID. Los picos de 2016-2019 y 2025 fueron de política pura (elecciones, aranceles, techo de deuda) con la economía normal. **Contrapunto para KPV:** su efecto "mayor con economía débil" quizá pese menos hoy.
- **Pronóstico P0202**, vinculado a la ficha del 26-oct (VRP): ¿la vol realizada de BTC en los próximos 30 días queda por debajo del DVOL de hoy (36.63)? **p = 0.62.** Tasa base 0.69 (2022-2025) y 0.61 en 2026. La ventana incluye la elección y el vencimiento de US$11 mil millones del 30-oct.

## 5. Contrapuntos y límites

- **Añada de los datos.** El índice BBD se revisó después de 2011, y el CFNAI y el INDPRO se revisan siempre. Las réplicas "dentro de muestra" no son de tiempo real. Las t se parecen a las de PV, pero los coeficientes difieren en escala.
- **Faltan piezas.** Sin P/E y sin correlación entre acciones (no hay componentes gratis). −DEF usa BAA − AAA. La tabla 5 usa el rendimiento de precio y no el exceso con dividendos.
- **−REC fuera de muestra es degenerada** (2 meses de recesión). Sus t de −15 a −301 se excluyen de los conteos.
- **BTC:** la correlación diaria es **asíncrona**. Yahoo cierra BTC a las 00:00 UTC y el S&P a las 20:00-21:00 UTC, lo que sesga la correlación a la baja, pero igual en todos los meses. 144 meses con dos regímenes muy distintos. **El DVOL solo tiene 66 meses.**
- **Causalidad:** ni PV ni esta réplica la establecen. El índice BBD mezcla la incertidumbre económica con la política, como advierten los autores.

## 6. Autoexamen

1. ¿Por qué el signo de la prima de riesgo sin condicionar es ambiguo en PV? (La PU sube la prima, pero el put implícito del gobierno, más valioso en malos tiempos, la baja; los dos operan en los mismos estados.)
2. ¿Qué predicción de PV sobrevive mejor fuera de muestra y cuál no? (Sobrevive "más PU → más vol del S&P": t 3.5-5.3 con tendencia e intra-año. No sobrevive "PU mayor con economía débil": CFI t −0.32 en 2011-2026.)
3. ¿Por qué la regresión de la correlación BTC–S&P sobre la PU da t 4.04 y no significa nada? (Las dos series tienen tendencia al alza por causas distintas después de 2020; con tendencia o intra-año, t 1.39 y 0.46, y en cada submuestra no es significativa.)
4. ¿Por qué se excluye −REC fuera de muestra? (Solo hay 2 meses de recesión, mar-abr 2020; la regresión depende de 2 puntos y la t es degenerada.)

## 7. Estado

- **Documentado con comprobación** (Doctorado: literatura académica, incertidumbre política y riesgo). Sección amplia del WP de abr-2013 (A). Réplica propia de las tablas 2-5 (sin P/E ni correlaciones) dentro y fuera de muestra, con dos índices, robustez de tendencia e intra-año, y segunda lectura. Extensión a BTC con 144 meses.
- **Hallazgo:** fuera de muestra (2011-2026) **sobrevive "más incertidumbre política → más volatilidad del S&P"** (t 3.5-5.3) y **muere "más incertidumbre con economía débil"** (CFI t −0.32). En BTC, la PU no mueve la volatilidad de forma robusta, y su aparente relación con la correlación BTC–S&P (t 4.04) es un artefacto del cambio de régimen de 2020 (t 0.46 intra-año).
- **Siguiente prueba:**
  1. resolver P0202 (28-nov), P0196 (5-nov) y P0190 (4-nov);
  2. completar el IVD de 2026 con la ventana *c* (~2-dic);
  3. leer la versión publicada en JFE si hay copia legal (posibles cambios en las tablas);
  4. índice diario de BBD (`USEPUINDXD`) contra los rendimientos diarios de BTC alrededor de los anuncios de aranceles de 2025, como estudio de eventos.
