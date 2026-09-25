# Módulo 16 — Macro global, divisas y el peso mexicano

> Nivel: especialidad (macro internacional + mesa de FX emergentes) · Actualizado: 2026-09-25 · Grado de evidencia global: **B**. Tres hechos llegan a grado **A**: (1) la paridad descubierta de tasas (UIP) falla, y las monedas de tasa alta pagan en promedio un exceso positivo con sesgo negativo; (2) el peso es una moneda de riesgo que se deprecia cuando el mundo entra en pánico, con correlación mensual de −0.4 a −0.56 contra el S&P 500 en todas las submuestras de 1996 a 2026; (3) por lo mismo, para quien mide en MXN, los activos en dólares sin cubrir son una cobertura natural en *shocks* globales: el *drawdown* del S&P medido en MXN fue de −40% en 2007-09 (contra −57% en USD) y de −15% en 2020 (contra −34%). Las estrategias de *timing* cambiario (momentum, filtros, valor de corto plazo, marcos de ciclo de deuda) son **C/D**.

Capítulos relacionados, que aquí no se repiten: [01 Fundamentos](01-licenciatura-fundamentos.md) · [02 Portafolio y asset pricing](02-maestria-portafolio-y-asset-pricing.md) · cap. 04 (renta fija y macro) · cap. 06 (asset pricing empírico y decaimiento) · cap. 07 (riesgo y backtesting) · cap. 11 (México: SIC, fiscalidad, BMV) · cap. 13 (estado del mercado) · [23 Geopolítica](23-geopolitica-y-riesgo-politico-global.md) (taxonomía de *shocks* A-E). La fórmula de rendimiento en pesos y el registro del tipo de cambio están en [ideas adoptadas](ideas-adoptadas-2026-09-25.md), punto 7. Los parámetros salen de `config/parametros.json`.

**Convenciones.** USD/MXN = pesos por dólar: si sube, el peso se deprecia. Un alza de 23% en USD/MXN equivale a una caída de 19% del valor del peso (1 − 1/1.23), así que hay que decir siempre cuál de las dos cifras se usa. "Cálculo propio" = series descargadas el 2026-09-25 con `herramientas/datos.py` (FRED: DEXMXUS, IR3TIB01MXM156N, TB3MS, VIXCLS, DGS10, DFII10, T10YIE, DTWEXBGS, RBMXBIS, TRESEGMXM052N; Yahoo: ^GSPC). Salvo que se diga otra cosa, son cifras **in-sample, brutas, sin costos ni impuestos**. "(nv)" = dato de consenso no re-verificado en esta sesión. "Inferencia:" = interpretación propia.

---

## 1. Objetivos de dominio

Quien se titule en este módulo debe poder, con números y sin ayuda:

1. Escribir la CIP, la UIP y el exceso de rendimiento del *carry* (rx = i* − i − Δs), y explicar por qué el *forward* **no** pronostica el tipo de cambio.
2. Explicar las cuatro familias de explicación de la falla de la UIP (prima por riesgo de *crash*, factor global, *convenience yield* del dólar y *peso problem*), cuál tiene mejor evidencia y qué parte del "puzzle" es frágil (Hassan-Mano 2019).
3. Distinguir los dos factores que mueven casi todas las monedas, el **dólar** y el **carry**, y ubicar al MXN en ellos.
4. Leer el ciclo financiero global (Rey) y anticipar qué le pasa al peso cuando la Fed aprieta, sube el VIX o el yen deja de fondear *carry*.
5. Diagnosticar vulnerabilidad de crisis (crisis gemelas, *sudden stops*, deuda) con un tablero de indicadores, sabiendo que como predictor de *timing* es débil.
6. Contar la historia de las crisis del peso de 1976 a 2026 con magnitudes y extraer el patrón común.
7. Cuantificar la cobertura natural: cuánto bajan la volatilidad y el *drawdown* de acciones de EUA al medirlas en MXN, y en qué regímenes falla (2022, abril de 2025).
8. Decidir cuándo cubrir y cuándo no el tipo de cambio para cada tipo de activo y de pasivo, y qué cuesta cada opción hoy (diferencial Banxico-Fed de 250-275 pb, el menor en más de una década).
9. Manejar la exposición cambiaria de la cuenta arena como una **apuesta relativa contra los rivales**, coherente con `modo_torneo`.
10. Dar el estado de septiembre de 2026 (tasas, peso, calificaciones, Pemex, T-MEC, remesas, IED, reservas) y separar narrativa de flujo.

---

## 2. Núcleo teórico / marco

### 2.1 Identidades

- **Paridad cubierta (CIP):** F/S = (1 + i_MXN)/(1 + i_USD). Es arbitraje, no pronóstico. Con Banxico en 6.50% y la Fed en 3.75-4.00%, el *forward* a un año de USD/MXN está alrededor de 2.5-2.75% **arriba** del spot.
- **Paridad descubierta (UIP):** E[Δs] = i_MXN − i_USD. Si se cumpliera, el *carry* rendiría cero en promedio. No se cumple.
- **Exceso del *carry* (largo MXN fondeado en USD):** rx ≈ i_MXN − i_USD − Δln(USD/MXN). Para un mexicano, **tener CETES en vez de T-bills en dólares es estar largo en este *carry***, y tener dólares es estar corto.
- **Rendimiento en pesos:** 1 + R_MXN = (1 + R_USD) × (FX_final/FX_inicial). Está en las ideas adoptadas, punto 7.

### 2.2 La falla de la UIP (*forward premium puzzle*)

Fama (1984) encontró que la pendiente de Δs sobre (f − s) es **negativa**, cuando la UIP exige 1. La moneda de tasa alta no se deprecia lo que dice el diferencial, y casi toda la variación del *forward* es prima por riesgo. En las replicaciones la pendiente parte de alrededor de −2.4 a un mes y sólo deja de rechazar la UIP a 36 meses (fuente 1).

**Réplica propia para el MXN (mensual, 1997-2026):** β = **−0.07** (e.e. 0.39, R² ≈ 0). La UIP se rechaza a unos 2.7 e.e. En 2008-2026 la estimación es inservible (β = 0.81, e.e. 2.33). Con una sola moneda, la regresión es ruido. La evidencia fuerte viene de carteras de muchas monedas.

Explicaciones, de mayor a menor evidencia:
1. **Prima por riesgo de *crash* y factor global** (Brunnermeier-Nagel-Pedersen 2008; Lustig-Roussanov-Verdelhan 2011). Las monedas de tasa alta pierden cuando sube la aversión global y se seca el fondeo.
2. ***Convenience yield* del dólar** (Jiang-Krishnamurthy-Lustig 2021). Cuando la base del Treasury se ensancha, el dólar se aprecia de inmediato y luego se deprecia.
3. **Hassan-Mano (2019).** El *carry* es sobre todo **transversal**: hay monedas que pagan siempre más. El *puzzle* en series de tiempo y el *dollar trade* son frágiles, y ajustando por la incertidumbre sobre la tasa media futura "nunca rechazan" que se espere depreciación de las monedas de tasa alta. **Inferencia:** para el MXN, lo robusto es su **nivel** persistente de *carry*, no hacer *timing* con los cambios del diferencial.
4. ***Peso problem***. Un salto raro y grande que no aparece en muestras cortas. El nombre viene del peso de antes de 1976 (Krasker 1980, (nv)).
5. **Límites al arbitraje** y capital lento (discusión de Menkhoff et al. 2012).

**Engel (2016):** las monedas de tasa real alta tienen exceso de rendimiento a corto plazo y, en niveles, son "demasiado fuertes" frente a la UIP. Eso implica una reversión posterior que ningún modelo reproduce. **Inferencia:** un peso con *carry* alto y real fuerte, como el "super peso", acumula riesgo de reversión cuyo *timing* no se conoce.

### 2.3 PPP: ancla lenta, no reloj

Rogoff (1996) documenta el consenso de una **vida media de 3 a 5 años** en las desviaciones de la PPP, combinada con una volatilidad de corto plazo enorme. Meese-Rogoff (1983): los modelos estructurales no le ganan fuera de muestra a la caminata aleatoria. **Dato (cálculo propio, BIS REER):** el peso real estaba en **139.8 en jul-2026**, contra un promedio de 127.3 entre 1994 y 2026, es decir, en el **percentil 73**. Tocó 144.6 en abr-2024 y 122.9 en dic-2024. Es un viento en contra a varios años, pero no una señal para una temporada de 6 meses.

### 2.4 Dos factores: dólar y *carry*

- **LRV (2011, RFS):** el factor **dólar** (el promedio contra el USD) y el factor ***carry*** (HML_FX) explican el corte transversal. En el *working paper* (nov-1983 a mar-2008), HML_FX rinde **4.8% anual neto de *bid-ask*** con Sharpe **0.54**. Las acciones de EUA tuvieron 0.48 en la misma muestra. Sólo con desarrollados, el Sharpe baja a 0.39.
- **LRV (2014, JFE):** el *dollar carry* va corto en USD cuando el promedio de las tasas extranjeras supera a la de EUA. Paga por estar corto en dólares en malos tiempos y predice **hasta 25%** de la variación del dólar a un año (in-sample).
- **Verdelhan (2018, JF):** dólar y *carry* explican entre **18% y 80%** de los movimientos mensuales de cada tipo de cambio bilateral.
- **Daniel-Hodrick-Lu (2017):** en el G10, el *carry* neutral al dólar tiene alfa insignificante. La parte del dólar es la que gana, con poco sesgo.

**Inferencia:** buena parte del movimiento del USD/MXN es factor (dólar, *carry* y riesgo global). La noticia mexicana explica el residuo.

### 2.5 Ciclo financiero global (Rey)

Rey (2013) documenta un ciclo global de flujos, crédito y precios de activos que se mueve con el VIX y que la Fed impulsa a través del apalancamiento de los bancos globales. Con capital libre, el trilema se vuelve **dilema**: sólo hay política monetaria independiente si se administra la cuenta de capital, sin importar el régimen cambiario. Miranda-Agrippino y Rey (2020) encuentran que el factor global de los activos de riesgo cae significativamente tras un apretón de la Fed. **Inferencia:** Banxico puede desviarse de la Fed ("no la seguirá mecánicamente", 24-sep-2026), pero lo paga en el tipo de cambio. Ese día el peso perdió 1.16%.

### 2.6 Crisis: gemelas, *sudden stops* y "esta vez es diferente"

- **Kaminsky-Reinhart (1999):** los problemas bancarios **preceden** a la crisis cambiaria, y ésta los agrava en espiral. La liberalización financiera precede a las crisis bancarias. El caldo de cultivo es un auge de crédito, entradas de capital y moneda sobrevaluada que termina en recesión.
- **Calvo (1998) y Calvo-Izquierdo-Mejía (2004):** un frenazo de flujos puede detonar una crisis aunque el déficit se financie con IED. Con 32 países, los grandes movimientos del tipo de cambio real ligados a frenazos son "básicamente un fenómeno emergente", y llegan en racimos. La **poca apertura** combinada con la **dolarización de pasivos** es un "cóctel peligroso" no lineal.
- **Reinhart-Rogoff (2009):** 66 países y 800 años. El *default* en serie es casi universal. Tras las crisis bancarias grandes, la vivienda real cae **35% en unos 6 años** y el desempleo sube **7 pp en unos 4 años**.

**Inferencia para México 2026:** los detonadores de 1994 eran Tesobonos en USD, tipo semifijo y reservas agotadas. Hoy no están: hay flotación y reservas de alrededor de **US$248 mil millones** (ago-2026). Las vulnerabilidades actuales son Pemex, el déficit fiscal con bajo crecimiento, el riesgo institucional y un T-MEC en revisión anual. Apuntan a una **depreciación gradual y a degradaciones de calificación**, no a un 1994 (confianza media).

### 2.7 Dalio: qué tomar y qué no

- ***Principles for Navigating Big Debt Crises* (2018):** plantilla "arquetípica" del ciclo de deuda. Distingue desapalancamientos deflacionarios (deuda en moneda propia) e inflacionarios (deuda externa) y propone el *beautiful deleveraging*, que equilibra austeridad, reestructura, transferencias e impresión.
- ***How Countries Go Broke* (jun-2025):** afirma que EUA está en la última etapa del ciclo de deuda pública y propone bajar el déficit a **3% del PIB** desde alrededor de 6%.
- **Críticas:** abuso del *pattern-matching*, poca discusión con posturas contrarias y la contradicción de presentar un ciclo casi determinista mientras pide evitarlo (reseñas de AIER y otras). Una investigación del NYT de 2023 reportó que Bridgewater decidía en buena medida con las elecciones personales de Dalio.
- **Grado:** **C** como lista de canales (deuda → monetización → moneda débil). **D** como reloj: no hay señales fechadas verificables fuera de muestra.

### 2.8 Dominancia fiscal

Cecchetti-Schoenholtz (oct-2025) la definen como la presión fiscal que obliga al banco central a abandonar la estabilidad de precios para financiar la deuda. Un alza sostenida de 1 pp en las tasas añade más de 1% del PIB al costo federal de EUA. **Firma en precios (Inferencia):** *breakevens* al alza, una curva que se empina por el componente de inflación, un dólar débil aunque suban las tasas y oro al alza junto con las tasas nominales. En 2026 no se ve esa firma (sección 4.6).

### 2.9 Por qué el peso es moneda de riesgo

1. **Liquidez:** es la moneda **14** del mundo por operación según la encuesta trienal del BIS de 2025 (reporte de Banxico). Se negocia casi 24 horas y por eso se usa como **cobertura sustituta** de riesgo emergente.
2. ***Carry* concurrido:** los *unwinds* fondeados en yenes o en dólares son simultáneos.
3. **Exposición a EUA:** ciclo, remesas, aranceles y petróleo.
4. **Prima local (Kalemli-Özcan-Varela):** en emergentes, la prima de UIP la mueven el riesgo local y la **incertidumbre de política**. En avanzados la mueve el riesgo global. México tiene ambas.

Resultado (cálculo propio, sección 5.4): la correlación mensual del USD/MXN con el S&P 500 es de **−0.50** (1996-2026), y con el cambio del VIX de **+0.47**.

---

## 3. Literatura y fuentes canónicas

| # | Referencia | Hallazgo cuantificado | Enlace | Grado |
|---|---|---|---|---|
| 1 | Fama (1984), JME 14(3): 319-338 | La pendiente de Δs sobre (f − s) es **negativa** (≈ −2.4 a 1 mes en replicaciones). Casi toda la variación del *forward* es prima por riesgo | ideas.repec.org/a/eee/moneco/v14y1984i3p319-338.html | **A** (el hecho). **B** (su uso en series de tiempo, por Hassan-Mano) |
| 2 | Lustig-Roussanov-Verdelhan (2011), RFS 24(11): 3731-3777 | HML_FX: **4.8%/año neto de spreads**, Sharpe **0.54** (1983-2008). Dos factores, dólar y *carry*, explican el corte transversal | nber.org/papers/w14082 | **B** |
| 3 | Brunnermeier-Nagel-Pedersen (2008), NBER Macro Annual 23 | El *carry* tiene **sesgo negativo**, mayor con más diferencial. Un VIX o un TED alto predice mayor rendimiento futuro del *carry*. Hay *crashes* sin noticias (yen, 7-8 oct-1998) | nber.org/papers/w14473 | **A** |
| 4 | Menkhoff-Sarno-Schmeling-Schrimpf (2012), JFE 106: 660-684 | Momentum FX de hasta **10%/año** bruto y Sharpe 0.95 en MOM(1,1), con 48 monedas entre 1976 y 2010. Con el *spread* completo cae a **alrededor de 4%**. Límites al arbitraje (monedas menores, riesgo país) | ideas.repec.org/a/eee/jfinec/v106y2012i3p660-684.html | **C** para ejecución minorista |
| 5 | Menkhoff et al. (2012), JF, *carry* y volatilidad FX global | Sharpe del *carry* **0.82**. La volatilidad global explica el *carry* (citado en la fuente 4) | — | **B** |
| 6 | Rogoff (1996), JEL 34(2): 647-668 | Vida media de las desviaciones de la PPP de **3-5 años** | sfu.ca/~kkasa/rogoff96.pdf | **A** (el hecho). **D** (como *timing*) |
| 7 | Meese-Rogoff (1983), JIE 14: 3-24 | La caminata aleatoria no pierde fuera de muestra contra los modelos estructurales | ideas.repec.org/a/eee/inecon/v14y1983i1-2p3-24.html | **A** |
| 8 | Lustig-Roussanov-Verdelhan (2014), JFE 111(3): 527-553 | *Dollar carry*: exceso grande, sin correlación con el *carry* clásico. Predicción de **hasta 25%** de la variación del dólar a 1 año (in-sample) | nber.org/papers/w16427 | **B** |
| 9 | Verdelhan (2018), JF 73(1): 375-418 | Dólar y *carry* explican **18-80%** de los movimientos mensuales bilaterales | onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12587 | **A** (descriptivo) |
| 10 | Rey (2013), Jackson Hole | Ciclo financiero global ligado al VIX. Dilema en lugar de trilema. La política de la Fed es un motor | kansascityfed.org (2013Rey.pdf) | **B** |
| 11 | Miranda-Agrippino y Rey (2020), RES 87(6): 2754-2776 | El factor global de los activos de riesgo **cae significativamente** tras un apretón de la Fed | academic.oup.com/restud/article/87/6/2754/5834728 | **B** |
| 12 | Kaminsky-Reinhart (1999), AER 89(3): 473-500 | La crisis bancaria precede a la cambiaria. La liberalización precede a la bancaria | aeaweb.org/articles?id=10.1257/aer.89.3.473 | **B** (descriptivo). **C** (alerta temprana) |
| 13 | Reinhart-Rogoff (2009) y "Aftermath" (AER P&P 2009) | 66 países y 800 años. Tras la crisis, vivienda real **−35% en 6 años** y desempleo **+7 pp en 4 años** | nber.org/papers/w14656 | **B** |
| 14 | Calvo (1998), JAE 1(1): 35-54. Calvo-Izquierdo-Mejía (2004) | Frenazos incluso con IED. Con 32 países, poca apertura combinada con dolarización de pasivos es un "cóctel" no lineal | ucema.edu.ar (calvo.pdf) · frbsf.org (Calvo.pdf) | **B** |
| 15 | Campbell-Serfaty-de Medeiros-Viceira (2010), JF 65(1): 87-121 | Entre 1975 y 2005, USD, EUR y CHF se mueven **contra** las acciones mundiales. Al inversionista de bonos le conviene cubrir casi todo | nber.org/papers/w13088 | **B** |
| 16 | Engel (2016), AER 106(2): 436-474 | La moneda de tasa alta tiene exceso de rendimiento a corto plazo pero es "demasiado fuerte" en nivel. Esto implica reversión | nber.org/papers/w21042 | **B** |
| 17 | Hassan-Mano (2019), QJE 134(1): 397-450 | El *carry* es transversal. El FPP y el *dollar trade* son del componente temporal y son frágiles | nber.org/papers/w20294 | **B** |
| 18 | Jiang-Krishnamurthy-Lustig (2021), JF 76(3): 1049-1089 | *Convenience yield* del Treasury: si se ensancha la base, el dólar se aprecia de inmediato y luego se deprecia | nber.org/papers/w24439 | **B** |
| 19 | Daniel-Hodrick-Lu (2017), CFR 6(2): 211-262 | Con el G10, el *carry* neutral al dólar tiene alfa insignificante. La parte del dólar sí gana, con poco sesgo | nber.org/papers/w20433 | **B** |
| 20 | Koijen-Moskowitz-Pedersen-Vrugt, "Carry", JFE | El *carry* predice rendimientos en 8 clases de activos, y todas pierden **a la vez en recesiones globales** | nber.org/papers/w19325 | **B** |
| 21 | Dalio (2018) y (2025) | Plantilla arquetípica del ciclo de deuda. Regla de un déficit de 3% del PIB para EUA | economicprinciples.org/how-countries-go-broke | **C** (descriptivo). **D** (*timing*) |

---

## 4. Lo más reciente 2023-2026

### 4.1 El "super peso" (2023 a mayo de 2024)

USD/MXN bajó de 19.50 a 16.90 en 2023 (**−13.3%**) y tocó **16.325 el 8-abr-2024**, el peso más fuerte desde 2015 (FRED). Banxico estaba en **11.25%**, su máximo histórico, y la Fed en 5.25-5.50% (nv), así que el diferencial rondaba 6 pp. El *carry* propio de ene-2023 a may-2024 rindió **+17.5% anualizado**, con volatilidad de 8.5%, Sharpe de alrededor de 2 y *drawdown* de −6%. Su correlación con el S&P fue de **+0.77**: era el mismo *beta* de riesgo, pero con viento a favor. Era además la operación más concurrida del mercado (Bloomberg, 16-abr-2024: "Massive global carry trade unwinding hits the super peso").

### 4.2 2024: elección, reforma judicial y el *unwind* de agosto

- **Tras el 2-jun-2024** (mayoría calificada de Morena), el peso pasó de 16.97 a 18.36 en una semana, **−8.19%** (Banco Base). Le siguió la reforma judicial con elección popular de jueces.
- **5-ago-2024 (BIS Bulletin 90):** había alrededor de **¥40 billones (US$250 mil millones)** en *carry* fondeado en yenes. Ese día el TOPIX cayó **12%**, el VIX pasó de 60 intradía y **el peso, el real y el rand se debilitaron**. USD/MXN subió 4.6% entre el 31-jul y el 5-ago (cálculo propio). La causa fue el desapalancamiento procíclico, no un cambio en los fundamentos de México.
- **En el año,** USD/MXN cerró en **20.87** (+23%, o −19% del valor del peso). Fue la mayor depreciación anual desde 2008. El *carry* perdió **−16.9%** entre mar y dic-2024 y se recuperó hasta dic-2025.

### 4.3 2025: dólar débil y un *shock* nacido en EUA

El índice amplio del dólar cayó **−7.6% en el 1S-2025** y **−7.4% en el año** (FRED DTWEXBGS). Su máximo desde 2006 fue el 13-ene-2025. USD/MXN bajó de 20.86 a **18.01 (−13.7%)**. En el ***shock* arancelario de abril** (tipo C del cap. 23), el S&P cayó **−11.5%** del 1 al 8-abr, pero USD/MXN sólo subió **+3.0%** (a 20.94 el 9-abr). En MXN, el S&P cayó −9.9%. **La cobertura natural casi no funcionó, porque el *shock* era contra el dólar.**

### 4.4 2026: guerra, Fed que sube y diferencial mínimo

- **Guerra de Irán (tipo B):** USD/MXN pasó de 17.22 a **18.12 (+5.2%)** entre el 27-feb y el 30-mar. En el mínimo, el S&P perdía −7.8% en USD y **−3.0% en MXN**. Banxico recortó a 6.75% en marzo y a **6.50% en mayo**, y desde entonces pausa.
- **El peso más fuerte del año** fue **16.863 el 4-sep** (FRED).
- **Tres golpes en una semana:** el **16-sep** la Fed subió a **3.75-4.00%**, su primera alza desde 2023. El **18-sep** el BoJ subió a **1.25%**, máximo desde 1995, con voto 7-2; el yen se debilitó a alrededor de 156.7 porque Ueda no prometió más. El **22-sep** Trump llamó a México "epicentro" de la violencia de los cárteles.
- **23-sep:** el UST a 10 años llegó a **5.11%**, máximo desde 2007 (CNBC y FRED), con PMI fuerte, el gobernador Barr pidiendo más alzas y una subasta débil. El peso tuvo su **peor día en 6 meses (−1.3%, a 17.51)**.
- **24-sep:** Banxico **mantuvo 6.50%** por unanimidad, con inflación de 3.42% y convergencia prevista para el 4T-2027, y dijo que no seguirá mecánicamente a la Fed. El peso cerró en **17.7148** (FIX 17.6425). El **diferencial quedó en 250-275 pb, el menor en más de una década** (El Financiero).
- **Fondeo en yenes:** según un resumen de Bloomberg (18-sep, fuente secundaria), el préstamo transfronterizo en yenes creció alrededor de 67% entre dic-2021 y mar-2026, a alrededor de ¥360 billones.

**Inferencia:** el *carry* del peso es el más delgado de la era post-2008. Con la volatilidad realizada a 63 días de 6.3%, el cociente *carry*/vol es de alrededor de 0.4. Con una vol normal (10-11%) sería de alrededor de 0.25. El mercado paga poco por cargar pesos justo cuando la Fed y el BoJ aprietan, que es la configuración que precedió a los *unwinds* de 2024.

### 4.5 México, fundamentales a septiembre de 2026

| Variable | Dato | Fuente |
|---|---|---|
| USD/MXN | 17.7148 (cierre del 24-sep). Rango 2026: 16.863-18.119 | El Financiero y FRED |
| Tasa Banxico / Fed | 6.50% (24-sep) / 3.75-4.00% (16-sep) | Expansión y CNBC (cap. 23) |
| Inflación México | 3.42% (1ª quincena de sep). Meta en el 4T-2027 | PorEsto y Expansión |
| UST 10 años / real / *breakeven* | 5.11% / 2.76% / 2.33% (23-sep) | FRED |
| VIX | 14.2 (22-sep) y alrededor de 15.7 (24-sep) | FRED y Yahoo |
| Calificación soberana | Moody's **Baa3** estable (bajó desde Baa2 el 20-may-2026). S&P **BBB negativa** (may-2026). Fitch **BBB−** estable | Bloomberg Línea y El CEO |
| Motivos (Moody's) | Debilitamiento fiscal acelerado en 2024. Crecimiento **<1% en 2026**. Deuda de **54.75% del PIB** en 2026. Déficit de 4.9% en 2025. Pasivos de Pemex | Bloomberg Línea |
| Pemex | Moody's **B1** estable (22-may). Fitch **BB+** estable (24-sep) | El Financiero y Bloomberg Línea |
| T-MEC | Sin extensión el 1-jul-2026, con revisiones anuales hasta 2036. 4ª ronda del 28 al 29 de sep. Pendientes: autos (EUA pide 50% de contenido de EUA), acero, agro y laboral | White & Case y Rio Times |
| Aranceles de EUA | Sección 232: 50% a acero y aluminio y 25% a autos fuera del T-MEC. Sección 301: 10%, con **exención T-MEC** | AS/COA y cap. 23 |
| Remesas | 2025: **US$61,791 millones (−4.6%)**, la primera caída en 11 años. Ene-jul 2026: **US$36,349 millones (+3.1%)**. Impuesto de EUA de 1% a los envíos en efectivo desde el 1-ene-2026 | BBVA, El Financiero y Wikipedia (OBBBA) |
| IED | 1S-2026: **US$34,968 millones**, récord (+2.1%). La **inversión nueva es sólo 7.8%** y cae 13% | SE y El Financiero |
| Reservas | Alrededor de **US$248 mil millones** (ago-2026, sin oro) | FMI vía FRED |
| Coberturas de Banxico | *Forwards* liquidables en MXN: US$20 mil millones (feb-2017), subieron a **US$30 mil millones** (mar-2020) y se decidió su **reducción gradual** el 31-ago-2023. Estado 2024-2026 (nv) | Banxico |

**Inferencias:** (a) el récord de IED es sobre todo **reinversión de utilidades** (68% al 3T-2025, según la SE). La tesis de que el *nearshoring* aprecia el peso es **D** mientras no crezca la IED nueva. (b) Las remesas ya no son el viento a favor de 2015-2024. (c) México está a un escalón de *junk* con Moody's y Fitch, y S&P tiene perspectiva negativa. Si dos agencias bajan la nota, los mandatos de grado de inversión venderían (umbrales por índice: (nv)). El mercado suele anticipar estas bajas, así que el golpe se concentra en el anuncio.

### 4.6 Dominancia fiscal, debate 2024-2026

- **A favor:** la CBO proyecta un déficit federal de **US$1.9 billones en 2026**, de 5.6% del PIB o más cada año hasta 2036, y un interés neto que pasa de alrededor de US$970 mil millones (2025) a más de US$1 billón (3.3% del PIB) (vía fuente secundaria). En la ASSA del 4-ene-2026, Yellen, Mester, Orphanides y Romer advirtieron que "las precondiciones se fortalecen". Hubo presión presidencial por bajar las tasas "al menos 3 pp".
- **En contra, con los precios de 2026:** la Fed de Warsh **subió** tasas (12-0). El *breakeven* a 10 años está en 2.33%. El alza del UST a 5.11% vino de la **tasa real** (+0.83 pp en 2026). El oro cayó alrededor de 22% desde su récord de enero (cap. 23).
- **Veredicto (Inferencia):** la dominancia fiscal no se ve hoy en los precios. Lo que sí hay es **prima por plazo creciente** y un riesgo institucional de cola. La tesis de vender dólares y bonos largos "ya" es **C/D**. Para el MXN es ambiguo: la dominancia fiscal en EUA debilitaría al USD, pero la prima por plazo global aprieta a los emergentes, y en 2026 domina esto último. En México, Banxico mantiene una tasa real de alrededor de 3%, así que no hay evidencia de captura (vigilar la retórica y la Junta).

### 4.7 Investigación nueva

- **Kalemli-Özcan y Varela (NBER w28923, revisado en ago-2026):** con encuestas de 22 emergentes y 12 avanzados, la prima de UIP emergente es más alta y volátil, la mueve el riesgo local, y la **incertidumbre de política** es su predictor más fuerte. En México, los eventos internos (la reforma judicial) mueven la prima, no sólo el VIX.
- **Bartram-Grinblatt-Xu (NBER w33423, 2025):** la restricción relativa de M1, medida con regresiones de panel fuera de muestra sobre datos de archivo, predice el rendimiento de las monedas de 1 mes a 3 años y **subsume al *carry***. Grado **C**: es un solo estudio y la señal cuesta construirla.
- **BIS Bulletin 90:** el *carry* moderno es apalancamiento con márgenes procíclicos. El *unwind* es rápido y se estabiliza si no hay daño de solvencia.

---

## 5. Evidencia real: qué funciona, qué no, magnitudes

### 5.1 Historia de las crisis del peso (magnitudes)

| Episodio | Detonador | Magnitud | Patrón |
|---|---|---|---|
| **1976** | Fin del tipo fijo de 12.50 (vigente desde 1954 (nv)) con déficit y deuda | **12.50 → 19.90** (ago) → **26.50** (oct). Unos 22 al cierre del sexenio | Tipo fijo sostenido con déficit. Es el origen del *peso problem* |
| **1982** | Caída del petróleo, deuda externa, tasas de Volcker | **25 → 47 en un día** (feb/mar-1982). Sexenio: 22.69 → 70. El 1-sep hubo **control de cambios y nacionalización de la banca**. Moratoria de deuda en agosto (nv) | Deuda externa en USD con el precio del petróleo en contra |
| **1994-95** | Déficit externo, Tesobonos en USD, reservas agotadas y *shocks* políticos | Del 19 al 22-dic-1994: **−29.1%** (3.46 → 4.89) y reservas **−43.8%** (10,457 → 5,881 mdd). **7.50 en mar-1995**. Rescate de **alrededor de US$50 mil millones** (EUA 20, FMI y otros alrededor de 30) | Crisis gemela, *sudden stop* y dolarización de pasivos (Calvo) |
| **2008-09** | Lehman y **derivados cambiarios corporativos** | **10.03 → 15.41** (31-jul-2008 → 2-mar-2009, **+53.5%**). Comercial Mexicana perdió **US$1,080 millones** y entró en concurso. Cemex reportó US$1,353 millones en instrumentos financieros. Pérdidas de alrededor de **US$2,200 millones** entre CCM, Gruma, Autlán, Posadas y GIS. Banxico vendió unos US$8,900 millones (Expansión) | Empresas "vendiendo volatilidad" del peso (apostando a su estabilidad) |
| **2013-16** | *Taper*, caída del petróleo y el alza de la Fed | **12.97 → 19.19** (jun-2014 → feb-2016, **+48%**). Ahí empezó el peor *drawdown* del *carry* (sección 5.2) | Lenta, no un *crash*. El *carry* no compensó |
| **2016-17** | Elección de Trump y amenaza al TLCAN | **18.64 → 21.89** (7-nov-2016 → 19-ene-2017, +17.5%). Máximo FIX de alrededor de 21.9 | Riesgo comercial binario |
| **2020** | COVID | **18.59 → 25.13** (19-feb → 24-mar-2020, **+35.2%**). Máximo FIX de **25.36** (23-mar) | *Risk-off* global puro |
| **2024** | Elección, reforma judicial y *unwind* del yen | **16.99 → 19.79** (31-may → 29-ago, +16.4%). En el año, **+23%** | Riesgo local más *carry* concurrido |
| **2025** | Aranceles de EUA | +3.0% (1-9 abr), y luego el peso se apreció 13.7% en el año | *Shock* de origen EUA: el peso no fue el perdedor |
| **2026** | Guerra de Irán y Fed/BoJ halcones | +5.2% (feb-mar). Peor semana en septiembre | Diferencial mínimo |

(Cifras de 2008 en adelante: cálculo propio con FRED DEXMXUS, tipo de cambio de mediodía en Nueva York, que no es el FIX. Antes de 2008: Wikipedia, Infobae y UNAM/Meganoticias.)

**Patrón (Inferencia):** las crisis grandes (1976, 1982, 1994) combinaron **tipo fijo o semifijo, deuda en dólares y reservas bajas**. Desde la flotación, las depreciaciones son **grandes pero reversibles**: +35% en 2020 y +54% en 2008, recuperadas en parte en uno o dos años. En la flotación, el peligro ya no es la devaluación discrecional. Es tener pasivos en USD, estar corto en volatilidad (derivados de 2008) o necesitar pesos justo en el pico.

### 5.2 El *carry* del peso, 1997-2026 (cálculo propio)

Se trata de un largo en MXN fondeado en USD. Tasas: interbancaria a 3 meses de México (OCDE, IR3TIB) contra el T-bill a 3 meses. Mensual, bruto, sin costos.

| Periodo | Rend. anual (arit./geo.) | Vol | Sharpe | Sesgo | Máx. DD | Corr. con S&P |
|---|---|---|---|---|---|---|
| 1997-2026 | 4.9% / 4.5% | 10.5% | 0.47 | −0.94 | **−33.0%** | +0.51 |
| 1997-2007 | 7.6% / 7.4% | 8.3% | 0.91 | −0.56 | −13.1% | +0.42 |
| 2008-2026 | 3.4% / 2.8% | 11.6% | **0.29** | −0.94 | −33.0% | +0.55 |
| 2016-2026 | 6.1% / 5.6% | 11.7% | 0.52 | −1.00 | −20.0% | +0.41 |
| ene-2023 a may-2024 | 17.5% (geo.) | 8.5% | ≈2.0 | −0.51 | −6.0% | +0.77 |
| jun a dic-2024 | −25.2% (geo., anualizado) | 7.8% | — | — | −15.6% | — |

- **Peores meses:** mar-2020 **−15.5%**, oct-2008 −13.1%, sep-2011 −10.1%, ago-1998 −9.4% y may-2012 −8.8%.
- ***Drawdowns* mayores a 10%:** 1998 (−10.5%), 2002-03 (−13.1%), **2008-09 (−30.4%, recuperado en abr-2011)**, 2011-12 (−15.2%), **abr-2013 a ene-2017 (−33.0%, recuperado apenas en nov-2022: unos 9.6 años bajo el agua)** y 2024 (−16.9%, recuperado en dic-2025).
- **Aritmética:** el diferencial promedio de 1997 a 2026 fue de **7.07 pp** y la depreciación promedio de USD/MXN de **2.67% anual**. El resto, alrededor de 4.4 pp, es la prima. De 2008 a 2026 el diferencial promedio bajó a 5.18 pp.
- **Lectura:** el *carry* del peso **sí** tiene prima positiva de largo plazo, lo cual es consistente con la UIP fallida y con Hassan-Mano. Pero decayó después de 2008 (Sharpe de 0.91 a 0.29), tiene sesgo negativo y está **correlacionado +0.5 con las acciones**. No diversifica un portafolio de acciones: suma al mismo riesgo. Grado **B**.

### 5.3 Momentum, valor y filtros en FX: lo que no sobrevive

- **Momentum FX (MSSS 2012):** ~10% bruto → ~4% con *spread* completo; concentrado en monedas menores con alto riesgo idiosincrático. Para una persona física en GBM **no es implementable** (no hay *forwards* minoristas en 48 monedas). **C**.
- **Reglas técnicas clásicas en FX** (medias móviles 1/20, 1/50, 1/200): ~5% anual con Sharpe 0.77-0.88 en 1976-2010 (MSSS, tabla 3), bien documentado su decaimiento posterior en la literatura (nv para cifras post-2010). **C**.
- **Filtros "prudentes" sobre el *carry* del MXN (cálculo propio, 1998-2026; parámetros estándar tomados de `parametros.json` y de la literatura, sin optimizar):**

| Regla | Rend. geo. | Vol | Sharpe | Máx. DD | Tiempo invertido |
|---|---|---|---|---|---|
| A. Siempre largo MXN | 4.2% | 10.6% | **0.44** | −33.0% | 100% |
| B. Sólo con VIX < 25 al cierre del mes previo (umbral de `filtro_apalancados`) | 2.6% | 8.2% | 0.35 | −32.5% | 79% |
| C. Sólo con USD/MXN bajo su media de 10 meses | 2.1% | 6.1% | 0.38 | −27.3% | 51% |
| D. B y C a la vez | 1.2% | 5.5% | 0.24 | −25.1% | 43% |

**Ningún filtro mejora el Sharpe y casi no reducen el *drawdown*.** El filtro de VIX llega tarde: el *crash* ocurre en el mismo mes en que sube el VIX. **Después** de un VIX por arriba de 30 (32 meses, agrupados en 1998, 2002, 2008, 2011 y 2020), el *carry* siguiente rindió **7.0% a 6 meses y 11.6% a 12 meses**, contra 2.4% y 4.9% incondicionales. Esto es consistente con BNP (un VIX alto predice más *carry* futuro), pero son pocos episodios independientes. Grado **C**. **Inferencia:** la prima se cobra **después** del pánico, no evitándolo.

### 5.4 La cobertura natural: el dólar como seguro del mexicano (cálculo propio)

**Correlación mensual de Δln(USD/MXN):**

| Periodo | Con el S&P 500 | Con ΔVIX | Vol. del S&P en USD | Vol. del S&P en MXN |
|---|---|---|---|---|
| 1996-2026 | **−0.50** | +0.47 | 15.3% | **13.6%** |
| 2008-2026 | −0.56 | +0.48 | 15.6% | 13.4% |
| 2016-2026 | −0.42 | +0.36 | 15.0% | 14.9% |
| 2023-2026 | −0.44 | +0.32 | 12.3% | 11.6% |

- **En los meses con el S&P abajo más de 5%** (n = 40, 1996-2026): el S&P promedió **−7.8% en USD**, USD/MXN **+3.7%** y el S&P en MXN **−4.5%**. El dólar absorbió alrededor de 40% del golpe.
- ***Drawdown* máximo del S&P (precio):** 2007-09 **−56.8% en USD contra −39.8% en MXN**. 2020 **−33.9% contra −15.0%**. **2022: −25.4% contra −27.4%.** En 2022 falló, porque Banxico subió más que la Fed, el *carry* favoreció al peso y el *shock* fue de inflación y tasas, no de pánico.
- **Episodios** (del inicio al mínimo del S&P): Lehman, S&P −46.6% en USD y **−18.2% en MXN**. COVID, −33.9% y **−10.7%**. Agosto de 2024, −6.1% y −1.8%. Irán 2026, −7.8% y −3.0%. **Aranceles de abr-2025, −11.5% y −9.9%** (casi sin cobertura).
- **CAGR del S&P (precio):** de 1996 a 2026, **8.17% en USD y 11.06% en MXN** (USD/MXN +2.67% anual). De 2016 a 2026, 13.48% en USD y **11.41% en MXN** (el peso se apreció −1.82% anual). La cobertura natural **no es gratis**: en años de *carry* alto con peso estable, cuesta el diferencial.
- **Coherencia con la literatura:** Campbell et al. (2010) encuentran que el USD se mueve contra las acciones mundiales, y el peso es el lado opuesto de esa moneda. **Grado A** para "el USD reduce la volatilidad y la cola de un portafolio medido en MXN en *shocks* globales". **B** para "siempre": falla en *shocks* de inflación con Banxico halcón (2022) y en *shocks* de origen EUA (abr-2025).

### 5.5 Distribución del tipo de cambio a 6 meses (horizonte de la temporada arena)

Cambios de USD/MXN en ventanas de 126 días hábiles, diarios de 1996 a 2026, traslapados: **p5 −8.7%, p25 −3.0%, mediana +0.4%, p75 +4.9%, p95 +16.4%**. P(> +10%) = **12.4%**. P(< −5%) = 15.8%. Volatilidad diaria anualizada de largo plazo: 10.9%.

**Lectura:** la cola derecha (el peso se desploma) es casi el doble de larga que la izquierda. En una temporada de 6 meses, con 5% de probabilidad en cada cola, **el tipo de cambio por sí solo mueve una cartera 100% en USD más de −9% o más de +16%**, medida en MXN.

### 5.6 Resumen de qué funciona

| Afirmación | Evidencia | Grado |
|---|---|---|
| La UIP falla y el *carry* tiene prima positiva de largo plazo | Fama, LRV y MXN propio (4.4 pp de prima 1997-2026) | **A** |
| La prima del *carry* es compensación por riesgo de *crash* (sesgo negativo, correlación con acciones) | BNP, LRV, Koijen et al. y MXN propio (sesgo −0.94, correlación +0.5) | **A** |
| El *carry* del MXN después de 2008 conserva un Sharpe atractivo | 0.29 en 2008-2026. Casi 10 años bajo el agua entre 2013 y 2022 | **C** |
| Pronosticar el USD/MXN a 6-12 meses con fundamentales o PPP | Meese-Rogoff y Rogoff | **D** |
| El momentum FX es explotable por una persona física | MSSS: se cae neto de *spreads* y exige *forwards* en muchas monedas | **D** |
| Los filtros de VIX o tendencia protegen el *carry* sin perder rendimiento | MXN propio: bajan el Sharpe | **D** |
| Un VIX alto (> 30) predice mejor *carry* posterior | BNP y MXN propio (32 meses) | **C** |
| El USD sin cubrir es la cobertura natural de un portafolio en MXN | Correlación de −0.42 a −0.56. *Drawdowns* de 2008 y 2020 | **A/B** |
| El *nearshoring* sostiene la apreciación del peso | IED nueva = 7.8% del total | **D** |
| Dalio como reloj de crisis | Sin registro fechado verificable | **D** |

---

## 6. Traducción operable

### 6.1 Principio rector

Para un inversionista que mide en MXN, **la decisión cambiaria es la más grande y la más barata del portafolio**. Es la más grande porque el USD/MXN tiene una volatilidad de alrededor de 11% y se correlaciona con todo lo demás. Es la más barata porque se ejecuta eligiendo entre activos en pesos y activos en dólares, sin derivados. El benchmark principal de `parametros.json` (50% S&P 500 TR en MXN + 50% CETES 28) **ya tiene 50% de exposición al USD sin cubrir**, así que la exposición neutral es 50%.

### 6.2 Reglas para el patrimonio principal (propuesta, no modifica `parametros.json`)

1. **Exposición USD neutral: 50%. Rango permitido: 35-70%.** Se cuenta como exposición USD todo activo cuyo valor en USD no cambia con el peso: acciones y ETFs del SIC, T-bills y bonos en USD y efectivo en USD.
2. **Movimientos de 10 pp como máximo por mes**, ejecutados con las bandas de rebalanceo (`banda_absoluta` 0.05) y registrados con el FX de ejecución en GBM (el FIX no es un precio ejecutable).
3. **Sesgo actual (Inferencia, confianza media): la mitad superior del rango (55-65% en USD).** Por tres razones: (a) el costo de oportunidad de no tener *carry* es el **menor en más de una década** (250-275 pb); (b) Fed y BoJ están apretando y el peso real está en el percentil 73; (c) la cola derecha del USD/MXN es el doble de gruesa. Se revierte hacia 50% si el diferencial vuelve a más de 400 pb con volatilidad implícita normal.
4. **Acciones de EUA: nunca se cubren** en el patrimonio principal (sección 5.4).
5. **Renta fija en USD:** sólo se tiene si su función es **ser el seguro en dólares**. Si la función es rendimiento, se sustituye por CETES, Bonos M o Udibonos, porque "USD cubierto a MXN" ≈ tasa en pesos y replicarlo sale más caro que comprar el instrumento local.
6. **Pasivos:** los gastos en MXN de los próximos 12 meses deben estar en MXN (reserva de emergencia de 6 meses, fuera del portafolio según `liquidez`). Los gastos en USD (viajes, colegiaturas o deudas en USD) deben estar en USD. La cobertura se hace **contra pasivos**, no contra la opinión sobre el peso.
7. **Prohibido:** ***carry* apalancado** y vender volatilidad del peso con derivados (la lección de 2008). Con `apalancamiento.bruto_max_fase_1` = 1.0 ni siquiera cabe.

### 6.3 Reglas para la cuenta arena (temporadas de 6 meses, TWR en MXN)

- **La exposición cambiaria es una apuesta relativa.** Con MXN 20,000 en GBM, lo más probable es que los rivales compren acciones o ETFs de EUA en el SIC. Su exposición al USD es alta y **ninguno la cubre**, porque no hay *forwards* minoristas (Inferencia; no se conocen sus posiciones). Entonces:
  - **Adelante del mejor rival por 5 pp o más** (`ventaja_para_bajar_varianza_pp`): se iguala la exposición USD "de consenso" (70-100%) para que el tipo de cambio no cambie el orden.
  - **Atrás del mejor rival por 5 pp o más** (`desventaja_para_subir_exposicion_pp`): una sobreexposición al MXN (CETES o acciones mexicanas) es una fuente **barata** de varianza relativa, pero sólo con señal de grado C o mejor: VIX por arriba de 30 y ya bajando de 25, o diferencial arriba de 400 pb. **Hoy no hay señal**, porque el diferencial está en 250-275 pb.
- **Tamaño del riesgo cambiario:** un 10% de alza de USD/MXN (probabilidad de alrededor de 12% en 6 meses) mueve la cuenta en 10% × (fracción en MXN) **contra** los rivales dolarizados. Una posición en MXN del 50% implica un riesgo relativo de −5 pp en ese escenario. Esto se compara con `limites_perdida.mensual` (0.18) y con los cortacircuitos (−12%).
- **Operaciones:** los cambios de exposición cambiaria cuentan dentro de `operaciones_max_mes` = 8.
- **Filtro de apalancados:** los ETFs apalancados en USD, además del filtro de media móvil de 200 días con VIX < 25, suman riesgo cambiario. Su exposición en MXN se calcula con la fórmula de las ideas adoptadas, punto 7.

### 6.4 Cuándo cubrir y cuándo no

| Situación | ¿Cubrir el USD (pasarlo a MXN)? | Motivo |
|---|---|---|
| Acciones globales, horizonte de más de 1 año | **No** | Correlación de −0.5. *Drawdown* de −40% contra −57% (2008) y de −15% contra −34% (2020) |
| Bonos o efectivo en USD con fin de rendimiento | **Sí** (sustituir por deuda en MXN) | La vol del FX domina a la del bono (Campbell et al.) |
| Gasto en MXN a menos de 12 meses | **Sí** (tenerlo en MXN) | Calce de pasivos |
| Gasto o deuda en USD | **No** | Calce de pasivos |
| *Shock* global de pánico (tipo A o B del cap. 23) en curso | **No** (no vender dólares en el pico sin plan) | El USD ya pagó el seguro. Rebalancear sólo con las bandas |
| *Shock* originado en EUA (tipo C) | **Diversificar fuera del USD** (oro, CHF, JPY o EUR) en lugar de cubrir a MXN | En abr-2025 el peso casi no se depreció |
| *Shock* de inflación global con Banxico más halcón que la Fed | **Parcial**: subir la deuda en MXN de tasa real alta | En 2022 la cobertura natural falló |
| Diferencial mayor a 500 pb, vol normal y VIX bajando tras un pico | **Considerar** bajar la exposición USD hacia 40% | Ventana histórica de *carry* (grado C) |
| Diferencial menor a 300 pb y bancos centrales del G10 apretando (hoy) | **No bajar** la exposición USD | Poco *carry* por cargar la cola |

**Instrumentos minoristas:** en GBM la "cobertura" se hace eligiendo el activo (CETES o fondos de deuda en MXN contra ETFs del SIC). Los futuros de dólar de MexDer tienen contratos de USD 10,000 (nv), demasiado grandes para MXN 20,000. Los ETFs con cobertura cambiaria listados en la BMV se deben verificar uno por uno: existencia, costo, liquidez y *tracking*.

### 6.5 Tablero cambiario semanal (conectar con el cap. 22 y con `herramientas/tablero.py`)

| Indicador | Fuente | Umbral de alerta (Inferencia, calibrado con este capítulo) |
|---|---|---|
| USD/MXN spot y FIX | Banxico, FRED DEXMXUS | +5% en 10 días hábiles → protocolo 6.7 |
| Diferencial Banxico − Fed y TIIE a 28/91 días contra T-bill | Banxico y FRED | Menos de 300 pb → no hay sobrepeso en MXN. Más de 500 pb → ventana de *carry* |
| *Carry*/vol (diferencial ÷ vol implícita a 1 mes, o realizada si no hay implícita) | Cálculo | Menos de 0.3 → peso "caro por riesgo" |
| VIX | FRED VIXCLS | Más de 25 → nada de *carry* nuevo. Arriba de 30 y luego bajo 25 → ventana de *carry* (C) |
| Dólar amplio (DTWEXBGS) y DXY | FRED | Dólar débil con VIX alto → posible *shock* tipo C |
| UST 10 años, TIPS y *breakeven* | FRED | *Breakeven* arriba de 2.8% con la Fed en pausa → vigilar dominancia fiscal |
| BoJ, USD/JPY y préstamo en yenes | Prensa y BIS | Alza del BoJ con el yen apreciándose rápido → riesgo de *unwind* |
| Posicionamiento especulativo en MXN | CFTC COT (futuros CME) | Máximos de 2 años en largos → riesgo de *unwind* (C) |
| Calificaciones y Pemex | Moody's, S&P y Fitch | Cualquier baja a *junk* soberana → protocolo 6.7 |
| Calendario del T-MEC | USTR y SE | Rondas y fechas de revisión anual: registrar un pronóstico antes |
| Remesas e IED (nueva contra reinversión) | Banxico y SE | Tendencia, no gatillo |
| Tipo de cambio real BIS | FRED RBMXBIS | Arriba del percentil 85 → sesgo estructural a USD (horizonte de años) |

### 6.6 *Checklist* antes de cualquier decisión motivada por el tipo de cambio

- [ ] ¿La decisión es contra un **pasivo** o contra una **opinión**? Si es contra una opinión, necesita una señal de grado C o mejor y un pronóstico registrado con probabilidad (`pronosticos.brier_objetivo` 0.2).
- [ ] ¿Cuál es la exposición USD actual contra la neutral (50%) y contra la de "consenso" de los rivales?
- [ ] ¿Qué tipo de *shock* (A-E del cap. 23) cubre o expone este cambio?
- [ ] ¿Cuánto *carry* se gana o se pierde por año con el diferencial de hoy?
- [ ] ¿Qué pasa en el escenario p95 (+16% de USD/MXN en 6 meses) y en el p5 (−9%)?
- [ ] ¿Respeta las bandas, `operaciones_max_mes` y los límites de pérdida?
- [ ] ¿Se registró el FX de ejecución (no el FIX), la hora y la fuente?

### 6.7 Protocolo de estrés del peso (USD/MXN +5% en 10 días, o una degradación soberana)

1. **En la primera hora, clasificar** el *shock*: global (A o B, el USD protege), de origen EUA (C, el USD puede no proteger) o local (reforma, calificación o Pemex, el USD protege y el *carry* no compensa).
2. **No vender dólares en el pico** para "aprovechar". Sólo se rebalancea cuando la exposición USD sale de la banda por más de 5 pp, y en tercios.
3. **Local con degradación a *junk***: reducir la deuda mexicana de plazo largo y la deuda de Pemex, y no promediar el primer día.
4. **Global con VIX arriba de 30:** registrar el pronóstico "el *carry* rendirá más de 5% en los próximos 6 meses" y **esperar a que el VIX baje de 25** para considerar un sobrepeso en MXN (grado C, tamaño chico).
5. Hacer un *post-mortem* con el formato del cap. 23: ¿funcionó la cobertura natural?, ¿el tipo de *shock* estaba bien asignado?

### 6.8 Parámetros propuestos (para revisión con el dueño; no están en `parametros.json`)

```json
"divisas": {
  "exposicion_usd_neutral": 0.50,
  "exposicion_usd_rango_patrimonio": [0.35, 0.70],
  "cambio_max_mensual_pp": 0.10,
  "cubrir_acciones_usd": false,
  "diferencial_min_para_sobrepeso_mxn_pb": 400,
  "carry_vol_min_para_sobrepeso_mxn": 0.3,
  "vix_max_para_carry_nuevo": 25,
  "alerta_depreciacion_10d": 0.05,
  "arena_exposicion_usd_si_adelante": "igualar consenso estimado (0.7-1.0)"
}
```

---

## 7. Trampas y errores comunes

1. **Confundir las convenciones.** Que el USD/MXN suba 23% significa que el peso cayó 19%.
2. **Leer el *forward* como pronóstico.** Está 2.5-2.75% arriba del spot por aritmética de tasas. En promedio, el peso no se deprecia eso.
3. **Tratar el diferencial como ganancia segura.** El *carry* del MXN tuvo un *drawdown* de −33%, **9.6 años bajo el agua** (2013-2022) y un mes de −15.5% (mar-2020).
4. **Creer que CETES diversifica las acciones.** Estar en CETES es estar largo en *carry*, con correlación de +0.5 con las acciones. Lo que diversifica es el dólar.
5. **Operar a 6 meses con PPP o tipo de cambio real.** Con una vida media de 3-5 años, eso es ruido.
6. **Poner filtros "prudentes".** El filtro de VIX < 25 bajó el Sharpe del *carry* de 0.44 a 0.35 y no evitó el *crash*.
7. **Suponer que el dólar siempre protege.** No protegió en abr-2025 (*shock* de origen EUA) ni en 2022 (*shock* de tasas con Banxico halcón).
8. **Confundir narrativa con flujo.** El *nearshoring* es sólo 7.8% de IED nueva, y el "super peso" era *carry* concurrido.
9. **Usar a Dalio o la "dominancia fiscal" como gatillo.** En 2026 subieron las tasas reales, no los *breakevens*, y el oro cayó alrededor de 22%.
10. **Medir en USD y reportar en MXN, o usar el FIX como precio ejecutable.**
11. **Olvidar que el benchmark ya es 50% USD.** Refugiarse en CETES "por miedo" es apostar 50 pp contra el dólar.
12. **Vender volatilidad del peso** (derivados de rango, *notes* que pagan si el peso no se deprecia), que fue el error de 2008. También tomar las cifras brutas de momentum FX (10%) como si fueran netas (alrededor de 4%).

---

## 8. Examen de titulación

1. **Con Banxico en 6.50% y la Fed en 3.875% (punto medio), ¿cuánto cotiza el *forward* a 1 año sobre un spot de 17.71? ¿Qué implica para el valor esperado?**
   Unos 17.71 × 1.065/1.03875 ≈ **18.16**. No implica que el mercado espere 18.16: es la CIP. Con la UIP fallida, en promedio el spot futuro queda **debajo** del *forward*, y esa diferencia es la prima del *carry*.

2. **¿Qué encontró Fama (1984) y cuál es la réplica para el MXN?**
   Una pendiente negativa de Δs sobre (f − s), con casi toda la variación del *forward* como prima por riesgo. Para el MXN (1997-2026) la réplica da β = −0.07 (e.e. 0.39): la UIP se rechaza a unos 2.7 e.e., pero en submuestras la estimación es ruido.

3. **Según Hassan-Mano, ¿qué parte de la anomalía es robusta?**
   La **transversal**: algunas monedas pagan persistentemente más. El FPP de series de tiempo y el *dollar trade* son frágiles.

4. **¿Por qué el *carry* tiene sesgo negativo y qué predice un VIX alto?**
   Porque los *unwinds* son súbitos cuando caen el apetito por riesgo y la liquidez de fondeo (BNP 2008). Un VIX o un TED alto predicen mayor rendimiento **posterior** del *carry*. En el MXN, tras un VIX > 30, dio 7.0% a 6 meses contra 2.4% incondicional (grado C).

5. **Da el Sharpe del *carry* MXN antes y después de 2008, y su peor *drawdown*.**
   0.91 (1997-2007) y 0.29 (2008-2026). El peor *drawdown* fue de −33% entre abr-2013 y ene-2017, recuperado hasta nov-2022.

6. **¿Qué dicen LRV (2011) y Verdelhan (2018)?**
   Dos factores, dólar y *carry*, explican el corte transversal. HML_FX rindió 4.8% neto con Sharpe 0.54 (1983-2008). Esos dos factores explican entre 18% y 80% de los movimientos mensuales bilaterales.

7. **¿Cuál es la vida media de la PPP y qué implica para una temporada de 6 meses?**
   De 3 a 5 años (Rogoff 1996). A 6 meses, el tipo de cambio real no da señal de *timing*.

8. **Explica el "dilema, no trilema" de Rey.**
   El ciclo financiero global, movido en parte por la Fed y ligado al VIX, limita la política monetaria de cualquier país con cuenta abierta, sin importar su régimen cambiario. Sólo hay independencia si se administra la cuenta de capital.

9. **¿Qué combinación de vulnerabilidades señalan Calvo-Izquierdo-Mejía y qué tenía México en 1994?**
   Poca apertura (pocos comerciables) junto con dolarización de pasivos, en una relación no lineal. En 1994 México tenía Tesobonos en USD, tipo semifijo y reservas que cayeron 43.8% en tres días.

10. **¿Cuánto redujo el USD el *drawdown* del S&P para un mexicano en 2008 y en 2020? ¿Cuándo falló?**
    En 2008 de −56.8% a −39.8%. En 2020 de −33.9% a −15.0%. Falló en 2022 (−25.4% contra −27.4%, *shock* de tasas con Banxico halcón) y casi no ayudó en abr-2025 (*shock* de origen EUA).

11. **¿Por qué no cubrir acciones de EUA pero sí sustituir los bonos en USD con fin de rendimiento?**
    En acciones, la correlación negativa del USD/MXN reduce la volatilidad y la cola. En bonos, la volatilidad del FX domina a la del bono. "USD cubierto" ≈ tasa en MXN, así que conviene comprar deuda en pesos directamente (Campbell et al. 2010).

12. **¿Qué demuestra y qué no el récord de IED del 1S-2026?**
    Demuestra que las empresas reinvierten utilidades en México. No demuestra una ola de *nearshoring*: la inversión nueva es sólo 7.8% del total y cayó 13%.

13. **¿Hay dominancia fiscal en EUA según los precios de sep-2026?**
    No en los precios. El UST a 10 años está en 5.11%, con real de 2.76% y *breakeven* de 2.33%, y la Fed subió tasas. Lo que sube es la prima real y por plazo, no la inflación esperada. El riesgo institucional es de cola (grado C).

14. **En la arena vas 6 pp detrás del mejor rival. El diferencial está en 260 pb y el VIX en 15. ¿Sobrepesas el MXN?**
    No. `modo_torneo` permite subir la varianza relativa, pero la apuesta en MXN no tiene señal: el *carry* es mínimo y la Fed y el BoJ aprietan. Se busca varianza relativa con otra fuente de ventaja validada, o se espera la ventana posterior a un pico del VIX.

15. **¿Qué lección de 2008 aplica a una persona física?**
    Nunca estar corto en volatilidad del peso (derivados de "rango", *notes* que pagan si el peso no se deprecia). Pagan poco en años tranquilos y pueden quebrar la cuenta en un *risk-off*. Comercial Mexicana perdió US$1,080 millones.

---

## 9. Fuentes

1. Fama (1984), "Forward and spot exchange rates", JME: https://ideas.repec.org/a/eee/moneco/v14y1984i3p319-338.html · PDF: https://eml.berkeley.edu/~craine/EconH195/Fall_09/webpage/Fama_Forward%20Discount.pdf · Pendientes por horizonte (revisión): https://www.sciencedirect.com/science/article/abs/pii/S0378426613002550
2. Lustig, Roussanov y Verdelhan (2011), "Common Risk Factors in Currency Markets", RFS: https://academic.oup.com/rfs/article-abstract/24/11/3731/1589752 · WP con cifras: https://www.nber.org/papers/w14082
3. Brunnermeier, Nagel y Pedersen (2008), "Carry Trades and Currency Crashes": https://www.nber.org/papers/w14473
4. Menkhoff, Sarno, Schmeling y Schrimpf (2012), "Currency momentum strategies", JFE: https://ideas.repec.org/a/eee/jfinec/v106y2012i3p660-684.html · PDF: https://faculty.washington.edu/ss1110/IF/Sarno%20Currency%20Momentum%20JFE%20(1).pdf
5. Rogoff (1996), "The Purchasing Power Parity Puzzle", JEL: https://www.sfu.ca/~kkasa/rogoff96.pdf
6. Meese y Rogoff (1983), JIE: https://ideas.repec.org/a/eee/inecon/v14y1983i1-2p3-24.html
7. Lustig, Roussanov y Verdelhan (2014), "Countercyclical currency risk premia", JFE: http://web.mit.edu/adrienv/www/LRV_JFE_2014.pdf · https://www.nber.org/papers/w16427
8. Verdelhan (2018), JF: https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12587
9. Rey (2013), "Dilemma not Trilemma", Jackson Hole: https://www.kansascityfed.org/Jackson%20Hole/documents/4575/2013Rey.pdf · https://www.nber.org/papers/w21162
10. Miranda-Agrippino y Rey (2020), RES: https://academic.oup.com/restud/article/87/6/2754/5834728
11. Kaminsky y Reinhart (1999), "The Twin Crises", AER: https://www.aeaweb.org/articles?id=10.1257%2Faer.89.3.473 · IFDP: https://www.federalreserve.gov/econres/ifdp/the-twin-crises-the-causes-of-banking-and-balance-of-payments-problems.htm
12. Reinhart y Rogoff, *This Time Is Different*: https://press.princeton.edu/books/paperback/9780691152646/this-time-is-different · "The Aftermath of Financial Crises": https://www.nber.org/papers/w14656
13. Calvo (1998), "Capital Flows and Capital-Market Crises": https://ucema.edu.ar/publicaciones/download/volume1/calvo.pdf
14. Calvo, Izquierdo y Mejía (2004), "On the Empirics of Sudden Stops": https://www.frbsf.org/wp-content/uploads/Calvo.pdf
15. Campbell, Serfaty-de Medeiros y Viceira (2010), "Global Currency Hedging", JF: https://www.nber.org/papers/w13088
16. Engel (2016), "Exchange Rates, Interest Rates, and the Risk Premium", AER: https://www.nber.org/papers/w21042
17. Hassan y Mano (2019), QJE: https://www.nber.org/papers/w20294
18. Jiang, Krishnamurthy y Lustig (2021), JF: https://www.nber.org/papers/w24439
19. Daniel, Hodrick y Lu (2017), CFR: https://www.nber.org/papers/w20433
20. Koijen, Moskowitz, Pedersen y Vrugt, "Carry": https://www.nber.org/papers/w19325
21. Kalemli-Özcan y Varela, "Five Facts about the UIP Premium": https://www.nber.org/papers/w28923
22. Bartram, Grinblatt y Xu (2025), "Monetary Policy Predicts Currency Movements": https://www.nber.org/papers/w33423
23. BIS Bulletin 90, "The market turbulence and carry trade unwind of August 2024": https://www.bis.org/publ/bisbull90.htm
24. Dalio, *How Countries Go Broke*: https://economicprinciples.org/how-countries-go-broke · Reseña de AIER: https://thedailyeconomy.org/article/debt-destiny-and-dalio-a-review-of-how-countries-go-broke/ · Reseña: https://frankdiana.net/2025/09/29/book-review-how-countries-go-broke-the-big-cycle-by-ray-dalio/ · Perfil y críticas: https://en.wikipedia.org/wiki/Ray_Dalio
25. Cecchetti y Schoenholtz, "Fiscal Dominance: A Primer" (oct-2025): https://www.moneyandbanking.com/primers/2025/10/25/fiscal-dominance-a-primer
26. Debate 2026 (ASSA, CBO vía fuente secundaria): https://www.faf.ae/home/2026/1/5/the-federal-reserve-confronts-a-fiscal-dominance-crisis-how-washingtons-debt-could-force-the-central-bank-to-abandon-its-inflation-mandate · OMFIF: https://www.omfif.org/2025/09/fed-treasury-tensions-and-the-risk-of-fiscal-dominance/
27. El Financiero, cierre del peso del 24-sep-2026: https://www.elfinanciero.com.mx/mercados/2026/09/24/peso-dolar-precio-hoy-24-de-septiembre-de-2026/
28. El Financiero, "Los 'estate quieto' que aplacaron al superpeso": https://www.elfinanciero.com.mx/economia/2026/09/24/los-estate-quieto-que-aplacaron-al-superpeso-hay-riesgo-de-una-depreciacion-mayor/
29. El Financiero, el peor día del peso en 6 meses: https://www.elfinanciero.com.mx/economia/2026/09/24/peso-registra-su-peor-jornada-en-6-meses-y-alcanza-175-unidades-por-dolar/
30. Expansión, Banxico mantiene 6.5% (24-sep-2026): https://expansion.mx/economia/2026/09/24/banxico-tasa-de-interes-de-referencia-6-5-septiembre · PorEsto: https://www.poresto.com/mexico/2026/9/24/banxico-mantiene-tasa-de-interes-en-650-y-preve-que-inflacion-llegue-a-la-meta-hasta-finales-de-2027.html
31. CNBC, UST a 10 años en máximo de 19 años (23-sep-2026): https://www.cnbc.com/2026/09/23/treasury-yields-oil-inflation-fed.html
32. CNBC, el BoJ sube a 1.25% (18-sep-2026): https://www.cnbc.com/2026/09/18/japan-raises-rates-30-year-high-yen-jgb.html · Bloomberg: https://www.bloomberg.com/news/articles/2026-09-18/bank-of-japan-hike-could-reshape-yen-carry-trade
33. Bloomberg Línea, Moody's baja a México a Baa3 (20-may-2026): https://www.bloomberglinea.com/latinoamerica/mexico/mexico-queda-en-el-ultimo-escalon-de-grado-de-inversion-con-moodys-y-fitch/ · El CEO, calificaciones 2026: https://elceo.com/economia/estas-son-las-calificaciones-crediticias-de-mexico-en-2026-segun-sp-fitch-y-moodys/
34. Pemex: Moody's B1 (El Financiero, 22-may-2026): https://www.elfinanciero.com.mx/economia/2026/05/22/pemex-se-salva-de-ser-reprobado-por-moodys-su-calificacion-queda-en-b1-con-perspectiva-estable/ · Fitch BB+: https://www.bloomberglinea.com/latinoamerica/mexico/fitch-mantiene-calificacion-de-pemex-como-bono-basura-a-un-escalon-del-grado-de-inversion/
35. White & Case, revisión del T-MEC de 2026: https://www.whitecase.com/insight-alert/usmca-2026-joint-review-united-states-declines-extend-agreement-triggering-annual · AS/COA: https://www.as-coa.org/articles/tracking-us-mexico-talks-usmca-review · Rio Times (llamada del 16-sep-2026): https://www.riotimesonline.com/trump-sheinbaum-call-mexico-us-trade-deal-september-2026/
36. Remesas 2025 (BBVA Research): https://www.bbvaresearch.com/en/publicaciones/mexico-11-consecutive-years-of-remittance-growth-end-falling-46-in-2025/ · Julio 2026 (El Financiero): https://www.elfinanciero.com.mx/economia/2026/09/01/remesas-enviadas-a-mexico-se-sacuden-el-polvo-crecen-3-en-julio-y-ligan-seis-meses-al-alza/ · Impuesto de 1% (OBBBA): https://en.wikipedia.org/wiki/One_Big_Beautiful_Bill_Act
37. IED 1S-2026 (Secretaría de Economía): https://www.gob.mx/se/prensa/mexico-registra-un-maximo-historico-de-inversion-extranjera-directa-ied-para-un-primer-semestre-34-mil-968-millones-de-dolares-en-2026 · El Financiero: https://www.elfinanciero.com.mx/economia/2026/08/25/inversion-extranjera-directa-ied-en-mexico-alcanza-nivel-historico-al-cierre-del-primer-semestre/
38. Banxico, coberturas cambiarias: https://www.banxico.org.mx/mercados/subastas-coberturas-cambiaria.html · Reducción de ago-2023: https://expansion.mx/economia/2023/08/31/comision-de-cambios-reduce-coberturas-cambiarias
39. Encuesta trienal BIS 2025, reporte de Banxico: https://www.banxico.org.mx/markets/central-bank-surveys-of-foreign-exchange-and-deriv/%7BAD2EB8E3-502A-5705-6E63-B14B7C1867AD%7D.pdf
40. El peso en 2024: https://www.elfinanciero.com.mx/mercados/2024/12/31/mal-ano-para-ser-peso-mexicano-tiene-en-2024-su-mayor-depreciacion-en-16-anos/ · https://www.elimparcial.com/dinero/2025/01/01/el-2024-fue-el-peor-ano-para-el-peso-desde-2008/ · https://www.mexperience.com/2024-was-a-year-of-two-halves-for-the-mexican-peso/ · Bloomberg (abr-2024): https://www.bloomberg.com/news/articles/2024-04-16/massive-global-carry-trade-unwinding-hits-the-super-peso
41. Historia de las devaluaciones: https://es.wikipedia.org/wiki/Devaluaci%C3%B3n_del_peso_mexicano · 1994: https://www.meganoticias.mx/cdmx/noticia/error-de-diciembre-cuando-el-dinero-dejo-de-alcanzar/687931 · Máximo de 2020: https://mvsnoticias.com/economia/2024/10/18/cual-es-el-precio-maximo-al-que-ha-estado-el-dolar-en-mexico-655855.html
42. Derivados de 2008: https://expansion.mx/expansion/2008/11/12/doble-o-nada · https://expansion.mx/negocios/2008/10/15/derivados-maldicion-del-peso-y-empresas
43. Series FRED usadas en los cálculos propios (descargadas el 2026-09-25): DEXMXUS https://fred.stlouisfed.org/series/DEXMXUS · IR3TIB01MXM156N https://fred.stlouisfed.org/series/IR3TIB01MXM156N · TB3MS https://fred.stlouisfed.org/series/TB3MS · VIXCLS https://fred.stlouisfed.org/series/VIXCLS · DGS10, DFII10, T10YIE, DTWEXBGS, RBMXBIS y TRESEGMXM052N (misma raíz https://fred.stlouisfed.org/series/)
44. S&P 500 (^GSPC, Yahoo Finance, 30 años diarios): https://finance.yahoo.com/quote/%5EGSPC/history

**Registro de verificación (2026-09-25):** 35 búsquedas web y alrededor de 34 lecturas de páginas y PDFs (MSSS 2012, BNP 2008, LRV 2008 y Calvo-Izquierdo-Mejía 2004 leídos en texto completo). Cálculos propios reproducibles con `herramientas/datos.py`. **Pendiente de verificar:** el estado 2024-2026 del programa de coberturas de Banxico, el tamaño del contrato de dólar en MexDer, la muestra exacta de Kaminsky-Reinhart, el número de casos de *Big Debt Crises*, el tipo fijo "desde 1954", la fecha de la moratoria de 1982, el mandato exacto de los índices ante una degradación a *junk* y las cifras de la CBO (vistas sólo por fuente secundaria).
