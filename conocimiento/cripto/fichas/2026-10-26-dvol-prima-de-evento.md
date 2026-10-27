# Ficha de avance · 26-oct-2026 · DVOL, prima de riesgo de volatilidad y prima de evento (FOMC) en opciones de BTC

> **Por qué este tema.** Es el siguiente punto de la cola de la literatura académica del plan (`00-plan-de-estudio.md`, fila "Literatura académica…": "microestructura de opciones (DVOL y prima de evento)") y el punto 2 de la §7 de la ficha del 25-oct. El pulso ya publica el DVOL; nunca se había medido si "DVOL alto o bajo" significa algo. Hay un evento real a 2 días: la decisión del FOMC del **miércoles 28-oct-2026** (calendario de la Fed: reunión 27-28 de octubre).

## 0. Preguntas de hoy

1. ¿El DVOL (volatilidad implícita a 30 días de Deribit) sobreestima la volatilidad realizada de los 30 días siguientes? ¿Cuánto, en qué régimen, y pronostica mejor que la realizada pasada?
2. ¿Cuánta varianza extra cotiza hoy la cadena de opciones para el día del FOMC y cuánta tuvo BTC, de verdad, en las 46 decisiones programadas de 2021-2026?
3. ¿Qué cambia para el filtro y el pulso?

## 1. Acceso y fuentes (declarado)

| Fuente | Grado | Acceso real |
|---|---|---|
| **Deribit, "DVOL – Deribit Implied Volatility Index"** ([Deribit Insights](https://insights.deribit.com/exchange-updates/dvol-deribit-implied-volatility-index/), 31-mar-2021, actualizado 20-mar-2023) | **A** (metodología del emisor del índice) | **Sección íntegra** de "Methodology" y "Crunching the numbers" (pasos 1-6) |
| **Deribit API pública**: `public/get_volatility_index_data` (DVOL BTC diario, 24-mar-2021 a 26-oct-2026) y `public/get_book_summary_by_currency?currency=BTC&kind=option` (cadena, `mark_iv`, foto 26-oct 14:39 UTC) | **A** (dato del mercado) | Íntegro; foto guardada en `2026-10-26-dvol-prima-de-evento-datos.json` |
| **Binance** `data-api.binance.vision` klines BTCUSDT 1d y 8h, 2021-2026 | **A** | Íntegro |
| **Fed**, [calendario del FOMC](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) 2021-2027 | **A** | Íntegro (fechas de decisión) |
| **Alexander e Imeraj**, "The Bitcoin VIX and its Variance Risk Premium", *Journal of Alternative Investments* 23(4), 2021, pp. 84-109 ([repositorio Sussex](https://sro.sussex.ac.uk/id/eprint/91094/)) | **B** (revista arbitrada; dato de Deribit 2019-2020) | **Resumen** (fragmentos del buscador; figshare da 403). No leí el texto |
| **Almeida, Grith, Miftachov y Wang**, "Risk Premia in the Bitcoin Market", [arXiv 2410.15195](https://arxiv.org/abs/2410.15195) v2 (1-ago-2025) | **B** (preprint) | **Resumen** |

**No leído (no se cita como evidencia):** Bollerslev-Tauchen-Zhou (RFS 2009) sobre VRP en acciones y Dubinsky-Johannes-Kaeck-Seeger (RFS 2019) sobre prima de anuncios; solo los nombro como marco.

## 2. Lo que dicen las fuentes [H]

- **Metodología DVOL (A):** toma los 2 vencimientos más cercanos a 30 días, a cada lado; precio por profundidad del libro (VWAP hasta 2 BTC); descarta ITM y OTM con delta < 5%; **"use the variance swap methodology"** para cada vencimiento, interpola y saca raíz; filtra ruido. Es la fórmula del VIX. Regla práctica de Deribit: movimiento diario esperado = DVOL / √365. Como es una **varianza** (swap), incluye la sonrisa: no es la IV ATM.
- **Alexander-Imeraj (B, resumen):** construyen un "VIX de bitcoin" con >7 millones de precios de Deribit (mar-2019 a mar-2020), plazos de 1 semana a 3 meses, con la fórmula de variance swap, y comparan su VRP con acciones, petróleo, oro, EUR/USD y el bono a 10 años. Un artículo derivado de Alexander dice que en BTC la VRP **puede ser muy grande cuando es negativa** (la realizada supera a la implícita en los saltos).
- **Almeida et al. (B, resumen):** BTC tiene una VRP **mayor que la del S&P 500**; hay dos regímenes de volatilidad y la VRP es **alta en el régimen de baja volatilidad** y más baja en el de alta.

## 3. Ejercicio numérico (comprobado en Python)

Código: [`2026-10-26-dvol-prima-de-evento.py`](2026-10-26-dvol-prima-de-evento.py); datos: [`2026-10-26-dvol-prima-de-evento-datos.json`](2026-10-26-dvol-prima-de-evento-datos.json). Se reproduce con `python3 -I conocimiento/cripto/fichas/2026-10-26-dvol-prima-de-evento.py` (y `… descargar` para bajar una foto nueva). Volatilidad realizada = √(365/30 · Σ r²) con r logarítmico diario, sin restar la media (convención de variance swap).

### A. DVOL contra la realizada de los 30 días siguientes (2,012 días, 24-mar-2021 a 25-sep-2026)

| Medida | Valor |
|---|---|
| DVOL medio / realizada futura media | 59.86 / 51.50 |
| **VRP media (puntos de vol)** | **+8.36** (mediana +10.11); DVOL > realizada en 71.6% de los días |
| Sin traslape (cada 30 días, n = 68) | +10.19, e.e. 2.26, **t = 4.51**, 75% positivos |
| Mincer-Zarnowitz, DVOL | RV = 15.01 + 0.61·DVOL, **R² 0.37** (RMSE 18.7 pts) |
| Mincer-Zarnowitz, RV pasada 30 d | RV = 30.32 + 0.41·RV, R² 0.17 (RMSE 20.5 pts) |

**Por año:** 2021 +17.9 (88% positivos), 2022 +12.3, 2023 +6.5, 2024 +7.0, 2025 +6.6, **2026 −0.27 (60%)**. La prima se encogió a la mitad tras 2022 y **en 2026 desapareció en promedio**.

**Por régimen de la realizada pasada** (condicionar en el DVOL mete un sesgo mecánico; aquí se condiciona en lo ya observado):

| RV pasada 30 d | n | DVOL medio | RV futura media | VRP | DVOL²/RV² |
|---|---|---|---|---|---|
| < 35 | 391 | 41.39 | **44.62** | **−3.23** | 0.78 |
| 35-50 | 703 | 51.40 | 44.76 | +6.64 | 1.21 |
| 50-70 | 592 | 68.78 | 57.65 | +11.13 | 1.36 |
| ≥ 70 | 326 | 84.05 | 63.09 | +20.95 | 1.67 |

**Hoy:** vol30 realizada 24.83% (filtro) y DVOL 38.50 (vela del 26-oct). Estamos en la fila de arriba: **cuando BTC viene en calma, la volatilidad de los 30 días siguientes promedió 44.6, más que el DVOL**. La calma de BTC no dura; las opciones la cobran de menos, no de más.

### B. Prima de evento: decisión del FOMC

**B1, histórico (ventana 08:00→08:00 UTC, la misma de los vencimientos diarios de Deribit; Binance 8h; 46 decisiones contra 1,470 días hábiles sin FOMC):**

- σ diaria en el FOMC **2.69%** contra 3.11% del resto: **razón de varianzas 0.75** (IC 95% bootstrap 0.47-1.11). Contra los 20 días hábiles previos de cada decisión: media 0.79, mediana 0.47.
- |r| mediano 1.99% contra 1.51%: el FOMC da **movimientos medianos algo mayores pero menos colas**. P(|r| > 2%) 50% contra 40%; P(|r| > 3%) 24% contra 25%; P(|r| > 4%) 13% contra 16%.
- |r| medio en FOMC por año: 2021 2.06%, 2022 2.70%, 2023 2.18%, 2024 2.37%, 2025 1.66%, 2026 1.75%.

**B2, implícito (cadena de Deribit, 26-oct 14:39 UTC; IV ATM interpolada en el forward):**

| Vencimiento (08:00 UTC) | IV ATM | Tramo | Vol a plazo | σ del tramo |
|---|---|---|---|---|
| mar 27-oct | 36.16 | hoy→27 | — | — |
| mié 28-oct | 34.10 | 27→28 | 32.54 | 1.70% |
| **jue 29-oct** | 36.23 | **28→29 (FOMC 18:00 UTC)** | **39.64** | **2.07%** |
| vie 30-oct | 35.64 | 29→30 (PIB EUA, BCE) | 33.96 | 1.78% |
| vie 6-nov | 38.49 | 30-oct→6-nov (elección de EUA 3-nov) | 39.92 | 5.53% en 7 d |

- *Precisión (27-oct-2026, decisiones-pendientes del 27-oct 02:30 UTC):* el "tramo FOMC" es el **28→29-oct** (vencimientos de 08:00 UTC) porque es el que **contiene la decisión del miércoles 28-oct a las 18:00 UTC**; la reunión es el 27–28 de octubre (federalreserve.gov), no el 28–29.
- **Razón implícita del tramo FOMC: 1.48** contra la base limpia 27→28 (1.42 con base 27→28 + 29→30). Varianza extra = salto de evento 1σ de **~1.13-1.18%**.
- **La historia dice 0.75 (IC 0.47-1.11); el mercado cobra 1.48.** El cociente implícito queda fuera del intervalo histórico: **la prima de evento del FOMC en BTC está cara frente a lo que el FOMC ha movido a BTC desde 2021.**
- Escala de régimen: σ realizada de los últimos 20 días hábiles = 1.36%; con la razón histórica, el día FOMC "debería" valer ~1.18%, no 2.07%.

**B3, probabilidad de que el movimiento 28→29-oct supere la σ implícita (2.07%):**

| Escala histórica | Umbral | FOMC | Resto |
|---|---|---|---|
| σ realizada de 20 d previos | 1.53 σ | **11%** (n = 45) | 13% |
| DVOL del día previo | 1.03 σ | **18%** (n = 44) | 21% |
| Normal con la σ implícita | 1.00 σ | 32% | — |

Con DVOL como escala, la varianza realizada fue 0.67 de la implícita en los FOMC y 0.88 en el resto (la VRP de A, vista día a día).

## 4. Qué cambia para invertir [I/O]

- **El DVOL bajo no es señal de "vol barata para vender".** Con la realizada en calma (hoy 24.8), la historia da VRP **negativa** (−3.2 pts): la volatilidad tiende a despertar. Para el filtro: llegar a la salida (70,798) desde 79,730 pide una caída de 11.2% (ln 0.119). Con el DVOL (38.5/√12 = 11.1% al mes) eso es **~1.1 σ mensual**; con la vol30 realizada (7.2% al mes) parecían ~1.7 σ. El colchón es real, pero **más delgado de lo que sugiere la vol30**.
- **El FOMC del 28-oct no es, por historia, un día de cola para BTC.** La cadena cobra 1.48× la varianza diaria; BTC dio 0.75×. Ninguna acción: la cuenta es spot y no vende opciones (`cripto_binance` prohíbe opciones). La lectura sirve para **no sobrerreaccionar** al titular de la Fed y para calibrar el pronóstico P0184.
- **Tramo 30-oct→6-nov:** la vol a plazo sube a 39.9 con la elección intermedia de EUA (3-nov) dentro. Es la siguiente prueba del mismo método.
- **Para el pulso:** reportar DVOL **junto a** la vol30 realizada y su diferencia (VRP en vivo). Hoy: 38.5 − 24.8 = **+13.7 pts** contra la realizada pasada. Parece una prima grande, pero en la fila "RV < 35" la VRP contra la realizada *futura* fue negativa en promedio.

## 5. Contrapuntos y límites

- **Traslape y pocos episodios:** 2,012 días se reducen a 68 meses independientes; la fila "RV < 35" (391 días) son quizá 10-15 episodios de calma. El −3.2 tiene error grande.
- **ATM no es DVOL:** B2 usa IV ATM (mark de Deribit), no la fórmula de variance swap; el sesgo de la sonrisa en vencimientos de 1-3 días es pequeño pero no cero. El `mark_iv` es del modelo de Deribit, no un precio operado.
- **Base contaminada:** el 29→30 trae PIB de EUA y BCE; el 27→28 tiene la apertura de la reunión. Las dos bases dan 1.42-1.48; la conclusión no cambia.
- **El FOMC de hoy no es el promedio:** 2022 (alzas de 75 pb) y 2026 no son lo mismo. 46 eventos dan un IC de 0.47-1.11; con 1.48 fuera, la prima luce cara, pero un solo FOMC no la prueba ni la refuta.
- **Contradicción con Almeida et al.:** ellos hallan VRP **alta** en el régimen de baja volatilidad; yo hallo VRP en puntos de vol **negativa** cuando la realizada pasada es < 35. Pueden diferir la definición (varianza en riesgo neutral con densidad completa, régimen por modelo de cambio de régimen, periodo). Solo leí su resumen: queda abierto, no lo declaro refutado.
- **Deribit concentra ~90% de las opciones de BTC según la propia Deribit** (dato del emisor, C). Los ETF de opciones sobre IBIT no entran aquí.

## 6. Autoexamen

1. ¿Por qué el DVOL no es la IV ATM a 30 días? (Es la raíz de una varianza de swap: pondera toda la sonrisa OTM, como el VIX.)
2. ¿Cómo se aísla la varianza de un evento con vencimientos diarios? (Varianza total w = σ²T; la varianza a plazo del tramo que contiene el evento, menos la de un tramo base de igual duración.)
3. ¿Por qué condicionar la VRP en el DVOL exagera la prima? (Si el DVOL es alto por ruido, la VRP medida es alta por construcción; hay que condicionar en información pasada.)
4. Con DVOL 38.5, ¿cuál es el movimiento diario esperado de 1σ? (38.5/√365 ≈ 2.0%.)

## 7. Estado

- **Documentado con comprobación** (Doctorado: microestructura de opciones). Metodología DVOL en A; VRP y prima de evento medidas con datos propios (A); literatura en B (resumen).
- **Siguiente prueba:**
  1. resolver P0184 (FOMC 28→29-oct) y repetir B2 con la elección del 3-nov (tramo 2→3 o 3→4-nov);
  2. VRP con la fórmula de variance swap propia (no ATM) y con régimen por modelo, para cotejar con Almeida et al.;
  3. leer el texto de Alexander-Imeraj si aparece una copia legal.
