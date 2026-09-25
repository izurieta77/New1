# Teoría de torneos y estrategia competitiva para la arena (1 vs 1, 6 meses)

**Fecha de corte:** 2026-09-25
**Documento:** A3 de `arena/investigacion/`
**Alcance:** cómo maximizar la probabilidad de terminar arriba de un rival en rendimiento % (TWR en MXN) en una temporada de 6 meses que empieza en octubre de 2026. Cuenta `arena-claude` (20,000 MXN, GBM) contra `arena-grok` (15,000 MXN, GBM). El documento cubre la teoría de torneos, las matemáticas de Kelly frente a ganar un ranking, lo que dejaron Alpha Arena y el estilo documentado de Grok, la evidencia de cada estrategia candidata y un modelo cuantitativo de P(R_claude > R_rival).
**Modelo reproducible:** `arena/modelos/p_ganar_torneo.py` (solo stdlib). Salida completa en `arena/modelos/salida_p_ganar_torneo.txt`.

**Convención de etiquetas** (igual que en A1):
- **[H]** Hecho con fuente y fecha.
- **[I]** Inferencia mía a partir de hechos citados o del modelo.
- **[R]** Recomendación operativa para la cuenta arena.
- **(no verificado)**: el dato sale de fuentes secundarias o de resúmenes de búsqueda y no lo confirmé en una fuente primaria.

**Grados de evidencia (A–D)** para las estrategias:
- **A:** varios estudios revisados por pares, muestras largas, varios mercados, y el efecto sigue después de publicado.
- **B:** robusto en muestras largas, pero con decaimiento después de publicarse o dependiente del régimen.
- **C:** muestra pequeña, evidencia sobre todo de practicantes o resultados fuera de muestra débiles.
- **D:** desapareció después de publicarse o no se replica.

---

## Resumen ejecutivo

1. **[H] La teoría de torneos predice que quien va atrás apuesta más.** Brown-Harlow-Starks (1996) y Chevalier-Ellison (1997) lo encontraron en fondos mutuos [1][2]. Busse (2001) no lo encontró con datos diarios [3]. Taylor (2003) mostró que, en un juego estratégico, **el que va adelante también sube su riesgo para "cubrir" al rival** [5].
2. **[H] Browne (2000) resolvió el duelo entre dos inversionistas.** Si ninguno tiene ventaja, la estrategia de equilibrio es la de crecimiento óptimo (Kelly). El que está en desventaja debe ser más audaz. **Si los dos invierten en lo mismo, el juego es trivial: cada movimiento se puede copiar** [9].
3. **[I, modelo] En una carrera de beta pura, apalancarse más que el rival te da ~50%, no más.** Con k_claude > k_rival, P(ganar) = Φ(√T·(μ_e − (k_c + k_r)σ²/2)/σ). Esa probabilidad **no crece con la diferencia de exposición**: depende de que el mercado suba. Con μ_e = 8% y σ = 20%, sale entre 47% y 54%.
4. **[I, modelo] Lo que mueve la probabilidad es la razón de información (IR) de la diferencia, no el nivel de riesgo.** P ≈ Φ(IR·√0.5): IR 0.25 da 57%, IR 0.5 da 64% e IR 1.0 da 76%. Sin ventaja real, el techo realista contra un rival típico es de **55% a 60%**.
5. **[I, modelo] Estrategia según el marcador.** A mitad de temporada, con +5 pp de ventaja, P(ganar) = 98% si el tracking error contra el rival es de 5%, y baja a 71% si es de 20%. Con −5 pp, es 3% con TE de 5% y 40% con TE de 40%. **"Bajar varianza" cuando vas adelante significa bajar la varianza RELATIVA al rival, es decir, copiar su beta. Irse a efectivo no es bajar varianza.**
6. **[H] Alpha Arena, temporada 1 (cripto, 17/18-oct a 3-nov-2025).** Según la API de Nof1 al cierre (3-nov-2025, ~17:00 ET, copia archivada) [44]: Qwen3 Max +22.0%, DeepSeek +4.5%, Claude Sonnet 4.5 −31.1%, **Grok 4 −45.4% (4° lugar)**, Gemini 2.5 Pro −56.2% y GPT-5 −62.7%. *(Corregido el 25-sep-2026: decía Claude −42.01%, Grok 4 −57.92% (5°), Gemini −45.55% y GPT-5 −58.74%, cifras de ForkLog [12] que no aparecen en la serie de la API.)* **El 20-oct (~21:00 UTC) Grok 4 iba +30.5% y Claude +28.1%; Grok llegó a +50.4% el 21-oct** [13][44]: los líderes tempranos apalancados se derrumbaron.
7. **[H] Estilo documentado de Grok 4** (corridas previas al lanzamiento): es de los que más shortean, tiene los holdings más largos, opera menos que los demás y pone los stops más holgados [11]. En la temporada en vivo, 17 de sus 52 posiciones observadas fueron cortos y quedó a media tabla en número de posiciones (cálculo propio con capturas horarias de la API [44]). **Grok 4.20 ganó la temporada 1.5 (acciones de EUA) con +12.11% agregado** (otras fuentes: +9.3% a +10.6%) y ganó dinero en las cuatro modalidades [15][16][17]. Desde dic-2025 no ha habido temporadas públicas nuevas [19].
8. **[H] Estrategias candidatas.** Las de mejor evidencia son el momentum de series de tiempo (grado A) y la rotación apalancada con SMA200 (grado B; Sharpe de 0.51 contra 0.30 del buy & hold en 1928–2015 [27]). También tienen evidencia la estacionalidad nov–abr (grado B; +4.52% en 319 años [31]) y el efecto post-intermedias (grado C; ~+25% compuesto en el 4T de las intermedias más los dos trimestres siguientes, 1954–2017 [38]). **La temporada cae justo en esa ventana.** La deriva pre-FOMC ya desapareció (grado D) [35].
9. **[I, Monte Carlo] Contra una mezcla de rivales "tipo Grok"**, la probabilidad de ganar (primer valor: régimen A de estrés corto; segundo valor: régimen B bajista persistente) queda así:
   - tendencia + apalancado (2x, filtro SMA200 con banda de 3%): **54% / 57%**, con P(pérdida > 35%) de ~1%;
   - momentum concentrado: 53–58%, según el alfa que se suponga;
   - barbell: 53% / 54%, con ~0% de ruina;
   - la misma tendencia + apalancado con **modo torneo a mitad de temporada: 58% / 60%**;
   - el simple índice 1x sin filtro: 58% / 57%.

   El filtro compra cola, no probabilidad.
10. **[R] Plan base:** 1–2x efectivo sobre renta variable de EUA de gran capitalización, con filtro SMA200 + banda de 3% + VIX < 25 como seguro. A mitad de temporada entra el modo torneo: el 3x se reserva para cuando vayamos atrás ≥5 pp. La beta del rival se estima con sus reportes semanales. **El error que más cuesta es el sobretrading.** Un rival que rota cada semana sin ventaja pierde de 5% a 9% por comisiones en la temporada, y contra él ganamos del 67% al 88% de las veces.
    - **[I] Restricción del perfil (agregado el 25-sep-2026):** con `etf_apalancado_max` = 0.5, la exposición máxima es ~2x (50% en un 3x + 50% en un 1x). El "3x cuando vamos atrás" del modo torneo (C9–C11) y "copiar la beta de un rival 3x" **no caben en el perfil provisional**: hay que subir ese límite o rebajar el modo torneo. El Monte Carlo tampoco modela los cortacircuitos de −12/−20/−28% ni el filtro de VIX (sección 7).

---

## 1. Teoría de torneos: qué dice la evidencia en fondos

| Estudio | Muestra | Hallazgo | Tamaño / robustez | Lectura para la arena |
|---|---|---|---|---|
| Brown, Harlow y Starks (1996), *JF* 51:85–110 [1] | 334 fondos growth, 1976–1991 | Los perdedores de mitad de año suben la volatilidad del fondo en la segunda mitad más que los ganadores. El efecto crece con los años, a medida que los inversionistas ponen más atención al desempeño | Efecto significativo con datos mensuales (la magnitud exacta de la razón de volatilidades: no verificado) | [I] El rival que vaya atrás en el reporte de mitad de temporada tenderá a subir el riesgo |
| Chevalier y Ellison (1997), *JPE* 105(6):1167–1200 [2] | Fondos growth y growth & income, 1982–1992; carteras de septiembre y diciembre | La relación flujo-desempeño es convexa. Eso crea incentivos a cambiar el riesgo según el rendimiento acumulado del año, y **los fondos sí cambian su riesgo entre septiembre y diciembre** en esa dirección | Semiparamétrico. Resultado citado como canónico | [I] Lo que importa es la forma del premio: si solo cuenta ganar, el premio es binario y aumenta el incentivo a apostar |
| Busse (2001), *JFQA* 36(1):53–73 [3] | Fondos de acciones de EUA, **datos diarios** (tamaño de muestra y periodo: no verificados en el resumen) | Con datos diarios **no hay efecto torneo**. El resultado mensual venía de un sesgo por autocorrelación en la estimación de la volatilidad | Refutación metodológica | [I] Buena parte de lo que parecía "apuesta" era ruido de medición. No hay que sobrerreaccionar a la volatilidad aparente del rival con pocos datos |
| Taylor (2003), *JEBO* 50(3):373–383 [5] | Modelo teórico de 2 gestores con un activo riesgoso **perfectamente correlacionado** | Con benchmark exógeno, el que va perdiendo apuesta. En el juego estratégico solo hay equilibrio mixto, **y el líder elige la estrategia riesgosa más seguido que el rezagado** | Teórico | [I] Clave para la arena: si el rival va a apostar y tú vas adelante, **copiar su apuesta preserva tu ventaja**, igual que cuando el velero que va adelante "cubre" al de atrás |
| Kempf y Ruenzi (2008), *RFS* 21(2):1013–1036 [4] | Fondos de acciones de EUA dentro de familias | Los gestores ajustan el riesgo según su posición en la familia, y la dirección depende de la situación competitiva. **En familias grandes los perdedores suben más el riesgo que los ganadores; en familias chicas es al revés: los ganadores lo suben más (comportamiento estratégico)**. El efecto es mayor con comisiones altas, un solo gestor y familias grandes | Empírico | [I] El comportamiento depende del marcador y de cuántos rivales haya. Con pocos rivales (un 1 vs 1 es el caso extremo), la evidencia empírica apunta en la misma dirección que Taylor: **el que va adelante también sube el riesgo** |
| Seel y Strack (2013), *JET* 148(5):2033–2048 [6] | Modelo de n jugadores en un concurso donde el ganador se lo lleva todo, con movimiento browniano y quiebra en 0 | Equilibrio de Nash en forma cerrada: los jugadores "apuestan" (arriesgan más de lo que haría un maximizador de valor esperado) | Teórico | [I] En un duelo donde el ganador se lleva todo, lo racional es arriesgar más de lo que conviene para maximizar el patrimonio |
| Browne (1999), *Finance & Stochastics* 3:275–294 [7] | Control estocástico contra un benchmark estocástico | Encuentra la estrategia que maximiza la probabilidad de superar al benchmark por un % dado sin caer debajo de él por otro % | Teórico | [I] La herramienta formal para "ganarle a un objetivo que se mueve" |
| Browne (1999), "Reaching goals by a deadline", *Adv. Appl. Prob.* 31(2):551–577 [8] | Maximizar P(llegar a una meta en una fecha fija) | **La política óptima equivale a comprar una opción digital europea.** En general, el activo se sustituye por el portafolio de crecimiento óptimo | Teórico (datos de publicación verificados el 25-sep-2026) | [I] Replicar una digital deja el patrimonio en la meta o en ~0. Cerca de la fecha límite, la delta explota si vas atrás: "atrás, sube" llevado al extremo |
| Browne (2000), *J. Appl. Prob.* 37(1) [9] | Juego de suma cero entre 2 inversionistas con oportunidades correlacionadas y **revelación perfecta** (cada uno ve el patrimonio del otro en todo momento) | (a) Hace falta **correlación imperfecta**; con la misma oportunidad, "cualquier movimiento de A puede ser neutralizado por B". (b) En el caso simétrico, el equilibrio **se reduce a la estrategia de crecimiento óptimo** (Kelly). (c) **El jugador en desventaja sigue una estrategia más audaz**, del orden del cuadrado del parámetro de ventaja κ. Esto coincide con el "bold play" de Dubins-Savage | Teórico (verificado en el PDF) | [I] La ventaja la da el precio de mercado del riesgo, es decir, el Sharpe de cada quien. **Sin Sharpe superior, la única forma de ganar es ser distinto y tener suerte.** En la arena solo hay marcador semanal y nunca posiciones, así que cubrir o neutralizar al rival es aproximado |

**Síntesis [I]:**
- La literatura empírica de fondos sobre el efecto torneo es mixta: hay evidencia mensual y Busse la refuta con datos diarios [1][2][3].
- La teoría es consistente en tres puntos:
  - **quien está en desventaja debe subir su varianza relativa** [9];
  - **quien va adelante debe cubrir, es decir, parecerse al rival** [5];
  - **si nadie tiene ventaja, Kelly es el equilibrio** [9].
- La asimetría que importa en la arena es el Sharpe de cada estrategia y los errores no forzados de cada jugador (costos, ruina). El valor absoluto de la varianza pesa menos.

---

## 2. Matemáticas de la carrera: Kelly, mediana y ranking

### 2.1 Kelly y el costo de sobreapostar

[I, derivación estándar] Supuesto: rendimiento en exceso μ_e, volatilidad σ y exposición constante k (rebalanceo continuo). El crecimiento mediano (log) anual es:

`g(k) = k·μ_e − k²·σ²/2`

- Se maximiza en **k\* = μ_e/σ²** (Kelly).
- En **k = 2k\*** el crecimiento en exceso es **cero**.
- Arriba de 2k\* es negativo: la mediana del patrimonio cae aunque la media suba.

| μ_e anual (σ = 20%) | k\* (Kelly) | g(1x) | g(2x) | g(3x) | g(4x) |
|---|---|---|---|---|---|
| 5% | 1.25 | +3.0% | +2.0% | −3.0% | −12.0% |
| 8% | 2.00 | +6.0% | +8.0% | +6.0% | 0.0% |
| 15% | 3.75 | +13.0% | +22.0% | +27.0% | +28.0% |

Fuente: salida del modelo, bloque 4.

- [H] MacLean, Thorp y Ziemba documentan las propiedades buenas y malas de Kelly y del Kelly fraccional. El error de estimación de μ lleva a sobreapostar [10].
- [I, derivado] Con Kelly completo, la probabilidad de caer alguna vez a la mitad del capital es 1/2. Con medio Kelly es 1/8, porque P(tocar x) = x^(2/f − 1) para una fracción f de Kelly bajo GBM. Si la μ estimada es el doble de la verdadera, "Kelly completo" es en realidad 2k\* y el crecimiento en exceso es cero [10].
- [I] **Para ganar un duelo no se maximiza la mediana, se maximiza P(tu resultado > el del rival).** Un 3x con μ_e = 8% tiene la misma mediana que un 1x (ambos +6%), pero una distribución mucho más ancha. Esa anchura ayuda si vas atrás o si el rival es mejor que tú. Estorba si vas adelante o si tú eres el mejor.

### 2.2 La carrera de beta pura (resultado central)

[I, derivación propia con el modelo del bloque 1] Supuesto: las dos cuentas están expuestas al mismo factor M (por ejemplo, Nasdaq-100 en MXN) con exposiciones k_c > k_r y sin ruido propio. El log-rendimiento relativo es (k_c − k_r)·(σW_T) más una deriva, así que:

**P(Claude > rival) = Φ( √T · (μ_e − (k_c + k_r)·σ²/2) / σ )**

| μ_e anual | (1.5x vs 1x) | (2x vs 1x) | (3x vs 1x) | (3x vs 2x) |
|---|---|---|---|---|
| −10% | 29.8% | 28.6% | 26.2% | 24.0% |
| 0% | 43.0% | 41.6% | 38.9% | 36.2% |
| +8% | 54.2% | 52.8% | 50.0% | 47.2% |
| +15% | 63.8% | 62.5% | 59.8% | 57.0% |
| +20% | 70.2% | 69.0% | 66.4% | 63.8% |

σ = 20%, T = 0.5. Fuente: bloque 2 del modelo.

Qué implica [I]:
1. Estar "más apalancado que el rival" es **apostar a que el mercado sube**. Cuánto más apalancado estés no mejora la probabilidad: solo agranda la cola.
2. Subir k_c **baja** la probabilidad por el arrastre de volatilidad (el término (k_c + k_r)σ²/2).
3. Si hay razones para esperar μ_e alto en la temporada (sección 5: estacionalidad + intermedias), basta con estar **un poco** más expuesto que el rival. Estar "al máximo" no agrega nada.

### 2.3 Habilidad: la razón de información de la diferencia

[I] Si la diferencia de rendimientos tiene una media anual α_rel y una volatilidad TE, entonces P(ganar en T) ≈ Φ(IR·√T), con IR = α_rel/TE.

| IR de la diferencia | 0 | 0.25 | 0.50 | 0.75 | 1.00 | 1.50 |
|---|---|---|---|---|---|---|
| P(ganar en 6 meses) | 50.0% | 57.0% | 63.8% | 70.2% | 76.0% | 85.6% |

[I] Una IR de 0.5 sostenida ya es un gestor de primer cuartil. **Pasar de 65% exige una ventaja real o que el rival cometa errores** (costos, ruina, whipsaw). El nivel de riesgo, por sí solo, no la da.

### 2.4 Estrategia según el marcador

[I, bloque 5 del modelo] P(ganar) a mitad de temporada, con 3 meses restantes, μ_e = 8% y σ = 20%. Las filas son la ventaja actual en log-puntos y las columnas el tracking error anual de la diferencia:

| Ventaja \ TE | 2% | 5% | 10% | 20% | 40% |
|---|---|---|---|---|---|
| −10 pp | 0.0% | 0.0% | 2.7% | 17.1% | 30.9% |
| −5 pp | 0.0% | 2.8% | 17.7% | 32.6% | 40.1% |
| 0 | 53.8% | 53.5% | 53.0% | 52.0% | 50.0% |
| +5 pp | 100.0% | 98.2% | 85.9% | 70.9% | 59.9% |
| +10 pp | 100.0% | 100.0% | 98.1% | 85.3% | 69.1% |

- [I] Esto confirma la regla del `modo_torneo` en `parametros.json`: adelante se baja la varianza, atrás se sube la exposición. **Pero la varianza que cuenta es la de la diferencia contra el rival.**
- [I] Si el rival está 3x apalancado y tú vas adelante, irte a CETES **sube** el TE. La jugada que cubre es acercar tu exposición a la beta estimada del rival.
- [I] Taylor (2003) predice exactamente eso: el líder elige más seguido la estrategia riesgosa cuando el rezagado apuesta [5].

---

## 3. Competencias reales entre IAs: Alpha Arena (Nof1)

### 3.1 Temporada 1 (cripto)

- [H] **Formato:** 6 modelos con 10,000 USD reales cada uno. Operaron perpetuos en Hyperliquid sobre BTC, ETH, SOL, BNB, DOGE y XRP, con apalancamiento permitido.
- [H] Todos recibieron el mismo prompt y solo datos numéricos (sin noticias). Había una inferencia cada ~2–3 min. Cada acción incluía un plan de salida con objetivo, stop y "condición de invalidación".
- [H] La temporada corrió hasta el 3-nov-2025 a las 17:00 ET [11]. El inicio se reporta como 18-oct-2025 [14][19]; el primer registro de la API de Nof1 es del 17-oct-2025 ~23:00 UTC (ya 18-oct en hora de Asia) [44].

**Resultados finales [H] [44]** (API de Nof1 `account-totals`, marca horaria 407 = 3-nov-2025 ~22:00 UTC / 17:00 ET, copia archivada el 4-nov-2025 02:23 UTC):

| Lugar | Modelo | Valor final (USD, API) | Rendimiento (API) | Cifra publicada por iWeaver [14] |
|---|---|---|---|---|
| 1 | Qwen3 Max | 12,202 | **+22.0%** | +22.3% (Phemex: 12,231.82 USD) |
| 2 | DeepSeek Chat V3.1 | 10,453 | +4.5% | +4.89% |
| 3 | Claude Sonnet 4.5 | 6,890 | −31.1% | −30.81% |
| 4 | **Grok 4** | **5,456** | **−45.4%** | −45.3% |
| 5 | Gemini 2.5 Pro | 4,376 | −56.2% | −56.71% |
| 6 | GPT-5 | 3,734 | −62.7% | −62.66% (GNcrypto: ~3,733 USD) |
| — | Comprar y mantener BTC (referencia) | 9,994 | −0.1% | — |

- *(Corregido el 25-sep-2026.)* La versión anterior usaba ForkLog (4-nov-2025) [12] y TradeRank [19]: Claude 5,799 USD (−42.01%), Gemini 5,445 (−45.55%), **Grok 4 4,208 (−57.92%, 5° lugar)** y GPT-5 4,126 (−58.74%). **Esas cifras son erróneas:** en la serie horaria de la API, Claude nunca bajó de 6,345 USD ni Grok 4 de 5,179 USD. Las cifras de iWeaver [14] coinciden con la API con una diferencia de ±0.5 pp (probablemente por el minuto exacto de la captura). ForkLog sí acierta en el orden de los dos primeros.
- [H] **Foto publicada el 21-oct-2025** [13]: DeepSeek +35%, **Grok 4 +30%**, **Claude Sonnet 4.5 +28%**, Gemini −33% y GPT-5 −27%. Esa fuente dice que Grok "ganó dinero en el 100% de las últimas 5 rondas". *(Precisado el 25-sep-2026: esos valores coinciden con la API el **20-oct-2025 a las ~21:00 UTC**, día 3 [44].)*
- [H, cálculo propio con [44]] **Picos:** Grok 4 llegó a 15,037 USD (+50.4%) el 21-oct ~16:00 UTC. Claude llegó a 12,817 USD (+28.2%) el 27-oct.
- [I] **De +50% a −45%:** Grok 4 perdió ~64% desde su pico en ~13 días (15,037 → 5,456). Desde la foto del 20-oct (+30.5%) perdió ~58%. Claude pasó de +28% a −31%.
- [I] La lección para un duelo de 6 meses: **ir adelante temprano con apalancamiento alto y stops holgados no sirve de nada.** Hay que cuidar la ventaja (sección 2.4).

**Comportamiento observado por Nof1 en las corridas previas y el arranque [H] [11]:**
- Sesgo direccional: "**Grok 4, GPT-5 y Gemini 2.5 Pro shortean mucho más seguido** que los demás; Claude Sonnet 4.5 casi nunca shortea."
- Holding: "En nuestras corridas previas al lanzamiento, **Grok 4 tuvo los tiempos de tenencia más largos**."
- Frecuencia: "Gemini 2.5 Pro es el más activo; **Grok 4 típicamente el que menos**."
- Stops: "Qwen 3 usa las distancias de stop y objetivo más estrechas; **Grok 4 y DeepSeek V3.1 típicamente las más holgadas**."
- Tamaño: Qwen 3 abría las posiciones más grandes, a menudo múltiplos de las de GPT-5 y Gemini. Claude y Qwen mantenían 1–2 posiciones a la vez.
- Costos: "Al principio, el PnL estaba dominado por costos de operación"; los agentes sobreoperaban.
- Sensibilidad: hubo alta sensibilidad a cambios mínimos del prompt.
- Cifras que circulan en fuentes secundarias: Grok 4 con "apalancamiento promedio de 18x" y "158 órdenes contra 1,418 de Qwen" **(no verificado; contradicho por la API)**.
- [H, cálculo propio con las capturas horarias de la API [44]] Posiciones distintas observadas en la temporada en vivo y su apalancamiento:

| Modelo | Posiciones observadas | Cortos | Apalancamiento medio / mediano |
|---|---|---|---|
| Gemini 2.5 Pro | 196 | 97 | 14.3x / 10x |
| GPT-5 | 119 | 57 | 16.7x / 15x |
| **Grok 4** | **52** | **17** | **12.0x / 10x** |
| DeepSeek V3.1 | 43 | 2 | 12.3x / 10x |
| Qwen3 Max | 33 | 5 | 17.1x / 20x |
| Claude Sonnet 4.5 | 33 | 0 | 13.2x / 15x |

  - [I] Las capturas son horarias, así que las posiciones que abrieron y cerraron dentro de la misma hora no aparecen: son cotas inferiores. Aun así, el "18x" de Grok 4 y las "1,418 órdenes" de Qwen no son compatibles con estos datos.
  - [I] En vivo, Grok 4 **no fue el que menos operó** (quedó 3° de 6 en posiciones) y un tercio de sus posiciones fueron cortos. Claude no abrió ningún corto. El sesgo corto de Grok se confirma; la "baja actividad" solo se observó en las corridas previas.

### 3.2 Temporada 1.5 (acciones de EUA)

- [H] **Formato:** del 19/20-nov al 3-dic-2025, con acciones tokenizadas de EUA (TSLA, NVDA, MSFT, AMZN y el Nasdaq-100; algunas fuentes agregan GOOGL y PLTR).
- [H] Hubo 8 modelos en 4 competencias paralelas de 10,000 USD cada una:
  - New Baseline, con noticias y memoria;
  - Monk Mode, enfocada en preservar capital;
  - Situational Awareness, donde cada modelo veía el ranking;
  - Max Leverage, con apalancamiento de hasta 20x.
- [H] Fuentes del formato: [15][16][18].
- [H] **Grok 4.20** entró como "Mystery Model". Terminó con **+12.11% agregado (~4,844 USD de P&L sumando las cuatro cuentas)** y fue el único modelo positivo en el agregado [15]. **Ganó dinero en las cuatro competencias** [16].
- [H] GPT-5.1 quedó segundo y Gemini 3 tercero, ambos con pérdidas [15][16]. Otra fuente pone a DeepSeek V3.1 en segundo lugar [18] (hay contradicción entre fuentes).
- [H] Benzinga (18-ene-2026) reporta ~11,060 USD de equity promedio (+10.6%), habla de "10%–12% de rendimiento agregado" y **4 variantes de Grok en los 6 primeros lugares** [17]. Un post en X (dic-2025) da un valor de cuenta promedio de 10,927 USD (+9.3%) para Grok 4.20, 9,053 para GPT-5.1 y 6,718 para Gemini 3 Pro [45] **(no verificado)**. [I] El orden de los tres primeros es consistente entre fuentes; la magnitud del triunfo (+9% a +12%) depende de cómo se agregue.
- Mejor instancia individual: "+46.98% en Situational Awareness" según un post en X [20], y "máximo +34.59%, mínimo −96.15% entre 32 entradas" según un agregador **(ambos no verificados y contradictorios)**.
- Resultados de otros modelos que circulan en resúmenes: Claude Sonnet 4.5 −32.44%, DeepSeek V3.1 −24.51%, Kimi K2 −25.8%, Grok 4 −53.39% y Qwen3 Max ~−70% **(no verificado)**.
- Algunas notas dicen que Grok usó el "firehose" de X para sus señales **(no verificado; contradice que todos los modelos recibían el mismo input [15])**.

### 3.3 Temporadas posteriores

- [H] Al 6-ago-2026, el leaderboard de nof1.ai era un archivo con series que terminaban el 12-dic-2025. **No había roster ni resultados públicos de una temporada 2** [19] (TradeRank, actualizado el 14-sep-2026).
- No encontré resultados de temporadas de 2026.
- Versiones vigentes de Grok: Grok 4.6 salió el 12-ago-2026 y Grok 4.7 el 21-sep-2026; Grok 5 no ha salido [21]. *(25-sep-2026: las dos fechas coinciden en varias fuentes secundarias independientes; no consulté un comunicado de xAI.)*

### 3.4 Lecciones de Alpha Arena para el duelo

1. [I] **La mayoría pierde, y pierde por costos, apalancamiento y salidas.** En S1, 4 de 6 modelos perdieron más de 30% en ~17 días, y 3 de ellos más de 45% [44]. En S1.5, 7 de 8 perdieron en el agregado [15]. El "juego base" contra una IA que sobreopera o se sobreapalanca **se gana no cometiendo esos errores**.
2. [I] **El ranking temprano no predice nada.** La mitad de arriba del día 3 (DeepSeek, Grok, Claude) terminó 2°, 4° y 3°, y el líder final (Qwen) iba 4° ese día [13][44]. *(Corregido: decía 2°, 5° y 3°.)*
3. [I] **Grok 4.20 ganó en la modalidad con información del ranking**, y en conjunto en todas las modalidades [16][17]. Si el dueño le reporta el marcador a Grok, hay que esperar ajustes de riesgo según ese marcador.
4. [I] Los horizontes de Alpha Arena (2 semanas y apalancamiento de 10–20x) no se parecen a un duelo de 6 meses en GBM. **Lo transferible es el estilo del modelo, no los números.**

---

## 4. Perfil anticipado del rival (`arena-grok`, 15,000 MXN en GBM)

| Rasgo | Evidencia | Expectativa en GBM [I] |
|---|---|---|
| Direccionalidad | Grok 4 shortea más que la media [11]; en S1 en vivo, 17 de 52 posiciones fueron cortos [44] | Puede usar ETFs inversos o salirse a efectivo si ve debilidad. **SQQQ y SOXS están listados en el SIC** (A2 [46]); SH en el SIC: no verificado. El corto directo en GBM pide contrato firmado y activación por correo, y aparta 2 MXN de garantía por cada 1 MXN vendido; el "mínimo de 10,000 MXN" parece ser un ejemplo de la FAQ, no una regla (A1 [43], parcialmente verificado; no verificado) |
| Holding y frecuencia | Grok 4 tuvo los holdings más largos y la menor actividad en las corridas previas [11]; en vivo quedó a media tabla en actividad [44] | Pocas operaciones y posiciones que se mantienen. La ejecución manual del dueño también limita la frecuencia |
| Stops | Grok 4 usa los stops más holgados [11] | Drawdowns profundos antes de salir. **Puede regalar ventajas grandes**, como en S1: pico de +50% → −45% [13][44] |
| Apalancamiento | Alpha Arena lo permitía (8x–20x en los ejemplos de Nof1) [11]; Grok 4 usó 10x de mediana en vivo [44] | En GBM, apalancamiento vía ETFs 2x/3x. **TQQQ, SOXL y SPXL están listados y activos en el SIC**; QLD también, pero casi no opera. **UPRO y SSO: listado en el SIC no verificado** (A1 [43], A2 [46]) |
| Selección de activos | En S1.5 operó TSLA, NVDA, PLTR y NDX con éxito [15][18] | Acciones de "IA/momentum" concentradas (NVDA, PLTR, TSLA, semis) y ETFs 3x de Nasdaq o semis |
| Reacción al marcador | Su mejor versión ganó con información del ranking [16][17][20] | Si va atrás, más riesgo. Si va adelante, puede quedarse quieto |
| Versión | La que ganó fue Grok 4.20 (dic-2025). Hoy corren 4.6/4.7 [21] (no verificado) | El estilo puede haber cambiado. **Estas expectativas no están garantizadas** |

- [I] **Restricción de capital del rival:** con 15,000 MXN, en el SIC (títulos completos) un solo título de SMH (~600 USD ≈ 10,600 MXN con USD/MXN de 17.73; datos de la sección 6) ocuparía el ~70% de su cuenta. Por eso es probable que concentre o use Trading USA con fracciones.
- [I] Los costos fijos (por ejemplo, un W-8BEN de 75 USD + IVA en el SIC, según A1) pesan 33% más en % sobre 15k que sobre 20k.

**Cómo estimar la beta del rival solo con sus resultados [R]:**
1. Pedirle al dueño el valor de la cuenta del rival **cada viernes al cierre** (misma hora). Hoy `competencia/rivales.csv` está vacío.
2. Calcular el rendimiento semanal del rival, r_g, y el de QQQ, SPY y NAFTRAC en MXN.
3. Estimar β̂ = cov(r_g, r_QQQ,MXN)/var(r_QQQ,MXN) con una ventana móvil de 6–8 semanas, más el residuo (proxy del ruido idiosincrático) y R².
4. [I] Con 8 observaciones, el error estándar de β̂ es grande: del orden de σ_residuo/(σ_mercado·√6). Hay que usarlo como rango, no como punto. Un R² alto (> 0.7) con β̂ ≈ 3 delata un ETF 3x. Un R² bajo con residuo alto delata acciones concentradas.

---

## 5. Evidencia de estrategias candidatas para 6 meses

| Estrategia | Tamaño del efecto (fuente) | Persistencia fuera de muestra | Grado | Riesgo de cola | Uso en la arena [R] |
|---|---|---|---|---|---|
| **Momentum de series de tiempo (TSMOM, 12 meses)** | 58 contratos (1985–2009; datos desde 1965). **Sharpe > 1** en portafolio diversificado, ~2.5 veces el del mercado. Poca correlación con factores. Rinde mejor en mercados extremos (forma de "sonrisa") [22] | Documentado en varios activos. Sufre en reversiones: pérdidas en mar–may 2009 [22] | **A** (diversificado); B en un solo activo | Reversión en V al terminar las crisis [22] | Úsalo como filtro de exposición (dentro/fuera del índice), no como fuente de alfa en un solo activo |
| **Momentum transversal 12-1 / 6-6** | ~1% al mes largo-corto. La estrategia 6/6 da 12.01% anual compuesto en exceso (Jegadeesh-Titman 1993) [23] | 30+ años de réplicas. Se debilita en algunos periodos | **A/B** | **Momentum crashes**: pérdidas persistentes en "estados de pánico", después de caídas y con volatilidad alta, justo cuando el mercado rebota [25] | En 6 meses: 3–5 líderes con momentum positivo cerca de máximos. Se apaga en estado de pánico |
| **Cercanía al máximo de 52 semanas** | Domina y mejora el poder predictivo del rendimiento pasado [24]. Rendimiento mensual de ~0.45% en EUA según una cita secundaria **(no verificado en el paper)** | Replicado internacionalmente [24] | **B** | Igual que el momentum; más concentrado en líderes | Criterio de desempate para elegir líderes |
| **Dual momentum (Antonacci, GEM)** | Backtest original 1974–2013: CAGR ~17.4%, máxima caída de ~−22% y Sharpe de ~0.9 **(no verificado)**. El autor reporta +440 pb al año sobre el S&P 500 desde 1950 [26] **(no verificado: la página devolvió 403 el 25-sep-2026)** | **Fuera de muestra (2014–2026): CAGR de 8.4% contra 13.6% de SPY, Sharpe de 0.70 contra 0.94, máxima caída de −20% contra −24%** [26b] (secundaria; página del 31-jul-2026) | **C** | Whipsaw en mercados laterales (2011 y 2015–16) [26b] | No como núcleo. A 6 meses, lo más probable es 0–1 cambios de señal |
| **ETFs apalancados + filtro de tendencia (Gayed-Bilello 2016)** | Oct-1928 a oct-2015. S&P 500 buy & hold: 9.1% anual, vol de 18.9%, Sharpe de 0.30 y máxima caída de −86.2%. **LRS 2x: 19.1%, 24.9%, 0.51 y −78.7%.** **LRS 3x: 26.8%, 37.3%, 0.47 y −92.2%.** Unos 5 cambios al año, con costo de apalancamiento de 1% anual [27]. [I] El texto no menciona un costo de financiamiento aparte del 1% anual; si la simulación no descuenta el préstamo implícito ((L−1) × tasa de los T-bills mientras está invertido), sobreestima el rendimiento absoluto del 2x y del 3x (no verificado) | La regla de MA **sin apalancar** le gana al buy & hold en rendimiento absoluto solo en **49%** de las ventanas móviles de 3 años (promedio de MAs de 10 a 200 días, nota 21 del paper). El LRS supera al S&P en **80%** de ellas, en promedio [27] | **B** | Whipsaw. En 6 meses, el filtro **reduce la mediana** si el mercado arranca en tendencia (modelo, sección 7) | Núcleo del arquetipo A, con banda de 3% para reducir whipsaw |
| **Decaimiento de ETFs apalancados** | El rendimiento de un LETF lleva una opción dependiente del camino que destruye valor con volatilidad alta (Cheng-Madhavan 2009) [28]. Fórmula exacta que liga el rendimiento a L veces el del subyacente y a su varianza realizada (Avellaneda-Zhang 2010) [29]; "probada en 56 LETFs desde 2008" **(no verificado: no pude leer el resumen)** | Es matemática, no una anomalía | **A** | [I] Arrastre ≈ (L² − L)/2·σ²·T. Con σ realizada de QQQ de 20.6% (sección 6): **3x ≈ 6.4% y 2x ≈ 2.1% en 6 meses**. Con SPY (11.5%): 3x ≈ 2.0% y 2x ≈ 0.7% | Preferir 2x efectivo. El 3x solo en tendencia con VIX bajo, o para alcanzar al rival |
| **Estacionalidad nov–abr ("Halloween")** | Invierno > verano en **36 de 37 países** (Bouman-Jacobsen 2002) [30]. Versión de trabajo de 2012 de Jacobsen-Zhang: **108 mercados, 55,425 observaciones mensuales (más de 300 años de datos del Reino Unido): +4.52%; +6.25% en los últimos 50 años** [47]; el t = 9.69: no verificado. **Versión publicada (Zhang-Jacobsen, *JIMF* 110, 2021): 62,962 observaciones, nov–abr rinde "en promedio 4% más" y el verano tiene exceso de rendimiento de ~−1%** [31] | En 2012 los autores decían que el efecto **se estaba haciendo más fuerte** [47]; la versión de 2021 lo describe como "notablemente robusto" [31] | **B** | Ninguno propio. Es un sesgo de μ, no una cobertura | [I] La temporada (oct-2026 a abr-2027) cae en la mitad favorable. Sube la probabilidad a priori de μ_e > 0 |
| **Turn-of-the-month (TOM)** | 1926–2005 (EUA): **los inversionistas no recibieron premio por riesgo salvo en los 4 días del TOM** (del último día hábil a +3): 0.15% diario en el TOM contra −0.001% el resto de los días. Aparece en 31 de 35 países (McConnell-Xu 2008, *FAJ* 64(2):49–64) [32]. En el Dow 1897–1986 ya se había documentado que todo el rendimiento positivo caía en esa ventana (según Quantpedia) [33]. Quantpedia: 7.2% anual, vol de 6.9% y Sharpe de 1.04 (1926–2005) [33]. *(Corregido: decía "1897–2005" y "también en 1987–2005"; esto último no lo verifiqué.)* | Quantpedia advierte que "los efectos de calendario tienden a desaparecer o a rotar" [33] | **B** como efecto; **C** como estrategia en GBM | Bajo | [I] Con 0.58% por vuelta (A1) no conviene operarlo solo. **Úsalo para el timing**: compra antes del cierre de mes y vende después del día +3 |
| **Deriva pre-FOMC** | **+49 pb en las 24 h previas** al FOMC, sep-1994 a mar-2011; ~80% del exceso anual (Lucca-Moench 2015) [34] | **"Esencialmente desapareció después de 2015"** en la muestra hasta dic-2019 (Kurov-Wolfe-Gilbert 2021) [35] | **D** | — | No usar. Fechas relevantes: FOMC del 27–28 oct y del 8–9 dic de 2026 [40] |
| **Ciclo presidencial / intermedias** | El exceso de rendimiento es mayor con presidentes demócratas (+9% VW, +16% EW) y **no se concentra alrededor de las elecciones** (Santa-Clara-Valkanov 2003) [36]. El ciclo de 4 años es el más prominente en 1965–2003 (Wong-McAleer 2009) [37]. **Post-intermedias: el S&P 500 fue positivo 9 de cada 10 veces en el 4T del año de intermedias y los dos trimestres siguientes, ~+25% compuesto, 1954–2017** (Białkowski-Nahavandi 2019, *JWM* 21(4):76–84) [38]. Sin rendimiento negativo a 12 meses tras una intermedia desde 1950 (19 de 19) [39] (secundaria) | Muestra pequeña (~16 intermedias en 1954–2017). La política monetaria y la fiscal no lo explican [38] | **C** | Sin cola propia. Riesgo de sobreajuste de narrativa | [I] Elección intermedia: **martes 3-nov-2026** (primer martes después del primer lunes de noviembre). Coincide casi exacto con la temporada. Refuerza no estar corto ni en efectivo "por defecto" |
| **Momentum crashes (riesgo)** | Crashes parcialmente pronosticables: en estados de pánico, después de caídas y con volatilidad alta, y contemporáneos a los rebotes (Daniel-Moskowitz 2016) [25] | Desde la era victoriana, en varios países y activos [25] | **A** (como riesgo) | Es la cola del momentum | [R] Si el S&P cae más de 15% y el VIX supera 30, no se entra a momentum transversal; se reduce a beta de índice |

---

## 6. Contexto de mercado al arranque (datos al 24-sep-2026)

[H] Cálculos míos con precios diarios de Yahoo Finance (API de gráficas, cierre del 24-sep-2026; USD/MXN y BTC del 25-sep). Los valores exactos se pueden verificar en [41][42].

| Activo | Cierre | vs SMA200 | vs máx. 52 sem. | Momentum 12-1 | Vol. realizada 63 d |
|---|---|---|---|---|---|
| S&P 500 (^GSPC) | 7,704.13 | **+7.1%** | −1.2% | +14.3% | 11.2% |
| SPY | 767.18 | +6.8% | −1.4% | +16.4% | 11.5% |
| QQQ | 741.10 | **+11.4%** | −0.9% | +19.2% | 20.6% |
| SSO (2x S&P) | 70.26 | +11.6% | −3.1% | +26.8% | 22.6% |
| QLD (2x Nasdaq-100) | 96.10 | +19.4% | −4.4% | +30.4% | 41.0% |
| UPRO (3x S&P) | 149.99 | +16.0% | −4.9% | +33.4% | 34.4% |
| TQQQ (3x Nasdaq-100) | 78.58 | +25.0% | −9.9% | +37.9% | 60.8% |
| SMH (semis) | 600.52 | +22.0% | −10.2% | **+73.3%** | 43.3% |
| IPC (^MXX) | 64,264 | **−4.4%** | −10.2% | +6.1% | 12.2% |
| NAFTRAC | 64.01 | −4.4% | −10.0% | +10.6% | 13.1% |
| USD/MXN | 17.73 | +1.8% | −5.1% | −8.1% | 6.6% |
| BTC-USD | 84,227 | +18.9% | −11.8% | −14.9% | 35.2% |
| **VIX** | **15.67** | −13.3% | −49.5% | — | — |

[I] Qué implica:
- **El filtro de `parametros.json` (subyacente arriba de su SMA200 y VIX < 25) hoy está en "verde" para S&P y Nasdaq, y en "rojo" para el IPC.** La temporada arranca en "estado de calma", no de pánico: el riesgo de momentum crash es bajo al inicio [25].
- El liderazgo está muy concentrado en semis/IA (SMH con +73% de momentum 12-1). Es el candidato natural del rival y un riesgo de rotación.
- La depreciación reciente del peso (el USD/MXN sube de su SMA50 de 17.16 a 17.73) suma a los activos en USD, medidos en MXN.
- [I] *(Corregido el 25-sep-2026: decía que algunas volatilidades, como la de QLD contra la de QQQ, sugerían datos ruidosos.)* Las volatilidades de los apalancados son consistentes con L × σ del subyacente: QLD 41.0% ≈ 2 × 20.6%, TQQQ 60.8% ≈ 3 × 20.6%, SSO 22.6% ≈ 2 × 11.5% y UPRO 34.4% ≈ 3 × 11.5%. Lo atípico es la razón QQQ/SPY (20.6% contra 11.5%), que A2 también encuentra en 2026 (22.3% contra 13.5% a 6 meses) [46]. Recalculé S&P, SPY, QQQ, SMH, VIX y USD/MXN con la misma API el 25-sep-2026 y coinciden con la tabla (USD/MXN: 17.71 a la hora de la consulta).

---

## 7. Modelo: P(R_claude > R_rival) a 6 meses

### 7.1 Supuestos

| Supuesto | Valor | Por qué |
|---|---|---|
| Horizonte | T = 0.5 años (126 días hábiles) | Temporada de 6 meses |
| Métrica | Rendimiento en exceso de un mismo efectivo (CETES/cash). El tipo de cambio es parte del factor común | Las dos cuentas probablemente estarán en activos en USD. Si el rival se queda en MXN, el USD/MXN se vuelve fuente de TE (no modelado) |
| Factor común M (analítico) | σ = 20%. μ_e con escenarios de −10% (25%), +8% (50%) y +20% (25%) | Volatilidad tipo Nasdaq/S&P en MXN. La mezcla de escenarios refleja la incertidumbre sobre μ |
| Factor M (Monte Carlo) | **Régimen A:** calma (μ +16%, σ 13%) / estrés (μ −15%, σ 35%), con transiciones de 1/120 y 1/40 por día → μ ≈ 8% y σ ≈ 21%. **Régimen B:** calma (μ +20%, σ 12%) / bajista persistente (μ −30%, σ 30%), con transiciones de 1/250 y 1/80 → μ ≈ 8% y σ ≈ 18% | A = estrés corto (poca persistencia de tendencia). B = mercados bajistas persistentes (lo que el filtro SMA200 explota [27]) |
| Estado inicial | Calma. Precio entre +4% y +10% sobre la SMA200 (historia de 200 días simulada y filtrada por rechazo) | Hecho al 24-sep-2026: S&P +7.1% sobre su SMA200 y VIX 15.67 (sección 6) |
| Costos | Comisión GBM 0.29% por lado + 0.10% de spread = **0.39% por lado**. ETF apalancado: 1% anual. ETF 1x: 0.1% anual | A1 [43]. El 1% de apalancamiento es el supuesto de Gayed-Bilello [27]. [I] En el SIC, A2 midió una desviación mediana contra el valor justo de 0.17% en TQQQ/SPXL y de 0.41% en QLD [46]: el 0.10% es optimista para los LETF. Con ≤5 cambios al año no mueve las conclusiones, pero sí el costo del sobretrading (R3) |
| ETFs apalancados | Reinicio diario: V_{t+1} = V_t·(1 + L·r_t − f) | Así funcionan los LETF [28][29] |
| Rivales | R1 concentrado (beta 1.3 + ruido idiosincrático de 30%). R2 3x comprar y mantener. R3 "trader sin ventaja" (cada semana elige al azar 0x, 1x o 2x y paga comisiones). R4 conservador (0.6x) | R1 y R2 son el estilo esperado de Grok (sección 4). R3 es el sobretrading que se vio en Alpha Arena [11]. R4 es un control |
| "Rival tipo Grok" | Mezcla de 40% R1, 25% R2, 20% R3 y 15% R4 | Supuesto mío, basado en la sección 4 |
| Momentum concentrado | Beta 1.3 + ruido de 20% + alfa de 4% anual (C7) o de 0% (C7b) | El 4% es un recorte fuerte al ~12% anual de JT [23], por decaimiento, solo largos y costos. C7b es el caso sin ventaja |
| Modo torneo (C9–C11) | Igual que su base hasta el día 63 (C9: base C8; C10: 2x sin filtro; C11: 1x sin filtro). Si va atrás ≥5% → sube un escalón (3x, o 2x en C11). Si va adelante ≥5% → copia la beta del rival, sin filtro. Cada cambio cuesta 2 lados de comisión | **Optimista:** supone que se conoce la beta del rival. En la práctica se estima con ruido (sección 4). [I] El escalón a 3x y copiar la beta de R2 (3x) **exceden `etf_apalancado_max` = 0.5** (máximo ~2x efectivo) |
| No modelado | Cortacircuitos del perfil (−12%: bajar 50% la exposición táctica; −20%: sin LETF; −28%: pausa; −35%: todo a CETES), filtro de VIX < 25 y `kelly_fraccion_max` = 0.5 | [I] Revisado en el código el 25-sep-2026. En las estrategias con LETF, el −20% corta la cola antes del −35% (salvo gaps), así que el P(< −35%) reportado probablemente sobreestima la ruina, y el P(ganar) puede cambiar en cualquier dirección |
| Empates | Cuentan 1/2 | Relevante cuando se usa exactamente el mismo instrumento que el rival |

### 7.2 Código

Archivo completo: `/home/user/New1/arena/modelos/p_ganar_torneo.py`. Se corre con `python3 p_ganar_torneo.py 20000` (~50 s).

```python
"""
P(R_claude > R_rival) a 6 meses para distintos niveles de exposicion.
Solo stdlib. Todos los rendimientos son EN EXCESO sobre un mismo rendimiento de efectivo (CETES/cash);
el tipo de cambio se trata como parte del factor comun (ambas cuentas en activos en USD).
"""
import math, random, statistics, sys

T = 0.5          # horizonte: 6 meses
DIAS = 126       # dias habiles en 6 meses
def Phi(x):      # CDF normal estandar
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

# 1) MODELO ANALITICO (log-normal, rebalanceo continuo)
#    X_i = [a_i + k_i*mu_e - (k_i^2*sigma^2 + s_i^2)/2 - c_i]*T + k_i*sigma*W_T + s_i*Z_i*sqrt(T)
#    D = X_c - X_r es normal => P(gana Claude) = Phi(E[D]/sd[D]).
def p_analitica(k_c, k_r, mu_e, sigma, s_c=0.0, s_r=0.0, c_c=0.0, c_r=0.0, a_c=0.0, a_r=0.0, tau=T, ventaja_log=0.0):
    m_c = a_c + k_c * mu_e - (k_c**2 * sigma**2 + s_c**2) / 2 - c_c
    m_r = a_r + k_r * mu_e - (k_r**2 * sigma**2 + s_r**2) / 2 - c_r
    media = ventaja_log + (m_c - m_r) * tau
    sd = math.sqrt(((k_c - k_r)**2 * sigma**2 + s_c**2 + s_r**2) * tau)
    if sd == 0:
        return 1.0 if media > 0 else (0.5 if media == 0 else 0.0)
    return Phi(media / sd)

def costo_letf(k):   # comision anual implicita de ETF apalancado (supuesto: 1%/ano como Gayed-Bilello)
    return 0.01 if k > 1 else 0.001

# (tabla_analitica(): bloques 1-5 de la salida; ver archivo)

# 2) MONTE CARLO con regimenes, ETFs con reinicio diario, filtro SMA200 y costos de GBM.
COM = 0.0029 + 0.0010                      # 0.29% comision+IVA por lado + 0.10% spread
PESOS_RIVAL_GROK = (0.40, 0.25, 0.20, 0.15)
REGIMENES = {
    "A_estres_corto": dict(mu_c=0.16, sd_c=0.13, mu_s=-0.15, sd_s=0.35, p_cs=1 / 120, p_sc=1 / 40),
    "B_bajista_persistente": dict(mu_c=0.20, sd_c=0.12, mu_s=-0.30, sd_s=0.30, p_cs=1 / 250, p_sc=1 / 80),
}
def simula(n, semilla=7, regimen="A_estres_corto"):
    rng = random.Random(semilla)
    g = REGIMENES[regimen]
    mu_c, sd_c = g["mu_c"] / 252, g["sd_c"] / math.sqrt(252)
    mu_s, sd_s = g["mu_s"] / 252, g["sd_s"] / math.sqrt(252)
    p_cs, p_sc = g["p_cs"], g["p_sc"]
    # ... estrategias C0..C8, rivales R1..R4 y variantes C9..C11 de modo torneo por rival (ver archivo) ...
    for _ in range(n):
        while True:   # historia de 200 dias condicionada: precio entre +4% y +10% sobre su SMA200
            estado, precios = 0, [100.0]
            for _d in range(200):
                if estado == 0 and rng.random() < p_cs: estado = 1
                elif estado == 1 and rng.random() < p_sc: estado = 0
                mu, sd = (mu_c, sd_c) if estado == 0 else (mu_s, sd_s)
                precios.append(precios[-1] * math.exp(mu - sd * sd / 2 + sd * rng.gauss(0, 1)))
            if 1.04 <= precios[-1] / (sum(precios[-200:]) / 200) <= 1.10:
                break
        estado = 0
        for d in range(DIAS):
            sma = sum(precios[-200:]) / 200
            # senal de filtro (precio > SMA200; C8: sale < 0.97*SMA, reentra > SMA), cobro de COM por cambio,
            # R3 cambia exposicion semanal al azar, C9..C11 deciden modo en d == 63 segun ventaja vs cada rival
            if estado == 0 and rng.random() < p_cs: estado = 1
            elif estado == 1 and rng.random() < p_sc: estado = 0
            mu, sd = (mu_c, sd_c) if estado == 0 else (mu_s, sd_s)
            r = math.exp(mu - sd * sd / 2 + sd * rng.gauss(0, 1)) - 1
            precios.append(precios[-1] * (1 + r))
            # ETF L-veces con reinicio diario: V *= max(0, 1 + L*r - fee_diario)
            # concentrado: V *= (1 + beta*r) * exp(eps - s^2/2/252) [+ alfa/252]
```

El fragmento de arriba resume el archivo. El archivo trae todas las estrategias, los cobros de comisión, el modo torneo por rival y los reportes.

### 7.3 Resultados analíticos (bloque 1): P(Claude > rival) ponderada por escenarios de μ

| Rival \ exposición de Claude | 0x | 0.5x | 1x | 1.5x | 2x | 2.5x | 3x |
|---|---|---|---|---|---|---|---|
| Conservador (0.8x, ruido 5%) | 44.5% | 47.7% | **54.8%** | 51.8% | 50.9% | 49.7% | 48.5% |
| Concentrado (1.3x, ruido 30%) | 49.8% | 52.1% | **54.0%** | 53.9% | 53.3% | 51.9% | 50.3% |
| Apalancado (2.5x, ruido 15%) | 48.7% | 50.2% | 51.7% | 52.2% | **52.8%** | 51.2% | 47.5% |

Contra el rival concentrado, por escenario de μ_e:
- Bajista (−10%): 0x = 64.8% … 3x = 33.3%.
- Base (+8%): el máximo es 54.2% con 1.5–2x.
- Alcista (+20%): 0x = 37.6% … 3x = 64.2%.

[I] El óptimo analítico es una exposición **parecida o un poco mayor que la del rival**, y la curva es plana (±3 pp). **Ningún nivel de exposición, por sí solo, pasa de ~55%.** El salto en la fila del conservador (1x → 1.5x) se debe a que el costo de 1% anual del LETF entra cuando k > 1.

### 7.4 Resultados Monte Carlo (20,000 trayectorias por régimen)

**Régimen A (estrés corto):**

| Estrategia de Claude | Mediana | p5 | p95 | P(< −35%) | vs R1 | vs R2 | vs R3 | vs R4 | Promedio | **Mezcla Grok** |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 efectivo | 0.0% | 0.0% | 0.0% | 0.0% | 46.4% | 39.8% | 63.3% | 35.6% | 46.3% | 46.5% |
| C1 índice 1x | 4.9% | −19.4% | 28.0% | 0.6% | 52.9% | 41.9% | 83.8% | 64.2% | 60.7% | 58.0% |
| C2 2x comprar-mantener | 8.3% | −36.9% | 61.2% | 5.7% | 55.8% | 43.6% | 77.9% | 61.0% | 59.6% | 58.0% |
| C3 3x comprar-mantener | 10.4% | −51.9% | 100.6% | 12.1% | 56.5% | 50.0% | 70.2% | 59.1% | 58.9% | 58.0% |
| C4 2x con filtro SMA200 | 1.9% | −27.6% | 60.1% | 1.6% | 53.9% | 27.1% | 73.5% | 53.6% | 52.0% | 51.1% |
| C5 3x con filtro SMA200 | 1.8% | −38.3% | 98.8% | 7.0% | 54.9% | 40.1% | 67.0% | 51.3% | 53.3% | 53.1% |
| C6 barbell (60% efectivo + 40% 3x con filtro) | 0.5% | −15.5% | 39.3% | 0.0% | 52.0% | 32.6% | 78.9% | 53.7% | 54.3% | 52.8% |
| C7 momentum concentrado (alfa 4%) | 6.6% | −29.1% | 52.5% | 2.6% | 55.4% | 47.1% | 74.4% | 58.5% | 58.9% | 57.6% |
| C7b momentum concentrado (alfa 0%) | 4.5% | −30.5% | 49.4% | 3.1% | 52.3% | 44.2% | 70.7% | 53.8% | 55.2% | 54.2% |
| C8 2x con filtro SMA200 y banda de 3% | 5.3% | −27.2% | 60.6% | 1.4% | 55.7% | 30.9% | 76.6% | 56.7% | 55.0% | 53.8% |
| **C9 = C8 + modo torneo** | — | — | — | 3.2% | 57.9% | 34.2% | 80.6% | 65.8% | 59.6% | **57.7%** |
| C10 = 2x sin filtro + modo torneo | — | — | — | 6.8% | 57.6% | 41.3% | 81.7% | 70.0% | 62.7% | **60.2%** |
| C11 = 1x sin filtro + modo torneo (atrás → 2x) | — | — | — | 2.4% | 53.3% | 44.1% | 83.9% | 66.2% | 61.9% | **59.1%** |

**Régimen B (bajista persistente):**

| Estrategia de Claude | Mediana | p5 | p95 | P(< −35%) | vs R1 | vs R2 | vs R3 | vs R4 | Promedio | **Mezcla Grok** |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 efectivo | 0.0% | 0.0% | 0.0% | 0.0% | 41.8% | 29.3% | 58.1% | 26.8% | 39.0% | 39.7% |
| C1 índice 1x | 7.4% | −17.4% | 26.1% | 0.5% | 51.6% | 30.7% | 87.0% | 73.5% | 60.7% | 56.7% |
| C2 2x comprar-mantener | 14.1% | −33.6% | 57.3% | 4.6% | 59.2% | 31.6% | 84.7% | 71.1% | 61.6% | 59.2% |
| C3 3x comprar-mantener | 20.7% | −47.8% | 95.3% | 8.5% | 63.6% | 50.0% | 79.4% | 70.0% | 65.8% | 64.3% |
| C4 2x con filtro SMA200 | 11.6% | −22.7% | 57.0% | 0.7% | 58.9% | 19.9% | 81.8% | 65.8% | 56.6% | 54.7% |
| C5 3x con filtro SMA200 | 17.1% | −31.7% | 94.8% | 3.5% | 63.4% | 41.9% | 77.4% | 64.2% | 61.7% | 60.9% |
| C6 barbell (60% efectivo + 40% 3x con filtro) | 6.6% | −12.9% | 37.7% | 0.0% | 53.3% | 23.8% | 85.0% | 65.7% | 56.9% | 54.1% |
| C7 momentum concentrado (alfa 4%) | 9.9% | −26.0% | 51.1% | 2.0% | 55.7% | 37.8% | 76.5% | 62.2% | 58.0% | 56.3% |
| C7b momentum concentrado (alfa 0%) | 7.8% | −27.5% | 48.1% | 2.3% | 52.4% | 34.7% | 72.7% | 57.6% | 54.4% | 52.8% |
| C8 2x con filtro SMA200 y banda de 3% | 13.4% | −22.2% | 57.2% | 0.6% | 60.4% | 23.2% | 85.1% | 68.8% | 59.4% | 57.3% |
| **C9 = C8 + modo torneo** | — | — | — | 1.9% | 61.3% | 25.4% | 87.7% | 75.6% | 62.5% | **59.8%** |
| C10 = 2x sin filtro + modo torneo | — | — | — | 5.1% | 60.2% | 29.7% | 87.7% | 78.0% | 63.9% | **60.7%** |
| C11 = 1x sin filtro + modo torneo (atrás → 2x) | — | — | — | 2.0% | 52.3% | 32.4% | 87.2% | 74.8% | 61.7% | **57.7%** |

En C9, C10 y C11 la mediana y los percentiles no aplican: hay una trayectoria distinta contra cada rival. P(< −35%) es el promedio de las cuatro.

Medianas de los rivales:
- Régimen A: R1 2.6%, R2 10.4%, R3 **−5.0%** y R4 2.9%.
- Régimen B: R1 5.7%, R2 20.7%, R3 −2.5% y R4 4.3%.

**Cómo leer el modelo [I]:**
1. **Todas las estrategias sensatas quedan entre 51% y 64%** contra la mezcla de rivales (C4 en el régimen A: 51.1%). El modelo no tiene una estrategia que "gane seguro".
2. **Contra el mismo instrumento (C3 vs R2) es un volado exacto (50%).** Esto confirma a Browne [9]: sin diferenciación no hay ventaja.
3. **El filtro SMA200 sin banda (C4) le quita de 4 a 7 pp de probabilidad al 2x comprar-mantener** en un horizonte de 6 meses que arranca en tendencia, por el whipsaw. **La banda de 3% (C8) recupera 2.6–2.7 pp (entre 40% y 60% de lo perdido) y deja el riesgo de ruina en 0.6–1.4%**, contra 4.6–5.7% del 2x sin filtro. *(Corregido: decía "recupera la mayor parte"; en el régimen A recupera 2.7 de 6.9 pp.)*
   - Esto es coherente con Gayed-Bilello: la regla solo gana en términos absolutos en 49% de las ventanas de 3 años. Su valor está en la cola [27].
4. **El modo torneo agrega de +1 a +4 pp a cualquier base.**
   - Sobre C8, sube a 57.7% / 59.8% (C9).
   - Sobre el 2x sin filtro, sube a 60.2% / 60.7% (C10), pero con una ruina de 5–7%.
   - Sobre el 1x, sube a 59.1% / 57.7% (C11), con una ruina de ~2%.
   - Supuesto optimista: se conoce la beta del rival.
5. **La sencillez compite.** El índice 1x sin filtro (C1) logra 58.0% / 56.7% con una ruina de 0.5–0.6%: mejor que C8 sin modo torneo en el régimen A (58.0% contra 53.8%) y 0.6 pp peor en el B (56.7% contra 57.3%).
   - [I] El filtro de tendencia en un duelo de 6 meses es **un seguro contra la cola**, no una fuente de probabilidad.
   - El filtro paga en el régimen B (bajistas persistentes) y cuesta en el A.
6. **3x comprar y mantener (C3) tiene la probabilidad más alta en el régimen B (64.3%), pero con P(< −35%) de 8.5–12.1%.** Viola el límite `etf_apalancado_max` = 0.5 del perfil y dispararía el cortacircuitos de −35%, que en la práctica te saca del juego.
7. **El sobretrading es el peor error.** Contra R3, cualquier estrategia con exposición gana del 67% al 88% de las veces. R3 pierde de 5% a 9% solo en comisiones: 26 semanas × 2/3 de probabilidad de cambio × ~1.33 lados × 0.39% ≈ 9%.
8. **Error de Monte Carlo:** con 20,000 trayectorias, el error estándar de cada probabilidad es de ~0.35 pp. Las comparaciones usan los mismos números aleatorios (pareadas), así que diferencias de ≥1 pp son del modelo y no del ruido. **Las diferencias de 1–3 pp entre las mejores opciones son menores que la incertidumbre de los supuestos.**

---

## 8. Tres arquetipos para la temporada

| Arquetipo | Implementación en GBM [R] | Exposición efectiva | P(ganar) vs "rival tipo Grok" (régimen A / B) | P(< −35%) | Supuestos clave |
|---|---|---|---|---|---|
| **A. Tendencia + apalancado** (base) | 50% en ETF 3x (**SPXL o TQQQ**, listados y activos en el SIC; UPRO no verificado [46]) + 50% en ETF 1x. En el SIC no hay fracciones: 1 título de QQQ o SPY es 66–68% de la cuenta, así que el 1x va en QQQM o SPYM (antes SPLG) [46]. Otra opción es 100% en un 2x si el perfil sube el límite de apalancados: QLD está listado pero opera ≤0.1 M MXN/día y SSO no está verificado en el SIC [46]. Filtro: subyacente arriba de SMA200 **con banda de 3% para salir** y VIX < 25. Con modo torneo a mitad de temporada | ~2x (≈ Kelly completo con μ_e = 8% y σ = 20%; [I] eso es el doble de `kelly_fraccion_max` = 0.5 del perfil, que con esos supuestos da ~1x) | **53.8% / 57.3%** sin modo torneo; **57.7% / 59.8%** con modo torneo | 0.6–1.4% (hasta 1.9–3.2% con modo torneo) | μ_e > 0 en la temporada (apoyado por nov–abr [31] e intermedias [38]). Decaimiento del LETF con la σ actual (~2–6% en 6 meses). Arranque en calma |
| **B. Momentum concentrado** | 3–5 ETFs sectoriales o acciones líderes con momentum 12-1 positivo y a ≤5% de su máximo de 52 semanas, revisión mensual (≤ 8 operaciones al mes). Se apaga en estado de pánico [25] | ~1.3x por la beta de los líderes | **52.8–57.6% / 52.8–56.3%**, según el alfa (0–4%) | 2.0–3.1% | La ventaja depende de que el momentum siga vivo en líderes de IA/semis (SMH +73% en 12-1). Riesgo de rotación. **Se parece a lo que probablemente hará el rival**, así que baja la diferenciación |
| **C. Barbell** | 60% en CETES/efectivo + 40% en ETF 3x con filtro. El efectivo es munición para subir la exposición si vamos atrás | ~1.2x cuando el filtro está dentro | **52.8% / 54.1%** | **0.0%** | Pierde contra rivales con beta > 1 en mercados alcistas (R2: 24–33%). Su valor es la opcionalidad para el modo torneo y el desempate (menor máxima caída) |

**Variante simple de A [I]:** índice 1x sin filtro + modo torneo (atrás → 2x; adelante → copiar la beta del rival). Da **59.1% / 57.7%** con una ruina de ~2% (C11). Es casi la misma probabilidad con menos piezas móviles y menos operaciones. Pierde en la cola si hay un mercado bajista persistente antes de la mitad de la temporada.

**Probabilidad estimada contra un rival típico [I]:**
- A ≈ 54–60%: 54–57% sin modo torneo y 58–60% con él.
- B ≈ 53–58%.
- C ≈ 53–54%.

Rangos y supuestos [I]:
- Los rangos combinan los dos regímenes y la mezcla supuesta de rivales. Los supuestos principales son μ_e ≈ 8% anual incondicional, σ ≈ 18–21% y el arranque en calma (sección 7.1).
- Si la temporada resulta alcista (μ_e ≈ 20%), todas las estrategias con exposición ≥ 1.5x suben a ~60–65%.
- Si resulta bajista (μ_e ≈ −10%), el filtro y el barbell pasan a ser los mejores (bloque 1).
- **No simulé** la mejora por habilidad en la selección (IR > 0). Cada 0.25 de IR suma ~7 pp (sección 2.3).

---

## Implicaciones para la cuenta arena

1. **[R] Arquetipo base: A (tendencia + apalancado ~2x con banda de 3%) con modo torneo (C9: 57.7% / 59.8%, ruina 2–3%).**
   - La base (50% en 3x + 50% en 1x) cabe en `etf_apalancado_max` 0.5. *(Corregido el 25-sep-2026: decía que todo el arquetipo era compatible con el perfil provisional.)* [I] Tres choques con `parametros.json`: (a) el escalón a 3x del modo torneo y copiar a un rival 3x piden 100% en LETF, fuera del límite de 0.5; (b) ~2x es Kelly completo con μ_e = 8%, contra `kelly_fraccion_max` = 0.5; (c) el Monte Carlo no incluye los cortacircuitos −12/−20/−28/−35 ni el filtro de VIX. Hay que decidir si el perfil se ajusta al modo torneo o el modo torneo se limita a ~2x, y volver a correr C9 con esa regla.
   - Alternativa de igual probabilidad y menos operaciones: 1x + modo torneo (C11: 59.1% / 57.7%, ruina ~2%). [I] Su escalón (atrás → 2x = 50% en 3x + 50% en 1x) **sí cabe en `etf_apalancado_max` = 0.5**; solo la rama "adelante → copiar a un rival 3x" lo excede. Con el perfil actual, C11 es la variante de modo torneo más cercana a ser ejecutable tal como se simuló.
   - La versión sin filtro (C10: 60.2% / 60.7%) gana 1–2 pp más, pero duplica la ruina (5–7%). No conviene mientras el cortacircuitos de −35% nos saque del juego.
   - El 3x completo (C3/C5) solo se usa como herramienta para alcanzar al rival, no como punto de partida.
2. **[R] Corregir el sentido del `modo_torneo` en `parametros.json`.** Donde dice "Adelante del mejor rival: reducir varianza" debe decir **"reducir el tracking error contra el rival (acercarse a su beta estimada)"**. Irse a efectivo cuando el rival está apalancado **aumenta** el riesgo de perder la ventaja (tabla 2.4; Taylor [5]).
3. **[R] Instrumentar el marcador.**
   - El dueño registra en `competencia/rivales.csv` el valor de `arena-grok` cada viernes al cierre, con la fecha y la hora.
   - Con eso se estima la β̂ del rival contra QQQ, SPY y NAFTRAC en MXN, con una ventana de 6–8 semanas (sección 4).
   - El marcador se lleva en log-puntos, con ajuste por aportaciones (TWR).
4. **[R] Regla de mitad de temporada** (enero de 2027, ~día 63):
   - atrás ≥ 5 pp → subir a ~3x efectivo en la parte de LETF, manteniendo el filtro; [I] con `etf_apalancado_max` = 0.5 el tope real es ~2x total (50% en 3x + 50% en 1x). El 3x total que simula C9 exige subir ese límite;
   - adelante ≥ 5 pp → copiar la β̂ del rival (sin irse a efectivo), con el mismo tope de ~2x si su β̂ es mayor;
   - en otro caso, sin cambios.
   - En el último mes, si vamos atrás, la teoría de Browne [8][9] justifica subir el TE todavía más: la ventana para alcanzar se cierra. Si vamos adelante, cubrir.
5. **[R] Presupuesto de operaciones.**
   - ≤ 1 rotación completa al mes, como en A1.
   - Ninguna operación que dependa de efectos de calendario (pre-FOMC: grado D; TOM: solo para el timing de entradas).
   - **El modelo muestra que el sobretrading sin ventaja cuesta de 5% a 9% en la temporada**, más que cualquier diferencia entre estrategias.
6. **[R] Estacionalidad a favor, no en contra.**
   - La temporada (oct-2026 a abr-2027) coincide con la mitad fuerte del año [30][31] y con la ventana post-intermedias [38]: elección el 3-nov-2026.
   - Implicación: **no arrancar en efectivo ni corto "por prudencia"**. En el bloque 1, el efectivo (0x) solo gana si la temporada es bajista.
   - Grado B + C: sesgo de μ, no certeza.
7. **[R] Diferenciarse del rival solo donde haya ventaja.**
   - Si se espera que Grok concentre en IA/semis (sección 4), la opción A sobre índice amplio (S&P/Nasdaq-100) es **distinta con Sharpe comparable**. Gana si su concentración sufre arrastre de volatilidad o una rotación.
   - Copiar su canasta convierte el duelo en un volado.
8. **[R] Stops y ejecución.**
   - Las posiciones apalancadas van en Trading MX/SIC con stop u OCA registrados desde la entrada (A1: Trading USA no tiene stops).
   - La banda de 3% bajo la SMA200 del subyacente es la regla de salida. El VIX > 25 corta los LETF (perfil vigente).
   - [I] El `filtro_apalancados` vigente dice "se venden al perder el filtro", es decir, al cruzar la SMA200 sin banda (la estrategia C4). Usar la banda de 3% (C8) requiere cambiar ese texto en `parametros.json`.
9. **[R] Estado de pánico = no hay momentum.** Si el S&P cae más de 15% desde su máximo y el VIX supera 30, se desmonta cualquier sesgo de momentum transversal (Daniel-Moskowitz [25]). Quedan beta de índice y efectivo, y se reevalúa con el marcador.
10. **[R] Qué validar en papel antes de operar** (fase 0):
    - correr `p_ganar_torneo.py` con la σ realizada del momento y con el rival re-estimado;
    - comprobar en la app de GBM que se pueden comprar SPXL, TQQQ y QQQM/SPYM en el SIC y si piden algún perfil o carta. TQQQ, SPXL, SOXL y QLD ya están confirmados como listados y activos en la BMV; UPRO y SSO no [43][46];
    - medir el spread real de cada ETF.

---

## No verificado (resumen)

- Magnitud exacta (razón de volatilidades) del efecto en Brown-Harlow-Starks (1996).
- Tamaño de muestra y periodo de Busse (2001).
- El 0.45% mensual atribuido a George-Hwang (2004). Viene de una cita secundaria.
- Backtest original de GEM (CAGR 17.4%, máxima caída −22%, Sharpe 0.9), los +440 pb de Antonacci desde 1950 y la tabla fuera de muestra de quant4free (el periodo y los 30 cambios no cuadran; menciona whipsaw en 2011, antes de su periodo 2014–2026).
- El t = 9.69 de Jacobsen-Zhang y el "56 LETFs desde 2008" de Avellaneda-Zhang.
- Que el TOM se cumpla también en 1987–2005.
- Si Gayed-Bilello descuentan el costo de financiamiento de los LETF simulados además del 1% anual.
- Resultados por modelo en la temporada 1.5 de Alpha Arena, salvo el +12.11% de Grok 4.20 (otras fuentes: +9.3% a +10.6%). Incluye la mejor instancia (+46.98% o +34.59%) y el uso del "firehose" de X.
- El apalancamiento promedio de 18x y las 158 órdenes de Grok 4 en S1 (los datos horarios de la API los contradicen).
- Fechas de Grok 4.6 y 4.7: solo fuentes secundarias (varias, coincidentes).
- Que GBM permita comprar LETFs de EUA desde la app (pendiente en A1 y A2).
- Si SH, UPRO y SSO están en el SIC.
- Las condiciones de la venta en corto en GBM (el "mínimo de 10,000 MXN" parece ser un ejemplo).

---

## Fuentes

1. Brown, K., Harlow, W. y Starks, L. (1996). "Of Tournaments and Temptations: An Analysis of Managerial Incentives in the Mutual Fund Industry". *Journal of Finance* 51(1):85–110. https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1996.tb05203.x — resumen SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7460 (consultado el 25-sep-2026).
2. Chevalier, J. y Ellison, G. (1997). "Risk Taking by Mutual Funds as a Response to Incentives". *JPE* 105(6):1167–1200. https://ideas.repec.org/a/ucp/jpolec/v105y1997i6p1167-1200.html ; https://papers.ssrn.com/sol3/papers.cfm?abstract_id=225298
3. Busse, J. (2001). "Another Look at Mutual Fund Tournaments". *JFQA* 36(1):53–73. https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/another-look-at-mutual-fundtournaments/CD3356D7C7EDDC18D960CEF90CA7D84F (resumen verificado el 25-sep-2026) ; https://papers.ssrn.com/sol3/papers.cfm?abstract_id=110028 ; descripción de sus resultados en "Yet another look at mutual fund tournaments": https://www.sciencedirect.com/science/article/abs/pii/S092753980400026X
4. Kempf, A. y Ruenzi, S. (2008). "Tournaments in Mutual-Fund Families". *RFS* 21(2):1013–1036. https://academic.oup.com/rfs/article-abstract/21/2/1013/1604978 ; versión de trabajo: https://www.ssrn.com/abstract=322421 (hallazgo de familias grandes contra chicas tomado del resumen, vía búsqueda del 25-sep-2026)
5. Taylor, J. (2003). "Risk-taking behavior in mutual fund tournaments". *JEBO* 50(3):373–383. https://www.researchgate.net/publication/222735303_Risk-taking_behavior_in_mutual_fund_tournaments
6. Seel, C. y Strack, P. (2013). "Gambling in contests". *JET* 148(5):2033–2048. https://econpapers.repec.org/article/eeejetheo/v_3a148_3ay_3a2013_3ai_3a5_3ap_3a2033-2048.htm
7. Browne, S. (1999). "Beating a moving target: Optimal portfolio strategies for outperforming a stochastic benchmark". *Finance and Stochastics* 3:275–294. https://link.springer.com/article/10.1007/s007800050063
8. Browne, S. (1999). "Reaching Goals by a Deadline: Digital Options and Continuous-Time Active Portfolio Management". *Advances in Applied Probability* 31(2):551–577 (datos de publicación verificados el 25-sep-2026; versión de trabajo de 1997). https://doi.org/10.2139/ssrn.703 ; https://www.semanticscholar.org/paper/Reaching-Goals-by-a-Deadline:-Digital-Options-and-Browne/589eb76f3a04bfd8c3f81a0ff805c0acbc5ef302
9. Browne, S. (2000). "Stochastic Differential Portfolio Games". *Journal of Applied Probability* 37(1). PDF: https://business.columbia.edu/sites/default/files-efs/pubfiles/6339/Jap_9348.pdf (texto verificado el 25-sep-2026).
10. MacLean, L., Thorp, E. y Ziemba, W. *The Kelly Capital Growth Investment Criterion: Theory and Practice*. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1797366 ; Thorp, simulaciones: http://www.edwardothorp.com/wp-content/uploads/2016/11/KellySimulationsNew.pdf
11. Nof1. "Exploring the Limits of Large Language Models (LLMs) as Quant Traders in Live Markets" (oct-2025). https://nof1.ai/blog/TechPost1 — leído en la copia de archivo: https://web.archive.org/web/20251028041142/https://nof1.ai/blog/TechPost1
12. ForkLog (4-nov-2025). "Four Out of Six AI Models Suffer Losses in Trading Tournament". https://forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/ — **sus valores finales de Claude, Gemini, Grok 4 y GPT-5 no coinciden con la API de Nof1 [44]; no usar para cifras.**
13. Blockhead (21-oct-2025). "AI Models Battle in Live Crypto Trading Competition". https://www.blockhead.co/2025/10/21/ai-models-battle-in-live-crypto-trading-competition/
14. iWeaver (4-ago-2026). "Alpha Arena Season 1 Results: Final Ranking and Lessons". https://www.iweaver.ai/blog/alpha-arena-ai-trading-season-1-results/
15. aiHola (9-dic-2025). "Grok 4.20 Beats Top AI Models in Live Stock Trading Contest". https://aihola.com/article/grok-wins-alpha-arena-trading
16. ForkLog (8-dic-2025). "AI Model Grok 4.2 Triumphs in Trading Tournament". https://forklog.com/en/ai-model-grok-4-2-triumphs-in-trading-tournament/
17. Benzinga vía Yahoo Finance (18-ene-2026). "Elon Musk's Grok 4.20 Beats OpenAI, Google Models In Live Stock Trading Contest". https://finance.yahoo.com/news/elon-musks-grok-4-20-123855766.html
18. OneDayAdvisor (16-ene-2026). "NoF1.ai Alpha Arena Review (Season 1.5)". https://www.onedayadvisor.com/2025/12/nof1ai-alpha-arena-review-season-15.html
19. TradeRank (24-abr-2026, actualizado el 14-sep-2026). "5 Alpha Arena Alternatives for AI Trading (2026)". https://www.traderank.ai/blog/alpha-arena-alternatives-2026 — válido para el estado del leaderboard; su −57.92% de Grok 4 repite el error de [12].
20. Post en X de S.E. Robinson, Jr. (dic-2025) sobre el +46.98% de Grok 4.20 (no verificado). https://x.com/SERobinsonJr/status/1996919327375716677
21. Versiones de Grok (fuentes secundarias): https://www.ai-toolbox.co/grok-models/grok-models-explained-2026 ; https://geotoolbox.ai/blog/grok-5 ; https://evolink.ai/blog/grok-4-7-release-date ; https://llm-stats.com/blog/research/grok-4.6-launch (consultadas el 25-sep-2026).
22. Moskowitz, T., Ooi, Y. y Pedersen, L. (2012). "Time Series Momentum". *JFE* 104(2):228–250. https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf (texto verificado).
23. Jegadeesh, N. y Titman, S. (1993). "Returns to Buying Winners and Selling Losers". *JF* 48(1). https://www.researchgate.net/publication/4992307_Returns_to_Buying_Winners_and_Selling_Losers_Implications_for_Stock_Market_Efficiency
24. George, T. y Hwang, C. (2004). "The 52-Week High and Momentum Investing". *JF* 59:2145–2176. https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2004.00695.x
25. Daniel, K. y Moskowitz, T. (2016). "Momentum Crashes". *JFE* 122(2):221–247. https://www.sciencedirect.com/science/article/pii/S0304405X16301490 ; NBER w20439: https://www.nber.org/papers/w20439
26. Antonacci, G. "Extended Backtest of Global Equities Momentum". https://medium.com/@garyantonacci_30463/extended-backtest-of-global-equities-momentum-dual-momentum-eb12902612e0
    26b. Quant for Free. "Dual Momentum out of sample". https://quant4free.com/analysis/dual-momentum/
27. Gayed, M. y Bilello, C. (2016). "Leverage for the Long Run – A Systematic Approach to Managing Risk and Magnifying Returns in Stocks" (Premio Charles H. Dow 2016). https://docs.cmtassociation.org/dow-award/2016-gayed-bilello.pdf (tablas 6–8 y notas 21–23 verificadas en el PDF el 25-sep-2026).
28. Cheng, M. y Madhavan, A. (2009). "The Dynamics of Leveraged and Inverse Exchange-Traded Funds". https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1539120
29. Avellaneda, M. y Zhang, S. (2010). "Path-Dependence of Leveraged ETF Returns". *SIAM J. Financial Math.* 1(1):586–603 (cita verificada; resumen no leído: SSRN devolvió 403). https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1404708
30. Bouman, S. y Jacobsen, B. (2002). "The Halloween Indicator, 'Sell in May and Go Away': Another Puzzle". *AER* 92(5):1618–1635. https://www.aeaweb.org/articles?id=10.1257%2F000282802762024683
31. Zhang, C. y Jacobsen, B. (2021). "The Halloween Indicator, 'Sell in May and Go Away': Everywhere and All the Time". *Journal of International Money and Finance* 110:102268. Resumen: https://econpapers.repec.org/RePEc:eee:jimfin:v:110:y:2021:i:c:s0261560620302242 (verificado el 25-sep-2026) ; SSRN: https://www.ssrn.com/abstract=2154873
32. McConnell, J. y Xu, W. (2008). "Equity Returns at the Turn of the Month". *FAJ* 64(2):49–64. Resumen: https://ideas.repec.org/a/taf/ufajxx/v64y2008i2p49-64.html (verificado el 25-sep-2026) ; https://business.purdue.edu/faculty/mcconnell/publications/Equity-Returns-at-the-Turn-of-the-Month.pdf
33. Quantpedia. "Turn of the Month in Equity Indexes". https://quantpedia.com/strategies/turn-of-the-month-in-equity-indexes
34. Lucca, D. y Moench, E. (2015). "The Pre-FOMC Announcement Drift". *JF* 70(1). https://www.newyorkfed.org/research/staff_reports/sr512.html
35. Kurov, A., Wolfe, M. y Gilbert, T. (2021). "The disappearing pre-FOMC announcement drift". *Finance Research Letters* 40. https://pmc.ncbi.nlm.nih.gov/articles/PMC7525326/
36. Santa-Clara, P. y Valkanov, R. (2003). "The Presidential Puzzle: Political Cycles and the Stock Market". *JF* 58(5):1841–1872. https://onlinelibrary.wiley.com/doi/abs/10.1111/1540-6261.00590
37. Wong, W. y McAleer, M. (2009). "Mapping the Presidential Election Cycle in US stock markets". *Mathematics and Computers in Simulation* 79(11):3267–3277. https://www.sciencedirect.com/science/article/abs/pii/S0378475409001268
38. Białkowski, J. y Nahavandi, A. (2019). "Midterm Elections' Stock Market Surge: An Unintentional Gift from US Politicians". *Journal of Wealth Management* 21(4):76–84. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3253726 ; https://jwm.pm-research.com/content/21/4/76
39. Yahoo Finance (4-may-2026). "Stocks have never posted a losing year after a midterm election since 1950". https://finance.yahoo.com/markets/stocks/articles/stocks-never-posted-losing-midterm-144711137.html
40. Federal Reserve. Calendario FOMC 2026 (27–28 oct y 8–9 dic). https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
41. Yahoo Finance, históricos del S&P 500 y ETFs (API de gráficas `query1.finance.yahoo.com/v8/finance/chart`, consultada el 25-sep-2026). https://finance.yahoo.com/quote/%5EGSPC/history/
42. Yahoo Finance, históricos del VIX (cierre de 15.67 el 24-sep-2026). https://finance.yahoo.com/quote/%5EVIX/history/
43. Documento interno A1: `/home/user/New1/arena/investigacion/01-gbm-operativa-y-costos.md` (comisiones de GBM, SIC, Trading USA y listado de TQQQ). Comisión de 0.25% + IVA por escalón re-verificada en la FAQ de GBM el 25-sep-2026: https://gbm.com/faqs/que-comisiones-cobran-al-invertir-en-gbm/
44. Nof1, API `account-totals` de Alpha Arena, temporada 1, marca horaria 407 (3-nov-2025 ~22:00 UTC), copia de Wayback Machine del 4-nov-2025 02:23 UTC: https://web.archive.org/web/20251104022344/https://nof1.ai/api/account-totals?lastHourlyMarker=407 (descargada y procesada el 25-sep-2026: equity por modelo, picos, posiciones, cortos y apalancamiento).
45. Post en X de @tetsuoai (dic-2025) con el valor de cuenta promedio de la temporada 1.5 (no verificado). https://x.com/tetsuoai/status/1997198868329431057
46. Documento interno A2: `/home/user/New1/arena/investigacion/02-universo-sic-bmv-agresivo.md` (listado en BMV de SOXL, TQQQ, SPXL, QLD, SQQQ y SOXS; UPRO y SSO no verificados; desviaciones contra el valor justo; granularidad del SIC).
47. CFA Institute, Enterprising Investor (30-oct-2012). "The Halloween Indicator: A Stock Market Anomaly That Is Stronger than Ever" (resume la versión de trabajo de Jacobsen-Zhang: 108 mercados, 55,425 observaciones, 4.52% y 6.25%). https://blogs.cfainstitute.org/investor/2012/10/30/the-halloween-indicator-a-stock-market-anomaly-that-is-stronger-than-ever

---

## Registro de verificacion (2026-09-25)

**Verificador adversarial.** Partí de que había errores. Revisé ~110 afirmaciones contra fuentes primarias cuando fue posible: PDFs de los papers (Gayed-Bilello, Browne 2000, Moskowitz-Ooi-Pedersen, Jacobsen-Zhang versión de trabajo), resúmenes de revista, el blog de Nof1 y la **API de Nof1 archivada en Wayback Machine** (serie horaria completa de la temporada 1, procesada con Python), la FAQ de GBM, el calendario de la Fed y la API de gráficas de Yahoo. También volví a leer `parametros.json`, el código `p_ganar_torneo.py` y su salida, y crucé con A1 y A2.

### Qué se sostiene

| Afirmación | Fuente de la verificación |
|---|---|
| Brown-Harlow-Starks (1996): 334 fondos growth, 1976–1991; perdedores suben la volatilidad; el efecto crece con el tiempo | Resumen en EconPapers [1] |
| Busse (2001) *JFQA* 36(1):53–73: con datos diarios el efecto desaparece; sesgo por autocorrelación en la volatilidad mensual | Resumen en Cambridge Core [3] |
| Taylor (2003) *JEBO* 50(3):373–383: con benchmark endógeno el ganador apuesta | Resumen vía búsqueda [5] |
| Kempf-Ruenzi (2008) *RFS* 21(2):1013–1036 | Resumen vía búsqueda [4] (se agregó el matiz de familias chicas) |
| Browne (1999) *F&S* 3:275–294; Browne (1999) *AAP* 31(2):551–577; Browne (2000) *JAP* 37(1): "correlación imperfecta", "any move by Investor A can be immediately reacted…", equilibrio = crecimiento óptimo en el caso simétrico, el que está en desventaja es más audaz "on the order of the square of … κ" | PDF de Browne (2000) y su bibliografía [9]; búsqueda [8] |
| Moskowitz-Ooi-Pedersen (2012): 58 instrumentos, ene-1965 a dic-2009, Sharpe > 1, ~2.5 veces el del mercado, pérdidas en mar–may 2009 | PDF [22] |
| Jegadeesh-Titman (1993): 6/6 = 12.01% anual compuesto | Búsqueda [23] |
| Gayed-Bilello (2016): tablas 6–8 (9.1%/18.9%/0.30/−86.2%; LRS 2x 19.1%/24.9%/0.51/−78.7%; LRS 3x 26.8%/37.3%/0.47/−92.2%), 5 cambios al año, 1% anual, 49% y 80% de ventanas de 3 años | PDF [27] |
| Cheng-Madhavan (2009): opción dependiente del camino | Búsqueda [28] |
| Bouman-Jacobsen (2002) *AER* 92(5):1618–1635, 36 de 37 países | Búsqueda y PDF de Jacobsen-Zhang [30] |
| McConnell-Xu (2008): TOM de 4 días, 31 de 35 países, 1926–2005 | Resumen en IDEAS/CFA [32] |
| Quantpedia TOM: 7.2%, 6.9%, 1.04, 1926–2005, advertencia de que los efectos de calendario desaparecen o rotan | Página [33] |
| Lucca-Moench: +49 pb en 24 h, sep-1994 a mar-2011, ~80%; Kurov-Wolfe-Gilbert: desaparece después de 2015, muestra a dic-2019 | PMC [35] |
| Santa-Clara-Valkanov: +9% VW y +16% EW con demócratas; no se concentra en elecciones | Búsqueda [36] |
| Wong-McAleer (2009): ciclo de 4 años el más prominente, 1965–2003 | Búsqueda [37] |
| Białkowski-Nahavandi (2019): 9 de 10, ~25% compuesto, 1954–2017; política monetaria y fiscal no lo explican | Búsqueda [38] |
| Yahoo Finance (4-may-2026): 19 de 19 intermedias sin año negativo a 12 meses desde 1950 | Página [39] |
| FOMC 2026: 27–28 oct y 8–9 dic | Fed [40] |
| Elección intermedia: 3-nov-2026 | Regla del primer martes después del primer lunes |
| Nof1 [11]: todas las citas de estilo (cortos, holding, frecuencia, stops, tamaño, 1–2 posiciones de Claude y Qwen, costos dominando el PnL, sensibilidad al prompt, inferencia cada ~2–3 min, mismo prompt, plan de salida con invalidación, fin el 3-nov-2025 17:00 ET) | Texto completo de la copia archivada [11] |
| Temporada 1.5: 19/20-nov a 3-dic-2025, 4 modalidades, 20x máximo, Grok 4.20 +12.11% y 4,844 USD, ganó en las 4 competencias, GPT-5.1 2° y Gemini 3 3°, 320,000 USD en total | aiHola [15], ForkLog [16], Benzinga [17], búsqueda |
| TradeRank: al 6-ago-2026 no hay temporada 2 pública | Página [19] |
| Comisión GBM Trading MX/SIC: 0.25% por escalón de "monto operado promedio de 3 meses" (0.29% con IVA según la Guía citada en A1) | FAQ de GBM [43] |
| TQQQ, SPXL, SOXL, QLD, SQQQ y SOXS listados en la BMV/SIC | A2 [46] (verificado ahí contra BMV) |
| Datos de mercado de la sección 6 (S&P, SPY, QQQ, SMH, VIX, USD/MXN) | Recalculados con la API de Yahoo: coinciden al decimal |
| Aritmética: tabla de Kelly, fórmula y tabla de la carrera de beta, tabla de IR, arrastre de LETF (6.4%/2.1%/2.0%/0.7%), costo de R3 (~9%), error de Monte Carlo (~0.35 pp), P(tocar x) = x^(2/f − 1) | Recalculado |
| Tablas del modelo (bloques 1–6) contra `salida_p_ganar_torneo.txt` | Coinciden |

### Correcciones hechas en el documento

1. **Resultados finales de Alpha Arena S1 (cambia el perfil del rival).** ForkLog [12] y TradeRank [19] daban Claude −42.01%, Gemini −45.55%, **Grok 4 −57.92% (5°)** y GPT-5 −58.74%. La API de Nof1 al cierre da Claude −31.1%, **Grok 4 −45.4% (4°)**, Gemini −56.2% y GPT-5 −62.7%. Claude nunca bajó de 6,345 USD ni Grok 4 de 5,179 USD, así que las cifras de ForkLog no existieron en ningún momento. iWeaver [14] sí coincidía (±0.5 pp). Corregido en el resumen (punto 6), en la tabla de 3.1, en el perfil del rival y en las lecciones.
2. **Foto "del 21-oct":** los valores (+35/+30/+28/−33/−27) coinciden con la API el 20-oct ~21:00 UTC; Blockhead la publicó el 21-oct.
3. **Caída de Grok 4:** decía "+30% → −58%, −68% desde el pico". Dato real: pico de +50.4% (21-oct), final −45.4%; −64% desde el pico y −58% desde la foto del 20-oct. Claude: de +28% a −31% (no −42%).
4. **"4 de 6 perdieron más de 40%"** → 4 de 6 perdieron más de 30%; 3 de ellos más de 45%.
5. **"El ranking del día 3 terminó 2°, 5° y 3°"** → 2°, 4° y 3°.
6. **"18x de apalancamiento promedio de Grok 4" y "1,418 órdenes de Qwen":** contradichos por la API (Grok 4: 12x medio y 10x mediano; Qwen: ~33 posiciones observadas).
7. **Estilo de Grok:** la "menor actividad" es de las corridas previas; en vivo quedó 3° de 6 en posiciones. El sesgo corto se confirma (17 de 52 posiciones). Agregué la tabla de posiciones por modelo.
8. **Temporada 1.5:** el +12.11% se mantiene, pero otras fuentes dan +9.3% a +10.6%.
9. **Browne, "Reaching goals by a deadline":** ya no es no verificado: *AAP* 31(2):551–577 (1999).
10. **Browne (2000):** agregué que el modelo supone revelación perfecta; en la arena solo hay marcador semanal.
11. **Kempf-Ruenzi:** agregué que en familias chicas los ganadores suben más el riesgo que los perdedores. Refuerza la lectura de Taylor para un 1 vs 1.
12. **Busse (2001):** el "230 fondos, 1985–1995" no aparece en el resumen; quedó como no verificado y agregué volumen y páginas.
13. **Halloween:** 55,425 observaciones, +4.52% y +6.25% son de la versión de trabajo de 2012 [47]. La versión publicada (*JIMF* 110, 2021) dice 62,962 observaciones y ~4%. El t = 9.69 no lo pude verificar.
14. **TOM:** decía "1897–2005" y "también 1987–2005". McConnell-Xu es 1926–2005; el 1897–1986 viene de literatura previa citada por Quantpedia.
15. **Gayed-Bilello:** el 49% es sin apalancar y es el promedio de MAs de 10 a 200 días (nota 21). Agregué la advertencia de que el paper no menciona un costo de financiamiento aparte del 1% (no verificado).
16. **Antonacci (+440 pb) y Avellaneda-Zhang ("56 LETFs desde 2008"):** marcados como no verificados.
17. **Sección 6:** la nota de "volatilidades ruidosas" era falsa. Las de los LETF son exactamente L × σ del subyacente.
18. **Instrumentos en GBM:** UPRO y SSO no están verificados en el SIC; se reemplazaron por SPXL (y QLD, que casi no opera). SH tampoco está verificado; SQQQ y SOXS sí están listados. Agregué que el 1x debe ir en QQQM/SPYM por la granularidad (1 título de QQQ/SPY = 66–68% de la cuenta).
19. **Venta en corto en GBM:** el "mínimo de 10,000 MXN" aparece como ejemplo en el resumen de la FAQ, no como regla; quedó como no verificado.
20. **Costos del modelo:** el spread de 0.10% es optimista para los LETF del SIC (A2 midió 0.17% en TQQQ/SPXL y 0.41% en QLD).
21. **Compatibilidad con el perfil (cambia decisiones):** el documento decía que el arquetipo A con modo torneo "es compatible con el perfil provisional". No lo es: el escalón a 3x y copiar a un rival 3x exceden `etf_apalancado_max` = 0.5 (tope real ~2x). Además, ~2x es Kelly completo con μ_e = 8%, el doble de `kelly_fraccion_max` = 0.5. El `filtro_apalancados` vigente vende al cruzar la SMA200 (sin banda), así que la banda de 3% requiere cambiar el perfil.
22. **Límites del Monte Carlo:** revisé el código. No modela los cortacircuitos (−12/−20/−28/−35) ni el filtro de VIX. El P(< −35%) probablemente sobreestima la ruina de las estrategias con LETF.
23. **Lectura del modelo:** "entre 52% y 64%" → 51% a 64% (C4 = 51.1%). "La banda recupera la mayor parte" → recupera 2.6–2.7 pp (40%–60% de lo perdido). "C1 igual o mejor que C8" → mejor en A y 0.6 pp peor en B.
24. **Fuentes:** marqué [12] y [19] como no confiables para cifras. Agregué [44] (API de Nof1), [45], [46] (A2) y [47], y completé volumen y páginas de [3], [8], [31], [32] y [38].

### No pude verificar (sigue marcado)

- MacLean-Thorp-Ziemba y George-Hwang (2004): hoy no releí sus resúmenes. Solo sostienen lecturas cualitativas; el 0.45% mensual de George-Hwang sigue marcado. (Chevalier-Ellison *JPE* 105(6):1167–1200, 1982–92, septiembre y diciembre; Seel-Strack *JET* 148(5):2033–2048; y Daniel-Moskowitz *JFE* 122(2):221–247, "panic states": sí verificados vía IDEAS/EconPapers el 25-sep-2026.)
- Resultados por modelo de la temporada 1.5: la API archivada no tiene capturas de dic-2025.
- Que GBM permita comprar los LETF desde la app y con qué perfil. Las condiciones reales del corto.
- El resumen de "No verificado" de arriba ya incluye todos estos puntos.

### Inconsistencia fuera de este documento

- `parametros.json` → `rivales.capital_inicial_mxn` = 20000 y `metrica_competencia` = "igual capital para todos", pero `arena-grok` tiene 15,000 MXN. El TWR en % no depende del capital, salvo por los costos fijos y la granularidad del SIC (sección 4), que perjudican más al rival.

### Veredicto

La teoría de torneos y las matemáticas del documento se sostienen. Los datos de Alpha Arena S1 estaban mal y se corrigieron con datos primarios: Grok 4 perdió 45%, no 58%, y quedó 4°. La lección de fondo no cambia: los líderes tempranos apalancados se derrumbaron. **El hallazgo que más cambia decisiones:** el plan recomendado (C9, modo torneo con escalón a 3x) no cabe en el perfil provisional (`etf_apalancado_max` 0.5, `kelly_fraccion_max` 0.5, filtro sin banda), y su Monte Carlo no incluye los cortacircuitos. Antes de adoptarlo hay que decidir si cambia el perfil o se recorta el modo torneo a ~2x, y volver a correr el modelo con esa regla. Con el perfil actual, C11 (1x → 2x si vamos atrás; 59.1% / 57.7%) es la variante más cercana a lo que se puede ejecutar tal como se simuló.
