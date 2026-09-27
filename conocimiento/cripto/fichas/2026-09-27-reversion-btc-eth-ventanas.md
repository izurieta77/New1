# Ficha de avance · 27-sep-2026 · G1 Bitcoin (pendiente: Dinero Roto caps. 9-30 + ampliar reversión a 10/60 días y a ETH)

> Corrida de las 08:17 CDMX (14:18:04 UTC), `analista-cripto`. Continúa el pendiente de `conocimiento/estado-de-dominio.csv`, fila `cripto/01`, dejado abierto el 26-sep-2026 en [fichas/2026-09-26-reversion-6-confirmaciones.md](2026-09-26-reversion-6-confirmaciones.md).

## 1. Intento breve de acceso a Dinero Roto caps. 9-30 (un solo intento, como pide la instrucción)

**Resultado: sin cambio. Sigue sin haber vía legal gratuita.** Una búsqueda web hoy (27-sep) sobre "capítulo 9 leer gratis" solo devolvió las mismas vías ya descartadas el 25 y 26-sep: la prueba de pago de Everand (30 días, pide método de pago), Kobo, Amazon y demás tiendas del ebook. Ninguna fuente nueva. **No insisto más esta semana**: el pendiente de lectura íntegra de los caps. 9-30 depende de que el dueño compre el ebook (~€5), como ya declaraban las fichas 28 y del 26-sep.

## 2. Ejercicio propio ampliado: reversión con ventanas de 10/60/90 días, en BTC y ahora también en ETH

### 2.1 Metodología (igual que el 26-sep, con dos extensiones declaradas antes de correr el análisis)

- **Datos:** klines diarios de `BTCUSDT` y, por primera vez, `ETHUSDT`, de `data-api.binance.vision`, interval=1d, desde el listado del par (2017-08-17 para ambos) hasta el 2026-09-26 (se excluye la vela del 27-sep, aún abierta). 3,328 velas por símbolo.
- **Evento de caída, agrupación en episodios y trough:** idéntico al 26-sep-2026 (drawdown ≥20% desde el máximo de cierre acumulado; se agrupan días con brechas ≤5 y se busca el mínimo real con una ventana de +10 días).
- **Extensión 1 — más horizontes de "reversión confirmada":** además de los 90 días ya usados, se agregan **10 días** y **60 días**: ¿el precio recupera al menos el 50% de la caída del episodio dentro de esa ventana desde el trough?
- **Extensión 2 — mismo cálculo en ETHUSDT**, con la misma definición de episodio, las mismas 6 señales técnicas (RSI, SMA20, SMA50, MACD, volumen, ruptura de 10 días) y los mismos tres horizontes.
- **Recomputo independiente del código:** el script de la ficha del 26-sep vivía en el scratchpad de esa sesión (fuera del repo) y no persiste entre sesiones. Hoy se reescribió desde cero con la misma metodología declarada. Esto es relevante para el punto 2.3 (limitación).
- **Límites declarados antes de ver el resultado:** los mismos del 26-sep (n pequeño, un puñado de activos, umbrales propios, sin control de régimen macro), más uno nuevo: las convenciones exactas de suavizado de RSI (Wilder vs. promedio simple) y de la semilla del EMA del MACD pueden mover en ±1 día el momento en que una señal técnica se marca "verdadera", lo que puede cambiar qué episodios caen en el grupo "6 de 6 confirmadas". Se documenta como hallazgo, no solo como limitación (ver 2.3).

### 2.2 Resultado — BTCUSDT (17 episodios, 2017-08-17 a 2026-09-26)

| Horizonte | Recuperan 50% de la caída | Tasa |
|---|---|---|
| 10 días | 6 / 17 | **35.3%** |
| 60 días | 13 / 17 | **76.5%** |
| 90 días | 13 / 17 | **76.5%** |

- **Hallazgo nuevo:** la tasa de 60 días es **idéntica** a la de 90 días (13/17 en ambas). Ningún episodio adicional recuperó el 50% entre el día 60 y el día 90. Es decir, si un episodio de BTC va a recuperar la mitad de su caída en 90 días, casi siempre ya lo hizo para el día 60 — el margen de 90 días no agrega casos nuevos en esta muestra.
- La ventana de 10 días es mucho menos confiable (35.3%): recuperar la mitad de una caída ≥20% en solo 10 días es la excepción, no la regla, incluso cuando eventualmente sí se recupera en 60-90 días.
- **Con 6/6 señales dentro de 30 días del trough:** esta corrida encontró **2 de 17** episodios (ago-2024 y sep-2024), no 3 como el 26-sep (que incluía jul-2021). En jul-2021, hoy el máximo de señales simultáneas fue 5/6, no 6/6. La diferencia es consistente con el punto declarado en 2.1: pequeños cambios de convención de suavizado mueven el resultado de un caso límite. **Esto refuerza, no debilita, la conclusión del 26-sep: la regla de "6/6" es fragil y sensible a decisiones de implementación menores, además de tener n minúsculo.**
  - 10 días: confirmados 0/2 (0%) vs. no confirmados 6/15 (40.0%). Fisher p=0.51.
  - 60 y 90 días: confirmados 2/2 (100%) vs. no confirmados 11/15 (73.3%). Fisher p=1.00 en ambos.
- **Sensibilidad ≥5/6 señales** (14 episodios cumplen, 3 no): a 90 días, 12/14 (85.7%) vs. 1/3 (33.3%), p=0.121 — coincide con el resultado del 26-sep (85.7% vs. 33.3%), lo que da algo de confianza en que el recomputo es correcto pese a la diferencia en el caso 6/6 estricto.

### 2.3 Resultado — ETHUSDT (15 episodios, 2017-08-17 a 2026-09-26; primera vez que se corre este ejercicio en ETH)

| Horizonte | Recuperan 50% de la caída | Tasa |
|---|---|---|
| 10 días | 3 / 15 | **20.0%** |
| 60 días | 7 / 15 | **46.7%** |
| 90 días | 8 / 15 | **53.3%** |

- **Hallazgo principal: ETH revierte sistemáticamente menos que BTC en los tres horizontes** (20.0/46.7/53.3% contra 35.3/76.5/76.5% de BTC). La brecha más grande es en 90 días: 53.3% vs. 76.5%, 23 puntos porcentuales. **Grado B** para el cálculo (reproducible, cubre todo el historial de ETHUSDT en Binance), pero con la salvedad de que son solo 15 episodios y algunos comparten el mismo pico de referencia (p. ej., 4 episodios distintos cuelgan del máximo de nov-2021), por lo que no son 15 observaciones independientes.
- A diferencia de BTC, en ETH la tasa de 90 días (53.3%) sí es mayor que la de 60 días (46.7%): hubo un episodio (trough sep-2024, colgado del pico de nov-2021) que recuperó el 50% entre el día 60 y el 90. En BTC no ocurrió ningún caso así.
- **Con 6/6 señales:** solo **1 de 15** episodios en ETH las juntó (feb-2021), y sí revirtió en los tres horizontes. Con n=1 no hay ninguna base para generalizar (Fisher p entre 0.20 y 1.00 según el horizonte, sin poder).
- **Sensibilidad ≥5/6:** 12 de 15 cumplen; a 90 días, 8/12 (66.7%) vs. 0/3 (0%) en los que no llegan a 5/6, p=0.077 (el más cercano a significativo de todo el ejercicio, pero con un grupo de comparación de solo 3 episodios).

### 2.4 El episodio en curso (BTC) y por qué importa para mañana

El episodio con trough el 30-jun-2026 (58,624.71, −53.0% desde el máximo de 124,658.54 del 6-oct-2025) **no había recuperado el 50% de su caída (≈91,641.63) en ninguno de los tres horizontes** al cierre del 26-sep-2026 (BTC cerró en 84,433.10, un 7.9% por debajo del umbral de 50%). El horizonte de 90 días de este episodio se cumple **mañana, 28-sep-2026** — el mismo día que se evalúa O0003. Con el precio de hoy (~84,900-85,000), este episodio terminará su ventana de 90 días sin haber revertido el 50%, uniéndose a 2018 y 2022 como los tres únicos de 17 episodios de BTC que no lo lograron. Esto es un dato de contexto, no cambia la regla operativa del filtro de tendencia (independiente de este ejercicio).

### 2.5 Lectura para invertir

- **[I, nuestra]** La ventana de 90 días sigue siendo razonable para BTC (no se gana nada extendiéndola más allá de 60 días en esta muestra), pero para ETH un horizonte de 90 días capta ~7 puntos porcentuales más que 60 días — si se quisiera fijar una regla de "esperar a la reversión", en ETH conviene dar más tiempo.
- **[I, nuestra]** La regla de "6/6 confirmaciones" sigue sin poder estadístico en ningún activo (n=2 en BTC, n=1 en ETH) y hoy se demostró además que es sensible a detalles de implementación menores (qué convención de RSI/EMA se use). **Grado C, sin cambio respecto al 26-sep, y con una razón adicional para desconfiar de una regla tan estricta.**
- **[I, nuestra]** La brecha BTC vs. ETH en tasa base de reversión (76.5% vs. 53.3% a 90 días) es el hallazgo más sólido de esta ficha (grado B, reproducible), y es coherente con la decisión ya tomada por el comité de no incluir ETH en la cuenta `arena-clache-binance` (aunque esa decisión se basó en otros argumentos, principalmente de gobernanza de cartera, no en este dato, que no existía todavía el 25-sep).
- Sigue sin cambiar la regla operativa: el filtro de tendencia de `arena-claude-binance` (SMA200 × 0.97/1.03) no usa estas señales; este ejercicio es de estudio.

Script y datos: `scratchpad/g1_reversion/{fetch_klines.py, reversion_multi.py, resultados_multi.json}` de esta sesión (fuera del repo, no persiste; si el dueño adopta el método, conviene moverlo a `herramientas/`).

## 3. Estado del pendiente de `cripto/01`

- **Ejercicio de reversión ampliado a 10/60 días y a ETHUSDT: hecho y documentado.** Cierra esta mitad del pendiente del 26-sep.
- **Lectura de Dinero Roto caps. 9-30: sigue pendiente**, sin vía legal gratuita (tercer intento sin éxito: 25, 26 y 27-sep). No se busca de nuevo hasta que el dueño decida comprar el ebook o hasta que haya una señal concreta de que apareció algo nuevo (por ejemplo, un anuncio del lector oficial).
- **Nuevo pendiente para `estado-de-dominio.csv`:** dado que el ejercicio cuantitativo de G1 quedó razonablemente cerrado con esta ampliación, el siguiente paso de bajo nivel que no depende de una compra es leer a detalle los capítulos 2, 3 y 8 (MuSig2/FROST) de *Mastering Bitcoin* (recurso 16, ya con acceso íntegro de 10 de 14 capítulos), pendiente listado desde el 25-sep en la sección 7 del capítulo de síntesis y todavía sin tocar. La compra de Dinero Roto queda como pendiente paralelo, a cargo del dueño.
