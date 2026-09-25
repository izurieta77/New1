# Módulo 19 — Biblioteca esencial: 40 libros y sus lecciones operables

> Nivel: licenciatura → doctorado + práctica · Actualizado: 2026-09-25 · Grado de evidencia global: **B (bimodal)**. Lo que el canon enseña como **matemática o aritmética** (Kelly, costos, "el inversionista promedio obtiene el mercado menos costos", p = E(mx), sesgo de supervivencia) o como **historia replicada con datos** (DMS, Reinhart-Rogoff, Kindleberger, LTCM) es **A**. Lo que enseña como **método de practicante** (margen de seguridad, ciclos, reflexividad) es **B/C**. Lo que enseña como **anécdota de ganadores** (Market Wizards, Lefèvre, "invierte en lo que conoces") es **D** como evidencia, aunque sirve como fuente de hipótesis.

Capítulos relacionados que aquí no se repiten: [01 Fundamentos](01-licenciatura-fundamentos.md) (Kelly fraccional, DMS 2026, Bessembinder, SPIVA), [02 Portafolio](02-maestria-portafolio-y-asset-pricing.md) (factores y su decaimiento), [03 Valuación](03-maestria-valuacion-y-analisis-fundamental.md) (Graham y Dodd, fórmula mágica, decaimiento de Berkshire), [05 Derivados](05-maestria-derivados-y-volatilidad.md) (tail hedging y Universa), cap. 07 (backtesting), cap. 08 (sesgos y pronóstico), [15 Situaciones especiales](15-eventos-corporativos-y-situaciones-especiales.md), [16 Macro](16-macro-global-divisas-y-el-peso.md) (Dalio, Reinhart-Rogoff), [17 Crisis](17-crisis-burbujas-libro-de-patrones.md) (Kindleberger-Minsky), [18 Grandes inversionistas](18-grandes-inversionistas-decodificados.md) (historiales de los autores; aquí solo se citan cuando cambian la lectura del libro). Parámetros: `config/parametros.json`.

**Convenciones.** *Hecho* = dato con fuente numerada [n]. **"Inferencia:"** = interpretación propia. **"Regla:"** = recomendación, solo en la sección 6. **"(no verificado)"** = no confirmado en esta sesión. Un libro no se califica por su fama: su grado es el **mínimo** entre la calidad de su evidencia y su aplicabilidad a una cuenta de MXN 20,000 ejecutada a mano en GBM.

**Nota de método.** La cuota de WebSearch de la sesión estaba agotada (200/200). Título, autor, año y edición se verificaron con Open Library (API de búsqueda y de ediciones), Wikipedia (API y WebFetch) y páginas de editoriales (Wiley, Springer, Princeton UP, Cambridge, Stern/NYU). Las cifras de desempeño de los autores se tomaron de esas fuentes o de los capítulos 01, 03 y 18, que las verificaron antes.

---

## 1. Objetivos de dominio

Al terminar este módulo el sistema debe poder:

1. Citar de cada uno de los 40 libros el autor, el año, la última edición verificada, la tesis central, de 3 a 5 lecciones operables y la crítica principal.
2. Ubicar cada libro en su estante (A decisión · B negocio y valuación · C tamaño y supervivencia · D mercados y rendimientos esperados · E crisis y ciclos · F cuantitativo · G practicantes) y en su nivel.
3. Separar dentro de un mismo libro la parte matemática (A), la empírica replicada, el historial auditado y la anécdota (D).
4. Resolver con evidencia los desacuerdos del canon: eficiencia contra ineficiencia, concentración contra diversificación, Kelly completo contra fraccional, timing de ciclo contra permanencia.
5. Traducir cada lección a una regla atada a un parámetro de `config/parametros.json`.
6. Seguir la ruta de lectura por niveles y actualizar la biblioteca con lo publicado en 2023-2026.

## 2. Núcleo teórico / marco

### 2.1 Jerarquía de evidencia de un libro de inversión

| Nivel | Tipo de afirmación | Ejemplos | Grado máximo |
|---|---|---|---|
| 1 | Identidad o teorema | Kelly (Thorp, Poundstone), aritmética de costos (Bogle), p = E(mx) (Cochrane) | A |
| 2 | Datos públicos replicados por terceros | DMS, Reinhart-Rogoff, Siegel/McQuarrie, SPIVA | A/B |
| 3 | Historial público del autor | Berkshire (precio diario), Magellan | B (sesgo de selección) |
| 4 | Historial privado reportado | Baupost, Gotham, Medallion, Quantum | C |
| 5 | Anécdota, entrevista, novela | Lefèvre, Market Wizards, Housel, Lynch | D como prueba |

**Inferencia:** una biblioteca de inversión es una muestra de sobrevivientes. Casi todo autor-practicante escribe después de ganar. Las excepciones valiosas son los libros sobre fracasos: *When Genius Failed*, la vida de Livermore que cuenta Lefèvre y *The Missing Billionaires*. Por eso el canon sobrerrepresenta la concentración y la convicción, y subrepresenta la ruina que esas mismas conductas producen en los que no escribieron libro (cap. 18, §2.4).

### 2.2 Las ocho convergencias del canon (lo que casi todos dicen y sobrevive a la evidencia)

1. **Sobrevivir primero.** Lo dicen Buffett, Marks, Taleb, Thorp, Housel, Lowenstein y Haghani. La razón es matemática: el crecimiento geométrico castiga la varianza y la ruina es absorbente (cap. 01).
2. **Los costos deciden.** Lo dicen Bogle, Malkiel, Swensen y Carver. El inversionista promedio obtiene el mercado menos costos (A).
3. **Precio contra valor, o qué descuenta el precio.** Graham, Klarman, Rappaport-Mauboussin y Damodaran. Es una herramienta A, pero como fuente de alfa es B/C (cap. 03).
4. **El tamaño importa tanto como la dirección.** Thorp, Poundstone, Haghani-White, Chan y Carver.
5. **Proceso sobre resultado.** Duke, Mauboussin, Tetlock y Taleb: con muestras chicas, el resultado mide suerte.
6. **Los ciclos existen y el timing es difícil.** Marks, Kindleberger, Shiller, Reinhart-Rogoff, Dalio y Soros.
7. **Los backtests mienten por defecto.** López de Prado, Carver y Chan; en la academia, McLean-Pontiff (−26% fuera de muestra, −58% después de publicarse; cap. 03).
8. **Apalancamiento más iliquidez es la combinación letal.** LTCM, Kindleberger y Pedersen (espirales de liquidez).

### 2.3 Los cinco desacuerdos reales y cómo se resuelven

| Desacuerdo | Bando 1 | Bando 2 | Resolución con evidencia |
|---|---|---|---|
| ¿Se le gana al mercado? | Graham, Buffett, Lynch, Klarman | Malkiel, Bogle | Pedersen y Lo: "eficientemente ineficiente". La mayoría pierde neto de costos (SPIVA, A). Hay primas que pagan liquidez y riesgo, y decaen al publicarse |
| ¿Concentrar o diversificar? | Munger, Fisher, Buffett | Bogle, Swensen | Bessembinder: la mediana de una acción pierde contra T-bills (cap. 01). Concentrar solo con ventaja demostrada y con tope de posición |
| Kelly completo o fraccional | Kelly y los primeros escritos de Thorp | Samuelson | El error de estimación manda: fraccional (A) |
| ¿Hacer timing del ciclo? | Marks, Shiller, Dalio, Soros | Bogle, Malkiel | La valuación predice rendimientos a 10 años con ruido y falla como gatillo de corto plazo: ajustar dentro de bandas, no pasar de 0 a 100 |
| Cobertura de cola permanente | Taleb | Ilmanen, AQR | En la evidencia sistemática, el put continuo cuesta más de lo que protege y la tendencia protege más barato (cap. 05) |

## 3. Literatura y fuentes canónicas

### 3.1 Tabla maestra de los 40

Estantes: **A** decisión e incertidumbre · **B** negocio y valuación · **C** tamaño y supervivencia · **D** mercados y rendimientos esperados · **E** crisis y ciclos · **F** cuantitativo · **G** practicantes. Nivel: Lic = licenciatura, Maes = maestría, Doc = doctorado, Práct = práctica.

| # | Libro · autor · año (última edición verificada) | Estante · nivel | Evidencia cuantificada clave | Grado | Fuente |
|---|---|---|---|---|---|
| 1 | *Thinking, Fast and Slow* · Kahneman · 2011 (+ *Noise*, con Sibony y Sunstein, 2021) | A · Lic/Maes | Capítulo 4 (priming): R-index de 14. Kahneman admitió "I placed too much faith in underpowered studies" | B | [15] |
| 2 | *Superforecasting* · Tetlock y Gardner · Crown, 2015 | A · Lic/Maes | El GJP ganó las dos temporadas del torneo IARPA-ACE con una precisión 35-72% mayor que la de los otros equipos. Sus mejores pronosticadores fueron "reportedly 30% better" que analistas de inteligencia con información clasificada | A (geopolítica) / C (precios) | [16] |
| 3 | *Thinking in Bets* · Duke · Portfolio, 2018 (+ *Quit*, 2022) | A · Lic | Marco de decisión sin métrica propia | B (marco) | [17] |
| 4 | *Fooled by Randomness* (Texere, 2001; 2.ª ed. 2004) y *The Black Swan* (Random House, 2007; ampliado 2010) · Taleb | A · Maes | Las colas gruesas son un hecho. Universa reportó +3,612% sobre la prima en mar-2020, contra el costo continuo de la cobertura (cap. 05) | A (hecho) / D (cobertura permanente) | [14] |
| 5 | *More Than You Know* (Columbia UP, 2006) y *The Success Equation* (HBR Press, 2012) · Mauboussin | A · Maes | Marco de suerte contra habilidad, sin backtest | B | [10] |
| 6 | *Poor Charlie's Almanack* · Munger (comp. P. Kaufman) · 2005; ed. ampliada 2008; Stripe Press, 2023 | A · Lic/Práct | Wheeler Munger: 19.8% anual contra 5.0% del Dow (1962-1975) | B/C | [43] |
| 7 | *The Psychology of Money* · Housel · Harriman House, 2020 (+ *Same as Ever*, 2023; *The Art of Spending Money*, 2025) | A · Lic | Anecdótico | C | [41] |
| 8 | *Against the Gods* · P. L. Bernstein · Wiley, 1996 | A · Lic | Historia de las ideas de riesgo | A (historia) | [26] |
| 9 | *The Intelligent Investor* (1949; 4.ª ed. revisada 1973; 3.ª ed. revisada con comentarios de J. Zweig, Harper Business, 2024) y *Security Analysis*, con Dodd (1934; 7.ª ed., McGraw-Hill, 27-jun-2023) · Graham | B · Lic (II) / Maes (SA) | En los años 70, Graham dudaba de que el análisis extenso justificara su costo. HML cayó −57.8% (dic-2006 a sep-2020; cap. 03) | B | [1][2] |
| 10 | *Common Stocks and Uncommon Profits* · P. Fisher · 1958 | B · Lic/Maes | Motorola, comprada en 1955 y conservada hasta su muerte: es un caso, no una muestra | C | [3] |
| 11 | *The Essays of Warren Buffett* · L. Cunningham · 1997; ediciones revisadas de 2001 a 2019; ed. Wiley 2021 | B · Lic/Maes | Berkshire: 19.7% contra 10.5% (1965-2025), pero 13.0% contra 14.1% (2011-2025) | B | [4][46] |
| 12 | *One Up on Wall Street* · Lynch con J. Rothchild · 1989 | B · Lic | Magellan: 29.2% contra 15.8% del S&P (1977-1990); los activos pasaron de US$18 millones a US$14 mil millones | C/D | [5] |
| 13 | *Margin of Safety* · Klarman · HarperBusiness, 1991 (sin reedición en catálogo) | B · Maes | Baupost, "20% compuesto desde 1982" (Wikipedia, sin cita); −7% a −13% en 2008 | B/C | [7] |
| 14 | *The Little Book That (Still) Beats the Market* (Wiley, 2005 y 2010) y *You Can Be a Stock Market Genius* (1997) · Greenblatt | B · Lic/Maes | Réplica en EUA 2003-2015: 11.4% contra 8.7% del S&P. El libro reportaba alrededor de 30%, con un backtest del propio autor | C | [8] |
| 15 | *Investment Valuation* (Wiley; 4.ª ed., 2024) y *Narrative and Numbers* (Columbia UP, 2017) · Damodaran (+ *The Corporate Life Cycle*, ago-2024) | B · Maes | Herramienta; no hay alfa atribuible | A (herramienta) / C (alfa) | [9] |
| 16 | *Expectations Investing* · Rappaport y Mauboussin · 2001; ed. revisada 2021 | B · Maes | Método (DCF inverso) sin backtest | B | [10] |
| 17 | *The Most Important Thing* (Columbia UP, 2011; *Illuminated*, 2012) y *Mastering the Market Cycle* (2018) · Marks | C · Lic/Maes | Oaktree levantó US$10.9 mil millones en 2008: el mayor fondo de deuda en problemas de la historia | B (riesgo) / C (timing) | [6] |
| 18 | *A Man for All Markets* · Thorp · Random House, 2017 | C · Lic/Práct | Thorp reportó en 1998 un 20% anual en 28.5 años. Ridgeline cerró en 2002 por el bajo rendimiento del arbitraje estadístico | A (Kelly) / D (replicar) | [11] |
| 19 | *Fortune's Formula* · Poundstone · Hill and Wang, 2005 | C · Lic | Experimento Haghani-Dewey: con una ventaja de 60/40, el 28% de los participantes quebró | A | [12][13] |
| 20 | *When Genius Failed* · Lowenstein · Random House, 2000 | C · Lic | LTCM: apalancamiento de más de 25:1; perdió US$4.6 mil millones en menos de 4 meses; recapitalización de US$3.625 mil millones | A | [40] |
| 21 | *A Random Walk Down Wall Street* · Malkiel · 1973; 13.ª ed. (50 aniversario), 2023 | D · Lic | SPIVA EUA 2025: 79% de los fondos activos large-cap perdió contra el índice | A | [27][47] |
| 22 | *The Little Book of Common Sense Investing* · Bogle · Wiley, 2007; ed. de 10.º aniversario, 2017 | D · Lic | SPIVA México: 75.6% de los fondos activos perdió contra el índice a 10 años (cap. 01) | A | [25][47] |
| 23 | *Stocks for the Long Run* · Siegel · 1994; 6.ª ed., McGraw-Hill, 2022 | D · Lic | ~6.5-7% real anual en 200 años. McQuarrie: en 1797-1942, acciones ≈ bonos | B | [28] |
| 24 | *Triumph of the Optimists* · Dimson, Marsh y Staunton · Princeton UP, 2002 (+ Yearbook anual) | D · Maes | 16 países, 101 años. El Yearbook 2026 cubre 35 mercados y 126 años; EUA rindió 6.6% real | A | [29] |
| 25 | *Pioneering Portfolio Management* (2000; ed. revisada 2009) y *Unconventional Success* (2005) · Swensen | D · Maes/Lic | Yale: 12.4% anual en los 30 años a 2020; −24.6% en 2008 | B (individuos) / C (modelo endowment) | [24] |
| 26 | *Expected Returns* (Wiley, 2011) y *Investing Amid Low Expected Returns* (Wiley, abr-2022) · Ilmanen | D · Doc/Práct | Factores long-short de EUA 2016-2025: ≈0 bruto (cap. 02) | B | [22] |
| 27 | *Efficiently Inefficient* · L. H. Pedersen · Princeton UP, 2015 | D · Maes/Doc | Marco de primas por liquidez e información | B | [23] |
| 28 | *Adaptive Markets* · A. Lo · Princeton UP, 2017 | D · Maes | Congruente con el decaimiento post-publicación (−58%, McLean-Pontiff) | C | [30] |
| 29 | *Asset Pricing* · Cochrane · 2001; ed. revisada 2005 | D · Doc | "Discount Rates" (JF, 2011): toda la variación del precio/dividendo corresponde a variación de las tasas de descuento | A (marco) | [42] |
| 30 | *Irrational Exuberance* · Shiller · Princeton UP, mar-2000; 2.ª ed. 2005; 3.ª ed. 2015 | E · Lic/Maes | Salió el mes del pico del Nasdaq, que después cayó más de 80% en dos años | B/C | [31] |
| 31 | *Manias, Panics, and Crashes* · Kindleberger (1978); 8.ª ed. con Aliber y McCauley, Springer, 2023 | E · Maes | Patrón de 5 etapas (cap. 17) | B | [32] |
| 32 | *This Time Is Different* · Reinhart y Rogoff · Princeton UP, 2009 | E · Maes | 66 países y 8 siglos. Tras una crisis bancaria, la vivienda real cae ~35% en ~6 años (cap. 16) | B | [33] |
| 33 | *Principles* (Simon & Schuster, 2017) y *Principles for Navigating Big Debt Crises* (2018) · Dalio (+ *How Countries Go Broke*, 2025) | E · Lic/Maes | Pure Alpha II: −18.6% en 2020 (a agosto) y +33% en 2025 (cap. 18) | B (proceso) / D (como reloj) | [21] |
| 34 | *The Alchemy of Finance* · Soros · 1987; reeditado 2003 | E · Maes | Quantum: más de 20% compuesto; más de US$1,000 millones en 1992 | C | [18] |
| 35 | *Advances in Financial Machine Learning* · López de Prado · Wiley, 2018 (+ *ML for Asset Managers*, 2020; *Causal Factor Investing*, 2023) | F · Doc/Práct | El DSR (JPM, 2014) corrige el sesgo de selección, las pruebas múltiples y la no normalidad | A (validación) / C (alfa) | [34][35][36] |
| 36 | *Systematic Trading* · Carver · Harriman House, 2015 (+ *Leveraged Trading*, 2019; *Advanced Futures Trading Strategies*, abr-2023) | F · Práct | Marco sin historial auditado público | B | [37] |
| 37 | *Quantitative Trading* (Wiley, 2008; 2.ª ed. 2021) y *Algorithmic Trading* (Wiley, 2013) · E. Chan | F · Práct | Backtests dentro de muestra | C | [38] |
| 38 | *The Man Who Solved the Market* · Zuckerman · Portfolio, 2019 | F · Lic | Medallion: 66% bruto y 39% neto anual (1988-2018) | A (hecho) / D (transferible) | [39] |
| 39 | *Reminiscences of a Stock Operator* · Lefèvre · 1923; ed. anotada, Wiley, 2009 | G · Práct | Livermore quebró varias veces y se suicidó en 1940 (cap. 18) | D | [19] |
| 40 | *Market Wizards* · Schwager · 1989 (serie hasta *Unknown Market Wizards*, 2020) | G · Práct | No hay grupo de control | C/D | [20] |

### 3.2 Las 40 fichas: tesis, lecciones y contra

**Estante A — Decisión e incertidumbre**

**1. Kahneman.** *Tesis:* el juicio intuitivo (Sistema 1) comete errores sistemáticos y predecibles. La teoría prospectiva describe decisiones donde las pérdidas pesan más que las ganancias. *Noise* agrega que la varianza entre juicios (ruido) cuesta tanto como el sesgo. *Lecciones:* (1) partir de la tasa base (visión externa) antes del caso particular; (2) escribir la probabilidad antes de ver el resultado, contra el sesgo retrospectivo; (3) revisar el portafolio con menos frecuencia, porque la aversión miope a las pérdidas empuja a vender en las caídas; (4) promediar juicios independientes y usar reglas simples para bajar el ruido. *Contra:* parte del libro no replicó. Los sesgos describen a los demás; no son alfa por sí mismos.

**2. Tetlock y Gardner.** *Tesis:* pronosticar es una habilidad medible (Brier), entrenable y agregable. Los mejores descomponen el problema, parten de la tasa base, actualizan en pasos pequeños y piensan como "zorros". *Lecciones:* (1) formular cada tesis como una pregunta con fecha y probabilidad; (2) descomponer al estilo Fermi; (3) actualizar poco y seguido; (4) llevar un marcador Brier y ponderar a cada quien por su historial; (5) agregar pronósticos independientes. *Contra:* las preguntas de IARPA eran geopolíticas y binarias. En un mercado el precio ya agrega pronósticos, así que la ventaja hay que tenerla contra el precio y no contra un analista.

**3. Duke.** *Tesis:* decidir es apostar con información incompleta, y juzgar una decisión por su resultado (*resulting*) es el error central. *Lecciones:* (1) separar en el post-mortem la calidad de la decisión de la suerte; (2) expresar la convicción en porcentaje; (3) hacer un pre-mortem antes de entrar; (4) fijar de antemano los criterios de abandono (el tema de *Quit*); (5) tener alguien que ataque la tesis. *Contra:* en el póker la retroalimentación es rápida. En inversión la muestra es chica y la señal débil, así que el post-mortem necesita N grande.

**4. Taleb.** *Tesis:* confundimos suerte con habilidad y subestimamos los extremos de alto impacto (Extremistán). Una estrategia que "ganó 50 veces" puede esconder la ruina: los vendedores de opciones "eat like chickens and go to the bathroom like elephants". *Lecciones:* (1) desconfiar de los historiales cortos con sesgo negativo; (2) dimensionar por la pérdida máxima plausible y no por una σ gaussiana; (3) barbell: un núcleo muy seguro con un satélite convexo de pérdida acotada; (4) pensar en los caminos alternos que no ocurrieron. *Contra:* no da reglas de entrada, y la cobertura de cola permanente pierde contra alternativas más baratas (cap. 05).

**5. Mauboussin (ensayos y suerte-habilidad).** *Tesis:* a largo plazo gana el proceso. En actividades con mucha suerte, la habilidad se mide con muestras grandes y hay que esperar regresión a la media. Paradoja de la habilidad: cuando todos son hábiles, decide más la suerte. *Lecciones:* (1) ubicar la actividad en el continuo suerte-habilidad antes de juzgar a nadie, rivales incluidos; (2) usar tasas base para el crecimiento de ventas y de márgenes; (3) no extrapolar el mejor semestre; (4) la sabiduría de la multitud requiere independencia. *Contra:* son ensayos, no pruebas.

**6. Munger.** *Tesis:* un enrejado de modelos mentales de varias disciplinas, inversión del problema y una lista de 25 sesgos cuya combinación ("lollapalooza") produce extremos. *Lecciones:* (1) invertir el problema: listar cómo fracasaría la tesis; (2) usar un checklist multidisciplinario; (3) pocas decisiones grandes y paciencia; (4) un círculo de competencia explícito. *Contra:* la sociedad tuvo −32% en 1973 y −31% en 1974 (cap. 18). La concentración exige tolerar caídas que los cortacircuitos de la cuenta no permiten.

**7. Housel.** *Tesis:* el resultado financiero depende más de la conducta que de la inteligencia. Sobrevivir con margen de error deja operar al compuesto, y unos pocos eventos de cola explican casi todo. *Lecciones:* (1) dejar margen de error en cada plan; (2) "razonable" le gana a "racional": elegir la estrategia que sí se va a sostener; (3) no salirse del mercado en los eventos de cola; (4) definir qué es "suficiente". *Contra:* anécdotas elegidas. Lo que tiene de cuantificable ya está en Bessembinder y DMS (cap. 01).

**8. Bernstein.** *Tesis:* la historia del concepto de riesgo, de Pascal y Fermat a Bernoulli, Galton, Markowitz y Kahneman-Tversky, y la frontera entre riesgo medible e incertidumbre. *Lecciones:* (1) separar riesgo (distribución conocida) de incertidumbre (Knight); (2) la regresión a la media existe, pero engaña cuando la media cambia; (3) utilidad no es valor esperado (Bernoulli), que es la base de Kelly. *Contra:* se publicó antes de LTCM, de 2008 y de la literatura de factores.

**Estante B — Negocio y valuación**

**9. Graham (*Intelligent Investor* y *Security Analysis*).** *Tesis:* una acción es parte de un negocio. El precio lo pone un "Señor Mercado" de ánimo cambiante, y se compra con margen de seguridad. Distingue inversión de especulación y al inversionista defensivo del emprendedor. *Lecciones:* (1) estimar el valor como un rango conservador, no como un punto; (2) el margen de seguridad protege contra el error propio; (3) el defensivo diversifica con reglas mecánicas, y solo es "emprendedor" quien dedica tiempo real; (4) normalizar el poder de ganancia con varios años. *Contra:* el propio Graham, en los años 70: "I doubt whether in most cases such extensive efforts will generate sufficiently superior selections to justify their cost" [2]. Las reglas numéricas de 1973 no se trasladan tal cual.

**10. Fisher.** *Tesis:* comprar pocas empresas excepcionales, con crecimiento por I+D y una administración superior, investigadas con *scuttlebutt* (clientes, proveedores, competidores). El mejor momento para vender es "almost never". *Lecciones:* (1) investigar en campo a lo largo de la cadena de valor; (2) juzgar la calidad de la administración y de su reinversión; (3) no vender por una sobrevaluación leve. John Train describió a Buffett como "85% Graham y 15% Fisher". *Contra:* sesgo de supervivencia (Motorola). La mayoría de las acciones pierde contra los T-bills (Bessembinder), así que "casi nunca vender" solo funciona si se atina a los pocos ganadores.

**11. Cunningham / Buffett.** *Tesis:* las cartas de Buffett ordenadas por tema: gobierno corporativo, asignación de capital, valor intrínseco contra valor contable, recompras solo debajo del valor y el float de seguros. *Lecciones:* (1) medir un negocio por su rentabilidad sin apalancamiento excesivo y por sus *owner earnings*; (2) recomprar solo debajo del valor conservador; (3) no usar un apalancamiento que obligue a vender; (4) pensar como dueño. *Contra:* el motor es value, calidad y beta baja apalancados ~1.6-1.7× con float barato (Frazzini-Kabiller-Pedersen; caps. 03 y 18), y ese motor no se copia en GBM. El alfa decayó con el tamaño. Buffett dejó de ser CEO el 31-dic-2025.

**12. Lynch.** *Tesis:* el individuo puede ver una empresa antes que Wall Street, siempre que después revise los fundamentales. Clasifica las acciones en seis tipos: crecimiento lento, *stalwarts*, crecimiento rápido, cíclicas, *turnarounds* y *asset plays*. *Lecciones:* (1) clasificar antes de valuar, porque cada tipo pide otra métrica y otra salida; (2) poder explicar la tesis en dos minutos; (3) dejar correr a los ganadores (*tenbaggers*); (4) en las cíclicas, un P/U bajo en el pico de utilidades es una trampa. *Contra:* Lynch tenía cientos de acciones y el equipo de Fidelity. "Invierte en lo que conoces" coincide con el sesgo de familiaridad documentado por Huberman (RFS, 2001) [45].

**13. Klarman.** *Tesis:* invertir con aversión al riesgo buscando rendimiento absoluto, comprar con descuento sobre un valor conservador y aprovechar las restricciones institucionales de otros. *Lecciones:* (1) medir en pérdida permanente, no contra un índice; (2) el efectivo es una opción (llegó a 30-50%); (3) buscar vendedores forzados (spin-offs, quiebras); (4) exigir un catalizador. *Contra:* el efectivo alto tiene costo de oportunidad y el historial reportado no está auditado.

**14. Greenblatt.** *Tesis:* comprar de forma sistemática "buenas empresas baratas", con EBIT/EV alto y ROC alto: 20-30 acciones con rebalanceo anual. Y en *Genius*, situaciones especiales donde vendedores no económicos equivocan el precio. *Lecciones:* (1) combinar calidad con valor; (2) sostener la disciplina en los años de rezago; (3) buscar eventos con vendedores forzados; (4) una regla simple le gana al juicio ruidoso. *Contra:* la réplica independiente se quedó lejos del ~30% del libro y estuvo por debajo del S&P en 2007-2011. Un estudio de 2024 (EUA 1963-2022) atribuye su rendimiento sobre todo a exposición a factores conocidos [8]. Los spin-offs decayeron (cap. 15).

**15. Damodaran.** *Tesis:* cualquier activo se valúa con flujos, crecimiento y riesgo coherentes entre sí. Una valuación es una historia convertida en números, y cada número necesita una historia. *Lecciones:* (1) coherencia: crecimiento = reinversión × ROIC, y la tasa en la misma moneda que los flujos (MXN o USD); (2) historia → variables (mercado, margen, reinversión, riesgo) → valor → revisión; (3) pasar la historia por los filtros de posible, plausible y probable; (4) el ciclo de vida cambia las métricas relevantes (*The Corporate Life Cycle*); (5) que algo esté barato no garantiza que el precio converja. *Contra:* el DCF es muy sensible a sus supuestos y no es una regla de trading.

**16. Rappaport y Mauboussin.** *Tesis:* en lugar de pronosticar el valor, leer las expectativas que ya trae el precio (DCF inverso) y apostar solo cuando se anticipa una revisión de esas expectativas. *Lecciones:* (1) calcular qué crecimiento, qué margen y qué duración de la ventaja descuenta el precio; (2) identificar el disparador de valor (ventas, costos o inversión) con más impacto; (3) comprar solo si la brecha es grande y hay catalizador; (4) una recompra crea valor solo debajo del valor intrínseco. *Contra:* la ventaja exige pronosticar mejor que el consenso, y eso es difícil (cap. 25).

**Estante C — Tamaño y supervivencia**

**17. Marks.** *Tesis:* pensamiento de segundo nivel. El riesgo es la probabilidad de pérdida permanente, no la volatilidad. Los ciclos de economía, crédito y psicología oscilan como un péndulo: se puede saber "dónde estamos" sin saber "a dónde vamos". *Lecciones:* (1) preguntar qué descuenta el consenso y en qué se difiere de él; (2) tomar la temperatura con síntomas como la apertura del crédito, las emisiones de baja calidad y el "esta vez es distinto"; (3) ajustar la agresividad dentro de límites; (4) evitar perdedores rinde más que buscar ganadores. *Contra:* no tiene reglas cuantitativas, y el ciclo es fácil de diagnosticar a posteriori.

**18. Thorp.** *Tesis:* el matemático que venció al blackjack con conteo de cartas y Kelly, y después al mercado con arbitraje de derivados. La ventaja debe ser medible y el tamaño, disciplinado. *Lecciones:* (1) sin ventaja cuantificada no hay apuesta; (2) Kelly fraccional contra el error de estimación; (3) cubrir los riesgos que no pagan; (4) detectar el fraude por su imposibilidad estadística (dudó de Madoff desde 1991); (5) las ventajas se agotan. *Contra:* sus oportunidades de los años 60 a 80 ya están arbitradas.

**19. Poundstone.** *Tesis:* la historia del criterio de Kelly (Bell Labs, Shannon, Thorp) y de su pleito con Samuelson. El crecimiento geométrico depende del tamaño correcto de la apuesta. *Lecciones:* (1) maximizar el logaritmo de la riqueza equivale a maximizar el CAGR, que es la función objetivo de `parametros.json`; (2) apostar el doble de Kelly baja el crecimiento a la tasa libre de riesgo (cap. 01); (3) una fracción de Kelly recorta mucho la volatilidad y poco el crecimiento. *Contra:* Samuelson: "When you lose — and you sure can lose — with N large, you can lose real big" [12]. En un torneo de 6 meses el objetivo no es la utilidad logarítmica (cap. 18, §5.5).

**20. Lowenstein.** *Tesis:* la caída de LTCM: premios Nobel, modelos de convergencia y apalancamiento. *Lecciones:* (1) en una fuga hacia la liquidez, las posiciones "diversificadas" se mueven juntas; (2) el apalancamiento convierte pérdidas temporales en permanentes: la prima de Royal Dutch sobre Shell pasó de 8-10% a ~22% antes de converger; (3) una posición grande respecto de su mercado es una posición ilíquida; (4) devolver capital sin reducir posiciones sube el apalancamiento; (5) el "largo plazo" no existe si llegan llamadas de margen. *Contra:* es un relato periodístico que no estima la probabilidad ex ante.

**Estante D — Mercados y rendimientos esperados**

**21. Malkiel.** *Tesis:* los precios siguen aproximadamente una caminata aleatoria. Ni el análisis técnico ni el fundamental le ganan al índice de forma consistente, neto de costos. *Lecciones:* (1) un núcleo indexado barato; (2) rebalancear y diversificar entre países; (3) no elegir fondos por su desempeño pasado; (4) las burbujas se ven con claridad solo después. *Contra:* las anomalías existen dentro de muestra, pero su decaimiento tras publicarse (caps. 02 y 03) le da la razón a Malkiel neto de costos.

**22. Bogle.** *Tesis:* la aritmética: en conjunto, los inversionistas obtienen el mercado menos costos, así que el índice barato le gana a la mayoría. *Lecciones:* (1) minimizar comisiones, rotación, spread e impuestos; (2) comprar el pajar en vez de buscar la aguja; (3) estimar el rendimiento a 10 años como dividendo + crecimiento + cambio de P/U; (4) mantener al menos 20% en bonos para la mayoría. *Contra:* en un torneo, indexar asegura la mediana, no el primer lugar.

**23. Siegel.** *Tesis:* desde 1802, las acciones de EUA rinden de 6.5% a 7% real, y a horizontes largos son menos riesgosas que los bonos en poder de compra. *Lecciones:* (1) el horizonte cambia cuál es el riesgo relevante; (2) la estabilidad del rendimiento real justifica tener acciones; (3) valuaciones altas implican rendimientos menores. *Contra:* McQuarrie reconstruyó los datos y encontró que en 1797-1942 las acciones rindieron casi lo mismo que los bonos, y que Siegel subestimó en ~1.5 pp el rendimiento de los bonos del siglo XIX. EUA es el ganador ex post (DMS).

**24. Dimson, Marsh y Staunton.** *Tesis:* 101 años en 16 países. Las acciones ganan en el largo plazo, pero los índices con sobrevivientes y los datos de EUA sobreestiman la prima esperada. *Lecciones:* (1) basarse en la evidencia global y no solo en EUA; (2) esperar una prima menor que la histórica de EUA; (3) actualizar cada año con el Yearbook. *Contra:* Inferencia: aun con 35 mercados, la muestra sigue sesgada hacia los países que sobrevivieron.

**25. Swensen.** *Tesis:* para una institución perpetua: diversificar mucho, sesgarse a renta variable, ir a activos ilíquidos donde hay más alfa y seleccionar gestores con rigor. Para el individuo: seis clases de activo (acciones de EUA, desarrolladas, emergentes, REITs, Treasuries y TIPS), rebalanceo y fondos índice baratos. *Lecciones:* (1) la política de asignación pesa más que la selección; (2) rebalancear con disciplina; (3) la iliquidez es un costo que solo conviene a quien puede cargarlo; (4) cuidarse de los conflictos de interés de la industria. *Contra:* Charles Ellis considera difícil de replicar el modelo de Yale, y las primas alternativas se comprimen [24]. Con MXN 20,000, los ilíquidos no están al alcance.

**26. Ilmanen.** *Tesis:* estimar rendimientos esperados desde cuatro ángulos: clases de activo, estilos, factores y variación en el tiempo. En 2022, tras décadas de revaluación, los rendimientos esperados estaban en mínimos, y lo que queda es disciplina, humildad y control de costos. *Lecciones:* (1) descomponer el rendimiento histórico en yield + crecimiento + cambio de valuación, y no proyectar la revaluación; (2) diversificar entre primas de estilo; (3) timing táctico solo en dosis pequeñas; (4) el ahorro en costos es el alfa más seguro. *Contra:* el libro de 2022 salió justo antes de que subieran las tasas, y los estilos long-short tuvieron una década pobre (cap. 02).

**27. Pedersen.** *Tesis:* los mercados son lo bastante ineficientes para compensar a los gestores activos por sus costos y por el riesgo de liquidez, pero no más. Explica las estrategias de hedge funds (acciones discrecionales, cuantitativas, macro, futuros administrados, arbitrajes) y trae entrevistas con sus gestores. *Lecciones:* (1) toda estrategia rentable es el pago por un servicio: liquidez, riesgo o información; (2) preguntar quién está del otro lado (cap. 26); (3) la liquidez de mercado y la de fondeo se refuerzan en espiral. *Contra:* el marco es sólido, pero cada prima concreta decayó.

**28. Lo.** *Tesis:* la eficiencia varía con el entorno. Las estrategias nacen, se saturan y mueren como especies, y los sesgos son heurísticas adaptadas a otro ambiente. *Lecciones:* (1) esperar que toda ventaja decaiga y vigilar su vida útil; (2) las primas dependen del régimen; (3) diversificar entre estrategias de "ecologías" distintas. *Contra:* cuesta falsarlo; es más un marco que una predicción.

**29. Cochrane.** *Tesis:* todo precio es p = E(mx), un factor de descuento estocástico, y el resto son casos particulares. *Lecciones:* (1) una anomalía es riesgo o precio equivocado, así que hay que preguntar en qué estados del mundo paga mal; (2) los rendimientos esperados varían en el tiempo y la valuación los predice a horizontes largos; (3) conviene dominar GMM y las pruebas de factores. *Contra:* es un texto técnico y no un manual, y a corto plazo la predictibilidad es de R² bajo (Inferencia).

**Estante E — Crisis y ciclos**

**30. Shiller.** *Tesis:* las burbujas son circuitos de retroalimentación (precio → narrativa → precio). Un CAPE alto anticipa rendimientos bajos a 10 años. La 2.ª edición advirtió de la burbuja inmobiliaria. *Lecciones:* (1) ante una valuación alta, bajar la expectativa de rendimiento; (2) identificar los amplificadores: medios, "nueva era" y crédito; (3) a largo plazo, la vivienda rinde menos de 1% real anual. *Contra:* Fama: Shiller "has been consistently pessimistic", y con un horizonte largo cualquier pesimista le atina a una crisis [31].

**31. Kindleberger.** *Tesis:* las crisis siguen el patrón de Minsky: desplazamiento → auge con crédito → euforia → dificultad financiera → pánico, y el prestamista de última instancia decide el desenlace. La 8.ª ed. agrega cripto y el papel global del dólar y la Fed [32]. *Lecciones:* (1) fechar la etapa por el crédito, no por el precio; (2) el fraude aparece al final del auge; (3) el contagio viaja por los flujos de capital. *Contra:* no da timing; ex post todo encaja.

**32. Reinhart y Rogoff.** *Tesis:* los defaults, las crisis bancarias, la inflación y los colapsos cambiarios se repiten en todas partes y en todos los siglos. *Lecciones:* (1) "esta vez es distinto" es la frase de alarma; (2) deuda externa con tipo de cambio fijo es fragilidad; (3) las recuperaciones tras una crisis bancaria son largas. *Contra:* el error de Excel pertenece a otro trabajo, *Growth in a Time of Debt* (2010): con deuda de más de 90% del PIB reportaron −0.1% de crecimiento, que corregido daba 2.2% (Herndon-Ash-Pollin, 2013) [33]. No invalida la base de datos del libro, pero enseña a desconfiar de los umbrales duros.

**33. Dalio.** *Tesis:* "dolor + reflexión = progreso". Decidir con transparencia radical y con opiniones ponderadas por su credibilidad. Las crisis de deuda siguen arquetipos (deflacionario o inflacionario) y el ideal es un "desapalancamiento hermoso". *Lecciones:* (1) escribir las decisiones y los principios y revisarlos con cada error; (2) ponderar opiniones por historial, como el Brier del comité; (3) diversificar entre flujos no correlacionados (paridad de riesgo); (4) conocer los canales deuda → monetización → moneda. *Contra:* *The Fund* (Copeland, nov-2023) describe una cultura de vigilancia; Dalio la rechazó [21]. Como reloj de crisis no tiene señales fechadas verificables (cap. 16).

**34. Soros.** *Tesis:* reflexividad: las percepciones sesgadas de los participantes cambian los fundamentales (crédito ↔ colateral) y generan auges y quiebras lejos del equilibrio. *Lecciones:* (1) buscar los circuitos que se refuerzan solos (crédito-colateral, precio-emisión); (2) posiciones grandes cuando la tesis es fuerte y salida rápida si falla; (3) reconocer la propia falibilidad. *Contra:* la teoría es poco falsable, y él mismo admitió "I have a record of crying wolf" [18].

**Estante F — Cuantitativo**

**35. López de Prado.** *Tesis:* la mayoría de los descubrimientos de las finanzas cuantitativas son falsos por sobreajuste y pruebas múltiples. Hacen falta etiquetas, validación y métricas diseñadas para series financieras. *Causal Factor Investing* agrega que la literatura de factores es asociacional y no causal, con errores de especificación y confusores omitidos [35]. *Lecciones:* (1) Deflated Sharpe Ratio; (2) probabilidad de sobreajuste del backtest (PBO); (3) validación cruzada purgada y con embargo; (4) etiquetado de triple barrera y meta-etiquetado para dimensionar; (5) registrar cuántas pruebas se hicieron. *Contra:* los métodos piden muchos datos, y hay poca evidencia pública de alfa neto obtenido con ellos.

**36. Carver.** *Tesis:* un marco modular: pronósticos escalados y combinados, volatilidad objetivo y control de costos, suponiendo que el Sharpe real será menor que el del backtest. *Lecciones:* (1) dimensionar por volatilidad; (2) pronósticos continuos en lugar de binarios; (3) un presupuesto de costos por rotación; (4) preferir la simplicidad a la optimización. *Contra:* está pensado para futuros diversificados; en GBM, con MXN 20,000 y ejecución manual, la diversificación y la rotación quedan limitadas.

**37. Chan.** *Tesis:* un individuo puede montar estrategias cuantitativas simples (reversión a la media, pares, momentum) si hace backtests honestos y usa Kelly y control de riesgo. *Lecciones:* (1) revisar los sesgos del backtest: look-ahead, supervivencia y costos; (2) probar estacionariedad y cointegración antes de operar pares; (3) la capacidad y los costos definen la estrategia. *Contra:* los ejemplos son de rotación alta y se degradan; las cifras son dentro de muestra.

**38. Zuckerman.** *Tesis:* Simons y Renaissance: científicos, datos limpios y miles de señales pequeñas. *Lecciones:* (1) muchas apuestas con ventaja leve le ganan a pocas apuestas grandes; (2) la investigación tiene que ser industrial y reproducible; (3) limitar la capacidad protege la ventaja. *Contra:* el fondo abierto a externos (RIEF) quedó muy por debajo de Medallion [39]. No es replicable; Simons murió en 2024.

**Estante G — Practicantes**

**39. Lefèvre.** *Tesis:* novela en clave sobre Jesse Livermore: leer la tendencia, esperar el momento, dejar correr las ganancias y no promediar las pérdidas. *Lecciones:* (1) cortar pérdidas rápido y quedarse con las ganancias; (2) no operar por tips; (3) la paciencia paga más que la actividad; (4) el apalancamiento de 100 a 1 de los *bucket shops* también llevó a la quiebra. *Contra:* no tiene estadística, y el protagonista murió en la ruina.

**40. Schwager.** *Tesis:* entrevistas con traders excepcionales, que coinciden en control de riesgo, disciplina y un método ajustado a la personalidad de cada uno. *Lecciones:* (1) un riesgo por operación pequeño y fijo; (2) un método que calce con el horizonte y la tolerancia propios; (3) reducir el tamaño en las rachas perdedoras. *Contra:* sesgo de supervivencia extremo, sin grupo de control.

## 4. Lo más reciente 2023-2026

| Fecha | Novedad | Qué cambia en la lectura |
|---|---|---|
| abr-2023 | Carver, *Advanced Futures Trading Strategies* [37] | Versión actual de su marco |
| 27-jun-2023 | *Security Analysis*, 7.ª ed., McGraw-Hill (con Klarman) [2] | Leer esta y no la 6.ª (2008) |
| 2023 | Malkiel, 13.ª ed. (50 aniversario) [27] | Edición vigente |
| 2023 | Kindleberger, Aliber y McCauley, 8.ª ed. (Springer) [32] | Agrega cripto y el papel del dólar y la Fed como prestamista global |
| 2023 | López de Prado, *Causal Factor Investing* (Cambridge Elements) [35] | Separa los errores de sobreajuste (tipo A) de los confusores omitidos (tipo B) |
| 2023 | Housel, *Same as Ever*; Stripe Press reedita *Poor Charlie's Almanack* [41][43] | — |
| sep-2023 | Haghani y White, *The Missing Billionaires* (Wiley) [44] | Las fortunas que faltan se perdieron por el tamaño de las apuestas y el gasto, no por elegir mal los activos. Complemento operable de Thorp y Poundstone |
| nov-2023 | Copeland, *The Fund* [21] | Contrapunto a *Principles* |
| 28-nov-2023 | Muere Munger [43] | Su obra queda cerrada |
| 2023 | Jensen-Kelly-Pedersen (JF): la mayoría de los factores replica dentro de muestra (cap. 02) | Respalda a Cochrane, Ilmanen y Pedersen, pero después de publicarse las primas decaen |
| 2024 | McQuarrie, FAJ 80(1) (cap. 01) [28] | Refuta la versión "siempre acciones" de Siegel |
| 2024 | *The Intelligent Investor*, 3.ª ed. revisada con Zweig (Harper Business) [1] | Edición vigente |
| 27-mar-2024 | Muere Kahneman [15] | — |
| 2024 | Muere Simons [39] | — |
| 2024 | Damodaran: *Investment Valuation*, 4.ª ed.; *The Corporate Life Cycle* (ago-2024) [9] | Métricas distintas según la etapa del ciclo de vida |
| 2024 | Estudio de fórmulas en EUA 1963-2022 (fórmula mágica, F-score, Acquirer's Multiple, Conservative Formula) [8] | Las cuatro rinden, sobre todo por exposición a factores; ninguna domina en todas las métricas |
| 2025 | Dalio, *How Countries Go Broke*; Housel, *The Art of Spending Money* [21][41] | — |
| 31-dic-2025 | Buffett deja de ser CEO; la carta de 2025 la firma Greg Abel (28-feb-2026) (cap. 03) [46] | *The Essays* quedan como el corpus completo de Buffett como CEO |
| mar-2026 | UBS Global Investment Returns Yearbook 2026 (DMS) (cap. 01) [29] | 35 mercados, 126 años |
| dic-2026 | Carver anuncia *The Art and Science of Trading* [37] | (contenido no verificado) |

**Experimento de Haghani y Dewey (2016), la base de *The Missing Billionaires*.** 61 participantes, US$25 iniciales, moneda con 60% de probabilidad de cara, apuestas a la par, 30 minutos y premio con tope de US$250. El 28% quebró, solo el 21% llegó al tope y el pago promedio fue de US$91. Kelly indicaba apostar 20% en cada tiro [12]. **Inferencia:** incluso con la ventaja explícita, el error dominante fue el tamaño. Es la prueba más limpia de que el estante C importa más que el B.

## 5. Evidencia real: qué funciona, qué no, magnitudes

### 5.1 Tesis del canon contra la evidencia independiente

| Tesis (libros) | Evidencia | Magnitud | Grado |
|---|---|---|---|
| El índice barato le gana a la mayoría (21, 22, 25) | SPIVA EUA y México (cap. 01) | 79% pierde (EUA, 2025); 75.6% pierde a 10 años (México) | **A** |
| Las acciones le ganan a los bonos a largo plazo (23, 24) | DMS 2026; McQuarrie 2024 | EUA 6.6% real (1900-2025), pero hay periodos multidecenales de empate | **B** |
| Margen de seguridad y valor (9, 13, 14) | HML; réplicas de la fórmula mágica | −57.8% (dic-2006 a sep-2020); 11.4% contra 8.7% (2003-2015) | **B/C** |
| Calidad + valor + beta baja con apalancamiento (11) | Frazzini-Kabiller-Pedersen; carta de 2025 | Sharpe ≈0.76-0.79 según periodo; 2011-2025: 13.0% contra 14.1% | **A** mecanismo / **C** alfa futuro |
| Kelly maximiza el crecimiento (18, 19) | Teorema; experimento de la moneda | 28% quebró teniendo la ventaja | **A** |
| Colas gruesas (4) | Hecho estadístico; costo de la cobertura (cap. 05) | +3,612% sobre la prima en un mes (Universa) contra la sangría continua | **A** hecho / **D** cobertura permanente |
| El pronóstico se entrena (2) | GJP/IARPA | 35-72% más preciso que otros equipos | **A** geopolítica / **C** precios |
| Sesgos cognitivos (1) | Crisis de replicación | R-index de 14 en el capítulo de priming | **B** prospectiva / **D** priming |
| Ciclos y crisis (30-34, 17) | Reinhart-Rogoff, Kindleberger | Vivienda −35% y desempleo +7 pp tras una crisis bancaria (cap. 16) | **B** descriptivo / **D** timing |
| Apalancamiento + iliquidez mata (20) | LTCM | De US$4.7 mil millones de capital a US$400 millones el 25-sep-1998; apalancamiento efectivo de más de 250:1 | **A** |
| Los backtests se sobreajustan (35-37) | McLean-Pontiff; DSR | −26% fuera de muestra, −58% después de publicarse | **A** |
| "Invierte en lo que conoces" (12) | Huberman 2001 | Sesgo de familiaridad | **D** como regla |
| Modelo endowment (25) | Yale | 12.4% en 30 años; −24.6% en 2008; difícil de replicar | **C** para individuos |
| Medallion (38) | Cifras reportadas por el libro | 66% bruto y 39% neto | **D** transferible |
| Reflexividad, mercados adaptativos (34, 28) | Poco falsables | — | **C** |

### 5.2 Qué envejeció bien y qué mal

- **Envejecieron bien (A/B):** Bogle, Malkiel, Thorp y Poundstone (Kelly), Lowenstein, Reinhart-Rogoff, Kindleberger, DMS, Cochrane, la teoría prospectiva de Kahneman, Tetlock y la parte de validación de López de Prado.
- **Envejecieron mal o requieren fe de erratas:** la versión "siempre acciones" de Siegel (McQuarrie), el ~30% de Greenblatt, el capítulo de priming de Kahneman, el modelo endowment de Swensen para individuos, Dalio como reloj, "invierte en lo que conoces" de Lynch y Market Wizards como plantilla.
- **Inferencia:** los libros que envejecen mejor son los de aritmética, historia y validación. Los que envejecen peor son los que prometen un método de selección con cifras de backtest propio, porque la publicación misma erosiona la ventaja (Lo, McLean-Pontiff).

## 6. Traducción operable

### 6.1 Ruta de lectura por nivel (orden recomendado)

| Nivel | Orden (número de ficha) | Objetivo |
|---|---|---|
| **1. Licenciatura: conducta y aritmética** | 22 Bogle → 21 Malkiel → 7 Housel → 9a *Intelligent Investor* → 3 Duke → 8 Bernstein → 12 Lynch → 10 Fisher → 11 Buffett → 17a *The Most Important Thing* → 20 Lowenstein → 38 Zuckerman → 6 Munger | Saber por qué indexar es la base, qué es margen de seguridad y cómo muere un fondo |
| **2. Maestría: evidencia, valuación, tamaño y ciclos** | 23 Siegel → 24 DMS → 1 Kahneman → 2 Tetlock → 4 Taleb → 5 Mauboussin → 16 Expectations → 15 Damodaran (N&N → IV) → 13 Klarman → 14 Greenblatt → 18 Thorp → 19 Poundstone → 17b *Market Cycle* → 25 Swensen → 30 Shiller → 31 Kindleberger → 32 Reinhart-Rogoff → 33 Dalio → 34 Soros | Poner en duda cada tesis con datos; valuar; dimensionar; reconocer la etapa del ciclo |
| **3. Doctorado: asset pricing y validación** | 29 Cochrane → 26 Ilmanen (ER → ILER) → 27 Pedersen → 28 Lo → 35 López de Prado → 9b *Security Analysis* (7.ª) | Saber de dónde sale cada prima y cómo no engañarse con un backtest |
| **4. Práctica: ejecución sistemática** | 36 Carver → 37 Chan → 39 Lefèvre → 40 Schwager | Convertir reglas en un sistema operable y reconocer la psicología del operador |

Satélites 2023-2026, que se leen después de su libro madre: *The Missing Billionaires* (después de 19), *Causal Factor Investing* (después de 35), *The Corporate Life Cycle* (después de 15), *The Fund* (después de 33), *Noise* (después de 1) y AFTS (después de 36).

### 6.2 Reglas: del libro al parámetro

| # | Regla | Libros | Parámetro |
|---|---|---|---|
| R1 | **Regla:** la supervivencia manda. Límite duro de drawdown de −20% (estándar) y −35% (arena); apalancamiento bruto de 1.0 en la fase 1; ninguna estrategia apalancada con sesgo negativo | 4, 7, 20, 17 | `drawdown_maximo_duro`, `cortacircuitos_drawdown`, `apalancamiento.bruto_max_fase_1` |
| R2 | **Regla:** tamaño = mín(fracción × Kelly estimado con la ventaja recortada 50%, tope de concentración) | 18, 19, 37, *Missing Billionaires* | `kelly.fraccion_max` 0.25 (arena 0.5); `riesgo_por_operacion` 1% (arena 3%; 0.5% en fase de prueba) |
| R3 | **Regla:** costos primero. Núcleo en índices baratos; una idea satélite solo entra si su ventaja esperada supera varias veces el costo de ida y vuelta (~0.58% en el SIC, cap. 15) | 21, 22, 25, 36 | `estructura.nucleo_min` 0.70 (estándar) |
| R4 | **Regla:** toda compra discrecional lleva valor conservador, escenario bajista escrito y DCF inverso (qué descuenta el precio) | 9, 13, 15, 16 | Plantilla de ficha-empresa; `riesgo_por_operacion` |
| R5 | **Regla:** toda tesis se registra con probabilidad y fecha, y se califica con Brier | 1, 2, 3, 5 | `pronosticos.brier_objetivo` 0.20; `min_pronosticos_para_evaluar` 50 |
| R6 | **Regla:** no juzgar una estrategia por su resultado antes de tener muestra suficiente | 3, 5, 40 | `paper_trading_min_meses` 3; `paper_trading_min_operaciones` 30; `rachas` 3→×0.5, 5→pausa |
| R7 | **Regla:** ningún backtest pasa sin 10 años con costos, DSR ≥ 0.95 y PBO ≤ 0.25; el Sharpe del backtest se recorta antes de dimensionar | 35, 36, 37 | `validacion_estrategias.*` |
| R8 | **Regla:** el termómetro de ciclo solo mueve la exposición táctica dentro de las bandas; nunca se pasa todo a dentro o a fuera | 17, 30-34 | `rebalanceo` (bandas de 5 pp absolutas y 25% relativas); `satelite_max` 0.30 |
| R9 | **Regla:** ETFs apalancados solo con tendencia a favor y sin promediar a la baja | 39, 40, 36 | `filtro_apalancados` (MA200 y VIX < 25); `etf_apalancado_max` 0.5 |
| R10 | **Regla:** concentrar solo con una ventaja documentada y dentro de topes | 6, 10, 11 contra 22, 24 | `accion_individual_max` 0.10 (arena 0.30); `sector_max` 0.25 |
| R11 | **Regla:** en la temporada de 6 meses domina la suerte; la varianza se usa como palanca del torneo, no como sustituto de la ventaja | 5, 18, 19 | `modo_torneo` (±5 pp contra el mejor rival) |
| R12 | **Regla:** cada ventaja tiene fecha de caducidad; se revisa si sigue viva después de 5 pérdidas seguidas o de una caída de Sharpe fuera de muestra | 28, 18, 14 | `rachas.perdedoras_para_pausa` 5 |

### 6.3 Checklist del canon antes de cualquier operación, de papel o real (10 preguntas)

1. ¿Qué descuenta el precio y en qué difiero del consenso? (16, 17)
2. ¿Cuál es la tasa base de este tipo de situación? (1, 2, 5)
3. ¿Qué probabilidad y qué fecha le pongo a la tesis? (2, 3)
4. ¿Cómo fracasaría? Pre-mortem e inversión del problema (3, 6)
5. ¿Cuál es la pérdida máxima plausible y cabe en `riesgo_por_operacion`? (4, 20)
6. ¿El tamaño sale de Kelly fraccional con la ventaja recortada? (18, 19)
7. ¿Quién está del otro lado y por qué me vende? (27, 13)
8. ¿Hay apalancamiento o iliquidez que me obliguen a vender en el peor momento? (20, 31)
9. ¿La idea sobrevive a los costos de GBM y al tipo de cambio? (22, 36)
10. ¿Qué evidencia me haría salir? Criterio de abandono escrito (3, 39)

### 6.4 Protocolo para extraer un libro nuevo

Para cada libro que entre a la biblioteca: (a) la tesis como hipótesis falsable; (b) la mejor evidencia independiente a favor y en contra, con su grado; (c) una regla candidata; (d) el parámetro al que afecta; (e) una prueba en papel de al menos 3 meses antes de adoptarla. Sin los pasos (b) y (e), el libro se queda como lectura y no se vuelve regla.

## 7. Trampas y errores comunes

1. **Leer a los ganadores como si fueran una muestra.** Los autores-practicantes son sobrevivientes, y los que quebraron no escribieron libro (cap. 18).
2. **Tomar un backtest publicado como resultado fuera de muestra.** El ~30% de la fórmula mágica era del autor; la réplica independiente dio mucho menos.
3. **Trasladar consejos institucionales a MXN 20,000.** Swensen (ilíquidos), Carver (futuros diversificados) y Buffett (float y capital permanente) no se escalan hacia abajo.
4. **Usar a Taleb para justificar la compra permanente de puts.** La tesis de las colas es A; esa estrategia es D (cap. 05).
5. **Usar a Lefèvre o a Market Wizards para justificar piramidar con apalancamiento.** Livermore quebró varias veces.
6. **Usar a Dalio, Shiller o Marks como reloj.** Diagnostican bien la etapa, pero no dan la fecha.
7. **Citar a Kahneman sin fe de erratas.** El capítulo de priming no replica.
8. **Confundir el error de Reinhart-Rogoff con el libro.** El error estaba en el paper de 2010; el libro de 2009 es otra cosa.
9. **Leer una edición vieja.** Hay que usar la 7.ª de *Security Analysis*, la 3.ª revisada de *The Intelligent Investor*, la 13.ª de Malkiel, la 6.ª de Siegel, la 8.ª de Kindleberger y la 4.ª de *Investment Valuation*.
10. **Leer sin convertir.** Una lección que no termina en regla y en parámetro se evapora (6.4).
11. **Kelly completo porque "es el óptimo".** Solo lo es con la ventaja conocida; con una ventaja estimada, es sobreapostar.
12. **"Invierte en lo que conoces" como regla de selección.** Es sesgo de familiaridad, no una ventaja.

## 8. Examen de titulación

1. **¿Cuál es la edición vigente de los dos libros de Graham?** *The Intelligent Investor*: 3.ª edición revisada con comentarios de Zweig (Harper Business, 2024), que parte de la 4.ª edición revisada de 1973. *Security Analysis*: 7.ª edición (McGraw-Hill, 27-jun-2023, con Klarman).
2. **¿Qué pensaba Graham en los años 70 sobre el análisis extenso?** Dudaba de que produjera selecciones lo bastante superiores como para justificar su costo, y se acercó a la escuela del mercado eficiente.
3. **Describe el experimento de Haghani y Dewey y su resultado.** 61 personas, US$25, moneda con 60% de cara, tope de US$250, 30 minutos. El 28% quebró, el 21% llegó al tope y el pago promedio fue de US$91. Kelly indicaba 20% por tiro.
4. **¿Por qué Kelly fraccional?** Porque la ventaja se estima con error: apostar el doble de Kelly baja el crecimiento a la tasa libre de riesgo. Un cuarto de Kelly obtiene 43.75% del crecimiento máximo con 25% de la volatilidad (cap. 01). Samuelson: con N grande, cuando se pierde, se pierde en grande.
5. **Da las cifras clave de LTCM.** Más de 25:1 a principios de 1998; perdió US$4.6 mil millones en menos de 4 meses; su capital cayó de US$4.7 mil millones a US$400 millones (25-sep-1998); recapitalización de US$3.625 mil millones con 14 instituciones, organizada por la Fed de Nueva York.
6. **¿Qué parte de *Thinking, Fast and Slow* no replicó?** El capítulo 4 (priming), con un R-index de 14. Kahneman reconoció que confió demasiado en estudios con poco poder estadístico.
7. **¿Qué logró el Good Judgment Project?** Ganó las dos temporadas de IARPA-ACE con una precisión 35-72% mayor que la de los otros equipos. Sus mejores pronosticadores fueron ~30% mejores que analistas con información clasificada. Todo se midió con Brier.
8. **¿Qué encontró McQuarrie sobre Siegel?** Que en 1797-1942 las acciones rindieron casi lo mismo que los bonos, y que Siegel subestimó los rendimientos de los bonos del siglo XIX en ~1.5 pp.
9. **¿Dónde estuvo el error de Reinhart-Rogoff y de qué tamaño fue?** En *Growth in a Time of Debt* (2010), no en el libro: con deuda de más de 90% del PIB el crecimiento reportado era −0.1% y el corregido, 2.2% (Herndon-Ash-Pollin, 2013).
10. **¿Qué dice la evidencia independiente sobre la fórmula mágica?** EUA 2003-2015: 11.4% contra 8.7% del S&P, con rezago en 2007-2011 y más volatilidad. Un estudio de 2024 (1963-2022) la explica sobre todo con factores conocidos. El ~30% del libro era un backtest del propio autor.
11. **Medallion: cifras y por qué no se transfiere.** 66% bruto y 39% neto anual (1988-2018). El fondo abierto a externos (RIEF) quedó muy por debajo. Horizonte corto, capacidad cerrada y una infraestructura que no se puede copiar.
12. **¿Qué corrige el Deflated Sharpe Ratio y qué umbral usa el sistema?** Corrige el sesgo de selección por pruebas múltiples y la no normalidad (Bailey y López de Prado, JPM 2014). Umbrales del sistema: `deflated_sharpe_min_probabilidad` 0.95 y `pbo_max` 0.25.
13. **Lynch: rendimiento y crítica.** 29.2% contra 15.8% del S&P (1977-1990). "Invierte en lo que conoces" coincide con el sesgo de familiaridad (Huberman, RFS 2001), y Lynch tenía cientos de acciones y un equipo de análisis.
14. **¿Qué agrega la 8.ª edición de Kindleberger y cuáles son las cinco etapas?** Agrega cripto y el papel de EUA y la Fed como prestamista global (con McCauley). Etapas: desplazamiento → auge con crédito → euforia → dificultad financiera → pánico.
15. **¿Por qué el grado de un libro es el mínimo entre su evidencia y su aplicabilidad?** Porque una lección verdadera pero inaplicable a MXN 20,000 ejecutados a mano en GBM (el float de Buffett, los ilíquidos de Swensen, la infraestructura de Medallion) no produce rendimiento en esta cuenta.

## 9. Fuentes

1. Wikipedia, *The Intelligent Investor* (ediciones; 3.ª ed. revisada, Harper Business, 2024, ISBN 9780063356733): https://en.wikipedia.org/wiki/The_Intelligent_Investor
2. Wikipedia, *Security Analysis* (ediciones; 7.ª ed., 27-jun-2023; cita de Graham en los años 70; "Superinvestors of Graham-and-Doddsville"): https://en.wikipedia.org/wiki/Security_Analysis_(book)
3. Wikipedia, Philip Fisher / *Common Stocks and Uncommon Profits*: https://en.wikipedia.org/wiki/Common_Stocks_and_Uncommon_Profits
4. Open Library, *The Essays of Warren Buffett* (ediciones de 1997 a 2023): https://openlibrary.org/works/OL18072192W · https://openlibrary.org/works/OL20374816W
5. Wikipedia, *One Up on Wall Street* y Peter Lynch: https://en.wikipedia.org/wiki/One_Up_on_Wall_Street · https://en.wikipedia.org/wiki/Peter_Lynch
6. Wikipedia, Howard Marks: https://en.wikipedia.org/wiki/Howard_Marks_(investor)
7. Wikipedia, Seth Klarman: https://en.wikipedia.org/wiki/Seth_Klarman
8. Wikipedia, Joel Greenblatt y Magic formula investing (réplicas, estudio de 2024): https://en.wikipedia.org/wiki/Joel_Greenblatt · https://en.wikipedia.org/wiki/Magic_formula_investing
9. Damodaran, página de libros (4.ª ed. de *Investment Valuation*; *Corporate Life Cycle*, ago-2024): https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm · Open Library: https://openlibrary.org/works/OL21035837W · https://en.wikipedia.org/wiki/Aswath_Damodaran
10. Wikipedia, Michael J. Mauboussin: https://en.wikipedia.org/wiki/Michael_J._Mauboussin · Open Library, *Expectations Investing* (2001, 2021): https://openlibrary.org/search?q=expectations+investing+mauboussin
11. Wikipedia, Edward O. Thorp: https://en.wikipedia.org/wiki/Edward_O._Thorp
12. Wikipedia, Kelly criterion (Samuelson; experimento de Haghani-Dewey): https://en.wikipedia.org/wiki/Kelly_criterion
13. Open Library, *Fortune's Formula* (Hill and Wang, 2005): https://openlibrary.org/search?q=fortune%27s+formula+poundstone
14. Wikipedia, *Fooled by Randomness* y *The Black Swan*: https://en.wikipedia.org/wiki/Fooled_by_Randomness · https://en.wikipedia.org/wiki/The_Black_Swan:_The_Impact_of_the_Highly_Improbable
15. Wikipedia, *Thinking, Fast and Slow* (crisis de replicación) y Daniel Kahneman: https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow · https://en.wikipedia.org/wiki/Daniel_Kahneman
16. Wikipedia, Good Judgment Project: https://en.wikipedia.org/wiki/Good_Judgment_Project
17. Wikipedia, Annie Duke: https://en.wikipedia.org/wiki/Annie_Duke
18. Wikipedia, George Soros (reflexividad, Quantum, 1992): https://en.wikipedia.org/wiki/George_Soros
19. Wikipedia, *Reminiscences of a Stock Operator*: https://en.wikipedia.org/wiki/Reminiscences_of_a_Stock_Operator
20. Wikipedia, Jack D. Schwager: https://en.wikipedia.org/wiki/Jack_D._Schwager
21. Wikipedia, Ray Dalio y *Principles*: https://en.wikipedia.org/wiki/Ray_Dalio · https://en.wikipedia.org/wiki/Principles_(Dalio_book)
22. Wiley, *Investing Amid Low Expected Returns* (abr-2022): https://www.wiley.com/en-us/Investing+Amid+Low+Expected+Returns%3A+Making+the+Most+When+Markets+Offer+the+Least-p-9781119860198 · Open Library, *Expected Returns*: https://openlibrary.org/search?q=expected+returns+ilmanen
23. Wikipedia, Lasse Heje Pedersen: https://en.wikipedia.org/wiki/Lasse_Heje_Pedersen · Open Library: https://openlibrary.org/search?q=efficiently+inefficient+pedersen
24. Wikipedia, David F. Swensen: https://en.wikipedia.org/wiki/David_F._Swensen
25. Wikipedia, John C. Bogle: https://en.wikipedia.org/wiki/John_C._Bogle
26. Open Library, *Against the Gods* (Wiley, 1996): https://openlibrary.org/search?q=against+the+gods+bernstein
27. Wikipedia, *A Random Walk Down Wall Street* (13.ª ed., 2023): https://en.wikipedia.org/wiki/A_Random_Walk_Down_Wall_Street
28. Wikipedia, *Stocks for the Long Run* (6.ª ed., 2022; crítica de McQuarrie): https://en.wikipedia.org/wiki/Stocks_for_the_Long_Run · McQuarrie (2024), FAJ 80(1): https://www.tandfonline.com/doi/abs/10.1080/0015198X.2023.2268556
29. Princeton UP, *Triumph of the Optimists*: https://press.princeton.edu/books/hardcover/9780691091945/triumph-of-the-optimists · UBS Yearbook 2026: https://www.ubs.com/content/dam/assets/wm/static/cio/documents/giry2026-summary-public.pdf
30. Wikipedia, Andrew Lo y Adaptive market hypothesis: https://en.wikipedia.org/wiki/Andrew_Lo · https://en.wikipedia.org/wiki/Adaptive_market_hypothesis
31. Wikipedia, *Irrational Exuberance*: https://en.wikipedia.org/wiki/Irrational_Exuberance_(book)
32. Springer, *Manias, Panics, and Crashes*, 8.ª ed. (2023): https://www.springerprofessional.de/en/manias-panics-and-crashes/24098366
33. Wikipedia, *Growth in a Time of Debt*: https://en.wikipedia.org/wiki/Growth_in_a_Time_of_Debt · Princeton UP, *This Time Is Different*: https://press.princeton.edu/books/paperback/9780691152646/this-time-is-different
34. Bailey y López de Prado (2014), "The Deflated Sharpe Ratio", JPM: https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
35. López de Prado (2023), *Causal Factor Investing*, Cambridge Elements: https://doi.org/10.1017/9781009397315
36. Open Library, *Advances in Financial Machine Learning* (Wiley, 2018) y *Machine Learning for Asset Managers* (2020): https://openlibrary.org/search?q=advances+in+financial+machine+learning
37. Blog de Robert Carver (AFTS, abr-2023; libro anunciado para dic-2026): https://qoppac.blogspot.com/ · Open Library: https://openlibrary.org/search?q=systematic+trading+carver
38. Open Library, *Quantitative Trading*, 2.ª ed. (Wiley, 2021): https://openlibrary.org/works/OL25274055W
39. Wikipedia, Renaissance Technologies (cita de Zuckerman: 66% y 39%; RIEF): https://en.wikipedia.org/wiki/Renaissance_Technologies
40. Wikipedia, *When Genius Failed* y LTCM: https://en.wikipedia.org/wiki/When_Genius_Failed · https://en.wikipedia.org/wiki/Long-Term_Capital_Management
41. Open Library, obras de Morgan Housel: https://openlibrary.org/search?q=morgan+housel
42. Wikipedia, John H. Cochrane: https://en.wikipedia.org/wiki/John_H._Cochrane · NBER w16972, "Discount Rates": https://www.nber.org/papers/w16972
43. Wikipedia, *Poor Charlie's Almanack* y Charlie Munger: https://en.wikipedia.org/wiki/Poor_Charlie%27s_Almanack · https://en.wikipedia.org/wiki/Charlie_Munger
44. Wiley, *The Missing Billionaires* (sep-2023): https://www.wiley.com/en-us/The+Missing+Billionaires%3A+A+Guide+to+Better+Financial+Decisions-p-9781119747918
45. Huberman (2001), "Familiarity Breeds Investment", RFS 14(3): https://academic.oup.com/rfs/article-abstract/14/3/659/1578906
46. Berkshire Hathaway, carta de 2025 (cifras en el cap. 03): https://www.berkshirehathaway.com/letters/2025ltr.pdf
47. S&P DJI, SPIVA (cifras en el cap. 01): https://www.spglobal.com/spdji/en/spiva/article/spiva-us/
48. Open Library, API de búsqueda (verificación de años y ediciones): https://openlibrary.org/developers/api

**Registro de verificación (2026-09-25).** WebSearch no estuvo disponible (cuota de la sesión agotada). Se hicieron ~30 lecturas con WebFetch (Wikipedia, Wiley, Springer, Princeton UP, Cambridge, NBER, OUP, Stern/NYU y el PDF de Bailey y López de Prado), ~60 extractos de Wikipedia por API y ~90 consultas a la API de Open Library (títulos, autores, primer año y ediciones). **No verificado:** el número de la edición de 2019 de *The Essays of Warren Buffett* y si existen ediciones posteriores a la de Wiley de 2021; el título del artículo de Samuelson de 1979 contra Kelly; la crítica de Pedersen (FAJ 2018) a la "aritmética" de Sharpe; el contenido del libro de Carver anunciado para dic-2026; la fecha exacta de la muerte de Simons.
