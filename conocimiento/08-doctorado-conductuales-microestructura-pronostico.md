# Módulo 08: Finanzas conductuales, microestructura y ciencia del pronóstico

> Nivel: doctorado · Actualizado: 2026-09-25 · Grado de evidencia global: **B**. Lo que **destruye** rendimiento del minorista es grado **A**: sobretrading, day trading, compras por atención y efecto disposición, replicado con cifras netas en EUA, Taiwán y Brasil, con evidencia conductual adicional en Finlandia y Países Bajos. Que un minorista **cobre** esos sesgos ajenos es grado **C**: las anomalías conductuales viven sobre todo en la pierna corta y decaen tras publicarse. La ciencia del pronóstico es grado **A** en geopolítica, pero su traslado a mercados es **C** porque no hay evidencia auditada.

**Método de verificación.** Con el presupuesto de WebSearch agotado, las citas se confirmaron con Crossref, Semantic Scholar, arXiv, Europe PMC, govinfo.gov, el blog del FRI, el archivo de Mauboussin y PDFs de autores (Odean, Tóth et al., meta-análisis de UGent). Lo no confirmado dice "(no verificado)"; los cálculos propios, "Inferencia".

Enlaces internos que este módulo no repite: cap. 06 (decaimiento de anomalías y Sharpe deflactado), cap. 09 (IA/LLM en inversión), cap. 20 (econometría y métricas), cap. 25 (pronóstico de reportes), `arena/investigacion/01-gbm-operativa-y-costos.md` (costos reales en GBM) y `arena/investigacion/03-teoria-de-torneos-y-estrategia-competitiva.md` (torneos y Alpha Arena).

---

## 1. Objetivos de dominio (qué debe saber hacer quien "se titula" en este módulo)

1. Escribir la función de valor y la de ponderación de probabilidades de prospect theory, y explicar con ellas el efecto disposición, el efecto "house money", el de "break-even" y la aversión miope a las pérdidas.
2. Medir el efecto disposición propio (PGR − PLR) con la bitácora y ponerle precio en pp/año con la evidencia de Odean (1998).
3. Citar de memoria las cifras de sobretrading y day trading (EUA, Taiwán y Brasil) y usarlas como tasa base contra cualquier plan de trading activo.
4. Explicar por qué una ineficiencia puede persistir (límites al arbitraje, riesgo de noise traders) y en qué pierna vive (corta y difícil de arbitrar).
5. Derivar el λ de Kyle y el spread de Glosten-Milgrom. Estimar el spread con Roll o con Corwin-Schultz y el impacto con la ley de raíz cuadrada. Decidir qué costo domina en una cuenta de 20,000 MXN.
6. Saber qué es el PFOF, qué encontró la evidencia (2023-2025) sobre calidad de ejecución y qué pasó con la reforma de la SEC en 2025.
7. Calcular Brier, su descomposición de Murphy, el skill score y la tabla de calibración, y decir cuántos pronósticos hacen falta para distinguir habilidad de suerte.
8. Aplicar la vista externa (tasa base), el pre-mortem, el checklist y el diario de decisiones, y separar calidad de decisión de resultado.
9. Conocer lo que se sabe de fisiología del trader (testosterona, cortisol, sueño y fatiga), incluidos sus límites muestrales.
10. Convertir todo en protocolos anti-sesgo coherentes con `config/parametros.json`: así se le gana a rivales que no los tienen.

---

## 2. Núcleo teórico (conceptos, fórmulas en texto/LaTeX simple, intuición económica)

### 2.1 Prospect theory
- **Valor sobre cambios, no sobre riqueza** [1][2]: v(x) = x^α si x ≥ 0 y v(x) = −λ(−x)^β si x < 0.
  - Tversky-Kahneman (1992) reportaron **medianas** α = β = 0.88 y λ = 2.25. Salieron de **25 estudiantes de posgrado, en experimentos sin incentivo monetario**, y no reportaron dispersión [3].
  - La meta-análisis de 607 estimaciones (150 artículos) da **λ medio = 1.955, IC95% [1.820, 2.102]**, con mediana cruda de 1.69 [3].
  - Gal-Rucker (2018) sostienen que la evidencia no muestra que las pérdidas pesen más en general [4].
- **Ponderación de probabilidades** (forma TK92): w(p) = p^γ / (p^γ + (1−p)^γ)^{1/γ}. Sobrepondera probabilidades chicas. Inferencia: de ahí sale la demanda de "loterías" (opciones OTM, acciones de centavos, 0DTE). Los valores γ = 0.61 (ganancias) y δ = 0.69 (pérdidas) son los que se suelen atribuir a TK92 **(no verificado en fuente primaria)**.
- **Intuición.** Concavidad en ganancias: vender ganadoras. Convexidad en pérdidas: apostar para "recuperar". λ > 1 con evaluaciones frecuentes da **aversión miope a las pérdidas**, que Benartzi-Thaler (1995) proponen para explicar la prima de acciones [5].
- **Resultados previos** (Thaler-Johnson 1990) [6]:
  - efecto "house money": más riesgo después de ganar;
  - efecto "break-even": después de perder atraen las apuestas que ofrecen salir tablas.
  - Jelschen-Schmidt (2023, *JRU* 66(3)) replican con ganancias caídas del cielo, pero encuentran el "house money" puro menos ubicuo.

### 2.2 Efecto disposición y sobreconfianza
- **Métrica** (Odean 1998) [8]:
  - PGR = ganancias realizadas / (ganancias realizadas + ganancias en papel);
  - PLR = lo mismo con pérdidas;
  - DE = PGR − PLR.
- **Marco de Shefrin-Statman (1985)** [7]: aversión a realizar pérdidas + contabilidad mental + aversión al arrepentimiento + autocontrol.
- **Sobreconfianza** (Gervais-Odean) [103]: el trader se atribuye los aciertos, aprende a sobreestimarse y opera de más.
  - Gödker-Odean-Smeets (2023) conectan las dos piezas. Quien vende más a menudo con ganancia termina **más sobreconfiado**, porque evalúa su habilidad por ganancias realizadas y no por el rendimiento del portafolio [42].
  - Chague et al. (2023): los day traders juzgan su habilidad por la **proporción de días ganadores**. El efecto disposición la infla de 48% (contrafactual) a **54% observado** [19].

### 2.3 Límites al arbitraje, noise traders y sentimiento
- **De Long-Shleifer-Summers-Waldmann (1990)** [31]. La creencia errática de los noise traders crea un riesgo que un arbitrajista con horizonte finito no puede eliminar: el precio se aleja del fundamental, y los noise traders pueden ganar más en promedio porque cargan el riesgo que crean.
- **Shleifer-Vishny (1997)** [30]. El arbitraje real usa capital ajeno y es riesgoso. Tras pérdidas vienen los retiros, y el arbitraje se vuelve ineficaz justo cuando el precio está más lejos del valor.
  - Predicción: las anomalías viven donde el arbitraje es caro (alta volatilidad idiosincrática, baja liquidez, venta en corto difícil).
- **Sentimiento.** Baker-Wurgler (2006, 2007) [32][33]:
  - con sentimiento bajo al inicio del periodo, luego rinden relativamente más las acciones pequeñas, jóvenes, volátiles, no rentables, sin dividendo, de crecimiento extremo y en problemas;
  - con sentimiento alto, luego rinden relativamente menos.
  - Stambaugh-Yu-Yuan (2012): cada anomalía es más fuerte tras sentimiento alto; la **pierna corta** es la que gana; y el sentimiento **no guarda relación con las piernas largas** [34].
- **Sobre y subreacción.**
  - De Bondt-Thaler (1985): los perdedores de largo plazo superan a los ganadores, con retornos de enero excepcionales hasta cinco años después [35]. La magnitud que se suele citar, ~25% en 36 meses: (no verificado).
  - Barberis-Shleifer-Vishny (1998) lo modelan con dos sesgos [36]: **conservadurismo**, que da subreacción a noticias y explica momentum y deriva; y **representatividad**, que da sobrerreacción a rachas y explica la reversión.
- **Atención.**
  - Los individuos son compradores netos de acciones que llaman la atención: noticias, volumen anormal, retornos extremos de un día (Barber-Odean 2008) [28]. Al comprar eligen entre miles; al vender, solo entre lo que ya tienen.
  - Un alza en búsquedas de Google (SVI) predice precios más altos las 2 semanas siguientes y **reversión dentro del año** (Da-Engelberg-Gao 2011) [29].

### 2.4 Microestructura
- **Kyle (1985)** [44], versión de un periodo:
  - datos: v ~ N(p₀, Σ₀); ruido u ~ N(0, σ_u²);
  - el informado ordena x = β(v − p₀) y el formador fija p = p₀ + λ(x + u);
  - equilibrio: **β = σ_u/√Σ₀** y **λ = √Σ₀ / (2σ_u)**. El precio incorpora la mitad de la información privada, porque la varianza posterior es Σ₀/2.
  - Intuición: la profundidad (1/λ) crece con el ruido. Donde operan muchos minoristas desinformados, el informado se esconde y el impacto por unidad baja.
- **Glosten-Milgrom (1985)** [45]:
  - ask = E[V | compra] y bid = E[V | venta];
  - con dos valores equiprobables V_L, V_H y una fracción μ de informados, el spread es **μ(V_H − V_L)**;
  - el spread existe por **selección adversa**, aunque el formador no tenga costos.
- **Roll (1984)** [46]: s = 2√(−Cov(Δp_t, Δp_{t−1})). El rebote bid-ask genera autocorrelación negativa.
- **Corwin-Schultz (2012)** [47] estiman el spread con máximos y mínimos diarios. Sirven cuando no hay cotizaciones, por ejemplo en el SIC.
- **Ley de raíz cuadrada** [49][50][51]: Δ(Q) = Y·σ_d·√(Q/V_d). σ_d es la volatilidad diaria, V_d el volumen diario, Y es "de orden unidad" y el exponente empírico está entre 0.4 y 0.7 [49].
  - Sato-Kanazawa (2025, *PRL*) usan todas las cuentas de la Bolsa de Tokio durante 8 años. Encuentran δ = 1/2 dentro del error estadístico, por acción y por trader, y rechazan los modelos GGPS y FGLW [51].
  - Maitrier-Loeper-Kanazawa-Bouchaud (2026) muestran que el impacto es "mecánico" (una doble raíz cuadrada) y no informativo [52].
  - La ley aplica a **metaórdenes** (órdenes hijas de una misma decisión) y es cóncava: el costo por peso crece con √Q.
- **Almgren-Chriss (2001)** [48] minimizan E[costo] + κ·Var[costo]. Operar rápido paga impacto y operar lento paga riesgo de precio; la trayectoria óptima es un seno hiperbólico decreciente.
- **PFOF.** El mayorista paga al bróker por el flujo minorista porque ese flujo está poco informado: es la selección adversa inversa de Glosten-Milgrom. El debate es si el bróker traslada la mejora de precio al cliente. En opciones el PFOF es mucho mayor y la internalización es imperfectamente competitiva (Ernst-Spatt 2022) [57]. Los costos reales de un gran institucional resultaron un orden de magnitud menores que los estimados en estudios previos (Frazzini-Israel-Moskowitz) [53].

### 2.5 Ciencia del pronóstico
- **Brier (1950)** [70]: BS = (1/N) Σ (f_t − o_t)², en escala 0–1 en binario. Es la escala de `herramientas/metricas.brier`. Brier sumaba sobre categorías, lo que da escala 0–2, y así se ve en la literatura del GJP.
  - Referencias: siempre 50% da 0.25. La "climatología", que es pronosticar siempre la tasa base ō, da ō(1−ō).
- **Descomposición de Murphy (1973)** [71]: BS = REL − RES + UNC.
  - REL (confiabilidad) es el error de calibración: debe ser chico.
  - RES (resolución) es la capacidad de separar casos: debe ser grande.
  - UNC = ō(1−ō) es la dificultad intrínseca.
  - **Skill score**: BSS = 1 − BS/BS_ref.
- **Regla de puntaje propia.** Brier y log score dan su mejor puntaje esperado solo si se reporta la creencia verdadera. Redondear a 0% o 100% nunca conviene salvo certeza.
- **Vista externa.** Kahneman-Lovallo (1993) [81]: los decisores tratan cada problema como único y anclan en el plan (inside view), lo que da pronósticos audaces y elecciones tímidas.
  - Remedio: partir de la **clase de referencia**, luego ajustar. Flyvbjerg (2006) lo formalizó como reference class forecasting [82]. Mauboussin-Callahan-Majd (2016) llevan la tasa base a ventas, márgenes y ROIC [83]. Por ejemplo, entre las 1,000 mayores empresas del mundo en 1950-2015, el crecimiento real de ventas a 3 años tuvo media de 8.1% anual y mediana de 5.4%, y 23% de las empresas encogió en términos reales. El rango de los consensos es más estrecho que el histórico.
- **Agregación.**
  - Las pruebas en tournaments de IARPA mostraron que el promedio simple de pronosticadores queda "comprimido" hacia 0.5. Transformarlo hacia los extremos (**extremizing**) mejora la precisión (Baron et al. 2014; Satopää et al. 2014) [68][69].
  - Las encuestas de pronóstico en equipo, agregadas con decaimiento temporal, pesos por historial y recalibración, superaron al mercado de predicción (Atanasov et al. 2017) [67].

---

## 3. Literatura canónica (tabla: Autores | Año | Título | Revista/Editorial | Hallazgo clave cuantificado | Enlace/DOI | Grado)

| Autores | Año | Título | Revista/Editorial | Hallazgo clave cuantificado | Enlace/DOI | Grado |
|---|---|---|---|---|---|---|
| Kahneman, Tversky | 1979 | Prospect Theory: An Analysis of Decision under Risk | *Econometrica* 47(2) | Valor sobre ganancias y pérdidas; aversión a pérdidas y efecto certeza | 10.2307/1914185 | A (concepto) |
| Tversky, Kahneman | 1992 | Advances in Prospect Theory | *JRU* 5(4):297-323 | Medianas λ = 2.25, α = β = 0.88; n = 25, sin incentivo [3] | 10.1007/BF00122574 | B |
| Brown, Imai, Vieider, Camerer | 2024 | Meta-analysis of Empirical Estimates of Loss Aversion | *JEL* 62(2):485-516 | 607 estimaciones: λ = 1.955 [1.820, 2.102]; mediana cruda 1.69 | 10.1257/jel.20221698 | A |
| Benartzi, Thaler | 1995 | Myopic Loss Aversion and the Equity Premium Puzzle | *QJE* 110(1):73-92 | Aversión a pérdidas + evaluación frecuente explican la prima | 10.2307/2118511 | B |
| Thaler, Johnson | 1990 | Gambling with the House Money and Trying to Break Even | *Mgmt Sci* 36(6):643-660 | Más riesgo después de ganar; atracción por salir tablas después de perder | 10.1287/mnsc.36.6.643 | B |
| Shefrin, Statman | 1985 | The Disposition to Sell Winners Too Early and Ride Losers Too Long | *JF* 40(3):777-790 | Acuñan el efecto disposición; los impuestos no lo explican | 10.1111/j.1540-6261.1985.tb05002.x | A |
| Odean | 1998 | Are Investors Reluctant to Realize Their Losses? | *JF* 53(5):1775-1798 | 10,000 cuentas: PGR 0.148 vs PLR 0.098. Al año, la ganadora vendida rinde +2.4% sobre el mercado y la perdedora retenida −1.0%: **3.4 pp** | 10.1111/0022-1082.00072 | A |
| Barber, Odean | 2000 | Trading Is Hazardous to Your Wealth | *JF* 55(2):773-806 | 66,465 hogares (1991-96): el que más opera gana 11.4%/año contra 17.9% del mercado; el hogar promedio 16.4% con rotación de 75% | 10.1111/0022-1082.00226 | A |
| Barber, Odean | 2001 | Boys Will Be Boys | *QJE* 116(1):261-292 | Los hombres operan 45% más; operar les resta 2.65 pp/año contra 1.72 pp a las mujeres | 10.1162/003355301556400 | A |
| Barber, Odean | 2002 | Online Investors: Do the Slow Die First? | *RFS* 15(2):455-488 | Antes de pasar a operar en línea le ganaban >2%/año al mercado; después quedan >3%/año abajo | 10.1093/rfs/15.2.455 | A |
| Grinblatt, Keloharju | 2009 | Sensation Seeking, Overconfidence, and Trading Activity | *JF* 64(2):549-578 | Finlandia: los sobreconfiados y los que buscan sensaciones operan más | 10.1111/j.1540-6261.2009.01443.x | A |
| Barber, Lee, Liu, Odean | 2009 | Just How Much Do Individual Investors Lose by Trading? | *RFS* 22(2):609-632 | Taiwán: los individuos pierden **3.8 pp/año** (2.2% del PIB). Las pérdidas vienen de órdenes **agresivas**; las pasivas ganan a horizonte corto | 10.1093/rfs/hhn046 | A |
| Barber, Lee, Liu, Odean | 2014 | The Cross-Section of Speculator Skill | *JFM* 18:1-24 | **<1%** de los day traders gana de forma predecible neto de comisiones. Top 500: 37.9 pb/día neto; los peores: −28.9 pb/día | 10.1016/j.finmar.2013.05.006 | A |
| Barber, Lee, Liu, Odean, Zhang | 2020 | Learning, Fast or Slow | *RAPS* 10(1):61-93 | 97% de los day traders probablemente perderá; 74% del volumen viene de traders con historial de pérdidas | 10.1093/rapstu/raz006 | A |
| Chague, De-Losso, Giovannetti | 2019 | Day Trading for a Living? | SSRN WP | Brasil, futuros de renta variable (quienes empezaron en 2013-2015): **97%** de los que persistieron >300 días perdió; 1.1% ganó más que el salario mínimo y 0.5% más que un cajero bancario | 10.2139/ssrn.3423101 | A |
| Heimer, Simsek | 2019 | Should Retail Investors' Leverage Be Limited? | *JFE* 132(3) | Tope de apalancamiento en FX de EUA (2010): volumen −23%; rendimiento de los muy apalancados +18 pp/mes (pérdidas −40%) | 10.1016/j.jfineco.2018.10.017 | B |
| Barber, Huang, Odean, Schwarz | 2022 | Attention-Induced Trading and Returns: Robinhood | *JF* 77(6):3141-3190 | Las acciones más compradas del día rinden **−4.7%** anormal a 20 días | 10.1111/jofi.13183 | A |
| Welch | 2022 | The Wisdom of the Robinhood Crowd | *JF* 77(3):1489-1527 | Contrapunto: el portafolio consenso (2018-2020) tuvo buen timing y alfa; compraron en marzo de 2020 | 10.1111/jofi.13128 | B |
| Kelley, Tetlock | 2013 | How Wise Are Crowds? | *JF* 68(3):1229-1265 | La compra neta minorista predice retornos mensuales sin reversión; solo las órdenes agresivas anticipan noticias | 10.1111/jofi.12028 | B |
| Linnainmaa | 2010 | Do Limit Orders Alter Inferences…? | *JF* 65(4):1473-1506 | Gran parte del "mal desempeño" y del efecto disposición es mecánica: selección adversa de órdenes limitadas | 10.1111/j.1540-6261.2010.01576.x | A |
| Barber, Odean | 2008 | All That Glitters | *RFS* 21(2):785-818 | Los individuos son compradores netos de acciones con noticias, volumen anormal o retornos extremos | 10.1093/rfs/hhm079 | A |
| Da, Engelberg, Gao | 2011 | In Search of Attention | *JF* 66(5):1461-1499 | Un alza de SVI da precio más alto 2 semanas y reversión en el año | 10.1111/j.1540-6261.2011.01679.x | B |
| De Long, Shleifer, Summers, Waldmann | 1990 | Noise Trader Risk in Financial Markets | *JPE* 98(4):703-738 | El riesgo de noise traders limita el arbitraje | 10.1086/261703 | A (teoría) |
| Shleifer, Vishny | 1997 | The Limits of Arbitrage | *JF* 52(1):35-55 | El arbitraje con capital ajeno falla en los extremos | 10.1111/j.1540-6261.1997.tb03807.x | A (teoría) |
| Baker, Wurgler | 2006 | Investor Sentiment and the Cross-Section | *JF* 61(4):1645-1680 | El sentimiento predice el rendimiento relativo de acciones difíciles de valuar y de arbitrar | 10.1111/j.1540-6261.2006.00885.x | B |
| Stambaugh, Yu, Yuan | 2012 | The Short of It | *JFE* 104(2):288-302 | Anomalías más fuertes tras sentimiento alto, vía la pierna corta; sin relación con la pierna larga | 10.1016/j.jfineco.2011.12.001 | B |
| De Bondt, Thaler | 1985 | Does the Stock Market Overreact? | *JF* 40(3):793-805 | Los perdedores superan a los ganadores; enero excepcional hasta 5 años después | 10.1111/j.1540-6261.1985.tb05004.x | C (hoy) |
| Barberis, Shleifer, Vishny | 1998 | A Model of Investor Sentiment | *JFE* 49(3):307-343 | Conservadurismo + representatividad dan subreacción y sobrerreacción | 10.1016/S0304-405X(98)00027-0 | B (teoría) |
| McLean, Pontiff | 2016 | Does Academic Research Destroy Stock Return Predictability? | *JF* 71(1):5-32 | 97 predictores: −26% fuera de muestra y **−58% tras publicación** | 10.1111/jofi.12365 | A |
| Kyle | 1985 | Continuous Auctions and Insider Trading | *Econometrica* 53(6):1315 | λ = √Σ₀/(2σ_u) | 10.2307/1913210 | A (teoría) |
| Glosten, Milgrom | 1985 | Bid, Ask and Transaction Prices… | *JFE* 14(1):71-100 | El spread sale de la selección adversa | 10.1016/0304-405X(85)90044-3 | A (teoría) |
| Roll | 1984 | A Simple Implicit Measure of the Effective Bid-Ask Spread | *JF* 39(4):1127-1139 | s = 2√(−cov) | 10.1111/j.1540-6261.1984.tb03897.x | B |
| Almgren, Chriss | 2001 | Optimal Execution of Portfolio Transactions | *J. of Risk* 3(2):5-39 | Frontera eficiente impacto-riesgo | 10.21314/JOR.2001.041 | A (teoría) |
| Tóth, Lempérière, Deremble, de Lataillade, Kockelkoren, Bouchaud | 2011 | Anomalous Price Impact and the Critical Nature of Liquidity | *PRX* 1:021006 | Δ = Yσ√(Q/V), Y ~ 1, exponente 0.4–0.7 | 10.1103/PhysRevX.1.021006 | A |
| Brier | 1950 | Verification of Forecasts Expressed in Terms of Probability | *Monthly Weather Review* 78(1):1-3 | Puntaje cuadrático | 10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 | A |
| Murphy | 1973 | A New Vector Partition of the Probability Score | *J. Appl. Meteor.* 12(4):595-600 | BS = REL − RES + UNC | 10.1175/1520-0450(1973)012<0595:ANVPOT>2.0.CO;2 | A |
| Tetlock | 2005 (2.ª ed. 2017) | Expert Political Judgment | Princeton UP | Expertos apenas mejores que el azar; los "zorros" le ganan a los "erizos"; más de 20 años de datos | 10.1515/9781400888818 | A |
| Mellers et al. | 2014 | Psychological Strategies for Winning a Geopolitical Forecasting Tournament | *Psych. Science* 25(5):1106-1115 | Entrenamiento, equipos y tracking mejoran calibración y resolución | 10.1177/0956797614524255 | A |
| Mellers et al. | 2015 | Identifying and Cultivating Superforecasters | *Perspect. Psych. Sci.* 10(3):267-281 | Los superpronosticadores mantuvieron su precisión 2 años seguidos, contra la regresión a la media | 10.1177/1745691615577794 | A |
| Chang, Chen, Mellers, Tetlock | 2016 | Developing Expert Political Judgment | *JDM* 11(5):509-526 | Un entrenamiento de <1 hora mejoró el Brier **6–11%** contra el control, en 4 años | 10.1017/S1930297500004599 | A |
| Atanasov et al. | 2017 | Distilling the Wisdom of Crowds | *Mgmt Sci* 63(3):691-706 | 2,400+ participantes y 261 eventos: el mercado le gana al promedio simple; las encuestas de equipo bien agregadas le ganan al mercado | 10.1287/mnsc.2015.2374 | A |
| Baron, Mellers, Tetlock, Stone, Ungar | 2014 | Two Reasons to Make Aggregated Probability Forecasts More Extreme | *Decision Analysis* 11(2):133-145 | Extremizar el agregado corrige la compresión | 10.1287/deca.2014.0293 | A |
| Tetlock, Gardner | 2015 | Superforecasting | Crown | El GJP superó al grupo de control por **más de 60%** (p. 18, cita secundaria [63]) | ver [63] | B |
| Kahneman, Lovallo | 1993 | Timid Choices and Bold Forecasts | *Mgmt Sci* 39(1):17-31 | La vista interna da pronósticos audaces; remedio: tasa base | 10.1287/mnsc.39.1.17 | A |
| Klein | 2007 | Performing a Project Premortem | *HBR* 2007; reimpr. *IEEE EMR* 36(2), 2008 | Imaginar que ya fracasó y explicar por qué | 10.1109/EMR.2008.4534313 | C |
| Haynes et al. | 2009 | A Surgical Safety Checklist… | *NEJM* 360:491-499 | 8 hospitales, antes y después: muertes de 1.5% a 0.8%, complicaciones de 11.0% a 7.0% | 10.1056/NEJMsa0810119 | B (no aleatorizado) |
| Coates, Herbert | 2008 | Endogenous Steroids and Financial Risk Taking on a London Trading Floor | *PNAS* 105(16):6167-6172 | La testosterona matutina predice el P&L del día; el cortisol sube con la varianza del P&L y la volatilidad | 10.1073/pnas.0704025105 | C (muestra chica) |
| Kandasamy et al. | 2014 | Cortisol Shifts Financial Risk Preferences | *PNAS* 111(9):3608-3613 | 8 días de cortisol elevado dan **más aversión al riesgo** | 10.1073/pnas.1317908111 | B |
| Venkatraman et al. | 2011 | Sleep Deprivation Biases the Neural Mechanisms Underlying Economic Preferences | *J. Neurosci.* 31(10):3712-3718 | Una noche sin dormir cambia la estrategia de defender pérdidas a buscar ganancias | 10.1523/JNEUROSCI.4407-10.2011 | B (laboratorio) |
| Hirshleifer, Levi, Lourie, Teoh | 2019 | Decision Fatigue and Heuristic Analyst Forecasts | *JFE* 133(1):83-98 | Cada pronóstico adicional del día reduce la precisión y aumenta el rebaño y el redondeo | 10.1016/j.jfineco.2019.01.005 | B |
| Kamstra, Kramer, Levi | 2000 | Losing Sleep at the Market | *AER* 90(4):1005-1011 | Fines de semana de cambio de horario: retorno 200–500% más negativo; **disputado** por Pinegar (2002) | 10.1257/aer.90.4.1005 | C |

---

## 4. Lo más reciente 2023-2026 (papers, working papers, datos nuevos; con fecha)

**Sesgos del minorista**
1. **Brown, Imai, Vieider y Camerer (JEL, jun-2024).** λ ≈ 1.96, no 2.25. Pocas características del diseño explican la dispersión [3]. Uso: calibrar modelos de preferencia con ~2 y no anclar en 2.25.
2. **Gödker, Odean y Smeets ("Disposed to Be Overconfident", WP 2023, próxima publicación según el sitio de Odean).** Vender con ganancia genera sobreconfianza y, en el experimento, más riesgo [42].
3. **Chague, Giovannetti, Guimarães y Maciel (WP nov-2023).** Los días ganadores inflados por el efecto disposición: 54% observado contra 48% contrafactual [19].
4. **Chague y Giovannetti (*Brazilian Review of Finance*, 2025).** El day trading de la pandemia en Brasil llegó a ~100,000 participantes activos al día. **Pérdidas brutas de R$9.9 mil millones** entre el inicio de la pandemia y dic-2023, en promedio **R$10,200 por persona** [18].
5. **Chague, Giovannetti y Paiva (*JBF* 185, 2026).** Sesgo de familiaridad en el day trading: vivir en una ciudad chica con una tienda de la empresa "más que duplica" la probabilidad de hacer day trading con esa acción [20].
6. **Barber, Chu, Liu, Odean y Shi ("Mired in Losses", WP 2026).** Un portafolio con pérdidas latentes deprime las compras nuevas por dos canales, liquidez y menor atención a recomendaciones. El segundo explica hasta 1/3 de la caída [43].
7. **Barber, Lin y Odean (*JFQA* 59(6), 2024).** La paradoja: el desbalance de órdenes minoristas predice retornos, pero el minorista pierde. La razón es que sus compras se concentran en acciones de atención. El largo-corto por desbalance extremo rinde **−14.8% anual** en acciones con mucho minorista y **+6.6%** en las demás [25].
8. **Chapkovski, Khapko y Zoican (*Management Science* 72(1), 2026).** RCT sobre gamificación [41]:
   - los elementos hedónicos suben el volumen **5.17%**;
   - la diferencia entre plataformas es 70% autoselección y 30% gamificación;
   - las notificaciones de tendencia refuerzan los errores de quien tiene creencias equivocadas.
9. **Cookson, Engelberg y Mullins (*RFS* 36(2), 2023).** En StockTwits (400,000 usuarios), los alcistas tienen 5 veces más probabilidad de seguir a otro alcista. En 50 días ven 62 mensajes alcistas más y 24 bajistas menos que los bajistas. Las creencias formadas en cámaras de eco se asocian con peores retornos ex post y más volumen [39].
10. **Kakhbod, Kazempour, Livdan y Schuerhoff ("Finfluencers", WP 2023).** La mayoría de los finfluencers no tiene habilidad o tiene habilidad negativa ("antiskilled"), y esos son más atractivos y tienen más seguidores [40].

**Microestructura y ejecución**
11. **Barber, Huang, Jorion, Odean y Schwarz (*JF* 79(4), 2024).** Colocaron 85,000 operaciones minoristas reales:
    - el algoritmo BJZZ solo identifica 35% como minoristas y firma mal 28%;
    - con el punto medio de las cotizaciones el error baja a 5% [55].
    - Las medidas de "flujo minorista" de TAQ tienen mucho ruido.
12. **Schwarz, Barber, Huang, Jorion y Odean (*JF* 80(5), oct-2025).** 85,000 órdenes a mercado simultáneas en 6 cuentas de 5 brókeres. El costo de ida y vuelta sin comisiones va de **0.07% a 0.46%** según la cuenta, y **el PFOF no explica la variación** [54].
13. **SEC, retiro formal (Federal Register, 17-jun-2025).** Se retiraron la *Order Competition Rule* (propuesta en ene-2023) y la *Regulation Best Execution* [60]. El PFOF en EUA sigue sin la reforma propuesta en 2022-2023.
14. **Bryzgalova, Pavlova y Sikorskaya (*JF* 78(6), 2023).** En opciones de EUA, el minorista supera el 60% del volumen y ~90% del PFOF viene de tres mayoristas. Prefiere semanales baratas con **spread promedio de 12.6%** y pierde en promedio [56].
15. **Beckmeyer, Branger y Gayda (WP 2023).** Más del 75% de las operaciones minoristas en opciones del S&P 500 son **0DTE**, con pérdidas sustanciales pese a la mejora de precio [58]. Además, el trading minorista de opciones sube la volatilidad del subyacente por la cobertura de los formadores (Lipson-Tomio-Zhang, WP 2023) [59].
16. **Bradley, Goncalo, Jame y Roseman (WP 2026).** Tras la derogación de la regla *Pattern Day Trader*:
    - las operaciones minoristas en opciones suben 14–24%, concentradas en 0DTE fuera del dinero;
    - los spreads se estrechan [61].
17. **Sato y Kanazawa (*PRL* 135, 2025) y Maitrier et al. (*Quantitative Finance* 26(4), 2026).** La raíz cuadrada es universal y de origen mecánico [51][52].

**Ciencia del pronóstico e IA**
18. **Schoenegger et al. (*Science Advances* 10(45), 2024).** Un ensamble de 12 LLM (31 preguntas) es estadísticamente indistinguible de la multitud humana (925 pronosticadores). Mostrarle a GPT-4 y Claude 2 la mediana humana los mejora **17–28%**. También muestran sesgo de aquiescencia [75]. En sentido inverso, un asistente LLM mejora la precisión de pronosticadores humanos (N = 991, experimento pre-registrado) [76].
19. **Halawi, Zhang, Chen y Steinhardt (NeurIPS 2024).** Un sistema con recuperación de información "se acerca" al agregado de pronosticadores competitivos y a veces lo supera [77].
20. **ForecastBench (Karger et al., arXiv v5 feb-2025)** [78] y **"Brier Index" del FRI (4-mar-2026)** [79]:
    - superpronosticadores **70.6%** contra los mejores LLM **67.9%**, una brecha de **2.7 pp**;
    - los LLM mejoraron 2.4 pp entre oct-2024 y oct-2025;
    - la paridad se proyecta para **may-2027** (IC95% abr-2026 a may-2028), por extrapolación lineal con pocos modelos.
21. **Gómez-Cram, Guo, Jensen y Kung (WP 2026).** En un mercado de predicción grande, ~**3% de las cuentas** genera la mayor parte del descubrimiento de precio. La mayoría no aporta precisión, la financia [80].
22. **Tetlock, Karvetski, Satopää y Chen (*Futures & Foresight Science*, 2024)** [72]. Con juicios hechos en 1988 y 1997, a 5, 10 y 25 años los especialistas le ganan a los generalistas solo en algunos temas (proliferación nuclear), no en otros (fronteras). La precisión cae más rápido donde la pericia no ayudaba a corto plazo. Relacionado: el torneo XPT sobre riesgo existencial (Karger et al., *IJF* 41(2), 2025) [73]; sus cifras no se leyeron aquí.
23. **Agentes LLM que operan en vivo.**
    - Barton et al. (arXiv 2609.05663, 4-sep-2026), 6 meses y dos flotas en producción [100]:
      - el apalancamiento no depende de la volatilidad: mediana 5.0x en todos los sextiles;
      - 43.2% de las posiciones llegó a +300 pb a favor en 24 h, y **49.3% de ellas cerró con pérdida**;
      - no hay ventaja direccional: 41% de operaciones ganadoras contra 50% del benchmark minorista;
      - los modelos de frontera no se distinguen en calidad de decisión.
    - Qu-Chen (CLQT, arXiv 2606.29771, rev. 12-sep-2026) [101]:
      - el retorno de un periodo está dominado por la trayectoria del mercado;
      - hay una brecha sistemática entre lo que el agente dice y lo que asigna: +0.30 en backtest y +0.23 en vivo;
      - neto de costos, no le ganan limpiamente al índice.
    - Ninguno de los dos está revisado por pares (grado C).
24. **Mauboussin y Callahan (Counterpoint Global, 2025-2026)** [84]: *Drawdowns and Recoveries* (2025), *Probabilities and Payoffs* (2025), *Bayes and Base Rates* 1 y 2.0 (2026), *Who Is On the Other Side?* (2026) y *The Wisdom of Crowds in Markets* (2026). Títulos confirmados; contenido no leído porque Morgan Stanley bloqueó la descarga (no verificado).

---

## 5. Evidencia real: qué funciona, qué no, magnitudes netas, decaimiento post-publicación

### 5.1 Lo que NO funciona (grado A, neto de costos)

| Conducta | Magnitud | Muestra | Estado post-publicación |
|---|---|---|---|
| Sobretrading | El quintil que más opera: 11.4% contra 17.9% del mercado (−6.5 pp/año). El hogar promedio: −1.5 pp [10] | EUA 1991-96 | Se repite en Taiwán: −3.8 pp/año agregado [14] |
| Day trading | <1% gana de forma predecible neto [15]; 97% perderá [16]; en Brasil, 97% de los persistentes pierde [17] y R$10,200 por persona en la pandemia [18] | Taiwán y Brasil (mercados completos) | Se repite en 2020-2023 [18] |
| Compras por atención | −4.7% a 20 días (Robinhood) [22]; −14.8% anual en el largo-corto de acciones con mucho minorista [25] | EUA (Robinhood y TAQ) | Consistente con 2008 [28]: no decae |
| Efecto disposición | 3.4 pp en 12 meses entre la ganadora vendida y la perdedora retenida [8] | EUA 1987-93 | Persiste; hoy se estudia su canal a la sobreconfianza [42][19] |
| Apalancamiento minorista | Con tope, los muy apalancados mejoran +18 pp/mes [21] | FX EUA 2010 | Experimento natural |
| Opciones de corto plazo y 0DTE del minorista | Spread de 12.6% [56]; pérdidas sustanciales [58] | EUA (datos recientes) | Crece con la desregulación [61] |

**Inferencia.** La forma más barata y segura de "ganar" contra el participante promedio, humano o IA, es **no cometer estos cinco errores**. Por Barber-Odean (2000), eso vale entre 1.5 y 6.5 pp al año, con un Sharpe implícito que ninguna anomalía publicada ofrece neta (cap. 06: 4 pb/mes para la anomalía promedio [38]).

### 5.2 Lo que funciona (con matices)

- **Ser el lado pasivo.** Las órdenes pasivas de individuos en Taiwán **ganan a horizonte corto** y pierden poco a horizontes largos [14]. Linnainmaa advierte que las limitadas sufren selección adversa: se llenan justo cuando el precio va en contra [27]. Resultado neto: limitada al punto medio o cerca de él, con vigencia corta y nunca abierta a través de un evento.
- **La sabiduría minorista agregada no siempre es tonta.** La compra neta minorista predice retornos mensuales [26], y el consenso de Robinhood tuvo alfa en 2018-2020 [23]. Barber-Lin-Odean lo reconcilian: funciona en acciones **sin** frenesí de atención y falla en las que sí lo tienen [25]. Las caídas de Robinhood mejoran la liquidez en acciones de alto interés minorista y las de brókeres tradicionales la empeoran [24]. Grado B.
- **Sentimiento como filtro de riesgo, no como señal de compra.** En un portafolio solo en largo el sentimiento no predice nada, porque el efecto está en la pierna corta [34]. Sirve para **evitar** "loterías" cuando el sentimiento está alto [32]. Grado B.
- **Reversión de largo plazo (De Bondt-Thaler).** Débil hoy: su rendimiento se concentra en enero [35] y aplica el decaimiento general post-publicación de 58% [37]. Grado C para operar.
- **Atención.** Momentum de 2 semanas y reversión en el año [29]. Para swings de 5% o más en semanas, perseguir un pico de atención tiene esperanza negativa a un año. Grado B.
- **Entrenamiento de pronóstico.** Menos de 1 hora mejora el Brier 6–11% [66]. Equipos + tracking + agregación extremizada fueron la estrategia ganadora de IARPA [64][65][68]. Grado A en geopolítica. En mercados el rival es el precio, que ya agrega pronósticos: grado C mientras no le ganemos a las probabilidades implícitas.
- **Checklists.** Muertes quirúrgicas de 1.5% a 0.8% en un diseño antes-después [89]. En inversión la evidencia es anecdótica (grado D), pero cuestan casi nada.
- **Pre-mortem.** La "retrospectiva prospectiva" cambia la naturaleza de las explicaciones [86]. La cifra popular de "+30% de razones identificadas" no se verificó. Grado C.

### 5.3 Microestructura: qué costo importa en una cuenta de 20,000 MXN

- **Comisión GBM:** 0.25% + IVA por lado, es decir **0.58% ida y vuelta**, más spread. Total de 0.7% a 1.2% por vuelta según liquidez (arena/01).
- **Impacto de raíz cuadrada (Inferencia, con Y = 1):**
  - σ_d = 2% y Q/V = 0.01% dan **0.02%**;
  - Q/V = 1% da 0.2%;
  - Q/V = 5% da 0.45%.
  - Con órdenes de 5,000–10,000 MXN, el impacto es despreciable en ETFs y megacaps. Solo importa en emisoras del SIC o de la BMV con poco volumen **local**, donde la orden puede ser una fracción grande del libro.
- **Dispersión de ejecución entre brókeres:** hasta 0.39 pp de ida y vuelta para la misma orden [54]. **Inferencia:** en el SIC, la ejecución (precio local contra origen × tipo de cambio) puede pesar más que la comisión; se mide.
- **Conclusión operable:** domina comisión + spread, y lo controla **cuántas veces se opera**, no cómo se rebana la orden. Almgren-Chriss y la raíz cuadrada importan solo si el capital crece más de 100 veces o en emisoras con volumen diario local menor a 1 millón de MXN (umbral propio, Inferencia).

### 5.4 Pronóstico: cuánta muestra hace falta (Inferencia, cálculo propio)

- Pronosticador calibrado en 0.70 contra una moneda: su Brier esperado es 0.21, con desviación estándar por pronóstico de 0.183.
- Para una t ≈ 2 contra 0.25 necesita **~84** pronósticos. Para una ventaja de 0.05 bastan **~54**.
- El mínimo de 50 de `pronosticos.min_pronosticos_para_evaluar` alcanza para detectar ventajas de ~0.05 o más, no menores.
- **Resultado de 6 meses como prueba de habilidad:** con Sharpe verdadero S y horizonte T, P(pérdida) ≈ Φ(−S√T).
  - S = 0.5 y T = 0.5 años: **36%**. S = 1.0 y T = 0.5: 24%.
  - Una temporada de la arena **no distingue** habilidad de suerte. CLQT llega a lo mismo: el retorno de un periodo lo domina la trayectoria del mercado [101].
  - Hay que evaluar el proceso además del resultado.

### 5.5 Fisiología y sueño: lo que se sabe y lo que no
- La testosterona matutina predijo el P&L del día en traders de Londres [91][92]. El tamaño de muestra que se suele citar, 17 traders y 8 días: (no verificado). Todos eran hombres.
- El cortisol sube con la volatilidad [91]. Si se eleva de forma crónica (8 días), aumenta la aversión al riesgo [93]. **Inferencia:** después de un drawdown, el humano tiende a subinvertir justo cuando las tasas base de recuperación favorecen mantener la exposición.
- La interocepción predijo P&L y permanencia en el piso de remates [94]. Es correlación; la muestra es chica.
- Una noche sin dormir cambia la conducta hacia buscar ganancias [95]. La fatiga de decisiones degrada pronósticos de analistas a lo largo del día [97]. La anomalía del cambio de horario a nivel mercado está **disputada** [96].
- Grado global de la sección: C para el mercado y B para el individuo en laboratorio. Se usa para **higiene de decisiones**, no como señal de trading.

---

## 6. Traducción operable (reglas concretas, parámetros, checklists: cómo lo usa el sistema para ganar dinero; coherente con config/parametros.json)

**Marco.** En fase 0 (`prioridad_actual`) nada de esto mueve dinero real. Se aplica al portafolio de papel y a la bitácora de pronósticos. Los límites vienen de `config/parametros.json` y este módulo **no crea límites de riesgo nuevos**. Los umbrales de conducta que propongo dicen **"criterio"**: son reglas de proceso, no de riesgo.

### 6.1 Ficha de decisión obligatoria (antes de cualquier orden de papel o real)
Va en `bitacora/decisiones/AAAA-MM-DD-<ticker>.md`. Se llena **fuera del horario de mercado**; en horario solo se ejecuta lo ya escrito.

1. **Tesis en una frase + cadena causal** (ver `ideas-adoptadas` #9).
2. **Clase de referencia y tasa base con fuente.** Ejemplos: "de las acciones del SIC con caída de 30% o más, qué % recuperó en 6 meses" o "qué % de swings de 5% llega al objetivo antes que al stop". Si no hay tasa base, la probabilidad propia se encoge hacia 50%.
3. **Probabilidad propia de la tesis y fecha de resolución.** Se registra también en `bitacora/pronosticos.csv` con `herramientas/pronosticos.py agregar`.
4. **Movimiento esperado ≥ 5%** (regla de `nota_rotacion` del perfil arena) y costo estimado de la vuelta (0.58% + spread medido). Si el costo pasa de 25% del movimiento esperado, no se opera (criterio de arena/01).
5. **Tamaño por fórmula, nunca a ojo:**
   - riesgo al stop ≤ `riesgo_por_operacion` (arena 0.03; estándar 0.01; fase de prueba 0.005);
   - Kelly fraccional ≤ `kelly_fraccion_max` (arena 0.5; estándar 0.25);
   - límites de concentración del perfil.
   - El tamaño se calcula antes de mirar el P&L del mes.
6. **Pre-mortem de 5 minutos.** "Es la fecha de resolución y la operación perdió el stop completo: ¿por qué?". Se escriben 3 razones. Si una parece tener ≥ 30% de probabilidad (criterio), se reduce el tamaño a la mitad o no se opera.
7. **El caso bajista más fuerte**, contra las cámaras de eco [39]: se escribe el mejor argumento del otro lado con una fuente que no venga de quien comparte la tesis.
8. **Señal de invalidación** observable: un precio, un dato o una fecha.
9. **Salida pre-programada.** Stop y objetivo, o regla de tiempo, se definen antes de entrar [100]. Se colocan como órdenes en GBM cuando el menú lo permita (Trading MX sí tiene stop; Trading USA no) o como alerta con instrucción escrita.
10. **Estado del decisor:** hora, número de decisiones previas en la sesión y horas de sueño del dueño si él va a ejecutar algo discrecional.

### 6.2 Protocolo anti-sesgo por sesgo

| Sesgo | Evidencia | Regla del sistema | Parámetro / métrica de control |
|---|---|---|---|
| Sobretrading | [10][14] | Tope de operaciones y de rotación; cada operación nueva compite contra "no hacer nada" | `operaciones_max_mes` = 8; `rotacion_max_mensual_x_capital` = 1.5; `orden_minima_mxn` = 5,000. Métrica: costos acumulados / capital. Alarma (criterio) si en la temporada pasa de 3.5% (presupuesto de arena/01) |
| Day trading | [15][16][17][18] | **Prohibido abrir y cerrar el mismo día por iniciativa.** Solo se cierra intradía si salta un stop o un cortacircuitos | Tasa base: 97% pierde |
| Disposición | [8][9][42] | Revisión mensual con la pregunta "¿la compraría hoy a este precio?", **sin mostrar el costo de compra** (ocultarlo reduce el efecto 25% [9]). Las salidas son las de la ficha, no las del estado de ánimo | PGR y PLR propios desde `bitacora/operaciones.csv`. Alarma (criterio) si PGR/PLR > 1.2 con ≥ 20 decisiones de venta (el inversionista promedio de Odean: ~1.5) |
| Juzgar por % de aciertos | [19][42] | Se evalúa por expectativa, profit factor y Brier. El hit rate se reporta, pero no decide nada | `metricas.expectancy`, `profit_factor`, `hit_rate` |
| House money / break-even | [6] | Prohibido subir el tamaño "para recuperar" o "porque vamos ganando". El `modo_torneo` es una regla **pre-registrada** de la temporada, no una emoción: se activa solo por su umbral (±5 pp contra el mejor rival reportado) y **cede ante los cortacircuitos**, que tienen prioridad | `modo_torneo.ventaja_para_bajar_varianza_pp` = 5; `desventaja_para_subir_exposicion_pp` = 5; cortacircuitos arena −12/−20/−28/−35% |
| Rachas | [16][91][93] | Reducción mecánica | `rachas`: 3 pérdidas → ×0.5; 2 ganancias → se restaura; 5 → pausa y revisión del edge |
| Compra por atención | [22][25][28][29] | Criterio: no comprar el mismo día ni el siguiente de un pico de atención (volumen > 3× su promedio de 20 días, tendencia en X o en listas de "más compradas") salvo que la señal esté pre-registrada. Se esperan ≥ 5 días hábiles y se vuelve a evaluar | Registro del motivo en la ficha |
| Sentimiento | [32][34] | Con sentimiento alto (medido en el tablero), el satélite excluye "loterías": no rentables, sin dividendo, volatilidad extrema, IPO de menos de 2 años (criterio). Tampoco se usa como señal alcista | Etiqueta de régimen en `bitacora/briefs` |
| Apalancamiento | [21] | Solo dentro del perfil y del filtro | `filtro_apalancados`: subyacente > SMA200 y VIX < 25; `etf_apalancado_max` = 0.5; cortacircuitos −20% → sin ETFs apalancados |
| Opciones "lotería" | [56][58] | Nada de 0DTE ni semanales OTM | `opciones_prima_en_riesgo_max` = 0.02 (estándar) |
| X y finfluencers | [39][40] | X solo genera hipótesis. Se aplica el filtro de `ideas-adoptadas` #6: publicación original fechada, historial con pérdidas, reglas previas, capital, flujos y costos. El número de seguidores no es evidencia | Fuente anotada en la ficha |
| Fatiga | [97] | Criterio: máximo 5 decisiones nuevas por sesión, las importantes primero. Lo que sobra pasa a la sesión siguiente | Contador en la ficha |
| Sueño y estrés del dueño | [93][95] | El dueño ejecuta **solo órdenes ya escritas** por el sistema, con precio límite y vigencia. Si durmió < 6 h (criterio) o está en un evento de estrés, no ejecuta nada discrecional ese día | Casilla en la ficha |
| Resultado ≠ proceso | [63][87] | Cada post-mortem califica la **decisión** con la ficha, **antes** de ver el P&L, en una matriz 2×2 (decisión buena o mala × resultado bueno o malo). Se usa la skill `post-mortem` | Brecha "dice vs hace" [101]: se compara la ficha con la orden real cada mes |

### 6.3 Protocolo de pronósticos (fase 0: criterio de salida)
1. Todo pronóstico es binario o por intervalo, con **fecha y criterio de resolución** escritos antes, en `bitacora/pronosticos.csv`. La versión original nunca se sobrescribe.
2. **Primero la vista externa:** tasa base → ajuste por la vista interna en pasos chicos. Las probabilidades se recortan a [0.02, 0.98] (criterio), porque un 0 o un 100 equivocados destruyen el log score.
3. **Escala 0–1** (la de `metricas.brier`). Objetivo `brier_objetivo` = 0.20 con ≥ `min_pronosticos_para_evaluar` = 50. Además de ese objetivo absoluto, se exige **skill contra la climatología > 0**: `pronosticos.py` ya calcula `brier_skill_vs_climatologia`. Un Brier de 0.18 en eventos de base 10% es peor que la climatología (0.09).
4. **Calibración mensual** con `metricas.tabla_calibracion`, en cubetas con n ≥ 10 (criterio).
   - Si la frecuencia observada en la cubeta del 70% queda por debajo de 60%, las probabilidades de esa zona se encogen hacia 50%.
   - Solo se **extremiza** un agregado (nunca un pronóstico individual) si hay ≥ 50 resueltos y muestran subconfianza [68].
5. **Multitud de silicio** [75]:
   - cada pregunta importante se contesta con ≥ 3 corridas o agentes independientes, sin ver la respuesta de los otros (higiene de decisión: juicios independientes antes de agregar [90]);
   - se agrega con la media de log-odds (o la mediana);
   - si existe probabilidad humana o de mercado, se muestra **después** del pronóstico propio y se registran las dos.
6. **Contra el precio.** Cuando haya probabilidad implícita (opciones, futuros de tasas, mercados de predicción), el pronóstico propio se compara con ella. Si en 50 pronósticos no le gana, **no hay edge operable**, aunque el Brier sea bueno.
7. **Descomposición de Murphy** trimestral: si REL es alto, hay que calibrar; si RES es bajo, falta información o método.

### 6.4 Ejecución en GBM (microestructura para minorista)
- **Siempre limitadas.** Precio en el punto medio o hasta 1/3 del spread hacia la contraparte (criterio), con vigencia del día, nunca abiertas a través de un reporte o de un anuncio de la Fed. Base: las órdenes agresivas explican las pérdidas minoristas [14] y las limitadas viejas sufren selección adversa [27].
- **SIC:** antes de operar se compara el precio local contra precio de origen × USD/MXN spot del mismo minuto y se registra la diferencia (regla de arena/01).
  - Se opera cuando el mercado de origen está abierto, que es cuando el formador local tiene referencia: BMV 7:30–14:00 hasta el 30-oct-2026 y 8:30–15:00 desde el 3-nov-2026, hora CDMX.
  - Se evitan los primeros y últimos minutos (criterio; que el spread se ensancha en la apertura en el SIC: no verificado).
- **Tamaño contra liquidez local:** orden ≤ 1% del volumen diario local promedio (criterio), lo que deja el impacto en ≤ 0.2% con σ_d = 2%. Si no se cumple, se elige la versión más líquida del mismo riesgo (ETF en lugar de acción o listado de origen vía Trading USA).
- **Costo efectivo medido por operación:** 2·|P_ejec − M|/M, con M el punto medio al momento de la orden. Se registra en `bitacora/operaciones.csv`. Si tres operaciones seguidas en el mismo instrumento cuestan más de 0.3% de spread efectivo (criterio), se cambia de vehículo.
- **PFOF:** no se conoce el esquema de enrutamiento de DriveWealth ni de GBM (no verificado). No se supone nada: se mide.

### 6.5 Rutinas
- **Diaria (fase 0, 20 min, antes de la apertura):**
  1. estado de límites y cortacircuitos;
  2. pronósticos vencidos (`pronosticos.py vencidos`) y resolución con evidencia;
  3. 1–3 pronósticos nuevos con tasa base;
  4. portafolio de papel: solo órdenes de fichas ya escritas.
  - No se abren decisiones nuevas en horario de mercado.
- **Semanal:** Brier y calibración acumulados; fichas de la semana contra lo ejecutado; "picos de atención" rechazados y qué pasó después (control del filtro).
- **Mensual:**
  - métricas conductuales propias: PGR/PLR, rotación, costos / capital, % de operaciones fuera de ficha (objetivo 0) y brecha dice-hace;
  - revisión "¿la compraría hoy?" sin costo de compra visible.
- **Por temporada o trimestre:** post-mortem completo (skill `post-mortem`); descomposición de Murphy; comparación contra los rivales **por proceso** (drawdown, rotación estimada) y no solo por rendimiento, porque 6 meses no distinguen habilidad (§5.4). Para comparar sistemas, lo mejor es un torneo con preguntas comunes y puntaje propio [74]; es la lógica del intercambio de bancos en `conocimiento/examenes/PROTOCOLO.md`.

### 6.6 Cómo ganarle a otras IAs con esto (Inferencia)
La evidencia 2025-2026 sobre agentes LLM en vivo muestra cuatro fallas repetidas [100][101]:
- tamaño ciego a la volatilidad;
- no capturan lo que el mercado les ofrece (salidas malas);
- brecha entre el análisis que escriben y lo que asignan;
- sin ventaja direccional neta de costos.

En Alpha Arena los líderes tempranos apalancados se derrumbaron (arena/03). La ventaja reproducible del sistema es **conductual y de costos**:
1. tamaño por fórmula y por volatilidad;
2. salidas pre-programadas;
3. ficha escrita que se ejecuta sin cambios;
4. pocas operaciones;
5. calibración medida.

Contra un rival que sobretradea (R3 de arena/03: 5–9% de comisiones por temporada), la disciplina sola gana del 67% al 88% de las veces en ese modelo. **La ventaja se pierde el día que el sistema imita al rival que va ganando.**

---

## 7. Trampas y errores comunes

1. **Citar λ = 2.25 como constante universal.** Es la mediana de 25 estudiantes sin incentivos. La meta-análisis da ~1.96 y hay escépticos serios [3][4].
2. **Leer todo efecto disposición como irracional.** Parte es mecánica por las limitadas [27], y en México hay impuestos: 10% sobre la ganancia en la anual. Lo que se corrige es vender por **ganancia** en lugar de por **expectativa**.
3. **"El minorista siempre se equivoca: hagamos lo contrario".** Falso: su compra neta predice retornos [26][23] y solo falla en acciones de atención [25]. Además, el lado contrario exige vender en corto, restringido y caro en GBM (arena/01).
4. **Usar el sentimiento como señal de compra en un portafolio solo en largo.** El efecto está en la pierna corta [34].
5. **Presumir el hit rate.** El efecto disposición lo infla [19]. Hay que exigir expectativa neta.
6. **Brier sin referencia.** En eventos raros, un Brier "bajo" puede ser peor que la climatología. Siempre se reporta el BSS.
7. **Calibrar con 15 pronósticos.** Menos de 50 no distingue ventajas de 0.04–0.05 (§5.4).
8. **Extremizar pronósticos individuales.** Extremizar solo corrige la compresión de un **agregado** [68].
9. **Aplicar la raíz cuadrada o Almgren-Chriss a 10,000 MXN.** El costo relevante es comisión + spread + frecuencia (§5.3).
10. **Suponer que el PFOF implica mala ejecución, o que "sin comisión" implica ejecución barata.** La dispersión de 0.07–0.46% no la explica el PFOF [54]. Hay que medir.
11. **Convertir la fisiología en señal.** Muestras chicas y solo hombres [91]; la anomalía del cambio de horario está disputada [96]. Sirve para higiene de decisiones, no para operar.
12. **Tomar benchmarks de pronóstico de LLM como edge de trading.** Pronosticar bien geopolítica no es ganarle al precio; los agentes en vivo no muestran ventaja neta [100][101].
13. **Convertir el modo torneo en "get-evenitis".** Subir exposición cuando se va perdiendo es racional en un premio tipo "el ganador se lo lleva" solo si está pre-registrado, acotado por los límites del perfil y subordinado a los cortacircuitos [6][98][99].
14. **Confundir resultado con decisión.** Con Sharpe 0.5, 36% de las temporadas de 6 meses termina en pérdida (§5.4).
15. **Creerle a X por el número de seguidores.** Los finfluencers sin habilidad o con habilidad negativa tienen **más** seguidores [40].

---

## 8. Examen de titulación (12-15 preguntas con respuesta breve y correcta)

1. **¿Qué λ usarías hoy y por qué no 2.25?** ~1.96 (IC95% 1.82–2.10), de la meta-análisis de 607 estimaciones [3]. 2.25 es una mediana de n = 25 sin incentivos.
2. **Define PGR y PLR y da los valores de Odean (1998).** PGR = RG/(RG + PG) y PLR = RL/(RL + PL). En el año completo, 0.148 contra 0.098; en diciembre se invierte, 0.108 contra 0.128, por impuestos.
3. **¿Cuánto costaba al año la ganadora vendida frente a la perdedora retenida?** Unos 3.4 pp: la ganadora rindió +2.4% sobre el mercado y la perdedora −1.0% [8].
4. **Cifras clave de Barber-Odean (2000).** 66,465 hogares; el quintil que más opera gana 11.4% contra 17.9% del mercado; el promedio 16.4% con rotación de 75%.
5. **Tasa base del day trading en Taiwán y en Brasil.** Taiwán: <1% gana de forma predecible neto y 97% probablemente perderá. Brasil: 97% de los que persisten >300 días pierde, y solo 1.1% gana más que el salario mínimo.
6. **¿Por qué la pierna larga de una estrategia de sentimiento no sirve para un portafolio solo en largo?** Stambaugh-Yu-Yuan: tras sentimiento alto la anomalía gana por la pierna corta (sobrevaloración más restricciones a la venta en corto), y el sentimiento no se relaciona con las piernas largas.
7. **Deriva el λ de Kyle e interprétalo.** λ = √Σ₀/(2σ_u). Más ruido da más profundidad; el informado revela la mitad de su información.
8. **¿De dónde sale el spread en Glosten-Milgrom y cuánto vale en el caso simple?** De la selección adversa: ask = E[V|compra], bid = E[V|venta]. Spread = μ(V_H − V_L).
9. **Escribe la ley de raíz cuadrada y di si importa para 10,000 MXN en un ETF líquido.** Δ = Yσ√(Q/V) con Y ~ 1. Con Q/V = 0.01% y σ = 2%, el impacto es ~0.02%: no importa; domina la comisión de 0.58% ida y vuelta.
10. **¿Qué encontró Schwarz et al. (2025) sobre ejecución minorista?** Costo de ida y vuelta de 0.07–0.46% según la cuenta, sin comisiones, por precios distintos de los mayoristas. El PFOF no explica la variación.
11. **¿Qué pasó en 2025 con la Order Competition Rule?** La SEC la retiró formalmente junto con Regulation Best Execution (Federal Register, 17-jun-2025).
12. **Descomposición de Murphy y por qué reportar el BSS.** BS = REL − RES + UNC. El BSS compara contra la climatología ō(1−ō): en eventos raros un Brier bajo puede no tener skill.
13. **¿Cuántos pronósticos necesita alguien calibrado al 70% para distinguirse de una moneda?** ~84 para t ≈ 2 (ventaja de 0.04). El mínimo de 50 solo detecta ventajas de ~0.05 o más.
14. **Tres palancas de IARPA/GJP y el efecto medido del entrenamiento.** Entrenamiento, equipos y tracking de los mejores, más agregación extremizada. Menos de 1 hora de entrenamiento mejoró el Brier 6–11%.
15. **¿Por qué una temporada de 6 meses no prueba habilidad, y qué se evalúa entonces?** Con Sharpe 0.5, P(pérdida) ≈ Φ(−0.5√0.5) ≈ 36%. Se evalúa el proceso: fichas contra órdenes, calibración, costos, apego a límites y brecha dice-hace.

---

## 9. Fuentes (lista numerada con URL)

1. Kahneman & Tversky (1979). https://doi.org/10.2307/1914185
2. Tversky & Kahneman (1992). https://doi.org/10.1007/BF00122574
3. Brown, Imai, Vieider & Camerer (2024), JEL. https://doi.org/10.1257/jel.20221698 — texto completo: https://biblio.ugent.be/publication/8756103/file/8756105.pdf
4. Gal & Rucker (2018). https://doi.org/10.1002/jcpy.1047
5. Benartzi & Thaler (1995). https://doi.org/10.2307/2118511
6. Thaler & Johnson (1990). https://doi.org/10.1287/mnsc.36.6.643 ; Jelschen & Schmidt (2023) https://doi.org/10.1007/s11166-023-09411-5
7. Shefrin & Statman (1985). https://doi.org/10.1111/j.1540-6261.1985.tb05002.x
8. Odean (1998). https://doi.org/10.1111/0022-1082.00072 ; PDF: https://faculty.haas.berkeley.edu/odean/papers%20current%20versions/areinvestorsreluctant.pdf
9. Frydman & Rangel (2014). https://doi.org/10.1016/j.jebo.2014.01.017
10. Barber & Odean (2000). https://doi.org/10.1111/0022-1082.00226
11. Barber & Odean (2001). https://doi.org/10.1162/003355301556400 ; PDF: https://faculty.haas.berkeley.edu/odean/papers%20current%20versions/boyswillbeboys.pdf
12. Barber & Odean (2002). https://doi.org/10.1093/rfs/15.2.455
13. Grinblatt & Keloharju (2009). https://doi.org/10.1111/j.1540-6261.2009.01443.x
14. Barber, Lee, Liu & Odean (2009). https://doi.org/10.1093/rfs/hhn046 ; resumen: https://doi.org/10.2139/ssrn.529062
15. Barber, Lee, Liu & Odean (2014). https://doi.org/10.1016/j.finmar.2013.05.006 ; PDF: https://faculty.haas.berkeley.edu/odean/papers/Day%20Traders/The%20Cross-Section%20of%20Speculator%20Skill.pdf
16. Barber, Lee, Liu, Odean & Zhang (2020). https://doi.org/10.1093/rapstu/raz006
17. Chague, De-Losso & Giovannetti (2019). https://doi.org/10.2139/ssrn.3423101
18. Chague & Giovannetti (2025). https://doi.org/10.12660/rbfin.v23n1.2025.94291
19. Chague, Giovannetti, Guimarães & Maciel (2023). https://doi.org/10.2139/ssrn.4636623
20. Chague, Giovannetti & Paiva (2026). https://doi.org/10.1016/j.jbankfin.2026.107651
21. Heimer & Simsek (2019). https://doi.org/10.1016/j.jfineco.2018.10.017 ; resumen: https://doi.org/10.2139/ssrn.2150980
22. Barber, Huang, Odean & Schwarz (2022). https://doi.org/10.1111/jofi.13183
23. Welch (2022). https://doi.org/10.1111/jofi.13128
24. Eaton, Green, Roseman & Wu (2022). https://doi.org/10.1016/j.jfineco.2022.08.002
25. Barber, Lin & Odean (2024). https://doi.org/10.1017/S0022109023000601
26. Kelley & Tetlock (2013). https://doi.org/10.1111/jofi.12028
27. Linnainmaa (2010). https://doi.org/10.1111/j.1540-6261.2010.01576.x
28. Barber & Odean (2008). https://doi.org/10.1093/rfs/hhm079
29. Da, Engelberg & Gao (2011). https://doi.org/10.1111/j.1540-6261.2011.01679.x
30. Shleifer & Vishny (1997). https://doi.org/10.1111/j.1540-6261.1997.tb03807.x
31. De Long, Shleifer, Summers & Waldmann (1990). https://doi.org/10.1086/261703
32. Baker & Wurgler (2006). https://doi.org/10.1111/j.1540-6261.2006.00885.x
33. Baker & Wurgler (2007). https://doi.org/10.1257/jep.21.2.129
34. Stambaugh, Yu & Yuan (2012). https://doi.org/10.1016/j.jfineco.2011.12.001
35. De Bondt & Thaler (1985). https://doi.org/10.1111/j.1540-6261.1985.tb05004.x
36. Barberis, Shleifer & Vishny (1998). https://doi.org/10.1016/S0304-405X(98)00027-0
37. McLean & Pontiff (2016). https://doi.org/10.1111/jofi.12365
38. Chen & Velikov (2023). https://doi.org/10.1017/S0022109022000874
39. Cookson, Engelberg & Mullins (2023). https://doi.org/10.1093/rfs/hhac058
40. Kakhbod, Kazempour, Livdan & Schuerhoff (2023). https://doi.org/10.2139/ssrn.4428232
41. Chapkovski, Khapko & Zoican (2026). https://doi.org/10.1287/mnsc.2022.02650
42. Gödker, Odean & Smeets (2023). https://doi.org/10.2139/ssrn.4404706
43. Barber, Chu, Liu, Odean & Shi (2026). https://doi.org/10.2139/ssrn.6141687
44. Kyle (1985). https://doi.org/10.2307/1913210
45. Glosten & Milgrom (1985). https://doi.org/10.1016/0304-405X(85)90044-3
46. Roll (1984). https://doi.org/10.1111/j.1540-6261.1984.tb03897.x
47. Corwin & Schultz (2012). https://doi.org/10.1111/j.1540-6261.2012.01729.x
48. Almgren & Chriss (2001). https://doi.org/10.21314/JOR.2001.041
49. Tóth et al. (2011). https://doi.org/10.1103/PhysRevX.1.021006 ; https://arxiv.org/abs/1105.1694
50. Bouchaud, Bonart, Donier & Gould (2018), *Trades, Quotes and Prices*, Cambridge UP. https://doi.org/10.1017/9781316659335
51. Sato & Kanazawa (2025), PRL. https://doi.org/10.1103/65jz-81kv ; https://arxiv.org/abs/2411.13965
52. Maitrier, Loeper, Kanazawa & Bouchaud (2026). https://doi.org/10.1080/14697688.2026.2615106 ; https://arxiv.org/abs/2502.16246
53. Frazzini, Israel & Moskowitz (2018), "Trading Costs" (1.7 billones de USD en ejecuciones reales, 21 mercados, 19 años; costos un orden de magnitud menores que en estudios previos). https://doi.org/10.2139/ssrn.3229719
54. Schwarz, Barber, Huang, Jorion & Odean (2025). https://doi.org/10.1111/jofi.13467
55. Barber, Huang, Jorion, Odean & Schwarz (2024). https://doi.org/10.1111/jofi.13334
56. Bryzgalova, Pavlova & Sikorskaya (2023). https://doi.org/10.1111/jofi.13285
57. Ernst & Spatt (2022), NBER w29883 https://doi.org/10.3386/w29883 ; "Payment for Order Flow and Option Internalization" https://doi.org/10.2139/ssrn.4056512
58. Beckmeyer, Branger & Gayda (2023). https://doi.org/10.2139/ssrn.4404704
59. Lipson, Tomio & Zhang (2023). https://doi.org/10.2139/ssrn.4383463
60. SEC, *Withdrawal of Proposed Regulatory Actions*, Federal Register 2025-11110 (17-jun-2025). https://www.govinfo.gov/content/pkg/FR-2025-06-17/html/2025-11110.htm
61. Bradley, Goncalo, Jame & Roseman (2026). https://doi.org/10.2139/ssrn.7448381
62. Tetlock (2005; 2.ª ed. 2017). https://press.princeton.edu/books/paperback/9780691175973/expert-political-judgment
63. Tetlock & Gardner (2015), *Superforecasting*, Crown (ficha: https://openlibrary.org/search?q=superforecasting+tetlock). Cifras del libro vía AI Impacts: https://aiimpacts.org/evidence-on-good-forecasting-practices-from-the-good-judgment-project/
64. Mellers et al. (2014). https://doi.org/10.1177/0956797614524255
65. Mellers et al. (2015). https://doi.org/10.1177/1745691615577794
66. Chang, Chen, Mellers & Tetlock (2016). https://doi.org/10.1017/S1930297500004599
67. Atanasov et al. (2017). https://doi.org/10.1287/mnsc.2015.2374
68. Baron, Mellers, Tetlock, Stone & Ungar (2014). https://doi.org/10.1287/deca.2014.0293
69. Satopää et al. (2014). https://doi.org/10.1016/j.ijforecast.2013.09.009
70. Brier (1950). https://doi.org/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2
71. Murphy (1973). https://doi.org/10.1175/1520-0450(1973)012%3C0595:ANVPOT%3E2.0.CO;2
72. Tetlock, Karvetski, Satopää & Chen (2024). https://doi.org/10.1002/ffo2.157
73. Karger et al. (2025). https://doi.org/10.1016/j.ijforecast.2024.11.008
74. Tetlock, Mellers & Scoblic (2017), *Science*. https://doi.org/10.1126/science.aal3147
75. Schoenegger et al. (2024). https://doi.org/10.1126/sciadv.adp1528
76. Schoenegger, Park, Karger, Trott & Tetlock (2025). https://doi.org/10.1145/3707649
77. Halawi, Zhang, Chen & Steinhardt (2024). https://arxiv.org/abs/2402.18563
78. Karger et al., ForecastBench. https://arxiv.org/abs/2409.19839
79. Forecasting Research Institute, "Introducing the Brier Index" (4-mar-2026). https://forecastingresearch.substack.com/p/introducing-the-brier-index
80. Gómez-Cram, Guo, Jensen & Kung (2026). https://doi.org/10.2139/ssrn.6617059
81. Kahneman & Lovallo (1993). https://doi.org/10.1287/mnsc.39.1.17
82. Flyvbjerg (2006). https://doi.org/10.1177/875697280603700302
83. Mauboussin, Callahan & Majd (2016), *The Base Rate Book*, Credit Suisse (26-sep-2016). https://12mv2.files.wordpress.com/2024/04/16-09-26-the-base-rate-book__integrating-the-past-to-better-anticipate-the-future.pdf
84. Archivo de Mauboussin (Counterpoint Global 2025-2026). https://www.michaelmauboussin.com/writing
85. Klein (2007/2008), "Performing a Project Premortem". https://doi.org/10.1109/EMR.2008.4534313
86. Mitchell, Russo & Pennington (1989). https://doi.org/10.1002/bdm.3960020103
87. Duke (2018), *Thinking in Bets*, Portfolio. https://openlibrary.org/search?q=thinking+in+bets+duke
88. Gawande (2009), *The Checklist Manifesto*, Metropolitan Books (Open Library registra 2010). https://openlibrary.org/search?q=checklist+manifesto
89. Haynes et al. (2009), NEJM. https://doi.org/10.1056/NEJMsa0810119
90. Kahneman, Sibony & Sunstein (2021), *Noise*, Little, Brown. https://openlibrary.org/search?q=noise+kahneman+sibony
91. Coates & Herbert (2008). https://doi.org/10.1073/pnas.0704025105
92. Coates (2012), *The Hour Between Dog and Wolf*, Penguin Press. https://openlibrary.org/search?q=hour+between+dog+and+wolf
93. Kandasamy et al. (2014). https://doi.org/10.1073/pnas.1317908111
94. Kandasamy et al. (2016). https://doi.org/10.1038/srep32986
95. Venkatraman et al. (2011). https://doi.org/10.1523/JNEUROSCI.4407-10.2011
96. Kamstra, Kramer & Levi (2000) https://doi.org/10.1257/aer.90.4.1005 ; Pinegar (2002) https://doi.org/10.1257/00028280260344786 ; réplica (2002) https://doi.org/10.1257/00028280260344795
97. Hirshleifer, Levi, Lourie & Teoh (2019). https://doi.org/10.1016/j.jfineco.2019.01.005
98. Brown, Harlow & Starks (1996). https://doi.org/10.1111/j.1540-6261.1996.tb05203.x
99. Chevalier & Ellison (1997). https://doi.org/10.1086/516389
100. Barton et al. (2026), arXiv 2609.05663. https://arxiv.org/abs/2609.05663
101. Qu & Chen (2026), CLQT, arXiv 2606.29771. https://arxiv.org/abs/2606.29771
102. Interno: `arena/investigacion/01-gbm-operativa-y-costos.md` y `arena/investigacion/03-teoria-de-torneos-y-estrategia-competitiva.md` (costos GBM, horarios, Alpha Arena, modelo P(ganar)).
103. Gervais & Odean, "Learning to Be Overconfident" (WP 1997). https://doi.org/10.2139/ssrn.36313
