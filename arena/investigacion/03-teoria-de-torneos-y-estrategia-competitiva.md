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

1. **[H] La teoría de torneos predice que quien va atrás apuesta más.** Brown-Harlow-Starks (1996) y Chevalier-Ellison (1997) lo encontraron en fondos mutuos [1][2]. Busse (2001) lo refutó con datos diarios [3]. Taylor (2003) mostró que, en un juego estratégico, **el que va adelante también sube su riesgo para "cubrir" al rival** [5].
2. **[H] Browne (2000) resolvió el duelo entre dos inversionistas.** Si ninguno tiene ventaja, la estrategia de equilibrio es la de crecimiento óptimo (Kelly). El que está en desventaja debe ser más audaz. **Si los dos invierten en lo mismo, el juego es trivial: cada movimiento se puede copiar** [9].
3. **[I, modelo] En una carrera de beta pura, apalancarse más que el rival te da ~50%, no más.** Con k_claude > k_rival, P(ganar) = Φ(√T·(μ_e − (k_c + k_r)σ²/2)/σ). Esa probabilidad **no crece con la diferencia de exposición**: depende de que el mercado suba. Con μ_e = 8% y σ = 20%, sale entre 47% y 54%.
4. **[I, modelo] Lo que mueve la probabilidad es la razón de información (IR) de la diferencia, no el nivel de riesgo.** P ≈ Φ(IR·√0.5): IR 0.25 da 57%, IR 0.5 da 64% e IR 1.0 da 76%. Sin ventaja real, el techo realista contra un rival típico es de **55% a 60%**.
5. **[I, modelo] Estrategia según el marcador.** A mitad de temporada, con +5 pp de ventaja, P(ganar) = 98% si el tracking error contra el rival es de 5%, y baja a 71% si es de 20%. Con −5 pp, es 3% con TE de 5% y 40% con TE de 40%. **"Bajar varianza" cuando vas adelante significa bajar la varianza RELATIVA al rival, es decir, copiar su beta. Irse a efectivo no es bajar varianza.**
6. **[H] Alpha Arena, temporada 1 (cripto, 18-oct a 3-nov-2025).** Qwen3 Max +22.31%, DeepSeek +4.89%, Claude Sonnet 4.5 −42.01%, Gemini 2.5 Pro −45.55%, **Grok 4 −57.92%** y GPT-5 −58.74% [12]. **El 21-oct Grok 4 iba +30% y Claude +28%** [13]: los líderes tempranos apalancados se derrumbaron.
7. **[H] Estilo documentado de Grok 4:** es de los que más shortean, tiene los holdings más largos, opera menos que los demás y pone los stops más holgados [11]. **Grok 4.20 ganó la temporada 1.5 (acciones de EUA) con +12.11% agregado** y ganó dinero en las cuatro modalidades [15][16]. Desde dic-2025 no ha habido temporadas públicas nuevas [19].
8. **[H] Estrategias candidatas.** Las de mejor evidencia son el momentum de series de tiempo (grado A) y la rotación apalancada con SMA200 (grado B; Sharpe de 0.51 contra 0.30 del buy & hold en 1928–2015 [27]). También tienen evidencia la estacionalidad nov–abr (grado B; +4.52% en 319 años [31]) y el efecto post-intermedias (grado C; ~+25% compuesto en el 4T de las intermedias más los dos trimestres siguientes, 1954–2017 [38]). **La temporada cae justo en esa ventana.** La deriva pre-FOMC ya desapareció (grado D) [35].
9. **[I, Monte Carlo] Contra una mezcla de rivales "tipo Grok"**, la probabilidad de ganar (primer valor: régimen A de estrés corto; segundo valor: régimen B bajista persistente) queda así:
   - tendencia + apalancado (2x, filtro SMA200 con banda de 3%): **54% / 57%**, con P(pérdida > 35%) de ~1%;
   - momentum concentrado: 53–58%, según el alfa que se suponga;
   - barbell: 53% / 54%, con ~0% de ruina;
   - la misma tendencia + apalancado con **modo torneo a mitad de temporada: 58% / 60%**.
10. **[R] Plan base:** 2x efectivo sobre renta variable de EUA de gran capitalización, con filtro SMA200 + banda de 3% + VIX < 25. El 3x se reserva para cuando vayamos atrás ≥5 pp, y se estima la beta del rival con sus reportes semanales. **El error que más cuesta es el sobretrading.** Un rival que rota cada semana sin ventaja pierde de 5% a 9% por comisiones en la temporada, y contra él ganamos del 70% al 87% de las veces.

---

## 1. Teoría de torneos: qué dice la evidencia en fondos

| Estudio | Muestra | Hallazgo | Tamaño / robustez | Lectura para la arena |
|---|---|---|---|---|
| Brown, Harlow y Starks (1996), *JF* 51:85–110 [1] | 334 fondos growth, 1976–1991 | Los perdedores de mitad de año suben la volatilidad del fondo en la segunda mitad más que los ganadores. El efecto crece con los años, a medida que los inversionistas ponen más atención al desempeño | Efecto significativo con datos mensuales (la magnitud exacta de la razón de volatilidades: no verificado) | [I] El rival que vaya atrás en el reporte de mitad de temporada tenderá a subir el riesgo |
| Chevalier y Ellison (1997), *JPE* 105(6):1167–1200 [2] | Fondos growth y growth & income, 1982–1992; carteras de septiembre y diciembre | La relación flujo-desempeño es convexa. Eso crea incentivos a cambiar el riesgo según el rendimiento acumulado del año, y **los fondos sí cambian su riesgo entre septiembre y diciembre** en esa dirección | Semiparamétrico. Resultado citado como canónico | [I] Lo que importa es la forma del premio: si solo cuenta ganar, el premio es binario y aumenta el incentivo a apostar |
| Busse (2001), *JFQA* [3] | 230 fondos de acciones de EUA, 1985–1995, **datos diarios** | Con datos diarios **no hay efecto torneo**. El resultado mensual venía de un sesgo por autocorrelación en la estimación de la volatilidad | Refutación metodológica | [I] Buena parte de lo que parecía "apuesta" era ruido de medición. No hay que sobrerreaccionar a la volatilidad aparente del rival con pocos datos |
| Taylor (2003), *JEBO* 50(3):373–383 [5] | Modelo teórico de 2 gestores con un activo riesgoso **perfectamente correlacionado** | Con benchmark exógeno, el que va perdiendo apuesta. En el juego estratégico solo hay equilibrio mixto, **y el líder elige la estrategia riesgosa más seguido que el rezagado** | Teórico | [I] Clave para la arena: si el rival va a apostar y tú vas adelante, **copiar su apuesta preserva tu ventaja**, igual que cuando el velero que va adelante "cubre" al de atrás |
| Kempf y Ruenzi (2008), *RFS* 21(2):1013–1036 [4] | Fondos de acciones de EUA dentro de familias | Los gestores ajustan el riesgo según su posición en la familia, y la dirección depende de la situación competitiva. El efecto es mayor con comisiones altas, un solo gestor y familias grandes | Empírico | [I] El comportamiento depende del marcador y de cuántos rivales haya. En un 1 vs 1 el incentivo es directo |
| Seel y Strack (2013), *JET* 148(5):2033–2048 [6] | Modelo de n jugadores en un concurso donde el ganador se lo lleva todo, con movimiento browniano y quiebra en 0 | Equilibrio de Nash en forma cerrada: los jugadores "apuestan" (arriesgan más de lo que haría un maximizador de valor esperado) | Teórico | [I] En un duelo donde el ganador se lleva todo, lo racional es arriesgar más de lo que conviene para maximizar el patrimonio |
| Browne (1999), *Finance & Stochastics* 3:275–294 [7] | Control estocástico contra un benchmark estocástico | Encuentra la estrategia que maximiza la probabilidad de superar al benchmark por un % dado sin caer debajo de él por otro % | Teórico | [I] La herramienta formal para "ganarle a un objetivo que se mueve" |
| Browne, "Reaching goals by a deadline" (*Adv. Appl. Prob.*; versión de trabajo de 1997) [8] | Maximizar P(llegar a una meta en una fecha fija) | **La política óptima equivale a comprar una opción digital europea.** En general, el activo se sustituye por el portafolio de crecimiento óptimo | Teórico (año y volumen de la versión publicada: no verificados en la fuente primaria) | [I] Replicar una digital deja el patrimonio en la meta o en ~0. Cerca de la fecha límite, la delta explota si vas atrás: "atrás, sube" llevado al extremo |
| Browne (2000), *J. Appl. Prob.* 37(1) [9] | Juego de suma cero entre 2 inversionistas con oportunidades correlacionadas | (a) Hace falta **correlación imperfecta**; con la misma oportunidad, "cualquier movimiento de A puede ser neutralizado por B". (b) En el caso simétrico, el equilibrio **se reduce a la estrategia de crecimiento óptimo** (Kelly). (c) **El jugador en desventaja sigue una estrategia más audaz**, del orden del cuadrado del parámetro de ventaja κ. Esto coincide con el "bold play" de Dubins-Savage | Teórico (verificado en el PDF) | [I] La ventaja la da el precio de mercado del riesgo, es decir, el Sharpe de cada quien. **Sin Sharpe superior, la única forma de ganar es ser distinto y tener suerte** |

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
- [H] La temporada corrió hasta el 3-nov-2025 a las 17:00 ET [11]. El inicio fue el 18-oct-2025 [14][19].

**Resultados finales [H] [12]** (ForkLog, 4-nov-2025):

| Lugar | Modelo | Valor final (USD) | Rendimiento |
|---|---|---|---|
| 1 | Qwen3 Max | 12,231 | **+22.31%** |
| 2 | DeepSeek Chat V3.1 | 10,489 | +4.89% |
| 3 | Claude Sonnet 4.5 | 5,799 | −42.01% |
| 4 | Gemini 2.5 Pro | 5,445 | −45.55% |
| 5 | **Grok 4** | **4,208** | **−57.92%** |
| 6 | GPT-5 | 4,126 | −58.74% |

- [H] Otra fuente (iWeaver, 4-ago-2026) publica cifras distintas para los perdedores: Claude −30.81%, Grok 4 −45.3%, Gemini −56.71% y GPT-5 −62.66% [14]. [I] Probablemente es otra fecha de corte. Uso ForkLog porque se publicó un día después del cierre y coincide con TradeRank, que da Grok 4 −57.92% ≈ 4,208 USD [19].
- [H] **Foto del 21-oct-2025** (día 3–4): DeepSeek +35%, **Grok 4 +30%**, **Claude Sonnet 4.5 +28%**, Gemini −33% y GPT-5 −27%. Esa fuente dice que Grok "ganó dinero en el 100% de las últimas 5 rondas" [13].
- [I] **De +30% a −58%:** Grok 4 perdió ~68% desde su pico en ~2 semanas (1.30 → 0.42). Claude pasó de +28% a −42%.
- [I] La lección para un duelo de 6 meses: **ir adelante temprano con apalancamiento alto y stops holgados no sirve de nada.** Hay que cuidar la ventaja (sección 2.4).

**Comportamiento observado por Nof1 en las corridas previas y el arranque [H] [11]:**
- Sesgo direccional: "**Grok 4, GPT-5 y Gemini 2.5 Pro shortean mucho más seguido** que los demás; Claude Sonnet 4.5 casi nunca shortea."
- Holding: "En nuestras corridas previas al lanzamiento, **Grok 4 tuvo los tiempos de tenencia más largos**."
- Frecuencia: "Gemini 2.5 Pro es el más activo; **Grok 4 típicamente el que menos**."
- Stops: "Qwen 3 usa las distancias de stop y objetivo más estrechas; **Grok 4 y DeepSeek V3.1 típicamente las más holgadas**."
- Tamaño: Qwen 3 abría las posiciones más grandes, a menudo múltiplos de las de GPT-5 y Gemini. Claude y Qwen mantenían 1–2 posiciones a la vez.
- Costos: "Al principio, el PnL estaba dominado por costos de operación"; los agentes sobreoperaban.
- Sensibilidad: hubo alta sensibilidad a cambios mínimos del prompt.
- Cifras que circulan en fuentes secundarias: Grok 4 con "apalancamiento promedio de 18x" y "158 órdenes contra 1,418 de Qwen" **(no verificado)**.

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
- [H] Benzinga (18-ene-2026) reporta ~11,060 USD de equity promedio, que corresponde a +10–12%, y **4 variantes de Grok en los 6 primeros lugares** [17].
- Mejor instancia individual: "+46.98% en Situational Awareness" según un post en X [20], y "máximo +34.59%, mínimo −96.15% entre 32 entradas" según un agregador **(ambos no verificados y contradictorios)**.
- Resultados de otros modelos que circulan en resúmenes: Claude Sonnet 4.5 −32.44%, DeepSeek V3.1 −24.51%, Kimi K2 −25.8%, Grok 4 −53.39% y Qwen3 Max ~−70% **(no verificado)**.
- Algunas notas dicen que Grok usó el "firehose" de X para sus señales **(no verificado; contradice que todos los modelos recibían el mismo input [15])**.

### 3.3 Temporadas posteriores

- [H] Al 6-ago-2026, el leaderboard de nof1.ai era un archivo con series que terminaban el 12-dic-2025. **No había roster ni resultados públicos de una temporada 2** [19] (TradeRank, actualizado el 14-sep-2026).
- No encontré resultados de temporadas de 2026.
- Versiones vigentes de Grok: Grok 4.6 salió el 12-ago-2026 y Grok 4.7 el 21-sep-2026; Grok 5 no ha salido [21] **(no verificado; fuentes secundarias)**.

### 3.4 Lecciones de Alpha Arena para el duelo

1. [I] **La mayoría pierde, y pierde por costos, apalancamiento y salidas.** En S1, 4 de 6 modelos perdieron más de 40% en 16 días [12]. En S1.5, 7 de 8 perdieron en el agregado [15]. El "juego base" contra una IA que sobreopera o se sobreapalanca **se gana no cometiendo esos errores**.
2. [I] **El ranking temprano no predice nada.** La mitad de arriba del día 3 (DeepSeek, Grok, Claude) terminó 2°, 5° y 3° [12][13].
3. [I] **Grok 4.20 ganó en la modalidad con información del ranking**, y en conjunto en todas las modalidades [16][17]. Si el dueño le reporta el marcador a Grok, hay que esperar ajustes de riesgo según ese marcador.
4. [I] Los horizontes de Alpha Arena (2 semanas y apalancamiento de 10–20x) no se parecen a un duelo de 6 meses en GBM. **Lo transferible es el estilo del modelo, no los números.**

---

## 4. Perfil anticipado del rival (`arena-grok`, 15,000 MXN en GBM)

| Rasgo | Evidencia | Expectativa en GBM [I] |
|---|---|---|
| Direccionalidad | Grok 4 shortea más que la media [11] | Puede usar ETFs inversos (SQQQ/SH en SIC o Trading USA) o salirse a efectivo si ve debilidad. El corto directo en GBM exige contrato y un mínimo de 10,000 MXN, según A1 |
| Holding y frecuencia | Grok 4 tuvo los holdings más largos y la menor actividad [11] | Pocas operaciones y posiciones que se mantienen. La ejecución manual del dueño también limita la frecuencia |
| Stops | Grok 4 usa los stops más holgados [11] | Drawdowns profundos antes de salir. **Puede regalar ventajas grandes**, como en S1: +30% → −58% [12][13] |
| Apalancamiento | Alpha Arena lo permitía (8x–20x en los ejemplos de Nof1) [11] | En GBM, apalancamiento vía ETFs 2x/3x (TQQQ, SOXL, UPRO). TQQQ está listado en el SIC según A1 |
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
| **Dual momentum (Antonacci, GEM)** | Backtest original 1974–2013: CAGR ~17.4%, máxima caída de ~−22% y Sharpe de ~0.9 **(no verificado)**. El autor reporta +440 pb al año sobre el S&P 500 desde 1950 [26] | **Fuera de muestra (2014–2026): CAGR de 8.4% contra 13.6% de SPY, Sharpe de 0.70 contra 0.94** [26b] (secundaria) | **C** | Whipsaw en mercados laterales (2011 y 2015–16) [26b] | No como núcleo. A 6 meses, lo más probable es 0–1 cambios de señal |
| **ETFs apalancados + filtro de tendencia (Gayed-Bilello 2016)** | Oct-1928 a oct-2015. S&P 500 buy & hold: 9.1% anual, vol de 18.9%, Sharpe de 0.30 y máxima caída de −86.2%. **LRS 2x: 19.1%, 24.9%, 0.51 y −78.7%.** **LRS 3x: 26.8%, 37.3%, 0.47 y −92.2%.** Unos 5 cambios al año, con costo de apalancamiento de 1% anual [27] | La regla de MA le gana al buy & hold en rendimiento absoluto solo en **49%** de las ventanas móviles de 3 años. El LRS supera al S&P en **80%** de ellas [27] | **B** | Whipsaw. En 6 meses, el filtro **reduce la mediana** si el mercado arranca en tendencia (modelo, sección 7) | Núcleo del arquetipo A, con banda de 3% para reducir whipsaw |
| **Decaimiento de ETFs apalancados** | El rendimiento de un LETF lleva una opción dependiente del camino que destruye valor con volatilidad alta (Cheng-Madhavan 2009) [28]. Fórmula exacta que liga el rendimiento a L veces el del subyacente y a su varianza realizada, probada en 56 LETFs desde 2008 (Avellaneda-Zhang 2010) [29] | Es matemática, no una anomalía | **A** | [I] Arrastre ≈ (L² − L)/2·σ²·T. Con σ realizada de QQQ de 20.6% (sección 6): **3x ≈ 6.4% y 2x ≈ 2.1% en 6 meses**. Con SPY (11.5%): 3x ≈ 2.0% y 2x ≈ 0.7% | Preferir 2x efectivo. El 3x solo en tendencia con VIX bajo, o para alcanzar al rival |
| **Estacionalidad nov–abr ("Halloween")** | Invierno > verano en **36 de 37 países** (Bouman-Jacobsen 2002) [30]. **319 años y 55,425 observaciones: +4.52% (t = 9.69); +6.25% en los últimos 50 años** (Jacobsen-Zhang) [31] | Los autores dicen que el efecto **se está haciendo más fuerte** [31] | **B** | Ninguno propio. Es un sesgo de μ, no una cobertura | [I] La temporada (oct-2026 a abr-2027) cae en la mitad favorable. Sube la probabilidad a priori de μ_e > 0 |
| **Turn-of-the-month (TOM)** | 1897–2005: **todo el rendimiento en exceso ocurrió en los 4 días del TOM** (del último día hábil a +3). También en 1987–2005. Aparece en 31 de 35 países (McConnell-Xu 2008) [32]. Quantpedia: 7.2% anual, vol de 6.9% y Sharpe de 1.04 (1926–2005) [33] | Quantpedia advierte que "los efectos de calendario tienden a desaparecer o a rotar" [33] | **B** como efecto; **C** como estrategia en GBM | Bajo | [I] Con 0.58% por vuelta (A1) no conviene operarlo solo. **Úsalo para el timing**: compra antes del cierre de mes y vende después del día +3 |
| **Deriva pre-FOMC** | **+49 pb en las 24 h previas** al FOMC, sep-1994 a mar-2011; ~80% del exceso anual (Lucca-Moench 2015) [34] | **"Esencialmente desapareció después de 2015"** en la muestra hasta dic-2019 (Kurov-Wolfe-Gilbert 2021) [35] | **D** | — | No usar. Fechas relevantes: FOMC del 27–28 oct y del 8–9 dic de 2026 [40] |
| **Ciclo presidencial / intermedias** | El exceso de rendimiento es mayor con presidentes demócratas (+9% VW, +16% EW) y **no se concentra alrededor de las elecciones** (Santa-Clara-Valkanov 2003) [36]. El ciclo de 4 años es el más prominente en 1965–2003 (Wong-McAleer 2009) [37]. **Post-intermedias: el S&P 500 fue positivo 9 de cada 10 veces en el 4T del año de intermedias y los dos trimestres siguientes, ~+25% compuesto, 1954–2017** (Białkowski-Nahavandi 2019) [38]. Sin rendimiento negativo a 12 meses tras una intermedia desde 1950 (19 de 19) [39] (secundaria) | Muestra pequeña (~16 intermedias en 1954–2017). La política monetaria y la fiscal no lo explican [38] | **C** | Sin cola propia. Riesgo de sobreajuste de narrativa | [I] Elección intermedia: **martes 3-nov-2026** (primer martes después del primer lunes de noviembre). Coincide casi exacto con la temporada. Refuerza no estar corto ni en efectivo "por defecto" |
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
- [I] Algunas volatilidades calculadas (por ejemplo, la de QLD contra la de QQQ) sugieren datos ruidosos en la fuente. Hay que verificarlas antes de usarlas para dimensionar.

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
| Costos | Comisión GBM 0.29% por lado + 0.10% de spread = **0.39% por lado**. ETF apalancado: 1% anual. ETF 1x: 0.1% anual | A1 [43]. El 1% de apalancamiento es el supuesto de Gayed-Bilello [27] |
| ETFs apalancados | Reinicio diario: V_{t+1} = V_t·(1 + L·r_t − f) | Así funcionan los LETF [28][29] |
| Rivales | R1 concentrado (beta 1.3 + ruido idiosincrático de 30%). R2 3x comprar y mantener. R3 "trader sin ventaja" (cada semana elige al azar 0x, 1x o 2x y paga comisiones). R4 conservador (0.6x) | R1 y R2 son el estilo esperado de Grok (sección 4). R3 es el sobretrading que se vio en Alpha Arena [11]. R4 es un control |
| "Rival tipo Grok" | Mezcla de 40% R1, 25% R2, 20% R3 y 15% R4 | Supuesto mío, basado en la sección 4 |
| Momentum concentrado | Beta 1.3 + ruido de 20% + alfa de 4% anual (C7) o de 0% (C7b) | El 4% es un recorte fuerte al ~12% anual de JT [23], por decaimiento, solo largos y costos. C7b es el caso sin ventaja |
| Modo torneo (C9) | Igual que C8 hasta el día 63. Si va atrás ≥5% → 3x con el mismo filtro. Si va adelante ≥5% → copia la beta del rival, sin filtro | **Optimista:** supone que se conoce la beta del rival. En la práctica se estima con ruido (sección 4) |
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
    # ... estrategias C0..C8, rivales R1..R4 y C9 por rival (ver archivo) ...
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
            # R3 cambia exposicion semanal al azar, C9 decide modo en d == 63 segun ventaja vs cada rival
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

Medianas de los rivales:
- Régimen A: R1 2.6%, R2 10.4%, R3 **−5.0%** y R4 2.9%.
- Régimen B: R1 5.7%, R2 20.7%, R3 −2.5% y R4 4.3%.

**Cómo leer el modelo [I]:**
1. **Todas las estrategias sensatas quedan entre 52% y 64%** contra la mezcla de rivales. El modelo no tiene una estrategia que "gane seguro".
2. **Contra el mismo instrumento (C3 vs R2) es un volado exacto (50%).** Esto confirma a Browne [9]: sin diferenciación no hay ventaja.
3. **El filtro SMA200 sin banda (C4) le quita de 4 a 7 pp de probabilidad al 2x comprar-mantener** en un horizonte de 6 meses que arranca en tendencia, por el whipsaw. **La banda de 3% (C8) recupera la mayor parte y deja el riesgo de ruina en 0.6–1.4%**, contra 4.6–5.7% del 2x sin filtro.
   - Esto es coherente con Gayed-Bilello: la regla solo gana en términos absolutos en 49% de las ventanas de 3 años. Su valor está en la cola [27].
4. **El modo torneo (C9) agrega de +2.5 a +4 pp sobre C8** (57.7% y 59.8%). Es la mejor combinación de probabilidad y ruina del modelo, pero supone que se conoce la beta del rival.
5. **3x comprar y mantener (C3) tiene la probabilidad más alta en el régimen B (64.3%), pero con P(< −35%) de 8.5–12.1%.** Viola el límite `etf_apalancado_max` = 0.5 del perfil y dispararía el cortacircuitos de −35%.
6. **El sobretrading es el peor error.** Contra R3, cualquier estrategia con exposición gana del 67% al 88% de las veces. R3 pierde de 5% a 9% solo en comisiones: 26 semanas × 2/3 de probabilidad de cambio × ~1.33 lados × 0.39% ≈ 9%.

---

## 8. Tres arquetipos para la temporada

| Arquetipo | Implementación en GBM [R] | Exposición efectiva | P(ganar) vs "rival tipo Grok" (régimen A / B) | P(< −35%) | Supuestos clave |
|---|---|---|---|---|---|
| **A. Tendencia + apalancado** (base) | 50% en ETF 3x (UPRO o TQQQ) + 50% en ETF 1x (SPY/QQQ o su equivalente en SIC). Otra opción es 100% en un 2x (SSO/QLD), si el perfil sube el límite de apalancados. Filtro: subyacente arriba de SMA200 **con banda de 3% para salir** y VIX < 25. Con modo torneo a mitad de temporada | ~2x (≈ Kelly con μ_e = 8% y σ = 20%) | **53.8% / 57.3%** sin modo torneo; **57.7% / 59.8%** con modo torneo | 0.6–1.4% (hasta 1.9–3.2% con modo torneo) | μ_e > 0 en la temporada (apoyado por nov–abr [31] e intermedias [38]). Decaimiento del LETF con la σ actual (~2–6% en 6 meses). Arranque en calma |
| **B. Momentum concentrado** | 3–5 ETFs sectoriales o acciones líderes con momentum 12-1 positivo y a ≤5% de su máximo de 52 semanas, revisión mensual (≤ 8 operaciones al mes). Se apaga en estado de pánico [25] | ~1.3x por la beta de los líderes | **52.8–57.6% / 52.8–56.3%**, según el alfa (0–4%) | 2.0–3.1% | La ventaja depende de que el momentum siga vivo en líderes de IA/semis (SMH +73% en 12-1). Riesgo de rotación. **Se parece a lo que probablemente hará el rival**, así que baja la diferenciación |
| **C. Barbell** | 60% en CETES/efectivo + 40% en ETF 3x con filtro. El efectivo es munición para subir la exposición si vamos atrás | ~1.2x cuando el filtro está dentro | **52.8% / 54.1%** | **0.0%** | Pierde contra rivales con beta > 1 en mercados alcistas (R2: 24–33%). Su valor es la opcionalidad para el modo torneo y el desempate (menor máxima caída) |

**Probabilidad estimada contra un rival típico [I]:** A ≈ 54–60% (con modo torneo), B ≈ 53–58% y C ≈ 53–54%.

Rangos y supuestos [I]:
- Los rangos combinan los dos regímenes y la mezcla supuesta de rivales. Los supuestos principales son μ_e ≈ 8% anual incondicional, σ ≈ 18–21% y el arranque en calma (sección 7.1).
- Si la temporada resulta alcista (μ_e ≈ 20%), todas las estrategias con exposición ≥ 1.5x suben a ~60–65%.
- Si resulta bajista (μ_e ≈ −10%), el filtro y el barbell pasan a ser los mejores (bloque 1).
- **No simulé** la mejora por habilidad en la selección (IR > 0). Cada 0.25 de IR suma ~7 pp (sección 2.3).

---

## Implicaciones para la cuenta arena

1. **[R] Arquetipo base: A (tendencia + apalancado ~2x con banda de 3%) con modo torneo.**
   - Es el mejor equilibrio del modelo entre probabilidad (54–60%) y ruina (≤ 3%). Es compatible con el perfil provisional: `etf_apalancado_max` 0.5 y los cortacircuitos −12/−20/−28/−35.
   - El 3x completo (C3/C5) solo se usa como herramienta para alcanzar al rival, no como punto de partida.
2. **[R] Corregir el sentido del `modo_torneo` en `parametros.json`.** Donde dice "Adelante del mejor rival: reducir varianza" debe decir **"reducir el tracking error contra el rival (acercarse a su beta estimada)"**. Irse a efectivo cuando el rival está apalancado **aumenta** el riesgo de perder la ventaja (tabla 2.4; Taylor [5]).
3. **[R] Instrumentar el marcador.**
   - El dueño registra en `competencia/rivales.csv` el valor de `arena-grok` cada viernes al cierre, con la fecha y la hora.
   - Con eso se estima la β̂ del rival contra QQQ, SPY y NAFTRAC en MXN, con una ventana de 6–8 semanas (sección 4).
   - El marcador se lleva en log-puntos, con ajuste por aportaciones (TWR).
4. **[R] Regla de mitad de temporada** (enero de 2027, ~día 63):
   - atrás ≥ 5 pp → subir a ~3x efectivo en la parte de LETF, manteniendo el filtro;
   - adelante ≥ 5 pp → copiar la β̂ del rival (sin irse a efectivo);
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
9. **[R] Estado de pánico = no hay momentum.** Si el S&P cae más de 15% desde su máximo y el VIX supera 30, se desmonta cualquier sesgo de momentum transversal (Daniel-Moskowitz [25]). Quedan beta de índice y efectivo, y se reevalúa con el marcador.
10. **[R] Qué validar en papel antes de operar** (fase 0):
    - correr `p_ganar_torneo.py` con la σ realizada del momento y con el rival re-estimado;
    - comprobar en la app de GBM que se pueden comprar UPRO, TQQQ, SSO y QLD en el SIC (pendiente en A1);
    - medir el spread real de cada ETF.

---

## No verificado (resumen)

- Magnitud exacta (razón de volatilidades) del efecto en Brown-Harlow-Starks (1996).
- Año, volumen y páginas de la versión publicada de Browne, "Reaching goals by a deadline". El paper consultado es la versión de trabajo de 1997.
- El 0.45% mensual atribuido a George-Hwang (2004). Viene de una cita secundaria.
- Backtest original de GEM (CAGR 17.4%, máxima caída −22%, Sharpe 0.9) y la tabla fuera de muestra de quant4free (el periodo y los 30 cambios no cuadran).
- Resultados por modelo en la temporada 1.5 de Alpha Arena, salvo el +12.11% de Grok 4.20. Incluye la mejor instancia (+46.98% o +34.59%) y el uso del "firehose" de X.
- El apalancamiento promedio de 18x y las 158 órdenes de Grok 4 en S1.
- Versiones vigentes de Grok (4.6 y 4.7) y sus fechas de lanzamiento.
- Algunas volatilidades realizadas calculadas con datos de Yahoo (QLD, TQQQ, SMH) que parecen ruidosas.
- Que GBM permita comprar LETFs de EUA desde la app (pendiente en A1).

---

## Fuentes

1. Brown, K., Harlow, W. y Starks, L. (1996). "Of Tournaments and Temptations: An Analysis of Managerial Incentives in the Mutual Fund Industry". *Journal of Finance* 51(1):85–110. https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1996.tb05203.x — resumen SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7460 (consultado el 25-sep-2026).
2. Chevalier, J. y Ellison, G. (1997). "Risk Taking by Mutual Funds as a Response to Incentives". *JPE* 105(6):1167–1200. https://ideas.repec.org/a/ucp/jpolec/v105y1997i6p1167-1200.html ; https://papers.ssrn.com/sol3/papers.cfm?abstract_id=225298
3. Busse, J. (2001). "Another Look at Mutual Fund Tournaments". *JFQA*. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=110028 ; descripción de sus resultados en "Yet another look at mutual fund tournaments": https://www.sciencedirect.com/science/article/abs/pii/S092753980400026X
4. Kempf, A. y Ruenzi, S. (2008). "Tournaments in Mutual-Fund Families". *RFS* 21(2):1013–1036. https://academic.oup.com/rfs/article-abstract/21/2/1013/1604978
5. Taylor, J. (2003). "Risk-taking behavior in mutual fund tournaments". *JEBO* 50(3):373–383. https://www.researchgate.net/publication/222735303_Risk-taking_behavior_in_mutual_fund_tournaments
6. Seel, C. y Strack, P. (2013). "Gambling in contests". *JET* 148(5):2033–2048. https://econpapers.repec.org/article/eeejetheo/v_3a148_3ay_3a2013_3ai_3a5_3ap_3a2033-2048.htm
7. Browne, S. (1999). "Beating a moving target: Optimal portfolio strategies for outperforming a stochastic benchmark". *Finance and Stochastics* 3:275–294. https://link.springer.com/article/10.1007/s007800050063
8. Browne, S. "Reaching Goals by a Deadline: Digital Options and Continuous-Time Active Portfolio Management" (*Advances in Applied Probability*; versión de trabajo de 1997). https://doi.org/10.2139/ssrn.703 ; https://www.semanticscholar.org/paper/Reaching-Goals-by-a-Deadline:-Digital-Options-and-Browne/589eb76f3a04bfd8c3f81a0ff805c0acbc5ef302
9. Browne, S. (2000). "Stochastic Differential Portfolio Games". *Journal of Applied Probability* 37(1). PDF: https://business.columbia.edu/sites/default/files-efs/pubfiles/6339/Jap_9348.pdf (texto verificado el 25-sep-2026).
10. MacLean, L., Thorp, E. y Ziemba, W. *The Kelly Capital Growth Investment Criterion: Theory and Practice*. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1797366 ; Thorp, simulaciones: http://www.edwardothorp.com/wp-content/uploads/2016/11/KellySimulationsNew.pdf
11. Nof1. "Exploring the Limits of Large Language Models (LLMs) as Quant Traders in Live Markets" (oct-2025). https://nof1.ai/blog/TechPost1 — leído en la copia de archivo: https://web.archive.org/web/20251028041142/https://nof1.ai/blog/TechPost1
12. ForkLog (4-nov-2025). "Four Out of Six AI Models Suffer Losses in Trading Tournament". https://forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/
13. Blockhead (21-oct-2025). "AI Models Battle in Live Crypto Trading Competition". https://www.blockhead.co/2025/10/21/ai-models-battle-in-live-crypto-trading-competition/
14. iWeaver (4-ago-2026). "Alpha Arena Season 1 Results: Final Ranking and Lessons". https://www.iweaver.ai/blog/alpha-arena-ai-trading-season-1-results/
15. aiHola (9-dic-2025). "Grok 4.20 Beats Top AI Models in Live Stock Trading Contest". https://aihola.com/article/grok-wins-alpha-arena-trading
16. ForkLog (8-dic-2025). "AI Model Grok 4.2 Triumphs in Trading Tournament". https://forklog.com/en/ai-model-grok-4-2-triumphs-in-trading-tournament/
17. Benzinga vía Yahoo Finance (18-ene-2026). "Elon Musk's Grok 4.20 Beats OpenAI, Google Models In Live Stock Trading Contest". https://finance.yahoo.com/news/elon-musks-grok-4-20-123855766.html
18. OneDayAdvisor (16-ene-2026). "NoF1.ai Alpha Arena Review (Season 1.5)". https://www.onedayadvisor.com/2025/12/nof1ai-alpha-arena-review-season-15.html
19. TradeRank (24-abr-2026, actualizado el 14-sep-2026). "5 Alpha Arena Alternatives for AI Trading (2026)". https://www.traderank.ai/blog/alpha-arena-alternatives-2026
20. Post en X de S.E. Robinson, Jr. (dic-2025) sobre el +46.98% de Grok 4.20 (no verificado). https://x.com/SERobinsonJr/status/1996919327375716677
21. Versiones de Grok (no verificado): https://www.ai-toolbox.co/grok-models/grok-models-explained-2026 ; https://geotoolbox.ai/blog/grok-5
22. Moskowitz, T., Ooi, Y. y Pedersen, L. (2012). "Time Series Momentum". *JFE* 104(2):228–250. https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf (texto verificado).
23. Jegadeesh, N. y Titman, S. (1993). "Returns to Buying Winners and Selling Losers". *JF* 48(1). https://www.researchgate.net/publication/4992307_Returns_to_Buying_Winners_and_Selling_Losers_Implications_for_Stock_Market_Efficiency
24. George, T. y Hwang, C. (2004). "The 52-Week High and Momentum Investing". *JF* 59:2145–2176. https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2004.00695.x
25. Daniel, K. y Moskowitz, T. (2016). "Momentum Crashes". *JFE* 122(2):221–247. https://www.sciencedirect.com/science/article/pii/S0304405X16301490 ; NBER w20439: https://www.nber.org/papers/w20439
26. Antonacci, G. "Extended Backtest of Global Equities Momentum". https://medium.com/@garyantonacci_30463/extended-backtest-of-global-equities-momentum-dual-momentum-eb12902612e0
    26b. Quant for Free. "Dual Momentum out of sample". https://quant4free.com/analysis/dual-momentum/
27. Gayed, M. y Bilello, C. (2016). "Leverage for the Long Run – A Systematic Approach to Managing Risk and Magnifying Returns in Stocks" (Premio Charles H. Dow 2016). https://docs.cmtassociation.org/dow-award/2016-gayed-bilello.pdf (tablas 6–8 verificadas en el PDF).
28. Cheng, M. y Madhavan, A. (2009). "The Dynamics of Leveraged and Inverse Exchange-Traded Funds". https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1539120
29. Avellaneda, M. y Zhang, S. (2010). "Path-Dependence of Leveraged ETF Returns". *SIAM J. Financial Math.* 1(1):586–603. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1404708
30. Bouman, S. y Jacobsen, B. (2002). "The Halloween Indicator, 'Sell in May and Go Away': Another Puzzle". *AER* 92(5):1618–1635. https://www.aeaweb.org/articles?id=10.1257%2F000282802762024683
31. Jacobsen, B. y Zhang, C. "The Halloween Indicator, 'Sell in May and Go Away': Everywhere and All the Time". SSRN: https://www.ssrn.com/abstract=2154873 ; revista: https://www.sciencedirect.com/science/article/abs/pii/S0261560620302242
32. McConnell, J. y Xu, W. (2008). "Equity Returns at the Turn of the Month". *FAJ* 64(2). https://business.purdue.edu/faculty/mcconnell/publications/Equity-Returns-at-the-Turn-of-the-Month.pdf
33. Quantpedia. "Turn of the Month in Equity Indexes". https://quantpedia.com/strategies/turn-of-the-month-in-equity-indexes
34. Lucca, D. y Moench, E. (2015). "The Pre-FOMC Announcement Drift". *JF* 70(1). https://www.newyorkfed.org/research/staff_reports/sr512.html
35. Kurov, A., Wolfe, M. y Gilbert, T. (2021). "The disappearing pre-FOMC announcement drift". *Finance Research Letters* 40. https://pmc.ncbi.nlm.nih.gov/articles/PMC7525326/
36. Santa-Clara, P. y Valkanov, R. (2003). "The Presidential Puzzle: Political Cycles and the Stock Market". *JF* 58(5):1841–1872. https://onlinelibrary.wiley.com/doi/abs/10.1111/1540-6261.00590
37. Wong, W. y McAleer, M. (2009). "Mapping the Presidential Election Cycle in US stock markets". *Mathematics and Computers in Simulation* 79(11):3267–3277. https://www.sciencedirect.com/science/article/abs/pii/S0378475409001268
38. Białkowski, J. y Nahavandi, A. (2019). "Midterm Elections' Stock Market Surge: An Unintentional Gift from US Politicians". *Journal of Wealth Management* 21(4):76. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3253726 ; https://jwm.pm-research.com/content/21/4/76
39. Yahoo Finance (4-may-2026). "Stocks have never posted a losing year after a midterm election since 1950". https://finance.yahoo.com/markets/stocks/articles/stocks-never-posted-losing-midterm-144711137.html
40. Federal Reserve. Calendario FOMC 2026 (27–28 oct y 8–9 dic). https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
41. Yahoo Finance, históricos del S&P 500 y ETFs (API de gráficas `query1.finance.yahoo.com/v8/finance/chart`, consultada el 25-sep-2026). https://finance.yahoo.com/quote/%5EGSPC/history/
42. Yahoo Finance, históricos del VIX (cierre de 15.67 el 24-sep-2026). https://finance.yahoo.com/quote/%5EVIX/history/
43. Documento interno A1: `/home/user/New1/arena/investigacion/01-gbm-operativa-y-costos.md` (comisiones de GBM, SIC, Trading USA y listado de TQQQ).
