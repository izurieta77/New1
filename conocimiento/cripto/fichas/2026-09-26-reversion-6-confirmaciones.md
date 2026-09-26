# Ficha de avance · 26-sep-2026 · G1 Bitcoin (pendiente: Dinero Roto caps. 9-30 + ejercicio de reversión con 6 confirmaciones)

> Corrida de las 08:17 CDMX (14:17:42 UTC), `analista-cripto`. Cierra el pendiente de menor nivel sin terminar registrado en `conocimiento/estado-de-dominio.csv`, fila `cripto/01`.

## 1. Intento de acceso legal a Dinero Roto, caps. 9-30 (parte 1 del pendiente)

**Resultado: sigue sin haber acceso legal gratuito. No leí los caps. 9-30. No invento ni afirmo una lectura que no ocurrió.**

Vías revisadas hoy, todas de pago o sin cambio respecto al 25-sep-2026:

| Vía | Resultado |
|---|---|
| Lector oficial `dineroroto.com` (Konsensus) | Intenté acceder directamente a una URL de capítulo 9 (`/capitulo-9`); redirige a la portada/índice, igual que el 25-sep. **No hay capítulos nuevos liberados.** |
| Swan (`swanbitcoin.com/broken-money-chapter-8`) | Confirmado hoy vía WebFetch: la página dice explícitamente "Swan Bitcoin has made **Chapter 7 and 8** available for free download". Sin cambio. |
| Everand/Scribd | Aparece un "leer gratis 30 días", pero es una **prueba de suscripción de pago** (pide método de pago, se cobra si no se cancela). No lo cuento como acceso legal gratuito equivalente a lo ya usado (transcripciones públicas de podcasts, reseñas). |
| Kobo, Barnes & Noble, Amazon, Apple Books | Solo venta del ebook/audiolibro. Sin cambio. |
| Búsqueda de una entrevista o reseña nueva (2026) que cubra específicamente los caps. 9-30 | No encontré ninguna entrevista o reseña posterior a las ya citadas en la ficha 28 (MacroVoices, The Investor's Podcast, Stephan Livera SLP518, reseña "Conflated"). |

**Conclusión:** el pendiente de lectura íntegra de los caps. 9-30 **sigue abierto** y depende de que el dueño compre el ebook (€5), como ya declaraba la ficha 28. No se avanzó esta parte hoy más allá de descartar vías nuevas.

## 2. Ejercicio propio: reversión a la media de BTC con 6 confirmaciones (parte 2 del pendiente, independiente del libro)

### 2.1 Metodología (declarada antes de correr el análisis)

- **Datos:** klines diarios de `BTCUSDT`, `data-api.binance.vision`, interval=1d, del 2017-08-17 (listado del par) al 2026-09-25 (excluyo la vela del 26-sep, aún abierta). 3,327 velas cerradas.
- **Evento de caída:** día *t* con cierre ≤ 80% de su máximo de cierre acumulado (drawdown ≥ 20% desde el máximo). Días de caída con brechas ≤ 5 días se agrupan en **episodios**; el **trough** (mínimo) de cada episodio es el cierre más bajo dentro de él (con una ventana de +10 días para no cortar el mínimo real).
- **6 señales de confirmación técnica**, evaluadas el mismo día, buscadas en los 30 días siguientes al trough:
  1. RSI(14) cruzó de <30 a ≥30 en los 5 días previos (sobreventa ya liberada);
  2. cierre > SMA20;
  3. cierre > SMA50;
  4. línea MACD(12,26) > línea de señal(9);
  5. volumen del día > promedio de volumen de los 20 días previos;
  6. el cierre de hoy es el más alto de los últimos 10 días (ruptura de estructura).
- **"Reversión confirmada":** dentro de los 90 días siguientes al trough, el precio recupera al menos el 50% de la caída del episodio (mide desde el trough hacia el pico previo).
- **Comparación (no es un experimento aleatorizado):** tasa de recuperación en episodios donde **nunca** se juntan las 6 señales en la ventana de 30 días, como referencia de "qué pasa sin filtro".
- **Límites declarados antes de ver el resultado:** n pequeño (cripto solo desde 2017), un solo activo, los umbrales (20% de caída, ventanas de 30/90 días, 50% de recuperación) son decisión propia, no de un paper, y no hay control por régimen macro.

### 2.2 Resultado

- **17 episodios** de caída ≥20% desde 2017-08-17 al 2026-09-25 (incluye el episodio en curso, con trough el 30-jun-2026 en 58,624.71, −53.0% desde el máximo de 124,658.54 del 6-oct-2025; a hoy 25-sep sigue sin recuperar el 50% de esa caída, consistente con el −32.8% que reporta el capítulo de síntesis).
- **Con las 6 señales dentro de 30 días del trough: 3 de 17 episodios** (jul-2021, y dos en ago-sep-2024). **Los 3 (100%) recuperaron** el 50% de la caída en 90 días.
- **Sin las 6 señales dentro de 30 días: 14 episodios.** De esos, **10 (71.4%)** igual recuperaron el 50% en 90 días, solo por el paso del tiempo.
- **Prueba de Fisher exacta (6/6 vs. resto): p = 0.54.** Con n=3 en el grupo "confirmado", la diferencia entre 100% y 71.4% **no es distinguible de ruido**.
- **Sensibilidad (≥5 de 6 señales en vez de 6 de 6):** 14 episodios cumplen, de los cuales 12 (85.7%) recuperan; de los 3 que no cumplen ni 5 de 6, solo 1 (33.3%) recupera. La brecha se agranda al relajar el umbral, pero los grupos siguen siendo chicos (n=14 vs. n=3).
- **Tiempo medio trough → confirmación de 6 señales:** 14 días (mediana 7, con outlier de 29 días en ago-2024).

Script y datos: `scratchpad/g1_reversion/{fetch_klines.py, reversion_6conf.py, resultados.json}` (fuera del repo; si el dueño lo adopta, pasar a `herramientas/`).

### 2.3 Lectura para invertir

- **[I, nuestra] Con la definición estricta de 6/6 señales, el ejercicio no tiene poder estadístico** (n=3): no se puede afirmar que "6 confirmaciones" mejoren la tasa base de reversión frente a simplemente esperar 90 días desde un trough de −20% (71.4% de tasa base ya es alta).
- **[I, nuestra] La tasa base de recuperación del 50% de una caída ≥20% en 90 días es alta (13/17 = 76.5%, sin condicionar en nada)**, lo que es consistente con lo que ya decía la ficha 01 sobre BTC como activo con reversiones fuertes, pero **no dice nada sobre el momento exacto ni protege del episodio en curso** (−53% desde oct-2025, el peor de la muestra junto con 2018 y 2022, y el único además de esos dos que a 90 días de su trough **no** había recuperado el 50%).
- **Grado C** para el hallazgo de "6/6 confirmaciones ayudan": muestra demasiado corta para afirmar una ventaja. **Grado B** para la tasa base de reversión de 76.5% en 90 días tras una caída de 20%+, porque el cálculo es reproducible y cubre todo el historial de BTCUSDT en Binance, aunque solo son 17 episodios.
- Relevancia para la cuenta `arena-claude-binance`: el filtro de tendencia de la cuenta (SMA200 × 0.97/1.03) **no usa estas 6 señales**; es una regla más simple y ya decidida por el comité. Este ejercicio es de estudio, no cambia la regla operativa.

### 2.4 Estado del pendiente de `cripto/01`

- **Ejercicio propio de reversión con 6 confirmaciones: hecho y documentado.** Cierra esa mitad del pendiente.
- **Lectura de Dinero Roto caps. 9-30: sigue pendiente**, sin vía legal gratuita disponible hoy. Se mantiene como pendiente explícito, condicionado a que el dueño compre el ebook.
- Nuevo pendiente propuesto para `estado-de-dominio.csv`: "Comprar o conseguir acceso legal a Dinero Roto caps. 9-30 (ebook, €5) y, aparte, ampliar el ejercicio de reversión con una segunda ventana de confirmación (10 o 60 días) y con ETH, para ver si el resultado de n=3 se sostiene con más casos."
