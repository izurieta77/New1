# Auditoría semanal 2026-W43: abogado del diablo

- **Fecha:** 23-oct-2026, ~22:50 UTC (después del cierre). Solo lectura; no se ejecuta nada. Fase 0.
- **Conclusiones atacadas** (las tres van hoy al comité, `bitacora/comite/2026-10-23-expediente.md` L29-37 y L60):
  1. "El riesgo del UPRO se controla con el tamaño, no con capas rápidas" (R16, R17, R18 y su adenda: P(−12%) ≈ 21% por trimestre; bajar UPRO a 13.5% quita ~4.6 pp).
  2. "El ISR del SIC cuesta ~0.8 pp/año; el rebalanceo mensual suma < 0.2 pp; la parte cambiaria es ~7%" (R19, AC-25).
  3. "El Brier global llegó a 0.1979 (n = 74) y por primera vez cumple ≤ 0.20".
- **Método:** los cálculos propios usan las funciones `cargar`, `rendimientos` y `curva` de `laboratorio/replicas/R18.py` (fuente A, sin modificar el script) y `bitacora/pronosticos.csv` íntegro. Son de grado C: no tienen lado B.

---

## Conclusión 1 · "El riesgo del UPRO se controla con el tamaño, no con capas rápidas"

### Pre-mortem (es 23-abr-2027 y la cuenta de papel perdió 30%)
1. **La métrica de R18 no es la de los cortacircuitos.** R18 mide la caída "bajo el máximo **desde t**" dentro de 63 días: cada ventana arranca en su propio pico. `riesgo.estado_cortacircuitos` (`herramientas/riesgo.py` L82-89) mide contra el **máximo histórico de la cuenta**. El papel ya está a −3.3% de su pico (104.41 contra 100.97 en `bitacora/equity.csv`). Una corrección normal suma ese −3.3% al trimestre siguiente, toca −12% y luego −20% (sin apalancados). La cuenta vende abajo dos veces y no recupera en el horizonte.
2. **Una brecha sin aviso.** 1987 queda fuera de la muestra, que empieza en 1990. Un día como el 19-oct-1987 (S&P −20.47%, cap. 17 L156) con el filtro encendido le hace al 3x sintético −61%. A la mezcla le hace ≈ −29%: 0.269 × −61.4 + 0.41 × −20.5 + 0.268 × (supuesto de −15% para el NDX, no verificado) ≈ −28.9%. Pasa de un salto los niveles de −12, −20 y −28%. Ni el filtro, ni el stop, ni la volatilidad objetivo actúan dentro del día. **"Un stop no es un put"** (cap. 17).
3. **El 3x real rinde menos que el sintético en lo que importa.** El sintético rinde ~1.6 pp/año más que el UPRO real (R11, lado B, L100). La ejecución al día siguiente cuesta 1.84-3.56 pp/año en apalancados (R06 L972). El UPRO real cayó −76.8% en feb-mar 2020 ([totalrealreturns](https://totalrealreturns.com/s/SPY,UPRO)). Todas las cifras de R16 a R18 son de un instrumento más favorable que el que se tiene.

### Vista externa y tasa base
- Los resultados de backtest pierden ~26% fuera de muestra y ~58% después de publicarse (McLean y Pontiff 2016, *JF* 71(1); cap. 08 L133). R16 a R18 son pruebas dentro de muestra sobre **una sola trayectoria**. La MDD de R16 y R17 sale de **un solo episodio** (1998-2003, AC-23).
- Lo y Remorov (*J. Financial Markets*, 2017; [MIT DSpace](https://dspace.mit.edu/handle/1721.1/107017)): los stops estrechos rinden menos que comprar y mantener por costos. Los stops amplios a 10 días **sí reducen algo el riesgo de caída** ([CXO Advisory](https://www.cxoadvisory.com/equity-premium/stop-losses-on-stock-positions-in-depth)). "Las capas rápidas no sirven" es una generalización: lo que se probó es **un** stop con **una** regla de reentrada.

### Evidencia contraria (propia y externa)
- **Cálculo propio (A, funciones de R18), drawdown contra el máximo histórico, como lo calcula la cuenta:**

  | UPRO | P(toca −12% en 63 d, partiendo arriba de −12%) | Ídem, con DD actual entre −2% y −5% (el estado de hoy) | Ídem, 126 d | Cuenta nueva: P(−20% en 252 d) | MDD de la mezcla |
  |---|---|---|---|---|---|
  | 0% | 14.1% | — | — | 16.6% | −58.3% |
  | 13.5% | 20.0% | **17.1%** | 29.6% | 25.4% | −56.9% |
  | **26.9%** | **33.3%** | **25.1%** | **44.7%** | **27.1%** | −55.6% |
  | 40% | 37.8% | — | — | — | −54.3% |

  - El 21% del expediente subestima: la cifra comparable es **25% condicional a hoy** (33% sin condicionar).
  - La diferencia por bajar a 13.5% es **~8 pp a 63 días y ~15 pp a 126 días**, no 4.6 pp. El tamaño importa **más** de lo que dice el expediente en el primer nivel.
  - **En la cola profunda el tamaño del UPRO casi no mueve nada.** La MDD de la mezcla es −54% a −58% con cualquier peso de UPRO, y baja al subir UPRO porque el filtro saca al 3x. P(−20% en un año, cuenta nueva) es 25-27% con 13.5% o con 26.9%. El tope duro de −35% se rompe en 2000-02 y 2008 en todas las variantes. **La cola profunda la pone el 68% de beta sin cobertura (SPYM + QQQM), no el UPRO.** El "3.5% por trimestre" de P(−20%) del expediente se lee como un riesgo menor, y no lo es en un horizonte de un año.
- **R16 depende de la regla de reentrada.** Con reentrada a 21 días el Sharpe es igual (0.543 contra 0.537) y la MDD mejora 1.7 pp. En 2009-hoy el S10.92 tuvo un Sharpe **mayor** que V0 (0.647 contra 0.616). El costo sale de **dos stops** (1994-12 y 2018-03, AC-22). Es n = 2.
- **R17 confunde regla con tamaño:** VT30 baja la MDD 12-13 pp. Es "tamaño dinámico". Concluir "tamaño sí, capas no" cuando la capa que funcionó es una forma de tamaño es una distinción semántica.
- **El tipo de cambio no siempre amortigua:** en 2022 el peso se apreció y el S&P TR en MXN perdió −28.9%, más que en USD (cap. 17 L168). El "en MXN amortigua 5-7 pp" de R18 B es un promedio, no una garantía.
- Los flujos de rebalanceo diario de los ETF apalancados se parecen a los del *portfolio insurance* de 1987 ([Fed FEDS 2013-48](https://www.federalreserve.gov/pubs/feds/2013/201348/)).

### Contraparte
- En el UPRO, los bancos de swaps cobran el diferencial de fondeo sobre un nocional de ~200% (la causa principal del rezago contra el 3x perfecto; [ETF.com](https://www.etf.com/sections/features/leveraged-etfs-hidden-costs-eat-your-returns-0)). Quienes dan liquidez al cierre conocen el flujo de rebalanceo del ETF. Al disparar el −12% vendemos a quien compra caídas con horizonte largo y sin cortacircuitos: ellos no saben más del índice, pero **no están obligados a vender**. Esa es su ventaja.

### Sesgos detectados en el sistema
- **Anclaje:** en la métrica de R18, diseñada para el −8% y heredada por la adenda y la conciliación (que verificaron que las cifras **cuadran**, no que la **métrica es la correcta**). La conciliación del 22-oct reconoce que es "independiente en el código, no en la fuente". Tampoco lo es en la **definición**.
- **Narrativa:** la "lectura común R16-R18" es una historia limpia hecha con tres pruebas sobre la misma trayectoria.
- **Exceso de confianza:** "fallo vinculante para el comité" sobre una cifra (21%) que no mide lo mismo que el freno.

### Veredicto 1: **se sostiene con matiz (la dirección sí; las cifras no)**
**Qué debe cambiar en el expediente:**
- Sustituir "P(−12%) ≈ 21%; −4.6 pp" por "contra el máximo histórico y con el DD actual (−3.3%): **~25% a 63 días y ~45% a 126 días con 26.9%, contra ~17% / ~30% con 13.5%** (cálculo propio A, grado C, falta B)".
- Agregar: "El tamaño del UPRO **no** controla la cola profunda: P(−20% en 12 meses) ≈ 25-27% con cualquier peso; la MDD de la mezcla es ~−55%. Riesgo de brecha tipo 1987 fuera de muestra: ≈ −29% en un día con 26.9% (≈ −24% con 13.5%)."
- Cambiar "no con capas rápidas" por "no con **este** stop ni con **esta** regla de reentrada".

---

## Conclusión 2 · "El ISR del SIC cuesta ~0.8 pp/año; rebalanceo mensual < 0.2 pp; parte cambiaria ~7%"

### Pre-mortem (abril de 2028: la declaración anual sale mucho peor que el modelo)
1. **Faltaron los dividendos.** R19 usa el TR completo, igual antes y después de ISR (§7 lo declara), así que **el arrastre no incluye ningún impuesto sobre dividendos**. GBM describe tres capas para los dividendos del SIC ([GBM FAQ](https://gbm.com/faqs/como-funcionan-los-impuestos-sobre-los-dividendos-en-trading-mx)): 30% en EUA (10% con W-8BEN vigente), 10% de retención en México sobre el neto y acumulación en la declaración anual (hasta 35%) con acreditamiento. Con un rendimiento por dividendo de la mezcla de ~0.9% anual (SPYM 41% × ~1.8%, QQQM 26.8% × ~0.7%; supuesto propio), la retención combinada de ~19% a ~30% suma **~0.18-0.30 pp/año**. **El total queda en ~1.0-1.1 pp, en el umbral de H1** (≥ 1.0), que el expediente presenta como refutada.
2. **UPRO no está cubierto por la regla fiscal que se le aplicó.** La ficha fiscal del 22-oct dice: "faltan apalancados, derivados y cripto" (L79). El UPRO replica con swaps, no "representa exclusivamente acciones". Si el SAT no lo trata como fr. II del art. 129, sus ganancias se acumulan a tasa progresiva. **Más de la mitad del arrastre viene del filtro del UPRO** (R19: M 0.81 contra B 0.35). Este es el componente con más riesgo de que el 10% no aplique. Riesgo no verificado y potencialmente grande.
3. **Efectivo y moneda mal modelados.** En el SIC la venta liquida en **MXN**. El efectivo medio es ~12% de la cartera (5.3% fijo más la manga de UPRO cuando el filtro está apagado, ~27% del tiempo). R19 lo trata como T-bill en USD, sin ISR. En la realidad: interés en MXN con retención y acumulación del interés real, y la manga **sin exposición al dólar** justo cuando el filtro está apagado, en las crisis en que el peso se deprecia. Cambian el arrastre (+0.05-0.15 pp estimado) y la propia CAGR en MXN.

### Vista externa y tasa base
- En un modelo con supuestos declarados pero no cuantificados, la tasa base es que el sesgo de omisión vaya **en una sola dirección**: los cuatro riesgos del §7 de R19 (efectivo sin ISR, dividendos sin retención, pérdidas sin actualizar e INPC proxy) **todos** subestiman o no cambian el costo. Ninguno lo sobreestima salvo las comisiones (−0.05 pp).
- La única desviación encontrada por B (las comisiones) se llamó "conservadora". Las omisiones no medidas van en sentido **contrario** y son 4-6 veces más grandes.

### Evidencia contraria
- La retención en EUA y la segunda retención mexicana sobre dividendos del SIC ([GBM FAQ](https://gbm.com/faqs/como-funcionan-los-impuestos-sobre-los-dividendos-en-trading-mx); [Finantres, W-8BEN en GBM](https://finantres.mx/w8ben-gbm/)). Sin W-8BEN vigente es 30%.
- **Tratamiento incierto de ETF que no son de renta variable simple** ([Rankia](https://www.rankia.mx/blog/como-comenzar-invertir-bolsa/7335308-que-impuestos-pagas-vender-acciones-etfs-mexico): la ley no resuelve expresamente ciertos ETF; posible tarifa progresiva).
- **"El rebalanceo mensual suma < 0.2 pp" es cierto solo en ISR y engaña en el total.** Después de ISR, M rinde 17.94% contra 18.52% de A (−0.58 pp, lado A) y 17.99% contra 18.36% (−0.37 pp, lado B). **El rebalanceo mensual cuesta ~0.4-0.6 pp/año después de impuestos**, sobre todo por comisiones de 0.29% en 1,344 operaciones y por deriva. Si el comité lee "< 0.2 pp", concluirá que la frecuencia de rebalanceo no importa, y sí importa.
- **La parte cambiaria de ~7% depende de la muestra:** el INPC subió ×10.5 y el tipo de cambio ×6.0 (AC-25). La actualización por inflación neutraliza el efecto cambiario **solo si el peso no se deprecia en términos reales**. En un choque cambiario con inflación baja (2008: USD/MXN +57%, cap. 17 L175) o en tenencias cortas (el 100% cambiario del caso real del 22-oct), la proporción es otra. Es una cifra de 32 años que empieza en el piso de 1994.
- **Instrumentos anacrónicos:** UPRO existe desde 2009 y QQQM desde 2020. Antes de 2009, el 3x sintético no paga el diferencial real de los swaps (~1.6 pp/año de rezago, R11 B). Un CAGR antes de ISR más alto infla las ganancias realizadas, pero también la base de comparación. El efecto neto en pp es chico, pero el 18.75% en MXN **no es alcanzable** (R19 §7 lo dice; el expediente no).

### Contraparte
- **El SAT**, que tiene la ventaja del texto legal y de la interpretación. El dato que manda no es el modelo sino la **constancia fiscal (CFDI) de GBM**: cómo clasifica a UPRO y cuánto retiene por dividendos.

### Sesgos detectados
- **Exceso de confianza:** "Replicado" se lee como "correcto". A y B replicaron **el mismo modelo con las mismas omisiones**; la réplica verifica el código, no el alcance.
- **Confirmación:** AC-25 llamó "conservadora" a la desviación de A sin sumar las omisiones del lado contrario.
- **Anclaje:** en la expectativa del pre-registro (0.5-1.5 pp). Se refutó H1 con 0.81 contra el umbral de 1.0, y la omisión de los dividendos basta para cruzarlo.

### Veredicto 2: **no se sostiene tal como está redactada** (la parte cambiaria se sostiene con matiz)
**Qué debe cambiar en el expediente:**
- Sustituir "~0.8 pp" por "**≥ 0.8 pp sin dividendos ni intereses; estimado ~1.0-1.2 pp con la retención sobre dividendos (EUA 10-30% más 10% en México) y los intereses del efectivo en MXN; no incluye el riesgo de que UPRO no tribute al 10%**".
- Sustituir "el rebalanceo mensual suma < 0.2 pp" por "**en ISR < 0.2 pp; en total, después de impuestos y comisiones, el mensual rinde 0.4-0.6 pp/año menos que el anual**".
- Agregar "parte cambiaria ~7% **en tenencias largas con inflación mayor que la depreciación**; en tenencias cortas puede ser ~100%".
- Antes de usar R19 en una decisión de frecuencia o de UPRO: confirmar con GBM o con el SAT si UPRO cae en el art. 129 fr. II.

---

## Conclusión 3 · "Brier 0.1979 (n = 74), por primera vez cumple ≤ 0.20"

### Pre-mortem (balance mensual de noviembre: Brier 0.22, "dejó de cumplir")
1. **Fue suerte de una centésima.** Cuatro pronósticos (P0028, P0038, P0071 y P0096) son **la misma variable**: el VIX del 16-oct contra 20. El VIX cerró en **19.99**. **Si hubiera cerrado en 20.00, el Brier global sería 0.233.** Una centésima del VIX mueve 3.5 pp del Brier.
2. **Regresión a la media.** El cruce de 0.20 ocurrió hoy con 4 resoluciones (0.204 → 0.198), entre ellas P0093 (p = 0.08 de un statu quo) y P0135 (el propio papel, ganado por **0.05 puntos** de índice).
3. **Preguntas fáciles o autorreferentes:**
   - P0056 (p = 0.97 de que **nuestras propias órdenes** se ejecuten);
   - P0035 (0.97 sobre un mercado de Polymarket que ya estaba en ~1);
   - P0079 (0.88 de que el UPRO siga arriba del stop);
   - P0113 y P0118, creados el mismo día de su resolución con la brecha nocturna ya conocida.

### Vista externa y tasa base
- **No es distinguible de 0.20.** EE del Brier = 0.0157. IC 95% normal [0.167, 0.229]; bootstrap [0.168, 0.228]. P(bootstrap > 0.20) = **44%**.
- **Un pronosticador perfectamente calibrado con nuestras p** tendría un Brier esperado de 0.213 y pasaría el ≤ 0.20 solo el **22%** de las veces (20,000 simulaciones, cálculo propio; coincide con la ficha del 20-oct). El Spiegelhalter Z = −0.91 no rechaza la calibración. **Pasar el umbral es compatible con el ruido.**
- Foresight Arena (cap. 08 L211): hacen falta **~348 pronósticos** para detectar una ventaja de 0.02 en Brier. Con n = 50 solo se detectan ventajas ≥ 0.053. Bradley et al. (2008, *Weather and Forecasting* 23(5), [U. Iowa](https://iro.uiowa.edu/esploro/outputs/journalArticle/Sampling-Uncertainty-and-Confidence-Intervals-for/9983991990102771)): se necesitan **cientos** de pares para mostrar habilidad. Con preguntas correlacionadas, los intervalos ingenuos son demasiado estrechos (Wilks 2010, *QJRMS* 136(653), [infona](https://www.infona.pl/resource/bwmeta1.element.wiley-qj-v-136-i-653-qj709)).

### Evidencia contraria (cálculo propio con `bitacora/pronosticos.csv`)
| Ajuste | Brier | n |
|---|---|---|
| Tal como se reporta | 0.1979 | 74 |
| Antes de las resoluciones de hoy | 0.2040 | 70 |
| VIX del 16-oct = 20.00 (4 resultados invertidos) | **0.2330** | 74 |
| Los 4 del VIX colapsados a 1 | 0.2047 | 71 |
| Promedio por grupo de la misma variable (VIX 16-oct, BTC 15-oct, Brent 16-oct, WTI 14-oct, ISM sep, S&P 16-oct, BTC 20/21-oct, CPI sep) | 0.2056 | 62 grupos |
| Sin los triviales o autorreferentes (P0035, P0056, P0079, P0093, P0030, P0135) | 0.2090 | 68 |
| Sin duplicados ni triviales | 0.2220 | 57 |
| Sin duplicados, triviales ni pronósticos del mismo día | **0.2261** | 55 |

- **Ninguna de las depuraciones razonables cumple ≤ 0.20.**
- **No hay resoluciones vencidas sin resolver** (0 casos): no hay sesgo de resolución selectiva.
- Las resoluciones anticipadas (P0041, P0068, P0077 y P0099) tienen criterio de "toca" o comunicado ya publicado: son válidas.
- P0125 se resolvió con el cierre de las 20:15 UTC: válido.
- **Lo que sí es real:** el skill contra la climatología es **+0.18** y el BSS contra 50% es +0.21. El sistema le gana a la tasa base. Eso es más informativo que el umbral, y sobrevive mejor a las depuraciones.
- **Lo que falta:** la regla del cap. 08 §6 ("contra el precio") pide comparar con la probabilidad implícita (opciones, Polymarket o Kalshi). No se ha hecho. **Sin ese contraste, "cumple" no implica ventaja operable.**

### Contraparte
- El mercado: precios de opciones del VIX, del S&P y de BTC, y Polymarket. En las preguntas de nivel a 1-2 semanas, la distribución implícita ya da esas probabilidades. Si el Brier no le gana al precio, no hay ventaja.

### Sesgos detectados
- **Recencia y narrativa:** "por primera vez cumple" con 4 resoluciones del mismo día.
- **Confirmación:** la propia ficha del 20-oct advierte que el umbral "premia la facilidad de las preguntas tanto como la habilidad" y propone medir "real − esperado". El expediente reporta el umbral, no la métrica que el sistema mismo eligió.
- **Doble conteo:** la ficha del 20-oct ya señaló los pares P0071/P0096 y P0075/P0095. Desde entonces se sumaron más duplicados (P0038 y P0028 sobre el mismo VIX), y `puntuar` no los agrupa.

### Veredicto 3: **no se sostiene**
**Qué debe cambiar en el expediente:**
- Sustituir por: "**Brier 0.198 (IC 95% 0.168-0.228), no distinguible de 0.20.** Depurado de duplicados y triviales: 0.21-0.23. Skill contra la climatología +0.18 (lo sustantivo). El umbral de fase 0 **no** se da por cumplido."
- Proponer al balance mensual:
  - `puntuar` agrupa por variable y fecha;
  - las preguntas sobre las propias órdenes o el propio papel se excluyen o se marcan;
  - el criterio es "sostenido ≥ 8 semanas con n ≥ 100 agrupado, con el IC superior < 0.21", más el BSS contra el precio cuando exista.

---

## Prueba de falsabilidad (datos fechados)
1. **C1:** si el lado B (auditor) recalcula P(−12% contra el máximo histórico, 63 días, con DD entre −2% y −5%) con 26.9% y da ≤ 21%, mi objeción a la cifra cae. Fecha: siguiente laboratorio (≤ 30-oct-2026). En la cuenta: si con UPRO a 26.9% el papel **no** toca −12% contra su pico (104.41) antes del 23-abr-2027, el riesgo fue de ~45% y no se materializó, pero eso no valida la cifra.
2. **C2:** el primer dividendo de SPYM y QQQM en el papel o en real (distribuciones trimestrales; la siguiente es ~dic-2026) y su CFDI: si la retención total es < 10%, el ajuste por dividendos se reduce a ~0.09 pp y "~0.8-0.9 pp" queda en pie. Si GBM o el SAT confirman que UPRO tributa con el art. 129 fr. II antes del 30-nov-2026, el riesgo 2 del pre-mortem cae.
3. **C3:** al 30-nov-2026, con n ≥ 100 y agrupando por variable, Brier ≤ 0.20 **y** la cota superior del IC < 0.21: entonces "cumple". Si no, no.

## Veredicto global: **no sobrevive** como paquete
C1 sobrevive en su dirección (de hecho, el argumento a favor de reducir el UPRO es **más fuerte** de lo que dice el expediente), pero con cifras equivocadas. C2 y C3 no sobreviven tal como están escritas.

## Condiciones mínimas para que sobreviva
1. Corregir las cifras de C1 a la métrica contra el máximo histórico, con el DD actual, y declarar que el tamaño del UPRO no controla la cola profunda (P(−20%/12 m) ≈ 25-27%; MDD ≈ −55%; brecha tipo 1987 ≈ −29%).
2. Reexpresar C2 como "~1.0-1.2 pp con dividendos e intereses; rebalanceo mensual −0.4-0.6 pp en total; UPRO pendiente de confirmación fiscal".
3. Retirar "cumple" de C3 y reportar el IC, el Brier agrupado y el skill contra la climatología.

## Voto
- **En contra** de que las tres conclusiones entren al expediente con su redacción actual.
- **A favor de B1** (UPRO de 2 a 1 título), por una razón distinta a la del expediente: contra el máximo histórico, el riesgo de tocar −12% en 6 meses baja de ~45% a ~30%, y la exposición a una brecha de un día baja ~5 pp. Cuidado: B1 **no** protege la cola profunda, que depende del 68% en SPYM + QQQM.

## Fuentes
- [McLean y Pontiff 2016, JF](https://doi.org/10.1111/jofi.12365) (cap. 08 L133)
- [Lo y Remorov, stop-loss (MIT DSpace)](https://dspace.mit.edu/handle/1721.1/107017); [CXO Advisory, resumen](https://www.cxoadvisory.com/equity-premium/stop-losses-on-stock-positions-in-depth)
- [ETF.com, costos ocultos de los apalancados](https://www.etf.com/sections/features/leveraged-etfs-hidden-costs-eat-your-returns-0); [Koala Gains, UPRO](https://koalagains.com/etfs/NYSEARCA/UPRO/cost-efficiency-team) (tercero; rezago de −50 a −100 pb/año)
- [Fed FEDS 2013-48, rebalanceo de LETF](https://www.federalreserve.gov/pubs/feds/2013/201348/)
- [totalrealreturns, UPRO](https://totalrealreturns.com/s/SPY,UPRO) (MDD −76.8%, 2020)
- [GBM FAQ, dividendos en Trading MX](https://gbm.com/faqs/como-funcionan-los-impuestos-sobre-los-dividendos-en-trading-mx); [Finantres, W-8BEN en GBM](https://finantres.mx/w8ben-gbm/); [Rankia, impuestos de ETF en México](https://www.rankia.mx/blog/como-comenzar-invertir-bolsa/7335308-que-impuestos-pagas-vender-acciones-etfs-mexico)
- [Bradley et al. 2008, incertidumbre muestral del Brier](https://iro.uiowa.edu/esploro/outputs/journalArticle/Sampling-Uncertainty-and-Confidence-Intervals-for/9983991990102771); [Wilks 2010, QJRMS](https://www.infona.pl/resource/bwmeta1.element.wiley-qj-v-136-i-653-qj709); [arXiv 2509.08744, suerte contra habilidad](https://arxiv.org/pdf/2509.08744)
- Internas: R06 L972, R11 L100, AC-22, AC-23, AC-25; cap. 08 L211 (Foresight Arena); cap. 17 L156, L168, L175; `conocimiento/fichas/2026-10-22-fiscalidad-sic-isr-caso-real.md` L64 y L79; `conocimiento/fichas/2026-10-20-brier-contraste-real.md`.
